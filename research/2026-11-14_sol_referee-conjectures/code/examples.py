from independent import *
import sympy as sp

def bipyramid(p):
    faces=[]
    for i in range(p):faces.extend([(p,i,(i+1)%p),(p+1,(i+1)%p,i)])
    return rotation_from_faces(faces)

def main():
    out={};instances={}
    for label,p in [('octahedron',4),('hexagonal_prism_dual',6)]:
        rot=bipyramid(p);instances[label]=Instance(rot,(p,0,1));out[label]=lattice_analysis(instances[label],detail=True)
    e=json.loads((ROOT/'research/2026-11-14_fable_figures-review/search_example_13.json').read_text())[0]
    rot=rotation_from_faces(e['faces'])
    # Manuscript example A excludes face [0,5,4], not search fixture's first t0.
    I=Instance(rot,(0,5,4));wanted=json.loads((ROOT/'research/2026-11-14_opus_manuscript-merge/example.json').read_text())
    assert {frozenset(f) for f in I.A}=={frozenset(f) for f in wanted['faces_A']}
    out['running_V13']=lattice_analysis(I,detail=True)
    instances['running_V13']=I
    d=json.loads((OUT/'v18.json').read_text());out['witness_V18']=d
    source=json.loads((ROOT/'research/2026-11-14_opus_conjectures/data/c2_counterexample_V18.json').read_text())
    instances['witness_V18']=Instance(*parse_text(source['line']))
    z=sp.Symbol('z')
    for label,d in out.items():
        I=instances[label];weights=I.spoke_weights()
        for e in d['entries']:
            cs=I.cycles(e['u']);s=[None]*I.n;areas=[]
            for c in cs:
                delta=sum(1 if I.A[k][(I.A[k].index(a)+1)%3]==b else -1 for a,b,k in c)
                area=0
                for a,b,k in c:
                    tail,head=(a,b) if delta==3 else (b,a)
                    s[k]=head;area+=weights[k,tail]-weights[k,head]
                assert area>0;areas.append(area)
            b=sum(weights[k,v] for k,v in enumerate(s));poly={b:(-1)**((I.n-len(cs))//2)}
            for a in areas:
                nxt=co.Counter()
                for k,v in poly.items():nxt[k+a]+=v;nxt[k]-=v
                poly=nxt
            expected={k:v for k,v in poly.items() if v}
            assert expected=={int(k):v for k,v in e['signed'].items()}
        p={int(k):v for k,v in d['signed'].items()};shift=-min(p)
        expr=sum(v*z**(k+shift) for k,v in p.items());m=d['c_min']
        for j in range(m):assert sum(v*sp.binomial(k,j) for k,v in p.items())==0
        leading=sum(v*sp.binomial(k,m) for k,v in p.items());assert leading
        d.update(normalizing_exponent=shift,normalized_factorization=str(sp.factor(expr)),
                 lowest_order=m,leading_coefficient=int(leading),fibre_product_formula_checked=True)
    save('examples.json',out)
    for label,d in out.items():print(label,{k:d[k] for k in ('lattice','pairs','TM','rank_polynomial','signed','extreme_tree_pairs')})

if __name__=='__main__':main()
