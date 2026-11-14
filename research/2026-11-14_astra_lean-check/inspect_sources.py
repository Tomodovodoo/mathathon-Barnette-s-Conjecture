from pathlib import Path
import re,difflib,json,hashlib
R=Path.cwd(); D=R/'research/2026-11-14_astra_lean-check'; P=Path('E:/lb2')
# All hits retained, including comments; classify in report.
pattern=re.compile(r'\b(sorry|admit|axiom|native_decide|unsafe|opaque|implemented_by)\b|\bset_option\b')
files=list((R/'proofs/lean').rglob('*.lean'))+list((P/'PaperRoute').glob('*.lean'))
hits=[]
for p in files:
 for i,line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1):
  if pattern.search(line): hits.append(f'{p}:{i}: {line}')
(D/'source-scan.txt').write_text('Pattern: '+pattern.pattern+'\nFiles scanned: '+str(len(files))+'\n'+'\n'.join(hits)+'\n',encoding='utf-8')
diffs=[]; summary=[]
for p in sorted((P/'PaperRoute').glob('*.lean')):
 old=P/'lean/OAI/Combinatorics/Hamiltonian'/p.name
 a=old.read_text(encoding='utf-8').splitlines(True); b=p.read_text(encoding='utf-8').splitlines(True)
 diffs.extend(difflib.unified_diff(a,b,fromfile='upstream/'+p.name,tofile='PaperRoute/'+p.name))
 summary.append((p.name,len([x for x in difflib.ndiff(a,b) if x.startswith('- ')]),len([x for x in difflib.ndiff(a,b) if x.startswith('+ ')])))
(D/'generated.diff').write_text(''.join(diffs),encoding='utf-8')
(D/'generated-diff-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print('scanned',len(files),'files;',len(hits),'hits;',len(summary),'generated files diffed')
