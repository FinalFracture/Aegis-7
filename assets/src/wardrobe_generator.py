#!/usr/bin/env python3
"""Wardrobe (#21) - 5 iterations. Owner: Rook. 0.5 D (Z) x 2.7 W (X) x 2.1 H, front +Z, back -Z on the wall, Y up,
pivot bottom-center. Modular: end panels 0.15 m (or 0.05 m slim) + bays of 0.6 / 0.9 m:
  2.7 = 0.15+0.9+0.6+0.9+0.15 (default) | 2.5 = 0.05+0.9+0.6+0.9+0.05 | 3.0 = 0.15+0.9+0.9+0.9+0.15.
Reuses loft / glb writer / soft rasterizer + emissive tone-map + white exposure lift. Outputs design/assets/wardrobe/."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dining_chair_generator as dc
from dining_chair_generator import loft, rrect, xf, export_final, render_view, FMAT
from bath_pod_generator import blk, cyl, Pod, views
from kitchen_counter_generator import bev, box, crop, tonemap
from trimesh.visual.material import PBRMaterial as _PBR
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(dc.ROOT, "design/assets/wardrobe")
FMAT.update({
 "white": _PBR(name="WhiteComposite", baseColorFactor=(0.92, 0.93, 0.94, 1), metallicFactor=0.0, roughnessFactor=0.35),
 "warmgrey": _PBR(name="FabricWarmGrey", baseColorFactor=(0.55, 0.52, 0.49, 1), metallicFactor=0.0, roughnessFactor=0.9),
 "slatefab": _PBR(name="FabricSlate", baseColorFactor=(0.30, 0.33, 0.38, 1), metallicFactor=0.0, roughnessFactor=0.9),
 "green": _PBR(name="StatusGreen", baseColorFactor=(0.247, 0.686, 0.416, 1), metallicFactor=0.0, roughnessFactor=0.4, emissiveFactor=(0.247, 0.686, 0.416)),
 "lamp": _PBR(name="NicheLight", baseColorFactor=(1, .95, .85, 1), metallicFactor=0, roughnessFactor=.4, emissiveFactor=(1, .92, .78)),
})
W, D, H = 2.7, 0.5, 2.1; ZB, ZF = -D / 2, D / 2; EP = 0.15
BAYS = [0.9, 0.6, 0.9]

def bays():
    x = -W / 2 + EP; out = []
    for i, w in enumerate(BAYS): out.append((i, x + w / 2, w)); x += w
    return out

def roty(m, deg, pivot):
    R = trimesh.transformations.rotation_matrix(np.radians(deg), [0, 1, 0], pivot); return xf(m, R)

def garments(p, cx, w, y1, z=0.0, n=5, mat="warmgrey"):   # hanging garment masses + bar + retaining top bar
    p.add("Garment_Bar", "alloy", blk(cx - w / 2 + .03, cx + w / 2 - .03, y1 - .03, y1, z - .012, z + .012, .01, 1))
    p.add("Garment_RetainBar", "gunmetal", blk(cx - w / 2 + .03, cx + w / 2 - .03, y1 + .04, y1 + .055, z - .02, z + .02, .006, 1))
    for k, xx in enumerate(np.linspace(cx - w / 2 + .12, cx + w / 2 - .12, n)):
        hh = .9 if k % 2 else 1.1
        p.add("Garments", mat if k % 2 else "slatefab", bev(.07, .4, y1 - .05 - hh, y1 - .04, .03, .01, 2, xx, z))

def shelves(p, cx, w, ys, mat="white", z0=ZB + .02, z1=ZF - .03):
    p.add("Shelves", mat, *[box(cx - w / 2 + .02, cx + w / 2 - .02, y, y + .02, z0, z1) for y in ys])

def hollow(p, name, x0, x1, y0, y1, z0, z1, t=.025, mat="white", divs=(), back="slatefab"):
    """Open-front carcass: bevelled top/sides + bottom, back panel (fabric-lined) and bay dividers."""
    w, d = x1 - x0, z1 - z0; cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    p.add(name, mat, bev(w, d, y1 - t, y1, .03, .01, 2, cx, cz), bev(t, d, y0, y1 - t, .01, .006, 1, x0 + t / 2, cz),
          bev(t, d, y0, y1 - t, .01, .006, 1, x1 - t / 2, cz), box(x0 + t, x1 - t, y0, y0 + t, z0, z1),
          *[box(x - t / 2, x + t / 2, y0 + t, y1 - t, z0, z1 - .02) for x in divs])
    p.add("Back_Lining", back, box(x0 + t, x1 - t, y0 + t, y1 - t, z0, z0 + .012))

def latch(p, x, y, z, mat="amber"): p.add("Latch_Lights", mat, box(x - .025, x + .025, y - .006, y + .006, z, z + .01))

def iter1():  # flush moulded slab, latched sliding doors
    p = Pod("Moulded Slab + Sliding Doors")
    p.add("Base", "gunmetal", box(-W / 2 + .06, W / 2 - .06, 0, .08, ZB + .02, ZF - .06))
    hollow(p, "Carcass", -W / 2, W / 2, .08, H, ZB, ZF - .04, divs=[-W / 2 + EP] + [cx + w / 2 for i, cx, w in bays()])
    p.add("Accent_Band", "violet", box(-W / 2 + .05, W / 2 - .05, H - .07, H - .06, ZF - .043, ZF - .039))
    p.add("Door_Track", "alloy", box(-W / 2 + .02, W / 2 - .02, H - .05, H - .03, ZF - .06, ZF))
    for i, cx, w in bays():
        shelves(p, cx, w, (.3, 1.75))
        if w > .8: garments(p, cx, w, 1.68, 0)
    xs = [(-W / 2 + .02, -.33), (-.36, .36), (.33, W / 2 - .02)]
    for k, (a, b) in enumerate(xs):
        off = .55 if k == 0 else 0; z = ZF - (.035 if k == 1 else .015)   # left door slid over the middle
        p.add(f"Door_Slide_{k + 1}", "white", bev(b - a, .02, .1, H - .06, .01, .006, 1, (a + b) / 2 + off, z))
        p.add("Handles", "alloy", box(b + off - .06, b + off - .045, .9, 1.3, z + .01, z + .025))
        latch(p, b + off - .052, 1.36, z + .01)
    return p

def iter2():  # alloy rail system, open bays, elastic straps
    p = Pod("Alloy Rail + Open Bays")
    p.add("Anchor_Backplate", "gunmetal", box(-W / 2, W / 2, .1, H, ZB, ZB + .02))
    xs = [-W / 2 + .02] + [cx + w / 2 for i, cx, w in bays()][:-1] + [W / 2 - .02]
    xs = [-W / 2 + EP] + [cx + w / 2 for i, cx, w in bays()]
    for x in [-W / 2 + .02, W / 2 - .02] + xs:
        p.add("Uprights", "alloy", box(x - .015, x + .015, 0, H, ZB + .02, ZF - .02))
        p.add("Anchor_Feet", "gunmetal", box(x - .04, x + .04, 0, .012, ZB, ZF))
        p.add("Anchor_Bolts", "alloy", *[box(x - .012, x + .012, y - .012, y + .012, ZB + .02, ZB + .03) for y in (.5, 1.9)])
    for s in (-1, 1): shelves(p, s * (W / 2 - EP / 2), EP - .03, np.linspace(.2, 1.9, 6), "gunmetal")
    for i, cx, w in bays():
        if w > .8:
            garments(p, cx, w, 1.75, 0, 5, "warmgrey"); shelves(p, cx, w, (1.85,), "gunmetal")
            p.add("Restraint_Straps", "slatefab", *[box(cx - w / 2 + .02, cx + w / 2 - .02, y, y + .04, ZF - .03, ZF - .02) for y in (.55, 1.15)])
        else:
            ys = np.linspace(.15, 1.85, 6); shelves(p, cx, w, ys, "gunmetal")
            p.add("Restraint_Straps", "slatefab", *[box(cx - w / 2 + .02, cx + w / 2 - .02, y + .12, y + .15, ZF - .03, ZF - .02) for y in ys[:-1]])
            for y in ys[:-1]: latch(p, cx + w / 2 - .05, y + .135, ZF - .02)
    return p

def iter3():  # wall-pod cabinets on rails
    p = Pod("Wall Pods on Rails"); WZ = ZB + .025
    p.add("Anchor_Strongback", "gunmetal", box(-W / 2, W / 2, .12, H, ZB, WZ))
    p.add("Wall_Rail", "alloy", *[blk(-W / 2 + .02, W / 2 - .02, y, y + .045, WZ, WZ + .03, .012, 1) for y in (.45, 1.95)])
    for x in [-W / 2 + EP] + [cx + w / 2 for i, cx, w in bays()][:-1] + [W / 2 - EP]:
        p.add("Anchor_Cleats", "gunmetal", box(x - .012, x + .012, .15, H - .02, WZ, ZF - .05))
        p.add("Anchor_Bolts", "alloy", *[box(x - .014, x + .014, y - .014, y + .014, WZ, WZ + .012) for y in (.3, 1.8)])
    for i, cx, w in bays():
        if i == 1: hollow(p, "Pod_2", cx - (w - .05) / 2, cx + (w - .05) / 2, .2, H - .02, WZ + .005, WZ + D - .075)
        else: p.add(f"Pod_{i + 1}", "white", bev(w - .05, D - .08, .2, H - .02, .06, .02, 2, cx, WZ + (D - .08) / 2 + .005))
        for y in (.42, 1.92): p.add("Hook_Clamps", "gunmetal", box(cx - .05, cx + .05, y, y + .1, WZ + .03, WZ + .07))
        zf = WZ + D - .075
        if i == 1:   # middle door swung open 70 deg to show shelves + garment netting
            door = bev(w - .07, .02, .24, H - .06, .01, .006, 1, cx, zf + .01)
            p.add("Door_2", "white", roty(door, -70, [cx - (w - .07) / 2, 0, zf]))
            shelves(p, cx, w - .08, (.5, .9, 1.3, 1.7), "gunmetal", WZ + .03, zf - .02)
        else:
            p.add(f"Door_{i + 1}", "white", bev(w - .07, .02, .24, H - .06, .01, .006, 1, cx, zf + .01))
            p.add("Handles", "alloy", box(cx + w / 2 - .1, cx + w / 2 - .08, .9, 1.3, zf + .02, zf + .04)); latch(p, cx + w / 2 - .09, 1.36, zf + .02)
    for s in (-1, 1): p.add("EndCap", "white", bev(EP - .03, D - .08, .2, H - .02, .03, .012, 2, s * (W / 2 - EP / 2), WZ + (D - .08) / 2))
    p.add("Accent_Band", "violet", box(-W / 2 + .03, W / 2 - .03, .19, .2, WZ, ZF - .06))
    return p

def iter4():  # tambour roll doors
    p = Pod("Tambour Roll-Door Unit")
    p.add("Base", "gunmetal", box(-W / 2 + .06, W / 2 - .06, 0, .08, ZB + .02, ZF - .06))
    hollow(p, "Carcass", -W / 2, W / 2, .08, H, ZB, ZF - .04, divs=[-W / 2 + EP] + [cx + w / 2 for i, cx, w in bays()])
    p.add("Header_Box", "white", bev(W, .12, H - .2, H, .03, .01, 2, 0, ZF - .06))
    for i, cx, w in bays():
        top = [1.0, 1.95, .55][i]          # each tambour rolled to a different height
        n = int((top - .12) / .06)
        p.add(f"Tambour_{i + 1}", "alloy" if i != 1 else "gunmetal", *[box(cx - w / 2 + .03, cx + w / 2 - .03, .12 + k * .06, .12 + k * .06 + .055, ZF - .035, ZF - .02) for k in range(n)])
        hy = .12 + n * .06
        p.add("Tambour_Pulls", "gunmetal", box(cx - .15, cx + .15, hy - .03, hy - .01, ZF - .02, ZF - .005)); latch(p, cx + .2, hy - .02, ZF - .02)
        if w > .8: garments(p, cx, w, 1.75, -.05)
        else: shelves(p, cx, w, (.5, 1.0, 1.5), "white", ZB + .03, ZF - .06)
    for x in [-W / 2 + EP] + [cx + w / 2 for i, cx, w in bays()]:
        p.add("Tambour_Tracks", "gunmetal", box(x - .015, x + .015, .1, H - .2, ZF - .045, ZF - .01))
    p.add("Accent_Band", "violet", box(-W / 2 + .05, W / 2 - .05, H - .12, H - .11, ZF + .0, ZF + .004))
    return p

def iter5():  # mixed: drawers + hanging bay + lit display niche + Sprocket laundry chute
    p = Pod("Mixed: Drawers + Hanging + Niche")
    p.add("Base", "gunmetal", box(-W / 2 + .08, W / 2 - .08, 0, .08, ZB + .02, ZF - .07))
    for sx in (-1, 1):
        x = sx * (W / 2 - .1)
        p.add("FloorPlates", "gunmetal", box(x - .1, x + .1, 0, .012, -.12, .12)); p.add("Clamps", "gunmetal", box(x - .05, x + .05, .012, .08, -.05, .05))
        p.add("Clamp_Lights", "amber", box(x + sx * .05, x + sx * .055, .03, .05, -.02, .02))
    hollow(p, "Carcass", -W / 2, W / 2, .08, H, ZB, ZF - .04, divs=[-W / 2 + EP] + [cx + w / 2 for i, cx, w in bays()])
    b = bays(); zf = ZF - .04
    _, cx, w = b[0]   # left 0.9: latched drawer stack + doors above
    for k, y in enumerate((.1, .4, .7)):
        p.add(f"Drawer_{k + 1}", "white", bev(w - .02, .02, y + .01, y + .29, .01, .006, 1, cx, zf + .01))
        p.add("Handles", "alloy", box(cx - .2, cx + .2, y + .23, y + .245, zf + .02, zf + .035)); latch(p, cx + .3, y + .238, zf + .02)
    p.add("Door_Upper_L", "white", bev(w - .02, .02, 1.01, H - .02, .01, .006, 1, cx, zf + .01)); latch(p, cx + .38, 1.5, zf + .02)
    _, cx, w = b[1]   # middle 0.6: lit display niche + Sprocket laundry chute hatch
    p.add("Niche_Light", "lamp", box(cx - w / 2 + .05, cx + w / 2 - .05, 1.59, 1.6, ZB + .05, zf - .05))
    p.add("Niche_Shelf", "gunmetal", box(cx - w / 2 + .02, cx + w / 2 - .02, 1.1, 1.12, ZB + .03, zf))
    p.add("Niche_Lip", "alloy", box(cx - w / 2 + .02, cx + w / 2 - .02, 1.12, 1.15, zf - .015, zf))
    p.add("Door_Upper_M", "white", bev(w - .02, .02, 1.62, H - .02, .01, .006, 1, cx, zf + .01))
    p.add("Door_Lower_M", "white", bev(w - .02, .02, .1, 1.08, .01, .006, 1, cx, zf + .01))
    p.add("Laundry_Chute", "gunmetal", blk(cx - .18, cx + .18, .3, .6, zf + .02, zf + .03, .03, 2))
    p.add("Service_Port", "amber", box(cx - .03, cx + .03, .42, .48, zf + .03, zf + .04))
    _, cx, w = b[2]   # right 0.9: hanging bay, door swung open
    garments(p, cx, w, 1.75, -.02); shelves(p, cx, w, (1.85,))
    hx = cx + w / 2 - .01
    p.add("Door_Hang_R", "white", roty(bev(w - .02, .02, .1, H - .02, .01, .006, 1, cx, zf + .01), 75, [hx, 0, zf]))
    for s in (-1, 1): shelves(p, s * (W / 2 - EP / 2), EP - .04, (.6, 1.2, 1.8), "white")
    p.add("Accent_Band", "violet", box(-W / 2 + .05, W / 2 - .05, .09, .1, ZF - .044, ZF - .04))
    return p

def sheet(p, path, title):
    tris, geo = export_final(p.P, [path.replace("_sheet.png", ".glb")])
    saved = tonemap(); top, front, side, iso = views()
    def rv(R, s, sh):
        im = render_view(geo, R, size=s, shadow=sh); ns = render_view(geo, R, size=s, shadow=False) if sh else im
        fg = np.abs(ns - ns[0, 0]).sum(2) > .03; im[fg] = np.clip(im[fg] * 1.12 + .02, 0, 1); return crop(im)
    ims = [rv(top, 700, False), rv(front, 700, True), rv(side, 600, True), rv(iso, 760, True)]; FMAT.update(saved)
    bg = "#F4F2EC"; fig = plt.figure(figsize=(14, 10), facecolor=bg); gs = fig.add_gridspec(2, 3, width_ratios=[1, 1, .45], height_ratios=[.5, 1])
    for ax, im, t in ((fig.add_subplot(gs[0, :2]), ims[0], "Top"), (fig.add_subplot(gs[:, 2]), ims[2], "Side"),
                      (fig.add_subplot(gs[1, 0]), ims[1], "Front"), (fig.add_subplot(gs[1, 1]), ims[3], "Iso")):
        ax.imshow(im); ax.axis("off"); ax.set_title(t, y=-0.08, fontsize=11, color="#555")
    fig.suptitle(title, fontsize=12, color="#444"); plt.tight_layout(); fig.savefig(path, dpi=100, facecolor=bg); plt.close(fig)
    V = np.vstack([g[1] for g in geo.values()])
    bad = [n for n, (mk, m) in p.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    return tris, ims[3], V.min(0).round(3), V.max(0).round(3), bad

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); tris, iso, lo, hi, bad = sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}")
        isos.append((p.name, iso)); print(i, p.name, tris, lo, hi, "non-watertight:", bad)
    fig, axs = plt.subplots(2, 3, figsize=(18, 10), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", y=-0.1, fontsize=11, color="#555")
    plt.tight_layout(); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)

if __name__ == "__main__":
    main()
