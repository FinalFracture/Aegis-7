"""Rook: Tennis Tower E-terrace playground piece 5 (round 2), toddler zone 8 x 8 m as a sculpted natural play landscape
(spec §3.11.6: spring riders + toddler deck in an 8 x 8 m toddler zone; round 1 toddler_zone.py rejected by Jared Nov 4 -> superseded).
Five concepts built from one kit: rubber mounds (convex, 3-ring), crawl tunnels, hollow trunk crawl-through, sunken sand dig with a
rubber rim, stepping pods, wavy low balance path, mini slide off a mound (on a rubber wedge), leaf-canopy tree, sensory panels, foliage.
Toddler-safe: play surfaces 0..1.2 m, tunnel bore 0.6 m, no spinning parts, no wood, no planter boxes, every piece has a collider.
REUSE: #63/#64/#66 playground language (EPDM, HDPE leaf/sand, ball yellow, court line), #65 leaf crest, #64 Tree Swing foliage clumps,
#66 racket hoops, modlib leaf/clump/cap, cabana_lounger.boxuv. Run: python3 toddler_landscape.py"""
from modlib import *
import modlib, play_tower as pt
from cabana_lounger import boxuv
from restroom_extras import crest
U = pt.U; PAD = .03; HZ = 4.0; HX = 4.0  # HX: half-size in X (zone may be rectangular)
modlib._m("tt_rubber_moss", "TT_PlayRubber_Moss", (.36, .55, .30), 0, .9)
modlib._m("tt_rubber_tan", "TT_PlayRubber_Tan", (.70, .60, .44), 0, .9)
modlib._m("tt_rubber_river", "TT_PlayRubber_River", (.26, .50, .72), 0, .6)
modlib._m("tt_rubber_bark", "TT_PlayRubber_Bark", (.40, .29, .20), 0, .85)
modlib._m("tt_sand", "TT_PlaySand", (.86, .78, .60), 0, .95)
modlib._m("tt_rubber_stone", "TT_PlayRubber_Stone", (.55, .56, .54), 0, .85)
RU, MOSS, TAN, RIV, BARK, SAND, STONE, HL, HS = pt.RU, "tt_rubber_moss", "tt_rubber_tan", "tt_rubber_river", "tt_rubber_bark", "tt_sand", "tt_rubber_stone", "tt_hdpe_leaf", "tt_hdpe_sand"
Y = lambda a: trimesh.transformations.rotation_matrix(a, [0, 1, 0])

def depth(a, b):
    d = 0.0
    for x, y in ((a, b), (b, a)):
        S = np.vstack([x.vertices, trimesh.sample.sample_surface_even(x, 300, seed=1)[0]]); ins = y.contains(S)
        if ins.any(): d = max(d, float(trimesh.proximity.signed_distance(y, S[ins]).max()))
    return d
def near(a, b, pad=.05): return np.all(a.bounds[0] <= b.bounds[1] + pad) and np.all(b.bounds[0] <= a.bounds[1] + pad)
def rest_on(ms, bases, tol=.0035, lo=-.4, hi=.4):  # move ms vertically (rigidly) until they just touch the bases (penetration <= tol)
    def bad(dy):
        for m in ms:
            mm = trimesh.Trimesh(m.vertices + (0, dy, 0), m.faces, process=False)
            if any(near(mm, b) and depth(mm, b) > tol for b in bases): return True
        return False
    for _ in range(16):
        mid = (lo + hi)/2
        if bad(mid): lo = mid
        else: hi = mid
    for m in ms: m.apply_translation((0, hi, 0))
    return ms

def drop(ms, bases, emb=.003, n=500):  # lift/lower ms rigidly so they rest on the highest base surface below them (embedded emb)
    B = trimesh.util.concatenate([b for b in bases if any(np.all(b.bounds[0][[0, 2]] <= m.bounds[1][[0, 2]] + .1) and np.all(m.bounds[0][[0, 2]] <= b.bounds[1][[0, 2]] + .1) for m in ms)]); R = trimesh.ray.ray_triangle.RayMeshIntersector(B)
    P = np.vstack([np.vstack([m.vertices, trimesh.sample.sample_surface_even(m, n, seed=2)[0]]) for m in ms])
    loc, ri, _ = R.intersects_location(np.c_[P[:, 0], np.full(len(P), 9.0), P[:, 2]], np.tile([0, -1, 0], (len(P), 1)), multiple_hits=True)
    g = np.full(len(P), -9.0); np.maximum.at(g, ri, loc[:, 1]); ok = g > -9
    dy = float(np.max(g[ok] - P[ok, 1]) - emb)
    for m in ms: m.apply_translation((0, dy, 0))
    return dy

