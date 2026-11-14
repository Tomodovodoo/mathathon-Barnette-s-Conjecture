"""Exact rational half-ray implementation of Li Definitions 13--23, c_min=1.
Appendix B multi-mark extension is intentionally not claimed here.
"""
import sympy as sp
from .core import Instance


class LiObjects:
    def __init__(self, b):
        self.b = b
        roots = list(b.faces[b.outer])
        fixed = dict(zip(roots, [(0, 0), (100, 0), (0, 100)]))
        xs = b.X
        lap = sp.Matrix([[b.T.degree(v) if u == v else -int(b.T.has_edge(u, v)) for u in xs] for v in xs])
        rhs = sp.Matrix([[sum(fixed[w][k] for w in b.T[v] if w in fixed) for k in (0, 1)] for v in xs])
        sol = lap.inv() * rhs
        pos = {v: tuple(map(sp.Rational, xy)) for v, xy in fixed.items()}
        pos.update({v: tuple(sol[i, k] for k in (0, 1)) for i, v in enumerate(xs)})
        centers = {t: tuple(sum(pos[v][k] for v in b.faces[t]) / 3 for k in (0, 1)) for t in range(len(b.faces)) if t != b.outer}
        for shear in range(1, 10000):
            def transform(p):
                return p[0] + shear * p[1], p[1]
            pp = {v: transform(p) for v, p in pos.items()}
            cc = {t: transform(p) for t, p in centers.items()}
            if all(cc[y][0] != p[0] for y in b.white for p in list(pp.values()) + [cc[t] for t in b.A]):
                self.pos, self.centers = pp, cc
                break
        else:
            raise ValueError('Could not put rays in general position')

    def hits(self, pair, cycle, white):
        b = self.b
        wx, wy = self.centers[white]
        hits = []
        for t in cycle:
            i = b.A.index(t)
            for kind, state in enumerate(pair):
                ax, ay = self.centers[t]
                bx, by = self.pos[state[i]]
                if min(ax, bx) < wx < max(ax, bx):
                    y = ay + (by - ay) * (wx - ax) / (bx - ax)
                    if y > wy:
                        hits.append((y, t, kind))
        return sorted(hits)

    def objects(self, pairs):
        for p in pairs:
            for y in self.b.white:
                for c in self.b.dcycles(*p):
                    for _, t, kind in self.hits(p, c, y):
                        if kind == 1:
                            yield p, (y, t)

    def sign(self, obj):
        p, (y, t) = obj
        i = self.b.A.index(t)
        direction = int(bool(self.pos[p[1][i]][0] < self.centers[t][0]))
        return (self.b.J(*p) // 2 + direction) % 2

    def iota1(self, obj):
        p, mark = obj
        cs = self.b.qcycles(p[1])
        return (self.b.reverse_q(p, cs[0]), mark) if cs else obj

    def iota2(self, obj):
        p, (y, t) = obj
        cs = self.b.dcycles(*p)
        c = next(c for c in cs if t in c)
        unmarked = [z for z in cs if z != c]
        if unmarked:
            return self.b.reverse_d(p, unmarked[0]), (y, t)
        hits = self.hits(p, c, y)
        index = next(i for i, (_, f, kind) in enumerate(hits) if f == t and kind == 1)
        if len(hits) % 2 and index == 0:
            return obj
        partner = (index ^ 1) if len(hits) % 2 == 0 else ((index - 1) ^ 1) + 1
        _, new_t, kind = hits[partner]
        return (self.b.reverse_d(p, c) if kind == 0 else p), (y, new_t)


class LiMultiObjects(LiObjects):
    """Appendix B using unordered sets of distinct intersections as Definition 14.
    A canonical tuple stores each set. No repetitions or ordering multiplicity.
    """
    def objects(self, pairs):
        from itertools import combinations
        m = min(len(self.b.dcycles(*p)) for p in pairs)
        for p in pairs:
            marks = set()
            for y in self.b.white:
                for c in self.b.dcycles(*p):
                    marks.update((y,t) for _,t,k in self.hits(p,c,y) if k==1)
            for tokens in combinations(sorted(marks),m):
                yield p,tokens

    def sign(self,obj):
        p, marks=obj
        return (self.b.J(*p)//2 + sum(int(bool(self.pos[p[1][self.b.A.index(t)]][0] < self.centers[t][0])) for y,t in marks))%2

    def iota2(self,obj):
        p,marks=obj
        cs=self.b.dcycles(*p)
        for c in cs:
            if not any(t in c for y,t in marks):
                return self.b.reverse_d(p,c),marks
        # Minimum cycle count forces exactly one mark per cycle.
        assert len(cs)==len(marks)
        entries=[]
        for c in cs:
            y,t=next(mark for mark in marks if mark[1] in c)
            hits=self.hits(p,c,y)
            index=next(i for i,(_,f,k) in enumerate(hits) if f==t and k==1)
            entries.append((c,y,t,hits,index))
        offending=next((e for e in entries if len(e[3])%2==0),None)
        if offending is None:
            offending=next((e for e in entries if e[4]>0),None)
        if offending is None: return obj
        c,y,t,hits,index=offending
        partner=(index^1) if len(hits)%2==0 else ((index-1)^1)+1
        _,new_t,kind=hits[partner]
        new_marks=tuple(sorted((set(marks)-{(y,t)})|{(y,new_t)}))
        return (self.b.reverse_d(p,c) if kind==0 else p),new_marks
