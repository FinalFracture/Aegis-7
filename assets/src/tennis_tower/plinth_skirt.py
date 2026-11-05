"""Rook: Tennis Tower plinth skirt (spec §3.3: F1 = +4.0 HD, plinth p(Z) = 4.0 - (Z-40)^2/400, 4.0 m deep at the W/E faces where the
raised West Arrival / East Plaza terrace edges and plaza steps meet the hull; 0 at the S/N faces). One 4.0 m façade-module tile, 4.0 m tall
(grade 0 -> F1 +4.0), built as 4 x 1.0 m courses so it can be trimmed to p(Z) (drop / cut courses where the plinth is shallower).
+Z = exterior, face line z 0 (sits under tt_facade_bay / tt_entrance_bay at +4.0), pivot bottom centre. Matches #74 Court Wayfinding (slate,
gunmetal, amber court lines, ball bollards) and #75 Branch Glass (trunks, forks, leaf clusters, stepped slate ledge).
No wood, no planter boxes (planting = clumps on treads/ledges). Run: python3 plinth_skirt.py"""
from modlib import *
from restroom_extras import crest
from ridge_crown import huv
W, HT = 4.0, 4.0; h = W/2; X0, X1 = -h + .001, h - .001
def coping(p, d=.5):
    p.add("Coping", G, box(X0, X1, HT - .12, HT, -.2, d)); p.add("Coping_Court_Line", AM, box(X0, X1, HT - .08, HT - .045, d - E, d + .007))
