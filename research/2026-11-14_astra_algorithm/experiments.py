"""Reproduce: python -B research/2026-11-14_astra_algorithm/experiments.py census|families|figures|examples

Each campaign stops after 480 seconds; one worker at a time, <=8 seconds per job.
"""
import sys, json, time, random, subprocess, importlib.util, heapq
from pathlib import Path
from collections import Counter, deque
ROOT = Path(__file__).resolve().parents[2]
BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'workings/barnette_lab'))
import networkx as nx
from barnette_lab.core import Instance, edge, plantri_graphs, glue_triangles
from barnette_lab.optimized import enumerate_tree, verify, solve_piece
from barnette_lab.algorithms import marked_walk, exchange_walk, solve
from barnette_lab.optimized.path import path_tree, BudgetExceeded


def graph_from_faces(fs):
    return nx.Graph((a,b) for f in fs for a,b in zip(f, f[1:]+f[:1]))


def rooted(case):
    g = nx.Graph(case['edges'])
    b = Instance(g)
    return Instance(g, next(i for i,f in enumerate(b.faces) if set(f)==set(case['root'])))


def case(name,g,root=None):
    b=Instance(g)
    return dict(name=name,edges=list(g.edges()),root=list(root or b.faces[0]))


def split(g,rng):
    _,emb=nx.check_planarity(g)
    v=rng.choice(list(g)); ns=list(emb.neighbors_cw_order(v)); d=len(ns)
    offset=rng.randrange(d); ns=ns[offset:]+ns[:offset]
    k=rng.choice(list(range(2,d,2)))
    w,x=max(g)+1,max(g)+2
    h=g.copy(); h.remove_edges_from((v,z) for z in ns[1:k])
    h.add_edges_from((w,z) for z in ns[:k+1])
    h.add_edges_from((x,z) for z in (v,w,ns[0],ns[k]))
    return h


def family_cases():
    spec=importlib.util.spec_from_file_location('families_source',ROOT/'research/2026-11-14_sol_counting-families/code/families.py')
    fam=importlib.util.module_from_spec(spec); spec.loader.exec_module(fam)
    out=[]
    for size in (2,6,12,24):
        for p in (4,6): out.append(case(f'tube{p}-{size}',fam.tube(p,size)))
        b=fam.stack(6,size);out.append(case(f'prism-sum-{size}',b.T,b.R))
    for seed in range(3):
        rng=random.Random(7461+seed);g=nx.octahedral_graph()
        for target in (20,40,80,150):
            while len(g)<target:g=split(g,rng)
            out.append(case(f'split-{seed}-{target}',g))
    for v in (38,40):
        fn=f'cycles_hunt_{v}_'+('400_19' if v==38 else '200_5')+'_0.0.json'
        data=json.loads((ROOT/'research/2026-11-14_fable_referee-topology/data'/fn).read_text())
        ex=data['result']['examples'][0]
        g=nx.Graph((i,j) for i,ns in enumerate(ex['rot']) for j in ns)
        out.append(case(f'evict-{v}',g,ex['outer_face_vertices']))
    line=(ROOT/'research/2026-11-14_fable_descent/data/witnesses.txt').read_text().splitlines()[0]
    adj=line.split('|')[1].strip().split()[1].split(',')
    g=nx.Graph((i,ord(c)-97) for i,ns in enumerate(adj) for c in ns)
    root={0,1,2};base=g.copy()
    for count in range(1,9):
        if count in (1,2,4,8):out.append(case(f'trap-chain-{count}',g,root))
        b=Instance(g);b=Instance(g,next(i for i,f in enumerate(b.faces) if set(f)==root))
        bb=Instance(base);r=next(i for i,f in enumerate(bb.faces) if set(f)==root)
        g=glue_triangles(g,base,b.white[-1],r)
    return out


def baseline(g, forbidden, stats):
    g=g.copy();g.remove_edge(*forbidden)
    start=min(g);path=[start];seen={start}
    def rec(v):
        stats['nodes']+=1
        if len(path)==len(g):return g.has_edge(v,start)
        for w in sorted(g[v],key=lambda x:sum(y not in seen for y in g[x])):
            if w in seen:continue
            seen.add(w);path.append(w)
            if all(sum(y not in seen or y in (start,w) for y in g[x])>=2 for x in g if x not in seen) and rec(w):return True
            path.pop();seen.remove(w)
        return False
    return path if rec(start) else None


