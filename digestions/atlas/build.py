"""Recompute all atlas objects; import the paper toolkit without writing to it.
Run from the repository root: python digestions/atlas/build.py
"""
import os, sys, json, math, itertools as it, subprocess, hashlib
from pathlib import Path
from collections import defaultdict, Counter
sys.dont_write_bytecode = True
O = Path(__file__).resolve().parent
ROOT = O.parents[1]
FIG = ROOT/'paper/figures'
sys.path[:0] = [str(FIG), str(ROOT/'workings/barnette_lab')]
import numpy as np
import networkx as nx
import sympy as sp
import fitz
from PIL import Image, ImageOps, ImageDraw
from scipy.optimize import linprog
import check, draw
from model import Model, und, dual_of_cubic
from model import oriented_faces
from barnette_lab.core import Instance

def plain(x):
    if isinstance(x, dict): return {str(k):plain(v) for k,v in x.items()}
    if isinstance(x, (list,tuple,set)): return [plain(v) for v in x]
    if isinstance(x, np.ndarray): return x.tolist()
    if isinstance(x, (np.integer,np.floating)): return x.item()
    if isinstance(x, sp.Integer): return int(x)
    return x

def dump(name,x): (O/name).write_text(json.dumps(plain(x),indent=2),encoding='utf8')

run = check.running(); oc = check.octahedron()
m,xy,R = run['model'],run['xy'],run['R']
states=m.states(); pairs=m.pairs(states); r,s=run['r'],run['s']; rec=run['rec']
sid={z:i for i,z in enumerate(states)}
eps=lambda a,b: math.prod(m.delta(u,v) for u,v in zip(a,b))
trees={z for z in states if m.Q_is_forest(z) and any(b==z for a,b in pairs)}

# Independently enumerate the same labelled triangulation with barnette_lab.
b=Instance(m.T); outer=next(i for i,f in enumerate(b.faces) if set(f)==set(m.roots)); b=Instance(m.T,outer)
fid={frozenset(f):i for i,f in enumerate(m.F)}
def labstate(z):
    choices=dict(zip(m.A,z)); return tuple(choices[fid[frozenset(b.faces[t])]] for t in b.A)
assert set(labstate(z) for z in states)==set(b.states())
assert set((labstate(a),labstate(z)) for a,z in pairs)==set(b.pairs(list(b.states())))
lc=b.recover(labstate(r),prescribed=m.e0)
assert set(map(tuple,rec['P']))==set(map(tuple,lc['P']))

# Face-potential coordinates in the embedded spoke graph H0. This computes
# heights, rather than assigning ranks by eye. The exterior face has height 0.
spokes=[(t,v) for t in m.A for v in m.F[t]]; index={e:i for i,e in enumerate(spokes)}
inner=[w for w in m.white if all(m.black_face(u,v)!=m.t0 for u,v in zip(m.F[w],m.F[w][1:]+m.F[w][:1]))]
C=sp.zeros(len(spokes),len(inner))
for j,w in enumerate(inner):
    f=m.F[w]
    for u,v in zip(f,f[1:]+f[:1]):
        t=m.black_face(u,v); C[index[t,v],j]+=1; C[index[t,u],j]-=1
def vec(z): return sp.Matrix([int(z[m.A.index(t)]==v) for t,v in spokes])
def heights(v):
    h=list(C.gauss_jordan_solve(v)[0]); assert all(z.q==1 for z in h); return tuple(map(int,h))
hs=[heights(vec(z)-vec(states[0])) for z in states]
minimum=tuple(min(h[j] for h in hs) for j in range(len(inner)))
hs=[tuple(v-a for v,a in zip(h,minimum)) for h in hs]
def covers(hh):
    order=nx.DiGraph(); order.add_nodes_from(range(len(hh)))
    for i,a in enumerate(hh):
        for j,z in enumerate(hh):
            if i!=j and all(u<=v for u,v in zip(a,z)): order.add_edge(i,j)
    return nx.transitive_reduction(order)
state_order=covers(hs)
factors={}
for a,z in pairs:
    key=tuple(sorted(und(u,v) for u,v in zip(a,z)))
    factors.setdefault(key,[]).append((a,z))
groups=list(factors.values())
ph=[heights(vec(a)+vec(z)-vec(groups[0][0][0])-vec(groups[0][0][1])) for (a,z),*rest in groups]
pair_order=covers(ph)

# Integer polynomial, using the linear substitution of the referee.
a=run['spoke_weights']; x=sp.Symbol('x')
aa={e:sp.Rational(float(w)).limit_denominator(100000) for e,w in a.items()}
assert all(sum(C[i,j]*aa[e] for i,e in enumerate(spokes))==1 for j in range(len(inner)))
P=sp.expand(sum(eps(u,v)*sp.prod(1+x*aa[t,z] for t,z in zip(m.A,v)) for u,v in pairs))
termdata=[{'r':sid[u],'s':sid[v],'J':m.J(u,v),'sign':eps(u,v),'omega':str(sum(aa[t,z] for t,z in zip(m.A,v)))} for u,v in pairs]

