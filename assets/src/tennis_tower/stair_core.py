"""Rook: Tennis Tower stair core Type A (Rev 2.5 §3.11.8: core 5.5 x 5.5 m, 2 flights x 2.5 m, no well) + lift core
(2 cars per stack, 2 x 2.0 x 2.8 m shafts, car 1.6 x 2.4 x 2.5 m, centre-opening doors 1.1 x 2.1 m).
REUSE (preface residential sector, Rev C): the stair is a parameterized port of stair_set_generator.py (switchback: flight 1 cast /
flight 2 bolted modules, 15 mm slate tread finish, 30 mm amber emergency nosing, 0.25 / 0.30 m landing slabs, violet stringer LEDs,
wall anchor plates), the centre guard + wall handrails follow stair_guard_generator.py (scissor guard, alloy posts / cap rail / standoffs),
colliders use stair_core_colliders_rev_c.slab_between (Flight*_Ramp-colonly through the nosings, *_Landing-colonly flush, GEO-22
understair closure), materials are the stair_pbr_materials.py texture sets (white cladding, qa03 gunmetal, qa03 brushed titanium,
alpha-scissor guards), the lift follows lift_generator.py (white shaft, two-skin door wall + cavity, gunmetal jambs, alloy sills, guide rails,
call panel with amber glyph, green/amber status lamps). Rise per module: half a 6.1 m storey (18 R x 0.1694, T 0.28) -> stack 2 per storey.
ground=True: flight 1 cast solid + understair closure (module on F1/F2/F3 floor); ground=False: both flights modular (stacked half).
Run: python3 stair_core.py"""
from modlib import *
from stair_core_colliders_rev_c import slab_between
from structure.struct_lib import SCR, finish_scissor
def _scrub(p):  # zero-area loft/slice caps become zero-length shade_split normals; drop them and keep UVs
    for k, (mk, m) in list(p.P.items()):
        n = len(m.vertices); uv = m.metadata.get("uv"); uv = np.array(uv, float, copy=True) if uv is not None and len(uv) == n else np.zeros((n, 2))
        m.update_faces(m.nondegenerate_faces()); ref = m.remove_unreferenced_vertices(); m.metadata["uv"] = uv if ref is None else uv[np.asarray(ref)]; p.P[k] = (mk, m)
    return p
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
    # guard: centre scissor panel on the F2 edge (F2 is up to 1.5 m above F1), alloy posts + cap rail; wall handrails both sides
    gl, po, cap = [], [], []
    for j in range(1, N):
        za = ZL + (j-1)*T; yt = YL + j*R
        if j % 3 == 1: po.append(box(.045, .075, yt - E, yt + 1.0 - .034 + E, za + .1, za + .14))
        gl.append(box(.03, .042, yt + .06, yt + .85, za + .015, za + T - .015))
    a, b = np.array([.04, YL + R + 1.0, ZL + .12]), np.array([.04, YL + (N-1)*R + 1.0, ZL + (N-2)*T + .12])
    cap.append(tube(a - [0, 0, .3*0], b, .025, 6))
    p.add("Guard_Scissor_Centre", SCR, *gl); p.add("Guard_Posts", ALY, *po); p.add("Guard_Cap_Rail", ALY, *cap)
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
    dress_stair(p, q); return _scrub(p)

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
    dress_lift(p, q, xs, Zf + .24, DH, DW); return _scrub(p)

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

