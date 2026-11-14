from pathlib import Path
import json
p=Path('research/2026-11-14_astra_final-proofread'); t=(p/'source.tex').read_text()
edits=[
('S1',6,332,'Clarify the scope of necessity. Goodness is necessary for Y_s to be a tree, but not for a state to come from an acyclic selection.',r'The condition is sufficient for what follows and it is not necessary: the state that Lemma~\ref{lem:selections-give-states} reads off an acyclic selection need not satisfy it (Section~\ref{sec:remarks}).',r'This condition is sufficient for recovering an acyclic selection, but not every state obtained from an acyclic selection satisfies it (Section~\ref{sec:remarks}).'),
('S2',9,494,'The existence assertion needs the hypothesis of Proposition 4.8.',r'This section shows that one exists, by a count in four steps.',r'This section shows that one exists whenever a pair exists, by a count in four steps.'),
('S3',9,508,'Figure 7 currently appears on page 9 but is first cited in body text on page 10.',r'For a pair we write $u(t)$ for the third corner of $t$.',r'For a pair we write $u(t)$ for the third corner of $t$ (Figure~\ref{fig:localpair}).'),
('S4',18,1006,'P was defined as edges of T; the complement of the Hamiltonian cycle is edges of G.',r'If $s_C$ is good, the complement $P$ of $\mathcal{C}$ avoids $S_{s_C}$, because its side in each $t\in A$ contains $s_C(t)$ and its side in $t_0$ is $e_0$.',r'If $s_C$ is good, let $P$ be the set of edges of $\T$ crossing the edges of $G$ outside $\mathcal{C}$. Then $P$ avoids $S_{s_C}$, because its side in each $t\in A$ contains $s_C(t)$ and its side in $t_0$ is $e_0$.'),
('S5',18,1007,'Use the dual-edge notation for perfect matchings of Y_s.',r'Thus $P$ and $P_{s_C}$ are perfect matchings of the tree $Y_{s_C}$, and a tree has at most one perfect matching, so $P=P_{s_C}$.',r'Thus $P^*$ and $P_{s_C}^*$ are perfect matchings of the tree $Y_{s_C}$, and a tree has at most one perfect matching, so $P=P_{s_C}$.'),
('S6',19,1054,'Define the summation range and c(D) before the polynomial display.',r'Grouping by the undirected cycles of $D$ as in Proposition~\ref{prop:good},',r'Let $D$ range over the covers and let $c(D)$ be the number of cycles in $D$. Grouping by covers as in Proposition~\ref{prop:good},'),
('S7',19,1084,'Avoid attributing an intention to Li; describe the mathematical relationship.',r'It writes out in full the argument that Li \cite{Li2026} intended for Proposition~\ref{prop:good}, with marked crossings in place of the power $\omega^m$, and it is a term-by-term unpacking of Lemmas~\ref{lem:cancel}, \ref{lem:height} and~\ref{lem:difference} for one particular height.',r'It gives a version of Li\textquotesingle s argument \cite{Li2026} for Proposition~\ref{prop:good}, with marked crossings in place of the power $\omega^m$, and unpacks Lemmas~\ref{lem:cancel}, \ref{lem:height} and~\ref{lem:difference} term by term for one particular height.'),
]
# Use plain apostrophe, avoiding a new command dependency.
edits[-1]=(*edits[-1][:-1],edits[-1][-1].replace(r'Li\textquotesingle s',"Li's"))
text='# Ready-to-apply source edits\n\nAll pairs below are should-fix items. No must-fix change to the proof in barnette.tex was found. The must-fix bibliography residue is recorded separately in PROOFREAD.md because it is generated from refs.bib, not a unique string in barnette.tex. Do not replace the bibliography command to address it.\n\nLocations refer to source.tex and the 20-page PDF identified in manifest.json. Each old string occurs exactly once in that source. Apply S4 and S5 together.\n'
for id,page,line,why,old,new in edits:
 assert t.count(old)==1,(id,t.count(old))
 actual=t[:t.index(old)].count('\n')+1
 text+=f'\n## {id}. Page {page}, source line {actual}\n\n{why}\n\nOld:\n```tex\n{old}\n```\n\nNew:\n```tex\n{new}\n```\n'
(p/'EDITS.md').write_text(text)
(p/'edits.json').write_text(json.dumps([dict(id=id,page=page,line=t[:t.index(old)].count('\n')+1,reason=why,old=old,new=new) for id,page,line,why,old,new in edits],indent=2))
