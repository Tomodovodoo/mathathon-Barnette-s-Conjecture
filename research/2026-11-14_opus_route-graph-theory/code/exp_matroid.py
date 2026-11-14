"""E1: matroid structure.  Families of n-edge sets Q in E(T) (edges of bounded black faces):
  BT = one edge per bounded black face, Q + two edges of t0 a spanning tree of T
  OT = one edge opposite each nonroot (opposite inside its black face), same tree condition
  TM = BT & OT (= Q_s of tree matchings s)
Tests: inclusions; basis-exchange axiom for BT, OT, TM.
Usage: python exp_matroid.py Vmax"""
import sys, itertools
from tri import generate, load
from states import Rooted, UF

def is_tree(R, Q):
    uf = UF(R.T.V)
    r = R.R
    uf.union(r[0], r[1]); uf.union(r[1], r[2])
    return all(uf.union(*e) for e in Q)

def families(R):
    Xs = set(R.X)
    BT = set()
    choices = [[R.opp(t, v) for v in t] for t in R.A]
    for Q in itertools.product(*choices):
        if is_tree(R, Q):
            BT.add(frozenset(Q))
    OT = set()
    ch2 = [[R.opp(t, x) for t in R.faces_at[x]] for x in R.X]
    for Q in itertools.product(*ch2):
        if is_tree(R, Q):
            OT.add(frozenset(Q))
    TM = {frozenset(R.Q(s)) for s in R.states() if R.is_tree_matching(s)}
    return BT, OT, TM

def exchange_fail(F):
    for B1 in F:
        for B2 in F:
            for e in B1 - B2:
                if not any((B1 - {e}) | {f} in F for f in B2 - B1):
                    return (B1, B2, e)
    return None

Vmax = int(sys.argv[1])
Vmin = int(sys.argv[2]) if len(sys.argv) > 2 else 6
for V in range(Vmin, Vmax + 1):
    try:
        Ts = load(V)
    except FileNotFoundError:
        Ts = generate(V)[V]
    stats = dict(inst=0, BTinOT=0, OTinBT=0, TMeq=0, BTmat=0, OTmat=0, TMmat=0)
    for T in Ts:
        for f in T.faces():
            R = Rooted(T, f)
            if R.black_inner_sep_triangles():
                continue
            BT, OT, TM = families(R)
            stats['inst'] += 1
            stats['BTinOT'] += BT <= OT
            stats['OTinBT'] += OT <= BT
            stats['TMeq'] += (BT & OT) == TM
            stats['BTmat'] += exchange_fail(BT) is None
            stats['OTmat'] += exchange_fail(OT) is None
            stats['TMmat'] += exchange_fail(TM) is None
            if V <= 8:
                print("  ", V, f, "|BT|", len(BT), "|OT|", len(OT), "|TM|", len(TM))
    print(V, stats, flush=True)
