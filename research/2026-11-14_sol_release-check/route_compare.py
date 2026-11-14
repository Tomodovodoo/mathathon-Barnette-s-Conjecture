"""Compare regenerated route figures. python -B route_compare.py CLONE LOGDIR"""
from pathlib import Path
import re,json,subprocess,fitz,sys
r=Path(sys.argv[1]);out=Path(sys.argv[2]);rows=[]
for stem in ['route-kinds','route-map','route-map-overview']:
 rel=f'digestions/route-map/{stem}.svg'
 old=subprocess.check_output(['git','show','HEAD:'+rel],cwd=r).decode();new=(r/rel).read_text(encoding='utf8')
 def normalize(t):
  t=re.sub(r'<dc:date>.*?</dc:date>','<dc:date/>',t)
  mapping={key:'stable'+str(i) for i,key in enumerate(re.findall(r'\bid="([^"]+)"',t))}
  return re.sub(r'(?<=id=")[^"]+|(?<=url\(#)[^)]+|(?<=href="#)[^"]+',lambda m:mapping.get(m.group(),m.group()),t)
 pdf=f'digestions/route-map/{stem}.pdf'
 with fitz.open(stream=subprocess.check_output(['git','show','HEAD:'+pdf],cwd=r),filetype='pdf') as oldpdf,fitz.open(r/pdf) as newpdf:
  rows.append(dict(stem=stem,svg_equal_after_metadata_and_id_normalization=normalize(old)==normalize(new),pdf_text_equal=''.join(p.get_text() for p in oldpdf)==''.join(p.get_text() for p in newpdf),pdf_pixels_equal=[p.get_pixmap().samples for p in oldpdf]==[p.get_pixmap().samples for p in newpdf]))
(out/'route-reproducibility.json').write_text(json.dumps(rows,indent=2),encoding='utf8');print(rows)
