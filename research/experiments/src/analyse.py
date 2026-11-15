"""Stage 2: from the raw results to the tables in data/.

  python src/analyse.py

Reads raw/exh/*.npz, raw/large/*.npz and raw/large/deep.npy and writes

  data/exhaustive_summary.csv   quantiles of every measured quantity, by size
                                and by class, for the exhaustive part
  data/exhaustive_counts.csv    graphs, instances and group types by size
  data/exhaustive_tails.csv     distributions for the tail plots
  data/small_instances.csv.gz   all instances with at most 16 vertices of T
  data/large_graphs.csv.gz      the constructed and the random graphs
  data/large_instances.csv.gz   their instances
  data/large_summary.csv        quantiles by source and size
  data/mixing.csv               diagnostics of the Markov chain sampler
  data/deep.csv                 exact counts of good states with a larger budget
  data/extremal.json            the extremal instances of the exhaustive part, each
                                named by its place in the output of plantri
  data/open_problems.json       the checks that bear on research/OPEN-PROBLEMS.md
  data/fits.json                fitted growth rates, with the fitted ranges
  data/totals.json              totals quoted in the report
"""
import glob
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))
import symmetry                                               # noqa: E402

DATA = ROOT / 'data'
QS = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]


def stats(x):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if len(x) == 0:
        return None
    q = np.quantile(x, QS)
    return dict(count=len(x), min=x.min(), q01=q[0], q05=q[1], q25=q[2], median=q[3], q75=q[4],
                q95=q[5], q99=q[6], max=x.max(), mean=x.mean())


def aut_class(a):
    return np.select([a == 1, a == 2, a <= 4, a <= 8], ['1', '2', '3-4', '5-8'], default='>8')


def face_class(d):
    return np.select([d <= 6, d == 8, d == 10, d == 12], ['4,6', '8', '10', '12'], default='>=14')


def sep_class(s):
    return np.select([s == 0, s == 1, s == 2, s == 3], ['0', '1', '2', '3'], default='>=4')


KEEP = ['gid', 't0', 'orbit', 'n', 'has_pair', 'states', 'good', 'log10_states', 'good_status', 'pairs',
        'pairs_status', 'two_factors', 'm', 'cuts', 'pieces', 'nodes', 'nodes_bfs', 'nodes_rand', 'st_search',
        'st_bfs', 'st_rand', 'moves', 'moves_mirror', 'moves_rand', 'st_walk', 'st_walk_mirror',
        'st_walk_rand', 't_search', 't_walk', 'h0', 'h1', 'h2', 'cycles_ok', 'cycles_bad', 'error',
        'rd0', 'rd1', 'rd2']
SMALL = {'states': 'i4', 'good': 'i4', 'pairs': 'i4', 'two_factors': 'i4', 'nodes': 'i4', 'nodes_bfs': 'i4',
         'nodes_rand': 'i4', 'moves': 'i4', 'moves_mirror': 'i4', 'moves_rand': 'i4', 'h0': 'i4', 'h1': 'i4',
         'h2': 'i4', 'log10_states': 'f4', 'm': 'i1', 'n': 'i2', 't0': 'i2', 'orbit': 'i2', 'rd0': 'i2',
         'rd1': 'i2', 'rd2': 'i2', 'cuts': 'i2', 'pieces': 'i2'}


