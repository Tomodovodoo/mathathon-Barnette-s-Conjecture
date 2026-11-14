"""Direction 1. Which 4-cut patterns does Theorem 2.2 force, through a cap with a prescribed facial edge?

    python gadgets.py NMAX

A cap is a side G of a 4-cycle cut, read in its canonical frame (signs ++-- or +-+-).
For a face t of G and an edge e of t, look at all Hamiltonian-compatible labellings of G
in which e is the same-label edge of t. If they all have one boundary pattern q, then for
every disk D with the opposite signs such that D + G is simple, Theorem 2.2 applied to
D + G with (t, e) puts the partner pattern of q into F(D).
"""
import sys
from collections import defaultdict
from common import corpus, Tri, UF, labellings_no_mono
from cuts import cycles_of_length, sides, Disk, name4, rotate_name


def forced_patterns(d):
    """(face, edge) -> set of pattern names over prescribed Hamiltonian-compatible labellings."""
    tri, cyc = d.tri, d.cyc
    out = defaultdict(set)
    for lab, c0, c1, rank in labellings_no_mono(tri, d.verts, d.fs, d.edges):
        uf = UF(d.verts)
        for u, v in d.edges:
            if lab[u] == lab[v]:
                uf.union(u, v)
        blocks = defaultdict(list)
        for i, v in enumerate(cyc):
            blocks[uf.find(v)].append(i)
        if c0 + c1 != len(blocks):
            continue
        part = frozenset(frozenset(b) for b in blocks.values())
        nm = name4(tuple(lab[v] for v in cyc), part)
        for f in d.fs:
            a = tri.faces[f]
            for i in range(3):
                x, y, z = a[i], a[(i + 1) % 3], a[(i + 2) % 3]
                if lab[x] == lab[y] != lab[z]:
                    out[f, (x, y)].add(nm)
    return out


def forced_patterns_p4(d):
    """(three consecutive crossed edges of T inside the cap) -> set of pattern names.

    A 3-edge path of the cubic graph is four faces f1..f4 of T glued along three edges;
    a Hamiltonian cycle contains it when the three edges have ends of different labels."""
    tri, cyc = d.tri, d.cyc
    fset = set(d.fs)
    paths = set()
    for f2 in d.fs:
        a = tri.faces[f2]
        es = [frozenset((a[i], a[(i + 1) % 3])) for i in range(3)]
        for e23 in es:
            f3 = next(h for h in (tri.sides[tuple(e23)], tri.sides[tuple(e23)[::-1]]) if h != f2)
            if f3 not in fset:
                continue
            b = tri.faces[f3]
            for e12 in es:
                if e12 == e23:
                    continue
                for j in range(3):
                    e34 = frozenset((b[j], b[(j + 1) % 3]))
                    if e34 == e23:
                        continue
                    paths.add(frozenset((e12, e23, e34)) if False else (min(tuple(sorted(e12)), tuple(sorted(e34))), tuple(sorted(e23)), max(tuple(sorted(e12)), tuple(sorted(e34)))))
    out = defaultdict(set)
    for lab, c0, c1, rank in labellings_no_mono(tri, d.verts, d.fs, d.edges):
        uf = UF(d.verts)
        for u, v in d.edges:
            if lab[u] == lab[v]:
                uf.union(u, v)
        blocks = defaultdict(list)
        for i, v in enumerate(cyc):
            blocks[uf.find(v)].append(i)
        if c0 + c1 != len(blocks):
            continue
        part = frozenset(frozenset(b) for b in blocks.values())
        nm = name4(tuple(lab[v] for v in cyc), part)
        for p in paths:
            if all(lab[x] != lab[y] for x, y in p):
                out[p].add(nm)
    return out


def main_p4(nmax):
    partner = {'X02': 'X13', 'X13': 'X02'}
    found = defaultdict(list)
    for name, g in corpus(6, nmax):
        tri = Tri(g)
        for cyc in cycles_of_length(g, 4):
            a, b = sides(tri, cyc)
            rev = (cyc[0],) + tuple(reversed(cyc[1:]))
            for base in (cyc, rev):
                for rot in range(4):
                    c = base[rot:] + base[:rot]
                    for fs in (a, b):
                        d = Disk(tri, c, fs)
                        if d.signs not in ('++--', '+-+-'):
                            continue
                        shift = 2 if d.signs == '++--' else 1
                        for path, names in forced_patterns_p4(d).items():
                            if len(names) != 1:
                                continue
                            q = rotate_name(next(iter(names)), shift)
                            p = partner.get(q, q)
                            chords = sorted(tuple(sorted(((i + shift) % 4, (j + shift) % 4))) for i, j in d.chords)
                            found[d.signs, p].append((d.interior, len(d.fs), name, c, path, chords))
    for signs in ('++--', '+-+-'):
        print('disks D with signs', signs, '(forcing by a prescribed 3-edge path, Corollary 7.2)')
        for p in ('A0', 'A1', 'A2', 'A3', 'P01', 'P12', 'X02', 'X13'):
            caps = sorted(found.get((signs, p), []), key=lambda r: (r[0], str(r[5])))
            if not caps:
                print('  %s: no forcing cap found' % p)
                continue
            best = next((r for r in caps if not r[5]), caps[0])
            print('  %s: %d forcing (cap, path) pairs; e.g. interior=%d faces=%d %s cycle=%s crossed edges=%s cap chords in D frame=%s'
                  % ((p, len(caps)) + best))


def main(nmax):
    partner = {'X02': 'X13', 'X13': 'X02'}
    found = defaultdict(list)   # (signs of D, pattern forced in D) -> list of caps
    for name, g in corpus(6, nmax):
        tri = Tri(g)
        for cyc in cycles_of_length(g, 4):
            a, b = sides(tri, cyc)
            rev = (cyc[0],) + tuple(reversed(cyc[1:]))
            for base in (cyc, rev):
                for rot in range(4):
                    c = base[rot:] + base[:rot]
                    for fs in (a, b):
                        d = Disk(tri, c, fs)
                        if d.signs not in ('++--', '+-+-'):
                            continue
                        shift = 2 if d.signs == '++--' else 1
                        for (f, e), names in forced_patterns(d).items():
                            if len(names) != 1:
                                continue
                            q = rotate_name(next(iter(names)), shift)   # pattern of the cap in the frame of D
                            p = partner.get(q, q)                         # pattern forced on D
                            chords = sorted(tuple(sorted(((i + shift) % 4, (j + shift) % 4))) for i, j in d.chords)
                            found[d.signs, p].append((d.interior, len(d.fs), name, c, tri.faces[f], e, chords))
    for signs in ('++--', '+-+-'):
        print('disks D with signs', signs)
        for p in ('A0', 'A1', 'A2', 'A3', 'P01', 'P12', 'X02', 'X13'):
            caps = sorted(found.get((signs, p), []), key=lambda r: (r[0], str(r[6])))
            if not caps:
                print('  %s: no forcing cap found' % p)
                continue
            # prefer a cap without chords; else report the chord that D must not have
            best = next((r for r in caps if not r[6]), caps[0])
            print('  %s: %d forcing (cap, face, edge) triples; smallest chordless or first: interior=%d faces=%d %s cycle=%s face=%s edge=%s cap chords in D frame=%s'
                  % ((p, len(caps)) + best))


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[2] == 'p4':
        main_p4(int(sys.argv[1]))
    else:
        main(int(sys.argv[1]))
