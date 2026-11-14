# Barnette's Conjecture

A collaborative workspace for studying Barnette's Conjecture, collecting the information needed to understand it, and developing a constructive, explanatory proof.

The repository holds detailed digestions of the conjecture and related results, a focused library of relevant literature, and current proof attempts and workings in their own folders. Digestions explain the ideas, assumptions, and dependencies of each argument so contributors can follow and build on the work.

## Goal

The goal is to create a constructive and explanatory proof of OpenAI's October 6 release.

Keep established results, proposed arguments, and unresolved gaps clearly distinguished as the proof develops.

## Start here

| If you want | Read |
| --- | --- |
| What the overnight campaign of 14 November 2026 found, with review status | [`digestions/SYNTHESIS.md`](digestions/SYNTHESIS.md) |
| The exposition itself | [`paper/main/barnette.pdf`](paper/main/barnette.pdf) |
| How the proof works, in plain words | [`digestions/route-map/HOW-IT-WORKS.md`](digestions/route-map/HOW-IT-WORKS.md), then [`digestions/steps/00-overview.md`](digestions/steps/00-overview.md) |
| Every proof route as a picture | [`digestions/atlas/atlas.pdf`](digestions/atlas/atlas.pdf) |
| What is still open | [`digestions/steps/09-what-is-still-open.md`](digestions/steps/09-what-is-still-open.md) |

Nothing produced in that campaign has been read by a human. "Refereed" in these documents means a second AI model checked the work with its own reasoning and its own code. `SYNTHESIS.md` says which documents a human should check first.

## Repository layout

| Folder | Contents |
| --- | --- |
| `papers/` | Source literature. The three papers on the 2026 proof, a curated library, `INDEX.md` (what each source is used for and how it was verified) and `barnette.bib`. |
| `paper/` | The manuscript. `main/` is the current exposition, with earlier versions under `main/history/`. `figures/` is the shared figure toolkit. `draft-A/` and `draft-B/` are the two independent drafts the exposition was merged from, kept as records. |
| `proofs/` | Proof routes with their status. `primal/` proves the theorem in the cubic graph itself. `involutions/` is the bijective proof. `blueprint/` maps the exposition statement by statement against the Lean proof. `lean/` holds Lean files for the exposition's own devices. |
| `digestions/` | Explanations. `SYNTHESIS.md`, `steps/` (one document per step of the proof, plus a glossary), `route-map/` (every route found or refuted), `atlas/` (illustrated routes). |
| `workings/` | Shared computations. `barnette_lab/` is the reference implementation of every object in the proof. |
| `labyrinth/` | The research map: knowledge graph, events, state of the art, dashboard. |
| `research/` | One folder per agent run, with its report, code and data. `INDEX.md` lists them. `BRIEF.md` is the protocol agents follow. |
| `skills/` | Skills for writing and auditing the paper. |

## Contributing

Work in the appropriate subfolder. Keep ongoing investigations in `workings/`, proof developments in `proofs/`, and manuscript updates in `paper/`. Explain what an argument establishes, which assumptions it uses, and what remains open. Cite the literature that supports it.

Merge changes as you see fit. No special permission is required to merge.

## Literature

Include all important literature in `papers/`. Keep the collection relevant to the conjecture and the approaches under investigation, and trim unnecessary or duplicate literature. Record enough bibliographic information to identify each source and connect it to the corresponding digestion or proof discussion.

## Writing and auditing

Consult `skills/` for useful skills when writing, reviewing, or auditing the paper. Record gaps and objections explicitly so other contributors can check and resolve them.
