from pathlib import Path
import hashlib, json, subprocess

OUT = Path(__file__).resolve().parent
ROOT = Path('E:/Personal/Math/Leeham/floating')
REPO = OUT.parents[1]

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

inventory = []
for p in sorted(ROOT.rglob('*')):
    if p.is_file() and p.suffix.lower() in {'.tex', '.pdf', '.md'}:
        inventory.append({'path':str(p), 'bytes':p.stat().st_size, 'sha256':digest(p)})
(OUT/'source-inventory.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
subprocess.run(['pdftotext','-layout',str(ROOT/'floating.pdf'),str(OUT/'original-floating.txt')],check=True)
cases = json.loads((ROOT/'Astra/v6/work/editorial-20/proposals.json').read_text(encoding='utf-8'))['cases']
text = '# Twenty approved changes\n\nSource: Astra/v6/work/editorial-20/proposals.json. Approval: thread position 2169; implementation confirmation: 2194. Exact source excerpts follow.\n\n'
for i,c in enumerate(cases,1):
    text += f"## {i}. {c['title']}\n\n{c['location']}. {c['note']}\n\nBefore:\n\n```tex\n{c['old']}\n```\n\nAfter:\n\n```tex\n{c['new']}\n```\n\n"
(OUT/'APPROVED-EDIT-EXAMPLES.md').write_text(text,encoding='utf-8')
print(f'Indexed {len(inventory)} source files and extracted {len(cases)} approved edits.')

# Source pages inspected for formulas and layout, not newly authored figures.
import fitz
for filename, page in [('OpenAI-Barnette.pdf',5), ('A-Note-On-Barnette.pdf',11), ('barnette_trees.pdf',8)]:
    with fitz.open(REPO/'papers'/filename) as doc:
        doc[page].get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(OUT/(filename+'.png'))
