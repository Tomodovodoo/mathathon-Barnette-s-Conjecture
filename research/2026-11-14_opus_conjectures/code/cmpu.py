"""Compare the deleted-corner map u stored in an earlier agent's JSON with bar.c's two extremes."""
import json, sys, subprocess
d = json.load(open(sys.argv[1]))
rot = {int(k): v for k, v in d['rot'].items()}
idx = {v: i for i, v in enumerate(sorted(rot))}
txt = subprocess.run(['python', 'rot2txt.py', sys.argv[1]], capture_output=True, text=True).stdout
out = subprocess.run(['./bar.exe', '-T', '-U'], input=txt, capture_output=True, text=True).stdout
theirs = {frozenset(idx[x] for x in t): idx[v] for t, v in d['u']}
for line in out.splitlines():
    if line.startswith('UM'):
        tag, *items = line.split()
        mine = {}
        for it in items:
            a, b = it.split(':'); mine[frozenset(map(int, a.split(',')))] = int(b)
        diff = sum(1 for t in mine if mine[t] != theirs.get(t))
        print(tag, 'faces', len(mine), 'theirs', len(theirs), 'differ', diff)
    elif line.startswith('SUMMARY'):
        print(line)
