"""Complete state search with rollback white-tree tests and matching repair.

No existing lab object or export format is modified. See proofs/algorithm.
"""
from collections import Counter, deque
from itertools import combinations
import networkx as nx
from ..core import Instance, edge
from ..algorithms import separators


class RollbackForest:
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.size = dict.fromkeys(vertices, 1)
        self.log = []

    def find(self, x):
        while x != self.parent[x]:
            x = self.parent[x]
        return x

    def join(self, x, y):
        x, y = self.find(x), self.find(y)
        if x == y:
            return False
        if self.size[x] < self.size[y]:
            x, y = y, x
        self.log.append((x, y, self.size[x]))
        self.parent[y] = x
        self.size[x] += self.size[y]
        return True

    def rollback(self, mark):
        while len(self.log) > mark:
            x, y, size = self.log.pop()
            self.parent[y] = y
            self.size[x] = size


def enumerate_tree(b, stats=None, preferred=None, mrv=True):
    """Complete deterministic search. Return None exactly when no good state exists.

    Every frame owns a full extending matching. Forcing one incidence needs at
    most one augmenting-path repair. The white-edge forest is rolled back.
    """
    stats = stats if stats is not None else Counter()
    X = set(b.X)
    choices = [sorted(X.intersection(b.faces[t])) for t in b.A]
    white = set(b.white)
    ends = {}
    for i, t in enumerate(b.A):
        for x in choices[i]:
            ends[i, x] = tuple(next(y for y in (b.sides[x, z], b.sides[z, x]) if y in white)
                               for z in b.faces[t] if z != x)
    forest = RollbackForest(b.white)

    def augment(start, match, fixed):
        owner = {x: i for i, x in enumerate(match) if x is not None}
        prev = {start: None}
        queue = deque([start])
        while queue:
            i = queue.popleft()
            for x in choices[i]:
                j = owner.get(x)
                if j is None:
                    while True:
                        match[i], old = x, match[i]
                        if prev[i] is None:
                            return True
                        i, x = prev[i], old
                if j not in fixed and j not in prev:
                    prev[j] = i
                    queue.append(j)
        return False

    initial = [None] * b.n
    for i in range(b.n):
        if not augment(i, initial, set()):
            return None
    # Iterative search avoids dependence on Python's recursion limit.
    state = [None] * b.n
    fixed, used = set(), set()

    def frame(match):
        stats['prefixes'] += 1
        available = [(i, [x for x in choices[i] if x not in used])
                     for i in range(b.n) if i not in fixed]
        i, xs = min(available, key=lambda z: (len(z[1]), z[0])) if mrv else available[0]
        if preferred is not None:
            xs.sort(key=lambda x: (x != preferred[i], x))
        return [i, iter(xs), match, len(forest.log), None]

    stack = [frame(initial)]
    while stack:
        f = stack[-1]
        i, it, match, mark, old_x = f
        forest.rollback(mark)
        if old_x is not None:
            used.remove(old_x)
            fixed.remove(i)
            state[i] = None
            f[4] = None
        x = next(it, None)
        if x is None:
            stack.pop()
            continue
        stats['candidates'] += 1
        if not forest.join(*ends[i, x]):
            stats['cycle_rejections'] += 1
            continue
        trial = match.copy()
        if trial[i] != x:
            displaced = trial.index(x)
            trial[displaced] = None
            trial[i] = x
            stats['repairs'] += 1
            if not augment(displaced, trial, fixed | {i}):
                stats['matching_rejections'] += 1
                continue
        state[i] = x
        used.add(x)
        fixed.add(i)
        f[4] = x
        if len(fixed) == b.n:
            return tuple(state)
        stack.append(frame(trial))
    return None


