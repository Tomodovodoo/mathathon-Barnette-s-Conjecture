"""Extract numbered statements, their proofs and cited labels from the three TeX sources.

Usage (from the repository root):
    python -I research/2026-11-14_opus_blueprint/scripts/extract_tex.py [--worktree]

By default the sources are read with `git show` at the pinned commit REV (the text the
referees read); --worktree reads the working tree instead (output suffix -worktree).

Writes research/2026-11-14_opus_blueprint/data/statements-{main,primal,involutions}.json.

For every statement: id, kind, number, label, title, statement text, proof text,
explicit uses (labels cited inside the proof, and inside the statement), proof length
in source lines and words, and the source line where the statement starts.

paper/main/barnette.tex uses amsthm environments sharing the equation counter
within each section; numbers are recomputed here and checked against barnette.aux.
Load-bearing claims made in running text (no environment) are added as "text" nodes
from fixed anchors; their extent is the paragraph that contains the anchor.
proofs/primal/primal.tex uses bold run-in headings ("\\textbf{Lemma 5, ...}"); a
statement runs to "Proof." and the proof to the next heading.
proofs/involutions/involutions.tex uses amsthm with \\label.
"""
import json, re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).resolve().parents[1] / 'data'
REV = 'b0fc398a303cb6522ab016d17a269996e0a6fa72'  # pinned: the refereed text of all three notes


def read_src(rel):
    """Source text at the pinned commit (pass --worktree to read the working tree)."""
    if '--worktree' in sys.argv:
        return (ROOT / rel).read_text(encoding='utf-8')
    import subprocess
    return subprocess.run(['git', '-C', str(ROOT), 'show', f'{REV}:{rel}'], capture_output=True,
                          check=True).stdout.decode('utf-8')


ENVS = ['theorem', 'proposition', 'lemma', 'definition', 'example', 'remark']


def words(s):
    return len(re.findall(r'[A-Za-z0-9]+', re.sub(r'\\[a-zA-Z]+', ' ', s)))


def lineno(text, pos):
    return text.count('\n', 0, pos) + 1


def refs(s):
    return sorted(set(re.findall(r'\\(?:eq)?ref\{([^}]+)\}', s)), key=s.find)


