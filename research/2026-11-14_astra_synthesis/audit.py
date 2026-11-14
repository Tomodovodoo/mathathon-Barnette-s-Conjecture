"""Validate synthesis links and create the paragraph-to-source ledger.
Run: python research/2026-11-14_astra_synthesis/audit.py
"""
from pathlib import Path
import re,json
root=Path(__file__).resolve().parents[2];out=Path(__file__).parent
p=root/'digestions/SYNTHESIS.md';s=p.read_text(encoding='utf-8-sig')
links=re.findall(r'\]\(([^)]+)\)',s)
bad=[x for x in links if not x.startswith('http') and not (p.parent/x.split('#')[0]).exists()]
assert not bad,bad
words=len(re.sub(r'\]\([^)]*\)',']',s).split())
assert 3500<=words<=5000,words
assert not re.search(r'\b(?:LIT|PROVED-HERE|COMPUTED|CONJECTURE|HUNCH|REFUTED)\b',s)
assert not any(c in s for c in '\u2014\u2013\u201c\u201d\u2019')
assert '<!-- INVENTORY -->' not in s and '<!-- LATE_SCAN -->' not in s
rows=['# Claims and sources','','This synthesis asserts no new mathematical theorem. Tags below describe the underlying claim type, not a promotion of its review status. The prose cites the report that establishes the claim and the referee where available. Every cited source was read; no mathematical census was rerun here.','','| Claim group | Protocol status | Review and source |','|---|---|---|',
'| Supplied signed-count route | LIT | Supplied preprints, not externally peer-reviewed; [main AI referee](../2026-11-14_sol_referee-main/REPORT.md). |',
'| Disk balance, height argument, count bounds | PROVED-HERE | Existing proofs accepted by [combinatorics referee](../2026-11-14_astra_referee-combinatorics/REPORT.md). No new proof here. |',
'| Exact pair criterion, gluing, recovery image | PROVED-HERE | [Structure referee](../2026-11-14_sol_referee-structure/INTEGRATION.md). |',
'| Mixed determinants and linear weights | PROVED-HERE | [Determinant referee](../2026-11-14_fable_referee-determinants/REPORT.md). |',
'| Turning and Morse readings | PROVED-HERE | [Topology referee](../2026-11-14_fable_referee-topology/REPORT.md); its new rainbow lemmas have no further review. |',
'| Packing and induction additions | PROVED-HERE | Author-written proofs, unreviewed; [packing](../2026-11-14_opus_two-tree-packing/REPORT.md), [induction](../2026-11-14_astra_induction-lemmas/REPORT.md). |',
'| Canonical choices, matroid relaxations, gauges, lifting, lattice extremes | REFUTED | Exact scope and smallest-known versus proved-minimum distinctions retained in synthesis section 5 and linked reviews. |',
'| Exponential bound, monotone descent, induction G and X | CONJECTURE | Tests and ranges in synthesis section 7; no general proof claimed. |',
'| Why signed counting seems necessary | HUNCH | Explicit interpretation in synthesis section 6, not an impossibility theorem. |',
'| Reported census sizes and product inventory | COMPUTED | [count.py](count.py), [evidence.py](evidence.py); source outputs extracted, not mathematical computations replayed. |',
'| Phase adjudication | PROVED-HERE; COMPUTED | [Cross-audit](../2026-11-14_opus_cross-audit/ADJUDICATION.md), independent proof and own code. |',
'| New involution path model | PROVED-HERE | [Author revision](../2026-11-14_sol_involutions-revision/REPORT.md); independent new-lemma review pending at writing. |',
'| Cover identity and two-cover bound | PROVED-HERE | [Cover referee](../2026-11-14_sol_referee-covers/REFEREE-covers.md). Large census independently replayed only through order 16. |',
'| Family counts | PROVED-HERE; COMPUTED | [Families referee](../2026-11-14_sol_referee-covers/REFEREE-families.md); exact transfer replay distinct from larger census and decimal asymptotics. |',
'| Formal finite difference | COMPUTED | [Blueprint report](../2026-11-14_opus_blueprint/REPORT.md), own compilation; surrounding translations remain informal. |',
'','## Paragraph and table-row traceability','','The excerpt identifies a paragraph or table row in SYNTHESIS.md. Its links support the complete block. Recommendations are editorial judgments. Lists in the exposition-method section inherit that section\'s two explicit sources.','','| Block | Opening words | Sources |','|---|---|---|']
i=0
for block in s.split('\n\n'):
    for part in (block.splitlines() if block.startswith('|') else [block]):
        refs=re.findall(r'\]\(([^)]+)\)',part)
        if not refs:continue
        i+=1
        excerpt=re.sub(r'\[([^]]+)\]\([^)]*\)',r'\1',part)
        excerpt=' '.join(excerpt.replace('|','/').split()[:17])
        targets=[]
        for x in refs:
            if x.startswith('http'):continue
            q=(p.parent/x.split('#')[0]).resolve().relative_to(root).as_posix()
            targets.append(f'[Source](../../{q})')
        rows.append(f'| C{i:03} | {excerpt} | '+', '.join(targets)+' |')
rows+=['','## Retained negative routes','','REFUTED entries below are copied from the route map snapshot. Their labels do not refute broader unnamed routes. The full scope, counterexample and source locator are retained in routes.py.','','| Route | Rejected proposal | Source locator |','|---|---|---|']
import runpy
for r in runpy.run_path(str(root/'digestions/route-map/routes.py'))['ROUTES']:
    if r['status']=='REFUTED':rows.append('| '+r['id']+' | '+r['label'].replace('|','/')+' | '+str(r.get('where','')).replace('|','/').replace('\n',' ')+' |')
rows+=['','Source: [routes.py](../../digestions/route-map/routes.py). Folder abbreviations resolve through its FOLDERS table.']
(out/'CLAIMS.md').write_text('\n'.join(rows)+'\n',encoding='utf8')
result=dict(words_excluding_link_targets=words,links_checked=len(links),missing_links=bad,source_blocks=i,pdf_files=[p.name for p in (root/'digestions/synthesis-figures').glob('*.pdf')])
(out/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result,indent=2))
