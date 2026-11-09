"""temp-Active batch 1 (scratch, outside repo). tt_gym_dumbbell_rack, tt_gym_bench, tt_gym_cycle, tt_rink_goal.
Uses modlib primitives/materials; output dirs redirected to scratch + rooms/temp-Active renders."""
import os, sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, "/workspace/game-project/assets/src/tennis_tower")
import modlib as ML
from modlib import *
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
_build_glb = "glb"
ML.GLB_OUT = str(HERE / _build_glb)
ML.RENDER_OUT = "/workspace/renders/tennis_tower/rooms/temp-Active"
ML._m("tt_rubber", "TT_PlayRubber_Black", (.07, .075, .08), 0, .9)
ML._m("tt_rubteal", "TT_PlayRubber_Teal", (.05, .42, .45), 0, .85)
RB, RT = "tt_rubber", "tt_rubteal"
def U(m): m.metadata["uv"] = np.zeros((len(m.vertices), 2)); return m
def col(p, name, lo, hi): p.add(name + "-convcolonly", G, U(trimesh.creation.box(bounds=[lo, hi])))
def crest(p, c, n=5, s=.12, mat=LF, nm="Leaf_Crest", dz=1):
    p.add(nm, mat, *[leaf_dir(c, (np.cos(a), 1.1, .3*dz), s, s*.45, t=.006) for a in np.linspace(.5, np.pi - .5, n)])

# ---------------- dumbbell rack: 2 angled tiers, varied bells ----------------
def rack(q):
    p = Part(); L = q["L"]; n = q["pairs"]
    for x in np.linspace(-L/2 + .04, L/2 - .04, 3):
        p.add("Frame_Legs", G, beam((x, .04 - E, -.22), (x, .90, -.14), .06, .06), beam((x, .04 - E, .24), (x, .62, .20), .06, .06),
              beam((x, .30, -.20), (x, .30, .225), .04, .04))
        p.add("Rubber_Feet", RB, box(x - .05, x + .05, 0, .04, -.30, -.16), box(x - .05, x + .05, 0, .04, .18, .32))
    tiers = ((.60, .20), (.86, -.12))
    for t, (y, z) in enumerate(tiers):
        p.add(f"Tier{t}_Rails", ST, box(-L/2, L/2, y - .035, y, z - .135, z - .095), box(-L/2, L/2, y - .035, y, z + .095, z + .135))
        p.add(f"Tier{t}_Pads", RB, box(-L/2 + .01, L/2 - .01, y - E, y + .012, z - .13, z - .10), box(-L/2 + .01, L/2 - .01, y - E, y + .012, z + .10, z + .13))
        p.add(f"Tier{t}_LED", CY if t else AM, box(-L/2 + .02, L/2 - .02, y - .03, y - .01, z + .135 - E, z + .14))
        heads, grips, bands = [], [], []
        for i in range(n):
            k = i + t*n; r = .045 + .005*k + q.get("rb", 0); w = .05 + .007*k
            cx = -L/2 + (i + .5)*L/n; yy = y + .012 + r - .006
            zo = .07 + w/2
            for s in (-1, 1):
                heads.append(tube((cx, yy, z + s*(zo - w/2)), (cx, yy, z + s*(zo + w/2)), r, q.get("seg", 10)))
                bands.append(tube((cx, yy, z + s*(zo + w/2) - s*E), (cx, yy, z + s*(zo + w/2 + .006)), r*.55, 8))
            grips.append(tube((cx, yy, z - .07 - E), (cx, yy, z + .07 + E), .016, 8))
        p.add(f"Tier{t}_Bell_Heads", RB, *heads); p.add(f"Tier{t}_Grips", ALY, *grips); p.add(f"Tier{t}_End_Caps", BA if q.get("ball") else ST, *bands)
    p.add("Ball_Finials", BA, *[node((x, .90 + .045, -.14), .05, 1) for x in (-L/2 + .04, L/2 - .04)])
    col(p, "Rack", (-L/2 - .03, 0, -.32), (L/2 + .03, 1.0, .33)); return p

