r"""Authoring file for the edit list.

Run from the repository root:
    python research/2026-11-14_fable_coldread-main/code/edits_src.py
It reads paper/main/barnette.tex (read only), writes edits.json (literal old/new strings)
next to EDITS.md, and regenerates EDITS.md from it. The old strings of a few long edits
are taken from the file by line range, so that they are exact; edits.json stores them
literally together with the sha256 of the file they were cut from.

Operations:
  replace: old string (must occur exactly once in the original file) -> new string
  move:    the block from `start` to `end` inclusive (each occurs once) is cut and
           re-inserted immediately after `after` (occurs once); optional `spec`
           replaces the float specifier [tb] of the block.
  instruct: prose instruction, not machine-applied.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parents[1]
TEX = ROOT / "paper" / "main" / "barnette.tex"
src = TEX.read_text(encoding="utf-8")
lines = src.split("\n")


def L(a, b):
    """Lines a..b (1-based, inclusive) of the original file."""
    return "\n".join(lines[a - 1:b])


E = []


def edit(n, title, why, ops):
    E.append({"n": n, "title": title, "why": why, "ops": ops})


def rep(old, new):
    return {"op": "replace", "old": old, "new": new}


def mov(start, end, after, spec=None):
    d = {"op": "move", "start": start, "end": end, "after": after}
    if spec:
        d["spec"] = spec
    return d


def ins(text):
    return {"op": "instruct", "text": text}


# ---------------------------------------------------------------- 1 abstract
edit(1, "Abstract: six sentences, no undefined term",
     "The present abstract uses five terms it does not define (dual triangulation, black triangle, outer triangle, heights, separating triangles) and leaves the inference from the count to the reader. COLD-READ p. 1; review (d).",
     [rep(L(36, 40),
r"""We give a self-contained exposition of OpenAI's 2026 proof of Barnette's conjecture, in the form that every cubic, bipartite, 3-connected planar graph has a Hamiltonian cycle avoiding any given edge.
In a cubic graph the complement of a perfect matching has degree two at every vertex, so the task is to find a perfect matching whose complement is connected.
In the planar dual, a triangulation whose triangles are coloured black and white, a perfect matching is a set of edges containing one side of every triangle, and its complement is connected when the set contains no cycle.
We reduce the search for such a set to a choice of one corner in each black triangle.
A suitable choice exists because of a signed count over pairs of choices, in which the unsuitable ones cancel and a second grouping of the same sum shows that it is not zero.
The avoided edge is what lets an induction cut the triangulation along triangles that are not faces.""")])

# ---------------------------------------------------------------- 2 plan
edit(2, "\"The plan\": one reason per object, and the disk identity named",
     "Sentences 4 to 7 of the plan carry the whole proof in four clauses. The reader cannot say how an edge set chooses a corner, why opposite sides matter, what the second state is for, or why a count proves existence, and the disk identity is absent. The replacement uses the reasons the body gives later (Lemma 3.1, l.259 to 263, Lemma 4.2, l.610). The five steps are complete sentences and can be run into one paragraph if the one-paragraph form is required.",
     [rep(L(63, 70),
r"""The proof takes place in the planar dual $\T$ of $G$.
It has a vertex in each face of $G$ and an edge across each edge of $G$.
Each vertex of $G$ lies in a face of $\T$, which is a triangle because $G$ is cubic, and we colour that triangle black or white by the class of the vertex (Figure~\ref{fig:cube}(b)).
A perfect matching of $G$ is then a set $P$ of edges of $\T$ that contains exactly one side of every triangle.
One side per triangle gives the rest of $G$ degree two.
The rest of $G$ is connected exactly when $P$ contains no cycle, because a cycle of $P$ would separate the triangles inside it from those outside (Section~\ref{sec:picture}).
So we look for a set of edges of $\T$ with one side in every triangle and no cycle, and we want it to contain the edge $e_0$ that crosses $e$.
\begin{enumerate}
\item \emph{Corner choices.}
Let $t_0$ be a black triangle at $e_0$.
A set $P$ as above is a forest, and once $e_0$ is removed each of its trees contains one corner of $t_0$.
Direct the trees towards these corners.
Every other black triangle $t$ has one side in $P$, and that side leaves a corner $s(t)$ of $t$.
Every vertex off $t_0$ is $s(t)$ for exactly one $t$.
A choice of corners with this property is called a \emph{state}, and states are what we search for (Section~\ref{sec:corners}).
\item \emph{From a state back to $P$.}
A set built from a state $s$ uses a side at the chosen corner in each black triangle, so it avoids the opposite side.
Call $s$ \emph{good} if the opposite sides form a forest with one corner of $t_0$ in each tree.
Then the opposite sides and the two sides of $t_0$ other than $e_0$ form a spanning tree of $\T$, the other edges join the triangles into a tree, and that tree leaves only one way to take a side in every triangle (Figure~\ref{fig:cube}(d)--(f)).
The set obtained has no cycle because of one count, the \emph{disk identity}.
It says that a cycle made of sides leaving chosen corners encloses exactly one more white triangle than black.
\item \emph{Two states.}
Take another state $r$ that differs from $s$ in every black triangle.
Then $r(t)$ is an end of the side opposite $s(t)$.
Directing that side out of $r(t)$ gives every vertex off $t_0$ exactly one outgoing side, and then a tree of opposite sides contains exactly one corner of $t_0$.
So $s$ is good as soon as its opposite sides contain no cycle (Section~\ref{sec:pairs}).
\item \emph{A count.}
We cannot point to a pair $(r,s)$ of this kind.
We count instead.
Every pair gets a sign and a weight that depends on $s$ alone.
If the opposite sides of $s$ contain a cycle, reversing it gives another pair with the same $s$ and the opposite sign, so in the sum of sign times weight over all pairs only good states remain.
The same sum can be grouped in a second way.
The arrows from $r(t)$ to $s(t)$ form cycles (Figure~\ref{fig:cube}(c)), and reversing one of them exchanges $r$ and $s$ along it.
With weights that count the white triangles inside these cycles, the second grouping shows that the sum is not zero.
So a good state exists as soon as one pair exists.
The disk identity is used again here.
It makes both reversals change the sign, and it puts a white triangle inside every cycle.
\item \emph{The first pair and the induction.}
A flow argument gives a pair when every $3$-cycle of $\T$ bounds a triangle (Section~\ref{sec:flow}).
Otherwise some $3$-cycle has vertices on both sides; it is called a \emph{separating triangle}.
Cutting $\T$ along it gives two smaller triangulations.
The solution of the first decides which side of the cut the second must use, and this is why Theorem~\ref{thm:main} prescribes an edge (Section~\ref{sec:glue}).
\end{enumerate}""")])

# ---------------------------------------------------------------- 3 history
edit(3, "History paragraph: credit without undefined names",
     "l.84 lists eight objects by names the reader has not met; l.88 to 89 compare the two other expositions in terms defined on pages 9 to 14. Remark 4.10 already makes that comparison where it can be read.",
     [rep(L(84, 84), r"""Every object and every step of the proof below is theirs."""),
      rep(L(87, 89),
r"""Two expositions followed, one by Li \cite{li2026}, who works in $G$, and one in an unsigned manuscript \cite{constructive2026}, which adds an exact criterion for the first step and an enumeration algorithm.
Remark~\ref{rem:other-sums} and Section~\ref{sec:remarks} say how these accounts and ours differ.""")])

# ---------------------------------------------------------------- 4 differences paragraph
edit(4, "Move \"Our account differs from [16]\" from page 2 to Section 7, corrected",
     "The paragraph names spokes, the sliding argument, circulations and the black dual trace, none of which is in this paper; it can only be read after Section 4. Two claims are corrected: the finite difference of Lemma 4.7, not the heights, replaces the exponential sum; the real sign is that of [5]. The new subsection also replaces the process sentence \"Each remark says whether it is proved here, computed, or open.\" and absorbs the source note of l.663.",
     [rep(L(91, 95) + "\n\n", ""),
      rep("Each remark says whether it is proved here, computed, or open.\n",
r"""\subsection*{How this account differs from the sources}
The proof is that of \cite{openai2026}, and its presentation here differs in four places.
The disk identity is stated as ``one more white face than black'', Lemma~\ref{lem:connected} makes Euler's formula applicable to the inside of a cycle, and Proposition~\ref{prop:recover} reads the acyclicity of the selection off that statement.
The sign of a pair is real, as in \cite{constructive2026}, and is written as a product of local signs.
The weights are heights read along paths of faces.
They are the weights that OpenAI construct in the proof of \cite[Lemma~5.3]{openai2026} for one choice of their circulations, and they are Li's counts of crossings between half-rays and matching edges \cite[Section~4]{li2026} taken along fixed paths.
This choice removes the spokes and the sliding argument of \cite[Section~5.3]{openai2026}, and the finite difference of Lemma~\ref{lem:difference} replaces the exponential sum.
The tree of faces $Y_s$ is obtained from the opposite sides by planar duality in $\T$; in $G$ it is Li's black dual trace \cite[Section~6]{li2026} with one extra leaf.
""")])

# ---------------------------------------------------------------- 5 disk identity statement
edit(5, "Lemma 3.8 states its own hypotheses",
     "\"In this situation\" refers to two paragraphs of set-up. The lemma is cited nine times and should be readable alone.",
     [rep(r"In this situation $W=B+1$ and $h=2\ell+3$.",
r"""Let $r$ be a state and $Z$ a directed cycle of chosen sides for $r$, of length $h$.
Let $B$ and $W$ be the numbers of black and white faces inside $Z$, and $\ell$ the number of edges of $Z$ whose black face is inside.
Then $W=B+1$ and $h=2\ell+3$.""")])

# ---------------------------------------------------------------- 6 disk figure
edit(6, "Figure 5 (disk identity) before the lemma, at the sentence that introduces B, W, I, l, h",
     "The figure shows the five numbers on a real cycle and now appears a page after the proof. The reader needs it when the five letters are introduced.",
     [rep(L(381, 381), L(381, 381) + "\n" + r"Figure~\ref{fig:disk} shows these five numbers on a cycle of the example."),
      rep("Figure~\\ref{fig:disk} shows the five numbers on a cycle of the example.\n", ""),
      mov("\\begin{figure}[tb]\n\\centering\n\\includegraphics[width=0.78\\textwidth]{\\FIG 08-disk.pdf}",
          "\\label{fig:disk}\n\\end{figure}",
          r"Figure~\ref{fig:disk} shows these five numbers on a cycle of the example.",
          spec="[!htb]")])

# ---------------------------------------------------------------- 7 selection figure
edit(7, "Figure 6 (tree of faces, selection) at Lemma 3.6",
     "The figure illustrates Lemma 3.6 (p. 6) and Example 3.10 (p. 8) and is printed on p. 9, at the head of Section 4. Its \\FloatBarrier eviction leaves 40 percent of page 8 blank.",
     [rep(r"\begin{lemma}\label{lem:Y}",
r"""Figure~\ref{fig:selected}(a) shows the tree $Y_s$ and the selection of the next lemma for the state $\beta$ of the example.

