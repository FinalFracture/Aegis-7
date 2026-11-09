"""temp-Active batch 4 (scratch, outside repo): entry guard, training board + end trim, locker bay, change bench, hook rail, kettlebell + 3-bell rack.
Metal and composite only: gunmetal, alloy, rubber, slate, cyan/amber LED, pad teal. NO wood. NO planter boxes.
Imports modlib + struct_lib (read-only) for the TT palette. Do not reuse tt_climbing_panel*.

FACE_PLANE for tt_climb_train_board and tt_climb_train_trim:
  mounting back is local z=0 (flush to wall); holds/spray face toward +Z.
  Place in world with yaw=-90 so local +Z -> world +X (into boulder hall); world X of back = 94.0.
  Board width (local X) = 1.25 m; trim width = 0.25 m; height 2.4 m; depth 0.12 m
  (back at z=0, front holds to z≈+0.12). Trim is the plain frame+slate end of the 13 m run.

Entry guard: local +Z is the mat-field face, -Z the corridor face; bottom-centre pivot; min_y=0; 1.90 x 1.15 x 0.08.
Hook rail: wall back at local z=0, H pegs at y=1.5, hooks toward +Z.
"""
import os, sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, "/workspace/game-project/assets/src/tennis_tower"); sys.path.insert(0, "/workspace/game-project/assets/src/tennis_tower/structure")
import modlib as ML
from modlib import *
import struct_lib as SLB
from struct_lib import PAD
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
ML.GLB_OUT = str(HERE / 'glb')
ML.RENDER_OUT = '/workspace/renders/tennis_tower/rooms/temp-Active'
ML._m("tt_rubber", "TT_PlayRubber_Black", (.07, .075, .08), 0, .9)
ML._m("tt_rubteal", "TT_PlayRubber_Teal", (.05, .42, .45), 0, .85)
RB, RT = "tt_rubber", "tt_rubteal"
def U(m): m.metadata["uv"] = np.zeros((len(m.vertices), 2)); return m
def hull(pts): return U(trimesh.convex.convex_hull(np.asarray(pts, float)))
def col(p, name, lo, hi): p.add(name + "-convcolonly", G, U(trimesh.creation.box(bounds=[lo, hi])))
def leaves(c, n=5, s=.12):
    return [leaf_dir(c, (np.cos(a), 1.0, 0), s, s * .45, t=.006) for a in np.linspace(.5, np.pi - .5, n)]

TB_H, TB_D = 2.40, 0.12   # training board / trim: same height, same depth; back plane z=0

def hold_blob(x, y, s, seed, z_face):
    rng = np.random.default_rng(seed); pts = [(x, y, z_face - .006)]
    for ang in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        rad = s * float(rng.uniform(.7, 1.05)); zz = z_face + float(rng.uniform(.045, .070))
        pts.append((x + np.cos(ang) * rad, y + np.sin(ang) * rad * float(rng.uniform(.62, .9)), zz))
    return hull(pts)

def kb_parts(o, s, seed):
    """Rubber bell + alloy handle. Local bottom at o[1]; handle plane is local XY (readable from +Z)."""
    ox, oy, oz = o; rng = np.random.default_rng(seed); pts = []
    for ang in np.linspace(0, 2 * np.pi, 10, endpoint=False):
        c, sn = np.cos(ang), np.sin(ang); j = float(rng.uniform(.98, 1.02))
        pts += [(ox + .100 * s * c * j, oy + .045 * s, oz + .100 * s * sn * j),
                (ox + .108 * s * c, oy + .12 * s, oz + .108 * s * sn),
                (ox + .078 * s * c, oy + .185 * s, oz + .078 * s * sn),
                (ox + .044 * s * c, oy + .22 * s, oz + .044 * s * sn)]
    r = .016 * s; xh, yb, yt = .042 * s, oy + .20 * s, oy + .31 * s
    handles = [tube((ox - xh, yb, oz), (ox - xh, yt + r, oz), r, 8),
               tube((ox - xh - r, yt, oz), (ox + xh + r, yt, oz), r, 8),
               tube((ox + xh, yb, oz), (ox + xh, yt + r, oz), r, 8)]
    shoes = [box(ox - xh - .012, ox - xh + .018, yb - .012, yb + .028, oz - .016, oz + .016),
             box(ox + xh - .018, ox + xh + .012, yb - .012, yb + .028, oz - .016, oz + .016)]
    disc = tube((ox, oy, oz), (ox, oy + .04 * s, oz), .100 * s, 10)
    return hull(pts), handles, shoes, disc

