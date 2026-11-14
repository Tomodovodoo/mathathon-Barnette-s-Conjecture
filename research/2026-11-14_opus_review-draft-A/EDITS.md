# Twenty-five edits to draft A, ordered by value to the reader

Against `paper/draft-A/barnette.tex` at commit d76deee. Each edit gives the exact old text (copy from the file) and the new text. Line numbers are approximate guides; the old text is authoritative. Edits are independent except: apply E11 before E15 (E15 renames the counts that E11 displays), and E14 before E22. Where an edit needs a shared figure changed, it says so; this review does not edit `paper/figures/`.

Trial build: applying E1–E25 mechanically to a scratch copy compiles with pdflatex/BibTeX with no errors, undefined references or overfull boxes; the paper grows from 11 to 12 pages.

Mathematical status of the new text: E10 and E11 change proofs. Both are `PROVED-HERE` in `REFEREE.md` §3 (N7, N6), and E10 is also `COMPUTED` (`check_examples.py`, keys `eps_equals_prod_delta_all_pairs`, `eps_prod_delta_family`). All other edits change wording, order, attribution or references only.

---

## E1. Replace the "Our main change" paragraph with an honest, self-contained statement of what differs (l.42)

Why: the paragraph uses five undefined terms, cites an internal note as a publication for the paper's main idea, and under-credits Li, whose half-ray counts are heights (EXPOSITION-REVIEW §f).

Old:
```
Our main change is in the signed count. Li \cite{li2026} replaces OpenAI's exponential sum by involutions on marked crossings. The constructive exposition \cite{constructive2026} uses integer signs and a polynomial. The root-component count below also follows that exposition. We use the product of face heights proposed in the project note \cite[Sections 1--3]{heightnote}, and prove its counting identity here. We also use that note's formulation of the disk identity and its short recovery argument. The product of heights uses the same cancellation mechanism, with each factor detecting enclosure of one face.
```
New:
```
Two arguments below differ from OpenAI's. To prove Proposition~\ref{prop:forest} we replace OpenAI's positive spoke circulations and exponential sum by a product of signed crossing counts at white faces. These counts are the half-ray intersections of Li \cite[Section~4]{li2026}, taken along fixed paths and multiplied rather than marked and paired by involutions. The constructive paper \cite{constructive2026} had already replaced OpenAI's complex phase by an integer sign. To prove Lemma~\ref{lem:selected} we pair faces through their selected sides. Both arguments keep OpenAI's disk identity and OpenAI's two regroupings of one signed sum, and we prove both in full.
```

## E2. Give the route as implications, and say that P is read off from Q_s (l.61)

Why: the cold reader carried "how does Q_s become P?" from p2 to p9 (COLD-READ p2, p8). Style rule 2.

Old:
```
We first construct the partition when there is no separating triangle, meaning a 3-cycle with vertices strictly on both sides. Section~\ref{sec:glue} then proves the proposition by induction. The matching and cancellation arguments in between will also apply whenever a pair of states exists.
```
New:
```
We first construct the partition when there is no separating triangle, meaning a 3-cycle with vertices strictly on both sides. Section~\ref{sec:glue} removes this assumption by induction. The construction has four steps. Section~\ref{sec:states} picks one corner $s(t)$ in each black face and looks at the sides opposite these corners, a graph $Q_s$. A second choice $r$, disjoint from $s$, orients $Q_s$ so that each of its components contains a root or a cycle. Lemma~\ref{lem:pair} shows that such pairs exist. Sections~\ref{sec:disk} and~\ref{sec:count} show that some pair has $Q_s$ a forest. Section~\ref{sec:recover} turns that forest into a tree on the white faces, and this tree picks the sides of $P$. So $P$ is read off from $Q_s$; it is not $Q_s$. The arguments of Sections~\ref{sec:states}--\ref{sec:count} hold whenever a pair of states exists, with or without separating triangles.
```

## E3. Give the spokes a job when they appear (l.81), and define H there once (l.267)

Why: spokes and centres are introduced with no purpose and suppressed one paragraph later (COLD-READ p2). The constructive paper's framing (C §1) fixes this. The counts are `PROVED-HERE`: H has (n+3) + (n+1) vertices and 3(n+1) spokes.

