from pathlib import Path
import json,subprocess,hashlib,datetime
root=Path.cwd();out=root/'research/2026-11-14_sol_digest-fixes'
logs=[]
for args in [('labyrinth/seed.py',),('labyrinth/lab.py','check'),('labyrinth/lab.py','build')]:
 cmd=['python','-X','utf8','-B',*args];p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf8');logs.append('$ '+' '.join(cmd)+'\n'+p.stdout+p.stderr+'\nexit='+str(p.returncode));assert p.returncode==0,logs[-1]
(out/'build-check.txt').write_text('\n\n'.join(logs)+'\n',encoding='utf8')
reports=['2026-11-14_fable_descent','2026-11-14_astra_referee-descent','2026-11-14_astra_lean-check','2026-11-14_opus_referee-rainbow','2026-11-14_fable_referee-families','2026-11-14_sol_lab-tests']
scan=[]
for name in reports:
 p=root/'research'/name/'REPORT.md';scan.append(dict(path=str(p.relative_to(root)),exists=p.exists(),sha256=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None,heading=p.read_text(encoding='utf8').splitlines()[0] if p.exists() else None))
(out/'final-report-scan.json').write_text(json.dumps(dict(scanned=datetime.datetime.now().isoformat(),reports=scan),indent=2)+'\n')
print('\n'.join(logs))
