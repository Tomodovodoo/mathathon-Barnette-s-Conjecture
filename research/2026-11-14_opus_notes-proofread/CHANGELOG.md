# Changelog

Every edit to the two companion notes, old text and new text. No mathematical statement or proof step was changed.

## proofs/primal/primal.tex

### primal edit (move)

The section "Sources" (formerly Section 10, placed before the remarks) now follows Section 10 "Which states and Hamiltonian cycles occur" and is numbered 11, so the note ends its text with the sources. Its content is as edited above.

### primal edit 1

Old:

```latex
\date{14 November 2026, refereed revision}
```

New:

```latex
\date{14 November 2026}
```

### primal edit 2

Old:

```latex
Status: PROVED-HERE, a complete informal reconstruction, corrected after the independent Fable referee report; human review pending. The theorem is LIT, OpenAI, Theorem 1.1 and Corollary 7.1. The proof follows the checked Lean development at commit \nolinkurl{4eaee87548250b2682affda7d05d947c05554bae}, with two explicit departures: Li's primal deficit proof supplies the first pair, and real local signs replace Lean's complex phases. STATUS.md distinguishes restatements from these departures. Numerical checks are evidence about the implementation, not a proof of the theorem.

This note gives the proof of the project's main paper (\nolinkurl{paper/main/barnette.pdf}) in the cubic graph $G$ itself, lemma by lemma, with a dictionary at the end; two steps differ, since Li's deficit argument gives the first pair (Lemma 4) and flow potentials with a polynomial (Lemmas 6 and 8) replace the heights.
```

New:

```latex
This note proves Barnette's conjecture in the form of Theorem T below, a theorem of OpenAI (their Theorem 1.1 and Corollary 7.1). It accompanies \emph{The proof of Barnette's conjecture: an exposition} (\nolinkurl{paper/main/barnette.pdf} in the same repository), called the main paper below, and follows its proof lemma by lemma, but works throughout in the cubic graph $G$ instead of the dual triangulation. A dictionary between the two languages follows Section 11. Two steps differ from the main paper. The first pair, its Proposition 5.2, comes here from Li's deficit argument (Lemma 4). The heights of its Section 4 are replaced by flow potentials and one polynomial (Lemmas 6 to 8), which give its Proposition 4.8. The argument also follows OpenAI's Lean development at commit \nolinkurl{4eaee87548250b2682affda7d05d947c05554bae}, and departs from it in two places: Li's deficit argument supplies the first pair, and real local signs replace Lean's complex phases. The proof below is an informal one; this text has not been machine-checked.
```

### primal edit 3

Old:

```latex
\textbf{General circuit-cut fact.} PROVED-HERE. In
```

New:

```latex
\textbf{General circuit-cut fact.} In
```

### primal edit 4

Old:

```latex
\textbf{Lemma 1, elementary setup.} PROVED-HERE. Facial
```

New:

```latex
\textbf{Lemma 1, elementary setup.} Facial
```

### primal edit 5

Old:

```latex
\textbf{Lemma 2, face circuits and cut-side faces.} PROVED-HERE; Lean counterparts are
```

New:

```latex
\textbf{Lemma 2, face circuits and cut-side faces.} Its Lean counterparts are
```

### primal edit 6

Old:

```latex
\textbf{Lemma 3, orientation of a bond.} PROVED-HERE. On
```

New:

```latex
\textbf{Lemma 3, orientation of a bond.} On
```

### primal edit 7

Old:

```latex
\textbf{Lemma 4, a pair exists in the irreducible case.} PROVED-HERE, expanding Li, Lemma 9 and Claim 12; its
```

New:

```latex
\textbf{Lemma 4, a pair exists in the irreducible case.} This expands Li, Lemma 9 and Claim 12; its
```

### primal edit 8

Old:

```latex
\textbf{Lemma 5, the cut-side identity.} PROVED-HERE, restating the conjunction of Lean's \nolinkurl{state_disk_count} and \nolinkurl{disk_boundary_imbalance}; LIT in equivalent form, OpenAI, Lemma 4.1. Let
```

New:

```latex
\textbf{Lemma 5, the cut-side identity.} This restates the conjunction of Lean's \nolinkurl{state_disk_count} and \nolinkurl{disk_boundary_imbalance}. In equivalent form it is OpenAI's Lemma 4.1, the disk identity, which is Lemma 3.8 of the main paper. Let
```

### primal edit 9

Old:

```latex
\textbf{Lemma 6, the weights.} PROVED-HERE, a primal restatement
```

