"""python -B -m barnette_lab.optimized input.json

Input: {"edges": [[u,v], ...], "forbidden": [u,v], "vertices": [...]}
Vertices is optional. Labels must be JSON strings or integers.
"""
import argparse
import json
from collections import Counter
from pathlib import Path
import networkx as nx
from . import hamiltonian_cycle

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('input', type=Path)
args = p.parse_args()
data = json.loads(args.input.read_text(encoding='utf-8'))
g = nx.Graph()
g.add_nodes_from(data.get('vertices', []))
g.add_edges_from(data['edges'])
stats = Counter()
cycle = hamiltonian_cycle(g, data['forbidden'], stats)
print(json.dumps({'cycle': cycle, 'stats': stats}))
