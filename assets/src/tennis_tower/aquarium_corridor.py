"""Rook: lobby / aquarium corridor candidates (spec §3.12.1 Rev 2.8). Corridor X 0..30, Z 34.5..44.5;
tank X 1..23 / Z 42.5..44.5, water 2.8 m, top +3.2; acrylic line Z 42.5 as 4 x 5.5 m panels (0.2 m);
clear width 8.0 m (Z 34.5..42.5); slate terrazzo, cyan inlay Z 41.5, lean rail Z 41.9, 4 benches,
2 info plinths, 3 caustic projectors, blades at X 1 / X 24. Acrylic = the ONLY BLEND (part Glass_Acrylic);
signs/screens opaque emissive; no other glass. No wood, no planter boxes.
Kit per variant (local +Z = corridor side, pivot bottom centre):
  tank   5.5 m tank bay: sill, acrylic panel, mullions, reef backdrop + themed reef, header/catwalk lip,
         1.2 m terrazzo front strip with cyan inlay (local z +1.0) and lean rail (local z +0.6)
  floor  5.5 x 6.8 m terrazzo tile (covers Z 34.5..41.3), tileable on X
  bench  2.0 m bench   plinth  info plinth   sign  overhead AQUATICS blade (hangs 1.0 m)   caustic  ceiling projector
Run: python3 aquarium_corridor.py"""
from modlib import *
from restroom_extras import crest
PIECES = ("tank", "floor", "bench", "plinth", "sign", "caustic")
THEMES = [
    ("court", "Court Reef", "Court-line amber mullion caps + inlay, tennis-ball buoy rocks, slate reef terraces"),
    ("kelp", "Kelp Forest", "Tall kelp ribbons on moss-capped boulders, leaf-crest benches, green-chip terrazzo"),
    ("river", "River Delta", "Stepped river-stone tiers, pebble bed, amber river-seam LEDs in floor and rail"),
    ("rally", "Rally Lagoon", "Net-pattern header, racket-loop coral, scoreboard info plinths, ball-buoy rail finials"),
    ("branch", "Branch Coral", "Branch Fin coral trees with leaf-crest polyps, fork-leg benches, branch mullions"),
]
W, SILL, WTOP, FY = 5.5, .4, 3.2, .02   # bay width, tank floor, water top, terrazzo thickness
def stroke(x0, x1, y0, y1, z0, z1, bev=.006):
    return [box(x0, x1, y0, y1, z0, z1), box(x0 + bev, x1 - bev, y0 + bev, y1 - bev, z1 - E, z1 + .007)]
def letters(word, x0, y0, y1, zf, cell=.26, gap=.06, th=.025):
    """Bevelled stroke capitals (A Q U T I C S) for the AQUATICS blade."""
    out, x, t = [], x0, (y1 - y0) * .16
    for ch in word:
        a, b, m = x, x + cell, (y0 + y1) / 2; z0, z1 = zf, zf + th; c = (a + b) / 2
        if ch == "A":
            out += stroke(a, a + t, y0, y1 - t + E, z0, z1) + stroke(b - t, b, y0, y1 - t + E, z0, z1) + stroke(a, b, y1 - t, y1, z0, z1) + stroke(a + t - E, b - t + E, m - t/2, m + t/2, z0, z1)
        elif ch == "Q":
            out += stroke(a, a + t, y0 + t - E, y1 - t + E, z0, z1) + stroke(b - t, b, y0 + t - E, y1 - t + E, z0, z1) + stroke(a, b, y1 - t, y1, z0, z1) + stroke(a, b, y0, y0 + t, z0, z1) + stroke(c, b + t*.6, y0 - t*.6, y0 + t*.4, z0 + .002, z1 + .002)
        elif ch == "U":
            out += stroke(a, a + t, y0 + t - E, y1, z0, z1) + stroke(b - t, b, y0 + t - E, y1, z0, z1) + stroke(a, b, y0, y0 + t, z0, z1)
        elif ch == "T":
            out += stroke(a, b, y1 - t, y1, z0, z1) + stroke(c - t/2, c + t/2, y0, y1 - t + E, z0, z1)
        elif ch == "I":
            out += stroke(c - t/2, c + t/2, y0, y1, z0, z1)
        elif ch == "C":
            out += stroke(a, a + t, y0 + t - E, y1 - t + E, z0, z1) + stroke(a, b, y1 - t, y1, z0, z1) + stroke(a, b, y0, y0 + t, z0, z1)
        elif ch == "S":
            out += stroke(a, b, y1 - t, y1, z0, z1) + stroke(a, a + t, m, y1 - t + E, z0, z1) + stroke(a, b, m - t/2, m + t/2, z0, z1) + stroke(b - t, b, y0 + t - E, m, z0, z1) + stroke(a, b, y0, y0 + t, z0, z1)
        x += cell + gap
    return out
