"""Reproduce source extraction aids and selected source-page renders."""
from pathlib import Path
import fitz

BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[1]
files=['papers/OpenAI-Barnette.pdf','papers/barnette_trees.pdf','papers/A-Note-On-Barnette.pdf','papers/equivalents/2023-Gorsky-Matching-theory-and-Barnettes-conjecture.pdf']
for f in files:
    d=fitz.open(ROOT/f)
    (BASE/'code'/f'{Path(f).stem}.txt').write_text('\n'.join('PAGE '+str(i+1)+'\n'+p.get_text() for i,p in enumerate(d)),encoding='utf-8')
for f,p,name in [(files[0],9,'source-openai-10'),(files[1],1,'source-trees-02'),(files[3],5,'source-gsw-06'),(files[3],6,'source-gsw-07'),(files[3],11,'source-gsw-12')]:
    fitz.open(ROOT/f)[p].get_pixmap(dpi=130).save(BASE/'pages'/f'{name}.png')
