#!/usr/bin/env python3
"""Double bed (#19) - 5 iterations. Owner: Rook. ~1.6 W (X) x 2.0 L (Z) x 0.6 H, foot at +Z, headboard at -Z, Y up,
pivot bottom-center. Reuses loft / glb writer / soft rasterizer (dining_chair -> bath_pod -> kitchen_counter helpers),
incl. emissive tone-mapping + object-only exposure lift so whites read white. Outputs design/assets/double_bed/."""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dining_chair_generator as dc
from dining_chair_generator import loft, rrect, circle, torus_ring, xf, export_final, render_view, FMAT
from bath_pod_generator import blk, cyl, Pod, views
from kitchen_counter_generator import bev, box, crop, tonemap
from trimesh.visual.material import PBRMaterial as _PBR
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(dc.ROOT, "design/assets/double_bed")
FMAT.update({
 "white": _PBR(name="WhiteComposite", baseColorFactor=(0.92, 0.93, 0.94, 1), metallicFactor=0.0, roughnessFactor=0.35),
 "linen": _PBR(name="FabricOffWhite", baseColorFactor=(0.86, 0.84, 0.80, 1), metallicFactor=0.0, roughnessFactor=0.9),
 "warmgrey": _PBR(name="FabricWarmGrey", baseColorFactor=(0.55, 0.52, 0.49, 1), metallicFactor=0.0, roughnessFactor=0.9),
 "slatefab": _PBR(name="FabricSlate", baseColorFactor=(0.30, 0.33, 0.38, 1), metallicFactor=0.0, roughnessFactor=0.9),
 "green": _PBR(name="StatusGreen", baseColorFactor=(0.247, 0.686, 0.416, 1), metallicFactor=0.0, roughnessFactor=0.4, emissiveFactor=(0.247, 0.686, 0.416)),
})
W, LZ = 1.6, 2.0; ZH, ZF = -LZ / 2, LZ / 2

def soft(w, d, y0, y1, r, cx=0, cz=0, n=3, k=3):
    """Cushion: rounded plan + quarter-round top/bottom edge profile (smooth-shaded loft)."""
    e = min((y1 - y0) / 2, r) * 0.9; rings = []
    for a in np.linspace(-np.pi / 2, 0, k + 1):
        s = 1 - e * (1 - np.cos(a)); rings.append((y0 + e * (1 + np.sin(a)), 1 - 2 * e * (1 - np.cos(a)) / w, 1 - 2 * e * (1 - np.cos(a)) / d))
    for a in np.linspace(0, np.pi / 2, k + 1)[1:]:
        rings.append((y1 - e * (1 - np.sin(a)), 1 - 2 * e * (1 - np.cos(a)) / w, 1 - 2 * e * (1 - np.cos(a)) / d))
    rings = [rings[0]] + [r_ for i, r_ in enumerate(rings[1:], 1) if r_[0] > rings[i - 1][0] + 1e-5]
    return xf(loft(rrect(w, d, min(r, w / 2.1, d / 2.1), n), rings), t=(cx, 0, cz))

def bedding(p, y, mw=1.5, ml=1.95, mz=0.0, th=.2, duvet="warmgrey", pil="linen", mat="linen", duvet_from=-.35):
    p.add("Mattress", mat, soft(mw, ml, y, y + th, .06, 0, mz))
    dl = ml / 2 + mz - duvet_from
    p.add("Duvet", duvet, soft(mw + .04, dl, y + th - .03, y + th + .05, .05, 0, duvet_from + dl / 2 + .02))
    for s, nm in ((-1, "Pillow_L"), (1, "Pillow_R")):
        p.add(nm, pil, soft(.62, .38, y + th - .01, y + th + .11, .06, s * .37, mz - ml / 2 + .27))

def latch(p, x, y, z, mat="amber", w=.05): p.add("Latch_Lights", mat, box(x - w / 2, x + w / 2, y - .006, y + .006, z, z + .01))

