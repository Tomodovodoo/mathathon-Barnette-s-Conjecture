"""Structural census for the induction step at a triangulation without separating
triangles: for every root and every non-root degree-4 vertex x, which of the two
contractions at x keep a pair ("good")?  one-sided = exactly one good, two-sided = both.
usage: python onesided.py VMIN VMAX OUT.json [--c4]
--c4 generates only triangulations without separating triangles (plantri -bc4)."""
import sys, json, subprocess, time
import et


def plantri_c4(nv):
    out = subprocess.run([et.PLANTRI, "-bc4", "-a", str(nv)], capture_output=True, text=True).stdout
    res = []
    for line in out.splitlines():
        line = line.strip()
        if line:
            n, body = line.split(" ", 1)
            res.append([[ord(c) - 97 for c in part] for part in body.split(",")])
    return res


vmin, vmax, outp = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
c4 = "--c4" in sys.argv
summary = {}
for nv in range(vmin, vmax + 1):
    t = time.time()
    S = dict(V=nv, triangulations_without_sep_triangle=0, rooted=0, no_good_contraction=0,
             no_one_sided_vertex=0, only_two_sided=[], x_one_sided=0, x_two_sided=0, x_none=0)
    for gid, rot in enumerate(plantri_c4(nv) if c4 else et.plantri(nv)):
        first = True
        for blacks, ri, whites in et.rooted_instances(rot):
            t0 = blacks[ri]
            if first:
                if et.separating_triangles(blacks, whites, t0):
                    break
                first = False
                S["triangulations_without_sep_triangle"] += 1
            S["rooted"] += 1
            one = two = 0
            for (x, a, v1, b, v2) in et.degree4_setups(blacks, whites, t0):
                good = 0
                for (p, q) in ((v1, v2), (a, b)):
                    res = et.contract(blacks, ri, x, p, q)
                    if res and et.is_simple(res[0]) and et.has_pair_flow(*res):
                        good += 1
                if good == 1:
                    one += 1; S["x_one_sided"] += 1
                elif good == 2:
                    two += 1; S["x_two_sided"] += 1
                else:
                    S["x_none"] += 1
            if one + two == 0:
                S["no_good_contraction"] += 1
            if one == 0:
                S["no_one_sided_vertex"] += 1
                if len(S["only_two_sided"]) < 20:
                    S["only_two_sided"].append(dict(gid=gid, t0=list(t0), two_sided=two,
                                                    rot=["".join(chr(97 + u) for u in r) for r in rot]))
    S["seconds"] = round(time.time() - t, 1)
    summary[nv] = S
    print(json.dumps(S), flush=True)
json.dump(summary, open(outp, "w"), indent=1)
