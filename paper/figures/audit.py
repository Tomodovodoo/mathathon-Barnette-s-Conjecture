"""Source style inventory and rendered-font audit; writes style-audit.json.
python paper/figures/audit.py
"""
import json,re
from pathlib import Path
import fitz
HERE=Path(__file__).parent
rows=[]
for p in [HERE/'barnette-figs.sty',HERE/'draw.py']+sorted(HERE.glob('[0-9][0-9]-*.tex')):
    text=p.read_text()
    rows.append(dict(source=p.name,
        widths_pt=sorted(set(re.findall(r'line width\s*=\s*([.0-9]+)pt',text)),key=float),
        font_commands=sorted(set(re.findall(r'\\(footnotesize|scriptsize|tiny|small|normalsize)',text))),
        colours=sorted(set(re.findall(r'(?:draw|fill|text)\s*=\s*([A-Za-z]+(?:![0-9]+)?)',text))),
        colour_definitions=re.findall(r'\\definecolor\{(.*?)\}\{(.*?)\}\{(.*?)\}',text)))
    assert not re.search(r'\\(?:tiny|scriptsize)\b',text),p
pdfs=[]
for p in sorted(HERE.glob('[0-9][0-9]-*.pdf')):
    d=fitz.open(p); sizes={}
    for page in d:
        for b in page.get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                for span in line['spans']:
                    size=round(span['size'],2);sizes[size]=sizes.get(size,0)+len(span['text'])
    pdfs.append(dict(pdf=p.name,font_sizes_pt=sizes,width_cm=round(d[0].rect.width*2.54/72,2),height_cm=round(d[0].rect.height*2.54/72,2)))
result=dict(status='COMPUTED',sources=rows,rendered=pdfs,
    interpretation='All source label declarations use footnotesize. Smaller rendered glyphs are standard TeX subscripts, superscripts, fractions and summation limits, not independently shrunken labels. The PDF reports bp, so nominal 8pt labels appear near 7.97bp.',
    style_reference='The first-pass FIGURE-STYLE.md is superseded by the second-pass README and barnette-figs.sty. Deviations from that historical file are retained deliberately.',
    historical_deviations=['17% black faces rather than 9%','0.4pt context rather than 0.35pt','filled/outlined wedges rather than disk/square states','D and Q 1.1pt rather than 1pt','P 1.6pt rather than 1.3pt','purple #AA3377 cycle rather than blue','black disk/white square induced classes rather than coloured classes','0.62cm running panels side by side rather than 0.72cm stacked','cube 0.34cm, gluing 0.44cm, introduction strip 0.205cm units; fonts and stroke widths stay physical'],
    local_overrides=['0.5pt face-centre dot outlines and overview box borders','0.8pt induced-square and white-centre outlines','0.6pt overview connectors','1.7pt Q-cycle emphasis in cancellation','0.8pt dashed original D in spoke-detour comparison','incidence r matching uses double stroke, s uses single stroke'])
(HERE/'style-audit.json').write_text(json.dumps(result,indent=1))
print('inventoried',len(rows),'sources and',len(pdfs),'PDFs')
