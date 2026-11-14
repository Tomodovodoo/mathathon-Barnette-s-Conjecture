"""Search every 4-connected Eulerian triangulation on 8..14 vertices (plantri -bc4)
and every face t0 for a running example that both draws well and shows the proof.
Wanted: a cyclic Q_s (so cancellation is visible), a forest pair, a D-cycle with a
strictly interior vertex, and small degrees at the roots and at the three apexes of
the faces across the outer edges.
Run: python research/2026-11-14_fable_figures-review/search_example.py [nmax]
Writes search_example.json (all candidates with a cyclic pair and an interior D-cycle).
"""
import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'paper' / 'figures'))
from model import Model
PLANTRI = ROOT / 'workings' / 'barnette_lab' / 'vendor' / 'plantri.exe'

def faces_from_ascii(line):
    n, rest = line.split()
    rot = [[ord(c) - 97 for c in s] for s in rest.split(',')]
    seen, faces = set(), []
    for u in range(len(rot)):
        for v in rot[u]:
            if (u, v) in seen: continue
            f, a, b = [], u, v
            while (a, b) not in seen:
                seen.add((a, b)); f.append(a)
                nb = rot[b]; c = nb[(nb.index(a) + 1) % len(nb)]
                a, b = b, c
            faces.append(tuple(f))
    assert all(len(f) == 3 for f in faces)
    return faces

nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 14
rows = []
for n in range(8, nmax + 1):
    out = subprocess.run([str(PLANTRI), '-bc4', '-a', str(n)], capture_output=True, text=True).stdout.split('\n')
    tris = [faces_from_ascii(l) for l in out if l.strip()]
    print(n, len(tris), 'triangulations', flush=True)
    for k, F in enumerate(tris):
        for t0 in range(len(F)):
            m = Model(F, t0)
            st = m.states(); ps = m.pairs(st)
            cyc = [(r, s) for r, s in ps if not m.Q_is_forest(s)]
            if not cyc or len(cyc) == len(ps): continue
            dI = 0
            for r, s in ps:
                for c in m.directed_cycles(m.D(r, s)):
                    if m.disk(c)['I'] >= 1: dI += 1
            if not dI: continue
            deg = dict(m.T.degree())
            apex = [m.third(m.left[b, a] if m.left[a, b] == t0 else m.left[a, b], a, b) for a, b in
                    zip(m.roots, m.roots[1:] + m.roots[:1])]
            rows.append(dict(n=n, index=k, t0=t0, faces=F, maxdeg=max(deg.values()), rootdeg=sorted(deg[v] for v in m.roots),
                             apexdeg=sorted(deg[v] for v in apex), states=len(st), pairs=len(ps), cyclic=len(cyc), D_I=dI))
            r = rows[-1]; print({k: v for k, v in r.items() if k != 'faces'}, flush=True)
(Path(__file__).parent / 'search_example.json').write_text(json.dumps(rows))
