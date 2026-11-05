"""Rook: Tennis Tower E-terrace playground poured-rubber surface (spec §3.11.6 item 9: poured-rubber surface in 3 colours, decals),
as 6 x 6 m tileable surface tiles. 3 colours = base pad + inlay layer L1 + inlay layer L2, built as stepped inlays (no z-fighting):
base pad top +0.030 | L1 +0.0265..+0.034 | L2 +0.0285..+0.038 (L2 always 4 mm above L1, embedded 1.5-3.5 mm; every layer is one unioned part,
so no coplanar faces). Low rubber humps (0.08-0.14 m, toddler bumps) give relief; decals are clipped clear of them.
Each concept matches a promoted winner: #67 Meadow Hills, #68 Forest Roots, #69 Riverbed, #71 Court Line, #70 Leaf Canopy.
REUSE: toddler_landscape kit (Scape pad, mounds, zone collider), winners' rubber colours. Run: python3 surface.py"""
from modlib import *
import sys
import modlib, toddler_landscape as tl
from toddler_landscape import Scape, iso, RU, MOSS, TAN, RIV, BARK, STONE, PAD
from shapely.geometry import Point, LineString, Polygon, box as sbox
from shapely.ops import unary_union
from shapely import affinity
modlib._m("tt_rubber_leaf", "TT_PlayRubber_Leaf", (.47, .66, .36), 0, .9); modlib._m("tt_rubber_sun", "TT_PlayRubber_Sun", (.86, .76, .30), 0, .9)
modlib._m("tt_rubber_cream", "TT_PlayRubber_Cream", (.86, .83, .72), 0, .9); modlib._m("tt_rubber_slate", "TT_PlayRubber_Slate", (.26, .29, .34), 0, .9)
modlib._m("tt_rubber_white", "TT_PlayRubber_LineWhite", (.86, .87, .85), 0, .8)
LEAFR, SUN, CREAM, SLATE, WHITE = "tt_rubber_leaf", "tt_rubber_sun", "tt_rubber_cream", "tt_rubber_slate", "tt_rubber_white"
tl.HX = tl.HZ = 3.0
LAY = {1: (PAD - .0035, PAD + .004), 2: (PAD - .0015, PAD + .008)}
def lens(x, z, L, w, a, n=10):
    t = np.linspace(0, 1, n); up = [(L*u, w/2*np.sin(np.pi*u)) for u in t]; dn = [(L*u, -w/2*np.sin(np.pi*u)) for u in t[::-1][1:-1]]
    return affinity.translate(affinity.rotate(Polygon(up + dn), a, origin=(0, 0), use_radians=True), x, z)
def flower(x, z, r):
    return unary_union([Point(x + r*np.cos(a), z + r*np.sin(a)).buffer(r*.7, 2) for a in np.linspace(0, 2*np.pi, 5, endpoint=False)] + [Point(x, z).buffer(r*.6, 2)])
def ring(x, z, r, w): return Point(x, z).buffer(r, 16).difference(Point(x, z).buffer(r - w, 16))
class Surf:
    def __init__(s, base, hump_mat):
        s.s = Scape(base, hump_mat); s.keep = sbox(-2.99, -2.99, 2.99, 2.99); s.humps = []; s.L = {1: [], 2: []}
    def hump(s, x, z, rx, rz, h):
        s.s.mound(x, z, rx, rz, h); s.humps.append(affinity.scale(Point(x, z).buffer(1, 24), rx + .06, rz + .06))
    def lay(s, layer, geom, part, mat):
        g = unary_union(geom).intersection(s.keep)
        for hp in s.humps: g = g.difference(hp)
        if layer == 2 and s.L[1]: pass
        s.L[layer].append(g); polys = [g] if g.geom_type == "Polygon" else list(getattr(g, "geoms", []))
        y0, y1 = LAY[layer]; ms = []
        for pg in polys:
            if pg.geom_type != "Polygon" or pg.area < 1e-4: continue
            pg = Polygon([(x, -z) for x, z in pg.exterior.coords], [[(x, -z) for x, z in r.coords] for r in pg.interiors]).buffer(0)
            m = trimesh.creation.extrude_polygon(pg, y1 - y0); m.apply_transform(trimesh.transformations.rotation_matrix(-np.pi/2, [1, 0, 0])); m.apply_translation((0, y0, 0)); ms.append(m)
        s.s.add(part, mat, *ms, col=None, solid=False)
    def finish(s): return s.s.finish()

