"""Rook: Tennis Tower generic F1-F2 façade bay (S/N/E faces + W outside the doors). Spec defines no F1/F2 elevation (only §3.11.1 F3 wall),
so this follows the §3.11.1 4.0 m module and #52 Branch Fin language: 4.0 m x 12.2 m (F1 0..6.1, F2 6.1..12.2, F3 Glass Box starts at +12.2),
heavy fin on the grid line + light fin at 2.0 m (inside, -Z), layered slab-edge band at +6.1, +Z = exterior. Tiles along X; stacks under
tt_curtain_wall_panel. Matches #74 entrance bay (slate/gunmetal fascia, amber court line), #53 Leaf Capital, #58 Leaf Crest.
No wood, no planter boxes. Glass BLEND (envelope). Run: python3 facade_bay.py"""
from modlib import *
from restroom_extras import crest
W, H, SB = 4.0, 12.2, 6.1; h = W/2; X0, X1 = -h + .001, h - .001
ROWS = [(.15, 3.05), (3.05, 5.75), (6.45, 9.15), (9.15, 12.05)]
COLS = [(-h + .085, -.0125), (.0125, h - .045)]
def cell(p, q, kind, a, b, y0, y1, k):
    ya, yb = y0 + (.06 if y0 > .2 and y0 not in (6.45,) else 0) - E, y1 - (.06 if y1 not in (5.75, 12.05) else 0) + E
    if kind == "glass": p.add(f"Glass_{k}", GL, pane(a + .002, b - .002, ya, yb, 0))
    elif kind in ("slate", "green", "mural", "court"):
        p.add("Slate_Panels", SL, box(a + .002, b - .002, ya, yb, -.03, .03))
        if kind == "green": ga = max(ya, .5); p.add("Green_Wall", LF, green_wall(a + .03, b - .03, ga + .04, yb - .04, .03, r=.15, seed=k*7))
        if kind == "court":   # court-line inlay: outline + centre line + service box (amber), raised 6 mm
            c = (a + b)/2; m = (ya + yb)/2; L = []
            for (u0, u1, v0, v1) in ((a + .15, b - .15, ya + .15, ya + .2), (a + .15, b - .15, yb - .2, yb - .15), (a + .15, a + .2, ya + .2 - E, yb - .2 + E), (b - .2, b - .15, ya + .2 - E, yb - .2 + E), (a + .2 - E, b - .2 + E, m - .025, m + .025), (c - .025, c + .025, m + .025 - E, yb - .2 + E)):
                L.append(box(u0, u1, v0, v1, .03 - E, .036))
            p.add("Court_Inlay", AM if q.get("amber") else WH, *L)
        if kind == "mural":   # racket + ball relief
            c = (a + b)/2; m = (ya + yb)/2; R = []
            ang = np.linspace(0, 2*np.pi, 15)[:-1]; P = [(c + .55*np.cos(t), m + .2 + .75*np.sin(t), .07) for t in ang]
            R += [tube(P[i], P[(i+1) % len(P)], .04, 6) for i in range(len(P))] + [tube((c, m - .55, .07), (c, m - 1.1, .07), .045, 6)]
            for x in np.arange(c - .4, c + .45, .2): R.append(box(x - .008, x + .008, m + .2 - .75*np.sqrt(max(0, 1 - ((x - c)/.55)**2)) + .04, m + .2 + .75*np.sqrt(max(0, 1 - ((x - c)/.55)**2)) - .04, .06, .075))
            p.add("Racket_Relief", ALY, *[xf(r, t=(0, 0, 0)) for r in R]); p.add("Racket_Relief", ALY, *[tube((c, y, .03 - E), (c, y, .07), .03, 6) for y in (m - .55, m + .95)])
            p.add("Ball_Relief", BA, node((c + .45, m - .85, .03 + .14 - E*2), .14, 1))
