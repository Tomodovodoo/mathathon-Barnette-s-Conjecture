"""Turn data/census_V.txt (output of descent.exe) into data/census_summary.json and markdown tables.
Usage: python summarize.py > ../data/census_tables.md
"""
import re, json, glob, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
rows = {}; tot = {}
for fn in glob.glob(os.path.join(D, 'census_[0-9]*.txt')):
    for line in open(fn):
        if line.startswith('T '):
            d = dict(x.split('=') for x in line.split()[1:])
            tot[int(d['V'])] = {k: int(v) for k, v in d.items()}
        elif line.startswith('K '):
            V = int(line.split()[1].split('=')[1])
            tot.setdefault(V, {})['khist'] = {a.split(':')[0]: int(a.split(':')[1]) for a in line.split()[3:]}
        elif line.startswith('S '):
            m = re.match(r'S V=(\d+) pot=(\S+) nontarget=(\d+) trap1=(\d+)\(inst (\d+)\) trap2=(\d+)\(inst (\d+)\) sinks=(\d+)\(inst (\d+)\) maxrho=(\d+) maxmono=(\d+) maxstrictlen=(\d+) rhohist (.*)', line)
            V = int(m.group(1))
            rows.setdefault(m.group(2), {})[V] = dict(nontarget=int(m.group(3)), trap1=int(m.group(4)), trap1_inst=int(m.group(5)),
                trap2=int(m.group(6)), trap2_inst=int(m.group(7)), sinks=int(m.group(8)), sinks_inst=int(m.group(9)),
                maxrho=int(m.group(10)), maxmono=int(m.group(11)), maxstrictlen=int(m.group(12)), rhohist=m.group(13).strip())
json.dump(dict(totals=tot, potentials=rows), open(os.path.join(D, 'census_summary.json'), 'w'), indent=1, sort_keys=True)
Vs = sorted(tot)
print('## Totals\n')
print('| V | rooted instances with a pair | 2-factors | pairs | tree pairs | k=1 | k=2 | k=3 | components of E | largest distance to a tree pair |')
print('|---|---|---|---|---|---|---|---|---|---|')
for V in Vs:
    t = tot[V]; kh = t.get('khist', {})
    print(f"| {V} | {t['rooted_with_pair']:,} | {t['factors']:,} | {t['pairs']:,} | {t['tree_pairs']:,} | {kh.get('1',0):,} | {kh.get('2',0):,} | {kh.get('3',0):,} | {t['components']:,} | {t['max_free_dist']} |")
s = lambda key: sum(tot[V][key] for V in Vs)
print(f"| all | {s('rooted_with_pair'):,} | {s('factors'):,} | {s('pairs'):,} | {s('tree_pairs'):,} | | | | {s('components'):,} | |")


def first(pot, key):
    for V in Vs:
        if rows[pot].get(V, {}).get(key, 0) > 0:
            return V
    return None


print('\n## Verdict per potential (single moves, macro moves of length <= 2)\n')
print('| potential | first V with a pair trapped under non-increasing single moves | same with macro moves of length <= 2 | first V with a strict local minimum that is not a tree pair | largest escape radius, V <= 22 | longest shortest non-increasing path, V <= 22 | longest strictly decreasing path, V <= 22 |')
print('|---|---|---|---|---|---|---|')
for pot in rows:
    r = rows[pot]
    f1, f2, fs = first(pot, 'trap1'), first(pot, 'trap2'), first(pot, 'sinks')
    mr = max(x['maxrho'] for x in r.values()); mm = max(x['maxmono'] for x in r.values()); ms = max(x['maxstrictlen'] for x in r.values())
    print(f"| `{pot}` | {f1 or 'none'} | {f2 or 'none'} | {fs or 'none'} | {'no smaller value in the component' if mr == 99 else mr} | {mm} | {ms} |")
print('\n## Counts at each V for the main potentials\n')
for pot in ['k', '(k,+om)', '(k,-om)', '(k,+psi,-om)', '(k,+psi,+om)', 'k+c', '(c,wq)']:
    print(f'\n`{pot}`\n')
    print('| V | non-tree pairs | trapped (single moves) | trapped (length <= 2) | strict local minima | escape radius histogram |')
    print('|---|---|---|---|---|---|')
    for V in Vs:
        x = rows[pot].get(V)
        if x and x['nontarget']:
            hist = ' '.join(a for a in x['rhohist'].split() if not a.endswith(':0')).replace('7:', '>=7 or none:')
            print(f"| {V} | {x['nontarget']:,} | {x['trap1']:,} | {x['trap2']:,} | {x['sinks']:,} | {hist} |")
