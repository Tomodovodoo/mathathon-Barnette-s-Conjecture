from pathlib import Path
import sys,shutil
sys.path.insert(0,str(Path(__file__).parent))
from rebuild import run,R,D,P,L
for f in D.glob('*.lean'):
 s=f.read_text(encoding='utf-8-sig');f.write_text(s,encoding='utf-8');shutil.copy2(f,P/f.name)
with (D/'BUILD-LOG.md').open('a',encoding='utf-8') as f:f.write('\nReviewer checker first compile failed because Windows PowerShell Set-Content inserted a UTF-8 BOM before import. Removed BOMs from reviewer-only .lean files. Submitted sources were unaffected.\n')
run('compile-walker-utf8',[L,'env','lean','-o','.lake/build/lib/lean/IndependentWalker.olean','IndependentWalker.lean'],P)
run('statements',[L,'env','lean','Statements.lean'],P)
run('definitions',[L,'env','lean','Definitions.lean'],P)
run('nonvacuity',[L,'env','lean','Nonvacuity.lean'],P)
run('original-walk',[L,'env','lean','OriginalCheck.lean'],P)
run('replacement-walk',[L,'env','lean','ReplacementCheck.lean'],P)
