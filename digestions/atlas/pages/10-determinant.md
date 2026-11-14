# 10. A determinant needs coefficient extraction

The hexagonal prism is a useful warning. Its dual has three states and two tree matchings. The desired integer polynomial is a coefficient of a determinant whose matrix entries combine local triangle contributions. Each triangle receives its own auxiliary variable. Extracting their squarefree product forces every triangle to be used exactly once. Evaluating all those variables at one discards that condition. Terms that repeat a triangle survive, so the resulting number need not count tree matchings or prove their existence. The displayed counterexample formula was reproduced independently by the determinant referee. Even the valid coefficient norm counts surviving monomials only after nonvanishing has been proved. The running example's fixed-state matrix on page 9 is a different determinant with a different job. These two uses of determinant should not be conflated merely because both involve incidence signs.

Status: PROVED-HERE formulas independently AI-refereed in fable_referee-determinants. REFUTED shortcut: one raw evaluation counts tree matchings. The prism formula is independently reproduced there.

Connects to: 4 polynomial; 9 fixed-state matrix; 14 relaxations; 25 Berezin.

Sources: research/2026-11-14_fable_referee-determinants/REFEREE-dimers.md; SIGNIFICANCE.md, Sections 1 and 3.

COMPUTED figure provenance: build.py, computed.json, picture kind `determinant`.
