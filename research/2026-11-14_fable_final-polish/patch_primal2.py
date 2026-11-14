"""Follow-up to patch_primal.py: shorten the relation paragraph so that the PDF keeps 15 pages."""
from pathlib import Path

OLD = ('This note is a companion to the project\'s main paper, The proof of Barnette\'s conjecture: an exposition '
       '(PATH in the same repository). It gives the same proof in the cubic graph $G$ itself, lemma by lemma, '
       'and the dictionary at the end translates each object into the main paper\'s names. '
       'Two steps are carried out differently. The first pair comes from Li\'s deficit argument (Lemma 4). '
       'The weights are potentials of a flow, tested with a polynomial (Lemmas 6 and 8), '
       'where the main paper uses heights along paths of faces and a power of the weight.')
NEW = ('This note accompanies the project\'s main paper (PATH in the same repository). '
       'It gives the same proof in the cubic graph $G$ itself, lemma by lemma, and the dictionary at the end translates the names. '
       'Two steps differ: Li\'s deficit argument gives the first pair (Lemma 4), and flow potentials with a polynomial (Lemmas 6 and 8) '
       'replace the main paper\'s heights and power of the weight.')
for name, path in [('PRIMAL-PROOF.md', 'paper/main/barnette.pdf'), ('primal.tex', r'\nolinkurl{paper/main/barnette.pdf}')]:
    f = Path('proofs/primal') / name
    raw = f.read_bytes().decode('utf-8')
    old, new = OLD.replace('PATH', path), NEW.replace('PATH', path)
    assert raw.count(old) == 1, name
    f.write_bytes(raw.replace(old, new).encode('utf-8'))
print('patched')
