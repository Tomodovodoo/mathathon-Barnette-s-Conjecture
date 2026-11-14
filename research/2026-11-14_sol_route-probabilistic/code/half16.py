"""Predict half-pair feasibility persists at V=16; test both face colours."""
from explore import *
def fast(b,ps):
    es=white_edges(b);ix={v:i for i,v in enumerate(b.white)};covers={tuple(sorted((t,min(r[i],s[i]),max(r[i],s[i])) for i,t in enumerate(b.A))):(r,s) for r,s in ps};n=len(ix)
    for r,s in covers.values():
        used={(t,v) for t,v in zip(b.A,r)}|{(t,v) for t,v in zip(b.A,s)};adj=[Counter() for _ in ix]
        for t,v,a,c in es:
            if (t,v) in used:adj[ix[a]][ix[c]]+=1;adj[ix[c]][ix[a]]+=1
        count=[0]*(1<<n)
        for mask in range(1,1<<n):
            bit=mask&-mask;j=bit.bit_length()-1;prev=mask^bit
            count[mask]=count[prev]+sum(w for v,w in adj[j].items() if prev>>v&1)
            if count[mask]>2*(mask.bit_count()-1):return {'r':r,'s':s,'mask':mask,'white':b.white,'mass2':count[mask]}
    return None
rows=[]
for k,g in enumerate(plantri_graphs(16,ROOT/'workings/barnette_lab/vendor/plantri.exe')):
    for outer in (0,1):
        b=Instance(g,outer);ss=list(b.states());ps=b.pairs(ss);bad=fast(b,ps)
        rows.append({'index':k,'outer':outer,'pairs':len(ps),'failure':bad})
        if bad:print('FAIL',rows[-1],flush=True)
        deadline()
(OUT/'data/half16.json').write_text(json.dumps({'rows':rows,'seconds':time.monotonic()-START},indent=2));print('done',len(rows),sum(r['failure'] is not None for r in rows))
