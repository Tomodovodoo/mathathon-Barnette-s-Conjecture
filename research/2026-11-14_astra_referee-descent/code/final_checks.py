from check import *
import ast, hashlib

code=BASE/'code'
for p in code.glob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'),filename=str(p))
data={p.name:json.loads(p.read_text(encoding='utf-8-sig')) for p in code.glob('*.json')}
assert all(r['certificate_holds'] for r in data['potentials.json'])
assert all(r['certificate_holds'] for r in data['all_potentials.json']['checked'])
assert len(data['macro40.json'])==8 and all(r['radius_two_verified'] for r in data['macro40.json'].values())
census=data['c3_6_19.json']+data['c3_20_20.json']
assert [r['V'] for r in census]==list(range(6,21))
random_roots=[r for g in data['random_separator_free.json'] for r in g['roots']]
out=dict(c3_census={k:sum(r[k] for r in census) for k in ('graphs','roots','paired_roots','pairs','good','strict_sinks','radius_over_two')},independent_separator_free_sample=dict(graphs=len(data['random_separator_free.json']),roots=len(random_roots),**{k:sum(r[k] for r in random_roots) for k in ('pairs','good','strict_sinks','radius_over_two')}),signed_macro_certificates=len(data['macro40.json']),checked_saved_potential_certificates=len(data['all_potentials.json']['checked']))
changes=[]
for r in data['source-manifest.json']:
 p=REPO/r['path'];now=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
 if now!=r['sha256']:changes.append(dict(path=r['path'],before=r['sha256'],after=now))
(code/'source-changes.json').write_text(json.dumps(changes,indent=2))
out['source_changes_since_checkpoint']=len(changes)
(code/'verification_summary.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
