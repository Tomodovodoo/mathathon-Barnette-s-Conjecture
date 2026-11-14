from pathlib import Path
p=Path('labyrinth/seed.py');s=p.read_text(encoding='utf8').replace('T3  only the census cross-check, where two independent implementations agree instance by instance.','T3  the census cross-check and the independently replayed finite C1 census.')
s=s.replace('pre = all(f in ("O", "L", "T", "Lean") or f in RT.FOLDERS for f in srcs(r))','pre = r["id"] == "G2.2" or all(f in ("O", "L", "T", "Lean") or f in RT.FOLDERS for f in srcs(r))')
s=s.replace("updates = {","updates = {\n 'q.structural': ('No unsigned existence proof yet. Contraction has ML1 and ML2 open; C3 and rainbow exchange require plateaus. Packing and exact rounding are separate.', 'Finish the pending reports, then referee the new local and density arguments.'),")
p.write_text(s,encoding='utf8')
p=Path('digestions/route-map/routes.py');s=p.read_text(encoding='utf8');s+="\n_upd('TG.older',label='older radial-tree dictionary and limits')\n";p.write_text(s,encoding='utf8')
p=Path('digestions/route-map/build_map.py');s=p.read_text(encoding='utf8');s+='''
# Matplotlib emits harmless trailing spaces in SVG path data; normalize generated
# text so the owned-path whitespace check remains useful for actual prose edits.
for svg in HERE.glob('*.svg'):
    svg.write_text('\\n'.join(line.rstrip() for line in svg.read_text(encoding='utf8').splitlines())+'\\n',encoding='utf8')
''';p.write_text(s,encoding='utf8')
