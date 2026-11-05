"""Rook: Tennis Tower F1 W-face main-entrance bay (spec §3.3 / §3.6 / §5.3 Rev 2.7: 42 m of main-entrance doors on the W face, Z 18.5..60.5,
level onto the +4.0 HD West Arrival terrace; F1 storey 0..6.1). One 4.0 m façade-module bay (§3.11.1 grid), tiles along the façade
(local X), +Z = exterior/terrace, glass line z 0, fins inside (-Z) like the #52 curtain wall. Pair of 1.85 m glass door leaves per bay
(2 x 0.93 m clear each leaf pair -> 42 m of doors = 10.5 bays). Matches #52 Branch Fin, #53 Leaf Capital, #57 Court Wayfinding, #58 Leaf Crest.
No wood, no planter boxes. Glass = BLEND (the envelope layer). Run: python3 entrance_bay.py"""
from modlib import *
from restroom_extras import crest
H, W = 6.1, 4.0; X0, X1 = -W/2 + .001, W/2 - .001
TD, T2 = 2.6, 4.35      # door head transom, upper transom
def frame(p, q):
    p.add("Frame", G, box(X0, X1, 0, .05, -.65, .12)); p.add("Frame", G, box(X0, X1, H - .15, H, -.65, .08))
    hf = (-1.965, -1.915); p.add("Frame" if q.get("fin") != "slate" else "Heavy_Fin_Slate", G if q.get("fin") != "slate" else SL, fin(sum(hf)/2, .05 - E, H - .15 + E, .6, .05, z0=.03))
    p.add("Frame", G, box(1.955, 1.99, .05 - E, H - .15 + E, -.04, .04)); p.add("Frame", G, box(-.05, .05, .05 - E, H - .15 + E, -.05, .05))
    for t in (TD, T2): p.add("Frame", G, box(-1.915 - E, 1.955 + E, t - .075, t + .075, -.06, .06))
    for i, (a, b) in enumerate(((-1.912, -.047), (.053, 1.952))):
        m = (a + b)/2; S = []
        for (u, v) in ((a, a + .07), (b - .07, b), (m - .035, m + .035)): S.append(box(u, v, .06, TD - .08, -.03, .03))
        for (u, v) in ((.06, .18), (TD - .2, TD - .08)): S.append(box(a + .07 - E, b - .07 + E, u, v, -.03, .03))
        p.add("Door_Stiles", ALY if q.get("frame") == "alloy" else G, *S)
        for (u, v) in ((a + .07, m - .035), (m + .035, b - .07)): p.add(f"Glass_Door_{i}", GL, pane(u + .002, v - .002, .18 - E, TD - .2 + E, 0, t=.016))
        p.add("Push_Bars", ALY, tube((a + .2, 1.05, .06), (b - .2, 1.05, .06), .02, 8), tube((a + .2, 1.05, .03 - E), (a + .2, 1.05, .06), .012, 6), tube((b - .2, 1.05, .03 - E), (b - .2, 1.05, .06), .012, 6))
    if q.get("spandrel"):
        p.add("Spandrel_Panel", SL, box(-1.913, -.052, T2 + .075 - E, H - .15 + E, -.03, .03), box(.052, 1.953, T2 + .075 - E, H - .15 + E, -.03, .03))
        p.add("Green_Wall", LF, green_wall(-1.88, 1.92, T2 + .12, H - .2, .03, r=.14, seed=3))
    else:
        for k, (a, b) in enumerate(((-1.915, -.05), (.05, 1.955))): p.add(f"Glass_Upper_{k}", GL, pane(a + .002, b - .002, T2 + .075 - E, H - .15 + E, 0))
    for k, (a, b) in enumerate(((-1.915, -.05), (.05, 1.955))): p.add(f"Glass_Mid_{k}", GL, pane(a + .002, b - .002, TD + .075 - E, T2 - .075 + E, 0))
    p.add("Threshold_Mat", SSL, box(X0 + .02, X1 - .02, 0, .012, .12 + .002, 1.4))
