"""Rook: Tennis Tower stair core Type A (Rev 2.5 §3.11.8: core 5.5 x 5.5 m, 2 flights x 2.5 m, no well) + lift core
(2 cars per stack, 2 x 2.0 x 2.8 m shafts, car 1.6 x 2.4 x 2.5 m, centre-opening doors 1.1 x 2.1 m).
REUSE (preface residential sector, Rev C): the stair is a parameterized port of stair_set_generator.py (switchback: flight 1 cast /
flight 2 bolted modules, 15 mm slate tread finish, 30 mm amber emergency nosing, 0.25 / 0.30 m landing slabs, violet stringer LEDs,
wall anchor plates), the centre guard + wall handrails follow stair_guard_generator.py (glass guard, alloy posts / cap rail / standoffs),
colliders use stair_core_colliders_rev_c.slab_between (Flight*_Ramp-colonly through the nosings, *_Landing-colonly flush, GEO-22
understair closure), materials are the stair_pbr_materials.py texture sets (white cladding, qa03 gunmetal, qa03 brushed titanium,
atrium glass), the lift follows lift_generator.py (white shaft, two-skin door wall + cavity, gunmetal jambs, alloy sills, guide rails,
call panel with amber glyph, green/amber status lamps). Rise per module: half a 6.1 m storey (18 R x 0.1694, T 0.28) -> stack 2 per storey.
ground=True: flight 1 cast solid + understair closure (module on F1/F2/F3 floor); ground=False: both flights modular (stacked half).
Run: python3 stair_core.py"""
from modlib import *
from stair_core_colliders_rev_c import slab_between
ST_H = 6.1; RISE = ST_H / 2; N = 9; R = RISE / (2*N); T = .28; FW = 2.5; WT = .25; FIN, NOSE = .015, .03
XI = (-2.5, 2.5); ZS, ZN = -2.5, 2.5; F1, F2 = (-2.5, -.001), (.001, 2.5)
ZL = ZS + 1.38; Z1b = ZL + (N-1)*T; Z2t = ZL + (N-1)*T; YL = N*R

