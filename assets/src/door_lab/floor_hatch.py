"""Rook door_lab pass C (rev 2, Vance counterbalance decision 2026-11-20): door_lab_floor_hatch.glb - flush floor hatch.
Built with the finished floor at y = 0 and the clear opening centred on X/Z, then recentred bottom-centre (the well floor is the GLB min_y),
so in the GLB the finished floor plane is y = FLOOR_Y (printed; 0.462 m for the 0.45 well). Place the GLB at (x, floor_top - FLOOR_Y, z).
  Clear column 0.90 x 0.90 m (throat + well liner), kept clear of ALL fixed hardware and of every counterbalance / stay / damper part over 0-105 deg.
  Leaf 1.00 x 1.00 x 0.10 m, top FLUSH with the continuous 1.24 x 1.24 m flange (+-0 mm), 6 mm gap all round, inflatable seal bead in the land groove.
  Hinge: full-length Oe56 hinge tube (leaf side) on the hinge axis 24 mm outboard of the leaf edge, 32 mm below the floor (tube top 4 mm under the floor),
  in an open hinge channel 69 mm wide behind the leaf; frame end bearings at both ends.
  Counterbalance (Vance): NO gas struts. 585 N m torsion bar (Oe25) inside the hinge tube, one exposed anchor clevis at each end
  (frame anchor clevis at the -X end, leaf anchor clevis on the tube's +X end cap; mirrored on LH). Rotary damper on the hinge axis, outboard (+X end),
  speed caps 77.8 deg/s opening, 33.3 deg/s closing (GLB extras + Gage metas).
  Torque model at 1 G: leaf weight moment 687 N m, torsion bar 585 N m, net ~102 N m closing at the closed position, actuator <= 530 N m; phase timing unchanged.
  Stay: on the non-hinge +X side wall (mirrored on LH), entirely in the band x 0.4515..0.482 (outside the 0.45 column): 5 x 20 mm flat-bar stay arm pinned to a
  leaf lug (x 0.4585..0.4615, inside the seal bead), foot pin in a slider running in a slot in the side-wall recess (recess 12.5 mm deep, slot to 32 mm <= 40 mm);
  folds into the recess when closed; at 105 deg the slider reaches the slot end and a spring detent plunger pops up behind it (orange release knob visible in the recess).
  4 dogs + linkages to an underside locking wheel, 4 keepers in pockets behind the liner, recessed lift handle, recessed OverrideOrange handwheel and lever.
Rig (pivots on the real axes):
  hatch_leaf                 group, origin ON the hinge axis; open = rotate about local +X by -OPEN_DEG.
  hatch_HingeTube            child of leaf (rides with it). hatch_TorsionAnchor_leaf: child of leaf (tube +X end clevis + torque arm).
  hatch_TorsionBar / hatch_TorsionAnchor_frame / hatch_HingeBearing_frame / hatch_RotaryDamper: fixed roots on the hinge axis.
  hatch_LockWheel            child of leaf; dogs thrown = rotate about local +Y by +90 deg.
  hatch_Dog_01..04 / hatch_Linkage_01..04: child of leaf; thrown = local +X 0.025 m.
  hatch_OverrideOrange_Handwheel: child of leaf, about local +Y (4320 deg = 12 turns full throw). hatch_OverrideOrange_Lever: about local +Z, +70 deg.
  hatch_InflatableSeal       root; inflate = scale local Y by SEAL_INFLATE_SCALE.
  hatch_stay_arm             child of leaf, origin on the leaf-lug pin; rotate about local X by STAY table (deg, relative to the leaf) vs opening.
  hatch_stay_slider          root, origin on the foot pin; travel along local Z by SLIDE table (m) vs opening.
  hatch_stay_detent_plunger  root, local Z = world +Y; travel along local Z by PLUNGER table (m, 0 = up/latched, -0.0085 = pressed by the slider).
  hatch_stay_detent_knob     child of the plunger (OverrideOrange pull knob, rides with it).
Run: python3 assets/src/door_lab/floor_hatch.py"""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from door_lab_lib import *

