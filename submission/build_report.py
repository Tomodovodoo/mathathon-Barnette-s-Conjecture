"""Compile the four-page project report. report.tex is the complete source."""
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent

if __name__ == '__main__':
    for _ in range(3):
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'report.tex'],
            cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        if result.returncode:
            print(result.stdout.decode(errors='replace')[-6000:])
            raise SystemExit(result.returncode)
    print('Built', HERE / 'report.pdf')
