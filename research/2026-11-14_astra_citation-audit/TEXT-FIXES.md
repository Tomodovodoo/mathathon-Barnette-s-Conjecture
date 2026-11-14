# Text fixes for document owners

No document prose was edited. The numbered literature citations checked in the main paper match their sources. The following changes concern attribution precision, publication status, and statements not certified by this pass.

## Atlas page 24, publication status

Current sentence in `digestions/atlas/atlas.tex`: "The three results are published."

LIT. This wording hides the access chain. The library holds Stein's published article, Feder and Subi's ECCC technical report, and explanations of Kelmans rather than his original paper. Suggested replacement:

> Stein's result is published. We read Feder and Subi in ECCC report TR06-015, and Kelmans' strengthening through Hertel and Alt and coauthors. The original Kelmans paper was not opened.

The underlying mathematical statements are supported. This is a provenance correction, not a refutation of them.

## Route-map gluing paragraph, Kelmans attribution

Current sentence in `digestions/route-map/HOW-IT-WORKS.md`: "The reduction itself was known to Kelmans in 1986."

LIT, secondary. Suggested replacement:

> Alt, Payne, Schmidt and Wood explain the reduction in Section 5 and attribute it to Kelmans' 1986 work; we did not open Kelmans' original paper.

The main paper already uses this secondary-source convention. Keep it consistent in the route map.

## Route-map gluing paragraph, decision problem

Current sentence: "Prescribing arbitrary sets of edges is NP-complete for Barnette graphs."

LIT. The proof of Theorem 4.6, printed p. 12 of Bagheri Gh., Feder, Fleischner and Subi 2022, explicitly states the prescribed-edge decision hardness. The current shorthand names an operation rather than a decision problem. Suggested replacement:

> Given a Barnette graph and a set of edges, deciding whether a Hamiltonian cycle contains every prescribed edge is NP-complete, as stated in the proof of Theorem 4.6 of Bagheri Gh., Feder, Fleischner and Subi 2022.

Do not describe this as Corollary 4.3. The source has Claim 4.3, which concerns a different reduction.

## Sign-free manuscript, original versus secondary access

LIT. The statements and optional locators at `sign-free.tex` lines 144, 430 and 431 match the opened Schrijver sources. Rado 1942, Nash-Williams 1964 and Edmonds 1973 were not opened in full. The existing paired citations are good; adding the phrase "in the form reproduced by Schrijver" would make the access chain explicit. The Edmonds publisher is already correctly Academic Press. No correction to the theorem statements is needed.

## Waterloo attribution

LIT, secondary. No requested current document directly cites Barnette1969. Its canonical bibliography note now cites Alt et al. 2016, reference 3, printed p. 364, as the evidence for Barnette, "Conjecture 5," proceedings p. 343. The original proceedings page remains unavailable. Do not say this audit read its wording. The supplied OpenAI PDF's attribution to Grunbaum is a source discrepancy; the protected PDF was not changed.

## Checks that require no correction

- LIT. Main paper 64/90 bounds have the correct separate attributions.
- LIT. The main paper's unsigned-manuscript entry has no author field. The short title "A constructive proof" in the involution bibliography is identifiable; the full title would be clearer but is not a false attribution.
- LIT. The synthesis credits the triangle-parity condition to Bagheri Gh., Feder, Fleischner and Subi. Theorem 11 also requires the stated face and separating-digon hypotheses. The main paper's Feder-Subi citation is only for face-colour conditions, so it does not repeat the old misattribution.
- LIT. KPW Theorem 1 needs incident vertex and face for a bijection. A general replacement of any incidence matching problem by spanning trees would be stronger than that theorem. No such direct claim was found in the four TeX documents.
- LIT. Thomason's cubic bipartite consequence is supported by Corollary 1.5, printed p. 262. The parity of all Hamiltonian cycles in an arbitrary cubic graph is not asserted.
- LIT. Juhasz-Kalman-Rasmussen Theorem 1.1 concerns hypertrees and sutured Floer support. It supplies a dictionary, not a Hamiltonicity theorem. No direct citation to it occurs in the four TeX documents.

## Still requiring a content audit

The extraction ledger includes project-report links, internal figure references, numerical ranges, and claims of referee acceptance. File existence was checked; their mathematical content and changing review status were not all independently rechecked here. Those records remain explicitly unverified. This report does not certify every sentence of the digestions or atlas.