def strip(s):
    s = re.sub(r'\\label\{[^}]*\}', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()


# ---------------------------------------------------------------- merged paper
def main_paper():
    text = read_src('paper/main/barnette.tex')
    auxp = ROOT / 'paper/main/barnette.aux'
    # the aux file is untracked; it is only a cross-check and matches the working tree build
    aux = auxp.read_text(encoding='utf-8') if (auxp.exists() and '--worktree' in sys.argv) else ''
    auxnum = dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}', aux))
    body = text[text.index('\\begin{document}'):]
    off = text.index('\\begin{document}')
    tokens = re.compile(r'\\section\{|\\begin\{(' + '|'.join(ENVS) + r'|equation|proof)\}(\[[^\]]*\])?')
    sec = 0
    cnt = 0
    nodes = []
    pos = 0
    last = None
    while True:
        m = tokens.search(body, pos)
        if not m:
            break
        if m.group(0).startswith('\\section'):
            sec += 1
            cnt = 0
            pos = m.end()
            continue
        env = m.group(1)
        end = body.index('\\end{%s}' % env, m.end())
        inner = body[m.end():end]
        if env == 'proof':
            opt = m.group(2) or ''
            target = None
            r = refs(opt)
            if r:
                target = next((n for n in nodes if n['label'] == r[0]), None)
            elif last is not None and not body[last['_end']:m.start()].strip():
                target = last
            if target is not None and target['proof'] is None:
                target['proof'] = inner.strip()
                target['proof_line'] = lineno(text, off + m.start())
            pos = end
            continue
        cnt += 1
        number = f'{sec}.{cnt}'
        lab = re.search(r'\\label\{([^}]+)\}', inner)
        label = lab.group(1) if lab else None
        if env == 'equation':
            if label:
                nodes.append(dict(id=label, kind='equation', number=f'({number})', label=label,
                                  title='', statement=strip(inner), proof=None,
                                  line=lineno(text, off + m.start()), _end=end + len('\\end{equation}')))
            pos = end
            last = None
            continue
        title = (m.group(2) or '')[1:-1]
        nid = label or f'{env[:3]}:{number}'
        node = dict(id=nid, kind=env, number=number, label=label, title=title,
                    statement=strip(inner), proof=None, line=lineno(text, off + m.start()),
                    _end=end + len('\\end{%s}' % env))
        if label and auxnum.get(label) not in (None, number):
            print('NUMBER MISMATCH', label, auxnum.get(label), number, file=sys.stderr)
        nodes.append(node)
        last = node
        pos = end
    # names for the unlabeled definitions
    names = {'selection': 'def:selection', 'state}': 'def:state', 'good}': 'def:good', 'pair}': 'def:pair'}
    for n in nodes:
        if n['kind'] == 'definition' and n['label'] is None:
            for key, nid in names.items():
                if '\\emph{' + key in n['statement']:
                    n['id'] = nid
    # load-bearing text claims: (id, anchor regex, title)
    anchors = [
        ('txt:two-faces', r'Two faces share at most one side', 'two faces share at most one side'),
        ('txt:inside', r'Euler\'s formula needs a connected plane graph', 'the inside of a directed cycle Z is a connected plane graph R_Z'),
        ('txt:D', r'Besides \$Q_s\$ a pair gives the set', 'D(r,s) is a disjoint union of directed cycles covering X'),
        ('txt:delta', r'For adjacent vertices \$v,w\$ put', 'definition of delta; delta-sum of a cycle of chosen sides is -3 ccw, +3 cw'),
        ('txt:heights', r'For each white face \$y\$ fix a path of faces', 'heights eta_s(y) and weight omega(s) along fixed paths of faces'),
        ('txt:flow', r'Let \$\\mathcal\{B\}\$ be the bipartite graph', 'a pair exists if the capacity condition (5.1) holds (max-flow)'),
    ]
    for nid, pat, title in anchors:
        mm = re.search(pat, text)
        if mm is None:
            print('anchor missing:', nid, file=sys.stderr)
            continue
        a = text.rfind('\n\n', 0, mm.start()) + 2
        if nid == 'txt:flow':  # paragraph plus the displayed condition
            b = text.index('\\end{equation}', mm.start()) + len('\\end{equation}')
        else:
            b = text.find('\n\n', mm.start())
        para = text[a:b]
        nodes.append(dict(id=nid, kind='text', number='', label=None, title=title,
                          statement=strip(para), proof=strip(para), line=lineno(text, a), _end=None))
    # the three-count equation eq:counts has its derivation in the preceding sentence
    for n in nodes:
        if n['id'] == 'eq:counts' and r'Each edge of $\T$ has exactly one black face and each black face' in text:
            a = text.index('Each edge of $\\T$ has exactly one black face and each black face')
            n['proof'] = strip(text[a:text.index('\\begin{equation}\\label{eq:counts}')])
        if n['id'] == 'eq:density':
            n['proof'] = '(inside the proof of Proposition 5.2)'
    for n in nodes:
        pr = n['proof'] or ''
        n['explicit_uses'] = [r for r in refs(pr) if not r.startswith(('fig:', 'tab:', 'sec:'))]
        n['statement_refs'] = [r for r in refs(n['statement']) if not r.startswith(('fig:', 'tab:', 'sec:'))]
        n['proof_lines'] = pr.count('\n') + (1 if pr else 0)
        n['proof_words'] = words(pr)
        n['source'] = 'main'
        n.pop('_end', None)
    return nodes