\begin{lemma}\label{lem:Y}"""),
      mov("\\begin{figure}[tb]\n\\centering\n\\includegraphics[width=0.94\\textwidth]{\\FIG 13-selected.pdf}",
          "\\label{fig:selected}\n\\end{figure}",
          "The side that $t_0$ shares with $y_0$ is $e_0$, and for $t\\in A$ the side shared with its child is not in $Q_s$, so it is one of the two sides at $s(t)$.\n\\end{proof}",
          spec="[!htb]")])

# ---------------------------------------------------------------- 8 section 4 roadmap
edit(8, "Section 4 opens with its four steps; \"second state\" means s only",
     "The section is a four-part argument and never lays it out. The frame (one sum, computed twice, nonzero, hence a good state) is missing from the paper. Also l.474 and l.477 call r \"a second state\" three lines before Definition 4.1 gives that name to s.",
     [rep(L(474, 477),
r"""We do not know how to point to a good state.
This section shows that one exists, by a count in four steps.
A second corner choice turns goodness into the absence of cycles (Lemma~\ref{lem:partner}).
Every pair of choices gets a sign, and the pairs that fail cancel in twos (Lemma~\ref{lem:cancel}).
A weight, built from the white faces that certain cycles enclose, lets the same sum be computed in a second way (Lemma~\ref{lem:height}).
The second computation shows that the sum is not zero (Proposition~\ref{prop:good}), so some pair does not fail.

