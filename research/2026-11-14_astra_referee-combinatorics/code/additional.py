"""Extra independent checks, including all directed state cycles and mirror images."""
from check import *
sys.path.insert(0,str(REPO/'workings/barnette_lab'))
from barnette_lab.core import Instance

start=time.time(); counts=Counter(); mirrors=[]
for v in range(6,13):
    for M in generated(v):
        perfects=list(pm(M.G))
        for o in M.G:
            R=Root(M,o)
            for s in R.ss:
                d=nx.DiGraph()
                for t,x in zip(R.A,s):
                    d.add_edges_from((x,y) for y in M.faces[t] if y!=x)
                for c in nx.simple_cycles(d):
                    R.disk_check(c); counts['arbitrary_state_cycles']+=1
                # Exact global determinant factor, no floating point.
                col={min(M.T):0}; todo=deque(col)
                while todo:
                    x=todo.popleft()
                    for y in M.T[x]:
                        if y not in col: col[y]=(col[x]+R.delta(x,y))%3; todo.append(y)
                mat=[]
                for t,x in zip(R.A,s):
                    mat.append([0 if y==x or y not in M.faces[t] else (1 if (col[y]-col[x])%3==1 else -1) for y in R.X])
                sig=(-1)**sum(s[i]>s[j] for i in range(R.n) for j in range(i+1,R.n))
                assert sum(R.eps(r,s) for r in R.partners[s])==(-1)**R.n*sig*int(sp.det(sp.Matrix(mat)))
                counts['exact_signed_determinants']+=1
                for matching in perfects:
                    P={e for e,d in M.dual.items() if d in matching}
                    e0=next(e for e in P if set(e)<=R.R)
                    byface={t:e for e in P for t in M.dual[e]}
                    if all(x in byface[t] for t,x in zip(R.A,s)):
                        p=nx.Graph(); p.add_nodes_from(M.T); p.add_edges_from(P)
                        assert nx.is_forest(p) and P in M.hcs
                        counts['compatible_face_pairings']+=1
            # Cross-check a third implementation, allowing its embedding reversal.
            B=Instance(M.T)
            face_ids={frozenset(f):i for i,f in enumerate(B.faces)}
            B=Instance(M.T,face_ids[frozenset(M.faces[o])])
            weights=B.weights(); ratios=set(); ranks=[]
            for x,y in M.T.edges():ratios.add(B.delta(x,y)*R.delta(x,y))
            assert len(ratios)==1; orientation=next(iter(ratios))
            mapping=[R.A.index(next(t for t in R.A if set(M.faces[t])==set(B.faces[a]))) for a in B.A]
            bs=list(B.states())
            assert {tuple(s[i] for i in mapping) for s in R.ss}==set(bs)
            for s in R.ss:
                sb=tuple(s[i] for i in mapping)
                ranks.append(sum(weights[t,x] for t,x in zip(B.A,sb))-orientation*R.rank[s])
            assert len(set(ranks))==1
            counts['reference_volume_comparisons']+=len(R.ss)

data=json.loads((HERE/'examples.json').read_text())
for k,w in data['witnesses'].items():
    M=Map([tuple(reversed(f)) for f in w['faces']]); R=Root(M,w['root']); R.check()
    mirrors.append({'original_example':k,'faces':M.faces,'root':R.o,'results':witness(R)})
assert mirrors[0]['results']['bottom_bad'] and mirrors[0]['results']['cw_min_bad']
sources=['PROOF.md','REPORT.md','ROUTES.md','DATA.md']
out={'command':' '.join(sys.argv),'seconds':time.time()-start,'counts':dict(counts),'mirrors':mirrors,
     'audited_source_sha256':{f:hashlib.sha256((AUTHOR/f).read_bytes()).hexdigest() for f in sources}}
(HERE/'additional.json').write_text(json.dumps(out,indent=2))
print(dict(counts),time.time()-start)
