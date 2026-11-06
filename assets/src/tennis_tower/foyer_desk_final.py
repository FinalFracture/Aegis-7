"""Rook: #79 W foyer ticketing kit FINAL (Jared pick V4 River Queue, densified).
Pieces: tt_foyer_desk (8 m + 1 m accessible bay), tt_foyer_kiosk, tt_foyer_stanchion, tt_foyer_backdrop.
Density: ticket slots + RFID + printers (baked), layered river-slate fascia + pebble relief, sculpted
counter edge, cable rings, seated moss; kiosk slate base + pebble plinth + deep bezel; sculpted cable-ring
stanchions; backdrop river-wave relief + sculpted TICKETS glyphs. No wood, no planter boxes.
Run: python3 foyer_desk_final.py"""
from modlib import *
from restroom_extras import crest
import foyer_desk as FD
import entrance_bay_final as EB
from foyer_desk import CH, CHA, TOPT, place
CH, CHA, TOPT = FD.CH, FD.CHA, FD.TOPT
PIECES = ("desk", "kiosk", "stanchion", "backdrop")
def stroke(x0, x1, y0, y1, z0, z1, bev=.005):
    return [box(x0, x1, y0, y1, z0, z1), box(x0 + bev, x1 - bev, y0 + bev, y1 - bev, z1 - E, z1 + .006)]
def glyph_word(word, x0, y0, y1, z_face, cell=.22, gap=.06, thick=.022):
    """Sculpted bevelled block capitals for TICKETS / etc. Returns meshes."""
    # simple stroke fonts for T,I,C,K,E,S
    def letter(ch, cx):
        w, t = cell * .85, cell * .18; zh0, zh1 = z_face, z_face + thick; M = []
        midy = (y0 + y1) / 2
        if ch == "T":
            M += stroke(cx - w/2, cx + w/2, y1 - t, y1, zh0, zh1)
            M += stroke(cx - t/2, cx + t/2, y0, y1 - t + E, zh0, zh1)
        elif ch == "I":
            M += stroke(cx - t/2, cx + t/2, y0, y1, zh0, zh1)
            M += stroke(cx - w*.35, cx + w*.35, y1 - t*.6, y1, zh0, zh1)
            M += stroke(cx - w*.35, cx + w*.35, y0, y0 + t*.6, zh0, zh1)
        elif ch == "C":
            M += stroke(cx - w/2, cx - w/2 + t, y0 + t*.5, y1 - t*.5, zh0, zh1)
            M += stroke(cx - w/2, cx + w*.35, y1 - t, y1, zh0, zh1)
            M += stroke(cx - w/2, cx + w*.35, y0, y0 + t, zh0, zh1)
        elif ch == "K":
            M += stroke(cx - w/2, cx - w/2 + t, y0, y1, zh0, zh1)
            # upper / lower diagonals as stepped boxes
            for i in range(4):
                yy0 = midy + (y1 - midy) * i / 4; yy1 = midy + (y1 - midy) * (i + 1) / 4
                xx0 = cx - w/2 + t + (w - t) * i / 4; xx1 = xx0 + (w - t) / 4 + t * .5
                M += stroke(xx0, xx1, yy0, yy1, zh0, zh1, bev=.003)
                yy0 = midy - (midy - y0) * (i + 1) / 4; yy1 = midy - (midy - y0) * i / 4
                M += stroke(xx0, xx1, yy0, yy1, zh0, zh1, bev=.003)
        elif ch == "E":
            M += stroke(cx - w/2, cx - w/2 + t, y0, y1, zh0, zh1)
            M += stroke(cx - w/2 + t - E, cx + w/2, y1 - t, y1, zh0, zh1)
            M += stroke(cx - w/2 + t - E, cx + w*.2, midy - t/2, midy + t/2, zh0, zh1)
            M += stroke(cx - w/2 + t - E, cx + w/2, y0, y0 + t, zh0, zh1)
        elif ch == "S":
            M += stroke(cx - w/2, cx + w/2, y1 - t, y1, zh0, zh1)
            M += stroke(cx + w/2 - t, cx + w/2, midy, y1 - t + E, zh0, zh1)
            M += stroke(cx - w/2, cx + w/2, midy - t/2, midy + t/2, zh0, zh1)
            M += stroke(cx - w/2, cx - w/2 + t, y0 + t - E, midy, zh0, zh1)
            M += stroke(cx - w/2, cx + w/2, y0, y0 + t, zh0, zh1)
        elif ch == " ":
            pass
        else:  # fallback bar
            M += stroke(cx - w/2, cx + w/2, midy - t/2, midy + t/2, zh0, zh1)
        return M
    out = []; x = x0
    for ch in word:
        out += letter(ch, x + cell / 2); x += cell + gap
    return out
