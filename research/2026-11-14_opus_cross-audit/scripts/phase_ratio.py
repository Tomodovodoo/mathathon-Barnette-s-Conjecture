"""Check the ratio between the primal note's real sign and Lean's phase.

For every Eulerian triangulation read from plantri ascii output (or a
running.json file), every choice of black root triangle and every pair
(r, s) of states, compute

  delta(t)  = +1 if s(t) follows r(t) in the stored cyclic order of t, else -1
  eps       = prod delta(t)                       (note, Section 6)
  tsum      = sum delta(t)                        (Lean rawIndexSum, aligned)
  phase     = i^(tsum ediv 3)                     (Lean PairPhases.phase)
  circuits of D(r,s): permutation f -> s(r^-1(f)) on X
  c_plus    = circuits with delta-sum -3 (the note's "positive" orientation)
  c_minus   = circuits with delta-sum +3

and assert: every circuit sum is +-3; 3 | tsum; eps = i^(n - tsum);
eps / phase = i^n (aligned indexing) and = i^(-n) (reversed indexing);
the referee's closed forms eps = (-1)^((n+3c)/2) (-1)^c_minus and
phase = i^(c_minus - c_plus) agree; the referee's ratio
(-1)^((n+3c)/2) i^c equals i^n.  It also records which circuit counts c
occur, so that a c-dependent ratio would have been visible.  Finally the
two weight polynomials, with the same random integer weights, are compared
coefficientwise: Z_note == i^n * Z_lean.

Usage: python -I phase_ratio.py FILE [FILE ...] > out.json
FILE is plantri -a output (lines "N adj,adj,...") or a running.json.
"""
import json
import random
import sys

I_POW = [1, 1j, -1, -1j]


def ipow(k):
    return I_POW[k % 4]


def read_plantri(path):
    out = []
    with open(path) as fh:
        for line in fh:
            parts = line.split()
            if len(parts) != 2 or not parts[0].isdigit():
                continue
            rows = parts[1].split(",")
            rot = [[ord(ch) - ord("a") for ch in row] for row in rows]
            out.append(faces_from_rotation(rot))
    return out


def faces_from_rotation(rot):
    seen = set()
    faces = []
    for u in range(len(rot)):
        for v in rot[u]:
            if (u, v) in seen:
                continue
            face = []
            a, b = u, v
            while (a, b) not in seen:
                seen.add((a, b))
                face.append(a)
                nb = rot[b]
                c = nb[(nb.index(a) - 1) % len(nb)]
                a, b = b, c
            faces.append(face)
    assert all(len(f) == 3 for f in faces), "not a triangulation"
    return faces


def two_colour(faces):
    edge_faces = {}
    for i, f in enumerate(faces):
        for k in range(3):
            e = frozenset((f[k], f[(k + 1) % 3]))
            edge_faces.setdefault(e, []).append(i)
    col = {0: 0}
    stack = [0]
    while stack:
        i = stack.pop()
        f = faces[i]
        for k in range(3):
            for j in edge_faces[frozenset((f[k], f[(k + 1) % 3]))]:
                if j == i:
                    continue
                if j in col:
                    assert col[j] != col[i], "not Eulerian"
                else:
                    col[j] = 1 - col[i]
                    stack.append(j)
    return [col[i] for i in range(len(faces))]


def states(black, X):
    """All bijections black -> X with s(t) a corner of t."""
    out = []
    order = sorted(range(len(black)), key=lambda i: sum(v in X for v in black[i]))
    used = set()
    cur = [None] * len(black)

    def rec(k):
        if k == len(order):
            out.append(tuple(cur))
            return
        i = order[k]
        for v in black[i]:
            if v in X and v not in used:
                used.add(v)
                cur[i] = v
                rec(k + 1)
                used.discard(v)
        cur[i] = None

    rec(0)
    return out


def delta(tri, f, g, reverse=False):
    k = tri.index(f)
    succ = tri[(k + 1) % 3]
    d = 1 if g == succ else -1
    return -d if reverse else d


def poly_mul_linear(p, a):
    q = p + [0]
    for k in range(len(p)):
        q[k + 1] += p[k] * a
    return q


def has_separating_triangle(faces):
    adj = {}
    for f in faces:
        for k in range(3):
            adj.setdefault(f[k], set()).add(f[(k + 1) % 3])
            adj.setdefault(f[(k + 1) % 3], set()).add(f[k])
    facesets = {frozenset(f) for f in faces}
    for u in adj:
        for v in adj[u]:
            for w in adj[u] & adj[v]:
                if frozenset((u, v, w)) not in facesets:
                    return True
    return False