def frame(G, R, compact=False, full=None):
    """Join instances with their graphs and add the derived columns.  With
    compact set, only the columns needed for the summaries are kept, in small
    types (the values of the exhaustive part fit)."""
    g = pd.DataFrame({k: G[k] for k in G.dtype.names})
    if compact:
        r = pd.DataFrame({k: R[k].astype(SMALL[k]) if k in SMALL else R[k] for k in KEEP})
        g = g[['gid', 'V', 'N', 'aut', 'aut_op', 'type', 'maxdeg', 'nsep']]
    else:
        r = pd.DataFrame({k: R[k] for k in R.dtype.names})
    d = r.merge(g, on='gid', how='left')
    pair = d['has_pair'] == 1
    exact = (d['good'] >= 0) & (d['states'] > 0)
    d['ratio'] = np.where(pair & exact, d['good'] / d['states'].clip(lower=1), np.nan)
    known = (d['good'] >= 0) & pair & ~exact & np.isfinite(d['log10_states'])
    d.loc[known, 'ratio'] = d.loc[known, 'good'] / 10.0 ** d.loc[known, 'log10_states'].astype(float)
    hmin = d[['h0', 'h1', 'h2']].min(axis=1)
    d['g_over_hmin'] = np.where(pair & (hmin > 0), d['good'] / hmin.clip(lower=1), np.nan)
    d['hmin'] = hmin
    d['g_over_2m'] = np.where(pair & (d['m'] >= 0), d['good'] / 2.0 ** d['m'].clip(lower=0), np.nan)
    for a in ('nodes', 'nodes_bfs', 'nodes_rand'):
        st = {'nodes': 'st_search', 'nodes_bfs': 'st_bfs', 'nodes_rand': 'st_rand'}[a]
        d[a + '_per_n'] = np.where(d[st] == 0, d[a] / d['n'], np.nan)
        # no backtracking: exactly n partial choices are kept
        d[a.replace('nodes', 'direct')] = np.where(d[st] >= 0, (d[st] == 0) & (d[a] == d['n']), np.nan)
    d['bound_per_n'] = np.where(pair & (d['states'] > 0), (d['n'] + 1.0) * d['states'] / d['n'], np.nan)
    d['aut_class'] = pd.Categorical(aut_class(d['aut'].to_numpy()))
    d['face_class'] = pd.Categorical(face_class(d['maxdeg'].to_numpy()))
    d['sep_class'] = pd.Categorical(sep_class(d['nsep'].to_numpy()))
    fam = {t: (symmetry.family_of_type(t) if t and t != '?' else 'unknown') for t in set(d['type'])}
    d['sym_class'] = pd.Categorical(d['type'].map(fam))
    d['roots'] = pd.Categorical(d['rd0'].astype(str) + '-' + d['rd1'].astype(str) + '-' + d['rd2'].astype(str))
    if compact:
        for c in ('ratio', 'g_over_hmin', 'g_over_2m', 'nodes_per_n', 'nodes_bfs_per_n', 'nodes_rand_per_n',
                  'bound_per_n', 'direct', 'direct_bfs', 'direct_rand'):
            d[c] = d[c].astype('f4')
        d = d.drop(columns=['rd0', 'rd1', 'rd2', 'h0', 'h1', 'h2', 'type'])
    return d


METRICS = ['ratio', 'log10_states', 'states', 'good', 'nodes_per_n', 'nodes_bfs_per_n', 'nodes_rand_per_n',
           'bound_per_n', 'moves', 'moves_mirror', 'moves_rand', 'g_over_hmin', 'g_over_2m', 'm',
           'two_factors', 'pairs', 't_search', 't_walk', 'cuts', 'has_pair', 'direct', 'direct_bfs',
           'direct_rand']


def summarise(d, keys, rows):
    for metric in METRICS:
        x = d[metric]
        if metric in ('states', 'good', 'log10_states', 'two_factors', 'pairs', 'm'):
            x = x.where(d['has_pair'] == 1)
        if metric.startswith('moves'):
            st = {'moves': 'st_walk', 'moves_mirror': 'st_walk_mirror', 'moves_rand': 'st_walk_rand'}[metric]
            x = x.where(d[st] == 0)
        s = stats(x.to_numpy())
        if s:
            rows.append({**keys, 'metric': metric, **s})


def censoring(d, keys, rows):
    """Fractions of censored runs, per method."""
    for name, st in (('search', 'st_search'), ('search_bfs', 'st_bfs'), ('search_rand', 'st_rand'),
                     ('walk', 'st_walk'), ('walk_mirror', 'st_walk_mirror'), ('walk_rand', 'st_walk_rand'),
                     ('good_count', 'good_status')):
        run = d[st] >= 0
        if run.sum():
            rows.append({**keys, 'metric': 'censored_' + name, 'count': int(run.sum()),
                         'mean': float((d.loc[run, st] == 1).mean())})


