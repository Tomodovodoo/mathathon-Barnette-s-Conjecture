# What the induction now establishes

G and X remain open as cancellation-free lemmas. There is no INDUCTIVE-PROOF.md because the route is incomplete. This folder closes the Hall-formula verification, gives the full short-cycle obstruction classification, and refutes two proposed ways of closing the gaps.

## A cancellation-free conditional induction

PROVED-HERE, T2 unreviewed, conditional on the stated reduction certificate and the already refereed gluing and rotation lemmas.

Suppose a rooted simple Eulerian triangulation with a pair admits a finite reduction certificate with these rules:

1. A leaf is an octahedron.
2. A separating triangle is cut and capped, with the pair-preserving white-inner gluing convention. Both smaller pieces have certificates.
3. At a non-root degree-4 vertex x, one contraction is simple, has a pair, and has a certificate. The other contraction has no pair.

Then T has a tree matching.

Proof. Induct up the finite certificate. The octahedron has a tree matching, as seen directly by taking either of its two disjoint state assignments. In rule 2, the gluing lemma multiplies tree matchings of the two pieces. In rule 3, the recursive branch has a tree matching by induction. Any exception would rotate to a tree matching of the other contraction. A tree matching has a unique mate and hence a pair, contradicting the rule's no-pair premise. Thus lift-or-rotate succeeds. No signed sum, parity theorem or lower bound for tree-matchings is used. QED.

This is a certificate theorem, not an assertion that all instances possess such a certificate. The V=14 graph 31 from the prior census has no one-sided vertex at any facial root. That obstruction was already known; the new results do not remove it.

PROVED-HERE. Independently of X, G holds if T has no chordless five-cycle, by G.md section 7. This gives a structural class where contraction can preserve the pair. It does not guarantee the no-pair premise for the other contraction.

## The smallest concrete obligations now exposed

REFUTED. A descent into an arbitrary innermost bad region cannot prove G. The V=11 graph in G.md has an innermost bad four-cycle containing only a degree-4 vertex whose two merges are bad. Any successful proof must select regions differently or compare obstructions which cross or leave that disk.

REFUTED. A repair confined to the original D-cover cannot prove X. The V=18 graph in X.md has an exceptional matching isolated among the tree matchings of its cover, while other covers contain successful lifts. Any universal exchange proof must sometimes change the deleted corner map u.

These are counterexamples to proof strategies, not counterexamples to G, X, or Barnette's conjecture. The supplied OpenAI Proposition 5.1 proves the underlying existence statement using cancellation. No claim of a new proof is made here.

## Two adversarial readings

First reading checked boundaries. G1 requires a connected complement; the certificate says so. A simple bad contraction comes from five boundary vertices, whereas a parallel pair comes from four. The V=11 innermost disk really has singleton interior, and both contractions have explicit negative Hall sets. The restrictions in the G corollary are retained.

Second reading checked the X quantifiers. Exceptions require both the lift and rotation to fail. The V=17 witness defeats only a single reversal, since reversing both cycles succeeds. The V=18 witness defeats every orientation in its fixed cover. The all-exception cover in that contraction is not the cover of the first exception encountered by the earlier census; the certificate explicitly selects its saved state before replay. The strict counting condition is used only as a sufficient condition for a tree matching of T. Self-review does not count as independent refereeing.

The bounded dependency audit is in AUDIT.md.
