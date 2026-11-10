"""Rook: Tennis Tower aquatic slide tower T1/T2 (spec §3.6: 5 x 5 m). Island datum y0 = F1+1.0; N2 5.1 / deck 6.0 / roof 8.4 local
(= +6.1/+7.0/+9.4 building), roof under the +9.7 soffit. Stair half (-X): switchback 8/8/7/7 risers x 0.17 to bridge landing N2 at 5.1,
then 5 risers x 0.18 eastward onto the start deck at 6.0. T1 has the +Z link opening; T2 is the Z-mirror with the -X bridge gate at final
local Z -1.36..-0.26 (world 58.14..59.24 at Z 59.5, r3: matches the Aquatics 9c11848 gate clear opening) and its link opening on -Z. Slide tube stub leaves through the +X face (invert at deck).
REUSE: stair_core_colliders_rev_c.slab_between ramps + Rev C stair materials/finish/nosing scheme (tt_stair_core V5), court-partition
scissor guard language, curtain-wall fin() (Branch Fin), restroom Leaf Crest crest(), stand planter()/shrubs(), green_wall(), tree-column CHS columns.
Run: python3 slide_tower.py"""
from modlib import *
from stair_core_colliders_rev_c import slab_between
from restroom_extras import crest
from structure.struct_lib import SCR, finish_scissor
FIN, NOSE, T, TH = .015, .03, .28, .25
TH2 = .09   # thin steel-pan cast for flight 4, S2 + N2: 16/14 riser split leaves N2-N1 = 2.38 m, so 0.25 casts would cut headroom to 1.96
NS = [8, 8, 7, 7]; R = 5.1 / sum(NS); R5, N5 = .18, 5
XA, XB = (-2.3, -1.25), (-1.15, -.1); ZN, ZS, ZI = 1.2, -2.3, 2.3; C = 2.4
DECK = 6.0; YR = DECK + 2.15; ROOF = YR + .25   # 8.15 roof underside, 8.4 roof top
PG = .011  # half pane thickness
TH3 = .03         # r3: N2 extension pan thickness over the flight-3 start
GZ = (.26, 1.36)  # r3: T2 -X bridge-gate opening, pre-mirror local Z (world 58.14..59.24)
def U(m): m.metadata["uv"] = np.zeros((len(m.vertices), 2)); return m

def flight(p, xr, z0, y0, n, d, nos, th=TH):  # d=-1 rises toward -Z, +1 toward +Z; first riser at z0
    xa, xb = (xr[0], xr[1] + E) if xr is XA else (xr[0] - E, xr[1])
    for k in range(1, n):
        za, zb = sorted((z0 + d*(k-1)*T, z0 + d*k*T)); yt = y0 + k*R
        if k == n - 1: za, zb = (za - E, zb) if d < 0 else (za, zb + E)
        if k == 1: za, zb = (za, zb + E) if d < 0 else (za - E, zb)
        p.add("Stair_Cast", WH, box(xa, xb, .002 if y0 == 0 else yt - th, yt - FIN + E, za, zb))
        fa, fb = (za + .002, zb + .005) if d < 0 else (za - .005, zb - .002)
        p.add("Treads_Slate", SSL, box(xa + .002, xb - .002, yt - FIN, yt, fa, fb))
        if nos: p.add("Nosing_Emergency", AM, box(xr[0] + .03, xr[1] - .03, yt - .003, yt + .002, *((fb - NOSE, fb - .002) if d < 0 else (fa + .002, fa + NOSE))))
    zl = z0 + d*(n-1)*T; y1 = y0 + n*R
    p.add(f"F{len([k for k in p.P if k.startswith('F') and k.endswith('_Ramp-colonly')]) + 1}_Ramp-colonly", G, slab_between(*xr, z0 - d*T, y0, zl, y1))
    return zl, y1

