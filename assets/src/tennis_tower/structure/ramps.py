"""Rook r4: Rev 3.5 accessible routes (Vance 19fece7, Jared-approved 2026-11-10). Building coords (F1 = 0).
tt_struct_pool_ramp: F1 -> +2.0 pool-deck switchback, Rev 3.6 (ad89c1a): cut X 1..10 Z 26..32 + passage X 8.5..10 Z 32..34.5, four 6 m 1:12 legs
  along X (X 2.5..8.5; L1..L4 at Z 30.5..32 / 29..30.5 / 27.5..29 / 26..27.5), 1.5 m landings, cast spine walls between legs (1.07 m over the higher side), handrails both sides of every leg,
  1.07 m deck-edge guards around the cut.  tt_struct_leisure_ramp: F1 -> +1.0 on the leisure S strip (Z 44.8..46.3), bottom landing
  X 0.3..1.8 Z 44.8..47.0 at the N-deck door, two 6 m legs + 1.5 m mid landing at +0.5, rails both sides, 1.07 m guard on the +Z side.
Style: shared stair / terrace V1 Court Line (slate, stair slate treads, white / amber court-line inlays, alloy posts + ball finials,
TT_GlassScissor infill). No wood, no planter boxes. The deck-fill cuts and the Z 34.5 opening live in build_structure.py."""
from struct_lib import *
from ridge_crown import huv
RH, RR, RO = .865, .02, .065            # handrail height over the walk line, tube radius, centre offset from its wall / post line
GT = 1.07                               # guard height
def wedge(x0, x1, z0, z1, ya, yb, axis="z"):   # solid fill from F1 to a plane rising ya -> yb along axis (z0->z1 or x0->x1)
    P = []
    for x in (x0, x1):
        for z in (z0, z1):
            t = (z - z0)/(z1 - z0) if axis == "z" else (x - x0)/(x1 - x0); P += [(x, -E, z), (x, ya + (yb - ya)*t, z)]
    return huv(P)
def lerp(a, b, ya, yb):
    return lambda s: ya + (yb - ya)*(s - a)/(b - a)
def strip(x0, x1, z0, z1, f, axis, dy=.003):   # thin inlay on a sloped / flat surface f(s) (s along axis)
    P = []
    for x in (x0, x1):
        for z in (z0, z1):
            s = z if axis == "z" else x; P += [(x, f(s) - E, z), (x, f(s) + dy, z)]
    return huv(P)
