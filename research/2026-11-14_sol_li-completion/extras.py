"""Census cross-check, witnesses, families and comparison. Run after verify.py."""
from verify import *
import subprocess

levels=enumerate_classes(14)
exe=ROOT/'workings/barnette_lab/vendor/plantri.exe'
cross={}
for v,codes in levels.items():
    proc=subprocess.run([str(exe),'-ba',str(v)],capture_output=True,text=True,check=True,timeout=120)
    got=set()
    from tri import canon
    for line in proc.stdout.splitlines():
        n,adj=line.split();g=nx.Graph()
        for u,row in enumerate(adj.split(',')):
            g.add_edges_from((u,ord(z)-97) for z in row)
        ok,emb=nx.check_planarity(g);seen=set();fs=[]
        for u,w in emb.edges():
            if (u,w) not in seen:fs.append(tuple(emb.traverse_face(u,w,seen)))
        got.add(canon(Tri(fs)))
    assert got==set(codes),(v,len(got),len(codes))
    cross[v]=len(got)
(OUT/'plantri-crosscheck.json').write_text(json.dumps(dict(command='python research/2026-11-14_sol_li-completion/extras.py',executable=str(exe),classes=cross),indent=2))

rows=json.loads((OUT/'census.json').read_text())['rows']; witnesses=[]
for m in (2,3):
    row=next(r for r in rows if r.get('m')==m)
    T=from_code(levels[row['v']][row['cls']]);b=Check(T.faces,row['root'])
    cases={}
    for o in b.objects(m):
        cs,_,_,h=b.data(o[0]);M=o[1]
        empty=[c for c in cs if not any(i in c for w,i in M)]
        if empty:typ='unmarked cycle'
        elif any(len(h[c,next(w for w,i in M if i in c)])%2==0 for c in cs):typ='exterior mark'
        elif b.two(o)!=o:typ='nonfirst interior mark'
        else:typ='fixed point'
        if typ not in cases:cases[typ]=dict(object=o,image=b.two(o),sign=b.sign(o),image_sign=b.sign(b.two(o)))
    witnesses.append(dict(instance=row,faces=T.faces,cases=cases))
(OUT/'witnesses.json').write_text(json.dumps(witnesses,indent=2))

# Import only family input generation. Compare against the existing walk, never
# use it to implement or decide either independently checked map.
sys.path.insert(0,str(ROOT/'research/2026-11-14_sol_counting-families/code'))
from families import tube,stack,subdivide
from barnette_lab.core import Instance
from barnette_lab.algorithms import marked_walk
families=[]
inputs=[('tube',p,L,tube(p,L)) for p in (4,6) for L in range(3)]
inputs += [('stack',p,q,stack(p,q).T) for p in (4,6) for q in (2,3)]
inputs += [('subdivided',4,0,subdivide(tube(4,0)))]
for name,p,k,g in inputs:
    bb=Instance(g); b=Check(bb.faces,bb.outer)
    if not b.pairs:continue
    # Large marked sets are unnecessary for measuring paths from fixed points.
    m=min(len(b.data(z)[0]) for z in b.pairs); lengths=[]
    for pair in b.pairs:
        cs,_,_,h=b.data(pair)
        if len(cs)!=m:continue
        pools=[]
        for c in cs:
            pools.append([(w,hh[0][1]) for w in b.w if len(hh:=h[c,w])%2 and hh[0][2]==1])
        from itertools import product
        for marks in product(*pools):
            o=(pair,tuple(sorted(marks)));assert b.two(o)==o;steps=0;seen=set()
            while b.one(o)!=o:
                assert o not in seen;seen.add(o);o=b.two(b.one(o));steps+=2
            lengths.append(steps)
    base=[]
    for pair in bb.pairs():
        out,stats=marked_walk(bb,pair);assert bb.is_tree(out[1]);base.append(stats)
    row=dict(family=name,p=p,k=k,vertices=len(g),m=m,fixed_starts=len(lengths),ray_hist=dict(Counter(lengths)),trees_walk_max=max(z['moves'] for z in base),trees_restarts=sum(len(z['restarts']) for z in base))
    families.append(row);print(row,flush=True)
    (OUT/'families.json').write_text(json.dumps(families,indent=2))
