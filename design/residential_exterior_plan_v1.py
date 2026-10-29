# Residential rev C exterior + 20 m city ring (v1.1 QC: plan -> residential_exterior_plan_v1_1_plan.png; v1 PNG kept), Cylinder Hab-7. DESIGN ONLY (plan diagrams).
# Axis mapping: X = axial (fore -X / aft +X), Z = circumferential (+Z spinward, -Z antispinward),
# up = toward spin axis, down = radially outward. Walking floor R_HULL_FLOOR = 185.5 m.
import math, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch
R=185.5; WALL="#1A1E24"; GRAPH="#282E38"; PEARL="#D8DEE6"; AMB="#FF9500"; GRN="#3FAF6A"; VIO="#7B5CFF"; ORG="#D95B26"
WATER="#BFD9E0"; PAVE="#E9ECF0"; STREET="#B9C0C9"; PLOT="#F3F4F6"
rise=lambda s: R*(1-math.cos(s/R)); ang=lambda s: math.degrees(s/R)
srise=lambda h: R*math.acos(1-h/R)
NUM={s:(rise(s),ang(s)) for s in (9,20,29,39)}
for s,(r,a) in NUM.items(): print(f"s={s} m rise={r:.3f} m angle={a:.2f} deg")
print("edge->+20m rise", rise(20)); print("eye 1.7 m meets floor at", srise(1.7)); print("contours",[srise(h) for h in (0.5,1,2)])
def R_(ax,x0,x1,z0,z1,fc,ec="none",lw=0,z=1,**k): ax.add_patch(Rectangle((x0,z0),x1-x0,z1-z0,fc=fc,ec=ec,lw=lw,zorder=z,**k))
def T(ax,x,z,s,fs=7.5,**k): ax.text(x,z,s,ha=k.pop("ha","center"),va=k.pop("va","center"),fontsize=fs,color=k.pop("color",WALL),zorder=20,**k)
# ---------------- PLAN v1.1 (data-driven geometry + QC checks) ----------------
Zg=[("promenade",-47,47,-18.5,-9,"walk"),("plaza",-8,8,-18.5,-9,"walk"),("platform",9,21,-18.5,-15.5,"walk"),
("tram band",-47,47,-22.5,-18.5,"road"),("kerb walk",-47,47,-26,-22.5,"walk"),("canal",-47,47,-42,-26,"water"),
("W sidewalk",-17,-14,-9,11.8,"walk"),("E sidewalk",14,17,-9,11.8,"walk"),("N sidewalk",-14,14,9,11.8,"walk"),
("service lane",-17,17,11.8,15.8,"road"),("N far sidewalk",-17,17,15.8,18,"walk"),("co-op yard",-17,2,18,42,"walk"),
("hydro co-op",-14,-2,18.5,27,"green"),("NE sidewalk",15,17,18,42,"walk"),("Plot N-E",2,15,18,40,"plot"),
("Spin St W",-23,-17,-9,42,"road"),("Spin St E",17,23,-9,42,"road"),("W outer sidewalk",-26,-23,-9,42,"walk"),("E outer sidewalk",23,26,-9,42,"walk"),
("Plot W",-44,-26,-2,22,"plot"),("Plot SW",-44,-26,-9,-3,"plot"),("Plot E",26,44,-2,22,"plot"),("Plot SE",26,44,-9,-3,"plot"),("building",-14,14,-9,9,"bldg")]
CHILD={"plaza":"promenade","platform":"promenade","hydro co-op":"co-op yard"}
ZD={z[0]:z for z in Zg}
O=[]  # objects: (name,x0,x1,z0,z1,walkable)
for x0 in (-13.8,-11.6,-9.4,-7.2,-5.0,3.0,5.2,7.4,9.6,11.8): O.append(("planter S",x0,x0+2.0,-10.0,-9.1,False))
for x0 in (-13.8,-11.6,-9.4,-7.2,-5.0,-2.8,8.0,10.0,12.0): O.append(("planter N",x0,x0+2.0 if x0<12 else 14.0,9.1,10.0,False))
O+= [("ramp exit 1:12",-1.8,1.8,-11.65,-9.0,True),("ramp service 1:12",1.0,5.6,9.0,11.65,True),("Sprocket pad",6.4,7.6,9.1,10.3,False),
     ("tram shelter",12,18,-16.9,-15.6,False),("memorial nook",15.0,16.6,-11.8,-10.2,False)]
