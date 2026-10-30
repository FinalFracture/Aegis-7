"""Rook (Oct 30, Jared 12:58 PM CT): memorial round with a scaled-down Aegis-7 habitat -> ext_memorial_aegis_01..05 (all prior memorial files kept).
REFERENCE (silhouette + proportions):
  - PROJECT.md line 4: rotating O'Neill cylinder, 800 m long x 400 m diameter (2:1 overall).
  - design/cylinder_interior_overhaul_spec.md S3/S4: 520 m rotating habitat drum (R = 200 m) with a forward hemispherical endcap / axial
    docking bowl; a heavy 45-deg chamfered gunmetal baffle bulkhead aft; behind it the counter-rotating 280 m aft zero-G starport and
    5-coil fusion drive (docking collar R 45..75 m); three 120-deg valleys alternating with solarium window strips.
  Scale model: overall length L, drum 520/800 L (incl. forward dome), starport spine 280/800 L at R_spine = 45/200 R with a collar at 75/200 R,
  5 amber fusion coils at the aft end; 12-sided drum, 3 BLEND solarium strips (2 faces each) alternating with 3 titanium land strips.
Nook (plan v1.3, Vance): <= 3.9 W x 1.6 D x 4.3 H, centred X 19.5, back at Z -9.7, rotated 180 deg.
Run: python3 ext_memorial_aegis_generator.py"""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
import ext_street_furniture_generator as sf
import ext_memorial_hydro_generator as mh
from ext_street_furniture_generator import G, S, T, A, GL, E, ring, box, blk, Pod, loft, xf
from ext_memorial_monument_generator import tag_row, torus
V, VM = mh.V, mh.VM
N = 12; HALF = np.pi / N

def xprism(R, rings, cy, n=N, phase=HALF, z0=0.0):
    """n-gon solid along X: rings = [(x, scale)], vertex angle theta from +Y toward +Z, flat faces centred at k*2pi/n (phase=pi/n)."""
    th = phase + 2 * np.pi * np.arange(n) / n; Vt = []; UV = []
    for x, s in rings:
        for t in th: Vt.append((x, cy + R * s * np.cos(t), z0 + R * s * np.sin(t))); UV.append((t / (2 * np.pi), x))
    F = []
    for i in range(len(rings) - 1):
        for j in range(n):
            a, b = i * n + j, i * n + (j + 1) % n; F += [(a, b, a + n), (b, b + n, a + n)]
    for ri, flip in ((0, True), (len(rings) - 1, False)):
        c = len(Vt); Vt.append((rings[ri][0], cy, z0)); UV.append((.5, rings[ri][0]))
        for j in range(n):
            a, b = ri * n + j, ri * n + (j + 1) % n; F.append((c, a, b) if flip else (c, b, a))
    m = trimesh.Trimesh(np.array(Vt), np.array(F), process=False)
    if m.volume < 0: m.invert()
    m.metadata["uv"] = np.array(UV); return m
def panel(x0, x1, a, t, w, phi, cy, z0=0.0):  # flat hull panel on the drum face centred at angle phi (from +Y toward +Z)
    m = box(x0, x1, a - E, a + t, -w / 2, w / 2); uv = m.metadata["uv"]
    m.apply_transform(trimesh.transformations.rotation_matrix(phi, (1, 0, 0))); m.apply_translation((0, cy, z0)); m.metadata["uv"] = uv; return m

