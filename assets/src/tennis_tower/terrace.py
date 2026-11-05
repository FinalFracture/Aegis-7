"""Rook: Tennis Tower terrace decks + ramps kit (spec §3.3 / §3.8 Rev 2.7): West Arrival terrace (48 x 48) and East Plaza (30 x 48) decks at
+4.0 HD, East Spine ramp 1:20 (12 m wide, 80 m, +4.0 -> grade), 1:12 aprons at the S/N faces (~1 m). Spec gives no rail rules; used IBC 2021
(*real-world ref*): 1.07 m guards wherever the drop > 0.76 m (terrace edge over the plinth skirt, ramp sides), pickets < 100 mm apart, no
handrail on 1:20 (a walking surface, not a ramp); the 1:12 apron rises < 0.15 m so needs no handrail.
Pieces (each a GLB, pivot bottom centre, +Z out): deck 4 x 4 (0.30 deep; place at +3.70), edge 4 m (deck strip + coping kerb + guard, sits
on tt_plinth_skirt's cap), ramp 4 m run x 6 m half-width (drop 0.20, mirror for the other half; chain every 4 m, -0.20 each), apron 4 x 1 m.
Families V1..V5 share the #74/#75/#76 language. No wood, no planter boxes. Run: python3 terrace.py"""
from modlib import *
import modlib
from restroom_extras import crest
from ridge_crown import huv
modlib._m("tt_paver", "TT_PaverStone", (.60, .59, .55), 0, .85); modlib._m("tt_river", "TT_RiverInlayBlue", (.22, .46, .70), 0, .35)
PV, RV = "tt_paver", "tt_river"; DK = .30; SLOPE = 1/20; APR = 1/12
def pavers(p, x0, x1, z0, z1, n, m, yb, yt, mats=(PV, SL), skip=None, ytop=None):
    xs = np.linspace(x0, x1, n + 1); zs = np.linspace(z0, z1, m + 1); A, B = [], []
    for i in range(n):
        for j in range(m):
            a, b, c, d = xs[i] + .005, xs[i+1] - .005, zs[j] + .005, zs[j+1] - .005
            if skip and skip((a + b)/2, (c + d)/2): continue
            if ytop is None: t = box(a, b, yb, yt, c, d)
            else: t = huv([(x, y, z) for x in (a, b) for z in (c, d) for y in (yb, ytop(x, z))])
            (A if (i + j) % 2 == 0 else B).append(t)
    if A: p.add("Pavers_A", mats[0], *A)
    if B: p.add("Pavers_B", mats[1], *B)
def tufts_at(pts, y, rng):
    T = []
    for (x, z) in pts: T += [leaf((x + .015*np.cos(a), y - .004, z + .015*np.sin(a)), .14 + .05*rng.random(), .028, yaw=a, pitch=-.25, t=.006) for a in (0, 2.1, 4.2)]
    return T
