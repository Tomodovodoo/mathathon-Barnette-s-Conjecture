"""Tube sequences beyond the initial values of the claimed recurrences, by brute force."""
import json, time, sys
from core import *
from t_families_lib import det_states, tube_root

def rec_check(vals, start, coeffs):
    """vals: dict L->value. Returns list of (L, predicted, actual) where both exist."""
    d = len(coeffs); out = []
    for L in sorted(vals):
        if all((L - j) in vals and (L - j) >= start for j in range(1, d + 1)):
            pred = sum(c * vals[L - j] for j, c in enumerate(coeffs, 1))
            out.append((L, pred, vals[L], pred == vals[L]))
    return out

budget = float(sys.argv[1]) if len(sys.argv) > 1 else 60
res = {}
def run(name, p, Ls, fn):
    vals = {}
    for L in Ls:
        t = time.time()
        inst = Inst(tube(p, L), tube_root(p, L))
        vals[L] = fn(inst)
        dt = time.time() - t
        print(name, p, L, vals[L], round(dt, 1)); sys.stdout.flush()
        if dt > budget: break
    res[f'{name}{p}'] = vals
    return vals

S4 = run('S', 4, range(0, 21), det_states)
fib = [0, 1]
for _ in range(60): fib.append(fib[-1] + fib[-2])
print('S4 = Fib(2L+3):', all(S4[L] == fib[2 * L + 3] for L in S4))
print('S4 rec', rec_check(S4, 2, [3, -1]))
S6 = run('S', 6, range(0, 13), det_states)
print('S6 rec', rec_check(S6, 2, [7, -9, 7, -1]))
def count_good(inst): return sum(1 for _ in inst.good_states())
def pairs_m(inst):
    P = 0; m = None
    for d in inst.covers():
        c = len(inst.cover_cycles(d)); P += 1 << c; m = c if m is None else min(m, c)
    return (P, m)
M4 = run('M', 4, range(0, 15), count_good)
PM4 = run('Pm', 4, range(0, 15), pairs_m)
M6 = run('M', 6, range(0, 13), count_good)
print('M6 rec', rec_check(M6, 2, [0, 4, 4, 0, 1, 0, -4, -4]))
PM6 = run('Pm', 6, range(0, 10), pairs_m)
print('P6 rec', rec_check({L: v[0] for L, v in PM6.items()}, 2, [4, -4, 4]))
def ham(inst): return hamilton(inst, per_edge=False)[0]
H4 = run('H', 4, range(0, 11), ham)
print('H4 rec', rec_check(H4, 0, [2, -1, 4]))
H6 = run('H', 6, range(0, 8), ham)
print('H6 rec', rec_check(H6, 0, [2, -1, 40, 8, 64, -16]))
json.dump(res, open('out_tubes_long.json', 'w'), indent=1)
