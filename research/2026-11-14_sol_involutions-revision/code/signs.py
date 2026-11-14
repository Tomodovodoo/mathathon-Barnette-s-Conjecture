from itertools import permutations
from pathlib import Path
import json
from check import Check,enumerate_classes,from_code,run_checked,OUT
for orient in (-1,1):
    cyclic={(0,1),(1,2),(2,0)}
    delta=lambda a,b:orient*(1 if (a,b) in cyclic else -1)
    for r,s,u in permutations(range(3)):
        assert delta(u,s)-delta(r,s)==2*delta(r,u)
for n in range(1,101):
    for J in range(-n,n+1,2):
        assert (-1)**((n+J)//2)==(-1)**((n+1)//2)*(-1)**(J//2)
    for m in range(1,n+1):
        if n%2==m%2:
            assert (n+1)//2+m//2==(n+m)//2
            for q in range(m+1):assert (m-2*q)//2+q==m//2
T=from_code(enumerate_classes(6)[6][0]);b=Check(T.faces,0);r=run_checked(b)
assert b.n==3 and r['m']==1 and r['F']==1 and r['moment']==1
(OUT/'signs.json').write_text(json.dumps(dict(command='python research/2026-11-14_sol_involutions-revision/code/signs.py',local_triangle_orders=12,integer_phase_range='1<=n<=100, -n<=J<=n, J=n mod 2; all 1<=m<=n with n=m mod 2 and all 0<=q<=m',octahedron=r),indent=1))
