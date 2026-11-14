"""Side claims of the note, checked on all rooted instances up to MAXV vertices (default 12).

1. H(s) (signed ray crossings, left-to-right positive) changes by -a(C) when a cycle C of D_p
   turns from clockwise to counterclockwise, +a(C) the other way. So H plays the role of
   -omega of paper/main (whose omega rises by L(C)), which explains the factor (-1)^m in Section 7.
2. The ordered-list convention with repeated tokens allowed: the signed count over lists is
   m! times the signed count over sets (the note's claim "fixed objects are m! labelled versions").
   Checked as a signed count only.
3. With k = m+1 marks the signed count is not a certificate in general: record zeros and sign
   disagreements with (-1)^floor(m/2) (informational; the note does not claim anything here).

Usage: python research/2026-11-14_opus_referee-involutions/code/extras.py 12
"""
import json
import sys
from collections import Counter
from itertools import product, combinations
from math import factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from ref import Inst, Maps, faces_from_rotation, plantri  # noqa: E402

maxv = int(sys.argv[1]) if len(sys.argv) > 1 else 12
res = Counter()
kplus = Counter()
for nv in range(6, maxv + 1):
    for cls, rot in enumerate(plantri(nv)):
        faces = faces_from_rotation(rot)
        for t0 in range(len(faces)):
            I = Inst(faces, t0)
            P = I.pairs()
            if not P:
                continue
            mp = Maps(I, P)
            m = mp.m
            Hs = {}
            for p in P:
                Hs[p] = sum(1 - 2 * I.dir(p, w, i) for (w, i) in mp.toks(p))
            for p in P:
                for c in I.dcycles(p):
                    q = I.reverse(p, c)
                    poly = [I.pos[p[0][i]] for i in c]
                    area = sum(poly[k][0] * poly[(k + 1) % len(poly)][1] - poly[k][1] * poly[(k + 1) % len(poly)][0] for k in range(len(poly)))
                    cw = area < 0
                    a = sum(1 for w in I.white if I.inside_poly(poly, I.cen[w]))
                    dH = Hs[q] - Hs[p]
                    res['reversals'] += 1
                    res['dH=-a when cw->ccw' if (cw and dH == -a) or ((not cw) and dH == a) else 'other'] += 1
            # list convention (repetition allowed), signed count
            if len(mp.toks(P[0])) ** m < 20000 and m <= 3:
                tot = 0
                for p in P:
                    J2 = I.J(p) // 2
                    for L in product(mp.toks(p), repeat=m):
                        tot += (-1) ** (J2 + sum(I.dir(p, w, i) for (w, i) in L))
                sets = sum(I.sign(*o) for o in mp.objects())
                res['list=m!*set' if tot == factorial(m) * sets else 'list mismatch'] += 1
            # k = m + 1
            sk = sum(I.sign(*o) for o in mp.objects(m + 1))
            target = (-1) ** (m // 2)
            kplus['zero' if sk == 0 else ('same sign as k=m' if (sk > 0) == (target > 0) else 'opposite sign')] += 1
out = dict(command=f'python research/2026-11-14_opus_referee-involutions/code/extras.py {maxv}', H_increment=dict(res), k_m_plus_1=dict(kplus))
(HERE / 'out' / f'extras-{maxv}.json').write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
