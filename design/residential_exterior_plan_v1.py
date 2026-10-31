# Residential rev C exterior + 20 m city ring (v1.3 placements -> residential_exterior_plan_v1_3_plan.png
# + exterior_placements_v1_3.json; v1.2 plan and section PNGs still written; v1 and v1.1 PNGs kept), Cylinder Hab-7.
# DESIGN ONLY (plan diagrams).
# Axis mapping: X = axial (fore -X / aft +X), Z = circumferential (+Z spinward, -Z antispinward),
# up = toward spin axis, down = radially outward. Walking floor R_HULL_FLOOR = 185.5 m.
# Yaw is degrees about +Y; local +Z is the asset front. Paths are next to this file (any cwd).
import math, os, json, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch
HERE = os.path.dirname(os.path.abspath(__file__))
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
# Jared: no traditional roads. Tram band -> guideway bed + walk strips. Service lane and Spin St W/E -> walk (paving #44).
Zg=[("promenade",-47,47,-18.5,-9,"walk"),("plaza",-8,8,-18.5,-9,"walk"),("platform",9,21,-18.5,-15.5,"walk"),
("guideway bed",-47,47,-21.65,-18.504,"guideway"),("guideway N strip",-47,47,-18.504,-18.5,"walk"),("guideway S walk",-47,47,-22.5,-21.65,"walk"),
("kerb walk",-47,47,-26,-22.5,"walk"),("canal",-47,47,-42,-26,"water"),
("W sidewalk",-17,-14,-9,11.8,"walk"),("E sidewalk",14,17,-9,11.8,"walk"),("N sidewalk",-14,14,9,11.8,"walk"),
("service lane",-17,17,11.8,15.8,"walk"),("N far sidewalk",-17,17,15.8,18,"walk"),("co-op yard",-17,2,18,42,"walk"),
("hydro co-op",-14,-2,18.5,27,"green"),("NE sidewalk",15,17,18,42,"walk"),("Plot N-E",2,15,18,40,"plot"),
("Spin St W",-23,-17,-9,42,"walk"),("Spin St E",17,23,-9,42,"walk"),("W outer sidewalk",-26,-23,-9,42,"walk"),("E outer sidewalk",23,26,-9,42,"walk"),
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
# v1.2 street furniture: benches 1.8 x 0.5, bins 0.5 x 0.5, bollards 0.2 x 0.2
BENCH=[(9.3,11.1,-16.05,-15.55),(18.9,20.7,-16.05,-15.55),(-36,-34.2,-17.6,-17.1),(-26,-24.2,-17.6,-17.1),(26,27.8,-17.6,-17.1),(33,34.8,-17.6,-17.1),
       (-7.9,-7.4,-17.6,-15.8),(13.0,14.8,-12.3,-11.8)]
BIN=[(11.3,11.8,-16.05,-15.55),(18.2,18.7,-16.05,-15.55),(-34.0,-33.5,-17.6,-17.1),(28.0,28.5,-17.6,-17.1),(-7.9,-7.4,-18.3,-17.8),(12.3,12.8,-12.3,-11.8)]
BROWS={"Spin St W end":([-22.0,-20.667,-19.333,-18.0],-9.4,(-23,-17)),"Spin St E end":([18.0,19.333,20.667,22.0],-9.4,(17,23)),
       "apron W":([-1.0,0.4],11.55,None),"apron E":([6.1,7.5],11.55,None)}
for b in BENCH: O.append(("bench",)+b+(False,))
for b in BIN: O.append(("bin",)+b+(False,))
for xs,z,_ in BROWS.values():
    for x in xs: O.append(("bollard",x-0.1,x+0.1,z-0.1,z+0.1,False))
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
QC.append(("shelter not on platform",bad)); QC.append(("shelter clearance to track (m)",round(O[[o[0] for o in O].index("tram shelter")][3]-ZD["guideway bed"][4],2)))
CLR=[("exit approach 2.6 m",-1.3,1.3,-18.5,-11.65),("W sidewalk clear",-15.4,-14,-9,11.8),("E sidewalk clear",14,16.6,-9,11.8),
     ("N sidewalk clear",-14,14,10.3,11.4),("platform front",9,21,-18.5,-16.9),("promenade through-walk",-47,47,-15.4,-12.5),("apron + ramp opening",0.5,6.0,9.0,11.8),("hydro aisle 1",-13,-3,20.4,21.5),("hydro aisle 2",-13,-3,22.4,23.5),("kerb walk clear",-47,47,-25.4,-22.5)]
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
QC.append(("Sprocket route blocked by",path_hits(SPR,0.45,("walk",))))  # walk only; must not enter the guideway
for n,(xs,z,ends) in BROWS.items():
    e=[x-0.1 for x in xs]; f=[x+0.1 for x in xs]; gaps=[e[i+1]-f[i] for i in range(len(xs)-1)]+([e[0]-ends[0],ends[1]-f[-1]] if ends else [])
    QC.append((f"bollard row {n} gaps {[round(g,2) for g in gaps]} (0.9..1.5 m)",[g for g in gaps if not 0.9-1e-6<=g<=1.5]))
QC.append(("apron opening for Sprocket 0.78 m (m)",round((6.1-0.1)-(0.4+0.1),2)))
pz=[(x,z,kind_at(x,z)) for x,z in POLES]; QC.append(("poles in guideway",[(x,z) for x,z,k in pz if "guideway" in k]))
QC.append(("off-map items",[o[0] for o in O if o[1]<-47 or o[2]>47 or o[3]<-42 or o[4]>42]))
dist=lambda x,z: math.hypot(max(abs(x)-14,0),max(abs(z)-9,0))
ring=[]
for cx,cz,a0 in [(14,9,0),(-14,9,90),(-14,-9,180),(14,-9,270)]:
    ring+=[(cx+30*math.cos(math.radians(a)),cz+30*math.sin(math.radians(a))) for a in range(a0,a0+91,2)]
QC.append(("ring max |offset-30| (m)",round(max(abs(dist(x,z)-30) for x,z in ring),6)))
QC.append(("study-box corner (34,29) offset from footprint (m)",round(dist(34,29),2)))
# ---------------- v1.3 placements (local AABB, pivot bottom-centre, front = local +Z) ----------------
def P(i, asset, x, y, z, rot, note=""):
    return {"id": i, "asset": asset, "x": round(float(x), 4), "y": round(float(y), 4), "z": round(float(z), 4), "rot_deg": round(float(rot), 4), "note": note}
def aabb_xz(x, z, sx, sz, rot):
    r = float(rot) % 360.0
    q = int(round(r / 90.0))
    if abs(r - q * 90.0) <= 1e-2:
        hx, hz = (sz / 2.0, sx / 2.0) if q % 2 else (sx / 2.0, sz / 2.0)
        return (x - hx, x + hx, z - hz, z + hz)
    th = math.radians(r); c, s = math.cos(th), math.sin(th); hx, hz = sx / 2.0, sz / 2.0
    xs, zs = [], []
    for lx in (-hx, hx):
        for lz in (-hz, hz):
            xs.append(x + lx * c + lz * s); zs.append(z - lx * s + lz * c)
    return (min(xs), max(xs), min(zs), max(zs))
def box_hit(a, b, eps=1e-6):
    return a[0] < b[1] - eps and b[0] < a[1] - eps and a[2] < b[3] - eps and b[2] < a[3] - eps
def aabb_gap(a, b):
    dx = max(a[0] - b[1], b[0] - a[1], 0.0); dz = max(a[2] - b[3], b[2] - a[3], 0.0)
    if dx > 0.0 or dz > 0.0: return math.hypot(dx, dz)
    return -min(min(a[1], b[1]) - max(a[0], b[0]), min(a[3], b[3]) - max(a[2], b[2]))
def in_rect(x, z, r):
    return r[0] <= x <= r[1] and r[2] <= z <= r[3]
CURB_PITCH, CURB_LEN, CURB_OFF = 1.997, 1.994, 0.304 / 2.0  # 3 mm joints; centreline half a curb outside the edge
CURB_HALF = CURB_LEN / 2.0
def curb_run(start, fixed, length, along_x, rot, note):
    n = int(math.ceil(length / CURB_PITCH - 1e-9)); out = []
    for k in range(n):
        t = start + CURB_HALF + CURB_PITCH * k
        x, z = (t, fixed) if along_x else (fixed, t)
        extra = "; last segment overhangs the run and is to be trimmed" if k == n - 1 else ""
        out.append(P(41, "ext_curb_segment.glb", x, 0, z, rot, note + extra))
    return out
shelter = P(15, "ext_tram_shelter.glb", 15, 0.297, -16.25, 180, "rot 180: open side (local +Z) faces the guideway boarding edge at -Z")
kerbs = [P(16, "ext_tram_platform_kerb.glb", x, 0, -17.55, 180, "rot 180, front face Z -18.5; 2 m steps from the west end of platform X 9..21") for x in range(10, 21, 2)]
gw_over = 9.994 / 2.0 - (47 - 45)
guides = []
for x in range(-45, 46, 10):
    note = "10 m pitch across the section; rot 0; track centre Z -19.90"
    if x in (-45, 45): note += "; end overhangs scene bounds X -47..47 by %.3f m each side (~3 m)" % gw_over
    guides.append(P(17, "ext_maglev_guideway.glb", x, 0, -20.077, 0, note))
Xc = round(15.0 + 12.306 / 2.0, 4); Xc2 = round(Xc - 12.306, 4)
bodies = [P(19, "ext_maglev_car_body.glb", Xc - 0.069, 0.06, -19.90, 0, "car 1; Xc=%.4f = 15.0+12.306/2" % Xc),
          P(19, "ext_maglev_car_body.glb", Xc2 + 0.069, 0.06, -19.90, 180, "car 2; Xc2=%.4f = Xc-12.306" % Xc2)]
mags = [P(19, "ext_maglev_magnet_module.glb", Xc - 0.30, 0.06, -19.90, 0, "car 1 magnet; Xc=%.4f" % Xc),
        P(19, "ext_maglev_magnet_module.glb", Xc2 + 0.30, 0.06, -19.90, 180, "car 2 magnet; Xc2=%.4f" % Xc2)]
curb_segs, corners = [], []
for o in O:
    if not o[0].startswith(("planter S", "planter N", "hydro planter W", "hydro bed")): continue
    nm, x0, x1, z0, z1 = o[0], o[1], o[2], o[3], o[4]
    tag = "%s (%.1f..%.1f, %.1f..%.1f)" % (nm, x0, x1, z0, z1)
    curb_segs += curb_run(x0, z0 - CURB_OFF, x1 - x0, True, 0, tag + " south")
    curb_segs += curb_run(x0, z1 + CURB_OFF, x1 - x0, True, 0, tag + " north")
    curb_segs += curb_run(z0, x0 - CURB_OFF, z1 - z0, False, 90, tag + " west")
    curb_segs += curb_run(z0, x1 + CURB_OFF, z1 - z0, False, 90, tag + " east")
    for cx, cz, lab in ((x0 - CURB_OFF, z0 - CURB_OFF, "SW"), (x1 + CURB_OFF, z0 - CURB_OFF, "SE"), (x1 + CURB_OFF, z1 + CURB_OFF, "NE"), (x0 - CURB_OFF, z1 + CURB_OFF, "NW")):
        corners.append(P(41, "ext_curb_corner.glb", cx, 0, cz, 0, tag + " outside corner " + lab))
curb_segs += curb_run(-47, -18.504 + CURB_OFF, 9 - (-47), True, 0, "guideway north X -47..9")
curb_segs += curb_run(21, -18.504 + CURB_OFF, 47 - 21, True, 0, "guideway north X 21..47")
curb_segs += curb_run(-47, -21.65 - CURB_OFF, 47 - (-47), True, 0, "guideway south X -47..47")
infill = P("infill", "ext_platform_infill.glb", 15, 0, -16.048, 0, "platform infill")
ramp = P(45, "ext_kerb_ramp.glb", 9.75, 0, -13.996, 0, "kerb ramp at the platform west end")
blockers = [aabb_xz(p["x"], p["z"], 1.994, 1.9, p["rot_deg"]) for p in kerbs]
blockers += [aabb_xz(ramp["x"], ramp["z"], 1.5, 3.0, 0), aabb_xz(infill["x"], infill["z"], 11.994, 1.096, 0)]
kept, n_skip = [], 0
for seg in curb_segs:
    if any(box_hit(aabb_xz(seg["x"], seg["z"], CURB_LEN, 0.304, seg["rot_deg"]), b) for b in blockers): n_skip += 1
    else: kept.append(seg)
curb_segs = kept
# #44 grid: corner at the platform west end (9, -18.5). +Z centres -17.5+2j; -Z centres -19.5-2j.
PLAZA_BOX = (9.0, 18.0, -25.6, -12.5)  # given slice: shelter + kerb ramp + canal-edge north face, not the full canal run
GUIDE_BED = (-47.0, 47.0, -21.65, -18.504); PLATFORM_BOX = (9.0, 21.0, -18.5, -15.5)
shelter_box = aabb_xz(shelter["x"], shelter["z"], 6.024, 1.304, shelter["rot_deg"])
ramp_box = aabb_xz(ramp["x"], ramp["z"], 1.5, 3.0, 0); infill_box = aabb_xz(infill["x"], infill["z"], 11.994, 1.096, 0)
xs_grid = [10 + 2 * i for i in range(-29, 20)]
zs_grid = [-17.5 + 2 * j for j in range(0, 31)] + [-19.5 - 2 * j for j in range(0, 8)]
BAD_KIND = {"bldg", "plot", "green", "water", "guideway"}
def solid_at(x, z):
    return any((not o[5]) and o[1] <= x <= o[2] and o[3] <= z <= o[4] for o in O)
plaza_tiles, prom_tiles = [], []
seen_plaza = set()
for x in xs_grid:
    for z in zs_grid:
        if not in_rect(x, z, PLAZA_BOX): continue
        if in_rect(x, z, GUIDE_BED) or in_rect(x, z, PLATFORM_BOX) or in_rect(x, z, shelter_box) or in_rect(x, z, ramp_box) or in_rect(x, z, infill_box): continue
        seen_plaza.add((x, z))
        plaza_tiles.append(P(44, "ext_paving_plaza.glb", x, 0, z, 0, ""))
for x in xs_grid:
    for z in zs_grid:
        if (x, z) in seen_plaza: continue
        ks = kind_at(x, z)
        if "walk" not in ks or any(k in BAD_KIND for k in ks) or solid_at(x, z): continue
        prom_tiles.append(P(44, "ext_paving_promenade.glb", x, 0, z, 0, ""))
plaza_tiles.sort(key=lambda p: (p["z"], p["x"])); prom_tiles.sort(key=lambda p: (p["z"], p["x"]))
if plaza_tiles: plaza_tiles[0]["note"] = "plaza; 2 m grid origin corner (9, -18.5); box X 9..18, Z -25.6..-12.5; not on guideway, platform, shelter, ramp or infill"
if prom_tiles: prom_tiles[0]["note"] = "promenade; 2 m grid origin corner (9, -18.5); walk zones including former Spin St / service lane; not plaza, not under a non-walkable object"
canal = [P(46, "ext_canal_edge.glb", x, 0, -25.8, 180, "rot 180; 2 m modules X -46..46") for x in range(-46, 47, 2)]
dx, dz = 0.0 - 9.75, -11.65 - (-13.996); L = math.hypot(dx, dz); yaw = math.degrees(math.atan2(dx, dz)); n_des = int(math.ceil(L / 4.0 - 1e-12))
desire = []
for k in range(n_des):
    dist = 2.0 + 4.0 * k
    desire.append(P(47, "ext_desire_path_decal.glb", 9.75 + dx / L * dist, 0.053, -13.996 + dz / L * dist, yaw, ""))
dnote = "from kerb-ramp foot (9.75, -13.996) to Sector-4 exit ramp foot (0, -11.65); L=%.3f m, n=%d, yaw=%.4f deg; the entrance at Z -9 is reached up that ramp; local +Z along the path" % (L, n_des, desire[0]["rot_deg"])
for p in desire: p["note"] = dnote
dead = P(49, "ext_ts4_dead_foliage.glb", -16.6, 0, 0, 90, "replaces middle west TS-4 (hydro planter W z0 -2, Z -2..2); rot 90, back (local -Z) to Spin St W edge X -16.8; 4 m along Z")
wear = P(49, "ext_ts4_wear_decal.glb", -16.6, 0, 0, 90, "identical transform to the dead TS-4")
refs = [P(25, "hydro_planter_tiered_exterior.glb", -16.6, 0, z, 90, "existing TS-4 reference") for z in (-5, 5)]
xw = (ZD["Spin St W"][1] + ZD["Spin St W"][2]) / 2.0; xe = (ZD["Spin St E"][1] + ZD["Spin St E"][2]) / 2.0
litter = []
for x, z, asset, tag in ((xw, -7, "ext_litter_drift_01.glb", "W 01"), (xw, -3.5, "ext_litter_drift_03.glb", "W 03"), (xw, 2, "ext_litter_drift_05.glb", "W 05"),
                         (xe, -7, "ext_litter_drift_02.glb", "E 02"), (xe, -3.5, "ext_litter_drift_04.glb", "E 04"), (xe, 2, "ext_litter_drift_03.glb", "E 03")):
    litter.append(P(50, asset, x, 0.05, z, 0, "%s; walkway centre X=(zone x0+x1)/2 = %.4f" % (tag, x)))
# Rule 12: scuffs only on the guideway module at the stop (shelter centre X 15) and one module either side. No kerb scuffs.
scuff_g = [P(51, "ext_track_scuff_guideway.glb", p["x"], p["y"], p["z"], p["rot_deg"], "identical transform to guideway module at the stop (X 15) or one module either side") for p in guides if p["x"] in (5, 15, 25)]
PLACEMENTS = [shelter] + kerbs + guides + bodies + mags + curb_segs + corners + prom_tiles + plaza_tiles + [infill, ramp] + canal + desire + [dead, wear] + refs + litter + scuff_g
kb = sorted(kerbs, key=lambda p: p["x"]); bad = [] if len(kb) == 6 else ["count %d" % len(kb)]
for a, b in zip(kb, kb[1:]):
    gap = aabb_xz(b["x"], b["z"], 1.994, 1.9, b["rot_deg"])[0] - aabb_xz(a["x"], a["z"], 1.994, 1.9, a["rot_deg"])[1]
    if gap > 0.02: bad.append(round(gap, 4))
QC.append(("kerbs contiguous with no gaps", bad))
bad = []
kerb_boxes = [aabb_xz(p["x"], p["z"], 1.994, 1.9, p["rot_deg"]) for p in kerbs]
for p in curb_segs + corners:
    sx, sz = (CURB_LEN, 0.304) if p["asset"] == "ext_curb_segment.glb" else (0.304, 0.304)
    if any(box_hit(aabb_xz(p["x"], p["z"], sx, sz, p["rot_deg"]), k) for k in kerb_boxes): bad.append((p["x"], p["z"]))
QC.append(("no curb under a kerb", bad))
bad = []
for p in litter:
    box = aabb_xz(p["x"], p["z"], 1.07, 2.97, 0)
    for o in O:
        if o[0] != "bollard": continue
        g = aabb_gap(box, (o[1], o[2], o[3], o[4]))
        if g < 0.8 - 1e-9: bad.append((p["asset"], p["x"], p["z"], round(g, 4)))
QC.append(("litter-bollard clearance >= 0.8 m", bad))
bad = [(p["x"], p["z"]) for p in desire if "walk" not in kind_at(p["x"], p["z"])]
QC.append(("desire-path segment centres in walk zones", bad))
gb = sorted((aabb_xz(p["x"], p["z"], 9.994, 3.146, p["rot_deg"]) for p in guides), key=lambda b: b[0])
bad = [] if gb and gb[0][0] <= -47 and gb[-1][1] >= 47 else ["span"]
for a, b in zip(gb, gb[1:]):
    if b[0] - a[1] > 0.02: bad.append(round(b[0] - a[1], 4))
QC.append(("guideway run covers X -47..47", bad))
QC.append(("guideway scuff modules", [] if [p["x"] for p in scuff_g] == [5, 15, 25] else [p["x"] for p in scuff_g]))
QC.append(("kerb scuffs", [p["x"] for p in PLACEMENTS if p["asset"] == "ext_track_scuff_kerb.glb"]))
for q in QC: print("QC:",q)
assert all((not v) if isinstance(v,list) else True for _,v in QC), "QC failed"
print("benches",len(BENCH),"bins",len(BIN),"bollards",sum(len(v[0]) for v in BROWS.values()),"objects",len(O),"poles",len(POLES),"planters",sum(o[0].startswith("planter") for o in O))
print("paving counts: plaza", len(plaza_tiles), "promenade", len(prom_tiles), "| curb segments", len(curb_segs), "skipped", n_skip, "corners", len(corners), "| placements", len(PLACEMENTS))
order, groups = [], {}
for p in PLACEMENTS:
    key = (p["id"], p["asset"])
    if key not in groups:
        groups[key] = []; order.append(key)
    groups[key].append(p)
print("PLACEMENT SUMMARY")
print("%-8s %-42s %5s  first transform (x, y, z, rot_deg)" % ("id", "asset", "count"))
for key in order:
    p = groups[key][0]
    print("%-8s %-42s %5d  (%s, %s, %s, %s)" % (p["id"], p["asset"], len(groups[key]), p["x"], p["y"], p["z"], p["rot_deg"]))
print("--- resolved TBD ---")
print("#15 shelter rot 180 at (15, 0.297, -16.25); open side local +Z faces guideway boarding edge -Z")
print("#16 kerb x", [p["x"] for p in kerbs], "rot 180 z -17.55")
print("#17 guideway x", [p["x"] for p in guides], "n", len(guides), "end overhang m", round(gw_over, 4))
print("#19 Xc", Xc, "Xc2", Xc2, "bodies", [(p["x"], p["rot_deg"]) for p in bodies], "magnets", [(p["x"], p["rot_deg"]) for p in mags])
print("#41 curb segments", len(curb_segs), "corners", len(corners), "skipped (overlap kerb/ramp/infill)", n_skip)
print("#44 grid origin corner (9, -18.5) pitch 2.0; plaza", len(plaza_tiles), "promenade", len(prom_tiles))
print("#46 canal x", canal[0]["x"], "..", canal[-1]["x"], "n", len(canal), "z -25.8 rot 180")
print("#47 L", round(L, 4), "n", len(desire), "yaw", desire[0]["rot_deg"], "centres", [(p["x"], p["z"]) for p in desire])
print("#49 dead foliage and wear decal (-16.6, 0, 0) rot 90; neighbour refs z", [p["z"] for p in refs])
print("#50 Spin St W centre X", round(xw, 4), "Spin St E centre X", round(xe, 4))
print("#51 guideway scuff x", [p["x"] for p in scuff_g], "kerb scuffs", 0)
resolved = {"15_rot_deg": 180, "16_kerb_x": [p["x"] for p in kerbs], "17_guideway_x": [p["x"] for p in guides], "17_end_overhang_m": round(gw_over, 4),
            "19_Xc": Xc, "19_Xc2": Xc2, "41_segments": len(curb_segs), "41_corners": len(corners), "41_skipped": n_skip,
            "44_grid_origin_corner": [9, -18.5], "44_pitch_m": 2.0, "44_plaza_count": len(plaza_tiles), "44_promenade_count": len(prom_tiles),
            "46_canal_x0_x1_n": [canal[0]["x"], canal[-1]["x"], len(canal)], "47_length_m": round(L, 4), "47_n": len(desire), "47_yaw_deg": desire[0]["rot_deg"],
            "47_centres": [[p["x"], p["z"]] for p in desire], "49_rot_deg": 90, "50_spin_st_w_x": round(xw, 4), "50_spin_st_e_x": round(xe, 4),
            "51_guideway_scuff_x": [p["x"] for p in scuff_g]}
with open(os.path.join(HERE, "exterior_placements_v1_3.json"), "w", encoding="utf-8") as fh:
    json.dump({"version": "v1.3", "yaw": "degrees about +Y; local +Z is front", "resolved": resolved, "placements": PLACEMENTS}, fh, indent=2)
    fh.write("\n")
print("wrote", os.path.join(HERE, "exterior_placements_v1_3.json"))
ASSET_SIZE = {"ext_tram_shelter.glb": (6.024, 1.304), "ext_tram_platform_kerb.glb": (1.994, 1.9), "ext_maglev_guideway.glb": (9.994, 3.146),
              "ext_maglev_car_body.glb": (12.162, 2.66), "ext_maglev_magnet_module.glb": (11.0, 1.412), "ext_curb_segment.glb": (1.994, 0.304),
              "ext_curb_corner.glb": (0.304, 0.304), "ext_platform_infill.glb": (11.994, 1.096), "ext_kerb_ramp.glb": (1.5, 3.0),
              "ext_canal_edge.glb": (1.994, 0.4), "ext_desire_path_decal.glb": (1.2, 4.0), "ext_ts4_dead_foliage.glb": (4.0, 0.406),
              "ext_ts4_wear_decal.glb": (4.0, 0.406), "hydro_planter_tiered_exterior.glb": (4.0, 0.406),
              "ext_track_scuff_guideway.glb": (9.994, 3.146), "ext_track_scuff_kerb.glb": (1.994, 1.9)}
def draw_v13(ax):
    # Tiles stay in the JSON. Draw one hatch per walk zone plus the plaza-tile centres, not one patch per tile.
    for n, x0, x1, z0, z1, k in Zg:
        if k == "walk": R_(ax, x0, x1, z0, z1, "none", ec="#A8B0B8", lw=0.15, z=4, hatch="..")
    R_(ax, 9, 18, -25.6, -12.5, "none", ec="#C47B3A", lw=1.0, z=6)
    for p in plaza_tiles: ax.plot(p["x"], p["z"], marker="s", ms=3.2, color="#E39A45", zorder=6, linestyle="none")
    style = {"ext_maglev_guideway.glb": ("#8E97A3", WALL, 0.45, 0.95, 5, None), "ext_curb_segment.glb": ("#5E6872", "#3A424C", 0.2, 0.9, 7, None),
             "ext_curb_corner.glb": ("#3E4650", "#3A424C", 0.2, 0.9, 7, None), "ext_canal_edge.glb": ("#7FA8B3", "#3B5966", 0.3, 0.95, 7, None),
             "ext_tram_platform_kerb.glb": ("#2E6BFF", WALL, 0.35, 0.9, 8, None), "ext_platform_infill.glb": ("#C5CAD1", WALL, 0.4, 0.75, 7, None),
             "ext_kerb_ramp.glb": ("#F4C98A", "#8A5A12", 0.6, 0.95, 8, None), "ext_tram_shelter.glb": ("#1A1E24", VIO, 1.3, 0.95, 9, None),
             "ext_maglev_car_body.glb": ("#F4F7FA", WALL, 0.7, 0.95, 10, None), "ext_maglev_magnet_module.glb": (VIO, VIO, 0.4, 0.35, 11, None),
             "ext_track_scuff_guideway.glb": ("none", ORG, 0.4, 1, 12, "///"), "ext_track_scuff_kerb.glb": ("none", ORG, 0.4, 1, 12, "///"),
             "ext_desire_path_decal.glb": (AMB, "#B36A00", 0.5, 0.55, 13, None), "ext_ts4_dead_foliage.glb": (ORG, WALL, 0.6, 0.9, 9, None),
             "ext_ts4_wear_decal.glb": ("none", AMB, 0.5, 1, 14, "xx"), "hydro_planter_tiered_exterior.glb": ("none", GRN, 0.7, 1, 9, None)}
    for p in PLACEMENTS:
        if p["asset"] in ("ext_paving_promenade.glb", "ext_paving_plaza.glb"): continue
        if p["asset"].startswith("ext_litter_drift"):
            fc, ec, lw, alpha, z, hatch = (ORG, WALL, 0.4, 0.9, 13, None); sx, sz = 1.07, 2.97
        else:
            fc, ec, lw, alpha, z, hatch = style[p["asset"]]; sx, sz = ASSET_SIZE[p["asset"]]
        rot = p["rot_deg"]; r = rot % 360.0; q = int(round(r / 90.0))
        if abs(r - q * 90.0) <= 1e-2:
            if q % 2: sx, sz = sz, sx
            R_(ax, p["x"] - sx / 2, p["x"] + sx / 2, p["z"] - sz / 2, p["z"] + sz / 2, fc, ec=ec, lw=lw, z=z, alpha=alpha, hatch=hatch)
        else:
            th = math.radians(rot); c, s = math.cos(th), math.sin(th); hx, hz = sx / 2, sz / 2
            pts = [(p["x"] + lx * c + lz * s, p["z"] - lx * s + lz * c) for lx, lz in ((-hx, -hz), (hx, -hz), (hx, hz), (-hx, hz))]
            ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=ec, lw=lw, zorder=z, alpha=alpha, hatch=hatch))
