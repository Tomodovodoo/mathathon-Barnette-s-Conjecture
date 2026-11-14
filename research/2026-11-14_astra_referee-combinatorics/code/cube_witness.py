"""A new cardinality obstruction to an abstract partition into c_min-cubes."""
from check import *
M=list(generated(13))[7]
R=Root(M,2)
R.check()
assert R.m==2 and len(R.tm)==6
out={'command':' '.join(sys.argv),'faces':M.faces,'root':R.o,'A':R.A,'states':R.ss,'tree_matchings':R.tm,
     'pairs':R.pp,'results':witness(R),'obstruction':'Six elements cannot be partitioned into sets of four.'}
(HERE/'cube_cardinality.json').write_text(json.dumps(out,indent=2))
print(out['obstruction'], 'V=13, c_min=2, TM=6')
