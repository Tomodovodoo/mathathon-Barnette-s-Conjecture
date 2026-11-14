"""HC avoiding the primal edge dual to an arbitrary specified tube dual edge.

Mark that dual edge monochromatic in the induced-tree transfer.
"""
from hamilton_matrix import *

def avoiding(p,L,e):
    a,b=sorted(e);pole0=(L+1)*p;pole1=pole0+1
    # Identify the stage that introduces this edge, and its local endpoints.
    if b==pole0:stage=0;local=(0,1+a)
    elif b==pole1:stage=L+1;local=(a-L*p,p)
    else:
        ja,ia=divmod(a,p);jb,ib=divmod(b,p)
        if ja==jb:stage=ja;local=(ia+p,ib+p) if ja else (ia+1,ib+1)
        else:stage=jb;local=(ia,p+ib)
    dp=defaultdict(int)
    for col in product((0,1),repeat=p):
        cs=(0,)+col
        if stage==0 and cs[local[0]]!=cs[local[1]]:continue
        k=update(((0,),(0,)),col,p,initial=True)
        if k is not None:dp[k]+=1
    for j in range(1,L+1):
        nd=defaultdict(int)
        for k,n in dp.items():
            for col in product((0,1),repeat=p):
                cs=k[0]+col
                if stage==j and cs[local[0]]!=cs[local[1]]:continue
                z=update(k,col,p)
                if z is not None:nd[z]+=n
        dp=nd
    result=0
    for k,n in dp.items():
        for c in (0,1):
            cs=k[0]+(c,)
            if stage==L+1 and cs[local[0]]!=cs[local[1]]:continue
            if update(k,(c,),p,terminal=True):result+=n
    return result

if __name__=='__main__':
    out=[]
    for p in (4,6):
        for L in range(1,9):
            # Three edges of the specified root, plus one edge at the far cap.
            es=[(0,1),(0,p+1),(1,p+1),(L*p,(L+1)*p+1)]
            vals=[avoiding(p,L,e) for e in es]
            out.append({'width':p,'L':L,'dual_edges':es,'avoiding':vals});print(p,L,vals,flush=True)
    (Path(__file__).resolve().parents[1]/'data'/'avoidance.json').write_text(json.dumps(out,indent=2))
