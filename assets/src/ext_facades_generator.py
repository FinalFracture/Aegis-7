"""Rook (Oct 30, Jared 1:59 PM CT, NO vote / single finals): facade batch to Vance's spec, design/residential_exterior_asset_list_v1.md.
#6 ext_facade_panel_res (x60 MultiMesh, tileable: all geometry inside X +-1.497 / Y 0..4.397 -> 6 mm reveal, no overlap when tiled)
#7 ext_window_unit, #8 ext_l2_promenade_window, #9 ext_roof_parapet_plantcap, #5 ext_door_canopy,
#10-14 ext_nbr_r6_residential / ext_nbr_clinic_market / ext_nbr_workshop_row / ext_nbr_kiosk_row / ext_nbr_tram_depot (facade-only).
Palette: Aegis-7 gunmetal/carbon-slate/titanium/amber + list spec pearl alabaster #D8DEE4 cladding, Civic cyan #38B8C8 accent (clinic, depot).
Run: python3 ext_facades_generator.py <key|all|sheet>"""
import os, sys, json, shutil, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import ext_street_furniture_generator as sf, ext_clip_check as cc
from ext_street_furniture_generator import G, S, T, A, GL, E, box, Pod, export_final, set_glass_blend, views, render_view, crop, recenter, FMAT, _PBR, plt
FMAT["a7_pearl"] = _PBR(name="A7_PearlAlabaster", baseColorFactor=(0xD8/255, 0xDE/255, 0xE4/255, 1), metallicFactor=0.15, roughnessFactor=0.45)
FMAT["a7_cyan"] = _PBR(name="A7_CivicCyan", baseColorFactor=(0x38/255, 0xB8/255, 0xC8/255, 1), metallicFactor=0.1, roughnessFactor=0.4)
P_, C_ = "a7_pearl", "a7_cyan"; ROOT = sf.ROOT

def panel():  # #6 3.0 x 0.2 x 4.4
    p = Pod("ext_facade_panel_res"); X = 1.485
    p.add("Backer", G, box(-1.497, 1.497, 0, 4.397, -.1, -.06))
    p.add("Cladding", P_, box(-X, X, .012, 3.25, -.06 - E, .1), box(-X, X, 4.1, 4.385, -.06 - E, .1))
    p.add("Reveals", T, box(-1.491, 1.491, 3.246, 3.274, -.06 - E + .002, .07), box(-1.491, 1.491, 4.076, 4.104, -.06 - E + .002, .07))
    p.add("Spandrel", S, box(-X, X, 3.27, 4.08, -.06 - E, .085))
    p.add("Joint_Groove", T, box(-.006, .006, .012 + .3, 3.25 - .3, .1 - E, .106))
    return p
def window(name, W, H, D, mull, transom=None, rail=False):
    p = Pod(name); f = .06; zs = D / 2
    p.add("Sill", T, box(-W / 2, W / 2, 0, .05, -zs, zs))
    p.add("Frame", S, box(-W / 2 + .01, -W / 2 + .01 + f, .05 - E, H - .003, -zs + .01, zs - .02), box(W / 2 - .01 - f, W / 2 - .01, .05 - E, H - .003, -zs + .01, zs - .02),
          box(-W / 2 + .01 + f - E, W / 2 - .01 - f + E, H - .003 - f, H - .006, -zs + .01, zs - .02), box(-W / 2 + .01 + f - E, W / 2 - .01 - f + E, .05 - E + .002, .05 + f, -zs + .01, zs - .02))
    xi0, xi1 = -W / 2 + .01 + f, W / 2 - .01 - f; yi0, yi1 = .05 + f, H - .003 - f
    xs = np.linspace(xi0, xi1, mull + 2)[1:-1]; mw = .025
    p.add("Mullions", G, *[box(x - mw, x + mw, yi0 - E, yi1 + E, -zs + .015, zs - .03) for x in xs])
    ys = [yi0, yi1] if transom is None else [yi0, transom - mw, transom + mw, yi1]
    if transom is not None: p.add("Transom", G, *[box(a + (mw if i else 0) - E, b - (mw if i < len(xs) else 0) + E, transom - mw, transom + mw, -zs + .016, zs - .031) for i, (a, b) in enumerate(zip([xi0] + list(xs), list(xs) + [xi1]))])
    edges = [xi0] + list(xs) + [xi1]; panes = []
    for i in range(len(edges) - 1):
        a = edges[i] + (mw if i else 0) - E; b = edges[i + 1] - (mw if i < len(xs) else 0) + E
        for k in range(0, len(ys), 2): panes.append(box(a, b, ys[k] - E, ys[k + 1] + E, -.003, .003))
    p.add("Glass", GL, *panes)
    if rail: p.add("Guard_Rail", T, box(xi0 - E, xi1 + E, .95, .99, zs - .02 - E + .001, zs + .02), *[box(x - .015, x + .015, .05 + f, .95 + E, zs - .02 - E + .002, zs + .005) for x in (xi0 + .3, 0, xi1 - .3)])
    return p
