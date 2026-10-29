#!/usr/bin/env python3
"""Table family (#10 small dining 1.2x0.8x0.75, #11 dining-4 1.6x0.9x0.75, #12 tea 1.2x0.8x0.45) - 5 family iterations.
Owner: Rook. Length along X, width along Z, Y up, pivot bottom-center, front +Z. Each family shares one design language
across the 3 sizes. Chair fit is checked numerically against godot/assets/models/dining_chair_swivel.glb (floor-clamped
swivel: plate 0.34 sq, foot ring r0.181 @ y0.19-0.21, seat top 0.479). Outputs design/assets/table_family/."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dining_chair_generator as dc
from dining_chair_generator import xf, export_final, render_view, FMAT
from bath_pod_generator import blk, cyl, Pod, views
from kitchen_counter_generator import bev, box, crop, tonemap
from trimesh.visual.material import PBRMaterial as _PBR
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(dc.ROOT, "design/assets/table_family")
FMAT.update({
 "white": _PBR(name="WhiteComposite", baseColorFactor=(0.92, 0.93, 0.94, 1), metallicFactor=0.0, roughnessFactor=0.35),
 "slate": _PBR(name="Slate", baseColorFactor=(0.30, 0.33, 0.38, 1), metallicFactor=0.2, roughnessFactor=0.55),
 "green": _PBR(name="StatusGreen", baseColorFactor=(0.247, 0.686, 0.416, 1), metallicFactor=0.0, roughnessFactor=0.4, emissiveFactor=(0.247, 0.686, 0.416)),
})
SIZES = [("small_dining", 1.2, 0.8, 0.75), ("dining4", 1.6, 0.9, 0.75), ("tea", 1.2, 0.8, 0.45)]
TT = 0.035   # top thickness

def clamp(p, x, z, sx=.16, sz=.16, top=.06, nm="Clamp"):
    p.add("FloorPlates", "gunmetal", box(x - sx / 2, x + sx / 2, 0, .012, z - sz / 2, z + sz / 2))
    p.add(f"{nm}s", "gunmetal", box(x - sx / 4, x + sx / 4, .012, top, z - sz / 4, z + sz / 4))
    p.add("Clamp_Bolts", "alloy", *[box(x + dx - .01, x + dx + .01, .012, .02, z + dz - .01, z + dz + .01) for dx, dz in ((-sx * .38, -sz * .38), (sx * .38, sz * .38))])
    p.add("Clamp_Lights", "amber", box(x - .02, x + .02, .03, .045, z + sz / 4, z + sz / 4 + .005))

def port(p, x, y, z, nx=0):   # Sprocket service / charge port (amber)
    p.add("Service_Port", "gunmetal", box(x - .05, x + .05, y - .04, y + .04, z, z + .01))
    p.add("Service_Port_Light", "amber", box(x - .02, x + .02, y - .015, y + .015, z + .01, z + .014))

def fam1(L, Wd, Ht):   # moulded pedestal(s), recessed plate + tucked clamps
    p = Pod("Moulded Pedestal")
    p.add("Top", "white", bev(L, Wd, Ht - TT, Ht, .1, .012, 3))
    p.add("Top_Edge_Band", "violet", box(-L / 2 + .15, L / 2 - .15, Ht - TT + .004, Ht - TT + .01, Wd / 2 - .002, Wd / 2 + .001))
    xs = (0,) if L < 1.4 else (-.4, .4)
    for x in xs:
        p.add("Pedestal", "white", bev(.18, .14, .06, Ht - TT, .06, .02, 3, x, 0))
        p.add("Pedestal_Base", "gunmetal", bev(.34, .22, 0, .06, .08, .015, 2, x, 0))
        clamp(p, x - .12, 0, .1, .14); clamp(p, x + .12, 0, .1, .14)
    port(p, xs[-1] + .09, min(.3, Ht * .5), -.07 + .0, 0) if False else port(p, xs[0], min(.3, Ht * .55), .07)
    return p

def fam2(L, Wd, Ht):   # alloy four-leg frame, gunmetal apron, bolted feet
    p = Pod("Alloy Frame + Apron")
    p.add("Top", "slate", bev(L, Wd, Ht - TT, Ht, .03, .008, 2))
    p.add("Top_Edge", "alloy", box(-L / 2, L / 2, Ht - TT - .006, Ht - TT, -Wd / 2, Wd / 2))
    ap = .06 if Ht > .6 else .04
    p.add("Apron", "gunmetal", box(-L / 2 + .06, L / 2 - .06, Ht - TT - ap, Ht - TT - .006, -Wd / 2 + .08, -Wd / 2 + .1),
          box(-L / 2 + .06, L / 2 - .06, Ht - TT - ap, Ht - TT - .006, Wd / 2 - .1, Wd / 2 - .08))
    for sx in (-1, 1):
        x = sx * (L / 2 - .05)
        p.add("Apron", "gunmetal", box(x - .01, x + .01, Ht - TT - ap, Ht - TT - .006, -Wd / 2 + .08, Wd / 2 - .08))
        for sz in (-1, 1):
            z = sz * (Wd / 2 - .09)
            p.add("Legs", "alloy", cyl(x, z, .022, .012, Ht - TT - .006, 10))
            p.add("Foot_Plates", "gunmetal", box(x - .045, x + .045, 0, .012, z - .045, z + .045))
            p.add("Foot_Bolts", "alloy", box(x - .01, x + .01, .012, .02, z - .035, z - .015), box(x - .01, x + .01, .012, .02, z + .015, z + .035))
    p.add("Accent_Band", "violet", box(-.2, .2, Ht - TT - .03, Ht - TT - .022, Wd / 2 - .08, Wd / 2 - .077))
    port(p, L / 2 - .04, Ht - TT - ap / 2 - .003, -.05) if False else port(p, 0, Ht - TT - ap / 2 - .003, Wd / 2 - .08)
    return p

def fam3(L, Wd, Ht):   # wall-rail anchored at -X end + single clamped T-leg at +X
    p = Pod("Wall-Rail End + T-Leg"); WX = -L / 2
    p.add("Top", "white", bev(L, Wd, Ht - TT, Ht, .06, .012, 3))
    p.add("Wall_Plate", "gunmetal", box(WX - .02, WX, .1, Ht + .1, -Wd / 2 + .05, Wd / 2 - .05))
    p.add("Wall_Rail", "alloy", box(WX, WX + .03, Ht - .1, Ht - .06, -Wd / 2 + .08, Wd / 2 - .08))
    p.add("Hook_Clamps", "gunmetal", *[box(WX + .03, WX + .07, Ht - .11, Ht - TT, z - .05, z + .05) for z in (-Wd / 4, Wd / 4)])
    p.add("Brackets", "gunmetal", *[box(WX, WX + .25, Ht - TT - .05, Ht - TT, z - .01, z + .01) for z in (-Wd / 4, Wd / 4)])
    p.add("Bracket_Bolts", "alloy", *[box(WX - .03, WX - .02, y - .012, y + .012, z - .012, z + .012) for y in (.25, Ht - .02) for z in (-Wd / 4, Wd / 4)])
    x = L / 2 - .12
    p.add("T_Leg", "gunmetal", box(x - .03, x + .03, .06, Ht - TT, -.03, .03), box(x - .03, x + .03, Ht - TT - .05, Ht - TT, -Wd / 2 + .1, Wd / 2 - .1))
    p.add("T_Foot", "alloy", bev(.08, Wd - .3, .012, .06, .02, .008, 2, x, 0))
    clamp(p, x, -(Wd / 2 - .2), .12, .1); clamp(p, x, Wd / 2 - .2, .12, .1)
    p.add("Accent_Band", "violet", box(x - .031, x - .03, .2, Ht - TT - .1, -.01, .01))
    port(p, WX + .005, .45 if Ht > .6 else .25, -.0) if False else port(p, x, .3 if Ht > .6 else .2, .03)
    return p

def fam4(L, Wd, Ht):   # moulded slab end legs + high stretcher + tucked clamps
    p = Pod("Slab Ends + Stretcher")
    p.add("Top", "white", bev(L, Wd, Ht - TT, Ht, .04, .012, 3))
    for sx in (-1, 1):
        x = sx * (L / 2 - .085)
        p.add("Slab_Legs", "white", bev(.05, Wd - .16, .05, Ht - TT, .02, .01, 2, x, 0))
        p.add("Slab_Feet", "gunmetal", bev(.09, Wd - .12, 0, .05, .02, .008, 2, x, 0))
        clamp(p, x, -(Wd / 2 - .13), .08, .08, .05); clamp(p, x, Wd / 2 - .13, .08, .08, .05)
    sy = Ht - TT - (.12 if Ht > .6 else .08)
    p.add("Stretcher", "gunmetal", bev(L - .22, .06, sy, sy + .05, .015, .006, 2, 0, 0))
    p.add("Accent_Band", "violet", box(-L / 2 + .2, L / 2 - .2, sy + .02, sy + .028, .03, .033))
    port(p, 0, sy + .025, .03 + .003) if False else port(p, L / 2 - .11, .25 if Ht > .6 else .2, .0)
    return p

def fam5(L, Wd, Ht):   # torsion-box spine + forked alloy feet + Sprocket service bay in spine
    p = Pod("Spine Beam + Fork Feet")
    p.add("Top", "slate", bev(L, Wd, Ht - TT, Ht, .05, .01, 2))
    p.add("Top_Inlay", "alloy", box(-L / 2 + .06, L / 2 - .06, Ht - .001, Ht + .001, -.01, .01))
    sy = Ht - TT - .1
    p.add("Spine", "gunmetal", bev(L - .3, .12, sy, Ht - TT, .02, .008, 2, 0, 0))
    p.add("Spine_Light", "green", box(-.25, .25, sy + .04, sy + .05, .06, .064))
    for sx in (-1, 1):
        x = sx * (L / 2 - .18)
        p.add("Fork_Posts", "alloy", bev(.06, .06, .05, sy, .015, .006, 2, x, 0))
        p.add("Fork_Feet", "alloy", bev(.06, Wd - .24, 0, .05, .02, .008, 2, x, 0))
        clamp(p, x, -(Wd / 2 - .16), .1, .08, .05); clamp(p, x, Wd / 2 - .16, .1, .08, .05)
    port(p, 0, sy + .05, .06)
    return p

FAMS = [fam1, fam2, fam3, fam4, fam5]

# ---------- swivel chair (approved glb) for fit checks + iso ----------
CH_MAT = {"FloorPlate": "gunmetal", "LockLight": "amber", "Column": "alloy", "SwivelHub": "gunmetal", "FootRing": "alloy",
          "Seat_Pan": "alloy", "Seat_Cushion": "fabric", "BackSpine": "alloy", "Back_Panel": "gunmetal", "AccentInset": "violet"}
def chair_geo(x, z, face_minus_z):
    sc = trimesh.load(os.path.join(dc.ROOT, "godot/assets/models/dining_chair_swivel.glb")); out = {}
    R = trimesh.transformations.rotation_matrix(np.pi if face_minus_z else 0, [0, 1, 0])
    for n, g in sc.geometry.items():
        m = g.copy(); m.apply_transform(R); m.apply_translation((x, 0, z))
        out[f"Chair_{x:.2f}_{z:.2f}_{n}"] = (CH_MAT.get(n, "alloy"), np.array(m.vertices), np.array(m.vertex_normals), np.array(m.faces))
    return out

def chair_spots(L, Wd):
    xs = (-.27, .27) if L < 1.4 else (-.4, .4)
    return [(x, sz * (Wd / 2 + .16), sz > 0) for x in xs for sz in (-1, 1)]   # seat front 0.055 under the top edge

def fit_check(p, L, Wd, Ht):
    V = [np.asarray(m.vertices) for _, m in p.P.values()]; V = np.vstack(V)
    res = {"seat_to_top": round(Ht - .479, 3)}
    knee, plate = [], []
    for x, z, _ in chair_spots(L, Wd):
        zin = np.sign(z) * Wd / 2
        kz = (np.abs(V[:, 0] - x) < .225) & (np.abs(V[:, 2]) > abs(zin) - .3) & (np.abs(V[:, 2]) <= abs(zin)) & (V[:, 1] > .25) & (V[:, 1] < Ht - TT - .001) & (np.sign(V[:, 2]) == np.sign(z))
        knee.append(min(V[kz, 1].min(), Ht - TT) - .479 if kz.any() else Ht - TT - .479)
        low = V[V[:, 1] < .22]   # chair plate (0.34 sq) + foot ring (r .181) zone
        dx = np.maximum(np.abs(low[:, 0] - x) - .181, 0); dz = np.maximum(np.abs(low[:, 2] - z) - .181, 0)
        plate.append(np.sqrt(dx ** 2 + dz ** 2).min() if len(low) else 9)
    res["thigh_clear_min"] = round(min(knee), 3); res["chair_base_clear_min"] = round(min(plate), 3)
    return res

def render_set(geo, s=330):
    top, front, side, iso = views(); out = []
    for R, sh in ((top, False), (front, True), (side, True), (iso, True)):
        im = render_view(geo, R, size=s, shadow=sh); ns = render_view(geo, R, size=s, shadow=False) if sh else im
        fg = np.abs(ns - ns[0, 0]).sum(2) > .03; im[fg] = np.clip(im[fg] * 1.12 + .02, 0, 1); out.append(crop(im))
    return out

def main():
    os.makedirs(OUT, exist_ok=True); isos = []; rows = []
    for i, fam in enumerate(FAMS, 1):
        bg = "#F4F2EC"; fig, axs = plt.subplots(3, 4, figsize=(16, 11), facecolor=bg); saved = None
        for r, (nm, L, Wd, Ht) in enumerate(SIZES):
            p = fam(L, Wd, Ht); tris, geo = export_final(p.P, [os.path.join(OUT, f"iter_0{i}_{nm}.glb")])
            bad = [n for n, (mk, m) in p.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
            fit = fit_check(p, L, Wd, Ht) if Ht > .6 else {"seat_to_top": "n/a (tea)"}
            rows.append((i, p.name, nm, tris, fit, bad))
            saved = tonemap(); ims = render_set(geo)
            if nm == "dining4":
                g2 = dict(geo)
                for x, z, f in chair_spots(L, Wd): g2.update(chair_geo(x, z, f))
                ims[3] = render_set(g2, 420)[3]; isos.append((p.name, ims[3]))
            FMAT.update(saved)
            for c, (im, t) in enumerate(zip(ims, ("Top", "Front", "Side", "Iso" + (" + swivel chairs" if nm == "dining4" else "")))):
                ax = axs[r, c]; ax.imshow(im); ax.axis("off"); ax.set_title(f"{nm.replace('_', ' ')} - {t}", y=-0.14, fontsize=9, color="#555")
        fig.suptitle(f"iter_0{i}  {p.name}", fontsize=12, color="#444"); plt.tight_layout()
        fig.savefig(os.path.join(OUT, f"iter_0{i}_sheet.png"), dpi=90, facecolor=bg); plt.close(fig)
    fig, axs = plt.subplots(2, 3, figsize=(18, 10), facecolor="#F4F2EC")
    for ax in axs.flat: ax.axis("off")
    for ax, (i, (n, im)) in zip(axs.flat, enumerate(isos, 1)): ax.imshow(im); ax.set_title(f"{i}. {n} (dining for 4 + swivel chairs)", y=-0.1, fontsize=11, color="#555")
    plt.tight_layout(); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)
    for r in rows: print(*r)

# ---------- final: polished Moulded Pedestal (family 1), all 3 sizes ----------
from dining_chair_generator import loft, rrect
def ped_column(x, y0, y1, w=.18, d=.14, r=.06):
    """Pedestal with flared fillets top and bottom (smooth loft)."""
    h = y1 - y0; rings = [(y0, 1.25, 1.3), (y0 + .02, 1.1, 1.12), (y0 + .05, 1, 1), (y1 - .05, 1, 1), (y1 - .02, 1.1, 1.12), (y1, 1.22, 1.28)]
    return xf(loft(rrect(w, d, r, 4), rings), t=(x, 0, 0))

def final_pedestal(L, Wd, Ht, tag):
    p = Pod(f"Moulded Pedestal {tag}")
    p.add("Top", "white", bev(L, Wd, Ht - TT, Ht, .1, .014, 4))
    p.add("Top_Underside", "gunmetal", bev(L - .12, Wd - .12, Ht - TT - .006, Ht - TT, .07, .002, 3))
    p.add("Top_EdgeBand", "violet", box(-L / 2 + .15, L / 2 - .15, Ht - TT + .006, Ht - TT + .012, Wd / 2 - .002, Wd / 2 + .001))
    xs = (0,) if L < 1.4 else (-.4, .4)
    for k, x in enumerate(xs, 1):
        p.add(f"Pedestal_{k}", "white", ped_column(x, .06, Ht - TT - .006))
        p.add(f"Pedestal_Base_{k}", "gunmetal", bev(.34, .22, 0, .06, .08, .015, 3, x, 0))
        for side, dx in (("L", -.12), ("R", .12)):
            cx = x + dx
            p.add(f"FloorPlate_{k}{side}", "gunmetal", bev(.1, .15, 0, .012, .02, .004, 1, cx, 0))
            p.add(f"Clamp_{k}{side}", "gunmetal", box(cx - .025, cx + .025, .012, .075, -.04, .04))
            p.add("Clamp_Bolts", "alloy", *[box(cx - .01, cx + .01, .012, .02, z - .01, z + .01) for z in (-.06, .06)])
            p.add("Clamp_Lights", "amber", box(cx - .015, cx + .015, .045, .06, .04, .044))
    p.add("Service_Port", "gunmetal", bev(.1, .01, min(.26, Ht * .5), min(.34, Ht * .5 + .08), .015, .003, 2, xs[0], .072))
    p.add("Service_Port_Light", "amber", box(xs[0] - .02, xs[0] + .02, min(.29, Ht * .5 + .03), min(.31, Ht * .5 + .05), .077, .081))
    return p

def final_main():
    from PIL import Image, ImageDraw, ImageFont
    names = {"small_dining": "table_pedestal_small", "dining4": "table_pedestal_dining4", "tea": "table_pedestal_tea"}
    top, front, side, iso = views(); VIEWS = [("Top", top, False), ("Front", front, True), ("Side", side, True), ("Iso", iso, True)]
    PX = 300   # common scale: pixels per metre for every view of every size
    rows = []
    for nm, L, Wd, Ht in SIZES:
        p = final_pedestal(L, Wd, Ht, nm); gp = os.path.join(dc.ROOT, "godot/assets/models", names[nm] + ".glb")
        tris, geo = export_final(p.P, [gp]); V = np.vstack([g[1] for g in geo.values()])
        bad = [n for n, (mk, m) in p.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
        fit = fit_check(p, L, Wd, Ht) if Ht > .6 else "n/a"
        print(nm, "tris", tris, "dims", (V.max(0) - V.min(0)).round(3), "fit", fit, "bad", bad)
        saved = tonemap(); ims = []
        for t, R, sh in VIEWS:
            P = V @ R.T; span = (P[:, :2].max(0) - P[:, :2].min(0)).max() * 1.25; size = int(round(span * PX))
            im = render_view(geo, R, size=size, shadow=sh); ns = render_view(geo, R, size=size, shadow=False) if sh else im
            fg = np.abs(ns - ns[0, 0]).sum(2) > .03; im[fg] = np.clip(im[fg] * 1.12 + .02, 0, 1); ims.append((t, crop(im)))
        FMAT.update(saved); rows.append((nm, ims))
    bg = (244, 242, 236); font = ImageFont.truetype("DejaVuSans.ttf", 22); gap, lab = 30, 26
    colw = [max(r[1][c][1].shape[1] for r in rows) for c in range(4)]
    rowh = [max(im.shape[0] for _, im in r[1]) for r in rows]
    Wc = sum(colw) + gap * 5 + 170; Hc = sum(rowh) + (gap + lab) * 3 + 60
    canvas = Image.new("RGB", (Wc, Hc), bg); d = ImageDraw.Draw(canvas)
    d.text((Wc // 2 - 300, 12), "Final  Moulded Pedestal tables (common scale)", fill=(70, 70, 70), font=font)
    y = 50
    for (nm, ims), rh in zip(rows, rowh):
        d.text((10, y + rh // 2), {"small_dining": "Small dining", "dining4": "Dining for 4", "tea": "Tea"}[nm], fill=(85, 85, 85), font=font)
        x = 170
        for (t, im), cw in zip(ims, colw):
            pim = Image.fromarray((np.clip(im, 0, 1) * 255).astype(np.uint8))
            ox, oy = x + (cw - pim.width) // 2, y + rh - pim.height     # bottom-aligned (shared ground line)
            canvas.paste(pim, (ox, oy)); d.text((x + cw // 2 - 25, y + rh + 6), t, fill=(85, 85, 85), font=font)
            x += cw + gap
        y += rh + lab + gap
    canvas.save(os.path.join(OUT, "final_pedestal_sheet.png"))

if __name__ == "__main__":
    final_main() if len(sys.argv) > 1 and sys.argv[1] == "final" else main()
