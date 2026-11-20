"""Rook door_lab: door_lab_bulkhead_hatch.glb - heavy pressure bulkhead, plug leaf (Gage door-lab sprint 2026-11-20).
Dimensions/gaps per Vance context/door_lab/REALISM_SPEC.md section 4 (clear 0.90 x 1.90 m R150 over the plant-only 150 mm coaming,
plug leaf 1.10 x 2.10 x 0.12 m seated in a frame rebate with 6 mm all round, 30 mm inflatable seal in a land groove (deflated in the
GLB; 8 mm compression when inflated), 8 dogs (2 per side) with linkage bars to the central locking wheel (wheel turns 90 deg,
dog throw 25 mm onto frame wedges), 2 heavy hinges, hinge axis 0.10 m outboard of the leaf edge, rotary actuator housing at the lower
hinge, linear damper, push-off rams, dP gauges both sides + digital readout, equalize valve, hub lamp ring, amber beacon).
Materials per Sloane AESTHETIC_SPEC section 1 (gunmetal body, graphite recessed panels, brushed-steel dogs/wheel, rubber seal).
Rig (values after the bottom-centre recenter are printed by qa_hatch.py):
  leaf      : origin ON the hinge axis (vertical); open = rotate about local +Y by +OPEN_DEG (swings out to +Z).
  dog_handwheel : child of leaf (named so Godot does not auto-convert a *_wheel node into VehicleWheel3D), origin on the wheel axis (local Z); dogging = rotate about local Z by DOG_DEG.
  latch_bolt_0..7 : children of leaf (dog + its linkage bar), origin = retracted dog tip; local +X = dog axis (outward);
                    throw = +X BOLT_THROW.
  piston_body : root child, origin on its frame clevis pin; body runs along local -Z (look_at the piston_rod origin).
  piston_rod  : child of leaf, origin on its leaf clevis pin; rod runs along local -Z (look_at the piston_body origin).
  seal      : root child, origin on the groove floor; inflate = scale local Z by SEAL_INFLATE_SCALE (deflated as modelled).
  gauge_needle_front / gauge_needle_back : origin on the dial centre, rotate about local Z (0 = 0 kPa).
  status_light (hub lamp ring, child of leaf) / beacon (root): emissive DL_StatusLamp (amber default).
Run: python3 assets/src/door_lab/bulkhead_hatch.py"""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from door_lab_lib import *

CW, CH, CR = .90, 1.90, .15         # clear opening (Vance 4.1)
SILL = .15; CY = SILL + CH/2         # plant-only coaming (Vance 4.1)
LAPW = .10; LW, LH, LR = CW + 2*LAPW, CH + 2*LAPW, CR + LAPW
LZ0, LZ1 = -.06, .06                 # leaf back / front (0.12 T)
GAP = .006                           # leaf to frame, seal deflated
REB_OFF = LAPW + GAP; LAND_Z = LZ0 - GAP
TAPER = .012                         # plug-edge taper toward the back (sweep clearance in the rebate)
COL_OFF, COL_Z0 = .40, -.30
HX, HZ = LW/2 + .10, .08             # hinge axis: 0.10 m outboard of the leaf edge, 20 mm above the leaf front plane
OPEN_DEG = 100.0
DOG_Z, DOG_R, DOG_LEN, BOLT_THROW = .085, .011, .13, .025
DOG_DEG = 90.0
WEDGE_GAP = .010                     # wedge starts 10 mm beyond the leaf edge (leaf sweep clears it)
PY = 2.30; PF = np.array([-.45, PY, .10]); PL = np.array([.36, PY, .13])
BODY_LEN, BORE_LEN, ROD_LEN = .62, .55, .66
SEAL_Z0, SEAL_TOP = LAND_Z - .017, LZ0 - .002
SEAL_INFLATE_SCALE = ((LZ0 + .008) - SEAL_Z0) / (SEAL_TOP - SEAL_Z0)
HINGES = (.30, 1.80)                 # station bottoms (station = frame knuckle / leaf knuckle / frame knuckle, 2 mm clear)
# dogs: (edge anchor point on the leaf edge, outward unit dir)
EX, ETOP, EBOT = LW/2, CY + LH/2, CY - LH/2
DOGS = [((-EX, .65), (-1, 0)), ((-EX, 1.55), (-1, 0)), ((EX, .75), (1, 0)), ((EX, 1.45), (1, 0)),
        ((-.18, ETOP), (0, 1)), ((.18, ETOP), (0, 1)), ((-.18, EBOT), (0, -1)), ((.18, EBOT), (0, -1))]

