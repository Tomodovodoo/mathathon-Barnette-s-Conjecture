from pathlib import Path
import urllib.request, subprocess, json, hashlib
P=Path(__file__).resolve().parent
sources={
'hine-kalman':'https://arxiv.org/pdf/1808.06091',
'kalman-hypergraphs':'https://www.math.titech.ac.jp/top/~kalman/hypertutte.pdf',
'kalman-postnikov':'https://arxiv.org/pdf/1602.04449',
'juhasz-kalman-rasmussen':'https://arxiv.org/pdf/1112.2632',
'kalman-murakami':'https://arxiv.org/pdf/1305.4925',
'kalman-tothmeresz':'https://arxiv.org/pdf/1810.00812',
'kenyon-double-dimer':'https://arxiv.org/pdf/1105.4158',
'kenyon-propp-wilson':'https://arxiv.org/pdf/math/9903025',
'propp-orientations':'https://arxiv.org/pdf/math/0209005',
'burton-pemantle':'https://arxiv.org/pdf/math/0404048',
'stein':'https://msp.org/pjm/1971/37-1/pjm-v37-n1-p20-p.pdf',
'fps-bipolar':'https://arxiv.org/pdf/0803.0400',
'bousquet-melou-schaeffer':'https://arxiv.org/pdf/math/0211070',
'alon-nullstellensatz':'https://www.tau.ac.il/~nogaa/PDFS/null2.pdf',
'jung-induced-forests':'https://arxiv.org/pdf/2608.17350',
'makarov-induced-forests':'https://arxiv.org/pdf/2608.13964',
}
log=[]
for key,url in sources.items():
 try:
  f=P/'pdf'/f'{key}.pdf'
  if not f.exists():
   req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=45) as r: data=r.read()
   if not data.startswith(b'%PDF'): raise ValueError('not PDF')
   f.write_bytes(data)
  out=P/'source-text'/f'{key}.txt';out.parent.mkdir(exist_ok=True)
  subprocess.run(['pdftotext','-layout',str(f),str(out)],check=True,capture_output=True)
  log.append({'key':key,'url':url,'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'status':'downloaded and text extracted'})
  print(key,'OK',flush=True)
 except Exception as e:
  log.append({'key':key,'url':url,'status':str(e)});print(key,str(e),flush=True)
(P/'downloads.json').write_text(json.dumps(log,indent=2),encoding='utf-8')
(P/'pdf'/'INDEX.md').write_text('# Downloaded source PDFs\n\nRetrieved 2026-11-14 with `python research/2026-11-14_sol_machinery-literature/fetch_sources.py`. Only public arXiv, publisher or author-hosted copies. See `../downloads.json` for checksums and failures. Text extraction is for reading, not a substitute for checking formulas.\n\n'+'\n'.join(f"- [{v['key']}]({v['key']}.pdf). Source <{v['url']}>. {v['status']}." for v in log),encoding='utf-8')
