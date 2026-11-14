# Twenty approved changes

Source: Astra/v6/work/editorial-20/proposals.json. Approval: thread position 2169; implementation confirmation: 2194. Exact source excerpts follow.

## 1. Identify what the spherical formulas compute

Section 2. Calls the displayed quantities eigenvalues before using them to locate the resonance. Shortens the kernel definition to make room for that identification.

Before:

```tex
Let $C_h,T_h$ be the spherical convolution operators with kernels $\mathbf1_{s>h}$ and $(s-h)_+$, using unnormalized surface measure. Put $\Lambda_l=l(l+d-2)$ and $\omega_{d-2}=|S^{d-2}|$. Funk--Hecke and two integrations of the Gegenbauer equation give
\[
c_l(h)=\frac{\omega_{d-2}(1-h^2)^{(d-1)/2}Z_l'(h)}{\Lambda_l},\qquad
 t_l(h)=\frac{\omega_{d-2}(1-h^2)^{(d+1)/2}Z_l''(h)}{\Lambda_l(\Lambda_l-d+1)}.
\]
```

After:

```tex
Let $C_h,T_h$ be spherical convolutions with kernels $\mathbf1_{s>h}$ and $(s-h)_+$, using unnormalized surface measure. Put $\Lambda_l=l(l+d-2)$ and $\omega_{d-2}=|S^{d-2}|$. Funk--Hecke gives their degree-$l$ eigenvalues
\[
c_l(h)=\frac{\omega_{d-2}(1-h^2)^{(d-1)/2}Z_l'(h)}{\Lambda_l},\qquad
 t_l(h)=\frac{\omega_{d-2}(1-h^2)^{(d+1)/2}Z_l''(h)}{\Lambda_l(\Lambda_l-d+1)}.
\]
```

## 2. State the arithmetic objective before the division

Section 2, proof of Lemma 3. States the nonvanishing criterion first. The known root and the factor theorem replace the term-by-term explanation of divisibility.

Before:

```tex
The first three terms vanish at $T_*$, since $Z_4''(h)=0$, and every later product contains $T-T_*$. We show that the quotient by this factor is a local unit at every integer spectral value.
```

After:

```tex
To prove isolation, we show that $S_M(T)/(T-T_*)$ is a local unit at every spectral value. This quotient is polynomial because $Z_4''(h)=0$.
```

## 3. Finish each exceptional case explicitly

Section 2, end of Lemma 3. Names D = 24 instead of referring to "the last quotient", and makes the subject of the final deduction explicit. The calculation is unchanged.

Before:

```tex
Substitution in \eqref{spectral-polynomial} gives the quotients. For $D=12$, $\Lambda_l=l(l+7)\equiv0,2\pmod3$; the last quotient is one at either residue modulo two. They are therefore units at all spectral values. Since $\Lambda_l$ is strictly increasing, only $l=4$ can vanish.
```

After:

```tex
Substitution in \eqref{spectral-polynomial} gives the quotients. For $D=12$, $\Lambda_l=l(l+7)\equiv0,2\pmod3$; for $D=24$, the quotient is one at both residues modulo two. The quotients are therefore units at all spectral values. Since $\Lambda_l$ is strictly increasing, only $l=4$ can vanish.
```

## 4. Make the formal implicit-function step explicit

Section 2, proof of Proposition 4. Orders the argument as elimination, invertibility, closure of polynomial coefficients, then the formal implicit function theorem.

Before:

```tex
Eliminate the height from $V(R,H)=v_d\rho$ using $V_H=-A$. Write $R=1+\eps(f+w)$, $[w]_L=0$, and divide the nonconstant energy and volume equations by $\eps$. Their linearization in $w$ and $\rho-\rho_d(h_*)$ has noncritical entries $t_l$, volume entry $dv_d$, and critical density entry $v_db$. It is invertible on polynomial coefficients. Taylor coefficients of cap integrals preserve finite spherical polynomials, by Funk--Hecke applied to products and to derivatives of the cap kernel. The formal implicit function theorem therefore supplies the radial series.
```

