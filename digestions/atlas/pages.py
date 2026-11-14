"""Page texts for the atlas. Plain words, 80 to 150 words of body plus status.
Provenance goes in `sources`, which build.py sets in the appendix table."""
PAGES = []
SHORT = {}
OA = 'papers/OpenAI-Barnette.pdf'
LI = 'papers/A-Note-On-Barnette.pdf'
BT = 'papers/barnette_trees.pdf'
RS = 'research/2026-11-14_'
HERE = 'computed by digestions/atlas/build.py'


def page(slug, short, title, group, text, status, see, sources, caption=None):
    SHORT[slug] = short
    PAGES.append(dict(slug=slug, title=title, group=group, text=' '.join(text.split()),
                      status=r'\textbf{Status.} ' + ' '.join(status.split()), see=see, sources=sources, caption=caption))


INTRO = (r'Readings of one proof, each drawn on a computed example. The proof is the one in the OpenAI paper: '
         r'every cubic, bipartite, 3-connected planar graph $G$ has a Hamiltonian cycle. '
         r'Most pages use one triangulation $T$ with 13 vertices, the dual of a graph $G$ with 22 vertices. '
         r'Black faces of $T$ are grey, the outer black face is the grey collar, and the three roots are hollow. '
         r'A state is a set of filled corner wedges, one in each black face. '
         r'Page 1 is the map. The last page lists where each picture and number comes from.')
SOURCES_INTRO = ('Each row lists the papers, the project reports and the computation behind one page. '
                 'Paths are relative to the repository root. The build script draws every figure from objects it computes and asserts, '
                 'and it writes the certificates to computed.json next to the atlas. '
                 'Where a row says a report is unrefereed, no second model has checked it. A check by a second model is not peer review. '
                 'A second model audited an earlier atlas page by page. The latest repair was rechecked on pages 24, 26, 29 and 30. '
                 'No human mathematician has read any page of it.')

G1, G2, G3, G4, G5, G6 = 'main chain', 'linear algebra', 'order', 'trees', 'cutting', 'scope'

page('chain', 'the chain', 'The chain, and where the routes branch', G1, r'''
Read the stations in order. The proof turns a cubic graph into its dual triangulation, finds two states that disagree at every black face,
and shows that some state is good: its opposite edges form three trees, one at each root. From such a state, three forced steps build the Hamiltonian cycle.
Only the step from station 5 to station 6 is hard, and the atlas has four readings of it. They are four ways to organise one argument,
a signed sum that cancels the cyclic states and still cannot vanish. They are not four proofs.
The stubs are shortcuts that this project tested and refuted with explicit examples.
The dotted line marks two routes that would avoid the sum. Neither is proved.''',
     r'''The chain is the proof in the OpenAI paper, Sections 3 to 7. Every thumbnail is computed on the running example.''',
     ['pairs', 'disk', 'sum', 'recovery', 'open'], [OA + ', Sections 3 to 7', 'digestions/route-map/ROUTE-MAP.md', HERE])

page('pairs', 'two states', 'Two states from one count', G1, r'''
A state gives each bounded black face one of its corners, uses no root, and uses every other vertex once.
The proof needs two states that disagree at every face. A doubled form of Hall's theorem says they exist when every set $S$ of non-root vertices passes one count.
Each black face scores the number of its corners in $S$, capped at two, and the scores must add up to at least $2|S|$.
The count can fail. In (c) a separating triangle has black faces just inside it, the three vertices inside score five against a required six, and no pair exists.
The paper cuts along separating triangles first, so that the count passes on every piece.''',
     r'''OpenAI paper, Proposition 3.1 and Section 7. The checker tests all 1024 sets $S$ on the running example and the failing set in (c).''',
     ['chain', 'dimers', 'matroids', 'cuts'], [OA + ', Proposition 3.1, Section 7', 'toolkit/check.py (cut inequality for all subsets)', HERE])

