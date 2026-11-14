from check import graphs,forest,BASE
import itertools,json,collections
rot,faces=next(g for i,g in enumerate(graphs(16)) if i==27)
t0=next(i for i,f in enumerate(faces) if set(f)=={0,1,2})
R=set(faces[t0]);X=sorted(set(range(16))-R)
ef=collections.defaultdict(list)
for i,f in enumerate(faces):
    for e in itertools.combinations(f,2):ef[tuple(sorted(e))].append(i)
color={t0:0};q=[t0]
for t in q:
    for e in itertools.combinations(faces[t],2):
        for z in ef[tuple(sorted(e))]:
            if z not in color:color[z]=1-color[t];q.append(z)
A=[t for t in range(len(faces)) if not color[t] and t!=t0]
states=[]
def rec(i,s):
    if i==len(A):states.append(tuple(s));return
    for x in faces[A[i]]:
        if x not in R and x not in s:rec(i+1,s+[x])
rec(0,[])
factors=set()
for i,s in enumerate(states):
    for r in states[i+1:]:
        if all(x!=y for x,y in zip(s,r)):
            factors.add(frozenset((t,x) for j,t in enumerate(A) for x in (s[j],r[j])))
out=[]
for F in factors:
    adj=collections.defaultdict(list)
    for t,x in F:adj['t'+str(t)].append('x'+str(x));adj['x'+str(x)].append('t'+str(t))
    todo=set(adj);cycles=0
    while todo:
        qq=[todo.pop()];cycles+=1
        for x in qq:
            for y in adj[x]:
                if y in todo:todo.remove(y);qq.append(y)
    contained=[s for s in states if all((t,x) in F for t,x in zip(A,s))]
    ok=[]
    for s in contained:
        qe=[tuple(x for x in faces[t] if x!=y) for t,y in zip(A,s)]
        ok.append(forest(qe+[(16,r) for r in R],17))
    out.append(dict(cycles=cycles,states=len(contained),good=sum(ok),choices=[list(s) for s in contained],incidences=sorted(F)))
assert len(out)==3 and sum(z['good'] for z in out)==12
bad=[z for z in out if not z['good']]
assert len(bad)==1 and bad[0]['cycles']==1 and bad[0]['states']==2
result=dict(command='python research/2026-11-14_sol_referee-sign-free/witness_detail.py',faces=faces,black=A,root=faces[t0],covers=out)
(BASE/'witness-detail.json').write_text(json.dumps(result,indent=2))
print([(z['cycles'],z['states'],z['good']) for z in out])
