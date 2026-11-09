"""Rook: #78 S/N/E secondary entrance FINAL (Jared pick V5 Rally Mark, densified).
8.0 m × 6.1 m F1 module. Three face assets (_s/_n/_e) with sculpted bevelled glyphs.
Density: racket-arch string relief, ball finials with seams, layered scoreboard, net-pattern
kick panels, seated greenery (no planter boxes, no wood). Promote as
tt_secondary_entrance_{s,n,e}.glb. Skirt under entrance: 2+4+2 m so no seam at door centreline.
Run: python3 secondary_entrance_final.py"""
from modlib import *
from restroom_extras import crest
import secondary_entrance as SE
import facade_bay_final as FB
from secondary_entrance import canopy_base, doors, frame_base, planted_edge, door_clear, seam_with_facade, H, W0
from structure.struct_lib import SCR, finish_scissor
H, W0 = SE.H, SE.W0
def stroke(x0, x1, y0, y1, z0, z1, bev=.006):
    """Bevelled rectangular stroke: core + raised face inset by bev (holds up close)."""
    return [box(x0, x1, y0, y1, z0, z1),
            box(x0 + bev, x1 - bev, y0 + bev, y1 - bev, z1 - E, z1 + .008)]
def glyph_sculpted(face, cx, y0, y1, z_face, sx=1, thick=.028, w=.22):
    """Sculpted bevelled S/N/E letter standing on the scoreboard +Z face. Returns meshes."""
    # local letter box: width w, height (y1-y0), extruded along +Z from z_face
    zh0, zh1 = z_face, z_face + thick
    midy = (y0 + y1) / 2; t = .055  # stroke thickness in Y/X
    # letter centred at cx; sx flips for a mirrored face if needed (unused for +Z-only board)
    def X(a, b): return (cx + a, cx + b) if sx > 0 else (cx - b, cx - a)
    M = []
    if face == "S":
        # top bar, upper vertical (right), mid bar, lower vertical (left), bottom bar
        for (a, b, u, v) in [(-w/2, w/2, y1 - t, y1),           # top
                             (w/2 - t, w/2, midy, y1 - t + E),   # UR vert
                             (-w/2, w/2, midy - t/2, midy + t/2),# mid
                             (-w/2, -w/2 + t, y0 + t - E, midy), # LL vert
                             (-w/2, w/2, y0, y0 + t)]:           # bottom
            xa, xb = X(a, b); M += stroke(xa, xb, u, v, zh0, zh1)
    elif face == "N":
        for (a, b, u, v) in [(-w/2, -w/2 + t, y0, y1),           # left vert
                             (w/2 - t, w/2, y0, y1)]:            # right vert
            xa, xb = X(a, b); M += stroke(xa, xb, u, v, zh0, zh1)
        # diagonal: stepped boxes approximating a bevelled diagonal
        n = 5
        for i in range(n):
            yy0 = y0 + (y1 - y0) * i / n; yy1 = y0 + (y1 - y0) * (i + 1) / n
            xx0 = -w/2 + t/2 + (w - t) * i / n; xx1 = xx0 + (w - t) / n + t * .6
            xa, xb = X(xx0, xx1); M += stroke(xa, xb, yy0, yy1, zh0, zh1, bev=.004)
    else:  # E
        for (a, b, u, v) in [(-w/2, -w/2 + t, y0, y1),           # spine
                             (-w/2 + t - E, w/2, y1 - t, y1),    # top
                             (-w/2 + t - E, w/2 * .55, midy - t/2, midy + t/2),  # mid
                             (-w/2 + t - E, w/2, y0, y0 + t)]:   # bottom
            xa, xb = X(a, b); M += stroke(xa, xb, u, v, zh0, zh1)
    return M
def racket_head(cx, cy, cz, rx=.38, ry=.30, strings=True):
    """Oval racket head + optional string grid relief."""
    oval = [(cx + rx * np.cos(t), cy + ry * np.sin(t), cz) for t in np.linspace(0, 2 * np.pi, 13)]
    M = [tube(a, b, .02, 5) for a, b in zip(oval[:-1], oval[1:])]
    if strings:
        # vertical strings
        for fx in np.linspace(-.55, .55, 3):
            pts = [(cx + fx * rx * .7, cy + ry * np.sin(t) * .8, cz + .006) for t in np.linspace(-.85, .85, 4)]
            M += [tube(a, b, .006, 4) for a, b in zip(pts[:-1], pts[1:])]
        for fy in np.linspace(-.5, .5, 3):
            pts = [(cx + rx * np.cos(t) * .8, cy + fy * ry * .7, cz + .006) for t in np.linspace(.25, np.pi - .25, 4)]
            M += [tube(a, b, .006, 4) for a, b in zip(pts[:-1], pts[1:])]
    return M
