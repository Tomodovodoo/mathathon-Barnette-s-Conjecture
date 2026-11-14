from independent import *

def glue_into_face(outer,inner,face):
    """Oriented connected sum, removing a white outer face and black inner root."""
    f=tuple(face);g=inner.faces[inner.rootid]
    ident={g[0]:f[0],g[1]:f[2],g[2]:f[1]}
    nxt=max(outer.rot)+1
    for v in sorted(inner.rot):
        if v not in ident:ident[v]=nxt;nxt+=1
    faces=[q for q in outer.faces if set(q)!=set(f)]
    faces += [tuple(ident[v] for v in q) for i,q in enumerate(inner.faces) if i!=inner.rootid]
    result=Instance(rotation_from_faces(faces),outer.faces[outer.rootid])
    result.gluing_ident=ident
    return result

if __name__=='__main__':
    d=json.loads((ROOT/'research/2026-11-14_opus_conjectures/data/c2_counterexample_V18.json').read_text())
    rot,root=parse_text(d['line']);I=Instance(rot,root)
    # Use a white face disjoint from the outer root, selected by a fixed ordering.
    f=next(I.faces[j] for j in sorted(I.white) if not (set(I.faces[j])&I.R))
    K=glue_into_face(I,I,f)
    result=lattice_analysis(K,detail=True)
    result.update(rotation=K.rot,gluing_face=f,source_root=root)
    us=list(I.factors());phis=[I.potential(u,us[0]) for u in us]
    fj=next(j for j,q in enumerate(I.hfaces) if set(q)&set(I.rot)==set(f))
    result['gluing_face_H0_id']=fj
    result['gluing_face_potential_values']=[p[fj] for p in phis]
    assert len(set(result['gluing_face_potential_values']))==1
    save('R2_glued_V33.json',result)
    print({k:v for k,v in result.items() if k not in ('entries','rotation','faces_A','hfaces','join_order')})
    assert not result['R2']
