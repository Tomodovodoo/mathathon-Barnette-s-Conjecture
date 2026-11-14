# Reverse-Lamport audit of `proofs/sign-free/sign-free.tex`

Fable 5.2, 2026-11-14. Method: `skills/reverse-lamport/SKILL.md`. I am the author of the write-up, so this is a self-audit; the mathematics was refereed before by Opus 5.5 (`research/2026-11-14_opus_referee-rainbow/`). Numbers are those of the PDF.

## Boundary

Conclusions audited: Theorems 3.1, 4.2, 5.3, 6.5, 6.8, 6.9 and Corollaries 4.3, 6.10. Not audited as proofs: Theorem 1.1 (cited), Proposition 7.1 (a computation), Conjecture 7.2 and the quoted ranges of Section 7.

Accepted primitives: Euler's formula for plane graphs with `c` components; the count of edge sides; the Jordan curve theorem for a 3-cycle; tree and cotree duality (exposition Lemma 2.5); Rado's theorem, the Nash-Williams theorem and Edmonds' theorem in the forms quoted in the note; the facts about `T` from Section 1 (simple, every edge has one black and one white face, `|A| = |X| = n`, equally many black and white faces).

## Graph

```text
T3.1 <- R (AND: L2.1, O1 rank of a union, Rado, O2 reduction to connected J, O3 faces of T[U], O4 three counts, O5 identity (3.3), O6 sign analysis, O7 converse count)
T4.2(1) <- (AND: O8 neighbours of x and of c(t) in F_sigma, L4.1)
T4.2(2) <- (AND: L4.1, O9 one arc per face iff bijection)
T4.2(3) <- (AND: O10 distinct t_i, O11 alternating closed trails, O12 edge outside F ends at u(t))
C4.3 <- (AND: T4.2(1), T3.1, O13 Hall count inside a black-inner triangle, O7)
T5.3 <- (AND: L2.3, L5.1, L5.2, O14 excess stays 2 and t stays the only empty face, O15 S_1 has no predecessor, O16 injective map on a finite set, O17 reversal, O18 parity)
L6.3 <- (AND: L6.2, O19 reduction to components, O20 p <= 3, O21 triangular regions)
T6.5 <- (AND: L6.3, (6.1), O22 edge count of M_u, O23 reduction to (6.6), O24 term table, Nash-Williams, O25 both forests are trees and share the doubled spokes, L2.1)
T6.8 <- (AND: L6.3, (6.1), O26 no loops in T/R, O27 two cases for S, Nash-Williams, O28 lift to T)
T6.9 <- (AND: L4.1, O29 splitting = two in-trees, both directions, Edmonds reversed, O30 arcs inside Y, L6.3)
C6.10 <- (AND: T6.9, T6.5, O31 rank of j blocks, Rado)
```

## Obligations

