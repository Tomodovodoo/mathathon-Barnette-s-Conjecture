from experiment import *
r=json.loads((ROOT/'data/results.json').read_text()); t=r['heawood_torus']; a=t['black_vertices']; fs=t['faces']; corners={int(k):v for k,v in t['corners'].items()}; rot={int(k):v for k,v in t['rotation'].items()}
order={v:[next(i for i,f in enumerate(fs) if any(x==v and y==w for x,y in zip(f,f[1:]+f[:1]))) for w in rot[v]] for v in a}
def delta(v,x,y): return 1 if (order[v].index(y)-order[v].index(x))%3==1 else -1
ss=[s for s in it.permutations(range(7)) if all(s[i] in corners[v] for i,v in enumerate(a))]
out=[]; dsum={}; evenq=None
for s in ss:
 q=nx.Graph(); q.add_nodes_from(range(7)); q.add_edges_from(tuple(x for x in corners[v] if x!=s[i]) for i,v in enumerate(a)); cyc=nx.cycle_basis(q); coef=0; mates=0
 for rr in ss:
  if any(x==y for x,y in zip(rr,s)): continue
  mates+=1; eps=1
  for i,v in enumerate(a): eps*=delta(v,rr[i],s[i])
  coef+=eps; z=sum(delta(v,rr[i],s[i]) for i,v in enumerate(a)); dsum[z]=dsum.get(z,0)+1
 out.append(dict(s=s,Q_cycles=cyc,coefficient=coef,mates=mates))
 if any(len(c)%2==0 for c in cyc) and evenq is None: evenq=out[-1]
result={'order':order,'D_delta_sum':dsum,'states':out,'first_even_Q':evenq,'nonzero_coefficients':sum(x['coefficient']!=0 for x in out)}
(ROOT/'data/torus_signs.json').write_text(json.dumps(result,indent=2)); print(json.dumps({k:v for k,v in result.items() if k!='states'},indent=2))
# Triple boundary signatures, abstract paths are represented as edges on terminals.
patterns=[((i,(i+1)%4),) for i in range(4)]+[((0,1),(2,3)),((0,3),(1,2))]
valid=[]
for ix in it.product(range(6),repeat=3):
 h=nx.MultiGraph(); h.add_nodes_from(range(4))
 for j in ix: h.add_edges_from(patterns[j])
 if all(d==2 for v,d in h.degree()) and nx.is_connected(h): valid.append(ix)
(ROOT/'data/patterns.json').write_text(json.dumps({'patterns':patterns,'compatible_triples':valid},indent=2)); print('compatible triples',len(valid))
# Use the planar reference implementation without writing bytecode in it.
sys.dont_write_bytecode=True; sys.path.insert(0,str(ROOT.parents[1]/'workings/barnette_lab'))
from barnette_lab import hamiltonian_cycle, check_cycle
print('reference cube',hamiltonian_cycle(nx.cubical_graph(),(0,1)))
