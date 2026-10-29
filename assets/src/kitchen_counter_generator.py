#!/usr/bin/env python3
"""Kitchen counter + hob (#9) - 5 modular run iterations. Owner: Rook.
Default run 3.5 m = EndCap 0.25 + 5 x 0.6 m modules (Cold, Store, Sink, Hob, Store) + EndCap 0.25; any 2.4-4.2 m run
is the same modules re-ordered. Pivot bottom-center, front faces +Z, Y up, worktop ~0.9 m. Reuses the loft / glb writer /
soft rasterizer from dining_chair_generator.py via bath_pod_generator.py. Outputs design/assets/kitchen_counter/."""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dining_chair_generator as dc
from dining_chair_generator import loft, rrect, circle, torus_ring, xf, merge, export_final, render_view, FMAT
from bath_pod_generator import blk, cyl, thick_path, Pod, views
from trimesh.visual.material import PBRMaterial as _PBR
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(dc.ROOT, "design/assets/kitchen_counter")
FMAT.update({
 "hobglass": _PBR(name="HobSlateGlass", baseColorFactor=(0.07, 0.075, 0.09, 1), metallicFactor=0.2, roughnessFactor=0.15),
 "green": _PBR(name="StatusGreen", baseColorFactor=(0.247, 0.686, 0.416, 1), metallicFactor=0.0, roughnessFactor=0.4, emissiveFactor=(0.247, 0.686, 0.416)),
})
L, DEP, TOP = 3.5, 0.6, 0.9; MW, EC = 0.6, 0.25
ORDER = ["Cold", "Store", "Sink", "Hob", "Store"]
ZB, ZF = -DEP / 2, DEP / 2

def slots():
    x = -L / 2 + EC; out = []
    for i, k in enumerate(ORDER): out.append((k, i, x + MW / 2)); x += MW
    return out

def lip_ring(x0, x1, z0, z1, y, h, mat_t=0.02, r=0.03):
    ring = rrect(x1 - x0, z1 - z0, r, 3); ring = np.vstack([ring, ring[:1]])
    return xf(thick_path(ring, mat_t, y, y + h), t=((x0 + x1) / 2, 0, (z0 + z1) / 2))

def sink(p, cx, y, mat="ceramic"):
    p.add("Sink_Basin", mat, lip_ring(cx - .22, cx + .22, -.2, .16, y, .012, .03, .06))
    p.add("Sink_Bowl", "slate", blk(cx - .19, cx + .19, y - .002, y + .004, -.17, .13, .05, 3))
    p.add("Sink_Drain", "gunmetal", cyl(cx - .1, -.02, .025, y + .004, y + .007, 10))   # spinward (-X) drain
    p.add("Sink_Tap", "alloy", cyl(cx, -.24, .015, y, y + .28, 10), blk(cx - .012, cx + .012, y + .26, y + .285, -.24, -.1, .008, 1))

def hob(p, cx, y, fence=True):
    p.add("Hob_Surface", "hobglass", blk(cx - .27, cx + .27, y, y + .008, -.25, .22, .02, 2))
    for dx, dz, R in ((-.12, -.08, .09), (.13, .06, .075)):
        p.add("Hob_InductionRings", "violet", xf(torus_ring(R, .004, 20, 3), t=(cx + dx, y + .009, dz)))
    if fence:   # pan-retention fences: low alloy posts + rails around each zone
        for dx, dz, R in ((-.12, -.08, .12), (.13, .06, .105)):
            p.add("Hob_PanFence", "alloy", *[blk(cx + dx + R * np.cos(a) - .006, cx + dx + R * np.cos(a) + .006, y, y + .03,
                  dz + R * np.sin(a) - .006, dz + R * np.sin(a) + .006, .003, 1) for a in np.linspace(0, 2 * np.pi, 4, endpoint=False) + .4])
    p.add("Hob_Status", "amber", blk(cx + .18, cx + .24, y + .008, y + .011, .17, .2, .005, 1))

def latch(p, x, y, z, mat="amber"): p.add("Latch_Lights", mat, blk(x - .03, x + .03, y - .006, y + .006, z, z + .012, .004, 1))

