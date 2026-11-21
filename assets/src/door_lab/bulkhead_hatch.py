"""Rook door_lab pass C: door_lab_bulkhead_hatch.glb - heavy pressure bulkhead, real plug leaf (Vance REALISM_SPEC sections 4.1/4.5/4.7,
section 9 FAIL list). Approach side = -Z (Gage's door lab approach and QA cameras); the leaf swings 100 deg toward +Z (high-pressure side, plug).
  Clear opening 0.90 x 1.90 m R150 over a 150 mm plant coaming (V3/V4: 300 mm marine coaming).
  Leaf 1.10 x 2.10 x 0.12 m: a 60 mm flange (stepped back edge = seal land, 10 mm front chamfer) plus a 60 mm PLUG that enters the opening
  (6 mm to the reveal at the land, chamfered to 18 mm at the plug face so the latch edge clears the reveal on the swing).
  Seal: inflatable bead (30 mm section) in a 34 mm groove in the collar land, 6 mm land gap, 8 mm compression when inflated.
  8 dogs (2 per side) on the plug face, cam-driven by linkages from the central locking wheel (90 deg, 25 mm throw), engaging 8 wedge keepers on
  the opening reveal (3 mm lead-in). Coaxial OverrideOrange handwheel (rim + 5 spokes) on a planetary gearbox, 12 turns full throw.
  2 heavy hinges (axis 0.10 m outboard of the leaf edge), davit arm + frame bracket, hydraulic rotary actuator housing under the lower hinge,
  linear damper, 2 push-off rams in bored holes near the latch edge, ribbed +Z back face, dP gauges (0-110 kPa, green band <= 0.5 kPa) and
  digital readouts on BOTH faces, equalize port + grille, OverrideOrange manual equalize lever, hub lamp ring, amber beacon.
Rig (closed pose; LH variants are X-mirrors: rotations about local Y/Z and translations along local X flip sign):
  leaf (pivot name kept for Gage's scene)  origin ON the hinge axis; open = rotate about local +Y by +OPEN_DEG.
  bulkhead_LockWheel        child of leaf, origin on the wheel axis; dogs thrown = rotate about local +Z by +DOG_DEG (90).
  bulkhead_OverrideOrange_Handwheel  child of leaf, coaxial; manual = rotate about local +Z, 12 turns (4320 deg) for full throw.
  bulkhead_Dog_01..08       child of leaf, origin at the retracted dog tip, local +X = throw; thrown = +X 0.025 m.
  bulkhead_Linkage_01..08   child of leaf, origin at the cam-follower pin; thrown = +X 0.025 m (same axis as its dog).
  bulkhead_InflatableSeal   root, origin on the groove floor; inflate = scale local Z by SEAL_INFLATE_SCALE.
  bulkhead_PushOffRam_1/2   root, origin at the ram head; unseat = +Z 0.012 m (phase 6), retract after.
  bulkhead_Damper_body      root, origin on the frame clevis pin, body along local -Z; aim at bulkhead_DamperRod origin (rotate about Y).
  bulkhead_DamperRod        child of leaf, origin on the leaf clevis pin, rod along local -Z; aim at the body origin.
  bulkhead_Gauge_needle_front/back  origin on the dial centre; rotate about local Z by -270/110 (front) / +270/110 (back) deg per kPa
                            (clockwise as seen from each face; needle modelled at 0 kPa).
  bulkhead_EqualizeLever    root, origin on the valve stem (approach face); open = rotate about local Z by -90 deg (handle swings toward the opening).
Run: python3 assets/src/door_lab/bulkhead_hatch.py"""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from door_lab_lib import *

