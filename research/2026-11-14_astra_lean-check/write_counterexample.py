from pathlib import Path
import json,collections
D=Path('research/2026-11-14_astra_lean-check');j=json.loads((D/'numerical.json').read_text());example=next(h for h in j['T5_counterexample']['hamiltonian_cycles'] if not h['good'])
f=[(6,i,(i+1)%6) for i in range(6)]+[(7,(i+1)%6,i) for i in range(6)]
edges=collections.defaultdict(list)
for i,t in enumerate(f):
 for k in range(3):edges[tuple(sorted((t[k],t[(k+1)%3])))].append(i)
match={tuple(e) for e in example['matching']};adj=collections.defaultdict(list)
for e,(a,b) in edges.items():
 if e not in match:adj[a].append(b);adj[b].append(a)
cycle=[0];prev=None;v=0
while True:
 w=next(x for x in adj[v] if x!=prev)
 if w==0:break
 cycle.append(w);prev,v=v,w
print(cycle+[0]);print([edges[e] for e in match])
(D/'COUNTEREXAMPLE.md').write_text(f'''# Explicit counterexample to TODO T5\n\nREFUTED, with COMPUTED enumeration in numerical.py/numerical.json and the following direct verification, PROVED-HERE.\n\nTake the hexagonal bipyramid T. Its equator is 0,1,2,3,4,5 and its apices are 6,7. Its oriented upper faces are U_i=(6,i,i+1), its lower faces L_i=(7,i+1,i), with equatorial indices modulo 6. Colour U_0,U_2,U_4,L_1,L_3,L_5 black. Root at U_0, with roots 6,0,1, and prescribe side e0={{0,1}}. Its dual G is the hexagonal prism. Label U_i by i and L_i by 6+i.\n\nChoose the selection P with dual sides {{0,1}}, {{1,2}}, {{2,3}}, {{4,6}}, {{0,5}}, {{4,7}}. Each face contains exactly one selected side, so its primal dual edges form a perfect matching. The complement is the explicit Hamiltonian cycle\n\n    {' -> '.join(map(str,cycle+[0]))}.\n\nIt avoids the edge across e0 because e0 belongs to the matching. Thus P satisfies the premise of T5. Direct inspection of the two hexagons joined by their six spokes, or the deletion check in numerical.py, verifies cubicity, bipartiteness and three-vertex-connectivity. The usual prism embedding gives planarity.\n\nRemove e0 from the selected dual forest and orient its edges towards roots 6,0,1. On the five nonroot black faces U_2,U_4,L_1,L_3,L_5, the tails give the recovered state\n\n    s=(3,4,2,7,5).\n\nThese are precisely the five nonroot vertices, each once. Its opposite edges are {{6,2}}, {{6,5}}, {{7,1}}, {{4,3}}, {{7,0}}. The three components are {{6,2,5}}, {{7,1,0}}, and {{4,3}}. They contain respectively one, two, and zero roots. Q_s is acyclic but s is not good.\n\nNo other good state can recover P. If a good state recovered P, orienting its selected forest minus e0 towards the roots would recover that state, uniquely, since each rooted tree has a unique orientation towards its root. This same operation gives the non-good s above. Hence the universal claim in T5 is false. The conditional image characterisation in the current paper is consistent with this example.\n''',encoding='utf-8')