def aegis(p, L, cy, xc=0.0, cut=False):
    """Scaled Aegis-7. Returns (R, x_drum0, x_drum1, belly_y). Forward = -X."""
    s = L / 800.; R = 200 * s; Ld = 520 * s; Ls = 280 * s; xa = xc - L / 2; xb = xa + Ld; dome = .25 * R
    a_core = R * .94 * np.cos(HALF); t = R * .06; fw = 2 * R * np.sin(HALF) * .94 - .01   # panel width leaves a gap: no shared edges
    def xs(v): return v
    if not cut:
        p.add("Drum_Core", S, xprism(R * .94, [(xa + dome, 1), (xb - .02 * L, 1)], cy))
        p.add("Fwd_Endcap_Dome", T, xprism(R * .94, [(xa + dome + E, 1), (xa + dome * .5, .8), (xa, .25)], cy))
    else:  # cutaway: open drum, bulkhead discs, land strips inside, axial sun spine
        p.add("Fwd_Endcap_Dome", T, xprism(R * .94, [(xa + dome + E, 1), (xa + dome * .5, .8), (xa, .25)], cy))
        p.add("Bulkhead_Discs", G, xprism(R * .94, [(xa + dome, 1), (xa + dome + .03 + E, 1)], cy), xprism(R * .94, [(xb - .02 * L - .03 - E, 1), (xb - .02 * L, 1)], cy))
        p.add("Axial_Sun_Spine", A, xprism(R * .06, [(xa + dome + .03 - E, 1), (xb - .02 * L - .03 + E, 1)], cy, 8, np.pi / 8))
    gl, ti = [], []
    for k in range(N):
        phi = 2 * np.pi * k / N
        if cut and k in (2, 3, 4): continue  # front-upper 90 deg removed to show the spinning interior
        x0, x1 = (xa + dome + (.03 if cut else 0), xb - .02 * L - (.03 if cut else 0))
        (gl if k % 4 < 2 else ti).append(panel(x0 + .012, x1 - .012, a_core, t, fw, phi, cy))
    p.add("Drum_Solarium_Glass", GL, *gl); p.add("Drum_Hull_Strips", T, *ti)
    if cut:
        land = [panel(xa + dome + .03 + .004, xb - .02 * L - .03 - .004, a_core - .05, .02, fw * .98, 2 * np.pi * k / N, cy) for k in range(N) if k not in (2, 3, 4) and k % 4 >= 2]
        for m in land:  # land strips sit on stand-offs from the hull panels: lift inward so they float clear, joined by ribs
            pass
        p.add("Valley_Land", "leaf", *[panel(xa + dome + .06, xb - .02 * L - .06, a_core - t * 1.2, t * .6, fw * .8, 2 * np.pi * k / N, cy) for k in range(N) if k not in (2, 3, 4) and k % 4 >= 2])
        p.add("Valley_Ribs", G, *[panel(xx - .01, xx + .01, a_core - t * .6 - E, t * .6 + E, fw * .3, 2 * np.pi * k / N, cy) for k in range(N) if k not in (2, 3, 4) and k % 4 >= 2 for xx in (xa + dome + .3, xb - .02 * L - .3)])
    # aft chamfered baffle bulkhead (45 deg) + starport spine with collar and 5 fusion coils
    p.add("Aft_Baffle_Bulkhead", G, xprism(R * .94, [(xb - .02 * L - E, 1.0), (xb + .08 * L, .45)], cy))
    rs = 45 * s; rc = 75 * s; x = xb + .08 * L - E; xe = xa + L
    seg = []; coils = []; xs_c = np.linspace(xe - .25 * Ls, xe - .02, 5); cw = .012 * L
    p.add("Docking_Collar", G, xprism(rc, [(x + .1 * Ls, 1), (x + .1 * Ls + .03 * L, 1)], cy, 10, np.pi / 10))
    pts = [x] + [v for c in xs_c for v in (c - cw / 2, c + cw / 2)] + [xe]
    spine = [(x, x + .1 * Ls + E)] + [(x + .1 * Ls + .03 * L - E, xs_c[0] - cw / 2 + E)] + [(xs_c[i] + cw / 2 - E, xs_c[i + 1] - cw / 2 + E) for i in range(4)]
    p.add("Starport_Spine", T, *[xprism(rs, [(u0, 1), (u1, 1)], cy, 8, np.pi / 8) for u0, u1 in spine])
    p.add("Fusion_Coils", A, *[xprism(rs * 1.9, [(c - cw / 2, 1), (c + cw / 2, 1)], cy, 10, np.pi / 10) for c in xs_c])
    return R, xa + dome, xb, cy - R * .94 * np.cos(HALF) - t * 0  # belly = core flat-face bottom (panel outer = +t)

