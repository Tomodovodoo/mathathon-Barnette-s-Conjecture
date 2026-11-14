from inventory import *
inv=json.loads(read(O/'inventory.json'));c=bib(R/'papers/barnette.bib');m=bib(R/'paper/main/refs.bib')
used={k for x in inv if x['file']=='paper/main/barnette.tex' for k in x.get('keys',[])}
allused={k for x in inv for k in x.get('keys',[])}
assert sum(x['file']=='digestions/atlas/atlas.tex' for x in inv)==30
assert set(m)==used
assert all(c[k]==v for k,v in m.items())
assert allused<=c.keys()
idx=read(R/'papers/INDEX.md');assert all('| '+k+' |' in idx for k in allused)
orig=json.loads(read(O/'pdf-inventory.json'))
assert all(hashlib.sha256((R/x['file']).read_bytes()).hexdigest()==x['sha256'] for x in orig)
rights=json.loads(read(O/'rights.json'));assert len(rights)==50
texs=['paper/main/barnette.tex','proofs/primal/primal.tex','proofs/involutions/involutions.tex','proofs/sign-free/sign-free.tex']
result=dict(cite_commands=sum(x['kind']=='cite' for x in inv),contexts=len(inv),cited_keys=len(allused),main_subset_entries=len(m),canonical_entries=len(c),research_pdf_files=len(rights),research_pdf_bytes=sum(x['bytes'] for x in rights),original_pdf_hashes_unchanged=True,exact_main_subset=True,missing_keys=[],snapshot_hashes={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in texs})
(O/'VALIDATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(result)
cat={x['key']:x for x in json.loads(read(R/'research/2026-11-14_astra_literature-consolidation/catalog.json'))}
web={x['key']:x for x in json.loads(read(O/'web-checks.json'))}
out=['# Metadata audit','','Every current TeX citation key exists in the canonical bibliography. Metadata is distinct from statement verification. The table records the evidence actually available; a successful HTTP request alone does not certify every field. Existing publisher/Crossref comparisons remain in the consolidation METADATA-AUDIT.md and metadata-checks.json. No fields were filled from an unrelated search hit.','','| Key | Current lookup | Earlier metadata evidence | Limits or correction |','|---|---|---|---|']
for k in c:
 x=cat.get(k,{});w=web.get(k,{})
 out.append('| '+k+' | '+w.get('url','Local source or newly documented source')+'; '+w.get('status','No separate online lookup saved')+' | '+x.get('metadata','See entry and source-level decisions in CITATION-AUDIT.md')+' | '+('Current explicit citation.' if k in allused else 'No current explicit citation; may be cited in prose.')+' '+('Fresh metadata contains citation fields; compare web-checks.json.' if w.get('metadata') else 'Not every field independently reverified in this pass.')+' |')
out+=['','## Specific decisions','','- Barnette1969 attribution corrected to secondary evidence in the published Alt et al. bibliography; exact original-page wording remains unresolved.','- Anonymous2026 has no author; title and date are printed on the supplied manuscript.','- OpenAI2026b is pinned to the full upstream commit confirmed locally.','- Gorsky2023 retains journal year 2023 and arXiv v3 numbering.','- Feder2006 retains the ECCC report year 2006; its scanned manuscript is dated 20 January 2004. The 2008 author revision is distinct.','- Source PDFs preserve Tomas Feder, Tamas Kalman, Andras Juhasz and Frantisek Kardos with their printed diacritics; canonical entries retain the existing Unicode/TeX accent spelling. Terminal mojibake in PowerShell output was not treated as file corruption.','- Georges1989 and Holton-McKay1988 were missing from the library and were imported from the main bibliography. Georges metadata was then matched to the Elsevier page https://www.sciencedirect.com/science/article/pii/0095895689900129 . The associated DOI is 10.1016/0095-8956(89)90012-9; the existing entry is identifiable without adding it.','- Nash-Williams metadata is corroborated by the publisher record https://londmathsoc.onlinelibrary.wiley.com/doi/abs/10.1112/jlms/s1-39.1.12 . Original statement checked secondarily in Schrijver.','- Added the sign-free inline bibliography keys unchanged. SchrijverCourse and Schrijver2017 name the same course; SchrijverHandbook and SchrijverUndated name the same handbook chapter. These aliases are intentional and documented in papers/README.md.']
(O/'METADATA-AUDIT.md').write_text('\n'.join(out)+'\n',encoding='utf-8')
