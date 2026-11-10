import sys, math; from pathlib import Path
AQ_HERE=Path(__file__).resolve().parent; TT=AQ_HERE.parent.parent
sys.path[:0]=[str(TT),str(TT/'structure')]
from struct_lib import *        # brings box, tube, node, leaf_dir, trimesh, np, G, ST, LF, LF2, BA, E ... (overwrites HERE; never use HERE)
AQ_HERE=Path(__file__).resolve().parent
def add(it,n,m,mesh): it.append((n,m,mesh)); return mesh

# Enclosed T1/T2 spiral tubes (spec 3.6). Building metres, Y up. Centre y = invert + RI.
# Section matches Rook's tt_slide_tower r2 stub: 16 staves, flats on the cardinals, inner/outer flat
# apothems 0.3960/0.4460 (stub vertex radii 0.4041/0.4532 are bevel points). Our sharp 16-gon uses the
# corner radii of those flats, so the bore floor flat is +7.004 at the stub face, the same as the stub's.
RI,RO,SEG=0.3960/math.cos(math.pi/16),0.4460/math.cos(math.pi/16),16
PHASE=math.pi/SEG
XS,CX,R,S=25.53,24.66,0.87,0.20
X_END,STUB_X=22.60,25.052   # flush with the tower stub end face
RB=XS-STUB_X                # 0.478 elbow radius (> RO)
H_STUB,H_EXIT,RUN_S=7.40-RI,1.45,0.10   # centre +7.40 at the stub face
TRI_PIECE=2700

def _cat(chunks):
    P=np.vstack([p for p,_ in chunks]); T=np.vstack([t for _,t in chunks])
    T=T/np.linalg.norm(T,axis=1,keepdims=True)
    keep=np.r_[True, np.linalg.norm(np.diff(P,axis=0),axis=1)>=1e-3]
    P,T=P[keep],T[keep]
    return [(P[i].copy(),T[i].copy()) for i in range(len(P))]

def centreline(zs, cz, turns):
    """(P, T) stations, invert-based, plus per-section height data. Joins drop <1 mm duplicates."""
    # Level lead-in: the elbow starts horizontal (vertical start face at STUB_X) and eases linearly to 1:5.
    z0=zs+RB; earc=RB*math.pi/2; h_elbow=H_STUB-S*earc/2; h_entry=h_elbow-S*(cz-z0)
    na=int(math.ceil(earc/0.12)); a=np.linspace(-math.pi/2,0,na+1); s=RB*(a+math.pi/2); h=H_STUB-S*s*s/(2*earc)
    Pe=np.c_[STUB_X+RB*np.cos(a), h+RI, z0+RB*np.sin(a)]
    Te=np.c_[-RB*np.sin(a), -S*RB*(s/earc), RB*np.cos(a)]
    ns=int(math.ceil((cz-z0)/1.0)); z=np.linspace(z0,cz,ns+1); hs=h_elbow-S*(z-z0)
    Ps=np.c_[np.full_like(z,XS), hs+RI, z]
    Ts=np.c_[np.zeros_like(z), np.full_like(z,-S), np.ones_like(z)]
    th_max=2*math.pi*turns; nh=int(math.ceil((R*th_max)/0.30)); th=np.linspace(0,th_max,nh+1)
    hh=h_entry+(H_EXIT-h_entry)*(th/th_max); dh=(H_EXIT-h_entry)/th_max
    Ph=np.c_[CX+R*np.cos(th), hh+RI, cz+R*np.sin(th)]
    Th=np.c_[-R*np.sin(th), np.full_like(th,dh), R*np.cos(th)]
    x=np.linspace(CX,X_END,3); hr=H_EXIT-RUN_S*(CX-x); lane=cz+R
    Pr=np.c_[x, hr+RI, np.full_like(x,lane)]
    Tr=np.c_[np.full_like(x,-1.0), np.full_like(x,-RUN_S), np.zeros_like(x)]
    info=dict(elbow_end=float(h_elbow),
              straight=dict(z0=float(z0),z1=float(cz),h0=float(h_elbow),slope=S,
                            h=lambda zz, z0=float(z0), h0=float(h_elbow): h0-S*(zz-z0)),
              helix=dict(cz=float(cz),turns=float(turns),h_entry=float(h_entry),h_exit=H_EXIT),
              runout=dict(z=float(lane),h=lambda xx: H_EXIT-RUN_S*(CX-xx)))
    return _cat([(Pe,Te),(Ps,Ts),(Ph,Th),(Pr,Tr)]), info

def _frames(stations):
    P=np.asarray([p for p,_ in stations],float)
    T=np.asarray([t for _,t in stations],float)
    T=T/np.linalg.norm(T,axis=1,keepdims=True)
    side=np.cross(np.broadcast_to([0.,1.,0.],T.shape), T)
    side=side/np.linalg.norm(side,axis=1,keepdims=True)
    up=np.cross(T,side)
    return P,T,side,up

