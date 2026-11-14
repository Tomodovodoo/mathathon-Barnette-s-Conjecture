"""Build proofs/blueprint/ from the extracted statements and the curation.

Usage (from the repository root, after extract_tex.py and lean_sigs.py):
    python -I research/2026-11-14_opus_lean-integration/scripts/build_blueprint.py

Version 2 (opus_lean-integration): statuses come from curation.V2, which applies the
independent check research/2026-11-14_astra_lean-check; the Lean column includes the
project declarations of proofs/lean/Devices (data/lean-sigs-devices.json).

Writes proofs/blueprint/blueprint.json, blueprint.dot, columns.dot, and renders
blueprint.{pdf,svg} and columns.{pdf,svg} with Graphviz `dot` if it is on PATH or in
C:/Program Files/Graphviz/bin. Prints the analyses used in BLUEPRINT.md and writes
them to research/2026-11-14_opus_blueprint/data/analysis.json.
"""
import json, re, sys, pathlib, shutil, subprocess, collections

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import curation as C  # noqa: E402

ROOT = HERE.parents[2]
DATA = HERE.parent / 'data'
OUT = ROOT / 'proofs/blueprint'

STATUS = {
    'exact': 'exact Lean counterpart',
    'translation': 'Lean counterpart after an unformalised translation',
    'weaker': 'Lean counterpart for a weaker or different form',
    'none': 'no Lean counterpart (refereed by a second model only)',
    'example': 'example (computed)',
}
OLD_STATUS = {'checked-exact': 'exact', 'checked-form': 'different form (v1: counterpart in different form)',
              'refereed': 'none', 'unrefereed': 'none'}
COLOR = {'exact': '#1b7837', 'translation': '#a6dba0', 'weaker': '#fee08b', 'none': '#f4a582', 'example': '#eeeeee'}
FONT = {'exact': 'white', 'translation': 'black', 'weaker': 'black', 'none': 'black', 'example': 'black'}
ORIGIN = {'upstream': 'Lean: upstream', 'project': 'Lean: added here, rebuilt', 'both': 'Lean: upstream + added here', '-': ''}
LEAN_COLOR = {'upstream': '#4d4d4d', 'project': '#2166ac'}


def load(name):
    return json.loads((DATA / name).read_text(encoding='utf-8'))


def lean_lookup(sigs, short):
    hits = [k for k in sigs if k == short or k == 'OAI.Barnette.' + short or k.endswith('.' + short)]
    if not hits:
        raise KeyError(short)
    hits.sort(key=len)
    k = hits[0]
    d = sigs[k]
    return dict(id='lean:' + short, name=k, file=d['file'], line=d['line'], kind=d['kind'], header=d['header'],
                origin=d['origin'])


def status_of(rel, covered, refereed):
    if rel == 'exact' and covered:
        return 'checked-exact'
    if covered:
        return 'checked-form'
    return 'refereed' if refereed else 'unrefereed'


def section_of_line(text, line):
    secs = [(text.count('\n', 0, m.start()) + 1, i + 1) for i, m in enumerate(re.finditer(r'\\section\{', text))]
    s = 0
    for ln, k in secs:
        if ln <= line:
            s = k
    return s


