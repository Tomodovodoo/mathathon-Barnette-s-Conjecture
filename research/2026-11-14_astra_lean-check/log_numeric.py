from pathlib import Path
import sys,hashlib,json
sys.path.insert(0,str(Path(__file__).parent))
from rebuild import run,R,D
run('numerical',[sys.executable,'-I',str(D/'numerical.py')])
run('source-inspection',[sys.executable,'-I',str(D/'inspect_sources.py')])
p=R/'paper/figures/running.json'
(D/'numerical-input-sha256.json').write_text(json.dumps({str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()},indent=2)+'\n')