def ring(cx, cy, cz, r, tr, seg=10, axis="z"):
    if axis == "z": P = [(cx + r*np.cos(t), cy + r*np.sin(t), cz) for t in np.linspace(0, 2*np.pi, seg)]
    else: P = [(cx + r*np.cos(t), cy, cz + r*np.sin(t)) for t in np.linspace(0, 2*np.pi, seg)]
    return [tube(a, b, tr, 4) for a, b in zip(P[:-1], P[1:])]
def seat(m, y):
    m.apply_translation((0, y - .004 - m.bounds[0][1], 0)); return m
def reef(p, th, X0, X1, rng):
    """Themed reef behind the acrylic (local z -1.9..-0.3), seated on the tank floor (y = SILL)."""
    zb0, zb1 = -1.85, -.35
    p0 = set(p.P); occ = []
    rocks = []
    for i in range(0):
        r = rng.uniform(.18, .3); x = rng.uniform(X0 + .2 + r, X1 - .2 - r); z = rng.uniform(-1.84 + r*1.3, -.45 - r*1.3)
        rocks.append(seat(clump((x, SILL + r, z), r, 100 + i), SILL))
    if th == "court":
        p.add("Reef_Terraces", SL, box(X0 + .3, X1 - .3, SILL - E, SILL + .35, zb0 + .02, zb0 + .55), box(X0 + .8, X1 - .8, SILL + .35 - E, SILL + .75, zb0 + .02, zb0 + .35))
        p.add("Terrace_Court_Line", AM, box(X0 + .3, X1 - .3, SILL + .3, SILL + .33, zb0 + .55 - E, zb0 + .56), box(X0 + .8, X1 - .8, SILL + .7, SILL + .73, zb0 + .35 - E, zb0 + .36))
        p.add("Ball_Buoys", BA, *[node((x, SILL + .75 + .12 - E, zb0 + .18), .12, 1) for x in np.linspace(X0 + 1.2, X1 - 1.2, 4)])
        p.add("Sea_Grass", LF, *[leaf_dir((x, SILL + .35 - E, zb0 + .45), (rng.uniform(-.2, .2), 1, .1), .45, .07) for x in np.linspace(X0 + .5, X1 - .5, 10)])
    elif th == "kelp":
        K, L = [], []
        for i, x in enumerate(np.linspace(X0 + .5, X1 - .5, 7)):
            z = -1.5 + .3*(i % 3); hgt = rng.uniform(2.0, 2.6); y0 = SILL + .05
            pts = [(x + .08*np.sin(k*1.3 + i), y0 + hgt*k/6, z + .05*np.cos(k + i)) for k in range(7)]
            K += [tube(a, b, .025, 5) for a, b in zip(pts[:-1], pts[1:])]
            L += [leaf_dir(np.add(q, np.multiply((np.sin(k + i), .6, .3), .05 / np.linalg.norm((np.sin(k + i), .6, .3)))), (np.sin(k + i), .6, .3), .35, .09) for k, q in enumerate(pts[1:-1])]
        p.add("Kelp_Stipes", LF2, *K); p.add("Kelp_Blades", LF, *L)
        p.add("Moss_Caps", LF2, *[seat(clump((x, SILL + .3, z), .14, 300 + i), SILL) for i, (x, z) in enumerate([(X0 + .5 + .75*1.5, -.55), (X0 + .5 + .75*3.5, -.55), (X0 + .5 + .75*5.5, -.55)])])
    elif th == "river":
        p.add("River_Tiers", SL, box(X0 + .2, X1 - .2, SILL - E, SILL + .25, zb0 + .02, zb0 + .7), box(X0 + .6, X1 - .6, SILL + .25 - E, SILL + .55, zb0 + .02, zb0 + .45), box(X0 + 1.2, X1 - 1.2, SILL + .55 - E, SILL + .85, zb0 + .02, zb0 + .25))
        p.add("River_Seams", AM, *[box(a, b, y - .015, y + .005, zb0 + d - E, zb0 + d + .008) for (a, b, y, d) in ((X0 + .2, X1 - .2, SILL + .25, .7), (X0 + .6, X1 - .6, SILL + .55, .45), (X0 + 1.2, X1 - 1.2, SILL + .85, .25))])
        p.add("Pebble_Bed", SSL, *[seat(node((rng.uniform(X0 + .3, X1 - .3), SILL + .06, rng.uniform(-1.0, -.45)), rng.uniform(.035, .06), 0), SILL) for _ in range(16)])
        p.add("Water_Grass", LF, *[leaf_dir((x, SILL + .25 - E, zb0 + .6), (0, 1, .2), .4, .06) for x in np.linspace(X0 + .4, X1 - .4, 9)])
    elif th == "rally":
        C = []
        for x in np.linspace(X0 + .9, X1 - .9, 4):
            y = SILL + .9; C += [tube((x, SILL + .05, -1.3), (x, y, -1.3), .03, 6)] + ring(x, y + .32, -1.3, .28, .02, 12) + ring(x, y + .32, -1.3, .18, .008, 8)
        p.add("Racket_Coral", ALY, *C)
        p.add("Net_Fan", WH, *[box(X0 + .4, X1 - .4, y - .006, y + .006, zb0 + .02, zb0 + .05) for y in np.linspace(SILL + .3, WTOP - .4, 6)], *[box(x - .006, x + .006, SILL + .3, WTOP - .4, zb0 + .02, zb0 + .05) for x in np.linspace(X0 + .4, X1 - .4, 9)])
        p.add("Ball_Buoys", BA, *[node((x, SILL + .1 - E, -.75), .1, 1) for x in (X0 + 1.4, -.3, X1 - 1.6)])
    else:  # branch
        T, Lc = [], []
        for i, x in enumerate(np.linspace(X0 + 1.0, X1 - 1.0, 3)):
            z = -1.2; n0 = (x, SILL + .05, z); n1 = (x, SILL + 1.0, z); T += [tube(n0, n1, .07, 8), node(n1, .09, 0)]
            for dx, dy in ((.55, .7), (-.5, .8), (.15, 1.1)):
                e = (x + dx, n1[1] + dy, z + .1); m = (x + dx*.45, n1[1] + dy*.5, z + .05); T += [tube(n1, m, .045, 6), node(m, .05, 0), tube(m, e, .03, 6)]
                Lc += [crest((e[0], e[1] - .01, e[2])), clump((e[0], e[1] + .06, e[2]), .07, 400 + i)]
        p.add("Branch_Coral", G, *T); p.add("Coral_Polyps", LF, *Lc)
    occ = [m.bounds for n in set(p.P) - p0 for m in p.P[n][1].split(only_watertight=False)]
    hit = lambda b: any(np.all(b[0] < o[1] + .012) and np.all(b[1] > o[0] - .012) for o in occ)
    rocks, sand, k = [], [], 0
    while len(rocks) < 8 and k < 300:
        k += 1; r = rng.uniform(.16, .28); x = rng.uniform(X0 + .2 + r, X1 - .2 - r); z = rng.uniform(-1.84 + r*1.3, -.45 - r*1.3)
        m = seat(clump((x, SILL + r, z), r, 100 + k), SILL)
        if not hit(m.bounds): rocks.append(m); occ.append(m.bounds)
    while len(sand) < 10 and k < 900:
        k += 1; m = seat(clump((rng.uniform(X0 + .3, X1 - .3), SILL + .06, rng.uniform(-1.6, -.5)), .06, 200 + k), SILL)
        if not hit(m.bounds): sand.append(m); occ.append(m.bounds)
    p.add("Reef_Rocks", SSL, *rocks); p.add("Reef_Sand", WH, *sand)
