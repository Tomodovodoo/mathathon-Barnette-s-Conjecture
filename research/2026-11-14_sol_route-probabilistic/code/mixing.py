"""Uniform lazy white-face flip chain: finite spectra and hitting times, not asymptotic bounds."""
from campaign import local_options
from explore import *
rows=[]
for L in range(1,7):
    b=Instance(tube(4,L));ss=list(b.states());idx={s:i for i,s in enumerate(ss)};opts=local_options(b);N=len(ss);P=np.eye(N)
    for j,s in enumerate(ss):
        for cyc in opts:
            cand=list(s)
            if all(s[i]==u for i,u,v in cyc):
                for i,u,v in cyc:cand[i]=v
            elif all(s[i]==v for i,u,v in cyc):
                for i,u,v in cyc:cand[i]=u
            else:continue
            k=idx[tuple(cand)];P[j,k]+=.5/len(opts);P[j,j]-=.5/len(opts)
    assert np.max(abs(P-P.T))<1e-10
    eig=np.linalg.eigvalsh(P);bad=[i for i,s in enumerate(ss) if not b.is_tree(s)]
    gap=float(1-eig[-2]);h=np.linalg.solve(np.eye(len(bad))-P[np.ix_(bad,bad)],np.ones(len(bad)))
    rows.append({'L':L,'states':N,'TM':N-len(bad),'spectral_gap':gap,'uniform_start_mean_hit_proposals':float(sum(h)/N),'worst_start_mean_hit_proposals':float(max(h)),'proposal_faces':len(opts)})
    print(rows[-1],flush=True);deadline()
(OUT/'data/mixing.json').write_text(json.dumps({'rows':rows,'seconds':time.monotonic()-START},indent=2))
