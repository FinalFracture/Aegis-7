"""Rook: Tennis Tower E-terrace playground piece 5, toddler zone (spec §3.11.6: 4 spring riders + toddler deck in an 8 x 8 m zone).
Poured-rubber pad 8 x 8; toddler deck 2.0 x 2.0 at +0.45 on the -Z side with a 3-step stair (0.15 rise / 0.30 tread) facing +Z and 0.6 m
low guards; 4 spring riders at (+-2.4, +0.9) and (+-2.4, +2.9), coil 0.35 m, seat ~0.55, separate RiderN_Body parts (animate: rock about
the coil base, +-12 deg). No spinning parts, no wood, no planter boxes.
REUSE: #63/#64/#66 playground language (EPDM pad, HDPE panels, ball finials, court-line pad), restroom Leaf Crest crest(), leaf_dir(), clump(),
cabana_lounger.boxuv. Run: python3 toddler_zone.py"""
from modlib import *
import play_tower as pt
from cabana_lounger import boxuv
from restroom_extras import crest
U = pt.U; PAD = .03; HZ = 4.0; DY = .45; DX0, DX1, DZ0, DZ1 = -1.0, 1.0, -3.0, -1.0
RIDERS = [(-2.4, .9), (2.4, .9), (-2.4, 2.9), (2.4, 2.9)]; CY0, CH, CR, WR = PAD + .03, .35, .11, .022
def coil(x, z, turns=4, seg=8, side=5):
    n = turns*seg; V = []; F = []
    for k in range(n + 1):
        a = 2*np.pi*k/seg; c = np.array([x + CR*np.cos(a), CY0 + .01 + (CH - .027)*k/n, z + CR*np.sin(a)])
        t = np.array([-np.sin(a), (CH/turns)/(2*np.pi*CR), np.cos(a)]); t /= np.linalg.norm(t)
        u = np.cross(t, [0, 1, 0]); u /= np.linalg.norm(u); w = np.cross(t, u)
        V += [c + WR*(np.cos(b)*u + np.sin(b)*w) for b in np.linspace(0, 2*np.pi, side, endpoint=False)]
    for k in range(n):
        for j in range(side):
            a, b, c, d = k*side + j, k*side + (j + 1) % side, (k + 1)*side + j, (k + 1)*side + (j + 1) % side; F += [[a, b, d], [a, d, c]]
    F += [[0, j + 1, j] for j in range(1, side - 1)]; o = n*side; F += [[o, o + j, o + j + 1] for j in range(1, side - 1)]
    m = trimesh.Trimesh(np.array(V), np.array(F), process=True); m.fix_normals(); return m
def depth(a, b):
    d = 0.0
    for x, y in ((a, b), (b, a)):
        S = np.vstack([x.vertices, trimesh.sample.sample_surface_even(x, 400, seed=1)[0]])
        ins = y.contains(S)
        if ins.any(): d = max(d, float(trimesh.proximity.signed_distance(y, S[ins]).max()))
    return d
def rest_on(ms, bases, tol=E):  # lift the meshes ms (rigidly, together) until they penetrate the bases by <= tol
    lo, hi = -.0, .3
    def bad(dy): return any(depth(trimesh.Trimesh(m.vertices + (0, dy, 0), m.faces, process=False), b) > tol for m in ms for b in bases)
    if not bad(0): 
        # lower until it touches (avoid floating), then step back
        lo2, hi2 = -.3, 0.0
        for _ in range(14):
            mid = (lo2 + hi2)/2
            if bad(mid): lo2 = mid
            else: hi2 = mid
        dy = hi2
    else:
        for _ in range(14):
            mid = (lo + hi)/2
            if bad(mid): lo = mid
            else: hi = mid
        dy = hi
    for m in ms: m.apply_translation((0, dy, 0))
