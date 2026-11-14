import sys,json,time
from pathlib import Path
sys.dont_write_bytecode=True
root=Path.cwd();out=root/'research/2026-11-14_sol_involutions-revision'
sys.path.insert(0,str(root/'research/2026-11-14_opus_referee-involutions/code'))
from ref import Inst,faces_from_rotation,plantri
from check import check
rows=[];start=time.monotonic()
for v in range(6,15):
    for cls,rot in enumerate(plantri(v)):
        fs=faces_from_rotation(rot)
        for r in range(len(fs)):
            I=Inst(fs,r);q=check(I);rows.append(dict(v=v,cls=cls,root=r,**q))
    print(v,round(time.monotonic()-start,1),flush=True)
    (out/'referee-rerun.json').write_text(json.dumps(dict(command='python research/2026-11-14_sol_involutions-revision/code/referee_rerun.py',rows=rows),indent=1))
p=[r for r in rows if r['pairs']];print('objects',sum(r['objects'] for r in p),'above zeros',sum(r['signed_other_k'][r['m']+1]==0 for r in p),flush=True)