Old (l.81):
```
We need a local choice whose acyclicity can eventually be tested. Put a center $c_t$ in each black face and join it to its corners by three spokes. We will delete one spoke at each bounded black center and one at each nonroot.
```
New:
```
Put a center $c_t$ in each black face, including $t_0$, and join it to its corners by three spokes. Call this graph of spokes $H$. It has $2n+4$ vertices and $3n+3$ edges, so a spanning tree of $H$ keeps all but $n$ spokes. Section~\ref{sec:recover} turns such a spanning tree into the forest $P$, so we look for $n$ spokes to delete. We will delete one spoke at each bounded black center and one at each nonroot.
```
Old (l.267):
```
Let $H$ be the sphere graph of all black centers and their spokes, including the center of $t_0$. It is connected:
```
New:
```
Recall the spoke graph $H$ from Section~\ref{sec:states}. It is connected, since
```

## E4. Say what Q_s is for, and show it in one triangle (after l.83)

Why: Q_s is defined without a stated purpose; the most useful missing figure is the one-triangle picture (EXPOSITION-REVIEW §e).

Old:
```
Distinct black faces supply distinct edges, since an edge has only one black incident face.
```
New:
```
Distinct black faces supply distinct edges, since an edge has only one black incident face. The two spokes kept at $c_t$ are a subdivided copy of this side. So $Q_s$ is what is left of $H$ after deleting the spokes $(t,s(t))$ and the outer center, with the other centers suppressed. Section~\ref{sec:recover} shows that $H$ minus the spokes $(t,s(t))$ is a spanning tree when $Q_s$ is a forest with one root in each component. That is the property we look for. Figure~\ref{fig:04-local} shows the sides involved in one black face.
\fig{04-local}{.45}{One bounded black face $t$. The outlined corner is $r(t)$, the solid corner is $s(t)$, and the third corner is $u(t)$. The dashed side opposite $s(t)$ is the edge of $Q_s$; the arrow $r(t)\to s(t)$ is the edge of $D$ used in Section~\ref{sec:count}.}
```
Figure note: in a trial build with both panels at width .45 the labels fell below footnote size. Include only panel (a) of `04-local.pdf` (clip with `trim`) at width about .4, or ask the figure owner for a variant without the a(t,·) labels of panel (b), which draft A does not use.

## E5. Lemma 4: put the partner hypothesis on the second sentence (l.88)

Why: as printed, the second sentence asserts that every forest Q_s has a partner. False without the hypothesis (REFEREE N4).

Old:
```
If $Q_s$ is a forest, it has three components, one at each root, and $s$ has exactly one partner.
```
New:
```
If moreover $Q_s$ is a forest, it has three components, one at each root, and $r$ is the only partner of $s$.
```

## E6. State the two tasks before the examples, not after (l.112 → after l.93)

Why: the cold reader met the 13-vertex table without knowing what it was for (COLD-READ p3).

Old (l.93, end of paragraph):
```
Its edges require distinct tails, exhausting all its vertices.
```
New:
```
Its edges require distinct tails, exhausting all its vertices.

We now have two tasks: obtain a pair at all, then find a pair whose second state has forest $Q_s$.
```
Old (l.112):
```
We now have two tasks: obtain a pair at all, then find a pair whose second state has forest $Q_s$. The following density argument is OpenAI's \cite[Proposition 3.1]{openai2026}.
```
New:
```
The first task is OpenAI's density argument \cite[Proposition 3.1]{openai2026}.
```

## E7. Say why the cube is not enough (l.96, l.98)

Old:
```
Both states of this rooted octahedron have forest opposite-edge graphs. To see cancellation of a cyclic $Q_s$, we need a larger example.
```
New:
```
Both states of this rooted octahedron have forest opposite-edge graphs. So the cube cannot show the difficulty that Section~\ref{sec:count} must overcome.
```
Old:
```
For that purpose we also use the 13-vertex triangulation
```
New:
```
For that we also use the 13-vertex triangulation
```

