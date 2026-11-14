"""Print each declaration's statement (text up to ':= by' / ':=' / 'where'), with docstring.
Usage: python -I statements.py graph/lean-decls.json SRC_DIR [Module ...]"""
import json, sys, re
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
d = json.load(open(sys.argv[1], encoding="utf-8"))
src = Path(sys.argv[2]); mods = set(sys.argv[3:])
cache = {}
for n in d["nodes"]:
    if mods and n["module"] not in mods: continue
    lines = cache.setdefault(n["file"], (src / n["file"]).read_text(encoding="utf-8").splitlines())
    s = n["start_line"] - 1
    out = []
    for l in lines[s:n["end_line"]]:
        out.append(l)
        if re.search(r":=\s*by\b|:=\s*$|\bwhere\s*$|:=\s*\S", l) and n["kind"] not in ("structure",):
            break
    if n["kind"] in ("structure","def","abbrev") and n["lines"] <= 15:
        out = lines[s:n["end_line"]]
    print(f"--- {n['module']}:{n['start_line']} [{n['lines']}]" + (f" /-- {n['doc']}" if n['doc'] else ""))
    print("\n".join(out))