def exhaustive():
    files = defaultdict(list)
    for f in glob.glob(str(ROOT / 'raw' / 'exh' / '*.npz')):
        files[int(re.match(r'V(\d+)_', Path(f).name).group(1))].append(f)
    rows, counts, tails, small, extremal = [], [], [], [], {}
    op = {'instances': 0, 'instances_with_pair': 0, 'faces': 0, 'faces_with_pair': 0, 'graphs_with_states_depending_on_t0': 0,
          'good_odd': 0, 'good_below_2m': 0, 'good_below_2_to_m': 0,
          'equality_g_2m_power': 0, 'single_two_factor': 0, 'equality_and_single_two_factor': 0,
          'pair_without_good_state': 0, 'good_state_without_pair': 0, 'good_above_cycles_avoiding_e': 0,
          'sizes': []}
    totals = {'graphs': 0, 'instances': 0, 'cycles_verified': 0, 'cycles_failed': 0, 'errors': 0,
              'dart_orbits': 0, 'censored': 0}
    from run_exhaustive import PARTS
    for V in sorted(files):
        files[V] = [f for f in files[V] if '.part.' not in f]
        if len(files[V]) != PARTS.get(V, 1):
            print(f'V = {V}: {len(files[V])} of {PARTS.get(V, 1)} parts, skipped', flush=True)
            continue
        G = np.concatenate([np.load(f)['graphs'] for f in sorted(files[V])])
        parts = []
        for f in sorted(files[V]):
            z = np.load(f)
            parts.append(frame(z['graphs'], z['inst'], compact=V > 16))
        d = pd.concat(parts, ignore_index=True)
        del parts
        for c in ('aut_class', 'face_class', 'sep_class', 'sym_class', 'roots'):
            d[c] = d[c].astype(str)
        info = pd.DataFrame({k: G[k] for k in ('gid', 'params', 'type', 'degs', 'nsep')}).set_index('gid')
        pair = d['has_pair'] == 1
        totals['graphs'] += len(G)
        totals['instances'] += len(d)
        totals['cycles_verified'] += int(d['cycles_ok'].sum())
        totals['cycles_failed'] += int(d['cycles_bad'].sum())
        totals['errors'] += int((d['error'] != 0).sum())
        totals['dart_orbits'] += int(G['dart_orbits'].sum())
        totals['censored'] += int(((d[['st_search', 'st_bfs', 'st_rand', 'st_walk', 'st_walk_mirror',
                                       'st_walk_rand', 'good_status', 'pairs_status']] == 1).any(axis=1)).sum())
        types = Counter(G['type'].tolist())
        counts.append({'V': V, 'N': 2 * V - 4, 'n': V - 3, 'graphs': len(G), 'instances': len(d),
                       'edge_orbits': int(G['dart_orbits'].sum()),
                       'graphs_without_separating_triangle': int((G['nsep'] == 0).sum()),
                       'graphs_only_4_6_faces': int((G['maxdeg'] <= 6).sum()),
                       'graphs_trivial_group': int((G['aut'] == 1).sum()),
                       'graphs_chiral': int((G['aut'] == G['aut_op']).sum()),
                       'instances_with_pair': int(pair.sum()),
                       'hamiltonian_cycles_min': int(G['hc_total'].min()),
                       'hamiltonian_cycles_median': float(np.median(G['hc_total'])),
                       'hamiltonian_cycles_max': int(G['hc_total'].max()),
                       'types': ' '.join(f'{t}:{c}' for t, c in sorted(types.items()))})
        base = {'V': V, 'N': 2 * V - 4, 'n': V - 3}
        summarise(d, {**base, 'group': 'all', 'value': 'all'}, rows)
        censoring(d, {**base, 'group': 'all', 'value': 'all'}, rows)
        for group in ('aut_class', 'face_class', 'sep_class', 'sym_class'):
            for value, part in d.groupby(group):
                summarise(part, {**base, 'group': group, 'value': value}, rows)
        top = d['roots'].value_counts().index[:12]
        for value in top:
            summarise(d[d['roots'] == value], {**base, 'group': 'roots', 'value': value}, rows)

        # the open problems
        p = d[pair]
        op['sizes'].append(V)
        op['instances'] += len(d)
        op['instances_with_pair'] += len(p)
        # every face of T as t0, without reduction by symmetry
        op['faces'] += int(d['orbit'].sum())
        op['faces_with_pair'] += int(p['orbit'].sum())
        op['graphs_with_states_depending_on_t0'] += int((d.groupby('gid')['states'].nunique() > 1).sum())
        op['good_odd'] += int((p['good'] % 2 == 1).sum())
        op['good_below_2m'] += int((p['good'] < 2 * p['m']).sum())
        op['good_below_2_to_m'] += int((p['good'] < 2 ** p['m']).sum())
        eq = p['good'] == 2 ** p['m']
        one = p['two_factors'] == 1
        op['equality_g_2m_power'] += int(eq.sum())
        op['single_two_factor'] += int(one.sum())
        op['equality_and_single_two_factor'] += int((eq & one).sum())
        op['pair_without_good_state'] += int((p['good'] == 0).sum())
        op['good_state_without_pair'] += int((d.loc[~pair, 'good'] > 0).sum())
        op['good_above_cycles_avoiding_e'] += int((d['good'] > d['hmin']).sum())

        # tails: distributions of moves and of nodes per n
        for col in ('moves', 'moves_mirror', 'moves_rand'):
            vc = d[col].value_counts().sort_index()
            tails += [{'V': V, 'quantity': col, 'value': float(k), 'count': int(c)} for k, c in vc.items()]
        edges = np.round(np.logspace(0, 2.2, 45), 4)
        for col in ('nodes_per_n', 'nodes_bfs_per_n', 'nodes_rand_per_n'):
            h, _ = np.histogram(d[col].to_numpy(), bins=edges)
            tails += [{'V': V, 'quantity': col, 'value': float(e), 'count': int(c)}
                      for e, c in zip(edges[:-1], h) if c]
        ratio_edges = np.round(np.logspace(-2.5, 0, 51), 5)
        h, _ = np.histogram(p['ratio'].to_numpy(), bins=ratio_edges)
        tails += [{'V': V, 'quantity': 'ratio', 'value': float(e), 'count': int(c)}
                  for e, c in zip(ratio_edges[:-1], h) if c]
        gh_edges = np.round(np.linspace(0, 1, 41), 4)
        h, _ = np.histogram(p['g_over_hmin'].to_numpy().clip(max=0.9999), bins=gh_edges)
        tails += [{'V': V, 'quantity': 'g_over_hmin', 'value': float(e), 'count': int(c)}
                  for e, c in zip(gh_edges[:-1], h) if c]
        vc = p['g_over_2m'].value_counts().sort_index()
        tails += [{'V': V, 'quantity': 'g_over_2m', 'value': float(k), 'count': int(c)} for k, c in vc.items()]

        # extremal instances
        def note(name, j):
            row = d.loc[j]
            gr = info.loc[row['gid']]
            extremal[f'{name}_V{V}'] = {
                'V': V, 'N': 2 * V - 4, 'gid': int(row['gid']), 't0': int(row['t0']), 'graph': gr['params'],
                'group': gr['type'], 'faces_of_G': gr['degs'], 'separating_triangles': int(gr['nsep']),
                'roots': row['roots'], 'states': int(row['states']), 'good': int(row['good']),
                'ratio': round(int(row['good']) / int(row['states']), 6) if row['has_pair'] == 1 else None,
                'has_pair': bool(row['has_pair'] == 1), 'm': int(row['m']),
                'two_factors': int(row['two_factors']), 'nodes': int(row['nodes']),
                'nodes_bfs': int(row['nodes_bfs']), 'nodes_rand': int(row['nodes_rand']),
                'moves': int(row['moves']), 'moves_mirror': int(row['moves_mirror'])}
        if len(p):
            note('min_ratio', p['ratio'].idxmin())
            note('max_ratio', p['ratio'].idxmax())
            note('max_states', p['states'].idxmax())
            note('max_good', p['good'].idxmax())
            note('max_nodes', d['nodes'].idxmax())
            note('max_nodes_bfs', d['nodes_bfs'].idxmax())
            note('max_moves', d['moves'].idxmax())
            note('min_g_over_hmin', p['g_over_hmin'].idxmin())
            note('max_g_over_2m', p['g_over_2m'].idxmax())
        if V <= 16:
            small.append(d)
        print('exhaustive', V, len(G), len(d), flush=True)
    pd.DataFrame(rows).to_csv(DATA / 'exhaustive_summary.csv', index=False, float_format='%.6g')
    pd.DataFrame(counts).to_csv(DATA / 'exhaustive_counts.csv', index=False)
    pd.DataFrame(tails).to_csv(DATA / 'exhaustive_tails.csv', index=False, float_format='%.6g')
    keep = ['gid', 'V', 'N', 'n', 't0', 'orbit', 'roots', 'params', 'type', 'aut', 'degs', 'nsep', 'has_pair',
            'states', 'good', 'pairs', 'two_factors', 'm', 'cuts', 'pieces', 'nodes', 'nodes_bfs',
            'nodes_rand', 'moves', 'moves_mirror', 'moves_rand', 'h0', 'h1', 'h2', 'hc_total', 'cycles_ok']
    pd.concat(small)[keep].to_csv(DATA / 'small_instances.csv.gz', index=False)
    return extremal, op, totals