def build(q):
    p = Part(); k = q["kind"]; rng = np.random.default_rng(q.get("seed", 1))
    p.add("Skirt_Core", SL, box(X0, X1, 0, HT - .12 + E, -.2, .02))
    if k in ("steps", "green"):   # stepped slate courses, deeper at the bottom
        D = [1.6, 1.2, .8, .4]; C = []; N = []
        for i, d in enumerate(D):
            y0, y1 = i*1.0, (i + 1)*1.0 - (.116 if i == 3 else 0)
            C.append(box(X0, X1, y0 + (0 if i == 0 else -E), y1, .02 - E, d))
            N.append(box(X0, X1, y1 - .05, y1 - .02, d - E, d + .006))
            if i < 3: C.append(box(X0, X1, y0 + .08, y1 - .08, d - E, d + .05))   # shadow-line reveal course
        p.add("Skirt_Courses", SL, *C); p.add("Court_Line_Nosings", AM, *N); coping(p, .45)
        if k == "green":
            L = []; L2 = []
            for i, d in enumerate(D[:3]):
                zt = (d + D[i+1])/2 + .05; yt = (i + 1)*1.0
                xs = np.arange(-h + .25, h - .2, .32 + .04*i)
                L += [clump((x, yt + .17 - .006, zt), .17, 10*i + j) for j, x in enumerate(xs)]
            st, lv = vine([(X0 + .05, 1.9, D[1] + .05 + .014), (0, 1.5, D[1] + .05 + .014), (X1 - .05, 1.85, D[1] + .05 + .014)], r=.014, leaf_every=.25, leaf_len=.22, seed=3, outward=True)
            p.add("Tread_Hedges", LF, *L); p.add("Trailing_Vine", LF, st); p.add("Trailing_Vine_Leaves", LF2, lv)
        if k == "steps":
            for x in (-1.0, 1.0): p.add("Ball_Bollards", G, tube((x, 1.0 - E, 1.4), (x, 1.85, 1.4), .1, 10)); p.add("Bollard_Balls", BA, node((x, 1.85 + .11 - E, 1.4), .11, 1))
    if k == "branch":   # battered slate wall with Branch Fin buttresses every 2 m, forks into the coping, leaf clusters
        WL = [huv([(x, y, z) for x in (X0, X1) for (y, z) in ((0, .02 - E), (0, .7), (HT - .12 + E, .02 - E), (HT - .12 + E, .25))])]
        B = []; Lc = []
        for x0 in (-1.0, 1.0):
            zb = .7 + .35; WL += [box(x0 - .25, x0 + .25, 0, .4, .5, zb + .25), box(x0 - .3, x0 + .3, 0, .12, .45, 1.35)]
            n0 = (x0, .4 + .1 - E, zb); n1 = (x0, 2.4, zb - .15); B += [node(n0, .1, 0), tube(n0, n1, .085, 10), node(n1, .13, 0)]
            for dx in (-.7, 0, .7):
                e = (x0 + dx, HT - .12 + .012, .3 + .1); B += [tube(n1, e, .05 if dx == 0 else .04, 8)]
            Lc += [clump((x0, 2.4 + .16, zb - .15 + .249), .17, int(x0 + 5))]
        p.add("Branch_Buttress", G, *B); p.add("Fork_Leaves", LF, *Lc); coping(p, .5)
        p.add("Battered_Wall", SL, *WL)
    if k == "rock":     # riverbed rockery: layered sculpted boulders at the base, pebbles + moss, slate terraces above
        p.add("Upper_Courses", SL, box(X0, X1, 2.0 - E, HT - .116, .02 - E, .35), box(X0, X1, 1.2, 2.0, .02 - E, .6))
        R = []; S = []; M = []
        for j, (x, s) in enumerate(((-1.55, .55), (-.75, .7), (.1, .6), (.9, .75), (1.6, .5))):
            P = (rng.normal(size=(14, 3))*[s*.55, s*.5, s*.45]); P[:, 1] = np.abs(P[:, 1]); P[:, 1] *= 1.6
            P[:, 0] = np.clip(P[:, 0] + x, X0 + .01, X1 - .01); P[:, 2] += .7; P[:, 2] = np.clip(P[:, 2], .03, 1.6); P[:, 1] -= P[:, 1].min(); P[:, 1] = np.minimum(P[:, 1], 1.15)
            R.append(huv(P))
        for j in range(16):
            x = -1.85 + j*.245 + rng.uniform(-.05, .05); r = .06 + rng.uniform(0, .03); S.append(node((x, r - E, 1.72 + (j % 3)*.13), r, 0))
        for j, x in enumerate(np.arange(-1.7, 1.75, .42)): M.append(clump((x, 2.0 + .14 - .006, .48), .14, 70 + j))
        p.add("River_Boulders", SSL, *R); p.add("River_Pebbles", ST, *S); p.add("Terrace_Moss", LF, *M); coping(p, .45)
    if k == "boulder":  # climbing-boulder facets (#60 language): tilted slate facets with tennis-ball holds + amber route tape
        Fc = [huv([(x, y, z) for x in (X0, X1) for (y, z) in ((0, .02 - E), (0, 1.1), (1.6, .02 - E), (1.6, .75))]),
              huv([(x, y, z) for x in (X0, X1) for (y, z) in ((1.6 - .002, .02 - E), (1.6 - .002, .75), (3.0, .02 - E), (3.0, .95))]),
              huv([(x, y, z) for x in (X0, X1) for (y, z) in ((3.0 - .002, .02 - E), (3.0 - .002, .95), (HT - .12 + E, .02 - E), (HT - .12 + E, .5))])]
        p.add("Boulder_Facets", SL, *Fc)
        def zf(y): return 1.1 + (.75 - 1.1)*y/1.6 if y < 1.6 else (.75 + .2*(y - 1.6)/1.4 if y < 3.0 else .95 + (.5 - .95)*(y - 3.0)/(HT - .12 - 3.0))
        Hd = [node((x, y, zf(y) + (.05 if y < 3.0 else .062)), .06, 0) for (x, y) in ((-1.5, .5), (-.8, 1.1), (-.2, .6), (.5, 1.3), (1.2, .8), (-1.1, 2.2), (.1, 2.5), (.9, 2.1), (1.6, 2.6), (-.4, 3.3), (.7, 3.4), (-1.7, 1.4), (1.7, 1.5), (-.5, 1.9), (.4, 1.9), (-1.6, 3.0 - .3), (1.3, 3.2), (-1.2, .2 + .1), (.9, .4), (0, 3.6))]
        p.add("Tennis_Ball_Holds", BA, *Hd)
        T = []
        for y in (.3, 1.9, 3.25):
            z = zf(y); T.append(box(X0, X1, y, y + .04, z - .03, z + .006 + (.02 if 1.6 > y else .0)))
        p.add("Route_Tape", AM, *[huv([(x, y, zf(y) - .008) for x in (X0, X1) for y in (y0, y0 + .04)] + [(x, y, zf(y) + .008) for x in (X0, X1) for y in (y0, y0 + .04)]) for y0 in (.3, 1.9, 3.25)])
        p.add("Base_Mat", SSL, box(X0, X1, 0, .05, 1.1 + .002, 2.0)); coping(p, .55)
        p.add("Base_Moss", LF, *[clump((x, .05 + .13 - .006, 1.75), .13, 90 + j) for j, x in enumerate(np.arange(-1.7, 1.75, .38))])
    if q.get("lamps"):
        p.add("Court_Lamps", CY, *[box(x - .2, x + .2, HT - .115, HT - .09, .45 - E, .457) for x in (-1.0, 1.0)])
    p.add("Skirt-colonly", SL, box(X0, X1, 0, HT, -.2, .45))
    return p
