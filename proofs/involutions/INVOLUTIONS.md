# Two involutions for the forest-pair lemma

PROVED-HERE. If a pair of disjoint states exists in a simple face-bicoloured sphere triangulation, a pair exists whose opposite-edge graph is a forest. The complete standalone proof is in involutions.tex and involutions.pdf. It assumes pair existence, so it does not need a separating-triangle hypothesis.

## Objects and the two maps

Let m be the minimum cycle count of a pair. A marked object consists of a pair and an unordered set of m distinct crossings of selected second-state spokes with fixed white-face rays. Repeated white faces and repeated spokes are permitted; repeated identical crossings are not. Direct each cycle through the first-state corner, centre, and second-state corner. With J equal to clockwise minus counterclockwise cycles, its sign is (-1) raised to floor(J/2) plus the number of marked right-to-left crossings.

The first map fixes objects with a forest opposite-edge graph. Otherwise it reverses the first opposite-edge cycle, choosing that cycle from the second state alone. This preserves all marks. The disk identity changes J by two, so it reverses sign.

The second map first reverses the first unmarked cycle of the underlying unoriented cover. If all cycles are marked, minimality forces exactly one mark per cycle. First select an exterior white-face mark, or else a nonfirst interior crossing, using a fixed orientation-independent cycle order. Pair successive ray crossings, leaving only the first crossing of an interior ray unpaired. Move the mark to its partner and reverse its cycle exactly when the partner is currently a first-state spoke. All other marks lie on other cycles. The same cycle qualifies on the return move; this proves involutivity. Geometric pairing reverses crossing direction, and cycle reversal reverses it again while flipping floor(J/2). Thus the sign reverses in either case.

Second-fixed objects are minimum covers with one interior white-face point per cycle, marked at the first crossing, with the unique orientation making that crossing a second-state spoke. Their number is the sum over minimum covers of the product of enclosed white-face counts. It is positive, and all fixed objects have sign (-1)^floor(m/2). The two signed counts force a first-fixed object.

## Explicit construction

Choose any second-fixed object by enumerating minimum covers. Alternate first and second moves, stopping before a fixed move. The finite two-coloured degree-two graph of the two involutions is a path from this endpoint. A second-fixed terminal endpoint would have the opposite sign after an odd number of moves, impossible. Hence it ends at a forest pair. This is the Garsia-Milne finite path argument. It is an exhaustive constructor, with no claim that finding a minimum cover is efficient.

## Verification

COMPUTED by research/2026-11-14_sol_li-completion/verify.py and extras.py. All 56 classes through 14 triangulation vertices agree as canonical maps with plantri. All 1206 roots are checked, including 880 with pairs. The verifier enumerates 221050 marked objects and checks both maps, signs, fixed sets, lowest coefficients and all 4658 paths from second-fixed objects. Maximum path length is two moves. Family checks reach 20 triangulation vertices. See the research census, witnesses and family outputs.

## Example and source relation

The current running.json has minimum cycle count two. The exact rational layout here gives 279 marked objects, nine second-fixed objects, and lowest coefficient nine. running-objects.json lists every object and both images; example-table.tex includes the full listing in the PDF. Earlier counts of 213 refer to a different geometry or input and are not silently reused.

Li's incidence orientation is opposite to the directed two-spoke convention used here, so his cw-prime is -J. The two sign definitions nevertheless agree because n and m have the same parity. Li Definitions 13 through 23 and Appendix B supply the maps. The full general-m verifications, set convention, invariant selection rule, nonemptiness proof and finite-path extraction are written in the note. OpenAI supplies the disk identity and first cancellation; barnette_trees uses a different ordered weight-token walk with restarts. Heights at white faces are signed counts of the same ray crossings.