CW, CH, CR = .90, 1.90, .15
LAPW = .10; LW, LH, LR = CW + 2*LAPW, CH + 2*LAPW, CR + LAPW
GAP = .006
FZ0, FZ1 = GAP, GAP + .060          # flange back / front
PZ0 = FZ1 - .120                     # plug face (-0.054)
PLUG_IN0, PLUG_IN1 = .006, .018      # plug inset from the reveal at the land / at the plug face
COL_OFF, COL_Z0 = .40, -.30
GRV_I, GRV_O, GRV_D = .033, .067, .020
OPEN_DEG = 100.0
DOG_DEG, DOG_THROW, DOG_LEN = 90.0, .025, .13
# Rook M-122 (2026-11-21): the dogging gear is HOUSED in the leaf. The plug face is a tray (TRAY_IN inside the opening outline, floor
# TRAY_Z), with the dogs, linkages and cam disc stacked inside it (front to back: dogs, linkage bars, cam disc + lobes), so every dog /
# linkage sits >= 4 mm inside the leaf shell's bounds (Gage's lab used to scale them toward the shell centre at runtime, x0.68 / x0.54).
# The dogs run out to the keepers through slots in the tray rim; the keepers moved back with them (still behind the thrown dog tip).
TRAY_IN, TRAY_Z = .024, PZ0 + .0485
DOG_Z0, DOG_Z1 = PZ0 + .004, PZ0 + .018   # dog bar, 14 mm, its front 4 mm behind the plug face
KEEP_Z0, KEEP_Z1, KEEP_IN = DOG_Z1 + .0015, DOG_Z1 + .018, .009
LINK_Z0, LINK_Z1 = DOG_Z1 + .002, DOG_Z1 + .012   # linkage bars behind the dogs
DISC_Z0, DISC_Z1 = LINK_Z1 + .002, LINK_Z1 + .0125  # cam disc behind the linkages (lobes on its back, 2 mm off the tray floor)
SEAL_Z0 = -GRV_D - .002; SEAL_TOP = FZ0 - .002
SEAL_INFLATE_SCALE = ((FZ0 + .008) - SEAL_Z0) / (SEAL_TOP - SEAL_Z0)

def params(prm):
    p = dict(sill=.15, ribs=4, kick=False); p.update(prm or {}); return p

class B:  # derived geometry for one variant
    def __init__(s, p):
        s.p = p; s.SILL = p["sill"]; s.CY = s.SILL + CH/2
        s.HX, s.HZ = LW/2 + .10, FZ1 + .020
        s.HINGES = (.30 + s.SILL - .15, 1.80 + s.SILL - .15)
        s.PY = s.CY + LH/2 + .15
        s.PF = np.array([-.45, s.PY, .106]); s.PL = np.array([.36, s.PY, .136])
        ex, et, eb = CW/2, s.CY + CH/2, s.CY - CH/2
        s.DOGS = [((-ex, s.CY - .45), (-1, 0)), ((-ex, s.CY + .45), (-1, 0)), ((ex, s.CY - .45), (1, 0)), ((ex, s.CY + .45), (1, 0)),
                  ((-.18, et), (0, 1)), ((.18, et), (0, 1)), ((-.18, eb), (0, -1)), ((.18, eb), (0, -1))]

def rr_prism(b, off, z0, z1, n=4):
    return solid_rr(CW + 2*off, CH + 2*off, CR + off, [(0, z0), (0, z1)], n, (0, b.CY))
def dog_frame(b, i):
    (px, py), (dx, dy) = b.DOGS[i]; return np.array([px, py]), np.arctan2(dy, dx)
def place(b, m, i, z=0.0, inset=0.0):
    p, ang = dog_frame(b, i); d = np.array([np.cos(ang), np.sin(ang)]); q = p - d*inset
    return xf(m, R=TF.rotation_matrix(ang, [0, 0, 1]), t=(q[0], q[1], z))
def mz_(m): m = xf(m.copy(), R=np.diag([1, 1, -1, 1])); m.fix_normals(); return m

