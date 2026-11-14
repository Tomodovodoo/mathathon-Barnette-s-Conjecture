"""Extract the cited local primary texts and locate numbered citations."""
from verify_numbers import ROOT, OUT
import fitz,json,re
sources={
 'OpenAI2026':('papers/OpenAI-Barnette.pdf',['Theorem 1.1','Corollary 7.1','Corollary 7.2','Lemma 5.3','5.3']),
 'Li2026':('papers/A-Note-On-Barnette.pdf',['Definition 28','Lemma 30','Appendix C']),
 'Anonymous2026':('papers/barnette_trees.pdf',['Theorem 1.2','Proposition 6.2']),
 'Hertel2005':('research/2026-11-14_opus_history-literature/pdf/2005_Hertel_Survey-and-strengthening-Barnette.pdf',['Corollary 3','Theorem 10','64']),
 'Gorsky2023':('research/2026-11-14_opus_history-literature/pdf/2022_Gorsky-Steiner-Wiederrecht_Matching-theory-Barnette_arXiv2202.11641v3.pdf',['Theorem 4.3','Theorem 4.16']),
 'Alt2016':('research/2026-11-14_opus_history-literature/pdf/2013_Alt-Payne-Schmidt-Wood_Thoughts-on-Barnette_arXiv1312.3783.pdf',['Lemma 5','5.']),
 'Stein1971':('research/2026-11-14_opus_history-literature/pdf/1971_Stein_B-sets-and-planar-maps_PJM.pdf',['THEOREM 2.2']),
 'Brinkmann2022':('research/2026-11-14_opus_history-literature/pdf/2021_Brinkmann-Goedgebeur-McKay_Minimality-Georges-Kelmans_arXiv2101.00943.pdf',['Theorem 4.1','90','50']),
 'Schnieders2025':('research/2026-11-14_opus_history-literature/pdf/2025_Schnieders_Barnette-faces-up-to-8_arXiv2508.03531.pdf',['Corollary 1.13']),
 'Feder2006':('research/2026-11-14_opus_history-literature/pdf/2006_Feder-Subi_On-Barnettes-conjecture_ECCC-TR06-015.pdf',[]),
 'Hine2018':('research/2026-11-14_opus_history-literature/pdf/2018_Hine-Kalman_Clock-theorems-triangulated-surfaces_arXiv1808.06091.pdf',[]),
}
res={}
for key,(path,terms) in sources.items():
    doc=fitz.open(ROOT/path); txt='\n\f\n'.join(p.get_text() for p in doc)
    (OUT/f'source-{key}.txt').write_text(txt,encoding='utf-8')
    found={}
    for term in terms:
        hits=[]
        for i,p in enumerate(doc):
            flat=re.sub(r'\s+',' ',p.get_text())
            j=flat.find(term)
            if j>=0:hits.append(dict(pdf_page=i+1,context=flat[max(0,j-100):j+900]))
        found[term]=hits
    res[key]=dict(path=path,pages=len(doc),locators=found)
(OUT/'source-locators.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
print(json.dumps({k:{t:[x['pdf_page'] for x in hits] for t,hits in v['locators'].items()} for k,v in res.items()},indent=2))
