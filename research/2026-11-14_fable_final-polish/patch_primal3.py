"""Second follow-up to patch_primal.py: one-sentence relation paragraph and shorter wording, to keep 15 pages."""
from pathlib import Path

for name, path in [('PRIMAL-PROOF.md', 'paper/main/barnette.pdf'), ('primal.tex', r'\nolinkurl{paper/main/barnette.pdf}')]:
    f = Path('proofs/primal') / name
    s = f.read_bytes().decode('utf-8')
    for old, new in [
        ('This note accompanies the project\'s main paper (PATH in the same repository). '
         'It gives the same proof in the cubic graph $G$ itself, lemma by lemma, and the dictionary at the end translates the names. '
         'Two steps differ: Li\'s deficit argument gives the first pair (Lemma 4), and flow potentials with a polynomial (Lemmas 6 and 8) '
         'replace the main paper\'s heights and power of the weight.',
         'This note gives the proof of the project\'s main paper (PATH) in the cubic graph $G$ itself, lemma by lemma, '
         'with a dictionary at the end; two steps differ, since Li\'s deficit argument gives the first pair (Lemma 4) '
         'and flow potentials with a polynomial (Lemmas 6 and 8) replace the heights.'),
        ('The marked edges of a pair (the collection $D$ of Lemma 8) split into state circuits', 'The marked edges of a pair split into state circuits'),
        ('We say marked for the edges of $D$ and keep selected for the edges of the matching $P$ of Lemma 10.', 'Its edges are marked; selected is kept for the matching $P$.'),
    ]:
        old = old.replace('PATH', path)
        new = new.replace('PATH', path)
        assert s.count(old) == 1, (name, old[:50])
        s = s.replace(old, new)
    f.write_bytes(s.encode('utf-8'))
print('patched')
