"""Rook door_lab pass C: door_lab_floor_hatch.glb - flush floor hatch (Vance REALISM_SPEC section 4.6 + 4.7 hatch items, section 9 FAIL list).
Built with the finished floor at y = 0 and the clear opening centred on X/Z, then recentred bottom-centre (the well floor is the GLB min_y),
so in the GLB the finished floor plane is y = FLOOR_Y (printed; 0.462 m). Place the GLB at (x, floor_top - FLOOR_Y, z).
  Clear opening 0.90 x 0.90 m (throat + well liner), leaf 1.00 x 1.00 x 0.10 m with its top FLUSH with the floor (+-0 mm) inside a continuous
  frame flange (1.24 x 1.24 m, flush), 6 mm leaf-to-frame gap all round, inflatable seal bead in a land groove, 105 deg swing about a concealed
  hinge axis on the -Z edge (axis 24 mm outboard of the leaf edge, 16 mm below the floor, knuckles in a 36 mm hinge channel).
  2 gas struts (585 N m total counterbalance, ~2.03 kN each at a 0.144 m closed arm, 1.58 stroke ratio, 556 -> 877 mm), stay arm on a frame pin whose
  roller runs in a slotted track under the leaf and drops into a V detent at full open, coaxial rotary damper at the hinge, 4 dogs + linkages to an underside locking wheel, 4 keepers in pockets behind the throat liner (no fixed hardware inside the 0.90 clear opening), recessed lift handle,
  recessed OverrideOrange handwheel (12 turns full throw) and OverrideOrange manual lever.
Rig (all pivots on the real axes; values after the recenter are printed by the QA script):
  hatch_leaf               group, origin ON the hinge axis; open = rotate about local +X by -OPEN_DEG (lifts the +Z edge; Gage sign -1).
  hatch_LockWheel          child of leaf, origin on its axis; dogs thrown = rotate about local +Y by +90 deg.
  hatch_Dog_01..04         child of leaf, origin at the retracted dog tip, local +X = throw direction; thrown = +X 0.025 m.
  hatch_Linkage_01..04     child of leaf, origin at the cam-follower pin; thrown = same +0.025 m along its dog's axis (local +X).
  hatch_OverrideOrange_Handwheel  child of leaf, origin on axis; manual drive = rotate about local +Y (12 turns = 4320 deg for full throw).
  hatch_OverrideOrange_Lever      child of leaf, origin on its pin; lift = rotate about local +Z by +70 deg.
  hatch_InflatableSeal     root, origin on the groove floor; inflate = scale local Y by SEAL_INFLATE_SCALE (deflated as modelled).
  hatch_strut_L/R_body     root, origin on the frame clevis pin, body along local +Z toward the rod; aim at the rod origin (rotate about local X).
  hatch_strut_L/R_rod      child of leaf, origin on the leaf clevis pin, rod along local +Z toward the body; aim at the body origin.
  hatch_stay_arm           root, origin on the frame pin; rotate about local X so its roller stays on the leaf track (angle table in the QA json).
Run: python3 assets/src/door_lab/floor_hatch.py"""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from door_lab_lib import *

