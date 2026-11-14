from pathlib import Path
import json,re,hashlib,shutil,unicodedata,csv
R=Path('research/2026-11-14_astra_literature-consolidation'); P=Path('papers')
entries=json.loads((R/'raw-catalog.json').read_text(encoding='utf-8')); meta={e['old']:e for e in json.loads((R/'metadata-checks.json').read_text(encoding='utf-8'))}
alias=json.loads((R/'aliases.json').read_text())
exclude=set('grinberg1968 grunbaum1970 grunbaum-walther1973 horton1982 ellingham-horton1983 georges1989 abhm2000 abhm1999 holton-mckay1988 whitney1931 bondy-locke1981 ozeki-ye2016 hko2016 ma2026 knauer-valicov2017 cambie2024 bonnet2023 bej2020 florek2020b cahit2009 clarke2013 shah2014 hongmin-li2026 formal-conjectures-pr kalai-blog2026 hn-2026 openproblemgarden cert-machine BMSConstellations1999 Bonichon2002 FPSDissections BMS2002 Schaeffer1997 Jung2026 Makarov2026 YutsisProject'.split())
# Additional sources found in route reports or requested explicitly.
def add(key,typ,**f):entries.append(dict(old=key,type=typ,fields=f,origin='consolidation primary-source lookup'))
add('Felsner2004','article',author='Felsner, Stefan',title='Lattice Structures from Planar Graphs',year='2004',journal='Electronic Journal of Combinatorics',volume='11',number='1',pages='R15',doi='10.37236/1768',url='https://www.combinatorics.org/ojs/index.php/eljc/article/download/v11i1r15/pdf/',note='Primary PDF opened; Theorem 1. Reuse permission not established.')
add('Batagelj1989','incollection',author='Batagelj, Vladimir',title='An improved inductive definition of two restricted classes of triangulations of the plane',year='1989',booktitle='Combinatorics and Graph Theory',series='Banach Center Publications',volume='25',pages='11--18',doi='10.4064/-25-1-11-18',note='Publisher volume listing checked; full paper not obtained; statement via Drapal 2009 as recorded in the induction report.')
add('Branden2020','article',author='Brändén, Petter and Huh, June',title='Lorentzian polynomials',year='2020',journal='Annals of Mathematics',volume='192',number='3',pages='821--891',doi='10.4007/annals.2020.192.3.4',eprint='1902.03719',archiveprefix='arXiv',url='https://annals.math.princeton.edu/2020/192-3/p04',note='Publisher PDF title and abstract opened; no identification of the Barnette polynomial as Lorentzian established.')
add('Thomas1994','article',author='Thomas, Robin and Yu, Xingxing',title='4-connected projective-planar graphs are Hamiltonian',year='1994',journal='Journal of Combinatorial Theory, Series B',volume='62',pages='114--132',url='https://thomas.math.gatech.edu/PAP/ham.pdf',note='Author PDF opened by older-approaches agent; introduction and Section 2 checked there.')
add('Pivotto2019','misc',author='Pivotto, Irene and Royle, Gordon',title='Highly-connected planar cubic graphs with few or many Hamilton cycles',year='2019',eprint='1901.10683',archiveprefix='arXiv',note='Sections 2, 5, 6 opened by counting-families agent; families are not asserted bipartite.')
# Confirmed matching registry records; wrong search hits are deliberately rejected.
if (R/'extra-metadata.json').exists():
 for record in json.loads((R/'extra-metadata.json').read_text(encoding='utf-8')):
  if record['old'] in ['GarsiaMilne1981','Lindstrom1973','GesselViennot1985','Lovasz1980','JKR2012','KalmanMurakami2017'] and 'record' in record:
   for entry in entries:
    if entry['old']==record['old']:
     m=record['record'];entry['fields']['doi']=m['DOI']
     for dst,src in [('volume','volume'),('number','issue'),('pages','page')]:
      if m.get(src):entry['fields'].setdefault(dst,m[src])