After:

```tex
Eliminate the cap height using $V(R,H)=v_d\rho$ and $V_H=-A$. For $R=1+\eps(f+w)$, $[w]_L=0$, divide the nonconstant energy and volume equations by $\eps$. The linearization has nonzero coefficients $t_l$ on the noncritical modes, $dv_d$ for volume, and $v_db$ for the critical density variation. Funk--Hecke shows that the cap Taylor coefficients preserve finite spherical polynomials. The formal implicit function theorem gives the radial series in this class.
```

## 5. Give the purpose of the endpoint conjugacy first

Section 2, end of Proposition 4. Connects the endpoint map directly to constant chord separation, and names the Fourier coefficients determined by the translation equation.

Before:

```tex
The two endpoint angles $B_\pm(\theta,\eps)$ solve $R(B_\pm)\cos(B_\pm-\theta)=H(\theta)$ and start at $\theta\pm a_*$. Their endpoint map $B_+B_-^{-1}$ is reversible under $x\mapsto-x$ and commutes with translation by $\pi$. Its normalized formal conjugacy to translation by $2a_\eps$ is obtained order by order from $u(x+2a_*)-u(x)=G(x)-\av G$. Irrationality gives each nonzero coefficient; the mean determines the angle, and reversibility makes the conjugacy odd. At first order the mean endpoint separation gives $a_1=((h_*-b)\mu-h_1)/\sigma_*$. Since $a_1>0$, formally invert $a_\eps$ and truncate in $a-a_*$. Taylor's theorem on a slightly wider strip proves the stated residual estimate, with constants allowed to depend on the fixed truncation order.
```

After:

```tex
To give the chord endpoints constant parameter separation, let $B_\pm(\theta,\eps)$ solve $R(B_\pm)\cos(B_\pm-\theta)=H(\theta)$, with $B_\pm=\theta\pm a_*+O(\eps)$. The map $B_+B_-^{-1}$ is reversible under $x\mapsto-x$ and commutes with translation by $\pi$. Conjugating it formally to translation by $2a_\eps$ requires, at each order, $u(x+2a_*)-u(x)=G(x)-\av G$. Irrationality determines the nonzero Fourier coefficients, the mean determines the angle, and reversibility gives an odd conjugacy. The first-order mean separation is $a_1=((h_*-b)\mu-h_1)/\sigma_*$. Since $a_1>0$, invert $a_\eps$ formally and truncate in $a-a_*$. Taylor's theorem on a slightly wider strip gives the residual estimate for each fixed truncation order.
```

## 6. State the target domain before the change of variables

Section 3. Moves the target inequality ahead of the transformation and removes its repeated announcement afterward. The Cartesian extension and all formulas stay in place.

Before:

```tex
Put $\chi=e^2-H^2o^2$, $W=e-Ho\eta_1$, and $s=\xi y+H\eta_1$. The sphere transformation
\[
\eta_{1,\mathrm{old}}=\frac{e\eta_1-Ho}{W},\qquad
 \eta_{\perp,\mathrm{old}}=\frac{\sqrt\chi}{W}\eta_\perp
\]
satisfies $n\cdot(X,Y\eta_{\mathrm{old}})-q=(\chi/W)(s-h)$ and has Jacobian $\chi^{(d-2)/2}W^{-(d-2)}$. For the Cartesian extension, put $g(y)=Y(u)/\sin u$. In coordinates $\omega=(y,\omega_2,\omega_\perp)$, the first component is $\widehat X(y)=X(u)$, while the transverse components have common denominator $e-\sin x\,o\omega_2$ and numerators $g(e\omega_2-\sin x(1-y^2)o)$ and $g\sqrt\chi\,\omega_\perp$. These are analytic Cartesian expressions, and the denominator is close to one.

The cap inequality is now $s>h$.
```

After:

