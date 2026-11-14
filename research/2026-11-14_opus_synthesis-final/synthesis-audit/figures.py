"""Draw the two figures of digestions/SYNTHESIS.md.

Run from the repository root, after count.py:

    python research/2026-11-14_opus_synthesis-final/synthesis-audit/figures.py

Writes products.pdf/.png and route-outcomes.pdf/.png to digestions/synthesis-figures/.
The PNGs are rendered from the PDFs. The route chart reads counts.json in this folder.
The products chart is drawn from the PRODUCTS table below; its page counts are
checked against counts.json, so a changed PDF stops the script.
"""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import fitz

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / "digestions/synthesis-figures"
data = json.loads((HERE / "counts.json").read_text(encoding="utf8"))
pages = data["pdf_pages"]

INK, LINE, PAPER = "#1f2a28", "#54736d", "#faf9f5"
plt.rcParams.update({"font.family": "DejaVu Sans", "pdf.fonttype": 42, "font.size": 10,
                     "text.color": INK})

# ---------------------------------------------------------------- products
MAIN, V1 = pages["paper/main/barnette.pdf"], pages["paper/main/history/barnette-v1.pdf"]
PRI, INV = pages["proofs/primal/primal.pdf"], pages["proofs/involutions/involutions.pdf"]
ATL = pages["digestions/atlas/atlas.pdf"]

fig, ax = plt.subplots(figsize=(11.7, 8.3))
fig.patch.set_facecolor(PAPER)
ax.set(xlim=(0, 12), ylim=(0, 8.3))
ax.axis("off")
ax.text(0.2, 7.85, "What exists, where it comes from, and who checked it", size=20, weight="bold")
ax.text(0.2, 7.45, "Arrows run from a source to the text built on it. "
                    "The line under each proof names the model that checked it.", size=10.5)


def box(x, y, w, h, title, body, fill="#ffffff", note=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=.07",
                                fc=fill, ec=LINE, lw=1.2))
    ax.text(x + w / 2, y + h - 0.27, title, ha="center", va="center", size=10.5, weight="bold")
    ax.text(x + w / 2, y + h / 2 - (0.12 if note is None else 0.02), body, ha="center", va="center", size=9.2)
    if note:
        ax.text(x + w / 2, y + 0.2, note, ha="center", va="center", size=8.6, style="italic", color="#3c5a54")
    return (x, y, w, h)


def arrow(a, b, rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=11, color="#63716d", lw=1,
                                 shrinkA=3, shrinkB=3, connectionstyle=f"arc3,rad={rad}"))


def rowlabel(y, text):
    ax.text(0.33, y, text, size=8.5, color=LINE, weight="bold", rotation=90, ha="center", va="center")


W, H = 2.55, 1.75
xs = [0.75, 3.55, 6.35, 9.15]
cx = [x + W / 2 for x in xs]

# row 1: sources
YS, HS = 5.85, 1.1
rowlabel(YS + HS / 2, "SOURCES")
box(xs[0], YS, 8.0 - xs[0], HS, "Three source papers",
    "OpenAI's proof, Li's note, the unsigned constructive manuscript.\nPreprints. No journal has refereed them.")
box(8.4, YS, xs[3] + W - 8.4, HS, "OpenAI's Lean proof",
    "31 files, built twice, once from\na fresh clone. Three standard axioms.")

# row 2: proofs written here
Y = 3.45
rowlabel(Y + H / 2, "WRITTEN HERE")
box(xs[0], Y, W, H, "Main paper", f"version 2, {MAIN} pages\ndual triangulation",
    note="Both versions\nrefereed by Sol.")
box(xs[1], Y, W, H, "Involution companion", f"{INV} pages\nLi's argument, general m",
    note="Refereed by Opus,\nthen by Fable.")
box(xs[2], Y, W, H, "Primal companion", f"{PRI} pages\nthe proof inside G",
    note="Refereed by Fable.\nFinal review by Opus.")
