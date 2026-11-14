"""Independent referee enumeration. No project algorithm imports."""
import json, itertools, collections, pathlib, sys, subprocess, time
import networkx as nx
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def tube(p,L):
    g=nx.Graph()
    for j in range(L+1):
        for i in range(p): g.add_edge(j*p+i,j*p+(i+1)%p)
    for j in range(L):
        for i in range(p):
            g.add_edge(j*p+i,(j+1)*p+i)
            a,b=(i,(i+1)%p) if i%2==0 else ((i+1)%p,i)
            g.add_edge(j*p+a,(j+1)*p+b)
    g.add_edges_from(((L+1)*p,i) for i in range(p))
    g.add_edges_from(((L+1)*p+1,L*p+i) for i in range(p))
    return g

def family(m):
    g=nx.Graph()
    for i in range(m):
        x,y,z=2+3*i,3+3*i,4+3*i; prev=3+3*((i-1)%m)
        g.add_edges_from([(0,x),(0,y),(x,y),(x,prev),(1,y),(1,z),(z,y),(z,prev),(z,x)])
    return g

def faces(g):
    ok,e=nx.check_planarity(g); assert ok
    seen=set(); fs=[]
    for a,b in e.edges():
        if (a,b) not in seen: fs.append(tuple(e.traverse_face(a,b,seen)))
    assert all(len(f)==3 for f in fs)
    return fs

def instance(g,root,enumerate_states=True):
    fs=faces(g); ri=next(i for i,f in enumerate(fs) if set(f)==set(root))
    incidence=collections.defaultdict(list)
    for i,f in enumerate(fs):
        for e in itertools.combinations(f,2): incidence[tuple(sorted(e))].append(i)
    dual=nx.Graph(); dual.add_nodes_from(range(len(fs)))
    dual.add_edges_from(v for v in incidence.values())
    colors=nx.bipartite.color(dual)
    A=[f for i,f in enumerate(fs) if colors[i]==colors[ri] and i!=ri]
    if not enumerate_states:return fs,incidence,dual,A,[]
    X=set(g)-set(root)
    order=sorted(range(len(A)),key=lambda i:len(set(A[i])&X)); result=[]
    def visit(k,used,s):
        if k==len(A): result.append(tuple(s)); return
        i=order[k]
        for v in A[i]:
            if v in X and v not in used:
                s[i]=v; visit(k+1,used|{v},s)
    visit(0,set(),[None]*len(A))
    return fs,incidence,dual,A,result

def forest(g,A,s,root):
    q=nx.Graph(); q.add_nodes_from(g)
    q.add_edges_from(tuple(v for v in f if v!=s[i]) for i,f in enumerate(A))
    return nx.is_forest(q) and all(len(set(c)&set(root))==1 for c in nx.connected_components(q))

def analyse(g,root,hc=False,details=False):
    fs,inc,dual,A,states=instance(g,root)
    good=[forest(g,A,s,root) for s in states]
    covers={}; fibres=collections.defaultdict(set); pairs=0
    # Phase uses the oriented black facial boundaries from a single embedding.
    for r in states:
        for s in states:
            if any(a==b for a,b in zip(r,s)): continue
            pairs+=1
            es=tuple(sorted(tuple(sorted(e)) for e in zip(r,s)))
            d=nx.Graph(); d.add_edges_from(es); c=nx.number_connected_components(d)
            cut=dual.copy(); cut.remove_edges_from(inc[e] for e in es)
            assert nx.number_connected_components(cut)==c+1
            covers[es]=c
            fibres[es].add(s)
    if len(covers)==2:
        e1,e2=covers; d1=nx.Graph();d1.add_edges_from(e1);d2=nx.Graph();d2.add_edges_from(e2)
        csets=lambda d:{frozenset(tuple(sorted(e)) for e in d.subgraph(v).edges()) for v in nx.connected_components(d)}
        j=len(csets(d1)&csets(d2)); a=len(fibres[e1]&fibres[e2]); assert a in [0,2**j]
        assert sum(good)==2**covers[e1]+2**covers[e2]-2*a
    out=dict(V=len(g),S=len(states),P=pairs,M=sum(good),covers=len(covers),cmin=min(covers.values(),default=None),cycle_hist=dict(collections.Counter(covers.values())))
    if hc:
        # Enumerate primal perfect matchings; complement must be one cycle.
        hs=[]; nodes=set(dual)
        def match(left,selected):
            if not left:
                rem=dual.copy(); rem.remove_edges_from(selected)
                if nx.is_connected(rem): hs.append(tuple(sorted(tuple(sorted(e)) for e in selected)))
                return
            v=min(left,key=lambda x:len(set(dual[x])&left))
            for w in set(dual[v])&left: match(left-{v,w},selected+[(v,w)])
        match(nodes,[])
        out['H']=len(hs); out['avoid']=sorted(collections.Counter(e for h in hs for e in h).values())
    if details: return out,A,states,covers
    return out

