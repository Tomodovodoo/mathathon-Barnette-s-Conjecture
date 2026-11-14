from pathlib import Path
import json,re,datetime,subprocess,hashlib
root=Path(__file__).resolve().parents[2];out=Path(__file__).parent
p=root/'digestions/SYNTHESIS.md';s=p.read_text(encoding='utf8')
c=json.loads((out/'counts.json').read_text())
line=f"At {c['timestamp']}, the inventory has {c['run_folders']} run folders and {c['reports']} delivered REPORT files, including this synthesis. Four model labels occur: "+', '.join(f"{k}, {v} runs" for k,v in c['models'].items())+'. '
line+=f"The route map has {c['routes']} records: 46 source arguments, 57 project proofs, 12 computed routes, 19 conjectures, 25 suggestions and 67 refutations. These are recorded statuses, not a fresh adjudication. [Inventory](../research/2026-11-14_astra_synthesis/counts.json)"
page='\n\n| Current product PDF | Pages |\n|---|---:|\n'
for path,n in c['pdf_pages'].items():page+=f'| [{path}](../{path}) | {n} |\n'
page+=f"\nThese six PDFs total {sum(c['pdf_pages'].values())} pages, including two one-page blueprint diagrams. Drafts, archived versions and individual figure PDFs are excluded. The step files contain {c['step_words_total']:,} regex-counted word tokens, including headings and Markdown targets, so that count is not reading-time prose. [Counting method](../research/2026-11-14_astra_synthesis/count.py)"
inv=line+page+'\n\nThe [computation ledger](../research/2026-11-14_astra_synthesis/EVIDENCE.md) gives each largest cited census by claim, with its own population and review scope. Its rainbow total is 69,458,112 enumerated trees; unique-cover instances settled by a proposition are separate. [Extraction script](../research/2026-11-14_astra_synthesis/evidence.py)'
if '<!-- INVENTORY -->' in s:s=s.replace('<!-- INVENTORY -->','<!-- inventory-start -->\n'+inv+'\n<!-- inventory-end -->')
else:s=re.sub(r'<!-- inventory-start -->.*?<!-- inventory-end -->','<!-- inventory-start -->\n'+inv+'\n<!-- inventory-end -->',s,flags=re.S)
targets=['astra_induction-lemmas','fable_descent','sol_referee-covers','fable_referee-topology','opus_cross-audit','opus_blueprint','astra_main-revision','sol_involutions-revision','fable_referee-involutions-v2','opus_lean-devices']
scan={}
for t in targets:
    f=root/('research/2026-11-14_'+t)
    scan[t]={'report_exists':(f/'REPORT.md').exists(),'markdown':[x.name for x in f.glob('*.md')]}
for rel in ['paper/main/barnette.tex','paper/main/barnette.pdf']:
    b=(root/rel).read_bytes();scan[rel]={'sha256':hashlib.sha256(b).hexdigest()}
scan['time']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(out/'late-scan.json').write_text(json.dumps(scan,indent=2),encoding='utf8')
late='''The closing scan incorporated the induction-lemmas report, topology referee, finished cover and families referee report, cross-audit adjudication, blueprint and involution revision. The main paper has a revised working PDF and an archived version 1, but no main-revision REPORT at this scan; version 2 is not certified here as finished. Descent, the new involution referee and Lean-devices runs also have no REPORT. Their existence is not a mathematical result. This document freezes that boundary instead of promoting unfinished work. [Scan record](../research/2026-11-14_astra_synthesis/late-scan.json)
'''
if '<!-- LATE_SCAN -->' in s:s=s.replace('<!-- LATE_SCAN -->','<!-- late-start -->\n'+late+'<!-- late-end -->')
else:s=re.sub(r'<!-- late-start -->.*?<!-- late-end -->','<!-- late-start -->\n'+late+'<!-- late-end -->',s,flags=re.S)
p.write_text(s,encoding='utf8')
print(json.dumps(scan,indent=2))
