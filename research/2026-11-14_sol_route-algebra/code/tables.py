"""Generate TABLES.md from exact count outputs, including every root in grouped rows."""
import json
from pathlib import Path
from collections import defaultdict
OUT=Path(__file__).resolve().parents[1]
d=json.loads((OUT/'counts.json').read_text())
lines=['# Counts and residues','','COMPUTED, T4, unreviewed. Exact integers from `code/count.py --max 14`. The corpus has 55 plantri graphs through 14 vertices, with every one of their 1,206 facial roots, plus the two larger named graphs and all their 72 roots. No enumeration beyond order 14 is claimed. `counts.json` stores edges, roots, mate histograms, all residues, and every primal edge avoidance count.','',
'Commands from repository root:','','```powershell','python -B research/2026-11-14_sol_route-algebra/code/count.py --max 14','python -B research/2026-11-14_sol_route-algebra/code/invariants.py','python -B research/2026-11-14_sol_route-algebra/code/check.py','python -B research/2026-11-14_sol_route-algebra/code/tables.py','```','',
'## Graph totals','','COMPUTED. H counts undirected Hamiltonian cycles without a marked start or direction. Tait counts proper edge colorings with three labeled colors. H avoidance is tabulated per edge in JSON. For a prescribed dual facial edge, the avoided primal edge is its dual.','',
'| Graph | T vertices | Facial roots | States | Tree counts over roots | Pair counts over roots | H | H avoidance values | Tait |',
'|---|---:|---:|---:|---|---|---:|---|---:|']
for g in d['graphs']:
    vals=lambda k:','.join(map(str,sorted({r[k] for r in g['roots']})))
    avoid=','.join(map(str,sorted({a for e,a in g['primal']['avoidance']})))
    lines.append(f"| {g['name']} | {g['vertices']} | {len(g['roots'])} | {vals('states')} | {vals('trees')} | {vals('pairs')} | {g['primal']['hamilton']} | {avoid} | {g['primal']['tait']} |")
lines+=['','## Every root, grouped by equal count data','','COMPUTED. Each row lists all face indices sharing the displayed data. Residue vectors use moduli 2,3,4,5,7,11 in that order. T is both tree-matchings and forest-pairs; the signed unweighted count is zero in every row. A lists the three Hamiltonian avoidance counts at the chosen face, sorted for grouping.','',
'| Graph | Root indices | S | S residues | P | P residues | T | T residues | A |',
'|---|---|---:|---|---:|---|---:|---|---|']
for g in d['graphs']:
    groups=defaultdict(list)
    for r in g['roots']:
        key=(r['states'],r['pairs'],r['trees'],tuple(sorted(r['avoid'+str(i)] for i in range(3))))
        groups[key].append(r['outer'])
    for (s,p,t,a),roots in groups.items():
        res=lambda x:','.join(str(x%m) for m in d['moduli'])
        lines.append(f"| {g['name']} | {','.join(map(str,roots))} | {s} | {res(s)} | {p} | {res(p)} | {t} | {res(t)} | {','.join(map(str,a))} |")
lines+=['','## Specific failures','','COMPUTED. Smallest here means smallest in this corpus, not an unrestricted minimality theorem.','',
'- Odd tree count and signed count one fail on the octahedron, with T=2 and signed count zero.',
'- Universal nonzero tree count mod 3 fails at plantri_13_7, outer face 2, with S=12, P=8, T=6.',
'- Universal nonzero tree count mod 4 fails at plantri_9_0, with T=4 at its unobstructed roots.',
'- Universal nonzero tree count mod 5 fails at a 14-vertex rooted example, as the full table records.',
'- Unrooted invariant equality fails on plantri_12_2, whose tree counts vary between 2 and 8 with the root even though all roots admit pairs.',
'- All unweighted signed counts vanish. Positive existence certificates must retain a statistic or select another coefficient.','',
'## Independent small checks','','COMPUTED. `code/check.py` uses all permutations for states, disjoint-set cycle detection after root contraction for trees, and path DFS for Hamiltonian cycles and avoidance. See `checks.json` for its completed range. This is a second implementation by the author, not an independent referee.','',
'## Invariant comparisons','','COMPUTED. `invariants.json` gives full Tutte polynomials of all three two-color vertex graphs, and all six hypergraph interior/exterior polynomials, for all five plantri graphs of orders 6,8,9,10. Interior and exterior coefficients are dictionaries indexed by inactivity exponent. Their evaluations at one equal S in these data.','',
'| Example | T | S | Three graph T(1,1) values | Six hypergraph I(1)=X(1) values | Tait / Penrose P_G(3) | Z3 flows on primal G |',
'|---|---:|---:|---|---|---:|---:|']
iv=json.loads((OUT/'invariants.json').read_text())
for r in iv:
    g=next(g for g in d['graphs'] if g['name']==r['name'])
    lines.append(f"| {r['name']} | {r['trees']} | {r['states']} | {','.join(str(x['evaluations']['(1, 1)']) for x in r['trinity_graphs'])} | {','.join(str(h['hypertrees']) for x in r['trinity_graphs'] for h in x['hypergraphs'])} | {g['primal']['tait']} | 2 |")
lines+=['','LIT. The interpretation of Penrose P_G(3) as labeled Tait colorings is the standard plane cubic specialization. Source identification and access limits are in ROUTES.md. COMPUTED values here enumerate the colorings; they do not independently evaluate the Penrose state sum. The Z3 flow value follows from PROOF 2, not a flow enumeration. No root-normalized or coefficient-extracted invariant identity has been excluded.']
(OUT/'TABLES.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(len(lines),'table lines')
