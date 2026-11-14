from inventory import *
import ast
rows=json.loads(read(O/'pdf-inventory.json'));web=json.loads(read(O/'web-checks.json'))
manifest=json.loads(read(R/'research/2026-11-14_astra_literature-consolidation/manifest.json'))
if isinstance(manifest,dict): print(manifest.keys());raise SystemExit('inspect manifest format')
urls={}
for line in read(R/'research/2026-11-14_opus_history-literature/pdf/INDEX.md').splitlines():
 if line.startswith('| `'):
  cells=line.split('|');urls[cells[1].strip().strip('`')]=cells[-2].strip()
tree=ast.parse(read(R/'research/2026-11-14_sol_machinery-literature/fetch_sources.py'))
for n in tree.body:
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='sources' for t in n.targets):urls.update({k+'.pdf':v for k,v in ast.literal_eval(n.value).items()})
def norm(u):return re.sub(r'v\d+$','',u.replace('/pdf/','/abs/'))
byurl={norm(x['url']):x for x in web};bysha={x['sha256']:x for x in manifest}
out=['# PDF rights inventory','','COMPUTED file inventory from `inventory.py`; source URLs transcribed from the two download manifests. Licence fields from current arXiv pages are in `web-checks.json`; matching curated-copy permissions are inherited from the named consolidation manifest. This is a provenance and owner-decision list, not a legal opinion. No file was deleted, moved, or newly redistributed. A nonexclusive arXiv distribution grant is not a general downstream redistribution licence.','','| File | Bytes | Source URL | Licence evidence | Recommendation |','|---|---:|---|---|---|']
data=[]
for r in rows:
 if not r['file'].startswith('research/'):continue
 u=urls.get(Path(r['file']).name,'Source URL not recovered from download manifest')
 w=byurl.get(norm(u),{});licenses=w.get('license',[]);match=bysha.get(r['sha256'])
 if match:
  lic=match.get('license','See curated manifest');rec='Keep licensed canonical copy in papers/ under '+lic+'; duplicate research copy is an owner decision.'
 elif licenses:
  lic='; '.join(licenses)
  if any('creativecommons.org' in l for l in licenses):rec='May keep in papers/ under the listed licence after checking version identity and attribution; no copy made here.'
  else:rec='Replace shared copy by a source link; existing private research copy requires owner decision.'
 else:
  lic='No downstream reuse licence established. '+('Author/publisher source; free access alone is not permission.' if 'arxiv.org' not in u else 'Exact arXiv licence field not recovered in this pass.')
  rec='Owner decision for retained research copy; use a link in the curated library.'
 out.append('| `'+r['file']+'` | '+str(r['bytes'])+' | '+u+' | '+lic+' | '+rec+' |')
 data.append(dict(**r,url=u,license_evidence=lic,recommendation=rec))
out+=['',f"COMPUTED: {len(data)} files, {sum(x['bytes'] for x in data):,} bytes. Exact SHA-256 values are in pdf-inventory.json. Reproduce with `python research/2026-11-14_astra_citation-audit/rights.py`."]
(O/'PDF-RIGHTS.md').write_text('\n'.join(out)+'\n',encoding='utf-8')
(O/'rights.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
