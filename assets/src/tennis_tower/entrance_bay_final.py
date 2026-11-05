"""Rook: #74 F1 W main-entrance bay, final (Jared pick V3 Court Wayfinding, thickened). 4.0 m bay + 2.0 m half bay (42 m = 10 x 4.0 + 1 x 2.0).
Layered: 3-step slate/gunmetal fascia with amber court line, deep alloy soffit with cyan downlight strips, double-sided wayfinding blade
(gunmetal frame, slate core, glyphs both faces, court stripe, ball finial, leaf crest), slate kerb along the terrace mat front with
low hedge clumps + flowers (planted edge, no planter boxes), ball bollards. Tiles along X. +Z = terrace. Run: python3 entrance_bay_final.py"""
from modlib import *
from restroom_extras import crest
H, TD, T2 = 6.1, 2.6, 4.35
def build(q):
    w = q.get("width", 4.0); h = w/2; X0, X1 = -h + .001, h - .001; p = Part()
    hf = -h + .06; jb = (h - .045, h - .01)
    F = [box(X0, X1, 0, .05, -.65, .12), box(X0, X1, H - .15, H, -.65, .08), fin(hf, .05 - E, H - .15 + E, .6, .05, z0=.03), box(*jb, .05 - E, H - .15 + E, -.04, .04)]
    cols = [(hf + .025, jb[0])]
    if w > 3: F.append(box(-.05, .05, .05 - E, H - .15 + E, -.05, .05)); cols = [(hf + .025, -.05), (.05, jb[0])]
    for t in (TD, T2): F.append(box(hf + .025 - E, jb[0] + E, t - .075, t + .075, -.06, .06))
    p.add("Frame", G, *F)
    for i, (a0, b0) in enumerate(cols):
        a, b = a0 + .003, b0 - .003; m = (a + b)/2; S = [box(a, a + .07, .06, TD - .08, -.03, .03), box(b - .07, b, .06, TD - .08, -.03, .03), box(m - .035, m + .035, .06, TD - .08, -.03, .03)]
        S += [box(a + .07 - E, b - .07 + E, u, v, -.03, .03) for (u, v) in ((.06, .18), (TD - .2, TD - .08))]
        p.add("Door_Stiles", ALY, *S)
        for k, (u, v) in enumerate(((a + .07, m - .035), (m + .035, b - .07))):
            p.add(f"Glass_Door_{i}{k}", GL, pane(u + .002, v - .002, .18 - E, TD - .2 + E, 0, t=.016))
            p.add("Push_Bars", ALY, tube((u + .12, 1.05, .07), (v - .12, 1.05, .07), .02, 8), tube((u + .12, 1.05, .03 - E), (u + .12, 1.05, .07), .012, 6), tube((v - .12, 1.05, .03 - E), (v - .12, 1.05, .07), .012, 6))
        for r, (y0, y1) in enumerate(((TD + .075, T2 - .075), (T2 + .075, H - .15))): p.add(f"Glass_Upper_{i}{r}", GL, pane(a0 + .002, b0 - .002, y0 - E, y1 + E, 0))
    # ---- canopy: slab + deep soffit + 3-step fascia ----
    y0, y1, zt = 3.0, 3.16, 2.6; cx0, cx1 = X0 + .02, X1 - .02
    p.add("Canopy", SL, box(cx0, cx1, y0, y1, .061, zt), box(-h + .05, -h + .12, y0 - .34, y1 + E, .061 - E, .6), box(h - .12, h - .05, y0 - .34, y1 + E, .061 - E, .6))
    p.add("Canopy_Soffit", ALY, box(-h + .123, h - .123, y0 - .12, y0 + E, .3, zt - .02), box(-h + .123, h - .123, y0 - .06, y0 + E, .63, .3 + E))
    p.add("Soffit_Downlights", CY, *[box(cx0 + .2, cx1 - .2, y0 - .128, y0 - .12 + E, z, z + .04) for z in (.9, 1.5, 2.1)])
    p.add("Fascia_Slate", SL, box(cx0, cx1, y0 - .26, y1 + .06, zt - E, zt + .1))
    p.add("Fascia_Gunmetal", G, box(cx0, cx1, y0 - .16, y1 + .02, zt + .1 - E, zt + .18), box(cx0, cx1, y1 + .06 - E, y1 + .12, zt - .3, zt + .1 - .003))
    p.add("Court_Line_LED", AM, box(cx0, cx1, y0 - .26 - E, y0 - .23, zt + .1 - E, zt + .11), box(cx0, cx1, y0 - .06, y0 - .03, zt + .18 - E, zt + .19), box(cx0, cx1, y1 - E, y1 + .006, .3, .34))
    for x in (-h*.65, h*.65): p.add("Tie_Rods", ST, tube((x, 5.4, .06 - E), (x, y1 - E, zt - .4), .028, 6))
    # ---- wayfinding blade (double-sided) ----
    by0, by1, bz0, bz1 = y1 + .12 - E, y1 + 1.0, zt - .55, zt - .05
    p.add("Blade_Core", SL, box(-.05, .05, by0 + .046, by1 + .004, bz0, bz1))
    p.add("Blade_Frame", G, box(-.065, .065, by1 - E, by1 + .05, bz0 - .015, bz1 + .015), box(-.065, .065, by0, by0 + .05, bz0 - .015, bz1 + .015),
          box(-.065, .065, by0 + .03, by1 + .02, bz1 - .01, bz1 + .015), box(-.065, .065, by0 + .03, by1 + .02, bz0 - .015, bz0 + .01))
    G2 = []
    for sx in (-1, 1):
        o = sx*.05; d = (lambda u, v: (min(o + sx*.012, o - sx*.004), max(o + sx*.012, o - sx*.004)))(0, 0)
        G2 += [box(*d, by0 + .48, by0 + .78, bz0 + .2, bz0 + .25), box(*d, by0 + .36, by0 + .42, bz0 + .2, bz0 + .42), box(*d, by0 + .12, by0 + .2, bz0 + .05, bz1 - .05)]
    p.add("Wayfinding_Glyphs", CY, *G2[:2], *G2[3:5]); p.add("Blade_Court_Stripe", AM, G2[2], G2[5])
    p.add("Blade_Ball_Finial", BA, node((0, by1 + .05 + .08 - E, (bz0 + bz1)/2 - .12), .08, 1))
    p.add("Blade_Leaf_Crest", LF, crest((0, by1 + .05 - E, (bz0 + bz1)/2 + .12)))
    p.add("Fascia_Leaf_Crests", LF, *[crest((x, y1 + .12 - E, zt - .1)) for x in np.arange(-h + .4, h - .3, .8) if abs(x) > .3])
    # ---- terrace mat + planted edge on a slate kerb (no boxes: a 0.08 kerb strip, hedge + flowers on top) ----
    p.add("Threshold_Mat", SSL, box(X0 + .02, X1 - .02, 0, .012, .122, 1.4))
    p.add("Terrace_Kerb", SL, box(X0 + .02, X1 - .02, 0, .08, 1.402, 1.7))
    xs = [x for x in np.arange(-h + .25, h - .15, .3) if all(abs(x - b) > .24 for b in (-h*.5, h*.5))]
    p.add("Hedge_Edge", LF, *[clump((x, .08 + .17 - E*3, 1.55), .19, i) for i, x in enumerate(xs)])
    L2 = [clump((x + .15, .1 - E*3, 1.82), .1, 40 + i) for i, x in enumerate(xs[:-1]) if xs[i+1] - x < .35]
    if L2: p.add("Hedge_Edge_Light", LF2, *L2)
    for x in (-h*.5, h*.5):
        p.add("Ball_Bollards", G, tube((x, .08 - E, 1.55), (x, .85, 1.55), .1, 10)); p.add("Bollard_Balls", BA, node((x, .85 + .11 - E, 1.55), .11, 1))
    return p
