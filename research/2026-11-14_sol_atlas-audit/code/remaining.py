from extra import *
# Width four tube from ring graph definition, independent enumeration.
rows=[]
for layers in range(4):
 g=nx.Graph();p=4
 for h in range(layers+1):
  g.add_edges_from((4*h+i,4*h+(i+1)%4) for i in range(4))
 for h in range(layers):
  g.add_edges_from((4*h+i,4*(h+1)+i) for i in range(4));g.add_edges_from([(4*h,4*(h+1)+1),(4*h+2,4*(h+1)+1),(4*h+2,4*(h+1)+3),(4*h,4*(h+1)+3)])
 top=4*(layers+1);bot=top+1;g.add_edges_from((top,i) for i in range(4));g.add_edges_from((bot,4*layers+i) for i in range(4));_,em=nx.check_planarity(g);fs,_=faces_of(em);root={top,0,1} if not layers else {0,1,5};idx=next(i for i,f in enumerate(fs) if set(f)==root);ff,vv,ee,t,l,gg,bb,aa,xx,ww=setup(fs,idx);ss=enum(ff,aa,xx);gn=sum(nx.is_forest(qgraph(z,ff,aa,vv)) and all(len(set(cc)&root)==1 for cc in nx.connected_components(qgraph(z,ff,aa,vv))) for z in ss);rows.append([layers,len(vv),len(ss),gn]);ck('tube layer '+str(layers),[len(ss),gn],[[2,2],[5,2],[13,2],[34,2]][layers])
# Reconstruct the 26-vertex two-cut obstruction without the atlas code.
g=nx.Graph();term=['top','bottom'];g.add_nodes_from(term)
for k in range(3):
 cube=nx.cubical_graph();u,v=next(iter(cube.edges()));cube.remove_edge(u,v);mp={x:(k,x) for x in cube};g.add_edges_from((mp[a],mp[b]) for a,b in cube.edges());g.add_edge('top',mp[u]);g.add_edge('bottom',mp[v])
h=g.copy();h.remove_nodes_from(term);ck('26 obstruction',[len(g),set(dict(g.degree()).values())=={3},nx.is_bipartite(g),nx.check_planarity(g)[0],nx.number_connected_components(h)],[26,True,True,True,3])
# Nonbijective disk fixture.
nb=json.loads((R/'research/2026-11-14_astra_limits/examples/nonbijective_disk.json').read_text());ff,vv,ee,t,l,gg,bb,aa,xx,ww=setup(nb['faces'],nb['outer']);cy=nb['cycle'];ds=sum(1 if l[a,b] in bb else -1 for a,b in zip(cy,cy[1:]+cy[:1]));cnt=Counter(nb['assignment'].values());ck('nonbijective delta',ds,0);ck('nonbijective repeats',sorted(cnt.values()),[1,1,1,1,2])
# Torus nine-vertex Q explicitly contains three diagonal 3-cycles.
q=nx.Graph();q.add_edges_from(((a,b),((a+1)%3,(b+1)%3)) for a in range(3) for b in range(3));ck('torus Q',[len(q),q.number_of_edges(),len(nx.cycle_basis(q))],[9,9,3])
(O/'remaining.json').write_text(json.dumps(dict(checks=checks,tubes=rows),indent=2,default=str));print('checks',len(checks),'failed',sum(not c['ok'] for c in checks))