OPEN_HALF, LEAF_HALF, LT, GAP = .45, .50, .10, .006
REB = LEAF_HALF + GAP                # 0.506
FL, FLT, BODY, FD = .62, .012, .56, .20
LAND_Y = -LT - GAP                   # -0.106
GRV_I, GRV_O, GRV_D = .461, .495, .020
AX = np.array([0.0, -.016, -.524])   # hinge axis (x ignored): y, z
CH_Z0, CH_Y0 = -.542, -.040          # hinge channel back wall / floor
KR = .014                            # knuckle radius (top 2 mm below the floor)
OPEN_DEG = 105.0
WELL = .45; WT = .006
HINGES = (-.30, .30)
DOG_THROW = .025
DOGS = [((-.14, .435), (0, 1)), ((.14, .435), (0, 1)), ((-.435, .30), (-1, 0)), ((.435, .30), (1, 0))]   # retracted tip (x,z), outward dir
KP_D, KP_W = .030, .022             # keeper pockets in the throat walls: depth beyond the 0.45 liner face, half width (dogs never enter the 0.90 clear opening as fixed hardware)
DOG_Y0, DOG_Y1 = -.160, -.140
SEAL_Y0 = LAND_Y - GRV_D; SEAL_TOP = -LT - .0015
SEAL_INFLATE_SCALE = ((-LT + .004) - (SEAL_Y0 - .002)) / (SEAL_TOP - (SEAL_Y0 - .002))
STRUT_X = .34; SF = np.array([-.16, -.38]); SL_DZ = .70; SL_Y = -.16    # frame pin (y,z); leaf pin dz from axis, y (searched: 1.58 stroke ratio)
BODY_LEN, ROD_LEN, BODY_R, ROD_R, BORE_R = .42, .50, .020, .007, .0085
STAY_X, STAY_PF, STAY_LEN = .42, np.array([-.15, -.37]), .37               # stay arm frame pin (y,z), length (searched)
TRACK_DY = -LT - .026                                                     # roller track line under the leaf (closed-pose y)

def rz(m):  # XY-built (height along z) -> plan in XZ, height along +Y
    return xf(m, R=TF.rotation_matrix(-np.pi/2, [1, 0, 0]))
def sq_prism(half_o, y0, y1, r=.004, n=2):
    return rz(solid_rr(2*half_o, 2*half_o, r, [(0, y0), (0, y1)], n))
def leaf_pt(dz, y):  # closed-pose world point of a leaf feature given dz from the axis
    return np.array([y, AX[2] + dz])
def rot_leaf(p_yz, th):  # rotate a (y,z) point about the hinge axis by the opening angle th (rad, lifting)
    dy, dz = p_yz[0] - AX[1], p_yz[1] - AX[2]; c, s = np.cos(th), np.sin(th)
    return np.array([AX[1] + dz*s + dy*c, AX[2] + dz*c - dy*s])