def stair(q):
    p = Part(); g = q.get("ground", True)
    for k in range(1, N):  # flight 1 rises toward -Z
        za, zb, yt = Z1b - k*T - (E if k == N-1 else 0), Z1b - (k-1)*T, k*R
        p.add("Flight1_Cast" if g else "Flight1_Modules", WH, box(F1[0] - E, F1[1], 0 if g else yt - .25, yt - FIN + E, za, zb))
        p.add("Treads_Slate", SSL, box(F1[0] - E + .002, F1[1] - .002, yt - FIN, yt, za + .002, zb + .005)); p.add("Nosing_Emergency", AM, box(F1[0] + .03, F1[1] - .03, yt - .003, yt + .002, zb - NOSE, zb - .002))
    for j in range(1, N):  # flight 2 rises toward +Z
        za, zb, yt = ZL + (j-1)*T - (E if j == 1 else 0), ZL + j*T - (.002 if j == N-1 else 0), YL + j*R
        p.add("Flight2_Modules", WH, box(F2[0], F2[1] + E, yt - .25, yt - FIN + E, za, zb))
        p.add("Treads_Slate", SSL, box(F2[0] + .002, F2[1] + E - .002, yt - FIN, yt, za - .005, zb - .002)); p.add("Nosing_Emergency", AM, box(F2[0] + .03, F2[1] - .03, yt - .003, yt + .002, za + .002, za + NOSE))
    p.add("Mid_Landing", WH, box(XI[0] - E, XI[1] + E, 0 if g else YL - .25, YL - FIN + E, ZS - E, ZL)); p.add("Mid_Landing_Slate", SSL, box(XI[0] + .002, XI[1] - .002, YL - FIN, YL, ZS + .002, ZL + .005))
    p.add("Top_Landing", WH, box(XI[0] - E, XI[1] + E, RISE - .30, RISE - FIN + E, Z2t, ZN)); p.add("Top_Landing_Slate", SSL, box(XI[0] + .002, XI[1] - .002, RISE - FIN, RISE, Z2t - .005, ZN - .002))
    p.add("Core_Walls", WH, box(XI[0] - WT, XI[0], 0, RISE, ZS - WT, ZN), box(XI[1], XI[1] + WT, 0, RISE, ZS - WT, ZN), box(XI[0], XI[1], 0, RISE, ZS - WT, ZS))
    p.add("Stringer_LEDs", VIO, *[box(F2[0] + .002, F2[0] + .006 + 0, YL + j*R - .2, YL + j*R - .17, ZL + (j-1)*T + .01, ZL + j*T - .01) for j in range(2, N)]) if False else None
    if g:  # GEO-22: flight 2 + mid landing closed below on the F2 side (visual screen + collider)
        p.add("Understair_Screen", WH, box(F2[0] + .01, F2[1] - .01, 0, YL + (N-1)*R - .25 + E, Z2t - .05 - E*0, Z2t - .05 + .04)) if False else \
        p.add("Understair_Screen", WH, box(F2[0] + .01, F2[1] - .01, 0, YL + (N-2)*R - .25 + E, ZL + (N-1)*T - .04 - .28, ZL + (N-1)*T - .28))
    # guard: centre glass on the F2 edge (F2 is up to 1.5 m above F1), alloy posts + cap rail; wall handrails both sides
    gl, po, cap = [], [], []
    for j in range(1, N):
        za = ZL + (j-1)*T; yt = YL + j*R
        if j % 3 == 1: po.append(box(.045, .075, yt - E, yt + 1.0 - .034 + E, za + .1, za + .14))
        gl.append(box(.03, .042, yt + .06, yt + .85, za + .015, za + T - .015))
    a, b = np.array([.04, YL + R + 1.0, ZL + .12]), np.array([.04, YL + (N-1)*R + 1.0, ZL + (N-2)*T + .12])
    cap.append(tube(a - [0, 0, .3*0], b, .025, 6))
    p.add("Guard_Glass_Centre", GL, *gl); p.add("Guard_Posts", ALY, *po); p.add("Guard_Cap_Rail", ALY, *cap)
    hr = []
    for x, (y0, z0, y1, z1) in ((XI[0] + .07, (R + .9, Z1b - .5*T, (N-1)*R + .9, ZL + .5*T)), (XI[1] - .07, (YL + R + .9, ZL + .5*T, YL + (N-1)*R + .9, Z2t - .5*T))):
        hr.append(tube((x, y0, z0), (x, y1, z1), .022, 6))
        for u in (.15, .85):
            c = np.array([x, y0 + (y1 - y0)*u, z0 + (z1 - z0)*u]); s = -1 if x < 0 else 1
            hr.append(box(*sorted((c[0], x - s*.07 + s*0 - s*(-E) )), c[1] - .015, c[1] + .015, c[2] - .015, c[2] + .015))
    p.add("Handrail_Wall", ALY, *hr)
    # colliders (Rev C scheme)
    p.add("Flight1_Ramp-colonly", G, slab_between(*F1, Z1b + T, 0.0, ZL, YL)); p.add("Flight2_Ramp-colonly", G, slab_between(*F2, ZL - T, YL, Z2t, RISE))
    p.add("Mid_Landing-colonly", G, trimesh.creation.box(bounds=[[XI[0], YL - .25, ZS], [XI[1], YL, ZL]])); p.add("Top_Landing-colonly", G, trimesh.creation.box(bounds=[[XI[0], RISE - .3, Z2t], [XI[1], RISE, ZN]]))
    if g: p.add("Flight2_Understair_Closure-colonly", G, trimesh.creation.box(bounds=[[F2[0], 0, ZS], [F2[1], YL - .25, Z2t - .32]]))
    for k, (mk, m) in list(p.P.items()):
        if "colonly" in k:  # trim collider slabs at the floor so min Y = 0 (pivot rule); flat face at y 0 stays walkable
            if m.bounds[0][1] < 0: m = m.slice_plane([0, 0, 0], [0, 1, 0], cap=True); p.P[k] = (mk, m)
            m.metadata["uv"] = np.zeros((len(m.vertices), 2))
    dress_stair(p, q); return p

