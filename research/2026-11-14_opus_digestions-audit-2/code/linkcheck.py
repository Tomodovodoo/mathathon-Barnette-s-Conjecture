"""Check every Markdown link and image in digestions/steps/*.md, and every
backticked repository path (starting with research/, paper/, papers/, proofs/,
digestions/ or workings/).

    python research/2026-11-14_opus_digestions-audit-2/code/linkcheck.py

Writes ../outputs/linkcheck.txt. Exit status 1 if a link in 01-08 or GLOSSARY fails.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STEPS = ROOT / 'digestions' / 'steps'
LINK = re.compile(r'!?\[[^\]]*\]\(([^)\s]+)\)')
TICK = re.compile(r'`((?:research|paper|papers|proofs|digestions|workings)/[^`\s]+)`')
lines, bad_owned = [], 0
for md in sorted(STEPS.glob('*.md')):
    text = md.read_text(encoding='utf-8')
    owned = md.name not in ('00-overview.md', '09-what-is-still-open.md')
    n_ok = 0
    for target in LINK.findall(text):
        if target.startswith(('http://', 'https://', '#', 'mailto:')):
            continue
        path = (md.parent / target.split('#')[0]).resolve()
        if path.exists():
            n_ok += 1
        else:
            lines.append(f'MISSING link  {md.name}: {target}')
            bad_owned += owned
    for target in TICK.findall(text):
        target = target.rstrip('.,;:)')
        path = ROOT / target.split('#')[0]
        if not path.exists():
            lines.append(f'missing path  {md.name}: `{target}`')
            bad_owned += owned
        else:
            n_ok += 1
    lines.append(f'{md.name}: {n_ok} links and paths resolve')
out = '\n'.join(lines)
print(out)
(Path(__file__).resolve().parents[1] / 'outputs' / 'linkcheck.txt').write_text(out + '\n', encoding='utf-8')
sys.exit(1 if bad_owned else 0)
