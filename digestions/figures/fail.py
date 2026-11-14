"""Regenerate the count and failed-route illustrations: python digestions/figures/fail.py.

Requires the paper's Python dependencies, pdflatex and pdftocairo. Only the
four SVGs are written here; TeX, PDF and conversion files use a temporary directory.
All examples and drawing primitives come from the paper or workings/barnette.
"""
import sys
sys.dont_write_bytecode = True
import itertools as it
import json
import math
import re
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'paper/figures'), str(ROOT / 'workings')]
import networkx as nx
import numpy as np
from model import Model, layout, load, und
from figures import Panel, PREAMBLE, is_good, two_factors, pt
from barnette.examples import eight_vertex_example
from barnette.triangulation import Triangulation

HERE = Path(__file__).parent


def convert(t):
    keys = list(t.faces)
    return Model(list(t.faces.values()), keys.index(t.t0), t.e0)


def cell(p, title, detail):
    return (r'\begin{tabular}{@{}c@{}}\textbf{' + title + r'}\\[1mm]'
            + p.tex() + r'\\[1mm]\parbox{' + str(10*p.unit+.7) + r'cm}{\centering\footnotesize ' + detail + r'}\end{tabular}')


def side_by_side(cells):
    return r'\begin{tabular}{@{}c@{\hspace{4mm}}c@{}}' + ' & '.join(cells) + r'\end{tabular}'


def stack(*rows):
    return r'\begin{tabular}{@{}c@{}}' + r'\\[3mm]'.join(rows) + r'\end{tabular}'


def write(name, body):
    with tempfile.TemporaryDirectory(prefix='barnette-fail-') as d:
        d = Path(d)
        (d / 'figure.tex').write_text(PREAMBLE + body + '\n\\end{document}', encoding='utf8')
        proc = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'figure.tex'], cwd=d, capture_output=True)
        if proc.returncode:
            raise RuntimeError(proc.stdout.decode(errors='replace')[-3500:])
        subprocess.run(['pdftocairo', '-svg', str(d / 'figure.pdf'), str(d / 'figure.svg')], check=True, capture_output=True)
        svg = (d / 'figure.svg').read_text(encoding='utf8')
        view = re.search(r'viewBox="([^"]+)"', svg).group(1)
        x, y, w, h = map(float, view.split())
        svg = re.sub(r'width="[^"]+" height="[^"]+"', f'width="720" height="{720*h/w:.2f}"', svg, count=1)
        end = svg.index('>', svg.index('<svg')) + 1
        svg = svg[:end] + f'\n<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white"/>\n' + svg[end:]
        (HERE / f'fail-{name}.svg').write_text(svg, encoding='utf8')
    print(f'fail-{name}.svg')


def crossing_data(m, p):
    """Straight parallel gamma_y; exact segment intersections determine chi.

    Each starts at the paper Panel's interior point of a white face and ends
    outside the disk. H arcs are the paper's straight p_t-to-corner segments.
    """
    direction = np.array([.371, 1.0])
    direction /= np.linalg.norm(direction)
    gammas, crossings = {}, []
    for y in m.white:
        start = p.cen[y]
        length = -np.dot(start, direction) + math.sqrt(np.dot(start, direction)**2 + 5.13**2 - np.dot(start, start))
        gammas[y] = (start, start + length * direction)
        for t in m.A:
            a = p.cen[t]
            for v in m.F[t]:
                if v not in m.X:
                    continue
                e = p.xy[v] - a
                det = np.linalg.det(np.column_stack((e, -direction)))
                if abs(det) < 1e-9:
                    continue
                u, h = np.linalg.solve(np.column_stack((e, -direction)), start - a)
                if 0 < u < 1 and 0 < h < length:
                    chi = -1 if (e[0]*direction[1]-e[1]*direction[0]) > 0 else 1
                    crossings.append(dict(y=y, t=t, v=v, h=h, chi=chi, q=a+u*e))
    return gammas, crossings