def fronts(p, cx, kind, y0, y1, z, mat, gap=.006, ribbed=False):
    x0, x1 = cx - MW / 2 + gap, cx + MW / 2 - gap
    if kind == "Cold":
        p.add("Module_Cold", mat, blk(x0, x1, y0, y1, z, z + .02, .012, 2)); latch(p, cx + .2, y1 - .08, z + .02, "green")
        p.add("Handles", "alloy", blk(x1 - .05, x1 - .03, y0 + .25, y1 - .15, z + .02, z + .045, .008, 1))
        return
    n = {"Store": 3, "Sink": 1, "Hob": 2}[kind]; hs = np.linspace(y0, y1, n + 1)
    for a, b in zip(hs[:-1], hs[1:]):
        p.add(f"Module_{kind}", mat, blk(x0, x1, a + gap, b - gap, z, z + .02, .01, 2))
        p.add("Handles", "alloy", blk(cx - .18, cx + .18, b - .05, b - .035, z + .02, z + .04, .006, 1))
        latch(p, cx + .24, b - .042, z + .02)
        if ribbed:
            p.add("Front_Ribs", "gunmetal", *[blk(cx + d - .006, cx + d + .006, a + .04, b - .07, z + .02, z + .03, .003, 1) for d in (-.15, 0, .15)])

def worktop(p, mat, y0, y1, r=.03, n=2, lipmat=None, front_lip=True):
    p.add("Worktop", mat, blk(-L / 2, L / 2, y0, y1, ZB, ZF, r, n))
    lm = lipmat or mat   # spin-down retention: back upstand + side rails + low front lip
    p.add("Lip", lm, blk(-L / 2, L / 2, y1, y1 + .08, ZB, ZB + .025, .008, 1),
          blk(-L / 2, -L / 2 + .02, y1, y1 + .03, ZB, ZF, .006, 1), blk(L / 2 - .02, L / 2, y1, y1 + .03, ZB, ZF, .006, 1))
    if front_lip: p.add("Lip", lm, blk(-L / 2, L / 2, y1, y1 + .012, ZF - .018, ZF, .006, 1))

def utensil_rail(p, y, z, mat="alloy", clips=6):
    p.add("Utensil_Rail", mat, blk(-1.1, .9, y, y + .02, z, z + .02, .008, 1))
    p.add("Rail_Clips", "gunmetal", *[blk(x - .01, x + .01, y - .12, y + .02, z + .015, z + .03, .004, 1) for x in np.linspace(-.9, .7, clips)])

def recycler(p, cx, y0, y1, z0=ZB, z1=ZB + .12):
    p.add("Recycler_TieIn", "gunmetal", blk(cx - .2, cx + .2, y0, y1, z0, z1, .02))
    p.add("Recycler_TieIn", "alloy", cyl(cx - .1, z0 + .06, .02, y1, TOP - .04, 8), cyl(cx + .1, z0 + .06, .02, y1, TOP - .04, 8))
    p.add("Service_Port", "amber", blk(cx + .12, cx + .17, y0 + .05, y0 + .1, z1, z1 + .01, .005, 1))

def endcaps(p, mat, y0, y1, r=.03):
    for s in (-1, 1):
        x0, x1 = sorted((s * L / 2, s * (L / 2 - EC)))
        p.add("EndCap", mat, blk(x0, x1, y0, y1, ZB, ZF - .01, r, 2))

# ---------- iterations ----------
def iter1():  # monolithic moulded white run
    p = Pod("Monolithic Moulded Run"); TY = TOP - .05
    p.add("Plinth", "gunmetal", blk(-L / 2 + .02, L / 2 - .02, 0, .1, ZB, ZF - .06, .02))
    p.add("Carcass", "white", blk(-L / 2, L / 2, .1, TY, ZB, ZF - .03, .04, 3))
    worktop(p, "white", TY, TOP - .012, .04, 3)
    for k, i, cx in slots(): fronts(p, cx, k, .12, TY - .01, ZF - .03, "white")
    p.add("Accent_Band", "violet", blk(-L / 2 + .01, L / 2 - .01, .1, .108, ZF - .065, ZF - .055, .003, 1))
    sl = dict((k, cx) for k, i, cx in slots() if k in ("Sink", "Hob")); sink(p, sl["Sink"], TOP - .012); hob(p, sl["Hob"], TOP - .012)
    recycler(p, sl["Sink"], .12, .5, ZB - .0, ZB + .1)
    utensil_rail(p, TOP + .25, ZB - .0)
    return p