def certificates():
    path=ROOT/'research/2026-11-14_sol_counting-families/data'; rows=[]
    for name in ['certificates.json','HC-certificates.json','pair-certificates.json']:
        for cert in json.loads((path/name).read_text()):
            n=cert['matrix_dimension']; entries=cert['matrix_entries']; v=cert['initial']; w=cert['terminal']; rec=cert['recurrence']; d=len(rec)
            # sparse vectors may be stored as dicts or dense lists
            if isinstance(v,dict): v=[v.get(str(i),0) for i in range(n)]
            if isinstance(w,dict): w=[w.get(str(i),0) for i in range(n)]
            scalar=lambda a:sum(a.values()) if isinstance(a,dict) else a
            v=list(map(scalar,v)); w=list(map(scalar,w))
            entries=[(i,j,scalar(a)) for i,j,a in entries]
            seq=[]
            for k in range(n+d+5):
                seq.append(sum(a*b for a,b in zip(v,w)))
                nxt=[0]*n
                for i,j,a in entries: nxt[j]+=v[i]*a
                v=nxt
            assert all(seq[k]==sum(a*seq[k-j-1] for j,a in enumerate(rec)) for k in range(d,len(seq)))
            rows.append(dict(file=name,width=cert['width'],quantity=cert.get('quantity','pairs'),dimension=n,checked_discrepancies=n,initial=seq[:d],ok=True))
    return rows

def plantri(V,c4=False):
    exe=ROOT/'workings/barnette_lab/vendor/plantri.exe'
    raw=subprocess.run([str(exe),'-b']+(['-c4'] if c4 else [])+[str(V)],capture_output=True,check=True,timeout=500).stdout.replace(b'\r\n',b'\n')
    assert raw.startswith(b'>>planar_code<<'); raw=raw[len(b'>>planar_code<<'):]; pos=0
    while pos<len(raw):
        n=raw[pos];pos+=1;g=nx.Graph();g.add_nodes_from(range(n))
        for i in range(n):
            while raw[pos]: g.add_edge(i,raw[pos]-1);pos+=1
            pos+=1
        yield g

