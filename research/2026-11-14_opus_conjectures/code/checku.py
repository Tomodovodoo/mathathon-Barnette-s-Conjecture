"""Locate an earlier agent's stored 2-factor u inside the exact lattice (bar.c -u)."""
import json, sys, subprocess
d = json.load(open(sys.argv[1]))
rot = {int(k): v for k, v in d['rot'].items()}
idx = {v: i for i, v in enumerate(sorted(rot))}
txt = subprocess.run(['python', 'rot2txt.py', sys.argv[1]], capture_output=True, text=True).stdout
with open('_u.txt', 'w') as f:
    for t, v in d['u']:
        f.write(' '.join(str(idx[x]) for x in t) + f' {idx[v]}\n')
out = subprocess.run(['./bar.exe', '-T', '-u', '_u.txt'], input=txt, capture_output=True, text=True).stdout
print(out.strip())
