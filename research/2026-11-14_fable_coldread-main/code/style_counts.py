"""Count style tells in paper/main/barnette.tex.

Run from the repository root:
    python research/2026-11-14_fable_coldread-main/code/style_counts.py
Writes nothing; prints counts and line numbers used in EXPOSITION-REVIEW.md section (g).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TEX = ROOT / "paper" / "main" / "barnette.tex"
s = TEX.read_text(encoding="utf-8")
lines = s.split("\n")
start = s.index(r"\begin{abstract}")
end = s.index(r"\bibliographystyle")
body = s[start:end]

print("semicolons in body:", body.count(";"))
print("'exactly':", len(re.findall(r"\bexactly\b", body)))
print("'separating triangle' occurrences:", body.count("separating triangle"))

pats = [
    r"Here is", r"In words", r"that is,", r"namely", r"[Ii]n particular", r"Thus", r"Hence",
    r"We claim", r"once and for all", r"the whole", r"completely", r"\(proved", r"computed",
    r"we have not checked", r"used four times", r"which is why", r"Throughout",
    r"shows", r"---", r"Conversely", r"read off", r"so that",
]
for p in pats:
    print(f"{p!r}: {len(re.findall(p, body))}")

print("\nlines with 45 or more words (one sentence per source line):")
for i, l in enumerate(lines, 1):
    if l.startswith("\\caption") or l.startswith("%"):
        continue
    w = len(l.split())
    if w >= 45:
        print(f"  l.{i} ({w} words): {l[:100]}")

print("\ncolon followed by lower case or math (connector use), outside captions:")
n = 0
for i, l in enumerate(lines, 1):
    if l.startswith("\\caption"):
        continue
    for m in re.finditer(r"[a-z\$\)\}]: [a-z\$\\]", l):
        n += 1
        print(f"  l.{i}: ...{l[max(0, m.start() - 45):m.start() + 45]}...")
print("count:", n)

print("\nparenthetical asides of 4 or more words in prose lines:")
n = 0
for i, l in enumerate(lines, 1):
    if l.startswith("\\caption") or "includegraphics" in l or l.startswith("\\node") or l.startswith("\\draw"):
        continue
    for m in re.finditer(r"\(([^()$\\]{20,})\)", l):
        n += 1
        print(f"  l.{i}: ({m.group(1)[:70]})")
print("count:", n)
sys.exit(0)