COL={"walk":PAVE,"guideway":STREET,"water":WATER,"green":"#CFEBD8","plot":"#E3E6EA","bldg":"#EEF1F5"}
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
    elif n=="bench": R_(ax,x0,x1,z0,z1,"#8C939E",ec=WALL,lw=0.8,z=9)
    elif n=="bin": R_(ax,x0,x1,z0,z1,WALL,ec=AMB,lw=0.8,z=9)
    elif n=="bollard": ax.add_patch(Circle(((x0+x1)/2,(z0+z1)/2),0.17,fc=WALL,ec="white",lw=0.5,zorder=11))
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
 (-8.4,11.25,"planters + 1:12 ramps mask 0.22 m step",5.8,"#1F6B3E","center"),
 (-2.4,-16.9,"SECTOR-4 PLAZA\n16 x 9.5 m",8,WALL,"center"),(-24.5,-12.2,"SECTOR-4 PROMENADE\n(Valley A frontage)",8,WALL,"left"),
 (10.3,-14.4,"worn desire path",6.5,"#B36A00","left"),(15,-20.5,"TRAM STOP (LIVE) + lived-in shelter",7,"white","center"),
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
    (GRN,GRN,"Sprocket route / pad"),(AMB,AMB,"light pole / worn path"),("#E3E6EA",GRAPH,"facade-only plot"),("#8C939E",WALL,"bench"),(WALL,AMB,"bin"),(WALL,"white","bollard")]