def V(m): m = trimesh.Trimesh(m.vertices, m.faces, process=True); m.fix_normals(); return m
def boolean(op, ms):
    r = getattr(trimesh.boolean, op)([V(m) for m in ms], engine="manifold"); r.fix_normals(); return uvp(r)
def rr_prism(off, z0, z1, n=5, r_add=0.0):
    return solid_rr(CW + 2*off, CH + 2*off, CR + off + r_add, [(0, z0), (0, z1)], n, (0, CY))
def dog_frame(i):
    (px, py), (dx, dy) = DOGS[i]; ang = np.arctan2(dy, dx); return np.array([px, py]), ang
def place(m, i, z=0.0):
    p, ang = dog_frame(i); return xf(m, R=TF.rotation_matrix(ang, [0, 0, 1]), t=(p[0], p[1], z))

def frame(rig):
    cut = rr_prism(COL_OFF - E, -.40, .10, 4)
    wall = boolean("difference", [trimesh.creation.box(bounds=[[-1.30, 0, -.22], [1.30, 3.0, -.12]]), cut])
    pil = []
    for s in (-1, 1):
        x0, x1 = sorted((s*1.02, s*1.28))
        pil += [bplate(x0, x1, 0, 2.86, -.12 - E, -.085, .015), bplate(x0 + .05*(s < 0), x1 - .05*(s > 0), .25, 2.60, -.085 - E, -.065, .010)]
        for yy in np.arange(.40, 2.50, .42): pil.append(cap(((x0 + x1)/2 - .02*s, yy, -.065 + .004), .016, .016, 6, "z"))
    pil.append(bplate(-1.28, 1.28, 2.86, 3.0 - .01, -.12 - E, -.08, .02))
    rig.part("frame", None, G, [wall] + pil)
    # collar: bevelled outer block - clear opening - plug rebate (leaf + 6 mm, to the land) - 34 mm seal groove, cut at the floor
    outer = solid_rr(CW + 2*COL_OFF, CH + 2*COL_OFF, CR + COL_OFF, [(-.03, COL_Z0), (0, COL_Z0 + .03), (0, -.04), (-.04, 0)], 4, (0, CY))
    opening = rr_prism(0, -.5, .2); reb = rr_prism(REB_OFF, LAND_Z, .2)
    groove = boolean("difference", [rr_prism(.067, SEAL_Z0, LAND_Z + .01), rr_prism(.033, SEAL_Z0 - .02, LAND_Z + .02)])
    groove = V(groove)
    col = boolean("difference", [outer, opening, reb, groove])
    col = boolean("intersection", [col, trimesh.creation.box(bounds=[[-2, 0, -1], [2, 4, 1]])])
    rig.part("frame_collar", None, SGM, [col])
    # inflatable seal bead (deflated: top 2 mm below the leaf back), origin on the groove floor for the inflate scale
    bead = sweep_rr(CW, CH, CR, [(.035, SEAL_Z0 - E), (.065, SEAL_Z0 - E), (.064, SEAL_TOP - .006), (.058, SEAL_TOP), (.042, SEAL_TOP), (.036, SEAL_TOP - .006)], 4, (0, CY))
    bead = boolean("intersection", [bead, trimesh.creation.box(bounds=[[-2, .002, -1], [2, 4, 1]])])
    rig.part("seal", None, SEAL, [bead], W=T((0, CY, SEAL_Z0)))
    # frame wedges (dog keepers): sloped blocks on the collar face beyond each dog
    wd = []
    for i in range(8):
        m = loft(np.array([(.035, 0), (-.035, 0), (-.035, .070), (.035, .070)]), [(0, 1, 1), (.06, 1, 1)])   # (v, z) outline along +Y=u
        m = xf(m, R=TF.rotation_matrix(-np.pi/2, [0, 0, 1]), t=(WEDGE_GAP, 0, 0))       # +Y -> +X (u)
        m.vertices[:, 2] = np.where(m.vertices[:, 2] > .05, np.where(m.vertices[:, 0] < WEDGE_GAP + .02, .062, .070), m.vertices[:, 2]) - E
        if dog_frame(i)[0][1] < .2: m.vertices[:, 0] = np.minimum(m.vertices[:, 0], WEDGE_GAP + .036)     # bottom wedges stop 2 mm off the floor
        wd.append(place(m, i))
    rig.part("dog_wedges", None, ST, wd)
    # hinges (frame side): knuckles + brackets; rotary actuator housing under the lower hinge
    hk = []
    for s0 in HINGES:
        for y0, y1 in ((s0, s0 + .098), (s0 + .202, s0 + .30)):
            hk += [cap((HX, (y0 + y1)/2, HZ), .05, y1 - y0, 10, "y"), box(HX - .04, HX + .04, y0, y1, -E, HZ)]
    hk += [cap((HX, (.17 + HINGES[0] + E)/2, HZ), .065, HINGES[0] + E - .17, 12, "y"), box(HX - .045, HX + .045, .17, HINGES[0] + E, -E, HZ)]
    rig.part("hinge_frame", None, ST, hk)
    # damper frame clevis
    cl = [box(PF[0] - .05, PF[0] + .05, PY - .06, PY - .029, -E, PF[2] + .05), box(PF[0] - .05, PF[0] + .05, PY + .029, PY + .06, -E, PF[2] + .05),
          box(PF[0] - .05, PF[0] + .05, PY - .06, PY + .06, -E, .03), cap(PF, .012, .13, 8, "y")]
    rig.part("damper_mount", None, ALY, cl)
    # push-off rams on the land (2, near the latch edge), 4 mm short of the leaf back
    rams = [cap((-(CW/2 + .085), y, (LAND_Z - E + LZ0 - .004)/2), .011, (LZ0 - .004) - (LAND_Z - E), 8, "z") for y in (.70, 1.50)]
    rig.part("pushoff_rams", None, ALY, rams)
    # dP gauges (front + back) with digital readout, equalize valve grille (latch side, outside the leaf sweep)
    gx, gy = -.73, 1.25
    for side, zf in (("front", 0.0), ("back", COL_Z0)):
        sz = 1 if side == "front" else -1
        hs = [cap((gx, gy, zf + sz*.018), .065, .036 + 2*E, 12, "z"), box(gx - .07, gx + .07, 1.04, 1.13, zf - sz*E, zf + sz*.03) if sz > 0 else mz_(box(gx - .07, gx + .07, 1.04, 1.13, -zf - E, -zf + .03)),
              box(gx - .06, gx + .06, .84, .98, zf - sz*E, zf + sz*.025) if sz > 0 else mz_(box(gx - .06, gx + .06, .84, .98, -zf - E, -zf + .025))]
        for k in range(4):
            yy = .855 + k*.032; g_ = box(gx - .05, gx + .05, yy, yy + .012, zf + sz*.025 - sz*E, zf + sz*.031) if sz > 0 else mz_(box(gx - .05, gx + .05, yy, yy + .012, -zf + .025 - E, -zf + .031))
            hs.append(g_)
        rig.part(f"gauge_housing_{side}", None, ALY, hs)
        face = [cap((gx, gy, zf + sz*.041), .055, .005, 16, "z"), (box(gx - .055, gx + .055, 1.06, 1.11, zf + sz*.03 - sz*E, zf + sz*.033) if sz > 0 else mz_(box(gx - .055, gx + .055, 1.06, 1.11, -zf + .03 - E, -zf + .033)))]
        rig.part(f"gauge_face_{side}", None, GLOW, face)
        c = np.array([gx, gy, zf + sz*.047])
        nd = [box(-.004, .004, -.008, .045, -.002, .002), cap((0, 0, 0), .008, .004, 8, "z")]
        rig.part(f"gauge_needle_{side}", None, AM, [xf(m, t=c) for m in nd], W=T(c))
    # amber beacon above the door on the wall panel
    bc = [cap((0, 2.66, -.12 + .02), .05, .04 + 2*E, 12, "z")]
    rig.part("beacon_housing", None, ALY, bc)
    rig.part("beacon", None, STAT, [xf(trimesh.creation.icosphere(1, .04), t=(0, 2.66, -.12 + .04 + .015)) if False else cap((0, 2.66, -.12 + .052), .038, .028, 12, "z")])
    ccol = boolean("difference", [solid_rr(CW + 2*COL_OFF, CH + 2*COL_OFF, CR + COL_OFF, [(0, COL_Z0), (0, 0)], 3, (0, CY)), rr_prism(0, -.5, .2, 3), rr_prism(REB_OFF, LAND_Z, .2, 3)])
    ccol = boolean("intersection", [ccol, trimesh.creation.box(bounds=[[-2, 0, -1], [2, 4, 1]])])
    rig.part("frame-colonly", None, G, [wall.copy(), ccol])

