"""Focused guards for the counted campaign; exhaustive work lives in campaign.py."""
import unittest
from collections import Counter
from itertools import combinations, product
import networkx as nx
from barnette_lab import Instance, named_graphs
from barnette_lab.algorithms import white_ground
from barnette_lab.campaign import Coverage, require, recovery_state, sampler


class CampaignTests(unittest.TestCase):
    def test_require_never_uses_optimizable_assert(self):
        with self.assertRaisesRegex(AssertionError, 'sentinel'):
            require(False, 'sentinel')

    def test_coverage_separates_vacuous_runs(self):
        cov = Coverage()
        cov.hit('cancellation', 0); cov.finish()
        cov.hit('cancellation', 2); cov.finish()
        self.assertEqual(cov.rows['cancellation'], [1, 2, 1])

    def test_hexagonal_prism_all_relaxation_bases(self):
        b = Instance.from_primal(named_graphs()['hexagonal_prism'])
        ground = {(t,v):(y,z) for t,v,y,z in white_ground(b)}
        valid = Counter()
        for s in product(*[sorted(set(b.faces[t]) & set(b.X)) for t in b.A]):
            g = nx.MultiGraph(); g.add_nodes_from(b.white)
            g.add_edges_from(ground[t,v] for t,v in zip(b.A,s))
            if nx.is_tree(g): valid[b.valid(s)] += 1
        self.assertEqual(valid, {True:2, False:4})

    def test_recovery_left_inverse_all_cube_prescriptions(self):
        b = Instance.from_primal(named_graphs()['cube'])
        for e in combinations(b.faces[b.outer],2):
            e=tuple(sorted(e))
            for s in b.states():
                result=b.recover(s,e)
                self.assertEqual(recovery_state(b,result['P'],e),s)

    def test_sampler_exact_and_seeded_chi_square(self):
        b = Instance.from_primal(named_graphs()['hexagonal_prism'])
        result = sampler(b,Coverage(),samples=600)
        self.assertLess(result['chi_square'],result['cutoff'])

if __name__ == '__main__': unittest.main()