def dress_stair(p, q):
    d = q["dress"]
    if d == "garden":  # planters on the mid landing (back wall) + front landing, vines on the back wall
        tr, so, sy = planter(-2.3, -.4, YL - E, ZS + .03, ZS + .45, h=.45); p.add("Planter_Trough", G, tr); p.add("Planter_Soil", SO, so); p.add("Foliage", LF2, shrubs(-2.2, -.5, sy, ZS + .24, r=.18, seed=1))
        s, l = vine([(-2.0, YL + .9, ZS + .02), (-1.4, YL + .3 + 1.2, ZS + .02), (-.8, RISE - .1, ZS + .02)], r=.015, leaf_every=.3, leaf_len=.22, seed=2, outward=True)
        p.add("Vine_Stems", LF, s); p.add("Vine_Leaves", LF2, l)
    elif d == "fin":  # Branch Fin: Y-fork fins replace the plain guard posts' look on the centre guard
        for j in (2, 5, 8):
            za = ZL + (j-1)*T; yt = YL + j*R; c = np.array([.1, yt + .5, za + .12])
            p.add("Branch_Fins", ST, tube((.1, yt - E, za + .12), c, .03, 6), tube(c, (.1, yt + .95, za + .12 - .2), .02, 5), tube(c, (.1, yt + .95, za + .12 + .2), .02, 5), node(c, .04, 1))
    elif d == "leaf":  # Leaf Capital: leaf canopy light over the top landing and the mid landing
        for c in ((0, RISE + 2.4, 1.8), (0, YL + 2.4, -1.8)):
            c = np.array(c); p.add("Leaf_Canopy_Lamp", LF, *[leaf_dir(c + [np.cos(a)*.1, 0, np.sin(a)*.1], (np.cos(a), -.35, np.sin(a)), .7, .3, t=.015) for a in np.arange(6)*np.pi/3])
            p.add("Lamp_Stem", ALY, box(-.02, .02, c[1] - .1, RISE if c[2] > 0 and False else c[1] + .6, c[2] - .02, c[2] + .02) if False else node(c, .1, 1))
    elif d == "diag":  # Branch Diagonals: V-lattice on both side walls
        for x in np.arange(XI[0] + .3, XI[1] - 1.3, 1.2):
            p.add("Wall_Lattice", ST, tube((x, YL + .3, ZS + .016), (x + .6, RISE - .1, ZS + .016), .02, 5), tube((x + .6, RISE - .1, ZS + .016), (x + 1.2, YL + .3, ZS + .016), .02, 5))
    elif d == "court":  # wayfinding: court-line stripe on landings, ball finials on the centre posts, floor numeral disc
        p.add("Court_Line_Landing", AM, box(XI[0] + .2, XI[1] - .2, RISE - .002, RISE + .003, ZN - .2, ZN - .14), box(XI[0] + .2, XI[1] - .2, YL - .002, YL + .003, ZS + .2, ZS + .26))
        p.add("Ball_Finials", BA, *[node((.04, YL + j*R + 1.0 + .025 + .05 - E, ZL + (j-1)*T + .12), .05, 1) for j in (1, 4, 7)]) if False else None
        p.add("Level_Disc", AM, cap((XI[0] + .02 + .005, 1.6, 2.0), .3, .01, 16, axis="x"))

