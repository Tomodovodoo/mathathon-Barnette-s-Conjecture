"""One-off naming patch for proofs/involutions (14 November 2026). Run once from the repository root.

"forest pair" becomes "good pair" (older name mentioned once), the cover and m are named as in
the main paper, and the sign of H against the main paper's weight is stated where H appears.
No statement or proof step changes.
"""
from pathlib import Path

D = Path('proofs/involutions')


def patch(name, pairs, everywhere=()):
    f = D / name
    raw = f.read_bytes().decode('utf-8')
    crlf = '\r\n' in raw
    s = raw.replace('\r\n', '\n')
    for old, new in pairs:
        assert s.count(old) == 1, (name, s.count(old), old[:60])
        s = s.replace(old, new)
    for old, new in everywhere:
        s = s.replace(old, new)
    f.write_bytes((s.replace('\n', '\r\n') if crlf else s).encode('utf-8'))


patch('involutions.tex', [
    (r'\title{Two involutions for the forest-pair lemma}', r'\title{Two involutions for the good-pair lemma}'),
    ('path constructs a forest pair. The coefficient', 'path constructs a good pair. The coefficient'),
    (r'''\begin{theorem}[Forest-pair lemma]\label{main}
If a pair exists, a pair exists for which $Q_s$ is a forest.
\end{theorem}
''', r'''\begin{theorem}[Good-pair lemma]\label{main}
If a pair exists, a pair exists for which $Q_s$ is a forest.
\end{theorem}

We call a pair $(r,s)$ for which $Q_s$ is a forest a \emph{good pair}.
Earlier versions of this note said forest pair.
Its second state is a good state in the sense of the main paper, by Lemma~4.2 there.

This note accompanies the project's main paper, \emph{The proof of
Barnette's conjecture: an exposition}, in the same repository.
Through that Lemma~4.2, Theorem~\ref{main} is its Proposition~4.8. The proof
here is Li's intended proof written out in full, and in the form of
Section~\ref{paths} it is a term-by-term unpacking of the main paper's
Lemmas~4.5 to~4.7 for one particular height.
'''),
    (r'''cycle cover $D_p$ of $X$. There are no repeated undirected edges, since each
edge has exactly one black face.''', r'''cycle cover $D_p$ of $X$. There are no repeated undirected edges, since each
edge has exactly one black face. As in the main paper, the undirected edge
set of $D_p$ is the \emph{cover} of $p$.'''),
    (r'''cycles. If $c(p)$ counts cycles then $J(p)\equiv c(p)\equiv n\pmod2$.
Let $m=\min_p c(p)$. Thus $m\ge1$.''', r'''cycles. If $c(p)$ counts cycles then $J(p)\equiv c(p)\equiv n\pmod2$.
Let $m=\min_p c(p)$. Thus $m\ge1$. This is the $m$ of the main paper, and a
cover with $m$ cycles is a minimum cover.'''),
    (r'''For this version $H(s)=-\sum_w\eta_s(w)=-\omega(s)$ exactly, with the
main paper's turn heights for the same paths and the same orientation of the sphere.''',
     r'''Let $H(s)$ be the signed number of tokens of $s$, a token counting $+1$
when $\kappa_w(i)=-1$ and $-1$ when $\kappa_w(i)=1$; Section~\ref{compare}
defines the same quantity for rays.
For this version $H(s)=-\sum_w\eta_s(w)=-\omega(s)$ exactly, with the
main paper's turn heights for the same paths and the same orientation of the sphere.
So $H$ has the opposite sign to the main paper's weight $\omega$.'''),
    (r'\section{Relations and computational checks}', r'\section{Relations and computational checks}\label{compare}'),
    ('This procedure terminates at a forest pair without repeating an object.', 'This procedure terminates at a good pair without repeating an object.'),
    (r'''For comparison only, put $H(s)$ equal to the sum, over all white rays,
of the signed crossings with the selected spokes, left-to-right positive.''',
     r'''For comparison only, put $H(s)$ equal to the sum, over all white rays,
of the signed crossings with the selected spokes, left-to-right positive.
This $H$ has the opposite sign to the weight $\omega$ of the main paper.'''),
])

patch('INVOLUTIONS.md', [
    ('a pair exists whose opposite-edge graph is a forest. The complete',
     'a pair exists whose opposite-edge graph is a forest. Such a pair is a good pair (a forest pair in earlier versions), and its second state is a good state of the main paper, paper/main/barnette.pdf. The theorem is that paper\'s Proposition 4.8, and the proof is Li\'s intended proof written out in full, a term-by-term unpacking of its Lemmas 4.5 to 4.7 for one particular height. The complete'),
    ('For face-path tokens H=-omega exactly, for the same paths and the same orientation of the sphere.',
     'For face-path tokens H=-omega exactly, for the same paths and the same orientation of the sphere, so H has the opposite sign to the main paper\'s weight omega.'),
], everywhere=[('forest-pair', 'good-pair'), ('forest pair', 'good pair'), ('(a good pair in earlier versions)', '(a forest pair in earlier versions)')])

patch('STATUS.md', [
    ('| Theorem 1, forest pair from pair existence |', '| Theorem 1, good pair (earlier name: forest pair) from pair existence |'),
], everywhere=[('forest-pair', 'good-pair')])

patch('README.md', [
    ('# Forest pairs by two involutions', '# Good pairs by two involutions'),
], everywhere=[('forest-pair', 'good-pair')])
print('patched')
