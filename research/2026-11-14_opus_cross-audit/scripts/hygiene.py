"""Survey the repository for build artefacts, duplicates, large files, missing
reports and broken relative links.  Read-only.  Run from the repository root:

    python research/2026-11-14_opus_cross-audit/scripts/hygiene.py > research/2026-11-14_opus_cross-audit/data/hygiene.json
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

ROOT = Path.cwd()
BUILD = re.compile(r"(\.aux|\.log|\.out|\.fls|\.fdb_latexmk|\.synctex\.gz|\.pyc|\.toc|\.bbl|\.blg|\.nav|\.snm)$|(^|/)__pycache__/")
LAYOUT = {"papers", "digestions", "workings", "proofs", "paper", "skills"}


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf8").stdout


def main():
    tracked = [p for p in git("ls-files", "-z").split("\0") if p]
    info = {}
    for p in tracked:
        fp = ROOT / p
        if fp.is_file():
            info[p] = fp.stat().st_size
    out = {}
    out["tracked_files"] = len(tracked)
    out["tracked_bytes"] = sum(info.values())
    out["tracked_build_artefacts"] = sorted(p for p in tracked if BUILD.search(p))
    out["large_files_over_1MB"] = sorted(([p, s] for p, s in info.items() if s > 1_000_000), key=lambda x: -x[1])
    out["empty_files"] = sorted(p for p, s in info.items() if s == 0)
    # duplicates by sha256 among binary-ish files
    by_hash = defaultdict(list)
    for p, s in info.items():
        if s == 0:
            continue
        if not p.lower().endswith((".pdf", ".png", ".jpg", ".svg", ".json", ".txt", ".tex", ".py", ".md")):
            continue
        h = hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
        by_hash[h].append(p)
    dups = [[h[:12], info[v[0]], sorted(v)] for h, v in by_hash.items() if len(v) > 1]
    dups.sort(key=lambda x: -x[1] * (len(x[2]) - 1))
    out["duplicate_groups"] = dups
    out["duplicate_bytes_wasted"] = sum(d[1] * (len(d[2]) - 1) for d in dups)
    out["vendored_or_upstream"] = sorted(p for p in tracked if re.search(r"(^|/)(upstream|vendor|node_modules|\.lake|site-packages)/", p))
    tops = sorted({p.split("/")[0] for p in tracked})
    out["top_level_entries"] = tops
    out["outside_readme_layout"] = [t for t in tops if t not in LAYOUT and "/" not in t and not (ROOT / t).is_file()]
    # research reports
    rdirs = sorted(d.name for d in (ROOT / "research").iterdir() if d.is_dir())
    out["research_folders"] = len(rdirs)
    out["research_without_REPORT"] = [d for d in rdirs if not (ROOT / "research" / d / "REPORT.md").exists()]
    out["research_REPORT_untracked"] = [d for d in rdirs if (ROOT / "research" / d / "REPORT.md").exists()
                                        and f"research/{d}/REPORT.md" not in info]
    # untracked and ignored, summarised by top folder
    untracked = [l[3:] for l in git("status", "--porcelain", "--untracked-files=all").splitlines() if l.startswith("??")]
    ignored = [l[3:] for l in git("status", "--porcelain", "--ignored", "--untracked-files=normal").splitlines() if l.startswith("!!")]
    out["untracked_count"] = len(untracked)
    out["untracked_build_artefacts"] = sorted(p for p in untracked if BUILD.search(p))
    out["ignored_entries"] = sorted(ignored)
    # links
    md_files = [p for p in tracked if p.endswith(".md") and (p.startswith("digestions/") or Path(p).name.upper().startswith("README"))]
    link_re = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
    broken = []
    nlinks = 0
    for p in md_files:
        text = (ROOT / p).read_text(encoding="utf8", errors="replace")
        # skip fenced code
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        for m in link_re.finditer(text):
            target = m.group(1)
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            nlinks += 1
            path = unquote(target.split("#")[0])
            if not path:
                continue
            resolved = (ROOT / p).parent / path
            if not resolved.exists():
                # suggest a fix: same basename anywhere in the tree
                base = Path(path).name
                cands = [t for t in tracked if Path(t).name == base]
                rel = [os.path.relpath(ROOT / c, (ROOT / p).parent).replace("\\", "/") for c in cands[:3]]
                broken.append({"file": p, "target": target, "candidates": rel})
    out["markdown_files_checked"] = len(md_files)
    out["relative_links_checked"] = nlinks
    out["broken_links"] = broken
    json.dump(out, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
