"""Sample the same rounded cubic controls emitted to TikZ; no independent drawing."""
import math
import numpy as np
from model import und

def samples(pieces, n=160):
    out=[]
    u=np.linspace(0,1,n+1)[:,None]
    for piece in pieces:
        a,b,c,d=(np.round(q,3) for q in piece)
        q=(1-u)**3*a+3*(1-u)**2*u*b+3*(1-u)*u**2*c+u**3*d
        out.extend(q[:-1])
    out.append(np.round(pieces[-1][-1],3))
    return np.array(out)

def intersections(path, segments):
    hits={}
    p=path[:-1]; r=np.diff(path,axis=0)
    for key, poly in segments.items():
        points=[]; angles=[]
        for q,z in zip(poly[:-1],poly[1:]):
            s=z-q; den=r[:,0]*s[1]-r[:,1]*s[0]
            ok=abs(den)>1e-12
            v=q-p
            t=np.divide(v[:,0]*s[1]-v[:,1]*s[0],den,out=np.full(len(r),2.),where=ok)
            u=np.divide(v[:,0]*r[:,1]-v[:,1]*r[:,0],den,out=np.full(len(r),2.),where=ok)
            for j in np.where(ok & (t>=-1e-8)&(t<=1+1e-8)&(u>=-1e-8)&(u<=1+1e-8))[0]:
                point=p[j]+t[j]*r[j]
                if not any(np.linalg.norm(point-old)<.006 for old in points):
                    points.append(point)
                    angles.append(math.degrees(math.asin(min(1,abs(den[j])/(np.linalg.norm(r[j])*np.linalg.norm(s))))))
        if points: hits[key]=(len(points),min(angles))
    return hits

def arc(p,a,b,r):
    d=(b-a+180)%360-180
    t=np.radians(np.linspace(a,a+d,361))
    return np.column_stack((np.cos(t),np.sin(t)))*r

def verify(data):
    from draw import Panel, ang, RING
    report=[]
    for name,run,state in data:
        m=run['model']; xy=run['xy']; R=run['R']; p=Panel(m,xy,R)
        T={e:(arc(p,ang(xy[e[0]]),ang(xy[e[1]]),R) if p.outer(*e) else np.array([xy[v] for v in e])) for e in m.E}
        angles=[]
        for g in m.G.edges():
            path=samples(p.dual_curves(g))
            if m.t0 in g:
                a,b=m.cross[und(*g)]; start=ang(p.mid(a,b))
                path=np.concatenate((path,arc(p,start,-90,R+RING)[1:]))
            hits=intersections(path,T); expected=m.cross[und(*g)]
            assert set(hits)=={expected} and hits[expected][0]==1,(name,'G',g,expected,hits)
            angles.append(hits[expected][1])
        H={(t,v):np.array([p.cen[t],xy[v]]) for t in m.A for v in m.F[t]}
        for t,v in zip(m.A,state):
            hits=intersections(samples(p.white_curves(run['rec'],t,v)),H)
            assert set(hits)=={(t,v)} and hits[t,v][0]==1,(name,'white',t,v,hits)
            angles.append(hits[t,v][1])
        assert min(angles)>10,(name,'near tangent',min(angles))
        report.append(dict(example=name,G_edges=m.G.number_of_edges(),white_edges=len(state),samples_per_cubic=160,minimum_crossing_angle_degrees=min(angles)))
    return report
