"""Read numerical certificates directly. Does not import audit.py or author code."""
import json
from pathlib import Path
from itertools import permutations
import networkx as nx
import sympy as sp

P=Path(__file__).resolve().parent
def read(name): return json.loads((P/name).read_text())

lp=read('lp-certificate.json'); x=list(map(sp.Rational,lp['x'])); variables=lp['variables']; white=list(map(int,lp['white_faces']))
assert all(0<=v<=1 for v in x)
assert sum(x)==len(white)-1
for f in {tuple(f) for f,v in variables}:
    assert sum(xx for (ff,v),xx in zip(variables,x) if tuple(ff)==f)==1
for v in {v for f,v in variables}:
    assert sum(xx for (ff,vv),xx in zip(variables,x) if vv==v)==1
for bits in range(1,1<<len(white)):
    S={v for i,v in enumerate(white) if bits>>i&1}
    assert sum(xx for (a,b),xx in zip(lp['dual_edges'],x) if a in S and b in S)<=len(S)-1
M=sp.Matrix([r['row'] for r in lp['independent_active_rows']]); determinant=M.det()
assert M.rows==M.cols==len(x) and determinant!=0
for rec in lp['independent_active_rows']:
    label=rec['label']; val=sum(a*b for a,b in zip(rec['row'],x))
    rhs=0 if label[0]=='zero' else len(label[1])-1 if label[0]=='white_subset' else 1
    assert val==rhs

def tree_complement(faces,root,s):
    verts=set(root)|{v for f in faces for v in f}
    assert len(s)==len(faces) and set(s)==verts-set(root)
    assert all(v in f for f,v in zip(faces,s))
    H=nx.Graph()
    for i,f in enumerate([root]+faces): H.add_edges_from(((0,i),(1,v)) for v in f)
    H.remove_edges_from(((0,i+1),(1,v)) for i,v in enumerate(s))
    return nx.is_tree(H)

c=read('contractions.json')['counterexample_to_reverse_implication'][0]
assert tree_complement(c['large_faces'],c['t0'],c['large_state'])
assert not tree_complement(c['small_faces'],c['t0'],c['small_state'])

local=read('limits-examples.json')['local_prism']; faces=local['bounded_black_faces']; root=local['root']
nonroots=sorted({v for f in faces for v in f}-set(root))
ss=[s for s in permutations(nonroots) if all(v in f for f,v in zip(faces,s))]
assert set(ss)==set(map(tuple,local['states']))
assert len(ss)==3 and sum(tree_complement(faces,root,s) for s in ss)==2

weights=read('weights-leading-zero.json'); poly={int(e):int(c) for e,c in weights['normalized_Z_laurent_coefficients'].items()}
assert poly and sum(poly.values())==0 and sum(e*c for e,c in poly.items())==0
assert all(isinstance(w,int) for f,v,w in weights['spoke_weights'])
assert weights['cmin']==1
factor={}
for bits in range(8):
    exponent=-18+sum(v for j,v in enumerate([7,9,13]) if bits>>j&1)
    factor[exponent]=1 if bits.bit_count()%2==0 else -1
assert factor==poly

census=read('census.json'); alpha=read('alpha-small.json'); glue=read('gluing.json'); strengths=read('strengthenings.json')
assert census['root_count']==alpha['roots']==1206
assert sum(r[4]>0 for r in census['rows'])==880
assert census['D3_ordered_pairs']==3280 and census['images']==9720 and census['partitions']==35664
assert glue['prescriptions_checked']==3618
assert len(strengths)==55 and all(not(r['include_avoid_failures'] or r['P4_failures'] or r['opposite_endpoint_failures']) for r in strengths)

result={'LP_subset_inequalities':2047,'LP_full_rank_active_matrix_determinant':str(determinant),'LP_vertex':True,'degree_four_reverse_implication_refuted':True,'local_rarity_enumeration_rechecked':True,'zero_first_coefficient_nonzero_polynomial':True,'weight_sum_factorization':'exp(-18x)*(1-exp(7x))*(1-exp(9x))*(1-exp(13x))','output_count_sanity_checks':True}
(P/'certificate-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
