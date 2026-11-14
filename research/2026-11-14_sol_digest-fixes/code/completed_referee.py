from pathlib import Path
import json
root=Path.cwd();out=root/'research/2026-11-14_sol_digest-fixes'
p=root/'digestions/steps/09-what-is-still-open.md';s=p.read_text()
s=s.replace('newer one-sided and exception-bijection extensions have only partial review. The [descent referee checkpoint]', 'the completed descent review also supports the qualified one-sided and exception-bijection arguments. The [descent referee]')
s=s.replace('independently reproduces the exceptions and rotation bijection through $V=16$', 'independently reproduces all 7,940 exceptions, the rotation bijection and counting inequality through $V=18$')
s=s.replace('[G.md](../../research/2026-11-14_astra_induction-lemmas/G.md) proves', '[G.md](../../research/2026-11-14_astra_induction-lemmas/G.md), now checked in the [induction review](../../research/2026-11-14_astra_referee-descent/REFEREE-induction.md), proves')
s=s.replace('`PROVED-HERE`, unreviewed. [G.md]', '`PROVED-HERE`, independently AI-refereed. [G.md]')
s=s.replace('is `PROVED-HERE`, still under review.', 'is `PROVED-HERE`, accepted by the completed independent AI referee.')
s=s.replace('The [independent checkpoint]', 'The [completed independent review]')
s=s.replace('confirms C3 only through $V=16$ and replays saved larger traps.', 'confirms C3 through $V=19$ and on all 335,704 pairs of a 40-graph $V=40$ batch. It supplies a complete radius-four witness at graph 3, root {10,16,11}, in [recovered40_0_40.json](../../research/2026-11-14_astra_referee-descent/code/recovered40_0_40.json); the originally selected $V=40$ line had radius three.')
s=s.replace("Of the author's tested potentials, 27 of 28 fail.", "All 27 named alternatives to $q$ now have independently checked counterexamples.")
s=s.replace('`PROVED-HERE`, under review. The three-height identity', '`PROVED-HERE`, independently AI-refereed. The three-height identity')
s=s.replace('and is `PROVED-HERE`, under review.', 'and is `PROVED-HERE`, supported by the completed independent review.')
s=s.replace('The full Hamiltonian search additionally needs explicit composition or a checked closure citation.', 'Extension to full Hamiltonian search needs polynomial-time decomposition, flow and reconstruction plus the PPADS closure citation. The referee checked that citation in an author/publisher abstract but could not access its full theorem statement.')
p.write_text(s,encoding='utf8')
p=root/'digestions/route-map/routes.py';s=p.read_text();s+='''
# Completed descent referee arrived at the final report scan.
_upd('N.11',text='C3 is open. Author census checks 193,623,384 pairs through V=23, plus all pairs on 230 random graphs through V=80 and sampled starts through V=200. Three capped V=300 starts remain undecided. Independent referee verifies all roots and pairs through V=19 and all 335,704 pairs of a 40-graph V=40 batch. The larger author census is not thereby independently replayed.',where='des/REPORT.md; des/data/census_summary.json; des/data/census_23_part0of8.txt; rd/REPORT.md; rd/code/c3_6_19.json; rd/code/summary40_0_40.json',review={'state':'refereed','by':[FOLDERS['rd']],'verdict':'Finite C3 checks independently replayed through V=19 and on the named V=40 batch. C3 remains a conjecture; author V=23 and larger samples retain their own scope.'})
for rid in ('N.descent-structure','N.three-heights','N.PPADS'):
    _upd(rid,where='+; rd/REFEREE-descent.md; rd/INTEGRATION.md',review={'state':'refereed','by':[FOLDERS['rd']],'verdict':'Structural descent identities and conditional sink reduction supported, with scope and encoding qualifications; no human check.'})
_upd('N.lookahead',where='+; rd/REPORT.md; rd/code/recovered40_0_40.json',cex='Strict q-descent fails first at V=16. Lookahead two fails at V=21, with minimality from author census. Lookahead three fails at recovered V=40 graph 3, root {10,16,11}; saved V=60 also has escape radius four. The original selected V=40 line has radius three. Lookahead four remains open.')
_upd('N.height-ties',where='+; rd/REPORT.md; rd/code/all_potentials.json; rd/code/recovered40_0_40.json',text='The 27 explicitly named alternative potentials have independent counterexamples, including repaired complete area/size certificates. This refutes neither every potential involving cover count nor every bounded local rule.',review={'state':'refereed','by':[FOLDERS['rd']],'verdict':'All 27 named alternative potentials independently refuted; universal overclaims rejected.'})
for rid in ('U.G-partial','U.ML2'):
    _upd(rid,where='+; rd/REFEREE-induction.md; rd/REPORT.md',review={'state':'refereed','by':[FOLDERS['rd']],'verdict':'Named structural and repair statements supported with outer-forest and sufficient-condition qualifications. General G and X remain open; same model family as induction author, independent code.'})
_upd('U.ML2',text='Induction X: when both opposite contractions have good states, at least one has a nonexceptional state whose unique lift or three-face rotation succeeds. This is sufficient for induction, not a converse equivalent to existence upstairs. Independent referee reproduces all 7,940 exceptions through V=18, the rotation bijection, counting inequality, corner avoidance and global half bound; none of those finite checks proves general X.')
''';p.write_text(s,encoding='utf8')
p=root/'labyrinth/README.md';s=p.read_text().replace('the independent descent referee currently confirms only through 16', 'the completed independent descent referee confirms through 19 and on the full named 40-vertex batch');p.write_text(s,encoding='utf8')
# Extract all finite numbers newly quoted from the referee outputs.
nums=json.loads((out/'numbers.json').read_text());d=json.loads((root/'research/2026-11-14_astra_referee-descent/code/c3_6_19.json').read_text());nums['descent_referee_census_max_V']=max(r['V'] for r in d)
r=json.loads((root/'research/2026-11-14_astra_referee-descent/code/summary40_0_40.json').read_text());nums['descent_referee_random_batch']=r
(out/'numbers.json').write_text(json.dumps(nums,indent=2)+'\n')
