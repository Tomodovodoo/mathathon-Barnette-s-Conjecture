"""Rebuild stationary S, M, P transfers from independently embedded tubes.

No author code or boundary-state numbering is used. Pair costs are Boolean sets
of achievable cycle counts; integer weights independently count all pairs.
"""
from check import tube,instance,HERE,ROOT
import collections,itertools,json
import networkx as nx

def canon(xs):
    names={}
    return tuple(names.setdefault(x,len(names)) for x in xs)

def advance(inputs,active,rows,final,kind,marked=False):
    # Keys have one or two used-bit vectors followed by connectivity labels.
    copies=2 if kind=='P' else 1
    last={v:i for i,row in enumerate(rows) for v in row}
    last.update({v:len(rows) for v in final})
    if kind!='P':last[-1]=len(rows)
    for index,row in enumerate(rows):
        vertices=tuple(sorted(set(active)|set(row)))
        keep=tuple(v for v in vertices if last[v]>index)
        output=collections.defaultdict(lambda:[0,0]) if marked else collections.Counter()
        for key,multiplicity in inputs.items():
            used=[dict(zip(active,key[j])) for j in range(copies)]
            labels=dict(zip(active,key[-1])) if key[-1] else {}
            for v in vertices:
                if v not in labels: labels[v]=max(labels.values(),default=-1)+1
            options=[v for v in row if v!=-1]
            for selected in itertools.product(options,repeat=copies):
                if len(set(selected))!=copies:continue
                if any(used[j].get(v,False) for j,v in enumerate(selected)):continue
                newused=[{v:int(used[j].get(v,False) or v==selected[j]) for v in vertices} for j in range(copies)]
                if any(not newused[j][v] for j in range(copies) for v in vertices if v not in keep and v!=-1):continue
                lab=labels.copy()
                if kind=='M': ends=[v for v in row if v!=selected[0]]
                elif kind=='P':ends=list(selected)
                else:ends=[]
                inc=0
                if ends:
                    a,b=ends; x,y=lab[a],lab[b]
                    inc=int(x==y)
                    if kind=='M' and x==y:continue
                    lab={v:x if z==y else z for v,z in lab.items()}
                k=tuple(tuple(u[v] for v in keep) for u in newused)+(canon([lab[v] for v in keep]) if kind!='S' else (),)
                if marked:
                    for deg in range(2-inc):output[k][deg+inc]+=multiplicity[deg]
                else:output[k]+=multiplicity
        inputs=output;active=keep
    return inputs,active