def parapet():  # #9 28 x 18 ring, ~1.0
    p = Pod("ext_roof_parapet_plantcap"); X, Z, t, h = 14, 9, .25, .9
    p.add("Parapet_Long", S, box(-X, X, 0, h, Z - t, Z), box(-X, X, 0, h, -Z, -Z + t))
    p.add("Parapet_Short", S, box(X - t, X, .002, h - .002, -Z + t - E, Z - t + E), box(-X, -X + t, .002, h - .002, -Z + t - E, Z - t + E))
    co = .04
    p.add("Coping_Long", P_, box(-X - co, X + co, h - E, h + .06, Z - t - co, Z + co), box(-X - co, X + co, h - E, h + .06, -Z - co, -Z + t + co))
    p.add("Coping_Short", P_, box(X - t - co, X + co, h - .002 - E, h + .058, -Z + t + co - E, Z - t - co + E), box(-X - co, -X + t + co, h - .002 - E, h + .058, -Z + t + co - E, Z - t - co + E))
    p.add("Hazard_Edge", A, box(-X + t + co + .01, X - t - co - .01, h + .06 - E, h + .066, Z - t - co + .004, Z - t - co + .05), box(-X + t + co + .01, X - t - co - .01, h + .06 - E, h + .066, -Z + t + co - .05, -Z + t + co - .004))
    hs = []
    for x in np.linspace(-11, 11, 6):
        for z in (Z - t - .45, -Z + t + .45): hs.append(box(x - .6, x + .6, .003, .7, z - .4, z + .4))
    for z in (-4, 4):
        for x in (X - t - .45, -X + t + .45): hs.append(box(x - .4, x + .4, .003, .7, z - .6, z + .6))
    p.add("Plantcap_Housings", S, *hs)
    p.add("Plantcap_Lids", G, *[box(m.bounds[0][0] + .03, m.bounds[1][0] - .03, .7 - E, .74, m.bounds[0][2] + .03, m.bounds[1][2] - .03) for m in hs])
    p.add("Plantcap_Vents", T, *[box(m.bounds[0][0] + .15, m.bounds[1][0] - .15, .74 - E, .76, (m.bounds[0][2] + m.bounds[1][2]) / 2 - .05, (m.bounds[0][2] + m.bounds[1][2]) / 2 + .05) for m in hs])
    return p
def canopy():  # #5 3.2 W x 1.2 D x 0.3 H, wall plate at the back (-Z)
    p = Pod("ext_door_canopy")
    p.add("Wall_Plate", S, box(-1.6, 1.6, 0, .3, -.6, -.56))
    p.add("Hood", P_, box(-1.55, 1.55, .18, .297, -.56 - E, .584))
    p.add("Fascia", G, box(-1.56, 1.56, .15, .3, .56, .6 + .003) if False else box(-1.553, 1.553, .15, .25, .584 - E, .6))
    p.add("Gussets", G, *[box(x - .02, x + .02, .03, .18 + E, -.56 - E, -.2) for x in (-1.3, 1.3)])
    p.add("Light_Strip", A, box(-1.3, 1.3, .17, .18 + E, .2, .3))
    return p
