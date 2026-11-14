"""Independent audit. Reads fixtures/certificates, never imports atlas logic."""
from pathlib import Path
import itertools as it,json,math
from collections import Counter,defaultdict
import networkx as nx
import sympy as sp
R=Path(__file__).resolve().parents[3]; O=Path(__file__).resolve().parents[1]/'outputs'
C=json.loads((O/'snapshot-computed.json').read_text()); out={}; checks=[]
def ck(name,a,b):
 checks.append(dict(test=name,actual=a,expected=b,ok=a==b))
 if a!=b: print('MISMATCH',name,a,b)
def setup(fs,t0):
 F=list(map(tuple,fs)); V=sorted(set(sum((list(f) for f in F),[]))); E={tuple(sorted(e)) for f in F for e in zip(f,f[1:]+f[:1])}; T=nx.Graph(list(E)); left={(a,b):i for i,f in enumerate(F) for a,b in zip(f,f[1:]+f[:1])}; G=nx.Graph([(left[a,b],left[b,a]) for a,b in E]); col=nx.bipartite.color(G); B=[i for i in range(len(F)) if col[i]==col[t0]]; A=[i for i in B if i!=t0]; X=sorted(set(V)-set(F[t0])); W=sorted(set(range(len(F)))-set(B))
 return F,V,E,T,left,G,B,A,X,W
j=json.loads((R/'digestions/atlas/toolkit/running.json').read_text()); F,V,E,T,left,G,B,A,X,W=setup(j['faces'],j['t0']); roots=set(F[j['t0']])
def enum(F,A,X):
 st=[]
 def go(i,z,used):
  if i==len(A): st.append(tuple(z)); return
  for v in F[A[i]]:
   if v in X and v not in used: go(i+1,z+[v],used|{v})
 go(0,[],set()); return st
S=enum(F,A,X); P=[(r,s) for r in S for s in S if all(a!=b for a,b in zip(r,s))]
def qgraph(z,F=F,A=A,V=V):
 q=nx.Graph();q.add_nodes_from(V);q.add_edges_from(tuple(u for u in F[t] if u!=v) for t,v in zip(A,z));return q
def good(z):
 q=qgraph(z);return nx.is_forest(q) and all(len(set(c)&roots)==1 for c in nx.connected_components(q))
def delta(a,b):return 1 if left[a,b] in B else -1
ck('states',sorted(map(list,S)),sorted(C['running']['states'])); ck('pairs',len(P),8); ck('good states',sum(map(good,S)),6)
# Enumerate all induced-tree partitions independently, without primal cycle enumeration.
parts=[]
for bits in range(1,1<<(len(V)-1)):
 U={V[i] for i in range(len(V)-1) if bits>>i&1}; Z=set(V)-U
 if nx.is_tree(T.subgraph(U)) and nx.is_tree(T.subgraph(Z)):parts.append((U,Z))
ck('Hamiltonian cycles via two induced trees',len(parts),28)
col=nx.greedy_color(T,strategy='DSATUR');per=[sum(any(not any(col[a]!=c and col[b]!=c for a,b in T.subgraph(U).edges()) for U in ps) for ps in parts) for c in range(3)]
ck('FS relaxed predicate',per,[28]*3)
# Hall all subsets.
margin=[]
for mask in range(1<<len(X)):
 U={v for i,v in enumerate(X) if mask>>i&1};margin.append(sum(min(2,len(U&set(F[t]))) for t in A)-2*len(U))
ck('Hall failures over 1024 sets',sum(v<0 for v in margin),0)
# Exact height potential independently reconstructed from oriented white boundaries.
spokes=[(t,v) for t in A for v in F[t]]; inner=[w for w in W if all(next(t for t in B if {a,b}<=set(F[t]))!=j['t0'] for a,b in zip(F[w],F[w][1:]+F[w][:1]))]; M=sp.zeros(len(spokes),len(inner))
for k,w in enumerate(inner):
 for a,b in zip(F[w],F[w][1:]+F[w][:1]):
  t=next(t for t in B if {a,b}<=set(F[t]));M[spokes.index((t,b)),k]+=1;M[spokes.index((t,a)),k]-=1
vec=lambda z:sp.Matrix([int(z[A.index(t)]==v) for t,v in spokes]); hs=[list(M.gauss_jordan_solve(vec(z)-vec(S[0]))[0]) for z in S]; minima=[min(h[k] for h in hs) for k in range(len(inner))]; hs=[[int(x-y) for x,y in zip(h,minima)] for h in hs]; vol=[sum(h) for h in hs]
ck('height vectors',[hs[S.index(tuple(z))] for z in C['running']['states']],C['running']['heights']); names={z:i for i,z in enumerate(sorted(S,key=lambda z:(vol[S.index(z)],C['running']['states'].index(list(z)))))}
x=sp.Symbol('x'); terms=[]; Z=0;poly=0; aa=M*(M.T*M).inv()*sp.ones(len(inner),1)
for r,s in P:
 D=nx.DiGraph(zip(r,s));J=sum(delta(a,b) for a,b in zip(r,s))//3;sg=int((sp.I**J)); ep=math.prod(delta(a,b) for a,b in zip(r,s));v=vol[S.index(s)];Z+=sg*sp.exp(x*v);poly+=ep*sp.prod(1+x*aa[spokes.index((t,vv))] for t,vv in zip(A,s));terms.append([names[r],names[s],J,sg,ep,v])
