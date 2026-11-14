from check import *
from induction import *
from structure import structure,region
out={}
for filename in ('cube_witness.json','repair_witness.json'):
 d=json.loads((REPO/'research/2026-11-14_astra_induction-lemmas/data'/filename).read_text());src=d['source'];rot=src['rot'];R=src['root'];x,a,p,b,q=src['setup'];fs,col=faces(rot);ri=next(i for i,f in enumerate(fs) if set(f)==set(R));A=[f for i,f in enumerate(fs) if col[i]==col[ri] and i!=ri];B,RR,inds=contract(A,R,x,p,q);ss=states(B,RR);pp=[(r,s) for s in ss for r in states(B,RR,s)];gs={s:classify(A,R,x,p,q,s)[0] for s in ss if good(B,RR,s)};covers={}
 for z in pp:
  u,Q,D=info(B,z);covers.setdefault(u,[]).append((gs.get(z[1],'bad'),[len(C) for C in D]))
 out[filename]=dict(states=len(ss),pairs=len(pp),classes={c:list(gs.values()).count(c) for c in ('L','R','E')},covers=list(covers.values()))
 print(filename,out[filename],flush=True)
for d in json.loads((REPO/'research/2026-11-14_astra_induction-lemmas/data/g_five_certificates.json').read_text()):
 src=d['source'];rot=src['rot'];R=src['root'];res,details=structure(rot);r,valid,ws=next(z for z in details if set(z[0])==set(R));C=tuple(src['cycle']);inside,w=region(rot,C,R);minimal=not any(I<inside for _,I in ws);out[d['kind']]=dict(V=len(rot),inside=sorted(inside),white=w,valid=valid,minimal_all_bad5=minimal);print(out[d['kind']],flush=True)
# V11 witness, reproduced from its stated plantri index, independent of certificate labels.
lines=subprocess.run([str(P),'-ba','11'],capture_output=True,check=True).stdout.decode().splitlines();rot=parse(lines[1]);res,details=structure(rot);r,valid,ws=next(z for z in details if set(z[0])=={0,1,2});inside,w=region(rot,(0,1,7,5),(0,1,2));out['four11']=dict(inside=sorted(inside),valid=valid,white=w)
(BASE/'code/induction_witnesses.json').write_text(json.dumps(out,indent=2))
