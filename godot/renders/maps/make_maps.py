import math, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Wedge, Circle, FancyArrow, Patch
from matplotlib.lines import Line2D
OUT="godot/renders/maps/"
BG="#0e1117"; FG="#e6e6e6"
plt.rcParams.update({"figure.facecolor":BG,"axes.facecolor":BG,"text.color":FG,"axes.labelcolor":FG,"xtick.color":FG,"ytick.color":FG,"axes.edgecolor":"#555","font.size":10})
names=["The Long Window","Meridian Science Quarter","Cascade Biosphere (Valley B)","Civic Commons","Spin Street Residential (Valley A)","The Green (Recreation)","Lantern Row Residential","Terrace Farms","Foundry Reach (Valley C)","Signal & Cargo Yards"]
cols=["#7fd6ff","#8a6cd8","#3fa36b","#e8e8f0","#e0a040","#6fd36f","#d9604c","#a8c34a","#c77d2a","#5a7fa8"]
seam=lambda k:18+36*k   # S k|k+1 ; S9|0 = 342
rings=[0,200,400,600,800]; rname=["Fore Ring","Ring 25","Mid Ring","Ring 75","Aft Ring"]
# ---------- 1 unrolled
fig,ax=plt.subplots(figsize=(18,10.5),dpi=100)
for k in range(10):
    lo=36*k-18
    ax.add_patch(Rectangle((0,lo),800,36,fc=cols[k],alpha=0.30 if k else 0.45,ec="none",hatch="//" if k==0 else None))
    ax.text(400 if k!=4 else 560,36*k+6,f"{k} · {names[k]}",ha="center",va="center",fontsize=12,weight="bold",color=cols[k] if k!=3 else "#ffffff")
    ax.text(400 if k!=4 else 560,36*k-4,f"θ {36*k}°",ha="center",fontsize=8,color="#aaa")
for k in range(10):
    y=seam(k); ax.plot([0,800],[y,y],color="#00e5ff",lw=2.2)
    lab=f"S{k}|{(k+1)%10}"+(" (+freight)" if k in (7,8) else "")
    ax.text(803,y,lab,va="center",fontsize=8,color="#00e5ff")
for x,n in zip(rings,rname):
    ax.plot([x,x],[-18,342],color="#ff4fd8",lw=2.5)
    ax.text(x,346,f"{n}\n{x} m",ha="center",va="bottom",fontsize=9,color="#ff4fd8")
ax.scatter([x for x in rings for k in range(10)],[seam(k) for x in rings for k in range(10)],s=55,c="#ffffff",edgecolors="#ff4fd8",zorder=5)
ax.scatter([x for x in (100,300,500,700) for k in range(10)],[seam(k) for x in (100,300,500,700) for k in range(10)],s=22,c="#00e5ff",marker="s",zorder=5)
hubs=[("1 Fore Hub",0,4),("2 Aft Hub",800,8),("3 Prism West",400,0),("4 Prism East",400,9),("5 Commons Central",400,3),("6 Green Central",400,5),("7 Cascade Junction",200,2),("8 Foundry Junction",600,7)]
for n,x,k in hubs:
    y=seam(k); ax.scatter([x],[y],s=260,marker="*",c="#ffd84a",edgecolors="k",zorder=6)
    ax.annotate(n,(x,y),xytext=(x+(8 if x<800 else -8),y+5),fontsize=9,weight="bold",color="#ffd84a",ha="left" if x<800 else "right",
        bbox=dict(fc=BG,ec="none",alpha=0.7,pad=1),zorder=7)
# preface: x 86..114, z 27..45 -> theta 144+z/200 rad
t=lambda z:144+math.degrees(z/200)
ax.add_patch(Rectangle((86,t(27)),28,t(45)-t(27),fc="#ff3030",ec="white",lw=1.2,zorder=6))
ax.annotate("Preface area (P-1)\nx 86–114 m",(100,t(36)),xytext=(130,150),color="#ff6060",fontsize=9,weight="bold",arrowprops=dict(arrowstyle="->",color="#ff6060"))
for x,n,ha in ((0,"FORE CAP\n(separate map)\npassenger dock",'right'),(800,"AFT CAP\n(separate map)\nstarport + cargo",'left')):
    ax.add_patch(Rectangle((x-40 if x==0 else x+38,-18),2 if 0 else 0,0))
    ax.text(-12 if x==0 else 860,162,n,ha=ha,va="center",fontsize=10,color="#bbbbbb",weight="bold",bbox=dict(fc="#222833",ec="#888",ls="--"))