def iter2():  # alloy frame + drop-in cassettes
    p = Pod("Alloy Frame + Cassettes")
    xs = [-L / 2 + EC] + [-L / 2 + EC + MW * (i + 1) for i in range(5)]
    for x in [-L / 2 + .02] + xs + [L / 2 - .02]:
        p.add("Frame", "alloy", blk(x - .02, x + .02, 0, TOP - .04, ZB, ZB + .04, .01, 1), blk(x - .02, x + .02, 0, TOP - .04, ZF - .06, ZF - .02, .01, 1))
    p.add("Frame", "alloy", blk(-L / 2, L / 2, .06, .1, ZB, ZF - .02, .01, 1), blk(-L / 2, L / 2, TOP - .08, TOP - .04, ZF - .06, ZF - .02, .01, 1))
    for k, i, cx in slots():
        p.add("Cassettes", "gunmetal", blk(cx - MW / 2 + .025, cx + MW / 2 - .025, .1, TOP - .08, ZB + .05, ZF - .07, .015, 1))
        fronts(p, cx, k, .11, TOP - .09, ZF - .07, "white", gap=.03)
    endcaps(p, "slate", .06, TOP - .04, .02)
    worktop(p, "slate", TOP - .04, TOP - .01, .015, 1, lipmat="alloy")
    sl = dict((k, cx) for k, i, cx in slots()); sink(p, sl["Sink"], TOP - .01, "alloy"); hob(p, sl["Hob"], TOP - .01)
    recycler(p, sl["Sink"], .1, .45, ZB + .05, ZB + .15)
    p.add("Accent_Band", "violet", blk(-L / 2 + .3, L / 2 - .3, TOP - .065, TOP - .055, ZF - .02, ZF - .015, .003, 1))
    utensil_rail(p, TOP + .2, ZB)
    return p

def iter3():  # galley rail system with wall-hung pods
    p = Pod("Galley Rail + Wall Pods")
    p.add("Wall_Rail", "gunmetal", blk(-L / 2, L / 2, .35, .42, ZB, ZB + .03, .01, 1), blk(-L / 2, L / 2, 1.85, 1.92, ZB, ZB + .03, .01, 1))
    p.add("Wall_Rail", "alloy", blk(-L / 2, L / 2, TOP + .3, TOP + .33, ZB, ZB + .02, .008, 1))
    for k, i, cx in slots():
        p.add("Pods_Low", "white", blk(cx - .28, cx + .28, .3 if k != "Cold" else .05, TOP - .05, ZB + .03, ZF - .04, .07, 3))
        fronts(p, cx, k, .32 if k != "Cold" else .07, TOP - .07, ZF - .04, "white", gap=.04)
        if k != "Hob":
            p.add("Pods_High", "white", blk(cx - .28, cx + .28, 1.45, 1.95, ZB + .03, ZB + .33, .06, 3))
            latch(p, cx + .2, 1.5, ZB + .33)
    p.add("Pods_High", "gunmetal", blk(.6 - .28, .6 + .28, 1.7, 1.95, ZB + .03, ZB + .4, .03, 2))   # hood pod over hob
    p.add("Accent_Band", "violet", blk(.35, .85, 1.69, 1.7, ZB + .1, ZB + .38, .003, 1))
    worktop(p, "slate", TOP - .05, TOP - .015, .03, 2, lipmat="gunmetal")
    sl = dict((k, cx) for k, i, cx in slots()); sink(p, sl["Sink"], TOP - .015); hob(p, sl["Hob"], TOP - .015)
    recycler(p, sl["Sink"], .05, .28, ZB + .03, ZB + .2)
    p.add("Feet", "gunmetal", *[cyl(x, ZF - .12, .02, 0, .3, 8) for x in (-1.6, 1.6)])
    return p

