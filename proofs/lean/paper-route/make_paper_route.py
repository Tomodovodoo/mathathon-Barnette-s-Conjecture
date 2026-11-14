r"""Generate PaperRoute/: copies of the openai/math files Forest.lean .. Main.lean (the tail of the
linear import chain) under the module prefix `PaperRoute.`, with ONE change: in Forest.lean the
call to the phase/polynomial lemma `Pair.forest_pair_of_disk_circulation` is replaced by
`Pair.forest_pair_of_disk_circulation_real` (Devices/RealSign.lean: real sign, omega^m, finite
differences), and Forest.lean additionally imports Devices.RealSign.

Usage (from the Lake project root, e.g. E:\lbb):  python make_paper_route.py
The OpenAI files are read from OAI/Combinatorics/Hamiltonian/ and are not modified.
"""
import pathlib, re, sys

SRC = pathlib.Path("OAI/Combinatorics/Hamiltonian")
DST = pathlib.Path("PaperRoute")
CHAIN = ["Forest", "Contraction", "MinorDuality", "BMatching", "Matching", "ForestMatching",
         "ThreeCuts", "CappedDuality", "Gluing", "Traces", "SquareGrid", "Corridors",
         "MinorModel", "BranchPartition", "Rectangle", "ExactDual", "Main"]

DST.mkdir(exist_ok=True)
changes = 0
for name in CHAIN:
    text = (SRC / f"{name}.lean").read_text(encoding="utf-8")
    for other in CHAIN:
        text = text.replace(f"import OAI.Combinatorics.Hamiltonian.{other}\n",
                            f"import PaperRoute.{other}\n")
    if name == "Forest":
        old = "  exact Pair.forest_pair_of_disk_circulation hex\n"
        new = "  exact Pair.forest_pair_of_disk_circulation_real hex\n"
        assert text.count(old) == 1, "expected exactly one call site"
        text = text.replace(old, new)
        text = text.replace("import OAI.Combinatorics.Hamiltonian.PairPolynomials\n",
                            "import OAI.Combinatorics.Hamiltonian.PairPolynomials\nimport Devices.RealSign\n")
        changes += 1
    (DST / f"{name}.lean").write_text(text, encoding="utf-8")
print(f"wrote {len(CHAIN)} files to {DST}/, {changes} file(s) changed beyond import paths")
