"""Assert, from figdata.json alone, every fact that the figures and their captions show.

Usage: python check.py     (from this folder). Uses sf.py for the graph objects; reads nothing else.
"""
import json
import sf

D = json.load(open('figdata.json'))
I = sf.Inst(D['running']['faces'], D['running']['t0'])
fidx = {f: i for i, f in enumerate(I.A)}


def sig(d):
    return {int(x): fidx[tuple(f)] for x, f in d.items()}


n_checks = 0


def ok(cond, what):
    global n_checks
    assert cond, what
    n_checks += 1


# the example
ok(I.V == 13 and I.R == {0, 4, 5} and I.n == 10 and len(I.white) == 11, 'example sizes')
trees = I.rainbow_trees()
ok(len(trees) == 1792 == D['running']['rainbow_trees'], '1792 rainbow trees')
ok(sum(1 for t in trees if I.excess(t) == 0) == 6, 'six good states')
ok(len(I.two_factors()) == 2, 'two 2-factors')

# Figure 1
a, b = sig(D['rainbow']['a']), sig(D['rainbow']['b'])
for s in (a, b):
    ok(I.is_rainbow(s) and I.w_tree([(s[x], x) for x in I.X]), 'rainbow tree and tree on white faces')
ok(I.excess(a) == 2 and I.excess(b) == 0, 'excess 2 and 0')
la = I.load(a)
ok(la[fidx[(1, 2, 9)]] == 2 and la[fidx[(0, 2, 3)]] == 0, 'loads in panel (a)')
ok(I.good_state({b[x]: x for x in I.X}), 'panel (b) is a good state by the definition with Q_s')

# Figure 2
u = {fidx[tuple(json.loads(k.replace('(', '[').replace(')', ']')))]: v for k, v in D['digraph']['u'].items()}
used = {x: [i for i in I.at[x] if u[i] != x] for x in I.X}
ok(all(len(used[x]) == 2 for x in I.X) and all(sum(1 for x in I.X if i in used[x]) == 2 for i in range(I.n)), 'u is the deleted-corner map of a 2-factor')
ok(all(a[x] in used[x] for x in I.X), 'sigma lies in this 2-factor')
arcs = sorted([v, u[i]] for i, f in enumerate(I.A) for v in f if v != u[i])
ok(arcs == D['digraph']['all_arcs'] and len(arcs) == 20, 'arcs of G_u')
ok([1, 8] in arcs and [8, 9] in arcs and [9, 1] in arcs, 'directed cycle 1 -> 8 -> 9 -> 1')
forest = {int(x): y for x, y in D['digraph']['forest'].items()}
par = I.parent(a)
ok(all(forest[x] == u[par[x]] and par[x] in used[x] and par[x] != a[x] for x in I.X), 'forest arcs are x -> u(par(x))')
for x in I.X:
    y, k = x, 0
    while y in forest:
        y, k = forest[y], k + 1
        assert k <= I.n
    ok(y in I.R, 'forest leads to a root')
t0, t2 = fidx[(0, 2, 3)], fidx[(1, 2, 9)]
ok(sum(1 for x in I.X if par[x] == t0) == 2 and sum(1 for x in I.X if par[x] == t2) == 0, 'arcs of the faces of load 0 and 2')

# Figure 3
E = D['exchange']
x = E['x']
ok(x == 8 and a[x] == fidx[tuple(E['old_face'])] == fidx[(8, 9, 10)], 'exchange starts at 8 in {8,9,10}')
ok(I.alts(a, x) == [fidx[tuple(E['new_face'])]] and tuple(E['new_face']) == (8, 11, 12), 'unique exchange to {8,11,12}')
g = E['gamma']
rem = {(a[y], y) for y in I.X} - {(a[x], x)}
for p, q in zip(g, g[1:] + g[:1]):
    v, f = (p, q) if isinstance(p, int) else (q, p)
    ok((fidx[tuple(f)], v) in I.spokes and (fidx[tuple(f)], v) not in rem, 'cycle Gamma uses spokes of F_sigma + (sigma(x), x)')
