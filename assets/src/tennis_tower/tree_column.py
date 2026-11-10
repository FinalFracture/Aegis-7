"""Rook: Tennis Tower tree column (spec §3.11.3 Rev 2.5/2.6, §4.6). Grade-to-roof type (TC-S/N/E): 2.0x2.0x0.6 concrete pedestal on F1 (0),
cast-steel pinned shoe, trunk clad 1.2 m square through F1/F2 bands up to F3 (+12.2), CHS 914 trunk to crown node at +19.0,
4 CHS 406 branches to bottom-chord nodes at +22.5 on an 8x8 m square (Ø450 heads), cyan LED ring at the crown.
base='truss' gives the TC-W1/W2 type (shoe at F3 only). Run: python3 tree_column.py"""
from modlib import *
F3, CR, BC, HS = 12.2, 19.0, 22.5, 4.0
CN = [(sx*HS, BC, sz*HS) for sx in (-1, 1) for sz in (-1, 1)]
KR, KY, LY, LT = .30, 21.0, 20.80, .20   # r1 stepped crown: knuckle offset / height, leaf ring height / up-tilt

def base(p, q):
    if q.get("base", "grade") == "grade":
        p.add("Pedestal_Concrete", SL, box(-1, 1, 0, .6, -1, 1)); p.add("Pin_Shoe", G, box(-.55, .55, .6 - E, .9, -.55, .55))
        if q.get("ribs"):  # bark-ribbed cladding: core + vertical ribs (one part)
            p.add("Trunk_Clad", G, box(-.5, .5, .9 - E, F3, -.5, .5), *[box(x-.05, x+.05, .9 - E, F3, -.6, -.5 + E) for x in (-.3, 0, .3)],
                  *[box(x-.05, x+.05, .9 - E, F3, .5 - E, .6) for x in (-.3, 0, .3)], *[box(-.6, -.5 + E, .9 - E, F3, z-.05, z+.05) for z in (-.3, 0, .3)],
                  *[box(.5 - E, .6, .9 - E, F3, z-.05, z+.05) for z in (-.3, 0, .3)])
        else: p.add("Trunk_Clad", G, box(-.6, .6, .9 - E, F3, -.6, .6))
        return F3 - E
    p.add("Pin_Shoe", G, box(-.55, .55, F3, F3 + .3, -.55, .55)); return F3 + .3 - E

def build(q):
    p = Part(); y0 = base(p, q); st = []
    st.append(tube((0, y0, 0), (0, CR, 0), .457, 16)); st.append(node((0, CR, 0), .6, 1))
    st += [node(c, .225, 1) for c in CN]
    f = q["crown"]
    if f == "straight" and q.get("stepped"):  # r1 stepped crown: each branch rises inside a 0.69 m radius to a cast knuckle at KY, then runs to its node,
        for c in CN:                          # so nothing below +20.7 reaches past the F3 stand backs (0.74 m off the trunk axis, canopies to +20.61)
            k = (np.sign(c[0])*KR, KY, np.sign(c[2])*KR); st += [tube((0, CR, 0), k, .203, 10), node(k, .25, 1), tube(k, c, .203, 10)]
    elif f == "straight": st += [tube((0, CR, 0), c, .203, 10) for c in CN]
    elif f == "organic":  # curved jointed branches + root-flare sleeve
        for c in CN:
            c = np.array(c); m1 = np.array([c[0]*.35, CR + 1.9, c[2]*.35]); m2 = np.array([c[0]*.75, CR + 3.0, c[2]*.75])
            st += [tube((0, CR, 0), m1, .23, 10), node(m1, .23, 1), tube(m1, m2, .2, 10), node(m2, .2, 1), tube(m2, c, .18, 10)]
        st.append(tube((0, y0 + 2.5, 0), (0, y0 + .02, 0), .52, 16))
    elif f == "fractal":  # V3 Branch Fin language: 2 arms fork at +16.5, each forks again at +20
        for sx in (-1, 1):
            a = np.array([sx*2.0, 20.0, 0]); st += [tube((0, 16.5, 0), a, .26, 10), node(a, .3, 1)]
            st += [tube(a, c, .19, 10) for c in CN if np.sign(c[0]) == sx]
        st.append(node((0, 16.5, 0), .55, 1))
    p.add("Tree_Steel", ST, *st)
    p.add("Crown_LED_Ring", CY, ring_band(.457, 15.5 if f == "fractal" else CR - 1.2, h=.12, n=16))
    if q.get("leaves") and q.get("stepped"):  # r1: leaf capital lifted to the knuckle ring and tilted up (crown only above the stands)
        p.add("Leaf_Capital", LF, *[leaf_dir((np.cos(a)*.72, LY, np.sin(a)*.72), (np.cos(a), LT, np.sin(a)), 3.0, .6, t=.05) for a in np.arange(8)*np.pi/4 + np.pi/8])
    elif q.get("leaves"):  # leaf-canopy capital: 8 big leaves radiating from the crown between branches
        p.add("Leaf_Capital", LF, *[leaf_dir((np.cos(a)*.64, CR - .3, np.sin(a)*.64), (np.cos(a), -.3, np.sin(a)), 3.2, .7, t=.05) for a in np.arange(8)*np.pi/4 + np.pi/8])
    if q.get("planter"):  # 4 troughs around the pedestal with shrubs + vines up the clad
        for k in range(4):
            R = trimesh.transformations.rotation_matrix(k*np.pi/2, [0, 1, 0])
            tr, so, sy = planter(-1.6, 1.6, 0, 1.03, 1.9, h=.55)
            p.add("Planter_Trough", G, xf(tr, R=R)); p.add("Planter_Soil", SO, xf(so, R=R)); p.add("Foliage", LF2, xf(shrubs(-1.4, 1.4, sy, 1.45, r=.28, seed=k*7), R=R))
            s, l = vine([(-.25, .9, .63), (.1, 4, .63), (-.15, 8, .63), (.2, 11.8, .63)], r=.02, leaf_every=.5, leaf_len=.3, seed=k, outward=True)
            p.add("Vine_Stems", LF, xf(s, R=R)); p.add("Vine_Leaves", LF2, xf(l, R=R))
    if q.get("bench"):  # octagonal bench ring + amber scoreboard band
        segs = []
        for k in range(8):
            R = trimesh.transformations.rotation_matrix(k*np.pi/4, [0, 1, 0])
            segs += [xf(box(-.62, .62, .4, .46, 1.7, 2.2), R=R), xf(box(-.5, .5, 0, .4 + E, 1.85, 2.05), R=R), xf(box(-.62, .62, .46 - E, .9, 2.2 - E, 2.26), R=R)]
        p.add("Bench_Ring", ST, *segs)
        p.add("Score_Band", AM, *[xf(box(-.5, .5, 6.0, 6.6, .6 - E, .62), R=trimesh.transformations.rotation_matrix(k*np.pi/2, [0, 1, 0])) for k in range(4)])
    return p

