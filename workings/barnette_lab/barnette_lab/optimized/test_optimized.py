import unittest
from collections import Counter
import networkx as nx
from barnette_lab.core import Instance, generated, named_graphs, plantri_graphs
from barnette_lab.optimized import enumerate_tree, hamiltonian_cycle, verify
from barnette_lab.optimized.path import path_tree, BudgetExceeded


class SearchTests(unittest.TestCase):
    def test_every_root_small(self):
        for t in generated(10):
            for root in range(len(Instance(t).faces)):
                b = Instance(t, root)
                expected = [s for s in b.states() if b.is_tree(s)]
                dp = path_tree(b)
                self.assertEqual(dp is not None, bool(expected))
                if dp is not None:
                    self.assertIn(dp, expected)
                for mrv in (False, True):
                    s = enumerate_tree(b, mrv=mrv)
                    self.assertEqual(s is not None, bool(expected))
                    if s is not None:
                        self.assertIn(s, expected)

    def test_all_prescriptions(self):
        for name, g in named_graphs().items():
            for e in g.edges():
                c = hamiltonian_cycle(g, e)
                self.assertTrue(verify(g, c, e), (name, e))

    def test_labels_and_bad_certificate(self):
        g = nx.relabel_nodes(nx.cubical_graph(), lambda x: 'vertex-' + str(x))
        e = next(iter(g.edges()))
        c = hamiltonian_cycle(g, e)
        self.assertTrue(verify(g, c, e))
        self.assertFalse(verify(g, c[:-1], e))
        self.assertFalse(verify(g, [c[0]] * len(g), e))
        self.assertFalse(verify(g, c, (c[0], c[1])))
        with self.assertRaises(BudgetExceeded):
            path_tree(Instance(nx.octahedral_graph()), width_limit=1)


if __name__ == '__main__':
    unittest.main()