ax.set_xlim(-120,900); ax.set_ylim(-30,375)
ax.set_xlabel("Axial distance from Fore cap seam (m)"); ax.set_ylabel("Angle around axis θ (degrees, unrolled; strip 0 wraps −18°…+18°)")
ax.set_xticks(range(0,801,100)); ax.set_yticks([seam(k) for k in range(-1,10)])
ax.set_title("Cylinder Hab-7 — Unrolled Master Plan (10 × 36° strips, 800 m) — source: design/cylinder_master_plan.md @124a1bb",fontsize=14,pad=30)
# scale bar + axis arrow
ax.plot([20,120],[-24,-24],color="w",lw=4); ax.text(70,-21,"100 m",ha="center",fontsize=9)
ax.annotate("",xy=(320,-24),xytext=(180,-24),arrowprops=dict(arrowstyle="->",color="w",lw=2)); ax.text(250,-21,"Spin axis → Aft",ha="center",fontsize=9)
ax.text(560,-25,"Arc width per strip = 125.66 m at R 200 (angle axis not to scale with length)",fontsize=8,color="#aaa")
leg=[Line2D([],[],color="#00e5ff",lw=2.2,label="Seam maglev line (elevated 4.6–6.1 m), 10"),Line2D([],[],color="#ff4fd8",lw=2.5,label="Ring line, 5 (glazed bridge over window)"),
 Line2D([],[],marker="o",ls="",mfc="w",mec="#ff4fd8",ms=8,label="Transfer station (50)"),Line2D([],[],marker="s",ls="",color="#00e5ff",ms=6,label="Local stop (40, 100 m spacing)"),
 Line2D([],[],marker="*",ls="",color="#ffd84a",ms=14,label="Major hub (8, suggested)"),Patch(fc="#7fd6ff",alpha=.45,hatch="//",label="Observation window (glass)"),Patch(fc="#ff3030",label="Preface area")]
ax.legend(handles=leg,loc="upper left",bbox_to_anchor=(1.0,1.0),facecolor="#1a1f29",edgecolor="#555",fontsize=9)
fig.tight_layout(); fig.savefig(OUT+"cylinder_unrolled.png",facecolor=BG); plt.close(fig)
# ---------- 2 cross section
fig,ax=plt.subplots(figsize=(18,13),dpi=100); ax.set_aspect("equal"); ax.axis("off")
# math angle: theta=0 (window) at bottom? Put window at top for drama: display angle = 90 - theta... use theta measured from bottom ("down"=strip under viewer) - keep simple: theta 0 at top, clockwise.
d=lambda th:90-th
for k in range(10):
    w=Wedge((0,0),200,d(36*k+18),d(36*k-18),width=200 if k else 200,fc=cols[k],alpha=0.30 if k else 0.18,ec="#444",lw=1,hatch="//" if k==0 else None)
    ax.add_patch(w)
    a=math.radians(d(36*k)); r=150
    ax.text(r*math.cos(a),r*math.sin(a),f"{k}\n{names[k]}\nθ {36*k}°",ha="center",va="center",fontsize=10,weight="bold",color=cols[k] if k!=3 else "w",
        rotation=0)
    ax.add_patch(Wedge((0,0),205,d(36*k+18),d(36*k-18),width=8,fc=cols[k] if k else "#bff0ff",ec="none",alpha=0.9))
for k in range(10):
    a=math.radians(d(seam(k))); ax.plot([0,195*math.cos(a)],[0,195*math.sin(a)],color="#555",lw=.8,ls=":")
    ax.scatter([195*math.cos(a)],[195*math.sin(a)],s=60,c="#00e5ff",zorder=5)
    ax.text(222*math.cos(a),222*math.sin(a),f"S{k}|{(k+1)%10}",ha="center",va="center",fontsize=9,color="#00e5ff")
