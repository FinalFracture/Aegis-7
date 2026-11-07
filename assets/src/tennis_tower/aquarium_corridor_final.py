"""Rook: #80 lobby / aquarium corridor FINAL: V2 Kelp Forest (Jared pick), densified + sculpted.
Spec §3.12.1 Rev 2.8. Builds on aquarium_corridor.py (theme 'kelp') and adds layers: backdrop kelp-silhouette relief,
two moss-capped backdrop ledges, a free-swimming alloy fish school (rejection-placed), kelp crests along the header,
denser floor (two chip layers + flush pebble discs), bench sub-slab + seated moss tufts, plinth kelp side ribbons +
moss tuft, double-crest sign, finned caustic projector. Acrylic (Glass_Acrylic) is the ONLY BLEND; no other glass;
signage/screens opaque emissive. No wood, no planter boxes.  ->  godot/assets/models/tt_aquarium_{tank,floor,bench,plinth,sign,caustic}.glb"""
import shutil
import aquarium_corridor as AQ
from aquarium_corridor import *
BASE = AQ.build
GODOT = os.path.join(os.path.dirname(__file__), "..", "..", "..", "godot", "assets", "models")
def fish(c, L, rng):
    v = np.array([(L/2, 0, 0), (-L/2, 0, 0), (0, L*.22, 0), (0, -L*.22, 0), (0, 0, L*.12), (0, 0, -L*.12)], float) + c
    m = trimesh.Trimesh(v, [[0,2,4],[2,1,4],[1,3,4],[3,0,4],[2,0,5],[1,2,5],[3,1,5],[0,3,5]], process=False); m.metadata["uv"] = np.zeros((6, 2)); return m
def build(q):
    q = dict(q, theme="kelp"); p = BASE(q); pc = q["piece"]; rng = np.random.default_rng(80); h = W/2; X0, X1 = -h + .001, h - .001
    if pc == "tank":
        L = [(X0 + .2, -.6, 1.4), (.4, X1 - .2, 2.2)]; RB = []
        for x, y1 in zip(np.linspace(X0 + .3, X1 - .3, 11), rng.uniform(1.6, 2.9, 11)):
            segs = [(SILL + .1, y1)]
            for a_, b_, y in L:
                if a_ - .06 < x < b_ + .06: segs = [s for (u, v) in segs for s in ([(u, v)] if not (u < y and v > y - .06) else [(u, y - .06 + E), (y - E, v)]) if s[1] - s[0] > .05]
            RB += [box(x - .05, x + .05, u, v, -1.84 - E, -1.825) for u, v in segs]
        p.add("Backdrop_Kelp_Relief", LF2, *RB)
        p.add("Backdrop_Ledges", SSL, *[box(a, b, y - .06, y, -1.842, -1.7) for a, b, y in L])
        p.add("Ledge_Moss", LF2, *[seat(clump((x, y + .05, -1.77), .05, 600 + k), y) for k, (a, b, y) in enumerate(L) for x in np.linspace(a + .15, b - .15, 5)])
        F, occ, k = [], [], 0
        while len(F) < 14 and k < 400:
            k += 1; c = (rng.uniform(X0 + .5, X1 - .5), rng.uniform(1.6, 2.8), rng.uniform(-.6, -.4)); b = (np.subtract(c, .1), np.add(c, .1))
            if not any(np.all(b[0] < o[1]) and np.all(b[1] > o[0]) for o in occ): F.append(fish(c, rng.uniform(.12, .18), rng)); occ.append(b)
        p.add("Fish_School", ALY, *F)
        p.add("Header_Kelp_Crests", LF, *[crest((x, WTOP + .48 - E, .05)) for x in (-1.4, 0, 1.4)])
    elif pc == "floor":
        Z0, Z1 = -3.4, 3.4; inl = [(-1.6, 0, 1.6)]
        def free(x, z, r): return all(abs(z - zz) > .05 + r for zz in np.linspace(Z0 + 1.1, Z1 - 1.1, 5)) and not (abs(z) < .05 + r and any(abs(x - xi) < .28 + r for xi in inl[0]))
        P2 = [(x, z) for x, z in zip(rng.uniform(X0 + .15, X1 - .15, 200), rng.uniform(Z0 + .15, Z1 - .15, 200)) if free(x, z, .04)]
        p.add("Terrazzo_Chips_Dark", SL, *[box(x, x + .03, FY - .004, FY + .0009, z, z + .025) for x, z in P2[:50]])
        p.add("Pebble_Discs", WH, *[tube((x, FY - .004, z), (x, FY + .0015, z), .03, 8) for x, z in P2[50:80]])
    elif pc == "bench":
        p.add("Bench_Subslab", G, box(-.55 + E, .55 - E, .38, .42 + E, -.22, .22))
        p.add("Moss_Tufts", LF2, *[seat(clump((x, .05, z), .05, 700 + i), 0.0) for i, (x, z) in enumerate([(-.7, .3), (.7, -.3), (.7, .3)])])
    elif pc == "plinth":
        p.add("Kelp_Side_Ribbons", LF2, *[box(s*.3 - (E if s > 0 else .012), s*.3 + (.012 if s > 0 else E), .12, y1, z - .025, z + .025) for s in (-1, 1) for z, y1 in ((-.1, .9), (0, 1.02), (.1, .8))])
        p.add("Moss_Tuft", LF2, seat(clump((.42, .05, .1), .05, 9), 0.0))
    elif pc == "sign":
        p.add("Blade_Crest_W", LF, crest((-1.6, .6 - E, 0)))
    else:
        p.add("Can_Fins", ALY, *[xf(box(.104, .13, .1, .23, -.006, .006), R=trimesh.transformations.rotation_matrix(a, [0, 1, 0])) for a in np.linspace(0, 2*np.pi, 8, endpoint=False) + np.pi/8])
    return p