# ---------------- adjustable bench: incline back, seat, leg roller ----------------
def bench(q):
    p = Part(); a = np.radians(q["incline"]); Lb = 1.0
    Rx = trimesh.transformations.rotation_matrix(a, [1, 0, 0]); piv = np.array([0, .40, -.03])
    back = lambda m: xf(m, R=Rx, t=piv)
    p.add("Frame_Weldment", G, box(-.04, .04, .10, .18, -.68, .58), box(-.03, .03, .18 - E, .27, .49, .55),
          box(-.16, .16, .37, .40, -.03, .33), box(-.035, .035, .18 - E, .37 + E, .08, .16),
          box(-.06, .06, .18 - E, .23, -.62, -.30), *[box(-.07, .07, .23 - E, .245, z - .012, z + .012) for z in (-.58, -.50, -.42, -.34)],
          back(box(-.16, .16, -.035, E, -Lb, -.02)))
    p.add("Rubber_Feet", RB, box(-.30, .30, 0, .06, .50, .60), box(-.28, .28, 0, .06, -.70, -.60))
    p.add("Feet_Steel", ST, box(-.29, .29, .06 - E, .10 + E, .51, .59), box(-.27, .27, .06 - E, .10 + E, -.69, -.61))
    p.add("Seat_Pad", RT, box(-.15, .15, .40 - E, .47, -.02, .32))
    p.add("Seat_Pad_Line", BA, box(-.015, .015, .47 - E, .474, 0, .30))
    p.add("Back_Pad", RT, back(box(-.15, .15, 0, .07, -Lb + .01, -.03)))
    p.add("Back_Pad_Line", BA, back(box(-.015, .015, .07 - E, .074, -Lb + .03, -.05)))
    sup = piv + np.array([0, np.sin(a), -np.cos(a)])*.55 - np.array([0, np.cos(a), np.sin(a)])*.035
    p.add("Strut_Hinge", ST, tube(sup + [0, E, 0], (0, .23, -.45), .022, 8))
    p.add("Roller_Axle_Hardware", ALY, tube((-.04 - E, .26, .52), (.04 + E, .26, .52), .015, 8))
    p.add("Leg_Rollers", RB, tube((-.22, .26, .52), (-.04, .26, .52), .07, 12), tube((.04, .26, .52), (.22, .26, .52), .07, 12))
    p.add("Roller_Caps", BA, tube((-.235, .26, .52), (-.22 + E, .26, .52), .05, 10), tube((.22 - E, .26, .52), (.235, .26, .52), .05, 10))
    p.add("Court_Line_LED", CY, box(-.042 - .004, -.04 + E, .12, .16, -.6, .5))
    col(p, "Bench", (-.31, 0, -.72), (.31, .5, .62))
    top = piv + np.array([0, np.sin(a), -np.cos(a)])*Lb + np.array([0, np.cos(a), np.sin(a)])*.07
    col(p, "BackPad", (-.16, .37, min(top[2], -.1)), (.16, max(top[1], .48), 0)); return p

