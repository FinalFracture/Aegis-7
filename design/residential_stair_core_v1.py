# Residential rev C stair core v1.1 (bot lift #51 added; writes *_v1_1_*.png, v1 PNGs kept) (assets #3 stair set, #4 glass + handrail, #5 skylight). DESIGN ONLY.
# Plan coords: X (axial, fore -X / aft +X), Z (+Z spinward, -Z antispinward = Sector-4 promenade side). Y up (toward axis).
import math, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
WALL="#1A1E24"; GRAPH="#282E38"; PEARL="#D8DEE6"; AMB="#FF9500"; GRN="#3FAF6A"; VIO="#7B5CFF"; ORG="#D95B26"; U="#EEF1F5"
# ---- geometry ----
RISE=4.2; NR=26; R_=RISE/NR; T_=0.28; N1,N2=16,10           # unequal flights so the mid-landing clears the exit door head
FW=1.5; WELL=0.8; XC=(-1.9,1.9); ZS,ZN=-8.9,-0.8               # clear core: walls on centreline X+-2 (0.2), shell face Z -8.9, open to corridor at Z -0.8
F1=(-1.9,-1.9+FW); F2=(1.9-FW,1.9)                              # flight 1 west, flight 2 east; well X -0.4..0.4
LD=1.5; ZL=ZS+LD                                                # mid-landing Z -8.9..-7.4
Z1b=ZL+(N1-1)*T_; Z2t=ZL+(N2-1)*T_                              # flight 1 base riser, flight 2 top riser (L2 arrival edge)
YL=N1*R_; SLAB_L=0.25; SLAB2=0.30; ROOF=8.8; DOOR_H=2.3; HR=2.1; GUARD=1.1; RAIL=0.9; HANDRAIL_PROJ=0.1
G=dict(riser=R_,tread=T_,pitch=math.degrees(math.atan(R_/T_)),twoRplusT=2*R_+T_,YL=YL,soffitL=YL-SLAB_L,Z1b=Z1b,Z2t=Z2t,
       run1=(N1-1)*T_,run2=(N2-1)*T_,bottom_landing=ZN-Z1b,L2_landing=ZN-Z2t,clear_flight=FW-2*HANDRAIL_PROJ)
for k,v in G.items(): print(f"{k} = {v:.3f}")
def soffit_over(x,z):
    """lowest structure underside above L1 floor at plan point (x,z) for the L1 walk zones"""
    c=[ROOF]
    if ZS<=z<=ZL: c.append(YL-SLAB_L)                                          # mid-landing
    if F2[0]<=x<=F2[1] and ZL<=z<=Z2t: c.append(YL+(z-ZL)/T_*R_-SLAB_L)       # flight 2 waist underside
    if XC[0]<=x<=XC[1] and Z2t<=z<=ZN: c.append(RISE-SLAB2)                   # L2 landing slab
    if F1[0]<=x<=F1[1] and ZL<=z<=Z1b: c.append((Z1b-z)/T_*R_-SLAB_L)         # flight 1 (closed below)
    return min(c)
def over_flight(z,flight):
    """clear height above the nosing at z on a flight"""
    y=(Z1b-z)/T_*R_+R_ if flight==1 else YL+(z-ZL)/T_*R_+R_
    top=RISE-SLAB2 if (Z2t<=z<=ZN and flight==1) else ROOF
    return top-y
# ---- object table (plan, L1 level) ----
SOLID=[("flight 1 + closed under-stair store",F1[0],F1[1],ZL,Z1b),("glass guard F1 inner",-0.42,-0.38,ZL,Z1b),
       ("wall grab rail L1 W",-1.9,-1.86,Z1b,ZN),("strap locker (in under-stair store)",-1.85,-0.45,-6.6,-6.0)]
CLEAR=[("Sector-4 exit clear zone 2.6 x 1.5",-1.3,1.3,ZS,ZL),("L1 walk corridor->vestibule",-0.38,1.9,ZL,ZN),
       ("flight 1 bottom landing (to rail face)",-1.86,F1[1],Z1b,ZN),("core opening to corridor (to rail face)",-1.86,XC[1],ZN-0.9,ZN)]
DOORS=[("103",-4.5,1.4),("104",4.5,1.4),("Laundry",-2.0,1.4),("Maint",3.2,2.0)]   # corridor doors; clear zone 0.9 into corridor
for n,x,w in DOORS:
    zf=-0.8 if n in("103","104") else 0.8
    CLEAR.append((f"door {n} clear",x-w/2,x+w/2,(zf if zf<0 else zf-0.9),(zf+0.9 if zf<0 else zf)))
