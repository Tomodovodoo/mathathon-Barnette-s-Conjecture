from pathlib import Path
p=Path('digestions/route-map/build_map.py');s=p.read_text(encoding='utf8')
s=s.replace('    ymax = 1.75 if detail else 1.15','    ymax = 2.25 if detail else 1.15')
s=s.replace('        s = STEP[sid]\n        ax.text(x, ytop + 0.13', '''        s = STEP[sid]
        # Route lists have an opaque backing so dense bypass strands stay behind them.
        nr=len(BY_STEP[sid])
        ax.add_patch(FancyBboxPatch((x-0.04, ytop-nr*RH-0.04), width+0.08, nr*RH+0.32,
                                   boxstyle="square,pad=0", facecolor="white", edgecolor="none", zorder=5))
        ax.text(x, ytop + 0.13''')
s=s.replace('            ax.text(x + 0.95, y, r["label"], fontsize=FS, va="center", ha="left", color=tcol, zorder=6)', '''            # The catalogue keeps the full title; this index uses a shortened title.
            import textwrap
            title=textwrap.shorten(r["label"],width=48,placeholder="...")
            tx=ax.text(x + 1.45, y, title, fontsize=FS, va="center", ha="left", color=tcol, zorder=6)
            avail=(width-1.8)*fig.dpi
            while tx.get_window_extent(fig.canvas.get_renderer()).width>avail and tx.get_fontsize()>5.2:
                tx.set_fontsize(tx.get_fontsize()-0.2)''')
s=s.replace('rows("U", xc + 0.45, yu)','rows("U", xc, yu)')
p.write_text(s,encoding='utf8')
p=Path('digestions/route-map/routes.py');s=p.read_text(encoding='utf8');s+='''
# Late main-manuscript referee delivered during final integration.
_upd('G2.main',where='paper/main/barnette.tex; research/2026-11-14_sol_referee-main/REFEREE.md; research/2026-11-14_sol_referee-main/EDITS.md',text='Merged dual proof independently AI-refereed: FOLLOWS for Theorem 1.1, including the inside-cycle connectivity repair. Eight replacements proposed; application not checked here. Off-route Remark 4.10 is Laurent, not an ordinary polynomial with the chosen heights. Second cold read remains pending.')
checked('G2.main','research/2026-11-14_sol_referee-main','Main theorem route FOLLOWS. Off-route Laurent terminology and conditional-scope edits proposed; application not certified. Second cold read pending.')
''';p.write_text(s,encoding='utf8')
for fn in ['digestions/steps/00-overview.md','digestions/route-map/HOW-IT-WORKS.md']:
    p=Path(fn);s=p.read_text(encoding='utf8');s+='''

Late review update. The merged manuscript now has one independent AI referee, `research/2026-11-14_sol_referee-main/REPORT.md`, verdict FOLLOWS for the main theorem, including the disk-connectivity repair. Eight edits are proposed; their application is not certified here. The off-route generating expression in Remark 4.10 is Laurent with these heights, not an ordinary polynomial. The second cold read and the involution referee are still pending at this scan. This supersedes the earlier under-review wording for the merged main route only.
''';p.write_text(s,encoding='utf8')
p=Path('labyrinth/seed.py');s=p.read_text(encoding='utf8').replace("for entry in S['entries']:","for entry in S['entries']:\n    if entry['id']=='new-presentations': entry['status']='Merged theorem AI-refereed FOLLOWS, eight edits proposed; second cold read and involution review pending. Earlier primal version AI-refereed, revision self-audited; M4 disagreement explicit. No human check.'")
p.write_text(s,encoding='utf8')