def entry_guard(q):
    """Low partition, L 1.90 x H 1.15 x T 0.08. +Z mat-field face, -Z corridor. Bottom-centre, min_y=0."""
    p = Part(); L, H, T = 1.90, 1.15, .08; a, b = -L/2, L/2
    # Outer frame only — no crossing members through posts
    p.add("Frame", G,
          box(a, a + .06, .02, H, -.04, .04),
          box(b - .06, b, .02, H, -.04, .04),
          box(a + .06 - E, b - .06 + E, H - .05, H, -.035, .035),
          box(a + .08, b - .08, .50, .55, -.028, .028))
    p.add("Feet", RB, box(a, a + .07, 0, .02 + E, -.05, .05), box(b - .07, b, 0, .02 + E, -.05, .05))
    p.add("Kick", RB, box(a + .10, b - .10, 0, .08, -.03, .03))
    p.add("Panel", SL, box(a + .065, b - .065, .58, H - .055, -.010, .010))
    # LED 3 mm proud of +Z face
    p.add("LED_Edge", CY, box(a + .10, b - .10, H - .045, H - .02, .040, .048))
    p.add("Leaf_Crest", LF2, *leaves((0, H + .03, 0), n=5, s=.10))
    col(p, "EntryGuard", (a, 0, -.06), (b, H + .14, .06)); return p

def _board(q, width, mode):
    # FACE_PLANE mesh note (Frame, Spray_Face, Side_Trim, T_Nuts, Holds_Rubber, Holds_Teal, Spray_Fleck, Top_LED, -convcolonly):
    # mounting back is local z=0 (flush to wall); holds/spray face toward +Z.
    # Place yaw=-90 so local +Z -> world +X (into boulder hall); world X of back = 94.0.
    p = Part(); a, b = -width / 2, width / 2; H, D = TB_H, TB_D
    t = .026 if mode == "trim" else .04
    fz = D if mode == "trim" else .05
    p.add("Frame", G, box(a, b, 0, .05, 0, fz), box(a, b, H - .05, H, 0, fz),
          box(a, a + t, .05 - E, H - .05 + E, 0, fz), box(b - t, b, .05 - E, H - .05 + E, 0, fz),
          box(a + t - E, b - t + E, .05 - E, H - .05 + E, 0, .012))
    if mode == "trim":
        p.add("Spray_Face", SL, box(a + t + .004, b - t - .004, .06, H - .06, .07, .108))
        col(p, "TrainTrim", (a, 0, 0), (b, H, D)); return p
    z_face = .048
    p.add("Spray_Face", SL, box(a + t + .006, b - t - .006, .06, 2.345, .012 - E, z_face))
    p.add("Side_Trim", ALY, box(a + .008, a + .028, .08, 2.28, .052, .098), box(b - .028, b - .008, .08, 2.28, .052, .098))
    p.add("Top_LED", AM, box(a + t + .004, b - t - .004, 2.308, 2.340, z_face - .004, .070))
    rng = np.random.default_rng(int(q.get("seed", 1)))
    hold_xy = [(x, y) for y in (.48, 1.20, 1.90) for x in np.linspace(a + .22, b - .22, 4)]
    if mode == "dense":
        hr, ht = [], []
        for i, (x, y) in enumerate(hold_xy):
            blob = hold_blob(x, y, (.030, .042, .026, .038)[i % 4], int(q.get("seed", 1)) * 20 + i, z_face)
            (ht if i % 3 == 0 else hr).append(blob)
        p.add("Holds_Rubber", RB, *hr); p.add("Holds_Teal", RT, *ht)
        nut_xy = [(x, y) for y in (.78, 1.55, 2.12) for x in np.linspace(a + .28, b - .28, 3)]
    else:
        sl, tl = [], []
        for i in range(24):
            x = float(rng.uniform(a + .10, b - .12)); y = float(rng.uniform(.16, 2.18))
            w = float(rng.uniform(.012, .026)); h = float(rng.uniform(.008, .018))
            flake = box(x, x + w, y, y + h, z_face - E, z_face + .012)
            (sl if i % 2 == 0 else tl).append(flake)
        p.add("Spray_Fleck", SL, *sl); p.add("Spray_Fleck_Teal", RT, *tl)
        nut_xy = [(x, y) for y in np.linspace(.40, 2.05, 3) for x in np.linspace(a + .16, b - .16, 4)]
    p.add("T_Nuts_Hardware", ST, *[tube((x, y, .030), (x, y, .076), .007, 6) for x, y in nut_xy])
    col(p, "TrainBoard", (a, 0, 0), (b, H, D)); return p