\subsection*{Why two states}
Goodness asks two things of $Q_s$, no cycle and one root per component.
The second condition concerns whole components.
Another state $r$ that differs from $s$ in every face turns it into the first.
It gives every vertex of $X$ exactly one outgoing edge of $Q_s$, and then a component without a cycle contains exactly one root.""")])

# ---------------------------------------------------------------- 9 split figure 3
panel_b = L(278, 287)
edit(9, "Split Figure 3: the state triangle stays, the pair triangle moves to Definition 4.1; both a third larger",
     "Panel (b) and its caption use pair, partner, D(r,s) and u(t) four pages before they are defined (also raised on draft B). The triangles are 29 mm wide with footnote-size labels in a 159 mm text block. The new caption of (b) states the wedge encoding, which the paper never states.",
     [rep("\\begin{figure}[tb]\n\\centering\n\\begin{tikzpicture}[x=0.075\\textwidth,y=0.075\\textwidth,font=\\footnotesize,line cap=round,line join=round]\n\\coordinate (x) at (0,0);",
          "\\begin{figure}[!htb]\n\\centering\n\\begin{tikzpicture}[x=0.1\\textwidth,y=0.1\\textwidth,font=\\small,line cap=round,line join=round]\n\\coordinate (x) at (0,0);"),
      rep("\\node at (1.2,-0.5) {(a) a state in $t$};\n", ""),
      rep(L(277, 290),
r"""\end{tikzpicture}
\caption{One black triangle $t\in A$. A state chooses the corner $s(t)$ (solid wedge). A selection built from $s$ uses one of the two bold sides at $s(t)$, and the dashed side opposite $s(t)$ is the edge of $Q_s$ in $t$.}"""),
      rep("(Figure~\\ref{fig:local}(a)).", "(Figure~\\ref{fig:local})."),
      rep("For a pair we write $u(t)$ for the third corner of $t$.\n\\end{definition}",
          "For a pair we write $u(t)$ for the third corner of $t$.\n\\end{definition}\n\n\\begin{figure}[!htb]\n\\centering\n"
          + panel_b.replace("x=0.075\\textwidth,y=0.075\\textwidth,font=\\footnotesize", "x=0.1\\textwidth,y=0.1\\textwidth,font=\\small")
          + "\n\\end{tikzpicture}\n"
          + r"""\caption{A pair in one black triangle $t$: the corner $r(t)$ (outlined wedge), the corner $s(t)$ (solid wedge) and the third corner $u(t)$. The arrow $r(t)\to s(t)$ is the edge of $D(r,s)$ in $t$, defined below, and $r$ directs the edge of $Q_s$ from $r(t)$ to $u(t)$ (Lemma~\ref{lem:partner}). In every figure outlined wedges mark the first state of a pair and solid wedges the second.}