def mz_(m): m = xf(m.copy(), R=np.diag([1, 1, -1, 1])); m.fix_normals(); return m

def dog_line_dist(x, y):
    best = 9
    for i in range(8):
        p, ang = dog_frame(i); d = np.array([np.cos(ang), np.sin(ang)]); q = np.array([x, y]) - p
        u = q @ d; v = abs(q @ np.array([-d[1], d[0]]))
        if -.17 < u < .03: best = min(best, v)
    return best

def leaf(rig):
    g = rig.group("leaf", None, T((HX, 0, HZ)))
    shell = solid_rr(LW, LH, LR, [(-TAPER - .004, LZ0), (-TAPER, LZ0 + .004), (0, 0), (0, LZ1 - .008), (-.008, LZ1)], 5, (0, CY))
    rig.part("leaf_shell", g, G, [shell])
    # graphite panels (4 quadrants), gunmetal boss for the wheel
    pn = []
    for sx in (-1, 1):
        for y0, y1 in ((CY - .86, CY - .22), (CY + .22, CY + .86)):
            x0, x1 = sorted((sx*.08, sx*.40)); pn.append(bplate(x0, x1, y0, y1, LZ1 - E, LZ1 + .006, .003))
    rig.part("leaf_panels", g, SL, pn)
    boss = [cap((0, CY, LZ1 + .018), .12, .036 + 2*E, 16, "z")]
    # bolt heads ring (avoid dog paths, hinge straps, damper mount)
    heads = []
    ring = rr_xy(LW - .08, LH - .08, LR - .04, 10, (0, CY)); per = np.r_[0, np.cumsum(np.linalg.norm(np.diff(np.vstack([ring, ring[:1]]), axis=0), axis=1))]
    for t in np.linspace(0, per[-1], 24, endpoint=False):
        i = np.searchsorted(per, t, side="right") - 1; f = (t - per[i]) / (per[i + 1] - per[i]); x, y = ring[i] + f*(ring[(i + 1) % len(ring)] - ring[i])
        if dog_line_dist(x, y) < .05: continue
        if x > .35 and any(s0 + .07 < y < s0 + .23 for s0 in HINGES): continue
        if .28 < x < .45 and y > 2.0: continue
        heads.append(cap((x, y, LZ1 + .006), .014, .012 + 2*E, 6, "z"))
    rig.part("leaf_bolt_heads", g, ST, heads + boss)
    # dog guides (one U-strap per dog, 20 mm inside the edge)
    gd = []
    for i in range(8):
        uc = -.045
        for m in (box(uc - .012, uc + .012, .015, .025, LZ1 - E, .106), box(uc - .012, uc + .012, -.025, -.015, LZ1 - E, .106), box(uc - .012, uc + .012, -.025, .025, .098, .106)):
            gd.append(place(m, i))
    rig.part("leaf_dog_guides", g, ALY, gd)
    # hinge straps + leaf knuckles
    hs = []
    for s0 in HINGES:
        y0, y1 = s0 + .10, s0 + .20
        hs += [cap((HX, (y0 + y1)/2, HZ), .05, y1 - y0, 10, "y"), bplate(.42, HX, y0, y1, LZ1 - E, HZ + .02, .010)]
    rig.part("leaf_hinge_straps", g, ST, hs)
    # damper leaf clevis (post on the +Z side; the rod only points leaf-local -Z / +-X)
    lm = [box(PL[0] - .05, PL[0] + .05, 2.06, PY - .029, LZ1 - E, PL[2] + .05), box(PL[0] - .05, PL[0] + .05, PY + .029, PY + .06, PL[2] - .06, PL[2] + .07),
          box(PL[0] - .03, PL[0] + .03, PY - .029 - E, PY + .029 + E, PL[2] + .05, PL[2] + .07), cap(PL, .012, .13, 8, "y")]
    rig.part("leaf_damper_mount", g, ALY, lm)
    # hub lamp ring (status, own emissive material)
    rig.part("status_light", g, STAT, [annulus_z((0, CY), .125, .14, LZ1 - E, LZ1 + .006, 16)])
    rig.part("leaf-convcolonly", g, G, [solid_rr(LW, LH, LR, [(-TAPER, LZ0), (0, 0), (0, LZ1)], 3, (0, CY))])
    # locking wheel (origin on its axis)
    wc = np.array([0, CY, .165])
    wh = [xf(torus(.20, .018, 16, 5), t=wc), cap(wc, .05, .05, 10, "z"), cap((0, CY, (LZ1 + .036 + .14)/2), .028, .14 - (LZ1 + .036) + E, 8, "z")]
    for k in range(4):
        a = np.radians(90*k + 45); wh.append(xf(box(.045, .19, -.011, .011, -.011, .011), R=TF.rotation_matrix(a, [0, 0, 1]), t=wc))
    rig.part("dog_handwheel", g, ST, wh, W=T(wc))
    # 8 dogs: rod + linkage bar to the hub (part of the dog node, so it moves with it)
    for i in range(8):
        p, ang = dog_frame(i); tip = np.array([p[0], p[1], DOG_Z]) + np.array([np.cos(ang), np.sin(ang), 0])*(-.005)
        Wb = T(tip) @ TF.rotation_matrix(ang, [0, 0, 1])
        rod = xf(cap((0, 0, 0), DOG_R, DOG_LEN, 10, "x"), t=(-DOG_LEN/2, 0, 0))
        riser = box(-DOG_LEN, -DOG_LEN + .025, -.012, .012, LZ1 + .006 + .002 - DOG_Z, 0)
        # bar from the riser to a point 0.155 m from the hub centre, flat on 2 mm standoff over the panels
        hub = np.array([0, CY]); a_ = tip[:2] + np.array([np.cos(ang), np.sin(ang)])*(-DOG_LEN + .012)
        dv = a_ - hub; h0 = hub + dv/np.linalg.norm(dv)*.155
        L = np.linalg.norm(a_ - h0); th = np.arctan2(*(a_ - h0)[::-1])
        bar_w = box(0, L, -.012, .012, LZ1 + .008, LZ1 + .016)
        bar_w = xf(bar_w, R=TF.rotation_matrix(th, [0, 0, 1]), t=(h0[0], h0[1], 0))
        bar_l = bar_w.copy(); bar_l.apply_transform(np.linalg.inv(Wb)); bar_l.metadata["uv"] = bar_w.metadata["uv"]
        m = merge([rod, riser, bar_l]); m = xf(m, R=Wb)
        rig.part(f"latch_bolt_{i}", g, ST, [m], W=Wb)
    return g

