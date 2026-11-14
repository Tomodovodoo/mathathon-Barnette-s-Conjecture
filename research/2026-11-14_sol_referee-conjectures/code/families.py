import networkx as nx
from independent import *
from examples import bipyramid
from gluing import glue_into_face

def tube(p,L):
    N=p*(L+1);g=nx.Graph()
    for j in range(L+1):
        for i in range(p):g.add_edge(j*p+i,j*p+(i+1)%p)
    for j in range(L):
        for i in range(p):
            g.add_edge(j*p+i,(j+1)*p+i)
            a,b=(i,(i+1)%p) if i%2==0 else ((i+1)%p,i)
            g.add_edge(j*p+a,(j+1)*p+b)
    for i in range(p):g.add_edge(N,i);g.add_edge(N+1,L*p+i)
    ok,e=nx.check_planarity(g);assert ok
    rot={v:list(e.neighbors_cw_order(v)) for v in sorted(g)}
    return rot,(N,0,1) if L==0 else (0,1,p+1)

if __name__=='__main__':
    rows=[]
    for p,last in [(4,6),(6,4),(8,3)]:
        for L in range(last+1):
            I=Instance(*tube(p,L));d=lattice_analysis(I);d.update(family='tube',width=p,length=L)
            rows.append(d);print('tube',p,L,{k:d[k] for k in ('V','lattice','pairs','TM','R2')},flush=True)
    I=Instance(bipyramid(6),(6,0,1));base=I
    for q in range(1,6):
        if q>1:
            f=next(I.faces[j] for j in I.white if not(set(I.faces[j])&I.R));I=glue_into_face(I,base,f)
        d=lattice_analysis(I);d.update(family='prism_sum',copies=q);rows.append(d)
        print('prism_sum',q,{k:d[k] for k in ('V','lattice','pairs','TM','R2')},flush=True)
    d=json.loads((ROOT/'research/2026-11-14_opus_conjectures/data/c2_counterexample_V18.json').read_text())
    base=Instance(*parse_text(d['line']));I=base
    f=next(base.faces[j] for j in sorted(base.white) if not(set(base.faces[j])&base.R))
    for q in range(1,4):
        if q>1:
            I=glue_into_face(I,base,f)
            f=tuple(I.gluing_ident[v] for v in (1,2,9))
        d=lattice_analysis(I);d.update(family='witness_sum',copies=q);rows.append(d)
        print('witness_sum',q,{k:d[k] for k in ('V','lattice','pairs','TM','R2')},flush=True)
    save('families.json',rows)
