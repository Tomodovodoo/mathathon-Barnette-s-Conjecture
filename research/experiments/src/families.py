"""The constructed families and the random ensembles.

families()  yields (source, params, F, t0) for every constructed graph; t0 is a
            prescribed face or None.
random_graphs(kind, V, count, chains, seed)  samples by the Markov chain.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))
import fb                                                     # noqa: E402
import graphs                                                 # noqa: E402
import symmetry                                               # noqa: E402

MAX_FACES = 4100

# The Eulerian triangulation with 11 vertices and no separating triangle, the
# start of the chain for odd sizes (plantri -bc4 11).
ODD_START = None


def plantri_maps(args, every=1, limit=None):
    """Plane maps from plantri (neighbour lists), every `every`-th one."""
    path = ROOT / 'build' / ('maps_' + '_'.join(a.strip('-').replace('/', 'of') for a in args) + '.pc')
    subprocess.run([str(ROOT / 'build' / 'bin' / 'plantri.exe'), *args, str(path)],
                   check=True, capture_output=True)
    out = []
    for i, rot in enumerate(graphs.read_planar_code(path)):
        if i % every == 0:
            out.append((i, rot))
            if limit and len(out) >= limit:
                break
    path.unlink()
    return out


def odd_start():
    global ODD_START
    if ODD_START is None:
        (_, rot), = plantri_maps(['-bc4', '11'])
        ODD_START = graphs.faces_of_rotation(rot)
    return ODD_START


def grow(steps, p_octahedron, seed):
    """Growth from the octahedron: at each step, with probability
    p_octahedron an octahedron is put into a uniformly random face, otherwise
    a uniformly random vertex split is made (a random edge, then a random
    second edge at its tail among those that keep the degrees even)."""
    rng = np.random.default_rng(seed)
    F = graphs.octahedron()
    for _ in range(steps):
        if rng.random() < p_octahedron:
            F = graphs.insert_octahedron(F, int(rng.integers(len(F))))
        else:
            rot = graphs.rotation_of_faces(F)
            f = F[int(rng.integers(len(F)))].tolist()
            k = int(rng.integers(3))
            a, b = f[k], f[(k + 1) % 3]
            ring = rot[a]
            i = ring.index(b)
            gap = 2 * int(rng.integers(1, len(ring) // 2))
            F = graphs.split_vertex(F, a, b, ring[(i + gap) % len(ring)])
    return graphs.relabel(F)


def families():
    out = []

    def add(source, params, F, t0=None):
        F = np.ascontiguousarray(F, dtype=np.int32)
        if len(F) <= MAX_FACES:
            out.append((source, params, F, t0))

    # prisms and tubes
    for k in list(range(2, 13)) + [14, 16, 20, 24, 32, 40, 50, 64, 80, 100, 128, 160, 200, 256,
                                   320, 400, 512, 750, 1000]:
        add('prism', f'k={k}', graphs.bipyramid(k))
    for k in (2, 3, 4, 5, 6, 8, 12, 16, 32):
        for m in (2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 50, 64, 80, 100, 128, 160, 200, 250):
            if 4 * k * m <= 2000:
                add('tube', f'k={k} m={m}', graphs.tube(k, m))
    for m in list(range(1, 13)) + [14, 16, 20, 24, 32, 40, 50, 64, 80, 100, 128, 160]:
        add('nanotube', f'm={m}', graphs.nanotube(m))

    # octahedral symmetry, only 4- and 6-faces
    for k in range(1, 17):
        for l in range(0, k + 1):
            if k * k + k * l + l * l <= 256:
                add('octahedral', f'k={k} l={l}', graphs.octahedral(k, l))

    # omnitruncated polyhedra and their Goldberg-Coxeter images
    for name in ('tetrahedron', 'cube', 'dodecahedron'):
        base = graphs.omnitruncated(name)
        add('omnitruncated', name, base)
        for k, l in ((2, 0), (1, 1), (2, 1), (3, 0), (2, 2), (3, 1), (4, 0)):
            add('omnitruncated-gc', f'{name} k={k} l={l}', graphs.goldberg_coxeter(base, k, l))

    # duals of barycentric subdivisions of plane maps
    import networkx as nx
    for v in range(4, 9):
        for i, rot in plantri_maps(['-p', str(v)]):
            add('barycentric', f'polyhedron v={v} #{i}', graphs.barycentric(rot))
    for args, every in ((['-p', '9'], 40), (['-p', '10'], 500), (['-p', '11'], 5000),
                        (['-p', '12', '0/64'], 1500), (['14'], 5000), (['16'], 200000),
                        (['-q', '18'], 2000), (['-q', '24', '0/256'], 4000)):
        for i, rot in plantri_maps(args, every):
            add('barycentric', f'plantri {" ".join(args)} #{i}', graphs.barycentric(rot))
    named = {'icosahedron': nx.icosahedral_graph(), 'dodecahedron': nx.dodecahedral_graph(),
             'octahedron': nx.octahedral_graph(), 'truncated tetrahedron': nx.truncated_tetrahedron_graph(),
             'truncated cube': nx.truncated_cube_graph()}
    for k in (3, 5, 7, 9, 12, 20, 40):
        named[f'prism over a {k}-gon'] = nx.circular_ladder_graph(k)
        named[f'wheel with {k} spokes'] = nx.wheel_graph(k + 1)
        anti = nx.Graph()
        for i in range(k):
            anti.add_edges_from([(i, (i + 1) % k), (k + i, k + (i + 1) % k), (i, k + i), (i, k + (i + 1) % k)])
        named[f'antiprism over a {k}-gon'] = anti
    for name, G in named.items():
        G = nx.convert_node_labels_to_integers(G)
        add('barycentric', name, graphs.barycentric(graphs.rotation_of_graph(G)))

    # separating triangles: stacked octahedra
    for d in list(range(1, 13)) + [16, 20, 30, 40, 60, 80, 120, 160, 240, 320]:
        add('stacked-chain', f'depth={d}', graphs.stacked_octahedra(d))
    for d in (1, 2, 3):
        add('stacked-all', f'depth={d}', graphs.stacked_octahedra(d, 'all'))

    # one very large face
    for k in (6, 8, 10, 12, 16, 20, 24, 32, 40, 50, 64, 80, 100, 128, 160, 200, 256):
        add('split-bipyramid', f'k={k}', graphs.split_bipyramid(k))

    # the trap chains, as stored
    for k in range(1, 11):
        F, t0, _ = graphs.trap_chain(k)
        add('trap-chain', f'k={k}', F, t0)

    # growth by random local substitutions
    for i, steps in enumerate([6, 8, 10, 12, 16, 20, 24, 32, 40, 50, 64, 80, 100, 128, 160, 200,
                               256, 320, 400, 500]):
        for rep in range(6):
            add('grow-split', f'steps={steps} seed={1000 * i + rep}', grow(steps, 0.0, 1000 * i + rep))
            add('grow-mixed', f'steps={steps} seed={1000 * i + rep}', grow(steps, 0.5, 50000 + 1000 * i + rep))

    # Goldberg-Coxeter images of the small triangulations with symmetry
    for v in range(8, 15):
        for i, rot in plantri_maps(['-b', str(v)]):
            F = graphs.faces_of_rotation(rot)
            c = symmetry.describe(F)
            if c['order'] >= 4 or i % 7 == 0:
                for k, l in ((2, 0), (1, 1), (2, 1), (3, 0), (2, 2), (3, 1), (4, 0), (5, 0), (4, 2)):
                    if (k * k + k * l + l * l) * len(F) <= 1300:
                        add('gc-small', f'plantri -b {v} #{i} ({c["type"]}) k={k} l={l}',
                            graphs.goldberg_coxeter(F, k, l))
    return out


def random_graphs(kind, V, count, chains, seed):
    """`count` triangulations with V vertices from `chains` independent runs
    of the Markov chain of fastbarnette.c (bx_mcmc).

    kind 0: all simple Eulerian triangulations, with vertex splits, insertion
    of octahedra and their inverses, at most V + 3 vertices; kind 1: those
    without separating triangle, with vertex splits and their inverses only,
    at most V + 2 vertices.  A chain starts at a small triangulation, runs
    10 * thin steps, and then yields a sample every thin = 50 V^2 steps at
    which it has V vertices.  Returns a list of (chain, index, F)."""
    out = []
    thin = 50 * V * V
    per_chain = -(-count // chains)
    for c in range(chains):
        if kind == 0:
            start, head = graphs.octahedron(), 3
        else:
            start, head = (graphs.bipyramid(2) if V % 2 == 0 else odd_start()), 2
        burn, _ = fb.mcmc(start, V, kind, 400 * thin, 10 * thin, 1, seed + 7919 * c, headroom=head, gamma=3.6)
        samples, _ = fb.mcmc(burn[0], V, kind, 400 * thin * per_chain, thin, per_chain,
                             seed + 7919 * c + 1, headroom=head, gamma=3.6)
        out += [(c, i, F) for i, F in enumerate(samples)]
    return out[:count]
