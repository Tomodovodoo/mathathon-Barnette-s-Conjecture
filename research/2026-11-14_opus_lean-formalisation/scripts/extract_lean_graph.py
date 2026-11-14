"""Extract a declaration-level dependency graph from the OpenAI Barnette Lean files.

Usage (from the repository root):
    python -I research/2026-11-14_opus_lean-formalisation/scripts/extract_lean_graph.py \
        research/2026-11-14_opus_lean-formalisation/upstream/openai-math/lean/OAI/Combinatorics/Hamiltonian \
        research/2026-11-14_opus_lean-formalisation/graph

Approximations (also stated in LEAN-STRUCTURE.md):
  * A declaration starts at a line, at column 0, that begins (after optional
    attributes and modifiers) with theorem/lemma/def/structure/abbrev/instance/
    inductive/class. Its text runs to the next declaration start or to a
    namespace/section/end/variable line at column 0.
  * Names are qualified by the open `namespace` stack only (sections ignored).
  * A dependency edge X -> Y is recorded when an identifier token in X's text
    resolves to project declaration Y.  Resolution: a token a.b.c is matched
    against full names that end with a.b.c, then b.c, then c (dot notation such as
    `h.hamiltonian` therefore resolves through its last component).  If the last
    component alone is used and several declarations share it, an edge is added to
    every candidate that is earlier in the import order and the edge is marked
    ambiguous.  Structure fields resolve to their structure.
  * Mathlib declarations are not nodes.  Local hypothesis names that happen to equal
    a project declaration's last component can create spurious edges; we suppress
    tokens starting with `h` followed by an uppercase letter, digit or nothing
    else meaningful, and single-letter tokens.
"""
import json
import re
import sys
from pathlib import Path

ORDER = """Model Network CutSpaces FlowCircuits Bonds Quotients DiskRegions StateDisk
Circulation TriangleSystem ColoredDual CycleReversal PairPhases PairPolynomials Forest
Contraction MinorDuality BMatching Matching ForestMatching ThreeCuts CappedDuality
Gluing Traces SquareGrid Corridors MinorModel BranchPartition Rectangle ExactDual
Main""".split()

KW = r"(theorem|lemma|def|structure|abbrev|instance|inductive|class)"
DECL_RE = re.compile(
    r"^(?:@\[[^\]]*\]\s*)*(?:(?:private|protected|noncomputable|nonrec|unsafe|partial)\s+)*"
    + KW + r"\s+([^\s:({\[⦃]+)?")
NS_RE = re.compile(r"^namespace\s+(\S+)")
END_RE = re.compile(r"^end(?:\s+(\S+))?\s*$")
SEC_RE = re.compile(r"^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$")
BOUNDARY_RE = re.compile(r"^(namespace|end|section|noncomputable section|variable|open|omit|include|local|attribute|universe|/-!|#)")
IDENT_RE = re.compile(r"[A-Za-z_α-ωΑ-Ω][A-Za-z0-9_'α-ωΑ-Ω!?₀-₉]*(?:\.[A-Za-z_][A-Za-z0-9_'!?₀-₉]*)*")
FIELD_RE = re.compile(r"^  ([a-z_][A-Za-z0-9_']*)\s*:")


