"""Exact edge-frontier DP for a good state; explicit optional resource caps.

Retained spokes form a forest. Deleted spokes form a partial matching.
The outer centre stays on every frontier, preventing closed components.
"""


class BudgetExceeded(RuntimeError):
    pass


def path_tree(b, stats=None, width_limit=None, state_limit=None):
    stats = stats if stats is not None else {}
    anchor = ('t', b.outer)
    edges = [(('t', t), ('v', v))
             for t in sorted(b.black, key=lambda t: tuple(sorted(b.faces[t])))
             for v in sorted(b.faces[t])]
    last = {v: k for k, e in enumerate(edges) for v in e}
    bag = [anchor]
    stages = []
    for k, (u, v) in enumerate(edges):
        add = [x for x in (u, v) if x not in bag]
        large = bag + add
        keep = [i for i, x in enumerate(large) if x == anchor or last[x] > k]
        stages.append((large, add, keep, large.index(u), large.index(v)))
        bag = [large[i] for i in keep]
    width = max(len(s[0]) for s in stages)
    stats['frontier_width'] = width
    if width_limit is not None and width > width_limit:
        raise BudgetExceeded('frontier width')

    def target(x):
        return x != anchor and not (x[0] == 'v' and x[1] in b.R)

    def canonical(part):
        labels = {}
        return tuple(labels.setdefault(x, len(labels)) for x in part)

    states = {(0, (0,)): (None,) * b.n}
    face_index = {t: i for i, t in enumerate(b.A)}
    total = 0
    for (u, v), (bag, add, keep, ui, vi) in zip(edges, stages):
        next_states = {}
        forgotten = set(range(len(bag))) - set(keep)
        for (mask, part), chosen in states.items():
            total += 1
            start_label = max(part) + 1
            part = part + tuple(range(start_label, start_label + len(add)))
            alternatives = []
            if part[ui] != part[vi]:
                old, new = part[vi], part[ui]
                alternatives.append((mask, tuple(new if x == old else x for x in part), chosen))
            if target(u) and target(v) and not mask & ((1 << ui) | (1 << vi)):
                state = list(chosen)
                state[face_index[u[1]]] = v[1]
                alternatives.append((mask | (1 << ui) | (1 << vi), part, tuple(state)))
            for bits, blocks, state in alternatives:
                if any(bool(bits & (1 << i)) != target(bag[i]) for i in forgotten):
                    continue
                if set(blocks) != {blocks[i] for i in keep}:
                    continue
                key = (sum(((bits >> i) & 1) << j for j, i in enumerate(keep)),
                       canonical(tuple(blocks[i] for i in keep)))
                next_states.setdefault(key, state)
        if state_limit is not None and len(next_states) > state_limit:
            raise BudgetExceeded('DP states')
        states = next_states
        stats['peak_states'] = max(stats.get('peak_states', 0), len(states))
        if not states:
            return None
    stats['dp_states_processed'] = total
    return states.get((0, (0,)))