def sat(g, forbidden, stats):
    from ortools.sat.python import cp_model
    model=cp_model.CpModel(); arcs=[]; variables={}
    ids={v:i for i,v in enumerate(g)}
    for a,b in g.edges():
        if set((a,b))==set(forbidden):continue
        for u,v in ((a,b),(b,a)):
            z=model.NewBoolVar(f'{u}_{v}');variables[u,v]=z;arcs.append((ids[u],ids[v],z))
    model.AddCircuit(arcs)
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
    solver.parameters.max_time_in_seconds=6
    result=solver.Solve(model)
    stats['nodes']=solver.NumBranches()
    if result not in (cp_model.OPTIMAL,cp_model.FEASIBLE):raise TimeoutError('CP-SAT limit')
    successor={u:v for (u,v),z in variables.items() if solver.Value(z)}
    cycle=[next(iter(g))]
    while successor[cycle[-1]]!=cycle[0]:cycle.append(successor[cycle[-1]])
    return cycle


def search_pair(b,p,method,stats):
    if method=='marked':
        p,st=marked_walk(b,p,cap=2000);stats.update(st);stats['phases']=1+len(st['restarts']);return p
    if method in ('random','greedy'):
        p,moves=exchange_walk(b,p,seed=24,cap=500,greedy=method=='greedy')
        stats['moves']=moves
        if p is None:raise TimeoutError('500 moves')
        return p
    # Complete graph search under a measurement cap; no claim that C3 suffices.
    todo=[(0,0,p)];seen={p};parents={p:None};serial=0
    while todo:
        _,_,p=heapq.heappop(todo);stats['expanded']+=1
        if b.is_tree(p[1]):
            x=p;d=0
            while parents[x] is not None:x=parents[x];d+=1
            stats['moves']=d;return p
        if stats['expanded']>2000:raise TimeoutError('2000 expansions')
        for z in b.neighbors(p):
            if z not in seen:
                seen.add(z);parents[z]=p;serial+=1
                score=len(b.qcycles(z[1])) if method=='best-first' else 0
                heapq.heappush(todo,(score,serial,z))
    raise AssertionError('Component theorem failed')


def run_one(c,method):
    b=rooted(c);e0=edge(*sorted(c['root'])[:2]);forbidden=b.dual_edges[e0]
    st=Counter();start=time.perf_counter()
    if method=='reference':cert=solve(b,e0,st);cycle=cert['cycle']
    elif method in ('optimized','hybrid'):cert=solve_piece(b,e0,st,warm_start=method=='hybrid');cycle=cert['cycle']
    elif method=='path-dp':
        try:s=path_tree(b,st,width_limit=16,state_limit=100000)
        except BudgetExceeded as e:raise TimeoutError(str(e))
        if s is None:return dict(name=c['name'],n=len(b.G),method=method,status='no-good-state')
        cycle=b.recover(s,e0)['cycle']
    elif method in ('baseline','sat'):cycle=(baseline if method=='baseline' else sat)(b.G,forbidden,st)
    else:
        p=b.flow_pair()
        if p is None:return dict(name=c['name'],n=len(b.G),method=method,status='no-pair')
        # Start at a bad pair when cheaply available, to avoid all-zero move plots.
        if len(b.T)<=16:
            p=next((z for z in b.pairs() if not b.is_tree(z[1])),p)
        p=search_pair(b,p,method,st);cycle=b.recover(p[1],e0)['cycle']
    elapsed=time.perf_counter()-start
    if cycle is None or not verify(b.G,cycle,forbidden):raise AssertionError('Certificate rejected')
    return dict(name=c['name'],n=len(b.G),method=method,status='ok',seconds=elapsed,stats=dict(st),cycle=cycle,forbidden=forbidden)