def iter1():  # moulded white platform + side drawers
    p = Pod("Moulded Platform + Drawers")
    p.add("Plinth", "gunmetal", box(-W / 2 + .08, W / 2 - .08, 0, .06, ZH + .08, ZF - .08))
    p.add("Frame", "white", bev(W, LZ, .06, .34, .08, .02, 2))
    p.add("Accent_Band", "violet", box(-W / 2 + .1, W / 2 - .1, .2, .21, ZF, ZF + .004))
    for s in (-1, 1):
        for j, zc in enumerate((-.25, .45)):
            x0 = s * W / 2
            p.add(f"Drawer_{'LR'[s > 0]}{j + 1}", "white", blk(min(x0, x0 + s * .02), max(x0, x0 + s * .02), .09, .3, zc - .32, zc + .32, .01, 1))
            p.add("Handles", "alloy", box(min(x0 + s * .02, x0 + s * .035), max(x0 + s * .02, x0 + s * .035), .255, .27, zc - .15, zc + .15))
            p.add("Latch_Lights", "amber", box(min(x0 + s * .02, x0 + s * .03), max(x0 + s * .02, x0 + s * .03), .275, .287, zc + .2, zc + .25))
    p.add("Headboard", "white", bev(W, .1, .06, .8, .05, .02, 2, 0, ZH - .05 + .0))
    bedding(p, .34, mz=.05)
    return p

def iter2():  # folded alloy frame + strap restraint
    p = Pod("Alloy Frame + Strap Restraint")
    for x in (-W / 2 + .03, W / 2 - .03):
        p.add("Frame", "alloy", blk(x - .03, x + .03, .22, .3, ZH, ZF, .01, 1))
        for z in (ZH + .05, ZF - .05):
            p.add("Frame", "alloy", cyl(x, z, .025, .02, .3, 10))
            p.add(f"Anchor_Feet", "gunmetal", blk(x - .06, x + .06, 0, .02, z - .06, z + .06, .01, 1))
            p.add("Anchor_Bolts", "alloy", *[box(x + dx - .01, x + dx + .01, .02, .03, z + dz - .01, z + dz + .01) for dx, dz in ((-.04, -.04), (.04, .04))])
    p.add("Frame", "alloy", blk(-W / 2, W / 2, .22, .3, ZF - .06, ZF, .01, 1))
    p.add("Slats", "gunmetal", *[box(-W / 2 + .06, W / 2 - .06, .26, .28, z - .03, z + .03) for z in np.linspace(ZH + .15, ZF - .15, 9)])
    p.add("Headboard", "slatefab", soft(W - .02, .1, .3, 1.0, .04, 0, ZH + .05))
    p.add("Headboard", "alloy", blk(-W / 2, W / 2, .96, 1.0, ZH, ZH + .1, .01, 1))
    bedding(p, .28, mw=1.48, duvet="slatefab")
    for z in (-.1, .55):   # cross straps over the duvet with clip buckles to the side rails
        p.add("Restraint_Straps", "gunmetal", box(-W / 2 + .02, W / 2 - .02, .55, .565, z - .03, z + .03),
              box(-W / 2 + .01, -W / 2 + .03, .3, .56, z - .03, z + .03), box(W / 2 - .03, W / 2 - .01, .3, .56, z - .03, z + .03))
        for s in (-1, 1): latch(p, s * (W / 2 - .02) - .0, .4, z + .03, "amber", .03)
    return p

def iter3():  # wall-anchored cantilever + headboard pod
    p = Pod("Wall-Anchored Cantilever")
    p.add("Anchor_Strongback", "gunmetal", box(-W / 2 - .1, W / 2 + .1, .05, 1.05, ZH - .04, ZH))
    for x in (-.6, 0, .6):
        p.add("Anchor_Brackets", "gunmetal", box(x - .015, x + .015, .1, .3, ZH, ZH + .7))
        p.add("Anchor_Bolts", "alloy", *[box(x - .014, x + .014, y - .014, y + .014, ZH, ZH + .012) for y in (.4, .95)])
    p.add("Frame", "white", bev(W, LZ, .18, .32, .05, .02, 2))
    p.add("Accent_Band", "violet", box(-W / 2 + .05, W / 2 - .05, .18, .19, ZF - .002, ZF + .002))
    p.add("Drawer_Under", "gunmetal", blk(-.6, .6, .19, .2, -.6, .6, .02, 1))   # under-glow tray is flush; lift deck seam
    p.add("Headboard", "white", bev(W + .2, .25, .55, 1.05, .06, .02, 2, 0, ZH + .125))
    p.add("Headboard_Shelf", "gunmetal", box(-W / 2 - .05, W / 2 + .05, .9, .905, ZH + .25, ZH + .252))
    for s in (-1, 1): p.add("Reading_Lights", "green", box(s * .55 - .04, s * .55 + .04, .6, .61, ZH + .25, ZH + .26))
    p.add("Headboard_Rail", "alloy", blk(-W / 2, W / 2, .5, .53, ZH, ZH + .04, .01, 1))
    bedding(p, .32, mz=.12, ml=1.75)
    return p

