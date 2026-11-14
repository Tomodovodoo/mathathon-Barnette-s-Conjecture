"""Generate owned tables/figures, importing the project's toolkit read-only."""
from verify import *
import shutil
import numpy as np
DEST=ROOT/'proofs/involutions'
d=json.loads((ROOT/'paper/figures/running.json').read_text())
shutil.copyfile(ROOT/'paper/figures/running.json',DEST/'running.json')
b=Check([tuple(f) for f in d['faces']],d['t0'])
res=b.run(True)
rows=json.loads((OUT/'running-objects.json').read_text())
ss=sorted(b.states);pairs=sorted(b.pairs)
body=[r'\subsection*{States and pairs}',r'Corner tuples are in black-face order $'+','.join(map(str,b.a))+r'$.',r'\begin{center}\small\begin{tabular}{rl}\toprule State & Corner tuple\\\midrule']
body += [str(i)+' & $'+','.join(map(str,s))+r'$\\' for i,s in enumerate(ss)]
body += [r'\bottomrule\end{tabular}\qquad\begin{tabular}{rrr}\toprule Pair & $r$ state & $s$ state\\\midrule']
body += [f'{i} & {ss.index(p[0])} & {ss.index(p[1])}'+r'\\' for i,p in enumerate(pairs)]
body += [r'\bottomrule\end{tabular}\end{center}',r'\small',r'\begin{longtable}{rrrrrr}\toprule Object & Pair & Tokens & Sign & $\iota_1$ & $\iota_2$\\\midrule\endfirsthead',r'\toprule Object & Pair & Tokens & Sign & $\iota_1$ & $\iota_2$\\\midrule\endhead']
for row in rows:
    p=tuple(map(tuple,row['pair']));tokens=','.join(f'{w}:{b.a[i]}' for w,i in row['marks'])
    body.append(f"{row['id']} & {pairs.index(p)} & ${tokens}$ & {'+' if row['sign']>0 else '-'} & {row['iota1']} & {row['iota2']}"+r'\\')
body += [r'\bottomrule\end{longtable}\normalsize']
(DEST/'example-table.tex').write_text('\n'.join(body))
shutil.copyfile(OUT/'running-geometry.json',DEST/'running-geometry.json')
shutil.copyfile(OUT/'running-objects.json',DEST/'running-objects.json')

sys.path.insert(0,str(ROOT/'paper/figures'))
from model import Model
from draw import Panel,pt
from tri import enumerate_classes,from_code

def figure(b,o,name,other=None,label=''):
    fs=b.f if b.orientation>0 else [tuple(reversed(f)) for f in b.f]
    model=Model(fs,b.root)
    # Affine transform the generic Tutte layout, including the ray direction.
    shear=next(k for k in range(1,10000) if all(b.cen[w][0] != z[0] for w in b.w for z in list(b.pos.values())+[b.cen[t] for t in b.a]))
    # Recover actual shear from the fixed second/third root coordinates.
    rr=b.f[b.root];shear=float(b.pos[rr[2]][0])/100
    def trans(z):
        x,y=map(float,z);x-=shear*y
        return np.array([-4.330127+8.660254*x/100+4.330127*y/100,-2.5+7.5*y/100])
    xy={v:trans(z) for v,z in b.pos.items()}
    def panel(obj):
        p,M=obj;pp=Panel(model,xy,5,unit=.42)
        pp.base().arrows(zip(*p)).vertices(labels=False)
        for t,v in zip(b.a,p[1]):
            pp.add(rf'\draw[bf spoke] {pt(trans(b.cen[t]))} -- {pt(xy[v])};')
        for w,i in M:
            t=b.a[i];a=trans(b.cen[t]);v=xy[p[1][i]];q=trans(b.cen[w])
            pp.add(rf'\draw[bf kept] {pt(a)} -- {pt(v)};')
            pp.add(rf'\node[draw=bfW,circle,fill=white,inner sep=1pt,font=\tiny] at {pt(q)} {{$w_{{{w}}}$}};')
            pp.add(rf'\node[fill=white,font=\tiny,inner sep=.3pt] at {pt((a+v)/2)} {{$t_{{{t}}}$}};')
        return pp.tex()
    out=panel(o)
    if other is not None:out+=r'\quad$\longleftrightarrow$\quad'+panel(other)
    (DEST/'figures'/f'{name}.tex').write_text(out)
    return r'\begin{figure}[ht]\centering\input{figures/'+name+r'.tex}\caption{'+label+r'}\end{figure}'

