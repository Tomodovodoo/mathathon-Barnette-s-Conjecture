"""Analyse contraction rows: monotone laws, deletion-contraction identities, lift statistics.
usage: python analyse_contract.py file1.jsonl [file2.jsonl ...]"""
import sys, json
from collections import defaultdict, Counter

rows = []
for fn in sys.argv[1:]:
    with open(fn) as f:
        rows += [json.loads(l) for l in f]
print('rows', len(rows), 'V range', min(r['V'] for r in rows), max(r['V'] for r in rows))
ok = [r for r in rows if not r['loop']]
print('loop (p~q) rows', len(rows) - len(ok))
simple = [r for r in ok if r['simple']]
print('non-loop', len(ok), 'simple', len(simple))


def show(b):
    return 'V=%d gid=%d t0=%d x=%d merge %d<-%d rootnbrs=%d' % (b['V'], b['gid'], b['t0'], b['x'], b['p'], b['q'], b['rootnbrs']) + ' ' + \
        str({k: (b['T'].get(k), b['Tp'].get(k)) for k in ('states', 'pairs', 'TM', 'cmin', 'lc')}) + \
        ' ' + str({k: b.get(k, 0) for k in ('A', 'B', 'C', 'b', 'LC')})


def law(name, pred, rs):
    bad = [r for r in rs if not pred(r)]
    print(f'{name:62s} {len(rs)-len(bad):7d}/{len(rs):<7d}', end='')
    if bad:
        b = min(bad, key=lambda r: (r['V'], r['gid']))
        print('  FAIL e.g. ' + show(b))
    else:
        print('  holds')
    return bad


for label, rs in (('simple T\'', simple), ('all T\' (multigraphs allowed)', ok),
                  ('simple T\', x has no root neighbour', [r for r in simple if r['rootnbrs'] == 0])):
    print('==', label)
    law('TM(T) >= TM(T\')', lambda r: r['T']['TM'] >= r['Tp']['TM'], rs)
    law('states(T) >= states(T\')', lambda r: r['T']['states'] >= r['Tp']['states'], rs)
    law('pairs(T) >= pairs(T\')', lambda r: r['T']['pairs'] >= r['Tp']['pairs'], rs)
    law('lc(T) >= lc(T\')', lambda r: r['T']['lc'] >= r['Tp']['lc'], rs)
    law('cmin(T) <= cmin(T\') (both have pairs)', lambda r: r['T']['cmin'] is None or r['Tp']['cmin'] is None or r['T']['cmin'] <= r['Tp']['cmin'], rs)
    law('pair(T) => pair(T\')', lambda r: r['T']['pairs'] == 0 or r['Tp']['pairs'] > 0, rs)
    law('[old Lemma 6.2(iii)] B == 0 (projection of lift-type TM is TM)', lambda r: r.get('B', 0) == 0, rs)
    law('LC => preimage TM (LCbad == 0)', lambda r: r.get('LCbad', 0) == 0, rs)
    law('some TM of T\' lifts (A>0 when TM(T\')>0)', lambda r: r['Tp']['TM'] == 0 or r['A'] > 0, rs)
    law('some TM of T\' satisfies LC (when TM(T\')>0)', lambda r: r['Tp']['TM'] == 0 or r['LC'] > 0, rs)
    law('all TMs of T\' lift (b == 0)', lambda r: r.get('b', 0) == 0, rs)
    law('B >= b (same-type compensation)', lambda r: r.get('B', 0) >= r.get('b', 0), rs)
    law('C >= b (other-type compensation)', lambda r: r.get('C', 0) >= r.get('b', 0), rs)
    law('A >= TM(T\')/2', lambda r: 2 * r['A'] >= r['Tp']['TM'], rs)
    law('TM(T) >= 2 TM(T\')', lambda r: r['T']['TM'] >= 2 * r['Tp']['TM'], rs)

# deletion-contraction: the two merges at the same x
grp = defaultdict(list)
for r in rows:
    grp[(r['V'], r['gid'], r['t0'], r['x'])].append(r)
cnt = Counter(); fails = Counter(); ex = {}
for k, g in grp.items():
    if len(g) != 2 or any(r['loop'] for r in g):
        cnt['skip'] += 1
        continue
    cnt['both'] += 1
    T = g[0]['T']; a, b = g[0]['Tp'], g[1]['Tp']
    tests = {
        'states(T) = states(T1)+states(T2)': T['states'] == a['states'] + b['states'],
        'TM(T) = (A+B)_1 + (A+B)_2': T['TM'] == g[0]['A'] + g[0]['B'] + g[1]['A'] + g[1]['B'],
        'C_1 = (A+B)_2': g[0]['C'] == g[1]['A'] + g[1]['B'],
        'TM(T) <= TM(T1)+TM(T2)': T['TM'] <= a['TM'] + b['TM'],
        'TM(T) >= TM(T1)+TM(T2)': T['TM'] >= a['TM'] + b['TM'],
        'TM(T) = TM(T1)+TM(T2)': T['TM'] == a['TM'] + b['TM'],
        'pairs(T) = pairs(T1)+pairs(T2)': T['pairs'] == a['pairs'] + b['pairs'],
        'D(T) = D(T1)+D(T2)': T['D'] == a['D'] + b['D'],
        'both T1,T2 simple': g[0]['simple'] and g[1]['simple'],
    }
    for name, v in tests.items():
        if not v:
            fails[name] += 1
            ex.setdefault(name, k)
print('groups (both merges at x defined)', dict(cnt))
for name in ['states(T) = states(T1)+states(T2)', 'TM(T) = (A+B)_1 + (A+B)_2', 'C_1 = (A+B)_2', 'TM(T) <= TM(T1)+TM(T2)',
             'TM(T) >= TM(T1)+TM(T2)', 'TM(T) = TM(T1)+TM(T2)', 'pairs(T) = pairs(T1)+pairs(T2)', 'D(T) = D(T1)+D(T2)', 'both T1,T2 simple']:
    print(f'  {name:40s} fails {fails[name]:7d}/{cnt["both"]}', ex.get(name, ''))
