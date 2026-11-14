from model import *
import random
random.seed(9)
for trial in range(100):
 T=nx.octahedral_graph()
 for step in range(2+trial//25):
  _,em=nx.check_planarity(T);w=random.choice(list(T));ns=list(em.neighbors_cw_order(w));j=random.choice(list(range(2,len(ns)-1,2))); a,b=max(T)+1,max(T)+2
  T.remove_edges_from((w,v) for v in ns[j+1:]);T.add_edges_from((a,v) for v in ns[j:]+ns[:1]);T.add_edges_from((b,v) for v in [w,a,ns[0],ns[j]])
 tf=faces(T);G=nx.Graph();G.add_nodes_from(range(len(tf)))
 for i,j in it.combinations(G,2):
  if len(set(tf[i])&set(tf[j]))==2:G.add_edge(i,j)
 m=model(G)
 if m[9]:
  nx.write_adjlist(G,OUT/'running-primal.adjlist');break
