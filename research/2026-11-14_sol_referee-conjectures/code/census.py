import sys,time
from independent import *

def run(n):
    start=time.monotonic(); row=co.Counter(V=n)
    for rot in plantri(n):
        row['graphs']+=1
        for root in facial_walks(rot)[0]:
            I=Instance(rot,root);row['roots']+=1
            sts=list(I.states());us=list(I.factors());row['states']+=len(sts)
            brute={(r,s) for r in sts for s in sts if all(a!=b for a,b in zip(r,s))}
            decomposed={(r,s) for u in us for r,s in I.decompositions(u)}
            assert brute==decomposed
            if not us:assert not brute;continue
            row['feasible']+=1
            ps=[I.potential(u,us[0]) for u in us];lo,hi=I.shortest_extremes(us[0])
            assert lo==tuple(map(min,zip(*ps))) and hi==tuple(map(max,zip(*ps)))
            row['factors']+=len(us); goods=[];tm=0
            for u in us:
                tp=0
                for r,s in I.decompositions(u):
                    good=I.forest(s);assert good==I.criterion(u,r)
                    tp+=good;row['pairs']+=1
                tm+=tp;goods.append(tp>0)
            row['TM']+=tm
            m=min(len(I.cycles(u)) for u in us)
            assert tm>=2**m
            assert (tm==2**m)==(len(us)==1)
            row['equality']+=tm==2**m
            row['C2_failure']+=not goods[ps.index(lo)] and not goods[ps.index(hi)]
            if n<=14:
                a=lattice_analysis(I,us)
                assert a['R2']
    row['seconds']=round(time.monotonic()-start,3)
    print(dict(row),flush=True)
    return dict(row)

if __name__=='__main__':
    rows=[run(n) for n in range(6,int(sys.argv[1])+1)]
    save('census_'+sys.argv[1]+'.json',rows)
