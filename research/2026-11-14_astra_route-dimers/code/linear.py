from explore import *
rows=json.loads((OUT/'data.json').read_text()); results=[]
for row in rows:
 g=nx.Graph(row['edges']); temp=Instance(g); b=Instance(g,next(i for i,f in enumerate(temp.faces) if set(f)==set(row['root_face']))); a=b.weights(); ss=list(b.states()); pairs=b.pairs(ss)
 coeff=Counter(); bystate=Counter()
 for r,s in pairs:
  sg=math.prod(b.delta(u,v) for u,v in zip(r,s));bystate[s]+=sg
  p=[1]
  for t,v in zip(b.A,s):
   w=a.get((t,v),0);nxt=[0]*(len(p)+1)
   for j,c in enumerate(p):nxt[j]+=c;nxt[j+1]+=w*c
   p=nxt
  for j,c in enumerate(p):coeff[j]+=sg*c
 coeff={k:v for k,v in coeff.items() if v}
 assert sum(c*c for c in bystate.values())==row['trees']
 if row['cmin'] is not None:
  assert min(coeff)==row['cmin']; pp=b.polynomial(); expected=sum(c*math.comb(k,row['cmin']) for k,c in pp.items()); assert coeff[row['cmin']]==expected
 else:assert not coeff
 results.append(dict(name=row['name'],linear_polynomial=coeff,norm=sum(c*c for c in bystate.values())))
(OUT/'linear_weights.json').write_text(json.dumps(results,indent=2))
print('18 linear-weight and norm checks passed')

