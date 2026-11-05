"""Rook: Tennis Tower E-terrace playground piece 8, parents' bench (spec §3.11.6 item 8: 6 benches; one module, instance x6) as a sculpted
2.6 x 1.8 m bench nook: 2.0 m bench (seat +0.42, 15° back to +0.85, slats with 25 mm gaps) set into a berm / hedge / canopy backdrop,
facing +Z (toward the play pieces). No wood (slats are HDPE / alloy / rubber), no planter boxes.
REUSE: #69 Riverbed (stone rubber, blue ribbon), #67 Meadow Hills (moss berm, flowers), #68 Forest Roots (bark rubber, mushrooms),
#61/#62 L3 alloy + slate slats, #63/#66 court line + ball finials, #65 leaf crest, toddler_landscape kit + balance_trail tufts. Run: python3 bench_nook.py"""
from modlib import *
import toddler_landscape as tl
from toddler_landscape import Scape, iso, RU, MOSS, TAN, RIV, BARK, SAND, STONE, HL, HS, Y, PAD, U
from balance_trail import tufts
from restroom_extras import crest
tl.HX, tl.HZ = 1.3, .9
SY, BZ, L = .42, -.22, 2.0; TILT = np.radians(15)
def bench(s, slat=HS, frame=ALY, top=None):
    s.add("Bench_Seat", slat, *[box(-L/2, L/2, SY - .04, SY, z0, z0 + .09) for z0 in np.arange(BZ, .24, .115)])
    F = []; B = []
    R = trimesh.transformations.rotation_matrix(TILT, [1, 0, 0])
    def back(m): m.apply_transform(R); m.apply_translation((0, SY, BZ)); return m
    for x in (-L/2 + .15, 0, L/2 - .15):
        F.append(box(x - .03, x + .03, PAD - E, SY - .04 + E, BZ - .02, .24 + .02))
        F.append(back(box(x - .03, x + .03, -.06, .45, -.06, 0)))
    for u in (.12, .25, .38): B.append(back(box(-L/2, L/2, u - .045, u + .045, -E, .025)))
    s.add("Bench_Frame", frame, *F); s.add("Bench_Back", slat, *B)
    tp = back(box(0, 0, .45, .45, 0, 0)).vertices.mean(0) if False else np.array([0, SY + .45*np.cos(TILT), BZ - .45*np.sin(TILT) - .03*np.cos(TILT)])
    if top == "ball": s.add("Ball_Finials", BA, *[node((x, tp[1] + .045 - E, tp[2]), .045, 0) for x in (-L/2 + .15, L/2 - .15)], col=None)
    if top == "leaf": s.add("Leaf_Crests", LF, *[crest((x, tp[1] - .004, tp[2])) for x in (-L/2 + .15, L/2 - .15)], col=None)
def berm(s, h=.75, rz=.28, z=-.6):
    s.mound(0, z, L/2 + .2, rz, h); s.mound(-1.15, -.5, .14, .34, h*.55); s.mound(1.15, -.5, .14, .34, h*.55)

def river(q):    # Riverbed Boulder Bench (#69)
    s = Scape(RU, STONE); bench(s, slat=STONE, frame=G); berm(s, .8)
    R = [box(-1.2, 1.2, PAD - .0015, PAD + .004, .45, .8)]; s.add("River_Ribbon", RIV, *R, col=None)
    s.pods([(-1.0, .62, .1, .08), (-.6, .7, .09, .1), (.7, .6, .1, .08), (1.05, .7, .08, .1)], STONE, part="River_Stones")
    s.cluster(0, -.6, 5, .22, seed=1, spread=.9); s.cluster(-1.15, -.5, 2, .14, seed=2, spread=.05); s.cluster(1.15, -.5, 2, .14, seed=3, spread=.05); tufts(s, 6, seed=1, keep=.15)
    return s.finish()
def meadow(q):   # Meadow Berm Bench (#67)
    s = Scape(RU, MOSS); bench(s, slat=HS, frame=SGM); berm(s, .7)
    s.flowers(0, -.6, 10, 1, .9); s.flowers(-1.15, -.5, 3, 2, .05); s.flowers(1.15, -.5, 3, 3, .05); s.cluster(-.6, -.7, 2, .2, seed=4, spread=.2); s.cluster(.6, -.7, 2, .2, seed=5, spread=.2); tufts(s, 8, seed=2, keep=.15)
    return s.finish()
def forest(q):   # Forest Roots Bench (#68)
    s = Scape(MOSS, RU); bench(s, slat=BARK, frame=BARK); berm(s, .65)
    st = [(-1.15, .45, .3), (1.15, .45, .25)]; sm = s.pods([(x, z, .07, h) for x, z, h in st], WH, part="Mushroom_Stems"); caps = []
    for m, (x, z, h) in zip(sm, st):
        c = node((0, 0, 0), .14, 1); c.vertices *= [1, .42, 1]; c.apply_translation((x, PAD + h + .06, z)); tl.drop([c], [m], emb=.003); caps.append(c)
    s.add("Mushroom_Caps", BA, *caps)
    s.cluster(0, -.6, 6, .24, seed=1, spread=.9); tufts(s, 8, seed=3, keep=.15)
    return s.finish()
