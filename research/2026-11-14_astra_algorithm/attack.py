"""Find a prefix accepted by both source tests with no good completion.

python -B research/2026-11-14_astra_algorithm/attack.py
Also stress minimum-remaining-corners on biased degree-four split instances.
"""
from experiments import *


def prefix_attack(filtered=False):
    examined=0
    for v in range(6,17):
        for j,g in enumerate(plantri_graphs(v,ROOT/'workings/barnette_lab/vendor/plantri.exe')):
            for root in range(len(Instance(g).faces)):
                b=Instance(g,root);ss=list(b.states());good=[s for s in ss if b.is_tree(s)]
                if not good:continue
                examined+=1
                for s in ss:
                    h=b.H.copy()
                    for k,(t,x) in enumerate(zip(b.A,s),1):
                        h.remove_edge(('t',t),('v',x))
                        if not nx.is_connected(h):break
                        if not any(z[:k]==s[:k] for z in good):
                            if filtered:
                                residual=nx.Graph()
                                rows=[('t',a) for a in b.A[k:]]
                                residual.add_nodes_from(rows)
                                for a in b.A[k:]:
                                    for y in set(b.faces[a]) & (set(b.X)-set(s[:k])):
                                        hh=h.copy();hh.remove_edge(('t',a),('v',y))
                                        if nx.is_connected(hh):residual.add_edge(('t',a),('v',y))
                                if len(nx.bipartite.maximum_matching(residual,top_nodes=rows))!=2*len(rows):continue
                            return dict(status='REFUTED',examined=examined,V=v,census_index=j,root=root,edges=list(g.edges()),faces=b.faces,A=b.A,prefix=list(s[:k]),extension=s,good_states=good,claim='The two necessary prefix tests guarantee a good completion')
    return dict(status='no-witness',examined=examined)


def stress():
    start=time.monotonic();rng=random.Random(101441);best=None;records=[]
    for rep in range(500):
        if time.monotonic()-start>100:break
        g=nx.octahedral_graph()
        target=rng.choice((20,30,40,50))
        while len(g)<target:g=split(g,rng)
        b=Instance(g);root=rng.randrange(len(b.faces));b=Instance(g,root)
        st=Counter();t=time.perf_counter();s=enumerate_tree(b,st)
        row=dict(rep=rep,V=len(g),seconds=time.perf_counter()-t,stats=dict(st),exists=s is not None)
        if s is not None:
            cert=b.recover(s);assert verify(b.G,cert['cycle'],cert['avoided_edge'])
        records.append(row)
        if best is None or st['candidates']>best['stats']['candidates']:
            best=dict(**row,edges=list(g.edges()),root=list(b.R),state=s)
    (BASE/'stress.json').write_text(json.dumps(dict(seed=101441,records=records,worst=best),indent=2))
    print('stress',len(records),best['stats'])


if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='filtered':
        witness=prefix_attack(True);witness['claim']='After removing individually forest-incompatible incidences, a residual perfect matching guarantees a good completion'
        (BASE/'filtered-prefix-counterexample.json').write_text(json.dumps(witness,indent=2));print(witness);sys.exit()
    witness=prefix_attack();(BASE/'prefix-counterexample.json').write_text(json.dumps(witness,indent=2));print({k:v for k,v in witness.items() if k not in ('edges','good_states','faces')},flush=True)
    stress()