def canopy(p, q):
    c = q["canopy"]; y0, y1, zt = 3.0, 3.14, 2.6
    if c in ("branch", "court", "green"):
        cm = SL if c != "branch" else G; p.add("Canopy", cm, box(X0 + .02, X1 - .02, y0, y1, .061, zt))
        p.add("Canopy_Fascia", ALY if c == "court" else G, box(X0 + .02, X1 - .02, y0 - .1, y1 + .04, zt - E, zt + .08))
        p.add("Canopy", cm, box(-1.95, -1.88, y0 - .3, y1 + E, .061 - E, .5), box(1.88, 1.95, y0 - .3, y1 + E, .061 - E, .5))
        for x in (-1.3, 1.3):
            if c == "branch":   # Y-fork branch hanger from the head (Leaf Capital / Branch Fin echo)
                h = (x, 5.2, .25); p.add("Branch_Hangers", G, tube((x, 5.2, .06 - E), h, .05, 8), node(h, .08, 0), tube(h, (x - .5, y1 - E, zt - .2), .035, 6), tube(h, (x + .5, y1 - E, zt - .2), .035, 6))
            elif c == "court": p.add("Tie_Rods", ST, tube((x, 5.4, .06 - E), (x, y1 - E, zt - .15), .025, 6))
        if c == "court":
            p.add("Court_Line_LED", AM, box(X0 + .02, X1 - .02, y0 - .1 - E, y0 - .07, zt + .08 - E, zt + .09), box(X0 + .02, X1 - .02, y1 - E, y1 + .006, .3, .34))
            p.add("Wayfinding_Blade", SL, box(-.06, .06, y1 + .04 - E, y1 + .74, zt - .4, zt - .05))
            p.add("Wayfinding_Glyph", CY, *[box(sx*.06 - (.004 if sx > 0 else .01), sx*.06 + (.01 if sx > 0 else .004), yy0, yy1, za, zb) for sx in (-1, 1) for (yy0, yy1, za, zb) in ((y1 + .32, y1 + .62, zt - .33, zt - .29), (y1 + .2, y1 + .26, zt - .33, zt - .12))])
            p.add("Ball_Finial", BA, node((0, y1 + .74 + .07 - E, zt - .225), .07, 1))
        if c in ("branch", "court"): p.add("Fascia_Leaf_Crests", LF, *[crest((x, y1 + .04 - E, zt + .04)) for x in np.arange(-1.6, 1.7, .8) if c == "branch" or abs(x) > .1])
        if c == "green":
            st, lv = vine([(X0 + .05, y0 + .02, zt + .094 - E), (0, y0 + .02, zt + .094 - E), (X1 - .05, y0 + .02, zt + .094 - E)], r=.014, leaf_every=.3, leaf_len=.22, seed=4, outward=True)
            p.add("Fascia_Vine", LF, st); p.add("Fascia_Vine_Leaves", LF2, lv)
            p.add("Canopy_Moss", LF, *[clump((x, y1 + .1 - E, z), .12, i) for i, (x, z) in enumerate([(x, z) for x in np.arange(-1.6, 1.7, .8) for z in (.6, 1.4, 2.2)])])
    if c == "leaf":     # layered leaf-blade canopy, two blades at two heights, hung from branch stems
        for k, (x, y, Ls, Wd, m) in enumerate(((-.9, 3.4, 2.7, 1.8, LF), (.95, 3.0, 2.5, 1.7, LF2))):
            p.add(f"Leaf_Canopy_{k}", m, leaf((x, y, .061), Ls, Wd, pitch=np.pi/2 - .06, t=.08))
            r = (x, y + .3, Ls*.55); p.add("Frame", G, tube((x, y + .11, .3), (x, 5.3, .06 - E), .05, 8), tube((x, y + .14, Ls*.3), (x, 5.25, .07), .03, 6))
    if c == "racket":   # racket-head arch over the doors: oval tube frame, string grid, ball keystone
        a = np.linspace(0, np.pi, 13); P = [(1.82*np.cos(t), 2.75 + 2.6*np.sin(t), .28) for t in a]
        p.add("Racket_Frame", ALY, *[tube(P[i], P[i+1], .07, 8) for i in range(len(P) - 1)], *[node(P[i], .07, 0) for i in range(len(P))])
        p.add("Racket_Frame", ALY, tube((1.82, .1, .28), P[0], .07, 8), tube((-1.82, .1, .28), P[-1], .07, 8), node((1.82, .012 + .1 - E, .28), .1, 0), node((-1.82, .012 + .1 - E, .28), .1, 0))
        S = []
        for x in np.arange(-1.5, 1.6, .5):
            yt = 2.75 + 2.6*np.sqrt(max(0, 1 - (x/1.82)**2)) - .175; S.append(box(x - .01, x + .01, 3.195, yt, .27, .29))
        for y in np.arange(3.4, 5.2, .45):
            xh = 1.82*np.sqrt(max(0, 1 - ((y - 2.75)/2.6)**2)) - .175; S.append(box(-xh, xh, y - .01, y + .01, .292, .31))
        p.add("Racket_Strings", WH, *S); p.add("Racket_Frame", ALY, box(-1.8, 1.8, 3.1, 3.2, .21, .35)); p.add("Ball_Keystone", BA, node((0, 5.35 + .07 + .14 - E, .28), .14, 1))
        p.add("Leaf_Crests", LF, *[crest((x, 3.2 - E, .28)) for x in (-1.2, -.4, .4, 1.2)])
    if q.get("bollards"):
        for x in (-1.0, 1.0):
            p.add("Ball_Bollards", G, tube((x, .012 - E, 1.9), (x, .85, 1.9), .1, 10)); p.add("Bollard_Balls", BA, node((x, .85 + .11 - E, 1.9), .11, 1))
