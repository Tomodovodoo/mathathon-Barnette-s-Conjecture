"""Exact worked examples and finite state chains. Predictions in ../PREDICTIONS.md."""
import sys,json,time,random,itertools,math
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'workings/barnette_lab'))
sys.path.insert(0,str(ROOT/'research/2026-11-14_sol_counting-families/code'))
from barnette_lab.core import Instance,dual_graph,faces_of,plantri_graphs
from families import tube,stack,subdivide
import networkx as nx
import sympy as sp
import numpy as np
START=time.monotonic()
def deadline():
    if time.monotonic()-START>530: raise TimeoutError('530 seconds')
def from_faces(fs,outer):
    g=nx.Graph()
    for f in fs:g.add_edges_from(zip(f,f[1:]+f[:1]))
    b=Instance(g);return Instance(g,next(i for i,f in enumerate(b.faces) if set(f)==set(fs[outer])))
def white_edges(b):
    es=[]
    for t in b.A:
        for v in b.faces[t]:
            if v not in b.X:continue
            ends=[b.sides[v,u] if b.sides[v,u] in b.white else b.sides[u,v] for u in b.faces[t] if u!=v]
            es.append((t,v,*ends))
    return es
def halfpair(b,ps):
    es=white_edges(b);best=None
    covers={tuple(sorted((t,min(r[i],s[i]),max(r[i],s[i])) for i,t in enumerate(b.A))):(r,s) for r,s in ps}
    for r,s in covers.values():
        used={(t,v) for t,v in zip(b.A,r)}|{(t,v) for t,v in zip(b.A,s)}
        for mask in range(1,1<<len(b.white)):
            if mask.bit_count()<2:continue
            vs={v for i,v in enumerate(b.white) if mask>>i&1}
            weight=sum((t,v) in used for t,v,a,c in es if a in vs and c in vs)
            excess=weight-2*(len(vs)-1)
            if excess>0:return {'feasible':False,'subset':sorted(vs),'twice_mass':weight,'r':r,'s':s}
    return {'feasible':True,'covers':len(covers)}
def profile(name,b,chain=True):
    deadline();ss=list(b.states());ps=b.pairs(ss);trees=[s for s in ss if b.is_tree(s)]
    weights=b.weights(); signs=Counter(); terms=[]
    for r,s in ps:
        e=b.sign(r,s);h=sum(weights[t,v] for t,v in zip(b.A,s));signs[str(e)]+=1;terms.append((e,h))
    poly=b.polynomial(ps);z=sp.Symbol('z');expr=sum(v*z**k for k,v in poly.items())
    normalized=sp.expand(expr/z**min(poly)) if poly else sp.Integer(0)
    q=sp.Poly(normalized,z)
    roots=[]
    if poly and q.degree()>0:
        # Exact factor list plus numpy approximations, not certified root locations.
        roots=[[float(v.real),float(v.imag)] for v in np.roots([float(v) for v in q.all_coeffs()])]
    defects=[len(b.qcycles(s)) for s in ss]
    chainout={}
    if chain:
        dg=nx.DiGraph();dg.add_nodes_from(range(len(ss)))
        for i,s in enumerate(ss):
            for j in range(i):
                if sum(a!=c for a,c in zip(s,ss[j]))==3:
                    if defects[j]<=defects[i]:dg.add_edge(i,j)
                    if defects[i]<=defects[j]:dg.add_edge(j,i)
        good={ss.index(s) for s in trees}; reachable=set(good)
        for i in good:reachable.update(nx.ancestors(dg,i))
        chainout={'states_reaching_TM_nonincreasing':len(reachable),'traps':[list(ss[i]) for i in range(len(ss)) if i not in reachable][:3], 'zero_cycle_nonTM':sum(d==0 and s not in trees for s,d in zip(ss,defects))}
    lap=nx.laplacian_matrix(b.H).toarray();tau=int(sp.Matrix(lap[:-1,:-1]).det())
    cmin=min((len(b.dcycles(r,s)) for r,s in ps),default=None)
    ans={'name':name,'V':len(b.T),'states':len(ss),'pairs':len(ps),'TM':len(trees),'cmin':cmin,'sign_counts':dict(signs),'sign_height_hist':{str(e):dict(sorted(Counter(h for a,h in terms if a==e).items())) for e in (-1,1)},'polynomial':poly,'factor':str(sp.factor(normalized)),'roots_approx':roots,'UST_trees':tau,'UST_success':str(sp.Rational(len(trees),tau)),'state_success':str(sp.Rational(len(trees),len(ss))),'q_cycle_hist':dict(Counter(defects)),'chain':chainout,'half_pair':halfpair(b,ps) if len(b.T)<=16 else 'not tested'}
    print(name,len(ss),len(trees),cmin,ans['half_pair'],chainout,flush=True);return ans

def main():
    cases=[('cube',Instance.from_primal(nx.cubical_graph())),('hexagonal_prism',Instance.from_primal(nx.circular_ladder_graph(6)))]
    d=json.loads((ROOT/'research/2026-11-14_fable_figures-review/search_example.json').read_text())[0];cases.append(('running13_reconstructed_candidate',from_faces(d['faces'],d['t0'])))
    d=json.loads((ROOT/'research/2026-11-14_sol_referee-structure/code/fable16.json').read_text());cases.append(('bad_cover16',from_faces(d['faces'],d['outer'])))
    cases += [(f'prism_{2*m}',Instance.from_primal(nx.circular_ladder_graph(2*m))) for m in range(4,9)]
    cases += [(f'tube4_L{L}',Instance(tube(4,L))) for L in range(1,5)]
    cases += [(f'prism_chain{q}',stack(6,q)) for q in range(2,4)]
    rows=[profile(name,b) for name,b in cases]
    (OUT/'data/exact.json').write_text(json.dumps({'command':'python research/2026-11-14_sol_route-probabilistic/code/explore.py','seconds':time.monotonic()-START,'rows':rows},indent=2))
if __name__=='__main__':main()