def split_items(stmt):
    parts = re.split(r'\\item\s*', stmt)
    head, items = parts[0], parts[1:]
    items = [re.sub(r'\\end\{enumerate\}.*', '', x).strip() for x in items]
    head = re.sub(r'\\begin\{enumerate\}', '', head).strip()
    return head, items


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    sigs = {k: dict(v, origin='upstream') for k, v in load('lean-sigs-upstream.json').items()}
    sigs.update({k: dict(v, origin='project') for k, v in load('lean-sigs-devices.json').items()})
    from extract_tex import read_src
    tex = read_src('paper/main/barnette.tex')
    main_raw = load('statements-main.json')
    primal_raw = load('statements-primal.json')
    inv_raw = load('statements-involutions.json')

    # ---- merged paper nodes, with parts split and the two proved remarks of Sec 7 added
    nodes = {}
    for n in main_raw:
        if n['id'] in ('lem:duality', 'prop:target'):
            head, items = split_items(n['statement'])
            for i, it in enumerate(items, 1):
                m = dict(n)
                m['id'] = f"{n['id']}.{i}"
                m['number'] = f"{n['number']}({i})"
                m['statement'] = (head + ' (' + str(i) + ') ' + it).strip()
                nodes[m['id']] = m
        else:
            nodes[n['id']] = n
    for rid, anchor, title in [('rem:which', 'Which Hamiltonian cycles arise', 'which Hamiltonian cycles arise'),
                               ('rem:poly', 'The polynomial behind the count', 'the polynomial behind the count')]:
        a = tex.index('\\subsection*{' + anchor)
        b = tex.index('\\subsection*', a + 10)
        body = re.sub(r'\s+', ' ', tex[a:b]).strip()
        nodes[rid] = dict(id=rid, kind='remark', number='Sec 7', label=None, title=title, statement=body, proof=body,
                          line=tex.count('\n', 0, a) + 1, explicit_uses=re.findall(r'\\ref\{([^}]+)\}', body),
                          statement_refs=[], proof_lines=tex[a:b].count('\n'), proof_words=len(body.split()), source='main')
    for n in nodes.values():
        n['section'] = section_of_line(tex, n['line'])

    # ---- check curated uses against explicit citations
    problems = []
    parts = {'lem:duality': ['lem:duality.1', 'lem:duality.2'], 'prop:target': ['prop:target.1', 'prop:target.2']}
    for nid, n in nodes.items():
        if n['kind'] == 'example':
            n['uses'] = []
            continue
        cur = C.MAIN.get(nid)
        if cur is None:
            problems.append(f'no curation for {nid}')
            n['uses'] = []
            continue
        uses = cur['uses']
        for r in n['explicit_uses']:
            if r in C.DROP.get(nid, []):
                continue
            cands = parts.get(r, [r])
            if not any(c in uses for c in cands):
                problems.append(f'{nid}: explicit citation {r} missing from curated uses')
        for u in uses:
            if u not in nodes:
                problems.append(f'{nid}: unknown use {u}')
        n['uses'] = uses
        n['implicit_uses'] = cur['implicit']
    print('consistency problems:', problems or 'none')

    # ---- Lean nodes
    lean = {}

    def L(short):
        if short not in lean:
            lean[short] = lean_lookup(sigs, short)
        return lean[short]['id']

    # ---- statuses and correspondences for the merged paper
    out_nodes, edges = [], []
    for nid, n in nodes.items():
        if n['kind'] == 'example':
            st, cur = 'example', {}
        else:
            cur = C.MAIN[nid]
            old = status_of(cur['rel'], cur['covered'], refereed=True)
            v2 = C.V2[nid]
            st = v2['status']
        rec = dict(id=nid, source='main', label=n['label'], number=n['number'], kind=n['kind'], title=n['title'],
                   section=n['section'], line=n['line'], statement=n['statement'][:1200],
                   proof_lines=n['proof_lines'], proof_words=n['proof_words'],
                   explicit_uses=n.get('explicit_uses', []), implicit_uses=n.get('implicit_uses', []),
                   status=st, status_text=STATUS[st])
        if cur:
            rec.update(status_v1=old, status_v1_text=OLD_STATUS[old], origin=v2['origin'],
                       translation=v2.get('via'), weaker_how=v2.get('how'))
            rec.update(openai=cur['openai'], primal=cur['primal'], involutions=cur['inv'],
                       lean=[L(x) for x in cur['lean'] + v2['lean2']], lean_relation=cur['rel'], lean_route=cur['route'],
                       covered=cur['covered'], bridge=cur.get('bridge'), gap=cur.get('gap'))
            for x in cur['lean'] + v2['lean2']:
                edges.append(dict(src=nid, dst=L(x), type='corresponds-to', relation=cur['rel']))
        if n['kind'] != 'example':
            rec['short'] = short_label(n, rec).split('\\n')[1]
        out_nodes.append(rec)
        for u in n['uses']:
            edges.append(dict(src=nid, dst=u, type='uses'))

    # ---- primal and involution nodes
    for raw, cur_all, src, refereed in [(primal_raw, C.PRIMAL, 'primal', True), (inv_raw, C.INVOLUTIONS, 'involutions', True)]:
        for n in raw:
            cur = cur_all[n['id']]
            old = status_of(cur['rel'], cur['covered'], refereed)
            st = C.V2_NOTES[n['id']]
            lean_ids = cur['lean'] + C.V2_NOTES_LEAN2.get(n['id'], [])
            out_nodes.append(dict(id=n['id'], source=src, label=n['label'], number=n['number'], kind=n['kind'], title=n['title'],
                                  line=n['line'], statement=n['statement'][:1200], proof_lines=n['proof_lines'],
                                  proof_words=n['proof_words'], explicit_uses=n['explicit_uses'], status=st,
                                  status_text=STATUS[st], status_v1=old, lean=[L(x) for x in lean_ids], lean_relation=cur['rel'],
                                  covered=cur['covered'], note=cur.get('note')))
            for u in cur['uses']:
                edges.append(dict(src=n['id'], dst=u, type='uses'))
            for x in lean_ids:
                edges.append(dict(src=n['id'], dst=L(x), type='corresponds-to', relation=cur['rel']))
            if cur.get('main'):
                edges.append(dict(src=cur['main'], dst=n['id'], type='corresponds-to', relation='informal'))
    for k, v in lean.items():
        out_nodes.append(dict(id=v['id'], source='lean', label=v['name'], kind=v['kind'], statement=v['header'],
                              file=v['file'], line=v['line'], origin=v['origin'], status='lean',
                              status_text=('machine-checked upstream (openai/math 4eaee875)' if v['origin'] == 'upstream' else
                                           'machine-checked, added in proofs/lean/Devices; independently rebuilt (astra_lean-check)')))

    # ---- analyses on the merged paper
    G = {n: list(nodes[n]['uses']) for n in nodes if nodes[n]['kind'] != 'example'}

    def anc(x, seen=None):
        seen = set() if seen is None else seen
        for u in G.get(x, []):
            if u not in seen:
                seen.add(u)
                anc(u, seen)
        return seen
    skeleton = anc('thm:main') | {'thm:main'}
    unused = sorted(n for n in G if n not in skeleton)
    used_by = collections.defaultdict(list)
    for a, us in G.items():
        for u in us:
            used_by[u].append(a)
    never_used = sorted(n for n in G if not used_by[n] and n != 'thm:main')
    order = []
    for a, us in G.items():
        for u in us:
            where = nodes[a].get('proof_line') or nodes[a]['line']
            if nodes[u]['line'] > where and nodes[u]['kind'] != 'equation':
                order.append((a, u, where, nodes[u]['line']))
    # longest chain (depth) from a leaf to thm:main
    memo = {}

    def depth(x):
        if x in memo:
            return memo[x]
        best = (0, [x])
        for u in G[x]:
            d, p = depth(u)
            if d + 1 > best[0]:
                best = (d + 1, [x] + p)
        memo[x] = best
        return best
    chain = depth('thm:main')[1]
    # transitive reduction of the skeleton graph
    red = {}
    for a in G:
        keep = []
        for u in G[a]:
            others = [w for w in G[a] if w != u]
            if not any(u in anc(w) for w in others):
                keep.append(u)
        red[a] = keep
    uncovered = [r for r in out_nodes if r['source'] == 'main' and r['status'] == 'none']
    uncovered_route = [r['id'] for r in uncovered if r['id'] in skeleton]
    words_sk = sum(nodes[n]['proof_words'] for n in skeleton)
    words_cov = sum(nodes[n]['proof_words'] for n in skeleton if C.V2[n]['status'] != 'none')
    analysis = dict(skeleton=sorted(skeleton, key=lambda x: nodes[x]['line']), off_skeleton=unused,
                    never_used=never_used, order_problems=order, longest_chain=chain,
                    uncovered_on_route=uncovered_route,
                    uncovered_off_route=[r['id'] for r in uncovered if r['id'] not in skeleton],
                    proof_words_skeleton=words_sk, proof_words_covered=words_cov,
                    status_counts=collections.Counter(r['status'] for r in out_nodes if r['source'] == 'main'),
                    status_counts_skeleton=collections.Counter(r['status'] for r in out_nodes if r['id'] in skeleton),
                    status_counts_skeleton_v1=collections.Counter(r['status_v1'] for r in out_nodes if r['id'] in skeleton),
                    origin_counts_skeleton=collections.Counter((r['status'], r['origin']) and r['origin'] for r in out_nodes if r['id'] in skeleton and r['status'] != 'none'),
                    transitive_reduction=red, consistency_problems=problems)
    (DATA / 'analysis.json').write_text(json.dumps(analysis, indent=1, ensure_ascii=False), encoding='utf-8')
    for k, v in analysis.items():
        if k != 'transitive_reduction':
            print(k, ':', v)

    # ---- write blueprint.json
    OUT.mkdir(parents=True, exist_ok=True)
    bp = dict(
        description='Statement-level blueprint of the Barnette proofs in this repository (version 2: paper version 2, statuses after the independent Lean check).',
        paper_commit=__import__('subprocess').run(['git', '-C', str(ROOT), 'log', '-1', '--format=%H', '--', 'paper/main/barnette.tex'], capture_output=True, text=True).stdout.strip(),
        independent_check='research/2026-11-14_astra_lean-check (fresh clone, Lean 4.34.1, Mathlib d13f23b7; FAITHFULNESS.md, REACHABILITY.md, RECOUNT.md)',
        project_lean='proofs/lean/Devices (29 headline theorems; axioms propext, Classical.choice, Quot.sound)',
        origin_vocabulary=dict(upstream='openai/math@4eaee875 only', project='added in proofs/lean/Devices and independently rebuilt', both='combines the two'),
        sources=dict(main='paper/main/barnette.tex', primal='proofs/primal/primal.tex',
                     involutions='proofs/involutions/involutions.tex', openai='papers/OpenAI-Barnette.pdf',
                     lean='github.com/openai/math lean/OAI/Combinatorics/Hamiltonian at 4eaee87548250b2682affda7d05d947c05554bae',
                     lean_project='proofs/lean/Devices'),
        status_vocabulary=STATUS,
        status_vocabulary_v1=OLD_STATUS,
        relation_vocabulary=dict(exact='same proposition', **{'primal-form': 'same content stated on the cubic graph or the algebraic dual',
                                 'different-form': 'same content with another device (for example phase instead of sign)',
                                 'stronger': 'Lean proves more', 'weaker': 'Lean proves less', 'none': 'no counterpart'}),
        referees=dict(main='research/2026-11-14_sol_referee-main (FOLLOWS)',
                      primal='research/2026-11-14_fable_referee-primal (FOLLOWS, on the pre-revision text; Remarks 14-15 added afterwards)',
                      involutions='research/2026-11-14_opus_referee-involutions (FOLLOWS, commit 45c4cea; one sign error in the off-route Sec 7 comparison)'),
        nodes=out_nodes, edges=edges, analysis={k: v for k, v in analysis.items() if k != 'transitive_reduction'})
    (OUT / 'blueprint.json').write_text(json.dumps(bp, indent=1, ensure_ascii=False), encoding='utf-8')

    write_dot(nodes, red, skeleton, out_nodes)
    write_columns(nodes, out_nodes, lean)
    render()


