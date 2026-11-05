"""Rook: #76 plinth skirt final (Jared pick V5 Boulder Skirt, densified). 4.0 m tile + 2.0 m half tile, grade 0 -> F1 +4.0 (§3.3).
Four 1.0 m trimmable courses (Course0..3, each a separate part: 2-3 layered overlapping faceted slate slabs at different tilts), slate cap
course 3.88..4.0 that carries tt_facade_bay's slate plinth ledge (same slate, amber line at the same z +0.42), ray-seated holds (tennis-ball
holds dominant + jugs, crimps, slopers), grip-relief grit dots, moss-edged slate base mat with river stones and grass tufts.
+Z exterior, face line z 0, pivot bottom centre. Colliders: Skirt-colonly + Mat-colonly. Run: python3 plinth_skirt_final.py"""
from modlib import *
from ridge_crown import huv
HT = 4.0
def slab(xa, xb, ya, yb, zb, zt, bulge=0.0, zback=.02 - E):   # faceted slab: back on the core (z .02), front tilted from zb (bottom) to zt (top), optional ridge
    xm = (xa + xb)/2; P = [(x, y, z) for x in (xa, xb) for (y, z) in ((ya, zback), (yb, zback), (ya, zb), (yb, zt))]
    if bulge: P += [(xm, (ya + yb)/2, (zb + zt)/2 + bulge)]
    return huv(P)
def orient(m, hit, n, lift):
    R = np.eye(4); R[:3, :3] = trimesh.geometry.align_vectors([0, 0, 1], n)[:3, :3]; m.apply_transform(R); m.apply_translation(np.asarray(hit) + n*lift); return m