def pistons(rig):
    d = PL - PF; psi = np.arctan2(-d[0], -d[2])
    Wb = T(PF) @ TF.rotation_matrix(psi, [0, 1, 0]); Wr = T(PL) @ TF.rotation_matrix(psi + np.pi, [0, 1, 0])
    eye = xf(ring_between(circle(.02, 10), circle(.045, 10), -.024, .024), R=TF.rotation_matrix(-np.pi/2, [1, 0, 0]))
    shank = box(-.02, .02, -.022, .022, -BODY_LEN + BORE_LEN - .005, -.04)
    cyl = ring_between(circle(.026, 12), circle(.042, 12), -BODY_LEN, -BODY_LEN + BORE_LEN)
    endcap = cap((0, 0, -BODY_LEN + BORE_LEN + .005), .044, .02, 12, "z")
    gland = ring_between(circle(.026, 12), circle(.047, 12), -BODY_LEN, -BODY_LEN + .03)
    body = [eye, shank, cyl, endcap, gland]
    for m in body: m.fix_normals()
    rig.part("piston_body", None, ST, body, world=False, W=Wb)
    reye = xf(ring_between(circle(.02, 10), circle(.045, 10), -.024, .024), R=TF.rotation_matrix(-np.pi/2, [1, 0, 0]))
    rod = cap((0, 0, -(ROD_LEN + .04)/2), .018, ROD_LEN - .04, 10, "z"); head = cap((0, 0, -ROD_LEN + .01), .023, .02, 12, "z")
    rig.part("piston_rod", "leaf", ALY, [reye, rod, head], world=False, W=Wr)

