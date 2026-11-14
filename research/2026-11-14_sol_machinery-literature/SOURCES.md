# Source and reading ledger

All URLs were searched or opened on 2026-11-14. `pdf/INDEX.md` lists the actual downloaded PDFs and original URLs. `downloads.json` records SHA-256 checksums. The download command is `python research/2026-11-14_sol_machinery-literature/fetch_sources.py`; it also runs `pdftotext -layout` for each successful download. Downloading a source does not imply a proof audit. Reading depths below are deliberately different.

## Direct proof inputs

The supplied O, L and C text dumps were read in the repository, followed by targeted rereading of the disk identity, weighted sum, two involutions, Li's Appendix B, mate-count criterion, component polynomial, marked walk, determinant count and recovery. OpenAI page 6 was rendered and visually checked to confirm J, Z and the +/-2 phase change:

    pdftoppm -f 6 -singlefile -scale-to 1600 -png papers/OpenAI-Barnette.pdf research/2026-11-14_sol_machinery-literature/pdf/openai-page6

The resulting `pdf/openai-page6.png` is a local verification image, not an independently downloaded paper. The reading does not independently authenticate the three documents or prove every claim in them.

## Sources read at the relevant theorem level

| Source | Checked content | Public source |
| --- | --- | --- |
| Hine-Kálmán | State convention, connected sums, Theorems 4.2-4.3, Lemma 4.4, references | https://arxiv.org/abs/1808.06091 |
| Kálmán, hypergraphs | Definition 3.1, Theorem 3.4, Sections 9-10, Berman determinant | https://www.math.titech.ac.jp/top/~kalman/hypertutte.pdf |
| Kenyon | Sections 3.1-3.3, Lemma 1, Theorem 2, doubled-edge and connection conventions | https://arxiv.org/abs/1105.4158 |
| KPW | Overlay bijection, weighted statement and root convention | https://arxiv.org/abs/math/9903025 |
| Stein | Theorem 2.2 and Alexander-duality argument | https://msp.org/pjm/1971/37-1/pjm-v37-n1-p20-p.pdf |
| Alon | Theorem 1.2, coefficient nonvanishing criterion | https://www.tau.ac.il/~nogaa/PDFS/null2.pdf |
| Alon-Tarsi | Original Theorem 1.1 and definitions of Eulerian subgraphs | https://kostochk.web.illinois.edu/math581/Alon-Tarsi92.pdf |
| Schrijver | Matroid intersection, Theorem 5.26, page 1678 | https://ir.cwi.nl/pub/2216/2216D.pdf |
| Kuperberg | LGV Theorem 6, Section 3.3; Kasteleyn-Percus Section 3.1 | https://arxiv.org/abs/math/0108150 |

## Statements and relevant definitions inspected, without auditing their entire proofs

The full PDFs were downloaded for Kálmán-Postnikov, Juhász-Kálmán-Rasmussen, Kálmán-Murakami, Kálmán-Tóthmérész, Propp, Burton-Pemantle, Bernardi, Bernardi-Kálmán-Postnikov, the two FPS papers, Bousquet-Mélou-Schaeffer, Lovász-Recski, Ellis-Monaghan-Moffatt, and Krajewski-Moffatt-Tanasa. Abstracts, introductions, definitions and the theorem statements cited in `MACHINERY.md` were checked. These are sources for their stated results, not a claim that every proof or every possible connection was checked.

The Jung and Makarov August 2026 preprints were downloaded after searching the present status of Albertson-Berman. Their abstract claims were checked on their actual arXiv pages. Their alleged counterexamples were not independently computed. They are reported as preprint claims and are not used in any proof here.

## Older originals not obtained

