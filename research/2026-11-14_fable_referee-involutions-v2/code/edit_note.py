from pathlib import Path
p = Path('proofs/involutions/involutions.tex'); s = p.read_text()
def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:60])
    s = s.replace(old, new)

# R1 definition paragraph of Section 5
rep(r"""The following version uses only the oriented sphere map, its face incidences,
and a fixed tree in the dual graph rooted at $t_0$. No coordinates, rays,
or general-position choices enter its definitions. For each white face $w$
let $w=f_0,f_1,\ldots,f_j=t_0$ be its tree path. At each bounded black
face $t=f_i$, the entering and leaving sides meet in a corner $v$.""",
r"""The following version uses only the oriented sphere map, its face incidences,
and a fixed tree in the dual graph rooted at $t_0$. No coordinates, rays,
or general-position choices enter its definitions. A side of a simple
cycle is inside when it does not contain $t_0$, and the cycle is
counterclockwise when its inside lies to its left; with this reading
Lemma~\ref{disk} and $J$ need no drawing. For each white face $w$
let $w=f_0,f_1,\ldots,f_j=t_0$ be its tree path. Its faces are distinct,
and only the last is $t_0$. At each black
face $t=f_i$ with $0<i<j$, the entering and leaving sides meet in a corner $v$.""")

# R2 statement of the lemma
rep(r"""\begin{lemma}\label{path-crossings}
These lists have the same parity, alternation, and first-exit sign rules
as the ray lists. With these lists and direction bits, both involutions,
the fixed-set formula, and the alternating constructor hold unchanged.
\end{lemma}""",
r"""\begin{lemma}\label{path-crossings}
Let $C$ be a spoke cycle of a pair and $w$ a white face.
\begin{enumerate}
\item The list of $C$ at $w$ has odd length exactly when $w$ is inside $C$.
\item At consecutive entries of the list, $C$ crosses the path in opposite
directions.
\item If $w$ is inside $C$, then at the first entry $C$ crosses the path
from right to left when $C$ is counterclockwise, and from left to right
when it is clockwise.
\end{enumerate}
Consequently Lemmas~\ref{one}, \ref{two}, \ref{fixed} and \ref{walk} and
the proof of Theorem~\ref{main} hold for path tokens, with these lists in
place of the ray lists and with the same number $F$.
\end{lemma}""")

# R3 proof, first paragraph
rep(r"""Subdivide every black triangle into its three corner sectors by its formal
centre-to-corner incidences. Passing through $t$ between two sides cuts off
exactly their common corner $v$. It crosses the incidence at $v$ once and
neither of the other two. Its local signed crossing with the incidence
directed away from the centre is $-\kappa_w(i)$. Reversing the incidence
changes this sign. This is a check of the two cyclic orders of the entering
and leaving sides, so it uses no lengths or angles.""",
r"""Subdivide every black triangle of $A$ into three sectors by its formal
centre-to-corner incidences. Each sector contains one side of the
triangle, and the sectors on two sides share the incidence at their
common corner. A step that enters $t$ by one side and leaves by another
therefore passes from one sector to the next. It crosses the incidence
at their common corner $v$ once and neither of the other two. If $v$ is
on the left of the step, the incidence directed away from the centre
points to the left, so it crosses the path from right to left. With left
to right counted positive, its signed crossing is $-\kappa_w(i)$.
Reversing the incidence changes this sign. This is a check of the two
cyclic orders of the entering and leaving sides, so it uses no lengths
or angles.""")

# R4 proof, second paragraph
rep(r"""Cut the subdivided sphere map along the simple incidence cycle $C$.
The two components are its inside disk and its outside disk. The face path
changes components exactly at the listed steps: in a triangle on $C$,
the route $r(t),t,s(t)$ separates precisely the corner sectors at $r(t)$
and $s(t)$ from each other, and the third turn crosses neither incidence.
Successive listed steps therefore alternate exit and entry. The path ends
in $t_0$ on the outside, so its list is odd exactly when $w$ is inside.""",
r"""The incidence cycle $C$ is simple, since its corners and its centres are
distinct. Cut the subdivided sphere map along it. The two components are
its inside disk and its outside disk. They contain the same white faces as
the two sides of the side cycle, because the two cycles differ only by
the sectors on the sides $r(t)s(t)$. The refined face path changes
components exactly when it crosses an incidence of $C$. In a triangle
$t$ on $C$ these are the incidences at $r(t)$ and $s(t)$, crossed by the
turns around $r(t)$ and $s(t)$; a turn around $u(t)$ crosses neither.
In white faces, in $t_0$ and in triangles off $C$ the path crosses no
incidence of $C$. So the path changes components exactly at the listed
steps, and successive listed steps alternate exit and entry. The path ends
in $t_0$ on the outside, so its list is odd exactly when $w$ is inside.""")

