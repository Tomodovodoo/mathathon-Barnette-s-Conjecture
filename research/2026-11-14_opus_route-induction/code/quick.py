import time
from tri import *
for n in range(6,15):
    rots = plantri(n); t=time.time()
    tot=0; noTM=0; inst=0
    for rot in rots:
        T = from_rotation(rot)
        for t0 in range(len(T.F)):
            R = T.rooted(t0)
            inv = R.invariants(full=True)
            inst+=1
            if inv['pairs']>0 and inv['TM']==0: noTM+=1
            if (inv['pairs']>0) != (inv['TM']>0): print('MISMATCH', n)
            assert inv['TM'] == inv['TMpos']+inv['TMneg']
    print(n, len(rots), inst, noTM, round(time.time()-t,2))