def guard(p, q, x0, x1, z, yb, slope=0.0, xref=0.0):   # 1.07 m guard (posts, top + mid rails, pickets at 0.095 m), optional slope along X
    yy = lambda x: yb - slope*(x - xref); th = q["theme"]; F = []
    posts = [x for x in np.arange(x0 + .5, x1 - .3, 1.0)]
    for x in posts:
        if th == "branch":   # Branch Fin post: trunk + Y fork into the top rail
            n = (x, yy(x) + .7, z); F += [tube((x, yy(x) - E, z), n, .04, 8), node(n, .055, 0), tube(n, (x - .3, yy(x - .3) + 1.07, z), .025, 6), tube(n, (x + .3, yy(x + .3) + 1.07, z), .025, 6), tube(n, (x, yy(x) + 1.07, z), .03, 6)]
        else: F.append(tube((x, yy(x) - E, z), (x, yy(x) + 1.07, z), .035, 8))
    F += [tube((x0 + .001, yy(x0) + 1.07, z), (x1 - .001, yy(x1) + 1.07, z), .03, 8), tube((x0 + .001, yy(x0) + .16, z), (x1 - .001, yy(x1) + .16, z), .02, 6)]
    for x in np.arange(x0 + .05, x1 - .02, .095):
        if any(abs(x - px) < .06 for px in posts): continue
        F.append(box(x - .006, x + .006, yy(x) + .16 - .004, yy(x) + 1.07 - .02, z - .006, z + .006) if not slope else tube((x, yy(x) + .16, z), (x, yy(x) + 1.05, z), .007, 4))
    p.add("Guard_Frame", G if th in ("branch", "river") else ALY, *F)
    if th == "court": p.add("Post_Ball_Finials", BA, *[node((x, yy(x) + 1.07 + .03 + .05 - E, z), .05, 1) for x in posts])
    if th == "branch": p.add("Post_Leaf_Crests", LF, *[crest((x, yy(x) + 1.07 + .03 - E, z)) for x in posts])
    if th == "boulder": p.add("Post_Holds", BA, *[node((x, yy(x) + .6, z + .035 + .045 - .006), .045, 1) for x in posts])
    p.add("Guard-convcolonly", ALY, huv([(x, yy(x) + o, z + dz) for x in (x0, x1) for o in (0, 1.1) for dz in (-.05, .05)]))
def theme_deck(p, q, x0, x1, z0, z1, rng, yb=.2, yt=DK):
    th = q["theme"]; skip = None
    xs = np.linspace(x0, x1, 9); zs = np.linspace(z0, z1, 9)
    if th == "river":   # river channel along X (rows 3-4 of 8), tiles seamlessly in X
        pavers(p, x0, x1, z0, z1, 8, 8, yb, yt, skip=lambda x, z: zs[3] < z < zs[5])
        za, zb = zs[3] + .007, zs[5] - .007; p.add("River_Inlay", RV, box(x0, x1, yb, yt - .025, za, zb))
        p.add("River_Pebbles", ST, *[node((x, yt - .025 + r*.75 - .004, z), r, 0) for x, z, r in zip(np.linspace(x0 + .2, x1 - .2, 14), rng.uniform(za + .08, zb - .08, 14), rng.uniform(.035, .06, 14))])
        return
    if th == "green":   # grass strip along Z (cols 3-4 of 8)
        pavers(p, x0, x1, z0, z1, 8, 8, yb, yt, mats=(PV, PV), skip=lambda x, z: xs[3] < x < xs[5])
        xa, xb = xs[3] + .007, xs[5] - .007; p.add("Grass_Strip", SO, box(xa, xb, yb, yt - .03, z0, z1 - .003))
        mz = [z0 + (z1 - z0)*f for f in (.25, .75)]
        p.add("Moss_Clumps", LF, *[clump(((xa + xb)/2, yt - .03 + .1*.8, z), .1, i) for i, z in enumerate(mz)])
        tz = [z for z in np.linspace(z0 + .15, z1 - .15, 12) if all(abs(z - m) > .25 for m in mz)]
        p.add("Grass_Tufts", LF2, *tufts_at([((xa + xb)/2 + rng.uniform(-.2, .2), z) for z in tz], yt - .03, rng))
        return
    pavers(p, x0, x1, z0, z1, 8, 8, yb, yt)
    if th == "court":
        L = [box(x0 + .37, x1 - .3, yt - E, yt + .004, (z0 + z1)/2 - .025, (z0 + z1)/2 + .025), box((x0 + x1)/2 - .025, (x0 + x1)/2 + .025, yt - E, yt + .004, z0 + .3, (z0 + z1)/2 - .025 - .002)]
        p.add("Court_Lines", WH, *L); p.add("Court_Line_Amber", AM, box(x0 + .3, x0 + .35, yt - E, yt + .004, z0 + .3, z1 - .3))
    if th == "branch":
        R = []; c = ((x0 + x1)/2, yt + .018 - .006, (z0 + z1)/2)
        L1 = min(1.1, (z1 - z0)/2 - .55); L2 = L1*.45
        for a in np.linspace(0, 2*np.pi, 6)[:-1]:
            e1 = (c[0] + L1*np.cos(a), c[1], c[2] + L1*np.sin(a)); R += [tube(c, e1, .018, 4)]
            for s_ in (-.5, .5): R.append(tube(e1, (e1[0] + L2*np.cos(a + s_), c[1], e1[2] + L2*np.sin(a + s_)), .012, 4))
        p.add("Root_Relief", G, *R, node((c[0], yt + .04 - .006, c[2]), .04, 0))
    if th == "boulder":
        B = []
        for j, (x, z, s) in enumerate(((x0 + .9, z1 - .9, .5), (x0 + 1.5, z1 - .6, .35), (x0 + .5, z1 - 1.5, .3))):
            ang = np.linspace(0, 2*np.pi, 7)[:-1] + rng.uniform(0, 1); P = [(x + .55*s*np.cos(t), yt - .008, z + .5*s*np.sin(t)) for t in ang]
            P += [(x + s*np.cos(t + .3)*rng.uniform(.85, 1.1), yt + .25*s, z + .9*s*np.sin(t + .3)*rng.uniform(.85, 1.1)) for t in ang]
            P += [(x + rng.uniform(-.3, .3)*s, yt + rng.uniform(.6, .8)*s, z + rng.uniform(-.3, .3)*s) for _ in range(3)]; B.append(huv(P))
        p.add("Boulder_Seats", SL, *B)
        bc = [(m.centroid[0], m.centroid[2], m.extents[0]) for m in B]
        p.add("Grit_Dots", ST, *[node((x, yt + .012 - .005, z), .012, -1) for x, z in rng.uniform([x0 + .2, z0 + .2], [x1 - .2, z1 - .2], (24, 2)) if all(np.hypot(x - a_, z - b_) > e_*.7 for a_, b_, e_ in bc)])