class Scape:
    """collects meshes per (part, material); terrain = one rubber part per concept (pieces of one part may interlock)."""
    def __init__(s, ground, terrain):
        s.p = Part(); s.L = {}; s.col = {}; s.terrain = terrain; s.T = []; s.solid = []; s.G = []; s.Q = []; s.SQ = []
        s.pad = box(-HX, HX, 0, PAD, -HZ, HZ); s.add("Safety_Pad", ground, s.pad, col=None)
    def add(s, part, mat, *ms, col="hull", solid=True):
        s.L.setdefault((part, mat), []).extend(ms)
        if solid: s.solid += ms
        if col == "hull": s.col.setdefault(part, []).extend([trimesh.convex.convex_hull(m.vertices) for m in ms])
        elif col == "mesh": s.col.setdefault(part + "_mesh", []).extend([m.copy() for m in ms])
        return ms
    def mound(s, x, z, rx, rz, h, off=(0, 0), part="Terrain", mat=None, rot=0.0):
        n = 14; P = []
        for f, y, (dx, dz) in ((1.0, PAD - E, (0, 0)), (.74, .6*h, (off[0]*.4, off[1]*.4)), (.34, h, off)):
            for a in np.linspace(0, 2*np.pi, n, endpoint=False):
                u, v = f*rx*np.cos(a) + dx, f*rz*np.sin(a) + dz
                P.append((x + u*np.cos(rot) - v*np.sin(rot), y, z + u*np.sin(rot) + v*np.cos(rot)))
        m = trimesh.convex.convex_hull(np.array(P)); s.add(part, mat or s.terrain, m); s.G.append(m)
        if part == "Terrain": s.T.append(m)
        return m
    def tunnel(s, x, z, L, yaw, ro=.38, ri=.30, part="Terrain", mat=None):
        m = trimesh.creation.annulus(ri, ro, L, sections=14); m.apply_transform(Y(yaw)); m.apply_translation((x, PAD - E*.5 + ro*np.cos(np.pi/14), z))
        s.add(part, mat or s.terrain, m, col="mesh"); s.G.append(m)
        if part == "Terrain": s.T.append(m)
        return m
    def slide(s, *a, **k): s.SQ.append((a, k))
    def _slide(s, x, z, yaw, h, mat=BA, ang=24.0, wedge_part="Terrain", wedge_mat=None):
        t = .03; a = np.radians(ang); ytop = h + t - E; L = (ytop - .25)/np.sin(a); run = L*np.cos(a)
        def place(m): m.apply_transform(Y(yaw)); m.apply_translation((x, 0, z)); return m
        def plate(x0, x1, y0, y1, z0, z1):
            m = box(x0, x1, y0, y1, z0, z1); m.apply_transform(trimesh.transformations.rotation_matrix(-a, [0, 0, 1])); m.apply_translation((0, ytop, 0)); return place(m)
        bed = [plate(-.25, L, -t, 0, -.26, .26), plate(-.25, L, -E, .12, -.29, -.25), plate(-.25, L, -E, .12, .25, .29)]
        yb = ytop - L*np.sin(a)
        ro = [place(box(run - .02, run + .45, yb - t, yb, -.26, .26)), place(box(run - .02, run + .45, yb - E, yb + .1, -.29, -.255)), place(box(run - .02, run + .45, yb - E, yb + .1, .255, .29))]
        dy = drop(bed + ro, s.G, emb=.003); s.add("Mini_Slide", mat, *bed, *ro); s.slide_top = ytop + dy
        rot = lambda u, v: (u*np.cos(a) + v*np.sin(a), -u*np.sin(a) + v*np.cos(a) + ytop + dy)
        for wp in ([rot(-.23, -t + E), rot(L + .01, -t + E)], [(run - .05, yb - t + E + dy), (run + .43, yb - t + E + dy)]):
            W = np.array([(px, py, w) for px, py in wp for w in (-.24, .24)] + [(px, PAD - E, w) for px, _ in wp for w in (-.24, .24)])
            wm = place(trimesh.convex.convex_hull(W)); s.add(wedge_part, wedge_mat or s.terrain, wm); s.G.append(wm)
            if wedge_part == "Terrain": s.T.append(wm)
    def pods(s, pts, mat, part="Stepping_Pods"):
        return s.add(part, mat, *[cap((x, PAD - E + h/2, z), r, h, 12, axis="y") for x, z, r, h in pts])
    def path(s, pts, mat, w=.22, part="Balance_Path"):
        ms = []
        for (x0, z0, h0), (x1, z1, h1) in zip(pts, pts[1:]):
            L = np.hypot(x1 - x0, z1 - z0); m = box(-L/2 - .03, L/2 + .03, PAD - E, (h0 + h1)/2, -w/2, w/2)
            m.apply_transform(Y(-np.arctan2(z1 - z0, x1 - x0))); m.apply_translation(((x0 + x1)/2, 0, (z0 + z1)/2)); ms.append(m)
        s.add(part, mat, *ms)
    def sandpit(s, x, z, r, rim=TAN):
        rm = trimesh.creation.annulus(r, r + .16, .3, sections=20); rm.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0])); rm.apply_translation((x, PAD - E + .15, z))
        s.add("Sand_Rim", rim, rm, col="mesh"); s.add("Dig_Sand", SAND, cap((x, PAD - .002 + .07, z), r + E, .14, 20, axis="y"))
    def trunk(s, x, z, L, yaw):
        m = trimesh.creation.annulus(.31, .42, L, sections=14); m.apply_transform(Y(yaw)); m.apply_translation((x, PAD - E*.5 + .42*np.cos(np.pi/14), z))
        s.add("Crawl_Trunk", BARK, m, col="mesh"); return m
    def tree(s, x, z, h=2.5, n=7, mat=LF, lean=.35, leaf_len=1.35):
        s.add("Tree_Trunk", ST, tube((x, PAD - E, z), (x, h, z), .1, 10), node((x, h, z), .14, 1))
        L = []
        for k in range(n):
            a = 2*np.pi*k/n + .3; d = np.array([np.cos(a), lean*(1 if k % 2 else .4), np.sin(a)]); d /= np.linalg.norm(d)
            L.append(leaf_dir(np.array((x, h, z)) + d*(.14 - .006), d, leaf_len, .55, t=.025))
        L.append(crest((x, h + .14 + .17 - .006, z))); s.add("Tree_Canopy", mat, *L, col=None)
    def panel(s, x, z, yaw, kind, mat=HL, w=1.0, h=.7):
        M = Y(yaw)
        def T(m): m.apply_transform(M); m.apply_translation((x, 0, z)); return m
        s.add("Sensory_Panels", mat, T(box(-w/2, w/2, PAD - E, h, -.03, .03)))
        s.add("Panel_Feet", G, T(box(-w/2 + .05, w/2 - .05, PAD - .0015, PAD + .05, -.14, -.03 + E)), T(box(-w/2 + .06, w/2 - .06, PAD - .0025, PAD + .046, .03 - E, .14)), col=None)
        if kind == "beads": F = [T(node((u, v, .03 + .04 - E), .04, 0)) for u in np.linspace(-w/2 + .15, w/2 - .15, 5) for v in (h*.45, h*.72)]; fm = BA
        elif kind == "leaves": F = [T(xf(leaf((0, 0, 0), .32, .16, t=.012), R=trimesh.transformations.rotation_matrix(r, [0, 0, 1]), t=(u, h*.3, .03 + .012 - E))) for u, r in zip(np.linspace(-w/2 + .2, w/2 - .2, 4), (.4, -.2, .3, -.4))]; fm = LF2
        else: F = [T(xf(trimesh.creation.torus(.1, .012, 12, 6), t=(u, h*.55, .03 + .012 - E))) for u in (-w/4, w/4)]; fm = AM
        s.add("Panel_Features", fm, *F, col=None)
    def bush(s, x, z, r, mat=LF2, seed=0):
        x, z = np.clip(x, -HX + r + .05, HX - r - .05), np.clip(z, -HZ + r + .05, HZ - r - .05); s.Q.append((clump((x, 1.6, z), r, seed), mat))
    def cluster(s, x, z, n, r, mats=(LF, LF2), seed=0, spread=.35):
        rng = np.random.default_rng(seed)
        for k in range(n): s.bush(x + rng.uniform(-spread, spread), z + rng.uniform(-spread, spread), r*rng.uniform(.6, 1.0), mats[k % len(mats)], seed*10 + k)
    def flowers(s, x, z, n, seed=0, spread=.5, mats=(BA, WH, AM)):
        rng = np.random.default_rng(seed)
        for k in range(n): s.bush(x + rng.uniform(-spread, spread), z + rng.uniform(-spread, spread), .07, mats[k % len(mats)], seed*10 + k + 500)
    def finish(s):
        for a, k in s.SQ: s._slide(*a, **k)
        SL = s.L.get(next((k for k in s.L if k[0] == "Mini_Slide"), None), [])
        for c, mat in s.Q:
            if any(np.all(c.bounds[0][[0, 2]] <= m.bounds[1][[0, 2]] + .35) and np.all(m.bounds[0][[0, 2]] <= c.bounds[1][[0, 2]] + .35) for m in SL): continue  # keep slide run-outs clear
            drop([c], [s.pad] + s.solid, emb=.006); s.add("Foliage", mat, c, col=None, solid=False)
        V = np.vstack([m.vertices for ms in s.L.values() for m in ms]); assert np.all(np.abs(V[:, 0]) <= HX + 1e-6) and np.all(np.abs(V[:, 2]) <= HZ + 1e-6), ("outside the 8 x 8 zone", V[:, [0, 2]].min(0), V[:, [0, 2]].max(0))
        for (part, mat), ms in s.L.items(): s.p.add(part, mat, *[boxuv(m, .5) for m in ms])
        for k, ms in s.col.items(): s.p.add(k.replace("_mesh", "") + ("-colonly" if k.endswith("_mesh") else "-convcolonly"), G, *[U(m) for m in ms])
        s.p.add("Zone-colonly", G, U(box(-HX, HX, 0, PAD, -HZ, HZ)))
        return s.p