OPEN_HALF, LEAF_HALF, LT, GAP = .45, .50, .10, .006
REB = LEAF_HALF + GAP                # 0.506
FL, FLT, BODY, FD = .62, .012, .615, .20
LAND_Y = -LT - GAP                   # -0.106
GRV_I, GRV_O, GRV_D = .461, .495, .020
AX = np.array([0.0, -.032, -.524])   # hinge axis (x ignored): y, z  (32 mm below the floor so the Oe56 tube stays under the floor)
CH_Z0, CH_Y0, CH_X = -.575, -.072, .600   # open hinge channel: back wall z, floor y, half length
CH_ZF = -.488                        # under-flange extension of the channel at the bearing / damper / anchor ends (|x| > 0.495)
OPEN_DEG = 105.0
WELL = .45; WT = .006
DOG_THROW = .025
DOGS = [((-.14, .435), (0, 1)), ((.14, .435), (0, 1)), ((-.435, .30), (-1, 0)), ((.435, .30), (1, 0))]   # retracted tip (x,z), outward dir
KP_D, KP_W = .030, .022
DOG_Y0, DOG_Y1 = -.160, -.140
SEAL_Y0 = LAND_Y - GRV_D; SEAL_TOP = -LT - .0015
SEAL_INFLATE_SCALE = ((-LT + .004) - (SEAL_Y0 - .002)) / (SEAL_TOP - (SEAL_Y0 - .002))
# hinge tube / torsion bar (x layout, RH)
TUBE_RO, TUBE_RI, TUBE_X0, TUBE_X1 = .028, .022, -.490, .450
BAR_R, STUB_RO, STUB_RI, BRG_RI, BRG_RO = .0125, .019, .0155, .0215, .028
BRG_L, BRG_R, DAMP_X = (-.530, -.505), (.505, .530), (.535, .590)
ANCH_PIN_R = .030; ANCH_LEAF_BETA = 135.0; ANCH_FRAME_BETA = 200.0
# stay (RH, +X side wall)
ST_ARM_X = (.4515, .4565); ST_LUG_X = (.4585, .4615); ST_SLIDER_X = (.464, .4805)
REC_X1, SLOT_X1 = .4625, .482
ST_A = np.array([-.125, AX[2] + .25])     # leaf lug pin (y, z) closed
ST_YS, ST_L = -.145, .40                  # slider pin line y, arm length
PL_X, PL_R, PL_TRAVEL = .472, .005, .0085
TORQUE = dict(weight_moment_Nm=687.0, torsion_bar_Nm=585.0, net_closing_Nm=102.0, actuator_max_Nm=530.0)
DAMPER = dict(open_cap_dps=77.8, close_cap_dps=33.3)

def rz(m):  # XY-built (height along z) -> plan in XZ, height along +Y
    return xf(m, R=TF.rotation_matrix(-np.pi/2, [1, 0, 0]))
def sq_prism(half_o, y0, y1, r=.004, n=2):
    return rz(solid_rr(2*half_o, 2*half_o, r, [(0, y0), (0, y1)], n))
def rot_leaf(p_yz, th):  # rotate a (y,z) point about the hinge axis by the opening angle th (rad, lifting)
    dy, dz = p_yz[0] - AX[1], p_yz[1] - AX[2]; c, s = np.cos(th), np.sin(th)
    return np.array([AX[1] + dz*s + dy*c, AX[2] + dz*c - dy*s])
def ringx(ri, ro, x0, x1, seg=14, yz=None):
    """annulus about the X axis through (y, z) = yz (default: the hinge axis), from x0 to x1."""
    yz = AX[1:] if yz is None else yz
    m = ring_between(circle(ri, seg), circle(ro, seg), x0, x1)
    return xf(m, R=TF.rotation_matrix(np.pi/2, [0, 1, 0]), t=(0, yz[0], yz[1]))
def cylx(r, x0, x1, seg=14, yz=None):
    yz = AX[1:] if yz is None else yz
    return cap(((x0 + x1)/2, yz[0], yz[1]), r, x1 - x0, seg, "x")
def off(beta, rho):  # (y, z) of a point at angle beta (deg; 0 = +Z, 90 = +Y) and radius rho about the hinge axis
    b = np.radians(beta); return AX[1:] + rho*np.array([np.sin(b), np.cos(b)])
