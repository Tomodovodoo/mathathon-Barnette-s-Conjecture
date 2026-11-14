from campaign import *
from barnette_lab.core import glue_triangles,dual_graph
base=dual_graph(nx.circular_ladder_graph(6));t=base.copy();rootset=set(Instance(t).faces[0]);out=[]
for q in range(1,7):
 b0=Instance(t);outer=next(i for i,f in enumerate(b0.faces) if set(f)==rootset);b=Instance(t,outer)
 ss=list(b.states());nt=sum(b.is_tree(s) for s in ss)
 row={'q':q,'vertices':len(t),'states':len(ss),'trees':nt};out.append(row);print(row,flush=True)
 save(f'examples/rarity_{q}.json',{'dual_edges':list(t.edges()),'outer':outer})
 t=glue_triangles(t,base,b.white[-1],0)
save('data/rarity.json',out);event('White-inner prism sums counted through six pieces')

