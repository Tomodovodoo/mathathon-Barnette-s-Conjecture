"""Referee's numerical check of Lemmas 1-13 and Theorem T of the primal note.

usage: python check_lemmas.py NMIN NMAX [--light]
  NMIN..NMAX  number of faces of G (= vertices of the dual triangulation)
  --light     skip the exhaustive bond enumeration of Lemma 2 (2^(|V|-1) subsets)

Every check is counted; a failed check is counted under '<name> FAIL' and
the first failures are printed.  Nothing is asserted silently.
"""
import sys, json, random, time
from collections import Counter
from itertools import combinations
from primal import PG, Rooted, E, undirected_cycles, is_forest, padd, pmul, pscale, ptrim
from gen import family, cube

C = Counter()
FAIL = []
STAT = Counter()


def chk(name, cond, info=None):
    C[name] += 1
    if not cond:
        C[name + " FAIL"] += 1
        if len(FAIL) < 100:
            FAIL.append((name, repr(info)[:400]))


# --------------------------------------------------------------------------
def order_cycle(G, eset):
    """Cyclic list of (face, edge, next face) for a dual cycle given by its edges."""
    inc = {}
    for e in eset:
        for f in G.efaces[e]:
            inc.setdefault(f, []).append(e)
    f0 = min(inc)
    e = inc[f0][0]
    out, f = [], f0
    while True:
        a, b = G.efaces[e]
        g = b if a == f else a
        out.append((f, e, g))
        f = g
        if f == f0:
            break
        e = next(x for x in inc[f] if x != e)
    return out