def meadow(q):   # Meadow Hills
    s = Scape(RU, MOSS)
    s.mound(-1.7, -1.9, 1.9, 1.6, 1.0, off=(.2, .2)); s.mound(1.3, -2.2, 1.5, 1.3, .7); s.mound(2.6, .6, 1.1, 1.0, .45)
    s.tunnel(-.15, -2.1, 1.6, .25); s.slide(-1.3, -1.45, -np.pi/2 + .25, 1.0)
    s.mound(-3.4, 1.5, .5, 1.9, .4); s.mound(-.6, 3.5, 2.2, .45, .35)
    s.pods([(.2, .6, .2, .12), (.75, .95, .2, .2), (1.3, 1.45, .2, .28), (1.6, 2.1, .2, .2)], HL)
    s.path([(-2.6, .2, .15), (-2.1, .9, .22), (-1.5, 1.2, .28), (-.9, 1.0, .22), (-.4, 1.4, .15)], HS)
    for k, (x, z, r) in enumerate([(-3.5, -3.4, .32), (3.4, -3.3, .3), (3.5, 3.3, .28), (2.2, -3.6, .22), (-2.5, -3.6, .25), (.4, -3.5, .22)]): s.bush(x, z, r, LF2 if k % 2 else LF, k)
    s.mound(3.4, -1.6, .5, 1.3, .4); s.mound(3.5, 2.8, .5, 1.0, .3)
    s.flowers(-1.9, -2.2, 8, 1); s.flowers(1.4, -2.4, 6, 2); s.flowers(2.7, .7, 5, 3, .35); s.flowers(-.6, 3.5, 7, 4, .9)
    s.cluster(-3.4, 1.6, 4, .25, seed=5); s.cluster(3.4, -1.6, 3, .22, seed=6); s.cluster(-2.9, -3.4, 3, .3, seed=7)
    for x, z, r, h in [(1.0, 3.0, .7, .25), (2.6, 2.6, .5, .2), (-2.4, 2.9, .6, .22), (.2, -.5, .5, .18)]: s.mound(x, z, r, r*.8, h)
    return s.finish()
