"""temp-Active pass 4 (scratch, outside repo): rink rubber surface panels + futsal 40x20 line set, gym mirror / floor tile /
treadmill / rower, moss berm + green wall. Reuses modlib (read-only) + batch2 helpers."""
import sys, numpy as np
sys.dont_write_bytecode = True
from build_batch2 import *
import modlib as ML
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
ML.GLB_OUT = str(HERE / 'glb')
ML.RENDER_OUT = '/workspace/renders/tennis_tower/rooms/temp-Active'
ML._m("tt_rinkrub", "TT_RinkRubber_Slate", (.17, .22, .26), 0, .85); RR = "tt_rinkrub"
ML._m("tt_mirror", "TT_MirrorOpaque", (.93, .95, .96), 1.0, .03); MI = "tt_mirror"   # opaque reflective, no alpha
WH, ALY, LF, LF2 = "tt_white", "tt_alloy", "tt_leaf", "tt_leaf2"
from shapely.geometry import Polygon, Point, box as sbox
from shapely.ops import unary_union
def ext(poly, y0, y1):  # shapely polygon in (x, z) -> prism y0..y1
    m = trimesh.creation.extrude_polygon(poly, y1 - y0)
    m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0])); m.apply_translation((0, y1, 0))
    v = m.vertices; m.metadata["uv"] = np.c_[v[:, 0], v[:, 2]]; return m
def arc(cx, cz, r, w, a0, a1, n=24):
    t = np.linspace(a0, a1, n); o = [(cx + (r + w/2)*np.cos(a), cz + (r + w/2)*np.sin(a)) for a in t]
    i = [(cx + (r - w/2)*np.cos(a), cz + (r - w/2)*np.sin(a)) for a in t[::-1]]; return Polygon(o + i)
ST_T = .012
def surf_panel(q):
    p = Part(); W, D = q["W"], q["D"]
    p.add("Rubber_Surface", RR, box(-W/2, W/2, 0, ST_T, -D/2, D/2)); col(p, "Surface", (-W/2, 0, -D/2), (W/2, ST_T, D/2)); return p
def surf_corner(q):
    p = Part(); R = q["R"]; poly = Point(0, 0).buffer(R, 64).intersection(sbox(0, 0, R, R))
    p.add("Rubber_Surface", RR, ext(poly, 0, ST_T)); col(p, "Surface", (0, 0, 0), (R, ST_T, R)); return p
LW, LT = .08, .006
def futsal(q):
    hx, hz = 20.0, 10.0; g = []
    g += [sbox(-hx, -hz, hx, -hz + LW), sbox(-hx, hz - LW, hx, hz), sbox(-hx, -hz, -hx + LW, hz), sbox(hx - LW, -hz, hx, hz)]
    g += [sbox(-LW/2, -hz, LW/2, hz), Point(0, 0).buffer(3.0, 48).difference(Point(0, 0).buffer(3.0 - LW, 48)), Point(0, 0).buffer(.10, 16)]
    for s in (-1, 1):
        gx = s*hx  # goal line outer edge; distances measured from goal line
        for zp in (-1.5, 1.5):
            if s < 0: a0, a1 = (0, np.pi/2) if zp > 0 else (-np.pi/2, 0)
            else: a0, a1 = (np.pi/2, np.pi) if zp > 0 else (np.pi, 3*np.pi/2)
            g.append(arc(gx, zp, 6.0 - LW/2, LW, a0, a1, 20))
        lx = gx - s*(6.0 - LW/2); g.append(sbox(lx - LW/2, -1.5, lx + LW/2, 1.5))
        g += [Point(gx - s*6.0, 0).buffer(.06, 12), Point(gx - s*10.0, 0).buffer(.06, 12)]
        for zc in (-1, 1):
            a0 = {(1, 1): np.pi, (1, -1): np.pi/2, (-1, 1): 3*np.pi/2, (-1, -1): 0}[(s, zc)]
            g.append(arc(s*hx, zc*hz, .25, LW, a0, a0 + np.pi/2, 8))
        for d in (5.0, 10.0): g.append(sbox(s*d - .04, hz - .4, s*d + .04, hz))   # substitution zone marks (bench side, inside half)
    u = unary_union(g).intersection(sbox(-hx, -hz, hx, hz)); p = Part()
    ps = []
    for gg in g:
        gg = gg.intersection(sbox(-hx, -hz, hx, hz))
        ps += [ext(pg, 0, LT) for pg in (gg.geoms if hasattr(gg, "geoms") else [gg]) if pg.area > 1e-5]
    p.add("Line_Paint", WH, *ps); return p
