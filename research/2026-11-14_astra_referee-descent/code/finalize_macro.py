from check import *
from potentials import geometry,potential
import copy
path=BASE/'code/macro40.json';found=json.loads(path.read_text());names=['(k,'+a+'om,'+b+'psi)' for a in ('+','-') for b in ('+','-')]+['(k,'+a+'psi,'+b+'om)' for a in ('+','-') for b in ('+','-')]
flip=lambda name:name.translate(str.maketrans({'+':'-','-':'+'}))
for name in names:
 if name not in found:
  d=copy.deepcopy(found[flip(name)]);d['rotation']=[ns[::-1] for ns in d['rotation']];d['reflected_from']=flip(name);found[name]=d
for name,d in found.items():
 A=[tuple(f) for f in d['A']];p=tuple(tuple(s) for s in d['pair']);area=geometry(d['rotation'],d['root']);h={p:(0,0)};front=[p];initial=potential(name,(len(info(A,p)[1]),0,0,0,0,0,0))
 for depth in (1,2):
  nxt=[]
  for z in front:
   u,Q,D=info(A,z);om,psi=h[z]
   for i,w in enumerate(moves(A,z)):
    hh=(om-area(D[i]),psi) if i<len(D) else (om,psi-area(Q[i-len(D)]))
    if w in h:assert h[w]==hh;continue
    h[w]=hh;nxt.append(w);assert potential(name,(len(info(A,w)[1]),0,0,0,0,*hh))>=initial
  front=nxt
 d['radius_two_verified']=True
path.write_text(json.dumps(found,indent=2));print('verified',len(found),'signed radius-two obstructions')
