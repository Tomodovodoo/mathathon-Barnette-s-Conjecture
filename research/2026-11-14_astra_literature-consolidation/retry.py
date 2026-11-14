from pathlib import Path
import urllib.request,re,json,subprocess
R=Path('research/2026-11-14_astra_literature-consolidation'); (R/'downloads').mkdir(exist_ok=True)
urls={
'Ford1956':'https://www.cs.yale.edu/homes/lans/readings/routing/ford-max_flow-1956.pdf',
'Felsner2004':'https://www.combinatorics.org/ojs/index.php/eljc/article/download/v11i1r15/pdf/',
'Batagelj1989':'https://www.impan.pl/shop/publication/transaction/download/product/86708',
'Branden2020':'https://annals.math.princeton.edu/wp-content/uploads/annals-v192-n3-p04-s.pdf',
'Kalman2020':'https://alco.centre-mersenne.org/item/10.5802/alco.129.pdf',
'Akiyama1980':'https://www.ecei.tohoku.ac.jp/alg/nishizeki/sub/j/DVD/PDF_J/J029.pdf',
'Tutte1956':'https://www.ams.org/journals/tran/1956-082-01/S0002-9947-1956-0081471-8/S0002-9947-1956-0081471-8.pdf',
'Garsia1981b':'https://pmc.ncbi.nlm.nih.gov/articles/PMC319275/pdf/pnas00616-0042.pdf'}
log=[]
for key,url in urls.items():
 try:
  with urllib.request.urlopen(url,timeout=20) as r:b=r.read()
  if not b.startswith(b'%PDF'):raise ValueError('response is not a PDF')
  p=R/'downloads'/(key+'.pdf');p.write_bytes(b)
  subprocess.run(['pdftotext','-layout',str(p),str(R/'text'/(key+'.txt'))],capture_output=True)
  log.append(dict(key=key,url=url,status='PDF downloaded',bytes=len(b)))
 except Exception as e:log.append(dict(key=key,url=url,status=str(e)))
 print(key,log[-1]['status'],flush=True)
(R/'retry-downloads.json').write_text(json.dumps(log,indent=2),encoding='utf-8')
