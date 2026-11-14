# Exact replacements

These are proposed edits only. No file in `paper/` was edited. Each old string occurs exactly once in the audited source. The headings give the associated findings in REFEREE.md. Mathematical corrections have status PROVED-HERE in that report.

## E1, ERROR, Remark 4.10

Source line 751.

Old string:

```tex
The unsigned manuscript \cite{constructive2026} uses the integer polynomial $\sum\eps(r,s)z^{\omega(s)}$ and its coefficient of $(z-1)^m$, which is $\sum\eps(r,s)\binom{\omega(s)}{m}=\Sigma/m!$, because the sums of $\eps\,\omega^j$ with $j<m$ vanish by Lemma~\ref{lem:difference}.
```

New string:

```tex
The unsigned manuscript \cite{constructive2026} uses nonnegative integer incidence weights to obtain an integer polynomial of this form.
For our signed heights, $\sum\eps(r,s)z^{\omega(s)}$ is an integer Laurent polynomial.
Its expansion at $z=1$ has coefficient $\sum\eps(r,s)\binom{\omega(s)}{m}=\Sigma/m!$ in degree $m$, where the binomial coefficient has its usual polynomial meaning also for negative integers $\omega(s)$; the lower moments vanish by Lemma~\ref{lem:difference}.
```

## E2, IMPRECISION, Section 7 polynomial remark

Source line 918.

Old string:

```tex
Proposition~\ref{prop:good} is the statement $F\neq0$, read off at $w_{t,v}=1+\xi\kappa(t,v)$ with $\kappa=\sum_y\kappa_y$: each factor is then $\xi L(C)+O(\xi^2)$.
```

New string:

```tex
When a pair exists, Proposition~\ref{prop:good} proves $F\neq0$.
This can also be read off at $w_{t,v}=1+\xi\kappa(t,v)$ with $\kappa=\sum_y\kappa_y$: each factor is then $\xi L(C)+O(\xi^2)$, and the classes with the fewest cycles have a common leading sign.
```

## E3, IMPRECISION, Section 7 cycle-recovery remark

Source line 896.

Old string:

```tex
The complement $P$ of $C$ avoids $S_{s_C}$, because its side in each $t\in A$ contains $s_C(t)$ and its side in $t_0$ is $e_0$; so it is a perfect matching of the tree $Y_{s_C}$, and a tree has at most one perfect matching; hence $P=P_{s_C}$.
Conversely $s_{C}$ is recovered from $P_s$ when $C$ comes from $s$.
```

New string:

```tex
If $s_C$ is good, the complement $P$ of $C$ avoids $S_{s_C}$, because its side in each $t\in A$ contains $s_C(t)$ and its side in $t_0$ is $e_0$.
Thus $P$ and $P_{s_C}$ are perfect matchings of the tree $Y_{s_C}$, and a tree has at most one perfect matching, so $P=P_{s_C}$.
Conversely, when $C$ comes from a good state $s$, directing $P_s\setminus\{e_0\}$ out of $s(t)$ gives outdegree one at each nonroot and zero at each root.
On each rooted tree this is its orientation towards the root, so Lemma~\ref{lem:selections-give-states} recovers $s_C=s$.
This also proves that different good states give different cycles.
```

## E4, TYPO, Section 1 example

Source line 100.

Old string:

```tex
It has $12$ states and $8$ pairs, all listed in Table~\ref{tab:pairs}.
```

New string:

```tex
It has $12$ states and $8$ pairs; all eight pairs are listed in Table~\ref{tab:pairs}.
```

## E5, IMPRECISION, Section 7 computation range

Source line 908.

Old string:

```tex
Two octahedra glued along a face ($9$ vertices) give the smallest examples, with a pair for one choice of $t_0$ and none for another of the same colour (computed).
```

New string:

```tex
Two octahedra glued along a face ($9$ vertices) give the smallest examples, with a pair for one choice of $t_0$ and none for another of the same colour (computed over every face rooting of every Eulerian sphere triangulation with at most $12$ vertices).
```

## E6, GAP, Section 7 noncubic example

Source line 906.

Old string:

```tex
The incidence graph of the vertices and faces of the triangular bipyramid is planar, bipartite and $3$-connected with $11$ vertices, and its classes have sizes $5$ and $6$, so it has no Hamiltonian cycle.
```

New string:

```tex
The incidence graph of the vertices and faces of the triangular bipyramid has classes of sizes $5$ and $6$, so it has $11$ vertices and no Hamiltonian cycle.
It is planar by drawing each face centre joined to its three corners.
Here is also a check of $3$-connectivity.
The bipyramid has equatorial vertices $a,b,c$, apices $u,v$, and faces $uab,ubc,uca,vab,vbc,vca$.
Deleting at most two of its five vertices leaves a connected graph, as is seen directly from the equatorial triangle and the two apices.
If at most one face centre is deleted from the incidence graph, every surviving bipyramid edge is still represented by a two-edge path through one of its incident face centres, and every remaining face centre has a surviving corner.
If two face centres are deleted, no original vertex is deleted, and at most one bipyramid edge loses both its incident face centres, since two faces share at most one side.
The bipyramid stays connected after deleting one edge, and the surviving face centres all attach to it.
Thus the incidence graph stays connected after any two vertex deletions.
```

## E7, GAP, Section 7 two-connected example

Source line 907.

Old string:

```tex
The result is cubic, bipartite, planar and $2$-connected with $26$ vertices, and deleting the two new vertices leaves three components, which no Hamiltonian cycle allows.
```

New string:

```tex
The result is cubic, bipartite and planar with $26$ vertices.
To check $2$-connectivity, each cube with an edge removed is $2$-connected and joins the two new vertices by a path.
Deleting a new vertex leaves the three copies connected through the other new vertex.
Deleting a vertex of a copy leaves that copy connected to at least one new vertex, while the other two copies still connect the new vertices.
Deleting both new vertices leaves three components, so the graph is $2$-connected but has no Hamiltonian cycle.
```

## E8, IMPRECISION, Remark 4.10 final sentence

Source line 753.

Old string:

```tex
None of these arguments is constructive.
```

New string:

```tex
These nonvanishing arguments do not by themselves give an efficient construction.
```
