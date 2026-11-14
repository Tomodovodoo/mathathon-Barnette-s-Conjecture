"""Direct flow, S_s equivalence, disk, polynomial, and difference checks."""
from check import *
import random

def main():
    rng=random.Random(14112026); counts=co.Counter(); witness=None
    for order in range(6,13):
        lines=(OUT/f'plantri-{order}.txt').read_text().splitlines()
        for line in lines:
            if not line.startswith(str(order)+' '): continue
            faces=rotation_faces(line)
            for root in range(len(faces)):
                m=M(faces,root); ss=m.states()
                pairs=[(r,s) for r in ss for s in ss if all(a!=b for a,b in zip(r,s))]
                flow=nx.DiGraph()
                for x in m.X: flow.add_edge('source',('x',x),capacity=2)
                for t in m.A:
                    flow.add_edge(('t',t),'sink',capacity=2)
                    for x in set(m.f[t])&m.X: flow.add_edge(('x',x),('t',t),capacity=1)
                value=nx.maximum_flow_value(flow,'source','sink')
                assert (value==2*m.n)==bool(pairs)
                if not pairs and witness is None:
                    witness=dict(order=order,root=root,faces=faces,states=ss,flow=value,required=2*m.n)
                for s in ss:
                    for a,b in it.combinations(m.R,2):
                        c,=m.R-{a,b}; S=m.q(s)|{edge(a,c),edge(b,c)}
                        assert nx.is_tree(graph(m.V,S))==m.good(s)
                        counts['S_equivalences']+=1
                # Numeric evaluations at generic independent corner weights.
                w={(t,v):rng.randint(-9,9) for t in m.A for v in m.f[t]}
                left=sum(m.eps(r,s)*math.prod(w[t,v] for t,v in zip(m.A,s)) for r,s in pairs)
                classes={frozenset(edge(a,b) for a,b in zip(r,s)):(r,s) for r,s in pairs}
                right=0
                for r,s in classes.values():
                    cs=cycles(list(zip(r,s))); term=(-1)**((m.n-len(cs))//2)
                    for cyc in cs:
                        d=m.disk(cyc); es={edge(a,b) for a,b in zip(cyc,cyc[1:]+cyc[:1])}
                        indices=[i for i,t in enumerate(m.A) if edge(r[i],s[i]) in es]
                        p=math.prod(w[m.A[i],s[i]] for i in indices)
                        q=math.prod(w[m.A[i],r[i]] for i in indices)
                        term*=p-q if d['ccw'] else q-p
                        inside=set(d['faces']); vs=set(cyc)|set(d['interior'])
                        E={e for e,ts in m.E.items() if set(ts)&inside}
                        H=graph(vs,E); assert nx.is_connected(H)
                        assert len(vs)-len(E)+len(inside)==1
                        assert 2*len(E)==3*len(inside)+len(cyc)
                        assert all(set(m.f[t])<=vs for t in inside)
                        assert all(set(m.f[t])&set(d['interior'])==set() for t in set(m.G)-inside)
                        counts['disks']+=1
                    right+=term
                assert left==right
                counts['flow_and_polynomial_rootings']+=1
    for c in range(7):
        for m in range(c+1):
            for trial in range(20):
                w0=rng.randint(-9,9); L=[rng.randint(-4,4) for _ in range(c)]
                actual=sum((-1)**sum(xs)*(w0+sum(x*l for x,l in zip(xs,L)))**m for xs in it.product((0,1),repeat=c))
                expected=0 if m<c else (-1)**c*math.factorial(c)*math.prod(L)
                assert actual==expected; counts['difference_instances']+=1
    (OUT/'supplement.json').write_text(json.dumps(dict(checks=counts,no_pair_witness=witness),indent=2))
    print(json.dumps(counts,indent=2))

if __name__=='__main__': main()
