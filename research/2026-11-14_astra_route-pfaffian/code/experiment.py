"""Exact finite experiments. Run from repository root; output lives beside code/."""
import networkx as nx, itertools as it, json, pathlib, time, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
def edge(u,v): return tuple(sorted((u,v)))
def squares(g):
 return sorted({min(tuple(p[i:]+p[:i]) for p in (list(c),list(reversed(c))) for i in range(4)) for c in nx.simple_cycles(g,length_bound=4) if len(c)==4})
def trisum(gs,cs):
 h=nx.Graph(); nxt=4
 for g,c in zip(gs,cs):
  mp={v:i for i,v in enumerate(c)}
  for v in sorted(set(g)-set(c)): mp[v]=nxt; nxt+=1
  h.add_edges_from((mp[u],mp[v]) for u,v in g.edges if not (u in c and v in c))
 return h

def matchings(g):
 col=nx.bipartite.color(g); a=sorted(v for v in g if col[v]); b=sorted(set(g)-set(a)); out=[]
 def rec(i,used,ls):
  if i==len(a): out.append(tuple(ls)); return
  for v in sorted(g[a[i]]):
   if v not in used: rec(i+1,used|{v},ls+[v])
 rec(0,set(),[])
 return a,b,out

def parity(p,b):
 q=[b.index(v) for v in p]; return sum(q[i]>q[j] for i in range(len(q)) for j in range(i+1,len(q)))%2

def sign_solution(g,a,b,ms):
 es=sorted(edge(u,v) for u,v in g.edges); ix={e:i for i,e in enumerate(es)}; basis={}
 for m in ms:
  x=sum(1<<ix[edge(u,v)] for u,v in zip(a,m)); rhs=parity(m,b)
  while x:
   k=x.bit_length()-1
   if k in basis: y,t=basis[k]; x^=y; rhs^=t
   else: basis[k]=(x,rhs); break
  if not x and rhs: return None
 sol=0
 for k,(x,rhs) in sorted(basis.items()):
  if ((x&sol).bit_count()%2)^rhs: sol|=1<<k
 assert all(parity(m,b)==sum((sol>>ix[edge(u,v)])&1 for u,v in zip(a,m))%2 for m in ms)
 return [list(e) for i,e in enumerate(es) if sol>>i&1]

def analyse(name,g):
 a,b,ms=matchings(g); hams=[]; hist={}; witness=None
 for m in ms:
  h=g.copy(); h.remove_edges_from(zip(a,m)); n=nx.number_connected_components(h); hist[n]=hist.get(n,0)+1
  if n==1: hams.append(set(edge(u,v) for u,v in h.edges))
  elif witness is None: witness={'matching':list(zip(a,m)),'cycles':[sorted(c) for c in nx.connected_components(h)]}
 paths=set()
 for p in it.permutations(g,2):
  u,v=p
  if not g.has_edge(u,v): continue
  for w in g[v]:
   if w==u: continue
   for x in g[w]:
    if x not in (u,v): paths.add(min((u,v,w,x),(x,w,v,u)))
 bad=[p for p in paths if not any(all(edge(u,v) in h for u,v in zip(p,p[1:])) for h in hams)]
 signs=sign_solution(g,a,b,ms)
 result=dict(name=name,n=len(g),edges=sorted(edge(u,v) for u,v in g.edges),cubic=set(dict(g.degree()).values())=={3},bipartite=nx.is_bipartite(g),connectivity=nx.node_connectivity(g),planar=nx.check_planarity(g)[0],matchings=len(ms),negative_signed_edges=signs,pfaffian=signs is not None,complement_components=hist,hamiltonian_cycles=len(hams),paths=len(paths),bad_paths=bad,disconnected_witness=witness)
 print(name, result['n'],len(ms),len(hams),len(paths),len(bad),flush=True)
 return result

def signature(g,c):
 a,b,ms=matchings(g); counts={}; witnesses={}
 for m in ms:
  h=g.copy(); h.remove_edges_from(zip(a,m))
  if not nx.is_connected(h): continue
  h.remove_edges_from(zip(c,c[1:]+c[:1]))
  paths=[]
  for comp in nx.connected_components(h):
   if len(comp)>1:
    ends=sorted(c.index(v) for v in comp if h.degree(v)==1); assert len(ends)==2
    paths.append(tuple(ends))
  key=str(sorted(paths)); counts[key]=counts.get(key,0)+1; witnesses[key]=sorted(edge(u,v) for u,v in h.edges)
 return counts

def torus(g):
 ns={v:sorted(g[v]) for v in g}
 for mask in range(1<<len(g)):
  rot={v:ns[v][::(-1 if mask>>v&1 else 1)] for v in g}; darts=set((u,v) for u,v in g.edges for u,v in ((u,v),(v,u))); fs=[]
  while darts:
   start=min(darts); d=start; f=[]
   while True:
    darts.remove(d); u,v=d; f.append(u); d=(v,rot[v][(rot[v].index(u)+1)%3])
    if d==start: break
   fs.append(f)
  if len(fs)==7 and all(len(f)==len(set(f))==6 for f in fs): break
 else: raise RuntimeError('no embedding')
 col=nx.bipartite.color(g); a=sorted(v for v in g if col[v]); corners={v:[i for i,f in enumerate(fs) if v in f] for v in a}
 states=[s for s in it.permutations(range(7)) if all(s[i] in corners[v] for i,v in enumerate(a))]; pairs=0; even=None; sums={}
 for r in states:
  for s in states:
   if any(x==y for x,y in zip(r,s)): continue
   pairs+=1; perm=dict(zip(r,s)); unseen=set(perm)
   while unseen:
    v=min(unseen); cyc=[]
    while v not in cyc: cyc.append(v); unseen.remove(v); v=perm[v]
    if len(cyc)%2==0 and even is None: even={'r':r,'s':s,'D_cycle':cyc}
 return dict(rotation=rot,faces=fs,black_vertices=a,corners=corners,rooted_cardinality=[6,4],rootfree_states=len(states),pairs=pairs,even_D_witness=even,Q_edges=7,Q_vertices=7)

def main():
 t=time.time(); cube=nx.cubical_graph(); prism=nx.circular_ladder_graph(6); c=squares(cube)[0]; p=squares(prism)[0]
 tri=trisum([cube]*3,[c]*3); nested=trisum([tri,cube,cube],[squares(tri)[0],c,c])
 graphs={'cube':cube,'hexagonal_prism':prism,'heawood':nx.heawood_graph(),'cube_trisum':tri,'cube_cube_prism':trisum([cube,cube,prism],[c,c,p]),'nested_trisum':nested,'K33_control':nx.complete_bipartite_graph(3,3)}
 result={'graphs':[analyse(n,g) for n,g in graphs.items()],'signatures':{n:signature(g,squares(g)[0]) for n,g in graphs.items() if squares(g)},'heawood_torus':torus(graphs['heawood']),'seconds':time.time()-t,'python':sys.version,'networkx':nx.__version__}
 (ROOT/'data/results.json').write_text(json.dumps(result,indent=2))
if __name__=='__main__': main()
