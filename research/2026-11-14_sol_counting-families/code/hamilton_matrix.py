"""Stationary HC transfer via the two induced trees in the dual."""
from certify import *
from itertools import product

def update(key,new,p,initial=False,terminal=False):
    colors,part=key;old=len(colors)
    cs=list(colors)+list(new);labels=list(part)+list(range(max(part,default=-1)+1,max(part,default=-1)+1+len(new)))
    es=[];tris=[]
    if initial:
        # old vertex is the first pole, new p vertices form the first ring.
        es=[(old+i,old+(i+1)%p) for i in range(p)]+[(0,old+i) for i in range(p)]
        tris=[(0,old+i,old+(i+1)%p) for i in range(p)]
        keep=list(range(old,old+p))
    elif terminal:
        es=[(i,p) for i in range(p)];tris=[(i,(i+1)%p,p) for i in range(p)];keep=list(range(p+1))
    else:
        es=[(p+i,p+(i+1)%p) for i in range(p)]+[(i,p+i) for i in range(p)]
        for i in range(p):
            j=(i+1)%p
            if i%2==0:es.append((i,p+j));tris.extend(((i,j,p+j),(i,p+j,p+i)))
            else:es.append((j,p+i));tris.extend(((i,j,p+i),(j,p+j,p+i)))
        keep=list(range(p,2*p))
    if any(cs[a]==cs[b]==cs[c] for a,b,c in tris):return None
    for a,b in es:
        if cs[a]!=cs[b]:continue
        x,y=labels[a],labels[b]
        if x==y:return None
        labels=[x if z==y else z for z in labels]
    if terminal:
        return len(set(labels))==2
    if set(cs[i] for i in keep)!={0,1}:return None
    if set(labels)!=set(labels[i] for i in keep):return None
    return tuple(cs[i] for i in keep),canon([labels[i] for i in keep])

def certificate_hc(p):
    init=defaultdict(int)
    for col in product((0,1),repeat=p):
        k=update(((0,),(0,)),col,p,initial=True)
        if k is not None:init[k]+=1
    keys=list(init);trans={};i=0
    while i<len(keys):
        k=keys[i];i+=1;out=defaultdict(int)
        for col in product((0,1),repeat=p):
            z=update(k,col,p)
            if z is not None:
                out[z]+=1
                if z not in keys:keys.append(z)
        trans[k]=out
    ix={k:i for i,k in enumerate(keys)};edges=[[ix[k],ix[z],n] for k in keys for z,n in trans[k].items()]
    v=[init.get(k,0) for k in keys];w=[sum(bool(update(k,(c,),p,terminal=True)) for c in (0,1)) for k in keys]
    vectors=[v]
    for _ in range(2*len(keys)+2):
        z=[0]*len(keys)
        for a,b,n in edges:z[b]+=vectors[-1][a]*n
        vectors.append(z)
    seq=[sum(a*b for a,b in zip(v,w)) for v in vectors]
    rec=recurrence(seq,maxd=40);d=len(rec)
    assert all(seq[i]==sum(rec[j]*seq[i-j-1] for j in range(d)) for i in range(d,len(seq)))
    return {'width':p,'quantity':'HC','matrix_dimension':len(keys),'boundary_keys':keys,'matrix_entries':edges,'initial':v,'terminal':w,'recurrence':[int(x) for x in rec],'initial_L0_onward':seq[:d],'scalar_sequence_L0_onward':seq[:30],'certified':True}

if __name__=='__main__':
    out=[]
    for p in (4,6):
        r=certificate_hc(p);out.append(r);print({k:r[k] for k in ('width','matrix_dimension','recurrence','initial_L0_onward')},flush=True)
    (Path(__file__).resolve().parents[1]/'data'/'HC-certificates.json').write_text(json.dumps(out,indent=2))
