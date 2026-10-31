"""Rook (Oct 30, box pipeline): residential exterior list v1 #41 curb segment (straight 2 m + corner), x68, 2.0 x 0.3 x 0.15, <=120 tris.
Five candidates, each = straight `ext_curb_segment_0N.glb` + matching outside corner `ext_curb_corner_0N.glb` (0.3 x 0.3 x 0.15).
Straight: along X, tiles at a 2.000 m pitch (ends at +/-0.997 -> 6 mm joints); +Z = road face; top y 0.15 above road (y 0), sidewalk side -Z.
Corner: square 0.3 x 0.3 with the rounded outside quadrant at +X/+Z (road side); place where two straights meet (rotate per corner).
Fit: curbs are street edges only; the tram platform uses the promoted #16 kerb (0.30 tall) - curb runs stop 6 mm short of kerb ends.
Aegis-7 (slate/gunmetal/titanium/pearl), amber reflectors, Civic cyan glow, zero wood, wordless. Run: python3 ext_curb_generator.py"""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import ext_street_furniture_generator as sf
from ext_street_furniture_generator import Pod, box, loft, xf, FMAT, _PBR, G, S, T, A, E
FMAT["a7_pearl"] = _PBR(name="A7_PearlAlabaster", baseColorFactor=(0xD8/255, 0xDE/255, 0xE4/255, 1), metallicFactor=0.15, roughnessFactor=0.45)
FMAT["a7_cyan"] = _PBR(name="A7_CivicCyan", baseColorFactor=(0x38/255, 0xB8/255, 0xC8/255, 1), metallicFactor=0.1, roughnessFactor=0.4, emissiveFactor=(.1, .45, .5))
PL, CY = "a7_pearl", "a7_cyan"; L = .997

def prof(pts_zy, x0, x1):  # extrude a convex (z, y) profile along X
    P = np.array(pts_zy, float); c = P.mean(0); m = loft(P - c, [(x0, 1, 1), (x1, 1, 1)])
    V = m.vertices.copy(); m.vertices = np.c_[V[:, 1], V[:, 2] + c[1], V[:, 0] + c[0]]
    if m.volume < 0: m.invert()
    return m
def quad(r, y0, y1, n=6, sq=.3):  # corner plan: square sq x sq centred, outside (+X+Z) corner rounded radius r
    h = sq / 2; pts = [(-h, -h), (h, -h)] + [(h - r + r * np.cos(a), h - r + r * np.sin(a)) for a in np.linspace(0, np.pi / 2, n)] + [(-h, h)]
    P = np.array(pts); m = loft(P, [(y0, 1, 1), (y1, 1, 1)]); return m
CH = [(-.15, 0), (.15, 0), (.15, .11), (.11, .15), (-.15, .15)]                     # chamfered road-top edge
BN = [(-.15, 0), (.15, 0), (.15, .09)] + [(.09 + .06 * np.cos(a), .09 + .06 * np.sin(a)) for a in np.linspace(0, np.pi / 2, 4)][1:] + [(-.15, .15)]  # bullnose

