"""Format scan evidence without exposing personal values. Run from this folder."""
from pathlib import Path
import json,collections
out=Path(__file__).resolve().parent; d=json.loads((out/'logs/scan.json').read_text(encoding='utf8'))
lines=['# Reader-facing process residue','','Exact source lines at the pinned commit. Matches are an inventory, not a recommendation to remove source attribution or mathematical terminology. No source was edited.','']
for x in d['internal_residue']:
 lines += [f"## {x['file']}:{x['line']}",'','```text',x['text'],'```','']
lines += ['## Proposed replacement for the primal opening','','Replace primal.tex line 16, through its opening status sentence, with:','','> We reconstruct the proof in the cubic graph. The theorem is OpenAI, Theorem 1.1 and Corollary 7.1.','','Keep the subsequent explanation of the Lean commit and the two departures. Move the review status to STATUS.md. This is a proposal only. The date at line 12 also says "refereed revision".']
(out/'RESIDUE.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
lines=['# Hygiene inventory','','Snapshot: eceaf633aaff996f18f00075ce1b7d4af5cf6b5b. Full machine-readable locations and SHA256 duplicate groups are in logs/scan.json. Personal values are omitted.','','## Large files','','Threshold: 5,000,000 bytes.','', '| File | Bytes |','| --- | ---: |']
lines += [f"| {x['file']} | {x['bytes']} |" for x in d['large']]
lines += ['','## Exact duplicate groups','','SHA256 over tracked file bytes, before any rebuild. Empty files also form a group.','']
for i,group in enumerate(d['duplicates'],1):
 lines += [f'Group {i}: '+', '.join('`'+f+'`' for f in group),'']
lines += ['## Tracked build-pattern files','','Only the three involutions.aux/.log/.out files are disposable TeX artefacts identified here. The other 64 files are computation, formal-build or audit records and were retained. The two committed .bbl files are not counted by this extension scan and may be intentional distribution inputs.','']
lines += ['- `'+f+'`' for f in d['build_pattern_files']]
lines += ['','## Absolute local paths','','Locations only. Includes historical command records and data provenance, not just executable assumptions.','']
for f,rows in __import__('itertools').groupby(d['absolute_paths'],key=lambda x:x['file']):
 lines.append('- `'+f+'`: '+', '.join(str(x['line']) for x in rows))
lines += ['','## Personal-data candidates','','Email addresses, local-account username and user-directory paths in UTF-8 tracked text. Literature author emails are included. Locations only; no values are reproduced. This does not certify the absence of names or identifiers in binary PDF/image metadata.','']
for f,rows in __import__('itertools').groupby(d['personal_locations'],key=lambda x:x['file']):
 lines.append('- `'+f+'`: '+', '.join(str(x['line']) for x in rows))
lines += ['','## Reports and index','','Every tracked research folder has REPORT.md. Seven folders are missing from the index after respecting its documented date-prefix abbreviation.','']
lines += ['- `'+f+'`' for f in d['research_missing_index']]
lines += ['','## Earlier cleanup proposal','','- A1/A2 closed: record-22.txt and record-24.txt are now gzip files. A3/A4 remain, including counts.json and census_V16-17.json. A5 remains low-priority record compression; A6 canonical-changes.patch is no longer tracked.','- B1 remains: three large raster proof PDFs. B2/B3/B5 duplicate groups remain wherever listed above; no history was deleted. B4 historical primal renders remain. B6 current map outputs retained.','- C3/C4/C5 literature copies and duplicates remain in research folders. No tracked upstream/vendor clone was found.','- C1 remains: involutions.aux/.log/.out are still tracked, even though its local .gitignore now covers them. C2 both .bbl files remain.','- E1 empty record-7/9 files remain. E2 empty stderr record remains if listed among duplicate empty files. E3 drafts retained as records, now with rebuild READMEs. E4 primal README already labels its first-version examples; historical STATUS/EXAMPLES wording is unchanged. E5 historical revise.py remains explicitly excluded from builds.','- C9 closed: opus_blueprint/.gitignore now ignores upstream/. C10 closed: top README lists research and labyrinth. C11 partly open: seven missing folders listed above. C12 retained policy: local TeX ignores, no global suppression of computation logs.','','No research data, literature, render history or mathematical files were removed.']
(out/'HYGIENE.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
