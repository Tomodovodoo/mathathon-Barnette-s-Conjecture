"""Graph generation only.  Calls the plantri binary built by workings/barnette_lab
(plantri -ba N lists Eulerian triangulations with N vertices, one per
isomorphism class, each with its rotation system) and turns each
triangulation into its dual cubic graph with a rotation system.  The parsing
and the dualisation are the referee's code.
"""
import subprocess
from pathlib import Path
from primal import PG

ROOT = Path(__file__).resolve().parents[3]
PLANTRI = ROOT / "workings/barnette_lab/vendor/plantri.exe"


def triangulations(n):
    run = subprocess.run([str(PLANTRI), "-ba", str(n)], capture_output=True, text=True, check=True, timeout=600)
    for line in run.stdout.splitlines():
        k, data = line.split()
        rot = [[ord(c) - 97 for c in part] for part in data.split(",")]
        assert len(rot) == int(k) == n
        yield rot


def dual_cubic(trot):
    """Dual of a triangulation given by rotation lists.  Returns PG."""
    n = len(trot)
    dface, tris = {}, []
    for a in range(n):
        for b in trot[a]:
            if (a, b) in dface:
                continue
            d, walk = (a, b), []
            while d not in dface:
                dface[d] = len(tris)
                walk.append(d)
                x, y = d
                i = trot[y].index(x)
                d = (y, trot[y][(i + 1) % len(trot[y])])
            assert len(walk) == 3, "not a triangulation"
            tris.append(walk)
    rot = {t: [dface[(y, x)] for (x, y) in walk] for t, walk in enumerate(tris)}
    return PG(rot)


def cube():
    # vertices are bit triples; rotation written by hand, checked by genus0()
    rot = {0: [1, 2, 4], 1: [0, 5, 3], 2: [0, 3, 6], 3: [1, 7, 2],
           4: [0, 6, 5], 5: [1, 4, 7], 6: [2, 7, 4], 7: [3, 5, 6]}
    return PG(rot)


def family(nmin, nmax):
    out = []
    for n in range(nmin, nmax + 1):
        for j, t in enumerate(triangulations(n)):
            out.append((f"T{n}_{j}", dual_cubic(t)))
    return out