def build(q):
    face = q.get("face", "S"); w = q.get("width", W0)
    h = w / 2; X0, X1 = -h + .001, h - .001; p = Part()
    rng = np.random.default_rng(q.get("seed", 17))
    cols = [(-h + .2, -.15), (.15, h - .2)] if w > 6 else [(-h + .15, h - .15)]
    frame_base(p, X0, X1, cols)
    doors(p, cols)
    p.add("Plinth_Court_Line", AM,
          box(X0 + .08, -2.4, .18, .22, .28 - E, .287),
          box(-2.3, 2.3, .18, .22, .28 - E, .287),
          box(2.4, X1 - .08, .18, .22, .28 - E, .287))
    y1, zt = canopy_base(p, X0, X1, zt=2.15)
    # ---- racket arches with string relief (lean) + throat ----
    arch = []
    for sx in (-1, 1):
        throat = [(sx * 1.55, y1 + .12, zt + .02), (sx * 1.35, y1 + .28, zt + .05), (sx * 1.15, y1 + .42, zt + .07)]
        arch += [tube(a, b, .026, 6) for a, b in zip(throat[:-1], throat[1:])]
        arch += racket_head(sx * 1.15, y1 + .55, zt + .08, rx=.34, ry=.26, strings=True)
    p.add("Racket_Arch", ALY, *arch)
    # ---- ball finials (seams merged into Ball_Cluster) + leaf crest ----
    Fin, Crests = [], []
    for x in (-2.55, 2.55):  # outer only — clears scoreboard
        c = (x, y1 + .12 + .09 - E, zt - .02)
        Fin.append(node(c, .085, 1))
        for sgn in (-1, 1):
            pts = [(c[0] + sgn * .055 * np.cos(u), c[1] + .065 * np.sin(u), c[2] + .035 * (1 - abs(np.sin(u)))) for u in np.linspace(-1.0, 1.0, 5)]
            Fin += [tube(a, b, .007, 4) for a, b in zip(pts[:-1], pts[1:])]  # seams same part
        Crests.append(crest((x, y1 + .12 + .09 + .1, zt + .04)))
    p.add("Ball_Cluster", BA, *Fin)
    p.add("Finial_Crests", LF, *Crests)
    # ---- layered scoreboard, raised clear of fascia top (fascia to y1+.12, zt to zt+.18) ----
    by0, by1 = y1 + .14, y1 + 1.05
    bz0, bz1 = zt + .2, zt + .42   # entirely in front of fascia
    p.add("Scoreboard", SL,
          box(-.72, .72, by0, by1, bz0, bz1 - .03),
          box(-.74, .74, by1 - E, by1 + .04, bz0 - .015, bz1 + .015),
          box(-.74, .74, by0 - .015, by0 + .03, bz0 - .015, bz1 + .015),
          box(-.74, -.70, by0 + .015, by1 + .015, bz0 - .015, bz1 + .015),
          box(.70, .74, by0 + .015, by1 + .015, bz0 - .015, bz1 + .015))
    p.add("Scoreboard_Well", G, box(-.64, .64, by0 + .07, by1 - .07, bz1 - .03 - E, bz1 - .008))
    cells, bez, leds = [], [], []
    for x0 in (-.52, -.24, .06, .34):
        cells.append(box(x0, x0 + .2, by0 + .22, by1 - .32, bz1 - .006, bz1 + .01))
        bez += [box(x0 - .012, x0 + .212, by0 + .205, by0 + .22 + E, bz1 + .002, bz1 + .014),
                box(x0 - .012, x0 + .212, by1 - .32 - E, by1 - .305, bz1 + .002, bz1 + .014)]
        leds.append(box(x0 + .07, x0 + .13, by1 - .28, by1 - .26, bz1 + .008, bz1 + .014))
    p.add("Score_Cells", CY, *cells)
    p.add("Score_Bezels", ALY, *bez)
    p.add("Score_LEDs", AM, *leds)
    p.add("Score_Court_Line", AM, box(-.64, .64, by0 + .08, by0 + .115, bz1 + .002, bz1 + .01))
    # sculpted glyphs: twin plaques flanking scoreboard (x ±0.95), clear of balls at ±1.45/±2.55
    for gcx in (-.95, .95):
        gy0, gy1 = by0 + .12, by1 - .08
        p.add("Glyph_Plaque", SL, box(gcx - .18, gcx + .18, gy0 - .03, gy1 + .03, bz1 - .01, bz1 + .004))
        p.add("Glyph_Plaque_Frame", G,
              box(gcx - .195, gcx + .195, gy1 + .03 - E, gy1 + .055, bz1 - .02, bz1 + .016),
              box(gcx - .195, gcx + .195, gy0 - .055, gy0 - .03 + E, bz1 - .02, bz1 + .016),
              box(gcx - .195, gcx - .18 + E, gy0 - .03, gy1 + .03, bz1 - .02, bz1 + .016),
              box(gcx + .18 - E, gcx + .195, gy0 - .03, gy1 + .03, bz1 - .02, bz1 + .016))
        p.add("Wayfinding_Glyphs", CY, *glyph_sculpted(face, gcx, gy0, gy1, bz1 + .006, thick=.028, w=.26))
    # ---- net-pattern kick panels ----
    kicks = [box(a, b, .06, .38, .288, .318) for (a, b) in [(-2.0, -.4), (.4, 2.0)]]
    p.add("Kick_Panels", SL, *kicks)
    net = []
    for (a, b) in [(-2.0, -.4), (.4, 2.0)]:
        for y in np.linspace(.12, .34, 4):
            net.append(box(a + .03, b - .03, y - .004, y + .004, .318 - E, .328))
        for x in np.linspace(a + .2, b - .2, 5):
            net.append(box(x - .004, x + .004, .1, .36, .318 - E, .328))
    p.add("Net_Kick", WH, *net)
    p.add("Kick_Court_Line", AM, box(X0 + .15, -2.05, .36, .385, .318 - E, .33),
          box(-.35, .35, .36, .385, .318 - E, .33),
          box(2.05, X1 - .15, .36, .385, .318 - E, .33))
    # ---- planted edge + seated moss (lean) ----
    planted_edge(p, X0, X1, rng, z_mat=1.15, dense=True)
    moss = [clump((x, .012 + .035 - E*2, .5 + (i % 2) * .25), .05, 20 + i)
            for i, x in enumerate(np.arange(X0 + .6, X1 - .5, .7)) if abs(x) > .4]
    if moss: p.add("Mat_Moss", LF2, *moss)

    # colliders
    p.add("Wall-colonly", G, box(X0, X1, .5, H, -.08, .02))
    p.add("DoorClear-colonly", SL, box(X0, X1, 0, .02, -.3, 1.4))
    for a, b in cols:
        p.add("Jamb-colonly", G, box(a - .02, a + .02, 0, H, -.08, .14), box(b - .02, b + .02, 0, H, -.08, .14))
    p.add("Canopy-colonly", SL, box(X0 + .05, X1 - .05, 3.0, 3.16, .06, 2.0))
    p.add("Scoreboard-colonly", SL, box(-.74, .74, by0, by1 + .05, bz0, bz1 + .02))
    return p