# ---------------- indoor cycle ----------------
def cycle(q):
    p = Part(); fly = np.array([0, .32, .44]); R = .22; bb = np.array([0, .30, -.02])
    sd = np.array([0, .65, -.22]); sd /= np.linalg.norm(sd); seat = bb + sd*q.get("seat", .72)
    stem = np.array([0, q.get("bar_y", 1.08), .30]); low = bb - sd*(.18/sd[1]) + [0, -E, 0]
    stay = bb + sd*.38
    p.add("Frame_Weldment", G, box(-.30, .30, .02, .08, .40, .48), box(-.28, .28, .02, .08, -.50, -.42),
          box(-.04, .04, .08 - E, .12, -.46, .20),
          box(.03, .05, .08 - E, fly[1] + .03, fly[2] - .03, fly[2] + .03), box(-.05, -.03, .08 - E, fly[1] + .03, fly[2] - .03, fly[2] + .03),
          beam(low, seat - sd*.12, .07, .07), beam((0, .12 - E, -.42), stay, .05, .05),
          tube(bb - [.055, 0, 0], bb + [.055, 0, 0], .045, 12),
          beam(bb, stem + [0, -.016 + E, 0], .07, .07))
    p.add("Rubber_Feet", RB, *[box(x - .05, x + .05, 0, .02 + E, z - .035, z + .035) for x in (-.24, .24) for z in (.44, -.46)])
    p.add("Flywheel", ST, tube(fly - [.02, 0, 0], fly + [.02, 0, 0], R, 20))
    p.add("Flywheel_Rim_Line", AM, tube(fly + [.023, 0, 0], fly + [.026, 0, 0], .12, 16))
    p.add("Flywheel_Hub_Hardware", ST, tube(fly - [.018, 0, 0], fly + [.018, 0, 0], .045, 12))  # stay inside flywheel disc
    p.add("Fork_LED", CY, box(.05 - E, .054, .12, fly[1] - .06, fly[2] - .012, fly[2] + .012), box(-.054, -.05 + E, .12, fly[1] - .06, fly[2] - .012, fly[2] + .012))
    p.add("Crank_Axle_Hardware", ALY, *[tube(bb + [sg*(.055 - E), 0, 0], bb + [sg*.066, 0, 0], .02, 10) for sg in (-1, 1)])
    th = np.radians(q.get("crank_deg", 30)); cv = np.array([0, -np.cos(th), np.sin(th)])*.17
    cranks, pedals = [], []
    for sgn, v in ((1, cv), (-1, -cv)):
        x0, x1 = sorted((sgn*.061, sgn*.085)); e = bb + v
        cranks.append(_orient(box(x0, x1, 0, .17 + .015, -.015, .015), bb - v/.17*.015 + [0, 0, 0], e) if False else beam(bb + [sgn*.073, 0, 0], e + [sgn*.073, 0, 0], .024, .03))
        px0, px1 = sorted((sgn*.095, sgn*.20)); pedals.append(box(px0, px1, e[1] - .018, e[1] + .018, e[2] - .045, e[2] + .045))
    p.add("Crank_Arms", ALY, *cranks); p.add("Pedals", RB, *pedals)
    p.add("Pedal_Reflectors", AM, *[box(*sorted((np.sign(b.bounds[0][0] + .01)*.12, np.sign(b.bounds[0][0] + .01)*.16)), b.bounds[1][1] - E, b.bounds[1][1] + .003, b.bounds[0][2] + .01, b.bounds[0][2] + .03) for b in pedals])
    p.add("Seat_Post_Hardware", ALY, beam(seat - sd*.124, seat + [0, -.02 + E, 0], .045, .045))
    p.add("Saddle", RT, xf(prism([(.03, .16), (-.03, .16), (-.09, -.02), (-.08, -.10), (.08, -.10), (.09, -.02)], seat[1] - .02, seat[1] + .05), t=(0, 0, seat[2])))
    sy, sz = stem[1], stem[2]
    p.add("Handlebar", ALY, tube((-.24, sy, sz), (.24, sy, sz), .016, 8), tube((-.24, sy, sz - .01), (-.24, sy + .06, sz + .18), .016, 8),
          tube((.24, sy, sz - .01), (.24, sy + .06, sz + .18), .016, 8))
    dg = np.array([0, .06, .19]); dg /= np.linalg.norm(dg)
    p.add("Grips", RB, *[tube(np.array((x, sy + .06, sz + .18)) - dg*E, np.array((x, sy + .06, sz + .18)) + dg*.09, .021, 8) for x in (-.24, .24)])
    p.add("Console", SL, box(-.08, .08, sy + .016 - E, sy + .13, sz - .025, sz + .025))
    p.add("Console_Screen", CY, box(-.065, .065, sy + .03, sy + .12, sz + .025 - E, sz + .029))
    p.add("Wheels", RB, tube((-.30, .04, .53), (-.22, .04, .53), .04, 10), tube((.22, .04, .53), (.30, .04, .53), .04, 10))
    p.add("Wheel_Axle", ST, box(-.22 - E, .22 + E, .03, .05, .476, .55))
    col(p, "Cycle", (-.31, 0, -.52), (.31, 1.30, .68)); return p