\label{fig:localpair}
\end{figure}""")])

# ---------------------------------------------------------------- 10 table 1
edit(10, "Table 1 after Lemma 4.4, where its columns have a meaning",
     "The table floats into the statement of Lemma 4.3 and uses \"sign\", F(s) and \"the sum\" before each is defined.",
     [rep(r"A pair can be changed along a cycle in two ways, which Table~\ref{tab:reversals} sets side by side.",
          r"A pair can be changed along a cycle in two ways."),
      rep(r"a cycle of $Q_s$ & $r$ on its faces & $s$, so $Q_s$ and $F(s)$ & flips & cancelling cyclic $Q_s$\\",
          r"a cycle of $Q_s$ & $r$ on its faces & $s$ and $Q_s$ & flips & cancelling the pairs with cyclic $Q_s$\\"),
      rep(r"a cycle of $D(r,s)$ & $r$ and $s$ on its faces & undirected $D$ & flips & showing the sum is not $0$\\",
          r"a cycle of $D(r,s)$ & $r$ and $s$ on its faces & undirected $D$ & flips & the second grouping of the count\\"),
      rep(r"The product of local signs changes in a computable way under both reversals, and the disk identity makes the number of changed factors odd.",
          "The product of local signs changes in a computable way under both reversals, and the disk identity makes the number of changed factors odd.\nTable~\\ref{tab:reversals} sets the two reversals side by side."),
      mov("\\begin{table}[tb]\n\\centering\n\\begin{tabular}{@{}lllll@{}}",
          "\\label{tab:reversals}\n\\end{table}",
          r"Table~\ref{tab:reversals} sets the two reversals side by side.",
          spec="[!htb]")])

# ---------------------------------------------------------------- 11 cancellation heading
edit(11, "\"Cancellation\": say what is fixed and why a weight F is allowed",
     "The heading is followed at once by a lemma \"for every function F on states\"; the reason for F is one page later (l.610).",
     [rep("\\subsection*{Cancellation}\n\n\\begin{lemma}\\label{lem:cancel}",
r"""\subsection*{Cancellation}
Fix $s$ and let the partner vary.
If $Q_s$ contains a cycle, the first reversal pairs up the partners of $s$ with opposite signs.
The lemma allows a weight $F(s)$ on each term, and the next subsection shows why one is needed.

\begin{lemma}\label{lem:cancel}""")])

# ---------------------------------------------------------------- 12 heights caption
edit(12, "Figure 9 caption: only one panel is \"reversed\"",
     "The caption calls (a) \"the pair obtained from (beta, alpha) by reversing the 7-cycle\" while the subcaption of (b) says \"reversed\". The panels follow Lemma 4.6 (clockwise, then reversed to counterclockwise); the caption should too.",
     [rep("\\begin{figure}[tb]\n\\centering\n\\includegraphics[width=0.94\\textwidth]{\\FIG 17-heights.pdf}",
          "\\begin{figure}[!htb]\n\\centering\n\\includegraphics[width=0.94\\textwidth]{\\FIG 17-heights.pdf}"),
      rep(r"(a) The pair obtained from $(\beta,\alpha)$ by reversing the $7$-cycle, which now runs clockwise.",
          r"(a) A pair whose $7$-cycle runs clockwise."),
      rep(r"(b) The pair $(\beta,\alpha)$, with the $7$-cycle counterclockwise.",
          r"(b) Reversing the $7$-cycle as in Lemma~\ref{lem:height} gives the pair $(\beta,\alpha)$ of Figure~\ref{fig:pair}, where it runs counterclockwise.")])

# ---------------------------------------------------------------- 13 before Lemma 4.6
edit(13, "Say what Lemma 4.6 measures before stating it; drop the source note from the argument",
     "The sentence that carries the intuition (the change of height counts crossings of the path with C) is inside the proof (l.656). The source note of l.663 interrupts the argument and is now in Section 7 (edit 4).",
     [rep(r"\begin{lemma}\label{lem:height}",
r"""Reversing a clockwise cycle $C$ of $D$ raises the height at $y$ by the number of times the path of $y$ leaves the inside of $C$ minus the number of times it enters it.
That number is $1$ when $y$ is inside $C$ and $0$ otherwise.

\begin{lemma}\label{lem:height}"""),
      rep(L(663, 663) + "\n", "")])

# ---------------------------------------------------------------- 14 groupings figure
groupings = r"""\begin{figure}[!htb]
\centering
\begin{tikzpicture}[x=0.185\textwidth,y=1.9cm,font=\footnotesize,
  pair/.style={draw=black!62,line width=.4pt,minimum width=0.16\textwidth,minimum height=1.05cm,align=center,inner sep=2pt},
  bad/.style={pair,fill=bfblack}]
\foreach \i/\o/\e/\w in {0/{cw, cw}/{+}/{-4},1/{cw, ccw}/{-}/{-3},3/{ccw, ccw}/{+}/{3}}
  \node[pair] (a\i) at (\i,1) {\o\\$\eps=\e1$, $\omega=\w$};
\node[bad] (a2) at (2,1) {ccw, cw\\$\eps=-1$, $\omega=2$};
\foreach \i/\o/\e/\w in {0/{cw, cw}/{+}/{-2},1/{cw, ccw}/{-}/{-1},2/{ccw, cw}/{-}/{1}}
  \node[pair] (b\i) at (\i,0) {\o\\$\eps=\e1$, $\omega=\w$};
