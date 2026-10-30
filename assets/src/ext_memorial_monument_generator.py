"""Rook (Oct 30, 12:41 PM CT brief): #29 memorial made monumental -> ext_memorial_monument_01..05 (old ext_memorial_tag_rack files kept).
~3-4 m wide x 3-4.5 m tall, <=~6,000 tris, Aegis-7 palette, zero wood, wordless. Each leaves a ledge / floor pad for the
#30 violet field lamp (0.3x0.3x1.2) and #31 offering set (0.6x0.3x0.3); see LEDGES. Same build/check pattern as
ext_street_furniture_generator.py. Tags are 16-tri boxes (cheap; can be MultiMesh-instanced in Godot).
Run: python3 ext_memorial_monument_generator.py"""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
import ext_street_furniture_generator as sf
import ext_memorial_hydro_generator as mh  # registers violet materials
from ext_street_furniture_generator import G, S, T, A, GL, E, ring, box, blk, Pod, loft, xf
from folding_counter_generator import xcyl
from dining_chair_generator import circle
V, VM = mh.V, mh.VM

def tag_row(p, x0, x1, y, z, rng, pitch=.1, r=.005):
    p.add("Tag_Rails", T, xcyl(x0 - E, x1 + E, y, z, r, 6)); n = 0
    xs = np.arange(x0 + .06, x1 - .05, pitch)
    for x in xs + rng.uniform(-.012, .012, len(xs)):
        h = rng.uniform(.05, .08); mat = VM if rng.random() < .3 else T
        p.add("Tags_Violet" if mat == VM else "Tags_Ti", mat, box(x - .018, x + .018, y - h, y + r * .4, z - .0015, z + .0015)); n += 1
    return n
def torus(R, r, maj, mnr, cy):  # trimesh torus lies in XY with axis Z: a vertical ring facing +Z
    m = trimesh.creation.torus(major_radius=R, minor_radius=r, major_sections=maj, minor_sections=mnr)
    m.apply_translation((0, cy, 0)); m.metadata["uv"] = np.c_[np.arctan2(m.vertices[:, 1] - cy, m.vertices[:, 0]) / (2 * np.pi), m.vertices[:, 2]]; return m
def rotz(m, a, t):
    uv = m.metadata["uv"]; m.apply_transform(trimesh.transformations.rotation_matrix(a, (0, 0, 1))); m.apply_translation(t); m.metadata["uv"] = uv; return m

