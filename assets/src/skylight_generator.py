"""Rev C asset #5: skylight strip over the stair void (stair core v1.1). Same plan origin as stair_set_switchback.glb.
Plan / section: roof slab Y 8.8..9.1 (ROOF = 8.8 underside), skylight X -1.9..1.9, Z -8.9..-4.88 (the void, ZS..Z2t).
Interpretation: real glazing set into the roof slab; 'up' is toward the axis, so it lights the core from axis lighting.
Serviced from the roof side (panels lift out upward after the latches release)."""
import os, sys, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
import stair_set_generator as S, stair_guard_generator as SG
import dining_chair_generator as dc
from dining_chair_generator import export_final, shade_split
from bath_pod_generator import Pod
from kitchen_counter_generator import box
from stair_guard_generator import render_sheet
ROOF, RT = 8.8, .30; X0, X1 = S.XC; Z0, Z1 = S.ZS, S.Z2t
NX, NZ = 3, 4                    # 3 x 4 panels (~1.2 x 0.95 m)
FR, MU = .08, .05                # perimeter frame / mullion widths
def build():
    p = Pod("Stair_Skylight")
    # perimeter frame (gunmetal) lining the roof opening, full slab depth
    p.add("Frame", "gunmetal", box(X0, X1, ROOF, ROOF + RT, Z0, Z0 + FR), box(X0, X1, ROOF, ROOF + RT, Z1 - FR, Z1),
          box(X0, X0 + FR, ROOF, ROOF + RT, Z0 + FR, Z1 - FR), box(X1 - FR, X1, ROOF, ROOF + RT, Z0 + FR, Z1 - FR))
    xs = np.linspace(X0 + FR, X1 - FR, NX + 1); zs = np.linspace(Z0 + FR, Z1 - FR, NZ + 1); yg = ROOF + .16
    p.add("Mullions", "alloy", *[box(x - MU / 2, x + MU / 2, ROOF + .08, ROOF + .2, Z0 + FR, Z1 - FR) for x in xs[1:-1]],
          *[box(X0 + FR, X1 - FR, ROOF + .08, ROOF + .2, z - MU / 2, z + MU / 2) for z in zs[1:-1]])
    pan, lat = [], []
    for i in range(NX):
        for j in range(NZ):
            a0, a1 = xs[i] + (MU / 2 if i else 0), xs[i + 1] - (MU / 2 if i < NX - 1 else 0)
            b0, b1 = zs[j] + (MU / 2 if j else 0), zs[j + 1] - (MU / 2 if j < NZ - 1 else 0)
            pan.append(box(a0 + .005, a1 - .005, yg - .012, yg + .012, b0 + .005, b1 - .005))     # 24 mm laminated unit
            lat.append(box(a0 + .03, a0 + .07, ROOF + .075, ROOF + .08, b0 + .03, b0 + .05))         # latch light on the soffit side
    p.add("Glass_Panels", "glass", *pan); p.add("Panel_Latch_Lights", "amber", *lat)
    # bolted perimeter anchor plates (soffit) + violet perimeter light strip
    anc = [box(x - .1, x + .1, ROOF - .012, ROOF, Z0 + .01, Z0 + FR + .06) for x in (-1.3, 0, 1.3)] + \
          [box(x - .1, x + .1, ROOF - .012, ROOF, Z1 - FR - .06, Z1 - .01) for x in (-1.3, 0, 1.3)] + \
          [box(xx, xx + (.14 if xx < 0 else -.14) * 0 + .14, ROOF - .012, ROOF, z - .1, z + .1) for xx in (X0 + .0,) for z in np.linspace(Z0 + .8, Z1 - .8, 3)] + \
          [box(X1 - .14, X1, ROOF - .012, ROOF, z - .1, z + .1) for z in np.linspace(Z0 + .8, Z1 - .8, 3)]
    p.add("Anchor_Plates", "gunmetal", *anc)
    p.add("Perimeter_Light", "violet", box(X0 + FR, X1 - FR, ROOF + .02, ROOF + .035, Z0 + FR, Z0 + FR + .012), box(X0 + FR, X1 - FR, ROOF + .02, ROOF + .035, Z1 - FR - .012, Z1 - FR),
          box(X0 + FR, X0 + FR + .012, ROOF + .02, ROOF + .035, Z0 + FR + .012, Z1 - FR - .012), box(X1 - FR - .012, X1 - FR, ROOF + .02, ROOF + .035, Z0 + FR + .012, Z1 - FR - .012))
    p.add("Service_Lift_Lugs", "amber", *[box(x - .02, x + .02, yg + .012, yg + .022, z - .02, z + .02) for x in (xs[:-1] + xs[1:]) / 2 for z in (zs[:-1] + zs[1:]) / 2])
    return p
if __name__ == "__main__":
    import pygltflib
    p = build(); gp = os.path.join(dc.ROOT, "godot/assets/models/stair_skylight.glb"); tris, geo = export_final(p.P, [gp])
    g = pygltflib.GLTF2().load(gp)
    for m in g.materials:
        if m.name.lower() == "glass": m.alphaMode = "BLEND"; m.doubleSided = True
    g.save_binary(gp)
    V = np.vstack([gg[1] for gg in geo.values()]); lo, hi = V.min(0), V.max(0)
    st = S.build(); gd, _ = SG.build()
    top3 = max(m.bounds[1][1] for _, m in st.P.values()); top4 = max(m.bounds[1][1] for _, m in gd.P.values())
    bad = [n for n, (mk, m) in p.P.items() if not all(c.is_watertight for c in m.split(only_watertight=False))]
    print("tris", tris, "bounds", lo.round(3), hi.round(3), "size", (hi - lo).round(3), "bad", bad)
    print("opening", (X1 - X0, round(Z1 - Z0, 3)), "lowest skylight y", round(lo[1], 3), "top #3", round(top3, 3), "top #4", round(top4, 3),
          "clearance", round(lo[1] - max(top3, top4), 3), "XZ inside core", lo[0] >= X0 - 1e-9 and hi[0] <= X1 + 1e-9 and lo[2] >= Z0 - 1e-9 and hi[2] <= Z1 + 1e-9)
    G = {}
    for pre, P in (("S_", st.P), ("G_", gd.P), ("", p.P)):
        for k, (mk, m) in P.items(): G[pre + k] = (mk,) + tuple(shade_split(m)[i] for i in (0, 1, 3))
    render_sheet(G, os.path.join(S.OUT, "final_skylight_sheet.png"), "Final  #5 skylight strip in the roof over the stair void, with #3 stair set + #4 guards (stair core v1.1)")
