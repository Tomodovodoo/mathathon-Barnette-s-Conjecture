"""Supplemental path/anchor resolution. python -B paths.py CLONE LOGDIR"""
from pathlib import Path
import subprocess,re,json,sys,urllib.parse
r=Path(sys.argv[1]);out=Path(sys.argv[2]);fs=subprocess.check_output(['git','ls-files'],cwd=r,text=True).splitlines()
d=json.loads((out/'scan.json').read_text(encoding='utf8')); rows=[]
for x in d['unresolved_code_paths']:
 target=x['target']; candidates=[f for f in fs if f.endswith('/'+target.rstrip('/')) or f.endswith('/2026-11-14_'+target.rstrip('/')+'/REPORT.md') or f.endswith('/2026-11-14_'+target)]
 x=dict(x,candidates=candidates)
 if candidates:x['classification']='contextual reference, candidate targets listed'
 elif any(k in target for k in ['NN-','*.','/.svg','/.png']):x['classification']='filename pattern'
 elif target.startswith(('python ','pdftoppm ','lake.exe ')):x['classification']='command, not a literal path'
 elif '/2026-11-14_' in target or target.endswith(('.lean','.md')):x['classification']='review context or missing/proposed path; inspect surrounding text'
 else:x['classification']='contextual/generated path; inspect surrounding text'
 rows.append(x)
(out/'path-triage.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
checks=[]
for f in fs:
 if not f.endswith('.md'):continue
 if not (f in ['README.md','research/INDEX.md','papers/INDEX.md'] or f.startswith(('digestions/','proofs/')) or f.startswith('paper/') and Path(f).name.startswith('README')):continue
 for i,line in enumerate((r/f).read_text(encoding='utf8').splitlines(),1):
  for target in re.findall(r'\[[^\]]*\]\(([^)]+#[^)]*)\)',line):
   if re.match(r'\w+:',target):continue
   path,anchor=target.split('#',1);p=(r/f).parent/path if path else r/f
   if p.suffix!='.md' or not p.exists():continue
   text=p.read_text(encoding='utf8');heads=re.findall(r'^#{1,6}\s+(.+)',text,re.M)
   slugs=[re.sub(r'[^\w -]','',h.lower()).replace(' ','-') for h in heads]
   checks.append(dict(file=f,line=i,target=target,anchor_found=urllib.parse.unquote(anchor) in slugs or f'id="{anchor}"' in text))
(out/'anchors.json').write_text(json.dumps(dict(checks=checks,unresolved=[x for x in checks if not x['anchor_found']]),indent=2),encoding='utf8')
t=(r/'papers/INDEX.md').read_text(encoding='utf8').replace(r'\_','_');checked=[]
pat=r'(?<![\w/])(?:papers|paper|proofs|research|digestions|workings|labyrinth)/[\w./*?+-]+'
for i,line in enumerate(t.splitlines(),1):
 for m in re.finditer(pat,line):checked.append(dict(line=i,target=m.group()))
(out/'papers-paths.json').write_text(json.dumps(dict(checked=checked,missing=[x for x in checked if not (r/x['target']).exists()]),indent=2),encoding='utf8')
allpaths=[]
for f in fs:
 if not f.endswith('.md'):continue
 if not (f in ['README.md','research/INDEX.md','papers/INDEX.md'] or f.startswith(('digestions/','proofs/')) or f.startswith('paper/') and Path(f).name.startswith('README')):continue
 for i,line in enumerate((r/f).read_text(encoding='utf8').replace(r'\_','_').splitlines(),1):
  for m in re.finditer(pat,line):
   target=m.group().rstrip('.')
   allpaths.append(dict(file=f,line=i,target=target,exists=(r/target).exists(),glob_matches=[p.relative_to(r).as_posix() for p in r.glob(target)] if '*' in target else []))
(out/'rooted-paths.json').write_text(json.dumps(dict(checked=allpaths,missing=[x for x in allpaths if not x['exists'] and not x['glob_matches']]),indent=2),encoding='utf8')