def landing(p, tag, z0, z1, y, th=TH):
    p.add("Stair_Cast", WH, box(XA[0], XB[1], y - th, y - FIN + E, z0, z1)); p.add("Treads_Slate", SSL, box(XA[0] + .002, XB[1] - .002, y - FIN, y, z0 + .002, z1 - .002))
    p.add(f"{tag}_Landing-colonly", G, trimesh.creation.box(bounds=[[XA[0], y - th, z0], [XB[1], y, z1]]))

def build(q):
    p = Part(); nos = q.get("nosing", False); t2 = q.get("tower", "t1") == "t2"
    ZN1, ZN2 = (.68, .40) if t2 else (1.2, 1.2); sz = -1 if t2 else 1; ZN2L = ZN2 - .14 if t2 else ZN2
    # --- switchback to the bridge landing (stair frame: N landings toward +Z) ---
    z, y = flight(p, XA, ZN1, 0.0, NS[0], -1, nos); landing(p, "S1", ZS, z - E*0, y); zs1 = z
    z, y = flight(p, XB, zs1, y, NS[1], +1, nos); landing(p, "N1", ZN1, ZI, y); yn1 = y
    if t2:  # XA-lane extension ZN2..ZN1 so flight 3 can start at ZN2
        p.add("Stair_Cast", WH, box(XA[0], XA[1] + E, y - TH, y - FIN + E, ZN2, ZN1))
        p.add("Treads_Slate", SSL, box(XA[0] + .002, XA[1] + E - .002, y - FIN, y, ZN2 + .002, ZN1 - .002))
        p.add("N1x_Landing-colonly", G, trimesh.creation.box(bounds=[[XA[0], y - TH, ZN2], [XA[1] + E, y, ZN1]]))
    z, y = flight(p, XA, ZN2, y, NS[2], -1, nos); landing(p, "S2", ZS, z, y, TH2); zs2, ys2 = z, y
    z, y = flight(p, XB, zs2, y, NS[3], +1, nos, TH2); landing(p, "N2", ZN2, ZI, y, TH2); yn2 = y
    if t2:  # r3: N2 extension over the XA lane (ZN2L..ZN2) so the whole shifted -X gate opening (GZ 0.26..1.36) lands on N2, not over flight 3
        p.add("Stair_Cast", WH, box(XA[0], XA[1] + E, y - TH3, y - FIN + E, ZN2L, ZN2 + E))   # 30 mm steel-pan nose keeps >= 2.1 m headroom over flight 3
        p.add("Treads_Slate", SSL, box(XA[0] + .002, XA[1] + E - .002, y - FIN, y, ZN2L + .002, ZN2 + E - .002))
        p.add("N2x_Landing-colonly", G, trimesh.creation.box(bounds=[[XA[0], y - TH3, ZN2L], [XA[1] + E, y, ZN2 + E]]))
    # --- flight 5 eastward onto the deck (ZN = 1.2 band for both towers) ---
    x0 = XB[1]
    for k in range(1, N5):
        xa, xb, yt = x0 + (k-1)*T - (E if k == 1 else 0), x0 + k*T + (E if k == N5 - 1 else 0), yn2 + k*R5
        p.add("Stair_Cast", WH, box(xa, xb, yt - TH, yt - FIN + E, ZN, ZI)); p.add("Treads_Slate", SSL, box(xa - .005, xb - .002, yt - FIN, yt, ZN + .002, ZI - .002))
        if nos: p.add("Nosing_Emergency", AM, box(xa - .003, xa + NOSE - .005, yt - .003, yt + .002, ZN + .03, ZI - .03))
    x5 = x0 + (N5 - 1)*T
    hull = lambda pts: trimesh.convex.convex_hull(np.array(pts))
    p.add("F5_Ramp-colonly", G, hull([(x, yy - dy, z) for (x, yy) in ((x0 - T, yn2), (x5, DECK)) for dy in (0, .2) for z in (ZN, ZI)]))
    # --- start deck (+X half) ---
    p.add("Deck", WH, box(-.035, ZI, DECK - TH, DECK - FIN + E, ZS, ZN - .002), box(x5 - E, ZI, DECK - TH, DECK - FIN + E, ZN - .01, ZI + .003))
    p.add("Deck_Finish", SSL, box(-.033, ZI - .002, DECK - FIN, DECK, ZS + .002, ZN - .004), box(x5 + .002, ZI - .002, DECK - FIN, DECK, ZN - .004 + E, ZI - .002))
    p.add("Deck-colonly", G, U(trimesh.creation.box(bounds=[[-.035, DECK - TH, ZS], [ZI, DECK, ZN]])), U(trimesh.creation.box(bounds=[[x5, DECK - TH, ZN], [ZI, DECK, ZI]])))
    # --- spine wall between the flights ---
    sw = []
    if zs2 - zs1 > .01: sw.append(box(XA[1], XB[0], 0, ys2 - TH2 - .002, zs1 - 2*E, zs2 + E))
    sw.append(box(XA[1], XB[0], 0, yn2 + 1.0, zs2 + .006, ZN2 - .002))
    if t2: sw.append(box(XA[1], XB[0], 0, yn2 - TH2 - .002, ZN2 + .002, ZN1 - .002))
    p.add("Spine_Wall", q.get("spine_mat", WH), *sw)
    # --- columns + roof (tree-column CHS language) ---
    p.add("Columns", G, *[tube((sx*C, 0, szc*C), (sx*C, YR + E, szc*C), .1, 16) for sx in (-1, 1) for szc in (-1, 1)])
    p.add("Roof", q.get("roof_mat", WH), box(-2.6, 2.6, YR, ROOF, -2.6, 2.6))
    # --- scissor enclosure (court-partition guard language), split around openings ---
    e = 2.305; gt = YR - .002; LX0, LX1 = 1.10, 2.20; GZ0, GZ1 = GZ
    oz0, oz1 = sorted((sz * -1.7, sz * -.7)); outer = []
    if t2:  # -X bridge gate Z 0.26..1.36 (lands at -1.36..-0.26 after the T2 mirror)
        outer += [(-C - PG, -C + PG, 0, gt, -e, GZ0), (-C - PG, -C + PG, 0, yn2 - TH2 - .02, GZ0, GZ1), (-C - PG, -C + PG, yn2 + 2.3, gt, GZ0, GZ1), (-C - PG, -C + PG, 0, gt, GZ1, e)]
    else: outer += [(-C - PG, -C + PG, 0, gt, -e, e)]   # -X, full pane, no bridge opening
    outer += [(XA[1], LX0, 0, gt, C - PG, C + PG), (LX1, e, 0, gt, C - PG, C + PG), (LX0, LX1, 0, DECK - .052, C - PG, C + PG)]  # +Z link opening X 1.10..2.20
    outer += [(-e, XA[1], 2.4, gt, C - PG, C + PG)]   # +Z ground entry
    outer += [(-e, e, 0, gt, -C - PG, -C + PG)] if q.get("south") != "green" else [(-.05, e, 0, gt, -C - PG, -C + PG)]
    outer += [(C - PG, C + PG, 0, gt, -e, oz0), (C - PG, C + PG, 0, gt, oz1, e), (C - PG, C + PG, 0, DECK - .07, oz0, oz1), (C - PG, C + PG, DECK + .9, gt, oz0, oz1)]  # +X, slide opening
    panes = [box(*a) for a in outer]
    panes += [box(-.05 - PG, -.05 + PG, 0, DECK + 1.1, ZS, ZN - .003), box(-.05 - PG, -.05 + PG, 0, yn2 - TH2 - .05, ZN + .003, ZI - .003)]  # inner screen (stair | shaft)
    panes += [box(-.035, x5, DECK + .002, DECK + 1.1, ZN - .03, ZN - .008), box(XA[0], XA[1] - .002, yn2 + .002, yn2 + 1.1, ZN2L + .008, ZN2L + .03)]  # deck + N2 edge guards
    p.add("Enclosure_Scissor", SCR, *panes)
    p.add("Enclosure-colonly", G, *[U(trimesh.creation.box(bounds=[[a[0], a[2], a[4]], [a[1], a[3], a[5]]])) for a in outer])
    p.add("Link_Sill", SGM, box(LX0 + .004, LX1 - .004, DECK - .05, DECK - .002, ZI - E, C + PG + .002))
    p.add("Link_Sill-colonly", G, U(trimesh.creation.box(bounds=[[LX0, DECK - TH, ZI - E], [LX1, DECK, C + PG + .002]])))
    if q.get("south") == "green":   # Garden face: solid composite wall on the stair side of -Z with a planted wall outside
        p.add("Garden_Wall", WH, box(-e, -.05 - .002, 0, gt, -C - .05, -C + .05))
        p.add("Green_Wall", LF, *[leaf_dir((x + (.12 if j % 2 else 0), y, -C - .05 - .03), (0, -1, -.3), .26, .14) for j, y in enumerate(np.arange(.35, 2.6, .2)) for x in np.arange(-2.2, -.35, .26)])
    # --- slide start: gate posts + tube stub (sz pre-mirrors T2 so the stub matches T1 after the Z flip) ---
    p.add("Gate_Posts", SGM, *[box(2.07, 2.13, DECK - E, YR + E, *sorted((sz * zc - .03, sz * zc + .03))) for zc in (-1.75, -.65)])
    lz0, lz1 = sorted((sz * -.67, sz * -.63)); p.add("Start_Light", q.get("light", GRN), box(2.13 - E, 2.15, DECK + 1.2, DECK + 1.35, lz0, lz1))
    tb = ring_band(.4, .125, h=.25, n=16, t=.05); tb.apply_transform(trimesh.transformations.rotation_matrix(-np.pi/2, [0, 0, 1])); tb.apply_translation((2.302, DECK + .4, sz * -1.2))
    tb.metadata["uv"] = np.zeros((len(tb.vertices), 2)); p.add("Slide_Tube", q.get("tube", CY), tb)
    dress(p, q, yn1, ys2, yn2, x5)
    for k, (mk, m) in list(p.P.items()):
        if "colonly" not in k: continue
        if m.bounds[0][1] < 0: m = m.slice_plane([0, 0, 0], [0, 1, 0], cap=True)  # F1 ramp slab dips below the floor
        m.update_faces(m.nondegenerate_faces()); m.remove_unreferenced_vertices()  # slice cap slivers -> zero-length shade_split normals
        m.metadata["uv"] = np.zeros((len(m.vertices), 2)); p.P[k] = (mk, m)
    if t2:
        p.walk = [(-1.775, 2.9), (-1.775, -1.8), (-.625, -1.8), (-.625, 1.75), (-1.775, 1.75), (-1.775, -1.8), (-.625, -1.8), (-.625, 1.75), (1.6, 1.75), (1.6, 1.2), (1.95, 1.2)]
        p.walk_gate = [(-.625, 1.75), (-1.775, 1.75), (-1.775, .81), (-2.28, .81)]   # r3: gate centre GZ 0.81
    else:
        p.walk = [(-1.775, 2.9), (-1.775, -1.7), (-.625, -1.7), (-.625, 1.75), (-1.775, 1.75), (-1.775, -1.5), (-.625, -1.5), (-.625, 1.75), (1.6, 1.75), (1.6, -1.2), (1.95, -1.2), (1.6, 1.75), (1.65, 2.3)]
    return p