def large():
    Gs, Rs = [], []
    for f in sorted(glob.glob(str(ROOT / 'raw' / 'large' / '*.npz'))):
        if '.part.' in f:
            continue
        z = np.load(f)
        Gs.append(z['graphs'])
        Rs.append(z['inst'])
    G, R = np.concatenate(Gs), np.concatenate(Rs)
    d = frame(G, R)
    for c in ('aut_class', 'face_class', 'sep_class', 'sym_class', 'roots'):
        d[c] = d[c].astype(str)
    g = pd.DataFrame({k: G[k] for k in G.dtype.names})
    g.drop(columns=['hc_status']).to_csv(DATA / 'large_graphs.csv.gz', index=False)
    keep = ['gid', 't0', 'orbit', 'roots', 'n', 'log10_states', 'states', 'good', 'good_status', 'good_nodes',
            'has_pair', 'pairs', 'two_factors', 'm', 'cuts', 'pieces', 'max_piece', 'nodes', 'st_search',
            't_search', 'nodes_bfs', 'st_bfs', 'nodes_rand', 'st_rand', 'moves', 'rounds', 'st_walk', 't_walk',
            'moves_mirror', 'st_walk_mirror', 'moves_rand', 'st_walk_rand', 'h0', 'h1', 'h2', 'uni_good',
            'uni_n', 'uni_excess', 'cycles_ok', 'cycles_bad', 'error']
    d[keep].to_csv(DATA / 'large_instances.csv.gz', index=False, float_format='%.6g')

    rows = []
    for (source, n), part in d.groupby(['source', 'n']):
        if source.startswith('random'):
            keys = {'source': source, 'n': n, 'N': 2 * n + 2, 'graphs': part['gid'].nunique()}
            summarise(part, keys, rows)
            censoring(part, keys, rows)
            p = part[part['has_pair'] == 1]
            for metric, x in (('uni_excess', p['uni_excess']), ('nsep', part['nsep']),
                              ('max_piece_n', part['max_piece_n']), ('maxdeg', part['maxdeg']),
                              ('good_exact', (p['good_status'] == 0).astype(float)),
                              ('uni_fraction', (p['uni_good'] / p['uni_n'].clip(lower=1)).where(p['uni_n'] > 0))):
                s = stats(x.to_numpy(dtype=float))
                if s:
                    rows.append({**keys, 'metric': metric, **s})
    pd.DataFrame(rows).to_csv(DATA / 'large_summary.csv', index=False, float_format='%.6g')
    totals = {'graphs': len(G), 'instances': len(d), 'cycles_verified': int(d['cycles_ok'].sum()),
              'cycles_failed': int(d['cycles_bad'].sum()), 'errors': int((d['error'] != 0).sum()),
              'by_source': {s: {'graphs': int(p['gid'].nunique()), 'instances': len(p),
                                'N_min': int(p['N'].min()), 'N_max': int(p['N'].max())}
                            for s, p in d.groupby('source')}}
    return d, totals


