#!/usr/bin/env python3
"""Washer/dryer stack (#37) - 5 iterations. 0.8 W (X) x 0.8 D (Z) x 1.9 H, front +Z, Y up, pivot bottom-center.
Family language: white moulded composite, brushed alloy, gunmetal, violet band, amber latches/ports, green status,
bolted floor clamps + wall plates. Sprocket service port at 0.45 m. Empty (no clothes). Outputs design/assets/washer_dryer/."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dining_chair_generator as dc
from dining_chair_generator import loft, circle, torus_ring, xf, FMAT
from bath_pod_generator import blk, cyl, Pod
from kitchen_counter_generator import bev, box
import wardrobe_generator as wg
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(dc.ROOT, "design/assets/washer_dryer")
W, D, H = 0.8, 0.8, 1.9; ZB, ZF = -D / 2, D / 2
RX = trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0])

def zdisc(x, y, z0, z1, r, s=20):   # cylinder along Z
    m = loft(circle(r, s), [(0, 1, 1), (z1 - z0, 1, 1)]); m = xf(m, RX); return xf(m, t=(x, y, z1))

def zring(x, y, z, R, r=.018, nu=20):
    return xf(xf(torus_ring(R, r, nu, 5), RX), t=(x, y, z))

def porthole(p, nm, y, z, R=.2):
    p.add(f"{nm}_Door_Ring", "alloy", zring(0, y, z + .02, R, .022))
    p.add(f"{nm}_Door_Glass", "slate", zdisc(0, y, z, z + .02, R - .01))
    p.add(f"{nm}_Door_Latch", "amber", box(R - .02, R + .03, y - .015, y + .015, z + .02, z + .03))

def controls(p, y, z, w=.5):
    p.add("Control_Strip", "gunmetal", bev(w, .015, y, y + .06, .01, .004, 1, 0, z + .0075))
    p.add("Status_Lights", "green", box(-w / 2 + .03, -w / 2 + .09, y + .025, y + .035, z + .015, z + .019))
    p.add("Status_Lights", "amber", box(w / 2 - .09, w / 2 - .03, y + .025, y + .035, z + .015, z + .019))

def clamps(p, inset=.08, top=.06):
    for sx in (-1, 1):
        for sz in (-1, 1):
            x, z = sx * (W / 2 - inset), sz * (D / 2 - inset)
            p.add("Floor_Clamps", "gunmetal", box(x - .04, x + .04, .012, top, z - .04, z + .04))
            p.add("Floor_Plates", "gunmetal", box(x - .07, x + .07, 0, .012, z - .07, z + .07))
            p.add("Clamp_Bolts", "alloy", box(x - .06, x - .04, .012, .02, z - .06, z - .04), box(x + .04, x + .06, .012, .02, z + .04, z + .06))
            p.add("Iso_Pads", "slatefab", cyl(x, z, .03, top, top + .02, 10))

def sprocket_port(p, x, z, face="+x"):
    if face == "+x":
        p.add("Sprocket_Port", "gunmetal", box(x, x + .01, .39, .51, z - .06, z + .06)); p.add("Sprocket_Port_Light", "amber", box(x + .01, x + .014, .43, .47, z - .02, z + .02))
    else:
        p.add("Sprocket_Port", "gunmetal", box(x - .06, x + .06, .39, .51, z, z + .01)); p.add("Sprocket_Port_Light", "amber", box(x - .02, x + .02, .43, .47, z + .01, z + .014))

def iter1():  # monolithic moulded tower, two front portholes
    p = Pod("Moulded Tower Stack"); clamps(p)
    p.add("Plinth", "gunmetal", bev(W - .12, D - .12, .08, .14, .03, .01, 2))
    p.add("Washer_Shell", "white", bev(W, D, .14, 1.0, .06, .02, 3)); p.add("Dryer_Shell", "white", bev(W, D, 1.02, H, .06, .02, 3))
    p.add("Accent_Band", "violet", bev(W - .01, D - .01, 1.0, 1.02, .055, .004, 2))
    porthole(p, "Washer", .55, ZF); porthole(p, "Dryer", 1.42, ZF)
    controls(p, .88, ZF); controls(p, 1.78, ZF)
    p.add("Lint_Drawer", "gunmetal", bev(.3, .012, 1.08, 1.13, .01, .003, 1, -.18, ZF + .006))
    p.add("Water_Drawer", "gunmetal", bev(.3, .012, .18, .24, .01, .003, 1, -.18, ZF + .006))
    sprocket_port(p, W / 2, 0)
    return p

def iter2():  # alloy frame + slide-in cassettes, wall plate, visible dampers
    p = Pod("Alloy Frame + Cassettes"); clamps(p, .05, .04)
    p.add("Wall_Plate", "gunmetal", box(-W / 2, W / 2, .1, H, ZB - .02, ZB))
    p.add("Wall_Rail", "alloy", *[box(-W / 2 + .02, W / 2 - .02, y, y + .04, ZB, ZB + .03) for y in (.3, 1.84)])
    for sx in (-1, 1):
        for sz in (-1, 1): p.add("Frame_Posts", "alloy", bev(.04, .04, .04, H, .008, .004, 1, sx * (W / 2 - .02), sz * (D / 2 - .02)))
    for y in (.08, .98, H - .04): p.add("Frame_Rails", "alloy", bev(W, D, y, y + .03, .01, .004, 1) if y < .1 or y > 1.8 else box(-W / 2, W / 2, y, y + .03, ZF - .04, ZF))
    for nm, y0, y1 in (("Washer", .12, .96), ("Dryer", 1.02, H - .05)):
        p.add(f"{nm}_Cassette", "white" if nm == "Washer" else "gunmetal", bev(W - .1, D - .1, y0, y1, .04, .015, 2))
        porthole(p, nm, (y0 + y1) / 2 - .04, ZF - .05, .18); controls(p, y1 - .1, ZF - .05, .4)
        p.add("Cassette_Latches", "amber", *[box(sx * (W / 2 - .07) - .015, sx * (W / 2 - .07) + .015, y1 - .06, y1 - .03, ZF - .05, ZF - .04) for sx in (-1, 1)])
    p.add("Dampers", "gunmetal", *[cyl(sx * .25, sz * .25, .03, .11, .14, 10) for sx in (-1, 1) for sz in (-1, 1)])
    p.add("Accent_Band", "violet", box(-W / 2 + .02, W / 2 - .02, .965, .975, ZF - .04, ZF - .036))
    sprocket_port(p, 0, ZF - .05, "+z") if False else sprocket_port(p, W / 2 - .05, 0)
    return p

def iter3():  # washer on isolation plinth + dryer hung on wall rails above
    p = Pod("Floor Washer + Wall-Hung Dryer"); clamps(p)
    p.add("Wall_Plate", "gunmetal", box(-W / 2, W / 2, .1, H, ZB - .02, ZB))
    p.add("Wall_Rail", "alloy", *[box(-W / 2 + .02, W / 2 - .02, y, y + .04, ZB, ZB + .03) for y in (1.15, 1.82)])
    p.add("Hook_Clamps", "gunmetal", *[box(x - .05, x + .05, y - .02, y + .06, ZB + .03, ZB + .07) for x in (-.25, .25) for y in (1.15, 1.82)])
    p.add("Isolation_Plinth", "gunmetal", bev(W - .04, D - .04, .08, .16, .03, .01, 2))
    p.add("Washer_Shell", "white", bev(W, D - .04, .16, 1.0, .06, .02, 3, 0, .02)); porthole(p, "Washer", .56, ZF); controls(p, .9, ZF)
    p.add("Dryer_Shell", "white", bev(W, D - .2, 1.1, H, .06, .02, 3, 0, ZB + .07 + (D - .2) / 2)); 
    zf = ZB + .07 + D - .2; porthole(p, "Dryer", 1.48, zf, .17); controls(p, 1.8, zf, .4)
    p.add("Lint_Drawer", "gunmetal", bev(.3, .012, 1.14, 1.19, .01, .003, 1, -.18, zf + .006))
    p.add("Accent_Band", "violet", box(-W / 2 + .03, W / 2 - .03, 1.1, 1.108, ZB + .08, zf))
    p.add("Brackets", "gunmetal", *[box(x - .012, x + .012, 1.04, 1.12, ZB + .03, zf - .05) for x in (-.33, .33)])
    sprocket_port(p, W / 2, 0)
    return p

def iter4():  # pull-out drawer drums (vertical axis = spin-gravity aligned), one open
    p = Pod("Drawer-Drum Stack"); clamps(p)
    p.add("Plinth", "gunmetal", bev(W - .12, D - .12, .08, .14, .03, .01, 2))
    p.add("Carcass", "white", bev(W, D, .14, H, .06, .02, 3))
    p.add("Accent_Band", "violet", box(-W / 2 + .04, W / 2 - .04, 1.0, 1.01, ZF, ZF + .004))
    for nm, y0, y1, out in (("Washer", .18, .96, .45), ("Dryer", 1.04, 1.82, 0)):
        z = ZF + out
        p.add(f"{nm}_Front", "white", bev(W - .04, .03, y0, y1, .03, .01, 2, 0, z + .015))
        p.add(f"{nm}_Pull", "alloy", bev(.4, .015, y1 - .1, y1 - .08, .006, .003, 1, 0, z + .035))
        p.add(f"{nm}_Latch", "amber", box(.25, .3, y1 - .1, y1 - .08, z + .03, z + .036))
        controls(p, y0 + .04, z + .03, .3)
        if out:   # pulled-out drum drawer: gunmetal tub, alloy drum rim, lid hinged up
            p.add(f"{nm}_Tub", "gunmetal", bev(W - .1, .55, y0 + .06, y1 - .12, .1, .02, 3, 0, z - .275))
            p.add(f"{nm}_Drum_Rim", "alloy", xf(torus_ring(.24, .015, 20, 5), t=(0, y1 - .12, z - .28)))
            p.add(f"{nm}_Drum_Floor", "slate", cyl(0, z - .28, .23, y1 - .14, y1 - .125, 20))
            p.add(f"{nm}_Slides", "alloy", *[box(sx * (W / 2 - .05) - .01, sx * (W / 2 - .05) + .01, y0 + .2, y0 + .24, ZF - .1, z) for sx in (-1, 1)])
    sprocket_port(p, W / 2, 0)
    return p

def iter5():  # single combo drum at ergonomic height + reclaim/cartridge base + condensate/recycler top
    p = Pod("Combo Drum + Reclaim Tower"); clamps(p)
    p.add("Plinth", "gunmetal", bev(W - .12, D - .12, .08, .14, .03, .01, 2))
    p.add("Reclaim_Base", "gunmetal", bev(W, D, .14, .62, .05, .015, 3))
    p.add("Cartridge_Drawer", "white", bev(W - .06, .02, .36, .58, .02, .006, 2, 0, ZF + .01)); p.add("Drawer_Latches", "amber", box(.25, .3, .54, .555, ZF + .02, ZF + .026))
    p.add("Service_Hatch", "white", bev(W - .06, .02, .17, .33, .02, .006, 2, 0, ZF + .01))
    p.add("Combo_Shell", "white", bev(W, D, .62, 1.5, .06, .02, 3)); porthole(p, "Combo", 1.03, ZF, .22); controls(p, 1.4, ZF)
    p.add("Accent_Band", "violet", bev(W - .01, D - .01, 1.5, 1.52, .055, .004, 2))
    p.add("Recycler_Top", "gunmetal", bev(W, D, 1.52, H, .05, .015, 3))
    p.add("Recycler_Vent", "alloy", *[box(-.3, .3, y, y + .012, ZF, ZF + .006) for y in (1.6, 1.64, 1.68, 1.72)])
    p.add("Recycler_Status", "green", box(-.05, .05, 1.8, 1.82, ZF, ZF + .005))
    p.add("Lint_Drawer", "alloy", bev(.25, .012, 1.76, 1.82, .01, .003, 1, -.22, ZF + .006))
    sprocket_port(p, 0, ZF, "+z") if False else sprocket_port(p, W / 2, 0)
    return p

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (empty)")
        isos.append((p.name, iso)); print(i, p.name, tris, lo, hi, "non-watertight:", bad)
    fig, axs = plt.subplots(1, 5, figsize=(20, 7), facecolor="#F4F2EC")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.axis("off"); ax.set_title(f"{i}. {n}", fontsize=12, color="#555")
    plt.tight_layout(rect=(0, 0, 1, .93)); fig.savefig(os.path.join(OUT, "overview.png"), dpi=85, facecolor="#F4F2EC"); plt.close(fig)

# ---------- final: iter_02 alloy frame + cassettes, iter_05 reclaim as a SHARED side tower ----------
from dining_chair_generator import export_final, render_view, shade_split
from kitchen_counter_generator import crop, tonemap
from bath_pod_generator import views
TW = .28; SX = -TW / 2          # stack centre offset so stack+tower is bottom-centred; tower on +X
def final_alloy_reclaim():
    p = Pod("Alloy Frame + Cassettes + Reclaim Tower (final)")
    x0, x1 = SX - W / 2, SX + W / 2
    for sx in (x0 + .05, x1 - .05):     # bolted plates + clamps + isolation pads under the frame
        for sz in (ZB + .07, ZF - .07):
            p.add("Floor_Plates", "gunmetal", bev(.13, .13, 0, .012, .015, .004, 1, sx, sz))
            p.add("Floor_Clamps", "gunmetal", box(sx - .035, sx + .035, .012, .045, sz - .035, sz + .035))
            p.add("Clamp_Bolts", "alloy", box(sx - .055, sx - .035, .012, .02, sz - .055, sz - .035), box(sx + .035, sx + .055, .012, .02, sz + .035, sz + .055))
    p.add("Wall_Plate", "gunmetal", bev(W + TW, .02, .1, H, .006, .004, 1, 0, ZB - .01))
    p.add("Wall_Rail", "alloy", *[blk(x0 + .02, x1 + TW - .02, y, y + .04, ZB, ZB + .03, .01, 1) for y in (.3, 1.84)])
    p.add("Hook_Clamps", "gunmetal", *[box(x - .05, x + .05, y - .02, y + .06, ZB + .03, ZB + .06) for x in (x0 + .15, x1 - .15) for y in (.3, 1.84)])
    for px in (x0 + .02, x1 - .02):
        for pz in (ZB + .05, ZF - .03):
            p.add("Frame_Posts", "alloy", bev(.04, .04, .045, H, .008, .004, 1, px, pz))
    p.add("Frame_Base", "alloy", bev(W, D - .06, .045, .08, .01, .004, 1, SX, .01), )
    p.add("Frame_Top", "alloy", bev(W, D - .06, H - .03, H, .01, .004, 1, SX, .01))
    p.add("Frame_Mid_Rail", "alloy", bev(W, .04, .97, 1.0, .008, .004, 1, SX, ZF - .03))
    p.add("Accent_Band", "violet", box(x0 + .03, x1 - .03, .98, .99, ZF - .01, ZF - .006))
    p.add("Dampers", "gunmetal", *[cyl(SX + sx * .25, sz * .25, .03, .08, .12, 12) for sx in (-1, 1) for sz in (-1, 1)])
    p.add("Dampers", "slatefab", *[cyl(SX + sx * .25, sz * .25, .034, 1.0, 1.03, 12) for sx in (-1, 1) for sz in (-1, 1)])
    for nm, y0, y1, mat in (("Washer", .12, .96, "white"), ("Dryer", 1.03, H - .05, "white")):
        p.add(f"{nm}_Cassette", mat, bev(W - .1, D - .12, y0, y1, .05, .02, 3, SX, 0))
        zf = (D - .12) / 2; yc = (y0 + y1) / 2 - .05
        p.add(f"{nm}_Door_Ring", "alloy", xf(zring(0, yc, zf + .02, .18, .022), t=(SX, 0, 0)))
        p.add(f"{nm}_Door_Glass", "slate", xf(zdisc(0, yc, zf, zf + .02, .17), t=(SX, 0, 0)))
        p.add(f"{nm}_Door_Latch", "amber", box(SX + .16, SX + .21, yc - .015, yc + .015, zf + .02, zf + .03))
        p.add(f"{nm}_Controls", "gunmetal", bev(.4, .012, y1 - .1, y1 - .045, .01, .004, 1, SX, zf + .006))
        p.add("Status_Lights", "green", box(SX - .17, SX - .11, y1 - .08, y1 - .07, zf + .012, zf + .016))
        p.add(f"{nm}_Cassette_Latches", "amber", *[box(SX + d - .015, SX + d + .015, y1 - .08, y1 - .05, zf, zf + .012) for d in (-W / 2 + .1, W / 2 - .1)])
    # shared reclaim / recycler tower (all parts prefixed Reclaim_ so the paired unit can hide them)
    tx = x1 + TW / 2; tz = .0
    p.add("Reclaim_Tower", "gunmetal", bev(TW - .02, D - .1, .02, H - .01, .04, .015, 3, tx, tz - .02))
    p.add("Reclaim_Cartridge_Drawer", "white", bev(TW - .06, .02, 1.0, 1.35, .02, .006, 2, tx, ZF - .06))
    p.add("Reclaim_Drawer_Latch", "amber", box(tx + .05, tx + .1, 1.31, 1.325, ZF - .05, ZF - .044))
    p.add("Reclaim_Lint_Drawer", "alloy", bev(TW - .06, .02, 1.45, 1.55, .02, .006, 2, tx, ZF - .06))
    p.add("Reclaim_Vents", "alloy", *[box(tx - .1, tx + .1, y, y + .012, ZF - .07, ZF - .064) for y in (1.65, 1.69, 1.73, 1.77)])
    p.add("Reclaim_Status", "green", box(tx - .04, tx + .04, 1.83, 1.845, ZF - .07, ZF - .066))
    p.add("Reclaim_Service_Hatch", "gunmetal", bev(TW - .06, .02, .3, .6, .02, .006, 2, tx, ZF - .06))
    p.add("Reclaim_Sprocket_Port", "amber", box(tx - .02, tx + .02, .43, .47, ZF - .05, ZF - .046))
    p.add("Reclaim_Pipes", "alloy", *[xf(xf(loft(circle(.02, 10), [(0, 1, 1), (.06, 1, 1)]), trimesh.transformations.rotation_matrix(-np.pi / 2, [0, 0, 1])), t=(x1 - .02, y, -.15)) for y in (.3, 1.3)])
    p.add("Reclaim_Floor_Clamps", "gunmetal", *[box(tx - .03, tx + .03, 0, .02, z - .05, z + .05) for z in (-.25, .2)])
    return p

def mirror_geo(geo, xm, drop="Reclaim_"):
    out = {}
    for n, (mk, V, N, F) in geo.items():
        if n.startswith(drop): continue
        V2 = V.copy(); V2[:, 0] = 2 * xm - V2[:, 0]; N2 = N.copy(); N2[:, 0] *= -1
        out["B_" + n] = (mk, V2, N2, F[:, ::-1])
    return out

def final_main():
    p = final_alloy_reclaim(); gp = os.path.join(dc.ROOT, "godot/assets/models/washer_dryer_alloy_reclaim.glb")
    tris, geo = export_final(p.P, [gp]); V = np.vstack([g[1] for g in geo.values()])
    bad = [n for n, (mk, m) in p.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    print("tris", tris, "bounds", V.min(0).round(3), V.max(0).round(3), "size", (V.max(0) - V.min(0)).round(3), "bad", bad)
    xm = SX + W / 2 + TW / 2; pair = dict(geo); pair.update(mirror_geo(geo, xm + TW / 2 - TW / 2 + 0))
    saved = tonemap(); top, front, side, iso = views()
    def rv(g, R, s, sh):
        im = render_view(g, R, size=s, shadow=sh); ns = render_view(g, R, size=s, shadow=False) if sh else im
        fg = np.abs(ns - ns[0, 0]).sum(2) > .03; im[fg] = np.clip(im[fg] * 1.12 + .02, 0, 1); return crop(im)
    ims = [rv(geo, top, 600, False), rv(geo, front, 600, True), rv(geo, side, 600, True), rv(geo, iso, 640, True), rv(pair, iso, 700, True)]
    FMAT.update(saved)
    bg = "#F4F2EC"; fig, axs = plt.subplots(1, 5, figsize=(22, 7), facecolor=bg, gridspec_kw={"width_ratios": [1, 1, 1, 1.1, 1.5]})
    for ax, im, t in zip(axs, ims, ("Top", "Front", "Side", "Iso", "Pair Iso (shared tower; unit B mirrored, Reclaim_* hidden)")):
        ax.imshow(im); ax.axis("off"); ax.set_title(t, fontsize=10, color="#555")
    fig.suptitle("Final  Alloy Frame + Cassettes + Shared Reclaim Tower", fontsize=12, color="#444"); plt.tight_layout(rect=(0, 0, 1, .93))
    fig.savefig(os.path.join(OUT, "final_alloy_reclaim_sheet.png"), dpi=90, facecolor=bg); plt.close(fig)

if __name__ == "__main__":
    final_main() if len(sys.argv) > 1 and sys.argv[1] == "final" else main()