# Three-matroid relaxation. The same matching variables select opposite edges.
choices=[(t,v) for t in m.A for v in m.F[t] if v in m.X]
qedges=[tuple(0 if u in m.roots else 1+m.X.index(u) for u in m.F[t] if u!=v) for t,v in choices]
Aeq=np.array([[int(tt==t) for tt,v in choices] for t in m.A]+[[int(vv==v) for t,vv in choices] for v in m.X],float)
Aub=[]; rhs=[]
for mask in range(1,1<<(len(m.X)+1)):
    if mask.bit_count()<2: continue
    row=[int((mask>>u&1) and (mask>>v&1)) for u,v in qedges]
    if any(row): Aub.append(row); rhs.append(mask.bit_count()-1)
Aub=np.array(Aub,float); rhs=np.array(rhs,float)
rng=np.random.default_rng(714); lp=None
for trial in range(250):
    sol=linprog(rng.normal(size=len(choices)),A_ub=Aub,b_ub=rhs,A_eq=Aeq,b_eq=np.ones(2*len(m.A)),bounds=(0,1),method='highs')
    assert sol.success
    if any(abs(v-round(v))>1e-7 for v in sol.x): lp=sol.x; break
if lp is not None:
    exact=[sp.Rational(float(v)).limit_denominator(1000) for v in lp]
    assert all(v in (0,sp.Rational(1,2),1) for v in exact)
    assert sp.Matrix(Aeq.astype(int))*sp.Matrix(exact)==sp.ones(2*len(m.A),1)
    assert all(sum(int(v)*z for v,z in zip(row,exact))<=int(y) for row,y in zip(Aub,rhs))
    active=list(Aeq)+[row for row,y in zip(Aub,rhs) if abs(row@lp-y)<1e-8]
    active += [np.eye(len(lp))[i] for i,v in enumerate(lp) if min(abs(v),abs(v-1))<1e-8]
    assert sp.Matrix(np.array(active).astype(int)).rank()==len(lp)
else: exact=[]

# Hexagonal prism. Use its own dual numbering and record the change of example.
hm=Model(dual_of_cubic(nx.circular_ladder_graph(6)),0)
hstates=hm.states(); hpairs=hm.pairs(hstates)
himages={frozenset(und(*e) for e in hm.recover(z)['hamiltonian']) for z in hstates if hm.Q_is_forest(z) and any(v==z for u,v in hpairs)}
hall=[frozenset(und(*e) for e in q) for q in hm.two_factors(1)]
assert (len(hstates),len(hpairs),len(himages),len(hall))==(3,2,2,8)
badchoices=[]
for z in it.product(*[[v for v in hm.F[t] if v in hm.X] for t in hm.A]):
    Q=hm.Q_graph(z)
    if nx.is_forest(Q) and all(len(set(c)&set(hm.roots))==1 for c in nx.connected_components(Q)) and not hm.is_state(z): badchoices.append(z)
assert len(badchoices)==4

# Canonical-choice witness from the submission, independently rechecked here.
import ast
ct=(ROOT/'research/2026-11-14_fable_route-combinatorics/data/counterexamples.txt').read_text()
cf=ast.literal_eval(ct.split('faces (counterclockwise):\n')[1].splitlines()[0].strip())
cm=Model(cf,8); cs=(0,4,1,5,8,9,11,6,10)
assert cm.is_state(cs) and not cm.Q_is_forest(cs)
assert len(cm.V)==12 and len(cm.states())==9 and len(cm.pairs())==10

# Cube boundary restrictions from every Hamiltonian cycle, modulo exchanging labels.
om=oc['model']; oh=om.two_factors(1)
def partitions(model):
    out=[]
    for cyc in model.two_factors(1):
        blocked={und(*model.cross[und(*g)]) for g in cyc}
        f=model.T.copy(); f.remove_edges_from(blocked)
        parts=list(nx.connected_components(f)); assert len(parts)==2
        out.append({v:int(v not in parts[0]) for v in model.V})
    return out
oparts=partitions(om)
tri=list(om.F[om.t0]); quad=next(c for c in nx.cycle_basis(om.T) if len(c)==4) if any(len(c)==4 for c in nx.cycle_basis(om.T)) else None
if quad is None:
    quad=next(list(q) for q in it.permutations(om.V,4) if min(q)==q[0] and all(om.T.has_edge(u,v) for u,v in zip(q,q[1:]+q[:1])))
def boundary(c):
    return sorted({tuple(p[v]^p[c[0]] for v in c) for p in oparts})
bt,bq=boundary(tri),boundary(quad)

certificate={'command':'python digestions/atlas/build.py','counts':run['counts'],'lab_agrees':True,'states':states,'pairs':termdata,'white_faces':inner,'heights':hs,'state_covers':list(state_order.edges()),'pair_heights':ph,'pair_covers':list(pair_order.edges()),'groups':[[[sid[u],sid[v]] for u,v in g] for g in groups], 'linear_polynomial':str(P),'lp':{'choices':choices,'x':list(map(str,exact)),'active_rank':len(choices) if exact else None,'trials':trial+1},'hex_prism':{'states':hstates,'bad_two_matroid_choices':badchoices,'images':len(himages),'cycles':len(hall)},'cube_boundary':{'triangle':tri,'patterns3':bt,'quadrilateral':quad,'patterns4':bq}}
dump('computed.json',certificate)
dump('examples.json',{'running':{'faces':m.F,'t0':m.t0,'e0':m.e0,'coordinates':xy,'R':R},'cube':{'faces':om.F,'t0':om.t0},'hex_prism':{'faces':hm.F,'t0':hm.t0},'canonical_witness':{'faces':cm.F,'t0':cm.t0,'state':cs}})