def ov(a,b): return a[1]<b[2]-1e-9 and b[1]<a[2]-1e-9 and a[3]<b[4]-1e-9 and b[3]<a[4]-1e-9
QC=[]
QC.append(("risers <= 0.17 m",R_<=0.17)); QC.append(("tread >= 0.28 m",T_>=0.28)); QC.append(("2R+T in 0.60..0.64",0.60<=2*R_+T_<=0.64))
QC.append(("risers sum to 4.2 m",abs(NR*R_-RISE)<1e-9 and N1+N2==NR))
QC.append(("fits 8.1 m clear (landing+run1+bottom landing)",abs(LD+G["run1"]+G["bottom_landing"]-(ZN-ZS))<1e-9 and G["bottom_landing"]>=FW))
QC.append(("mid-landing depth >= flight width",LD>=FW)); QC.append(("L2 landing depth >= flight width",G["L2_landing"]>=FW))
QC.append(("flight clear between handrails >= 0.9",G["clear_flight"]>=0.9))
QC.append(("exit door head 2.3 under mid-landing soffit",YL-SLAB_L>=DOOR_H))
QC.append(("solid/solid overlaps (except store inside flight)",[(a[0],b[0]) for i,a in enumerate(SOLID) for b in SOLID[i+1:] if ov(a,b) and "store" not in a[0]+b[0] and not ("guard" in a[0]+b[0] and "flight" in a[0]+b[0])]))
QC.append(("solids inside clear zones / door zones",[(s[0],c[0]) for s in SOLID for c in CLEAR if ov(s,c)]))
QC.append(("clear zones >= 0.9 m wide",[c[0] for c in CLEAR if min(c[2]-c[1],c[4]-c[3])<0.9-1e-9]))
hl=[]
for c in CLEAR[:2]:
    for i in range(21):
        for j in range(21):
            x=c[1]+(c[2]-c[1])*i/20; z=c[3]+(c[4]-c[3])*j/20
            if soffit_over(x,z)<HR-1e-9: hl.append((round(x,2),round(z,2),round(soffit_over(x,z),2)))
QC.append(("L1 walk + exit zone headroom >= 2.1 m",hl))
mh=min(min(over_flight(Z1b-k*T_-0.01,1) for k in range(N1-1)),min(over_flight(ZL+k*T_+0.01,2) for k in range(N2-1)))
QC.append((f"headroom over flights >= 2.1 m (min {mh:.2f})",mh>=HR))
QC.append(("min L1 walk soffit (m)",round(min(soffit_over(x/10,z/10) for x in range(-3,19) for z in range(int(ZS*10),int(ZN*10)+1)),3)))

# ---- v1.1: Sprocket bot lift + Maintenance re-plan (riser re-aligned so services stack) ----
SHAFT=(0.6,2.2,0.8,2.4); CAR=(0.8,2.0,1.0,2.2); LDOOR=(0.9,1.9); RISER=(0.6,1.6,2.4,3.4)
MAINT=(0.6,5.9,0.9,8.9); U202=(0.1,13.9,0.9,8.9)
M_SOL=[("lift shaft",)+SHAFT,("riser (re-aligned)",)+RISER,("tool wall",0.6,1.1,3.6,6.4),("substation",5.3,5.9,1.0,3.5),
       ("pad W",0.8,2.0,6.6,7.8),("pad E1",4.4,5.6,4.0,5.2),("pad E2",4.4,5.6,6.6,7.8),("spares shelf",4.3,5.9,8.4,8.9),("coupler mounts",0.6,1.9,8.4,8.9)]
M_CLR=[("egress lane corridor door -> service door (2.0 m)",2.2,4.2,0.9,8.9),("lift landing L1 (corridor) 1.2",0.8,2.0,-0.4,0.8)]
L2_SOL=[("lift shaft",)+SHAFT,("riser chase (re-aligned)",)+RISER,("202 services slot: lift controller + chase",0.1,0.6,0.9,3.4),
        ("202 wardrobe (moved)",0.1,0.6,3.5,6.5),("202 kitchen counter",5.0,9.0,0.9,1.5)]