def frame(rig, b):
    cut = rr_prism(b, COL_OFF - E, -.40, .10, 3)
    wall = boolean("difference", [trimesh.creation.box(bounds=[[-1.30, .002, -.22], [1.30, 3.0, -.12]]), cut])   # 2 mm off the floor: no coplanar floor band with the collar foot
    pil = []
    for s in (-1, 1):
        x0, x1 = sorted((s*1.02, s*1.28))
        pil += [bplate(x0, x1, 0, 2.86, -.12 - E, -.085, .015), bplate(x0 + .05*(s < 0), x1 - .05*(s > 0), .25, 2.60, -.085 - E, -.065, .010)]
    pil.append(bplate(-1.28, 1.28, 2.86, 3.0 - .01, -.12 - E, -.08, .02))
    rig.part("bulkhead_frame", None, G, [wall] + pil)
    # collar: bevelled block - clear opening - seal groove in the land (front face z = 0) - push-off ram bores, cut at the floor
    outer = solid_rr(CW + 2*COL_OFF, CH + 2*COL_OFF, CR + COL_OFF, [(-.03, COL_Z0), (0, COL_Z0 + .03), (0, -.04), (-.04, 0)], 3, (0, b.CY))
    groove = boolean("difference", [rr_prism(b, GRV_O, -GRV_D, .02, 3), rr_prism(b, GRV_I, -GRV_D - .01, .03, 3)])
    bores = [cap((-(CW/2 + .085), b.CY + dy, -.02), .013, .042, 10, "z") for dy in (-.40, .40)]
    col = boolean("difference", [outer, rr_prism(b, 0, -.5, .2, 3), groove] + bores)
    col = boolean("intersection", [col, trimesh.creation.box(bounds=[[-2, 0, -1], [2, 4, 1]])])
    rig.part("bulkhead_frame_collar", None, SGM, [col])
    bead = sweep_rr(CW, CH, CR, [(GRV_I + .002, SEAL_Z0), (GRV_O - .002, SEAL_Z0), (GRV_O - .002, SEAL_TOP - .008), (GRV_O - .009, SEAL_TOP),
                                 (GRV_I + .009, SEAL_TOP), (GRV_I + .002, SEAL_TOP - .008)], 3, (0, b.CY))
    bead = boolean("intersection", [bead, trimesh.creation.box(bounds=[[-2, .002, -1], [2, 4, 1]])])
    rig.part("bulkhead_InflatableSeal", None, SEAL, [bead], W=T((0, b.CY, SEAL_Z0)))
    # wedge keepers on the reveal, in front of (toward +Z of) each thrown dog tip; 3 mm lead-in on the back face
    kp = []
    for i in range(8):
        m = box(-KEEP_IN, E, -.032, .032, KEEP_Z0, KEEP_Z1)
        m.vertices[:, 2] = np.where((m.vertices[:, 2] < KEEP_Z0 + 1e-6) & (m.vertices[:, 0] < -.005), KEEP_Z0 + .003, m.vertices[:, 2])
        kp.append(place(b, m, i))
    rig.part("bulkhead_Keeper", None, ST, kp)
    # hinges (frame side knuckles + brackets) and the rotary actuator housing under the lower hinge
    hk = []
    for s0 in b.HINGES:
        for y0, y1 in ((s0, s0 + .098), (s0 + .202, s0 + .30)):
            hk += [cap((b.HX, (y0 + y1)/2, b.HZ), .05, y1 - y0, 10, "y"), box(b.HX - .04, b.HX + .04, y0, y1, -E, b.HZ)]
    rig.part("bulkhead_HingeHeavy_frame", None, ST, hk)
    a0 = max(.02, b.HINGES[0] - .13)
    act = [cap((b.HX, (a0 + b.HINGES[0] + E)/2, b.HZ), .065, b.HINGES[0] + E - a0, 12, "y"), box(b.HX - .045, b.HX + .045, a0, b.HINGES[0] + E, -E - .002, b.HZ - .006),
           cap((b.HX + .07, a0 + .05, b.HZ), .018, .05, 8, "x")]
    rig.part("bulkhead_Actuator_housing", None, G, act)
    # davit: frame knuckle + bracket on the collar face, on the hinge axis just above the leaf's davit arm (below the damper band)
    ytop = b.CY + LH/2; dy0 = ytop + .086
    dv = [cap((b.HX, dy0 + .04, b.HZ), .04, .08, 10, "y"), box(b.HX - .04, b.HX + .04, dy0, dy0 + .08, -E, b.HZ)]
    rig.part("bulkhead_Davit_bracket", None, ST, dv)
    # damper frame clevis
    PF, PY = b.PF, b.PY
    cl = [box(PF[0] - .05, PF[0] + .05, PY - .06, PY - .029, -E, PF[2] + .05), box(PF[0] - .05, PF[0] + .05, PY + .029, PY + .06, -E, PF[2] + .05),
          box(PF[0] - .05, PF[0] + .05, PY - .06, PY + .06, -E, .03), cap(PF, .012, .13, 8, "y")]
    rig.part("bulkhead_damper_mount", None, ALY, cl)
    # push-off rams in their bores (head 4 mm short of the flange back)
    for k, dy in enumerate((-.40, .40)):
        c = np.array([-(CW/2 + .085), b.CY + dy, FZ0 - .004])
        rig.part(f"bulkhead_PushOffRam_{k + 1}", None, ALY, [cap((c[0], c[1], c[2] - .021), .011, .042, 10, "z")], W=T(c))
    # dP gauges + digital readouts both faces, equalize port/grille both faces, OverrideOrange equalize lever on the approach face
    gx, gy = -.73, b.CY + .15
    for side, zf, sz in (("front", 0.0, 1), ("back", COL_Z0, -1)):
        def F(m): return m if sz > 0 else mz_(m)
        z0 = zf*sz      # mirrored build: back face parts are built at +|zf| then mirrored to -Z
        hs = [F(cap((gx, gy, z0 + .018), .065, .036 + 2*E, 14, "z")), F(box(gx - .07, gx + .07, gy - .21, gy - .12, z0 - E, z0 + .03))]
        rig.part(f"bulkhead_Gauge_housing_{side}", None, ALY, hs)
        face = [F(cap((gx, gy, z0 + .038), .055, .004 + 2*E, 16, "z"))]
        rig.part(f"bulkhead_Gauge_dial_{side}", None, SL, face)
        # green band 0..0.5 kPa (true span 1.2 deg on a 270 deg dial; drawn 4 deg so it reads) + 6 ticks
        a0g = np.radians(225)
        bnd = xf(box(.040, .052, -.003, .003, z0 + .0442, z0 + .0462), R=TF.rotation_matrix(a0g - np.radians(2), [0, 0, 1]), t=(gx, gy, 0))
        rig.part(f"bulkhead_Gauge_greenband_{side}", None, GREEN, [F(bnd)])
        ticks = [F(xf(box(.044, .053, -.0012, .0012, z0 + .0442, z0 + .0457), R=TF.rotation_matrix(a0g - np.radians(270*k/5), [0, 0, 1]), t=(gx, gy, 0))) for k in (1, 3, 5)]
        rig.part(f"bulkhead_Gauge_ticks_{side}", None, ALY, ticks)
        c = np.array([gx, gy, sz*(z0 + .049)])
        nd = [box(-.0025, .0025, -.006, .046, -.0015, .0015), cap((0, 0, 0), .007, .004, 8, "z")]
        nd = [xf(m, R=TF.rotation_matrix(np.radians(135 if sz > 0 else 225), [0, 0, 1])) for m in nd]     # needle at 0 kPa (front 225 deg from +X; back mirrored = 315 deg, reads the same from -Z)
        rig.part(f"bulkhead_Gauge_needle_{side}", None, AM, [xf(m, t=c) for m in nd], W=T(c))
        rig.part(f"bulkhead_DigitalReadout_{side}", None, GLOW, [F(box(gx - .055, gx + .055, gy - .195, gy - .135, z0 + .03 - E, z0 + .034))])
        # equalize port (valve body) + grille below the readout
        ec = (gx, b.CY - .40)
        port = [F(cap((ec[0], ec[1], z0 + .015), .06, .03 + 2*E, 14, "z"))]
        rig.part(f"bulkhead_EqualizePort_{side}", None, ALY, port)
        gr = [F(box(ec[0] - .045, ec[0] + .045, ec[1] - .033 + k*.017, ec[1] - .025 + k*.017, z0 + .030 - E, z0 + .036)) for k in range(4)]
        rig.part(f"bulkhead_EqualizeGrille_{side}", None, G, gr)
        if side == "back":
            lc = np.array([gx + .11, b.CY - .40, -(z0 + .012)])
            lv = [mz_(cap((lc[0], lc[1], z0 + .012), .016, .024 + 2*E, 10, "z")), mz_(box(lc[0] - .009, lc[0] + .009, lc[1], lc[1] + .16, z0 + .024 - E, z0 + .040)),
                  mz_(cap((lc[0], lc[1] + .16, z0 + .032), .014, .03, 8, "z"))]
            rig.part("bulkhead_EqualizeLever", None, ORANGE, lv, W=T(lc))
    # amber beacon above the door
    rig.part("bulkhead_Beacon_housing", None, ALY, [cap((0, 2.66 + b.SILL - .15, -.12 + .02), .05, .04 + 2*E, 12, "z")])
    rig.part("bulkhead_Beacon", None, STAT, [cap((0, 2.66 + b.SILL - .15, -.12 + .052), .038, .028, 12, "z")])
    if b.SILL < .1:   # accessible: bevelled 20 mm threshold plates (1:4) both sides of the collar
        th = []
        for zs in (1, -1):
            m = loft(np.array([(.0, 0), (.08, 0), (.0, b.SILL)]), [(0, 1, 1)]) if False else None
        ramp = trimesh.Trimesh(np.array([(-.40, 0, 0), (.40, 0, 0), (-.40, b.SILL, 0), (.40, b.SILL, 0), (-.40, 0, .08), (.40, 0, .08)]),
                               np.array([[0, 1, 3], [0, 3, 2], [2, 3, 5], [2, 5, 4], [0, 4, 5], [0, 5, 1], [0, 2, 4], [1, 5, 3]]), process=False)
        ramp.fix_normals(); uvp(ramp)
        th += [xf(ramp.copy(), t=(0, 0, -E)), mz_(xf(ramp.copy(), t=(0, 0, -COL_Z0 - E)))]
        rig.part("bulkhead_threshold", None, ALY, th)
    ccol = boolean("difference", [solid_rr(CW + 2*COL_OFF, CH + 2*COL_OFF, CR + COL_OFF, [(0, COL_Z0), (0, 0)], 3, (0, b.CY)), rr_prism(b, 0, -.5, .2, 3)])
    ccol = boolean("intersection", [ccol, trimesh.creation.box(bounds=[[-2, 0, -1], [2, 4, 1]])])
    rig.part("bulkhead_frame-colonly", None, G, [wall.copy(), ccol])