class Kit:
    def __init__(s): s.I = []; s.C = []
    def add(s, pn, mk, *ms): s.I += [(pn, mk, m) for m in ms]
    def col(s, *ms): s.C += list(ms)
    def guard(s, a, b, line, axis, base, top, posts_at_ends=(True, True), kerb=True):
        """1.07 m Court Line guard along axis ('x': s = X at Z=line; 'z': s = Z at X=line). base(s): standing surface, top(s): rail top."""
        L = b - a; n = max(1, int(np.ceil(L/1.5))); S = np.linspace(a, b, n + 1)
        P = lambda s, y: (s, y, line) if axis == "x" else (line, y, s)
        posts = [t for i, t in enumerate(S) if (i or posts_at_ends[0]) and (i < n or posts_at_ends[1])]
        kb = .1 if kerb else 0.0       # posts stand on the kerb top
        s.add("Guard_Posts", ALY, *[tube(P(t, base(t) + kb - E), P(t, top(t) - .03 + E), .035, 8) for t in posts])
        s.add("Guard_Ball_Finials", BA, *[node(P(t, top(t) + .05 - E), .05, 0) for t in posts])
        s.add("Guard_Rail", ST, huv([P(t, top(t) + o) for t in (a, b) for o in (-.03, 0)] + [(P(t, top(t) - .015)[0] + (0 if axis == "x" else d), top(t) - .015, P(t, 0)[2] + (d if axis == "x" else 0)) for t in (a, b) for d in (-.03, .03)]))
        PA = []
        for u, v in zip(S[:-1], S[1:]):
            u2, v2 = u + .045, v - .045
            if v2 - u2 < .05: continue
            q = []
            for t in (u2, v2):
                for y in (base(t) + (.12 if kerb else .06), top(t) - .05):
                    for d in (-.01, .01): q.append((t, y, line + d) if axis == "x" else (line + d, y, t))
            PA.append(huv(q))
        s.add("Guard_Pane_Scissor", SCR, *PA)
        if kerb:
            q = []
            ka, kb2 = a + (0 if posts_at_ends[0] else .05), b - (0 if posts_at_ends[1] else .05)   # stop short of the neighbour run's kerb
            for t in (ka, kb2):
                for y in (base(t) - E, base(t) + .1):
                    for d in (-.05, .05): q.append((t, y, line + d) if axis == "x" else (line + d, y, t))
            s.add("Guard_Kerb", SL, huv(q))
        q = []
        for t in (a, b):
            for y in (base(t), top(t)):
                for d in (-.05, .05): q.append((t, y, line + d) if axis == "x" else (line + d, y, t))
        s.col(huv(q))
    def rail(s, pts, line, axis, mount=None, every=1.5):
        """handrail polyline [(s, y)] at line; brackets back to the mount line every ~1.5 m."""
        P = lambda t, y: (t, y, line) if axis == "x" else (line, y, t)
        s.add("Handrail", ST, *[tube(P(*p), P(*q), RR, 8) for p, q in zip(pts, pts[1:])])
        if mount is None: return
        B = []
        for p, q in zip(pts, pts[1:]):
            n = max(1, int(round(abs(q[0] - p[0])/every)))
            for k in range(n):
                t = p[0] + (q[0] - p[0])*(k + .5)/n; y = p[1] + (q[1] - p[1])*(k + .5)/n
                a = (t, y - .09, mount) if axis == "x" else (mount, y - .09, t); c = (t, y - RR + .002, line) if axis == "x" else (line, y - RR + .002, t)
                B.append(tube(a, c, .009, 6))
        s.add("Handrail_Brackets", G, *B)