LEDGES = {}
def monument(v):
    p = Pod(f"ext_memorial_monument_0{v}"); rng = np.random.default_rng(290 + v)
    if v == 1:  # Titanium Stele Wall: ~260 hanging RFID tags on 8 rails between gunmetal side fins
        p.add("Plinth", S, box(-1.9, 1.9, 0, .3, -.5, .5))
        p.add("Stele", T, box(-1.75, 1.75, .3 - E, 3.7, -.48, -.25))
        p.add("Lintel", G, box(-1.85, 1.85, 3.7 - E, 3.9, -.49, -.18))
        p.add("Side_Fins", G, box(-1.87, -1.75 + E, .3 - E, 3.7 + E, -.47, -.1), box(1.75 - E, 1.87, .3 - E, 3.7 + E, -.47, -.1))
        for y in np.linspace(1.0, 3.45, 8): tag_row(p, -1.75, 1.75, y, -.17, rng, .105)
        p.add("Violet_Plinth_Seam", V, box(-1.85, 1.85, .25, .29, .5 - E, .506))
        LEDGES[v] = "plinth front ledge 3.8 x 0.6 m at y 0.30 (z -0.10..+0.50; lowest tags end ~y 0.92): lamp at x +1.5, offering at x -0.6"
    elif v == 2:  # Tiered Plinth + tapered titanium obelisk, violet light seams between tiers
        tiers = [(3.6, 1.6, 0, .32), (2.7, 1.2, .35, .67), (1.8, .8, .7, 1.02)]
        for k, (w, d, y0, y1) in enumerate(tiers):
            p.add("Tiers", S if k != 1 else G, box(-w / 2, w / 2, y0 - (E if k else 0), y1, -d / 2, d / 2))
            if k < 2:
                nw, nd, ny0 = tiers[k + 1][0], tiers[k + 1][1], tiers[k + 1][2]
                p.add("Light_Seams", V, box(-nw / 2 - .03, nw / 2 + .03, y1 - E, ny0, -nd / 2 - .03, nd / 2 + .03))
        p.add("Collar", G, box(-.36, .36, 1.02 - E, 1.12, -.36, .36))
        p.add("Obelisk", T, loft(np.array([(.28, .28), (-.28, .28), (-.28, -.28), (.28, -.28)]), [(1.12 - E, 1, 1), (3.9, .55, .55), (4.3, .02, .02)]))
        for sx in (-1, 1):  # corner pylons on tier 1 (back corners), violet caps
            p.add("Pylons", T, box(sx * 1.62 - .08, sx * 1.62 + .08, .32 - E, 2.4, -.72, -.56)); p.add("Pylon_Caps", V, box(sx * 1.62 - .09, sx * 1.62 + .09, 2.4 - E, 2.46, -.73, -.55))
        p.add("Tag_Brackets", G, box(-1.32, -1.25 + E, .67 - E, 1.0, .6 - E, .66), box(1.25 - E, 1.32, .67 - E, 1.0, .6 - E, .66))
        tag_row(p, -1.25, 1.25, .95, .64, rng, .09)
        LEDGES[v] = "tier-1 side ledges y 0.32, 0.45 x 1.6 m each (x +-1.35..1.8; pylons only at the back corners z < -0.55): lamp on the left ledge at x -1.57, z +0.3; offering on the right ledge turned 90 deg at x +1.57, z +0.15 (front strips are only 0.2 m deep)"
    elif v == 3:  # Halo Ring: 3.4 m titanium ring (echoes the cylinder) on a slate cradle, violet inner halo, tag strands
        R = 1.7; cy = .45 + R
        p.add("Base", S, box(-1.6, 1.6, 0, .2, -.6, .6)); p.add("Cradle", G, box(-.55, .55, .2 - E, .45 - .12 + .007, -.2, .2))
        p.add("Halo_Ring", T, torus(R, .12, 64, 8, cy)); p.add("Inner_Halo", V, torus(R - .3, .04, 64, 6, cy))
        p.add("Spokes", G, *[rotz(box(R - .3 + .03, R - .12 + .004, -.008, .008, -.03, .03), a, (0, cy, 0)) for a in np.radians(np.arange(0, 360, 30) + 15)])
        for x in np.linspace(-.9, .9, 7):
            ytop = cy + np.sqrt((R - .34) ** 2 - x ** 2) + .004; ybot = ytop - (1.25 - .5 * abs(x))
            p.add("Strands", T, ring(.004, ybot, ytop, 6, x=x))
            for y in np.arange(ytop - .1, ybot + .05, -.11):
                m = VM if rng.random() < .3 else T; p.add("Tags_Violet" if m == VM else "Tags_Ti", m, box(x - .018, x + .018, y - .06, y, -.0015, .0015))
        LEDGES[v] = "base plinth 3.2 x 1.2 at y 0.20, clear front strips z +0.25..+0.6 either side of the cradle: lamp at x +1.2, offering at x -1.1"
    elif v == 4:  # Tag Curtain: gunmetal canopy on two titanium posts; cascading cables strung with tags
        p.add("Floor_Plate", S, box(-1.9, 1.9, 0, .06, -.6, .6))
        p.add("Posts", T, *[box(s * 1.75 - .07, s * 1.75 + .07, .06 - E, 3.9 + E, -.07, .07) for s in (-1, 1)])
        p.add("Canopy", G, blk(-1.95, 1.95, 3.9, 4.1, -.5, .5, .05, 2)); p.add("Canopy_Light", V, box(-1.6, 1.6, 3.88, 3.9 + E, -.3, .3))
        for x in np.linspace(-1.5, 1.5, 11):
            for z in (-.15, .15):
                L = 2.6 - 1.4 * abs(x) / 1.5 + rng.uniform(-.1, .1); ybot = 3.88 - L
                p.add("Cables", T, ring(.003, ybot, 3.88 + E, 4, x=x, z=z))
                for y in np.arange(3.8, ybot + .04, -.13):
                    m = VM if rng.random() < .3 else T; p.add("Tags_Violet" if m == VM else "Tags_Ti", m, box(x - .016, x + .016, y - .055, y, z + .0025, z + .0055))
        LEDGES[v] = "open floor plate 3.8 x 1.2 at y 0.06; outer cables stop at y ~2.6 so the plate ends are clear: lamp at x -1.4, offering at x +1.2 (z +0.3)"
    elif v == 5:  # Eternal Emitter: titanium stele split by an amber seam, slate plinth with an open emitter bowl and layered flame form
        p.add("Stele", T, box(-1.8, -.03, 0, 3.8, -.6, -.4), box(.03, 1.8, 0, 3.8, -.6, -.4))
        p.add("Amber_Seam", A, box(-.03 - E, .03 + E, .2, 3.6, -.59, -.41))
        p.add("Plinth", S, box(-1.2, 1.2, 0, .9, -.396, .6)); p.add("Plinth_Top", G, box(-1.22, 1.22, .9 - E, .96, -.38, .62))
        w = .5; h0 = .96 - E; t = .03
        p.add("Emitter_Bowl", T, box(-w / 2, w / 2, h0, h0 + .04, -w / 2, w / 2), box(-w / 2, w / 2, h0 + .04 - E, h0 + .2, w / 2 - t, w / 2), box(-w / 2, w / 2, h0 + .04 - E, h0 + .2, -w / 2, -w / 2 + t),
              box(-w / 2, -w / 2 + t, h0 + .04 - E, h0 + .2, -w / 2 + t - E, w / 2 - t + E), box(w / 2 - t, w / 2, h0 + .04 - E, h0 + .2, -w / 2 + t - E, w / 2 - t + E))
        fl = lambda r, y1, n: loft(circle(r, n), [(h0 + .04 - E, 1, 1), (h0 + .04 + (y1 - h0) * .45, .8, .8), (y1, .05, .05)])
        p.add("Flame_Outer", A, fl(.1, 1.8, 10)); p.add("Flame_Core", V, xf(fl(.05, 1.45, 8), t=(.155, 0, 0)))
        LEDGES[v] = "plinth top 2.44 x 1.0 at y 0.96 either side of the bowl (x +-0.35..1.2): lamp at x +0.9, offering at x -0.85; floor in front (z > 0.62) also clear"
    return p
MON = [(1, "Tag_Stele_Wall"), (2, "Tiered_Obelisk"), (3, "Halo_Ring"), (4, "Tag_Curtain"), (5, "Eternal_Emitter")]
sf.ASSETS["monument"] = ("ext_memorial_monument", monument, MON, 6000, "#29 memorial monument (~3-4 W x 3-4.5 H)")
if __name__ == "__main__":
    sf.build("monument"); [print("LEDGE", k, v) for k, v in sorted(LEDGES.items())]