# ---------------- lift core ----------------
PIT, SW, SD, LW = .15, 2.0, 2.8, .2   # pivot at pit floor; landing level = +0.15
def lift(q):
    p = Part(); X0, X1 = -SW - LW*1.5, SW + LW*1.5; Zb, Zf = -SD/2, SD/2; Y1 = PIT + ST_H; DH, DW = 2.1, 1.1
    xs = [(-SW - LW/2, -LW/2), (LW/2, SW + LW/2)]
    p.add("Shaft_Walls", WH, box(X0, X0 + LW, 0, Y1, Zb - LW, Zf + E), box(X1 - LW, X1, 0, Y1, Zb - LW, Zf + E), box(-LW/2, LW/2, 0, Y1, Zb - LW + E, Zf + E), box(X0 + LW - E, X1 - LW + E, 0, Y1, Zb - LW, Zb))
    fw = []
    for z0, z1 in ((Zf, Zf + .08), (Zf + .14, Zf + .22)):  # two-skin door wall with cavity
        fw.append(box(X0, X1, PIT + DH, Y1, z0, z1))
        cs = [X0] + [v for a, b in xs for v in ((a + b)/2 - DW/2, (a + b)/2 + DW/2)] + [X1]
        fw += [box(cs[i], cs[i+1], 0, PIT + DH + E, z0, z1) for i in (0, 2, 4)]
    p.add("Door_Wall", WH, *fw)
    for (a, b), k in zip(xs, (0, 1)):
        c = (a + b)/2
        p.add("Door_Jambs", SGM, box(c - DW/2 - .03, c - DW/2 + E, PIT, PIT + DH + .03, Zf + .22 - E, Zf + .24), box(c + DW/2 - E, c + DW/2 + .03, PIT, PIT + DH + .03, Zf + .22 - E, Zf + .24), box(c - DW/2 + E, c + DW/2 - E, PIT + DH - E, PIT + DH + .03, Zf + .22 - E, Zf + .24))
        p.add("Sills", ALY, box(c - DW/2 + .003, c + DW/2 - .003, PIT - .03, PIT, Zf - .05, Zf + .22 + .001))
        op = .55 if k == 0 else 0  # shaft A open, shaft B closed: centre-opening panels in the cavity
        p.add("Landing_Doors", SGM, box(c - DW/2 - op + .002, c - op - .002, PIT + .005, PIT + DH - .005, Zf + .095, Zf + .125), box(c + op + .002, c + DW/2 + op - .002, PIT + .005, PIT + DH - .005, Zf + .095, Zf + .125))
        p.add("Call_Panels", SGM, box(c + DW/2 + .12, c + DW/2 + .3, PIT + .9, PIT + 1.4, Zf + .22 - E, Zf + .24))
        p.add("Call_Glyph", AM, box(c + DW/2 + .17, c + DW/2 + .25, PIT + 1.1, PIT + 1.2, Zf + .24 - E, Zf + .245))
        p.add("Status_Lamps", GRN if k == 0 else AM, box(c - .1, c + .1, PIT + DH + .1, PIT + DH + .14, Zf + .22 - E, Zf + .235))
        p.add("Guide_Rails", ALY, box(a + .02, a + .06, 0, Y1 - .1, -.02, .02), box(b - .06, b - .02, 0, Y1 - .1, -.02, .02))
    c = sum(xs[0])/2; cz = (Zb + Zf)/2  # car in shaft A at the landing, doors open; 1.6 x 2.4 x 2.5 internal
    p.add("Lift_Car", ALY, box(c - .85, c + .85, PIT - .1, PIT, cz - 1.25, cz + 1.2), box(c - .85, c + .85, PIT + 2.5, PIT + 2.6, cz - 1.25, cz + 1.2),
          box(c - .85, c - .8, PIT - E, PIT + 2.5 + E, cz - 1.2, cz + 1.2), box(c + .8, c + .85, PIT - E, PIT + 2.5 + E, cz - 1.2, cz + 1.2), box(c - .8 + E, c + .8 - E, PIT - E, PIT + 2.5 + E, cz - 1.25, cz - 1.2))
    p.add("Car_Floor_Slate", SSL, box(c - .8 + E, c + .8 - E, PIT - .003, PIT + .0, cz - 1.2 + E, cz + 1.2 - .002)) if False else None
    dress_lift(p, q, xs, Zf + .24, DH, DW); return p