FACES = ("S", "N", "E")
VARIANTS = [dict(label=f"Rally Mark final: face {f}", face=f, seed=17) for f in FACES]
def skirt_layout_check():
    """2+4+2 m plinth_skirt_terrace under the 8 m entrance: seams at ±3 m, NOT at door centreline x=0."""
    import plinth_skirt_final as PS
    from terrace_final import place
    PS.HT = 3.7
    A = {}
    # centre 4 m tile centred on door (x=0); 2 m halves at ±3
    for tag, w, x in (("C", 4.0, 0.0), ("L", 2.0, -3.0), ("R", 2.0, 3.0)):
        for n, (mk, m) in PS.build(dict(width=w, seed=7 if w > 3 else 12)).P.items():
            if "colonly" in n: continue
            m2 = m.copy(); m2.apply_translation((x, 0, 2.0))
            m2.metadata["uv"] = m.metadata.get("uv", np.zeros((len(m.vertices), 2)))
            A[f"{tag}_{n}"] = (mk, m2)
    PS.HT = 4.0
    chk = cc.check(A, n_samp=250)
    bad = [o for o in chk["overlap"] if not o[3] and o[0].split("_")[0] != o[1].split("_")[0] and o[2] > .0101]
    cop = [c for c in chk["coplanar"] if c[0].split("_")[0] != c[1].split("_")[0]]
    # also confirm no part straddles x=0 seam (centre tile owns |x|<2)
    return dict(pass_=not bad and not cop, bad=bad[:3], cop=cop[:3], layout="2+4+2", seams_at=(-3.0, 3.0))
