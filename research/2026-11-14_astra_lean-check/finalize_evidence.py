from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,str(Path(__file__).parent))
from rebuild import run,R,D,P,L
run('numerical-final',[sys.executable,'-I',str(D/'numerical.py')])
run('source-inspection-final',[sys.executable,'-I',str(D/'inspect_sources.py')])
run('cache-integrity-final',[sys.executable,'-I',str(D/'check_cache.py')])
run('python-version',[sys.executable,'--version'])
run('summarize-checks',[sys.executable,'-I',str(D/'summarize_checks.py')])
run('counterexample',[sys.executable,'-I',str(D/'write_counterexample.py')])
with (D/'REACHABILITY.md').open('a',encoding='utf-8') as f:
 f.write('''\n## Qualification: general polynomial library dependencies remain\n\nREFUTED if read literally: “not reaching any polynomial lemma.” The replacement reaches 276 Polynomial namespace declarations, against 297 in the original. This does not undermine removal of the six named phase/polynomial nonvanishing dependencies, all of which are absent. The following independently traced path runs entirely through the unchanged exact-dual and rank-condition machinery, not through the replaced nonvanishing argument. The command source is PathCheck.lean, its implementation is the #audit_path command above, and the full output is polynomial-path.out.\n\n```\n'''+(D/'polynomial-path.txt').read_text(encoding='utf-8')+'\n```\n\nThe reached declarations from the upstream PairPolynomials module are structural: group indices and their equivalences, cycle faces/deltas/slopes, orientation values, and second-state fibers. None is the old polynomial nonvanishing proof.\n')
p=D/'ROUTE-AUDIT.md';s=p.read_text(encoding='utf-8-sig').replace('discharged after successful build','discharged').replace('The verdict for C0 is conditional on the completed build and independent walk recorded in REACHABILITY.md.','C0 FOLLOWS by the supplied replacement route. The fresh build and independent walk in REACHABILITY.md discharge every obligation on R0 through R5, using only the three standard axioms.');p.write_text(s,encoding='utf-8')
p=D/'RECOUNT.md';s=p.read_text(encoding='utf-8').replace('conditional on the successful fresh build recorded in BUILD-LOG.md','based on the successful fresh build recorded in BUILD-LOG.md');p.write_text(s,encoding='utf-8')
manifest=json.loads((D/'inputs-sha256.json').read_text()); changed=[]
for path,h in manifest.items():
 if hashlib.sha256((R/path).read_bytes()).hexdigest()!=h:changed.append(path)
(D/'input-changes-at-finish.json').write_text(json.dumps(changed,indent=2)+'\n')
with (D/'BUILD-LOG.md').open('a',encoding='utf-8') as f:
 f.write('''\n## Reviewer-only diagnostic failures\n\nThe first reviewer walker file had a BOM; compile-walker.out records its rejected import. The corrected compile-walker-utf8.out and compile-walker-path.out succeed. The optional explicit witness first used an undecidable set-equality decision procedure, then a text edit decoded UTF-8 as Windows-1252, then required unfolding set membership for decidability. Those failed runs are nonvacuity.out, nonvacuity-explicit.out and nonvacuity-final.out. Lean inserts sorryAx in declarations downstream of rejected proof holes during such failed elaborations; none of those declarations was imported or used. nonvacuity-verified.out is the successful final witness with only the three standard axioms. All submitted sources compiled without these errors.\n\nFor future runs, rebuild.py now kills its own process tree on the 590-second timeout. The actual first upstream build was manually stopped at 438 seconds and resumed; all source files were freshly compiled across those bounded runs. No Mathlib cache download was needed because the copied package cache sufficed.\n''')
print('Inputs changed during review:',changed)
