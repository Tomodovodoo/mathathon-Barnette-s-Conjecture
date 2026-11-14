"""Recompute the two worked examples of proofs/primal/PRIMAL-PROOF.md, Section 11.

The script reads the printed data (edges, flow, facial cycles, potentials,
states, pairs, circuits, polynomial, recovery) from the note itself, rebuilds
the rotation system from the printed facial cycles, recomputes every item
with primal.py and reports each comparison.
"""
import re, sys, json
from pathlib import Path
from primal import PG, Rooted, E, undirected_cycles, is_forest, padd, pmul, pscale, ptrim

ROOT = Path(__file__).resolve().parents[3]
TEXT = (ROOT / "proofs/primal/PRIMAL-PROOF.md").read_text(encoding="utf-8")
ints = lambda s: [int(x) for x in re.findall(r"-?\d+", s)]
REPORT = []


def say(ok, what, detail=""):
    REPORT.append((bool(ok), what, detail))
    print(("ok   " if ok else "FAIL ") + what + (("  " + str(detail)) if detail else ""))


def run(title, body):
    print("\n==", title)
    b0 = int(re.search(r"root is \$b_0=(\d+)\$", body).group(1))
    e0 = E(*ints(re.search(r"prescribed\}=\((\d+), (\d+)\)", body).group(0))[-2:])
    edges = {int(k): E(int(u), int(v)) for k, u, v in re.findall(r"^\$e_\{(\d+)\}=\((\d+), (\d+)\)\$", body, re.M)}
    alpha_note = {edges[int(k)]: int(a) for k, a in re.findall(r"\\alpha\(e_\{(\d+)\}\)=(-?\d+)", body)}
    faces = {int(k): ints(c) for k, c in re.findall(r"^\$f_\{(\d+)\}=\(([\d,]+)\)\$", body, re.M)}
    # rotation system from the printed facial cycles
    succ = {}
    for w in faces.values():
        for i in range(len(w)):
            u, v, x = w[i - 1], w[i], w[(i + 1) % len(w)]
            succ.setdefault(v, {})[u] = x
    rot = {}
    consistent = True
    for v, m in succ.items():
        u = min(m)
        cyc = [u, m[u], m[m[u]]]
        consistent &= len(m) == 3 and m[cyc[2]] == u and len(set(cyc)) == 3
        rot[v] = cyc
    say(consistent, "printed facial cycles are coherently oriented and give a rotation system")
    G = PG(rot)
    say(G.genus0() and set(G.edges) == set(edges.values()), "rotation system has genus 0 and the printed edge set",
        f"|V|={len(G.V)} |E|={len(G.edges)} |F|={G.nF}")
    canon = lambda w: frozenset(w)
    mine = {canon(w): i for i, w in enumerate(G.faces)}
    fmap = {mine[canon(w)]: k for k, w in faces.items()}      # my face id -> printed face id
    say(len(fmap) == G.nF, "traced faces are exactly the printed facial cycles")
    inv_f = {k: i for i, k in fmap.items()}

    pots = {int(b): (ints(f), ints(p)) for b, f, p in
            re.findall(r"^\$b=(\d+)\$ has incident faces \$\(([\d,]+)\)\$ and potentials \$\(([-\d,]+)\)\$", body, re.M)}
    orient = None
    for o in (1, -1):
        Rt = Rooted(G, b0, orient=o, alpha=alpha_note)
        ok = True
        for b, (fs, ps) in pots.items():
            base = Rt.pot[b][inv_f[fs[0]]]
            ok &= all(Rt.pot[b][inv_f[f]] - base == p for f, p in zip(fs, ps))
        if ok:
            orient = o
    say(orient is not None, "printed potentials satisfy (5.2) with the printed flow", f"orientation convention {orient}")
    Rt = Rooted(G, b0, orient=orient or 1, alpha=alpha_note)
    for b, (fs, ps) in pots.items():        # use the printed normalisation
        Rt.pot[b] = {inv_f[f]: p for f, p in zip(fs, ps)}
    sets = dict(re.findall(r"\$([BWARX])=\\\{([\d,]+)\\\}\$", body))
    say(set(ints(sets["B"])) == Rt.black and set(ints(sets["W"])) == Rt.white and ints(sets["A"]) == sorted(Rt.A)
        and {inv_f[f] for f in ints(sets["R"])} == Rt.R and {inv_f[f] for f in ints(sets["X"])} == set(Rt.X),
        "B, W, A, R, X as printed")
    Rt.A = sorted(Rt.A)
    Rt._states = None
    say(Rt.divergence(b0) == len(Rt.white) and all(Rt.divergence(w) == -1 for w in Rt.white)
        and all(Rt.divergence(b) == 0 for b in Rt.A), "printed flow has divergence |W| at b0, -1 at whites, 0 elsewhere")

    # states
    st_note = {}
    for k, tup, q, c in re.findall(r"^\$s_\{(\d+)\}=\(([\d,]+)\)\$, \$Q_\{s_\d+\}=\\\{(.*?)\\\}\$, \$c_\{s_\d+\}=(-?\d+)\$", body, re.M):
        st_note[int(k)] = (tuple(inv_f[f] for f in ints(tup)), {edges[i] for i in ints(q)}, int(c))
    states = Rt.states()
    say(st_note and set(states) == {v[0] for v in st_note.values()}, "state list", f"{len(states)} states, {len(st_note)} printed")
    partners = {s: [r for r in states if Rt.is_pair(r, s)] for s in states}
    say(all(set(Rt.Q(s)) == q for s, q, c in st_note.values()), "every printed Q_s")
    say(all(sum(Rt.eps(r, s) for r in partners[s]) == c for s, q, c in st_note.values()), "every printed c_s")

    # pairs and their circuits
    sid = {v[0]: k for k, v in st_note.items()}
    blocks = re.split(r"^Pair ", body, flags=re.M)[1:]
    note_pairs = {}
    for blk in blocks:
        blk = blk.split("The exact polynomial")[0]
        i, j, sg = ints(blk.split("\n")[0])[:3]
        circs = []
        for fs, es, S, cnt, ds, sl in re.findall(
                r"Faces \$\(([\d,]+)\)\$; edges \$\(([^)]*)\)\$; cut side \$S=\\\{([\d,]+)\\\}\$\. Counts \$\(([\d,]+)\)\$; delta-sum \$(-?\d+)\$; slope \$(-?\d+)\$", blk):
            circs.append((ints(fs), [edges[k] for k in ints(es)], set(ints(S)), ints(cnt), int(ds), int(sl)))
        note_pairs[(i, j)] = (sg, circs)
    my_pairs = {(sid[r], sid[s]) for s in states for r in partners[s]}
    say(my_pairs == set(note_pairs), "set of ordered pairs", f"{len(my_pairs)} pairs")
    okc = True
    ncirc = 0
    for (i, j), (sg, circs) in note_pairs.items():
        r, s = st_note[i][0], st_note[j][0]
        okc &= Rt.eps(r, s) == sg
        mine_c = Rt.pair_circuits(r, s)
        okc &= len(mine_c) == len(circs)
        for fs, es, S, cnt, ds, sl in circs:
            ncirc += 1
            # find my circuit through the first printed face
            c = next(c for c in mine_c if any(x[0] == inv_f[fs[0]] for x in c))
            k = next(t for t, x in enumerate(c) if x[0] == inv_f[fs[0]])
            c = c[k:] + c[:k]
            d = Rt.circuit_data(c)
            okc &= [fmap[x[0]] for x in c] == fs and [x[2] for x in c] == es and d["S"] == S
            okc &= [d["nS"], d["nBS"], d["nES"], d["nUS"], d["h"], d["ell"]] == cnt
            okc &= d["dsum"] == ds and d["slope"] == sl
            sgm = next(iter(d["sigma"]))
            okc &= d["dsum"] == -3 * sgm and d["slope"] == sgm * d["nWS"] and d["h"] == 2 * d["ell"] + 3
    say(okc, "every printed pair sign, circuit, cut side, count tuple, delta-sum and slope", f"{ncirc} circuits")

    # polynomial
    Z = [0]
    for s in states:
        Ls = [1]
        for b, f in zip(Rt.A, s):
            Ls = pmul(Ls, [1, Rt.pot[b][f]])
        for r in partners[s]:
            Z = padd(Z, pscale(Rt.eps(r, s), Ls))
    Z = ptrim(Z)
    ptxt = re.search(r"Z\(z\)=([^\n$]+)", body.split("The exact polynomial is")[1]).group(1).rstrip(".")
    Zn = {}
    for sign, coef, zpart, power in re.findall(r"([+-]?)(\d+)(z?)(?:\^(\d+))?", ptxt):
        if coef:
            Zn[int(power) if power else (1 if zpart else 0)] = int(sign + coef)
    Znote = ptrim([Zn.get(i, 0) for i in range(max(Zn) + 1)])
    say(Z == Znote, "the printed polynomial Z(z)", f"mine {Z}, note {Znote}")

    # cancellation claim (second example only)
    m = re.search(r"cancelling second state is \$s_\{(\d+)\}\$\. Its two partners are \$s_\{(\d+)\}\$ with sign \$(-?\d+)\$ and \$s_\{(\d+)\}\$ with sign \$(-?\d+)\$\. The fixed circuit of \$Q_s\$ is the face sequence \$\(([\d,]+)\)\$", body)
    if m:
        k, p1, g1, p2, g2 = (int(m.group(i)) for i in range(1, 6))
        s = st_note[k][0]
        ps = {sid[r]: Rt.eps(r, s) for r in partners[s]}
        Qs = Rt.Q(s)
        cycs = undirected_cycles(range(G.nF), [(i, *G.efaces[e]) for i, e in enumerate(Qs)])
        cf = [{fmap[f] for i in c for f in G.efaces[Qs[i]]} for c in cycs]
        say(ps == {p1: g1, p2: g2} and set(ints(m.group(6))) in cf, "the printed cancelling state, its partners and its Q-circuit",
            f"circuits of Q_s: {cf}")
        c = next(c for c in cycs if {fmap[f] for i in c for f in G.efaces[Qs[i]]} == set(ints(m.group(6))))
        onc = {Rt.A[i] for i in c}
        r = st_note[p1][0]
        r2 = tuple(Rt.third(b, f, g) if b in onc else f for b, f, g in zip(Rt.A, r, s))
        say(sid[r2] == p2, "reversing that circuit exchanges the two partners")
        cyclic = [k for k, v in st_note.items() if not is_forest(range(G.nF), [(i, *G.efaces[e]) for i, e in enumerate(Rt.Q(v[0]))])]
        say(True, "states with a circuit in Q_s", cyclic)

    # recovery
    rec = body.split("For recovery choose")[1]
    k = int(re.search(r"\$s_\{(\d+)\}\$", rec).group(1))
    sets_e = [{edges[i] for i in ints(x)} for x in re.findall(r"\\\{((?:e_\{\d+\},?)+)\\\}", rec)]
    removed, tree, P = sets_e[:3]
    cyc = ints(re.search(r"cyclic vertex order, is \$\(([\d,]+)\)\$", rec).group(1))
    s = st_note[k][0]
    rem = set(Rt.Q(s)) | {E(b0, u) for u in G.rot[b0] if E(b0, u) != e0}
    say(rem == removed and set(G.edges) - rem == tree, "printed removed set and recovery tree")
    par = {b0: None}
    stack = [b0]
    while stack:
        x = stack.pop()
        for y in G.rot[x]:
            if y not in par and E(x, y) not in rem:
                par[y] = x
                stack.append(y)
    myP = {E(w, par[w]) for w in Rt.white}
    say(myP == P and e0 in P, "printed perfect matching P")
    cedges = {E(cyc[i - 1], cyc[i]) for i in range(len(cyc))}
    say(len(set(cyc)) == len(G.V) and cedges == set(G.edges) - P and e0 not in cedges, "printed Hamiltonian cycle is G - P and avoids e0")


parts = TEXT.split("### ")
for p in parts[1:]:
    title, body = p.split("\n", 1)
    run(title, body)
bad = [r for r in REPORT if not r[0]]
print(f"\n{len(REPORT)} comparisons, {len(bad)} failed")
