"""Rook: Tennis Tower aquatic slide tower T1/T2 (spec §3.6: 5 x 5 m, stair to a start deck at +7.0, roof +9.4 under the +9.7 soffit,
F2 slide bridge from the gallery at +6.1). Datum y 0 = tower base (island deck). One GLB per tower, +Z = ground entry face.
Stair half (-X): switchback 9/9/8/8 risers x 0.1794 to the bridge landing N2 at +6.1 (bridge opening in the -X face),
then 5 risers x 0.18 eastward onto the start deck (+X half) at +7.0. Slide tube stub leaves through the +X face (invert at +7.0).
REUSE: stair_core_colliders_rev_c.slab_between ramps + Rev C stair materials/finish/nosing scheme (tt_stair_core V5), court-partition
scissor guard language, curtain-wall fin() (Branch Fin), restroom Leaf Crest crest(), stand planter()/shrubs(), green_wall(), tree-column CHS columns.
Run: python3 slide_tower.py"""
from modlib import *
from stair_core_colliders_rev_c import slab_between
from restroom_extras import crest
from structure.struct_lib import SCR, finish_scissor
FIN, NOSE, T, TH = .015, .03, .28, .25
NS = [9, 9, 8, 8]; R = 6.1 / sum(NS); R5, N5 = .18, 5
XA, XB = (-2.3, -1.25), (-1.15, -.1); ZN, ZS, ZI = 1.2, -2.3, 2.3; C = 2.4; YR = 9.15; DECK = 7.0
PG = .011  # half pane thickness
def U(m): m.metadata["uv"] = np.zeros((len(m.vertices), 2)); return m

def flight(p, xr, z0, y0, n, d, nos):  # d=-1 rises toward -Z, +1 toward +Z; first riser at z0
    xa, xb = (xr[0], xr[1] + E) if xr is XA else (xr[0] - E, xr[1])
    for k in range(1, n):
        za, zb = sorted((z0 + d*(k-1)*T, z0 + d*k*T)); yt = y0 + k*R
        if k == n - 1: za, zb = (za - E, zb) if d < 0 else (za, zb + E)
        if k == 1: za, zb = (za, zb + E) if d < 0 else (za - E, zb)
        p.add("Stair_Cast", WH, box(xa, xb, .002 if y0 == 0 else yt - TH, yt - FIN + E, za, zb))
        fa, fb = (za + .002, zb + .005) if d < 0 else (za - .005, zb - .002)
        p.add("Treads_Slate", SSL, box(xa + .002, xb - .002, yt - FIN, yt, fa, fb))
        if nos: p.add("Nosing_Emergency", AM, box(xr[0] + .03, xr[1] - .03, yt - .003, yt + .002, *((fb - NOSE, fb - .002) if d < 0 else (fa + .002, fa + NOSE))))
    zl = z0 + d*(n-1)*T; y1 = y0 + n*R
    p.add(f"F{len([k for k in p.P if k.startswith('F') and k.endswith('_Ramp-colonly')]) + 1}_Ramp-colonly", G, slab_between(*xr, z0 - d*T, y0, zl, y1))
    return zl, y1

def landing(p, tag, z0, z1, y):
    p.add("Stair_Cast", WH, box(XA[0], XB[1], y - TH, y - FIN + E, z0, z1)); p.add("Treads_Slate", SSL, box(XA[0] + .002, XB[1] - .002, y - FIN, y, z0 + .002, z1 - .002))
    p.add(f"{tag}_Landing-colonly", G, trimesh.creation.box(bounds=[[XA[0], y - TH, z0], [XB[1], y, z1]]))

