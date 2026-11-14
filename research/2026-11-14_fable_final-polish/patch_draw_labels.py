"""One-off patch applied to paper/figures/draw.py on 14 November 2026.

Adds an obstacle registry to Panel and a computed placement of vertex labels.
Run once from the repository root: python research/2026-11-14_fable_final-polish/patch_draw_labels.py
Kept as the record of what changed; draw.py is the maintained source.
"""
from pathlib import Path

F = Path('paper/figures/draw.py')
s = F.read_text(encoding='utf-8')


def rep(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:70])
    s = s.replace(old, new)


rep('''def pt(p):
    return f'({p[0]:.3f},{p[1]:.3f})'
''', '''PT = 0.03515         # cm per TeX point
LABEL_CLEAR = 1.0    # pt of white wanted between a vertex label and every drawn object
LABEL_MIN = 0.5      # pt; write() fails if any label ends up closer than this
LABEL_LOG = {}       # figure -> placed labels per panel, written to label-placement.json


def pt(p):
    return f'({p[0]:.3f},{p[1]:.3f})'
''')

rep('''        self.box = [-self.ext, -self.ext, self.ext, self.ext]
''', '''        self.box = [-self.ext, -self.ext, self.ext, self.ext]
        self.obs = []        # drawn objects as sample disks (x, y, radius), layout units
        self.placed = []     # vertex labels placed by vertices(): (v, offset, clearance in pt, moved)
        self.shaded = False

    # obstacles: what a vertex label must stay clear of -------------------------
    def u(self, points):
        """TeX points to layout units."""
        return points * PT / self.unit

    def ob_disc(self, p, r_pt):
        self.obs.append((float(p[0]), float(p[1]), self.u(r_pt)))
        return self

    def ob_seg(self, p, q, w_pt):
        p, q = np.asarray(p, float), np.asarray(q, float)
        for t in np.linspace(0, 1, max(2, int(np.hypot(*(q - p)) / 0.04) + 2)):
            self.ob_disc(p + t * (q - p), w_pt / 2)
        return self

    def ob_edge(self, a, b, w_pt):
        """The edge ab of T, drawn with line width w_pt."""
        if not self.outer(a, b):
            return self.ob_seg(self.xy[a], self.xy[b], w_pt)
        t1, t2 = math.radians(ang(self.xy[a])), math.radians(ang(self.xy[b]))
        d = (t2 - t1 + math.pi) % (2 * math.pi) - math.pi
        for t in np.linspace(0, 1, int(abs(d) * self.R / 0.04) + 2):
            self.ob_disc(self.R * np.array([math.cos(t1 + t * d), math.sin(t1 + t * d)]), w_pt / 2)
        return self

    def ob_curve(self, pieces, w_pt):
        for a, b, c, d in pieces:
            for t in np.linspace(0, 1, 30):
                self.ob_disc((1-t)**3*a + 3*(1-t)**2*t*b + 3*(1-t)*t*t*c + t**3*d, w_pt / 2)
        return self

    def grey(self, p):
        """Is the point p on a shaded region (a black face or the collar)?"""
        if not self.shaded:
            return False
        rad = float(np.hypot(*p))
        if rad >= self.R:
            return self.collar and rad <= self.R + COLLAR
        for i in self.m.black:
            if i == self.m.t0:
                continue
            f = self.m.F[i]
            inside = True
            for a, b in zip(f, f[1:] + f[:1]):
                if self.outer(a, b):
                    continue
                e, o = self.xy[b] - self.xy[a], self.xy[a]
                if (e[0] * (p[1] - o[1]) - e[1] * (p[0] - o[0])) * (e[0] * (self.cen[i][1] - o[1]) - e[1] * (self.cen[i][0] - o[0])) <= 0:
                    inside = False
                    break
            if inside:
                return True
        return False

    def label_clear(self, c, hw, hh):
        """Clearance in layout units of the box with centre c and half sizes hw, hh from all obstacles."""
        o = np.array(self.obs)
        dx = np.maximum(np.abs(o[:, 0] - c[0]) - hw, 0)
        dy = np.maximum(np.abs(o[:, 1] - c[1]) - hh, 0)
        return float(np.min(np.hypot(dx, dy) - o[:, 2]))

    def place_label(self, v, default):
        """Offset of the label of vertex v: the default if it is clear, else the best free spot.

        The label box (8pt digits with the halo) should keep LABEL_CLEAR points from every
        registered object, lie on white, and stay as near the vertex as that allows.
        """
        hw, hh = self.u(2.125 * len(str(v)) + 0.9), self.u(2.6 + 0.9)
        want, o = self.u(LABEL_CLEAR), self.xy[v]
        default = np.array(default, float)

        def look(off):
            c = o + off
            g = any(self.grey(c + np.array(q)) for q in [(0, 0), (hw, hh), (-hw, hh), (hw, -hh), (-hw, -hh)])
            return self.label_clear(c, hw, hh), g
        cl, g = look(default)
        off, moved = default, False
        if cl < want or g:
            moved, cands = True, []
            for dcm in np.arange(0.20, 0.56, 0.02):
                for th in np.arange(0, 360, 5):
                    q = dcm / self.unit * np.array([math.cos(math.radians(th)), math.sin(math.radians(th))])
                    c2, g2 = look(q)
                    drift = float(np.hypot(*(q - default))) * self.unit
                    val = min(c2, want) - (self.u(1.5) if g2 else 0) - (self.u(0.6) * dcm / 0.2 if c2 >= want else 0) - self.u(0.05) * drift
                    cands.append((val, c2, tuple(q)))
            val, cl, q = max(cands)
            off = np.array(q)
        c = o + off
        for x in np.linspace(-hw, hw, 5):          # later labels keep clear of this one
            for y in np.linspace(-hh, hh, 4):
                self.ob_disc(c + np.array([x, y]), 0)
        self.placed.append((v, [round(float(z), 3) for z in off], round(cl / self.u(1), 2), moved))
        return off
''')

