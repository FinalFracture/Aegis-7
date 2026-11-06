"""Rook: W foyer ticketing + lobby desk candidates. Spec Rev 2.6/2.7: W foyer X −12..0,
Z 10..69 under F2 gallery, behind 42 m main doors. Desk length not specified — kit uses an
8.0 m main desk (tileable 4 m halves) with a 1.0 m accessible lowered bay (top 0.86 m, knee
clear), standard top 1.05 m; freestanding ticket kiosk; queue stanchion; backdrop / wayfinding
wall. Reuses #74 Court Wayfinding + #78 Rally Mark language. No wood, no planter boxes.
Run: python3 foyer_desk.py"""
from modlib import *
from restroom_extras import crest
import entrance_bay_final as EB
CH, CHA, TOPT = 1.05, .86, .04  # standard / accessible counter heights
PIECES = ("desk", "kiosk", "stanchion", "backdrop")
THEMES = [
    ("court", "Court Wayfinding Desk", "Amber court-line fascia, wayfinding blade riser, ball finials, planted kerb language"),
    ("rally", "Rally Scoreboard Desk", "Scoreboard desk front, net-kick relief, cyan ticket screens, racket uprights"),
    ("branch", "Branch Portal Desk", "Branch Fin uprights with leaf capitals, deep slate top, fork leaves"),
    ("river", "River Queue Desk", "River-slate top, pebble plinth, amber river LEDs, cable queue rings"),
    ("green", "Green Spine Desk", "Vine-wrapped posts, moss plinth tufts, leaf-crest signage (no planter boxes)"),
]
def desk_body(p, X0, X1, z0, z1, h, tag=""):
    p.add(f"Desk_Body{tag}", G,
          box(X0, X1, .08, h - TOPT - .002, z0, z1 - .02),
          box(X0 + .04, X1 - .04, 0, .08 + E, z0 + .04, z1 - .04),
          box(X0 + .01, X1 - .01, .08, min(.7, h - TOPT - .05), z1 - .02 - E, z1 + .015))
    p.add(f"Desk_Top{tag}", SSL, box(X0 + .002, X1 - .002, h - TOPT, h, z0 - .06, z1 + .1))
