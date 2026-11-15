"""Stage 0: build the tools.

  python src/build.py            compile fastbarnette.dll (needs gcc)
  python src/build.py plantri    also download plantri 5.8 and compile it

Everything goes to build/, which is not under version control.
"""
import hashlib
import subprocess
import sys
import tarfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'src'
BIN = ROOT / 'build' / 'bin'

# plantri 5.8 by G. Brinkmann and B. D. McKay, https://users.cecs.anu.edu.au/~bdm/plantri/
PLANTRI_URLS = ['https://users.cecs.anu.edu.au/~bdm/plantri/plantri58.tar.gz',
                'https://mirrors.mit.edu/sage/spkg/upstream/plantri/plantri58.tar.gz']
PLANTRI_SHA256 = 'e78a944116fec9f2c9f5e484206276cc2b0043bae803e9815f4b2683614629b8'


def run(cmd):
    print(' '.join(map(str, cmd)))
    subprocess.run(cmd, check=True)


def build_dll():
    BIN.mkdir(parents=True, exist_ok=True)
    run(['gcc', '-O2', '-Wall', '-Wextra', '-shared', '-static', '-o', BIN / 'fastbarnette.dll',
         SRC / 'fastbarnette.c'])


def build_plantri():
    BIN.mkdir(parents=True, exist_ok=True)
    tar = ROOT / 'build' / 'plantri58.tar.gz'
    if not tar.exists():
        for url in PLANTRI_URLS:
            try:
                print('downloading', url)
                urllib.request.urlretrieve(url, tar)
                break
            except OSError as error:
                print('  failed:', error)
    digest = hashlib.sha256(tar.read_bytes()).hexdigest()
    if digest != PLANTRI_SHA256:
        raise SystemExit(f'unexpected checksum {digest} for {tar}')
    dest = ROOT / 'build' / 'plantri_src'
    dest.mkdir(exist_ok=True)
    with tarfile.open(tar) as archive:
        archive.extractall(dest, filter='data')
    # MinGW has no <sys/times.h>; src/compat supplies a replacement.
    run(['gcc', '-O3', '-w', '-I', SRC / 'compat', '-o', BIN / 'plantri.exe',
         dest / 'plantri58' / 'plantri.c'])


if __name__ == '__main__':
    build_dll()
    if 'plantri' in sys.argv[1:]:
        build_plantri()
