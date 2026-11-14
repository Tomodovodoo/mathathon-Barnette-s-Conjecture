"""Deterministic, counted regression campaign. Run with python -m barnette_lab.campaign.

External referees are imported read-only, with bytecode writes disabled. Assertions
are deliberately explicit so the new checks remain active under python -O.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import importlib.util
from itertools import combinations, product
import json
from math import comb, prod
from pathlib import Path
import sys
import time
import networkx as nx
from .core import Instance, edge, plantri_graphs, faces_of
from .algorithms import (separators, pool, alpha, beta, marked_walk,
                         exchange_walk, determinant_sample, white_ground)
from .li import LiObjects, LiMultiObjects

ROOT = Path(__file__).resolve().parents[3]
RESEARCH = ROOT / 'research'


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def external(folder, filename):
    path = RESEARCH / folder / 'code' / filename
    spec = importlib.util.spec_from_file_location('lab_ref_' + path.stem, path)
    module = importlib.util.module_from_spec(spec)
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


class Coverage:
    def __init__(self):
        self.rows = defaultdict(lambda: [0, 0, 0])
        self.current = Counter()

    def hit(self, check, objects=1):
        self.current[check] += objects

    def finish(self):
        for check, objects in self.current.items():
            row = self.rows[check]
            row[0] += bool(objects)
            row[1] += objects
            row[2] += not bool(objects)
        self.current.clear()

    def table(self):
        lines = ['| check | instances | objects | vacuous count |',
                 '| --- | ---: | ---: | ---: |']
        lines += [f'| {k} | {v[0]} | {v[1]} | {v[2]} |' for k, v in sorted(self.rows.items())]
        return '\n'.join(lines)


def inside(b, edges):
    d = b.G.copy()
    d.remove_edges_from(b.dual_edges[edge(*e)] for e in edges)
    return set(d) - nx.node_connected_component(d, b.outer)


def state_cycles(b, states, exhaustive):
    """Include cycles of arbitrary outgoing choices, not just disjoint pairs."""
    seen = set()
    for r in states:
        choices = [[v for v in b.faces[t] if v != a] for t, a in zip(b.A, r)]
        heads = product(*choices) if exhaustive else (s for s in states if all(a != z for a, z in zip(r, s)))
        for s in heads:
            d = nx.DiGraph(zip(r, s))
            for c in nx.simple_cycles(d):
                es = tuple(sorted(edge(a, z) for a, z in zip(c, c[1:] + c[:1])))
                if es not in seen:
                    seen.add(es)
                    yield c, es


def regions(b, cov, exhaustive):
    # All connected induced K up to order 10. At larger orders use all
    # triples plus deterministic prefixes and complements of single vertices.
    vertices = sorted(b.T)
    subsets = (combinations(vertices, k) for k in range(3, len(vertices) + 1)) if exhaustive else (
        combinations(vertices, 3), [vertices[:k] for k in range(4, len(vertices) + 1)],
        [set(vertices) - {v} for v in vertices])
    for family in subsets:
        for subset in family:
            k = b.T.subgraph(subset)
            if not nx.is_connected(k):
                continue
            d = b.G.copy()
            d.remove_edges_from(b.dual_edges[edge(*e)] for e in k.edges())
            terms = 0
            for region in nx.connected_components(d):
                length = sum(int(b.sides[u,v] in region) + int(b.sides[v,u] in region) for u,v in k.edges())
                balance = len(region & set(b.black)) - len(region & set(b.white))
                signed = sum((1 if f in b.black else -1) for u,v in k.edges()
                             for f in (b.sides[u,v], b.sides[v,u]) if f in region)
                require(3 * balance == signed, 'region signed boundary')
                if length >= 4:
                    require(abs(balance) <= length - 4, 'bound 3.3')
                    cov.hit('bound 3.3 regions')
                if len(region) > 1:
                    terms += balance - length + 4
            black = sum(set(b.faces[t]) <= set(subset) for t in b.black)
            defect = k.number_of_edges() - black - 2 * len(subset) + 4
            require(2 * defect == terms, 'exact Euler identity')
            cov.hit('Euler induced regions')
            if len(subset) >= 4 and not separators(b):
                require(defect <= 0, 'bound 3.4')
                cov.hit('bound 3.4 connected subsets')


def independent(b, ss, pairs, cov, referee):
    other = referee.Tri(b.T.edges(), b.faces[b.outer])
    by_face = {frozenset(f): i for i, f in enumerate(other.faces)}
    order = [other.A.index(by_face[frozenset(b.faces[t])]) for t in b.A]
    convert = lambda s: tuple(s[i] for i in order)
    require(set(ss) == {convert(s) for s in other.states()}, 'independent states')
    require(set(pairs) == {(convert(r), convert(s)) for r,s in other.pairs()}, 'independent pairs')
    require({s for s in ss if b.is_tree(s)} == {convert(s) for s in other.states() if other.is_tree_state(s)}, 'independent good states')
    # Tri chooses a global orientation independently. Align once on an edge.
    u,v = next(iter(b.T.edges()))
    mirror = b.delta(u,v) * other.delta(u,v)
    for r,s in other.pairs():
        require(b.sign(convert(r), convert(s)) == other.eps(r,s) * mirror ** b.n, 'independent signs')
    for check, count in [('independent states', len(ss)), ('independent pairs', len(pairs)),
                         ('independent good states', sum(b.is_tree(s) for s in ss)), ('independent signs', len(pairs))]:
        cov.hit(check, count)


def recovery_state(b, selected, e0):
    forest = nx.Graph()
    forest.add_nodes_from(b.T)
    forest.add_edges_from(set(selected) - {e0})
    parent = {}
    for root in sorted(b.R):
        for a,z in nx.bfs_edges(forest, root):
            parent[z] = a
    out = []
    for t in b.A:
        es = [e for e in selected if set(e) <= set(b.faces[t])]
        require(len(es) == 1, 'one selected edge per black face')
        u,v = es[0]
        out.append(u if parent.get(u) == v else v)
    return tuple(out)


def hamiltonian_sets(g, forbidden):
    start = min(g)
    def visit(path, used):
        if len(path) == len(g):
            if g.has_edge(path[-1], start) and path[1] < path[-1] and edge(path[-1], start) != forbidden:
                yield frozenset(edge(a,z) for a,z in zip(path, path[1:] + path[:1]))
            return
        for z in sorted(g[path[-1]]):
            if z not in used and edge(path[-1], z) != forbidden:
                yield from visit(path + [z], used | {z})
    yield from visit([start], {start})


def check_instance(b, cov, referee, fp, exhaustive_disk=False, exhaustive_regions=False, reverse_image=False, li=False):
    checks = ['state disk W=B+1', 'pair local sign and closed formula', 'Lean phase ratio',
              'Q cancellation partnered states', 'Q reversal objects', 'pair criterion',
              'good unique partner', 'even good states', 'directed good-pair criterion',
              'cover components', 'cycle white-face weight', 'lowest finite difference',
              'recovery injectivity', 'recovery image', 'heights path independence',
              'height cycle increments', 'marked constructors', 'marked nonfixed moves',
              'ordered token involutions', 'exchange adjacency', 'exchange walks',
              'bound 3.3 regions', 'bound 3.4 connected subsets', 'Euler induced regions']
    for check in checks:
        cov.hit(check, 0)
    ss = list(b.states()); pairs = b.pairs(ss); ps = set(pairs)
    sep = separators(b)
    require(bool(pairs) == (not any(z[2] for z in sep)), 'exact pair criterion')
    cov.hit('pair criterion')
    if any(z[2] for z in sep): cov.hit('property black inner separator')
    if any(not z[2] for z in sep): cov.hit('property white inner separator')
    if pairs: cov.hit('property has pair')
    trees = [s for s in ss if b.is_tree(s)]
    require(len(trees) % 2 == 0, 'even good states')
    cov.hit('even good states', len(ss))
    for s in trees:
        require(sum(z == s for _,z in pairs) == 1, 'unique partner')
        cov.hit('good unique partner')
    for s in ss:
        mates = [r for r,z in pairs if z == s]
        if b.qcycles(s) and mates:
            require(sum(b.sign(r,s) for r in mates) == 0, 'nonvacuous cancellation')
            cov.hit('Q cancellation partnered states')
            for r in mates:
                for c in b.qcycles(s):
                    q = b.reverse_q((r,s),c)
                    require(q in ps and q != (r,s) and q[1] == s and b.reverse_q(q,c) == (r,s), 'Q involution')
                    require(b.sign(*q) == -b.sign(r,s), 'Q sign reversal')
                    cov.hit('Q reversal objects')
    for c, es in state_cycles(b, ss, exhaustive_disk):
        ins = inside(b, es)
        black = len(ins & set(b.black)); white = len(ins & set(b.white))
        require(white == black + 1, 'state disk W=B+1')
        cov.hit('state disk W=B+1')
    groups = defaultdict(list)
    I = fp.Inst(b.faces, b.outer)
    paths1 = I.tree_paths('bfs+'); paths2 = I.tree_paths('dfs')
    cr1 = I.path_crossings(paths1); cr2 = I.path_crossings(paths2)
    def height(s, cr):
        return {w: sum(a for k,v,a,_ in cr[w] if s[k] == v) for w in b.white}
    heights = {s: height(s,cr1) for s in ss}
    for s in ss:
        require(all(heights[s][w] - heights[ss[0]][w] == height(s,cr2)[w] - height(ss[0],cr2)[w] for w in b.white), 'path independent relative signed height')
        cov.hit('heights path independence', len(b.white))
    a = b.weights()
    for p in pairs:
        r,s = p; j = b.J(*p)
        local = prod(b.delta(u,v) for u,v in zip(r,s))
        require(local == b.sign(*p) == (-1) ** ((b.n + j)//2), 'local/closed sign')
        require((1j)**((b.n-3*j) % 4) == local and local / (1j)**(j % 4) == (1j)**(b.n % 4), 'Lean phase ratio')
        cov.hit('pair local sign and closed formula'); cov.hit('Lean phase ratio')
        f = nx.DiGraph()
        for t,u,v in zip(b.A,r,s):
            third, = set(b.faces[t]) - {u,v}
            f.add_edge(('v',third), ('t',t)); f.add_edge(('t',t), ('v',u))
        require(nx.is_directed_acyclic_graph(f) == b.is_tree(s), 'directed criterion')
        cov.hit('directed good-pair criterion')
        es = [edge(u,v) for u,v in zip(r,s)]
        g = b.G.copy(); g.remove_edges_from(b.dual_edges[e] for e in es)
        cycles = b.dcycles(*p)
        require(len(cycles) == nx.number_connected_components(g) - 1, 'cover component identity')
        cov.hit('cover components')
        groups[tuple(sorted(es))].append(p)
        for c in cycles:
            edges = [edge(r[b.A.index(t)],s[b.A.index(t)]) for t in c]
            ins = inside(b,edges); whites = len(ins & set(b.white))
            require(len(pool(b,p,c,True)) - len(pool(b,p,c,False)) == whites, 'white-face cycle weight')
            q = b.reverse_d(p,c)
            diff = {w: heights[q[1]][w] - heights[s][w] for w in b.white}
            nonzero = {diff[w] for w in b.white if w in ins}
            require(len(nonzero) == 1 and nonzero <= {-1,1} and all(diff[w] == 0 for w in b.white if w not in ins), 'height cycle indicator')
            cov.hit('cycle white-face weight'); cov.hit('height cycle increments', len(b.white))
        for q in b.neighbors(p):
            require(q in ps and p in b.neighbors(q) and b.sign(*q) == -b.sign(*p), 'exchange adjacency')
            cov.hit('exchange adjacency')
        result, stats = marked_walk(b,p,cap=10000)
        require(b.is_tree(result[1]), 'marked walk')
        cov.hit('marked constructors'); cov.hit('marked nonfixed moves',stats['moves'])
        result, moves = exchange_walk(b,p,seed=17,cap=10000)
        require(result is not None and b.is_tree(result[1]), 'exchange walk')
        cov.hit('exchange walks', moves + 1)
        for token in [(t,k) for t,v in zip(b.A,s) for k in range(1,a[t,v]+1)]:
            obj = p,(token,)
            for inv in (alpha,beta):
                image = inv(b,obj)
                require(inv(b,image) == obj and (image == obj or b.sign(*image[0]) == -b.sign(*p)), 'token involution')
                cov.hit('ordered token involutions')
    if pairs:
        m = min(len(b.dcycles(*p)) for p in pairs)
        cov.hit(f'property m={m}')
        expected = 0
        for group in groups.values():
            p = group[0]; cs = b.dcycles(*p)
            if len(cs) == m:
                expected += prod(len(pool(b,p,c,True))-len(pool(b,p,c,False)) for c in cs)
        poly = b.polynomial(pairs)
        for k in range(m):
            require(sum(v * comb(e,k) for e,v in poly.items() if e >= k) == 0, 'lower finite difference')
        require(sum(v * comb(e,m) for e,v in poly.items() if e >= m) == (-1)**((b.n-m)//2)*expected, 'exact lowest coefficient')
        cov.hit('lowest finite difference',len(groups))
    for e0 in combinations(b.faces[b.outer],2):
        e0 = edge(*e0); images = set()
        for s in trees:
            cert = b.recover(s,e0)
            require(recovery_state(b,cert['P'],e0) == s, 'recovery left inverse')
            image = frozenset(edge(u,v) for u,v in zip(cert['cycle'], cert['cycle'][1:]+cert['cycle'][:1]))
            require(image not in images, 'recovery injectivity'); images.add(image)
            cov.hit('recovery injectivity')
        if reverse_image:
            for image in hamiltonian_sets(b.G,b.dual_edges[e0]):
                selected = {e for e,d in b.dual_edges.items() if d not in image}
                s = recovery_state(b,selected,e0)
                require(b.valid(s) and ((image in images) == b.is_tree(s) == any(z == s for _,z in pairs)), 'recovery exact image')
                cov.hit('recovery image')
    if len(b.T) <= 12:
        independent(b,ss,pairs,cov,referee)
    regions(b,cov,exhaustive_regions)
    if li and pairs:
        compare_li(b,pairs,cov,fp)
    return {'vertices':len(b.T),'states':len(ss),'pairs':len(pairs),'good':len(trees),
            'm':min((len(b.dcycles(*p)) for p in pairs),default=None)}


def compare_li(b,pairs,cov,fp):
    I = fp.Inst(b.faces,b.outer)
    m = min(len(b.dcycles(*p)) for p in pairs)
    lab = (LiObjects if m == 1 else LiMultiObjects)(b)
    cr, ori = I.ray_crossings(lab.pos,(0,1),lab.centers)
    require(cr is not None, 'generic lab rays')
    model = fp.Model(I,cr)
    def convert(obj):
        p,marks = obj
        marks = tuple(sorted((w,b.A[cr[w][i][0]]) for w,i in marks))
        return p, (marks[0] if m == 1 else marks)
    obs = list(model.objects()); labobs = set(lab.objects(pairs))
    require({convert(o) for o in obs} == labobs, 'Li objects independent equality')
    signs = set()
    for o in obs:
        q = convert(o)
        require(convert(model.iota1(o)) == lab.iota1(q), 'Li iota1 comparison')
        require(convert(model.iota2(o)) == lab.iota2(q), 'Li iota2 comparison')
        signs.add(model.sign(o) * (-1)**lab.sign(q))
        for inv in (lab.iota1,lab.iota2):
            image = inv(q)
            require(image in labobs and inv(image) == q and (image == q or lab.sign(image) != lab.sign(q)), 'Li closure involution sign')
        cov.hit('Li independent objects and maps')
    require(len(signs) == 1, 'Li signs differ only by global convention')
    cov.hit('Li independent signed convention',len(obs))


def sampler(b,cov,samples=1800):
    ss = list(b.states())
    # Compute every conditional determinant probability exactly, independently
    # compare each residual determinant to brute-force completion counts.
    for s in ss:
        probability = Fraction(1)
        for i in range(b.n):
            completions = [z for z in ss if z[:i] == s[:i]]
            weights = {}
            for v in sorted(set(b.faces[b.A[i]]) & set(b.X) - set(s[:i])):
                cols = [j for j,x in enumerate(b.X) if x not in set(s[:i]) | {v}]
                count = abs(int(b.K.extract(list(range(i+1,b.n)),cols).det()))
                require(count == sum(z[i] == v for z in completions),'residual determinant count')
                weights[v] = count
            probability *= Fraction(weights[s[i]],sum(weights.values()))
        require(probability == Fraction(1,len(ss)),'exact uniform state probability')
        cov.hit('sampler exact probability')
    hist = Counter(determinant_sample(b,912700+i) for i in range(samples))
    require(set(hist) <= set(ss),'sample support')
    expected = samples / len(ss)
    chi = sum((hist[s]-expected)**2/expected for s in ss)
    # Laurent-Massart chi-square upper tail, alpha < exp(-14), generous fixed
    # cutoff avoids a fragile test while detecting severe sampler bias.
    df = len(ss)-1
    cutoff = df + 2*(14*df)**0.5 + 28
    require(chi < cutoff, f'chi square {chi} >= {cutoff}')
    cov.hit('sampler seeded chi square',samples)
    return {'states':len(ss),'samples':samples,'chi_square':chi,'df':df,'cutoff':cutoff}


def special_instances():
    # File renamed since the brief: example.json is now running.json.
    data = json.loads((ROOT/'paper/figures/running.json').read_text())
    faces = data['faces']
    g = nx.Graph(e for f in faces for e in combinations(f,2))
    initial = Instance(g)
    # Use the retained root triangle, not an embedding-dependent face ID.
    root = data.get('outer',data.get('t0',0))
    if isinstance(root,list): rootset = set(root)
    else: rootset = set(faces[root])
    yield 'running', Instance(g,next(i for i,f in enumerate(initial.faces) if set(f)==rootset))
    import ast, re
    text = (RESEARCH/'2026-11-14_fable_route-combinatorics/data/counterexamples.txt').read_text()
    section = text.split('E3 refuted:')[1].split('==============================================================================')[0]
    faces = ast.literal_eval(re.search(r'\[\(.*\)\]',section).group())
    g = nx.Graph(e for f in faces for e in combinations(f,2)); initial=Instance(g)
    yield 'minimal_cover_no_good_16', Instance(g,next(i for i,f in enumerate(initial.faces) if set(f)==set(faces[8])))
    data=json.loads((RESEARCH/'2026-11-14_opus_conjectures/data/c2_counterexample_V18.json').read_text())
    g=nx.Graph(data['edges']); initial=Instance(g)
    yield 'lattice_18', Instance(g,next(i for i,f in enumerate(initial.faces) if set(f)==set(data['roots'])))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tier',choices=['quick','full'],default='quick')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    started=time.perf_counter(); cov=Coverage(); rows=[]
    referee=external('2026-11-14_fable_referee-determinants','etri.py')
    fp=external('2026-11-14_fable_referee-involutions-v2','fp.py')
    exe=ROOT/'workings/barnette_lab/vendor/plantri.exe'
    require(exe.exists(),'Run python workings/barnette_lab/setup_plantri.py first')
    maximum=14 if args.tier=='full' else 10
    for n in range(6,maximum+1):
        for index,g in enumerate(plantri_graphs(n,exe)):
            for root in range(2*len(g)-4):
                b=Instance(g,root)
                name=f'plantri_{n}_{index}_root_{root}'
                rec=check_instance(b,cov,referee,fp,exhaustive_disk=n<=8,
                                   exhaustive_regions=n<=8 or (n<=10 and root==0),
                                   reverse_image=n<=8,li=n<=12)
                rec['name']=name; rows.append(rec); cov.finish()
        print(f'completed order {n}: {len(rows)} rooted runs',flush=True)
    for name,b in special_instances():
        rec=check_instance(b,cov,referee,fp,li=True)
        rec['name']=name; rows.append(rec); cov.finish()
        print(name,rec,flush=True)
    # Small deterministic witness for m=3, selected by property.
    if args.tier == 'quick':
        found = False
        for g in plantri_graphs(12,exe):
            for root in range(20):
                b=Instance(g,root); pairs=b.pairs()
                if pairs and min(len(b.dcycles(*p)) for p in pairs)==3:
                    rec=check_instance(b,cov,referee,fp,li=True)
                    rec['name']='property_selected_m3'; rows.append(rec); cov.finish()
                    found=True; break
            if found: break
    from .core import named_graphs
    sample_rows=[]
    for name in ['cube','hexagonal_prism']:
        b=Instance.from_primal(named_graphs()[name]); sample_rows.append(sampler(b,cov)); cov.finish()
    # Exhaustively expose the augmenting-order accident on the prism.
    b=Instance.from_primal(named_graphs()['hexagonal_prism'])
    bases=states=0
    for choices in product(*[[v for v in b.faces[t] if v in b.X] for t in b.A]):
        w=nx.MultiGraph(); w.add_nodes_from(b.white)
        ground={(t,v):(y,z) for t,v,y,z in white_ground(b)}
        w.add_edges_from(ground[t,v] for t,v in zip(b.A,choices))
        if nx.is_tree(w): bases+=1; states+=b.valid(choices)
    require((bases,states)==(6,2),'hexagonal prism relaxation false positives')
    cov.hit('two matroid common bases',bases); cov.finish()
    require(cov.rows['Q reversal objects'][1]>0,'cancellation coverage floor')
    for m in (1,2,3): require(cov.rows[f'property m={m}'][0]>0,f'm={m} coverage floor')
    for check in ['property black inner separator','property white inner separator']:
        require(cov.rows[check][0]>0,check)
    elapsed=time.perf_counter()-started
    print(cov.table(),flush=True)
    print(f'PASS {args.tier}: {len(rows)} rooted runs; {elapsed:.2f} seconds',flush=True)
    if args.output:
        args.output.mkdir(parents=True,exist_ok=True)
        (args.output/f'{args.tier}.json').write_text(json.dumps({'tier':args.tier,'seconds':elapsed,'instances':rows,
            'sampler':sample_rows,'coverage':dict(cov.rows)},indent=2))
        (args.output/f'{args.tier}-coverage.md').write_text(cov.table()+'\n')

if __name__=='__main__': main()