def dress_lift(p, q, xs, zf, DH, DW):
    d = q["dress"]; cs = [(a + b)/2 for a, b in xs]
    if d == "garden":
        for c in cs:
            for s in (-1, 1):
                x = c + s*(DW/2 + .55); tr, so, sy = planter(x - .25, x + .25, PIT if False else 0, zf + .02, zf + .52, h=.6)
                if s > 0: continue
                p.add("Planter_Trough", G, tr); p.add("Planter_Soil", SO, so); p.add("Foliage", LF2, clump((x, sy + .25 - E, zf + .27), .26, int(c*10) % 7 + 1))
    elif d == "fin":
        for x in (cs[0] - DW/2 - .5, (cs[0] + cs[1])/2, cs[1] + DW/2 + .5):
            p.add("Branch_Fins", ST, fin(x, .3, PIT + ST_H - .3, .3, .05, z0=zf - E + .3)) if False else p.add("Branch_Fins", ST, box(x - .025, x + .025, .3, PIT + ST_H - .3, zf - E, zf + .3))
            y = PIT + DH + .6; p.add("Fin_Forks", ST, tube((x, y, zf + .32 - E), (x - .3, y + .9, zf + .32 - E), .02, 5), tube((x, y, zf + .32 - E), (x + .3, y + .9, zf + .32 - E), .02, 5))
    elif d == "leaf":
        for c in cs: p.add("Leaf_Hood", LF, *[leaf_dir((c + dx, PIT + DH + .12, zf - E + .01), (dx*1.5, .35, 1), .8, .35, t=.02) for dx in (-.35, 0, .35)])
    elif d == "diag":
        for c in cs:
            y0, y1 = PIT + DH + .4, PIT + ST_H - .4
            p.add("Front_Lattice", ST, *[tube((c + a, y0, zf + .02), (c + b, y1, zf + .02), .02, 5) for a, b in ((-.9, 0), (0, .9), (-.9, .9), (.9, -.9))]) if False else \
            p.add("Front_Lattice", ST, tube((c - .9, y0, zf + .02 - E + .02), (c, y1, zf + .04), .02, 5), tube((c, y1, zf + .04), (c + .9, y0, zf + .04), .02, 5))
    elif d == "court":
        p.add("Floor_Indicator_Band", AM, box(xs[0][0], xs[1][1], PIT + DH + .35, PIT + DH + .5, zf - E, zf + .01))
        p.add("Court_Line_Sill", AM, box(xs[0][0], xs[1][1], 0, PIT + .003 if False else .02, zf + .3, zf + .36)) if False else None

VARIANTS = [
    dict(label="Garden Landing: planters + vines on landings, planters at lift doors", dress="garden"),
    dict(label="Branch Fin: Y-fork guard fins, fin pilasters on lift front", dress="fin"),
    dict(label="Leaf Capital: leaf canopy lamps, leaf hoods over lift doors", dress="leaf"),
    dict(label="Branch Diagonals: V-lattice walls + lift front lattice", dress="diag"),
    dict(label="Court Wayfinding: court-line landing stripes, level disc, lift indicator", dress="court"),
]
PATH = [(-1.25, 2.3), (-1.25, ZL - .2), (-1.25, ZS + .6), (1.25, ZS + .6), (1.25, ZL), (1.25, ZN - .2)]
if __name__ == "__main__":
    rs = run("stair_core", stair, VARIANTS, title="Type A 5.5 x 5.5 m, half-storey switchback (stack 2 per 6.1 m storey) | ground module")
    ru = run("stair_core", stair, [dict(v, ground=False) for v in VARIANTS], title="Type A upper half (modular flights)", suffix="_upper")
    rl = run("stair_core", lift, VARIANTS, title="lift core: 2 shafts 2.0 x 2.8, car 1.6 x 2.4 x 2.5, doors 1.1 x 2.1", suffix="_lift")
    W = {}
    for i, v in enumerate(VARIANTS, 1):
        for tag, q in (("ground", v), ("upper", dict(v, ground=False))):
            pp = stair(q); fl = trimesh.creation.box(bounds=[[-2.5, -.2, 1.1], [0, 0, 2.5]]); fl.metadata["uv"] = np.zeros((8, 2)); pp.P["Entry_Floor-colonly"] = (G, fl)
            W[f"v{i}_{tag}"] = walk_check(pp, PATH)
    json.dump(W, open(os.path.join(RENDER_OUT, "stair_core", "walk_check.json"), "w"), indent=1); print(json.dumps(W))