def iter4():  # island-style with recycler plinth
    p = Pod("Island + Recycler Plinth")
    p.add("Recycler_Plinth", "gunmetal", blk(-L / 2 + .05, L / 2 - .05, 0, .2, ZB + .02, ZF - .05, .04, 2))
    p.add("Accent_Band", "violet", blk(-L / 2 + .06, L / 2 - .06, .19, .2, ZF - .06, ZF - .045, .003, 1))
    p.add("Carcass", "white", blk(-L / 2 + EC, L / 2 - EC, .2, TOP - .05, ZB, ZF - .03, .02, 2))
    for k, i, cx in slots(): fronts(p, cx, k, .21, TOP - .06, ZF - .03, "white")
    for s in (-1, 1):   # waterfall slate ends
        x0, x1 = sorted((s * L / 2, s * (L / 2 - .05)))
        p.add("EndCap", "slate", blk(x0, x1, 0, TOP - .01, ZB, ZF, .02, 2))
        x0, x1 = sorted((s * (L / 2 - .05), s * (L / 2 - EC)))
        p.add("EndCap", "white", blk(x0, x1, .2, TOP - .05, ZB, ZF - .03, .02, 2))
    worktop(p, "slate", TOP - .05, TOP - .01, .03, 2, lipmat="alloy")
    sl = dict((k, cx) for k, i, cx in slots()); sink(p, sl["Sink"], TOP - .01); hob(p, sl["Hob"], TOP - .01)
    p.add("Service_Port", "amber", blk(-.3, -.2, .06, .12, ZF - .05, ZF - .04, .005, 1))
    p.add("Recycler_TieIn", "alloy", cyl(sl["Sink"], ZB + .1, .025, .2, TOP - .05, 8))
    utensil_rail(p, TOP + .05, ZB + .03)
    return p

def iter5():  # ribbed industrial-refined with overhead rack
    p = Pod("Ribbed Industrial + Overhead Rack")
    p.add("Plinth", "gunmetal", blk(-L / 2, L / 2, 0, .12, ZB, ZF - .04, .01, 1))
    p.add("Carcass", "gunmetal", blk(-L / 2 + EC, L / 2 - EC, .12, TOP - .05, ZB, ZF - .03, .015, 1))
    for k, i, cx in slots(): fronts(p, cx, k, .13, TOP - .06, ZF - .03, "white", ribbed=True)
    endcaps(p, "gunmetal", .12, TOP - .05, .015)
    worktop(p, "alloy", TOP - .05, TOP - .01, .01, 1, lipmat="gunmetal")
    sl = dict((k, cx) for k, i, cx in slots()); sink(p, sl["Sink"], TOP - .01, "alloy"); hob(p, sl["Hob"], TOP - .01)
    recycler(p, sl["Sink"], .13, .5, ZB, ZB + .1)
    for x in (-1.5, 0, 1.5): p.add("Overhead_Rack", "gunmetal", blk(x - .02, x + .02, TOP + .01, 2.0, ZB, ZB + .04, .008, 1),
                                   blk(x - .015, x + .015, 1.96, 2.0, ZB, ZB + .35, .006, 1))
    p.add("Overhead_Rack", "alloy", blk(-1.6, 1.6, 1.94, 1.97, ZB + .3, ZB + .33, .008, 1), blk(-1.6, 1.6, 1.4, 1.43, ZB + .02, ZB + .05, .008, 1))
    p.add("Rack_Hooks", "alloy", *[blk(x - .008, x + .008, 1.75, 1.94, ZB + .305, ZB + .325, .003, 1) for x in np.linspace(-1.4, 1.4, 8)])
    p.add("Accent_Band", "violet", blk(-1.6, 1.6, 1.93, 1.94, ZB + .3, ZB + .33, .003, 1))
    return p

def tonemap():
    saved = {}
    for k in ("amber", "green", "violet"):
        pm = FMAT[k]; saved[k] = pm; em = np.array(dc._col(pm.emissiveFactor)); em = em / max(em.max(), 1e-6) * 0.85
        FMAT[k] = _PBR(name=pm.name, baseColorFactor=(0, 0, 0, 1), metallicFactor=0, roughnessFactor=1, emissiveFactor=tuple(em))
    return saved

def crop(im, pad=12):
    m = (np.abs(im - im[0, 0]).sum(2) > .02); ys, xs = np.where(m)
    if not len(ys): return im
    return im[max(ys.min() - pad, 0):ys.max() + pad, max(xs.min() - pad, 0):xs.max() + pad]