def leaf(rig, b):
    g = rig.group("leaf", None, T((b.HX, 0, b.HZ)))
    st = LAPW - .012
    prof = [(-PLUG_IN1, PZ0), (-PLUG_IN0, FZ0), (st, FZ0), (st, FZ0 + .015), (LAPW, FZ0 + .015), (LAPW, FZ1 - .010), (LAPW - .010, FZ1)]
    shell = solid_rr(CW, CH, CR, prof, 4, (0, b.CY))
    cuts = [rr_prism(b, -TRAY_IN, PZ0 - .01, TRAY_Z, 3)]
    for i in range(8):   # dog slots through the tray rim (dog 24 x 14 mm, 2 mm clear)
        cuts.append(place(b, box(-.045, .002, -.014, .014, DOG_Z0 - .002, DOG_Z1 + .002), i))
    shell = boolean("difference", [shell] + cuts)
    rig.part("bulkhead_leaf_shell", g, G, [shell])
    # +Z back face ribs (stiffeners) clear of the hinge straps, damper clevis, davit hanger and the hub ring
    rb = []; RZ0, RZ1 = FZ1 - E, FZ1 + .030
    ys = [b.CY - .75, b.CY - .35, b.CY + .35, b.CY + .75] if b.p["ribs"] == 4 else [b.CY - .85, b.CY - .55, b.CY - .25, b.CY + .25, b.CY + .55, b.CY + .85]
    for y in ys: rb.append(box(-.47, .33, y - .011, y + .011, RZ0, RZ1))
    for x in (-.30, .20): rb.append(box(x - .011, x + .011, b.CY - .93, b.CY + .93, RZ0, RZ1 - .004))
    if b.p["kick"]: rb.append(bplate(-.47, .33, b.CY - 1.02, b.CY - .86, RZ0, FZ1 + .012, .004))
    rig.part("bulkhead_Rib_back", g, SL, [boolean("union", rb)])
    # hub lamp ring (+Z face) on a boss
    rig.part("status_light", g, STAT, [annulus_z((0, b.CY), .125, .14, FZ1 - E, FZ1 + .008, 16)])
    # hinge straps + leaf knuckles
    hs = []
    for s0 in b.HINGES:
        y0, y1 = s0 + .10, s0 + .20
        hs += [cap((b.HX, (y0 + y1)/2, b.HZ), .05, y1 - y0, 10, "y"), bplate(.42, b.HX, y0, y1, FZ1 - E, b.HZ + .02, .010)]
    rig.part("bulkhead_HingeHeavy_leaf", g, ST, hs)
    # davit arm: knuckle on the hinge axis + top arm along the leaf's top edge toward the latch side (clear of the damper band)
    PY = b.PY; ytop = b.CY + LH/2
    da = [cap((b.HX, ytop + .006 + .039, b.HZ), .04, .078, 10, "y"), box(-.27, b.HX, ytop - E, ytop + .06, FZ0 + .004, b.HZ - .02)]
    rig.part("bulkhead_Davit_arm", g, ST, da)
    # damper leaf clevis (post on the +Z face)
    PL = b.PL
    lm = [box(PL[0] - .05, PL[0] + .05, ytop - .09, PY - .029, FZ1 - E, PL[2] + .05), box(PL[0] - .05, PL[0] + .05, PY + .029, PY + .06, PL[2] - .06, PL[2] + .07),
          box(PL[0] - .03, PL[0] + .03, PY - .029 - E, PY + .029 + E, PL[2] + .05, PL[2] + .07), cap(PL, .012, .13, 8, "y")]
    rig.part("bulkhead_leaf_damper_mount", g, ALY, lm)
    # ---- approach (-Z) plug face: gearbox hub, cam disc (lock wheel), 8 dogs + guides + linkages, OverrideOrange handwheel
    hc = (0, b.CY)
    GB_Z = LINK_Z0 - .002   # gearbox body (r 75) from just in front of the linkage plane to the handwheel; hub (r 50) through the disc to the tray floor
    gb = [cap((0, b.CY, (TRAY_Z + E + GB_Z)/2), .05, (TRAY_Z + E) - GB_Z, 12, "z"),
          cap((0, b.CY, (GB_Z + E + (-.150))/2), .075, (GB_Z + E) - (-.150), 14, "z")]
    rig.part("bulkhead_override_gearbox", g, G, gb)
    wc = np.array([0, b.CY, (DISC_Z0 + DISC_Z1)/2])
    disc = [annulus_z(hc, .054, .22, DISC_Z0, DISC_Z1, 16)]
    for k in range(4):
        a = np.radians(45 + 90*k); disc.append(xf(box(.07, .20, -.012, .012, DISC_Z1 - E, DISC_Z1 + .004), R=TF.rotation_matrix(a, [0, 0, 1]), t=(0, b.CY, 0)))
    rig.part("bulkhead_LockWheel", g, ST, disc, W=T(wc))
    hwc = np.array([0, b.CY, -.170])
    hw = place_axis(handwheel(.20, .014, 5, .04, .03, 18, 5, .018), hwc, (0, 0, 1)) + [cap((0, b.CY, (-.150 + E + -.158)/2), .022, .008 + E, 10, "z")]
    rig.part("bulkhead_OverrideOrange_Handwheel", g, ORANGE, hw, W=T(hwc))
    gd = []
    for i in range(8):
        p, ang = dog_frame(b, i); d = np.array([np.cos(ang), np.sin(ang)])
        tip = p - d*(PLUG_IN1 + .008)
        Wd = T((tip[0], tip[1], (DOG_Z0 + DOG_Z1)/2)) @ TF.rotation_matrix(ang, [0, 0, 1])
        dz = (DOG_Z1 - DOG_Z0)/2
        dog = [box(-DOG_LEN, -.006, -.012, .012, -dz, dz), box(-.006 - E, 0, -.012, .012, -dz, dz*.3)]
        rig.part(f"bulkhead_Dog_{i + 1:02d}", g, ST, [xf(m, R=Wd) for m in dog], W=Wd)
        zc = (DOG_Z0 + DOG_Z1)/2
        # guide: two cheeks standing on the tray floor + a strap across the dog's front (1.5 mm clear, 0.5 mm behind the plug face)
        zf, zs, zb = -dz - .0035, -dz - .0015, TRAY_Z + E - zc
        gd.append(xf(prism_x([(-.020, zf), (.020, zf), (.020, zb), (.014, zb), (.014, zs), (-.014, zs), (-.014, zb), (-.020, zb)], -.09, -.07), R=Wd))
        # linkage: bar from the cam-follower pin (r = 0.17 on the disc) to a riser on the dog's inner end
        inner = tip - d*(DOG_LEN - .012)
        v0 = inner - np.array(hc); pin = np.array(hc) + v0/np.linalg.norm(v0)*.17
        Lw = T((pin[0], pin[1], (LINK_Z0 + LINK_Z1)/2)) @ TF.rotation_matrix(ang, [0, 0, 1])
        v = inner - pin; L = np.linalg.norm(v); th = np.arctan2(v[1], v[0])
        bar = xf(box(0, L, -.008, .008, LINK_Z0, LINK_Z1), R=TF.rotation_matrix(th, [0, 0, 1]), t=(pin[0], pin[1], 0))
        riser = box(inner[0] - .008, inner[0] + .008, inner[1] - .008, inner[1] + .008, DOG_Z1 - E, LINK_Z0 + E)
        head = cap((pin[0], pin[1], LINK_Z0 - .003), .011, .006 + E, 6, "z")
        rig.part(f"bulkhead_Linkage_{i + 1:02d}", g, ALY, [bar, riser, head], W=Lw)
    rig.part("bulkhead_dog_guides", g, ALY, gd)
    # two convex hulls (plug + flange): one hull over both cut the reveal corner by 40 mm (Gage F-CLIP-LEAF)
    rig.part("bulkhead_leaf_plug-convcolonly", g, G, [solid_rr(CW, CH, CR, [(-PLUG_IN1, PZ0), (-PLUG_IN0, FZ0 + .002)], 3, (0, b.CY))])
    rig.part("bulkhead_leaf_flange-convcolonly", g, G, [solid_rr(CW, CH, CR, [(LAPW, FZ0 + .001), (LAPW, FZ1)], 3, (0, b.CY))])
    return g

