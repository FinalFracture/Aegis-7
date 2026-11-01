#!/usr/bin/env python3
"""Rook (2026-11-01): Rev C rebuild of godot/assets/models/preface_residential_sector.glb.
Sources: design/residential_apartment_layout_v2.md (rev C / C.2 / C.2a), residential_floorplan_rev_c.py,
residential_roomlayout_rev_c.py (v3 plans), residential_asset_list_rev_c.md.
Building-local datum (same as stair_set_switchback / riser_shaft / sprocket_lift / stair_skylight glbs):
  L1 floor top Y 0.000, L2 floor top Y 4.200 (slab 3.90..4.20), roof slab 8.80..9.10, outer walls on the
  X +-14 / Z +-9 centerlines (0.20 m), partitions 0.20 m on their centerlines. Corridor walls sit OUTSIDE the
  Z +-0.8 faces (0.8..1.0) so the corridor is 1.6 m clear and the hubs/lift fronts seat on Z +-0.8 (QA-BK-01).
Atrium, mezzanine, Alcove 2C, ramp connector and the old open portals are removed (rev C REAL-05).
Shell = one manifold union of slabs + walls minus real cut-outs (doors, windows, shaft, riser, stair, skylight),
so every wall corner/T is closed by construction (no slab seams, no coplanar internal faces). It is then split
into L1 / L2 / Roof nodes and diced on a 3.5 m grid for world-space atlas UVs (Mat_Residential atlas)."""
import os, sys, json, numpy as np, trimesh
from trimesh.boolean import union, difference
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "../..")
GLB = os.path.join(ROOT, "godot/assets/models/preface_residential_sector.glb")
sys.path.insert(0, HERE)
import patch_residential_sector_generator as g
L2, TOP, HD, T = 4.2, 8.8, 2.3, 0.1   # L2 floor top, roof soffit, door head, half partition
def B(x0, x1, y0, y1, z0, z1):
    b = trimesh.creation.box(extents=(x1 - x0, y1 - y0, z1 - z0)); b.apply_translation(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)); return b
# ---------------- solids ----------------
solid = [B(-14.1, 14.1, -0.3, 0.0, -9.1, 9.1),            # ground slab
         B(-14.1, 14.1, 3.9, L2, -9.1, 9.1),               # L2 slab
         B(-14.1, 14.1, TOP, 9.1, -9.1, 9.1),              # roof slab
         B(-14.1, -13.9, 0, TOP, -9.1, 9.1), B(13.9, 14.1, 0, TOP, -9.1, 9.1),
         B(-14.1, 14.1, 0, TOP, -9.1, -8.9), B(-14.1, 14.1, 0, TOP, 8.9, 9.1),
         B(-13.9, 13.9, 0, TOP, 0.8, 1.0),                 # corridor N wall (also closes 101/102 off the end strips)
         B(-9.9, -1.9, 0, TOP, -1.0, -0.8), B(1.9, 9.9, 0, TOP, -1.0, -0.8),   # corridor S wall (stair core open)
         B(-10.1, -9.9, 0, TOP, -1.0, 0.8), B(9.9, 10.1, 0, TOP, -1.0, 0.8),   # corridor end walls (end strips)
         B(-2.1, -1.902, 0, TOP, -8.9, -0.8), B(1.902, 2.1, 0, TOP, -8.9, -0.8),   # stair core walls; 2 mm off the stair glb stringers (x +-1.900) so no coplanar contact
         B(-4.6, -4.4, 0, 3.9, 1.0, 8.9), B(0.4, 0.6, 0, 3.9, 1.0, 8.9), B(5.9, 6.1, 0, 3.9, 1.0, 8.9),  # L1 N partitions
         B(-0.1, 0.1, L2, TOP, 1.0, 8.9)]                   # L2 201|202 partition