def train_board(q):
    """FACE_PLANE: mounting back local z=0; holds/spray toward +Z. 1.25 x 2.4 x 0.12. Not a tt_climbing_panel."""
    return _board(q, 1.25, "dense" if q.get("dense", True) else "spray")

def train_trim(q):
    """FACE_PLANE: mounting back local z=0; plain slate face toward +Z. 0.25 x 2.4 x 0.12 end trim."""
    return _board(q, 0.25, "trim")

def locker_bay(q):
    p = Part(); W, H, D = 1.20, 2.10, .55; a, b = -W/2, W/2
    p.add("Plinth", RB, box(a + .03, b - .03, 0, .05, -D/2 + .03, D/2 - .05))
    p.add("Body", G, box(a, b, .055, H, -D/2, D/2 - .04))
    # door faces float 3 mm in front of body front (body front at D/2-.04)
    zf = D/2 - .04
    doors=[]; handles=[]
    for x0, x1 in ((-.52, -.18), (-.16, .16), (.18, .52)):
        doors.append(box(x0, x1, .14, H - .10, zf + .003, zf + .018))
        handles.append(tube((x1 - .04, 1.0, zf + .020), (x1 - .04, 1.0, zf + .045), .012, 8))
    p.add("Doors", SL, *doors)
    p.add("Handles", ALY, *handles)
    p.add("LED_Toe", CY, box(a + .05, b - .05, .06, .08, zf + .020, zf + .028))
    col(p, "Locker", (a, 0, -D/2), (b, H, D/2 + .02)); return p

def change_bench(q):
    """1.8 m long, seat depth 0.45, height 0.48. Rubber and pad slats, not wood."""
    p = Part(); L, SD, SH = 1.80, .45, .48; a, b = -L / 2, L / 2; z0, z1 = -SD / 2, SD / 2
    lx, lz = (a + .14, b - .14), (z0 + .07, z1 - .07); fr = []
    for x in lx:
        for z in lz: fr.append(box(x - .022, x + .022, .02, .40, z - .02, z + .02))
        fr.append(box(x - .022, x + .022, .16, .20, lz[0], lz[1]))
    fr += [box(a + .12, b - .12, .36, .40, z0 + .05, z0 + .09), box(a + .12, b - .12, .36, .40, z1 - .09, z1 - .05),
           box(a + .12, b - .12, .36, .40, -.02, .02)]
    p.add("Frame", G, *fr)
    p.add("Feet", RB, *[box(x - .04, x + .04, 0, .022, z - .035, z + .035) for x in lx for z in lz])
    n, gap = 5, .01; w = (SD - gap * (n - 1)) / n; z = z0; rb, pd = [], []
    for i in range(n):
        slab = box(a + .012, b - .012, .40 - E, SH, z, z + w); (rb if i % 2 == 0 else pd).append(slab); z += w + gap
    p.add("Seat_Slats_Rubber", RB, *rb); p.add("Seat_Slats_Pad", PAD, *pd)
    hk = []
    for x in np.linspace(a + .36, b - .36, 4):
        for s in (-1, 1):
            hk.append(box(x - .007, x + .007, .22, .36 + E, s * .06 - .008, s * .06 + .008))
            za, zb = s * .052, s * .12; hk.append(box(x - .007, x + .007, .20, .245, min(za, zb), max(za, zb)))
    p.add("Hooks", ALY, *hk)
    col(p, "Bench", (a, 0, z0), (b, SH, z1)); return p

def hook_rail(q):
    """Wall rail. Back plate at local z=0; H pegs at y=1.5 project toward +Z."""
    p = Part(); L = 1.50; a, b = -L / 2, L / 2; y = 1.50
    p.add("Back_Plate", G, box(a, b, y - .09, y + .09, 0, .012))
    p.add("Rail", ALY, box(a + .02, b - .02, y - .028, y + .028, .012 - E, .042))
    p.add("Mount_Bolts_Hardware", ST, *[tube((x, y + dy, .012 - E), (x, y + dy, .024), .008, 6) for x in (a + .08, 0, b - .08) for dy in (-.05, .05)])
    pegs = []
    for x in np.linspace(a + .18, b - .18, 5):
        pegs += [box(x - .046, x - .028, y - .07, y + .07, .04 - E, .09),
                 box(x + .028, x + .046, y - .07, y + .07, .04 - E, .09),
                 box(x - .046, x + .046, y - .012, y + .012, .058, .10)]
    p.add("H_Pegs", ALY, *pegs)
    col(p, "HookRail", (a, y - .09, 0), (b, y + .09, .11)); return p

