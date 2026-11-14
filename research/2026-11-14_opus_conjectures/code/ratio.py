import sys, re
from fractions import Fraction
mn = None; below = 0; n = 0; at_half = 0
for l in sys.stdin:
    if not l.startswith('R '): continue
    L = int(re.search(r' L=(\d+)', l).group(1)); Lt = int(re.search(r'Ltp=(\d+)', l).group(1))
    r = Fraction(Lt, L); n += 1
    if mn is None or r < mn: mn = r; ex = l.strip()
    if r < Fraction(1, 2): below += 1
    if r == Fraction(1, 2): at_half += 1
print(sys.argv[1], 'instances', n, 'min fraction', mn, 'below 1/2:', below, 'exactly 1/2:', at_half, '| example:', ex[:90])