def curb(v):
    p = Pod(f"ext_curb_segment_0{v}")
    if v == 1:  # Chamfer Slate: chamfered carbon-slate curb, amber reflector strip on the road face
        p.add("Curb", S, prof(CH, -L, L)); p.add("Reflector_Strip", A, box(-.9, .9, .05, .08, .15 - E, .154))
    elif v == 2:  # Titanium Nosing: slate body capped with a titanium angle nosing on the road-top edge
        p.add("Curb", S, box(-L, L, 0, .135, -.15, .15)); p.add("Nosing", T, box(-L + .002, L - .002, .135 - E, .15, .09, .154))
        p.add("Top_Cap", S, box(-L + .002, L - .002, .133, .148, -.148, .09 + E))
    elif v == 3:  # Pearl Bullnose: rounded pearl curb on a gunmetal gutter lip
        p.add("Curb", PL, prof(BN, -L, L)); p.add("Gutter_Lip", G, box(-L + .002, L - .002, .002, .03, .15 - E, .2))
    elif v == 4:  # Drain Inlet: gunmetal curb split around a real inlet cut-out with a titanium grate, slate top
        p.add("Curb", G, box(-L, -.25, 0, .12, -.15, .15), box(.25, L, 0, .12, -.15, .15), box(-.25 - E, .25 + E, 0, .12, -.15, .08))
        p.add("Inlet_Grate", T, *[box(x - .015, x + .015, .02, .12, .08 - E, .145) for x in (-.15, 0, .15)])
        p.add("Top_Slab", S, box(-L + .002, L - .002, .12 - E, .15, -.148, .148))
    elif v == 5:  # Lit Edge: carbon-slate curb, Civic cyan glow line in a top groove (real cut-out), amber studs
        p.add("Curb", S, box(-L, L, 0, .12, -.15, .15), box(-L, L, .12 - E, .15, -.15, .07), box(-L, L, .12 - E, .15, .10, .15))
        p.add("Glow_Line", CY, box(-L + .002, L - .002, .118, .142, .07 - E, .10 + E))
        p.add("Reflector_Studs", A, *[box(x - .04, x + .04, .06, .10, .15 - E, .156) for x in (-.5, .5)])
    return p
def corner(v):
    p = Pod(f"ext_curb_corner_0{v}"); mat = {1: S, 2: S, 3: PL, 4: G, 5: S}[v]
    p.add("Curb", mat, quad(.15 if v != 2 else .06, 0, .15 - (.015 if v in (2, 4) else 0)))
    if v == 2: p.add("Top_Cap", T, quad(.06, .135 - E, .15, sq=.296))
    if v == 4: p.add("Top_Slab", S, quad(.15, .135 - E, .15, sq=.296))
    if v == 1:  # amber reflector wraps the curved road face: one thin box per arc chord, 4 mm proud (embedded E)
        P = [(np.cos(t) * .15, np.sin(t) * .15) for t in np.linspace(0, np.pi / 2, 4)]; segs = []
        for (x0, z0), (x1, z1) in zip(P[:-1], P[1:]):
            mx, mz = (x0 + x1) / 2, (z0 + z1) / 2; L2 = np.hypot(x1 - x0, z1 - z0) / 2 - .001; nx, nz = mx / np.hypot(mx, mz), mz / np.hypot(mx, mz)
            d = np.hypot(mx, mz); m = box(-L2, L2, .05, .08, -E, .004); ang = np.arctan2(nx, nz)
            R = np.eye(4); R[:3, :3] = [[np.cos(ang), 0, np.sin(ang)], [0, 1, 0], [-np.sin(ang), 0, np.cos(ang)]]
            xf(m, R=R); m.apply_translation((nx * d, 0, nz * d)); segs.append(m)
        p.add("Reflector_Strip", A, *segs)
        p.add("Reflector_Ends", A, box(-.149, -.004, .05, .08, .15 - E, .154), box(.15 - E, .154, .05, .08, -.149, -.004))
    if v == 5: p.add("Glow_Cap", CY, quad(.15, .15 - E, .154, sq=.2))
    return p
ITERS = [(1, "Chamfer_Slate"), (2, "Titanium_Nosing"), (3, "Pearl_Bullnose"), (4, "Drain_Inlet"), (5, "Lit_Edge")]
sf.ASSETS["curb"] = ("ext_curb_segment", curb, ITERS, 120, "#41 curb straight 2.0x0.3x0.15 (tiles @2.0 m, +Z road)")
sf.ASSETS["curb_corner"] = ("ext_curb_corner", corner, ITERS, 120, "#41 curb outside corner 0.3x0.3x0.15")
if __name__ == "__main__":
    import validate_models as vm
    for k in ("curb", "curb_corner"):
        for r in sf.build(k): print(r["cand"], "validate", vm.validate_file(os.path.join(sf.ROOT, r["glb"]), require_textures=False))
