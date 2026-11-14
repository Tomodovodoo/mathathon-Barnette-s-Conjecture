from pathlib import Path
p=Path('digestions/route-map/ROUTE-MAP.tail.md')
p.write_text('''## Shared steps and live alternatives

The supplied proofs share the disk identity, a sign-reversing cancellation with the second state fixed, and a nonzero lowest coefficient after regrouping by covers. The partner certifies root connectivity. These are statements about the supplied routes, not impossibility theorems for other proofs.

The failed shortcuts are kept as routes with lessons and certificates. C2 fails first at V=18. R2, extreme or irreducible, fails at V=33. Natural two-matroid and integral-LP relaxations fail; exact reformulations alone supply no existence proof. The signed sum cannot be recovered from the ordinary rank polynomial of the factor lattice.

The contraction route has two missing lemmas, ML1 and ML2. C3 allows plateaus among pairs. Rainbow exchange X allows plateaus among white trees, while the surplus walk alone can cycle. Two-tree packing is tracked separately from exact degree rounding. These are the current unsigned doors; their finite evidence is not a proof.

## Limits of this map

- The map integrates attributed reports and named AI referee verdicts. New results in a referee's own report remain unreviewed unless another review is named. Nothing is human-checked.
- The independently checked full invariant-value frontier remains at dual order 16. The C1 census reaches 22 for all facial roots and 24 only for separator-free inputs. The latter is T4 under review.
- The upstream Lean proof was built locally. Machine checking applies to its formal statement, not every new research claim or written route.
- A counterexample order is a witness size, not a minimum, unless an exhaustive minimum-order check is explicitly named. V=33 R2 is not claimed minimal.
- Sources still running at the final scan are listed in the map-update report. The generated figures and catalogue come from routes.py; the dashboard also uses seed.py and make_frontier.py.
''',encoding='utf8')
p=Path('digestions/route-map/ROUTE-MAP.head.md');s=p.read_text(encoding='utf8').replace('| published. One strand','| supplied source result; 2026 preprints are unrefereed. One strand');p.write_text(s,encoding='utf8')
p=Path('digestions/route-map/build_map.py');s=p.read_text(encoding='utf8').replace('va="center", zorder=6)\n    if detail:\n        n = len(BY_STEP["TG"])','va="center", zorder=6, bbox=dict(facecolor="white", edgecolor="none", pad=2))\n    if detail:\n        n = len(BY_STEP["TG"])');p.write_text(s,encoding='utf8')
p=Path('labyrinth/seed.py');s=p.read_text(encoding='utf8').replace('import json\n','import json\nimport re\n',1).replace('out = out.replace(f"{tag}/", folder + "/")','out = re.sub(r"(?<![\\w/])" + re.escape(tag) + "/", folder + "/", out)')
s=s.replace("if entry['id']=='canonical':","if entry['id']=='pair': entry['status']='PROVED-HERE, independently AI-refereed in structure INTEGRATION.md; human check pending.'\n    if entry['id']=='structural': entry.update(result='No unsigned existence proof yet. Contraction ML1 and ML2, C3, rainbow X and packing remain live at this snapshot.',status='Conjectures with stated tests; named local lemmas AI-refereed, new extensions unreviewed.')\n    if entry['id']=='rarity': entry.update(result='Exponential rarity also without separating triangles: width-four nanotubes have two tree matchings among Fib_(2L+3) states.',status='T2 author proof and T4 transfer arithmetic unreviewed; older prism-sum proof AI-refereed.')\n    if entry['id']=='which-hc': entry['status']='Earlier recovery image and injectivity independently AI-refereed; revised compatible-state converse is separate, unreviewed.'\n    if entry['id']=='canonical':")
p.write_text(s,encoding='utf8')
# Named structure claims only, not the entire folder.
p=Path('digestions/route-map/routes.py');s=p.read_text(encoding='utf8');s+='''
for rid in ('A.GT','G.1','G.5','U.5','F.3','D.5','U.3','U.6','U.4'):
    if any(r['id']==rid and r['status']=='PROVED-HERE' for r in R):
        checked(rid,'research/2026-11-14_sol_referee-structure','Named surrounding structural claim checked in INTEGRATION.md; use its corrected scope, not the refuted broad degree-four converse or matroid isomorphism.')
for rid in ('B.6','F.6','K.4','U.7'):
    checked(rid,'reft','Original topology claim checked with corrections; new RAINBOW.md theorems have separate unreviewed entries.')
''';p.write_text(s,encoding='utf8')
