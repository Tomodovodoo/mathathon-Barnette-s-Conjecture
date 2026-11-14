"""Third follow-up: move the lead-in to the figures from before the dictionary page to after it.

Before this move the three-line paragraph sat alone on page 11 of primal.pdf.
"""
from pathlib import Path

f = Path('proofs/primal/primal.tex')
s = f.read_bytes().decode('utf-8')
nl = '\r\n' if '\r\n' in s else '\n'
para = ('The exact cube and 20-vertex worked-example data remain in EXAMPLES.md. The illustrated running example below '
        'instead uses the current 13-face example, whose primal graph has 22 vertices.')
assert s.count(para) == 1
i = s.index(para)
j = s.index('\\clearpage\\section*{Primal-dual dictionary}')
assert s[i + len(para):j].strip() == ''
s = s[:i].rstrip() + nl + s[j:]
anchor = 'The recovery tree here lies in G, whereas the sources also use a tree on white faces.'
assert s.count(anchor) == 1
s = s.replace(anchor, anchor + nl + nl + para.replace('The illustrated running example below instead uses',
                                                    'The figures on the following pages instead use'))
f.write_bytes(s.encode('utf-8'))
print('patched')