# door openings: (name, axis-wall, centre, z/x of wall, clear width, floor y)  - 1.4 m doors cut 1.5 m clear (Gage)
DOORS = [("101", "N", -6.5, 1.5, 0), ("Laundry", "N", -2.0, 1.5, 0), ("Maintenance", "N", 3.2, 2.0, 0), ("102", "N", 8.0, 1.5, 0),
         ("103", "S", -4.5, 1.5, 0), ("104", "S", 4.5, 1.5, 0), ("Sector4_Exit", "X", 0.0, 2.6, 0), ("Maintenance_Service", "R", 3.2, 2.0, 0),
         ("201", "N", -3.0, 1.5, L2), ("202", "N", 3.0, 1.5, L2), ("203", "S", -4.5, 1.5, L2), ("204", "S", 4.5, 1.5, L2)]
WZ = {"N": (0.75, 1.05), "S": (-1.05, -0.75), "X": (-9.15, -8.85), "R": (8.85, 9.15)}
cut = [B(c - w / 2, c + w / 2, y, y + HD, *WZ[k]) for _, k, c, w, y in DOORS]
# windows (sill 0.9, head 2.4): promenade windows of 103/104/203/204 (window desk / nook / toy-drift strip X 3..7),
# 201 west window by the C.2 reading chair (Z 3.2..6.2), stair promenade slot at the mid-landing (Y 3.0..7.0).
WIN = [("103", (-6.5, -3.5), 0, "S"), ("104", (3.5, 6.5), 0, "S"), ("203", (-6.5, -3.5), L2, "S"), ("204", (3.5, 6.5), L2, "S"),
       ("201", (3.2, 6.2), L2, "W"), ("Stair_Slot", (-0.6, 0.6), None, "S")]
for n, (a, b), y, k in WIN:
    y0, y1 = (3.0, 7.0) if y is None else (y + 0.9, y + 2.4)
    cut.append(B(a, b, y0, y1, -9.15, -8.85) if k == "S" else B(-14.15, -13.85, y0, y1, a, b))
# M-62 (2026-11-01): sprocket_lift.glb / riser_shaft.glb are not placed yet (M-11), so the corridor wall stays SOLID across the
# shaft front (x 0.6..2.2, both levels) and the shaft/riser slab holes stay closed. Set LIFT_CUTOUTS = True when M-11 lands
# (then the lift glb supplies the shaft walls + its 1.0 x 1.3 corridor doors, and its front wall must replace ours at z 0.8..1.0).
LIFT_CUTOUTS = False
if LIFT_CUTOUTS:
    cut += [B(0.6, 2.2, -0.15, 6.6, 0.75, 2.4), B(0.6, 2.2, 3.85, 4.25, 0.75, 2.4),
            B(0.6, 1.64, 3.85, 4.25, 2.4, 3.4)]              # lift shaft + riser through the L2 slab
cut += [
        B(-1.9, 1.9, 3.85, 4.25, -8.9, -0.8),                # stair core: stair_set_switchback.glb supplies mid + L2 landings
        B(-1.9, 1.9, 8.75, 9.15, -8.9, -4.88)]              # skylight strip (stair_skylight.glb)
# rooms (name, level y, rect list x0,x1,z0,z1 clear-of-walls) -> marker nodes + QA
ROOMS = {"101": (0, [(-13.9, -4.6, 1.0, 8.9)]), "Laundry": (0, [(-4.4, 0.4, 1.0, 8.9)]), "Maintenance": (0, [(0.6, 5.9, 1.0, 8.9)]),
         "102": (0, [(6.1, 13.9, 1.0, 8.9)]), "103": (0, [(-13.9, -2.1, -8.9, -1.0), (-13.9, -10.1, -1.0, 0.8)]),
         "104": (0, [(2.1, 13.9, -8.9, -1.0), (10.1, 13.9, -1.0, 0.8)]), "Corridor_L1": (0, [(-9.9, 9.9, -0.8, 0.8)]),
         "StairCore": (0, [(-1.9, 1.9, -8.9, -0.8)]),
         "201": (L2, [(-13.9, -0.1, 1.0, 8.9)]), "202": (L2, [(0.1, 13.9, 1.0, 8.9)]),
         "203": (L2, [(-13.9, -2.1, -8.9, -1.0), (-13.9, -10.1, -1.0, 0.8)]), "204": (L2, [(2.1, 13.9, -8.9, -1.0), (10.1, 13.9, -1.0, 0.8)]),
         "Corridor_L2": (L2, [(-9.9, 9.9, -0.8, 0.8)])}
