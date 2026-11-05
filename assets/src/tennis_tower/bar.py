"""Rook: Tennis Tower F3 small bar (spec §3.9: zone X 8..20, Z 35..44 = 12 x 9 m, ~14 m counter, ~20 stools, opposite the LW / lift W landing).
U counter: 8.0 m front run (guest side +Z) + two 3.0 m returns = 14.0 m, open at the back (-Z) for staff, back bar 4.8 m inside.
Counter h 1.10, slate top with 0.25 m guest overhang, gunmetal toe-recessed plinth, alloy foot rail. 20 stools (12 front + 4 per return)
in the #61 L3 Alloy + Slate language (brushed alloy frame, tufted slate upholstery on the starting-area atlas UV_FABRIC_SLATE).
No wood (art direction). UVs: world box projection (cabana_lounger.boxuv). Run: python3 bar.py"""
from modlib import *
from cabana_lounger import boxuv, atlasuv, pillow, fit, T, ATLAS, vcolor
from restroom_extras import crest
CH, TOPT = 1.10, .04
def U(m): m.metadata["uv"] = np.zeros((len(m.vertices), 2)); return m
STOOLS = [(x, 1.68) for x in np.linspace(-3.575, 3.575, 12)] + [(sx*4.65, z) for sx in (-1, 1) for z in (-1.45, -.8, -.15, .5)]
lay = trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0])

def stool(F, C, x, z):
    F += [cap((x, .01, z), .22, .02, 10, axis="y"), tube((x, .02 - E, z), (x, .70 + E, z), .03, 8), box(x - .15, x + .15, .30, .33, z - .015, z + .015), cap((x, .71, z), .17, .02, 10, axis="y")]
    C.append(fit(T(loft(rrect(.38, .08, .03, 2), [(0, .95, .55), (.025, 1, 1), (.355, 1, 1), (.38, .95, .55)]), lay), (x - .19, .72 - E, z - .19)))

def build(q):
    p = Part(); body = q.get("body", WH); d = q["dress"]
    B = [box(-4, 4, .1, CH - TOPT + E, .6, 1.2), box(3.4, 4, .1, CH - TOPT + E, -1.8, .6), box(-4, -3.4, .1, CH - TOPT + E, -1.8, .6)]
    p.add("Counter_Body", body, *[boxuv(m, .6) for m in B])
    p.add("Counter_Plinth", SGM, *[boxuv(m, .6) for m in (box(-3.92, 3.92, 0, .1 + E, .66, 1.12), box(3.48, 3.92, 0, .1 + E, -1.75, .66), box(-3.92, -3.48, 0, .1 + E, -1.75, .66))])
    p.add("Counter_Top_Slate", SSL, *[boxuv(m, .6) for m in (box(-4.25, 4.25, CH - TOPT, CH, .55, 1.45), box(3.35, 4.25, CH - TOPT, CH, -1.85, .55), box(-4.25, -3.35, CH - TOPT, CH, -1.85, .55))])
    rail = [tube((-4.12, .22, 1.32), (4.12, .22, 1.32), .025, 8)] + [tube((sx*4.12, .22, -1.7), (sx*4.12, .22, 1.32), .025, 8) for sx in (-1, 1)]
    rail += [box(x - .015, x + .015, .2, .24, 1.2 - E, 1.32) for x in np.linspace(-3.6, 3.6, 5)]
    rail += [box(4 - E, 4.12, .2, .24, z - .015, z + .015) for z in (-1.2, .2)] + [box(-4.12, -4 + E, .2, .24, z - .015, z + .015) for z in (-1.2, .2)]
    p.add("Foot_Rail", ALY, *[boxuv(m, .5) for m in rail])
    p.add("Back_Bar", body, boxuv(box(-2.4, 2.4, 0, .95 + E, -1.8, -1.35), .6)); p.add("Back_Bar_Top", SSL, boxuv(box(-2.42, 2.42, .95, .99, -1.82, -1.33), .6))
    F, C = [], []
    for x, z in (STOOLS if q.get("stools", True) else []): stool(F, C, x, z)
    if F: p.add("Stool_Frame", ALY, *[boxuv(m, .4) for m in F]); p.add("Stool_Cushions", "tt_cush_slate", *[atlasuv(m, ATLAS["tt_cush_slate"]) for m in C])
    cols = [box(-4.25, 4.25, 0, CH, .55, 1.45), box(3.35, 4.25, 0, CH, -1.85, .55), box(-4.25, -3.35, 0, CH, -1.85, .55), box(-2.42, 2.42, 0, .99, -1.82, -1.33)]
    p.add("Bar-convcolonly", G, *[U(trimesh.creation.box(bounds=c.bounds)) for c in cols])
    if d == "leaf":    # Leaf Crest: leaf-green counter front + leaf crests standing on the back bar
        p.add("Counter_Front_Leaf", LF, boxuv(box(-3.9, 3.9, .27, .95, 1.2 - E, 1.212), .6))
        p.add("Leaf_Crests", LF, *[crest((x, .99 - .003, -1.575)) for x in np.linspace(-2.1, 2.1, 6)])
    elif d == "fin":   # Branch Fin gantry: fish-belly fins over the back bar carrying a glass shelf
        fs = [xf(fin(0, .99 - E, 2.6, .12, .04, 0, belly=.6), t=(x, 0, -1.42)) for x in np.linspace(-2.2, 2.2, 5)]
        p.add("Branch_Fins", ST, *[boxuv(U(f), .5) for f in fs]); p.add("Shelf_Glass", GL, box(-2.3, 2.3, 1.8, 1.812, -1.75, -1.6))
    elif d == "court": # Court Line: amber court-line LED strip on the counter front, score screen + ball pendants over the back bar
        p.add("Court_Line_LED", AM, boxuv(box(-3.9, 3.9, .95, .98, 1.2 - E, 1.206), .5))
        p.add("Score_Screen_Frame", SGM, boxuv(box(-1.2, 1.2, 1.4, 2.2, -1.78, -1.72), .5), boxuv(box(-.04, .04, .99 - E, 1.4 + E, -1.77, -1.73), .5)); p.add("Score_Screen", CY, box(-1.15, 1.15, 1.45, 2.15, -1.72 - E, -1.715))
        p.add("Ball_Finials", BA, *[node((x, .99 + .035 - E, -1.5), .035, 0) for x in (-2.2, -1.8, 1.8, 2.2)])
    elif d == "garden":  # Garden Bar: herb planter on the back bar + planter troughs at the counter returns' back ends
        tr, so, sy = planter(-2.3, 2.3, .99 - E, -1.78, -1.4, h=.22); p.add("Herb_Planter", G, boxuv(tr, .5)); p.add("Herb_Soil", SO, so)
        p.add("Herb_Foliage", LF2, shrubs(-2.25, 2.25, sy, -1.59, r=.13, seed=6))
    elif d == "canopy":  # Tree Canopy: Y-fork posts at the back bar ends carrying a leaf ring over the staff aisle (top 2.9)
        tb = []
        for sx in (-1, 1):
            a = (sx*2.55, 0, -1.55); b = (sx*2.55, 2.2, -1.55); tb += [tube(a, b, .06, 8), tube(b, (sx*2.0, 2.8, -.6), .04, 6), tube(b, (sx*3.1, 2.8, -.6), .04, 6)]
        tb.append(tube((-3.15, 2.8, -.6), (3.15, 2.8, -.6), .035, 6)); p.add("Tree_Forks", ST, *[boxuv(m, .5) for m in tb])
        p.add("Canopy_Leaves", LF, *[leaf_dir((x, 2.8 - .035 + E - .0, -.6 + .03), (0, -.3, 1), .3, .16) for x in np.linspace(-2.9, 2.9, 12)])
    return p