def frame(rig):
    blk = boolean("union", [box(-FL, FL, -FLT, 0, -FL, FL), box(-BODY, BODY, -FD, -FLT + E, -BODY, BODY)])
    throat = box(-OPEN_HALF, OPEN_HALF, -1, 1, -OPEN_HALF, OPEN_HALF)
    reb = box(-REB, REB, LAND_Y, 1, -REB, REB)
    chan = box(-.40, .40, CH_Y0, 1, CH_Z0, -REB + E)
    groove = boolean("difference", [sq_prism(GRV_O, SEAL_Y0, LAND_Y + .01, .02), sq_prism(GRV_I, SEAL_Y0 - .01, LAND_Y + .02, .008)])
    pockets = []
    for (px, pz), (dx, dz) in DOGS:
        u = np.array([dx, dz]); w = np.abs(np.array([-dz, dx])); c0 = np.array([px, pz]); wall = c0 + u*(OPEN_HALF - c0 @ u)
        a, b = wall - u*.002, wall + u*KP_D; lo, hi = np.minimum(a, b) - w*KP_W, np.maximum(a, b) + w*KP_W
        pockets.append(box(lo[0], hi[0], DOG_Y0 - .008, DOG_Y1 + .010, lo[1], hi[1]))
    fr = boolean("difference", [blk, throat, reb, chan, groove] + pockets)
    well = []
    for s in (-1, 1):
        well += [box(s*OPEN_HALF if s > 0 else -OPEN_HALF - WT, OPEN_HALF + WT if s > 0 else -OPEN_HALF, -WELL, -FD + E, -OPEN_HALF - WT, OPEN_HALF + WT),
                 box(-OPEN_HALF, OPEN_HALF, -WELL, -FD + E, s*OPEN_HALF if s > 0 else -OPEN_HALF - WT, OPEN_HALF + WT if s > 0 else -OPEN_HALF)]
    well.append(box(-OPEN_HALF - WT, OPEN_HALF + WT, -WELL - .012, -WELL + E, -OPEN_HALF - WT, OPEN_HALF + WT))
    rig.part("hatch_frame", None, G, [fr] + well)
    # seal bead (30 mm section, embedded 2 mm in the groove floor, top 1.5 mm under the leaf when deflated)
    c = (GRV_I + GRV_O)/2; prof = [(c - .015 - OPEN_HALF, SEAL_Y0 - .002), (c + .015 - OPEN_HALF, SEAL_Y0 - .002), (c + .015 - OPEN_HALF, SEAL_TOP - .008),
                                    (c + .008 - OPEN_HALF, SEAL_TOP), (c - .008 - OPEN_HALF, SEAL_TOP), (c - .015 - OPEN_HALF, SEAL_TOP - .008)]
    bead = rz(sweep_rr(2*OPEN_HALF, 2*OPEN_HALF, .004, prof, 3))
    rig.part("hatch_InflatableSeal", None, SEAL, [bead], W=T((0, SEAL_Y0, 0)))
    # keepers: steel striker plates on the pocket ceilings (2 mm over the thrown dog, 3 mm lead-in at the throat edge); pockets 30 mm deep
    kp = []
    for (px, pz), (dx, dz) in DOGS:
        u = np.array([dx, dz]); w = np.abs(np.array([-dz, dx])); c0 = np.array([px, pz]); wall = c0 + u*(OPEN_HALF - c0 @ u)
        a, b = wall + u*.002, wall + u*(KP_D - .002); lo, hi = np.minimum(a, b) - w*(KP_W - .003), np.maximum(a, b) + w*(KP_W - .003)
        k = box(lo[0], hi[0], DOG_Y1 + .002, DOG_Y1 + .0105, lo[1], hi[1])
        k.vertices[:, 1] = np.where((k.vertices[:, 1] < DOG_Y1 + .005) & ((k.vertices[:, [0, 2]] - wall) @ u < .003), DOG_Y1 + .005, k.vertices[:, 1])
        kp.append(k)
    rig.part("hatch_Keeper", None, ST, kp)
    # frame hinge knuckles in the channel (2 per hinge) + brackets to the channel floor
    hk = []
    for cx in HINGES:
        for x0, x1 in ((cx - .077, cx - .037), (cx + .037, cx + .077)):
            hk += [cap(((x0 + x1)/2, AX[1], AX[2]), KR, x1 - x0, 10, "x"), box(x0, x1, CH_Y0 - E, AX[1], AX[2] - .010, AX[2] + .010)]
    rig.part("hatch_HingeHeavy_frame", None, ST, hk)
    # coaxial rotary damper housing (centre of the hinge line) on a channel-floor saddle
    rd = [cap((0, AX[1], AX[2]), KR, .14, 12, "x"), box(-.06, .06, CH_Y0 - E, AX[1] - .006, AX[2] - .012, AX[2] + .012)]
    for s in (-1, 1): rd.append(cap((s*.074, AX[1], AX[2]), KR*.55, .008, 8, "x"))
    rig.part("hatch_RotaryDamper", None, G, rd)
    # gas-strut frame clevises on the hinge-side throat wall
    br = []
    for s in (-1, 1):
        x = s*STRUT_X
        for dx in (-.024, .014): br.append(box(x + dx, x + dx + .010, SF[0] - .022, SF[0] + .022, -OPEN_HALF - E, SF[1] + .012))
        br.append(cap((x, SF[0], SF[1]), .006, .052, 8, "x"))
    rig.part("hatch_frame_strut_clevis", None, ST, br)
    return rig

def track_s(th):
    """leaf-local distance from the hinge axis (dz) of the stay roller on the leaf track at opening angle th (rad)."""
    ss = np.linspace(.03, 1.0, 2000)
    P = np.array([rot_leaf(np.array([TRACK_DY, AX[2] + q]), th) for q in ss])
    dd = np.linalg.norm(P - STAY_PF, axis=1) - STAY_LEN
    i = np.where(np.sign(dd[:-1]) != np.sign(dd[1:]))[0][0]; f = dd[i]/(dd[i] - dd[i + 1]); return ss[i] + f*(ss[i + 1] - ss[i])