def solve_piece(b, prescribed, stats, warm_start=False):
    """Reference gluing semantics, optimized complete enumeration at each leaf.

    Separators are still discovered per obstructed piece, not precomputed.
    """
    stats['pieces'] += 1
    s = None
    p = b.flow_pair() if warm_start else None
    if p is not None:
        seen = {p}
        # This bounded heuristic is never used as a termination argument.
        for _ in range(33):
            if b.is_tree(p[1]):
                s = p[1]
                break
            ns = [z for z in b.neighbors(p) if z not in seen]
            if not ns or stats['moves'] >= 32:
                break
            p = min(ns, key=lambda z: (len(b.qcycles(z[1])), z))
            seen.add(p)
            stats['moves'] += 1
    if s is None and (p is not None or not warm_start):
        if warm_start:
            from .path import path_tree, BudgetExceeded
            try:
                s = path_tree(b, stats, width_limit=12, state_limit=20000)
            except BudgetExceeded:
                stats['dp_budget_exceeded'] += 1
        if s is None:
            s = enumerate_tree(b, stats, preferred=p[1] if p is not None else None)
    if s is not None:
        return b.recover(s, prescribed)
    sep = next((x for x in separators(b) if x[2]), None)
    if sep is None:
        raise AssertionError('No good state and no black-inner separator')
    tri, components, _ = sep
    tri = set(tri)
    outside = next(c for c in components if c & b.R)
    inside = next(c for c in components if c != outside)

    def piece(vertices, root):
        t = b.T.subgraph(vertices | tri).copy()
        unrooted = Instance(t)
        return Instance(t, next(i for i, f in enumerate(unrooted.faces) if set(f) == root))

    a = solve_piece(piece(outside, b.R), prescribed, stats, warm_start)
    labels = {v: i for i, c in enumerate(a['classes']) for v in c}
    same = next(edge(u, v) for u, v in combinations(sorted(tri), 2) if labels[u] == labels[v])
    z = solve_piece(piece(inside, tri), same, stats, warm_start)
    labels2 = {v: i for i, c in enumerate(z['classes']) for v in c}
    v = min(tri)
    flip = labels[v] ^ labels2[v]
    if any(labels[v] != labels2[v] ^ flip for v in tri):
        raise AssertionError('Gluing prescription mismatch')
    labels.update({v: c ^ flip for v, c in labels2.items()})
    classes = [[v for v in b.T if labels[v] == i] for i in (0, 1)]
    p = [edge(u, v) for u, v in b.T.edges() if labels[u] == labels[v]]
    h = b.G.copy()
    h.remove_edges_from(b.dual_edges[e] for e in p)
    cycle = _cycle(h)
    stats['splits'] += 1
    return {'classes': classes, 'P': p, 'cycle': cycle, 'avoided_edge': b.dual_edges[prescribed]}


def _cycle(h):
    start = next(iter(h))
    cycle, prev, cur = [start], None, start
    while True:
        nxt = next(v for v in h[cur] if v != prev)
        if nxt == start:
            return cycle
        if nxt in cycle:
            raise AssertionError('Premature cycle')
        cycle.append(nxt)
        prev, cur = cur, nxt


def verify(g, cycle, forbidden):
    """Independent certificate checker: no dual, state or recovery operations."""
    if len(cycle) != len(g) or set(cycle) != set(g) or len(set(cycle)) != len(cycle):
        return False
    banned = frozenset(forbidden)
    return all(g.has_edge(a, b) and frozenset((a, b)) != banned
               for a, b in zip(cycle, cycle[1:] + cycle[:1]))


def hamiltonian_cycle(g, forbidden, stats=None):
    """Validate a Barnette graph and return an independently checked cycle."""
    if g.is_directed() or g.is_multigraph() or nx.number_of_selfloops(g):
        raise ValueError('Expected a simple undirected graph')
    if not g.has_edge(*forbidden):
        raise ValueError('Forbidden edge is absent')
    stats = stats if stats is not None else Counter()
    b = Instance.from_primal(g)
    inverse = {v: i for i, v in b.primal_labels.items()}
    e = edge(*(inverse[v] for v in forbidden))
    e0 = next(x for x, y in b.dual_edges.items() if y == e)
    rooted = Instance(b.T, inverse[forbidden[0]])
    cert = solve_piece(rooted, e0, stats, warm_start=True)
    cycle = [b.primal_labels[v] for v in cert['cycle']]
    if not verify(g, cycle, forbidden):
        raise AssertionError('Invalid Hamiltonian certificate')
    return cycle
