from pathlib import Path
import json,re
root=Path.cwd(); folder=root/'research/2026-11-14_sol_digest-fixes'
p=root/'digestions/route-map/routes.py'; s=p.read_text(encoding='utf8')
# Replace the malformed induction registrations at their source, not in generated prose.
a=s.index('# Retain all thirteen failed induction schemes'); b=s.index("add('U.loads-dead'",a)
claims=json.loads((folder/'induction-prose.json').read_text())
block='# Failed induction rules. Witness IDs use the original plantri ordering.\n'
for rid,claim,witness in claims:
 review='R8 coefficient comparison is author-only.' if rid=='R8' else 'R13 independently checked only on the octahedron.' if rid=='R13' else 'Specified witness independently replayed in the completion referee.'
 block+=f"add('U.ind-{rid}','U',{('induction '+rid+': '+claim)!r},'REFUTED','ind','ind/data/failed_inductions.json; ri/REFEREE.md',{(claim+' '+review)!r},'induction',cex={(witness+'.')!r},lesson='The failed statement cannot be used as the induction hypothesis; retain the qualified lift and rotation criteria.')\n"
s=s[:a]+block+'\n'+s[b:]
s=s.replace('extremes of the whole matching lattice fail at 10 vertices',"extremes of Propp's state clock lattice fail at V=10")
s=s.replace('C2 is false. Both true lattice extremes can have no good pair. Independent exhaustive minimum-order check finds 26 failures at V=18 and none below.',"C2 is false. Both extremes of Felsner's pair lattice can carry no good pair; the independent witness has V=18. This is distinct from Propp's state clock lattice, where an extreme can lack a partner at V=10.")
s=s.replace('49,325,864 pairs through V=22','193,623,384 pairs through V=23')
s=s.replace('Independent earlier reachability replay only through V=16.','Independent descent referee checkpoint reproduces C3 through V=16; larger-range checks and proof verdicts remain in progress.')
s=s.replace('reference-engine radius-four certificate at V=60.','a reference-engine escape-radius-four certificate at V=60 also refutes radius-three lookahead. Radius-four lookahead is open.')
s += '''
# Digest-fixes integration. Current paper recovery and independently reviewed Lean scope.
FOLDERS.update(rd='research/2026-11-14_astra_referee-descent',
               rr='research/2026-11-14_opus_referee-rainbow',
               rf='research/2026-11-14_fable_referee-families',
               tests='research/2026-11-14_sol_lab-tests')
for tag in ('rd','rr','rf','tests'):
    REVIEW[tag]={'state':'unreviewed'}
for waypoint in WAYPOINTS:
    if waypoint['id']=='FP':
        waypoint.update(name='Good pair / good state',what='A good state has Q_s a forest with one root in each component, equivalently S_s=Q_s union {ao,bo} is a spanning tree of T. With a partner, acyclicity suffices; without one it does not. A good pair has a good second state.')
    if waypoint['id']=='IT':
        waypoint.update(name='Spanning tree S_s of T',what='The opposite edges Q_s together with ao and bo, two sides of the root face abo, form a spanning tree of T. Paper Lemma 3.5.')
    if waypoint['id']=='WT':
        waypoint.update(name='Tree of faces Y_s',what='Faces of T joined across edges outside S_s form the dual spanning tree Y_s. Every bounded black face has degree two; t0 has degree one. Paper Lemma 3.6.')
    if waypoint['id']=='SE':
        waypoint.update(what='Root Y_s at t0. Each black face selects the side shared with its child. This gives one selected side per face, including e0 at t0. Its crossing edges form a perfect matching in G.')
for step in STEPS:
    if step['id']=='R':
        step.update(title='Good state gives S_s',must='The forest Q_s has one root per component; adding ao and bo makes S_s a spanning tree of T.',freedom='Paper Lemma 3.5. The older spoke-complement tree is an equivalent presentation.')
    if step['id']=='E':
        step.update(title='Dual tree of faces',must='The edges outside S_s join faces into a tree Y_s by planar tree/cotree duality.',freedom='Paper Lemma 3.6; older routes suppress black nodes to obtain a white-face tree.')
    if step['id']=='E2':
        step.update(title='Root Y_s at t0 and select',must='Each black face selects the side shared with its child. Every face is matched once across its selected side.',freedom='Paper Lemma 3.6 defines P_s; the formal proof needs only a weaker existence statement.')
_upd('N.x14',label='strict q-descent',text='Every non-good pair has an immediately q-decreasing D-swap or Q-reversal.',cex='V=16, least by author census and independently replayed through V=16.',where='des/DESCENT.md; rd/REPORT.md',lesson='Plateaus are necessary. This concerns q(s), not rainbow black-face excess.')
_upd('N.lookahead',text='For a fixed lookahead L, every non-good pair has a lower-q pair within L exchanges. L=1,2,3 are refuted; L=4 and unbounded escape radius remain open.')
_upd('N.11',where='+; rd/REPORT.md',review={'state':'under-review','by':[FOLDERS['rd']],'verdict':'Checkpoint independently verifies all pairs through V=16; larger campaign and structural proofs remain under review.'})
_upd('G2.devices',where='proofs/lean/README.md; lc/REPORT.md; lc/FAITHFULNESS.md; lc/REACHABILITY.md',text='Independently rebuilt and checked: upstream theorem, submitted devices and real-sign finite-difference replacement main. Only propext, Classical.choice and Quot.sound occur in the advertised axiom reports. Qualifications: TODO T5 surjectivity is false; full general paper Lemma 4.5 is not formalised; generic Mathlib polynomial dependencies remain; heights use an abstract flow whose translation from paper face paths is unformalised.',review={'state':'refereed','by':[FOLDERS['lc']],'verdict':'Independent fresh rebuild and statement/dependency check completed, with four explicit qualifications. No human check.'})
_upd('U.rainbow',where='+; rr/REFEREE-rainbow.md',text='Step R gives a point-rainbow tree iff no black-inner separating triangle exists, by Rado and Euler. Theorem S gives unique-factor completion. Independent rainbow referee accepts these proofs with corrections; final summary pending.',review={'state':'refereed','by':[FOLDERS['rr']],'verdict':'Detailed referee accepts R and S with stated corrections; final summary pending.'})
for rid in ('U.evict','U.rainbow-local'):
    _upd(rid,where='+; rr/REFEREE-rainbow.md',review={'state':'refereed','by':[FOLDERS['rr']],'verdict':'Detailed referee accepts unique exchange and resident-eviction results; final summary pending.'})
_upd('U.rainbow-strict',where='+; rr/REFEREE-rainbow.md',text='Every positive-black-excess rainbow tree has an immediately black-excess-decreasing exchange. This is distinct from strict q-descent on pairs.',cex='V=8, independently replayed by the rainbow referee.',review={'state':'refereed','by':[FOLDERS['rr']],'verdict':'Strict black-excess descent counterexample independently reproduced.'})
_upd('U.packing',where='+; rr/REFEREE-packing.md',review={'state':'refereed','by':[FOLDERS['rr']],'verdict':'Ordinary packing and named one-sided results checked in detailed report; same model as author, independent code; final summary pending.'})
add('N.three-heights','N','conserved three-height identity','PROVED-HERE','des','des/PROOFS.md; rd/REPORT.md','Three heights for r, s and the unused-corner map have constant sum. A move transfers enclosed white area between two heights. This is not a progress potential; proof under review.','topology',review={'state':'under-review','by':[FOLDERS['rd']],'verdict':'Checkpoint does not yet give a final verdict on this identity.'})
add('G2.lab-tests','G2','counted reference-lab regression','COMPUTED','tests','tests/REPORT.md; tests/full.json; tests/quick.json','Both counted tiers pass. Full census covers all facial roots through V=14 plus saved larger fixtures; independent complete state/pair/sign checks through V=12. Relative heights and moments pass; absolute heights may shift by path constants, and raw marked counts depend on drawing. Finite checks, not a general proof.','count')
'''
p.write_text(s,encoding='utf8')
# Correct our summary's radius versus lookahead distinction.
p=root/'digestions/steps/09-what-is-still-open.md'; s=p.read_text()
s=s.replace('radius three fails at $V=40$ and radius four at $V=60$, without minimum-order claims for the last two. These finite radii fail; unbounded escape radius is still open.', 'radius three fails at $V=40$, without a minimum-order claim. The saved $V=60$ pair also has escape radius four, which refutes lookahead three, not four. Lookahead four and unbounded escape radius remain open.')
p.write_text(s,encoding='utf8')
