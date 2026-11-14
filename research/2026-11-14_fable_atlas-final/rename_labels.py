"""One-shot rename of old names inside the atlas figure sources (strings and comments only).
Run once on 2026-11-14 from the repository root:  python research/2026-11-14_fable_atlas-final/rename_labels.py
The phrases contain a space, so identifiers such as is_tree_matching and CERT keys are untouched."""
import re
from pathlib import Path
A = Path('digestions/atlas')
SUB = [('tree matchings', 'good states'), ('tree matching', 'good state'), ('Tree matching', 'Good state'),
       ('tree pairs', 'good pairs'), ('tree pair', 'good pair'), ('forest state', 'good state'), ('forest pair', 'good pair')]
for f in ['figs_chain.py', 'figs_algebra.py', 'figs_order.py', 'figs_scope.py', 'lib.py']:
    t = (A / f).read_text(encoding='utf8')
    n = {}
    for a, b in SUB:
        n[a] = t.count(a)
        t = t.replace(a, b)
    (A / f).write_text(t, encoding='utf8', newline='\n')
    print(f, {k: v for k, v in n.items() if v})
