from pathlib import Path
p=Path('digestions/route-map/build_map.py');s=p.read_text(encoding='utf8')
a=s.index('    L += ["", "Read from the picture,');b=s.index('    L += [tail.rstrip()',a)
s=s[:a]+'''    L += ["", "The cells count supplied proofs, open routes and refutations, not independently established theorems. Review states are attached to the written route entries.", "",
          "- Induction now has local contraction and rotation proofs at U, with ML1 and ML2 still open; gluing alone is no longer the whole column.",
          "- Topological disk and Morse readings are AI-refereed with corrections. The newer Rado-Euler rainbow and unique-factor proofs are unreviewed; exchange X remains conjectural.",
          "- Probability has a mean-fitting obstruction, failed zero-location shortcuts and the two-tree packing question. Exact rounding remains separate.",
          "- The lattice column retains the failed extreme and irreducible rules and the linear test of a specified pair. It does not assert an efficient direction-choice algorithm.",
          "- Matroid reformulations do not prove existence. The natural two-matroid relaxation and the natural integral-LP claim fail.", ""]
''' + s[b:]
# White-backed labels keep the many bypass strands from running through text.
s=s.replace('style="italic", zorder=6)','style="italic", zorder=6, bbox=dict(facecolor="white", edgecolor="none", pad=2))')
s=s.replace('va="center", zorder=6)\n        ax.text(x, y - 0.07','va="center", zorder=6, bbox=dict(facecolor="white", edgecolor="none", pad=2))\n        ax.text(x, y - 0.07')
s=s.replace('color=VERDICT_COLOUR[s["verdict"]], zorder=6)\n        ax.text(x, y - 0.23','color=VERDICT_COLOUR[s["verdict"]], zorder=6, bbox=dict(facecolor="white", edgecolor="none", pad=2))\n        ax.text(x, y - 0.23')
s=s.replace('color="#666666", zorder=6)\n\n    hh', 'color="#666666", zorder=6, bbox=dict(facecolor="white", edgecolor="none", pad=2))\n\n    hh')
p.write_text(s,encoding='utf8')
p=Path('digestions/route-map/HOW-IT-WORKS.md');s=p.read_text(encoding='utf8')
s=s.replace('The conjecture campaign now reports a joint failure of the two true lattice extremes at 18 vertices; that computation awaits independent replay.','An independent referee confirms the first joint failure of the two true lattice extremes at 18 vertices. The replacement extreme-or-irreducible rule also fails, at 33 vertices, by two independent implementations.')
s=s.replace('It can be larger than 1. It is 2 on a 9-vertex example and reaches 3 with no separating triangle [`COMPUTED`, route-combinatorics], so first-order arguments are not enough.','It is unbounded even without separating triangles, according to the new T2 unreviewed construction in `research/2026-11-14_astra_cycle-covers/PROOFS.md`. On 3m+2 dual vertices it has one cover, cmin=m-1 and 2^(m-1) tree matchings. The primal meaning is components(G-S)-1 for the admissible deletion S. The finite separator-free census reaches cmin=6 at V=23. First-order arguments cannot cover this family.')
s=s.replace('a proof from one Euler identity is `PROVED-HERE` in route-graph-theory, under review','a proof from one Euler identity is `PROVED-HERE` in route-graph-theory, independently AI-refereed by the structure referee')
a=s.index('- **No canonical choice.**');b=s.index('\n',a)
s=s[:a]+'- **No canonical choice.** C2 is independently refuted first at V=18 and R2 at V=33. Rainbow exchange X passes all trees through V=17 and samples to V=120, but remains conjectural. Surplus walks can cycle at V=38; plateau search is essential.'+s[b:]
a=s.index('- **How many.**');b=s.index('\n',a)
s=s[:a]+'- **How many.** C1, #TM >= 2^cmin, passes the independently reproduced all-root census through V=22 and a T4 separator-free census through V=24 on 23,824,742 facial roots. Only 2 cmin is proved in general, with an AI referee. One-cover equality is independently AI-refereed; its converse remains open. The new two-cover proof is T2 unreviewed.'+s[b:]
s+='''

## Current written routes and unfinished shortcuts

Three complete written routes now exist: `paper/main/` in the dual language, `proofs/primal/` entirely in G, and `proofs/involutions/` with distinct marked crossings and two finite involutions. The merged and involution texts are under independent AI review. The earlier primal version was AI-refereed; the revised version has author verification. Its revision disputes referee M4, whose phase ratio it simplifies to i^n. This disagreement needs another check. The upstream Lean proof was machine-checked in a local build; that does not formalize every new exposition. Nothing here is human-checked.

The merged exposition adopts the product of local signs, heights defined by crossing counts along face paths, and an explicit lemma establishing connectivity on the inside of a selected cycle before applying Euler's formula. These simplify the explanation without removing the signed nonvanishing argument. The marked-involution text counts 279 objects on its current fixture, while the older digestion audit counted 213 with a different fixture or convention. No equality between those object sets is claimed; the texts need a direct convention comparison.

The unsigned contraction route now has two exact gaps, ML1 and ML2, in `research/2026-11-14_fable_induction-completion/MISSING-LEMMA.md`. Local splitting, lift criteria and rotation have an independent AI referee. A new one-sided existence step is unreviewed. Direct lifting of even one contracted matching can fail at V=18, although rotation succeeds on that example. The two-tree packing conjecture supplies a possible fractional step, with exact rounding still missing. C3 and rainbow exchange remain the other live descent questions. See [the open problems](../steps/09-what-is-still-open.md) for ranges, counterexamples and tests.
'''
p.write_text(s,encoding='utf8')
p=Path('digestions/steps/00-overview.md');s=p.read_text(encoding='utf8');s+='''

## Where the project stands now

The three current written routes are [the merged dual paper](../../paper/main/barnette.tex), [the revised primal proof](../../proofs/primal/PRIMAL-PROOF.md), and [the marked-involution proof](../../proofs/involutions/INVOLUTIONS.md). The first and third are under independent AI review. The original primal note was AI-refereed; its revision is self-audited and disputes the referee's circuit-dependent phase normalization, simplifying the proposed ratio to i^n. The dispute is recorded in `research/2026-11-14_astra_primal-revision/REPORT.md`. None is human-checked. The upstream Lean theorem was machine-checked in a local build.

The merged paper uses the sign as a product of local signs, heights measured along face paths, and a connectivity lemma for the inside of a selected cycle. The last point supplies the connectedness hypothesis needed before Euler's formula is used. These are changes to the presentation, not an unsigned existence proof.

For sentence 8, c_min is the minimum number of components in the unoriented D-cover of a pair. It differs from the number of cycles in Q_s. The cycle-cover run supplies an unreviewed primal interpretation, c(D)=components(G-S)-1, and a separator-free family on 3m+2 dual vertices with c_min=m-1 and #TM=2^(m-1). Large c_min is therefore not an effect of separating triangles alone. Its census tests the exponential bound through dual order 24 only in the 4-connected class; the independent all-root census reaches 22.

Several hoped-for simplifications are false. Both lattice extremes can fail at V=18; extrema together with irreducibles can all fail at V=33. Direct contraction lifting fails at V=18. The contraction route still needs ML1 and a two-sided lifting lemma, and monotone pair descent C3 and rainbow exchange X remain conjectural. Their exact statements and finite ranges are in [09](09-what-is-still-open.md).
''';p.write_text(s,encoding='utf8')