def build(q):
    p = Part(); rng = np.random.default_rng(q.get("seed", 3)); pc = q["piece"]; th = q["theme"]
    if pc == "deck":
        h = 2.0; X0, X1 = -h + .001, h - .001
        p.add("Deck_Slab", G, box(X0, X1, 0, .2 + .002, X0, X1)); p.add("Deck_Drain", SSL, box(X0 + .1, X1 - .1, .2 - .03, .2 + .004, X0 + .04, X0 + .09))
        theme_deck(p, q, X0, X1, X0 + .1, X1, rng)
        p.add("Deck-colonly", SL, box(X0, X1, 0, DK, X0, X1))
    if pc == "edge":
        h = 2.0; X0, X1 = -h + .001, h - .001; zc0, zc1 = .25, .9   # coping front at z .9 = tt_plinth_skirt cap front (face line z 0)
        p.add("Deck_Slab", G, box(X0, X1, 0, .2 + .002, -1.6, zc0 - .002))
        theme_deck(p, q, X0, X1, -1.6, zc0 - .004, rng)
        p.add("Coping_Kerb", SL, box(X0, X1, 0, .36, zc0, zc1), box(X0, X1, .36 - E, .4, zc0 + .04, zc1 - .1))
        p.add("Coping_Line", AM if th != "river" else RV, box(X0, X1, .28, .32, zc1 - E, zc1 + .007))
        guard(p, q, X0, X1, .62, .4)
        if th == "green": p.add("Guard_Hedge", LF, *[clump((x, .4 + .16 - .008, .34), .16, i) for i, x in enumerate(np.arange(-1.75, 1.8, .35))])
        if th == "river": p.add("Kerb_Stones", ST, *[node((x, .4 + .04 - .004, .82), .04, 0) for x in np.arange(-1.8, 1.85, .3)])
        p.add("Edge-colonly", SL, box(X0, X1, 0, .36, -1.6, zc1))
    if pc == "ramp":   # 4 m run along X (down toward +X), 6 m half width (z -3..+2.4 walk, kerb + guard at z 2.4..3.0)
        h = 2.0; X0, X1 = -h + .001, h - .001; yt = lambda x, z=0: DK + .2 - SLOPE*(x - X0)
        p.add("Ramp_Body", G, huv([(x, y, z) for x in (X0, X1) for z in (-2.999, 2.4 - .002) for y in (0, yt(x) - .1 + .002)]))
        if th == "river":
            p.add("Runnel", RV, huv([(x, y, z) for x in (X0, X1) for z in (2.0, 2.4 - .004) for y in (yt(x) - .1, yt(x) - .03)]))
            pavers(p, X0, X1, -2.999, 2.0 - .004, 4, 5, 0, 0, ytop=lambda x, z: yt(x)) if False else None
        zmax = 2.0 - .004 if th in ("river", "green") else 2.4 - .004
        A, B = [], []
        for i, (xa, xb) in enumerate(zip(np.linspace(X0, X1, 5)[:-1], np.linspace(X0, X1, 5)[1:])):
            for j, (za, zb) in enumerate(zip(np.linspace(-2.999, zmax, 6)[:-1], np.linspace(-2.999, zmax, 6)[1:])):
                t = huv([(x, y, z) for x in (xa + .005, xb - .005) for z in (za + .005, zb - .005) for y in (yt(x) - .1, yt(x))]); (A if (i + j) % 2 == 0 else B).append(t)
        p.add("Pavers_A", PV, *A); p.add("Pavers_B", SL if th != "green" else PV, *B)
        if th == "green":
            p.add("Verge_Soil", SO, huv([(x, y, z) for x in (X0, X1) for z in (2.0, 2.4 - .004) for y in (yt(x) - .1, yt(x) - .03)]))
            p.add("Verge_Moss", LF, *[clump((x, yt(x) - .03 + .12*.8, 2.2), .12, i) for i, x in enumerate(np.arange(-1.7, 1.8, .42))])
        if th == "court": p.add("Court_Lines", WH, *[huv([(x, y, z) for x in (X0, X1) for z in (z0, z0 + .05) for y in (yt(x) - E, yt(x) + .004)]) for z0 in (-.025,)])
        if th == "boulder": p.add("Grit_Dots", ST, *[node((x, yt(x) + .012 - .005, z), .012, -1) for x, z in rng.uniform([X0 + .1, -2.8], [X1 - .1, 2.2], (24, 2)) if True])
        if th == "branch": p.add("Root_Relief", G, *[tube((x, yt(x) + .008, -2.6), (x + .8, yt(x + .8) + .008, 2.0), .014, 4) for x in (-1.9, -.4) ])
        p.add("Ramp_Kerb", SL, huv([(x, y, z) for x in (X0, X1) for z in (2.4, 3.0 - .001) for y in (0, yt(x) + .06)]))
        guard(p, q, X0, X1, 2.75, yt(X0) + .06, slope=SLOPE, xref=X0)
        if th == "boulder":
            KB = []
            for x in (-1.3, .2, 1.4):
                P = rng.normal(size=(10, 3))*[.25, .12, .1]; P[:, 1] = np.abs(P[:, 1]); P[:, 1] -= P[:, 1].min(); P[:, 2] = np.clip(P[:, 2], -.08, .08)
                P += [x, 0, 2.53]; P[:, 0] = np.clip(P[:, 0], X0 + .01, X1 - .01); P[:, 1] += [yt(px) + .06 - .006 - SLOPE*.0 for px in P[:, 0]]; KB.append(huv(P))
            p.add("Kerb_Boulders", SSL, *KB)
        p.add("Ramp-colonly", SL, huv([(x, y, z) for x in (-2.0, 2.0) for z in (-3.0, 2.4) for y in (0, yt(x))]))
        p.add("Kerb-colonly", SL, huv([(x, y, z) for x in (X0, X1) for z in (2.4, 3.0) for y in (0, yt(x) + 1.1)]))
    if pc == "apron":  # 4 m along the face x 1.0 m deep, 1:12 up toward the face (-Z): +0.083 over 1.0 m
        h = 2.0; X0, X1 = -h + .001, h - .001; Z0, Z1 = -.5, .5; yt = lambda z: .05 + APR*(Z1 - z)
        p.add("Apron_Body", G, huv([(x, y, z) for x in (X0, X1) for z in (Z0, Z1 - .12) for y in (0, yt(z) - .04 + .002)]))
        A, B = [], []
        for i, (xa, xb) in enumerate(zip(np.linspace(X0, X1, 9)[:-1], np.linspace(X0, X1, 9)[1:])):
            for j, (za, zb) in enumerate(((Z0 + .06, 0), (0, Z1 - .12))):
                t = huv([(x, y, z) for x in (xa + .005, xb - .005) for z in (za + .005, zb - .005) for y in (yt(z) - .04, yt(z))]); (A if (i + j) % 2 == 0 else B).append(t)
        p.add("Pavers_A", PV, *A); p.add("Pavers_B", SL if th != "green" else PV, *B)
        p.add("Drain_Grate", SSL, box(X0, X1, yt(Z0) - .046, yt(Z0) - .004, Z0 + .002, Z0 + .055))
        p.add("Nosing_Line", AM if th in ("court", "boulder") else (RV if th == "river" else LF), box(X0 + .003, X1 - .003, 0, yt(Z1 - .12) + .002, Z1 - .118, Z1 + .012))
        if th == "green": p.add("Edge_Tufts", LF2, *tufts_at([(x, Z1 + .0 - .06) for x in np.arange(-1.8, 1.85, .45)], yt(Z1 - .12) + .002, rng))
        if th == "river": p.add("Apron_Pebbles", ST, *[node((x, yt(Z1 - .12) + .002 + .025 - .004, Z1 - .06), .025, 0) for x in np.arange(-1.85, 1.9, .25)])
        if th == "branch": p.add("Apron_Crests", LF, *[crest((x, yt(Z1 - .12) + .002 - E, Z1 - .06)) for x in (-1.5, -.5, .5, 1.5)])
        if th == "boulder": p.add("Grit_Dots", ST, *[node((x, yt(z) + .012 - .005, z), .012, -1) for x, z in rng.uniform([X0 + .1, Z0 + .1], [X1 - .1, Z1 - .2], (16, 2))])
        if th == "court": p.add("Court_Lines", WH, box(X0, X1, yt(-.2) - E, yt(-.2) + .004 + .001, -.225, -.175))
        p.add("Apron-colonly", SL, huv([(x, y, z) for x in (-2.0, 2.0) for z in (Z0, Z1) for y in (0, yt(z))]))
    return p