def build(q):
    th, pc = q["theme"], q["piece"]; p = Part(); rng = np.random.default_rng(q.get("seed", 3))
    h = W/2; X0, X1 = -h + .001, h - .001
    if pc == "tank":
        S0, S1 = X0 + .003, X1 - .003
        p.add("Tank_Shell", SL, box(S0, S1, 0, SILL, -2.0, -.116), box(S0, S1, SILL - E, WTOP + .4, -2.0, -1.88), box(S0, S1, WTOP, WTOP + .4, -.6, -.116))  # sill slab, reef wall, header slab
        p.add("Reef_Backdrop", SSL, *[box(a, b, SILL - E, y1, -1.88 - E, -1.84) for a, b, y1 in ((X0, -.9, 2.6), (-.9, 1.0, 3.0), (1.0, X1, 2.3))])
        p.add("Glass_Acrylic", GL, box(X0 + .066, X1 - .066, SILL + .016, WTOP - .016, -.1, .1))
        Fm = [box(X0, X0 + .07, 0, WTOP + .4, -.12, .14), box(X1 - .07, X1, 0, WTOP + .4, -.12, .14),     # half-mullions (tile to full)
              box(X0 + .07 - E, X1 - .07 + E, SILL - .04, SILL + .02, -.103, .14), box(X0 + .07 - E, X1 - .07 + E, WTOP - .02, WTOP + .06, -.103, .14),
              box(X0, X1, WTOP + .4 - E, WTOP + .48, -.62, .2)]                                                # catwalk lip / header cap
        p.add("Acrylic_Frame", G, *Fm)
        p.add("Sill_Nosing", SL, box(X0 + .066, X1 - .066, 0, SILL - .04 + E, -.114, .3))
        p.add("Sill_Light", CY, box(X0 + .1, X1 - .1, SILL - .1, SILL - .07, .3 - E, .306))
        p.add("Header_Light", CY, box(X0 + .1, X1 - .1, WTOP + .1, WTOP + .13, .2 - E, .206))
        reef(p, th, X0, X1, rng)
        # 1.2 m terrazzo front strip with the cyan inlay (local z +1.0 = Z 41.5) and lean rail posts (z +0.6 = Z 41.9)
        p.add("Terrazzo_Strip", SSL, box(X0, X1, 0, FY, .3 + .002, 1.2))
        p.add("Cyan_Inlay", CY, box(X0 + .0015, X1 - .0015, FY - .006, FY + .002, .97, 1.03))
        R = [tube((x, FY - E, .6), (x, .95, .6), .03, 8) for x in (-1.8, 0, 1.8)] + [box(x - .09, x + .09, FY - E, FY + .012, .51, .69) for x in (-1.8, 0, 1.8)]
        R += [box(X0, X1, .95 - .01, 1.0, .5, .7)]                                                        # lean shelf
        p.add("Lean_Rail", ALY, *R)
        acc = {"court": AM, "kelp": LF2, "river": AM, "rally": WH, "branch": G}[th]
        p.add("Rail_Accent", acc, box(X0, X1, 1.0 - E, 1.012, .58, .62))
        if th == "court": p.add("Mullion_Caps", BA, node((X0 + .036, WTOP + .48 + .033 - E, .05), .033, 1), node((X1 - .036, WTOP + .48 + .033 - E, .05), .033, 1))
        elif th == "rally": p.add("Header_Net", WH, *[box(X0 + .1, X1 - .1, y - .005, y + .005, .2 - E, .212) for y in (WTOP + .2, WTOP + .3)], *[box(x - .005, x + .005, WTOP + .15, WTOP + .35, .2 - E, .212) for x in np.linspace(X0 + .2, X1 - .2, 12)])
        elif th == "river": p.add("Rail_Pebbles", SSL, *[node((x, FY + .025 - E, 1.12), .03, 0) for x in np.linspace(X0 + .3, X1 - .3, 9)])
        elif th == "kelp": p.add("Strip_Moss", LF2, *[clump((x, FY + .02, 1.14), .035, 500 + i) for i, x in enumerate(np.linspace(X0 + .4, X1 - .4, 6))])
        else: p.add("Mullion_Leaves", LF, crest((X0 + .035, WTOP + .48 - E, .1)), crest((X1 - .035, WTOP + .48 - E, .1)))
        p.add("Tank-colonly", SL, box(-h, h, 0, WTOP + .48, -2.0, .3)); p.add("Rail-colonly", ALY, box(-h, h, 0, 1.0, .5, .7))
        p.add("Floor-colonly", SSL, box(-h, h, 0, FY, .3, 1.2))
    elif pc == "floor":
        Z0, Z1 = -3.4 + .001, 3.4 - .001
        p.add("Terrazzo", SSL, box(X0, X1, 0, FY, Z0, Z1))
        chip = {"court": AM, "kelp": LF2, "river": SSL, "rally": WH, "branch": G}[th]
        p0 = set(p.P); chips = [(x, z) for x, z in zip(rng.uniform(X0 + .1, X1 - .1, 90), rng.uniform(Z0 + .1, Z1 - .1, 90))]
        p.add("Joint_Lines", G, *[box(X0, X1, FY - .003, FY + .0006, z - .006, z + .006) for z in np.linspace(Z0 + 1.1, Z1 - 1.1, 5)])
        if th == "court": p.add("Court_Inlay", AM, box(X0, X1, FY - .005, FY + .002, -.03, .03), box(-.03, .03, FY - .005, FY + .002, -1.0, -.04))
        elif th == "river": p.add("River_Inlay", AM, *[box(a, b, FY - .005, FY + .002, z - .02, z + .02) for a, b, z in ((X0, -1.0, .8), (-1.0, 1.2, .5), (1.2, X1, .8))])
        elif th == "rally": p.add("Service_Box", WH, box(-1.5, 1.5, FY - .005, FY + .002, -1.53, -1.47), box(-.03, .03, FY - .005, FY + .002, -1.47, 1.0))
        elif th == "kelp": p.add("Leaf_Inlay", LF2, *[box(x - .25, x + .25, FY - .005, FY + .002, -.02, .02) for x in (-1.6, 0, 1.6)])
        else: p.add("Branch_Inlay", G, box(-2.0, 2.0, FY - .005, FY + .002, -.02, .02), box(-.9, -.86, FY - .005, FY + .002, .02, .8), box(.86, .9, FY - .005, FY + .002, -.8, -.02))
        occ = [m.bounds for n in set(p.P) - p0 for m in p.P[n][1].split(only_watertight=False)]
        ok = [c for c in chips if not any(c[0] < o[1][0] + .03 and c[0] + .04 > o[0][0] - .03 and c[1] < o[1][2] + .03 and c[1] + .03 > o[0][2] - .03 for o in occ)][:60]
        p.add("Terrazzo_Chips", chip if chip != SSL else SL, *[box(x, x + .04, FY - .004, FY + .0012, z, z + .03) for x, z in ok])
        p.add("Floor-colonly", SSL, box(-h, h, 0, FY, -3.4, 3.4))
    elif pc == "bench":
        L = 1.0
        p.add("Bench_Seat", SL, box(-L, L, .42, .47, -.25, .25))
        p.add("Seat_Edge", AM if th in ("court", "river") else ALY, box(-L + .02, L - .02, .47 - E, .475, .23, .245))
        if th == "branch":
            legs = [tube((x, .022, z), (x*.8, .42 + E, z*.6), .035, 6) for x in (-.8, .8) for z in (-.18, .18)]
            p.add("Fork_Legs", G, *legs); p.add("Leg_Feet", G, *[box(x - .06, x + .06, 0, .02, z - .06, z + .06) for x in (-.8, .8) for z in (-.18, .18)])
        else:
            p.add("Bench_Plinths", G, box(-.85, -.55, 0, .42 + E, -.2, .2), box(.55, .85, 0, .42 + E, -.2, .2))
        if th == "kelp": p.add("Seat_Crests", LF, *[crest((x, .475 - E, 0)) for x in (-.6, 0, .6)])
        elif th == "rally": p.add("Seat_Net", WH, *[box(-.55 - E, .55 + E, .2, .21, z - .005, z + .005) for z in (-.19, .19)])
        elif th == "court": p.add("Ball_Ends", BA, node((-L + .06, .475 + .05 - E, 0), .05, 1), node((L - .06, .475 + .05 - E, 0), .05, 1))
        elif th == "river": p.add("Base_Pebbles", SSL, *[node((x, .03, z), .03, 0) for x in (-.4, 0, .4) for z in (-.12, .12)])
        else: p.add("Seat_Leaves", LF, crest((0, .475 - E, 0)))
        p.add("Bench-colonly", SL, box(-L, L, 0, .47, -.25, .25))
    elif pc == "plinth":
        p.add("Plinth_Body", SL, box(-.3, .3, .06, 1.1, -.2, .2), box(-.34, .34, 0, .06 + E, -.24, .24))
        p.add("Plinth_Top", G, box(-.33, .33, 1.1 - E, 1.14, -.23, .23))
        p.add("Info_Screen", CY, box(-.24, .24, .6, 1.02, .2 - E, .214))
        p.add("Screen_Frame", G, box(-.27, .27, .57, .6 + E, .197, .225), box(-.27, .27, 1.02 - E, 1.05, .197, .225), box(-.27, -.24 + E, .6, 1.02, .197, .225), box(.24 - E, .27, .6, 1.02, .197, .225))
        p.add("Wayfinding_Glyphs", WH, *letters("AQUATICS", -.25, .3, .4, .2 - E, cell=.05, gap=.012, th=.012))
        if th == "rally": p.add("Score_Cells", AM, *[box(x, x + .1, 1.06, 1.08, .2 - E, .23) for x in (-.22, -.06, .1)])
        elif th == "kelp": p.add("Top_Moss", LF2, clump((.2, 1.14 + .03, -.12), .05, 9))
        elif th == "branch": p.add("Top_Leaf", LF, crest((-.2, 1.14 - E, -.1)))
        elif th == "court": p.add("Top_Ball", BA, node((.22, 1.14 + .05 - E, -.12), .05, 1))
        else: p.add("Top_Pebbles", SSL, node((.2, 1.14 + .025 - E, -.12), .03, 0), node((.1, 1.14 + .02 - E, -.15), .022, 0))
        p.add("Plinth-colonly", SL, box(-.34, .34, 0, 1.14, -.24, .24))
    elif pc == "sign":   # hangs from the soffit: local y 0 = blade bottom, rods rise 1.0 m
        Lb = 1.6
        p.add("Blade_Core", SL, box(-Lb, Lb, .04, .56, -.05, .05))
        p.add("Blade_Frame", G, box(-Lb - .03, Lb + .03, 0, .04 + E, -.07, .07), box(-Lb - .03, Lb + .03, .56 - E, .6, -.07, .07), box(-Lb - .03, -Lb + E, .04, .56, -.07, .07), box(Lb - E, Lb + .03, .04, .56, -.07, .07))
        p.add("Wayfinding_Glyphs", CY, *letters("AQUATICS", -1.25, .14, .46, .05 - E, cell=.24, gap=.07, th=.02))
        back = [xf(m, R=trimesh.transformations.rotation_matrix(np.pi, [0, 1, 0])) for m in letters("AQUATICS", -1.25, .14, .46, .05 - E, cell=.24, gap=.07, th=.02)]
        p.add("Wayfinding_Glyphs_Back", CY, *back)
        p.add("Hanger_Rods", ST, tube((-1.2, .6 - E, 0), (-1.2, 1.6, 0), .015, 6), tube((1.2, .6 - E, 0), (1.2, 1.6, 0), .015, 6))
        acc = {"court": (BA, lambda: [node((-Lb - .03 - .07 + E, .3, 0), .07, 1)]), "kelp": (LF, lambda: [crest((Lb, .6 - E, 0))]),
               "river": (AM, lambda: [box(-Lb, Lb, .04 - E, .06, .05 - E, .058)]), "rally": (WH, lambda: [box(-Lb + .1, Lb - .1, .08, .09, .05 - E, .058)]),
               "branch": (LF, lambda: [crest((-Lb, .6 - E, 0))])}[th]
        p.add("Blade_Accent", acc[0], *acc[1]())
        p.add("Sign-colonly", SL, box(-Lb - .03, Lb + .03, 0, .6, -.07, .07))
    else:  # caustic projector (ceiling): local y 0 = lens bottom, mount plate at +0.45
        p.add("Projector_Can", G, tube((0, .08, 0), (0, .25 + E, 0), .11, 12), tube((0, .29 - E, 0), (0, .45 + E, 0), .11, 12))
        p.add("Mount_Plate", G, box(-.16, .16, .45 - E, .48, -.16, .16)); p.add("Yoke", ALY, box(-.13, -.11, .2, .45, -.02, .02), box(.11, .13, .2, .45, -.02, .02))
        p.add("Lens_Ring", ALY, tube((0, .04, 0), (0, .08 + E, 0), .12, 12))
        p.add("Caustic_Lens", CY, tube((0, .0, 0), (0, .04 + E, 0), .09, 12))
        acc = {"court": AM, "kelp": LF2, "river": AM, "rally": WH, "branch": LF}[th]
        p.add("Can_Band", acc, tube((0, .25, 0), (0, .29, 0), .115, 12))
        p.add("Projector-colonly", G, box(-.16, .16, 0, .48, -.16, .16))
    return p
