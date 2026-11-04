"""Rook: Tennis Tower E-terrace playground piece 7, soft-play pit 6 x 6 m (spec §3.11.6 item 7) as a sculpted, enclosed soft landscape.
Each concept: cushion berms 0.45-0.6 m all round (one 1.2 m entry gap, +Z), a ball pit (rubber rim, bed + one layer of r 0.07 balls on a
hex grid), foam hills / rollers / steps / wedges inside, foliage, tufts and theme props. Fall heights <= 0.9 m, no gaps in the 89-230 mm
band, nothing spinning (rollers are fixed), no wood, no planter boxes.
REUSE: #67 toddler_landscape kit (Scape: mounds, tunnel, slide, pods, tree, panels, foliage), #68 Forest Roots (bark rubber, mushrooms,
canopy tree) + balance_trail tufts/beams, #63/#66 court line + ball language, #65 leaf crest. Run: python3 soft_play.py"""
from modlib import *
import toddler_landscape as tl
from toddler_landscape import Scape, iso, RU, MOSS, TAN, RIV, BARK, SAND, STONE, HL, HS, Y, PAD, U
from balance_trail import tufts, beam, wavy, arc
tl.HX, tl.HZ = 3.0, 3.0
def walls(s, h=.55, gap=1.2):
    for x, z, rx, rz in [(0, -2.68, 2.9, .3), (-2.68, -.1, .3, 2.7), (2.68, -.1, .3, 2.7)]: s.mound(x, z, rx, rz, h)
    w = (5.8 - gap)/4; s.mound(-gap/2 - w, 2.68, w + .05, .3, h*.85); s.mound(gap/2 + w, 2.68, w + .05, .3, h*.85)
def ballpit(s, x, z, r, rim=TAN, mats=(BA, WH, HL)):
    rm = trimesh.creation.annulus(r, r + .18, .4, sections=24); rm.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0])); rm.apply_translation((x, PAD - E + .2, z))
    s.add("Pit_Rim", rim, rm, col="mesh"); bed = cap((x, PAD - .002 + .08, z), r + E, .16, 24, axis="y"); s.add("Pit_Bed", SAND, bed)
    yb = PAD - .002 + .16; d = .148; B = {m: [] for m in mats}; k = 0
    for i in range(-12, 13):
        for j in range(-12, 13):
            px, pz = x + d*(i + .5*(j % 2)), z + d*j*np.sqrt(3)/2
            if np.hypot(px - x, pz - z) < r - .085: B[mats[k % len(mats)]].append(node((px, yb + .07 - E, pz), .07, -1)); k += 1
    for m, ms in B.items():
        if ms: s.add(f"Pit_Balls_{m.split('_')[-1].title()}", m, *ms, col=None)
def roller(s, x0, x1, z, r=.16, mat=HL, part="Foam_Rollers"):
    s.add(part, mat, tube((x0, PAD - E + r, z), (x1, PAD - E + r, z), r, 12))
def steps(s, x, z, yaw, n, mat=HS, w=.8, part="Foam_Steps"):
    ms = []
    for k in range(n):
        m = box(-w/2 + k*.004, w/2 - k*.004, PAD - E, .15*(k + 1), -.2 - .3*(n - 1 - k), .2 + .3*k*0 + .002*k); m.apply_transform(Y(yaw)); m.apply_translation((x, 0, z)); ms.append(m)
    s.add(part, mat, *ms)

