"""Stationary pair transfer with a formal variable marking D components."""
from certify import *
from collections import Counter

def advance_pairs(dp,active,rows,final):
    last={v:i for i,f in enumerate(rows) for v in f}
    for v in final:last[v]=len(rows)
    for i,f in enumerate(rows):
        live=tuple(sorted(set(active)|set(f)));keep=tuple(v for v in live if last[v]>i);nd=defaultdict(Counter)
        for (br,bs,part),pol in dp.items():
            ur=dict(zip(active,br));us=dict(zip(active,bs));ls=dict(zip(active,part));fresh=max(part,default=-1)+1
            for v in live:
                if v not in ls:ls[v]=fresh;fresh+=1
            for r in f:
                if ur.get(r,0):continue
                for s in f:
                    if r==s or us.get(s,0):continue
                    rr={v:int(ur.get(v,0) or v==r) for v in live};ss={v:int(us.get(v,0) or v==s) for v in live}
                    if any(not rr[v] or not ss[v] for v in live if v not in keep):continue
                    a,z=ls[r],ls[s];inc=int(a==z);ll={v:a if x==z else x for v,x in ls.items()}
                    key=tuple(rr[v] for v in keep),tuple(ss[v] for v in keep),canon([ll[v] for v in keep])
                    for c,n in pol.items():nd[key][c+inc]+=n
        dp=nd;active=keep
    return dp,active

def certificate_pairs(p):
    b=Instance(tube(p,6));poles={7*p,7*p+1};rows=[b.faces[t] for t in face_order(b,p)]
    level=lambda f:max(v//p for v in f if v not in poles)
    pre=[tuple(v for v in f if v not in b.R) for f in rows if level(f)<=2]
    init,active=advance_pairs({((),(),()):Counter({0:1})},(),pre,set(range(2*p,3*p)))
    assert active==tuple(range(2*p,3*p))
    layer=[tuple(v-2*p for v in f) for f in rows if level(f)==3]
    cap=[tuple(v-6*p if v not in poles else p for v in f) for f in rows if 7*p+1 in f]
    keys=list(init);trans={};i=0
    while i<len(keys):
        k=keys[i];i+=1;out,live=advance_pairs({k:Counter({0:1})},tuple(range(p)),layer,set(range(p,2*p)));trans[k]=out
        for z in out:
            if z not in keys:keys.append(z)
    ix={k:i for i,k in enumerate(keys)};edges=[[ix[k],ix[z],dict(pol)] for k in keys for z,pol in trans[k].items()]
    terminal=[]
    for k in keys:
        out,_=advance_pairs({k:Counter({0:1})},tuple(range(p)),cap,set());terminal.append(dict(sum(out.values(),Counter())))
    polys=[init.get(k,Counter()) for k in keys];seq=[];hist=[];mins=[]
    # Boolean cost<=1 vector eventually repeats, certifying cmin=1 forever.
    seen={};period=None
    for r in range(101):
        total=Counter()
        for a,w in zip(polys,terminal):
            for x,n in a.items():
                for y,m in w.items():total[x+y]+=n*m
        seq.append(sum(total.values()));hist.append(dict(total));mins.append(min(total))
        state=tuple(tuple(c for c in (0,1) if pol.get(c,0)) for pol in polys)
        if state in seen and period is None:period=[seen[state],r]
        seen.setdefault(state,r)
        nxt=[Counter() for _ in keys]
        for a,z,pol in edges:
            for x,n in polys[a].items():
                for y,m in pol.items():nxt[z][x+int(y)]+=n*m
        polys=nxt
    rec=recurrence(seq[:2*len(keys)+10],40);d=len(rec)
    assert len(seq)>=len(keys)+d and all(seq[i]==sum(rec[j]*seq[i-j-1] for j in range(d)) for i in range(d,len(seq)))
    assert period and set(mins)=={1}
    return {'width':p,'matrix_dimension':len(keys),'matrix_entries':edges,'initial':[dict(init.get(k,{})) for k in keys],'terminal':terminal,'recurrence':[int(x) for x in rec],'initial_L2_onward':seq[:d],'histograms_L2_onward':hist[:20],'cmin_range':[2,102],'cost01_boolean_repeat':period,'certified':True}

if __name__=='__main__':
    out=[]
    for p in (4,6):
        r=certificate_pairs(p);out.append(r);print({k:r[k] for k in ('width','matrix_dimension','recurrence','initial_L2_onward','cost01_boolean_repeat')},flush=True)
    (Path(__file__).resolve().parents[1]/'data'/'pair-certificates.json').write_text(json.dumps(out,indent=2))
