import unittest
import json
from pathlib import Path
from itertools import combinations, product
import networkx as nx
from barnette_lab import Instance, named_graphs, check_cycle, hamiltonian_cycle
from barnette_lab.core import glue_triangles, edge, faces_of
from barnette_lab.algorithms import solve, determinant_sample, alpha, beta, marked_walk
from barnette_lab.verify import verify

class ProofTests(unittest.TestCase):
    def test_cube_all_outgoing_choices(self):
        row=verify(Instance.from_primal(named_graphs()['cube']),True)
        self.assertEqual(row['states'],2)
        self.assertEqual(row['exchange_components'],1)

    def test_all_cube_incidence_forests_dual_connected(self):
        b=Instance.from_primal(named_graphs()['cube'])
        # Inherited spoke embedding is implicit in the white-side correspondence.
        # Use the planar embedding of this subdivided K4, whose embedding is unique.
        _,emb=nx.check_planarity(b.H)
        fs,sides=faces_of(emb)
        es=list(b.H.edges())
        for bits in product((0,1),repeat=len(es)):
            forest=nx.Graph(); forest.add_nodes_from(b.H)
            selected=[e for e,bit in zip(es,bits) if bit]
            forest.add_edges_from(selected)
            if not nx.is_forest(forest): continue
            d=nx.MultiGraph(); d.add_nodes_from(range(len(fs)))
            for (u,v),bit in zip(es,bits):
                if not bit: d.add_edge(sides[u,v],sides[v,u])
            self.assertTrue(nx.is_connected(d))
            if nx.is_tree(forest): self.assertTrue(nx.is_tree(d))

    def test_separator_both_boundary_colors(self):
        t=glue_triangles(nx.octahedral_graph(),nx.octahedral_graph())
        for root in range(14):
            b=Instance(t,root)
            for e in combinations(b.faces[root],2):
                result=solve(b,e)
                self.assertTrue(check_cycle(b.G,result['cycle'],result['avoided_edge']))
                self.assertTrue(all(nx.is_tree(b.T.subgraph(c)) for c in result['classes']))

    def test_sampling_stays_a_state(self):
        b=Instance.from_primal(named_graphs()['hexagonal_prism'])
        self.assertEqual({determinant_sample(b,seed) for seed in range(100)},set(b.states()))

    def test_named_graphs(self):
        for name,g in named_graphs().items():
            b=Instance.from_primal(g)
            s=b.enumerate_tree()
            self.assertTrue(b.is_tree(s),name)
            r=b.recover(s)
            self.assertTrue(check_cycle(b.G,r['cycle'],r['avoided_edge']))

    def test_every_input_edge_named_graphs(self):
        for name,g in named_graphs().items():
            for e in g.edges():
                self.assertTrue(check_cycle(g,hamiltonian_cycle(g,e),e),name)

    def test_cyclic_cancellation_fixture(self):
        data=json.loads((Path(__file__).parent/'fixtures/cyclic.json').read_text())
        b=Instance(nx.Graph(data['T_edges']))
        p=tuple(map(tuple,data['pair']))
        self.assertFalse(b.is_tree(p[1]))
        row=verify(b)
        self.assertEqual(row['pairs'],10)
        self.assertEqual(row['tree_states'],8)

    def test_marked_restart_fixture(self):
        data=json.loads((Path(__file__).parent/'fixtures/restart.json').read_text())
        b=Instance(nx.Graph(data['T_edges']))
        p=tuple(map(tuple,data['pair']))
        result,stats=marked_walk(b,p)
        self.assertTrue(b.is_tree(result[1]))
        self.assertEqual(stats['restarts'],[[4,2]])
        self.assertEqual(stats['moves'],3)

    def test_checker_rejects_bad_certificates(self):
        b=Instance.from_primal(named_graphs()['cube'])
        c=b.recover(b.enumerate_tree())
        self.assertFalse(check_cycle(b.G,c['cycle'][:-1],c['avoided_edge']))
        self.assertFalse(check_cycle(b.G,c['cycle'],c['cycle'][:2]))

if __name__=='__main__': unittest.main()
