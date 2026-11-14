"""Generate vector PDF figures and render the PDFs to PNG. Run from root."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import fitz
root=Path(__file__).resolve().parents[2]
out=root/'digestions/synthesis-figures'
data=json.loads((Path(__file__).parent/'counts.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','pdf.fonttype':42,'font.size':11})
fig,ax=plt.subplots(figsize=(11.7,8.3)); fig.patch.set_facecolor('#faf9f5');ax.set(xlim=(0,12),ylim=(0,8));ax.axis('off')
ax.text(.3,7.65,'What to read, and what supports it',size=22,weight='bold')
ax.text(.3,7.2,'Arrows show source or evidence flowing into a product, not independent proofs.',size=11)
boxes={
'sources':(.3,5.7,3.2,.9,'Three source papers\nLibrary: papers/INDEX.md'),
'lean':(4.2,5.7,3.2,.9,'Upstream Lean proof\nBuild + declaration dictionary'),
'research':(8.1,5.7,3.5,.9,'Research and AI referees\nProofs, counterexamples, scripts'),
'paper':(.3,3.6,3.2,1.1,'Main paper\nDual, disk, signed count, recovery'),
'companions':(4.2,3.6,3.2,1.1,'Companion proofs\nPrimal route / marked involutions'),
'maps':(8.1,3.6,3.5,1.1,'Route map + labyrinth\nAlternatives and failed routes'),
'digestions':(.3,1.6,3.2,1.1,'Step digestions + atlas\nDetails and illustrated routes'),
'figures':(4.2,1.6,3.2,1.1,'Figure toolkit + lab\nComputed objects and examples'),
'synthesis':(8.1,1.6,3.5,1.1,'This synthesis\nStart here; follow the links')}
for key,(x,y,w,h,t) in boxes.items():
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.03,rounding_size=.06',fc='#e3ece9' if key=='synthesis' else '#ffffff',ec='#54736d',lw=1.2))
    ax.text(x+w/2,y+h/2,t,ha='center',va='center',size=10)
def arrow(a,b):
    x,y,w,h,_=boxes[a];X,Y,W,H,_=boxes[b]
    start=(x+w/2,y);end=(X+W/2,Y+H)
    if Y>y:start=(x+w/2,y+h);end=(X+W/2,Y)
    if y==Y:start=(x+w,y+h/2);end=(X,Y+H/2)
    ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=12,color='#63716d',lw=1,shrinkA=6,shrinkB=6))
for a,b in [('sources','paper'),('sources','companions'),('lean','companions'),('research','maps'),('research','companions'),('paper','digestions'),('figures','companions'),('maps','synthesis'),('figures','synthesis')]:arrow(a,b)
ax.text(.3,.65,'The lab checks finite instances. AI reports audit written arguments.\nThe upstream Lean build certifies its own formal route, not every new manuscript.',size=11)
fig.savefig(out/'products.pdf',bbox_inches='tight');plt.close(fig)
fig,ax=plt.subplots(figsize=(11.7,8.3));fig.patch.set_facecolor('#faf9f5');ax.axis('off')
ax.text(0,1.03,'Kinds of route by recorded outcome',transform=ax.transAxes,size=22,weight='bold')
cols=['Proved','Computed','Open','Refuted']; rows=list(data['route_matrix'])
vals=[[data['route_matrix'][r][c] for c in cols] for r in rows]
table=ax.table(cellText=vals,rowLabels=rows,colLabels=cols,cellLoc='center',bbox=[.36,.19,.62,.74]);table.auto_set_font_size(False);table.set_fontsize(12)
for (i,j),cell in table.get_celld().items():
    cell.set_edgecolor('#d0d6d3');cell.set_linewidth(.6)
    cell.set_facecolor('#e3ece9' if i==0 else '#ffffff')
    if i==0:cell.set_text_props(weight='bold')
    if i>0 and j>=0 and vals[i-1][j]>0:cell.set_facecolor(['#e0ece4','#e3edf6','#f5eedb','#f2e2df'][j])
ax.text(0,.09,'226 records, each assigned one primary kind by count.py. Overlapping subjects are forced into one row.\nProved = source proof or proof written here, including unreviewed work. Open includes speculative routes.\nThese are route records, not independent proofs, success rates or a review verdict.',transform=ax.transAxes,size=10)
ax.text(0,.01,'Source: digestions/route-map/routes.py. Full assignments: research/2026-11-14_astra_synthesis/route-classification.json',transform=ax.transAxes,size=8)
fig.savefig(out/'route-outcomes.pdf',bbox_inches='tight');plt.close(fig)
for stem in ['products','route-outcomes']:
    with fitz.open(out/(stem+'.pdf')) as doc:
        assert len(doc)==1
        doc[0].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(out/(stem+'.png'))
print('Created two vector PDFs and rendered their two PNGs.')
