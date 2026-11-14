# Mathematical issues for the referee (`research/2026-11-14_sol_referee-main-v2/`)

I found no mathematical error in version 2. I did not referee the paper; I read it as an
exposition. Below are the checks I made, and two points the referee may want to confirm,
because my new exposition leans on them.

1. **The cube in "The total is not zero" (new text).** I state that the cube's two states
   give two pairs with the same cover, the triangle 3,4,5 around one white face, with opposite
   signs and weights differing by 1, so $\sum\varepsilon\omega=\pm1$. Checks by hand: $n=3$;
   faces 045, 234, 135; states (4,3,5) and (5,4,3); $D$ is $5\to4\to3\to5$ or its reverse; the
   inside of the triangle away from $t_0$ is the single white face 345, so $L=1$. Proposition
   4.8 with $m=1$ gives $\Sigma=(-1)^{(3-1)/2}\cdot1\cdot1=-1$. I wrote $\pm1$ to avoid relying
   on the drawing's orientation. COMPUTED by hand only; a one-line machine check would be good.
2. **"The unsigned manuscript [4] calls a good state a tree matching" (new sentence).** The
   trees paper defines a tree matching through its incidence tree ("H − s is a tree"). That
   this is the same as "good" is the equivalence in Lemma 3.5 plus duality. CONSISTENCY.md C1
   says the same. Please confirm the wording against [4]'s definition.
3. Example 4.9 arithmetic rechecked: $\Sigma=18=2!\,(6\cdot1+3\cdot1)$, with sign
   $(-1)^{(10-2)/2}=+1$. Consistent with Proposition 4.8 and with the new Figure 11.

No typo-level mathematical fixes were made.
