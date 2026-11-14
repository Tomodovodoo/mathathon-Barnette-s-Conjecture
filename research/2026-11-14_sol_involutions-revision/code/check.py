"""Run from repo root: python research/2026-11-14_sol_involutions-revision/code/check.py 14.
Base maps copied with attribution from sol_li-completion/verify.py; path token data,
all extra sign checks, and dual-tree construction implemented for this revision.
"""
import sys,json,math,time
from pathlib import Path
from collections import Counter,deque
from base import Check,enumerate_classes,from_code,ROOT
OUT=Path(__file__).resolve().parents[1]
class Paths(Check):
    def __init__(self,faces,root,reverse=False):
        super().__init__(faces,root)
        adj={i:set() for i in range(len(faces))}
        for (u,v),i in self.side.items():adj[i].add(self.side[v,u])
        parent={root:None};q=deque([root])
        while q:
            i=q.popleft()
            for j in sorted(adj[i],reverse=reverse):
                if j not in parent:parent[j]=i;q.append(j)
        self.paths={};self.turns={}
        for w in self.w:
            path=[w]
            while path[-1]!=root:path.append(parent[path[-1]])
            self.paths[w]=path
            for step,t in enumerate(path[1:-1],1):
                if t not in self.a:continue
                f=self.f[t];prev=set(f)&set(self.f[path[step-1]]);nxt=set(f)&set(self.f[path[step+1]])
                v,=prev&nxt
                edges=[set((f[k],f[(k+1)%3])) for k in range(3)]
                e=edges.index(prev);ex=edges.index(nxt)
                kap=(-1 if ex==(e+1)%3 else 1)*self.orientation
                self.turns[w,self.a.index(t)]=(step,v,kap)
        self.cache={}
    def data(self,p):
        if p in self.cache:return self.cache[p]
        # Reuse independently checked cycle/J/Q_s enumeration, replace all ray data.
        cs,qs,J,_=super().data(p)
        hits={}
        for c in cs:
            for w in self.w:
                h=[]
                for i in c:
                    if (w,i) not in self.turns:continue
                    step,v,kap=self.turns[w,i]
                    for k in (0,1):
                        if p[k][i]==v:h.append((step,i,k))
                hits[c,w]=tuple(sorted(h))
                # Independent winding test in rational Tutte coordinates.
                verts=[];cur=p[0][c[0]];perm=dict(zip(*p))
                while cur not in verts:verts.append(cur);cur=perm[cur]
                poly=[self.pos[v] for v in verts];x,y=self.cen[w];wn=0
                for a,b in zip(poly,poly[1:]+poly[:1]):
                    det=(b[0]-a[0])*(y-a[1])-(b[1]-a[1])*(x-a[0])
                    if a[1]<=y<b[1] and det>0:wn+=1
                    if b[1]<=y<a[1] and det<0:wn-=1
                hh=hits[c,w]
                assert len(hh)%2==int(wn!=0)
                dirs=[(-kap if k==1 else kap) for _,i,k in hh for _,_,kap in [self.turns[w,i]]]
                assert all(a==-b for a,b in zip(dirs,dirs[1:]))
                if wn and dirs:assert dirs[0]==(-1 if wn>0 else 1), (self.f,self.root,w,c,p,hh,dirs,wn,self.orientation,self.turns)
        val=cs,qs,J,hits;self.cache[p]=val;return val
    def sign(self,o):
        p,M=o
        return (-1)**(self.data(p)[2]//2+sum(self.turns[w,i][2]>0 for w,i in M))
    def run(self,*a,**kw):
        # The base moment calculation uses coordinates; replace its direction test
        # by a dictionary giving exactly the combinatorial token direction.
        return run_checked(self)

def run_checked(b):
    if not b.pairs:return dict(states=len(b.states),pairs=0)
    m=min(len(b.data(p)[0]) for p in b.pairs);objs=list(b.objects(m));U=set(objs);fixed=[];total=0
    for o in objs:
        for fn in (b.one,b.two):
            q=fn(o);assert q in U and fn(q)==o
            assert q==o or b.sign(q)==-b.sign(o)
        assert (b.one(o)==o)==(not b.data(o[0])[1])
        if b.two(o)==o:fixed.append(o);assert b.sign(o)==(-1)**(m//2)
        total+=b.sign(o)
    covers={};mom=[0]*(m+1)
    for p in b.pairs:
        cs,qs,J,h=b.data(p)
        assert J%2==len(cs)%2==b.n%2
        eps=(-1)**((b.n+J)//2)
        assert eps==(-1)**((b.n+1)//2)*(-1)**(J//2)
        # Li's opposite orientation and crossing convention gives the same sign.
        for pp,M in (o for o in objs if o[0]==p):
            d=sum(b.turns[w,i][2]>0 for w,i in M) if isinstance(b,Paths) else sum(int(bool(b.pos[p[1][i]][0]<b.cen[b.a[i]][0])) for w,i in M)
            assert (-1)**((-J)//2+m-d)==b.sign((p,M))
        H=lambda pp:sum(( -b.turns[w,i][2] if isinstance(b,Paths) else (1 if b.pos[pp[1][i]][0]>b.cen[b.a[i]][0] else -1)) for c in b.data(pp)[0] for w in b.w for _,i,k in b.data(pp)[3][c,w] if k==1)
        height=H(p)
        for j in range(m+1):mom[j]+=eps*height**j
        for c in cs:
            q=b.swap(p,c);diff=b.data(q)[2]-J;assert abs(diff)==2
            area=sum(len(h[c,w])%2 for w in b.w)
            assert H(q)-height==diff//2*area
        for c in qs:
            q=b.swap(p,c,False);assert abs(b.data(q)[2]-J)==2
        if len(cs)==m:
            key=tuple(sorted(tuple(sorted((b.a[i],min(p[0][i],p[1][i]),max(p[0][i],p[1][i])) for i in c)) for c in cs))
            covers[key]=math.prod(sum(len(h[c,w])%2 for w in b.w) for c in cs)
    F=sum(covers.values());assert F==len(fixed)>0
    assert total==(-1)**(m//2)*F
    assert mom[:m]==[0]*m and mom[m]==math.factorial(m)*(-1)**((b.n+m)//2)*F
    walks=[]
    for start in fixed:
        o=start;seen=set();steps=0
        while b.one(o)!=o:
            assert o not in seen;seen.add(o);o=b.one(o);assert o not in seen;seen.add(o)
            q=b.two(o);assert q!=o;o=q;steps+=2
        walks.append(steps)
    extra={k:sum(b.sign(o) for o in b.objects(k)) for k in (m-1,m+1)}
    assert extra[m-1]==0
    return dict(states=len(b.states),pairs=len(b.pairs),m=m,objects=len(objs),F=F,signed=total,moment=mom[m]//math.factorial(m),walk_hist=dict(Counter(walks)),other_k=extra)

if __name__=='__main__':
    vmax=int(sys.argv[1]);levels=enumerate_classes(vmax,True);rows=[];start=time.monotonic()
    for v,codes in levels.items():
        for cls,code in enumerate(codes):
            T=from_code(code)
            for root in range(T.F):
                results=[]
                for mode in ('ray','tree','reverse-tree'):
                    b=Check(T.faces,root) if mode=='ray' else Paths(T.faces,root,mode=='reverse-tree')
                    r=run_checked(b);rows.append(dict(v=v,cls=cls,root=root,mode=mode,**r));results.append(r)
                if results[0]['pairs']:
                    assert len({(r['F'],r['signed'],r['moment']) for r in results})==1
        print(v,len(rows),round(time.monotonic()-start,1),flush=True)
        (OUT/'verification.json').write_text(json.dumps(dict(command='python research/2026-11-14_sol_involutions-revision/code/check.py '+str(vmax),classes={v:len(c) for v,c in levels.items()},rows=rows),indent=1))



