"""Check the Hall deficiency by embedded region traversal, all eligible U, both colours.
Usage: python -B code/deficiency.py MIN MAX data/output.json
U must be connected and contain an actual face, which supplies a possible root.
The tested formula is independent of which black face in U is chosen as root.
"""
from common import *
import json, time
import sympy as sp

def symbolic():
    p,b,w,q,D,W=sp.symbols('p b w q D W')
    # Euler: m=p+b+w+q-2. Side count and global balance solve for b,w.
    m=p+b+w+q-2
    sol=sp.solve([2*m-3*(b+w)-D, 3*(w-b)-(D-2*W)], [b,w])
    residual=sp.simplify((2*p-4-m+b-(D+W-6*q)/3).subs(sol))
    assert residual==0
    return str(residual)

res={'symbolic_residual':symbolic(),'per_V':{}}
for nv in range(int(sys.argv[1]),int(sys.argv[2])+1):
    start=time.time(); C={'graphs':0,'eligible_colour_subsets':0,'regions':0,'repeated_boundary_regions':0,'failures':0}
    for gid,rot in enumerate(et.plantri(nv)):
        C['graphs']+=1
        fs=et.faces_of(rot); col=et.two_colour(fs)
        side={(f[i],f[(i+1)%3]):k for k,f in enumerate(fs) for i in range(3)}
        fm=[sum(1<<v for v in f) for f in fs]
        for um in range(1<<nv):
            if um.bit_count()<3:continue
            actual=[k for k,m in enumerate(fm) if m&um==m]
            if not actual:continue
            U={v for v in range(nv) if um>>v&1}
            if not connected(rot,U):continue
            S=set(range(nv))-U
            regions=[]
            for walk in walks(rot,U):
                original={side[e] for e in walk}
                if len(walk)==3 and len(original)==1:continue
                regions.append(walk)
            for black in set(col[k] for k in actual):
                direct=sum(min(2,len(set(f)&S)) for f,c in zip(fs,col) if c==black)-2*len(S)
                numerator=sum(len(walk)+sum(col[side[e]]!=black for e in walk)-6 for walk in regions)
                C['eligible_colour_subsets']+=1; C['regions']+=len(regions)
                C['repeated_boundary_regions']+=sum(len({u for u,v in walk})<len(walk) for walk in regions)
                if 3*direct!=numerator:
                    C['failures']+=1
                    raise AssertionError((nv,gid,U,black,direct,numerator,regions))
    C['seconds']=round(time.time()-start,2); res['per_V'][nv]=C
    print(nv,C,flush=True)
    Path(sys.argv[3]).write_text(json.dumps(res,indent=2))
