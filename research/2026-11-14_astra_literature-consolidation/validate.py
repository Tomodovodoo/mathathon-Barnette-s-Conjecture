"""Validate the curated library without writing outside the assigned folder."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

R = Path('research/2026-11-14_astra_literature-consolidation')
rows = json.loads((R / 'catalog.json').read_text(encoding='utf-8'))
manifest = json.loads((R / 'manifest.json').read_text(encoding='utf-8'))
bib = Path('papers/barnette.bib').read_text(encoding='utf-8')
keys = re.findall(r'@\w+\{([^,]+),', bib)
assert len(keys) == len(set(keys)) == len(rows)
assert set(keys) == {r['key'] for r in rows}
assert len({m['sha256'] for m in manifest}) == len(manifest)
for m in manifest:
    data = Path(m['filename']).read_bytes()
    assert data.startswith(b'%PDF'), m['filename']
    assert len(data) == m['size'], m['filename']
    assert hashlib.sha256(data).hexdigest() == m['sha256'], m['filename']
assert {p.as_posix() for p in Path('papers').rglob('*.pdf')} == {m['filename'] for m in manifest}
for name in ['OpenAI-Barnette.pdf', 'A-Note-On-Barnette.pdf', 'barnette_trees.pdf']:
    committed = subprocess.check_output(['git', 'show', 'HEAD:papers/' + name])
    assert committed == (Path('papers') / name).read_bytes(), name
for r in rows:
    assert r['use'] and r['dependency'] and r['verified'], r['key']
    if not r['local'].startswith('not held'):
        assert (Path('papers') / r['local']).is_file(), r['key']
    assert '[' not in r['key'] and '\\' not in r['key'], r['key']
assert '10.1137/1.9781611973105.28' not in bib, 'rejected Thomas search hit'
assert '10.1017/cbo9780511566059.004' not in bib, 'rejected Alon search hit'
summary = (
    '# Validation\n\n'
    f'- {len(rows)} catalogue records and unique BibTeX keys; exact coverage.\n'
    f'- {len(manifest)} held PDFs; all headers, hashes and sizes match.\n'
    '- No duplicate SHA-256 among held PDFs.\n'
    '- All three original PDFs match the committed originals byte for byte.\n'
    '- Every row has a project use, dependency and verification field.\n'
    '- Rejected metadata search hits were not imported.\n'
    f'- Total held PDF bytes: {sum(m["size"] for m in manifest):,}.\n\n'
    'Command: `python research/2026-11-14_astra_literature-consolidation/validate.py`.\n'
    'This checks library consistency, not mathematical correctness or completeness of historical metadata.\n'
)
(R / 'VALIDATION.md').write_text(summary, encoding='utf-8')
print(summary)
