"""Read-only tracked-tree inventory. python -B scan.py CLONE OUTDIR"""
from pathlib import Path
import subprocess,sys,re,json,hashlib,collections,urllib.parse
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve()
files=subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0')[:-1]
tracked=set(files); texts={}; hashes=collections.defaultdict(list); large=[]
for f in files:
 p=root/f;b=p.read_bytes();hashes[hashlib.sha256(b).hexdigest()].append(f)
 if len(b)>5_000_000:large.append({'file':f,'bytes':len(b)})
 if p.suffix.lower() in {'.md','.tex','.py','.txt','.json','.toml','.yaml','.yml','.ps1','.sh','.bib','.html','.js','.sty','.gitignore','.cfg'} or p.name=='.gitignore':
  try:texts[f]=b.decode('utf-8-sig')
  except UnicodeDecodeError:pass
artifacts=[f for f in files if re.search(r'\.(aux|log|out|fls|fdb_latexmk|synctex\.gz|pyc)$|__pycache__/',f)]
folders=sorted({f.split('/')[1] for f in files if f.startswith('research/') and f.count('/')>=2})
index=texts.get('research/INDEX.md','')
absolute=[];personal=[]
for f,t in texts.items():
 for i,line in enumerate(t.splitlines(),1):
  if re.search(r'\b[A-Z]:[\\/]',line):absolute.append({'file':f,'line':i})
  if re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|[A-Z]:[\\/]Users[\\/][^\\/\s]+|/home/[^/\s]+|\b'+re.escape(__import__('os').environ.get('USERNAME','Tom'))+r'\b',line,re.I):personal.append({'file':f,'line':i,'kind':'email, local username or user directory'})
residue=[]
for f,t in texts.items():
 if f in ['paper/main/barnette.tex','proofs/primal/primal.tex','proofs/involutions/involutions.tex'] or (f.startswith('proofs/sign-free/') and f.endswith('.tex')) or (f.startswith('digestions/atlas/') and Path(f).name in ['pages.py','pages_more.py']):
  for i,line in enumerate(t.splitlines(),1):
   if re.search(r'PROVED-HERE|\bCOMPUTED\b|\bLIT\b|\bHUNCH\b|\bREFUTED\b|astra|\bsol\b|fable|opus|\bGPT\b|Claude|research/|agent|referee report',line,re.I):residue.append({'file':f,'line':i,'text':line})
links=[];paths=[];tex=[]
def resolve(f,target,extensions=()):
 target=urllib.parse.unquote(target.split('#')[0].split('?')[0]); target=target.replace('\\','/')
 if not target:return True
 candidates=[root/Path(f).parent/target,root/target]
 return any(p.exists() or any(p.with_suffix(ext).exists() for ext in extensions) for p in candidates)
def scope(f):return f in ['README.md','research/INDEX.md','papers/INDEX.md'] or f.startswith('digestions/') or (f.startswith('proofs/') and f.endswith('.md')) or (f.startswith('paper/') and Path(f).name.startswith('README'))
for f,t in texts.items():
 if f.endswith('.md') and scope(f):
  fence=False
  for i,line in enumerate(t.splitlines(),1):
   if line.strip().startswith('```'):fence=not fence;continue
   if not fence:
    prose=re.sub(r'\$[^$]*\$','',line)
    for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',prose):
     target=target.strip('<>').split(' "')[0]
     if not re.match(r'[a-z]+:|#',target,re.I) and not resolve(f,target):links.append({'file':f,'line':i,'target':target})
   for target in re.findall(r'`([^`\n]+)`',line):
    if re.fullmatch(r'[\w./*?\\ -]+',target) and (('/' in target and not target.startswith('/')) or re.search(r'\.(pdf|py|tex|json|md|bib|sty|txt|html|svg|png)$',target)):
     if not resolve(f,target):paths.append({'file':f,'line':i,'target':target,'fenced':fence})
 if f.endswith('.tex'):
  for i,line in enumerate(t.splitlines(),1):
   line=re.split(r'(?<!\\)%',line)[0]
   for cmd,target in re.findall(r'\\(includegraphics|input|include|bibliography)(?:\[[^\]]*\])?\{([^}]+)\}',line):
    if '\\' in target or '#' in target:continue
    for item in target.split(','):
     ext=('.pdf','.png','.jpg','.eps') if cmd=='includegraphics' else ('.bib',) if cmd=='bibliography' else ('.tex',)
     # Shared TeX input paths and atlas TEXINPUTS documented by the generators.
     bases=[root/Path(f).parent,root/'paper/figures',root/'digestions/atlas',root/'digestions/atlas/toolkit']
     if f.startswith('proofs/involutions/figures/'): bases.append(root/'proofs/involutions')
     found=any((b/item).is_file() or any(Path(str(b/item)+e).is_file() for e in ext) for b in bases)
     if not found:tex.append({'file':f,'line':i,'command':cmd,'target':item})
data={'tracked_files':len(files),'tracked_bytes':sum((root/f).stat().st_size for f in files),'large':large,'duplicates':[v for v in hashes.values() if len(v)>1],'build_pattern_files':artifacts,'absolute_paths':absolute,'personal_locations':personal,'research_without_report':[p for p in folders if f'research/{p}/REPORT.md' not in tracked],'research_missing_index':[p for p in folders if p not in index and p.removeprefix('2026-11-14_') not in index],'broken_markdown_links':links,'unresolved_code_paths':paths,'unresolved_tex_targets':tex,'internal_residue':residue,'upstream_candidates':[f for f in files if re.search(r'(^|/)(vendor|upstream|node_modules|\.git)/|plantri\.c$',f)]}
(out/'scan.json').write_text(json.dumps(data,indent=2),encoding='utf8')
for k,v in data.items(): print(k,len(v) if isinstance(v,list) else v)
