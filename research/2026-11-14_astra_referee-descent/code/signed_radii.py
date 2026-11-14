from check import *
from potentials import geometry,potential
import re
out=[]
for line in (REPO/'research/2026-11-14_fable_descent/data/witnesses.txt').read_text().splitlines():
 if not line.startswith('W SIGNEDRHO'):continue
 head,raw,pairs=line.split(' | ');rot=parse(raw);R=tuple(map(int,re.search(r't0=(\d+,\d+,\d+)',head)[1].split(',')));fs,col=faces(rot);ri=next(i for i,f in enumerate(fs) if set(f)==set(R));black=[f for i,f in enumerate(fs) if col[i]==col[ri] and i!=ri];ab=[tuple(map(int,s.split('>'))) for s in pairs[5:].split()];A=[next(f for f in black if a in f and b in f) for a,b in ab];p=tuple(zip(*ab));area=geometry(rot,R);name='(k,+psi,-om)' if 'pot=1 ' in head else '(k,+om,+psi)';k=len(info(A,p)[1]);cost0=potential(name,(k,0,0,0,0,0,0));heights={p:(0,0)};front=[p];rho=None
 for depth in range(1,6):
  nxt=[];lower=[]
  for z in front:
   u,Q,D=info(A,z);om,psi=heights[z]
   for i,w in enumerate(moves(A,z)):
    h=(om-area(D[i]),psi) if i<len(D) else (om,psi-area(Q[i-len(D)]))
    if w in heights:assert heights[w]==h;continue
    heights[w]=h;nxt.append(w)
    if potential(name,(len(info(A,w)[1]),0,0,0,0,*h))<cost0:lower.append(w)
  if lower:rho=depth;break
  front=nxt
 row=dict(header=head,potential=name,radius=rho,visited=len(heights));out.append(row);print(row)
(BASE/'code/signed_radii.json').write_text(json.dumps(out,indent=2))
