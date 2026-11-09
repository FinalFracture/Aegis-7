"""Rook: S/N/E secondary entrances (candidates). Spec Rev 2.6/2.7: S/N at grade on 1:12 aprons,
E on East Plaza terrace (+4.0). Lift-lobby gap ~10 m; module is 8.0 m (2 × 4 m façade columns)
with 1 m façade fillers each side to fill the gap. Reuses #74 Court Wayfinding + #75 Branch Glass
language. 5 themes. Each: F1 height 6.1 m, alpha-scissor TT_GlassScissor (MASK cutoff 0.5, factor alpha 1 via finish_scissor), pivot bottom centre, +Z out, colliders,
door-clearance walk. Run: python3 secondary_entrance.py"""
from modlib import *
from restroom_extras import crest
import facade_bay_final as FB
import entrance_bay_final as EB
from structure.struct_lib import SCR, finish_scissor
H, W0 = 6.1, 8.0
THEMES = [
    ("court", "Court Wayfinding Secondary", "Scaled V3 Court Wayfinding: deep soffit canopy, S/N/E blade, planted kerb, ball bollards"),
    ("branch", "Branch Portal", "Branch Fin trunks frame the doors, leaf-capital lintel, deep reveals, fork leaves"),
    ("river", "River Threshold", "River-slate mat, pebble nosing, amber river LEDs, cable-tied canopy"),
    ("green", "Green Spine", "Vine-wrapped reveals, moss sill, dense hedge edge, leaf soffit discs"),
    ("rally", "Rally Mark", "Racket-arch canopy, ball-cluster finials, court-line scoreboard blade, net kick"),
]
def glyph_boxes(face, y0, y1, z0, z1, sx):
    """Simple face letter as box glyphs. z0..z1 = plate thickness on the blade face."""
    o = sx * .055; d = (min(o + sx*.01, o - sx*.004), max(o + sx*.01, o - sx*.004))
    midy = (y0 + y1)/2; zh0, zh1 = z0, z1
    # letters drawn in Y spanning the blade; Z is only the plate thickness
    if face == "E":
        return [box(*d, y0 + .12, y1 - .12, zh0, zh1),
                box(*d, y1 - .2, y1 - .12, zh0, zh1),
                box(*d, midy - .05, midy + .05, zh0, zh1),
                box(*d, y0 + .12, y0 + .2, zh0, zh1)]
    if face == "N":
        return [box(*d, y0 + .12, y1 - .12, zh0, zh1),
                box(*d, y0 + .12, midy + .08, zh0, zh1),
                box(*d, midy - .08, y1 - .12, zh0, zh1)]
    return [box(*d, y1 - .2, y1 - .12, zh0, zh1),
            box(*d, midy - .05, midy + .05, zh0, zh1),
            box(*d, y0 + .12, y0 + .2, zh0, zh1),
            box(*d, y0 + .12, midy, zh0, zh1),
            box(*d, midy, y1 - .12, zh0, zh1)]
def doors(p, cols, TD=2.6):
    for i, (a0, b0) in enumerate(cols):
        a, b = a0 + .003, b0 - .003; m = (a + b)/2
        S = [box(a + .004, a + .07, .06, TD - .08, -.028, .028), box(b - .07, b - .004, .06, TD - .08, -.028, .028),
             box(m - .035, m + .035, .06, TD - .08, -.028, .028)]
        S += [box(a + .07 - E, b - .07 + E, u, v, -.028, .028) for (u, v) in ((.06, .18), (TD - .2, TD - .08))]
        p.add("Door_Stiles", ALY, *S)
        for k, (u, v) in enumerate(((a + .07, m - .035), (m + .035, b - .07))):
            p.add(f"Door_Scissor_{i}{k}", SCR, pane(u + .002, v - .002, .18 - E, TD - .2 + E, 0, t=.016))
            p.add("Push_Bars", ALY, tube((u + .12, 1.05, .07), (v - .12, 1.05, .07), .02, 8),
                  tube((u + .12, 1.05, .03 - E), (u + .12, 1.05, .07), .012, 6),
                  tube((v - .12, 1.05, .03 - E), (v - .12, 1.05, .07), .012, 6))
        for r, (y0, y1) in enumerate(((TD + .075, 4.35 - .075), (4.35 + .075, H - .15))):
            p.add(f"Upper_Scissor_{i}{r}", SCR, pane(a0 + .002, b0 - .002, y0 - E, y1 + E, 0))
