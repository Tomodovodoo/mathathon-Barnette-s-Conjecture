"""Stage 2b: the tables of the report, as Markdown, from the tables in data/.

  python src/report.py        writes data/tables.md
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'


def md(df, fmt=None):
    fmt = fmt or {}
    head = '| ' + ' | '.join(map(str, df.columns)) + ' |'
    sep = '| ' + ' | '.join('---:' if i else '---' for i in range(len(df.columns))) + ' |'
    lines = [head, sep]
    for _, row in df.iterrows():
        cells = []
        for c in df.columns:
            v = row[c]
            if isinstance(v, str):
                cells.append(v)
            elif v is None or (isinstance(v, float) and not np.isfinite(v)):
                cells.append('')
            elif c in fmt:
                cells.append(fmt[c].format(v))
            elif float(v) == int(v):
                cells.append(f'{int(v):,}')
            else:
                cells.append(f'{v:.3g}')
        lines.append('| ' + ' | '.join(cells) + ' |')
    return '\n'.join(lines)


def get(ex, metric, col, group='all', value='all'):
    s = ex[(ex['metric'] == metric) & (ex['group'] == group) & (ex['value'].astype(str) == value)]
    return s.set_index('N')[col]


def main():
    ex = pd.read_csv(DATA / 'exhaustive_summary.csv')
    cnt = pd.read_csv(DATA / 'exhaustive_counts.csv')
    ls = pd.read_csv(DATA / 'large_summary.csv')
    lg = pd.read_csv(DATA / 'large_graphs.csv.gz')
    li = pd.read_csv(DATA / 'large_instances.csv.gz').merge(
        lg[['gid', 'source', 'params', 'N', 'type', 'aut', 'nsep', 'maxdeg']], on='gid')
    out = []

    out.append('## exhaustive: graphs\n')
    t = cnt[['N', 'V', 'graphs', 'graphs_without_separating_triangle', 'graphs_only_4_6_faces',
             'graphs_trivial_group', 'instances', 'instances_with_pair', 'edge_orbits',
             'hamiltonian_cycles_min', 'hamiltonian_cycles_median', 'hamiltonian_cycles_max']].copy()
    t.columns = ['N', 'V(T)', 'graphs', 'no 3-edge cut', 'only 4- and 6-faces', 'trivial group', 'instances',
                 'with a pair', 'orbits of (e, t0)', 'HC min', 'HC median', 'HC max']
    out.append(md(t))

    out.append('\n## exhaustive: group types\n')
    types = {}
    for _, row in cnt.iterrows():
        for item in str(row['types']).split():
            k, v = item.split(':')
            types.setdefault(k, {})[row['N']] = int(v)
    tt = pd.DataFrame(types).T.fillna(0).astype(int)
    tt['all'] = tt.sum(axis=1)
    tt = tt.sort_values('all', ascending=False)
    tt.insert(0, 'group', tt.index)
    tt = tt[['group'] + sorted(c for c in tt.columns if c not in ('group', 'all') and c >= 28) + ['all']]
    tt.columns = ['group'] + [f'N={c}' if c != 'all' else 'all N' for c in tt.columns[1:]]
    out.append(md(tt))

    out.append('\n## exhaustive: states, good states, proportion (instances with a pair)\n')
    N = get(ex, 'ratio', 'count').index
    t = pd.DataFrame({'N': N, 'n': N // 2 - 1, 'with a pair': get(ex, 'ratio', 'count').values,
                      'share with a pair': get(ex, 'has_pair', 'mean').reindex(N).values,
                      'states: median': get(ex, 'states', 'median').values,
                      'states: max': get(ex, 'states', 'max').values,
                      'good: min': get(ex, 'good', 'min').values, 'good: median': get(ex, 'good', 'median').values,
                      'good: max': get(ex, 'good', 'max').values,
                      'ratio: min': get(ex, 'ratio', 'min').values, 'ratio: 5%': get(ex, 'ratio', 'q05').values,
                      'ratio: median': get(ex, 'ratio', 'median').values,
                      'ratio: mean': get(ex, 'ratio', 'mean').values,
                      'ratio: 95%': get(ex, 'ratio', 'q95').values, 'ratio: max': get(ex, 'ratio', 'max').values})
    out.append(md(t, {c: '{:.4f}' for c in t.columns if c.startswith('ratio')} | {'share with a pair': '{:.3f}'}))

    out.append('\n## exhaustive: search (partial choices kept / n, all instances)\n')
    N = get(ex, 'nodes_per_n', 'count').index
    t = pd.DataFrame({'N': N, 'instances': get(ex, 'nodes_per_n', 'count').values})
    for col, name in (('nodes_per_n', 'stored'), ('nodes_bfs_per_n', 'breadth-first'), ('nodes_rand_per_n', 'random')):
        direct = col.replace('nodes', 'direct').replace('_per_n', '')
        t[f'{name}: no backtracking'] = get(ex, direct, 'mean').reindex(N).values
        for q, qn in (('mean', 'mean'), ('q99', '99%'), ('max', 'max')):
            t[f'{name}: {qn}'] = get(ex, col, q).reindex(N).values
    t['bound (n+1)M/n: median'] = get(ex, 'bound_per_n', 'median').reindex(N).values
    out.append(md(t, {c: '{:.2f}' for c in t.columns if ':' in c}
                  | {c: '{:.3f}' for c in t.columns if 'backtracking' in c}))

    out.append('\n## exhaustive: exchange walk (moves, all instances; without a pair the walk runs in the pieces)\n')
    tails = pd.read_csv(DATA / 'exhaustive_tails.csv')
    N = get(ex, 'moves', 'count').index
    t = pd.DataFrame({'N': N, 'instances': get(ex, 'moves', 'count').values})
    for col, name in (('moves', 'stored'), ('moves_mirror', 'mirror'), ('moves_rand', 'random labelling')):
        zero = []
        for n_ in N:
            q = tails[(tails['V'] == n_ // 2 + 2) & (tails['quantity'] == col) & (tails['value'] >= 0)]
            zero.append(q.loc[q['value'] == 0, 'count'].sum() / q['count'].sum() if q['count'].sum() else np.nan)
        t[f'{name}: share with 0 moves'] = zero
        for q, qn in (('mean', 'mean'), ('q99', '99%'), ('max', 'max')):
            t[f'{name}: {qn}'] = get(ex, col, q).reindex(N).values
    out.append(md(t, {c: '{:.3f}' for c in t.columns if 'share' in c or 'mean' in c}))

    out.append('\n## exhaustive: good states against Hamiltonian cycles and against 2^m (instances with a pair)\n')
    N = get(ex, 'g_over_hmin', 'count').index
    t = pd.DataFrame({'N': N})
    for q, qn in (('min', 'min'), ('q05', '5%'), ('median', 'median'), ('mean', 'mean'), ('max', 'max')):
        t[f'g/h: {qn}'] = get(ex, 'g_over_hmin', q).values
    for q, qn in (('min', 'min'), ('mean', 'mean'), ('q99', '99%'), ('max', 'max')):
        t[f'g/2^m: {qn}'] = get(ex, 'g_over_2m', q).reindex(N).values
    for q, qn in (('median', 'median'), ('max', 'max')):
        t[f'2-factors: {qn}'] = get(ex, 'two_factors', q).reindex(N).values
        t[f'pairs: {qn}'] = get(ex, 'pairs', q).reindex(N).values
    out.append(md(t, {c: '{:.3f}' for c in t.columns if c.startswith('g/h')} | {'g/2^m: mean': '{:.3f}'}))

    # the largest size at which the search was also run in breadth-first order
    Nmax = int(get(ex, 'nodes_bfs_per_n', 'count').index.max())
    out.append(f'\n## exhaustive: classes at N = {Nmax}\n')
    rows = []
    for group, title in (('aut_class', 'group order'), ('sym_class', 'group type'),
                         ('face_class', 'largest face'), ('sep_class', 'separating triangles'),
                         ('roots', 'faces at t0')):
        vals = ex[(ex['group'] == group) & (ex['N'] == Nmax)]['value'].astype(str).unique()
        for v in vals:
            def g(metric, col):
                s = get(ex, metric, col, group, v)
                return s.get(Nmax, np.nan)
            rows.append({'class': title, 'value': v, 'instances': g('has_pair', 'count'),
                         'share with a pair': g('has_pair', 'mean'), 'ratio: median': g('ratio', 'median'),
                         'ratio: mean': g('ratio', 'mean'), 'ratio: min': g('ratio', 'min'),
                         'states: median': g('states', 'median'), 'good: median': g('good', 'median'),
                         'search/n: mean': g('nodes_per_n', 'mean'), 'search/n: max': g('nodes_per_n', 'max'),
                         'bfs/n: mean': g('nodes_bfs_per_n', 'mean'), 'bfs/n: max': g('nodes_bfs_per_n', 'max'),
                         'walk: mean': g('moves', 'mean'), 'walk: max': g('moves', 'max')})
    t = pd.DataFrame(rows)
    out.append(md(t, {c: '{:.3f}' for c in t.columns if 'ratio' in c or 'share' in c or 'mean' in c}
                  | {'search/n: max': '{:.1f}', 'bfs/n: max': '{:.1f}'}))

    rows = []
    for source in ('random3', 'random4'):
        d = li[li['source'] == source]
        for Nn, part in d.groupby('N'):
            p = part[part['has_pair'] == 1]
            exact = p[p['good'] >= 0]
            allexact = len(exact) == len(p)
            ratio = exact['good'] / 10.0 ** exact['log10_states']
            row = {'ensemble': source, 'N': Nn, 'graphs': part['gid'].nunique(), 'instances': len(part),
                   'share with a pair': len(p) / len(part),
                   'sep. triangles: mean': part.drop_duplicates('gid')['nsep'].mean(),
                   'log10 states: median': p['log10_states'].median(),
                   'good counted': len(exact) / max(len(p), 1),
                   'ratio: median': ratio.median() if allexact else np.nan,
                   'ratio: min': ratio.min() if allexact else np.nan,
                   'ratio: max': ratio.max() if allexact else np.nan}
            for col, st, name in (('nodes', 'st_search', 'stored'), ('nodes_bfs', 'st_bfs', 'bfs'),
                                  ('nodes_rand', 'st_rand', 'random')):
                x = np.where(part[st] == 0, part[col] / part['n'], np.inf)
                row[f'search {name}: median/n'] = np.median(x)
                row[f'search {name}: censored'] = float((part[st] == 1).mean())
            # the three runs of the walk (stored, mirror image, random labelling), all instances;
            # a censored run counts as larger than every finished one
            w = pd.concat([part['moves'], part['moves_mirror'], part['moves_rand']]).astype(float)
            ws = pd.concat([part['st_walk'], part['st_walk_mirror'], part['st_walk_rand']])
            w[ws == 1] = np.inf
            row['walk: median'] = w.median()
            row['walk: 90%'] = w.quantile(0.9, interpolation='higher')
            row['walk: 99%'] = w.quantile(0.99, interpolation='higher')
            row['walk: max finished'] = w[ws == 0].max()
            row['walk: censored'] = float((ws == 1).mean())
            row['walk time: median (ms)'] = 1e3 * part['t_walk'].median()
            row['cuts: mean'] = part['cuts'].mean()
            row['largest piece n: median'] = part['max_piece'].median()
            rows.append(row)
    t = pd.DataFrame(rows)
    fmt = ({c: '{:.3f}' for c in t.columns if 'share' in c or 'censored' in c or 'counted' in c}
           | {'ratio: median': '{:.2e}', 'ratio: min': '{:.2e}', 'ratio: max': '{:.2e}',
              'log10 states: median': '{:.2f}', 'sep. triangles: mean': '{:.2f}',
              'cuts: mean': '{:.2f}', 'walk time: median (ms)': '{:.3f}'})
    first = ['ensemble', 'N', 'graphs', 'instances', 'share with a pair', 'sep. triangles: mean', 'cuts: mean',
             'largest piece n: median', 'log10 states: median', 'good counted', 'ratio: median', 'ratio: min',
             'ratio: max']
    out.append('\n## random ensembles: graphs, states, good states\n')
    out.append(md(t[first], fmt))
    out.append('\n## random ensembles: search and walk\n')
    out.append(md(t[['ensemble', 'N', 'instances'] + [c for c in t.columns if c not in first]], fmt))

    out.append('\n## constructed families\n')
    rows = []
    for source, part in li.groupby('source'):
        if source.startswith('random'):
            continue
        p = part[part['has_pair'] == 1]
        w = pd.concat([part['moves'], part['moves_mirror'], part['moves_rand']]).astype(float)
        ws = pd.concat([part['st_walk'], part['st_walk_mirror'], part['st_walk_rand']])
        ws = ws[w >= 0]
        w = w[w >= 0]
        w[ws == 1] = np.inf
        sr = pd.concat([part['st_search'], part['st_bfs'], part['st_rand']])
        rows.append({'family': source, 'graphs': part['gid'].nunique(), 'instances': len(part),
                     'N from': part['N'].min(), 'N to': part['N'].max(),
                     'share with a pair': len(p) / len(part),
                     'good counted': float((p['good'] >= 0).mean()) if len(p) else np.nan,
                     'search censored': float((sr == 1).mean()),
                     'largest N with every search finished': part.groupby('N').filter(
                         lambda q: ((q[['st_search', 'st_bfs', 'st_rand']] == 0).all().all()))['N'].max(),
                     'walk: median': w.median(), 'walk: max finished': w[ws == 0].max(),
                     'walk censored': float((ws == 1).mean()),
                     'largest N with every walk finished': part.groupby('N').filter(
                         lambda q: ((q[['st_walk', 'st_walk_mirror', 'st_walk_rand']] <= 0).all().all()))['N'].max()})
    t = pd.DataFrame(rows)
    out.append(md(t, {c: '{:.3f}' for c in t.columns if 'share' in c or 'censored' in c or 'counted' in c}))

    out.append('\n## fits (least squares on the logarithm; intervals are 95% for the growth factor or exponent)\n')
    rows = []
    for name, f in json.loads((DATA / 'fits.json').read_text()).items():
        base = {'quantity': name, 'n from': f['n_from'], 'n to': f['n_to'], 'points': f['points']}
        if 'r' in f:
            rows.append({**base, 'model': 'c r^n', 'c': f['c'], 'r or k': f['r'], 'low': f['r_low'],
                         'high': f['r_high'], 'rms residual of log': np.nan})
        elif 'growth_per_n' in f:
            r = f['growth_per_n']
            rows.append({**base, 'model': 'c r^n', 'c': 10.0 ** f['a'], 'r or k': r,
                         'low': 10.0 ** (f['b'] - 1.96 * f['b_se']), 'high': 10.0 ** (f['b'] + 1.96 * f['b_se']),
                         'rms residual of log': np.nan})
        else:
            e, p = f['exponential'], f['power law']
            rows.append({**base, 'model': 'c r^n', 'c': e['c'], 'r or k': e['r'], 'low': e['r_low'],
                         'high': e['r_high'], 'rms residual of log': e['rms residual of log']})
            rows.append({**base, 'model': 'c n^k', 'c': p['c'], 'r or k': p['k'], 'low': p['k_low'],
                         'high': p['k_high'], 'rms residual of log': p['rms residual of log']})
    out.append(md(pd.DataFrame(rows), {'c': '{:.3g}', 'r or k': '{:.4f}', 'low': '{:.4f}', 'high': '{:.4f}',
                                       'rms residual of log': '{:.2f}'}))
    for name in ('open_problems', 'totals'):
        out.append(f'\n## {name}\n\n```json\n' + (DATA / f'{name}.json').read_text() + '```')
    if (DATA / 'mixing.csv').exists():
        mix = pd.read_csv(DATA / 'mixing.csv')
        out.append('\n## mixing: sizes at which the exact means are known\n')
        out.append(md(mix[mix['exact_mean'].notna() & (mix['se'] > 0)],
                      {'mean': '{:.3f}', 'se': '{:.3f}', 'lag1_autocorrelation': '{:.3f}', 'exact_mean': '{:.3f}'}))
        ac = mix['lag1_autocorrelation'].dropna()
        out.append(f'\nlag-one autocorrelations over all sizes and statistics: {len(ac)} values, '
                   f'mean {ac.mean():.3f}, from {ac.min():.3f} to {ac.max():.3f}; '
                   f'{int((ac.abs() > 0.2).sum())} exceed 0.2 in absolute value')
    if (DATA / 'deep.csv').exists():
        d = pd.read_csv(DATA / 'deep.csv')
        d['ensemble'] = np.where(d['gid'] // 10**12 == 2, 'random3', 'random4')
        rows = []
        for (e, n), part in d.groupby(['ensemble', 'n']):
            ok = part[(part['status'] == 0) & (part['good'] > 0)]
            rows.append({'ensemble': e, 'n': n, 'instances': len(part), 'counted': int((part['status'] == 0).sum()),
                         'without good state': int(((part['status'] == 0) & (part['good'] == 0)).sum()),
                         'ratio: min': ok['ratio'].min(), 'ratio: median': ok['ratio'].median(),
                         'ratio: max': ok['ratio'].max(), 'good: median': ok['good'].median(),
                         'good: max': ok['good'].max(), 'seconds: max': part['seconds'].max()})
        out.append('\n## deep counts\n')
        out.append(md(pd.DataFrame(rows), {'ratio: min': '{:.2e}', 'ratio: median': '{:.2e}', 'ratio: max': '{:.2e}'}))
    (DATA / 'tables.md').write_text('\n'.join(out) + '\n', encoding='utf8')


if __name__ == '__main__':
    main()