def cable_ring(cx, cy, cz, r=.07, tube_r=.01, seg=10):
    pts = [(cx + r * np.cos(t), cy + r * np.sin(t), cz) for t in np.linspace(0, 2 * np.pi, seg)]
    return [tube(a, b, tube_r, 4) for a, b in zip(pts[:-1], pts[1:])]
def wave_strip(x0, x1, y, z_face, amp=.035, n=12, thick=.025, depth=.035):
    """Horizontal river-wave relief proud of z_face (never into the wall core)."""
    xs = np.linspace(x0, x1, n); M = []
    for a, b in zip(xs[:-1], xs[1:]):
        da = amp * (1 + np.sin((a - x0) / max(1e-6, x1 - x0) * 2 * np.pi * 2)) * .5
        db = amp * (1 + np.sin((b - x0) / max(1e-6, x1 - x0) * 2 * np.pi * 2)) * .5
        d = max(da, db, .008)
        M.append(box(a, b, y - thick/2, y + thick/2, z_face + .002, z_face + .002 + depth + d))
    return M
def build(q):
    pc = q["piece"]; p = Part(); rng = np.random.default_rng(q.get("seed", 44))
    if pc == "desk":
        X0, X1 = -4.0 + .001, 4.0 - .001; z0, z1 = -.55, .45
        FD.desk_body(p, X0, -0.5 - .002, z0, z1, CH, "_L")
        FD.desk_body(p, 0.5 + .002, X1, z0, z1, CH, "_R")
        p.add("Desk_Body_A", G,
              box(-0.5 + .004, 0.5 - .004, .08, CHA - TOPT - .002, z0, z1 - .05),
              box(-0.5 + .04, 0.5 - .04, 0, .08 + E, z0 + .04, z1 - .08))
        p.add("Desk_Top_A", SSL, box(-0.5 + .006, 0.5 - .006, CHA - TOPT, CHA, z0 - .06, z1 + .1))
        # sculpted counter edge: bevelled nosing on guest overhang
        p.add("Counter_Edge", SL,
              box(X0 + .02, -0.52, CH + .002, CH + .014, z1 + .1 + .002, z1 + .125),
              box(0.52, X1 - .02, CH + .002, CH + .014, z1 + .1 + .002, z1 + .125),
              box(-0.48, 0.48, CHA + .002, CHA + .014, z1 + .1 + .002, z1 + .125))
        # layered river-slate fascia (two courses) with amber LED seam
        p.add("Fascia_Slate", SL,
              box(X0 + .06, -0.55, .55, .86, z1 + .018, z1 + .055),
              box(0.55, X1 - .06, .55, .86, z1 + .018, z1 + .055),
              box(-0.48, 0.48, .4, .68, z1 + .018, z1 + .05))
        p.add("Fascia_Gunmetal", G,
              box(X0 + .08, -0.55, .35, .55 - E, z1 + .02, z1 + .048),
              box(0.55, X1 - .08, .35, .55 - E, z1 + .02, z1 + .048),
              box(-0.46, 0.46, .28, .4 - E, z1 + .02, z1 + .045))
        p.add("River_LED", AM,
              box(X0 + .1, -0.55, .875, .91, z1 + .058, z1 + .07),
              box(0.55, X1 - .1, .875, .91, z1 + .058, z1 + .07),
              box(-0.46, 0.46, .695, .73, z1 + .055, z1 + .068),
              box(X0 + .15, -0.55, .52, .545, z1 + .058, z1 + .07),
              box(0.55, X1 - .15, .52, .545, z1 + .058, z1 + .07))
        # pebble relief seated on plinth / fascia lower band
        peb = []
        for i in range(12):
            x = rng.uniform(X0 + .4, X1 - .4)
            if abs(x) < .7 or any(abs(x - m) < .25 for m in (-3.7, -0.9, 0.9, 3.7)): continue
            r = rng.uniform(.022, .035); y = .02 + r * .55 - E
            z = rng.uniform(z1 + .055, z1 + .09)
            peb.append(node((x, y, z), r, 0))
        if peb: p.add("Pebble_Relief", SSL, *peb)
        # cable rings on fascia face
        rings = []
        for x in (-3.2, -1.8, 1.8, 3.2):
            rings += cable_ring(x, .7, z1 + .07, r=.06, tube_r=.009, seg=9)
        p.add("Cable_Rings", ALY, *rings)
        # ---- baked ticket hardware (note in GAGE_NOTES) ----
        # guest RFID / card reader pads with slot mouths
        for x, h in [(-3.2, CH), (-1.8, CH), (1.8, CH), (3.2, CH), (0.0, CHA)]:
            p.add("RFID_Reader", ALY,
                  box(x - .1, x + .1, h + .002, h + .022, z1 + .015, z1 + .07),
                  box(x - .07, x + .07, h + .022 - E, h + .038, z1 + .025, z1 + .06))
            p.add("Ticket_Slot", G, box(x - .06, x + .06, h + .008, h + .028, z1 + .085, z1 + .13))
        # staff-side ticket printers (baked) under monitors
        for x in (-3.0, -1.5, 1.5, 3.0):
            p.add("Ticket_Printer", G,
                  box(x - .14, x + .14, .76 + .002, .92, z0 - .2, z0 - .08),
                  box(x - .1, x + .1, .92 - E, .95, z0 - .18, z0 - .1))
            p.add("Printer_Mouth", ALY, box(x - .08, x + .08, .88, .91, z0 - .08 - E, z0 - .05))
            p.add("Printer_LED", AM, box(x - .03, x + .03, .955, .97, z0 - .16, z0 - .12))
        # staff ledge + monitors
        p.add("Staff_Ledge", SSL, box(X0 + .15, X1 - .15, .72, .76, z0 - .18, z0 - .004))
        p.add("Staff_Monitor_Arms", ALY,
              *[tube((x, CH + .01, z0 - .14), (x, 1.18, z0 - .14), .015, 6) for x in (-3.0, -1.5, 1.5, 3.0)])
        p.add("Staff_Screens", CY, *[box(x - .22, x + .22, 1.18 + .002, 1.42, z0 - .18, z0 - .14) for x in (-3.0, -1.5, 1.5, 3.0)])
        p.add("Screen_Bezel", ALY,
              *[box(x - .24, x + .24, 1.16, 1.18 - .002, z0 - .19, z0 - .145) for x in (-3.0, -1.5, 1.5, 3.0)],
              *[box(x - .24, x + .24, 1.42 + .002, 1.45, z0 - .19, z0 - .145) for x in (-3.0, -1.5, 1.5, 3.0)])
        # seated moss / greenery on plinth ends + between pebbles (no planter boxes)
        moss = [clump((x, .02 + .03 - E*2, z1 + .16), .035, 10 + i)
                for i, x in enumerate([-3.7, -0.9, 0.9, 3.7])]
        p.add("Seated_Moss", LF2, *moss)
        p.add("End_Tufts", LF, clump((X0 + .2, .08 + .07, z1 + .12), .09, 1), clump((X1 - .2, .08 + .07, z1 + .12), .09, 2))
        p.add("Desk-colonly", G, box(X0, -0.5, 0, CH, z0, z1), box(0.5, X1, 0, CH, z0, z1), box(-0.5, 0.5, 0, CHA, z0, z1))
        p.add("AccessKnee-colonly", G, box(-.48, .48, 0, .08, z1 - .3, z1 + .05))
    elif pc == "kiosk":
        # denser kiosk: gunmetal body, slate base band, pebble plinth, deep screen bezel
        p.add("Kiosk_Body", G, box(-.28, .28, .12, 1.08 - .002, -.22, .22))
        p.add("Kiosk_Slate_Base", SL, box(-.3, .3, .04, .12 - .002, -.24, .2),
              box(-.28, .28, .04, .12 - .002, .22 + .002, .3))
        p.add("Kiosk_Plinth", SGM, box(-.24, .24, 0, .04 - .002, -.18, .18))
        p.add("Kiosk_Top", SSL, box(-.3, .3, 1.08, 1.12, -.26, .18))
        # deep screen with layered bezel
        p.add("Kiosk_Screen", CY, box(-.18, .18, .58, .98, .26, .29))
        p.add("Kiosk_Bezel", ALY,
              box(-.24, .24, .52, .58 - .002, .24, .3), box(-.24, .24, .98 + .002, 1.04, .24, .3),
              box(-.24, -.18 - .002, .58, .98, .24, .3), box(.18 + .002, .24, .58, .98, .24, .3),
              box(-.22, .22, .54, 1.02, .3 - E, .315))  # outer reveal
        p.add("Card_Slot", ALY, box(-.07, .07, .42, .48, .24, .32))
        p.add("Ticket_Mouth", G, box(-.09, .09, .28, .36, .24, .34))
        p.add("RFID_Pad", ALY, box(-.1, .1, 1.12 + .002, 1.145, .02, .14))
        p.add("River_LED", AM, box(-.24, .24, .125, .14, .3 + .002, .32),
              box(-.24, .24, 1.05, 1.075, .3 + .002, .32))
        peb = [node((x, .02 + .02 - E, .36), .022, 0) for x in (-.15, -.05, .05, .15)]
        p.add("Pebble_Plinth", SSL, *peb)
        rings = cable_ring(0, .75, .32, r=.05, tube_r=.008, seg=8)
        p.add("Cable_Ring", ALY, *rings)
        p.add("Seated_Moss", LF2, clump((-.22, .02 + .025, .42), .025, 3), clump((.2, .02 + .025, .42), .024, 4))
        p.add("Kiosk-colonly", G, box(-.3, .3, 0, 1.12, -.24, .28))
    elif pc == "stanchion":
        p.add("Post", G, tube((0, .04 - E, 0), (0, .95, 0), .035, 8),
              box(-.12, .12, 0, .04, -.12, .12),
              box(-.05, .05, .85, .94, .035 + .002, .08))
        p.add("Post_Cap", ALY, node((0, .95 + .035 - E, 0), .038, 0))
        # sculpted double cable rings
        rings = cable_ring(0, .55, .06, r=.075, tube_r=.01, seg=10)
        rings += cable_ring(0, .72, .06, r=.06, tube_r=.009, seg=9)
        p.add("Cable_Rings", ALY, *rings)
        p.add("River_LED", AM, box(-.03, .03, .62, .66, .07, .09))
        # clean belt segment asset (fixed ribbon toward +X)
        p.add("Belt", WH, box(.08, 1.12, .88, .92, .04, .07))
        p.add("Belt_Tip", ALY, box(1.12 + .002, 1.18, .875, .925, .035, .075))
        p.add("Seated_Moss", LF2, clump((.16, .02 + .025, .16), .025, 5), clump((-.16, .02 + .025, -.14), .022, 6))
        p.add("Stanchion-colonly", G, tube((0, 0, 0), (0, .95, 0), .04, 8), box(-.12, .12, 0, .04, -.12, .12))
    else:  # backdrop
        X0, X1 = -2.0 + .001, 2.0 - .001
        p.add("Wall_Core", SL, box(X0 + .04, X1 - .04, .1, 2.32, -.06, .06))
        p.add("Wall_Frame", G, box(X0 - .05, X0 + .03, 0, 2.4, -.1, .1), box(X1 - .03, X1 + .05, 0, 2.4, -.1, .1),
              box(X0 - .05, X1 + .05, 2.33, 2.45, -.1, .1), box(X0 - .05, X1 + .05, 0, .09, -.1, .1))
        # river-wave relief bands
        waves = []
        for y in (.32, .48, .72, 2.28):
            waves += wave_strip(X0 + .3, X1 - .3, y, .06, amp=.028, n=10, thick=.018, depth=.022)
        p.add("River_Waves", SSL, *waves)
        p.add("River_LED", AM,
              box(X0 + .2, X1 - .2, .6, .63, .12 + .002, .14),
              box(X0 + .2, X1 - .2, .88, .91, .12 + .002, .14),
              box(X0 + .2, X1 - .2, 2.25, 2.28, .12 + .002, .14))
        # screen band with bezel
        p.add("Screen_Band", CY, box(X0 + .25, X1 - .25, 1.15, 1.95, .09, .12))
        p.add("Screen_Bezel", ALY,
              box(X0 + .18, X1 - .18, 1.08, 1.15 - .002, .08, .13),
              box(X0 + .18, X1 - .18, 1.95 + .002, 2.02, .08, .13),
              box(X0 + .18, X0 + .25 - .002, 1.15, 1.95, .08, .13),
              box(X1 - .25 + .002, X1 - .18, 1.15, 1.95, .08, .13))
        # sculpted TICKETS word above screen
        p.add("Wayfinding_Glyphs", CY, *glyph_word("TICKETS", X0 + .4, 2.08, 2.26, .13, cell=.16, gap=.028, thick=.016))
        # pebble base + moss
        peb = [node((x, .02 + .025, .18), .028, 0) for x in np.linspace(X0 + .4, X1 - .4, 6)]
        p.add("Pebble_Base", SSL, *peb)
        p.add("Seated_Moss", LF2, *[clump((x, .02 + .03, .28), .03, i) for i, x in enumerate([-1.5, -.5, .5, 1.5])])
        rings = cable_ring(X0 + .12, .5, .12, r=.045, tube_r=.008, seg=8) + cable_ring(X1 - .12, .5, .12, r=.045, tube_r=.008, seg=8)
        p.add("Cable_Rings", ALY, *rings)
        p.add("Backdrop-colonly", G, box(X0, X1, 0, 2.4, -.08, .08))
    return p
