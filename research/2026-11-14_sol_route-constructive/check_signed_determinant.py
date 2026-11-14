import numpy as np,cmath,json
from barnette_lab import *
from barnette_lab.core import *
from pathlib import Path
rows=[]
for name,g in named_graphs().items():
 b=Instance.from_primal(g); a=b.weights(); z=1.25
 m=np.zeros((b.n,b.n),dtype=complex)
 for t in b.A:
  for u in set(b.faces[t])&set(b.X):
   for v in set(b.faces[t])&set(b.X)-{u}:
    m[b.X.index(u),b.X.index(v)]+=cmath.exp(1j*np.pi/6*b.delta(u,v))*z**a.get((t,v),0)
 naive=(1j**b.n)*np.linalg.det(m)
 exact=sum(c*z**k for k,c in b.polynomial().items())
 rows.append({'name':name,'z':z,'naive_determinant_real':naive.real,'naive_determinant_imag':naive.imag,'exact_signed_polynomial':exact,'error':abs(naive-exact)})
print(rows)
Path('research/2026-11-14_sol_route-constructive/data/naive_determinant.json').write_text(json.dumps(rows,indent=2))
