"""Convert a JSON file with 'rot' (ccw rotation dict) and 't0' into bar.c -T text format."""
import json, sys
d = json.load(open(sys.argv[1]))
rot = {int(k): v for k, v in d['rot'].items()}
idx = {v: i for i, v in enumerate(sorted(rot))}
parts = [str(len(rot))]
for v in sorted(rot):
    parts.append(str(len(rot[v]))); parts += [str(idx[w]) for w in rot[v]]
t0 = d['t0'] if not isinstance(d['t0'], str) else json.loads(d['t0'])
parts += [str(idx[x]) for x in t0]
print(' '.join(parts))
