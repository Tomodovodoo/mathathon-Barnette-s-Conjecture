"""Replay of the authors' integer certificates (their JSON data, referee arithmetic).
For each certificate: f_r = v T^r w; check the recurrence on D consecutive discrepancies
(D = matrix dimension; Cayley-Hamilton then gives all r), and compare f_r with the
referee's brute-force counts in out_tubes_long.json."""
import json
D0 = '../../2026-11-14_sol_counting-families/data/'
bf = json.load(open('out_tubes_long.json'))
def seq(c, nterms, pair=False):
    D = c['matrix_dimension']
    val = (lambda x: sum(x.values())) if pair else (lambda x: x)      # pair weights at q=1
    rows = [[] for _ in range(D)]
    for s, t, w in c['matrix_entries']: rows[s].append((t, val(w)))
    v = [val(x) for x in c['initial']]; w = [val(x) for x in c['terminal']]
    out = []
    for _ in range(nterms):
        out.append(sum(a * b for a, b in zip(v, w)))
        nv = [0] * D
        for s in range(D):
            if v[s]:
                for t, x in rows[s]: nv[t] += v[s] * x
        v = nv
    return out
def check(c, key, start, pair=False):
    D = c['matrix_dimension']; rec = c['recurrence']; d = len(rec)
    f = seq(c, D + d + 12, pair)
    ok_rec = all(f[r] == sum(a * f[r - j] for j, a in enumerate(rec, 1)) for r in range(d, d + D + 10))
    mine = {int(L): (v[0] if isinstance(v, list) else v) for L, v in bf[key].items()}
    cmp = [(L, f[L - start] == mine[L]) for L in sorted(mine) if 0 <= L - start < len(f)]
    print(f"{key:4s} D={D:2d} recurrence {rec} holds on {D + 10} consecutive terms: {ok_rec}; "
          f"equals referee brute force for L={cmp[0][0]}..{cmp[-1][0]}: {all(x for _, x in cmp)}")
names = {('states', 4): 'S4', ('TM', 4): 'M4', ('states', 6): 'S6', ('TM', 6): 'M6'}
for c in json.load(open(D0 + 'certificates.json')): check(c, names[(c['quantity'], c['width'])], 2)
for c in json.load(open(D0 + 'HC-certificates.json')): check(c, f"H{c['width']}", 0)
for c in json.load(open(D0 + 'pair-certificates.json')): check(c, f"Pm{c['width']}", 2, pair=True)