ax.add_patch(Circle((0,0),200,fill=False,ec="#ff4fd8",lw=1.5,ls="--"))
ax.scatter([0],[0],c="#ffd84a",s=80,zorder=6); ax.text(0,-12,"Axial spine (R 0)\nSun-Core + zero-G tube",ha="center",va="top",fontsize=9,color="#ffd84a")
a=math.radians(d(144+math.degrees(36/200))); ax.scatter([200*math.cos(a)],[200*math.sin(a)],marker="s",c="#ff3030",s=90,zorder=7)
ax.annotate("Preface area (strip 4, z +36 m)",(200*math.cos(a),200*math.sin(a)),xytext=(150,-250),color="#ff6060",fontsize=10,arrowprops=dict(arrowstyle="->",color="#ff6060"))
ax.text(0,232,"GLASS — 36° full-length observation window",ha="center",fontsize=11,color="#bff0ff",weight="bold")
ax.text(-300,-250,"Static cylinder: does not rotate in-engine.\nStars / sun / planets orbit outside (orbit rate TBD in plan).\nDown = toward hull floor (R 200 m).",fontsize=9,color="#aaa")
ax.plot([-280,-180],[255,255],color="w",lw=4); ax.text(-230,262,"100 m",ha="center")
ax.text(-290,230,"View looking along the axis (Fore → Aft)\nθ clockwise from window. Seam lines = cyan (elevated maglev).\nDashed magenta = ring maglev path (follows floor)",fontsize=9,color="#aaa")
ax.set_xlim(-310,310); ax.set_ylim(-280,290)
ax.set_title("Cylinder Hab-7 — Cross-section across the axis (R 200 m, Ø 400 m, 10 × 36°)",fontsize=15)
fig.tight_layout(); fig.savefig(OUT+"cylinder_cross_section.png",facecolor=BG); plt.close(fig)
# ---------- 3 strip 4
fig,axs=plt.subplots(2,1,figsize=(18,12),dpi=100)
H=62.83
blocks=[("B-Fore",0,50,-H,H,"#3a3f4a"),("B1 Preface",50,150,6,H,"#5a3030"),("B2 Housing Row A",50,200,-H,-6,"#4a3e2a"),("B3 Courtyard Homes",150,200,6,H,"#3e4a2a"),
 ("B4 Ring 25 Commons",200,250,-H,H,"#2a3e4a"),("B5 Housing Rows B/C",250,400,-H,H,"#4a3e2a"),("B6 Mid Ring Civic Gate",400,450,-H,H,"#3a3a55"),
 ("B7 Housing Rows D/E",450,600,-H,H,"#4a3e2a"),("B8 Ring 75 Commons",600,650,-H,H,"#2a3e4a"),("B9 Aft Housing",650,800,-H,H,"#4a3e2a")]
HA=[(53,73),(77,97),(103,123),(127,147),(153,171),(175,193)]
GRID=[(a-50,b-50) for a,b in HA]  # v2 44 m block grid (H-B..F positions inferred from H-A pattern)
bld=[("P-1",86,114,27,45)]+[(f"H-A{i+1}",a,b,-42,-24) for i,(a,b) in enumerate(HA)]+[("C-1..4",155,195,10,40),("M-1",210,240,-20,20),("K-1",303,343,-44.5,-32.5),("G-1",407,437,-44.5,-30.5),("R-1",610,640,-40,-20)]
for lab,x0 in (("H-B/C",255),("H-D/E",455),("H-F",655)):
    for i,(a,b) in enumerate(GRID):
        for s in (1,-1): bld.append((lab if i==0 else "",x0-5+a,x0-5+b,24 if s>0 else -42,42 if s>0 else -24))
