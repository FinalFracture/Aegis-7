"""Rook: Tennis Tower restroom extras in the #58 V2 Leaf Crest style (spec §3.10, §3.11.7 grid 0.9 m).
basin      : 3.6 m wall-hung lavatory run, 4 basins (bath_pod_generator.sink recipe), leaf-green splash, mirror band, leaf-crest end fins.
accessible : 1.8 x 1.6 m accessible WC stall, 1 per block. Same wet-wall line and 2.4 m half-unit depth as tt_restroom.glb, so it
             tiles at the end of a row (row end x +-3.6 -> accessible centre x +-4.5). WC 0.45 m off the side wall, grab bars, corner basin,
             0.95 m clear out-swing door (leaf-green), leaf crests on the partitions.
Run: python3 restroom_extras.py"""
from modlib import *
import bath_pod_generator as bp
from restroom import wc, Z0, ZW
bp.FL = 0.0
def crest(c): return xf(leaf_dir((0, 0, 0), (0, 1, 0), .35, .25, t=.0125), R=trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]), t=c)  # leaf crest, blade in the partition plane

def basin(p):   # §3.11.7: vanities at 0.75 m centres, 0.6 m deep counter, 1.0 m mirror band
    W, D, N = 3.0, .6, 4; x0 = -W/2
    p.add("Wet_Wall", WH, box(x0, -x0, 0, 2.4, -.1, 0))
    p.add("Splash_Panel", LF, box(x0 + .05, -x0 - .05, .86 + .002, 1.0, -E, .008))
    p.add("Mirror", "mirror", box(x0 + .05, -x0 - .05, 1.05, 2.05, -E, .01))
    p.add("Counter", WH, box(x0 + .0425 - E, -x0 - .0425 + E, .82, .86, -E, D))
    for k in range(N):
        cx = x0 + .375 + k*.75
        p.add("Basin_Bowl", SSL, xf(loft(circle(1, 16), [(0.858, .2, .15), (0.864, .19, .14)]), t=(cx, 0, .3)))
        p.add("Taps", ALY, box(cx - .015, cx + .015, .86 - E, .98, .05, .08), box(cx - .015, cx + .015, .95, .98, .08 - E, .16))
    p.add("Counter_Brackets", SGM, *[box(x - .04, x + .04, .3, .82 + E, -E, D - .06) for x in (-.75, 0, .75)])
    for x in (x0 + .03, -x0 - .03):
        p.add("End_Fins", WH, box(x - .0125, x + .0125, .15, 1.95, -E, D + .1))
        p.add("Leaf_Crests", LF, crest((x, 1.95 - .003, (D + .1)/2)))
    p.add("Dryer_Lamps", GRN, *[box(x - .05, x + .05, 2.1, 2.14, -E, .03) for x in (-.75, .75)])

def urinal(p):  # §3.11.7: urinals at 0.75 m centres with 0.45 m privacy screens (V2 Leaf Crest: leaf-green screens, leaf crests)
    W, N = 3.0, 4; x0 = -W/2
    p.add("Wet_Wall", WH, box(x0, -x0, 0, 2.4, -.1, 0))
    p.add("Splash_Panel", SSL, box(x0 + .05, -x0 - .05, .2, 1.3, -E, .008))
    for k in range(N):
        cx = x0 + .375 + k*.75
        body = loft(rrect(.36, .32, .1, 3), [(.35, .8, .8), (.42, 1, 1), (.85, 1, 1), (.95, .9, .85)])
        p.add("Urinal", WH, xf(body, t=(cx, 0, .008 - E + .16)))
        p.add("Urinal_Bowl", SSL, box(cx - .12, cx + .12, .45, .78, .008 - E + .32 - .004, .008 - E + .32 + .004))
        p.add("Flush_Sensor", GRN, box(cx - .03, cx + .03, 1.12, 1.16, .008 - E, .02))
    for k in range(1, N):
        x = x0 + k*.75
        p.add("Privacy_Screens", LF, box(x - .0125, x + .0125, .3, 1.5, .008 - E, .45))
        p.add("Leaf_Crests", LF2, crest((x, 1.5 - .003, .23)))

