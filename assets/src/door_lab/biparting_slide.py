"""Rook door_lab: door_lab_biparting_slide.glb - bi-parting pocket slider (Gage door-lab sprint 2026-11-20).
Dimensions/gaps per Vance context/door_lab/REALISM_SPEC.md section 1 (clear 2.00 W x 2.30 H above a 16 mm threshold plate, leaves
1.05 W class x 2.40 H x 0.05 T, travel 1.000 m, gaps 6 / 15 / 8 / 10 / 50 mm, 2 x 12 mm meeting bulbs compressed 3 mm),
materials per Sloane AESTHETIC_SPEC section 1 (pearl faces + graphite inset, alloy stiles/track, gunmetal frame, rubber seals, cyan reveal).
Rig: leaf_L / leaf_R slide along X (leaf_L -X, leaf_R +X) by TRAVEL; leaf origin = closed position on the track line
(leaf centre X, running-rail top Y, Z 0). roller_* = wheels, children of their leaf, origin on the axle (axle along Z,
spin = travel / r). Fixed: frame, threshold, top_track, drive_belt, status_light, reveal_strips, frame-colonly.
Run: python3 assets/src/door_lab/biparting_slide.py"""
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from door_lab_lib import *

TH = .016                            # threshold plate top (finished floor of the opening)
CW, CHT = 2.00, 2.30                 # clear width / clear height above TH
HW = CW / 2
LAP = .025                           # leaf lap behind each jamb lip when closed
LT = .025                            # leaf half thickness (0.05 T)
LEAF_BOT = TH + .008; LEAF_TOP = LEAF_BOT + 2.40
SEAL_W, SEAL_COMP = .012, .003       # meeting bulbs (each), total compression when closed
MOUTH_Z = LT + .006                  # jamb pocket-mouth faces (6 mm)
LIN_Z = LT + .015                    # pocket liner (15 mm)
FZ1 = .075                           # outer face of the pocket walls / head box (150 D)
TRAVEL = 1.000
END_X = HW + LAP + TRAVEL + .050     # pocket end liner (50 mm behind the tail at full open)
SOF_Y = LEAF_TOP + .010              # soffit underside (10 mm)
RAIL_Y0, RAIL_Y1 = SOF_Y + .036, SOF_Y + .048
ROLLER_R = .030; ROLLER_Y = RAIL_Y1 + ROLLER_R + .002
UP_Y0 = ROLLER_Y + .049              # upper (anti-lift) rail underside
AL_R = .015; AL_Y = UP_Y0 - AL_R - .002
BELT_LO, BELT_HI = UP_Y0 + .022, UP_Y0 + .062
CAP_Y0 = BELT_HI + .03; CAP_Y1 = CAP_Y0 + .05

def mz(m):
    m = xf(m.copy(), R=np.diag([1, 1, -1, 1])); m.fix_normals(); return m
def both(m): return [m, mz(m)]