def main():
    os.makedirs(OUT, exist_ok=True); isos = []; rows = []
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        p = fn(); tris, geo = export_final(p.P, [os.path.join(OUT, f"iter_0{i}.glb")])
        V = np.vstack([g[1] for g in geo.values()]); rows.append((i, p.name, tris, V.min(0).round(3), V.max(0).round(3)))
        saved = tonemap(); top, front, side, iso = views()
        ims = [crop(render_view(geo, R, size=s, shadow=sh)) for R, s, sh in ((top, 900, False), (front, 900, True), (side, 520, True), (iso, 820, True))]
        FMAT.update(saved); isos.append((p.name, ims[3]))
        bg = "#F4F2EC"; fig = plt.figure(figsize=(14, 9), facecolor=bg); gs = fig.add_gridspec(2, 3, width_ratios=[1, 1, 0.55], height_ratios=[1, 1.25])
        for ax, im, t in ((fig.add_subplot(gs[0, :2]), ims[0], "Top"), (fig.add_subplot(gs[0, 2]), ims[2], "Side"),
                          (fig.add_subplot(gs[1, 0]), ims[1], "Front"), (fig.add_subplot(gs[1, 1:]), ims[3], "Iso")):
            ax.imshow(im); ax.axis("off"); ax.set_title(t, y=-0.1, fontsize=11, color="#555")
        fig.suptitle(f"iter_0{i}  {p.name}", fontsize=12, color="#444"); plt.tight_layout()
        fig.savefig(os.path.join(OUT, f"iter_0{i}_sheet.png"), dpi=100, facecolor=bg); plt.close(fig)
    fig, axs = plt.subplots(2, 3, figsize=(18, 9), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)):
        ax.imshow(im); ax.set_title(f"{i}. {n}", y=-0.12, fontsize=11, color="#555")
    plt.tight_layout(); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)
    for r in rows: print(*r)

# ---------- final: polished Galley Rail + Wall Pods (iter_03) ----------
def bev(w, d, y0, y1, r, e=0.012, n=3, cx=0, cz=0):
    """Rounded-plan slab with chamfer-bevelled top and bottom edges (closed loft)."""
    sx, sz = 1 - 2 * e / w, 1 - 2 * e / d
    return xf(loft(rrect(w, d, r, min(n, 2)), [(y0, sx, sz), (y0 + e, 1, 1), (y1 - e, 1, 1), (y1, sx, sz)]), t=(cx, 0, cz))

def box(x0, x1, y0, y1, z0, z1):   # 16-tri closed box for small hardware
    return xf(loft(np.array([(x1 - x0) / 2, (z1 - z0) / 2]) * np.array([(1, 1), (-1, 1), (-1, -1), (1, -1)]), [(y0, 1, 1), (y1, 1, 1)]), t=((x0 + x1) / 2, 0, (z0 + z1) / 2))

def ffronts(p, cx, kind, y0, y1, z, gap=.008):
    x0, x1 = cx - (MW - .05) / 2 + gap, cx + (MW - .05) / 2 - gap
    n = {"Cold": 1, "Store": 3, "Sink": 1, "Hob": 2}[kind]; hs = np.linspace(y0, y1, n + 1)
    for a, b in zip(hs[:-1], hs[1:]):
        p.add(f"Module_{kind}", "white", blk(x0, x1, a + gap, b - gap, z, z + .02, .012, 1))
        hx = (x1 - .05, x1 - .03, a + .1, b - .12) if kind == "Cold" else (cx - .17, cx + .17, b - .055, b - .04)
        p.add("Handles", "alloy", box(hx[0], hx[1], hx[2], hx[3], z + .02, z + .038))
        p.add("Latch_Lights", "green" if kind == "Cold" else "amber", box(cx + .2, cx + .25, b - .05, b - .038, z + .02, z + .03))

def bolt(x, y, z):   # bolt head on the strongback face (+Z)
    return box(x - .014, x + .014, y - .014, y + .014, z, z + .012)

