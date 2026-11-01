#!/usr/bin/env python3
"""Rook (M-45): derive every Rev C shell room-corner from preface_sector_rev_c_generator.ROOMS and verify closure on the
GLB itself (shell meshes only, no props). Ray from 0.25 m inside the corner along the corner diagonal; gap = how far the
ray travels past the corner point before hitting wall (0 = closed). Writes design/rev_c_shell_corners.json."""
import os, sys, json, numpy as np, trimesh
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import preface_sector_rev_c_generator as G
geo = trimesh.load(G.GLB).dump(); shell = trimesh.util.concatenate([m for m in geo if "Shell" in str(m.metadata.get("name"))])
R = trimesh.ray.ray_triangle.RayMeshIntersector(shell)
SOLID = G.shell  # watertight pre-split union from the generator
# extra rects not in ROOMS: 103/104/203/204 end strips are rs[1]; corridor + stair core are open to each other (skip their shared edge corners)
out, worst = [], 0.0
for n, (y0, rs) in G.ROOMS.items():
    for ri, (x0, x1, z0, z1) in enumerate(rs):
        for sx, sz in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            cx, cz = (x0, x1)[sx > 0], (z0, z1)[sz > 0]
            # SEAM_AUDIT method (placement_assert.gd): origin 0.5 m inside on x and z, ray toward the corner,
            # past = hit - 0.5*sqrt(2). Verified densely over the FULL wall height (every 0.1 m) plus +-1 mm aim jitter.
            d = -np.array([-sx, 0, -sz]) / np.sqrt(2); wall_h = 3.9 if y0 == 0 else G.TOP - G.L2
            AH = [0.3, 1.2, 2.0, 2.8, 3.6] + ([4.4] if y0 > 0 else [])
            def past(h, jx=0.0, jz=0.0):
                o = np.array([cx - sx * 0.5, y0 + h, cz - sz * 0.5]); tgt = np.array([cx + jx, y0 + h, cz + jz]); dd = (tgt - o) / np.linalg.norm(tgt - o)
                l, _, _ = R.intersects_location([o], [dd], multiple_hits=False)
                return (np.linalg.norm(l[0] - o) if len(l) else np.inf) - np.linalg.norm(tgt - o)
            rows = [round(float(past(h)), 4) for h in AH]
            dense = max(max(past(h, jx, jz) for jx, jz in ((0, 0), (.001, 0), (0, .001), (-.001, 0), (0, -.001))) for h in np.arange(0.1, wall_h - 0.05, 0.1))
            # M-61: a rect corner is a real closure corner only if wall mass sits diagonally behind it. Corners where
            # the end strip (rect 1) meets the unit body (rect 0) are CONVEX wall tips (e.g. the corridor end wall at
            # (+-10.10, -1.00)): past the tip the room continues, so a ray/capsule there correctly hits nothing.
            behind = [bool(SOLID.contains([[cx + sx * 0.03, y0 + h, cz + sz * 0.03]])[0]) for h in (0.3, 1.2, 2.0, 2.8, 3.6)]
            open_side = not all(behind)
            g = max(max(rows), dense)
            if not open_side: worst = max(worst, g)
            out.append({"room": n, "rect": ri, "level_y": y0, "corner_x": cx, "corner_z": cz, "inside_dir_xz": [-sx, -sz],
                        "audit_heights_above_floor": AH, "past_m": rows, "dense_full_height_max_past_m": round(float(dense), 4), "wall_height_m": wall_h,
                        "kind": "closure" if not open_side else "convex-tip/open-by-design (exclude from SEAM_AUDIT)",
                        "status": "SKIP" if open_side else ("PASS" if g <= 0.010 else "FAIL")})
res = {"source": "godot/assets/models/preface_residential_sector.glb (Rev C, M-61 r2 chamfered corners)", "datum": "GLB root at identity: L1 floor 0.000, L2 floor 4.200",
       "method": "SEAM_AUDIT method: origin 0.5 m inside on x and z, ray toward the corner, past = hit - 0.5*sqrt(2); dense check every 0.1 m over the full wall height with +-1 mm aim jitter. Corners carry a 20 mm 45-deg chamfer (hit lands before the corner, past < 0)",
       "tolerance_m": 0.010, "max_gap_closed_corners_m": worst,
       "n_corners": len(out), "n_fail": sum(c["status"] == "FAIL" for c in out), "n_closure": sum(c["status"] != "SKIP" for c in out), "skipped_convex_tips": [(c["room"], c["corner_x"], c["corner_z"]) for c in out if c["status"] == "SKIP"], "corners": out}
json.dump(res, open(os.path.join(G.ROOT, "design/rev_c_shell_corners.json"), "w"), indent=1)
print(res["n_corners"], "corners,", res["n_closure"], "closure, fail", res["n_fail"], "max gap", worst, "skipped", res["skipped_convex_tips"])
