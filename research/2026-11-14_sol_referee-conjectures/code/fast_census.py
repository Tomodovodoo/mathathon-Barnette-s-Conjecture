import subprocess,sys,json
from pathlib import Path
from independent import ROOT,OUT,save
exe=Path(__file__).with_name('count.exe')
rows=[]
for n in map(int,sys.argv[1:]):
    p=subprocess.Popen([str(ROOT/'workings/barnette_lab/vendor/plantri.exe'),'-ab',str(n)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # plantri is only the input generator; the sole heavy process is our counter.
    r=subprocess.run([str(exe)],stdin=p.stdout,capture_output=True,text=True,timeout=540,check=True)
    p.stdout.close();p.stdout=None
    err=p.communicate()[1].decode();assert p.returncode==0
    d=json.loads(r.stdout);d['V']=n
    rows.append(d);save(f'fast_census_{n}.json',d);print(d,flush=True)
save('fast_census_summary.json',rows)
