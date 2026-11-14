"""Derived tables, generating functions, roots and validation; exact inputs."""
from transfer import *
from certify import recurrence
import sympy as sp
P=Path(__file__).resolve().parents[1];out={};z=sp.Symbol('z');x=sp.Symbol('x')
for name in ('certificates','HC-certificates','pair-certificates'):
    for r in json.loads((P/'data'/f'{name}.json').read_text()):
        c=r['recurrence'];d=len(c);den=1-sum(c[j]*z**(j+1) for j in range(d))
        init=r.get('initial_L0_onward',r.get('initial_L2_onward'))
        num=sp.expand(sum(init[j]*z**j for j in range(d))*den)
        num=sum(num.coeff(z,j)*z**j for j in range(d))
        char=x**d-sum(c[j]*x**(d-j-1) for j in range(d))
        roots=sp.polys.polytools.intervals(char,eps=sp.Rational(1,10**10))
        largest=max(float((a+b)/2) for (a,b),mult in roots)
        key=f"{r['width']}_{r.get('quantity','pairs')}"
        out[key]={'recurrence':c,'generating_numerator':str(num),'generating_denominator':str(den),'characteristic_factorization':str(sp.factor(char)),'largest_real_root':largest,'per_vertex_base':largest**(1/(2*r['width'])),'sequence_start_L':0 if 'initial_L0_onward' in r else 2}
checks=[]
for p in (4,6):
    transfer=json.loads((P/'data'/f'transfer{p}.json').read_text())
    direct=json.loads((P/'data'/f'tube{p}.json').read_text())
    for r in direct:
        L=r['parameter'];a=transfer[L]
        assert (a['states'],a['TM'],a['HC'])==(r['states'],r['tree_matchings'],r['HC'])
    cs=json.loads((P/'data'/'certificates.json').read_text())
    for r in cs:
        if r['width']!=p:continue
        field='TM' if r['quantity']=='TM' else 'states'
        for k,v in enumerate(r['scalar_sequence_L2_onward']):
            if k+2<len(transfer):assert v==transfer[k+2][field]
    hc_cert=next(r for r in json.loads((P/'data'/'HC-certificates.json').read_text()) if r['width']==p)
    for k,v in enumerate(hc_cert['scalar_sequence_L0_onward']):
        if k<len(transfer):assert v==transfer[k]['HC']
    checks.append({'width':p,'direct_enumeration_max_L':max(r['parameter'] for r in direct),'transfer_max_L':transfer[-1]['L'],'all_equal':True})
(P/'data'/'recurrences.json').write_text(json.dumps(out,indent=2));(P/'data'/'cross-checks.json').write_text(json.dumps(checks,indent=2))
print(json.dumps(out,indent=2))