New:

```latex
\textbf{Lemma 6, the weights.} A primal restatement
```

### primal edit 10

Old:

```latex
 STATUS.md records the adjudication of an earlier claim that the ratio depends on the number of circuits.
```

New:

```latex
(deleted)
```

### primal edit 11

Old:

```latex
\textbf{Lemma 7, cancellation.} PROVED-HERE. For
```

New:

```latex
\textbf{Lemma 7, cancellation.} For
```

### primal edit 12

Old:

```latex
\textbf{Lemma 8, nonvanishing.} PROVED-HERE. If
```

New:

```latex
\textbf{Lemma 8, nonvanishing.} If
```

### primal edit 13

Old:

```latex
\textbf{Lemma 9, the recovery tree.} PROVED-HERE, restating Lean's
```

New:

```latex
\textbf{Lemma 9, the recovery tree.} This restates Lean's
```

### primal edit 14

Old:

```latex
\textbf{Lemma 10, the selected matching.} PROVED-HERE, a constructive
```

New:

```latex
\textbf{Lemma 10, the selected matching.} A constructive
```

### primal edit 15

Old:

```latex
\textbf{Lemma 11, matching cut balance.} PROVED-HERE; Lean's \nolinkurl{matching_cut_balance}. If
```

New:

```latex
\textbf{Lemma 11, matching cut balance.} This is Lean's \nolinkurl{matching_cut_balance}. If
```

### primal edit 16

Old:

```latex
\textbf{Lemma 12, the complement is one cycle.} PROVED-HERE, restating Lean's
```

New:

```latex
\textbf{Lemma 12, the complement is one cycle.} This restates Lean's
```

### primal edit 17

Old:

```latex
\textbf{Lemma 13, caps and gluing.} PROVED-HERE, expanding Li, Appendix C, and matching the statements
```

New:

```latex
\textbf{Lemma 13, caps and gluing.} This expands Li, Appendix C, and matches the statements
```

### primal edit 18

Old:

```latex
The phrase "one selected edge per face" from
```

New:

```latex
The phrase ``one selected edge per face'' from
```

### primal edit 19

Old:

```latex
Apply strong induction on $|V(G)|$, with the quantifier "for every edge $e_0$" retained.
```

New:

```latex
Apply strong induction on $|V(G)|$, with the quantifier ``for every edge $e_0$'' retained.
```

### primal edit 20

Old:

```latex
The real-sign polynomial proof in Section 6 is the linear-weight refinement from research/2026-11-14\_fable\_referee-determinants/SIGNIFICANCE.md, Section 2. The flow
```

New:

```latex
The real-sign polynomial of Section 6 takes the place of OpenAI's exponential sum and complex phases. The flow
```

### primal edit 21

Old:

```latex
\section*{10. Sources}
```

New:

```latex
%SOURCES-MOVED
```

### primal edit 22

Old:

```latex
LIT. OpenAI, \emph{Paired states
```

New:

```latex
OpenAI, \emph{Paired states
```

### primal edit 23

Old:

```latex
LIT. Zhentao Li, \emph{A note
```

New:

```latex
Zhentao Li, \emph{A note
```

### primal edit 24

Old:

```latex
LIT. \emph{A constructive proof
```

New:

```latex
\emph{A constructive proof
```

### primal edit 25

Old:

```latex
Source-checked Lean statements and exact file locations are recorded in STATUS.md and the first reconstruction's LEAN-EXTRACTS.md. The revised reverse-Lamport audit is research/2026-11-14\_astra\_primal-revision/AUDIT.md. Exact example data remain in EXAMPLES.md; the PDF adds the dictionary and checked figures.
```

New:

```latex
OpenAI, \emph{Lean formalisation of Barnette's conjecture}, commit \nolinkurl{4eaee87548250b2682affda7d05d947c05554bae}. The Lean declarations named in this note, with their file locations, are listed in STATUS.md beside this note. Exact data for two further worked examples, the cube and a 20-vertex graph, are in EXAMPLES.md there.
```

### primal edit 26

Old:

```latex
\section*{11. Which states and Hamiltonian cycles occur}
```

New:

```latex
\section*{10. Which states and Hamiltonian cycles occur}
```

### primal edit 27

Old:

```latex
\textbf{Remark 14, the partner is unique when it exists.} PROVED-HERE. If
```

New:

```latex
\textbf{Remark 14, the partner is unique when it exists.} If
```

### primal edit 28

