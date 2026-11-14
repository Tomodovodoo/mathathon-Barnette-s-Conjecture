from check import *
from induction import contract,good,classify
import networkx as nx, random, collections

def rotation(g):
 ok,e=nx.check_planarity(g);assert ok
 return [list(e.neighbors_cw_order(i)) for i in range(len(g))]
def graph(rot):return nx.Graph((i,j) for i,ns in enumerate(rot) for j in ns)
def rooted(rot,R):
 fs,col=faces(rot);ri=next(i for i,f in enumerate(fs) if set(f)==set(R));return [f for i,f in enumerate(fs) if col[i]==col[ri] and i!=ri]
def glue(rot,R,rot2,R2,white):
 g=graph(rot);mp=dict(zip(R2,white));n=len(rot)
 for i in range(len(rot2)):
  if i not in mp:mp[i]=n;n+=1
 for i,ns in enumerate(rot2):
  for j in ns:g.add_edge(mp[i],mp[j])
 return rotation(g),R

def tube(p,L):
 g=nx.Graph()
 for j in range(L+1):
  for i in range(p):g.add_edge(j*p+i,j*p+(i+1)%p)
 for j in range(L):
  for i in range(p):
   g.add_edge(j*p+i,(j+1)*p+i);a,b=(i,(i+1)%p) if i%2==0 else ((i+1)%p,i);g.add_edge(j*p+a,(j+1)*p+b)
 for i in range(p):g.add_edge((L+1)*p,i);g.add_edge((L+1)*p+1,L*p+i)
 return rotation(g)
def onecover(m):
 g=nx.Graph()
 for i in range(m):
  x,y,z=2+3*i,3+3*i,4+3*i;yp=3+3*((i-1)%m)
  g.add_edges_from([(0,x),(0,y),(x,y),(x,yp),(1,y),(1,z),(z,y),(z,yp),(z,x)])
 return rotation(g)
def expand(rot,rng):
 # split an edge into a degree-four vertex; two inserted subdivisions preserve parity
 g=graph(rot);fs,_=faces(rot);u,v=rng.choice(list(g.edges()));opp=[next(x for x in f if x not in (u,v)) for f in fs if u in f and v in f]
 # splitting two incident edges at u with the same opposite pair is not general.
 # use white-face octahedral insertion instead; valid and deliberately product-biased.
 return rot
if __name__=='__main__':
 out=[];rng=random.Random(20261114)
 def run(label,rot,R=None):
  fs,_=faces(rot);R=R or fs[0];res=check(rooted(rot,R),R);row=dict(label=label,V=len(rot),root=R,rotation=rot,**res);out.append(row);print({k:v for k,v in row.items() if k!='rotation'},flush=True)
 for p in (4,6,8):
  for L in range(3):run(f'tube-{p}-{L}',tube(p,L))
 for m in range(2,8):run(f'separator-free-{m}',onecover(m))
 d=json.loads((REPO/'research/2026-11-14_opus_conjectures/data/c2_counterexample_V18.json').read_text());r=parse(d['line']);R=d['roots'];run('lattice18',r,R)
 fs,col=faces(r);ri=next(i for i,f in enumerate(fs) if set(f)==set(R));w=next(f for i,f in enumerate(fs) if col[i]!=col[ri]);rr,RR=glue(r,R,r,R,w);run('lattice18-white-gluing33',rr,RR)
 # Independent random sample: uniform selection from a fresh plantri stream, random facial roots.
 for v in (17,18,19):
  lines=subprocess.run([str(P),'-ba',str(v)],capture_output=True,check=True).stdout.decode().splitlines()
  for j,line in enumerate(rng.sample(lines,10)):
   rot=parse(line);fs,_=faces(rot);run(f'random-census-{v}-{j}',rot,rng.choice(fs))
 # Random white-face gluings of independently selected small census pieces.
 small=subprocess.run([str(P),'-ba','14'],capture_output=True,check=True).stdout.decode().splitlines()
 for j in range(10):
  r=parse(rng.choice(small));R=rng.choice(faces(r)[0]);r2=parse(rng.choice(small));R2=rng.choice(faces(r2)[0]);fs,col=faces(r);ri=next(i for i,f in enumerate(fs) if set(f)==set(R));w=rng.choice([f for i,f in enumerate(fs) if col[i]!=col[ri]]);rr,RR=glue(r,R,r2,R2,w);run(f'random-glue-{j}',rr,RR)
 (BASE/'code/families.json').write_text(json.dumps(out,indent=2))
