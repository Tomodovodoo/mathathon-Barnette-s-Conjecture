from pathlib import Path
import re,json,subprocess
from check import Paths,Check,ROOT,OUT,enumerate_classes,from_code
D=ROOT/'proofs/involutions';F=D/'figures'
rays=r'\draw[bfW,densely dashed,thin] (-0.112,-1.905) -- (-3.353,3.709);'+'\n'+r'\draw[bfW,densely dashed,thin] (-0.849,-0.317) -- (-3.234,3.813);'+'\n'
for name in ('marked','second'):
    s=subprocess.check_output(['git','show','55e60f9:proofs/involutions/figures/'+name+'.tex'],cwd=ROOT,text=True).replace(r'\tiny',r'\footnotesize')
    s=s.replace(r'\node[draw=bfW,circle,fill=white,inner sep=1pt,font=\footnotesize] at (-0.112,-1.905)',rays+r'\node[draw=bfW,circle,fill=white,inner sep=1pt,font=\footnotesize] at (-0.112,-1.905)')
    panels=re.findall(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',s,re.S)
    def zoom(p):
        return p.replace('x=0.42cm,y=0.42cm','x=1.45cm,y=1.45cm').replace(r'\path[use as bounding box] (-5.80,-5.80) rectangle (5.80,5.80);',r'\path[use as bounding box] (-2.6,-2.2) rectangle (1.0,2.3);\clip (-2.6,-2.2) rectangle (1.0,2.3);')
    if name=='marked':out=re.sub(r'\\node\[.*?\] at .*?;','',panels[0])+r'\qquad'+zoom(panels[0])
    else:out=zoom(panels[0])+r'\quad$\longleftrightarrow$\quad'+zoom(panels[1])
    (F/(name+'.tex')).write_text(out)
f=F/'first.tex';f.write_text(f.read_text().replace(r'\tiny',r'\footnotesize'))
d=json.loads((D/'running.json').read_text());fs=[tuple(f) for f in d['faces']];b=Check(fs,d['t0'])
o=next(o for o in b.objects(2) if b.two(o)!=o and len({w for w,i in o[1]})==2)
rows=json.loads((D/'running-objects.json').read_text());keys=[(tuple(map(tuple,r['pair'])),tuple(map(tuple,r['marks']))) for r in rows]
assert keys[rows[keys.index(o)]['iota2']]==b.two(o)
levels=enumerate_classes(12);T=from_code(levels[12][6]);b1=Check(T.faces,8);o1=next(o for o in b1.objects(1) if b1.one(o)!=o)
assert b1.one(b1.one(o1))==o1
p=Paths(fs,d['t0']);po=next(o for o in p.objects(2) if p.two(o)!=o and len({w for w,i in o[1]})==2);pq=p.two(po);assert p.two(pq)==po
lines=[r'\begin{tikzpicture}[bf,x=1.6cm,y=1cm]']
for row,(w,i) in enumerate(po[1]):
    for j,f in enumerate(p.paths[w]):
        style='draw,rectangle,fill=bfblack' if f in p.a else 'draw,circle,fill=white'
        if f==p.a[i]:style+=',very thick,draw=bfW'
        lines.append(rf'\node[{style}] (n{row}{j}) at ({j},{-row*1.8}) {{$f_{{{f}}}$}};')
        if j:lines.append(rf'\draw[-{{Stealth}}] (n{row}{j-1}) -- (n{row}{j});')
        if f in p.a and (w,p.a.index(f)) in p.turns:
            step,v,kap=p.turns[w,p.a.index(f)]
            lines.append(rf'\node at ({j},{-row*1.8-.55}) {{$v={v},\ \kappa={kap:+d}$}};')
lines.append(r'\end{tikzpicture}');(F/'paths.tex').write_text('\n'.join(lines))
(OUT/'figure-data.json').write_text(json.dumps(dict(command='python research/2026-11-14_sol_involutions-revision/code/figures.py',ray=dict(object=o,image=b.two(o),id=keys.index(o)),first=dict(object=o1,image=b1.one(o1)),paths=dict(object=po,image=pq,path_faces={w:p.paths[w] for w,i in po[1]},turns={str((w,i)):p.turns[w,i] for w,i in po[1]})),indent=1,default=str))
(F/'panels.tex').write_text(r'''
\clearpage
\begin{figure}[p]\centering\input{figures/marked.tex}
\caption{A computed marked pair in the running example. Left: the cover. Right: a zoom of its marked spokes. Dashed lines are the rays from $w_5$ and $w_6$, in the direction that is vertical in the exact layout. Thick spokes carry the tokens; blue arrows show $D$.}\end{figure}
\begin{figure}[p]\centering\input{figures/second.tex}
\caption{The second move on the same object, before and after, in the zoomed region. Both rays are drawn. The token moves to its partner crossing; its cycle reverses when the partner is an $r$-spoke.}\end{figure}
\clearpage
\begin{figure}[p]\centering\input{figures/paths.tex}
\caption{Drawing-free marks on the same triangulation. Each row is a tree path from its white face to the outer face $f_4$. Squares are bounded black faces; circles are white faces or the outer face. A thick green square is a marked step. Labels give the turned corner and its turn sign; the selected corner equals the turned corner at every marked step. Face IDs follow \texttt{running.json}.}\end{figure}
\begin{figure}[p]\centering\input{figures/first.tex}
\caption{The first move on class 6, root 8, with 12 vertices. The second state and its token stay fixed while the opposite-edge cycle reverses. Blue arrows show $D$. This panel illustrates the state change.}\end{figure}
\clearpage
''')
