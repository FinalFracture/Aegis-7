#!/usr/bin/env python3
"""Rook (2026-10-31): SEAM-01 / SEAM-02 wall-closure patch for godot/assets/models/preface_residential_sector.glb.
Patch's ray audit (context/playtest_bug_report.md, pass_playthrough_ee61cb6) found:
  SEAM-01  L1 side rooms had NO side walls: Side_Room_East_Lounge (x -12.25 / -4.75) and Side_Room_West_Storage
           (x 0.75 / 8.25) only had the z 2.76..2.94 door wall; the visual "walls" were the atrium back wall far behind.
  SEAM-02  corner notches where wall slabs stop short: Alcove 2C, APT 201/202 at x +/-5.35, atrium corners.
Fix = add closing boxes (world-space UV boxes from patch_residential_sector_generator.make_world_uv_box, material 0 =
Mat_Residential_AtriumAndApartmentAtlas, wall UV regions) as child nodes "<Room>_SeamFix" of the existing room nodes, so
the scene's per-MeshInstance trimesh colliders pick them up and interior streaming carries them with the room.
Boxes embed EMB = 5 mm into the walls they meet (<= 0.010 m overlap rule; no coplanar contact faces).
Idempotent: does nothing if *_SeamFix nodes already exist. Edits the GLB JSON + appends to its BIN chunk (textures untouched)."""
import json, struct, sys, os, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import patch_residential_sector_generator as g
GLB = os.path.join(os.path.dirname(__file__), "../../godot/assets/models/preface_residential_sector.glb")
E, I, T = 0.005, 0.002, 0.016
def sk_x(xp, out, y0, y1, z0, z1):  # skin on outer plane x = xp facing +out*x
    a = xp - out * I; return (*sorted((a, a - out * T)), y0 + I, y1 - I, z0, z1)
def sk_z(zp, out, y0, y1, x0, x1):  # skin on outer plane z = zp facing +out*z
    a = zp - out * I; return (x0, x1, y0 + I, y1 - I, *sorted((a, a - out * T)))
def apt(sx, zf):  # APT 201 (sx -1) / 202 (sx +1): outer side plane x = sx*5.35, front plane z 2.65, back plane z 8.55;
    # y between L2 floor (4.415) and ceiling slab (8.115). zf = front wall outer face (2.66 / 2.67), kept 2 mm clear.
    xs = sorted((sx * 5.53, sx * (5.35 + I + T)))  # z skins stop at the x skin's inner face (no overlap / shared face)
    return [sk_x(sx * 5.35, -sx, 4.415, 8.115, 2.65 + I, 8.55 - I),  # side wall faces the atrium: outward = -sx
            sk_z(2.65, -1, 4.415, 8.115, *xs), sk_z(8.55, 1, 4.415, 8.115, *xs)]