VARIANTS = [
    dict(label="Court Steps: 4 stepped slate courses with amber court-line nosings, ball bollards", kind="steps", lamps=True),
    dict(label="Green Terraces: stepped courses with hedge rows on every tread, trailing vine", kind="green"),
    dict(label="Branch Buttress: battered slate wall, Branch Fin buttresses forking into the coping, leaf clusters", kind="branch"),
    dict(label="Riverbed Rockery: sculpted boulders, pebbles, moss terrace, slate courses (#72 Riverbed)", kind="rock", seed=4),
    dict(label="Boulder Skirt: tilted climbing facets, tennis-ball holds, amber route tape (#60)", kind="boulder"),
]
def pair_check(prm):
    A = {}
    for k in range(2):
        for n, (mk, m) in build(prm).P.items():
            if "colonly" in n: continue
            m2 = m.copy(); m2.apply_translation((k*W, 0, 0)); A[f"T{k}_{n}"] = (mk, m2)
    near = {k: v for k, v in A.items() if v[1].bounds[1][0] > h - .6 and v[1].bounds[0][0] < h + .6}
    chk = cc.check(near, n_samp=300); bad = [o for o in chk["overlap"] if not o[3] and o[0][:2] != o[1][:2]]; cop = [c for c in chk["coplanar"] if c[0][:2] != c[1][:2]]
    print("PAIR", bad[:3], cop[:3]); return not bad and not cop
def sheet(rep, seams):
    import facade_bay_final as FB
    rdir = os.path.join(RENDER_OUT, "plinth_skirt"); fig, axs = plt.subplots(3, 5, figsize=(28, 17), facecolor="#F4F2EC")
    Ry = lambda el, az: (lambda a, b: np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]) @ np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]))(np.radians(az), np.radians(el))
    for i, (prm, r) in enumerate(zip(VARIANTS, rep)):
        p = recenter(build(prm)); _, geo = export_final(p.P, [f"/tmp/ps_{i}.glb"]); geo = {k: v for k, v in geo.items() if "colonly" not in k}
        for row, (el, az) in enumerate(((8, 38), (25, -70))):
            im = crop(render_view(geo, Ry(el, az), size=760, shadow=False, glass_alpha=.35)); axs[row, i].imshow(np.clip(im, 0, 1)); axs[row, i].axis("off")
            plt.imsave(os.path.join(rdir, f"v{i+1}_{['front34', 'side'][row]}.png"), np.clip(im, 0, 1))
        A = Part()   # 3 skirt tiles with tt_facade_bay (#75) seated on top at +4.0 (face line z 0 on both)
        for k in range(3):
            for src, dy in ((build(prm), 0), (FB.build(dict(width=4.0)), HT)):
                for n, (mk, m) in src.P.items():
                    if "colonly" in n: continue
                    m2 = m.copy(); m2.apply_translation((k*W, dy, 0)); m2.metadata["uv"] = m.metadata.get("uv", np.zeros((len(m.vertices), 2))); A.add(f"B{k}{dy}_{n}", mk, m2)
        _, g2 = export_final(A.P, [f"/tmp/pss_{i}.glb"]); im = crop(render_view(g2, Ry(10, 28), size=900, shadow=False, glass_alpha=.35))
        plt.imsave(os.path.join(rdir, f"v{i+1}_with_facade.png"), np.clip(im, 0, 1)); axs[2, i].imshow(np.clip(im, 0, 1)); axs[2, i].axis("off")
        a, b = prm["label"].split(": ")
        axs[0, i].set_title(f"v{i+1}  {a}\n{b}\n{r['tris']} tris | {'PASS' if r['passed'] else 'FAIL'} | pair {'PASS' if seams[i] else 'FAIL'}", fontsize=9)
    for row, t in enumerate(("low 3/4 from the plaza", "raking side (depth)", "3 tiles + tt_facade_bay on top (F1 +4.0)")): axs[row, 0].text(-.02, .5, t, transform=axs[row, 0].transAxes, rotation=90, va="center", ha="right", fontsize=12)
    fig.suptitle("Rook | Tennis Tower plinth skirt V1-V5 | 4.0 m tile, grade -> F1 +4.0 (W/E faces, §3.3) | candidates (not promoted)", fontsize=15)
    plt.tight_layout(rect=(0, 0, 1, .95)); sp = os.path.join(rdir, "plinth_skirt_contact_sheet.png"); fig.savefig(sp, dpi=85, facecolor="#F4F2EC"); plt.close(fig); print("SHEET", sp)
if __name__ == "__main__":
    rep = run("plinth_skirt", build, VARIANTS, title="plinth skirt 4.0 m", sheet="plinth_skirt_run_sheet.png")
    seams = [pair_check(v) for v in VARIANTS]; json.dump(rep, open(os.path.join(RENDER_OUT, "plinth_skirt", "report.json"), "w"), indent=1, default=str); sheet(rep, seams)