def mixing():
    """Diagnostics of the Markov chain: for each ensemble and size, the mean of
    three statistics of the sampled triangulations, the autocorrelation at
    lag one between consecutive samples of a chain, and, where all
    triangulations are known, the exact mean under the weights 1/|Aut|."""
    g = pd.read_csv(DATA / 'large_graphs.csv.gz')
    g = g[g['source'].str.startswith('random')].copy()
    g['chain'] = g['params'].str.extract(r'chain=(\d+)')[0].astype(int)
    g['sample'] = g['params'].str.extract(r'sample=(\d+)')[0].astype(int)
    g['no_sep'] = (g['nsep'] == 0).astype(float)
    exact = {}
    for V in (20, 22):
        files = sorted(glob.glob(str(ROOT / 'raw' / 'exh' / f'V{V}_*.npz')))
        if files:
            G = pd.DataFrame(np.concatenate([np.load(f)['graphs'] for f in files]))
            G['no_sep'] = (G['nsep'] == 0).astype(float)
            w = 1 / G['aut']
            for source, sel in (('random3', G['aut'] > 0), ('random4', G['nsep'] == 0)):
                exact[source, V] = {c: float((G.loc[sel, c] * w[sel]).sum() / w[sel].sum())
                                    for c in ('nsep', 'n4', 'maxdeg', 'no_sep')}
    rows = []
    for (source, V), part in g.groupby(['source', 'V']):
        for col in ('nsep', 'n4', 'maxdeg', 'no_sep'):
            x, y = [], []
            for _, chain in part.sort_values('sample').groupby('chain'):
                v = chain[col].to_numpy(dtype=float)
                x += v[:-1].tolist()
                y += v[1:].tolist()
            ac = float(np.corrcoef(x, y)[0, 1]) if len(x) > 2 and np.std(x) > 0 and np.std(y) > 0 else np.nan
            rows.append({'source': source, 'V': V, 'graphs': len(part), 'statistic': col,
                         'mean': part[col].mean(), 'se': part[col].std() / np.sqrt(len(part)),
                         'lag1_autocorrelation': ac, 'exact_mean': exact.get((source, V), {}).get(col, np.nan)})
    pd.DataFrame(rows).to_csv(DATA / 'mixing.csv', index=False, float_format='%.5g')