for entry in entries:
 if entry['old']=='KPW2000':
  entry['fields']['doi']='10.37236/1503'
  entry['fields']['note']+='; publisher landing page gives 1999 date but issue and PDF identify volume 7 (2000); year retained as 2000'
 if entry['old']=='tutte1975':entry['fields'].pop('number',None)
 if entry['old']=='Batagelj1989':entry['fields']['publisher']='PWN'
 if entry['old']=='Edmonds1979':entry['fields'].update(booktitle='Discrete Optimization I',publisher='Elsevier',pages='39--49')
# Repair known names, retaining source initials rather than inventing expansions.
fix={'Tamas Kalman':'Tamás Kálmán','Lilla Tothmeresz':'Lilla Tóthmérész','Andras Juhasz':'András Juhász','Laszlo Lovasz':'László Lovász','Andras Recski':'András Recski','Bernt Lindstrom':'Bernt Lindström','Gerard Viennot':'Gérard Viennot','Mireille Bousquet-Melou':'Mireille Bousquet-Mélou','Eric Fusy':'Éric Fusy','Andre Bouchet':'André Bouchet','Adrian Tanasa':'Adrian Tanasă'}
def plain(s):
 for a,b in [(r"{\'a}",'á'),(r"{\'o}",'ó'),(r"{\'e}",'é'),(r'{\"u}','ü'),(r'{\"o}','ö'),(r'{\v{s}}','š')]:s=s.replace(a,b)
 return s.replace('{','').replace('}','').replace('\\&','&')
def slug(s):return re.sub('[^A-Za-z0-9]','',unicodedata.normalize('NFKD',plain(s)).encode('ascii','ignore').decode())
# Candidate files indexed by bibliography key, never by title alone.
candidates={}
h=Path('research/2026-11-14_opus_history-literature/pdf')
for line in (h/'INDEX.md').read_text(encoding='utf-8').splitlines():
 cells=[x.strip() for x in line.split('|')]
 if len(cells)>5 and cells[1].startswith('`'):
  candidates[cells[3].strip('`')]=(h/cells[1].strip('`'),cells[4])
m=Path('research/2026-11-14_sol_machinery-literature')
mp=dict(zip('bms-constellations kuperberg-cokernels alon-tarsi bernardi-kalman-postnikov bernardi-orientations penrose-embedded hopf-tutte fps-dissections schrijver-matroid-intersection lovasz-recski hine-kalman kalman-hypergraphs kalman-postnikov juhasz-kalman-rasmussen kalman-murakami kalman-tothmeresz kenyon-double-dimer kenyon-propp-wilson propp-orientations burton-pemantle stein fps-bipolar bousquet-melou-schaeffer alon-nullstellensatz jung-induced-forests makarov-induced-forests'.split(),'BMSConstellations1999 Kuperberg2002 AlonTarsi1992 BKP2022 Bernardi2008 EllisMonaghanMoffatt2013 KrajewskiMoffattTanasa2017 FPSDissections SchrijverIntersection LovaszRecski1982 hine-kalman2018 Kalman2013 KalmanPostnikov2017 JKR2012 KalmanMurakami2017 KalmanTothmeresz2020 Kenyon2011 KPW2000 Propp2002 BurtonPemantle1993 stein1971 FPS2009 BMS2002 Alon1999 Jung2026 Makarov2026'.split()))
for d in json.loads((m/'downloads.json').read_text()):
 if d['key'] in mp and (m/'pdf'/(d['key']+'.pdf')).exists(): candidates.setdefault(mp[d['key']],(m/'pdf'/(d['key']+'.pdf'),d['url']))
for old,key in [('ford1956','Ford1956'),('Felsner2004','Felsner2004'),('Branden2020','Branden2020'),('ans1980','Akiyama1980'),('KalmanTothmeresz2020','Kalman2020')]:
 for d in json.loads((R/'retry-downloads.json').read_text()):
  if d['key']==key and d['status']=='PDF downloaded':candidates[old]=(R/'downloads'/(key+'.pdf'),d['url'])
