import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]; lab=p/'labyrinth'
claims=[('mixed','Real mixed determinant','PROOF.md section 2'),('norm','Positive coefficient norm counts tree matchings','PROOF.md section 4'),('matrix_tree','Constrained Laplacian coefficient','PROOF.md section 5'),('linear','Degree-n linear incidence weights suffice','PROOF.md section 7')]
nodes=[dict(id=k,kind='theorem',tier='T2',status='established',title=t,statement=t,review={'state':'unreviewed'},where=[w],evidence=['data.json'],links=[]) for k,t,w in claims]
for k,t,why in [('raw','Raw determinant is not Z','Repeated face labels introduce extra configurations'),('doubling','Doubling nonvanishing does not force trees','Diagonal pairs survive on obstructed examples'),('ust','Unconstrained tree count is not tree-matching count','Two label constraints remain')]:
 nodes.append(dict(id=k,kind='deadend',status='refuted',title=t,statement=t,lesson=why,evidence=['data.json'],links=[]))
nodes.append(dict(id='gadget',kind='question',status='open',title='Can a local Pfaffian gadget remove coefficient extraction?',statement='Find a verified local signature that enforces distinct matching incidences and turn signs.',links=[]))
(lab/'knowledge.json').write_text(json.dumps(dict(schema=1,meta={'title':'Dimer and determinant routes','subtitle':'T2 proofs unreviewed; T4 sampled computations'},nodes=nodes),indent=2))
rows=json.loads((p/'data.json').read_text()); sizes=[]
for n in sorted({r['vertices'] for r in rows}):
 vals=sorted({r['cmin'] if r['cmin'] is not None else 0 for r in rows if r['vertices']==n})
 sizes.append(dict(size=n,lo=0,hi=(n-3)//3,step=1,realized=[[v,'Sampled witness in data.json; 0 means no pair'] for v in vals]))
(lab/'frontier.json').write_text(json.dumps(dict(meta={'size_name':'vertices of T','value_name':'minimum cycles, 0 = no pair'},sizes=sizes),indent=2))
(lab/'sota.json').write_text(json.dumps(dict(about='Agent-local findings only, not coordinator integration',groups=['algebra'],entries=[dict(id=k,group='algebra',cls=t,result=t,status='T2 unreviewed',kind='proved',refs=[w],lit=[],updated='2026-11-14') for k,t,w in claims]),indent=2))
(lab/'events.jsonl').write_text((p/'events.jsonl').read_text())
