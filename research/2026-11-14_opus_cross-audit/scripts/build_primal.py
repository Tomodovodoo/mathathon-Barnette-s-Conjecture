"""Copy of research/2026-11-14_astra_primal-revision/build.py with logs and renders
redirected to ../build-primal/ so that the rebuild does not write into the reviser's folder."""
"""Translate the checked Markdown, add a one-page dictionary and natural-size figures."""
from pathlib import Path
import re,json,subprocess
OUT=Path(__file__).resolve().parent.parent/'build-primal';OUT.mkdir(exist_ok=True)
ROOT=Path(__file__).resolve().parents[3];HERE=ROOT/'proofs/primal'
def esc(s):return ''.join({'&':r'\&','%':r'\%','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','\\':r'\textbackslash{}'}.get(c,c) for c in s)
def inline(s):
 out=[]
 for t in re.split(r'(\$[^$]+\$|`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*)',s):
  if t.startswith('$'):out.append(t.replace(',',r',\allowbreak '))
  elif t.startswith('`'):out.append(r'\nolinkurl{'+t[1:-1]+'}')
  elif t.startswith('**'):out.append(r'\textbf{'+esc(t[2:-2])+'}')
  elif t.startswith('*'):out.append(r'\emph{'+esc(t[1:-1])+'}')
  else:out.append(esc(t))
 return ''.join(out)
md=(HERE/'PRIMAL-PROOF.md').read_text(encoding='utf8');out=[];math=False
for line in md.splitlines():
 if line=='$$':out.append(r'\end{equation*}' if math else r'\begin{equation*}');math=not math;continue
 if math:out.append(line);continue
 if line.startswith('# '):continue
 if line.startswith('## '):out.append(r'\section*{'+esc(line[3:])+'}');continue
 if line.startswith('### '):out.append(r'\subsection*{'+esc(line[4:])+'}');continue
 out.append(inline(line))
pre=r'''\documentclass[a4paper,11pt]{amsart}
\usepackage[margin=1in]{geometry}
\usepackage[T1]{fontenc}
\usepackage{lmodern,amsmath,amssymb,microtype,url,tabularx,booktabs}
\makeatletter\def\input@path{{../../paper/figures/}}\makeatother\usepackage{barnette-figs}
\usepackage[hidelinks]{hyperref}
\setlength{\emergencystretch}{3em}
\allowdisplaybreaks
\title{Barnette's conjecture in the cubic graph}
\author{Primal reconstruction, gpt-6-astra}
\date{14 November 2026, refereed revision}
\begin{document}
\maketitle
'''
out += [r'\clearpage\section*{Primal-dual dictionary}',r'\begingroup\footnotesize\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.35}',r'\noindent\begin{tabularx}{\textwidth}{@{}*{6}{>{\raggedright\arraybackslash}X}@{}}\toprule']
rows=[x for x in (HERE/'DICTIONARY.md').read_text(encoding='utf-8-sig').splitlines() if x.startswith('|') and not x.startswith('| ---')]
for j,row in enumerate(rows):
 cells=[x.strip() for x in row.strip('|').split('|')]
 # discretionary breaks in long declaration names, keep table readable at footnote size
 def cell(x):
  if ('_' in x or 'TriangleSystem' in x or 'ColoredDual' in x) and cells.index(x)==5:return r'\nolinkurl{'+x+'}'
  return esc(x)
 out.append(' & '.join(cell(x) for x in cells)+r'\\'+(r'\midrule' if j==0 else ''))
out += [r'\bottomrule\end{tabularx}\par\endgroup',r'\medskip',inline('LIT for the source terminology; PROVED-HERE for the identifications. Sources: OpenAI, Sections 2--7; Li, Definitions 5--6, Lemmas 7--8, Claim 25 and Appendix C; the constructive paper, Sections 1, 4, 5 and 7. Lean namespaces and exact citation scopes are in STATUS.md. With aligned signs and weights, the real-sign polynomial is i to the power n times Lean\'s phase polynomial. The recovery tree here lies in G, whereas the sources also use a tree on white faces.')]
caps=json.loads((HERE/'figures/captions.json').read_text(encoding='utf-8-sig'))
for i,(name,cap) in enumerate(caps.items()):
 if i%2==0:out.append(r'\clearpage')
 out += [r'\begin{center}\begin{minipage}{\textwidth}\centering',r'\input{figures/'+name+'-body.tex}',r'\par\smallskip\raggedright\footnotesize '+esc(f'Figure {i+1}. '+cap),r'\end{minipage}\end{center}\vspace{5mm}']
(HERE/'primal.tex').write_text(pre+'\n'.join(out)+'\n\\end{document}\n',encoding='utf8')
for i in range(2):
 p=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','primal.tex'],cwd=HERE,capture_output=True,text=True)
 (OUT/f'latex-{i+1}.log').write_text(p.stdout)
 assert p.returncode==0,p.stdout[-4000:]
log=(HERE/'primal.log').read_text();bad=[float(x) for x in re.findall(r'Overfull \\hbox \(([0-9.]+)pt',log)]
assert not any(x>2 for x in bad),bad
assert 'undefined references' not in log and 'LaTeX Error' not in log
import fitz
from PIL import Image,ImageDraw
doc=fitz.open(HERE/'primal.pdf');render=OUT/'renders';render.mkdir(exist_ok=True)
for i,page in enumerate(doc):page.get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(render/f'page-{i+1:02}.png')
for start in range(0,len(doc),4):
 canvas=Image.new('RGB',(1200,1700),'white')
 for j in range(start,min(start+4,len(doc))):
  im=Image.open(render/f'page-{j+1:02}.png');im.thumbnail((600,825));x=((j-start)%2)*600;y=((j-start)//2)*850;canvas.paste(im,(x,y+20));ImageDraw.Draw(canvas).text((x+10,y+3),f'Page {j+1}',fill='black')
 canvas.save(render/f'contact-{start//4}.png')
print('Pages',len(doc),'overfull widths',bad)

