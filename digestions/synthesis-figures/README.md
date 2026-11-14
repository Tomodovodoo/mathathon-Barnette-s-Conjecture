# Synthesis figures

Two single-page vector PDFs, each with a PNG rendered from the PDF by PyMuPDF. Both PNGs were looked at after the last build.

- `products.pdf`, `products.png`: the sources, the proofs written here with the model that checked each, and the guides and tools. Arrows run from a source to a text built on it. It is not a dependency graph of the mathematics. That is in [the blueprint](../../proofs/blueprint/README.md).
- `route-outcomes.pdf`, `route-outcomes.png`: the records of [routes.py](../route-map/routes.py) by kind and recorded status. Each record gets one kind by keyword rules, and the kinds overlap. "Proved" includes proofs nobody has reviewed. "Open" includes hunches.

To rebuild, run from the repository root:

    python research/2026-11-14_fable_synthesis-audit/count.py
    python research/2026-11-14_fable_synthesis-audit/figures.py

The first script writes the counts and the per-record assignments into [the audit folder](../../research/2026-11-14_fable_synthesis-audit/). The second draws both figures from those counts. The first version of these figures, by GPT-6 Astra, was built by the scripts in [the synthesis folder](../../research/2026-11-14_astra_synthesis/). Neither chart is a mathematical result.