def kettlebell(q):
    p = Part()
    p.add("Bell", RB, tube((0, .02, 0), (0, .17, 0), .09, 12))
    p.add("Bell_Cap", RB, tube((0, .165, 0), (0, .185, 0), .07, 10))
    p.add("Handle_Hardware", ALY, tube((-.055, .170, 0), (-.055, .275, 0), .011, 8),
          tube((.055, .170, 0), (.055, .275, 0), .011, 8), tube((-.055, .275, 0), (.055, .275, 0), .011, 8))
    p.add("Weight_Pip", AM, tube((0, .09, .088), (0, .09, .098), .01, 6))
    col(p, "KB", (-.11, 0, -.11), (.11, .29, .11)); return p

def kb_rack(q):
    p = Part(); a, b = -.55, .55
    p.add("Feet", RB, box(a, a + .08, 0, .025, -.12, .12), box(b - .08, b, 0, .025, -.12, .12))
    p.add("Rack_Frame", G,
          box(a + .02, b - .02, .025 - E, .05, -.10, .10),
          box(a + .03, a + .06, .05 - E, .40, -.08, -.04), box(b - .06, b - .03, .05 - E, .40, -.08, -.04),
          box(a + .03, a + .06, .05 - E, .40, .04, .08), box(b - .06, b - .03, .05 - E, .40, .04, .08),
          box(a + .03, b - .03, .38, .42, -.08, .08))
    p.add("Cradle_Pads", RB, box(a + .10, b - .10, .425, .445, -.06, .06))
    bells=[]; handles=[]
    for i, x in enumerate((-.32, 0.0, .32)):
        r = .08 + .008 * i
        bells.append(tube((x, .46, 0), (x, .58, 0), r, 10))
        handles += [tube((x - .045, .57, 0), (x - .045, .66, 0), .01, 6),
                    tube((x + .045, .57, 0), (x + .045, .66, 0), .01, 6),
                    tube((x - .045, .66, 0), (x + .045, .66, 0), .01, 6)]
    p.add("Bells", RB, *bells); p.add("Handles_Hardware", ALY, *handles)
    p.add("LED_Pip", CY, box(-.015, .015, .40, .415, .085, .100))
    col(p, "KBRack", (a, 0, -.13), (b, .68, .13)); return p

SETS = {
 "tt_climb_entry_guard": (entry_guard, [dict(label="Entry guard 1.90 x 1.15 x 0.08: posts, mid rail, perforated slate, cyan LED edge, leaf crest, rubber kick. +Z mat-field face, -Z corridor, bottom-centre, min_y=0")]),
 "tt_climb_train_board": (train_board, [
    dict(label="Holds-dense training board 1.25 x 2.4 x 0.12, 12 rubber/teal holds, T-nuts, side trim, amber top LED. FACE_PLANE: mounting back local z=0 (flush to wall); holds face +Z. Place yaw=-90 so local +Z -> world +X (into boulder hall); world X of back = 94.0.", dense=True, seed=1),
    dict(label="Spray-plain training board 1.25 x 2.4 x 0.12, slate spray flecks, T-nut field, side trim, amber top LED, no hold blobs. FACE_PLANE: mounting back local z=0; spray face +Z. Place yaw=-90 so local +Z -> world +X; world X of back = 94.0.", dense=False, seed=7)]),
 "tt_climb_train_trim": (train_trim, [dict(label="End trim 0.25 x 2.4 x 0.12, plain gunmetal frame and slate, no holds. FACE_PLANE: mounting back local z=0; face +Z. Place yaw=-90 so local +Z -> world +X; world X of back = 94.0.")]),
 "tt_climb_locker_bay": (locker_bay, [dict(label="Locker bay 1.2 x 2.1 x 0.55, 3 doors, alloy handles, vents, cyan LED toe, rubber plinth")]),
 "tt_climb_change_bench": (change_bench, [dict(label="Change bench 1.8 x 0.45 seat x 0.48 high, gunmetal frame, rubber/pad slats, hooks under")]),
 "tt_climb_hook_rail": (hook_rail, [dict(label="Hook rail 1.5 m, wall back at z=0, five H pegs at y=1.5 toward +Z")]),
 "tt_gym_kettlebell": (kettlebell, [dict(label="Kettlebell, rubber bell, alloy handle, gunmetal shoes, amber weight pip")]),
 "tt_gym_kb_rack": (kb_rack, [dict(label="Kettlebell rack, 3 rubber bells, gunmetal cradle, rubber pads, cyan/amber pips")]),
}
if __name__ == '__main__':
    for mod in (sys.argv[1:] or list(SETS)):
        b, prm = SETS[mod]; run(mod, b, prm, title="temp-Active batch 4", names=[f"{mod}_v{i+1}" for i in range(len(prm))])
