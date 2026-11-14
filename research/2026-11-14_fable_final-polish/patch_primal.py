"""One-off naming patch for proofs/primal (14 November 2026). Run once from the repository root.

The edges of D are "marked"; "selected" is kept for the matching P. The dictionary column for T
uses the main paper's names. One paragraph relates the note to the main paper. EXAMPLES.md and
the finite-range section of STATUS.md are labelled as the first version's worked example.
primal.tex and PRIMAL-PROOF.md receive the same edits by hand; the generator in
research/2026-11-14_astra_primal-revision/ was not rerun. No statement or proof step changes.
"""
from pathlib import Path

D = Path('proofs/primal')


def patch(name, pairs):
    f = D / name
    raw = f.read_bytes().decode('utf-8')
    crlf = '\r\n' in raw
    s = raw.replace('\r\n', '\n')
    for old, new in pairs:
        assert s.count(old) == 1, (name, s.count(old), old[:70])
        s = s.replace(old, new)
    f.write_bytes((s.replace('\n', '\r\n') if crlf else s).encode('utf-8'))


RELATION = ('This note is a companion to the project\'s main paper, The proof of Barnette\'s conjecture: an exposition '
            '(paper/main/barnette.pdf in the same repository). It gives the same proof in the cubic graph $G$ itself, lemma by lemma, '
            'and the dictionary at the end translates each object into the main paper\'s names. '
            'Two steps are carried out differently. The first pair comes from Li\'s deficit argument (Lemma 4). '
            'The weights are potentials of a flow, tested with a polynomial (Lemmas 6 and 8), '
            'where the main paper uses heights along paths of faces and a power of the weight.')

common = [
    ('The selected edges of a pair split into state circuits', 'The marked edges of a pair (the collection $D$ of Lemma 8) split into state circuits'),
    ('Proof. A pair selects at each black vertex the edge whose incident faces are $r(b)$ and $s(b)$, directed from the former to the latter. Call this collection $D$.',
     'Proof. A pair marks at each black vertex the edge whose incident faces are $r(b)$ and $s(b)$, directed from the former to the latter. Call this collection $D$. We say marked for the edges of $D$ and keep selected for the edges of the matching $P$ of Lemma 10.'),
    ('has exactly one black endpoint and is selected at most once.', 'has exactly one black endpoint and is marked at most once.'),
    ('each black vertex labels exactly one selected edge.', 'each black vertex labels exactly one marked edge.'),
]

patch('PRIMAL-PROOF.md', common + [
    ('\n## 1. The target and the objects\n', '\n' + RELATION + '\n\n## 1. The target and the objects\n'),
])
patch('primal.tex', common + [
    ('\n\\section*{1. The target and the objects}\n', '\n' + RELATION.replace('paper/main/barnette.pdf', r'\nolinkurl{paper/main/barnette.pdf}') + '\n\n\\section*{1. The target and the objects}\n'),
    (r'Object in G & Object in T & OpenAI & Li & Constructive paper & Lean declaration\\\midrule',
     r'Object in G & Main paper, in T & OpenAI & Li & Constructive paper & Lean declaration\\\midrule'),
    (r'Incidences A to X & Black triangles to nonroot corners & State &', r'Incidences A to X & State: a corner in each black triangle & State &'),
    (r'Two disjoint states & Two disjoint corner choices & Pair (r,s) &', r'Two disjoint states & Pair (r,s), different in every triangle & Pair (r,s) &'),
    (r'Edge not on s(b), as face link & Side opposite s(t) & Q\_s &', r'Edge not on s(b), as face link & Opposite side, in Q\_s & Q\_s &'),
    (r'Directed selected face links & Directed edges r(t) to s(t) & D(r,s) &', r'Directed marked face links; undirected D & D(r,s); its cover & D(r,s); group &'),
    (r'Forest Q\_s with a partner & One root per Q component & Forest pair &', r'Forest Q\_s with a partner & Good state; good pair & Forest pair &'),
    (r'Compatible perfect matching P & Selected primal-dual edge set & One selected edge per face &', r'Compatible perfect matching P & Selection P, one side of every face & One selected edge per face &'),
    (r'Hamiltonian cycle G-P & Boundary of two induced trees & Tree partition &', r'Hamiltonian cycle G-P & Acyclic selection; two induced trees & Tree partition &'),
])
patch('DICTIONARY.md', [
    ('| Object in G | Object in T | OpenAI | Li | Constructive paper | Lean declaration |', '| Object in G | Main paper, in T | OpenAI | Li | Constructive paper | Lean declaration |'),
    ('| Incidences A to X | Black triangles to nonroot corners | State |', '| Incidences A to X | State: a corner in each black triangle | State |'),
    ('| Two disjoint states | Two disjoint corner choices | Pair (r,s) |', '| Two disjoint states | Pair (r,s), different in every triangle | Pair (r,s) |'),
    ('| Edge not on s(b), as face link | Side opposite s(t) | Q_s |', '| Edge not on s(b), as face link | Opposite side, in Q_s | Q_s |'),
    ('| Directed selected face links | Directed edges r(t) to s(t) | D(r,s) |', '| Directed marked face links; undirected D | D(r,s); its cover | D(r,s); group |'),
    ('| Forest Q_s with a partner | One root per Q component | Forest pair |', '| Forest Q_s with a partner | Good state; good pair | Forest pair |'),
    ('| Compatible perfect matching P | Selected primal-dual edge set | One selected edge per face |', '| Compatible perfect matching P | Selection P, one side of every face | One selected edge per face |'),
    ('| Hamiltonian cycle G-P | Boundary of two induced trees | Tree partition |', '| Hamiltonian cycle G-P | Acyclic selection; two induced trees | Tree partition |'),
    ('\nPROVED-HERE. With aligned corner signs', '\nThe second column uses the names of the project\'s main paper, paper/main/barnette.pdf: state, pair, opposite sides Q_s, cover (the undirected D), good state, good pair (a pair whose second state is good), selection. In this note the edges of D are marked, and selected refers only to the matching P.\n\nPROVED-HERE. With aligned corner signs'),
])
patch('EXAMPLES.md', [
    ('## 11. Two exact worked examples\n', '## 11. Two exact worked examples\n\nThese are the worked examples of the first version of this note: the cube and a 20-vertex graph. The current PDF illustrates the proof on a different running example, the 22-vertex graph of paper/figures/running.json, which is also the main paper\'s example. Nothing below describes that graph.\n'),
    ('### A 20-vertex cancellation example', '### A 20-vertex cancellation example (first version\'s worked example)'),
])
patch('STATUS.md', [
    ('## Exact finite range\n', '## Exact finite range (first version\'s checker and worked example)\n'),
])
print('patched')