def leaf(rig, tag, s):
    inner = -(SEAL_W - SEAL_COMP/2) if s < 0 else (SEAL_W - SEAL_COMP/2)
    tail = s*(HW + LAP); a, b = sorted((tail, inner))
    g = rig.group(f"leaf_{tag}", None, T(((a + b)/2, RAIL_Y1, 0)))
    st_in = (inner - .045, inner) if s < 0 else (inner, inner + .045)
    st_tl = (a, a + .04) if s < 0 else (b - .04, b)
    core0, core1 = (st_tl[1] - E, st_in[0] + E) if s < 0 else (st_in[1] - E, st_tl[0] + E)
    rig.part(f"leaf_{tag}_core", g, SL, [bplate(core0, core1, LEAF_BOT, LEAF_TOP, -.021, .021, .004)])
    # pearl face frame (both faces): stiles-side borders, top/bottom rails, mid rail -> graphite centre insets read 4 mm recessed
    f0, f1 = core0 + E + .002, core1 - E - .002; pf = []          # 2 mm shadow line to the stiles
    for (x0, x1, y0, y1) in ((f0, f0 + .11, LEAF_BOT + .004, LEAF_TOP - .004), (f1 - .11, f1, LEAF_BOT + .004, LEAF_TOP - .004),
                             (f0 + .11 - E, f1 - .11 + E, LEAF_TOP - .16, LEAF_TOP - .004), (f0 + .11 - E, f1 - .11 + E, LEAF_BOT + .004, LEAF_BOT + .20),
                             (f0 + .11 - E, f1 - .11 + E, LEAF_BOT + 1.13, LEAF_BOT + 1.25)):
        pf += both(bplate(x0, x1, y0, y1, .021 - E, LT, .003))
    rig.part(f"leaf_{tag}_face", g, PEARL, pf)
    st = [bplate(*st_in, LEAF_BOT, LEAF_TOP, -LT, LT, .004), bplate(*st_tl, LEAF_BOT, LEAF_TOP, -LT, LT, .004)]
    rig.part(f"leaf_{tag}_stiles", g, ALY, st)
    # meeting bulb seal 12 mm (tip 1.5 mm past the centre line -> 3 mm total compression when closed)
    sc = (inner + SEAL_W/2 - .002) if s < 0 else (inner - SEAL_W/2 + .002)
    sl = xf(loft(rrect(SEAL_W + .004, .022, .0079, 3), [(LEAF_BOT + .02 + .003*(s > 0), 1, 1), (LEAF_TOP - .02 - .003*(s > 0), 1, 1)]), t=(sc, 0, 0))   # R ends 3 mm short: no coplanar end caps
    rig.part(f"leaf_{tag}_seal", g, SEAL, [sl])
    # bottom guide shoes (run in the 14 x 12 floor channel, 2 mm each side / 2 mm off its floor)
    shoes = [box(x - .05, x + .05, TH - .010, LEAF_BOT + E, -.005, .005) for x in ((a + .12, b - .30) if s < 0 else (a + .30, b - .12))]
    # carriages: hanger up the 20 mm soffit slot, bridge forward, carriage plate in front of the rail holding 2 x d60 rollers + anti-lift roller
    car = []
    for k, cx in enumerate((a + .18, b - .18)):
        car += [box(cx - .04, cx + .04, LEAF_TOP - E, SOF_Y + .024, -.006, .006), box(cx - .04, cx + .04, SOF_Y + .016, SOF_Y + .028, -.006, .036),
                bplate(cx - .085, cx + .085, SOF_Y + .016, AL_Y + .022, .026, .036, .004)]
        for dx in (-.05, .05): car.append(cap((cx + dx, ROLLER_Y, .021), .008, .010 + 2*E, 8, "z"))
        car.append(cap((cx, AL_Y, .021), .006, .010 + 2*E, 8, "z"))
        for dx in (-.05, .05):
            c = (cx + dx, ROLLER_Y, 0); n = f"roller_{tag}{k}{'ab'[dx > 0]}"
            rig.part(n, g, SEAL, [annulus_z(c, .011, ROLLER_R, -.008, .016, 10)], W=T(c))
        c = (cx, AL_Y, 0); rig.part(f"roller_{tag}{k}_antilift", g, SEAL, [annulus_z(c, .009, AL_R, -.004, .016, 10)], W=T(c))
    # belt clamp bracket: leaf L grips the upper belt run, leaf R the lower run (mirrored motion); jaws clear the belt by 1 mm
    cx = (a + .18) if s < 0 else (b - .18); by = BELT_HI if s < 0 else BELT_LO
    car += [box(cx - .03, cx + .03, AL_Y + .022 - E, by + .016, .026, .036), box(cx - .03, cx + .03, by + .006, by + .016, .036 - E, .062),
            box(cx - .03, cx + .03, by - .016, by - .006, .036 - E, .062), box(cx - .03, cx + .03, by - .016, by + .016, .058, .062)]
    rig.part(f"leaf_{tag}_carriages", g, ALY, car + shoes)
    rig.part(f"leaf_{tag}-convcolonly", g, G, [box(a, b, LEAF_BOT, LEAF_TOP, -LT, LT)])