def dress(p, q, yn1, ys2, yn2, x5):
    d = q["dress"]; sz = -1 if q.get("tower", "t1") == "t2" else 1; gy = DECK + 1.1
    if d in ("crown", "garden"):   # green roof (stand planter + shrubs) kept under the +9.7 soffit
        tr, so, sy = planter(-2.4, 2.4, ROOF - E, -2.4, 2.4, h=.08); p.add("Roof_Planter", G, tr); p.add("Planter_Soil", SO, so)
        p.add("Roof_Foliage", LF2, *[shrubs(-2.3, 2.3, sy, z, r=.1, n=14, seed=int(z*10 + 30)) for z in (-1.6, 0, 1.6)])
    if d == "crown":   # Tree Crown: leaf caps on every column (tree-column V4 echo) under the roof
        p.add("Leaf_Caps", LF, *[leaf_dir((sx*(C + .08), YR - .15, szc*(C + .08)), (sx*.3, -1, szc*.3), .28, .16) for sx in (-1, 1) for szc in (-1, 1)])
    if d == "fin":     # Branch Fin: fish-belly fins on the +Z and -Z faces (curtain-wall V3)
        fs = []
        for szf in (-1, 1):
            for x in np.arange(-2.1, 2.2, .6):
                if szf > 0 and x < -1.2: continue     # keep the ground entry clear
                f = xf(fin(0, .3, YR - .3, .1, .04, 0, belly=.8), R=trimesh.transformations.rotation_matrix(np.pi if szf > 0 else 0, [0, 1, 0])); f.apply_translation((x, 0, szf*(C + PG + .002)))
                f.metadata["uv"] = np.zeros((len(f.vertices), 2)); fs.append(f)
        p.add("Branch_Fins", ST, *fs)
    if d == "leaf":    # Leaf Crest: leaf crests on the deck guard cap rail + spine, leaf-green fascia (restroom #58 echo)
        p.add("Guard_Cap_Rail", ALY, tube((-.03, gy + .02 - E, 1.181), (x5, gy + .02 - E, 1.181), .02, 6))
        p.add("Leaf_Crests", LF, *[crest((x, gy + .036, 1.181)) for x in np.linspace(.15, x5 - .15, 3)])
        p.add("Fascia_Band", LF, box(-2.6, 2.6, ROOF - E, ROOF + .06, 2.6 - .03, 2.6 + .01), box(-2.6, 2.6, ROOF - E, ROOF + .06, -2.6 - .01, -2.6 + .03))
    if d == "garden":  # Garden Terrace: deck planters at the -Z corner
        tr, so, sy = planter(1.3, 2.25, DECK - E, -2.25, -1.85, h=.45); p.add("Deck_Planter", G, tr); p.add("Deck_Soil", SO, so); p.add("Deck_Foliage", LF2, shrubs(1.35, 2.2, sy, -2.05, r=.15, seed=8))
    if d == "court":   # Court Wayfinding (stair core V5): level discs on the spine, court line on the deck, ball finials on the gate posts
        p.add("Level_Disc", AM, *[cap((XA[1] - .005 + .002, y + 1.6, .2), .3, .01, 16, axis="x") for y in (0, yn1)])
        p.add("Court_Line_Deck", AM, box(.3, 2.0, DECK - .002, DECK + .003, -.15, -.09))
        p.add("Ball_Finials", BA, *[node((2.1, DECK + 1.6, sz * (zc + .03 + .035 - E)), .035, 0) for zc in (-1.75, -.65)])