def meadow(q):    # #67 Meadow Hills
    S = Surf(MOSS, MOSS)
    for x, z, rx, rz, h in [(-1.6, -1.4, .7, .55, .12), (1.5, .9, .6, .5, .1), (-.6, 1.9, .45, .4, .08)]: S.hump(x, z, rx, rz, h)
    S.lay(1, [affinity.scale(Point(x, z).buffer(1, 8), a, b) for x, z, a, b in [(.8, -1.6, 1.6, .8), (-1.9, .9, 1.0, 1.4), (1.9, 2.3, 1.2, .6), (-.2, .1, 1.1, .7)]], "Meadow_Inlay", LEAFR)
    rng = np.random.default_rng(1)
    S.lay(2, [flower(*rng.uniform(-2.8, 2.8, 2), rng.uniform(.08, .14)) for _ in range(26)], "Flower_Inlay", SUN)
    return S.finish()
def forest(q):    # #68 Forest Roots
    S = Surf(MOSS, BARK)
    for x, z, rx, rz, h in [(-1.9, 1.8, .5, .45, .1), (1.9, -1.9, .55, .45, .12)]: S.hump(x, z, rx, rz, h)
    roots = [LineString([(-3, -.4), (-1.6, -.1), (-.3, -.6), (1.0, -.2), (3, -.8)]).buffer(.13, 6), LineString([(-1.6, -.1), (-1.9, -1.6), (-1.4, -3)]).buffer(.09, 6),
             LineString([(1.0, -.2), (1.6, 1.0), (1.2, 2.2), (1.7, 3)]).buffer(.09, 6), LineString([(-.3, -.6), (-.6, .9), (-1.0, 3)]).buffer(.07, 6), LineString([(1.0, -.2), (2.2, -1.0)]).buffer(.06, 6)]
    S.lay(1, roots, "Root_Inlay", BARK)
    rng = np.random.default_rng(2); prints = []
    for _ in range(14):
        x, z = rng.uniform(-2.7, 2.7, 2); prints.append(lens(x, z, rng.uniform(.3, .45), .16, rng.uniform(0, 6.28)))
    S.lay(2, prints + [Point(x, z).buffer(r, 12) for x, z, r in [(-2.3, -1.6, .16), (.4, 1.7, .14), (2.4, .9, .18), (-.4, -2.2, .13)]], "Leafprint_Inlay", CREAM)
    return S.finish()
def river(q):     # #69 Riverbed
    S = Surf(RU, RU)
    for x, z, rx, rz, h in [(-2.0, -2.0, .55, .5, .12), (2.0, 1.9, .6, .5, .1)]: S.hump(x, z, rx, rz, h)
    rv = LineString([(-3, .6), (-1.8, -.2), (-.4, .4), (.8, -.5), (2.0, .1), (3, -.6)]).buffer(.55, 8)
    S.lay(1, [rv, Point(-.4, -1.9).buffer(.7, 20)], "River_Inlay", RIV)
    stones = [affinity.scale(Point(x, z).buffer(1, 12), .22, .15) for x, z in [(-2.2, .25), (-1.3, -.05), (-.4, .4), (.5, -.3), (1.4, -.15), (2.4, -.2), (-.6, -1.9), (-.1, -1.6)]]
    rng = np.random.default_rng(3); peb = [Point(*rng.uniform(-2.8, 2.8, 2)).buffer(rng.uniform(.05, .09), 8) for _ in range(30)]
    S.lay(2, stones + [p for p in peb if not p.intersects(rv.buffer(.05))], "Stone_Inlay", STONE)
    return S.finish()
def wrap(g, P=6.0):  # periodic copies so anything crossing an edge re-enters on the opposite edge
    return unary_union([affinity.translate(g, dx, dz) for dx in (-P, 0, P) for dz in (-P, 0, P)])