# M-61 r2: 20 mm 45-degree chamfer column in every concave (closure) room corner, full wall height. A ray/capsule aimed
# exactly at a 90-degree corner line can slip between the two wall faces in a runtime trimesh; with the chamfer the
# corner ray lands on a flat face (13 mm from the corner along each wall, invisible at play distance).
base = union(solid, engine="manifold"); CH = 0.02; chamfers = []
for _n, (_y, _rs) in ROOMS.items():
    for (_x0, _x1, _z0, _z1) in _rs:
        for _sx, _sz in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            _cx, _cz = (_x0, _x1)[_sx > 0], (_z0, _z1)[_sz > 0]; _y1 = 3.9 if _y == 0 else TOP
            if all(base.contains([[_cx + _sx * 0.03, _y + h, _cz + _sz * 0.03]])[0] for h in (0.3, 2.0, 3.6)):
                c = trimesh.creation.box(extents=(CH, _y1 - _y + 0.02, CH))
                c.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 4, [0, 1, 0]))
                c.apply_translation((_cx, (_y + _y1) / 2, _cz)); chamfers.append(c)
shell = difference([union([base] + chamfers, engine="manifold"), union(cut, engine="manifold")], engine="manifold")
assert shell.is_watertight and shell.is_volume, "shell not manifold"
# glass panes 20 mm, centred in the wall, 5 mm into each reveal
glass = []
for n, (a, b), y, k in WIN:
    y0, y1 = (3.0, 7.0) if y is None else (y + 0.9, y + 2.4)
    glass.append((n, B(a - .005, b + .005, y0 - .005, y1 + .005, -9.01, -8.99) if k == "S" else B(-14.01, -13.99, y0 - .005, y1 + .005, a - .005, b + .005)))
# ---------------- UVs ----------------
TILE = 3.5; GOFF = 0.173  # M-61 r2: grid offset keeps dice seams off round probe heights (e.g. y 7.0)
def dice(m):
    for ax in range(3):
        lo, hi = m.bounds[:, ax]
        for k in range(int(np.floor((lo - GOFF) / TILE)) + 1, int(np.ceil((hi - GOFF) / TILE))):
            o = np.zeros(3); o[ax] = k * TILE + GOFF; n = np.zeros(3); n[ax] = 1
            a = trimesh.intersections.slice_mesh_plane(m, n, o); b = trimesh.intersections.slice_mesh_plane(m, -n, o)
            m = trimesh.util.concatenate([a, b])
    return m
def uv_mesh(m, mat):
    m = dice(m); m.merge_vertices(); m = m.copy(); m.unmerge_vertices()
    F = m.faces; V = m.vertices; Nf = m.face_normals; uv = np.zeros((len(V), 2))
    for fi, f in enumerate(F):
        n = Nf[fi]; ax = int(np.argmax(np.abs(n))); o = [i for i in range(3) if i != ax]
        rect = g.UV_FLOOR_SLATE if (ax == 1 and n[1] > 0.5) else g.UV_WALL_APT
        c = V[f].mean(0); cell = np.floor((c - GOFF) / TILE) * TILE + GOFF
        loc = np.clip((V[f] - cell) / TILE, 0, 1)
        u0, u1, v0, v1 = rect
        uv[f, 0] = u0 + loc[:, o[0]] * (u1 - u0); uv[f, 1] = v0 + loc[:, o[1]] * (v1 - v0)
    m.visual = trimesh.visual.TextureVisuals(uv=uv, material=mat); return m
