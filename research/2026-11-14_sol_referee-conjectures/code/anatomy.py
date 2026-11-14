import networkx as nx
from independent import *

if __name__=='__main__':
    data=json.loads((ROOT/'research/2026-11-14_opus_conjectures/data/c2_counterexample_V18.json').read_text())
    I=Instance(*parse_text(data['line']));d=json.loads((OUT/'v18.json').read_text());out=[]
    for i in (d['lo'],d['hi']):
        u=d['entries'][i]['u'];g=nx.DiGraph();g.add_nodes_from(I.hr)
        for k,f in enumerate(I.A):
            for v in f:g.add_edge(v,I.N+k) if u[k]==v else g.add_edge(I.N+k,v)
        cycles=list(nx.simple_cycles(g));checks=[]
        for r,s in I.decompositions(u):
            bad=[]
            for j,c in enumerate(cycles):
                if all(c[(a+1)%len(c)]==r[v-I.N] for a,v in enumerate(c) if v>=I.N):bad.append(j)
            assert bool(bad)!=I.forest(s)
            checks.append({'r':r,'s':s,'harmful_cycles':bad})
        out.append({'element':i,'directed_cycles':cycles,'checks':checks})
    save('v18_directed_cycles.json',out)
    # Arithmetic of the barrier, independently generated from exact integers.
    moments=[]
    for m,a,b in [(3,[0,4,5],[1,2,6]),(4,[0,4,7,11],[1,2,9,10])]:
        vals=[[sum(x**k for x in a),sum(x**k for x in b)] for k in range(m+1)]
        assert all(x==y for x,y in vals[:m]) and vals[m][0]!=vals[m][1]
        moments.append({'m':m,'plus':a,'minus':b,'moments':vals})
    save('moments.json',moments)
    print('directed cycle lengths',[[len(c) for c in e['directed_cycles']] for e in out]);print(moments)
