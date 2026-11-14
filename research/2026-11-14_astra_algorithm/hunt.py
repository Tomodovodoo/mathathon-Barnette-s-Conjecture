"""Adversarial relabelling/root search for the public hybrid; 480s total cap."""
from experiments import *
from barnette_lab.optimized import hamiltonian_cycle


if __name__=='__main__':
    if len(sys.argv)>1:
        c=json.loads((BASE/'hunt-instances.json').read_text())[int(sys.argv[1])]
        b=rooted(c);e0=edge(*sorted(c['root'])[:2]);e=b.dual_edges[e0];st=Counter()
        start=time.perf_counter();cycle=hamiltonian_cycle(b.G,e,st);elapsed=time.perf_counter()-start
        if not verify(b.G,cycle,e):raise AssertionError('bad certificate')
        print(json.dumps(dict(name=c['name'],n=len(b.G),seconds=elapsed,stats=st,cycle=cycle,forbidden=e,status='ok')))
        sys.exit()
    start=time.monotonic();rng=random.Random(719883);cases=[]
    for i in range(60):
        g=nx.octahedral_graph();target=rng.choice((30,50,80,120))
        while len(g)<target:g=split(g,rng)
        perm=list(g);rng.shuffle(perm);g=nx.relabel_nodes(g,dict(zip(list(g),perm)))
        b=Instance(g);cases.append(case(f'hunt-{i}',g,rng.choice(b.faces)))
    (BASE/'hunt-instances.json').write_text(json.dumps(cases))
    with (BASE/'hunt.jsonl').open('w') as f:
        for i,c in enumerate(cases):
            if time.monotonic()-start>480:break
            try:
                p=subprocess.run([sys.executable,'-B',__file__,str(i)],capture_output=True,text=True,timeout=8)
                row=json.loads(p.stdout) if p.returncode==0 else dict(name=c['name'],status='error',error=p.stderr)
            except subprocess.TimeoutExpired:row=dict(name=c['name'],status='timeout')
            f.write(json.dumps(row)+'\n');f.flush()
            if i%10==0:print(i,round(time.monotonic()-start,2),flush=True)
