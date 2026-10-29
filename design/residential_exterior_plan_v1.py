# Residential rev C exterior + 20 m city ring, Cylinder Hab-7. DESIGN ONLY (plan diagrams).
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
# ---------------- PLAN ----------------
fig,ax=plt.subplots(figsize=(15,13),dpi=150)
R_(ax,-47,47,-42,42,"#FAFAFB")
for (x0,x1,z0,z1,lab) in [(-47,-25,-42,42,""),(25,47,-42,42,""),(-25,25,24,42,""),(-25,25,-42,-29,"")]: R_(ax,x0,x1,z0,z1,PLOT)
# streets running spinward (Z) at X +-17..23 and service lane (X) at Z 11.5..15.5, tram along X at Z -19..-22
R_(ax,-23,-17,-42,42,STREET); R_(ax,17,23,-42,42,STREET)
R_(ax,-23,23,11.5,15.5,STREET); R_(ax,-47,47,-22.5,-18.5,STREET)
for z in (-21.6,-20.9,-20.1,-19.4): ax.plot([-47,47],[z,z],color="#6A737D",lw=0.8,zorder=2)
# promenade + plaza (south, Sector-4), sidewalks
R_(ax,-47,47,-18.5,-9,PAVE); R_(ax,-8,8,-18.5,-9,"#F7EBDC")
for x in range(-8,9,2): ax.plot([x,x],[-18.5,-9],color="#E3CFB4",lw=0.6,zorder=2)
R_(ax,-17,-14,-9,11.5,PAVE); R_(ax,14,17,-9,11.5,PAVE); R_(ax,-14,14,9,11.5,PAVE)
R_(ax,-47,47,-26,-22.5,PAVE); R_(ax,-47,47,-42,-26,WATER); T(ax,0,-33.5,"VALLEY A CANAL ESPLANADE (context)",8,color="#3B5966")
# neighbor plots / building edges
for (x0,x1,z0,z1,lab) in [(-43,-26,-8,22,"PLOT W  - R-6 residential\nFACADE ONLY (edge X -26)"),(26,46,-8,22,"PLOT E  - clinic / market\nFACADE ONLY (edge X +26)"),
                          (2,16,18,40,"PLOT N-E  - workshop row\nFACADE ONLY (edge Z +18)"),(-43,-26,-17,-10,"PLOT SW kiosks (facade)")]:
    R_(ax,x0,x1,z0,z1,"#E3E6EA",ec=GRAPH,lw=1.6,z=3,hatch="//"); T(ax,(x0+x1)/2,(z0+z1)/2,lab,7.5,weight="bold",bbox=dict(fc="white",ec="none",pad=1.5))
R_(ax,26,46,-17,-10,"#E3E6EA",ec=GRAPH,lw=1.6,z=3,hatch="//"); T(ax,36,-13.5,"PLOT SE depot (facade)",7.5,weight="bold",bbox=dict(fc="white",ec="none",pad=1.5))
# hydro / green
R_(ax,-21,-5,18,28,"#CFEBD8",ec=GRN,lw=1.5,z=3); T(ax,-13,25.5,"HYDRO CO-OP BEDS\n(community, patched liners)",7.5,color="#1F6B3E",weight="bold")
for z in (19.5,21.5,23.5): R_(ax,-20,-6,z,z+0.9,GRN,z=4,alpha=0.7)
R_(ax,-13,-9,21.5,22.4,AMB,z=5)
for z0 in (-7,-2,3): R_(ax,-16.6,-15,z0,z0+4,GRN,z=4,alpha=0.75)
R_(ax,-16.6,-15,3,7,AMB,z=5,alpha=0.8); T(ax,-15.8,-8.3,"hydro\nplanters",6.5,color="#1F6B3E")
R_(ax,-30,-26,-26,-22.5,"#CFEBD8",ec=GRN,lw=1,z=3)
# building
R_(ax,-14,14,-9,9,"#EEF1F5",ec=WALL,lw=5,z=6)
T(ax,0,3.2,"RESIDENTIAL  rev C\n28 x 18 x 8.8 m  (L1 + L2)",10,weight="bold")
T(ax,0,-1.2,"10 units: 8 apts + Laundry + Maintenance",7.5,color="#555")
for x0,x1,z in [(-13,-5,9),(-4,0,9),(6.8,13.2,9),(-13,-3,-9),(3,13,-9)]:
    ax.plot([x0,x1],[z,z],color=VIO,lw=3.2,zorder=7)