def short_label(n, rec):
    kind = {'lemma': 'Lemma', 'proposition': 'Prop.', 'theorem': 'Theorem', 'definition': 'Def.',
            'equation': 'Eq.', 'text': 'Text', 'remark': 'Remark'}[n['kind']]
    num = n['number'] if n['kind'] != 'text' else ''
    title = n['title'] or rec.get('title') or ''
    nm = {'thm:main': 'Hamiltonian cycle avoiding e', 'lem:dual': 'the dual is a coloured triangulation',
          'lem:connected': 'faces bounded by cycles => connected', 'eq:counts': 'k black, k white, 3k edges, k+2 vertices',
          'def:selection': 'selection', 'lem:duality.1': 'cycle in N => dual disconnected',
          'lem:duality.2': 'N acyclic => dual connected', 'prop:target.1': 'acyclic selection => HC',
          'prop:target.2': 'two induced trees', 'lem:selections-give-states': 'HC => state',
          'def:state': 'state', 'def:good': 'good state', 'lem:good': 'good <=> S_s spanning tree',
          'lem:Y': 'tree Y_s and selection P_s', 'lem:outdegree': 'outdegree <= 1', 'lem:disk': 'disk identity',
          'prop:recover': 'P_s acyclic', 'def:pair': 'pair', 'lem:partner': 'partner orients Q_s',
          'lem:reversals': 'two reversals', 'lem:sign': 'sign = product of local signs', 'lem:cancel': 'cancellation',
          'lem:height': 'height jump = white faces inside', 'lem:difference': 'finite difference',
          'prop:good': 'a pair gives a good state', 'rem:other-sums': 'other sums', 'eq:hall': 'capacity condition',
          'prop:pair': 'no separating triangle => pair', 'lem:cap': 'caps', 'thm:T': 'acyclic selection containing e0',
          'txt:two-faces': 'two faces share <= 1 side', 'txt:inside': 'inside of a cycle (R_Z)',
          'txt:D': 'D(r,s) = disjoint cycles', 'txt:delta': 'delta, delta-sum = -/+3', 'txt:heights': 'heights along face paths',
          'txt:flow': 'capacity => pair (max-flow)', 'rem:which': 'which HCs arise', 'rem:poly': 'polynomial F(w)'}[n['id']]
    o = ORIGIN.get(rec.get('origin', '-'), '')
    return (f"{kind} {num}\\n{nm}" + (f"\\n[{o}]" if o else '')).replace('  ', ' ')


