"""Write data/eul_<V>.json: rotation systems of all Eulerian triangulations, V<=Vmax.
Usage: python gen_census.py 16"""
import json, sys
from tri import generate
E = generate(int(sys.argv[1]), verbose=True)
for V, ts in E.items():
    with open(f"data/eul_{V}.json", "w") as f:
        json.dump([{str(k): v for k, v in T.rot.items()} for T in ts], f)
