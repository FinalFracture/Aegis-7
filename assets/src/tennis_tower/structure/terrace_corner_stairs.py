"""Rook (2026-11-20): terrace / facade corner stairs (Jared card answer 3:37 PM CT: "Yes, build the outdoor terrace corner stairs too").
At the four terrace/facade corners the W / E terrace (deck +0.0) stops at its S / N edge (kerb + 1.07 m guard, skirt face Z 13.45 / 66.55)
and the drum floor is ~2.0..2.3 m below (drum(Z) = 195.9592 - sqrt(40000 - (Z - 40)^2)). Each corner gets an exterior stair down to the drum:
  * edge opening: the corner terrace edge module (SW/NW X -16..-12, SE/NE X 140..144) is swapped for an opening variant
    (V1 kit, kerb + guard removed over 3.0 m at the facade end, flush paved threshold): tt_terrace_edge_open_cs_a (local -2..1, SW yaw 180 /
    NE yaw 0) and tt_terrace_edge_open_cs_b (local -1..2, NW yaw 0 / SE yaw 180). The remaining 1 m of each module keeps its kerb + guard.
  * top landing at +0.0 outside the edge (SW frame: X -15.3..-12.45, Z 11.5..13.45, lip over the skirt head to Z 13.502), solid
    cast fill to the drum, butting the facade plinth (X -12.449, 3 mm) / skirt (X -12.25, 2 mm).
  * one flight running out along -X (SW frame): 12 risers x 0.1664 (= drum(11.5) + 3 mm over 12) on 0.30 treads, X -15.3 -> -18.6,
    clear Z 11.5..13.25 (1.75 m), then a 2.5 m foot pad X -18.6..-21.1 warped onto the drum (flush on its S edge, <= 1:10 on its N edge).
  * 1.07 m solid slate cheeks both sides (S cheek Z 11.30..11.50 also guards the landing's S drop, N cheek Z 13.25..13.447 against the
    terrace skirt), alloy caps, handrails both sides at 0.865 m with 0.3 m extensions. Colliders: 'Access-colonly' (landing, lip,
    Flight_Ramp-style nosing-line ramp, pad) + 'Guard-colonly' (each cheek segment cut into <= 0.40 m bands, TTQA-004 language).
SW is built in building coords; NW = mirror Z about 40, SE = mirror X about 64, NE = both (the drum and the facade/terrace are symmetric).
SE: facade bay 557's decorative tree pedestal (X 140.445..140.869, Z 13.05..13.45, base +0.0) used to overhang the skirt over the drum; it
now stands on the SE landing deck (top +0.0, contact) in the landing's facade/edge corner, clear of the walk line (opening 2.13 m clear
beside it, landing 1.55 m).
5 dress variants (V1 placed): python3 terrace_corner_stairs.py          -> v1..v5 + contact sheet (assets/glb/tennis_tower/terrace_corner_stair)
                               python3 terrace_corner_stairs.py place    -> tt_struct_terrace_stair_{sw,se,nw,ne} (V1, building frame) +
                                                                            tt_terrace_edge_open_cs_a/_b; layout entries to /workspace/rook_ttqa
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from struct_lib import *
from ridge_crown import huv
from ramps import Kit, RH, RR, RO, GT
from access_rev37 import U, drum, edge_open, export_part, MZ, MX
import trimesh

N, TR = 12, .30
X_TOP = -15.3                       # flight-1 top nosing (landing W edge)
XP, XF = -12.452, -12.252           # landing E end above +0 (plinth face -12.449) / below (skirt face -12.25)
XO = -14.998                        # opening W end (kerb segment ends -15.002)
Z0, Z1 = 11.5, 13.25                # flight clear width
ZS, ZL = 13.447, 13.502             # landing N edge (skirt face 13.45) / lip end (threshold face 13.5035, 1.5 mm)
R = -(drum(Z0) + .003) / N          # 0.16638
YB = drum(13.5) - .12               # common fill bottom
F1 = (N - 1) * TR                   # 3.3: last nosing
XB, XE_ = X_TOP - F1, X_TOP - F1 - 2.5   # -18.6 pad start, -21.1 pad end
CS = (Z0 - .2, Z0 + E); CN = (Z1 - E, ZS)  # cheek Z spans

def nose(x):                         # nosing line along the run (landing 0, flight, pad -12R)
    d = X_TOP - x
    if d <= 0: return 0.0
    if d <= F1: return -R * d / TR
    return -N * R

def _bands(m, h=.40):
    lo, hi = m.bounds[0][1], m.bounds[1][1]; nb = max(1, int(np.ceil((hi - lo) / h - 1e-6))); out = []
    for i in range(nb):
        y0, y1 = lo + (hi - lo) * i / nb, lo + (hi - lo) * (i + 1) / nb; b = m
        if i > 0: b = b.slice_plane([0, y0, 0], [0, 1, 0], cap=True)
        if i < nb - 1: b = b.slice_plane([0, y1, 0], [0, -1, 0], cap=True)
        b = trimesh.Trimesh(b.vertices.copy(), b.faces.copy()); b.metadata["uv"] = np.zeros((len(b.vertices), 2)); out.append(b)
    return out

def seg_prism(a, b, z0, z1, ybot, top):
    return huv([(x, y, z) for x in (a, b) for z in (z0, z1) for y in (ybot, top(x))])

def build(prm=None):
    """SW corner stair in building coords -> (Kit, guard bands)."""
    prm = prm or {}; k = Kit(); dress = prm.get("dress", "court")
    # ---- body (visual): landing + under-plinth fill + lip + 11 treads + warped pad
    D = [box(X_TOP, XO, YB, 0.0, Z0, Z1), box(XO - .004, XP, YB, 0.0, Z0, ZS), box(XP - .01, XF, YB, -.003, Z0, ZS)]
    LIP = box(XO + .002, XP, -.298, 0.0, ZS - .007, ZL)
    x = X_TOP; NOS = []
    for i in range(N - 1):
        y = -(i + 1) * R
        D.append(box(x - TR, x + .02, YB, y, Z0, Z1))
        NOS.append(box(x - TR + .008, x - TR + .05, y - E, y + .004, Z0 + .05, Z1 - .05))
        x -= TR
    NOS.insert(0, box(X_TOP + .008, X_TOP + .05, -E, .004, Z0 + .05, Z1 - .05))
    yl = -N * R
    pad = huv([(xx, yy, zz) for xx in (XB + .02, XE_) for zz in (Z0, Z1) for yy in (YB, (yl if xx != XE_ else drum(zz) + .003))])
    D.append(pad)
    body = U(D + [LIP])
    k.add("Stair_Body", SSL, body)
    k.add("Nosing_Court_Line", AM if dress == "amber" else WH, *NOS)
    # ---- colliders: landing + lip + nosing-line ramp (one tread onto the pad) + pad
    ramp = huv([(X_TOP - d, yy, zz) for d, yt in ((0.0, 0.0), (F1 + TR, yl)) for zz in (Z0, Z1) for yy in (YB, yt)])
    k.col(D[0].copy(), D[1].copy(), D[2].copy(), LIP.copy(), ramp, pad.copy())
    # ---- cheeks: S (landing + flight + pad), N (0.3 m landing return + flight + pad)
    BP = [X_TOP, XB, XE_]
    W, CAP, G = [], [], []
    def run(z0, z1, xs_land):
        segs = []
        if xs_land: segs.append((xs_land, X_TOP, lambda xx: GT))
        for a, b in zip(BP[:-1], BP[1:]): segs.append((a, b, lambda xx: nose(xx) + GT))
        for a, b, top in segs:
            pr = seg_prism(a, b, z0, z1, YB, top); W.append(pr); G.extend(_bands(pr))
            CAP.append(huv([(xx, yy, zz) for xx in (a, b) for zz in (z0 + .002, z1 - .002) for yy in (top(xx) - E, top(xx) + .03)]))
    run(*CS, XP); run(*CN, XO)
    sx = box(XP - .01, XF, YB, -.003, *CS); W.append(sx); G.append(sx.copy())       # S cheek under the plinth to the skirt face
    k.add("Cheek_Walls", SL, U(W)); k.add("Cheek_Caps", LF if dress == "leaf" else ALY, U(CAP))
    rail = [(XO, RH), (X_TOP, RH), (XB, nose(XB + 1e-6) + RH), (XB - .3, nose(XB + 1e-6) + RH)]
    k.rail(rail, CS[1] + RO, "x", CS[1]); k.rail(rail, CN[0] - RO, "x", CN[0])
    # ---- dress (visual only)
    if dress == "green":       # clipped green band on the S cheek's outer (drum) face
        cl = []
        for i, xx in enumerate(np.arange(XP - .3, XE_ + .2, -.55)):
            yt = (nose(xx) if xx < X_TOP else 0.0) + GT
            cl.append(clump((xx, yt - .32, CS[0] - .13 + .006), .13, seed=i))
        k.add("Cheek_Green_Band", LF, *cl)
    if dress == "amber":       # step lights in the cheek inner faces, one per tread
        L = []
        for i in range(N - 1):
            xx = X_TOP - (i + .5) * TR; y = -(i + 1) * R + .22
            L += [box(xx - .1, xx + .1, y, y + .025, CS[1] - E, CS[1] + .006), box(xx - .1, xx + .1, y, y + .025, CN[0] - .006, CN[0] + E)]
        k.add("Step_Lights", AM, *L)
    if dress == "leaf":        # leaf crests along the S cheek cap
        LV = []
        for xx in np.arange(XP - .4, XE_ + .3, -1.2):
            for x2, ln, wd, pt in ((xx, .32, .12, -.35), (xx + .12, .26, .10, .35)):
                yt = (nose(x2) if x2 < X_TOP else 0.0) + GT + .03 + .002
                LV.append(leaf((x2, yt, sum(CS) / 2), ln, wd, yaw=np.pi / 2, pitch=pt))
        k.add("Leaf_Crests", LF2, *LV)
    if dress == "rally":       # white court-line band on the S cheek outer face + tennis-ball finials on the cheek ends
        BL = []
        for a, b in zip([XP] + BP[:-1], BP):
            ya, yb = (nose(a) if a < X_TOP else 0.0) + GT - .14, (nose(b) if b < X_TOP else 0.0) + GT - .14
            BL.append(huv([(xx, yy, zz) for xx, yt in ((a, ya), (b, yb)) for zz in (CS[0] - .006, CS[0] + E) for yy in (yt, yt + .05)]))
        k.add("Court_Line_Band", WH, *BL)
        k.add("Ball_Finials", BA, *[node((xx, nose(xx) + GT + .03 + .06 - E, zc), .06, 1) for xx in (XE_ + .1, X_TOP) for zc in (sum(CS) / 2, sum(CN) / 2)])
    return k, G

def to_part(name, k, G):
    p = Part(name); groups = {}
    for pn, mk, m in k.I: groups.setdefault((pn, mk), []).append(m)
    for (pn, mk), ms in groups.items(): p.add(pn, mk, *ms)
    p.add("Access-colonly", SL, *[m.copy() for m in k.C]); p.add("Guard-colonly", SL, *[m.copy() for m in G])
    return p

VARIANTS = [
    dict(label="V1 Court Line: slate cheeks, alloy caps, white nosings", dress="court"),
    dict(label="V2 Living Cheek: clipped green band on the drum-side cheek", dress="green"),
    dict(label="V3 Amber Step: amber nosings + cheek step lights", dress="amber"),
    dict(label="V4 Leaf Crest: leaf-green caps with leaf crests", dress="leaf"),
    dict(label="V5 Rally Mark: white court-line band, tennis-ball finials", dress="rally"),
]
def build_local(prm):
    k, G = build(prm); return to_part("terrace_corner_stair", k, G)

CORNERS = {"sw": np.eye(4), "nw": MZ, "se": MX, "ne": MX @ MZ}
EDGES = {"tt_terrace_edge_open_cs_a": (-2.0, 1.0), "tt_terrace_edge_open_cs_b": (-1.0, 2.0)}

def place(out_dir="/workspace/rook_ttqa/terrace_stairs"):
    os.makedirs(out_dir, exist_ok=True); REP, LAY = [], {}
    for c, M in CORNERS.items():
        k, G = build(VARIANTS[0])
        for _, _, m in k.I: uv = m.metadata.get("uv"); m.apply_transform(M); m.metadata["uv"] = uv
        for m in list(k.C) + G: m.apply_transform(M)
        groups = {}
        for pn, mk, m in k.I: groups.setdefault((pn, mk), []).append(m)
        export_chunk(f"tt_struct_terrace_stair_{c}", [(pn, mk, ms) for (pn, mk), ms in groups.items()],
                     [("Access-colonly", k.C), ("Guard-colonly", G)], REP, layout=LAY,
                     note=f"Terrace corner stair {c.upper()} (Jared 2026-11-20 3:37 PM CT): 12 x {R:.4f} / 0.30, top landing +0.0, 2.5 m drum pad, 1.07 m cheeks")
    for nm, (a, b) in EDGES.items():
        export_part(nm, edge_open(a, b, nm), REP, None, f"terrace corner stair edge opening, local {a}..{b}")
    json.dump(LAY, open(os.path.join(out_dir, "layout_entries.json"), "w"), indent=1)
    json.dump(REP, open(os.path.join(out_dir, "report.json"), "w"), indent=1, default=str)
    print("ASSETS", len(REP), "FAILED", [r["asset"] for r in REP if not r["passed"]])

if __name__ == "__main__":
    if sys.argv[1:2] == ["place"]: place()
    else:
        import modlib as ML
        ML.RENDER_OUT = "/workspace/renders/terrace_stairs"
        a, b = np.radians(215), np.radians(26)       # drum-side (-Z) iso: the side players approach from
        view = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]) @ np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
        rep = ML.run("terrace_corner_stair", build_local, VARIANTS, view=view, title=f"12 x {R:.4f} / 0.30, landing +0.0, 2.5 m drum pad, 1.07 m cheeks (SW frame, drum-side view)")
