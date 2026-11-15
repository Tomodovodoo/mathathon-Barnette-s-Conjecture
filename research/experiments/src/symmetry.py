"""The automorphism group of a plane triangulation as a point group.

A 3-connected plane graph has the same automorphisms as its abstract graph,
and they form a finite group of isometries of the sphere.  The type is named
in Schoenflies notation: C1, Cs, Ci, Cn, Cnv, Cnh, S2n, Dn, Dnh, Dnd, T, Td,
Th, O, Oh, I, Ih.
"""
import fb


def group_type(order, order_op, aut_info):
    """aut_info: rows (orientation-preserving, order, fixes a vertex, an edge
    or a face) for all automorphisms."""
    rot = [int(o) for op, o, _ in aut_info if op]
    if len(aut_info) != order or len(rot) != order_op:
        return '?'
    kmax = max(rot)
    if kmax == order_op:
        base, n = 'C', order_op
    elif order_op % 2 == 0 and kmax == order_op // 2 or order_op == 4:
        base, n = 'D', order_op // 2
    elif order_op in (12, 24, 60):
        base, n = {12: 'T', 24: 'O', 60: 'I'}[order_op], 0
    else:
        return '?'
    if order == order_op:
        return {'C': f'C{n}', 'D': f'D{n}'}.get(base, base)
    if order != 2 * order_op:
        return '?'
    reflections = sum(1 for op, o, fixed in aut_info if not op and o == 2 and fixed)
    if base == 'C':
        if n == 1:
            return 'Cs' if reflections == 1 else 'Ci'
        if reflections == n:
            return f'C{n}v'
        if reflections == 1:
            return f'C{n}h'
        return f'S{2 * n}' if reflections == 0 else '?'
    if base == 'D':
        if reflections == n + 1:
            return f'D{n}h'
        return f'D{n}d' if reflections == n else '?'
    if base == 'T':
        return {6: 'Td', 3: 'Th'}.get(reflections, '?')
    return base + 'h'


def family_of_type(name):
    """A coarse class: trivial, cyclic, dihedral, tetrahedral, octahedral,
    icosahedral; with the suffix '*' if there are orientation-reversing
    automorphisms."""
    if name == 'C1':
        return 'trivial'
    if name in ('Cs', 'Ci'):
        return 'cyclic*'
    star = '' if name[1:].isdigit() or name in ('T', 'O', 'I') else '*'
    base = {'C': 'cyclic', 'S': 'cyclic', 'D': 'dihedral', 'T': 'tetrahedral', 'O': 'octahedral',
            'I': 'icosahedral'}[name[0]]
    if name[0] == 'S':
        star = '*'
    return base + star


def describe(F):
    """Canonical code, group order and type, and the orbits of the faces and
    of the pairs (face, side) of the triangulation F."""
    c = fb.canon(F)
    c['type'] = group_type(c['order'], c['order_op'], c['aut_info'])
    return c