def canopy_base(p, X0, X1, zt=2.2, y0=3.0, y1=3.16, deep=True):
    h = (X1 - X0)/2 + .001
    cx0, cx1 = X0 + .02, X1 - .02
    p.add("Canopy", SL, box(cx0, cx1, y0, y1, .061, zt),
          box(X0 + .05, X0 + .12, y0 - .34, y1 + E, .061 - E, .55),
          box(X1 - .12, X1 - .05, y0 - .34, y1 + E, .061 - E, .55))
    p.add("Canopy_Soffit", ALY, box(X0 + .123, X1 - .123, y0 - .12, y0 + E, .25, zt - .02),
          box(X0 + .123, X1 - .123, y0 - .06, y0 + E, .55, .25 + E))
    zs = (.7, 1.2, 1.7) if zt > 2 else (.7, 1.3)
    p.add("Soffit_Downlights", CY, *[box(cx0 + .25, cx1 - .25, y0 - .128, y0 - .12 + E, z, z + .04) for z in zs])
    p.add("Fascia_Slate", SL, box(cx0, cx1, y0 - .26, y1 + .06, zt - E, zt + .1))
    p.add("Fascia_Gunmetal", G, box(cx0, cx1, y0 - .16, y1 + .02, zt + .1 - E, zt + .18),
          box(cx0, cx1, y1 + .06 - E, y1 + .12, zt - .25, zt + .1 - .003))
    p.add("Court_Line_LED", AM, box(cx0, cx1, y0 - .26 - E, y0 - .23, zt + .1 - E, zt + .11),
          box(cx0, cx1, y0 - .06, y0 - .03, zt + .18 - E, zt + .19),
          box(cx0, cx1, y1 - E, y1 + .006, .25, .29))
    for x in (-h*.7, h*.7):
        p.add("Tie_Rods", ST, tube((x, 5.4, .06 - E), (x, y1 - E, zt - .35), .028, 6))
    return y1, zt
def blade(p, face, y1, zt):
    by0, by1, bz0, bz1 = y1 + .12 - E, y1 + .95, zt - .5, zt - .05
    p.add("Blade_Core", SL, box(-.05, .05, by0 + .046, by1 + .004, bz0 + .02, bz1 - .02))
    p.add("Blade_Frame", G, box(-.065, .065, by1 - E, by1 + .05, bz0 - .015, bz1 + .015),
          box(-.065, .065, by0, by0 + .05, bz0 - .015, bz1 + .015),
          box(-.065, .065, by0 + .03, by1 + .02, bz1 - .012, bz1 + .002),
          box(-.065, .065, by0 + .03, by1 + .02, bz0 - .002, bz0 + .012))
    G2 = []
    for sx, zplate in ((-1, (bz0 - .032, bz0 - .018)), (1, (bz1 + .018, bz1 + .032))):
        G2 += glyph_boxes(face, by0 + .12, by1 - .12, zplate[0], zplate[1], sx)
    p.add("Wayfinding_Glyphs", CY, *G2)
    p.add("Blade_Core", SL, box(-.04, .04, by0 + .55, by0 + .58, bz0 + .06, bz1 - .06))
    p.add("Blade_Ball_Finial", BA, node((0, by1 + .05 + .08 - E, (bz0 + bz1)/2 - .1), .08, 1))
    p.add("Blade_Leaf_Crest", LF, crest((0, by1 + .05 - E, (bz0 + bz1)/2 + .1)))
def planted_edge(p, X0, X1, rng, z_mat=1.25, dense=False):
    p.add("Threshold_Mat", SSL, box(X0 + .02, X1 - .02, 0, .012, .122, z_mat))
    p.add("Terrace_Kerb", SL, box(X0 + .02, X1 - .02, 0, .08, z_mat + .002, z_mat + .32))
    step = .28 if dense else .35
    boll = (X0 + 1.2, X1 - 1.2)
    xs = [x for x in np.arange(X0 + .3, X1 - .25, step) if all(abs(x - b) > .32 for b in boll)]
    p.add("Hedge_Edge", LF, *[clump((x, .08 + .16 - E*3, z_mat + .16), .15 if dense else .13, i) for i, x in enumerate(xs)])
    if dense:
        L2 = [clump((x + .12, .09 - E*3, z_mat + .38), .08, 50 + i) for i, x in enumerate(xs[:-1])]
        if L2: p.add("Hedge_Edge_Light", LF2, *L2)
    for x in boll:
        p.add("Ball_Bollards", G, tube((x, .08 - E, z_mat + .16), (x, .85, z_mat + .16), .1, 10))
        p.add("Bollard_Balls", BA, node((x, .85 + .11 - E, z_mat + .16), .11, 1))
