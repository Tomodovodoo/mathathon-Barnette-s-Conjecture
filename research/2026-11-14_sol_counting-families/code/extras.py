"""Reproduce the root sweep and the negative subdivision experiment."""
from count import *
from transfer import matching_transfer
out=[]
for p in (4,6):
    for L in range(1,6):
        g=tube(p,L);b=Instance(g);rows=[]
        for f in range(len(b.faces)):
            z=Instance(g,f);t,peak=matching_transfer(z,True,p)
            rows.append({'root':f,'vertices':list(z.faces[f]),'TM':t})
        out.append({'p':p,'L':L,'root_counts':rows})
        print('root sweep',p,L,sorted(set(r['TM'] for r in rows)),flush=True)
P=Path(__file__).resolve().parents[1]
(P/'data'/'root-sweeps.json').write_text(json.dumps(out,indent=2))
out=[]
for q in range(1,4):
    b=Instance(subdivide(stack(4,q).T));r=profile(b,False);r['q']=q;out.append(r)
    print('subdivided stack',q,r['states'],r['pairs'],r['tree_matchings'],r['cmin'],flush=True)
    (P/'data'/'subdivided-stacks.json').write_text(json.dumps(out,indent=2))
