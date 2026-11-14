"""Extract the formal statement (header up to ':=' or 'where') of Lean declarations.

Usage: python -I scripts/lean_sigs.py <lean-dir> <out.json> [names...]
Reads every *.lean file under <lean-dir>, finds column-0 declarations
(theorem/lemma/def/structure/abbrev/inductive/class), qualifies them by the
namespace stack, and writes {fullname: {file, line, kind, header}}.
"""
import json, re, sys, pathlib

DECL = re.compile(r'^(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable|nonrec)\s+)*'
                  r'(theorem|lemma|def|structure|abbrev|inductive|class|instance)\s+([^\s:({\[]+)')

def scan(lean_dir):
    out = {}
    for f in sorted(pathlib.Path(lean_dir).glob('*.lean')):
        lines = f.read_text(encoding='utf-8').splitlines()
        ns = []
        i = 0
        while i < len(lines):
            L = lines[i]
            m = re.match(r'^namespace\s+(\S+)', L)
            if m:
                ns.append(m.group(1)); i += 1; continue
            m = re.match(r'^end\s+(\S+)', L)
            if m and ns and ns[-1] == m.group(1):
                ns.pop(); i += 1; continue
            m = DECL.match(L)
            if m:
                kind, name = m.groups()
                full = '.'.join(ns + [name])
                hdr = []
                j = i
                while j < len(lines):
                    s = lines[j]
                    if j > i and (DECL.match(s) or re.match(r'^(namespace|end|section|variable|open|omit)', s)):
                        j -= 1; break
                    cut = None
                    for tok in (':= by', ':=', ' where'):
                        k = s.find(tok)
                        if k >= 0 and (cut is None or k < cut):
                            cut = k
                    if cut is not None:
                        hdr.append(s[:cut]); break
                    hdr.append(s)
                    j += 1
                    if j - i > 40:
                        break
                header = ' '.join(x.strip() for x in hdr)
                header = re.sub(r'\s+', ' ', header).strip()
                out[full] = dict(file=f.name, line=i + 1, kind=kind, header=header)
                i = j + 1 if j > i else i + 1
                continue
            i += 1
    return out

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    lean_dir, outp = sys.argv[1], sys.argv[2]
    decls = scan(lean_dir)
    json.dump(decls, open(outp, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(len(decls), 'declarations')
    for q in sys.argv[3:]:
        hits = [k for k in decls if k == q or k.endswith('.' + q)]
        for k in hits:
            d = decls[k]
            print(f"{k} [{d['file']}:{d['line']}]\n   {d['header'][:400]}")
        if not hits:
            print('MISSING', q)
