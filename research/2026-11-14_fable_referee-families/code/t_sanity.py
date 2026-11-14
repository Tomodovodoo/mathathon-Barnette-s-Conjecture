"""Sanity checks of core.py: conventions, disk identity, (5.3), sign formula."""
from core import *
def check(inst, name):
    inst.check_circulation()
    res = inst.summary()
    # sign formula and (5.3) on every cover
    const = set(); gain = set()
    for d in inst.covers():
        cyc = inst.cover_cycles(d)
        ors = list(inst.orientations(d))
        for r, s, eps, js in ors:
            J = js // 3
            const.add(eps * (-1) ** ((inst.n + J) // 2))
        # single-cycle reversals: omega difference vs J difference
        r0, s0, e0, j0 = ors[0]
        for i in range(len(cyc)):
            r1, s1, e1, j1 = ors[1 << i]
            dJ = (j1 - j0) // 3          # +-2
            dw = inst.omega(s1) - inst.omega(s0)
            gain.add((dJ > 0) == (dw > 0))
            assert dw != 0
    H, use = hamilton(inst)
    print(name, 'V', len(inst.g), 'n', inst.n, {k: res[k] for k in ('S','P','M','good_pairs','m','poly')}, 'H', H, 'signconst', const, 'J-up<=>omega-up', gain)
    return res, H, use
check(Inst(bipyramid(4), (4,0,1)), 'cube')
for p in (6,8,10):
    check(Inst(bipyramid(p), (p,0,1)), f'prism{p}')