originals={'openai2026':'OpenAI-Barnette.pdf','li2026':'A-Note-On-Barnette.pdf','constructive2026':'barnette_trees.pdf'}
# Explicit permissions for the exact retained files. Others remain URL records.
permissions={'bagheri2022':'CC0 1.0, arXiv record','gsw2023':'CC BY 4.0, arXiv record','bekos2025':'CC BY 4.0, PDF first page','shao-wu2025':'CC BY 4.0, arXiv record','KalmanTothmeresz2020':'CC BY 4.0, journal PDF cover'}
uses={
 'stein1971':('equivalents','LIT. Theorem 2.2, region-cycle B-set criterion.','digestions/steps/02-dual-and-two-trees.md; paper/draft-A/barnette.tex introduction; paper/draft-B/barnette.tex target equivalence'),
 'apsw2016':('equivalents','LIT. Lemma 5, Hamiltonian dual iff two permeating induced trees.','digestions/steps/02-dual-and-two-trees.md; both drafts, dual target'),
 'hertel2005':('equivalents','LIT. Corollary 3, universal prescribed-edge strengthening; Theorems 8–10.','digestions/steps/08-gluing-and-hypotheses.md; both drafts, introduction'),
 'gsw2023':('equivalents','LIT. Theorems 4.3 and 4.16, universal edge-avoidance and Pfaffian P4 equivalences; v3 numbering.','digestions/steps/09-what-is-still-open.md; research/2026-11-14_astra_route-pfaffian/GSW-CHAIN.md'),
 'kelmans1994':('equivalents','LIT via Alt and Hertel. Prescribed-edge strengthening and cut reductions.','digestions/steps/08-gluing-and-hypotheses.md; both drafts, introduction'),
 'harant2013':('equivalents','LIT. Linear-path reformulation.','research/2026-11-14_opus_history-literature/EQUIVALENTS.md; no direct draft dependency'),
 'openai2026':('2026','LIT, supplied preprint. Proposition 3.1; Lemmas 4.1, 5.3; Sections 5–6.','digestions/steps/00-overview.md through 08-gluing-and-hypotheses.md; proofs/primal/PRIMAL-PROOF.md; both drafts'),
 'li2026':('2026','LIT, preprint. Section 6 black dual trace and Appendix C gluing.','proofs/primal/PRIMAL-PROOF.md; draft B, recovery and gluing'),
 'constructive2026':('2026','Supplied unsigned manuscript. Integer sign, polynomial, partners and marked walk; not independently certified here.','digestions/steps/05-cancellation.md; proofs/primal/PRIMAL-PROOF.md; both drafts'),
 'ford1956':('machinery','LIT. Theorem 1, minimal-cut theorem. Integral augmentation is supplied in draft A itself.','digestions/steps/03-states-and-pairs.md; both drafts, pair-existence argument'),
 'Felsner2004':('machinery','LIT. Theorem 1, feasible alpha-orientations form a distributive lattice; essential cycles matter.','digestions/steps/09-what-is-still-open.md; research/2026-11-14_sol_referee-structure/INTEGRATION.md'),
 'Batagelj1989':('machinery','LIT via Drápal 2009 and plantri. Inductive generation operations.','research/2026-11-14_opus_route-induction/INDUCTION.md; no direct draft dependency'),
 'Branden2020':('machinery','LIT. Lorentzian polynomial framework; applicability to project polynomials remains open.','research/2026-11-14_sol_counting-families/BOUNDS.md; research routes only, no draft dependency'),
 'ans1980':('history','LIT. Section 2 concerns planar 2-connected cubic bipartite hardness, not the Barnette class.','digestions/steps/08-gluing-and-hypotheses.md; research/2026-11-14_sol_referee-structure/REFEREE-graph-theory.md'),
 'bgm2021':('history','LIT. Theorem 4.1, computational verification through 90 vertices.','paper/draft-B/barnette.tex introduction; digestions/steps/09-what-is-still-open.md'),
 'goodey1975':('history','LIT via Hertel. Hamiltonicity with face sizes four and six.','paper/draft-B/barnette.tex introduction'),
 'hmm1985':('history','LIT via Holton–Aldred. Bound 64, not the later bound 90.','paper/draft-B/barnette.tex introduction'),
 'tutte1946':('history','LIT via Hertel. Non-Hamiltonian cubic 3-connected planar counterexample.','paper/draft-B/barnette.tex introduction and hypotheses'),
 'tait1884':('history','LIT via Hertel. Historical conjecture without bipartiteness.','paper/draft-B/barnette.tex introduction'),
 'barnette1969':('history','Historical conjecture record; attribution conflict remains unresolved.','both drafts, introduction; see MISMATCHES.md'),
 'feder-subi2006':('history','LIT. Face-colour conditions; distinguish 2006 report from 2008 author revision.','paper/draft-B/barnette.tex introduction; research/2026-11-14_astra_older-approaches/OLD-MACHINERY.md'),
 'schnieders2025':('history','LIT, preprint. Face sizes at most eight; not independently proof-audited here.','paper/draft-B/barnette.tex introduction'),
 'tutte1975':('machinery','LIT via Hine–Kálmán and Kálmán. Trinity and states.','digestions/steps/03-states-and-pairs.md; both drafts, states'),
 'hine-kalman2018':('machinery','LIT. Planar state convention, Section 1; clock theorems.','digestions/steps/03-states-and-pairs.md; both drafts, states'),
 'heightnote':('2026','Project proof note, not a published result. Sections 1–3 height product.','paper/draft-A/barnette.tex signed count'),
 'draftdata':('2026','COMPUTED provenance only; no new calculations in this consolidation.','paper/draft-A/barnette.tex examples'),
 'Pivotto2019':('history','LIT, preprint. Sections 2, 5, 6, fixed-width cycle counts outside the bipartite restriction.','research/2026-11-14_sol_counting-families/BOUNDS.md; no direct draft dependency'),
 'Thomas1994':('machinery','LIT. Tutte-path bridge conditions, Section 2.','research/2026-11-14_astra_older-approaches/SOURCES.md; no direct draft dependency')}

