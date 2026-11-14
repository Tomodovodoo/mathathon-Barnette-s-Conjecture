from pathlib import Path
p=Path('digestions/route-map/build_map.py');s=p.read_text(encoding='utf8').replace('edgecolor="none", zorder=5))','edgecolor="none", zorder=2.5))')
s=s.replace('            avail=(width-1.8)*fig.dpi\n            while tx.get_window_extent(fig.canvas.get_renderer()).width>avail and tx.get_fontsize()>5.2:\n                tx.set_fontsize(tx.get_fontsize()-0.2)','''            srcwidth=max(0.32,len(r["src"])*(FS-1)*0.57/72)
            avail=(width-1.45-srcwidth-0.1)*fig.dpi
            lim=48
            while tx.get_window_extent(fig.canvas.get_renderer()).width>avail and lim>12:
                lim-=1
                tx.set_text(textwrap.shorten(r["label"],width=lim,placeholder="..."))''')
p.write_text(s,encoding='utf8')
# Supersede obsolete report-availability prose in the maintained documents.
p=Path('labyrinth/README.md');s=p.read_text(encoding='utf8').replace('Merged and involution texts are under review at this snapshot.','Merged main theorem now has one independent AI referee, FOLLOWS; proposed ancillary edits are not certified applied. Its second cold read and the involution referee remain pending.')
p.write_text(s,encoding='utf8')
p=Path('digestions/steps/09-what-is-still-open.md');s=p.read_text(encoding='utf8').replace('The exact merged, primal and involution texts still need human review.','The exact merged, primal and involution texts still need human review. The merged theorem route now has one independent AI referee, verdict FOLLOWS, in `research/2026-11-14_sol_referee-main/REPORT.md`. Eight ancillary edits are proposed, including Laurent terminology; their application is not certified here. The second cold read remains pending.')
p.write_text(s,encoding='utf8')