## E8. Lemma 5: goal first, drop the re-proof of integral max-flow (l.118, l.124)

Why: style rules 10 and 12; the cold reader found the network before the goal, and the integrality paragraph redundant.

Old:
```
Give capacity two to edges from a source to $X$ and from $A$ to a sink,
```
New:
```
A pair is the same as a spanning subgraph of $B$ with degree two at every vertex, since such a subgraph is a union of even cycles, which split alternately into two disjoint perfect matchings. We find one as an integral flow. Give capacity two to edges from a source to $X$ and from $A$ to a sink,
```
Old:
```
Integral max-flow/min-cut \cite{ford1956} then gives a flow of value $2n$. All source and sink edges are saturated. The incidences carrying one unit form a spanning degree-two subgraph of $B$, whose even cycles split alternately into two disjoint perfect matchings. For completeness, integrality follows by augmenting from zero along residual paths: the bottleneck is an integer, the value increases each time, and if no path remains the reachable vertices give a cut of equal value.
```
New:
```
The integral max-flow/min-cut theorem \cite{ford1956} then gives an integral flow of value $2n$. It saturates every source and sink edge, so the incidences carrying one unit have degree two at every vertex of $B$.
```

## E9. Lemma 5: replace the t0 instruction by the actual computation (l.126)

Why: "Include t0 in the sum with contribution zero" does not say which sum; the equivalence (3)⇔(4) holds when b(U) counts t0 (REFEREE N5b; `COMPUTED` on all 1024 subsets of the running example). The sentence is OpenAI's, copied.

Old:
```
Write $e(U)$ for the number of edges induced by $U$ and $b(U)$ for the number of actual black faces all of whose corners lie in $U$. Include $t_0$ in the sum with contribution zero. A black face with $j$ corners in $U$ has shortfall $\max(0,j-1)$ from two. This is its number of induced sides minus one when $j=3$. Summing over black faces and using~\eqref{eq:counts} shows that~\eqref{eq:flow} is equivalent to
```
New:
```
Write $e(U)$ for the number of edges of $T[U]$ and $b(U)$ for the number of black faces of $T$, including $t_0$, with all corners in $U$. A face $t\in A$ with $j$ corners in $U$ has $\min(2,|V(t)\cap S|)=2-\max(0,j-1)$, and $\max(0,j-1)$ is its number of sides in $T[U]$, minus one if $j=3$. Every edge lies in exactly one black face, and $t_0$ has its three sides in $T[U]$. Summing over $A$, the left side of~\eqref{eq:flow} is $2n-(e(U)-3)+(b(U)-1)$. Since $|S|=n+3-|U|$ by~\eqref{eq:counts}, inequality~\eqref{eq:flow} is equivalent to
```

## E10. Define the sign as the product of local signs; drop J (l.181–189, l.198–202, l.209, l.238)

Why: removes J, its integrality paragraph and the identity δ(u,s) − δ(r,s) = 2δ(r,u), and makes the sign flip a one-line parity count. Equal to the draft's ε on every pair (`PROVED-HERE` REFEREE N7; `COMPUTED` on 196 pairs). Also fixes the unstated Lemma 6 call (REFEREE N8).