L2_CLR=[("lift landing L2 (corridor) 1.2",0.8,2.0,-0.4,0.8),("202 entry path",2.55,3.45,0.9,7.8),("202 door clear",2.3,3.7,-0.1,0.8)]
CORE_L=[c for c in CLEAR if "door" in c[0] or "opening" in c[0]]
QC.append(("L1 Maintenance solid overlaps",[(a[0],b[0]) for i,a in enumerate(M_SOL) for b in M_SOL[i+1:] if ov(a,b)]))
QC.append(("L1 solids in egress lane / lift landing / corridor door zones",[(a[0],c[0]) for a in M_SOL for c in M_CLR+CORE_L if ov(a,c)]))
QC.append(("L1 lift landing vs other door/core zones",[c[0] for c in CORE_L if ov(M_CLR[1],c)]))
QC.append(("L2 solid overlaps",[(a[0],b[0]) for i,a in enumerate(L2_SOL) for b in L2_SOL[i+1:] if ov(a,b)]))
QC.append(("L2 solids in lift landing / 202 path / door zones",[(a[0],c[0]) for a in L2_SOL for c in L2_CLR if ov(a,c)]))
QC.append(("L2 lift landing vs 202 door + core opening",[c[0] for c in L2_CLR[2:]+CORE_L[-1:] if ov(L2_CLR[0],c)]))
inside=lambda r,b: b[0]<=r[0] and r[1]<=b[1] and b[2]<=r[2]+0.1 and r[3]<=b[3]
QC.append(("shaft + riser inside Maintenance (L1) and 202 (L2), same XZ both levels",inside(SHAFT,MAINT) and inside(SHAFT,U202) and inside(RISER,MAINT) and inside(RISER,U202)))
QC.append(("riser touches shaft (services stack)",abs(RISER[2]-SHAFT[3])<1e-9))
QC.append(("car 1.2 x 1.2 with >= 0.1 running clearance",CAR[1]-CAR[0]>=1.2-1e-9 and CAR[0]-SHAFT[0]>=0.1 and SHAFT[1]-CAR[1]>=0.1))
QC.append(("lift door >= Sprocket 0.78 + 0.2",LDOOR[1]-LDOOR[0]>=0.98))
QC.append(("lift landings >= 1.2 x 1.2",all(min(c[2]-c[1],c[4]-c[3])>=1.2-1e-9 for c in (M_CLR[1],L2_CLR[0]))))
QC.append(("egress lane >= 0.9 and straight door-to-door",M_CLR[0][2]-M_CLR[0][1]>=0.9))
QC.append(("each pad within 0.3 m of the egress lane",all(min(abs(p_[2]-2.2),abs(p_[1]-4.2))<=0.3 for p_ in M_SOL if p_[0].startswith("pad"))))
AREA=dict(maint_lost=(SHAFT[1]-SHAFT[0])*(SHAFT[3]-SHAFT[2]),u202_shaft=(SHAFT[1]-SHAFT[0])*(SHAFT[3]-SHAFT[2]),u202_slot=0.6*2.6,u202_riser=1.0,old_chase=1.0)
print("AREA",AREA)
for q in QC: print("QC:",q)
bad=[k for k,v in QC if not ((v is True) or (isinstance(v,list) and not v) or isinstance(v,float))]
assert not bad, ("QC failed",bad)
# ---- PLAN PNG: L1 | L2 ----
def R(ax,x0,x1,z0,z1,fc,ec="none",lw=0,z=2,**k): ax.add_patch(Rectangle((x0,z0),x1-x0,z1-z0,fc=fc,ec=ec,lw=lw,zorder=z,**k))
def T(ax,x,z,s,fs=7,**k): ax.text(x,z,s,ha=k.pop("ha","center"),va=k.pop("va","center"),fontsize=fs,color=k.pop("color",WALL),zorder=30,**k)
B=dict(fc="white",ec="none",pad=0.8)
fig,axs=plt.subplots(1,2,figsize=(16,13.5),dpi=150)
for lvl,ax in zip(("L1",'L2'),axs):
    R(ax,-6.5,6.5,-0.8,0.8,PEARL); T(ax,-4.9,0,"CORRIDOR 1.6 m",6.5,color="#555")
    names=[("103" if lvl=="L1" else "203",-6.5,-2,-9,-0.8),("104" if lvl=="L1" else "204",2,6.5,-9,-0.8)]
    names+= [("LAUNDRY",-6.5,0.5,0.8,9.0),("MAINT.\n42.5 m2",0.5,6.0,0.8,9.0),("102",6.0,6.5,0.8,9.0)] if lvl=="L1" else [("201",-6.5,0,0.8,9.0),("202  109.7 m2",0,6.5,0.8,9.0)]
    for n,x0,x1,z0,z1 in names: R(ax,x0,x1,z0,z1,U,ec=WALL,lw=2.5); (n!="102") and T(ax,(x0+x1)/2+(0 if z0>0 else (-1.0 if x0<0 else 1.0)) + (1.2 if n.startswith("202") else 0),((2.9 if n.startswith("MAINT") else 7.6) if z0>0 else -6.0),n,8.5,weight="bold",bbox=dict(fc="#EEF1F5",ec="none",pad=1))
    for x in (-2,2): ax.plot([x,x],[-9,-0.8],color=WALL,lw=4,zorder=5)
    ax.plot([-6.5,6.5],[-9,-9],color=WALL,lw=6,zorder=5)
    dz=[("103",-4.5,1.4,-0.8),("104",4.5,1.4,-0.8),("LAUNDRY",-2.0,1.4,0.8),("MAINT.",3.2,2.0,0.8)] if lvl=="L1" else [("203",-4.5,1.4,-0.8),("204",4.5,1.4,-0.8),("201",-3.0,1.4,0.8),("202",3.0,1.4,0.8)]
    for n,x,w,zf in dz:
        R(ax,x-w/2,x+w/2,zf-0.12,zf+0.12,"white",ec=VIO,lw=1.8,z=8); R(ax,x+w/2+0.05,x+w/2+0.4,(zf+0.12 if zf<0 else zf-0.32),(zf+0.32 if zf<0 else zf-0.12),AMB,ec=WALL,lw=0.8,z=8)
        R(ax,x-w/2,x+w/2,(zf if zf<0 else zf-0.9),(zf+0.9 if zf<0 else zf),VIO,z=3,alpha=0.08)
    if lvl=="L1":
        R(ax,-1.3,1.3,-9.12,-8.88,"white",ec=VIO,lw=2.2,z=8); R(ax,1.45,1.85,-8.85,-8.6,AMB,ec=WALL,lw=0.8,z=8)
        R(ax,-1.3,1.3,ZS,ZL,GRN,z=3,alpha=0.12)
        for k in range(N1): ax.plot([F1[0],F1[1]],[Z1b-k*T_]*2,color="#707A84",lw=0.9,zorder=6)
        R(ax,F1[0],F1[1],ZL,Z1b,"none",ec=GRAPH,lw=1.2,z=6)
        ax.annotate("",xy=(-1.15,ZL+0.3),xytext=(-1.15,Z1b-0.15),arrowprops=dict(arrowstyle="->",color=WALL,lw=1.3),zorder=9)
        T(ax,-1.15,-5.3,"FLIGHT 1\nUP 16 R",6.5,weight="bold",bbox=B)
        R(ax,XC[0],XC[1],ZS,ZL,"none",ec=GRAPH,lw=1,z=6,ls="--"); T(ax,0,-8.15,"mid-landing above (Y 2.58, soffit 2.33)",6,color="#555",bbox=B)
        R(ax,F2[0],F2[1],ZL,Z2t,"none",ec=GRAPH,lw=1,z=6,ls="--"); T(ax,1.15,-6.9,"flight 2\nabove",6,color="#555",bbox=B)
        ax.plot([0.6,0.6,0.2],[-1.2,-7.0,-7.6],color=GRN,lw=2,ls=(0,(3,2)),zorder=9); T(ax,1.3,-3.6,"L1 walk\n2.3 m clear\nhead >= 2.33",6,color="#1F6B3E",bbox=B)
        ax.plot([-0.4,-0.4],[ZL,Z1b],color=VIO,lw=2.5,zorder=7)
        for x in (-1.86,-0.44): ax.plot([x,x],[ZL,Z1b],color=AMB,lw=1.2,zorder=7)
        T(ax,-1.15,-2.0,"bottom\nlanding\n2.4 m",6,bbox=B)
        T(ax,-3.6,-8.4,"closed under flight 1:\nstore + strap locker",6,color=ORG,bbox=B); ax.plot([-2.6,-1.6],[-8.0,-6.5],color=ORG,lw=0.8,zorder=9)
        T(ax,0,-9.7,"SECTOR-4 EXIT 2.6 m (head 2.3) -> exit ramp + plaza (exterior v1.2)",7,weight="bold")
        gp=[(-1.9,-2.0),(1.9,-2.0),(1.9,-7.9),(-1.9,-7.9)]
    else:
        R(ax,XC[0],XC[1],Z2t,ZN,PEARL,z=2); T(ax,0,-2.6,"L2 LANDING\n(Y 4.20)",8,weight="bold")
        R(ax,XC[0],XC[1],ZS,Z2t,"#F4F5F7",z=2,hatch="..",ec="none")
        R(ax,XC[0],XC[1],ZS,ZL,"#E5E8EC",ec=GRAPH,lw=1,z=3); T(ax,0,-8.2,"mid-landing Y 2.58 (below)",6.5,bbox=B)
        for k in range(N2): ax.plot([F2[0],F2[1]],[ZL+k*T_]*2,color="#707A84",lw=0.9,zorder=6)
        R(ax,F2[0],F2[1],ZL,Z2t,"none",ec=GRAPH,lw=1.2,z=6)
        ax.annotate("",xy=(1.15,Z2t-0.1),xytext=(1.15,ZL+0.2),arrowprops=dict(arrowstyle="->",color=WALL,lw=1.3),zorder=9); T(ax,1.15,-6.3,"FLIGHT 2\nUP 10 R",6.5,weight="bold",bbox=B)
        R(ax,F1[0],F1[1],ZL,Z1b,"none",ec="#9AA1AB",lw=0.8,z=4,ls=":"); T(ax,-1.15,-6.3,"open to\nflight 1\nbelow",6,color="#555",bbox=B)
        for seg in [([-1.9,0.4],[Z2t,Z2t]),([0.4,0.4],[ZL,Z2t]),([-0.4,0.4],[ZL,ZL]),([-0.4,-0.4],[ZL,Z2t])]: ax.plot(*seg,color=VIO,lw=2.5,zorder=7)
        for x in (1.86,0.44): ax.plot([x,x],[ZL,Z2t],color=AMB,lw=1.2,zorder=7)
        R(ax,XC[0],XC[1],ZS,Z2t,"none",ec=AMB,lw=1.6,z=8,ls=(0,(5,3))); T(ax,-3.9,-4.4,"SKYLIGHT STRIP\n(roof, 3.8 x 4.0 m)\nover the stair void",6.5,color="#B36A00",weight="bold",bbox=B)
        ax.plot([-2.9,-1.9],[-4.9,-5.6],color=AMB,lw=0.8)
        ax.plot([-1.2,1.2],[-9.0,-9.0],color=VIO,lw=5,zorder=9)
        T(ax,0,-9.7,"PROMENADE WINDOW Y 3.0-7.0 (at mid-landing, seen from L2) faces promenade + tram",7,weight="bold",color=VIO)
        gp=[(-1.9,-2.0),(1.9,-2.0),(1.9,-8.4),(-1.9,-8.4)]
        for x,z in [(-1.5,-1.3),(1.5,-1.3),(-1.5,-8.6),(1.5,-8.6)]: ax.add_patch(Circle((x,z),0.12,fc="white",ec=ORG,lw=1.5,zorder=10))

    if lvl=="L1":
        for (n,x0,x1,z0,z1) in M_SOL:
            fc={"lift shaft":"#C9CED6","pad W":GRN,"pad E1":GRN,"pad E2":GRN}.get(n,"#88929E" if "riser" in n else "#B9C0C9")
            R(ax,x0,x1,z0,z1,fc,ec=WALL,lw=1.0,z=6)
        T(ax,5.6,2.25,"sub-\nstation",5.5,rotation=90); T(ax,0.85,5.0,"tool wall",5.5,rotation=90); T(ax,5.1,8.65,"spares",5.5)
        T(ax,1.25,8.65,"coupler mounts",5); T(ax,1.1,2.9,"R",7,weight="bold")
        for (n,x0,x1,z0,z1) in [p_ for p_ in M_SOL if p_[0].startswith("pad")]: T(ax,(x0+x1)/2,(z0+z1)/2,"pad",6,color="white",weight="bold")
        R(ax,2.2,4.2,0.9,8.9,GRN,z=3,alpha=0.10); ax.annotate("",xy=(3.2,8.6),xytext=(3.2,1.2),arrowprops=dict(arrowstyle="->",color=GRN,lw=1.5,ls="--"),zorder=9)
        T(ax,3.2,5.6,"FIRE EGRESS\nLANE 2.0 m\n(kept clear)",6,color="#1F6B3E",weight="bold",bbox=B)
        R(ax,2.2,4.2,8.88,9.12,"white",ec=VIO,lw=2.2,z=8); R(ax,4.35,4.75,9.14,9.4,AMB,ec=WALL,lw=0.8,z=8)
        T(ax,1.6,9.6,"SERVICE DOOR 2.0 m (X 3.2) -> exterior ramp",6.5,weight="bold")
    else:
        for (n,x0,x1,z0,z1) in L2_SOL:
            fc="#C9CED6" if "shaft" in n else "#88929E" if ("riser" in n or "slot" in n) else "#E3E6EA"
            R(ax,x0,x1,z0,z1,fc,ec=WALL,lw=1.0,z=6)
        T(ax,1.1,2.9,"R",7,weight="bold"); T(ax,0.35,1.6,"ctrl",5,rotation=90,color="white"); T(ax,0.35,5.0,"wardrobe",5,rotation=90)
        T(ax,5.75,1.2,"kitchen",5.5); R(ax,2.55,3.45,0.9,7.8,VIO,z=3,alpha=0.06)
    R(ax,CAR[0],CAR[1],CAR[2],CAR[3],"none",ec=GRAPH,lw=1,z=7,ls="--"); T(ax,1.4,1.6,"BOT\nLIFT",6,weight="bold")
    R(ax,LDOOR[0],LDOOR[1],0.68,0.92,"white",ec=VIO,lw=2,z=8); R(ax,0.45,0.85,0.48,0.68,AMB,ec=WALL,lw=0.8,z=8)
    R(ax,0.8,2.0,-0.4,0.8,GRN,z=3,alpha=0.16); T(ax,1.4,-0.12,"lift landing 1.2",5.5,color="#1F6B3E")
    for x,z in gp: R(ax,x-0.09,x+0.09,z-0.18,z+0.18,GRN,ec=WALL,lw=0.6,z=10)
    ax.set_title(f"{lvl}  (Y {'0.00' if lvl=='L1' else '4.20'})",fontsize=11,weight="bold")
    ax.plot([-6.5,6.5],[9,9],color=WALL,lw=6,zorder=5); ax.set_xlim(-6.6,6.6); ax.set_ylim(-10.9,9.9); ax.set_aspect("equal"); ax.axis("off")
    R(ax,-6.4,-4.4,-10.6,-10.45,WALL,z=9); R(ax,-6.4,-5.4,-10.6,-10.45,"white",ec=WALL,lw=0.8,z=9); T(ax,-5.4,-10.25,"0    1    2 m",6)
    ax.annotate("",xy=(6.1,-9.6),xytext=(6.1,-10.6),arrowprops=dict(arrowstyle="-|>",color=WALL)); T(ax,6.1,-9.35,"+Z spinward",6)
