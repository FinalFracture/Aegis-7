"""Rook: Tennis Tower E-terrace playground piece 6, 3 balance beams (spec §3.11.6 item 6) as a sculpted 8 x 5 m balance trail.
Each concept: 3 distinct low beams (top 0.15..0.45 m, 0.12-0.15 m wide, HDPE/rubber on short posts, gentle pitch <= 6°) threaded through
rubber berms/hummocks, foliage + flower clusters and theme props, so the zone reads layered and dense (lesson from the #67 round-1 rejection).
REUSE: #67 toddler_landscape kit (Scape: mounds, pods, path, tree, panels, foliage drop, colliders), #63/#66 court line + ball pods,
#65 leaf crest, play_tower materials. No wood, no planter boxes, nothing spinning. Run: python3 balance_trail.py"""
from modlib import *
import toddler_landscape as tl
from toddler_landscape import Scape, iso, RU, MOSS, TAN, RIV, BARK, SAND, STONE, HL, HS, Y, PAD, U
from restroom_extras import crest
tl.HX, tl.HZ = 4.0, 2.5
def beam(s, pts, mat, w=.14, th=.1, post=SGM, part="Balance_Beam", finial=None):
    seg = []
    for (x0, z0, y0), (x1, z1, y1) in zip(pts, pts[1:]):
        L = np.hypot(x1 - x0, z1 - z0); m = box(-L/2 - .04, L/2 + .04, -th, 0, -w/2, w/2)
        m.apply_transform(trimesh.transformations.rotation_matrix(np.arctan2(y1 - y0, L), [0, 0, 1])); m.apply_transform(Y(-np.arctan2(z1 - z0, x1 - x0)))
        m.apply_translation(((x0 + x1)/2, (y0 + y1)/2, (z0 + z1)/2)); seg.append(m)
    s.add(part, mat, *seg)
    P = [box(x - .03, x + .03, PAD - E, y - th + .0045, z - .03, z + .03) for x, z, y in pts]
    s.add(part + "_Posts", post, *P)
    if finial == "ball": s.add(part + "_Finials", BA, *[node((x, y + .05 - E, z), .05, 0) for x, z, y in (pts[0], pts[-1])], col=None)
    if finial == "leaf": s.add(part + "_Crests", LF, *[crest((x, y - .004, z)) for x, z, y in (pts[0], pts[-1])], col=None)
def tufts(s, n, seed=0, mats=(LF, LF2), keep=.3):  # dense grass/fern tufts on open ground (clear of every solid footprint)
    for a, k in s.SQ: s._slide(*a, **k)
    s.SQ = []; rng = np.random.default_rng(seed); placed = 0; tries = 0
    S = [m for m in s.solid if m is not s.pad]
    while placed < n and tries < 4000:
        tries += 1; x, z = rng.uniform(-tl.HX + .25, tl.HX - .25), rng.uniform(-tl.HZ + .25, tl.HZ - .25)
        if any(m.bounds[0][0] - keep < x < m.bounds[1][0] + keep and m.bounds[0][2] - keep < z < m.bounds[1][2] + keep and (m.bounds[1][0] - m.bounds[0][0]) * (m.bounds[1][2] - m.bounds[0][2]) < 1.5 for m in S): continue
        if any(m.contains([[x, PAD + .01, z]])[0] for m in S if m.is_watertight and m.bounds[0][0] < x < m.bounds[1][0] and m.bounds[0][2] < z < m.bounds[1][2]): continue
        if any(trimesh.proximity.closest_point(m, [[x, PAD, z]])[1][0] < keep for m in S if m.bounds[0][0] - 1 < x < m.bounds[1][0] + 1 and m.bounds[0][2] - 1 < z < m.bounds[1][2] + 1): continue
        if any(np.hypot(x - c.centroid[0], z - c.centroid[2]) < (c.bounds[1][0] - c.bounds[0][0])/2 + keep for c, _ in s.Q): continue
        h = rng.uniform(.22, .4); L = []
        for k in range(5):
            a = 2*np.pi*k/5 + rng.uniform(0, 1); d = np.array([np.cos(a)*.45, 1, np.sin(a)*.45])
            L.append(leaf_dir((x, PAD - .003, z), d, h, .07, t=.008))
        s.add("Grass_Tufts", mats[placed % len(mats)], *L, col=None, solid=False); s.solid_tuft = True; placed += 1