def sweep_annulus(stations, ri=RI, ro=RO, seg=SEG):
    """Closed annular tube. Outer normals outward, inner normals into the bore, annular end caps."""
    P,T,side,up=_frames(stations); n=len(P); k=np.arange(seg); phi=2*np.pi*k/seg+PHASE
    rad=np.cos(phi)[None,:,None]*side[:,None,:]+np.sin(phi)[None,:,None]*up[:,None,:]
    outer=P[:,None,:]+ro*rad; inner=P[:,None,:]+ri*rad
    V=np.ascontiguousarray(np.vstack([outer.reshape(-1,3), inner.reshape(-1,3)]))
    o=lambda i,kk: i*seg+(kk%seg); inn=lambda i,kk: n*seg+o(i,kk)
    F=[]
    for i in range(n-1):
        for kk in range(seg):
            a,b,c,d=o(i,kk),o(i,kk+1),o(i+1,kk),o(i+1,kk+1)
            F+=[(a,b,d),(a,d,c)]
            a,b,c,d=inn(i,kk),inn(i,kk+1),inn(i+1,kk),inn(i+1,kk+1)
            F+=[(a,d,b),(a,c,d)]
    for kk in range(seg):
        a,b,c,d=o(0,kk),o(0,kk+1),inn(0,kk),inn(0,kk+1)
        F+=[(a,c,d),(a,d,b)]
        a,b,c,d=o(n-1,kk),o(n-1,kk+1),inn(n-1,kk),inn(n-1,kk+1)
        F+=[(a,d,c),(a,b,d)]
    m=trimesh.Trimesh(V, np.asarray(F,np.int64), process=False)
    step=np.linalg.norm(np.diff(P,axis=0),axis=1)
    arc=np.concatenate([[0.], np.cumsum(step)])
    u=np.repeat(arc,seg); v=np.tile(k/float(seg), n)
    m.metadata['uv']=np.column_stack([np.r_[u,u], np.r_[v,v]]).astype(float)
    m.fix_normals()
    assert m.is_watertight
    assert m.metadata['uv'].shape==(len(m.vertices),2)
    return m

def _split_idx(stations):
    P=np.asarray([p for p,_ in stations],float)
    h0=next(i for i in range(len(P)-1) if abs(P[i,0]-XS)<1e-3 and P[i+1,0]<XS-1e-3)
    zmax=float(P[:,2].max())
    h1=max(i for i in range(len(P)) if abs(P[i,0]-CX)<1e-3 and abs(P[i,2]-zmax)<1e-3)
    assert h1>h0
    return h0, h0+(h1-h0)//2

def tube_pieces(stations):
    """Elbow+straight, first half of the helix, rest of helix + runout. Each mesh < 2700 tris."""
    h0,mid=_split_idx(stations)
    spans=[stations[:h0+1], stations[h0:mid+1], stations[mid:]]
    out=[]
    def emit(span):
        if 4*SEG*len(span)>=TRI_PIECE and len(span)>2:
            m=len(span)//2; emit(span[:m+1]); emit(span[m:]); return
        mesh=sweep_annulus(span)
        assert len(mesh.faces)<TRI_PIECE
        out.append(mesh)
    for s in spans: emit(s)
    return out

def _cy_straight(info,z): return info['straight']['h'](z)+RI
def _cy_theta(info,th):
    H=info['helix']; u=th/(2*math.pi*H['turns'])
    return H['h_entry']+(H['h_exit']-H['h_entry'])*u+RI
def _cy_runout(x): return H_EXIT-RUN_S*(CX-x)+RI

def _foot(it,x,z,w):
    h=w/2; add(it,'Tube_Footplate',G,box(x-h,x+h,1.008,1.050,z-h,z+h))
def _clamp(it,x,z,y0,y1):
    add(it,'Tube_HardwareClamp',ST,box(x-.04,x+.04,y0,y1,z-.04,z+.04))
def _post(it,x,z,y0,y1):
    add(it,'Tube_SupportPosts',G,tube((x,y0,z),(x,y1,z),0.06,12))
def stand(it,x,z,ob):
    _foot(it,x,z,0.30); _post(it,x,z,1.046,ob-0.030); _clamp(it,x,z,ob-0.040,ob+0.012)
def stack(it,x,z,ob1,ot1,ob2):
    stand(it,x,z,ob1)
    _clamp(it,x,z,ot1-0.012,ot1+0.040)
    _post(it,x,z,ot1+0.030,ob2-0.030)
    _clamp(it,x,z,ob2-0.040,ob2+0.012)

