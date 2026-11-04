"""Rook: Tennis Tower E-terrace playground piece 3, climbing dome (spec §3.11.6: Ø 4 m). Lamella dome R 2.0: 4 rings x 10 nodes
(elevations 0 / 22.5 / 45 / 67.5 deg, alternate rings offset half a bay) + apex; struts = convex-hull edges (110), hub nodes merged into
the frame part. Poured-rubber fall-zone pad Ø 7.0 (1.5 m past the dome). No spinning parts, no wood.
REUSE: #63/#64 playground language (EPDM pad, HDPE panels, ball finial, court-line), restroom Leaf Crest crest(), #60 climbing-panel ball
holds on slate panels, stand planter()/shrubs(), cabana_lounger.boxuv. Run: python3 dome_climber.py"""
from modlib import *
import play_tower as pt
from cabana_lounger import boxuv
from restroom_extras import crest
U = pt.U; R, N, RT, RN, PAD = 2.0, 10, .025, .06, .03
def nodes():
    P = []
    for k in range(4):
        e = np.radians(22.5*k); P += [(R*np.cos(e)*np.cos(2*np.pi*j/N + (k % 2)*np.pi/N), R*np.sin(e), R*np.cos(e)*np.sin(2*np.pi*j/N + (k % 2)*np.pi/N)) for j in range(N)]
    P.append((0, R, 0)); P = np.array(P); P[:, 1] += PAD + RN - E; return P
def lattice():
    P = nodes(); h = trimesh.convex.convex_hull(P); edges = set()
    for f in h.faces:
        if all(P[i, 1] < PAD + RN for i in f): continue          # bottom cap
        for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])): edges.add(tuple(sorted((a, b))))
    tris = [f for f in h.faces if not all(P[i, 1] < PAD + RN for i in f)]
    return P, sorted(edges), tris, h

def panel(P, f, t=.02, c0=.09):  # hexagonal infill panel: edges embedded E into the struts, corners chamfered clear of the hub nodes
    V = P[f]; c = V.mean(0); n = np.cross(V[1] - V[0], V[2] - V[0]); n /= np.linalg.norm(n)
    if np.dot(n, c - (0, PAD, 0)) < 0: n = -n
    H = []
    for i in range(3):
        a, b = V[i], V[(i + 1) % 3]; u = (b - a)/np.linalg.norm(b - a); w = np.cross(n, u)
        if np.dot(w, c - a) < 0: w = -w
        H += [a + u*c0 + w*.0155, b - u*c0 + w*.0155]
    H = np.array(H); return U(trimesh.convex.convex_hull(np.vstack([H - n*t/2, H + n*t/2]))), c, n

