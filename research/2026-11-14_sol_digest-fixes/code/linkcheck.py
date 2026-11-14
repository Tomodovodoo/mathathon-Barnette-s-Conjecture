from pathlib import Path
import re,json,urllib.parse
ROOT=Path.cwd(); out=ROOT/'research/2026-11-14_sol_digest-fixes'
files=[ROOT/'digestions/steps/00-overview.md',ROOT/'digestions/steps/09-what-is-still-open.md',ROOT/'digestions/atlas/README.md']
files+=sorted((ROOT/'digestions/route-map').rglob('*.md'))
files+=sorted((ROOT/'labyrinth').rglob('*.md'))
files+=sorted(out.rglob('*.md'))
lines=[]; bad=[]
for p in files:
 count=0
 for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',p.read_text(encoding='utf8')):
  target=target.strip().strip('<>')
  if re.match(r'^[a-z]+://|^mailto:',target): continue
  local=urllib.parse.unquote(target.split('#')[0].split('?')[0])
  if not local: continue
  q=(p.parent/local).resolve()
  if not q.exists(): bad.append(f'{p.relative_to(ROOT)}: {target}')
  else: count+=1
 lines.append(f'{p.relative_to(ROOT)}: {count} local Markdown links resolve')
for p in sorted((ROOT/'labyrinth/dashboard').glob('*.html')):
 count=0
 for target in re.findall(r'(?:href|src)=["\']([^"\']+)["\']',p.read_text(encoding='utf8')):
  if re.match(r'^[a-z]+:|^#',target): continue
  local=urllib.parse.unquote(target.split('#')[0].split('?')[0])
  if not local: continue
  if not (p.parent/local).resolve().exists(): bad.append(f'{p.relative_to(ROOT)}: {target}')
  else: count+=1
 lines.append(f'{p.relative_to(ROOT)}: {count} static HTML targets resolve; dynamic JavaScript links not executed')
lines+=['MISSING '+b for b in bad]
lines.append(f'{len(files)} Markdown files; {len(bad)} missing targets')
(out/'link-check.txt').write_text('\n'.join(lines)+'\n',encoding='utf8')
print('\n'.join(lines)); raise SystemExit(bool(bad))