# ---------------- rink goal: box-lacrosse / arena soccer, 1.83 x 1.22 m class mouth -----------
def goal(q):
    p = Part(); W, H, Dp = q["W"], q["H"], q["D"]; r = .04; yb = .045 - E; zp = -.04 + E
    p.add("Posts", AM if q.get("red") else WH, tube((-W/2, .02 - E, 0), (-W/2, H, 0), r, 12), tube((W/2, .02 - E, 0), (W/2, H, 0), r, 12),
          tube((-W/2, H - .005, 0), (W/2, H - .005, 0), r, 12), node((-W/2, H, 0), r*1.1, 1), node((W/2, H, 0), r*1.1, 1))
    hx = W/2 - .3; apex = lambda s: (s*hx, H*.55, -Dp*.5)
    p.add("Frame_Base", G, tube((-W/2, yb, zp), (-W/2, yb, -Dp), .025, 8), tube((W/2, yb, zp), (W/2, yb, -Dp), .025, 8), tube((-W/2 - .02, yb, -Dp), (W/2 + .02, yb, -Dp), .025, 8),
          tube((-hx, yb, -Dp), apex(-1), .02, 8), tube((hx, yb, -Dp), apex(1), .02, 8))
    p.add("Hoop_Hinge", G, tube((-W/2 + .035, H - .06, -.02), apex(-1), .018, 8), tube((W/2 - .035, H - .06, -.02), apex(1), .018, 8))
    p.add("Ground_Pads", RB, box(-W/2 - .06, -W/2 + .06, 0, .02, -.06, .06), box(W/2 - .06, W/2 + .06, 0, .02, -.06, .06), box(-W/2 + .1, W/2 - .1, 0, .02, -Dp - .04, -Dp + .04))
    m = q["mesh"]; cords = []; zoff = .045
    def seg(a, b): cords.append(beam(a, b, .008, .008))
    top = lambda x: (x, H - .035, -.06); mid = lambda x: (x, H*.55, -Dp*.5 + zoff); low = lambda x: (x, .06, -Dp + .09)
    xs = [x for x in np.arange(-W/2 + .08, W/2 - .05, m) if abs(abs(x) - hx) > .05]
    for x in xs: seg(top(x), mid(x)); seg(mid(x), low(x))
    for f in np.linspace(.12, .88, max(4, int(1.2/m))):
        a, b, c = map(np.array, (top(0), mid(0), low(0))); pt = a + (b - a)*f*2 if f < .5 else b + (c - b)*(f*2 - 1)
        seg((-W/2, pt[1], pt[2]), (W/2, pt[1], pt[2]))
    # side nets: closed panels in the post planes x = +-W/2 under the drape profile, open mouth at +Z
    prof = np.array([top(0), mid(0), low(0)])[:, 1:]  # (y, z) top -> low
    yz = lambda z: np.interp(-z, -prof[:, 1], prof[:, 0])
    zy = lambda y: np.interp(y, prof[::-1, 0], prof[::-1, 1])
    yb0 = .068
    for sx in (-W/2, W/2):
        seg((sx, yb0, -.06), (sx, yz(-.06), -.06)); seg((sx, yb0, -.06), (sx, yb0, zy(yb0) if yb0 > prof[2, 0] else prof[2, 1]))
        for a, b in zip(prof[:-1], prof[1:]): seg((sx, a[0], a[1]), (sx, b[0], b[1]))
        for z in np.arange(-.06 - m, prof[2, 1], -m): seg((sx, yb0, z), (sx, yz(z), z))
        for y in np.arange(yb0 + m, prof[0, 0], m): seg((sx, y, -.06), (sx, y, zy(y)))
    p.add("Net_Cord", SL, *cords)
    p.add("Net_Lead_Rope", RB, tube((-W/2 + .12, .02 + .02 - E, -Dp + .1), (W/2 - .12, .02 + .02 - E, -Dp + .1), .02, 6))
    p.add("Crease_Line_LED", CY, box(-W/2 - .1, W/2 + .1, 0, .006, .065, .1))
    col(p, "GoalFrame", (-W/2 - .06, 0, -Dp - .06), (W/2 + .06, H + .08, .1)); return p

SETS = {
 "tt_gym_dumbbell_rack": (rack, [dict(label="Rack 2.0m: 10 pairs, ball caps", L=2.0, pairs=5, ball=True, moss=True),
                                  dict(label="Rack 1.5m: 8 pairs, steel caps", L=1.5, pairs=4)]),
 "tt_gym_bench": (bench, [dict(label="Bench incline 30deg", incline=30, moss=True), dict(label="Bench flat 0deg", incline=0)]),
 "tt_gym_cycle": (cycle, [dict(label="Indoor cycle: cranks 30deg, saddle 0.72 from BB"), dict(label="Indoor cycle: cranks 75deg, low saddle 0.66, bar 1.04", crank_deg=75, seat=.66, bar_y=1.04)]),
 "tt_rink_goal": (goal, [dict(label="Box-lacrosse goal 1.22 W x 1.45 H (NLL 4 ft x 4 ft 9 in), 10 cm net", W=1.22, H=1.45, D=.9, mesh=.10),
                         dict(label="Futsal goal 3.0 W x 2.0 H (FIFA futsal), 12 cm net", W=3.0, H=2.0, D=1.0, mesh=.12, red=True)]),
}
if __name__ == "__main__":
    only = sys.argv[1:] or list(SETS); allrep = {}
    for mod in only:
        b, prm = SETS[mod]; allrep[mod] = run(mod, b, prm, title="temp-Active batch 1", names=[f"{mod}_v{i+1}" for i in range(len(prm))])
    json.dump(allrep, open("/workspace/tennis-active-work/report_batch1.json", "w"), indent=1, default=str)