def mirror(q):
    p = Part(); W, H = q["W"], q["H"]; y0 = .30
    p.add("Kick_Plinth", RB, box(-W/2, W/2, 0, y0, -.06, .03))
    p.add("Frame", G, box(-W/2, W/2, y0 - E, y0 + .04, -.04, .02), box(-W/2, W/2, y0 + H - .04, y0 + H, -.04, .02),
          box(-W/2, -W/2 + .04, y0 + .04 - E, y0 + H - .04 + E, -.04, .02), box(W/2 - .04, W/2, y0 + .04 - E, y0 + H - .04 + E, -.04, .02))
    p.add("Mirror_Sheet", MI, box(-W/2 + .036, W/2 - .036, y0 + .036, y0 + H - .036, -.006, .006))
    p.add("Backer_Plate", G, box(-W/2 + .045, W/2 - .045, y0 + .045, y0 + H - .045, -.035, -.008))
    p.add("Crest_LED", AM, box(-W/2 + .06, W/2 - .06, y0 + H - .03, y0 + H - .01, .02 - E, .028))
    if q.get("crest"):
        p.add("Leaf_Crest", LF, *[leaf_dir((x, y0 + H - E, -.01), (np.sign(x)*.6, 1, 0), .14, .06, t=.006) for x in (-.12, -.05, .05, .12)])
    col(p, "Mirror", (-W/2, 0, -.06), (W/2, y0 + H, .03)); return p
def floor_tile(q):
    p = Part(); S, T = 1.0, .02
    if q.get("stripe"):
        p.add("Rubber_Tile", RB, box(-S/2, S/2, 0, T, -S/2, -.06), box(-S/2, S/2, 0, T, .06, S/2))
        p.add("Lane_Inlay", RR, box(-S/2 + .001, S/2 - .001, .001, T + .002, -.06 + .001, .06 - .001))
    else:
        p.add("Rubber_Tile", RB, box(-S/2, S/2, 0, T, -S/2, S/2))
        rng = np.random.default_rng(5)
        p.add("Fleck_Inlay", SL, *[box(x - .012, x + .012, T - .003, T + .0015, z - .012, z + .012) for x, z in rng.uniform(-.45, .45, (14, 2))])
    col(p, "Tile", (-S/2, 0, -S/2), (S/2, T, S/2)); return p
def treadmill(q):
    p = Part(); BT = .20
    p.add("Frame_Rails", G, box(-.32, -.28, .06, .18, -.95, .85 + E), box(.28, .32, .06, .18, -.95, .85 + E))
    p.add("Cross_Members", ST, box(-.28 - E, .28 + E, .08, .12, -.6, -.55), box(-.28 - E, .28 + E, .08, .12, .3, .35))
    p.add("Feet", RB, *[box(x0, x0 + .08, 0, .06 + E, z0, z0 + .14) for x0 in (-.34, .26) for z0 in (-.95, .70)])
    p.add("Deck_Board", SL, box(-.265, .265, .15, .185, -.82, .72))
    p.add("Belt", RB, box(-.25, .25, .187, BT, -.86, .76))
    p.add("Rollers_Hardware", ST, tube((-.284, .14, -.90), (.284, .14, -.90), .04, 12), tube((-.284, .14, .80), (.284, .14, .80), .04, 12))
    p.add("Side_Rails", ALY, box(-.36, -.27, .18 - E, .21, -.9, .85 + E), box(.27, .36, .18 - E, .21, -.9, .85 + E))
    p.add("Motor_Hood", WH, hull([(x, y, z) for x in (-.36, .36) for (y, z) in ((.07, .85), (.07, 1.16), (.30, 1.16), (.30, .90), (.24, .85))]))
    up = [tube((s*.30, .298, 1.04), (s*.30, 1.204, .819), .025, 10) for s in (-1, 1)]
    up += [tube((s*.30, 1.06, .854), (s*.30, 1.06, .61), .02, 10) for s in (-1, 1)]
    p.add("Uprights_Handrails", ST, *up)
    p.add("Grip_Pads", RB, *[tube((s*.30, 1.06, .62), (s*.30, 1.06, .30), .028, 10) for s in (-1, 1)])
    p.add("Console", G, box(-.40, .40, 1.20, 1.36, .70, .92))
    p.add("Console_Screen_LED", CY, box(-.18, .18, 1.36 - E, 1.37, .74, .88))
    p.add("Safety_Key_Amber", AM, box(.25, .31, 1.36 - E, 1.375, .76, .80))
    col(p, "Treadmill", (-.40, 0, -.95), (.40, 1.42, 1.16)); return p
