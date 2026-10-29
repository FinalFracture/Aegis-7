#!/usr/bin/env python3
"""Sprocket-first service wall (#25 redirect) - 5 iterations. 3.0 W (X) x 2.0 H x <=0.5 D (floor pad may project),
back on the wall, front +Z, pivot bottom-center. Each has: a small latched human kit (<=0.6 m: hand tools + fuse /
first-aid box), and for Sprocket (~0.78 x 1.03 x 0.77, ports @0.45 m): an auto-reach parts dispenser at Sprocket height,
a charge coupler, a diagnostic port, a tool/battery swap bay, and the floor pad + coupler arm (group-3 items) folded in.
Outputs design/assets/service_wall/."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dining_chair_generator as dc
from dining_chair_generator import xf, torus_ring, FMAT, export_final, render_view
from bath_pod_generator import blk, cyl, Pod, views
from kitchen_counter_generator import bev, box, crop, tonemap
from washer_dryer_generator import zdisc
from tool_wall_generator import plate_rails, tool
import coat_closet_generator as cc
import wardrobe_generator as wg
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(dc.ROOT, "design/assets/service_wall")
W, D, H = 3.0, 0.5, 2.0; ZB = -D / 2; WZ = ZB + .02; ZMAX = ZB + D

def human_kit(p, x, y0=1.3):   # <=0.6 m latched kit: hand tools + fuse/first-aid box
    p.add("Kit_Panel", "slate", bev(.56, .015, y0, y0 + .55, .01, .004, 1, x, WZ + .0375))
    for dx, k in ((-.19, "driver"), (-.11, "wrench"), (-.03, "pliers")): tool(p, k, x + dx, y0 + .5, WZ + .05)
    p.add("Kit_Box", "white", bev(.2, .14, y0 + .1, y0 + .45, .03, .01, 2, x + .16, WZ + .11))
    p.add("Kit_Box_Cross", "green", box(x + .15, x + .17, y0 + .22, y0 + .33, WZ + .18, WZ + .184), box(x + .105, x + .215, y0 + .265, y0 + .285, WZ + .18, WZ + .184))
    p.add("Kit_Box_Latch", "amber", box(x + .2, x + .24, y0 + .4, y0 + .415, WZ + .18, WZ + .186))

def coupler_diag(p, x):   # charge coupler + diagnostic port at 0.45 m
    p.add("Charge_Coupler", "gunmetal", bev(.22, .05, .35, .55, .02, .006, 2, x, WZ + .025))
    p.add("Charge_Port", "amber", box(x - .03, x + .03, .42, .48, WZ + .05, WZ + .055))
    p.add("Diag_Port", "gunmetal", bev(.1, .03, .4, .5, .01, .004, 1, x + .2, WZ + .015))
    p.add("Diag_Port_Light", "green", box(x + .18, x + .22, .44, .46, WZ + .03, WZ + .034))
    p.add("Status_Bar", "green", box(x - .1, x + .1, .62, .632, WZ + .02, WZ + .024))

def pad_arm(p, x, folded=True):   # floor pad (projects) + coupler arm folded flat on the plate
    p.add("Floor_Pad", "gunmetal", bev(.9, .8, 0, .015, .06, .006, 3, x, WZ + .4))
    p.add("Floor_Pad_Ring", "amber", xf(torus_ring(.22, .006, 20, 3), t=(x, .016, WZ + .42)))
    p.add("Pad_Clamps", "gunmetal", *[box(xx - .03, xx + .03, 0, .03, WZ + .74, WZ + .78) for xx in (x - .38, x + .38)])
    p.add("Coupler_Arm_Base", "gunmetal", bev(.12, .05, .9, 1.02, .02, .006, 2, x - .3, WZ + .025))
    p.add("Coupler_Arm", "alloy", box(x - .3, x + .25, .94, .98, WZ + .05, WZ + .08))     # stowed flat, latched
    p.add("Coupler_Arm_Head", "white", bev(.1, .05, .92, 1.0, .015, .006, 2, x + .28, WZ + .075))
    p.add("Coupler_Arm_Latch", "amber", box(x + .1, x + .14, .985, 1.0, WZ + .07, WZ + .08))

def swap_bay(p, x, n=4, y0=.15, w=.5):   # latched battery / tool-head swap slots
    p.add("Swap_Bay", "gunmetal", bev(w, .3, y0, y0 + .6, .02, .008, 2, x, WZ + .15))
    for i in range(n):
        xx = x - w / 2 + w / n * (i + .5)
        p.add("Swap_Packs", "white", bev(w / n - .03, .26, y0 + .05, y0 + .45, .015, .006, 2, xx, WZ + .15))
        p.add("Swap_Latches", "amber" if i % 2 else "green", box(xx - .02, xx + .02, y0 + .5, y0 + .52, WZ + .3, WZ + .306))

def iter1():  # rotary carousel
    p = Pod("Rotary Carousel"); plate_rails(p, (1.15, 1.95))
    cx = -.55
    p.add("Carousel_Housing", "white", bev(.7, .46, .1, 1.05, .1, .02, 3, cx, WZ + .23))
    p.add("Carousel_Drum", "gunmetal", cyl(cx, WZ + .24, .2, .15, 1.0, 18))
    for y in (.3, .5, .7, .9): p.add("Carousel_Bins", "white", xf(torus_ring(.21, .02, 18, 4), t=(cx, y, WZ + .24)))
    p.add("Carousel_Window", "slate", bev(.36, .01, .2, .95, .02, .004, 1, cx, WZ + .465))
    p.add("Carousel_Gate", "amber", box(cx - .12, cx + .12, .44, .46, WZ + .468, WZ + .474))
    human_kit(p, -1.15); coupler_diag(p, .35); pad_arm(p, .35); swap_bay(p, 1.15)
    return p

def iter2():  # vertical lift dispenser
    p = Pod("Vertical Lift Dispenser"); plate_rails(p, (1.15, 1.95))
    cx = -.55
    p.add("Lift_Column", "alloy", *[bev(.04, .3, .1, 1.95, .01, .004, 1, cx + s * .24, WZ + .15) for s in (-1, 1)])
    p.add("Lift_Back", "slate", box(cx - .22, cx + .22, .1, 1.95, WZ, WZ + .01))
    for y in np.arange(.75, 1.85, .2): p.add("Lift_Bins", "white", bev(.42, .26, y, y + .16, .02, .008, 2, cx, WZ + .15))
    p.add("Lift_Carriage", "gunmetal", bev(.46, .3, .4, .5, .02, .008, 2, cx, WZ + .15))
    p.add("Lift_Delivery_Tray", "alloy", box(cx - .2, cx + .2, .5, .52, WZ + .02, WZ + .3), box(cx - .2, cx + .2, .52, .56, WZ + .28, WZ + .3))
    p.add("Lift_Gates", "amber", *[box(cx - .2, cx + .2, y + .075, y + .085, WZ + .28, WZ + .29) for y in np.arange(.75, 1.85, .2)])
    human_kit(p, -1.15); coupler_diag(p, .35); pad_arm(p, .35); swap_bay(p, 1.15)
    return p

def iter3():  # linear rail shuttle at Sprocket height
    p = Pod("Linear Rail Shuttle"); plate_rails(p, (1.15, 1.95))
    p.add("Shuttle_Rail", "alloy", blk(-1.45, 1.45, .72, .76, WZ, WZ + .05, .01, 1), blk(-1.45, 1.45, .98, 1.02, WZ, WZ + .05, .01, 1))
    for x in np.linspace(-1.3, -.3, 6):
        p.add("Shuttle_Bins", "white", bev(.14, .2, .78, .96, .02, .008, 2, x, WZ + .15))
        p.add("Shuttle_Bin_Latches", "amber", box(x - .02, x + .02, .92, .935, WZ + .25, WZ + .256))
    p.add("Shuttle_Carriage", "gunmetal", bev(.2, .26, .66, 1.06, .02, .008, 2, .05, WZ + .15))
    p.add("Shuttle_Light", "violet", box(-.03, .13, 1.0, 1.01, WZ + .28, WZ + .284))
    p.add("Shuttle_Drop_Tray", "alloy", box(-.05, .15, .55, .57, WZ + .05, WZ + .3))
    human_kit(p, -1.1, 1.3); coupler_diag(p, .55); pad_arm(p, .55); swap_bay(p, 1.25, 3, .1, .4)
    return p

def iter4():  # drawer-matrix auto-feed
    p = Pod("Drawer-Matrix Auto-Feed"); plate_rails(p, (1.15, 1.95))
    cx, nx, ny = -.55, 5, 5; w, h = .7, .8
    p.add("Matrix_Frame", "white", bev(w + .04, .4, .12, .12 + h + .04, .02, .008, 2, cx, WZ + .2))
    for i in range(nx):
        for j in range(ny):
            x = cx - w / 2 + w / nx * (i + .5); y = .14 + h / ny * (j + .5)
            p.add("Matrix_Drawers", "gunmetal", box(x - w / nx / 2 + .006, x + w / nx / 2 - .006, y - h / ny / 2 + .006, y + h / ny / 2 - .006, WZ + .4, WZ + .41))
            p.add("Matrix_Latches", "amber" if (i + j) % 3 else "green", box(x - .012, x + .012, y - .006, y + .006, WZ + .41, WZ + .414))
    p.add("Feed_Chute", "alloy", box(cx + w / 2 + .03, cx + w / 2 + .1, .3, .6, WZ + .2, WZ + .4))
    p.add("Feed_Tray", "alloy", box(cx + w / 2 + .03, cx + w / 2 + .2, .44, .46, WZ + .2, WZ + .42))
    human_kit(p, -1.15, 1.3); coupler_diag(p, .45); pad_arm(p, .45); swap_bay(p, 1.2, 3, .15, .45)
    return p

def iter5():  # compact alcove pod: everything inside one moulded Sprocket alcove (+ kit beside)
    p = Pod("Compact Alcove Pod"); plate_rails(p, (1.15, 1.95))
    cx, aw = .2, 1.1
    p.add("Alcove_Shell", "white", bev(.06, D - .02, 0, 1.4, .02, .008, 2, cx - aw / 2, WZ + (D - .02) / 2),
          bev(.06, D - .02, 0, 1.4, .02, .008, 2, cx + aw / 2, WZ + (D - .02) / 2), bev(aw + .06, D - .02, 1.32, 1.42, .03, .01, 3, cx, WZ + (D - .02) / 2))
    p.add("Alcove_Edge", "violet", box(cx - aw / 2 - .03, cx + aw / 2 + .03, 1.32, 1.33, ZMAX - .03, ZMAX - .026))
    for s in (-1, 1):   # side-wall dispensers (rotary cartridges) at Sprocket height, gated
        x = cx + s * (aw / 2 - .06)
        p.add("Side_Dispensers", "gunmetal", bev(.06, .3, .55, 1.15, .015, .006, 2, x, WZ + .2))
        p.add("Side_Dispenser_Gates", "amber", *[box(x - .03, x + .03, y, y + .012, WZ + .35, WZ + .356) for y in (.65, .85, 1.05)])
    p.add("Alcove_Swap_Shelf", "gunmetal", bev(aw - .2, .3, 1.15, 1.18, .01, .004, 1, cx, WZ + .15))
    p.add("Swap_Packs", "white", *[bev(.18, .24, 1.18, 1.3, .015, .006, 2, x, WZ + .15) for x in (cx - .3, cx - .1, cx + .1, cx + .3)])
    p.add("Swap_Latches", "green", *[box(x - .02, x + .02, 1.27, 1.285, WZ + .27, WZ + .276) for x in (cx - .3, cx - .1, cx + .1, cx + .3)])
    coupler_diag(p, cx - .1); pad_arm(p, cx, True)
    human_kit(p, -1.05, 1.0)
    p.add("Spare_Bins", "white", *[bev(.5, .3, y, y + .18, .03, .01, 2, 1.15, WZ + .15) for y in (.3, .55, .8)])
    p.add("Spare_Bin_Latches", "amber", *[box(1.33, 1.37, y + .14, y + .155, WZ + .3, WZ + .306) for y in (.3, .55, .8)])
    return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}")
        print(i, p.name, tris, lo, hi, "non-watertight:", bad)
        if i == 5:   # render-only: Sprocket docked
            _, geo = export_final(p.P, [os.path.join(OUT, "iter_05.glb")]); g = dict(geo); sg, _ = cc.sprocket_geo(.2); g.update(sg)
            saved = tonemap(); R = views()[3]; im = render_view(g, R, size=760, shadow=True); ns = render_view(g, R, size=760, shadow=False)
            fg = np.abs(ns - ns[0, 0]).sum(2) > .03; im[fg] = np.clip(im[fg] * 1.12 + .02, 0, 1); FMAT.update(saved); iso = crop(im)
        isos.append((p.name + (" (Sprocket docked, render only)" if i == 5 else ""), iso))
    fig, axs = plt.subplots(3, 2, figsize=(16, 14), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", fontsize=12, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .97)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=80, facecolor="#F4F2EC"); plt.close(fig)

if __name__ == "__main__":
    main()
