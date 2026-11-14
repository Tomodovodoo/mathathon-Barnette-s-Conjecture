from pathlib import Path
import json
p=Path('digestions/route-map/routes.py')
s=p.read_text(encoding='utf8')
d=json.loads(Path('research/2026-11-14_opus_route-induction/data/failed_inductions.json').read_text())
s+='\n# Retain all thirteen failed induction schemes, including unreplayed cases.\n'
for r in d['refuted']:
    cex='; '.join(k+'='+str(v) for k,v in r.items() if k not in ('id','statement','lesson'))
    review='R8 lowest-coefficient claim was not independently replayed; R13 checked only at V=6. Other specified witnesses confirmed in ri/REFEREE.md.'
    s+=f"add({'U.ind-'+r['id']!r},'U',{('induction '+r['id']+': '+r['statement'][:60])!r},'REFUTED','ind','ind/data/failed_inductions.json; ri/REFEREE.md',{(r['statement']+' '+review)!r},'induction',cex={cex!r},lesson={r['lesson']!r})\n"
s+='''
add('U.loads-dead','U','rainbow loads are M-convex','REFUTED','reft','reft/RAINBOW.md; reft/data/loads_sampled_6_13.json','Rainbow load vectors satisfy simultaneous M-exchange.','matroid',cex='V=12, first instances with two factors; author search, unreviewed.',lesson='Singleton-factor tests made the exchange property vacuous; include instances with several factors.')
add('D.chain-dead','D','every maximal lattice chain hits success','REFUTED','rc','rc/REFEREE.md; rc/data/r3.json; rc/data/R2_glued_V33.json','Every maximal chain contains an element carrying a tree pair.','lattice',cex='Saved V=60 chain of seven elements; V=33 gluing already refutes it. No minimum claim.',lesson='A chain can complete one coordinate block before entering the next and miss every success.')
add('D.fraction-dead','D','at least half the lattice succeeds','REFUTED','rc','rc/REFEREE.md; rc/data/r5.json; rc/data/R2_glued_V33.json','At least half the factor lattice admits a successful direction choice.','lattice',cex='Saved V=70 gives 654/1410=109/235; V=33 gluing gives 4/16. No minimum claim.',lesson='Independent witness blocks multiply the successful fraction down to 2^-q.')
'''
p.write_text(s,encoding='utf8')
# Persist concrete integration checks, with no imported research code.
d=json.loads(Path('research/2026-11-14_sol_referee-conjectures/data/R2_glued_V33.json').read_text())
e=d['entries']; n=len(e)
assert n==16 and sum(x['tree_pairs'] for x in e)==144
# Reconstruct covers purely from stored potential order; check rank and all R2 candidates.
le=lambda a,b: all(x<=y for x,y in zip(a['phi'],b['phi']))
lower=[];upper=[]
for i,a in enumerate(e):
    lo=[j for j,b in enumerate(e) if j!=i and le(b,a)]
    hi=[j for j,b in enumerate(e) if j!=i and le(a,b)]
    lower.append([j for j in lo if not any(j!=k and le(e[j],e[k]) for k in lo)])
    upper.append([j for j in hi if not any(j!=k and le(e[k],e[j]) for k in hi)])
c=[i for i in range(n) if len(lower[i])<=1 or len(upper[i])<=1]
assert len(c)==10 and all(e[i]['tree_pairs']==0 for i in c)
rows=json.loads(Path('research/2026-11-14_sol_referee-conjectures/data/fast_census_summary.json').read_text())
assert sum(r['roots'] for r in rows)==9531638 and sum(r['feasible'] for r in rows)==4656948
assert sum(r['violations'] for r in rows)==0
rows24=json.loads(Path('research/2026-11-14_astra_cycle-covers/data/census.json').read_text())
import re
roots24=sum(int(re.search(r'rooted=(\d+)',next(x for x in r['summary'] if x.startswith('SUMMARY')))[1]) for r in rows24)
assert roots24==23824742
Path('research/2026-11-14_sol_map-update/spotcheck.json').write_text(json.dumps({'command':'python -X utf8 -B research/2026-11-14_sol_map-update/add_failures.py','V33_elements':n,'R2_candidates':len(c),'candidate_tree_pairs':0,'V33_total_tree_pairs':144,'roots_through_22':9531638,'feasible_through_22':4656948,'separator_free_roots_through_24':roots24,'scope':'Checks saved certificate order and arithmetic; does not independently enumerate graphs or replay all pair tests.'},indent=2))
