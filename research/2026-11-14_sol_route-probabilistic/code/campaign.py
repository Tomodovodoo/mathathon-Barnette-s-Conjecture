"""Capped scan, independent tree enumeration for the cube, and Monte Carlo models."""
from explore import *
from count import partners

def scan():
    rows=[];bad=None
    for V in range(6,15):
        for k,g in enumerate(plantri_graphs(V,ROOT/'workings/barnette_lab/vendor/plantri.exe')):
            b=Instance(g);ss=list(b.states());ps=b.pairs(ss);hp=halfpair(b,ps)
            row={'V':V,'index':k,'states':len(ss),'TM':sum(b.is_tree(s) for s in ss),'pairs':len(ps),'half':hp}
            rows.append(row)
            if not hp['feasible']:
                bad={'edges':list(g.edges()),'outer':b.outer,**row};break
            deadline()
        if bad:break
    # All cube spanning trees: exact independent connectivity test.
    b=Instance.from_primal(nx.cubical_graph());es=list(b.H.edges());nodes=list(b.H)
    support={};cnt=0
    for omit in itertools.combinations(range(len(es)),b.n):
        h=b.H.copy();h.remove_edges_from(es[i] for i in omit)
        if nx.is_tree(h):
            cnt+=1;d=tuple(h.degree(v) for v in nodes);support[d]=list(omit)
    witness=None
    for a in support:
        for c in support:
            for i in range(len(a)):
                if a[i]<=c[i]:continue
                possible=[]
                for j in range(len(a)):
                    if a[j]>=c[j]:continue
                    d=list(a);d[i]-=1;d[j]+=1
                    if tuple(d) in support:possible.append(j)
                if not possible:witness={'nodes':nodes,'a':a,'b':c,'coordinate':i,'omitted_a':support[a],'omitted_b':support[c]};break
            if witness:break
        if witness:break
    out={'rows':rows,'half_failure':bad,'cube_trees':cnt,'cube_support_size':len(support),'M_exchange_failure':witness,'seconds':time.monotonic()-START}
    (OUT/'data/scan.json').write_text(json.dumps(out,indent=2));print('scan',len(rows),'half failure',bad,'M witness',witness,flush=True)

def sample_state(b,rng):
    # Numerically evaluate exact determinant self-reduction, not a certified exact sampler.
    cols=list(b.X);s=[];K=np.array(b.K,dtype=float)
    for i,t in enumerate(b.A):
        inv=np.linalg.inv(K);p=K[0,:]*inv[:,0];assert min(p)>-1e-7 and abs(sum(p)-1)<1e-7;p=np.maximum(p,0);p/=sum(p)
        x=rng.choices(range(len(cols)),weights=p)[0];s.append(cols.pop(x));K=np.delete(K[1:,:],x,axis=1)
    return tuple(s)

def local_options(b):
    out=[]
    for w in b.white:
        vs=b.faces[w]
        ts=[next(t for t in [b.sides[u,v],b.sides[v,u]] if t in b.black) for u,v in zip(vs,vs[1:]+vs[:1])]
        if b.outer in ts or not set(vs)<=set(b.X):continue
        out.append([(b.A.index(t),u,v) for t,u,v in zip(ts,vs,vs[1:]+vs[:1])])
    return out

def randoms():
    rng=random.Random(11714);graphs=[]
    # Uniform among unlabelled plantri objects at V=16, then one uniform face.
    gs=list(plantri_graphs(16,ROOT/'workings/barnette_lab/vendor/plantri.exe'))
    for k in rng.sample(range(len(gs)),8):
        b=Instance(gs[k]);graphs.append((f'plantri16_{k}',Instance(gs[k],rng.randrange(len(b.faces)))))
    # Random recursive white-face octahedral insertions, root retained.
    from barnette_lab.core import glue_triangles
    for rep in range(3):
        b=Instance(nx.octahedral_graph());root=b.R
        for j in range(10):
            g=glue_triangles(b.T,nx.octahedral_graph(),rng.choice(b.white),0)
            bb=Instance(g);b=Instance(g,next(i for i,f in enumerate(bb.faces) if set(f)==root))
        graphs.append((f'random_white_gluing{rep}',b))
    graphs += [('subdivision_tube6',Instance(subdivide(tube(6,1)))),('rare_tube4_L12',Instance(tube(4,12))),('rare_chain8',stack(6,8))]
    rows=[]
    for name,b in graphs:
        deadline();hits=0;ch=Counter();pair_c=Counter();zero=0;N=160
        for _ in range(N):
            deadline()
            s=sample_state(b,rng);assert b.valid(s)
            hits+=b.is_tree(s);k=len(b.qcycles(s));ch[k]+=1;zero+=k==0 and not b.is_tree(s)
            rs=list(partners(b,s))
            for r in rs:pair_c[len(b.dcycles(r,s))]+=1
        opts=local_options(b);runs=[]
        for rep in range(12):
            s=sample_state(b,rng);energy=len(b.qcycles(s));accepted=0
            for step in range(2001):
                if step%100==0:deadline()
                if b.is_tree(s):break
                if not opts:break
                cycle=rng.choice(opts);cand=list(s)
                if all(s[i]==u for i,u,v in cycle):
                    for i,u,v in cycle:cand[i]=v
                elif all(s[i]==v for i,u,v in cycle):
                    for i,u,v in cycle:cand[i]=u
                else:continue
                cand=tuple(cand);e=len(b.qcycles(cand))
                if e<=energy:s=cand;energy=e;accepted+=1
            runs.append({'success':b.is_tree(s),'steps':step,'accepted':accepted})
        row={'name':name,'edges':list(b.T.edges()),'outer':b.outer,'has_pair':b.flow_pair() is not None,'V':len(b.T),'states_exact':abs(int(b.K.det())),'samples':N,'hits':hits,'cycle_hist':dict(ch),'zero_cycle_nonTM':zero,'sampled_pair_cycle_hist':dict(pair_c),'cmin_upper_bound':min(pair_c,default=None),'flip_runs':runs}
        rows.append(row);print(name,row['V'],hits,'flip',sum(r['success'] for r in runs),flush=True)
        (OUT/'data/random.json').write_text(json.dumps({'seed':11714,'rows':rows,'seconds':time.monotonic()-START},indent=2))
if __name__=='__main__':
    if sys.argv[1]=='scan':scan()
    else:randoms()
