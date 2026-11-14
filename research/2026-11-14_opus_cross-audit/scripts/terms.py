"""Count how often each named object appears in each project document, and print
the first defining line for selected terms.  Run from the repository root:

    python research/2026-11-14_opus_cross-audit/scripts/terms.py > research/2026-11-14_opus_cross-audit/data/terms.txt
"""
import re
from glob import glob
from pathlib import Path

DOCS = {
    "main": "paper/main/barnette.tex",
    "v1": "paper/main/history/barnette-v1.tex",
    "invol.tex": "proofs/involutions/involutions.tex",
    "INVOL.md": "proofs/involutions/INVOLUTIONS.md",
    "primal": "proofs/primal/PRIMAL-PROOF.md",
    "steps": "digestions/steps/*.md",
    "HOW": "digestions/route-map/HOW-IT-WORKS.md",
}
TERMS = {
    "good state": r"good state",
    "tree matching": r"tree matching",
    "forest pair": r"forest pair",
    "tree pair": r"tree pair",
    "forest state": r"forest state",
    "cycle cover": r"cycle cover",
    "cover": r"\bcovers?\b",
    "2-factor": r"2-factor",
    "height": r"\bheights?\b",
    "c_min": r"c_\{?\\min|c_min|cmin|c_\{\\rm min",
    "J": r"\$J\b|\bJ\(|J=|J =",
    "phase": r"\bphase",
    "varepsilon": r"\\varepsilon",
    "delta": r"\\delta",
    "k-1": r"k\s*-\s*1",
    "selected edge": r"selected edge",
    "black inner": r"black[- ]inner",
    "white-face tree": r"white[- ]face tree|tree on (the )?white",
    "partner": r"\bpartners?\b",
    "mate": r"\bmates?\b",
    "spoke": r"\bspokes?\b",
    "marked": r"\bmarked\b",
    "Q_s": r"Q_s|Q_\{s\}",
    "omega": r"\\omega",
    "slope": r"\bslope",
    "circulation": r"circulation",
}


def main():
    texts = {k: "\n".join(Path(f).read_text(encoding="utf8", errors="replace") for f in sorted(glob(g)))
             for k, g in DOCS.items()}
    print("term".ljust(18) + "".join(k.ljust(11) for k in DOCS))
    for t, pat in TERMS.items():
        flags = 0 if t == "J" else re.I
        print(t.ljust(18) + "".join(str(len(re.findall(pat, texts[k], flags))).ljust(11) for k in DOCS))
    print()
    for t in ["good state", "height", "J", "phase", "forest pair", "tree pair", "cover", "black inner", "white-face tree", "c_min", "k-1"]:
        pat = TERMS[t]
        for k, txt in texts.items():
            m = re.search(pat, txt, 0 if t == "J" else re.I)
            if m:
                a = max(0, m.start() - 160)
                print(f"[{t} | {k}] ..." + txt[a:m.end() + 220].replace("\n", " ") + "...")
        print()


if __name__ == "__main__":
    main()