VARIANTS = [
    dict(label="Organic Fork: curved jointed branches, root-flare sleeve", crown="organic"),
    dict(label="Geometric Fractal: Y-fork twice (Branch Fin echo), cyan crown", crown="fractal"),
    dict(label="Bark Rib + Planter: ribbed clad, planter ring, climbing vines", crown="straight", ribs=True, planter=True),
    dict(label="Leaf Capital: 8 steel-green leaves at the crown", crown="straight", leaves=True),
    dict(label="Bench Ring: octagon bench at foot, amber score band", crown="fractal", bench=True),
]
def colliders(p, q):  # r1: trunk colliders (pedestal + clad / shoe + trunk to the crown node); branches are above reach
    cs = [box(-.46, .46, (F3 if q.get("base") == "truss" else .9), CR, -.46, .46)]
    cs += [box(-1, 1, 0, .6, -1, 1), box(-.6, .6, .6, F3, -.6, .6)] if q.get("base", "grade") == "grade" else [box(-.55, .55, F3, F3 + .3, -.55, .55)]
    for m in cs: m.metadata["uv"] = np.zeros((len(m.vertices), 2))
    p.P["Trunk-colonly"] = (G, trimesh.util.concatenate(cs)); p.P["Trunk-colonly"][1].metadata["uv"] = np.zeros((len(p.P["Trunk-colonly"][1].vertices), 2))
    return p

def promote():  # r1 fixes: stepped V4 Leaf Capital -> tt_tree_column.glb (grade) + tt_tree_column_west.glb (truss)
    rep = []
    for fn, base_ in (("tt_tree_column.glb", "grade"), ("tt_tree_column_west.glb", "truss")):
        q = dict(VARIANTS[3], stepped=True, base=base_); p = recenter(colliders(build(q), q)); gp = os.path.join(ROOT, "godot/assets/models", fn)
        tris, _ = export_final(p.P, [gp]); finish_glb(gp)
        chk = cc.check({k: v for k, v in p.P.items() if "colonly" not in k}, n_samp=400)
        try: ok_v = vm.validate_file(gp, check_tri_range=(1, TRI_MAX), require_textures=False, require_blend_glass=False)
        except AssertionError as e: print("VALIDATE FAIL", e); ok_v = False
        V = np.vstack([m.vertices for k, (_, m) in p.P.items() if "colonly" not in k])
        r = dict(glb=fn, tris=int(tris), clip_pass=bool(chk["pass"]), worst_overlap=chk["worst_overlap"], coplanar=chk["coplanar"], open=chk["open"], validate=bool(ok_v),
                 bbox=[V.min(0).round(4).tolist(), V.max(0).round(4).tolist()]); rep.append(r); print(json.dumps(r, default=str))
    return rep

if __name__ == "__main__" and sys.argv[1:] == ["promote"]: promote()
elif __name__ == "__main__": run("tree_column", build, VARIANTS, title="§3.11.3 grade-to-roof tree, 8x8 m head, 22.5 m to bottom chord | nature + sports")
