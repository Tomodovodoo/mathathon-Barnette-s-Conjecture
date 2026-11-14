from pathlib import Path
f = Path('research/2026-11-14_fable_final-polish/REPORT.md'); s = f.read_text(encoding='utf-8')
for a, b in [
    ("The 10 incidences without flow are listed.", "The 5 incidences without flow are listed (25 incidences between `A` and `X`, of which 20 are used)."),
    ("Setting Figure 2 back to `0.62\textwidth` would not recover the page; shortening the Lean paragraph by about five lines probably would.", "I did not test which cut recovers the page. The closing section is about fifteen lines longer than before and Figure 2 about 1.4cm taller."),
    ("In its Figures 1 and 2 some face labels (`f6`, `f11`, `f12`) sit close to curves of G.", "In its Figures 1 and 2 some face labels (`f6`, `f11`, `f12`) looked close to curves of G on a 66 dpi contact sheet. I did not inspect them at 200 dpi."),
]:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
f.write_text(s, encoding='utf-8', newline='\n')