if __name__ == "__main__":
    AQ.build = build
    VAR = [dict(piece=pc, label=f"Kelp Forest / {pc}") for pc in PIECES]
    REP = run("aquarium_corridor_final", build, VAR, title="aquarium corridor final (V2 Kelp Forest)", names=[f"tt_aquarium_{pc}" for pc in PIECES], sheet="aquarium_corridor_final_run_sheet.png")
    SE = tank_seam("kelp"); CL = clearance(1); print("SEAM", SE, "CLEAR", CL)
    rdir = os.path.join(RENDER_OUT, "aquarium_corridor_final"); json.dump(dict(rep=REP, seam=SE, clear=CL), open(os.path.join(rdir, "report.json"), "w"), indent=1, default=str)
    Ry = lambda el, az: (lambda a, b: np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]) @ np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]))(np.radians(az), np.radians(el))
    fig = plt.figure(figsize=(28, 22), facecolor="#F4F2EC"); gs = fig.add_gridspec(3, 4)
    shots = [("tank", (8, 25), "tank bay 3/4"), ("tank", (22, -72), "tank raking side (reef depth)"), ("tank", (2, 0), "tank front elevation"), ("floor", (35, 30), "floor tile"),
             ("bench", (20, 35), "bench"), ("plinth", (12, 30), "info plinth"), ("sign", (10, 20), "AQUATICS blade"), ("caustic", (-25, 30), "caustic projector")]
    for j, (pc, (el, az), t) in enumerate(shots):
        geo = {k: v for k, v in export_final(recenter(build(dict(piece=pc))).P, [f"/tmp/aqf_{j}.glb"])[1].items() if "colonly" not in k}
        ax = fig.add_subplot(gs[j // 4, j % 4]); ax.imshow(np.clip(crop(render_view(geo, Ry(el, az), size=750, shadow=False, glass_alpha=.3)), 0, 1)); ax.axis("off")
        r = REP[PIECES.index(pc)]; ax.set_title(f"tt_aquarium_{pc} ({t})\n{r['tris']} tris | {'PASS' if r['passed'] else 'FAIL'}", fontsize=11)
    A = vignette(1); A.pop("Soffit")
    Pt = Part()
    for n, (mk, m) in A.items(): Pt.add(n, mk, m)
    _, g2 = export_final(Pt.P, ["/tmp/aqfv.glb"])
    ax = fig.add_subplot(gs[2, :]); ax.imshow(np.clip(crop(render_view(g2, Ry(16, 32), size=1500, shadow=False, glass_alpha=.3)), 0, 1)); ax.axis("off")
    ax.set_title(f"corridor vignette X 0..27.5 (soffit hidden): 4 tank bays = 22 m acrylic line Z 42.5, terrazzo, 4 benches, 2 plinths, blades X 1 / X 24, 3 projectors, clad pier X 0 / Z 39.5\n"
                 f"tank seam {'PASS' if SE else 'FAIL'} | clear past rail {CL['clear_rail']} m, past bench row {CL['clear_bench_row']} m (8.0 m corridor)", fontsize=12)
    fig.suptitle("Rook | #80 tt_aquarium_{tank,floor,bench,plinth,sign,caustic} (V2 Kelp Forest, densified) | FINAL", fontsize=16)
    plt.tight_layout(rect=(0, 0, 1, .96)); sp = os.path.join(rdir, "aquarium_corridor_final_sheet.png"); fig.savefig(sp, dpi=72, facecolor="#F4F2EC"); print("SHEET", sp)
    if all(r["passed"] for r in REP) and SE and CL["pass_"]:
        for pc in PIECES: shutil.copy(os.path.join(GLB_OUT, "aquarium_corridor_final", f"tt_aquarium_{pc}.glb"), os.path.join(GODOT, f"tt_aquarium_{pc}.glb"))
        print("PROMOTED")