def count_figure():
    m, xy = load('running.json')
    fs = two_factors(m)
    p = Panel(m, xy, .64)
    gammas, crossings = crossing_data(m, p)
    weight = lambda s: sum(c['chi'] for c in crossings if s[m.A.index(c['t'])] == c['v'])
    sign = lambda r, s: math.prod(m.delta(a,b) for a,b in zip(r,s))
    pairs = m.pairs()
    offset = min(weight(s) for r,s in pairs)
    polynomial = Counter()
    for r,s in pairs:
        polynomial[weight(s)-offset] += sign(r,s)
    assert {k:v for k,v in polynomial.items() if v} == {0:1,1:-1,2:1,3:-1,5:-1,7:1}
    assert len(m.states()) == 12 and len(pairs) == 8
    assert sum(is_good(m,s)[0] for s in m.states()) == 6
    assert sum(sign(r,s)*weight(s)**2 for r,s in pairs) == 18
    marked_total = 0
    for r,s in pairs:
        cs = [c for c in crossings if s[m.A.index(c['t'])] == c['v']]
        marked_total += sum(sign(r,s)*a['chi']*b['chi'] for a,b in it.combinations(cs,2))
    assert marked_total == 9
    fixed = []
    cells = []
    for i,F in enumerate(fs):
        disks = F['disks']
        candidates = []
        for r,s in F['pairs']:
            for ys in it.product(*(d['white'] for d in disks)):
                marks = []
                for d,y in zip(disks,ys):
                    vertices = set(d['cycle'])
                    cycle_faces = {t for t,a,b in zip(m.A,r,s) if a in vertices and b in vertices}
                    cs = [c for c in crossings if c['y']==y and c['t'] in cycle_faces and c['v'] in (r[m.A.index(c['t'])],s[m.A.index(c['t'])])]
                    first = min(cs,key=lambda c:c['h'])
                    if s[m.A.index(first['t'])] != first['v']:
                        break
                    marks.append(first)
                if len(marks)==2:
                    assert sign(r,s)*math.prod(c['chi'] for c in marks)==1
                    candidates.append((r,s,marks))
        assert len(candidates) == math.prod(d['W'] for d in disks)
        fixed += candidates
        # Separate the two parallel gamma_y as widely as possible.
        r,s,marks = min(candidates,key=lambda z:(len({c['y'] for c in z[2]})<2, -abs(np.linalg.det(np.array([gammas[z[2][0]['y']][0]-gammas[z[2][1]['y']][0], [.371,1.0]]))),sum(c['h'] for c in z[2])))
        p = Panel(m,xy,.64).base()
        p.graphH(F['arcs']).state(r,'r').state(s,'s')
        for c in marks:
            a,b = gammas[c['y']]
            p.add(rf'\draw[gamma] {pt(a)} -- {pt(b)};')
            p.add(rf'\fill[white] {pt(c["q"])} circle[radius=2.6pt];\fill {pt(c["q"])} circle[radius=1.8pt];')
            p.add(rf'\draw[fill=white,line width=.5pt] {pt(a)} circle[radius=1.4pt];')
        p.vertices()
        values = [d['W'] for d in disks]
        cells.append(cell(p, rf'$F_{i+1}$: $a(C)={values[0]},{values[1]}$', rf'$\iota_2$: ${len(candidates)}$ fixed marked pairs'))
    assert len(fixed)==9
    write('count', stack(
        r'\textbf{One example, three presentations: $n=10$, $m=2$}',
        side_by_side(cells),
        r'$Z(z)=z^{\omega_0}(1-z)\bigl((1-z^6)+z^2(1-z^3)\bigr)$',
        r'$\displaystyle \left.\frac{Z(z)}{(1-z)^2}\right|_{z=1}=9'
        r'\qquad [x^2]Z(e^x)=9\qquad \sum_{(r,s)}\varepsilon(r,s)\omega(s)^2=18$',
        r'\textbf{Marked crossings:} $6\cdot1+3\cdot1=9$ fixed points of sign $+1$.'))
    print('count: polynomial, power sum, signed marked count and nine fixed points verified; omega0=',offset)


