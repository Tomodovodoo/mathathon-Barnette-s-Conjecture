"""Contact sheets (two pages per image) of rendered atlas pages, for inspection."""
import sys, glob, os
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
fs = sorted(glob.glob(src + '/*.png'))
for i in range(0, len(fs), 2):
    ims = [Image.open(f) for f in fs[i:i + 2]]
    s = Image.new('RGB', (sum(a.width for a in ims), ims[0].height), 'white'); x = 0
    for a in ims:
        s.paste(a, (x, 0)); x += a.width
    s.save(f'{dst}/s{i // 2:02d}.png')
print(len(fs), 'pages')
