#!/usr/bin/env python3
"""Tool wall panel (#25, pegboard + cable variant) - 5 iterations. 3 needed (101, 201, Maintenance).
Default 3.0 W (X) x 0.5 D (Z, max incl. shelves) x 2.0 H, back on the wall, front +Z, pivot bottom-center.
Modular 0.6 m panels: 2.4 / 3.0 / 3.6 -> spec range 2.5-3.5 via 0.05 end trims. Family language: bolted gunmetal
wall plate, alloy rails + hook clamps, amber latches, violet/green accents, Sprocket at 0.45 m. Tools are simple
low-poly silhouettes, every one latched. Outputs design/assets/tool_wall/."""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dining_chair_generator as dc
from dining_chair_generator import xf, torus_ring, FMAT
from bath_pod_generator import blk, cyl, Pod
from kitchen_counter_generator import bev, box
from washer_dryer_generator import zdisc, zring
import wardrobe_generator as wg
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(dc.ROOT, "design/assets/tool_wall")
W, D, H = 3.0, 0.5, 2.0; ZB = -D / 2; WZ = ZB + .02; PW = .6
XS = [-W / 2 + PW * (k + .5) for k in range(5)]

def plate_rails(p, rails=(.3, 1.95)):
    p.add("Wall_Plate", "gunmetal", bev(W, .02, .1, H, .006, .004, 1, 0, ZB + .01))
    p.add("Wall_Rail", "alloy", *[blk(-W / 2 + .02, W / 2 - .02, y, y + .04, WZ, WZ + .03, .01, 1) for y in rails])
    p.add("Accent_Strip", "violet", box(-W / 2 + .05, W / 2 - .05, rails[-1] + .045, rails[-1] + .055, WZ + .02, WZ + .024))
    for x in [-W / 2 + PW * k for k in range(6)]:
        x = min(max(x, -W / 2 + .04), W / 2 - .04)
        p.add("Hook_Clamps", "gunmetal", *[box(x - .04, x + .04, y - .02, y + .06, WZ + .03, WZ + .06) for y in rails])
        p.add("Plate_Bolts", "alloy", *[box(x - .012, x + .012, y - .012, y + .012, WZ, WZ + .01) for y in (.6, 1.7)])

def tool(p, kind, x, y, z):   # latched silhouette hanging on the face at depth z (tool top at y)
    if kind == "wrench":
        p.add("Tools", "alloy", box(x - .012, x + .012, y - .3, y - .04, z, z + .012), box(x - .03, x + .03, y - .05, y, z, z + .012), box(x - .025, x + .025, y - .33, y - .29, z, z + .012))
    elif kind == "driver":
        p.add("Tools", "gunmetal", cyl(x, z + .015, .016, y - .13, y, 8)); p.add("Tools", "alloy", cyl(x, z + .015, .005, y - .32, y - .13, 6))
    elif kind == "hammer":
        p.add("Tools", "gunmetal", box(x - .07, x + .07, y - .05, y, z, z + .03)); p.add("Tools", "alloy", box(x - .013, x + .013, y - .34, y - .05, z + .005, z + .025))
    elif kind == "pliers":
        p.add("Tools", "alloy", box(x - .03, x - .01, y - .22, y, z, z + .012), box(x + .01, x + .03, y - .22, y, z, z + .012), box(x - .02, x + .02, y - .03, y, z, z + .015))
    p.add("Tool_Latches", "amber", box(x - .03, x + .03, y - .16, y - .14, z + .03, z + .04))   # spring gate over every tool
    p.add("Tool_Latch_Pins", "gunmetal", box(x - .036, x - .03, y - .17, y - .13, z, z + .04), box(x + .03, x + .036, y - .17, y - .13, z, z + .04))

def shelf(p, x0, x1, y, d=.3, lip=True):
    p.add("Shelves", "gunmetal", bev(x1 - x0, d, y, y + .02, .006, .004, 1, (x0 + x1) / 2, WZ + d / 2))
    if lip: p.add("Shelf_Lips", "alloy", box(x0, x1, y + .02, y + .06, WZ + d - .012, WZ + d))
    p.add("Shelf_Brackets", "gunmetal", *[box(x - .01, x + .01, y - .12, y, WZ, WZ + d - .02) for x in (x0 + .05, x1 - .05)])