THEMES = [("court", "Court Line", "slate + paver checker, white/amber court-line inlays, alloy pickets with ball finials"),
          ("river", "Riverbed", "blue river inlay with pebbles through the pavers, gunmetal guard, river-stone kerb, ramp runnel"),
          ("green", "Green Grid", "grass strip + tufts in the paver grid, hedge behind the guard, moss verge on the ramp"),
          ("branch", "Branch Rail", "Branch Fin Y-fork guard posts with leaf crests, gunmetal root relief in the pavers"),
          ("boulder", "Boulder Terrace", "sculpted boulder seats, grit-dot grip, tennis-ball holds on posts, boulder kerb (#76)")]
PIECES = ("deck", "edge", "ramp", "apron")
def V(pc): return [dict(label=f"{n}: {d}", theme=t, piece=pc, seed=3 + i) for i, (t, n, d) in enumerate(THEMES)]
def place(A, part, t, tag, mirror_z=None):
    for n, (mk, m) in part.P.items():
        if "colonly" in n: continue
        m2 = m.copy()
        if mirror_z is not None:
            m2.vertices[:, 2] = 2*mirror_z - m2.vertices[:, 2]; m2.invert()
        m2.apply_translation(t); m2.metadata["uv"] = m.metadata.get("uv", np.zeros((len(m.vertices), 2))); A[f"{tag}_{n}"] = (mk, m2)