def rider(p, i, x, z, kind, q):
    top = CY0 + CH
    p.add(f"Rider{i}_Base", G, boxuv(cap((x, PAD + .015 - E, z), .18, .03 + E, 12, axis="y"), .3))
    p.add(f"Rider{i}_Spring", ALY, boxuv(coil(x, z), .3))
    p.add(f"Rider{i}_Plate", G, boxuv(cap((x, top + .015 - E, z), .14, .03, 12, axis="y"), .3))
    b0 = top + .03 - 2*E
    if kind == "ball":     # tennis ball body, seat saddle and handle bar
        body = [node((x, b0 + .2, z), .2, 1)]; m = q.get("seat", BA)
        seat = box(x - .14, x + .14, b0 + .38, b0 + .43, z - .12, z + .1)
        hb = tube((x - .14, b0 + .55, z + .16), (x + .14, b0 + .55, z + .16), .016, 6); post = tube((x, b0 + .36, z + .14), (x, b0 + .55 - .016 + E, z + .16), .016, 6)
    elif kind == "leaf":   # leaf body (fat HDPE lens, long axis along Z) with a seat pad
        body = [xf(leaf_dir((0, 0, 0), (0, 0, 1), .8, .34, t=.12), t=(x, b0 + .12, z - .4))]; m = q.get("seat", LF)
        seat = box(x - .12, x + .12, b0 + .2, b0 + .25, z - .16, z + .06)
        hb = tube((x - .13, b0 + .5, z + .2), (x + .13, b0 + .5, z + .2), .016, 6); post = tube((x, b0 + .17, z + .2), (x, b0 + .5 - .016 + E, z + .2), .016, 6)
    else:                  # turtle: domed shell + head ball
        sh = node((0, 0, 0), .26, 1); sh.vertices *= [1, .55, 1.2]; sh.apply_translation((x, b0 + .1, z)); body = [sh, node((x, b0 + .14, z + .3 + .08 - .02), .09, 0)]; m = q.get("seat", LF2)
        seat = box(x - .12, x + .12, b0 + .24, b0 + .29, z - .14, z + .06)
        hb = tube((x - .13, b0 + .5, z + .14), (x + .13, b0 + .5, z + .14), .016, 6); post = tube((x, b0 + .22, z + .14), (x, b0 + .5 - .016 + E, z + .14), .016, 6)
    pl = cap((x, top + .015 - E, z), .14, .03, 12, axis="y"); sp = coil(x, z)
    rest_on(body, [pl, sp], .0035); rest_on([seat], body, .0035); rest_on([post, hb], body + [seat], .0035)
    p.add(f"Rider{i}_Body", q.get("body", BA if kind == "ball" else "tt_hdpe_leaf" if kind == "leaf" else LF), *[boxuv(b, .3) for b in body])
    p.add(f"Rider{i}_Seat", m, boxuv(seat, .3)); p.add(f"Rider{i}_Handle", ALY, boxuv(hb, .3), boxuv(post, .3))
    p.add(f"Rider{i}-convcolonly", G, U(trimesh.creation.cylinder(radius=.25, height=.9 - .0, transform=trimesh.transformations.translation_matrix((x, .45, z)))))