def write_dot(nodes, red, skeleton, out_nodes):
    recs = {r['id']: r for r in out_nodes}
    secname = {1: '1 Introduction', 2: '2 The dual and the target', 3: '3 Corner choices and the tree of faces',
               4: '4 Pairs of states', 5: '5 The first pair', 6: '6 Separating triangles', 7: '7 Remarks'}
    sk = collections.Counter(recs[n]['status'] for n in skeleton)
    title = ('Paper (paper/main/barnette.tex, version 2): uses-graph, transitive reduction. Arrow A -> B: the proof of B uses A.\\n'
             f"Route to Theorem 1.1: {len(skeleton)} statements; {sk['exact']} exact, {sk['translation']} after an unformalised translation, "
             f"{sk['weaker']} weaker or different form, {sk['none']} no Lean counterpart. Statuses after the independent rebuild (astra_lean-check).")
    L = ['digraph blueprint {', ' rankdir=BT; newrank=true; nodesep=0.3; ranksep=0.5; splines=true; pad=0.3;',
         ' node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=11, margin="0.1,0.05"];',
         ' edge [color="#666666", arrowsize=0.6];',
         f' labelloc=t; fontname="Helvetica"; fontsize=16; label="{title}";']
    secpen = {1: '#000000', 2: '#1f78b4', 3: '#6a3d9a', 4: '#b15928', 5: '#e31a1c', 6: '#33a02c', 7: '#999999'}
    rows = ''.join(f'<TR><TD BGCOLOR="{COLOR[k]}" WIDTH="30">  </TD><TD ALIGN="LEFT">{STATUS[k]}</TD></TR>'
                   for k in ('exact', 'translation', 'weaker', 'none'))
    rows += '<TR><TD></TD><TD ALIGN="LEFT">third line: where the Lean counterpart lives (upstream = openai/math 4eaee875;<BR ALIGN="LEFT"/>added here = proofs/lean/Devices, rebuilt by an independent checker)</TD></TR>'
    rows += '<TR><TD></TD><TD ALIGN="LEFT">dashed border: not needed for Theorem 1.1</TD></TR>'
    rows += ''.join(f'<TR><TD BORDER="2" COLOR="{secpen[k]}">  </TD><TD ALIGN="LEFT">border colour: Sec {v}</TD></TR>' for k, v in secname.items())
    L.append(' subgraph legend { rank=sink; node [shape=plaintext, style="", fontsize=11];')
    L.append('  lg [label=<<TABLE BORDER="1" COLOR="#999999" CELLSPACING="3" CELLPADDING="3">' + rows + '</TABLE>>]; }')
    for nid, n in sorted(nodes.items(), key=lambda kv: kv[1]['line']):
        if n['kind'] == 'example':
            continue
        r = recs[nid]
        st = r['status']
        style = 'rounded,filled' if nid in skeleton else 'rounded,filled,dashed'
        L.append(f' "{nid}" [label="{short_label(n, r)}", fillcolor="{COLOR[st]}", fontcolor="{FONT[st]}", '
                 f'color="{secpen[n["section"]]}", penwidth=2.4, style="{style}"];')
    for a, us in red.items():
        for u in us:
            L.append(f' "{u}" -> "{a}";')
    L.append('}')
    (OUT / 'blueprint.dot').write_text('\n'.join(L), encoding='utf-8')


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def write_columns(nodes, out_nodes, lean):
    recs = {r['id']: r for r in out_nodes}
    head = ['waypoint', 'OpenAI paper', 'paper (version 2)', 'primal note', 'involution note', 'Lean']

    def cell(ids, src):
        items = []
        for i in ids:
            r = recs.get(i) if src != 'lean' else recs.get('lean:' + i)
            if r is None:
                continue
            if src == 'main':
                txt = ' '.join(short_label(nodes[i], r).split('\\n')[:2])
            elif src == 'primal':
                txt = {'PT': 'Theorem T', 'Pcircuit': 'circuit-cut fact'}.get(i, ('Lemma ' if i.startswith('PL') else 'Remark ') + i[2:])
                if r.get('title'):
                    txt += ' ' + r['title'].replace('$', '')
            elif src == 'involutions':
                txt = {'I:main': 'Theorem 1 forest pair', 'I:disk': 'Lemma 2 disk identity', 'I:objects': 'Def. 3 marked objects',
                       'I:one': 'Lemma 4 first involution', 'I:two': 'Lemma 5 second involution', 'I:fixed': 'Lemma 6 fixed points',
                       'I:path-crossings': 'Lemma 7 path crossings', 'I:walk': 'Lemma 8 alternating path'}[i]
            else:
                mark = '+ ' if r['origin'] == 'project' else ''
                txt = mark + i.split('.')[-1] + f"  ({r['file'].replace('.lean', '')}:{r['line']})"
                items.append(f'<TR><TD BGCOLOR="{LEAN_COLOR[r["origin"]]}" ALIGN="LEFT"><FONT COLOR="white">{esc(txt)}</FONT></TD></TR>')
                continue
            col = COLOR[r['status']]
            items.append(f'<TR><TD BGCOLOR="{col}" ALIGN="LEFT"><FONT COLOR="{FONT[r["status"]]}">{esc(txt)}</FONT></TD></TR>')
        if not items:
            items = ['<TR><TD ALIGN="LEFT"><FONT COLOR="#888888">-</FONT></TD></TR>']
        return '<TABLE BORDER="0" CELLSPACING="1" CELLPADDING="3">' + ''.join(items) + '</TABLE>'
    H = ['<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">']
    H.append('<TR>' + ''.join(f'<TD BGCOLOR="#e0e0e0"><B>{h}</B></TD>' for h in head) + '</TR>')
    for w in C.WAYPOINTS_V2:
        name, oai, m, p, i, l = w
        H.append('<TR>' + f'<TD ALIGN="LEFT"><B>{esc(name)}</B></TD><TD ALIGN="LEFT">{esc(oai)}</TD>'
                 + f'<TD>{cell(m, "main")}</TD><TD>{cell(p, "primal")}</TD><TD>{cell(i, "involutions")}</TD><TD>{cell(l, "lean")}</TD></TR>')
    H.append('</TABLE>')
    leg = ''.join(f'<TD BGCOLOR="{COLOR[k]}">{STATUS[k]}</TD>' for k in ('exact', 'translation', 'weaker', 'none'))
    leg2 = (f'<TD BGCOLOR="{LEAN_COLOR["upstream"]}"><FONT COLOR="white">Lean upstream (openai/math 4eaee875)</FONT></TD>'
            f'<TD BGCOLOR="{LEAN_COLOR["project"]}"><FONT COLOR="white">+ Lean added in proofs/lean/Devices, independently rebuilt</FONT></TD>')
    legend = ('<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="2" CELLPADDING="4"><TR>' + leg + '</TR><TR>' + leg2
              + '<TD COLSPAN="2" BORDER="0"></TD></TR></TABLE>')
    dot = ['digraph columns {', ' graph [fontname="Helvetica", pad=0.3];',
           ' node [shape=plaintext, fontname="Helvetica", fontsize=11];',
           ' title [label=<<FONT POINT-SIZE="16">Five-column correspondence, one row per waypoint (paper version 2; statuses after the independent Lean check)</FONT>>];',
           ' leg [label=<' + legend + '>];',
           ' t [label=<' + ''.join(H) + '>];', ' title -> leg -> t [style=invis];', '}']
    (OUT / 'columns.dot').write_text('\n'.join(dot), encoding='utf-8')


def render():
    dot = shutil.which('dot') or r'C:\Program Files\Graphviz\bin\dot.exe'
    for stem in ('blueprint', 'columns'):
        for fmt in ('pdf', 'svg', 'png'):
            subprocess.run([dot, f'-T{fmt}'] + (['-Gdpi=150'] if fmt == 'png' else []) + [str(OUT / f'{stem}.dot'), '-o', str(OUT / f'{stem}.{fmt}')], check=True)
    print('rendered with', dot)


if __name__ == '__main__':
    main()
