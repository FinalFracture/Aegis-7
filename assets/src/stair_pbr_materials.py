"""Rook (2026-11-03, VIS-18/VIS-19): PBR materials + UVs for stair_set_switchback.glb and stair_guard_handrail.glb.
Re-skins the visual primitives only (no geometry/collider/node/pivot change; triangle count preserved, vertices unwelded
per corner for planar UVs). Uses the existing Aegis texture sets by relative URI (nothing duplicated into the glb):
  Slate        -> residential atlas UV_FLOOR_SLATE (albedo+ORM+normal, same as the sector shell floors)
  Underside    -> residential atlas UV_PLANTER_STONE, dark painted concrete (#5E656E), for down-facing WhiteComposite faces
  WhiteComposite -> facade_aerospace_white_cladding (albedo)       Gunmetal -> qa03/door_jamb_gunmetal (albedo+ORM)
  BrushedAlloy -> qa03/rail_brushed_titanium (albedo+ORM)          Glass    -> residential_atrium_glass_translucent
LockAmber / AccentViolet emissive accents keep their factor-only materials. Rerunnable: on an already re-skinned glb only the Stair_* materials/texture tables are rewritten.
Run: python3 assets/src/stair_pbr_materials.py   (after stair_set_generator / stair_core_colliders_rev_c)."""
import os, sys, json, struct, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import patch_residential_sector_generator as g
M = os.path.join(HERE, "../../godot/assets/models")
T = "../textures/"
ATL = {"albedo": T + "residential_atrium_and_apartment_atlas_albedo.png", "orm": T + "residential_atrium_and_apartment_atlas_orm.png",
       "normal": T + "residential_atrium_and_apartment_atlas_normal.png"}
# name: (albedo, orm, normal, baseColorFactor, metallic, roughness, uv mode[, orm drives MR?])
# glTF multiplies metallicFactor x ORM.B and roughnessFactor x ORM.G. Sampled 2026-11-03: atlas slate region G~0.24
# (designed terrazzo, kept), planter region G~0.32 (too glossy for painted concrete -> ORM used for AO only, scalar
# rough 0.85); gunmetal B=1.00 / G~0.65, brushed titanium B=1.00 / G~0.37 (real metal data -> metallic 1.0 kept).
SETS = {"Stair_Slate": (ATL["albedo"], ATL["orm"], ATL["normal"], [1, 1, 1, 1], 0.0, 1.0, ("rect", g.UV_FLOOR_SLATE)),
        "Stair_Underside_PaintedConcrete": (ATL["albedo"], ATL["orm"], ATL["normal"], [0.85, 0.85, 0.85, 1], 0.0, 0.85, ("rect", g.UV_PLANTER_STONE), False),
        "Stair_WhiteComposite": (T + "facade_aerospace_white_cladding.png", None, None, [1, 1, 1, 1], 0.0, 0.5, ("tile", 1.0)),
        "Stair_Gunmetal": (T + "qa03/door_jamb_gunmetal_albedo.png", T + "qa03/door_jamb_gunmetal_orm.png", None, [1, 1, 1, 1], 1.0, 1.0, ("tile", 0.5)),
        "Stair_BrushedAlloy": (T + "qa03/rail_brushed_titanium_albedo.png", T + "qa03/rail_brushed_titanium_orm.png", None, [1, 1, 1, 1], 1.0, 1.0, ("tile", 0.5)),
        "Stair_Glass": (T + "residential_atrium_glass_translucent.png", None, None, [0.72, 0.8, 0.86, 0.25], 0.0, 0.08, ("tile", 1.0))}
MAP = {"Slate": "Stair_Slate", "WhiteComposite": "Stair_WhiteComposite", "Gunmetal": "Stair_Gunmetal", "BrushedAlloy": "Stair_BrushedAlloy", "Glass": "Stair_Glass"}
UNDER = "Stair_Underside_PaintedConcrete"
CT = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}; NC = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}
def read(J, BIN, ai):
    a = J["accessors"][ai]; v = J["bufferViews"][a["bufferView"]]; o = v.get("byteOffset", 0) + a.get("byteOffset", 0)
    return np.frombuffer(bytes(BIN[o:o + a["count"] * NC[a["type"]] * np.dtype(CT[a["componentType"]]).itemsize]), CT[a["componentType"]]).reshape(a["count"], -1)
def add(J, BIN, arr, typ, comp, tgt):
    while len(BIN) % 4: BIN.append(0)
    off = len(BIN); BIN += arr.tobytes(); J["bufferViews"].append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes, "target": tgt})
    a = {"bufferView": len(J["bufferViews"]) - 1, "componentType": comp, "count": int(len(arr)), "type": typ}
    if typ == "VEC3": a["min"] = arr.min(0).tolist(); a["max"] = arr.max(0).tolist()
    J["accessors"].append(a); return len(J["accessors"]) - 1
def uvs(P, mode):   # P: (3,3) corner positions of one triangle
    n = np.cross(P[1] - P[0], P[2] - P[0]); ax = int(np.argmax(np.abs(n))); o = [i for i in range(3) if i != ax]
    q = P[:, o]
    if mode[0] == "tile": return q / mode[1]
    u0, u1, v0, v1 = mode[1]; c = np.floor(q.mean(0) / 1.5) * 1.5; loc = np.clip((q - c) / 1.5, 0, 1)
    return np.stack([u0 + loc[:, 0] * (u1 - u0), v0 + loc[:, 1] * (v1 - v0)], 1)