\node[bad] (b3) at (3,0) {ccw, ccw\\$\eps=+1$, $\omega=2$};
\draw[bfR,line width=1.1pt] (a2.south) -- (b3.north) node[midway,fill=white,inner sep=1.5pt,text=black] {same $s=\alpha$};
\node[anchor=west] at (3.5,1) {$\sum\eps\,\omega^2=12$};
\node[anchor=west] at (3.5,0) {$\sum\eps\,\omega^2=6$};
\end{tikzpicture}
\caption{The eight pairs of the example, grouped in the two ways of this section. Each row is a class of Proposition~\ref{prop:good}, the same undirected cycles of $D$ with their four orientations (the $7$-cycle first, then the triangle). Along a row $\eps$ alternates, $\omega$ moves by the numbers $L$ of enclosed white faces, and $\sum\eps\,\omega^2=2L_1L_2$. The two shaded pairs have the same second state $\alpha$, whose $Q_\alpha$ contains a cycle. They have opposite signs and equal weights, so they cancel as in Lemma~\ref{lem:cancel}. The six other pairs carry the six good states.}
\label{fig:groupings}
\end{figure}

"""
edit(14, "New figure: the same eight pairs grouped in both ways",
     "Section 4 computes one sum twice and no figure or table shows the two groupings together. Table 2 shows the classes; the cancelling couple is hidden in its last column. The data are those of Table 2.",
     [rep(r"\begin{remark}\label{rem:other-sums}", groupings + r"\begin{remark}\label{rem:other-sums}"),
      rep(r"The two pairs with a cycle in $Q_s$ have the same second state $\alpha$ and cancel; the six good states",
          r"The two pairs with a cycle in $Q_s$ have the same second state $\alpha$ and cancel (Figure~\ref{fig:groupings}); the six good states")])

# ---------------------------------------------------------------- 15 why a tree
edit(15, "Say why the faces should form a tree, and that goodness is sufficient only",
     "\"For this graph to be a tree we need the following condition\" gives no reason to want a tree. The reason is at l.896 in the Remarks. The cold reader could not tell that Lemma 3.1 and Definition 3.4 are not converses until page 17.",
     [rep(r"For this graph to be a tree we need the following condition on $s$.",
r"""A tree has at most one perfect matching, found by matching a leaf to its neighbour, removing both and repeating.
So if $Y_s$ is a tree, at most one selection of this kind exists and no choice is left.
For $Y_s$ to be a tree we need the following condition on $s$.
The condition is sufficient for what follows and it is not necessary: the state that Lemma~\ref{lem:selections-give-states} reads off an acyclic selection need not satisfy it (Section~\ref{sec:remarks}).""")])

# ---------------------------------------------------------------- 16 face names
edit(16, "Faces with two-digit corners: separate the corners",
     "The header of the table in Example 3.3 prints 41011, 5611, 6712, 81112, 8910. Same at l.600.",
     [rep(L(299, 299),
          r"t & 0{\cdot}1{\cdot}6 & 0{\cdot}2{\cdot}3 & 1{\cdot}7{\cdot}8 & 1{\cdot}2{\cdot}9 & 3{\cdot}4{\cdot}9 & 4{\cdot}10{\cdot}11 & 5{\cdot}6{\cdot}11 & 6{\cdot}7{\cdot}12 & 8{\cdot}11{\cdot}12 & 8{\cdot}9{\cdot}10\\\hline"),
      rep(r"in the faces $178$, $129$, $89\,10$ from", r"in the faces $1{\cdot}7{\cdot}8$, $1{\cdot}2{\cdot}9$, $8{\cdot}9{\cdot}10$ from")])

# ---------------------------------------------------------------- 17 heading with no text
edit(17, "The heading before Proposition 3.9 gets a sentence and drops \"recovered\"",
     "A run-in heading is followed at once by a proposition. The selection was \"produced\" on p. 6 and is \"recovered\" only in this heading.",
     [rep("\\subsection*{The recovered selection has no cycle}\n\n\\begin{proposition}\\label{prop:recover}",
r"""\subsection*{The selection $P_s$ has no cycle}
A cycle in $P_s$ would be a cycle of chosen sides, so the disk identity fixes the number of white faces it encloses.
The selection itself gives a different number.