Old:

```latex
\textbf{Remark 15, compatible matchings.} PROVED-HERE. For
```

New:

```latex
\textbf{Remark 15, compatible matchings.} For
```

### primal edit 29

Old:

```latex
COMPUTED before these proofs: the independent referee checked 25,272 forest-state/root-edge cases without a partner, 3,256 forest states with a partner, and 186,476 matching/root pairs on 56 graph records with 8 to 24 primal vertices. The records include the cube twice. The three observations held throughout that range. See the referee's code/README.md for commands. These finite observations motivated Remarks 14 and 15; they do not replace the proofs. The tree-matching criterion in research/2026-11-14\_sol\_referee-structure/INTEGRATION.md, Sections 5 and 7, describes the same one-root-per-component condition through the incidence graph. Remark 15 covers every Hamiltonian complement, but does not assert that every compatible state is itself a forest state with a partner.
```

New:

```latex
Remarks 14 and 15 were first observed by computer, before the proofs were written: 25,272 forest-state and root-edge cases without a partner, 3,256 forest states with a partner, and 186,476 matching and root pairs, on 56 graph records with 8 to 24 vertices (the cube occurs twice). The three observations held throughout that range. The tree matchings of the constructive paper express the same one-root-per-component condition through the incidence graph. Remark 15 covers every Hamiltonian complement, but does not assert that every compatible state is itself a forest state with a partner.

\section*{11. Sources}
```

### primal edit 30

Old:

```latex
Object in G & Main paper, in T &
```

New:

```latex
Object in $G$ & Main paper, in $T$ &
```

### primal edit 31

Old:

```latex
Black / white vertex & Black / white triangle & Black / white face & B / W &
```

New:

```latex
Black / white vertex & Black / white triangle & Black / white face & $B$ / $W$ &
```

### primal edit 32

Old:

```latex
Root vertex b0, its three faces & Outer black triangle t0, its corners & t0, R & b0 and its face neighbours &
```

New:

```latex
Root vertex $b_0$, its three faces & Outer black triangle $t_0$, its corners & $t_0$, $R$ & $b_0$ and its face neighbours &
```

### primal edit 33

Old:

```latex
Incidences A to X & State: a corner in each black triangle & State & Perfect matching of H & Perfect matching of B &
```

New:

```latex
Incidences $A$ to $X$ & State: a corner in each black triangle & State & Perfect matching of $H$ & Perfect matching of $B$ &
```

### primal edit 34

Old:

```latex
Two disjoint states & Pair (r,s), different in every triangle & Pair (r,s) & Ordered 2-factor (M1,M2) &
```

New:

```latex
Two disjoint states & Pair $(r,s)$, different in every triangle & Pair $(r,s)$ & Ordered 2-factor $(M_1,M_2)$ &
```

### primal edit 35

Old:

```latex
Edge not on s(b), as face link & Opposite side, in Q\_s & Q\_s &
```

New:

```latex
Edge not on $s(b)$, as face link & Opposite side, in $Q_s$ & $Q_s$ &
```

### primal edit 36

Old:

```latex
Directed marked face links; undirected D & D(r,s); its cover & D(r,s); group & Cycles of M1 union M2 &
```

New:

```latex
Directed marked face links; undirected $D$ & $D(r,s)$; its cover & $D(r,s)$; group & Cycles of $M_1\cup M_2$ &
```

### primal edit 37

Old:

```latex
Bond; root-free shore & Cycle; disk away from t0 &
```

New:

```latex
Bond; root-free shore & Cycle; disk away from $t_0$ &
```

### primal edit 38

Old:

```latex
Forest Q\_s with a partner & Good state; good pair &
```

New:

```latex
Forest $Q_s$ with a partner & Good state and its partner &
```

### primal edit 39

Old:

```latex
Compatible perfect matching P & Selection P, one side of every face & One selected edge per face & Matching P &
```

New:

```latex
Compatible perfect matching $P$ & Selection $P$, one side of every face & One selected edge per face & Matching $P$ &
```

### primal edit 40

Old:

```latex
Hamiltonian cycle G-P &
```

New:

```latex
Hamiltonian cycle $G-P$ &
```

### primal edit 41

Old:

```latex
Nontrivial three-edge cut; cap & Separating triangle; capped piece &
```

New:

```latex
Nontrivial three-edge cut; cap & Separating triangle; piece with its cap &
```

### primal edit 42

Old:

```latex
LIT for the source terminology; PROVED-HERE for the identifications. Sources: OpenAI
```

