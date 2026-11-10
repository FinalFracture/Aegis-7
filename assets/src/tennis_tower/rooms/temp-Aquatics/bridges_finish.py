import sys, math; from pathlib import Path
AQ_HERE=Path(__file__).resolve().parent; TT=AQ_HERE.parent.parent
sys.path[:0]=[str(TT),str(TT/'structure')]
from struct_lib import *
AQ_HERE=Path(__file__).resolve().parent
def add(it,n,m,mesh): it.append((n,m,mesh)); return mesh
def B(it,n,m,a,b,c,d,e,f): return add(it,n,m,box(a,b,c,d,e,f))
import numpy as np

def _spans(stations, posts, gap=.021):
    spans=[]
    for a,b in zip(stations, stations[1:]):
        u=a+(gap if any(abs(a-p)<1e-6 for p in posts) else 0.0)
        v=b-(gap if any(abs(b-p)<1e-6 for p in posts) else 0.0)
        if v>u: spans.append((u,v))
    return spans

def landing_note():
    return 'Dogleg landing E/S edges and span N edge west of X2.1 closed; 1.12 m scissor guard'

def landing_guard_items():
    it=[]
    # East edge of the landing, plus a return kick 4 mm short of the X2.1 guard.
    B(it,'Bridge_Kick',G,1.92,2.00,6.1,6.2,56.00,58.14)
    B(it,'Bridge_Kick',G,2.00,2.096,6.1,6.2,58.06,58.14)
    zs=(56.10,56.80,57.50,58.05)
    for z in zs: B(it,'Bridge_Post',ST,1.935,1.985,6.196,7.19,z-.025,z+.025)
    B(it,'Bridge_CapRail',ST,1.92,2.00,7.186,7.22,56.00,58.14)
    for a,b in zip(zs,zs[1:]):
        B(it,'Bridge_Pane_Scissor',SCR,1.952,1.968,6.23,7.15,a+.021,b-.021)
    # South edge, clear of the gallery wall face at X 0.15.
    B(it,'Bridge_Kick',G,0.155,1.916,6.1,6.2,56.00,56.08)
    sx=(0.25,0.95,1.65)
    for x in sx: B(it,'Bridge_Post',ST,x-.025,x+.025,6.196,7.19,56.015,56.065)
    B(it,'Bridge_CapRail',ST,0.155,1.916,7.186,7.22,56.00,56.08)
    for u,v in _spans((0.16,)+sx+(1.91,), sx):
        B(it,'Bridge_Pane_Scissor',SCR,u,v,6.23,7.15,56.032,56.048)
    # North edge of the span west of the existing Z60.30 guard (kick begins at X2.1).
    B(it,'Bridge_Kick',G,0.155,2.096,6.1,6.2,60.26,60.34)
    nx=(0.25,1.0,1.75)
    for x in nx: B(it,'Bridge_Post',ST,x-.025,x+.025,6.196,7.19,60.275,60.325)
    B(it,'Bridge_CapRail',ST,0.155,2.096,7.186,7.22,60.26,60.34)
    for u,v in _spans((0.16,)+nx+(2.09,), nx):
        B(it,'Bridge_Pane_Scissor',SCR,u,v,6.23,7.15,60.292,60.308)
    return it

def gate_note():
    return ('T2 queue gate: 1.10 m clear Z58.65..59.75 + 0.65 m solid each side; '
            'aligned to the bridge centre; tower opening alignment is an open Rook item')

def t2_gate_items():
    it=[]
    for za,zb in ((58.00,58.526),(59.874,60.40)):
        B(it,'Gate_FlarePanel',WH,19.84,19.92,6.1,7.22,za,zb)
        B(it,'Gate_FlareInlay',CY,19.832,19.844,6.70,6.74,za+.05,zb-.05)
        zc=(za+zb)*.5
        for i,y in enumerate((6.35,6.6,6.85)):
            m=add(it,'Gate_LeafCrests',LF2,leaf_dir((19.836,y,zc),(0,1,0.35 if i%2==0 else -0.35),.28,.14))
            uv=m.metadata['uv']; m.vertices[:,0] = 19.836 + (m.vertices[:,0]-19.836)*0.1; m.metadata['uv']=uv
    B(it,'Gate_Posts',G,19.82,19.94,6.1,8.50,58.53,58.65)
    B(it,'Gate_Posts',G,19.82,19.94,6.1,8.50,59.75,59.87)
    B(it,'Gate_Header',WH,19.80,19.96,8.30,8.50,58.654,59.746)
    B(it,'Gate_StatusLight',GRN,19.776,19.804,8.36,8.44,59.14,59.26)
    yc=8.50+0.10-0.006
    for z in (58.59,59.81):
        add(it,'Gate_BallFinial',BA,node((19.88,yc,z),0.10,1))
    return it