def lug_yz(c0, r0, c1, r1, x0, x1, seg=12):
    """flat plate x0..x1 whose YZ outline is the convex hull of two discs (c0, r0) and (c1, r1)."""
    from scipy.spatial import ConvexHull
    a = np.linspace(0, 2*np.pi, seg, endpoint=False); P = np.vstack([np.c_[c0[0] + r0*np.sin(a), c0[1] + r0*np.cos(a)], np.c_[c1[0] + r1*np.sin(a), c1[1] + r1*np.cos(a)]])
    H = P[ConvexHull(P).vertices]; n = len(H)
    V = [(x, y, z) for x in (x0, x1) for y, z in H]; F = []
    for j in range(n):
        k = (j + 1) % n; F += [(j, k, n + k), (j, n + k, n + j)]
    for j in range(1, n - 1): F += [(0, j + 1, j), (n, n + j, n + j + 1)]
    return mk(V, F)

# ------------------------------------------------------------------ stay kinematics (closed-form, pre-recenter coordinates)
def stay_state(th):
    """(A_yz, S_yz, arm world angle) at opening th (rad). Arm local +Z points from the lug pin A to the slider pin S."""
    A = rot_leaf(ST_A, th); dy = A[0] - ST_YS
    S = np.array([ST_YS, A[1] + np.sqrt(ST_L**2 - dy**2)]); d = S - A
    return A, S, np.arctan2(-d[0], d[1])
def stay_tables(step_deg=0.5):
    """per step: arm delta about local X (deg, relative to the leaf), slider travel along Z (m), plunger travel (m, <= 0)."""
    A0, S0, a0 = stay_state(0.0); _, Sopen, _ = stay_state(np.radians(OPEN_DEG)); zp = plunger_z(Sopen[1])
    angs = np.arange(0, OPEN_DEG + 1e-9, step_deg); arm, slide, plg = [], [], []
    for d in angs:
        th = np.radians(d); _, S, a = stay_state(th)
        arm.append(np.degrees(a - a0 + th)); slide.append(S[1] - S0[1])
        over = (S[1] + .016 > zp - PL_R - .0015) and (S[1] - .016 < zp + PL_R + .0015) and d < OPEN_DEG - 1e-6
        plg.append(-PL_TRAVEL if over else 0.0)
    return angs, np.array(arm), np.array(slide), np.array(plg)
def plunger_z(zs_open): return zs_open + .016 + .0015 + PL_R + .0005   # plunger centre just behind the slider's trailing (+Z) face at full open
def stay_extent():
    """z range used by the arm / lug below the land (recess) and the slider travel range."""
    zs, zr = [], []
    for d in np.arange(0, OPEN_DEG + 1e-9, .5):
        A, S, _ = stay_state(np.radians(d)); zs.append(S[1])
        for t in np.linspace(0, 1, 41):
            p = A + t*(S - A)
            if p[0] < -.080: zr.append(p[1])
        if A[0] < -.070: zr += [A[1] - .03, A[1] + .03]
    return min(zs), max(zs), min(zr), max(zr)

