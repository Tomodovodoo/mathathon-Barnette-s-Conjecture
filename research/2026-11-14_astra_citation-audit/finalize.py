from inventory import *
import csv,html
inv=json.loads(read(O/'inventory.json'));cat=json.loads(read(R/'research/2026-11-14_astra_literature-consolidation/catalog.json'));web={x['key']:x for x in json.loads(read(O/'web-checks.json'))}
canonical=bib(R/'papers/barnette.bib'); main=bib(R/'paper/main/refs.bib')
used=sorted({k for x in inv for k in x.get('keys',[])})
main_used=sorted({k for x in inv if x['file']=='paper/main/barnette.tex' for k in x.get('keys',[])})
canonical.update({
'Edmonds1973':'''@incollection{Edmonds1973,
  author = {Edmonds, Jack},
  title = {Edge-disjoint branchings},
  booktitle = {Combinatorial Algorithms},
  editor = {Rustin, Randall},
  publisher = {Academic Press},
  address = {New York},
  year = {1973},
  pages = {91--96},
  note = {Metadata and statement verified through Schrijver, Polyhedral combinatorics; original not opened}
}''',
'NashWilliams1964':'''@article{NashWilliams1964,
  author = {Nash-Williams, C. St. J. A.},
  title = {Decomposition of finite graphs into forests},
  journal = {Journal of the London Mathematical Society},
  volume = {39},
  pages = {12},
  year = {1964},
  note = {Statement verified through Schrijver, A Course in Combinatorial Optimization, Exercise 10.29; original not opened}
}''',
'Expo':'''@misc{Expo,
  title = {The proof of Barnette's conjecture: an exposition},
  year = {2026},
  howpublished = {Project manuscript, paper/main/barnette.pdf},
  note = {14 November 2026; project proof, not a published literature result}
}''',
'SchrijverCourse':'''@misc{SchrijverCourse,
  author = {Schrijver, Alexander},
  title = {A Course in Combinatorial Optimization},
  year = {2017},
  url = {https://homepages.cwi.nl/~lex/files/dict.pdf},
  note = {Lecture notes dated 23 March 2017; Exercises 10.26, 10.28 and 10.29}
}''',
'SchrijverHandbook':'''@incollection{SchrijverHandbook,
  author = {Schrijver, Alexander},
  title = {Polyhedral combinatorics},
  booktitle = {Handbook of Combinatorics},
  publisher = {Elsevier},
  year = {1995},
  pages = {1649--1704},
  chapter = {30},
  url = {https://ir.cwi.nl/pub/2216/2216D.pdf}
}'''})
for k in used:
 if k not in canonical:canonical[k]=main[k]
canonical['Barnette1969']=re.sub(r'  note = .*?(?=\n\})','  note = {Attribution verified secondarily in Alt, Payne, Schmidt and Wood, 2016, reference 3, printed p. 364. Original proceedings p. 343 not obtained.}',canonical['Barnette1969'],flags=re.S)
canonical['OpenAI2026b']=re.sub(r'  note = .*?(?=\n\})',r'  note = {Source revision 4eaee87548250b2682affda7d05d947c05554bae, confirmed against the project upstream checkout on 14 November 2026; independent build reported in research/2026-11-14_astra_lean-check/REPORT.md.}',canonical['OpenAI2026b'],flags=re.S)
canonical['Schrijver2017']='''@misc{Schrijver2017,
  author = {Schrijver, Alexander},
  title = {A Course in Combinatorial Optimization},
  year = {2017},
  url = {https://homepages.cwi.nl/~lex/files/dict.pdf},
  note = {Lecture notes dated 23 March 2017; Exercises 10.26, 10.28 and 10.29}
}'''
canonical['Thomason1978']='''@article{Thomason1978,
  author = {Thomason, A. G.},
  title = {Hamiltonian cycles and uniquely edge colourable graphs},
  journal = {Annals of Discrete Mathematics},
  volume = {3},
  pages = {259--268},
  year = {1978},
  doi = {10.1016/S0167-5060(08)70511-9},
  url = {https://www.dpmms.cam.ac.uk/~agt2/HC.pdf}
}'''
for k in canonical:
 canonical[k]=re.sub(r'(?m)^(  note = .*?)$',lambda m:re.sub(r'(?<!\\)_',r'\\_',m[0]),canonical[k])
