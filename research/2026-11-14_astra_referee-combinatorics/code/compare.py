"""Compare orientation-independent rooted profiles with the submitted output."""
from check import *
ours=json.loads((HERE/'up_to_16.json').read_text())
theirs=json.loads((AUTHOR/'data/rows_v16.json').read_text())
def own(r):return r['V'],r['states'],r['pairs'],r['tree_matchings'],r['cmin'],r['hc']
def other(r):return r['V'],r['states'],r['pairs'],r['trees'],r['cmin'],r['hams']
assert Counter(map(own,ours['rows']))==Counter(map(other,theirs))
paired=[r for r in ours['rows'] if r['pairs']]
out={'command':' '.join(sys.argv),'rooted_profiles_equal':True,'fields':['V','states','pairs','tree_matchings','cmin','Hamiltonian_cycles'],
     'roots_with_pairs':len(paired),'nonimage_HC_on_roots_with_pairs':sum(r['nonimage_HC_states'] for r in paired),
     'totals':ours['totals'],'classes':ours['classes'],'seconds_main_run':ours['seconds']}
assert out['nonimage_HC_on_roots_with_pairs']==176726
(HERE/'comparison.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