def prism_figure(m,xy):
    states = sorted(m.states(),key=lambda s:not is_good(m,s)[0])
    assert len(states)==3 and all(m.Q_is_forest(s) for s in states)
    assert sum(is_good(m,s)[0] for s in states)==2
    cells=[]
    for i,s in enumerate(states):
        p=Panel(m,xy,.43).base().state(s,'s').lines(m.Q(s),'Q',1.1)
        # The two root sides in the definition of good are drawn solid black.
        sides=[e for e in zip(m.roots,m.roots[1:]+m.roots[:1]) if und(*e)!=m.e0]
        p.lines(sides,'bold',1.5).vertices()
        q=m.Q_graph(s)
        multi=[c for c in nx.connected_components(q) if len(set(c)&set(m.roots))>1]
        status='good' if is_good(m,s)[0] else 'not good'
        cells.append(cell(p,rf'$s_{i+1}$: {status}',r'$Q_s$ has no cycle'))
        if multi:
            assert len(multi)==1
            print('prism bad component roots:', sorted(set(multi[0])&set(m.roots)))
    row=r'\begin{tabular}{@{}c@{\hspace{3mm}}c@{\hspace{3mm}}c@{}}'+' & '.join(cells)+r'\end{tabular}'
    write('one-state',stack(r'\textbf{A forest need not give a good state}',row,
        r'Dashed: $Q_s$.\quad Black: the two sides of $t_0$ other than $e_0$.',
        r'For $s_3$, these edges contain a cycle; one component of $Q_{s_3}$ contains two roots.'))


def bad_factor():
    data=json.loads((ROOT/'research/instances/2-factor-without-good-state-16.json').read_text())
    t=Triangulation.from_graph(nx.Graph(data['edges']),data['t0'],data['t0'][:2])
    m=convert(t); xy=layout(m)
    unused={frozenset(f):v for f,v in zip(data['black_faces'],data['unused'])}
    fs=two_factors(m)
    F=next(F for F in fs if all(unused[frozenset(m.F[t])] not in (a,b) for t,a,b in zip(m.A,F['r'],F['s'])))
    assert len(fs)==3 and len(F['pairs'])==2 and len(F['disks'])==1 and F['disks'][0]['h']==13
    assert sum(is_good(m,s)[0] for s in m.states())==12
    cells=[]
    for i,(r,s) in enumerate(F['pairs']):
        assert not is_good(m,s)[0]
        p=Panel(m,xy,.67).base().state(r,'r').state(s,'s').arrows(m.D(r,s)).vertices()
        cycles=nx.cycle_basis(m.Q_graph(s))
        assert len(cycles)==1
        cyc=cycles[0]
        p.lines(list(zip(cyc,cyc[1:]+cyc[:1])),'K',1.5)
        cells.append(cell(p,rf'$(r,s)$' if i==0 else r'$(s,r)$',rf'$Q_s$ contains a cycle of length ${len(cyc)}$' if i==0 else rf'$Q_r$ contains a cycle of length ${len(cyc)}$'))
    write('single-factor',stack(r'\textbf{Both pairs of one $2$-factor fail}',side_by_side(cells),
        r'One cycle of $D(r,s)$, of length $13$; reversing it exchanges the two states.',
        r'Only the cycle of $Q_s$ (left) or $Q_r$ (right) is dashed.'))
    print('16 vertices: three 2-factors, twelve good states; chosen factor has none')


def matroids(m,xy):
    def root_tree(s):
        edges=[tuple(-1 if v in m.roots else v for v in e) for e in m.Q(s)]
        g=nx.MultiGraph();g.add_nodes_from([-1]+m.X);g.add_edges_from(edges)
        return nx.is_tree(g)
    choices=[s for s in it.product(*[[v for v in m.F[t] if v in m.X] for t in m.A]) if root_tree(s)]
    assert len(choices)==6 and sum(m.is_state(s) for s in choices)==2
    bad=next(s for s in choices if not m.is_state(s))
    good=next(s for s in choices if m.is_state(s))
    cells=[]
    for s,title in [(bad,'Two matroids'),(good,'All three matroids')]:
        p=Panel(m,xy,.66).base().state(s,'s').lines(m.Q(s),'Q',1.1).vertices()
        counts=Counter(s)
        for v in m.X:
            if counts[v]!=1:
                p.add(rf'\draw[line width=1pt,{"densely dashed" if counts[v]==0 else "solid"}] {pt(xy[v])} circle[radius=5pt];')
        cells.append(cell(p,title,r'Independent after identifying the roots' if s==bad else 'A good state'))
    write('matroids',stack(r'\textbf{The condition at each vertex is necessary}',side_by_side(cells),
        r'Left: the ringed vertices are chosen twice and not at all.',
        r'Of the $6$ common bases of these two matroids, only $2$ are states.'))


if __name__=='__main__':
    count_figure()
    m=convert(eight_vertex_example()); xy=layout(m)
    prism_figure(m,xy)
    bad_factor()
    matroids(m,xy)
