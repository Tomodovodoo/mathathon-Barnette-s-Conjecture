"""Checked primal-only panels. Imports shared geometry read-only; writes here only."""
import sys,json,subprocess
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[3]; HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'paper/figures'))
import check as shared
from draw import Panel,pt
from model import und
sys.path.insert(0,str(ROOT/'research/2026-11-14_fable_referee-primal/code'))
from primal import PG,Rooted,E,undirected_cycles
from check_lemmas import recover,tree_matching

def primal(m):
 g=PG({i:[m.left[b,a] for a,b in zip(f,f[1:]+f[:1])] for i,f in enumerate(m.F)})
 assert g.genus0() and set(g.edges)=={E(*e) for e in m.G.edges}
 fmap={i:next(v for v in m.V if {t for t,f in enumerate(m.F) if v in f}==vs) for i,vs in enumerate(g.fverts)}
 assert len(set(fmap.values()))==len(m.V)
 return g,fmap

def data(name):
 m=shared.load(name); xy,L=shared.coords(name); g,fmap=primal(m); R=Rooted(g,m.t0)
 states=R.states(); pairs=[(r,s) for r in states for s in states if R.is_pair(r,s)]
 forest=lambda s: not undirected_cycles(range(g.nF),[(i,*g.efaces[e]) for i,e in enumerate(R.Q(s))])
 if name=='running':
  r,s=next((r,s) for r,s in pairs if not forest(s) and forest(r) and max(len(c) for c in R.pair_circuits(r,s))>3)
 else:r,s=pairs[0]
 circ=max(R.pair_circuits(r,s),key=len); d=R.circuit_data(circ)
 assert d and d['h']==2*d['ell']+3 and d['nWS']==d['nBS']+1
 assert 3*d['nS']+d['h']==2*d['nES']
 assert 3*d['nBS']+d['h']==d['nES']+d['ell']
 assert d['nS']+d['nUS']==d['nES']+1
 assert d['nBS']+d['h']==d['nUS']+d['ell']
 assert d['slope']==next(iter(d['sigma']))*d['nWS']
 sf=r if forest(r) else s; e0=E(*m.dual[m.e0]); rem,K=recover(R,sf,e0); P,par=tree_matching(R,rem)
 assert nx.is_tree(nx.Graph([tuple(e) for e in K]))
 assert e0 in P and all(sum(v in e for e in P)==1 for v in g.V) and g.connected(P)
 assert all(R.divergence(w)==-1 for w in R.white) and R.divergence(m.t0)==len(R.white)
 assert all(R.divergence(b)==0 for b in R.A)
 return dict(m=m,xy=xy,L=L,g=g,fmap=fmap,R=R,r=r,s=s,circ=circ,d=d,P=P,K=K,e0=e0,states=states,pairs=pairs)

def panel(z):return Panel(z['m'],z['xy'],z['L']['R'],unit=0.62,collar=False,pad=.85).graphG()
def faces(p,z):
 for v in z['m'].V:p.label(z['xy'][v],rf'$f_{{{v}}}$','fill=white,text=black!75')
 p.label(p.cen[z['m'].t0]+[.0,-.45],r'$b_0$')
 return p

def state(p,z,s,style):
 for b,f in zip(z['R'].A,s):
  v=z['fmap'][f]
  p.add(rf'\draw[{style}] {pt(p.cen[b])} -- {pt(z["xy"][v])};')
 return p

def shore(p,z):
 for v in z['d']['S']:p.add(rf'\fill[bfW,opacity=.20] {pt(p.cen[v])} circle[radius=5pt];')
 for _,_,e,_ in z['circ']:p.graphG('bf Q',edges=[und(*e)],dots=False)
 p.dotsG();return p

def output(name,panels,caption):
 body='\n\\hfill\n'.join(r'\makebox[.48\textwidth][c]{'+p.tex()+'}' for p in panels)
 (HERE/(name+'-body.tex')).write_text(body)
 pre=r'\documentclass[border=4pt]{standalone}\usepackage{../../../paper/figures/barnette-figs}\setlength{\textwidth}{15.92cm}\begin{document}'
 (HERE/(name+'.tex')).write_text(pre+body+r'\end{document}')
 captions[name]=caption

captions={}; cube=data('octahedron');run=data('running'); both=[cube,run]
ps=[]
for z in both:
 p=faces(panel(z),z);p.graphG('bf P',edges=[und(*z['e0'])]);ps.append(p)
output('01-graph',ps,'The cube and the 22-vertex running graph G, with faces labelled. Filled vertices are black, hollow vertices white. The bold edge is e0. Face labels use the shared dual layout, but only edges of G are drawn.')
ps=[]
for z in both:
 p=panel(z);state(p,z,z['r'],'draw=bfR,line width=1.2pt,double=white,double distance=.5pt');state(p,z,z['s'],'draw=bfS,line width=1.1pt');faces(p,z);p.dotsG();ps.append(p)
output('02-pair',ps,'A pair as incidence matchings: blue solid segments assign s; vermilion outlined segments assign r. Endpoints labelled f are primal faces, not vertices of G. Each nonroot black vertex and each nonroot face occurs once in each colour.')
ps=[]
for z in both:
 p=shore(panel(z),z);d=z['d'];p.label([0,-z['L']['R']-.8],rf'$|S|={d["nS"]},\ |B\cap S|={d["nBS"]},\ |E_S|={d["nES"]},\ |U_S|={d["nUS"]}$');p.box[1]-=1;ps.append(p)
