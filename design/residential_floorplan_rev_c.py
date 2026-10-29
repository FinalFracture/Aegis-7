import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
def R(x0,x1,z0,z1): return [(x0,z0),(x1,z0),(x1,z1),(x0,z1)]
S103=[(-14,-9),(-2,-9),(-2,-0.8),(-10,-0.8),(-10,0.8),(-14,0.8)]
S104=[(-x,z) for x,z in S103]
WALL="#1A1E24"; HUB="#FF9500"; GRN="#3FAF6A"
def draw(level,units,doors,extra,fn):
    fig,ax=plt.subplots(figsize=(14,9.6),dpi=150)
    ax.add_patch(Rectangle((-10,-0.8),20,1.6,fc="#D8DEE6",ec="none"))
    ax.text(7.5,0,"CORRIDOR 1.6 m",ha="center",va="center",fontsize=8,color="#555")
    for name,poly,lx,lz,col in units:
        ax.add_patch(Polygon(poly,closed=True,fc=col,ec=WALL,lw=3))
        ax.text(lx,lz,name,ha="center",va="center",fontsize=10,weight="bold",color=WALL,zorder=8,bbox=dict(fc=col,ec="none",pad=1) if name else None)
    ax.add_patch(Rectangle((-14,-9),28,18,fill=False,ec=WALL,lw=5))
    for x,z,w,lab in doors:
        ax.add_patch(Rectangle((x-w/2,z-0.15),w,0.3,fc="white",ec="#7B5CFF",lw=2,zorder=5))
        side=0.35 if z<0.5 and z>-1 and z>0 else -0.35
        hz = z-0.55 if z>0 else z+0.25
        if z<=-8.9: hz=z+0.25
        if z>=8.9: hz=z+0.2
        ax.add_patch(Rectangle((x+w/2+0.1,hz),0.4,0.3,fc=HUB,ec=WALL,lw=1,zorder=6))
    extra(ax)
    ax.add_patch(Rectangle((-13.5,-10.6),5,0.25,fc=WALL)); ax.add_patch(Rectangle((-13.5,-10.6),2.5,0.25,fc="white",ec=WALL))
    ax.text(-11,-11.1,"0     2.5     5 m",ha="center",fontsize=8)
    ax.add_patch(Rectangle((-4,-10.75),0.6,0.3,fc="white",ec="#7B5CFF",lw=2)); ax.text(-3.2,-10.6,"force-field door",fontsize=8,va="center")
    ax.add_patch(Rectangle((1.5,-10.75),0.4,0.3,fc=HUB,ec=WALL)); ax.text(2.1,-10.6,"Bulkhead Hub",fontsize=8,va="center")
    ax.add_patch(Rectangle((6.5,-10.75),0.3,0.3,fc=GRN,ec=WALL)); ax.text(7.0,-10.6,"Sprocket pad 1.2 m",fontsize=8,va="center")
    ax.annotate("N",xy=(13.3,10.4),xytext=(13.3,9.6),ha="center",arrowprops=dict(arrowstyle="->"),fontsize=10)
    ax.set_title(level,fontsize=13,weight="bold",color=WALL)
    ax.set_xlim(-15,15); ax.set_ylim(-11.6,10.8); ax.set_aspect("equal"); ax.axis("off")
    fig.savefig(fn,bbox_inches="tight",facecolor="white"); plt.close(fig)
