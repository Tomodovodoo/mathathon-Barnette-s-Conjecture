import json,numpy as np
from pathlib import Path
from scipy.optimize import minimize
O=Path(__file__).parent;d=json.loads((O/'example.json').read_text());X=d['X'];xy={int(k):np.array(v) for k,v in d['coordinates'].items()};F=d['faces'][1:]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
signs=[np.sign(cross(xy[b]-xy[a],xy[c]-xy[a])) for a,b,c in F]
def unpack(z):return xy|dict(zip(X,z.reshape(-1,2)))
def areas(z):
 p=unpack(z);return np.array([sgn*cross(p[b]-p[a],p[c]-p[a]) for (a,b,c),sgn in zip(F,signs)])-1.0
def loss(z):
 p=np.array(list(unpack(z).values()));ds=((p[:,None,:]-p[None,:,:])**2).sum(2);return sum(1/(ds[i,j]+.01) for i in range(len(p)) for j in range(i)) - 2*sum(np.log(np.maximum(areas(z)+1.0,.00001)))
z=minimize(loss,np.array([xy[v] for v in X]).ravel(),constraints=[dict(type='ineq',fun=areas)],method='SLSQP',options=dict(maxiter=1000,ftol=1e-10))
assert z.success and min(areas(z.x))>-.00001
(O/'layout.json').write_text(json.dumps({str(v):p.tolist() for v,p in unpack(z.x).items()},indent=2));print(z.fun)
