from pathlib import Path
p=Path('labyrinth/make_frontier.py');s=p.read_text(encoding='utf8')
s=s.replace('for v in (17, 18, 23, 28, 33):','for v in (*range(17,25), 28, 33):').replace('"beyond every enumeration in the repository"','"Beyond the independently cross-checked full invariant-value frontier; newer censuses track C1, not the complete value spectrum"')
s+='''
# Record statistic coverage separately from invariant-value resolution. Larger C1
# censuses do not enumerate the whole admissible TM-count spectrum in this file.
fp=LAB/'frontier.json'
f=json.loads(fp.read_text())
f['statistic_coverage']=[
 {'statistic':'complete realized spectrum of TM counts, states and pairs cross-check','class':'all facial roots of Eulerian triangulations','through_dual_order':16,'tier':'T3','by':['fable_route-combinatorics','sol_route-algebra','astra_referee-combinatorics'],'source':'labyrinth/frontier_crosscheck.json'},
 {'statistic':'C1 and equality iff one factor; TM and pair totals','class':'all facial roots of Eulerian triangulations','through_dual_order':22,'tier':'T3','by':['opus_conjectures','sol_referee-conjectures'],'source':'research/2026-11-14_sol_referee-conjectures/data/fast_census_summary.json','note':'independent complete implementations agree; not imported as full TM value spectrum'},
 {'statistic':'C1, equality iff one factor and c_min distribution','class':'4-connected Eulerian triangulations, every facial root','through_dual_order':24,'rooted_instances':23824742,'tier':'T4','review':'under-review','by':['astra_cycle-covers'],'source':'research/2026-11-14_astra_cycle-covers/data/census.json','note':'inherited C engine; no independent order-24 replay; maximum c_min=6 at order 23'},
 {'statistic':'ML1 pair-preserving merge existence','class':'separator-free rooted triangulations','through_dual_order':19,'tier':'T4','by':['fable_induction-completion'],'source':'research/2026-11-14_fable_induction-completion/MISSING-LEMMA.md'},
 {'statistic':'rainbow exchange X, all rainbow trees','class':'all feasible facial roots','through_dual_order':17,'tier':'T4','by':['fable_referee-topology'],'source':'research/2026-11-14_fable_referee-topology/REPORT.md'}]
fp.write_text(json.dumps(f,indent=1))
'''
p.write_text(s,encoding='utf8')
p=Path('digestions/route-map/routes.py');s=p.read_text(encoding='utf8');s+='''
add('D.C1-census','D','independent C1 census through V=22','COMPUTED','rc','rc/code/count.cpp; rc/data/fast_census_summary.json; rc/REFEREE.md','All 9,531,638 facial roots through V=22, 4,656,948 feasible: C1 and equality iff one factor pass. Independent Python and C++ implementations agree through V=18; author and referee totals agree through V=22.','count',tier='T3',review={'state':'refereed','by':[FOLDERS['rc']],'date':'2026-11-14','verdict':'Independent replay of submitted C1 computation; human check pending.'})
''';p.write_text(s,encoding='utf8')
