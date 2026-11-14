"""Generate benchmark tables, descriptive fits and reproducibility manifest."""
from experiments import *
import math, statistics, platform, hashlib


rows=[json.loads(s) for fn in ('census.jsonl','families.jsonl','hybrid.jsonl') for s in (BASE/fn).read_text().splitlines()]
methods=sorted({r['method'] for r in rows})
text=['# Benchmarks','',
'Every result in this file is COMPUTED, from `research/2026-11-14_astra_algorithm/experiments.py`. This is finite evidence. Timings do not establish a polynomial bound. All successful rows retain their cycle and forbidden edge, checked against primal adjacency by `optimized.verify`, which uses no dual or matching objects.','',
'## Inputs and timing boundary','',
'The census contains all 15 unrooted plantri Eulerian triangulations through dual order 12 and all 262 facial rootings. Each rooting uses the side joining its two least-labelled root vertices. This is not an all-edge benchmark; separate unit tests exercise every edge of the four named graphs. Four solvers run on every census input.','',
'The larger campaign contains 30 inputs: width-4 and width-6 tubes with 2, 6, 12 and 24 layers; prism sums with 2, 6, 12 and 24 factors; three split-generated samples at each dual order 20, 40, 80 and 150; the saved 38- and 40-vertex periodic-evict graphs; and chains of 1, 2, 4 and 8 copies of the 16-vertex trap. Graphs and roots are saved in `families-instances.json`. The largest primal input has 300 vertices. The evict graphs are reused as inputs; their original rainbow-tree walk states are not pair-walk starting states.','',
'The random generator starts from an octahedron and repeatedly splits a uniformly chosen vertex between two even-separated neighbours in its rotation, adding a degree-four vertex. Seeds are 7461, 7462 and 7463. Orders in one seed are nested samples. This distribution favours graphs obtainable by these insertions and is not uniform over Barnette graphs. Tube and prism generation imports the earlier family module read-only.','',
'Times begin after construction of the rooted lab Instance. They include flow, the chosen search, recovery and any separator recursion. They exclude initial planarity checking, dense incidence-matrix construction, public input validation and the final independent certificate check. Each larger solver job has its own process and an eight-second wall cap including startup. CP-SAT has a six-second internal cap, one search worker and an AddCircuit formulation on both orientations of every allowed edge; no loops are supplied, so every vertex must be visited. OR-Tools was already installed. Its import is included in the recorded SAT time. Census timings use one process, so its first SAT call includes a cold import.','',
'## Methods','',
'`optimized` in the raw logs means rollback enumeration alone, with minimum-remaining-corners ordering and incremental matching repair. It has no initial flow hint. `hybrid` is the public implementation: flow, up to 32 deterministic unvisited-neighbour exchanges ranked by Q-cycle count, bounded path DP, then complete enumeration. `reference` is the existing lab solve function with its flow-first enumeration. `baseline` is primal Hamiltonian-path backtracking with a residual degree test.','',
'`marked` is the manuscript ordered-token walk, capped at 2,000 moves. `random` and `greedy` are the reference exchange walks with seed 24 and 500-move caps. Greedy chooses randomly among neighbours of least Q-cycle count; it is not guaranteed monotone. BFS and best-first retain visited pairs and stop at 2,000 expansions. Best-first ranks by Q-cycle count. These caps are measurement limits, not existence failures. At dual order at most 16, pair methods start at the first enumerated nongood pair when one exists; larger pair methods start at the flow pair. Thus move and time comparisons with flow-first reference/hybrid are not comparisons from identical starting states.','',
'`path-dp` is complete within a frontier-width limit of 16 and a table limit of 100,000. The hybrid uses limits 12 and 20,000. It orders black centres by their sorted corner triples. A width-limit rejection is reported as capped, not as no good state.','',
'## Aggregate results','',
'The table combines the census and family campaigns. Only optimized, reference, baseline and SAT have census rows. Maxima exclude censored runs.','',
'| Method | Successes / runs | Capped or timed out | Largest successful n | Maximum successful seconds | Worst successful input |',
'|---|---:|---:|---:|---:|---|']
for method in methods:
    rs=[r for r in rows if r['method']==method];ok=[r for r in rs if r['status']=='ok'];worst=max(ok,key=lambda r:r['seconds'])
    text.append(f'| {method} | {len(ok)} / {len(rs)} | {sum(r["status"] in ("capped","timeout") for r in rs)} | {max(r["n"] for r in ok)} | {worst["seconds"]:.6f} | {worst["name"]} |')
text+=['','| Walk | Maximum successful exchanges | Maximum phases | Maximum normalization reversals |','|---|---:|---:|---:|']
for method in ('marked','random','greedy','bfs','best-first','hybrid'):
    rs=[r for r in rows if r['method']==method and r['status']=='ok']
    text.append(f'| {method} | {max(r["stats"].get("moves",0) for r in rs)} | '+(str(max(r['stats']['phases'] for r in rs)) if method=='marked' else 'not applicable')+' | '+(str(max(r['stats']['normalization_reversals'] for r in rs)) if method=='marked' else '0')+' |')