def pistons(rig, b):
    BODY_LEN, BORE_LEN, ROD_LEN = .62, .55, .66
    PF, PL = b.PF, b.PL; d = PL - PF; psi = np.arctan2(-d[0], -d[2])
    Wb = T(PF) @ TF.rotation_matrix(psi, [0, 1, 0]); Wr = T(PL) @ TF.rotation_matrix(psi + np.pi, [0, 1, 0])
    eye = xf(ring_between(circle(.0145, 10), circle(.045, 10), -.024, .024), R=TF.rotation_matrix(-np.pi/2, [1, 0, 0]))
    shank = box(-.02, .02, -.022, .022, -BODY_LEN + BORE_LEN - .005, -.04)
    cyl = ring_between(circle(.026, 10), circle(.042, 10), -BODY_LEN, -BODY_LEN + BORE_LEN)
    endcap = cap((0, 0, -BODY_LEN + BORE_LEN + .005), .044, .02, 10, "z")
    gland = ring_between(circle(.026, 10), circle(.047, 10), -BODY_LEN, -BODY_LEN + .03)
    body = [eye, shank, cyl, endcap, gland]
    for m in body: m.fix_normals()
    rig.part("bulkhead_Damper_body", None, ST, body, world=False, W=Wb)
    reye = xf(ring_between(circle(.0145, 10), circle(.045, 10), -.024, .024), R=TF.rotation_matrix(-np.pi/2, [1, 0, 0]))
    rod = cap((0, 0, -(ROD_LEN + .04)/2), .018, ROD_LEN - .04, 10, "z"); head = cap((0, 0, -ROD_LEN + .01), .023, .02, 12, "z")
    rig.part("bulkhead_DamperRod", "leaf", ALY, [reye, rod, head], world=False, W=Wr)

