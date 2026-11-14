"""Print the Markdown tables of BLUEPRINT.md from proofs/blueprint/blueprint.json.

Usage: python -I research/2026-11-14_opus_blueprint/scripts/tables.py > research/2026-11-14_opus_blueprint/data/tables.md
"""
import json, pathlib, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = pathlib.Path(__file__).resolve().parents[3]
bp = json.loads((ROOT / 'proofs/blueprint/blueprint.json').read_text(encoding='utf-8'))
N = {n['id']: n for n in bp['nodes']}
inv = {}
for e in bp['edges']:
    if e['type'] == 'corresponds-to' and e.get('relation') == 'informal':
        inv.setdefault(e['src'], []).append(e['dst'])
short = {'checked-exact': 'checked, exact', 'checked-form': 'checked, other form', 'refereed': 'refereed only', 'unrefereed': 'unrefereed'}
sk = set(bp['analysis']['skeleton'])
print('| merged paper | statement | OpenAI | primal note | involution note | Lean (file:line) | relation | status |')
print('| --- | --- | --- | --- | --- | --- | --- | --- |')
for n in sorted((n for n in bp['nodes'] if n['source'] == 'main' and n['kind'] != 'example'), key=lambda n: n['line']):
    lean = ', '.join(f"`{N[l]['label'].split('.')[-1]}` ({N[l]['file'][:-5]}:{N[l]['line']})" for l in n['lean']) or 'none'
    num = n['number'] if n['kind'] != 'text' else 'text'
    kind = {'lemma': 'Lemma', 'proposition': 'Prop.', 'theorem': 'Thm', 'definition': 'Def.', 'equation': 'Eq.', 'text': '', 'remark': 'Remark'}[n['kind']]
    name = f"{kind} {num} `{n['id']}`" + ('' if n['id'] in sk else ' (off route)')
    title = n.get('short', '')
    print(f"| {name} | {title} | {n['openai']} | {n['primal']} | {n['involutions']} | {lean} | {n['lean_relation']} | {short[n['status']]} |")
print()
print('| primal / involution | Lean | relation | status | merged-paper node |')
print('| --- | --- | --- | --- | --- |')
for n in bp['nodes']:
    if n['source'] in ('primal', 'involutions'):
        lean = ', '.join(f"`{N[l]['label'].split('.')[-1]}`" for l in n['lean']) or 'none'
        m = [k for k, v in inv.items() if n['id'] in v]
        print(f"| {n['source']} {n['number']} {n['title'] or n.get('label') or ''} | {lean} | {n['lean_relation']} | {short[n['status']]} | {', '.join(m)} |")