Old (l.181–189):
```
To assign a sign that reverses on either kind of cycle, put
\begin{equation}\label{eq:sign}
\begin{split}
 J(r,s)&=\frac13\sum_{t\in A}\delta(r(t),s(t))
       =\#\cw\text{ cycles of }D-\#\ccw\text{ cycles of }D,\\
 \eps(r,s)&=(-1)^{(n+J(r,s))/2}.
\end{split}
\end{equation}
The exponent is an integer: if $D$ has $c$ cycles, their odd lengths sum to $n$, so $c\equiv n\pmod2$, and $J\equiv c\pmod2$. The two operations we will use are different.
```
New:
```
To assign a sign that reverses on either kind of cycle, put
\begin{equation}\label{eq:sign}
 \eps(r,s)=\prod_{t\in A}\delta(r(t),s(t)).
\end{equation}
By Lemma~\ref{lem:disk}, a cycle of $D$ of length $h$ contributes $(h+3)/2$ factors $-1$ if it is counterclockwise and $(h-3)/2$ if it is clockwise. The two operations we will use are different.
```
Old (l.198–202, from "On each changed triangle"):
```
On each changed triangle the cyclic order of its three corners gives
\[
 \delta(u(t),s(t))-\delta(r(t),s(t))=2\delta(r(t),u(t)).
\]
For example, when $(r,u,s)$ is counterclockwise the left side is $1-(-1)=2$; the other cyclic order negates all three signs. Lemma~\ref{lem:disk} on $K$ therefore gives $J(r',s)-J(r,s)=\pm2$, and $\eps(r',s)=-\eps(r,s)$.
```
New:
```
On each changed triangle the directed sides $r(t)\to s(t)$ and $s(t)\to u(t)$ run the same way round $t$, so $\delta(u(t),s(t))=-\delta(r(t),s(t))$. Hence $\eps(r',s)=(-1)^{|K|}\eps(r,s)$. Lemma~\ref{lem:disk}, applied to the state $r$ with the sides $r(t)\to u(t)$ chosen on the faces of $K$, makes $|K|$ odd. So $\eps(r',s)=-\eps(r,s)$.
```
Old (l.209):
```
The values of $J$ are $0$ and $-2$; since $n=10$, the signs are $-1$ and $+1$.
```
New:
```
The cycle $K$ has length three, so the signs are opposite: $\eps(r,s)=-1$ and $\eps(r',s)=+1$.
```
Old (l.238):
```
With $U$ its counterclockwise cycles, $J=c-2|U|$. Thus its group contributes
```
New:
```
If $U$ is the set of its counterclockwise cycles, \eqref{eq:sign} has $(n-3c)/2+3|U|$ factors $-1$, so $\eps=(-1)^{(n+c)/2}(-1)^{|U|}$. Thus its group contributes
```
Also delete the now unused `\newcommand{\cw}` and `\newcommand{\ccw}` (l.14–15).

## E11. Make the disk identity's displayed counts the ones Figure 4 shows (l.158–163)

Why: eq. (6) uses E_d; Figure 4's side panel shows B + W = 2I + h − 2 and 3(B − W) = 2ℓ − h. The reader had to reconcile them (COLD-READ p6). The new proof is OpenAI's (4.1)–(4.2), `PROVED-HERE` in REFEREE N6.

Old:
```
Bijectivity gives the first of the three counts
\begin{equation}\label{eq:threecounts}
 B=I+\ell,\qquad E_d=3B+h-\ell=3W+\ell,
 \qquad (I+h)-E_d+B+W=1.
\end{equation}
For the middle count, each edge has one black and one white incident face; count the edges by the black faces inside, then add the boundary edges with black outside. The last count is Euler's formula for the disk. Substitution gives $W-B=1$, and the two expressions for $E_d$ give $h-2\ell=3$.
```
New:
```
Bijectivity gives the first of the three counts
\begin{equation}\label{eq:threecounts}
 B=I+\ell,\qquad B+W=2I+h-2,\qquad 3(B-W)=2\ell-h.
\end{equation}
The second is Euler's formula: the disk has $I+h$ vertices, $B+W$ triangles and $E_d$ edges with $2E_d=3(B+W)+h$. The third counts sides with sign: a black triangle contributes $+3$, a white one $-3$, an interior side cancels, and a boundary side gives $+1$ when its black face is inside and $-1$ otherwise. Putting $I=B-\ell$ into the second count gives $W=B+h-2\ell-2$, and the third gives $W=B+(h-2\ell)/3$. Hence $h-2\ell=3$ and $W=B+1$.
```
And in the example after the lemma (l.168), "so all three counts in~\eqref{eq:threecounts} can be seen in Figure~\ref{fig:08-disk}" is now literally true; keep it.

## E12. Flag that P uses the side through s(t), not Q_s (l.271)

Why: the switch from "opposite s(t)" to "through s(t)" is unannounced (COLD-READ p8, SUMMARY gap 3).

