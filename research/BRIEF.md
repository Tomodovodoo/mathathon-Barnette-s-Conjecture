# Agent protocol (read this first)

Repository: `E:\Personal\Math\mathathon\barnette-s-conjecture` (remote `origin`, branch `main`). Read the top-level `README.md`.

## What this project is

OpenAI released a proof of Barnette's conjecture (every cubic bipartite 3-connected planar graph is Hamiltonian). We hold three papers:

| File | What it is |
| --- | --- |
| `papers/OpenAI-Barnette.pdf` (text: `papers/text/OpenAI-Barnette.txt`) | The original. Dual Eulerian triangulation, Tutte states, pairs of states, disk identity, exponential sum `Z(x)` with cancellation plus positive spoke circulations, forest state, tree on white faces, two induced trees, gluing over separating triangles. |
| `papers/A-Note-On-Barnette.pdf` (text: `papers/text/A-Note-On-Barnette.txt`) | Zhentao Li's exposition. Works in the primal graph with the face/black-vertex incidence graph, "cycle-breaking 2-factor", two sign-reversing involutions instead of the exponential sum. |
| `papers/barnette_trees.pdf` (text: `papers/text/barnette_trees.txt`) | "A constructive proof". Incidence-tree criterion, exchange graph, signed integer polynomial, marked walk (Garsia-Milne), determinant bound `3^{N/4}`. |

The text files are `pdftotext -layout` dumps. Formulas are garbled in places, so open the PDF when a formula matters.

The goal of the mathathon is a much better exposition: we want to know HOW the proof works, find other proof routes (combinatorial, graph-theoretic, constructive, and wilder ones), and write a paper that starts from the necessary principles and lets each definition and lemma arrive when the reader expects it. Good figures matter.

## Rules

1. **Your folder.** Create `research/2026-11-14_<model>_<slug>/` (the brief names it). Write only there unless the brief says otherwise. Never edit another agent's folder or the three source PDFs.
2. **Report.** End with `REPORT.md` in your folder: what you set out to do, what you established, what failed and why, what is still open, and the three best next steps. Put a five-line summary at the top. Your final chat message is a short version of the same.
3. **Status vocabulary.** Tag every mathematical claim: `LIT` (published, cite it exactly), `PROVED-HERE` (full proof written in your folder), `COMPUTED` (give script path and range checked), `CONJECTURE` (state a test), `HUNCH`, `REFUTED` (keep it, with the lesson). Never cite anything below `COMPUTED` as a fact. Do not invent citations. If you could not open a source, say so.
4. **Mathematical honesty.** A gap is a result. Say exactly where an argument stops. A clean negative ("this route fails because of this 8-vertex example") is worth as much as a proof.
5. **Skills.** `skills/unslop/SKILL.md` applies to every piece of prose you write. `skills/reverse-lamport/SKILL.md` is the method for dependency audits. `skills/labyrinth-exploration/SKILL.md` describes tiers and the map. Read the ones your brief names.
6. **Compute.** At most one heavy process per agent, and keep any single run under about ten minutes. Python 3.14 is on PATH. MiKTeX (`pdflatex`, `latexmk`, `pdftotext`) is installed. Record the command that produced every data file.
7. **Git.** The working tree is shared with about eight other agents, so:
   - stage and commit only your own paths: `git add -- <your paths>` then `git commit -m "<message>" -- <your paths>`;
   - never run `git add -A`, `git add .`, `git commit -a`, `git stash`, `git reset`, `git checkout -- .`, `git clean`, `git rebase` or `git pull` in this tree;
   - if you hit `index.lock`, wait a few seconds and retry;
   - commit early and often (at least at every stable point and at the end), then try `git push origin main`. If the push is rejected, leave it. The coordinator syncs with the remote.
   - End commit messages with the line `Co-Authored-By:` naming your model.
8. **No subagents** unless your brief says so. Do the work yourself.
9. **Scope.** Explore broadly inside your topic. If you find something important outside it, write it under "Leads for others" in your report and keep going on your own topic.

## Shared notation (use it unless you have a reason, and say when you deviate)

- `G`: the Barnette graph. `T = G*`: its dual, a simple sphere triangulation with faces properly coloured black and white (an Eulerian triangulation).
- `t0`: the outer black face, its vertices are the roots `R`. `A`: the other black faces. `X`: the non-root vertices. `|A| = |X| = n = k - 1`.
- A **state** is a bijection `s: A -> X` with `s(t)` a corner of `t` (a perfect matching of the incidence graph `B` on `A` and `X`). A **pair** `(r, s)` is two states that differ at every face.
- `Q_s`: the edge opposite `s(t)` in each `t`. `D(r,s)`: the edges `r(t) -> s(t)`. `H`: the spoke graph (black centres joined to their corners).
- **Disk identity**: Lemma 4.1 of the OpenAI paper.
