"""Write STATUS-TABLE.md (statement by statement: old status, new status, reason) and the
tables for proofs/blueprint/BLUEPRINT.md from proofs/blueprint/blueprint.json.

Usage (repository root): python -I research/2026-11-14_opus_lean-integration/scripts/status_table.py
"""
import json, pathlib, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = pathlib.Path(__file__).resolve().parents[3]
HERE = pathlib.Path(__file__).resolve().parents[1]
bp = json.loads((ROOT / 'proofs/blueprint/blueprint.json').read_text(encoding='utf-8'))
N = {n['id']: n for n in bp['nodes']}
sk = bp['analysis']['skeleton']
OLD = {'checked-exact': 'exact', 'checked-form': 'other form', 'refereed': 'none', 'unrefereed': 'none'}
NEW = {'exact': 'exact', 'translation': 'after translation', 'weaker': 'weaker / different', 'none': 'none'}
ORG = {'upstream': 'upstream', 'project': 'added here', 'both': 'both', '-': '-'}
KIND = {'lemma': 'Lemma', 'proposition': 'Prop.', 'theorem': 'Thm', 'definition': 'Def.', 'equation': 'Eq.', 'text': 'Text', 'remark': 'Remark'}


def name(n):
    num = n['number'] if n['kind'] != 'text' else ''
    return f"{KIND[n['kind']]} {num} `{n['id']}`".replace('  ', ' ')


def lean(n, origin=None):
    out = []
    for l in n['lean']:
        L = N[l]
        if origin and L['origin'] != origin:
            continue
        out.append(f"`{L['label'].split('.')[-1]}` ({L['file'][:-5]}:{L['line']})")
    return ', '.join(out) or '-'


def reason(n):
    if n['status'] == 'exact':
        return n.get('weaker_how') or 'same proposition under the definitions of states and pairs'
    if n['status'] == 'translation':
        return 'translation: ' + n['translation']
    return n.get('weaker_how') or ''


rows = []
for nid in sk:
    n = N[nid]
    rows.append(f"| {name(n)} | {n['short']} | {OLD[n['status_v1']]} | **{NEW[n['status']]}** | {ORG[n['origin']]} | {lean(n, 'project')} | {reason(n)} |")
off = [n for n in bp['nodes'] if n['source'] == 'main' and n['kind'] not in ('example',) and n['id'] not in sk]
rows_off = [f"| {name(n)} | {n['short']} | {OLD[n['status_v1']]} | **{NEW[n['status']]}** | {ORG[n['origin']]} | {lean(n, 'project')} | {reason(n)} |" for n in off]
head = '| statement | content | v1 status | new status | Lean origin | project declarations | reason |\n| --- | --- | --- | --- | --- | --- | --- |'
c = bp['analysis']['status_counts_skeleton']
c1 = bp['analysis']['status_counts_skeleton_v1']
promoted = [nid for nid in sk if N[nid]['status_v1'] == 'refereed' and N[nid]['status'] != 'none']
split_weaker = [nid for nid in sk if N[nid]['status_v1'] == 'checked-form' and N[nid]['status'] == 'weaker']
changed = promoted
md = f"""# Status table, statement by statement

COMPUTED from `proofs/blueprint/blueprint.json` by `scripts/status_table.py`. Paper: `paper/main/barnette.tex` at commit `{bp['paper_commit'][:10]}` (version 2). Statement numbers are unchanged from version 1 (`extract_tex.py --worktree` reports no mismatch against `barnette.aux`).

Old status: the blueprint of `research/2026-11-14_opus_blueprint` (v1), which had three values, exact, "counterpart in different form" (covered) and none.
New status: four values, after the independent rebuild `research/2026-11-14_astra_lean-check`. Where the author's report (`opus_lean-devices`) and the checker disagree, the checker's verdict is used.

- **exact**: the Lean states the same proposition, given the upstream definitions of state and pair.
- **after translation**: the Lean states the proposition in its algebraic-dual model, and the dictionary to the paper's drawing is informal. The translation is named (B1 to B5, see `proofs/blueprint/BLUEPRINT.md`).
- **weaker / different**: the Lean states less, or a different statement that the route can use. The reason says what is missing.
- **none**: no Lean counterpart.

Lean origin: `upstream` = OpenAI's 31 files at `4eaee875`; `added here` = `proofs/lean/Devices`, built by opus_lean-devices and rebuilt from a fresh clone by astra_lean-check; `both` = the counterpart uses both.

## Counts on the route to Theorem 1.1 ({len(sk)} statements)

| | exact | after translation | weaker / different | none |
| --- | --- | --- | --- | --- |
| v1 (opus_blueprint) | {c1.get('checked-exact', 0)} | {c1.get('checked-form', 0)} (one class: "different form") | | {c1.get('refereed', 0)} |
| checker's advisory recount (astra RECOUNT.md) | 5 | 27 (one class) | | 2 |
| **now** | **{c.get('exact', 0)}** | **{c.get('translation', 0)}** | **{c.get('weaker', 0)}** | **{c.get('none', 0)}** |

The new count agrees with the checker's: its 27 is our {c.get('translation', 0)} + {c.get('weaker', 0)}. Splitting the class is new here. It separates statements whose whole content is in the Lean from statements of which the Lean has only part.

Moved out of "none" by the project's Lean, now independently rebuilt: {', '.join('`'+x+'` ('+NEW[N[x]['status']]+')' for x in promoted)}.
The v1 class "different form" (25 statements) splits into {c.get('translation', 0) - sum(N[x]['status']=='translation' for x in promoted)} after translation and {len(split_weaker)} weaker or different: {', '.join('`'+x+'`' for x in split_weaker)}.

## Route statements

{head}
{chr(10).join(rows)}

## Off the route

{head}
{chr(10).join(rows_off)}
"""
(HERE / 'STATUS-TABLE.md').write_text(md, encoding='utf-8')

# tables for BLUEPRINT.md
inv = {}
for e in bp['edges']:
    if e['type'] == 'corresponds-to' and e.get('relation') == 'informal':
        inv.setdefault(e['src'], []).append(e['dst'])
T = ['| paper (v2) | statement | OpenAI | primal note | involution note | Lean upstream (file:line) | Lean added here (file:line) | status | origin |',
     '| --- | --- | --- | --- | --- | --- | --- | --- | --- |']
for n in sorted((n for n in bp['nodes'] if n['source'] == 'main' and n['kind'] != 'example'), key=lambda n: n['line']):
    T.append(f"| {name(n)}{'' if n['id'] in sk else ' (off route)'} | {n['short']} | {n['openai']} | {n['primal']} | {n['involutions']} | {lean(n, 'upstream')} | {lean(n, 'project')} | {NEW[n['status']]} | {ORG[n['origin']]} |")
T += ['', '| primal / involution | Lean | status | paper node |', '| --- | --- | --- | --- |']
for n in bp['nodes']:
    if n['source'] in ('primal', 'involutions'):
        l = ', '.join(('+' if N[x]['origin'] == 'project' else '') + f"`{N[x]['label'].split('.')[-1]}`" for x in n['lean']) or '-'
        m = [k for k, v in inv.items() if n['id'] in v]
        T.append(f"| {n['source']} {n['number']} {n['title'] or n.get('label') or ''} | {l} | {NEW[n['status']]} | {', '.join(m)} |")
(HERE / 'data' / 'tables.md').write_text('\n'.join(T) + '\n', encoding='utf-8')
print('written; changed:', changed)
