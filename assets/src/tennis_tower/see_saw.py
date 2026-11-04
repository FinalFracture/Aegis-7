"""Rook: Tennis Tower E-terrace playground piece 4, pair of see-saws (spec §3.11.6: 2 see-saws, axial). Two 3.0 m beams along X (pivot +0.60,
seat +0.66), side by side at z -0.8 / +0.8 on twin-post fulcrums with axle stubs; T-handles at x +-1.0, EPDM end bumpers. No spinning parts, no wood.
Beams are separate animatable parts (SeesawN_Beam incl. seats + handles; hinge = Z line at (0, 0.60, z_i), +-15 deg).
REUSE: #63/#64 playground language (EPDM pad, HDPE seats, ball finials, court-line), restroom Leaf Crest crest(), clump() foliage, cabana_lounger.boxuv.
Run: python3 see_saw.py"""
from modlib import *
import play_tower as pt
from cabana_lounger import boxuv
from restroom_extras import crest
U = pt.U; PAD = .03; YP = .60; BH = .06; BW = .10; ZS = (-.8, .8); HL = 1.5; PX, PZ = 2.5, 1.5
def one(p, i, z, q):
    fm = q.get("frame", SGM); sm = q.get("seat", BA); d = q["dress"]
    B = [box(-HL, HL, YP - BH/2, YP + BH/2, z - BW, z + BW)]
    S = [box(-1.45, -1.15, YP + BH/2 - E, YP + BH/2 + .05, z - .12, z + .12), box(1.15, 1.45, YP + BH/2 - E, YP + BH/2 + .05, z - .12, z + .12)]
    H = []
    for s in (-1, 1):
        x = s*1.0
        H += [tube((x, YP + BH/2 - E, z + w*.08), (x, .95 - .02 + E, z + w*.08), .016, 6) for w in (-1, 1)]
        H += [tube((x, .95, z - .15), (x, .95, z + .15), .02, 8)]
    p.add(f"Seesaw{i}_Beam", fm, *[boxuv(m, .5) for m in B]); p.add(f"Seesaw{i}_Seats", sm, *[boxuv(m, .4) for m in S])
    p.add(f"Seesaw{i}_Handles", ALY, *[boxuv(m, .3) for m in H])
    F = [box(-.06, .06, PAD - E, YP + .08, z + .12, z + .16), box(-.06, .06, PAD - E, YP + .08, z - .16, z - .12)]
    F += [box(-.2, .2, PAD - E, PAD + .03, z - .25, z + .25)]
    p.add(f"Fulcrum{i}", fm, *[boxuv(m, .5) for m in F])
    p.add(f"Fulcrum{i}_Axle", ALY, *[boxuv(tube((0, YP, z + w*(BW - E)), (0, YP, z + w*(.12 + E)), .025, 8), .3) for w in (-1, 1)])
    p.add(f"Bumpers{i}", pt.RU, *[boxuv(cap((s*1.3, PAD + .06 - E, z), .1, .12, 12, axis="y"), .3) for s in (-1, 1)])
    p.add(f"Seesaw{i}-convcolonly", G, U(trimesh.creation.box(bounds=[[-HL, YP - BH/2, z - .15], [HL, .97, z + .15]])))
    p.add(f"Fulcrum{i}-convcolonly", G, U(trimesh.creation.box(bounds=[[-.2, 0, z - .25], [.2, YP + .08, z + .25]])))
    if d == "court":
        p.add(f"Ball_Finials{i}", BA, *[node((s*1.0, .95, z + w*(.15 + .03 - E)), .03, 0) for s in (-1, 1) for w in (-1, 1)])
    elif d in ("leaf", "fern"):
        p.add(f"Leaf_Crests{i}", LF, *[crest((0, YP + .08 + .17 - .003, z + w*.14)) for w in (-1, 1)])
    elif d == "racket":  # racket-head hoops on the handle crossbars
        p.add(f"Racket_Hoops{i}", AM, *[boxuv(xf(trimesh.creation.torus(.11, .012, 12, 6), R=trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]), t=(s*1.0, .95 + .02 + .11 + .012 - E, z)), .3) for s in (-1, 1)])
def build(q):
    p = Part(); d = q["dress"]
    p.add("Safety_Pad", pt.RU, boxuv(box(-PX, PX, 0, PAD, -PZ, PZ), .5))
    for i, z in enumerate(ZS, 1): one(p, i, z, q)
    if d == "court":
        p.add("Court_Line", AM, *[boxuv(box(-PX + .1, PX - .1, PAD - .002, PAD + .002, -.025, .025), .5)], *[boxuv(box(s*2.0 - .025, s*2.0 + .025, PAD - .002, PAD + .002, -PZ + .1, PZ - .1), .5) for s in (-1, 1)])
    elif d == "fern":   # Fern Edge: low foliage clumps at the pad corners (no planters)
        p.add("Foliage", LF2, *[clump((sx*(PX - .3), PAD + .2 - E, sz*(PZ - .3)), .2, k) for k, (sx, sz) in enumerate([(a, b) for a in (-1, 1) for b in (-1, 1)])])
    elif d == "ball":   # Tennis-ball bumpers + centre ball between the fulcrums
        p.add("Centre_Ball", BA, node((0, PAD + .2 - E, 0), .2, 1))
    return p
VARIANTS = [
    dict(label="Court Line: gunmetal beams, ball seats + finials, court-line pad", dress="court"),
    dict(label="Leaf Crest: leaf crests on the fulcrums, leaf seats", dress="leaf", seat=LF),
    dict(label="Racket: amber racket-hoop handles, sand seats", dress="racket", seat="tt_hdpe_sand"),
    dict(label="Fern Edge: slate frame, leaf seats, foliage pad corners", dress="fern", frame=ST, seat=LF2),
    dict(label="Ball Court: centre tennis ball, ball seats, slate frame", dress="ball", frame=SSL),
]
if __name__ == "__main__":
    run("see_saw", build, VARIANTS, title="2 axial see-saws, 3.0 m beams, pivot +0.60, pad 5 x 3 m | nature + sports")
