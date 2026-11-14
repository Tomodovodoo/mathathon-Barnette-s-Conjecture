"""Minimal alpha-orientation of H0 by face flips, and tree pairs inside a 2-factor.
u: deleted-corner map (A -> corners).  A white triangle y = (a,b,c) avoiding the roots is a
directed facial cycle of the orientation iff u rotates around it: u(t_ab), u(t_bc), u(t_ca)
are a,b,c (one rotation) or b,c,a (the other).  Its sense comes from the Tutte drawing."""
import itertools
import numpy as np
from exp_alpha import tutte_positions, area
from pairs import flow_pair, third

def u_of(R, r, s):
    return {t: third(t, r[t], s[t]) for t in R.A}

def face_data(R):
    """for each flippable white face: (y, [(t, a, b)] sides with black faces)"""
    Rs = set(R.R)
    out = []
    for y in R.white:
        if Rs & set(y):
            continue
        sides = []
        for i in range(3):
            a, b = y[i], y[(i + 1) % 3]
            t = R.bf[frozenset((a, b))]
            sides.append((t, a, b))
        out.append((y, sides))
    return out

def flip_to_extreme(R, u, sense=+1, P=None):
    """repeatedly flip directed faces whose sense (sign of area of the directed hexagon)
    equals `sense` (+1 = ccw).  Returns final u."""
    if P is None:
        P = tutte_positions(R)
    faces = face_data(R)
    u = dict(u)
    changed = True
    while changed:
        changed = False
        for y, sides in faces:
            # pattern 1: u(t_ab)=a for all sides (directed a->t_ab->b ...)
            for k in (0, 1):
                if all(u[t] == (a if k == 0 else b) for (t, a, b) in sides):
                    # directed hexagon: k=0: a -> t_ab -> b ; k=1: b -> t_ab -> a (reverse)
                    cyc = []
                    for (t, a, b) in sides:
                        cyc += [a, ("c", t)]
                    sgn = 1 if area(P, cyc) > 0 else -1   # sense of a->t_ab->b traversal
                    if k == 1:
                        sgn = -sgn
                    if sgn == sense:
                        for (t, a, b) in sides:
                            u[t] = b if k == 0 else a
                        changed = True
    return u

def pairs_of_factor(R, u):
    """all ordered pairs (r,s) with deleted corners u: orient each cycle of the 2-factor"""
    # D-edge in t joins the two corners other than u(t); cycles on X
    adj = {x: [] for x in R.X}
    for t in R.A:
        p, q = [w for w in t if w != u[t]]
        adj[p].append((q, t)); adj[q].append((p, t))
    seen = set(); cycles = []
    for x0 in R.X:
        if x0 in seen:
            continue
        cyc = []  # list of (tail, head, t)
        prev_t = None; x = x0
        while True:
            seen.add(x)
            (y, t) = [(y, t) for (y, t) in adj[x] if t != prev_t][0] if prev_t else adj[x][0]
            cyc.append((x, y, t))
            prev_t = t; x = y
            if x == x0:
                break
        cycles.append(cyc)
    for mask in itertools.product((0, 1), repeat=len(cycles)):
        r, s = {}, {}
        for bit, cyc in zip(mask, cycles):
            for (x, y, t) in cyc:
                if bit == 0:
                    r[t], s[t] = x, y
                else:
                    r[t], s[t] = y, x
        yield r, s
