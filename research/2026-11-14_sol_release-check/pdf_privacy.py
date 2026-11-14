"""PDF personal-data locations only. python -B pdf_privacy.py CLONE LOGDIR"""
from pathlib import Path
import fitz,subprocess,re,json,sys,os
r=Path(sys.argv[1]);out=Path(sys.argv[2]);findings=[];errors=[];count=0
pattern=re.compile(r'[\w.+-]{1,120}@[\w.-]{1,120}\.[A-Za-z]{2,}|[A-Z]:[\\/]Users[\\/][^\\/\s]+|\b'+re.escape(os.environ.get('USERNAME','Tom'))+r'\b',re.I)
for f in subprocess.check_output(['git','ls-files'],cwd=r,text=True).splitlines():
 if not f.lower().endswith('.pdf'):continue
 count+=1
 try:
  with fitz.open(r/f) as doc:
   for field,value in (doc.metadata or {}).items():
    if pattern.search(value or ''):findings.append(dict(file=f,metadata_field=field))
   for page in doc:
    for i,line in enumerate(page.get_text().splitlines(),1):
     if pattern.search(line):findings.append(dict(file=f,page=page.number+1,line=i))
 except Exception as e:errors.append(dict(file=f,error=type(e).__name__))
(out/'pdf-personal-locations.json').write_text(json.dumps(dict(pdfs=count,locations=findings,errors=errors),indent=2),encoding='utf8')
print('PDFs',count,'candidate locations',len(findings),'errors',len(errors))
