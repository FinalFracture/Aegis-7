"""Rook (Oct 31, box pipeline): residential exterior list v1 #45 accessible kerb ramp, re-specced after the road cut: ramps between paving top
(y 0.05) and platform level (y 0.30, #16 kerb / platform infill). Rise 0.25 over 3.0 m = 1:12 (plan's 1.5 x 1.2 was for a 0.15 road kerb).
1.5 W (X) x 3.0 run (Z) ; high end at -Z (y 0.30, butts the infill back face Z -15.5 with 4 mm), low end at +Z (y 0.05 = paving top).
Placement: rotation 0, origin (X, 0, -13.996), X clear of the shelter (12..18), e.g. X 9.75 (platform west end); a second at X 20.25 optional.
Cyan tactile warning bars (paving 04 style) across the top 0.6 m, floating 1.5-5 mm above the slope. Zero wood, wordless.
Also usable at curb-edged beds by scaling Z (0.15 rise -> 1.8 m run). Run: python3 ext_kerb_ramp_generator.py"""
import os, sys, json, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
import ext_street_furniture_generator as sf
from ext_street_furniture_generator import Pod, box, cyl, FMAT, G, S, T, A, E, xf
from ext_curb_generator import prof
from ext_road_curved_generator import PL, CY
import ext_clip_check as cc
ZH, W, Y0, Y1 = 1.5, .75, .05, .30
def surf(z): return Y0 + (Y1 - Y0) * (ZH - z) / (2 * ZH)   # top height at z (high at -Z)
def wedge(x0, x1, up=0.0): return prof([(-ZH, 0), (ZH, 0), (ZH, Y0 + up), (-ZH, Y1 + up)], x0, x1)
def band(x0, x1, z0, z1, d0, d1): return prof([(z0, surf(z0) + d0), (z1, surf(z1) + d0), (z1, surf(z1) + d1), (z0, surf(z0) + d1)], x0, x1)  # sloped strip at offsets d0..d1
def bars(xw, n=5):
    out = []
    for c in np.linspace(-1.44, -.96, n): out.append(box(-xw, xw, surf(c - .02) + .0015, surf(c - .02) + .0055, c - .02, c + .02))
    return out
def hull(pts):
    m = trimesh.convex.convex_hull(np.array(pts)); m.metadata["uv"] = np.c_[m.vertices[:, 0], m.vertices[:, 2]]; return m

def ramp(v):
    p = Pod(f"ext_kerb_ramp_0{v}")
    if v == 1:  # Plain Wedge: pearl 1:12 wedge, cyan warning bars, slate guide strip down the centre (paving 04 language)
        p.add("Ramp", PL, wedge(-W, W)); p.add("Tactile_Bars", CY, *bars(.7))
        p.add("Guide_Strip", S, band(-.15, .15, -.9, ZH - .02, .002, .004))
    elif v == 2:  # Railed: wedge + titanium handrails both sides at 0.9 m (posts at 1.0 m)
        p.add("Ramp", PL, wedge(-W, W)); p.add("Tactile_Bars", CY, *bars(.62, 2))
        p.add("Rail_Posts", T, *[box(s * .7 - .02, s * .7 + .02, surf(z - .02) - .004, surf(z) + .906, z - .02, z + .02) for s in (1, -1) for z in (-1.0, 1.0)])
        p.add("Handrails", T, *[band(s * .7 - .025, s * .7 + .025, -1.35, 1.35, .9, .94) for s in (1, -1)])
    elif v == 3:  # Side Upstands: wedge between slate upstands 0.10 proud (wheel/cane guard), amber end caps
        p.add("Ramp", PL, wedge(-.65 - E, .65 + E)); p.add("Tactile_Bars", CY, *bars(.6, 4))
        p.add("Upstands", S, *[prof([(-ZH + .002, .002), (ZH - .002, .002), (ZH - .002, surf(ZH - .002) + .10), (-ZH + .002, surf(-ZH + .002) + .10)], *sorted((s * .65, s * W))) for s in (1, -1)])
        p.add("End_Caps", A, *[box(*sorted((s * .66, s * .74)), surf(ZH - .03) + .10 - E, surf(ZH - .03) + .10 + .006, ZH - .03, ZH + .002) for s in (1, -1)])
    elif v == 4:  # Flared: central 1.0 m ramp with side flares sloping down to paving level (approach from three sides)
        p.add("Ramp", PL, wedge(-.5, .5)); p.add("Tactile_Bars", CY, *bars(.46))
        for s in (1, -1):
            pts = []
            for z in (-ZH + .003, ZH - .003):
                pts += [(s * (.5 - E), .002, z), (s * (.5 - E), surf(z) - .002, z), (s * W, .002, z), (s * W, Y0 - .002, z)]
            p.add("Flares", S, hull(pts))
    elif v == 5:  # Lit Edge: wedge with amber glow strips along both edges + cyan bars (night wayfinding)
        p.add("Ramp", PL, wedge(-W, W)); p.add("Tactile_Bars", CY, *bars(.6))
        p.add("Edge_Glow", A, *[band(s * .69 - .02, s * .69 + .02, -ZH + .02, ZH - .02, .002, .005) for s in (1, -1)])
    return p
ITERS = [(1, "Plain_Wedge"), (2, "Railed"), (3, "Side_Upstands"), (4, "Flared"), (5, "Lit_Edge")]
sf.ASSETS["ramp"] = ("ext_kerb_ramp", ramp, ITERS, 150, "#45 kerb ramp 1.5x3.0, 0.05->0.30 (1:12)")

def fit(v, seed=0):
    from ext_platform_infill_generator import infill
    from ext_tram_platform_kerb_generator import kerb
    from ext_paving_kit_generator import tile
    asm = {}; Rr = np.eye(4); Rr[0, 0] = Rr[2, 2] = -1
    for k, (mk, m) in infill().P.items(): m.apply_translation((15.0, 0, -16.048)); asm["I_" + k] = (mk, m)
    for i, x in enumerate((10, 12)):
        for k, (mk, m) in kerb(2).P.items(): xf(m, R=Rr); m.apply_translation((x, 0, -17.55)); asm[f"K{i}_{k}"] = (mk, m)
    for k, (mk, m) in ramp(v).P.items(): m.apply_translation((9.75, 0, -13.996)); asm["R_" + k] = (mk, m)
    for i, x in enumerate((9.75,)):
        for k, (mk, m) in tile(4, "promenade").P.items(): m.apply_translation((x, 0, -12.496 + .004 + 1.0)); asm[f"P{i}_{k}"] = (mk, m)
    for k, (mk, m) in tile(4, "promenade").P.items(): m.apply_translation((11.506, 0, -14.496)); asm["PS_" + k] = (mk, m)   # beside the ramp
    a = cc.check(asm, seed=seed); return dict(bad=[o for o in a["overlap"] if not o[3]], coplanar=a["coplanar"], open=a["open"])

if __name__ == "__main__":
    import validate_models as vm
    for r, (v, nm) in zip(sf.build("ramp"), ITERS):
        f = [fit(v, s) for s in (0, 1, 2)]
        print("RES", r["cand"], r["tris"], r["budget_ok"], r["clip_pass"], r["worst_overlap"], r["overlaps_over"][:2], r["coplanar"][:2], r["open"][:2], r["size"],
              vm.validate_file(os.path.join(sf.ROOT, r["glb"]), require_textures=False), all(not x["bad"] and not x["coplanar"] and not x["open"] for x in f), [x for x in f if x["bad"] or x["coplanar"] or x["open"]][:1])