def build(q):
    p = Part(); frame(p, q); canopy(p, q); return p
VARIANTS = [
    dict(label="Branch Fin Portal: Y-fork branch hangers, gunmetal canopy, leaf crest fascia", canopy="branch"),
    dict(label="Leaf Canopy: two layered leaf-blade canopies on branch stems", canopy="leaf"),
    dict(label="Court Wayfinding: slate canopy, amber court lines, wayfinding blade, ball bollards", canopy="court", frame="alloy", bollards=True),
    dict(label="Green Portal: green-wall spandrel, mossy canopy, vine fascia", canopy="green", spandrel=True),
    dict(label="Racket Arch: racket-head arch with strings, ball keystone, leaf crests", canopy="racket", fin="slate"),
]
def sheet(rep):
    rdir = os.path.join(RENDER_OUT, "entrance_bay"); fig, axs = plt.subplots(3, 5, figsize=(28, 16), facecolor="#F4F2EC")
    Ry = lambda el, az: (lambda a, b: np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]) @ np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]))(np.radians(az), np.radians(el))
    for i, (prm, r) in enumerate(zip(VARIANTS, rep)):
        p = recenter(build(prm)); _, geo = export_final(p.P, [f"/tmp/eb_{i}.glb"])
        for row, (el, az) in enumerate(((8, 35), (28, -60))):
            im = crop(render_view(geo, Ry(el, az), size=760, shadow=False, glass_alpha=.35)); axs[row, i].imshow(np.clip(im, 0, 1)); axs[row, i].axis("off")
            plt.imsave(os.path.join(rdir, f"v{i+1}_{['front34', 'side'][row]}.png"), np.clip(im, 0, 1))
        A = Part()
        for k in range(3):
            for n, (mk, m) in build(prm).P.items():
                m2 = m.copy(); m2.apply_translation((k*W, 0, 0)); m2.metadata["uv"] = m.metadata.get("uv", np.zeros((len(m.vertices), 2))); A.add(f"B{k}_{n}", mk, m2)
        _, g2 = export_final(A.P, [f"/tmp/ebs_{i}.glb"]); im = crop(render_view(g2, Ry(14, 25), size=900, shadow=False, glass_alpha=.35))
        plt.imsave(os.path.join(rdir, f"v{i+1}_3bays.png"), np.clip(im, 0, 1)); axs[2, i].imshow(np.clip(im, 0, 1)); axs[2, i].axis("off")
        a, b = prm["label"].split(": ")
        axs[0, i].set_title(f"v{i+1}  {a}\n{b}\n{r['tris']} tris | {'PASS' if r['passed'] else 'FAIL'} | pair {'PASS' if r['pair']['pass_'] else 'FAIL'}", fontsize=10)
    for row, t in enumerate(("low 3/4 from the terrace", "high side (depth: fins / canopy)", "3 bays tiled (12 m of the 42 m door run)")): axs[row, 0].text(-.02, .5, t, transform=axs[row, 0].transAxes, rotation=90, va="center", ha="right", fontsize=12)
    fig.suptitle("Rook | Tennis Tower F1 W main-entrance bay V1-V5 | 4.0 m module, F1 0..6.1, +Z terrace | candidates (not promoted)", fontsize=15)
    plt.tight_layout(rect=(0, 0, 1, .95)); sp = os.path.join(rdir, "entrance_bay_contact_sheet.png"); fig.savefig(sp, dpi=90, facecolor="#F4F2EC"); plt.close(fig); print("SHEET", sp)
def pair_check(prm):
    A = {}
    for k in range(2):
        for n, (mk, m) in build(prm).P.items():
            m2 = m.copy(); m2.apply_translation((k*W, 0, 0)); A[f"T{k}_{n}"] = (mk, m2)
    near = {k: v for k, v in A.items() if v[1].bounds[1][0] > W/2 - .6 and v[1].bounds[0][0] < W/2 + .6}
    chk = cc.check(near, n_samp=300); bad = [o for o in chk["overlap"] if not o[3] and o[0][:2] != o[1][:2]]; cop = [c for c in chk["coplanar"] if c[0][:2] != c[1][:2]]
    return dict(bad=bad[:3], coplanar=cop[:3], pass_=not bad and not cop)
if __name__ == "__main__":
    rep = run("entrance_bay", build, VARIANTS, title="F1 entrance bay 4.0 m", sheet="entrance_bay_run_sheet.png")
    for r, prm in zip(rep, VARIANTS): r["pair"] = pair_check(prm); print("PAIR", r["v"], r["pair"])
    json.dump(rep, open(os.path.join(RENDER_OUT, "entrance_bay", "report.json"), "w"), indent=1, default=str); sheet(rep)