def pool_ramp():   # r4b: Rev 3.6 (ad89c1a) layout, legs along X north of the 3 m board
    k = Kit(); C = lambda *ms: k.col(*[m.copy() for m in ms])
    L1 = lerp(2.5, 8.5, .5, 0); L2 = lerp(2.5, 8.5, .5, 1.0); L3 = lerp(2.5, 8.5, 1.5, 1.0); L4 = lerp(2.5, 8.5, 1.5, 2.0)
    legs = [((30.55, 32.0), L1), ((29.05, 30.45), L2), ((27.55, 28.95), L3), ((26.0, 27.45), L4)]   # Z bands between spine / cut faces
    # legs run 3 mm into their landings (no walk-line crack); 6 mm / 3 mm side reveals keep wedge, landing and wall faces off each other's planes
    W = [wedge(2.497, 8.503, z0 + .006, z1 - .006, f(2.497), f(8.503), "x") for (z0, z1), f in legs]
    W[0] = wedge(2.497, 8.5, 30.556, 31.994, L1(2.497), 0.0, "x")                                        # L1 ends on the F1 bottom landing
    g = .003
    LD = [box(1.0, 2.5, -E, .5, 29.05 + g, 32.0), box(1.0, 2.5, -E, 1.5, 26.0, 28.95 - g),                # W turning landings +0.5 / +1.5
          box(8.5, 10.0, -E, 1.0, 27.55 + g, 30.45 - g), box(8.5, 10.0, -E, 2.0, 26.0, 27.45 - g)]        # E +1.0 turn, +2.0 top (exits +X)
    k.add("Ramp_Legs", SSL, *W); k.add("Ramp_Landings", SSL, *LD); C(*W, *LD)
    sp = lambda x0, x1, z, y0, y1: huv([(x, y, zz) for x, yt in ((x0, y0), (x1, y1)) for zz in (z - .05, z + .05) for y in (-E, yt)])
    SP = [sp(2.5, 8.5, 30.5, 1.57, 2.07), box(8.5, 10.0, -E, 2.07, 30.45, 30.55),          # L1 | L2, then F1 bottom landing | +1.0
          box(1.0, 2.5, -E, 2.57, 28.95, 29.05), sp(2.5, 8.497, 29.0, 2.57, 2.0703),          # +0.5 | +1.5 landings, then L2 | L3
          sp(2.5, 8.5, 27.5, 2.57, 3.07), box(8.5, 10.0, -E, 3.07, 27.45, 27.55)]             # L3 | L4, then +1.0 | +2.0 top
    k.add("Ramp_Walls", SL, *SP); C(*SP)
    k.add("Spine_Caps", ALY, *[huv([(x, y, z) for x in (m.bounds[0][0], m.bounds[1][0]) for z in (m.bounds[0][2] - .01, m.bounds[1][2] + .01)
                                    for y in (np.interp(x, *zip(*sorted({(round(v[0], 3), round(v[1], 3)) for v in m.vertices if v[1] > .1}))) + o for o in (-E, .03))])
                                for m in SP])
    WL, AL = [], []
    for (z0, z1), f in legs:
        c = (z0 + z1)/2; WL.append(strip(2.6, 8.4, c - .025, c + .025, f, "x"))
        AL += [strip(2.5, 2.55, z0 + .05, z1 - .05, f, "x"), strip(8.45, 8.5, z0 + .05, z1 - .05, f, "x")]
    k.add("Court_Lines", WH, *WL); k.add("Court_Line_Amber", AM, *AL)
    for (z0, z1), f in legs:   # handrails both sides of every leg, 0.3 m extensions onto the landings
        pts = [(2.2, f(2.5) + RH), (2.5, f(2.5) + RH), (8.5, f(8.5) + RH), (8.8, f(8.5) + RH)]
        k.rail(pts, z0 + RO, "x", z0); k.rail(pts, z1 - RO, "x", z1)
    D = lambda s: 2.0; T = lambda s: 2.0 + GT
    k.guard(25.9, 32.1, .9, "z", D, T)                                           # W edge
    k.guard(.9, 10.0, 25.9, "x", D, T, (False, True))                            # S edge, ends at the top-landing exit
    k.guard(.9, 8.4, 32.1, "x", D, T, (False, True))                             # N edge
    k.guard(32.1, 34.17, 8.4, "z", D, T, (False, True))                          # passage W edge
    k.guard(27.55, 34.17, 10.1, "z", D, T, (True, True))                         # E edge: +1.0 turn, F1 bottom landing, passage
    return k

def leisure_ramp():
    k = Kit(); C = lambda *ms: k.col(*[m.copy() for m in ms])
    a = lerp(1.8, 7.8, 0, .5); b = lerp(9.3, 15.3, .5, 1.0)
    W = [wedge(1.8, 7.803, 44.803, 46.297, 0, a(7.803), "x"), wedge(9.297, 15.3, 44.803, 46.297, b(9.297), 1.0, "x")]   # legs run 3 mm into the landing
    LD = [box(7.8, 9.3, -E, .5, 44.801, 46.299)]
    k.add("Ramp_Legs", SSL, *W); k.add("Ramp_Landings", SSL, *LD); C(*W, *LD)
    k.add("Court_Lines", WH, strip(1.9, 15.2, 45.525, 45.575, lambda s: a(s) if s <= 7.8 else (.5 if s <= 9.3 else b(s)), "x") if False else strip(1.9, 7.7, 45.525, 45.575, a, "x"),
          strip(9.4, 15.2, 45.525, 45.575, b, "x"))
    k.add("Court_Line_Amber", AM, *[strip(x, x + .05, 44.85, 46.18, f, "x") for x, f in ((1.8, a), (7.75, a), (9.3, b), (15.25, b))])
    surf = lambda s: 0.0 if s <= 1.8 else (a(s) if s <= 7.8 else (.5 if s <= 9.3 else (b(s) if s <= 15.3 else 1.0)))
    T = lambda s: 1.0 + GT
    k.guard(1.77, 15.3, 46.24, "x", surf, T, (True, True), kerb=False)          # +Z side along the drop from the +1.0 strip
    k.guard(46.24, 46.94, 1.77, "z", lambda s: 0.0, T, (False, True))           # landing / deck-strip edge at X 1.8
    k.guard(.96, 1.77, 46.94, "x", lambda s: 0.0, T, (True, False))            # landing / river wall (lining Z 47.0..47.06), kerb 0.01 off it
    k.guard(.2, .96, 47.06, "x", lambda s: 1.0, T, (True, True))               # W deck strip X 0..1 edge over the landing
    pts = [(1.5, RH), (1.8, RH), (7.8, .5 + RH), (9.3, .5 + RH), (15.3, 1.0 + RH), (15.6, 1.0 + RH)]
    k.rail(pts, 44.8 + RO, "x", 44.8)                                             # S: on the tank-bay wall face
    k.rail([(1.8, RH)] + pts[2:5], 46.24 - RO, "x", 46.24 - .035)                # N: on the guard posts
    return k