def iter4():  # low tatami platform + floor clamps + lift-up deck
    p = Pod("Low Platform + Floor Clamps")
    p.add("Frame", "slate", bev(W + .2, LZ + .1, 0, .18, .03, .01, 2))
    p.add("Lift_Deck", "warmgrey", box(-W / 2 + .05, W / 2 + .05, .18, .185, -.4, .8))
    p.add("Lift_Deck_Seam", "gunmetal", box(-W / 2 + .04, W / 2 + .06, .18, .186, .79, .81))
    for sx in (-1, 1):
        for sz in (-1, 1):
            x, z = sx * (W / 2 + .1), sz * (LZ / 2 + .05)
            p.add("Anchor_Clamps", "gunmetal", blk(x - .07, x + .07, 0, .2, z - .07, z + .07, .02, 1))
            p.add("Anchor_Bolts", "alloy", box(x - .02, x + .02, .2, .212, z - .02, z + .02))
            p.add("Clamp_Lights", "amber", box(x - .03, x + .03, .1, .112, z + sz * .07, z + sz * .072) if True else None)
    p.add("Headboard", "white", bev(W + .2, .08, .18, .55, .03, .015, 2, 0, ZH - .01))
    bedding(p, .185, mw=1.5, ml=1.9, th=.14, duvet="linen", pil="warmgrey", mat="linen")
    return p

def iter5():  # capsule bed: moulded tub, bolsters, partial canopy
    p = Pod("Capsule Bed + Canopy")
    p.add("Plinth", "gunmetal", box(-W / 2 + .1, W / 2 - .1, 0, .08, ZH + .1, ZF - .1))
    p.add("Frame", "white", bev(W, LZ, .08, .4, .14, .03, 2))
    for s in (-1, 1):
        p.add(f"Bolster_{'LR'[s > 0]}", "slatefab", soft(.12, 1.6, .4, .56, .06, s * (W / 2 - .07), .1))
        p.add("Drawer_" + "LR"[s > 0], "white", blk(min(s * W / 2, s * (W / 2 + .015)), max(s * W / 2, s * (W / 2 + .015)), .12, .34, -.2, .6, .01, 1))
        latch(p, s * (W / 2 + .0), .3, .6, "amber", .04)
    # partial canopy: arched moulded hood over the head end (to 1.1 m)
    a = np.linspace(0, np.pi, 13); outer = np.c_[np.cos(a) * W / 2, .45 + np.sin(a) * .65]; inner = np.c_[np.cos(a) * (W / 2 - .05), .45 + np.sin(a) * .6]
    import trimesh
    Vs, Fs = [], []
    poly = np.vstack([outer, inner[::-1]]); n = len(poly)
    for z in (ZH, ZH + .55): Vs += [(x, y, z) for x, y in poly]
    for i in range(n):
        j = (i + 1) % n; Fs += [(i, j, n + j), (i, n + j, n + i)]
    for i in range(len(a) - 1):   # end caps (strip between outer i and inner i)
        o0, o1, i0, i1 = i, i + 1, n - 1 - i, n - 2 - i
        Fs += [(o0, i0, o1), (o1, i0, i1), (n + o0, n + o1, n + i0), (n + o1, n + i1, n + i0)]
    can = trimesh.Trimesh(np.array(Vs), np.array(Fs), process=False); trimesh.repair.fix_normals(can)
    can.metadata["uv"] = np.array(Vs)[:, [0, 1]]
    p.add("Canopy", "white", can)
    p.add("Accent_Band", "violet", box(-W / 2 - .003, W / 2 + .003, .46, .47, ZH + .5, ZH + .52))
    p.add("Reading_Lights", "amber", box(-.25, .25, .93, .94, ZH + .3, ZH + .33))
    bedding(p, .4, mw=1.42, ml=1.85, mz=.05, th=.16)
    return p

def sheet(p, path, title):
    tris, geo = export_final(p.P, [path.replace("_sheet.png", ".glb")]) if path.endswith("_sheet.png") else (None, None)
    saved = tonemap(); top, front, side, iso = views()
    def rv(R, s, sh):
        im = render_view(geo, R, size=s, shadow=sh); ns = render_view(geo, R, size=s, shadow=False) if sh else im
        fg = np.abs(ns - ns[0, 0]).sum(2) > .03; im[fg] = np.clip(im[fg] * 1.12 + .02, 0, 1); return crop(im)
    ims = [rv(top, 600, False), rv(front, 600, True), rv(side, 600, True), rv(iso, 700, True)]; FMAT.update(saved)
    bg = "#F4F2EC"; fig, axs = plt.subplots(2, 2, figsize=(12, 10), facecolor=bg)
    for ax, im, t in zip(axs.flat, ims, ("Top", "Front (foot)", "Side", "Iso")):
        ax.imshow(im); ax.axis("off"); ax.set_title(t, y=-0.09, fontsize=11, color="#555")
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

