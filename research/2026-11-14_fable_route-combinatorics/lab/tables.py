"""Markdown tables from the survey output.  usage: python tables.py ../data/rows_v16.json"""
import sys, json
from collections import defaultdict, Counter

rows = json.load(open(sys.argv[1]))
byV = defaultdict(list)
for r in rows:
    byV[r['V']].append(r)

print("### Summary by number of vertices of T\n")
print("| V(T) | N=|V(G)| | n | classes | rooted (T,t0) | with a pair | states (min..max) | pairs (max) | tree matchings (min..max over rooted with a pair) | cmin values | max trees/2^cmin |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for V in sorted(byV):
    rs = byV[V]
    wp = [r for r in rs if r['pairs'] > 0]
    cm = Counter(r['cmin'] for r in wp)
    print(f"| {V} | {2*V-4} | {V-3} | {len({r['cls'] for r in rs})} | {len(rs)} | {len(wp)} | "
          f"{min(r['states'] for r in rs)}..{max(r['states'] for r in rs)} | {max(r['pairs'] for r in rs)} | "
          f"{min(r['trees'] for r in wp)}..{max(r['trees'] for r in wp)} | "
          f"{', '.join(f'{k}: {v}' for k, v in sorted(cm.items()))} | "
          f"{max(r['trees'] / 2 ** r['cmin'] for r in wp):g} |")

print("\n### Distinct rooted profiles, V(T) <= 12\n")
print("| V | class | #t0 with this profile | sep. triangles | states | partnered states | pairs | D by cycle count | cmin | lead | tree matchings (+/-) | partner-count histogram k: #s | HC of G | HC avoiding each edge of t0 |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for V in sorted(byV):
    if V > 12:
        continue
    prof = Counter()
    for r in byV[V]:
        key = (r['cls'], r['sep'], r['states'], r['partnered'], r['pairs'], json.dumps(r.get('D_hist', {})),
               r.get('cmin'), r.get('lead'), r['trees_plus'], r['trees_minus'], json.dumps(r['k_hist']),
               r['hams'], tuple(sorted(r['hc_avoid'])))
        prof[key] += 1
    for key in sorted(prof, key=lambda k: (k[0], k[2])):
        (cls, sep, st, pa, pr, dh, cm, lead, tp, tm, kh, hams, hca) = key
        print(f"| {V} | {cls} | {prof[key]} | {sep} | {st} | {pa} | {pr} | {dh} | {cm} | {lead} | {tp+tm} ({tp}/{tm}) | {kh} | {hams} | {list(hca)} |")

print("\n### Tree matchings against 2^cmin (rooted triangulations with a pair)\n")
c = Counter()
for r in rows:
    if r['pairs']:
        c[(r['cmin'], r['trees'])] += 1
print("| cmin | tree matchings | how many rooted triangulations |")
print("|---|---|---|")
for (m, t) in sorted(c):
    print(f"| {m} | {t} | {c[(m, t)]} |")
