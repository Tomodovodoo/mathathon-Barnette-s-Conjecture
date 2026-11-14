"""Extract reported census sizes, preserving population and review scope.
Run from root: python research/2026-11-14_astra_synthesis/evidence.py.
This reads reports; it does not independently replay those experiments.
"""
from pathlib import Path
import re,json
root=Path(__file__).resolve().parents[2];out=Path(__file__).parent
specs=[
('Exponential bound, all roots','sol_referee-conjectures/REPORT.md',r'4,656,948','feasible roots, dual order <=22; independent referee'),
('Exponential bound, separator-free','astra_cycle-covers/REPORT.md',r'23,824,742','facial roots, dual order <=24; author run; independent replay only <=16'),
('Height identity','astra_referee-combinatorics/REPORT.md',r'636,682','height monomials, all roots through dual order 16; independent'),
('Main manuscript','sol_referee-main/REPORT.md',r'707,952','chosen-side systems through dual order 12; independent'),
('Primal proof','fable_referee-primal/REPORT.md',r'1,214','roots through 14 faces, including repeated cube; independent'),
('Primal normalization','opus_cross-audit/ADJUDICATION.md',r'24,856','ordered pairs through dual order 16 plus repeated running example; independent'),
('Induction G','astra_induction-lemmas/REPORT.md',r'62,416','separator-free roots through dual order 19; structural test'),
('Contraction inequality','fable_induction-completion/MISSING-LEMMA.md',r'1,202,792','rooted contractions through dual order 18; independent'),
('Packing','opus_two-tree-packing/REPORT.md',r'14,881','supports through dual order 17; new author computation'),
('Involution revision','sol_involutions-revision/REPORT.md',r'1206','roots through dual order 14, multiple mark modes; author rerun'),
]
rows=[]
for claim,suffix,pat,scope in specs:
    path=root/('research/2026-11-14_'+suffix);text=path.read_text(encoding='utf-8-sig')
    m=re.search(pat,text);assert m,(claim,pat)
    rows.append(dict(claim=claim,count=int(m[0].replace(',','')),scope=scope,source=path.relative_to(root).as_posix(),matched=m[0]))
p=root/'research/2026-11-14_fable_referee-topology/REPORT.md';s=p.read_text(encoding='utf-8-sig')
nums=[int(x.replace(',','')) for x in re.findall(r'74,432|1,327,360|4,030,720|29,366,528|34,659,072',s)]
assert len(nums)==5,nums
rows.append(dict(claim='Rainbow descent',count=sum(nums),scope='enumerated trees through dual order 17; remaining unique-cover cases handled by proposition',source=p.relative_to(root).as_posix(),summands=nums))
(out/'evidence-counts.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
md=['# Reported computation populations','','COMPUTED: extracted by evidence.py from the linked records. This synthesis did not replay the mathematical censuses. Counts measure different populations and must not be added.','','| Claim | Count | Population and scope | Source |','|---|---:|---|---|']
for r in rows:md.append(f"| {r['claim']} | {r['count']:,} | {r['scope']} | [Record](../../{r['source']}) |")
(out/'EVIDENCE.md').write_text('\n'.join(md)+'\n',encoding='utf8');print('\n'.join(md))