for z0,z1,x in [(-8,8,-14),(-8,8,14)]: ax.plot([x,x],[z0,z1],color=VIO,lw=3.2,zorder=7)
ax.plot([-1.2,1.2],[-9.35,-9.35],color=VIO,lw=3.2,ls=(0,(1,1)),zorder=7)
# plinth masking (approved): planters + ramps along +-Z walls (no curvature along X, so none on +-X walls)
for zc,(x0s) in ((-9.55,(-13.6,-11.2,-8.8,-6.4,-4.0,3.0,5.4,7.8,10.2,12.6)),(9.55,(-13.6,-11.2,-8.8,-6.4,-4.0,-1.6,6.6,9.0,11.4))):
    for x0 in x0s: R_(ax,x0,x0+2.0,zc-0.45,zc+0.45,"#9ED9B1",ec=GRN,lw=0.8,z=7)
for x0,x1,zc in ((-1.8,1.8,-9.55),(0.9,5.6,9.55)): R_(ax,x0,x1,zc-0.45,zc+0.45,"#F4F5F7",ec=GRAPH,lw=0.8,z=7,hatch="---")
T(ax,-8.5,10.8,"planters + ramps hide 0.22 m step (both Z walls)",6.3,color="#1F6B3E")
# doors
R_(ax,-1.3,1.3,-9.25,-8.75,"white",ec=VIO,lw=2.2,z=8); R_(ax,1.45,1.85,-9.6,-9.25,AMB,ec=WALL,lw=1,z=8)
T(ax,0,-7.6,"SECTOR-4 EXIT  2.6 m\n(only resident entrance)",7.5,weight="bold")
T(ax,-4.6,-10.7,"L2 promenade window above",6.5,color=VIO)
R_(ax,2.2,4.2,8.75,9.25,"white",ec=VIO,lw=2.2,z=8); R_(ax,4.35,4.75,9.25,9.6,AMB,ec=WALL,lw=1,z=8)
T(ax,3.2,7.4,"SERVICE DOOR 2.0 m + Bulkhead Hub\n(Maintenance; Sprocket + 2nd fire exit)",7,color=WALL,weight="bold")
R_(ax,1,6,9.3,11.4,"#FCE3D3",ec=ORG,lw=1,z=4); R_(ax,1.4,2.6,9.8,11.0,GRN,ec=WALL,lw=0.8,z=5); T(ax,4.6,10.4,"apron",6.5,color=ORG)
# plaza / promenade labels, tram stop, shrine
T(ax,-28,-13.6,"",7)
T(ax,0,-12.6,"SECTOR-4 PLAZA\n16 x 9.5 m",8,weight="bold")
T(ax,-31,-11.5,"",7)
T(ax,-34,-20.5,"TRAM  (axial line)",7.5,weight="bold",color="white")
R_(ax,6,20,-18.5,-16.6,"#DADDE2",ec=GRAPH,lw=1,z=4); R_(ax,10,16,-18.3,-17.0,GRAPH,z=5)
T(ax,13,-15.6,"TRAM STOP (LIVE) - lived-in shelter",7,weight="bold")
ax.add_patch(Circle((15.1,-6.0),0.8,fc="#F2E6FF",ec=VIO,lw=1.5,zorder=6)); T(ax,15.1,-3.9,"memorial\nnook",6.5,color=VIO,weight="bold",bbox=dict(fc="white",ec="none",pad=0.6))
T(ax,-31,-16,"",7)
T(ax,-24.5,-12.4,"SECTOR-4 PROMENADE\n(Valley A frontage)",8,weight="bold",ha="left")
T(ax,-20,2.5,"SPIN ST W",7.5,weight="bold",rotation=90); T(ax,20,2.5,"SPIN ST E",7.5,weight="bold",rotation=90)
T(ax,-9,13.5,"SERVICE LANE  4 m  (Sprocket + carts)",7.5,weight="bold")
# routes: resident desire path, Sprocket route
ax.plot([13,6,0.6],[-17.4,-13,-9.4],color=AMB,lw=2.2,ls=(0,(4,2)),zorder=9); T(ax,10.2,-13.6,"worn desire path",6.5,color="#B36A00",ha="left")
ax.plot([-31,-10,-1],[-15.5,-15.5,-9.4],color=AMB,lw=1.2,ls=(0,(4,2)),zorder=9,alpha=0.8)
ax.plot([20,20,10,3.2,3.2],[42,13.5,13.5,13.5,9.4],color=GRN,lw=2.4,ls=(0,(2,1.5)),zorder=9)
ax.plot([3.2,16.6,16.6,1.9],[13.5,13.5,-11,-11],color=GRN,lw=1.4,ls=(0,(2,1.5)),zorder=9,alpha=0.85)
T(ax,24.0,16.3,"Sprocket route from\nnorth grid depot",7,color="#1F6B3E",weight="bold",ha="left",bbox=dict(fc="white",ec="none",pad=1))
# lighting poles
poles=[(x,-18.2) for x in range(-40,41,10)]+[(x,15.8) for x in (-21,-9,3,15)]+[(-17.4,z) for z in (-30,-4,8,30)]+[(17.4,z) for z in (-30,-4,8,30)]+[(-7.6,-9.6),(7.6,-9.6)]
for x,z in poles: ax.add_patch(Circle((x,z),1.1,fc=AMB,alpha=0.18,zorder=8)); ax.add_patch(Circle((x,z),0.35,fc=AMB,ec=WALL,lw=0.6,zorder=9))
# rise contours (curvature: rise depends only on Z)
for h in (0.5,1.0,2.0):
    s=srise(h)
    for zz in (s,-s): ax.plot([-47,-43.3],[zz,zz],color=VIO,lw=0.9,ls=":",zorder=10)
    T(ax,-45.2,s+0.8,f"+{h:g} m",6,color=VIO); T(ax,-45.2,-s+0.8,f"+{h:g} m",6,color=VIO)