def analyse(faces, rng, label):
    col = two_colour(faces)
    septri = has_separating_triangle(faces)
    # either colour class can be "black"; use the class of face 0 and also the other one
    results = []
    for colour in (0, 1):
        blacks = [faces[i] for i, c in enumerate(col) if c == colour]
        for root in range(len(blacks)):
            t0 = blacks[root]
            A = [t for j, t in enumerate(blacks) if j != root]
            X = set(v for f in faces for v in f) - set(t0)
            n = len(A)
            assert n == len(X)
            S = states(A, X)
            weights = [{v: rng.randint(-3, 3) for v in t} for t in A]
            deg = n
            Znote = [0] * (deg + 1)
            Zlean = [0j] * (deg + 1)
            cset = set()
            npairs = 0
            for s in S:
                L = [1]
                for i, t in enumerate(A):
                    L = poly_mul_linear(L, weights[i][s[i]])
                for r in S:
                    if any(r[i] == s[i] for i in range(n)):
                        continue
                    npairs += 1
                    d = [delta(A[i], r[i], s[i]) for i in range(n)]
                    drev = [delta(A[i], r[i], s[i], reverse=True) for i in range(n)]
                    eps = 1
                    for x in d:
                        eps *= x
                    tsum = sum(d)
                    tsum_rev = sum(drev)
                    assert tsum % 3 == 0, (label, tsum)
                    assert eps == ipow(n - tsum)
                    phase = ipow(tsum // 3)
                    phase_rev = ipow(tsum_rev // 3)
                    assert abs(eps / phase - ipow(n)) < 1e-12
                    assert abs(eps / phase_rev - ipow(-n)) < 1e-12
                    # circuits
                    rinv = {r[i]: i for i in range(n)}
                    seen = set()
                    cp = cm = 0
                    for f0 in X:
                        if f0 in seen:
                            continue
                        f = f0
                        tot = 0
                        while f not in seen:
                            seen.add(f)
                            i = rinv[f]
                            tot += d[i]
                            f = s[i]
                        assert tot in (3, -3), (label, tot)
                        if tot == -3:
                            cp += 1
                        else:
                            cm += 1
                    c = cp + cm
                    assert (n - c) % 2 == 0
                    cset.add(c)
                    ref_eps = (-1) ** ((n + 3 * c) // 2) * (-1) ** cm
                    ref_phase = ipow(cm - cp)
                    assert ref_eps == eps and abs(ref_phase - phase) < 1e-12
                    ref_ratio = (-1) ** ((n + 3 * c) // 2) * ipow(c)
                    assert abs(ref_ratio - ipow(n)) < 1e-12
                    for k in range(deg + 1):
                        Znote[k] += eps * L[k]
                        Zlean[k] += phase * L[k]
            for k in range(deg + 1):
                assert abs(Znote[k] - ipow(n) * Zlean[k]) < 1e-9
            # Lemma 4 of the note: no separating triangle => a pair exists
            assert septri or npairs > 0, (label, "no pair without separating triangle")
            results.append({
                "separating_triangle": septri,
                "graph": label, "colour": colour, "root": root, "n": n,
                "states": len(S), "pairs": npairs,
                "circuit_counts": sorted(cset),
                "Z_note": Znote,
            })
    return results


def main():
    rng = random.Random(20261114)
    all_res = []
    for path in sys.argv[1:]:
        if path.endswith(".json"):
            graphs = [json.load(open(path))["faces"]]
        else:
            graphs = read_plantri(path)
        for gi, faces in enumerate(graphs):
            all_res.extend(analyse(faces, rng, f"{path}#{gi}"))
    summary = {
        "graphs": len({r["graph"] for r in all_res}),
        "rooted_instances": len(all_res),
        "pairs": sum(r["pairs"] for r in all_res),
        "instances_with_two_or_more_circuit_counts":
            sum(1 for r in all_res if len(r["circuit_counts"]) > 1),
        "max_n": max(r["n"] for r in all_res),
        "rooted_instances_without_pairs": sum(1 for r in all_res if r["pairs"] == 0),
        "of_which_with_separating_triangle":
            sum(1 for r in all_res if r["pairs"] == 0 and r["separating_triangle"]),
        "failures": 0,
    }
    json.dump({"summary": summary, "instances": all_res}, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