def polynomial(g,root):
    import sympy as sp
    fs,inc,dual,A,states=instance(g,root); n=len(A)
    incidences=[(i,v) for i,f in enumerate(A) for v in f]; pos={e:k for k,e in enumerate(incidences)}
    vars=sp.symbols('a:'+str(len(pos))); eq=[]
    black={tuple(sorted(f)):i for i,f in enumerate(A)}
    edgeblack={tuple(sorted(e)):i for i,f in enumerate(A) for e in itertools.combinations(f,2)}
    for f in fs:
        if tuple(sorted(f)) in black or set(f)==set(root):continue
        if any(tuple(sorted(e)) not in edgeblack for e in itertools.combinations(f,2)):continue
        expr=0
        for u,v in zip(f,f[1:]+f[:1]):
            t=edgeblack[tuple(sorted((u,v)))];expr+=vars[pos[t,v]]-vars[pos[t,u]]
        eq.append(expr-1)
    sol=next(iter(sp.linsolve(eq,vars))); free=set().union(*(x.free_symbols for x in sol)); weights=[int(x.subs(dict.fromkeys(free,0))) for x in sol]
    z,x=sp.symbols('z x'); P=0; linear=0
    for r in states:
        for s in states:
            if any(a==b for a,b in zip(r,s)):continue
            J=sum(1 if (f.index(b)-f.index(a))%3==1 else -1 for f,a,b in zip(A,r,s))
            sign=(-1)**((n+J)//2); ws=[weights[pos[i,v]] for i,v in enumerate(s)]
            P+=sign*z**sum(ws); linear+=sign*sp.prod(1+x*a for a in ws)
    P=sp.expand(P); lo=min(t[0][0] for t in sp.Poly(P*z**(sum(abs(w) for w in weights)+1),z).terms())-(sum(abs(w) for w in weights)+1)
    return dict(z=str(sp.factor(P/z**lo)),linear=str(sp.factor(linear)),weights=weights,root=list(root))

def witnesses():
    out=[]; path=ROOT/'research'
    for file in [path/'2026-11-14_astra_cycle-covers/data/levels.json',path/'2026-11-14_opus_conjectures/data/c2_counterexample_V18.json']:
        obj=json.loads(file.read_text()); print(file.name,obj.keys(),flush=True)
        g=nx.Graph(obj['edges']); root=obj.get('root',obj.get('roots'))
        a,A,states,covers=analyse(g,root,details=True)
        # Complements in incidence graph: u is the corner NOT selected in a cover.
        us=[tuple(next(v for v in f if all(tuple(sorted((v,w))) not in es for w in f if w!=v)) for f in A) for es in covers]
        adj=[]
        for i,u in enumerate(us):
            for j,v in enumerate(us[:i]):
                changes=[k for k in range(len(A)) if u[k]!=v[k]]
                h=nx.Graph();h.add_edges_from((u[k],v[k]) for k in changes)
                if h and nx.is_connected(h) and all(d==2 for _,d in h.degree()):adj.append((j,i))
        a.update(source=str(file.relative_to(ROOT)),cycles=list(covers.values()),flip_edges=adj,root=list(root)); out.append(a)
    return out

def stack(q):
    g=tube(6,0); root=(6,0,1); outgoing=(7,4,5)
    for _ in range(q-1):
        h=tube(6,0); mapping=dict(zip((6,0,1),outgoing)); nxt=max(g)+1
        for v in h:
            if v not in mapping:mapping[v]=nxt;nxt+=1
        g.add_edges_from((mapping[u],mapping[v]) for u,v in h.edges())
        outgoing=tuple(mapping[v] for v in (7,4,5))
    return g,root

def main():
    mode=sys.argv[1]; out=[]
    if mode=='families':
        for m in range(2,9):
            a=analyse(family(m),(0,2,3)); a.update(family='astra',m=m); out.append(a)
        for m in range(2,8):
            g=tube(2*m,0); a=analyse(g,(2*m,0,1),True); a.update(family='prism',m=m); out.append(a)
        for p,maxL in [(4,5),(6,3)]:
            for L in range(maxL+1):
                g=tube(p,L); root=(p*(L+1),0,1) if L==0 else (0,1,p+1)
                a=analyse(g,root,True); a.update(family='tube',p=p,L=L); out.append(a)
                print(p,L,a,flush=True)
    elif mode=='certificates': out=certificates()
    elif mode=='witnesses': out=witnesses()
    elif mode=='stacks':
        for q in range(1,5):
            g,r=stack(q); a=analyse(g,r,True);a.update(q=q,polynomial=polynomial(g,r));out.append(a)
    elif mode=='stack-source':
        path=ROOT/'research/2026-11-14_sol_counting-families/data'
        for obj in json.loads((path/'stack.json').read_text()):
            g=nx.Graph(obj['dual_edges']); r=obj['root_vertices']; a=analyse(g,r,True);a.update(q=obj['parameter'],polynomial=polynomial(g,r));assert a['H']==obj['HC'];out.append(a)
        g=tube(6,0); local=[]
        for bits in itertools.product([0,1],repeat=7):
            color=(0,)+bits; sets=[{i for i in g if color[i]==c} for c in [0,1]]
            if all(s and nx.is_tree(g.subgraph(s)) for s in sets):local.append(frozenset(tuple(sorted((u,v))) for u,v in g.edges() if color[u]==color[v]))
        cert=json.loads((path/'stack-HC-transfer.json').read_text());assert set(local)=={frozenset(map(tuple,c)) for c in cert['base_cycles_as_avoided_dual_edges']}
        for step in cert['steps']:
            matrix=[[sum(tuple(e) in c and tuple(f) in c for c in local) for f in step['outgoing_local_edges']] for e in step['incoming_local_edges']]
            assert matrix==step['matrix']
        out.append(dict(base_cycles=len(local),tensor_verified=True))
    elif mode=='family-polynomials':
        for m in range(2,7):out.append(dict(m=m,**polynomial(family(m),(0,2,3))))
    elif mode=='polynomials':
        data=json.loads((ROOT/'research/2026-11-14_sol_route-probabilistic/data/roots.json').read_text())
        for key in ['first_offcircle','first_linear_nonreal']:
            obj=data[key]; g=nx.Graph(obj['edges']); f=faces(g)[0]
            a=polynomial(g,f);a['source']=key;out.append(a)
        out.append(polynomial(tube(8,0),(8,0,1)))
    elif mode=='census':
        for V in range(6,17):
            rows=[analyse(g,f) for g in plantri(V,True) for f in faces(g)]
            row=dict(V=V,classes=len(rows)//(2*V-4),roots=len(rows),cmin_hist=dict(collections.Counter(r['cmin'] for r in rows)),violations=sum(r['M']<2**r['cmin'] or (r['covers']>1 and r['M']<=2**r['cmin']) for r in rows))
            out.append(row);print(row,flush=True)
    (HERE/(mode+'.json')).write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
