from explore import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
p=Path(__file__).resolve().parents[1]
I=family(4);u=next(covers(I));D=nx.Graph()
for t,v in zip(I.A,u):D.add_edge(*(set(I.faces[t])-{v}))
S={I.dual_edges[tuple(sorted(e))] for e in D.edges()};rem=I.G.copy();rem.remove_edges_from(S)
fig,axs=plt.subplots(1,2,figsize=(13,6));colors=['#bc4529','#267780','#72549b','#b58b28']
# Tutte coordinates with chosen roots on the outer triangle.
rs=sorted(I.R);pos={rs[0]:np.array([0.,1.]),rs[1]:np.array([-1.,-0.7]),rs[2]:np.array([1.,-0.7])};X=I.X;ix={v:i for i,v in enumerate(X)}
M=np.zeros((len(X),len(X)));rhs=np.zeros((len(X),2))
for v in X:
 M[ix[v],ix[v]]=I.T.degree(v)
 for w in I.T[v]:
  if w in ix:M[ix[v],ix[w]]-=1
  else:rhs[ix[v]]+=pos[w]
sol=np.linalg.solve(M,rhs);pos.update({v:sol[ix[v]] for v in X})
nx.draw_networkx_edges(I.T,pos,ax=axs[0],edge_color='#bfc4ca',width=.8)
for j,vs in enumerate(nx.connected_components(D)):nx.draw_networkx_edges(D.subgraph(vs),pos,ax=axs[0],edge_color=colors[j],width=3)
labels={0:'A',1:'B'}
for i in range(4):labels.update({2+3*i:f'x{i}',3+3*i:f'y{i}',4+3*i:f'z{i}'})
nx.draw_networkx_nodes(I.T,pos,ax=axs[0],node_size=100,node_color=['#222222' if v in I.R else 'white' for v in I.T],edgecolors='#222222')
nx.draw_networkx_labels(I.T,pos,labels,font_size=8,ax=axs[0],font_color='#222222',bbox={'facecolor':'white','alpha':.8,'edgecolor':'none','pad':.3})
axs[0].set_title('Dual: unique cover, two triangles and a pentagon')
posg=nx.planar_layout(I.G)
for j,vs in enumerate(nx.connected_components(rem)):
 nx.draw_networkx_edges(rem.subgraph(vs),posg,ax=axs[1],edge_color=colors[j],width=2)
 nx.draw_networkx_nodes(I.G,posg,nodelist=list(vs),node_color=colors[j],node_size=65,ax=axs[1])
nx.draw_networkx_edges(I.G,posg,edgelist=list(S),ax=axs[1],edge_color='#777777',style='dashed',width=1)
nx.draw_networkx_nodes(I.G,posg,nodelist=[I.outer],node_color='black',node_size=120,node_shape='s',ax=axs[1])
axs[1].set_title('Primal: delete dashed S, leaving four components')
for ax in axs:ax.set_axis_off()
fig.tight_layout();fig.savefig(p/'data/dictionary.png',dpi=180);fig.savefig(p/'data/dictionary.svg');plt.close(fig)
rows=json.loads((p/'data/census.json').read_text());pts=[]
for row in rows:
 cs=[int(s.split(':')[0].split('=')[1]) for s in row['summary'] if s.startswith('cmin=')]
 if cs:pts.append((row['V'],max(cs)))
fig,ax=plt.subplots(figsize=(7,3));ax.plot(*zip(*pts),marker='o',color=colors[1]);ax.set(xlabel='Dual vertices',ylabel='Maximum c_min',xticks=list(range(6,25,2)),yticks=range(1,7));ax.grid(alpha=.2);fig.tight_layout();fig.savefig(p/'data/census.png',dpi=150)
html='''<!doctype html><meta charset="utf-8"><style>body{font:14px var(--font-sans);color:var(--foreground)}img{width:100%;height:auto}p{line-height:1.5}</style><p>For the 14-vertex family member, c = 3 counts the extra components after the selected primal edges are deleted.</p>'''
html+=f'<img src="{p / "data/dictionary.png"}" alt="Dual cover and primal deletion"><p>Exhaustive 4-connected census, all facial roots, through dual order 24. Computational results await independent review.</p><img src="{p / "data/census.png"}" alt="Maximum minimum cycle count by size">'
(p/'data/visual.html').write_text(html)