def panel(model=m,pos=xy,radius=R,unit=1.05): return draw.Panel(model,pos,radius,unit=unit)
def graph(kind):
    p=panel().base()
    if kind=='pair': p.state(r,'bf r').state(s).arrows(m.D(r,s))
    elif kind=='forest': p.state(r).lines(m.Q(r),'bf Q')
    elif kind=='cyclic': p.state(s).lines(m.Q(s),'bf Q')
    elif kind=='white': p.spokes(deleted=list(zip(m.A,r)),outer=True).white_tree(rec,r)
    elif kind=='recover': p.lines(rec['P'],'bf P').graphG('bf cycle',rec['hamiltonian'],dots=False).vertices(classes=rec['parts']); return p.tex()
    elif kind=='primal': p.graphG(dots=False).graphG('bf cycle',rec['hamiltonian'],dots=False).dotsG()
    p.vertices(); return p.tex()
def tikz(lines): return '\\begin{tikzpicture}[bf,x=1cm,y=1cm]\n'+'\n'.join(lines)+'\n\\end{tikzpicture}'
def table(head,rows):
    return '\\begin{tabular}{'+'c'*len(head)+'}\\hline\n'+' & '.join(head)+r'\\\hline'+'\n'+'\n'.join(' & '.join(map(str,row))+r'\\' for row in rows)+ '\n\\hline\\end{tabular}'
def lattice(hh,g,marked):
    rank=[sum(h) for h in hh]; levels=defaultdict(list)
    for i,v in enumerate(rank): levels[v].append(i)
    pos={i:((j-(len(ids)-1)/2)*1.45,(v-min(rank))*1.10) for v,ids in levels.items() for j,i in enumerate(ids)}
    lines=[]
    for i,j in g.edges(): lines.append(rf'\draw[bf edge] {draw.pt(pos[i])} -- {draw.pt(pos[j])};')
    for i,p in pos.items():
        extreme=g.in_degree(i)==0 or g.out_degree(i)==0
        opts='draw=black,fill=white,minimum size=6mm,circle'
        if i in marked: opts='draw=bfW,fill=white,minimum size=6mm,rectangle,line width=1pt'
        lines.append(rf'\node[{opts}] at {draw.pt(p)} {{$ {i} $}};')
        if extreme: lines.append(rf'\draw[line width=.7pt] {draw.pt(p)} circle[radius=.47];')
    return tikz(lines)

def diskpic(mode):
    k=run['disk']; p=panel().base(tint={f:('bfR!12!bfblack' if f in m.black else 'bfR!7') for f in k['black']+k['white']})
    p.arrows(list(zip(k['cycle'],k['cycle'][1:]+k['cycle'][:1])))
    if mode=='count':
        p.state(r)
        for v in k['interior']: p.label(xy[v]+np.array([.25,.25]),'$I$')
    elif mode=='white':
        for f in k['black']: p.label(p.cen[f],'$B$')
        for f in k['white']: p.label(p.cen[f],'$W$')
    else:
        cyc=k['cycle']
        for j,v in enumerate(cyc):
            prev=cyc[j-1]; nxt=cyc[(j+1)%len(cyc)]
            turn=(m.delta(prev,v)+m.delta(v,nxt))/2-3*m.delta(v,nxt)
            p.label(xy[v]*1.08,rf'${turn:g}$',opts='fill=white')
    p.vertices(); return p.tex()

def heightpic():
    p=panel().base().state(r)
    h=hs[sid[r]]
    for j,w in enumerate(inner): p.label(p.cen[w],rf'${h[j]}$',opts='fill=white,rounded corners=1pt')
    p.vertices(); return p.tex()

def matrixpic():
    # Rows are signed endpoint incidences of the selected Q edges, roots removed.
    N=sp.zeros(len(m.A),len(m.X))
    for i,(t,v) in enumerate(zip(m.A,s)):
        ends=[u for u in m.F[t] if u!=v]
        for u in ends:
            if u in m.X: N[i,m.X.index(u)]=m.delta(u,v)
    assert N.det()==0
    ker=N.T.nullspace()[0]; assert N.T*ker==sp.zeros(len(m.X),1)
    dump('incidence.json',{'rows':m.A,'columns':m.X,'matrix':N.tolist(),'dependence':list(map(str,ker))})
    return r'$\displaystyle d_s='+sp.latex(N)+r'$'+r'\par\medskip $\displaystyle c='+sp.latex(ker.T)+r',\qquad c d_s=0.$'

def lp_pic():
    if not exact: return r'No fractional vertex found in the specified 250 objectives. This page records a failed search, not integrality.'
    p=panel().base()
    for (t,v),val in zip(choices,exact):
        if val:
            p.wedge(t,v,'bf s' if val==1 else 'bf r')
    p.vertices(); return p.tex()+r'\par Solid blue $=1$; outlined vermilion $=\frac12$; absent $=0$.'