page('disk', 'disk identity', 'The disk identity, three ways', G1, r'''
Take a cycle of $D$ and the disk it bounds on the side away from the root face. Three arguments reach the same fact about that disk.
Euler's formula, with one wedge for each black face inside, gives $3(B-W)=2\ell-h$.
Shading shows one more white face than black.
Reading corners as angles makes the disk flat, so its boundary turns exactly once.
Each version says the same thing about a walk around the cycle. Black faces lie on the left three more times than on the right, or three fewer if the walk is clockwise.
That fixed number is why the signs on page @sum@ behave.''',
     r'''Lemma 4.1 of the OpenAI paper. The shading and turning versions were proved in this project and checked by a second model. No human has read them.''',
     ['sum', 'polynomial', 'primal', 'hypotheses'],
     [OA + ', Lemma 4.1', RS + 'astra_referee-combinatorics/REWRITTEN-PROP-5-1.md', RS + 'opus_route-topology/TOPOLOGY.md, Section 2',
      RS + 'fable_referee-topology/REFEREE.md, parts a and b', HERE])

page('sum', 'exponential sum', 'Eight terms, grouped twice', G1, r'''
Give every state $s$ an exponent, its volume from page @heights@, and every pair $(r,s)$ a sign read off the cycles of $D$.
The eight pairs of the running example give eight terms $\pm e^{vx}$.
Group them by $s$. The two pairs that share a cyclic $Q_s$ cancel, so only good states survive.
Group the same terms by the cover, the set of cycles of $D$ with their directions forgotten. Each group factors into one bracket per cycle, no bracket vanishes identically,
and by the disk identity the groups with the fewest cycles agree in sign at lowest order.
So the sum is not zero and a good state exists. The argument does not say which state.''',
     r'''OpenAI paper, Section 5. All eight terms and both factorisations are computed here.''',
     ['disk', 'polynomial', 'involutions', 'heights', 'rowdep'], [OA + ', Proposition 5.1, Lemmas 5.2 and 5.3', HERE + ' (lib.py: term, group_data)'])

page('polynomial', 'integer polynomial', 'The same sum as an integer polynomial', G1, r'''
Replace the exponential by a polynomial. Each pair contributes plus or minus a product of variables, one for each black face, picked by $s$.
Cyclic states still cancel, because the two cancelling pairs pick the same variables.
With every variable equal to one the polynomial is zero, since the signs balance.
Move every variable a little in the direction of the spoke weights. Each cycle of $D$ then contributes the number of white faces inside it,
and the lowest coefficient is a sum of positive products, here $6+3=9$.
This version has integer coefficients and no analysis. The geometric input is unchanged, since positivity still comes from white faces inside disks.''',
     r'''Proved in this project and checked by a second model. Not read by a human. The coefficients are computed here.''',
     ['sum', 'disk', 'determinant', 'heights'],
     [RS + 'fable_referee-determinants/SIGNIFICANCE.md, Section 2', BT + ' (signed integer polynomial)', HERE + ' (lib.py: Fpoly)'])

page('involutions', 'involutions', 'Cancellation as a pairing of objects', G1, r'''
Li's note replaces the sum by two pairings. If $Q_s$ has a cycle, move $r$ to the third corner on each of its faces, as in (a) and (b).
The new pair has the same $s$ and weight and the opposite sign, so the two cancel. With $q$ cycles a state has $2^q$ partners, and they pair off.
The second pairing shows that the good states do not cancel.
Reversing a cycle of $D$ flips the sign but changes the weight, so Li adds marks where a fixed ray from a white face crosses a spoke of $s$. Crossings along a ray pair off, and (c) and (d) move one mark to its partner.''',
     r'''Li's note, Definitions 13 to 23. Two models checked this project's write-up of both pairings on 1,206 examples.
     The panels are computed here. Page @keystep@ draws a complete marked object. Not read by a human.''',
     ['sum', 'rowdep', 'lattice'],
     [LI + ', Definitions 13 to 23, Appendix B', 'proofs/involutions/INVOLUTIONS.md (both pairings in full)', RS + 'opus_referee-involutions/REPORT.md',
      RS + 'fable_referee-involutions-v2/REPORT.md', RS + 'sol_atlas-audit/code/proposed.py (ray panel proposed there; recomputed here)',
      RS + 'fable_referee-topology/REFEREE.md, part d (Morse reading)', HERE + ' (figs_chain.py: crossing parity asserted on all 176 pair, cycle, white-face triples)'])

