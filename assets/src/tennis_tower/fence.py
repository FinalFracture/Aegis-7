"""Rook: Tennis Tower E-terrace playground fence + gates (spec §3.11.6 item 9: 1.2 m fence with 3 gates) as tileable pieces.
Per concept: PANEL (2.0 m pitch along X: one 80 mm post at the -X end, infill to +X; tile every 2.0 m, the next panel's post closes it)
and GATE (1.6 m module: 2 posts, 1.42 m single leaf, hinge -X, child-proof latch on top at +1.2; leaf parts Gate_* animate about a Y hinge
at local x -0.72). Height 1.2 m; child-safe: infill clear gaps 80 mm (< 89), bottom gap 40 mm, no mid-height rails, rounded/caps on posts.
Planted / sculpted base: low berm strip + foliage on the outside (-Z), so a run reads as a living edge, not a railing. No wood, no planter boxes.
REUSE: #70 Leaf Canopy (gunmetal + leaf HDPE + leaf crests), #67 Meadow Hills (moss berm, flowers), #68 Forest Roots (bark rubber),
#69 Riverbed (stone rubber, blue), #63/#66 court line + ball finials, toddler_landscape kit. Run: python3 fence.py"""
from modlib import *
import toddler_landscape as tl
from toddler_landscape import Scape, iso, RU, MOSS, TAN, RIV, BARK, SAND, STONE, HL, HS, Y, PAD, U
from balance_trail import tufts
from restroom_extras import crest
H, PW, Y0 = 1.2, .04, .07
def infill(s, x0, x1, q, part="Infill", rail_part="Rails", top=None):
    st = q["infill"]; mat = q["fill"]; rm = q["rail"]
    rz = .025 if rail_part == "Rails" else .02
    o = 0 if rail_part == "Rails" else .004
    s.add(rail_part, rm, box(x0, x1, Y0 + o, Y0 + .06, -rz, rz), box(x0, x1, H - .08, H - .02 - o, -rz, rz))
    if st in ("pickets", "wave", "roots"):
        n = int((x1 - x0 + .08)/(.05 + .08)); xs = np.linspace(x0 + .025 + .04, x1 - .025 - .04, n)
        P = []
        for k, x in enumerate(xs):
            y1 = H - .08 + E
            if st == "wave": y1 = H - .08 + E  # wave crest added above the top rail as separate fins
            P.append(box(x - .025, x + .025, Y0 + .06 - E, y1, -.015, .015))
        s.add(part, mat, *P)
        if st == "wave": s.add(part + "_Wave", mat, *[box(x - .025, x + .025, H - .02 - E, H - .02 + .06 + .05*np.sin(4*np.pi*(x - x0)/(x1 - x0)), -.015, .015) for x in xs])
    elif st in ("net", "screen"):
        s.add(part, mat, box(x0 + .002, x1 - .002, Y0 + .06 - E, H - .08 + E, -.008, .008))
        if st == "net": s.add(part + "_Tape", WH, box(x0 + .012, x1 - .012, H - .2, H - .086, -.012, .012), col=None)
def post(s, x, q):
    s.add("Posts", q["post"], box(x - PW, x + PW, PAD - E, H + .02, -PW, PW))
    f = q.get("finial")
    if f == "leaf": s.add("Leaf_Crests", LF, crest((x, H + .02 - .004, 0)), col=None)
    elif f == "ball": s.add("Ball_Finials", BA, node((x, H + .02 + .045 - E, 0), .045, 0), col=None)
    else: s.add("Post_Caps", q["post"], cap((x, H + .02 + .015 - E, 0), .038, .03, 10, axis="y"), col=None)
def base(s, x0, x1, q, seed=0):
    b = q["base"]
    if b == "berm":
        s.mound((x0 + x1)/2, -.3, (x1 - x0)/2, .2, .32); s.cluster((x0 + x1)/2, -.3, 4, .2, seed=seed, spread=(x1 - x0)/2 - .1); s.flowers((x0 + x1)/2, -.32, 4, seed + 1, (x1 - x0)/2 - .1)
    elif b == "ferns":
        s.mound((x0 + x1)/2, -.28, (x1 - x0)/2, .18, .22); s.cluster((x0 + x1)/2, -.3, 5, .22, seed=seed, mats=(LF, LF2), spread=(x1 - x0)/2 - .1)
    elif b == "stone":
        s.add("Stone_Base", STONE, box(x0 + .002, x1 - .002, PAD - E, .34, -.33, -.06)); s.add("River_Ribbon", RIV, box(x0, x1, PAD - .0015, PAD + .004, .12, .42), col=None)
        s.pods([(x, -.42, .07, .08) for x in np.linspace(x0 + .2, x1 - .2, 4)], STONE, part="Pebbles"); [s.bush(x, -.43, .13, LF if k % 2 else LF2, seed + k) for k, x in enumerate(np.linspace(x0 + .35, x1 - .35, 3))]
    elif b == "hedge":
        s.mound((x0 + x1)/2, -.24, (x1 - x0)/2, .14, .18)
        for k, x in enumerate(np.linspace(x0 + .2, x1 - .2, 5)): s.bush(x, -.26, .2, LF if k % 2 else LF2, seed + k)
    tufts(s, 3, seed=seed + 7, keep=.12)