def prism_picture(cycles):
    # Relabel face-centre vertices to the actual circular ladder by graph isomorphism.
    G=nx.circular_ladder_graph(6); iso=next(nx.isomorphism.GraphMatcher(hm.G,G).isomorphisms_iter())
    lines=[]
    for j,cyc in enumerate(cycles):
        center=j*5.7
        pos={v:(center+(2 if v<6 else 1)*math.cos(2*math.pi*(v%6)/6), (2 if v<6 else 1)*math.sin(2*math.pi*(v%6)/6)) for v in G}
        for u,v in G.edges(): lines.append(rf'\draw[bf G] {draw.pt(pos[u])} -- {draw.pt(pos[v])};')
        for u,v in cyc: lines.append(rf'\draw[bf cycle] {draw.pt(pos[iso[u]])} -- {draw.pt(pos[iso[v]])};')
        for v in G: lines.append(rf'\draw[fill={"black" if (v%6+v//6)%2==0 else "white"}] {draw.pt(pos[v])} circle[radius=1.5pt];')
        lines.append(rf'\node at ({center},-2.5) {{{"produced" if j==0 else "missed"}}};')
    return tikz(lines)

def boundarypic():
    lines=[]
    for y,(c,patterns) in enumerate([(tri,bt),(quad,bq)]):
        for j,pattern in enumerate(patterns):
            pos=[(j*1.75+.59*math.cos(2*math.pi*k/len(c)), -y*2.15+.59*math.sin(2*math.pi*k/len(c))) for k in range(len(c))]
            for k in range(len(c)): lines.append(rf'\draw[bf edge] {draw.pt(pos[k])} -- {draw.pt(pos[(k+1)%len(c)])};')
            for p,z in zip(pos,pattern): lines.append(rf'\node[draw,fill={"black" if z==0 else "white"},circle,minimum size=4pt,inner sep=0pt] at {draw.pt(p)} {{}};')
    return tikz(lines)

def chart():
    # Counts directly recomputed, rather than copying the large-family tables.
    data=[]
    for p in (4,6,8,10,12):
        model=Model(dual_of_cubic(nx.circular_ladder_graph(p)),0); ss=model.states(); ps=model.pairs(ss)
        data.append((p,len(ss),len(ps),len(model.two_factors(1))))
    dump('prism-counts.json',{'command':'python digestions/atlas/build.py','rows':data})
    lines=[]
    for j,(label,col,k,dash) in enumerate([('states','bfS',1,''),('ordered pairs','bfR',2,'dashed'),('Hamiltonian cycles','bfH',3,'dash dot')]):
        pts=[((p-4)*.65,math.log2(row[k])*.6) for row in data for p in [row[0]]]
        lines.append(rf'\draw[draw={col},line width=1pt,{dash}] '+' -- '.join(draw.pt(p) for p in pts)+';')
        for px,py in pts: lines.append(rf'\node[draw={col},fill=white,rectangle,minimum size=3pt,inner sep=0pt] at ({px},{py}) {{}};')
        lines.append(rf'\node[anchor=west,text={col}] at (5.5,{3.5-j*.5}) {{{label}}};')
    lines.append(r'\draw[->] (-.3,0)--(5.4,0) node[right] {$p$};\draw[->] (-.3,0)--(-.3,3) node[above] {$\log_2$ count};')
    for p,*_ in data: lines.append(rf'\node[anchor=north] at ({(p-4)*.65},0) {{{p}}};')
    for exponent in range(1,5): lines.append(rf'\node[anchor=east] at (-.3,{exponent*.6}) {{{exponent}}};')
    # A separate directly enumerated nanotube comparison, width 4, L=0..3.
    tube=[]
    for L in range(4):
        p=4; g=nx.Graph(); A=p*(L+1); B=A+1
        for j in range(L+1):
            for i in range(p): g.add_edge(j*p+i,j*p+(i+1)%p)
        for j in range(L):
            for i in range(p):
                g.add_edge(j*p+i,(j+1)*p+i)
                if i%2==0: g.add_edge(j*p+i,(j+1)*p+(i+1)%p)
                else: g.add_edge(j*p+(i+1)%p,(j+1)*p+i)
        for i in range(p): g.add_edge(A,i); g.add_edge(B,L*p+i)
        fs=oriented_faces(g); root={A,0,1} if L==0 else {0,1,p+1}
        mod=Model(fs,next(i for i,f in enumerate(fs) if set(f)==root))
        ss=mod.states()
        tm=sum(mod.Q_is_forest(z) and all(len(set(c)&set(mod.roots))==1 for c in nx.connected_components(mod.Q_graph(z))) for z in ss)
        tube.append([L,len(ss),tm])
    dump('nanotube-counts.json',{'command':'python digestions/atlas/build.py','width':4,'rows':tube})
    assert tube==[[0,2,2],[1,5,2],[2,13,2],[3,34,2]],tube
    return tikz(lines)+r'\par\bigskip Width-four nanotubes, direct enumeration:\par '+table(['layers $L$','states','tree matchings'],tube)

