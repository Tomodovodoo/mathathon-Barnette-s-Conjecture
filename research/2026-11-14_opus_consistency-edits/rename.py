"""One-shot term rename to the project convention (CONSISTENCY.md section 4).

Usage: python -X utf8 rename.py FILE...   (run once from the repository root)
Lines of labyrinth/seed.py that call ev(...) are historical events and are skipped.
Prints the number of replacements per file and rule.
"""
import re, sys

RULES = [
    (r"\bTree matchings\b", "Good states"), (r"\btree matchings\b", "good states"),
    (r"\bTree matching\b", "Good state"), (r"\btree matching\b", "good state"),
    (r"\bForest pairs\b", "Good pairs"), (r"\bforest pairs\b", "good pairs"),
    (r"\bForest pair\b", "Good pair"), (r"\bforest[- ]pair\b", "good pair"),
    (r"\bTree pairs\b", "Good pairs"), (r"\btree pairs\b", "good pairs"),
    (r"\bTree pair\b", "Good pair"), (r"\btree pair\b", "good pair"),
    (r"\bforest states\b", "good states"), (r"\bforest state\b", "good state"),
    (r"\b2 (?:c_min|cmin)\b", "2m"),
    (re.escape("$c_{\min}$"), "$m$"), (re.escape("c_{\min}"), "m"),
    (r"\bc_min\b", "m"), (r"\bcmin\b", "m"),
]

def fix(text, skip_ev):
    counts = {}
    out = []
    for line in text.splitlines(keepends=True):
        if skip_ev and line.lstrip().startswith("ev("):
            out.append(line); continue
        for pat, rep in RULES:
            line, k = re.subn(pat, lambda _m, r=rep: r, line)
            if k: counts[pat] = counts.get(pat, 0) + k
        out.append(line)
    return "".join(out), counts

for path in sys.argv[1:]:
    with open(path, encoding="utf-8", newline="") as f: text = f.read()
    new, counts = fix(text, path.endswith("seed.py"))
    if new != text:
        with open(path, "w", encoding="utf-8", newline="") as f: f.write(new)
    print(path, sum(counts.values()), counts)
