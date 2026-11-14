from pathlib import Path
import sys,shutil
sys.path.insert(0,str(Path(__file__).parent))
from rebuild import run,R,D,P,L
with (D/'BUILD-LOG.md').open('a',encoding='utf-8') as f:f.write('\nInitial upstream build deliberately stopped after 438s to keep each heavy run below ten minutes. Command `taskkill /PID 25644 /T /F` stopped only the inspected review-owned Lake/Lean tree. First import took 295s; compiled checkpoints retained. This is an interrupted run, not a Lean error. Resuming the same fresh build.\n')
run('build-upstream-resumed',[L,'build'],P)
run('build-devices-route',[L,'build','Devices','PaperRoute'],P)
run('axioms',[L,'env','lean','Devices/Axioms.lean'],P)
for name in ['IndependentWalker','Statements','Definitions','Nonvacuity','OriginalCheck','ReplacementCheck']:
 shutil.copy2(D/(name+'.lean'),P/(name+'.lean'))
run('compile-walker',[L,'env','lean','-o','.lake/build/lib/lean/IndependentWalker.olean','IndependentWalker.lean'],P)
run('statements',[L,'env','lean','Statements.lean'],P)
run('definitions',[L,'env','lean','Definitions.lean'],P)
run('nonvacuity',[L,'env','lean','Nonvacuity.lean'],P)
run('original-walk',[L,'env','lean','OriginalCheck.lean'],P)
run('replacement-walk',[L,'env','lean','ReplacementCheck.lean'],P)