def export(name, k, REP, LAY, note):
    groups = {}
    for pn, mk, m in k.I: groups.setdefault((pn, mk), []).append(m)
    return export_chunk(name, [(pn, mk, ms) for (pn, mk), ms in groups.items()], [("Ramp-colonly", k.C)], REP, layout=LAY, note=note)

def grade(pts, meshes, y0=0.0):
    """ray-sample the walk line on the collider set every 0.1 m; worst grade over 0.5 m windows (1:N)."""
    col = trimesh.util.concatenate(meshes); R = trimesh.ray.ray_triangle.RayMeshIntersector(col); S = []; y = y0
    for (ax, az), (bx, bz) in zip(pts, pts[1:]):
        n = max(2, int(np.hypot(bx - ax, bz - az)/.1))
        for i in range(n):
            x, z = ax + (bx - ax)*i/n, az + (bz - az)*i/n; l, _, _ = R.intersects_location([[x, y + .35, z]], [[0, -1, 0]], multiple_hits=False)
            if len(l): y = l[0][1]; S.append(y)
    S = np.array(S); g = np.abs(S[5:] - S[:-5]).max()/.5
    return dict(worst_grade_1_in=round(1/max(g, 1e-9), 2), top=round(float(S[-1]), 3))

def walk(p, path, y0=0.0, step=.03, head=2.1, ds=.05):
    """modlib.walk_check with stacked colliders: floor = highest collider hit below the probe (the ramp casts sit on the F1 slab,
    so first-hit order is not nearest), headroom = lowest visual hit above the walk line. Also reports the worst 1:N grade (0.5 m window)."""
    col = trimesh.util.concatenate([m for k, (_, m) in p.P.items() if "colonly" in k]); vis = trimesh.util.concatenate([m for k, (_, m) in p.P.items() if "colonly" not in k])
    fl, hv = trimesh.ray.ray_triangle.RayMeshIntersector(col), trimesh.ray.ray_triangle.RayMeshIntersector(vis)
    pts = []; y = y0; w = dict(step=0.0, head=9.0, nofloor=0); Y = []
    for (ax, az), (bx, bz) in zip(path, path[1:]):
        n = max(2, int(np.hypot(bx - ax, bz - az)/ds)); pts += [(ax + (bx - ax)*k/n, az + (bz - az)*k/n) for k in range(n)]
    for i, (x, z) in enumerate(pts):
        l, _, _ = fl.intersects_location([[x, y + step + .05, z]], [[0, -1, 0]], multiple_hits=True)
        if not len(l): w["nofloor"] += 1; continue
        f = float(l[:, 1].max())
        if i: w["step"] = max(w["step"], abs(f - y))
        y = f; Y.append(y); u, _, _ = hv.intersects_location([[x, y + .05, z]], [[0, 1, 0]], multiple_hits=True)
        if len(u): w["head"] = min(w["head"], float(u[:, 1].min() - y))
    Y = np.array(Y); k = int(round(.5/ds)); g = np.abs(Y[k:] - Y[:-k]).max()/.5
    w.update(grade_1_in=round(1/max(g, 1e-9), 2), top_y=round(float(y), 3), samples=len(Y))
    w["pass"] = bool(w["nofloor"] == 0 and w["step"] <= step and w["head"] >= head and w["grade_1_in"] >= 12 - .05)
    return {kk: (round(v, 3) if isinstance(v, float) else v) for kk, v in w.items()}
