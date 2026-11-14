from pathlib import Path
import re,json,subprocess,urllib.request,concurrent.futures,hashlib
R=Path('research/2026-11-14_astra_literature-consolidation'); R.mkdir(exist_ok=True)
def parse(p):
 s=Path(p).read_text(encoding='utf-8'); out=[]
 for m in re.finditer(r'@(\w+)\s*\{\s*([^,]+),',s):
  i=m.end(); start=i; level=1
  while level and i<len(s):
   if s[i]=='{' and s[i-1]!='\\': level+=1
   if s[i]=='}' and s[i-1]!='\\': level-=1
   i+=1
  body=s[start:i-1]; fields={}; pos=0
  while (a:=re.search(r'(\w+)\s*=\s*',body[pos:])):
   key=a[1].lower(); j=pos+a.end(); k=j
   if body[j]=='{':
    depth=1;k=j+1
    while depth and k<len(body):
     if body[k]=='{' and body[k-1]!='\\': depth+=1
     if body[k]=='}' and body[k-1]!='\\': depth-=1
     k+=1
    val=body[j+1:k-1]
   else:
    k=body.find(',',j); k=len(body) if k<0 else k; val=body[j:k].strip('" ')
   fields[key]=val;pos=k+1
  out.append(dict(old=m[2],type=m[1],fields=fields,origin=str(p)))
 return out
sources=['research/2026-11-14_opus_history-literature/bibliography.bib','research/2026-11-14_sol_machinery-literature/bibliography.bib','paper/draft-A/refs.bib','paper/draft-B/refs.bib']
entries=[]; aliases={}; seen={}
def norm(s):return re.sub('[^a-z0-9]','',s.lower())
for src in sources:
 for e in parse(src):
  f=e['fields']; old=e['old']; ident=old.lower()
  # common variants
  if old.lower() in ['openai2026','li2026','constructive2026','tutte1975','stein1971','hine-kalman2018','hinekalman2018','hertel2005','barnette1969','ford1956','fordfulkerson1956']:
   ident={'hinekalman2018':'clocktheoremsfortriangulatedsurfaces','fordfulkerson1956':'maximalflowthroughanetwork','ford1956':'maximalflowthroughanetwork'}.get(old.lower(),old.lower())
   ident=ident.replace('hine-kalman2018','clocktheoremsfortriangulatedsurfaces')
  if ident in seen:
   prev=seen[ident]; aliases[old]=prev['old']
   for k,v in f.items(): prev['fields'].setdefault(k,v)
   continue
  seen[ident]=e;aliases[old]=old;entries.append(e)
(R/'raw-catalog.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'aliases.json').write_text(json.dumps(aliases,indent=2),encoding='utf-8')
# Extract every downloaded PDF once for title and statement inspection. No source modified.
paths=list(Path('research/2026-11-14_opus_history-literature/pdf').glob('*.pdf'))+list(Path('research/2026-11-14_sol_machinery-literature/pdf').glob('*.pdf'))+list(Path('papers').glob('*.pdf'))
(R/'text').mkdir(exist_ok=True)
for p in paths:
 subprocess.run(['pdftotext','-layout',str(p),str(R/'text'/(p.stem+'.txt'))],capture_output=True)
def fetch(e):
 f=e['fields']; result={'old':e['old']}
 if f.get('eprint'): url='https://arxiv.org/abs/'+f['eprint']
 elif f.get('doi'):url='https://api.crossref.org/works/'+urllib.parse.quote(f['doi'],safe='')
 elif f.get('url'):url=f['url']
 else:return result|{'status':'no primary URL in record'}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'LiteratureAudit/1.0'}),timeout=25) as r: b=r.read()
  result.update(url=url,status='retrieved',bytes=len(b))
  (R/'metadata').mkdir(exist_ok=True)
  (R/'metadata'/(re.sub('[^a-zA-Z0-9-]','_',e['old'])+'.txt')).write_bytes(b)
  if 'arxiv.org/abs' in url:
   result['licenses']=list(set(re.findall(r'https?://(?:creativecommons.org|arxiv.org/licenses)[^\s"<>]+',b.decode(errors='replace'))))
  elif 'crossref' in url:
   msg=json.loads(b)['message']; result['title']=msg.get('title'); result['author']=msg.get('author'); result['license']=msg.get('license',[])
 except Exception as ex:result.update(url=url,status=str(ex))
 return result
cache={x['old']:x for x in json.loads((R/'metadata-checks.json').read_text(encoding='utf-8'))} if (R/'metadata-checks.json').exists() else {}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: results=list(pool.map(lambda e: cache.get(e['old']) or fetch(e),entries))
(R/'metadata-checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(entries),'entries;',len(paths),'PDF extractions;',sum(r['status']=='retrieved' for r in results),'primary records retrieved')