# ---------------- neighbour facades: wall + bay grid ----------------
def grid(p, W, H, floors, bays, pier=.5, ground=None, glass_rows=None, spand=P_, piermat=P_, mull=2):
    """Pier/spandrel/glass facade. floors = list of (y0, y1) storey bands; each band = spandrel (lower .9) + window (rest)."""
    D = .4; p.add("Wall", S, box(-W / 2 + .01, W / 2 - .01, 0, H - .3 + E, -D, 0))
    p.add("Cornice", G, box(-W / 2, W / 2, H - .3, H, -D - .02, .25))
    xs = np.linspace(-W / 2 + pier / 2, W / 2 - pier / 2, bays + 1)
    p.add("Piers", piermat, *[box(x - pier / 2, x + pier / 2, .002, H - .3 + E, -E, .2) for x in xs])
    sp, gl, mu = [], [], []
    for (y0, y1) in floors:
        for i in range(bays):
            a, b = xs[i] + pier / 2 - E, xs[i + 1] - pier / 2 + E
            sp.append(box(a, b, y0 + (.002 if y0 == 0 else 0), y0 + .9, -E, .12))
            ms = np.linspace(a, b, mull + 2)[1:-1]
            mu += [box(m - .03, m + .03, y0 + .9 - E, y1 - .25 + E, -E, .08) for m in ms]
            ed = [a] + list(ms) + [b]
            for k in range(len(ed) - 1): gl.append(box(ed[k] + (.03 if k else 0) - E, ed[k + 1] - (.03 if k < len(ms) else 0) + E, y0 + .9 - E, y1 - .25 + E, .03, .036))
            sp.append(box(a, b, y1 - .25, y1 - (0 if y1 < H - .3 else -E), -E, .1))
    p.add("Spandrels", spand, *sp); p.add("Mullions", T, *mu); p.add("Glass", GL, *gl)
    return xs
def r6():
    p = Pod("ext_nbr_r6_residential"); W, H = 30, 12
    xs = grid(p, W, H, [(0, 3.9), (3.9, 7.8), (7.8, 11.7)], 8, spand=S)
    bal = []; rail = []
    for y in (3.9, 7.8):
        for i in (1, 3, 4, 6):
            c = (xs[i] + xs[i + 1]) / 2; bal.append(box(c - 1.2, c + 1.2, y + .9 - .15, y + .9, .12 - E, 1.3))
            rail.append(box(c - 1.15, c + 1.15, y + .9 - E, y + 1.9, 1.24, 1.26))
    p.add("Balcony_Slabs", "a7_pearl", *bal); p.add("Balcony_Glass", GL, *rail)
    p.add("Balcony_Rails", T, *[box(m.bounds[0][0] - .02, m.bounds[1][0] + .02, m.bounds[1][1] - E, m.bounds[1][1] + .04, 1.23, 1.27) for m in rail])
    return p
def clinic():
    p = Pod("ext_nbr_clinic_market"); W, H = 30, 10
    xs = grid(p, W, H, [(4.6, 9.7)], 6, spand=P_, piermat=P_)
    # market hall ground floor: tall glazed bays, canopy, cyan civic band
    p.add("Hall_Frames", G, *[box(x - .25, x + .25, .002, 4.6 + E, -E, .3) for x in xs[1:-1]] if False else [box(-W / 2 + .01, W / 2 - .01, 4.0, 4.6 + E, -E, .3)])
    gl = []; mu = []
    for i in range(6):
        a, b = xs[i] + .25 - E, xs[i + 1] - .25 + E; mid = (a + b) / 2
        mu.append(box(mid - .04, mid + .04, .002, 4.0 + E, -E, .1))
        gl += [box(a, mid - .04 + E, .002, 4.0 + E, .04, .046), box(mid + .04 - E, b, .002, 4.0 + E, .04, .046)]
    p.add("Hall_Mullions", T, *mu); p.add("Hall_Glass", GL, *gl)
    p.add("Hall_Canopy", T, box(-W / 2 + .3, W / 2 - .3, 4.0 + .05, 4.2, .3 - E, 2.2))
    p.add("Civic_Band", C_, box(-W / 2 + .02, W / 2 - .02, 4.25, 4.45, .3 - E, .32))
    p.add("Clinic_Mark", C_, box(-.15, .15, 7.0, 8.4, .2 - E, .23), box(-.7, -.15 + E, 7.55, 7.85, .2 - E, .229), box(.15 - E, .7, 7.55, 7.85, .2 - E, .229))
    return p
