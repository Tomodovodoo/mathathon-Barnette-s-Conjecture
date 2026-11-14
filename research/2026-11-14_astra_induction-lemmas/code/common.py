"""Read-only access to the previous independently checked enumerator."""
import sys
from pathlib import Path
sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parents[1]
sys.path.insert(0, str(REPO / 'research/2026-11-14_fable_induction-completion/code'))
import et

def connected(rot, U):
    if not U: return False
    seen = {next(iter(U))}
    stack = list(seen)
    while stack:
        for v in rot[stack.pop()]:
            if v in U and v not in seen:
                seen.add(v); stack.append(v)
    return seen == U

def walks(rot, U):
    rr = {v: [u for u in rot[v] if u in U] for v in U}
    nxt = {(u,v): (v,nb[(i+1)%len(nb)]) for v,nb in rr.items() for i,u in enumerate(nb)}
    seen=set(); out=[]
    for e in nxt:
        if e in seen: continue
        f=[]; cur=e
        while cur not in seen:
            seen.add(cur); f.append(cur); cur=nxt[cur]
        out.append(f)
    return out

def mate(s, root):
    adj={}
    for f,u in s.items():
        a,b=[v for v in f if v!=u]
        adj.setdefault(a,[]).append((b,f)); adj.setdefault(b,[]).append((a,f))
    seen=set(root); stack=list(root); r={}
    while stack:
        v=stack.pop()
        for u,f in adj.get(v,[]):
            if u not in seen:
                seen.add(u); stack.append(u); r[f]=u
    assert len(r)==len(s)
    return r

def tree(s, root):
    par={v:v for f in s for v in f}
    for v in root: par[v]=v
    def find(v):
        while par[v]!=v: v=par[v]
        return v
    for a,b in et.root_edges(root)+[tuple(v for v in f if v!=u) for f,u in s.items()]:
        a,b=find(a),find(b)
        if a==b:return False
        par[a]=b
    return len({find(v) for v in par})==1
