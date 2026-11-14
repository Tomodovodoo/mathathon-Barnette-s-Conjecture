from campaign import *
from special import dual_multi
x=json.load(open(OUT/'examples/theta_cube_26.json'));g=nx.Graph(x['edges']);d,fs,corners=dual_multi(g);col=nx.bipartite.color(g);root=0;A=sorted(v for v in g if v!=root and col[v]==col[root]);X=sorted(set(d)-set(corners[root]));best=(0,[])
for bits in range(1<<len(X)):
 S={v for i,v in enumerate(X) if bits>>i&1};deficit=2*len(S)-sum(min(2,len(set(corners[t])&S)) for t in A)
 if deficit>best[0]:best=(deficit,sorted(S))
H=nx.Graph();H.add_edges_from((('t',t),('v',v)) for t in [root]+A for v in corners[t]);fake=Instance.__new__(Instance);fake.A=A;fake.X=X;fake.n=len(A);fake.faces=corners
states=[]
for s in fake.states():
 h=H.copy();h.remove_edges_from((('t',t),('v',v)) for t,v in zip(A,s));states.append({'s':s,'H_minus_s_connected':nx.is_connected(h),'cycle_rank':h.number_of_edges()-len(h)+nx.number_connected_components(h)})
save('data/non3connected_cut.json',{'root':root,'A':A,'X':X,'S':best[1],'deficit':best[0],'states':states});event('Theta26 root0 capacity obstruction and all eight incidence complements checked')
print(best,states)