def build(q):
    p = Part(); d = q["dress"]; fm = q.get("frame", SGM); pn = q.get("panel", "tt_hdpe_leaf")
    p.add("Safety_Pad", pt.RU, boxuv(box(-HZ, HZ, 0, PAD, -HZ, HZ), .5))
    p.add("Toddler_Deck", fm, boxuv(box(DX0, DX1, PAD - E, DY, DZ0, DZ1), .5))
    p.add("Deck_Top", pt.RU, boxuv(box(DX0 + .006, DX1 - .006, DY - E, DY + .02, DZ0 + .006, DZ1 - .006), .5))
    st = [boxuv(box(-.5 + k*.004, .5 - k*.004, PAD - E, DY - .15*(k + 1) + .0, DZ1 - E + .3*k, DZ1 + .3*(k + 1)), .5) for k in range(2)]
    p.add("Deck_Steps", WH, *st); p.add("Step_Treads", pt.RU, *[boxuv(box(-.49 + k*.004, .49 - k*.004, DY - .15*(k + 1) - E, DY - .15*(k + 1) + .015, DZ1 + .3*k + .004, DZ1 + .3*(k + 1) - .004), .5) for k in range(2)])
    gy0, gy1 = DY + .02 - E, DY + .62
    gu = [box(DX0 + .03, DX1 - .03, gy0, gy1, DZ0 + .03, DZ0 + .07)]
    gu += [box(s*.97 - .02, s*.97 + .02, gy0, gy1 - .006, DZ0 + .07 - E, DZ1 - .03) for s in (-1, 1)]
    gu += [box(s*.75 - .22, s*.75 + .22, gy0, gy1 - .012, DZ1 - .07, DZ1 - .03) for s in (-1, 1)]
    p.add("Deck_Guards", pn, *[boxuv(m, .5) for m in gu])
    p.add("Deck-colonly", G, U(trimesh.creation.box(bounds=[[DX0, 0, DZ0], [DX1, DY + .02, DZ1]])))
    p.add("Steps_Ramp-colonly", G, U(pt.hull([(x, y, z) for x in (-.5, .5) for (y, z) in ((0, DZ1 + .6), (DY, DZ1), (0, DZ1))])))
    p.add("Guards-convcolonly", G, U(trimesh.creation.box(bounds=[[DX0, DY, DZ0], [DX1, gy1, DZ0 + .1]])), *[U(trimesh.creation.box(bounds=[[s*.97 - .03, DY, DZ0], [s*.97 + .03, gy1, DZ1]])) for s in (-1, 1)])
    kinds = q["riders"]
    for i, (x, z) in enumerate(RIDERS, 1): rider(p, i, x, z, kinds[(i - 1) % len(kinds)], q)
    if d == "court":
        p.add("Ball_Finials", BA, *[node((s*.97, gy1 - .006 + .035 - E, zz), .035, 0) for s in (-1, 1) for zz in (DZ0 + .1, DZ1 - .1)])
        p.add("Court_Line", AM, *[boxuv(box(-HZ + .15, HZ - .15, PAD - .002, PAD + .002, z - .025, z + .025), .5) for z in (-.3, HZ - .15)], *[boxuv(box(s*1.4 - .025, s*1.4 + .025, PAD - .002, PAD + .002, -.3 + .025, HZ - .175), .5) for s in (-1, 1)])
    elif d == "leaf":
        p.add("Leaf_Crests", LF, *[crest((s*.97, gy1 - .006 + .17 - .003, zz)) for s in (-1, 1) for zz in (DZ0 + .1, DZ1 - .1)])
    elif d == "fern":
        p.add("Foliage", LF2, *[clump((sx*(HZ - .35), PAD + .22 - E, sz*(HZ - .35)), .24, k) for k, (sx, sz) in enumerate([(a, b) for a in (-1, 1) for b in (-1, 1)])])
    return p
VARIANTS = [
    dict(label="Court Line: tennis-ball riders, ball finials, court-line pad", dress="court", riders=["ball"]),
    dict(label="Leaf Crest: leaf riders, leaf crests on the deck guards", dress="leaf", riders=["leaf"]),
    dict(label="Garden Critters: turtle + leaf riders, sand guards", dress="plain", riders=["turtle", "leaf"], panel="tt_hdpe_sand"),
    dict(label="Fern Edge: turtle riders, slate deck, foliage corners", dress="fern", riders=["turtle"], frame=ST),
    dict(label="Match Point: ball + leaf riders, court-line pad, leaf guards", dress="court", riders=["ball", "leaf"], frame=SSL),
]
if __name__ == "__main__":
    run("toddler_zone", build, VARIANTS, title="toddler zone 8 x 8 m: 4 spring riders + 2.0 x 2.0 deck at +0.45 | nature + sports")