def stay_frame(rig):
    """frame-side stay pivot bracket on the +X throat wall."""
    x = STAY_X; y, z = STAY_PF
    br = [box(x + .018, OPEN_HALF + E, y - .03, y + .03, z - .025, z + .025), cap((x + .008, y, z), .006, .036, 8, "x")]
    rig.part("hatch_stay_pivot_bracket", None, ST, br)

def stay_track(rig, g, s_closed, s_open):
    """slotted roller track under the leaf with a V detent notch where the roller sits at full open."""
    z0, z1 = AX[2] + s_open - .035, AX[2] + s_closed + .03
    rails = [box(STAY_X - .016, STAY_X - .010, TRACK_DY - .016, -LT + E, z0, z1), box(STAY_X + .010, STAY_X + .016, TRACK_DY - .016, -LT + E, z0, z1),
             box(STAY_X - .016, STAY_X + .016, TRACK_DY - .016, -LT + E, z1 - E, z1 + .012),
             box(STAY_X - .010 - E, STAY_X - .0075, TRACK_DY - .016, TRACK_DY - .011, z0, z1), box(STAY_X + .0075, STAY_X + .010 + E, TRACK_DY - .016, TRACK_DY - .011, z0, z1)]   # running lips
    tr = boolean("union", rails)
    notch = xf(box(-.05, .05, -.007, .007, -.007, .007), R=TF.rotation_matrix(np.pi/4, [1, 0, 0]), t=(STAY_X, TRACK_DY - .016, AX[2] + s_open))
    rig.part("hatch_stay_track_detent", g, ALY, [boolean("difference", [tr, notch])])

