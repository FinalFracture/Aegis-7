#!/usr/bin/env python3
"""Coat & storage closet (#22) - 5 iterations, 3.7 W (X) x 0.5 D (Z) x 2.1 H, front +Z, back on the wall, pivot
bottom-center. EMPTY by design (no clothes/coats; bars + hooks only). Shares the approved open-bay wardrobe's language:
bolted gunmetal wall plate, alloy rails @0.30 / 2.06 with a violet strip, alloy uprights, gunmetal brackets + hook clamps.
Modules: 0.05 slim ends + bays 0.9 / 0.6 / 0.6 / 0.6 / 0.9 = 3.7. Outputs design/assets/coat_closet/."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dining_chair_generator as dc
from dining_chair_generator import xf, export_final, render_view, FMAT, shade_split
from bath_pod_generator import blk, cyl, Pod, views
from kitchen_counter_generator import bev, box, crop, tonemap
import wardrobe_generator as wg
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(dc.ROOT, "design/assets/coat_closet")
W, D, H = 3.7, 0.5, 2.1; ZB, ZF = -D / 2, D / 2; WZ = ZB + .02; EP = .05; Y0, YT = .15, 2.06
BAYS = [.9, .6, .6, .6, .9]

def bays():
    x = -W / 2 + EP; out = []
    for i, w in enumerate(BAYS): out.append((i, x + w / 2, w)); x += w
    return out

def joints(): return [-W / 2 + EP] + [cx + w / 2 for _, cx, w in bays()]

def wall_system(p, uprights=True, y0=Y0):
    """Shared wardrobe language: plate, rails, violet strip, uprights, brackets, bolts, hook clamps, slim end cheeks."""
    p.add("Wall_Plate", "gunmetal", bev(W, .02, .1, H, .006, .004, 1, 0, ZB + .01))
    p.add("Wall_Rail", "alloy", *[blk(-W / 2 + .02, W / 2 - .02, y, y + .04, WZ, WZ + .03, .01, 1) for y in (.3, 2.06)])
    p.add("Accent_Strip", "violet", box(-W / 2 + .05, W / 2 - .05, 2.07, 2.085, WZ + .03, WZ + .034))
    for x in joints():
        if uprights: p.add("Uprights", "alloy", bev(.03, D - .04, y0, YT, .006, .004, 1, x, WZ + (D - .04) / 2))
        p.add("Brackets", "gunmetal", box(x - .04, x + .04, .25, 2.04, WZ, WZ + .015))
        p.add("Bracket_Bolts", "alloy", *[box(x - .012, x + .012, y - .012, y + .012, WZ + .015, WZ + .024) for y in (.6, 1.6)])
        p.add("Hook_Clamps", "gunmetal", *[box(x - .05, x + .05, y - .02, y + .04, WZ + .03, WZ + .06) for y in (.3, 2.06)])
    for s in (-1, 1): p.add("End_Cheeks", "gunmetal", bev(EP - .01, D - .04, y0, H - .04, .008, .004, 1, s * (W / 2 - EP / 2), WZ + (D - .04) / 2))

def shelf(p, name, a, b, y, z0=WZ + .01, z1=ZF - .02):
    p.add(name, "gunmetal", bev(b - a, z1 - z0, y, y + .02, .006, .004, 1, (a + b) / 2, (z0 + z1) / 2))

def hooks(p, a, b, y, n, z=WZ + .03):   # alloy coat hooks on a gunmetal hook bar (empty)
    p.add("Hook_Bars", "gunmetal", box(a + .02, b - .02, y - .03, y + .03, z, z + .015))
    for x in np.linspace(a + .1, b - .1, n):
        p.add("Coat_Hooks", "alloy", box(x - .008, x + .008, y - .02, y + .02, z + .015, z + .09), box(x - .008, x + .008, y + .02, y + .06, z + .075, z + .09))

def strap(p, a, b, y, zf=ZF - .02):
    p.add("Straps", "slatefab", box(a, b, y, y + .035, zf - .012, zf))
    p.add("Buckle_Latches", "amber", box(b - .06, b - .02, y + .008, y + .027, zf, zf + .008))

def boot_tray(p, a, b):
    p.add("Boot_Trays", "gunmetal", bev(b - a, D - .08, Y0, Y0 + .02, .01, .004, 1, (a + b) / 2, WZ + (D - .08) / 2))
    p.add("Boot_Tray_Lips", "alloy", box(a, b, Y0 + .02, Y0 + .06, ZF - .045, ZF - .035))

def sprocket_dock(p, cx, w):
    p.add("Sprocket_DockPad", "gunmetal", bev(w - .08, D - .06, 0, .03, .04, .01, 2, cx, WZ + (D - .06) / 2))
    p.add("Sprocket_DockRing", "amber", xf(dc.torus_ring(.16, .006, 16, 3), t=(cx, .032, WZ + .25)))
    p.add("Sprocket_Port", "gunmetal", box(cx - .06, cx + .06, .39, .51, WZ + .015, WZ + .03))
    p.add("Sprocket_Port_Light", "amber", box(cx - .02, cx + .02, .43, .47, WZ + .03, WZ + .034))

def iter1():  # open rail bays: hook bays + strapped shelf bays (pure wardrobe twin)
    p = Pod("Open Hook + Shelf Bays"); wall_system(p)
    for i, cx, w in bays():
        a, b = cx - w / 2 + .015, cx + w / 2 - .015
        shelf(p, f"Shelves_{i + 1}", a, b, YT - .02)
        if w > .8:
            hooks(p, a, b, 1.7, 5); hooks(p, a, b, 1.25, 4); boot_tray(p, a, b)
        else:
            ys = list(np.linspace(Y0, YT - .02, 5))
            for y in ys[:-1]: shelf(p, f"Shelves_{i + 1}", a, b, y)
            for y in ys[:-1]: strap(p, a, b, y + .17)
    return p

def iter2():  # hung moulded doors on rails (wall-pod language), one open
    p = Pod("Hung Doors on Rails"); wall_system(p)
    for i, cx, w in bays():
        a, b = cx - w / 2 + .015, cx + w / 2 - .015; zf = ZF - .03
        shelf(p, f"Shelves_{i + 1}", a, b, YT - .02); shelf(p, f"Shelves_{i + 1}", a, b, Y0)
        if w > .8: hooks(p, a, b, 1.7, 4)
        else: shelf(p, f"Shelves_{i + 1}", a, b, 1.1)
        door = bev(w - .03, .02, Y0 + .02, YT - .03, .02, .006, 2, cx, zf + .01)
        if i == 0:
            p.add("Door_1", "white", wg.roty(door, -75, [cx - (w - .03) / 2, 0, zf]))
        else:
            p.add(f"Door_{i + 1}", "white", door)
            p.add("Door_Pulls", "alloy", box(cx + w / 2 - .07, cx + w / 2 - .055, .9, 1.3, zf + .02, zf + .035))
            p.add("Door_Latches", "amber", box(cx + w / 2 - .07, cx + w / 2 - .055, 1.33, 1.37, zf + .02, zf + .03))
    return p

def iter3():  # mudroom: bench with lift-lid storage, hooks, cubbies, Sprocket dock bay
    p = Pod("Mudroom Bench + Sprocket Dock"); wall_system(p, uprights=False)
    b_ = bays(); a0, a1 = -W / 2 + EP, b_[3][1] + b_[3][2] / 2          # bench over bays 1-4
    p.add("Bench_Box", "gunmetal", bev(a1 - a0, D - .06, Y0, .42, .02, .008, 2, (a0 + a1) / 2, WZ + (D - .06) / 2))
    p.add("Bench_Lids", "white", *[bev(w - .02, D - .05, .42, .46, .03, .01, 2, cx, WZ + (D - .05) / 2) for _, cx, w in b_[:4]])
    for _, cx, w in b_[:4]: p.add("Lid_Latches", "amber", box(cx - .03, cx + .03, .43, .445, ZF - .03, ZF - .022))
    p.add("Bench_Kick", "gunmetal", box(a0 + .02, a1 - .02, 0, Y0, WZ + .02, ZF - .08))
    hooks(p, a0, a1, 1.55, 12)
    for _, cx, w in b_[:4]:
        p.add("Cubbies", "gunmetal", bev(w - .02, .32, 1.8, 1.82, .006, .004, 1, cx, WZ + .17), box(cx + w / 2 - .02, cx + w / 2, 1.82, YT, WZ, WZ + .32))
        p.add("Cubby_Tops", "gunmetal", bev(w - .02, .32, YT - .02, YT, .006, .004, 1, cx, WZ + .17))
        strap(p, cx - w / 2 + .03, cx + w / 2 - .03, 1.88, WZ + .32)
    _, cx, w = b_[4]          # 0.9 Sprocket dock bay (Sprocket ~0.78 W x 1.03 H): open to the floor
    p.add("Dock_Uprights", "alloy", *[bev(.03, D - .04, 0, YT, .006, .004, 1, x, WZ + (D - .04) / 2) for x in (cx - w / 2, cx + w / 2)])
    sprocket_dock(p, cx, w); shelf(p, "Dock_Shelf", cx - w / 2 + .015, cx + w / 2 - .015, 1.2); shelf(p, "Dock_Shelf", cx - w / 2 + .015, cx + w / 2 - .015, YT - .02)
    p.add("Dock_Status", "green", box(cx - .1, cx + .1, 1.18, 1.19, ZF - .05, ZF - .02))
    return p

def iter4():  # sliding gunmetal panels on the top rail + equipment (suit/hardware) locker
    p = Pod("Sliding Panels + Suit Locker"); wall_system(p)
    for i, cx, w in bays():
        a, b = cx - w / 2 + .015, cx + w / 2 - .015
        shelf(p, f"Shelves_{i + 1}", a, b, YT - .02); shelf(p, f"Shelves_{i + 1}", a, b, Y0)
        if i == 4:   # suit / hardware locker: latched white door, green status, hooks inside
            p.add("Locker_Door", "white", bev(w - .03, .025, Y0 + .02, YT - .03, .02, .008, 2, cx, ZF - .015))
            p.add("Locker_Status", "green", box(cx + .3, cx + .36, 1.5, 1.515, ZF - .002, ZF + .004))
            p.add("Locker_Latch", "amber", box(cx + .3, cx + .36, 1.4, 1.43, ZF - .002, ZF + .004))
        elif w > .8: hooks(p, a, b, 1.7, 4); boot_tray(p, a, b)
        else:
            for y in (.6, 1.1, 1.6): shelf(p, f"Shelves_{i + 1}", a, b, y)
    p.add("Slide_Track", "alloy", box(-W / 2 + EP, W / 2 - EP - .9, YT - .005, YT + .01, ZF - .04, ZF - .005))
    for k, x0 in enumerate((-W / 2 + EP + .6, .05)):   # two sliding panels, gaps show the empty bays
        p.add(f"Slide_Panel_{k + 1}", "gunmetal", bev(.9, .015, Y0 + .03, YT - .01, .01, .004, 1, x0 + .45, ZF - .022))
        p.add("Slide_Pulls", "alloy", box(x0 + .82, x0 + .84, .9, 1.3, ZF - .014, ZF))
    return p

def iter5():  # mixed utility: tall tool locker, drawer stack, hooks, Sprocket hatch + laundry chute
    p = Pod("Utility Mix + Service Hatch"); wall_system(p)
    b_ = bays()
    _, cx, w = b_[0]; a, b = cx - w / 2 + .015, cx + w / 2 - .015
    p.add("Tool_Locker", "white", bev(w - .03, .025, Y0 + .02, YT - .03, .02, .008, 2, cx, ZF - .015))
    p.add("Tool_Locker_Latch", "amber", box(cx + .3, cx + .36, 1.1, 1.13, ZF - .002, ZF + .004))
    for k in (1, 2):
        _, cx, w = b_[k]; a, b = cx - w / 2 + .015, cx + w / 2 - .015
        for j, y in enumerate((Y0 + .02, .45, .75, 1.05)):
            p.add(f"Drawer_{k}_{j + 1}", "white", bev(w - .03, .02, y, y + .27, .012, .005, 2, cx, ZF - .02))
            p.add("Drawer_Latches", "amber", box(cx + .18, cx + .23, y + .22, y + .235, ZF - .01, ZF - .002))
        shelf(p, f"Shelves_{k + 1}", a, b, 1.4); shelf(p, f"Shelves_{k + 1}", a, b, YT - .02); strap(p, a, b, 1.6)
    _, cx, w = b_[3]; a, b = cx - w / 2 + .015, cx + w / 2 - .015
    p.add("Service_Hatch", "gunmetal", bev(w - .05, .02, .2, .7, .03, .008, 2, cx, ZF - .02))
    p.add("Sprocket_Port_Light", "amber", box(cx - .02, cx + .02, .43, .47, ZF - .01, ZF - .006))
    p.add("Laundry_Chute", "gunmetal", bev(w - .1, .02, .9, 1.25, .04, .008, 2, cx, ZF - .02))
    p.add("Chute_Status", "green", box(cx - .08, cx + .08, 1.27, 1.28, ZF - .03, ZF - .02))
    shelf(p, "Shelves_4", a, b, 1.5); shelf(p, "Shelves_4", a, b, YT - .02)
    _, cx, w = b_[4]; a, b = cx - w / 2 + .015, cx + w / 2 - .015
    hooks(p, a, b, 1.7, 4); hooks(p, a, b, 1.2, 4); boot_tray(p, a, b); shelf(p, "Shelves_5", a, b, YT - .02)
    return p

def wardrobe_geo(dx):
    w = wg.final_openbays(); out = {}
    for n, (mk, m) in w.P.items():
        V, N, UV, F = shade_split(m); out["WR_" + n] = (mk, V + np.array([dx, 0, 0]), N, F)
    return out

def main():
    os.makedirs(OUT, exist_ok=True); isos = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); tris, iso, lo, hi, bad = wg.sheet(p, os.path.join(OUT, f"iter_0{i}_sheet.png"), f"iter_0{i}  {p.name}  (empty: no clothes)")
        print(i, p.name, tris, lo, hi, "non-watertight:", bad)
        _, geo = export_final(p.P, [os.path.join(OUT, f"iter_0{i}.glb")])
        g = dict(geo); g.update(wardrobe_geo(-(W / 2 + wg.W / 2 + .1)))
        saved = tonemap(); top, front, side, isoR = views()
        im = render_view(g, isoR, size=820, shadow=True); ns = render_view(g, isoR, size=820, shadow=False)
        fg = np.abs(ns - ns[0, 0]).sum(2) > .03; im[fg] = np.clip(im[fg] * 1.12 + .02, 0, 1); FMAT.update(saved)
        isos.append((p.name, crop(im)))
    fig, axs = plt.subplots(3, 2, figsize=(18, 14), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)):
        ax.imshow(im); ax.set_title(f"{i}. {n}  (right)  beside approved open-bay wardrobe (left)", y=-0.1, fontsize=11, color="#555")
    plt.tight_layout(); fig.savefig(os.path.join(OUT, "overview.png"), dpi=80, facecolor="#F4F2EC"); plt.close(fig)

# ---------- final: polished Mudroom Bench + Sprocket Dock (iter_03) ----------
SPROCKET = os.path.join(dc.ROOT, "godot/assets/models/char_bot_r2_05_livery_01_sprocket.glb")
PROUD = 0.20   # dock alcove cheeks + charging collar stand proud of the closet face

def final_mudroom():
    p = Pod("Mudroom Bench + Sprocket Dock (final)"); b_ = bays(); _, dcx, dw = b_[4]
    da, db = dcx - dw / 2, dcx + dw / 2                    # dock bay x-range
    # wall plate + bottom rail NOTCHED at the dock bay (open back: Sprocket docks against the wall); top rail continuous
    p.add("Wall_Plate", "gunmetal", bev(da - (-W / 2), .02, .1, H, .006, .004, 1, (da - W / 2) / 2, ZB + .01),
          bev(W / 2 - db + .0, .02, .1, H, .006, .004, 1, (db + W / 2) / 2, ZB + .01), bev(dw, .02, 1.3, H, .006, .004, 1, dcx, ZB + .01))
    p.add("Wall_Rail_Top", "alloy", blk(-W / 2 + .02, W / 2 - .02, 2.06, 2.1, WZ, WZ + .03, .01, 1))
    p.add("Wall_Rail_Low", "alloy", blk(-W / 2 + .02, da - .02, .3, .34, WZ, WZ + .03, .01, 1))
    p.add("Accent_Strip", "violet", box(-W / 2 + .05, W / 2 - .05, 2.07, 2.085, WZ + .03, WZ + .034))
    for x in joints():
        p.add("Brackets", "gunmetal", box(x - .04, x + .04, .25 if x < da - .01 else 1.32, 2.04, WZ, WZ + .015))
        p.add("Bracket_Bolts", "alloy", *[box(x - .012, x + .012, y - .012, y + .012, WZ + .015, WZ + .024) for y in ((.6, 1.6) if x < da - .01 else (1.5, 1.9))])
        p.add("Hook_Clamps", "gunmetal", *[box(x - .05, x + .05, y - .02, y + .04, WZ + .03, WZ + .06) for y in ((.3, 2.06) if x < da - .01 else (2.06,))])
    p.add("End_Cheek_L", "gunmetal", bev(EP - .01, D - .04, Y0, H - .04, .008, .004, 1, -W / 2 + EP / 2, WZ + (D - .04) / 2))
    # bench (bays 1-4): gunmetal box, latched white lift lids, recessed kick
    a0, a1 = -W / 2 + EP, da
    p.add("Bench_Box", "gunmetal", bev(a1 - a0 - .01, D - .06, Y0, .42, .025, .01, 3, (a0 + a1) / 2, WZ + (D - .06) / 2))
    p.add("Bench_Kick", "gunmetal", bev(a1 - a0 - .06, D - .14, 0, Y0, .02, .006, 2, (a0 + a1) / 2, WZ + (D - .14) / 2))
    for k, (_, cx, w) in enumerate(b_[:4], 1):
        p.add(f"Bench_Lid_{k}", "white", bev(w - .02, D - .05, .42, .465, .035, .014, 3, cx, WZ + (D - .05) / 2))
        p.add(f"Lid_Latch_{k}", "amber", box(cx - .03, cx + .03, .435, .45, ZF - .028, ZF - .02))
        p.add(f"Lid_Pull_{k}", "alloy", bev(.16, .012, .44, .452, .005, .002, 1, cx - .12, ZF - .022))
    # hook rail (empty) + strapped cubbies
    p.add("Hook_Bar", "gunmetal", bev(a1 - a0 - .04, .015, 1.52, 1.58, .006, .003, 1, (a0 + a1) / 2, WZ + .0225))
    for x in np.linspace(a0 + .12, a1 - .12, 12):
        p.add("Coat_Hooks", "alloy", box(x - .008, x + .008, 1.53, 1.57, WZ + .03, WZ + .1), box(x - .008, x + .008, 1.57, 1.61, WZ + .085, WZ + .1))
    for k, (_, cx, w) in enumerate(b_[:4], 1):
        p.add("Cubby_Shelves", "gunmetal", bev(w - .02, .32, 1.8, 1.82, .006, .004, 1, cx, WZ + .17), bev(w - .02, .32, YT - .02, YT, .006, .004, 1, cx, WZ + .17))
        p.add("Cubby_Dividers", "alloy", bev(.02, .32, 1.82, YT - .02, .005, .003, 1, cx + w / 2 - .01, WZ + .17))
        p.add(f"Cubby_Strap_{k}", "slatefab", box(cx - w / 2 + .03, cx + w / 2 - .03, 1.88, 1.915, WZ + .308, WZ + .32))
        p.add("Cubby_Buckles", "amber", box(cx + w / 2 - .09, cx + w / 2 - .05, 1.888, 1.907, WZ + .32, WZ + .328))
    # dock alcove: proud gunmetal cheeks (from floor), alloy edge, charging collar header, recessed-look pad, wall coupler
    zc1 = ZF + PROUD
    for x, nm in ((da, "L"), (db, "R")):
        sx = -1 if nm == "L" else 1
        p.add(f"Dock_Cheek_{nm}", "gunmetal", bev(.04, zc1 - ZB, 0, YT, .01, .005, 2, x + sx * .0 - sx * 0, (ZB + zc1) / 2))
        p.add(f"Dock_Cheek_Edge_{nm}", "alloy", bev(.044, .02, 0, YT, .006, .003, 1, x, zc1 - .01))
    p.add("Dock_Collar", "gunmetal", bev(dw + .04, zc1 - ZB, 1.2, 1.28, .02, .008, 2, dcx, (ZB + zc1) / 2))
    p.add("Dock_Collar_Light", "amber", box(dcx - .3, dcx + .3, 1.2 - .004, 1.2, zc1 - .1, zc1 - .03))
    p.add("Dock_Status", "green", box(dcx - .1, dcx + .1, 1.23, 1.25, zc1, zc1 + .004))
    p.add("Dock_Shelf", "gunmetal", bev(dw - .04, D - .06, YT - .02, YT, .006, .004, 1, dcx, WZ + (D - .06) / 2))
    p.add("Dock_Pad", "gunmetal", bev(dw - .06, zc1 - ZB - .02, 0, .015, .05, .006, 3, dcx, (ZB + zc1) / 2))      # 15 mm low-ramp pad
    p.add("Dock_Pad_Ring", "amber", xf(dc.torus_ring(.2, .006, 20, 3), t=(dcx, .016, .1)))
    p.add("Dock_Coupler_Plate", "gunmetal", bev(.2, .012, .35, .55, .02, .004, 2, dcx, ZB + .006))          # bolted to wall surface
    p.add("Dock_Coupler_Port", "amber", box(dcx - .03, dcx + .03, .42, .48, ZB + .012, ZB + .016))
    p.add("Dock_Floor_Clamps", "gunmetal", *[box(x - .03, x + .03, 0, .06, zc1 - .08, zc1 - .02) for x in (da + .05, db - .05)])
    p.add("Dock_Clamp_Lights", "amber", *[box(x - .015, x + .015, .03, .045, zc1 - .02, zc1 - .016) for x in (da + .05, db - .05)])
    return p

def sprocket_geo(dcx):
    sc = trimesh.load(SPROCKET); out = {}; z_off = ZB + .016 - (-.346)
    for n, g in sc.geometry.items():
        m = g.copy(); m.apply_translation((dcx, .015, z_off)); ln = n.lower()
        mk = ("violet" if "rfid" in ln else "gunmetal" if any(k in ln for k in ("track", "eye", "claw")) else "alloy" if any(k in ln for k in ("servo", "gimbal", "brow")) else "white")
        out["SPROCKET_" + n] = (mk, np.array(m.vertices), np.array(m.vertex_normals), np.array(m.faces))
    return out, z_off + .423

def final_main():
    p = final_mudroom(); gp = os.path.join(dc.ROOT, "godot/assets/models/coat_closet_mudroom.glb")
    tris, geo = export_final(p.P, [gp]); V = np.vstack([g[1] for g in geo.values()])
    bad = [n for n, (mk, m) in p.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    _, dcx, _ = bays()[4]; sg, sfront = sprocket_geo(dcx)
    print("tris", tris, "bounds", V.min(0).round(3), V.max(0).round(3), "bad", bad)
    print("sprocket front z", round(sfront, 3), "overhang vs closet face", round(sfront - ZF, 3), "vs alcove cheeks", round(sfront - (ZF + PROUD), 3))
    saved = tonemap(); top, front, side, iso = views()
    def rv(g, R, s, sh):
        im = render_view(g, R, size=s, shadow=sh); ns = render_view(g, R, size=s, shadow=False) if sh else im
        fg = np.abs(ns - ns[0, 0]).sum(2) > .03; im[fg] = np.clip(im[fg] * 1.12 + .02, 0, 1); return crop(im)
    g2 = dict(geo); g2.update(sg)
    ims = [rv(geo, top, 700, False), rv(geo, front, 700, True), rv(geo, side, 600, True), rv(geo, iso, 700, True), rv(g2, iso, 700, True)]
    FMAT.update(saved)
    bg = "#F4F2EC"; fig = plt.figure(figsize=(15, 11), facecolor=bg); gs = fig.add_gridspec(3, 3, width_ratios=[1, 1, .45], height_ratios=[.45, 1, 1])
    for ax, im, t in ((fig.add_subplot(gs[0, :2]), ims[0], "Top"), (fig.add_subplot(gs[:, 2]), ims[2], "Side"),
                      (fig.add_subplot(gs[1, 0]), ims[1], "Front"), (fig.add_subplot(gs[1, 1]), ims[3], "Iso"),
                      (fig.add_subplot(gs[2, :2]), ims[4], "Iso with Sprocket docked (visual only, not in glb)")):
        ax.imshow(im); ax.axis("off"); ax.set_title(t, y=-0.08, fontsize=10, color="#555")
    fig.suptitle("Final  Mudroom Bench + Sprocket Dock (empty)", fontsize=12, color="#444"); plt.tight_layout()
    fig.savefig(os.path.join(OUT, "final_mudroom_sheet.png"), dpi=100, facecolor=bg); plt.close(fig)

if __name__ == "__main__":
    final_main() if len(sys.argv) > 1 and sys.argv[1] == "final" else main()