def _tree(it,info):
    H=info['helix']; cz=H['cz']; top=H['h_entry']+RI+0.50
    _foot(it,CX,cz,0.70)
    add(it,'Helix_TreeTrunk',G,tube((CX,1.046,cz),(CX,top,cz),0.25,12))
    th=math.pi/4; limit=2*math.pi*H['turns']-0.2
    while th<limit:
        y=_cy_theta(info,th); c,s=math.cos(th),math.sin(th)
        add(it,'Tube_HardwareArms',ST,beam((CX+0.235*c,y,cz+0.235*s),(CX+0.435*c,y,cz+0.435*s),0.06,0.06))
        th+=math.pi/2
    for i in range(10):
        a=2*math.pi*i/10; c,s=math.cos(a),math.sin(a)
        add(it,'Helix_LeafCrown',LF2,leaf_dir((CX+0.12*c,top,cz+0.12*s),(c*0.6,1,s*0.6),0.32,0.16))
    add(it,'Helix_BallFinial',BA,node((CX,top+0.12,cz),0.11,1))

def tube_items():
    it=[]; infos=[]
    for zs,cz,turns in ((52.3,64.88,2.25),(58.3,68.38,3.25)):
        stations,info=centreline(zs,cz,turns); infos.append(info)
        for m in tube_pieces(stations): add(it,'Slide_Tube',LF,m)
    i1,i2=infos
    for z in (54.0,56.5): stand(it,XS,z,_cy_straight(i1,z)-RO)
    for z in (60.0,62.8):
        stack(it,XS,z,_cy_straight(i1,z)-RO,_cy_straight(i1,z)+RO,_cy_straight(i2,z)-RO)
    stand(it,XS,66.63,_cy_straight(i2,66.63)-RO)
    for info in infos:
        _tree(it,info)
        stand(it,23.40,info['runout']['z'],_cy_runout(23.40)-RO)
    return it

def tube_note():
    return 'Enclosed T1/T2 spiral tubes from tower +X stubs (16-gon, centre +7.40, level start face at X 25.05 easing to 1:5) down X 25.53 strip to NE-corner helices; runouts run -X into lanes Z 65.75/69.25; crown max +7.85; no walkway crossing'

# T1 +Z / T2 -Z link openings (tt_slide_tower r2, 1ef96f1): X 23.60..24.70, clear from +7.0.
# Enclosure faces at world Z 55.911 (T1) / 57.089 (T2); sills Z 55.796..55.913 / 57.087..57.204.
LX0,LX1=23.60,24.70
LZ0,LZ1=55.909,57.091     # deck/finish embed 4 mm into each tower sill (no gap at either door)
GZ0,GZ1=55.915,57.085     # kicks/posts/rails stop 4 mm short of the enclosure faces

def link_items():
    """T1<->T2 +7.0 link deck spanning the gap between the towers. Underside +6.75 keeps the
    ground-entry gap below clear."""
    it=[]
    add(it,'Link_Deck',WH,box(LX0,LX1,6.75,6.985,LZ0,LZ1))
    add(it,'Link_DeckFinish',SSL,box(LX0+.002,LX1-.002,6.981,7.0,LZ0+.002,LZ1-.002))
    zs=(GZ0+.04,(GZ0+GZ1)/2,GZ1-.04)
    for x0,d in ((LX0,1.0),(LX1,-1.0)):
        xs=lambda u,v: (min(x0+d*u,x0+d*v),max(x0+d*u,x0+d*v))
        k=xs(0,0.08); add(it,'Link_Kick',G,box(k[0],k[1],6.996,7.10,GZ0,GZ1))      # 4 mm into the deck finish
        q=xs(0.02,0.06)
        for z in zs: add(it,'Link_Post',ST,box(q[0],q[1],7.096,8.084,z-.02,z+.02))  # 4 mm into kick and rail
        r=xs(0.005,0.075); add(it,'Link_CapRail',ST,box(r[0],r[1],8.08,8.12,zs[0]-.03,zs[-1]+.03))
        pc=(q[0]+q[1])/2
        for za,zb in zip(zs,zs[1:]):
            add(it,'Link_Pane_Scissor',SCR,box(pc-.008,pc+.008,7.098,8.082,za+.016,zb-.016))
    return it

def link_note():
    return 'T1<->T2 link deck at +7.0, X 23.60..24.70 between the tower link openings; 1.1 m guards; underside +6.75 keeps the ground-entry gap clear'

if __name__=='__main__':
    it=tube_items()
    tris=[len(m.faces) for _,_,m in it]
    Y=np.concatenate([m.vertices[:,1] for n,_,m in it if n=='Slide_Tube'])
    print(len(it), int(sum(tris)), int(max(tris)), float(Y.min()), float(Y.max()))
    assert float(Y.max())<=9.0
    assert link_items()