def build(q):
    p = Part(); F = [box(X0, X1, 0, .15, -.65, .1), box(X0, X1, H - .15, H, -.65, .08)]
    F.append(fin(-h + .06, .15 - E, H - .15 + E, .6, .05, z0=.03)); F.append(fin(0, .15 - E, H - .15 + E, .45, .025, z0=.03)); F.append(box(h - .045, h - .01, .15 - E, H - .15 + E, -.04, .04))
    for t in (3.05, 9.15): F += [box(a - E, b + E, t - .06, t + .06, -.05, .05) for a, b in COLS]
    F.append(box(X0, X1, .002, .45, .1 - E, .16))
    # layered slab-edge band at +6.1 (5.75..6.45): slate band, gunmetal step, amber court line
    p.add("Frame", G, *F)
    p.add("Slab_Band_Slate", SL, box(X0, X1, 5.75 - E, 6.45 + E, .042, .1))
    p.add("Slab_Band_Step", G, box(X0, X1, 5.86, 6.5, .1 - E, .19))
    p.add("Slab_Band_Court_Line", AM, box(X0, X1, 6.02, 6.06, .19 - E, .197))
    
    k = 0
    for r, (y0, y1) in enumerate(ROWS):
        for c, (a, b) in enumerate(COLS): cell(p, q, q["cells"][r][c], a, b, y0, y1, k); k += 1
    d = q.get("dress", ())
    F = p.P.pop("Frame")[1:]; F = [F[0]]
    if "louvres" not in d:   # exterior Branch Fin trunk on the heavy-fin grid line (#52 / #53 echo): shoe, trunk, Y-branches onto the transoms, leaf capital
        x0, zt = -h + .115, .42; T = [node((x0, .1 - E, zt), .1, 0), tube((x0, .1, zt), (x0, 11.55, zt), .06, 8)]
        for y in (3.05, 9.15, 6.1):
            zz = .05 - E if y != 6.1 else .19 + .028; T += [node((x0, y, zt), .09, 0), tube((x0, y, zt), (x0 + .65, y - .02, zz), .035, 6), tube((x0, y + .3, zt), (x0 + .35, y + .02, zz), .03, 6)]
        T.append(node((x0, 11.55, zt), .1, 0)); F += T
        p.add("Leaf_Capital", LF, *[xf(crest((0, 0, 0)), R=trimesh.transformations.rotation_matrix(a, [0, 1, 0]), t=(x0, 11.55 + .08, zt)) for a in (0, np.pi/3, -np.pi/3)])
    p.add("Frame", G, *F)
    if "crests" in d: p.add("Band_Leaf_Crests", LF, *[crest((x, 6.5 - E, .16)) for x in (-1.5, -.5, .5, 1.5)])
    if "louvres" in d:   # exterior leaf-blade louvres on the F2 storey, standing on the slab band, alloy
        L = []
        for x in np.arange(-h + .3, h - .2, .4):
            L.append(trimesh.convex.convex_hull(np.array([(x + dx, y, z) for y in (6.6 - E, 11.9 + E) for (dx, z) in ((-.012, .28), (.012, .28), (-.012, .5), (.012, .5), (0, .62), (0, .22))])))
        for m in L: m.metadata["uv"] = m.vertices[:, [2, 1]]
        p.add("Leaf_Louvres", ALY, *L, box(X0, X1, 11.9, 12.0, .2, .64), box(X0, X1, 6.5 + .002, 6.6, .2, .64))
        p.add("Louvre_Brackets", G, *[box(x - .03, x + .03, y0, y1, .1, .2 + E) for x in (-1.2, 1.2) for (y0, y1) in ((6.5 + .002, 6.6), (11.9, 12.0))])
    if "vine" in d:
        st, lv = vine([(X0 + .05, 6.25, .19 + .012 - E), (0, 6.2, .19 + .012 - E), (X1 - .05, 6.25, .19 + .012 - E)], r=.014, leaf_every=.28, leaf_len=.24, seed=6, outward=True)
        p.add("Band_Vine", LF, st); p.add("Band_Vine_Leaves", LF2, lv)
        for x in (-1.4, .1, 1.3):
            s2, l2 = vine([(x, 5.9, .19 + .012 - E), (x + .1, 5.2, .1 + .014), (x - .05, 4.4, .1 + .014)], r=.012, leaf_every=.25, leaf_len=.2, seed=int(abs(x)*10) + 9, outward=True)
            p.add("Trailing_Vine", LF, s2); p.add("Trailing_Vine_Leaves", LF2, l2)
    if "bollards" in d:
        for x in (-1.0, 1.0): p.add("Court_Ball_Lamps", BA, node((x, .45 + .1 - E, .25), .1, 1)), p.add("Lamp_Posts", G, tube((x, .45 - E, .13), (x, .45 + .02, .25), .03, 6))
    return p
