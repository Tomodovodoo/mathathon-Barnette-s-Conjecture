from pathlib import Path
import sys,shutil
sys.path.insert(0,str(Path(__file__).parent))
from rebuild import run,R,D,P,L
shutil.copy2(D/'Nonvacuity.lean',P/'Nonvacuity.lean')
run('nonvacuity-verified',[L,'env','lean','Nonvacuity.lean'],P)
run('original-walk',[L,'env','lean','OriginalCheck.lean'],P)
run('replacement-walk',[L,'env','lean','ReplacementCheck.lean'],P)
