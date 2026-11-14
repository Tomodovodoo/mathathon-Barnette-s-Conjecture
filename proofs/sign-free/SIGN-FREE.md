# Good states without signs: what is proved and where it stops

The same text as `sign-free.pdf`, without the drawings. Generated from `sign-free.tex` by `research/2026-11-14_fable_sign-free-note/code/tex2md.py`.

**Abstract.** The proof of Barnette's conjecture rests on one lemma: a triangulation that has a pair of disjoint states has a good state, and the only known proofs get it from a signed count.
We collect what can be proved about this lemma with no sign at all.
A pair exists exactly when a certain spanning tree on the white faces exists, by Rado's theorem and one Euler count; each such tree lies in exactly one cover; the number of good states is even, by explicit involutions; and inside every cover each of the two conditions that define a good state can be met alone, by the theorems of Nash-Williams and Edmonds.
Both conditions cannot always be met inside one cover, as a triangulation with $16$ vertices shows, so a proof without signs has to move between covers.
We state the conjecture that would finish such a proof, with the range in which it has been checked and the natural stronger forms that fail.


## 1. The lemma and the question

We use the notation of the exposition [3].
$T$ is a simple triangulation of the sphere whose faces are coloured black and white so that every edge has one face of each colour.
One black face $t_0$ is drawn as the outer face, its corners are the *roots*, $A$ is the set of the other black faces, $X$ the set of vertices that are not roots, and $|A|=|X|=n$.
A *state* is a bijection $s\colon A\to X$ with $s(t)$ a corner of $t$, that is, a perfect matching of the incidence graph $\mathcal{B}$ on $A\cup X$.
$Q_s$ is the set of the $n$ sides opposite the corners $s(t)$, and $s$ is *good* if $Q_s$ is a forest with exactly one root in each component.
A good state yields a Hamiltonian cycle of the cubic graph dual to $T$ [3, Proposition 3.9].
A *pair* is two states $(r,s)$ with $r(t)\ne s(t)$ for all $t$; then $u(t)$ denotes the third corner of $t$.
The union of the two matchings of a pair is a spanning subgraph of $\mathcal{B}$ with all degrees two, which we call a *$2$-factor*.
A $2$-factor with $c$ cycles splits into two states in $2^{c-1}$ ways, and the $2^c$ ordered pairs obtained from it form one *cover* in the sense of [3]; we use the two words for the same object.

The key lemma is [3, Proposition 4.8], due to OpenAI [6].

**Theorem 1.1 (good-pair lemma).** 
If $T$ has a pair, then $T$ has a good state.

Every known proof gives each pair a sign, shows that the pairs whose second state is not good cancel, and shows by a second evaluation that the signed sum is not zero [6, 4, 1, 3].
The proof finds no good state.
It shows that the set of good states is not empty because a sum over it does not vanish.
Two things would be gained from a proof without signs.
The first is an algorithm: no polynomial-time construction of a Hamiltonian cycle in these graphs is known, and a direct argument might provide one.
The second is a reason.
The cancellation does not say why a good state exists, in the way Hall's theorem says why a matching exists.

This note records how far one gets with no sign.
Sections 3 to 6 contain complete proofs.
The existence of a pair, which [3] takes from a flow, is equivalent to the existence of a *rainbow tree*, a spanning tree on the white faces that meets one of the two conditions defining a good state (Theorems 3.1 and 4.2).
The good states are paired off by $n$ involutions, so their number is even (Theorem 5.3).
Inside every cover, each of the two conditions can be met alone (Theorems 6.5 and 6.9).
Section 7 shows where this stops.
One cover of a triangulation with $16$ vertices contains no good state, so every argument that stays inside a cover fails.
What is missing is Conjecture 7.2: from a rainbow tree, exchanges that never raise a certain excess reach a good state.
It holds for every instance with at most $17$ vertices.
Section 8 says what a proof of it would give.

Every statement below, proved or not, was also tested on all $262$ choices of $t_0$ in all Eulerian triangulations with at most $12$ vertices; Section 9 gives the ranges.

## 2. Good states as trees on the white faces

Put a centre $c(t)$ in every black face $t$, the outer face included, and join it to the three corners of $t$ by *spokes*.
The *spoke graph* $H$ has the $n+3$ vertices of $T$ and the $n+1$ centres as vertices and the $3n+3$ spokes as edges.
It is connected, because every edge of $T$ lies in a black face.
The *white-face graph* $W$ has the $n+1$ white faces as vertices, and one edge $e(t,v)$ for every spoke $(t,v)$, joining the two white faces that lie across the two sides of $t$ at $v$.
It can have parallel edges.

**Lemma 2.1 (duality).** 
$W$ is the plane dual of $H$, the edge $e(t,v)$ being dual to the spoke $(t,v)$.
So for a set $S$ of spokes, $H-S$ is a spanning tree of $H$ if and only if $\{e(t,v):(t,v)\in S\}$ is a spanning tree of $W$.

*Proof.* 
Let $w$ be a white face with corners $v_1,v_2,v_3$, and let $t_i$ be the black face across the side $v_iv_{i+1}$.
The closed curve $v_1,c(t_1),v_2,c(t_2),v_3,c(t_3)$ in $H$ bounds $w$ together with three thirds of black faces.
This region contains no vertex and no spoke, so it is a face of $H$.
Different white faces give different faces, and by Euler's formula $H$ has $(3n+3)-(2n+4)+2=n+1$ faces, so these are all.
The spoke $(t,v)$ lies between the two thirds of $t$ at $v$, which belong to the faces around the white faces across the two sides of $t$ at $v$.
The second sentence is the duality between spanning trees of a connected plane graph and of its dual [3, Lemma 2.5].
 ∎

**Definition.** 
A *rainbow tree* is a map $\sigma\colon X\to A$ with $x$ a corner of $\sigma(x)$ such that $F_\sigma=H-\{(\sigma(x),x):x\in X\}$ is a spanning tree of $H$.
The *load* of $t\in A$ is $c_\sigma(t)=|\sigma^{-1}(t)|$, and the *excess* is $\operatorname{exc}(\sigma)=\sum_{t\in A}|c_\sigma(t)-1|$.

