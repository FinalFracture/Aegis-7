"""Rook: Tennis Tower F3 cabana (spec §3.11.6 + §3.9 W terrace: 8 cabanas 4 x 4 m, X -11..-7, Z 18..62, 1.5 m apart, looking out at the W glass).
Post-and-beam frame 3.0 m to the eave, fabric hip roof peak +3.4, roll-down fabric on 3 sides (back down, sides rolled), open face = +Z
(place +Z toward the W glass, i.e. rotate so +Z points -X). 2 loungers + side table inside.
REUSE: court-partition SGM post language, Rev C materials, stand planter()/shrubs(), restroom Leaf Crest crest(), roof/tree-column Y-fork tubes,
court tennis-ball nodes + court-line tape (climbing panel #60). Run: python3 cabana.py"""
from modlib import *
from restroom_extras import crest
S, PC, PW, EAVE, PEAK = 2.0, 1.88, .06, 3.0, 3.4   # half size, post centre, post half width
def U(m): m.metadata["uv"] = np.zeros((len(m.vertices), 2)); return m

def build(q):
    p = Part(); fab, d = q["fabric"], q["dress"]; y0 = .002 if q.get("rug") else 0.0
    p.add("Posts", q.get("post", SGM), *[box(sx*PC - PW, sx*PC + PW, 0, EAVE - .15 + E, sz*PC - PW, sz*PC + PW) for sx in (-1, 1) for sz in (-1, 1)])
    p.add("Eave_Beams", q.get("post", SGM), box(-S, S, EAVE - .15, EAVE, -S, -S + .12), box(-S, S, EAVE - .15, EAVE, S - .12, S), box(-S, -S + .12, EAVE - .15, EAVE, -S + .12 - E, S - .12 + E), box(S - .12, S, EAVE - .15, EAVE, -S + .12 - E, S - .12 + E))
    p.add("Fabric_Roof", q.get("roof", fab), loft(rrect(2*S, 2*S, .001, 1), [(EAVE - E, 1, 1), (PEAK, .01, .01)]))
    p.add("Fabric_Back_Drop", fab, box(-PC + PW - E, PC - PW + E, .12, EAVE - .15 + E, -PC - .005, -PC + .005))
    p.add("Fabric_Rolls", fab, *[tube((sx*PC, EAVE - .15 - .06 + E, -PC + PW - E), (sx*PC, EAVE - .15 - .06 + E, PC - PW + E), .06, 8) for sx in (-1, 1)])
    for sx in (-1, 1):   # loungers
        x = sx*.8
        p.add("Lounger_Frame", WH, box(x - .35, x + .35, y0, .3, -.9, 1.0))
        p.add("Cushions", q.get("cushion", LF2), box(x - .33, x + .33, .3 - E, .4, -.5, .98), beam((x, .37, -.52), (x, .95, -.88), .66, .08))
    p.add("Side_Table", ALY, cap((0, .5, -.4), .25, .03, 16, axis="y"), tube((0, y0, -.4), (0, .485 + E, -.4), .03, 6))
    cols = [box(sx*PC - PW, sx*PC + PW, 0, EAVE, sz*PC - PW, sz*PC + PW) for sx in (-1, 1) for sz in (-1, 1)] + [box(sx*.8 - .35, sx*.8 + .35, 0, .4, -.9, 1.0) for sx in (-1, 1)]
    p.add("Cabana-convcolonly", G, *[U(trimesh.creation.box(bounds=[c.bounds[0], c.bounds[1]])) for c in cols])
    if q.get("rug"): p.add("Court_Rug", q["rug"], box(-1.5, 1.5, 0, .006, -1.4, 1.6))
    if d == "garden":   # Garden Canopy: planters in the back corners, foliage
        for sx in (-1, 1):
            tr, so, sy = planter(sx*1.45 - .3, sx*1.45 + .3, 0, -1.75, -1.25, h=.45); p.add("Planters", G, tr); p.add("Planter_Soil", SO, so)
            p.add("Foliage", LF2, shrubs(sx*1.45 - .28, sx*1.45 + .28, sy, -1.5, r=.18, seed=3 + sx))
    elif d == "leaf":   # Leaf Crest: leaf crests on every post head + leaf-green cushions
        p.add("Leaf_Crests", LF, *[xf(leaf((0, 0, 0), .34, .12, t=.0125), R=trimesh.transformations.rotation_matrix(np.pi/2*(1 if i % 2 else -1), [0, 0, 1]), t=(x, EAVE - .075, S + .0125 - E)) for i, x in enumerate(np.linspace(-1.35, 1.35, 4))])
    elif d == "branch": # Branch Fork: Y-fork brackets from each post to the eave beams
        fk = []
        for sx in (-1, 1):
            for sz in (-1, 1):
                zf = sz*(S - .06); a = (sx*(PC - PW - .03 + E), 2.1, zf); b = (sx*(PC - .4), 2.5, zf)
                fk += [tube(a, b, .03, 6), tube(b, (sx*(PC - .25), EAVE - .15 + E, zf), .025, 6), tube(b, (sx*(PC - .7), EAVE - .15 + E, zf), .025, 6)]
        p.add("Branch_Forks", ST, *fk)
    elif d == "court":  # Court Line: amber court-line stripe on the rug, tennis balls in a basket on the table
        p.add("Court_Line", AM, box(-1.4, 1.4, .004, .009, .25, .3), box(-.025, .025, .004, .009, -1.3, 1.5))
        p.add("Ball_Basket", WH, box(-.12, .12, .515 - E, .6, -.52, -.28)); p.add("Tennis_Balls", BA, *[node((x, .6 + .033 - E, z), .035, 0) for x, z in ((-.05, -.45), (.05, -.45), (0, -.35))])
    elif d == "grove":  # Shade Grove: hanging foliage along the inside of the eave beams + vine on the back posts
        p.add("Hanging_Foliage", LF2, *[clump((x, EAVE - .15 - .1 + E, S - .11), .11, i) for i, x in enumerate(np.linspace(-1.5, 1.5, 6))])
        st, lv = vine([(sx*(PC + PW + .012 - E), .1, -PC) for sx in (-1,)] + [(-(PC + PW + .012 - E), 2.7, -PC)], outward=True, seed=4)
        p.add("Vine_Stem", LF, st); p.add("Vine_Leaves", LF2, lv)
    return p

VARIANTS = [
    dict(label="Garden Canopy: leaf-green fabric, corner planters", dress="garden", fabric=LF, cushion=WH),
    dict(label="Leaf Crest: white fabric, leaf crests on the eave, green cushions", dress="leaf", fabric=WH, cushion=LF),
    dict(label="Branch Fork: Y-fork brackets, steel posts, white fabric", dress="branch", fabric=WH, post=ST, cushion=LF2),
    dict(label="Court Line: white fabric, court rug + amber line, ball basket", dress="court", fabric=WH, rug=SSL, cushion=LF2),
    dict(label="Shade Grove: green fabric, hanging foliage, vine post", dress="grove", fabric=LF2, cushion=WH),
]
if __name__ == "__main__": run("cabana", build, VARIANTS, title="4 x 4 m, eave 3.0, hip peak 3.4, open face +Z (to the glass) | nature + sports")