def forest(q):   # Forest Floor soft-play (#68 Forest Roots language)
    s = Scape(MOSS, RU); walls(s)
    ballpit(s, 1.1, -1.1, .95, rim=BARK, mats=(BA, WH))
    s.mound(-1.4, -1.5, .9, .8, .8, off=(.1, -.1)); s.mound(-1.5, 1.0, .7, .55, .45)
    s.slide(-1.35, -1.25, -np.pi/2 + .15, .8, mat=HL)
    roller(s, .3, 1.5, 1.0, mat=BARK, part="Root_Rollers"); roller(s, .5, 1.7, 1.55, r=.13, mat=BARK, part="Root_Rollers")
    st = [(2.0, .6, .2), (2.1, 1.4, .3)]; sm = s.pods([(x, z, .08, h) for x, z, h in st], WH, part="Mushroom_Stems"); caps = []
    for m, (x, z, h) in zip(sm, st):
        c = node((0, 0, 0), .22, 1); c.vertices *= [1, .42, 1]; c.apply_translation((x, PAD + h + .08, z)); tl.drop([c], [m], emb=.003); caps.append(c)
    s.add("Mushroom_Caps", BA, *caps)
    s.cluster(-2.5, -2.4, 3, .24, seed=1); s.cluster(2.5, -2.4, 3, .24, seed=2); s.cluster(-2.6, 2.4, 3, .22, seed=3); s.cluster(2.6, 2.4, 3, .22, seed=4)
    s.flowers(-1.5, 1.0, 5, 5, .3); tufts(s, 14, seed=1, keep=.22)
    return s.finish()
def meadow(q):   # Meadow Hills soft-play (#67 winner language)
    s = Scape(RU, MOSS); walls(s, .6)
    s.mound(-1.2, -1.4, 1.0, .9, .9, off=(-.1, -.1)); s.mound(1.3, -1.6, .8, .7, .55); s.tunnel(.1, -1.5, 1.1, 0.0)
    s.slide(-1.0, -.95, -np.pi/2 + .2, .9)
    ballpit(s, 1.2, .9, .8, rim=TAN, mats=(BA, HL, WH))
    steps(s, -1.6, .9, 0, 3); s.pods([(.0, .15, .17, .14), (.35, -.3, .17, .2)], HL)
    s.flowers(-1.2, -1.4, 6, 1, .5); s.flowers(1.3, -1.6, 4, 2, .3); s.cluster(-2.5, 2.4, 3, .22, seed=3); s.cluster(2.5, -2.45, 3, .22, seed=4); tufts(s, 14, seed=2, keep=.22)
    return s.finish()
def tennis(q):   # Tennis Ball Pit
    s = Scape(RU, MOSS); walls(s, .5)
    ballpit(s, 0, -.6, 1.4, rim=WH, mats=(BA, BA, WH))
    s.mound(-1.9, 1.4, .55, .6, .5, part="Ball_Mounds", mat=BA); s.mound(1.9, 1.4, .55, .6, .5, part="Ball_Mounds", mat=BA)
    s.add("Court_Line", AM, *[box(-2.2, 2.2, PAD - .002, PAD + .002, z - .025, z + .025) for z in (1.05,)], *[box(x - .025, x + .025, PAD - .002, PAD + .002, 1.075, 2.25) for x in (0,)], col=None)
    roller(s, -.9, .9, 1.7, mat=HL); s.pods([(-1.0, 1.2, .17, .14), (1.0, 1.2, .17, .14)], BA, part="Ball_Pods")
    s.panel(-2.05, -.6, np.pi/2, "hoops", HS, w=.9, h=.6); s.panel(2.05, -.6, -np.pi/2, "beads", HL, w=.9, h=.6)
    s.cluster(-2.5, -2.4, 3, .24, seed=1); s.cluster(2.5, -2.4, 3, .24, seed=2); tufts(s, 10, seed=3, keep=.22)
    return s.finish()
def river(q):    # Riverbed soft-play
    s = Scape(RU, MOSS); walls(s, .5)
    ballpit(s, -.9, .3, .9, rim=STONE, mats=(RIV, WH))
    C = [(-2.2, -1.6), (-1.0, -1.2), (.4, -1.6), (1.5, -.9), (2.2, -1.1)]; R = []
    for k, ((x0, z0), (x1, z1)) in enumerate(zip(C, C[1:])):
        L = np.hypot(x1 - x0, z1 - z0); m = box(-L/2 - .02, L/2 + .02, PAD - .0015, PAD + .004 + .0012*(k % 2), -.35, .35); m.apply_transform(Y(-np.arctan2(z1 - z0, x1 - x0))); m.apply_translation(((x0 + x1)/2, 0, (z0 + z1)/2)); R.append(m)
    s.add("River_Ribbon", RIV, *R, col=None)
    s.pods([(-1.6, -1.4, .16, .12), (-.3, -1.4, .16, .16), (.9, -1.25, .16, .12), (1.9, -1.0, .16, .14)], STONE, part="River_Stones")
    s.mound(1.4, .9, .9, .8, .7); s.mound(1.9, -2.0, .4, .3, .3); s.slide(1.4, .55, np.pi/2, .7, mat=HS)
    roller(s, -1.9, -1.0, 1.85, mat=STONE, part="Stone_Rollers")
    s.cluster(1.4, .9, 4, .22, seed=1); s.cluster(-2.5, -2.4, 3, .22, seed=2); s.flowers(-.2, 2.0, 5, 3, .3); tufts(s, 12, seed=4, keep=.22)
    return s.finish()