for z0 in (-7,-2,3): O.append(("hydro planter W",-16.8,-15.4,z0,z0+4,False))
for z in (19.5,21.5,23.5): O.append(("hydro bed",-13,-3,z,z+0.9,False))
POLES=[(x,-18.0) for x in (-40,-30,-20,-10.5,8.5,22,30,40)]+[(-6,-10.8),(6,-10.8)]+[(-16.6,z) for z in (-8,2.5,10.8)]+[(16.75,z) for z in (-8,2.5,10.8)] \
     +[(x,16.2) for x in (-15,-5,5,15)]+[(-23.4,z) for z in (-5,8,20)]+[(23.4,z) for z in (-5,8,20)]+[(x,-25.6) for x in (-30,-10,10,30)]
for x,z in POLES: O.append(("pole",x-0.15,x+0.15,z-0.15,z+0.15,False))
def ov(a,b): return a[1]<b[2]-1e-9 and b[1]<a[2]-1e-9 and a[3]<b[4]-1e-9 and b[3]<a[4]-1e-9
def kind_at(x,z):
    ks=[k for n,x0,x1,z0,z1,k in Zg if x0<=x<=x1 and z0<=z<=z1]; return ks
def inside(o,kinds):
    n=8; return all(any(k in kinds for k in kind_at(o[1]+(o[2]-o[1])*(i+.5)/n,o[3]+(o[4]-o[3])*(j+.5)/n)) for i in range(n) for j in range(n))
QC=[]
bad=[(a[0],b[0]) for i,a in enumerate(Zg) for b in Zg[i+1:] if ov(a,b) and CHILD.get(a[0])!=b[0] and CHILD.get(b[0])!=a[0]]
QC.append(("ground-zone overlaps",bad))
bad=[(a[0],b[0]) for i,a in enumerate(O) for b in O[i+1:] if ov(a,b)]; QC.append(("object-object overlaps",bad))
bad=[o[0]+f"@{o[1]:.1f},{o[3]:.1f}" for o in O if not inside(o,("green",) if o[0]=="hydro bed" else ("walk",))]; QC.append(("objects outside walk/green zones",bad))
bad=[o for o in O if o[0]=="tram shelter" and not (ZD["platform"][1]<=o[1] and o[2]<=ZD["platform"][2] and ZD["platform"][3]<=o[3] and o[4]<=ZD["platform"][4])]
QC.append(("shelter not on platform",bad)); QC.append(("shelter clearance to track (m)",round(O[[o[0] for o in O].index("tram shelter")][3]-ZD["tram band"][4],2)))
CLR=[("exit approach 2.6 m",-1.3,1.3,-18.5,-11.65),("W sidewalk clear",-15.4,-14,-9,11.8),("E sidewalk clear",14,16.6,-9,11.8),
     ("N sidewalk clear",-14,14,10.3,11.8),("platform front",12,18,-18.5,-16.9),("hydro aisle 1",-13,-3,20.4,21.5),("hydro aisle 2",-13,-3,22.4,23.5),("kerb walk clear",-47,47,-25.4,-22.5)]
for c in CLR:
    w=min(c[2]-c[1],c[4]-c[3]); hit=[o[0] for o in O if not o[5] and ov(("c",)+c[1:],o)]
    QC.append((f"clear corridor {c[0]} width {w:.2f} m (>=0.9)",[] if (w>=0.9 and not hit) else hit+([f"w={w}"] if w<0.9 else [])))
DESIRE=[(9.5,-17.0),(1.3,-12.6),(0.0,-11.65)]; PROM=[(-34,-14.0),(-8,-14.0),(-1.3,-12.2)]; SPR=[(20,42),(20,13.8),(3.3,13.8),(3.3,9.0)]
def path_hits(P,half,kinds):
    hits=set()
    for (ax_,az),(bx,bz) in zip(P,P[1:]):
        for k in range(41):
            x=ax_+(bx-ax_)*k/40; z=az+(bz-az)*k/40
            for o in O:
                if not o[5] and o[1]-half<x<o[2]+half and o[3]-half<z<o[4]+half: hits.add(o[0])
            if not any(q in kinds for q in kind_at(x,z)): hits.add(f"off-walk@{x:.1f},{z:.1f}")
    return sorted(hits)