fig.text(0.5,0.06,"Legend:  violet = glass guard 1.1 m (latched/clamped)   amber = handrail 0.9 m (both sides)   green bar = mag-lock grab point   orange ring = strap anchor   "
         "violet tint = door clear zone   green tint = exit / egress / lift landing   [orange] Bulkhead Hub / lift call panel",ha="center",fontsize=7.5)
fig.suptitle("RESIDENTIAL rev C - STAIR CORE v1.1 (assets #3 #4 #5 + #51 bot lift)  |  X -2..2, Z -9..-0.8  |  26 R x 0.1615, T 0.28, flights 1.5 m  |  v1.1 pending Jared review",fontsize=11.5,weight="bold")
fig.savefig("residential_stair_core_v1_1_plan.png",bbox_inches="tight",facecolor="white"); plt.close(fig)
# ---- SECTION PNG (longitudinal, along Z) ----
fig=plt.figure(figsize=(19,9.5),dpi=150); ax=fig.add_axes([0.05,0.08,0.66,0.84])
R(ax,-10.2,1.8,-0.35,0,"#B9C0C9"); R(ax,-9.1,-8.9,0,ROOF+0.3,"#C9CED6",ec=WALL,lw=1.2)
R(ax,-9.1,-8.9,0,DOOR_H,"white",ec=VIO,lw=1.5,z=4); T(ax,-9.55,1.15,"EXIT\n2.6 W\n2.3 H",6.5,weight="bold")
R(ax,-9.12,-8.88,3.0,7.0,"#E9E3FF",ec=VIO,lw=2,z=4); T(ax,-9.6,5.0,"promenade\nwindow\nY 3.0-7.0",6.5,color=VIO,weight="bold")
R(ax,ZS,ZL,YL-SLAB_L,YL,GRAPH,z=5); R(ax,Z2t,1.8,RISE-SLAB2,RISE,GRAPH,z=5); R(ax,-8.9,1.8,ROOF,ROOF+0.3,GRAPH,z=5)
R(ax,ZS,Z2t,ROOF,ROOF+0.3,"#FFE2B8",ec=AMB,lw=1.5,z=6); T(ax,(ZS+Z2t)/2,ROOF+0.75,"SKYLIGHT STRIP (asset #5) over stair void, 3.8 x 4.0 m",7.5,color="#B36A00",weight="bold")
for x in (-8.3,-7.3,-6.3): ax.annotate("",xy=(x+0.3,YL+0.4),xytext=(x,ROOF-0.1),arrowprops=dict(arrowstyle="->",color=AMB,alpha=0.5))
p1=[(Z1b,0)]
for i in range(1,N1):
    z0=Z1b-(i-1)*T_; p1+=[(z0,i*R_),(z0-T_,i*R_)]