def promote():
    for face in FACES:
        p = recenter(build(dict(face=face, seed=17)))
        gp = os.path.join(ROOT, "godot/assets/models", f"tt_secondary_entrance_{face.lower()}.glb")
        tris, _ = export_final(p.P, [gp]); finish_glb(gp); finish_scissor(gp)
        V = np.vstack([m.vertices for n, (mk, m) in p.P.items() if "colonly" not in n])
        lo, hi = V.min(0), V.max(0)
        print(f"tt_secondary_entrance_{face.lower()}.glb", "tris", int(tris), "bbox", lo.round(4).tolist(), hi.round(4).tolist())
if __name__ == "__main__":
    import terrace_final as TF, plinth_skirt_final as PS
    from terrace_final import place
    # temporarily point SE.build at ours for door_clear / seam helpers
    SE.build = build
    REP = run("secondary_entrance_final", build, VARIANTS, title="secondary entrance final",
              names=[f"tt_secondary_entrance_{f.lower()}" for f in FACES],
              sheet="secondary_entrance_final_run_sheet.png", post=finish_scissor)
    WK = {f: door_clear(dict(face=f, seed=17)) for f in FACES}
    SEAM = {f: seam_with_facade(dict(face=f, seed=17))[0] for f in FACES}
    SK = skirt_layout_check()
    print("CLEAR", {f: dict(pass_=WK[f]["pass_"], opens=WK[f]["opens"]) for f in FACES})
    print("SEAM_FACADE", SEAM, "SKIRT_2+4+2", SK)
    rdir = os.path.join(RENDER_OUT, "secondary_entrance_final")
    json.dump(dict(rep=REP, clear=WK, seam=SEAM, skirt=SK), open(os.path.join(rdir, "report.json"), "w"), indent=1, default=str)
    Ry = lambda el, az: (lambda a, b: np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]) @ np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]))(np.radians(az), np.radians(el))
    fig = plt.figure(figsize=(30, 24), facecolor="#F4F2EC"); gs = fig.add_gridspec(3, 4)
    # row 0: three faces + glyph close-up of S
    for j, f in enumerate(FACES):
        p = recenter(build(dict(face=f, seed=17))); _, geo = export_final(p.P, [f"/tmp/sef_{f}.glb"])
        geo = {k: v for k, v in geo.items() if "colonly" not in k}
        im = crop(render_view(geo, Ry(12, 30), size=800, shadow=False, glass_alpha=.35))
        ax = fig.add_subplot(gs[0, j]); ax.imshow(np.clip(im, 0, 1)); ax.axis("off")
        r = REP[j]; ax.set_title(f"tt_secondary_entrance_{f.lower()}\n{r['tris']} tris | {'PASS' if r['passed'] else 'FAIL'} | door {'PASS' if WK[f]['pass_'] else 'FAIL'} | façade seam {'PASS' if SEAM[f] else 'FAIL'}", fontsize=10)
    # glyph close-up: crop camera toward the left plaque
    p = recenter(build(dict(face="S", seed=17))); _, geo = export_final(p.P, ["/tmp/sef_glyph.glb"])
    geo = {k: v for k, v in geo.items() if "colonly" not in k}
    # shift view toward plaque by rendering high side
    im = crop(render_view(geo, Ry(5, -25), size=800, shadow=False, glass_alpha=.35))
    ax = fig.add_subplot(gs[0, 3]); ax.imshow(np.clip(im, 0, 1)); ax.axis("off")
    ax.set_title("glyph close-up (face S plaque)\nsculpted bevelled strokes", fontsize=10)
    # row 1: depth angles
    shots = [("S", (28, -55), "high side canopy + racket strings"), ("S", (-12, 20), "soffit from below"), ("E", (14, 40), "face E 3/4"), ("N", (10, -40), "face N 3/4")]
    for j, (f, (el, az), t) in enumerate(shots):
        p = recenter(build(dict(face=f, seed=17))); _, geo = export_final(p.P, [f"/tmp/sef_d{j}.glb"])
        geo = {k: v for k, v in geo.items() if "colonly" not in k}
        im = crop(render_view(geo, Ry(el, az), size=750, shadow=False, glass_alpha=.35))
        ax = fig.add_subplot(gs[1, j]); ax.imshow(np.clip(im, 0, 1)); ax.axis("off"); ax.set_title(t, fontsize=10)
    # row 2: vignettes — S grade+apron | E terrace with 2+4+2 skirt | N grade | assembled run
    def vignette(face, on_terrace, ax, title):
        A = {}; y0 = 3.7 if on_terrace else 0.0
        place(A, build(dict(face=face, seed=17)), (0, y0, 0), "SE")
        for side, dx in (("L", -6.0), ("R", 6.0)):
            place(A, FB.build(dict(width=4.0)), (dx, y0, 0), side)
        if on_terrace:
            PS.HT = 3.7
            for tag, w, x in (("C", 4.0, 0.0), ("L", 2.0, -3.0), ("R", 2.0, 3.0)):
                place(A, PS.build(dict(width=w, seed=7 if w > 3 else 12)), (x, 0, 2.0), f"SK{tag}")
            for dx in (-4.0, 0.0, 4.0):
                place(A, TF.build(dict(piece="deck")), (dx, 3.7, -5.0), f"D{dx}")
            place(A, TF.build(dict(piece="edge")), (0, 3.7, 1.5), "EDGE")
            PS.HT = 4.0
        else:
            for dx in (-4.0, 0.0, 4.0):
                place(A, TF.build(dict(piece="apron")), (dx, 0, 1.55), f"AP{dx}")
        Pt = Part()
        for n, (mk, m) in A.items():
            if "uv" not in m.metadata: m.metadata["uv"] = np.zeros((len(m.vertices), 2))
            Pt.add(n, mk, m)
        _, g2 = export_final(Pt.P, [f"/tmp/sefv_{face}.glb"])
        im = crop(render_view(g2, Ry(12, 28), size=900, shadow=False, glass_alpha=.35))
        ax.imshow(np.clip(im, 0, 1)); ax.axis("off"); ax.set_title(title, fontsize=10)
    vignette("S", False, fig.add_subplot(gs[2, 0]), "S at grade + apron + façade flanks")
    vignette("E", True, fig.add_subplot(gs[2, 1]), f"E terrace + skirt 2+4+2 (seams ±3 m) | {'PASS' if SK['pass_'] else 'FAIL'}")
    vignette("N", False, fig.add_subplot(gs[2, 2]), "N at grade + apron + façade flanks")
    # wide run: facade + entrance + facade
    A = {}
    place(A, build(dict(face="S", seed=17)), (0, 0, 0), "SE")
    for dx in (-10.0, -6.0, 6.0, 10.0):
        place(A, FB.build(dict(width=4.0)), (dx, 0, 0), f"F{dx}")
    for dx in (-4.0, 0.0, 4.0):
        place(A, TF.build(dict(piece="apron")), (dx, 0, 1.55), f"AP{dx}")
    Pt = Part()
    for n, (mk, m) in A.items():
        if "uv" not in m.metadata: m.metadata["uv"] = np.zeros((len(m.vertices), 2))
        Pt.add(n, mk, m)
    _, g2 = export_final(Pt.P, ["/tmp/sef_run.glb"])
    im = crop(render_view(g2, Ry(10, 25), size=1100, shadow=False, glass_alpha=.35))
    ax = fig.add_subplot(gs[2, 3]); ax.imshow(np.clip(im, 0, 1)); ax.axis("off")
    ax.set_title("S run: 4 façade bays + Rally Mark secondary", fontsize=10)
    fig.suptitle("Rook | #78 tt_secondary_entrance_{s,n,e} (V5 Rally Mark, densified) | FINAL", fontsize=16)
    plt.tight_layout(rect=(0, 0, 1, .96)); sp = os.path.join(rdir, "secondary_entrance_final_sheet.png")
    fig.savefig(sp, dpi=72, facecolor="#F4F2EC"); print("SHEET", sp)