| ID | Obligation | Classification | Support | Status |
| --- | --- | --- | --- | --- |
| L2.1 | `W` is the dual of `H` | algebraic/logical step | hexagon around a white face; face count `n + 1` by Euler; `H` connected because every edge of `T` is in a black face | discharged |
| L2.3 | good iff `F_σ` tree | algebraic/logical step | `F_σ` is `Q_s` subdivided plus a star at the roots; edge count | discharged |
| O1 | rank of `⋃ C_x` is `w(J) - comp(T[J])` | algebraic/logical step | each `C_x` is connected on the white faces at `x`; two share a face iff adjacent | discharged |
| O2 | connected `J` suffice | algebraic/logical step | `w` and `|J|` add over components since a white face meets one component | discharged |
| O3 | faces of `T[U]` are `Φ` and the faces of `T` inside `U` | side condition | both inclusions in the text; the converse inclusion is stated without the open-and-closed sentence of the referee | discharged (the missing sentence is routine; noted) |
| O4 | Euler with `c` components; sides; signed sides | algebraic/logical step | counted in the text | discharged |
| O5 | identity (3.3) | algebraic/logical step | re-derived by hand; holds on 57,901 sets | discharged |
| O6 | `d >= 3`; case table; the case `Δ = ∂t0` | side condition | first draft said "the three faces around `t0` are white", which skipped a step; rewritten: if the far side had no vertex it would be `t0` and the faces in `Φ` along `Δ` would be white | discharged after fix |
| O7 | `W' = I`, `B = I + 1` inside a black-inner triangle | algebraic/logical step | Euler on the disk, sides, signed sides | discharged |
| L4.1 | orientation lemma | algebraic/logical step | every spoke of `F_σ` gets one direction; out-degree one except at `c(t0)`; `2n + 3` spokes | discharged |
| O8 | all faces at `x ∈ X` are in `A`; children of `c(t)` are not roots | side condition | `x` is not a corner of `t0`; roots have parent `c(t0)` | discharged |
| O9 | one arc per face iff `σ'` bijective iff `σ` bijective | algebraic/logical step | degrees in the 2-factor | discharged |
| O10 to O12 | Theorem 4.2(3) | algebraic/logical step | the referee's correction (closed trails) is used; a face has at most one edge of `F' \ F` | discharged |
| O13 | at most `2I - 1` edges at the inner vertices | algebraic/logical step | three faces with one inner corner, `I - 2` others | discharged; uses that the three faces along the sides are distinct, which holds because a face along two sides would be the triangle itself. Not said in the text. |
| L5.1, L5.2 | exchange, reversal | algebraic/logical step | fundamental cycle | discharged |
| O14 | excess and the empty face along the walk | algebraic/logical step | paragraph after Lemma 5.1 | discharged |
| O15 | `S_1` is not in the image of `step` | algebraic/logical step | Lemma 5.2 and the empty face `t` | discharged |
| O16 | no return in the forward orbit | algebraic/logical step | standard; one sentence in the text | discharged |
| O17, O18 | reversal of the walk; no fixed point | algebraic/logical step | as in the referee's proof | discharged |
| L6.2 | Euler identity, bounds on `β` | algebraic/logical step | elimination redone by hand | discharged |
| O19 | reduction to components | algebraic/logical step | the first draft omitted `Σ (2p_K - 2) <= 2|U| - 2`; added | discharged after fix |
| O20 | `p <= 3` | side condition | cases in the text; "`p <= 2` is clear" checked: `1 <= 2 - max(0, ρ - 1)` | discharged |
| O21 | a triangular region is a separating triangle; at most one contains `t0` | side condition | text | discharged |
| O22 to O25 | Theorem 6.5 | algebraic/logical step, named theorem | Nash-Williams is applied to a multigraph without loops; the multigraph form is the referee's remark | discharged |
| O26 to O28 | Theorem 6.8 | algebraic/logical step | `ϱ ∈ S` uses density with three roots | discharged |
| O29 | splitting into rainbow trees = two arc-disjoint in-trees | algebraic/logical step | the first draft had only one direction; the converse sentence was added | discharged after fix |
| O30 | at most `j_t - 1` arcs of `t` inside `Y`, only if `u(t) ∈ Y` | algebraic/logical step | text | discharged |
| O31 | `j` disjoint 2-sets inside two forests have rank at least `j` | algebraic/logical step | text | discharged |

## Statements outside the proofs that I checked separately

- "When `𝓑` has only one 2-factor the conjecture holds": the argument (push the second vertex of a face of load 2 along its cycle) is only sketched in the note. I checked it: the next face has load at most 1 before the move, and the push must meet an empty face before returning, because the other vertex of the starting face points back into it.
- "The exchange leaves the cover exactly when the other arc would close a directed cycle": follows from Lemma 4.1 and the uniqueness in Lemma 5.1.
- Every number in a caption is asserted by `figures/check.py` (61 checks). Two caption facts in my first draft were written before I had the data; one of them (the orbit: which vertex starts in `t`) was wrong and is corrected.

## Not discharged

- The publication year and page range of Schrijver's handbook chapter are from memory.
- Section 7 quotes ranges above 12 vertices from other agents' reports. I recomputed only Proposition 7.1.
- No second reader has gone through the note as written.

## Verdict

FOLLOWS for Theorems 3.1, 4.2, 5.3, 6.5, 6.8, 6.9, Lemmas 2.1, 2.3, 4.1, 5.1, 5.2, 6.2, 6.3 and Corollaries 4.3, 6.10, by the routes in the text, after three fixes made during the audit (O6, O19, O29).

## Unslop pass

No em dashes, sentence-case headings, no bold labels in the note. I removed "at once" style fillers where I saw them and kept the opinions that the note needs (what a proof of Step X would not give; where to look). The abstract's third sentence is long, with three semicolons; I left it because it is the list of results.
