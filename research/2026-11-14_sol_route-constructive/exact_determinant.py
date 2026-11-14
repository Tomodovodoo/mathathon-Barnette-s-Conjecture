import sympy as s,json
from pathlib import Path
from barnette_lab import *
b=Instance.from_primal(named_graphs()['hexagonal_prism']); a=b.weights(); z=s.Rational(5,4); ys=s.symbols('y:'+str(b.n)); q=(s.sqrt(3)+s.I)/2
m=s.zeros(b.n)
for j,t in enumerate(b.A):
 for u in set(b.faces[t])&set(b.X):
  for v in (set(b.faces[t])&set(b.X))-{u}:
   phase=q if b.delta(u,v)==1 else s.conjugate(q)
   m[b.X.index(u),b.X.index(v)]+=ys[j]*phase*z**a.get((t,v),0)
f=s.expand(s.I**b.n*m.det(method='domain-ge'))
coefficient=f
for y in ys: coefficient=s.expand(coefficient).coeff(y,1)
coefficient=s.simplify(coefficient)
naive=s.simplify(f.subs(dict.fromkeys(ys,1)))
exact=sum(v*z**k for k,v in b.polynomial().items())
assert coefficient==exact and naive==0
out={'naive':str(naive),'coefficient':str(coefficient),'signed_sum':str(exact),'formula':str(s.simplify(f))}
Path('research/2026-11-14_sol_route-constructive/data/exact_determinant.json').write_text(json.dumps(out,indent=2))
print(out)