# ------------------------------------------------------------------ frame
def frame(rig):
    blk = boolean("union", [box(-FL, FL, -FLT, 0, -FL, FL), box(-BODY, BODY, -FD, -FLT + E, -BODY, BODY)])
    throat = box(-OPEN_HALF, OPEN_HALF, -1, 1, -OPEN_HALF, OPEN_HALF)
    reb = box(-REB, REB, LAND_Y, 1, -REB, REB)
    chan = box(-CH_X, CH_X, CH_Y0, 1, CH_Z0, -REB + E)
    chan_ext = [box(s*.495 if s > 0 else -CH_X, CH_X if s > 0 else -.495, CH_Y0, -.008, CH_Z0, CH_ZF) for s in (-1, 1)]
    groove = boolean("difference", [sq_prism(GRV_O, SEAL_Y0, LAND_Y + .01, .02), sq_prism(GRV_I, SEAL_Y0 - .01, LAND_Y + .02, .008)])
    pockets = []
    for (px, pz), (dx, dz) in DOGS:
        u = np.array([dx, dz]); w = np.abs(np.array([-dz, dx])); c0 = np.array([px, pz]); wall = c0 + u*(OPEN_HALF - c0 @ u)
        a, b = wall - u*.002, wall + u*KP_D; lo, hi = np.minimum(a, b) - w*KP_W, np.maximum(a, b) + w*KP_W
        pockets.append(box(lo[0], hi[0], DOG_Y0 - .008, DOG_Y1 + .010, lo[1], hi[1]))
    zs_min, zs_max, zr_min, zr_max = stay_extent(); zs_open = stay_state(np.radians(OPEN_DEG))[1][1]; zp = plunger_z(zs_open)
    rec = [box(OPEN_HALF - .001, REC_X1, -.190, LAND_Y + .02, min(zr_min, zs_min - .02) - .01, max(zr_max, zs_max + .02) + .01),          # stay recess (12.5 mm)
           box(REC_X1 - E, SLOT_X1, ST_YS - .0075, ST_YS + .0075, zs_min - .016 - .006, zs_max + .016 + .006),                                 # slider slot (to 32 mm)
           box(REC_X1 - E, SLOT_X1, -.190, ST_YS - .0075 + E, zp - .014, zp + .014)]                                                            # detent plunger pocket
    fr = boolean("difference", [blk, throat, reb, chan] + chan_ext + [groove] + pockets + rec)
    well = []
    for s in (-1, 1):
        well += [box(s*OPEN_HALF if s > 0 else -OPEN_HALF - WT, OPEN_HALF + WT if s > 0 else -OPEN_HALF, -WELL, -FD + E, -OPEN_HALF - WT, OPEN_HALF + WT),
                 box(-OPEN_HALF, OPEN_HALF, -WELL, -FD + E, s*OPEN_HALF if s > 0 else -OPEN_HALF - WT, OPEN_HALF + WT if s > 0 else -OPEN_HALF)]
    well.append(box(-OPEN_HALF - WT, OPEN_HALF + WT, -WELL - .012, -WELL + E, -OPEN_HALF - WT, OPEN_HALF + WT))
    rig.part("hatch_frame", None, G, [fr] + well)
    c = (GRV_I + GRV_O)/2; prof = [(c - .015 - OPEN_HALF, SEAL_Y0 - .002), (c + .015 - OPEN_HALF, SEAL_Y0 - .002), (c + .015 - OPEN_HALF, SEAL_TOP - .008),
                                    (c + .008 - OPEN_HALF, SEAL_TOP), (c - .008 - OPEN_HALF, SEAL_TOP), (c - .015 - OPEN_HALF, SEAL_TOP - .008)]
    bead = rz(sweep_rr(2*OPEN_HALF, 2*OPEN_HALF, .004, prof, 3))
    rig.part("hatch_InflatableSeal", None, SEAL, [bead], W=T((0, SEAL_Y0, 0)))
    kp = []
    for (px, pz), (dx, dz) in DOGS:
        u = np.array([dx, dz]); w = np.abs(np.array([-dz, dx])); c0 = np.array([px, pz]); wall = c0 + u*(OPEN_HALF - c0 @ u)
        a, b = wall + u*.002, wall + u*(KP_D - .002); lo, hi = np.minimum(a, b) - w*(KP_W - .003), np.maximum(a, b) + w*(KP_W - .003)
        k = box(lo[0], hi[0], DOG_Y1 + .002, DOG_Y1 + .0105, lo[1], hi[1])
        k.vertices[:, 1] = np.where((k.vertices[:, 1] < DOG_Y1 + .005) & ((k.vertices[:, [0, 2]] - wall) @ u < .003), DOG_Y1 + .005, k.vertices[:, 1])
        kp.append(k)
    rig.part("hatch_Keeper", None, ST, kp)
    return rig

