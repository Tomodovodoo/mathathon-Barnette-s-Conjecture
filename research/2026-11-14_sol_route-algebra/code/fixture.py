"""Append the saved 17-vertex restart fixture to an existing completed corpus."""
import sys,json
sys.dont_write_bytecode=True
from count import ROOT,OUT,Instance,primal_counts,rooted
import networkx as nx
d=json.loads((OUT/'counts.json').read_text())
f=json.loads((ROOT/'workings/barnette_lab/tests/fixtures/restart.json').read_text())
t=nx.Graph();t.add_edges_from(f['T_edges']);b=Instance(t);pc=primal_counts(b.G)
row=dict(name='fixture_restart',vertices=len(t),edges=sorted(t.edges()),primal=pc,
         roots=[rooted(t,o,pc) for o in range(len(b.faces))])
d['graphs']=[g for g in d['graphs'] if g['name']!='fixture_restart']+[row]
(OUT/'counts.json').write_text(json.dumps(d,indent=2));print(row['name'],len(row['roots']))