def fit_line(x, y):
    """Least squares y = a + b x; returns (a, b, standard error of b)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    A = np.vstack([np.ones_like(x), x]).T
    coef, res, *_ = np.linalg.lstsq(A, y, rcond=None)
    dof = max(len(x) - 2, 1)
    s2 = float(np.sum((y - A @ coef) ** 2)) / dof
    se = float(np.sqrt(s2 / np.sum((x - x.mean()) ** 2)))
    return float(coef[0]), float(coef[1]), se


def fits(dl):
    out = {}
    ex = pd.read_csv(DATA / 'exhaustive_summary.csv')
    ex = ex[(ex['group'] == 'all')]

    def series(metric, col):
        s = ex[ex['metric'] == metric].set_index('n')[col]
        return s

    # exhaustive: mean and median proportion against n, both parities
    for label, sel in (('all n', lambda n: n >= 9), ('n odd', lambda n: (n >= 9) & (n % 2 == 1)),
                       ('n even', lambda n: (n >= 9) & (n % 2 == 0))):
        for col in ('mean', 'median', 'min'):
            s = series('ratio', col)
            s = s[sel(s.index.to_numpy())]
            a, b, se = fit_line(s.index, np.log(s.to_numpy()))
            out[f'exhaustive ratio {col}, {label}'] = {
                'model': 'ratio = c * r^n', 'r': np.exp(b), 'r_low': np.exp(b - 2 * se), 'r_high': np.exp(b + 2 * se),
                'c': np.exp(a), 'n_from': int(s.index.min()), 'n_to': int(s.index.max()), 'points': len(s)}
    for metric, col in (('states', 'median'), ('states', 'max'), ('states', 'mean'), ('good', 'mean'),
                        ('nodes_per_n', 'mean'), ('nodes_bfs_per_n', 'mean'), ('nodes_rand_per_n', 'mean'),
                        ('nodes_per_n', 'max'), ('nodes_bfs_per_n', 'max'), ('nodes_rand_per_n', 'max'),
                        ('nodes_per_n', 'q99'), ('nodes_bfs_per_n', 'q99'), ('nodes_rand_per_n', 'q99')):
        s = series(metric, col)
        s = s[s.index >= 11]
        a, b, se = fit_line(s.index, np.log(s.to_numpy()))
        out[f'exhaustive {metric} {col}'] = {
            'model': 'y = c * r^n', 'r': np.exp(b), 'r_low': np.exp(b - 2 * se), 'r_high': np.exp(b + 2 * se),
            'c': np.exp(a), 'n_from': int(s.index.min()), 'n_to': int(s.index.max()), 'points': len(s)}

    # random ensembles
    for source in ('random3', 'random4'):
        p = dl[(dl['source'] == source) & (dl['has_pair'] == 1)]
        by = p.groupby('n')
        # number of states
        m = by['log10_states'].mean()
        a, b, se = fit_line(m.index, m.to_numpy())
        out[f'{source} states'] = {'model': 'log10(states) = a + b n', 'b': b, 'b_se': se, 'a': a,
                                   'growth_per_n': 10 ** b, 'n_from': int(m.index.min()),
                                   'n_to': int(m.index.max()), 'points': len(m)}
        # proportion: sizes at which every count is exact
        exact = by['good_status'].apply(lambda s: (s == 0).mean())
        ok = exact[exact >= 0.999].index
        q = p[p['n'].isin(ok) & (p['good'] > 0)]
        for name, agg in (('median', q.groupby('n')['ratio'].median()),
                          ('mean of log', np.exp(q.groupby('n')['ratio'].apply(lambda s: np.log(s).mean())))):
            agg = agg[agg.index >= 20]
            a, b, se = fit_line(agg.index, np.log(agg.to_numpy()))
            out[f'{source} ratio {name}'] = {
                'model': 'ratio = c * r^n', 'r': np.exp(b), 'r_low': np.exp(b - 2 * se),
                'r_high': np.exp(b + 2 * se), 'c': np.exp(a), 'n_from': int(agg.index.min()),
                'n_to': int(agg.index.max()), 'points': len(agg)}
        g = np.exp(q.groupby('n')['good'].apply(lambda s: np.log(s).mean()))
        g = g[g.index >= 20]
        a, b, se = fit_line(g.index, np.log(g.to_numpy()))
        out[f'{source} good (geometric mean)'] = {
            'model': 'good = c * r^n', 'r': np.exp(b), 'r_low': np.exp(b - 2 * se), 'r_high': np.exp(b + 2 * se),
            'c': np.exp(a), 'n_from': int(g.index.min()), 'n_to': int(g.index.max()), 'points': len(g)}
        # search: median nodes while fewer than half of the runs are censored
        allp = dl[dl['source'] == source]
        for col, st in (('nodes', 'st_search'), ('nodes_bfs', 'st_bfs'), ('nodes_rand', 'st_rand')):
            med, ns = [], []
            for n, part in allp.groupby('n'):
                x = np.where(part[st] == 0, part[col], np.inf)
                if np.median(x) < np.inf:
                    ns.append(n)
                    med.append(np.median(x) / n)
            ns, med = np.array(ns), np.array(med)
            keepn = ns >= 20
            if keepn.sum() >= 3:
                a, b, se = fit_line(ns[keepn], np.log(med[keepn]))
                out[f'{source} search median {col}/n'] = {
                    'model': 'nodes/n = c * r^n', 'r': np.exp(b), 'r_low': np.exp(b - 2 * se),
                    'r_high': np.exp(b + 2 * se), 'c': np.exp(a), 'n_from': int(ns[keepn].min()),
                    'n_to': int(ns[keepn].max()), 'points': int(keepn.sum())}
        # walk: the three runs per instance pooled (stored, mirror image, random labelling);
        # median and 90% quantile against n, a censored run counting as infinite; both a
        # power law and an exponential are fitted
        ns, med, q90 = [], [], []
        for n, part in allp.groupby('n'):
            x = np.concatenate([np.where(part[st] == 0, part[col], np.inf)
                                for col, st in (('moves', 'st_walk'), ('moves_mirror', 'st_walk_mirror'),
                                                ('moves_rand', 'st_walk_rand'))])
            if n >= 100 and np.quantile(x, 0.9, method='higher') < np.inf:
                ns.append(n)
                med.append(np.median(x))
                q90.append(np.quantile(x, 0.9, method='higher'))
        if len(ns) >= 3:
            for name, y in (('median', med), ('90% quantile', q90)):
                y = np.array(y)
                okp = y > 0
                x = np.array(ns)[okp]
                a, b, se = fit_line(np.log(x), np.log(y[okp]))
                a2, b2, se2 = fit_line(x, np.log(y[okp]))
                r1 = float(np.sqrt(np.mean((np.log(y[okp]) - a - b * np.log(x)) ** 2)))
                r2 = float(np.sqrt(np.mean((np.log(y[okp]) - a2 - b2 * x) ** 2)))
                out[f'{source} walk moves, {name}'] = {
                    'power law': {'model': 'moves = c * n^k', 'k': b, 'k_low': b - 2 * se, 'k_high': b + 2 * se,
                                  'c': np.exp(a), 'rms residual of log': r1},
                    'exponential': {'model': 'moves = c * r^n', 'r': np.exp(b2), 'r_low': np.exp(b2 - 2 * se2),
                                    'r_high': np.exp(b2 + 2 * se2), 'c': np.exp(a2),
                                    'rms residual of log': r2},
                    'n_from': int(x.min()), 'n_to': int(x.max()), 'points': int(okp.sum())}
    return out


def main():
    DATA.mkdir(exist_ok=True)
    extremal, op, totals = exhaustive()
    dl, totals_large = large()
    mixing()
    deep_file = ROOT / 'raw' / 'large' / 'deep.npy'
    if deep_file.exists():
        deep = pd.DataFrame(np.load(deep_file))
        deep['ratio'] = np.where(deep['status'] == 0, deep['good'] / 10.0 ** deep['log10_states'], np.nan)
        deep.to_csv(DATA / 'deep.csv', index=False, float_format='%.6g')

    # the open problems on the non-exhaustive instances with enumerated pairs
    p = dl[(dl['has_pair'] == 1) & (dl['m'] >= 0) & (dl['good'] >= 0)]
    op_large = {'instances_with_pairs_enumerated': len(p), 'n_max': int(p['n'].max()),
                'good_below_2_to_m': int((p['good'] < 2 ** p['m']).sum()),
                'good_odd': int((dl.loc[dl['good'] >= 0, 'good'] % 2 == 1).sum()),
                'instances_with_exact_count': int((dl['good'] >= 0).sum()),
                'equality': int((p['good'] == 2 ** p['m']).sum()),
                'equality_and_single_two_factor': int(((p['good'] == 2 ** p['m']) & (p['two_factors'] == 1)).sum()),
                'single_two_factor': int((p['two_factors'] == 1).sum()),
                'pair_without_good_state': int(((dl['has_pair'] == 1) & (dl['good'] == 0)).sum()),
                'good_state_without_pair': int(((dl['has_pair'] == 0) & (dl['good'] > 0)).sum())}
    # the number of states of a graph, over the faces t0 measured
    spread = dl[np.isfinite(dl['log10_states'])].groupby('gid')['log10_states'].agg(['min', 'max', 'count'])
    spread = spread[spread['count'] > 1]
    op_large['graphs_with_several_t0'] = len(spread)
    op_large['largest_spread_of_log10_states_within_a_graph'] = float((spread['max'] - spread['min']).max())
    (DATA / 'open_problems.json').write_text(json.dumps({'exhaustive': op, 'other': op_large}, indent=1) + '\n')
    (DATA / 'extremal.json').write_text(json.dumps(extremal, indent=1) + '\n')
    (DATA / 'fits.json').write_text(json.dumps(fits(dl), indent=1) + '\n')
    (DATA / 'totals.json').write_text(json.dumps({'exhaustive': totals, 'other': totals_large}, indent=1) + '\n')
    print(json.dumps({'exhaustive': totals, 'other': {k: v for k, v in totals_large.items() if k != 'by_source'}}))


if __name__ == '__main__':
    main()