def build(prm=None):
    p = params(prm); b = B(p)
    rig = Rig("door_lab_bulkhead_hatch"); frame(rig, b); leaf(rig, b); pistons(rig, b); rig.b = b; return rig

def deltas(rig, f_open=0.0, f_dog=1.0, f_seal=0.0, f_ram=0.0, mirror=False, f_eq=0.0, kpa=0.0):
    sg = -1.0 if mirror else 1.0
    phi = sg*np.radians(OPEN_DEG*f_open)
    d = {"leaf": TF.rotation_matrix(phi, [0, 1, 0]), "bulkhead_LockWheel": TF.rotation_matrix(sg*np.radians(DOG_DEG*f_dog), [0, 0, 1]),
         "bulkhead_OverrideOrange_Handwheel": TF.rotation_matrix(sg*np.radians(4320*f_dog), [0, 0, 1])}
    for i in range(8):
        d[f"bulkhead_Dog_{i + 1:02d}"] = T((sg*DOG_THROW*f_dog, 0, 0)); d[f"bulkhead_Linkage_{i + 1:02d}"] = T((sg*DOG_THROW*f_dog, 0, 0))
    if f_seal: S = np.eye(4); S[2, 2] = 1 + (SEAL_INFLATE_SCALE - 1)*f_seal; d["bulkhead_InflatableSeal"] = S
    for k in (1, 2): d[f"bulkhead_PushOffRam_{k}"] = T((0, 0, .012*f_ram))
    d["bulkhead_EqualizeLever"] = TF.rotation_matrix(-sg*np.radians(90*f_eq), [0, 0, 1])
    for fb, k in (("front", -1), ("back", 1)): d[f"bulkhead_Gauge_needle_{fb}"] = TF.rotation_matrix(sg*k*np.radians(270/110*kpa), [0, 0, 1])
    W0 = rig.pose(d); F = W0["bulkhead_Damper_body"][:3, 3]; L = W0["bulkhead_DamperRod"][:3, 3]; v = L - F
    psi_w = np.arctan2(-v[0], -v[2]); r0 = rig.N["bulkhead_DamperRod"]["W"][:3, 3] - rig.N["bulkhead_Damper_body"]["W"][:3, 3]; psi0 = np.arctan2(-r0[0], -r0[2])
    d["bulkhead_Damper_body"] = TF.rotation_matrix(psi_w - psi0, [0, 1, 0]); d["bulkhead_DamperRod"] = TF.rotation_matrix(psi_w - psi0 - phi, [0, 1, 0])
    return d

if __name__ == "__main__":
    rig = build(); sh = rig.recenter(); print("recenter shift", sh)
    gp = os.path.join(OUT_GLB, "door_lab_bulkhead_hatch.glb"); print("tris", rig.export(gp)); print("\n".join(rig.tree()))