def seam(prm, shifts, mirror=None):
    A = {}; place(A, build(prm), (0, 0, 0), "T0")
    for k, s in enumerate(shifts): place(A, build(prm), s, f"T{k+1}", mirror)
    chk = cc.check(A, n_samp=200); bad = [o for o in chk["overlap"] if not o[3] and o[0][:2] != o[1][:2]]; cop = [c for c in chk["coplanar"] if c[0][:2] != c[1][:2]]
    return not bad and not cop, bad[:2], cop[:2]
def walk(prm):
    pc = prm["piece"]
    if pc == "ramp":
        P = Part(); a, b = build(prm), build(prm)
        for n, (mk, m) in a.P.items(): P.add(f"A_{n}", mk, m)
        for n, (mk, m) in b.P.items(): m2 = m.copy(); m2.apply_translation((4.0, -.2, 0)); m2.metadata["uv"] = m.metadata.get("uv"); P.add(f"B_{n}", mk, m2)
        r = walk_check(P, [(-1.95, 0), (5.95, 0)], y0=DK + .2, step=.03); r["grade_1_in"] = round(8.0/ max(1e-6, (DK + .2) - r["top_y"]), 1); return r
    if pc == "apron":
        r = walk_check(build(prm), [(0, .49), (0, -.49)], y0=.05, step=.03); r["grade_1_in"] = round(1.0/max(1e-6, r["top_y"] - .05), 1) if r["top_y"] > .05 else None; return r
    return None