```tex
To transform the moving cap into $s>h$, put $\chi=e^2-H^2o^2$, $W=e-Ho\eta_1$, and $s=\xi y+H\eta_1$. The change of variables on the sphere
\[
\eta_{1,\mathrm{old}}=\frac{e\eta_1-Ho}{W},\qquad
 \eta_{\perp,\mathrm{old}}=\frac{\sqrt\chi}{W}\eta_\perp
\]
satisfies $n\cdot(X,Y\eta_{\mathrm{old}})-q=(\chi/W)(s-h)$ and has Jacobian $\chi^{(d-2)/2}W^{-(d-2)}$. For the Cartesian extension, put $g(y)=Y(u)/\sin u$. In coordinates $\omega=(y,\omega_2,\omega_\perp)$, the first component is $\widehat X(y)=X(u)$, while the transverse components have common denominator $e-\sin x\,o\omega_2$ and numerators $g(e\omega_2-\sin x(1-y^2)o)$ and $g\sqrt\chi\,\omega_\perp$. These are analytic Cartesian expressions, and the denominator is close to one.


```

## 7. Give the family norm as a formula

Section 3. Makes the order of summation, supremum, and Lipschitz seminorm visible. This trades the verbal substitution rule for one reusable definition.

Before:

```tex
We use analytic Wiener norms $\|u\|_{r,s}=\sum_m(1+|m|)^se^{r|m|}|u_m|$. For parameter families on a closed subset of $I_t$, replace each coefficient absolute value by its supremum plus $t$ times its Lipschitz seminorm, before summation; a superscript $(t)$ denotes this convention. The same convention applies to matrices and tensor coefficients. These are algebra norms, and $\|u\|_{r-\delta,s}\le C_s\delta^{-s}\|u\|_{r,0}$.
```

After:

```tex
We use the analytic Wiener norms $\|u\|_{r,s}=\sum_m(1+|m|)^se^{r|m|}|u_m|$. For a parameter family on a closed subset of $I_t$, write $\|u\|_{r,s}^{(t)}=\sum_m(1+|m|)^se^{r|m|}(\sup|u_m|+t\Lip u_m)$, with the same coefficientwise convention for matrices and tensors. These are algebra norms, and $\|u\|_{r-\delta,s}\le C_s\delta^{-s}\|u\|_{r,0}$.
```

## 8. Define the nonlinear system before estimating it

Section 3. Moves the definition of F to the start of the paragraph, so the norm estimates lead to the residual actually used in Newton iteration.

Before:

```tex
Fix a sufficiently large integer $s_0$ and call $\|\cdot\|_{r,s_0}^{(t)}$ the strong norm. The formulas above give analytic cap maps with a fixed derivative loss, including three derivatives and differences between two parameter families. To bound the integrals, expand the amplitudes in $Z_p(\xi)Z_q(y)$ and apply Funk--Hecke in $y$. Normalized Gegenbauer products have nonnegative coefficients of sum one; conversion from cosine to Gegenbauer coefficients costs at most $d-1$ derivatives per variable, by orthogonality. Thus the integrals have polynomial strip costs. For $z=(\gamma,\nu,c_E)$, set $F(z,a)=(F_V,F_E,F_0)=(V-\nu,J+\nu q-c_E,\vol K-v_d)$.
In the coefficientwise family norm, its Taylor remainder is bounded by $C\|v\|_{r,s_0}^{(t)2}$ on a small meridian ball. All derivative losses below are fixed before the seed order is chosen.
```

After:

```tex
For $z=(\gamma,\nu,c_E)$, set $F(z,a)=(F_V,F_E,F_0)=(V-\nu,J+\nu q-c_E,\vol K-v_d)$.
Fix a sufficiently large integer $s_0$ and call $\|\cdot\|_{r,s_0}^{(t)}$ the strong norm. The cap formulas give analytic maps with a fixed derivative loss, through three derivatives and for differences of parameter families. To bound the integrals, expand the amplitudes in $Z_p(\xi)Z_q(y)$ and apply Funk--Hecke in $y$. Normalized Gegenbauer products have nonnegative coefficients of sum one; conversion from cosine to Gegenbauer coefficients costs at most $d-1$ derivatives per variable, by orthogonality. Thus the integrals have polynomial strip costs. The Taylor remainder of $F$ is bounded by $C\|v\|_{r,s_0}^{(t)2}$ on a small meridian ball. All derivative losses below are fixed before the seed order is chosen.
```

