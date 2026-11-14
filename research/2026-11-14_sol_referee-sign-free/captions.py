from check import BASE,ROOT,instance,forest
import collections,itertools,json,ast
d=json.loads((ROOT/'proofs/sign-free/figures/figdata.json').read_text())
f=d['running']['faces'];R=set(f[d['running']['t0']]);v=13
rot=[sorted({y for t in f if x in t for y in t if y!=x}) for x in range(v)]
out=instance(rot,f,d['running']['t0'],False)
assert out['rainbow']==1792 and out['good']==6 and out['covers']==2
ef=collections.defaultdict(list)
for i,t in enumerate(f):
    for e in itertools.combinations(t,2):ef[tuple(sorted(e))].append(i)
colors={d['running']['t0']:0};q=list(colors)
for t in q:
    for e in itertools.combinations(f[t],2):
        for z in ef[tuple(sorted(e))]:
            if z not in colors:colors[z]=1-colors[t];q.append(z)
black=[tuple(sorted(f[t])) for t in range(len(f)) if not colors[t]]
t0=tuple(sorted(f[d['running']['t0']]))
bi={t:v+i for i,t in enumerate(black)}
def decode(s):return {int(x):tuple(t) for x,t in s.items()}
def edges(s):return [(bi[t],x) for t in black for x in t if s.get(x)!=t]
def tree(s):return forest(edges(s),v+len(black))
def exc(s):return sum(abs(collections.Counter(s.values())[t]-1) for t in black if t!=t0)
def exchange(s,x):
    options=[]
    for t in black:
        if t!=s[x] and t!=t0 and x in t:
            z=dict(s);z[x]=t
            if tree(z):options.append(z)
    assert len(options)==1
    return options[0]
a,b=decode(d['rainbow']['a']),decode(d['rainbow']['b'])
assert tree(a) and tree(b) and exc(a)==2 and exc(b)==0
assert collections.Counter(a.values())[(1,2,9)]==2 and (0,2,3) not in a.values()
z=exchange(a,8)
assert z[8]==(8,11,12) and exc(z)==4
gamma=d['exchange']['gamma']
gg=[bi[tuple(z)] if isinstance(z,list) else z for z in gamma]
ee={frozenset(e) for e in edges(a)}|{frozenset((bi[a[8]],8))}
assert len(set(gg))==len(gg) and all(frozenset((x,y)) in ee for x,y in zip(gg,gg[1:]+gg[:1]))
start=decode(d['orbit']['s']);end=decode(d['orbit']['image'])
assert exc(start)==exc(end)==0 and tree(start) and tree(end)
z=exchange(start,2)
assert z==a
z=exchange(z,9);assert z==decode(d['orbit']['walk'][1]['sigma'])
z=exchange(z,3);assert z==end
coords=d['badcover']['coordinates']
states=[{ast.literal_eval(t):x for t,x in s.items()} for s in d['badcover']['states']]
u={ast.literal_eval(t):x for t,x in d['badcover']['u'].items()}
for i,s in enumerate(states):
    other=states[1-i]
    assert set(s.values())==set(range(3,16))
    assert all({s[t],other[t],u[t]}==set(t) for t in s)
    arcs={(other[t],u[t]) for t in s}
    cycle=d['badcover']['q_cycles'][i]
    assert all((x,y) in arcs for x,y in zip(cycle,cycle[1:]+cycle[:1]))
collisions=[(x,y) for x,y in itertools.combinations(coords,2) if coords[x]==coords[y]]
assert ('4','5') in collisions
(BASE/'captions.json').write_text(json.dumps(dict(command='python research/2026-11-14_sol_referee-sign-free/captions.py',running=out,figure5_coincident_vertices=collisions,checked=['rainbow loads','exchange endpoint and excess','fundamental cycle','involution orbit','both directed triangles in bad cover']),indent=2))
print(out,collisions)
