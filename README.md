# Barnette's Conjecture

Every cubic, bipartite, 3-connected planar graph has a Hamiltonian cycle. OpenAI proved this on 24 September 2026 and released the proof on 6 October. This repository holds an exposition of that proof and the material around it.

## Goal

A constructive and explanatory account of the proof: why it works, and how one gets from the statement to the cycle.

## Start here

Read [`paper/barnette.pdf`](paper/barnette.pdf). It is short and self-contained. For a map of the proof and of the routes around it, with a figure for each step, see [`digestions/routes.md`](digestions/routes.md).

## Layout

| Folder | Contents |
| --- | --- |
| `paper/` | The exposition: `barnette.tex`, `barnette.pdf`, and `figures/` with the script that draws them. |
| `papers/` | The accounts of the proof and the background literature, with `INDEX.md` and `barnette.bib`. |
| `proofs/` | Companion notes: the bijective proof by two involutions, the part of the argument that needs no sign, and what is known about algorithms. |
| `digestions/` | `routes.md`: a map of the routes to the theorem, how the different presentations of the count translate into each other, the routes that fail and the open ones. `figures/` holds its figures and the scripts that draw them. |
| `workings/` | `barnette/`, a small Python package that follows the paper and finds the cycle. |
| `research/` | Open problems and the counterexample graphs someone would need to continue. Work in progress goes here and leaves when it is done. |
| `skills/` | Skills for writing and auditing. |

The state of the repository before it was cut down to this is kept under the git tag `archive-2026-11-14`.

## Contributing

Work in the folder that fits. Use the paper's notation and terms. Say what an argument establishes and what it assumes, and cite the literature it rests on. Keep `research/` for questions that are still open.

Merge changes as you see fit. No special permission is required.

## Literature

Keep `papers/` to what the proof and its history need. Give each source a line in `papers/INDEX.md` and an entry in `papers/barnette.bib`.
