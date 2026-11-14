# Ready-to-apply source edits

All pairs below are should-fix items. No must-fix change to the proof in barnette.tex was found. The must-fix bibliography residue is recorded separately in PROOFREAD.md because it is generated from refs.bib, not a unique string in barnette.tex. Do not replace the bibliography command to address it.

Locations refer to source.tex and the 20-page PDF identified in manifest.json. Each old string occurs exactly once in that source. Apply S4 and S5 together.

## S1. Page 6, source line 332

Clarify the scope of necessity. Goodness is necessary for Y_s to be a tree, but not for a state to come from an acyclic selection.

Old:
```tex
The condition is sufficient for what follows and it is not necessary: the state that Lemma~\ref{lem:selections-give-states} reads off an acyclic selection need not satisfy it (Section~\ref{sec:remarks}).
```

New:
```tex
This condition is sufficient for recovering an acyclic selection, but not every state obtained from an acyclic selection satisfies it (Section~\ref{sec:remarks}).
```

## S2. Page 9, source line 494

The existence assertion needs the hypothesis of Proposition 4.8.

Old:
```tex
This section shows that one exists, by a count in four steps.
```

New:
```tex
This section shows that one exists whenever a pair exists, by a count in four steps.
```

## S3. Page 9, source line 508

Figure 7 currently appears on page 9 but is first cited in body text on page 10.

Old:
```tex
For a pair we write $u(t)$ for the third corner of $t$.
```

New:
```tex
For a pair we write $u(t)$ for the third corner of $t$ (Figure~\ref{fig:localpair}).
```

## S4. Page 18, source line 1006

P was defined as edges of T; the complement of the Hamiltonian cycle is edges of G.

Old:
```tex
If $s_C$ is good, the complement $P$ of $\mathcal{C}$ avoids $S_{s_C}$, because its side in each $t\in A$ contains $s_C(t)$ and its side in $t_0$ is $e_0$.
```

New:
```tex
If $s_C$ is good, let $P$ be the set of edges of $\T$ crossing the edges of $G$ outside $\mathcal{C}$. Then $P$ avoids $S_{s_C}$, because its side in each $t\in A$ contains $s_C(t)$ and its side in $t_0$ is $e_0$.
```

## S5. Page 18, source line 1007

Use the dual-edge notation for perfect matchings of Y_s.

Old:
```tex
Thus $P$ and $P_{s_C}$ are perfect matchings of the tree $Y_{s_C}$, and a tree has at most one perfect matching, so $P=P_{s_C}$.
```

New:
```tex
Thus $P^*$ and $P_{s_C}^*$ are perfect matchings of the tree $Y_{s_C}$, and a tree has at most one perfect matching, so $P=P_{s_C}$.
```

## S6. Page 19, source line 1054

Define the summation range and c(D) before the polynomial display.

Old:
```tex
Grouping by the undirected cycles of $D$ as in Proposition~\ref{prop:good},
```

New:
```tex
Let $D$ range over the covers and let $c(D)$ be the number of cycles in $D$. Grouping by covers as in Proposition~\ref{prop:good},
```

## S7. Page 19, source line 1084

Avoid attributing an intention to Li; describe the mathematical relationship.

Old:
```tex
It writes out in full the argument that Li \cite{Li2026} intended for Proposition~\ref{prop:good}, with marked crossings in place of the power $\omega^m$, and it is a term-by-term unpacking of Lemmas~\ref{lem:cancel}, \ref{lem:height} and~\ref{lem:difference} for one particular height.
```

New:
```tex
It gives a version of Li's argument \cite{Li2026} for Proposition~\ref{prop:good}, with marked crossings in place of the power $\omega^m$, and unpacks Lemmas~\ref{lem:cancel}, \ref{lem:height} and~\ref{lem:difference} term by term for one particular height.
```