def skin(path, under_meshes=()):
    b = bytearray(open(path, "rb").read()); jl = struct.unpack("<I", b[12:16])[0]
    J = json.loads(b[20:20 + jl]); bo = 20 + jl; bl = struct.unpack("<I", b[bo:bo + 4])[0]; BIN = bytearray(b[bo + 8:bo + 8 + bl])
    done = any(m.get("name", "").startswith("Stair_") for m in J["materials"])
    if done: J["images"], J["textures"] = [], []   # rerun: rebuild image/texture tables + Stair_* materials in place
    J.setdefault("images", []); J.setdefault("textures", []); J["samplers"] = [{"magFilter": 9729, "minFilter": 9987, "wrapS": 10497, "wrapT": 10497}]
    img = {}
    def tex(uri):
        if uri not in img: J["images"].append({"uri": uri}); J["textures"].append({"source": len(J["images"]) - 1, "sampler": 0}); img[uri] = len(J["textures"]) - 1
        return {"index": img[uri]}
    mid = {}
    for nm, (al, orm, nrm, f, met, rgh, _, *mr) in SETS.items():
        m = {"name": nm, "pbrMetallicRoughness": {"baseColorTexture": tex(al), "baseColorFactor": f, "metallicFactor": met, "roughnessFactor": rgh},
             "alphaMode": "BLEND" if f[3] < 1 else "OPAQUE", "doubleSided": f[3] < 1}
        if orm:
            m["occlusionTexture"] = tex(orm)
            if not mr or mr[0]: m["pbrMetallicRoughness"]["metallicRoughnessTexture"] = tex(orm)
        if nrm: m["normalTexture"] = tex(nrm)
        ex = [i for i, q in enumerate(J["materials"]) if q.get("name") == nm]
        if ex: J["materials"][ex[0]] = m; mid[nm] = ex[0]
        else: J["materials"].append(m); mid[nm] = len(J["materials"]) - 1
    tri0 = tri1 = 0; report = {}
    if done: return write(path, J, BIN, "materials updated")
    for mesh in J["meshes"]:
        if "_Col" in mesh["name"]: continue
        newp = []
        for pr in mesh["primitives"]:
            old = J["materials"][pr["material"]]["name"]; tgt = MAP.get(old)
            I = read(J, BIN, pr["indices"]).ravel(); tri0 += len(I) // 3
            if tgt is None: newp.append(pr); tri1 += len(I) // 3; continue
            P = read(J, BIN, pr["attributes"]["POSITION"])[I].reshape(-1, 3, 3)
            N = read(J, BIN, pr["attributes"]["NORMAL"])[I].reshape(-1, 3, 3)
            fn = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); fn /= np.linalg.norm(fn, axis=1, keepdims=True) + 1e-12
            down = (fn[:, 1] < -0.5) if mesh["name"] in under_meshes else np.zeros(len(P), bool)
            for mname, sel in ((tgt, ~down), (UNDER, down)):
                if not sel.any(): continue
                p, n = P[sel], N[sel]; uv = np.concatenate([uvs(t, SETS[mname][6]) for t in p]).astype(np.float32)
                p = p.reshape(-1, 3).astype(np.float32); n = n.reshape(-1, 3).astype(np.float32); idx = np.arange(len(p), dtype=np.uint32)
                newp.append({"attributes": {"POSITION": add(J, BIN, p, "VEC3", 5126, 34962), "NORMAL": add(J, BIN, n, "VEC3", 5126, 34962),
                             "TEXCOORD_0": add(J, BIN, uv, "VEC2", 5126, 34962)}, "indices": add(J, BIN, idx, "SCALAR", 5125, 34963), "mode": 4, "material": mid[mname]})
                tri1 += int(sel.sum()); report.setdefault(mesh["name"], []).append(f"{mname}:{int(sel.sum())}")
        mesh["primitives"] = newp
    assert tri0 == tri1, (tri0, tri1)
    write(path, J, BIN, f"tris {tri0} -> {tri1}"); [print(" ", k, v) for k, v in report.items()]
def write(path, J, BIN, msg):
    while len(BIN) % 4: BIN.append(0)
    J["buffers"][0]["byteLength"] = len(BIN)
    js = json.dumps(J, separators=(",", ":")).encode(); js += b" " * ((4 - len(js) % 4) % 4)
    open(path, "wb").write(struct.pack("<III", 0x46546C67, 2, 28 + len(js) + len(BIN)) + struct.pack("<II", len(js), 0x4E4F534A) + js + struct.pack("<II", len(BIN), 0x004E4942) + bytes(BIN))
    print(os.path.basename(path), msg)
if __name__ == "__main__":
    skin(os.path.join(M, "stair_set_switchback.glb"), under_meshes=("Flight1_Cast", "Flight2_Modules", "Mid_Landing", "L2_Landing"))
    skin(os.path.join(M, "stair_guard_handrail.glb"))