page('heights', 'heights', 'The exponent is a volume', G1, r'''
The exponent has a picture. Fix the lowest state and compare any other state with it.
The two differ along closed curves, and each white face gets the number of those curves that wind around it. That number is its height.
One clock move turns the wedges around a white face and raises that face by one.
The volume of a state is the sum of its heights, and the exponential sum weighs $s$ by $e$ to the volume times $x$.
So the analytic weights count white faces under a surface, and reversing a cycle of $D$ changes the volume by the number of white faces inside the cycle.''',
     r'''Proved in this project, with a corrected normalisation, and checked by a second model. Not read by a human. The heights of all twelve states are solved exactly here.''',
     ['sum', 'lattice', 'polynomial'],
     [RS + 'astra_referee-combinatorics/REFEREE.md', RS + 'fable_referee-topology/REPORT.md (height as winding number)', HERE + ' (lib.py: heights)'])

page('recovery', 'recovery', 'From a good state to the cycle', G1, r'''
Once a state is good, its opposite edges forming one tree per root, no choices remain.
Delete the chosen spoke in every black face. What remains of the spoke graph is a spanning tree,
so the curves that cross the deleted spokes form a tree on the white faces. Root that tree at the white face next to the prescribed edge $e$.
Each tree edge runs past two sides of one black face, and the side facing away from the root of the tree joins the selection.
The selection, with $e$, splits the vertices of $T$ into two classes that each induce a tree.
The boundary between the classes is one closed curve through every face. In $G$ it is a Hamiltonian cycle that avoids $e$.''',
     r'''OpenAI paper, Section 6. Every object in the four panels is asserted by the checker and agrees with the independent laboratory code.''',
     ['chain', 'primal', 'rainbow', 'produced', 'earlier'], [OA + ', Section 6', BT + ' (recovery criterion)', 'toolkit/model.py (recover)', HERE])

page('primal', 'primal picture', 'The same proof inside the cubic graph', G1, r'''
Li's note and this project's primal write-up keep everything inside $G$. The vertices of $G$ are the faces of $T$,
so black faces become black vertices and the vertices of $T$ become the faces of $G$.
A state lets each black vertex choose one of its three faces. A cycle of $D$ becomes an edge cut, and its disk becomes the shore of that cut away from the root vertex.
The disk identity says the shore has one more white vertex than black.
The outcome also needs no duality. Removing a perfect matching that contains $e$ leaves a single cycle.
The proof gets no shorter. The gain is that the inside of a curve becomes a shore of a cut, which a proof assistant can handle.''',
     r'''Written in this project, refereed by a second model, revised, and accepted in a cross-audit. Not read by a human.''',
     ['disk', 'recovery', 'keystep', 'blueprint', 'cuts'],
     [LI, 'proofs/primal/', RS + 'astra_primal-proof/', RS + 'fable_referee-primal/', RS + 'opus_lean-formalisation/REPORT.md', RS + 'opus_cross-audit/', HERE])

import pages_more  # noqa: E402,F401

# Reading order. It follows the chain of page 1, with the heights before the sum that uses them,
# the three-proofs comparison after the primal page, and the scope pages last (see README, "Order").
ORDER = ['chain', 'pairs', 'disk', 'heights', 'sum', 'polynomial', 'involutions', 'recovery', 'primal', 'keystep',
         'rowdep', 'determinant', 'dimers', 'lattice', 'pairlattice', 'canonical', 'matroids', 'lp',
         'rainbow', 'random', 'trinity', 'cuts', 'induction', 'earlier', 'produced', 'families', 'hypotheses', 'pfaffian',
         'blueprint', 'open']
assert sorted(ORDER) == sorted(p['slug'] for p in PAGES)
PAGES.sort(key=lambda p: ORDER.index(p['slug']))
_num = {p['slug']: i + 1 for i, p in enumerate(PAGES)}
import re as _re
for _p in PAGES:
    for _k in ('text', 'status'):
        _p[_k] = _re.sub(r'@(\w+)@', lambda _m: str(_num[_m.group(1)]), _p[_k])
