# Referee report on draft A: mathematics

Summary.
1. The route closes. Verdict FOLLOWS, for Theorem 1 as stated (Hamiltonian cycle avoiding any edge). No failing node.
2. Three text defects sit on the route and each needs a one-sentence repair: Lemma 4's second sentence is false without the partner hypothesis (N4); the reduction (3)⇔(4) gives a wrong instruction about t0 (N5b, inherited verbatim from OpenAI); Lemma 8 never says why y0 is outside the disk (N12c).
3. Lemma 8 cites "the outdegree count of Lemma 4" for P0. That lemma is about Q_s and a partner, not P0 and s. The bridge is one sentence (N12d).
4. Every number in the worked examples recomputes. The one imprecise claim is "the other group contributes a nonnegative integer": it contributes exactly 0 (COMPUTED).
5. One simplification is available and verified: ε(r,s) = ∏_t δ(r(t), s(t)). It removes J, the integrality paragraph and the identity δ(u,s) − δ(r,s) = 2δ(r,u) (PROVED-HERE below, COMPUTED on 196 pairs).

Status tags follow `research/BRIEF.md`. I did this audit before reading the author's `AUDIT.md`. The comparison is at the end.

## 1. Audit boundary

**Conclusion C0 (Theorem 1).** For every finite simple cubic bipartite planar 3-vertex-connected graph G and every edge e of G, G has a Hamiltonian cycle avoiding e.

**Source in scope.** `paper/draft-A/barnette.tex` at commit d76deee (the version that built `barnette.pdf`), Sections 1–6 and the proof of Theorem 1. Figures are not premises. Citations to OpenAI, Li, the constructive paper and the project note are provenance, not support: each step is checked on its own.

**Accepted primitives.** Euler's formula for connected plane graphs and for a triangulated closed disk; the Jordan curve theorem and the exit/entrance intersection count of a simple closed curve with a path; integral max-flow/min-cut (Ford–Fulkerson), whose conclusion I check is exactly what is used; elementary counting; the existence of generic polygonal paths in the plane avoiding finitely many points.

## 2. Obligation graph

All groups are AND groups. The draft supplies one route to each claim. Cases (separating triangle or not) are an AND with exhaustiveness.

```text
C0  Theorem 1                         <- R0: N1, N2, C3, N13
N2  Lemma 2 (tree/cotree)            <- R2: contraction, Euler count
C3  Prop 3 (prescribed induced trees) <- R3 induction on |V(T)|: N14 (separator case), C3a (no separator), exhaustiveness
C3a no-separator case                 <- R3a: N3, N5, C7, N11, N12
C7  Prop 7 (pair => forest pair)      <- R7: N6, N8, N9, N10
N3  counts |A| = |X| = n               <- Euler + side count
N4  Lemma 4 (components of Q_s)       <- outdegree count, needs a partner
N5  Lemma 5 (pair exists)             <- R5: N5a flow, N5b (3)<=>(4), N5c component density
N6  Lemma 6 (disk identity)           <- R6: N6a B = I + l, N6b edge count, N6c Euler
N8  Q_s-reversal cancels               <- R8: N4, N6, local delta identity, s-only choice
N9  height increment (10)             <- R9: N9a spoke-route curve simple, N9b slide, N9c crossing count
N10 nonvanishing of the height product <- R10: N6 (white face inside), N9, inclusion-exclusion
N11 recovery gives one side per face   <- R11: N4, N2 on H, rooted white tree
N12 Lemma 8 (P two induced trees)      <- R12: N12a directed cycle, N6, N12b pairing, N12c y0/t0 outside, N12d root count, N12e Jordan
N13 dual simplicity and colouring      <- cut argument, Jordan, cubicity
N14 gluing                              <- cap colour, induction twice, union of trees
```

No cycle: N6 uses only the state bijection; N9 uses only topology; N12 uses N6 with the state s, not C7.

## 3. Findings, by node

### N1, N13. Set-up and dual simplicity. Discharged.

The cut argument (a singleton has 3 crossing edges, an adjacent or nonadjacent pair at least 4, so each side of a ≤2-edge cut has ≥3 vertices) is correct. A dual loop or parallel pair gives a Jordan curve meeting one or two primal edges, with both sides nonempty because each crossed edge has its endpoints on opposite sides. The draft omits that last clause ("both sides nonempty"); OpenAI includes it. Minor.

### N2. Lemma 2. Discharged.

