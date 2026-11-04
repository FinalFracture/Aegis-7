"""Rook: Tennis Tower climbing wall panel (spec §3.11.6: module 1.25 m wide; lead wall 16 panels x 5 courses of 2.3 m = 20 x 11.5 m,
§3.7.1 Stand-Back Wall). One course panel 1.25 x 2.3 m, tiles in X every 1.25 m and stacks in Y every 2.3 m (face sheet inset 1 mm per edge).
Face at +Z (climber side), steel sub-frame behind. Holds sit on the face (embed 4 mm), never cross an edge.
REUSE: court-partition SGM post language for the sub-frame, Rev C stair materials (white composite / slate / gunmetal), restroom Leaf Crest
crest() leaves, roof-bay / tree-column Y-fork tubes, stand/court tennis-ball nodes, stand shrubs() clumps. Run: python3 climbing_panel.py"""
from modlib import *
from restroom_extras import crest
W, H, TF = 1.25, 2.3, .018
def U(m): m.metadata["uv"] = np.zeros((len(m.vertices), 2)); return m
def sit(m, z0=0.0):  # move a mesh so its back touches the face at z0 (embedded E)
    m.apply_translation((0, 0, z0 - m.bounds[0][2] - E)); return m
def hold(c, r, seed, flat=.55):
    m = clump((c[0], c[1], 0), r, seed); m.vertices[:, 2] *= flat; return sit(m)
def pts(n, seed, m=.14, sp=.26):
    global q_sp; q_sp = sp
    rng = np.random.default_rng(seed); P = []
    while len(P) < n:
        x, y = rng.uniform(-W/2 + m, W/2 - m), rng.uniform(m, H - m)
        if all(np.hypot(x - a, y - b) > q_sp for a, b in P): P.append((x, y))
    return P

def seg_d(c, a, b):
    c, a, b = np.array([*c, 0.]), np.array(a, float), np.array(b, float); t = np.clip(np.dot(c - a, b - a)/np.dot(b - a, b - a), 0, 1); return np.linalg.norm(c - a - t*(b - a))

def build(q):
    p = Part(); d = q["dress"]
    p.add("Face_Sheet", q.get("face", WH), box(-W/2 + .001, W/2 - .001, 0, H - .002, -TF, 0))
    p.add("Sub_Frame", SGM, box(-W/2 + .03, -W/2 + .07, 0, H - .002, -TF - .08, -TF + E), box(W/2 - .07, W/2 - .03, 0, H - .002, -TF - .08, -TF + E),
          box(-W/2 + .07 - E, W/2 - .07 + E, .02, .08, -TF - .06, -TF + E), box(-W/2 + .07 - E, W/2 - .07 + E, H - .08, H - .02, -TF - .06, -TF + E))
    p.add("Panel-colonly", G, U(trimesh.creation.box(bounds=[[-W/2 + .001, 0, -TF - .08], [W/2 - .001, H - .002, 0]])))
    P = pts(q.get("n", 14), q.get("seed", 1), sp=q.get("sp", .26)); hm = q.get("hold", GRN)
    if d == "leaf":    # Leaf Crest: leaf-blade edges (restroom crest leaves laid flat) + green jug holds
        p.add("Leaf_Edges", LF, *[sit(xf(leaf((0, 0, 0), .3, .16, t=.02), R=trimesh.transformations.rotation_matrix(a, [0, 0, 1]), t=(x, y - .1, 0))) for i, (x, y) in enumerate(P[:5]) for a in [(.6 if i % 2 else -.6)]])
        p.add("Holds", hm, *[hold(c, .07, i) for i, c in enumerate(P[5:])])
    elif d == "branch":  # Branch Fork: Y-fork arete volume (roof/tree-column fork) bolted on, crimp holds elsewhere
        a, b = (0, .15, 0), (0, 1.2, 0); c1, c2 = (-.4, 2.1, 0), (.4, 2.1, 0)
        tb = [sit(tube(a, b, .06, 6)), sit(tube(b, c1, .05, 6)), sit(tube(b, c2, .05, 6))]
        p.add("Branch_Volume", ST, *tb)
        p.add("Holds", hm, *[hold(c, .06, i) for i, c in enumerate(P) if min(seg_d(c, s0, s1) for s0, s1 in ((a, b), (b, c1), (b, c2))) > .16])
    elif d == "court":   # Court Line: tennis-ball holds, court-line route tape, slate face
        p.add("Holds", BA, *[sit(node((x, y, 0), .045, 0)) for x, y in P])
        p.add("Route_Tape", AM, *[box(x - .04, x + .04, y - .14, y - .12, .002, .004) for x, y in P[::3]])
    elif d == "bark":    # Tree Bark: faceted slate bark volumes + fern-leaf crests at the top
        rng = np.random.default_rng(4); vs = []
        for x, y in P[:3]:
            o = [(0, 0), (.24, .0), (.12, .3)]; m = prism([(-.14, 0), (.14, 0), (0, .12)], -.17, .17)
            vs.append(sit(xf(m, t=(x, y, 0))))
        p.add("Bark_Volumes", SSL, *vs)
        p.add("Holds", hm, *[hold(c, .065, i) for i, c in enumerate(P[3:])])
        p.add("Fern_Crests", LF, *[sit(crest((x, H - .32, 0)) if False else xf(leaf((0, 0, 0), .22, .1, t=.012), t=(x, H - .3, 0))) for x in (-.45, -.15, .15, .45) if min(np.hypot(x - u, H - .2 - v) for u, v in P) > .3])
    elif d == "pebble":  # River Pebble: big smooth pebble holds in greys + green fern pockets
        p.add("Holds", hm, *[hold(c, .09 if i % 3 == 0 else .06, i, .45) for i, c in enumerate(P)])
        p.add("Fern_Pockets", LF2, *[hold(c, .05, 50 + i, .4) for i, c in enumerate(pts(3, 77, .2)) if min(np.hypot(c[0] - a, c[1] - b) for a, b in P) > .17])
    return p

VARIANTS = [
    dict(label="Leaf Crest: leaf-blade edges, green jugs", dress="leaf", hold=GRN, face=WH, seed=3, sp=.36, n=11),
    dict(label="Branch Fork: Y-fork arete volume, crimps", dress="branch", hold=AM, face=WH, seed=5),
    dict(label="Court Line: tennis-ball holds, route tape, slate face", dress="court", face=SSL, seed=7),
    dict(label="Tree Bark: faceted bark volumes, fern crests", dress="bark", hold=LF2, face=WH, seed=9, sp=.3, n=12),
    dict(label="River Pebble: smooth pebble holds, fern pockets", dress="pebble", hold=SL, face=WH, n=12, seed=11),
]
if __name__ == "__main__":
    run("climbing_panel", build, VARIANTS, title="course panel 1.25 x 2.3 m (tile X 1.25, stack Y 2.3) | nature + sports")
