# Bounded audit of the final forest certificate

## Audit boundary

PROVED-HERE. We audit only the final conversion used in O §6.2, not the existence of its certificate. Let T be a finite simple connected sphere triangulation. Assume P is a spanning forest of T and exactly one side of every triangular face belongs to P. Let C be the spanning subgraph of T* consisting of edges dual to E(T)\P. The conclusion is that C is a Hamiltonian cycle of T*.

Accepted primitives: the given hypotheses; the definition of a plane dual with edge-side incidences; the definition of a Hamiltonian cycle; Euler's formula; contraction of a non-loop tree edge in a plane embedding, which deletes its dual edge while preserving faces; and elementary finite graph degree counts. No statement asserting the desired Hamiltonian cycle or the existence of P is accepted as a primitive.

## Obligation graph

```text
C0: C is a Hamiltonian cycle
  <- R0, characterization by degree and connectedness
     AND O1, C1, C2, O2
C1: C has degree two at every vertex
  <- R1, dual incidence count
     AND O3, O4, O5
C2: C is connected
  <- R2, complementary forest duality
     AND O6, C3
C3: complementary edges of a spanning tree dualize to a connected graph
  <- R3, contract the primal tree
     AND O7, O8
```

The source supplies this route. The two induced trees are useful later for gluing; they are not an additional premise needed for this bounded conversion. There is no OR branch replacing connectivity by a degree count.

## Critical findings and full local proof

PROVED-HERE. Extend P to a spanning tree U of T by repeatedly adding an edge between distinct forest components. Such an edge exists until there is only one component because T is connected. Contract U in the sphere embedding. The resulting plane graph has one vertex and the same faces as T; its dual is connected, and its edges are precisely the duals of E(T)\U. One elementary justification of dual connectedness is to join points in two faces by a curve transverse to finitely many edges and avoiding vertices; successive crossed edges give a dual walk. Since E(T)\U is contained in E(T)\P, C contains a connected spanning subgraph and is connected.

Each vertex of T* corresponds to a triangular face of T. Exactly one of its three sides belongs to P, leaving exactly two incident dual edges in C, counted with multiplicity. Thus C has degree two everywhere. A finite connected degree-two graph is one cycle: follow an edge, continue through the other incident edge, and stop at the first repetition. Degree two makes the first repeated vertex the starting vertex and prevents any edge leaving the resulting cycle. Connectedness excludes vertices outside it. Here T has at least four faces, so C is not a one-vertex loop or a two-vertex parallel-edge cycle. It visits every dual vertex once and is a Hamiltonian cycle.

This proves the local implication. It does not prove that P exists. In a whole-proof audit, existence must expand through the selection rule, its acyclicity proof, the forest-state proposition, initial pair and separator induction. Treating that unproved construction as a definition would be a missing obligation.

## Dependency table

| ID | Exact claim or obligation | Needed by | Route / edge | Classification | Support | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C0 | C is Hamiltonian in T* | root | R0 | root | C1, C2, O1, O2 | discharged |
| O1 | C spans the vertices of T* | C0 | R0 / AND | definition | C defined as spanning subgraph | discharged |
| C1 | Every vertex has degree two in C | C0 | R0 / AND | major claim | R1 | discharged |
| C2 | C is connected | C0 | R0 / AND | major claim | R2 | discharged |
| O2 | Finite connected spanning degree-two graph here is a Hamiltonian cycle | C0 | R0 / AND | algebraic/logical step | Traversal argument above; at least four faces | discharged |
| O3 | Each face of T has three distinct sides | C1 | R1 / AND | hypothesis | Simple triangulation | discharged |
| O4 | Exactly one of those sides is in P | C1 | R1 / AND | hypothesis | Certificate contract | discharged |
| O5 | Remaining sides count dual incidences | C1 | R1 / AND | definition | Plane dual | discharged |
| O6 | P extends to a spanning tree U and C contains the complementary dual of U | C2 | R2 / AND | algebraic/logical step | Add intercomponent edges; complement inclusion | discharged |
| C3 | Complementary dual of U is connected | C2 | R2 / AND | major claim | R3 | discharged |
| O7 | Contracting U preserves faces and deletes exactly its dual edges | C3 | R3 / AND | algebraic/logical step | Accepted plane contraction operation, iterated | discharged |
| O8 | The dual of the remaining connected plane graph is connected | C3 | R3 / AND | algebraic/logical step | Transverse face-to-face curve above | discharged |

## Verdict

FOLLOWS, for this conditional certificate conversion only. All obligations of R0 close, especially the distinct connectivity obligation C2. No verdict on the construction of P, the three full papers, or the floating-body theorem is implied.
