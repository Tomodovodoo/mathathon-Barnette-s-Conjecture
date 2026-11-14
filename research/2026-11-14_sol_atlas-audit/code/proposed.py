"""Compile proposed TikZ figures with atlas toolkit. All writes owned."""
from independent import *
import sys,os,subprocess,numpy as np
from scipy.optimize import minimize
sys.dont_write_bytecode=True
sys.path.insert(0,str(R/'digestions/atlas/toolkit'))
from model import Model,oriented_faces
from draw import Panel,pt
import layout,check
D=R/'digestions/atlas/proposed';D.mkdir(exist_ok=True)
ld=json.loads((R/'digestions/atlas/toolkit/layout-running.json').read_text());xy={int(k):np.array(v) for k,v in ld['coordinates'].items()};rad=ld['R'] if 'R' in ld else 5
m=Model(F,j['t0'],j['e0']); rad=float(np.linalg.norm(xy[m.roots[0]]))
def panel(mod=m,pos=xy,unit=.62):return Panel(mod,pos,rad,unit=unit)
def cell(tex,caption,w=7.1):return r'\begin{minipage}{'+str(w)+r'cm}\centering '+tex+r'\par\smallskip{\footnotesize '+caption+r'}\end{minipage}'
def compile(name,body):
 src=r'\documentclass[10pt,border=3pt]{standalone}'+'\n'+r'\usepackage{amsmath,amssymb,booktabs,atlas-figs}'+'\n'+r'\begin{document}'+body+r'\end{document}'
 (D/f'{name}.tex').write_text(src,encoding='utf8');env=dict(os.environ,TEXINPUTS=f'{R}/digestions/atlas;{R}/digestions/atlas/toolkit;');res=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',f'{name}.tex'],cwd=D,env=env,capture_output=True,text=True)
 if res.returncode:raise RuntimeError(res.stdout[-2000:])
 print(name)
# Matrix figure, full symbolic prism matrix, checked by direct pair expansion.
c=C['determinant']['prism'];hm=Model(c['faces'],c['t0']); Y=sp.symbols('a:'+str(len(hm.A))); ww={(t,v):sp.Symbol(f'w_{i}{v}') for i,t in enumerate(hm.A) for v in hm.F[t]};NN=sp.zeros(len(hm.X))
for i,t in enumerate(hm.A):
 for u,v in it.permutations([v for v in hm.F[t] if v in hm.X],2):NN[hm.X.index(u),hm.X.index(v)]+=hm.delta(u,v)*Y[i]*ww[t,v]
det=sp.Poly(sp.expand(NN.det()),*Y);coef=det.coeff_monomial(sp.prod(Y)); ss=enum(hm.F,hm.A,hm.X);pairpoly=sp.expand(sum(math.prod(hm.delta(u,v) for u,v in zip(r,s))*sp.prod(ww[t,v] for t,v in zip(hm.A,s)) for r in ss for s in ss if all(u!=v for u,v in zip(r,s))));assert sp.expand(coef-pairpoly)==0
# readable entries e.g. a w_a4
entry=lambda z:sp.latex(z).replace('w_{','w_{')
mat=r'\begin{pmatrix}'+r'\\[3mm]'.join(' & '.join(entry(NN[i,k]) for k in range(NN.cols)) for i in range(NN.rows))+r'\end{pmatrix}'
qdata=json.loads((R/'digestions/atlas/layouts.json').read_text())['prism6'];q={int(k):np.array(v) for k,v in qdata.items()};p=panel(hm,q,.57).base().vertices(labels=True)
for i,t in enumerate(hm.A):p.label(p.cen[t],rf'${sp.latex(Y[i])}$','af lab')
body=cell(p.tex(),r'Hexagonal-prism dual. The five bounded black faces are $a_0,\ldots,a_4$; rows and columns use vertices '+','.join(map(str,hm.X))+'.',7)+r'\\[3mm]'+cell(r'$\displaystyle N='+mat+r'$',r'$N_{uv}=\sum_{t\supset\{u,v\}}y_t\delta(u,v)w_{t,v}$ for $u\ne v$, and $N_{uu}=0$. Here $y_t=a_i$.',13)
body=r'\begin{tabular}{c}'+body+r'\\[4mm] $\displaystyle [a_0a_1a_2a_3a_4]\det N='+sp.latex(coef)+r'$\\[2mm] {\footnotesize Coefficient extraction gives two opposite-signed tree monomials. At all $w=1$, they cancel.}\end{tabular}'
compile('p11-matrix',body)
# FS witness, preserve three-shape coding. Root/layout generated in memory, never cache atlas.
w=json.loads((O/'fs-witness.json').read_text());tg=nx.Graph(w['edges']);ff=oriented_faces(tg);mm=Model(ff,0)
# Try both boundary orders while retaining the oriented fixture.
for angles in ([90,210,330],[90,330,210]):
 fixed={v:layout.R*np.array([np.cos(np.radians(a)),np.sin(np.radians(a))]) for v,a in zip(mm.roots,angles)};qq=layout.tutte(mm,fixed)
 if all(np.linalg.det(np.array([qq[f[1]]-qq[f[0]],qq[f[2]]-qq[f[0]]]))>0 for i,f in enumerate(ff) if i!=0):break
