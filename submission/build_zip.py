"""Package the required PDFs and report source with the supporting project files."""
from io import BytesIO
from pathlib import Path
import re
import subprocess
import tarfile
import zipfile

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / 'convex-curiosity-submission.zip'
SUPPORT = {
    'Every Vertex Once', 'README.md', 'barnette-proof-walkthrough.html',
    'digestions', 'index.html', 'paper', 'papers', 'proofs',
    'requirements.txt', 'research', 'slides',
    'workings',
}


def main():
    report = (ROOT / 'submission/report.tex').read_text(encoding='utf-8')
    match = re.search(r'Code snapshot: \\texttt\{([0-9a-f]{40})\}', report)
    if not match:
        raise SystemExit('The report title block must name the code snapshot.')
    snapshot = match.group(1)
    archive = subprocess.check_output(
        ['git', 'archive', '--format=tar', snapshot], cwd=ROOT,
    )
    entries = {}
    with tarfile.open(fileobj=BytesIO(archive), mode='r:') as source:
        for member in source.getmembers():
            if not member.isfile():
                continue
            name = member.name
            if name.split('/')[0] not in SUPPORT or name.endswith('/.gitignore'):
                continue
            entries['supplementary/' + name] = source.extractfile(member).read()

    for name in ('report.tex', 'report.pdf', 'README.md', 'build_report.py', 'build_zip.py'):
        data = (ROOT / 'submission' / name).read_bytes()
        entries['supplementary/submission/' + name] = data
        if name in ('report.tex', 'report.pdf'):
            entries[name] = data
    entries['slides.pdf'] = entries['supplementary/slides/slides.pdf']
    entries['README.txt'] = (
        'Convex Curiosity - Mathathon, Combinatorics\n\n'
        'report.tex and report.pdf: the official project report.\n'
        'slides.pdf: the presentation PDF.\n'
        'supplementary/: website, proof walkthrough, implementation, tests, '
        'experiment data, source papers and supporting notes.\n\n'
        'The report title block identifies the fixed repository snapshot for '
        'the supplementary files. No Lean project is submitted.\n\n'
        'To run the website locally, serve supplementary/ with a static HTTP '
        'server and open its index.html in a browser.\n'
        'For code and experiment instructions, see supplementary/workings/README.md '
        'and supplementary/research/experiments/README.md.\n'
    ).encode('utf-8')
    temporary = OUTPUT.with_suffix('.zip.tmp')
    with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as target:
        for name, data in sorted(entries.items()):
            target.writestr(name, data)
    with zipfile.ZipFile(temporary) as target:
        if target.testzip() is not None:
            raise SystemExit('ZIP integrity check failed.')
        for required in ('report.tex', 'report.pdf', 'slides.pdf'):
            if not target.read(required):
                raise SystemExit('Required file is empty: ' + required)
    temporary.replace(OUTPUT)
    print(f'Built {OUTPUT} ({len(entries)} files, {OUTPUT.stat().st_size:,} bytes)')


if __name__ == '__main__':
    main()