# 20 m study boundary + 30 m window-card ring
ax.add_patch(Rectangle((-34,-29),68,58,fill=False,ec=GRAPH,lw=2,ls="--",zorder=11)); T(ax,-33.6,28.0,"20 m study boundary",7.5,weight="bold",ha="left",bbox=dict(fc="white",ec="none",pad=1))
r=30; pts=[]
for cx,cz,a0 in [(14,9,0),(-14,9,90),(-14,-9,180),(14,-9,270)]:
    pts+= [(cx+r*math.cos(math.radians(a)),cz+r*math.sin(math.radians(a))) for a in range(a0,a0+91,5)]
ax.add_patch(Polygon(pts,closed=True,fill=False,ec=VIO,lw=1.8,ls=(0,(6,3)),zorder=11))
T(ax,-12,36.6,"30 m WINDOW-CARD RING: inside = real interiors; whole 20 m block is inside",7.5,color=VIO,weight="bold",bbox=dict(fc="white",ec="none",pad=1))
# compass + scale + legend
cx,cz=38,-37
for dx,dz,lab in [(0,4,"SPINWARD +Z"),(0,-4,"ANTISPIN -Z"),(4,0,"AFT +X"),(-4,0,"FORE -X")]:
    ax.annotate("",xy=(cx+dx,cz+dz),xytext=(cx,cz),arrowprops=dict(arrowstyle="-|>",color=WALL,lw=1.4),zorder=12)
T(ax,cx,cz+5,"SPINWARD +Z",7,weight="bold"); T(ax,cx,cz-4.9,"ANTISPINWARD -Z",7,weight="bold")
T(ax,cx-5.2,cz+1.3,"FORE",6.5); T(ax,cx+5.4,cz+1.3,"AFT",6.5); T(ax,cx,cz-2.0,"",6)
T(ax,cx+0.3,cz-7.0,"X = AXIAL (flat)   up = to axis",6.5,color="#555")
R_(ax,-45,-35,-40,-39.4,WALL,z=12); R_(ax,-45,-40,-40,-39.4,"white",ec=WALL,lw=1,z=12); T(ax,-40,-41.0,"0        5        10 m",7)
lg=[("white",VIO,"force-field door + Bulkhead Hub"),("#9ED9B1",GRN,"masking planter / ramp"),(VIO,VIO,"unit windows (outer walls)"),(GRN,GRN,"Sprocket route / pad"),(AMB,AMB,"light pole / worn path"),("#E3E6EA",GRAPH,"neighbor plot edge")]
for i,(fc,ec,lab) in enumerate(lg):
    R_(ax,-31,-29.6,-34.9-i*1.3,-34.2-i*1.3,fc,ec=ec,lw=1,z=12); T(ax,-29,-34.55-i*1.3,lab,6.8,ha="left")
R_(ax,-32,-6,-42,-34.4+1.0,"white",ec=GRAPH,lw=0.8,z=11,alpha=0.85)
ax.set_title("RESIDENTIAL rev C - EXTERIOR + 20 m CITY RING (plan, L1) - APPROVED 2026-10-29   |   Cylinder Hab-7, Valley A, Sector-4   |   floor R 185.5 m",fontsize=11.5,weight="bold",color=WALL)
ax.set_xlim(-47,47); ax.set_ylim(-42,42); ax.set_aspect("equal"); ax.axis("off")
fig.savefig("residential_exterior_plan_v1_plan.png",bbox_inches="tight",facecolor="white"); plt.close(fig)
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
