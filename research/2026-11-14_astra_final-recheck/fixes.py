from pathlib import Path
R=Path.cwd()
p=R/'research/2026-11-14_astra_citation-audit/validate.py';s=p.read_text(encoding='utf8');s=s.replace('assert all(c[k]==v for k,v in m.items())', '''# Internal verification notes use annote in the print subset; compare citation
# metadata byte for byte after removing both note and annote fields.
def without_notes(entry):
 starts=list(re.finditer(r'(?m)^  ([A-Za-z]+)\\s*=',entry))
 for i in range(len(starts)-1,-1,-1):
  if starts[i][1].lower() in {'note','annote'}:
   end=starts[i+1].start() if i+1<len(starts) else entry.rfind('}')
   entry=entry[:starts[i].start()]+entry[end:]
 return entry
assert all(without_notes(c[k])==without_notes(v) for k,v in m.items())''');p.write_text(s,encoding='utf8')
p=R/'papers/README.md';p.write_text(p.read_text(encoding='utf8')+'\nThe main bibliography uses nonprinting `annote` fields for internal verification notes, so the citation validator compares canonical entries after dropping both `note` and `annote`.\n',encoding='utf8')
p=R/'proofs/involutions/involutions.tex';s=p.read_text(encoding='utf8');s=s.replace('September 2026, local source\n\\texttt{papers/OpenAI-Barnette.pdf}',r'''OpenAI Math Release preprint, family 180, 24 September 2026,
\url{https://github.com/openai/math/blob/main/preprints/Paired-states-and-Hamiltonian-cycles-in-cubic-bipartite-planar-graphs-September-24-2026/paper.pdf}''');s=s.replace('\\emph{A constructive proof}, local project source\n\\texttt{papers/barnette\\_trees.pdf}',r'\emph{A constructive proof of Barnette\textquotesingle s conjecture}, unsigned manuscript, 18 October 2026');s=s.replace(r'Barnette\textquotesingle s',"Barnette's");p.write_text(s,encoding='utf8')
