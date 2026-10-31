"""Rook (Oct 31, box pipeline): residential exterior list v1 #46 canal edge module (railing + coping), x47, 2.0 x 0.4 x 1.1, <=300 tris.
Five candidates -> design/assets/ext_canal_edge/ext_canal_edge_01..05.glb + contact sheet.
Runs along X (axial, straight - the canal edge Z -26 is axial, no bend). Ends at x +/-0.997 -> 6 mm joints, 2.0 m pitch; all posts at x +/-0.5
so post spacing stays 1.0 m across joints. +Z = water side (coping drip lip). Coping top y 0.15 = 0.10 above the promenade paving top (0.05);
railing top y 1.10. Placement: rotate 180 (water at world -Z), origin Z -25.8 -> coping Z -26.0..-25.6; kerb-walk paving stops at Z -25.596 (4 mm).
Aegis-7 + pearl/cyan, amber, BLEND glass, zero wood, wordless. Run: python3 ext_canal_edge_generator.py"""
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import ext_street_furniture_generator as sf
from ext_street_furniture_generator import Pod, box, cyl, FMAT, G, S, T, A, GL, E, xf
from ext_road_curved_generator import PL, CY
import ext_clip_check as cc
L = .997
def coping(p, mat, lip=G):
    p.add("Coping", mat, box(-L, L, 0, .15, -.2, .16))
    p.add("Drip_Lip", lip, box(-L + .002, L - .002, .06, .15 - .003, .16 - E, .2))
def seg(y0, y1, z0, z1, pw=.03):  # rail run split at the posts (x +/-0.5), ends embedded E
    xs = [(-L + .002, -.5 - pw + E), (-.5 + pw - E, .5 - pw + E), (.5 + pw - E, L - .002)]
    return [box(a, b, y0, y1, z0, z1) for a, b in xs]
def canal(v):
    p = Pod(f"ext_canal_edge_0{v}")
    if v == 1:  # Glass Balustrade: slate coping, gunmetal base channel, BLEND glass panel, titanium top rail
        coping(p, S)
        p.add("Base_Channel", G, box(-L + .002, L - .002, .15 - E, .22, -.04, .04))
        p.add("Glass_Panel", GL, box(-L + .004, L - .004, .22 - E, 1.03 + E, -.008, .008))
        p.add("Top_Rail", T, box(-L + .002, L - .002, 1.03, 1.10, -.03, .03))
    elif v == 2:  # Titanium Post Rail: pearl coping, two titanium posts per module, top rail + two mid rails
        coping(p, PL, S)
        p.add("Posts", T, *[box(x - .03, x + .03, .15 - E, 1.06 + E, -.03, .03) for x in (-.5, .5)])
        p.add("Top_Rail", T, box(-L + .002, L - .002, 1.06, 1.10, -.04, .04))
        p.add("Mid_Rails", T, *[m for y in (.45, .75) for m in seg(y, y + .03, -.02, .02)])
    elif v == 3:  # Cable Rail: gunmetal posts, three thin titanium cables, amber post caps, slate coping
        coping(p, S)
        p.add("Posts", G, *[box(x - .03, x + .03, .15 - E, 1.05 + E, -.03, .03) for x in (-.5, .5)])
        p.add("Cables", T, *[m for y in (.35, .6, .85) for m in seg(y, y + .008, -.004, .004)])
        p.add("Top_Rail", G, box(-L + .002, L - .002, 1.05, 1.08, -.035, .035))
        p.add("Post_Caps", A, *[box(x - .03, x + .03, 1.08 - E, 1.10, -.03, .03) for x in (-.5, .5)])
    elif v == 4:  # Slatted Panel: gunmetal vertical slats (real openings between), pearl top rail, slate coping, cyan base line
        coping(p, S)
        p.add("Base_Rail", G, box(-L + .002, L - .002, .15 - E, .22, -.03, .03))
        p.add("Slats", G, *[box(x - .02, x + .02, .22 - E, 1.04 + E, -.015, .015) for x in np.arange(-.875, .9, .25)])
        p.add("Top_Rail", PL, box(-L + .002, L - .002, 1.04, 1.10, -.04, .04))
        p.add("Base_Line", CY, box(-L + .004, L - .004, .17, .19, .03 - E, .034))
    elif v == 5:  # Lit Coping: pearl coping with cyan glow under the water lip, glass panel, amber glow handrail
        coping(p, PL, S)
        p.add("Water_Glow", CY, box(-L + .004, L - .004, .06 - .012, .06 + E, .17, .195))
        p.add("Base_Channel", G, box(-L + .002, L - .002, .15 - E, .22, -.04, .04))
        p.add("Glass_Panel", GL, box(-L + .004, L - .004, .22 - E, 1.0 + E, -.008, .008))
        p.add("Handrail", T, box(-L + .002, L - .002, 1.0, 1.06, -.03, .03))
        p.add("Rail_Glow", A, box(-L + .004, L - .004, 1.06 - E, 1.10, -.015, .015))
    return p
ITERS = [(1, "Glass_Balustrade"), (2, "Titanium_Post_Rail"), (3, "Cable_Rail"), (4, "Slatted_Panel"), (5, "Lit_Coping")]
sf.ASSETS["canal"] = ("ext_canal_edge", canal, ITERS, 300, "#46 canal edge 2.0x0.4x1.1 (tiles @2.0 m, +Z water)")

def fit(v, seed=0):
    from ext_paving_kit_generator import tile
    asm = {}
    for i, x in enumerate((-1.0, 1.0)):
        for k, (mk, m) in canal(v).P.items(): m.apply_translation((x, 0, 0)); asm[f"E{i}_{k}"] = (mk, m)
    for i, x in enumerate((-1.0, 1.0)):
        for k, (mk, m) in tile(4, "promenade").P.items(): m.apply_translation((x, 0, -.2 - .004 - 1.0)); asm[f"P{i}_{k}"] = (mk, m)
    a = cc.check(asm, seed=seed); return dict(bad=[o for o in a["overlap"] if not o[3]], coplanar=a["coplanar"], open=a["open"])

if __name__ == "__main__":
    import validate_models as vm
    for r, (v, nm) in zip(sf.build("canal"), ITERS):
        f = [fit(v, s) for s in (0, 1, 2)]
        print("RES", r["cand"], r["tris"], r["budget_ok"], r["clip_pass"], r["worst_overlap"], r["overlaps_over"][:2], r["coplanar"][:2], r["size"],
              vm.validate_file(os.path.join(sf.ROOT, r["glb"]), require_textures=False, require_blend_glass=v in (1, 5)), all(not x["bad"] and not x["coplanar"] and not x["open"] for x in f), [x for x in f if x["bad"] or x["coplanar"]][:1])
