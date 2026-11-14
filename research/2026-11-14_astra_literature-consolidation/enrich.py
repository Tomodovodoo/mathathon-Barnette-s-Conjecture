from pathlib import Path
import urllib.request,json,re,subprocess
R=Path('research/2026-11-14_astra_literature-consolidation')
url='https://link.springer.com/content/pdf/10.1007/s10878-019-00460-8.pdf'
try:
 b=urllib.request.urlopen(url,timeout=25).read();assert b.startswith(b'%PDF');(R/'downloads/Florek2020.pdf').write_bytes(b)
 subprocess.run(['pdftotext','-layout',str(R/'downloads/Florek2020.pdf'),str(R/'text/Florek2020.txt')])
 print('Florek journal obtained')
except Exception as e:print(e)
# Primary publisher registry records for incomplete machinery bibliography.
queries={'GarsiaMilne1981':'A Rogers Ramanujan bijection Garsia Milne','Lindstrom1973':'On the vector representations of induced matroids','GesselViennot1985':'Binomial determinants paths hook length formulae','Alon1999':'Combinatorial Nullstellensatz Alon','SchrijverIntersection':'Polyhedral combinatorics Schrijver','Lovasz1980':'Matroid matching and some applications','Bouchet1989':'Maps and delta matroids','JKR2012':'Sutured Floer homology and hypergraphs','KalmanMurakami2017':'Root polytopes parking functions HOMFLY polynomial','Kasteleyn1967':'Graph theory and crystal physics','Fleischner1990':'Eulerian Graphs and Related Topics Part 1 Volume 1','Thomas1994':'4 connected projective planar graphs are Hamiltonian'}
log=[]
for key,q in queries.items():
 url='https://api.crossref.org/works?rows=1&query.bibliographic='+urllib.parse.quote(q)
 try:
  j=json.load(urllib.request.urlopen(url,timeout=20));r=j['message']['items'][0]; log.append(dict(old=key,url=url,record=r))
  print(key,r.get('title'),r.get('DOI'),r.get('published'),flush=True)
 except Exception as e:log.append(dict(old=key,url=url,error=str(e)))
(R/'extra-metadata.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
