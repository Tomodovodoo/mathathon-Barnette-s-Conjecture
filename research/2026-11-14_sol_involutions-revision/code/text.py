from pathlib import Path
p=Path('proofs/involutions/involutions.tex');s=p.read_text()
section=r'''
\section{Marks without a drawing}\label{paths}
The following version uses only the oriented sphere map, its face incidences,
and a fixed tree in the dual graph rooted at $t_0$. No coordinates, rays,
or general-position choices enter its definitions. For each white face $w$
let $w=f_0,f_1,\ldots,f_j=t_0$ be its tree path. At each bounded black
face $t=f_i$, the entering and leaving sides meet in a corner $v$.
Set $\kappa_w(i)=1$ if this turn has $v$ on its left and $-1$ if
it has $v$ on its right, using the orientation of the sphere map.
This is the turn convention of the main paper, Section 4.
A token for $s$ is the incidence $(w,i)$ with $f_i\in A$ and $s(f_i)=v$.
Its direction bit is $d(w,i)=(1+\kappa_w(i))/2$.
Keep exactly $m$ distinct tokens and the same sign formula as before.
Since a tree path visits a face at most once, $(w,i)$ also determines its
black face; retaining the step makes the definition explicit.

For a spoke cycle $C$, its list at $w$ consists of the steps turning
around either $r(t)$ or $s(t)$ for $t$ on $C$, in increasing path order.
A spoke here means the formal incidence of a triangle with a corner.
Such incidences have their cyclic order from the sphere map.

\begin{lemma}\label{path-crossings}
These lists have the same parity, alternation, and first-exit sign rules
as the ray lists. With these lists and direction bits, both involutions,
the fixed-set formula, and the alternating constructor hold unchanged.
\end{lemma}
\begin{proof}
Subdivide every black triangle into its three corner sectors by its formal
centre-to-corner incidences. Passing through $t$ between two sides cuts off
exactly their common corner $v$. It crosses the incidence at $v$ once and
neither of the other two. Its local signed crossing with the incidence
directed away from the centre is $-\kappa_w(i)$. Reversing the incidence
changes this sign. This is a check of the two cyclic orders of the entering
and leaving sides, so it uses no lengths or angles.

Cut the subdivided sphere map along the simple incidence cycle $C$.
The two components are its inside disk and its outside disk. The face path
changes components exactly at the listed steps: in a triangle on $C$,
the route $r(t),t,s(t)$ separates precisely the corner sectors at $r(t)$
and $s(t)$ from each other, and the third turn crosses neither incidence.
Successive listed steps therefore alternate exit and entry. The path ends
in $t_0$ on the outside, so its list is odd exactly when $w$ is inside.
At a first exit, a counterclockwise cycle traverses the incidence from
right to left relative to the path, and a clockwise cycle from left to
right. These statements can also be read directly from the oriented
boundary of the inside disk. If the incidence is an $s$-incidence its
traversal is away from the centre; an $r$-incidence is traversed towards it.
Thus the direction bit above has exactly the convention of Definition~\ref{objects}.

The first map retains $s$, so it retains token eligibility and every bit.
In the second map an unmarked cycle can still be reversed without changing
any token. Otherwise minimality again forces one token on each of $m$
cycles. Pair consecutive list entries with the same index rules as before.
The common white face, the unoriented cycle, and the status of an entry
as first or nonfirst are unchanged by this pairing and any cycle reversal.
The partner lies on $r$ or $s$ exactly as before; reversal when it lies on
$r$ makes it eligible. Distinct cycles have distinct incidences, so no
other token is lost or duplicated. The return move makes the same reversal
decision. Alternating traversal signs give the same two sign-reversal
cases in Lemma~\ref{two}.

For each enclosed white face the odd list has a first entry. Exactly one
orientation of its cycle makes this an $s$-incidence. Independent choices
on distinct cycles give exactly the same product $F$. If $q$ cycles are
counterclockwise, the first-exit rule gives direction sum $q$ and
$J=m-2q$, so every fixed sign is $(-1)^{\lfloor m/2\rfloor}$.
The counting proof and the finite alternating-path proof now apply without
any further change.
\end{proof}

The marked-set size, first-fixed count, and path lengths depend on the
chosen tree of face paths, even though they require no drawing. The
minimum $m$, the enclosed-face counts, $F$, the common fixed sign and the
signed sum depend only on the rooted oriented triangulation. The identities
of fixed marked objects depend on the paths; their number does not.
For this version $H(s)=-\sum_w\eta_s(w)=-\omega(s)$ exactly, with the
main paper's turn heights. For rays the same cycle-reversal increments
hold; an additive constant may differ between unoriented-cover classes.
This is a term-by-term bijective unpacking of the height proof for this
particular height. The first involution is its cancellation lemma on
marked objects. The second proves its height and finite-difference
lemmas together by pairing the terms of the expansion.

The number of marks matters. With fewer than $m$ marks every object has
an unmarked cycle, so the signed count is zero. With more than $m$, the
one-token-per-cycle deduction fails and the second map is undefined on
some objects. COMPUTED for the original ray convention: with $m-1$ marks
the count is zero on all 880 paired roots through 14 vertices; with $m+1$
it is zero on 57 of them. Thus arbitrary mark counts cannot replace $m$.

'''
s=s.replace('\\section{An explicit constructor}',section+'\\section{An explicit constructor}')
s=s.replace('We complete the multi-mark argument in Appendix B',"We write out Li's intended multi-mark proof in Appendix B")
s=s.replace('The signed sum $-9$ and the nine second-fixed objects do not, by','The signed sum $-9$ and the second-fixed count of nine do not, by')
s=s.replace('from $103$ to $363$.','from $103$ to $363$, taking 35 values; path lengths range from zero to six moves.')
s=s.replace('$(0,0),(100,0),(0,100)$ in stored face order','$(0,0),(100,0),(0,100)$ for roots $0,5,4$, respectively, in stored face order')
s=s.replace('The longest ray path is two moves.','The longest ray path in those particular drawings is two moves.')
s=s.replace('Euler\'s disk formula is',"The closed disk with its triangulation is connected: its underlying space is a disk,\nand its triangles join along their edges and vertices. Its faces are exactly\nthe triangles counted above. Euler's disk formula is")
p.write_text(s)
