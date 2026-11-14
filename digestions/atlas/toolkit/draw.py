"""Write the TikZ sources, captions and gallery from checked objects.

Every panel is a `Panel` over one rooted triangulation in the disk layout.
The methods are layers, drawn in call order. Only objects returned by check.py
are passed in. Encodings live in barnette-figs.sty.
"""
import json
import math

import numpy as np

import check
from model import HERE, und

UNIT = 0.62          # cm per layout unit in the half-width panels of the running example
COLLAR = 0.55        # width of the grey collar that shows the outer black face
RING = 0.28          # the centre of t0 and the edges reaching it live at radius R + RING
LBL = {3: (-0.5, 0.12), 9: (0.42, -0.42), 2: (-0.38, 0.4)}   # label offsets that avoid G and the edges


def pt(p):
    return f'({p[0]:.3f},{p[1]:.3f})'


def ang(p):
    return math.degrees(math.atan2(p[1], p[0]))


class Panel:
    def __init__(self, m, xy, R, unit=UNIT, collar=True, pad=0.25):
        self.m, self.xy, self.R, self.unit = m, xy, R, unit
        self.roots = set(m.roots)
        self.out = []
        self.collar = collar
        self.ext = R + (COLLAR if collar else 0) + pad
        self.cen = {i: self.centre(i) for i in range(len(m.F))}
        self.box = [-self.ext, -self.ext, self.ext, self.ext]

    # geometry ---------------------------------------------------------------
    def arcmid(self, a, b):
        v = self.xy[a] + self.xy[b]
        return self.R * v / np.hypot(*v)

    def centre(self, i):
        m, f = self.m, self.m.F[i]
        if i == m.t0:
            return np.array([0.0, -(self.R + RING)])
        rs = [v for v in f if v in self.roots]
        if len(rs) == 2:                       # a face with an outer arc as a side
            apex = next(v for v in f if v not in rs)
            start = 0.5 * self.xy[apex] + 0.5 * self.arcmid(*rs)
            if i in m.white:
                # Incentre of a circular-sided face: largest inscribed disk.
                from scipy.optimize import minimize
                edges = [(self.xy[a],self.xy[b]) for a,b in zip(f,f[1:]+f[:1]) if not (a in self.roots and b in self.roots)]
                def clearance(z):
                    return np.array([self.R-np.linalg.norm(z[:2])-z[2]] +
                        [check.cross2(b-a,z[:2]-a)/np.linalg.norm(b-a)-z[2] for a,b in edges])
                opt = minimize(lambda z:-z[2], [*start,.1], constraints=[{'type':'ineq','fun':clearance}],method='SLSQP',options={'ftol':1e-12})
                if not (opt.success and min(clearance(opt.x)) > -1e-7):
                    return start          # atlas copy: fall back to the midpoint rule instead of stopping
                return opt.x[:2]
            return start
        # Incentres keep white-face marks away from narrow corners.
        if i in m.white:
            a, b, c = (self.xy[v] for v in f)
            w = np.array([np.linalg.norm(b-c), np.linalg.norm(c-a), np.linalg.norm(a-b)])
            return (w[0]*a + w[1]*b + w[2]*c) / sum(w)
        return sum(self.xy[v] for v in f) / 3

    def outer(self, a, b):
        return a in self.roots and b in self.roots

    def seg(self, a, b):
        """Continuation of a path from a to b along the edge ab of T."""
        if not self.outer(a, b):
            return f' -- {pt(self.xy[b])}'
        t1, t2 = ang(self.xy[a]), ang(self.xy[b])
        d = (t2 - t1 + 180) % 360 - 180
        return f' arc[start angle={t1:.2f},end angle={t1 + d:.2f},radius={self.R}]'

    def edge_path(self, a, b):
        """Path of the edge ab of T: an arc of the outer circle or a segment."""
        return pt(self.xy[a]) + self.seg(a, b)

    def mid(self, a, b):
        return self.arcmid(a, b) if self.outer(a, b) else (self.xy[a] + self.xy[b]) / 2

    def face_path(self, i):
        f = self.m.F[i]
        return pt(self.xy[f[0]]) + ''.join(self.seg(a, b) for a, b in zip(f, f[1:] + f[:1])) + ' -- cycle'

    def smooth_route(self, points, gates, handle=.35):
        """Cubic pieces with explicit midpoint joins and transverse tangents.

        gates maps an interior waypoint to the crossed segment's endpoints.
        Short handles keep each piece inside its incident sector.
        """
        tangents = []
        for k, q in enumerate(points):
            direction = points[min(k+1,len(points)-1)] - points[max(0,k-1)]
            if k in gates:
                a, b = gates[k]
                edge = b-a
                direction = np.array([-edge[1], edge[0]])
                if np.dot(direction, points[k+1]-points[k-1]) < 0:
                    direction = -direction
            direction = direction / np.linalg.norm(direction)
            lens = [np.linalg.norm(q-points[j]) for j in (k-1,k+1) if 0 <= j < len(points)]
            tangents.append(direction * handle * min(lens))
        return [(points[k], points[k]+tangents[k], points[k+1]-tangents[k+1], points[k+1])
                for k in range(len(points)-1)]

    def curve_tex(self, pieces):
        return pt(pieces[0][0]) + ''.join(f' .. controls {pt(b)} and {pt(c)} .. {pt(d)}' for a,b,c,d in pieces)

    def dual_curves(self, g):
        i, j = g
        a, b = self.m.cross[und(i,j)]
        mid = self.mid(a,b)
        if self.m.t0 not in g:
            return self.smooth_route([self.cen[i],mid,self.cen[j]], {1:(self.xy[a],self.xy[b])})
        inner = j if i == self.m.t0 else i
        outer = mid * (self.R+RING)/self.R
        # A straight radial exit, followed by the collar arc.
        return self.smooth_route([self.cen[inner],mid,outer], {1:(mid+np.array([-mid[1],mid[0]]),mid)})

    def dual_path(self, g):
        s = self.curve_tex(self.dual_curves(g))
        if self.m.t0 in g:
            a,b = self.m.cross[und(*g)]
            t = ang(self.mid(a,b)); d = (-90-t+180)%360-180
            if abs(d)>1:
                s += f' arc[start angle={t:.2f},end angle={t+d:.2f},radius={self.R+RING}]'
        return s

    def white_curves(self, rec, t, x):
        ch = rec['chosen'][t]
        sides = [(x,v) for v in self.m.F[t] if v != x]
        sides.sort(key=lambda e: self.m.white_face(*e) != ch['parent'])
        q = .5*(self.cen[t]+self.xy[x])
        # The two adjacent H faces include the black sectors. A short arc
        # needs only the deleted-spoke midpoint, not two forced side bends.
        points = [self.cen[ch['parent']],q,self.cen[ch['child']]]
        return self.smooth_route(points,{1:(self.cen[t],self.xy[x])},handle=.42)

    # layers -------------------------------------------------------------------
    def add(self, s):
        self.out.append(s)
        return self

    def base(self, shade=True, tint=None):
        m, R = self.m, self.R
        if self.collar and shade:
            self.add(rf'\fill[bfblack,even odd rule] (0,0) circle[radius={R + COLLAR}] (0,0) circle[radius={R}];')
        for i in m.black:
            if i != m.t0 and shade:
                self.add(rf'\fill[bfblack] {self.face_path(i)};')
        for i, col in (tint or {}).items():
            self.add(rf'\fill[{col}] {self.face_path(i)};')
        self.add(rf'\draw[bf edge] (0,0) circle[radius={R}];')
        for a, b in m.E:
            if not self.outer(a, b):
                self.add(rf'\draw[bf edge] {self.edge_path(a, b)};')
        return self

    def vertices(self, classes=None, labels=False, skip=(), label_only=None):
        for v in self.m.V:
            p = pt(self.xy[v])
            if v in skip:
                continue
            if classes:
                k = 0 if v in classes[0] else 1
                if k == 0:
                    self.add(rf'\fill {p} circle[radius=2.6pt];')
                else:
                    self.add(rf'\draw[fill=white,line width=.8pt] ($ {p}+(-2.3pt,-2.3pt) $) rectangle ($ {p}+(2.3pt,2.3pt) $);')
            elif v in self.roots:
                self.add(rf'\draw[bf root] {p} circle[radius=2.3pt];')
            else:
                self.add(rf'\fill[bf vertex] {p} circle[radius=1.4pt];')
            if labels and (label_only is None or v in label_only):
                d = self.xy[v] / max(np.hypot(*self.xy[v]), 1e-9)
                off = d * (0.62 if v in self.roots else 0.5)
                if isinstance(labels, dict) and v in labels:
                    off = np.array(labels[v])
                self.add(rf'\node[fill=white,fill opacity=.8,text opacity=1,inner sep=.5pt] at {pt(self.xy[v] + off)} {{${v}$}};')
        return self

    def wedge(self, t, v, style):
        f = self.m.F[t]
        k = f.index(v)
        p, q = self.xy[f[(k + 1) % 3]], self.xy[f[(k + 2) % 3]]
        o = self.xy[v]
        a1 = ang(p - o)
        sweep = (ang(q - o) - a1) % 360
        alt = abs((p - o)[0] * (q - o)[1] - (p - o)[1] * (q - o)[0]) / np.hypot(*(q - p))
        rho = min(0.4 * min(np.hypot(*(p - o)), np.hypot(*(q - o))), 0.7 * alt, 0.85 * math.sqrt(60 / sweep))
        rho = max(rho, 0.42)
        self.add(rf'\begin{{scope}}\clip {self.face_path(t)};\path[{style}] {pt(o)} -- ++({a1:.2f}:{rho:.3f}) arc[start angle={a1:.2f},end angle={a1 + sweep:.2f},radius={rho:.3f}] -- cycle;\end{{scope}}')
        return self

    def state(self, s, style='bf s', only=None):
        for t, v in zip(self.m.A, s):
            if only is None or t in only:
                self.wedge(t, v, style)
        return self

    def arrows(self, arcs, style='bf D'):
        for a, b in arcs:
            self.add(rf'\draw[{style}] {pt(self.xy[a])} -- {pt(self.xy[b])};')
        return self

    def lines(self, edges, style):
        for a, b in edges:
            self.add(rf'\draw[{style}] {self.edge_path(a, b)};')
        return self

    def graphG(self, style='bf G', edges=None, dots=True):
        for g in (edges if edges is not None else self.m.G.edges()):
            self.add(rf'\draw[{style}] {self.dual_path(und(*g))};')
        if dots:
            self.dotsG()
        return self

    def dotsG(self, radius=1.5):
        for i in self.m.G:
            fill = 'black' if i in self.m.black else 'white'
            self.add(rf'\draw[line width=.5pt,fill={fill}] {pt(self.cen[i])} circle[radius={radius}pt];')
        return self

    def spokes(self, deleted=None, style='bf spoke', kept='bf kept', outer=False, centres=True):
        m = self.m
        dele = set(deleted or [])
        for t in m.black:
            if t == m.t0:
                continue
            for v in m.F[t]:
                st = style if deleted is None else ('bf cut' if (t, v) in dele else kept)
                if st is None:
                    continue
                self.add(rf'\draw[{st}] {pt(self.cen[t])} -- {pt(self.xy[v])};')
        if outer and kept:
            rr = self.R + RING
            for v in m.roots:
                t = ang(self.xy[v])
                d = (-90 - t + 180) % 360 - 180
                self.add(rf'\draw[{kept}] {pt(self.xy[v])} -- ({t:.2f}:{rr}) arc[start angle={t:.2f},end angle={t + d:.2f},radius={rr}];')
            self.add(rf'\draw[fill=black] {pt(self.cen[m.t0])} ++(-2pt,-2pt) rectangle ++(4pt,4pt);')
        if centres:
            for t in m.A:
                self.add(rf'\fill {pt(self.cen[t])} ++(-1.7pt,-1.7pt) rectangle ++(3.4pt,3.4pt);')
        return self

    def white_tree(self, rec, s, arrows=False):
        m = self.m
        for t, x in zip(m.A, s):
            self.add(r'\draw[bf wtree] ' + self.curve_tex(self.white_curves(rec,t,x)) + ';')
        for w in m.white:
            self.add(rf'\draw[draw=bfW,fill=white,line width=.8pt] {pt(self.cen[w])} circle[radius=2pt];')
        y = self.cen[rec['y0']]
        self.add(rf'\draw[draw=bfW,line width=.8pt] {pt(y)} circle[radius=3.6pt];')
        return self

    def label(self, p, text, opts=''):
        self.add(rf'\node[{opts}] at {pt(p)} {{{text}}};')
        return self

    def tex(self):
        x0, y0, x1, y1 = self.box
        head = [rf'\begin{{tikzpicture}}[bf,x={self.unit}cm,y={self.unit}cm]',
                rf'\path[use as bounding box] ({x0:.2f},{y0:.2f}) rectangle ({x1:.2f},{y1:.2f});']
        return '\n'.join(head + self.out + [r'\end{tikzpicture}'])


