"""Move the flow-network figure (and its lead-in sentence) after the proof of
Proposition 5.2 in paper/main/barnette.tex. Text is moved, not changed."""
import sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()
lead = r"Figure~\ref{fig:flow} shows the network and a tight cut in the example."
a = s.index(lead)
b = s.index(r"\end{figure}", a) + len("\\end{figure}\n")
block = s[a:b]
s2 = s[:a] + s[b:]
p = s2.index(r"\begin{proposition}\label{prop:pair}")
e = s2.index(r"\end{proof}", p) + len("\\end{proof}\n")
s2 = s2[:e] + "\n" + block + s2[e:]
open(path, "w", encoding="utf-8").write(s2)
print("moved", len(block), "characters")