for old,description,dep in [
 ('Kenyon2011','LIT. Section 3.2.1, Lemma 1: independent two-way cycle choices in the double-dimer expansion.','digestions/steps/06-nonvanishing.md; OpenAI Section 5.3'),
 ('KPW2000','LIT. Theorem 1: weighted tree-matching bijection when the root vertex meets the root face; otherwise only an injection.','digestions/steps/07-recovery.md; OpenAI Section 6'),
 ('Kalman2013','LIT. Definitions 3.1 and 9.1; Theorems 3.4 and 9.10, hypertrees and trinity.','digestions/steps/03-states-and-pairs.md; research/2026-11-14_opus_route-topology/TOPOLOGY.md'),
 ('JKR2012','LIT. Theorem 1.1, sutured Floer homology and hypertrees; not a proof of Barnette existence.','research/2026-11-14_opus_route-topology/TOPOLOGY.md; no direct draft dependency'),
 ('GarsiaMilne1981','LIT via constructive manuscript. Involution principle for finite alternating walks.','digestions/steps/09-what-is-still-open.md; papers/barnette_trees.pdf'),
 ('GarsiaMilneAnnouncement','LIT. Short announcement of bijective partition methods; full original proof not inspected.','digestions/steps/09-what-is-still-open.md; papers/barnette_trees.pdf'),
 ('SchrijverIntersection','LIT. Theorem 5.26, matroid intersection as a diagnostic for proposed exchanges.','research/2026-11-14_sol_machinery-literature/MACHINERY.md; no direct draft dependency'),
 ('Alon1999','LIT. Theorem 1.2, coefficient nonvanishing criterion.','digestions/steps/06-nonvanishing.md; machinery comparison only'),
 ('AlonTarsi1992','LIT. Theorem 1.1, orientation-based signed nonvanishing.','digestions/steps/05-cancellation.md; machinery comparison only'),
 ('Kuperberg2002','LIT. Theorem 6, path determinants, and comparison with Kasteleyn matrices.','research/2026-11-14_astra_route-pfaffian/REPORT.md; machinery report'),
 ('Propp2002','LIT. Orientation lattices for state-space comparisons.','research/2026-11-14_opus_route-topology/TOPOLOGY.md; no direct draft dependency'),
 ('florek2020','LIT. Theorem 1, Hamilton-cycle lower bound under a facial-quadrilateral 2-factor hypothesis.','research/2026-11-14_sol_counting-families/BOUNDS.md; no direct draft dependency')]:
 role=uses.get(old,('machinery',))[0]
 if old=='florek2020':role='history'
 uses[old]=(role,description,dep)

