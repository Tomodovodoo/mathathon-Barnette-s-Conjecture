"""Reproducible algorithm experiments. Each size has a fixed, biased sample."""
import argparse,json,time,random
from pathlib import Path
from collections import Counter
import networkx as nx
from barnette_lab.core import *
from barnette_lab.algorithms import *

parser=argparse.ArgumentParser(); parser.add_argument('--plantri',required=True,type=Path); parser.add_argument('--output',required=True,type=Path)
a=parser.parse_args(); rows=[]; witnesses=[]
for n in range(6,21):
 gs=list(plantri_graphs(n,a.plantri.resolve()))
 # Spread deterministic indices across the enumeration, at most 12 per size.
 ids=sorted(set(round(i*(len(gs)-1)/11) for i in range(12))) if gs else []
 for index in ids:
  b=Instance(gs[index]); p=b.flow_pair()
  if p is None: continue
  row={'dual_vertices':n,'primal_vertices':len(b.G),'index':index,'classes_at_size':len(gs)}
  st=Counter(); start=time.perf_counter(); s=b.enumerate_tree(st); row['enumeration_seconds']=time.perf_counter()-start; row['prefix_stats']=dict(st)
  start=time.perf_counter(); q,stats=marked_walk(b,p,cap=100000); row['marked_seconds']=time.perf_counter()-start; row['marked']=stats
  assert b.is_tree(s) and b.is_tree(q[1])
  # On small enough instances find all bad starts, rather than hiding them behind flow.
  if n<=17:
   ss=list(b.states()); ps=b.pairs(ss); bad=[q for q in ps if not b.is_tree(q[1])]
   row.update(states=len(ss),pairs=len(ps),bad_pairs=len(bad),tree_states=sum(b.is_tree(s) for s in ss))
   for pbad in bad[:4]:
    start=time.perf_counter(); q,stats=marked_walk(b,pbad,cap=100000)
    trials=[]
    for greedy in (False,True):
     runs=[exchange_walk(b,pbad,seed=seed,cap=1000,greedy=greedy) for seed in range(16)]
     trials.append({'greedy':greedy,'successes':sum(q is not None for q,k in runs),'steps':[k for q,k in runs]})
    witnesses.append({'n':n,'index':index,'T_edges':list(b.T.edges()),'pair':pbad,'marked':stats,'walk_trials':trials})
  if n<=16:
   start=time.perf_counter(); samples=[determinant_sample(b,seed) for seed in range(16)]
   row['determinant_sampling_seconds']=time.perf_counter()-start
   row['sample_tree_successes']=sum(b.is_tree(s) for s in samples)
  rows.append(row)
 print(n,len(gs),'rows',len(rows),'bad',len(witnesses),'max marked',max((w['marked']['moves'] for w in witnesses),default=0),flush=True)
 a.output.mkdir(exist_ok=True,parents=True)
 (a.output/'benchmarks.json').write_text(json.dumps(rows,indent=2))
 (a.output/'bad_starts.json').write_text(json.dumps(witnesses,indent=2))
