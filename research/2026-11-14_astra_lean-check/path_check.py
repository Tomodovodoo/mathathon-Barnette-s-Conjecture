from pathlib import Path
import sys,shutil
sys.path.insert(0,str(Path(__file__).parent))
from rebuild import run,R,D,P,L
shutil.copy2(D/'IndependentWalker.lean',P/'IndependentWalker.lean')
s='import PaperRoute.Main\nimport IndependentWalker\n#audit_path OAI.Barnette.main target Polynomial.eval\u2082_add to "'+D.as_posix()+'/polynomial-path.txt"\n'
(D/'PathCheck.lean').write_text(s,encoding='utf-8');shutil.copy2(D/'PathCheck.lean',P/'PathCheck.lean')
run('compile-walker-path',[L,'env','lean','-o','.lake/build/lib/lean/IndependentWalker.olean','IndependentWalker.lean'],P)
run('polynomial-path',[L,'env','lean','PathCheck.lean'],P)
