"""Helpers shared by the referee scripts."""
def det_states(inst):
    """|det K_B| by fraction-free elimination (exact integers)."""
    idx = {v: i for i, v in enumerate(inst.X)}
    Mx = [[0] * inst.n for _ in inst.A]
    for i, t in enumerate(inst.A):
        for v in inst.corners[t]:
            Mx[i][idx[v]] = 1
    n = inst.n; prev = 1
    for k in range(n - 1):
        if Mx[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if Mx[i][k]), None)
            if sw is None: return 0
            Mx[k], Mx[sw] = Mx[sw], Mx[k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                Mx[i][j] = (Mx[i][j] * Mx[k][k] - Mx[i][k] * Mx[k][j]) // prev
        prev = Mx[k][k]
    return abs(Mx[n - 1][n - 1])
def tube_root(p, L):
    return (0, 1, p + 1) if L >= 1 else (p, 0, 1)
