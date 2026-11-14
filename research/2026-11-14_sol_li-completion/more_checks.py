"""Cross-check lowest coefficients against the existing integer-weight model."""
from verify import *
sys.path.insert(0,str(ROOT/'workings/barnette_lab'))
from barnette_lab.core import Instance
levels=enumerate_classes(14);rows=json.loads((OUT/'census.json').read_text())['rows']
comparisons=[];interior=None;nonseparating=None
for row in rows:
    if not row['pairs']:continue
    T=from_code(levels[row['v']][row['cls']]);g=nx.Graph(list(T.de))
    base=Instance(g);root=next(i for i,f in enumerate(base.faces) if set(f)==set(T.faces[row['root']]))
    bb=Instance(g,root);a=bb.weights();m=row['m']
    coeff=[]
    for j in range(m+1):
        coeff.append(sum(bb.sign(*p)*math.comb(sum(a[t,v] for t,v in zip(bb.A,p[1])),j) for p in bb.pairs()))
    assert coeff[:m]==[0]*m
    assert abs(coeff[m])==abs(row['lowest_coefficient'])
    comparisons.append([row['v'],row['cls'],row['root'],coeff[m]])
    if nonseparating is None and m==3:
        triangles={frozenset((u,v,w)) for u,v in T.de for w in set(T.nbrs(u))&set(T.nbrs(v))}
        if len(triangles)==T.F:
            b=Check(T.faces,row['root']);o=next(o for o in b.objects(m) if b.two(o)!=o)
            nonseparating=dict(command='python research/2026-11-14_sol_li-completion/more_checks.py',instance=row,faces=T.faces,object=o,image=b.two(o))
    if interior is None and m>1:
        b=Check(T.faces,row['root'])
        for o in b.objects(m):
            cs,_,_,h=b.data(o[0]);M=o[1]
            if len(cs)!=m or any(sum(i in c for w,i in M)!=1 for c in cs):continue
            entries=[(c,w,i,h[c,w]) for c in cs for w,i in M if i in c]
            if all(len(hh)%2 for c,w,i,hh in entries) and any(hh[0][1:]!=(i,1) for c,w,i,hh in entries):
                interior=dict(instance=row,faces=T.faces,object=o,image=b.two(o));break
(OUT/'polynomial-comparison.json').write_text(json.dumps(dict(command='python research/2026-11-14_sol_li-completion/more_checks.py',comparisons=comparisons,interior_nonfirst=interior),indent=2))
(OUT/'nonseparating-witness.json').write_text(json.dumps(nonseparating,indent=2))
print('weight coefficients compared',len(comparisons),'interior witness',None if interior is None else interior['instance'])
