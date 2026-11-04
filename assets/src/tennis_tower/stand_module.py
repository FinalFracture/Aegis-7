"""Rook: Tennis Tower stand bay (spec §3.2, §3.11.4 Rev 2.5): instanced 7.5 m aisle bay = 0.6 m half-aisle + 12 seats + 0.6 m half-aisle
(tiles to 1.2 m radial aisles every 7.5 m). cfg F12: 5 rows, riser 0.40, tread 0.85. cfg F3: 12 rows, riser 0.45, tread 0.95.
Front (concourse edge) faces +Z, tiers rise toward -Z. Run: python3 stand_module.py  (writes v1..v5 and v1_f3..v5_f3)"""
from modlib import *
W, HA, NS = 7.5, .6, 12
CFG = {"F12": (5, .40, .85), "F3": (12, .45, .95)}

def build(q):
    n, R, T = CFG[q.get("cfg", "F12")]; p = Part(); x0, x1 = -W/2, W/2; sp = (W - 2*HA) / NS
    p.add("Tier_Concrete", SL, *[box(x0 + .001, x1 - .001, 0, R*(i+1), -T*(i+1), -T*i + (E if i else 0)) for i in range(n)])
    p.add("Aisle_Steps", G, *[box(*sorted((s*(W/2 - .01), s*(W/2 - HA + .02))), R*(i+1) - E, R*(i+1) + R/2, -T*(i+1) + T/2, -T*i - .01) for i in range(n - 1) for s in (-1, 1)])
    seats, backs, peds = [], [], []
    for i in range(n):
        y, zc = R*(i+1), -T*i - T*.45
        peds.append(box(x0 + HA + .1, x1 - HA - .1, y - E, y + .4, zc - .05, zc + .05))  # continuous seat beam per row
        for k in range(NS):
            cx = x0 + HA + sp*(k + .5)
            seats.append(box(cx - .22, cx + .22, y + .4 - E, y + .45, zc - .2, zc + .22))
            if q["back"] == "leaf": backs.append(leaf_dir((cx, y + .45 - E, zc - .17), (0, 1, -.15), .55, .4, t=.03))
            elif q["back"] == "solid": backs.append(box(cx - .21, cx + .21, y + .45 - E, y + .85, zc - .204, zc - .164))
    p.add("Seat_Beams", G, *peds); p.add("Seat_Pans", q.get("seat_mat", ST), *seats)
    if backs: p.add("Seat_Backs", LF if q["back"] == "leaf" else q.get("seat_mat", ST), *backs)
    if q.get("planters"):  # aisle-edge planters at each row, inboard of the aisle
        for i in range(0, n, 1 if n <= 5 else 2):
            for s in (-1, 1):
                xa, xb = sorted((s*(W/2 - HA - .02), s*(W/2 - HA - .32)))
                tr, so, sy = planter(xa, xb, R*(i+1) - E, -T*(i+1) + .03, -T*(i+1) + .22, h=.3)
                p.add("Planter_Trough", G, tr); p.add("Planter_Soil", SO, so); p.add("Foliage", LF2, shrubs(xa + .02, xb - .02, sy, -T*(i+1) + .125, r=.12, n=1, seed=i*3+s+1))
    if q.get("screen"):  # green rear screen with vines on the back edge
        yt = R*n; zb = -T*n
        p.add("Screen_Frame", G, box(x0 + .02, x1 - .02, 0, yt + 2.8, zb - .12, zb + E))
        p.add("Screen_Green", LF, green_wall(x0 + .1, x1 - .1, yt + .95, yt + 2.75, zb + E, r=.25 if n <= 5 else .34, seed=5))
    if q.get("sports"):  # front ball-guard glass rail, tennis-ball post caps, amber row LEDs on risers
        xs = np.linspace(x0 + HA + .1, x1 - HA - .1, 4)
        p.add("Guard_Glass", GL, *[box(a + .03 - E, b - .03 + E, R + .1, R + .9, -.095, -.085) for a, b in zip(xs[:-1], xs[1:])])
        for xp in xs:
            p.add("Rail_Posts", ST, box(xp - .03, xp + .03, R - E, R + 1.0, -.12, -.06)); p.add("Ball_Caps", BA, node((xp, R + 1.0 + .06 - E, -.09), .065, 0 if q.get("lite") else 1))
        p.add("Row_LED", AM, *[box(x0 + HA + .05, x0 + HA + .45, R*i + .1, R*i + .2, -T*i + E - E, -T*i + E + .008) for i in range(1, n)])
    if q.get("canopy"):  # rear branch-canopy posts with leaf shade (tree column language)
        yt = R*n; zb = -T*n + .1
        for xp in (x0 + 1.2, x1 - 1.2):
            top = np.array([xp, yt + 2.8, zb]); p.add("Canopy_Steel", ST, tube((xp, yt - E, zb), top, .08, 8), node(top, .12, 0 if q.get("lite") else 1),
                *[tube(top, top + d, .05, 6) for d in ([.6, .6, 1.4], [-.6, .6, 1.4])])
            p.add("Canopy_Leaves", LF, *[leaf_dir(top + np.array([dx, .62, 1.45]) + [0, .02, 0], (0, .15, 1), 1.4, .6, t=.03) for dx in (.6, -.6)])
    return p

VARIANTS = [
    dict(label="Planter Aisle: shrub troughs edge every aisle", back="solid", planters=True),
    dict(label="Leaf Backs: green leaf-blade seat backs", back="leaf"),
    dict(label="Green Screen: rear moss wall over the top row", back="solid", screen=True, seat_mat=SL),
    dict(label="Court Rail: glass ball-guard, ball caps, amber row LEDs", back="solid", sports=True),
    dict(label="Branch Canopy: rear Y-posts with leaf shades", back="none", canopy=True),
]
HYBRID = dict(label="Court Rail + Branch Canopy: V4 rail/ball caps/LEDs + V5 Y-posts, leaf shades", back="solid", sports=True, canopy=True, lite=True)
if __name__ == "__main__" and sys.argv[1:] == ["hybrid"]:
    run("stand_module", build, [HYBRID, dict(HYBRID, cfg="F3")], title="V6 hybrid: F1/F2 5-row | F3 12-row", names=["v6_hybrid", "v6_hybrid_f3"], sheet="hybrid_sheet.png", suffix="_hybrid")
elif __name__ == "__main__":
    run("stand_module", build, VARIANTS, title="7.5 m bay, 12 seats x 5 rows (F1/F2) | nature + sports")
    run("stand_module", build, [dict(v, cfg="F3") for v in VARIANTS], title="F3 case: 12 rows, riser 0.45, tread 0.95", suffix="_f3")