def campaign(kind):
    start=time.monotonic()
    if kind=='hybrid':
        cases=json.loads((BASE/'families-instances.json').read_text());methods=['hybrid','path-dp']
    elif kind=='census':
        cases=[]
        for v in range(6,13):
            for j,g in enumerate(plantri_graphs(v,ROOT/'workings/barnette_lab/vendor/plantri.exe')):
                for i,f in enumerate(Instance(g).faces):cases.append(case(f'census-{v}-{j}-{i}',g,f))
        methods=['optimized','reference','baseline','sat']
    else:
        cases=family_cases();methods=['optimized','reference','baseline','sat','marked','random','greedy','bfs','best-first']
    (BASE/f'{kind}-instances.json').write_text(json.dumps(cases))
    output=BASE/f'{kind}.jsonl'
    with output.open('w') as f:
        for i,c in enumerate(cases):
            for method in methods:
                if time.monotonic()-start>480:return
                if kind=='census':
                    row=run_one(c,method)
                else:
                    try:
                        p=subprocess.run([sys.executable,'-B',__file__,'worker',str(i),method],capture_output=True,text=True,timeout=8)
                        if p.returncode:row=dict(name=c['name'],n=2*len(nx.Graph(c['edges']))-4,method=method,status='error',error=p.stderr[-1500:])
                        else:row=json.loads(p.stdout)
                    except subprocess.TimeoutExpired:row=dict(name=c['name'],n=2*len(nx.Graph(c['edges']))-4,method=method,status='timeout',limit=8)
                f.write(json.dumps(row)+'\n');f.flush()
            if i%10==0:print(kind,i+1,len(cases),round(time.monotonic()-start,2),flush=True)


def figures():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    rows=[json.loads(s) for fn in ('census.jsonl','families.jsonl','hybrid.jsonl') for s in (BASE/fn).read_text().splitlines()]
    for r in rows:
        if r['method']=='hybrid' and r['status']=='ok':r['stats'].setdefault('moves',0)
    out=ROOT/'proofs/algorithm'
    for field,filename in [('seconds','time.png'),('moves','moves.png')]:
        methods=sorted({r['method'] for r in rows if r['status']=='ok' and (field=='seconds' or field in r['stats'])})
        fig,axs=plt.subplots(len(methods),1,figsize=(8,max(4,1.65*len(methods))),sharex=True,squeeze=False)
        for ax,method in zip(axs[:,0],methods):
            data=[r for r in rows if r['method']==method and r['status']=='ok' and (field=='seconds' or field in r['stats'])]
            xs=sorted({r['n'] for r in data});ys=[]
            for n in xs:
                vals=[r['seconds'] if field=='seconds' else r['stats'][field] for r in data if r['n']==n]
                ys.append(max(vals))
            ax.plot(xs,ys,'ko-',ms=3,lw=1);ax.text(.02,.82,method,transform=ax.transAxes,bbox=dict(facecolor='white',edgecolor='none',alpha=.9))
            if field=='seconds':ax.set_yscale('log')
            ax.set_ylabel('seconds' if field=='seconds' else 'exchanges');ax.grid(alpha=.2)
        axs[-1,0].set_xlabel('Primal vertices n');fig.suptitle('Maximum over successful tested instances at each order\nCapped failures excluded; see benchmark table')
        fig.tight_layout(rect=(0,0,1,.96));fig.savefig(out/filename,dpi=160);plt.close(fig)
    summary={}
    for method in sorted({r['method'] for r in rows}):
        rs=[r for r in rows if r['method']==method];ok=[r for r in rs if r['status']=='ok']
        summary[method]=dict(status=dict(Counter(r['status'] for r in rs)),max_seconds=max((r['seconds'] for r in ok),default=0),max_n=max((r['n'] for r in ok),default=0),worst=max(ok,key=lambda r:r['seconds'])['name'] if ok else None)
    (BASE/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))


if __name__=='__main__':
    mode=sys.argv[1]
    if mode in ('census','families','hybrid'):campaign(mode)
    elif mode=='worker':
        c=json.loads((BASE/'families-instances.json').read_text())[int(sys.argv[2])]
        try:row=run_one(c,sys.argv[3])
        except TimeoutError as e:row=dict(name=c['name'],n=2*len(nx.Graph(c['edges']))-4,method=sys.argv[3],status='capped',reason=str(e))
        print(json.dumps(row))
    elif mode=='figures':figures()
