"""Rook (Oct 30, box pipeline): residential exterior list v1 #42 curved road segment, bent to the walking floor R 185.5 m along Z (Spin Sts W/E), x34.
5.0 W (X) x 6.0 L (Z, arc length) x 0.05 slab, <=200 tris. Five candidates -> design/assets/ext_road_curved_R185/ext_road_curved_R185_01..05.glb.
Curvature: the spin axis is above (+Y); a point at arc length z and height h maps to (x, R-(R-h)cos(z/R), (R-h)sin(z/R)) -> ends rise 24 mm.
Tiling: segment ends are radial planes at arc +/-2.997 (6 mm joints); place consecutive segments rotated 1.8532 deg (6.0/185.5 rad) about X
around the spin axis (pivot = bottom-centre at arc 0). Width ends at x +/-2.497 (6 mm to neighbours/kerb-ramp aprons).
Curb fit (#41 ext_curb_segment, 2.0 straight): curbs sit on the road edges at road top y 0.05, chamfered face toward the road; on R 185.5 a 2 m chord
sags 2.7 mm and adjacent curbs rotate 0.62 deg -> 6 mm joints open < 2 mm at the top, so straight curbs follow the curve.
Decals are thin pieces floating 2-4 mm above the surface (no coplanar, no overlap). Aegis-7, amber/cyan, zero wood, wordless."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
import ext_street_furniture_generator as sf
from ext_street_furniture_generator import Pod, FMAT, _PBR, G, S, T, A, E
FMAT["a7_pearl"] = _PBR(name="A7_PearlAlabaster", baseColorFactor=(0xD8/255, 0xDE/255, 0xE4/255, 1), metallicFactor=0.15, roughnessFactor=0.45)
FMAT["a7_cyan"] = _PBR(name="A7_CivicCyan", baseColorFactor=(0x38/255, 0xB8/255, 0xC8/255, 1), metallicFactor=0.1, roughnessFactor=0.4, emissiveFactor=(.1, .45, .5))
PL, CY = "a7_pearl", "a7_cyan"; R = 185.5; ZL, XW, TH = 2.997, 2.497, .05

def bend(prof, z0, z1, n):  # prof = convex list of (x, h) CCW in x-h; extrude along arc z0..z1 with n segments
    P = np.array(prof, float); k = len(P); V = []; UV = []
    for z in np.linspace(z0, z1, n + 1):
        a = z / R
        for x, h in P: V.append((x, R - (R - h) * np.cos(a), (R - h) * np.sin(a))); UV.append((x / 5 + .5, z / 6))
    F = []
    for i in range(n):
        for j in range(k):
            a0, b0 = i * k + j, i * k + (j + 1) % k; a1, b1 = a0 + k, b0 + k; F += [(a0, b0, a1), (b0, b1, a1)]
    for ring, flip in ((0, False), (n, True)):
        c = len(V); V.append(tuple(np.mean(V[ring * k:(ring + 1) * k], 0))); UV.append((.5, .5))
        for j in range(k):
            a, b = ring * k + j, ring * k + (j + 1) % k; F.append((c, a, b) if not flip else (c, b, a))
    m = trimesh.Trimesh(np.array(V), np.array(F), process=False)
    if m.volume < 0: m.invert()
    m.metadata["uv"] = np.array(UV); return m
def rect(x0, x1, h0, h1): return [(x0, h0), (x1, h0), (x1, h1), (x0, h1)]
def dec(x0, x1, z0, z1, h, n=1, t=.002): return bend(rect(x0, x1, h + .002, h + .002 + t), z0, z1, n)  # floating decal 2 mm above surface

def road(v):
    p = Pod(f"ext_road_curved_R185_0{v}"); N = 6
    if v == 1:  # Slate Carriageway: carbon-slate slab, amber centre dashes, pearl edge lines
        p.add("Road", S, bend(rect(-XW, XW, 0, TH), -ZL, ZL, N))
        p.add("Centre_Dashes", A, dec(-.06, .06, -2.5, -1.0, TH), dec(-.06, .06, .5, 2.0, TH))
        p.add("Edge_Lines", PL, *[dec(s * 2.2 - .05, s * 2.2 + .05, -ZL + .01, ZL - .01, TH, N) for s in (1, -1)])
    elif v == 2:  # Pearl Pavers + Gutters: pearl carriageway with real gunmetal gutter channels cut along both edges
        p.add("Road", PL, bend(rect(-2.2, 2.2, 0, TH), -ZL, ZL, N))
        p.add("Gutters", G, *[bend(rect(*sorted((s * (2.2 - E), s * XW)), .002, TH - .015), -ZL + .002, ZL - .002, N) for s in (1, -1)])
        p.add("Centre_Dashes", A, dec(-.05, .05, -2.0, -.5, TH), dec(-.05, .05, 1.0, 2.5, TH))
    elif v == 3:  # Cart Track: slate slab with two titanium wear strips for service carts / Sprocket, amber edge ticks
        p.add("Road", S, bend(rect(-XW, XW, 0, TH), -ZL, ZL, N))
        p.add("Wear_Strips", T, *[dec(x - .15, x + .15, -ZL + .01, ZL - .01, TH, N) for x in (-.8, .8)])
        p.add("Edge_Ticks", A, *[dec(s * 2.3 - .05, s * 2.3 + .05, z - .3, z + .3, TH) for s, z in ((1, -1.5), (-1, 1.5))])
    elif v == 4:  # Shared Street Crossing: pearl slab with wordless cyan crossing bands at the +Z end, gunmetal edge bands
        p.add("Road", PL, bend(rect(-XW, XW, 0, TH), -ZL, ZL, N))
        p.add("Crossing_Bands", CY, *[dec(x - .25, x + .25, 1.6, 2.8, TH) for x in (-1.8, -.6, .6, 1.8)])
        p.add("Edge_Bands", G, *[dec(s * 2.3 - .1, s * 2.3 + .1, -ZL + .01, 1.4, TH, 4) for s in (1, -1)])
    elif v == 5:  # Drain Crown: crowned slate road (centre +20 mm, falls to the edges), amber edge reflector lines
        p.add("Road", S, bend([(-XW, 0), (XW, 0), (XW, TH), (0, TH + .02), (-XW, TH)], -ZL, ZL, N))
        p.add("Edge_Lines", A, *[dec(s * 2.3 - .04, s * 2.3 + .04, -ZL + .01, ZL - .01, .0519, N) for s in (1, -1)])
    return p
ITERS = [(1, "Slate_Carriageway"), (2, "Pearl_Pavers_Gutters"), (3, "Cart_Track"), (4, "Shared_Street_Crossing"), (5, "Drain_Crown")]
sf.ASSETS["road"] = ("ext_road_curved_R185", road, ITERS, 200, "#42 curved road 5.0x6.0 on R 185.5 (tiles 1.853 deg)")
if __name__ == "__main__":
    import validate_models as vm
    for r in sf.build("road"): print(r["cand"], "validate", vm.validate_file(os.path.join(sf.ROOT, r["glb"]), require_textures=False))