def row(panels, labels, sep='2mm'):
    """Panels side by side with a short label under each."""
    n = len(panels)
    cols = ('@{}' + ('c@{\\hspace{' + sep + '}}') * (n - 1) + 'c@{}')
    body = ' &\n'.join(panels) + r'\\[0.5mm]' + '\n' + ' & '.join(r'\footnotesize ' + s for s in labels)
    return rf'\begin{{tabular}}{{{cols}}}' + '\n' + body + '\n' + r'\end{tabular}'


FIGS = []


def fig(name, body, caption, note):
    FIGS.append((name, body, caption, note))


# ---------------------------------------------------------------------------
def make():
    run, oc, gl = check.running(), check.octahedron(), check.gluing()
    m, xy, R = run['model'], run['xy'], run['R']
    r, s, r2 = run['r'], run['s'], run['r2']
    rec = run['rec']

    def P(**kw):
        return Panel(m, xy, R, **kw)

    # 01 the cube and the octahedron, worked completely -------------------------
    om, oxy, oR = oc['model'], oc['xy'], oc['R']
    orr, os_, orec = oc['r'], oc['s'], oc['rec']
    U = 0.34

    def O():
        return Panel(om, oxy, oR, unit=U)
    # Put the two checked four-cycles on concentric squares.
    import networkx as nx
    cycles = nx.cycle_basis(nx.Graph(oc['two_factor']))
    assert sorted(map(len,cycles)) == [4,4]
    outer = cycles[0]
    inner = [next(v for v in om.G[u] if v not in outer) for u in outer]
    assert all(om.G.has_edge(inner[k],inner[(k+1)%4]) for k in range(4))
    corners = [np.array(q,float) for q in [(-3,-3),(3,-3),(3,3),(-3,3)]]
    square = {v:q for v,q in zip(outer,corners)}
    square.update({v:.46*q for v,q in zip(inner,corners)})
    cp = O()
    for g in om.G.edges():
        cp.add(rf'\draw[bf G] {pt(square[g[0]])} -- {pt(square[g[1]])};')
    for u,v in oc['two_factor']:
        cp.add(rf'\draw[bf cycle] {pt(square[u])} -- {pt(square[v])};')
    for v,q in square.items():
        cp.add(rf'\draw[fill={"black" if v in om.black else "white"},line width=.5pt] {pt(q)} circle[radius=1.5pt];')
    cube2=cp.tex()
    a = O().base().vertices(labels=True).tex()
    b = O().base().state(orr, 'bf r').state(os_).arrows(om.D(orr, os_)).vertices(labels=True).tex()
    c = O().base().state(os_).lines(om.Q(os_), 'bf Q').vertices(labels=True).tex()
    f0 = om.F[om.t0]
    Ss = om.Q(os_) + [(x, y) for x, y in zip(f0, f0[1:] + f0[:1]) if und(x, y) != om.e0]
    d = O().base().lines(Ss, 'bf kept').white_tree(orec, os_).vertices(labels=True).tex()
    e = O().base().lines(orec['P'], 'bf P').graphG('bf cycle', orec['hamiltonian'], dots=False).vertices(classes=orec['parts'], labels=True).tex()
    body = (r'\begin{tabular}{@{}c@{}}' + row([cube2, a, b], ['(a) two cycles, degree two', '(b) its dual, the octahedron $T$', '(c) two states and $D$'], '1mm')
            + r'\\[2mm]' + '\n'
            + row([c, d, e], ['(d) $Q_s$, opposite the wedges', '(e) $S_s$ and the tree of faces', '(f) $P$, two trees, one cycle'], '1mm') + r'\end{tabular}')
    fig('01-cube', body,
        r'The complete construction on the cube. (a) The square-in-square cube has a degree-two subgraph with two cycles. '
        r'(b) Its dual is the octahedron, in the disk embedding used below; shaded faces are black and hollow vertices are roots. '
        r'(c) Outlined choices $r$ and solid choices $s$ are disjoint states; the arrows $r(t)\to s(t)$ form $D$. '
        r'(d) The sides opposite $s$ form the forest $Q_s$. '
        r'(e) The bold edges $S_s$ are $Q_s$ and the two sides of the outer face other than $e_0=\{0,1\}$; they form a spanning tree. The dash-dotted tree joins the white faces across the other edges, rooted at the ring. '
        r'(f) That tree selects one bold side per face. The selected edges $P$ induce two trees, and their complementary dual is one Hamiltonian cycle.',
        'cube and octahedron; all objects from check.octahedron()')

    # 02 degree two is not enough ------------------------------------------------
    a = P().graphG(dots=False).graphG('bf cycle', run['two_factor'], dots=False).dotsG().tex()
    b = P().graphG(dots=False).graphG('bf cycle', rec['hamiltonian'], dots=False).dotsG().tex()
    fig('02-two-factors', row([a, b], ['(a) degree two, two cycles', '(b) degree two, one cycle']),
        r'The running example $G$: cubic, bipartite, planar, 3-connected, with 22 vertices. Filled and hollow dots are the two classes. '
        r'Both bold subgraphs have degree two at every vertex. Only (b) is connected, so only (b) is a Hamiltonian cycle. '
        r'The vertex below the picture is joined to three vertices inside, two of them by the long arcs.',
        'G = dual of running.json; (a) a 2-factor with two components, (b) the cycle recovered in Figure 13')

    # 03 the dual triangulation ----------------------------------------------------
    a = P().base().graphG().vertices(labels=LBL).label((0, -(R + RING) - 0.05), r'$t_0$', 'anchor=west,xshift=3pt').tex()
    fig('03-dual', a,
        r'The dual triangulation $T$ of the running example, with $G$ in grey. Each vertex of $G$ sits in a face of $T$ and each edge of $G$ crosses one edge of $T$. '
        r'Shaded faces are black. The outer face $t_0$ is black as well, which the grey collar shows, and the vertex of $G$ inside it is drawn below. '
        r'The roots $0,4,5$ are hollow. There are $10$ bounded black faces and $10$ other vertices.',
        'running.json with the disk layout; vertex numbers are those of running.json')

    # 04 local pictures (schematic) -----------------------------------------------
    loc = r'''\begin{tikzpicture}[bf,x=1cm,y=1cm]
\coordinate (r) at (0,0); \coordinate (s) at (3.2,0); \coordinate (u) at (1.6,2.6); \coordinate (c) at (1.6,0.87);
\fill[bfblack] (r)--(s)--(u)--cycle; \draw[bf edge] (r)--(s)--(u)--cycle;
\path[bf r] (r) -- ++(0:.62) arc[start angle=0,end angle=58.4,radius=.62] -- cycle;
\path[bf s] (s) -- ++(121.6:.62) arc[start angle=121.6,end angle=180,radius=.62] -- cycle;
\draw[bf D] (r)--(s); \draw[bf Qdir] (r)--(u);
\foreach \p in {r,s,u} \fill (\p) circle[radius=1.4pt];
\node[anchor=north east] at (r) {$r(t)$}; \node[anchor=north west] at (s) {$s(t)$}; \node[anchor=south] at (u) {$u(t)$};
\node at (1.75,1.0) {$t$}; \node[anchor=north,text=bfS] at (1.6,-.08) {$D$}; \node[anchor=east,text=bfR] at (.72,1.4) {$Q_s$};
\end{tikzpicture}'''
    det = r'''\begin{tikzpicture}[bf,x=1cm,y=1cm]
\coordinate (r) at (0,0); \coordinate (s) at (3.2,0); \coordinate (u) at (1.6,2.6); \coordinate (c) at (1.6,0.87);
\fill[bfblack] (r)--(s)--(u)--cycle; \fill[bfS!22] (r)--(c)--(s)--cycle; \draw[bf edge] (r)--(s)--(u)--cycle;
\draw[bf spoke] (c)--(u);
\draw[bf D,dash pattern=on 2pt off 1.6pt] (r)--(s);
\draw[bf detour,shorten <=1.2pt,-{Stealth[length=4.2pt,width=3.6pt]}] (r)--(c); \draw[bf detour,shorten >=1.6pt,-{Stealth[length=4.2pt,width=3.6pt]}] (c)--(s);
\foreach \p in {r,s,u} \fill (\p) circle[radius=1.4pt]; \fill (c) ++(-1.7pt,-1.7pt) rectangle ++(3.4pt,3.4pt);
\node[anchor=north east] at (r) {$r(t)$}; \node[anchor=north west] at (s) {$s(t)$}; \node[anchor=south] at (u) {$u(t)$};
\node[anchor=south west] at (1.62,.95) {$c_t$};
\node[anchor=east] at (.22,.75) {$-a(t,r(t))$}; \node[anchor=west] at (2.98,.75) {$+a(t,s(t))$};
\end{tikzpicture}'''
    fig('04-local', row([loc, det], ['(a) the two edges of a pair in $t$', '(b) the same step along two spokes'], '8mm'),
        r'One bounded black triangle $t$ of a pair $(r,s)$. (a) The outlined wedge marks the corner $r(t)$ and the solid wedge marks $s(t)$. The third corner is $u(t)$. '
        r'The solid arrow $r(t)\to s(t)$ is the edge of $D$ in $t$. The dashed arrow $r(t)\to u(t)$ is the edge of $Q_s$, the side opposite $s(t)$. '
        r'(b) The step $r(t)\to s(t)$ slid onto the two spokes through the centre $c_t$. Its spoke weight is $a(t,s(t))-a(t,r(t))$. The tinted region between the two routes does not contain $u(t)$.',
        'schematic of one triangle, no computed object')

    # 05 states as matchings, and the flow --------------------------------------------
    a = P().base().state(s).vertices().tex()
    pb = P().base()
    X = set(m.X)
    for t in m.A:
        for v in m.F[t]:
            if v in X:
                pb.add(rf'\draw[bf spoke] {pt(pb.cen[t])} -- {pt(xy[v])};')
    for t, v, w in zip(m.A, r, s):
        pb.add(rf'\draw[draw=bfR,line width=1.3pt,double=white,double distance=.7pt] {pt(pb.cen[t])} -- {pt(xy[v])};')
        pb.add(rf'\draw[draw=bfS,line width=1.5pt] {pt(pb.cen[t])} -- {pt(xy[w])};')
    for t in m.A:
        pb.add(rf'\fill {pt(pb.cen[t])} ++(-1.9pt,-1.9pt) rectangle ++(3.8pt,3.8pt);')
    b = pb.vertices().tex()
    fig('05-state', row([a, b], ['(a) a state $s$', '(b) the incidence graph and two disjoint states']),
        r'(a) A state marks one corner of every bounded black triangle so that every vertex other than a root is marked once. No wedge sits at a root. '
        r'(b) The same data as a graph. A square is the centre of a bounded black triangle, and a spoke joins it to each of its corners that is not a root. '
        r'A state is a perfect matching of this graph. The solid spokes are $s$ from (a). The double spokes are a second state $r$ that differs from $s$ at every triangle. Together they have degree two at every square and every dot.',
        's and r = the displayed pair (check.running)')

    # 06 the flow network for Proposition 3.1 -------------------------------------------
    order_x, order_t = [], []
    tf = {(a_, b_): t for t, a_, b_ in zip(m.A, r, s)}
    for k in run['D_cycles']:
        c = k['cycle']
        for a_, b_ in zip(c, c[1:] + c[:1]):
            order_x.append(a_)
            order_t.append(tf[a_, b_])
    n = len(order_x)
    yx = {v: (n - 1 - i) * 0.62 for i, v in enumerate(order_x)}
    yt = {t: (n - 1 - i) * 0.62 - 0.31 for i, t in enumerate(order_t)}
    L = [r'\begin{tikzpicture}[bf,x=1cm,y=1cm]']
    ys, xs0, xx, xa, xt = (n - 1) * 0.31 - 0.15, 0.0, 2.6, 6.0, 8.6
    for v in order_x:
        L.append(rf'\draw[draw=black!55,line width=.9pt] ({xs0},{ys}) -- ({xx},{yx[v]:.2f});')
    for t in order_t:
        L.append(rf'\draw[draw=black!55,line width=.9pt] ({xt},{ys}) -- ({xa},{yt[t]:.2f});')
    for t in m.A:
        for v in m.F[t]:
            if v in X:
                L.append(rf'\draw[bf spoke] ({xx},{yx[v]:.2f}) -- ({xa},{yt[t]:.2f});')
    for t, v, w in zip(m.A, r, s):
        L.append(rf'\draw[draw=bfR,line width=1.3pt,double=white,double distance=.7pt] ({xx},{yx[v]:.2f}) -- ({xa},{yt[t]:.2f});')
        L.append(rf'\draw[draw=bfS,line width=1.5pt] ({xx},{yx[w]:.2f}) -- ({xa},{yt[t]:.2f});')
    for v in order_x:
        L.append(rf'\fill ({xx},{yx[v]:.2f}) circle[radius=1.5pt]; \node[anchor=south,inner sep=2.5pt] at ({xx},{yx[v]:.2f}) {{${v}$}};')
    for t in order_t:
        L.append(rf'\fill ({xa},{yt[t]:.2f}) ++(-2pt,-2pt) rectangle ++(4pt,4pt); \node[anchor=west,inner sep=4pt] at ({xa},{yt[t]:.2f}) {{$\{{{",".join(map(str, sorted(m.F[t])))}\}}$}};')
    L += [rf'\draw[fill=white,line width=.6pt] ({xs0},{ys}) circle[radius=3pt]; \draw[fill=white,line width=.6pt] ({xt},{ys}) circle[radius=3pt];',
          rf'\node[anchor=east,inner sep=5pt] at ({xs0},{ys}) {{source}}; \node[anchor=west,inner sep=5pt] at ({xt},{ys}) {{sink}};',
          rf'\node at ({xx / 2 - .1},{(n - 1) * 0.62 + .55}) {{capacity $2$}}; \node at ({(xx + xa) / 2},{(n - 1) * 0.62 + .55}) {{capacity $1$}}; \node at ({(xa + xt) / 2 + .45},{(n - 1) * 0.62 + .55}) {{capacity $2$}};',
          rf'\node at ({xx},{-0.95}) {{vertices $X$}}; \node at ({xa + .35},{-0.95}) {{black triangles $A$}};',
          r'\end{tikzpicture}']
    fig('06-flow', '\n'.join(L),
        r'Why a pair exists. Send flow from the source through the vertices and the black triangles of Figure 5(b) to the sink. '
        r'A source or sink edge carries at most $2$ and an incidence carries at most $1$. An integral flow of value $2|X|=20$ uses two incidences at every vertex and at every triangle. '
        r'These are the double and the solid edges, and they alternate along cycles, so they split into two disjoint states $r$ and $s$. '
        r'Such a flow exists if every set $S$ of vertices satisfies $\sum_t \min(2,|V(t)\cap S|)\ge 2|S|$. Here equality holds for $S=\{2\}$, a vertex in only two black triangles.',
        'incidence graph of running.json; cut inequality (3.1) checked for all 1024 subsets S')

    # 07 a pair and D --------------------------------------------------------------------
    a = P().base().state(r, 'bf r').state(s).vertices(labels=LBL).tex()
    b = P().base().state(r, 'bf r').state(s).arrows(m.D(r, s)).vertices(labels=LBL).tex()
    fig('07-pair-D', row([a, b], ['(a) the pair $(\\beta,\\alpha)$: outlined $\\beta$, solid $\\alpha$', '(b) $D(\\beta,\\alpha)$']),
        r'(a) Two states $\beta$ (outlined) and $\alpha$ (solid) that choose different corners in every bounded black triangle. '
        r'(b) Join the outlined corner to the solid corner in each triangle. Every vertex other than a root has one arrow in and one arrow out, so the arrows form disjoint directed cycles: '
        r'the counterclockwise $7$-cycle $1,2,3,9,10,11,6$ and the clockwise triangle $8,7,12$.',
        'the displayed pair; D-cycles from check.running')

    # 08 the disk identity ------------------------------------------------------------------
    k = run['disk']
    tint = {i: ('bfS!34' if i in m.black else 'bfS!12') for i in k['faces']}
    pd = P().base(tint=tint)
    pd.state(r, 'bf r', only=set(k['black']))
    cyc = k['cycle']
    arcs = list(zip(cyc, cyc[1:] + cyc[:1]))
    pd.arrows(arcs)
    for a_, b_ in k['inner_black_edges']:
        mid = (xy[a_] + xy[b_]) / 2
        nrm = np.array([-(xy[b_] - xy[a_])[1], (xy[b_] - xy[a_])[0]])
        nrm = nrm / np.hypot(*nrm)
        if np.dot(pd.cen[m.black_face(a_, b_)] - mid, nrm) > 0:
            nrm = -nrm
        pd.label(mid + 0.42 * nrm, r'$\ell$', 'text=bfS,fill=white,inner sep=.8pt')
    pd.vertices(labels=LBL)
    for v in k['interior']:
        pd.add(rf'\draw[line width=.7pt] {pt(xy[v])} circle[radius=3.4pt];')
    side = (r'\begin{tabular}{@{}l@{}}'
            rf'$h={k["h"]}$ arrows on the cycle\\[1mm]'
            rf'$I={k["I"]}$ vertices inside (ringed)\\[1mm]'
            rf'$B={k["B"]}$ black faces inside\\[1mm]'
            rf'$W={k["W"]}$ white faces inside\\[1mm]'
            rf'$\ell={k["l"]}$ arrows with their\\\quad black face inside\\[3mm]'
            rf'$B+W=2I+h-2$\\[1mm] $3(B-W)=2\ell-h$\\[1mm] $B=I+\ell$\\[3mm]'
            r'so $2\ell-h=-3$'
            r'\end{tabular}')
    fig('08-disk', r'\begin{tabular}{@{}c@{\hspace{6mm}}c@{}}' + pd.tex() + ' & ' + r'\raisebox{26mm}{\footnotesize ' + side + r'}\end{tabular}',
        r'The disk identity on the long cycle of $D$ from Figure 7. The tinted disk has $B=5$ black and $W=6$ white faces and $I=3$ vertices strictly inside. '
        r'The first two equations hold for any cycle. The third uses the state $r$: each black face inside holds one outlined wedge, at a ringed vertex ($I$ of them) or at the tail of an arrow whose black face lies inside ($\ell$ of them, marked). '
        r'Hence $2\ell-h=-3$ for every counterclockwise cycle of this kind, whatever its length.',
        'disk of the 7-cycle of D(r,s); counts and the face-by-face matching from check.running')

    # 09 Q cyclic and Q forest -----------------------------------------------------------------
    a = P().base().state(s).lines(m.Q(s), 'bf Q').vertices(labels=LBL).tex()
    b = P().base().state(r).lines(m.Q(r), 'bf Q').vertices(labels=LBL).tex()
    fig('09-Q', row([a, b], ['(a) $Q_\\alpha$ contains a cycle', '(b) $Q_\\beta$ is a forest']),
        r'$Q$ of a state is the dashed edge opposite the solid wedge in each bounded black triangle. '
        rf'(a) For the state $\alpha$ the dashed edges contain a cycle, the triangle $1,8,9$ around a white face (length ${len(run["Q_cycle"])}$). '
        r'(b) For the state $\beta$ they form a forest with three components, one through each root. The proof needs a pair whose second state looks like (b).',
        'Q_s and Q_r for the displayed pair; one root per component asserted')

    # 10 cancellation ---------------------------------------------------------------------------
    ch = set(run['changed'])

    def canc(rr_, qc):
        inside = m.disk(qc)['faces']
        p = P().base(tint={i: 'bfR!22' for i in inside})
        on = {(x, y) for x, y in zip(qc, qc[1:] + qc[:1])}
        qd = m.Q_directed(rr_, s)
        p.lines([e for e in qd if e not in on], 'bf Q')
        p.arrows([e for e in qd if e in on], 'bf Qdir,line width=1.7pt')
        p.state(s).state(rr_, 'bf r')
        return p.vertices(labels=LBL).tex()
    fig('10-cancellation', row([canc(r, run['Q_cycle']), canc(r2, run['Q_cycle_rev'])],
                              [rf'(a) $(\beta,\alpha)$, $\varepsilon={(-1)**((len(m.A)+run["J"])//2):+d}$', rf'(b) $(\tilde\beta,\alpha)$, $\varepsilon={(-1)**((len(m.A)+run["J2"])//2):+d}$']),
        r'The two partners of the state $\alpha$, whose $Q_\alpha$ has a cycle. Dashed edges are $Q_\alpha$. Those on its cycle $1,8,9$, around the tinted face, are heavier and directed from the outlined corner to the third corner. '
        r'Going from (a) to (b), each outlined wedge on the cycle moves to the third corner of its triangle. The cycle reverses and the solid wedges stay. '
        r'Three local signs change, so the sign $\varepsilon$ changes, and the two pairs cancel in any sum weighted by a function of the second state.',
        'reversal of the Q_s cycle (Lemma 5.2); J values and involution asserted')

    # 11 spokes and the two orientations ----------------------------------------------------------
    ps_ = P()
    ps_.add(rf'\fill[bfblack,even odd rule] (0,0) circle[radius={R + COLLAR}] (0,0) circle[radius={R}];')
    polys = []
    for j, kk in enumerate(run['D_cycles']):
        c = kk['ccw_cycle']
        poly = []
        for x, y in zip(c, c[1:] + c[:1]):
            poly += [xy[x], ps_.cen[m.black_face(x, y)]]
        polys.append((kk, c, poly))
        ps_.add(rf'\fill[{"bfS!20" if j == 0 else "bfS!45"}] ' + ' -- '.join(pt(q) for q in poly) + ' -- cycle;')
    for i in m.A:
        ps_.add(rf'\fill[black,fill opacity=.17] {ps_.face_path(i)};')
    ps_.base(shade=False)
    ps_.spokes(centres=False)
    for kk, c, poly in polys:
        for x, y in zip(c, c[1:] + c[:1]):
            ct = ps_.cen[m.black_face(x, y)]
            ps_.add(rf'\draw[bf D,dash pattern=on 2pt off 1.6pt,line width=.8pt] {pt(xy[x])} -- {pt(xy[y])};')
            ps_.add(rf'\draw[bf detour] {pt(xy[x])} -- {pt(ct)};')
            ps_.add(rf'\draw[bf detour,shorten >=1.6pt,-{{Stealth[length=4.2pt,width=3.6pt]}}] {pt(ct)} -- {pt(xy[y])};')
    for t in m.A:
        ps_.add(rf'\fill {pt(ps_.cen[t])} ++(-1.7pt,-1.7pt) rectangle ++(3.4pt,3.4pt);')
    for kk,c,poly in polys:
        w = min(kk['white'],key=lambda w:ps_.cen[w][1])
        ps_.label(ps_.cen[w], rf'$W={kk["W"]}$', 'fill=white,inner sep=1pt')
    ps_.vertices()
    side = (r'\begin{tabular}{@{}l@{}}'
            r'long cycle $C_1$:\\[.5mm]\quad $L^+(C_1)-L^-(C_1)=' + f'{run["D_cycles"][0]["L_diff"]:.0f}' + r'$\\[2mm]'
            r'triangle $C_2$:\\[.5mm]\quad $L^+(C_2)-L^-(C_2)=' + f'{run["D_cycles"][1]["L_diff"]:.0f}' + r'$\\[3mm]'
            r'the four pairs with these\\ undirected cycles contribute\\[1mm]'
            rf'$\sum\varepsilon\,\omega(s)^2=2!\cdot {run["D_cycles"][0]["L_diff"]:.0f}\cdot {run["D_cycles"][1]["L_diff"]:.0f}$'
            r'\end{tabular}')
    fig('11-spokes', r'\begin{tabular}{@{}c@{\hspace{6mm}}c@{}}' + ps_.tex() + ' & ' + r'\raisebox{24mm}{\footnotesize ' + side + r'}\end{tabular}',
        r'Why the sum does not vanish. Both cycles of $D$ are drawn counterclockwise (dashed), and each arrow is replaced by its route along two spokes through the centre of its black triangle (solid). '
        r'The solid route is again a simple closed curve, and its inside is tinted. With spoke weights of circulation $1$ around each face of the spoke graph, its weight is the number of white faces it encloses: ' + f'${run["D_cycles"][0]["W"]}$ for the long cycle and ${run["D_cycles"][1]["W"]}$ for the triangle inside it. '
        r'That number is $L^+(C)-L^-(C)$, the difference between the weights of the two orientations of $C$, so it is positive. The four pairs with these two cycles contribute $2!$ times the product of the two numbers to $\sum\varepsilon\,\omega^2$.',
        'unit spoke circulations solved in check.spoke_weights; L+ - L- = W asserted for both cycles')

    # 12 tree and cotree ----------------------------------------------------------------------------
    dele = list(zip(m.A, r))
    a = P().base().spokes(deleted=dele, outer=True).state(r).vertices().label((0, -(R + RING)), r'$c_0$', 'anchor=north west,xshift=3pt,yshift=-1pt').tex()
    b = P().base().spokes(deleted=dele, kept=None).white_tree(rec, r).vertices().tex()
    fig('12-tree-cotree', row([a, b], ['(a) the spokes that remain form a tree', '(b) the white faces form the dual tree']),
        r'From a forest state to a tree on the white faces. The state is $\beta$ of Figure 9(b), drawn solid. '
        r'(a) All spokes, including the three from the centre $c_0$ of the outer face to the roots. Delete the dotted spoke at each solid wedge. The remaining spokes are $Q$ with a square on each edge, joined through $c_0$, and they form a spanning tree. '
        r'(b) Only the deleted spokes are shown. Each one separates two white faces, and joining them across it gives the green tree on all $11$ white faces. It is rooted at the ringed face $y_0$, the white face on the prescribed edge $e_0=\{0,4\}$.',
        'H - r is a tree, white-face tree is a tree (check.recover)')

    # 13 selected edges and the cycle ------------------------------------------------------------------
    a = P().base().white_tree(rec, r).lines(rec['P'], 'bf P').vertices(labels=LBL).tex()
    b = P().base().lines(rec['P'], 'bf P').graphG('bf cycle', rec['hamiltonian'], dots=False).vertices(classes=rec['parts'], labels=LBL).tex()
    fig('13-selected', row([a, b], ['(a) one bold edge for each white face', '(b) two trees and the curve between them']),
        r'(a) The root $y_0$ selects $e_0$, the bottom arc. Every other white face selects the side it shares with the black triangle on the tree edge towards $y_0$. Every face, black or white, then has one bold side. '
        r'(b) The bold edges $P$ form a forest with two components. The curve crosses the other $22$ edges once each. It is a single closed curve through all $22$ faces, which is the Hamiltonian cycle of Figure 2(b). '
        r'The disks lie inside it and the squares outside, and each class induces a tree.',
        'P, the two induced trees and the Hamiltonian cycle (check.recover asserts each property)')

    # 14 gluing -----------------------------------------------------------------------------------------
    T, gxy = gl['T'], gl['xy']
    U2 = 0.44

    def gp(mm, xx, parts, PP, tintface=None, only=None):
        p = Panel(mm, xx, gl['R'], unit=U2)
        p.base(tint=tintface)
        p.lines(PP, 'bf P')
        cls = [[v for v in parts[0] if v in mm.V], [v for v in parts[1] if v in mm.V]]
        p.vertices(classes=cls, labels=True, label_only=only)
        return p.tex()
    capset = set(gl['cap'])
    cap1 = next(i for i, f in enumerate(gl['m1'].F) if set(f) == capset)
    a = gp(gl['m1'], gl['xy1'], gl['parts1'], gl['P1'], {cap1: 'bfR!25'})
    b = gp(gl['m2'], gl['xy2'], gl['parts'], gl['P2'])
    c = gp(T, gxy, gl['parts'], gl['P'], only=set(gl['m1'].V))
    fig('14-gluing', row([a, b, c], ['(a) outer piece, cap tinted', '(b) inner piece, cap as outer face', '(c) glued'], '1mm'),
        r'A separating triangle, here $\{3,4,5\}$ in a triangulation with $9$ vertices. Cut along it and cap each side with a face. '
        r'(a) Solve the piece that contains $t_0$. On the cap, vertices $3$ and $5$ get the same class. (b) Solve the other piece with the cap as outer face and $\{3,5\}$ as prescribed edge, so the two solutions agree on the triangle. '
        r'(c) The trees of the two pieces meet in the edge $\{3,5\}$ or in the vertex $4$, so their unions are again two induced trees.',
        'two octahedra glued along a face (check.gluing asserts both glued classes induce trees)')

    # 15 overview ---------------------------------------------------------------------------------------------
    flow = r'''\begin{tikzpicture}[bf,x=1cm,y=1cm,every node/.style={font=\footnotesize}]
\tikzset{box/.style={draw,line width=.5pt,text width=6.8cm,align=center,minimum height=8mm,inner sep=3pt},
 aux/.style={draw,line width=.5pt,dash pattern=on 2pt off 1.5pt,text width=3.6cm,align=center,minimum height=8mm,inner sep=3pt},
 to/.style={-{Stealth[length=4.5pt]},line width=.6pt}}
\node[box] (a) at (0,0) {Cubic bipartite planar $G$\\ $\to$ black and white triangulation $T$ (Fig.~3)};
\node[box] (b) at (0,-1.5) {A pair of disjoint states $(r,s)$\\ by an integral flow (Figs.~5--7)};
\node[box] (c) at (0,-3.0) {Some pair has $Q_s$ a forest:\\ cyclic $Q_s$ cancel, the sum is not $0$ (Figs.~9--11)};
\node[box] (d) at (0,-4.5) {Remaining spokes form a tree;\\ dual tree on the white faces (Fig.~12)};
\node[box] (e) at (0,-6.0) {One selected edge per face,\\ and the selected edges form a forest (Fig.~13a)};
\node[box] (f) at (0,-7.5) {Two induced trees in $T$\\ $=$ a Hamiltonian cycle in $G$ (Fig.~13b)};
\node[aux] (k) at (6.6,-3.75) {Disk identity\\ $2\ell-h=-3$ (Fig.~8)};
\node[aux] (g) at (6.6,-7.5) {Separating triangles:\\ cut, solve, glue (Fig.~14)};
\node[aux] (n) at (6.6,-1.5) {needs no separating\\ triangle};
\foreach \u/\v in {a/b,b/c,c/d,d/e,e/f} \draw[to] (\u)--(\v);
\draw[to] (k.west) -- ++(-.5,0) |- (c.east); \draw[to] (k.west) -- ++(-.5,0) |- (e.east);
\draw[to] (g)--(f); \draw[to] (n)--(b);
\end{tikzpicture}'''
    fig('15-overview', flow,
        r'The order of the argument and where each figure belongs. Solid boxes are the main line for a triangulation without separating triangles. '
        r'The disk identity is used twice, for the cancellation and for the forest of selected edges. Separating triangles are handled last, by induction.',
        'logical dependence of Sections 2 to 7 of the OpenAI paper (LIT), no computed object')

    short_caps = {
    '02-two-factors': r'Degree two does not ensure one cycle. The running graph $G$ has $22$ vertices; filled and hollow dots are its bipartition. Both bold subgraphs have degree two everywhere, but only the connected one in (b) is Hamiltonian. The same embedding is used for the final cycle in Figure~13.',
    '03-dual': r'Pass from $G$ to $T=G^*$. Grey edges join face centres across their corresponding edges of $T$. Shaded faces are black, including the outer face $t_0$ shown by the collar. The hollow roots are $0,4,5$; the $10$ bounded black faces match the $10$ nonroot vertices.',
    '04-local': r'Read the two choices inside one black triangle $t$. The outlined corner is $r(t)$, the solid corner is $s(t)$, and the third is $u(t)$. The solid arrow is $D$, while the dashed opposite side is $Q_s$. In (b), replacing the edge by two spokes gives weight $a(t,s(t))-a(t,r(t))$ and excludes $u(t)$ from the tinted subdisk.',
    '05-state': r'A state is a perfect matching between the bounded black triangles $A$ and the nonroot vertices $X$. In (a), each solid choice belongs to its shaded triangle. In (b), the same choices are solid incidence edges; the double edges give the disjoint state $r$. Together $r+s$ has degree two at every square and dot.',
    '06-flow': r'The incidence flow supplies a pair. Source and sink edges have capacity $2$; incidence edges have capacity $1$. The displayed integral flow has value $2|X|=20$. Its used incidences have degree two at every vertex and triangle, so alternating along cycles splits them into states $r,s$. The cut inequality is tight at $S=\{2\}$.',
    '08-disk': r'Count the tinted disk of the long $D$-cycle. It contains $B=5$ black faces, $W=6$ white faces and $I=3$ ringed vertices. Each outlined choice lies at an interior vertex or at the tail of a marked boundary arrow, giving $B=I+\ell$. Combine this with the two face counts to get $2\ell-h=-3$.',
    '09-Q': r'The opposite sides distinguish failure from success. (a) The state $\alpha$ gives a cycle of $Q_\alpha$ around the white triangle $1,8,9$. (b) The state $\beta$ gives a forest with one root per component. Recovery uses the pair $(\alpha,\beta)$.',
    '10-cancellation': r'Keep $\alpha$ fixed and reverse the heavy dashed cycle of $Q_\alpha$. Only the outlined choices move, from $\beta$ to $\tilde\beta$; the solid choices stay. Three local signs flip, so $\varepsilon$ changes sign and the two pairs cancel in any sum weighted by a function of the second state.',
    '11-spokes': r'Slide each dashed cycle of $D$ onto its solid spoke route. Unit circulation around each bounded spoke face makes the counterclockwise weight difference $L^+-L^-$ equal to the white-face count inside the original cycle, labelled $W$. Both counts are positive, and the four pairs of this class contribute $2!\cdot6\cdot1$ to $\sum\varepsilon\,\omega^2$.',
    '12-tree-cotree': r'Recover from the forest state $\beta$ of Figure~9(b), drawn solid. (a) Delete the dotted chosen spokes; the remaining spokes, joined through $c_0$, form a spanning tree. (b) Each deleted spoke is crossed at its midpoint by one edge of the white-face tree. Its root $y_0$ is the ringed face across $e_0=\{0,4\}$.',
    '13-selected': r'The white-face tree selects the bold sides. Its root selects $e_0$; each other white face selects the side towards its parent. Every black and white face has one selected side. The resulting $P$ is a forest with two components. Its complementary dual in (b) is one cycle through all $22$ faces, separating the disk and square classes into two induced trees.',
    '14-gluing': r'Glue across the separating triangle $\{3,4,5\}$. Solve the outer piece first, then prescribe its same-class edge $\{3,5\}$ on the inner piece. The classes agree on the cap. For each class the two trees meet in that edge or in vertex $4$, so their union is again an induced tree.',
    }
    for i,(name,body,cap,note) in enumerate(FIGS):
        FIGS[i]=(name,body,short_caps.get(name,cap),note)

    def mini():
        return Panel(m,xy,R,unit=.205,pad=.05)
    panels=[mini().base().graphG().vertices().tex(),
            mini().base().state(r,'bf r').state(s).arrows(m.D(r,s)).vertices().tex(),
            mini().base().state(s).lines(m.Q(s),'bf Q').vertices().tex(),
            mini().base().state(r).lines(m.Q(r),'bf Q').vertices().tex(),
            mini().base().white_tree(rec,r).lines(rec['P'],'bf P').vertices().tex(),
            mini().base().lines(rec['P'],'bf P').graphG('bf cycle',rec['hamiltonian'],dots=False).vertices(classes=rec['parts']).tex()]
    strip=row(panels,[r'(a) $T=G^*$',r'(b) $(\beta,\alpha)$ and $D$',r'(c) cyclic $Q_\alpha$',r'(d) forest $Q_\beta$',r'(e) tree and $P$',r'(f) one cycle'],'1mm')
    notes=r'''\begin{minipage}{15.7cm}\footnotesize
\medskip
(a) Colour the dual triangles by the bipartition of $G$. Choose the black outer face and its roots.\\[2mm]
(b) An integral incidence flow supplies two states that differ in every triangle. Their arrows form $D$.\\[2mm]
(c) For a fixed second state, reverse a cycle of $Q_\alpha$. Opposite signs cancel all pairs with a cyclic $Q$.\\[2mm]
(d) Regroup by the cycles of $D$. Heights at the white faces make the weighted sum nonzero, so a pair with forest $Q$ survives.
Here the same states in the order $(\alpha,\beta)$ give the forest $Q_\beta$.\\[2mm]
(e) The tree of faces selects one side of every face; the disk identity makes the selected set $P$ acyclic.\\[2mm]
(f) One selected side at each face gives degree two in the complementary dual. Tree duality makes it connected,
so it is a Hamiltonian cycle. The two sides induce trees in $T$.\\[2mm]
Separating triangles are handled by cutting and gluing with a prescribed edge, as in Figure~14.
\end{minipage}'''
    fig('16-at-a-glance',r'\begin{tabular}{@{}c@{}}'+strip+r'\\[3mm]'+notes+r'\end{tabular}',
        r'The proof at a glance on the running example. Read the strip from left to right. Cancellation removes cyclic second states; nonvanishing supplies a forest state. The tree of faces then selects the forest whose complementary dual is the Hamiltonian cycle.',
        'running example; all states, cycles, white-tree and P from check.running; general implications LIT OpenAI Sections 2--7')

    # 17 heights by a path of faces ---------------------------------------------------------------------------
    dist = nx.single_source_shortest_path_length(m.G, m.t0)
    y = next(w for w in m.white if sorted(m.F[w]) == [1, 8, 9])
    path, cur = [y], y
    while cur != m.t0:
        cur = min(w for w in m.G[cur] if dist[w] == dist[cur] - 1)
        path.append(cur)
    turns = {}
    for prev, t, nxt in zip(path, path[1:], path[2:]):
        if t not in m.A:
            continue
        f = m.F[t]
        e_in, e_out = set(m.F[prev]) & set(f), set(f) & set(m.F[nxt])
        (v,) = e_in & e_out
        (a_,) = e_in - {v}
        (b_,) = e_out - {v}
        i = f.index(v)
        turns[t] = (v, 1 if (f[(i + 1) % 3], f[(i + 2) % 3]) == (a_, b_) else -1)
    long_ = run['D_cycles'][0]
    assert long_['h'] == 7 and long_['ccw'] and y in long_['white']
    on = set(zip(long_['cycle'], long_['cycle'][1:] + long_['cycle'][:1]))
    rcw = tuple(b_ if (a_, b_) in on else a_ for a_, b_ in zip(r, s))
    scw = tuple(a_ if (a_, b_) in on else b_ for a_, b_ in zip(r, s))
    assert m.is_pair(rcw, scw)

    def eta(st):
        return sum(sg for t, (v, sg) in turns.items() if st[m.A.index(t)] == v)
    assert (eta(scw), eta(s)) == (-1, 0)
    assert sorted(sorted(m.F[t]) for t in turns) == [[0, 1, 6], [1, 7, 8]]

    def hpanel(st, arcs):
        p = P().base(tint={y: 'bfW!28'})
        p.state(st)
        p.arrows(arcs)
        pts, gates = [p.cen[path[0]]], {}
        for f1, f2 in zip(path, path[1:]):
            a_, b_ = sorted(set(m.F[f1]) & set(m.F[f2]))
            pts.append(p.mid(a_, b_))
            gates[len(pts) - 1] = (xy[a_], xy[b_])
            if f2 != m.t0:
                pts.append(p.cen[f2])
        pts.append(pts[-1] * (R + COLLAR * 0.85) / np.hypot(*pts[-1]))
        p.add(r'\draw[bf wtree,-{Stealth[length=4.5pt,width=4pt]}] ' + p.curve_tex(p.smooth_route(pts, gates)) + ';')
        for t, (v, sg) in turns.items():
            q = xy[v] + 0.5 * (p.cen[t] - xy[v])
            p.label(q, rf'${"+" if sg > 0 else "-"}$', 'fill=white,draw=bfW,circle,inner sep=.3pt,line width=.5pt,minimum size=9pt')
        p.label(p.cen[y] + np.array([0.05, -0.05]), r'$y$', 'fill=white,inner sep=.8pt')
        return p.vertices(labels=LBL).tex()
    arcs_cw = [(b_, a_) for a_, b_ in on]
    arcs_ccw = list(on)
    fig('17-heights', row([hpanel(scw, arcs_cw), hpanel(s, arcs_ccw)],
                          [r'(a) $7$-cycle clockwise: $\eta_s(y)=-1$', r'(b) reversed: $\eta_\alpha(y)=0$']),
        r'A height. The white face $y=\{1,8,9\}$ (tinted) and its path of faces to the outer face (dash-dotted): $y$, $\{1,7,8\}$, $\{1,6,7\}$, $\{0,1,6\}$, $\{0,5,6\}$, $t_0$. '
        r'In each black face on the path, the path turns around one corner; the circled sign is $+$ if that corner lies on the left of the path and $-$ if it lies on the right. '
        r'The height of a state at $y$ adds the signs at turned corners that carry its wedge. '
        r'(a) The pair with the $7$-cycle of $D$ clockwise. Only $\{0,1,6\}$ has its solid wedge at the turned corner $6$, so the height is $-1$. '
        r'(b) After reversing the $7$-cycle the pair is $(\beta,\alpha)$ and the wedge in $\{0,1,6\}$ sits at $1$. The height is $0$, one more, because $y$ lies inside the cycle.',
        'face path = shortest path in G, ties by face index; heights asserted (-1, 0); pair with 7-cycle clockwise obtained from (beta, alpha)')

    return run, oc, gl