ok([tuple(z) for z in g if not isinstance(z, int)] == [(8, 11, 12), (4, 10, 11), (3, 4, 9), (8, 9, 10)], 'centres on Gamma')
a2 = dict(a)
a2[x] = fidx[(8, 11, 12)]
ok(I.excess(a2) == 4 and I.load(a)[fidx[(8, 11, 12)]] == 1, 'excess rises from 2 to 4')

# Figure 4
O = D['orbit']
t = fidx[tuple(O['t'])]
s, im = sig(O['s']), sig(O['image'])
ok(s == b and tuple(O['t']) == (0, 2, 3), 'orbit starts at the good state of Figure 1(b), t = {0,2,3}')
res, walk = I.iota(s, t)
ok(res == im and len(walk) == 2 == len(O['walk']), 'walk has two states and ends at the image')
for w, wd in zip(walk, O['walk']):
    ok(w[0] == sig(wd['sigma']) and I.A[w[1]] == tuple(wd['face']) and w[2] == wd['arrival'], 'walk state as drawn')
ok(walk[0][0] == a, 'S_1 is the tree of Figure 1(a)')
ok([(I.A[w[1]], w[2]) for w in walk] == [((1, 2, 9), 2), ((3, 4, 9), 9)], 'faces and arrivals of S_1, S_2')
ok(I.excess(im) == 0 and im != s and I.iota(im, t)[0] == s and im[3] == t, 'involution, no fixed point, 3 ends in t')

# Figure 5
B = D['badcover']
rot = sf.plantri(16)[B['plantri_index']]
fs = sf.faces_of(rot)
ok([list(f) for f in fs] == B['faces'], 'faces are those of plantri -b -a 16, index 27')
J = sf.Inst(fs, fs.index((0, 1, 2)))
ok(not J.black_inner_triangles(), 'no separating triangle with black inner boundary')
facs = J.two_factors()
ok(len(facs) == 3 == B['covers_in_this_rooting'], 'three 2-factors')
goods = [s for s in J.states() if J.good_state(s)]
ok(len(goods) == 12 == B['good_states_in_this_rooting'], '12 good states')
jf = {f: i for i, f in enumerate(J.A)}
ub = {jf[tuple(json.loads(k.replace('(', '[').replace(')', ']')))]: v for k, v in B['u'].items()}
ok(ub in facs, 'the drawn cover is a 2-factor')
cyc = J.factor_cycles(ub)
ok(len(cyc) == 1 and len(cyc[0]) == 13, 'one cycle through 13 vertices')
sts = J.states_in(ub)
ok(len(sts) == 2 and not any(J.good_state(s) for s in sts), 'neither state is good')
for sd, cy in zip(B['states'], B['q_cycles']):
    s = {jf[tuple(json.loads(k.replace('(', '[').replace(')', ']')))]: v for k, v in sd.items()}
    r = [z for z in sts if z != s][0]
    ok(s in sts, 'drawn state is a state of the cover')
    for p, q in zip(cy, cy[1:] + cy[:1]):
        ok(any(r[i] == p and q not in (s[i], r[i]) and q in J.A[i] for i in range(J.n)), 'arc r(t) -> u(t) of the directed triangle')
ok(sorted(map(sorted, B['q_cycles'])) == [[5, 13, 14], [9, 12, 14]], 'the two directed triangles')
cnt = 0
usedb = {x: [i for i in J.at[x] if ub[i] != x] for x in J.X}
for bits in range(1 << J.n):
    sg = {x: usedb[x][(bits >> j) & 1] for j, x in enumerate(J.X)}
    if J.is_rainbow(sg):
        cnt += 1
        assert J.excess(sg) > 0
ok(cnt == 6144 == B['rainbow_trees_inside_the_cover'], '6144 rainbow trees inside, none of excess 0')
print('all', n_checks, 'figure checks passed')