keys={}; counts={}; rows=[]; manifest=[]; decisions=[]
for e in entries:
 old=e['old'];f=e['fields']
 if old in exclude:decisions.append(f'{old}: excluded from curated bibliography as peripheral, duplicate-language original, superseded survey, withdrawn/unaccepted claim or commentary; remains in source research inventory.');continue
 for k in list(f):
  for a,b in fix.items():f[k]=f[k].replace(a,b)
 author=plain(f.get('author','Anonymous')).split(' and ')[0]
 surname=author.split(',')[0] if ',' in author else author.split()[-1]
 surname={'constructive2026':'Anonymous','heightnote':'Fable','draftdata':'BarnetteProject','openai-math-repo':'OpenAI','mohar-problem':'Mohar','SchrijverIntersection':'Schrijver'}.get(old,surname)
 key=slug(surname)+f.get('year','Undated'); counts[key]=counts.get(key,0)+1
 if counts[key]>1:key+=chr(96+counts[key])
 keys[old]=key;e['key']=key
 if old=='Kuperberg2002':f.update(eprint='math/0108150',archiveprefix='arXiv')
 if old=='barnette1969':f['note']='Original page not obtained. Draft A attributes Unsolved problem 5 to Grünbaum; draft B attributes Conjecture 5 to Barnette. Attribution retained provisionally from the history bibliography; see MISMATCHES.md.'
 role,use,dep=uses.get(old,('machinery' if 'machinery' in e['origin'] else 'history','Literature context. '+f.get('note','Statement not checked.'),e['origin'].replace('bibliography.bib','MACHINERY.md' if 'machinery' in e['origin'] else 'RESULTS-TABLE.md')+'; no direct draft dependency identified'))
 if old.startswith('florek'):dep+='; research/2026-11-14_sol_counting-families/BOUNDS.md' if old in ['florek2020','florek2025'] else ''
 if old in ['GarsiaMilne1981','GarsiaMilneAnnouncement']:dep='digestions/steps/09-what-is-still-open.md; papers/barnette_trees.pdf marked walk; machinery report'
 local='';url=f.get('url','');license=''
 if old in originals:local=originals[old];license='supplied original, preserved unchanged';url=f.get('url','supplied repository original')
 elif old in candidates:
  src,url=candidates[old]
  if old in permissions:
   title='-'.join(slug(x) for x in plain(f['title']).split()[:7]);local=role+'/'+f.get('year','Undated')+'-'+slug(surname)+'-'+title+'.pdf';license=permissions[old]
   dst=P/local;dst.parent.mkdir(exist_ok=True);shutil.copy2(src,dst)
  else:local='not held: free copy located; redistribution permission not established'
 else:local='not held: full source not obtained'
 if not url and f.get('eprint'):url='https://arxiv.org/abs/'+f['eprint']
 if not url and f.get('doi'):url='https://doi.org/'+f['doi']
 if url.startswith('http'):f['url']=url
 note=f.get('note','')
 checked=old in ['stein1971','apsw2016','openai2026','ford1956','gsw2023','li2026','Felsner2004','hertel2005','Kenyon2011','KPW2000','schnieders2025']
 if checked:verified='opened and statement checked'
 elif old in candidates or old in originals:verified='opened' if old in ['Branden2020','KalmanTothmeresz2020'] else 'opened'
 else:verified='cited from secondary source ('+e['origin']+')'
 evidence=meta.get(old,{}); metadata=evidence.get('url','source PDF or primary lookup recorded in report')+'; '+evidence.get('status','see source notes')
 citation=plain(f.get('author','Anonymous'))+'. '+plain(f['title'])+'. '+', '.join(plain(f[k]) for k in ['journal','booktitle','volume','number','pages','year'] if f.get(k))
 ids='; '.join((['DOI '+f['doi']] if f.get('doi') else [])+(['arXiv:'+f['eprint']] if f.get('eprint') else [])) or 'No DOI/arXiv identifier verified'
 rows.append(dict(key=key,old=old,role=role,citation=citation,ids=ids,local=local,url=url,use=use,dependency=dep,verified=verified,prior_note=note,metadata=metadata,license=license))
 if not local.startswith('not held'):
  b=(P/local).read_bytes();manifest.append(dict(filename='papers/'+local,sha256=hashlib.sha256(b).hexdigest(),source_url=url,size=len(b),license=license))
