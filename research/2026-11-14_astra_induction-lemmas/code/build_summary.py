"""Build the local research handoff map from completed census files."""
from pathlib import Path
import json,collections,html,hashlib,datetime
B=Path(__file__).resolve().parents[1]
def read(name):return json.loads((B/'data'/name).read_text())
def totals(rows):
    c=collections.Counter()
    for row in rows.values():
        for k,v in row.items():
            if isinstance(v,(int,float)) and k not in ('seconds','max_exception_fraction'):c[k]+=v
    return dict(c)
g=read('g_structure_8_19.json');x=read('x_hypotheses_6_18.json');d=read('deficiency_6_14.json');c=read('contraction_formula_6_14.json');cube=read('cube_repairs.json')
summary=dict(G=totals(g['per_V']),X=totals(x['per_V']),deficiency=totals(d['per_V']),
             contraction_formula=totals(c),cube=totals(cube['per_V']),
             max_exception_fraction=max(r.get('max_exception_fraction',0) for r in cube['per_V'].values()))
(B/'data/summary.json').write_text(json.dumps(summary,indent=2))
items=[
('k.G','conjecture','T5','open','Good contraction G','Some degree-4 nonroot has a simple contraction retaining a pair.','G.md'),
('k.X','conjecture','T5','open','Two-sided lifting X','A two-sided vertex has a nonexceptional tree matching in some contraction.','X.md'),
('th.hall','theorem','T2','established','Exact Hall formulas','Connected-complement deficiency G1 and contraction formulas G2,G3.','G.md'),
('th.short','theorem','T2','established','Four- and five-cycle obstruction','Bad merges are exactly the stated four- or black-heavy five-cycle obstructions.','G.md'),
('th.curvature','theorem','T2','established','Coloured disk curvature','2 n4 >= 6 minus the number of boundary colour changes.','G.md'),
('th.restricted','theorem','T2','established','G without chordless five-cycles','No separating triangle and no chordless five-cycle imply G.','G.md'),
('x.descent','deadend',None,'refuted','Innermost descent fails','Bad disks defeat inward descent at V=11; five-cycle and blocked-source refinements fail at V=13 and V=14.','G.md'),
('x.cube','deadend',None,'refuted','Fixed-cover repair fails','A fixed cover can contain a single tree matching, exceptional; V=18.','X.md'),
('k.avoid','conjecture','T5','open','Corner avoidance','Every bounded black face has at least two values across the tree matchings.','X.md'),
('ev.census','evidence','T4','computed','New census','Hall formulas through V=14; short-cycle structure through V=19; X probes through V=18.','code/README.md')]
nodes=[]
for id,kind,tier,status,title,stmt,where in items:
    n=dict(id=id,kind=kind,tier=tier,status=status,title=title,statement=stmt,where=[where],links=[])
    if tier=='T2':n['review']=dict(state='unreviewed',by=[])
    if tier=='T5':n['test']='Extend the stated census or supply an arbitrary-size proof.'
    if kind=='deadend':n['lesson']='Retain the witness and replace the refuted step, not the theorem.'
    nodes.append(n)
(B/'knowledge.json').write_text(json.dumps(dict(schema=1,meta=dict(title='Induction lemmas: two open steps'),nodes=nodes),indent=2))
# This frontier records tested predicates rather than invented resolved fractions for arbitrary graphs.
frontier=dict(meta=dict(size_name='V',value_name='tested statement',note='Finite tests do not resolve unrestricted G or X.'),
              ranges=dict(deficiency=[6,14],contraction_formula=[6,14],G_structure=[8,19],X_hypotheses=[6,18]),
              refutations=[dict(statement='innermost descent',first_V=11),dict(statement='five-cycle descent',first_V=13),dict(statement='blocked-source five-cycle descent',first_V=14),dict(statement='mate repair',first_V=16),dict(statement='single D reversal',first_V=17),dict(statement='fixed-cover repair',first_V=18)],
              unrestricted_open=['G','X','corner avoidance','half-exception bound'])
(B/'frontier.json').write_text(json.dumps(frontier,indent=2))
(B/'sota.json').write_text(json.dumps(dict(about='Local handoff snapshot; canonical coordinator table unchanged.',groups=['G','X'],entries=[
    dict(id='G',group='G',cls='separator-free rooted triangulations',result='Exact obstruction classification; restricted theorem; general selection remains open.',status='partial T2 unreviewed',refs=['G.md'],lit=[],updated='2026-11-14'),
    dict(id='X',group='X',cls='two-sided contractions',result='Fixed-cover repairs refuted at V=18; global half bound tested through V=18.',status='partial, computed T4',refs=['X.md'],lit=[],updated='2026-11-14')]),indent=2))
events=B/'events.jsonl'
if not events.exists():
    with events.open('w') as f:
        for typ,msg,ids in [('proposed','Initial predictions recorded before computation in JOURNAL.md.',['k.G','k.X']),
            ('computed','Symbolic Hall residual zero and census complete.',['th.hall']),
            ('refuted','V=11 refutes innermost descent.',['x.descent']),
            ('refuted','V=18 refutes fixed-cover repair; independent lab replay.',['x.cube']),
            ('proved','Restricted G and disk-colour curvature written, self-reviewed only.',['th.restricted','th.curvature']),
            ('documented','G and X remain open; bounded audit and partial certificate theorem completed.',['k.G','k.X'])]:
            f.write(json.dumps(dict(ts='2026-11-14',type=typ,summary=msg,nodes=ids,evidence=['JOURNAL.md'],backfilled=True))+'\n')
rows=''.join('<tr><td>'+html.escape(n['title'])+'</td><td>'+html.escape(str(n['tier'] or '')+' '+n['status'])+'</td><td>'+html.escape(n['statement'])+'</td><td><a href="'+n['where'][0]+'">Source</a></td></tr>' for n in nodes)
page='<!doctype html><meta charset="utf-8"><title>Induction lemma handoff</title><style>body{font:16px Georgia;max-width:1100px;margin:40px auto;padding:0 20px}td,th{padding:10px;border-bottom:1px solid #ccc;text-align:left}table{border-collapse:collapse}pre{white-space:pre-wrap}</style><h1>Induction lemma handoff</h1><p>G and X are open. The Hall identities pass; innermost descent and fixed-cover repair fail. New proofs are unreviewed.</p><p><a href="REPORT.md">Report</a> | <a href="AUDIT.md">Audit</a> | <a href="code/README.md">Commands</a></p><table><tr><th>Statement</th><th>Status</th><th>Result</th><th>Evidence</th></tr>'+rows+'</table><h2>Census totals</h2><pre>'+html.escape(json.dumps(summary,indent=2))+'</pre>'
(B/'dashboard.html').write_text(page)
manifest={str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((B/'data').glob('*.json')) if p.name!='sha256.json'}
(B/'data/sha256.json').write_text(json.dumps(manifest,indent=2))
assert len({n['id'] for n in nodes})==len(nodes)
assert all((B/n['where'][0]).exists() for n in nodes)
print(json.dumps(summary,indent=2))