def wavy(x0, x1, z, n, az, h0, h1, ph=0):
    return [(x, z + az*np.sin(ph + 2.4*np.pi*k/(n - 1)), h0 + (h1 - h0)*np.sin(np.pi*k/(n - 1))) for k, x in enumerate(np.linspace(x0, x1, n))]
def zig(x0, x1, z, n, az, h0, h1):
    return [(x, z + (az if k % 2 else -az), h0 + (h1 - h0)*np.sin(np.pi*k/(n - 1))) for k, x in enumerate(np.linspace(x0, x1, n))]
def arc(cx, cz, r, a0, a1, n, h0, h1):
    return [(cx + r*np.cos(a), cz + r*np.sin(a), h0 + (h1 - h0)*np.sin(np.pi*k/(n - 1))) for k, a in enumerate(np.linspace(a0, a1, n))]

def meadow(q):   # Meadow Ridge (#67 Meadow Hills language)
    s = Scape(RU, MOSS)
    beam(s, wavy(-3.0, 3.0, -1.6, 9, .25, .15, .4), HL, finial="leaf"); beam(s, zig(-2.6, 2.6, 0, 7, .3, .2, .45), HS, finial="leaf"); beam(s, arc(0, 3.6, 2.6, -2.3, -.85, 7, .15, .35), HL, finial="leaf")
    for x, z, rx, rz, h in [(-3.55, -.2, .4, 1.1, .5), (3.55, .1, .4, 1.2, .55), (-1.2, -.8, 1.0, .25, .22), (1.4, -.8, 1.0, .25, .25), (-3.0, 1.75, .6, .45, .3), (3.0, 1.8, .6, .45, .32), (0, -2.25, 1.6, .2, .18)]: s.mound(x, z, rx, rz, h)
    s.cluster(-3.55, -.3, 4, .26, seed=1); s.cluster(3.55, .2, 4, .26, seed=2); s.cluster(-2.7, 1.7, 3, .22, seed=3); s.cluster(2.9, 1.8, 3, .22, seed=4)
    s.flowers(-1.2, -.8, 6, 5, .7); s.flowers(1.4, -.8, 6, 6, .7); s.flowers(0, 1.9, 6, 7, .5); s.flowers(0, -2.2, 6, 8, 1.2)
    tufts(s, 34, seed=10)
    return s.finish()
def court(q):    # Court Line Trail (#63/#66 court-line + ball language)
    s = Scape(RU, MOSS)
    beam(s, [(-3.0, -1.6, .2), (-1.0, -1.6, .3), (1.0, -1.6, .3), (3.0, -1.6, .2)], WH, finial="ball")
    beam(s, [(-2.4, .1, .2), (-.8, .1, .3), (-.8, 1.4, .4), (.8, 1.4, .4), (.8, .1, .3), (2.4, .1, .2)], WH, finial="ball")
    beam(s, zig(-2.2, 2.2, -.75, 6, .18, .15, .3), BA, finial="ball")
    s.add("Court_Line", AM, *[box(-3.9, 3.9, PAD - .002, PAD + .002, z - .025, z + .025) for z in (-2.35, 2.35)], *[box(x - .025, x + .025, PAD - .002, PAD + .002, -2.325, 2.325) for x in (-3.85, 3.85)], col=None)
    s.mound(-3.2, 1.6, .55, .5, .45, part="Ball_Mounds", mat=BA); s.mound(3.2, 1.6, .55, .5, .45, part="Ball_Mounds", mat=BA)
    for x, z, rx, rz, h in [(0, 2.1, 1.4, .3, .25), (-3.4, -.4, .35, .9, .3), (3.4, -.4, .35, .9, .3), (0, -2.2, 2.2, .18, .16)]: s.mound(x, z, rx, rz, h)
    s.pods([(-1.6, .85, .16, .14), (-1.9, 1.5, .16, .2), (1.6, .85, .16, .14), (1.9, 1.5, .16, .2), (0, .55, .18, .16)], BA, part="Ball_Pods")
    s.cluster(-3.4, -.4, 3, .22, seed=1); s.cluster(3.4, -.4, 3, .22, seed=2); s.flowers(0, 2.1, 8, 3, 1.1, mats=(BA, WH)); s.cluster(0, -2.2, 5, .16, seed=4, spread=1.8)
    tufts(s, 34, seed=9)
    return s.finish()