\begin{proposition}\label{prop:recover}""")])

# ---------------------------------------------------------------- 18 parenthesis, filler
edit(18, "Remove the apology for the letter r and the sentence \"used four times\"",
     "\"(we will apply this to both states of a pair, which is why it is called r)\" interrupts a definition and does not explain the choice; the lemma is first applied to s. \"One principle about them is used four times\" tells the reader nothing.",
     [rep(r"Let $r$ be a state (we will apply this to both states of a pair, which is why it is called $r$), and suppose",
          r"Let $r$ be a state, and suppose"),
      rep("One principle about them is used four times.\n", "")])

# ---------------------------------------------------------------- 19 dense sentence
edit(19, "Lemma 2.1, proof: one sentence that reads as a statement about degrees",
     "\"One vertex has three edges leaving it, and two vertices have at least four\" means sets of one and two vertices.",
     [rep(r"One vertex has three edges leaving it, and two vertices have at least four, since $G$ is simple.",
          r"If $|U|=1$ then three edges leave $U$, and if $|U|=2$ at least four do, since $G$ is simple.")])

# ---------------------------------------------------------------- 20 pinched
edit(20, "\"no vertex is pinched between the two sides\"",
     "The cold reader could not say what the clause means or what it is for. Its use is in the third count of Lemma 3.8.",
     [rep(r"A vertex strictly inside $Z$ has all its faces inside $Z$, so no vertex is pinched between the two sides.",
          r"We also use that every face at a vertex strictly inside $Z$ lies inside $Z$.")])

# ---------------------------------------------------------------- 21..27 float moves
edit(21, "Figure 2 (the example) at \"The example\", a little wider",
     "Cited on p. 2, printed on p. 4 inside the proof of Lemma 2.5(2).",
     [rep(r"Figure~\ref{fig:dual} shows the example, with $k=11$.", r"In the example $k=11$ (Figure~\ref{fig:dual})."),
      mov("\\begin{figure}[tb]\n\\centering\n\\includegraphics[width=0.55\\textwidth]{\\FIG 03-dual.pdf}",
          "\\label{fig:dual}\n\\end{figure}",
          r"The numbers quoted for the example come from exhaustive enumeration.",
          spec="[!htb]"),
      rep(r"\includegraphics[width=0.55\textwidth]{\FIG 03-dual.pdf}", r"\includegraphics[width=0.62\textwidth]{\FIG 03-dual.pdf}")])

edit(22, "Figure 4 (opposite sides) stays after Example 3.3 and is set there",
     "It now floats between the statement of Lemma 3.5 and its proof.",
     [rep("\\begin{figure}[tb]\n\\centering\n\\includegraphics[width=0.94\\textwidth]{\\FIG 09-Q.pdf}",
          "\\begin{figure}[!htb]\n\\centering\n\\includegraphics[width=0.94\\textwidth]{\\FIG 09-Q.pdf}")])

edit(23, "Figure 7 (the pair and D) is set where it is cited",
     "It now floats, with Table 1, into the statement of Lemma 4.3.",
     [rep("\\begin{figure}[tb]\n\\centering\n\\includegraphics[width=0.94\\textwidth]{\\FIG 07-pair-D.pdf}",
          "\\begin{figure}[!htb]\n\\centering\n\\includegraphics[width=0.94\\textwidth]{\\FIG 07-pair-D.pdf}")])

edit(24, "Figure 8 (cancellation) is set after the remark that cites it",
     "It now floats into the proof of Lemma 4.4.",
     [rep("\\begin{figure}[tb]\n\\centering\n\\includegraphics[width=0.94\\textwidth]{\\FIG 10-cancellation.pdf}",
          "\\begin{figure}[!htb]\n\\centering\n\\includegraphics[width=0.94\\textwidth]{\\FIG 10-cancellation.pdf}")])

edit(25, "Table 2 before Example 4.9, not inside it",
     "The table splits the example across a page break.",
     [mov("\\begin{table}[tb]\n\\centering\n\\begin{tabular}{@{}cccrrl@{}}",
          "\\label{tab:pairs}\n\\end{table}",
          r"Only the classes with the fewest cycles are sure to agree.",
          spec="[!htb]")])

edit(26, "Figure 10 (flow network) at the sentence that cites it",
     "It is cited in the first paragraph of Section 5 and printed inside the proof of Proposition 5.2. The move also breaks the paragraph after the citing sentence, so that the network is described under its picture.",
     [mov("\\begin{figure}[tb]\n\\centering\n\\includegraphics[width=0.70\\textwidth]{\\FIG 06-flow.pdf}",
          "\\label{fig:flow}\n\\end{figure}",
          r"We find such a subgraph as a flow (Figure~\ref{fig:flow}).",
          spec="[!htb]")])

edit(27, "Figure 11 (gluing) at the definition of piece and cap",
     "It is cited after the proof of Theorem 6.2 and printed inside the proof of Lemma 6.1. The reader wants it when pieces and caps are defined.",
     [rep("Figure~\\ref{fig:glue} shows a small case.\n", ""),
      rep(r"The \emph{piece} $\T_{\mathsf{D}}$ consists of the vertices, edges and faces of $\T$ in $\mathsf{D}$, together with one new face, the \emph{cap}, bounded by $\Delta$ on the other side.",
          "The \\emph{piece} $\\T_{\\mathsf{D}}$ consists of the vertices, edges and faces of $\\T$ in $\\mathsf{D}$, together with one new face, the \\emph{cap}, bounded by $\\Delta$ on the other side.\nFigure~\\ref{fig:glue} shows the two pieces of a small example and the gluing of Theorem~\\ref{thm:T}."),
      mov("\\begin{figure}[tb]\n\\centering\n\\includegraphics[width=\\textwidth]{\\FIG 14-gluing.pdf}",
          "\\label{fig:glue}\n\\end{figure}",
          r"Figure~\ref{fig:glue} shows the two pieces of a small example and the gluing of Theorem~\ref{thm:T}.",
          spec="[!htb]")])

# ---------------------------------------------------------------- 28 status tags
edit(28, "Section 7: remove the project's status tags and process sentences",
     "\"(proved; computed)\", \"(proved; literature)\", \"(open)\" and \"we have not checked it\" are a working vocabulary, not the voice of a paper.",
     [rep(r"\subsection*{Which Hamiltonian cycles arise (proved; computed)}", r"\subsection*{Which Hamiltonian cycles arise}"),
      rep(r"\emph{Proved:} $C$ is produced by", r"$C$ is produced by"),
      rep(r"\emph{Computed:} in the example all six such cycles arise.", r"In the example all six such cycles arise."),
      rep(r"\subsection*{Why each hypothesis is needed (proved; literature)}", r"\subsection*{Why each hypothesis is needed}"),
      rep(r"none for another of the same colour (computed).", r"none for another of the same colour, as an enumeration shows."),
      rep(r"\subsection*{The polynomial behind the count (proved)}", r"\subsection*{The polynomial behind the count}"),
      rep(r"\subsection*{No polynomial-time construction is known (open)}", r"\subsection*{No polynomial-time construction is known}"),
      rep(r"times $3^{N/4}$; we have not checked it.", r"times $3^{N/4}$; we do not use it."),
      rep(r"\cite[Corollary~7.2]{openai2026} (literature).", r"\cite[Corollary~7.2]{openai2026}.")])

# ---------------------------------------------------------------- 29 purpose of D
edit(29, "Give D(r,s) its purpose when it is introduced",
     "\"Besides Q_s a pair gives the set D(r,s)\" introduces the second main object of Section 4 with no reason.",
     [rep(r"Besides $Q_s$ a pair gives the set $D(r,s)$ of edges $r(t)\to s(t)$, $t\in A$ (Figure~\ref{fig:local}(b)).",
r"""A pair determines a second set of edges, and it gives the second way of grouping the count.
Let $D(r,s)$ be the set of directed edges $r(t)\to s(t)$, $t\in A$ (Figure~\ref{fig:localpair}).""")])

# ---------------------------------------------------------------- 30 figure 1 caption
edit(30, "Figure 1 caption in words, without D, Q_s, S_s",
     "The caption is ten lines and repeats the plan in symbols that the plan avoids. With the plan of edit 2 it can describe what each panel shows.",
     [rep(L(75, 75),
r"""\caption{The construction on the cube. (a) A subgraph of degree two with two cycles. (b) The dual octahedron $\T$ with black triangles shaded. The outer triangle $t_0$ is black too, as the grey collar shows; its corners $0,1,2$ are hollow and the prescribed side is $e_0=\{0,1\}$. (c) Two states that differ in every black triangle (outlined and solid wedges), and the arrows of step~4 of the plan. (d) A state and the sides opposite its corners (dashed), which form a forest with one corner of $t_0$ in each tree. (e) The avoided edges (bold) form a spanning tree, and the other edges join the triangles into a tree (dash-dotted). (f) The side taken in each triangle (bold), and the Hamiltonian cycle of the cube, which crosses every other edge.}""")])

# ---------------------------------------------------------------- 31 separating triangle
edit(31, "Define \"separating triangle\" where Section 5 first uses it",
     "The only definition in the paper is a clause in the plan on page 1. Proposition 5.2, its proof and Section 6 use the term.",
     [rep(r"\begin{proposition}\label{prop:pair}",
r"""A \emph{separating triangle} of $\T$ is a $3$-cycle of $\T$ with vertices of $\T$ on both of its sides.