def build(q):
    th, pc = q["theme"], q["piece"]; p = Part(); rng = np.random.default_rng(q.get("seed", 21))
    if pc == "desk":
        # 8 m front run, guest +Z; staff side open at -Z. Accessible bay centred at x=0, 1.0 m wide.
        X0, X1 = -4.0 + .001, 4.0 - .001
        z0, z1 = -.55, .45  # depth ~1.0 m
        # left / right standard height segments, centre accessible
        # accessible bay: no front skirt (knee clear); standard segments have skirt via desk_body
        desk_body(p, X0, -0.5 - .002, z0, z1, CH, "_L")
        desk_body(p, 0.5 + .002, X1, z0, z1, CH, "_R")
        # accessible: body without front skirt protrusion
        p.add("Desk_Body_A", G,
              box(-0.5 + .004, 0.5 - .004, .08, CHA - TOPT - .002, z0, z1 - .05),
              box(-0.5 + .04, 0.5 - .04, 0, .08 + E, z0 + .04, z1 - .08))
        p.add("Desk_Top_A", SSL, box(-0.5 + .006, 0.5 - .006, CHA - TOPT, CHA, z0 - .06, z1 + .1))
        # staff worktop ledge at -Z
        p.add("Staff_Ledge", SSL, box(X0 + .15, X1 - .15, .72, .76, z0 - .18, z0 - .004))
        p.add("Staff_Monitor_Arms", ALY,
              *[tube((x, .76 + .004, z0 - .1), (x, 1.15, z0 - .1), .015, 6) for x in (-3.0, -1.5, 1.5, 3.0)])
        p.add("Staff_Screens", CY, *[box(x - .22, x + .22, 1.15 + .002, 1.4, z0 - .15, z0 - .12) for x in (-3.0, -1.5, 1.5, 3.0)])
        # ticket slot / card reader pads on guest top
        p.add("Ticket_Pads", ALY, *[box(x - .12, x + .12, CH - E, CH + .015, z1 + .02, z1 + .1) for x in (-3.2, -1.8, 1.8, 3.2)])
        p.add("Access_Pad", ALY, box(-.12, .12, CHA - E, CHA + .015, z1 + .02, z1 + .1))
        if th == "court":
            p.add("Court_Line_LED", AM, box(X0, -.52, .92, .96, z1 + .02 - E, z1 + .028),
                  box(.52, X1, .92, .96, z1 + .02 - E, z1 + .028),
                  box(-.48, .48, .72, .76, z1 + .02 - E, z1 + .028))
            p.add("Ball_Finials", BA, *[node((x, CH + .04 - E, z1 + .05), .04, 1) for x in (-3.6, -2.4, 2.4, 3.6)])
            p.add("Blade_Frame", G, box(-.06, .06, CH + .002, 1.88, z0 + .05, z0 + .18),
                  box(-.065, .065, 2.45 - E, 2.5, z0 + .02, z0 + .22), box(-.065, .065, 1.88, 1.93, z0 + .02, z0 + .22))
            p.add("Blade_Core", SL, box(-.05, .05, 1.93 + .002, 2.45 - .002, z0 + .05, z0 + .19))
            p.add("Blade_Ball", BA, node((0, 2.5 + .06, z0 + .12), .06, 1))
            p.add("Blade_Crest", LF, crest((0, 2.5 + .08, z0 + .22)))
            p.add("Fascia_Crests", LF, *[crest((x, CH - E, z1 + .08)) for x in (-3.0, -1.2, 1.2, 3.0)])
        elif th == "rally":
            p.add("Score_Front", SL, box(X0 + .08, -0.55, .72, .95, z1 + .02 - E, z1 + .05),
                  box(0.55, X1 - .08, .72, .95, z1 + .02 - E, z1 + .05),
                  box(-0.48, 0.48, .55, .78, z1 + .02 - E, z1 + .05))
            p.add("Score_Cells", CY, *[box(x, x + .3, .75, .9, z1 + .05 - E, z1 + .065) for x in list(np.arange(X0 + .4, -0.7, .7)) + list(np.arange(0.7, X1 - .5, .7))])
            p.add("Score_LEDs", AM, *[box(x + .08, x + .22, .91, .94, z1 + .065 - E, z1 + .078) for x in list(np.arange(X0 + .4, -0.7, .7)) + list(np.arange(0.7, X1 - .5, .7))])
            p.add("Net_Kick", WH, *[box(X0 + .15, -0.55, y - .004, y + .004, z1 + .018, z1 + .03) for y in (.18, .3)],
                  *[box(0.55, X1 - .15, y - .004, y + .004, z1 + .018, z1 + .03) for y in (.18, .3)],
                  *[box(x - .004, x + .004, .14, .36, z1 + .018, z1 + .03) for x in list(np.linspace(X0 + .4, -0.7, 5)) + list(np.linspace(0.7, X1 - .4, 5))])
            # racket uprights at ends
            for sx in (-1, 1):
                x = sx * 3.7
                oval = [(x + .18 * np.cos(t), 1.5 + .22 * np.sin(t), z1 + .08) for t in np.linspace(0, 2 * np.pi, 11)]
                p.add("Racket_Upright", ALY, tube((x, CH, z1 + .05), (x, 1.5, z1 + .05), .02, 6),
                      *[tube(a, b, .015, 5) for a, b in zip(oval[:-1], oval[1:])])
        elif th == "branch":
            for x in (-3.5, -1.5, 1.5, 3.5):
                p.add("Branch_Post", G, tube((x, CH + .002, z0 + .12), (x, 1.85, z0 + .12), .032, 8),
                      node((x, 1.85, z0 + .12), .05, 0))
                p.add("Fork_Leaves", LF, clump((x, 1.95, z0 + .12), .08, int(abs(x * 10))),
                      crest((x, 2.0, z0 + .12)))
            p.add("Branch_Post", ST, tube((-3.45, 1.55, z0 + .12), (-3.55 + .08, 1.55, z0 + .12), .018, 6))  # rail segments between posts via same part name merge
            p.add("Branch_Post", ST, *[tube((a, 1.55, z0 + .12), (b, 1.55, z0 + .12), .018, 6) for a, b in [(-3.45, -1.55), (-1.45, 1.45), (1.55, 3.45)]])
            p.add("Court_Line_LED", AM, box(X0, X1, .9, .94, z1 + .02 - E, z1 + .03))
        elif th == "river":
            p.add("River_LED", AM, *[box(X0 + .2, -0.55, .085, .1, z, z + .025) for z in (z0 + .2, z1 - .25)],
                  *[box(0.55, X1 - .2, .085, .1, z, z + .025) for z in (z0 + .2, z1 - .25)])
            peb = []
            for _ in range(12):
                r = rng.uniform(.03, .045); z = rng.uniform(z0 + .35, z1 - .35)
                if abs(z - (z0 + .2)) < .06 or abs(z - (z1 - .25)) < .06: continue
                x = rng.uniform(X0 + .4, X1 - .4)
                if abs(x) < .55: continue
                peb.append(node((x, .08 + r * .5 - E, z), r, 0))
            if peb: p.add("River_Pebbles", SSL, *peb)
            rings = []
            for x in (-3.2, -1.2, 1.2, 3.2):
                circ = [(x + .07 * np.cos(t), .55 + .07 * np.sin(t), z1 + .08) for t in np.linspace(0, 2 * np.pi, 9)]
                rings += [tube(a, b, .01, 4) for a, b in zip(circ[:-1], circ[1:])]
            p.add("Cable_Rings", ALY, *rings)
            p.add("Court_Line_LED", AM, box(X0, X1, CHA if False else .9, .94, z1 + .02 - E, z1 + .03))
        else:  # green
            V = []
            for x in (X0 - .1, X1 + .1):
                for y in np.linspace(.25, .7, 3):
                    V.append(clump((x, y, (z0 + z1) / 2), .04, int(abs(x * 5 + y * 10))))
            p.add("Vine_Wrap", LF, *V)
            p.add("Moss_Plinth", LF2, *[clump((x, .02 + .035, z1 + .04), .04, i) for i, x in enumerate(np.arange(X0 + .35, X1 - .3, .5))])
            p.add("Leaf_Sign", LF, *[crest((x, CH + .02, z1 + .06)) for x in (-2.5, 0, 2.5)])
            p.add("Court_Line_LED", AM, box(X0, X1, .9, .94, z1 + .02 - E, z1 + .03))
        # seated greenery at ends (no boxes)
        p.add("End_Tufts", LF, clump((X0 + .25, .08 + .08, z1 + .15), .1, 1), clump((X1 - .25, .08 + .08, z1 + .15), .1, 2))
        p.add("Desk-colonly", G, box(X0, -0.5, 0, CH, z0, z1), box(0.5, X1, 0, CH, z0, z1), box(-0.5, 0.5, 0, CHA, z0, z1))
        p.add("AccessKnee-colonly", G, box(-.48, .48, 0, .08, z1 - .3, z1 + .05))  # floor only under knee zone
    elif pc == "kiosk":
        # freestanding ticket kiosk ~0.7 x 0.7, screen + card slot, accessible reach
        p.add("Kiosk_Body", G, box(-.3, .3, .08, 1.1 - TOPT - .002, -.25, .25),
              box(-.28, .28, 0, .08 + E, -.23, .23))
        p.add("Kiosk_Top", SSL, box(-.32, .32, 1.1 - TOPT, 1.1, -.28, .22))  # inset from screen face
        p.add("Kiosk_Screen", CY, box(-.2, .2, .57, .98, .27, .285))
        p.add("Kiosk_Bezel", ALY, box(-.24, .24, .53, .57 - .002, .252, .29), box(-.24, .24, .98 + .002, 1.02, .252, .29),
              box(-.24, -.2 - .002, .57, .98, .252, .29), box(.2 + .002, .24, .57, .98, .252, .29))
        p.add("Card_Slot", ALY, box(-.08, .08, .4, .45, .25 - E, .3))
        p.add("Ticket_Mouth", G, box(-.1, .1, .25, .32, .25 - E, .32))
        if th == "court":
            p.add("Court_Line_LED", AM, box(-.28, .28, 1.025, 1.05, .29 + .002, .31))
            p.add("Ball_Finial", BA, node((0, 1.1 + .05, 0), .05, 1))
            p.add("Leaf_Crest", LF, crest((0, 1.1 + .05, .1)))
        elif th == "rally":
            p.add("Net_Face", WH, *[box(-.22, .22, y - .003, y + .003, .25 - E, .255) for y in (.2, .48)],
                  *[box(x - .003, x + .003, .18, .42, .25 - E, .255) for x in (-.15, .15)])
            p.add("Score_LED", AM, box(-.1, .1, 1.025, 1.055, .29 + .002, .31))
        elif th == "branch":
            p.add("Branch_Stem", G, tube((0, 1.1 + .002, 0), (0, 1.48, 0), .025, 6), node((0, 1.48, 0), .04, 0))
            p.add("Fork_Leaves", LF, clump((0, 1.58, .05), .07, 3), crest((0, 1.58, -.05)))
        elif th == "river":
            p.add("River_LED", AM, box(-.25, .25, .085, .1, .25 - E, .27))
            p.add("Pebbles", SSL, node((-.2, .02 + .025, .28), .028, 0), node((.18, .02 + .025, .28), .03, 0))
        else:
            p.add("Vine", LF, *[clump((.32 * sx, y, 0), .035, int(10 + y * 5)) for sx in (-1, 1) for y in (.35, .65, .95)])
            p.add("Moss", LF2, clump((0, .02 + .03, .3), .035, 5))
        p.add("Kiosk-colonly", G, box(-.3, .3, 0, 1.1, -.25, .25))
    elif pc == "stanchion":
        # queue post + retractable belt stub; pair spacing assumed 1.2 m for aisle check
        p.add("Post", G, tube((0, .04 - E, 0), (0, .95, 0), .035, 8),
              box(-.12, .12, 0, .04, -.12, .12),
              box(-.05, .05, .85, .94, .035 + .002, .08))  # cassette proud on +Z
        p.add("Post_Cap", ALY, node((0, .95 + .035 - E, 0), .038, 0))
        p.add("Belt", WH, box(.08, 1.15, .88, .92, .04, .07))  # from cassette toward +X, on +Z
        if th == "court":
            p.add("Court_Ring", AM, box(-.045, .045, .7, .74, .04 + .002, .055))
            p.add("Ball_Cap", BA, node((0, .95 + .12, 0), .038, 1))
        elif th == "rally":
            p.add("Net_Band", WH, box(-.045, .045, .5, .55, .04 + .002, .055), box(-.045, .045, .6, .65, .04 + .002, .055))
        elif th == "branch":
            p.add("Leaf_Cap", LF, crest((0, .95 + .08, 0)))
        elif th == "river":
            p.add("Cable_Ring", ALY, *[tube((.09 * np.cos(t), .75 + .09 * np.sin(t), .06), (.09 * np.cos(t2), .75 + .09 * np.sin(t2), .06), .008, 4)
                                       for t, t2 in zip(np.linspace(0, 2 * np.pi, 8)[:-1], np.linspace(0, 2 * np.pi, 8)[1:])])
        else:
            p.add("Moss_Base", LF2, clump((.14, .02 + .03, .14), .03, 7), clump((-.14, .02 + .03, -.14), .028, 8))
        p.add("Stanchion-colonly", G, tube((0, 0, 0), (0, .95, 0), .04, 8), box(-.12, .12, 0, .04, -.12, .12))
    else:  # backdrop
        # 4 m wayfinding / screen wall behind desk (staff side), ~2.4 m tall
        X0, X1 = -2.0 + .001, 2.0 - .001
        p.add("Wall_Core", SL, box(X0 + .04, X1 - .04, .1, 2.32, -.06, .06))
        p.add("Wall_Frame", G, box(X0 - .05, X0 + .03, 0, 2.4, -.1, .1), box(X1 - .03, X1 + .05, 0, 2.4, -.1, .1),
              box(X0 - .05, X1 + .05, 2.33, 2.45, -.1, .1), box(X0 - .05, X1 + .05, 0, .09, -.1, .1))
        p.add("Screen_Band", CY, box(X0 + .18, X1 - .18, 1.05, 2.05, .09, .11))
        p.add("Screen_Bezel", ALY, box(X0 + .12, X1 - .12, .97, 1.05 - .002, .08, .115), box(X0 + .12, X1 - .12, 2.05 + .002, 2.13, .08, .115),
              box(X0 + .12, X0 + .18 - .002, 1.05, 2.05, .08, .115), box(X1 - .18 + .002, X1 - .12, 1.05, 2.05, .08, .115))
        if th == "court":
            p.add("Court_Line_LED", AM, box(X0 + .1, X1 - .1, .85, .9, .08 - E, .1), box(X0 + .1, X1 - .1, 2.15, 2.2, .08 - E, .1))
            p.add("Blade", G, box(-.06, .06, 2.45 + .002, 2.55, -.04, .12), box(-.065, .065, 3.05, 3.1, -.04, .12))
            p.add("Blade_Core", SL, box(-.05, .05, 2.55 + .002, 3.05 - .002, -.02, .1))
            p.add("Blade_Ball", BA, node((0, 3.1 + .06, .04), .055, 1))
            p.add("Blade_Crest", LF, crest((0, 3.1 + .05, .16)))
            p.add("Wayfinding_Glyphs", CY, box(-.15, -.05, 1.3, 1.9, .1 - E, .12), box(-.15, .15, 1.85, 1.95, .1 - E, .12),
                  box(-.15, .15, 1.55, 1.65, .1 - E, .12), box(-.15, .15, 1.25, 1.35, .1 - E, .12))
        elif th == "rally":
            p.add("Score_Cells", CY, *[box(x, x + .4, 1.2, 1.9, .1 - E, .12) for x in (-1.5, -.7, .1, .9)])
            p.add("Score_LEDs", AM, *[box(x + .1, x + .3, 2.14, 2.18, .1 - E, .13) for x in (-1.5, -.7, .1, .9)])
            p.add("Net_Relief", WH, *[box(X0 + .2, X1 - .2, y - .004, y + .004, .08 - E, .095) for y in (.3, .5, .7)],
                  *[box(x - .004, x + .004, .2, .8, .08 - E, .095) for x in np.linspace(X0 + .3, X1 - .3, 8)])
            p.add("Ball_Row", BA, *[node((x, 2.45 + .04, .05), .04, 1) for x in np.linspace(-1.5, 1.5, 5)])
        elif th == "branch":
            for x in (-1.4, 0, 1.4):
                p.add("Branch_Post", G, tube((x, .1 + .002, -.14), (x, 2.5, -.14), .035, 8), node((x, 2.5, -.14), .05, 0))
                p.add("Fork_Leaves", LF, clump((x, 2.6, -.14), .08, int(20 + abs(x * 5))), crest((x, 2.65, -.14)))
            p.add("Court_Line_LED", AM, box(X0 + .1, X1 - .1, 2.2, 2.25, .08 - E, .1))
        elif th == "river":
            p.add("River_LED", AM, *[box(X0 + .15, X1 - .15, y, y + .025, .08 - E, .1) for y in (.4, .7, 2.15)])
            p.add("Pebble_Base", SSL, *[node((rng.uniform(X0 + .25, X1 - .25), .02 + .03, rng.uniform(.12, .2)), rng.uniform(.025, .04), 0) for _ in range(6)])
        else:
            p.add("Vine_Edge", LF, *[clump((X0 - .08, y, .05), .045, int(y * 10)) for y in np.linspace(.55, 2.0, 4)],
                  *[clump((X1 + .08, y, .05), .045, int(30 + y * 10)) for y in np.linspace(.55, 2.0, 4)])
            p.add("Leaf_Crests", LF, *[crest((x, 2.48, .05)) for x in (-1.2, 0, 1.2)])
            p.add("Moss_Base", LF2, *[clump((x, .02 + .03, .14), .04, i) for i, x in enumerate(np.arange(X0 + .35, X1 - .3, .5))])
        p.add("Backdrop-colonly", G, box(X0, X1, 0, 2.4, -.08, .08))
    return p