## 9. Name the norms in the product estimates

Section 4. Replaces references to "the first" and "the second" by the actual norms, and uses the standard term submultiplicative.

Before:

```tex
The first is an algebra norm. Left multiplication preserves the second; right multiplication across a gap $\delta$ costs $C\delta^{-8}$, since $(1+k)/(1+l)\le1+|k-l|$. Finite rows and columns give a remainder in the second norm after a positive strip margin, with a fixed power of that margin as its only cost. These statements also hold coefficientwise in the family norms.
```

After:

```tex
The norm $|\cdot|_r$ is submultiplicative. Left multiplication preserves $|\cdot|_{r,8}$; right multiplication across a strip gap $\delta$ costs $C\delta^{-8}$, since $(1+k)/(1+l)\le1+|k-l|$. Finite rows and columns satisfy the latter bound after a positive strip loss, with polynomial cost. The same estimates hold in the coefficientwise family norms.
```

## 10. Explain the balancing step before its equation

Section 4. Says what the translation equation achieves, and establishes its zero-mean forcing before asking the reader to solve it.

Before:

```tex
The two principal amplitudes of \eqref{cap-operators} are $\beta_\pm(x)=b_T(\cos x,\cos(x\pm a),h)$. They are positive, and $\beta_+(-x)=\beta_-(x)$. Solve
\[
 (\Tr_a-\Tr_{-a})u=\log\beta_- -\log\beta_+,\qquad \av u=0,
 \qquad w_b=e^u,\qquad e_b=\beta_+\Tr_aw_b=\beta_-\Tr_{-a}w_b.
\]
The forcing is odd, so $u$ is even. Condition \eqref{homogeneous} bounds the inverse with a fixed derivative loss, including parameter differences. For sufficiently large fixed $s_0$, the strong bound $\|\gamma-\gamma_*\|_{r,s_0}^{(t)}=O(t)$ gives $w_b,e_b=1+O(t)$ at the same width.
```

After:

```tex
We first equalize the two principal amplitudes of \eqref{cap-operators}, $\beta_\pm(x)=b_T(\cos x,\cos(x\pm a),h)$. They are positive and satisfy $\beta_+(-x)=\beta_-(x)$, so $\log\beta_- -\log\beta_+$ is odd. Solve
\[
 (\Tr_a-\Tr_{-a})u=\log\beta_- -\log\beta_+,\qquad \av u=0,
 \qquad w_b=e^u,\qquad e_b=\beta_+\Tr_aw_b=\beta_-\Tr_{-a}w_b.
\]
The zero-mean solution $u$ is even. Condition \eqref{homogeneous} bounds the inverse with a fixed derivative loss, including parameter differences. For sufficiently large fixed $s_0$, the strong bound $\|\gamma-\gamma_*\|_{r,s_0}^{(t)}=O(t)$ gives $w_b,e_b=1+O(t)$ at the same width.
```

## 11. Connect the expansion order to the remainder estimate

Section 4, proof of Lemma 5. Names the weighted remainder norm being estimated, then gives the two frequency ranges and their common bound.

Before:

```tex
Expand through order eleven. For $p+q\le c\sqrt k$, the error is bounded
by $C(1+p+q)^Ck^{-12}$ times the tensor norm; for $p+q>c\sqrt k$,
bandwidth and positivity give $Ck^\alpha e^{-c\delta\sqrt k}$ across a
margin $\delta$. Both have the norm \eqref{matrix-norms} with cost
$C\delta^{-P}$, also for one parameter difference, which costs one
power of $k$ and one transfer moment.
```

After:

```tex
For the remainder norm $|\cdot|_{r',8}$, expand through order eleven. When $p+q\le c\sqrt k$, the error is bounded by $C(1+p+q)^Ck^{-12}$ times the tensor norm; otherwise bandwidth and positivity give $Ck^\alpha e^{-c\delta\sqrt k}$ across a strip gap $\delta$. Both contributions satisfy the required bound with cost $C\delta^{-P}$, also for a parameter difference, which costs one power of $k$ and one transfer moment.
```

## 12. Separate the symbolic calculation from compression

Section 4, end of Lemma 5. Announces the remaining operator construction, defines the projection Pi, and identifies which estimate receives the perturbative factor.

Before:

```tex
Exact symbolic multiplication follows by Taylor
expansion for transfers $|\nu|\le k/2$; the other transfers gain
$e^{-\delta k/2}$. Differentiate only the inverse-power polynomials;
the exact reference correction is a remainder. On $\lambda+2\Z$ retain
all Fourier output rows of the analytic symbols, extend perturbative
input columns below $\lambda$ by zero, references boundedly, and
identities by the identity. Compression has defect
$-\Pi A(I-\Pi)B\Pi$; an omitted intermediate index forces transfer at
least $k-\lambda$, so a margin absorbs every fixed input weight.
Finite exceptional columns obey the same bound. Every defect vanishes
at the sphere and therefore has a perturbative factor. This proves the
exact identity \eqref{normal-form} with width-independent operators.
```

After:

```tex
To obtain operators on $\Lambda_+$, use Taylor expansion for transfers $|\nu|\le k/2$ and the factor $e^{-\delta k/2}$ for the rest. Differentiate only the inverse-power polynomials, treating the exact reference correction as a remainder. On $\lambda+2\Z$, retain all Fourier output rows; below $\lambda$, extend perturbative input columns by zero, references boundedly, and identities by the identity. Let $\Pi$ project onto $\Lambda_+$. The compression defect $-\Pi A(I-\Pi)B\Pi$ requires a transfer of at least $k-\lambda$, so a strip gap absorbs every fixed input weight; exceptional columns satisfy the same bound. Every defect vanishes at the sphere. This proves \eqref{normal-form} and \eqref{reduction-estimate} with width-independent operators.
```

## 13. Identify which factor loses strip width

Section 5, proof of Proposition 6. Replaces "the left diagonal" and "recovery" with the diagonal inverse and the eliminated variables. The order of the Neumann inverse is unchanged.

Before:

```tex
The series is bounded at the source width; the left diagonal costs a
strip power. Recovery gives the claimed type of bound for $S_z$ and
uniqueness on smaller strips, hence width independence. Also
$S_z1=S_zf=0$ and $S_zT_\gamma\xi=\xi$ on the constrained subspace.
```

After:

```tex
The Neumann series costs no strip width; $\DD_{\Lambda'}^{-1}$ has polynomial cost across a gap. Recovering the finite variables gives the bound for $S_z$, and uniqueness on smaller strips makes it width-independent. Also $S_z1=S_zf=0$ and $S_zT_\gamma\xi=\xi$ on the constrained subspace.
```

## 14. Use dominated convergence for the fixed-gap limit

Section 5, proof of Proposition 6. Names the convergence argument and its majorant, including the bound needed for the Lipschitz term. Keeps the order of operator composition.

Before:

```tex
Indeed each fixed noncritical $d_k$ tends to $d_k^*(a_*)\ne0$, so both
$t\sup|d_k^{-1}|$ and $t^2\Lip(d_k^{-1})$ tend to zero. Their tails
across a gap $\delta$ are bounded uniformly by
$C((1+k)^2+(1+k)^5)e^{-\delta k}$, by \eqref{reciprocals}.
A finite-mode and tail split proves the limit for the diagonal;
the bounded series in \eqref{neumann} acts first, and finite recovery
and the changes of variables preserve the limit using fixed further
margins. Use such margins for all scalar pairings below.
```

After:

```tex
For fixed $k\in\Lambda'$, $d_k\to d_k^*(a_*)\ne0$ and $\Lip d_k=O(1)$ by \eqref{phase}. Hence $t\sup|d_k^{-1}|,\,t^2\Lip(d_k^{-1})\to0$. Across a fixed gap $\delta$, \eqref{reciprocals} gives the summable majorant $C((1+k)^2+(1+k)^5)e^{-\delta k}$. Dominated convergence proves the limit for the diagonal inverse. The bounded Neumann series acts first; recovering the finite variables and changing coordinates preserve the limit after further fixed strip losses. Use these gaps for the scalar pairings below.
```

## 15. Introduce the ansatz by the equations it solves

Section 5, proof of Proposition 6. Moves the purpose of the ansatz before its definitions and removes the repeated explanation after the display.

Before:

```tex
Put $v_0=1/\delta\vol K(1)$, $v_L=f-v_0\delta\vol K(f)$ and
\[
\begin{gathered}
 \psi_g=v_0g_0+S_z(g_E-T_\gamma v_0g_0),\qquad
 \psi_a=v_L-S_zT_\gamma v_L,\qquad \psi_\rho=-v_dS_zq,\\
 \psi=\psi_g+\delta\eps\,\psi_a+\delta\rho\,\psi_\rho,
 \qquad \delta\nu=v_d\delta\rho.
 \end{gathered}
\]
This solves the volume and complementary energy equations.
```

After:

```tex
To solve the volume and noncritical energy equations, put $v_0=1/\delta\vol K(1)$, $v_L=f-v_0\delta\vol K(f)$ and
\[
\begin{gathered}
 \psi_g=v_0g_0+S_z(g_E-T_\gamma v_0g_0),\qquad
 \psi_a=v_L-S_zT_\gamma v_L,\qquad \psi_\rho=-v_dS_zq,\\
 \psi=\psi_g+\delta\eps\,\psi_a+\delta\rho\,\psi_\rho,
 \qquad \delta\nu=v_d\delta\rho.
 \end{gathered}
\]
```

## 16. State which coefficient the first variation computes

Section 5, proof of Proposition 6. Links the variation directly to the critical matrix entry, and states why changes of parametrization do not alter that coefficient.

Before:

```tex
At fixed normal angle, differentiating the boundary integral gives
\[
 \dot T f=(dT_*+h_*C_*)(f^2)-(h_1+bf)C_*f,\qquad
 [\dot T f]_L=c_L((h_*-b)B-h_1)=\beta.
\]
There is no moving-boundary term because the kernel vanishes on the cutting plane.
Coordinate changes contribute an image of $T_*$ or a derivative of $T_*f=0$, with zero critical projection.
```

After:

```tex
To compute the critical coefficient, differentiate $T_\gamma f$ at fixed normal angle:
\[
 \dot T f=(dT_*+h_*C_*)(f^2)-(h_1+bf)C_*f,\qquad
 [\dot T f]_L=c_L((h_*-b)B-h_1)=\beta.
\]
The kernel vanishes on the cutting plane, so there is no boundary term. Coordinate changes lie in the range of $T_*$ or differentiate $T_*f=0$, and therefore have zero degree-$L$ coefficient.
```

## 17. Tie the iteration estimates to the next inverse

Section 5, proof of Theorem 1. Identifies the proposition whose hypotheses must persist and the Schur formula used to bound increments. Removes the vague phrase "finite Schur product".

Before:

```tex
The inverse hypotheses propagate by differences. On
$r_{j+1}=R_{j+1}-\delta_{j+1}$, Lemma~\ref{reduction} and the finite
Schur product give every increment of $Q,E,\widehat R$ the bound
$Ct^{-P}\delta_{j+1}^{-P}\|v_j\|_{R_{j+1},s_0}^{(t)}$; allocate part
of the margin to the finite row and column. These increments are
summable to $O(t^\kappa)$ after increasing $N$. Thus the initial
$O(t)$ operator bounds and the $O(t^2)$ seed neighborhood persist.
Restrictions decrease all norms, and on a common fixed strip
\begin{equation}\label{diagonal-increment}
 \sup_k|d_{j+1,k}-d_{j,k}|\le Ct^{\kappa2^j}.
\end{equation}
The phase estimates remain uniform.
```

