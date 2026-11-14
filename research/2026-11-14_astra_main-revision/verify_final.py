"""Mechanical checks complementing the visual and mathematical read-through."""
from pathlib import Path
import collections, hashlib, json, re, subprocess
import fitz

root = Path(__file__).resolve().parent
repo = root.parents[1]
main = repo / 'paper/main'
src = (main / 'barnette.tex').read_text(encoding='utf-8')
assert '\u2014' not in src and '---' not in src
assert src.count('% AUTHOR LINE: to be decided by the project owner') == 1
assert r'\author{}' in src
stack = []
objects = []
protected = {'proof','theorem','lemma','proposition','example','remark','definition'}
for m in re.finditer(r'\\(begin|end)\{([^}]+)\}(\[[^]]*\])?', src):
    action, name, opt = m.groups()
    if action == 'begin':
        if name in {'figure','table'}:
            assert not protected.intersection(stack), (name, stack)
            assert opt == '[H]', (name, opt)
            objects.append(name)
        stack.append(name)
    else:
        assert stack.pop() == name
assert not stack
log = (main / 'barnette.log').read_text(errors='replace')
assert not re.search(r'Undefined|undefined|Overfull|Warning|^!', log, re.M)
assert 'Warning' not in (main / 'barnette.blg').read_text(errors='replace')
labels = re.findall(r'\\label\{([^}]+)\}', src)
assert len(labels) == len(set(labels))
assert set(re.findall(r'\\(?:eqref|ref)\{([^}]+)\}', src)) <= set(labels)
doc = fitz.open(main / 'barnette.pdf')
textwidth = doc[0].rect.width - 144
sizes = []
for m in re.finditer(r'\\includegraphics\[width=(.*?)\\textwidth\]\{\\FIG (.*?)\}', src):
    ratio = float(m[1] or 1)
    d = fitz.open(repo / 'paper/figures' / m[2])
    # Ordinary numeral labels, excluding tiny math subscripts and superscripts.
    spans = [s for b in d[0].get_text('dict')['blocks'] if b['type'] == 0
             for line in b['lines'] for s in line['spans']]
    base = collections.Counter(round(s['size'], 3) for s in spans if s['size'] > 7.9).most_common(1)[0][0]
    final = base * ratio * textwidth / d[0].rect.width
    assert final > 7.9, (m[2], final)
    sizes.append({'figure': m[2], 'body_label_bp_at_final_scale': round(final, 3)})
for name, cmd in [('example', ['python', str(root/'example.py')]),
                  ('independent-check', ['python', str(root/'independent/examples.py')]),
                  ('figure-check', ['python', 'paper/figures/check.py'])]:
    run = subprocess.run(cmd, cwd=repo, capture_output=True, text=True, errors='replace')
    (root / (name+'.txt')).write_text(run.stdout+run.stderr, encoding='utf-8')
    assert run.returncode == 0, (name, run.stdout[-1000:],run.stderr)
result = {'status': 'COMPUTED', 'pages': len(doc),
          'fixed_objects': dict(collections.Counter(objects)),
          'no_object_inside_statement_proof_example': True,
          'latex_warnings_undefined_references_overfull_boxes': 0,
          'figure_label_sizes': sizes,
          'sha256': {str(p.relative_to(repo)): hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in [main/'barnette.tex',main/'barnette.pdf',main/'refs.bib',
                               main/'history/barnette-v1.tex',main/'history/barnette-v1.pdf']}}
(root/'verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
