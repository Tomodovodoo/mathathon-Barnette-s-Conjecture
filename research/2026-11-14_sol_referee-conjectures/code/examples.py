from independent import *

def bipyramid(p):
    faces=[]
    for i in range(p):faces.extend([(p,i,(i+1)%p),(p+1,(i+1)%p,i)])
    return rotation_from_faces(faces)

def main():
    out={}
    for label,p in [('octahedron',4),('hexagonal_prism_dual',6)]:
        rot=bipyramid(p);out[label]=lattice_analysis(Instance(rot,(p,0,1)),detail=True)
    e=json.loads((ROOT/'research/2026-11-14_fable_figures-review/search_example_13.json').read_text())[0]
    rot=rotation_from_faces(e['faces'])
    # Manuscript example A excludes face [0,5,4], not search fixture's first t0.
    I=Instance(rot,(0,5,4));wanted=json.loads((ROOT/'research/2026-11-14_opus_manuscript-merge/example.json').read_text())
    assert {frozenset(f) for f in I.A}=={frozenset(f) for f in wanted['faces_A']}
    out['running_V13']=lattice_analysis(I,detail=True)
    d=json.loads((OUT/'v18.json').read_text());out['witness_V18']=d
    save('examples.json',out)
    for label,d in out.items():print(label,{k:d[k] for k in ('lattice','pairs','TM','rank_polynomial','signed','extreme_tree_pairs')})

if __name__=='__main__':main()
