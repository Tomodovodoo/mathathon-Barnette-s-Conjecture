from pathlib import Path
import subprocess,sys,time,json,re
p=Path(__file__).resolve().parents[1]; root=p.parents[1]
rows=[]
for v in map(int,sys.argv[1:]):
 start=time.time(); log=p/'data'/f'census-{v}.txt'; dump=p/'data'/f'record-{v}.txt'
 gen=subprocess.run([str(root/'workings/barnette_lab/vendor/plantri.exe'),'-b','-c4',str(v)],capture_output=True,timeout=120)
 proc=subprocess.run([str(p/'code/census.exe'),'-m','full','-d',str(dump)],input=gen.stdout,capture_output=True,timeout=550)
 assert proc.returncode==0
 lines=proc.stdout.decode().splitlines(); summaries=[x for x in lines if not x.startswith('R ')]
 log.write_text(gen.stderr.decode()+'\n'+'\n'.join(summaries)+'\n')
 row={'V':v,'seconds':round(time.time()-start,2),'summary':summaries,'generator':gen.stderr.decode()}
 rows.append(row); print(v,row['seconds'],' '.join(x for x in summaries if x.startswith(('SUMMARY','cmin=','C1 tested'))),flush=True)
 (p/'data/census.json').write_text(json.dumps(rows,indent=2))
