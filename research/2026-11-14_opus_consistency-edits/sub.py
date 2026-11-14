"""Exact one-occurrence substitutions: python sub.py FILE <<< 'old\n===\nnew\n%%%\nold2\n===\nnew2'"""
import sys
path = sys.argv[1]
spec = sys.stdin.read()
t = open(path, encoding="utf-8", newline="").read()
for block in spec.split("\n%%%\n"):
    if not block.strip(): continue
    old, new = block.split("\n===\n")
    old = old.strip("\n"); new = new.strip("\n")
    if "\r\n" in t:
        old = old.replace("\n", "\r\n"); new = new.replace("\n", "\r\n")
    n = t.count(old)
    if n != 1:
        sys.exit(f"{path}: {n} matches for: {old[:80]!r}")
    t = t.replace(old, new)
open(path, "w", encoding="utf-8", newline="").write(t)
print("ok", path)