QC.append(("desire path tram->exit blocked by",path_hits(DESIRE,0.45,("walk",))))
QC.append(("promenade path ->exit blocked by",path_hits(PROM,0.45,("walk",))))
QC.append(("Sprocket route blocked by",path_hits(SPR,0.45,("walk","road"))))
pz=[(x,z,kind_at(x,z)) for x,z in POLES]; QC.append(("poles in road/tram/lane",[(x,z) for x,z,k in pz if "road" in k]))
QC.append(("off-map items",[o[0] for o in O if o[1]<-47 or o[2]>47 or o[3]<-42 or o[4]>42]))
dist=lambda x,z: math.hypot(max(abs(x)-14,0),max(abs(z)-9,0))
ring=[]
for cx,cz,a0 in [(14,9,0),(-14,9,90),(-14,-9,180),(14,-9,270)]:
    ring+=[(cx+30*math.cos(math.radians(a)),cz+30*math.sin(math.radians(a))) for a in range(a0,a0+91,2)]
QC.append(("ring max |offset-30| (m)",round(max(abs(dist(x,z)-30) for x,z in ring),6)))
QC.append(("study-box corner (34,29) offset from footprint (m)",round(dist(34,29),2)))
for q in QC: print("QC:",q)
assert all((not v) if isinstance(v,list) else True for _,v in QC), "QC failed"
print("poles",len(POLES),"planters",sum(o[0].startswith("planter") for o in O))
COL={"walk":PAVE,"road":STREET,"water":WATER,"green":"#CFEBD8","plot":"#E3E6EA","bldg":"#EEF1F5"}
fig,ax=plt.subplots(figsize=(15,15),dpi=150)
R_(ax,-47,47,-42,42,"#FAFAFB")
for n,x0,x1,z0,z1,k in Zg:
    if k=="bldg": continue
    fc={"plaza":"#F7EBDC","platform":"#DADDE2"}.get(n,COL[k])
    R_(ax,x0,x1,z0,z1,fc,ec=(GRAPH if k=="plot" else GRN if k=="green" else "none"),lw=(1.6 if k in("plot","green") else 0),z=3 if n in CHILD else 2,hatch="//" if k=="plot" else None)
for x in range(-8,9,2): ax.plot([x,x],[-18.5,-9],color="#E3CFB4",lw=0.6,zorder=3)
for z in (-21.6,-20.9,-20.1,-19.4): ax.plot([-47,47],[z,z],color="#6A737D",lw=0.8,zorder=3)
for x0 in (-20.5,19.5): R_(ax,x0,x0+1,-9.35,-8.65,"none")
R_(ax,-14,14,-9,9,"#EEF1F5",ec=WALL,lw=5,z=6)
for x0,x1,z in [(-13,-5,9),(-4,0,9),(9,13.2,9),(-13,-3,-9),(3,13,-9)]: ax.plot([x0,x1],[z,z],color=VIO,lw=3.2,zorder=7)
for x in (-14,14): ax.plot([x,x],[-8,8],color=VIO,lw=3.2,zorder=7)
ax.plot([-1.2,1.2],[-9.35,-9.35],color=VIO,lw=3.2,ls=(0,(1,1)),zorder=7)
for o in O:
    n,x0,x1,z0,z1,_=o
    if n=="pole": continue
    if n.startswith("planter") or n=="hydro planter W": R_(ax,x0,x1,z0,z1,"#9ED9B1",ec=GRN,lw=0.8,z=7)
    elif n.startswith("ramp"): R_(ax,x0,x1,z0,z1,"#F4F5F7",ec=GRAPH,lw=0.8,z=7,hatch="---")
    elif n=="Sprocket pad": R_(ax,x0,x1,z0,z1,GRN,ec=WALL,lw=0.8,z=7)
    elif n=="tram shelter": R_(ax,x0,x1,z0,z1,GRAPH,z=7)
    elif n=="memorial nook": ax.add_patch(Circle(((x0+x1)/2,(z0+z1)/2),0.8,fc="#F2E6FF",ec=VIO,lw=1.5,zorder=7))
    elif n=="hydro bed": R_(ax,x0,x1,z0,z1,GRN,z=7,alpha=0.8)