def iter1():  # pegboard panels (slate inset, alloy peg grid) + latched tool silhouettes
    p = Pod("Pegboard Panels"); plate_rails(p)
    for k, x in enumerate(XS):
        p.add(f"Pegboard_{k + 1}", "slate", bev(PW - .03, .015, .4, 1.85, .01, .004, 1, x, WZ + .0375))
        p.add("Peg_Grid", "alloy", *[box(x - PW / 2 + .03, x + PW / 2 - .03, y, y + .006, WZ + .045, WZ + .05) for y in np.arange(.5, 1.85, .15)])
    for x, k in zip(XS, ("wrench", "driver", "hammer", "pliers", "wrench")):
        tool(p, k, x - .12, 1.7, WZ + .05); tool(p, "driver", x + .12, 1.7, WZ + .05)
    shelf(p, -W / 2 + .05, W / 2 - .05, .9, .22)
    return p

def iter2():  # cable variant: vertical trays, latched spools, cable gates
    p = Pod("Cable Management Wall"); plate_rails(p)
    for k, x in enumerate(XS):
        p.add("Cable_Trays", "alloy", box(x - .2, x - .18, .35, 1.9, WZ + .03, WZ + .12), box(x + .18, x + .2, .35, 1.9, WZ + .03, WZ + .12))
        p.add("Cable_Tray_Backs", "slate", box(x - .2, x + .2, .35, 1.9, WZ + .03, WZ + .04))
        for y in (.7, 1.1, 1.5):
            p.add("Cable_Gates", "amber", box(x - .18, x + .18, y, y + .02, WZ + .11, WZ + .12))
        y = 1.65 if k % 2 else 1.25
        p.add("Cable_Spools", "gunmetal", zdisc(x, y, WZ + .05, WZ + .16, .14, 16)); p.add("Cable_Spools", "slatefab", zdisc(x, y, WZ + .06, WZ + .15, .15, 16))
        p.add("Spool_Latches", "amber", box(x - .02, x + .02, y - .02, y + .02, WZ + .16, WZ + .17))
    p.add("Junction_Box", "gunmetal", bev(.4, .12, .4, .6, .02, .008, 2, 0, WZ + .06 + .04))
    p.add("Junction_Status", "green", box(-.05, .05, .58, .59, WZ + .16, WZ + .164))
    return p

def iter3():  # rail-hung latched tool cassettes, one open
    p = Pod("Rail Tool Cassettes"); plate_rails(p, (.3, 1.2, 1.95))
    for k, x in enumerate(XS):
        for j, (y0, y1) in enumerate(((.5, 1.15), (1.25, 1.9))):
            p.add(f"Cassette_{k + 1}{'LU'[j]}", "white", bev(PW - .05, .2, y0, y1, .04, .015, 3, x, WZ + .13))
            if (k, j) == (2, 1):
                p.add("Cassette_Open_Inner", "slate", box(x - .25, x + .25, y0 + .03, y1 - .03, WZ + .228, WZ + .232))
                tool(p, "wrench", x - .12, y1 - .05, WZ + .232); tool(p, "pliers", x + .12, y1 - .05, WZ + .232)
                p.add("Cassette_Lid_Open", "white", xf(bev(PW - .06, .02, y1, y1 + .4, .02, .008, 2, x, WZ + .25), t=(0, 0, 0)))
            else:
                p.add("Cassette_Latches", "amber", box(x + .18, x + .24, y1 - .06, y1 - .045, WZ + .23, WZ + .238))
                p.add("Cassette_Pulls", "alloy", box(x - .1, x + .1, y1 - .06, y1 - .048, WZ + .23, WZ + .24))
    p.add("Accent_Band", "violet", box(-W / 2 + .05, W / 2 - .05, .48, .49, WZ + .2, WZ + .23))
    return p

