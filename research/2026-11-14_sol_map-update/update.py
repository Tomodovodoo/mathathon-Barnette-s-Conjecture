from pathlib import Path
p=Path('labyrinth/seed.py')
s=p.read_text(encoding='utf8')
s=s.replace('n.update(kind="evidence", tier="T4", status="computed", evidence=[expand(r["where"])])','n.update(kind="exhaustive" if r.get("tier")=="T3" else "evidence", tier=r.get("tier","T4"), status="computed", evidence=[expand(r["where"])], review=r.get("review", {"state":"unreviewed"}))')
needle='(LAB / "knowledge.json").write_text'
idx=s.index(needle)
s=s[:idx]+'''# Current door statements supersede the first map's tests. Keep stable ids for events.
updates = {
 'q.canonical': ('No universal canonical forest pair is known. C2 fails first at V=18; R2 fails at V=33. The signed sum is not a rank polynomial of the base lattice.', 'Test the separator-free restriction of R2; keep direction search separate from testing a pair.'),
 'q.tm-lower': ('C1 is open. Independent all-root census through V=22; separator-free evidence through V=24. One cover implies equality; converse open.', 'Exclude the exceptional two-cover overlap; then treat more covers.'),
 'q.disk': ('Signed-angle Gauss-Bonnet derivation independently AI-refereed with boundary corrections. No human check.', 'Human-check the corrected flat-angle proof.'),
 'q.li-b': ('A complete marked-involution writeup now exists in proofs/involutions/, under independent AI review.', 'Finish the independent referee and reconcile distinct-mark conventions.'),
 'q.surface': ('Rooted cardinality fails by 2g. Root-free Heawood has odd-cycle cancellation but identically zero polynomial.', 'Find a replacement for spherical nonvanishing; compare the six trisum signatures.'),
 'q.human': ('No human-checked claim is recorded. Claim-specific AI reviews are in the route nodes; new referee discoveries remain unreviewed.', 'Check the merged exposition and revised primal sign normalization.')}
for node in nodes:
    if node['id'] in updates:
        node['statement'], node['next'] = updates[node['id']]
        node['why'] = node['statement']
        if node['id']=='q.disk': node['status']='answered'
''' + s[idx:]
# Include update events before append-only write.
idx=s.index('E.sort(key=')
s=s[:idx]+'''for typ, rid in [('refuted','D.ext2'),('reviewed','D.7'),('computed','D.cover-census'),('proved','D.covers'),('refuted','U.lift-dead'),('proved','U.induction'),('proposed','U.G'),('proposed','U.ML2'),('proved','U.rainbow'),('refuted','U.walk-dead'),('refuted','U.mean-dead'),('proposed','U.packing'),('proved','G2.pf'),('refuted','N.heawood'),('documented','G2.main'),('documented','G2.inv')]:
    rr=next(r for r in RT.ROUTES if r['id']==rid)
    ev('2026-11-14T15:%02d:00Z' % (len(E)-53), typ, 'Map refresh, attributed report integration: '+rr['label']+'. '+rr['text']+' New proofs remain unreviewed unless a named review says otherwise. Timestamp is bookkeeping.', [nid(rr)], [expand(rr['where'])])
''' + s[idx:]
# Replace history block, run after all entries including manuscript row are present.
a=s.index('prior_path = LAB / "sota.json"'); b=s.index('(LAB / "sota.json").write_text',a)
s=s[:a]+'''S['entries'].append(row('new-presentations',G1,'Written proof routes','Three current written routes: merged dual exposition, revised primal proof, marked involutions. Upstream Lean proof built locally.','Merged and involution texts under AI review; earlier primal version AI-refereed, revision self-audited; M4 phase disagreement explicit. No human check.','partial',['p.G2.main','p.G2.primal','p.G2.inv','c.G2.c'],[]))
for entry in S['entries']:
    if entry['id']=='canonical':
        entry.update(result='No canonical rule known. C2 false first at V=18; extreme-or-irreducible R2 false at V=33. R1/R3/R5 witnesses at V=24/60/70; gluing also defeats R3/R5 at V=33.',status='Independent AI referee and two V=33 implementations; no human check.',kind='refuted',refs=['k.D.7','x.D.ext2'])
    if entry['id']=='review':
        entry.update(result='Claim-specific AI referee states recorded on routes. New referee theorems remain T2 unreviewed. None human-checked.',status='See named review objects; revised primal M4 disagreement requires re-referee.')
    if entry['id']=='tm-lower' or entry['cls']=='Number of tree matchings':
        entry.update(result='Proved lower bound 2 c_min; C1 conjectures 2^c_min. Independent all-root census through V=22; separator-free tests through V=24. One-cover equality proved; converse open.',status='2 c_min AI-refereed; C1 finite census, not a theorem.')
for id,cls,rid in [('induction','Unsigned contraction induction','U.ML2'),('rainbow','Rainbow exchange','U.7h'),('packing','Two-tree packing','U.packing'),('covers','Meaning and range of c_min','D.covers'),('census24','Separator-free C1 census','D.cover-census'),('pfaffian','Pfaffian corollary','G2.pf')]:
    r=next(r for r in RT.ROUTES if r['id']==rid)
    S['entries'].append(row(id,G2,cls,r['text'],r['status']+'; new claims unreviewed, human check pending','computed' if r['status']=='COMPUTED' else 'conjecture' if r['status']=='CONJECTURE' else 'partial',[nid(r)],[]))
prior_path=LAB/'sota.json'
prior=json.loads(prior_path.read_text(encoding='utf8')) if prior_path.exists() else {'entries':[]}
prior_by_id={r['id']:r for r in prior['entries']}
for r in S['entries']:
    old_row=prior_by_id.get(r['id'])
    if old_row:
        r['previous']=old_row.get('previous',[]).copy()
        if old_row['result']!=r['result'] or old_row['status']!=r['status']:
            r['previous'].append({'date':DAY,'was':old_row['result'],'status':old_row['status']})
''' + s[b:]
p.write_text(s,encoding='utf8')
# Matrix header labels must fit each column.
p=Path('digestions/route-map/routes.py'); s=p.read_text(encoding='utf8').replace("'probability, positive measures'","'probability, positive measures'")
p.write_text(s,encoding='utf8')
