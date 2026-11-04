"""Rook: Tennis Tower E-terrace playground piece 1, combo tower (spec §3.11.6: 8 x 6 m, 2 decks at 1.2 / 2.0 m, 2 slides running axially (X),
no spinning parts). Entry stair on the +Z face (6 x 0.20 to deck A +1.2), 4 x 0.20 link stair to deck B +2.0, slide S1 from B toward +X,
slide S2 from A toward -X (30 deg, exit at +0.25). 0.9 m infill guards on every open deck edge, canopy over B at +4.1 (2.1 m adult headroom).
No wood. REUSE: slide-tower/stair-core ramp colliders (slab_between) + tread/cast scheme, court-partition SGM posts, restroom Leaf Crest crest(),
tree-column/roof Y-fork tubes, #60 climbing-panel ball holds, stand planter()/shrubs(), cabana_lounger.boxuv UVs. Run: python3 play_tower.py"""
from modlib import *
import modlib
from stair_core_colliders_rev_c import slab_between
from cabana_lounger import boxuv
from restroom_extras import crest
modlib._m("tt_rubber", "TT_PlayRubber_EPDM", (.22, .45, .33), 0, .9)
modlib._m("tt_hdpe_leaf", "TT_PlayPanel_HDPE_Leaf", (.30, .55, .34), 0, .6)
modlib._m("tt_hdpe_sand", "TT_PlayPanel_HDPE_Sand", (.78, .70, .55), 0, .6)
RU, YA, YB, CAN = "tt_rubber", 1.2, 2.0, 4.2
XL, XR = -1.5, 0.0; ZA0, ZA1, ZB0, ZB1 = -.25, 1.25, -2.71, -1.21; SX = (-1.4, -.4); R, TR = .2, .32; TH30 = np.radians(30)
def U(m): m.metadata["uv"] = np.zeros((len(m.vertices), 2)); return m
def tm(m, M): uv = m.metadata['uv']; m.apply_transform(M); m.metadata['uv'] = uv; return m
def hull(pts): return trimesh.convex.convex_hull(np.array(pts, float))

def stair(p, z0, y0, n, solid):
    for k in range(1, n):
        za, zb, yt = z0 - k*TR, z0 - (k-1)*TR, y0 + k*R
        if k == n - 1: za -= E
        p.add("Stair_Cast", WH, boxuv(box(SX[0] + .002, SX[1] - .002, .002 if solid else yt - .2, yt - .02 + E, za, zb), .5))
        p.add("Treads_Rubber", RU, boxuv(box(SX[0] + .004, SX[1] - .004, yt - .02, yt, za + .002, zb + .004), .5))
    z1, y1 = z0 - (n-1)*TR, y0 + n*R
    p.add(f"Stair{n}_Ramp-colonly", G, U(slab_between(*SX, z0 + TR, y0, z1, y1)))
    for x0, x1 in ((SX[0] - .04, SX[0]), (SX[1], SX[1] + .04)):   # solid cheek guards following the pitch (0.9 above the nosing line)
        b = y0 - (0 if solid else .1)
        p.add("Stair_Cheeks", q_panel, boxuv(hull([(x, y, z) for x in (x0, x1) for (y, z) in ((max(b, 0), z0 + (TR if solid else E)), (y0 + .9 + R, z0 + (TR if solid else E)), (y1 + .9, z1 - E), (y1 - .1, z1 - E))]), .5))
    return z1, y1

def slide(p, x0, y0, zc, sgn, mat):
    """flat start 0.3, 30 deg run to +0.25, flat exit 0.5; built along +u then mirrored for sgn=-1."""
    run = (y0 - .25)/np.tan(TH30); segs = [(0, .3, 0.0), (.3, .3 + run/np.cos(TH30), TH30), (None, .5, 0.0)]
    bed, walls, cols, legs = [], [], [], []; u0, yy = 0.0, y0 - .003
    for a, L, th in ((0, .3, 0), (0, run/np.cos(TH30), TH30), (0, .5, 0)):
        M = trimesh.transformations.translation_matrix((x0 + sgn*u0, yy, zc)) @ trimesh.transformations.rotation_matrix(-sgn*th, [0, 0, 1])
        lo, hi = (0, L) if sgn > 0 else (-L, 0)
        bed.append(tm(box(lo - .002*sgn*0, hi, -.03, 0, -.25, .25), M)); walls += [tm(box(lo, hi, -.03 + E, .15, s*.25 - (.03 if s > 0 else 0), s*.25 + (0 if s > 0 else .03)), M) for s in (-1, 1)]
        cols.append(U(hull(bed[-1].vertices)))
        u0 += L*np.cos(th); yy -= L*np.sin(th)
    p.add("Slide_Chute", mat, *[boxuv(m, .5) for m in bed + walls])
    for i, c in enumerate(cols): p.add(f"Slide_{'E' if sgn > 0 else 'W'}{i}-convcolonly", G, c)
    xe = x0 + sgn*(u0 - .25); p.add("Slide_Legs", SGM, *[boxuv(tube((xe, 0, zc + s*.18), (xe, .25 - .03 + E, zc + s*.18), .03, 6), .5) for s in (-1, 1)])
    xm = x0 + sgn*(.3 + run*.6); ym = y0 - .003 - run*.6*np.tan(TH30) - .03 + E
    p.add("Slide_Legs", SGM, *[boxuv(tube((xm, 0, zc + s*.18), (xm, ym - .02*0, zc + s*.18), .03, 6), .5) for s in (-1, 1)])

