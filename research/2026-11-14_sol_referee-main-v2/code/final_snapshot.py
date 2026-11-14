"""Separate the referee's edits from a concurrent finishing pass; freeze final review."""
from verify_numbers import ROOT,OUT
import regression
import subprocess,json,difflib
final=(ROOT/'paper/main/barnette.tex').read_text(encoding='utf-8')
(OUT/'v2-final.tex').write_text(final,encoding='utf-8')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT).decode('utf-8')
for name,args in {
 'own-corrections.diff':['show','d3b3651','--format=','--','paper/main/barnette.tex'],
 'last-correction.diff':['show','e97b061','--format=','--','paper/main/barnette.tex'],
 'concurrent-finishing.diff':['diff','d3b3651','f04e0d1','--','paper/main/barnette.tex'],
}.items():(OUT/name).write_text(git(*args),encoding='utf-8')
(OUT/'final-source.diff').write_text(''.join(difflib.unified_diff(regression.a.splitlines(True),final.splitlines(True),fromfile='v1',tofile='v2-final')),encoding='utf-8')
old={x['key']:x for x in regression.blocks(regression.a)}
chunks=[];envs=regression.blocks(final)
for x in envs:
    y=old.get(x['key'],{}).get('text','')
    if y!=x['text']:
        chunks.append(f"\n### {x['key']}, final line {x['line']}\n")
        chunks.extend(difflib.unified_diff(y.splitlines(True),x['text'].splitlines(True)))
(OUT/'final-environments.diff').write_text(''.join(chunks),encoding='utf-8')
(OUT/'final-environments.json').write_text(json.dumps(envs,indent=2),encoding='utf-8')
print('Final frozen; original input retained; referee edits isolated from finishing pass.')