# Approved stair core v1.1 + Sprocket bot lift (residential_stair_core_v1.md, APPROVED 2026-10-29)
VIO="#7B5CFF"; TT=0.28; ZL=-7.4; Z1B=-3.2; Z2T=-4.88
SHAFT=(0.6,2.2,0.8,2.4); RISER=(0.6,1.6,2.4,3.4); SLOT=(0.1,0.6,0.9,3.4); LANDING=(0.8,2.0,-0.4,0.8); LANE=(2.2,4.2,0.9,8.9)
PADS=[(0.8,2.0,6.6,7.8),(4.4,5.6,4.0,5.2),(4.4,5.6,6.6,7.8)]
OBJ1=[("lift shaft",)+SHAFT,("riser",)+RISER]+[("pad",)+p for p in PADS]+[("stair flight 1",-1.9,-0.4,ZL,Z1B)]
OBJ2=[("lift shaft",)+SHAFT,("riser chase",)+RISER,("lift controller strip",)+SLOT]
def box(ax,r,fc,ec=WALL,lw=1,z=4,**k): ax.add_patch(Rectangle((r[0],r[2]),r[1]-r[0],r[3]-r[2],fc=fc,ec=ec,lw=lw,zorder=z,**k))
def lift(ax):
    box(ax,SHAFT,"#C9CED6",lw=1.5,z=5); box(ax,(0.8,2.0,1.0,2.2),"none",lw=0.8,z=6,ls="--")
    ax.text(1.4,1.6,"BOT\nLIFT",ha="center",va="center",fontsize=6,weight="bold",zorder=7)
    ax.add_patch(Rectangle((0.9,0.65),1.0,0.3,fc="white",ec=VIO,lw=2,zorder=6))
    ax.add_patch(Rectangle((0.4,0.25),0.4,0.3,fc=HUB,ec=WALL,lw=1,zorder=6))
    box(ax,LANDING,GRN,ec="none",lw=0,z=2,alpha=0.25); ax.text(1.4,-0.6,"lift landing 1.2",ha="center",va="center",fontsize=5.5,color="#1F6B3E",zorder=7)
    box(ax,RISER,"#88929E",z=5); ax.text(1.1,2.9,"R",ha="center",va="center",fontsize=8,zorder=7)
def stairs(ax,lvl):
    if lvl=="L1":
        for k in range(16): ax.plot([-1.9,-0.4],[Z1B-k*TT]*2,color="#707A84",lw=0.9,zorder=3)
        ax.annotate("",xy=(-1.15,ZL+0.2),xytext=(-1.15,Z1B-0.1),arrowprops=dict(arrowstyle="->",color=WALL),zorder=4)
        ax.text(-1.15,-5.3,"UP\n16 R",ha="center",va="center",fontsize=6.5,weight="bold",zorder=7,bbox=dict(fc="white",ec="none",pad=0.5))
        box(ax,(0.4,1.9,ZL,Z2T),"none",lw=0.8,z=3,ls="--"); box(ax,(-1.9,1.9,-8.9,ZL),"none",lw=0.8,z=3,ls="--")
        ax.plot([-0.4,-0.4],[ZL,Z1B],color=VIO,lw=2,zorder=4)
        ax.plot([0.9,0.9],[-0.9,-7.6],color=GRN,lw=1.4,ls=(0,(2,2)),zorder=3)
        ax.text(-1.15,-2.0,"bottom\nlanding",ha="center",fontsize=6,zorder=7)
        ax.text(0,-8.2,"EXIT VESTIBULE\n(mid-landing above)",ha="center",va="center",fontsize=6.5,weight="bold",zorder=7,bbox=dict(fc="#E5E8EC",ec="none",pad=0.5))
    else:
        box(ax,(-1.9,1.9,Z2T,-0.8),"#D8DEE6",ec="none",lw=0,z=2); ax.text(0,-2.6,"L2 LANDING",ha="center",fontsize=7,weight="bold",zorder=7)
        box(ax,(-1.9,0.4,ZL,Z2T),"#F4F5F7",ec="none",lw=0,z=2,hatch=".."); ax.text(-1.15,-6.1,"void",ha="center",fontsize=6.5,color="#555",zorder=7,bbox=dict(fc="white",ec="none",pad=0.5))
        for k in range(10): ax.plot([0.4,1.9],[ZL+k*TT]*2,color="#707A84",lw=0.9,zorder=3)
        ax.annotate("",xy=(1.15,Z2T-0.1),xytext=(1.15,ZL+0.1),arrowprops=dict(arrowstyle="->",color=WALL),zorder=4)
        ax.text(1.15,-6.1,"UP\n10 R",ha="center",va="center",fontsize=6.5,weight="bold",zorder=7,bbox=dict(fc="white",ec="none",pad=0.5))
        box(ax,(-1.9,1.9,-8.9,ZL),"#E5E8EC",lw=0.8,z=3); ax.text(0,-8.15,"MID-LANDING Y 2.58",ha="center",va="center",fontsize=6.5,weight="bold",zorder=7)
        for seg in [([-1.9,0.4],[Z2T,Z2T]),([0.4,0.4],[ZL,Z2T]),([-0.4,0.4],[ZL,ZL]),([-0.4,-0.4],[ZL,Z2T])]: ax.plot(*seg,color=VIO,lw=2,zorder=5)
        ax.plot([-1.2,1.2],[-9,-9],color=VIO,lw=5,zorder=6)