def build():
    rig = Rig("door_lab_bulkhead_hatch"); frame(rig); leaf(rig); pistons(rig); return rig

def deltas(rig, f_open=0.0, f_bolt=1.0):
    """f_open 0..1 of OPEN_DEG; f_bolt 1 = dogs thrown. Pistons re-aimed at each other."""
    phi = np.radians(OPEN_DEG*f_open); d = {"leaf": TF.rotation_matrix(phi, [0, 1, 0]), "dog_handwheel": TF.rotation_matrix(np.radians(DOG_DEG*f_bolt), [0, 0, 1])}
    for i in range(8): d[f"latch_bolt_{i}"] = T((BOLT_THROW*f_bolt, 0, 0))
    W0 = rig.pose(d); F = W0["piston_body"][:3, 3]; L = W0["piston_rod"][:3, 3]; v = L - F
    psi_w = np.arctan2(-v[0], -v[2]); r0 = rig.N["piston_rod"]["W"][:3, 3] - rig.N["piston_body"]["W"][:3, 3]; psi0 = np.arctan2(-r0[0], -r0[2])
    d["piston_body"] = TF.rotation_matrix(psi_w - psi0, [0, 1, 0]); d["piston_rod"] = TF.rotation_matrix(psi_w - psi0 - phi, [0, 1, 0])
    return d

if __name__ == "__main__":
    rig = build(); sh = rig.recenter(); print("recenter shift", sh)
    gp = os.path.join(OUT_GLB, "door_lab_bulkhead_hatch.glb"); print("tris", rig.export(gp)); print("\n".join(rig.tree()))