p1+=[(ZL,N1*R_)]
ax.add_patch(Polygon(p1+[(ZL,YL-SLAB_L),(Z1b-0.5,0.0)],closed=True,fc="#9AA1AB",ec=WALL,lw=1.2,zorder=4))
p2=[(ZL,YL)]
for j in range(1,N2):
    z0=ZL+(j-1)*T_; p2+=[(z0,YL+j*R_),(z0+T_,YL+j*R_)]
p2+=[(Z2t,RISE)]
ax.plot([p[0] for p in p2],[p[1] for p in p2],color=VIO,lw=1.4,ls="--",zorder=5)
ax.plot([ZL,Z2t],[YL-SLAB_L,RISE-SLAB_L-R_],color=VIO,lw=1,ls="--",zorder=5)
ax.plot([Z1b,ZL],[RAIL,YL+RAIL],color=AMB,lw=2,zorder=6); ax.plot([ZL,Z2t],[YL+RAIL,RISE+RAIL],color=AMB,lw=1.5,ls="--",zorder=6)
ax.plot([Z1b,ZL],[HR,YL+HR],color=GRN,lw=1.2,ls=":",zorder=6); ax.plot([ZL,Z2t],[YL+HR,RISE+HR],color=GRN,lw=1.2,ls=":",zorder=6)
for z,y in [(Z2t,RISE),(ZL,YL)]: ax.plot([z,z],[y,y+GUARD],color=VIO,lw=3,zorder=7)
ax.plot([Z2t-0.05]*2,[RISE,RISE+GUARD],color=VIO,lw=3)
R(ax,-8.7,-8.5,0,YL-SLAB_L,"none"); ax.annotate("",xy=(-8.0,YL-SLAB_L),xytext=(-8.0,0),arrowprops=dict(arrowstyle="<->",color=GRN))
T(ax,-7.75,1.2,"vestibule\nhead 2.33",6.5,color="#1F6B3E",ha="left",bbox=B)
ax.annotate("",xy=(-1.5,RISE-SLAB2),xytext=(-1.5,0),arrowprops=dict(arrowstyle="<->",color=GRN)); T(ax,-1.3,1.6,"under L2 landing\nhead 3.90",6.5,color="#1F6B3E",ha="left",bbox=B)
T(ax,-6.3,0.45,"FLIGHT 1 (west, cut)  UP 16 R\nclosed below: store + strap locker",7,weight="bold",bbox=B)
T(ax,-3.3,5.65,"FLIGHT 2 (east, beyond)  UP 10 R",7,color=VIO,weight="bold",bbox=B); ax.annotate("",xy=(-5.6,4.1),xytext=(-4.2,5.5),arrowprops=dict(arrowstyle="->",color=VIO,lw=0.8))
T(ax,-8.05,YL+0.75,"MID-LANDING Y 2.58\n1.5 m deep",6.5,weight="bold",bbox=B)
T(ax,-1.6,RISE+0.35,"L2 LANDING Y 4.20 (4.1 m deep)",7,weight="bold",bbox=B)
T(ax,-2.3,3.3,"green dots: 2.1 m headroom\nline above nosings",6.5,color="#1F6B3E",ha="left",bbox=B)
T(ax,-1.2,6.3,"guards 1.1 m (violet)\nhandrails 0.9 m (amber), both sides",6.5,color=VIO,bbox=B)
T(ax,0.6,-0.65,"corridor (open, no door)",6.5,color="#555")
T(ax,-9.0,-0.65,"Z -9",6.5); T(ax,ZN,-0.65,"Z -0.8",6.5)
curv=("CURVATURE: the core spans Z -9..-0.8 at R 185.5 m. Floor rise across it is only "
      f"{185.5*(1-math.cos(9/185.5))-185.5*(1-math.cos(0.8/185.5)):.2f} m and local 'down' turns {math.degrees(8.2/185.5):.1f} deg end to end,\n"
      "so it is negligible for the rigid slab (hidden by the exterior plinth planters). Pitch reads +-1.4 deg vs the building centre.\n"
      "Climbing toward the axis gives a small Coriolis side push (2wv, about 0.02 g at 0.5 m/s), so there are handrails on both sides.")
