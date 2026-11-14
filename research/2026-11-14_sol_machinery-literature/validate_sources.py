from pathlib import Path
import hashlib
import json
import re
import sys
import sympy

p = Path(__file__).resolve().parent
required = ['MACHINERY.md', 'REFORMULATIONS.md', 'ROUTE-IDEAS.md',
            'bibliography.bib', 'REPORT.md', 'pdf/INDEX.md', 'SOURCES.md']
assert all((p / f).exists() for f in required)
bib = (p / 'bibliography.bib').read_text(encoding='utf-8-sig')
keys = re.findall(r'^@\w+\{([^,]+),', bib, re.M)
assert len(keys) == len(set(keys)) == 47
for source in json.loads((p / 'downloads.json').read_text(encoding='utf-8')):
    if source['status'] == 'downloaded and text extracted':
        f = p / 'pdf' / (source['key'] + '.pdf')
        assert hashlib.sha256(f.read_bytes()).hexdigest() == source['sha256']
index = (p / 'pdf' / 'INDEX.md').read_text(encoding='utf-8')
for link in re.findall(r'\]\(([^)]+\.pdf)\)', index):
    assert (p / 'pdf' / link).exists(), link
routes = (p / 'ROUTE-IDEAS.md').read_text(encoding='utf-8')
forms = (p / 'REFORMULATIONS.md').read_text(encoding='utf-8')
assert len(re.findall(r'^## \d+\.', routes, re.M)) == 18
assert len(re.findall(r'^## \d+\.', forms, re.M)) == 11
assert bib.count('{') == bib.count('}')
results = dict(required_files='pass', bibliography_records=len(keys),
               pdf_count=len(list((p / 'pdf').glob('*.pdf'))),
               checksums='pass', local_pdf_links='pass', ranked_routes=18,
               numbered_reformulations=11, python=sys.version,
               sympy=sympy.__version__,
               command='python research/2026-11-14_sol_machinery-literature/validate_sources.py')
(p / 'validation.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
print(json.dumps(results, indent=2))