def metro():
    names=['cut criterion','disjoint states','disk identity','cyclic terms cancel','positive lowest term','forest state','white-face tree','two induced trees','Hamiltonian cycle']
    lines=[]
    for i,label in enumerate(names):
        x0=0 if i<5 else 6.8; y0=5-i*1.05 if i<5 else .8+(i-5)*1.05
        if i and i!=5: lines.append(rf'\draw[draw=bfS,line width=1.5pt] ({x0},{y0+(1.05 if i<5 else -1.05)})--({x0},{y0});')
        lines.append(rf'\node[draw=bfS,circle,fill=white,minimum size=5pt,inner sep=0pt] at ({x0},{y0}) {{}};\node[anchor=west] at ({x0+.2},{y0}) {{{label}}};')
    lines.append(r'\draw[draw=bfS,line width=1.5pt,->] (0,.8)--(0,.2)--(6.8,.2)--(6.8,.8);')
    return tikz(lines)

def two_views(p1,p2,l1,l2):
    return draw.row([p1,p2],[l1,l2],sep='7mm')

def li_picture():
    def p(z): return panel(unit=.42).base().state(z,'bf r').state(s).lines(m.Q(s),'bf Q').vertices().tex()
    # The cube needs only one mark, so its exact ray involution is reviewable.
    from barnette_lab.li import LiObjects
    bb=Instance(om.T); bb=Instance(om.T,next(i for i,f in enumerate(bb.faces) if set(f)==set(om.roots)))
    lo=LiObjects(bb); pp=list(bb.pairs(list(bb.states()))); objects=list(lo.objects(pp)); universe=set(objects)
    fixed=[]
    for obj in objects:
        for invol in (lo.iota1,lo.iota2):
            partner=invol(obj); assert partner in universe and invol(partner)==obj
            if partner!=obj: assert lo.sign(partner)!=lo.sign(obj)
        if lo.iota2(obj)==obj: fixed.append(obj)
    assert len(set(lo.sign(obj) for obj in fixed))==1
    dump('li-cube.json',{'command':'python digestions/atlas/build.py','objects':len(objects),'iota1_fixed':sum(lo.iota1(obj)==obj for obj in objects),'iota2_fixed':len(fixed),'all_involutions_and_signs_checked':True})
    moving=next(obj for obj in objects if lo.iota2(obj)!=obj); mate=lo.iota2(moving)
    def token(obj):
        pair,(w,t)=obj
        return rf'$p_{{{pp.index(pair)}}},\ (y_{{{w}}},t_{{{t}}}),\ \mathrm{{sign}}={(-1)**lo.sign(obj)}$'
    return two_views(p(r),p(run['r2']),r'$(r,s)$',r'$(\widetilde r,s)$')+r'\par First involution: the second state stays fixed.'+r'\par\medskip Cube second involution, exact ray-intersection marks:\par '+token(moving)+r'$\quad\longleftrightarrow\quad$'+token(mate)+rf'\par {len(objects)} marked objects, {len(fixed)} second-involution fixed objects.'

def terms_picture():
    rows=[[f'$({d["r"]},{d["s"]})$',d['J'],d['sign'],d['omega']] for d in termdata]
    grouped=defaultdict(list)
    for d in termdata: grouped[d['s']].append(d['sign'])
    txt=two_views(panel(unit=.40).base().state(r,'bf r').state(s).arrows(m.D(r,s)).vertices().tex(),table(['pair','$J$',r'$\epsilon$',r'$\omega(s)$'],rows),'the running pair','all eight terms')
    txt+=r'\par\medskip Fixed second state: '+', '.join(rf'${i}\mapsto {sum(signs)}$' for i,signs in sorted(grouped.items()))+'.'
    txt+=r'\par Undirected $D$ groups: '+', '.join(rf'$D_{i}$ has {len(g)} orientations and {len(m.directed_cycles(m.D(*g[0])))} cycles' for i,g in enumerate(groups))+'.'
    txt+=r'\par $Z(x)=\sum i^J e^{x\omega(s)}$; multiplying by $i^n$ gives the real signs above.'
    return txt

def alphapic():
    pics=[]
    for i,g in enumerate(groups):
        u,z=g[0]
        pics.append(panel(unit=.42).base().state(u,'bf r').state(z).arrows(m.D(u,z)).vertices().tex())
    return two_views(*pics,*[f'$D_{i}$: {len(g)} ordered orientations' for i,g in enumerate(groups)])+r'\par\bigskip'+lattice(ph,pair_order,{i for i,g in enumerate(groups) if any(v in trees for u,v in g)})+r'\par Green square: a tree orientation exists. Ring: an extreme.'

def clockpic():
    diagram=lattice(hs,state_order,{sid[z] for z in trees})
    # One compact lookup table makes the node numbering self-contained.
    lookup=table(['state','choices in face order'],[[i,r'$'+','.join(map(str,z))+'$'] for i,z in enumerate(states)])
    return two_views(diagram,lookup,'clock order','face order '+','.join(map(str,m.A)))+r'\par Green squares: tree matchings. Rings: extrema.'

def linear_picture():
    assert sp.Poly(P,x).nth(2)==9 and sp.Poly(P,x).nth(0)==sp.Poly(P,x).nth(1)==0
    return graph('pair')+r'\par $F(1+xa)=9x^2-\frac{2563}{4056}x^3+O(x^4)$, of degree ten.'+r'\par Exact coefficients are recorded in computed.json.'

