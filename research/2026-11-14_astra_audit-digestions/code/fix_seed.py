from pathlib import Path
p=Path('labyrinth/seed.py');s=p.read_text(encoding='utf8').replace('known = {json.loads(line)["id"] for line in old if line.strip()}','known = {(json.loads(line)["ts"], json.loads(line)["type"]) for line in old if line.strip()}').replace('if e["id"] not in known:', 'if (e["ts"], e["type"]) not in known:')
s=s.replace("'Lattice minimum or maximum' has no joint failure in 180 random instances.","The conjecture campaign reports joint failures of the true minimum and maximum at 18 vertices; independent replay pending.")
s=s.replace('"conjecture", "conjecture", ["k.D.7",','"reported refuted; finite computation under review", "partial", ["k.D.7",')
s=s.replace('short proof proved here (gt, under review)','short proof checked in structure referee INTEGRATION.md; final REPORT still provisional').replace('proved here (lim, under review); computed for q <= 6','proved here, checked in structure referee INTEGRATION.md Section 6; computed for q <= 6')
s=s.replace('First test: exhaustive census to 24 vertices for k.D.7;', 'First test: independently replay the reported 18-vertex joint failures of k.D.7;')
p.write_text(s,encoding='utf8')
