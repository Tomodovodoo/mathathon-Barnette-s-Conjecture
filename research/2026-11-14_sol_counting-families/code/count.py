"""Exact enumeration, predicts in PREDICTIONS.md. 540 second wall budget."""
from families import *
from collections import Counter
from itertools import product
import time,json,argparse
START=time.monotonic()
def deadline():
    if time.monotonic()-START>540: raise TimeoutError('540 second budget')

def states(b):
    opts=[sum(1<<b.X.index(v) for v in b.faces[t] if v in b.X) for t in b.A]
    s=[None]*b.n
    def rec(todo,used):
        if not todo: yield tuple(s); return
        i=min(todo,key=lambda j:(opts[j]&~used).bit_count())
        avail=opts[i]&~used
        while avail:
            x=avail&-avail;avail-=x;s[i]=b.X[x.bit_length()-1]
            yield from rec(todo-{i},used|x)
    yield from rec(set(range(b.n)),0)

def partners(b,s):
    q=b.Q(s); fixed={}; cyc=[]
    for comp in nx.connected_components(q):
        h=q.subgraph(comp); roots=set(comp)&b.R
        if len(roots)==1 and h.number_of_edges()==len(h)-1:
            root=next(iter(roots)); ds=nx.single_source_shortest_path_length(h,root)
            for u,v,d in h.edges(data=True): fixed[d['face']]=u if ds[u]>ds[v] else v
        elif not roots and h.number_of_edges()==len(h):
            c=nx.cycle_basis(h)[0]; cs=set(c)
            ds=nx.multi_source_dijkstra_path_length(h,cs)
            for u,v,d in h.edges(data=True):
                if u not in cs or v not in cs: fixed[d['face']]=u if ds[u]>ds[v] else v
            cyc.append(c)
        else:return
    for bits in product((0,1),repeat=len(cyc)):
        r=fixed.copy()
        for c,bit in zip(cyc,bits):
            for u,v in zip(c,c[1:]+c[:1]):r[q[u][v]['face']]=u if bit else v
        yield tuple(r[t] for t in b.A)

def hc(g):
    """Enumerate perfect matchings independently of state construction."""
    vs=sorted(g); idx={v:i for i,v in enumerate(vs)}
    adj=[sum(1<<idx[w] for w in g[v]) for v in vs]; allmask=(1<<len(vs))-1
    total=0; avoid=Counter(); visited=0
    def rec(mask,es):
        nonlocal total,visited
        visited+=1
        if visited%10000==0: deadline()
        if not mask:
            h=g.copy();h.remove_edges_from(es)
            if nx.is_connected(h):
                total+=1;avoid.update(tuple(sorted(e)) for e in es)
            return
        candidates=[i for i in range(len(vs)) if mask>>i&1]
        i=min(candidates,key=lambda k:(adj[k]&mask).bit_count()); avail=adj[i]&mask
        while avail:
            x=avail&-avail;avail-=x;j=x.bit_length()-1
            rec(mask^(1<<i)^x,es+[(vs[i],vs[j])])
    rec(allmask,[])
    return total,dict(avoid)

def profile(b,do_hc=True,allroots=False):
    ss=list(states(b)); deadline(); coeff=Counter(); ph=Counter(); tm=[]; pairs=0
    a=b.weights()
    for s in ss:
        rs=list(partners(b,s)); pairs+=len(rs)
        if len(rs)==1: tm.append(s)
        for r in rs:
            assert b.valid(r) and all(x!=y for x,y in zip(r,s))
            perm=dict(zip(r,s));left=set(perm);c=0
            while left:
                c+=1;v=next(iter(left))
                while v in left:left.remove(v);v=perm[v]
            ph[c]+=1
            coeff[sum(a.get((t,v),0) for t,v in zip(b.A,s))]+=b.sign(r,s)
    coeff={k:v for k,v in sorted(coeff.items()) if v}
    # Remove irrelevant monomial shift and global sign for portable comparison.
    if coeff:
        shift=min(coeff);sgn=coeff[max(coeff)]//abs(coeff[max(coeff)])
        norm={k-shift:sgn*v for k,v in coeff.items()}
    else:shift=0;sgn=1;norm={}
    assert len(ss)==abs(int(b.K.det()))
    for s in tm:assert b.is_tree(s)
    out={'dual_order':len(b.T),'primal_order':len(b.G),'root':b.outer,'root_vertices':sorted(b.R),
         'states':len(ss),'pairs':pairs,'tree_matchings':len(tm),'forest_pairs':len(tm),
         'pair_cycle_histogram':dict(ph),'cmin':min(ph) if ph else None,
         'polynomial':coeff,'normalized_polynomial':norm,'shift':shift,'global_sign':sgn,
         'dual_edges':sorted([list(e) for e in b.T.edges()])}
    if do_hc:
        total,av=hc(b.G);out['HC']=total
        out['avoid']={str(e):av.get(b.dual_edges[e],0) for e in sorted(b.dual_edges)}
        out['root_avoid']=[av.get(b.dual_edges[tuple(sorted(e))],0) for e in zip(b.faces[b.outer],b.faces[b.outer][1:]+b.faces[b.outer][:1])]
        images=set()
        for s in tm:
            for e in zip(b.faces[b.outer],b.faces[b.outer][1:]+b.faces[b.outer][:1]):
                cert=b.recover(s,e);c=cert['cycle'];images.add(tuple(sorted(tuple(sorted(x)) for x in zip(c,c[1:]+c[:1]))))
        out['images_over_three_edges']=len(images)
        assert len(images)==3*len(tm) and len(images)<=total
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('family',choices=['prism','tube4','tube6','stack','inflation']);p.add_argument('--max',type=int,default=6);p.add_argument('--no-hc',action='store_true');args=p.parse_args()
    dest=Path(__file__).resolve().parents[1]/'data'/f'{args.family}.json';out=[]
    for k in range(1,args.max+1):
        if args.family=='prism':b=Instance(tube(2*k+2,0))
        elif args.family.startswith('tube'):b=Instance(tube(int(args.family[4:]),k))
        elif args.family=='stack':b=stack(6,k)
        else:
            g=nx.octahedral_graph()
            for _ in range(k):g=subdivide(g)
            b=Instance(g)
        row=profile(b,not args.no_hc);row['parameter']=k;out.append(row)
        dest.write_text(json.dumps(out,indent=2));print({key:row[key] for key in ('parameter','primal_order','states','pairs','tree_matchings','cmin','normalized_polynomial')},flush=True)
