import sys,time
from independent import *

def greedy():
    out=[]
    folder=ROOT/'research/2026-11-14_opus_route-graph-theory/code/data'
    files=sorted(folder.glob('alpha_*fail*.json'))+[folder/'ef_fail_40_40.json']
    for p in files:
        d=json.loads(p.read_text());rot={int(k):v for k,v in d['rot'].items()};I=Instance(rot,d['t0'])
        dic={frozenset(f):v for f,v in d['u']};u=tuple(dic[frozenset(f)] for f in I.A)
        lo,hi=I.shortest_extremes(u)
        single={}
        for step in (-1,1):
            good=[]
            for j in range(len(I.hfaces)):
                if j==I.outer:continue
                phi=[0]*len(I.hfaces);phi[j]=step;valid=True
                for k,f in enumerate(I.A):
                    for v in f:
                        a,b=(v,I.N+k) if u[k]==v else (I.N+k,v)
                        l,r=I.hleft[a,b],I.hleft[b,a]
                        if phi[r]-phi[l] not in (-1,0):valid=False
                if valid:good.append(j)
            single[step]=good
        out.append({'file':p.name,'V':I.N,'least':not any(lo),'greatest':not any(hi),'single_face_moves':single,
                    'tree_pairs':sum(I.forest(s) for r,s in I.decompositions(u))})
    save('greedy.json',out);print(json.dumps(out,indent=2))

def stored(which):
    v={'r1':24,'r3':60}[which]
    text=(ROOT/f'research/2026-11-14_opus_conjectures/data/{which}_counterexample_V{v}.txt').read_text().strip()
    I=Instance(*parse_text(text));d=lattice_analysis(I,detail=True);d['input']=text
    es=d['entries'];dist={d['lo']:0};q=[d['lo']]
    for j in q:
        for k in es[j]['upper']:
            if k not in dist:dist[k]=dist[j]+1;q.append(k)
    # Distance from either extreme along undirected covers.
    dist={j:0 for j in (d['lo'],d['hi'])};q=list(dist)
    for j in q:
        for k in es[j]['upper']+es[j]['lower']:
            if k not in dist:dist[k]=dist[j]+1;q.append(k)
    d['minimum_extreme_distance_to_tree']=min(dist[j] for j,e in enumerate(es) if e['tree_pairs'])
    paths={d['lo']:[d['lo']]} if not es[d['lo']]['tree_pairs'] else {}
    for j in sorted(range(len(es)),key=lambda j:es[j]['rank']):
        if j not in paths:continue
        for k in es[j]['upper']:
            if not es[k]['tree_pairs']:paths[k]=paths[j]+[k]
    d['tree_free_maximal_chain']=paths.get(d['hi'])
    save(which+'.json',d)
    print({k:v for k,v in d.items() if k not in ('entries','faces_A','hfaces','join_order','input')},flush=True)

def r5():
    # Author generator supplies ONLY the input, never a verification result.
    gen=ROOT/'research/2026-11-14_opus_conjectures/code/gen.py'
    lines=subprocess.run([sys.executable,str(gen),'skew','70','24','52'],capture_output=True,text=True,check=True).stdout.splitlines()
    rot,_=parse_text(lines[23]);root=facial_walks(rot)[0][80];I=Instance(rot,root)
    save('r5_input.json',{'generation':'python research/2026-11-14_opus_conjectures/code/gen.py skew 70 24 52; graph 24; face 80','rotation':rot,'root':root})
    t=time.monotonic();d=lattice_analysis(I,detail=False);d['seconds']=time.monotonic()-t
    save('r5.json',d);print(d,flush=True)
    assert d['lattice']==1410 and d['tree_elements']==654 and d['pairs']==483960 and d['TM']==71180

if __name__=='__main__':globals()[sys.argv[1]](*sys.argv[2:])
