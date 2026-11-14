"""Freeze inputs and generate exhaustive review inventories; no manuscript writes."""
from pathlib import Path
import difflib, hashlib, json, re

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).parent / 'outputs'
OUT.mkdir(exist_ok=True)
a = (ROOT/'paper/main/history/barnette-v1.tex').read_text(encoding='utf-8')
current = (ROOT/'paper/main/barnette.tex').read_text(encoding='utf-8')
if not (OUT/'v2-start.tex').exists():
    (OUT/'v2-start.tex').write_text(current, encoding='utf-8')
b = (OUT/'v2-start.tex').read_text(encoding='utf-8')
(OUT/'corrections.diff').write_text(''.join(difflib.unified_diff(b.splitlines(True), current.splitlines(True), fromfile='v2-start', tofile='v2-corrected')),encoding='utf-8')
(OUT/'full.diff').write_text(''.join(difflib.unified_diff(a.splitlines(True), b.splitlines(True), fromfile='v1', tofile='v2')), encoding='utf-8')
def blocks(s):
    found = []
    for m in re.finditer(r'\\begin\{(theorem|lemma|proposition|definition|example|remark|proof)\}(.*?)\\end\{\1\}',s,re.S):
        typ, body = m.groups()
        label = re.search(r'\\label\{([^}]+)\}',body)
        found.append({'type':typ,'label':label[1] if label else '', 'line':s.count('\n',0,m.start())+1,'text':m[0]})
    # Proof belongs to preceding theorem-like statement, irrespective of floats.
    previous=''
    counts={}
    for f in found:
        if f['type']=='proof':
            explicit=re.search(r'Proof of Theorem~\\ref\{([^}]+)\}',f['text'])
            f['key']='proof:'+(explicit[1] if explicit else previous)
        else:
            counts[f['type']]=counts.get(f['type'],0)+1
            f['key']=f['label'] or f['type']+':'+str(counts[f['type']])
            previous=f['key']
    return found
aa,bb=blocks(a),blocks(b)
am={x['key']:x for x in aa}
report=[]
for x in bb:
    old=am.get(x['key'])
    x['changed']=not old or old['text']!=x['text']
    if x['changed']:
        report.append(f"\n### {x['key']}, v2 line {x['line']}\n")
        report.extend(difflib.unified_diff((old['text'] if old else '').splitlines(True),x['text'].splitlines(True)))
(OUT/'environments.diff').write_text(''.join(report),encoding='utf-8')
(OUT/'environments.json').write_text(json.dumps(bb,indent=2),encoding='utf-8')
patterns={'display':r'\\\[.*?\\\]|\\begin\{equation\}.*?\\end\{equation\}', 'caption':r'\\caption\{'}
inventory=[]
for kind,pat in patterns.items():
    for m in re.finditer(pat,b,re.S):
        if kind=='caption':
            start=m.end(); depth=1; end=start
            while depth:
                if b[end]=='{': depth+=1
                if b[end]=='}': depth-=1
                end+=1
            val=b[start:end-1]
        else: val=m[0]
        inventory.append({'kind':kind,'line':b.count('\n',0,m.start())+1,'text':val,'identical_in_v1':val in a})
(OUT/'displays-captions.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
refs=[]
for m in re.finditer(r'\\(?:eq)?ref\{([^}]+)\}',b):
    start=b.rfind('\n',0,m.start())+1; end=b.find('\n',m.end())
    refs.append({'label':m[1],'line':b.count('\n',0,m.start())+1,'context':b[start:end]})
(OUT/'refs.json').write_text(json.dumps(refs,indent=2),encoding='utf-8')
if not (OUT/'fingerprints.json').exists():
    (OUT/'fingerprints.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'paper/main/history/barnette-v1.tex',ROOT/'paper/main/barnette.tex',ROOT/'paper/main/barnette.pdf']},indent=2))
print(json.dumps({'environments':len(bb),'changed_environments':sum(x['changed'] for x in bb),'displays_captions':len(inventory),'references':len(refs)}))