def rower(q):
    p = Part(); fz, fy = .92, .50
    p.add("Monorail", ALY, hull([(x, y, z) for x in (-.035, .035) for (y, z) in ((.28, -1.15), (.33, -1.15), (.38, .55), (.43, .55))]))
    p.add("Legs", G, box(-.25, .25, .06, .29, -1.20, -1.10), box(-.28, .28, .06, .386, .45, .55))
    p.add("Feet", RB, *[box(x0, x0 + .1, 0, .06 + E, z0, z0 + .12) for x0 in (-.27, .17) for z0 in (-1.21,)] + [box(x0, x0 + .1, 0, .06 + E, .44, .56) for x0 in (-.30, .20)])
    p.add("Frame_Neck", G, tube((0, .405, .55 - E), (0, .405, .638), .02, 10))
    p.add("Fan_Cage", WH, tube((-.17, fy, fz), (.17, fy, fz), .30, 24))
    p.add("Fan_Hub_LED", CY, tube((.17 - E, fy, fz), (.20, fy, fz), .07, 16), tube((-.20, fy, fz), (-.17 + E, fy, fz), .07, 16))
    p.add("Fan_Legs", G, tube((-.15, .08, fz), (-.15, .205, fz), .03, 8), tube((.15, .08, fz), (.15, .205, fz), .03, 8))
    p.add("Fan_Feet", RB, box(-.22, -.08, 0, .08 + E, fz - .07, fz + .07), box(.08, .22, 0, .08 + E, fz - .07, fz + .07))
    p.add("Footrests", RB, *[hull([(s*(.034 + x), y, z) for x in (0, .15) for (y, z) in ((.40, .36), (.44, .36), (.58, .46), (.55, .48))]) for s in (-1, 1)])
    p.add("Seat", RB, hull([(x, y, z) for x in (-.16, .16) for y in (.44, .50) for z in (-.47, -.20)]))
    p.add("Seat_Carriage_Hardware", ST, box(-.07, .07, .392, .44 + E, -.45, -.22))
    p.add("Handle_Bar", ST, tube((-.17, .62, .58), (.17, .62, .58), .015, 10))
    p.add("Handle_Grips", RB, tube((-.28, .62, .58), (-.17 - E, .62, .58), .022, 10), tube((.17 + E, .62, .58), (.28, .62, .58), .022, 10))
    p.add("Chain_Hardware", G, tube((0, .62, .58 + .012), (0, .60, .645), .008, 6))
    p.add("Monitor_Arm", G, tube((0, fy + .30 - E, fz - .05), (0, 1.0, .62), .018, 8))
    p.add("Monitor_LED", CY, box(-.11, .11, .98, 1.10, .58, .62))
    col(p, "Rower", (-.30, 0, -1.21), (.30, 1.10, fz + .30)); return p
