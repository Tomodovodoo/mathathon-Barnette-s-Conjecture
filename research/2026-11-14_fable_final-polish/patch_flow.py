"""One-off patch applied on 14 November 2026: the flow network of Figure 12.

check.py gets the explicit flow, its assertions and the row order of the figure.
draw.py gets the new drawing of 06-flow. Run once from the repository root.
Kept as the record of what changed; check.py and draw.py are the maintained sources.
"""
from pathlib import Path

# ---------------------------------------------------------------- check.py
F = Path('paper/figures/check.py')
raw = F.read_bytes().decode('utf-8')
crlf = '\r\n' in raw
s = raw.replace('\r\n', '\n')

old = '''    out['B_edges'] = B.number_of_edges()
    return out
'''
new = '''    out['B_edges'] = B.number_of_edges()

    # The flow network of Section 5, and the flow that the displayed pair gives.
    n = len(m.X)
    N = nx.DiGraph()
    for v in m.X:
        N.add_edge('source', ('v', v), capacity=2)
    for t in m.A:
        N.add_edge(('t', t), 'sink', capacity=2)
    for a_, b_ in B.edges():
        tt, vv = (a_, b_) if a_[0] == 't' else (b_, a_)
        N.add_edge(vv, tt, capacity=1)
    used = {(('v', v), ('t', t)) for t, v in zip(m.A, r)} | {(('v', v), ('t', t)) for t, v in zip(m.A, s)}
    flow = {e: (2 if 'source' in e or 'sink' in e else int(e in used)) for e in N.edges()}
    assert all(0 <= flow[e] <= N.edges[e]['capacity'] for e in N.edges())
    for x in N:
        if x not in ('source', 'sink'):
            assert sum(flow[e] for e in N.in_edges(x)) == sum(flow[e] for e in N.out_edges(x)) == 2
    value = sum(flow[e] for e in N.out_edges('source'))
    assert value == 2 * n == 20 == nx.maximum_flow_value(N, 'source', 'sink')
    noflow = sorted((v[1], t[1]) for v, t in N.edges() if v != 'source' and t != 'sink' and flow[v, t] == 0)
    assert len(noflow) == B.number_of_edges() - 2 * n
    # The cut with source side {source} + S for the tight S = {2}: its capacity is the value of the flow.
    S = set(out['tight_cut']['S'])
    side = {'source'} | {('v', v) for v in S}
    cut = sum(N.edges[e]['capacity'] for e in N.edges() if e[0] in side and e[1] not in side)
    assert cut == 2 * (n - len(S)) + sum(len(set(m.F[t]) & S) for t in m.A) == value
    tight_faces = sorted(t for t in m.A if set(m.F[t]) & S)
    assert len(tight_faces) == 2 and all((('v', v), ('t', t)) in used for v in S for t in tight_faces)

    # Rows of the figure. The used incidences form one even cycle of B for each cycle of D.
    # Folding a cycle (down on the even rows, back on the odd ones) puts its vertices and its
    # faces on consecutive rows so that every used incidence joins equal or neighbouring rows.
    tf = {(a_, b_): t for t, a_, b_ in zip(m.A, r, s)}

    def fold(cyc):
        h = len(cyc)
        faces = [tf[a_, b_] for a_, b_ in zip(cyc, cyc[1:] + cyc[:1])]      # faces[i] between cyc[i] and cyc[i+1]
        half = (h + 1) // 2
        xrow = {cyc[i]: (2 * i if i < half else 2 * (h - i) - 1) for i in range(h)}
        trow = {}
        for i, t in enumerate(faces):
            a_, b_ = xrow[cyc[i]], xrow[cyc[(i + 1) % h]]
            trow[t] = (a_ + b_) // 2 if abs(a_ - b_) == 2 else max(a_, b_) if a_ + b_ > 1 else 0
        assert sorted(xrow.values()) == sorted(trow.values()) == list(range(h))
        return xrow, trow

    best = None
    cycles = [k['cycle'] for k in out['D_cycles']]
    variants = []
    for c in cycles:
        variants.append([fold(list(c2[i:] + c2[:i])) for c2 in (c, c[::-1]) for i in range(len(c))])
    import itertools as it2
    for order in it2.permutations(range(len(cycles))):
        for pick in it2.product(*[range(len(variants[j])) for j in order]):
            xrow, trow, base = {}, {}, 0
            for j, p in zip(order, pick):
                xr, tr = variants[j][p]
                xrow.update({v: base + q for v, q in xr.items()})
                trow.update({t: base + q for t, q in tr.items()})
                base += len(xr) + 1                      # one empty row between two cycles
            cost = (sum(abs(xrow[v] - trow[t]) for v, t in noflow), sum((xrow[v] - trow[t]) ** 2 for v, t in noflow), order, pick)
            if best is None or cost < best[0]:
                best = (cost, xrow, trow)
    cost, xrow, trow = best
    span = [abs(xrow[v[1]] - trow[t[1]]) for v, t in used]
    assert max(span) == 1 and span.count(0) == 2 * len(cycles)

    def crosses(e, f):
        return (xrow[e[0]] - xrow[f[0]]) * (trow[e[1]] - trow[f[1]]) < 0
    ue = sorted((v[1], t[1]) for v, t in used)
    crossings = sum(crosses(e, f) for e, f in it.combinations(ue, 2))
    assert crossings == sum(len(c) - 1 for c in cycles) == 8     # the least possible for these cycles on two columns
    out['flow'] = dict(value=value, cut=cut, S=sorted(S), tight_faces=tight_faces, xrow=xrow, trow=trow,
                       noflow=noflow, crossings=crossings, noflow_span=cost[0],
                       first=[(v, t) for t, v in zip(m.A, r)], second=[(v, t) for t, v in zip(m.A, s)])
    return out
'''
assert s.count(old) == 1
s = s.replace(old, new)