def graph_level(name, G, exhaustive):
    V, n1 = G.V, len(G.V) // 2
    col = G.bipartition()
    # ---- Lemma 1 ----
    chk("L1 face boundary is a cycle", all(len(set(w)) == len(w) for w in G.faces))
    chk("L1 three distinct faces at each vertex", all(len(set(G.corner[v])) == 3 for v in V))
    share = Counter(frozenset(G.efaces[e]) for e in G.edges)
    chk("L1 two faces share at most one edge", max(share.values()) == 1 and all(len(k) == 2 for k in share))
    nb = sum(1 for v in V if col[v] == 0)
    chk("L1 counts", nb == len(V) - nb == n1 and len(G.edges) == 3 * n1 and G.nF == n1 + 2)
    chk("input simple cubic bipartite genus 0 3-edge-connected",
        G.simple and G.genus0() and col is not None and G.three_edge_connected())
    # ---- Lemma 2(a): face circuits are exactly bonds ----
    links = [(e, *G.efaces[e]) for e in G.edges]
    cycles = undirected_cycles(range(G.nF), links)
    STAT["face circuits"] += len(cycles)
    rooted = [Rooted(G, V[0]), Rooted(G, G.rot[V[0]][0])]   # both colourings
    for cyc in cycles:
        comps = G.components(set(cyc))
        isbond = len(comps) == 2 and G.cut(comps[0]) == set(cyc)
        chk("L2a face circuit is a bond", isbond, (name, sorted(map(sorted, cyc))))
        if not isbond:
            continue
        oc = order_cycle(G, cyc)
        cfaces = {f for f, _, _ in oc}
        for S in comps:
            chk("L2a shore connected", G.connected(verts=S))
            ES = {e for e in G.edges if e & S}
            US = {f for f in range(G.nF) if G.fverts[f] & S}
            chk("L2b Euler |S|+|U_S|=|E_S|+1", len(S) + len(US) == len(ES) + 1, (name, sorted(S)))
            mixed = {f for f in range(G.nF) if (G.fverts[f] & S) and (G.fverts[f] - S)}
            chk("L2b mixed faces = circuit faces", mixed == cfaces)
            chk("L2b mixed face has a cut edge", all(G.fedges[f] & cyc for f in mixed))
            # ---- Lemma 3 for both colourings and both directions ----
            for Rt in rooted:
                sg = {Rt.delta(Rt.bend[e], f, g) * ((Rt.bend[e] in S) - (Rt.wend[e] in S)) for f, e, g in oc}
                sgr = {Rt.delta(Rt.bend[e], g, f) * ((Rt.bend[e] in S) - (Rt.wend[e] in S)) for f, e, g in oc}
                chk("L3 common sigma", len(sg) == 1 and len(sgr) == 1 and sg != sgr and sg <= {1, -1})
    if exhaustive:
        idx = {v: i for i, v in enumerate(V)}
        N = len(V)
        nbm = [0] * N
        for v in V:
            for u in G.rot[v]:
                nbm[idx[v]] |= 1 << idx[u]
        full = (1 << N) - 1

        def conn(mask):
            comp = mask & -mask
            fr = comp
            while fr:
                nxt = 0
                while fr:
                    lb = fr & -fr
                    nxt |= nbm[lb.bit_length() - 1]
                    fr ^= lb
                fr = nxt & mask & ~comp
                comp |= fr
            return comp == mask

        bonds = bad_euler = unconn = 0
        deg = {i: None for i in range(N)}
        for mask in range(1, 1 << (N - 1)):
            if conn(mask):
                if conn(full ^ mask):
                    bonds += 1
                else:
                    unconn += 1
        chk("L2a number of bonds = number of face circuits", bonds == len(cycles), (name, bonds, len(cycles)))
        STAT["bonds by subset enumeration"] += bonds
    # ---- Lemma 11 over all perfect matchings ----
    pms = G.perfect_matchings()
    STAT["perfect matchings"] += len(pms)
    for M in pms:
        comps = G.components(M)
        for k in range(1, len(comps)):
            for sub in combinations(comps, k):
                S = set().union(*sub)
                cut = G.cut(S)
                h = len(cut)
                for c in (0, 1):
                    ell = sum(1 for e in cut if any(col[v] == c and v in S for v in e))
                    chk("L11 h = 2 ell", cut <= M and h == 2 * ell)
    # ---- Theorem T by brute force ----
    ham = [M for M in pms if G.connected(M)]
    STAT["Hamiltonian cycles"] += len(ham)
    for e in G.edges:
        chk("T brute force: Hamiltonian cycle avoiding each edge", any(e in M for M in ham), (name, sorted(e)))
    # ---- Lemma 13 ----
    cuts = G.three_cuts()
    nontriv = [(S, T) for S, T in cuts if len(S) >= 2 and len(T) >= 2]
    STAT["3-edge cuts"] += len(cuts)
    STAT["nontrivial 3-edge cuts"] += len(nontriv)
    for S, T in nontriv:
        cut = G.cut(set(S))
        chk("L13 shores connected", G.connected(verts=S) and G.connected(verts=T))
        ell = sum(1 for e in cut if any(col[v] == 0 and v in S for v in e))
        chk("L13 ell in {0,3}", ell in (0, 3))
        capdata = []
        for keep in (S, T):
            good, emap, ends = G.cap(keep, ("*", len(keep)))
            chk("L13 three distinct ends", len(set(ends)) == 3)
            chk("L13 cap planar (one rotation at the new vertex has genus 0)", len(good) >= 1, (name, len(good)))
            STAT[f"L13 rotations at cap vertex with genus 0: {len(good)}"] += 1
            if not good:
                continue
            g = good[0]
            chk("L13 cap simple cubic bipartite 3-edge-connected smaller",
                g.simple and g.bipartition() is not None and g.three_edge_connected() and len(g.V) < len(V))
            star = ("*", len(keep))
            cyc = [M for M in g.perfect_matchings() if g.connected(M)]
            capdata.append((g, emap, star, cyc))
        if len(capdata) == 2:
            (g1, m1, s1, c1), (g2, m2, s2, c2) = capdata
            for M1 in c1:
                a1 = m1[next(e for e in M1 if s1 in e)]
                for M2 in c2:
                    a2 = m2[next(e for e in M2 if s2 in e)]
                    if a1 == a2:
                        M = {m1[e] for e in M1} | {m2[e] for e in M2}
                        ok = len(M) == len(V) // 2 and all(sum(1 for e in M if v in e) == 1 for v in V) and G.connected(M)
                        chk("L13 glued cycles form a Hamiltonian cycle", ok)
    return pms, nontriv


# --------------------------------------------------------------------------
def kuhn(allowed, left):
    match = {}

    def aug(b, seen):
        for f in allowed[b]:
            if f in seen:
                continue
            seen.add(f)
            if f not in match or aug(match[f], seen):
                match[f] = b
                return True
        return False
    return all(aug(b, set()) for b in left)


