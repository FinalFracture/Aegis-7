#!/usr/bin/env python3
"""Rook (2026-11-02, M-70): collision for the approved Rev C stair core assets (stair core v1.1: 26 R x 0.1615, T 0.28,
16 R west flight + 10 R east flight, mid-landing Y 2.585, L2 landing Y 4.200). Appends invisible Godot `-colonly` /
`-convcolonly` child nodes to the existing glbs (visual meshes untouched; idempotent):
  stair_set_switchback.glb : Flight1_Ramp-colonly, Flight2_Ramp-colonly (walk plane through the tread nosings, 29.98 deg),
                             Mid_Landing-colonly, L2_Landing-colonly (top = finished landing surface, flush 2.585 / 4.200)
  stair_guard_handrail.glb : Guard_Glass_NN-convcolonly (one convex hull per glass panel, REAL-02)
Both glbs are in building-plan coordinates (same frame as preface_residential_sector.glb) -> place at identity."""
import os, sys, json, struct, numpy as np, trimesh
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import stair_set_generator as S
M = os.path.join(HERE, "../../godot/assets/models")
STAIR, GUARD = os.path.join(M, "stair_set_switchback.glb"), os.path.join(M, "stair_guard_handrail.glb")
TH = 0.20
def slab_between(x0, x1, za, ya, zb, yb):
    """thin box whose TOP face is the line (za,ya)->(zb,yb), full width x0..x1"""
    if zb < za: za, ya, zb, yb = zb, yb, za, ya   # keep +Z-ward direction so the box top stays up
    L = np.hypot(zb - za, yb - ya); b = trimesh.creation.box(extents=(x1 - x0, TH, L))
    ang = np.arctan2(yb - ya, zb - za)   # rotation about X taking +Z to the ramp direction
    b.apply_translation((0, -TH / 2, 0)); b.apply_transform(trimesh.transformations.rotation_matrix(-ang, [1, 0, 0]))
    b.apply_translation(((x0 + x1) / 2, (ya + yb) / 2, (za + zb) / 2)); return b
def stair_colliders():
    R, T, YL, ZL, Z1b, Z2t = S.R, S.T, S.YL, S.ZL, S.Z1b, S.Z2t
    return {"Flight1_Ramp-colonly": slab_between(*S.F1, Z1b + T, 0.0, ZL, YL),            # floor at Z -2.92 -> mid-landing edge
            "Flight2_Ramp-colonly": slab_between(*S.F2, ZL - T, YL, Z2t, S.RISE),        # mid-landing -> L2 landing edge Z -4.88
            "Mid_Landing-colonly": trimesh.creation.box(bounds=[[-1.9, YL - 0.25, S.ZS], [1.9, YL, ZL]]),
            "L2_Landing-colonly": trimesh.creation.box(bounds=[[-1.9, S.RISE - 0.30, Z2t], [1.9, S.RISE, S.ZN]]),
            "Flight1_Understair_Closure-colonly": understair_closure()}
def understair_closure():
    """GEO-22: flight 1 is cast solid to the floor (visual), but only its thin ramp collided, so a capsule could walk into
    the cast mass and head-strike the ramp underside (y 1.82 @ Z -6.48). Solid prism filling x F1, floor -> ramp underside,
    capped at the mid-landing collider soffit (YL-0.25); i.e. every point of flight 1 footprint with clear height < 2.1 m
    (in fact all of it, max underside 2.335) is closed. Touches but does not overlap the ramp / mid-landing colliders."""
    R, T, YL, ZL, Z1b = S.R, S.T, S.YL, S.ZL, S.Z1b
    za, zb = Z1b + T, ZL; slope = YL / (za - zb); ang = np.arctan(slope); dv = TH / np.cos(ang)
    z0 = za - dv / slope                       # where the ramp underside meets the floor
    ycap = YL - 0.25; zc = za - (ycap + dv) / slope
    prof = [(z0, 0.0), (zb, 0.0), (zb, ycap), (zc, ycap)]
    pts = [(x, y, z) for x in S.F1 for z, y in prof]
    return trimesh.convex.convex_hull(np.array(pts))
def guard_colliders():   # Guard_Glass = 18 panels, each a 12-tri 12 mm slab, emitted in order -> one hull per 12 faces
    g = trimesh.load(GUARD).geometry["Guard_Glass"]; assert len(g.faces) % 12 == 0
    out = {}
    for i in range(len(g.faces) // 12):
        h = trimesh.Trimesh(g.vertices[g.faces[i * 12:(i + 1) * 12].ravel()]).convex_hull if False else trimesh.convex.convex_hull(g.vertices[np.unique(g.faces[i * 12:(i + 1) * 12])])
        out[f"Guard_Glass_{i:02d}-convcolonly"] = h
    return out
def append(path, meshes):
    b = bytearray(open(path, "rb").read()); jl = struct.unpack("<I", b[12:16])[0]
    J = json.loads(b[20:20 + jl]); bo = 20 + jl; bl = struct.unpack("<I", b[bo:bo + 4])[0]; BIN = bytearray(b[bo + 8:bo + 8 + bl])
    keep = [i for i, n in enumerate(J["nodes"]) if "colonly" not in n.get("name", "")]
    if len(keep) != len(J["nodes"]): raise SystemExit(f"{os.path.basename(path)}: colliders already present (regenerate the glb first)")
    for nm, m in meshes.items():
        P = m.vertices.astype(np.float32); I = m.faces.astype(np.uint32).ravel(); acc = []
        for arr, typ, comp, tgt in ((P, "VEC3", 5126, 34962), (I, "SCALAR", 5125, 34963)):
            while len(BIN) % 4: BIN.append(0)
            off = len(BIN); BIN += arr.tobytes(); J["bufferViews"].append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes, "target": tgt})
            a = {"bufferView": len(J["bufferViews"]) - 1, "componentType": comp, "count": int(len(arr)), "type": typ}
            if typ == "VEC3": a["min"] = P.min(0).tolist(); a["max"] = P.max(0).tolist()
            J["accessors"].append(a); acc.append(len(J["accessors"]) - 1)
        J["meshes"].append({"name": nm.split("-")[0] + "_Col", "primitives": [{"attributes": {"POSITION": acc[0]}, "indices": acc[1]}]})
        J["nodes"].append({"name": nm, "mesh": len(J["meshes"]) - 1}); J["scenes"][J.get("scene", 0)]["nodes"].append(len(J["nodes"]) - 1)
    while len(BIN) % 4: BIN.append(0)
    J["buffers"][0]["byteLength"] = len(BIN)
    js = json.dumps(J, separators=(",", ":")).encode(); js += b" " * ((4 - len(js) % 4) % 4)
    open(path, "wb").write(struct.pack("<III", 0x46546C67, 2, 28 + len(js) + len(BIN)) + struct.pack("<II", len(js), 0x4E4F534A) + js + struct.pack("<II", len(BIN), 0x004E4942) + bytes(BIN))
if __name__ == "__main__":
    sc, gc = stair_colliders(), guard_colliders()
    for k, m in sc.items(): print(k, m.bounds.round(3).tolist())
    print(len(gc), "guard hulls"); append(STAIR, sc); append(GUARD, gc)
