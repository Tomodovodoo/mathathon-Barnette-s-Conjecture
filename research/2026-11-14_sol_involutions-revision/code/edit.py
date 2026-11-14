from pathlib import Path
import re
root=Path('.')
out=root/'research/2026-11-14_sol_involutions-revision'
edits=(root/'research/2026-11-14_opus_referee-involutions/EDITS.md').read_text(encoding='utf-8')
p=root/'proofs/involutions/involutions.tex'; s=p.read_text()
for num,body in re.findall(r'## E(\d+)\.(.*?)(?=\n## E|\Z)',edits,re.S):
    if int(num)>13:continue
    blocks=re.findall(r'```tex\n(.*?)\n```',body,re.S)
    if len(blocks)==2:
        old,new=blocks
        assert old in s,num
        s=s.replace(old,new)
    elif num=='2':s=s.replace('all 56 unrooted','all 55 unrooted')
p.write_text(s)
for name in ['INVOLUTIONS.md','STATUS.md']:
    p=root/'proofs/involutions'/name;s=p.read_text().replace('56 classes','55 classes')
    s=s.replace('Earlier counts of 213 refer to a different geometry or input and are not silently reused.', 'The earlier Li replay has 213 objects on the same input with roots 4 and 5 interchanged. The marked set depends on the drawing; the signed sum and the nine second-fixed objects do not.')
    s=s.replace('The original example.json is absent. The current running.json and a different exact layout are used and copied here. Earlier 213-object tables have not been identified with this 279-object set.', 'The original example.json is absent. The current running.json is copied here. The 213-object Li replay interchanges the anchor points of roots 4 and 5. Both counts are correct; the signed sum is -9 in both drawings.')
    p.write_text(s)