text+=['','No error rows are omitted. The scripts distinguish no-pair and no-good-state from caps. A failed certificate aborts the run.','',
'![Maximum recorded solver time by order](time.png)','',
'![Maximum recorded pair-walk length by order](moves.png)','',
'The figures use black lines and separate directly labelled panels. Zero-move runs are legitimate. Enumeration nodes, SAT branches and exchanges are different quantities and are not combined into one move count.','',
'## Family comparisons','',
'| Input | n | Rollback-only seconds | Reference seconds | Hybrid seconds | Path DP seconds |',
'|---|---:|---:|---:|---:|---:|']
cases=json.loads((BASE/'families-instances.json').read_text())
for c in cases:
    vals=[]
    for m in ('optimized','reference','hybrid','path-dp'):
        r=next(r for r in rows if r['name']==c['name'] and r['method']==m)
        vals.append(f'{r["seconds"]:.6f}' if r['status']=='ok' else r['status'])
    text.append('| '+c['name']+' | '+str(2*len(nx.Graph(c['edges']))-4)+' | '+' | '.join(vals)+' |')
text+=['','## Descriptive growth fits','',
'For each method and named family below, fit log(time)=a+p log(n) by ordinary least squares over successful sizes. Only families with at least three distinct successful orders are included. A censored size is omitted and its count is printed. These tiny, structured samples and omitted timeouts cannot estimate asymptotic worst-case complexity.','',
'| Family | Method | Successful observations | Censored observations | Fitted p |','|---|---|---:|---:|---:|']
fits=[]
for family in ('tube4','tube6','prism-sum','trap-chain','split'):
    for method in ('optimized','reference','hybrid','path-dp','baseline','sat'):
        rs=[r for r in rows if r['name'].startswith(family+'-') and r['method']==method]
        ok=[r for r in rs if r['status']=='ok']
        if len({r['n'] for r in ok})<3:continue
        xs=[math.log(r['n']) for r in ok];ys=[math.log(r['seconds']) for r in ok]
        xm,ym=statistics.mean(xs),statistics.mean(ys)
        p=sum((x-xm)*(y-ym) for x,y in zip(xs,ys))/sum((x-xm)**2 for x in xs)
        fits.append(dict(family=family,method=method,observations=len(ok),censored=len(rs)-len(ok),exponent=p))
        text.append(f'| {family} | {method} | {len(ok)} | {len(rs)-len(ok)} | {p:.3f} |')
text+=['','## What the measurements support','',
'The hybrid succeeds on all 30 larger inputs. Rollback enumeration alone is not the best dispatch: it times out on some narrow tubes despite cheap individual prefix tests. The path DP solves every tested tube and prism-sum input; their observed frontier widths are 8 for width-4 tubes and prism sums, and 10 for width-6 tubes. A small separator between layers matters more here than the global count of states.','',
'The experiment does not establish a best pivot rule. It does not test height-guided or bidirectional pair search, a full restart portfolio, dynamic planar connectivity, a precomputed linear-time separator decomposition, or a sphere-cut solver. The current greedy rule can increase Q-cycle count, and C3 is not used for correctness. The largest sizes are those selected for this campaign, not a hardware maximum.','',
'## Reproduction','',
'Run from the repository root:', '', '```powershell',
'python -B research/2026-11-14_astra_algorithm/experiments.py census',
'python -B research/2026-11-14_astra_algorithm/experiments.py families',
'python -B research/2026-11-14_astra_algorithm/experiments.py hybrid',
'python -B research/2026-11-14_astra_algorithm/experiments.py figures',
'python -B research/2026-11-14_astra_algorithm/metrics.py',
'```','',
'Each campaign runs one worker at a time and stops after 480 seconds. Complete archived output has 1,048 census rows, 270 original-family rows and 60 hybrid/DP rows. Do not interpret a shorter rerun after its campaign cap as complete. `manifest.json` records versions and hashes. Figures and tables are generated by committed scripts. All timings are a single run, not repeated confidence intervals.']
(ROOT/'proofs/algorithm/BENCHMARKS.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
(BASE/'fits.json').write_text(json.dumps(fits,indent=2))
import ortools, sympy
files=[p for p in BASE.iterdir() if p.is_file() and p.name!='manifest.json']
files+=list((ROOT/'workings/barnette_lab/barnette_lab/optimized').glob('*.py'))
manifest=dict(python=sys.version,platform=platform.platform(),processor=platform.processor(),networkx=nx.__version__,sympy=sympy.__version__,ortools=ortools.__version__,sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
(BASE/'manifest.json').write_text(json.dumps(manifest,indent=2))