def build(q):
    p = Part(); nos = q.get("nosing", False)
    # --- switchback to the bridge landing ---
    z, y = flight(p, XA, ZN, 0.0, NS[0], -1, nos); landing(p, "S1", ZS, z - E*0, y); zs1 = z
    z, y = flight(p, XB, zs1, y, NS[1], +1, nos); landing(p, "N1", ZN, ZI, y); yn1 = y
    z, y = flight(p, XA, ZN, y, NS[2], -1, nos); landing(p, "S2", ZS, z, y); zs2, ys2 = z, y
    z, y = flight(p, XB, zs2, y, NS[3], +1, nos); landing(p, "N2", ZN, ZI, y); yn2 = y
    # --- flight 5 eastward onto the deck ---
    x0 = XB[1]
    for k in range(1, N5):
        xa, xb, yt = x0 + (k-1)*T - (E if k == 1 else 0), x0 + k*T + (E if k == N5 - 1 else 0), yn2 + k*R5
        p.add("Stair_Cast", WH, box(xa, xb, yt - TH, yt - FIN + E, ZN, ZI)); p.add("Treads_Slate", SSL, box(xa - .005, xb - .002, yt - FIN, yt, ZN + .002, ZI - .002))
        if nos: p.add("Nosing_Emergency", AM, box(xa - .003, xa + NOSE - .005, yt - .003, yt + .002, ZN + .03, ZI - .03))
    x5 = x0 + (N5 - 1)*T
    hull = lambda pts: trimesh.convex.convex_hull(np.array(pts))
    p.add("F5_Ramp-colonly", G, hull([(x, yy - dy, z) for (x, yy) in ((x0 - T, yn2), (x5, DECK)) for dy in (0, .2) for z in (ZN, ZI)]))
    # --- start deck (+X half) ---
    p.add("Deck", WH, box(-.035, ZI, DECK - TH, DECK - FIN + E, ZS, ZN - .002), box(x5 - E, ZI, DECK - TH, DECK - FIN + E, ZN - .01, ZI))
    p.add("Deck_Finish", SSL, box(-.033, ZI - .002, DECK - FIN, DECK, ZS + .002, ZN - .004), box(x5 + .002, ZI - .002, DECK - FIN, DECK, ZN - .004 + E, ZI - .002))
    p.add("Deck-colonly", G, U(trimesh.creation.box(bounds=[[-.035, DECK - TH, ZS], [ZI, DECK, ZN]])), U(trimesh.creation.box(bounds=[[x5, DECK - TH, ZN], [ZI, DECK, ZI]])))
    # --- spine wall between the flights ---
    p.add("Spine_Wall", q.get("spine_mat", WH), box(XA[1], XB[0], 0, ys2 - TH - .002, zs1 - 2*E, zs2 + E), box(XA[1], XB[0], 0, yn2 + 1.0, zs2 + .006, ZN - .002))
    # --- columns + roof (tree-column CHS language) ---
    p.add("Columns", G, *[tube((sx*C, 0, sz*C), (sx*C, YR + E, sz*C), .1, 16) for sx in (-1, 1) for sz in (-1, 1)])
    p.add("Roof", q.get("roof_mat", WH), box(-2.6, 2.6, YR, 9.4, -2.6, 2.6))
    # --- scissor enclosure (court-partition guard language), split around openings ---
    e = 2.305; gt = YR - .002; panes = []
    panes += [box(-C - PG, -C + PG, 0, gt, -e, ZN), box(-C - PG, -C + PG, 0, yn2 - TH - .02, ZN, e), box(-C - PG, -C + PG, yn2 + 2.3, gt, ZN, e)]       # -X, bridge opening N2
    panes += [box(XA[1], e, 0, gt, C - PG, C + PG), box(-e, XA[1], 2.4, gt, C - PG, C + PG)]                                              # +Z, ground entry
    if q.get("south") != "green": panes += [box(-e, e, 0, gt, -C - PG, -C + PG)]
    else: panes += [box(-.05, e, 0, gt, -C - PG, -C + PG)]
    panes += [box(C - PG, C + PG, 0, gt, -e, -1.7), box(C - PG, C + PG, 0, gt, -.7, e), box(C - PG, C + PG, 0, DECK - .07, -1.7, -.7), box(C - PG, C + PG, 7.9, gt, -1.7, -.7)]  # +X, slide opening
    panes += [box(-.05 - PG, -.05 + PG, 0, 8.1, ZS, ZN - .003), box(-.05 - PG, -.05 + PG, 0, yn2 - TH - .05, ZN + .003, ZI - .003)]                        # inner screen (stair | shaft)
    panes += [box(-.035, x5, DECK + .002, 8.1, ZN - .03, ZN - .008), box(XA[0], XA[1] - .002, yn2 + .002, yn2 + 1.1, ZN + .008, ZN + .03)]  # deck + N2 edge guards
    p.add("Enclosure_Scissor", SCR, *panes)
    if q.get("south") == "green":   # Garden face: solid composite wall on the stair side of -Z with a planted wall outside
        p.add("Garden_Wall", WH, box(-e, -.05 - .002, 0, gt, -C - .05, -C + .05))
        p.add("Green_Wall", LF, *[leaf_dir((x + (.12 if j % 2 else 0), y, -C - .05 - .03), (0, -1, -.3), .26, .14) for j, y in enumerate(np.arange(.35, 2.6, .2)) for x in np.arange(-2.2, -.35, .26)])
    # --- slide start: gate posts + tube stub (invert at +7.0) ---
    p.add("Gate_Posts", SGM, *[box(2.07, 2.13, DECK - E, YR + E, zc - .03, zc + .03) for zc in (-1.75, -.65)])
    p.add("Start_Light", q.get("light", GRN), box(2.13 - E, 2.15, 8.2, 8.35, -.67, -.63))
    tb = ring_band(.4, .125, h=.25, n=16, t=.05); tb.apply_transform(trimesh.transformations.rotation_matrix(-np.pi/2, [0, 0, 1])); tb.apply_translation((2.302, DECK + .4, -1.2))
    tb.metadata["uv"] = np.zeros((len(tb.vertices), 2)); p.add("Slide_Tube", q.get("tube", CY), tb)
    dress(p, q, yn1, ys2, yn2, x5)
    for k, (mk, m) in list(p.P.items()):
        if "colonly" not in k: continue
        if m.bounds[0][1] < 0: m = m.slice_plane([0, 0, 0], [0, 1, 0], cap=True)  # F1 ramp slab dips below the floor
        m.update_faces(m.nondegenerate_faces()); m.remove_unreferenced_vertices()  # slice cap slivers -> zero-length shade_split normals
        m.metadata["uv"] = np.zeros((len(m.vertices), 2)); p.P[k] = (mk, m)
    p.walk = [(-1.775, 2.9), (-1.775, -1.7), (-.625, -1.7), (-.625, 1.75), (-1.775, 1.75), (-1.775, -1.5), (-.625, -1.5), (-.625, 1.75), (1.6, 1.75), (1.6, -1.2), (1.95, -1.2)]
    return p