def hinge_torsion(rig, g):
    """full-length hinge tube (leaf), frame end bearings, torsion bar, anchor clevis at each end, rotary damper outboard on the axis."""
    ay, az = AX[1], AX[2]
    # leaf: tube + end caps + -X journal stub + 4 webs welded to the leaf rear face
    tb = [ringx(TUBE_RI, TUBE_RO, TUBE_X0, TUBE_X1, 16), ringx(STUB_RI, TUBE_RO, TUBE_X0 - .006, TUBE_X0 + E, 16), ringx(STUB_RI, TUBE_RO, TUBE_X1 - E, TUBE_X1 + .006, 16),
          ringx(STUB_RI, STUB_RO, BRG_L[0] - .005, TUBE_X0 - .006 + E, 12)]
    for x in (-.42, -.14, .14, .38):
        tb += [box(x - .006, x + .006, -.066, ay - .024, -.530, -REB + E), box(x - .006, x + .006, -.095, ay - .018, -REB + .001, -LEAF_HALF + .003)]
    rig.part("hatch_HingeTube", g, ST, tb)
    # leaf anchor clevis on the +X end cap: two cheeks + pin + torque arm on the bar end + journal stub through the +X bearing into the damper
    pl = off(ANCH_LEAF_BETA, ANCH_PIN_R)
    la = [boolean("difference", [lug_yz(AX[1:], TUBE_RO - .004, pl, .008, TUBE_X1 + .004, TUBE_X1 + .012), cylx(STUB_RI + .003, TUBE_X1, TUBE_X1 + .02, 14)]), lug_yz(AX[1:], TUBE_RO*.8, pl, .008, TUBE_X1 + .036, TUBE_X1 + .042),
          cylx(.005, TUBE_X1 + .012 - E, TUBE_X1 + .036 + E, 10, pl),
          lug_yz(AX[1:], .018, pl, .0085, TUBE_X1 + .015, TUBE_X1 + .033),
          ringx(STUB_RI, STUB_RO, TUBE_X1 + .042 - E, DAMP_X[0] + .017, 12), cylx(STUB_RI + .001, TUBE_X1 + .042 - E, TUBE_X1 + .050, 12)]
    rig.part("hatch_TorsionAnchor_leaf", g, ALY, la)
    # torsion bar (fixed; the twist is invisible on a round bar): from the frame anchor hub to the leaf anchor hub (2 mm into each hub)
    rig.part("hatch_TorsionBar", None, ST, [cylx(BAR_R, -.575, TUBE_X1 + .017, 14)])
    # frame anchor clevis at the -X end: two cheeks standing on the channel floor + pin + torque arm on the bar end
    pf = off(ANCH_FRAME_BETA, ANCH_PIN_R)
    fa = [box(-.597, -.591, CH_Y0 - E, pf[0] + .010, pf[1] - .011, pf[1] + .011), box(-.567, -.561, CH_Y0 - E, pf[0] + .010, pf[1] - .011, pf[1] + .011),
          cylx(.005, -.591 - E, -.567 + E, 10, pf), lug_yz(AX[1:], .018, pf, .0085, -.585, -.573)]
    rig.part("hatch_TorsionAnchor_frame", None, ALY, fa)
    # frame end bearings (ring + foot to the channel floor)
    br = []
    for x0, x1 in (BRG_L, BRG_R):
        br += [ringx(BRG_RI, BRG_RO, x0, x1, 16), box(x0, x1, CH_Y0 - E, ay - .026, az - .024, az + .024)]
    rig.part("hatch_HingeBearing_frame", None, ST, br)
    # rotary damper housing on the axis, outboard of the +X bearing; closed outer end; saddle foot
    rd = [ringx(BRG_RI, BRG_RO, DAMP_X[0], DAMP_X[0] + .028, 16), cylx(BRG_RO, DAMP_X[0] + .028 - E, DAMP_X[1], 16), box(DAMP_X[0] + .004, DAMP_X[1] - .004, CH_Y0 - E, ay - .026, az - .024, az + .024),
          cylx(.010, DAMP_X[1] - E, DAMP_X[1] + .006, 10)]
    rig.part("hatch_RotaryDamper", None, G, rd)
    rig.extras["hatch_RotaryDamper"] = dict(DAMPER, axis="hinge", note="rotary damper speed caps (deg/s)")
    rig.extras["hatch_TorsionBar"] = dict(TORQUE, note="torsion-bar counterbalance in the hinge tube; torque model at 1 G")

