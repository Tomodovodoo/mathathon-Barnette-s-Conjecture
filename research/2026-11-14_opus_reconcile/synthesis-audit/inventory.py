"""Rewrite the two generated blocks of digestions/SYNTHESIS.md from counts.json.

Run from the repository root, after count.py:

    python research/2026-11-14_opus_reconcile/synthesis-audit/inventory.py

It replaces the text between the inventory-start/inventory-end markers and between
the late-start/late-end markers, and the two route counts quoted on page one and in
the products table. Everything else in the document is left alone.
"""
from pathlib import Path
import json, re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DOC = ROOT / "digestions/SYNTHESIS.md"
c = json.loads((HERE / "counts.json").read_text(encoding="utf8"))
m, st, pg = c["models"], c["route_status"], c["pdf_pages"]
when = c["timestamp"][:16].replace("T", " ") + " UTC"
WORD = {0: "No", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight"}

inventory = f"""<!-- inventory-start -->
The inventory was taken at {when} by [count.py](../research/2026-11-14_opus_reconcile/synthesis-audit/count.py), with output in [counts.json](../research/2026-11-14_opus_reconcile/synthesis-audit/counts.json). It counts folders and files. It reruns no census.

There are {c['run_folders']} run folders and {c['reports']} of them hold a final report. By folder name, {m['GPT-6 Astra']} are GPT-6 Astra, {m['Fable 5.2']} Fable 5.2, {m['Opus 5.5']} Opus 5.5 and {m['GPT-6.1 Sol']} GPT-6.1 Sol. The route map has {c['routes']} records: {st['LIT']} arguments from the sources, {st['PROVED-HERE']} proofs written here, {st['COMPUTED']} computations, {st['CONJECTURE']} conjectures, {st['HUNCH']} hunches and {st['REFUTED']} refutations. Those are recorded statuses, not review verdicts.

| PDF | Pages |
|---|---:|
| [Main paper, version 2, at the time of the count](../paper/main/barnette.pdf) | {pg['paper/main/barnette.pdf']} |
| [Main paper, version 1](../paper/main/history/barnette-v1.pdf) | {pg['paper/main/history/barnette-v1.pdf']} |
| [Primal companion](../proofs/primal/primal.pdf) | {pg['proofs/primal/primal.pdf']} |
| [Involution companion](../proofs/involutions/involutions.pdf) | {pg['proofs/involutions/involutions.pdf']} |
| [Atlas](atlas/atlas.pdf) | {pg['digestions/atlas/atlas.pdf']} |

The eleven step files hold about {round(c['step_words_total'], -3):,} words, counting headings and link text.
"""

open_runs = [n.replace("2026-11-14_", "") for n in c["runs_without_report"]]
k = len(open_runs)
if k:
    names = ", ".join(f"`{n}`" for n in open_runs)
    verb = "folder holds" if k == 1 else "folders hold"
    late = (f"<!-- late-start -->\n**Runs still open at this snapshot.** {WORD.get(k, str(k))} {verb} no final report: {names}. "
            "Nothing from them is counted as a result above.\n")
else:
    late = "<!-- late-start -->\n**Runs still open at this snapshot.** None. Every run folder holds a final report.\n"

t = DOC.read_text(encoding="utf8")
a, b = t.index("<!-- inventory-start -->"), t.index("<!-- inventory-end -->")
t = t[:a] + inventory + t[b:]
a, b = t.index("<!-- late-start -->"), t.index("<!-- late-end -->")
t = t[:a] + late + t[b:]
t, n1 = re.subn(r"a map of \d+ attempted routes, \d+ of them recorded as refuted",
                f"a map of {c['routes']} attempted routes, {st['REFUTED']} of them recorded as refuted", t)
t, n2 = re.subn(r"\| \d+ route records sorted", f"| {c['routes']} route records sorted", t)
assert n1 == 1 and n2 == 1, (n1, n2)
DOC.write_text(t, encoding="utf8", newline="\n")
print(f"inventory block: {c['run_folders']} folders, {c['reports']} reports, {c['routes']} routes; open runs: {k}")
