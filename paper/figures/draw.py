import json,math,networkx as nx,numpy as np
from pathlib import Path
O=Path(__file__).parent;d=json.loads((O/'checked.json').read_text());F=d['faces'];A=d['A'];xy={int(k):np.array(v) for k,v in d['coordinates'].items()};cent={i:sum((xy[v] for v in f))/3 for i,f in enumerate(F)};r,s=d['cyclic_pair'];rg,sg=d['forest_pair'];P={tuple(sorted(e)) for e in d['selected_edges']}
def pt(p):return '('+','.join(f'{x:.5f}' for x in p)+')'
def line(u,v,sty):return rf'\draw[{sty}] {pt(u)} -- {pt(v)};'
def edge(u,v):return tuple(sorted((u,v)))
def panel(mode='',pair=None,scale=.52,labels=False):
 scale=.72
 out=[rf'\begin{{tikzpicture}}[x={scale}cm,y={scale}cm]',r'\path[use as bounding box] (-.6,-.7) rectangle (12.6,11);']
 for t in d['black']:
  if t:out.append(r'\fill[black!9] '+' -- '.join(pt(xy[v]) for v in F[t])+' -- cycle;')
 if mode=='disk':
  for t in d['disk']['faces']:out.append(r'\fill[pairorange!18] '+' -- '.join(pt(xy[v]) for v in F[t])+' -- cycle;')
 for u,v in d['edges']:out.append(line(xy[u],xy[v],'base'))
 rr,ss=pair or (rg,sg)
 if mode in ['state','pair','cancel']:
  for t,a,b in zip(A,rr,ss):
   # Marker is inside its own black triangle, close to its chosen corner.
   out.append(r'\node[markS] at '+pt(.76*xy[b]+.24*cent[t])+' {};')
   if mode!='state':out.append(r'\node[markR] at '+pt(.76*xy[a]+.24*cent[t])+' {};')
 if mode in ['pair','D']:
  for a,b in zip(rr,ss):out.append(line(xy[a],xy[b],'dedge'))
 if mode in ['Q','cancel']:
  for t,a,b in zip(A,rr,ss):
   u=next(v for v in F[t] if v not in [a,b]);out.append(line(xy[a],xy[u],'qedge,-{Stealth[length=3pt]}'))
 if mode=='disk':
  cy=d['disk']['cycle']
  for a,b in zip(cy,cy[1:]+cy[:1]):out.append(line(xy[a],xy[b],'dedge'))
 if mode=='incidence':
  for t,v in zip(A,sg):
   for u in F[t]:out.append(line(cent[t],xy[u],'spoke,dashed' if u==v else 'pedge'))
   out.append(r'\fill '+pt(cent[t])+' circle[radius=1.5pt];')
  out += [line(np.array([6,-1.4]),xy[d['roots'][0]],'pedge'),line(np.array([6,-1.4]),xy[d['roots'][1]],'pedge')]
  # Third root is the apex in this fixed ordered boundary.
  out.append(r'\draw[pedge] (6,-1.4)--(14,-1.4)--(14,11.5)--(6,11.5)--(6,10.392);')
  out.append(r'\node[fill=white,inner sep=1pt] at (6,-1.4) {$c_0$};')
 if mode in ['spokes','detour']:
  for t in A:
   for v in F[t]:out.append(line(cent[t],xy[v],'spoke'))
  for t,a,b in zip(A,r,s):
   out.append(line(xy[a],cent[t],'dedge'));out.append(line(cent[t],xy[b],'dedge'))
 if mode=='white':
  for t,v in zip(A,sg):
   sides=[edge(v,u) for u in F[t] if u!=v];ws=[next(w for w in d['white'] if set(e)<=set(F[w])) for e in sides]
   # Route inside the two adjacent white faces and this black face; crosses only the deleted spoke.
   mid=[(xy[e[0]]+xy[e[1]])/2 for e in sides];p=(cent[t]+xy[v])/2
   path=[cent[ws[0]],mid[0],p,mid[1],cent[ws[1]]]
   out.append(r'\draw[wt] '+' -- '.join(pt(z) for z in path)+';')
  out.append(r'\node[draw=treegreen,circle,line width=1pt,inner sep=3pt] at '+pt(cent[d['white_root']])+' {};')
  out.append(r'\node[anchor=north,fill=white,inner sep=.3pt] at '+pt(cent[d['white_root']]+[0,-.1])+r' {$y_0$};')
  for w in d['white']:out.append(r'\node[circle,draw=treegreen,fill=white,inner sep=1.5pt] at '+pt(cent[w])+' {};')
 if mode in ['P','trees','jordan']:
  for a,b in d['selected_edges']:out.append(line(xy[a],xy[b],'pedge'))
 if mode=='trees':
  for j,part in enumerate(d['parts']):
   for v in part:out.append(r'\node['+('circle,fill=stateblue' if j==0 else 'rectangle,fill=pairorange')+',inner sep=2.3pt] at '+pt(xy[v])+' {};')
 if mode=='jordan':out+=dual_routes(d['hamiltonian'],'ham')
 for v in xy:
  if mode!='trees':out.append(r'\fill '+pt(xy[v])+' circle[radius=1.1pt];')
  if v in d['roots']:out.append(r'\draw[line width=.7pt,fill=white] '+pt(xy[v])+' circle[radius=2.4pt];')
  if labels:out.append(r'\node[fill=white,inner sep=.5pt,anchor=south] at '+pt(xy[v]+[0,.10])+' {$'+str(v)+'$};')
 if mode=='disk':
  for t in d['disk']['faces']:out.append(r'\node[fill=white,inner sep=1pt] at '+pt(cent[t])+(' {$B$};' if t in d['black'] else ' {$W$};'))
  out.append(r'\node[anchor=north] at (6,-.8) {$B=1,\ W=2,\ I=0,\ h=5,\ l=1$};')
 out.append(r'\node[anchor=north] at (6,-.25) {$t_0$ is the outer black face};')
 out.append(r'\end{tikzpicture}');return '\n'.join(out)
