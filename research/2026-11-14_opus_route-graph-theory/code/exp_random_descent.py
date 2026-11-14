"""E7: Descent conjecture on random large instances.
For a pair (r,s) and a D-cycle Delta meeting a cycle of the Q-map f, swapping along
Delta should give k(s') < k(s).  We random-walk in the exchange graph (D-swaps and
Q-reversals) to sample many pairs, and test every D-cycle at every visited pair.
Usage: python exp_random_descent.py V trials steps seed"""
import sys, random
from pairs import *

V, trials, steps, seed = map(int, sys.argv[1:5])
rng = random.Random(seed)
tested = viol = incr = 0
hist = {}
for trial in range(trials):
    T = random_eulerian_fast(V, rng)
    faces = T.faces()
    rng.shuffle(faces)
    R = None
    for f in faces:
        Rt = Rooted(T, f)
        if not Rt.black_inner_sep_triangles():
            R = Rt
            break
    if R is None:
        continue
    r, s = flow_pair(R)
    assert is_pair(R, r, s)
    for step in range(steps):
        f = fmap(R, r, s)
        k = len(fcycles(R, f))
        qcs = fcycles(R, f)
        qv = set().union(*map(set, qcs)) if qcs else set()
        for Dc in dcycles(R, r, s):
            if not (set(Dc) & qv):
                continue
            r2, s2 = d_swap(R, r, s, Dc)
            assert is_pair(R, r2, s2)
            k2 = len(fcycles(R, fmap(R, r2, s2)))
            tested += 1
            hist[k2 - k] = hist.get(k2 - k, 0) + 1
            if k2 >= k:
                viol += 1
                if viol <= 3:
                    print("VIOLATION", V, T.rot, R.t0, r, s, Dc, k, k2)
        # random move
        if qcs and rng.random() < 0.5:
            r, s = q_reverse(R, r, s, rng.choice(qcs))
        else:
            r, s = d_swap(R, r, s, rng.choice(dcycles(R, r, s)))
print(f"V={V} trials={trials} tested moves={tested} violations={viol} dk histogram={sorted(hist.items())}")
