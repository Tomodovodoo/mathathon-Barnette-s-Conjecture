from pathlib import Path
import itertools, json
import sympy as S
P=Path(__file__).resolve().parent
q=S.Symbol('q'); modulus=q**4-q**2+1
def norm(x):
 x=S.expand(x*q**(12*20)) if False else S.expand(x)
 # Replace negative powers using q^12=1 before polynomial reduction.
 x=S.expand(sum(c*q**(int(e[0])%12) for e,c in S.Poly(S.expand(x*q**120),q).terms())) if any(p.exp<0 for p in x.atoms(S.Pow) if p.base==q) else x
 return S.rem(x,modulus,q).expand()
# Two n-gonal bipyramids, with facial orientation fixed directly.
results=[]
for m in (4,6):
 faces=[]
 for j in range(m):
  faces.extend([(m,j,(j+1)%m), (m+1,(j+1)%m,j)])
 black=[f for i,f in enumerate(faces) if (i//2+i%2)%2==0]
 outer=black[0]; A=black[1:]; X=sorted(set(range(m+2))-set(outer)); n=len(A)
 states=[p for p in itertools.permutations(X) if all(p[j] in f for j,f in enumerate(A))]
 z=S.symbols('z:'+str(n)); M=S.zeros(n); pos={v:i for i,v in enumerate(X)}
 delta={}
 for j,f in enumerate(A):
  for u,v in itertools.permutations(f,2):
   d=1 if any(f[k]==u and f[(k+1)%3]==v for k in range(3)) else -1
   delta[j,u,v]=d
   if u in pos and v in pos: M[pos[u],pos[v]]+=z[j]*q**(d%12)*(1+3*j+pos[v])
 det=S.Poly(M.det(method='domain-ge'),*z).coeff_monomial(S.prod(z)); det=norm(det)
 direct=0; pairs=0
 for r,s in itertools.product(states,repeat=2):
  if any(u==v for u,v in zip(r,s)):continue
  pairs+=1; d=sum(delta[j,r[j],s[j]] for j in range(n))
  assert d%3==0
  direct+=q**(d%12)*S.prod(1+3*j+pos[s[j]] for j in range(n))
 direct=norm(direct); assert norm(det-direct)==0
 results.append({'rim':m,'n':n,'states':len(states),'ordered_disjoint_pairs':pairs,'determinant_coefficient':str(det),'direct_pair_sum':str(direct)})
 print(results[-1],flush=True)
(P/'determinant-check.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