def clearance(prm):
    prm = dict(prm, theme="river")  # densified kit is river-only
    return FD.clearance(prm)
VARIANTS = [dict(label=f"River Queue final / {pc}", piece=pc, seed=44, theme="river") for pc in PIECES]
if __name__ == "__main__":
    FD.build = build  # so clearance() uses densified geometry
    REP = run("foyer_desk_final", build, VARIANTS, title="foyer desk final",
              names=[f"tt_foyer_{pc}" for pc in PIECES], sheet="foyer_desk_final_run_sheet.png")
    CL = {pc: clearance(dict(piece=pc, seed=44)) for pc in PIECES}
    print("CLEARANCE", CL)
    rdir = os.path.join(RENDER_OUT, "foyer_desk_final")
    json.dump(dict(rep=REP, clearance=CL), open(os.path.join(rdir, "report.json"), "w"), indent=1, default=str)
    Ry = lambda el, az: (lambda a, b: np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]) @ np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]))(np.radians(az), np.radians(el))
    fig = plt.figure(figsize=(28, 22), facecolor="#F4F2EC"); gs = fig.add_gridspec(3, 4)
    shots = [("desk", (16, 32), "desk 3/4"), ("desk", (8, -50), "desk fascia raking"), ("kiosk", (18, 40), "kiosk"), ("stanchion", (12, 25), "stanchion")]
    for j, (pc, (el, az), t) in enumerate(shots):
        p = recenter(build(dict(piece=pc, seed=44))); _, geo = export_final(p.P, [f"/tmp/fdf_{j}.glb"])
        geo = {k: v for k, v in geo.items() if "colonly" not in k}
        im = crop(render_view(geo, Ry(el, az), size=750, shadow=False, glass_alpha=.35))
        ax = fig.add_subplot(gs[0, j]); ax.imshow(np.clip(im, 0, 1)); ax.axis("off")
        r = REP[PIECES.index(pc) if pc in PIECES else 0]
        # find matching rep
        rr = next(x for x in REP if x["label"].endswith(pc) or pc in x.get("v", ""))
        ax.set_title(f"tt_foyer_{pc} ({t})\n{rr['tris']} tris | {'PASS' if rr['passed'] else 'FAIL'} | clear {'PASS' if CL[pc]['pass_'] else 'FAIL'}", fontsize=10)
    # backdrop + glyph close-up + depth
    for j, (el, az, t) in enumerate([(14, 28, "backdrop 3/4"), (5, -20, "TICKETS glyph close-up"), (25, -55, "wave relief high side")]):
        p = recenter(build(dict(piece="backdrop", seed=44))); _, geo = export_final(p.P, [f"/tmp/fdf_b{j}.glb"])
        geo = {k: v for k, v in geo.items() if "colonly" not in k}
        im = crop(render_view(geo, Ry(el, az), size=750, shadow=False, glass_alpha=.35))
        ax = fig.add_subplot(gs[1, j]); ax.imshow(np.clip(im, 0, 1)); ax.axis("off")
        rr = next(x for x in REP if "backdrop" in x.get("v", "") or x["label"].endswith("backdrop"))
        ax.set_title(f"{t}\n{rr['tris']} tris | {'PASS' if rr['passed'] else 'FAIL'}", fontsize=10)
    # hardware close-up of desk
    p = recenter(build(dict(piece="desk", seed=44))); _, geo = export_final(p.P, ["/tmp/fdf_hw.glb"])
    geo = {k: v for k, v in geo.items() if "colonly" not in k}
    im = crop(render_view(geo, Ry(5, 60), size=750, shadow=False, glass_alpha=.35))
    ax = fig.add_subplot(gs[1, 3]); ax.imshow(np.clip(im, 0, 1)); ax.axis("off")
    ax.set_title("desk hardware close-up\nRFID + ticket slot + printers", fontsize=10)
    # vignette
    A = {}
    for k in range(3):
        place(A, EB.build(dict(width=4.0)), (-6 + 4 * k, 0, -3.5), f"EB{k}")
    place(A, build(dict(piece="desk", seed=44)), (0, 0, 1.5), "DK")
    place(A, build(dict(piece="backdrop", seed=44)), (0, 0, 0.15), "BD")
    for sx in (-1, 1):
        place(A, build(dict(piece="kiosk", seed=44)), (sx * 5.2, 0, 1.2), f"K{sx}")
    for j, x in enumerate(np.linspace(-3.6, 3.6, 4)):
        place(A, build(dict(piece="stanchion", seed=44)), (x, 0, 3.2), f"ST{j}")
    Pt = Part()
    for n, (mk, m) in A.items():
        if "uv" not in m.metadata: m.metadata["uv"] = np.zeros((len(m.vertices), 2))
        Pt.add(n, mk, m)
    _, g2 = export_final(Pt.P, ["/tmp/fdfv.glb"])
    im = crop(render_view(g2, Ry(14, 28), size=1400, shadow=False, glass_alpha=.35))
    ax = fig.add_subplot(gs[2, :]); ax.imshow(np.clip(im, 0, 1)); ax.axis("off")
    ax.set_title(f"vignette: entrance bays + River Queue desk kit | clearance desk/kiosk/stanchion/backdrop: {', '.join('PASS' if CL[pc]['pass_'] else 'FAIL' for pc in PIECES)}", fontsize=12)
    fig.suptitle("Rook | #79 tt_foyer_{desk,kiosk,stanchion,backdrop} (V4 River Queue, densified) | FINAL", fontsize=16)
    plt.tight_layout(rect=(0, 0, 1, .96)); sp = os.path.join(rdir, "foyer_desk_final_sheet.png"); fig.savefig(sp, dpi=72, facecolor="#F4F2EC"); print("SHEET", sp)