def dual_routes(es,sty):
 out=[]
 for a,b in es:
  common=list(set(F[a])&set(F[b]));mid=sum((xy[v] for v in common))/2
  if 0 not in [a,b]:out.append(r'\draw['+sty+'] '+' -- '.join(pt(z) for z in [cent[a],mid,cent[b]])+';')
  else:
   v=b if a==0 else a
   # Exterior arcs are routed outside the triangular boundary, all meeting t0 below.
   roots=d['roots'];e=set(common)
   if e==set(roots[:2]):route=[cent[v],mid,np.array([6,-1.0])]
   elif roots[0] in e:route=[cent[v],mid,mid+[-1.3,.5],np.array([-1.,-1.]),np.array([6,-1.])]
   else:route=[cent[v],mid,mid+[1.3,.5],np.array([13.,-1.]),np.array([6,-1.])]
   out.append(r'\draw['+sty+'] '+' -- '.join(pt(z) for z in route)+';')
 return out
# Independent planar primal drawing, with shared coordinates between its two panels.
G=nx.Graph(d['dual_edges'])
from model import faces
outer=max(faces(G),key=len); interior=sorted(set(G)-set(outer)); gp={v:np.array([6+5*math.cos(2*math.pi*i/len(outer)),5+5*math.sin(2*math.pi*i/len(outer))]) for i,v in enumerate(outer)}
L=nx.laplacian_matrix(G,nodelist=interior+outer).toarray();p=np.linalg.solve(L[:len(interior),:len(interior)],-L[:len(interior),len(interior):]@np.array([gp[v] for v in outer]));gp.update(dict(zip(interior,p)))

def primal(es):
 out=[r'\begin{tikzpicture}[x=.72cm,y=.72cm]',r'\path[use as bounding box] (-.6,-.7) rectangle (12.6,11);']
 for a,b in G.edges():out.append(line(gp[a],gp[b],'base'))
 for a,b in es:out.append(line(gp[a],gp[b],'ham'))
 for v in G:out.append(r'\node[circle,draw,fill='+('black' if v in d['black'] else 'white')+',inner sep=1.4pt] at '+pt(gp[v])+' {};')
 out.append(r'\end{tikzpicture}');return '\n'.join(out)
def two(a,b,la,lb):return r'\begin{tabular}{@{}c@{}}'+'\n'+a+r'\\[1mm]'+la+r'\\[4mm]'+b+r'\\[1mm]'+lb+'\n'+r'\end{tabular}'