def leaf(rig):
    g = rig.group("hatch_leaf", None, T((0, AX[1], AX[2])))
    shell = box(-LEAF_HALF, LEAF_HALF, -LT, 0, -LEAF_HALF, LEAF_HALF)
    cham = xf(box(-.6, .6, -.006, .006, -.006, .006), R=TF.rotation_matrix(np.pi/4, [1, 0, 0]), t=(0, 0, -LEAF_HALF))   # 4 mm hinge-edge chamfer (top)
    chamb = xf(box(-.6, .6, -.008, .008, -.008, .008), R=TF.rotation_matrix(np.pi/4, [1, 0, 0]), t=(0, -LT, -LEAF_HALF))  # 6 mm hinge-edge chamfer (underside)
    cuts = [cham, chamb, cap((0, -.0175, 0), .15, .035 + .002, 24, "y"),
            box(-.09, .09, -.035, .01, .365, .435), box(.215, .405, -.030, .01, -.235, -.165),
            cylx(TUBE_RO + .003, -.52, .52, 16)]                                    # tube scallop along the hinge edge (3 mm clearance)
    sh = boolean("difference", [shell] + cuts)
    rig.part("hatch_leaf_shell", g, G, [sh])
    hd = [cap((0, -.014, .40), .008, .17, 8, "x"), box(-.093, -.08, -.022, -.006, .392, .408), box(.08, .093, -.022, -.006, .392, .408)]
    rig.part("hatch_Handle", g, ST, hd)
    hc = np.array([0, -.016, 0])
    hw = place_axis(handwheel(.12, .009, 4, .028, .022, 18, 6, .014), hc, (0, 1, 0))
    hw.append(cap((0, -.029, 0), .02, .01, 10, "y"))
    rig.part("hatch_OverrideOrange_Handwheel", g, ORANGE, hw, W=T(hc))
    lc = np.array([.235, -.018, -.20])
    lv = [box(.235, .385, -.024, -.012, -.208, -.192), cap(tuple(lc), .007, .05, 8, "z"), box(.36, .385, -.024, -.008, -.212, -.188)]
    rig.part("hatch_OverrideOrange_Lever", g, ORANGE, lv, W=T(lc))
    wc = np.array([0, -.129, 0])
    lw = [cap((0, -.129, 0), .125, .012, 16, "y"), cap((0, -.125, 0), .035, .05 - E, 10, "y")]
    for k in range(4):
        a = np.radians(45 + 90*k); lw.append(xf(box(.036, .118, -.141, -.135 + E, -.008, .008), R=TF.rotation_matrix(a, [0, 1, 0])))
    rig.part("hatch_LockWheel", g, ST, lw, W=T(wc))
    gd = []
    for i, ((px, pz), (dx, dz)) in enumerate(DOGS):
        ang = np.arctan2(-dz, dx)
        Wd = T((px, (DOG_Y0 + DOG_Y1)/2, pz)) @ TF.rotation_matrix(ang, [0, 1, 0])
        dog = [box(-.12, -.004, -.010, .010, -.012, .012), box(-.004 - E, 0, -.010, .006, -.012, .012)]
        dog = [xf(m, R=Wd) for m in dog]
        rig.part(f"hatch_Dog_{i + 1:02d}", g, ST, dog, W=Wd)
        for m in (box(-.074, -.058, DOG_Y0 - .006 - (DOG_Y0 + DOG_Y1)/2, -LT + E - (DOG_Y0 + DOG_Y1)/2, .014, .020), box(-.074, -.058, DOG_Y0 - .006 - (DOG_Y0 + DOG_Y1)/2, -LT + E - (DOG_Y0 + DOG_Y1)/2, -.020, -.014),
                  box(-.074, -.058, DOG_Y0 - .006 - (DOG_Y0 + DOG_Y1)/2, DOG_Y0 - .002 - (DOG_Y0 + DOG_Y1)/2, -.020, .020)):
            gd.append(xf(m, R=Wd))
        inner = np.array([px, pz]) - np.array([dx, dz])*.110
        pin = inner/np.linalg.norm(inner)*.085
        Lw = np.array(T((pin[0], -.115, pin[1])) @ TF.rotation_matrix(ang, [0, 1, 0]))
        v = inner - pin; L = np.linalg.norm(v); th = np.arctan2(-v[1], v[0])
        bar = xf(box(0, L, -.005, .005, -.008, .008), R=TF.rotation_matrix(th, [0, 1, 0]), t=(pin[0], -.115, pin[1]))
        riser = box(inner[0] - .008, inner[0] + .008, DOG_Y1 - E, -.112 + E, inner[1] - .008, inner[1] + .008)
        pinm = cap((pin[0], (-.121 - .112)/2, pin[1]), .007, .009, 8, "y")
        rig.part(f"hatch_Linkage_{i + 1:02d}", g, ALY, [bar, riser, pinm], W=Lw)
    rig.part("hatch_dog_guides", g, ALY, gd)
    rig.part("hatch_leaf-convcolonly", g, G, [box(-LEAF_HALF, LEAF_HALF, -LT, 0, -LEAF_HALF, LEAF_HALF)])
    return g