for i,(fc,ec,lab) in enumerate(lg):
    x=-46+(i//4)*13; z=-44.2-(i%4)*1.5; R_(ax,x,x+1.4,z-0.35,z+0.35,fc,ec=ec,lw=1,z=12); T(ax,x+2,z,lab,7,ha="left")
R_(ax,-6,4,-47.6,-47.0,WALL,z=12); R_(ax,-6,-1,-47.6,-47.0,"white",ec=WALL,lw=1,z=12); T(ax,-1,-48.6,"0          5          10 m",7)
cx,cz=30,-47.5
for dx,dz in [(0,3),(0,-3),(3,0),(-3,0)]: ax.annotate("",xy=(cx+dx,cz+dz),xytext=(cx,cz),arrowprops=dict(arrowstyle="-|>",color=WALL,lw=1.4))
T(ax,cx,cz+3.8,"SPINWARD +Z",7,weight="bold"); T(ax,cx,cz-3.8,"ANTISPINWARD -Z",7,weight="bold")
T(ax,cx-3.6,cz,"FORE -X",7,ha="right"); T(ax,cx+3.6,cz,"AFT +X",7,ha="left")
T(ax,-46,-51.0,"X = axial (flat)  |  up = toward axis, down = radially outward",6.5,color="#555",ha="left")
ax.set_title("RESIDENTIAL rev C - EXTERIOR + 20 m CITY RING (plan, L1) - v1.2 furniture   |   Cylinder Hab-7, Valley A, Sector-4   |   floor R 185.5 m",fontsize=11.5,weight="bold",color=WALL)
ax.set_xlim(-51,47); ax.set_ylim(-52,42.5); ax.set_aspect("equal"); ax.axis("off")
fig.savefig(os.path.join(HERE,"residential_exterior_plan_v1_2_plan.png"),bbox_inches="tight",facecolor="white")
draw_v13(ax)
ax.set_title("RESIDENTIAL rev C - EXTERIOR + 20 m CITY RING (plan, L1) - v1.3 placements, no roads   |   Cylinder Hab-7, Valley A, Sector-4   |   floor R 185.5 m",fontsize=11.5,weight="bold",color=WALL)
ax.set_xlim(-52,52)
fig.savefig(os.path.join(HERE,"residential_exterior_plan_v1_3_plan.png"),bbox_inches="tight",facecolor="white"); plt.close(fig)
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
fig.savefig(os.path.join(HERE,"residential_exterior_plan_v1_section.png"),bbox_inches="tight",facecolor="white"); plt.close(fig)
