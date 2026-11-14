"""Check that file paths named in the `where` fields of digestions/route-map/routes.py exist.

Usage (from the repository root): python -X utf8 -B research/2026-11-14_opus_consistency-edits/wherecheck.py
Folder tags (rc/, covers/, ...) are expanded with routes.FOLDERS. Only tokens that look like a path
with a file extension or a trailing slash are checked; section references after the path are ignored.
"""
import re, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "digestions/route-map"))
import routes as RT

TOP = ("research/", "paper/", "proofs/", "papers/", "digestions/", "labyrinth/", "workings/", "toolkit/")
bad = n = 0
for r in RT.R:
    last = ""  # an untagged relative path continues the previous folder ("lim/A.md; examples/B.json")
    for part in re.split(r"[;,]", r.get("where", "")):
        tok = part.strip().lstrip("+").strip().split(" ")[0]
        if not tok or "/" not in tok or tok.startswith("http"):
            continue
        tag, _, rest = tok.partition("/")
        if tag in RT.FOLDERS:
            path = RT.FOLDERS[tag] + "/" + rest; last = RT.FOLDERS[tag]
        elif tok.startswith(TOP) or not last:
            path = tok
        else:
            path = last + "/" + tok
        if not (re.search(r"\.\w+$", path) or path.endswith("/")):
            continue
        if any(c in path for c in "*{}"):
            continue
        n += 1
        if not (REPO / path).exists() and not (REPO / (path + ".gz")).exists():
            bad += 1
            print(f"{r['id']}: {tok} -> {path}")
print(f"checked {n} where-paths, {bad} missing")
