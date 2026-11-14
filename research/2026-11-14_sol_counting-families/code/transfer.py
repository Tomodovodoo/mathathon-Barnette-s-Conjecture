"""Exact face-frontier transfer, no state enumeration. TM uses root contraction.

State key is used-vertex bits plus the connectivity partition of Q on live
vertices. Each triangle adds its opposite edge. Reject a cycle. Forgotten
vertices must already be matched. See FAMILIES.md for correctness proof.
"""
from families import *
from collections import defaultdict
import json,time,argparse

def canon(labels):
    d={};return tuple(d.setdefault(x,len(d)) for x in labels)

def face_order(b,p=None):
    if p is None:return list(b.A)
    poles={max(b.T),max(b.T)-1}
    return sorted(b.A,key=lambda t:(max(v//p for v in b.faces[t] if v not in poles),sum(v for v in b.faces[t] if v not in poles),t))

def matching_transfer(b,tree=False,p=None):
    fs=face_order(b,p); faces=[tuple(-1 if v in b.R else v for v in b.faces[t]) for t in fs]
    last={v:i for i,f in enumerate(faces) for v in f if v!=-1}
    active=(); dp={((),()):1};peak=0
    for i,f in enumerate(faces):
        live=tuple(sorted(set(active)|set(f)|{-1}));pos={v:j for j,v in enumerate(live)}
        keep=tuple(v for v in live if v==-1 or last[v]>i); nxt=defaultdict(int)
        for (bits,part),value in dp.items():
            used={v:bits[j] for j,v in enumerate(active)}
            labels={v:part[j] for j,v in enumerate(active)} if tree else {}
            fresh=max(labels.values(),default=-1)+1
            for v in live:
                if v not in labels:labels[v]=fresh;fresh+=1
            for j,v in enumerate(f):
                if v==-1 or used.get(v,0):continue
                nu={x:used.get(x,0) or x==v for x in live}
                if any(x!=-1 and last[x]==i and not nu[x] for x in live):continue
                lab=labels.copy()
                if tree:
                    a,c=[f[k] for k in range(3) if k!=j]
                    la,lc=lab[a],lab[c]
                    if la==lc:continue
                    lab={x:la if z==lc else z for x,z in lab.items()}
                key=(tuple(int(nu[x]) for x in keep),canon([lab[x] for x in keep]) if tree else ())
                nxt[key]+=value
        dp=nxt;active=keep;peak=max(peak,len(dp))
        if not dp:return 0,peak
    return sum(dp.values()),peak

def pair_transfer(b,p=None):
    fs=face_order(b,p);faces=[tuple(v for v in b.faces[t] if v not in b.R) for t in fs]
    last={v:i for i,f in enumerate(faces) for v in f}
    active=();dp={((),(),(),0):1};peak=0
    for i,f in enumerate(faces):
        live=tuple(sorted(set(active)|set(f)));keep=tuple(v for v in live if last[v]>i);nd=defaultdict(int)
        for (br,bs,part,c),value in dp.items():
            ur=dict(zip(active,br));us=dict(zip(active,bs));ls=dict(zip(active,part));fresh=max(part,default=-1)+1
            for v in live:
                if v not in ls:ls[v]=fresh;fresh+=1
            for r in f:
                if ur.get(r,0):continue
                for s in f:
                    if r==s or us.get(s,0):continue
                    rr={v:int(ur.get(v,0) or v==r) for v in live};ss={v:int(us.get(v,0) or v==s) for v in live}
                    if any(not rr[v] or not ss[v] for v in live if v not in keep):continue
                    a,z=ls[r],ls[s];cc=c+int(a==z);ll={v:a if x==z else x for v,x in ls.items()}
                    nd[tuple(rr[v] for v in keep),tuple(ss[v] for v in keep),canon([ll[v] for v in keep]),cc]+=value
        dp=nd;active=keep;peak=max(peak,len(dp))
    hist=defaultdict(int)
    for (_,_,_,c),v in dp.items():hist[c]+=v
    return dict(hist),peak

def hc_transfer(g,order=None,forbidden=None):
    """Edge-frontier DP for connected 2-factors, exact integer counts."""
    es=list(g.edges()) if order is None else order
    if forbidden is not None:es=[e for e in es if set(e)!=set(forbidden)]
    last={v:i for i,e in enumerate(es) for v in e}
    active=();dp={((),()):1};peak=0;result=0
    for i,(u,v) in enumerate(es):
        live=tuple(sorted(set(active)|{u,v}));keep=tuple(x for x in live if last[x]>i);nd=defaultdict(int)
        for (deg,part),value in dp.items():
            ds=dict(zip(active,deg));ls=dict(zip(active,part));fresh=max(part,default=-1)+1
            for x in live:
                ds.setdefault(x,0)
                if x not in ls:ls[x]=fresh;fresh+=1
            for take in (0,1):
                dd=ds.copy();ll=ls.copy()
                if take:
                    dd[u]+=1;dd[v]+=1
                    if dd[u]>2 or dd[v]>2:continue
                    a,c=ll[u],ll[v]
                    if a==c:
                        # A cycle may close only when it is the final whole cycle.
                        if any(dd[x]!=2 for x in live) or any(last[x]>i and x not in live for x in g):continue
                        # Future edges must all be excluded; count this completion now.
                        if all(x in live or last[x]<i for x in g):
                            nd[('DONE',())]+=value
                        continue
                    ll={x:a if z==c else z for x,z in ll.items()}
                if any(dd[x]!=2 for x in live if x not in keep):continue
                # Losing an entire connected component before closure is forbidden.
                if any(not any(ll[y]==ll[x] for y in keep) for x in live if x not in keep):continue
                nd[tuple(dd[x] for x in keep),canon([ll[x] for x in keep])]+=value
        # DONE is accumulated externally so it never goes through another edge.
        done=nd.pop(('DONE',()),0)
        if done: result+=done
        dp=nd;active=keep;peak=max(peak,len(dp))
    return result,peak

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--width',type=int,default=4);ap.add_argument('--max',type=int,default=12);args=ap.parse_args()
    start=time.monotonic();out=[]
    for L in range(args.max+1):
        b=Instance(tube(args.width,L));s,ps=matching_transfer(b,p=args.width);t,pt=matching_transfer(b,True,args.width)
        # Dual face IDs inherit planar embedding order. Order primal edges by
        # the earlier of the layer coordinates of their two incident triangles.
        rank={f:i for i,f in enumerate(sorted(range(len(b.faces)),key=lambda f:(max(v//args.width for v in b.faces[f] if v<max(b.T)-1),f)))}
        es=sorted(b.G.edges(),key=lambda e:(min(rank[e[0]],rank[e[1]]),max(rank[e[0]],rank[e[1]])))
        h,ph=hc_transfer(b.G,es)
        row={'L':L,'states':s,'TM':t,'HC':h,'peak_states':ps,'peak_TM':pt,'peak_HC':ph}
        out.append(row);print(row,flush=True)
        (Path(__file__).resolve().parents[1]/'data'/f'transfer{args.width}.json').write_text(json.dumps(out,indent=2))
        if time.monotonic()-start>500:break