def workshop():
    p = Pod("ext_nbr_workshop_row"); W, H = 14, 9
    xs = grid(p, W, H, [(5.0, 8.7)], 3, pier=.6, spand=S, piermat=P_, mull=3)
    sh, rib, haz, hood = [], [], [], []
    for i in range(3):
        a, b = xs[i] + .3 - E, xs[i + 1] - .3 + E
        sh.append(box(a, b, .002, 4.4, -E, .06))
        rib += [box(a + .02, b - .02, y, y + .04, .06 - E, .08) for y in np.arange(.3, 4.3, .25)]
        haz += [box(a + .02, a + .14, .3, 1.5, .06 - E, .07), box(b - .14, b - .02, .3, 1.5, .06 - E, .07)]
        hood.append(box(a, b, 4.4 - E, 5.0 + E, -E, .25))
    p.add("Roller_Shutters", T, *sh); p.add("Shutter_Ribs", G, *rib); p.add("Hazard_Jambs", A, *haz); p.add("Shutter_Boxes", S, *hood)
    return p
def kiosk():
    p = Pod("ext_nbr_kiosk_row"); W, H = 17, 4
    p.add("Wall", S, box(-W / 2 + .01, W / 2 - .01, 0, H - .3 + E, -.6, 0)); p.add("Roof_Fascia", G, box(-W / 2, W / 2, H - .3, H, -.62, .3))
    xs = np.linspace(-W / 2 + .2, W / 2 - .2, 5)
    p.add("Piers", P_, *[box(x - .2, x + .2, .002, H - .3 + E, -E, .25) for x in xs])
    cnt, top, gl, aw, st = [], [], [], [], []
    for i in range(4):
        a, b = xs[i] + .2 - E, xs[i + 1] - .2 + E
        cnt.append(box(a, b, .003, 1.0, -E, .45)); top.append(box(a - .0 + .02, b - .02, 1.0 - E, 1.05, -E + .001, .55))
        gl.append(box(a, b, 1.05 - E + .002, 2.6, .05, .056))
        aw.append(box(a + .05, b - .05, 2.65, 2.8, .25 - E, 1.4)); st.append(box(a + .1, b - .1, 2.6 - .1, 2.65 + E, .25 - E + .002, .3))
        st.append(box(a, b, 2.6 - E, 3.0, -E, .2))
    p.add("Counters", S, *cnt); p.add("Counter_Tops", T, *top); p.add("Kiosk_Glass", GL, *gl); p.add("Awnings", P_, *aw)
    p.add("Lintels", G, *st); p.add("Menu_Lights", A, *[box(m.bounds[0][0] + .3, m.bounds[1][0] - .3, 2.66 - E + .1, 2.72 + .1, .2 - E, .206) for m in aw]) if False else None
    p.add("Awning_Lights", A, *[box(m.bounds[0][0] + .3, m.bounds[1][0] - .3, 2.65 - .006, 2.65 + E, .6, .7) for m in aw])
    return p
def depot():
    p = Pod("ext_nbr_tram_depot"); W, H = 20, 7
    p.add("Wall", S, box(-W / 2 + .01, W / 2 - .01, 0, H - .3 + E, -.5, 0)); p.add("Cornice", G, box(-W / 2, W / 2, H - .3, H, -.52, .3))
    pc = [-9.6, -1.2, 1.2, 9.6]
    p.add("Piers", P_, *[box(x - .4, x + .4, .002, H - .3 + E, -E, .3) for x in pc])
    por, lin, gl, mu, cy = [], [], [], [], []
    for a, b in ((-8.8, -2.0), (2.0, 8.8)):
        por.append(box(a - E, b + E, .002, 4.6, -E, .02))  # dark portal (interior card)
        lin.append(box(a - E, b + E, 4.6, 5.2, -E, .25))
        ms = np.linspace(a, b, 5)
        mu += [box(m - .04, m + .04, 5.2 - E, H - .3 + E, -E, .1) for m in ms[1:-1]]
        ed = list(ms); ed[0] -= E; ed[-1] += E
        gl += [box(ed[k] + (.04 if k else 0) - E, ed[k + 1] - (.04 if k < 3 else 0) + E, 5.2 - E, H - .3 + E, .03, .036) for k in range(4)]
        cy.append(box(a + .2, b - .2, 4.8, 5.0, .25 - E, .27))
    p.add("Portals", G, *por); p.add("Lintels", P_, *lin); p.add("Clerestory_Mullions", T, *mu); p.add("Clerestory_Glass", GL, *gl); p.add("Civic_Livery", C_, *cy)
    p.add("Bay_Spandrels", P_, box(-2.0 + E * 0 - E, 2.0 + E, .002, H - .3 + E, -E, .15) if False else box(-1.2 + .4 - E, 1.2 - .4 + E, .002, H - .3 + E, -E, .15), box(-10 + .01, -9.6 - .4 + E, .002, H - .3 + E, -E, .15) if False else box(-8.8 - E, -9.2 + E, 4.6 - E + .002, 5.2, -E, .12))
    p.add("Rail_Inlays", T, *[box(c - .75 + d, c - .75 + d + .07, .0, .004, .02 - E, .4) for c in (-5.4, 5.4) for d in (0, 1.43)]) if False else None
    return p
