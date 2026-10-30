# Extends residential_floorplan_rev_c.py with furniture/fixture layouts (Vance, rev C)
import math
from matplotlib.patches import Rectangle
C={"bed":"#C9D3E0","kit":"#F2D7A8","bath":"#A9D6E5","sto":"#CBBFA5","work":"#D9C2E8","live":"#D6E8C9","mach":"#B8C2CC"}
def F(x0,z0,x1,z1,lab,k): return (x0,z0,x1,z1,lab,k)
def furnish(ax,items,paths):
    for x0,z0,x1,z1,lab,k in items:
        if k=="ghost":  # floor decal only (dust outline / clamp marks): drawn dashed, not an obstacle in QC
            ax.add_patch(Rectangle((x0,z0),x1-x0,z1-z0,fc="none",ec="#7A828E",lw=0.9,ls=(0,(3,2)),zorder=4))
            ax.text((x0+x1)/2,(z0+z1)/2,lab,ha="center",va="center",fontsize=5,style="italic",color="#5A626E",zorder=7); continue
        ax.add_patch(Rectangle((x0,z0),x1-x0,z1-z0,fc=C[k],ec="#1A1E24",lw=0.8,zorder=4))
        rot=90 if (x1-x0)<0.7 and (z1-z0)>(x1-x0) else 0
        ax.text((x0+x1)/2,(z0+z1)/2,lab.replace("-\n","").replace("\n"," ") if rot else lab,ha="center",va="center",fontsize=5.2,zorder=7,rotation=rot)
    for p in paths:
        xs,zs=zip(*p); ax.plot(xs,zs,ls=(0,(2,2)),color="#3FAF6A",lw=1.6,zorder=3)
def mx(items): return [(-x1,z0,-x0,z1,l,k) for x0,z0,x1,z1,l,k in items]
def mp(ps): return [[(-x,z) for x,z in p] for p in ps]
def SW(bed2,bunk,bin_,window,sofa,table):  # south-west unit template (103/203), mirrored for 104/204
    g=lambda l,k: (l[1:],"ghost") if l and l[0]=="~" else (l,k)
    it=[F(-13.9,0.2,-10.2,0.7,"coat & storage closet","sto"),
            F(-13.9,-3.2,-11.7,-0.9,"bath pod\nshower WC sink","bath"),
            F(-9.5,-1.5,-6,-0.9,"kitchen counter + hob","kit"),
            F(-9,-3.3,-7.4,-2.4,table,"live"),
            F(-11,-5.7,-8.5,-4.8,sofa,"live"),
            F(-13.9,-8.9,-11.9,-7.3,bed2,"bed"),
            F(-11.2,-8.9,-10.3,-7.0,*g(bunk,"bed")),
            F(-9.8,-8.9,-8.6,-8.3,bin_,"sto"),
            F(-7,-8.9,-3,-8.5,*g(window,"work")),
            F(-2.6,-7,-2.1,-4,"wardrobe","sto")]
    it[4]=F(-11,-5.7,-8.5,-4.8,*g(sofa,"live"))
    return [f for f in it if f[4] is not None]
