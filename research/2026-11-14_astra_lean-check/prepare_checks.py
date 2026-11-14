from pathlib import Path
R=Path.cwd();D=R/'research/2026-11-14_astra_lean-check';P=Path('E:/lb2')
s=(R/'proofs/lean/Devices/Axioms.lean').read_text(encoding='utf-8')
checks=s.replace('#print axioms ','#check @')
(D/'Statements.lean').write_text('set_option pp.width 140\n'+checks if False else checks,encoding='utf-8')
# Full upstream definitions, with aliases expanded by source inspection in FAITHFULNESS.
extra=['OAI.Barnette.MainStatement','OAI.Barnette.TriangleSystem','OAI.Barnette.TriangleSystem.State','OAI.Barnette.TriangleSystem.Partner','OAI.Barnette.TriangleSystem.Pair','OAI.Barnette.TriangleSystem.oppositeGraph','OAI.Barnette.TriangleSystem.Pair.next','OAI.Barnette.CycleClass','OAI.Barnette.TriangleSystem.Pair.Group','OAI.Barnette.TriangleSystem.Pair.GroupIndex','OAI.Barnette.TriangleSystem.Pair.GroupIndex.representative','OAI.Barnette.TriangleSystem.Pair.cycleSlope','OAI.Barnette.TriangleSystem.Pair.minCycles','OAI.Barnette.Network.ColoredDual','OAI.Barnette.Network.ColoredDual.system','OAI.Barnette.Network.ColoredDual.nonroots','OAI.Barnette.Network.Duality','OAI.Barnette.Network.whiteCharge','OAI.Barnette.phase']
(D/'Definitions.lean').write_text('import Devices.Concrete\n'+''.join('#print '+n+'\n' for n in extra),encoding='utf-8')
for route,imp in [('original','OAI.Combinatorics.Hamiltonian.Main'),('replacement','PaperRoute.Main')]:
 text='import '+imp+'\nimport IndependentWalker\n'
 text+='#check (OAI.Barnette.main : OAI.Barnette.MainStatement)\n#print axioms OAI.Barnette.main\n#print OAI.Barnette.MainStatement\n'
 text+=f'#audit_closure OAI.Barnette.main to "{D.as_posix()}/{route}-closure.txt"\n'
 if route=='replacement':
  text+='#same_type OAI.Barnette.TriangleSystem.Pair.forest_pair_of_disk_circulation and OAI.Barnette.TriangleSystem.Pair.forest_pair_of_disk_circulation_real\n'
 (D/(route.title()+'Check.lean')).write_text(text,encoding='utf-8')
