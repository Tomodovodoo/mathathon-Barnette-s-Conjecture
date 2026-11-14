from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent))
from rebuild import run,R,D
run('cleanup',['powershell','-NoProfile','-File',str(D/'cleanup.ps1')])