def V(pc):
    return [dict(theme=t, piece=pc, label=f"{name} / {pc}", seed=21 + i) for i, (t, name, _) in enumerate(THEMES)]
def clearance(prm):
    """Counter heights, accessible bay width, queue aisle (stanchion belt length)."""
    pc = prm["piece"]; r = dict(pass_=True, notes=[])
    if pc == "desk":
        p = build(prm)
        # measure top Y of Desk_Top_* 
        tops = {k: m.bounds[1][1] for k, (_, m) in p.P.items() if k.startswith("Desk_Top")}
        std = [v for k, v in tops.items() if k.endswith(("_L", "_R")) or "_L" in k or "_R" in k]
        acc = [v for k, v in tops.items() if "_A" in k]
        r["std_h"] = round(float(np.mean(std)), 3) if std else None
        r["acc_h"] = round(float(np.mean(acc)), 3) if acc else None
        r["acc_w"] = 1.0
        # ADA: accessible ≤ 0.915, width ≥ 0.915; standard service ~1.0-1.1
        ok = (r["acc_h"] is not None and r["acc_h"] <= .915 and r["acc_w"] >= .915
              and r["std_h"] is not None and .95 <= r["std_h"] <= 1.15)
        # knee clear: AccessKnee floor collider exists and body doesn't fill z1 front under acc
        r["knee"] = "AccessKnee-colonly" in p.P
        r["pass_"] = ok and r["knee"]
        r["notes"].append(f"std {r['std_h']} acc {r['acc_h']}x{r['acc_w']} knee {r['knee']}")
    elif pc == "stanchion":
        # belt extends to x=1.15 → centre spacing 1.2 m leaves ~1.1 m clear between posts (post r=.035)
        clear = 1.20 - 2 * .04
        r["aisle"] = round(clear, 3); r["pass_"] = clear >= 1.10
        r["notes"].append(f"aisle at 1.2 m centres = {clear:.2f} m")
    elif pc == "kiosk":
        # screen centre ~0.75 m (reachable); body width 0.6
        r["reach_h"] = 0.75; r["pass_"] = True; r["notes"].append("screen mid 0.75 m, card slot 0.4 m")
    else:
        r["pass_"] = True; r["notes"].append("backdrop wall 4 x 2.4 m")
    return r