R_(ax,-9,-6,21.5,22.4,AMB,z=8); R_(ax,-16.8,-15.4,3,7,AMB,z=8,alpha=0.8)
R_(ax,-1.3,1.3,-9.25,-8.75,"white",ec=VIO,lw=2.2,z=9); R_(ax,1.45,1.85,-8.6,-8.25,AMB,ec=WALL,lw=1,z=9)
R_(ax,2.3,4.3,8.75,9.25,"white",ec=VIO,lw=2.2,z=9); R_(ax,1.85,2.25,8.25,8.6,AMB,ec=WALL,lw=1,z=9)
for P,c,lw,ls in [(DESIRE,AMB,2.2,(0,(4,2))),(PROM,AMB,1.4,(0,(4,2))),(SPR,GRN,2.4,(0,(2,1.5)))]: ax.plot([p[0] for p in P],[p[1] for p in P],color=c,lw=lw,ls=ls,zorder=10)
for x,z in POLES: ax.add_patch(Circle((x,z),1.1,fc=AMB,alpha=0.18,zorder=8)); ax.add_patch(Circle((x,z),0.35,fc=AMB,ec=WALL,lw=0.6,zorder=11))
ax.add_patch(Rectangle((-34,-29),68,58,fill=False,ec=GRAPH,lw=2,ls="--",zorder=12))
ax.add_patch(Polygon(ring,closed=True,fill=False,ec=VIO,lw=1.8,ls=(0,(6,3)),zorder=12))
B=dict(fc="white",ec="none",pad=1.2)
L=[(0,3.2,"RESIDENTIAL  rev C\n28 x 18 x 8.8 m  (L1 + L2)",10,WALL,"center"),(0,-0.9,"10 units: 8 apts + Laundry + Maintenance",7.5,"#555","center"),
 (0,-7.4,"SECTOR-4 EXIT 2.6 m (resident entrance)",7.5,WALL,"center"),(0,-5.9,"L2 promenade window above exit",6.5,VIO,"center"),
 (3.3,7.0,"SERVICE DOOR 2.0 m + Bulkhead Hub\n(Maintenance: Sprocket + 2nd fire exit)",7,WALL,"center"),
 (-7.5,11.25,"planters + 1:12 ramps mask 0.22 m step",5.8,"#1F6B3E","center"),
 (-4.6,-16.9,"SECTOR-4 PLAZA\n16 x 9.5 m",8,WALL,"center"),(-24.5,-12.2,"SECTOR-4 PROMENADE\n(Valley A frontage)",8,WALL,"left"),
 (10.3,-14.4,"worn desire path",6.5,"#B36A00","left"),(15,-17.75,"TRAM STOP (LIVE) + lived-in shelter",6.5,WALL,"center"),
 (16.9,-11.0,"memorial nook",6.5,VIO,"left"),(-34,-20.5,"TRAM (axial, live)",7.5,"white","center"),
 (-8,13.8,"SERVICE LANE 4 m (Sprocket + carts)",7.5,WALL,"center"),(-8,25.7,"HYDRO CO-OP BEDS\n(community, patched liners)",7.5,"#1F6B3E","center"),
 (-35,10,"PLOT W  R-6 residential\nFACADE ONLY  (edge X -26)",7.5,WALL,"center"),(35,10,"PLOT E  clinic / market\nFACADE ONLY  (edge X +26)",7.5,WALL,"center"),
 (8.5,29,"PLOT N-E\nworkshop row\nFACADE ONLY\n(edge Z +18)",7.5,WALL,"center"),(-35,-6,"PLOT SW kiosks (facade, Z -9..-3)",7,WALL,"center"),
 (35,-6,"PLOT SE depot (facade, Z -9..-3)",7,WALL,"center"),(0,-33.5,"VALLEY A CANAL ESPLANADE (context, railing at Z -26)",8,"#3B5966","center"),
 (24.2,36,"Sprocket route from\nnorth grid depot",7,"#1F6B3E","left"),(-33.6,27.6,"20 m study boundary",7.5,WALL,"left"),
 (-12,36.6,"30 m WINDOW-CARD RING (true offset): whole 20 m block inside",7.5,VIO,"center")]
for x,z,s_,fs,c,ha in L: T(ax,x,z,s_,fs,color=c,ha=ha,weight="bold",bbox=B if c not in("white",) else None)
T(ax,-20,2.5,"SPIN ST W",7.5,weight="bold",rotation=90); T(ax,20,2.5,"SPIN ST E",7.5,weight="bold",rotation=90)
for h in (0.5,1.0,2.0):
    s=srise(h)
    for zz in (s,-s): ax.plot([-50.5,-47.2],[zz,zz],color=VIO,lw=1,ls=":"); T(ax,-49,zz+0.9,f"+{h:g} m",6.2,color=VIO)