T(ax,-4.2,7.55,curv,6.8,color="#333",bbox=dict(fc="#F7F8FA",ec=GRAPH,lw=0.6,pad=4))
ax.set_xlim(-10.3,1.9); ax.set_ylim(-1.0,9.9); ax.set_aspect("equal")
ax.set_xlabel("Z (m)   <- antispinward / Sector-4 promenade          corridor ->",fontsize=8); ax.set_ylabel("Y (m, up = toward axis)",fontsize=8)
for s_ in ("top","right"): ax.spines[s_].set_visible(False)
ax.set_title("STAIR CORE v1.1 - LONGITUDINAL SECTION along Z (X = -1.15 cut through flight 1, flight 2 beyond)  |  v1.1",fontsize=11,weight="bold")

ia=fig.add_axes([0.76,0.10,0.22,0.80])
R(ia,-1.2,0.7,-0.35,0,"#B9C0C9"); R(ia,0.7,0.9,0,ROOF,"#C9CED6",ec=WALL,lw=0.8); R(ia,2.3,2.4,0,6.6,"#C9CED6",ec=WALL,lw=0.8)
R(ia,-1.2,0.7,RISE-SLAB2,RISE,GRAPH); R(ia,2.4,3.6,RISE-SLAB2,RISE,GRAPH); R(ia,0.9,2.3,6.5,6.6,GRAPH); R(ia,-1.2,3.6,ROOF,ROOF+0.3,GRAPH)
R(ia,2.4,3.4,0,ROOF,"#88929E",ec=WALL,lw=0.8); T(ia,2.9,7.6,"RISER\n(re-aligned,\nstacks)",6,color="white",weight="bold")
for y0,lab in ((0,"L1"),(RISE,"L2")):
    R(ia,0.7,0.9,y0,y0+1.3,"white",ec=VIO,lw=1.5,z=5); T(ia,-0.6,y0+0.65,f"{lab} door\n1.0 x 1.3\n+ call panel",6,color=VIO)