PIECES = {"panel": ("ext_facade_panel_res", panel, 400, "#6 facade panel 3.0x0.2x4.4 (x60 MultiMesh)"), "window": ("ext_window_unit", lambda: window("ext_window_unit", 2.4, 1.5, .15, 1), 500, "#7 window unit 2.4x0.15x1.5"),
          "l2win": ("ext_l2_promenade_window", lambda: window("ext_l2_promenade_window", 2.4, 2.0, .2, 2, transom=1.45, rail=True), 600, "#8 L2 promenade window 2.4x2.0"),
          "parapet": ("ext_roof_parapet_plantcap", parapet, 3000, "#9 roof parapet + plant caps 28x18"), "canopy": ("ext_door_canopy", canopy, 600, "#5 door canopy 3.2x1.2x0.3"),
          "r6": ("ext_nbr_r6_residential", r6, 5000, "#10 nbr R-6 residential 30x12"), "clinic": ("ext_nbr_clinic_market", clinic, 5000, "#11 nbr clinic/market 30x10"),
          "workshop": ("ext_nbr_workshop_row", workshop, 4000, "#12 nbr workshop row 14x9"), "kiosk": ("ext_nbr_kiosk_row", kiosk, 3000, "#13 nbr kiosk row 17x4"), "depot": ("ext_nbr_tram_depot", depot, 3500, "#14 nbr tram depot edge 20x7")}
def build(key):
    name, fn, budget, title = PIECES[key]; p = recenter(fn()); chk = cc.check(p.P, n_samp=600)
    out = os.path.join(ROOT, "design/assets", name); os.makedirs(out, exist_ok=True); gp = os.path.join(out, f"{name}.glb")
    tris, geo = export_final(p.P, [gp]); set_glass_blend(gp)
    r = dict(name=name, title=title, tris=tris, budget=budget, size=chk["size"], pivot=chk["pivot"], clip_pass=chk["pass"], worst=chk["worst_overlap"],
             over=[o for o in chk["overlap"] if not o[3]][:12], coplanar=chk["coplanar"][:12], open=chk["open"])
    json.dump(r, open(os.path.join(out, f"{name}_report.json"), "w"), indent=1); print(json.dumps(r)); return r
def sheet():
    _, _, _, iso = views(); tiles = []
    FMAT[A] = _PBR(name="amber", baseColorFactor=(0, 0, 0, 1), metallicFactor=0, roughnessFactor=1, emissiveFactor=(1.0, .58, 0.0))
    for key, (name, fn, budget, title) in PIECES.items():
        r = json.load(open(os.path.join(ROOT, "design/assets", name, f"{name}_report.json"))); p = recenter(fn()); _, geo = export_final(p.P, ["/tmp/_fac.glb"])
        tiles.append((f"{title}\n{r['tris']} tris (<= {budget}) | clip {'PASS' if r['clip_pass'] else 'FAIL'} | godot/assets/models/{name}.glb", crop(render_view(geo, iso, size=560, shadow=True, glass_alpha=.35))))
    fig, axs = plt.subplots(2, 5, figsize=(28, 12), facecolor="#F4F2EC")
    for ax, (t, im) in zip(axs.flat, tiles): ax.imshow(im); ax.axis("off"); ax.set_title(t, fontsize=10, color="#333")
    fig.suptitle("Rook  residential exterior facade batch (#5-#14) - single finals, no vote (Jared waived 1:59 PM CT)  |  Aegis-7 palette + pearl/cyan per list, BLEND glass, iso", fontsize=14, color="#444")
    plt.tight_layout(rect=(0, 0, 1, .95)); sp = os.path.join(ROOT, "design/assets/ext_facade_batch_overview_sheet.png"); fig.savefig(sp, dpi=80, facecolor="#F4F2EC"); print("sheet", sp)
if __name__ == "__main__":
    for k in sys.argv[1:]:
        sheet() if k == "sheet" else [build(q) for q in (PIECES if k == "all" else [k])]