if __name__ == "__main__":
    import facade_bay_final as FB, plinth_skirt_final as PS
    REP = {}
    for pc in PIECES:
        REP[pc] = run("terrace", build, V(pc), title=f"terrace {pc}", suffix=f"_{pc}", names=[f"v{i+1}_{pc}" for i in range(5)], sheet=f"terrace_run_{pc}.png")
    SE, WK = {}, {}
    for i in range(5):
        d, e_, r, a = [V(pc)[i] for pc in PIECES]
        SE[i] = dict(deck_x=seam(d, [(4, 0, 0)])[0], deck_z=seam(d, [(0, 0, 4)])[0], edge_x=seam(e_, [(4, 0, 0)])[0], ramp_chain=seam(r, [(4, -.2, 0)])[0], ramp_mirror=seam(r, [(0, 0, 0)], mirror=-3.0)[0], apron_x=seam(a, [(4, 0, 0)])[0])
        WK[i] = dict(ramp=walk(r), apron=walk(a)); print("SEAM", i + 1, SE[i], "WALK", WK[i])
    json.dump(dict(rep=REP, seams=SE, walk=WK), open(os.path.join(RENDER_OUT, "terrace", "report_all.json"), "w"), indent=1, default=str)
    Ry = lambda el, az: (lambda a, b: np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]) @ np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]))(np.radians(az), np.radians(el))
    rdir = os.path.join(RENDER_OUT, "terrace"); fig, axs = plt.subplots(5, 5, figsize=(30, 33), facecolor="#F4F2EC")
    ang = dict(deck=(32, 30), edge=(14, 30), ramp=(18, 35), apron=(25, 30))
    for i in range(5):
        for row, pc in enumerate(PIECES):
            prm = V(pc)[i]; p = recenter(build(prm)); _, geo = export_final(p.P, [f"/tmp/tr_{i}_{pc}.glb"]); geo = {k: v for k, v in geo.items() if "colonly" not in k}
            im = crop(render_view(geo, Ry(*ang[pc]), size=560, shadow=False, glass_alpha=.35)); axs[row, i].imshow(np.clip(im, 0, 1)); axs[row, i].axis("off")
            r = REP[pc][i]; extra = ""
            if pc in ("ramp", "apron"): w = WK[i][pc]; extra = f" | walk {'PASS' if w['pass'] else 'FAIL'} 1:{w['grade_1_in']}"
            axs[row, i].set_title((f"v{i+1} {THEMES[i][1]}\n{THEMES[i][2]}\n" if row == 0 else "") + f"{pc}: {r['tris']} tris | {'PASS' if r['passed'] else 'FAIL'}{extra}", fontsize=9)
        # vignette: facade bays at F1 (+4.0) on the deck, 2 rows of deck tiles, edge + guard over a trimmed plinth skirt (top 3.7), 2 ramp tiles down to the east
        A = {}; d, e_, r = V("deck")[i], V("edge")[i], V("ramp")[i]
        for k in range(3):
            x = 2 + 4*k
            place(A, FB.build(dict(width=4.0)), (x, 4.0, -9.25), f"F{k}")
            for j in range(2): place(A, build(d), (x, 3.7, -7.0 + 4*j + 0), f"D{k}{j}")
            place(A, build(e_), (x, 3.7, 1.6 - 1.6 + 0), f"E{k}"); place(A, PS.build(dict(width=4.0, seed=7)), (x, -.3, 0), f"S{k}")
        for k in range(2):
            place(A, build(r), (14 + 4*k, 3.5 - .2*k, -5.0 + .0), f"R{k}")
            A[f"FILL{k}"] = (SSL, box(12 + 4*k + .001, 16 + 4*k - .001, -.3, 3.5 - .2*k + .002, -8.0, -2.0))
        Pt = Part()
        for n, (mk, m) in A.items():
            if "uv" not in m.metadata: m.metadata["uv"] = np.zeros((len(m.vertices), 2))
            Pt.add(n, mk, m)
        _, g2 = export_final(Pt.P, [f"/tmp/trv_{i}.glb"]); im = crop(render_view(g2, Ry(16, 32), size=900, shadow=False, glass_alpha=.35))
        plt.imsave(os.path.join(rdir, f"v{i+1}_vignette.png"), np.clip(im, 0, 1)); axs[4, i].imshow(np.clip(im, 0, 1)); axs[4, i].axis("off")
        s = SE[i]; axs[4, i].set_title(f"vignette: façade + deck + edge over skirt + ramp\ntiling: deck X/Z {'PASS' if s['deck_x'] and s['deck_z'] else 'FAIL'}, edge {'PASS' if s['edge_x'] else 'FAIL'}, ramp chain/mirror {'PASS' if s['ramp_chain'] and s['ramp_mirror'] else 'FAIL'}, apron {'PASS' if s['apron_x'] else 'FAIL'}", fontsize=9)
    for row, t in enumerate(("deck tile 4x4 (place at +3.70)", "edge + 1.07 m guard (on the skirt cap)", "ramp 1:20 (4 m run, half width 6 m)", "apron 1:12 (4 x 1 m)", "assembled vignette")): axs[row, 0].text(-.03, .5, t, transform=axs[row, 0].transAxes, rotation=90, va="center", ha="right", fontsize=12)
    fig.suptitle("Rook | Tennis Tower terrace decks + ramps V1-V5 (W Arrival / E Plaza +4.0, E Spine 1:20, S/N 1:12 aprons) | candidates (not promoted)", fontsize=16)
    plt.tight_layout(rect=(0, 0, 1, .97)); sp = os.path.join(rdir, "terrace_contact_sheet.png"); fig.savefig(sp, dpi=70, facecolor="#F4F2EC"); plt.close(fig); print("SHEET", sp)
