from pathlib import Path
import runpy,contextlib,json,re,collections
root=Path.cwd(); out=root/'research/2026-11-14_sol_digest-fixes'
ns=runpy.run_path(str(root/'research/2026-11-14_opus_digestions-audit-2/code/recompute.py'),run_name='review_import')
with (out/'worked-examples.txt').open('w',encoding='utf8') as log,contextlib.redirect_stdout(log):
 for key in ('running','cube','prism','double_octahedron','sixteen'): ns[key]()
 print('ALL ASSERTIONS PASSED; auditor implementation rerun read-only, outputs redirected here')
def plain(v):
 if isinstance(v,dict): return {str(k):plain(x) for k,x in v.items()}
 if isinstance(v,(tuple,list,set,frozenset)): return [plain(x) for x in v]
 return v
(out/'worked-examples.json').write_text(json.dumps(plain(ns['OUT']),indent=2)+'\n',encoding='utf8')
# Re-sum exact census records. The V=23 extension is stored in eight disjoint shards.
s=json.loads((root/'research/2026-11-14_fable_descent/data/census_summary.json').read_text())
print('census keys',s.keys())
base=s['totals'] if 'totals' in s else s['orders'] if 'orders' in s else s['census']
parts=[]
for p in sorted((root/'research/2026-11-14_fable_descent/data').glob('census_23_part*of8.txt')):
 line=next(l for l in p.read_text().splitlines() if l.startswith('T V=23 '))
 parts.append(dict(file=str(p.relative_to(root)),**{k:int(v) for k,v in re.findall(r'(\w+)=(\d+)',line)}))
npairs=sum(r['pairs'] for r in base.values())+sum(r['pairs'] for r in parts)
assert npairs==193623384,npairs
nums=dict(census_pairs_through_22=sum(r['pairs'] for r in base.values()),V23_parts=parts,census_pairs_through_23=npairs,method='Sum saved census records, not repeat the large computation.')
(out/'numbers.json').write_text(json.dumps(nums,indent=2)+'\n')
print(npairs)