In $F_\sigma$ the centre of $t$ keeps $3-c_\sigma(t)$ spokes and is not isolated, so every load is $0$, $1$ or $2$.
The excess is even, and it is zero exactly when $\sigma$ is a bijection.

**Lemma 2.3.** 
A state $s$ is good if and only if its inverse $\sigma=s^{-1}$ is a rainbow tree.
So the good states are the rainbow trees of excess $0$.

*Proof.* 
In $F_\sigma$ the centre of each $t\in A$ has degree two, and its neighbours are the ends of the side of $t$ in $Q_s$.
The centre of $t_0$ is joined to the three roots.
So $F_\sigma$ is $Q_s$ with every edge subdivided once, plus one new vertex joined to the roots.
It has $2n+3$ edges on $2n+4$ vertices, so it is a spanning tree exactly when it has no cycle, that is, when $Q_s$ is a forest in which no two roots share a component.
A forest with $n$ edges on $n+3$ vertices has three components, so this says that $s$ is good.
 ∎

By Lemmas 2.1 and 2.3, a good state is a spanning tree of $W$ that satisfies two conditions.
The *face condition* asks for exactly one edge $e(t,\cdot)$ for every black face $t\in A$.
The *vertex condition* asks for exactly one edge $e(\cdot,x)$ for every $x\in X$.
The face condition excludes $t_0$; the vertex condition excludes the roots.
A rainbow tree is a spanning tree of $W$ with the vertex condition (Figure 1).
A spanning tree with the face condition is, by the proof of Lemma 2.3, a choice of one corner in every $t\in A$, not necessarily a bijection onto $X$, whose opposite sides form a forest with one root in each component.

> **Figure 1** (drawn in `sign-free.pdf`; source `figures/`). Two rainbow trees on the example of [3], with $13$ vertices and roots $0,4,5$. Black faces are shaded and the grey collar is the outer face $t_0$. A solid wedge in the face $\sigma(x)$ at $x$ marks each removed spoke, and the dash-dotted edges $e(\sigma(x),x)$ form a spanning tree on the $11$ white faces, drawn as small circles. (a) Excess $2$: the dark face $\{1,2,9\}$ has load $2$ and the face $\{0,2,3\}$ with the dashed outline has load $0$. (b) Excess $0$, a good state. The example has $1792$ rainbow trees, six of them good states.

## 3. When a rainbow tree exists

A *separating triangle* is a $3$-cycle of $T$ with vertices on both sides.
It has *black inner boundary* if the three faces along its sides, on the side away from $t_0$, are black.
We use Rado's theorem in the following form [7], [8, Exercise 10.26]: subsets $X_1,\dots,X_m$ of the ground set of a matroid have an independent transversal if and only if the union of any $j$ of them has rank at least $j$.

**Theorem 3.1.** 
A rainbow tree exists if and only if no separating triangle of $T$ has black inner boundary.

*Proof.* 
For $x\in X$ let $C_x=\{e(t,x):t\ni x\}$.
These sets are disjoint, and $C_x$ is a closed walk through the white faces at $x$.
By Lemma 2.1 a rainbow tree is an independent transversal of $(C_x)_{x\in X}$ in the cycle matroid of $W$, whose rank is $n$.
Two walks $C_x$ and $C_y$ share a white face exactly when $xy$ is an edge of $T$.
So for $J\subseteq X$ the union of the $C_x$, $x\in J$, has one component for each component of the induced graph $T[J]$, and different components use disjoint sets of white faces.
Its rank is $w(J)-\operatorname{comp}(T[J])$, where $w(J)$ is the number of white faces with a corner in $J$.
Both $w$ and $|\cdot|$ add over the components of $T[J]$, so by Rado's theorem a rainbow tree exists if and only if

$$w(J)\ \ge\ |J|+1\qquad\text{for every nonempty } J\subseteq X \text{ with } T[J] \text{ connected.}\tag{3.2}$$

Fix such a $J$.
Let $U=V(T)\setminus J$, which contains the roots, and let $T[U]$ have $p$ vertices, $m$ edges and $c$ components.
The connected set $J$ lies in one face $\Phi$ of the plane graph $T[U]$.
Every other face of $T[U]$ contains no vertex of $T$ and no edge of $T$, since such an edge would join two vertices of $U$ and belong to $T[U]$; so it is a face of $T$.
Conversely a face of $T$ with all corners in $U$ is a face of $T[U]$ other than $\Phi$.
Let $b_U$ and $w_U$ count the black and the white faces of $T$ with all corners in $U$.
Let $d$ be the number of edge sides on the boundary of $\Phi$, and $\varsigma$ the sum over these sides of $+1$ or $-1$ according as the face of $T$ on the side of $\Phi$ is black or white.
Then

$$p-m+(b_U+w_U+1)=1+c,\qquad 2m=3(b_U+w_U)+d,\qquad \varsigma=3(w_U-b_U).$$

The first is Euler's formula and the second counts edge sides.
For the third, give every face of $T$ inside $\Phi$ the weight $+1$ or $-1$ on each of its three sides.
There are $n+1-b_U$ black and $n+1-w_U$ white faces inside, the two sides of an edge inside $\Phi$ cancel, and the boundary sides remain.
Solving, $w_U=p-c-d/2+\varsigma/6$.
Since $w(J)=n+1-w_U$ and $|J|=n+3-p$,

$$w(J)-|J|-1\ =\ (c-1)+\frac{3d-\varsigma-12}{6}.\tag{3.3}$$