New:

```latex
Each source column uses that source's own terminology; the identifications are proved in this note. Sources: OpenAI
```

### primal edit 43

Old:

```latex
Lean namespaces and exact citation scopes are in STATUS.md. With aligned signs and weights, the real-sign polynomial is i to the power n times Lean's phase polynomial. The recovery tree here lies in G, whereas
```

New:

```latex
Lean namespaces and exact citation scopes are listed in STATUS.md beside this note. With aligned signs and weights, the real-sign polynomial is $i^n$ times Lean's phase polynomial. The recovery tree here lies in $G$, whereas
```

### primal edit 44

Old:

```latex
The exact cube and 20-vertex worked-example data remain in EXAMPLES.md. The figures on the following pages instead use the current 13-face example, whose primal graph has 22 vertices.
```

New:

```latex
Exact data for the cube and for a 20-vertex example are in EXAMPLES.md beside this note. The figures on the following pages use the main paper's running example instead, whose graph $G$ has 22 vertices and 13 faces.
```

### primal edit 45

Old:

```latex
Figure 1. The cube and the 22-vertex running graph G, with faces labelled. Filled vertices are black, hollow vertices white. The bold edge is e0.
```

New:

```latex
Figure 1. The cube and the 22-vertex running graph $G$, with faces labelled. Filled vertices are black, hollow vertices white. The bold edge is $e_0$.
```

### primal edit 46

Old:

```latex
only edges of G are drawn.
```

New:

```latex
only edges of $G$ are drawn.
```

### primal edit 47

Old:

```latex
blue solid segments assign s; vermilion outlined segments assign r. Endpoints labelled f are primal faces, not vertices of G.
```

New:

```latex
blue solid segments assign $s$; vermilion outlined segments assign $r$. Endpoints labelled $f$ are faces of $G$, not vertices.
```

### primal edit 48

Old:

```latex
Green halos mark the vertices inside the cut side S; dashed
```

New:

```latex
Green halos mark the vertices of the cut side $S$; dashed
```

### primal edit 49

Old:

```latex
On the right h=7 and ell=2; the cut side has five black and six white vertices. Inside means the shore missing b0.
```

New:

```latex
On the right $h=7$ and $\ell=2$; the cut side has five black and six white vertices. The cut side is the shore missing $b_0$.
```

### primal edit 50

Old:

```latex
Integer path flow from b0 to every white vertex of G.
```

New:

```latex
Integer path flow from $b_0$ to every white vertex of $G$.
```

### primal edit 51

Old:

```latex
the weight is the number of white vertices in S, equivalently the white faces of T.
```

New:

```latex
the weight is the number of white vertices in $S$, equivalently of white faces of $T$ inside the disk.
```

### primal edit 52

Old:

```latex
A second state s whose Q\_s contains a face circuit, shown with its two partners. Dashed primal edges are Q\_s, viewed
```

New:

```latex
A second state $s$ whose $Q_s$ contains a face circuit, shown with its two partners. Dashed edges of $G$ are $Q_s$, viewed
```

### primal edit 53

Old:

```latex
The recovered perfect matching P is bold black; G-P is the purple Hamiltonian cycle. Every vertex has one matching edge and two cycle edges, and e0 belongs to P.
```

New:

```latex
The recovered perfect matching $P$ is bold black; $G-P$ is the purple Hamiltonian cycle. Every vertex has one matching edge and two cycle edges, and $e_0$ belongs to $P$.
```

### primal edit (move)

The section "Sources" (formerly Section 10, placed before the remarks) now follows Section 10 "Which states and Hamiltonian cycles occur" and is numbered 11, so the text ends with the sources. Its content is as edited above.

### primal edit (Lean source entry)

My first draft of the new Sources entry invented a title for the Lean development. It now uses the title and URL of the entry `OpenAI2026b` in paper/main/refs.bib, and the commit sentence is split off to avoid a 46pt overfull line. Final text:

```latex
OpenAI, \emph{openai/math: mathematical manuscripts and supporting proof artifacts}, \url{https://github.com/openai/math}. This note refers to its Lean development at commit \nolinkurl{4eaee87548250b2682affda7d05d947c05554bae}. The Lean declarations named in this note, with their file locations, are listed in STATUS.md beside this note. Exact data for two further worked examples, the cube and a 20-vertex graph, are in EXAMPLES.md there.
```

## proofs/involutions/involutions.tex

### involutions edit 1

Old:

```latex
We write out the intended multi-mark proof in Appendix B of Zhentao Li's note.
The proof uses finite signed sets and two explicit involutions. It uses no
generating function, limiting argument, or complex number. A finite alternating
path constructs a good pair. The coefficient comparison at the end is a
separate verification, not a premise of the proof.
```

New:

```latex
We prove that a coloured sphere triangulation with a pair of states has a
good pair (Theorem~\ref{main}). The proof is the multi-mark argument sketched
in Appendix B of Zhentao Li's note, written out in full. It uses finite signed
sets and two explicit involutions, and no generating function, limiting
argument or complex number. Section~\ref{paths} gives a version that needs no
drawing; in that form the proof unpacks, term by term, the height argument for
Proposition~4.8 of the main exposition. A finite alternating path between the
two involutions constructs a good pair. The coefficient comparison in
Section~\ref{compare} is a separate check, not part of the proof.
Section~\ref{example} lists every object of the main paper's running example.
```

### involutions edit 2

Old:

```latex
\section{Contract and notation}
```

New:

```latex
\section{Setting and notation}
```

### involutions edit 3

Old:

```latex
We call a pair $(r,s)$ for which $Q_s$ is a forest a \emph{good pair}.
Earlier versions of this note said forest pair.

```

New:

```latex
We call a pair $(r,s)$ for which $Q_s$ is a forest a \emph{good pair}.

```

### involutions edit 4

Old:

```latex
This note accompanies the project's main paper, \emph{The proof of
Barnette's conjecture: an exposition}, in the same repository.
```

New:

```latex
This note accompanies \emph{The proof of Barnette's conjecture: an
exposition} (\texttt{paper/main/barnette.pdf} in the same repository), called
the main paper below.
```

### involutions edit 5

Old:

```latex
This is OpenAI Proposition 5.1. It is the cancellation part of Li's Key
Lemma 7.
```

New:

```latex
Theorem~\ref{main} is OpenAI's Proposition 5.1 \cite{OAI}, and the
cancellation part of Li's Key Lemma 7 \cite{Li}.
```

### involutions edit 6

Old:

```latex
some objects. COMPUTED in the referee's ray drawings: with $m-1$ marks
the count is zero on all 880 paired roots through 14 vertices; with $m+1$
it is zero on 57 of them, versus 78 in the original author's drawings.
These higher-order counts depend on the rays.
```

New:

```latex
some objects. In computed examples with one generic family of ray
drawings, with $m-1$ marks the count is zero on all 880 paired roots with
at most 14 vertices, as it must be; with $m+1$ marks it is zero on 57 of
them, and on 78 with another family of drawings.
These higher-order counts depend on the rays.
```

### involutions edit 7

Old:

```latex
The marked construction in \emph{A constructive proof},
Section 5.1, starts
```

New:

```latex
The marked construction in \emph{A constructive proof} \cite{trees},
Section 5.1, starts
```

### involutions edit 8

Old:

```latex
The project's dependency audit of Li's note
(\texttt{research/2026-11-14\_fable\_dependency-graph/audit-li.md},
items L-F5 and L-F6) first identified these steps and sketched them.
```

New:

```latex
An audit of Li's note made for this project first identified these
steps and sketched them.
```

### involutions edit 9

Old:

```latex
Concrete pairs
and their images are recorded in \texttt{witnesses.json}.
```

New:

```latex
Concrete pairs
and their images are recorded in \texttt{witnesses.json}, one of the
verification data files listed in the README beside this note.
```

### involutions edit 10

Old:

```latex
All statements in the preceding proof are PROVED-HERE, with their source
attributions detailed in \texttt{STATUS.md}. The disk identity and first
cancellation are LIT in OpenAI Lemmas 4.1 and 5.2. The two geometric maps
are LIT in Li's note; their complete multi-mark verifications are written
here.
```

New:

```latex
Every statement of the preceding proof is proved in full here; the file
\texttt{STATUS.md} beside this note gives the source of each. The disk
identity and the first cancellation are OpenAI's Lemmas 4.1 and 5.2. The two
geometric maps are in Li's note; their complete multi-mark verifications are
written here.
```

### involutions edit 11

Old:

```latex
The height proof in the project's main paper (Section 4) measures
```

New:

```latex
The height proof in the main paper (Section 4) measures
```

### involutions edit 12

Old:

```latex
while the height $\omega$ of
the project's main paper rises
```

New:

```latex
while the height $\omega$ of
the main paper rises
```

### involutions edit 13

Old:

