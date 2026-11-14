from pathlib import Path
import re,json,hashlib
import fitz
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).parent/'outputs'; REND=OUT/'renders';REND.mkdir(exist_ok=True)
main=ROOT/'paper/main'
doc=fitz.open(main/'barnette.pdf')
pages=[]
for i,page in enumerate(doc):
    page.get_pixmap(dpi=130).save(REND/f'page-{i+1:02}.png')
    txt=page.get_text()
    (OUT/f'page-{i+1:02}.txt').write_text(txt,encoding='utf-8')
    pages.append(dict(page=i+1,width=page.rect.width,height=page.rect.height))
(OUT/'pdf-text.txt').write_text('\n\f\n'.join(p.get_text() for p in doc),encoding='utf-8')
tex=(main/'barnette.tex').read_text(encoding='utf-8')
aux=(main/'barnette.aux').read_text(encoding='utf-8')
labels={m[1]:{'number':m[2],'page':m[3]} for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]+)\}\{([^}]+)\}',aux) if not m[1].endswith('@cref')}
refs=[]
for m in re.finditer(r'\\(?:eq)?ref\{([^}]+)\}',tex):
    line=tex.count('\n',0,m.start())+1
    context=tex[tex.rfind('\n',0,m.start())+1:tex.find('\n',m.end())]
    assert m[1] in labels,m[1]
    refs.append(dict(line=line,label=m[1],**labels[m[1]],context=context))
(OUT/'resolved-refs.json').write_text(json.dumps(refs,indent=2),encoding='utf-8')
(OUT/'refs-review.txt').write_text('\n'.join(f"L{x['line']} {x['label']} -> {x['number']} (p{x['page']}): {x['context']}" for x in refs),encoding='utf-8')
cites=[]
for m in re.finditer(r'\\cite(?:\[([^]]+)\])?\{([^}]+)\}',tex):
    cites.append(dict(line=tex.count('\n',0,m.start())+1,locator=m[1],keys=m[2].split(',')))
bbl=(main/'barnette.bbl').read_text(encoding='utf-8')
keys=set(re.findall(r'\\bibitem\{([^}]+)\}',bbl))
assert {k for c in cites for k in c['keys']}==keys
(OUT/'citations.json').write_text(json.dumps(cites,indent=2),encoding='utf-8')
log=(main/'barnette.log').read_text(encoding='utf-8',errors='replace')
(OUT/'latex-final.txt').write_text(log,encoding='utf-8')
overfull=[float(x) for x in re.findall(r'Overfull \\[hv]box \((\d+(?:\.\d+)?)pt',log)]
bad=[s for s in log.splitlines() if re.search(r'undefined|multiply defined|^!',s,re.I)]
assert not bad,bad
assert max(overfull,default=0)<=2,overfull
result=dict(pages=len(doc),refs=len(refs),cited_entries=len(keys),overfull=overfull,bad_log_lines=bad,hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [main/'barnette.tex',main/'barnette.pdf',main/'refs.bib']})
(OUT/'build-verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