def river(q):    # Riverbed Crossing
    s = Scape(RU, MOSS)
    C = [(-1.0, -1.95), (-.4, -1.2), (-1.0, 0), (-.2, 1.2), (-.8, 1.95)]; R = []
    for k, ((x0, z0), (x1, z1)) in enumerate(zip(C, C[1:])):
        L = np.hypot(x1 - x0, z1 - z0); m = box(-L/2 - .02, L/2 + .02, PAD - .0015, PAD + .004 + .0012*(k % 2), -.55, .55); m.apply_transform(Y(-np.arctan2(z1 - z0, x1 - x0))); m.apply_translation(((x0 + x1)/2, 0, (z0 + z1)/2)); R.append(m)
    s.add("River_Ribbon", RIV, *R, col=None)
    beam(s, wavy(-3.0, 2.6, -1.7, 8, .15, .2, .45), STONE, post=ST); beam(s, [(-2.8, .3, .18), (-1.6, .1, .28), (-.6, .4, .38), (.6, .2, .3), (1.8, .5, .2)], STONE, post=ST); beam(s, arc(-.5, 3.4, 2.0, -2.6, -.6, 6, .15, .35), HS, post=ST)
    for x, z, rx, rz, h in [(-3.3, 1.5, .6, .8, .45), (3.3, -.3, .6, 1.6, .6), (-3.4, -1.0, .45, .5, .3), (2.2, 1.9, .9, .45, .3), (1.6, -.6, .5, .35, .2)]: s.mound(x, z, rx, rz, h)
    s.pods([(-.7, -.6, .17, .1), (-.55, .75, .17, .12), (-.5, 1.9, .17, .1)], STONE, part="River_Stones")
    s.cluster(3.3, -.3, 5, .26, seed=1); s.cluster(-3.3, 1.5, 3, .24, seed=2); s.cluster(2.2, 1.9, 3, .2, seed=3); s.flowers(1.6, -.6, 5, 4, .4); s.flowers(-3.4, -1.0, 4, 5, .3)
    tufts(s, 34, seed=9)
    return s.finish()
def forest(q):   # Forest Roots
    s = Scape(MOSS, RU)
    beam(s, wavy(-3.0, -.6, -1.5, 7, .35, .15, .4, ph=.5), BARK, post=BARK, part="Root_Beam"); beam(s, wavy(.6, 3.0, -1.4, 7, .35, .2, .42, ph=2), BARK, post=BARK, part="Root_Beam_B")
    beam(s, arc(0, 0, 1.25, .3, np.pi - .3, 7, .2, .4), BARK, post=BARK, part="Root_Beam_C")
    s.tree(0, -.2, 2.6, 7, LF)
    for x, z, rx, rz, h in [(-3.3, 1.2, .6, 1.0, .5), (3.3, 1.2, .6, 1.0, .45), (0, -2.15, .5, .3, .25), (-1.9, 1.9, .7, .4, .25), (1.9, 1.9, .7, .4, .25)]: s.mound(x, z, rx, rz, h)
    st = [(-1.0, -.55, .2), (-.5, -.85, .3), (.5, -.85, .3), (1.0, -.55, .2)]; sm = s.pods([(x, z, .08, h) for x, z, h in st], WH, part="Mushroom_Stems"); caps = []
    for m, (x, z, h) in zip(sm, st):
        c = node((0, 0, 0), .22, 1); c.vertices *= [1, .42, 1]; c.apply_translation((x, PAD + h + .08, z)); tl.drop([c], [m], emb=.003); caps.append(c)
    s.add("Mushroom_Caps", BA, *caps)
    s.cluster(-3.3, 1.2, 5, .28, seed=1); s.cluster(3.3, 1.2, 5, .28, seed=2); s.cluster(-1.9, 1.9, 3, .2, seed=3); s.cluster(1.9, 1.9, 3, .2, seed=4)
    s.flowers(0, 2.0, 6, 5, .5, mats=(WH, BA)); s.cluster(-3.5, -1.9, 3, .22, seed=6); s.cluster(3.5, -1.9, 3, .22, seed=7)
    tufts(s, 34, seed=10)
    return s.finish()
