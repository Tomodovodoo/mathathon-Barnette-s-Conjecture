from inventory import *
import urllib.request,concurrent.futures
cat=json.loads(read(R/'research/2026-11-14_astra_literature-consolidation/catalog.json'))
(O/'web').mkdir(exist_ok=True)
jobs=[]
for x in cat:
 u=x['url']
 if 'arxiv.org/' in u:u=u.replace('/pdf/','/abs/')
 elif x['key']=='Barnette1969':u='https://users.monash.edu/~davidwo/papers/Barnette-AJC.pdf'
 elif x['key']=='Li2026':u='https://arxiv.org/abs/2610.30490v1'
 elif not u.startswith('http') or '.pdf' in u:continue
 jobs.append((x['key'],u))
def fetch(job):
 k,u=job
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=22) as r:b=r.read();final=r.url
  (O/'web'/(k+'.html')).write_bytes(b)
  s=b.decode('utf-8',errors='replace')
  licenses=sorted(set(re.findall(r'https?://(?:creativecommons.org|arxiv.org/licenses|arxiv.org/help/license)[^\s\"<>]+',s)))
  meta=re.findall(r'<meta\s+name="citation_([^"<>]+)"\s+content="([^"]*)"',s)
  return dict(key=k,url=u,final_url=final,status='opened metadata page',license=licenses,metadata=meta)
 except Exception as e:return dict(key=k,url=u,status=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:results=list(pool.map(fetch,jobs))
(O/'web-checks.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf-8')
print(len(results),'lookups;',sum(x['status']=='opened metadata page' for x in results),'opened')