def dress(p, q, yn1, ys2, yn2, x5):
    d = q["dress"]
    if d in ("crown", "garden"):   # green roof (stand planter + shrubs) kept under the +9.7 soffit
        tr, so, sy = planter(-2.4, 2.4, 9.4 - E, -2.4, 2.4, h=.08); p.add("Roof_Planter", G, tr); p.add("Planter_Soil", SO, so)
        p.add("Roof_Foliage", LF2, *[shrubs(-2.3, 2.3, sy, z, r=.1, n=14, seed=int(z*10 + 30)) for z in (-1.6, 0, 1.6)])
    if d == "crown":   # Tree Crown: leaf caps on every column (tree-column V4 echo) under the roof
        p.add("Leaf_Caps", LF, *[leaf_dir((sx*(C + .08), YR - .15, sz*(C + .08)), (sx*.3, -1, sz*.3), .28, .16) for sx in (-1, 1) for sz in (-1, 1)])
    if d == "fin":     # Branch Fin: fish-belly fins on the +Z and -Z faces (curtain-wall V3)
        fs = []
        for sz in (-1, 1):
            for x in np.arange(-2.1, 2.2, .6):
                if sz > 0 and x < -1.2: continue     # keep the ground entry clear
                f = xf(fin(0, .3, YR - .3, .1, .04, 0, belly=.8), R=trimesh.transformations.rotation_matrix(np.pi if sz > 0 else 0, [0, 1, 0])); f.apply_translation((x, 0, sz*(C + PG + .002)))
                f.metadata["uv"] = np.zeros((len(f.vertices), 2)); fs.append(f)
        p.add("Branch_Fins", ST, *fs)
    if d == "leaf":    # Leaf Crest: leaf crests on the deck guard cap rail + spine, leaf-green fascia (restroom #58 echo)
        p.add("Guard_Cap_Rail", ALY, tube((-.03, 8.1 + .02 - E, 1.181), (x5, 8.1 + .02 - E, 1.181), .02, 6))
        p.add("Leaf_Crests", LF, *[crest((x, 8.1 + .036, 1.181)) for x in np.linspace(.15, x5 - .15, 3)])
        p.add("Fascia_Band", LF, box(-2.6, 2.6, 9.4 - E, 9.46, 2.6 - .03, 2.6 + .01), box(-2.6, 2.6, 9.4 - E, 9.46, -2.6 - .01, -2.6 + .03))
    if d == "garden":  # Garden Terrace: deck planters at the -Z corner
        tr, so, sy = planter(1.3, 2.25, DECK - E, -2.25, -1.85, h=.45); p.add("Deck_Planter", G, tr); p.add("Deck_Soil", SO, so); p.add("Deck_Foliage", LF2, shrubs(1.35, 2.2, sy, -2.05, r=.15, seed=8))
    if d == "court":   # Court Wayfinding (stair core V5): level discs on the spine, court line on the deck, ball finials on the gate posts
        p.add("Level_Disc", AM, *[cap((XA[1] - .005 + .002, y + 1.6, .2), .3, .01, 16, axis="x") for y in (0, yn1)])
        p.add("Court_Line_Deck", AM, box(.3, 2.0, DECK - .002, DECK + .003, -.15, -.09))
        p.add("Ball_Finials", BA, *[node((2.1, 8.6, zc + .03 + .035 - E), .035, 0) for zc in (-1.75, -.65)])