qq,_=layout.relax(mm,qq,rounds=80);col={int(k):v for k,v in w['colour'].items()};bc=w['B'];cells=[]
for tag,key in [('a','accept'),('b','reject')]:
 ps=list(map(set,w[key]));
 if key=='accept' and any(col[u]!=bc and col[v]!=bc for u,v in mm.T.subgraph(ps[0]).edges()):ps=ps[::-1]
 pp=Panel(mm,qq,layout.R,unit=.65).base();pe=[e for e in mm.E if (e[0] in ps[0])==(e[1] in ps[0])];pp.lines(pe,'bf P')
 bad=[]
 for U in ps:bad.append([e for e in mm.E if set(e)<=U and col[e[0]]!=bc and col[e[1]]!=bc])
 assert any(not b for b in bad) if key=='accept' else all(bad)
 for e in (sum(bad,[]) if key=='reject' else []):
  pp.lines([e],'bf P,dashed,line width=2pt');pp.label(pp.arcmid(*e) if set(e)<=set(mm.roots) else (qq[e[0]]+qq[e[1]])/2,r'$\times$','af lab')
 for v in mm.V:
  sh=['circle','rectangle','regular polygon,regular polygon sides=3'][col[v]];pp.add(rf'\node[draw,{sh},fill={"black" if v in ps[0] else "white"},minimum size=6pt,inner sep=0pt] at {pt(qq[v])} {{}};')
 cells.append(cell(pp.tex(),rf'({tag}) '+('Qualifies: the filled induced tree has independent vertices outside class '+str(bc)+'.' if key=='accept' else 'Excluded: both trees contain an edge outside class '+str(bc)+r'. Crosses mark those edges.')))
compile('p24-colour-restriction',r'\begin{tabular}{cc}'+ ' & '.join(cells)+rf'\\[3mm]\multicolumn{{2}}{{c}}{{\footnotesize Dual order 10, plantri index {w["index"]}: {w["qualifying"]} of {w["total"]} cycles pass for class {bc}. Shapes encode all three colours.}}\\ \multicolumn{{2}}{{c}}{{\footnotesize This is the relaxed radial-tree dictionary. Feder--Subi proper quasi vertices need degree four and no incident digon.}}\end{{tabular}}')
# Cut connections separately in the two closed sides, all 28 partitions.
cut=C['cuts']['four_cycle'];removed=T.copy();removed.remove_nodes_from(cut);sides=sorted(map(set,nx.connected_components(removed)),key=lambda U:bool(U&roots));groups=defaultdict(list)
for ps in parts:
 if cut[0] not in ps[0]:ps=ps[::-1]
 sig=[]
 for side in sides:
  sig.append(tuple(tuple(sorted(tuple(sorted(set(cc)&set(cut))) for cc in nx.connected_components(T.subgraph(U&(side|set(cut)))) if set(cc)&set(cut))) for U in ps))
 groups[(tuple(int(v not in ps[0]) for v in cut),str(sig))].append((ps,sig))
cells=[];records=[]
for (word,_),lst in sorted(groups.items()):
 ps,sig=lst[0];p=panel(unit=.43).base().lines([e for e in E if (e[0] in ps[0])==(e[1] in ps[0])],'bf P');p.lines(list(zip(cut,cut[1:]+cut[:1])),'draw=bfR,dashed,line width=2pt').vertices(classes=ps)
 for i,v in enumerate(cut):p.label(xy[v]+np.array([.15,.2]),str(i),'af lab')
 labels=[]
 for side,sg in zip(['inside','outside'],sig): labels.append(side+': '+ ' / '.join(';'.join(''.join(str(cut.index(v)) for v in block) for block in blocks) for blocks in sg))
 cells.append(cell(p.tex(),''.join(map(str,word))+rf', {len(lst)} cycles.\par '+r'\par '.join(labels),5.2));records.append(dict(word=word,count=len(lst),signature=sig))
