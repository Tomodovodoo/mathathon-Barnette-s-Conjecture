# Project literature

Start with [INDEX.md](INDEX.md). [barnette.bib](barnette.bib) is the canonical bibliography, including sources held only by citation.

The [14 November citation audit](../research/2026-11-14_astra_citation-audit/CITATION-AUDIT.md) records the four current manuscripts and the requested digestions. The canonical file has 96 entries. `paper/main/refs.bib` is an exact 17-entry subset for that manuscript, rather than a separate bibliography to maintain. The [rights ledger](../research/2026-11-14_astra_citation-audit/PDF-RIGHTS.md) covers all 50 PDFs retained in the two literature research folders. No research PDF was deleted or moved.

Inline bibliography aliases are retained for compatibility. In the involution note, `OAI` means `OpenAI2026`, `Li` means `Li2026`, and `trees` means `Anonymous2026`. In the sign-free note, `SchrijverCourse` names the same work as `Schrijver2017`, and `SchrijverHandbook` names the same work as `SchrijverUndated`. `Expo` is the project's exposition, not an external publication. The primal note cites sources in prose. [UNUSED-KEYS.md](../research/2026-11-14_astra_citation-audit/UNUSED-KEYS.md) flags keys with no explicit TeX citation without assuming they are absent from prose.

- `history/` holds licensed copies of partial results.
- `equivalents/` holds reformulations. GSW uses arXiv v3 to preserve the cited theorem numbers.
- `machinery/` holds licensed sources for tools used or investigated.
- `2026/` points to the three supplied accounts, which remain at the top level. `text/` remains in place.

Free reading access does not establish permission to redistribute a PDF. Most inspected arXiv records grant distribution rights to arXiv only. Those sources have links rather than new repository copies. Existing research downloads are unchanged.

## Adding a source

1. Identify its use in a digestion, proof note, draft or named research route.
2. Verify bibliographic fields against the source or publisher. Record uncertainty. Use `FirstAuthorYear` keys, `b` and `c` for collisions, and `Undated` where a year is unverified.
3. Check the exact version and reuse terms. Prefer the version cited by theorem number. Link paywalled papers by DOI.
4. Compare SHA-256 and bibliographic identity against the manifest. Keep one copy per work, named `Year-FirstAuthor-ShortTitle.pdf`. Preserve the three originals.
5. Add an index row, BibTeX entry and manifest record. Distinguish opening a source from checking a statement. Name secondary sources. Keep the library below roughly 80 MB.

The [manifest](../research/2026-11-14_astra_literature-consolidation/manifest.csv) records source URLs, SHA-256, byte sizes and licence evidence. New copies are unmodified. Attribution appears in INDEX.md. CC-BY copies retain [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); Bagheri Gh. 2022 uses [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Rights to supplied originals were not re-audited.

See the [report](../research/2026-11-14_astra_literature-consolidation/REPORT.md), [citation checks](../research/2026-11-14_astra_literature-consolidation/MISMATCHES.md) and [key map](../research/2026-11-14_astra_literature-consolidation/KEY-MAP.md). Drafts were not edited.