def frame_base(p, X0, X1, cols):
    h = (X1 - X0)/2 + .001
    F = [box(X0, X1, 0, .05, -.65, .12), box(X0, X1, H - .15, H, -.65, .08),
         box((X0 + .06) - .05/2, (X0 + .06) + .05/2, .05 - E, H - .15 + E, .03 - .6, .03),
         box(X1 - .045, X1 - .01, .05 - E, H - .15 + E, -.04, .04)]
    # mid mullions between door pairs + end
    for x in [c[1] for c in cols[:-1]] + [c[0] for c in cols[1:]]:
        pass
    mids = []
    for i in range(len(cols) - 1):
        mids.append((cols[i][1] + cols[i+1][0]) / 2)
    for mx in mids:
        F.append(box(mx - .04, mx + .04, .05 - E, H - .15 + E, -.05, .05))
    for t in (2.6, 4.35):
        F.append(box(X0 + .06 + .025 - E, X1 - .045 + E, t - .075, t + .075, -.06, .06))
    # deep reveals around each door cell (layered)
    R = []
    for a, b in cols:
        R += [box(a + .004, a + .055, .12 + .002, 2.6 - .2, .03 + .002, .14),
              box(b - .055, b - .004, .12 + .002, 2.6 - .2, .03 + .002, .14),
              box(a + .055 - E, b - .055 + E, .12 + .002, .18, .03 + .002, .14),
              box(a + .055 - E, b - .055 + E, 2.6 - .2, 2.6 - .14, .03 + .002, .12)]
    F += R
    F += [box(X0 + .003, X1 - .003, .05 + .002, .32, .14, .28), box(X0, X1, .32 - E, .5, -.65, .16)]
    p.add("Frame", G, *F)
