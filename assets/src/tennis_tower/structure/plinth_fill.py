"""Rook r7 (2026-11-11): tt_struct_plinth_fill, the cast fill between the flat building / terraces and the curved Strip 5 hull,
for the cylinder drop (design/tennis_tower_handoff/CYLINDER_DROP.md). Building coords (F1 = 0, origin SW corner).
Hull in building Y is the TRUE R 200 circle (not the spec parabola): hull(Z) = -F1_HD + R - sqrt(R^2 - (Z - 40)^2), with
F1_HD = R - sqrt(R^2 - 40^2) = 4.0408 so the S-face threshold (Z 0) is flush on the real drum (the parabola gives 4.000, 40.8 mm low).
Each region is a convex solid from its top (slab / terrace underside, 3 mm down: no coplanar faces) to hull - EMBED, so the
fill always runs 0.15 m into the drum floor (covers the 1-degree facet chord, <= 7.6 mm, and the parabola error, <= 6.7 mm).
Regions only span the Z band where the hull is below their top; outside it the slab / skirt itself is buried in the hull.
The diving pit (X 14.7..28.3, Z 21.7..34.3, walls to -2.9) gets its own region under the pit slab. Skirts stay the existing
tt_plinth_skirt / tt_plinth_skirt_terrace (assemble_preview.site / envelope), unchanged."""
import json
from struct_lib import *
from ridge_crown import huv
R, EMBED = 200.0, .15
F1_HD = R - np.sqrt(R*R - 1600.0)    # 4.0408
def hull(Z): return -F1_HD + R - np.sqrt(R*R - (Z - 40.0)**2)
def zband(top, z0, z1):            # Z range inside [z0, z1] where hull - EMBED < top - 0.02
    d = np.sqrt(R*R - (R - (top - .02 + EMBED + F1_HD))**2) if top - .02 + EMBED + F1_HD < R else 99.0
    return max(z0, 40 - d), min(z1, 40 + d)
def region(x0, x1, z0, z1, top, dz=1.0):
    a, b = zband(top, z0, z1)
    if b - a < .05: return None
    zs = np.unique(np.r_[np.arange(a, b, dz), b])
    return huv([(x, y, z) for x in (x0, x1) for z in zs for y in (top, min(hull(z) - EMBED, top - .02))])
PIT = (14.7, 28.3, 21.7, 34.3); G3 = .003; T1, TT, TP = -.403, -.313, -2.903     # pit walls / floor slab to -2.9 (build_structure f1_slab)
def fill():
    px0, px1, pz0, pz1 = PIT
    F = [region(-12, px0 - G3, 0, 79, T1), region(px1 + G3, 140, 0, 79, T1),
         region(px0, px1, 0, pz0 - G3, T1), region(px0, px1, pz1 + G3, 79, T1), region(px0, px1, pz0, pz1, TP)]
    W = [region(-62.5, -12.01, 13.5, 66.5, TT), region(140.01, 170.5, 13.5, 66.5, TT)]
    return [m for m in F + W if m is not None]
if __name__ == "__main__":
    LAY = json.load(open(LAYOUT)); REP = []
    ms = fill()
    export_chunk("tt_struct_plinth_fill", [("Plinth_Fill", CON, ms)], [("Fill-colonly", [m.copy() for m in ms])], REP, layout=LAY,
                 note="r7 cylinder drop: cast fill from slab / terrace undersides to the R 200 hull - 0.15 m")
    json.dump(LAY, open(LAYOUT, "w"), indent=1)
    r = REP[0]; print(r["asset"], r["tris"], r["passed"], r["world_offset"], r["coplanar"][:3], r["bad"][:3])