SWP=[[(-4.5,-0.8),(-4.5,-7.8)],[(-4.5,-3.9),(-11.6,-3.9),(-11.6,-6.6)]]
L1=([F(-13.9,0.9,-11.7,3.1,"bath pod\nshower WC sink","bath"),F(-11.4,0.9,-8,1.5,"kitchen counter","kit"),
     F(-10.5,3,-9.3,3.8,"table","live"),F(-11,5,-8.5,5.9,"sofa","live"),F(-5.1,4,-4.6,7,"ward-\nrobe","sto"),
     F(-13.9,7.3,-11.9,8.9,"double bed","bed"),F(-8,8.3,-5.5,8.9,"tool wall + work mat","work"),
     # Laundry
     F(-4.4,2.6,-3.6,3.4,"W/D","mach"),F(-4.4,3.5,-3.6,4.3,"W/D","mach"),F(-4.4,4.4,-3.6,5.2,"W/D","mach"),F(-4.4,5.3,-3.6,6.1,"W/D","mach"),
     F(-0.2,3,0.4,6.5,"folding\ncounter","work"),F(-4.4,8.4,0.4,8.9,"resident lockers","sto"),F(-3.5,6.6,-2.3,7.0,"bench","live"),
     # Maintenance
     F(5.3,1,5.9,3.5,"sub-\nstation","mach"),F(0.6,3.6,1.1,6.4,"tool\nwall","work"),F(4.3,8.4,5.9,8.9,"spares","sto"),
     F(0.6,8.4,1.9,8.9,"coupler arm\nmounts","mach"),
     # 102 (K4 elder)
     F(12.1,0.9,13.9,3.1,"bath pod\nshower WC sink","bath"),F(9,0.9,11.8,1.5,"kitchen counter","kit"),F(9.6,3,10.8,3.8,"tea table","live"),
     F(9,6,10,7,"reading\nchair","live"),F(10.3,6,11,6.7,"plants","live"),F(6.1,5,6.6,7.5,"suit\nhook +\nstorage","sto"),F(12,7.3,13.9,8.9,"double bed","bed")]
    +SW("double bed","kids\nbunk","toy bin","~planter clamp marks + toy drift","sofa","table for 4")
    +mx(SW("bed","~shelf\nghost","tele-\nscope","desk + data slates (window)","~dust outline\n(ex lab bench)","table"))+[F(7.4,-8.9,8.4,-8.3,"lab\ncrate","sto")]+[F(10.2,0.2,13.9,0.7,"coat & storage closet","sto")][0:0],
    [[(-6.5,0.8),(-6.5,7.5)],[(-6.5,4.4),(-11.5,4.4),(-11.5,7)],[(-1.8,0.8),(-1.8,8.0)],[(3.2,0.8),(3.2,8.6)],[(8,0.8),(8,8.4)],[(8,4.4),(11.5,4.4),(11.5,7)]]+SWP+mp(SWP))
L2=([F(-13.9,0.9,-11.7,3.1,"bath pod\nshower WC sink","bath"),F(-11.4,0.9,-7.6,1.5,"kitchen counter","kit"),F(-10,3,-8.8,3.8,"table","live"),
     F(-13.9,6.4,-10.2,8.9,"ex-bench\noutline","ghost"),F(-13.4,4.2,-12.4,5.2,"reading\nchair","live"),F(-9.5,8.4,-6,8.9,"tool + cable wall","work"),
     F(-7,5,-4.5,5.9,"sofa","live"),F(-0.6,4,-0.1,6.5,"ward-\nrobe","sto"),F(-2.1,7.3,-0.1,8.9,"double bed","bed"),
     # 202 (K2 family)
     F(12.1,0.9,13.9,3.1,"bath pod\nshower WC sink","bath"),F(5,0.9,9,1.5,"kitchen counter","kit"),F(6,3,7.6,3.8,"table for 4","live"),
     F(5,5.5,7.5,6.4,"sofa","live"),F(0.1,3.5,0.6,6.5,"ward-\nrobe","sto"),F(12,7.3,13.9,8.9,"double bed","bed"),
     F(10,7,10.9,8.9,"kids\nbunk","bed"),F(2.7,8.5,5,8.9,"planter clamp marks","ghost"),F(1.3,7.9,2.5,8.4,"2 chairs\n(window)","live")]
    +SW("bed","Cycler\nmodel","plants","reading nook (window)","armchair + sofa","tea table")
    +mx(SW("bed",None,"stuck\nSweep","work desk (window)","sofa","table"))+[F(10.3,-8.9,11.2,-8.2,"lab\ncrate","sto"),F(10.3,-8.1,11.2,-7.0,"bench\noutline","ghost"),F(12.6,-6.4,13.6,-5.4,"arm-\nchair","live")],
    [[(-3,0.8),(-3,7)],[(-3,4.4),(-8,4.4),(-8,7)],[(-8,4.4),(-11.4,4.4)],[(3,0.8),(3,7.8)],[(3,4.4),(10.5,4.4),(10.5,6.6)]]+SWP+mp(SWP))