def build(q):
    th = q["theme"]; face = q.get("face", "S"); w = q.get("width", W0)
    h = w/2; X0, X1 = -h + .001, h - .001; p = Part(); rng = np.random.default_rng(q.get("seed", 11))
    # two double-door pairs in an 8 m bay (or one pair in a 4 m)
    if w > 6:
        cols = [(-h + .15, -1.05), (-.95, .95), (1.05, h - .15)]
        # actually 2 pairs: left and right of centre mullion
        cols = [(-h + .2, -.15), (.15, h - .2)]
    else:
        cols = [(-h + .15, h - .15)]
    frame_base(p, X0, X1, cols)
    doors(p, cols)
    # plinth ledge matching facade bay language (shallow at secondary)
    p.add("Plinth_Court_Line", AM, box(X0 + .08, -2.4, .18, .22, .28 - E, .287), box(-2.3, 2.3, .18, .22, .28 - E, .287), box(2.4, X1 - .08, .18, .22, .28 - E, .287))
    if th == "court":
        y1, zt = canopy_base(p, X0, X1, zt=2.2)
        blade(p, face, y1, zt)
        p.add("Fascia_Leaf_Crests", LF, *[crest((x, y1 + .12 - E, zt - .08)) for x in np.arange(X0 + .5, X1 - .4, 1.0) if abs(x) > .4])
        planted_edge(p, X0, X1, rng, z_mat=1.2)
    elif th == "branch":
        y1, zt = canopy_base(p, X0, X1, zt=2.0)
        # Branch Fin trunks flanking the centre, standing proud
        T, Lc = [], []
        for x0 in (-2.2, 2.2):
            p.add("Trunk_Pedestal", SL, box(x0 - .18, x0 + .18, .012 + .002, .4, .28 + .002, .72))
            zt_ = .58
            T += [node((x0, .4 + .09 - E, zt_), .09, 0), tube((x0, .5, zt_), (x0, 2.72, zt_), .065, 8)]
            for y in (1.2, 2.1):
                n = (x0, y, zt_); T += [node(n, .09, 0)]
                for (dx, dy) in ((.45, .3), (.3, -.25)):
                    e = (x0 + np.sign(x0)*dx, y + dy, .18); m = (x0 + np.sign(x0)*dx*.4, y + dy*.5, .4)
                    T += [tube(n, m, .035, 6), node(m, .03, 0), tube(m, e, .028, 6)]
                Lc.append(clump((x0 + np.sign(x0)*.18, y + .12, .78), .09, int(abs(y*10 + x0*3))))
            T += [node((x0, 2.72, zt_), .08, 0)]
            # stop trunk below soffit (soffit bottom ~2.88)
            for a in (0.5, 2.3, -1.5): Lc.append(xf(crest((0, 0, 0)), R=trimesh.transformations.rotation_matrix(a, [0, 1, 0]), t=(x0 + np.sign(x0)*.1, 2.65, zt_ + .14)))
        p.add("Branch_Trunk", G, *T); p.add("Fork_Leaves", LF, *Lc)
        blade(p, face, y1, zt)
        planted_edge(p, X0, X1, rng, z_mat=1.15)
    elif th == "river":
        y1, zt = canopy_base(p, X0, X1, zt=2.1)
        p.add("River_Mat", SL, box(X0 + .02, X1 - .02, 0, .018, .122, 1.35))
        # amber river LED ribbons
        for z in (.4, .75, 1.1):
            p.add("River_LED", AM, box(X0 + .15, X1 - .15, .018 - E, .024, z, z + .025))
        peb = []
        for i in range(16):
            x = rng.uniform(X0 + .4, X1 - .4); z = rng.uniform(.25, 1.25); r = rng.uniform(.035, .065)
            if any(abs(z - zz) < .05 for zz in (.4, .75, 1.1)): continue
            if z < .32: continue
            peb.append(node((x, .018 + r*.55 - E, z), r, 0))
        if peb: p.add("River_Pebbles", SSL, *peb)
        p.add("Pebble_Nosing", SL, box(X0 + .02, X1 - .02, 0, .06, 1.352, 1.55))
        for x in (X0 + 1.4, X1 - 1.4):
            p.add("Ball_Bollards", G, tube((x, .06 - E, 1.42), (x, .8, 1.42), .09, 8))
            p.add("Bollard_Balls", BA, node((x, .8 + .1 - E, 1.42), .1, 1))
        blade(p, face, y1, zt)
    elif th == "green":
        y1, zt = canopy_base(p, X0, X1, zt=2.05)
        # vine wraps on mid/end mullions
        V = []
        for x in (-h + .1, h - .1):  # end fins only (mid mullion stays clean)
            for y in np.linspace(.8, 5.3, 7):
                if 2.6 < y < 3.5: continue
                V.append(clump((x + rng.uniform(-.02, .02), y, .14 + rng.uniform(0, .03)), .048, int(abs(y*10) + int(abs(x*5)))))
        p.add("Vine_Wrap", LF, *V)
        p.add("Moss_Sill", LF2, *[clump((x, .5 + .04, .2), .06, i) for i, x in enumerate(np.arange(X0 + .4, X1 - .3, .35))])
        # leaf discs under soffit
        p.add("Leaf_Soffit", LF, *[xf(crest((0, 0, 0)), R=trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]), t=(x, 3.0 - .14, z))
                                   for x in np.arange(X0 + .6, X1 - .5, 1.2) for z in (1.0, 1.6)])
        planted_edge(p, X0, X1, rng, z_mat=1.18, dense=True)
        blade(p, face, y1, zt)
    else:  # rally
        y1, zt = canopy_base(p, X0, X1, zt=2.15)
        # racket-arch tubes over the canopy fascia
        arch = []
        for sx in (-1, 1):
            for t in np.linspace(0, np.pi, 10):
                pass
            pts = [(sx * 1.6 * np.cos(t), y1 + .12 + 0.55 * np.sin(t), zt + .05) for t in np.linspace(0, np.pi, 11)]
            arch += [tube(a, b, .03, 6) for a, b in zip(pts[:-1], pts[1:])]
            # racket head oval
            oval = [(sx * (1.15 + .35*np.cos(t)), y1 + .45 + .28*np.sin(t), zt + .08) for t in np.linspace(0, 2*np.pi, 13)]
            arch += [tube(a, b, .022, 5) for a, b in zip(oval[:-1], oval[1:])]
        p.add("Racket_Arch", ALY, *arch)
        p.add("Ball_Cluster", BA, *[node((x, y1 + .12 + .08 - E, zt - .05), .07, 1) for x in (-2.5, -1.2, 1.2, 2.5)])
        # scoreboard blade (wider)
        by0, by1, bz0, bz1 = y1 + .12 - E, y1 + 1.05, zt - .55, zt - .02
        p.add("Blade_Core", SL, box(-.7, .7, by0 + .04, by1, bz0, bz1),
              box(-.72, .72, by1 - E, by1 + .04, bz0 - .015, bz1 + .015),
              box(-.72, .72, by0, by0 + .04, bz0 - .015, bz1 + .015),
              box(-.72, -.68, by0 + .02, by1 + .02, bz0 - .015, bz1 + .015),
              box(.68, .72, by0 + .02, by1 + .02, bz0 - .015, bz1 + .015))
        p.add("Score_Cells", CY, *[box(x, x + .25, by0 + .25, by1 - .2, bz1 + .002, bz1 + .012) for x in (-.55, -.2, .15, .4)])
        p.add("Blade_Core", SL, box(-.68, .68, by0 + .12, by0 + .16, bz1 + .002, bz1 + .008))
        # glyphs on the outer (+Z) face only
        G2 = glyph_boxes(face, by0 + .08, by1 - .1, bz1 + .012, bz1 + .03, 1)
        p.add("Wayfinding_Glyphs", CY, *G2)
        p.add("Net_Kick", WH, *[box(X0 + .1, X1 - .1, y - .008, y + .008, .287 + .002, .3) for y in (.12, .2, .28)])
        planted_edge(p, X0, X1, rng, z_mat=1.15)
    # colliders: wall plane + door clearance floor strip (for walk through doors) + canopy
    p.add("Wall-colonly", G, box(X0, X1, .5, H, -.08, .02))
    # door openings left clear: floor collider only outside door X ranges is wall; through doors a floor slab
    p.add("DoorClear-colonly", SL, box(X0, X1, 0, .02, -.3, 1.4))
    for a, b in cols:
        # cut? walk uses DoorClear floor; wall stops at .5 so headroom under transom — also add side jambs as solid
        p.add("Jamb-colonly", G, box(a - .02, a + .02, 0, H, -.08, .14), box(b - .02, b + .02, 0, H, -.08, .14))
    p.add("Canopy-colonly", SL, box(X0 + .05, X1 - .05, 3.0, 3.16, .06, 2.0))
    return p
