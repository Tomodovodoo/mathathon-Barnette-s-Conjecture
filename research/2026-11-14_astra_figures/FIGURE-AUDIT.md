# Figure audit

I inspected rendered PDF pages, not just text extraction. `python paper/figures/audit_render.py` produced the page images in `source-renders/`. Page numbers below are PDF page numbers. Width estimates are visual ratios to the text block, not measurements of individual PDF paths. The extra renders of Li p.13 and OpenAI p.10 contain rules or symbols, not figures.

## Original, OpenAI

LIT source: *Paired states and Hamiltonian cycles in cubic bipartite planar graphs*, September 24, 2026, Figure 1, p.8.

| Panel | What works | What fails |
|---|---|---|
| 1a, local paired-state edges | The triangle makes the distinction between the directed edge of D and the opposite edge of Q visible. Solid and dashed strokes survive greyscale. | The entire pair of diagrams occupies roughly 0.60 textwidth, each triangle about 0.23. Labels look about 80% of body size. Thin grey boundary edges disappear before the bold arrows do. The face name sits in ample empty space, but there is no global state, bijection, or directed cycle. |
| 1b, spoke detour | Blue distinguishes the two-spoke route; the excluded third corner is visible. A light grey subdisk explains the isotopy. | The route and shading are small. Blue becomes an ordinary dark stroke in greyscale, so the solid/dashed distinction does the work. The same face-centre letter and face name can be confused. There is no view showing disjoint detours around a complete cycle. |

The combined caption is unusually useful: it defines the arrows and says which corner the shaded disk excludes. The figure first appears on p.8, after its references on pp.6 and 7. The argument about global simple curves has to be imagined before the diagram arrives.

## Li's note

LIT source: Zhentao Li, *A note on the proof of Barnette's conjecture*, arXiv:2610.30490v1, October 21, 2026.

| Figure | What works | What fails |
|---|---|---|
| 1a, rooted primal graph, p.2 | Black and hollow nodes identify the bipartition; the chosen outer edge has a clear label. | Three columns reduce each graph to about 0.23 textwidth. Labels are around two thirds of body size. The graph has no vertex names to support later tracing. |
| 1b, auxiliary graph, p.2 | Keeps the primal positions, showing where face vertices enter. | Many thin grey incidences overlap the visual field. The outer face is represented by long arcs with little clearance near its label. The caption merely names the object. |
| 1c, incidence graph and H, p.2 | Shared geometry preserves correspondence with 1b; solid versus pale context conveys deletion. | Near-white context and tiny square vertices disappear in greyscale printing. The root is easier to see than the removed neighbourhood. Caption colour descriptions are insufficient when copied in monochrome. |
| 2a, two matchings, p.2 | Teal solid and orange dashed edges encode two choices redundantly. Larger than Figure 1, about 0.35 textwidth per panel. | Some remaining context vertices are barely visible. The figure does not expose a failed matching or a cycle-breaking move. |
| 2b, tree and cotree, p.2 | Purple open circles separate white vertices from black tree vertices. Shows the outer routing. | Arrowheads, dashed edges and curved boundaries compete in a small panel. The cotree needs a more explicit legend. |
| 2c, traced tree and P, p.2 | Red selected edges and arrow direction are easy to locate in colour. | Label scale differs from the drawing above. Red solid versus black solid relies on colour where a dash pattern or weight distinction would help. |
| 2d, final cycle, p.2 | Bold blue cycle and dashed red complement make the conclusion immediate. | The caption lists graphs rather than explaining why connectedness now follows. The two rows do not clearly identify the transformation that preserves which object. |
| 3, ray intersections, p.6 | Orthogonal cycle geometry is clear. Orange dashed and teal solid persist in greyscale; paired intersections have explicit names. The interior and exterior rays show different parity. | The diagram is roughly 0.37 textwidth, with explanations alongside it. Intersection labels are small and cluster near the upper crossings. The caption names the drawing; the actual pairing rule is deferred to the text. |

Figures 1 and 2 follow their first references on p.1 and occupy most of p.2. This is reasonable placement for an overview, though readers must turn back from later constructions. Figure 3 precedes some of the definitions it illustrates; its meaning becomes clear only after reading down the page. Li's repeated geometry is the strongest design choice among the three sources.

## Constructive exposition

LIT source: *Constructing Hamiltonian cycles*, supplied `barnette_trees.pdf`.

| Figure | What works | What fails |
|---|---|---|
| 1a and 1b, cube two-factors, p.2 | Same size and coordinates. Bold versus thin strokes show exactly what changes. Monochrome works. The caption states the actual distinction, connectedness. | Combined drawing about 0.52 textwidth, each cube about 0.21. Large unused page width. No connection yet to the dual example. First reference is on p.1. |
| 2a, rooted forest, p.5 | Light black-face shading, root labels, and bold Q edges connect notation to a small complete example. | Many labels are about 70% of body size. The lower central labels are tight. This panel is about 0.28 textwidth. There is no visible state mark, so the reader cannot check which corner supplied each opposite edge. |
| 2b, incidence tree, p.5 | Solid retained spokes and dashed deleted spokes are a good monochrome convention. The external root centre makes the sphere construction concrete. | Its vertical extent exceeds 2a's, making equal combinatorial features look differently scaled. The top outer arc and root label are close. The caption requires the reader to distinguish face names from centre names unaided. |
| 3a, local edges, p.7 | Same solid/dashed convention as the original; labels name the two edges explicitly. | This is again a local triangle, about 0.20 textwidth. It cannot show either exchange globally, and no other figure fills that gap. |
| 3b, spoke detour, p.7 | Monochrome route and shaded subdisk survive copying. Third corner is visible. | Small subfigure and low-contrast shading make the excluded region hard to inspect. Caption length greatly exceeds the visual content. No circulation or full spoke cycle is pictured. |

Figure 2 sits immediately after its reference in the cube example, a good choice. Figure 3 sits between the exchange discussion and disk identity, before the later detour argument. Figure 1's caption and Figure 2's solid/dashed encoding are worth keeping.

## Missing pictures

LIT dependencies refer to sections of the original supplied paper, not independent verification of its theorem.

- Section 3, capacity-one incidences and the flow cut. No source shows the network or why capacity two at endpoints gives two disjoint states.
- Section 4, disk count. No source draws the interior faces, boundary length, counted boundary sides, and strictly interior vertices together.
- Section 5.1, actual cancellation. None shows a cyclic Q with a valid partner before and after reversal. A local edge triangle cannot substitute for it.
- Sections 5.2 and 5.3, whole-cycle detours and positive circulation. None shows a complete cycle, its spoke polygon, and which bounded regions contribute positively.
- Section 5.3, regrouping the same pair set in two ways. An array indexed by second states and a grouping by undirected D would clarify why the two arguments address one sum.
- Section 6.1, the rooted white-face tree and assignment to the farther endpoint. Li has a cotree overview, but none of the sources draws the specific edge-selection rule in the triangulation notation.
- Section 6.2, selected forest and complementary Jordan curve on the same embedding. The two induced trees are never shown as the two regions of that curve.
- Section 7, matching labels across a separating triangle. Neither the cap colours nor the vertex-versus-edge intersections get a figure.
- The constructive exposition's marked alternating walk has no diagram of its path components or restart mechanism.

The delivered sequence addresses the requested fourteen slots. A flow-network inset, a sum-regrouping array, and a marked-walk diagram remain useful additions beyond those slots.
