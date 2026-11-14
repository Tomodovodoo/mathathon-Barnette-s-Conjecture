from pathlib import Path
import json,re,subprocess
R=Path.cwd();A=R/'research/2026-11-14_astra_audit-digestions';ledger=[]
def change(rel,old,new):
 p=R/rel;s=p.read_text(encoding='utf8');assert old in s,(rel,old);p.write_text(s.replace(old,new),encoding='utf8');ledger.append({'file':rel,'old':old,'new':new})
bridges=[('00-overview.md','## Dependency diagram','The count in steps 05 and 06 is an existence proof. A nonzero signed sum forces at least one tree matching, but does not identify one efficiently. Step 07 is an explicit construction once that matching is supplied.'),('01-degree-two-and-connectivity.md','## Precise statements','A 2-factor can have several cycles. Whenever this guide says connected, it means all its vertices lie in a single component; that is the extra property the proof must force.'),('02-dual-and-two-trees.md','## Precise statements and proofs','Keep the two vertex sets separate: vertices of G become faces of T. A cycle through vertices of T would solve a different problem.'),('03-states-and-pairs.md','## Why a second state','The edge of Q_s is opposite s(t); the edge of D is incident with s(t). They are different edges of the same triangle. Reversing Q_s changes r only, while reversing D changes both states.'),('04-disk-identity.md','## Worked examples','The bounded disk always means the side away from the outer face. Reversing a traversal changes its delta-sum, but does not change B, W, I or the number of black-inside boundary edges.'),('05-cancellation.md','## The two families of cubes','Here a cube is a finite set of independent binary choices, not a subgraph of the triangulation. Its dimension counts cycles that can be reversed independently.'),('06-nonvanishing.md','## Full proof of the heights version','The selected white faces w_i need not be distinct: nested cycles can use the same face. The indices i remain distinct, so the expansion counts bijections of indices even when face names repeat.'),('07-recovery.md','## The six links','There are two different roots here. The three vertices of t0 root the components of Q_s; the single white face y0 roots the white-face tree.'),('08-gluing-and-hypotheses.md','## Statement and proof','The induction solves the outer piece first. Its boundary split then determines the prescription for the inner piece. Choosing the two solutions independently would not justify gluing.'),('09-what-is-still-open.md','## 1. Algorithms and complexity','A finite check supports only its stated range. A proof supplied by an agent, a second-model referee verdict and a machine-checked theorem are different kinds of evidence; the status beside each claim records which is available.')]
for f,anchor,t in bridges:change('digestions/steps/'+f,anchor,t+'\n\n'+anchor)
change('digestions/steps/06-nonvanishing.md','## Why cancellation across covers cannot be avoided','![Two covers sharing the same cancelling second state](img/two-covers.png)\n\n## Why cancellation across covers cannot be avoided')
change('digestions/steps/06-nonvanishing.md','## Why extremal choices fail','![The two orientations of the bad 16-vertex cover](img/bad-cover-16.png)\n\n## Why extremal choices fail')
change('digestions/route-map/HOW-IT-WORKS.md','## 1. What must be shown','The diagram records routes supplied by these sources. Its words "forced" and "free" describe that inventory, not a theorem that other proofs are impossible. A route ID such as N.H is only a lookup key; the explanation below can be read without following those links.\n\n## 1. What must be shown')
# Remove typography tells while preserving mathematical punctuation and code.
for p in list((R/'digestions/steps').glob('*.md'))+[R/'digestions/route-map/HOW-IT-WORKS.md']:
 s=p.read_text(encoding='utf8');t=s.replace('\u2014','. ').replace('\u201c','"').replace('\u201d','"').replace('\u2019',"'")
 if t!=s:p.write_text(t,encoding='utf8');ledger.append({'file':str(p.relative_to(R)),'change':'Replaced em dashes and curly quotation marks with plain punctuation.'})
change('digestions/route-map/build_map.py','FORCED: one published argument','SHARED: one source argument')
change('digestions/route-map/build_map.py','FORCED: {k} wordings of one argument','SHARED: {k} source formulations')
change('digestions/route-map/build_map.py','FREE: {k} published arguments','CHOICE: {k} source arguments')
change('digestions/route-map/build_map.py','published (2026 papers: unrefereed preprints)','source proof (2026 preprints: unrefereed)')
# Reserve T1 for published reviewed or standard material.
p=R/'labyrinth/README.md';s=p.read_text(encoding='utf8');s=re.sub(r'- \*\*T1\*\*.*\n','- **T1** is reserved for peer-reviewed literature or standard results. Supplied 2026 preprint claims and source waypoints are conservatively T2 with review status stated. LIT records provenance and does not by itself assign a tier.\n',s);s=s.replace('waypoints `wp.*` (theorem, T1)','waypoints `wp.*` (source claims, T2)').replace('published routes `th.*` (theorem, T1)','source routes `th.*` (theorem, T1 or T2)');p.write_text(s,encoding='utf8')
# Persist per-row history and integrate the new manuscript routes in the canonical generator.
p=R/'labyrinth/seed.py';s=p.read_text(encoding='utf8');s=s.replace('status=f"established: proved here ({label})"','status=f"proof supplied ({label})"')
marker='(LAB / "sota.json").write_text'
i=s.index(marker)
insert='''# Keep prior state-of-the-art results when a row changes.
prior_path = LAB / "sota.json"
prior = json.loads(prior_path.read_text(encoding="utf-8")) if prior_path.exists() else {"entries": []}
prior_by_id = {r["id"]: r for r in prior["entries"]}
for r in S["entries"]:
    old_row = prior_by_id.get(r["id"])
    if old_row:
        r["previous"] = old_row.get("previous", [])
        if old_row["result"] != r["result"]:
            r["previous"].append({"date": DAY, "result": old_row["result"], "status": old_row["status"]})
S["entries"].append(dict(id="new-presentations", group=G1, cls="Additional manuscript routes", result="Primal proof, draft A heights proof, draft B polynomial proof; exact prism families as a separate structural route.", status="Proofs supplied; draft A referee reports sentence repairs; remaining independent reviews pending.", kind="partial", refs=["p.G2.primal", "p.G2.drafta", "p.G2.draftb", "p.D.families"], lit=[], previous=[]))
'''
s=s[:i]+insert+s[i:];p.write_text(s,encoding='utf8')
# Historical event lines are left untouched.
event={'ts':'2026-11-14T14:00:00Z','type':'reviewed','summary':'Digestion audit: corrected polynomial reflection, replayed Li multi-mark involutions, integrated provisional 18-vertex lattice refutation and new manuscript routes; preprints no longer imply T1. Timestamp is audit-day bookkeeping, not a claimed discovery time.','nodes':['k.D.7','c.N.li-check','p.G2.primal','p.G2.drafta','p.G2.draftb'],'evidence':['research/2026-11-14_astra_audit-digestions/REPORT.md']}
with (R/'labyrinth/events.jsonl').open('a',encoding='utf8') as f:f.write(json.dumps(event)+'\n')
(A/'outputs/reader-edits.json').write_text(json.dumps(ledger,indent=2),encoding='utf8')