def recover(Rt, s, e0):
    """Lemmas 9, 10: returns (K edges, P) or raises."""
    G = Rt.G
    rem = set(Rt.Q(s)) | {E(Rt.b0, u) for u in G.rot[Rt.b0] if E(Rt.b0, u) != e0}
    K = [e for e in G.edges if e not in rem]
    return rem, K


def tree_matching(Rt, rem):
    G = Rt.G
    par = {Rt.b0: None}
    stack = [Rt.b0]
    while stack:
        x = stack.pop()
        for y in G.rot[x]:
            if y not in par and E(x, y) not in rem:
                par[y] = x
                stack.append(y)
    return {E(w, par[w]) for w in Rt.white if w in par}, par


def rooted_level(name, G, b0, trivial_only, pms, rng):
    Rt = Rooted(G, b0)
    A, X, n = Rt.A, Rt.X, len(Rt.A)
    chk("L1 |R|=3 and |X|=|A|", len(Rt.R) == 3 and len(X) == n)
    # ---- Lemma 6: flow ----
    chk("L6 divergences", Rt.divergence(b0) == len(Rt.white) and all(Rt.divergence(w) == -1 for w in Rt.white)
        and all(Rt.divergence(b) == 0 for b in A))
    for b in A:
        c = G.corner[b]
        e = G.sep_edge(b, 2, 0)
        chk("L6 local potentials consistent", Rt.pot[b][c[0]] - Rt.pot[b][c[2]] == -Rt.delta(b, c[2], c[0]) * Rt.alpha[e])
    # second flow: add random circulations along facial boundaries
    alpha2 = dict(Rt.alpha)
    for f in range(G.nF):
        c = rng.randint(-3, 3)
        w = G.faces[f]
        for i in range(len(w)):
            u, v = w[i], w[(i + 1) % len(w)]
            alpha2[E(u, v)] += c if u in Rt.black else -c
    Rt2 = Rooted(G, b0, alpha=alpha2)
    chk("L6 second flow has the same divergences", Rt2.divergence(b0) == len(Rt.white) and all(Rt2.divergence(b) == 0 for b in A))

    states = Rt.states()
    STAT["states"] += len(states)
    partners = {s: [r for r in states if Rt.is_pair(r, s)] for s in states}
    npairs = sum(len(v) for v in partners.values())
    STAT["ordered pairs"] += npairs
    STAT["rootings (vertex b0)"] += 1
    if npairs:
        STAT["rootings with a pair"] += 1

    # ---- Lemma 4 ----
    Xi = {f: i for i, f in enumerate(X)}
    nbr = [sum(1 << Xi[f] for f in G.corner[b] if f in Xi) for b in A]
    deficit = {}
    for Y in range(1 << n):
        deficit[Y] = 2 * bin(Y).count("1") - sum(min(2, bin(m & Y).count("1")) for m in nbr)
    cap_ok = all(d <= 0 for d in deficit.values())
    chk("L4 capacity condition (3.1) holds iff a pair exists", cap_ok == (npairs > 0), (name, b0))
    if trivial_only:
        chk("L4 irreducible graph has a pair for this root", npairs > 0, (name, b0))
    if not cap_ok:
        STAT["rootings where (3.1) fails"] += 1
        pos = [Y for Y, d in deficit.items() if d > 0]
        minimal = [Y for Y in pos if not any(Z != Y and Z & Y == Z for Z in pos)]
        for Y in minimal:
            Yf = {X[i] for i in range(n) if Y >> i & 1}
            Kv = set().union(*(G.fverts[f] for f in Yf))
            Ke = set().union(*(G.fedges[f] for f in Yf))
            cnt = {v: sum(1 for f in G.corner[v] if f in Yf) for v in Kv}
            B1 = [v for v in Kv if v in Rt.black and cnt[v] == 1]
            W1 = [v for v in Kv if v in Rt.white and cnt[v] == 1]
            cut = G.cut(Kv)
            induced = Ke == {e for e in G.edges if e <= Kv}
            k = 2 - len(Kv) + len(Ke) - len(Yf)
            ok = (b0 not in Kv and not W1 and induced and len(cut) == len(B1) == 3
                  and all(Rt.bend[e] in Kv for e in cut) and G.connected(verts=Kv)
                  and k == 1 and deficit[Y] == 4 - 2 * k - len(cut) // 3 == 1
                  and len(Kv) >= 2 and len(set(G.V) - Kv) >= 2)
            chk("L4 minimal deficient set gives a nontrivial 3-cut with black inner ends", ok, (name, b0, sorted(Yf)))

    # ---- Lemmas 2, 3, 5, 6 on every state circuit of every state ----
    for r in states:
        for circ in Rt.state_circuits(r):
            d = Rt.circuit_data(circ)
            chk("L5 state circuit is a bond", d is not None)
            if d is None:
                continue
            STAT["state circuits (all choices)"] += 1
            STAT[f"state circuit length {d['h']}"] += 1
            chk("L2a no root face meets the cut side", d["rootfree"])
            chk("L5 count 1: 3|S|+h=2|E_S|", 3 * d["nS"] + d["h"] == 2 * d["nES"])
            chk("L5 count 2: 3|B_S|+h=|E_S|+ell", 3 * d["nBS"] + d["h"] == d["nES"] + d["ell"])
            chk("L5 count 3: |S|+|U|=|E_S|+1", d["nS"] + d["nUS"] == d["nES"] + 1)
            chk("L5 count 4: |B_S|+h=|U|+ell", d["nBS"] + d["h"] == d["nUS"] + d["ell"])
            inv = {f: b for b, f in zip(A, r)}
            chk("L5 U = r(B_S) union C", d["US"] == {inv_f for inv_f in d["US"] if inv_f in inv and inv[inv_f] in d["S"]} | d["faces"])
            chk("L5 h=2ell+3", d["h"] == 2 * d["ell"] + 3)
            chk("L5 |W_S|=|B_S|+1", d["nWS"] == d["nBS"] + 1)
            chk("L3 common sigma on state circuit", len(d["sigma"]) == 1)
            sg = next(iter(d["sigma"]))
            chk("L5 delta sum = -3 sigma", d["dsum"] == -3 * sg)
            chk("L6 slope = sigma |W_S| (path flow)", d["slope"] == sg * d["nWS"])
            sl2 = sum(Rt2.pot[b][g] - Rt2.pot[b][f] for f, b, e, g in circ)
            chk("L6 slope = sigma |W_S| (second flow)", sl2 == sg * d["nWS"])

    # ---- Lemma 7 ----
    faces = list(range(G.nF))
    forest_state = {}
    csum = {}
    for s in states:
        Qs = Rt.Q(s)
        chk("Q_s has n distinct edges", len(set(Qs)) == n)
        links = [(i, *G.efaces[e]) for i, e in enumerate(Qs)]
        cycs = undirected_cycles(faces, links)
        forest_state[s] = not cycs
        chk("forest test agrees with union-find", (not cycs) == is_forest(faces, links))
        ps = partners[s]
        csum[s] = sum(Rt.eps(r, s) for r in ps)
        if cycs and ps:
            STAT["cyclic second states with partners"] += 1
            chk("L7 partner signs cancel", csum[s] == 0, (name, b0, s))
            pset = set(ps)
            for cyc in cycs:
                onc = {A[i] for i in cyc}
                chk("L7 circuit of Q_s is odd and avoids R", len(cyc) % 2 == 1 and
                    not any(f in Rt.R for i in cyc for f in G.efaces[Qs[i]]))
                for r in ps:
                    r2 = tuple(Rt.third(b, f, g) if b in onc else f for b, f, g in zip(A, r, s))
                    r3 = tuple(Rt.third(b, f, g) if b in onc else f for b, f, g in zip(A, r2, s))
                    chk("L7 reversal is a sign-reversing involution on partners",
                        r2 in pset and r2 != r and r3 == r and Rt.eps(r2, s) == -Rt.eps(r, s))
        elif cycs:
            STAT["cyclic second states without partners"] += 1
        elif ps:
            STAT[f"forest second states with {len(ps)} partner(s)"] += 1
        else:
            STAT["forest states without partner"] += 1

    # ---- Lemma 8 ----
    if npairs:
        Z = [0]
        groups = {}
        for s in states:
            Ls = [1]
            for b, f in zip(A, s):
                Ls = pmul(Ls, [1, Rt.pot[b][f]])
            for r in partners[s]:
                Z = padd(Z, pscale(Rt.eps(r, s), Ls))
                D = frozenset(Rt.edge_between(b, f, g) for b, f, g in zip(A, r, s))
                groups.setdefault(D, []).append((r, s, pscale(Rt.eps(r, s), Ls)))
        Z = ptrim(Z)
        m = None
        low = 0
        for D, members in groups.items():
            r, s, _ = members[0]
            circs = Rt.pair_circuits(r, s)
            c = len(circs)
            chk("L8 circuits of D are odd, length >= 3, cover X",
                all(len(x) % 2 == 1 and len(x) >= 3 for x in circs) and sum(len(x) for x in circs) == n)
            chk("L8 group has 2^c pairs", len(members) == 2 ** c)
            prod = [(-1) ** ((n - c) // 2)]
            lam = 1
            for circ in circs:
                d = Rt.circuit_data(circ)
                sg = next(iter(d["sigma"]))
                pos = circ if sg == 1 else [(g, b, e, f) for f, b, e, g in circ]
                Lp, Lm = [1], [1]
                for f, b, e, g in pos:
                    Lp = pmul(Lp, [1, Rt.pot[b][g]])
                    Lm = pmul(Lm, [1, Rt.pot[b][f]])
                diff = padd(Lp, pscale(-1, Lm))
                chk("L8 difference has zero constant term and slope |W_S|>0",
                    diff[0] == 0 and diff[1] == d["nWS"] > 0)
                # number of negative local signs on the positive orientation
                neg = sum(1 for f, b, e, g in pos if Rt.delta(b, f, g) == -1)
                chk("L8 positive orientation has (h+3)/2 negative signs", 2 * neg == len(circ) + 3)
                prod = pmul(prod, diff)
                lam *= d["nWS"]
            tot = [0]
            for _, _, t in members:
                tot = padd(tot, t)
            chk("L8 group sum equals (6.3)", ptrim(tot) == ptrim(prod), (name, b0))
            if m is None or c < m:
                m, low = c, 0
            if c == m:
                low += lam
        chk("L8 Z nonzero", bool(Z))
        chk("L8 lowest coefficient (6.4)", Z[:m] == [0] * m and Z[m] == (-1) ** ((n - m) // 2) * low, (name, b0, Z, m, low))
        Zf = [0]
        for s in states:
            if forest_state[s] and partners[s]:
                Ls = [1]
                for b, f in zip(A, s):
                    Ls = pmul(Ls, [1, Rt.pot[b][f]])
                Zf = padd(Zf, pscale(csum[s], Ls))
        chk("L7+L8 Z equals the sum over forest second states", ptrim(Zf) == Z)
        chk("L8 a pair with circuit-free Q_s exists", any(forest_state[s] and partners[s] for s in states))
        STAT[f"minimum circuit number m={m}"] += 1

    # ---- Lemmas 9, 10, 12 ----
    root_edges = [E(b0, u) for u in G.rot[b0]]
    for s in states:
        if not forest_state[s]:
            continue
        for e0 in root_edges:
            rem, K = recover(Rt, s, e0)
            istree = G.connected(rem) and len(K) == len(G.V) - 1
            if not partners[s]:
                STAT["L9 for a forest state WITHOUT partner: K is a tree" if istree else
                     "L9 for a forest state WITHOUT partner: K is not a tree"] += 1
                continue
            chk("L9 K is a spanning tree", istree, (name, b0, s))
            Llinks = [(i, *G.efaces[e]) for i, e in enumerate(rem)]
            chk("L9 removed links form a face tree", is_forest(faces, Llinks) and len(rem) == G.nF - 1)
            degK = {v: sum(1 for u in G.rot[v] if E(v, u) not in rem) for v in G.V}
            chk("L9 degrees", degK[b0] == 1 and all(degK[b] == 2 for b in A))
            P, par = tree_matching(Rt, rem)
            pm = all(sum(1 for e in P if v in e) == 1 for v in G.V)
            chk("L10 P is a perfect matching in K containing e0", pm and e0 in P and not (P & rem))
            chk("L10 P edge at b lies on s(b)", all(next(e for e in P if b in e) in G.fedges[f] for b, f in zip(A, s)))
            Pl = [(i, *G.efaces[e]) for i, e in enumerate(P - {e0})]
            chk("L12 P minus e0 is a face forest, P has no face circuit",
                is_forest(faces, Pl) and is_forest(faces, [(i, *G.efaces[e]) for i, e in enumerate(P)]))
            chk("L12 G-P is a Hamiltonian cycle avoiding e0", G.connected(P))
            STAT["recoveries (forest state with partner, root edge)"] += 1

    # ---- Lemma 12 in the generality its proof gives ----
    for M in pms:
        allowed = {}
        for b in A:
            e = next(e for e in M if b in e)
            allowed[b] = [f for f in G.efaces[e] if f in Xi]
        comp = kuhn(allowed, A)
        conn = G.connected(M)
        if comp:
            chk("L12 general: matching compatible with some state has connected complement", conn, (name, b0))
        STAT[f"matchings: compatible state {comp}, complement connected {conn}"] += 1
    return Rt


# --------------------------------------------------------------------------
def solve(G, e0, b0, depth=0):
    """The proof of Theorem T as an algorithm.  Returns a perfect matching
    containing e0 whose complement is connected."""
    if not hasattr(G, "_cuts"):
        G._cuts = [(S, T) for S, T in G.three_cuts() if len(S) >= 2 and len(T) >= 2]
    if not G._cuts:
        Rt = Rooted(G, b0)
        states = Rt.states()
        faces = list(range(G.nF))
        for s in states:
            if not is_forest(faces, [(i, *G.efaces[e]) for i, e in enumerate(Rt.Q(s))]):
                continue
            if not any(Rt.is_pair(r, s) for r in states):
                continue
            rem, K = recover(Rt, s, e0)
            P, _ = tree_matching(Rt, rem)
            STAT[f"solve: main case at depth {depth}"] += 1
            return P
        raise RuntimeError("no pair with circuit-free Q_s in an irreducible graph")
    S, T = G._cuts[0]
    if not (e0 & S):
        S, T = T, S
    star1, star2 = ("*", depth, 1), ("*", depth, 2)
    good1, m1, _ = G.cap(S, star1)
    good2, m2, _ = G.cap(T, star2)
    g1, g2 = good1[0], good2[0]
    inv1 = {v: k for k, v in m1.items()}
    inv2 = {v: k for k, v in m2.items()}
    e1 = inv1[e0]
    r1 = b0 if b0 in e1 else next(iter(e1 - {star1}))
    P1 = solve(g1, e1, r1, depth + 1)
    a = m1[next(e for e in P1 if star1 in e)]
    e2 = inv2[a]
    P2 = solve(g2, e2, next(iter(e2 - {star2})), depth + 1)
    STAT[f"solve: glue at depth {depth}"] += 1
    return {m1[e] for e in P1} | {m2[e] for e in P2}


def main():
    nmin, nmax = int(sys.argv[1]), int(sys.argv[2])
    light = "--light" in sys.argv
    rng = random.Random(20261114)
    t0 = time.time()
    graphs = ([("cube_by_hand", cube())] if nmin <= 6 else []) + family(nmin, nmax)
    for name, G in graphs:
        t1 = time.time()
        pms, nontriv = graph_level(name, G, exhaustive=not light and len(G.V) <= 24)
        STAT["graphs"] += 1
        STAT[f"graphs with {len(G.V)} vertices"] += 1
        if not nontriv:
            STAT["graphs without nontrivial 3-edge cut"] += 1
        for b0 in G.V:
            rooted_level(name, G, b0, not nontriv, pms, rng)
        for e0 in G.edges:
            for b0 in e0:
                P = solve(G, e0, b0)
                ok = e0 in P and all(sum(1 for e in P if v in e) == 1 for v in G.V) and G.connected(P)
                chk("T: recursive construction gives a matching through e0 with connected complement", ok, (name, sorted(e0)))
                STAT["rootings (b0, e0) solved by the recursion"] += 1
        print(f"# {name}: |V|={len(G.V)} nontrivial 3-cuts={len(nontriv)} time={time.time()-t1:.1f}s", flush=True)
    print(json.dumps({"range": [nmin, nmax], "light": light, "seconds": round(time.time() - t0, 1),
                      "checks": dict(sorted(C.items())), "stats": dict(sorted(STAT.items())),
                      "failures": FAIL}, indent=1))


if __name__ == "__main__":
    main()
