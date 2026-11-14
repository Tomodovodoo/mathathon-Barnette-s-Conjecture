"""Keep exact new text visible in REFEREE.md as well as in EDITS.md."""
from pathlib import Path
import json

base=Path(__file__).resolve().parents[1]
p=base/'REFEREE.md'
text=p.read_text(encoding='utf-8')
start='## Exact replacement texts\n'
end='## Verification of the core obligations\n'
if start in text:
    a=text.index(start); b=text.index(end,a); text=text[:a]+text[b:]
pairs=json.loads((base/'code/edits.json').read_text(encoding='utf-8'))
mapping={'E1':'F1','E2':'F3','E3':'F4','E4':'F7','E5':'F5','E6':'F2','E7':'F2','E8':'F6'}
replacement=start+'\nThese are the exact proposed new strings. EDITS.md supplies their unique old strings. Status PROVED-HERE for mathematical repairs and COMPUTED for the added range.\n\n'
for pair in pairs:
    replacement+=f"### {pair['id']} for {mapping[pair['id']]}, source line {pair['line']}\n\n```tex\n{pair['new']}\n```\n\n"
assert text.count(end)==1
p.write_text(text.replace(end,replacement+end),encoding='utf-8')
print('Inserted eight exact replacement texts before the verification and dependency table.')