def forest(q):   # Forest Floor
    s = Scape(MOSS, RU)
    s.mound(1.9, -2.0, 1.6, 1.4, .85, off=(.2, -.1)); s.mound(-2.6, -2.5, 1.3, 1.1, .5); s.mound(-3.2, 2.4, .8, 1.4, .35)
    s.trunk(-.6, -2.3, 1.8, .35); s.tree(.4, .3, 2.5, 7, LF)
    s.slide(2.4, -1.3, -np.pi/2 - .3, .85, mat=HL)
    stems = [(-1.6, .6, .18), (-1.1, 1.1, .28), (-.5, 1.6, .38), (.2, 2.0, .3), (.9, 2.4, .2)]
    sm = s.pods([(x, z, .09, h) for x, z, h in stems], WH, part="Mushroom_Stems"); caps = []
    for st, (x, z, h) in zip(sm, stems):
        c = node((0, 0, 0), .26, 1); c.vertices *= [1, .42, 1]; c.apply_translation((x, PAD + h + .08, z)); drop([c], [st], emb=.003); caps.append(c)
    s.add("Mushroom_Caps", BA, *caps)
    s.path([(1.4, .9, .15), (2.0, 1.4, .2), (2.5, 2.1, .26), (2.9, 2.9, .2), (3.3, 3.4, .14)], BARK, part="Root_Path")
    for k, (x, z, r) in enumerate([(-3.5, -.3, .3), (-3.6, .5, .26), (3.5, .2, .3), (3.4, -3.5, .28), (-1.0, 3.5, .3), (-1.8, 3.6, .24), (0, -3.6, .26), (1.2, 3.6, .24)]): s.bush(x, z, r, LF if k % 2 else LF2, k)
    s.mound(-3.4, -.3, .5, 1.0, .35)
    s.cluster(-2.8, -2.8, 4, .3, seed=5); s.cluster(2.3, -2.8, 3, .28, seed=6); s.cluster(-3.3, 2.5, 3, .26, seed=7)
    s.flowers(-1.0, 2.7, 6, 8, .4, mats=(BA, WH)); s.flowers(-3.3, -.4, 4, 9, .3, mats=(WH, BA))
    for x, z, r, h in [(-2.0, 1.6, .6, .22), (-.3, 3.0, .6, .2), (3.2, -.8, .5, .25), (1.4, 2.9, .45, .18)]: s.mound(x, z, r, r*.8, h)
    return s.finish()