def box_uv(m, mat):
    m = m.copy(); m.unmerge_vertices(); V = m.vertices; uv = np.zeros((len(V), 2))
    for fi, f in enumerate(m.faces):
        ax = int(np.argmax(np.abs(m.face_normals[fi]))); o = [i for i in range(3) if i != ax]
        lo, hi = m.bounds; uv[f] = (V[f][:, o] - lo[o]) / np.maximum(hi[o] - lo[o], 1e-6)
    m.visual = trimesh.visual.TextureVisuals(uv=uv, material=mat); return m
def split_y(m, y0, y1):
    if y0 is not None: m = trimesh.intersections.slice_mesh_plane(m, [0, 1, 0], [0, y0, 0])
    if y1 is not None: m = trimesh.intersections.slice_mesh_plane(m, [0, -1, 0], [0, y1, 0])
    return m
def build():
    src = trimesh.load(GLB)
    mats = {gm.visual.material.name: gm.visual.material for gm in src.geometry.values()}
    wall = mats["Mat_Residential_AtriumAndApartmentAtlas"]; gl = mats["Mat_Glass_ResidentialAtrium_Translucent"]
    sc = trimesh.Scene(base_frame="PrefaceResidentialSector_Root")
    for nm, y0, y1 in (("RevC_Shell_L1", None, 3.9), ("RevC_Shell_L2", 3.9, TOP), ("RevC_Shell_Roof", TOP, None)):
        sc.add_geometry(uv_mesh(split_y(shell, y0, y1), wall), node_name=nm, geom_name=nm + "_Mesh", parent_node_name="PrefaceResidentialSector_Root")
    for n, m in glass:
        nm = f"RevC_Window_{n}_Glass"; sc.add_geometry(box_uv(m, gl), node_name=nm, geom_name=nm + "_Mesh", parent_node_name="PrefaceResidentialSector_Root")
    for n, (y, rs) in ROOMS.items():
        x0, x1, z0, z1 = rs[0]; sc.graph.update(frame_to=f"Unit_{n}", frame_from="PrefaceResidentialSector_Root", matrix=trimesh.transformations.translation_matrix(((x0 + x1) / 2, y, (z0 + z1) / 2)))
    for n, k, c, w, y in DOORS:
        z = {"N": 0.8, "S": -0.8, "X": -9.1, "R": 9.1}[k]
        sc.graph.update(frame_to=f"Door_{n}", frame_from="PrefaceResidentialSector_Root", matrix=trimesh.transformations.translation_matrix((c, y, z)))
    sc.graph.update(frame_to="Spawn_201_Suggested", frame_from="PrefaceResidentialSector_Root", matrix=trimesh.transformations.translation_matrix((-9.35, L2, 6.2)))
    sc.export(GLB); wrap_root(); return sc
def wrap_root():  # single named root node (old GLB root name kept) + scene name
    import struct
    b = open(GLB, "rb").read(); jl = struct.unpack("<I", b[12:16])[0]; J = json.loads(b[20:20 + jl]); rest = b[20 + jl:]
    kids = J["scenes"][0]["nodes"]; J["nodes"].append({"name": "PrefaceResidentialSector_Root", "children": kids})
    J["scenes"] = [{"name": "PrefaceResidentialSector_RevC", "nodes": [len(J["nodes"]) - 1]}]; J["scene"] = 0
    js = json.dumps(J, separators=(",", ":")).encode(); js += b" " * ((4 - len(js) % 4) % 4)
    open(GLB, "wb").write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + len(rest)) + struct.pack("<II", len(js), 0x4E4F534A) + js + rest)
if __name__ == "__main__":
    s = build(); print({k: len(v.faces) for k, v in s.geometry.items()})
