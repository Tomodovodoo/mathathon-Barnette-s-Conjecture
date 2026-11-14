from model import model,OUT,nx,it,json
rows=[]
pts=sorted(set(tuple(a*s for a,s in zip(p,sgn)) for p in set(it.permutations((0,1,2))) for sgn in it.product((-1,1),repeat=3)))
g=nx.Graph();g.add_nodes_from(range(len(pts)));g.add_edges_from((i,j) for i,j in it.combinations(g,2) if sum((a-b)**2 for a,b in zip(pts[i],pts[j]))==2)
for name,G in [('cube',nx.cubical_graph()),('truncated octahedron',g)]+[(f'{n}-prism',nx.circular_ladder_graph(n)) for n in range(6,25,2)]:
 m=model(G);rows.append(dict(name=name,dual_vertices=len(m[0]),states=len(m[7]),pairs=len(m[8]),cyclic_pairs=len(m[9])))
(OUT/'candidate-checks.json').write_text(json.dumps(rows,indent=2))
