#!/usr/bin/env python3
"""Sofa (#15) - 5 iterations. Owner: Rook. ~2.5 W (X) x 0.9 D (Z) x 0.85 H, seat ~0.43 m, front +Z, back -Z, Y up,
pivot bottom-center. Reuses loft / glb writer / soft rasterizer, emissive tone-map, white exposure lift and the bed's
smooth cushion loft. Outputs design/assets/sofa/."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dining_chair_generator as dc
from dining_chair_generator import xf, export_final, render_view, FMAT
from bath_pod_generator import blk, cyl, Pod, views
from kitchen_counter_generator import bev, box, crop, tonemap
from double_bed_generator import soft
from trimesh.visual.material import PBRMaterial as _PBR
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(dc.ROOT, "design/assets/sofa")
FMAT.update({   # fabric albedo lifted vs bed so upholstery doesn't read too dark
 "white": _PBR(name="WhiteComposite", baseColorFactor=(0.92, 0.93, 0.94, 1), metallicFactor=0.0, roughnessFactor=0.35),
 "slatefab": _PBR(name="FabricSlate", baseColorFactor=(0.42, 0.46, 0.52, 1), metallicFactor=0.0, roughnessFactor=0.9),
 "warmgrey": _PBR(name="FabricWarmGrey", baseColorFactor=(0.64, 0.61, 0.57, 1), metallicFactor=0.0, roughnessFactor=0.9),
 "linen": _PBR(name="FabricOffWhite", baseColorFactor=(0.86, 0.84, 0.80, 1), metallicFactor=0.0, roughnessFactor=0.9),
})
W, D, H = 2.5, 0.9, 0.85; ZB, ZF = -D / 2, D / 2; SEAT = .43

def roty(m, deg, pivot=(0, 0, 0)):
    return xf(m, trimesh.transformations.rotation_matrix(np.radians(deg), [0, 1, 0], pivot))

def tilt(m, deg, pivot):   # recline back cushions about X
    return xf(m, trimesh.transformations.rotation_matrix(np.radians(deg), [1, 0, 0], pivot))

def cushions(p, x0, x1, n, y0, y1, z0, z1, mat, by1=H - .03, bz=None, bt=.16, name="Seat"):
    w = (x1 - x0) / n; bz = bz if bz is not None else z0
    for i in range(n):
        cx = x0 + w * (i + .5)
        p.add(f"{name}_Cushion_{i + 1}", mat, soft(w - .015, z1 - z0, y0, y1, .06, cx, (z0 + z1) / 2))
        p.add(f"Back_Cushion_{i + 1}", mat, tilt(soft(w - .015, bt, y1 - .02, by1, .06, cx, bz + bt / 2), -8, [cx, y1, bz + bt / 2]))

def clips(p, xs, y, z, mat="amber"):   # cushion retention tabs (gunmetal tab + amber lock)
    for x in xs:
        p.add("Cushion_Clips", "gunmetal", box(x - .025, x + .025, y - .03, y, z, z + .012))
        p.add("Clip_Lights", mat, box(x - .012, x + .012, y - .02, y - .012, z + .012, z + .016))

def floor_clamps(p, xs, zs, top=.08):
    for x in xs:
        for z in zs:
            p.add("FloorPlates", "gunmetal", box(x - .09, x + .09, 0, .012, z - .07, z + .07))
            p.add("Clamps", "gunmetal", box(x - .045, x + .045, .012, top, z - .04, z + .04))
            p.add("Clamp_Bolts", "alloy", *[box(x + d - .01, x + d + .01, .012, .02, z - .05, z - .03) for d in (-.065, .065)])
            p.add("Clamp_Lights", "amber", box(x - .02, x + .02, .03, .05, z + .04, z + .045))

def iter1():  # moulded white shell, slate cushions, recessed base + tucked clamps
    p = Pod("Moulded Shell + Slate Cushions")
    p.add("Base", "gunmetal", box(-W / 2 + .12, W / 2 - .12, 0, .1, ZB + .1, ZF - .12))
    p.add("Shell_Deck", "white", bev(W - .3, D - .05, .1, SEAT - .14, .05, .02, 2, 0, .0))
    p.add("Shell_Back", "white", bev(W, .16, .1, H, .07, .025, 2, 0, ZB + .08))
    for s in (-1, 1): p.add("Shell_Arms", "white", bev(.15, D, .1, .62, .07, .025, 2, s * (W / 2 - .075), 0))
    p.add("Accent_Band", "violet", box(-W / 2 + .2, W / 2 - .2, .2, .21, ZF - .025, ZF - .021))
    cushions(p, -W / 2 + .15, W / 2 - .15, 3, SEAT - .14, SEAT, ZB + .16, ZF - .03, "slatefab", bz=ZB + .16)
    clips(p, [-.8, 0, .8], SEAT - .14, ZF - .025)
    floor_clamps(p, (-W / 2 + .3, W / 2 - .3), (ZB + .2, ZF - .25))
    return p

def iter2():  # alloy frame modular, clip-in cushion cassettes
    p = Pod("Alloy Frame + Cushion Cassettes")
    xs = (-W / 2 + .04, -.4, .4, W / 2 - .04)
    for x in xs:
        for z in (ZB + .06, ZF - .06):
            p.add("Frame_Legs", "alloy", cyl(x, z, .022, 0, .2, 10))
            p.add("Anchor_Feet", "gunmetal", box(x - .05, x + .05, 0, .012, z - .05, z + .05))
        p.add("Frame_Back_Posts", "alloy", blk(x - .02, x + .02, .2, H - .05, ZB + .02, ZB + .06, .008, 1))
    p.add("Frame_Rails", "alloy", blk(-W / 2, W / 2, .17, .21, ZB + .02, ZB + .1, .01, 1), blk(-W / 2, W / 2, .17, .21, ZF - .1, ZF - .02, .01, 1),
          blk(-W / 2, W / 2, H - .07, H - .03, ZB + .02, ZB + .06, .01, 1))
    for s in (-1, 1): p.add("Arm_Rails", "alloy", blk(s * (W / 2 - .04) - .03, s * (W / 2 - .04) + .03, .58, .62, ZB + .02, ZF - .02, .01, 1),
                            cyl(s * (W / 2 - .04), ZF - .06, .02, .2, .58, 10))
    for i, cx in enumerate((-.81, 0, .81)):
        p.add(f"Cassette_Tray_{i + 1}", "gunmetal", box(cx - .39, cx + .39, .21, .27, ZB + .08, ZF - .03))
    cushions(p, -W / 2 + .08, W / 2 - .08, 3, .27, SEAT, ZB + .1, ZF - .03, "warmgrey", bz=ZB + .07)
    clips(p, [-1.0, -.62, -.19, .19, .62, 1.0], .27, ZF - .03)
    return p

def iter3():  # wall-rail-hung floating sofa + Sprocket charge port
    p = Pod("Wall-Rail Floating Sofa"); WZ = ZB + .02
    p.add("Wall_Plate", "gunmetal", box(-W / 2 - .05, W / 2 + .05, .1, H, ZB, WZ))
    p.add("Wall_Rail", "alloy", *[blk(-W / 2, W / 2, y, y + .04, WZ, WZ + .03, .01, 1) for y in (.2, .78)])
    for x in (-1.0, -.33, .33, 1.0):
        p.add("Brackets", "gunmetal", box(x - .012, x + .012, .12, .3, WZ, ZF - .12))
        p.add("Bracket_Bolts", "alloy", *[box(x - .012, x + .012, y - .012, y + .012, WZ, WZ + .01) for y in (.4, .9)])
        p.add("Hook_Clamps", "gunmetal", box(x - .05, x + .05, .76, .84, WZ + .03, WZ + .06))
    p.add("Seat_Pod", "white", bev(W, D - .05, .16, SEAT - .13, .08, .025, 2, 0, WZ + (D - .05) / 2))
    p.add("Back_Pod", "white", bev(W, .1, SEAT - .13, H - .05, .05, .02, 2, 0, WZ + .08))
    p.add("Accent_Band", "violet", box(-W / 2 + .1, W / 2 - .1, .165, .175, ZF - .05, ZF - .046))
    cushions(p, -W / 2 + .04, W / 2 - .04, 3, SEAT - .13, SEAT, WZ + .13, ZF - .02, "linen", bz=WZ + .13, by1=H)
    p.add("Charge_Port", "gunmetal", blk(-.15, .15, .2, .27, ZF - .051, ZF - .04, .02, 1))
    p.add("Service_Port", "amber", box(-.03, .03, .22, .25, ZF - .041, ZF - .036))
    return p

def iter4():  # low lounge, deep seat, storage plinth, strapped back bolsters
    p = Pod("Low Lounge + Storage Plinth"); S = .4
    p.add("Plinth", "gunmetal", bev(W, D, 0, .22, .03, .01, 2))
    for i, cx in enumerate((-.83, 0, .83)):
        p.add(f"Drawer_{i + 1}", "white", blk(cx - .38, cx + .38, .03, .19, ZF - .012, ZF + .006, .01, 1))
        p.add("Drawer_Handles", "alloy", box(cx - .15, cx + .15, .15, .162, ZF + .006, ZF + .018))
        p.add("Drawer_Latches", "amber", box(cx + .25, cx + .3, .15, .162, ZF + .006, ZF + .014))
    p.add("Seat_Cushion", "warmgrey", soft(W - .04, D - .2, .22, S, .07, 0, .09))
    for i, cx in enumerate((-.83, 0, .83)):
        p.add(f"Back_Bolster_{i + 1}", "slatefab", soft(.8, .2, .22, .78, .09, cx, ZB + .1))
        p.add("Restraint_Straps", "slatefab", box(cx - .03, cx + .03, .6, .79, ZB + .2, ZB + .21))
        p.add("Buckle_Latches", "amber", box(cx - .02, cx + .02, .66, .69, ZB + .21, ZB + .216))
    for s in (-1, 1): p.add("Arm_Bolsters", "slatefab", soft(.16, D - .25, .4, .58, .07, s * (W / 2 - .1), .05))
    return p

def iter5():  # curved conversation sofa (arc within 2.5 x 0.9)
    p = Pod("Curved Conversation Sofa"); R, n = 2.8, 4; zc = ZB + R + .02
    ang = np.degrees(np.arcsin((W / 2 - .1) / R)); A = np.linspace(-ang, ang, n + 1)
    def seg(m, a): return roty(m, -a, [0, 0, zc])
    for i in range(n):
        a = (A[i] + A[i + 1]) / 2; segw = 2 * R * np.sin(np.radians((A[1] - A[0]) / 2)) + .01
        p.add("Shell_Base", "white", seg(bev(segw, .6, .1, SEAT - .14, .03, .015, 2, 0, ZB + .35), a))
        p.add("Shell_Back", "white", seg(bev(segw, .12, .1, H, .03, .015, 2, 0, ZB + .08), a))
        p.add(f"Seat_Cushion_{i + 1}", "linen", seg(soft(segw - .02, .5, SEAT - .14, SEAT, .06, 0, ZB + .39), a))
        p.add(f"Back_Cushion_{i + 1}", "slatefab", seg(tilt(soft(segw - .02, .14, SEAT - .02, H - .03, .06, 0, ZB + .21), -8, [0, SEAT, ZB + .21]), a))
        p.add("Cushion_Clips", "gunmetal", seg(box(-.025, .025, SEAT - .17, SEAT - .14, ZB + .645, ZB + .657), a))
        p.add("Clip_Lights", "amber", seg(box(-.012, .012, SEAT - .16, SEAT - .152, ZB + .657, ZB + .661), a))
    p.add("Base", "gunmetal", seg(box(-.9, .9, 0, .1, ZB + .15, ZB + .5), 0))
    p.add("Accent_Band", "violet", seg(box(-.9, .9, .3, .31, ZB + .14, ZB + .144), 0))
    floor_clamps(p, (-.75, .75), (ZB + .3,))
    return p

def sheet(p, path, title):
    tris, geo = export_final(p.P, [path.replace("_sheet.png", ".glb")])
    saved = tonemap(); top, front, side, iso = views()
    def rv(R, s, sh):
        im = render_view(geo, R, size=s, shadow=sh); ns = render_view(geo, R, size=s, shadow=False) if sh else im
        fg = np.abs(ns - ns[0, 0]).sum(2) > .03; im[fg] = np.clip(im[fg] * 1.12 + .02, 0, 1); return crop(im)
    ims = [rv(top, 700, False), rv(front, 700, True), rv(side, 500, True), rv(iso, 760, True)]; FMAT.update(saved)
    bg = "#F4F2EC"; fig = plt.figure(figsize=(14, 9), facecolor=bg); gs = fig.add_gridspec(2, 3, width_ratios=[1, 1, .5])
    for ax, im, t in ((fig.add_subplot(gs[0, :2]), ims[0], "Top"), (fig.add_subplot(gs[0, 2]), ims[2], "Side"),
                      (fig.add_subplot(gs[1, 0]), ims[1], "Front"), (fig.add_subplot(gs[1, 1:]), ims[3], "Iso")):
        ax.imshow(im); ax.axis("off"); ax.set_title(t, y=-0.1, fontsize=11, color="#555")
    fig.suptitle(title, fontsize=12, color="#444"); plt.tight_layout(); fig.savefig(path, dpi=100, facecolor=bg); plt.close(fig)
    V = np.vstack([g[1] for g in geo.values()])
    bad = [n for n, (mk, m) in p.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    return tris, ims[3], V.min(0).round(3), V.max(0).round(3), bad

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); tris, iso, lo, hi, bad = sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}")
        isos.append((p.name, iso)); print(i, p.name, tris, lo, hi, "non-watertight:", bad)
    fig, axs = plt.subplots(2, 3, figsize=(18, 9), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n}", y=-0.12, fontsize=11, color="#555")
    plt.tight_layout(); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)

if __name__ == "__main__":
    main()