def determinantpic():
    return r'''\begin{minipage}{.97\linewidth}\centering
    $\displaystyle F(w)=[\prod_{t\in A}y_t]\det N(y,w)$
    \par\bigskip Extracting the coefficient uses each triangle once.
    \par\bigskip $\displaystyle\det M(y,1)=\frac{5y_0y_1y_4}{64}
    (-4y_0y_3-5y_1y_2+9y_2y_3)$
    \par\bigskip Hexagonal prism, number-field normalization from the source.
    \par $\det M(1,1)=0$, although two tree matchings exist.
    \end{minipage}'''

def doublepic():
    p=panel(om,oc['xy'],oc['R'],unit=1.05).base()
    z=oc['s']; assert om.is_state(z)
    for t,v in zip(om.A,z):
        p.add(rf'\draw[bf kept,double=white,double distance=1pt] {draw.pt(p.cen[t])} -- {draw.pt(p.xy[v])};')
    p.spokes(style=None,kept=None).vertices()
    return p.tex()+r'\par Cube dual. Both copies choose the same checked state; every bold spoke has multiplicity two.'

def model_layout(model):
    rr=list(model.roots); radius=4.5
    angles={model.e0[0]:210,model.e0[1]:330}
    if model.left[model.e0]==model.t0: angles={model.e0[1]:210,model.e0[0]:330}
    angles[next(v for v in rr if v not in model.e0)]=90
    pos={v:radius*np.array([math.cos(math.radians(a)),math.sin(math.radians(a))]) for v,a in angles.items()}
    X=model.X; L=np.array([[model.T.degree(v) if u==v else -int(model.T.has_edge(u,v)) for u in X] for v in X],float)
    rhs=np.array([sum((pos[u] for u in model.T[v] if u in pos),np.zeros(2)) for v in X])
    sol=np.linalg.solve(L,rhs); pos.update(dict(zip(X,sol)))
    check.check_layout(model,pos,radius)
    return pos,radius

def matroidpic():
    z=badchoices[0]
    assert all(v in hm.F[t] for t,v in zip(hm.A,z))
    Q=hm.Q_graph(z); pos={}; lines=[]
    for j,root in enumerate(hm.roots):
        levels=defaultdict(list)
        for v,d in nx.single_source_shortest_path_length(Q,root).items(): levels[d].append(v)
        for d,vs in levels.items():
            for k,v in enumerate(sorted(vs)): pos[v]=(j*2.6+(k-(len(vs)-1)/2)*1.1,-d*1.2)
    for u,v in hm.Q(z): lines.append(rf'\draw[bf Q] {draw.pt(pos[u])} -- {draw.pt(pos[v])};')
    for v in hm.V:
        style='draw,fill=white,circle' if v in hm.roots else 'fill=black,text=white,circle'
        lines.append(rf'\node[{style},minimum size=5mm] at {draw.pt(pos[v])} {{${v}$}};')
    repeated=[v for v,k in Counter(z).items() if k>1]; missing=set(hm.X)-set(z)
    return tikz(lines)+r'\par\medskip '+table(['black face','chosen corner'],[[str(hm.F[t]),v] for t,v in zip(hm.A,z)])+r'\par Dashed opposite edges form three rooted trees. Repeated vertex '+str(repeated)+r'; missed vertex '+str(sorted(missing))+'.'

def rainbowpic():
    # Every H0 spoke has a dual edge between white regions, possibly the exterior.
    # The full white graph instead includes spokes at the root centre; the
    # atlas only exchanges bounded-face spokes, all with the same colour token t.
    candidates=[]
    for t in m.A:
        f=m.F[t]
        for v in f:
            ws=[m.white_face(v,u) for u in f if u!=v]
            candidates.append((t,v,*ws))
    selected={(t,v) for t,v in zip(m.A,r)}
    WT=nx.Graph(rec['white_tree']); swap=None
    for t,v,u,w in candidates:
        if (t,v) in selected: continue
        path=nx.shortest_path(WT,u,w)
        for g in zip(path,path[1:]):
            removed=next((tt,vv) for tt,vv,uu,ww in candidates if (tt,vv) in selected and und(uu,ww)==und(*g))
            if removed[0]!=t and removed[1]==v:
                trialtree=WT.copy(); trialtree.remove_edge(*g); trialtree.add_edge(u,w)
                assert nx.is_tree(trialtree)
                swap=dict(add=[t,v],remove=removed,added_edge=[u,w],removed_edge=g); break
        if swap: break
    assert swap
    newselected=(selected-{tuple(swap['remove'])})|{tuple(swap['add'])}
    assert Counter(v for t,v in newselected)==Counter(m.X)
    assert sorted(Counter(t for t,v in newselected).values())==[1]*8+[2]
    dump('rainbow-exchange.json',swap)
    before=panel(unit=.43).base().white_tree(rec,r).vertices()
    after=panel(unit=.43).base()
    for t,v,u,w in candidates:
        if (t,v) in (selected-{tuple(swap['remove'])})|{tuple(swap['add'])}:
            local={'chosen':{t:{'parent':u,'child':w}}}
            after.add(r'\draw[bf wtree] '+after.curve_tex(after.white_curves(local,t,v))+';')
    for w in m.white: after.add(rf'\draw[draw=bfW,fill=white] {draw.pt(after.cen[w])} circle[radius=2pt];')
    after.vertices()
    return two_views(before.tex(),after.tex(),'one token per face','after one checked tree exchange')+r'\par\medskip '+rf'$\text{{remove token }}{swap["remove"][0]}\ \longrightarrow\ \text{{insert token }}{swap["add"][0]}$'+r'\par The inserted token is repeated; the removed token is missing.'