VARIANTS = [dict(label="Court Wayfinding final: 4.0 m bay", width=4.0), dict(label="Court Wayfinding final: 2.0 m half bay", width=2.0)]
def run_layout(widths):
    A = {}; x = 0
    for k, w in enumerate(widths):
        x += w/2
        for n, (mk, m) in build(dict(width=w)).P.items():
            m2 = m.copy(); m2.apply_translation((x, 0, 0)); m2.metadata["uv"] = m.metadata.get("uv", np.zeros((len(m.vertices), 2))); A[f"T{k}_{n}"] = (mk, m2)
        x += w/2
    return A
def seam_check(widths):
    A = run_layout(widths); edge = widths[0]
    near = {k: v for k, v in A.items() if v[1].bounds[1][0] > edge - .6 and v[1].bounds[0][0] < edge + .6}
    chk = cc.check(near, n_samp=300); bad = [o for o in chk["overlap"] if not o[3] and o[0][:2] != o[1][:2]]; cop = [c for c in chk["coplanar"] if c[0][:2] != c[1][:2]]
    return dict(bad=bad[:3], coplanar=cop[:3], pass_=not bad and not cop)
if __name__ == "__main__":
    rep = run("entrance_bay_final", build, VARIANTS, title="F1 entrance bay final", sheet="entrance_bay_final_run_sheet.png")
    seams = {str(w): seam_check(w) for w in ([4, 4], [4, 2], [2, 4])}; print("SEAMS", seams)
    rdir = os.path.join(RENDER_OUT, "entrance_bay_final"); os.makedirs(rdir, exist_ok=True)
    Ry = lambda el, az: (lambda a, b: np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]) @ np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]))(np.radians(az), np.radians(el))
    fig = plt.figure(figsize=(26, 15), facecolor="#F4F2EC"); gs = fig.add_gridspec(2, 4)
    shots = [(0, (8, 35), "4.0 m bay, low 3/4"), (0, (30, -60), "4.0 m bay, high side (canopy depth)"), (0, (-8, 20), "4.0 m bay, soffit from below"), (1, (8, 35), "2.0 m half bay")]
    for j, (vi, (el, az), t) in enumerate(shots):
        p = recenter(build(VARIANTS[vi])); _, geo = export_final(p.P, [f"/tmp/ebf_{j}.glb"]); im = crop(render_view(geo, Ry(el, az), size=760, shadow=False, glass_alpha=.35))
        ax = fig.add_subplot(gs[0, j]); ax.imshow(np.clip(im, 0, 1)); ax.axis("off"); ax.set_title(f"{t}\n{rep[vi]['tris']} tris | {'PASS' if rep[vi]['passed'] else 'FAIL'}", fontsize=11)
    Pt = Part()
    for n, (mk, m) in run_layout([4, 4, 2, 4, 4]).items(): Pt.add(n, mk, m)
    _, g2 = export_final(Pt.P, ["/tmp/ebf_run.glb"]); im = crop(render_view(g2, Ry(12, 22), size=1400, shadow=False, glass_alpha=.35))
    ax = fig.add_subplot(gs[1, :]); ax.imshow(np.clip(im, 0, 1)); ax.axis("off"); ax.set_title(f"run 4+4+2+4+4 m (18 m of the 42 m door run) | seams 4|4, 4|2, 2|4: {'PASS' if all(s['pass_'] for s in seams.values()) else 'FAIL'}", fontsize=12)
    fig.suptitle("Rook | #74 tt_entrance_bay (V3 Court Wayfinding, thickened) + tt_entrance_bay_half | FINAL", fontsize=15)
    plt.tight_layout(rect=(0, 0, 1, .95)); sp = os.path.join(rdir, "entrance_bay_final_sheet.png"); fig.savefig(sp, dpi=90, facecolor="#F4F2EC"); print("SHEET", sp)
