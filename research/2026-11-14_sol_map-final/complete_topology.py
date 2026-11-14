from pathlib import Path
p=Path('digestions/route-map/routes.py');s=p.read_text(encoding='utf8')+'''
add('U.rainbow-local','U','unique exchange and disk-surplus identity','PROVED-HERE','reft','reft/RAINBOW.md Lemmas X1 and X2',
    'Every point of a rainbow tree has exactly one exchange, so the move graph is n-regular. The fundamental-cycle surplus is W-B-1 plus the old-face interior indicator. These exact local statements do not prove Step X. T2 unreviewed.','topology')
add('U.rainbow-mean','U','uniform rainbow mean load one','REFUTED','reft','reft/RAINBOW.md; reft/data/average_6_14.json',
    'The uniform rainbow tree has expected load one at every bounded black face.','probability',cex='V=12 first reported failure; holds in 828 of 880 instances through V=14, exactly the singleton-factor instances.',lesson='Uniform one-sided trees do not automatically meet the other degree constraint in expectation.')
add('U.evict-transitive','U','resident involutions act transitively','REFUTED','reft','reft/RAINBOW.md; reft/data/selection_6_13.json',
    'The n resident-eviction involutions connect every good state.','bijective',cex='Disconnected in 24 of 672 instances at V=13 or 14; exact least order not certified in the report.',lesson='Fixed-point-free pairings prove evenness, not connectivity of good states.')
''';p.write_text(s,encoding='utf8')
# Synchronize just the generated graveyard, preserving the edited ranking.
import sys,re
sys.path.insert(0,'digestions/route-map');import routes as rt
p=Path('digestions/steps/09-what-is-still-open.md');s=p.read_text(encoding='utf8');a=s.index('| Route and rejected shortcut');b=s.index('## What survives',a)
t='| Route and rejected shortcut | Counterexample and size | Data or proof | Lesson |\n|---|---|---|---|\n'
for r in rt.R:
 if r['status']!='REFUTED':continue
 w=r['where']
 for tag,folder in rt.FOLDERS.items():w=re.sub(r'(?<![\w/])'+re.escape(tag)+'/',folder+'/',w)
 vals=[r['id']+' '+r['label'],r.get('cex','No certified numerical minimum; see proof.'),w,r['lesson']]
 t+='| '+' | '.join(str(x).replace('|',' / ').replace('\n',' ') for x in vals)+' |\n'
s=s[:a]+t+'\n'+s[b:];s=s.replace('allowing plateaus. [RAINBOW.md]','allowing plateaus. The excess is twice the number of bounded black faces with load two, where load counts the selected point spokes at that face. [RAINBOW.md]');p.write_text(s,encoding='utf8')
