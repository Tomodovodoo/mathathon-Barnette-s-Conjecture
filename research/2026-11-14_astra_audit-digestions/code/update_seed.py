from pathlib import Path
p=Path('labyrinth/seed.py');s=p.read_text(encoding='utf8')
s=s.replace('return f"{PREFIX[r[\'status\']]}.{r[\'id\']}"','return "k.D.7" if r["id"] == "D.7" else f"{PREFIX[r[\'status\']]}.{r[\'id\']}"')
s=s.replace('kind="theorem", tier="T1",\n                      status="established (LIT: waypoint of the 2026 proofs; the papers are unrefereed preprints)"','kind="theorem", tier="T2", review={"state":"unreviewed"},\n                      status="source waypoint; unrefereed preprint, not a peer-review claim"')
s=s.replace('n.update(kind="theorem", tier="T1",','n.update(kind="theorem", tier="T2" if pre else "T1",')
s=s.replace('links.append({"to": f"wp.{s[\'to\']}", "rel": "supports"})\n    elif st == "PROVED-HERE":','if pre: n["review"] = {"state": "unreviewed", "verdict": "Supplied preprint or formal source; no journal review claimed."}\n        links.append({"to": f"wp.{s[\'to\']}", "rel": "supports"})\n    elif st == "PROVED-HERE":')
# Preserve all historical event bytes; append only genuinely new backfill entries.
a=s.index('old = []\npth = LAB / "events.jsonl"');b=s.index('# ---------------------------------------------------------------- state of the art',a)
s=s[:a]+'''pth = LAB / "events.jsonl"
old = pth.read_text(encoding="utf-8").splitlines() if pth.exists() else []
known = {json.loads(line)["id"] for line in old if line.strip()}
with pth.open("a", encoding="utf-8") as f:
    for e in E:
        if e["id"] not in known: f.write(json.dumps(e) + "\\n")

'''+s[b:]
p.write_text(s,encoding='utf8')
