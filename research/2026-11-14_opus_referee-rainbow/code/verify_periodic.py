"""Re-verify Fable's periodic surplus walks with my own code.
Reads only the rotation system, the outer face and sigma from Fable's JSON files.
Usage: python verify_periodic.py <json files...>   Output: ../data/periodic.json"""
import sys, json
from core import Tri, Rooted
import rb


def load_examples(path):
    d = json.load(open(path))
    r = d.get('result', d)
    exs = r.get('examples') or r.get('failures') or []
    return exs


def run(ex):
    tri = Tri(ex['rot'])
    outer = set(ex.get('outer_face_vertices') or ex.get('outer_face'))
    f0 = [f for f, fc in enumerate(tri.faces) if set(fc) == outer][0]
    R = Rooted(tri, f0)
    fid = {frozenset(tri.faces[f]): f for f in R.black}
    sig = {int(x): fid[frozenset(v)] for x, v in ex['sigma'].items()}
    assert set(sig) == set(R.X)
    assert rb.is_rainbow(R, sig), 'not a rainbow tree'
    exc = rb.excess(R, sig)
    res = []
    L = rb.loads(R, sig)
    for t in R.A:
        if L[t] != 2:
            continue
        for arr in [x for x in R.X if sig[x] == t]:
            start = (t, arr, rb.key(R, sig))
            state = (dict(sig), t, arr)
            for step in range(1, 20000):
                r = rb.walk_step(R, *state)
                if r[0] == 'stop':
                    res.append(('descent', step)); break
                state = r[1:]
                assert rb.is_rainbow(R, state[0])
                if (state[1], state[2], rb.key(R, state[0])) == start:
                    res.append(('cycle', step)); break
            else:
                res.append(('cap', None))
    return {'V': tri.V, 'excess': exc, 'walkers': res}


if __name__ == '__main__':
    out = []
    for p in sys.argv[1:]:
        for ex in load_examples(p):
            try:
                r = run(ex)
            except Exception as e:  # report, do not hide
                r = {'error': repr(e)}
            r['file'] = p.split('/')[-1]
            r['claimed_periods'] = ex.get('periods')
            out.append(r)
            print(r, flush=True)
    json.dump({'command': 'python verify_periodic.py ' + ' '.join(a.split('/')[-1] for a in sys.argv[1:]),
               'results': out}, open('../data/periodic.json', 'w'), indent=1)