U="#EEF1F5"; SV="#E5E8EC"
def ex1(ax):
    stairs(ax,"L1")
    ax.text(0,-9.6,"SECTOR-4 EXIT 2.6 m -> Promenade",ha="center",fontsize=8)
    for p_ in PADS: box(ax,p_,GRN,z=5)
    lift(ax)
    box(ax,LANE,GRN,ec="none",lw=0,z=2,alpha=0.12); ax.annotate("",xy=(3.2,8.6),xytext=(3.2,1.3),arrowprops=dict(arrowstyle="->",color=GRN,ls="--"),zorder=3)
    ax.text(3.2,6.0,"EGRESS\nLANE 2 m",ha="center",va="center",fontsize=6,color="#1F6B3E",weight="bold",zorder=7,bbox=dict(fc="white",ec="none",pad=0.5))
    ax.text(1.6,9.6,"service door 2.0 m",ha="center",fontsize=6.5)
def ex2(ax):
    stairs(ax,"L2")
    ax.text(0,-9.6,"promenade window (at the mid-landing)",ha="center",fontsize=8)
    lift(ax); box(ax,SLOT,"#5E6670",z=5); ax.text(0.35,2.15,"ctrl",ha="center",va="center",fontsize=5,color="white",rotation=90,zorder=7)
    ax.text(-11,7.6,"ex-2C workshop nook",fontsize=7,ha="center",style="italic")
draw("LEVEL 1 (Y 0.00 m) - Residential rev C",
 [("101\n77.9 m²",R(-14,-4.5,0.8,9),-9.25,5,U),("LAUNDRY\n41.0 m²",R(-4.5,0.5,0.8,9),-2,5,U),
  ("MAINT.\n42.5 m² net",R(0.5,6,0.8,9),3.3,3.2,U),("102\n65.6 m²",R(6,14,0.8,9),10,5,U),
  ("103\n104.8 m²",S103,-8,-5,U),("104\n104.8 m²",S104,8,-5,U),("",R(-2,2,-9,-0.8),0,-0.3,SV)],
 [(-6.5,0.8,1.4,""),(-2,0.8,1.4,""),(3.2,0.8,2.0,""),(8,0.8,1.4,""),(-4.5,-0.8,1.4,""),(4.5,-0.8,1.4,""),(0,-9,2.6,""),(3.2,9,2.0,"")],
 ex1,"residential_floorplan_rev_c_L1.png")
draw("LEVEL 2 (Y +4.20 m) - Residential rev C",
 [("201  PLAYER\n114.8 m²",R(-14,0,0.8,9),-7,4.5,"#E3EDF2"),("202\n109.7 m² net",R(0,14,0.8,9),7,5,U),
  ("203\n104.8 m²",S103,-8,-5,U),("204\n104.8 m²",S104,8,-5,U),("",R(-2,2,-9,-0.8),0,-0.3,SV)],
 [(-3,0.8,1.4,""),(3,0.8,1.4,""),(-4.5,-0.8,1.4,""),(4.5,-0.8,1.4,"")],
 ex2,"residential_floorplan_rev_c_L2.png")
