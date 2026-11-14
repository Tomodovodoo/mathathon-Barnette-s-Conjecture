"""Freeze the exact sources and artifacts used in this audit."""
from pathlib import Path
import hashlib,json,platform,sys
from datetime import datetime,timezone
import networkx,scipy,sympy

P=Path(__file__).resolve().parent; ROOT=P.parents[2]
opus=ROOT/'research/2026-11-14_opus_route-graph-theory'; astra=ROOT/'research/2026-11-14_astra_limits'; fable=ROOT/'research/2026-11-14_fable_route-combinatorics'
inputs=list((ROOT/'papers').glob('*.pdf'))+list((ROOT/'papers/text').glob('*.txt'))
inputs += [ROOT/'research/BRIEF.md',ROOT/'README.md']
inputs += [ROOT/p for p in ['skills/reverse-lamport/SKILL.md','skills/reverse-lamport/references/worked-audit.md','skills/unslop/SKILL.md','skills/labyrinth-exploration/SKILL.md']]
inputs += [opus/f'code/data/eul_{v}.json' for v in range(6,15)]
inputs += list((opus/'code/data').glob('alpha_*fail*.json'))
inputs += [opus/'code/data'/p for p in ['ef_fail_40_40.json','strongviol_50_seed50.json','deeptrap_50_1.json','lp_13.txt']]
inputs += list((astra/'examples').glob('*.json'))+[astra/'data/strengthenings.json',astra/'data/non3connected_cut.json']
inputs += [d/name for d,names in [(opus,['REPORT.md','PROOFS.md','ROUTES.md']),(astra,['REPORT.md','HYPOTHESES.md','STRENGTHENINGS.md']),(fable,['REPORT.md','PROOF.md','data/counterexamples.txt'])] for name in names]
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def records(paths): return {str(p.relative_to(ROOT)).replace('\\','/'):digest(p) for p in sorted(set(paths))}
result={'generated_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'platform':platform.platform(),'libraries':{'networkx':networkx.__version__,'scipy':scipy.__version__,'sympy':sympy.__version__},'author_or_reference_code_executed':False,'inputs':records(inputs),'referee_programs':records(P.glob('*.py')),'outputs':records(p for p in P.glob('*.json') if p.name!='provenance.json')}
(P/'provenance.json').write_text(json.dumps(result,indent=2)+'\n'); print('Frozen',len(result['inputs']),'inputs and',len(result['outputs']),'outputs')
