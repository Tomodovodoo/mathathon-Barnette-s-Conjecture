"""Mechanical checks on digestions/SYNTHESIS.md.

Run from the repository root, after count.py:

    python research/2026-11-14_opus_lean-integration/synthesis-audit/check.py

Checks: every relative link resolves; no em dash, en dash, curly quote or internal
status tag in the text; the numbers of the inventory block equal counts.json;
word count. Writes check-output.txt next to this file and exits non-zero on a failure.
"""
from pathlib import Path
import json, re, sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DOC = ROOT / "digestions/SYNTHESIS.md"
text = DOC.read_text(encoding="utf8")
counts = json.loads((HERE / "counts.json").read_text(encoding="utf8"))
problems, notes = [], []

links = re.findall(r"\]\(([^)\s]+)\)", text)
for target in links:
    if re.match(r"https?://", target):
        continue
    path = (DOC.parent / target.split("#")[0]).resolve()
    if not path.exists():
        problems.append(f"broken link: {target}")
notes.append(f"links checked: {len(links)}")

for name, pat in [("em dash", "—"), ("en dash", "–"), ("curly quote", "[‘’“”]"),
                  ("status tag", r"\b(PROVED-HERE|COMPUTED|HUNCH|REFUTED|CONJECTURE|LIT)\b")]:
    hits = re.findall(pat, text)
    if hits:
        problems.append(f"{name}: {len(hits)} occurrence(s)")

block = text[text.index("<!-- inventory-start -->"):text.index("<!-- inventory-end -->")]
m = counts["models"]
st = counts["route_status"]
pg = counts["pdf_pages"]
expect = [
    f"There are {counts['run_folders']} run folders and {counts['reports']} of them hold a final report",
    f"{m['GPT-6 Astra']} are GPT-6 Astra, {m['Fable 5.2']} Fable 5.2, {m['Opus 5.5']} Opus 5.5 and {m['GPT-6.1 Sol']} GPT-6.1 Sol",
    f"The route map has {counts['routes']} records: {st['LIT']} arguments from the sources, {st['PROVED-HERE']} proofs written here, "
    f"{st['COMPUTED']} computations, {st['CONJECTURE']} conjectures, {st['HUNCH']} hunches and {st['REFUTED']} refutations",
    f"(../paper/main/barnette.pdf) | {pg['paper/main/barnette.pdf']} |",
    f"(../paper/main/history/barnette-v1.pdf) | {pg['paper/main/history/barnette-v1.pdf']} |",
    f"(../proofs/primal/primal.pdf) | {pg['proofs/primal/primal.pdf']} |",
    f"(../proofs/involutions/involutions.pdf) | {pg['proofs/involutions/involutions.pdf']} |",
    f"about {round(counts['step_words_total'], -3):,} words",
    f"(atlas/atlas.pdf) | {pg['digestions/atlas/atlas.pdf']} |",
    counts["timestamp"][:16].replace("T", " ") + " UTC",
]
for e in expect:
    if e not in block:
        problems.append(f"inventory block does not say: {e}")

# numbers repeated outside the block
R, X = counts["routes"], st["REFUTED"]
for needle in [f"{pg['paper/main/barnette.pdf']}-page exposition",
               f"Version 2, {pg['paper/main/barnette.pdf']} pages",
               f"map of {R} attempted routes, {X} of them recorded as refuted",
               f"{pg['proofs/primal/primal.pdf']} pages. The whole proof",
               f"{pg['proofs/involutions/involutions.pdf']} pages. Li's argument",
               f"{pg['digestions/atlas/atlas.pdf']} pages of computed pictures",
               f"{R} route records sorted"]:
    if needle not in text:
        problems.append(f"sentence out of date, expected: {needle!r}")
no_report = counts["run_folders"] - counts["reports"]
words = {0: "No", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight"}
late = text[text.index("<!-- late-start -->"):text.index("<!-- late-end -->")]
if not re.search(rf"{words.get(no_report, str(no_report))} folders? holds? no final report", late):
    problems.append(f"late block should say that {no_report} folders hold no final report")

notes.append(f"words (prose, link targets removed): {counts['synthesis_words']}")
notes.append(f"sections: {len(re.findall(r'^## ', text, flags=re.M))}")
out = "\n".join(notes + ([f"PROBLEM {p}" for p in problems] or ["no problem found"])) + "\n"
(HERE / "check-output.txt").write_text(out, encoding="utf8")
sys.stdout.write(out)
sys.exit(1 if problems else 0)