def moss_berm(q):
    p = Part(); rng = np.random.default_rng(q.get("seed", 1)); L, D = q["L"], q["D"]; rocks = []
    for x in np.linspace(-L/2 + .25, L/2 - .25, 4):
        h = rng.uniform(.18, .34); w = rng.uniform(.18, .22)
        pts = [(x + rng.uniform(-w, w), 0, rng.uniform(-D/2 + .05, D/2 - .05)) for _ in range(8)] + [(x + rng.uniform(-w*.6, w*.6), h*rng.uniform(.7, 1), rng.uniform(-D/3, D/3)) for _ in range(6)]
        rocks.append(hull(pts))
    p.add("Boulders", SL, *rocks)
    moss = []
    for r in rocks:
        v = r.vertices[np.argmax(r.vertices[:, 1])]; moss.append(clump(tuple(v + (0, .068, 0)), .07, seed=int(rng.integers(99))))
    p.add("Moss_Cushions", LF2, *moss)
    ferns = []
    for x in np.linspace(-L/2 + .05, L/2 - .05, 5):
        c = (x + .12, 0, D/2 - .05)
        ferns += [leaf_dir(c, (np.cos(a), 1.3, .4), .30, .07, t=.006) for a in np.linspace(.4, np.pi - .4, 3)]
    p.add("Fern_Fronds", LF, *ferns)
    col(p, "Berm", (-L/2, 0, -D/2), (L/2, .4, D/2)); return p
def green_wall_prop(q):
    p = Part(); W, H = q["W"], q["H"]
    p.add("Frame", G, box(-W/2, -W/2 + .05, 0, H, -.10, 0), box(W/2 - .05, W/2, 0, H, -.10, 0), box(-W/2 + .05 - E, W/2 - .05 + E, H - .05, H, -.10, 0), box(-W/2 + .05 - E, W/2 - .05 + E, 0, .12, -.10, 0))
    p.add("Mesh_Backer", ST, box(-W/2 + .05 - E, W/2 - .05 + E, .12 - E, H - .05 + E, -.098, -.08))
    p.add("Foliage", LF, green_wall(-W/2 + .06, W/2 - .06, .14, H - .07, -.08, r=.12, seed=q.get("seed", 2)))
    p.add("Sport_Stripe_LED", AM, box(-W/2 + .06, W/2 - .06, .05, .07, -E, .006))
    col(p, "GreenWall", (-W/2, 0, -.10), (W/2, H, .15)); return p
SETS3 = {
 "tt_rink_surface_panel": (surf_panel, [dict(label="Rink rubber 12 mm panel 5.30 x 6.465 (centre field, 10 x 4)", W=5.30, D=6.465),
                                        dict(label="Rink rubber 12 mm panel 3.93 x 6.00 (end strip, 3 per end)", W=3.93, D=6.0)]),
 "tt_rink_surface_corner": (surf_corner, [dict(label="Rink rubber quarter disc R 3.93 (R 4.0 board line - 0.07 kick)", R=3.93)]),
 "tt_rink_lines_futsal": (futsal, [dict(label="Futsal 40 x 20 line set, 80 mm opaque strips, 6 mm thick (sits 2 mm into rubber, top 4 mm proud)")]),
 "tt_gym_mirror": (mirror, [dict(label="Mirror 1.2 x 2.1 on 0.3 rubber kick, opaque metal-reflective", W=1.2, H=2.1), dict(label="Mirror 1.2 x 2.1 + leaf crest", W=1.2, H=2.1, crest=True)]),
 "tt_gym_floor_tile": (floor_tile, [dict(label="Rubber floor tile 1 x 1 x 0.02, slate flecks"), dict(label="Rubber floor tile, slate lane inlay", stripe=True)]),
 "tt_gym_treadmill": (treadmill, [dict(label="Treadmill 0.8 x 2.1: belt over rollers, deck, motor hood, uprights, rails, console")]),
 "tt_gym_rower": (rower, [dict(label="Air rower: monorail, seat carriage, footrests, fan cage, chain to handle")]),
 "tt_gym_moss_berm": (moss_berm, [dict(label="Moss berm 1.8 x 0.6: slate boulders, moss cushions, ferns", L=1.8, D=.6)]),
 "tt_gym_green_wall": (green_wall_prop, [dict(label="Green wall panel 1.2 x 2.4, gunmetal frame, steel mesh, foliage", W=1.2, H=2.4)]),
}
if __name__ == "__main__":
    for mod in (sys.argv[1:] or list(SETS3)):
        b, prm = SETS3[mod]; run(mod, b, prm, title="temp-Active pass 4", names=[f"{mod}_v{i+1}" for i in range(len(prm))], post=fine_scissor)
