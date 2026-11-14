from check import *
from families import *
d=json.loads((REPO/'research/2026-11-14_sol_referee-conjectures/data/R2_glued_V33.json').read_text());rr=d['rotation'];rot=[rr[str(i)] for i in range(len(rr))];R=d['root'];out=[dict(label='saved-R2-V33',**check(rooted(rot,R),R))]
for p in (4,6,8):
 r=tube(p,0);R=faces(r)[0][0];base=r
 for j in range(2):
  fs,col=faces(r);ri=next(i for i,f in enumerate(fs) if set(f)==set(R));white=next(f for i,f in enumerate(fs) if col[i]!=col[ri]);r,R=glue(r,R,base,faces(base)[0][0],white);out.append(dict(label=f'prism-sum-{p}-{j+2}',V=len(r),**check(rooted(r,R),R)))
print(json.dumps(out,indent=2));(BASE/'code/adversarial_extra.json').write_text(json.dumps(out,indent=2))
