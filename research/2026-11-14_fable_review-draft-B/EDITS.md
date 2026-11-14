# Proposed edits to `paper/draft-B/barnette.tex`

25 edits, ordered by value. I did not touch the draft. Each `OLD` block is copied from the source as committed at `804b7ab` and occurs exactly once there; `verify_edits.py` checks this (output at the end of this file). `NEW` is the replacement. Where an edit is a move or a figure request it says "instruction". References: R = `REFEREE.md`, X = `EXPOSITION-REVIEW.md`, CR = `COLD-READ.md`.

New mathematics in these edits (Lemma D in edit 1, the face-path heights in edit 5, the product sign mentioned in edit 5's note) is `PROVED-HERE` in `REFEREE.md`. It has had no human check, so an editor should read those proofs before accepting the text.

---

## 1. Close the Euler gap with one lemma (R G1)

**1a.** Add connectedness to the standing definition and prove it.

OLD
```
From now on $\T$ is a \emph{coloured triangulation}: a simple graph with at least four vertices, embedded in the sphere with every face a triangle, and with a black and white colouring of its faces such that every edge has one face of each colour.
```
NEW
```
From now on $\T$ is a \emph{coloured triangulation}: a simple graph with at least four vertices, embedded in the sphere with every face bounded by a triangle, and with a black and white colouring of its faces such that every edge has one face of each colour.
Such a graph is connected, by the following lemma, which we use again for the inside of a cycle (Lemma~\ref{lem:disk}) and for the pieces of Section~\ref{sec:glue}.

\begin{lemma}\label{lem:connected}
Let $R$ be a finite graph embedded in the sphere such that every face of $R$ is bounded by a cycle of $R$.
Then $R$ is connected.
\end{lemma}

\begin{proof}
Let $K$ be a component of $R$.
The boundary of a face is a cycle, so it lies in one component.
Let $\Omega$ be the union of $K$ and the faces whose boundary lies in $K$, and $\Omega'$ the union of the other components and the other faces.
A point of $K$ has a neighbourhood that meets only $K$ and faces with that point on their boundary, and these faces have their boundary in $K$.
So $\Omega$ is open, and $\Omega'$ is open for the same reason.
They are disjoint and cover the sphere, which is connected, and $\Omega$ is not empty.
Hence $\Omega'$ is empty.
\end{proof}

```

**1b.** Check the hypothesis where Euler's formula is used.

OLD
```
The first is Euler's formula for the plane graph formed by $Z$ and everything inside it, which has $I+h$ vertices, $B+W+1$ faces and $(3(B+W)+h)/2$ edges, since each inner face has three sides and only the edges of $Z$ lie on a single inner face.
```
NEW
```
The first is Euler's formula for the plane graph $R_Z$ formed by $Z$ and the vertices and edges of $\T$ inside it.
The outside of $Z$ is an open disk that contains no point of $R_Z$, so it is one face of $R_Z$, bounded by $Z$.
Every other face of $R_Z$ lies inside $Z$ and contains no vertex or edge of $\T$, so it is a face of $\T$, bounded by a triangle.
So $R_Z$ has $B+W+1$ faces, each bounded by a cycle, and it is connected by Lemma~\ref{lem:connected}.
It has $I+h$ vertices and $(3(B+W)+h)/2$ edges, since each inner face has three sides, an edge strictly inside lies on two inner faces, and an edge of $Z$ lies on one.
```

**1c.** Say that a piece is connected.

OLD
```
The piece is a triangulation of the sphere whose graph is a subgraph of $\T$, hence simple; it has a vertex strictly inside $\mathsf{D}$, so at least four vertices, and it misses the vertices strictly on the other side.
```
NEW
```
Every face of the piece is bounded by a triangle, and its graph is a subgraph of $\T$, hence simple.
It has a vertex strictly inside $\mathsf{D}$, so at least four vertices, and it misses the vertices strictly on the other side.
```

## 2. Split Figure 3 and put each panel where it is used (X (e) finding 2, CR 24)

Instruction. Cut the single `figure` environment with `\label{fig:local}` into three.
- Panel (a) stays where it is, with caption: `One black triangle $t$ with the corner $s(t)$ chosen by a state (solid wedge). A selection built from $s$ uses one of the two bold sides at $s(t)$. The dashed side opposite $s(t)$ is the edge of $Q_s$ in $t$.`
- Panel (b) moves to directly after Definition 4.1 (`A \emph{pair} is an ordered pair ...`), with caption: `A pair in one black triangle. The outlined wedge is $r(t)$, the solid wedge $s(t)$. The arrow $r(t)\to s(t)$ is the edge of $\Dc(r,s)$ in $t$. The dashed arrow from $r(t)$ to the third corner $u(t)$ is the edge of $Q_s$, directed as in Lemma~\ref{lem:partner}.`
- Panel (c) moves to directly before Lemma 4.6, or is dropped if edit 5 is accepted. If kept, rename the white face in it from `$y$` to the letter used for white faces in Section 4 (see edit 9), and the vertices `$v$`, `$w$` to `$s(t)$`, `$r(t)$`, which is how Lemma 4.6 uses it.

## 3. Keep Section 3's figures in Section 3 (X (e) findings 3 and 7, CR 46, 47)

**3a.** OLD
```
\usepackage{booktabs}
```
NEW
```
\usepackage{booktabs}
\usepackage{placeins}
```

**3b.** OLD
```
\section{Pairs of states}\label{sec:pairs}
```
NEW
```
\FloatBarrier
\section{Pairs of states}\label{sec:pairs}
```

**3c.** New caption for Figure 7, without process talk and with the point of each panel first.

OLD
```
\caption{The same selection $P_s$ (bold) in the shared figure style. (a) The dash-dotted tree is $Y_s$ with its black nodes suppressed, a tree on the white faces rooted at the ringed face $y_0$ across $e_0$; each white face other than $y_0$ selects the side towards its parent. (b) The curve crossing every edge not in $P_s$ once is the Hamiltonian cycle of $G$ through all 22 faces. Its two sides hold the two components of $P_s$ (disks and squares), which are induced trees.}
```
NEW
```
\caption{The selection $P_s$ of Figure~\ref{fig:recover} (bold) and the Hamiltonian cycle it gives. (a) Each white face other than $y_0$ (ringed) selects the side towards its parent in $Y_s$; here $Y_s$ is drawn with its black nodes suppressed. (b) The curve that crosses every edge not in $P_s$ once is the Hamiltonian cycle of $G$ through all 22 faces. The two components of $P_s$ (disks and squares) lie on its two sides.}
```

Instruction. Also change every `\begin{figure}[t]` to `\begin{figure}[tb]`, so that a figure may follow its first reference on the same page. If only one panel of Figure 7 can be kept, keep (b) and cite it after Proposition 2.5, where the paragraph now points five pages ahead.

## 4. A figure for the heights (X (e) finding 1, CR 57)

Instruction. Add one figure at the definition of `h_s`, two panels on the running example.
- (a) One white face inside the 7-cycle, for instance the face `{1,8,9}`, its path to `t0`, the chosen corners of the state `s` of Figure 8 on the black faces the path passes through, and at each such face the value `+1`, `−1` or `0` of `κ`.
- (b) The same after reversing the 7-cycle, with the height one larger.
Caption: say which face, list the terms of the two sums, and state the two heights. This is the picture I looked for at CR 57 and did not find.

## 5. Heights by paths of faces: no spokes, no winding numbers (R S1)

This replaces the definition of heights and the proof of Lemma 4.6. It removes the general-position conditions, the polygonal paths and the winding-number fact, and it makes edits 6 and 7 unnecessary. `PROVED-HERE` in R S1; `COMPUTED` in `check_face_paths.py`. If the editor prefers to keep spokes, skip this edit and apply 6 and 7.

**5a.** OLD
```
We measure, for each white face, how often the chosen corners of $s$ wind around it.

Place a point $c_t$ inside each face $t\in A$ and call the segments from $c_t$ to the corners of $t$ \emph{spokes}; we draw the corner $(t,v)$ as the spoke $c_t v$, directed from $c_t$ to $v$.
For each white face $w$ fix a point $p_w$ inside $w$ and a polygonal path $\gamma_w$ from $p_w$ to a point $q$ in the outer face that avoids the vertices of $\T$ and the points $c_t$ and crosses spokes transversally.
For a spoke $c_t v$ let $\kappa_w(t,v)$ be the number of times it crosses $\gamma_w$ from the right of $\gamma_w$ to its left, minus the number of crossings in the other direction.
The \emph{height} of a state $s$ at $w$ and its \emph{weight} are
```
NEW
```
For each white face $y$ we walk from $y$ to the outer face and record, at every black face on the way, whether the walk passes the chosen corner.

For each white face $y$ fix a path of faces $y=f_0,f_1,\dots,f_k=t_0$ in $G$: consecutive faces share a side, and no face is repeated.
A black face $t\in A$ on the path is entered across one of its sides and left across another.
These two sides meet in one corner $v$ of $t$, and we say that the path \emph{turns around} $v$ in $t$.
Put $\kappa_y(t,v)=1$ if the path turns around $v$ in $t$ with $v$ on its left, $\kappa_y(t,v)=-1$ if it turns around $v$ with $v$ on its right, and $\kappa_y(t,v)=0$ if the path misses $t$ or turns around another corner of $t$.
The \emph{height} of a state $s$ at $y$ and its \emph{weight} are
```

**5b.** OLD
```
h_s(w)=\sum_{t\in A}\kappa_w\bigl(t,s(t)\bigr),\qquad \omega(s)=\sum_{w\ \text{white}}h_s(w).
\]
Changing the paths adds to each $h_s(w)$ a constant that does not depend on $s$; nothing below depends on the choice.
```
NEW
```
\eta_s(y)=\sum_{t\in A}\kappa_y\bigl(t,s(t)\bigr),\qquad \omega(s)=\sum_{y\ \text{white}}\eta_s(y).
\]
The paths are fixed once and for all.
```

**5c.** OLD
```
Then $h_{s'}(w)-h_s(w)$ is $1$ if $w$ lies inside $C$ and $0$ otherwise.
```
NEW
```
Then $\eta_{s'}(y)-\eta_s(y)$ is $1$ if the white face $y$ lies inside $C$ and $0$ otherwise.
```

**5d.** OLD
```
So $h_{s'}(w)-h_s(w)=\sum_{t}\bigl(\kappa_w(t,r(t))-\kappa_w(t,s(t))\bigr)$ over the faces $t$ supplying $C$.
This is the signed number of crossings of $\gamma_w$ with the closed curve $\Gamma$ obtained from the counterclockwise cycle $C$ by replacing each edge $s(t)\to r(t)$ with the route $s(t)\to c_t\to r(t)$; the first spoke is traversed backwards, which accounts for the minus sign.
For a closed polygonal curve $\Gamma$ and a path from $p$ to $q$ in general position, the signed number of crossings, counted as above, is the winding number of $\Gamma$ around $p$ minus its winding number around $q$; the winding number changes by one each time the path crosses $\Gamma$.
Each edge of $C$ and its route lie in one closed black triangle and have the same ends (Figure~\ref{fig:local}(c)), so $\Gamma$ can be deformed into $C$ inside these triangles.
The triangles contain neither $p_w$, which lies in a white face, nor $q$, which lies in the outer face.
So $\Gamma$ and $C$ have the same winding numbers around $p_w$ and $q$.
As $C$ is a counterclockwise simple closed curve, these are $1$ or $0$ around $p_w$ according as $w$ is inside $C$ or not, and $0$ around $q$, which lies in the outer face.
Finally $L(C)\ge1$ by the disk identity.
```
NEW
```
So $\eta_{s'}(y)-\eta_s(y)=\sum_{t}\bigl(\kappa_y(t,r(t))-\kappa_y(t,s(t))\bigr)$ over the faces $t$ supplying $C$.
Fix such a face $t$ and let $g$ be its side on $C$, which joins $s(t)$ and $r(t)$.
If the path of $y$ misses $t$ or turns around $u(t)$ in $t$, then it does not cross $g$ on its way through $t$, and the summand of $t$ is $0$.
Otherwise it crosses $g$ once on its way through $t$, and we claim that the summand is $+1$ if this crossing leads from the left of $s(t)\to r(t)$ to its right, and $-1$ if it leads from right to left.
Suppose the crossing leads from left to right.
If $t$ lies on the left of $s(t)\to r(t)$, the path leaves $t$ across $g$, and the corners of $t$ in counterclockwise order are $s(t),r(t),u(t)$.
Either the path entered across the side $r(t)u(t)$ and turns around $r(t)$, which is then on its left, or it entered across $s(t)u(t)$ and turns around $s(t)$, which is then on its right.
In both cases the summand is $+1$.
If $t$ lies on the right, the path enters $t$ across $g$, and the same check gives $+1$ again.
Reversing the direction of travel exchanges left and right, which gives $-1$ for a crossing from right to left.

Every step of the path across an edge of $C$ enters or leaves the black face of that edge, which lies in $A$ and is therefore not an end of the path.
So the sum over $t$ is the number of steps that cross $C$ from left to right minus the number that cross from right to left.
The left of the counterclockwise cycle $C$ is its inside, and by Lemma~\ref{lem:duality}(1) a step changes sides of $C$ exactly when it crosses an edge of $C$.
The path ends in $t_0$, which is outside $C$.
So the sum is $1$ if $y$ is inside $C$ and $0$ otherwise.
Finally $L(C)\ge1$ by the disk identity.
```

Instruction for the rest of Section 4 if 5 is accepted: replace `h_s(w)` by `\eta_s(y)` in the sentence after Lemma 4.6 ("Since $h_s(w)$ is a sum over faces"), delete the sentence "Spokes appear only as a way to draw a corner, when we define heights in Section~\ref{sec:pairs}." from the introduction, and drop panel (c) of Figure 3 and the dotted route in Figure 10.

Note. A further shortening of the same kind is the product sign `\eps(r,s)=\prod_{t\in A}\delta(r(t),s(t))` (R S2), which reduces the proof of Lemma 4.4 to "each reversal flips an odd number of factors". I do not write it out as an edit because it changes Lemma 4.4, Proposition 4.8, Figure 9 and Remark 4.10 together.

## 6. If spokes are kept: they are arcs, not segments (R G2)

OLD (only if edit 5 is not applied; the text is inside edit 5a's OLD block)
```
Place a point $c_t$ inside each face $t\in A$ and call the segments from $c_t$ to the corners of $t$ \emph{spokes};
```
NEW
```
We may assume that the edges of $\T$ are polygonal arcs. Place a point $c_t$ inside each face $t\in A$, join it to the three corners of $t$ by polygonal arcs inside $t$ that meet only at $c_t$, and call these arcs \emph{spokes};
```

## 7. If spokes are kept: drop or prove the remark on changing paths (R G3, CR 59)

OLD (only if edit 5 is not applied; the text is inside edit 5b's OLD block)
```
Changing the paths adds to each $h_s(w)$ a constant that does not depend on $s$; nothing below depends on the choice.
```
NEW
```
The paths are fixed once and for all.
(Another choice of paths changes each $h_s(w)$ by a constant that does not depend on $s$, because the spokes of two states differ by a closed chain. We do not use this.)
```

## 8. The route: say that step 3 needs a pair (CR 8)

OLD
```
Counting such pairs with a sign, the pairs that fail cancel in twos, while a regrouping by the cycles along which the two choices differ shows that the total is not zero (Section~\ref{sec:pairs}).
\item One pair is needed to start. A flow argument provides it unless $\T$ has a separating triangle (Section~\ref{sec:flow}), and separating triangles are removed by cutting $\T$ into two smaller triangulations whose solutions agree along the prescribed edge (Section~\ref{sec:glue}).
```
NEW
```
Counting such pairs with a sign, the pairs that fail cancel in twos, while a regrouping by the cycles along which the two choices differ shows that the total is not zero as soon as there is one pair (Section~\ref{sec:pairs}).
\item A flow argument provides a pair unless $\T$ has a separating triangle, that is, a triangle with vertices on both sides (Section~\ref{sec:flow}). Separating triangles are removed by cutting $\T$ into two smaller triangulations whose solutions agree along the prescribed edge (Section~\ref{sec:glue}).
```

## 9. Notation: one letter, one meaning (X rule 14, CR 58)

Instruction (scoped renames; none changes a statement).
- White faces are `y` in Lemma 3.3 and Figure 3(c) and `w` in Section 4. Use `y` everywhere (edit 5 does this for the heights; do the same in the caption of Figure 10 and in Example 4.9 if they name a face).
- The height `h_s(w)` clashes with the cycle length `h`. Rename the height `\eta_s(y)`.
- In Lemma 4.7 and Proposition 4.8 the constant `b` clashes with the root `b`. Rename it `\omega_0` in both places ("where $\omega_0$ is the weight of the second state in the all-clockwise orientation").
- In Proposition 5.2, "Let $b$ and $w$ be the numbers of black and white faces of $K$ of length three" clashes with the root `b`, the vertex `w` and the white face. Rename them `f_\bullet` and `f_\circ` through the end of the proof (five occurrences each).
- The component `K` of `\T[U]` in Proposition 5.2 clashes with the cycle `K` of `Q_s`. Rename the component `H`.
- Add after the first paragraph of Section 3 a table with one row per symbol: `t_0`, `e_0`, roots `a,b,c`, `A`, `X`, `n`, `s`, `Q_s`, `S_s`, `Y_s`, `P_s`, and later `r`, `u(t)`, `\Dc(r,s)`, `\delta`, `J`, `\eps`, `\omega`, with "what it is" and "where defined".

## 10. Define "good" before the lemma that needs it (R S3, CR 28)

Instruction. Move the block from `\begin{lemma}\label{lem:good}` through the `\end{definition}` of "good" to directly before `\begin{lemma}\label{lem:Y}`, in the order Definition (good), Lemma `lem:good`. Then:

OLD
```
Let $s$ be a state such that $S_s$ is a spanning tree of $\T$.
Then $Y_s$ is a tree on the $2k$ faces of $\T$, in which every face of $A$ has degree two and $t_0$ has degree one.
```
NEW
```
Let $s$ be a good state, so that $S_s$ is a spanning tree of $\T$ by Lemma~\ref{lem:good}.
Then $Y_s$ is a tree on the $2k$ faces of $\T$, in which every face of $A$ has degree two and $t_0$ has degree one.
```

## 11. Say why an $m$-th power before the algebra (X rule 10, CR 61, 62)

OLD
```
We take $F=\omega^m$.
The $m$-th power is what makes the cycles with fewest cycles count, as the following computation shows.
```
NEW
```
We take $F=\omega^m$.
Here is why a power.
Pairs with the same undirected cycles differ only in the orientations of these cycles, and by Lemma~\ref{lem:height} the weight $\omega$ is a constant plus one term for each cycle that runs counterclockwise.
The sign $\eps$ alternates with each orientation, so the signed sum over such pairs is a repeated difference, one difference for each cycle.
A difference taken $c$ times kills every polynomial of degree less than $c$, and on a polynomial of degree $c$ it leaves only the product of the $c$ steps.
So with the $m$-th power, pairs with more than $m$ cycles drop out and pairs with exactly $m$ cycles contribute a product of the numbers $L(C)$.
```

## 12. Proposition 4.8: one missing reason and one misleading word (R G4, CR 63)

**12a.** OLD
```
In each face $t$ it has $(r'(t),s'(t))=(r(t),s(t))$ or $(s(t),r(t))$.
```
NEW
```
The common edge set contains exactly one side of each face $t\in A$, because edges from distinct black faces are distinct.
So in each face $t$ the pair $(r',s')$ has $(r'(t),s'(t))=(r(t),s(t))$ or $(s(t),r(t))$.
```

**12b.** Instruction. In the proof of Proposition 4.8, in the paragraph after it and in Example 4.9, replace "group" by "class" (eight occurrences: "Group the pairs" becomes "Sort the pairs into classes", "the group of $(r,s)$" becomes "the class of $(r,s)$", "the group contributes" becomes "the class contributes", "Every group" becomes "Every class", "A group with $c$ cycles", "Only the groups", "two groups of four").

## 13. Sources paragraph: one list, exact claims, named notes (X (f))

OLD
```
The following simplifications were found in unpublished notes written during a collaborative reading of the three papers; we checked each one and give complete proofs:
\begin{itemize}
\item the disk identity in the form ``one more white face than black'' (Lemma~\ref{lem:disk});
\item the short acyclicity proof of Proposition~\ref{prop:recover};
\item the observation that every acyclic selection comes from a corner choice (Lemma~\ref{lem:selections-give-states});
\item heights at white faces in place of the circulation lemma of \cite{openai2026}, which removes the exponential sum and the complex phase (Lemma~\ref{lem:height});
\item the finite-difference form of the nonvanishing argument (Lemma~\ref{lem:difference}), which we apply to the weight $\omega^m$ that all three papers use.
\end{itemize}
Two smaller changes are ours: we obtain the tree of faces $Y_s$ of Lemma~\ref{lem:Y} directly from $Q_s$ by duality in $\T$ (in $G$ it is Li's ``black dual trace'' \cite[Section~6]{li2026} with one extra leaf), and a winding-number argument replaces the sliding of edges onto spokes in \cite[Section~5.3]{openai2026}.
```
NEW
```
We depart from \cite{openai2026} in the following places.
None of these departures has been published; they come from the working notes of this project, and each is proved in full below.
\begin{itemize}
\item The disk identity is stated as ``one more white face than black'' (Lemma~\ref{lem:disk}), and the acyclicity of the selected edges is read off from it (Proposition~\ref{prop:recover}). Both are rephrasings of counts in \cite{openai2026}.
\item Every acyclic selection comes from a corner choice (Lemma~\ref{lem:selections-give-states}). We use this to motivate the definition of a state.
\item The tree of faces $Y_s$ is obtained from $Q_s$ by duality in $\T$ (Lemma~\ref{lem:Y}). In $G$ it is Li's ``black dual trace'' \cite[Section~6]{li2026} with one extra leaf.
\item The weights are heights at the white faces (Lemma~\ref{lem:height}). They are the weights that \cite{openai2026} constructs in the proof of its Lemma~5.3, read face by face, and our proof of Lemma~\ref{lem:height} replaces the sliding of edges onto spokes in \cite[Section~5.3]{openai2026}.
\item Nonvanishing is a finite difference of an $m$-th power (Lemma~\ref{lem:difference}), where \cite{openai2026} takes a Taylor coefficient of order $m$ of an exponential sum.
\end{itemize}
```

Instruction. If the project decides to cite its notes, add the repository address after "working notes of this project". If `research/2026-11-14_opus_lean-formalisation/DIFFERENCES.md` item 19 is right that the formal proof released with [12] builds the same tree in `G`, add to the third bullet: "The formal proof that accompanies \cite{openai2026} proceeds in the same way."

## 14. Remark 4.10: what the three papers extract (R section 4, X (f) 3)

OLD
```
The constructive paper \cite{constructive2026} uses the integer polynomial $\sum\eps(r,s)z^{\omega(s)}$ and its coefficient of $(z-1)^m$, which is again $\Sigma/m!$; Li \cite{li2026} counts lists of $m$ marks, which are the terms of $\omega(s)^m$.
```
NEW
```
The constructive paper \cite{constructive2026} uses the integer polynomial $\sum\eps(r,s)z^{\omega(s)}$ and its coefficient of $(z-1)^m$, which is $\sum\eps(r,s)\binom{\omega(s)}{m}$. This is again $\Sigma/m!$, because the sums of $\eps\,\omega^j$ with $j<m$ vanish by Lemma~\ref{lem:difference}.
Li \cite{li2026} marks $m$ distinct crossings of rays with spokes, which gives a symmetric function of degree $m$ in the crossing signs in place of the power.
```

## 15. Section 7: name the side for the prism (R section 4)

OLD
```
For the hexagonal prism, whose dual is the hexagonal bipyramid, a direct check with a black face as $t_0$ gives three states, two of them good, and four Hamiltonian cycles avoiding the edge; so the map is not onto in general.
```
NEW
```
For the hexagonal prism, whose dual is the hexagonal bipyramid, take a black face as $t_0$ and its side on the equator as $e_0$, so that the avoided edge of the prism joins the two hexagons.
A direct check gives three states, two of them good, and four Hamiltonian cycles avoiding that edge; so the map is not onto in general.
(For the other two sides of $t_0$ there are two such cycles and both come from good states.)
```

## 16. Keep the promise "few enough to list": the eight pairs (CR 12, 65)

Insert at the end of Example 4.9, before `\end{example}`. Values `COMPUTED` (`recompute.txt`; orientation as in the figures, `\omega` normalised as in the author's `example.txt`, which differs from the lab's by `\omega\mapsto5-\omega`).

OLD
```
The other six pairs have good second states, three with $\eps=+1$ and three with $\eps=-1$.
\end{example}
```
NEW
```
The other six pairs have good second states, three with $\eps=+1$ and three with $\eps=-1$.
Table~\ref{tab:pairs} lists all eight.
In each class the four values of $\eps\,\omega^2$ add up to $2!\,L_1L_2$: $4-1-16+25=12$ and $0-1-9+16=6$.
\end{example}

\begin{table}[ht]
\centering
\begin{tabular}{@{}cccrrrc@{}}
\toprule
class & $7$-cycle & triangle & $J$ & $\eps$ & $\omega(s)$ & second state \\
\midrule
$L=6,1$ & cw & cw & $2$ & $+1$ & $-2$ & good \\
$L=6,1$ & cw & ccw & $0$ & $-1$ & $-1$ & good \\
$L=6,1$ & ccw & cw & $0$ & $-1$ & $4$ & cycle in $Q_s$ \\
$L=6,1$ & ccw & ccw & $-2$ & $+1$ & $5$ & good \\
\midrule
$L=3,1$ & cw & cw & $2$ & $+1$ & $0$ & good \\
$L=3,1$ & cw & ccw & $0$ & $-1$ & $1$ & good \\
$L=3,1$ & ccw & cw & $0$ & $-1$ & $3$ & good \\
$L=3,1$ & ccw & ccw & $-2$ & $+1$ & $4$ & cycle in $Q_s$ \\
\bottomrule
\end{tabular}
\caption{The eight pairs of the example. The two pairs with a cycle in $Q_s$ have the same second state and cancel.}
\label{tab:pairs}
\end{table}
```

## 17. Abstract: say the condition, split the long sentence (CR 1, 2; X (d) 11, 12)

OLD
```
In that picture a Hamiltonian cycle avoiding a given edge is an acyclic set of edges containing exactly one side of every triangle, and such a set can be built from a choice of one corner in each black triangle whose opposite sides form a suitably rooted forest.
To find such a choice we count pairs of disjoint corner choices with signs: fixing the second choice cancels every pair whose opposite sides contain a cycle, while grouping by the cycles along which the two choices differ shows that the total is not zero.
```
NEW
```
In that picture a Hamiltonian cycle avoiding a given edge is an acyclic set of edges containing exactly one side of every triangle.
Such a set can be built from a choice of one corner in each black triangle, provided the sides opposite the chosen corners form a forest with one corner of the outer triangle in each tree.
To find such a choice we count, with signs, pairs of corner choices that differ in every triangle.
For a fixed second choice whose opposite sides contain a cycle, the pairs cancel.
Grouping the pairs by the cycles along which the two choices differ shows that the total is not zero.
```

## 18. Two slips in Section 2 (CR 17, 22)

**18a.** OLD
```
We use the following lemma twice, once for $M=\T$ in Section~\ref{sec:corners} and once below.
```
NEW
```
We use the following lemma twice with $M=\T$, in Proposition~\ref{prop:target} and in Lemma~\ref{lem:Y}.
```

**18b.** OLD
```
A selection $P$ containing an edge $e_0$ of $\T$ gives a Hamiltonian cycle of $G$ that avoids the edge of $G$ crossing $e_0$.
```
NEW
```
An acyclic selection $P$ containing an edge $e_0$ of $\T$ gives a Hamiltonian cycle of $G$ that avoids the edge of $G$ crossing $e_0$.
We use part (2) in Lemma~\ref{lem:selections-give-states} and in the gluing of Section~\ref{sec:glue}.
```

## 19. Remove process talk (X rule 21, (d) 5 and 6)

**19a.** OLD
```
Filled and hollow dots are the two colour classes. Figure from the shared figure set of this project.}
```
NEW
```
Filled and hollow dots are the two colour classes.}
```

**19b.** OLD
```
It has 12 corner choices and 8 pairs, few enough to list, and it still shows every phenomenon of the proof: a pair whose opposite sides contain a cycle, and two choices that differ along a cycle enclosing a vertex.
All numbers we state about it were computed by a short script that is independent of the figure code.
```
NEW
```
It has 12 corner choices and 8 pairs, which Table~\ref{tab:pairs} lists.
Among them are a pair whose opposite sides contain a cycle and two choices that differ along a cycle enclosing a vertex.
The numbers quoted for the example come from exhaustive enumeration.
```

## 20. Credit Kelmans (X (f) 1 and 2)

**20a.** OLD
```
That the stronger statement is equivalent to the conjecture was known before; see Hertel's survey \cite{hertel2005}.
```
NEW
```
That the stronger statement is equivalent to the conjecture is due to Kelmans; see Hertel's survey \cite{hertel2005}.
```

**20b.** OLD
```
Read in the primal graph, $\Delta$ is a cut of three edges, each piece is $G$ with one side of the cut contracted to a vertex, and the gluing joins two Hamiltonian cycles that use the same two cut edges; this is the form of the argument in \cite[Appendix~C]{li2026}.
```
NEW
```
Read in the primal graph, $\Delta$ is a cut of three edges, each piece is $G$ with one side of the cut contracted to a vertex, and the gluing joins two Hamiltonian cycles that use the same two cut edges; this is the form of the argument in \cite[Appendix~C]{li2026}.
That it suffices to treat graphs without such cuts goes back to Kelmans; see \cite{hertel2005,apsw2016}.
```

Instruction. Add Kelmans's paper to `refs.bib` only after someone has seen it (A. K. Kelmans, AMS Transl. (2) 158 (1994) 127 to 140, as given in `research/2026-11-14_opus_history-literature/EQUIVALENTS.md`, which says "Kelmans' paper not seen").

## 21. Figure 2: say what the markers and the prescribed edge are (CR 19)

OLD
```
\caption{The example triangulation $\T$ with its 13 vertices labelled, drawn with the outer face $t_0=\{0,4,5\}$ as the grey collar. Black faces are shaded.
```
NEW
```
\caption{The example triangulation $\T$ with its 13 vertices labelled, drawn with the outer face $t_0=\{0,4,5\}$ as the grey collar. The three large hollow circles are its corners; in Sections~\ref{sec:corners} to~\ref{sec:flow} the prescribed side is $e_0=\{0,4\}$, the bottom arc. Black faces are shaded.
```

Instruction for the figure makers: move the labels 6, 11, 12 off the dots of `G` and 3, 8 off the edges in `03-dual`; print the thirteen labels in `07-pair-D`, `08-disk`, `09-Q`, `13-selected` and in the author's `fig-recover-a/b`; enlarge the inner octahedron in `14-gluing`(c) and keep one labelling across its three panels; use one grey for black faces in shared and own figures.

## 22. `S_s` is not all excluded edges (CR 26)

OLD
```
the set of all excluded edges, with $n+2=|V(\T)|-1$ elements (Figure~\ref{fig:local}(a)).
```
NEW
```
the set of edges that every such selection excludes, with $n+2=|V(\T)|-1$ elements (Figure~\ref{fig:local}(a)).
```

## 23. Cite Table 1 and keep it in place (X rule 16)

**23a.** OLD
```
A pair can be changed along a cycle in two ways.
```
NEW
```
A pair can be changed along a cycle in two ways, which Table~\ref{tab:reversals} sets side by side.
```

**23b.** OLD
```
\caption{The two reversals of Lemma~\ref{lem:reversals}.}
```
NEW
```
\vspace{4pt}
\caption{The two reversals of Lemma~\ref{lem:reversals}.}
```

## 24. Section 2 needs its own title (CR 13)

OLD
```
\section{One picture}\label{sec:picture}
```
NEW
```
\section{The dual triangulation and the target}\label{sec:picture}
```

## 25. "Why a second state": say what the partner does (CR 44, X (d) 9)

OLD
```
The second condition is global and awkward to control.
A second state takes care of it.
```
NEW
```
The second condition concerns whole components of $Q_s$.
A second state $r$ that differs from $s$ in every face turns it into the first.
Such an $r$ gives every non-root exactly one outgoing edge of $Q_s$, and then a component without a cycle must contain exactly one root (Lemma~\ref{lem:partner}).
So among states that have such a partner, good means that $Q_s$ has no cycle.
```

---

## Verification of the OLD blocks

Command: `python research/2026-11-14_fable_review-draft-B/verify_edits.py`. It extracts every block that follows a line starting with `OLD` and counts its occurrences in `paper/draft-B/barnette.tex`. Blocks marked "inside edit 5" are sub-strings of an earlier OLD block and are expected once.

Result of the run recorded in `verify_edits.txt`.
