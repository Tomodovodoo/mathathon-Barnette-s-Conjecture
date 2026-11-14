import sys
from independent import *

def qcycles(I,r,s):
    out={r[k]:(I.u_of(r,s)[k],k) for k in range(I.n)}
    done=set();cycles=[]
    for a in I.X:
        path=[];where={};v=a
        while v in out and v not in done and v not in where:
            where[v]=len(path);path.append(v);v=out[v][0]
        if v in where:cycles.append([out[w][1] for w in path[where[v]:]])
        done.update(path)
    return cycles

def check(I):
    pairs=[(r,s) for u in I.factors() for r,s in I.decompositions(u)]
    lookup={p:i for i,p in enumerate(pairs)};ks=[len(qcycles(I,r,s)) for r,s in pairs]
    rev=co.defaultdict(list);moves=0; flipped=0
    weights=I.spoke_weights(); sums=co.Counter()
    for i,(r,s) in enumerate(pairs):
        u=I.u_of(r,s);sums[s]+=I.sign(r,s)
        targets=[]
        for c in I.cycles(u):
            rr=list(r);ss=list(s)
            for a,b,k in c:rr[k],ss[k]=ss[k],rr[k]
            targets.append((tuple(rr),tuple(ss)))
            delta=sum(1 if I.A[k][(I.A[k].index(a)+1)%3]==b else -1 for a,b,k in c)
            w=sum(weights[k,b]-weights[k,a] for a,b,k in c)
            assert abs(delta)==3 and w*delta<0
        for c in qcycles(I,r,s):
            rr=list(r)
            for k in c:rr[k]=u[k]
            rr=tuple(rr);unew=I.u_of(rr,s)
            assert I.sign(rr,s)==-I.sign(r,s)
            phi=I.potential(unew,u)
            nz={x for x in phi if x};assert nz in ({1},{-1})
            targets.append((rr,s));flipped+=1
        for target in targets:
            j=lookup[target]
            if ks[j]<=ks[i]:rev[j].append(i);moves+=1
    for s,total in sums.items():assert total in (-1,1) if I.forest(s) else total==0
    seen={i for i,k in enumerate(ks) if k==0};q=list(seen)
    for i in q:
        for j in rev[i]:
            if j not in seen:seen.add(j);q.append(j)
    assert len(seen)==len(pairs)
    return {'pairs':len(pairs),'moves':moves,'Q_reversals':flipped}

if __name__=='__main__':
    totals=co.Counter();rows=[]
    for n in range(6,int(sys.argv[1])+1):
        row=co.Counter(V=n)
        for rot in plantri(n):
            for root in facial_walks(rot)[0]:
                row.update(check(Instance(rot,root)));row['roots']+=1
        rows.append(dict(row));print(dict(row),flush=True)
    for p in (ROOT/'research/2026-11-14_opus_route-graph-theory/code/data').glob('*trap*.json'):
        d=json.loads(p.read_text());I=Instance({int(k):v for k,v in d['rot'].items()},d['t0'])
        row=check(I);row['file']=p.name;rows.append(row);print(row,flush=True)
    save('cancellations_'+sys.argv[1]+'.json',rows)
