"""Append the exact command ledger to RELEASE-CHECK.md."""
from pathlib import Path
import json,subprocess
folder=Path(__file__).resolve().parent;p=folder/'RELEASE-CHECK.md'
text=p.read_text(encoding='utf8').split('\n<!-- COMMAND LEDGER -->')[0]
lines=['','<!-- COMMAND LEDGER -->','## Exact command ledger','','Commands execute sequentially. All unqualified working directories are relative to the indicated fresh clone. A nonzero code is a recorded failure, not an omitted check.','']
for base,clone in [(folder/'logs','E:/rc-sol-1114'),(folder/'logs/late','E:/rc-sol-late')]:
 for file in sorted(base.glob('*-commands.json')):
  lines += [f'### {clone}, {file.stem}','','| Working directory | Return | Seconds | Command |','| --- | --- | ---: | --- |']
  for row in json.loads(file.read_text(encoding='utf8')):
   args=['python' if Path(a).name.lower()=='python.exe' else a for a in row['command']]
   cmd=subprocess.list2cmdline(args).replace('|',r'\|')
   lines.append(f"| {row['cwd']} | {row['code']} | {row['seconds']} | `{cmd}` |")
  lines.append('')
lines += ['### Evidence scripts','','From the shared repository root, where `R=research/2026-11-14_sol_release-check`:','','```powershell',"$R = 'research/2026-11-14_sol_release-check'",'python -B $R/run.py E:/rc-sol-1114 $R/logs baseline','python -B $R/scan.py E:/rc-sol-1114 $R/logs','python -B $R/paths.py E:/rc-sol-1114 $R/logs','python -B $R/route_compare.py E:/rc-sol-1114 $R/logs','python -B $R/pdf_privacy.py E:/rc-sol-1114 $R/logs','python -B $R/scan.py E:/rc-sol-late $R/logs/late','python -B $R/paths.py E:/rc-sol-late $R/logs/late','python -B $R/route_compare.py E:/rc-sol-late $R/logs/late','python -B $R/summarize.py','python -B $R/append_commands.py','```','','Run baseline before any product rebuild. The runner phases used are baseline, code, figures, documents, compare, blueprint, pristine, supplement, late-docs and late-atlas. Each phase is invoked as `python -B $R/run.py CLONE LOGDIR PHASE`; its expanded child commands are the ledger above. `pristine` restores exact tracked inputs only inside the disposable clone. `figures` and `late-atlas` delete disposable cloned atlas figure PDFs to force real compilation rather than reuse the committed PDFs.','']
p.write_text(text+'\n'.join(lines),encoding='utf8')
