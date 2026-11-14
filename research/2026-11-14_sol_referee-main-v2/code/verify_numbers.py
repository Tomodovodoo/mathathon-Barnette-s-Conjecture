"""Independent finite referee engine. Reads face fixtures, imports no project code."""
from pathlib import Path
from itertools import combinations
from collections import deque, Counter, defaultdict
import json, math
import networkx as nx
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).parent/'outputs'
def edge(a,b): return tuple(sorted((a,b)))
def comps(v,e):
    g=nx.Graph(); g.add_nodes_from(v); g.add_edges_from(e)
    return sorted([sorted(c) for c in nx.connected_components(g)])
class Audit:
    def __init__(self,faces,t0,e0):
        self.f=[tuple(x) for x in faces]; self.t0=t0; self.e0=edge(*e0)
        self.left={(a,b):i for i,f in enumerate(self.f) for a,b in zip(f,f[1:]+f[:1])}
        self.edges=sorted({edge(*a) for a in self.left})
        self.v=sorted({x for f in faces for x in f}); self.roots=set(self.f[t0]); self.x=set(self.v)-self.roots
        self.g=nx.Graph(); self.g.add_nodes_from(range(len(faces)))
        self.dual={}
        for a,b in self.edges:
            de=edge(self.left[a,b],self.left[b,a]);self.g.add_edge(*de); self.dual[a,b]=de
        color=nx.bipartite.color(self.g)
        self.black=[i for i in self.g if color[i]==color[t0]]
        self.white=[i for i in self.g if color[i]!=color[t0]]
        self.a=[i for i in self.black if i!=t0]
        self.states=[]
        def rec(s,used):
            if len(s)==len(self.a):self.states.append(tuple(s));return
            for v in sorted(set(self.f[self.a[len(s)]]) & (self.x-used)):rec(s+[v],used|{v})
        rec([],set())
        self.pairs=[(r,s) for r in self.states for s in self.states if all(x!=y for x,y in zip(r,s))]
        self.good=[s for s in self.states if self.isgood(s)]
        self.kappa={}
        self.paths={}
        for w in self.white:
            queue=deque([[w]]); seen={w}
            while queue:
                p=queue.popleft()
                if p[-1]==t0:break
                for y in sorted(self.g[p[-1]]):
                    if y not in seen:seen.add(y);queue.append(p+[y])
            self.paths[w]=p
            for j,t in enumerate(p[1:-1],1):
                if t not in self.a:continue
                enter=set(self.f[t]) & set(self.f[p[j-1]])
                leave=set(self.f[t]) & set(self.f[p[j+1]])
                turn=next(iter(enter&leave)); aa=next(iter(enter-{turn}));bb=next(iter(leave-{turn}))
                cyc=self.f[t]; sign=1 if cyc[(cyc.index(turn)+1)%3]==aa else -1
                self.kappa[w,t,turn]=sign
    def q(self,s):return [tuple(sorted(set(self.f[t])-{v})) for t,v in zip(self.a,s)]
    def isgood(self,s):
        cc=comps(self.v,self.q(s))
        return len(cc)==3 and all(len(set(c)&self.roots)==1 for c in cc)
    def weight(self,s,w=None):
        return sum(self.kappa.get((y,t,v),0) for y in ([w] if w is not None else self.white) for t,v in zip(self.a,s))
    def sign(self,r,s):return math.prod(1 if self.left[a,b] in self.black else -1 for a,b in zip(r,s))
    def cycles(self,r,s):
        nxt=dict(zip(r,s)); todo=set(self.x);out=[]
        while todo:
            start=min(todo);cyc=[start]; cur=nxt[start]
            while cur!=start:cyc.append(cur);cur=nxt[cur]
            todo-=set(cyc);out.append(cyc)
        return out
    def disk(self,c):
        ee=[(a,b) for a,b in zip(c,c[1:]+c[:1])]
        cut={self.dual[edge(*e)] for e in ee}
        h=self.g.copy();h.remove_edges_from(cut)
        inside=set(self.g)-nx.node_connected_component(h,self.t0)
        verts=set().union(*(set(self.f[i]) for i in inside))-set(c)
        inneredges=[list(edge(a,b)) for a,b in ee if next(t for t in self.black if {a,b}<=set(self.f[t])) in inside]
        ccw=self.left[ee[0]] in inside
        return dict(cycle=c,h=len(c),B=len(inside&set(self.black)),W=len(inside&set(self.white)),I=len(verts),interior=sorted(verts),ell=len(inneredges),inner_black_edges=inneredges,ccw=ccw)
    def recover(self,s):
        excluded=set(self.q(s)) | {edge(a,b) for a,b in combinations(self.roots,2) if edge(a,b)!=self.e0}
        h=self.g.copy();h.remove_edges_from([self.dual[e] for e in excluded]);assert nx.is_tree(h)
        parent={self.t0:None}; order=[self.t0]
        for t in order:
            for y in sorted(h[t]):
                if y not in parent:parent[y]=t;order.append(y)
        selected=[]
        for t in self.black:
            child=[y for y in h[t] if parent[y]==t];assert len(child)==1
            selected.append(next(e for e,de in self.dual.items() if de==edge(t,child[0])))
        assert all(sum(set(e)<=set(f) for e in selected)==1 for f in self.f)
        assert len(comps(self.v,selected))==2
        return dict(edges=sorted(selected),components=comps(self.v,selected))
    def matchings(self):
        def rec(todo,chosen):
            if not todo:yield chosen;return
            v=min(todo)
            for u in sorted(set(self.g[v]) & todo):yield from rec(todo-{u,v},chosen+[edge(u,v)])
        return list(rec(set(self.g),[]))
    def run(self):
        matchings=self.matchings();ham=[]
        for pm in matchings:
            h=self.g.copy();h.remove_edges_from(pm)
            if nx.is_connected(h):ham.append(pm)
        avoid={str(e):sum(self.dual[e] in pm for pm in ham) for e in combinations(sorted(self.roots),2)}
        recs={str(s):self.recover(s) for s in self.good}
        pairrows=[];groups=defaultdict(list)
        for r,s in self.pairs:
            disks=[self.disk(c) for c in self.cycles(r,s)]
            disks.sort(key=lambda d:-d['h'])
            for d in disks:
                assert d['W']==d['B']+1 and d['h']==2*d['ell']+3
                assert d['B']==d['I']+d['ell']
            row=dict(r=r,s=s,eps=self.sign(r,s),omega=self.weight(s),good=s in self.good,disks=disks)
            pairrows.append(row);groups[tuple(sorted(edge(a,b) for a,b in zip(r,s)))].append(row)
        m=min((len(self.cycles(r,s)) for r,s in self.pairs),default=None)
        moments=[sum(row['eps']*row['omega']**j for row in pairrows) for j in range((m or 0)+1)]
        # Exact Laurent expansion coefficient, valid at negative exponents.
        laurent=Counter()
        for row in pairrows:laurent[row['omega']]+=row['eps']
        coeff=sum(c*math.prod(w-j for j in range(m))//math.factorial(m) for w,c in laurent.items()) if m else None
        assert m is None or coeff==moments[m]//math.factorial(m)
        hall=[sum(min(2,len(set(self.f[t])&set(ss))) for t in self.a)-2*len(ss) for k in range(len(self.x)+1) for ss in combinations(sorted(self.x),k)]
        tri=[c for c in combinations(self.v,3) if all(edge(a,b) in self.edges for a,b in combinations(c,2))]
        return dict(vertices=len(self.v),edges=len(self.edges),faces=len(self.f),black=len(self.black),white=len(self.white),n=len(self.a),separators=[c for c in tri if set(c) not in [set(f) for f in self.f]],states=self.states,good_states=self.good,pairs=pairrows,groups=list(groups.values()),m=m,moments=moments,Laurent={w:c for w,c in laurent.items() if c},Laurent_coefficient=coeff,perfect_matchings=len(matchings),Hamiltonian_cycles=len(ham),avoid=avoid,recoveries=recs,shortest_paths=self.paths,minimum_Hall_slack=min(hall),G_connectivity=nx.node_connectivity(self.g))
def main():
    out={}
    for name in ['octahedron','running']:
        d=json.loads((ROOT/f'paper/figures/{name}.json').read_text())
        obj=Audit(d['faces'],d['t0'],d['e0']);out[name]=obj.run()
        if name=='running':
            alpha=(1,3,7,2,9,11,6,12,8,10);beta=(6,2,8,1,3,10,11,7,12,9)
            out[name]['named']=dict(alpha_Q=comps(obj.v,obj.q(alpha)),beta_Q=comps(obj.v,obj.q(beta)),beta_P=obj.recover(beta),alpha_weight=obj.weight(alpha),beta_weight=obj.weight(beta))
            y=next(i for i,f in enumerate(obj.f) if set(f)=={1,8,9})
            out[name]['named']['height_alpha_at_189']=obj.weight(alpha,y)
            # Reverse only the long D cycle, keeping the short cycle fixed.
            r=list(beta);s=list(alpha)
            cyc=max(obj.cycles(beta,alpha),key=len)
            for i,v in enumerate(beta):
                if v in cyc:r[i],s[i]=s[i],r[i]
            out[name]['named']['height_before_at_189']=obj.weight(s,y)
    # Six-gon bipyramid, oriented combinatorially; its dual is the hexagonal prism.
    faces=[]
    for i in range(6):faces.extend([(6,i,(i+1)%6),(7,(i+1)%6,i)])
    out['hexagonal_prism']=Audit(faces,0,(0,1)).run()
    (OUT/'numbers.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:{x:v[x] for x in ['vertices','edges','faces','n','m','moments','Hamiltonian_cycles','avoid']}|{'states':len(v['states']),'good':len(v['good_states']),'pairs':len(v['pairs'])} for k,v in out.items()},indent=2))
if __name__=='__main__':main()