def build(q):
    global q_panel; q_panel = q.get("panel", "tt_hdpe_leaf"); p = Part(); d = q["dress"]
    p.add("Decks", RU, *[boxuv(box(XL + .046, XR - .046, y - .1, y, z0, z1), .5) for y, z0, z1 in ((YA, ZA0, ZA1), (YB, ZB0, ZB1))])
    p.add("Deck_Frame", SGM, *[boxuv(box(XL + .05, XR - .05, y - .25, y - .1 + E, z0 + .05, z1 - .05), .5) for y, z0, z1 in ((YA, ZA0, ZA1), (YB, ZB0, ZB1))])
    for tag, y, z0, z1 in (("A", YA, ZA0, ZA1), ("B", YB, ZB0, ZB1)): p.add(f"Deck{tag}-colonly", G, U(trimesh.creation.box(bounds=[[XL + .046, y - .25, z0], [XR - .046, y, z1]])))
    pm = q.get("post", SGM)
    p.add("Posts", pm, *[boxuv(tube((x, 0, z), (x, (CAN - .1 + E) if z <= ZB1 else YA + .95, z), .05, 8), .5) for x in (XL, XR) for z in (ZA0 + 0, ZA1, ZB0, ZB1)])
    stair(p, 2.85, 0.0, 6, True); stair(p, ZA0, YA, 4, False)
    g = []; gp = lambda y, x0, x1, z0, z1: g.append(boxuv(box(x0, x1, y + .002, y + .9, z0, z1), .5))
    for y, z0, z1 in ((YA, ZA0, ZA1), (YB, ZB0, ZB1)):
        gp(y, XR - .015, XR + .015, z0 + .05 - E, z1 - .05 + E) if y == YA else None
        gp(y, SX[1] + .046, XR - .05 + E, z1 - .015, z1 + .015) if y == YA else gp(y, SX[1] + .046, XR - .05 + E, z1 - .015, z1 + .015)
        gp(y, SX[1] + .046, XR - .05 + E, z0 - .015, z0 + .015) if y == YA else gp(y, XL + .05 - E, XR - .05 + E, z0 - .015, z0 + .015)
    gp(YA, XL - .015, XL + .015, ZA0 + .05 - E, .0); gp(YA, XL - .015, XL + .015, .6, ZA1 - .05 + E)
    gp(YB, XL - .015, XL + .015, ZB0 + .05 - E, ZB1 - .05 + E)
    gp(YB, XR - .015, XR + .015, ZB0 + .05 - E, -2.22); gp(YB, XR - .015, XR + .015, -1.58, ZB1 - .05 + E)
    p.add("Guard_Panels", q_panel, *g)
    p.add("Guards-convcolonly", G, *[U(trimesh.creation.box(bounds=m.bounds)) for m in g])
    sm = q.get("slide", ALY); slide(p, XR - .046 + .002, YB, -1.9, 1, sm); slide(p, XL + .046 - .002, YA, .3, -1, sm)
    p.add("Canopy", q.get("roof", "tt_hdpe_leaf"), boxuv(box(XL - .25, XR + .25, CAN - .1, CAN, ZB0 - .25, ZB1 + .25), .5))
    if d == "leaf":   # Leaf Crest: leaf crests standing on the A posts, leaf canopy fringe
        p.add("Leaf_Crests", LF, *[crest((x, YA + .95 + .17 - .003, z)) for x in (XL, XR) for z in (ZA0, ZA1)])
        p.add("Canopy_Leaves", LF, *[xf(leaf((0, 0, 0), .3, .14, t=.0125), R=trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]), t=(x, CAN - .1 + E, ZB1 + .25 - .1)) for x in np.linspace(-1.6, .1, 5)])
    elif d == "tree": # Tree House: Y-forks from the B posts into the canopy + foliage clumps on top
        p.add("Tree_Forks", ST, *[boxuv(tube((x + sx*.05, CAN - .8, z + sz*.05), (x + sx*.25, CAN - .1 - .002, z + sz*.25), .03, 6), .5) for x, sx in ((XL, -1), (XR, 1)) for z, sz in ((ZB0, -1), (ZB1, 1))])
        p.add("Canopy_Foliage", LF2, *[clump((x, CAN + .14 - E, z), .17, i) for i, (x, z) in enumerate([(a, b) for a in (-1.4, -.75, -.1) for b in (-2.55, -1.9, -1.25)])])
    elif d == "court":  # Court Line: tennis-ball finials on the A posts, amber court-line stripe on the decks, ball holds up the B -X guard
        p.add("Ball_Finials", BA, *[node((x, YA + .95 + .035 - E, z), .045, 0) for x in (XL, XR) for z in (ZA0, ZA1)])
        p.add("Court_Line", AM, boxuv(box(XL + .1, XR - .1, YA + .002, YA + .005, ZA1 - .15, ZA1 - .1), .5), boxuv(box(XL + .1, XR - .1, YB + .002, YB + .005, ZB0 + .1, ZB0 + .15), .5))
        p.add("Ball_Holds", BA, *[node((XL - .015 - .035 + E, y, z), .04, 0) for y, z in ((YB + .3, -2.4), (YB + .55, -1.9), (YB + .3, -1.45))])
    elif d == "garden": # Garden Deck: planters under deck A + green cheek-top shrubs
        tr, so, sy = planter(-1.3, -.2, 0, -.15, .45, h=.4); p.add("Planter", G, boxuv(tr, .5)); p.add("Planter_Soil", SO, so); p.add("Foliage", LF2, shrubs(-1.25, -.25, sy, .15, r=.15, seed=3))
    elif d == "climb":  # Climb Face: #60 Court Line climbing panel strip as a second way up to B on its -Z face
        p.add("Climb_Face", SSL, boxuv(box(XL + .06, XR - .06, .002, YB - .25 - .002, ZB0 - .08, ZB0 - .06), .5))
        p.add("Climb_Holds", BA, *[node((x, y, ZB0 - .08 - .04 + E), .045, 0) for x, y in ((-1.2, .3), (-.4, .55), (-.9, .9), (-.3, 1.2), (-1.1, 1.45), (-.7, 1.65))])
    for k, (mk, m) in list(p.P.items()):
        if "colonly" in k and m.bounds[0][1] < 0: m = m.slice_plane([0, 0, 0], [0, 1, 0], cap=True); p.P[k] = (mk, U(m))
    p.walk = [(-.9, 3.4), (-.9, .5), (-.9, -.1), (-.9, -1.4), (-.75, -2.2), (-.3, -1.9)]
    return p