def court(q):    # Court Line Bench (#61/#62 L3 alloy + slate)
    s = Scape(RU, MOSS); bench(s, slat=SSL, frame=ALY, top="ball")
    s.add("Court_Line", AM, box(-1.25, 1.25, PAD - .002, PAD + .002, .6, .65), *[box(x - .025, x + .025, PAD - .002, PAD + .002, -.85, .6 - E) for x in (-1.25, 1.25)], col=None)
    s.mound(0, -.72, L/2 + .2, .16, .35, mat=MOSS)
    for k, x in enumerate(np.linspace(-1.0, 1.0, 6)): s.bush(x, -.72, .2, LF if k % 2 else LF2, k)
    s.pods([(-1.12, .4, .1, .3), (1.12, .4, .1, .3)], BA, part="Ball_Side_Tables"); tufts(s, 6, seed=4, keep=.15)
    return s.finish()
def canopy(q):   # Leaf Canopy Bench (#65 leaf crest, #67 canopy tree)
    s = Scape(RU, TAN); bench(s, slat=HL, frame=SGM, top="leaf"); s.mound(-.65, -.7, .45, .18, .3); s.mound(.65, -.7, .45, .18, .3)
    h = 2.2; s.add("Tree_Trunk", ST, tube((0, PAD - E, -.75), (0, h, -.75), .09, 10), node((0, h, -.75), .13, 1))
    Lv = []
    for a in np.linspace(.2, np.pi - .2, 6):
        d = np.array([np.cos(a), .12, np.sin(a)]); d /= np.linalg.norm(d); Lv.append(leaf_dir(np.array((0, h, -.75)) + d*(.13 - .006), d, 1.05, .5, t=.025))
    Lv.append(crest((0, h + .13 - .006, -.75))); s.add("Tree_Canopy", LF, *Lv, col=None, solid=False)
    s.cluster(-.7, -.7, 2, .17, seed=1, spread=.15); s.cluster(.7, -.7, 2, .17, seed=2, spread=.15); s.flowers(-1.1, .5, 4, 3, .1); s.flowers(1.1, .5, 4, 4, .1); tufts(s, 6, seed=5, keep=.15)
    return s.finish()
B = dict(river=river, meadow=meadow, forest=forest, court=court, canopy=canopy)
def build(q): return B[q["c"]](q)
VARIANTS = [
    dict(c="river", label="Riverbed: stone-rubber bench in a boulder berm, river ribbon + pebbles"),
    dict(c="meadow", label="Meadow Berm: sand slats tucked into a flowering moss berm"),
    dict(c="forest", label="Forest Roots: bark-rubber bench, fern berm, mushroom side stools"),
    dict(c="court", label="Court Line: L3 alloy + slate slats, ball finials + tables, hedge"),
    dict(c="canopy", label="Leaf Canopy: leaf slats under a leaf-canopy tree, leaf crests"),
]
def sheet(rep):
    rdir = os.path.join(RENDER_OUT, "bench_nook"); fig, axs = plt.subplots(2, 5, figsize=(26, 10), facecolor="#F4F2EC")
    for i, (prm, r) in enumerate(zip(VARIANTS, rep)):
        p = recenter(build(prm)); _, geo = export_final(p.P, [f"/tmp/bn_{i}.glb"]); geo = {k: v for k, v in geo.items() if "colonly" not in k}
        for row, (el, az) in enumerate(((16, 25), (30, -40))):
            im = crop(render_view(geo, iso(el, az), size=720, shadow=True)); plt.imsave(os.path.join(rdir, f"v{i+1}_{'hero' if row == 0 else 'side'}.png"), np.clip(im, 0, 1))
            ax = axs[row, i]; ax.imshow(np.clip(im, 0, 1)); ax.axis("off")
            if row == 0: ax.set_title(f"v{i+1}  {prm['label'].split(': ')[0]}\n{prm['label'].split(': ')[1]}\n{r['tris']} tris | {'PASS' if r['passed'] else 'FAIL'}", fontsize=10, color="#222")
    fig.suptitle("Rook | Tennis Tower bench nook V1-V5 | 2.6 x 1.8 m module (x6), seat +0.42 | front 3/4 (top) + other front 3/4 (bottom)", fontsize=14, color="#333")
    plt.tight_layout(rect=(0, 0, 1, .95)); sp = os.path.join(rdir, "bench_nook_contact_sheet.png"); fig.savefig(sp, dpi=110, facecolor="#F4F2EC"); plt.close(fig); print("SHEET", sp)
if __name__ == "__main__":
    rep = run("bench_nook", build, VARIANTS, title="bench nook 2.6 x 1.8 m", view=iso(16, 25), sheet="bench_nook_run_sheet.png"); sheet(rep)