old = "    'cut inequality (3.1) for every subset S of X; r + s is a degree-two subgraph of the incidence graph',\n"
new = old + "    'flow network: the pair gives a feasible integral flow of value 2|X| = 20 = max flow = capacity of the cut at S = {2}; in the folded row order every used incidence joins equal or neighbouring rows, with 8 crossings',\n"
assert s.count(old) == 1
s = s.replace(old, new)
F.write_bytes((s.replace('\n', '\r\n') if crlf else s).encode('utf-8'))

# ---------------------------------------------------------------- draw.py
F = Path('paper/figures/draw.py')
s = F.read_text(encoding='utf-8')
i = s.index('    # 06 the flow network for Proposition 3.1')
j = s.index('    # 07 one pair panel')
new = r'''    # 06 the flow network of Section 5 --------------------------------------------------
    # Four columns: source, X, A, sink. Rows, flow and tight set come from check.running()['flow'].
    fl = run['flow']
    xrow, trow = fl['xrow'], fl['trow']
    PITCH, XS, XX, XA, XT = 0.66, 0.0, 2.7, 6.9, 9.6
    rows = max(xrow.values())
    yrow = lambda q: (rows - q) * PITCH
    ymid = rows * PITCH / 2
    fname = lambda t: r'{\cdot}'.join(map(str, sorted(m.F[t])))
    L = [r'\begin{tikzpicture}[bf,x=1cm,y=1cm,',
         r'  xn/.style={circle,draw=black,line width=.5pt,fill=white,minimum size=13.5pt,inner sep=0pt},',
         r'  tn/.style={rectangle,rounded corners=1.2pt,draw=black!62,line width=.4pt,fill=bfblack,minimum height=12.5pt,minimum width=33pt,inner sep=1.5pt},',
         r'  term/.style={circle,draw=black,line width=.6pt,fill=white,minimum size=7pt,inner sep=0pt},',
         r'  cap/.style={draw=black!45,line width=.5pt},',
         r'  noflow/.style={draw=black!28,line width=.35pt},',
         r'  first/.style={draw=bfR,line width=1.3pt,double=white,double distance=.7pt},',
         r'  second/.style={draw=bfS,line width=1.5pt}]']
    L.append(rf'\node[term] (so) at ({XS},{ymid:.3f}) {{}}; \node[term] (si) at ({XT},{ymid:.3f}) {{}};')
    for v, q in xrow.items():
        L.append(rf'\node[xn] (x{v}) at ({XX},{yrow(q):.3f}) {{${v}$}};')
    for t, q in trow.items():
        L.append(rf'\node[tn] (t{t}) at ({XA},{yrow(q):.3f}) {{${fname(t)}$}};')
    for v in fl['S']:                                  # the tight set, ringed
        L.append(rf'\node[circle,draw=black,line width=1.1pt,minimum size=18.5pt,inner sep=0pt] (S{v}) at (x{v}) {{}};')
    for v in xrow:
        L.append(rf'\draw[cap] (so) -- (x{v});')
    for t in trow:
        L.append(rf'\draw[cap] (t{t}) -- (si);')
    for v, t in fl['noflow']:
        L.append(rf'\draw[noflow] (x{v}) -- (t{t});')
    for v, t in fl['first']:
        L.append(rf'\draw[first] (x{v}) -- (t{t});')
    for v, t in fl['second']:
        L.append(rf'\draw[second] (x{v}) -- (t{t});')
    top = yrow(0) + 0.62
    L.append(rf'\node[anchor=base] at ({XS},{top}) {{source}}; \node[anchor=base] at ({XX},{top}) {{vertices $X$}}; '
             rf'\node[anchor=base] at ({XA},{top}) {{black triangles $A$}}; \node[anchor=base] at ({XT},{top}) {{sink}};')
    bot = -0.72
    L.append(rf'\node[anchor=base] at ({(XS+XX)/2},{bot}) {{capacity $2$}}; \node[anchor=base] at ({(XX+XA)/2},{bot}) {{capacity $1$}}; '
             rf'\node[anchor=base] at ({(XA+XT)/2},{bot}) {{capacity $2$}};')
    for v in fl['S']:
        L.append(rf'\node[anchor=east] at ($(S{v}.west)+(-.42,.30)$) {{$S=\{{{v}\}}$}};')
    ky = bot - 0.62
    L.append(rf'\draw[first] (0.15,{ky}) -- ++(.8,0) node[anchor=west,xshift=3pt] {{flow $1$, state $\beta$}};')
    L.append(rf'\draw[second] (3.55,{ky}) -- ++(.8,0) node[anchor=west,xshift=3pt] {{flow $1$, state $\alpha$}};')
    L.append(rf'\draw[noflow] (6.95,{ky}) -- ++(.8,0) node[anchor=west,xshift=3pt] {{no flow}};')
    L.append(r'\end{tikzpicture}')
    fig('06-flow', '\n'.join(L),
        r'The flow network of the running example in four columns. Every edge from the source and every edge to the sink has capacity $2$ and carries $2$; an incidence has capacity $1$. '
        r'The incidences that carry flow are the first state $\beta$ (double) and the second state $\alpha$ (solid); the thin ones carry none. '
        r'The ringed set $S=\{2\}$ is tight.',
        'check.running()["flow"]: explicit flow, max flow, tight cut and the folded row order, all asserted')

'''
s = s[:i] + new + s[j:]
old = "    '06-flow': r'The incidence flow supplies a pair."
k = s.index(old)
k2 = s.index('\n', k)
s = s[:k] + r"""    '06-flow': r'The incidence flow supplies a pair. Capacities are $2$ at the source and the sink and $1$ on an incidence. The displayed integral flow has value $2|X|=20$ and uses two incidences at every vertex and every triangle, one of the state $\beta$ (double) and one of $\alpha$ (solid). The thin incidences carry no flow. The cut inequality is tight at the ringed set $S=\{2\}$.',""" + s[k2:]
F.write_text(s, encoding='utf-8', newline='\n')
print('patched')
