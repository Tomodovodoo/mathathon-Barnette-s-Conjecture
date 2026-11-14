"""Sequential clean-clone release checks. python -B run.py CLONE LOGDIR PHASE"""
from pathlib import Path
import sys, subprocess, json, time, os, re, hashlib
root=Path(sys.argv[1]).resolve(); out=Path(sys.argv[2]).resolve(); out.mkdir(exist_ok=True,parents=True)
phase=sys.argv[3]; env=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',MPLBACKEND='Agg')
results=[]
def run(name,args,cwd='.',timeout=540):
    start=time.time(); log=out/(name+'.txt')
    with log.open('w',encoding='utf8') as f:
        f.write(f'cwd: {cwd}\ncommand: {subprocess.list2cmdline(args)}\n'); f.flush()
        try: code=subprocess.run(args,cwd=root/cwd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=timeout).returncode
        except subprocess.TimeoutExpired: code='TIMEOUT'
    row=dict(name=name,command=args,cwd=cwd,code=code,seconds=round(time.time()-start,2)); results.append(row)
    (out/(phase+'-commands.json')).write_text(json.dumps(results,indent=2),encoding='utf8'); print(row,flush=True)
    return code
def py(name,path,*args): return run(name,[sys.executable,'-X','utf8','-B',path,*args])
products=['paper/main/barnette.pdf','proofs/primal/primal.pdf','proofs/involutions/involutions.pdf','digestions/atlas/atlas.pdf','paper/figures/gallery.pdf','paper/draft-A/barnette.pdf','paper/draft-B/barnette.pdf']
if phase=='baseline':
    import fitz,importlib.metadata as m
    data={'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'python':sys.version,'packages':{p:m.version(p) for p in ['networkx','numpy','scipy','sympy','pymupdf','pillow','matplotlib']},'pdfs':{}}
    for p in products:
        with fitz.open(root/p) as doc:
            text=''.join(page.get_text() for page in doc)
            data['pdfs'][p]={'pages':len(doc),'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'text':text}
    (out/'baseline.json').write_text(json.dumps(data,indent=2),encoding='utf8')
if phase=='code':
    py('plantri-setup','workings/barnette_lab/setup_plantri.py')
    py('lab-quick','workings/barnette_lab/run_tests.py','quick')
    py('lab-full','workings/barnette_lab/run_tests.py','full')
    py('route-map','digestions/route-map/build_map.py')
    run('route-map-diff',['git','diff','--stat','--','digestions/route-map'])
    run('route-map-patch',['git','diff','--','digestions/route-map'])
    py('frontier','labyrinth/make_frontier.py'); py('seed','labyrinth/seed.py')
    py('labyrinth-check','labyrinth/lab.py','check'); py('labyrinth-build','labyrinth/lab.py','build')
    for s in ['count','evidence','audit','snapshot']:
        py('synthesis-'+s,f'research/2026-11-14_astra_synthesis/{s}.py')
if phase=='figures':
    # Force the atlas builder to compile every figure rather than reuse tracked PDFs.
    for p in (root/'digestions/atlas/figs').glob('*.pdf'): p.unlink()
    for name,path,args in [('figure-build','paper/figures/build.py',[]),('figure-geometry','paper/figures/geometry_check.py',[]),('figure-crosscheck','paper/figures/crosscheck_lab.py',[]),('primal-figures','proofs/primal/figures/check.py',['--build']),('atlas-build','digestions/atlas/build.py',[]),('atlas-verify','digestions/atlas/verify.py',[]),('involution-check','research/2026-11-14_sol_involutions-revision/code/check.py',['14']),('involution-referee','research/2026-11-14_sol_involutions-revision/code/referee_rerun.py',[]),('involution-drawings','research/2026-11-14_sol_involutions-revision/code/drawings.py',[]),('involution-figures','research/2026-11-14_sol_involutions-revision/code/figures.py',[]),('involution-second','research/2026-11-14_fable_referee-involutions-v2/code/figure2.py',[])]:
        py(name,path,*args)
if phase=='documents':
    run('latexmk-attempt',['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error','barnette.tex'],'paper/main',45)
    for d,stem,bib in [('paper/main','barnette',True),('proofs/primal','primal',False),('proofs/involutions','involutions',False),('paper/draft-A','barnette',True),('paper/draft-B','barnette',True)]:
        name=d.replace('/','-'); tex=['pdflatex','-interaction=nonstopmode','-halt-on-error',stem+'.tex']
        run(name+'-tex1',tex,d)
        if bib: run(name+'-bibtex',['bibtex',stem],d)
        run(name+'-tex2',tex,d);run(name+'-tex3',tex,d)
    py('primal-readme-build','research/2026-11-14_astra_primal-revision/build.py')
if phase=='compare':
    import fitz,difflib
    baseline=json.loads((out/'baseline.json').read_text(encoding='utf8')); data={}
    for p in products:
        with fitz.open(root/p) as doc:
            text=''.join(page.get_text() for page in doc); old=baseline['pdfs'][p]
            diff=''.join(difflib.unified_diff(old['text'].splitlines(True),text.splitlines(True),fromfile='committed',tofile='rebuilt'))
            (out/(p.replace('/','-')+'-text.diff')).write_text(diff,encoding='utf8')
            data[p]={'committed_pages':old['pages'],'rebuilt_pages':len(doc),'text_equal':text==old['text'],'diff_lines':len(diff.splitlines())}
        run(p.replace('/','-')+'-fonts',['pdffonts',str(root/p)])
    (out/'pdf-comparison.json').write_text(json.dumps(data,indent=2),encoding='utf8')
    warnings=[]
    for p in root.rglob('*.log'):
        text=p.read_text(errors='replace'); lines=text.splitlines()
        if 'This is pdfTeX' not in text: continue
        for i,line in enumerate(lines,1):
            sizes=re.findall(r'Overfull \\[hv]box \(([0-9.]+)pt',line)
            if any(float(v)>2 for v in sizes) or re.search(r'undefined|Missing character|not found|LaTeX Error|Font Warning|Font shape',line,re.I):
                warnings.append({'file':p.relative_to(root).as_posix(),'line':i,'text':line})
    (out/'tex-warnings.json').write_text(json.dumps(warnings,indent=2),encoding='utf8')
if phase=='blueprint':
    upstream='research/2026-11-14_opus_blueprint/upstream/openai-math'
    run('blueprint-clone',['git','clone','--filter=blob:none','--no-checkout','https://github.com/openai/math.git',upstream])
    run('blueprint-sparse',['git','-C',upstream,'sparse-checkout','set','lean/OAI/Combinatorics/Hamiltonian','lean/ComparatorChallenges'])
    run('blueprint-checkout',['git','-C',upstream,'checkout','4eaee87548250b2682affda7d05d947c05554bae'])
    s='research/2026-11-14_opus_lean-integration/scripts'; d='research/2026-11-14_opus_lean-integration/data'
    run('blueprint-upstream-sigs',[sys.executable,'-I',s+'/lean_sigs.py',upstream+'/lean/OAI/Combinatorics/Hamiltonian',d+'/lean-sigs-upstream.json'])
    run('blueprint-device-sigs',[sys.executable,'-I',s+'/lean_sigs.py','proofs/lean/Devices',d+'/lean-sigs-devices.json'])
    for name in ['extract_tex','build_blueprint','status_table']:
        run('blueprint-'+name,[sys.executable,'-I',s+'/'+name+'.py'])
if phase=='supplement':
    py('figure-hunch','research/2026-11-14_sol_figures-polish/check_hunch.py')
    py('figure-proofs','research/2026-11-14_sol_figures-polish/proofs.py')
    py('primal-cancellation15','research/2026-11-14_astra_primal-revision/check_cancellation.py','15')
    py('primal-cancellation16','research/2026-11-14_astra_primal-revision/check_cancellation.py','16')
    py('primal-inspect','research/2026-11-14_astra_primal-revision/inspect_figures.py')