# ---------------------------------------------------------------- primal note
def primal():
    text = read_src('proofs/primal/primal.tex')
    stop = text.index('\\clearpage\\section*{Primal-dual dictionary}')
    text_main = text[:stop]
    head = re.compile(r'\\textbf\{((?:Lemma|Remark) (\d+)|Theorem T|General circuit-cut fact)([^}]*)\}|\\section\*\{|Proof of Theorem T\.')
    marks = [m for m in head.finditer(text_main)]
    nodes = []
    for i, m in enumerate(marks):
        if m.group(0).startswith('\\section') or m.group(0).startswith('Proof of Theorem'):
            continue
        name = m.group(1)
        nxt = marks[i + 1].start() if i + 1 < len(marks) else len(text_main)
        chunk = text_main[m.end():nxt]
        if name.startswith('Lemma') or name.startswith('Remark'):
            kind = name.split()[0].lower()
            nid = f'P{kind[0].upper()}{m.group(2)}'
            number = m.group(2)
        elif name == 'Theorem T':
            kind, nid, number = 'theorem', 'PT', 'T'
        else:
            kind, nid, number = 'lemma', 'Pcircuit', 'circuit-cut fact'
        k = chunk.find('Proof.')
        statement, proof = (chunk[:k], chunk[k + 6:]) if k >= 0 else (chunk, '')
        if nid == 'PT':
            pm = re.search(r'Proof of Theorem T\.(.*?)\\section\*', text_main, re.S)
            proof = pm.group(1)
        title = m.group(3).strip(' ,.')
        uses = []
        for mm in re.finditer(r'Lemmas? (\d+)(?: (?:through|and|to) (\d+))?', proof):
            a = int(mm.group(1)); b = int(mm.group(2) or a)
            uses += [f'PL{x}' for x in range(a, b + 1)]
        for mm in re.finditer(r'\((\d)\.(\d)\)', proof):
            tag = f'{mm.group(1)}.{mm.group(2)}'
            owner = {'2.1': 'PL2', '2.2': 'PL3', '3.1': 'PL4', '4.1': 'PL5', '4.2': 'PL5',
                     '5.1': 'PL6', '5.2': 'PL6', '6.1': 'def-Z', '6.2': 'PL7', '6.3': 'PL8', '6.4': 'PL8'}.get(tag)
            if owner and owner != nid and owner != 'def-Z':
                uses.append(owner)
        if 'general fact' in proof or 'circuit-cut' in proof:
            uses.append('Pcircuit')
        uses = [u for u in dict.fromkeys(uses) if u != nid]
        nodes.append(dict(id=nid, kind=kind, number=number, label=None, title=title,
                          statement=strip(statement), proof=strip(proof), line=lineno(text, m.start()),
                          explicit_uses=uses, statement_refs=[], proof_lines=proof.strip().count('\n') + 1,
                          proof_words=words(proof), source='primal'))
    return nodes


# ---------------------------------------------------------------- involution note
def involutions():
    text = read_src('proofs/involutions/involutions.tex')
    envs = ['theorem', 'lemma', 'definition']
    nodes = []
    cnt = 0
    tokens = re.compile(r'\\begin\{(theorem|lemma|definition|proof)\}(\[[^\]]*\])?')
    last = None
    pos = 0
    while True:
        m = tokens.search(text, pos)
        if not m:
            break
        env = m.group(1)
        end = text.index('\\end{%s}' % env, m.end())
        inner = text[m.end():end]
        if env == 'proof':
            opt = m.group(2) or ''
            r = refs(opt)
            target = next((n for n in nodes if n['label'] == r[0]), None) if r else last
            if target is not None and target['proof'] is None:
                target['proof'] = inner.strip()
            pos = end
            continue
        cnt += 1
        lab = re.search(r'\\label\{([^}]+)\}', inner).group(1)
        node = dict(id='I:' + lab, kind=env, number=str(cnt), label=lab, title=(m.group(2) or '')[1:-1],
                    statement=strip(inner), proof=None, line=lineno(text, m.start()))
        nodes.append(node)
        last = node if env != 'definition' else None
        pos = end
    for n in nodes:
        pr = n['proof'] or ''
        n['explicit_uses'] = ['I:' + r for r in refs(pr)]
        n['statement_refs'] = ['I:' + r for r in refs(n['statement'])]
        n['proof_lines'] = pr.count('\n') + (1 if pr else 0)
        n['proof_words'] = words(pr)
        n['source'] = 'involutions'
    return nodes


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    OUT.mkdir(exist_ok=True)
    for name, fn in [('main', main_paper), ('primal', primal), ('involutions', involutions)]:
        nodes = fn()
        suffix = '-worktree' if '--worktree' in sys.argv else ''
        (OUT / f'statements-{name}{suffix}.json').write_text(json.dumps(nodes, indent=1, ensure_ascii=False), encoding='utf-8')
        print(f'{name}: {len(nodes)} statements')
        for n in nodes:
            print(f"  {n['id']:28s} {n['kind']:11s} {n['number']:6s} L{n['line']:<4d} proof {n['proof_lines']:3d} lines {n['proof_words']:4d} words  uses {n['explicit_uses']}")
