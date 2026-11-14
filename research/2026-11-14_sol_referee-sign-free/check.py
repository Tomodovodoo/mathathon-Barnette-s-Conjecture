"""Independent referee census. No imports from author or lab.
Run from repository root: python research/2026-11-14_sol_referee-sign-free/check.py
"""
import collections, itertools, json, pathlib, subprocess, time
BASE = pathlib.Path(__file__).resolve().parent
ROOT = BASE.parent.parent
COUNTS = collections.Counter()

def graphs(v):
    p = subprocess.run([str(ROOT/'workings/barnette_lab/vendor/plantri.exe'), '-b', '-a', str(v)], capture_output=True, check=True)
    for line in p.stdout.decode().splitlines():
        if not line.strip(): continue
        n, text = line.split()
        rot = [[ord(c)-97 for c in s] for s in text.split(',')]
        seen, faces = set(), []
        for a in range(int(n)):
            for b in rot[a]:
                if (a,b) in seen: continue
                f=[]; x,y=a,b
                while (x,y) not in seen:
                    seen.add((x,y)); f.append(x)
                    x,y=y,rot[y][(rot[y].index(x)+1)%len(rot[y])]
                assert len(f)==3
                faces.append(tuple(f))
        yield rot,faces

def forest(edges, n):
    p=list(range(n))
    def find(a):
        while p[a]!=a: a=p[a]
        return a
    for a,b in edges:
        a,b=find(a),find(b)
        if a==b:return False
        p[a]=b
    return True

def split_forests(edges,n):
    # Exact graphic matroid union, augment by moving a cycle edge to the other forest.
    parts=[set(),set()]
    def path(part,a,b):
        adj=[[] for _ in range(n)]
        for i in part:
            u,v=edges[i];adj[u].append((v,i));adj[v].append((u,i))
        q=[a]; prev={a:None}
        for u in q:
            if u==b:break
            for v,i in adj[u]:
                if v not in prev:prev[v]=(u,i);q.append(v)
        if b not in prev:return None
        out=[]
        while b!=a:
            b,i=prev[b];out.append(i)
        return out
    for start in range(len(edges)):
        q=[start];prev={start:None};done=None
        for i in q:
            for k in range(2):
                if i in parts[k]:continue
                cycle=path(parts[k],*edges[i])
                if cycle is None:done=(i,k);break
                for j in cycle:
                    if j not in prev:prev[j]=(i,k);q.append(j)
            if done:break
        if done is None:return False
        i,k=done
        while True:
            parts[k].add(i)
            if prev[i] is None:break
            j,l=prev[i];parts[l].remove(i);i,k=j,l
    assert all(forest([edges[i] for i in part],n) for part in parts)
    return True

