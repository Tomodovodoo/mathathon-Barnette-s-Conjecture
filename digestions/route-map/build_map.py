#!/usr/bin/env python3
"""Render the route map from routes.py.

Claim: every waypoint, step and route in routes.py appears in the figure, in routes.json,
in route-map.dot and in ROUTE-MAP.md, with one status style per route.

Command (from the repository root):
    python -X utf8 -B digestions/route-map/build_map.py
Output (next to this file):
    route-map.pdf, route-map.svg, route-map.png          the full map with every route listed
    route-map-overview.pdf, .svg, .png                    the same map without the route lists
    route-map.dot                                         the graph in Graphviz format
    routes.json                                           machine-readable export
    ROUTE-MAP.md                                          the written map
Needs matplotlib. Graphviz is not needed (it was not installed on the build machine).
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import routes as RT  # noqa: E402

WP = {w["id"]: w for w in RT.WAYPOINTS}
STEP = {s["id"]: s for s in RT.STEPS}
BY_STEP = defaultdict(list)
for r in RT.ROUTES:
    BY_STEP[r["step"]].append(r)

# role of a route in the picture
FACT_IDS = {"K.4", "F.6", "C.5", "A.6", "G.5", "S0.3", "ST.2", "ST.3", "ST.4", "A.d", "A.4", "C.1", "C.2", "K.2", "K.3", "N.id", "D.2", "D.4", "D.5",
            "F.2", "F.3", "G.1", "G.2", "G2.3", "G2.4", "G2.6", "E2.2", "J2.2", "G2.5"}
EQUIV_IDS = {"U.7", "TG.1", "TG.2", "U.1", "U.2", "U.3", "U.4", "U.5", "U.6"}


def role(r):
    if r["id"] in EQUIV_IDS:
        return "equiv"
    if r["id"] in FACT_IDS:
        return "fact"
    if r.get("partial"):
        return "partial"
    return "route"


STYLE = {   # colour, linestyle, linewidth
    "LIT": ("#111111", "-", 1.5),
    "PROVED-HERE": ("#1f5fbf", "-", 1.5),
    "COMPUTED": ("#1b8a5a", (0, (5, 1.5, 1, 1.5)), 1.3),
    "CONJECTURE": ("#c77700", (0, (1, 1.4)), 1.6),
    "HUNCH": ("#b9a26a", (0, (1, 2.2)), 1.4),
    "REFUTED": ("#c62828", (0, (3.5, 1.6)), 1.3),
    "PARTIAL": ("#8a8a8a", "-", 1.2),
}
VERDICT_COLOUR = {"forced": "#444444", "free": "#1b8a5a", "rigid": "#444444", "open": "#c77700"}
ORDER = {s: i for i, s in enumerate(RT.STATUS_ORDER)}


def sorted_routes(step):
    return sorted(BY_STEP[step], key=lambda r: (ORDER[r["status"]], r["id"]))


def strands(step):
    """What is drawn between the two waypoints: one strand per distinct published argument,
    then one per other route. Facts and reformulations are listed, not drawn."""
    out, seen = [], set()
    for r in sorted_routes(step):
        ro = role(r)
        if ro in ("fact", "equiv"):
            continue
        if r["status"] == "LIT" and ro == "route":
            a = r.get("arg", r["id"])
            if a in seen:
                continue
            seen.add(a)
            out.append("LIT")
        elif ro == "partial":
            out.append("PARTIAL")
        else:
            out.append(r["status"])
    return out


def n_published_args(step):
    return len({r.get("arg", r["id"]) for r in BY_STEP[step] if r["status"] == "LIT" and role(r) == "route"})


# ---------------------------------------------------------------- layout (inches)
RH = 0.185          # row height of a route list
FS = 7.2            # font size of a route row
LISTW = 4.25        # width of a route list
NW, NH = 2.25, 0.52  # waypoint box


def gap(step, detail):
    if not detail:
        return 1.3
    return max(1.25, len(BY_STEP[step]) * RH + 1.0)


def layout(detail):
    pos = {}
    y = 0.0
    left = [("G", None), ("T", "S0"), ("S", "ST"), ("P", "A"), ("M", "C"), ("N", "N"), ("FP", "D"), ("IT", "R")]
    for wid, st in left:
        if st:
            y -= gap(st, detail)
        pos[wid] = (0.0, y)
    xR = 13.9 if detail else 9.2
    yb = pos["IT"][1]
    top = 0.35 if detail else 0.0
    mins = [("SE", "E2"), ("JC", "F"), ("GL", "G"), ("HC", "G2")]
    need = sum(gap(s, detail) for _, s in mins)
    extra = max(0.0, (top - yb) - need)
    add = {"E2": 0.5 * extra, "F": 0.5 * extra, "G": 0.0, "G2": 0.0}
    pos["WT"] = (xR, yb)
    y = yb
    for wid, st in mins:
        y += gap(st, detail) + add[st]
        pos[wid] = (xR, y)
    xin = 3.6 if detail else 2.6
    pos["DI"] = (xin, pos["P"][1] + (0.45 if detail else 0.0))
    pos["K"] = (xin, pos["M"][1] - (1.25 if detail else 0.8))
    pos["2T"] = (xR - (3.4 if detail else 3.0), pos["GL"][1] - (0.1 if detail else 0.45))
    return pos, xR


def draw(detail, stem):
    pos, xR = layout(detail)
    nw, nh = (NW, NH) if detail else (1.95, 0.5)
    xmin, xmax = (-5.75, xR + 5.75) if detail else (-3.1, xR + 3.1)
    ymax = 1.75 if detail else 1.15
    ymin = pos["IT"][1] - (1.55 if detail else 2.85)
    fig = plt.figure(figsize=(xmax - xmin, ymax - ymin))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.axis("off")

    def node(wid, sub=None, goal=False):
        x, y = pos[wid]
        fc = "#fff6d6" if goal else "#f2f4f7"
        ec = "#111111"
        ax.add_patch(FancyBboxPatch((x - nw / 2, y - nh / 2), nw, nh, boxstyle="round,pad=0.02,rounding_size=0.09",
                                    fc=fc, ec=ec, lw=1.3, zorder=5))
        name = {"T": "Eulerian triangulation T = G*"}.get(wid, WP[wid]["name"])
        if sub:
            ax.text(x, y + 0.09, name, ha="center", va="center", fontsize=8.6 if detail else 8.0, weight="bold", zorder=6)
            ax.text(x, y - 0.13, sub, ha="center", va="center", fontsize=6.3, color="#444444", zorder=6)
        else:
            ax.text(x, y, name, ha="center", va="center", fontsize=8.6 if detail else 8.0, weight="bold", zorder=6)

    def seg_bundle(p, q, kinds, spacing=None, head=True):
        """Parallel strands from p to q. Refuted and partial strands stop on the way."""
        (x1, y1), (x2, y2) = p, q
        dx, dy = x2 - x1, y2 - y1
        L = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / L, dy / L
        px, py = -uy, ux
        k = len(kinds)
        spacing = spacing or (0.05 if detail else 0.04)
        for j, kind in enumerate(kinds):
            off = (j - (k - 1) / 2) * spacing
            col, ls, lw = STYLE[kind]
            a = (x1 + px * off, y1 + py * off)
            frac = {"REFUTED": 0.42, "PARTIAL": 0.6}.get(kind, 1.0)
            b = (a[0] + dx * frac, a[1] + dy * frac)
            ax.plot([a[0], b[0]], [a[1], b[1]], color=col, ls=ls, lw=lw, zorder=2, solid_capstyle="butt")
            if kind == "REFUTED":
                ax.plot([b[0]], [b[1]], marker="x", color=col, ms=4.5, mew=1.2, zorder=3)
            if kind == "PARTIAL":
                ax.plot([b[0] - px * 0.04, b[0] + px * 0.04], [b[1] - py * 0.04, b[1] + py * 0.04], color=col, lw=1.6, zorder=3)
        if head:
            ax.annotate("", xy=(x2, y2), xytext=(x2 - ux * 0.01, y2 - uy * 0.01),
                        arrowprops=dict(arrowstyle="-|>", color="#111111", lw=0, mutation_scale=13), zorder=4)

    def poly_bundle(pts, kinds, spacing=0.05):
        """Strands along a right-angled path S -> right -> down -> left (the bypass chord)."""
        (xa, ya), (xc, _), (_, yb), (xb, _) = pts[0], pts[1], pts[2], pts[3]
        k = len(kinds)
        total = (xc - xa) + (ya - yb) + (xc - xb)
        for j, kind in enumerate(kinds):
            d = (j - (k - 1) / 2) * spacing
            col, ls, lw = STYLE[kind]
            path = [(xa, ya + d), (xc + d, ya + d), (xc + d, yb - d), (xb, yb - d)]
            if kind == "REFUTED":
                stop = 0.3 * total
                out, acc = [path[0]], 0.0
                for (p, q) in zip(path, path[1:]):
                    seg = abs(q[0] - p[0]) + abs(q[1] - p[1])
                    if acc + seg >= stop:
                        t = (stop - acc) / seg
                        out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
                        break
                    out.append(q)
                    acc += seg
                path = out
            ax.plot([p[0] for p in path], [p[1] for p in path], color=col, ls=ls, lw=lw, zorder=2)
            if kind == "REFUTED":
                ax.plot([path[-1][0]], [path[-1][1]], marker="x", color=col, ms=4.5, mew=1.2, zorder=3)
        ax.annotate("", xy=(xb, yb), xytext=(xb + 0.01, yb),
                    arrowprops=dict(arrowstyle="-|>", color="#c77700", lw=0, mutation_scale=13), zorder=4)

    def thin(p, q, text=None, tpos=0.5, col="#666666", dx=0.08, dy=0.0, ha="left", ls="-"):
        ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=col, lw=1.0, ls=ls, mutation_scale=9), zorder=2)
        if text:
            ax.text(p[0] + (q[0] - p[0]) * tpos + dx, p[1] + (q[1] - p[1]) * tpos + dy, text, fontsize=6.4, color=col,
                    ha=ha, va="center", style="italic", zorder=6)

    def verdict_text(sid):
        s = STEP[sid]
        v, k = s["verdict"], n_published_args(sid)
        if v == "forced":
            return "FORCED: one published argument" if k <= 1 else f"FORCED: {k} wordings of one argument"
        if v == "rigid":
            return "RIGID"
        if v == "free":
            return f"FREE: {k} published arguments"
        return "OPEN: no route known"

    def rows(sid, x, ytop, width=LISTW):
        """The list of routes of a step, top-left corner at (x, ytop)."""
        s = STEP[sid]
        ax.text(x, ytop + 0.13, f"{sid}   {s['title']}", fontsize=8.0, weight="bold", va="center", ha="left", zorder=6)
        ax.text(x + width, ytop + 0.13, verdict_text(sid), fontsize=6.4, weight="bold", va="center", ha="right",
                color=VERDICT_COLOUR[s["verdict"]], zorder=6)
        ax.plot([x, x + width], [ytop, ytop], color="#999999", lw=0.6, zorder=1)
        y = ytop - RH * 0.62
        for r in sorted_routes(sid):
            ro = role(r)
            kind = "PARTIAL" if ro == "partial" else r["status"]
            col, ls, lw = STYLE[kind]
            if ro == "route" or ro == "partial":
                ax.plot([x, x + 0.3], [y, y], color=col, ls=ls, lw=lw, zorder=3)
                if kind == "REFUTED":
                    ax.plot([x + 0.3], [y], marker="x", color=col, ms=4, mew=1.1, zorder=3)
            elif ro == "equiv":
                ax.text(x + 0.15, y, "≡", fontsize=8.5, color=col, ha="center", va="center", zorder=3)
            else:
                ax.plot([x + 0.15], [y], marker="o", color=col, ms=2.8, zorder=3)
            tcol = "#111111" if kind in ("LIT", "PROVED-HERE", "COMPUTED") else col if kind == "REFUTED" else "#5a4500"
            if kind == "PARTIAL":
                tcol = "#555555"
            ax.text(x + 0.38, y, r["id"], fontsize=FS, weight="bold", va="center", ha="left", color=tcol, zorder=6)
            ax.text(x + 0.95, y, r["label"], fontsize=FS, va="center", ha="left", color=tcol, zorder=6)
            ax.text(x + width, y, r["src"], fontsize=FS - 1.0, va="center", ha="right", color="#666666", zorder=6)
            y -= RH
        return y

    def step_tag(sid, x, y, ha="left"):
        """Overview only: the step id and its verdict next to the bundle."""
        s = STEP[sid]
        c = Counter(r["status"] for r in BY_STEP[sid])
        ax.text(x, y + 0.11, f"{sid}  {s['title']}", fontsize=7.0, weight="bold", ha=ha, va="center", zorder=6)
        ax.text(x, y - 0.07, verdict_text(sid), fontsize=5.8, weight="bold", ha=ha, va="center",
                color=VERDICT_COLOUR[s["verdict"]], zorder=6)
        ax.text(x, y - 0.23, f"{c['REFUTED']} refuted, {c['CONJECTURE'] + c['HUNCH']} open", fontsize=5.6, ha=ha, va="center",
                color="#666666", zorder=6)

    hh = nh / 2
    # ---- left arm
    for a, b, sid in [("G", "T", "S0"), ("T", "S", "ST"), ("S", "P", "A"), ("P", "M", "C"), ("M", "N", "N"),
                      ("N", "FP", "D"), ("FP", "IT", "R")]:
        (xa, ya), (xb, yb) = pos[a], pos[b]
        seg_bundle((xa, ya - hh), (xb, yb + hh + 0.02), strands(sid))
        if detail:
            n = len(BY_STEP[sid])
            ytop = (ya + yb) / 2 + (n * RH) / 2 + 0.0
            rows(sid, -1.15 - LISTW, ytop)
        else:
            step_tag(sid, -0.85, (ya + yb) / 2, ha="right")
    # ---- bottom
    (xa, ya), (xb, yb) = pos["IT"], pos["WT"]
    seg_bundle((xa + nw / 2, ya), (xb - nw / 2 - 0.02, yb), strands("E"))
    if detail:
        rows("E", (xa + xb) / 2 - LISTW / 2, ya - 0.5)
    else:
        step_tag("E", (xa + xb) / 2, ya - 0.42, ha="center")
    # ---- right arm
    for a, b, sid in [("WT", "SE", "E2"), ("SE", "JC", "F"), ("JC", "GL", "G"), ("GL", "HC", "G2")]:
        (xa, ya), (xb, yb) = pos[a], pos[b]
        seg_bundle((xa, ya + hh), (xb, yb - hh - 0.02), strands(sid))
        if detail:
            n = len(BY_STEP[sid])
            ytop = (ya + yb) / 2 + (n * RH) / 2
            yend = rows(sid, xR + 1.3, ytop)
            if sid == "F":
                ax.text(xR + 1.3, yend - 0.12, "O and T use the disk identity here a third time; Li avoids it.",
                        fontsize=6.4, color="#666666", style="italic", ha="left", va="center")
        else:
            step_tag(sid, xR + 0.45, (ya + yb) / 2)
    # ---- side nodes: disk identity
    xs, ys = pos["S"]
    xd, yd = pos["DI"]
    seg_bundle((xs + 0.55, ys - hh), (xd - 0.35, yd + hh + 0.02), strands("B"))
    xm, ym = pos["M"]
    thin((xd - nw / 2, yd - 0.12), (xm + 0.75, ym + hh + 0.02), "used twice\n(D-cycles, Q-cycle)", tpos=0.5, dx=0.12)
    if detail:
        rows("B", xd - 0.55, yd - hh - 0.42)
    else:
        step_tag("B", xd + nw / 2 + 0.12, yd)
    # ---- K
    xk, yk = pos["K"]
    seg_bundle((xm + 0.98, ym - hh + 0.02), (xk - 0.5, yk + hh + 0.02), strands("K"))
    xf, yf = pos["FP"]
    thin((xk - nw / 2, yk - 0.1), (xf + 0.75, yf + hh + 0.02), "only forest pairs\nsurvive", tpos=0.5, dx=0.12)
    xn, yn = pos["N"]
    if detail:
        rows("K", xk - 0.55, yk - hh - 0.42)
        ax.text(xn + nw / 2 + 0.08, yn, "the sum is not zero", fontsize=6.4, color="#666666", style="italic", va="center")
    else:
        step_tag("K", xk + nw / 2 + 0.1, yk)
    # ---- bypass chord S -> FP
    xc = (8.4 if detail else 6.3)
    poly_bundle([(xs + nw / 2, ys), (xc, ys), (xc, yf), (xf + nw / 2 + 0.02, yf)], strands("U"))
    if detail:
        n = len(BY_STEP["U"])
        yu = (ys + yf) / 2 + n * RH / 2 + 1.2
        rows("U", xc + 0.45, yu)
    else:
        step_tag("U", xc - 0.4, ym + 0.1, ha="right")
    # ---- goal edge T -> 2T
    xt, yt = pos["T"]
    x2, y2 = pos["2T"]
    ax.annotate("", xy=(x2 - nw / 2 - 0.02, y2 + 0.05), xytext=(xt + nw / 2, yt),
                arrowprops=dict(arrowstyle="<|-|>", color="#999999", lw=5, alpha=0.35, mutation_scale=16), zorder=1)
    seg_bundle((xt + nw / 2, yt), (x2 - nw / 2 - 0.02, y2 + 0.05), strands("TG"), head=False)
    midx, midy = (xt + nw / 2 + x2 - nw / 2) / 2, (yt + y2) / 2
    ax.text(midx + (0.6 if detail else 0.2), midy - 0.42,
            "the goal, as an equivalence (Stein 1971). No direct proof: every route here stops or is partial." if detail else
            "the goal (Stein 1971). No direct proof:\nevery route here stops or is partial.",
            fontsize=6.6 if detail else 5.8, color="#555555", style="italic", ha="center", va="center", zorder=6)
    if detail:
        n = len(BY_STEP["TG"])
        rows("TG", 3.2, yt + 0.62 + n * RH)
    else:
        step_tag("TG", midx - 0.5, midy + 0.75, ha="center")
    # ---- JC -> 2T -> GL
    xj, yj = pos["JC"]
    xg, yg = pos["GL"]
    seg_bundle((xj - 0.7, yj + hh), (x2 + 0.3, y2 - hh - 0.02), strands("J2"))
    thin((x2 + nw / 2, y2 + 0.05), (xg - nw / 2 - 0.02, yg), "O, T glue trees", tpos=0.0, dx=0.05, dy=0.4, ha="left")
    if detail:
        rows("J2", x2 + nw / 2 - 3.6, y2 - hh - 0.5, width=3.6)
    else:
        step_tag("J2", x2 + 0.2, y2 + 0.62, ha="center")

    # ---- nodes on top
    node("G")
    node("T", "rooted at a black face t0, edge e0")
    node("S", "perfect matchings of B")
    node("P", "two states, different at every face")
    node("DI", "2l - h = -3; one more white face than black")
    node("M", "a sign that both reversals flip")
    node("K", "sum with s fixed")
    node("N", "sum with D fixed")
    node("FP", "Q_s a forest; exactly one partner")
    node("IT", "spanning tree of the spoke graph")
    node("WT", "duals of the deleted spokes")
    node("SE", "one side of every face of T")
    node("JC", "E(G) - P is one cycle")
    node("2T", "the goal in dual form", goal=True)
    node("GL", "cut at separating triangles")
    node("HC", "avoiding any prescribed edge", goal=True)

    # ---- title, legend
    tx = xmin + 0.25
    ax.text(tx, ymax - 0.3, "Route map of the proof of Barnette's conjecture", fontsize=15 if detail else 11, weight="bold", va="center")
    ax.text(tx, ymax - 0.62,
            "Boxes are waypoints. Each strand between two boxes is one argument. The proof goes down the left, across the bottom and up the right."
            if detail else "Boxes are waypoints, strands are arguments. Down the left, across, up the right.",
            fontsize=8 if detail else 6.4, color="#333333", va="center")
    if detail:
        ax.text(tx, ymax - 0.84,
                "One black strand per distinct published argument: a single black strand means all three papers walk the same corridor. "
                "Built by digestions/route-map/build_map.py from routes.py, 2026-11-14.",
                fontsize=7, color="#555555", va="center")
    # legend
    if detail:
        lx, ly = 3.2, yn + 1.75
    else:
        lx, ly = xmin + 0.4, pos["IT"][1] - 0.8
    items = [("LIT", "published (2026 papers: unrefereed preprints)"), ("PROVED-HERE", "proved in this project (AI-refereed at best)"),
             ("COMPUTED", "computed check"), ("CONJECTURE", "conjecture with a stated test"), ("HUNCH", "hunch"),
             ("REFUTED", "refuted (kept, with its lesson)"), ("PARTIAL", "published, partial (stops short)")]
    lw_ = 3.7 if detail else 2.9
    lh = (len(items) + (3 if detail else 0)) * 0.2 + 0.45
    ax.add_patch(FancyBboxPatch((lx - 0.15, ly - lh), lw_, lh + 0.1, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc="white", ec="#999999", lw=0.8, zorder=5))
    ax.text(lx, ly - 0.12, "Legend", fontsize=8 if detail else 7, weight="bold", va="center", zorder=6)
    yy = ly - 0.38
    for kind, text in items:
        col, ls, lw = STYLE[kind]
        frac = 0.3 if kind not in ("REFUTED", "PARTIAL") else 0.2
        ax.plot([lx, lx + 0.5 * frac / 0.3], [yy, yy], color=col, ls=ls, lw=lw, zorder=6)
        if kind == "REFUTED":
            ax.plot([lx + 0.5 * frac / 0.3], [yy], marker="x", color=col, ms=4, mew=1.1, zorder=6)
        ax.text(lx + 0.62, yy, text, fontsize=6.8 if detail else 6.0, va="center", zorder=6)
        yy -= 0.2
    if detail:
        ax.plot([lx + 0.25], [yy], marker="o", color="#1f5fbf", ms=2.8, zorder=6)
        ax.text(lx + 0.62, yy, "a fact about the step (listed, not a strand)", fontsize=6.8, va="center", zorder=6)
        yy -= 0.2
        ax.text(lx + 0.25, yy, "≡", fontsize=8.5, color="#1f5fbf", ha="center", va="center", zorder=6)
        ax.text(lx + 0.62, yy, "an exact reformulation of the target", fontsize=6.8, va="center", zorder=6)
        yy -= 0.2
        ax.text(lx, yy, "Sources: O OpenAI, L Li, T trees paper, Lean formal proof, lit older literature;", fontsize=6.2, va="center", color="#555555", zorder=6)
        ax.text(lx, yy - 0.16, "dep, comb, dim, con, mach, alg, lim, hist, gt, topo, refc, refd: folders under research/", fontsize=6.2, va="center",
                color="#555555", zorder=6)

    for ext in ("pdf", "svg", "png"):
        fig.savefig(HERE / f"{stem}.{ext}", dpi=150 if detail else 170)
    plt.close(fig)


# ---------------------------------------------------------------- exports
def export_json():
    out = {"folders": RT.FOLDERS, "waypoints": RT.WAYPOINTS, "steps": RT.STEPS,
           "routes": [{**r, "role": role(r)} for r in RT.ROUTES]}
    (HERE / "routes.json").write_text(json.dumps(out, indent=1), encoding="utf-8")


def export_dot():
    L = ["// Generated by build_map.py from routes.py. One edge per route.", "digraph routemap {",
         '  rankdir=TB; node [shape=box, style="rounded,filled", fillcolor="#f2f4f7", fontname="Helvetica"];']
    for w in RT.WAYPOINTS:
        L.append(f'  "{w["id"]}" [label="{w["name"]}"];')
    dotstyle = {"LIT": 'color="black"', "PROVED-HERE": 'color="#1f5fbf"', "COMPUTED": 'color="#1b8a5a", style=dashed',
                "CONJECTURE": 'color="#c77700", style=dotted', "HUNCH": 'color="#b9a26a", style=dotted',
                "REFUTED": 'color="#c62828", style=dashed, arrowhead=tee'}
    for r in RT.ROUTES:
        s = STEP[r["step"]]
        frm = s["frm"][-1] if r["step"] in ("B",) else s["frm"][0]
        label = f'{r["id"]} {r["label"]}'.replace('"', "'")
        L.append(f'  "{frm}" -> "{s["to"]}" [label="{label}", {dotstyle[r["status"]]}, status="{r["status"]}", '
                 f'role="{role(r)}", src="{r["src"]}"];')
    for s in RT.STEPS:
        for extra in s["frm"][1:] if s["id"] != "B" else s["frm"][:-1]:
            L.append(f'  "{extra}" -> "{s["to"]}" [color="gray", label="{s["id"]} (input)"];')
    L.append("}")
    (HERE / "route-map.dot").write_text("\n".join(L) + "\n", encoding="utf-8")


def md_escape(s):
    return s.replace("|", "\\|")


def export_md():
    c_all = Counter(r["status"] for r in RT.ROUTES)
    intro = (HERE / "ROUTE-MAP.head.md").read_text(encoding="utf-8")
    for key, val in {"{N}": len(RT.ROUTES), "{LIT}": c_all["LIT"], "{PH}": c_all["PROVED-HERE"], "{CO}": c_all["COMPUTED"],
                     "{CJ}": c_all["CONJECTURE"], "{HU}": c_all["HUNCH"], "{RE}": c_all["REFUTED"]}.items():
        intro = intro.replace(key, str(val))
    tail = (HERE / "ROUTE-MAP.tail.md").read_text(encoding="utf-8")
    L = [intro.rstrip(), ""]
    L += ["## Counts", "",
          f"{len(RT.WAYPOINTS)} waypoints, {len(RT.STEPS)} steps, {len(RT.ROUTES)} routes: "
          + ", ".join(f"{c_all[s]} `{s}`" for s in RT.STATUS_ORDER) + ".", "",
          "| Step | From | To | Verdict | Published arguments | `LIT` | `PROVED-HERE` | `COMPUTED` | `CONJECTURE` | `HUNCH` | `REFUTED` |",
          "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for s in RT.STEPS:
        c = Counter(r["status"] for r in BY_STEP[s["id"]])
        L.append(f"| {s['id']} {s['title']} | {', '.join(s['frm'])} | {s['to']} | {s['verdict']} | {n_published_args(s['id'])} | "
                 + " | ".join(str(c[x]) for x in RT.STATUS_ORDER) + " |")
    L += ["", "## Waypoints", "", "| Id | Waypoint | What it is |", "| --- | --- | --- |"]
    for w in RT.WAYPOINTS:
        L.append(f"| {w['id']} | {w['name']} | {md_escape(w['what'])} |")
    L += ["", "## Steps and routes", "",
          "For every step: what must be shown, how much freedom the known proofs have, then every route. "
          "A route marked *fact* or *reformulation* is listed with the step it belongs to and is not drawn as a strand.", ""]
    for s in RT.STEPS:
        L += [f"### {s['id']}. {s['title']} ({' + '.join(s['frm'])} to {s['to']})", "",
              f"What must be shown. {s['must']}", "", f"Freedom. {s['freedom']}", "",
              "| Id | Route | Status | Source | Statement |", "| --- | --- | --- | --- | --- |"]
        notes = []
        for r in sorted_routes(s["id"]):
            ro = role(r)
            tag = {"fact": " (fact)", "equiv": " (reformulation)", "partial": " (partial)"}.get(ro, "")
            rev = ""
            if r["status"] == "PROVED-HERE":
                states = {RT.REVIEW.get(f.strip(), {}).get("state", "unreviewed") for f in r["src"].split(",")}
                rev = ", " + ("AI-refereed" if states == {"refereed"} else "partly AI-refereed" if "refereed" in states else "under review" if "under-review" in states else "unreviewed")
            L.append(f"| {r['id']} | {md_escape(r['label'])}{tag} | `{r['status']}`{rev} | {md_escape(r['where'])} | {md_escape(r['text'])} |")
            if r["status"] == "REFUTED":
                notes.append(f"- **{r['id']}, refuted.** Lesson: {r['lesson']} Smallest known counterexample: {r['cex']}")
            elif r["status"] in ("CONJECTURE", "HUNCH"):
                extra = f" {r['vivid']}" if r.get("vivid") else ""
                notes.append(f"- **{r['id']}, {r['status'].lower()}.**{extra} Test: {r['test']}")
        L += [""] + notes + [""]
    L += [tail.rstrip(), ""]
    (HERE / "ROUTE-MAP.md").write_text("\n".join(L), encoding="utf-8")


def sanity():
    ids = [r["id"] for r in RT.ROUTES]
    assert len(ids) == len(set(ids)), [i for i, c in Counter(ids).items() if c > 1]
    for r in RT.ROUTES:
        assert r["step"] in STEP, r["id"]
        assert r["status"] in RT.STATUS_ORDER, r["id"]
        if r["status"] == "REFUTED":
            assert r.get("lesson") and r.get("cex"), r["id"]
        if r["status"] in ("CONJECTURE", "HUNCH"):
            assert r.get("test"), r["id"]
        for f in r["src"].split(","):
            assert f.strip() in RT.FOLDERS or f.strip() in ("O", "L", "T", "lit", "Lean"), (r["id"], f)
    for s in RT.STEPS:
        assert all(f in WP for f in s["frm"]) and s["to"] in WP, s["id"]
        assert BY_STEP[s["id"]], s["id"]
    assert (FACT_IDS | EQUIV_IDS) <= set(ids), (FACT_IDS | EQUIV_IDS) - set(ids)


if __name__ == "__main__":
    sanity()
    export_json()
    export_dot()
    draw(True, "route-map")
    draw(False, "route-map-overview")
    if (HERE / "ROUTE-MAP.head.md").exists():
        export_md()
    c = Counter(r["status"] for r in RT.ROUTES)
    print(len(RT.WAYPOINTS), "waypoints,", len(RT.STEPS), "steps,", len(RT.ROUTES), "routes:", dict(c))
