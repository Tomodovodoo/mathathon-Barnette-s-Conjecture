from pathlib import Path
p=Path('digestions/route-map/build_map.py');s=p.read_text(encoding='utf8')
old='''                rev = ", " + (f"AI-refereed ({', '.join(ref)})" if ref else f"under review ({', '.join(und)})" if und else "unreviewed")'''
new='''                rv = r.get("review")
                if rv:
                    state = rv["state"]
                    rev = ", " + {"refereed": "AI-refereed; human check pending", "under-review": "under review", "unreviewed": "unreviewed"}[state]
                    if rv.get("by"):
                        rev += " by " + ", ".join(rv["by"])
                else:
                    rev = ", " + (f"AI-refereed ({', '.join(ref)})" if ref else f"under review ({', '.join(und)})" if und else "unreviewed")
            elif r["status"] == "COMPUTED":
                rev = ", " + r.get("tier", "T4") + ", " + r.get("review", {}).get("state", "unreviewed").replace("-", " ")'''
assert old in s;s=s.replace(old,new)
s=s.replace('Smallest known counterexample:','Saved counterexample or reported minimum:')
s=s.replace('and the two-tree packing question. Exact rounding remains separate.','and proved ordinary two-tree packing. Face-side P2 and exact rounding remain open.')
p.write_text(s,encoding='utf8')
p=Path('labyrinth/seed.py');s=p.read_text(encoding='utf8')
s=s.replace("'A complete marked-involution writeup now exists in proofs/involutions/, under independent AI review.', 'Finish the independent referee and reconcile distinct-mark conventions.'","'The marked-involution writeup has two AI referees, FOLLOWS on rays and drawing-free face paths.', 'Human-check the note and formalise the path-mark dictionary.'")
s=s.replace("'Exclude the exceptional two-cover overlap; then treat more covers.'","'The AI-refereed two-cover weak bound is proved; exclude its equality overlap, then treat more covers.'")
pos=s.index("prior_path=LAB/'sota.json'")
s=s[:pos]+'''# Final rows consume the authoritative route statements and their claim-specific reviews.
by_route={r['id']:r for r in RT.ROUTES}
for entry in S['entries']:
    if entry['id']=='new-presentations':
        entry['result']='Three complete written routes. Main version 2 and both involution routes FOLLOWS; primal route ACCEPT.'
        entry['status']='Independent AI referees and completed main-v2 cold read; human check pending.'
    if entry['id']=='rarity': entry['status']='T2 independently AI-refereed all-length transfer at the specified lateral root; no human check.'
    if entry['id']=='formal':
        entry.update(result=by_route['G2.devices']['text'],status='COMPUTED T4; compiled by its author; independent check pending.',refs=['c.G2.c','c.G2.devices'])
    if entry['id']=='algorithm':
        entry['result']+=' Conditional PPADS reduction for TREE-PAIR supplied; C3 gives no automatic PLS membership or polynomial bound.'
        entry['status']='Supplied preprint time bounds; new PPADS proof T2 unreviewed, conditional on Theorem 5.3; recalled complexity citations not independently checked.'
    if entry['id']=='cancellation': entry['result']=by_route['N.11']['text']
    for key,rid in [('induction','U.ML2'),('rainbow','U.7h'),('packing','U.packing'),('covers','D.covers'),('census24','D.cover-census')]:
        if entry['id']==key:
            r=by_route[rid]; rv=review_of(r) if r['status']=='PROVED-HERE' else r.get('review',{'state':'unreviewed'})
            entry.update(result=r['text'],status=r['status']+'; '+rv['state']+'; human check pending')
for key,cls,rid in [('packing-P2','Face-side rainbow packing P2','U.packing-P2'),('pair-descent','Monotone pair descent C3','N.11'),('rainbow-R','Unsigned rainbow existence','U.rainbow'),('partial-G','Short-cycle obstruction and partial G','U.G-partial')]:
    r=by_route[rid]
    S['entries'].append(row(key,G2,cls,r['text'],r['status']+'; '+r.get('review',{'state':'unreviewed'})['state']+'; human check pending','conjecture' if r['status']=='CONJECTURE' else 'partial',[nid(r)],[]))
''' + s[pos:]
p.write_text(s,encoding='utf8')