def strip_comments(text):
    text = re.sub(r"/-.*?-/", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    return re.sub(r"--[^\n]*", "", text)


def parse_file(path, module):
    raw = path.read_text(encoding="utf-8").splitlines()
    clean = strip_comments("\n".join(raw)).splitlines()
    stack = []  # entries: ("ns", name) or ("sec", name)
    decls = []
    cur = None

    def close():
        nonlocal cur
        if cur is not None:
            body = clean[cur["start"]:cur["stop"]]
            while body and not body[-1].strip():
                body.pop()
            cur["lines"] = len([l for l in body if l.strip()])
            cur["end_line"] = cur["start"] + len(body)
            cur["text"] = "\n".join(body)
            decls.append(cur)
            cur = None

    doc = None
    for i, line in enumerate(raw):
        cl = clean[i]
        if line.startswith("/--"):
            doc = line.strip("/- ").strip()
        m = DECL_RE.match(cl)
        if m and not cl.startswith(" "):
            if cur is not None:
                cur["stop"] = i
                close()
            kind, name = m.group(1), m.group(2) or "(anon)"
            ns = ".".join(n for k, n in stack if k == "ns")
            full = (ns + "." + name) if ns and not name.startswith("_root_") else name
            cur = {"name": full, "short": name, "kind": kind, "module": module,
                   "file": path.name, "start": i, "stop": len(raw), "doc": doc,
                   "private": cl.lstrip().startswith("private") or "private " in cl.split(kind)[0],
                   "fields": []}
            doc = None
            continue
        if cur is not None and cur["kind"] in ("structure", "class") and FIELD_RE.match(cl):
            cur["fields"].append(FIELD_RE.match(cl).group(1))
        if cl and not cl.startswith(" ") and BOUNDARY_RE.match(cl):
            if cur is not None:
                cur["stop"] = i
                close()
            mm = NS_RE.match(cl)
            if mm:
                for part in mm.group(1).split("."):
                    stack.append(("ns", part))
            elif SEC_RE.match(cl.strip()):
                stack.append(("sec", SEC_RE.match(cl.strip()).group(1) or ""))
            else:
                me = END_RE.match(cl.strip())
                if me:
                    nm = me.group(1)
                    if nm:
                        parts = nm.split(".")
                        for _ in parts:
                            if stack:
                                stack.pop()
                    elif stack:
                        stack.pop()
        if line.startswith("/--") is False and not line.startswith(" ") and line.strip() and not line.startswith("/--"):
            if not DECL_RE.match(cl):
                pass
    if cur is not None:
        cur["stop"] = len(raw)
        close()
    for d in decls:
        d["start_line"] = d["start"] + 1
        del d["start"], d["stop"]
    return decls


def main():
    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    all_decls = []
    file_lines = {}
    for idx, mod in enumerate(ORDER):
        p = src / f"{mod}.lean"
        file_lines[mod] = len(p.read_text(encoding="utf-8").splitlines())
        for d in parse_file(p, mod):
            d["order"] = idx
            all_decls.append(d)
    by_full = {}
    for d in all_decls:
        by_full.setdefault(d["name"], []).append(d)
    # name index by suffix
    def suffixes(full):
        parts = full.split(".")
        return [".".join(parts[k:]) for k in range(len(parts))]
    suffix_index = {}
    for d in all_decls:
        for s in suffixes(d["name"]):
            suffix_index.setdefault(s, set()).add(d["name"])
        for f in d["fields"]:
            for s in suffixes(d["name"] + "." + f):
                suffix_index.setdefault(s, set()).add(d["name"])
    order_of = {d["name"]: (d["order"], d["start_line"]) for d in all_decls}
    edges = {}
    for d in all_decls:
        body = d["text"]
        # drop the declaration's own name token
        toks = set(IDENT_RE.findall(body))
        deps = {}
        for t in toks:
            if len(t) <= 1:
                continue
            parts = t.split(".")
            found = None
            amb = False
            for k in range(len(parts)):
                s = ".".join(parts[k:])
                if re.fullmatch(r"h[A-Z0-9]?\w{0,3}|h", s):
                    break
                cands = suffix_index.get(s)
                if cands:
                    found = cands
                    amb = (k == len(parts) - 1 and len(cands) > 1)
                    break
            if not found:
                continue
            for c in found:
                if c == d["name"]:
                    continue
                if order_of[c] >= order_of[d["name"]]:
                    continue  # Lean forbids forward references
                deps[c] = deps.get(c, True) and amb
        edges[d["name"]] = deps
    nodes = []
    for d in all_decls:
        nodes.append({k: d[k] for k in ("name", "kind", "module", "file", "start_line",
                                         "end_line", "lines", "doc", "private")}
                     | {"uses": sorted(edges[d["name"]]),
                        "ambiguous_uses": sorted(c for c, a in edges[d["name"]].items() if a)})
    used_by = {}
    for n in nodes:
        for u in n["uses"]:
            used_by.setdefault(u, []).append(n["name"])
    for n in nodes:
        n["used_by"] = sorted(used_by.get(n["name"], []))
    # reachability from the main theorem
    idx = {n["name"]: n for n in nodes}
    root = "OAI.Barnette.main"
    seen, todo = set(), [root]
    while todo:
        x = todo.pop()
        if x in seen or x not in idx:
            continue
        seen.add(x)
        todo.extend(idx[x]["uses"])
    for n in nodes:
        n["reachable_from_main"] = n["name"] in seen
    data = {"source": str(src), "file_order": ORDER, "file_lines": file_lines,
            "nodes": nodes}
    (out / "lean-decls.json").write_text(json.dumps(data, indent=1, ensure_ascii=False),
                                         encoding="utf-8")
    # DOT: declaration graph (reachable part), clustered by file
    def q(s):
        return '"' + s.replace('"', '\\"') + '"'
    lines = ["digraph lean {", "  rankdir=BT; node [shape=box,fontsize=8]; edge [arrowsize=0.4];"]
    for mod in ORDER:
        lines.append(f"  subgraph cluster_{mod} {{ label={q(mod)}; fontsize=10;")
        for n in nodes:
            if n["module"] == mod and n["reachable_from_main"]:
                short = n["name"].replace("OAI.Barnette.", "")
                lines.append(f"    {q(n['name'])} [label={q(short + chr(10) + str(n['lines']))}];")
        lines.append("  }")
    for n in nodes:
        if not n["reachable_from_main"]:
            continue
        for u in n["uses"]:
            style = " [style=dashed]" if u in n["ambiguous_uses"] else ""
            lines.append(f"  {q(n['name'])} -> {q(u)}{style};")
    lines.append("}")
    (out / "lean-decls.dot").write_text("\n".join(lines), encoding="utf-8")
    # DOT: file-level graph weighted by declaration edges
    fe = {}
    for n in nodes:
        for u in n["uses"]:
            a, b = n["module"], idx[u]["module"]
            if a != b:
                fe[(a, b)] = fe.get((a, b), 0) + 1
    fl = ["digraph files {", "  rankdir=BT; node [shape=box,fontsize=10];"]
    for mod in ORDER:
        fl.append(f"  {q(mod)} [label={q(mod + chr(10) + str(file_lines[mod]) + ' lines')}];")
    for (a, b), w in sorted(fe.items()):
        fl.append(f"  {q(a)} -> {q(b)} [label={w},fontsize=7,penwidth={min(4, 0.5 + w / 4):.2f}];")
    fl.append("}")
    (out / "lean-files.dot").write_text("\n".join(fl), encoding="utf-8")
    print(len(nodes), "declarations;", sum(len(n["uses"]) for n in nodes), "edges;",
          len(seen), "reachable from main")


if __name__ == "__main__":
    main()