def riverbed(q):  # Riverbed
    s = Scape(RU, MOSS)
    C = [(-3.4, -1.0), (-2.6, -.4), (-1.2, -1.1), (.2, -.2), (1.6, .5), (3.0, 0), (3.4, .6)]; R = []
    for k, ((x0, z0), (x1, z1)) in enumerate(zip(C, C[1:])):
        L = np.hypot(x1 - x0, z1 - z0); m = box(-L/2 - .25, L/2 + .25, PAD - .0015, PAD + .004 + .0012*(k % 2), -.5, .5); m.apply_transform(Y(-np.arctan2(z1 - z0, x1 - x0))); m.apply_translation(((x0 + x1)/2, 0, (z0 + z1)/2)); R.append(m)
    s.add("River_Ribbon", RIV, *R, col=None)
    s.mound(-1.9, -3.0, 2.0, .9, .8); s.mound(1.6, -2.7, 1.6, 1.0, 1.1, off=(.15, -.1)); s.mound(-.6, 2.3, 1.4, .9, .55); s.mound(2.6, 2.6, 1.1, 1.0, .4)
    s.tunnel(0, -2.75, 1.4, .1); s.slide(1.25, -2.15, -np.pi/2 + .2, 1.1, mat=HS)
    s.pods([(-2.0, -.95, .22, .12), (-1.7, -.35, .2, .16), (-1.3, .25, .2, .12), (.6, -.9, .22, .14), (.9, -.3, .2, .18), (1.1, .3, .2, .14)], STONE, part="River_Stones")
    s.sandpit(-3.0, 2.9, .75); s.panel(.6, 3.55, 0, "beads", HL); s.panel(3.55, -.9, -np.pi/2, "leaves", HL)
    s.path([(-3.6, -2.0, .15), (-3.1, -1.6, .2), (-2.6, -1.9, .25), (-2.1, -1.7, .2)], STONE)
    for k, (x, z, r) in enumerate([(-3.5, -3.5, .3), (3.5, -3.5, .3), (3.5, 3.5, .28), (-1.9, 3.6, .24)]): s.bush(x, z, r, LF if k % 2 else LF2, k)
    s.cluster(-1.9, -3.2, 4, .28, seed=5); s.cluster(-1.0, 2.4, 4, .26, seed=6); s.cluster(2.6, 2.7, 3, .25, seed=7)
    s.flowers(-.4, 1.8, 6, 8, .4); s.flowers(2.0, -3.2, 5, 9, .4)
    for x, z, r, h in [(-3.3, .9, .5, .22), (3.4, 1.6, .45, .2), (-1.6, 3.4, .45, .18), (2.9, -1.6, .45, .2)]: s.mound(x, z, r, r*.8, h)
    return s.finish()