def build(q):
    w = q.get("width", 4.0); h = w/2; X0, X1 = -h + .001, h - .001; p = Part(); rng = np.random.default_rng(q.get("seed", 7))
    p.add("Skirt_Core", SL, box(X0 + .006, X1 - .006, .049, HT - .12 + .004, -.2, .02))
    # base mat (slate) with moss edge, stones, tufts
    p.add("Base_Mat", SSL, box(X0 + .004, X1 - .004, 0, .05, -.2, 2.0))
    courses = []; SLABS = []
    tilts = [(1.05, .8), (.8, .95), (.95, .7), (.7, .4)]
    for k in range(4):
        ya, yb = (k if k else .046) - (.004 if k else 0), (k + 1) if k < 3 else HT - .12 + .004
        zb, zt = tilts[k]; zbk = .02 - (.002 if k % 2 == 0 else .007); ix = .003 if k % 2 else 0; S = [slab(X0 + ix, X1 - ix, ya, yb, zb, zt, zback=zbk)]
        cuts = sorted(rng.uniform(-h + .3, h - .3, 2)) if w > 3 else [rng.uniform(-h + .3, h - .3)]
        for j, c in enumerate(cuts):   # layered proud slabs, overlapping the base slab (same part), varied tilt and a sculpted ridge
            a, b = max(X0, c - rng.uniform(.4, .8)), min(X1, c + rng.uniform(.4, .8)); dz = rng.uniform(.06, .14)
            S.append(slab(a, b, ya + .03, yb - .03, zb + dz*(1 if j % 2 else .6), zt + dz*(.5 if j % 2 else 1.2), bulge=rng.uniform(.03, .08), zback=zbk))
        m = trimesh.util.concatenate(S); m.metadata["uv"] = np.vstack([s.metadata["uv"] for s in S]); courses.append(m); SLABS.extend(S)
        p.add(f"Course{k}_Facets", SL, *S)
    allc = trimesh.util.concatenate(courses)
    def seat(x, y):
        loc, ri, ti = allc.ray.intersects_location([(x, y, 5.0)], [(0, 0, -1)])
        if not len(loc): return None
        i = np.argmax(loc[:, 2]); n = allc.face_normals[ti[i]]; return loc[i], n / np.linalg.norm(n)
    # cap course tying into the façade plinth ledge
    p.add("Cap_Course", SL, box(X0, X1, HT - .12, HT, -.2, .78), box(X0, X1, HT - .2, HT - .12 + E, .62, .78))
    p.add("Cap_Court_Line", AM, box(X0, X1, HT - .09, HT - .05, .78 - E, .787))
    p.add("Cap_Drip_Edge", G, box(X0, X1, HT - .23, HT - .2 + E, .64, .76))
    def ok(m, lim=.0095):
        return max(trimesh.proximity.signed_distance(sb, m.vertices).max() for sb in SLABS if np.all(sb.bounds[0] - .2 < m.bounds[1]) and np.all(m.bounds[0] < sb.bounds[1] + .2)) <= lim
    # holds
    balls, jugs, crimps, slopers, grit, tape = [], [], [], [], [], []
    nx = int(w/.38)
    for k in range(4):
        for j in range(nx):
            x = -h + .2 + j*(w - .4)/(nx - 1) + rng.uniform(-.08, .08); y = k + .2 + rng.uniform(0, .6) if k < 3 else 3.1 + rng.uniform(0, .6)
            s = seat(x, y)
            if s is None or s[1][2] < .3: continue
            hit, n = s; t = rng.random()
            if t < .5: r = rng.uniform(.05, .075); balls.append(node(hit + n*(r - .006), r, 1))
            elif t < .68: jugs.append(orient(huv([(-.09, -.04, 0), (.09, -.04, 0), (-.07, .05, 0), (.07, .05, 0), (-.05, -.02, .07), (.05, -.02, .07), (0, .03, .05)]), hit, n, -.0045))
            elif t < .84: crimps.append(orient(box(-.07, .07, -.015, .015, 0, .03), hit, n, -.006))
            else: m = trimesh.creation.icosphere(1, .09); m.apply_scale([1.2, .8, .45]); m.metadata["uv"] = m.vertices[:, :2]; slopers.append(orient(m, hit, n, .04 - .008))
        for j in range(int(w*4)):   # grip-relief grit dots
            x, y = rng.uniform(-h + .08, h - .08), rng.uniform(k + .1, (k + .9) if k < 3 else 3.75); s = seat(x, y)
            if s is None or s[1][2] < .3: continue
            grit.append(node(s[0] + s[1]*(.014 - .005), .014, -1))
    cap = trimesh.util.concatenate([box(X0, X1, HT - .23, HT, -.2, .78)])
    clear = lambda m: m.bounds[1][1] < HT - .235
    balls, jugs, crimps, slopers = [[m for m in L if clear(m) and ok(m)] for L in (balls, jugs, crimps, slopers)]
    HC = np.array([m.centroid for L in (balls, jugs, crimps, slopers) for m in L])
    grit = [m for m in grit if clear(m) and ok(m) and np.min(np.linalg.norm(HC - m.centroid, axis=1)) > .16]
    for nm, mt, L in (("Tennis_Ball_Holds", BA, balls), ("Jug_Holds", AM, jugs), ("Crimp_Holds", G, crimps), ("Sloper_Holds", LF2, slopers), ("Grip_Relief", ST, grit)):
        if L: p.add(nm, mt, *L)
    # route tape seams along each course joint, seated on the outermost face
    for y in (1.0, 2.0, 3.0):
        P = []
        for x in np.linspace(X0 + .01, X1 - .01, 9):
            s = seat(x, y + .05)
            if s: P.append(s[0] + s[1]*.004)
        # short tape dashes between sample points (keeps every dash on the face)
        for a, b in zip(P[:-1], P[1:]):
            if abs(a[2] - b[2]) < .03: tape.append(tube(a, b, .008, 4))
    p.add("Seam_Tape", AM, *tape)
    # base: moss edge, river stones, tufts on the mat
    zf = max(courses[0].bounds[1][2], 1.2)
    M = [clump((x, .05 + .075, 1.86), .12, 90 + i) for i, x in enumerate(np.arange(-h + .2, h - .1, .34))]
    St = []; Tf = []
    for i in range(int(w*5)):
        x, z = rng.uniform(-h + .1, h - .1), rng.uniform(zf + .08, 1.66); r = rng.uniform(.03, .06)
        st = trimesh.creation.icosphere(1, r); st.apply_scale([1.3, .55, 1.0]); st.apply_translation((x, .05 + r*.55 - .004, z)); st.metadata["uv"] = st.vertices[:, [0, 2]]; St.append(st)
    SC = [(m.centroid[0], m.centroid[2]) for m in St]
    for i in range(int(w*6)):
        x, z = rng.uniform(-h + .15, h - .15), rng.uniform(zf + .1, 1.64)
        if any(np.hypot(x - a, z - b) < .13 for a, b in SC): continue
        Tf += [leaf((x + .02*np.cos(a), .05 - .004, z + .02*np.sin(a)), .16 + .05*rng.random(), .03, yaw=a, pitch=-.25, t=.006) for a in (0, 2.1, 4.2)]
    p.add("Moss_Edge", LF, *M); p.add("River_Stones", SSL if False else ST, *St); (p.add("Grass_Tufts", LF2, *Tf) if Tf else None)
    p.add("Skirt-colonly", SL, box(X0, X1, 0, HT, -.2, 1.15)); p.add("Mat-colonly", SSL, box(X0, X1, 0, .05, -.2, 2.0))
    return p