def panel(q):
    tl.HX, tl.HZ = 1.0, .5; s = Scape(q.get("ground", RU), q.get("terrain", MOSS))
    post(s, -1.0 + PW, q); infill(s, -1.0 + 2*PW - E, 1.0, q); base(s, -.95, .95, q, 1)
    if q.get("line"): s.add("Court_Line", AM, box(-1.0, 1.0, PAD - .002, PAD + .002, .25, .3), col=None)
    return s.finish()
def gate(q):
    tl.HX, tl.HZ = .8, .5; s = Scape(q.get("ground", RU), q.get("terrain", MOSS))
    for x in (-.8 + PW, .8 - PW): post(s, x, q)
    x0, x1 = -.8 + 2*PW + .012, .8 - 2*PW - .012
    s.add("Gate_Frame", q["rail"], box(x0, x0 + .05, Y0, H - .02, -.025, .025), box(x1 - .05, x1, Y0, H - .02, -.025, .025))
    infill(s, x0 + .05 - E, x1 - .05 + E, dict(q, infill="pickets" if q["infill"] == "wave" else q["infill"]), part="Gate_Infill", rail_part="Gate_Rails")
    s.add("Gate_Hinge_Hardware", G, *[box(-.8 + 2*PW - E, x0 + .02, y - .04, y + .04, -.03, .03) for y in (.25, 1.0)])
    s.add("Gate_Latch_Hardware", G, box(x1 - .03, .8 - 2*PW + E, H - .1, H + .0, -.035, .035))
    s.add("Gate_Sign", q.get("sign", LF), box(-.18, .18, .62, .82, .025 - E, .035), col=None)
    tufts(s, 2, seed=3, keep=.12)
    return s.finish()
C = [
    dict(c="leaf", label="Leaf Canopy: gunmetal posts + leaf crests, leaf pickets, moss berm", post=SGM, rail=SGM, fill=HL, infill="pickets", finial="leaf", base="berm", terrain=MOSS),
    dict(c="meadow", label="Meadow Wave: sand pickets with a wave crest, flowering berm", post=ALY, rail=ALY, fill=HS, infill="wave", base="berm", terrain=MOSS, sign=BA),
    dict(c="forest", label="Forest Roots: bark posts, leaf screen, fern bank", post=BARK, rail=BARK, fill=HL, infill="screen", finial="leaf", base="ferns", ground=MOSS, terrain=RU),
    dict(c="court", label="Court Line: alloy frame, court-net screen + tape, ball finials, hedge", post=ALY, rail=ALY, fill=SSL, infill="net", finial="ball", base="hedge", terrain=MOSS, line=True, sign=BA),
    dict(c="river", label="Riverbed: stone base wall, blue wave pickets, river ribbon", post=STONE, rail=STONE, fill="tt_rubber_river", infill="wave", base="stone", terrain=MOSS, sign=RIV),
]
PARAMS = [dict(q, piece=pc, label=f"{q['label'].split(':')[0]} {pc}: {q['label'].split(': ')[1]}") for q in C for pc in ("panel", "gate")]
NAMES = [f"v{i // 2 + 1}_{'panel' if i % 2 == 0 else 'gate'}" for i in range(10)]
def build(q): return panel(q) if q["piece"] == "panel" else gate(q)
def assembly(q):  # render-only run: panel, panel, gate, panel
    A = Part(); k = 0
    for pc, dx in (("panel", -3.0), ("panel", -1.0), ("gate", .8), ("panel", 2.6)):
        p = recenter(build(dict(q, piece=pc)))
        for n, (mk, m) in p.P.items():
            if "colonly" in n: continue
            m = m.copy(); m.metadata["uv"] = p.P[n][1].metadata["uv"]; m.apply_translation((dx, 0, 0)); A.add(f"{n}_{k}", mk, m)
        k += 1
    return A
def sheet(rep):
    rdir = os.path.join(RENDER_OUT, "fence"); fig, axs = plt.subplots(2, 5, figsize=(28, 10), facecolor="#F4F2EC")
    for i, q in enumerate(C):
        _, geo = export_final(assembly(q).P, [f"/tmp/fe_{i}.glb"])
        for row, (el, az) in enumerate(((14, 30), (24, 155))):
            im = crop(render_view(geo, iso(el, az), size=760, shadow=True)); plt.imsave(os.path.join(rdir, f"v{i+1}_run_{'out' if row == 0 else 'in'}.png"), np.clip(im, 0, 1))
            ax = axs[row, i]; ax.imshow(np.clip(im, 0, 1)); ax.axis("off")
            if row == 0:
                rp, rg = rep[2*i], rep[2*i + 1]
                ax.set_title(f"v{i+1}  {q['label'].split(': ')[0]}\n{q['label'].split(': ')[1]}\npanel {rp['tris']} | gate {rg['tris']} tris | {'PASS' if rp['passed'] and rg['passed'] else 'FAIL'}", fontsize=10, color="#222")
    fig.suptitle("Rook | Tennis Tower playground fence V1-V5 | 1.2 m, panel 2.0 m pitch + 1.6 m gate | run shown: panel, panel, gate, panel | outside 3/4 (top) + inside 3/4 (bottom)", fontsize=13, color="#333")
    plt.tight_layout(rect=(0, 0, 1, .95)); sp = os.path.join(rdir, "fence_contact_sheet.png"); fig.savefig(sp, dpi=110, facecolor="#F4F2EC"); plt.close(fig); print("SHEET", sp)
if __name__ == "__main__":
    rep = run("fence", build, PARAMS, title="fence panel + gate", names=NAMES, view=iso(14, 30), sheet="fence_run_sheet.png"); sheet(rep)