def tennis(q):   # Tennis Garden
    s = Scape(RU, MOSS)
    s.mound(-1.6, -2.0, 1.6, 1.6, 1.1, part="Ball_Mounds", mat=BA); s.mound(2.2, -2.4, 1.0, 1.0, .6, part="Ball_Mounds", mat=BA)
    s.slide(-1.6, -1.5, -np.pi/2 + .05, 1.1, mat=HL, wedge_part="Ball_Mounds", wedge_mat=BA)
    s.mound(-3.3, 2.6, .6, 1.3, .4); s.mound(3.3, 1.8, .6, 1.6, .45); s.mound(.4, 3.4, 2.4, .5, .35)
    tn = trimesh.creation.annulus(.30, .38, 1.4, sections=14); tn.apply_transform(Y(np.pi/2)); tn.apply_translation((.6, PAD - E*.5 + .38*np.cos(np.pi/14), -1.0)); s.add("Net_Tunnel", HL, tn, col="mesh")
    s.path([(-3.7, -.1, .15), (-3.2, -.1, .18), (-3.2, .5, .22), (-2.7, .5, .25), (-2.7, 1.1, .22), (-3.2, 1.1, .18)], WH, part="Court_Line_Path")
    s.pods([(.4, .8, .22, .14), (1.0, 1.1, .22, .22), (1.6, .8, .22, .3), (2.2, 1.1, .22, .22)], BA, part="Ball_Pods")
    s.panel(3.0, -.9, -np.pi/2, "hoops", HS); s.panel(-.2, -3.55, 0, "beads", HL)
    s.add("Court_Line", AM, box(-HZ + .1, HZ - .1, PAD - .002, PAD + .002, -.175, -.125), col=None)
    for k, x in enumerate(np.linspace(-3.5, 3.5, 7)): s.bush(x, -3.65, .24, LF if k % 2 else LF2, k)
    s.flowers(.4, 3.4, 8, 8, 1.2); s.cluster(3.3, 1.8, 3, .25, seed=5); s.cluster(-3.3, 2.6, 3, .25, seed=6)
    for x, z, r, h in [(1.4, 2.4, .6, .22), (-.2, 2.4, .5, .2), (3.55, -3.3, .35, .18), (-3.5, -3.0, .4, .2)]: s.mound(x, z, r, r*.8, h)
    return s.finish()