for ax,(xa,xb) in zip(axs,((0,400),(400,800))):
    ax.set_aspect("equal")
    for n,x0,x1,z0,z1,c in blocks:
        if x1<=xa or x0>=xb: continue
        ax.add_patch(Rectangle((x0,z0),x1-x0,z1-z0,fc=c,ec="none",alpha=0.8))
        ax.text(max(x0,xa)+2,(z0+z1)/2 if (z1-z0)<100 else -60,n,fontsize=7.5,color="#cfcfcf",va="center",clip_on=True)
    ax.add_patch(Rectangle((0,-6),800,12,fc="#c9b37a",alpha=.9))
    ax.text(xa+10,0,"SPINE WALK 12 m",fontsize=8,va="center",color="k",weight="bold")
    for z0,n in ((45,"Canal Promenade 9.5 m"),(-54.5,"Civic Promenade 9.5 m")):
        ax.add_patch(Rectangle((0,z0),800,9.5,fc="#9c8c66",alpha=.8)); ax.text(xa+52 if xa==0 else xa+10,z0+4.75,n,fontsize=7.5,va="center",color="k")
    for x in range(50,800,50):
        if x%200: ax.add_patch(Rectangle((x-3,-H),6,2*H,fc="#9c8c66",alpha=.7))
    for x in rings:
        ax.add_patch(Rectangle((x-6,-H),12,2*H,fc="#ff4fd8",alpha=.35)); ax.text(x,H+9,f"{rname[rings.index(x)]} x {x}",ha="center",fontsize=8,color="#ff4fd8")
    for n,x0,x1,z0,z1 in bld:
        ax.add_patch(Rectangle((x0,z0),x1-x0,z1-z0,fc="#d8d8e0" if n!="P-1" else "#ff3030",ec="k",lw=.6,alpha=.95))
        if n: ax.text((x0+x1)/2,(z0+z1)/2,n,ha="center",va="center",fontsize=6.5,color="k",weight="bold",clip_on=True)
    ax.add_patch(Rectangle((40,51.4),490,2.9,fc="#2f8cff",zorder=4)); ax.add_patch(Rectangle((518,45),27,9.3,fc="#2f8cff",ec="w",lw=.6,zorder=4)); ax.add_patch(Rectangle((527,54.3),6,8.5,fc="#2f8cff",alpha=.5,zorder=4))
    for zz,n in ((-H,"Seam S3|4 maglev (to Civic, strip 3)"),(H,"Seam S4|5 maglev (to The Green, strip 5)")):
        ax.plot([0,800],[zz,zz],color="#00e5ff",lw=3); ax.text(xb-2,zz+(3 if zz>0 else -5),n,ha="right",fontsize=8,color="#00e5ff")
    for x in (100,300,500,700):
        for zz in (H,-H):
            if x==100 and zz>0: ax.add_patch(Rectangle((85,57.93),30,3.5,fc="#00e5ff",ec="w",lw=.6,zorder=6))
            else: ax.add_patch(Rectangle((x-15,zz-3 if zz>0 else zz),30,3,fc="none",ec="#00e5ff",lw=1,ls="--"))
    for x in rings:
        for zz in (H,-H): ax.scatter([x],[zz],s=60,c="w",edgecolors="#ff4fd8",zorder=6)
    for x0 in (85,107): ax.add_patch(Rectangle((x0,54.3),7,5,fc="#ffd84a",ec="k",lw=.5,zorder=6))
    ax.add_patch(Rectangle((117.4,45.6),4.2,3.1,fc="#ff9de2",ec="k",zorder=7))
    ax.set_xlim(xa-5,xb+5); ax.set_ylim(-H-14,H+16)
    ax.set_xticks(range(xa,xb+1,50)); ax.set_yticks([-62.83,-45,-6,6,45,62.83]); ax.tick_params(labelsize=7)
    ax.set_ylabel("z arc (m)")
