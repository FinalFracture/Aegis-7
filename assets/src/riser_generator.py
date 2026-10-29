"""Rev C asset #7: riser shaft + sealed wall chase, stair core / rev C v1.1 position.
Origin = building plan origin (same as #3-#5): X axial, Y up from the L1 finished floor, +Z spinward.
Footprint X 0.6..1.6, Z 2.4..3.4 (RISER in residential_stair_core_v1.py / residential_floorplan_rev_c.py), Y 0..8.8 (L1 floor to roof soffit),
the same XZ on L1 (Maintenance) and L2 (202). It shares its south face Z 2.4 with the lift #51 shaft (X 0.6..2.2, Z 0.8..2.4).
Access panels are on the east face X 1.6 (into Maintenance on L1 and into 202 on L2)."""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import dining_chair_generator as dc
from dining_chair_generator import export_final, shade_split, render_view, FMAT
from bath_pod_generator import Pod, cyl
from kitchen_counter_generator import box, crop, tonemap
from wardrobe_generator import roty
from stair_guard_generator import render_sheet
OUT = os.path.join(dc.ROOT, "design/assets/riser")
X0, X1, Z0, Z1, H = .6, 1.6, 2.4, 3.4, 8.8; WT = .04; L2 = 4.2; SLAB = (3.9, 4.2)
LEVELS = [(0.0, "L1"), (L2, "L2")]; PZ = (2.55, 3.25); PY = (.15, 2.05)       # access panel opening (per level, relative Y)