o=next(o for o in b.objects(2) if b.two(o)!=o)
figs=[figure(b,o,'marked',label='A marked pair on the current running example. Blue arrows show $D$; thick spokes and labelled white points specify the two tokens. Rays are encoded by the stored exact layout. Thin spokes show $s$.')]
figs.append(figure(b,o,'second',b.two(o),'The second involution on the same marked pair. It preserves the unoriented cover and moves only the selected token, reversing its cycle when needed.'))
levels=enumerate_classes(12);T=from_code(levels[12][6]);b1=Check(T.faces,8)
o1=next(o for o in b1.objects(1) if b1.one(o)!=o)
figs.append(figure(b1,o1,'first',b1.one(o1),'The first involution on class 6, root 8, with 12 vertices. The second state and the token stay fixed while the directed opposite-edge cycle reverses. Blue arrows show the resulting change to $D$.'))
(DEST/'figures/panels.tex').write_text('\n'.join(figs))

# Markdown companion, with the complete proof source retained as the authority.
text='''# Two involutions for the forest-pair lemma

PROVED-HERE. If a pair of disjoint states exists in a simple face-bicoloured sphere triangulation, a pair exists whose opposite-edge graph is a forest. The complete standalone proof is in involutions.tex and involutions.pdf. It assumes pair existence, so it does not need a separating-triangle hypothesis.

## Objects and the two maps

Let m be the minimum cycle count of a pair. A marked object consists of a pair and an unordered set of m distinct crossings of selected second-state spokes with fixed white-face rays. Repeated white faces and repeated spokes are permitted; repeated identical crossings are not. Direct each cycle through the first-state corner, centre, and second-state corner. With J equal to clockwise minus counterclockwise cycles, its sign is (-1) raised to floor(J/2) plus the number of marked right-to-left crossings.

The first map fixes objects with a forest opposite-edge graph. Otherwise it reverses the first opposite-edge cycle, choosing that cycle from the second state alone. This preserves all marks. The disk identity changes J by two, so it reverses sign.

The second map first reverses the first unmarked cycle of the underlying unoriented cover. If all cycles are marked, minimality forces exactly one mark per cycle. First select an exterior white-face mark, or else a nonfirst interior crossing, using a fixed orientation-independent cycle order. Pair successive ray crossings, leaving only the first crossing of an interior ray unpaired. Move the mark to its partner and reverse its cycle exactly when the partner is currently a first-state spoke. All other marks lie on other cycles. The same cycle qualifies on the return move; this proves involutivity. Geometric pairing reverses crossing direction, and cycle reversal reverses it again while flipping floor(J/2). Thus the sign reverses in either case.

Second-fixed objects are minimum covers with one interior white-face point per cycle, marked at the first crossing, with the unique orientation making that crossing a second-state spoke. Their number is the sum over minimum covers of the product of enclosed white-face counts. It is positive, and all fixed objects have sign (-1)^floor(m/2). The two signed counts force a first-fixed object.

## Explicit construction

Choose any second-fixed object by enumerating minimum covers. Alternate first and second moves, stopping before a fixed move. The finite two-coloured degree-two graph of the two involutions is a path from this endpoint. A second-fixed terminal endpoint would have the opposite sign after an odd number of moves, impossible. Hence it ends at a forest pair. This is the Garsia-Milne finite path argument. It is an exhaustive constructor, with no claim that finding a minimum cover is efficient.

## Verification

COMPUTED by research/2026-11-14_sol_li-completion/verify.py and extras.py. All 56 classes through 14 triangulation vertices agree as canonical maps with plantri. All 1206 roots are checked, including 880 with pairs. The verifier enumerates 221050 marked objects and checks both maps, signs, fixed sets, lowest coefficients and all 4658 paths from second-fixed objects. Maximum path length is two moves. Family checks reach 20 triangulation vertices. See the research census, witnesses and family outputs.

## Example and source relation

The current running.json has minimum cycle count two. The exact rational layout here gives 279 marked objects, nine second-fixed objects, and lowest coefficient nine. running-objects.json lists every object and both images; example-table.tex includes the full listing in the PDF. Earlier counts of 213 refer to a different geometry or input and are not silently reused.

Li's incidence orientation is opposite to the directed two-spoke convention used here, so his cw-prime is -J. The two sign definitions nevertheless agree because n and m have the same parity. Li Definitions 13 through 23 and Appendix B supply the maps. The full general-m verifications, set convention, invariant selection rule, nonemptiness proof and finite-path extraction are written in the note. OpenAI supplies the disk identity and first cancellation; barnette_trees uses a different ordered weight-token walk with restarts. Heights at white faces are signed counts of the same ray crossings.
'''
(DEST/'INVOLUTIONS.md').write_text(text)
print(res)