def stay(rig, g):
    """side-wall stay: leaf lug, arm (leaf child, origin on the lug pin), slider (root), detent housing / plunger / knob."""
    A0, S0, a0 = stay_state(0.0); _, So, _ = stay_state(np.radians(OPEN_DEG)); zp = plunger_z(So[1])
    xm = sum(ST_ARM_X)/2; hx = (ST_ARM_X[1] - ST_ARM_X[0])/2
    # leaf lug: plate hanging from the underside (8 mm into the shell), bore 5.5 mm round the arm pin
    lug = boolean("difference", [box(ST_LUG_X[0], ST_LUG_X[1], A0[0] - .012, -LT + .008, A0[1] - .014, A0[1] + .014), cylx(.0055, ST_LUG_X[0] - .01, ST_LUG_X[1] + .01, 12, A0)])
    rig.part("hatch_stay_leaf_lug", g, ST, [lug])
    # arm (local: origin on the lug pin, +Z toward the slider pin, flat bar 5 x 20 mm with round ends, pins as part of the arm)
    W = T((xm, A0[0], A0[1])) @ TF.rotation_matrix(a0, [1, 0, 0])
    arm = [box(-hx, hx, -.010, .010, 0, ST_L), cap((0, 0, 0), .011, 2*hx, 12, "x"), cap((0, 0, ST_L), .011, 2*hx, 12, "x"),
           cap(((ST_LUG_X[1] - .0005 - xm + (-hx))/2, 0, 0), .004, ST_LUG_X[1] - .0005 - xm + hx, 10, "x"),
           cap(((ST_SLIDER_X[1] - .001 - xm + (-hx))/2, 0, ST_L), .004, ST_SLIDER_X[1] - .001 - xm + hx, 10, "x")]
    rig.part("hatch_stay_arm", g, ST, arm, world=False, W=W)
    # slider in the slot (bore round the foot pin)
    sl = boolean("difference", [box(ST_SLIDER_X[0], ST_SLIDER_X[1], -.006, .006, -.016, .016), cylx(.0055, ST_SLIDER_X[0] - .01, ST_SLIDER_X[1] + .01, 12, (0, 0))])
    rig.part("hatch_stay_slider", None, ALY, [sl], world=False, W=T((0, ST_YS, S0[1])))
    # detent: housing ring under the slot, plunger (local Z = world +Y), orange pull knob in the recess
    rig.part("hatch_stay_detent_housing", None, ST, [ring_y(PL_R + .0015, PL_R + .0045, -.168, ST_YS - .0075 - .0015, (PL_X, zp)),
                                                     box(PL_X + PL_R + .003, SLOT_X1 + .0015, -.166, -.157, zp - .005, zp + .005)])
    Wp = T((PL_X, ST_YS - .0075 + .007, zp)) @ TF.rotation_matrix(-np.pi/2, [1, 0, 0])   # origin at the plunger top centre (latched), local +Z = world +Y
    rig.part("hatch_stay_detent_plunger", None, ST, [cap((0, 0, -.012), PL_R, .024, 10, "z")], world=False, W=Wp)
    knob = [cap((0, 0, -.026), .0025, .006, 8, "z"), box(OPEN_HALF + .0025 - PL_X, .0025, -.004, .004, -.033, -.027)]
    rig.part("hatch_stay_detent_knob", "hatch_stay_detent_plunger", ORANGE, knob, world=False, W=Wp)
    rig.extras["hatch_stay_arm"] = dict(axis="local X", note="angle table (deg, relative to the leaf) vs leaf opening; see door_lab_passC.py / Gage stay_table meta")

def ring_y(ri, ro, y0, y1, xz, seg=12):
    m = ring_between(circle(ri, seg), circle(ro, seg), y0, y1)
    return xf(m, R=TF.rotation_matrix(-np.pi/2, [1, 0, 0]), t=(xz[0], 0, xz[1]))