def nest(q):     # Leaf Nest
    s = Scape(RU, TAN); walls(s, .5)
    for k in range(7):
        a = 2*np.pi*k/7 + .2; s.mound(1.6*np.cos(a), -.2 + 1.6*np.sin(a), .5, .35, .35 + .12*(k % 3), rot=a + np.pi/2)
    ballpit(s, 0, -.2, .8, rim=HL, mats=(HL, BA, WH))
    s.tree(-1.7, -1.7, 2.2, 6, LF, lean=.3, leaf_len=1.0)
    s.pods([(-.3, 1.9, .16, .12), (.3, 2.1, .16, .18), (2.0, 1.8, .16, .14)], HL)
    s.cluster(2.3, -2.2, 3, .24, seed=1); s.cluster(2.3, 1.6, 2, .2, seed=2); s.flowers(-2.2, 1.6, 4, 3, .3); tufts(s, 10, seed=5, keep=.22)
    return s.finish()
B = dict(forest=forest, meadow=meadow, tennis=tennis, river=river, nest=nest)
def build(q): return B[q["c"]](q)
VARIANTS = [
    dict(c="forest", label="Forest Floor: bark-rim ball pit, moss hill + slide, root rollers, mushrooms"),
    dict(c="meadow", label="Meadow Hills: twin hills, tunnel, slide, ball pit, foam steps + pods"),
    dict(c="tennis", label="Tennis Ball Pit: big tennis-ball pit, ball hills, court lines, hoop panels"),
    dict(c="river", label="Riverbed: blue ball pool, foam river + stones, bank hill slide"),
    dict(c="nest", label="Leaf Nest: ring of leaf cushions round a ball pit, canopy tree"),
]
def sheet(rep):
    rdir = os.path.join(RENDER_OUT, "soft_play"); fig, axs = plt.subplots(2, 5, figsize=(26, 11), facecolor="#F4F2EC")
    for i, (prm, r) in enumerate(zip(VARIANTS, rep)):
        p = recenter(build(prm)); _, geo = export_final(p.P, [f"/tmp/sp_{i}.glb"]); geo = {k: v for k, v in geo.items() if "colonly" not in k}
        for row, (el, az) in enumerate(((22, 25), (36, 200))):
            im = crop(render_view(geo, iso(el, az), size=720, shadow=True)); plt.imsave(os.path.join(rdir, f"v{i+1}_{'hero' if row == 0 else 'back'}.png"), np.clip(im, 0, 1))
            ax = axs[row, i]; ax.imshow(np.clip(im, 0, 1)); ax.axis("off")
            if row == 0: ax.set_title(f"v{i+1}  {prm['label'].split(': ')[0]}\n{prm['label'].split(': ')[1]}\n{r['tris']} tris | {'PASS' if r['passed'] else 'FAIL'}", fontsize=10, color="#222")
    fig.suptitle("Rook | Tennis Tower soft-play pit V1-V5 | 6 x 6 m enclosed | front 3/4 (top) + back 3/4 (bottom)", fontsize=14, color="#333")
    plt.tight_layout(rect=(0, 0, 1, .95)); sp = os.path.join(rdir, "soft_play_contact_sheet.png"); fig.savefig(sp, dpi=110, facecolor="#F4F2EC"); plt.close(fig); print("SHEET", sp)
if __name__ == "__main__":
    rep = run("soft_play", build, VARIANTS, title="soft-play pit 6 x 6 m", view=iso(22, 25), sheet="soft_play_run_sheet.png"); sheet(rep)