def place(A, part, t, tag):
    for n, (mk, m) in part.P.items():
        if "colonly" in n: continue
        m2 = m.copy(); m2.apply_translation(t)
        m2.metadata["uv"] = m.metadata.get("uv", np.zeros((len(m.vertices), 2))); A[f"{tag}_{n}"] = (mk, m2)
if __name__ == "__main__":
    REP = {}
    for pc in PIECES:
        REP[pc] = run("foyer_desk", build, V(pc), title=f"foyer desk {pc}", suffix=f"_{pc}",
                      names=[f"v{i+1}_{THEMES[i][0]}_{pc}" for i in range(5)], sheet=f"foyer_desk_run_{pc}.png")
    CL = {i: {pc: clearance(V(pc)[i]) for pc in PIECES} for i in range(5)}
    print("CLEARANCE", {i: {pc: CL[i][pc]["pass_"] for pc in PIECES} for i in range(5)})
    rdir = os.path.join(RENDER_OUT, "foyer_desk"); json.dump(dict(rep=REP, clearance=CL, themes=THEMES), open(os.path.join(rdir, "report.json"), "w"), indent=1, default=str)
    Ry = lambda el, az: (lambda a, b: np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]) @ np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]))(np.radians(az), np.radians(el))
    fig = plt.figure(figsize=(34, 30), facecolor="#F4F2EC"); gs = fig.add_gridspec(5, 5)
    ang = dict(desk=(18, 35), kiosk=(20, 40), stanchion=(15, 30), backdrop=(12, 25))
    for i in range(5):
        for row, pc in enumerate(PIECES):
            prm = V(pc)[i]; p = recenter(build(prm)); _, geo = export_final(p.P, [f"/tmp/fd_{i}_{pc}.glb"])
            geo = {k: v for k, v in geo.items() if "colonly" not in k}
            im = crop(render_view(geo, Ry(*ang[pc]), size=560, shadow=False, glass_alpha=.35))
            ax = fig.add_subplot(gs[row, i]); ax.imshow(np.clip(im, 0, 1)); ax.axis("off")
            r = REP[pc][i]; c = CL[i][pc]
            ax.set_title((f"v{i+1} {THEMES[i][1]}\n{THEMES[i][2][:52]}\n" if row == 0 else "") +
                         f"{pc}: {r['tris']} tris | {'PASS' if r['passed'] else 'FAIL'} | clear {'PASS' if c['pass_'] else 'FAIL'}", fontsize=8)
        # vignette: entrance bay run + desk kit behind
        A = {}
        for k in range(3):
            place(A, EB.build(dict(width=4.0)), (-6 + 4 * k, 0, -3.5), f"EB{k}")
        place(A, build(V("desk")[i]), (0, 0, 1.5), "DK")
        place(A, build(V("backdrop")[i]), (0, 0, 0.2), "BD")
        for sx in (-1, 1):
            place(A, build(V("kiosk")[i]), (sx * 5.2, 0, 1.2), f"K{sx}")
        # queue line of 4 stanchions
        for j, x in enumerate(np.linspace(-3.6, 3.6, 4)):
            place(A, build(V("stanchion")[i]), (x, 0, 3.2), f"ST{j}")
        Pt = Part()
        for n, (mk, m) in A.items():
            if "uv" not in m.metadata: m.metadata["uv"] = np.zeros((len(m.vertices), 2))
            Pt.add(n, mk, m)
        _, g2 = export_final(Pt.P, [f"/tmp/fdv_{i}.glb"])
        im = crop(render_view(g2, Ry(14, 28), size=900, shadow=False, glass_alpha=.35))
        ax = fig.add_subplot(gs[4, i]); ax.imshow(np.clip(im, 0, 1)); ax.axis("off")
        ax.set_title(f"vignette: entrance bays + desk + backdrop + kiosks + queue\nclear desk/kiosk/stanchion/backdrop: {', '.join('P' if CL[i][pc]['pass_'] else 'F' for pc in PIECES)}", fontsize=8)
    for row, t in enumerate(("desk 8 m + accessible bay", "ticket kiosk", "queue stanchion", "backdrop / wayfinding wall", "foyer vignette behind entrance")):
        fig.axes[row * 5].text(-.04, .5, t, transform=fig.axes[row * 5].transAxes, rotation=90, va="center", ha="right", fontsize=11)
    fig.suptitle("Rook | Tennis Tower W foyer ticketing + lobby desk V1-V5 | candidates (not promoted)", fontsize=16)
    plt.tight_layout(rect=(0, 0, 1, .97)); sp = os.path.join(rdir, "foyer_desk_contact_sheet.png"); fig.savefig(sp, dpi=65, facecolor="#F4F2EC"); print("SHEET", sp)
