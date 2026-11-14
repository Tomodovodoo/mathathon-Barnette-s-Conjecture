# Status of every statement in the sign-free note

Fable 5.2, 2026-11-14. Tags are those of `research/BRIEF.md`. "Referee" means the independent AI referee Opus 5.5 in `research/2026-11-14_opus_referee-rainbow/` (reports `REFEREE-rainbow.md`, `REFEREE-packing.md`, final wordings `INTEGRATION.md`). No human has checked any of this. "Census 6 to 12" is my own run `research/2026-11-14_fable_sign-free-note/code/verify.py 6 12` (output `data/verify_6_12.json`): all 262 choices of `t0` in all Eulerian triangulations with at most 12 vertices, 208 of them with a pair.

## Proved statements

| Note | Statement | Tag | Proved by | Checked by | Verified numerically |
| --- | --- | --- | --- | --- | --- |
| Lemma 2.1 | `W` is the plane dual of `H`; tree and cotree | PROVED-HERE, with LIT for tree-cotree duality (exposition Lemma 2.5) | referee (Fact 0), written out here | me, reverse-Lamport | 440,000 spoke sets, census 6 to 12 |
| Lemma 2.3 | good state = rainbow tree of excess 0 | PROVED-HERE | this note (subdivision argument); the statement is OpenAI's forest state | me | all 1,706 states, census 6 to 12 |
| Theorem 3.1 (Step R) | rainbow tree exists iff no separating triangle with black inner boundary | PROVED-HERE, uses LIT Rado | Fable (`2026-11-14_fable_referee-topology/RAINBOW.md`) | referee, line by line; me | 262 instances, identity (3.3) on 57,901 connected sets, 68 violating sets, all interiors of such triangles |
| Lemma 4.1, Theorem 4.2 (Theorem S, Proposition U) | each rainbow tree lies in one 2-factor; forests of `G_u`; directed cycle iff second 2-factor | PROVED-HERE | Fable | referee (with the fix "closed trails", used here); me | every one of 74,432 rainbow trees and 210 2-factors, all `2^n` selections |
| Corollary 4.3 | pair iff rainbow tree iff no such triangle | PROVED-HERE; first and third also LIT (constructive manuscript, Theorem 1.2) | Fable, Opus (Hall count) | referee; me | 262 instances |
| Lemma 5.1 | unique exchange | PROVED-HERE | Fable | referee; me | 651,072 (tree, vertex) pairs, by brute force over all alternatives |
| Lemma 5.2 | reversal of a step | PROVED-HERE | Fable | referee; me | 325,536 walk states |
| Theorem 5.3 | `n` involutions without fixed point; the number of good states is even | PROVED-HERE | Fable | referee; me | 5,052 evaluations of `ι_t`; longest walk 10 states |
| Lemma 6.2, Lemma 6.3 | Euler identity, density for every vertex set | PROVED-HERE | Opus (`2026-11-14_opus_two-tree-packing/PROOFS.md` Lemmas 1.1, 1.2) | referee; me | every nonempty vertex set in 262 instances; holds in the 208, fails in the 54 |
| Theorem 6.5 | two spanning trees of `W` for every deleted-corner map | PROVED-HERE, uses LIT Nash-Williams | Opus | referee; me | 210 covers and all maps for `n <= 7`, 20 random maps otherwise; 82,118 maps, explicit split found each time |
| Remark 6.7 | the hypothesis is needed | PROVED-HERE | Opus (Proposition 2.3) | referee; me | 68 maps, Nash-Williams count violated |
| Theorem 6.8 | two rooted spanning forests of `T`; `Q_r ∪ Q_s` splits | PROVED-HERE, uses LIT Nash-Williams | Opus | referee; me | the same 82,118 maps |
| Theorem 6.9 | every 2-factor is two rainbow trees | PROVED-HERE, uses LIT Edmonds | Opus | referee; me | all 210 2-factors, brute force |
| Corollary 6.10 | each condition alone inside any cover | PROVED-HERE, uses LIT Rado | Opus (Corollary 3.2) | referee; me | all 210 2-factors |

## Literature used

