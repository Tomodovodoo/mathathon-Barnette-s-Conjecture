"""Stage 3: the figures, from the tables in data/ only.

  python src/plots.py

Writes figures/<name>.pdf and figures/<name>.png.  The same colour and marker
stand for the same class of graphs in every figure.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt                               # noqa: E402
import numpy as np                                            # noqa: E402
import pandas as pd                                           # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA, FIG = ROOT / 'data', ROOT / 'figures'

# Categorical colours, checked for colour-vision deficiencies; every class also
# has its own marker, so no class is told apart by colour alone.
C = {'exhaustive': '#2a78d6', 'random3': '#eb6834', 'random4': '#1baf7a', 'prism': '#6250d6',
     'tube': '#e87ba4', 'octahedral': '#008300', 'trap': '#e34948', 'other': '#eda100'}
MARK = {'exhaustive': 'o', 'random3': 's', 'random4': '^', 'prism': 'D', 'tube': 'v', 'octahedral': 'P',
        'trap': 'X', 'other': '*'}
NAME = {'exhaustive': 'all graphs (exhaustive)', 'random3': 'random',
        'random4': 'random, no 3-edge cut', 'prism': 'prisms',
        'tube': 'tubes', 'octahedral': 'octahedral, 4- and 6-faces', 'trap': 'trap chains'}
INK, MUTED, GRID = '#0b0b0b', '#898781', '#e1e0d9'

plt.rcParams.update({
    'font.size': 9, 'axes.titlesize': 9.5, 'axes.labelsize': 9, 'legend.fontsize': 8,
    'xtick.labelsize': 8, 'ytick.labelsize': 8, 'axes.edgecolor': '#c3c2b7', 'axes.linewidth': 0.8,
    'axes.grid': True, 'grid.color': GRID, 'grid.linewidth': 0.6, 'axes.axisbelow': True,
    'axes.spines.top': False, 'axes.spines.right': False, 'legend.frameon': False,
    'lines.linewidth': 1.6, 'lines.markersize': 4.5, 'figure.dpi': 110, 'savefig.dpi': 200,
    'pdf.fonttype': 42, 'text.color': INK, 'axes.labelcolor': INK, 'xtick.color': '#52514e',
    'ytick.color': '#52514e', 'figure.facecolor': 'white', 'axes.facecolor': 'white'})


def save(fig, name):
    FIG.mkdir(exist_ok=True)
    fig.savefig(FIG / f'{name}.pdf', bbox_inches='tight')
    fig.savefig(FIG / f'{name}.png', bbox_inches='tight')
    plt.close(fig)


def load():
    ex = pd.read_csv(DATA / 'exhaustive_summary.csv')
    ls = pd.read_csv(DATA / 'large_summary.csv')
    lg = pd.read_csv(DATA / 'large_graphs.csv.gz')
    li = pd.read_csv(DATA / 'large_instances.csv.gz')
    li = li.merge(lg[['gid', 'source', 'params', 'N', 'nsep', 'maxdeg', 'aut']], on='gid')
    fits = json.loads((DATA / 'fits.json').read_text())
    tails = pd.read_csv(DATA / 'exhaustive_tails.csv')
    deep = pd.read_csv(DATA / 'deep.csv') if (DATA / 'deep.csv').exists() else None
    return ex, ls, lg, li, fits, tails, deep


def ex_metric(ex, metric, group='all', value='all'):
    return ex[(ex['metric'] == metric) & (ex['group'] == group) & (ex['value'].astype(str) == value)].sort_values('N')


def ls_metric(ls, source, metric):
    return ls[(ls['source'] == source) & (ls['metric'] == metric)].sort_values('N')


def param(params, key):
    return params.str.extract(rf'{key}=(\d+)')[0].astype(float)


def family_ratio(li, source, cond=None):
    """Per graph: the median over the faces t0 of the exact proportion."""
    d = li[(li['source'] == source) & (li['has_pair'] == 1) & (li['good'] >= 0)].copy()
    if cond is not None:
        d = d[cond(d)]
    d['ratio'] = d['good'] / 10.0 ** d['log10_states']
    return d.groupby('N')['ratio'].median().reset_index()


def fig_proportion(ex, ls, li, fits, deep):
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    r = ex_metric(ex, 'ratio')
    r = r[r['count'] >= 20]
    ax.fill_between(r['N'], r['min'], r['max'], color=C['exhaustive'], alpha=0.13, lw=0,
                    label='all graphs: minimum to maximum')
    ax.fill_between(r['N'], r['q05'], r['q95'], color=C['exhaustive'], alpha=0.28, lw=0,
                    label='all graphs: 5% to 95%')
    ax.plot(r['N'], r['mean'], color=C['exhaustive'], marker=MARK['exhaustive'], label='all graphs: mean')
    for source in ('random3', 'random4'):
        m = ls_metric(ls, source, 'ratio')
        exact = ls_metric(ls, source, 'good_exact').set_index('N')['mean']
        m = m[m['N'].map(exact) >= 0.999]
        ax.errorbar(m['N'], m['median'], yerr=[m['median'] - m['q25'], m['q75'] - m['median']],
                    color=C[source], marker=MARK[source], ls='none', capsize=2, elinewidth=1,
                    label=f'{NAME[source]}: median, quartiles')
        f = fits.get(f'{source} ratio median')
        if f:
            n = np.array([f['n_from'], f['n_to']])
            ax.plot(2 * n + 2, f['c'] * f['r'] ** n, color=C[source], ls='--', lw=1.1)
    if deep is not None:
        d = deep[deep['status'] == 0]
        for kind, source in ((2, 'random3'), (3, 'random4')):
            q = d[(d['gid'] // 10**12 == kind) & (d['good'] > 0)]
            if len(q):
                g = q.groupby('n')['ratio']
                ok = g.count() >= 5
                med = g.median()[ok]
                ax.plot(2 * med.index + 2, med, color=C[source], marker=MARK[source], ls='none', mfc='white',
                        ms=6)
    for source, cond, label in (('prism', None, 'prisms'),
                                ('tube', lambda d: d['params'].str.startswith('k=3 '), 'tubes, k = 3'),
                                ('octahedral', None, NAME['octahedral'])):
        f = family_ratio(li, source, cond)
        f = f[f['N'] <= 1000]
        ax.plot(f['N'], f['ratio'], color=C[source], marker=MARK[source], ms=3.5, lw=1.0, label=label)
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xlabel('number of vertices N of G')
    ax.set_ylabel('good states / states')
    ax.set_title('Proportion of good states (instances with a pair)')
    ax.plot([], [], color=MUTED, ls='--', lw=1.1, label='fit to the random medians')
    ax.plot([], [], color=MUTED, marker='s', mfc='white', ls='none', ms=6, label='open symbol: subsample, larger budget')
    ax.legend(loc='lower left', ncol=1)
    save(fig, 'proportion')


def fig_states(ex, ls, li):
    """The n-th root of the number of states, n = N/2 - 1."""
    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    s = ex_metric(ex, 'states')
    s = s[s['count'] >= 20]
    root = lambda m, n: np.asarray(m, float) ** (1 / np.asarray(n, float))
    ax.fill_between(s['N'], root(s['min'], s['n']), root(s['max'], s['n']), color=C['exhaustive'], alpha=0.2,
                    lw=0, label='all graphs: minimum to maximum')
    ax.plot(s['N'], root(s['median'], s['n']), color=C['exhaustive'], marker=MARK['exhaustive'],
            label='all graphs: median')
    for source in ('random3', 'random4'):
        m = ls_metric(ls, source, 'log10_states')
        ax.plot(m['N'], 10 ** (m['median'] / m['n']), color=C[source], marker=MARK[source], ls='none',
                label=f'{NAME[source]}: median')
    for source, cond, label in (('prism', None, 'prisms'),
                                ('tube', lambda d: d['params'].str.startswith('k=3 '), 'tubes, k = 3'),
                                ('octahedral', None, NAME['octahedral'])):
        d = li[(li['source'] == source) & (li['has_pair'] == 1)]
        if cond is not None:
            d = d[cond(d)]
        f = d.groupby('N')[['log10_states', 'n']].median().reset_index()
        ax.plot(f['N'], 10 ** (f['log10_states'] / f['n']), color=C[source], marker=MARK[source], ms=3.5, lw=1.0,
                label=label)
    ax.axhline(3 ** 0.5, color=MUTED, ls=':', lw=1.3)
    ax.text(9, 3 ** 0.5 + 0.012, r'upper bound $\sqrt{3}$', color='#52514e', fontsize=8)
    ax.set_xscale('log')
    ax.set_ylim(0.98, 1.8)
    ax.set_xlabel('number of vertices N of G')
    ax.set_ylabel(r'(number of states)$^{1/n}$, $n=N/2-1$')
    ax.set_title('Growth rate of the number of states (instances with a pair)')
    ax.legend(loc='center left', bbox_to_anchor=(1.01, 0.5))
    save(fig, 'states')


def fig_classes(ex):
    """Mean proportion by class.  Only the sizes with N divisible by 4 are
    drawn: the level alternates with the parity of n, and the two parities
    show the same order of the classes."""
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.9), sharey=True)
    panels = (('aut_class', 'order of the automorphism group', ['1', '2', '3-4', '5-8', '>8']),
              ('face_class', 'largest face of G', ['4,6', '8', '10', '12', '>=14']),
              ('sep_class', 'separating triangles of T', ['0', '1', '2', '3', '>=4']))
    cols = ['#2a78d6', '#eb6834', '#1baf7a', '#6250d6', '#e34948']
    marks = ['o', 's', '^', 'D', 'X']
    for ax, (group, title, values) in zip(axes, panels):
        for value, col, mk in zip(values, cols, marks):
            r = ex_metric(ex, 'ratio', group, value)
            r = r[(r['count'] >= 30) & (r['N'] >= 24) & (r['N'] % 4 == 0)]
            label = {'4,6': 'only 4 and 6', '>=14': '14 or more', '>=4': '4 or more', '>8': 'more than 8'}.get(
                value, value)
            if len(r):
                ax.plot(r['N'], r['mean'], color=col, marker=mk, label=label)
        ax.set_yscale('log')
        ax.set_title(title)
        ax.set_xticks(range(24, 41, 4))
        ax.set_xlabel('number of vertices N of G')
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3, columnspacing=1.0, handletextpad=0.4)
    axes[0].set_ylabel('good states / states (mean)')
    fig.suptitle('Proportion of good states by class: all graphs, N = 24, 28, ..., 40, instances with a pair',
                 y=1.0, fontsize=10)
    save(fig, 'proportion_by_class')


WALKS = (('moves', 'st_walk'), ('moves_mirror', 'st_walk_mirror'), ('moves_rand', 'st_walk_rand'))
ORDERS = (('nodes', 'stored order', '-', 'o'), ('nodes_bfs', 'breadth-first order', '--', 's'),
          ('nodes_rand', 'random order', ':', '^'))


def fig_search(ex, ls, li):
    fig = plt.figure(figsize=(10.6, 6.0))
    gs = fig.add_gridspec(2, 2, height_ratios=[3, 1.2], hspace=0.12, wspace=0.22)
    ax = fig.add_subplot(gs[:, 0])
    for col, label, ls_, mk in ORDERS:
        r = ex_metric(ex, col + '_per_n')
        r = r[r['count'] >= 20]
        ax.plot(r['N'], r['mean'], color=C['exhaustive'], ls=ls_, marker=mk, label=f'{label}: mean')
        ax.plot(r['N'], r['max'], color=C['exhaustive'], ls=ls_, marker=mk, mfc='white', lw=1.0,
                label=f'{label}: maximum')
    b = ex_metric(ex, 'bound_per_n')
    b = b[b['count'] >= 20]
    ax.plot(b['N'], b['median'], color=MUTED, ls='-.', lw=1.2, label=r'bound $(n+1)M_T/n$: median')
    ax.set_yscale('log')
    ax.set_xticks(range(20, int(b['N'].max()) + 1, 4))
    ax.set_xlabel('number of vertices N of G')
    ax.set_ylabel('partial choices kept / n')
    ax.set_title(f'All graphs with N ≤ {int(b["N"].max())} (no run censored)')
    ax.legend(loc='upper left', ncol=1)

    ax = fig.add_subplot(gs[0, 1])
    ax2 = fig.add_subplot(gs[1, 1], sharex=ax)
    for source in ('random3', 'random4'):
        d = li[li['source'] == source]
        for col, label, ls_, mk in ORDERS:
            st = {'nodes': 'st_search', 'nodes_bfs': 'st_bfs', 'nodes_rand': 'st_rand'}[col]
            xs, med, cens = [], [], []
            for N, part in d.groupby('N'):
                x = np.where(part[st] == 0, part[col] / part['n'], np.inf)
                xs.append(N)
                med.append(np.median(x))
                cens.append(float((part[st] == 1).mean()))
            xs, med, cens = map(np.array, (xs, med, cens))
            ok = np.isfinite(med)
            ax.plot(xs[ok], med[ok], color=C[source], ls=ls_, marker=mk, label=f'{NAME[source]}, {label}')
            ax2.plot(xs, cens, color=C[source], ls=ls_, marker=mk, ms=3)
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_title('Random graphs: median (a censored run counts as infinite)')
    ax.set_ylabel('partial choices kept / n')
    plt.setp(ax.get_xticklabels(), visible=False)
    handles, labels = ax.get_legend_handles_labels()
    ax2.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.42), ncol=2, fontsize=7.5)
    ax2.set_xlabel('number of vertices N of G')
    ax2.set_ylabel('share of runs\ncensored')
    ax2.set_ylim(-0.04, 1.04)
    fig.suptitle('Search for the first good state, in three orders of the faces', y=0.97, fontsize=10.5)
    save(fig, 'search_cost')


def fig_walk(ex, ls, li):
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.6))
    ax = axes[0]
    r = ex_metric(ex, 'moves')
    r = r[r['count'] >= 20]
    ax.plot(r['N'], r['mean'], color=C['exhaustive'], marker=MARK['exhaustive'], label='all graphs: mean')
    ax.plot(r['N'], r['max'], color=C['exhaustive'], marker=MARK['exhaustive'], mfc='white', lw=1.0, ls='--',
            label='all graphs: maximum')
    for source in ('random3', 'random4'):
        d = li[li['source'] == source]
        xs, med, q90, mx, cens = [], [], [], [], []
        for N, part in d.groupby('N'):
            w = np.concatenate([np.where(part[st] == 0, part[c], np.inf) for c, st in WALKS])
            xs.append(N)
            med.append(np.median(w))
            q90.append(np.quantile(w, 0.9, method='higher'))
            mx.append(w[np.isfinite(w)].max())
            cens.append(not np.isfinite(w).all())
        xs, med, q90, mx, cens = map(np.array, (xs, med, q90, mx, cens))
        ax.plot(xs, np.clip(med, 0.5, None), color=C[source], marker=MARK[source], label=f'{NAME[source]}: median')
        ok = np.isfinite(q90)
        ax.plot(xs[ok], np.clip(q90[ok], 0.5, None), color=C[source], marker=MARK[source], ls=':', lw=1.2,
                label=f'{NAME[source]}: 90%')
        ax.plot(xs, mx, color=C[source], marker=MARK[source], mfc='white', lw=1.0, ls='--',
                label=f'{NAME[source]}: largest finished')
        if cens.any():
            ax.plot(xs[cens], mx[cens], color=INK, marker='x', ls='none', ms=7)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('number of vertices N of G')
    ax.set_ylabel('moves of the exchange walk (0 drawn at 0.5)')
    ax.set_title('Exchange walk from the pair given by the flow')
    ax.plot([], [], color=INK, marker='x', ls='none', ms=7, label='some runs censored at this size')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.16), ncol=2)

    ax = axes[1]
    t = li[li['source'] == 'trap-chain'].sort_values('N')
    ax.plot(t['N'], t['moves'].clip(lower=0.5), color=C['trap'], marker=MARK['trap'],
            label='trap chains, as stored')
    ax.plot(t['N'], t['moves_mirror'].clip(lower=0.5), color=C['trap'], marker=MARK['trap'], mfc='white',
            ls='--', lw=1.0, label='trap chains, mirror image')
    for source, cond, label in (('octahedral', None, NAME['octahedral']),
                                ('tube', lambda d: d['params'].str.startswith('k=3 '), 'tubes, k = 3'),
                                ('prism', None, 'prisms')):
        d = li[li['source'] == source]
        if cond is not None:
            d = d[cond(d)]
        xs, med, cens = [], [], []
        for N, part in d.groupby('N'):
            w = np.concatenate([np.where(part[st] == 0, part[c], np.inf) for c, st in WALKS])
            xs.append(N)
            med.append(np.median(w))
            cens.append(not np.isfinite(w).all())
        xs, med, cens = map(np.array, (xs, med, cens))
        ok = np.isfinite(med)
        ax.plot(xs[ok], np.clip(med[ok], 0.5, None), color=C[source], marker=MARK[source], ms=3.5,
                lw=0 if source == 'octahedral' else 1.0, label=label)
        if (~ok).any():
            ax.plot(xs[~ok], np.full((~ok).sum(), 3e7), color=C[source], marker='x', ls='none', ms=5)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('number of vertices N of G')
    ax.set_ylabel('moves (median over the runs; 0 drawn at 0.5)')
    ax.set_title('Constructed families')
    ax.plot([], [], color=MUTED, marker='x', ls='none', ms=5, label='more than half of the runs censored')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.16), ncol=2)
    save(fig, 'walk_cost')


def fig_tails(tails, li):
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.0))
    ax = axes[0]
    V = int(tails.loc[tails['quantity'] == 'nodes_bfs_per_n', 'V'].max())
    for col, label, ls_, mk in ORDERS:
        t = tails[(tails['V'] == V) & (tails['quantity'] == col + '_per_n')].sort_values('value')
        ccdf = t['count'][::-1].cumsum()[::-1] / t['count'].sum()
        ax.step(t['value'], ccdf, where='post', color=C['exhaustive'], ls=ls_, label=label)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('partial choices kept / n')
    ax.set_ylabel('fraction of instances with at least this value')
    ax.set_title(f'Search, all instances with N = {2 * V - 4}')
    ax.legend()
    ax = axes[1]
    cols = ['#9ec5f4', '#5598e7', '#256abf', '#0d366b']
    d = li[li['source'] == 'random4']
    for N, col in zip((200, 500, 1000, 2000), cols):
        part = d[d['N'] == N]
        x = np.sort(np.concatenate([np.where(part[st] == 0, part[c], np.inf) for c, st in WALKS]))
        ccdf = 1 - np.arange(len(x)) / len(x)
        fin = np.isfinite(x)
        ax.step(np.clip(x[fin], 0.5, None), ccdf[fin], where='post', color=col,
                label=f'N = {N} ({len(x)} runs, {int((~fin).sum())} censored)')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('moves of the exchange walk (0 drawn at 0.5)')
    ax.set_ylabel('fraction of runs with at least this many moves')
    ax.set_title('Exchange walk, random graphs without 3-edge cut')
    ax.legend(loc='lower left', fontsize=7.5)
    save(fig, 'tails')


def fig_cycles(ex, tails):
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.8))
    ax = axes[0]
    r = ex_metric(ex, 'g_over_hmin')
    r = r[r['count'] >= 20]
    ax.fill_between(r['N'], r['q05'], r['q95'], color=C['exhaustive'], alpha=0.25, lw=0, label='5% to 95%')
    ax.plot(r['N'], r['median'], color=C['exhaustive'], marker='o', label='median')
    ax.plot(r['N'], r['min'], color=C['exhaustive'], marker='o', mfc='white', ls='--', lw=1.0, label='minimum')
    ax.set_yscale('log')
    ax.set_xlabel('number of vertices N of G')
    ax.set_ylabel('good states / Hamiltonian cycles avoiding e')
    ax.set_title('Good states among the Hamiltonian cycles avoiding e\n(e the edge at t0 avoided by the fewest cycles)')
    ax.set_xticks(range(20, int(r['N'].max()) + 1, 4))
    ax.legend(loc='lower left')
    ax = axes[1]
    r = ex_metric(ex, 'g_over_2m')
    r = r[r['count'] >= 20]
    V = r['V'].to_numpy()
    eq = []
    for v in V:
        t = tails[(tails['V'] == v) & (tails['quantity'] == 'g_over_2m')]
        eq.append(t.loc[t['value'] == 1, 'count'].sum() / t['count'].sum())
    ax.plot(r['N'], r['max'], color=C['exhaustive'], marker='o', mfc='white', ls='--', lw=1.0, label='maximum')
    ax.plot(r['N'], r['q99'], color=C['exhaustive'], marker='s', ls=':', label='99%')
    ax.plot(r['N'], r['mean'], color=C['exhaustive'], marker='o', label='mean')
    ax.plot(r['N'], r['min'], color=MUTED, marker='o', ms=3, lw=1.0, label='minimum (equals 1 throughout)')
    ax.set_yscale('log')
    ax.set_xlabel('number of vertices N of G')
    ax.set_ylabel(r'good states / $2^m$')
    ax.set_title('Good states against $2^m$\n($m$ the least number of cycles of a 2-factor of $H$)')
    ax.set_xticks(range(20, int(r['N'].max()) + 1, 4))
    ax.legend(loc='upper left')
    save(fig, 'cycles_and_bound')


def fig_random_state(ls):
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.8))
    for source in ('random3', 'random4'):
        m = ls_metric(ls, source, 'uni_excess')
        axes[0].plot(m['n'], m['mean'], color=C[source], marker=MARK[source], label=NAME[source])
        u = ls_metric(ls, source, 'uni_fraction')
        u = u[u['mean'] > 0]
        axes[1].plot(u['N'], u['mean'], color=C[source], marker=MARK[source],
                     label=f'{NAME[source]}: 1000 uniform states per instance')
        r = ls_metric(ls, source, 'ratio')
        exact = ls_metric(ls, source, 'good_exact').set_index('N')['mean']
        r = r[r['N'].map(exact) >= 0.999]
        axes[1].plot(r['N'], r['mean'], color=C[source], marker=MARK[source], mfc='white', ls='--', lw=1.0,
                     label=f'{NAME[source]}: exact')
    axes[0].set_xlabel('n = N/2 - 1')
    axes[0].set_ylabel('mean number of chosen sides that close a cycle')
    axes[0].set_title('A uniformly random state: distance from good')
    axes[0].legend()
    axes[1].set_yscale('log')
    axes[1].set_xlabel('number of vertices N of G')
    axes[1].set_ylabel('mean proportion of good states')
    axes[1].set_title('Chance that a uniformly random state is good')
    axes[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.17), ncol=2, fontsize=7.5)
    save(fig, 'random_state')


def fig_time(ex, li):
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    for metric, ls_, label in (('t_search', '-', 'search, stored order'), ('t_walk', '--', 'exchange walk')):
        r = ex_metric(ex, metric)
        r = r[r['count'] >= 20]
        ax.plot(r['N'], r['median'] * 1e3, color=C['exhaustive'], ls=ls_, marker='o', ms=3,
                label=f'all graphs, {label}')
        for source in ('random3', 'random4'):
            d = li[li['source'] == source]
            st = 'st_search' if metric == 't_search' else 'st_walk'
            xs, med = [], []
            for N, part in d.groupby('N'):
                x = np.where(part[st] == 0, part[metric], np.inf)
                xs.append(N)
                med.append(np.median(x) * 1e3)
            xs, med = np.array(xs), np.array(med)
            ok = np.isfinite(med)
            ax.plot(xs[ok], med[ok], color=C[source], ls=ls_, marker=MARK[source], label=f'{NAME[source]}, {label}')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('number of vertices N of G')
    ax.set_ylabel('median wall time per instance (ms)')
    ax.set_title('Wall time of the whole algorithm (censored runs count as infinite)')
    ax.legend(loc='upper left')
    save(fig, 'time')


def main():
    ex, ls, lg, li, fits, tails, deep = load()
    fig_proportion(ex, ls, li, fits, deep)
    fig_states(ex, ls, li)
    fig_classes(ex)
    fig_search(ex, ls, li)
    fig_walk(ex, ls, li)
    fig_tails(tails, li)
    fig_cycles(ex, tails)
    fig_random_state(ls)
    fig_time(ex, li)


if __name__ == '__main__':
    main()