Old:
```
A deleted spoke $(t,s(t))$ borders the white faces across the two sides of $t$ incident with $s(t)$. Select the side bordering its assigned white face.
```
New:
```
A deleted spoke $(t,s(t))$ borders the white faces across the two sides of $t$ incident with $s(t)$. Select the side bordering its assigned white face. This is one of the two sides through $s(t)$, never the side of $Q_s$.
```

## E13. Complete the two-reversal table (l.190–196)

Why: style rule 16 asks for purpose and sign effect; with E10 the sign effect is the parity of a cycle length.

Old:
```
\begin{tabular}{@{}lll@{}}\toprule
Cycle reversed & Data changed & Data fixed\\\midrule
A cycle of $Q_s$ & $r$ only & $s$, hence any function of $s$\\
A cycle of $D$ & exchange $r$ and $s$ there & undirected $D$\\\bottomrule
\end{tabular}
```
New:
```
\begin{tabular}{@{}lllll@{}}\toprule
Cycle reversed & Data changed & Data fixed & Sign & Used for\\\midrule
A cycle of $Q_s$ & $r$ only & $s$, hence $F(s)$ & flips & cancel cyclic $Q_s$\\
A cycle of $D$ & exchange $r,s$ there & undirected $D$ & flips & show the sum $\neq0$\\\bottomrule
\end{tabular}
```

## E14. Lemma 8: state the two missing bridges (l.283, l.285)

Why: REFEREE N12c (y0 must be outside the disk) and N12d (Lemma 4 is about Q_s, not P0).

Old:
```
But the selected edges pair black faces with white faces. A face in the disk is paired
```
New:
```
But the selected sides pair black faces with white faces. The pair $t_0,y_0$, joined by $e_0\notin P_0$, lies outside the disk, since $y_0$ has two roots as corners and the closed disk contains no root. A face in the disk is paired
```
Old:
```
The outdegree count of Lemma~\ref{lem:components} gives one root in each component of $P_0$.
```
New:
```
The outdegree count from the proof of Lemma~\ref{lem:components}, applied to $P_0$, gives each component at most one root. As $P_0$ is a forest with $n$ edges on $n+3$ vertices, it has three components, one at each root.
```

## E15. Stop B and W from meaning two things (l.149–163, l.168, l.170, l.281–283, l.312)

Why: style rule 14; the proof currently patches the clash with a sentence. Keep B for the incidence graph, as the shared notation does.

In Lemma 6, its proof, the example after it, the caption of Figure 4 and the proof of Lemma 8, replace the face counts $B$ and $W$ by $B_d$ and $W_d$ (every occurrence of `B` and `W` used as a count: `W=B+1`, `B=I+\ell`, `B+W`, `3(B-W)`, `B=5`, `W=6`, `B=I+\ell=3+2`, `W-B`, `B-\ell=W-(h-\ell)`). In §6 (l.312) replace `$3(B-W)$` by `$3(b-w)$`, where b, w are the faces on that side. Then delete:
```
 Here $B,W$ are face counts, not the incidence graph $B$.
```
and in the lemma statement replace
```
Write $B,W$ for the numbers of black and white faces in that disk.
```
by
```
Write $B_d,W_d$ for the numbers of black and white faces in that disk.
```
Figure 4's side panel uses B, W: ask the figure owner for B_d, W_d, or add "(B, W in the figure)" to the caption.

## E16. Other symbol collisions (Lemma 5, §4)

Why: m is the minimum cycle count, K the Q_s cycle, u the third corner. Lemma 5 and the four-term example reuse all three.

In Lemma 5, rename the edge count of a component from m to q:
- `$m$ edges and $f$ faces` → `$q$ edges and $f$ faces`
- the display ` 2m=4f-b-w+\sum(d-4)\geq4f-2b,` → ` 2q=4f-b-w+\sum(d-4)\geq4f-2b,`; ` \qquad p-m+f=2,` → ` \qquad p-q+f=2,`; ` \qquad m-b\leq2p-4.` → ` \qquad q-b\leq2p-4.`
- `the weaker bound $m-b\leq2p$` → `the weaker bound $q-b\leq2p$`

