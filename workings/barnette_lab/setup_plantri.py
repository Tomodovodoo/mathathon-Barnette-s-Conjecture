"""Fetch the exact plantri mirror snapshot used in this experiment; compile locally."""
from pathlib import Path
import hashlib,subprocess,urllib.request
url='https://raw.githubusercontent.com/mishun/plantri/master/plantri.c'
p=Path(__file__).parent/'vendor'; p.mkdir(exist_ok=True)
source=urllib.request.urlopen(url,timeout=30).read()
expected='1e5be747be18fc92e040d2ca5c442d9e5f66bc01223f9ae1cf7365f287ed9738'
if hashlib.sha256(source).hexdigest()!=expected:
 raise RuntimeError('Upstream changed; review source before updating the pinned hash')
source=source.replace(b'#define CPUTIME 1',b'#define CPUTIME 0')
(p/'plantri.c').write_bytes(source)
subprocess.run(['gcc','-O3','-o',str(p/'plantri.exe'),str(p/'plantri.c')],check=True)
print(p/'plantri.exe')