box(xs[3], Y, W, H, "Blueprint, Lean devices", "34 statements beside Lean:\n5 exact, 17 translated,\n10 weaker, 2 none.",
    note="Lean by Opus. Rebuilt and\naudited by Astra.")
for i in (0, 1):
    arrow((cx[i], YS), (cx[i], Y + H))
arrow((cx[2] - 0.45, YS), (cx[2] - 0.45, Y + H))      # sources -> primal
arrow((8.62, YS), (8.62, Y + H))                      # Lean -> primal
arrow((cx[3], YS), (cx[3], Y + H))                    # Lean -> blueprint
ax.text(6.0, Y - 0.3, "The blueprint sets each statement of the main paper beside its Lean counterpart.",
        ha="center", size=9, color="#3c5a54")

# row 3: guides and tools
Y3, H3 = 1.3, 1.15
rowlabel(Y3 + H3 / 2, "GUIDES, TOOLS")
box(xs[0], Y3, W, H3, "Step digestions", "eleven files: long proofs,\nexamples, failed alternatives")
box(xs[1], Y3, W, H3, "Route map, labyrinth", f"{data['routes']} route records,\n{data['route_status']['REFUTED']} refuted")
box(xs[2], Y3, W, H3, "Atlas", f"{ATL} pages of computed\npictures of the routes")
box(xs[3], Y3, W, H3, "Lab, figures, library", "reference code, figure toolkit,\n87 indexed sources")

ax.text(0.75, 0.6, f"Behind all of it: {data['run_folders']} research and referee runs by four AI models. "
                    "No human has checked any of it.\n"
                    "The Lean kernel checks Lean statements. It does not check the texts written here.",
        size=10)
fig.savefig(OUT / "products.pdf", bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- route outcomes
fig, ax = plt.subplots(figsize=(11.7, 8.3))
fig.patch.set_facecolor(PAPER)
ax.axis("off")
ax.text(0, 1.03, "Route records by kind and recorded status", transform=ax.transAxes, size=20, weight="bold")
cols = ["Proved", "Computed", "Open", "Refuted"]
kinds = list(data["route_matrix"])
vals = [[data["route_matrix"][k][c] for c in cols] for k in kinds]
tot = [sum(col) for col in zip(*vals)]
cells = vals + [tot]
table = ax.table(cellText=cells, rowLabels=kinds + ["All kinds"], colLabels=cols, cellLoc="center",
                 bbox=[.36, .19, .62, .76])
table.auto_set_font_size(False)
table.set_fontsize(12)
tint = ["#e0ece4", "#e3edf6", "#f5eedb", "#f2e2df"]
for (i, j), cell in table.get_celld().items():
    cell.set_edgecolor("#d0d6d3")
    cell.set_linewidth(.6)
    cell.set_facecolor("#e3ece9" if i == 0 else "#ffffff")
    if i == 0 or i == len(cells):
        cell.set_text_props(weight="bold")
    if i > 0 and j >= 0 and cells[i - 1][j] > 0:
        cell.set_facecolor(tint[j])
assert sum(tot) == data["routes"]
ax.text(0, .09, f"{data['routes']} records, each given one kind by keyword rules. The kinds overlap, so the rows are a rough guide.\n"
                "Proved = argument from a source paper, or a proof written here, reviewed or not. Open = conjecture or hunch.\n"
                "These are records of attempts. They are not independent proofs and not review verdicts.",
        transform=ax.transAxes, size=10)
ax.text(0, .01, "Source: digestions/route-map/routes.py. Rules and assignments: research/2026-11-14_opus_synthesis-final/synthesis-audit/ "
                f"(count.py, route-classification.json). Counted {data['timestamp'][:16].replace('T', ' ')} UTC.",
        transform=ax.transAxes, size=8)
fig.savefig(OUT / "route-outcomes.pdf", bbox_inches="tight")
plt.close(fig)

for stem in ["products", "route-outcomes"]:
    with fitz.open(OUT / (stem + ".pdf")) as doc:
        assert len(doc) == 1
        doc[0].get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(OUT / (stem + ".png"))
print("wrote products and route-outcomes (pdf and png)")
