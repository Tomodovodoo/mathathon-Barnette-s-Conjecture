from campaign import *
def dual_multi(g):
 _,emb=nx.check_planarity(g);fs,side=faces_of(emb);d=nx.MultiGraph();d.add_nodes_from(range(len(fs)))
 for u,v in g.edges():d.add_edge(side[u,v],side[v,u],primal=[u,v])
 corners={v:sorted({side[v,w] for w in g[v]}) for v in g}
 return d,fs,corners

def special():
 g=nx.Graph();g.add_nodes_from(range(26))
 cube=nx.cubical_graph();a,b=next(iter(cube.edges()));cube.remove_edge(a,b)
 for i in range(3):
  mp={v:2+8*i+v for v in cube};g.add_edges_from((mp[u],mp[v]) for u,v in cube.edges());g.add_edges_from([(0,mp[a]),(1,mp[b])])
 assert nx.is_bipartite(g) and nx.check_planarity(g)[0] and nx.node_connectivity(g)==2
 assert all(d==3 for _,d in g.degree()) and len(list(nx.connected_components(g.subgraph(set(g)-{0,1}))))==3
 d,fs,corners=dual_multi(g);col=nx.bipartite.color(g);rs=[]
 for root in g:
  black=[v for v in g if col[v]==col[root]];A=sorted(set(black)-{root});X=sorted(set(d)-set(corners[root]));B=nx.Graph()
  B.add_nodes_from(('t',t) for t in A);B.add_nodes_from(('v',v) for v in X)
  B.add_edges_from((('t',t),('v',v)) for t in A for v in corners[t] if v in X)
  fake=Instance.__new__(Instance);fake.A=A;fake.X=X;fake.n=len(A);fake.faces=corners
  ss=list(fake.states());ps=fake.pairs(ss)
  rs.append({'root':root,'states':len(ss),'pairs':len(ps)})
 save('examples/theta_cube_26.json',{'edges':sorted(map(list,g.edges())),'dual_multiedges':list(d.edges()),'dual_faces':fs,'dual_triangles':corners,'cut_vertices':[0,1]})
 save('data/non3connected.json',{'roots':rs,'parallel_edge_classes':[[u,v,d.number_of_edges(u,v)] for u,v in nx.Graph(d).edges() if d.number_of_edges(u,v)>1]})
 # Toroidal triangular grid: oriented faces in periodic coordinate chart.
 idx=lambda x,y:3*(x%3)+(y%3)
 black=[];white=[]
 for x in range(3):
  for y in range(3):
   black.append([idx(x,y),idx(x+1,y),idx(x+1,y+1)])
   white.append([idx(x,y),idx(x+1,y+1),idx(x,y+1)])
 t=nx.Graph();t.add_edges_from(edge(a,b) for f in black+white for a,b in zip(f,f[1:]+f[:1]))
 counts=collections.Counter(edge(a,b) for f in black+white for a,b in zip(f,f[1:]+f[:1]));assert set(counts.values())=={2}
 tg=nx.Graph();tg.add_nodes_from(range(18))
 for i,f in enumerate(black+white):
  for j,h in enumerate(black+white):
   if i<j and len(set(f)&set(h))==2:tg.add_edge(i,j)
 partitions=[]
 for bits in range(1,1<<8):
  u={i+1 for i in range(8) if bits>>i&1};v=set(t)-u
  if nx.is_tree(t.subgraph(u)) and nx.is_tree(t.subgraph(v)):partitions.append(sorted(u))
 assert all(d==6 for _,d in t.degree()) and nx.is_bipartite(tg)
 save('examples/torus_3x3.json',{'edges':list(t.edges()),'black_faces':black,'white_faces':white,'primal_edges':list(tg.edges()),'two_induced_tree_partitions':partitions,'hamiltonian_cycles':len(cycles(tg))})
 # Relax bijectivity, keep one outgoing edge per bounded black face and no root tails.
 witness=None
 for n in range(6,13):
  for t in plantri_graphs(n,ROOT/'workings/barnette_lab/vendor/plantri.exe'):
   for outer in range(2*len(t)-4):
    b=Instance(t,outer)
    for c in nx.simple_cycles(b.T.subgraph(b.X).to_directed()):
     if len(c)<3:continue
     es=list(zip(c,c[1:]+c[:1]));ts=[next(f for f in (b.sides[a,z],b.sides[z,a]) if f in b.black) for a,z in es]
     if len(set(ts))<len(ts):continue
     delta=sum(b.delta(a,z) for a,z in es)
     if abs(delta)==3:continue
     assignment={f:a for f,(a,z) in zip(ts,es)}
     for f in b.A:
      if f not in assignment:assignment[f]=next(iter(set(b.faces[f])&set(b.X)))
     witness={'dual_edges':list(t.edges()),'faces':b.faces,'outer':outer,'black':b.black,'A':b.A,'X':b.X,'assignment':assignment,'cycle':c,'delta_sum':delta}
     break
    if witness:break
   if witness:break
  if witness:break
 save('examples/nonbijective_disk.json',witness)
 for name,g in [('K4',nx.complete_graph(4)),('Tutte46',nx.tutte_graph())]:
  d,fs,corners=dual_multi(g)
  save(f'examples/{name}.json',{'edges':list(g.edges()),'dual_edges':list(d.edges()),'dual_faces':fs,'odd_dual_vertices':[v for v,k in d.degree() if k%2]})
 event('Special examples constructed: theta26, torus9, nonbijective disk, K4 and Tutte46')
 print('theta roots',rs);print('disk',witness);print('torus two trees',len(partitions))
if __name__=='__main__':special()