ck('exponential leading coefficient',int(sp.expand(sp.series(Z,x,0,3).removeO()).coeff(x,2)),C['running']['leading_coefficient']);ck('linear coefficient',str(sp.expand(poly).coeff(x,2)),'9')
# Signed partner matrices, all states.
dets={}
for s in S:
 N=sp.Matrix([[delta(u,v) if u!=v and u in F[t] else 0 for u in X] for t,v in zip(A,s)]);dets[names[s]]=int(N.det());ck(f'partner determinant magnitude s{names[s]}',abs(int(N.det())),int(good(s)))
# forest counts with one face or one vertex incidence, roots contracted.
def independent(es):
 uf=nx.utils.UnionFind()
 for a,b in es:
  a=0 if a in roots else a+1;b=0 if b in roots else b+1
  if uf[a]==uf[b]:return False
  uf.union(a,b)
 return True
ff=sum(independent([tuple(u for u in F[t] if u!=v) for t,v in zip(A,z)]) for z in it.product(*[[v for v in F[t] if v in X] for t in A]))
vf=sum(independent([tuple(u for u in F[t] if u!=v) for v,t in zip(X,z)]) for z in it.product(*[[t for t in A if v in F[t]] for v in X]))
ck('face plus forest',ff,350);ck('vertex plus forest',vf,304)
# Every LP inequality and exact vertex rank.
cs=[tuple(e) for e in C['lp']['choices']]; xv=sp.Matrix(list(map(sp.Rational,C['lp']['x']))); eq=[[int(t==tt) for tt,v in cs] for t in A]+[[int(v==vv) for t,vv in cs] for v in X];active=list(eq);ni=0
for mask in range(1,1<<(len(X)+1)):
 ids={i for i in range(len(X)+1) if mask>>i&1}
 if len(ids)<2:continue
 row=[]
 for t,v in cs:
  ends=[0 if u in roots else X.index(u)+1 for u in F[t] if u!=v]; row.append(int(all(u in ids for u in ends)))
 if not any(row):continue
 ni+=1; val=(sp.Matrix([row])*xv)[0];assert val<=len(ids)-1
 if val==len(ids)-1:active.append(row)
for i,a in enumerate(xv):
 if a in (0,1):active.append([int(k==i) for k in range(len(cs))])
ck('LP inequalities',ni,1946);ck('LP active rank',sp.Matrix(active).rank(),len(cs));ck('LP equalities',list(sp.Matrix(eq)*xv),[1]*(2*len(A)))
# Full spoke tree count.
H=nx.Graph([(('t',t),('v',v)) for t in B for v in F[t]]); L=nx.laplacian_matrix(H).toarray();tau=int(sp.Matrix(L[:-1,:-1]).det());ck('spoke spanning trees',tau,6670188)
cut=C['cuts']['four_cycle']; pats=Counter(tuple(int(v not in ps[0]) for v in cut) if cut[0] in ps[0] else tuple(int(v in ps[0]) for v in cut) for ps in parts);ck('4-cut frequencies',dict((str(k),v) for k,v in pats.items()),C['cuts']['four_patterns'])
# Prism and extreme-state fixtures independently enumerated.
for key in ['canonical','determinant']:
 c=C[key] if key=='canonical' else C[key]['prism'];f,v,e,t,l,g,b,a,xx,w=setup(c['faces'],c['t0']);ss=enum(f,a,xx);pp=[(r,s) for r in ss for s in ss if all(u!=v for u,v in zip(r,s))];rr=set(f[c['t0']]);gs=[z for z in ss if nx.is_forest(qgraph(z,f,a,v)) and all(len(set(cc)&rr)==1 for cc in nx.connected_components(qgraph(z,f,a,v)))];ck(key+' state count',len(ss),9 if key=='canonical' else 3);ck(key+' good count',len(gs),8 if key=='canonical' else 2)
# Each avoidance count from partitions, independent of atlas two-factor enumerator.
av={str(e):sum((e[0] in U)==(e[1] in U) for U,Z in parts) for e in E};ck('avoidance range',[min(av.values()),max(av.values())],[4,14])
out=dict(checks=checks,terms=terms,determinants=dets,cut_patterns=str(pats),avoidance=av,scope='Running example, canonical fixture, hexagonal prism. No atlas imports. Not a full verification of all extra fixtures.');(O/'independent.json').write_text(json.dumps(out,indent=2,default=str));print('checks',len(checks),'failed',sum(not c['ok'] for c in checks))