def V():
    return [dict(theme=t, label=name, face="S", seed=10 + i) for i, (t, name, _) in enumerate(THEMES)]
def door_clear(prm):
    """Doors are modelled closed (same as #74). Check clear opening >= 0.9 m W x 2.1 m H per leaf pair,
    and walk the threshold mat outside the glass line."""
    p = build(prm); w = prm.get("width", W0); h = w/2
    cols = [(-h + .2, -.15), (.15, h - .2)] if w > 6 else [(-h + .15, h - .15)]
    clears = []
    for a, b in cols:
        # clear between stiles (inset .07 each side + centre stile .07): two leaves
        leaf_w = ((b - a) - .14 - .07)/2
        clears.append(dict(leaf_w=round(leaf_w, 3), height=2.6 - .18 - .08, ok=leaf_w >= .9 and (2.6 - .26) >= 2.1))
    # threshold walk on DoorClear-colonly (outside only, z +.3 .. +1.2)
    cx = sum(cols[0])/2
    r = walk_check(p, [(cx, 1.15), (cx, .45)], y0=0.0, step=.05, head=2.0)
    # headroom outside uses canopy at 3.0 → ~3.0 m clear; ignore closed-door visual for approach
    return dict(opens=clears, all_ok=all(c["ok"] for c in clears), approach=r, pass_=all(c["ok"] for c in clears) and r["nofloor"] == 0)
def seam_with_facade(prm):
    """Place secondary between two facade bays; check seams at ±4 m (half of 8 m)."""
    A = {}
    for n, (mk, m) in build(prm).P.items():
        if "colonly" in n: continue
        m2 = m.copy(); m2.metadata["uv"] = m.metadata.get("uv", np.zeros((len(m.vertices), 2))); A[f"S_{n}"] = (mk, m2)
    for side, dx in (("L", -6.0), ("R", 6.0)):  # 8/2 + 4/2 = 6
        for n, (mk, m) in FB.build(dict(width=4.0)).P.items():
            if "colonly" in n: continue
            m2 = m.copy(); m2.apply_translation((dx, 0, 0)); m2.metadata["uv"] = m.metadata.get("uv", np.zeros((len(m.vertices), 2))); A[f"{side}_{n}"] = (mk, m2)
    chk = cc.check(A, n_samp=250)
    # only care about cross-module overlaps near the seam
    bad = [o for o in chk["overlap"] if not o[3] and o[0].split("_")[0] != o[1].split("_")[0] and o[2] > .0101]
    cop = [c for c in chk["coplanar"] if c[0].split("_")[0] != c[1].split("_")[0]]
    return not bad and not cop, bad[:3], cop[:3]