def saddle(p, x, ytop, R, cy, w=.12, d=.5):  # saddle under the ship's flat belly hull strip (embed E into the panel)
    yb = cy - (R * .94 * np.cos(HALF) + R * .06) + E
    return box(x - w / 2, x + w / 2, ytop, yb, -d / 2, d / 2)

LEDGES = {}
def mem(v):
    p = Pod(f"ext_memorial_aegis_0{v}"); rng = np.random.default_rng(1258 + v)
    if v == 1:  # Held aloft on a titanium stele: stele + fork yoke, ship 2.6 m long at ~3.4 m axis
        L = 2.6; R = 200 * L / 800; cy = 4.3 - R - .02
        p.add("Plinth", S, box(-1.6, 1.6, 0, .35, -.6, .6)); p.add("Plinth_Seam", V, box(-1.55, 1.55, .3, .34, .6 - E, .606))
        yb = cy - (R * .94 * np.cos(HALF) + R * .06) + E
        p.add("Stele", T, loft(np.array([(.22, .14), (-.22, .14), (-.22, -.14), (.22, -.14)]), [(.35 - E, 1, 1), (yb - .12, .6, .6)]))
        p.add("Yoke", G, box(-.75, .75, yb - .12 - E, yb - .06, -.12, .12), *[box(x - .05, x + .05, yb - .06 - E, yb, -.2, .2) for x in (-.6, .6)])
        aegis(p, L, cy)
        LEDGES[v] = "plinth top 3.2 x 1.2 at y 0.35 either side of the stele (x +-0.35..1.6): lamp at x +1.2, z +0.3; offering at x -1.0, z +0.3"
    elif v == 2:  # Ring frame cradle with RFID tags hanging beneath the ship
        Rr = 1.75; cyr = .3 + .1 + Rr - E; L = 2.4; R = 200 * L / 800; cy = cyr + .15
        p.add("Base", S, box(-1.7, 1.7, 0, .3, -.7, .7))
        p.add("Halo_Ring", T, torus(Rr, .1, 64, 8, cyr))
        yb = cy - (R * .94 * np.cos(HALF) + R * .06) + E
        for x in (-.7, .7):  # struts from the ring's lower arc up to the belly saddles
            yr = cyr - np.sqrt(Rr ** 2 - x ** 2) + .1 + .012
            p.add("Cradle_Struts", G, box(x - .025, x + .025, yr, yb - .05 + E, -.025, .025)); p.add("Saddles", G, box(x - .07, x + .07, yb - .05, yb, -.2, .2))
        aegis(p, L, cy)
        p.add("Tag_Beam", G, box(-.66, .66, yb - .3, yb - .26, -.03, .03)) if False else None
        p.add("Tag_Beam", G, box(-.66 - E + .04, .66 + E - .04, yb - .3, yb - .26, -.03, .03))
        for z in (-.0,):
            tag_row(p, -.6, .6, yb - .3 - .005, .036, rng, .07)
        p.add("Tag_Hangers", T, *[ring(.004, yb - .3 - .005 - .004, yb - .3 + E, 6, x=x, z=.036) for x in (-.62, .62)]) if False else None
        LEDGES[v] = "base 3.4 x 1.4 at y 0.30, front strip z +0.2..+0.7 outside the ring tube: lamp at x +1.3, offering at x -1.25"
    elif v == 3:  # Tiered plinth with violet light seams, ship on two saddles
        tiers = [(3.6, 1.5, 0, .3), (2.9, 1.2, .33, .63), (2.2, .9, .66, .96)]
        for k, (w, d, y0, y1) in enumerate(tiers):
            p.add("Tiers", S if k != 1 else G, box(-w / 2, w / 2, y0 - (E if k else 0), y1, -d / 2, d / 2))
            if k < 2:
                nw, nd, ny0 = tiers[k + 1][:2] + (tiers[k + 1][2],); p.add("Light_Seams", V, box(-nw / 2 - .03, nw / 2 + .03, y1 - E, ny0, -nd / 2 - .03, nd / 2 + .03))
        L = 3.0; R = 200 * L / 800; cy = .96 + .25 + R
        yb = cy - (R * .94 * np.cos(HALF) + R * .06) + E
        p.add("Saddles", T, *[box(x - .08, x + .08, .96 - E, yb, -.25, .25) for x in (-.7, .6)])
        aegis(p, L, cy)
        LEDGES[v] = "tier-1 side ledges y 0.30 (x +-1.45..1.8, 1.5 deep) and front strip z +0.6..+0.75: lamp on the left ledge x -1.62, z +0.3; offering on the right ledge turned 90 deg x +1.62"
    elif v == 4:  # Cutaway: open front-upper quarter shows bulkheads, green valley strips and the axial sun spine
        p.add("Plinth", S, box(-1.7, 1.7, 0, .7, -.7, .7)); p.add("Plinth_Seam", A, box(-1.65, 1.65, .62, .66, .7 - E, .706))
        L = 3.2; R = 200 * L / 800; cy = .7 + .2 + R
        yb = cy - (R * .94 * np.cos(HALF) + R * .06) + E
        p.add("Saddles", G, *[box(x - .08, x + .08, .7 - E, yb, -.25, .25) for x in (-.8, .5)])
        aegis(p, L, cy, cut=True)
        LEDGES[v] = "plinth top 3.4 x 1.4 at y 0.70 outside the saddles; front strip z +0.3..+0.7 under the ship's open side: lamp at x +1.45, offering at x -1.2 (z +0.45)"
    elif v == 5:  # Ship mounted on a titanium beam over a tag curtain
        p.add("Floor_Plate", S, box(-1.9, 1.9, 0, .06, -.6, .6))
        p.add("Posts", T, *[box(s_ * 1.75 - .07, s_ * 1.75 + .07, .06 - E, 2.75 + E, -.07, .07) for s_ in (-1, 1)])
        p.add("Beam", G, box(-1.9, 1.9, 2.75, 2.9, -.12, .12)); p.add("Beam_Light", V, box(-1.6, 1.6, 2.73, 2.75 + E, -.06, .06))
        L = 2.6; R = 200 * L / 800; cy = 2.9 + .1 + R
        yb = cy - (R * .94 * np.cos(HALF) + R * .06) + E
        p.add("Saddles", T, *[box(x - .07, x + .07, 2.9 - E, yb, -.2, .2) for x in (-.7, .6)])
        aegis(p, L, cy)
        for x in np.linspace(-1.5, 1.5, 11):
            for z in (-.15, .15):
                Lc = 2.0 - 1.0 * abs(x) / 1.5 + rng.uniform(-.08, .08); ybot = 2.73 - Lc
                p.add("Cables", T, ring(.003, ybot, 2.73 + E, 4, x=x, z=z))
                for y in np.arange(2.65, ybot + .04, -.13):
                    m = VM if rng.random() < .3 else T; p.add("Tags_Violet" if m == VM else "Tags_Ti", m, box(x - .016, x + .016, y - .055, y, z + .0025, z + .0055))
        LEDGES[v] = "floor plate 3.8 x 1.2 at y 0.06; outer cables stop at y ~1.9 so the ends are clear: lamp at x -1.45, offering at x +1.2 (z +0.3)"
    return p
MEM = [(1, "Stele_Aloft"), (2, "Ring_Cradle_Tags"), (3, "Tiered_Plinth_Seams"), (4, "Spinning_Cutaway"), (5, "Over_Tag_Curtain")]
sf.ASSETS["aegis"] = ("ext_memorial_aegis", mem, MEM, 6000, "#29 memorial with scaled Aegis-7 (nook v1.3: <=3.9 W x 1.6 D x 4.3 H)")
if __name__ == "__main__":
    sf.build("aegis"); [print("LEDGE", k, v) for k, v in sorted(LEDGES.items())]