def final_wallpods():
    FMAT["white"] = _PBR(name="WhiteComposite", baseColorFactor=(0.92, 0.93, 0.94, 1), metallicFactor=0.0, roughnessFactor=0.35)
    FMAT["lamp"] = _PBR(name="HoodLight", baseColorFactor=(1, .95, .85, 1), metallicFactor=0, roughnessFactor=.4, emissiveFactor=(1, .92, .78))
    p = Pod("Galley Rail + Wall Pods (final)"); WZ = ZB + .025; TY = TOP - .04
    # strongback on the wall plane + rails
    p.add("Strongback", "gunmetal", bev(L, .025, .22, 2.0, .008, .006, 1, 0, ZB + .0125))
    p.add("Wall_Rail", "alloy", *[blk(-L / 2 + .02, L / 2 - .02, y, y + .045, WZ, WZ + .03, .012, 1) for y in (.62, 1.86)])
    p.add("Utensil_Rail", "alloy", bev(2.0, .02, TOP + .3, TOP + .32, .009, .004, 2, -.2, WZ + .01))
    p.add("Rail_Clips", "gunmetal", *[box(x - .01, x + .01, TOP + .19, TOP + .33, WZ + .015, WZ + .03) for x in np.linspace(-1.0, .6, 5)])
    # cleats every 0.6 m at module joints, bolted
    joints = [-L / 2 + EC + MW * k for k in range(6)]
    for x in joints:
        p.add("Cleats", "gunmetal", box(x - .011, x + .011, .28, TY, WZ, ZB + DEP - .07),
              box(x - .035, x + .035, .28, TY, WZ, WZ + .02), box(x - .025, x + .025, 1.38, 1.98, WZ, WZ + .02))
        p.add("Bolt_Heads", "alloy", *[bolt(x + d, y, WZ + .02) for y in (.36, 1.46) for d in (0,)])
    # low pods (hung, no floor contact) + high pods + hood
    for k, i, cx in slots():
        y0 = .16 if k == "Cold" else .3
        p.add("Pods_Low", "white", bev(MW - .05, DEP - .1, y0, TY - .005, .05, .015, 3, cx, WZ + (DEP - .1) / 2))
        ffronts(p, cx, k, y0 + .02, TY - .02, WZ + DEP - .1)
        p.add("Hook_Clamps", "gunmetal", *[box(cx + d - .04, cx + d + .04, .6, .7, WZ + .03, WZ + .07) for d in (0,)])
        if k == "Hob":
            p.add("Hood", "white", bev(MW - .05, .42, 1.55, 1.98, .05, .015, 3, cx, WZ + .21))
            p.add("Hood_Vent", "gunmetal", bev(MW - .14, .03, 1.545, 1.552, .008, .002, 1, cx, WZ + .37))
            p.add("Hood_Light", "lamp", bev(MW - .14, .02, 1.545, 1.551, .006, .002, 1, cx, WZ + .3))
            p.add("Accent_Band", "violet", bev(MW - .06, .006, 1.6, 1.61, .002, .001, 1, cx, WZ + .423))
        else:
            p.add("Pods_High", "white", bev(MW - .05, .33, 1.42, 1.98, .05, .015, 3, cx, WZ + .165))
            p.add("Latch_Lights", "amber", box(cx + .17, cx + .23, 1.465, 1.477, WZ + .33, WZ + .34))
        p.add("Hook_Clamps", "gunmetal", *[box(cx + d - .04, cx + d + .04, 1.84, 1.94, WZ + .03, WZ + .07) for d in (0,)])
    for s in (-1, 1):   # end caps: hung white returns
        cx = s * (L / 2 - EC / 2); p.add("EndCap", "white", bev(EC - .03, DEP - .1, .3, TY - .005, .04, .012, 3, cx, WZ + (DEP - .1) / 2))
    # worktop with a real sink opening (4 slabs) + lips
    sx0, sx1, sz0, sz1 = -.22, .22, -.2, .16
    for a, b, c, d in ((-L / 2, sx0, ZB, ZF), (sx1, L / 2, ZB, ZF), (sx0, sx1, ZB, sz0), (sx0, sx1, sz1, ZF)):
        p.add("Worktop", "slate", blk(a, b, TY, TOP, c, d, .004, 1))
    p.add("Worktop_Edge", "slate", blk(-L / 2, L / 2, TY - .005, TOP, ZF - .03, ZF, .012, 1))
    p.add("Lip", "gunmetal", box(-L / 2, L / 2, TOP, TOP + .08, ZB, ZB + .025), box(-L / 2, -L / 2 + .02, TOP, TOP + .03, ZB + .025, ZF),
          box(L / 2 - .02, L / 2, TOP, TOP + .03, ZB + .025, ZF), box(-L / 2 + .02, L / 2 - .02, TOP, TOP + .012, ZF - .018, ZF))
    ring = rrect(sx1 - sx0, sz1 - sz0, .04, 3); ring = np.vstack([ring, ring[:1]])
    p.add("Sink_Basin", "alloy", xf(thick_path(ring, .012, TOP - .2, TOP + .004), t=(0, 0, (sz0 + sz1) / 2)),
          blk(sx0 + .005, sx1 - .005, TOP - .21, TOP - .19, sz0 + .005, sz1 - .005, .04, 3))
    p.add("Sink_Drain", "gunmetal", cyl(-.1, -.02, .025, TOP - .19, TOP - .186, 10))      # spinward (-X)
    p.add("Sink_Tap", "alloy", cyl(0, -.24, .015, TOP, TOP + .28, 10), blk(-.012, .012, TOP + .26, TOP + .285, -.24, -.1, .008, 1))
    cx, y = .6, TOP   # hob: slate-glass panel, violet induction rings, alloy pan fences (box posts), amber status
    p.add("Hob_Surface", "hobglass", blk(cx - .27, cx + .27, y, y + .008, -.25, .22, .02, 1))
    for dx, dz, R in ((-.12, -.08, .09), (.13, .06, .075)):
        p.add("Hob_InductionRings", "violet", xf(torus_ring(R, .004, 12, 3), t=(cx + dx, y + .009, dz)))
        for a in np.linspace(0, 2 * np.pi, 4, endpoint=False) + .4:
            px, pz = cx + dx + (R + .03) * np.cos(a), dz + (R + .03) * np.sin(a)
            p.add("Hob_PanFence", "alloy", box(px - .006, px + .006, y, y + .03, pz - .006, pz + .006))
    p.add("Hob_Status", "amber", box(cx + .18, cx + .24, y + .008, y + .011, .17, .2))
    recycler(p, 0, .3, .5, WZ, WZ + .12)
    return p

