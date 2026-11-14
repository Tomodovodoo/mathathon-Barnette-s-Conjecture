"""Style and link audit of digestions/steps/*.md (unslop word list, dashes, curly quotes, links)."""
import glob
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
BAD = ['crucial', 'delve', 'pivotal', 'landscape', 'underscore', 'testament', 'intricate', 'interplay', 'showcase',
       'vibrant', 'leverage', 'utilize', 'serves as', 'stands as', 'not just', 'in order to', 'it is important',
       'additionally', 'enhance', 'foster', 'garner', 'seamless', 'substrate', 'scaffold', 'paradigm', 'nexus',
       'groundbreaking', 'stunning', 'renowned']
for f in sorted(glob.glob(os.path.join(ROOT, 'digestions', 'steps', '*.md'))):
    t = open(f, encoding='utf-8').read()
    low = t.lower()
    hits = [b for b in BAD if b in low]
    dashes = [c for c in '—–' if c in t]
    curly = [c for c in '“”‘’' if c in t]
    missing = []
    for m in re.finditer(r'\]\(([^)]+)\)', t):
        tgt = m.group(1)
        if tgt.startswith('http'):
            continue
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), tgt))):
            missing.append(tgt)
    paths = []
    for m in re.finditer(r'`((?:research|paper|papers|workings)/[^`]+)`', t):
        p = m.group(1).split(' ')[0]
        if not os.path.exists(os.path.join(ROOT, p)):
            paths.append(p)
    colons = [l.strip()[:120] for l in t.splitlines()
              if re.search(r'[a-z]: [a-z]', l) and not l.strip().startswith('|')]
    print(os.path.basename(f), 'words', len(t.split()), 'banned', hits, 'dashes', dashes, 'curly', curly,
          'missing links', missing, 'missing paths', paths)
    for c in colons:
        print('     colon:', c)
