"""Check that every OLD block of EDITS.md occurs exactly once in the draft source.

Run from the repository root:
    python research/2026-11-14_fable_review-draft-B/verify_edits.py > research/2026-11-14_fable_review-draft-B/verify_edits.txt
"""
import re

here = 'research/2026-11-14_fable_review-draft-B/'
tex = open('paper/draft-B/barnette.tex', encoding='utf-8').read()
md = open(here + 'EDITS.md', encoding='utf-8').read()
section = '?'
bad = 0
lines = md.split('\n')
i = 0
while i < len(lines):
    line = lines[i]
    m = re.match(r'## (\d+)\.', line)
    if m:
        section = m.group(1)
    m = re.match(r'\*\*(\d+[a-z])\.\*\*', line)
    if m:
        section = m.group(1)
    if 'OLD' in line.split('(')[0].split() and i + 1 < len(lines) and lines[i + 1].startswith('```'):
        j = i + 2
        block = []
        while not lines[j].startswith('```'):
            block.append(lines[j])
            j += 1
        text = '\n'.join(block)
        n = tex.count(text)
        print(f'edit {section}: OLD block of {len(block)} line(s) occurs {n} time(s)')
        bad += n != 1
        i = j
    i += 1
print('all OLD blocks occur exactly once' if not bad else f'{bad} block(s) do not occur exactly once')
