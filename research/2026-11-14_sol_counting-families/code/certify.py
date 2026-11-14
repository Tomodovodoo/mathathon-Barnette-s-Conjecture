"""Build a stationary tube matching matrix; certify Krylov recurrences exactly."""
from transfer import *
import sympy as sp

def advance(dp,active,rows,final,tree):
    last={v:i for i,f in enumerate(rows) for v in f if v!=-1}
    for v in final:last[v]=len(rows)
    for i,f in enumerate(rows):
        live=tuple(sorted(set(active)|set(f)|{-1}));keep=tuple(v for v in live if v==-1 or last[v]>i);nd=defaultdict(int)
        for (bits,part),value in dp.items():
            used=dict(zip(active,bits));labels=dict(zip(active,part));fresh=max(part,default=-1)+1
            for v in live:
                if v not in labels:labels[v]=fresh;fresh+=1
            for j,v in enumerate(f):
                if v==-1 or used.get(v,0):continue
                nu={x:int(used.get(x,0) or x==v) for x in live}
                if any(x!=-1 and last[x]==i and not nu[x] for x in live):continue
                lab=labels.copy()
                if tree:
                    a,c=[f[k] for k in range(3) if k!=j];la,lc=lab[a],lab[c]
                    if la==lc:continue
                    lab={x:la if z==lc else z for x,z in lab.items()}
                nd[tuple(nu[x] for x in keep),canon([lab[x] for x in keep]) if tree else ()]+=value
        active=keep;dp=nd
    return dp,active

def recurrence(seq,maxd=20):
    for d in range(1,min(maxd,len(seq)//2)+1):
        a=sp.Matrix([[seq[k-j-1] for j in range(d)] for k in range(d,len(seq))]);b=sp.Matrix(seq[d:])
        try:sol,free=a.gauss_jordan_solve(b)
        except ValueError:continue
        if not free.rows:return list(sol)
    return None

def certificate(p,tree):
    b=Instance(tube(p,6));poles={6*p+p,6*p+p+1}
    rows=[b.faces[t] for t in face_order(b,p)]
    level=lambda f:max(v//p for v in f if v not in poles)
    pre=[tuple(-1 if v in b.R else v for v in f) for f in rows if level(f)<=2]
    init,active=advance({((),()):1},(),pre,set(range(2*p,3*p)),tree)
    boundary=(-1,)+tuple(range(p))
    assert active==(-1,)+tuple(range(2*p,3*p))
    layer=[tuple(v-2*p for v in f) for f in rows if level(f)==3]
    # Exact same local triangle list at every middle layer, after translation.
    for j in (4,5):assert layer==[tuple(v-(j-1)*p for v in f) for f in rows if level(f)==j]
    cap=[tuple(v-6*p if v not in poles else p for v in f) for f in rows if poles.__contains__(6*p+p+1) and 6*p+p+1 in f]
    keys=list(init);trans={};i=0
    while i<len(keys):
        key=keys[i];i+=1
        out,live=advance({key:1},boundary,layer,set(range(p,2*p)),tree)
        assert live==(-1,)+tuple(range(p,2*p))
        trans[key]=out
        for x in out:
            if x not in keys:keys.append(x)
    # Numerically indexed sparse integer matrix, row-vector convention.
    ix={k:i for i,k in enumerate(keys)};edges=[[ix[k],ix[z],v] for k in keys for z,v in trans[k].items()]
    v0=[init.get(k,0) for k in keys];w=[]
    for k in keys:
        out,_=advance({k:1},boundary,cap,set(),tree);w.append(sum(out.values()))
    vectors=[v0]
    for _ in range(24):
        z=[0]*len(keys)
        for a,c,n in edges:z[c]+=vectors[-1][a]*n
        vectors.append(z)
    seq=[sum(a*c for a,c in zip(v,w)) for v in vectors];rec=recurrence(seq)
    # Certify the proposed relation as a vector identity. This implies every
    # future scalar identity, independent of observed scalar agreement.
    d=len(rec);identity=all(vectors[d][j]==sum(rec[k]*vectors[d-k-1][j] for k in range(d)) for j in range(len(keys)))
    if not identity:
        # The row relation may be stronger than scalar minimality. Test the
        # scalar annihilator on the full reachable Krylov space instead.
        vectors=[v0]
        for _ in range(len(keys)+d):
            z=[0]*len(keys)
            for a,c,n in edges:z[c]+=vectors[-1][a]*n
            vectors.append(z)
        seq=[sum(a*c for a,c in zip(v,w)) for v in vectors]
        identity=all(seq[i]==sum(rec[k]*seq[i-k-1] for k in range(d)) for i in range(d,len(seq)))
    assert identity
    # Cayley-Hamilton makes len(keys) consecutive zero discrepancies sufficient.
    return {'width':p,'quantity':'TM' if tree else 'states','matrix_dimension':len(keys),'boundary_keys':keys,'matrix_entries':edges,'initial':v0,'terminal':w,'recurrence':[int(x) if x.q==1 else str(x) for x in rec],'initial_L2_onward':seq[:d],'certified':identity,'scalar_sequence_L2_onward':seq[:20]}

if __name__=='__main__':
    out=[]
    for p in (4,6):
        for tree in (False,True):
            row=certificate(p,tree);out.append(row);print({k:row[k] for k in ('width','quantity','matrix_dimension','recurrence','initial_L2_onward')},flush=True)
    (Path(__file__).resolve().parents[1]/'data'/'certificates.json').write_text(json.dumps(out,indent=2))
