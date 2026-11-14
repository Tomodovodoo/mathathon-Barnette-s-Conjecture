"""Fixed flow/weight/order marked-walk scaling, one <=20s worker at a time."""
from experiments import *
from barnette_lab.algorithms import marked_walk


if __name__=='__main__':
    if len(sys.argv)>1:
        i=int(sys.argv[1]);c=json.loads((BASE/'marked-chain-instances.json').read_text())[i]
        b=rooted(c);p=b.flow_pair();st=time.perf_counter()
        cap=100000 if len(sys.argv)>2 else 20000
        try:
            z,stats=marked_walk(b,p,cap=cap)
            cert=b.recover(z[1]);assert verify(b.G,cert['cycle'],cert['avoided_edge'])
            row=dict(name=c['name'],n=len(b.G),status='ok',seconds=time.perf_counter()-st,stats=stats,start=p,start_c=len(b.dcycles(*p)),cycle=cert['cycle'],forbidden=cert['avoided_edge'])
        except TimeoutError:
            row=dict(name=c['name'],n=len(b.G),status='capped',moves_at_least=cap,start=p,start_c=len(b.dcycles(*p)))
        if len(sys.argv)>2:(BASE/'marked-chain-eight.json').write_text(json.dumps(row),encoding='utf-8')
        print(json.dumps(row));sys.exit()
    old=json.loads((BASE/'families-instances.json').read_text());base=next(c for c in old if c['name']=='trap-chain-1')
    g=nx.Graph(base['edges']);base_g=g.copy();root=set(base['root']);cases=[]
    for k in range(1,11):
        cases.append(case(f'marked-chain-{k}',g,root))
        b=Instance(g);b=Instance(g,next(i for i,f in enumerate(b.faces) if set(f)==root))
        bb=Instance(base_g);ri=next(i for i,f in enumerate(bb.faces) if set(f)==root)
        g=glue_triangles(g,base_g,b.white[-1],ri)
    (BASE/'marked-chain-instances.json').write_text(json.dumps(cases))
    with (BASE/'marked-chains.jsonl').open('w') as f:
        for i,c in enumerate(cases):
            try:
                p=subprocess.run([sys.executable,'-B',__file__,str(i)],capture_output=True,text=True,timeout=20)
                row=json.loads(p.stdout) if p.returncode==0 else dict(name=c['name'],status='error',error=p.stderr)
            except subprocess.TimeoutExpired:row=dict(name=c['name'],status='timeout',limit=20)
            f.write(json.dumps(row)+'\n');f.flush();print({k:v for k,v in row.items() if k not in ('cycle','start')},flush=True)