def accessible(p):
    W, X0 = 1.8, -.9; ZFa = ZW + 1.6; xs = (X0 + .03, -X0 - .03)
    p.add("Wet_Wall", WH, box(X0 + .001, -X0 - .001, 0, 2.4, Z0, ZW)); p.add("Aisle_Centre_Strip", SSL, box(X0 + .001, -X0 - .001, 0, .003, -.03, -.001))
    p.add("Partitions", WH, *[box(x - .0125, x + .0125, .15, 1.95, ZW - E, ZFa - .02 + E) for x in xs])
    p.add("Leaf_Crests", LF, *[crest((x, 1.95 - .003, (ZW + ZFa)/2)) for x in xs])
    p.add("Pilasters", SGM, box(X0 + .001, X0 + .15, 0, 1.95, ZFa - .02, ZFa + .02), box(-X0 - .65, -X0 - .001, 0, 1.95, ZFa - .02, ZFa + .02))
    a, b = X0 + .155, -X0 - .655                        # 0.99 m leaf, 0.95 m clear
    p.add("Stall_Door", LF, box(a, b, .15, 1.95, ZFa - .012, ZFa + .008))
    p.add("Door_Pulls", ALY, box(b - .08, b - .05, .95, 1.1, ZFa + .008 - E, ZFa + .03), box(b - .08, b - .05, .95, 1.1, ZFa - .034, ZFa - .012 + E))
    wcx = -X0 - .45 - .03                                # WC centre 0.45 m from the +X partition face
    wc(p, wcx, ZW - E)
    gx = -X0 - .03 - .0125                               # side grab bar on the +X partition (1.07 m, y .85)
    p.add("Grab_Bars", ALY, tube((gx - .05, .85, ZW + .3), (gx - .05, .85, ZW + 1.37), .018, 6),
          *[box(gx - .05, gx + E, .84, .86, z - .01, z + .01) for z in (ZW + .35, ZW + 1.32)],
          tube((wcx - .45, 1.05, ZW + .06), (wcx + .38, 1.05, ZW + .06), .018, 6), *[box(x - .01, x + .01, 1.04, 1.06, ZW - E, ZW + .06) for x in (wcx - .4, wcx + .34)])
    cx = X0 + .35                                       # corner basin on the wet wall, knee clear (bath_pod sink recipe, 0.5 m)
    p.add("Basin", WH, box(cx - .25, cx + .25, .78, .82, ZW - E, ZW + .42))
    p.add("Basin_Bowl", SSL, xf(loft(circle(1, 16), [(0.818, .18, .13), (0.824, .17, .12)]), t=(cx, 0, ZW + .22)))
    p.add("Taps", ALY, box(cx - .015, cx + .015, .82 - E, .94, ZW + .02, ZW + .05), box(cx - .015, cx + .015, .91, .94, ZW + .05 - E, ZW + .13))
    p.add("Mirror", "mirror", box(cx - .22, cx + .22, 1.0, 1.7, ZW - E, ZW + .01))
    p.add("Access_Sign", CY, cap((0, 1.6, ZFa + .008 + .004 - E), .09, .008, 16, axis="z"))

def build(q): p = Part(); {"basin": basin, "accessible": accessible, "urinal": urinal}[q["kind"]](p); return p
VAR = [dict(kind="basin", label="Vanity unit: 3.0 m, 4 basins @0.75, 0.6 deep, 1.0 m mirror band"), dict(kind="accessible", label="Accessible stall: 1.8 x 1.6 m, grab bars, 0.95 m door"), dict(kind="urinal", label="Urinal unit: 3.0 m, 4 urinals @0.75, 0.45 m leaf screens")]
if __name__ == "__main__": run("restroom", build, VAR, names=["basin", "accessible", "urinal"], suffix="_extras", sheet="restroom_extras_sheet.png", title="V2 Leaf Crest extras")
