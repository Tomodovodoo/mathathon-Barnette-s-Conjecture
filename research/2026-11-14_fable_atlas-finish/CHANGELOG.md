# Changelog: finishing the atlas

Fable 5.2, 2026-11-14. Everything concerns `digestions/atlas/`. "Asserted" means an `assert` in a figure function, which `build.py` and `verify.py` both run. Such statements are `COMPUTED` on the named finite example by `python digestions/atlas/build.py` and say nothing general.

## 1. Inspection

See `INSPECTION.md`. Contact sheets: `before/` and `after/`, three sheets each in colour, greyscale and a deuteranopia simulation, made by `python research/2026-11-14_fable_atlas-finish/render_pages.py digestions/atlas/atlas.pdf <outdir>`.

## 2. Heading spacing

One macro, `lib.vs(length)`, a row break followed by an explicit vertical skip. `lib.grid` uses it between rows, so every multi-row grid now has the gap its code asked for (3 mm, was 0 under captioned panels). The stacked blocks on pages 5, 11, 12, 16, 22, 24, 25, 26 and 30 (old 4, 10, 11, 16, 22, 24, 25, 27, 28) use it too. Nine `\\[..]` remain in `lib.py` and `figs_*.py`. Each follows a picture or a single line of text, which has almost no depth, so there the length takes effect (seen on the renders of pages 5, 11, 12 and 30).

Side effect: figures with two rows of panels grew by about 3 mm. Three pages were already full, so pages 13, 17 and 18 draw their panels at unit 0.585 instead of 0.615.

## 3. Two new pages

| Page | Content | Asserted |
| --- | --- | --- |
| 10, three written proofs of the key step (`figs_proofs.keystep_fig`) | (a) one face path with its turn signs and the height of the running pair's second state; (b) all eleven face paths laid on `G` as one flow, with the units leaving the shore of the long cycle; (c) one unpaired marked object of the bijective note's path marks; (d) the three totals | For all 176 (pair, cycle, white face) triples, reversing a clockwise cycle raises the height by 1 exactly for the faces inside (paper, Lemma 4.6). The total height equals the volume of page 4 minus 4 on all twelve states. `sum eps * omega^2 = +18 = (-1)^((n-m)/2) m! * 9` with `n = 10`, `m = 2` (Proposition 4.8), and the same sum over good states only (Lemma 4.5). The flow has divergence +1 at each white vertex, -11 at `t0`, 0 elsewhere; its net flux out of the shore of each of the 16 (pair, cycle) shores equals the number of white vertices inside. The summed turn signs are local potentials of that flow (primal note, (5.2)), and the lowest coefficient of the primal polynomial is `+9` at degree 2 (its (6.4)). Of 43 objects (pair, two path marks) the signed count is `-9`; the 9 unpaired objects (one white face inside each cycle of a cover, first turning step on that cycle, cycle oriented so the corner carries `s`) all have sign `-1`. |
| 29, what is machine-checked (`figs_proofs.blueprint_fig`) | The 34 route statements of the main paper as a chart in four columns by section, filled by the blueprint's status, with the 51 arrows of the transitive reduction of its 67 uses; a count bar; a table of four translations | 34 statements; statuses 4, 25, 5; the five without counterpart are Lemma 2.2, Proposition 2.6(2), Lemmas 3.7, 4.4, 4.7; the uses form an acyclic graph, every statement reaches Theorem 1.1, and no statement uses a later section. The recount file of the independent rebuild gives 5, 27, 2 and moves exactly three statements (4.7 to exact, 4.4 and 3.7 to "after translation"). |

Nothing was pasted from the other documents' figures. The face paths are the ones the copied toolkit uses for the paper's heights figure (shortest paths in `G`, ties by face index); I did not compare them with the paths behind the primal note's own flow figure.

**Status sentence of page 29.** `research/2026-11-14_astra_lean-check/REPORT.md` appeared while I was working. It confirms the rebuild (fresh clone, all files compile, standard axioms only, statement types pass) and it also refutes one proposed target, narrows two claims, and calls its 5/27/2 recount advisory, leaving the blueprint's statuses unchanged. So the page keeps 4/25/5 as the fill, marks the three moved statements with a dot, gives 5, 27 and 2 in the text as the second model's count, and says "rebuilt and checked by a second model" together with "calls its recount advisory, and it corrected three claims made around the proof".

`verify.py` now also checks these numbers against the certificates, and that the page order equals `pages.ORDER`.

## 4. The two declined audit items

**The 466.** `COMPUTED` (`figs_scope.exception_shape`, run by every build): the 466 rows with `V <= 16` of `research/2026-11-14_fable_induction-completion/data/exceptions_6_13.jsonl` and `exceptions_14_17.jsonl.gz` (8, 20, 80, 358 at `V` = 13 to 16). For each row I rebuild the triangulation from its stored faces and check it is a two-coloured sphere triangulation in which `x` has degree four with the stored neighbours. Then, with `x` removed, the opposite edges of the stored state plus two root edges form a forest with exactly two trees, one through `a` and `v1` and the other through `b` and `v2`, in all 466. The black face on `a v2` uses `a` in all 466. This is pattern `P_1` of `RESIDUAL-CASES.md`. The sentence is on page 23.

Limit of the check: it does not rerun the census. Which lifts fail and which the rotation repairs is taken from the recorded rows (two programs agree on the count 466, per the referee report). I did not check `V` = 17, 18.

**Reading order.** Adopted in part; reasons in the README, section "Order". Mechanism: `pages.ORDER`, and `@slug@` references in the texts, so a later reorder needs no text edits.

## 5. Texts

Restored, from the list in the previous report: "With `q` cycles a state has `2^q` partners, and they pair off" (page 7); "so the determinant adds up the partners with signs" (page 11); "So a good state is a spanning tree with prescribed degrees" (page 20); "Each side only reports how its trees meet the cut" (page 22). Paid for by shortening other sentences on the same pages. All 30 texts are between 130 and 150 words.

Changed statuses: page 9 (primal note: refereed, revised, accepted in a cross-audit; the old "its Lean statement is unrefereed" is superseded by page 29), page 7 (points to page 10 for a complete marked object), page 23.

## 6. Build

`build.py` and `verify.py` detect an overflowing route page by content (page `i` starts with `i`, ends with "See also", and the page after the last route starts with "Sources") instead of by page count, since the sources now take three pages. The figure preamble loads `array`.

Final run: 30 routes, 34 pages, all checks passed, no overfull box, texts 130 to 150 words, figures 0.80 to 0.95 of the text width.