def canonicalpic():
    pos,rad=model_layout(cm)
    # The current harmonic embedding is a checked topology; the historical
    # numbering is retained so the obstruction can be located exactly.
    return panel(cm,pos,rad,unit=1.12).base().state(cs).lines(cm.Q(cs),'bf Q').vertices(labels={4:(.4,.32),10:(-.45,.05),5:(.42,-.2)}).tex()

def morsepic():
    mates=[u for u,v in pairs if v==s]
    assert set(mates)=={r,run['r2']} and len(nx.cycle_basis(m.Q_graph(s)))==1
    return graph('cyclic')+r'\par\medskip '+rf'$r_{{{sid[r]}}},\ \epsilon={eps(r,s)}\quad\longleftrightarrow\quad r_{{{sid[run["r2"]]}}},\ \epsilon={eps(run["r2"],s)}$'+r'\par The one-dimensional Boolean cube has no unmatched vertex.'

def trinitypic():
    K=nx.Graph()
    for t,f in enumerate(om.F):
        col='b' if t in om.black else 'w'
        K.add_edges_from(((col,t),('v',v)) for v in f)
    K.add_edges_from((('b',u),('w',v)) if u in om.black else (('b',v),('w',u)) for u,v in om.G.edges())
    assert nx.is_planar(K) and len(K)==14 and K.number_of_edges()==36
    kfaces=oriented_faces(K); assert len(kfaces)==24 and all(len(f)==3 for f in kfaces)
    assert all(d%2==0 for v,d in K.degree())
    assert nx.is_isomorphic(K.subgraph([v for v in K if v[0]!='v']),om.G)
    pos=nx.planar_layout(K)
    arr=np.array(list(pos.values())); scale=11.6/(arr[:,0].max()-arr[:,0].min())
    pos={v:np.array(p)*scale for v,p in pos.items()}
    edges=list(K.edges())
    for j,(a,b) in enumerate(edges):
        for c,d in edges[j+1:]:
            if {a,b}&{c,d}: continue
            p,q,rr,ss=(pos[v] for v in (a,b,c,d))
            assert not(check.cross2(q-p,rr-p)*check.cross2(q-p,ss-p)<-1e-10 and check.cross2(ss-rr,p-rr)*check.cross2(ss-rr,q-rr)<-1e-10)
    dump('trinity.json',{'command':'python digestions/atlas/build.py','nodes':list(K.nodes()),'edges':edges,'faces':kfaces,'coordinates':pos,'layout':'networkx planar_layout, independent plane drawing of the same cube objects'})
    lines=[rf'\draw[bf edge] {draw.pt(pos[u])} -- {draw.pt(pos[v])};' for u,v in edges]
    for v,p in pos.items():
        if v[0]=='b': lines.append(rf'\fill {draw.pt(p)} ++(-2pt,-2pt) rectangle ++(4pt,4pt);')
        elif v[0]=='w': lines.append(rf'\draw[draw=bfW,fill=white,line width=.9pt] {draw.pt(p)} circle[radius=2.5pt];')
        elif v[1] in om.roots: lines.append(rf'\draw[bf root] {draw.pt(p)} circle[radius=2.3pt];')
        else: lines.append(rf'\fill {draw.pt(p)} circle[radius=1.5pt];')
    return tikz(lines)+r'\par A separate checked plane layout of the cube objects.\par Delete green circles: $H$. Delete black squares: $H\prime$. Delete old vertices: $G$.'