a0,a1=axs
a0.text(100,22,"PREFACE — PENDING JARED REVIEW",ha="center",fontsize=7.5,color="#ff6060",weight="bold",zorder=8)
a0.text(250,52.8,"CANAL — PENDING JARED REVIEW",ha="center",va="center",fontsize=6.5,color="w",weight="bold",zorder=8)
a0.annotate("Memorial (#29)",(119.5,48.7),xytext=(135,75),fontsize=8,color="#ff9de2",arrowprops=dict(arrowstyle="->",color="#ff9de2"),annotation_clip=False)
a0.annotate("x100 stop (cantilevered, deck +5.40) + 2 towers 7×5 m",(100,58),xytext=(30,72),fontsize=8,color="#ffd84a",arrowprops=dict(arrowstyle="->",color="#ffd84a"),annotation_clip=False)
a0.annotate("Fore Hub",(0,H),xytext=(8,74),fontsize=9,weight="bold",color="#ffd84a",arrowprops=dict(arrowstyle="->",color="#ffd84a"),annotation_clip=False)
a0.text(40,-72,"Aqueduct supply culvert at x 40 (routing schematic / TBD)",fontsize=7.5,color="#2f8cff")
a1.annotate("Commons Central (x400, S3|4)",(400,-H),xytext=(410,-74),fontsize=9,weight="bold",color="#ffd84a",arrowprops=dict(arrowstyle="->",color="#ffd84a"),annotation_clip=False)
a1.annotate("Canal/Headwater Basin + culvert x 530 — PENDING JARED REVIEW",(530,58),xytext=(545,76),fontsize=8,color="#2f8cff",arrowprops=dict(arrowstyle="->",color="#2f8cff"),annotation_clip=False)
a1.set_xlabel("x axial (m) — Fore Ring 0 → Aft Ring 800")
a1.plot([700,750],[-73,-73],color="w",lw=4); a1.text(725,-71,"50 m",ha="center",fontsize=8)
a1.annotate("",xy=(690,-73),xytext=(610,-73),arrowprops=dict(arrowstyle="->",color="w",lw=2)); a1.text(612,-71,"axis → Aft",fontsize=8)
leg=[Patch(fc="#c9b37a",label="Spine Walk 12 m"),Patch(fc="#9c8c66",label="Promenades 9.5 m / cross walks 6 m"),Patch(fc="#ff4fd8",alpha=.35,label="Ring cross-walk 12 m (under ring line)"),
 Patch(fc="#d8d8e0",ec="k",label="Building footprint (v2)"),Patch(fc="#ff3030",label="Preface P-1 (pending Jared review)"),Patch(fc="#2f8cff",label="Canal + Basin (pending Jared review)"),
 Line2D([],[],color="#00e5ff",lw=3,label="Seam maglev (rail +5.26 m)"),Patch(fc="#00e5ff",label="x100 platform (as drafted)"),Patch(fc="none",ec="#00e5ff",ls="--",label="Other local-stop platforms (side/position TBD)"),
 Line2D([],[],marker="o",ls="",mfc="w",mec="#ff4fd8",ms=8,label="Transfer station"),Patch(fc="#ffd84a",label="Stair/lift tower"),Patch(fc="#ff9de2",label="Memorial")]
fig.legend(handles=leg,loc="lower center",ncol=6,facecolor="#1a1f29",edgecolor="#555",fontsize=8.5)
fig.suptitle("Strip 4 — Spin Street Residential — Plan v2 DRAFT (125.66 m × 800 m, unrolled; source design/strip4_plan.md @b2f4aad)\nRook blockers resolved in v2. H-B…H-F slots inferred from the v2 44 m grid rule (doc lists row ranges only). Crossings: option A (inset). Preface spot + canal PENDING JARED REVIEW. No building height cap.",fontsize=12)
ins=fig.add_axes([0.80,0.30,0.19,0.16]); ins.set_facecolor("#1a1f29"); ins.axhline(0,color="#888",lw=1)
ins.plot([-150,150],[5.26,5.26],color="#00e5ff",lw=2); ins.plot([-150,150],[10.2,10.2],color="#ff4fd8",lw=2)
ins.text(-145,11,"ring rail +10.2 (deck +10.34)",fontsize=6.5,color="#ff4fd8"); ins.text(-145,6,"seam rail +5.26 (deck +5.40)",fontsize=6.5,color="#00e5ff")
ins.set_xlim(-150,150); ins.set_ylim(-1,15); ins.tick_params(labelsize=6); ins.set_ylabel("m",fontsize=6)
ins.set_title("Crossings (Q3 = option A): rings permanently up,\ntwo-level transfers, no grades",fontsize=7.5)
fig.subplots_adjust(left=0.05,right=0.78,top=0.91,bottom=0.1,hspace=0.25); fig.savefig(OUT+"strip4_plan.png",facecolor=BG); plt.close(fig)