VARIANTS = [
    dict(label="Leaf Crest: leaf HDPE guards, leaf crests, leaf canopy fringe", dress="leaf"),
    dict(label="Tree House: Y-fork posts into a foliage canopy", dress="tree", panel="tt_hdpe_sand"),
    dict(label="Court Line: ball finials, court-line decks, ball holds", dress="court", panel=SGM, slide=BA, roof=SGM),
    dict(label="Garden Deck: planter under deck A, sand guards", dress="garden", panel="tt_hdpe_sand", roof="tt_hdpe_leaf"),
    dict(label="Climb Face: Court Line climbing strip up to deck B", dress="climb", slide=ALY),
]
if __name__ == "__main__":
    run("play_tower", build, VARIANTS, title="combo tower 8 x 6 m, decks +1.2 / +2.0, 2 axial slides | nature + sports")
    W = {}
    for i, v in enumerate(VARIANTS, 1):
        pp = build(v); fl = trimesh.creation.box(bounds=[[-1.6, -.2, 2.85], [0, 0, 3.7]]); pp.P["Entry_Floor-colonly"] = (G, U(fl)); W[f"v{i}"] = walk_check(pp, pp.walk)
    print("WALK", json.dumps(W)); json.dump(W, open(os.path.join(RENDER_OUT, "play_tower", "walk_check.json"), "w"), indent=1)
