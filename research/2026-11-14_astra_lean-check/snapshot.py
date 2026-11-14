from pathlib import Path
import hashlib,json,re,subprocess
R=Path.cwd(); D=R/'research/2026-11-14_astra_lean-check'
paths=list((R/'proofs/lean').rglob('*'))+[R/'paper/main/barnette.tex',R/'paper/main/barnette.aux',R/'proofs/blueprint/blueprint.json']
manifest={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}
(D/'inputs-sha256.json').write_text(json.dumps(manifest,indent=2)+'\n')
(D/'paper-at-review.tex.txt').write_text((R/'paper/main/barnette.tex').read_text(encoding='utf-8'),encoding='utf-8')
(D/'paper-labels.txt').write_text('\n'.join(l for l in (R/'paper/main/barnette.aux').read_text(encoding='utf-8').splitlines() if l.startswith('\\newlabel{lem:') or l.startswith('\\newlabel{prop:') or l.startswith('\\newlabel{thm:') or l.startswith('\\newlabel{rem:')),encoding='utf-8')
(D/'REVIEW-STATE.md').write_text('COMPUTED: fresh upstream clone started, with only dependency caches to be copied. Statements read in Devices/LocalSign, RealSign, Concrete, Outdegree, TreeMatching, FiniteDifference. Full build, axioms and independent reachability still pending.\n\nAudit boundary: unchanged upstream MainStatement at 4eaee875, under the Lean kernel and standard Mathlib axioms. Paper model bridges are separate obligations. Snapshot hashes and paper source preserve the working-tree version being reviewed.\n',encoding='utf-8')
print(len(manifest),'input hashes recorded')
