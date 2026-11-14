"""Independent check of Remark 6.7, one forced map per black-inner separator."""
from check import graphs,split_forests,BASE
import itertools,collections,json
total=0
for v in range(6,13):
    for rot,faces in graphs(v):
        ef=collections.defaultdict(list)
        for t,f in enumerate(faces):
            for e in itertools.combinations(f,2):ef[tuple(sorted(e))].append(t)
        for t0 in range(len(faces)):
            R=set(faces[t0]);color={t0:0};q=[t0]
            for t in q:
                for e in itertools.combinations(faces[t],2):
                    for z in ef[tuple(sorted(e))]:
                        if z not in color:color[z]=1-color[t];q.append(z)
            A=[t for t in range(len(faces)) if not color[t] and t!=t0]
            whites=[t for t in range(len(faces)) if color[t]];wi={t:i for i,t in enumerate(whites)}
            def we(t,x):return tuple(wi[z] for y in faces[t] if y!=x for z in ef[tuple(sorted((x,y)))] if z!=t)
            for tri in itertools.combinations(range(v),3):
                if not all(tuple(sorted(e)) in ef for e in itertools.combinations(tri,2)):continue
                todo=set(range(v))-set(tri);comps=[]
                while todo:
                    qq=[todo.pop()];comp=set(qq)
                    for x in qq:
                        for y in rot[x]:
                            if y in todo:todo.remove(y);comp.add(y);qq.append(y)
                    comps.append(comp)
                if len(comps)<2:continue
                inside=next(c for c in comps if not(c&R))
                inner=[next(t for t in ef[tuple(sorted(e))] if set(faces[t])&inside) for e in itertools.combinations(tri,2)]
                if any(color[t] for t in inner):continue
                u={t:faces[t][0] for t in A}
                for t in inner:u[t]=next(x for x in faces[t] if x in tri)
                edges=[we(t,x) for t in A for x in faces[t] if x!=u[t]]
                assert not split_forests(edges,len(whites))
                total+=1
(BASE/'necessity.json').write_text(json.dumps(dict(command='python research/2026-11-14_sol_referee-sign-free/necessity.py',forced_obstructed_maps=total),indent=2))
print(total)