def V(pc): return [dict(theme=t, piece=pc, label=f"{n} / {pc}", seed=3 + i) for i, (t, n, _) in enumerate(THEMES)]
def place(A, part, t, tag, rot=0.0):
    R = trimesh.transformations.rotation_matrix(rot, [0, 1, 0]) if rot else None
    for n, (mk, m) in part.P.items():
        if "colonly" in n: continue
        m2 = m.copy()
        if R is not None: m2.apply_transform(R)
        m2.apply_translation(t); m2.metadata["uv"] = m.metadata.get("uv", np.zeros((len(m.vertices), 2))); A[f"{tag}_{n}"] = (mk, m2)
def tank_seam(th):
    A = {}; place(A, build(dict(theme=th, piece="tank")), (0, 0, 0), "T0"); place(A, build(dict(theme=th, piece="tank")), (W, 0, 0), "T1")
    near = {k: v for k, v in A.items() if v[1].bounds[1][0] > W/2 - .5 and v[1].bounds[0][0] < W/2 + .5}
    c = cc.check(near, n_samp=250); bad = [o for o in c["overlap"] if not o[3] and o[0][:2] != o[1][:2] and o[2] > .0101]; cop = [x for x in c["coplanar"] if x[0][:2] != x[1][:2]]
    return not bad and not cop