rep('''        m, R = self.m, self.R
        if self.collar and shade:''', '''        m, R = self.m, self.R
        self.shaded = shade
        for a, b in m.E:
            self.ob_edge(a, b, .4)
        if self.collar and shade:''')

i, j = s.index('    def vertices(self, classes=None, labels=False, skip=(), label_only=None):'), s.index('    def wedge(self, t, v, style):')
s = s[:i] + '''    def vertices(self, classes=None, labels=False, skip=(), label_only=None):
        """Vertex marks and, with labels, their numbers. Call it after every other layer,
        because the labels are placed against the objects registered so far."""
        todo = []
        for v in self.m.V:
            p = pt(self.xy[v])
            if v in skip:
                continue
            if classes:
                k = 0 if v in classes[0] else 1
                if k == 0:
                    self.add(rf'\\fill {p} circle[radius=2.6pt];')
                    self.ob_disc(self.xy[v], 2.6)
                else:
                    self.add(rf'\\draw[fill=white,line width=.8pt] ($ {p}+(-2.3pt,-2.3pt) $) rectangle ($ {p}+(2.3pt,2.3pt) $);')
                    self.ob_disc(self.xy[v], 3.6)
            elif v in self.roots:
                self.add(rf'\\draw[bf root] {p} circle[radius=2.3pt];')
                self.ob_disc(self.xy[v], 2.65)
            else:
                self.add(rf'\\fill[bf vertex] {p} circle[radius=1.4pt];')
                self.ob_disc(self.xy[v], 1.4)
            if labels and (label_only is None or v in label_only):
                todo.append(v)
        for v in todo:
            d = self.xy[v] / max(np.hypot(*self.xy[v]), 1e-9)
            off = d * (0.62 if v in self.roots else 0.5)
            if isinstance(labels, dict) and v in labels:
                off = np.array(labels[v])
            if v in self.roots and self.collar and self.shaded:
                # a root label goes outside the collar, so that its halo does not cut into it
                off = d * (COLLAR + self.u(2.6 + 0.9 + LABEL_CLEAR) / max(abs(d[1]), 0.6))
                self.placed.append((v, [round(float(z), 3) for z in off], None, False))
            else:
                off = self.place_label(v, off)
            self.add(rf'\\node[fill=white,fill opacity=.8,text opacity=1,inner sep=.5pt] at {pt(self.xy[v] + off)} {{${v}$}};')
        return self

''' + s[j:]

rep('''        rho = max(rho, 0.42)
''', '''        rho = max(rho, 0.42)
        for rr in np.arange(rho, 0.02, -0.05):
            for th in np.linspace(a1, a1 + sweep, int(sweep / 360 * 2 * math.pi * rr / 0.04) + 2):
                self.ob_disc(o + rr * np.array([math.cos(math.radians(th)), math.sin(math.radians(th))]), 1.0)
''')

rep('''        for a, b in arcs:
            self.add(rf'\\draw[{style}] {pt(self.xy[a])} -- {pt(self.xy[b])};')
        return self
''', '''        for a, b in arcs:
            self.add(rf'\\draw[{style}] {pt(self.xy[a])} -- {pt(self.xy[b])};')
            self.ob_seg(self.xy[a], self.xy[b], 1.7 if '1.7pt' in style else 1.1)
            e = self.xy[a] - self.xy[b]
            self.ob_disc(self.xy[b] + self.u(4.5) * e / np.hypot(*e), 3.0)      # the arrowhead
        return self
''')

rep('''        for a, b in edges:
            self.add(rf'\\draw[{style}] {self.edge_path(a, b)};')
        return self
''', '''        for a, b in edges:
            self.add(rf'\\draw[{style}] {self.edge_path(a, b)};')
            self.ob_edge(a, b, 1.6 if style in ('bf P', 'bf kept') else 1.1)
        return self
''')

