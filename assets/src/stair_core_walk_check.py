#!/usr/bin/env python3
"""Rook (M-70): capsule walk check (r 0.35, h 1.8, step 0.3, max slope 35 deg) over the assembled Rev C stair core:
sector shell + stair_set_switchback + stair_guard_handrail, floors from the -colonly colliders + shell."""
import os, numpy as np, trimesh
M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../godot/assets/models")
def load(f, want):
    out = []
    for n, g in trimesh.load(os.path.join(M, f)).geometry.items():
        if want(n): out.append(g)
    return trimesh.util.concatenate(out)
shell = load("preface_residential_sector.glb", lambda n: "Shell" in n)
col = load("stair_set_switchback.glb", lambda n: n.endswith("_Col"))
vis = trimesh.util.concatenate([load("stair_set_switchback.glb", lambda n: not n.endswith("_Col")), load("stair_guard_handrail.glb", lambda n: not n.endswith("_Col"))])
gcol = load("stair_guard_handrail.glb", lambda n: n.endswith("_Col"))
floor = trimesh.ray.ray_triangle.RayMeshIntersector(trimesh.util.concatenate([shell, col]))
obst = trimesh.util.concatenate([shell, vis, gcol]); PQ = trimesh.proximity.ProximityQuery(obst)
R, STEP, H = 0.35, 0.3, 1.8
def fy(x, z, yprev):   # highest walkable surface at or below yprev + STEP (+ a little)
    l, _, _ = floor.intersects_location([[x, yprev + STEP + 0.05, z]], [[0, -1, 0]], multiple_hits=False)
    return l[0][1] if len(l) else None
def walk(name, pts, y0):
    path = []
    for (ax, az), (bx, bz) in zip(pts, pts[1:]):
        n = max(2, int(np.hypot(bx - ax, bz - az) / 0.05))
        path += [(ax + (bx - ax) * k / n, az + (bz - az) * k / n) for k in range(n)]
    path.append(pts[-1]); y = y0; ys = []; worst_clear = 9; worst_slope = 0; bad = []
    for i, (x, z) in enumerate(path):
        f = fy(x, z, y)
        if f is None: bad.append(("no floor", x, z)); break
        if i: worst_slope = max(worst_slope, np.degrees(np.arctan2(abs(f - y), 0.05)))
        if f - y > STEP: bad.append(("step", x, z, f - y))
        y = f; ys.append(y)
        axis = np.array([[x, y + h, z] for h in np.arange(0.45, H - R + 1e-6, 0.1)])
        d = PQ.signed_distance(axis); c = float(np.min(np.abs(d)))
        worst_clear = min(worst_clear, c)
        if c < R - 0.005: bad.append(("clip", round(x, 2), round(y, 2), round(z, 2), round(c, 3)))
    print(f"{name}: {len(path)} samples, y {ys[0]:.3f} -> {ys[-1]:.3f}, max slope {worst_slope:.1f} deg, min capsule clearance {worst_clear:.3f} m, issues {bad[:5]}")
    return not bad and worst_slope <= 35.5
ok = all([
    walk("descend L2 corridor -> flight 2 -> mid-landing -> flight 1 -> L1 corridor", [(1.15, 0.0), (1.15, -4.7), (1.15, -8.1), (-1.15, -8.1), (-1.15, -2.7), (-1.15, -0.2)], 4.2),
    walk("climb L1 -> flight 1 -> mid -> flight 2 -> L2", [(-1.15, -0.2), (-1.15, -2.7), (-1.15, -8.1), (1.15, -8.1), (1.15, -4.7), (1.15, -0.3)], 0.0),
    walk("L1 egress corridor -> under flight 2 -> vestibule -> Sector-4 exit", [(1.15, 0.0), (1.15, -8.2), (0.0, -8.5), (0.0, -8.8)], 0.0)])
print("WALK", "PASS" if ok else "FAIL")