figs=[]
def add(name,body,cap):figs.append((name,body,cap))
add('01-two-factors',two(primal(d['two_factor']),primal(d['hamiltonian']),'Two cycle components','One spanning cycle'),r'Both bold subgraphs have degree two at every vertex. Only the lower one is connected. These are the same 24-vertex graph, dual to the running triangulation.')
add('02-dual',panel(scale=.9,labels=True),r'The running Eulerian triangulation has 14 vertices and 24 faces. Grey interiors denote black faces; the unbounded face is also black. Hollow vertices are the three roots. Vertex numbers remain fixed throughout.')
add('03-cycle-trees',two(panel('trees'),primal(d['hamiltonian']),'Two induced trees in $T$','Complementary dual cycle in $G$'),r'Every edge within either vertex class is bold. The duals of all remaining edges form the single cycle below. Circle and square classes remain distinguishable without colour.')
add('04-state',panel('state',scale=.9),r'A blue disk marks the corner $s(t)$ inside each bounded black triangle. Every nonroot receives exactly one mark; roots receive none. This state has a disjoint partner and a forest $Q_s$.')
add('05-pair-D',two(panel('pair',(r,s)),panel('D',(r,s))),'') if False else None
add('05-pair-D',two(panel('pair',(r,s)),panel('D',(r,s)),'Squares: $r$; disks: $s$','$D$: arrows from $r(t)$ to $s(t)$'),r'The two states choose different corners in every black face. Their directed edges split the nonroots into three cycles. The lower panel removes corner marks to expose those cycles.')
add('06-Q',two(panel('Q',(r,s)),panel('Q',(rg,sg)),'Cyclic $Q_s$','Forest $Q_s$'),r'Each dashed edge lies opposite the second-state mark. The upper state has a cycle; the lower has three tree components, each containing one root. The panels use different second states.')
b=d['disk'];add('07-disk',panel('disk',(r,s),scale=.9),rf'The highlighted disk bounded by a five-edge cycle has $B={b["B"]}$, $W={b["W"]}$, $I={b["I"]}$, $h={b["h"]}$ and $l={b["l"]}$. Thus $B+W=2I+h-2$, $B=I+l$ and $2l-h=-3$. The other two cycles of $D$ are suppressed.')
add('08-cancellation',two(panel('cancel',(r,s)),panel('cancel',d['reversed_pair']),r'$J(r,s)=3$',r'$J(\widetilde r,s)=1$'),r'Reverse the dashed cycle by moving only the square marks. Blue disks, hence $s$ and its real weight, stay fixed. The phase changes from $i^3$ to $i$, so these two terms cancel. Applying the move twice restores the first panel.')
add('09-spokes',two(panel('D',(r,s)),panel('detour',(r,s)),'Edges of $D$','Two-spoke detours'),r'Each directed edge moves through the centre of its own black triangle. Detours have disjoint interiors and exclude the third corner. With $a(t,v)=\tfrac12\det(c_t,v)$, counterclockwise circulation is the positive area of the spoke polygon. The checked circulations are '+', '.join(f'{v:.3f}' for v in d['circulations'])+'.')
add('10-white-tree',two(panel('incidence'),panel('white'),'Retained incidence tree $H-s$','White-face cotree, rooted at $y_0$'),r'The dash-dot routes cross the deleted spokes $(t,s(t))$. The upper panel retains the solid spokes and deletes the dashed ones. Below, the routes join all 12 white centres in one tree with 11 edges. Each route stays within the two white faces and their common black triangle. This is the cotree of the retained incidence tree.')
add('11-selected-Jordan',panel('jordan',scale=.85),r'The bold black edges are $P$, one side of every face. The blue Jordan curve crosses precisely the unselected edges. Its two regions separate the two components of $P$; the exterior arcs represent edges incident with the outer-face dual vertex.')
add('12-recovered',two(panel('trees'),primal(d['hamiltonian']),'Induced tree partition','Hamiltonian cycle'),r'The recovered partition includes the prescribed outer edge in one tree. The complementary dual cycle visits each of the 24 faces once and avoids the dual of that prescribed edge. This is the same cycle as in Figures 1 and 3.')
# Gluing witness: two octahedra glued along a face, verified by exhaustive partitions.
OCT=nx.octahedral_graph();tri=next(c for c in nx.enumerate_all_cliques(OCT) if len(c)==3);rest=sorted(set(OCT)-set(tri));mapping={v:i for i,v in enumerate(tri+rest)};OCT=nx.relabel_nodes(OCT,mapping);GL=nx.compose(OCT,nx.relabel_nodes(OCT,{3:6,4:7,5:8}));part=None
for bits in range(1<<6):
 z={0,1}|{v for j,v in enumerate(range(3,9)) if bits>>j&1};zz=set(GL)-z
 if nx.is_tree(GL.subgraph(z)) and nx.is_tree(GL.subgraph(zz)):part=[z,zz];break