APT, ATR = g.UV_WALL_APT, g.UV_WALL_ATRIUM
# (parent node, uv rect, [(x0,x1, y0,y1, z0,z1) world])
FIX = {
 # SEAM-01: full side walls, door wall back face (z 2.94) -> atrium back wall inner face (z 8.76); 0.15 m thick
 # (matches ROOM_1A/1B_INTERIOR inset); floor top 0.23 / mezzanine soffit 3.985 embedded 5 mm.
 "Side_Room_East_Lounge": (APT, [(-12.25, -12.10, .225, 3.99, 2.94 - E, 8.76 + E), (-4.90, -4.75, .225, 3.99, 2.94 - E, 8.76 + E)]),
 "Side_Room_West_Storage": (APT, [(0.75, 0.90, .225, 3.99, 2.94 - E, 8.76 + E), (8.10, 8.25, .225, 3.99, 2.94 - E, 8.76 + E)]),
 # SEAM-02: thin closing SKINS (T = 16 mm thick) lying I = 2 mm inside each outer corner plane, so no skin face is coplanar
 # with a host face and no point of a skin is more than 8 mm inside host geometry (<= 0.010 m overlap rule); skins run
 # E = 5 mm into the wall ends they meet.
 "Alcove_2C_Upper_Vent_Chase": (APT, [sk_x(-12.74, -1, 4.41, 7.02, -5.69 + I, -5.58 + E),      # back corner, x = -12.74 plane
                                      sk_z(-5.69, -1, 4.41, 7.02, -12.74 + I + T, -12.68 + E),      # back corner, z = -5.69 plane
                                      sk_z(-3.40, 1, 4.41, 7.02, -12.74 + I, -12.58 + E)]),     # front strip, z = -3.40 plane
 "Tech_Apartment_Upper": (APT, apt(-1, 2.66)),
 "Room_2B_Neighbor_Balcony_Suite": (APT, apt(1, 2.67)),
 # Atrium outer corners: N = side slab (to z 9.00) x N wall (z 8.76..9.04, x <= 13.98); S = side slab x vestibule (z -9.01).
 "Residential_Hallway_Atrium": (ATR, [b for sx in (1, -1) for b in (
        sk_x(sx * 14.04, sx, .19, 8.75, 8.975, 9.04 - I), sk_z(9.04, 1, .19, 8.75, *sorted((sx * 13.975, sx * (14.04 - I - T)))),
        sk_x(sx * 14.04, sx, .19, 8.75, -9.01 + I, -8.975), sk_z(-9.01, -1, .19, 8.75, *sorted((sx * 13.975, sx * (14.04 - I - T)))))]),
}
def run():
    b = bytearray(open(GLB, "rb").read()); jl = struct.unpack("<I", b[12:16])[0]
    J = json.loads(b[20:20 + jl]); bo = 20 + jl; bl = struct.unpack("<I", b[bo:bo + 4])[0]; BIN = bytearray(b[bo + 8:bo + 8 + bl])
    names = {n.get("name"): i for i, n in enumerate(J["nodes"])}
    if any(n.get("name", "").endswith("_SeamFix") for n in J["nodes"]):
        print("already applied; nothing to do"); return []
    added = []
    for parent, (uvr, boxes) in FIX.items():
        pi = names[parent]; t = np.array(J["nodes"][pi].get("translation", [0, 0, 0]))
        geoms = [g.make_world_uv_box((x1 - x0, y1 - y0, z1 - z0), ((x0 + x1) / 2 - t[0], (y0 + y1) / 2 - t[1], (z0 + z1) / 2 - t[2]), uv_rect=uvr)
                 for x0, x1, y0, y1, z0, z1 in boxes]
        P, N, UV, I = g.merge_geometries(geoms)
        P = P.astype(np.float32); N = N.astype(np.float32); UV = UV.astype(np.float32); I = I.astype(np.uint32).ravel()
        acc = []
        for arr, typ, comp in ((P, "VEC3", 5126), (N, "VEC3", 5126), (UV, "VEC2", 5126), (I, "SCALAR", 5125)):
            while len(BIN) % 4: BIN.append(0)
            off = len(BIN); BIN += arr.tobytes()
            J["bufferViews"].append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes, **({"target": 34963} if typ == "SCALAR" else {"target": 34962})})
            a = {"bufferView": len(J["bufferViews"]) - 1, "componentType": comp, "count": int(len(arr)), "type": typ}
            if typ == "VEC3" and arr is P: a["min"] = P.min(0).tolist(); a["max"] = P.max(0).tolist()
            J["accessors"].append(a); acc.append(len(J["accessors"]) - 1)
        J["meshes"].append({"name": parent + "_SeamFix_Mesh", "primitives": [{"attributes": {"POSITION": acc[0], "NORMAL": acc[1], "TEXCOORD_0": acc[2]}, "indices": acc[3], "material": 0}]})
        J["nodes"].append({"name": parent + "_SeamFix", "mesh": len(J["meshes"]) - 1, "translation": [0.0, 0.0, 0.0]})
        J["nodes"][pi].setdefault("children", []).append(len(J["nodes"]) - 1); added.append((parent, len(boxes), len(I) // 3))
    while len(BIN) % 4: BIN.append(0)
    J["buffers"][0]["byteLength"] = len(BIN)
    js = json.dumps(J, separators=(",", ":")).encode(); js += b" " * ((4 - len(js) % 4) % 4)
    out = struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(BIN)) + struct.pack("<II", len(js), 0x4E4F534A) + js + struct.pack("<II", len(BIN), 0x004E4942) + bytes(BIN)
    open(GLB, "wb").write(out); return added
if __name__ == "__main__":
    print(run())