Correct; used on T (N0/C0) and on H (N11). Both are simple connected sphere graphs.

### N4. Lemma 4. Too strong as written; the route only uses the true weaker statement.

The second sentence, "If Q_s is a forest, it has three components, one at each root, and s has exactly one partner", is read under no hypothesis. It is false in that reading: a forest Q_s whose component contains two roots (and another component none) has no partner. The proof uses the partner throughout. Weaker supported statement: *if s has a partner and Q_s is a forest, then ...*. Every consumer (§5 ¶1, N11) invokes it with a partner present, so the route uses only the weaker statement. Classification: `too strong` for the printed statement; the route edge is discharged. **Repair:** EDITS.md E5.

### N5. Lemma 5. Discharged; one sentence is wrong as an instruction.

- N5a. The cut capacity and the passage from a 2n flow to two disjoint perfect matchings are correct. Ford–Fulkerson gives integrality; the extra residual-path paragraph is redundant (both OpenAI and the draft include it).
- N5b. "Include t0 in the sum with contribution zero." The equivalence (3)⇔(4) holds exactly when b(U) *counts t0* (t0 ⊂ U always). Derivation: with j = |V(t) ∩ U|, min(2, |V(t) ∩ S|) = 2 − (#induced sides of t) + [j = 3]. Summing over A, and adding t0's 3 sides and its 1 to both counts, (3) becomes e(U) − 3 − (b(U) − 1) ≤ 2|U| − 6, i.e. (4). So t0 contributes 3 − 1 = 2 to Σ(induced sides − [j=3]) and 0 to the shortfall sum. The printed sentence does not say which sum. A reader cannot verify (3)⇔(4) from the text. The draft copies the sentence from OpenAI §3. `COMPUTED`: (3)⇔(4) with t0 counted in b(U), for all 1024 subsets S ⊆ X of the running example (`check_examples.py`, key `eq3_iff_eq4_all_S_with_t0_in_b`). Classification: side condition, discharged after the fix in E9.
- N5c. Component bound. The only use of "no separating triangle" is "every triangular face of K is an actual face of T". Correct. The signed side count |b′ − w′| ≤ d − 4 (d = 4: sum ≡ 0 mod 2 and mod 3 gives 0; d = 5: sum ±3; d ≥ 6: d/3 ≤ d − 4) and the Euler chain to m − b ≤ 2p − 4 are correct. The root-component case p = 3 and the weak bound m − b ≤ 2p for other components are correct.

### N6. Lemma 6 (disk identity). Discharged.

B = I + ℓ: each interior vertex is r(t) for a face t inside; each boundary vertex v is r(t) for the face t of its outgoing cycle edge, inside exactly when that edge has black inside; conversely a black face inside has r(t) in the closed disk, and if r(t) is on C, its chosen edge is the cycle edge out of r(t) (r is injective). The edge count E_d = 3B + h − ℓ = 3W + ℓ and Euler give W − B = 1, h − 2ℓ = 3, δ-sum ∓3. All correct.

Notation: B (face count) collides with B (incidence graph). The draft patches this with a sentence in the proof. Not a mathematical defect.

### N7. Sign ε. Discharged; a simpler equivalent definition exists.

J = #cw − #ccw by N6; c ≡ n (mod 2) since cycle lengths are odd; so (n + J)/2 is an integer. Correct.

`PROVED-HERE`. **ε(r,s) = ∏_{t∈A} δ(r(t), s(t)).** Per cycle C of D of length h: the δ-values are ±1 with sum −3 (ccw) or +3 (cw), so the number of −1's is (h+3)/2 or (h−3)/2. The draft's exponent (n + J)/2 splits per cycle as (h − 1)/2 (ccw) or (h + 1)/2 (cw). The differences are 2 and −2, both even. So the two signs agree. With this definition the Q_s-reversal sign flip is immediate: in each changed face δ(u,s) = −δ(r,s) (the three directed edges r→s, s→u, u→r run the same way round t, so δ(r,s) = δ(s,u) = −δ(u,s)), so ε flips by (−1)^{|K|}, and |K| is odd by N6. `COMPUTED`: equality on all pairs of both examples and on 192 pairs of `barnette_lab.core.generated(12)` with every black outer face (key `eps_prod_delta_family`). The same observation is in `research/2026-11-14_fable_referee-determinants/SIGNIFICANCE.md` §2 (Step 1). The nonvanishing step still needs the disk identity's value −3 (not just parity) to give all minimum groups one sign; with ε = ∏δ the group sign is (−1)^{(n−c)/2}, the same as in (13).

### N8. Q_s-reversal cancellation. Discharged; one clause missing.

K is chosen from s alone and is directed under every partner (outdegree ≤ 1). Replacing r(t) by u(t) on K's faces gives a fixed-point-free involution on partners of s. The local identity δ(u,s) − δ(r,s) = 2δ(r,u) is correct. "Lemma 6 on K therefore gives J(r′,s) − J(r,s) = ±2": the lemma is applied to the state r with chosen edges r(t) → u(t) on K's faces (any choice elsewhere). The text does not say which state and which edges; a reader who has just seen Lemma 6 used on D may misapply it. Discharged; clarify (E10, which also states the Lemma 6 call).

### N9. Height increment (10). Discharged.

The change at a face is κ_w(t, v′) − κ_w(t, v), the crossing count of v → c_t → v′. The spoke routes form a simple closed curve (distinct centres, disjoint spoke interiors, distinct cycle vertices). The sector between an edge and its two spokes lies in the black face t, contains no white face and excludes the third corner, so sliding preserves orientation and the set of enclosed white faces. A ccw simple curve meets an outward path with signed count +1 when the path starts inside, 0 when it starts outside. With "spoke crosses γ_w from right to left = +1", a ccw exit is +1. `COMPUTED`: (10) holds for every white face and every pair in the group of D(r,s) on both examples, with heights computed literally from the definition (straight rays, two directions, signed spoke crossings; keys `height_change_eq10_holds_on_group`).

### N10. Nonvanishing. Discharged.

m exists (a pair exists, finitely many), m ≥ 1 (n ≥ 1). Witness faces exist by N6 (W ≥ 1). The Boolean expansion is correct: a monomial survives only if φ is onto the c cycles; impossible for c > m; for c = m it forces a bijection; the sign (−1)^{(n+m)/2 + m} = (−1)^{(n−m)/2} is common. D* contributes ≥ 1. With (8), some forest pair has a nonzero term. Correct.

### N11. Recovery. Discharged.

H is connected; its faces are the white triangles. Deleting the spokes (t, s(t)) leaves subdivided Q_s plus the three outer spokes, a spanning tree of H because Q_s's three components contain one root each (N4 with partner r). Lemma 2 gives the white tree W_s. Rooting at y0 and assigning each edge to its far endpoint gives every white face except y0 one parent edge; the selected side of t is the side through s(t) bordering that face; each selected side borders exactly one white face, so each white face other than y0 gets exactly one side; y0 gets e0. Correct.

Note for exposition: P takes in t the side *through* s(t); Q_s took the side *opposite* s(t). The draft does not flag the switch.

### N12. Lemma 8. Discharged; two unstated bridges.

- N12a. Directed P0 (out of s(t)) has outdegree 1 at nonroots and 0 at roots, so a cycle is directed. Correct.
- N12b. Pairing: P gives a perfect matching between black and white faces (one selected side per face, each side has one face of each colour). Inside the disk the unmatched-to-inside faces are exactly the inner faces of the boundary edges, ℓ black and h − ℓ white, so B − ℓ = W − (h − ℓ), W − B = 3, contradicting N6. Correct.
- N12c. **Unstated:** t0 and y0 are matched to each other through e0 ∉ P0. The count needs both outside the disk. t0 is the unbounded face. y0 has the two roots of e0 as corners, and the closed disk contains no root (N6 proof). So y0 is outside. One clause; classification side condition, discharged by N6's proof.
- N12d. "The outdegree count of Lemma 4 gives one root in each component of P0." Lemma 4 is about Q_s oriented by a partner r. Here the graph is P0 oriented out of s. The *argument* (v − a edges ≥ v − 1, so a ≤ 1; three roots, n edges on n + 3 vertices, so three components with one root each) transfers verbatim. Classification: route switch, bridged by repeating one sentence (E14). OpenAI writes "the same component count used for Q_s".
- N12e. Jordan-curve identification of the two classes. Correct, including "both sides contain vertices" and "two components, two sides".

### N14. Gluing. Discharged.

Capped pieces are simple, have ≥ 4 vertices and fewer than T. The cap colour is forced by the three-sign argument. The second induction uses Proposition 3 with the cap (possibly white) as distinguished face; Proposition 3 allows any face. The trees meet in a vertex or an edge; union is a tree by counting; induced because no edge joins the open sides. Correct.

### C0. Proof of Theorem 1. Discharged.

## 4. Worked examples (COMPUTED)

Script `research/2026-11-14_opus_review-draft-A/check_examples.py`, output `check_examples.json`, command `python research/2026-11-14_opus_review-draft-A/check_examples.py` from the repository root. Written independently of the author's `examples.py`; orientation-dependent quantities are computed from the oriented face triples in `paper/figures/{octahedron,running}.json` and a Tutte straight-line embedding with the figures' root angles (the shared layout coordinates are not a straight-line embedding: some faces have inconsistent orientation in them). `barnette_lab` is used only for orientation-free cross-checks and recovery.

| Claim in the draft | Recomputed | Verdict |
| --- | --- | --- |
| Cube: r = (3,4,5), s = (5,3,4) a pair; Q_s = {13, 24, 05}; both Q forests | yes; 2 states, 2 pairs, both forest | correct |
| Cube: D one triangle enclosing y3; reversing it raises h_s(y3) by one | D(r,s) = 3→5→4 clockwise, encloses only y3; h_s(y3) = −1, h_r(y3) = 0 | correct |
| Cube: recovery table, induced trees {0,1,4}, {2,3,5}, cycle t0,y2,t2,y3,t3,y0,t1,y1 | identical (lab recovery, translated names) | correct |
| Table (2): r, s states, a pair; 18, 19, 89 a cycle of Q_s; Q_r a forest | yes; Q_r components {0,1,3,7}, {2,4,8,9,10,11}, {5,6,12} | correct |
| D(r,s): 1,2,3,9,10,11,6 ccw; 8,7,12 cw | δ-sums −3 and +3 | correct |
| Long cycle: B = 5, W = 6, I = 3 (7, 8, 12), h = 7, ℓ = 2 | identical | correct |
| K = 8,1,9; r changes at a7, a9, a21 from (8,1,9) to (1,9,8); J = 0, −2; signs −1, +1 | identical; D(r′,s) has cycles 1,7,12,8,10,11,6 and 2,3,9, both ccw | correct |
| 8 pairs, two groups of four, 6 forest, 2 cyclic, m = 2 | identical; each group has 3 forest pairs and 1 cyclic | correct |
| w1 = 239 inside the long cycle, w2 = 78·12 inside both | identical | correct |
| Four-term difference = 1 | b1 = 0, b2 = −1; increments as stated; value 1 | correct |
| "The other group contributes a nonnegative integer with the same overall sign" | it contributes **0** | true but uninformative; say 0 (E17) |
| Recovery with r: Figure 7, cycle through 22 faces | classes {0,2,4,6,7,8} and {1,3,5,9,10,11,12}; cycle length 22 | correct |

## 5. Dependency table

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | Theorem 1: Hamiltonian cycle avoiding any e | root | R0 | root | N1, N2, C3, N13 | discharged |
| N1 | G finite simple cubic bipartite planar 3-connected; e ∈ E(G) | C0 | R0 | hypothesis | Theorem 1 | discharged |
| N13 | T = G* simple triangulation, ≥ 4 vertices, properly face-coloured | C0, C3 | R0 | algebraic/logical step | cut sizes, Jordan, cubicity, Euler | discharged |
| N2 | complement of spanning tree/forest dualizes to spanning tree/connected subgraph | C0, N11, N12 | R2 | algebraic/logical step | contraction, Euler | discharged |
| C3 | Prop 3 for every simple coloured triangulation, any face, any side | C0 | R3 | major claim | C3a, N14, exhaustiveness | discharged |
| C3a | Prop 3 when no separating triangle | C3 | R3a | major claim | N3, N5, C7, N11, N12 | discharged |
| N3 | k white faces, 3k edges, k+2 vertices; \|A\| = \|X\| = n | C3a, N5 | R3a | algebraic/logical step | side count, Euler | discharged |
| N4 | if s has a partner: components of Q_s are rooted trees or rootless unicycles; if also Q_s forest, three components, unique partner | N11, §5 ¶1 | R4 | too strong (printed without the partner hypothesis in sentence 2) | outdegree count | discharged in the weaker form the route uses |
| N5 | Lemma 5: no separating triangle ⇒ a pair exists | C3a | R5 | major claim | N5a–N5c | discharged |
| N5a | flow value 2n ⇒ two disjoint perfect matchings of B | N5 | R5 | named theorem | integral max-flow/min-cut, cut capacity | discharged |
| N5b | (3) ⇔ (4), with t0 counted in b(U) | N5 | R5 | side condition | derivation in §3; COMPUTED on running example | discharged; printed instruction about t0 unclear |
| N5c | e(U) − b(U) ≤ 2\|U\| − 4 via components | N5 | R5 | algebraic/logical step | no-separating-triangle face test, signed side count, Euler | discharged |
| N6 | Lemma 6: W = B + 1, h − 2ℓ = 3, δ-sum ∓3 | N7, N8, N10, N12 | R6 | major claim | N6a–N6c | discharged |
| N6a | B = I + ℓ | N6 | R6 | algebraic/logical step | state bijection, at most one chosen edge per face | discharged |
| N6b | E_d = 3B + h − ℓ = 3W + ℓ | N6 | R6 | algebraic/logical step | one black, one white face per edge | discharged |
| N6c | (I + h) − E_d + B + W = 1 | N6 | R6 | named theorem | Euler for a closed disk | discharged |
| N7 | (n + J)/2 ∈ Z; J = #cw − #ccw | N8, N10 | R7 | algebraic/logical step | N6, odd lengths | discharged |
| C7 | Prop 7: a pair exists ⇒ a forest pair exists | C3a | R7 | major claim | N8, N10 | discharged |
| N8 | Σ over pairs of ε F(s) = Σ over forest pairs | C7 | R8 | major claim | N4 (directedness), N6 on (r, r→u), local δ identity, s-only choice | discharged; state/edges of the Lemma 6 call unstated |
| N9 | h_{s_U}(w) = h_{s−}(w) + Σ_{C∈U} 1[w ∈ In(C)] | N10 | R9 | major claim | spoke-route curve simple, sector slide, crossing count | discharged; COMPUTED on examples |
| N10 | Σ ε F ≠ 0 for F = ∏ h_s(w_i) | C7 | R10 | major claim | N6 (witnesses), N9, inclusion–exclusion, common sign | discharged |
| N11 | forest pair ⇒ P with exactly one side per face | C3a | R11 | major claim | N4 with partner, N2 on H, rooted W_s | discharged |
| N12a | a cycle of P0 is directed | N12 | R12 | algebraic/logical step | outdegree ≤ 1 out of s | discharged |
| N12b | boundary pairing gives W − B = 3 | N12 | R12 | algebraic/logical step | P is a black–white perfect matching of faces | discharged |
| N12c | t0 and y0 lie outside the disk | N12b | R12 | side condition | N6 proof (no root in closed disk); y0 has two roots | discharged; unstated in text |
| N12d | P0 has three components, one root each | N12 | R12 | route switch (Lemma 4 cited for a different graph) | same outdegree count, repeated | discharged once bridged |
| N12e | Jordan curve classes = two components of P, induced | N12 | R12 | named theorem | Jordan, crossing parity | discharged |
| N12 | Lemma 8 | C3a | R12 | major claim | N12a–N12e, N6 | discharged |
| N14 | gluing across a separating triangle | C3 | R14 | major claim | cap colouring, Prop 3 on both pieces, union count | discharged |

## 6. Comparison with the author's AUDIT.md

The author's audit (`research/2026-11-14_astra_manuscript-A/AUDIT.md`) also reaches FOLLOWS and lists the same skeleton. It accepts "outer contribution zero" at O15 without comment (my N5b), does not flag the missing partner hypothesis in Lemma 4 (N4), does not mention y0 (N12c), and records Lemma 4 as "proved earlier" support for P0 (O41) where the lemma's statement does not apply (N12d). None of these breaks the route. All four are text repairs.

## 7. Verdict

**FOLLOWS.** The proof-supplied route R0 → R3 → (R3a: R5, R7 [R8, R9, R10], R11, R12; R14) discharges C0. No node fails. The decisive nodes are N5c (the only use of "no separating triangle"), N6a (the only place the state bijection enters the disk identity), N9 (heights detect enclosure), N10 (common sign at the minimum) and N12b (acyclicity of P0). The printed text needs four repairs to make the route checkable by a reader without reconstruction: N4 (add the partner hypothesis), N5b (state that b(U) counts t0), N12c (y0 outside the disk), N12d (repeat the outdegree count for P0). This is a bounded audit of the supplied route, `PROVED-HERE` with human review pending.