VARIANTS = [dict(label="Boulder Skirt final: 4.0 m tile", width=4.0, seed=7), dict(label="Boulder Skirt final: 2.0 m half tile", width=2.0, seed=12)]
def layout(builder, widths, dy=0.0, tag="S"):
    A = {}; x = 0
    for k, w in enumerate(widths):
        x += w/2
        for n, (mk, m) in builder(dict(width=w, seed=7 if w > 3 else 12)).P.items():
            if "colonly" in n: continue
            m2 = m.copy(); m2.apply_translation((x, dy, 0)); m2.metadata["uv"] = m.metadata.get("uv", np.zeros((len(m.vertices), 2))); A[f"{tag}{k}_{n}"] = (mk, m2)
        x += w/2
    return A
def seam_check(widths):
    A = layout(build, widths); edge = widths[0]
    near = {k: v for k, v in A.items() if v[1].bounds[1][0] > edge - .6 and v[1].bounds[0][0] < edge + .6}
    chk = cc.check(near, n_samp=300); bad = [o for o in chk["overlap"] if not o[3] and o[0][:3] != o[1][:3]]; cop = [c for c in chk["coplanar"] if c[0][:3] != c[1][:3]]
    return dict(bad=bad[:3], coplanar=cop[:3], pass_=not bad and not cop)
if __name__ == "__main__":
    import facade_bay_final as FB
    rep = run("plinth_skirt_final", build, VARIANTS, title="plinth skirt final", sheet="plinth_skirt_final_run_sheet.png")
    seams = {str(w): seam_check(w) for w in ([4, 4], [4, 2], [2, 4])}; print("SEAMS", seams)
    rdir = os.path.join(RENDER_OUT, "plinth_skirt_final"); os.makedirs(rdir, exist_ok=True)
    Ry = lambda el, az: (lambda a, b: np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]) @ np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]))(np.radians(az), np.radians(el))
    fig = plt.figure(figsize=(26, 18), facecolor="#F4F2EC"); gs = fig.add_gridspec(2, 4)
    shots = [(0, (8, 35), "4.0 m tile, low 3/4"), (0, (12, -78), "4.0 m tile, raking side (layered facets)"), (0, (35, 20), "4.0 m tile, high (holds, mat, tufts)"), (1, (8, 35), "2.0 m half tile")]
    for j, (vi, (el, az), t) in enumerate(shots):
        p = recenter(build(VARIANTS[vi])); _, geo = export_final(p.P, [f"/tmp/psf_{j}.glb"]); geo = {k: v for k, v in geo.items() if "colonly" not in k}
        im = crop(render_view(geo, Ry(el, az), size=800, shadow=False, glass_alpha=.35))
        ax = fig.add_subplot(gs[0, j]); ax.imshow(np.clip(im, 0, 1)); ax.axis("off"); ax.set_title(f"{t}\n{rep[vi]['tris']} tris | {'PASS' if rep[vi]['passed'] else 'FAIL'}", fontsize=11)
    Pt = Part(); run_w = [4, 4, 2, 4, 4]
    A = layout(build, run_w); A.update(layout(FB.build, run_w, HT, "F"))
    for n, (mk, m) in A.items(): Pt.add(n, mk, m)
    _, g2 = export_final(Pt.P, ["/tmp/psf_run.glb"]); im = crop(render_view(g2, Ry(8, 30), size=1500, shadow=False, glass_alpha=.35))
    ax = fig.add_subplot(gs[1, :]); ax.imshow(np.clip(im, 0, 1)); ax.axis("off"); ax.set_title(f"run 4+4+2+4+4 m: tt_plinth_skirt(_half) under tt_facade_bay(_half) at +4.0 | skirt seams 4|4, 4|2, 2|4: {'PASS' if all(s['pass_'] for s in seams.values()) else 'FAIL'}", fontsize=12)
    fig.suptitle("Rook | #76 tt_plinth_skirt (V5 Boulder Skirt, densified) + tt_plinth_skirt_half | FINAL", fontsize=15)
    plt.tight_layout(rect=(0, 0, 1, .95)); sp = os.path.join(rdir, "plinth_skirt_final_sheet.png"); fig.savefig(sp, dpi=85, facecolor="#F4F2EC"); print("SHEET", sp)