def rebuild(p,kind,rec):
    g=tube(p,6); root=(0,1,p+1)
    A=instance(g,root,False)[3]; poles={7*p,7*p+1}
    level=lambda f:max(v//p for v in f if v not in poles)
    groups={j:sorted(tuple(sorted(f)) for f in A if level(f)==j) for j in range(7)}
    pre=[f for j in range(3) for f in groups[j]]
    if kind!='P':pre=[tuple(-1 if v in root else v for v in f) for f in pre]
    else:pre=[tuple(v for v in f if v not in root) for f in pre]
    layer=[tuple(v-2*p for v in f) for f in groups[3]]
    for j in (4,5):assert layer==[tuple(v-(j-1)*p for v in f) for f in groups[j]]
    cap=[tuple(p if v==7*p+1 else v-6*p for v in f) for f in groups[6] if 7*p+1 in f]
    initialkey=((),(),()) if kind=='P' else ((),())
    initial,act=advance({initialkey:1},(),pre,set(range(2*p,3*p)),kind)
    boundary=tuple(range(p)) if kind=='P' else (-1,)+tuple(range(p))
    assert act==(tuple(range(2*p,3*p)) if kind=='P' else (-1,)+tuple(range(2*p,3*p)))
    keys=list(initial); edges=[];cursor=0
    while cursor<len(keys):
        key=keys[cursor]
        targets,act=advance({key:1},boundary,layer,set(range(p,2*p)),kind)
        assert act==(tuple(range(p,2*p)) if kind=='P' else (-1,)+tuple(range(p,2*p)))
        for target,weight in targets.items():
            if target not in keys:keys.append(target)
            edges.append((cursor,keys.index(target),weight))
        cursor+=1
    terminal=[]
    for key in keys:
        result,_=advance({key:1},boundary,cap,set(),kind);terminal.append(sum(result.values()))
    v=[initial.get(k,0) for k in keys]; seq=[]
    for _ in range(len(keys)+len(rec)+5):
        seq.append(sum(a*b for a,b in zip(v,terminal)));new=[0]*len(keys)
        for i,j,m in edges:new[j]+=m*v[i]
        v=new
    d=len(rec)
    assert all(seq[k]==sum(a*seq[k-j-1] for j,a in enumerate(rec)) for k in range(d,len(seq)))
    record=dict(width=p,quantity=kind,dimension=len(keys),initial=seq[:d],recurrence=rec,checked_discrepancies=len(keys),sequence=seq[:12],matrix=edges,initial_vector=[initial.get(k,0) for k in keys],terminal=terminal,boundary_keys=keys)
    if kind=='P':
        ip,_=advance({initialkey:[1,0]},(),pre,set(range(2*p,3*p)),kind,True)
        pe=[];tw=[]
        for i,key in enumerate(keys):
            result,_=advance({key:[1,0]},boundary,layer,set(range(p,2*p)),kind,True)
            pe.extend((i,keys.index(k),tuple(a>0 for a in poly)) for k,poly in result.items())
            result,_=advance({key:[1,0]},boundary,cap,set(),kind,True)
            tw.append(tuple(any(poly[d] for poly in result.values()) for d in range(2)))
        v=[tuple(a>0 for a in ip.get(k,[0,0])) for k in keys];seen={};costs=[]
        while tuple(v) not in seen:
            seen[tuple(v)]=len(costs); total=[False,False]
            for a,b in zip(v,tw):
                for d in range(2):total[d]|=any(a[j] and b[d-j] for j in range(d+1))
            assert total==[False,True];costs.append(total);nxt=[[False,False] for _ in keys]
            for i,j,pol in pe:
                for d in range(2):nxt[j][d]|=any(v[i][k] and pol[d-k] for k in range(d+1))
            v=list(map(tuple,nxt))
        record['cost01_repeat']=[seen[tuple(v)],len(costs)]
    return record

def hstep(p,key,colors,stage):
    old,part=key; n=len(old); cs=old+colors
    g=nx.Graph();g.add_nodes_from(range(len(cs)))
    for block in set(part):
        vertices=[i for i,b in enumerate(part) if b==block]
        g.add_edges_from((vertices[0],v) for v in vertices[1:])
    if stage=='capA':
        es=[(0,i+1) for i in range(p)]+[(i+1,(i+1)%p+1) for i in range(p)];keep=set(range(1,p+1))
    elif stage=='capB':es=[(i,p) for i in range(p)];keep=set(range(p+1))
    else:
        es=[(p+i,p+(i+1)%p) for i in range(p)]+[(i,p+i) for i in range(p)]
        es += [(i,p+(i+1)%p) if i%2==0 else ((i+1)%p,p+i) for i in range(p)];keep=set(range(p,2*p))
    for a,b in es:
        if cs[a]==cs[b]:
            if nx.has_path(g,a,b):return None
            g.add_edge(a,b)
    comps=list(nx.connected_components(g))
    if stage=='capB':return len(comps)==2
    if {cs[i] for i in keep}!={0,1} or any(not (c&keep) for c in comps):return None
    labels={i:j for j,c in enumerate(comps) for i in c};keep=sorted(keep)
    return tuple(cs[i] for i in keep),canon(labels[i] for i in keep)

def hamilton(p,rec):
    initial=collections.Counter()
    for cs in itertools.product((0,1),repeat=p):
        k=hstep(p,((0,),(0,)),cs,'capA')
        if k is not None:initial[k]+=1
    keys=list(initial);edges=[];cursor=0
    while cursor<len(keys):
        for cs in itertools.product((0,1),repeat=p):
            k=hstep(p,keys[cursor],cs,'middle')
            if k is None:continue
            if k not in keys:keys.append(k)
            edges.append((cursor,keys.index(k),1))
        cursor+=1
    w=[sum(bool(hstep(p,k,(c,),'capB')) for c in (0,1)) for k in keys]
    v=[initial.get(k,0) for k in keys];seq=[]
    for _ in range(len(keys)+len(rec)+5):
        seq.append(sum(a*b for a,b in zip(v,w)));nv=[0]*len(keys)
        for i,j,n in edges:nv[j]+=v[i]*n
        v=nv
    d=len(rec);assert all(seq[k]==sum(a*seq[k-j-1] for j,a in enumerate(rec)) for k in range(d,len(seq)))
    return dict(width=p,quantity='H',dimension=len(keys),initial=seq[:d],recurrence=rec,sequence=seq[:12],matrix=edges,initial_vector=[initial.get(k,0) for k in keys],terminal=w,boundary_keys=keys)

def main():
    records=[]
    recs={4:{'S':[3,-1],'M':[1],'P':[1]},6:{'S':[7,-9,7,-1],'M':[0,4,4,0,1,0,-4,-4],'P':[4,-4,4]}}
    for p in [4,6]:
        for kind,rec in recs[p].items():
            row=rebuild(p,kind,rec);records.append(row);print(p,kind,row['dimension'],row['initial'],flush=True)
        row=hamilton(p,[2,-1,4] if p==4 else [2,-1,40,8,64,-16]);records.append(row);print(p,'H',row['dimension'],row['initial'],flush=True)
    (HERE/'rebuilt-transfers.json').write_text(json.dumps(records,indent=2))
if __name__=='__main__':main()