def leafcrest(q):  # Leaf Crest Hedgerow
    s = Scape(RU, TAN)
    beam(s, zig(-3.0, 3.0, -1.5, 9, .22, .15, .4), HL, finial="leaf"); beam(s, wavy(-2.6, 2.6, .1, 8, .3, .2, .45, ph=1), HL, finial="leaf"); beam(s, [(-2.6, 1.6, .15), (-1.4, 1.5, .25), (-.4, 1.75, .3), (.6, 1.5, .3), (1.6, 1.75, .25), (2.6, 1.6, .15)], HS, finial="leaf")
    for x, z, rx, rz, h in [(-3.6, 0, .32, 1.9, .4), (3.6, 0, .32, 1.9, .4), (0, -2.25, 3.0, .2, .2), (0, 2.25, 3.0, .2, .2), (-.2, -.75, .8, .25, .2), (.3, .95, .6, .22, .18)]: s.mound(x, z, rx, rz, h)
    for k, x in enumerate(np.linspace(-3.4, 3.4, 9)): s.bush(x, -2.25, .24, LF if k % 2 else LF2, k); s.bush(x + .2, 2.25, .22, LF2 if k % 2 else LF, k + 20)
    s.cluster(-3.6, 0, 4, .24, seed=1); s.cluster(3.6, 0, 4, .24, seed=2); s.flowers(-.2, -.75, 5, 3, .5); s.flowers(.3, .95, 5, 4, .4)
    tufts(s, 34, seed=13)
    return s.finish()
B = dict(meadow=meadow, court=court, river=river, forest=forest, leaf=leafcrest)
def build(q): return B[q["c"]](q)
VARIANTS = [
    dict(c="meadow", label="Meadow Ridge: wavy, zig-zag + arc leaf beams between moss berms"),
    dict(c="court", label="Court Line Trail: white baseline + service-T beams, ball beam + pods"),
    dict(c="river", label="Riverbed Crossing: stone beams over a blue river, bank hills"),
    dict(c="forest", label="Forest Roots: bark-rubber root beams round a canopy tree"),
    dict(c="leaf", label="Leaf Crest Hedgerow: 3 leaf beams in a hedge-lined corridor"),
]
def sheet(rep):
    rdir = os.path.join(RENDER_OUT, "balance_trail"); fig, axs = plt.subplots(2, 5, figsize=(26, 10), facecolor="#F4F2EC")
    for i, (prm, r) in enumerate(zip(VARIANTS, rep)):
        p = recenter(build(prm)); _, geo = export_final(p.P, [f"/tmp/bt_{i}.glb"]); geo = {k: v for k, v in geo.items() if "colonly" not in k}
        for row, (el, az) in enumerate(((18, 25), (32, 200))):
            im = crop(render_view(geo, iso(el, az), size=720, shadow=True)); plt.imsave(os.path.join(rdir, f"v{i+1}_{'hero' if row == 0 else 'back'}.png"), np.clip(im, 0, 1))
            ax = axs[row, i]; ax.imshow(np.clip(im, 0, 1)); ax.axis("off")
            if row == 0: ax.set_title(f"v{i+1}  {prm['label'].split(': ')[0]}\n{prm['label'].split(': ')[1]}\n{r['tris']} tris | {'PASS' if r['passed'] else 'FAIL'}", fontsize=11, color="#222")
    fig.suptitle("Rook | Tennis Tower balance trail V1-V5 | 3 beams, 8 x 5 m, beam tops 0.15-0.45 m | front 3/4 (top) + back 3/4 (bottom)", fontsize=14, color="#333")
    plt.tight_layout(rect=(0, 0, 1, .95)); sp = os.path.join(rdir, "balance_trail_contact_sheet.png"); fig.savefig(sp, dpi=110, facecolor="#F4F2EC"); plt.close(fig); print("SHEET", sp)
if __name__ == "__main__":
    rep = run("balance_trail", build, VARIANTS, title="3 balance beams, 8 x 5 m", view=iso(18, 25), sheet="balance_trail_run_sheet.png"); sheet(rep)