| Original | What was actually checked | Limit |
| --- | --- | --- |
| Tutte, 1975 | Berman publisher references and Hine-Kálmán references; theorem in Kálmán Sections 9-10 | Original chapter not obtained |
| Berman, 1980 | Publisher record and abstract, DOI 10.1137/0601009; detailed theorem through Kálmán 9.10 | Original proof not obtained |
| Kauffman, 1983 | Hine-Kálmán Section 2.2 and references | Original book not read |
| Gilmer-Litherland, 1986 | Osaka repository record, DOI 10.18910/3828; role through Hine-Kálmán | Original access failed |
| Percus, 1969 | Record and DOI 10.1063/1.1664774; theorem through Kenyon and Kuperberg | Original DOI access failed |
| Kasteleyn, 1967 | Published references; theorem through Kenyon and Kuperberg | Original chapter not read |
| Garsia-Milne, JCTA 1981 | Garsia bibliography and supplied C references | Original not read; primary PNAS announcement opened |
| Rado, 1942 | Publisher record, DOI 10.1093/qmath/os-13.1.83 | Original proof paywalled |
| Edmonds, 1979 | Publisher record; theorem in Schrijver | Original chapter not read |
| Lovász, 1980 | Publisher abstract and primary-author Lovász-Recski survey | Original full text gave 403 |
| Bouchet, 1989 | Publisher search abstract and record | Original full text gave 403; detailed Eulerian-system identification remains HUNCH |
| Chaiken, 1982 | Publisher record and abstract, DOI 10.1137/0603033 | Full original not obtained |
| Lindström and Gessel-Viennot | Original bibliographic records and KPW references; general theorem in Kuperberg Theorem 6 | Original proofs not read |
| Bonichon | FPS paper and Fusy author discussion | Original citation not separately verified; no invented original entry in bibliography |
| Schaeffer, 1997 | Author's institutional publication record | Full original not read |

The exact original theorem numbering should not be cited for these unread originals. Use the modern theorem source named above.

## Further primary pages used

- [Garsia-Milne primary announcement](https://pmc.ncbi.nlm.nih.gov/articles/PMC319275/), PNAS 78, 1981, 2026-2028.
- [Berman publisher record](https://epubs.siam.org/doi/10.1137/0601009).
- [Chaiken publisher record](https://epubs.siam.org/doi/abs/10.1137/0603033).
- [Rado publisher record](https://academic.oup.com/qjmath/article-abstract/os-13/1/83/1520949).
- [Kálmán-Tóthmérész journal page](https://www.numdam.org/articles/10.5802/alco.129/).
- [BKP institutional publication record](https://dspace.mit.edu/entities/publication/402c0ed7-7fd9-4654-8263-2ade9159a15a).
- [Fusy author page](https://monge.univ-eiffel.fr/~fusy/), for map-bijection bibliographic distinctions.
- [Bousquet-Mélou-Schaeffer constellation record](https://researchportal.ip-paris.fr/en/publications/enumeration-of-planar-constellations/), a separate 2000 paper, not conflated with the downloaded degree-distribution paper.
- [Schaeffer 1997 institutional record](https://researchportal.ip-paris.fr/fr/publications/bijective-census-and-random-generation-of-eulerian-planar-maps-wi-2/).
- [Ghent Yutsis project](https://caagt.ugent.be/yutsis/), actual definition checked.
- [Jung preprint](https://arxiv.org/abs/2608.17350) and [Makarov preprint](https://arxiv.org/abs/2608.13964).

The Viennot author exposition search hit returned 403 when opened. The review instead uses the successfully downloaded Kuperberg statement for LGV. Search snippets alone were not promoted to proof-level verification.

## Unfinished bibliographic work

Locate legal open copies of Tutte, Berman, Gilmer-Litherland and Bouchet before writing a definitive historical account of their exact original formulations. Bousquet-Mélou-Schaeffer's FPSAC 1999 constellation paper was obtained late in the review and its Definition 2.1 and map/tree construction inspected. It contains Eulerian triangulations as a special 3-constellation class, but does not supply the extra state condition. Bonichon's exact FPSAC 2002 title and record were verified; the original PDF host failed TLS certificate validation, so that proof was not read. This review provides checked neighboring statements and explicit access limits, not exhaustive coverage of those originals.