# ---------- final: Moulded Platform + Drawers (iter_01) with iter_04 floor clamps ----------
def final_bed():
    p = Pod("Moulded Platform + Floor Clamps (final)"); Y0, Y1 = .08, .34
    p.add("Base", "gunmetal", bev(W - .2, LZ - .2, 0, Y0 + .01, .04, .008, 2))          # recessed plinth
    p.add("Shell", "white", soft(W, LZ, Y0, Y1, .05, n=3, k=2) if False else bev(W, LZ, Y0, Y1, .08, .025, 3))
    p.add("FootBand", "violet", box(-W / 2 + .12, W / 2 - .12, .2, .21, ZF - .003, ZF + .003))
    for sx in (-1, 1):
        for sz in (-1, 1):
            x, z, t = sx * (W / 2 - .08), sz * (LZ / 2 - .08), f"{'LR'[sx > 0]}{'HF'[sz > 0]}"
            p.add(f"FloorPlate_{t}", "gunmetal", box(x - .12, x + .12, 0, .012, z - .12, z + .12))       # 40 mm proud of shell
            p.add(f"Clamp_{t}", "gunmetal", box(x - .06, x + .06, .012, Y0, z - .06, z + .06))
            p.add("Clamp_Bolts", "alloy", *[box(x + dx - .012, x + dx + .012, .012, .022, z + dz - .012, z + dz + .012) for dx, dz in ((-.09, -.09), (.09, .09), (-.09, .09), (.09, -.09))])
            p.add("Clamp_Lights", "amber", box(x + sx * .06, x + sx * .066, .03, .05, z - .03, z + .03))
    for sx in (-1, 1):
        for j, zc in enumerate((-.25, .45)):
            x0 = sx * W / 2; a, b = sorted((x0, x0 + sx * .02)); t = f"{'LR'[sx > 0]}{j + 1}"
            p.add(f"Drawer_{t}", "white", blk(a, b, .1, .32, zc - .32, zc + .32, .012, 1))
            a, b = sorted((x0 + sx * .02, x0 + sx * .034))
            p.add("Drawer_Handles", "alloy", box(a, b, .27, .284, zc - .15, zc + .15))
            p.add("Drawer_Latches", "amber", box(a, b, .27, .284, zc + .2, zc + .25))
    p.add("Headboard", "white", bev(W, .1, Y0, .8, .05, .02, 2, 0, ZH + .05))
    bedding(p, Y1, mz=.03)
    return p

def final_main():
    p = final_bed(); gp = os.path.join(dc.ROOT, "godot/assets/models/double_bed_moulded_clamped.glb")
    tris, geo = export_final(p.P, [gp]); V = np.vstack([g[1] for g in geo.values()])
    bad = [n for n, (mk, m) in p.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    mat_top = max(g[1][:, 1].max() for n, g in geo.items() if n == "Mattress")
    print("tris", tris, "bounds", V.min(0).round(3), V.max(0).round(3), "mattress top", round(mat_top, 3), "non-watertight:", bad)
    saved = tonemap(); top, front, side, iso = views()
    def rv(R, s, sh):
        im = render_view(geo, R, size=s, shadow=sh); ns = render_view(geo, R, size=s, shadow=False) if sh else im
        fg = np.abs(ns - ns[0, 0]).sum(2) > .03; im[fg] = np.clip(im[fg] * 1.12 + .02, 0, 1); return crop(im)
    ims = [rv(top, 600, False), rv(front, 600, True), rv(side, 600, True), rv(iso, 700, True)]; FMAT.update(saved)
    bg = "#F4F2EC"; fig, axs = plt.subplots(2, 2, figsize=(12, 10), facecolor=bg)
    for ax, im, t in zip(axs.flat, ims, ("Top", "Foot", "Side", "Iso")):
        ax.imshow(im); ax.axis("off"); ax.set_title(t, y=-0.09, fontsize=11, color="#555")
    fig.suptitle("Final  Moulded Platform + Floor Clamps", fontsize=12, color="#444"); plt.tight_layout()
    fig.savefig(os.path.join(OUT, "final_moulded_clamped_sheet.png"), dpi=100, facecolor=bg); plt.close(fig)

if __name__ == "__main__":
    final_main() if len(sys.argv) > 1 and sys.argv[1] == "final" else main()