\begin{proposition}\label{prop:pair}""")])

# ---------------------------------------------------------------- 32 meaning of (5.3)
edit(32, "Say what inequality (5.3) is",
     "The cold reader followed the algebra and could not say what the inequality means. It is a planar edge count with equality for coloured triangulations (3p - 6 edges, p - 2 black faces).",
     [rep(r"The corners of a black face with all corners in $U$ are pairwise adjacent, so they lie in one component of the graph $\T[U]$ formed by the edges with both ends in $U$.",
r"""This is a planar edge count.
A coloured triangulation with $p$ vertices has $3p-6$ edges and $p-2$ black faces, so it attains equality, and the claim is that no set $U$ does better.
The corners of a black face with all corners in $U$ are pairwise adjacent, so they lie in one component of the graph $\T[U]$ formed by the edges with both ends in $U$.""")])

# ---------------------------------------------------------------- 33 purpose of the general lemma
edit(33, "Say why the duality lemma is about an arbitrary edge set",
     "The reader expects \"P acyclic if and only if the rest of G is a cycle\" and gets a lemma about M and N with no reason. (Every use has M = T; restating the lemma for T is the cleaner fix and touches the whole proof, so it is left as an instruction.)",
     [rep(r"For a plane graph $M$ and $N\subseteq E(M)$ write",
          "We need the answer for two kinds of edge set, a selection here and a spanning tree in Section~\\ref{sec:corners}, so the next lemma is about an arbitrary set $N$ of edges.\nFor a plane graph $M$ and $N\\subseteq E(M)$ write"),
      ins("Optional, larger: state Lemma 2.5 for $\\T$ in place of $M$ (every application has $M=\\T$), which removes two letters and the phrase \"with $M=\\T$ and $N=P$\" at l.213.")])

# ---------------------------------------------------------------- 34 notation
edit(34, "Two letters with two meanings: F and c",
     "F is a directed edge set (Lemma 3.7), a function on states (Lemma 4.5), a face of H (Section 5) and a polynomial (Section 7). c is the third root (l.229) and the number of cycles of D (l.561).",
     [rep("Let $F$ be a set of edges of $\\T$, each directed, such that every vertex has at most one outgoing edge in $F$.\nThen every cycle of $F$ is a directed cycle.\nA component of $F$ with $q$ vertices",
          "Let $\\vec E$ be a set of edges of $\\T$, each directed, such that every vertex has at most one outgoing edge in $\\vec E$.\nThen every cycle of $\\vec E$ is a directed cycle.\nA component of $\\vec E$ with $q$ vertices"),
      ins("Rename the third root from $c$ to $o$ (or name the roots $a_0,a_1,a_2$ with $e_0=a_1a_2$). Occurrences of the root $c$: l.229, l.232, l.246, l.262, l.263, l.295 ($c=5$), l.332, l.346, l.796. Rename the polynomial of Section 7 from $F(w)$ to $\\Pi(w)$ (l.911, l.912, l.915, l.918).")])

# ---------------------------------------------------------------- 35 title, author
edit(35, "Title and author line (decision for the user)",
     "The title names the setting, which OpenAI's paper shares, and does not say the paper is an exposition. There is no author, and the text says \"we\".",
     [rep(r"\title[Barnette's conjecture]{Barnette's conjecture in the dual triangulation}",
          r"\title[Barnette's conjecture]{The proof of Barnette's conjecture: an exposition}"),
      ins("Add an \\author line, or a first-page footnote that says who prepared the exposition and how. The choice is the user's.")])

# ---------------------------------------------------------------- 36..40 figures, prose pass
edit(36, "Regenerate Figure 1 (01-cube)",
     "Six 37 mm disks at 0.78 of the text width; the subcaptions of the first row touch the label \"2\" of the second; (a) and (b) are not tied together; the panel order is not the order of the plan; subcaptions use D, Q_s, S_s, P.",
     [ins("In paper/figures/draw.py: (i) natural width equal to the text width (451 pt), three panels per row; (ii) at least 4 mm between the subcaption of row 1 and the top label of row 2; (iii) in panel (b) draw the cube in thin grey over the octahedron, one cube vertex in each triangle, as Figure 2 does for the example; (iv) order the panels as the plan cites them: (a) two cycles, (b) the dual, (c) a state and its opposite sides, (d) the two trees, (e) the selection and the Hamiltonian cycle, (f) two states and their arrows; (v) word subcaptions: \"a state and its opposite sides\", \"avoided edges and the tree of triangles\", \"one side per triangle, one cycle\", \"two states\"; (vi) explain the double ring in the caption or drop it. Then update the panel letters in the plan (edit 2) and in the caption (edit 30), and set width=\\textwidth at l.74.")])

edit(37, "Regenerate Figure 2 (03-dual)",
     "Labels 6, 11 and 12 cover white vertices of G; the label 9 is far from its vertex; G competes with T.",
     [ins("In paper/figures/draw.py: (i) place every vertex label so that its white backing covers no vertex of G or T (6 up-left, 11 up-right, 12 right, 9 below its vertex, close); (ii) draw G at 0.3 pt in black!35 with smaller vertices, or split into two panels, T alone and T with G; (iii) natural width 0.62 of the text width, so that the paper does not rescale it.")])

edit(38, "Regenerate Figure 10 (06-flow)",
     "Six triangle labels are struck through by the edges to the sink, and the label 12 is overprinted.",
     [ins("In paper/figures/draw.py: (i) put each triangle label to the left of its square, above the incidence lines, or move the sink 15 mm to the right so that the sink edges clear the labels; (ii) write the capacity on one edge of each kind (2, 1, 2) and drop the column headings; (iii) shade the cut for S = {2} that the caption mentions.")])

edit(39, "Regenerate Figures 11(c), 8 and 7",
     "11(c): the inner octahedron is about 6 mm and unlabelled. 8: two full disks that differ in three wedges. 7: panel (a) is panel (b) without arrows; arrowheads are hard to find.",
     [ins("14-gluing: lay out the 9-vertex triangulation with the triangle 3, 4, 5 large (inner vertices 6, 7, 8 labelled as in panel (b)). 10-cancellation: draw a close-up of the faces 1.7.8, 1.2.9, 8.9.10 and the white face 1.8.9, before and after the reversal, at twice the present scale, with the rest of the triangulation omitted or faded. 07-pair-D: one panel at 0.6 of the text width with arrowheads of 6 pt, and a two-item legend (outlined: first state; solid: second state). In all running-example panels move the labels 1, 3, 7, 9, 10 off the wedges.")])

edit(40, "A punctuation pass over the proofs",
     "99 semicolons and 23 colons used as connectors (code/style_counts.py). Most proof sentences have the shape \"X; so Y\".",
     [ins("Turn the semicolon or colon into a full stop at l.109, l.250, l.345, l.346, l.351, l.380, l.386, l.397, l.398, l.406, l.407, l.477 (done in edit 8), l.492, l.493, l.596, l.715, l.870, l.871, l.896, l.903, l.907, l.908. Split l.907 (108 words) at each sentence boundary into a paragraph of its own per hypothesis. Replace l.621, the parenthesis \"(Combinatorially: ...)\", by a sentence that begins \"In combinatorial terms,\". Remove the parentheses at l.900.")])

# ---------------------------------------------------------------- write
out = {
    "source": "paper/main/barnette.tex",
    "sha256": hashlib.sha256(src.encode("utf-8")).hexdigest(),
    "edits": E,
}
(HERE / "edits.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
print("wrote edits.json:", len(E), "edits,", sum(len(e["ops"]) for e in E), "operations")
