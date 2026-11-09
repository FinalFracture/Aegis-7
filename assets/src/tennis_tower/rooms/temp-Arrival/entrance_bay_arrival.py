"""Arrival: W main-entrance bay (tt_entrance_bay) per 44 m plan / Rev 2.8+.
4.0 m Court Wayfinding bay: TT_GlassScissor doors/transoms, no kerb/hedge in egress,
half-jambs for tiling, colliders, canopy 2.6 m. Run from tennis_tower/: 
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
    """Court Wayfinding bay. width defaults to 4.0; other widths still build, but only 4.0 is promoted."""
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
    if w > 3:
        F.append(box(-.05, .05, .05 - E, H - .15 + E, -.05, .05)); cols = [(lj1, -.05), (.05, rj0)]
    for t in (TD, T2): F.append(box(lj1 - E, rj0 + E, t - .075, t + .075, -.06, .06))
    p.add("Frame", G, *F)
    for i, (a0, b0) in enumerate(cols):
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
    boll = (-h*.5, h*.5)   # 4.0 m bay: x = +-1.0, pitch 2.0 m
    for x in boll:
        p.add("Ball_Bollards", G, tube((x, .08 - E, 1.55), (x, .85, 1.55), .1, 10)); p.add("Bollard_Balls", BA, node((x, .85 + .11 - E, 1.55), .11, 1))
    # colliders. Wall starts at y=.5; DoorClear is a floor strip and does not fill the door volume.
    p.add("Wall-colonly", G, box(X0, X1, .5, H, -.08, .02))
    p.add("DoorClear-colonly", SL, box(X0, X1, 0, .02, -.3, 1.4))
    for a, b in cols:
        p.add("Jamb-colonly", G, box(a - .02, a + .02, 0, H, -.08, .14), box(b - .02, b + .02, 0, H, -.08, .14))
    p.add("Canopy-colonly", SL, box(cx0, cx1, y0, y1, .061, zt))
    p.add("Bollard-colonly", G, *[box(x - .08, x + .08, 0, .96, 1.55 - .08, 1.55 + .08) for x in boll])
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
def promote():
    """4.0 m asset only. The 2.0 m half bay is not part of the 44 m W run."""
    p = recenter(build(dict(width=4.0)))
    gp = os.path.join(ROOT, "godot/assets/models", "tt_entrance_bay.glb")
    tris, _ = export_final(p.P, [gp]); finish_glb(gp); finish_scissor(gp)
    V = np.vstack([m.vertices for n, (mk, m) in p.P.items() if "colonly" not in n])
    lo, hi = V.min(0), V.max(0)
    print("tt_entrance_bay.glb", "tris", int(tris), "bbox", lo.round(4).tolist(), hi.round(4).tolist())
if __name__ == "__main__":
    promote(); print("SEAM", seam_check([4, 4]))