GG = ("glass", "glass")
VARIANTS = [
    dict(label="Branch Glass: glazed F1+F2, layered slab band, leaf crests", cells=[("slate", "slate"), GG, GG, GG], dress=("crests",)),
    dict(label="Court Line Slate: slate F1 with amber court-line inlays, glass F2, crests", cells=[("court", "court"), ("court", "court"), GG, ("glass", "slate")], dress=("crests",), amber=True),
    dict(label="Green Band: green-wall F1 panels, glass above, trailing vines off the slab band", cells=[("green", "green"), GG, GG, GG], dress=("vine",)),
    dict(label="Leaf Louvre: glass + slate F1, exterior alloy leaf louvres over F2", cells=[("slate", "slate"), GG, GG, GG], dress=("louvres",)),
    dict(label="Sports Relief: slate F1 with racket + ball relief, court-line panels, glass F2", cells=[("mural", "court"), GG, GG, ("court", "glass")], dress=("crests", "vine")),
]

def sheet(rep, seams):
    rdir = os.path.join(RENDER_OUT, "facade_bay"); fig, axs = plt.subplots(3, 5, figsize=(28, 19), facecolor="#F4F2EC")
    Ry = lambda el, az: (lambda a, b: np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]) @ np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]))(np.radians(az), np.radians(el))
    for i, (prm, r) in enumerate(zip(VARIANTS, rep)):
        p = recenter(build(prm)); _, geo = export_final(p.P, [f"/tmp/fb_{i}.glb"])
        for row, (el, az) in enumerate(((6, 35), (25, -65))):
            im = crop(render_view(geo, Ry(el, az), size=760, shadow=False, glass_alpha=.35)); axs[row, i].imshow(np.clip(im, 0, 1)); axs[row, i].axis("off")
            plt.imsave(os.path.join(rdir, f"v{i+1}_{['front34', 'side'][row]}.png"), np.clip(im, 0, 1))
        A = Part()
        for k in range(3):
            for n, (mk, m) in build(prm).P.items():
                m2 = m.copy(); m2.apply_translation((k*W, 0, 0)); m2.metadata["uv"] = m.metadata.get("uv", np.zeros((len(m.vertices), 2))); A.add(f"B{k}_{n}", mk, m2)
        _, g2 = export_final(A.P, [f"/tmp/fbs_{i}.glb"]); im = crop(render_view(g2, Ry(10, 25), size=900, shadow=False, glass_alpha=.35))
        plt.imsave(os.path.join(rdir, f"v{i+1}_3bays.png"), np.clip(im, 0, 1)); axs[2, i].imshow(np.clip(im, 0, 1)); axs[2, i].axis("off")
        a, b = prm["label"].split(": ")
        axs[0, i].set_title(f"v{i+1}  {a}\n{b}\n{r['tris']} tris | {'PASS' if r['passed'] else 'FAIL'} | pair {'PASS' if seams[i] else 'FAIL'}", fontsize=10)
    for row, t in enumerate(("low 3/4 (F1 + F2, 12.2 m)", "high side (fins / slab band depth)", "3 bays tiled (12 m)")): axs[row, 0].text(-.02, .5, t, transform=axs[row, 0].transAxes, rotation=90, va="center", ha="right", fontsize=12)
    fig.suptitle("Rook | Tennis Tower generic F1-F2 façade bay V1-V5 | 4.0 m x 12.2 m, under the F3 Glass Box | candidates (not promoted)", fontsize=15)
    plt.tight_layout(rect=(0, 0, 1, .95)); sp = os.path.join(rdir, "facade_bay_contact_sheet.png"); fig.savefig(sp, dpi=80, facecolor="#F4F2EC"); plt.close(fig); print("SHEET", sp)
def pair_check(prm):
    A = {}
    for k in range(2):
        for n, (mk, m) in build(prm).P.items():
            m2 = m.copy(); m2.apply_translation((k*W, 0, 0)); A[f"T{k}_{n}"] = (mk, m2)
    near = {k: v for k, v in A.items() if v[1].bounds[1][0] > h - .6 and v[1].bounds[0][0] < h + .6}
    chk = cc.check(near, n_samp=300); bad = [o for o in chk["overlap"] if not o[3] and o[0][:2] != o[1][:2]]; cop = [c for c in chk["coplanar"] if c[0][:2] != c[1][:2]]
    print("PAIR", bad[:3], cop[:3]); return not bad and not cop
if __name__ == "__main__":
    rep = run("facade_bay", build, VARIANTS, title="F1-F2 facade bay", sheet="facade_bay_run_sheet.png")
    seams = [pair_check(v) for v in VARIANTS]; json.dump(rep, open(os.path.join(RENDER_OUT, "facade_bay", "report.json"), "w"), indent=1, default=str); sheet(rep, seams)