def canopy_note():
    return 'Slide-bridge leaf canopy, posts inboard of the guards, clear 2.45 m+, below +9.25 (soffit +9.7)'

def _arc(z):
    return 8.55+0.30*math.sin(math.pi*(z-58.24)/1.92)

def _downhill(z):
    dydz=0.30*math.pi/1.92*math.cos(math.pi*(z-58.24)/1.92)
    return (0.10, -abs(dydz), -1.0 if dydz>0 else 1.0)

def _tris(it):
    return sum(len(m.faces) for _,_,m in it)

def canopy_items():
    it=[]
    frames=(3.0,6.0,9.0,12.0,15.0,18.0)
    z_posts=(58.24,60.16)
    for x in frames:
        for z in z_posts:
            z1=min(z+.09, 60.25)  # north kick occupies z 60.26..60.34
            B(it,'Canopy_Footplate',G,x-.09,x+.09,6.096,6.13,z-.09,z1)
            add(it,'Canopy_Posts',G,tube((x,6.126,z),(x,8.51,z),.05,12))
        for i in range(8):
            z0=58.24+0.24*i; z1=z0+0.24
            y0=8.55-0.004 if i==0 else _arc(z0)  # 4 mm into the post top, within 8 mm
            y1=8.55-0.004 if i==7 else _arc(z1)
            add(it,'Canopy_Ribs',ST,tube((x,y0,z0),(x,y1,z1),.04,8))
    for t in (0.25,0.5,0.75):
        z=58.24+1.92*t; y=_arc(z)+0.075
        add(it,'Canopy_Purlins',ST,tube((2.6,y,z),(19.4,y,z),.03,8))
    step=0.42
    probe=leaf_dir((0,0,0),(0,1,.2),.46,.30,t=.012)
    one=len(probe.faces)
    used=_tris(it)
    while step<1.5:
        xs=np.arange(2.7,19.35,step)
        if used+len(xs)*7*one<5200: break
        step=round(step+0.06,2)
    groups={x:[] for x in frames}
    ts=np.linspace(0.05,0.95,7)
    for i,t in enumerate(ts):
        z=float(58.24+1.92*t); y=_arc(z)+0.22; d=_downhill(z)
        for x in xs:
            px=float(x)+0.21*(i%2)
            m=add(it,'Canopy_Leaves',LF2,leaf_dir((px,y,z),d,.46,.30,t=.012))
            groups[min(frames, key=lambda f: abs(f-px))].append(m)
    r=0.09
    for x in frames:
        if not groups[x]: continue
        hy=max(m.vertices[:,1].max() for m in groups[x])
        cy=min(8.55+0.30+0.20, 9.249-r)
        if cy-r>=hy+0.02:
            m=node((x,cy,59.20),r,1)
            if m.vertices[:,1].max()<9.25 and _tris(it)+len(m.faces)<5200:
                add(it,'Canopy_BallMedallion',BA,m)
    return it

if __name__=='__main__':
    def show(label, items):
        tris=_tris(items)
        print('%s %d items %d tris'%(label,len(items),tris))
        for n,mk,m in items:
            assert 'glass' not in n.lower(), n
            assert m.metadata['uv'].shape[1]==2, n
        return items
    show('landing', landing_guard_items())
    show('gate', t2_gate_items())
    cn=show('canopy', canopy_items())
    assert _tris(cn)<5200
    top=max(m.vertices[:,1].max() for _,_,m in cn)
    band=[]
    for n,_,m in cn:
        if n not in ('Canopy_Ribs','Canopy_Leaves'): continue
        v=m.vertices
        k=(v[:,2]>=58.4)&(v[:,2]<=60.1)
        if np.any(k): band.append(float(v[k,1].min()))
    head=min(band)
    print('canopy max y %.4f  rib/leaf y in Z58.4..60.1 %.4f'%(top,head))
    print(landing_note()); print(gate_note()); print(canopy_note())
    assert top<9.25, top
    assert head>=8.5, head