# ================= Rev 2.7 full-storey cores (Type A / B), V5 Court Wayfinding =================
CORE = {"A": dict(W=5.5, L=10.2, FW=2.5), "B": dict(W=6.0, L=10.6, FW=2.7)}
def stair_full(q):
    c = CORE[q["type"]]; WT2 = .2; xi = c["W"]/2 - WT2; zi = c["L"]/2 - WT2; FWc = c["FW"]; H = ST_H; n = 18; r = H/(2*n); t = .28
    f1, f2 = (-xi, -xi + FWc), (xi - FWc, xi); zs, zn = -zi, zi; zl = zs + FWc; z1b = zl + (n-1)*t; z2t = zl + (n-1)*t; yl = n*r
    assert zn - z2t >= FWc - 1e-6, "front landing shorter than flight width"
    p = Part()
    for k in range(1, n):
        za, zb, yt = z1b - k*t - (E if k == n-1 else 0), z1b - (k-1)*t, k*r
        p.add("Flight1_Cast", WH, box(f1[0] - E, f1[1], 0, yt - FIN + E, za, zb))
        p.add("Treads_Slate", SSL, box(f1[0] - E + .002, f1[1] - .002, yt - FIN, yt, za + .002, zb + .005)); p.add("Nosing_Emergency", AM, box(f1[0] + .03, f1[1] - .03, yt - .003, yt + .002, zb - NOSE, zb - .002))
    for j in range(1, n):
        za, zb, yt = zl + (j-1)*t - (E if j == 1 else 0), zl + j*t - (.002 if j == n-1 else 0), yl + j*r
        p.add("Flight2_Modules", WH, box(f2[0], f2[1] + E, yt - .25, yt - FIN + E, za, zb))
        p.add("Treads_Slate", SSL, box(f2[0] + .002, f2[1] + E - .002, yt - FIN, yt, za - .005, zb - .002)); p.add("Nosing_Emergency", AM, box(f2[0] + .03, f2[1] - .03, yt - .003, yt + .002, za + .002, za + NOSE))
    p.add("Mid_Landing", WH, box(-xi - E, xi + E, 0, yl - FIN + E, zs - E, zl)); p.add("Mid_Landing_Slate", SSL, box(-xi + .002, xi - .002, yl - FIN, yl, zs + .002, zl + .005))
    p.add("Top_Landing", WH, box(-xi - E, xi + E, H - .30, H - FIN + E, z2t, zn + E)); p.add("Top_Landing_Slate", SSL, box(-xi + .002, xi - .002, H - FIN, H, z2t - .005, zn - .002))
    p.add("Core_Walls", WH, box(-xi - WT2, -xi, 0, H - .002, zs - WT2, zn + WT2), box(xi, xi + WT2, 0, H - .002, zs - WT2, zn + WT2), box(-xi, xi, 0, H - .002, zs - WT2, zs))
    # front wall (corridor side) with the storey door opening on the flight-1 side (2.2 m high); next storey's opening sits on this top landing
    p.add("Front_Wall", WH, box(-xi + E*0 - E, f1[0] + .3, 0, H - .002, zn, zn + WT2 - .002), box(f1[1] - .3, xi + E, 0, H - .002, zn, zn + WT2 - .002), box(f1[0] + .3 - E, f1[1] - .3 + E, 2.2, H - .002, zn, zn + WT2 - .002))
    p.add("Door_Jambs", SGM, box(f1[0] + .28, f1[0] + .3 + E, 0, 2.2 + .02, zn + WT2 - .002 - E, zn + WT2 + .01), box(f1[1] - .3 - E, f1[1] - .28, 0, 2.2 + .02, zn + WT2 - .002 - E, zn + WT2 + .01))
    # well guards (closed scissor boxes + alloy posts + cap rail) on both flight edges, Rev C stair_guard language
    for fx, (zfun, yfun, ks) in ((f1[1], (lambda k: z1b - (k - .5)*t, lambda k: k*r, range(1, n))), (f2[0], (lambda j: zl + (j - .5)*t, lambda j: yl + j*r, range(1, n)))):
        s = 1 if fx > 0 else -1; gx = fx + s*.04; gl, po = [], []
        for k in ks:
            zc, yt = zfun(k), yfun(k)
            gl.append(box(gx - .006, gx + .006, yt + .06, yt + .85, zc - t/2 + .015, zc + t/2 - .015))
            if k % 4 == 1: po.append(box(*sorted((gx + s*.015, gx + s*.045)), yt - E, yt + .966 - .012 + E - .02, zc - .02, zc + .02))
        a, b = np.array([gx + s*.03, yfun(ks[0]) + 1.0, zfun(ks[0])]), np.array([gx + s*.03, yfun(ks[-1]) + 1.0, zfun(ks[-1])])
        p.add("Guard_Scissor", SCR, *gl); p.add("Guard_Posts", ALY, *po); p.add("Guard_Cap_Rail", ALY, tube(a, b, .025, 6))
    hr = []
    for x, (y0, z0, y1, z1) in ((-xi + .07, (r + .9, z1b - .5*t, (n-1)*r + .9, zl + .5*t)), (xi - .07, (yl + r + .9, zl + .5*t, yl + (n-1)*r + .9, z2t - .5*t))):
        hr.append(tube((x, y0, z0), (x, y1, z1), .022, 6)); s = -1 if x < 0 else 1
        for u in (.1, .5, .9):
            cc_ = np.array([x, y0 + (y1 - y0)*u, z0 + (z1 - z0)*u]); hr.append(box(*sorted((cc_[0], x + s*.07 - s*.0 + s*E)), cc_[1] - .015, cc_[1] + .015, cc_[2] - .015, cc_[2] + .015))
    p.add("Handrail_Wall", ALY, *hr)
    # V5 Court Wayfinding dressing
    p.add("Court_Line_Landing", AM, box(-xi + .2, xi - .2, H - .002, H + .003, zn - .2, zn - .14), box(-xi + .2, xi - .2, yl - .002, yl + .003, zs + .2, zs + .26))
    p.add("Level_Disc", AM, cap((-xi + .005 + .002, 1.6, zn - 1.2), .3, .01, 16, axis="x"), cap((xi - .007, yl + 1.6, zs + 1.2), .3, .01, 16, axis="x"))
    # colliders (Rev C scheme)
    p.add("Flight1_Ramp-colonly", G, slab_between(*f1, z1b + t, 0.0, zl, yl)); p.add("Flight2_Ramp-colonly", G, slab_between(*f2, zl - t, yl, z2t, H))
    p.add("Mid_Landing-colonly", G, trimesh.creation.box(bounds=[[-xi, yl - .25, zs], [xi, yl, zl]])); p.add("Top_Landing-colonly", G, trimesh.creation.box(bounds=[[-xi, H - .3, z2t], [xi, H, zn]]))
    for gname, fx in (("Well_Guard_F1-convcolonly", f1[1] - .04), ("Well_Guard_F2-convcolonly", f2[0] + .04)):
        pts = [(x, y, z) for x in (fx - .006, fx + .006) for (y, z) in ((0, zl), (0, z1b + t) if fx < 0 else (yl, zl), (yl + 1.0, zl), (1.0 if fx < 0 else H + 1.0, z1b + t if fx < 0 else z2t))]
        p.add(gname, G, trimesh.convex.convex_hull(np.array(pts)))
    for k, (mk, m) in list(p.P.items()):
        if "colonly" in k:
            if m.bounds[0][1] < 0: m = m.slice_plane([0, 0, 0], [0, 1, 0], cap=True); p.P[k] = (mk, m)
            m.metadata["uv"] = np.zeros((len(m.vertices), 2))
    p.walk = [(f1[0] + FWc/2, zn - .3), (f1[0] + FWc/2, zl - .3), (0, zs + .6), (f2[0] + FWc/2, zs + .6), (f2[0] + FWc/2, zl), (f2[0] + FWc/2, zn - .3)]
    return _scrub(p)