def build(q):
    p = Part(); d = q["dress"]; fm = q.get("frame", SGM); P, Ed, Tr, h = lattice()
    p.add("Fall_Zone_Pad", pt.RU, boxuv(cap((0, PAD/2, 0), 3.5, PAD, 24, axis="y"), .5))
    p.add("Dome_Frame", fm, *[boxuv(tube(P[a], P[b], RT, 6), .5) for a, b in Ed], *[boxuv(node(c, RN, 0), .3) for c in P])
    hc = trimesh.convex.convex_hull(P); p.add("Dome-convcolonly", G, U(hc))
    top = P[-1]
    pick = lambda sel: [panel(P, f) for i, f in enumerate(Tr) if sel(i, P[f].mean(0))]
    if d == "leaf":    # Leaf Crest: leaf-green HDPE shade panels on the upper ring + leaf crest on the apex
        pans = pick(lambda i, c: c[1] > 1.6 and i % 2 == 0); p.add("Shade_Panels", "tt_hdpe_leaf", *[boxuv(m, .5) for m, _, _ in pans])
        p.add("Leaf_Crest", LF, crest((0, top[1] + RN*.8 + .17 - .003, 0)))
    elif d == "court": # Court Line: ball finial on the apex, yellow panels, amber court-line rings on the pad
        p.add("Ball_Finial", BA, node((0, top[1] + RN*.8 + .06 - E, 0), .07, 0))
        pans = pick(lambda i, c: .8 < c[1] < 1.6 and i % 3 == 0); p.add("Court_Panels", BA, *[boxuv(m, .5) for m, _, _ in pans])
        ring = lambda r: [boxuv(xf(box(-.03, .03, PAD - .002, PAD + .002, -r*np.tan(np.pi/24) - .01, r*np.tan(np.pi/24) + .01), R=trimesh.transformations.rotation_matrix(a, [0, 1, 0]), t=(r*np.cos(a), 0, -r*np.sin(a))), .5) for a in np.linspace(0, 2*np.pi, 24, endpoint=False)]
        p.add("Court_Line", AM, *ring(2.6), *ring(3.3))
    elif d == "canopy":  # Leaf Canopy: full leaf-panel cap on the top ring (shade) + leaf-green frame
        pans = pick(lambda i, c: c[1] > 1.6); p.add("Canopy_Panels", "tt_hdpe_leaf", *[boxuv(m, .5) for m, _, _ in pans])
    elif d == "garden":  # Garden Ring: 4 planter troughs on the pad edge, outside the fall zone core
        for a in np.radians([45, 135, 225, 315]):
            tr, so, sy = planter(-.45, .45, PAD - E, -.15, .15, h=.35)
            for m in (tr, so): m.apply_transform(trimesh.transformations.rotation_matrix(-a + np.pi/2, [0, 1, 0])); m.apply_translation((3.2*np.cos(a), 0, 3.2*np.sin(a)))
            sh = shrubs(-.4, .4, sy, 0, r=.12, seed=int(a*10)); sh.apply_transform(trimesh.transformations.rotation_matrix(-a + np.pi/2, [0, 1, 0])); sh.apply_translation((3.2*np.cos(a), 0, 3.2*np.sin(a)))
            p.add("Planters", G, boxuv(tr, .5)); p.add("Planter_Soil", SO, so); p.add("Foliage", LF2, U(sh))
        p.add("Leaf_Crest", LF, crest((0, top[1] + RN*.8 + .17 - .003, 0)))
    elif d == "holds":   # Court Holds: #60 slate climbing panels in the lower triangles with tennis-ball holds
        pans = pick(lambda i, c: c[1] < 1.0 and i % 2 == 1); p.add("Climb_Panels", SSL, *[boxuv(m, .5) for m, _, _ in pans])
        p.add("Ball_Holds", BA, *[node(c + n*(.01 + .035 - E), .035, 0) for _, c, n in pans])
    return p

def openings():  # inscribed-circle diameter of every open triangle (entrapment band 89..230 mm must be avoided)
    P, Ed, Tr, h = lattice(); ds = []
    for f in Tr:
        a, b, c = (np.linalg.norm(P[f[i]] - P[f[(i+1) % 3]]) for i in range(3)); s = (a + b + c)/2; A = np.sqrt(max(s*(s-a)*(s-b)*(s-c), 0))
        ds.append(2*A/s - 2*RT)
    return dict(struts=len(Ed), min_open=round(min(ds), 3), max_open=round(max(ds), 3), entrapment_band_hits=int(sum(.089 <= x <= .23 for x in ds)), apex_h=round(float(P[-1][1] + RN), 3), fall_zone_past_dome=1.5)

VARIANTS = [
    dict(label="Leaf Crest: leaf shade panels on the top ring, leaf crest apex", dress="leaf"),
    dict(label="Court Line: ball finial, yellow panels, court-line rings", dress="court"),
    dict(label="Leaf Canopy: full leaf-panel shade cap, leaf-green frame", dress="canopy", frame=LF),
    dict(label="Garden Ring: planter troughs round the pad, leaf crest", dress="garden", frame=ST),
    dict(label="Court Holds: slate climbing panels with ball holds", dress="holds"),
]
if __name__ == "__main__":
    run("dome_climber", build, VARIANTS, title="climbing dome Ø 4.0 m, 110 struts, Ø 7 m fall-zone pad | nature + sports")
    o = openings(); print("OPEN", o); json.dump(o, open(os.path.join(RENDER_OUT, "dome_climber", "clearance.json"), "w"), indent=1)