def write():
    make()
    for name, body, cap, note in FIGS:
        (HERE / f'{name}-body.tex').write_text(body + '\n', encoding='utf-8')
        (HERE / f'{name}.tex').write_text(
            '\\documentclass[10pt,border=6pt]{standalone}\n\\usepackage{amsmath}\n\\usepackage{barnette-figs}\n\\begin{document}%\n'
            + body + '%\n\\end{document}\n', encoding='utf-8')
    g = [r'\documentclass[10pt,a4paper]{amsart}', r'\usepackage[margin=1in]{geometry}', r'\usepackage{barnette-figs}', r'\usepackage{capt-of}',
         r'\title{Figures for the Barnette exposition}', r'\begin{document}', r'\maketitle',
         r'\noindent This gallery sets every figure at its final size in the text block of the paper '
         r'(\texttt{amsart}, A4, 1in margins). Captions are the proposed captions. '
         r'The filler text between figures is there to judge scale against body type.\par\medskip']
    filler = (r'\noindent\textit{Body text for scale.} A state assigns to each bounded black triangle one of its corners '
              r'so that every vertex other than a root is used once. A pair is two states that differ at every triangle.\par')
    for i, (name, body, cap, note) in enumerate(FIGS, 1):
        g += [r'\par\medskip\noindent\begin{minipage}{\textwidth}\centering', rf'\input{{{name}-body.tex}}', rf'\captionof{{figure}}{{{cap}}}', rf'\label{{fig:{name[3:]}}}', r'\end{minipage}\par\medskip', filler]
        if i == 1 or i % 2 == 1 or i == len(FIGS):
            g.append(r'\clearpage')
    g.append(r'\end{document}')
    (HERE / 'gallery.tex').write_text('\n'.join(g) + '\n', encoding='utf-8')
    (HERE / 'captions.json').write_text(json.dumps({n: dict(caption=c, drawn_from=note) for n, _, c, note in FIGS}, indent=1), encoding='utf-8')
    print('wrote', len(FIGS), 'figures')


if __name__ == '__main__':
    write()