def river_seamless(q):  # #72: V3 Riverbed made periodic (6 m in X and Z): river z(x) has period 6, stones/pebbles wrapped, humps interior
    S = Surf(RU, RU); S.keep = sbox(-2.9985, -2.9985, 2.9985, 2.9985)
    for x, z, rx, rz, h in [(-1.9, -2.0, .5, .45, .12), (1.9, 1.9, .55, .45, .1)]: S.hump(x, z, rx, rz, h)
    f = lambda x: .25 + .55*np.sin(2*np.pi*x/6) + .2*np.sin(4*np.pi*x/6 + .7)
    xs = np.linspace(-4.5, 4.5, 37); rv = LineString([(x, f(x)) for x in xs]).buffer(.5, 6)
    pool = Point(-.2, -1.85).buffer(.62, 10)
    S.lay(1, [rv, pool], "River_Inlay", RIV)
    st = [affinity.scale(Point(x, f(x) + (.12 if k % 2 else -.12)).buffer(1, 6), .21, .14) for k, x in enumerate(np.arange(-3.0, 3.0, .75))] + [affinity.scale(Point(-.35, -1.9).buffer(1, 6), .2, .14), affinity.scale(Point(.1, -1.65).buffer(1, 6), .18, .12)]
    rng = np.random.default_rng(3); peb = []
    while len(peb) < 26:
        p = Point(*rng.uniform(-3, 3, 2)).buffer(rng.uniform(.05, .08), 3)
        if not wrap(p).intersects(rv.buffer(.06)) and not p.intersects(pool.buffer(.06)) and not any(p.intersects(h.buffer(.04)) for h in S.humps) and not any(p.buffer(.03).intersects(q2) for q2 in peb): peb.append(p)
    S.lay(2, [wrap(unary_union(st))] + [wrap(unary_union(peb))], "Stone_Inlay", STONE)
    return S.finish()
def court(q):     # #71 Court Line
    S = Surf(RU, RU)
    S.hump(-2.3, 2.3, .4, .35, .1); S.hump(2.3, -2.3, .4, .35, .1)
    ct = sbox(-2.3, -1.2, 2.3, 1.2); hop = unary_union([sbox(-.25 + dx, 1.6 + dz, .25 + dx, 2.1 + dz) for dx, dz in [(0, 0), (-.27, .52), (.27, .52), (0, 1.04)]])
    hop = affinity.translate(affinity.rotate(hop, 90, origin=(0, 2.1)), 1.2, -.1)
    S.lay(1, [ct, hop], "Court_Inlay", SLATE)
    lines = [ct.buffer(-.04, join_style=2).exterior.buffer(.025, 2), sbox(-.025, -1.2, .025, 1.2), sbox(-1.5, -.025, 1.5, .025).difference(sbox(-.03, -.03, .03, .03)) if False else sbox(-1.5, -.02, 1.5, .02),
             sbox(-1.525, -1.17, -1.475, 1.17), sbox(1.475, -1.17, 1.525, 1.17), ring(-2.0, 1.95, .3, .05), ring(2.0, -1.95, .28, .05)]
    S.lay(2, lines + [hop.boundary.buffer(.025, 2)], "Line_Inlay", WHITE)
    return S.finish()
def canopy(q):    # #70 Leaf Canopy
    S = Surf(TAN, MOSS)
    for x, z, rx, rz, h in [(2.1, 2.1, .5, .45, .1), (-2.2, -.2, .45, .4, .08)]: S.hump(x, z, rx, rz, h)
    leaves = [lens(x, z, L, w, a) for x, z, L, w, a in [(-2.6, -2.4, 2.6, .9, .6), (-.5, 2.6, 2.4, .8, -1.0), (.3, -1.6, 2.4, .85, .25), (-1.4, .9, 1.8, .6, -.3)]]
    S.lay(1, leaves, "Leaf_Inlay", LEAFR)
    vein = []
    for x, z, L, w, a in [(-2.6, -2.4, 2.6, .9, .6), (-.5, 2.6, 2.4, .8, -1.0), (.3, -1.6, 2.4, .85, .25), (-1.4, .9, 1.8, .6, -.3)]:
        mid = affinity.translate(affinity.rotate(sbox(.15, -.02, L - .2, .02), a, origin=(0, 0), use_radians=True), x, z); vein.append(mid)
        for u in (.3, .5, .7):
            br = affinity.translate(affinity.rotate(affinity.rotate(sbox(0, -.015, w*.38, .015), .9, origin=(0, 0), use_radians=True), a, origin=(0, 0), use_radians=True), x + L*u*np.cos(a), z + L*u*np.sin(a))
            br2 = affinity.translate(affinity.rotate(affinity.rotate(sbox(0, -.015, w*.38, .015), -.9, origin=(0, 0), use_radians=True), a, origin=(0, 0), use_radians=True), x + L*u*np.cos(a), z + L*u*np.sin(a)); vein += [br, br2]
    rng = np.random.default_rng(5); dap = [Point(*rng.uniform(-2.8, 2.8, 2)).buffer(rng.uniform(.06, .12), 10) for _ in range(30)]
    S.lay(2, [unary_union(vein).intersection(unary_union(leaves).buffer(-.04))] + [d for d in dap if not d.intersects(unary_union(leaves))], "Vein_Inlay", MOSS)
    return S.finish()