def iter4():  # magnetic strip wall + lipped shelf
    p = Pod("Magnetic Strip Wall"); plate_rails(p)
    for y in (1.75, 1.4, 1.05):
        p.add("Mag_Strips", "gunmetal", bev(W - .2, .02, y, y + .05, .01, .004, 1, 0, WZ + .04))
        p.add("Mag_Strip_Lights", "violet", box(-W / 2 + .12, W / 2 - .12, y + .02, y + .028, WZ + .05, WZ + .052))
    for x, k in zip(np.linspace(-1.3, 1.3, 10), ("wrench", "driver", "hammer", "pliers", "driver") * 2):
        tool(p, k, x, 1.79, WZ + .05)
    p.add("Mag_Status", "green", box(1.32, 1.4, 1.83, 1.845, WZ + .05, WZ + .054))
    shelf(p, -W / 2 + .05, W / 2 - .05, .7, .3)
    p.add("Bins", "white", *[bev(.5, .26, .72, .9, .03, .01, 2, x, WZ + .15) for x in XS])
    p.add("Bin_Latches", "amber", *[box(x - .03, x + .03, .85, .865, WZ + .28, WZ + .286) for x in XS])
    return p

def iter5():  # Sprocket service wall: tool panel + dock coupler at 0.45 + fold-down shelf + latched drawers
    p = Pod("Sprocket Service Wall"); plate_rails(p, (1.2, 1.95))
    for x in XS[:3]:
        p.add("Pegboard", "slate", bev(PW - .03, .015, 1.25, 1.9, .01, .004, 1, x, WZ + .0375))
        tool(p, "wrench", x - .12, 1.85, WZ + .05); tool(p, "driver", x + .12, 1.85, WZ + .05)
    for j, x in enumerate(XS[:3]):
        p.add("Drawer_Cabinet", "gunmetal", bev(PW - .02, .4, .1, .8, .02, .008, 2, x, WZ + .2))
        for i, y in enumerate((.12, .35, .58)):
            p.add(f"Drawer_{j + 1}_{i + 1}", "white", bev(PW - .06, .02, y, y + .2, .012, .005, 2, x, WZ + .41))
            p.add("Drawer_Latches", "amber", box(x + .18, x + .24, y + .16, y + .175, WZ + .42, WZ + .428))
    p.add("Worktop", "slate", bev(3 * PW, .45, .8, .84, .02, .006, 2, XS[1], WZ + .225))
    p.add("Worktop_Lip", "alloy", box(XS[0] - PW / 2, XS[2] + PW / 2, .84, .87, WZ + .44, WZ + .45))
    dx = (XS[3] + XS[4]) / 2   # 1.2 m Sprocket service bay
    p.add("Sprocket_Floor_Pad", "gunmetal", bev(1.0, .46, 0, .015, .05, .006, 3, dx, WZ + .23))
    p.add("Sprocket_Pad_Ring", "amber", xf(torus_ring(.2, .006, 20, 3), t=(dx, .016, WZ + .23)))
    p.add("Sprocket_Coupler", "gunmetal", bev(.24, .05, .35, .55, .02, .006, 2, dx, WZ + .025))
    p.add("Sprocket_Port", "amber", box(dx - .03, dx + .03, .42, .48, WZ + .05, WZ + .055))
    p.add("Sprocket_Status", "green", box(dx - .06, dx + .06, .6, .612, WZ + .02, WZ + .024))
    p.add("Fold_Shelf", "gunmetal", bev(1.0, .02, .9, 1.15, .015, .006, 2, dx, WZ + .01))       # folded-up service shelf
    p.add("Fold_Shelf_Latch", "amber", box(dx - .03, dx + .03, 1.12, 1.135, WZ + .02, WZ + .026))
    for x in (XS[3], XS[4]): tool(p, "pliers", x, 1.85, WZ + .05); tool(p, "hammer", x + .15, 1.85, WZ + .05)
    return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}")
        isos.append((p.name, iso)); print(i, p.name, tris, lo, hi, "non-watertight:", bad)
    fig, axs = plt.subplots(3, 2, figsize=(16, 13), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=12, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=80, facecolor="#F4F2EC"); plt.close(fig)

if __name__ == "__main__":
    main()
