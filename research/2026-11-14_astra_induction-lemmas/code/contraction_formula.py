"""Check contraction Hall formulas on every subset and root through specified V.
Usage: python -B code/contraction_formula.py MIN MAX OUT.json
"""
from common import *
import json,time,collections
res={}
for nv in range(int(sys.argv[1]),int(sys.argv[2])+1):
    C=collections.Counter();start=time.time()
    for rot in et.plantri(nv):
        for B,ri,W in et.rooted_instances(rot):
            root=B[ri];A=[f for i,f in enumerate(B) if i!=ri]
            masks=[sum(1<<v for v in f) for f in A]
            def f(S):return sum(min(2,(m&S).bit_count()) for m in masks)-2*S.bit_count()
            for x,a,p,b,q in et.degree4_setups(B,W,root):
                for a,p,b,q in ((a,p,b,q),(p,a,q,b)):
                    cb,cri=et.contract(B,ri,x,p,q); keep,drop=(q,p) if q in root else (p,q)
                    X=sorted({v for ff in cb for v in ff}-set(cb[cri]));cm=[sum(1<<v for v in ff) for i,ff in enumerate(cb) if i!=cri]
                    C['merges']+=1
                    for sm in range(1<<len(X)):
                        S=sum(1<<v for i,v in enumerate(X) if sm>>i&1)
                        actual=sum(min(2,(m&S).bit_count()) for m in cm)-2*len([v for v in X if S>>v&1])
                        if S>>keep&1:
                            predicted=f((S&~(1<<keep))|(1<<p)|(1<<q)|(1<<x))
                            C['merged_in_S']+=1
                        else:
                            predicted=f(S)-int(bool(S>>a&1))-int(bool(S>>b&1))
                            C['merged_not_in_S']+=1
                        assert actual==predicted
    C['seconds']=round(time.time()-start,2);res[nv]=dict(C);print(nv,dict(C),flush=True)
    Path(sys.argv[3]).write_text(json.dumps(res,indent=2))
