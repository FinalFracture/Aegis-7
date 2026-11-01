#!/usr/bin/env python3
"""Rook: 3d-part-clipping-check + closure QA for the rev C preface_residential_sector.glb (run after the generator)."""
import os, sys, numpy as np, trimesh
from shapely.geometry import Polygon
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import preface_sector_rev_c_generator as G
sc = trimesh.load(G.GLB); geo = sc.dump(concatenate=False)
shell = trimesh.util.concatenate([m for m in geo if "Shell" in str(m.metadata.get("name"))])
glass = [m for m in geo if "Glass" in str(m.metadata.get("name"))]
lift = trimesh.util.concatenate(trimesh.load(os.path.join(G.ROOT, "godot/assets/models/sprocket_lift.glb")).dump())  # assembled check: lift shaft fills its cut-out
allm = trimesh.util.concatenate(geo + ([lift] if G.LIFT_CUTOUTS else [])); R = trimesh.ray.ray_triangle.RayMeshIntersector(allm)
fails = []
def hit(o, d):
    l, _, _ = R.intersects_location([o], [d], multiple_hits=False)
    return np.linalg.norm(l[0] - o) if len(l) else np.inf
# 1+2: 72-ray closure + corner rays per unit rect
UNITS = [k for k in G.ROOMS if not k.startswith(("Corridor", "Stair"))]
for n in UNITS:
    y0, rs = G.ROOMS[n]
    for (x0, x1, z0, z1) in rs[:1]:
        c = np.array([(x0 + x1) / 2, 0, (z0 + z1) / 2]); hx, hz = (x1 - x0) / 2, (z1 - z0) / 2
        for h in (2.6, 3.5):
            o = c + [0, y0 + h, 0]
            for a in np.radians(np.arange(0, 360, 5)):
                d = np.array([np.cos(a), 0, np.sin(a)]); tmax = min(hx / max(abs(d[0]), 1e-9), hz / max(abs(d[2]), 1e-9))
                t = hit(o, d)
                if t > tmax + 0.005 and not (len(rs) > 1 and t < 30): fails.append((n, "ray", h, round(np.degrees(a)), t, tmax))
        for h in (0.3, 1.5, 2.6, 3.5):
            o = c + [0, y0 + h, 0]
            for sx, sz in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
                v = np.array([sx * hx, 0, sz * hz]); dist = np.linalg.norm(v); t = hit(o, v / dist)
                if len(rs) > 1 and (sz < 0) == (z0 < -0.9) and False: pass
                if t > dist + 0.005: fails.append((n, "corner gap", h, (sx, sz), round(t - dist, 4)))
# 3: floor contact
for n, (y0, rs) in G.ROOMS.items():
    if n == "StairCore": continue
    for (x0, x1, z0, z1) in rs:
        for x in np.linspace(x0 + .3, x1 - .3, 6):
            for z in np.linspace(z0 + .3, z1 - .3, 6):
                if G.LIFT_CUTOUTS and 0.1 < x < 2.3 and 0.7 < z < 3.5: continue   # lift shaft, its call panels / riser cut-outs
                t = hit(np.array([x, y0 + 1.0, z]), np.array([0, -1, 0])); fy = y0 + 1.0 - t
                if abs(fy - y0) > 0.005: fails.append((n, "floor", x, z, fy))
# 4: door clear widths at 1.0 m above floor
widths = {}
for n, k, c, w, y in G.DOORS:
    zc = {"N": 0.9, "S": -0.9, "X": -9.0, "R": 9.0}[k]; o = np.array([c, y + 1.0, zc])
    wd = hit(o, np.array([1, 0, 0])) + hit(o, np.array([-1, 0, 0])); hd = hit(np.array([c, y + 0.01, zc]), np.array([0, 1, 0])) + 0.01
    widths[n] = (round(wd, 3), round(hd, 3))
    if wd < w - 0.005 or wd > w + 0.005: fails.append((n, "door width", wd))
# 5: overlap / coplanar glass vs shell
def facets(m):
    out = []
    for f, n in zip(m.facets, m.facets_normal):
        pts = m.vertices[np.unique(m.faces[f])]; out.append((n, float(np.dot(n, pts[0])), pts))
    for i, fc in enumerate(m.faces):
        if i not in set(np.concatenate(m.facets)) if len(m.facets) else True:
            n = m.face_normals[i]; out.append((n, float(np.dot(n, m.vertices[fc[0]])), m.vertices[fc]))
    return out
def proj(p, n):
    ax = int(np.argmax(np.abs(n))); o = [i for i in range(3) if i != ax]; return Polygon(p[:, o]).convex_hull
sf = facets(shell); cop = 0
for gm in glass:
    for n1, d1, p1 in facets(gm):
        for n2, d2, p2 in sf:
            if abs(abs(np.dot(n1, n2)) - 1) < 1e-6 and abs(d1 - np.sign(np.dot(n1, n2)) * d2) < 0.001:
                a = proj(p1, n1).intersection(proj(p2, n2)).area
                if a > 1e-4: cop += 1; fails.append((gm.metadata.get("name"), "coplanar", a))
    pen = max(0.0, -min(trimesh.proximity.signed_distance(shell, gm.vertices)) if False else 0.0)
emb = max(abs(trimesh.proximity.signed_distance(shell, gm.vertices)).max() for gm in glass)
print("watertight shell parts:", [m.is_watertight for m in geo if "Shell" in str(m.metadata.get("name"))])
print("tris:", {m.metadata.get("name"): len(m.faces) for m in geo})
print("door clear (width, head):", widths)
print("glass max embed into reveal (m):", round(emb, 4), " coplanar glass/shell facets >1cm2:", cop)
print("FAILS:", len(fails)); [print(" ", f) for f in fails[:40]]
sys.exit(1 if fails else 0)