def leaf(rig):
    g = rig.group("hatch_leaf", None, T((0, AX[1], AX[2])))
    shell = box(-LEAF_HALF, LEAF_HALF, -LT, 0, -LEAF_HALF, LEAF_HALF)
    cham = xf(box(-.6, .6, -.006, .006, -.006, .006), R=TF.rotation_matrix(np.pi/4, [1, 0, 0]), t=(0, 0, -LEAF_HALF))   # 4 mm hinge-edge chamfer
    cuts = [cham, cap((0, -.0175, 0), .15, .035 + .002, 24, "y"),               # handwheel recess 35 mm deep
            box(-.09, .09, -.035, .01, .365, .435),                            # lift-handle recess
            box(.215, .405, -.030, .01, -.235, -.165)]                         # lever recess
    for cx in HINGES:                                                           # notches for the frame knuckles
        for x0, x1 in ((cx - .079, cx - .035), (cx + .035, cx + .079)): cuts.append(box(x0, x1, -.04, .01, -LEAF_HALF - .01, -LEAF_HALF + .012))
    cuts.append(box(-.072, .072, -.04, .01, -LEAF_HALF - .01, -LEAF_HALF + .012))  # rotary damper notch
    sh = boolean("difference", [shell] + cuts)
    rig.part("hatch_leaf_shell", g, G, [sh])
    # leaf knuckles + straps (rotate with the leaf about the axis)
    lk = []
    for x0, x1 in [(cx - .035 + .002, cx + .035 - .002) for cx in HINGES] + [(.082, .118), (-.118, -.082)]:
        lk += [cap(((x0 + x1)/2, AX[1], AX[2]), KR, x1 - x0, 10, "x"), box(x0, x1, AX[1] - .011, AX[1] + .011, AX[2], -LEAF_HALF + .010)]
    rig.part("hatch_HingeHeavy_leaf", g, ST, lk)
    # lift handle bail in its recess
    hd = [cap((0, -.014, .40), .008, .17, 8, "x")] + [box(s*.09 - .004*(s > 0), s*.09 + .004*(s < 0), -.034, -.006, .392, .408) for s in (-1, 1)]
    hd = [cap((0, -.014, .40), .008, .17, 8, "x"), box(-.093, -.08, -.022, -.006, .392, .408), box(.08, .093, -.022, -.006, .392, .408)]
    rig.part("hatch_Handle", g, ST, hd)
    # OverrideOrange handwheel (recessed, top 6 mm below the floor) on a hub boss
    hc = np.array([0, -.016, 0])
    hw = place_axis(handwheel(.12, .009, 4, .028, .022, 18, 6, .014), hc, (0, 1, 0))
    hw.append(cap((0, -.029, 0), .02, .01, 10, "y"))
    rig.part("hatch_OverrideOrange_Handwheel", g, ORANGE, hw, W=T(hc))
    # OverrideOrange manual lever in its recess, pin at the -X end
    lc = np.array([.235, -.018, -.20])
    lv = [box(.235, .385, -.024, -.012, -.208, -.192), cap(tuple(lc), .007, .05, 8, "z"), box(.36, .385, -.024, -.008, -.212, -.188)]
    rig.part("hatch_OverrideOrange_Lever", g, ORANGE, lv, W=T(lc))
    # underside: locking wheel (cam disc + hub), dogs, linkages, guides
    wc = np.array([0, -.129, 0])
    lw = [cap((0, -.129, 0), .125, .012, 16, "y"), cap((0, -.125, 0), .035, .05 - E, 10, "y")]
    for k in range(4):
        a = np.radians(45 + 90*k); lw.append(xf(box(.036, .118, -.141, -.135 + E, -.008, .008), R=TF.rotation_matrix(a, [0, 1, 0])))
    rig.part("hatch_LockWheel", g, ST, lw, W=T(wc))
    gd = []
    for i, ((px, pz), (dx, dz)) in enumerate(DOGS):
        ang = np.arctan2(-dz, dx)                                             # rotation about Y taking +X to (dx, 0, dz)
        Wd = T((px, (DOG_Y0 + DOG_Y1)/2, pz)) @ TF.rotation_matrix(ang, [0, 1, 0])
        dog = [box(-.12, -.004, -.010, .010, -.012, .012), box(-.004 - E, 0, -.010, .006, -.012, .012)]
        dog = [xf(m, R=Wd) for m in dog]
        rig.part(f"hatch_Dog_{i + 1:02d}", g, ST, dog, W=Wd)
        for m in (box(-.074, -.058, DOG_Y0 - .006 - (DOG_Y0 + DOG_Y1)/2, -LT + E - (DOG_Y0 + DOG_Y1)/2, .014, .020), box(-.074, -.058, DOG_Y0 - .006 - (DOG_Y0 + DOG_Y1)/2, -LT + E - (DOG_Y0 + DOG_Y1)/2, -.020, -.014),
                  box(-.074, -.058, DOG_Y0 - .006 - (DOG_Y0 + DOG_Y1)/2, DOG_Y0 - .002 - (DOG_Y0 + DOG_Y1)/2, -.020, .020)):
            gd.append(xf(m, R=Wd))
        # linkage: cam-follower pin at r = 0.085 toward the dog's inner end, bar at y -0.122..-0.112, riser onto the dog
        inner = np.array([px, pz]) - np.array([dx, dz])*.110
        pin = inner/np.linalg.norm(inner)*.085
        Lw = np.array(T((pin[0], -.115, pin[1])) @ TF.rotation_matrix(ang, [0, 1, 0]))
        v = inner - pin; L = np.linalg.norm(v); th = np.arctan2(-v[1], v[0])
        bar = xf(box(0, L, -.005, .005, -.008, .008), R=TF.rotation_matrix(th, [0, 1, 0]), t=(pin[0], -.115, pin[1]))
        riser = box(inner[0] - .008, inner[0] + .008, DOG_Y1 - E, -.112 + E, inner[1] - .008, inner[1] + .008)
        pinm = cap((pin[0], (-.121 - .112)/2, pin[1]), .007, .009, 8, "y")
        rig.part(f"hatch_Linkage_{i + 1:02d}", g, ALY, [bar, riser, pinm], W=Lw)
    rig.part("hatch_dog_guides", g, ALY, gd)
    # strut + stay clevises under the leaf
    lc_ = []
    sl = leaf_pt(SL_DZ, SL_Y)
    for s in (-1, 1):
        x = s*STRUT_X
        for dx in (-.024, .014): lc_.append(box(x + dx, x + dx + .010, sl[0] - .025, -LT + E, sl[1] - .025, sl[1] + .025))
        lc_.append(cap((x, sl[0], sl[1]), .006, .052, 8, "x"))
    rig.part("hatch_leaf_clevises", g, ALY, lc_)
    rig.part("hatch_leaf-convcolonly", g, G, [box(-LEAF_HALF, LEAF_HALF, -LT, 0, -LEAF_HALF, LEAF_HALF)])
    return g