def obligationpic(items):
    lines=[]
    for j,(title,detail) in enumerate(items):
        x0=(j%2)*5.5; y0=-(j//2)*2.2
        lines.append(rf'\node[draw=black!40,minimum width=5cm,minimum height=1.6cm,align=center,text width=4.5cm] at ({x0},{y0}) {{\textbf{{{title}}}\\[6pt]{detail}}};')
    return tikz(lines)

# Content is kept separate so the 100--180 word explanations are easy to edit.
from pages import PAGES
special={
 'metro':metro,
 'terms':terms_picture,
 'linear':linear_picture,
 'height':heightpic, 'count':lambda:diskpic('count'),'white':lambda:diskpic('white'),'angle':lambda:diskpic('angle'),'matrix':matrixpic,
 'alpha':alphapic,
 'clock':clockpic,
 'lp':lp_pic,'boundary':boundarypic,'chart':chart,
 'coverage':lambda:prism_picture([next(iter(himages)),next(z for z in hall if z not in himages)]),
 'li':li_picture,'determinant':determinantpic,'double':doublepic,'matroids':matroidpic,'rainbow':rainbowpic,'canonical':canonicalpic,
 'morse':morsepic,'trinity':trinitypic,
 'hypotheses':lambda:obligationpic([('without bipartiteness','alternating black and white faces disappear'),('without 3-connectivity','the simple dual and cut control fail'),('on the torus','a noncontractible cycle bounds no disk'),('without bijectivity','$B=I+l$ loses its once-only count')]),
 'older':lambda:graph('recover')+r'\par Stein: two induced trees.\quad Kelmans: prescribed edge and cuts.\par Feder--Subi: quasi spanning trees after contraction, not drawn here.',
 'berezin':lambda:obligationpic([('face variables','nilpotence enforces one use per triangle'),('vertex variables','integration enforces one use per nonroot'),('local signs','anticommutation records determinant signs'),('still required','positive circulation proves nonvanishing')]),
 'open':lambda:obligationpic([('local exchange','reach a tree matching with an efficient bound'),('two lattice extremes','prove the disjunction or find a joint failure'),('contraction','inject smaller tree matchings into larger ones'),('counting',r'$\#\mathrm{TM}\geq 2^{c_{\min}}$ remains a conjecture')]),
}

def tex_escape(t):
    # Prose is deliberately plain text; formulas live in pictures or callouts.
    for c,repl in [ ('\\',r'\textbackslash{}'),('&',r'\&'),('%',r'\%'),('_',r'\_'),('#',r'\#') ]: t=t.replace(c,repl)
    return t

env=os.environ.copy(); env['TEXINPUTS']=str(FIG).replace('\\','/')+';'+env.get('TEXINPUTS','')+';'
pre=r'''\documentclass[10pt,a4paper]{amsart}
\usepackage[margin=1in]{geometry}
\usepackage{barnette-figs}
\usepackage{graphicx,amssymb}
\setlength{\parindent}{0pt}
\setlength{\parskip}{7pt}
\pagestyle{plain}
\begin{document}
'''
(O/'pages').mkdir(exist_ok=True); (O/'renders').mkdir(exist_ok=True)
allbody=[]; manifest=[]
for num,page in enumerate(PAGES,1):
    slug=page['slug']; name=f'{num:02d}-{slug}'; title=page['title']; prose=page['text']
    words=len(prose.split()); assert 100<=words<=180,(slug,words)
    kind=page['picture']; picture=special[kind]() if kind in special else graph(kind)
    # Keep an honest text-only route when an advertised object is not certified.
    if 'custom' in page: picture=page['custom']
    body=rf'\section*{{{num:02d}. {tex_escape(title)}}}'+'\n'
    body+=r'\begin{center}\begin{minipage}{.86\textwidth}\centering'+ '\n'+picture+'\n'+r'\end{minipage}\end{center}'+'\n'
    body+=tex_escape(prose)+'\n\n'+r'\textbf{Status.} '+tex_escape(page['status'])+'\n\n'
    body+=r'\textbf{Connects to.} '+tex_escape(page['connect'])+'\n\n'
    body+=r'{\footnotesize\raggedright Sources: '+tex_escape(page['source']).replace('/',r'/\allowbreak{}').replace('; ',r';\allowbreak{} ')+'\\par}\n'
    (O/'pages'/f'{name}-body.tex').write_text(body,encoding='utf8')
    (O/'pages'/f'{name}.tex').write_text(pre+body+'\n\\end{document}',encoding='utf8')
    (O/'pages'/f'{name}.md').write_text(f'# {num:02d}. {title}\n\n{prose}\n\nStatus: {page["status"]}\n\nConnects to: {page["connect"]}\n\nSources: {page["source"]}\n\nCOMPUTED figure provenance: build.py, computed.json, picture kind `{kind}`.\n',encoding='utf8')
    result=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(O/'pages'),str(O/'pages'/f'{name}.tex')],cwd=O,env=env,capture_output=True,text=True)
    if result.returncode: raise RuntimeError(result.stdout[-5000:])
    doc=fitz.open(O/'pages'/f'{name}.pdf'); assert len(doc)==1,(slug,len(doc))
    doc[0].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(O/'renders'/f'{name}.png')
    allbody.append(body); manifest.append({'number':num,'name':name,'title':title,'status':page['status'],'words':words,'connects':page['connect']})
    print('built',name,words,flush=True)
(O/'atlas.tex').write_text(pre+'\n\\clearpage\n'.join(allbody)+'\n\\end{document}',encoding='utf8')
result=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(O),str(O/'atlas.tex')],cwd=O,env=env,capture_output=True,text=True)
if result.returncode: raise RuntimeError(result.stdout[-5000:])
assert len(fitz.open(O/'atlas.pdf'))==len(PAGES)
dump('manifest.json',manifest)
# Contact sheets are QA aids; the individual 108 dpi renders are authoritative.
for start in range(0,len(PAGES),6):
    sheet=Image.new('RGB',(900,1272),'#c6c6c6')
    for k,item in enumerate(manifest[start:start+6]):
        im=Image.open(O/'renders'/f'{item["name"]}.png'); im.thumbnail((300,424))
        sheet.paste(im,((k%3)*300,(k//3)*636))
    sheet.save(O/'renders'/f'contact-{start//6+1}.png')
print('Atlas complete:',len(PAGES),'pages')