def build(open_deg=0.0):
    p = Pod("Riser_Shaft")
    # sealed composite shell; the east wall has an opening behind each access panel
    p.add("Chase_Shell", "white", box(X0, X0 + WT, 0, H, Z0, Z1), box(X0 + WT, X1, 0, H, Z0, Z0 + WT), box(X0 + WT, X1, 0, H, Z1 - WT, Z1))
    ys = [0]
    for y, _ in LEVELS: ys += [y + PY[0], y + PY[1]]
    ys.append(H); east = []
    for k in range(0, len(ys), 2): east.append(box(X1 - WT, X1, ys[k], ys[k + 1], Z0 + WT, Z1 - WT))
    for y, _ in LEVELS:
        east += [box(X1 - WT, X1, y + PY[0], y + PY[1], Z0 + WT, PZ[0]), box(X1 - WT, X1, y + PY[0], y + PY[1], PZ[1], Z1 - WT)]
    p.add("Chase_Shell_East", "white", *east)
    # fire stops at the L2 slab crossing and the roof soffit (intumescent collar plate, gunmetal)
    p.add("Fire_Stops", "gunmetal", box(X0 + WT, X1 - WT, *SLAB, Z0 + WT, Z1 - WT) if False else box(X0 + WT, X1 - WT, SLAB[0], SLAB[0] + .05, Z0 + WT, Z1 - WT),
          box(X0 + WT, X1 - WT, SLAB[1] - .05, SLAB[1], Z0 + WT, Z1 - WT), box(X0 + WT, X1 - WT, H - .05, H, Z0 + WT, Z1 - WT), box(X0 + WT, X1 - WT, 0, .04, Z0 + WT, Z1 - WT))
    # services (pass through the fire-stop plates): water + reclaim, power bundle, data, air duct
    xi, zi = X0 + WT, Z0 + WT
    runs = [("Water_Pipe", "alloy", .78, 2.62, .045), ("Reclaim_Pipe", "white", .78, 2.80, .045), ("Power_Conduits", "gunmetal", .70, 3.0, .028),
            ("Power_Conduits", "gunmetal", .70, 3.07, .028), ("Power_Conduits", "gunmetal", .70, 3.14, .028)]
    for n, mk, x, z, r in runs: p.add(n, mk, cyl(x, z, r, .04, H - .05, 12))
    p.add("Data_Conduits", "violet", *[cyl(.94, z, .016, .04, H - .05, 8) for z in (2.98, 3.04, 3.10, 3.16)])
    p.add("Air_Duct", "alloy", box(1.05, 1.3, .04, H - .05, 3.0, 3.3))
    # spin-down: clamp rails every ~1.1 m, gripping every run against the west wall
    for y in np.arange(.6, H - .3, 1.1):
        if SLAB[0] - .1 < y < SLAB[1] + .1: continue
        p.add("Clamp_Rails", "gunmetal", box(xi, 1.34, y - .02, y + .02, Z1 - WT - .05, Z1 - WT), box(xi, 1.0, y - .02, y + .02, zi, zi + .04),
              box(xi, xi + .06, y - .02, y + .02, zi + .04, Z1 - WT - .05))
        p.add("Clamp_Collars", "gunmetal", *[cyl(x, z, r + .008, y - .025, y + .025, 12) for _, _, x, z, r in runs[:2]])
    # bolted access panels, one per level (latched), amber latch, green status, Sprocket port at 0.45 m
    for y, lv in LEVELS:
        piv = (X1, 0, PZ[1] + .03)
        def hinge(m): return roty(m, open_deg, piv) if open_deg else m
        p.add(f"Access_Panel_{lv}", "gunmetal", hinge(box(X1, X1 + .02, y + PY[0] - .03, y + PY[1] + .03, PZ[0] - .03, PZ[1] + .03)))
        p.add(f"Access_Panel_{lv}_Bolts", "alloy", *[hinge(box(X1 + .02, X1 + .026, y + yy - .012, y + yy + .012, z - .012, z + .012))
                                                   for yy in (PY[0] + .03, PY[1] - .03) for z in (PZ[0] + .0, PZ[1])])
        p.add(f"Access_Panel_{lv}_Latch", "amber", hinge(box(X1 + .02, X1 + .027, y + 1.2, y + 1.32, PZ[0] + .01, PZ[0] + .04)))
        p.add(f"Sprocket_Port_{lv}", "gunmetal", hinge(box(X1 + .02, X1 + .035, y + .4, y + .5, 2.85, 2.95)))
        p.add(f"Sprocket_Port_{lv}_Ring", "amber", hinge(box(X1 + .035, X1 + .039, y + .435, y + .465, 2.885, 2.915)))
        p.add(f"Status_Light_{lv}", "green", box(X1, X1 + .008, y + PY[1] + .12, y + PY[1] + .15, 2.85, 2.95))
    return p

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); p = build(); gp = os.path.join(dc.ROOT, "godot/assets/models/riser_shaft.glb")
    tris, geo = export_final(p.P, [gp]); V = np.vstack([g[1] for g in geo.values()]); lo, hi = V.min(0), V.max(0)
    bad = [n for n, (mk, m) in p.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    SH = (.6, 2.2, .8, 2.4)   # lift shaft envelope X0, X1, Z0, Z1
    gap = round(lo[2] - SH[3], 4)
    print("tris", tris, "bounds", lo.round(3), hi.round(3), "bad", bad, "lift gap (Z)", gap,
          "overlap with shaft", bool(lo[2] < SH[3] - 1e-9 and lo[0] < SH[1] and hi[0] > SH[0]))
    sp = os.path.join(OUT, "final_riser_sheet.png")
    G = {k: (mk,) + tuple(shade_split(m)[i] for i in (0, 1, 3)) for k, (mk, m) in p.P.items()}
    render_sheet(G, sp, "Final  #7 riser shaft + sealed chase (Maintenance L1 / 202 L2, v1.1)")
    # append an open-panel iso (render only; glb stays closed)
    from PIL import Image, ImageDraw
    from bath_pod_generator import views
    q = build(open_deg=-100); Gq = {k: (mk,) + tuple(shade_split(m)[i] for i in (0, 1, 3)) for k, (mk, m) in q.P.items()}
    saved = tonemap(); iso = views()[3]; a = -np.pi * .5; Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
    im = crop(render_view(Gq, iso @ Ry, size=700, shadow=True)); FMAT.update(saved)
    A = Image.open(sp).convert("RGB"); B = Image.fromarray((np.clip(im, 0, 1) * 255).astype(np.uint8)); s = A.height * .9 / B.height
    B = B.resize((int(B.width * s), int(B.height * s))); C = Image.new("RGB", (A.width + B.width + 20, A.height), (244, 242, 236))
    C.paste(A, (0, 0)); C.paste(B, (A.width + 10, int(A.height * .08))); ImageDraw.Draw(C).text((A.width + 20, 10), "Iso, access panels open (render only)", fill=(85, 85, 85)); C.save(sp)
