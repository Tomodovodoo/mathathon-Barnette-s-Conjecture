"""One-shot: in digestions/steps/06-nonvanishing.md, lines 37-156, rename the white-face letter w to y
and the height h_s to eta_s (the main paper's notation). Polynomial variables w_{t,v} above line 37 and
below line 156 are left alone. Run once from the repository root."""
import re

p = "digestions/steps/06-nonvanishing.md"
L = open(p, encoding="utf-8", newline="").read().split("\n")
reps = [
    ("h_s(", r"\eta_s("), ("h_{s_", r"\eta_{s_"), (r"\kappa_w", r"\kappa_y"), (r"\gamma_w", r"\gamma_y"),
    (r"\sum_w", r"\sum_y"), ("$w$", "$y$"), ("(w)", "(y)"), (r"w \text", r"y \text"),
    ("The selected white faces", "The chosen white faces"),
]
n = 0
for i in range(36, 156):
    for a, b in reps:
        n += L[i].count(a)
        L[i] = L[i].replace(a, b)
    L[i], k = re.subn(r"\bw_([i12])\b", r"y_\1", L[i])
    n += k
open(p, "w", encoding="utf-8", newline="").write("\n".join(L))
print(n, "replacements")
