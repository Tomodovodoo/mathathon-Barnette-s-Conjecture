"""Turn proofs/sign-free/sign-free.tex into SIGN-FREE.md (same text, GitHub-flavoured Markdown with TeX math).

Usage: python tex2md.py ../../../proofs/sign-free/sign-free.tex ../../../proofs/sign-free/SIGN-FREE.md
Numbers of statements, equations and figures are read from sign-free.aux, so build the PDF first.
"""
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
tex = open(src, encoding='utf-8').read()
aux = open(src[:-4] + '.aux', encoding='utf-8').read()
labels = dict(re.findall(r'\\newlabel\{([^}]*)\}\{\{([^}]*)\}', aux))
cites = {}
for i, k in enumerate(re.findall(r'\\bibitem\{([^}]*)\}', tex), 1):
    cites[k] = str(i)

title = re.search(r'\\title\[[^\]]*\]\{([^}]*)\}', tex).group(1)
abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1).strip()
body = tex[tex.index('\\raggedbottom') + len('\\raggedbottom'):tex.index('\\end{document}')]
macros = {r'\T': 'T', r'\cB': r'\mathcal{B}', r'\exc': r'\operatorname{exc}', r'\alt': r'\operatorname{alt}',
          r'\parent': r'\operatorname{par}', r'\step': r'\operatorname{step}', r'\mirror': r'\operatorname{mir}'}


def conv(t):
    for k, v in macros.items():
        t = re.sub(re.escape(k) + r'(?![A-Za-z])', lambda m: v, t)
    t = re.sub(r'\\begin\{figure\}\[H\].*?\\caption\{(.*?)\}\s*\\label\{([^}]*)\}\s*\\end\{figure\}',
               lambda m: '\n> **Figure %s** (drawn in `sign-free.pdf`; source `figures/`). %s\n' % (labels[m.group(2)], m.group(1)), t, flags=re.S)
    t = re.sub(r'\\begin\{thebibliography\}\{9\}', '## References\n', t)
    t = t.replace('\\end{thebibliography}', '')
    t = re.sub(r'\\bibitem\{([^}]*)\}', lambda m: '\n[%s] ' % cites[m.group(1)], t)
    t = re.sub(r'\\section\{([^}]*)\}\\label\{([^}]*)\}', lambda m: '\n## %s. %s\n' % (labels[m.group(2)], m.group(1)), t)
    t = re.sub(r'\\subsection\*\{([^}]*)\}', r'\n### \1\n', t)
    names = {'theorem': 'Theorem', 'lemma': 'Lemma', 'proposition': 'Proposition', 'corollary': 'Corollary',
             'conjecture': 'Conjecture', 'definition': 'Definition', 'remark': 'Remark'}
    for env, name in names.items():
        def head(m, name=name):
            opt = ' (%s)' % m.group(1) if m.group(1) else ''
            return '\n**%s %s%s.** ' % (name, labels[m.group(2)], opt) if m.group(2) else '\n**%s%s.** ' % (name, opt)
        t = re.sub(r'\\begin\{%s\}(?:\[([^\]]*)\])?(?:\\label\{([^}]*)\})?' % env, head, t)
        t = t.replace('\\end{%s}' % env, '\n')
    t = t.replace('\\begin{proof}', '\n*Proof.* ').replace('\\end{proof}', ' ∎\n')
    t = re.sub(r'\\begin\{equation\}\\label\{([^}]*)\}(.*?)\\end\{equation\}',
               lambda m: '\n$$%s\\tag{%s}$$\n' % (m.group(2).strip(), labels[m.group(1)]), t, flags=re.S)
    t = re.sub(r'\\\[(.*?)\\\]', lambda m: '\n$$%s$$\n' % m.group(1).strip(), t, flags=re.S)
    t = t.replace('\\begin{enumerate}', '').replace('\\end{enumerate}', '')
    n = [0]

    def item(m):
        n[0] += 1
        return '\n(%d) ' % n[0]
    t = re.sub(r'\\item\s*', item, t)
    t = re.sub(r'\\eqref\{([^}]*)\}', lambda m: '(%s)' % labels[m.group(1)], t)
    t = re.sub(r'~?\\ref\{([^}]*)\}', lambda m: ' ' + labels[m.group(1)], t)
    t = re.sub(r'\\cite\[([^\]]*)\]\{([^}]*)\}', lambda m: '[%s, %s]' % (cites[m.group(2)], m.group(1)), t)
    t = re.sub(r'\\cite\{([^}]*)\}', lambda m: '[' + ', '.join(cites[k] for k in m.group(1).split(',')) + ']', t)
    t = re.sub(r'\\emph\{([^{}]*)\}', r'*\1*', t)
    t = re.sub(r'\\textbf\{([^{}]*)\}', r'**\1**', t)
    t = re.sub(r'\\texttt\{([^{}]*)\}', lambda m: '`%s`' % m.group(1).replace('\\_', '_'), t)
    t = t.replace('~', ' ').replace('\\,', ' ').replace("\\'a", 'á').replace('\\"o', 'ö').replace('--', '-')
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t


out = '# %s\n\nThe same text as `sign-free.pdf`, without the drawings. Generated from `sign-free.tex` by `research/2026-11-14_fable_sign-free-note/code/tex2md.py`.\n\n**Abstract.** %s\n%s' % (
    title, conv(abstract), conv(body))
open(dst, 'w', encoding='utf-8').write(out.strip() + '\n')
print('written', dst, len(out.split()), 'words')