assert part
pos={0:np.array([0.,0.]),1:np.array([10.,0.]),2:np.array([5.,8.66])}
# Tutte solve for each octahedral piece, reflected apart for the two panels.
def gluepanel(nodes):
 g=GL.subgraph(nodes);xs=sorted(set(nodes)-{0,1,2});L=nx.laplacian_matrix(g,nodelist=xs+[0,1,2]).toarray();ps=np.linalg.solve(L[:3,:3],-L[:3,3:]@np.array([pos[v] for v in [0,1,2]]));p=pos|dict(zip(xs,ps));o=[r'\begin{tikzpicture}[x=.72cm,y=.72cm]']
 for a,b in g.edges():o.append(line(p[a],p[b],'pedge' if any(a in z and b in z for z in part) else 'base'))
 for v in nodes:o.append(r'\node['+('circle,fill=stateblue' if v in part[0] else 'rectangle,fill=pairorange')+',text=white,inner sep=2pt] at '+pt(p[v])+f' {{{v}}};')
 o.append(r'\end{tikzpicture}');return '\n'.join(o)
add('13-gluing',two(gluepanel(list(range(6))),gluepanel([0,1,2,6,7,8]),'First capped piece','Second capped piece'),r'This separate nine-vertex witness glues two octahedra along vertices $0,1,2$. The blue trees intersect in edge $01$; the orange trees intersect in vertex $2$. Exhaustive checking verifies both induced trees in the glued graph. Identify the boundary vertices rather than placing both interiors in the same planar disk.')
flow=r'''\begin{tikzpicture}[x=1cm,y=1cm]
\tikzset{box/.style={draw,rounded corners=0pt,text width=10cm,align=center,minimum height=9mm}}
\node[box] (a) at (0,0) {Rooted triangulation $T$ and incidence matchings};
\node[box] (b) at (0,-1.5) {Disjoint pair $(r,s)$ and directed cycles $D$};
\node[box] (c) at (0,-3) {Cancellation + positive spoke circulation $\Rightarrow$ forest $Q_s$};
\node[box] (d) at (0,-4.5) {Retained spoke tree $\longleftrightarrow$ white-face cotree};
\node[box] (e) at (0,-6) {Selected edges $P$: one side of every face, no cycles};
\node[box] (f) at (0,-7.5) {Two induced trees $\longleftrightarrow$ Hamiltonian cycle in $G$};
\foreach \u/\v in {a/b,b/c,c/d,d/e,e/f} \draw[-{Stealth}] (\u)--(\v);
\end{tikzpicture}'''
add('14-overview',flow,r'Read down the main proof for a triangulation without separating triangles. The disk identity supports both the cancellation step and acyclicity of $P$. For a separating triangle, apply the construction to the capped pieces and glue using Figure 13. The flow records logical dependence, not an efficient algorithm.')
for name,body,cap in figs:
 (O/(name+'-body.tex')).write_text(body)
 (O/(name+'.tex')).write_text(r'\documentclass[10pt,border=6pt]{standalone}'+'\n'+r'\usepackage{barnette-figs}'+'\n'+r'\begin{document}'+body+r'\end{document}')
gallery=[r'\documentclass[10pt,a4paper]{amsart}',r'\usepackage[margin=1in]{geometry}',r'\usepackage{barnette-figs}',r'\begin{document}']
for i,(name,body,cap) in enumerate(figs,1):
 gallery += [r'\section*{'+f'{i}. '+name[3:].replace('-',' ')+r'}',r'\begin{figure}[h!]\centering',r'\input{'+name+'-body.tex}',r'\caption{'+cap+r'}',r'\end{figure}',r'\clearpage']
gallery.append(r'\end{document}');(O/'gallery.tex').write_text('\n'.join(gallery));(O/'captions.json').write_text(json.dumps({name:cap for name,_,cap in figs},indent=2))
(O/'gluing.json').write_text(json.dumps(dict(edges=list(GL.edges()),parts=[sorted(z) for z in part]),indent=2))