rep('''            self.add(rf'\\draw[{style}] {self.dual_path(und(*g))};')
        if dots:''', '''            self.add(rf'\\draw[{style}] {self.dual_path(und(*g))};')
            self.ob_curve(self.dual_curves(und(*g)), 1.3 if style == 'bf cycle' else .3)
        if dots:''')

rep('''            self.add(rf'\\draw[line width=.5pt,fill={fill}] {pt(self.cen[i])} circle[radius={radius}pt];')
        return self''', '''            self.add(rf'\\draw[line width=.5pt,fill={fill}] {pt(self.cen[i])} circle[radius={radius}pt];')
            self.ob_disc(self.cen[i], radius + .25)
        return self''')

rep('''                self.add(rf'\\draw[{st}] {pt(self.cen[t])} -- {pt(self.xy[v])};')
        if outer and kept:''', '''                self.add(rf'\\draw[{st}] {pt(self.cen[t])} -- {pt(self.xy[v])};')
                self.ob_seg(self.cen[t], self.xy[v], 1.1)
        if outer and kept:''')

rep('''            self.add(r'\\draw[bf wtree] ' + self.curve_tex(self.white_curves(rec,t,x)) + ';')
        for w in m.white:
            self.add(rf'\\draw[draw=bfW,fill=white,line width=.8pt] {pt(self.cen[w])} circle[radius=2pt];')
        y = self.cen[rec['y0']]''', '''            self.add(r'\\draw[bf wtree] ' + self.curve_tex(self.white_curves(rec,t,x)) + ';')
            self.ob_curve(self.white_curves(rec,t,x), 1.1)
        for w in m.white:
            self.add(rf'\\draw[draw=bfW,fill=white,line width=.8pt] {pt(self.cen[w])} circle[radius=2pt];')
            self.ob_disc(self.cen[w], 2.4)
        y = self.cen[rec['y0']]
        self.ob_disc(y, 4.0)''')

rep('''    def label(self, p, text, opts=''):
        self.add(rf'\\node[{opts}] at {pt(p)} {{{text}}};')
        return self''', '''    def label(self, p, text, opts='', clear=4.0):
        """A free label at p. Vertex labels keep `clear` points away from p (None: not registered)."""
        self.add(rf'\\node[{opts}] at {pt(p)} {{{text}}};')
        if clear is not None:
            self.ob_disc(p, clear)
        return self''')

rep('''    def tex(self):
        x0, y0, x1, y1 = self.box''', '''    def tex(self):
        Panel.done.append(self.placed)
        x0, y0, x1, y1 = self.box''')

rep('''def row(panels, labels, sep='2mm'):''', '''Panel.done = []


def row(panels, labels, sep='2mm'):''')

rep('''def fig(name, body, caption, note):
    FIGS.append((name, body, caption, note))''', '''def fig(name, body, caption, note):
    FIGS.append((name, body, caption, note))
    LABEL_LOG[name] = [pl for pl in Panel.done if pl]     # the panels drawn since the previous figure
    Panel.done = []''')

# the figures that draw by hand must register what they draw, and call vertices() last
rep('''    pd.vertices(labels=LBL)
    for v in k['interior']:
        pd.add(rf'\\draw[line width=.7pt] {pt(xy[v])} circle[radius=3.4pt];')''', '''    for v in k['interior']:
        pd.add(rf'\\draw[line width=.7pt] {pt(xy[v])} circle[radius=3.4pt];')
        pd.ob_disc(xy[v], 3.75)
    pd.vertices(labels=LBL)''')

rep('''        p.add(r'\\draw[bf wtree,-{Stealth[length=4.5pt,width=4pt]}] ' + ' -- '.join(pt(q) for q in pts) + ';')''', '''        p.add(r'\\draw[bf wtree,-{Stealth[length=4.5pt,width=4pt]}] ' + ' -- '.join(pt(q) for q in pts) + ';')
        for q1, q2 in zip(pts, pts[1:]):
            p.ob_seg(q1, q2, 1.1)''')
rep('''minimum size=9pt')''', '''minimum size=9pt', clear=5.2)''')

rep('''    (HERE / 'captions.json').write_text(''', '''    low = [(n, pl) for n, panels in LABEL_LOG.items() for panel in panels for pl in panel if pl[2] is not None and pl[2] < LABEL_MIN]
    (HERE / 'label-placement.json').write_text(json.dumps(dict(
        note='vertex labels per figure and panel: [vertex, offset in layout units, clearance in pt from every registered object (null: root label outside the collar), moved from its default]',
        want_pt=LABEL_CLEAR, min_pt=LABEL_MIN, figures=LABEL_LOG), indent=1), encoding='utf-8')
    assert not low, f'vertex labels closer than {LABEL_MIN}pt to a drawn object: {low}'
    (HERE / 'captions.json').write_text(''')

F.write_text(s, encoding='utf-8', newline='\n')
print('patched')