def build(prm=None):
    """prm: well = well depth below the floor (V1/V2 0.45, V3/V4 0.75 step-down service well, V5 0.30 shallow)."""
    global WELL
    prm = prm or {}; WELL = float(prm.get("well", .45))
    rig = Rig("door_lab_floor_hatch"); rig.extras = {}
    frame(rig); g = leaf(rig); hinge_torsion(rig, g); stay(rig, g)
    col = [box(-FL, FL, -FD, 0, -FL, CH_Z0), box(-FL, FL, -FD, CH_Y0, CH_Z0, -REB), box(-FL, -CH_X, -FD, 0, CH_Z0, -REB), box(CH_X, FL, -FD, 0, CH_Z0, -REB),
           box(-FL, FL, -FD, 0, REB, FL), box(-FL, -REB, -FD, 0, -REB, REB), box(REB, FL, -FD, 0, -REB, REB),
           box(-OPEN_HALF - WT, OPEN_HALF + WT, -WELL - .012, -WELL, -OPEN_HALF - WT, OPEN_HALF + WT)]
    for s in (-1, 1):
        col += [box(s*OPEN_HALF - (WT if s < 0 else 0), s*OPEN_HALF + (WT if s > 0 else 0), -WELL, -FD, -OPEN_HALF - WT, OPEN_HALF + WT),
                box(-OPEN_HALF, OPEN_HALF, -WELL, -FD, s*OPEN_HALF - (WT if s < 0 else 0), s*OPEN_HALF + (WT if s > 0 else 0))]
    rig.part("hatch_frame-colonly", None, G, col)
    angs, arm, slide, plg = stay_tables(.5)
    rig.meta = dict(stay_len=ST_L, stay_tables=dict(step_deg=.5, arm_deg=arm.tolist(), slide_m=slide.tolist(), plunger_m=plg.tolist()))
    return rig

def _interp(tab, f):
    u = np.clip(f, 0, 1)*(len(tab) - 1); i = min(int(np.floor(u)), len(tab) - 2); return tab[i] + (tab[i + 1] - tab[i])*(u - i)

def deltas(rig, f_open=0.0, f_dog=1.0, f_seal=0.0, mirror=False, f_lever=0.0, exact=True):
    """mirror=True for the LH (X-mirrored) variants: rotations about local Y/Z and translations along local X flip sign
    (the leaf, the stay arm about X and the slider / plunger along Z do not). exact=True evaluates the stay closed-form, False uses the 0.5 deg tables (as Godot)."""
    sg = -1.0 if mirror else 1.0
    th = np.radians(OPEN_DEG*f_open)
    d = {"hatch_leaf": TF.rotation_matrix(-th, [1, 0, 0]), "hatch_LockWheel": TF.rotation_matrix(sg*np.radians(90*f_dog), [0, 1, 0]),
         "hatch_OverrideOrange_Handwheel": TF.rotation_matrix(sg*np.radians(4320*f_dog), [0, 1, 0]),
         "hatch_OverrideOrange_Lever": TF.rotation_matrix(sg*np.radians(70*f_lever), [0, 0, 1])}
    for i in range(4): d[f"hatch_Dog_{i + 1:02d}"] = T((sg*DOG_THROW*f_dog, 0, 0)); d[f"hatch_Linkage_{i + 1:02d}"] = T((sg*DOG_THROW*f_dog, 0, 0))
    if f_seal: S = np.eye(4); S[1, 1] = 1 + (SEAL_INFLATE_SCALE - 1)*f_seal; d["hatch_InflatableSeal"] = S
    st = rig.meta["stay_tables"]
    if exact:
        A0, S0, a0 = stay_state(0.0); _, S, a = stay_state(th); arm, slide = np.degrees(a - a0 + th), S[1] - S0[1]
        _, So, _ = stay_state(np.radians(OPEN_DEG)); zp = plunger_z(So[1])
        over = (S[1] + .016 > zp - PL_R - .0015) and (S[1] - .016 < zp + PL_R + .0015) and f_open < 1 - 1e-9
        plg = -PL_TRAVEL if over else 0.0
    else:
        arm, slide, plg = _interp(st["arm_deg"], f_open), _interp(st["slide_m"], f_open), _interp(st["plunger_m"], f_open)
    d["hatch_stay_arm"] = TF.rotation_matrix(np.radians(arm), [1, 0, 0]); d["hatch_stay_slider"] = T((0, 0, slide)); d["hatch_stay_detent_plunger"] = T((0, 0, plg))
    return d

def finalize(rig):
    sh = rig.recenter(); rig.meta["shift"] = sh
    rig.meta["floor_y"] = float(sh[1]); return sh

if __name__ == "__main__":
    rig = build(); sh = finalize(rig); print("recenter shift", sh, "floor_y", rig.meta["floor_y"])
    print("stay", stay_state(0.0), stay_state(np.radians(OPEN_DEG)), stay_extent())
    gp = os.path.join(OUT_GLB, "door_lab_floor_hatch.glb"); print("tris", rig.export(gp)); print("\n".join(rig.tree()))
