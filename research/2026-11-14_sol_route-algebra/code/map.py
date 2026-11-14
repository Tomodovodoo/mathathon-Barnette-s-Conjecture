"""Build the local proof/evidence map. Does not edit the coordinator's map."""
import json
from pathlib import Path
from datetime import datetime,timezone
OUT=Path(__file__).resolve().parents[1]; LAB=OUT/'labyrinth'; LAB.mkdir(exist_ok=True)
d=json.loads((OUT/'counts.json').read_text())
nodes=[]
def node(id,kind,title,statement,tier=None,**kw):
    a=dict(id=id,kind=kind,title=title,statement=statement,status='established' if kind=='theorem' else 'open',links=[],evidence=[],where=[])
    if tier:a['tier']=tier
    if tier=='T2':a['review']={'state':'unreviewed','by':[]}
    a.update(kw);nodes.append(a)
node('th.grassmann','theorem','Quartic integral and Gaussian decoupling','F equals a quartic Berezin integral and an expectation of two determinants. Integrand sign remains uncontrolled.','T2',where=['../PROOF.md, section 5'])
node('th.gram','theorem','Positive squared-minor representation','The double-transversal coefficient of the root-contracted opposite-edge Laplacian equals the tree count.','T2',where=['../PROOF.md, section 3'])
node('th.sign','theorem','Unsigned and signed support barriers','Tree coefficients have both signs; positive incidence rescaling preserves them; face/vertex multiplicative substitution annihilates F.','T2',where=['../PROOF.md, section 1'])
node('th.stability','theorem','Cube destroys real stability','The unsigned cube tree polynomial abc+def vanishes in the upper half-plane.','T2',where=['../PROOF.md, section 3'])
node('th.parity','theorem','Hamiltonian edge avoidance is even','Deduction from Thomason Corollary 1.5 for cubic bipartite graphs.','T2',where=['../PROOF.md, section 2'])
node('e.counts','evidence','All facial roots through order sixteen','297 plantri triangulations and all 7,868 roots, plus 102 named-example and fixture roots. Counts use exact integers.','T4',status='computed, independent review pending',evidence=['../counts.json','../checks.json'])
node('x.modular','deadend','Small-prime positivity fails','Positive tree counts divisible by each of 2,3,4,5,7,11 occur.',status='refuted',lesson='Unweighted residues do not force positivity by avoiding zero.',evidence=['../TABLES.md'])
node('x.invariant','deadend','Unrooted invariant equality fails','One unobstructed triangulation has root-dependent tree counts 2 and 8.',status='refuted',lesson='A prospective invariant must retain the root or a prescribed coefficient.',evidence=['../counts.json, plantri_12_2'])
node('x.gauge','deadend','Signed incidence gauge fails','A six-tree-state sign certificate prevents an incidence sign gauge from making every coefficient positive.',status='refuted',lesson='The obstruction persists beyond positive rescalings and local tensor factorization.',evidence=['../gauges.json'])
node('q.support','question','A transparent coefficient-support theorem','Prove the two endpoint partitions admit a nonzero opposite-edge minor whenever a pair exists.',status='open',next='Seek a special planar three-matroid support theorem rather than generic PSD positivity.')
node('h.at','hunch','Marked Alon-Tarsi coefficient','A directed graph could encode the minimum-cycle marked imbalance.','T6',status='live',test='Construct its orientation polynomial on the cube and a two-cycle input; compare every coefficient.',vivid='The disk index controls orientation signs, but no directed graph encoding is known.')
(LAB/'knowledge.json').write_text(json.dumps(dict(schema=1,meta=dict(title='Barnette algebra routes',eyebrow='Local research map',subtitle='T2 unreviewed proofs and T4 exact-count evidence'),nodes=nodes),indent=2))
sizes=[]
for n in range(6,17):
    rows=[g for g in d['graphs'] if g['name'].startswith('plantri_') and g['vertices']==n]
    if not rows:continue
    values=sorted({r['trees'] for g in rows for r in g['roots']})
    sizes.append(dict(size=n,label=f'{n} vertices; observed counts only',lo=0,hi=16,step=1,
        realized=[[v,'e.counts, T4 witness evidence'] for v in values if v<=16],
        intervals=[dict(v0=v,v1=v,status='impossible',why='Tree-count parity, PROOF 2') for v in range(1,17,2)]))
(LAB/'frontier.json').write_text(json.dumps(dict(meta=dict(size_name='T vertices',value_name='tree count, window 0..16; T4 observations',value_scale='linear'),sizes=sizes),indent=2))
entries=[]
for a in nodes[:6]:
    entries.append(dict(id=a['id'],group='Algebra',cls=a['title'],result=a['statement'],status=a.get('tier','')+' '+a['status']+'; independent review pending',refs=a['where'],lit=[],updated='2026-11-14',previous=[],kind='computed' if a['tier']=='T4' else 'proved'))
(LAB/'sota.json').write_text(json.dumps(dict(about='Local subagent map only',groups=['Algebra'],entries=entries),indent=2))
events=LAB/'events.jsonl'
if not events.exists():
    ts=datetime.now(timezone.utc).isoformat()
    with events.open('w') as f:
        for typ,summary,ids in [('proposed','Predictions recorded before testing in PREDICTIONS.md',[]),('computed','Completed exact all-root corpus; T4, review pending',['e.counts']),('refuted','Each tested small modulus permits a positive zero-residue count',['x.modular']),('proved','Quartic and auxiliary Gaussian identities; T2, unreviewed',['th.grassmann']),('documented','Completed local map; independent review remains pending',[])]:
            f.write(json.dumps(dict(ts=ts,type=typ,summary=summary,nodes=ids,evidence=['../PREDICTIONS.md'] if typ=='proposed' else [],backfilled=True))+'\n')
(LAB/'README.md').write_text('# Local algebra map\n\nGenerated by code/map.py. Dashboard: dashboard/index.html. This map belongs only to this subagent folder. T2 proofs are unreviewed; T4 counts are evidence. The frontier displays the fixed count window 0..16, marks odd values impossible by proof, and records observed even values. Unobserved even values remain unknown. It does not claim a certified exhaustive classification.\n')
print(len(nodes),'nodes;',len(sizes),'frontier rows')
