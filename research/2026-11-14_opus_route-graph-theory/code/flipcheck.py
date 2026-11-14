"""Independent check of tri.generate: BFS over the edge-flip graph of all
triangulations on V vertices (Wagner: connected), filter Eulerian ones."""
import sys
from tri import Tri
import networkx as nx

def flip(T, u, v):
    # faces u v w (left of u->v) and v u z
    _, w = T.nxt(u, v)
    _, z = T.nxt(v, u)
    if z in T.pos[w]:
        return None
    rot = {a: list(b) for a, b in T.rot.items()}
    rot[u].remove(v); rot[v].remove(u)
    # insert z-w edge: at w, between v and u ; at z between u and v
    # face (u,v,w) ccw: at w, ccw order ... u then v? find by rebuilding via networkx
    E = [e for e in T.edges() if set(e) != {u, v}] + [(w, z)]
    return Tri.from_edges(E)

def all_tris(V):
    # start: a "double wheel" triangulation
    edges = [(0, i) for i in range(2, V)] + [(1, i) for i in range(2, V)] + \
            [(i, i + 1) for i in range(2, V - 1)] + [(V - 1, 2)]
    T0 = Tri.from_edges(edges)
    seen = {T0.canon_code(): T0}
    stack = [T0]
    while stack:
        T = stack.pop()
        for (u, v) in T.edges():
            S = flip(T, u, v)
            if S is None:
                continue
            c = S.canon_code()
            if c not in seen:
                seen[c] = S
                stack.append(S)
    return list(seen.values())

for V in range(6, int(sys.argv[1]) + 1):
    ts = all_tris(V)
    print(V, len(ts), sum(T.is_eulerian() for T in ts), flush=True)
