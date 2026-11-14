from pathlib import Path
p=Path('proofs/sign-free/STATUS.md')
s=p.read_text(encoding='utf-8')
lines=s.splitlines()
for i,line in enumerate(lines):
    if line.startswith('| Edmonds, disjoint branchings |'):
        lines[i]='| Edmonds, disjoint branchings | Edmonds 1973; Schrijver, *Polyhedral combinatorics*, pp. 1674 and 1685-1686 | Sol independently opened https://ir.cwi.nl/pub/2216/2216D.pdf and https://ir.cwi.nl/pub/2216. Title page confirms Chapter 30, editors Graham, Grotschel and Lovasz, and 1995. Catalog confirms pages 1649-1704. The remembered fields were correct. |'
    if line.startswith('| 7, descent on pairs (C3) |'):
        lines[i]='| 7, descent on pairs (C3) | conjecture; independent replay through 20 vertices, original census through 23; strict descent fails at 16; three and four moves needed at 21 and 40; paths with non-increasing `c` fail at 16 | CONJECTURE and REFUTED variants | Sol reconciled FACTS.md, Astra final referee report and Fable descent REPORT.md. Independent: 3,373,400 pairs through 20. Original: 193,623,384 through 23. Not recomputed here. |'
p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