output('03-disk',ps,'Green halos mark the vertices inside the cut side S; dashed vermilion edges form its boundary. The four counts below each graph satisfy (4.2). On the right h=7 and ell=2; the cut side has five black and six white vertices. Inside means the shore missing b0.')
ps=[]
for z in both:
 p=shore(panel(z),z);R=z['R']
 for e,a in R.alpha.items():
  if not a:continue
  g=und(*e); start=g[1] if z['m'].t0 in g else g[0]
  # toolkit root paths run from the inner vertex to the root
  if z['m'].t0 in g:start=next(v for v in g if v!=z['m'].t0)
  forward=(a>0)==(start in R.black)
  mark='>' if forward else '<'
  p.add(rf'\draw[draw=bfS,line width=.8pt,postaction={{decorate}},decoration={{markings,mark=at position .55 with {{\arrow{{{mark}}}}}}}] {p.dual_path(g)};')
  mid=p.mid(*z['m'].cross[g]);p.label(mid,str(abs(a)),'fill=white,text=bfS')
 p.dotsG();p.label([0,-z['L']['R']-.8],rf'$\mathrm{{weight}}(C)=|W\cap S|={z["d"]["nWS"]}$');p.box[1]-=1;ps.append(p)
output('04-flow',ps,'Integer path flow from b0 to every white vertex of G. Arrows show net direction; labels give absolute flow. Every white vertex absorbs one unit. For the positive circuit orientation the weight is the number of white vertices in S, equivalently the white faces of T. Blue flow arrows are independent of the dashed cut orientation.')
z=run;R=z['R'];ps=[];partners=[r for r in z['states'] if R.is_pair(r,z['s'])];assert len(partners)==2 and sum(R.eps(r,z['s']) for r in partners)==0
for r in partners:
 p=panel(z);state(p,z,r,'draw=bfR,line width=1.2pt,double=white,double distance=.5pt');state(p,z,z['s'],'draw=bfS,line width=1.1pt');p.graphG('bf Q',edges=[und(*e) for e in R.Q(z['s'])]);p.label([0,-z['L']['R']-.8],rf'$\varepsilon(r,s)={R.eps(r,z["s"])}$');p.box[1]-=1;ps.append(p)
output('05-cancellation',ps,'A second state s whose Q_s contains a face circuit, shown with its two partners. Dashed primal edges are Q_s, viewed as links between faces. Reversing the tails on its odd face circuit exchanges the outlined incidence segments and reverses the sign. The blue state, and hence its entire weight polynomial, stays fixed.')
ps=[]
for z in both:
 p=panel(z);p.graphG('bf cycle',edges=[und(*e) for e in z['g'].edges if e not in z['P']],dots=False);p.graphG('bf P',edges=[und(*e) for e in z['P']]);ps.append(p)
output('06-recovery',ps,'The recovered perfect matching P is bold black; G-P is the purple Hamiltonian cycle. Every vertex has one matching edge and two cycle edges, and e0 belongs to P. Both objects are computed from the parent edges of the recovery tree.')
gl=shared.gluing();m=gl['T'];cut=[m.dual[und(a,b)] for a,b in zip(gl['cap'],gl['cap'][1:]+gl['cap'][:1])];H=m.G.copy();H.remove_edges_from(cut);comps=list(nx.connected_components(H));assert len(comps)==2 and min(map(len,comps))>1 and len(cut)==3
p=Panel(m,gl['xy'],gl['R'],unit=.62,collar=False,pad=.85).graphG();p.graphG('bf Q',edges=cut);ps=[p]
# separate page: original plus two cap pieces, full width total ~14cm
for mm,xy in [(gl['m1'],gl['xy1']),(gl['m2'],gl['xy2'])]:
 assert nx.is_isomorphic(mm.G,nx.cubical_graph())
 pp=Panel(mm,xy,gl['R'],unit=.42,collar=False,pad=.85).graphG();capv=next(i for i,f in enumerate(mm.F) if set(f)==set(gl['cap'])); assert set(mm.F[capv])==set(gl['cap']); pp.label(pp.cen[capv]+([.75,-.27] if pp.cen[capv][1]<-3 else [.75,.3]),'cap');ps.append(pp)
# Place original on one row, the pieces on the next to preserve label size.
output('07-cut',ps[:1],'A nontrivial three-edge cut in the glued-cube example, dashed vermilion. Its two capped shores are the cube pieces shown next. This example is separate from the irreducible running graph.')
output('08-pieces',ps[1:],'The two capped pieces of the preceding cut, both cubes. The cap vertices replace the opposite shores. If a Hamiltonian cycle in each piece omits the same cut edge, deleting the cap vertices leaves two spanning paths that glue across the two used cut edges (Lemma 13; the cycles are not drawn).')
summary={'status':'COMPUTED','examples':{name:{'vertices':len(z['g'].V),'faces':z['g'].nF,'states':len(z['states']),'pairs':len(z['pairs']),'counts':{k:z['d'][k] for k in ['nS','nBS','nWS','nES','nUS','h','ell','slope']},'P':[sorted(e) for e in z['P']],'r':z['r'],'s':z['s'],'face_map':z['fmap']} for name,z in [('cube',cube),('running',run)]},'cut':[list(e) for e in cut],'cut_shore_sizes':list(map(len,comps)),'assertions':'state bijections, pairs, four counts, slope, divergences, tree, perfect matching, Hamiltonian complement, nontrivial cut and cube caps'}
(HERE/'checked.json').write_text(json.dumps(summary,indent=2));(HERE/'captions.json').write_text(json.dumps(captions,indent=2))
print(json.dumps(summary,indent=2))
if '--build' in sys.argv:
 import fitz
 for name in captions:
  r=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',name+'.tex'],cwd=HERE,capture_output=True,text=True)
  (HERE/(name+'-build.log')).write_text(r.stdout)
  assert r.returncode==0,r.stdout[-3000:]
  doc=fitz.open(HERE/(name+'.pdf'));doc[0].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(HERE/(name+'.png'))
