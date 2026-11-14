from pathlib import Path
import json,re,fitz
root=Path.cwd(); p=root/'digestions/route-map/build_map.py'; s=p.read_text()
s=s.replace('node("IT", "spanning tree of the spoke graph")','node("IT", "opposite edges Q_s plus ao and bo")').replace('node("WT", "duals of the deleted spokes")','node("WT", "faces joined across edges outside S_s")'); p.write_text(s,encoding='utf8')
p=root/'labyrinth/seed.py'; s=p.read_text()
s=s.replace("status='COMPUTED T4; compiled by its author; independent check pending.'","status='COMPUTED; independently rebuilt and statement-checked; retain the four qualifications in the review.'")
s=s.replace('C2 false first at V=18; extreme-or-irreducible R2 false at V=33.',"Felsner pair-lattice extremes fail at V=18; Propp state-clock extremes can lack partners at V=10; extreme-or-irreducible R2 fails at V=33.")
s=s.replace('Four uses in OpenAI, three in Li. In the real-sign form three uses need only that state cycles are odd; the value 3 is used once.', 'The final paper uses the exact disk count in its sign and nonvanishing route, and again to exclude selected cycles during recovery; parity alone does not justify that recovery count.')
s=s.replace('All papers use one double count. Parity suffices three times and the value 3 once (p.C.5). The topology agent derives the identity ', 'All papers use one double count. The final paper needs the exact count for signs and nonvanishing and for recovery. The topology agent derives the identity ')
# Route statements remain authoritative for current rows; history stays append-only.
s=s.replace("prior_path=LAB/'sota.json'", """for entry in S['entries']:
    if entry['id']=='canonical': entry['result']=by_route['D.7']['text']+' '+by_route['D.ext2']['text']
    if entry['id']=='rainbow-R': entry['status']='PROVED-HERE; independently AI-refereed with corrections; no human check.'
prior_path=LAB/'sota.json'""")
p.write_text(s,encoding='utf8')
# The atlas owner has now committed the corrected numbering. Verify it against the PDF
# and reconstruct the README index from the current manifest, preserving all other text.
p=root/'digestions/atlas/README.md'; s=p.read_text(); manifest=json.loads((p.parent/'manifest.json').read_text())
doc=fitz.open(p.parent/'atlas.pdf'); checks=[]
for item in manifest['pages']:
 n=item['n']; slug=item['slug']; title=item['title']; pdf=f'{n:02d}-{slug}.pdf'
 assert (p.parent/'pages'/pdf).exists(),pdf
 combined=doc[n].get_text()
 # PDF route pages follow contents; compare a normalized title fragment.
 normalize=lambda x: re.sub('[^a-z0-9]','',x.lower())
 assert normalize(title) in normalize(combined), (n,title)
 checks.append(dict(route_page=n,pdf_page=n+1,file=pdf,title=title))
head=s[:s.index('## Index')]
tail=s[s.index('The text block is',s.index('## Index')):]
index='## Index\n\nRoute-page numbers below match the current combined PDF. The contents is PDF page 1, so route page 1 is PDF page 2. This index was checked against the PDF after the renumbering.\n\n| Page | Route | PDF | Figure, cm | Words |\n| --- | --- | --- | --- | --- |\n'
for item in manifest['pages']:
 n=item['n']; dims=' x '.join(map(str,item['figure_cm']))
 index+=f"| {n} | {item['title']} | [PDF](pages/{n:02d}-{item['slug']}.pdf) | {dims} | {item['words']} |\n"
p.write_text(head+index+'\n'+tail,encoding='utf8')
(root/'research/2026-11-14_sol_digest-fixes/atlas-index-check.json').write_text(json.dumps(checks,indent=2)+'\n')
# Integrate arrived final reports without claiming their missing checks.
p=root/'digestions/steps/09-what-is-still-open.md'; s=p.read_text()
s=s.replace('Its final summary is pending at this snapshot.', 'Its [summary report](../../research/2026-11-14_opus_referee-rainbow/REPORT.md) confirms those verdicts. The packing part uses independent code from a fresh instance of the author\'s model.')
s=s.replace('its final summary is pending.', 'its [summary report](../../research/2026-11-14_opus_referee-rainbow/REPORT.md) accepts the named theorems while leaving P2 open.')
s=s.replace('Its final summary is pending.', 'Its [summary report](../../research/2026-11-14_fable_referee-families/REPORT.md) checks finite sequences and matrix arithmetic but does not check the author\'s all-length transfer code. It also narrows the sign-gauge obstruction to signs on one state\'s incidences; allowing signs on both states remains open.')
s=s.replace('The [new lab campaign]', 'Our fresh full-tier replay also passes; its [output](../../research/2026-11-14_sol_digest-fixes/lab-replay/full.json) retains the counted evidence. The [new lab campaign]')
p.write_text(s,encoding='utf8')
