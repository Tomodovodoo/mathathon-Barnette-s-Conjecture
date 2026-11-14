"""Run after check.py, from root: python research/2026-11-14_sol_referee-sign-free/regions.py"""
from check import graphs, forest, BASE
import collections,itertools,json,random,time
counts=collections.Counter();rng=random.Random(14112026);begin=time.time()
for v in range(6,13):
    for rot,faces in graphs(v):
        ef=collections.defaultdict(list)
        for i,f in enumerate(faces):
            for e in itertools.combinations(f,2):ef[tuple(sorted(e))].append(i)
        for t0 in range(len(faces)):
            color={t0:0};q=[t0]
            for t in q:
                for e in itertools.combinations(faces[t],2):
                    for z in ef[tuple(sorted(e))]:
                        if z not in color:color[z]=1-color[t];q.append(z)
            black=[t for t in color if not color[t]];white=[t for t in color if color[t]]
            bi={t:v+i for i,t in enumerate(black)};wi={t:i for i,t in enumerate(white)}
            spokes=[(bi[t],x) for t in black for x in faces[t]]
            dual=[tuple(wi[z] for y in faces[t] if y!=x for z in ef[tuple(sorted((x,y)))] if z!=t) for t in black for x in faces[t]]
            # Random spoke sets of exactly dual-tree cardinality; no discarded failures.
            for repeat in range(2000):
                ids=set(rng.sample(range(len(spokes)),v-3))
                assert forest([e for i,e in enumerate(spokes) if i not in ids],v+len(black))==forest([dual[i] for i in ids],len(white))
                counts['duality_sets']+=1
            # Build actual regions by merging T-faces across edges absent from K.
            for mask in range(1,1<<v):
                U={x for x in range(v) if mask>>x&1};p=len(U)
                if p<3:continue
                seen={next(iter(U))};q=list(seen)
                for x in q:
                    for y in rot[x]:
                        if y in U and y not in seen:seen.add(y);q.append(y)
                if seen!=U:continue
                par=list(range(len(faces)))
                def find(a):
                    while par[a]!=a:a=par[a]
                    return a
                m=0
                for (a,b),(s,t) in ef.items():
                    if a in U and b in U:m+=1
                    else:par[find(s)]=find(t)
                groups=collections.defaultdict(list)
                for t in range(len(faces)):groups[find(t)].append(t)
                ds=collections.Counter()
                for (a,b),ts in ef.items():
                    if a in U and b in U:
                        for t in ts:ds[find(t)]+=1
                terms=[]
                for group,ts in groups.items():
                    if len(ts)==1 and set(faces[ts[0]])<=U:continue
                    d=ds[group];beta=sum(1 if color[t]==0 else -1 for t in ts)
                    if d>=4:assert beta<=d-4
                    elif d==3:assert beta in (-1,1)
                    else:raise AssertionError((v,t0,U,d))
                    terms.append(beta-d+4);counts['regions']+=1
                b=sum(set(faces[t])<=U for t in black)
                assert 2*(m-b-(2*p-4))==sum(terms)
                counts['identity_6_2_sets']+=1
        print(v,dict(counts),round(time.time()-begin,1),flush=True)
(BASE/'regions.json').write_text(json.dumps(dict(command='python research/2026-11-14_sol_referee-sign-free/regions.py',counts=dict(counts)),indent=2))