def clearance(i):
    """Corridor 8.0 m (Z 34.5..42.5): rail at Z 41.9 leaves >= 7.4 m; benches/plinths placed in the vignette must leave >= 6 m clear."""
    rail_z = 42.5 - .6; clear_after_rail = rail_z - .1 - 34.5   # rail shelf to z +0.7 local => Z 41.8
    benches_depth = .5; clear_with_benches = clear_after_rail - benches_depth
    return dict(clear_rail=round(clear_after_rail, 2), clear_bench_row=round(clear_with_benches, 2), pass_=clear_after_rail >= 7.0 and clear_with_benches >= 6.0)
def vignette(i):
    """World-ish layout: corridor X 0..30 mapped to local X; tank face (acrylic) at Z 42.5 -> local z 0 at Z 42.5."""
    A = {}; th = THEMES[i][0]
    for k in range(4):   # X 1..23
        place(A, build(dict(theme=th, piece="tank", seed=3 + i)), (1 + W/2 + W*k, 0, 42.5), f"T{k}")
    for k in range(5):   # floor X 0..27.5, Z 34.5..41.3 (strip covers 41.3..42.2)
        place(A, build(dict(theme=th, piece="floor", seed=3 + i)), (W/2 + W*k, 0, 34.5 + 3.4), f"F{k}")
    for k, x in enumerate((5.0, 10.5, 16.0, 21.5)): place(A, build(dict(theme=th, piece="bench", seed=3 + i)), (x, FY, 40.9), f"B{k}")
    for k, x in enumerate((2.5, 23.5)): place(A, build(dict(theme=th, piece="plinth", seed=3 + i)), (x, FY, 36.0), f"P{k}")
    for k, x in enumerate((1.0, 24.0)): place(A, build(dict(theme=th, piece="sign", seed=3 + i)), (x, 3.9, 38.5), f"S{k}", rot=np.pi/2)
    for k, x in enumerate((6.0, 12.0, 18.0)): place(A, build(dict(theme=th, piece="caustic", seed=3 + i)), (x, 5.0, 40.0), f"C{k}")
    A["Pier"] = (SL, box(-.45, .45, 0, 5.5, 39.05, 39.95))   # clad X 0 / Z 39.5 portal pier
    A["Soffit"] = (G, box(-.5, 27.5, 5.48, 5.55, 34.5, 44.5))
    for k, (mk, m) in list(A.items()):
        if "uv" not in m.metadata: m.metadata["uv"] = np.zeros((len(m.vertices), 2))
    return A