The number $\varsigma$ is a multiple of $3$ with the parity of $d$, and $|\varsigma|\le d$.
The component of $T[U]$ that contains $t_0$ has a vertex adjacent to $J$, so it borders $\Phi$, and it is not a tree, so $d\ge3$.
If $c\ge2$, the right side of (3.3) is at least $1+(2d-12)/6=(d-3)/3\ge0$.
Let $c=1$.
If $d=4$ then $\varsigma=0$, if $d=5$ then $\varsigma\le3$, and if $d\ge6$ then $3d-\varsigma\ge2d\ge12$; in each case the right side is at least $0$.
If $d=3$, the right side is negative only for $\varsigma=3$.
The boundary of $\Phi$ is then a triangle $\Delta$, the three faces along it inside $\Phi$ are black, and $t_0$ lies on the other side.
If the other side contained no vertex, it would be the face $t_0$, and the faces along $\Delta$ inside $\Phi$ would be white.
So $\Delta$ is a separating triangle, and it has black inner boundary.
This proves (3.2) when there is no such triangle.

Conversely let $\Delta$ be a separating triangle with black inner boundary, and let $J$ be the set of the $I\ge1$ vertices inside it.
Let $B$ and $W'$ count the black and white faces inside $\Delta$.
Euler's formula and the count of sides for the disk give $B+W'=2I+1$, and the signed count of sides gives $3(B-W')=3$.
So $W'=I$.
Every white face with a corner in $J$ lies inside $\Delta$, so $w(J)\le|J|$ and the union of the $C_x$, $x\in J$, has rank less than $|J|$.
By Rado's theorem there is no rainbow tree.
 ∎

Rado's theorem is a case of matroid intersection, so a rainbow tree can be found in polynomial time when one exists.

## 4. Each rainbow tree lies in one cover

For a $2$-factor $F$ of $\mathcal{B}$, let $u(t)$ be the corner of $t\in A$ that is not joined to $t$ in $F$.
When $F$ is the union of a pair this is the third corner $u(t)$ of [3].
Let $G_u$ be the digraph on $V(T)$ with an arc $v\to u(t)$ for each of the two corners $v$ of $t$ joined to $t$ in $F$, for every $t\in A$.
Its arcs run along the two sides of $t$ at $u(t)$.
Every vertex of $X$ has outdegree two, one arc through each of its two faces in $F$, and the roots have outdegree zero (Figure 2).

**Lemma 4.1 (orientation).** 
Let $F$ be a $2$-factor, let $\sigma$ choose one edge $(x,\sigma(x))$ of $F$ at every $x\in X$, and let $(x,\sigma'(x))$ be the other one.
Then $F_\sigma$ is a spanning tree if and only if the $n$ arcs $x\to u(\sigma'(x))$ contain no directed cycle.
In that case $\sigma'(x)$ is the parent of $x$ in $F_\sigma$ rooted at the centre of $t_0$.

*Proof.* 
Direct the spoke $(\sigma'(x),x)$ from $x$ to the centre, the spoke $(t,u(t))$ from the centre of $t\in A$ to $u(t)$, and the three spokes of $t_0$ from the roots to the centre of $t_0$.
A spoke $(t,v)$ with $t\in A$ that is not in $F$ has $v=u(t)$, so these are all $2n+3$ spokes of $F_\sigma$ and each has one direction.
Every vertex of $H$ except the centre of $t_0$ has outdegree one.
A graph with $|V(H)|-1$ edges directed in this way is a spanning tree if and only if it has no directed cycle, and its edges then point to the parents.
A directed cycle avoids the roots, so it alternates $x\to c(\sigma'(x))\to u(\sigma'(x))$.
 ∎

For a rainbow tree $\sigma$, let $\operatorname{par}_\sigma(x)$ be the black face whose centre is the parent of $x$ in $F_\sigma$ rooted at the centre of $t_0$.

**Theorem 4.2.** 

(1) Every rainbow tree $\sigma$ lies in exactly one $2$-factor of $\mathcal{B}$, namely $\sigma\cup\operatorname{par}_\sigma$.

(2) Inside a $2$-factor $F$, the rainbow trees correspond to the sets of arcs of $G_u$ that contain one arc out of every vertex of $X$ and no directed cycle; $\sigma$ corresponds to the arcs $x\to u(\sigma'(x))$. Such a set is a spanning forest of $G_u$ directed towards the roots. The good states inside $F$ correspond to the sets that contain exactly one of the two arcs of every face.

(3) $G_u$ has a directed cycle if and only if $\mathcal{B}$ has a $2$-factor other than $F$. If $F$ is the only $2$-factor, all $2^n$ choices of $\sigma$ inside $F$ are rainbow trees and all states inside $F$ are good.

*Proof.* 
(1) In $F_\sigma$ the neighbours of $x\in X$ are the centres of its faces other than $\sigma(x)$, all in $A$.
So $\operatorname{par}_\sigma(x)\in A$ and $\operatorname{par}_\sigma(x)\ne\sigma(x)$.
The centre of $t\in A$ has $3-c_\sigma(t)$ neighbours, one of them its parent, so $t$ is the parent of $2-c_\sigma(t)$ vertices, none of them a root.
Hence every $t$ has degree $c_\sigma(t)+2-c_\sigma(t)=2$ in $\sigma\cup\operatorname{par}_\sigma$, which is a $2$-factor.
If $\sigma\cup\sigma'$ is any $2$-factor, Lemma 4.1 gives $\sigma'=\operatorname{par}_\sigma$.

(2) The first sentence is Lemma 4.1. A set of $n$ arcs with one arc out of every vertex of $X$ and no directed cycle leads from every vertex to a root. The arc from $v$ through $t$ is chosen exactly when $\sigma'(v)=t$, so one arc in every face means that $\sigma'$ is a bijection, and then so is $\sigma$.

(3) Let $v_1\to v_2\to\dots\to v_k\to v_1$ be a directed cycle, the arc $v_i\to v_{i+1}$ running through $t_i$.
Then $u(t_i)=v_{i+1}$, so the $t_i$ are distinct, and replacing every edge $(v_i,t_i)$ of $F$ by $(v_{i+1},t_i)$ gives another $2$-factor.
Conversely let $F'\ne F$ be a $2$-factor.
Every vertex meets as many edges of $F\setminus F'$ as of $F'\setminus F$, so the symmetric difference splits into closed trails that alternate between the two.
An edge $(v,t)$ of $F'\setminus F$ has $v=u(t)$, so each trail is a closed directed walk in $G_u$, which contains a directed cycle.
The last sentence follows from (2).
 ∎

> **Figure 2** (drawn in `sign-free.pdf`; source `figures/`). (a) The digraph $G_u$ of the $2$-factor that contains the rainbow tree $\sigma$ of Figure 1(a). Each face of $A$ carries two arcs, along its two sides at $u(t)$. $G_u$ has a directed cycle, $1\to8\to9\to1$, and the example has two $2$-factors. (b) The forest of $\sigma$ in dashed arrows: one arc $x\to u(\operatorname{par}_\sigma(x))$ out of each of the ten vertices that are not roots. The solid wedges mark $\sigma$. The face $\{0,2,3\}$ of load $0$ has both its arcs in the forest, and the face $\{1,2,9\}$ of load $2$ has none.

For a pair $(r,s)$ and $\sigma=s^{-1}$ the arcs of Theorem 4.2(2) are $r(t)\to u(t)$.
This is the orientation of $Q_s$ in [3, Lemma 4.2], and the statement that $s$ is good exactly when $Q_s$ has no cycle is the case of excess $0$.

**Corollary 4.3.** 
The following are equivalent: $T$ has a pair; $T$ has a rainbow tree; no separating triangle of $T$ has black inner boundary.

*Proof.* 
A rainbow tree lies in a $2$-factor by Theorem 4.2(1), and alternate edges along its cycles form a pair.
By Theorem 3.1 it remains to show that a separating triangle $\Delta$ with black inner boundary excludes a $2$-factor.
Let $I$ vertices lie inside $\Delta$.
All their faces lie inside, and there are $I+1$ black faces inside by the proof of Theorem 3.1.
The three black faces along the sides of $\Delta$ have one corner inside each, and every face has degree two in a $2$-factor.
So at most $3+2(I-2)=2I-1$ edges of a $2$-factor meet the $I$ inner vertices, and $2I$ are needed.
 ∎

The equivalence of the first and the third statement is [1, Theorem 1.2].
The exposition proves one direction, for triangulations without separating triangles, by a flow [3, Proposition 5.2].
There the max-flow min-cut theorem reduces the existence of a pair to the inequality $e(U)-b(U)\le2|U|-4$ for all sets $U$ of vertices that contain the roots, and Euler's formula proves it component by component.
Here Rado's theorem reduces it to (3.2), which concerns only complements of connected sets and follows from the exact identity (3.3).
Both arguments use planarity through one Euler count, and both are constructive.
The route through Rado gives more than a pair.
One half of the cover it produces is a rainbow tree, a selection whose arcs in $G_u$ have no directed cycle.
This already has the acyclicity that a good state needs and lacks only the face condition.

## 5. The exchange and the parity of the number of good states

**Lemma 5.1 (exchange).** 
For a rainbow tree $\sigma$ and $x\in X$ there is exactly one face $t'\ne\sigma(x)$ at $x$ such that $\sigma[x:=t']$, the map that sends $x$ to $t'$ and agrees with $\sigma$ elsewhere, is a rainbow tree.
Applying the exchange at $x$ to $\sigma[x:=t']$ returns $\sigma$.

*Proof.* 
The graph $F_\sigma+(\sigma(x),x)$ has exactly one cycle $\Gamma$.
It passes through $x$ and uses two spokes there, $(\sigma(x),x)$ and one other, $(t',x)$.
Deleting a spoke at $x$ leaves a spanning tree exactly when the spoke lies on $\Gamma$.
The second exchange sees the same graph and the same cycle.
 ∎

Write $\operatorname{alt}_\sigma(x)$ for $t'$ (Figure 3).
The exchange lowers the load of $\sigma(x)$ by one and raises the load of $t'$, which was at most $1$, by one.
So an exchange out of a face of load $2$ lowers the excess by $2$ if $t'$ was empty and leaves it unchanged otherwise.
Let $F$ be the $2$-factor of $\sigma$.
If giving $x$ its other face in $F$ closes no directed cycle in $G_u$, the result is a rainbow tree, so it is the exchange, and the exchange stays in $F$.
Otherwise the exchange leads to a rainbow tree in another $2$-factor.

A *walk state* is a triple $(\sigma,t,a)$ of a rainbow tree $\sigma$, a face $t$ of load $2$ and one of the two vertices of $\sigma^{-1}(t)$, the *arrival* $a$.
The other vertex $y$ is the *resident*.
A *step* moves the resident to $t'=\operatorname{alt}_\sigma(y)$.
If $t'$ was empty, the step *stops* with the rainbow tree $\sigma[y:=t']$.
Otherwise $t'$ had load $1$, and the step produces the walk state $\operatorname{step}(\sigma,t,a)=(\sigma[y:=t'],t',y)$.
The *mirror* of $(\sigma,t,a)$ is $\operatorname{mir}(\sigma,t,a)=(\sigma,t,y)$.

**Lemma 5.2 (reversal).** 
If $\operatorname{step}(S)=S'$, then $\operatorname{step}(\operatorname{mir}(S'))=\operatorname{mir}(S)$.
In particular $\operatorname{step}$ is injective.

*Proof.* 
Let $S=(\sigma,t,a)$ with resident $y$, so $S'=(\sigma',t',y)$ with $\sigma'=\sigma[y:=t']$.
In $\operatorname{mir}(S')$ the resident is $y$.
By Lemma 5.1 its exchange in $\sigma'$ leads back to $t$, which has load $1$ in $\sigma'$.
So the step produces $(\sigma,t,y)=\operatorname{mir}(S)$.
 ∎

> **Figure 3** (drawn in `sign-free.pdf`; source `figures/`). An exchange at the ringed vertex $x=8$. Thin lines are the spokes of $F_\sigma$, the three spokes of $t_0$ being omitted, and solid wedges mark the removed spokes. (a) The rainbow tree of Figure 1(a). Adding the removed spoke at $8$, dotted, closes the cycle $\Gamma$, drawn bold, through the centres of $\{8,11,12\}$, $\{4,10,11\}$, $\{3,4,9\}$ and $\{8,9,10\}$. (b) Removing the other spoke of $\Gamma$ at $8$ moves $8$ from $\{8,9,10\}$ to $\{8,11,12\}$. Both faces have load $1$ before the move, so the excess rises from $2$ to $4$.

**Theorem 5.3.** 
Let $n\ge1$, let $t\in A$, and let $s$ be a good state with inverse $\sigma$.
Move $x_0=s(t)$ to $t_1=\operatorname{alt}_\sigma(x_0)$ and take steps from the walk state $S_1=(\sigma[x_0:=t_1],t_1,x_0)$.
The walk stops, at the inverse of a good state $\iota_t(s)$.
The map $\iota_t$ is an involution on the set of good states and has no fixed point.
So the number of good states is even.

*Proof.* 
In $S_1$ the excess is $2$, the face $t$ is empty and $t_1$ has load $2$.
A step that does not stop keeps the excess, so in every walk state reached $t$ is the only empty face.
The walk therefore stops exactly when it moves a vertex into $t$, and then the excess is $0$ and the result is a good state by Lemma 2.3.

*The walk stops.*
Suppose $S_1=\operatorname{step}(S)$ for a walk state $S$.
By Lemma 5.2, $\operatorname{step}(\operatorname{mir}(S_1))=\operatorname{mir}(S)$ is a walk state.
But the resident of $\operatorname{mir}(S_1)$ is $x_0$, and its exchange leads back into the empty face $t$, so this step stops.
Hence $S_1$ is not in the image of $\operatorname{step}$.
An injective map on a finite set cannot return to an earlier element of the forward orbit of an element outside its image.
So the walk $S_1,S_2,\dots$ ends at some $S_m$ whose step stops, with a good state $s'$.

*Involution.*
Start from $s'$ at $t$.
The vertex $s'(t)$ is the resident of $S_m$, and its exchange returns it to the face of $S_m$, so the first walk state is $\operatorname{mir}(S_m)$.
By Lemma 5.2 the walk continues with $\operatorname{mir}(S_{m-1}),\dots,\operatorname{mir}(S_1)$, and the step from $\operatorname{mir}(S_1)$ puts $x_0$ into $t$ and stops at $s$.
So $\iota_t(s')=s$.

*No fixed point.*
If $s'=s$, the two walks are the same, so $S_i=\operatorname{mir}(S_{m+1-i})$ for all $i$.
For odd $m$ the middle state would equal its mirror, but the arrival and the resident differ.
For even $m$ the states $S_{m/2}$ and $S_{m/2+1}$ would have the same tree, but every step changes the tree.
 ∎

Figure 4 shows one orbit.
The proof uses no sign, no weight and no planarity beyond Lemma 5.1.
It does not give existence: if there is no good state, the statement is empty.
With Theorem 1.1 it shows that a triangulation with a pair has at least two good states.

> **Figure 4** (drawn in `sign-free.pdf`; source `figures/`). One orbit of the involution $\iota_t$ for the face $t=\{0,2,3\}$, dashed outline, in the example. In the good state $s$ the vertex $2$ lies in $t$. Its exchange moves it to $\{1,2,9\}$, which becomes the face of load $2$, drawn dark, in the walk state $S_1$ with arrival $2$, ringed, and resident $9$, boxed. The tree of $S_1$ is the one of Figure 1(a). The step moves $9$ to $\{3,4,9\}$ and gives $S_2$ with arrival $9$ and resident $3$. The next step moves $3$ into the empty face $t$ and stops at the good state $s'$.

## 6. Packing: each condition alone, inside any cover

For $U\subseteq V(T)$ let $e(U)$ be the number of edges of $T[U]$, let $b(U)$ be the number of black faces, $t_0$ included, with all corners in $U$, and let $\rho(U)$ be the number of roots in $U$.
For a black face $t$ write $j_t=|V(t)\cap U|$.
Every edge of $T$ lies in exactly one black face, and a black face with $3,2,1,0$ corners in $U$ has $3,1,0,0$ sides in $T[U]$, so

$$e(U)-b(U)=\sum_{t\ \mathrm{black}}\max(0,j_t-1).\tag{6.1}$$

**Lemma 6.2 (Euler identity).** 
Let $K$ be a connected induced subgraph of $T$ with $p\ge3$ vertices and $m$ edges.
Call a face of the plane graph $K$ a *region* if it is not a face of $T$.
Let $b$ be the number of black faces of $T$ with all corners in $K$, and for a region $\Psi$ let $d(\Psi)$ be the length of its boundary in edge sides and $\beta(\Psi)$ the number of black minus the number of white faces of $T$ inside it.
Then

$$m-b-(2p-4)=\tfrac12\sum_{\Psi}\bigl(\beta(\Psi)-d(\Psi)+4\bigr),$$

and $\beta(\Psi)\le d(\Psi)-4$ if $d(\Psi)\ge4$, while $\beta(\Psi)=\pm1$ if $d(\Psi)=3$, with $+1$ exactly when the three faces along the boundary inside $\Psi$ are black.

*Proof.* 
A face of $T$ with all corners in $K$ is a face of $K$.
Let $w$ count the white ones and $q$ the regions.
Euler's formula $p-m+b+w+q=2$ and the count of sides $2m=3b+3w+\sum d(\Psi)$ give $m-b-(2p-4)=\frac12\bigl(w-b-\sum(d(\Psi)-4)\bigr)$.
$T$ has as many black faces as white, so $w-b=\sum\beta(\Psi)$.
As in the proof of Theorem 3.1, $3\beta(\Psi)$ is a sum of $d(\Psi)$ terms $\pm1$, one for each boundary side.
This gives $\beta=\pm1$ for $d=3$, $\beta=0$ for $d=4$, $|\beta|\le1$ for $d=5$ and $|\beta|\le d/3\le d-4$ for $d\ge6$.
 ∎

**Lemma 6.3 (density).** 
If no separating triangle has black inner boundary, then for every nonempty $U\subseteq V(T)$

$$e(U)-b(U)+\max(0,\rho(U)-1)\ \le\ 2|U|-2 .\tag{6.4}$$

*Proof.* 
Edges and black faces with corners in $U$ lie in one component of $T[U]$, and so do the roots in $U$, which are pairwise adjacent.
Since $\sum_K(2p_K-2)\le2|U|-2$, it suffices to show $m-b\le2p-2-\max(0,\rho_K-1)$ for every component $K$, with $p,m,b$ as in Lemma 6.2 and $\rho_K$ roots.
For $p\le2$ this is clear.
For $p=3$, a path has $m-b=2$ and at most two roots.
A triangle that bounds a black face has $m-b=2$, and any other triangle has $m-b=3$ and at most two roots, because the triangle on the three roots bounds $t_0$.

Let $p\ge4$ and apply Lemma 6.2.
A region with $d\ge4$ contributes at most $0$.
A region with $d=3$ is one side of a $3$-cycle.
It contains a vertex of $T$, since it is not a face, and $K$ has a vertex on the other side.
So the $3$-cycle is a separating triangle.
If the region does not contain $t_0$, the hypothesis gives $\beta=-1$ and the contribution is $0$.
At most one region contains $t_0$, and it contributes at most $1$.
Hence $m-b\le2p-4+\epsilon$, where $\epsilon=1$ if $t_0$ lies in a triangular region and $\epsilon=0$ otherwise.
If $\rho_K=3$ then $t_0$ is a face of $K$, so $\epsilon=0$.
If $\rho_K\le2$ then $2p-3\le2p-2-\max(0,\rho_K-1)$.
 ∎

We use two theorems on packing.
Nash-Williams [5], [8, Exercise 10.29]: the edges of a multigraph without loops can be partitioned into $k$ forests if and only if every nonempty set $Z$ of vertices spans at most $k(|Z|-1)$ edges.
Edmonds [2], [9, pp. 1674 and 1685-1686]: in a digraph with a vertex $\varrho$, the largest number of pairwise arc-disjoint spanning trees directed towards $\varrho$ equals the smallest number of arcs leaving a nonempty set of vertices that does not contain $\varrho$.
The source states this for trees directed away from $\varrho$; reverse all arcs.

A *deleted-corner map* $u$ chooses a corner $u(t)$ of every $t\in A$.
Every $2$-factor has one, but most deleted-corner maps come from no $2$-factor.

**Theorem 6.5 (two trees on the white faces).** 
Suppose no separating triangle has black inner boundary, and let $u$ be a deleted-corner map.
Then the $2n$ edges $e(t,v)$ of $W$ with $t\in A$ and $v\ne u(t)$ can be partitioned into two spanning trees of $W$.
In particular the edges of $W$ that belong to a cover form two spanning trees of $W$.

*Proof.* 
Let $M_u$ be the multigraph obtained from $H$ by doubling the three spokes of $t_0$ and the spokes $(t,u(t))$, $t\in A$.
It has $6+2n+2n=2(|V(H)|-1)$ edges.
Let $Z$ be a set of vertices of $H$, let $U=Z\cap V(T)$, and let $\mu_t$ be the number of edges of $M_u$ from the centre of $t$ to $U$.
If $U$ is empty, $Z$ spans no edge.
Otherwise $Z$ spans at most $2(|Z|-1)$ edges for every choice of centres in $Z$ exactly when

$$\sum_{t\ \mathrm{black}}\max(0,\mu_t-2)\ \le\ 2|U|-2 .\tag{6.6}$$

For $t_0$ the term is $2\max(0,\rho(U)-1)$.
For $t\in A$ we have $\mu_t=4$ if $j_t=3$, $\mu_t=3$ if $j_t=2$ and $u(t)\in U$, and $\mu_t\le2$ otherwise, so the term is at most $\max(0,j_t-1)$.
By (6.1), in which $t_0$ accounts for $\max(0,\rho(U)-1)$, the left side of (6.6) is at most $e(U)-b(U)+\max(0,\rho(U)-1)$, and Lemma 6.3 gives (6.6).
By the theorem of Nash-Williams, $M_u$ is the union of two forests.
By the count of edges both are spanning trees, and each contains one copy of every doubled spoke.
So the complement in $H$ of each of them is the part of the single spokes that lies in the other, and by Lemma 2.1 these two parts are spanning trees of $W$.
 ∎

**Remark 6.7.** 
The hypothesis is needed.
Let $\Delta$ be a separating triangle with black inner boundary, let $t_1,t_2,t_3$ be the black faces inside along its sides, and let $u(t_i)$ lie on $\Delta$ for each $i$.
For the set $U$ of vertices on or outside $\Delta$, Lemma 6.2 gives $e(U)-b(U)=2|U|-3$, every term of (6.6) equals its bound, and the left side of (6.6) is $2|U|-1$.
So the edges do not split.

**Theorem 6.8 (two forests in $T$).** 
Suppose no separating triangle has black inner boundary, and let $u$ be a deleted-corner map.
Then the $2n$ sides of the faces $t\in A$ at the corners $u(t)$ can be partitioned into two spanning forests of $T$, each with three components and one root in each component.
For a pair $(r,s)$ these sides are $Q_r\cup Q_s$.

*Proof.* 
Identify the three roots to one vertex $\varrho$.
The resulting multigraph $T/R$ has $n+1$ vertices, and the $2n$ sides give no loops, because an edge between two roots is a side of $t_0$.
A face $t\in A$ with $j_t$ corners in a set has at most $\max(0,j_t-1)$ of its two sides inside it.
Let $S$ be a nonempty set of vertices of $T/R$.
If $\varrho\notin S$, then by (6.1) and Lemma 6.3 the sides inside $S$ number at most $e(S)-b(S)\le2|S|-2$.
If $\varrho\in S$, let $U$ consist of $S\setminus\{\varrho\}$ and the three roots, so $|U|=|S|+2$; the sides inside number at most $e(U)-b(U)-2\le2|U|-6=2|S|-2$.
By the theorem of Nash-Williams the sides form two forests of $T/R$, with $2n$ edges, hence two spanning trees.
A spanning tree of $T/R$ is a spanning forest of $T$ with one root in each of its three components.
In a pair, the side of $t$ opposite $r(t)$ joins $s(t)$ and $u(t)$, and the side opposite $s(t)$ joins $r(t)$ and $u(t)$.
 ∎

**Theorem 6.9 (two rainbow trees in every cover).** 
Suppose no separating triangle has black inner boundary.
Then every $2$-factor $F$ of $\mathcal{B}$ is the union of two rainbow trees $\sigma$ and $\sigma'$.

*Proof.* 
Merge the roots of $G_u$ into one vertex $\varrho$.
By Lemma 4.1, a splitting $F=\sigma\cup\sigma'$ into two rainbow trees is a partition of the arcs into two spanning trees directed towards $\varrho$.
Conversely two such trees without a common arc have $n$ arcs each, one out of every vertex of $X$, so they use all arcs and give a splitting.
By the theorem of Edmonds they exist if at least two arcs leave every nonempty $Y\subseteq X$.
Every vertex of $Y$ has outdegree two, so this says that at most $2|Y|-2$ arcs have both ends in $Y$.
A face $t$ has such arcs only if $u(t)\in Y$, and then at most $j_t-1$ of them.
By (6.1) and Lemma 6.3 with $\rho(Y)=0$ their number is at most $e(Y)-b(Y)\le2|Y|-2$.
 ∎

**Corollary 6.10.** 
Suppose no separating triangle has black inner boundary, and let $F$ be a $2$-factor.
Then some spanning tree of $W$ made of edges of $F$ satisfies the vertex condition, and some other one satisfies the face condition.

*Proof.* 
The first is Theorem 6.9.
For the second, the $2n$ edges of $F$ in $W$ are two forests by Theorem 6.5, so every subset $Y$ of them has rank at least $|Y|/2$.
The $n$ sets $\{e(t,v):v\ne u(t)\}$ are disjoint and have two elements each, so the union of any $j$ of them has rank at least $j$.
Rado's theorem gives an independent transversal, which is a spanning tree with the face condition.
 ∎

## 7. Where it stops

### A cover with no good state

A good state inside a $2$-factor $F$ is a spanning tree made of edges of $F$ that meets both conditions.
Corollary 6.10 meets each of them alone.
Both together can fail.

**Proposition 7.1.** 
Let $T$ be the Eulerian triangulation with $16$ vertices of Figure 5, with outer face $\{0,1,2\}$.
It has no separating triangle with black inner boundary, three $2$-factors and $12$ good states.
One of the $2$-factors is a single cycle through all $13$ vertices of $X$, and neither of its two states is good.
It contains $6144$ rainbow trees, all of positive excess.

This is a finite computation.
The triangulation is number $27$, counted from $0$, in the list of Eulerian triangulations with $16$ vertices produced by `plantri -b -a 16`; its faces are listed in `figures/figdata.json`.
For each of the two states, $Q_s$ contains a directed triangle, drawn bold in the figure.
No cover without a good state exists up to $12$ vertices.

> **Figure 5** (drawn in `sign-free.pdf`; source `figures/`). The cover of Proposition 7.1. (a) The triangulation, with outer face $\{0,1,2\}$ as the grey collar, and the cover: one side in every face of $A$, forming a single cycle through the $13$ inner vertices. (b) One of its two states, as solid wedges, with $Q_s$ directed from $r(t)$ to $u(t)$ in dashed arrows; the directed triangle $5\to13\to14\to5$ is bold. (c) The other state; the directed triangle is $9\to12\to14\to9$. Theorems 6.5 to 6.9 hold for this cover.

So no argument that works inside one cover can prove Theorem 1.1.
Theorems 6.5 to 6.9 hold for every deleted-corner map or every cover, the bad one included, and therefore cannot tell a cover that contains a good state from one that does not.
The signed proof moves between covers as well.
Its cancellation reverses a cycle of $Q_s$, which changes the cover, and its second evaluation sums over all covers with the fewest cycles.
Here the move between covers is the exchange of Lemma 5.1 at a vertex whose other arc would close a directed cycle in $G_u$.

### The missing step

**Conjecture 7.2 (Step X).** 
Let $T$ have no separating triangle with black inner boundary.
Then for every rainbow tree $\sigma$ there are rainbow trees $\sigma=\sigma_0,\sigma_1,\dots,\sigma_k$ such that $\sigma_{i+1}$ arises from $\sigma_i$ by one exchange, $\operatorname{exc}(\sigma_{i+1})\le\operatorname{exc}(\sigma_i)$ for all $i$, and $\operatorname{exc}(\sigma_k)=0$.

With Theorem 3.1 and Lemma 2.3 this implies Theorem 1.1.
The conjecture has been checked by exhaustive enumeration of all rainbow trees for every choice of $t_0$ in every Eulerian triangulation with at most $17$ vertices, and in $1492$ of the $1543$ triangulations with $18$ vertices; the other $51$ exceeded the time limit of the runs.
In samples of larger triangulations, up to $120$ vertices, every rainbow tree tried could be brought to excess $0$ by such a sequence.
When $\mathcal{B}$ has only one $2$-factor the conjecture holds by Theorem 4.2(3): all choices inside the $2$-factor are rainbow trees, and moving the second vertex of a face of load $2$ onwards along its cycle, face after face, reaches an empty face without raising the excess.

Three stronger statements would give a proof or an algorithm at once, and all three fail.

*Strict descent.* A rainbow tree of positive excess need not have an exchange that lowers the excess.
The smallest examples are in the triangulation with $8$ vertices, where $120$ rainbow trees have none; up to $12$ vertices there are $8782$.
So a path as in Conjecture 7.2 must cross plateaus of constant excess.

*The deterministic walk.* The walk of Section 5, started at an arbitrary walk state, need not stop.
Periodic walks exist in triangulations with $38$ vertices, with periods $48$ and $68$, and with $40$ vertices, with period $60$.
None exists up to $15$ vertices.
Theorem 5.3 escapes them only because its first walk state has no predecessor.

*Convexity of loads.* If the set of load vectors of rainbow trees satisfied the exchange axiom of M-convex sets, a Hall-type condition would decide whether the vector with all loads $1$ belongs to it.
The axiom fails in a triangulation with $12$ vertices that has two $2$-factors.

The involutions $\iota_t$ do not help with existence, and they do not connect the good states either: for $13$ and $14$ vertices there are instances in which the group they generate is not transitive on the good states.

### Two sister conjectures

Two other attempts at Theorem 1.1 without signs stop at statements of the same shape, and at the same obstacle.

*Monotone descent on pairs.*
For a pair $(r,s)$ let $q$ be the number of cycles of $Q_s$, so that $s$ is good when $q=0$.
Two moves are available, reversing a cycle of $D(r,s)$ and reversing a cycle of $Q_s$.
The conjecture is that from every pair a good pair can be reached by such moves without ever raising $q$.
It was confirmed for all pairs up to $20$ vertices by two independent programs; the original program reports $193 623 384$ pairs up to $23$ vertices.
A move that lowers $q$ need not exist, first at $16$ vertices, and examples with $21$ and $40$ vertices need three and four moves before $q$ falls.
Paths that never raise the number of cycles of the cover fail at $16$ vertices, so again the cover has to change.

*Induction by contraction.*
Contracting two opposite edges at a vertex of degree four gives a smaller Eulerian triangulation, and a good state of the smaller one lifts back in exactly one way, which may fail to be good; a rotation at three faces repairs most failures.
Two statements are missing.
The first is that for more than $6$ vertices and no separating triangle, some vertex of degree four that is not a root has a contraction that is simple and has a pair.
The second is that where both contractions at such a vertex have good states, one of them has a good state whose lift or rotated lift is good.
No counterexample to either is known, and the second was confirmed, in a stronger counting form, for all contractions up to $18$ vertices.
An example with $18$ vertices has a good state in a cover with one cycle whose lift fails and whose only other state in that cover is not good, so a repair must change the cover here too.

In all three settings a number that should reach zero cannot be lowered step by step, and the moves that keep it constant leave the cover.
We know no quantity that decreases along them.

## 8. What a proof of Step X would give

Suppose Conjecture 7.2 were proved.
Theorem 3.1 supplies a rainbow tree whenever no separating triangle has black inner boundary, the conjecture carries it to a good state, and Theorem 4.2(1) hands over the partner.
That is Theorem 1.1 with no signed count, no weight and no sum over covers.
Planarity would enter through the identity (3.3) and through whatever the proof of the conjecture uses.
Barnette's conjecture would follow by the remaining steps of [3], which use no cancellation: the passage from a good state to a Hamiltonian cycle and the gluing along separating triangles.
Theorem 5.3 would then give a second good state.

It would not give a polynomial-time algorithm.
The conjecture asserts that a path exists.
Strict descent is false, the deterministic walk can cycle, and nothing bounds the search on a plateau.
In the exhaustive range the plateau search needed depth at most $7$, and at most $27$ in the sampled examples up to $120$ vertices, which leaves the question open in both directions.
It would not count the good states, and it would not explain the nonvanishing of the signed sum.

Nothing in Section 6 brings the conjecture closer in a direct way, for the reason given after Proposition 7.1.
The place to look is the exchange that leaves the cover.
A rainbow tree is an acyclic choice of arcs in $G_u$, its excess counts the faces with both arcs or no arc chosen, and correcting a face along a cycle of the cover works until the new arc closes a directed cycle.
That is the same event as a cycle of $Q_s$ in the signed proof, where the disk identity [3, Lemma 3.8] controls it.
The disk identity is not used anywhere in this note, and we expect that a proof of Conjecture 7.2 has to use it.

## 9. What was computed

All statements of Sections 2 to 6 were tested by one program written for this note, on every choice of the outer face in every Eulerian triangulation with $6$ to $12$ vertices.
There are $262$ such instances, $208$ of them without a separating triangle with black inner boundary, and they have $74 432$ rainbow trees and $620$ good states.
The program checks Lemma 2.1 on $440 000$ sets of spokes, Lemma 2.3 on all $1706$ states, the identity (3.3) on all $57 901$ connected sets $J$, Theorem 4.2 for every rainbow tree and every $2$-factor, Lemma 5.1 at every vertex of every rainbow tree, Lemma 5.2 on all $325 536$ walk states, Theorem 5.3 in $5052$ evaluations of $\iota_t$, Lemma 6.3 on every set of vertices, and Theorems 6.5 to 6.9 and Corollary 6.10 on all $210$ covers and $82 118$ deleted-corner maps.
It also confirms Conjecture 7.2 and the count for strict descent in this range.
The counts agree with those of two earlier independent programs.
Proposition 7.1 is recomputed by the script that draws the figures.
The statements about more than $12$ vertices in Section 7, other than Proposition 7.1, are quoted from the project's earlier runs and were not recomputed here; the file `STATUS.md` next to this note names the program and the range for each.

## References

[1]  *A constructive proof of Barnette's conjecture*, unsigned manuscript, dated 18 October 2026.

[2]  J. Edmonds, *Edge-disjoint branchings*, in: Combinatorial Algorithms (R. Rustin, ed.), Academic Press, New York, 1973, pp. 91-96.

[3]  *The proof of Barnette's conjecture: an exposition*, manuscript, 14 November 2026, in the same repository as this note (`paper/main/barnette.pdf`).

[4]  Z. Li, *A note on the proof of Barnette's conjecture*, arXiv:2610.30490v1, 2026.

[5]  C. St. J. A. Nash-Williams, *Decomposition of finite graphs into forests*, J. London Math. Soc. **39** (1964), 12.

[6]  OpenAI, *Paired states and Hamiltonian cycles in cubic bipartite planar graphs*, preprint, 24 September 2026.

[7]  R. Rado, *A theorem on independence relations*, Quart. J. Math. Oxford Ser. **13** (1942), 83-89.

[8]  A. Schrijver, *A course in combinatorial optimization*, lecture notes, CWI, Amsterdam, version of 23 March 2017.

[9]  A. Schrijver, *Polyhedral combinatorics*, in: Handbook of Combinatorics (R. L. Graham, M. Grötschel, L. Lovász, eds.), Elsevier, Amsterdam, 1995, Chapter 30, pp. 1649-1704.