| Result | Source as cited | What was opened |
| --- | --- | --- |
| Rado's theorem | Rado 1942; Schrijver, *A Course in Combinatorial Optimization*, Exercise 10.26 | The referee opened Schrijver's course notes and quotes the exercise. I did not open either. |
| Nash-Williams | Nash-Williams 1964; Schrijver's course notes, Exercise 10.29 via 10.28 | Same. The multigraph form is argued in `REFEREE-packing.md`. |
| Edmonds, disjoint branchings | Edmonds 1973; Schrijver, *Polyhedral combinatorics*, pp. 1674 and 1685-1686 | Sol independently opened https://ir.cwi.nl/pub/2216/2216D.pdf and https://ir.cwi.nl/pub/2216. Title page confirms Chapter 30, editors Graham, Grotschel and Lovasz, and 1995. Catalog confirms pages 1649-1704. The remembered fields were correct. |
| Tree and cotree duality | exposition, Lemma 2.5 | numbering read from `paper/main/barnette.aux` on 2026-11-14 |

## Computed and conjectured statements (Section 7)

| Note | Statement | Tag | Source and range |
| --- | --- | --- | --- |
| Proposition 7.1 | plantri index 27 at 16 vertices, outer face {0,1,2}: 3 covers, 12 good states, one cover with one cycle and no good state, 6,144 rainbow trees inside it | COMPUTED | `figures/make_figs.py` and `figures/check.py` (mine); found by Opus, confirmed by the referee (`data/BAD_16_16_27.json`) |
| after 7.1 | no cover without a good state up to 12 vertices | COMPUTED | census 6 to 12 (mine). I did not test 13 to 15. |
| Conjecture 7.2 (Step X) | non-increasing exchanges reach excess 0 | CONJECTURE | COMPUTED for all instances up to 12 vertices (mine and the referee's); up to 17 vertices and 1,485 of 1,543 triangulations at 18 (Fable, `RAINBOW.md` §3), plus 7 more at 18 (referee, `stepx.py`); 51 open at 18. Samples to 120 vertices: Fable, not recomputed. Test: a rainbow tree outside the backward closure of the good states. |
| 7, strict descent | fails first at 8 vertices (120 trees), 8,782 trees up to 12 | REFUTED strengthening, COMPUTED | census 6 to 12 (mine); same numbers from Fable and the referee |
| 7, deterministic walk | periodic at 38 vertices (periods 48, 68, 68) and 40 (period 60); none up to 15 | REFUTED strengthening, COMPUTED | Fable; four examples replayed by the referee (`data/periodic.json`). Not recomputed here. |
| 7, convexity of loads | exchange axiom fails at 12 vertices, plantri index 2, outer face {0,1,6} | REFUTED strengthening, COMPUTED | Fable and the referee. Not recomputed here. |
| 7, `ι_t` not transitive | 24 of 672 instances with 13 and 14 vertices | COMPUTED | Fable (`RAINBOW.md` line 223). Not recomputed here and not checked by the referee. |
| 7, descent on pairs (C3) | conjecture; independent replay through 20 vertices, original census through 23; strict descent fails at 16; three and four moves needed at 21 and 40; paths with non-increasing `c` fail at 16 | CONJECTURE and REFUTED variants | Sol reconciled FACTS.md, Astra final referee report and Fable descent REPORT.md. Independent: 3,373,400 pairs through 20. Original: 193,623,384 through 23. Not recomputed here. |
| 7, contraction induction | two missing lemmas; second one confirmed in the half-exception form to 18 vertices; fixed-cover repair fails at 18 | CONJECTURE | same file, section "State of contraction induction". Not recomputed here. The note says "no counterexample is known" for the first lemma because I found no explicit range for it. |
| 8, plateau depth | at most 7 in the exhaustive range, at most 27 in samples to 120 | COMPUTED | Fable (`RAINBOW.md` line 229). Not recomputed here. |
| 8, last paragraph | a proof of Step X has to use the disk identity | HUNCH | mine and Opus's (`PACKING.md` line 78) |

## Review state

Sections 2 to 6: refereed by Opus for the mathematics and self-audited by the author (`research/2026-11-14_fable_sign-free-note/AUDIT.md`). Sol has now independently audited this write-up, checked the named theorem sources, reproduced the requested counts and inspected all eleven PDF pages. See `research/2026-11-14_sol_referee-sign-free/REFEREE.md`, `RESULTS.md` and `REPORT.md`. Human check is pending. Figure 5 needs a layout repair because vertices 4 and 5 coincide; its numerical witness is confirmed.
