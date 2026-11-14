import sys,json,time
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'research/2026-11-14_fable_referee-primal/code'))
from gen import family
from primal import Rooted,PG,undirected_cycles
C=Counter(); start=time.time()
def check(G,name):
 C['graphs']+=1
 for b0 in G.V:
  R=Rooted(G,b0); states=R.states(); C['roots']+=1; C['states']+=len(states)
  for s in states:
   ps=[r for r in states if R.is_pair(r,s)]
   for r in ps:
    t=sum(R.delta(b,f,g) for b,f,g in zip(R.A,r,s))
    assert t%3==0 and R.eps(r,s)==(1j**(len(R.A)+t//3)).real and (1j**(len(R.A)+t//3)).imag==0
    C['phase normalization checks']+=1
   Q=R.Q(s); cycles=undirected_cycles(range(G.nF),[(i,*G.efaces[e]) for i,e in enumerate(Q)])
   if not cycles:
    if ps: assert len(ps)==1; C['forest states with unique partner']+=1
    continue
   if not ps: continue
   C['cancelling states']+=1
   assert sum(R.eps(r,s) for r in ps)==0
   for cyc in cycles:
    assert len(cyc)%2 and not any(f in R.R for i in cyc for f in G.efaces[Q[i]])
    onc={R.A[i] for i in cyc}
    for r in ps:
     r2=tuple(R.third(b,f,g) if b in onc else f for b,f,g in zip(R.A,r,s))
     r3=tuple(R.third(b,f,g) if b in onc else f for b,f,g in zip(R.A,r2,s))
     assert r2 in ps and r2!=r and r3==r and R.eps(r2,s)==-R.eps(r,s)
     C['checked reversals']+=1
 assert time.time()-start<590,'ten-minute budget'
 print(name,dict(C),flush=True)
if __name__=='__main__':
 n=int(sys.argv[1])
 for name,G in family(n,n): check(G,name)
 result={'command':f'python research/2026-11-14_astra_primal-revision/check_cancellation.py {n}','dual_vertices':n,'counts':dict(C),'seconds':time.time()-start,'failures':0}
 (Path(__file__).parent/f'cancellation-{n}.json').write_text(json.dumps(result,indent=2))