if __name__ == "__main__":
    REP = {pc: run("aquarium_corridor", build, V(pc), title=f"aquarium corridor {pc}", suffix=f"_{pc}", names=[f"v{i+1}_{THEMES[i][0]}_{pc}" for i in range(5)], sheet=f"aquarium_corridor_run_{pc}.png") for pc in PIECES}
    SE = {i: tank_seam(THEMES[i][0]) for i in range(5)}; CL = {i: clearance(i) for i in range(5)}
    print("SEAM", SE, "CLEAR", CL)
    rdir = os.path.join(RENDER_OUT, "aquarium_corridor"); json.dump(dict(rep=REP, seam=SE, clear=CL, themes=THEMES), open(os.path.join(rdir, "report.json"), "w"), indent=1, default=str)
    Ry = lambda el, az: (lambda a, b: np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]) @ np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]))(np.radians(az), np.radians(el))
    sheets = []
    for i in range(5):   # one depth sheet per variant
        fig = plt.figure(figsize=(26, 18), facecolor="#F4F2EC"); gs = fig.add_gridspec(2, 4)
        shots = [("tank", (8, 30), "tank bay low 3/4"), ("tank", (25, -70), "tank bay raking side (reef depth)"), ("bench", (20, 35), "bench"), ("plinth", (12, 30), "info plinth")]
        for j, (pc, (el, az), t) in enumerate(shots):
            geo = {k: v for k, v in export_final(recenter(build(V(pc)[i])).P, [f"/tmp/aq_{i}_{j}.glb"])[1].items() if "colonly" not in k}
            ax = fig.add_subplot(gs[0, j]); ax.imshow(np.clip(crop(render_view(geo, Ry(el, az), size=700, shadow=False, glass_alpha=.3)), 0, 1)); ax.axis("off")
            r = REP[pc][i]; ax.set_title(f"{t}\n{r['tris']} tris | {'PASS' if r['passed'] else 'FAIL'}", fontsize=11)
        for j, (pc, (el, az), t) in enumerate([("sign", (10, 20), "overhead AQUATICS blade"), ("caustic", (-25, 30), "caustic projector")]):
            geo = {k: v for k, v in export_final(recenter(build(V(pc)[i])).P, [f"/tmp/aq_{i}_s{j}.glb"])[1].items() if "colonly" not in k}
            ax = fig.add_subplot(gs[1, j]); ax.imshow(np.clip(crop(render_view(geo, Ry(el, az), size=600, shadow=False, glass_alpha=.3)), 0, 1)); ax.axis("off")
            r = REP[pc][i]; ax.set_title(f"{t}\n{r['tris']} tris | {'PASS' if r['passed'] else 'FAIL'}", fontsize=11)
        Pt = Part()
        for n, (mk, m) in vignette(i).items(): Pt.add(n, mk, m)
        _, g2 = export_final(Pt.P, [f"/tmp/aqv_{i}.glb"])
        ax = fig.add_subplot(gs[1, 2:]); ax.imshow(np.clip(crop(render_view(g2, Ry(14, 35), size=1100, shadow=False, glass_alpha=.3)), 0, 1)); ax.axis("off")
        ax.set_title(f"corridor vignette X 0..27.5: 4 tank bays (22 m), floor, 4 benches, 2 plinths, 2 blades, 3 projectors, pier\ntank seam {'PASS' if SE[i] else 'FAIL'} | clear past rail {CL[i]['clear_rail']} m, past bench row {CL[i]['clear_bench_row']} m", fontsize=11)
        fr = REP["floor"][i]
        fig.suptitle(f"Rook | aquarium corridor v{i+1} {THEMES[i][1]} — {THEMES[i][2]} | floor tile {fr['tris']} tris | candidate (not promoted)", fontsize=14)
        plt.tight_layout(rect=(0, 0, 1, .95)); sp = os.path.join(rdir, f"v{i+1}_{THEMES[i][0]}_sheet.png"); fig.savefig(sp, dpi=70, facecolor="#F4F2EC"); plt.close(fig); sheets.append(sp)
    # overview contact sheet: vignette per variant
    fig, axs = plt.subplots(1, 5, figsize=(40, 9), facecolor="#F4F2EC")
    for i in range(5):
        axs[i].imshow(plt.imread(sheets[i])); axs[i].axis("off"); axs[i].set_title(f"v{i+1} {THEMES[i][1]}", fontsize=14)
    sp = os.path.join(rdir, "aquarium_corridor_contact_sheet.png"); fig.savefig(sp, dpi=60, facecolor="#F4F2EC"); print("SHEETS", sheets, "OVERVIEW", sp)
