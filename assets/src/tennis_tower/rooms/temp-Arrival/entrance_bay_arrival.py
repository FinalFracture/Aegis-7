"""Arrival: 4.0 m W main-entrance bay (tt_entrance_bay) and 2.0 m half (tt_entrance_bay_half) per 44 m plan / Rev 2.8+.
Court Wayfinding bays: SCR Door_Scissor / Upper_Scissor, no kerb/hedge in egress,
closed-box half-jambs for tiling, colliders, canopy 2.6 m.
The 2.0 m half is retained for non-W runs and seams; it is NOT placed on the 44 m W run.
Run from tennis_tower/:
python3 rooms/temp-Arrival/entrance_bay_arrival.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TT = os.path.dirname(os.path.dirname(HERE))  # .../tennis_tower
sys.path.insert(0, TT)
sys.path.insert(0, os.path.join(TT, "structure"))
from modlib import *
from restroom_extras import crest
try:
    from structure.struct_lib import SCR, finish_scissor
except ImportError:
    from struct_lib import SCR, finish_scissor
H, TD, T2 = 6.1, 2.6, 4.35
def build(q):
    """Court Wayfinding bay. width defaults to 4.0; other widths still build. 4.0 and 2.0 are promoted."""
    w = q.get("width", 4.0); h = w/2; X0, X1 = -h + .001, h - .001; p = Part()
    hf = -h + .06
    # Loft fin replaced by a closed box (facade_bay_final._fin belly=0) so caps are not zero-area.
    # Full fin section: box(hf - .025, hf + .025, .05 - E, H - .15 + E, .03 - .6, .03)
    # Each end keeps a 0.025 half so the next bay does not coplanar-stack and column clad sits proud.
    # Inner faces stay put (left hf+.025, right h-.045) so the door module is unchanged.
    lj0, lj1 = hf, hf + .025
    rj0, rj1 = h - .045, h - .020
    F = [box(X0, X1, 0, .05, -.65, .12), box(X0, X1, H - .15, H, -.65, .08),
         box(lj0, lj1, .05 - E, H - .15 + E, .03 - .6, .03),
         box(rj0, rj1, .05 - E, H - .15 + E, -.04, .04)]
    cols = [(lj1, rj0)]
    L3 = bool(q.get("leaves3"))   # r8b Rev 3.7 #12 (TTQA-031): 3 x 1.0 m clear leaves at -1.6..-0.6 / -0.5..0.5 / 0.6..1.6, 0.10 m mullions
    if w > 3 and not L3:
        F.append(box(-.05, .05, .05 - E, H - .15 + E, -.05, .05)); cols = [(lj1, -.05), (.05, rj0)]
    if L3:
        F += [box(a, b, .05 - E, H - .15 + E, -.05, .05) for a, b in ((-.6, -.5), (.5, .6))]
        F += [box(a, b, .05 - E, TD - .075 + E, -.05, .05) for a, b in ((-1.6 - .05, -1.6), (1.6, 1.6 + .05))]   # leaf jambs; side lights beyond
    for t in (TD, T2): F.append(box(lj1 - E, rj0 + E, t - .075, t + .075, -.06, .06))
    p.add("Frame", G, *F)
    if L3:
        for i, (a0, b0) in enumerate(((-1.6, -.6), (-.5, .5), (.6, 1.6))):
            a, b = a0 + .003, b0 - .003
            # Rev 3.8.1: each leaf is its own node set (Leaf_<i>_*) + Leaf_<i>-colonly; group_leaves3() parents them under Leaf_<i>
            p.add(f"Leaf_{i}_Stiles", ALY, box(a, a + .07, .06, TD - .08, -.03, .03), box(b - .07, b, .06, TD - .08, -.03, .03),
                  *[box(a + .07 - E, b - .07 + E, u, v, -.03, .03) for (u, v) in ((.06, .18), (TD - .2, TD - .08))])
            p.add(f"Leaf_{i}_Door_Scissor", SCR, pane(a + .072, b - .072, .18 - E, TD - .2 + E, 0, t=.016))
            p.add(f"Leaf_{i}_Push_Bar", ALY, tube((a + .15, 1.05, .07), (b - .15, 1.05, .07), .02, 8), tube((a + .15, 1.05, .03 - E), (a + .15, 1.05, .07), .012, 6), tube((b - .15, 1.05, .03 - E), (b - .15, 1.05, .07), .012, 6))
            p.add(f"Leaf_{i}-colonly", ALY, box(a, b, .06, TD - .08, -.03, .03))
        for k, (a0, b0) in enumerate(((lj1, -1.65), (1.65, rj0))):
            p.add(f"Side_Scissor_{k}", SCR, pane(a0 + .002, b0 - .002, .05, TD - .075 + E, 0))
        for i, (a0, b0) in enumerate(((lj1, -.6), (-.5, .5), (.6, rj0))):
            for r, (y0, y1) in enumerate(((TD + .075, T2 - .075), (T2 + .075, H - .15))):
                p.add(f"Upper_Scissor_{i}{r}", SCR, pane(a0 + .002, b0 - .002, y0 - E, y1 + E, 0))
        cols = [(-1.6, -.6), (-.5, .5), (.6, 1.6)]
    for i, (a0, b0) in enumerate([] if L3 else cols):
        a, b = a0 + .003, b0 - .003; m = (a + b)/2
        S = [box(a, a + .07, .06, TD - .08, -.03, .03), box(b - .07, b, .06, TD - .08, -.03, .03), box(m - .035, m + .035, .06, TD - .08, -.03, .03)]
        S += [box(a + .07 - E, b - .07 + E, u, v, -.03, .03) for (u, v) in ((.06, .18), (TD - .2, TD - .08))]
        p.add("Door_Stiles", ALY, *S)
        for k, (u, v) in enumerate(((a + .07, m - .035), (m + .035, b - .07))):
            p.add(f"Door_Scissor_{i}{k}", SCR, pane(u + .002, v - .002, .18 - E, TD - .2 + E, 0, t=.016))
            p.add("Push_Bars", ALY, tube((u + .12, 1.05, .07), (v - .12, 1.05, .07), .02, 8), tube((u + .12, 1.05, .03 - E), (u + .12, 1.05, .07), .012, 6), tube((v - .12, 1.05, .03 - E), (v - .12, 1.05, .07), .012, 6))
        for r, (y0, y1) in enumerate(((TD + .075, T2 - .075), (T2 + .075, H - .15))):
            p.add(f"Upper_Scissor_{i}{r}", SCR, pane(a0 + .002, b0 - .002, y0 - E, y1 + E, 0))
    # ---- canopy: slab + deep soffit + 3-step fascia (depth stays 2.6 m) ----
    y0, y1, zt = 3.0, 3.16, 2.6; cx0, cx1 = X0 + .02, X1 - .02
    p.add("Canopy", SL, box(cx0, cx1, y0, y1, .061, zt), box(-h + .05, -h + .12, y0 - .34, y1 + E, .061 - E, .6), box(h - .12, h - .05, y0 - .34, y1 + E, .061 - E, .6))
    p.add("Canopy_Soffit", ALY, box(-h + .123, h - .123, y0 - .12, y0 + E, .3, zt - .02), box(-h + .123, h - .123, y0 - .06, y0 + E, .63, .3 + E))
    p.add("Soffit_Downlights", CY, *[box(cx0 + .2, cx1 - .2, y0 - .128, y0 - .12 + E, z, z + .04) for z in (.9, 1.5, 2.1)])
    p.add("Fascia_Slate", SL, box(cx0, cx1, y0 - .26, y1 + .06, zt - E, zt + .1))
    p.add("Fascia_Gunmetal", G, box(cx0, cx1, y0 - .16, y1 + .02, zt + .1 - E, zt + .18), box(cx0, cx1, y1 + .06 - E, y1 + .12, zt - .3, zt + .1 - .003))
    p.add("Court_Line_LED", AM, box(cx0, cx1, y0 - .26 - E, y0 - .23, zt + .1 - E, zt + .11), box(cx0, cx1, y0 - .06, y0 - .03, zt + .18 - E, zt + .19), box(cx0, cx1, y1 - E, y1 + .006, .3, .34))
    for x in (-h*.65, h*.65): p.add("Tie_Rods", ST, tube((x, 5.4, .06 - E), (x, y1 - E, zt - .4), .028, 6))
    # ---- wayfinding blade (double-sided) ----
    by0, by1, bz0, bz1 = y1 + .12 - E, y1 + 1.0, zt - .55, zt - .05
    p.add("Blade_Core", SL, box(-.05, .05, by0 + .046, by1 + .004, bz0, bz1))
    p.add("Blade_Frame", G, box(-.065, .065, by1 - E, by1 + .05, bz0 - .015, bz1 + .015), box(-.065, .065, by0, by0 + .05, bz0 - .015, bz1 + .015),
          box(-.065, .065, by0 + .03, by1 + .02, bz1 - .01, bz1 + .015), box(-.065, .065, by0 + .03, by1 + .02, bz0 - .015, bz0 + .01))
    G2 = []
    for sx in (-1, 1):
        o = sx*.05; d = (lambda u, v: (min(o + sx*.012, o - sx*.004), max(o + sx*.012, o - sx*.004)))(0, 0)
        G2 += [box(*d, by0 + .48, by0 + .78, bz0 + .2, bz0 + .25), box(*d, by0 + .36, by0 + .42, bz0 + .2, bz0 + .42), box(*d, by0 + .12, by0 + .2, bz0 + .05, bz1 - .05)]
    p.add("Wayfinding_Glyphs", CY, *G2[:2], *G2[3:5]); p.add("Blade_Court_Stripe", AM, G2[2], G2[5])
    p.add("Blade_Ball_Finial", BA, node((0, by1 + .05 + .08 - E, (bz0 + bz1)/2 - .12), .08, 1))
    p.add("Blade_Leaf_Crest", LF, crest((0, by1 + .05 - E, (bz0 + bz1)/2 + .12)))
    p.add("Fascia_Leaf_Crests", LF, *[crest((x, y1 + .12 - E, zt - .1)) for x in np.arange(-h + .4, h - .3, .8) if abs(x) > .3])
    # slate walk mat only — kerb, hedge and planted edge stay out of the 6 m egress
    p.add("Threshold_Mat", SSL, box(X0 + .02, X1 - .02, 0, .012, .122, 1.4))
    # w>=3: pair at +-h/2 (4.0 m -> +-1.0, pitch 2.0 m). w<3: one bollard at x=0 so pitch stays >= 1.5 m.
    # r8b Rev 3.7 #12 placed posts at +-0.55 (0.95 m clear between, in front of the centre mullion). That
    # put Bollard0 on the W-entrance walk line (bay_z 39.005 through bay 582: local x -0.495, collider
    # to -0.475). Posts move to +-1.50 (outer half of each leaf, in front of the side jambs): 1.35 m
    # clear from the inner face to the centre jamb, 0.93 m from the walk line to the collider; adjacent
    # bays' outer posts stay 1.00 m apart (0.85 m clear). 3l (unplaced) keeps +-0.55 at the mullions.
    boll = (0.0,) if w < 3 else ((-.55, .55) if L3 else (-1.50, 1.50))
    br, bb = (.1, .11) if w < 3 else (.075, .085)
    for x in boll:
        p.add("Ball_Bollards", G, tube((x, .08 - E, 1.55), (x, .85, 1.55), br, 10)); p.add("Bollard_Balls", BA, node((x, .85 + bb - E, 1.55), bb, 1))
    # colliders. Wall starts at y=.5; DoorClear is a floor strip and does not fill the door volume.
    if L3:
        # Rev 3.8.1: fixed Frame-colonly = the wall plane minus the three leaf openings (X -1.6..-0.6 / -0.5..0.5 / 0.6..1.6,
        # Y 0.05..2.525); mullions/leaf jambs/side lights/transom are solid. Leaves (3 mm clear all round) carry their own colliders.
        ot = TD - .075
        p.add("Frame-colonly", G, box(X0, X1, ot, H, -.08, .02),
              *[box(u, v, .05, ot + E, -.08, .02) for u, v in ((X0, -1.6), (-.6, -.5), (.5, .6), (1.6, X1))])
    else:
        p.add("Wall-colonly", G, box(X0, X1, .5, H, -.08, .02))
    p.add("DoorClear-colonly", SL, box(X0, X1, 0, .02, -.3, 1.4))
    for a, b in ([] if L3 else cols):
        p.add("Jamb-colonly", G, box(a - .02, a + .02, 0, H, -.08, .14), box(b - .02, b + .02, 0, H, -.08, .14))
    p.add("Canopy-colonly", SL, box(cx0, cx1, y0, y1, .061, zt))
    if w < 3: p.add("Bollard-colonly", G, *[box(x - .08, x + .08, 0, .96, 1.55 - .08, 1.55 + .08) for x in boll])
    else:
        for k, x in enumerate(boll): p.add(f"Bollard{k}-colonly", G, box(x - .075, x + .075, 0, .85 + 2 * bb, 1.55 - .075, 1.55 + .075))
    return p
def run_layout(widths):
    A = {}; x = 0
    for k, w in enumerate(widths):
        x += w/2
        for n, (mk, m) in build(dict(width=w)).P.items():
            m2 = m.copy(); m2.apply_translation((x, 0, 0)); m2.metadata["uv"] = m.metadata.get("uv", np.zeros((len(m.vertices), 2))); A[f"T{k}_{n}"] = (mk, m2)
        x += w/2
    return A
def seam_check(widths):
    A = run_layout(widths); edge = widths[0]
    near = {k: v for k, v in A.items() if "colonly" not in k and v[1].bounds[1][0] > edge - .6 and v[1].bounds[0][0] < edge + .6}
    chk = cc.check(near, n_samp=300); bad = [o for o in chk["overlap"] if not o[3] and o[0][:2] != o[1][:2]]; cop = [c for c in chk["coplanar"] if c[0][:2] != c[1][:2]]
    return dict(bad=bad[:3], coplanar=cop[:3], pass_=not bad and not cop)
def _promote_one(width, filename):
    p = recenter(build(dict(width=width)))
    gp = os.path.join(ROOT, "godot/assets/models", filename)
    tris, _ = export_final(p.P, [gp]); finish_glb(gp); finish_scissor(gp)
    V = np.vstack([m.vertices for n, (mk, m) in p.P.items() if "colonly" not in n])
    lo, hi = V.min(0), V.max(0)
    print(filename, "tris", int(tris), "bbox", lo.round(4).tolist(), hi.round(4).tolist())
# Rev 3.8.1 3l hinges: inswing (-Z, away from the canopy/push-bar side). Leaf_0 and Leaf_1 hinge on their -X stile edge,
# Leaf_2 on its +X stile edge, all on the leaf back face (z -0.03), so the leaf sweeps inside its own opening.
# Open pose = rotate Leaf_<i> about +Y by OPEN_YAW[i] degrees (closed = 0).
HINGE3 = ((0, -1), (1, -1), (2, +1)); OPEN_YAW3 = (90.0, 90.0, -90.0)
def group_leaves3(gp, p):
    import pygltflib as pg
    g = pg.GLTF2().load(gp); sc = g.scenes[g.scene or 0]; piv = {}
    for i, side in HINGE3:
        lo, hi = p.P[f"Leaf_{i}_Stiles"][1].bounds
        P = [float(lo[0] if side < 0 else hi[0]), 0.0, float(lo[2])]; piv[f"Leaf_{i}"] = [round(v, 4) for v in P]
        kids = [j for j, n in enumerate(g.nodes) if n.name and (n.name.startswith(f"Leaf_{i}_") or n.name == f"Leaf_{i}-colonly")]
        assert len(kids) == 4, kids
        for j in kids:
            t = g.nodes[j].translation or [0, 0, 0]; g.nodes[j].translation = [t[0] - P[0], t[1] - P[1], t[2] - P[2]]
        g.nodes.append(pg.Node(name=f"Leaf_{i}", translation=P, children=kids)); sc.nodes = [j for j in sc.nodes if j not in kids] + [len(g.nodes) - 1]
    g.save_binary(gp); return piv
def _promote_one3(filename):
    p = recenter(build(dict(width=4.0, leaves3=True)))
    gp = os.path.join(ROOT, "godot/assets/models", filename)
    tris, _ = export_final(p.P, [gp]); finish_glb(gp); finish_scissor(gp)
    print(filename, "pivots", group_leaves3(gp, p), "open_yaw", OPEN_YAW3)
    print(filename, "tris", int(tris), "clip", cc.check({k: v for k, v in p.P.items() if "colonly" not in k}, n_samp=60)["pass"])
def promote():
    """Export 4.0 m tt_entrance_bay and 2.0 m tt_entrance_bay_half. Half is not placed on the 44 m W run.
    r8b: tt_entrance_bay_3l (Rev 3.7 #12, 3 x 1.0 m leaves) is exported for Gage's proximity doors and is NOT placed yet."""
    _promote_one(4.0, "tt_entrance_bay.glb")
    if "--half" in sys.argv: _promote_one(2.0, "tt_entrance_bay_half.glb")
    _promote_one3("tt_entrance_bay_3l.glb")
if __name__ == "__main__":
    promote(); print("SEAM", seam_check([4, 4]), seam_check([4, 2]), seam_check([2, 4]))
