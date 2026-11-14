"""Exact one-match substitutions on a file. Usage: python sub.py FILE SPEC

SPEC is a UTF-8 text file of blocks "old\n===\nnew" separated by lines "%%%".
Stops without writing if an old string does not occur exactly once.
"""
import io, sys
path, spec = sys.argv[1], io.open(sys.argv[2], encoding="utf-8").read()
t = io.open(path, encoding="utf-8", newline="").read()
n = 0
for block in spec.split("\n%%%\n"):
    if not block.strip():
        continue
    old, new = block.split("\n===\n")
    old, new = old.strip("\n"), new.strip("\n")
    if t.count(old) != 1:
        sys.exit(f"{t.count(old)} matches for: {old[:90]!r}")
    t = t.replace(old, new)
    n += 1
io.open(path, "w", encoding="utf-8", newline="").write(t)
print("applied", n)