def nook(q):     # Treehouse Nook
    s = Scape(RU, TAN)
    for x, z, rx, rz, h, rot in [(-2.4, -2.3, 1.7, 1.1, 1.2, .5), (.4, -3.1, 1.8, .9, .9, 0), (2.7, -2.0, 1.1, 1.4, .7, -.4), (-3.1, .6, .9, 1.6, .6, 0), (3.1, 1.1, .8, 1.3, .45, 0)]: s.mound(x, z, rx, rz, h, rot=rot)
    s.tunnel(-1.0, -2.6, 1.4, -.35); s.slide(-2.35, -1.65, -np.pi/2 - .45, 1.2, mat=HL)
    s.tree(.3, -.6, 2.6, 8, LF, lean=.25, leaf_len=1.5)
    s.pods([(-1.0, .9, .22, .12), (-.4, 1.4, .2, .2), (.3, 1.6, .2, .28), (1.0, 1.4, .2, .2)], HS)
    s.sandpit(1.4, .5, .55, rim=BARK); s.panel(-1.9, 3.5, 0, "leaves", HL); s.panel(1.6, 3.5, 0, "beads", HS)
    s.path([(-3.5, 2.6, .15), (-2.9, 3.0, .2), (-2.3, 2.7, .25)], BARK)
    for k, (x, z, r) in enumerate([(-3.6, -3.6, .3), (3.6, -3.6, .3), (3.6, 3.6, .3), (-3.6, 3.6, .28), (0, 3.6, .22)]): s.bush(x, z, r, LF2 if k % 2 else LF, k)
    for k, (x, z) in enumerate([(-2.9, -2.7), (.4, -3.2), (2.9, -2.2), (-3.2, .6), (3.2, 1.2)]): s.cluster(x, z, 3, .26, seed=5 + k)
    s.flowers(-.6, 2.6, 6, 12, .4)
    for x, z, r, h in [(-.4, 2.9, .5, .2), (2.9, 3.0, .5, .25), (-2.0, 1.6, .5, .2)]: s.mound(x, z, r, r*.8, h)
    return s.finish()
B = dict(meadow=meadow, forest=forest, riverbed=riverbed, tennis=tennis, nook=nook)
def build(q): return B[q["c"]](q)
VARIANTS = [
    dict(c="meadow", label="Meadow Hills: rolling moss hills, crawl tunnel, mini slide, stepping pods"),
    dict(c="forest", label="Forest Floor: leaf-canopy tree, hollow trunk, mushroom steps, root path"),
    dict(c="riverbed", label="Riverbed: blue river, stepping stones, bank hills, sand beach"),
    dict(c="tennis", label="Tennis Garden: ball hills, court-line path, net tunnel, ball pods"),
    dict(c="nook", label="Treehouse Nook: hill horseshoe den, canopy tree, sand dig, tunnel"),
]
def iso(el, az):
    a, b = np.radians(az), np.radians(el)
    Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]); Rx = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]])
    return Rx @ Ry
def sheet(rep):
    rdir = os.path.join(RENDER_OUT, "toddler_landscape"); fig, axs = plt.subplots(2, 5, figsize=(26, 11.5), facecolor="#F4F2EC")
    for i, (prm, r) in enumerate(zip(VARIANTS, rep)):
        p = recenter(build(prm)); _, geo = export_final(p.P, [f"/tmp/tl_{i}.glb"]); geo = {k: v for k, v in geo.items() if "colonly" not in k}
        for row, (el, az) in enumerate(((20, 30), (34, 205))):
            im = crop(render_view(geo, iso(el, az), size=720, shadow=True)); plt.imsave(os.path.join(rdir, f"v{i+1}_{'hero' if row == 0 else 'back'}.png"), np.clip(im, 0, 1))
            ax = axs[row, i]; ax.imshow(np.clip(im, 0, 1)); ax.axis("off")
            if row == 0: ax.set_title(f"v{i+1}  {prm['label'].split(': ')[0]}\n{prm['label'].split(': ')[1]}\n{r['tris']} tris | {'PASS' if r['passed'] else 'FAIL'}", fontsize=11, color="#222")
    fig.suptitle("Rook | Tennis Tower toddler landscape (round 2) V1-V5 | 8 x 8 m, play heights 0-1.2 m | front 3/4 (top) + back 3/4 (bottom)", fontsize=14, color="#333")
    plt.tight_layout(rect=(0, 0, 1, .95)); sp = os.path.join(rdir, "toddler_landscape_contact_sheet.png"); fig.savefig(sp, dpi=110, facecolor="#F4F2EC"); plt.close(fig); print("SHEET", sp)
if __name__ == "__main__":
    rep = run("toddler_landscape", build, VARIANTS, title="natural play landscape 8 x 8 m", view=iso(20, 30), sheet="toddler_landscape_run_sheet.png")
    sheet(rep)