src=open("residential_floorplan_rev_c.py").read()
src=src.replace("residential_floorplan_rev_c_L","residential_roomlayout_rev_c_L").replace("Residential rev C","Room layouts rev C (dashed green = ≥0.9 m walking path)")
src=src.replace("def ex1(ax):\n","def ex1(ax):\n    furnish(ax,*L1)\n").replace("def ex2(ax):\n","def ex2(ax):\n    furnish(ax,*L2)\n")
src=src.replace('    ax.text(-11,7.6,"ex-2C workshop nook",fontsize=7,ha="center",style="italic")\n',"")
for a,b in [('-9.25,5,U','-9.25,7.3,U'),('-2,5,U','-2,7.4,U'),('S103,-8,-5,U','S103,-6.6,-6.9,U'),('S104,8,-5,U','S104,6.6,-6.9,U'),('-7,4.5,"#E3EDF2"','-5,3.0,"#E3EDF2"'),('R(0,14,0.8,9),7,5,U','R(0,14,0.8,9),9.6,5.8,U')]:
    src=src.replace(a,b)
exec(src)

# ---- QC (reuses the stair-core approach): furniture/fixture overlaps, 0.9 m paths, door zones, lift landing, egress lane ----
def ov(a,b): return a[1]<b[2]-1e-9 and b[1]<a[2]-1e-9 and a[3]<b[4]-1e-9 and b[3]<a[4]-1e-9
def rects(items,objs): return [(f[4].split("\n")[0],min(f[0],f[2]),max(f[0],f[2]),min(f[1],f[3]),max(f[1],f[3])) for f in items if f[5]!="ghost"]+list(objs)
def dzones(doors):
    out=[]
    for x,z,w,_ in doors:
        if z>=8.9: out.append((f"door@{x},{z} in",x-w/2,x+w/2,z-0.9,z-0.1))
        elif z<=-8.9: out.append((f"door@{x},{z} in",x-w/2,x+w/2,z+0.1,z+1.5))
        else:
            sg=1 if z>0 else -1
            out+= [(f"door@{x},{z} unit",x-w/2,x+w/2,min(z+sg*0.1,z+sg*1.0),max(z+sg*0.1,z+sg*1.0)),(f"door@{x},{z} corr",x-w/2,x+w/2,min(z,z-sg*0.9),max(z,z-sg*0.9))]
    return out
D1=[(-6.5,0.8,1.4,""),(-2,0.8,1.4,""),(3.2,0.8,2.0,""),(8,0.8,1.4,""),(-4.5,-0.8,1.4,""),(4.5,-0.8,1.4,""),(0,-9,2.6,""),(3.2,9,2.0,"")]
D2=[(-3,0.8,1.4,""),(3,0.8,1.4,""),(-4.5,-0.8,1.4,""),(4.5,-0.8,1.4,"")]
QC=[]
for lvl,(items,paths),objs,doors in (("L1",L1,OBJ1,D1),("L2",L2,OBJ2,D2)):
    rs=rects(items,objs)
    QC.append((f"{lvl} furniture/fixture overlaps",[(a[0],b[0]) for i,a in enumerate(rs) for b in rs[i+1:] if ov(a,b)]))
    zones=dzones(doors)+[("lift landing",)+LANDING]+([("egress lane",)+LANE] if lvl=="L1" else [])
    QC.append((f"{lvl} items in door zones / lift landing / egress lane",[(r[0],z[0]) for r in rs for z in zones if ov(r,z)]))
    QC.append((f"{lvl} lift landing vs door zones",[z[0] for z in dzones(doors) if ov(("l",)+LANDING,z)]))
    hits=[]
    for pth in paths:
        pts=[]
        for (ax_,az),(bx,bz) in zip(pth,pth[1:]):
            n=max(2,int(math.hypot(bx-ax_,bz-az)/0.1)); pts+=[(ax_+(bx-ax_)*k/n,az+(bz-az)*k/n) for k in range(n+1)]
        ex,ez=pth[-1]; pts=[q for q in pts if math.hypot(q[0]-ex,q[1]-ez)>0.5]
        for r in rs:
            if any(r[1]-0.45<x<r[2]+0.45 and r[3]-0.45<z<r[4]+0.45 for x,z in pts): hits.append((pth[0],r[0]))
    QC.append((f"{lvl} 0.9 m walk paths blocked",hits))
for q in QC: print("QC:",q)
bad=[k for k,v in QC if v]; assert not bad, ("QC failed",bad)
import shutil  # rev C.2 approval copies (main PNGs are overwritten too)
for l in ("L1","L2"): shutil.copy(f"residential_roomlayout_rev_c_{l}.png",f"residential_roomlayout_rev_c_v3_{l}.png")