def frame(rig):
    fr = []; X1 = END_X + .10
    for s in (-1, 1):
        x0, x1 = sorted((s*HW, s*X1))
        for zs in (1, -1):
            parts = [box(x0, x1, 0, SOF_Y + .012, LIN_Z, FZ1 - .02)]          # pocket wall plate (liner face at 15 mm)
            px0, px1 = (x0 + .22, x1 - .12) if s > 0 else (x0 + .12, x1 - .22)
            for y0, y1 in ((.12, .90), (1.00, 1.90), (2.00, SOF_Y - .06)):
                parts.append(bplate(px0, px1, y0, y1, FZ1 - .02 - E, FZ1, .010))
            for k in range(3):
                yy = 1.29 + k*.14; parts.append(box(px0 + .10, px1 - .10, yy, yy + .05, FZ1 - E, FZ1 + .012))
            for xx in (px0 + .045, px1 - .045):
                for yy in (.16, SOF_Y - .10): parts.append(cap((xx, yy, FZ1 + .004), .011, .014, 6, "z"))
            fr += parts if zs > 0 else [mz(p) for p in parts]
        ex0, ex1 = sorted((s*END_X, s*X1))                                     # end post
        fr += [bplate(ex0, ex1, 0, CAP_Y1, -FZ1 - .02, 0, .012, front=False), bplate(ex0, ex1, 0, CAP_Y1, -E, FZ1 + .02, .012)]
        jx0, jx1 = sorted((s*HW, s*(HW + .16)))                                # jamb trims + pocket-mouth lips (6 mm to the leaf)
        for zs in (1, -1):
            j = bplate(jx0, jx1, 0, SOF_Y + .012, FZ1 - E, FZ1 + .035, .012); fr.append(j if zs > 0 else mz(j))
            lx0, lx1 = sorted((s*HW, s*(HW + .045))); l = box(lx0, lx1, TH - E, SOF_Y + .012, MOUTH_Z, LIN_Z + E); fr.append(l if zs > 0 else mz(l))   # sits on the threshold cheek
    # lintel (leaf laps 108 mm behind it, 15 mm liner gap), soffit plates either side of the 20 mm carriage slot
    for zs in (1, -1):
        for p in (box(-HW - E, HW + E, TH + CHT, SOF_Y + .012, LIN_Z, FZ1 - .02), bplate(-HW + .02, HW - .02, TH + CHT + .006, SOF_Y + .006, FZ1 - .02 - E, FZ1, .008),
                  box(-END_X, END_X, SOF_Y, SOF_Y + .012, .010, LIN_Z + E)):
            fr.append(p if zs > 0 else mz(p))
    # head box: back wall (track side) full height, front left open as the track window, top cap
    fr.append(mz(box(-END_X, END_X, SOF_Y + .012 - E, CAP_Y0 + E, LIN_Z, FZ1 - .02)))
    fr.append(bplate(-X1, X1, CAP_Y0, CAP_Y1, -FZ1 - .02, FZ1 + .02, .012))
    # rubber end-stop bumpers in each pocket (25 mm off the tail at full open)
    for s in (-1, 1):
        bx0, bx1 = sorted((s*(END_X + E), s*(END_X - .025))); fr += [box(bx0, bx1, y - .04, y + .04, -.015, .015) for y in (.6, 1.8)]
    for p in fr: p.fix_normals()
    rig.part("frame", None, G, [p for p in fr])
    # threshold plate with the 14 x 12 floor channel (real cut: two plates + channel floor), bevelled leading edges
    thr = []; XO = HW - .002; XP = END_X - .002
    for zs in (1, -1):
        p = uvp(trimesh.creation.box(bounds=[[-XO, 0, .007], [XO, TH, .20]])); bev = box(-XO, XO, 0, TH*.5, .20 - E, .23)
        pk = [box(-XP, -XO + E, 0, TH, .007, LIN_Z - .002), box(XO - E, XP, 0, TH, .007, LIN_Z - .002)]   # in-pocket channel cheeks
        thr += [p, bev] + pk if zs > 0 else [mz(p), mz(bev)] + [mz(q) for q in pk]
    thr.append(box(-XP, XP, 0, TH - .012, -.007 - E, .007 + E))
    rig.part("threshold", None, ALY, thr)
    # top track: running rail, anti-lift upper rail, back web into the back liner, motor/gearbox, end tensioner pulleys
    tr = [box(-END_X + .01, END_X - .01, RAIL_Y0, RAIL_Y1, -.044, .019), box(-END_X + .01, END_X - .01, UP_Y0, UP_Y0 + .012, -.044, .019),
          box(-END_X + .01, END_X - .01, RAIL_Y0, UP_Y0 + .012, -LIN_Z - E, -.032)]
    tr += [bplate(-.12, .12, UP_Y0 + .012 - E, CAP_Y0 + .002, -LIN_Z - E, .020, .006, front=True)]
    for s in (-1, 1): tr.append(cap((s*(END_X - .08), (BELT_LO + BELT_HI)/2, .045), (BELT_HI - BELT_LO)/2 - .002, .016, 12, "z"))
    for s in (-1, 1): tr.append(box(s*(END_X - .08) - .012, s*(END_X - .08) + .012, (BELT_LO + BELT_HI)/2 - .012, CAP_Y0 + E, .030 - E, .037))
    rig.part("top_track", None, ALY, tr)
    belt = [box(-END_X + .08, END_X - .08, BELT_LO - .003, BELT_LO + .003, .040, .054), box(-END_X + .08, END_X - .08, BELT_HI - .003, BELT_HI + .003, .040, .054)]
    rig.part("drive_belt", None, SEAL, belt)
    # status lamp (one per door, header, both faces) + cyan reveal strips (soffit + both jambs, 10 mm)
    rig.part("status_light", None, STAT, both(box(-.6, .6, SOF_Y - .05, SOF_Y - .035, FZ1 - E, FZ1 + .004)))
    rv = both(box(-HW + .02, HW - .02, TH + CHT - .002, TH + CHT + E, .047, .057))     # under the lintel (the visible head soffit)
    for s in (-1, 1):
        x0, x1 = sorted((s*(HW + .03), s*(HW + .04))); rv += both(box(x0, x1, .12, TH + CHT - .05, FZ1 + .035 - E, FZ1 + .039))
    rig.part("reveal_strips", None, REV, rv)
    col = []
    for s in (-1, 1):
        x0, x1 = sorted((s*HW, s*X1)); col += [box(x0, x1, 0, CAP_Y1, MOUTH_Z, FZ1), box(x0, x1, 0, CAP_Y1, -FZ1, -MOUTH_Z)]
    col += [box(-HW, HW, TH + CHT, CAP_Y1, MOUTH_Z, FZ1), box(-HW, HW, TH + CHT, CAP_Y1, -FZ1, -MOUTH_Z), box(-X1, X1, SOF_Y + .012, CAP_Y1, -FZ1, FZ1)]
    rig.part("frame-colonly", None, G, col)

def build():
    rig = Rig("door_lab_biparting_slide"); frame(rig); leaf(rig, "L", -1); leaf(rig, "R", 1); return rig

def deltas(f):   # f = 0 closed .. 1 open
    d = {"leaf_L": T((-TRAVEL*f, 0, 0)), "leaf_R": T((TRAVEL*f, 0, 0))}
    for tag, sg in (("L", 1), ("R", -1)):
        for k in (0, 1):
            for x in "ab": d[f"roller_{tag}{k}{x}"] = T(yaw=sg*TRAVEL*f/ROLLER_R, axis=(0, 0, 1))
            d[f"roller_{tag}{k}_antilift"] = T(yaw=-sg*TRAVEL*f/AL_R, axis=(0, 0, 1))
    return d

if __name__ == "__main__":
    rig = build(); sh = rig.recenter(); print("recenter shift", sh)
    gp = os.path.join(OUT_GLB, "door_lab_biparting_slide.glb"); tris = rig.export(gp); print("tris", tris)
    print("\n".join(rig.tree()))
