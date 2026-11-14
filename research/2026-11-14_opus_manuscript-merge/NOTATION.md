# Notation of `paper/main/barnette.tex`

One meaning per symbol. Scope "local" means the symbol lives inside one proof or one section and is not reused elsewhere with another meaning. Numbers refer to the built PDF.

| Symbol | Type | What it is | Scope | First use |
| --- | --- | --- | --- | --- |
| `G` | graph | the cubic bipartite planar 3-connected graph; also "the graph of faces of `T`" | global | Thm 1.1 |
| `e` | edge of `G` | the edge to avoid | global | Thm 1.1 |
| `T` | plane graph | dual triangulation; from Section 2 on, any coloured triangulation | global | Sec. 1 |
| `k` | integer | number of black faces = number of white faces | global | (2.3) |
| `M`, `N` | plane graph, edge set | arguments of the duality Lemma 2.5 | local (Lemma 2.5) | Lemma 2.5 |
| `M* − N*` | graph | dual edges crossing edges not in `N` | Sec. 2, 3 | before Lemma 2.5 |
| `R` | graph | graph in Lemma 2.2 | local | Lemma 2.2 |
| `P`, `P*` | edge sets | a selection; the edges of `G` crossing it | global | Def. 2.4 |
| `t0`, `e0 = ab`, `c` | face, edge, vertex | outer black face, prescribed side, third corner | global | Sec. 3 |
| `a, b, c` | vertices | roots (corners of `t0`) | global (not reused as numbers) | Sec. 3 |
| `A`, `X`, `n` | sets, integer | black faces other than `t0`; non-roots; `n = |A| = |X| = k − 1` | global | Sec. 3 |
| `P0` | edge set | `P \ {e0}` for the selection at hand | Lemma 3.1, Prop 3.9 (same definition) | Lemma 3.1 |
| `s`, `r` | states | `s` second state (the one wanted good), `r` first state / partner | global, roles fixed | Def. 3.2, Def. 4.1 |
| `α`, `β`, `β~` | states of the example | `α` has a cycle in `Q_α`; `β` is good; `β~` the other partner of `α` | example only | Ex. 3.3 |
| `Q_s` | edge set | sides opposite `s(t)`, `t ∈ A` | global | Sec. 3 |
| `S_s` | edge set | `Q_s ∪ {ac, bc}` | global | Sec. 3 |
| `Y_s` | tree on faces | `T* − S_s*`, the tree of faces | global | Sec. 3 |
| `y0` | white face | the face across `e0` from `t0` | global | Lemma 3.6 |
| `P_s` | edge set | selection read off `Y_s` | global | Lemma 3.6 |
| `Z` | cycle of `T` | a directed cycle of chosen sides (disk identity); also the cycle in Lemma 2.5 and in the gluing proof | used only for "a cycle in a set of edges" | Lemma 2.5 |
| `R_Z` | plane graph | `Z` and everything of `T` inside it | Sec. 3 | before Lemma 3.8 |
| `B`, `W`, `I`, `h`, `ℓ` | integers | black and white faces inside `Z`, vertices strictly inside, length, edges of `Z` with black face inside | disk identity and Prop 3.9 only | before Lemma 3.8 |
| `F` | directed edge set / function | in Lemma 3.7 a directed edge set; from Sec. 4 on a function on states; in Sec. 5 a face of `H` | three local scopes, never overlapping | Lemma 3.7 |
| `q`, `γ` | integers | vertices and sinks of a component (Lemma 3.7); `q` = edges of `H` in Sec. 5 | local | Lemma 3.7 |
| `u(t)` | vertex | third corner of `t` in a pair | global | Def. 4.1 |
| `D(r,s)` | directed edge set | edges `r(t) → s(t)` | global | Sec. 4 |
| `C`, `C_i`, `c`, `c⁺` | cycles, integers | cycles of `D`; their number; number running counterclockwise | Sec. 4 | Lemma 4.3 |
| `K`, `K_s` | cycle | a cycle of `Q_s`; the one chosen from `s` | Sec. 4 | Lemma 4.3 |
| `δ(v,w)` | ±1 | +1 iff the black face of `vw` is left of `v → w` | global | Sec. 4 |
| `ε(r,s)` | ±1 | `∏ δ(r(t), s(t))` | global | Sec. 4 |
| `J` | integer | OpenAI's `Σδ/3`, only in Remark 4.10 | Remark 4.10 | Rem. 4.10 |
| `y` | white face | argument of a height | global | Sec. 4 |
| `f_0..f_j` | faces | the fixed path of faces from `y` to `t0` | Sec. 4 | heights |
| `κ_y(t,v)` | 0, ±1 | turn sign of the path of `y` at corner `v` of `t` | global | heights |
| `η_s(y)`, `ω(s)` | integers | height of `s` at `y`; weight `Σ_y η_s(y)` | global | heights |
| `L(C)` | integer | white faces inside `C` | global | Lemma 4.6 |
| `m` | integer | least number of cycles of `D` over all pairs | Sec. 4, Remarks | before Lemma 4.7 |
| `ω_0`, `L_i`, `x_i` | reals, bits | Lemma 4.7 data; `x_i = 1` iff `C_i` counterclockwise | Lemma 4.7, Prop 4.8 | Lemma 4.7 |
| `Σ` | integer | `Σ ε ω(s)^m` | Prop 4.8, Ex. 4.9 | Prop 4.8 |
| `𝓑` | bipartite graph | incidence graph on `A ∪ X` | Sec. 5 | Sec. 5 |
| `S`, `U` | vertex sets | `S ⊆ X`, `U = V(T) \ S` | Sec. 5 | (5.1) |
| `V(t)` | vertex set | corners of `t` | Sec. 5 | (5.1) |
| `e(U)`, `b(U)` | integers | edges with both ends in `U`; black faces (incl. `t0`) with all corners in `U` | Sec. 5 | Prop 5.2 |
| `H`, `p`, `q`, `b_H`, `f` | component and counts | component of `T[U]`, its vertices, edges, black faces, faces | Sec. 5 | Prop 5.2 |
| `f_•`, `f_∘`, `d_F`, `bal(F)` | integers | black/white length-3 faces; boundary length; black minus white faces in `F` | Sec. 5 | Prop 5.2 |
| `Δ = xyz`, `𝖣`, `T_𝖣`, `T_1`, `T_2`, `P_1`, `P_2`, `e'` | triangle, disk, pieces | separating triangle and gluing data | Sec. 6 | Sec. 6 |
| `s_C` | state | state read off a Hamiltonian cycle `C` | Remarks | Sec. 7 |
| `w_{t,v}`, `F(w)`, `w^{C±}`, `ξ` | variables, polynomial | the polynomial behind the count | Remarks | Sec. 7 |

Overloads listed by the two reviews and how each was resolved: `w` (vertex / white face / count) now `y` for white faces, `f_∘` for counts, no vertex called `w`; `h` (length / height) height is `η`; `b` (root / constant / count) constant `ω_0`, count `f_•` or `b(U)`, `b_H`; `c` (root / number of cycles) the root `c` and the count `c` of cycles never meet in one statement (Section 3 vs Section 4); `K` (cycle of `Q_s` / component) component is `H`; `S` (edge set / vertex set) edge set in the duality lemma is `N`; `D` (cycle set / disk) disk is `𝖣`; `B` (incidence graph / count) incidence graph is `𝓑`; `β` (region balance / state) balance is `bal`; `r`, `s` role swap in figures: example states named `α`, `β`.