(R/'papers/barnette.bib').write_text('% Canonical bibliography. Audit: research/2026-11-14_astra_citation-audit/\n\n'+'\n\n'.join(canonical.values())+'\n',encoding='utf-8')
(R/'paper/main/refs.bib').write_text('% Exact entry subset of papers/barnette.bib for citations in barnette.tex.\n\n'+'\n\n'.join(canonical[k] for k in main_used)+'\n',encoding='utf-8')
# These are statement checks, not proof certification.
evidence={
'Thomason1978':('opened','Author-hosted scan HC.pdf rendered, printed pp. 261-262. Corollary 1.2 gives the odd-degree path parity; Corollary 1.5 gives g(v) = h(e,f) = H modulo 2 for cubic graphs. In a cubic bipartite graph the odd (n-1)-cycles are absent, so cycles avoiding a fixed edge are even. No claim that the total count is even in every cubic graph.'),
'Expo':('opened','Project exposition and existing AUX label map checked. Sign-free references match Lemma 2.5, Proposition 3.9, Lemma 3.8, Lemma 4.2, Proposition 4.8 and Proposition 5.2. Status PROVED-HERE, not published LIT; no new proof audit implied.'),
'Edmonds1973':('secondary','Schrijver Handbook pp. 1674, 1685-1686, opened. Out-branching result becomes the cited in-branching statement by reversing arcs. Publisher Academic Press confirmed in handbook bibliography; original not opened.'),
'NashWilliams1964':('secondary','Schrijver course Exercise 10.29, printed p. 189, opened online; follows from matroid covering Exercise 10.28. Cycle matroids permit parallel edges; loops are excluded in the sign-free statement. Original not opened.'),
'SchrijverCourse':('opened','Author PDF dated 23 March 2017, Exercises 10.26 and 10.29, printed pp. 188-189. Exact optional exercise numbers and statements match.'),
'SchrijverHandbook':('opened','Held publisher scan, Application 5.6 p. 1674 and pp. 1685-1686. Exact optional page numbers match. Distinct from the course notes.'),
'OpenAI2026':('opened','Supplied PDF, Theorem 1.1 p. 1; Proposition 3.1 pp. 3-4; Lemma 4.1 p. 5; Proposition 5.1 and Lemma 5.2 p. 6; Lemma 5.3 p. 7; Section 5.3 pp. 7-8; Section 6 pp. 8-9; Corollaries 7.1 and 7.2 p. 10. Numbered references match. Weights arise from paths in a component dual; the project face-path identification is an additional project argument.'),
'Li2026':('opened','Supplied PDF/arXiv 2610.30490v1. Lemma 9 pp. 3-4; Claim 12 p. 4; Section 4 definitions and one-mark maps pp. 4-8; Claim 25 p. 8; Definition 28 and Lemma 30 in Section 6; Lemmas 34-35 p. 11; Appendix B sketches the generalization; Appendix C pp. 12-13. The project correctly distinguishes its full multi-mark proof from the sketch.'),
'Anonymous2026':('opened','Supplied unsigned PDF, dated 18 October 2026, title page has no author. Theorem 1.1 p. 1 gives enumeration bound; Theorem 1.2 p. 2 gives pair/black-inner obstruction/tree equivalence; Proposition 2.1 gives incidence-tree criterion; Lemma 5.1 integer weights; Theorem 5.3 pp. 10-11 gives the marked walk, with a different runtime. No author or public publication claimed.'),
'Gorsky2023':('opened','Held arXiv 2202.11641v3, Theorem 4.3 p. 7 and Theorem 4.16 pp. 12-13. Equivalence (i) with (v) is exactly the cubic Pfaffian three-edge-path consequence. Use v3 numbering, not an unpinned version. Earlier consolidation page 8 for Theorem 4.3 is inaccurate for this held copy.'),
'Hertel2005':('opened','Held author report, Corollary 3 p. 7 gives universal edge avoidance; Theorem 10 attributes the stronger common-face edge use/avoidance result to Kelmans. Page 5 reports HMM at 64 vertices and Goodey quadrilaterals/hexagons. Historical discussion supports Tutte counterexample.'),
'Alt2016':('opened','Held arXiv 1312.3783v1, Lemma 5 p. 3 gives dual Hamiltonicity, a permeating induced tree, and a partition into two permeating induced trees; Section 5 gives Kelmans equivalences. Published author PDF opened online, reference 3 on printed p. 364 attributes Conjecture 5, proceedings p. 343, to Barnette.'),
'Stein1971':('opened','Held publisher scan, Theorem 2.2, printed p. 218, PDF p. 3, states the region-cycle B-set equivalence. Two-induced-trees wording is supplied by Alt Lemma 5, not quoted as Stein verbatim.'),
'Brinkmann2022':('opened','Held arXiv 2101.00943v2, Theorem 4.1(a) pp. 14-15 gives n <= 90; introduction gives 50-vertex Georges-Kelmans minimality. Article year 2022 differs from preprint year 2021.'),
'Schnieders2025':('opened','Held arXiv 2508.03531v1, Corollary 1.13 p. 2 states the face-size-at-most-eight result. Preprint statement checked; its 339,068,624 cases were not rerun.'),
'Hine2018':('opened','Held arXiv 1808.06091v1, abstract and introduction define triangle-vertex states after deleting a triangle and its vertices, credit Tutte, and state sphere lattice results. Colours are exchanged harmlessly between accounts.'),
'Tutte1946':('secondary','Hertel 2005 historical discussion and Kardos 2020 introduction. Original 1946 full text not obtained; publisher access failed. Bibliographic fields agree with prior Crossref record, DOI 10.1112/jlms/s1-21.2.98.'),
'Feder2006':('opened','Original ECCC TR06-015 scan, first page rendered and read. Abstract confirms that two of three face-colour classes may contain only quadrilaterals and hexagons. Manuscript date is 20 January 2004; report header is 2006. Keep report year 2006. This is not the triangle-parity condition of Bagheri Gh. et al. The readable 2008 author revision is a different version.'),
'Ford1956':('secondary','Integral max-flow form checked through Schrijver course Chapter 4; prior consolidation opened original Ford-Fulkerson pp. 399-404. This pass did not reopen that original.'),
'Akiyama1980':('secondary','Bagheri Gh. et al. 2022 introduction p. 2 explicitly attributes NP-completeness for 2-connected cubic planar bipartite graphs to reference 10. Original unavailable in held corpus.'),
'georges1989':('secondary','Brinkmann-Goedgebeur-McKay introduction identifies Georges and Kelmans independently and establishes minimality. Original Georges article not opened.'),
'holton-mckay1988':('secondary','Kardos 2020 introduction and figure 1 state the 38-vertex minimum. Original Holton-McKay article not opened; metadata retained as supplied pending publisher confirmation.'),
'OpenAI2026b':('opened','Local upstream git rev-parse HEAD returns 4eaee87548250b2682affda7d05d947c05554bae. Formal proof/build status is secondary to research/2026-11-14_astra_lean-check/REPORT.md; no Lean build was rerun in this citation audit.'),
'Barnette1969':('secondary','Published Alt et al. 2016 reference 3, printed p. 364, verifies Barnette, Conjecture 5, p. 343. Original proceedings page not obtained. This resolves the bibliography attribution secondarily, not the exact wording of the original page.'),
'BagheriGh2021':('opened','Held arXiv 1806.05483v3, Theorem 11 p. 22: even interior vertex counts in every triangle of the contracted graph, plus face and separating-digon hypotheses. This is the parity criterion, not Feder-Subi 2006.'),
'BagheriGh2022':('opened','Held arXiv 2212.02668v2, Theorem 4.2 gives restricted face-tree hardness; the proof of Theorem 4.6, p. 12, explicitly states prescribed-edge Hamiltonicity decision hardness. The application must retain its decision-problem scope.'),
'Kardos2020':('opened','Held arXiv 1409.2440v2, Theorem 1: cubic 3-connected planar with face sizes at most six, without bipartiteness. Do not confuse its specialized definition of Barnette graph with the project definition.'),
'Kenyon2000':('opened','Held math/9903025, Theorem 1 p. 5. Weight-preserving bijection requires incident distinguished vertex and face. Otherwise only injection.'),
'Juhasz2012':('opened','Held arXiv 1112.2632, Theorem 1.1 p. 2 identifies sutured Floer support with hypertrees for the associated plane bipartite graph. Does not assert Barnette Hamiltonicity.'),
'Rado1942':('secondary','Schrijver, A Course in Combinatorial Optimization, Exercise 10.26. Independent transversal iff every union of t sets has rank at least t. Original Rado not opened.'),
'Schrijver2017':('opened','Author course PDF, dated 23 March 2017; Exercises 10.26, 10.28 and 10.29. Covers Rado and Nash-Williams via matroid covering. Separate source from Polyhedral combinatorics.'),
'SchrijverUndated':('opened','Held Polyhedral combinatorics, Application 5.6 p. 1674 and p. 1686: Edmonds disjoint branchings. Reverse arcs for in-arborescences. This source does not replace the course citation for Exercises 10.26-10.29.'),
'Goodey1975':('secondary','Hertel 2005 Theorem 2 p. 5; original not obtained.'),
'Holton1985':('secondary','Hertel p. 5 and Bagheri Gh. 2022 p. 2 explicitly give the 64-vertex bound.'),
'Tutte1975':('secondary','Hine-Kalman introduction and bibliography. Original Duality and trinity not opened.'),
'Kelmans1994':('secondary','Hertel Corollary 3/Theorem 10 and Alt Section 5; no direct Kelmans citation remains in main paper. Route-map prose should name this secondary chain.'),
}
labels={'opened':'verified by opening the source','secondary':'verified from a secondary source','unverified':'not verifiable in this audit'}
(O/'statement-checks.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
def status(k):
 a,b=evidence.get(k,('unverified','No exact statement comparison completed in this pass. Prior catalog inspection remains recorded separately.'))
 return labels[a]+': '+b
lines=['# Citation audit','', 'Snapshot 14 November 2026. `LIT` below means a source-attribution check, including explicitly qualified preprints; it is not proof certification. `COMPUTED` applies only to extraction and link inventory. The sign-free document appeared during this run and is included in the final extraction. Every extracted cite command, with optional arguments intact, appears below. Prose records retain full paragraphs so sentence boundaries inside TeX do not hide qualifiers. Some records overlap deliberately.','', 'The source-level checks are separate from project proof claims. A valid link does not verify a theorem, computation, or review status. Unchecked project reports are classified explicitly rather than promoted to LIT.','', '## Source-level decisions','']
for k,v in evidence.items():lines+=['### '+k,'','LIT. '+status(k),'']
lines+=['## Every extracted citation and context','']
for i,x in enumerate(inv,1):
 lines+=['### C'+str(i)+' '+x['file']+':'+str(x['line']),'']
 if x['kind']=='cite':
  lines+=['Citation: `'+x['citation']+'`.','']
  for k in x['keys']:lines+=['LIT. `'+k+'`: '+status(k),'']
 else:
  hits=[k for k,pat in {'OpenAI2026':r'OpenAI|\bO (?:Section|Corollary|Lemma|Proposition)', 'Li2026':r'\bLi\b|A-Note-On-Barnette','Anonymous2026':r'barnette.?trees|constructive (?:paper|manuscript|preprint)|trees paper','Stein1971':r'Stein','Alt2016':r'Alt,|Payne','Hertel2005':r'Hertel','Rado1942':r'Rado','BagheriGh2022':r'Bagheri.*2022','BagheriGh2021':r'parity condition of Bagheri','Brinkmann2022':r'Brinkmann','Ford1956':r'Ford and Fulkerson'}.items() if re.search(pat,x['context'])]
  for k in hits:lines+=['Source attribution only. '+k+': '+status(k),'']
  links=re.findall(r'\]\(([^)]+)\)|\\path\{([^}]+)\}|`((?:research|proofs|papers)/[^`]+)`',x['context'])
  for parts in links:
   target=next(t for t in parts if t);target=target.split('#')[0]
   if target.startswith('http'):exists='external link, not independently opened by this link check'
   else:
    path=(R/x['file']).parent/target if '../' in target else R/target
    exists='target exists' if path.exists() else 'target not resolved as a repository path'
   lines+=['COMPUTED link check: `'+target+'`, '+exists+'. Statement class: not verifiable from link existence alone; no independent content check is implied.','']
  if not hits:lines+=['Statement class: not verifiable in this pass. This context contains a project attribution, internal cross-reference, or unnumbered literature mention without a completed exact comparison. Retained for the owners to review.','']
 lines+=['```text',x['context'],'```','']
(O/'CITATION-AUDIT.md').write_text('\n'.join(lines),encoding='utf-8')
# Preserve old index, append an authoritative current-use table.
idx=read(R/'papers/INDEX.md').split('\n## Final reader citation audit')[0]
idx+='\n## Final reader citation audit\n\nThis table supersedes draft-only use labels above. Full sentences, limitations and optional arguments are in [CITATION-AUDIT.md](../research/2026-11-14_astra_citation-audit/CITATION-AUDIT.md). The main bibliography is an exact entry subset of the canonical file. Inline involution keys map OAI to OpenAI2026, Li to Li2026, trees to Anonymous2026; the primal note uses prose rather than BibTeX.\n\n| Key | Current use | Verification class and scope |\n|---|---|---|\n'
for k in sorted(set(used)|set(evidence)):
 locs=[x['file']+':'+str(x['line']) for x in inv if k in x.get('keys',[])]
 if k in ('Li2026','OpenAI2026','Anonymous2026'):locs+=['proofs/primal/primal.tex Sources','proofs/involutions/involutions.tex bibliography and prose','digestions/atlas/atlas.tex sources table']
 if not locs:locs=['Related prose / requested attention check; see audit. No explicit cite command in the four present TeX documents.']
 idx+='| '+k+' | '+'; '.join(locs)+' | '+status(k)+' |\n'
(R/'papers/INDEX.md').write_text(idx,encoding='utf-8')
all_text='\n'.join(read(p) for folder in ['paper','proofs','digestions','research'] for p in (R/folder).rglob('*.tex') if 'upstream' not in str(p))
uncited=[k for k in canonical if not re.search(r'\\cite\w*(?:\[[^\]]*\])*\{[^}]*\b'+re.escape(k)+r'\b',all_text)]
(O/'UNUSED-KEYS.md').write_text('# Keys without an explicit TeX cite\n\nCOMPUTED by finalize.py over project TeX, excluding upstream checkouts. This is not a claim that nobody mentions the work in prose or Markdown. Nothing was removed from the canonical bibliography.\n\n'+'\n'.join('- '+k for k in uncited)+'\n',encoding='utf-8')
print('Canonical',len(canonical),'main subset',len(used),'contexts',len(inv))
