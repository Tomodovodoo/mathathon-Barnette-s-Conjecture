"""Check relative links in Markdown files.

Usage (from the repository root):
    python -X utf8 research/2026-11-14_opus_consistency-edits/linkcheck.py [ROOT_OR_FILE ...]

Default targets: every .md under digestions/, the top-level README.md, labyrinth/README.md,
workings/barnette_lab/README.md and the README.md files under digestions/.
Checks Markdown links [text](target) and images ![alt](target), plus backticked repository
paths that start with research/, paper/, proofs/, papers/, digestions/, labyrinth/ or workings/
(resolved from the repository root). External URLs and pure #anchors are skipped. For links
with a #anchor to a Markdown file, the heading anchor is checked too (GitHub slug rules).
Prints one line per broken link and a summary; exits 1 if anything is broken.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
TICK = re.compile(r"`((?:research|paper|proofs|papers|digestions|labyrinth|workings)/[^`\s]*)`")
CODE = re.compile(r"```.*?```", re.S)


def slug(h):
    h = h.strip().lower()
    h = re.sub(r"[^\w\- ]", "", h)
    return h.replace(" ", "-")


def anchors(md):
    text = CODE.sub("", md.read_text(encoding="utf-8", errors="replace"))
    return {slug(m.group(1)) for m in re.finditer(r"^#+\s+(.*)$", text, re.M)}


def targets(args):
    if args:
        for a in args:
            p = REPO / a
            yield from (sorted(p.rglob("*.md")) if p.is_dir() else [p])
        return
    yield from sorted((REPO / "digestions").rglob("*.md"))
    for f in ("README.md", "labyrinth/README.md", "workings/barnette_lab/README.md"):
        if (REPO / f).exists():
            yield REPO / f


def check(md):
    bad, n = [], 0
    text = CODE.sub("", md.read_text(encoding="utf-8", errors="replace"))
    for lineno, line in enumerate(text.splitlines(), 1):
        for m in LINK.finditer(line):
            t = m.group(1)
            if re.match(r"^[a-z]+:", t) or t.startswith("#"):
                continue
            n += 1
            path, _, frag = t.partition("#")
            dest = (md.parent / path).resolve()
            if not dest.exists():
                bad.append((lineno, t, "missing"))
            elif frag and dest.suffix == ".md" and slug(frag) not in anchors(dest):
                bad.append((lineno, t, "no such heading"))
        for m in TICK.finditer(line):
            t = m.group(1).rstrip(".,;:)")
            if any(c in t for c in "*{}<>|"):
                continue
            n += 1
            if not (REPO / t.split("#")[0]).exists():
                bad.append((lineno, t, "missing (backticked path)"))
    return n, bad


def main():
    total, broken = 0, 0
    for md in targets(sys.argv[1:]):
        n, bad = check(md)
        total += n
        for lineno, t, why in bad:
            broken += 1
            print(f"{md.relative_to(REPO).as_posix()}:{lineno}: {t}  [{why}]")
    print(f"checked {total} links, {broken} broken")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
