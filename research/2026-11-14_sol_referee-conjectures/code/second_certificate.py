"""Second implementation: state brute force, literal H0 digraph and cycle reversals.

Does not import independent.py. It consumes only the saved graph and face lists.
"""
import collections as co
import itertools as it
import json
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]

def check(name):
    d=json.loads((HERE/'data'/name).read_text())
    faces=d['faces_A']; roots=set(d['root']);N=d['V']; X=set(range(N))-roots
    opts=[sorted(set(f)-roots) for f in faces]; order=sorted(range(len(faces)),key=lambda k:len(opts[k]))
    states=[];s=[None]*len(faces)
    def visit(k,used):
        if k==len(faces):states.append(tuple(s));return
        j=order[k]
        for v in opts[j]:
            if v not in used:s[j]=v;visit(k+1,used|{v})
    visit(0,set())
    factors=co.defaultdict(list)
    for r in states:
        for s in states:
            if all(a!=b for a,b in zip(r,s)):
                u=tuple(next(v for v in f if v!=r[k] and v!=s[k]) for k,f in enumerate(faces))
                factors[u].append((r,s))
    def tree(s):
        adj=co.defaultdict(list)
        for k,f in enumerate(faces):
            a,b=[v for v in f if v!=s[k]];adj[a].append(b);adj[b].append(a)
        seen=set()
        for a in range(N):
            if a in seen:continue
            stack=[(a,-1)];vertices=[]
            while stack:
                a,p=stack.pop()
                if a in seen:return False
                seen.add(a);vertices.append(a)
                stack.extend((b,a) for b in adj[a] if b!=p)
            if len(roots&set(vertices))!=1:return False
        return True
    rot={int(k):v for k,v in d.get('rotation',{}).items()}
    # Independent potential integration from the submitted hfaces, whose darts
    # are checked against rotation at each vertex below.
    hf=d['hfaces']; left={}
    if rot:
        lookup={frozenset(f):k for k,f in enumerate(faces)}
        hr={}
        for a,ns in rot.items():
            hr[a]=[N+lookup[frozenset((a,b,c))] for b,c in zip(ns,ns[1:]+ns[:1]) if frozenset((a,b,c)) in lookup]
        for k,f in enumerate(faces):hr[N+k]=f
        for f in hf:
            for a,b,c in zip(f,f[1:]+f[:1],f[2:]+f[:2]):assert hr[b][(hr[b].index(a)-1)%len(hr[b])]==c
    for j,f in enumerate(hf):
        for a,b in zip(f,f[1:]+f[:1]):
            assert (a,b) not in left;left[a,b]=j
    outer=max(range(len(hf)),key=lambda j:len(hf[j])); us=sorted(factors);base=us[0]
    phis=[]
    for u in us:
        eq=[]
        for k,f in enumerate(faces):
            for v in f:
                a,b=(v,N+k) if v==base[k] else (N+k,v)
                l,r=left[a,b],left[b,a]
                eq.append((l,r,-int((u[k]==v)!=(base[k]==v))))
        phi={outer:0}
        while len(phi)<len(hf):
            old=len(phi)
            for l,r,z in eq:
                if l in phi:phi[r]=phi[l]+z
                elif r in phi:phi[l]=phi[r]-z
            assert len(phi)>old
        assert all(phi[r]-phi[l]==z for l,r,z in eq)
        phis.append(tuple(phi[k] for k in range(len(hf))))
    lower=[];upper=[]
    for i,p in enumerate(phis):
        down=[j for j,q in enumerate(phis) if j!=i and all(a<=b for a,b in zip(q,p))]
        lower.append([j for j in down if not any(j!=k and all(a<=b for a,b in zip(phis[j],phis[k])) for k in down)])
        up=[j for j,q in enumerate(phis) if j!=i and all(a>=b for a,b in zip(q,p))]
        upper.append([j for j in up if not any(j!=k and all(a>=b for a,b in zip(phis[j],phis[k])) for k in up)])
    tp=[sum(tree(s) for r,s in factors[u]) for u in us]
    old={tuple(e['u']):e for e in d['entries']}
    for i,u in enumerate(us):assert old[u]['tree_pairs']==tp[i]
    candidates=[i for i in range(len(us)) if len(lower[i])<=1 or len(upper[i])<=1]
    result={'input':name,'states':len(states),'pairs':sum(map(len,factors.values())),'factors':len(factors),
            'tree_pairs':sum(tp),'candidate_tree_counts':[tp[i] for i in candidates],
            'R2':any(tp[i] for i in candidates)}
    (HERE/'data'/('second_'+name)).write_text(json.dumps(result,indent=2)+'\n')
    print(result)

if __name__=='__main__':check('R2_glued_V33.json')