assert sum(len(a) for a in groups.values())==28
rows=[' & '.join(cells[i:i+3]) for i in range(0,len(cells),3)];compile('p22-connections',r'\begin{tabular}{ccc}'+r'\\[4mm]'.join(rows)+r'\end{tabular}')
(O/'cut-connections.json').write_text(json.dumps(records,indent=2));print('cut signatures',len(groups))
# Aligned contraction. Keep every surviving vertex exactly in place, move merged vertex minimally.
x0=2;v1=3;v2=1;fs=[tuple(v1 if v==v2 else v for v in f) for f in F if x0 not in f];sm=Model(fs,next(i for i,f in enumerate(fs) if set(f)==roots),j['e0']);qq={v:xy[v].copy() for v in sm.V};qq[v1]=(xy[v1]+xy[v2])/2
free=list(sm.X);base=np.concatenate([qq[v] for v in free]);
def unpack(z):return {**{v:xy[v] for v in sm.roots},**{v:z[2*i:2*i+2] for i,v in enumerate(free)}}
def areas(z):
 pos=unpack(z);return np.array([np.linalg.det(np.array([pos[f[1]]-pos[f[0]],pos[f[2]]-pos[f[0]]])) for i,f in enumerate(fs) if i!=sm.t0])
sol=minimize(lambda z:sum((z-base)**2),base,constraints=[{'type':'ineq','fun':lambda z:areas(z)-.06}],method='SLSQP',options={'maxiter':500,'ftol':1e-12});assert sol.success and min(areas(sol.x))>.059;qq=unpack(sol.x);check.check_layout(sm,qq,rad)
ss=enum(sm.F,sm.A,sm.X);gss=[z for z in ss if nx.is_forest(qgraph(z,sm.F,sm.A,sm.V)) and all(len(set(cc)&roots)==1 for cc in nx.connected_components(qgraph(z,sm.F,sm.A,sm.V)))];assert len(gss)==4
pa=panel().base().vertices(labels=True);pa.add(rf'\draw[af bold,<->] {pt(xy[v1])} -- {pt(xy[v2])};');pb=panel(sm,qq).base().state(gss[0]).lines(sm.Q(gss[0]),'bf Q').vertices(labels=True);pb.label(qq[v1]+np.array([.5,0]),r'$1\sim3$','af lab');compile('p23-aligned',cell(pa.tex(),'(a) Delete 2 and identify 1 with 3. Labels persist.')+' '+cell(pb.tex(),'(b) Roots fixed; surviving vertices move only as required to keep every face oriented. One of four good states.'))
(O/'aligned.json').write_text(json.dumps({'positions':{v:list(map(float,q)) for v,q in qq.items()},'minimum_face_area':float(min(areas(sol.x))),'tree_state':gss[0]},indent=2))
# Li ray pairing in the running atlas geometry, computed independently with rational intersections.
from fractions import Fraction as Q
rp=panel();cen={t:tuple(Q(str(round(float(a),9))) for a in p) for t,p in rp.cen.items()};pos={v:tuple(Q(str(float(a))) for a in p) for v,p in xy.items()};dv=(Q(1,7),Q(1))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def ray(w,t,v):
 a=cen[t];e=sub(pos[v],a);d=cross(dv,e)
 if not d:return None
 lam=cross(sub(a,cen[w]),e)/d;mu=cross(sub(a,cen[w]),dv)/d
 if lam>0 and 0<mu<1:return lam
 return None
def dc(r,s):
 succ={a:b for a,b in zip(r,s)};seen=set();cs=[]
 for v in sorted(succ):
  if v in seen:continue
  cy=[];u=v
  while u not in seen:seen.add(u);cy.append(u);u=succ[u]
  cs.append([r.index(u) for u in cy])
 return cs
def crosses(r,s,cy,w):
 return sorted((lam,i,k) for i in cy for k,z in enumerate((r,s)) if (lam:=ray(w,A[i],z[i])) is not None)
found=None
for rr,ss in P:
 for cy in dc(rr,ss):
  for w0 in W:
   rl=crosses(rr,ss,cy,w0)
   for k,(la,i,kind) in enumerate(rl):
    if kind!=1 or len(rl)<2 or (len(rl)%2 and k==0):continue
    partner=k^1 if len(rl)%2==0 else ((k-1)^1)+1
    if partner>=len(rl):continue
    found=(rr,ss,cy,w0,rl,k,partner);break
   if found:break
  if found:break
 if found:break