def final_main():
    p = final_wallpods(); gp = os.path.join(dc.ROOT, "godot/assets/models/kitchen_counter_wallpods.glb")
    tris, geo = export_final(p.P, [gp]); V = np.vstack([g[1] for g in geo.values()])
    bad = [n for n, (mk, m) in p.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    print("tris", tris, "bounds", V.min(0).round(3), V.max(0).round(3), "non-watertight:", bad)
    saved = tonemap(); top, front, side, iso = views(); bgc = np.array([0.955, 0.948, 0.925])
    def rv(R, s, sh):
        im = render_view(geo, R, size=s, shadow=sh); ns = render_view(geo, R, size=s, shadow=False) if sh else im
        fg = np.abs(ns - ns[0, 0]).sum(2) > .03            # object mask (no contact shadow)
        im[fg] = np.clip(im[fg] * 1.12 + .02, 0, 1); return crop(im)       # sheet-only exposure lift
    ims = [rv(top, 900, False), rv(front, 900, True), rv(side, 520, True), rv(iso, 820, True)]; FMAT.update(saved)
    bg = "#F4F2EC"; fig = plt.figure(figsize=(14, 9), facecolor=bg); gs = fig.add_gridspec(2, 3, width_ratios=[1, 1, 0.55], height_ratios=[1, 1.25])
    for ax, im, t in ((fig.add_subplot(gs[0, :2]), ims[0], "Top"), (fig.add_subplot(gs[0, 2]), ims[2], "Side"),
                      (fig.add_subplot(gs[1, 0]), ims[1], "Front"), (fig.add_subplot(gs[1, 1:]), ims[3], "Iso")):
        ax.imshow(im); ax.axis("off"); ax.set_title(t, y=-0.1, fontsize=11, color="#555")
    fig.suptitle("Final  Galley Rail + Wall Pods", fontsize=12, color="#444"); plt.tight_layout()
    fig.savefig(os.path.join(OUT, "final_wallpods_sheet.png"), dpi=100, facecolor=bg); plt.close(fig)

if __name__ == "__main__":
    final_main() if len(sys.argv) > 1 and sys.argv[1] == "final" else main()