B = dict(river_seamless=river_seamless, meadow=meadow, forest=forest, river=river, court=court, canopy=canopy)
def build(q): return B[q["c"]](q)
VARIANTS = [
    dict(c="meadow", label="Meadow Hills: moss base, leaf meadow drifts, sun flowers, 3 humps"),
    dict(c="forest", label="Forest Roots: moss base, bark root network, cream leaf prints + caps"),
    dict(c="river", label="Riverbed: green base, blue river + pool, stepping stones, pebbles"),
    dict(c="court", label="Court Line: green base, slate mini-court + hopscotch, white lines"),
    dict(c="canopy", label="Leaf Canopy: tan base, giant leaf inlays with veins, dappled light"),
]
def sheet(rep):
    rdir = os.path.join(RENDER_OUT, "surface"); fig, axs = plt.subplots(2, 5, figsize=(26, 11), facecolor="#F4F2EC")
    for i, (prm, r) in enumerate(zip(VARIANTS, rep)):
        p = recenter(build(prm)); _, geo = export_final(p.P, [f"/tmp/su_{i}.glb"]); geo = {k: v for k, v in geo.items() if "colonly" not in k}
        for row, (el, az) in enumerate(((24, 30), (62, 0))):
            im = crop(render_view(geo, iso(el, az), size=760, shadow=True)); plt.imsave(os.path.join(rdir, f"v{i+1}_{'low' if row == 0 else 'high'}.png"), np.clip(im, 0, 1))
            ax = axs[row, i]; ax.imshow(np.clip(im, 0, 1)); ax.axis("off")
            if row == 0: ax.set_title(f"v{i+1}  {prm['label'].split(': ')[0]}\n{prm['label'].split(': ')[1]}\n{r['tris']} tris | {'PASS' if r['passed'] else 'FAIL'}", fontsize=10, color="#222")
    fig.suptitle("Rook | Tennis Tower playground poured-rubber surface V1-V5 | 6 x 6 m tile, 3 colours (stepped inlays) | low 3/4 (top) + high 3/4 (bottom)", fontsize=14, color="#333")
    plt.tight_layout(rect=(0, 0, 1, .95)); sp = os.path.join(rdir, "surface_contact_sheet.png"); fig.savefig(sp, dpi=110, facecolor="#F4F2EC"); plt.close(fig); print("SHEET", sp)
def tiled():
    rep = run("surface", build, [dict(c="river_seamless", label="#72 Riverbed seamless: 6 m periodic river, wrapped stones + pebbles")], names=["final"], suffix="_final", view=iso(24, 30), sheet="surface_final_sheet.png", title="#72 final")
    A = Part()
    for k, (dx, dz) in enumerate([(-3, -3), (3, -3), (-3, 3), (3, 3)]):
        p = recenter(build(dict(c="river_seamless")))
        for n, (mk, m) in p.P.items():
            if "colonly" in n: continue
            m = m.copy(); m.apply_translation((dx, 0, dz)); A.add(f"{n}_{k}", mk, m)
    _, geo = export_final(A.P, ["/tmp/su_tiled.glb"]); rdir = os.path.join(RENDER_OUT, "surface")
    fig, axs = plt.subplots(1, 2, figsize=(22, 11), facecolor="#F4F2EC")
    for ax, (el, az), t in zip(axs, ((90, 0), (28, 30)), ("top (seams at x = 0, z = 0)", "low 3/4")):
        im = crop(render_view(geo, iso(el, az), size=1100, shadow=True)); ax.imshow(np.clip(im, 0, 1)); ax.axis("off"); ax.set_title(t, fontsize=13)
    fig.suptitle(f"Rook | #72 tt_play_surface (Riverbed, seamless) | 2 x 2 tiled = 12 x 12 m | {rep[0]['tris']} tris per tile | {'PASS' if rep[0]['passed'] else 'FAIL'}", fontsize=15, color="#333")
    plt.tight_layout(rect=(0, 0, 1, .94)); sp = os.path.join(rdir, "surface_2x2_tiled_sheet.png"); fig.savefig(sp, dpi=100, facecolor="#F4F2EC"); plt.close(fig); print("TILED", sp)
if __name__ == "__main__" and sys.argv[1:] == ["final"]: tiled()
elif __name__ == "__main__":
    rep = run("surface", build, VARIANTS, title="poured-rubber surface", view=iso(24, 30), sheet="surface_run_sheet.png"); sheet(rep)