def struts(rig):
    sl = leaf_pt(SL_DZ, SL_Y)
    for tag, s in (("L", -1), ("R", 1)):
        x = s*STRUT_X; F = np.array([x, SF[0], SF[1]]); L = np.array([x, sl[0], sl[1]]); d = L - F
        a = np.arctan2(-d[1], d[2]); Wb = T(F) @ TF.rotation_matrix(a, [1, 0, 0]); Wr = T(L) @ TF.rotation_matrix(a + np.pi, [1, 0, 0])
        eye = xf(ring_between(circle(.0075, 10), circle(.016, 10), -.012, .012), R=TF.rotation_matrix(np.pi/2, [0, 1, 0]))
        body = [eye, cap((0, 0, .022), .010, .016, 8, "z"), cap((0, 0, .036), BODY_R, .016, 12, "z"),
                ring_between(circle(BORE_R, 12), circle(BODY_R, 12), .044 - E, BODY_LEN), ring_between(circle(BORE_R, 12), circle(BODY_R + .002, 12), BODY_LEN - .012, BODY_LEN)]
        for m in body: m.fix_normals()
        rig.part(f"hatch_strut_{tag}_body", None, G, body, world=False, W=Wb)
        reye = xf(ring_between(circle(.0075, 10), circle(.014, 10), -.0115, .0115), R=TF.rotation_matrix(np.pi/2, [0, 1, 0]))
        rod = [reye, cap((0, 0, .02), .009, .016, 8, "z"), cap((0, 0, (.028 + ROD_LEN)/2), ROD_R, ROD_LEN - .028, 8, "z"), cap((0, 0, ROD_LEN - .006), .007, .008, 10, "z")]
        rig.part(f"hatch_strut_{tag}_rod", "hatch_leaf", ALY, rod, world=False, W=Wr)

def stay(rig):
    """stay arm: root node, origin on the frame pin, arm along local +Z to the roller in the leaf track."""
    s0 = track_s(0.0); Q = np.array([STAY_X, TRACK_DY, AX[2] + s0]); P = np.array([STAY_X, STAY_PF[0], STAY_PF[1]]); d = Q - P
    a = np.arctan2(-d[1], d[2]); W = T(P) @ TF.rotation_matrix(a, [1, 0, 0]); L = np.linalg.norm(d)
    arm = [xf(ring_between(circle(.0075, 10), circle(.014, 10), -.006, .006), R=TF.rotation_matrix(np.pi/2, [0, 1, 0])),
           box(-.006, .006, -.008, .008, .011, L - .011), xf(ring_between(circle(.0036, 8), circle(.0098, 10), -.0055, .0055), R=TF.rotation_matrix(np.pi/2, [0, 1, 0]), t=(0, 0, L)),
           cap((0, 0, L), .0034, .0175, 8, "x")]
    for m in arm: m.fix_normals()
    rig.part("hatch_stay_arm", None, ST, arm, world=False, W=W)
    return s0

def build(prm=None):
    """prm: well = well depth below the floor (V1/V2 0.45, V3/V4 0.75 step-down service well, V5 0.30 shallow)."""
    global WELL
    prm = prm or {}; WELL = float(prm.get("well", .45))
    rig = Rig("door_lab_floor_hatch"); frame(rig); stay_frame(rig)
    g = leaf(rig); struts(rig); s0 = stay(rig); s1 = track_s(np.radians(OPEN_DEG)); stay_track(rig, g, s0, s1)
    col = [box(-FL, FL, -FD, 0, -FL, -REB), box(-FL, FL, -FD, 0, REB, FL), box(-FL, -REB, -FD, 0, -REB, REB), box(REB, FL, -FD, 0, -REB, REB),
           box(-OPEN_HALF - WT, OPEN_HALF + WT, -WELL - .012, -WELL, -OPEN_HALF - WT, OPEN_HALF + WT)]
    for s in (-1, 1):
        col += [box(s*OPEN_HALF - (WT if s < 0 else 0), s*OPEN_HALF + (WT if s > 0 else 0), -WELL, -FD, -OPEN_HALF - WT, OPEN_HALF + WT),
                box(-OPEN_HALF, OPEN_HALF, -WELL, -FD, s*OPEN_HALF - (WT if s < 0 else 0), s*OPEN_HALF + (WT if s > 0 else 0))]
    rig.part("hatch_frame-colonly", None, G, col)
    rig.meta = dict(stay_len=STAY_LEN, stay_track=(s0, s1))
    return rig