def final():
    rep = run("stair_core", stair_full, [dict(type="A", label="Type A 5.5 x 10.2: V5 Court Wayfinding, full storey"), dict(type="B", label="Type B 6.0 x 10.6: V5 Court Wayfinding, full storey")],
              names=["final_a", "final_b"], suffix="_final", sheet="final_ab_sheet.png", title="Rev 2.7 full-storey cores", post=finish_scissor)
    for ty, fn in (("A", "tt_stair_core_a.glb"), ("B", "tt_stair_core_b.glb")):
        p = recenter(stair_full(dict(type=ty))); gp = os.path.join(ROOT, "godot/assets/models", fn)
        tris, _ = export_final(p.P, [gp]); finish_glb(gp); finish_scissor(gp)
        V = np.vstack([m.vertices for _, m in p.P.values()]); lo, hi = V.min(0), V.max(0)
        print(fn, "tris", int(tris), "bbox", lo.round(4).tolist(), hi.round(4).tolist())
    W = {}
    for ty in ("A", "B"):
        pp = stair_full(dict(type=ty)); c = CORE[ty]; zi = c["L"]/2 - .2
        fl = trimesh.creation.box(bounds=[[-c["W"]/2, -.2, zi - c["FW"]], [c["W"]/2, 0, zi]]); fl.metadata["uv"] = np.zeros((8, 2)); pp.P["Entry_Floor-colonly"] = (G, fl)
        W[ty] = walk_check(pp, pp.walk)
    print("WALK", json.dumps(W)); json.dump(W, open(os.path.join(RENDER_OUT, "stair_core", "walk_check_final.json"), "w"), indent=1)
    return rep, W