```latex
coefficient of the refereed height polynomial with unit charge
```

New:

```latex
coefficient of the height polynomial with unit charge
```

### involutions edit 14

Old:

```latex
COMPUTED. The independent verifier checks all roots of all 55 unrooted
classes
```

New:

```latex
We also checked the construction by computer. A first program checks
all roots of all 55 unrooted classes
```

### involutions edit 15

Old:

```latex
Path lengths depend on the drawing: an independent census with a
different generic direction finds
```

New:

```latex
Path lengths depend on the drawing: a census with a
different generic direction finds
```

### involutions edit 16

Old:

```latex
The revision verifier also checks all these roots with two breadth-first
face-path trees,
```

New:

```latex
A second program checks all these roots with two breadth-first
face-path trees,
```

### involutions edit 17

Old:

```latex
the turn-sign rules, the corrected coefficient,
and agreement
```

New:

```latex
the turn-sign rules, the coefficient formula above,
and agreement
```

### involutions edit 18

Old:

```latex
The code and raw outputs are in
\texttt{research/2026-11-14\_sol\_involutions-revision/}.
A second referee's code, written from the text alone, reproduces every
count in this paragraph in the same encoding. It repeats all checks of
the face-path version with a depth-first tree, a random spanning tree,
and independent random simple paths that form no tree; see
\texttt{research/2026-11-14\_fable\_referee-involutions-v2/}.
```

New:

```latex
A third program, written from the text of this note alone, reproduces
every count in this paragraph in the same encoding. It repeats all checks
of the face-path version with a depth-first tree, a random spanning tree,
and independent random simple paths that form no tree. The code, commands
and raw outputs of all three programs are listed in the README beside this
note.
```

### involutions edit 19

Old:

```latex
An additional comparison computes the existing integer-weight polynomial's
coefficients directly at $z=1$ on all 880 paired roots. Lower coefficients
vanish and the absolute lowest coefficient agrees in every case. This check
uses the existing lab only as an external comparator, not to implement our maps.
```

New:

```latex
A further comparison computes, on all 880 paired roots, the coefficients
of the integer-weight polynomial of a separate implementation at $z=1$.
Lower coefficients vanish and the absolute lowest coefficient agrees in
every case. That implementation serves only as an external comparator; it
does not implement our maps.
```

### involutions edit 20

Old:

```latex
\section{A completely listed example}
The current project example is \texttt{paper/figures/running.json},
with outer face 4 and roots $0,4,5$. The requested older name
\texttt{example.json} is absent. We copy the current input into this folder.
```

New:

```latex
\section{A completely listed example}\label{example}
The example is the main paper's running example, stored as
\texttt{paper/figures/running.json}, with outer face 4 and roots $0,4,5$;
a copy is kept beside this note.
```

### involutions edit 21

Old:

```latex
The project's Li replay (\texttt{workings/barnette\_lab}) uses the same
recipe
```

New:

```latex
A separate implementation of Li's construction uses the same
recipe
```

### involutions edit 22

Old:

```latex
A token $w:t$ means the white face with ID $w$ and the selected spoke in
black face $t$. Object and pair IDs start at zero. The two mark entries
form a set, not an ordered list.
```

New:

```latex
A token $w:t$ means the white face with ID $w$ and the selected spoke in
black face $t$. Object and pair IDs start at zero. The two mark entries
form a set, not an ordered list. Figures~\ref{fig:marked}
and~\ref{fig:second} show two of these objects and one move of the second
map. Figure~\ref{fig:first} shows the first map on a smaller
triangulation.
```

### involutions edit 4a

The sentence on good states came before the main paper was introduced. Edits 3 and 4 are combined into this final text, which also lets the path break (the first version caused a 37pt overfull line).

Old (after edits 3 and 4):

```latex
Its second state is a good state in the sense of the main paper, by Lemma~4.2 there.

This note accompanies \emph{The proof of Barnette's conjecture: an
exposition} (\texttt{paper/main/barnette.pdf} in the same repository), called
the main paper below.
Through that Lemma~4.2, Theorem~\ref{main} is its Proposition~4.8. The proof
```

New:

```latex
This note accompanies \emph{The proof of Barnette's conjecture: an
exposition}, called the main paper below, which is
\nolinkurl{paper/main/barnette.pdf} in the same repository.
The second state of a good pair is a good state in the sense of the main
paper, by its Lemma~4.2, and through that lemma Theorem~\ref{main} is its
Proposition~4.8. The proof
```
