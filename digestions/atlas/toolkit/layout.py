"""Disk layout for a rooted triangulation.

The outer black face t0 is the unbounded region. Its three edges are drawn as
arcs of one circle of radius R with the roots on it, 120 degrees apart, so the
bounded faces fill a disk and each root has a half-plane of directions for its
edges. (Inside a straight outer triangle a root has only 60 degrees, which is
what made the first layout full of slivers.)

Interior coordinates start from a Tutte embedding and are then relaxed to
minimise

    sum over corners of 1/sin(angle/2)^2  +  AREA_WEIGHT * sum over faces of log(area/mean)^2,

with the true angles and areas of the three faces that have an arc as a side.
The search is a plain coordinate descent that never accepts a flipped face.

Run:  python paper/figures/layout.py running     (or: octahedron)
writes layout-<name>.json and prints the smallest corner angle and area spread.
Normal builds only read the saved file.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

from model import HERE, Model, und

R = 5.0
ROOT_ANGLES = (210.0, 330.0, 90.0)          # e0 = first two roots is the bottom arc
AREA_WEIGHT = 6.0
CAP = 3.0                                    # target area of the three faces on the outer arcs, in units of the others
SEGMENT = R * R / 2 * (2 * math.pi / 3 - math.sin(2 * math.pi / 3))   # area between a chord and its arc


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def tutte(m, fixed):
    import networkx as nx
    inner = [v for v in m.V if v not in fixed]
    L = nx.laplacian_matrix(m.T, nodelist=inner + list(fixed)).toarray().astype(float)
    k = len(inner)
    sol = np.linalg.solve(L[:k, :k], -L[:k, k:] @ np.array([fixed[v] for v in fixed]))
    return {**{v: np.array(p) for v, p in fixed.items()}, **dict(zip(inner, sol))}


def face_measures(m, xy):
    """For every bounded face: (area, [three corner angles in radians]).

    A face with an outer edge has a circular arc as that side: its area gains
    the circular segment, and its two root corners gain 60 degrees each.
    Returns None if some straight triangle with no outer side is flipped.
    """
    roots = set(m.roots)
    out = {}
    for i, f in enumerate(m.F):
        if i == m.t0:
            continue
        p = [xy[v] for v in f]
        area = cross(p[1] - p[0], p[2] - p[0]) / 2
        outer = sum(v in roots for v in f) == 2
        ang = []
        for k in range(3):
            a, b, c = p[k], p[(k + 1) % 3], p[(k + 2) % 3]
            th = math.atan2(cross(b - a, c - a), float(np.dot(b - a, c - a)))   # signed
            if outer and f[k] in roots:
                th += math.pi / 3
            elif outer and th < 0:
                th += 2 * math.pi                                    # reflex corner inside the segment
            ang.append(th)
        if outer:
            area += SEGMENT
        if area <= 0 or min(ang) <= 0.02:
            return None
        out[i] = (area, ang)
    return out


def energy(m, xy):
    fm = face_measures(m, xy)
    if fm is None:
        return math.inf
    if any(np.hypot(*xy[v]) > R * 0.985 for v in m.X):
        return math.inf
    roots = set(m.roots)
    unit = math.pi * R * R / (len(fm) - 3 + 3 * CAP)
    e = 0.0
    for i, (area, ang) in fm.items():
        cap = sum(v in roots for v in m.F[i]) == 2
        e += AREA_WEIGHT * math.log(area / (unit * (CAP if cap else 1))) ** 2
        e += sum(1 / math.sin(min(a, math.pi - 1e-3) / 2) ** 2 for a in ang) / 10
    return e


def relax(m, xy, rounds=400):
    xy = {v: p.copy() for v, p in xy.items()}
    best = energy(m, xy)
    assert math.isfinite(best), 'start layout is not a valid drawing'
    step = 0.4
    dirs = [np.array([math.cos(t), math.sin(t)]) for t in np.linspace(0, 2 * math.pi, 12, endpoint=False)]
    for _ in range(rounds):
        moved = False
        for v in m.X:
            for d in dirs:
                old = xy[v].copy()
                xy[v] = old + step * d
                e = energy(m, xy)
                if e < best - 1e-12:
                    best, moved = e, True
                else:
                    xy[v] = old
        if not moved:
            step /= 2
            if step < 1e-4:
                break
    return xy, best


def report(m, xy):
    fm = face_measures(m, xy)
    roots = set(m.roots)
    areas = [a for i, (a, _) in fm.items() if sum(v in roots for v in m.F[i]) < 2]
    angs = [math.degrees(a) for _, an in fm.values() for a in an]
    return dict(min_angle_deg=round(min(angs), 1), max_angle_deg=round(max(angs), 1),
                inner_area_ratio=round(max(areas) / min(areas), 2))


def make(name):
    d = json.loads((HERE / f'{name}.json').read_text())
    m = Model(d['faces'], d['t0'], d.get('e0'))
    # Root order on the circle: e0 at the bottom, faces counterclockwise.
    third = next(v for v in m.roots if v not in m.e0)
    a, b = m.e0
    if m.left[a, b] == m.t0:            # outer face on the left of a -> b means a -> b runs clockwise
        a, b = b, a
    fixed = {v: R * np.array([math.cos(math.radians(t)), math.sin(math.radians(t))])
             for v, t in zip((a, b, third), ROOT_ANGLES)}
    xy = tutte(m, fixed)
    for f in m.F:
        if f != m.F[m.t0]:
            assert cross(xy[f[1]] - xy[f[0]], xy[f[2]] - xy[f[0]]) > 0, 'Tutte drawing is mirrored'
    before = report(m, xy)
    xy, e = relax(m, xy)
    after = report(m, xy)
    out = dict(R=R, root_angles=dict(zip(map(str, (a, b, third)), ROOT_ANGLES)),
               coordinates={str(v): [round(float(p[0]), 3), round(float(p[1]), 3)] for v, p in sorted(xy.items())},
               tutte=before, relaxed=after)
    (HERE / f'layout-{name}.json').write_text(json.dumps(out, indent=1))
    print(name, 'Tutte', before, '-> relaxed', after)


if __name__ == '__main__':
    for n in sys.argv[1:] or ['running', 'octahedron']:
        make(n)