In the four-term example (l.258–261):
- `If their height increments are indexed by $u,v\in\{0,1\}$` → `Write $x,y\in\{0,1\}$ for the reversal of the long and the small cycle`
- `\sum_{u,v=0}^1(-1)^{u+v}(b_1+u)(b_2+u+v)=1.` → `\sum_{x,y=0}^1(-1)^{x+y}(b_1+x)(b_2+x+y)=1.`

## E17. Say what the other group contributes, and drop the referee's caution (l.262)

Why: `COMPUTED`: the other group's signed sum is 0, not just "nonnegative" (`check_examples.json`, `F_groups`). The last sentence is a review remark, not exposition.

Old:
```
This displays why two heights are needed here and why nesting causes no problem. The other group contributes a nonnegative integer with the same overall sign. The proof does not assert that a preferred orientation within the displayed group survives cancellation.
```
New:
```
The small cycle lies inside the long one, so $w_2$ sees both reversals, and still the alternating sum is one. In the other group no bijection puts each $w_i$ inside its own cycle, so that group contributes $0$, and the whole sum is $1$.
```

## E18. Reference every figure where it is needed

Why: Figures 3, 5, 6 and 8 are never referenced (style rule 18).

- After `The edges $18,19,89$ form a cycle in $Q_s$, whereas $Q_r$ is a forest.` add ` Figure~\ref{fig:09-Q} shows both.`
- After `Heights may be negative and depend on the paths; only their changes will matter.` add ` Figure~\ref{fig:height} shows the one property of heights we use.`
- After `By Lemma~\ref{lem:duality}, the duals of the deleted spokes form a tree $W_s$ on the white faces.` add ` Figure~\ref{fig:12-tree-cotree} shows both trees in the larger example.`
- After `The original prescription survives.` add ` Figure~\ref{fig:14-gluing} shows the gluing for two octahedra.`

## E19. Tell the reader where each panel of Figure 1 is explained (l.73 caption)

Old:
```
The cube construction, read from left to right along each row. The first panel shows two cycles rather than one. In the octahedron the roots are $0,1,2$. Outlined and filled wedges mark the two states; the opposite edges form three rooted trees. Deleting the filled spokes gives an incidence tree and a complementary tree on white faces. The last panel shows the selected forest and the single dual cycle. Later sections justify each transition.
```
New:
```
The cube construction, a map of the paper. (a)~Two cycles of degree two (Section~1). (b)~The cube inside its dual octahedron, roots $0,1,2$. (c)~Two states, outlined $r$ and filled $s$, and the arrows $r(t)\to s(t)$ (Section~\ref{sec:count}). (d)~The sides opposite $s$ form three rooted trees (Section~\ref{sec:states}). (e)~Deleting the filled spokes leaves a tree; its dual is a tree on the white faces (Section~\ref{sec:recover}). (f)~The selected sides form two induced trees, and the dual cycle crossing the other sides is Hamiltonian.
```
Figure note: ask the figure owner to repeat the labels 0–5 in panels (c)–(f).

## E20. Fix the false statements about a_j and grey vertices (l.98, l.108)

Old (l.98):
```
The symbols $a_j$ are the numerical face identifiers used in the figures.
```
New:
```
We write $a_j$ for face number $j$ of the face list; the missing indices are the white faces and $t_0=a_4$.
```
Old (l.108 caption):
```
Each grey vertex of $G$ lies in one triangle and each grey edge crosses its corresponding edge of $T$.
```
New:
```
Each vertex of $G$, drawn black or white by its bipartition class, lies in one triangle, and each grey edge of $G$ crosses its corresponding edge of $T$.
```
Figure note: the labels 6, 11, 12 in `03-dual.pdf` overprint white vertices of G. Ask the figure owner to move them.

## E21. Announce the role swap of r and s before the recovery figures (l.306)

Old:
```
The same recovery applies to the larger example using $r$ as the forest second state; Figure~\ref{fig:13-selected} displays the two classes and their complementary cycle.
```
New:
```
In the larger example the forest state is the state called $r$ in~\eqref{eq:running}; in this section it plays the role of $s$. Figures~\ref{fig:12-tree-cotree} and~\ref{fig:13-selected} show its white tree, the two classes and their complementary cycle.
```