def instance(rot,faces,t0,heavy=True):
    v=len(rot);n=v-3; R=set(faces[t0]);X=sorted(set(range(v))-R)
    edgefaces=collections.defaultdict(list)
    for i,f in enumerate(faces):
        for a,b in itertools.combinations(f,2):edgefaces[tuple(sorted((a,b)))].append(i)
    color={t0:0};q=[t0]
    for i in q:
        for a,b in itertools.combinations(faces[i],2):
            for j in edgefaces[tuple(sorted((a,b)))]:
                if j not in color:color[j]=1-color[i];q.append(j)
                elif j!=i:assert color[j]!=color[i]
    A=[i for i in range(len(faces)) if color[i]==0 and i!=t0]
    blacks=A+[t0]; whites=[i for i in range(len(faces)) if color[i]]
    wid={f:i for i,f in enumerate(whites)}
    WE={}
    for t in blacks:
        for x in faces[t]:
            ends=[]
            for y in faces[t]:
                if y!=x:ends += [wid[z] for z in edgefaces[tuple(sorted((x,y)))] if z!=t]
            WE[t,x]=tuple(ends)
    opts=[[t for t in A if x in faces[t]] for x in X]
    # Independent state enumeration by matching recursion.
    states=[]
    def matching(i,used,s):
        if i==n:states.append(tuple(s));return
        for x in faces[A[i]]:
            if x not in R and x not in used:matching(i+1,used|{x},s+[x])
    matching(0,set(),[])
    good=set()
    for s in states:
        qe=[tuple(x for x in faces[t] if x!=s[i]) for i,t in enumerate(A)]
        ok=forest(qe+[(v,r) for r in R],v+1)
        if ok:good.add(tuple(next(t for i,t in enumerate(A) if s[i]==x) for x in X))
    covers=set()
    for i,s in enumerate(states):
        for r in states[i+1:]:
            if all(a!=b for a,b in zip(s,r)):
                covers.add(frozenset((t,x) for j,t in enumerate(A) for x in (s[j],r[j])))
    # Enumerate independent transversals directly in W, with cycle pruning.
    trees={}
    def rainbow(i,par,s):
        if i==n:
            load=collections.Counter(s);trees[tuple(s)]=sum(abs(load[t]-1) for t in A);return
        def find(a):
            while par[a]!=a:a=par[a]
            return a
        for t in opts[i]:
            a,b=map(find,WE[t,X[i]])
            if a!=b:
                pp=par.copy();pp[a]=b;rainbow(i+1,pp,s+[t])
    rainbow(0,list(range(n+1)),[])
    assert {s for s,e in trees.items() if e==0}==good
    # Separators by deleting their boundary and locating the side away from roots.
    bad=0
    edges=set(edgefaces)
    for tri in itertools.combinations(range(v),3):
        if not all(tuple(sorted(e)) in edges for e in itertools.combinations(tri,2)):continue
        todo=set(range(v))-set(tri);comps=[]
        while todo:
            comp={todo.pop()};qq=list(comp)
            for x in qq:
                for y in rot[x]:
                    if y in todo:todo.remove(y);comp.add(y);qq.append(y)
            comps.append(comp)
        if len(comps)<2:continue
        inside=next(c for c in comps if not (c & R))
        adjacent=[next(z for z in edgefaces[tuple(sorted(e))] if set(faces[z]) & inside) for e in itertools.combinations(tri,2)]
        bad += all(color[z]==0 for z in adjacent)
    assert bool(trees)==bool(covers)==(bad==0)
    # Every vertex subset: density; connected J: exact Euler identity (3.3).
    density=0
    for mask in range(1,1<<v):
        U={x for x in range(v) if mask>>x&1};p=len(U)
        m=sum(a in U and b in U for a,b in edges)
        b=sum(set(faces[t])<=U for t in blacks)
        density+=m-b+max(0,len(U&R)-1)>2*p-2
    assert (density==0)==(bad==0)
    for mask in range(1,1<<n):
        J={X[i] for i in range(n) if mask>>i&1};seen={next(iter(J))};qq=list(seen)
        for x in qq:
            for y in rot[x]:
                if y in J and y not in seen:seen.add(y);qq.append(y)
        if seen!=J:continue
        U=set(range(v))-J;todo=set(U);c=0
        while todo:
            qq=[todo.pop()];c+=1
            for x in qq:
                for y in rot[x]:
                    if y in todo:todo.remove(y);qq.append(y)
        d=sg=0
        for a,b in edges:
            if a in U and b in U:
                for t in edgefaces[a,b]:
                    if set(faces[t]) & J:d+=1;sg+=1 if color[t]==0 else -1
        w=sum(bool(set(faces[t])&J) for t in whites)
        assert 6*(w-len(J)-1)==6*(c-1)+3*d-sg-12
        COUNTS['euler_connected_sets']+=1
    # Cover membership and S(2),(3), Edmonds, face condition by exhaustive choices.
    for F in covers:
        choices=[[t for t in opts[i] if (t,x) in F] for i,x in enumerate(X)]
        local=[]
        for s in itertools.product(*choices):
            other=tuple(next(t for t in choices[i] if t!=s[i]) for i in range(n))
            arcs=[(x,next(y for y in faces[t] if (t,y) not in F)) for x,t in zip(X,other)]
            acyclic=forest([(a if a in X else v,b if b in X else v) for a,b in arcs],v+1)
            assert acyclic==(s in trees)
            if acyclic:local.append(s)
            if len(covers)==1:assert acyclic
        assert any(tuple(next(t for t in choices[i] if t!=s[i]) for i in range(n)) in trees for s in local)
        assert any(len(set(s))==n and forest([WE[t,x] for x,t in zip(X,s)],n+1) for s in itertools.product(*choices))
        if heavy:assert any(s in good for s in local)
    # All rainbow trees: unique cover, exchange, reversal, Step X.
    alternatives={}; no_decrease=0
    for s,e in trees.items():
        membership=[F for F in covers if all((t,x) in F for x,t in zip(X,s))]
        assert len(membership)==1
        al=[]
        for i,x in enumerate(X):
            candidates=[s[:i]+(t,)+s[i+1:] for t in opts[i] if t!=s[i] and s[:i]+(t,)+s[i+1:] in trees]
            assert len(candidates)==1;al.append(candidates[0])
        alternatives[s]=al
        if e and all(trees[z]>=e for z in al):no_decrease+=1
    def walk(s,t,a):
        y=next(i for i,tt in enumerate(s) if tt==t and i!=a)
        ss=alternatives[s][y];tt=ss[y]
        return (ss,tt,y) if tt in s else ss
    for s in trees:
        for t in A:
            ids=[i for i,tt in enumerate(s) if tt==t]
            if len(ids)!=2:continue
            for a in ids:
                z=walk(s,t,a);COUNTS['walk_states']+=1
                if len(z)==3 and isinstance(z[0],tuple):
                    ss,tt,arrival=z; resident=next(i for i,val in enumerate(ss) if val==tt and i!=arrival)
                    assert walk(ss,tt,resident)==(s,t,next(i for i in ids if i!=a))
    def invol(s,t):
        i=s.index(t);ss=alternatives[s][i];z=(ss,ss[i],i);seen=set()
        while True:
            assert z not in seen;seen.add(z);out=walk(*z)
            if out in good:return out
            z=out
    for s in good:
        for t in A:
            ss=invol(s,t);assert ss!=s and invol(ss,t)==s;COUNTS['involutions']+=1
    reached=set(good);q=list(good)
    for s in q:
        for z in alternatives[s]:
            if trees[z]>=trees[s] and z not in reached:reached.add(z);q.append(z)
    assert len(reached)==len(trees)
    # Exact two-forest packing for every deleted-corner map at <=12 vertices.
    if trees and heavy:
        for u in itertools.product(*(faces[t] for t in A)):
            whiteedges=[WE[t,x] for t,y in zip(A,u) for x in faces[t] if x!=y]
            primal=[(x if x in X else v,y if y in X else v) for t,y in zip(A,u) for x in faces[t] if x!=y]
            assert split_forests(whiteedges,n+1)
            assert split_forests(primal,v+1)
            COUNTS['deleted_maps']+=1
    result=dict(vertices=v,root=list(faces[t0]),rainbow=len(trees),good=len(good),covers=len(covers),no_decrease=no_decrease)
    if not heavy:
        result['cover_counts']=[dict(rainbow=sum(all((t,x) in F for x,t in zip(X,s)) for s in trees),good=sum(all((t,x) in F for x,t in zip(X,s)) for s in good)) for F in covers]
    COUNTS.update(instances=1,paired=bool(covers),rainbow=len(trees),good=len(good),covers=len(covers),no_decrease=no_decrease,states=len(states))
    return result

if __name__=='__main__':
    begin=time.time();rows=[]
    for v in range(6,13):
        for gi,(rot,faces) in enumerate(graphs(v)):
            for t0 in range(len(faces)):rows.append(dict(index=gi,**instance(rot,faces,t0)))
        print(v,dict(COUNTS),round(time.time()-begin,2),flush=True)
    (BASE/'census.json').write_text(json.dumps(dict(command='python research/2026-11-14_sol_referee-sign-free/check.py',counts=dict(COUNTS),rows=rows),indent=2))
    for gi,(rot,faces) in enumerate(graphs(16)):
        if gi==27:
            t0=next(i for i,f in enumerate(faces) if set(f)=={0,1,2})
            out=instance(rot,faces,t0,False)
            (BASE/'witness16.json').write_text(json.dumps(out,indent=2));print(out,flush=True);break