VARIANTS = [
    dict(label="Tree Crown: green roof, leaf caps on the columns, leaf-green tube", dress="crown", tube=LF2),
    dict(label="Branch Fin: fish-belly steel fins on the +Z and -Z faces", dress="fin", tube=CY),
    dict(label="Leaf Crest: leaf-crest guard rail, leaf fascia, leaf tube", dress="leaf", tube=LF, spine_mat=LF),
    dict(label="Garden Terrace: planted south wall, green roof, deck planter", dress="garden", south="green", tube=GRN),
    dict(label="Court Wayfinding: amber nosings, level discs, ball finials", dress="court", nosing=True, tube=AM, light=GRN),
]
def _rect(xa, xb, ya, yb, za, zb, mir, d):
    xs = sorted((xa + d[0], xb + d[0])); ys = sorted((ya + d[1], yb + d[1]))
    zs = sorted(((-za if mir else za) + d[2], (-zb if mir else zb) + d[2]))
    r = lambda a: [round(float(a[0]), 4), round(float(a[1]), 4)]
    return dict(x=r(xs), y=r(ys), z=r(zs))

if __name__ == "__main__":
    if "--variants" in sys.argv:
        rep = run("slide_tower", build, VARIANTS, title="5 x 5 m, bridge landing +6.1, start deck +7.0, roof +9.4 | nature + sports", post=finish_scissor)
    for t in ("t1", "t2"):
        p = build(dict(VARIANTS[2], tower=t)); mir = t == "t2"
        yn2_m = float(p.P["N2_Landing-colonly"][1].bounds[1][1])
        if mir:
            for k, (mk, m) in list(p.P.items()):
                uv = np.array(m.metadata["uv"]); m.apply_transform(np.diag([1, 1, -1, 1])); m.metadata["uv"] = uv
        V0 = np.vstack([m.vertices for k, (_, m) in p.P.items() if "colonly" not in k]); lo0, hi0 = V0.min(0), V0.max(0)
        d = np.array((-(lo0[0] + hi0[0]) / 2, -lo0[1], -(lo0[2] + hi0[2]) / 2))
        gate = None if not mir else _rect(-C - PG, -C + PG, yn2_m - TH2 - .02, yn2_m + 2.3, *GZ, mir, d)
        link = _rect(1.10, 2.20, DECK - .052, YR - .002, C - PG, C + PG, mir, d)
        p = recenter(p); gp = os.path.join(ROOT, "godot/assets/models", f"tt_slide_tower_{t}.glb")
        tris, _ = export_final(p.P, [gp]); finish_glb(gp); finish_scissor(gp)
        chk = cc.check({k: v for k, v in p.P.items() if "colonly" not in k}, n_samp=400)
        try: ok_v = vm.validate_file(gp, check_tri_range=(1, TRI_MAX), require_textures=False, require_blend_glass=False)
        except AssertionError as e: print("VALIDATE FAIL", e); ok_v = False
        V = np.vstack([m.vertices for _, m in p.P.values()]); lo, hi = V.min(0), V.max(0)
        yn2 = float(p.P["N2_Landing-colonly"][1].bounds[1][1]); deck = float(p.P["Deck_Finish"][1].bounds[1][1])
        roof = float(p.P["Roof"][1].bounds[1][1]); fascia = float(p.P["Fascia_Band"][1].bounds[1][1])
        print(json.dumps(dict(tower=t, tris=int(tris), clip_pass=bool(chk["pass"]), worst_overlap=chk["worst_overlap"], coplanar=chk["coplanar"], open=chk["open"],
                              bbox=[lo.round(4).tolist(), hi.round(4).tolist()], yn2=round(yn2, 4), DECK=round(deck, 4), roof=round(roof, 4), fascia=round(fascia, 4), gate=gate, link=link), default=str))
    W = {}
    for i, v in enumerate(VARIANTS, 1):
        pp = build(v); fl = trimesh.creation.box(bounds=[[-2.6, -.2, -2.4], [0, 0, 3.2]]); fl.metadata["uv"] = np.zeros((8, 2)); pp.P["Entry_Floor-colonly"] = (G, fl)
        W[f"v{i}"] = walk_check(pp, pp.walk)
        pp2 = build(dict(v, tower="t2")); fl2 = trimesh.creation.box(bounds=[[-2.6, -.2, -2.4], [0, 0, 3.2]]); fl2.metadata["uv"] = np.zeros((8, 2)); pp2.P["Entry_Floor-colonly"] = (G, fl2)
        W[f"v{i}_t2"] = walk_check(pp2, pp2.walk); W[f"v{i}_t2_gate"] = walk_check(pp2, pp2.walk_gate, y0=5.1)
    print("WALK", json.dumps(W)); json.dump(W, open(os.path.join(RENDER_OUT, "slide_tower", "walk_check.json"), "w"), indent=1)