After:

```tex
Proposition~\ref{inverse} remains applicable. On $r_{j+1}=R_{j+1}-\delta_{j+1}$, the difference bounds in Lemma~\ref{reduction} and \eqref{schur} give increments of $Q,E,\widehat R$ bounded by $Ct^{-P}\delta_{j+1}^{-P}\|v_j\|_{R_{j+1},s_0}^{(t)}$, reserving part of the strip gap for the finite couplings. For large $N$, their sum is $O(t^\kappa)$, preserving the $O(t)$ bounds and $O(t^2)$ seed neighborhood. Restrictions decrease norms, and on a common fixed strip
\begin{equation}\label{diagonal-increment}
 \sup_k|d_{j+1,k}-d_{j,k}|\le Ct^{\kappa2^j}.
\end{equation}
The phase bounds in \eqref{phase} remain uniform.
```

## 18. Make the initial measure argument explicit

Section 5, proof of Theorem 1. Replaces "eventually protected" by the actual divisor condition, then invokes dominated convergence instead of repeating the finite-mode and tail argument.

Before:

```tex
Every fixed noncritical mode is eventually protected by
$d_k^*(a_*)\ne0$. The bounds \eqref{measure} divided by $t$ have a
summable majorant, so a finite-mode and tail split gives
$|G^{\rm h}\setminus G_0|=o(t)$.
```

After:

```tex
Each fixed $k\in\Lambda'$ satisfies the $G_0$ divisor bound for small $t$, since $d_{0,k}\to d_k^*(a_*)\ne0$. The summable majorant in \eqref{measure}, divided by $t$, gives $|G^{\rm h}\setminus G_0|=o(t)$ by dominated convergence.
```

## 19. Explain what the frequency cutoff preserves

Section 5, proof of Theorem 1. Identifies the threshold decrease and explains that low modes retain their bounds before summing the exclusions over high modes.

Before:

```tex
At step $j$, put $K_j^*=\lfloor t^{-\kappa2^j/4}\rfloor$.
For $k\le K_j^*$ the ratio of \eqref{diagonal-increment} to the
threshold decrease is at most $C2^jt^{(\kappa/2)2^j-1}<1$.
Only larger modes can be removed, and \eqref{measure} gives
\[
 |G_j\setminus G_{j+1}|
 \le CM\{t^2(K_j^*)^{-1}+t(K_j^*)^{-2}\},\qquad
 \sum_j|G_j\setminus G_{j+1}|=o(t).
\]
```

After:

```tex
To bound the new exclusions, put $K_j^*=\lfloor t^{-\kappa2^j/4}\rfloor$. For $k\le K_j^*$, the ratio of the increment in \eqref{diagonal-increment} to $(\Gamma_j-\Gamma_{j+1})(1+k)^{-2}$ is at most $C2^jt^{(\kappa/2)2^j-1}<1$. These modes retain their divisor bounds. Summing \eqref{measure} over $k>K_j^*$ gives
\[
 |G_j\setminus G_{j+1}|
 \le CM\{t^2(K_j^*)^{-1}+t(K_j^*)^{-2}\},\qquad
 \sum_j|G_j\setminus G_{j+1}|=o(t).
\]
```

## 20. Attach convexity and analyticity to the right arguments

Section 5, conclusion. Makes clear that strict convexity comes from C2 closeness, while the graph in Y squared proves analyticity at the poles.

Before:

```tex
The meridian is
$C^2$-close to the circle. At the poles its parity and $Y'\ne0$ give
an analytic graph $X=\chi(Y^2)$; its revolution is therefore analytic
and strictly convex.
```

After:

```tex
The meridian is $C^2$-close to the circle, so the body is strictly convex. At the poles, parity and $Y'\ne0$ give the analytic graph $X=\chi(Y^2)$, so revolution preserves analyticity.
```

