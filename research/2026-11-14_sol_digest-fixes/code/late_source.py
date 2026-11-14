from pathlib import Path
p=Path('digestions/route-map/routes.py'); s=p.read_text()
s=s.replace('Independent rainbow referee accepts these proofs with corrections; final summary pending.', 'Independent rainbow referee accepts these proofs with corrections in its completed REPORT.md.')
s=s.replace('Detailed referee accepts R and S with stated corrections; final summary pending.', 'Completed rainbow review accepts R and S with stated corrections; no human check.')
s=s.replace('Detailed referee accepts unique exchange and resident-eviction results; final summary pending.', 'Completed rainbow review accepts unique exchange and resident-eviction results; no human check.')
s=s.replace('Ordinary packing and named one-sided results checked in detailed report; same model as author, independent code; final summary pending.', 'Ordinary packing and named one-sided results accepted in completed report; same model as author, independent code; no human check.')
s += '''
_upd('D.families',where='+; rf/REPORT.md; rf/INTEGRATION.md',text='+ Different-model review checks finite tube sequences and matrix certificates, but not the all-length transfer code. Prism-chain Hamiltonian counts require an explicit gluing rule; they are not invariant under identification.')
_upd('D.tubes',where='+; rf/REPORT.md',text='+ Additional different-model referee confirms finite sequences and certificate arithmetic but explicitly leaves the all-length transfer code unchecked. The earlier all-length referee and this finite replay have different scopes.')
_upd('N.x15',where='+; rf/REPORT.md',text='+ The refutation concerns signs on the variables of F, hence one state only. Signs on both states incidences are not refuted: finite gauge equations remain solvable on the tested census. This does not establish a general positive formula.')
'''
p.write_text(s,encoding='utf8')