def mirror_b():  # r1: tt_stair_core_b_m = Type B mirrored in local Z (portal on the -Z face, same X side) for ST-AQN / ST-ARN,
    p = stair_full(dict(type="B"))  # so their F1/F2 portals and F3 arrival face the foyer / arcade like ST-AQS / ST-ARS, not the plant-stack S walls
    for k, (mk, m) in list(p.P.items()):
        uv = np.array(m.metadata["uv"]); m.apply_transform(np.diag([1, 1, -1, 1])); m.metadata["uv"] = uv
    p = recenter(p); gp = os.path.join(ROOT, "godot/assets/models", "tt_stair_core_b_m.glb")
    tris, _ = export_final(p.P, [gp]); finish_glb(gp); finish_scissor(gp)
    chk = cc.check({k: v for k, v in p.P.items() if "colonly" not in k}, n_samp=400)
    try: ok_v = vm.validate_file(gp, check_tri_range=(1, TRI_MAX), require_textures=False, require_blend_glass=False)
    except AssertionError as e: print("VALIDATE FAIL", e); ok_v = False
    V = np.vstack([m.vertices for k, (_, m) in p.P.items() if "colonly" not in k]); lo, hi = V.min(0), V.max(0)
    pp = stair_full(dict(type="B")); c = CORE["B"]; zi = c["L"]/2 - .2
    fl = trimesh.creation.box(bounds=[[-c["W"]/2, -.2, zi - c["FW"]], [c["W"]/2, 0, zi]]); fl.metadata["uv"] = np.zeros((8, 2)); pp.P["Entry_Floor-colonly"] = (G, fl)
    w = walk_check(pp, pp.walk)   # walk on the unmirrored twin (a mirror keeps every step, slope and headroom)
    print(json.dumps(dict(glb="tt_stair_core_b_m.glb", tris=int(tris), clip_pass=bool(chk["pass"]), worst_overlap=chk["worst_overlap"], coplanar=chk["coplanar"],
                          open=chk["open"], validate=bool(ok_v), bbox=[lo.round(4).tolist(), hi.round(4).tolist()], walk=w), default=str))

if __name__ == "__main__" and sys.argv[1:] == ["final"]:
    final()
elif __name__ == "__main__" and sys.argv[1:] == ["mirror_b"]:
    mirror_b()
elif __name__ == "__main__":
    rs = run("stair_core", stair, VARIANTS, title="Type A 5.5 x 5.5 m, half-storey switchback (stack 2 per 6.1 m storey) | ground module", post=finish_scissor)
    ru = run("stair_core", stair, [dict(v, ground=False) for v in VARIANTS], title="Type A upper half (modular flights)", suffix="_upper", post=finish_scissor)
    rl = run("stair_core", lift, VARIANTS, title="lift core: 2 shafts 2.0 x 2.8, car 1.6 x 2.4 x 2.5, doors 1.1 x 2.1", suffix="_lift", post=finish_scissor)
    W = {}
    for i, v in enumerate(VARIANTS, 1):
        for tag, q in (("ground", v), ("upper", dict(v, ground=False))):
            pp = stair(q); fl = trimesh.creation.box(bounds=[[-2.5, -.2, 1.1], [0, 0, 2.5]]); fl.metadata["uv"] = np.zeros((8, 2)); pp.P["Entry_Floor-colonly"] = (G, fl)
            W[f"v{i}_{tag}"] = walk_check(pp, PATH)
    json.dump(W, open(os.path.join(RENDER_OUT, "stair_core", "walk_check.json"), "w"), indent=1); print(json.dumps(W))