VARIANTS = [
    dict(label="Tree Crown: green roof, leaf caps on the columns, leaf-green tube", dress="crown", tube=LF2),
    dict(label="Branch Fin: fish-belly steel fins on the +Z and -Z faces", dress="fin", tube=CY),
    dict(label="Leaf Crest: leaf-crest guard rail, leaf fascia, leaf tube", dress="leaf", tube=LF, spine_mat=LF),
    dict(label="Garden Terrace: planted south wall, green roof, deck planter", dress="garden", south="green", tube=GRN),
    dict(label="Court Wayfinding: amber nosings, level discs, ball finials", dress="court", nosing=True, tube=AM, light=GRN),
]
if __name__ == "__main__":
    rep = run("slide_tower", build, VARIANTS, title="5 x 5 m, bridge landing +6.1, start deck +7.0, roof +9.4 | nature + sports", post=finish_scissor)
    p = recenter(build(VARIANTS[2])); gp = os.path.join(ROOT, "godot/assets/models", "tt_slide_tower.glb")
    tris, _ = export_final(p.P, [gp]); finish_glb(gp); finish_scissor(gp)
    V = np.vstack([m.vertices for _, m in p.P.values()]); lo, hi = V.min(0), V.max(0)
    yn2 = float(p.P["N2_Landing-colonly"][1].bounds[1][1]); deck = float(p.P["Deck_Finish"][1].bounds[1][1]); roof = float(p.P["Roof"][1].bounds[1][1])
    print("tt_slide_tower.glb", "tris", int(tris), "bbox", lo.round(4).tolist(), hi.round(4).tolist(), "yn2", round(yn2, 4), "DECK", round(deck, 4), "roof", round(roof, 4))
    W = {}
    for i, v in enumerate(VARIANTS, 1):
        pp = build(v); fl = trimesh.creation.box(bounds=[[-2.6, -.2, -2.4], [0, 0, 3.2]]); fl.metadata["uv"] = np.zeros((8, 2)); pp.P["Entry_Floor-colonly"] = (G, fl)
        W[f"v{i}"] = walk_check(pp, pp.walk)
    print("WALK", json.dumps(W)); json.dump(W, open(os.path.join(RENDER_OUT, "slide_tower", "walk_check.json"), "w"), indent=1)