assert found
rr,ss,cy,w0,rl,k,partner=found;_,ii,kind=rl[partner];rr2=list(rr);ss2=list(ss)
if kind==0:
 for i in cy:rr2[i],ss2[i]=ss[i],rr[i]
rr2,ss2=tuple(rr2),tuple(ss2);assert (rr2,ss2) in P
rl2=crosses(rr2,ss2,cy,w0);assert rl2[partner][2]==1
back=partner^1 if len(rl2)%2==0 else ((partner-1)^1)+1;assert back==k
cells=[]
for tag,r0,s0,mark in [('a',rr,ss,k),('b',rr2,ss2,partner)]:
 pp=panel(unit=.68).base()
 # All selected spokes have different dash patterns as well as colour.
 for i,t in enumerate(A):
  pp.add(rf'\draw[draw=bfR,line width=.9pt,dashed] {pt(pp.cen[t])} -- {pt(xy[r0[i]])};');pp.add(rf'\draw[draw=bfS,line width=1pt] {pt(pp.cen[t])} -- {pt(xy[s0[i]])};')
 pp.vertices();origin=np.array(list(map(float,cen[w0])));dd=np.array(list(map(float,dv)));endpoint=origin+dd*float(max(v[0] for v in rl)+Q(1,2));pp.add(rf'\draw[line width=1pt,->,dash pattern=on 4pt off 2pt] {pt(origin)} -- {pt(endpoint)};');pp.label(origin-np.array([.35,.25]),rf'$w_{{{w0}}}$','af lab')
 for n,(lam,i,ki) in enumerate(rl):
  cp=origin+float(lam)*dd;pp.add(rf'\draw[fill=white,line width={1.5 if n==mark else .6}pt] {pt(cp)} circle[radius={3.8 if n==mark else 2}pt];');pp.label(cp+np.array([.45 if n%2 else -.45,.04]),str(n+1),'af lab')
 cells.append(cell(pp.tex(),rf'({tag}) Pair $(s_{{{names[r0]}}},s_{{{names[s0]}}})$. The ring marks crossing {mark+1} of {len(rl)}. '+('For an even list, pair consecutive crossings; for an odd list, leave the first and pair the rest.' if tag=='a' else ('The selected spoke was $r$, so reverse this component to make it an $s$ spoke.' if kind==0 else 'The selected spoke was already $s$, so keep the pair.')),7.6))
compile('p06-rays',r'\begin{tabular}{cc}'+' & '.join(cells)+r'\\[3mm]\multicolumn{2}{c}{\footnotesize Dashed $r$ spokes, solid $s$ spokes; ray crossings ordered from the white point. One token shown.}\\\multicolumn{2}{c}{\footnotesize Other tokens can be held fixed. This panel illustrates the crossing-pairing case, not the whole marked set.}\end{tabular}')
(O/'rays.json').write_text(json.dumps(dict(pair=[names[rr],names[ss]],image=[names[rr2],names[ss2]],white=w0,ray=list(map(str,dv)),crossings=[[str(l),A[i],kind] for l,i,kind in rl],chosen=k,partner=partner,involutive=True),indent=2))
# Fill the white band on pages 16 and 25 with computed explanatory additions.
c=C['canonical'];cm=Model(c['faces'],c['t0']);zs=enum(cm.F,cm.A,cm.X);qgood=[z for z in zs if nx.is_forest(qgraph(z,cm.F,cm.A,cm.V)) and all(len(set(cc)&set(cm.roots))==1 for cc in nx.connected_components(qgraph(z,cm.F,cm.A,cm.V)))];assert len(zs)==9 and len(qgood)==8
compile('p16-count-strip',r'\begin{minipage}{14.5cm}\centering\large $9\text{ states}\quad=\quad8\text{ good}\quad+\quad1\text{ cyclic}$\par\smallskip\normalsize The unique cyclic state sits at the partnered extreme. Its three opposite edges surround one white triangle. Choosing an extreme by height therefore need not choose a good state. Reflecting the embedding reverses the height order.\end{minipage}')
compile('p25-count-strip',r'\begin{tikzpicture}[bf]\draw[very thick] (0,0) rectangle (14,1.1);\draw[very thick] (7,0)--(7,1.1);\draw[dashed,very thick] (3.5,0)--(3.5,1.1);\node at (1.75,.55) {2 produced};\node at (5.25,.55) {2 missed};\node at (10.5,.55) {4 use $e$};\node at (3.5,1.5) {4 avoid $e$};\node at (7,-.5) {8 Hamiltonian cycles of the hexagonal prism};\end{tikzpicture}')
