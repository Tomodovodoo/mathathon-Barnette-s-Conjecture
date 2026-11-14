from verify import ROOT,OUT,instance
import json,sys
from collections import Counter
import networkx as nx
import sympy as sp
D=json.loads((ROOT/'research/2026-11-14_fable_digestions/data/examples.json').read_text())
rows={}
for name,d in D.items():
 if 'info' not in d:continue
 b=instance(d['faces'],d['t0']);ss=list(b.states());ps=b.pairs(ss)
 actual={'states':len(ss),'pairs':len(ps),'tree_matchings':sum(b.is_tree(s) for s in ss),'partnered_states':len(set(s for r,s in ps))}
 for k,v in actual.items():assert v==d['info'][k],(name,k)
 covers={}
 for r,s in ps:
  key=tuple(sorted(tuple(sorted((r[i],s[i]))) for i in range(b.n)))
  covers.setdefault(key,[]).append((r,s))
 actual['cover_forest_counts']=sorted([len(b.dcycles(*ps0[0])),sum(b.is_tree(s) for r,s in ps0)] for ps0 in covers.values())
 assert sorted(x[0] for x in actual['cover_forest_counts'])==d['info']['covers_by_cycle_count']
 rows[name]=actual
# The two octahedra at all 14 facial roots.
f=D['double_octahedron']['faces'];hist=Counter()
for i in range(len(f)):
 b=instance(f,i);ss=list(b.states());hist[len(b.pairs(ss))]+=1
assert hist=={4:8,0:6};rows['double_octahedron_pairs_by_root']=dict(hist)
(OUT/'extended.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
# Figures reuse the repository's face model and Tutte layout without writing there.
sys.path.insert(0,str(ROOT/'paper/figures'))
from model import Model
from layout import tutte
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
IMG=ROOT/'digestions/steps/img';IMG.mkdir(exist_ok=True)
def draw(name,root,pairs,titles,out):
 faces=D[name]['faces'];m=Model(faces,root)
 xy=tutte(m,dict(zip(m.roots,[(0,0),(10,0),(5,9)])))
 fig,axs=plt.subplots(1,len(pairs),figsize=(14,7),layout='constrained')
 for ax,(r,s),title in zip(axs,pairs,titles):
  nx.draw_networkx_edges(m.T,xy,ax=ax,edge_color='#cccccc',width=0.8)
  arcs=[(r[i],s[i]) for i in range(len(r))]
  nx.draw_networkx_edges(nx.DiGraph(arcs),xy,ax=ax,edge_color='#1763a5',width=2,arrows=True,arrowsize=13,node_size=150)
  q=m.Q_graph(s);cs=nx.cycle_basis(q)
  edges=[(c[i],c[(i+1)%len(c)]) for c in cs for i in range(len(c))]
  nx.draw_networkx_edges(q,xy,edgelist=edges,ax=ax,edge_color='#c93832',width=2.5,style='dashed')
  nx.draw_networkx_nodes(m.T,xy,ax=ax,node_size=170,node_color='white',edgecolors='#333333')
  nx.draw_networkx_labels(m.T,xy,ax=ax,font_size=8)
  ax.set_title(title,fontsize=12);ax.set_aspect('equal');ax.axis('off')
 fig.suptitle('Blue arrows: D. Red dashed edges: cycles of Q_s.',fontsize=13)
 fig.savefig(IMG/out,dpi=180);plt.close(fig)
s=(1,3,7,2,9,11,6,12,8,10)
r=(6,2,8,1,3,10,11,7,12,9);rp=(6,2,1,9,3,10,11,7,12,8)
draw('running',D['running']['t0'],[(r,s),(rp,s)],['First cover, sign -1; same second state s*','Second cover, sign +1; same second state s*'],'two-covers.png')
d=D['v16_class158'];m=Model(d['faces'],d['t0']);ps=list(m.pairs());bad=[]
for r,s in ps:
 if len(m.directed_cycles(m.D(r,s)))==1:bad.append((r,s))
assert len(bad)==2 and all(not m.Q_is_forest(s) for r,s in bad)
draw('v16_class158',d['t0'],bad,['One orientation: Q_s has a triangle','Reverse orientation: Q_s has another triangle'],'bad-cover-16.png')