## E22. Unslop pass on the surviving tells (EXPOSITION-REVIEW §d)

- l.32 `is the easy part: the complement of a perfect matching has degree two everywhere.` → `is the easy part. The complement of a perfect matching has degree two everywhere.`
- l.44 delete `Here are the details needed for simplicity. `
- l.44 `A cut of one or two edges in $G$ would have at least three vertices on either side: a singleton in a simple cubic graph has three outgoing edges and a pair has at least four.` → `Suppose one or two edges of $G$ form a cut. Each side has at least three vertices, since a single vertex of a simple cubic graph has three outgoing edges and two vertices have at least four.`
- l.85 `A forest $Q_s$ would be useful only if its components keep the three roots separate. A second state supplies exactly this control.` → `We want $Q_s$ to be a forest with one root in each component. A second state gives a way to test this.`
- l.224 `Indeed, in any such orientation` → `In any such orientation`
- l.238 `Here is the full counting argument, for arbitrary $m$. Fix` → `Now let $m$ be arbitrary. Fix`
- l.254 `Indeed the sign is` → `The sign is`
- l.267 `In fact the spokes split` → `The spokes split`
- In the proof of Lemma 8 (l.281–287), replace every "selected edge" by "selected side"; also `Every boundary edge is selected` → `Every boundary side is selected` and `Internal selected chords` → `Selected chords`.
- l.289 caption: delete ` The separate degree and connectivity arguments are both needed.`

## E23. Pinpoint Theorem 1 (l.37)

Old:
```
\begin{theorem}[OpenAI \cite{openai2026}]\label{thm:main}
```
New:
```
\begin{theorem}[OpenAI {\cite[Theorem 1.1, Corollary 7.1]{openai2026}}]\label{thm:main}
```

## E24. Bibliography and history: no internal paths, Kelmans cited properly (l.40, refs.bib)

Old (l.40):
```
The prescribed-edge strengthening and the reduction to graphs without nontrivial three-edge cuts belong to the earlier work of Kelmans, as explained by Hertel and by Alt et al.\ \cite{hertel2005,apsw2016}.
```
New:
```
That avoiding a prescribed edge is equivalent to Barnette's conjecture goes back to Kelmans; see Hertel \cite[Corollary~3]{hertel2005} and Alt et al.\ \cite{apsw2016}.
```
In `refs.bib`:
- delete the entries `heightnote` and `draftdata` (no remaining citations after E1 and the change below);
- `constructive2026`: replace `note={Unsigned manuscript, 18 October 2026; supplied as papers/barnette\_trees.pdf}` by `note={Unsigned manuscript, dated 18 October 2026}`;
- `openai2026`: replace `note={OpenAI Math Release preprint, 24 September 2026, family 180}` by `note={Preprint, 24 September 2026}`.

l.107: `These assignments and all examples below can be checked directly from the face lists; the companion calculation \cite{draftdata} also recomputes them with the reference implementation.` → `The reader can check these assignments and all examples below from the face lists.`

Before `\bibliographystyle` add:
```
\subsection*{Acknowledgements and data}
The height formulation of Proposition~\ref{prop:forest} and the face-pairing proof of Lemma~\ref{lem:selected} were worked out while preparing this exposition. Scripts that recompute every example are available from the authors.
```
(Replace "available from the authors" with a public repository URL when one exists.)

## E25. One sentence on why "no separating triangle" appears (after Lemma 5's proof, l.142)

Why: the cold reader could not tell whether the hypothesis is essential (COLD-READ p5). The constructive manuscript states the exact criterion (LIT as a cited claim; this review did not re-prove it).

After `\end{proof}` of Lemma 5 add:
```
The hypothesis is used only once, to make every triangular face of $K$ a face of $T$. It is not the exact condition: the constructive manuscript \cite[Theorem~1.2]{constructive2026} states that a pair exists exactly when no separating triangle has black faces just inside all three of its sides, inside meaning on the side away from $t_0$. We do not need this, since Section~\ref{sec:glue} cuts along every separating triangle.
```
