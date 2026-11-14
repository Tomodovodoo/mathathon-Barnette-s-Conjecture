"""Read all stored lab instances and its finite named/generated test suite.
Run from repository root: python research/2026-11-14_sol_figures-polish/check_hunch.py
"""
import sys,json,time
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[2]
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT/'paper/figures'),str(ROOT/'workings/barnette_lab')]
from barnette_lab.core import Instance,named_graphs,generated
from model import Model
start=time.monotonic()
instances=[]
for path in sorted((ROOT/'workings/barnette_lab').rglob('*.json')):
    d=json.loads(path.read_text())
    if 'T_edges' in d:
        instances.append((str(path.relative_to(ROOT)),Instance(nx.Graph(d['T_edges']),d.get('outer',0))))
instances += [('named/'+name,Instance.from_primal(g)) for name,g in named_graphs().items()]
instances += [('generated12/'+str(i),Instance(g)) for i,g in enumerate(generated(12))]
instances=[(name+'/root'+str(t),Instance(b.T,t)) for name,b in instances for t in range(len(b.faces))]
rows=[]
for name,b in instances:
    assert time.monotonic()-start<550,'run exceeds ten-minute bound'
    m=Model(b.faces,b.outer)
    assert m.A==b.A and m.X==b.X
    ss=list(b.states()); ps=b.pairs(ss)
    # Exact integer weights independently supplied by lab Lemma 5.3 construction.
    a=b.weights(); ncycles=0; counts=set()
    for r,s in ps:
        for c in m.directed_cycles(m.D(r,s)):
            k=m.disk(c)
            if not k['ccw']: c=c[::-1]
            diff=sum(a.get((m.black_face(x,y),y),0)-a.get((m.black_face(x,y),x),0) for x,y in zip(c,c[1:]+c[:1]))
            assert diff==k['W'],(name,r,s,c,diff,k)
            ncycles+=1; counts.add(diff)
    row=dict(instance=name,T_vertices=len(m.V),G_vertices=len(m.F),states=len(ss),pairs=len(ps),D_cycles=ncycles,W_values=sorted(counts),outer=b.outer)
    rows.append(row); print(row,flush=True)
result=dict(status='COMPUTED',scope='All JSON T_edges instances recursively stored in workings/barnette_lab; four named graphs; generated(12), every face as outer face for every instance. Duplicate instances retained for provenance. Every state, ordered pair and D cycle.',instances=len(rows),pairs=sum(r['pairs'] for r in rows),cycles=sum(r['D_cycles'] for r in rows),T_vertex_range=[min(r['T_vertices'] for r in rows),max(r['T_vertices'] for r in rows)],rows=rows)
(ROOT/'research/2026-11-14_sol_figures-polish/hunch-results.json').write_text(json.dumps(result,indent=1))
