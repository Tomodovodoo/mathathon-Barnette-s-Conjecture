from campaign import *
import hashlib,platform,scipy,sympy
from datetime import datetime,timezone
L=OUT/'labyrinth';r=json.load(open(OUT/'data/roots.json'));s=json.load(open(OUT/'data/strengthenings.json'))
nodes=[]
def node(id,kind,tier,title,statement,evidence,**kw):
 nodes.append(dict(id=id,kind=kind,tier=tier,title=title,statement=statement,status='under-review' if tier else 'open',evidence=evidence,links=[],review={'state':'under-review' if tier=='T4' else 'unreviewed','by':[]},**kw))
node('th.image','theorem','T2','Recovery image','Fixed-root recovery is injective; its image consists exactly of cycles whose inverse state is a tree matching.',['HYPOTHESES.md'])
node('th.surface','theorem','T2','Surface obstruction','Original state parts differ by 2g on an orientable genus-g surface. Two induced trees are impossible on the torus.',['HYPOTHESES.md'])
node('th.rarity','theorem','T2','Exponential rarity','White-face prism sums have 3^q states and 2^q tree matchings.',['HYPOTHESES.md','data/rarity.json'])
node('e.census','evidence','T4','Small exhaustive census','55 graphs, 1206 rooted choices, 3618 prescriptions; all tested separator and recovery conditions pass.',['data/roots.json','code/campaign.py'])
node('e.strength','evidence','T4','Strengthenings tested','All 55 graphs pass P4, arbitrary include/avoid pairs, and opposite-color Hamiltonian paths.',['data/strengthenings.json'])
node('x.surjective','deadend',None,'Surjectivity fails','Hexagonal prism has four avoiding cycles but only two recovered ones.',['examples/prism_recovery.json'],lesson='State recovery gives a subset of avoiding cycles.');nodes[-1]['status']='refuted'
node('x.p5','deadend',None,'P5 fails','A four-edge cube path blocks the second incident cycle edge of vertex 5.',['examples/P5_cube.json'],lesson='P4 cannot be strengthened to arbitrary longer paths.');nodes[-1]['status']='refuted'
node('q.strength','question',None,'Beyond the finite tests','Settle arbitrary edge-pair and Hamilton-laceability literature status and larger cases.',['STRENGTHENINGS.md'],next='Read the original strengthening literature and extend generation.')
node('q.weights','question',None,'Mixed signs','Find a smallest example with nonzero cycle gaps whose leading terms cancel.',['HYPOTHESES.md'],next='Enumerate small integer circulation assignments.')
(L/'knowledge.json').write_text(json.dumps({'schema':1,'meta':{'title':'Limits of the Barnette proof','subtitle':'T2 proofs unreviewed; T4 computational evidence'},'nodes':nodes},indent=2))
front={'meta':{'size_name':'dual vertices','value_name':'failed strengthening type'},'sizes':[]}
for n in range(6,15):
 ss=[x for x in s if x['dual_vertices']==n]
 front['sizes'].append({'size':n,'lo':0,'hi':2,'step':1,'realized':[],'intervals':[],'note':f'{len(ss)} graphs tested, no failures; T4 evidence not a certified impossibility interval'})
(L/'frontier.json').write_text(json.dumps(front,indent=2))
(L/'sota.json').write_text(json.dumps({'groups':['Recovery'],'entries':[{'id':'image','group':'Recovery','cls':'fixed rooted sphere triangulation','result':'injective, not surjective','status':'T2 unreviewed','refs':['HYPOTHESES.md'],'lit':[],'updated':'2026-11-14','kind':'proved','previous':[]}]},indent=2))
# Preserve raw event history, normalize a copy for the dashboard.
events=[]
for line in (OUT/'events.jsonl').read_text().splitlines():
 e=json.loads(line);events.append({'ts':datetime.fromtimestamp(e['time'],timezone.utc).isoformat(),'type':'computed','summary':e['summary']+' (under review)','nodes':[],'evidence':[]})
(L/'events.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in events))
lines=['# Root count table','','COMPUTED T4, under review. Each triple is states / ordered pairs / tree matchings. Full root and edge data are in data/roots.json.','','| Graph | Root count triples |','|---|---|']
for name in dict.fromkeys(x['name'] for x in r):
 vals=sorted(set((x['states'],x['pairs'],x['trees']) for x in r if x['name']==name));lines.append('| '+name+' | '+', '.join('/'.join(map(str,z)) for z in vals)+' |')
(OUT/'ROOT_COUNTS.md').write_text('\n'.join(lines)+'\n')
exe=ROOT/'workings/barnette_lab/vendor/plantri.exe';save('data/environment.json',{'python':platform.python_version(),'networkx':nx.__version__,'sympy':sympy.__version__,'scipy':scipy.__version__,'plantri_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'reference_core_sha256':hashlib.sha256((ROOT/'workings/barnette_lab/barnette_lab/core.py').read_bytes()).hexdigest()})