# R5 after the lemma: the tree, and the orientation
rep(r"""The marked-set size, first-fixed count, and path lengths depend on the
chosen tree of face paths, even though they require no drawing.""",
r"""The tree is a convenience. The proof uses only that each path is simple
and ends at $t_0$, so any fixed family of such paths serves, as in the
main paper. The marked-set size, first-fixed count, and path lengths depend on the
chosen paths, even though they require no drawing.""")
rep(r"""For this version $H(s)=-\sum_w\eta_s(w)=-\omega(s)$ exactly, with the
main paper's turn heights.""",
r"""For this version $H(s)=-\sum_w\eta_s(w)=-\omega(s)$ exactly, with the
main paper's turn heights for the same paths and the same orientation of the sphere.""")

# R6 Li: where the set convention is stated
rep(r"""Appendix B states the set convention, the rule for an unmarked cycle,""",
r"""Definition 14 states the set convention. Appendix B states the rule for an unmarked cycle,""")

# R7 verification paragraph
rep(r"""The code and raw outputs are in
\texttt{research/2026-11-14\_sol\_involutions-revision/}.""",
r"""The code and raw outputs are in
\texttt{research/2026-11-14\_sol\_involutions-revision/}.
A second referee's code, written from the text alone, reproduces every
count in this paragraph in the same encoding. It repeats all checks of
the face-path version with a depth-first tree, a random spanning tree,
and independent random simple paths that form no tree; see
\texttt{research/2026-11-14\_fable\_referee-involutions-v2/}.""")

# R8 the mirror image
rep(r"""The listing uses that geometry, not the manuscript's optimized disk layout.""",
r"""The listing uses that geometry, not the manuscript's optimized disk layout.
In it the stored triples of \texttt{running.json} run clockwise. The main
paper draws them counterclockwise, so our pictures of this example are
mirror images of the main paper's, and each turn sign $\kappa$ in
Figure~\ref{fig:paths} is the negative of the sign that the main paper's
height figure shows at the same turn. The signed sum is the same in
both orientations.""")
p.write_text(s, newline='\n')

q = Path('proofs/involutions/figures/panels.tex'); c = q.read_text()
def repc(old, new):
    global c
    assert c.count(old) == 1, old[:50]
    c = c.replace(old, new)
repc(r"""\caption{A computed marked pair in the running example. Left: the cover. Right: a zoom of its marked spokes. Dashed lines are the rays from $w_5$ and $w_6$, in the direction that is vertical in the exact layout. Thick spokes carry the tokens; blue arrows show $D$.}\end{figure}""",
r"""\caption{Object 1 of the table: pair 0 with the tokens $5{:}0$ and $6{:}7$. Left: the whole triangulation, with the cycle cover $D$ in blue. Right: the same picture enlarged. Thin grey segments are the ten selected spokes. Dashed lines are the rays from $w_5$ and $w_6$, in the direction that is vertical in the exact layout. Each black dot is a marked crossing of a ray with a thick spoke. Both tokens lie on the 7-cycle, so the triangle at the upper left is unmarked.}\label{fig:marked}\end{figure}""")
repc(r"""\caption{The second move on the same object, before and after, in the zoomed region. Both rays are drawn. The token moves to its partner crossing; its cycle reverses when the partner is an $r$-spoke.}\end{figure}""",
r"""\caption{The second map moves a token. Left: object 2 of the table, pair 0 with the tokens $5{:}0$ and $16{:}11$, black dots. The triangle carries $16{:}11$, so every cycle is marked. The point $w_5$ is outside the 7-cycle, and its ray meets that cycle twice, at the selected spokes of $t_0$ and $t_7$. Right: the image, object 6. The token has moved along the ray to the partner crossing, the hollow dot on the left. Both spokes belong to $s$, so no cycle is reversed. The two spokes cross the ray in opposite directions, and the sign changes from $-$ to $+$. On object 1 of Figure~\ref{fig:marked} the second map instead reverses the unmarked triangle and moves no token.}\label{fig:second}\end{figure}""")
repc(r"""the selected corner equals the turned corner at every marked step. Face IDs follow \texttt{running.json}.}\end{figure}""",
r"""the selected corner equals the turned corner at every marked step. Face IDs follow \texttt{running.json}. The signs are those of the note's layout, the mirror image of the main paper's drawing, where the same turns have $\kappa=-1$.}\label{fig:paths}\end{figure}""")
repc(r"""\caption{The first move on class 6, root 8, with 12 vertices. The second state and its token stay fixed while the opposite-edge cycle reverses. Blue arrows show $D$. This panel illustrates the state change.}\end{figure}""",
r"""\caption{The first map on class 6, root 8, with 12 vertices, where $m=1$. The second state and the token, the thick spoke of $t_0$ crossed by the ray of $w_3$, stay fixed. The first state changes on the faces of one cycle of $Q_s$, so the blue arrows of $D$ differ between the two panels.}\label{fig:first}\end{figure}""")
q.write_text(c, newline='\n')
