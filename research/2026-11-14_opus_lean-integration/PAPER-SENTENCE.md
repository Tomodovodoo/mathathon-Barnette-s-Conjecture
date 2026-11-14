# The paper's sentence on formal verification

For the owner of `paper/main/barnette.tex`. I did not edit the paper.

## What the paper says now

`paper/main/barnette.tex`, lines 1060 to 1062 at commit `e97b061`, the last paragraph of "Consequences and open questions":

```tex
OpenAI's accompanying Lean formalisation gives a machine-checked proof of Barnette's conjecture \cite{OpenAI2026b}.
It uses a different route through algebraic duality and does not formally verify every statement or proof in this exposition, including the two-induced-trees statement of Proposition~\ref{prop:target}(2).
Two companion notes give a primal formulation and an account using two sign-reversing involutions.
```

## Does it need changing?

Nothing in it is false. It understates the record in one way: it implies that none of the paper's own devices is machine-checked. Since the independent check (`research/2026-11-14_astra_lean-check`), Lemma 4.4, Lemma 4.7, the case of Lemma 4.5 that the existence proof uses, and Proposition 4.8 by `ε · ω^m` are machine-checked in the Lean's model, and they carry the formal main theorem. The paper should say so only in the qualified form, since the heights are replaced by flow weights. I recommend the replacement below. If the owner prefers not to mention work outside the cited sources, the current two sentences can stay as they are.

## Proposed wording

Replace the first two sentences with these two. The third sentence, on the companion notes, stays.

```tex
OpenAI's accompanying Lean formalisation gives a machine-checked proof of Barnette's conjecture \cite{OpenAI2026b}; it argues through algebraic duality rather than a drawing, does not check this exposition statement by statement, and has no counterpart of Lemma~\ref{lem:connected} or of Proposition~\ref{prop:target}(2).
On top of it we have machine-checked, in its model, Lemmas~\ref{lem:sign} and~\ref{lem:difference}, the case of Lemma~\ref{lem:cancel} that Proposition~\ref{prop:good} uses, and Proposition~\ref{prop:good} by the argument given here with the formalisation's flow weights in place of the heights, so that the formal proof of the main theorem no longer uses OpenAI's phase and polynomial nonvanishing argument.
```

Why each clause is there:
- "in its model": the sign is checked with "counterclockwise" read as `δ`-sum `-3` on the Lean's algebraic dual, not on a drawing (bridge B1).
- "the case of Lemma 4.5 that Proposition 4.8 uses": the Lean proves the first sentence and the vanishing of the total when no pair has acyclic `Q_s`. The identity with good states and their unique partners is not checked (checker, FAITHFULNESS.md item 14).
- "flow weights in place of the heights": the bridge from heights along face paths to the Lean's weights is not formalised (TODO T2).
- "no longer uses OpenAI's phase and polynomial nonvanishing argument": the checker's own walk shows that the six named lemmas are unreachable. General Mathlib polynomial algebra is still reached through the dual construction, so the sentence must not say "no polynomial".
- No line count, theorem count or path. Those live in `proofs/lean/README.md`. If the paper has a data-availability line, add: "The Lean files and an independent rebuild are in the project repository."

## Shorter alternative, one sentence

```tex
OpenAI's accompanying Lean formalisation gives a machine-checked proof of Barnette's conjecture \cite{OpenAI2026b} through algebraic duality; it does not check this exposition statement by statement, but in its model we have also machine-checked Lemmas~\ref{lem:sign} and~\ref{lem:difference} and Proposition~\ref{prop:good}, with flow weights in place of the heights.
```

This drops the Lemma 4.5 qualification and the two missing statements. I prefer the two-sentence version, because it keeps the paper's current admission about Proposition 2.6(2).