VARIANTS = [
    dict(label="Leaf Crest: leaf-green counter front, leaf crests on the back bar", dress="leaf"),
    dict(label="Branch Fin: fish-belly fin gantry + glass shelf", dress="fin"),
    dict(label="Court Line: amber court-line LED, score screen, ball finials", dress="court", body=SGM),
    dict(label="Garden Bar: herb planter along the back bar", dress="garden"),
    dict(label="Tree Canopy: Y-fork posts with a leaf ring over the aisle", dress="canopy"),
]
def stool_only(q):
    p = Part(); F, C = [], []; stool(F, C, 0, 0)
    p.add("Stool_Frame", ALY, *[boxuv(m, .4) for m in F]); p.add("Stool_Cushions", "tt_cush_slate", *[atlasuv(m, ATLAS["tt_cush_slate"]) for m in C])
    p.add("Stool-convcolonly", G, U(trimesh.creation.cylinder(.22, .8, sections=10, transform=trimesh.transformations.translation_matrix((0, .4, 0)) @ trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0])))); return p

def final():
    q = dict(VARIANTS[2], stools=False); raw = build(q)
    V = np.vstack([m.vertices for k, (_, m) in raw.P.items() if "colonly" not in k]); lo, hi = V.min(0), V.max(0); sh = (-(lo[0]+hi[0])/2, -lo[1], -(lo[2]+hi[2])/2)
    rep = run("bar", lambda qq: build(qq) if qq.get("kind") != "stool" else stool_only(qq), [dict(q, label="Court Line counter + back bar (no stools)"), dict(kind="stool", label="L3 bar stool")],
              names=["final_bar", "final_stool"], suffix="_final", sheet="bar_final_sheet.png", title="#62 split", post=vcolor)
    pos = [(round(x + sh[0], 3), 0.0, round(z + sh[2], 3)) for x, z in STOOLS]; json.dump(pos, open(os.path.join(RENDER_OUT, "bar", "stool_positions.json"), "w")); print("POS", pos, "SHIFT", sh); return rep

if __name__ == "__main__" and sys.argv[1:] == ["final"]: final()
elif __name__ == "__main__": run("bar", build, VARIANTS, title="U counter 14 m (8 + 2 x 3), 20 L3 stools, back bar | nature + sports", post=vcolor)
