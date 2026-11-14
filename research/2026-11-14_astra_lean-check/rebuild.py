from pathlib import Path
import subprocess,time,datetime,sys,json,shutil
R=Path(r'E:/Personal/Math/mathathon/barnette-s-conjecture'); D=R/'research/2026-11-14_astra_lean-check'; P=Path('E:/lb2'); L=str(Path.home()/'.elan/bin/lake.exe')
def run(tag,args,cwd=R,timeout=590):
    start=time.time(); stamp=datetime.datetime.now().astimezone().isoformat()
    with (D/(tag+'.out')).open('w',encoding='utf-8') as out:
        p=subprocess.run(args,cwd=cwd,stdout=out,stderr=subprocess.STDOUT,timeout=timeout)
    with (D/'BUILD-LOG.md').open('a',encoding='utf-8') as log:
        log.write(f'\n## {tag}\n\nStarted {stamp}; cwd `{cwd}`.\n\n```\n{subprocess.list2cmdline(args)}\n```\n\nExit {p.returncode}; elapsed {time.time()-start:.3f} seconds. Full output: [{tag}.out]({tag}.out).\n')
    print(tag,p.returncode,round(time.time()-start,2),flush=True)
    if p.returncode: sys.exit(p.returncode)
if __name__=='__main__':
    (D/'BUILD-LOG.md').write_text('# Independent fresh build\n\nCOMPUTED. Only dependency packages are reused from E:/lbb; no OAI, Devices or PaperRoute compiled artifacts are copied. Every command output is retained alongside this log.\n',encoding='utf-8')
    run('clone',['git','clone','--no-checkout','https://github.com/openai/math.git',str(P)])
    run('checkout',['git','checkout','--detach','4eaee87548250b2682affda7d05d947c05554bae'],P)
    run('upstream-head',['git','rev-parse','HEAD'],P)
    for f in ['lakefile.toml','lake-manifest.json','lean-toolchain']: shutil.copy2(R/'proofs/lean'/f,P/f)
    shutil.copytree(P/'lean/OAI/Combinatorics/Hamiltonian',P/'OAI/Combinatorics/Hamiltonian')
    shutil.copytree(R/'proofs/lean/Devices',P/'Devices')
    shutil.copy2(R/'proofs/lean/paper-route/make_paper_route.py',P/'make_paper_route.py')
    start=time.time(); shutil.copytree(Path('E:/lbb/.lake/packages'),P/'.lake/packages')
    with (D/'BUILD-LOG.md').open('a',encoding='utf-8') as log: log.write(f'\nSetup: Python shutil.copy2 of the three configuration files, copytree of upstream Hamiltonian and submitted Devices, copy2 of route script. shutil.copytree E:/lbb/.lake/packages to E:/lb2/.lake/packages took {time.time()-start:.3f}s. Source cache read only.\n')
    run('lake-version',[L,'--version'],P)
    run('lean-version',[L,'env','lean','--version'],P)
    run('mathlib-head',['git','rev-parse','HEAD'],P/'.lake/packages/mathlib')
    run('generate',[sys.executable,'-I','make_paper_route.py'],P)
    run('build-upstream',[L,'build'],P)
    run('build-devices-route',[L,'build','Devices','PaperRoute'],P)
    run('axioms',[L,'env','lean','Devices/Axioms.lean'],P)