def deltas(rig, f_open=0.0, f_dog=1.0, f_seal=0.0, mirror=False, f_lever=0.0):
    """mirror=True for the LH (X-mirrored) variants: rotations about local Y/Z and translations along local X flip sign (leaf about X does not)."""
    sg = -1.0 if mirror else 1.0
    th = np.radians(OPEN_DEG*f_open)
    d = {"hatch_leaf": TF.rotation_matrix(-th, [1, 0, 0]), "hatch_LockWheel": TF.rotation_matrix(sg*np.radians(90*f_dog), [0, 1, 0]),
         "hatch_OverrideOrange_Handwheel": TF.rotation_matrix(sg*np.radians(4320*f_dog), [0, 1, 0]),
         "hatch_OverrideOrange_Lever": TF.rotation_matrix(sg*np.radians(70*f_lever), [0, 0, 1])}
    for i in range(4): d[f"hatch_Dog_{i + 1:02d}"] = T((sg*DOG_THROW*f_dog, 0, 0)); d[f"hatch_Linkage_{i + 1:02d}"] = T((sg*DOG_THROW*f_dog, 0, 0))
    if f_seal: S = np.eye(4); S[1, 1] = 1 + (SEAL_INFLATE_SCALE - 1)*f_seal; d["hatch_InflatableSeal"] = S
    # struts: re-aim body and rod at each other (rotation about local X)
    W0 = rig.pose(d)
    for tag in "LR":
        F = W0[f"hatch_strut_{tag}_body"][:3, 3]; L = W0[f"hatch_strut_{tag}_rod"][:3, 3]; v = L - F
        a_w = np.arctan2(-v[1], v[2]); r0 = rig.N[f"hatch_strut_{tag}_rod"]["W"][:3, 3] - rig.N[f"hatch_strut_{tag}_body"]["W"][:3, 3]; a0 = np.arctan2(-r0[1], r0[2])
        d[f"hatch_strut_{tag}_body"] = TF.rotation_matrix(a_w - a0, [1, 0, 0]); d[f"hatch_strut_{tag}_rod"] = TF.rotation_matrix(a_w - a0 + th, [1, 0, 0])
    # stay arm (root): aim at its roller on the leaf track
    Pw = W0["hatch_stay_arm"][:3, 3]; sh = rig.meta.get("shift", np.zeros(3)); q = track_s(th)
    Qyz = rot_leaf(np.array([TRACK_DY, AX[2] + q]), th) + sh[1:]
    v = np.array([0, Qyz[0] - Pw[1], Qyz[1] - Pw[2]]); a_w = np.arctan2(-v[1], v[2]); r0 = rig.meta["stay_dir0"]; a0 = np.arctan2(-r0[1], r0[2])
    d["hatch_stay_arm"] = TF.rotation_matrix(a_w - a0, [1, 0, 0])
    return d

def finalize(rig):
    sh = rig.recenter(); rig.meta["shift"] = sh
    W = rig.N["hatch_stay_arm"]["W"]; rig.meta["stay_dir0"] = W[:3, :3] @ np.array([0, 0, 1.0])
    rig.meta["floor_y"] = float(sh[1]); return sh

if __name__ == "__main__":
    rig = build(); sh = finalize(rig); print("recenter shift", sh, "floor_y", rig.meta["floor_y"])
    gp = os.path.join(OUT_GLB, "door_lab_floor_hatch.glb"); print("tris", rig.export(gp)); print("\n".join(rig.tree()))
