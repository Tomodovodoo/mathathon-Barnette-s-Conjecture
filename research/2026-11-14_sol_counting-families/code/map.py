"""Build the private local research map. Does not alter coordinator artifacts."""
from pathlib import Path
import json
from datetime import datetime,timezone
P=Path(__file__).resolve().parents[1];L=P/'labyrinth';nodes=[]
items=[
('prism','theorem','T2','Even-prism formulas','S=m, P=M=2, cmin=1, H=2m+2; full proof in FAMILIES.md.'),
('transfer','theorem','T2','Exact boundary transfer identities','Face matchings, pair-cycle distributions and two induced trees have finite stationary transfers.'),
('tube','evidence','T4','Exact integer tube certificates','Widths 4 and 6 have saved matrices, finite recurrence certificates and cmin=1 Boolean stabilization.'),
('chain','theorem','T2','Prism-chain factorization','S=3^q, P=M=2^q, cmin=q, signed product with gaps 5j+2.'),
('hcchain','evidence','T4','Three-port chain HC tensor','Local eight-cycle tensor gives H_q=20*3^(q-2), q>=2.'),
('rarity','evidence','T4','Rarity without triangular separators','Width-4 transfer has M=2 and S=Fib_(2L+3).'),
('subdivision','deadend',None,'Subdivision does not preserve growing cmin','Subdivided q=1,2,3 cube chains all have cmin=1.'),
('largec','question',None,'Unbounded cmin without separators','No family found here; investigate separators of length four.'),
('signed6','question',None,'Width-6 signed-polynomial recurrence','Only exact polynomials through L=4 are supplied.'),
('exponential','conjecture','T5','M >= 2^cmin','Exact for every exponent in the nested prism chain; general conjecture remains open.')]
for id,kind,tier,title,statement in items:
    n={'id':id,'kind':kind,'tier':tier,'title':title,'statement':statement,'status':'established' if kind=='theorem' else 'refuted' if kind=='deadend' else 'open' if kind in ('question','conjecture') else 'under-review','links':[],'evidence':['FAMILIES.md'],'where':['FAMILIES.md']}
    if tier in ('T2','T4'):n['review']={'state':'under-review','by':[]}
    if kind=='conjecture':n['test']='Find a rooted triangulation with a pair and M<2^cmin.'
    if kind=='deadend':n['lesson']='New states can join old D-cycles after subdivision.'
    nodes.append(n)
(L/'knowledge.json').write_text(json.dumps({'schema':1,'meta':{'title':'Counting Barnette families','eyebrow':'Private research','subtitle':'Exact transfers; independent review pending'},'nodes':nodes},indent=2))
(L/'frontier.json').write_text(json.dumps({'meta':{'size_name':'tube length L','value_name':'resolved selected quantities','value_scale':'linear'},'sizes':[{'size':i,'lo':0,'hi':3,'realized':[[0,'states'],[1,'pairs'],[2,'tree matchings'],[3,'HC']]} for i in range(2,21)]},indent=2))
# A selected-task tracker, not an exhaustive invariant feasibility frontier.
(L/'sota.json').write_text(json.dumps({'groups':['families'],'entries':[{'id':'tube','group':'families','cls':'T4','result':'Widths 4 and 6: integer transfer certificates','status':'under review','refs':'FAMILIES.md','lit':'','updated':'2026-11-14','previous':[]}]},indent=2))
events=L/'events.jsonl'
if not events.exists():
    rows=[]
    for typ,summ in [('proposed','Predictions saved before computation in PREDICTIONS.md.'),('computed','Prism, tube, stack and first-inflation counts completed; T4 under review.'),('computed','Stationary matching, HC and pair matrices and recurrence certificates completed.'),('refuted','Subdivision failed to preserve growing stacked cmin at q=2,3.'),('documented','Family proofs, bounds, unresolved tasks and reproduction commands written.')]:
        rows.append({'ts':datetime.now(timezone.utc).isoformat(),'type':typ,'summary':summ,'nodes':[],'evidence':['PREDICTIONS.md','FAMILIES.md'],'backfilled':True})
    events.write_text(''.join(json.dumps(r)+'\n' for r in rows))
print('Local map written; historical events explicitly backfilled.')
