"""Record actual key declaration headers, with source paths and line numbers."""
from pathlib import Path
import re
HERE=Path(__file__).resolve().parent
UP=HERE.parent/'2026-11-14_opus_lean-formalisation/upstream/openai-math/lean/OAI/Combinatorics/Hamiltonian'
NAMES=set('circuit_cut connected_shore region_euler mixed_corner_on_boundary state_disk_count disk_boundary_imbalance state_disk_delta boundary_of_sum_zero whiteCharge whiteCharge_cut_integral white_positive_of_boundary pair_nonempty forest_pair_of_disk_circulation removed_acyclic remainder_connected remainder_black_degree tree_matching recovery_matching matching_cut_balance selectNet_forest selected_forest recover_connected_complement cap_simple cap_cubic cap_threeConnected cap_coloring cap_glue_matching cap_glue_connected matching_strong connected_complement_matching weights weights_diff signed cycle_cut_scalar blackDelta_cut'.split())
out=['# Actual Lean statement extracts','',
     'Read from openai/math commit 4eaee87548250b2682affda7d05d947c05554bae. These are declaration headers from the existing upstream clone, not transcriptions from the earlier report. File-level variables and namespaces remain in the source. Our prose replaces the second network with the face-incidence relation of G; that interpretation is proved in Lemmas 2 and 3. No fresh Lean build was run by this agent. Regenerate with python research/2026-11-14_astra_primal-proof/extract_lean.py.','']
for path in sorted(UP.glob('*.lean')):
    s=path.read_text(encoding='utf-8')
    for m in re.finditer(r'^(?:private )?(?:theorem|lemma|def) ([\w.]+)',s,re.M):
        if m[1].split('.')[-1] not in NAMES:continue
        end=s.find(':=',m.start())
        out += [f'## {path.name}:{s[:m.start()].count(chr(10))+1}','','```lean',s[m.start():end].rstrip(),'```','']
(HERE/'LEAN-EXTRACTS.md').write_text('\n'.join(out),encoding='utf-8')