retained=[e for e in entries if 'key' in e]
(P/'barnette.bib').write_text('% Curated 2026-11-14. Verification and version notes: INDEX.md.\n\n'+'\n\n'.join('@'+e['type']+'{'+e['key']+',\n'+',\n'.join('  '+k+' = {'+v+'}' for k,v in e['fields'].items())+'\n}' for e in retained)+'\n',encoding='utf-8')
head='# Literature index\n\nOne record per source. LIT marks a literature statement, not an independent proof audit. Preprints and unsigned manuscripts retain that qualification. "Opened" can refer to the named prior agent inspection; exact inspection scope is preserved below. Metadata checks are separate from statement checks. No online permission is inferred merely from free access.\n\n'
for role in ['history','equivalents','machinery','2026']:
 head+='## '+role+'\n\n| Key and full citation | DOI / arXiv | Local file or access limit | Project use | Dependency | Verified |\n|---|---|---|---|---|---|\n'
 for r in rows:
  if r['role']!=role:continue
  loc=('['+r['local']+']('+r['local']+')') if not r['local'].startswith('not held') else r['local']
  if r['url'].startswith('http'):loc+='; [source]('+r['url']+')'
  cells=[r['key']+' — '+r['citation'],r['ids'],loc,r['use'],r['dependency'],r['verified']+'; inspection scope: '+r['prior_note']]
  head+='| '+' | '.join(c.replace('|','/').replace('\n',' ') for c in cells)+' |\n'
 head+='\n'
(P/'INDEX.md').write_text(head,encoding='utf-8')
(R/'catalog.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
with (R/'manifest.csv').open('w',encoding='utf-8',newline='') as out:
 w=csv.DictWriter(out,fieldnames=list(manifest[0]));w.writeheader();w.writerows(manifest)
(R/'KEY-MAP.md').write_text('# Bibliography key map\n\nDo not edit drafts during consolidation. Apply these replacements to both refs.bib files and citation commands together.\n\n| Existing key | Canonical key |\n|---|---|\n'+'\n'.join('| '+a+' | '+keys.get(b,'not retained')+' |' for a,b in alias.items())+'\n',encoding='utf-8')
(R/'SELECTION.md').write_text('# Selection decisions\n\n'+ '\n'.join('- '+x for x in decisions)+'\n\nVersion rules: history inventory wins for Stein, Hine–Kálmán and GSW v3. Kálmán–Tóthmérész uses the CC-BY journal copy instead of the arXiv copy. The originals remain untouched. Free copies without established redistribution rights remain URL records, even if research agents already downloaded them.\n',encoding='utf-8')
print(len(rows),'records',len(manifest),'PDFs',sum(x['size'] for x in manifest),'bytes')