R(ia,1.0,2.2,0.05,1.45,"none",ec=GRAPH,lw=1.5,z=4); R(ia,1.0,2.2,RISE+0.05,RISE+1.45,"none",ec=GRAPH,lw=1,ls="--",z=4)
ia.add_patch(Rectangle((1.2,0.1),0.78,1.03,fc=AMB,alpha=0.5,zorder=5)); T(ia,1.6,0.62,"Sprocket\n1.03",5.5)
ia.annotate("",xy=(1.6,RISE+0.1),xytext=(1.6,1.6),arrowprops=dict(arrowstyle="<->",color=GRN)); T(ia,1.6,2.9,"travel\n4.2 m",6,color="#1F6B3E",bbox=B)
T(ia,1.6,7.2,"shaft cap Y 6.6\n(MRL, ctrl in\n202 slot)",6); T(ia,-0.25,-0.75,"corridor",6,color="#555"); T(ia,1.6,-0.75,"shaft",6,color="#555")
ia.set_xlim(-1.3,3.7); ia.set_ylim(-1.0,9.4); ia.set_aspect("equal"); ia.set_xticks([0.8,2.4]); ia.set_xticklabels(["Z 0.8","Z 2.4"],fontsize=6); ia.tick_params(labelsize=6)
for s_ in ("top","right"): ia.spines[s_].set_visible(False)
ia.set_title("INSET: bot lift section along Z at X 1.4\n(not in the stair cut)",fontsize=8,weight="bold")
fig.savefig("residential_stair_core_v1_1_section.png",bbox_inches="tight",facecolor="white"); plt.close(fig)
