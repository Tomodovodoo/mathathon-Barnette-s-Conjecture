"""Inventory for section 11 of digestions/SYNTHESIS.md.

Run from the repository root:

    python research/2026-11-14_opus_synthesis-final/synthesis-audit/count.py

Writes counts.json, route-classification.json and count-output.txt next to this file.
It counts folders, reports, route records and PDF pages. It reruns no mathematical census.

The route-kind rules are copied unchanged from
research/2026-11-14_astra_synthesis/count.py (GPT-6 Astra), so that the chart stays
comparable with the first snapshot. They are editorial: each record gets the first
kind whose keyword pattern matches its text, and "Combinatorial" when none matches.
"""
from pathlib import Path
import runpy, json, re, hashlib, datetime, subprocess, sys
from collections import Counter
import fitz

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent

routes = runpy.run_path(str(ROOT / "digestions/route-map/routes.py"))["ROUTES"]
KINDS = ["Combinatorial", "Graph-theoretic / structural", "Constructive / algorithmic",
         "Algebraic / determinantal", "Topological", "Probabilistic", "Categorical",
         "Inductive", "Lattice-theoretic", "Non-planar / Pfaffian"]
RULES = [
    (9, r"pfaffian|nonplanar|non-planar|heawood|torus|other surfaces"),
    (6, r"categor|temperley.lieb|belyi|boundary.pattern|trinity|operad"),
    (7, r"induct|contraction|degree.4|local expansion|lift criterion|three.face rotation"),
    (8, r"lattice|felsner|irreducible|alpha.orientation|clock order|rank.compatible"),
    (5, r"probabil|random|sampling|measure|lorentz|m.convex|mean load"),
    (3, r"determinant|algebra|polynomial|berezin|gaussian|congruence|mod p|gauge|coefficient|real stability|semidefinite|nullstellensatz|2.adic"),
    (4, r"topolog|morse|gauss.bonnet|turning|winding|jordan|homolog|floer"),
    (2, r"algorithm|walk|search|descent|marked|complexity|ppad"),
    (1, r"matroid|packing|hall|flow|euler|duality|spanning.tree|connectivity|gluing|separator|cut|recovery|induced|structur"),
]


def kind(r):
    t = " ".join(str(r.get(k, "")) for k in ["label", "text", "where", "arg"]).lower()
    for k, pat in RULES:
        if re.search(pat, t):
            return KINDS[k]
    return KINDS[0]


OUTCOME = {"LIT": "Proved", "PROVED-HERE": "Proved", "COMPUTED": "Computed",
           "CONJECTURE": "Open", "HUNCH": "Open", "REFUTED": "Refuted"}
rows = [dict(id=r["id"], label=r["label"], kind=kind(r), status=r["status"],
             outcome=OUTCOME[r["status"]]) for r in routes]
(OUT / "route-classification.json").write_text(json.dumps(rows, indent=2), encoding="utf8")

runs = sorted(p for p in (ROOT / "research").iterdir()
              if p.is_dir() and p.name.startswith("2026-11-14_"))
reports = [p / "REPORT.md" for p in runs if (p / "REPORT.md").exists()]
MODELS = {"astra": "GPT-6 Astra", "sol": "GPT-6.1 Sol", "fable": "Fable 5.2", "opus": "Opus 5.5"}

PRODUCT_PDFS = ["paper/main/barnette.pdf", "paper/main/history/barnette-v1.pdf",
                "proofs/primal/primal.pdf", "proofs/involutions/involutions.pdf",
                "proofs/blueprint/blueprint.pdf", "proofs/blueprint/columns.pdf",
                "digestions/atlas/atlas.pdf"]
pdfs = {}
for rel in PRODUCT_PDFS:
    p = ROOT / rel
    if p.exists():
        with fitz.open(p) as doc:
            pdfs[rel] = len(doc)

step_words = {p.relative_to(ROOT).as_posix(): len(re.findall(r"\b[\w]+\b", p.read_text(encoding="utf8")))
              for p in sorted((ROOT / "digestions/steps").glob("*.md"))}
synthesis = (ROOT / "digestions/SYNTHESIS.md").read_text(encoding="utf8")
# prose words of the synthesis: drop link targets, HTML comments and table rules
prose = re.sub(r"<!--.*?-->", " ", synthesis, flags=re.S)
prose = re.sub(r"\]\([^)]*\)", "]", prose)
prose = re.sub(r"^\|[-:| ]+\|$", " ", prose, flags=re.M)
synthesis_words = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", prose))


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True).stdout.strip()


data = dict(
    timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    head=git("rev-parse", "--short", "HEAD"),
    run_folders=len(runs),
    reports=len(reports),
    models=dict(Counter(MODELS.get(p.name.split("_")[1], p.name.split("_")[1]) for p in runs)),
    runs_without_report=[p.name for p in runs if not (p / "REPORT.md").exists()],
    routes=len(rows),
    route_status=dict(Counter(r["status"] for r in rows)),
    route_matrix={k: {o: sum(r["kind"] == k and r["outcome"] == o for r in rows)
                      for o in ["Proved", "Computed", "Open", "Refuted"]} for k in KINDS},
    pdf_pages=pdfs,
    current_product_pages_total=sum(v for k, v in pdfs.items() if "history/" not in k),
    step_files=len(step_words),
    step_words_total=sum(step_words.values()),
    synthesis_words=synthesis_words,
    index_rows=len(re.findall(r"^\| `", (ROOT / "research/INDEX.md").read_text(encoding="utf8"), flags=re.M)),
    report_inventory=[dict(path=p.relative_to(ROOT).as_posix(),
                           sha256=hashlib.sha256(p.read_bytes()).hexdigest()[:16],
                           bytes=p.stat().st_size) for p in reports],
)
(OUT / "counts.json").write_text(json.dumps(data, indent=2), encoding="utf8")
shown = json.dumps({k: v for k, v in data.items() if k != "report_inventory"}, indent=2)
(OUT / "count-output.txt").write_text(shown + "\n", encoding="utf8")
sys.stdout.write(shown + "\n")