T(ax,-49,0,"floor\nrise\n(Z)",6.2,color=VIO)
# margin band below map: legend, scale, compass (outside map area)
lg=[("white",VIO,"force-field door"),(AMB,WALL,"Bulkhead Hub"),("#9ED9B1",GRN,"masking planter"),("#F4F5F7",GRAPH,"1:12 ramp"),(VIO,VIO,"unit windows"),
    (GRN,GRN,"Sprocket route / pad"),(AMB,AMB,"light pole / worn path"),("#E3E6EA",GRAPH,"facade-only plot")]
for i,(fc,ec,lab) in enumerate(lg):
    x=-46+(i//3)*13; z=-44.5-(i%3)*1.6; R_(ax,x,x+1.4,z-0.35,z+0.35,fc,ec=ec,lw=1,z=12); T(ax,x+2,z,lab,7,ha="left")
R_(ax,-6,4,-47.6,-47.0,WALL,z=12); R_(ax,-6,-1,-47.6,-47.0,"white",ec=WALL,lw=1,z=12); T(ax,-1,-48.6,"0          5          10 m",7)
cx,cz=30,-47.5
for dx,dz in [(0,3),(0,-3),(3,0),(-3,0)]: ax.annotate("",xy=(cx+dx,cz+dz),xytext=(cx,cz),arrowprops=dict(arrowstyle="-|>",color=WALL,lw=1.4))
T(ax,cx,cz+3.8,"SPINWARD +Z",7,weight="bold"); T(ax,cx,cz-3.8,"ANTISPINWARD -Z",7,weight="bold")
T(ax,cx-3.6,cz,"FORE -X",7,ha="right"); T(ax,cx+3.6,cz,"AFT +X",7,ha="left")
T(ax,-46,-50.0,"X = axial (flat)  |  up = toward axis, down = radially outward",6.5,color="#555",ha="left")
ax.set_title("RESIDENTIAL rev C - EXTERIOR + 20 m CITY RING (plan, L1) - v1.1 QC   |   Cylinder Hab-7, Valley A, Sector-4   |   floor R 185.5 m",fontsize=11.5,weight="bold",color=WALL)
ax.set_xlim(-51,47); ax.set_ylim(-52,42.5); ax.set_aspect("equal"); ax.axis("off")
fig.savefig("residential_exterior_plan_v1_1_plan.png",bbox_inches="tight",facecolor="white"); plt.close(fig)
# ---------------- SECTION ----------------
VE=5
fig=plt.figure(figsize=(15,9),dpi=150); ax=fig.add_axes([0.04,0.36,0.92,0.58]); ax2=fig.add_axes([0.04,0.0,0.30,0.24]); ax3=fig.add_axes([0.37,0.0,0.59,0.24])
ss=[i*0.25 for i in range(-200,201)]
X=[R*math.sin(s/R) for s in ss]; Y=[rise(s)*VE for s in ss]
ax.fill_between(X,[y-1.5 for y in Y],Y,color=PEARL); ax.plot(X,Y,color=WALL,lw=2.2,label="floor arc R 185.5 m")
ax.plot([-50,50],[0,0],color="#888",lw=1,ls="--"); T(ax,-44,-0.9,"flat tangent at building centre",7.5,color="#666",ha="left")
ax.add_patch(Rectangle((-9,0),18,8.8,fc="#EEF1F5",ec=WALL,lw=2.5,zorder=5)); ax.plot([-9,9],[4.2,4.2],color=WALL,lw=1,zorder=6)
T(ax,0,4.4,"RESIDENTIAL rev C\n(true height, not exaggerated)",8,weight="bold")
R_(ax,-9,9,-0.0,0.0,"none")
for s in (9,29,39):
    for sg in (-1,1):
        x=R*math.sin(sg*s/R); y=rise(s)*VE; ax.plot([x,x],[0,y],color=VIO,lw=1)
        ax.plot(x,y,"o",color=VIO,ms=4,zorder=7)
    T(ax,R*math.sin(s/R)+0.6,rise(s)*VE+{9:-2.2,29:0,39:1.5}[s],f"Z+{s}: +{rise(s):.2f} m, {ang(s):.1f} deg",7.2,color=VIO,ha="left" if s<39 else "right",weight="bold",bbox=dict(fc="white",ec="none",pad=0.5))
T(ax,-R*math.sin(29/R)-0.6,rise(29)*VE+2.2,"+20 m out\n(study edge)",7,color=VIO,ha="right")
T(ax,R*math.sin(9/R)+0.4,-3.4,"0.22 m step hidden by ramps + planters",6.5,color=ORG,ha="left")
# player on promenade at s=-12.5, eye line along local horizontal
sp=-12.5; th=sp/R; P=(R*math.sin(th),rise(sp)); up=(-math.sin(th),math.cos(th)); E=(P[0]+1.7*up[0],P[1]+1.7*up[1]); t=(math.cos(th),math.sin(th))
ax.plot([P[0],E[0]],[P[1]*VE,E[1]*VE],color=AMB,lw=3); ax.plot(E[0],E[1]*VE,"o",color=AMB,ms=7,zorder=8)
L=[E[0]-u*t[0] for u in range(0,30)]; ax.plot(L,[(E[1]-u*t[1])*VE for u in range(0,30)],color=AMB,lw=1.4,ls="--")
d=srise(1.7); sx=R*math.sin((sp-d)/R)
ax.annotate(f"looking antispinward, the floor reaches eye height {d:.1f} m ahead:\nbeyond this the ground is ABOVE the eye line,\nthe 'horizon' climbs upward overhead",xy=(sx,rise(sp-d)*VE),xytext=(-46,28.5),fontsize=7.5,color="#B36A00",arrowprops=dict(arrowstyle="->",color=AMB))
T(ax,E[0]+2.5,E[1]*VE+4.5,"player eye 1.7 m\n(promenade)",7.2,color="#B36A00",weight="bold")
ax.annotate("",xy=(44,26),xytext=(32,10),arrowprops=dict(arrowstyle="->",color=VIO,lw=1.5,connectionstyle="arc3,rad=0.25"))
T(ax,30.5,25,"sightline climbs with the floor\n-> far side 371 m overhead",7.2,color=VIO,ha="right")
T(ax,-46,-5.2,"ANTISPINWARD (-Z)  <- Sector-4 promenade / tram / canal",8,weight="bold",ha="left")
T(ax,46,-5.2,"service lane / hydro co-op ->  SPINWARD (+Z)",8,weight="bold",ha="right")
ax.set_xlim(-47,47); ax.set_ylim(-7,32); ax.set_title(f"DEVELOPED SECTION across spin (Z)   |   vertical exaggeration x{VE} for floor rise (building true height)   |   down = radially outward",fontsize=10.5,weight="bold")
ax.set_xlabel("arc distance from building centre along Z (m)",fontsize=8); ax.set_yticks([0,5,10]); ax.set_yticklabels(["0","+1 m","+2 m"],fontsize=7); ax.tick_params(labelsize=7)
for sp_ in ("top","right"): ax.spines[sp_].set_visible(False)
# inset: drum cross-section
ax2.add_patch(Circle((0,0),200,fill=False,ec=GRAPH,lw=1)); ax2.add_patch(Circle((0,0),R,fill=False,ec=WALL,lw=2)); ax2.plot(0,0,"x",color=AMB)
ax2.add_patch(Polygon([(-6,-R),(6,-R),(6,-R+20),(-6,-R+20)],fc=AMB,ec=WALL)); ax2.plot([0,0],[-R,R],color=VIO,lw=0.8,ls=":")
T(ax2,0,-R+48,"block",6.5,color="#B36A00"); T(ax2,0,R-30,"far side 371 m up",6.5,color=VIO); T(ax2,0,18,"spin axis",6.5)
T(ax2,130,-160,"R 185.5 floor\nR 200 hull",6.5,ha="left"); ax2.set_xlim(-215,300); ax2.set_ylim(-210,210); ax2.set_aspect("equal"); ax2.axis("off")
ax2.set_title("drum cross-section (to scale)",fontsize=8)
ax3.axis("off")
rows=[("Z from centre","rise vs centre tangent","floor tilt"),("9 m (building wall)",f"{rise(9):.2f} m",f"{ang(9):.2f} deg"),("29 m (wall +20 m)",f"{rise(29):.2f} m",f"{ang(29):.2f} deg"),("39 m (30 m card ring)",f"{rise(39):.2f} m",f"{ang(39):.2f} deg"),
      ("wall -> +20 m (own tangent)",f"{rise(20):.2f} m",f"{ang(20):.2f} deg"),("eye 1.7 m meets floor at",f"{d:.1f} m ahead",""),("AXIAL (X)","0.00 m - flat","0 deg")]
tb=ax3.table(cellText=rows[1:],colLabels=rows[0],loc="center",cellLoc="center"); tb.auto_set_font_size(False); tb.set_fontsize(8); tb.scale(1,1.25)
fig.savefig("residential_exterior_plan_v1_section.png",bbox_inches="tight",facecolor="white"); plt.close(fig)