if __name__ == "__main__":
    import terrace_final as TF, plinth_skirt_final as PS
    from terrace_final import place
    REP = run("secondary_entrance", build, V(), title="secondary entrance", sheet="secondary_entrance_run_sheet.png",
              names=[f"v{i+1}_{THEMES[i][0]}" for i in range(5)], post=finish_scissor)
    WK = {i: door_clear(V()[i]) for i in range(5)}
    SE = {i: seam_with_facade(V()[i])[0] for i in range(5)}
    print("CLEAR", {i: dict(pass_=WK[i]["pass_"], opens=WK[i]["opens"], approach_pass=WK[i]["approach"]["pass"]) for i in range(5)})
    print("SEAM_FACADE", SE)
    rdir = os.path.join(RENDER_OUT, "secondary_entrance")
    json.dump(dict(rep=REP, clear=WK, seam=SE, themes=THEMES), open(os.path.join(rdir, "report.json"), "w"), indent=1, default=str)
    Ry = lambda el, az: (lambda a, b: np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]) @ np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]))(np.radians(az), np.radians(el))
    fig = plt.figure(figsize=(32, 28), facecolor="#F4F2EC"); gs = fig.add_gridspec(3, 5)
    for i in range(5):
        prm = V()[i]
        for j, (el, az) in enumerate([(10, 32), (28, -55)]):
            p = recenter(build(prm)); _, geo = export_final(p.P, [f"/tmp/se_{i}_{j}.glb"]); geo = {k: v for k, v in geo.items() if "colonly" not in k}
            im = crop(render_view(geo, Ry(el, az), size=700, shadow=False, glass_alpha=.35))
            ax = fig.add_subplot(gs[j, i]); ax.imshow(np.clip(im, 0, 1)); ax.axis("off")
            r = REP[i]; w = WK[i]
            ax.set_title((f"v{i+1} {THEMES[i][1]}\n{THEMES[i][2][:58]}\n" if j == 0 else "") +
                         f"{'low 3/4' if j == 0 else 'high side (canopy depth)'} | {r['tris']} tris | {'PASS' if r['passed'] else 'FAIL'} | door clear {'PASS' if w['pass_'] else 'FAIL'} | façade seam {'PASS' if SE[i] else 'FAIL'}", fontsize=8)
        A = {}; on_terrace = (i % 2 == 1)  # alternate: odd on E terrace, even on S grade apron
        y0 = 3.7 if on_terrace else 0.0
        prm2=dict(prm); prm2["face"]="E" if on_terrace else "S"; place(A, build(prm2), (0, y0, 0), "SE")
        for side, dx in (("L", -6.0), ("R", 6.0)):
            place(A, FB.build(dict(width=4.0)), (dx, y0, 0), side)
        if on_terrace:
            PS.HT = 3.7
            for dx in (-4.0, 0.0, 4.0):
                place(A, TF.build(dict(piece="deck")), (dx, 3.7, -5.0), f"D{dx}")
                place(A, PS.build(dict(width=4.0, seed=7)), (dx, 0, 2.0), f"SK{dx}")
            place(A, TF.build(dict(piece="edge")), (0, 3.7, 1.5), "EDGE")
            PS.HT = 4.0
        else:
            for dx in (-4.0, 0.0, 4.0):
                place(A, TF.build(dict(piece="apron")), (dx, 0, 1.55), f"AP{dx}")
        Pt = Part()
        for n, (mk, m) in A.items():
            if "uv" not in m.metadata: m.metadata["uv"] = np.zeros((len(m.vertices), 2))
            Pt.add(n, mk, m)
        _, g2 = export_final(Pt.P, [f"/tmp/sev_{i}.glb"]); im = crop(render_view(g2, Ry(12, 28), size=900, shadow=False, glass_alpha=.35))
        ax = fig.add_subplot(gs[2, i]); ax.imshow(np.clip(im, 0, 1)); ax.axis("off")
        ax.set_title(f"vignette: {'E terrace + skirt/deck/edge' if on_terrace else 'S grade + apron'} + façade flanks\nglyph face {'E' if on_terrace else 'S'} (mirror X for N)", fontsize=9)
    fig.suptitle("Rook | Tennis Tower S/N/E secondary entrances V1-V5 (8 m module in ~10 m lift gap) | candidates (not promoted)", fontsize=16)
    plt.tight_layout(rect=(0, 0, 1, .97)); sp = os.path.join(rdir, "secondary_entrance_contact_sheet.png"); fig.savefig(sp, dpi=70, facecolor="#F4F2EC"); plt.close(fig); print("SHEET", sp)
