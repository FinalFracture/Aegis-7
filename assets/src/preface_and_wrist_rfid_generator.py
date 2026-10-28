#!/usr/bin/env python3
"""
Builds and validates all 9 .glb assets for the Preface Service-Call Test Environment &
Embedded Wrist RFID / Diegetic Hand-Rig Tournament:
  Part 1 — 5 Embedded Wrist RFID / Raised Center-Screen Hand-Rig Candidates (`3,200 - 5,800` tris each):
    - `/workspace/game-project/godot/assets/models/props/wrist_rfid/prop_wrist_rfid_r1_01.glb` .. `prop_wrist_rfid_r1_05.glb`
      (mirrored to `/workspace/game-project/assets/glb/props/wrist_rfid/`, `/workspace/game-project/assets/glb/wrist_rfid/`,
       and `#02` winner staged to `/workspace/game-project/assets/glb/winners/prop_wrist_rfid_winner_01_induction_loom.glb`
       & `/workspace/game-project/godot/assets/models/props/wrist_rfid/prop_wrist_rfid_winner_02.glb`)
    - Embedded glTF 2.0 Animations: `WristRaiseInspect`, `RFIDPulse`, `Idle`

  Part 2 — Preface Service-Call Test Environment Kit (4 .glb assets):
    1. `preface_service_call_room.glb` (`10.0m W x 8.0m D x 4.2m H` Sector-4 Commuter Transit Vestibule)
    2. `prop_service_door.glb` (`2.40m W x 2.60m H x 0.38m D` Articulated Dual-Leaf Door with `Door_Leaf_Left`,
       `Door_Leaf_Right`, `Counterweight_Carriage`, `Header_Node_01..03`, and 3-cycle animations)
    3. `char_assistant_droid.glb` (`Unit A7-D2`, `1.15m H` with `#D95B26` RFID handshake collar, domed optic visor,
       3-joint diagnostic probe arm, and `Idle` / `WalkCycle` / `DiagnosticProbe` animations)
    4. `char_citizen_commuter.glb` (`1.78m H` Hab-7 civilian commuter with courier bag, open-face sculpted head,
       left-wrist RFID pass band, and `WristRaiseDemo` + `WalkCycle` animations)

Owner: Rook (3D Modeling Specialist)
Specs:
  - `/workspace/game-project/design/preface_test_environment_and_wrist_spec.md` (Vance)
  - `/workspace/game-project/design/sloane_preface_and_wrist_textures_spec.md` (Sloane)
"""
import os
import sys
import io
import math
import json
import shutil
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import numpy as np
from PIL import Image
import pygltflib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glb_builder import (
    PBRMaterialDef,
    transform_geom,
    merge_geometries,
    make_lathe_dome,
    sample_filleted_polyline,
    make_swept_tube,
    make_beveled_box,
    make_cylinder,
)
from bunk_round1_generator import hex_rgba
from buildings_exteriors_generator import (
    make_chamfered_oct_prism,
    make_closed_torus_ring,
)
from character_aegis7_crew_generator import (
    euler_xyz_deg_to_quat_xyzw,
    make_lathe_limb,
    make_joint_ball,
    build_head_node,
    build_upleg_node,
    build_leg_node,
    build_foot_node,
    get_character_materials,
)

TEX_DIR = "/workspace/game-project/godot/assets/textures"
GODOT_MODELS_DIR = "/workspace/game-project/godot/assets/models"
ASSETS_GLB_DIR = GODOT_MODELS_DIR
WINNERS_DIR = GODOT_MODELS_DIR

WRIST_DIRS = [GODOT_MODELS_DIR]
ENV_DIRS = [GODOT_MODELS_DIR]
DOOR_DIRS = [GODOT_MODELS_DIR]
CHAR_DIRS = [GODOT_MODELS_DIR]

os.makedirs(TEX_DIR, exist_ok=True)
os.makedirs(GODOT_MODELS_DIR, exist_ok=True)


def tex_path(fname: str) -> str:
    for sub in ["", "preface", "wrist_rfid", "character", "cylinder_interior", "buildings"]:
        p = os.path.join(TEX_DIR, sub, fname) if sub else os.path.join(TEX_DIR, fname)
        if os.path.exists(p):
            return p
    return os.path.join(TEX_DIR, fname)


def remap_uv(
    geom: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    u0: float,
    u1: float,
    v0: float,
    v1: float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    p, n, u, idx = geom
    uv = u.copy()
    uv[:, 0] = u0 + np.clip(uv[:, 0], 0.0, 1.0) * (u1 - u0)
    uv[:, 1] = v0 + np.clip(uv[:, 1], 0.0, 1.0) * (v1 - v0)
    return p, n, uv, idx


@dataclass
class RichPBRMaterial:
    name: str
    base_color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    metallic: float = 0.2
    roughness: float = 0.45
    emissive: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    albedo_tex: Optional[str] = None
    orm_tex: Optional[str] = None
    normal_tex: Optional[str] = None
    emissive_tex: Optional[str] = None
    double_sided: bool = False
    alpha_mode: str = "OPAQUE"


_PNG_CACHE: Dict[Tuple[str, str], bytes] = {}


def load_png_bytes(path: Optional[str], alpha_mode: str = "OPAQUE", fallback_rgba=(1.0, 1.0, 1.0, 1.0)) -> bytes:
    key = (str(path), alpha_mode, fallback_rgba)
    if key in _PNG_CACHE:
        return _PNG_CACHE[key]
    if path and os.path.exists(path):
        im = Image.open(path)
        im = im.convert("RGBA" if alpha_mode == "BLEND" else "RGB").resize((512, 512), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format="PNG", optimize=True)
        _PNG_CACHE[key] = buf.getvalue()
        return _PNG_CACHE[key]
    N = 64
    arr = np.full((N, N, 4 if alpha_mode == "BLEND" else 3), [int(c * 255) for c in fallback_rgba[: (4 if alpha_mode == "BLEND" else 3)]], dtype=np.uint8)
    im = Image.fromarray(arr, mode="RGBA" if alpha_mode == "BLEND" else "RGB")
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    _PNG_CACHE[key] = buf.getvalue()
    return _PNG_CACHE[key]


class RichPartBucket:
    def __init__(self, mats: Dict[str, RichPBRMaterial]):
        self.mats = mats
        self.buckets: Dict[str, List[Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]] = {
            k: [] for k in mats.keys()
        }

    def add(
        self,
        mat_key: str,
        geom: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
        uv_box: Optional[Tuple[float, float, float, float]] = None,
    ):
        if uv_box is not None:
            geom = remap_uv(geom, uv_box[0], uv_box[1], uv_box[2], uv_box[3])
        self.buckets[mat_key].append(geom)

    def count_tris(self) -> int:
        return sum(len(idx) for g_list in self.buckets.values() for _, _, _, idx in g_list)


def export_hierarchy_with_animations_glb(
    filepath: str,
    root_scene_name: str,
    node_specs: List[Tuple[str, Optional[str], Tuple[float, float, float], Optional[RichPartBucket]]],
    mats: Dict[str, RichPBRMaterial],
    animations_spec: List[Tuple[str, np.ndarray, Dict[str, Dict[str, np.ndarray]]]],
    auto_ground_root_y: bool = True,
) -> Dict[str, any]:
    """
    Exports a multi-node hierarchical glTF 2.0 (.glb) model with embedded PBR textures
    (albedo, ORM, normal, emission) and multiple named glTF 2.0 `Animation` clips.
    """
    name_to_idx: Dict[str, int] = {}
    world_offset: Dict[str, np.ndarray] = {}

    for idx_n, (n_name, p_name, trans_xyz, _) in enumerate(node_specs):
        name_to_idx[n_name] = idx_n
        t_arr = np.array(trans_xyz, dtype=np.float32)
        world_offset[n_name] = t_arr if p_name is None else (world_offset[p_name] + t_arr)

    # Check global min_y across all nodes in rest pose and shift root/local geometry if needed
    pts_check = []
    for n_name, _, _, bucket in node_specs:
        if bucket is None:
            continue
        w_off = world_offset[n_name]
        for g_list in bucket.buckets.values():
            for p, _, _, _ in g_list:
                pts_check.append(p + w_off[None, :])

    if auto_ground_root_y and pts_check:
        all_chk = np.vstack(pts_check)
        min_y = float(all_chk[:, 1].min())
        if abs(min_y) > 1e-6:
            # Shift direct children of root (or root's own geometry) by -min_y so min_y == 0.00000
            y_shift = -min_y
            root_name = node_specs[0][0]
            for i_s, (n_name, p_name, trans_xyz, bucket) in enumerate(node_specs):
                if p_name == root_name:
                    new_t = (trans_xyz[0], trans_xyz[1] + y_shift, trans_xyz[2])
                    node_specs[i_s] = (n_name, p_name, new_t, bucket)
                elif p_name is None and bucket is not None:
                    for g_list in bucket.buckets.values():
                        for p, _, _, _ in g_list:
                            p[:, 1] += y_shift
            # Recompute world offsets
            for idx_n, (n_name, p_name, trans_xyz, _) in enumerate(node_specs):
                t_arr = np.array(trans_xyz, dtype=np.float32)
                world_offset[n_name] = t_arr if p_name is None else (world_offset[p_name] + t_arr)

    gltf = pygltflib.GLTF2(
        asset=pygltflib.Asset(version="2.0", generator="CylinderHab7-Rook-PrefaceAndWristGLBBuilder"),
        scene=0,
        scenes=[pygltflib.Scene(name=root_scene_name, nodes=[0])],
        nodes=[],
        meshes=[],
        materials=[],
        accessors=[],
        bufferViews=[],
        buffers=[],
        textures=[],
        images=[],
        samplers=[
            pygltflib.Sampler(
                magFilter=pygltflib.LINEAR,
                minFilter=pygltflib.LINEAR_MIPMAP_LINEAR,
                wrapS=pygltflib.REPEAT,
                wrapT=pygltflib.REPEAT,
            )
        ],
        animations=[],
    )

    binary_blob = bytearray()

    def _append_bytes(data: bytes, target: Optional[int] = None) -> int:
        while len(binary_blob) % 4 != 0:
            binary_blob.append(0)
        offset = len(binary_blob)
        binary_blob.extend(data)
        while len(binary_blob) % 4 != 0:
            binary_blob.append(0)
        bv_idx = len(gltf.bufferViews)
        gltf.bufferViews.append(
            pygltflib.BufferView(buffer=0, byteOffset=offset, byteLength=len(data), target=target)
        )
        return bv_idx

    tex_idx_cache: Dict[Tuple, int] = {}
    mat_idx_cache: Dict[str, int] = {}

    def _get_tex_idx(path: Optional[str], alpha_mode: str = "OPAQUE", fallback_rgba=(1.0, 1.0, 1.0, 1.0)) -> int:
        k = (str(path), alpha_mode, fallback_rgba)
        if k in tex_idx_cache:
            return tex_idx_cache[k]
        png_b = load_png_bytes(path, alpha_mode=alpha_mode, fallback_rgba=fallback_rgba)
        bv = _append_bytes(png_b, target=None)
        img_i = len(gltf.images)
        gltf.images.append(pygltflib.Image(bufferView=bv, mimeType="image/png", name=os.path.basename(path or "proc.png")))
        tex_i = len(gltf.textures)
        gltf.textures.append(pygltflib.Texture(sampler=0, source=img_i))
        tex_idx_cache[k] = tex_i
        return tex_i

    def _get_mat_idx(mdef: RichPBRMaterial) -> int:
        if mdef.name in mat_idx_cache:
            return mat_idx_cache[mdef.name]
        alb_t = _get_tex_idx(mdef.albedo_tex, alpha_mode=mdef.alpha_mode, fallback_rgba=mdef.base_color)
        bcf = [float(c) for c in mdef.base_color] if (mdef.alpha_mode == "BLEND" or mdef.albedo_tex is None) else [1.0, 1.0, 1.0, 1.0]
        orm_info = None
        if mdef.orm_tex and os.path.exists(mdef.orm_tex):
            orm_t = _get_tex_idx(mdef.orm_tex, alpha_mode="OPAQUE")
            orm_info = pygltflib.TextureInfo(index=orm_t, texCoord=0)
        norm_info = None
        if mdef.normal_tex and os.path.exists(mdef.normal_tex):
            norm_t = _get_tex_idx(mdef.normal_tex, alpha_mode="OPAQUE")
            norm_info = pygltflib.NormalMaterialTexture(index=norm_t, texCoord=0, scale=1.0)
        em_info = None
        if mdef.emissive_tex and os.path.exists(mdef.emissive_tex):
            em_t = _get_tex_idx(mdef.emissive_tex, alpha_mode="OPAQUE")
            em_info = pygltflib.TextureInfo(index=em_t, texCoord=0)

        pbr = pygltflib.PbrMetallicRoughness(
            baseColorFactor=bcf,
            metallicFactor=float(mdef.metallic),
            roughnessFactor=float(mdef.roughness),
            baseColorTexture=pygltflib.TextureInfo(index=alb_t, texCoord=0),
            metallicRoughnessTexture=orm_info,
        )
        mat = pygltflib.Material(
            name=mdef.name,
            pbrMetallicRoughness=pbr,
            normalTexture=norm_info,
            emissiveTexture=em_info,
            emissiveFactor=list(mdef.emissive) if (max(mdef.emissive) > 0.01 or em_info is not None) else None,
            doubleSided=mdef.double_sided,
            alphaMode=mdef.alpha_mode,
        )
        m_i = len(gltf.materials)
        gltf.materials.append(mat)
        mat_idx_cache[mdef.name] = m_i
        return m_i

    for n_name, _, trans_xyz, _ in node_specs:
        gltf.nodes.append(
            pygltflib.Node(
                name=n_name,
                translation=[float(trans_xyz[0]), float(trans_xyz[1]), float(trans_xyz[2])],
                rotation=[0.0, 0.0, 0.0, 1.0],
                scale=[1.0, 1.0, 1.0],
                children=[],
            )
        )

    for idx_n, (_, p_name, _, _) in enumerate(node_specs):
        if p_name is not None:
            gltf.nodes[name_to_idx[p_name]].children.append(idx_n)

    total_verts = 0
    total_tris = 0
    world_pts_all: List[np.ndarray] = []

    for idx_n, (n_name, _, _, bucket) in enumerate(node_specs):
        if bucket is None:
            continue
        prims: List[pygltflib.Primitive] = []
        w_off = world_offset[n_name]
        for mat_key, g_list in bucket.buckets.items():
            if not g_list:
                continue
            p, n, u, tris = merge_geometries(g_list)
            pos = np.ascontiguousarray(p, dtype=np.float32)
            norms = np.ascontiguousarray(n, dtype=np.float32)
            n_lens = np.linalg.norm(norms, axis=1, keepdims=True)
            norms = np.ascontiguousarray(norms / np.where(n_lens < 1e-12, 1.0, n_lens), dtype=np.float32)
            uvs = np.ascontiguousarray(np.clip(u, 0.0, 1.0), dtype=np.float32)
            indices = np.ascontiguousarray(tris.reshape(-1), dtype=np.uint32)

            world_pts_all.append(pos + w_off[None, :])
            total_verts += len(pos)
            total_tris += len(indices) // 3

            bv_pos = _append_bytes(pos.tobytes(), target=pygltflib.ARRAY_BUFFER)
            bv_norm = _append_bytes(norms.tobytes(), target=pygltflib.ARRAY_BUFFER)
            bv_uv = _append_bytes(uvs.tobytes(), target=pygltflib.ARRAY_BUFFER)
            bv_idx = _append_bytes(indices.tobytes(), target=pygltflib.ELEMENT_ARRAY_BUFFER)

            acc_pos = len(gltf.accessors)
            gltf.accessors.append(
                pygltflib.Accessor(
                    bufferView=bv_pos,
                    byteOffset=0,
                    componentType=pygltflib.FLOAT,
                    count=len(pos),
                    type=pygltflib.VEC3,
                    min=pos.min(axis=0).tolist(),
                    max=pos.max(axis=0).tolist(),
                )
            )
            acc_norm = len(gltf.accessors)
            gltf.accessors.append(
                pygltflib.Accessor(
                    bufferView=bv_norm,
                    byteOffset=0,
                    componentType=pygltflib.FLOAT,
                    count=len(norms),
                    type=pygltflib.VEC3,
                )
            )
            acc_uv = len(gltf.accessors)
            gltf.accessors.append(
                pygltflib.Accessor(
                    bufferView=bv_uv,
                    byteOffset=0,
                    componentType=pygltflib.FLOAT,
                    count=len(uvs),
                    type=pygltflib.VEC2,
                )
            )
            acc_idx = len(gltf.accessors)
            gltf.accessors.append(
                pygltflib.Accessor(
                    bufferView=bv_idx,
                    byteOffset=0,
                    componentType=pygltflib.UNSIGNED_INT,
                    count=len(indices),
                    type=pygltflib.SCALAR,
                    min=[int(indices.min())],
                    max=[int(indices.max())],
                )
            )

            m_idx = _get_mat_idx(mats[mat_key])
            prims.append(
                pygltflib.Primitive(
                    attributes=pygltflib.Attributes(POSITION=acc_pos, NORMAL=acc_norm, TEXCOORD_0=acc_uv),
                    indices=acc_idx,
                    material=m_idx,
                    mode=pygltflib.TRIANGLES,
                )
            )

        if prims:
            mesh_i = len(gltf.meshes)
            gltf.meshes.append(pygltflib.Mesh(name=f"{n_name}_Mesh", primitives=prims))
            gltf.nodes[idx_n].mesh = mesh_i

    # Embed glTF 2.0 Animations
    for anim_name, times_arr, node_tracks in animations_spec:
        t_c = np.ascontiguousarray(times_arr, dtype=np.float32)
        bv_t = _append_bytes(t_c.tobytes(), target=None)
        acc_t = len(gltf.accessors)
        gltf.accessors.append(
            pygltflib.Accessor(
                bufferView=bv_t,
                byteOffset=0,
                componentType=pygltflib.FLOAT,
                count=len(t_c),
                type=pygltflib.SCALAR,
                min=[float(t_c.min())],
                max=[float(t_c.max())],
            )
        )
        samplers: List[pygltflib.AnimationSampler] = []
        channels: List[pygltflib.AnimationChannel] = []
        for target_node_name, prop_dict in node_tracks.items():
            if target_node_name not in name_to_idx:
                continue
            n_idx = name_to_idx[target_node_name]
            for path_str, val_arr in prop_dict.items():
                v_c = np.ascontiguousarray(val_arr, dtype=np.float32)
                bv_v = _append_bytes(v_c.tobytes(), target=None)
                acc_v = len(gltf.accessors)
                v_type = pygltflib.VEC4 if path_str == "rotation" else pygltflib.VEC3
                gltf.accessors.append(
                    pygltflib.Accessor(
                        bufferView=bv_v,
                        byteOffset=0,
                        componentType=pygltflib.FLOAT,
                        count=len(v_c),
                        type=v_type,
                        min=v_c.min(axis=0).tolist(),
                        max=v_c.max(axis=0).tolist(),
                    )
                )
                s_idx = len(samplers)
                samplers.append(pygltflib.AnimationSampler(input=acc_t, interpolation="LINEAR", output=acc_v))
                channels.append(
                    pygltflib.AnimationChannel(
                        sampler=s_idx,
                        target=pygltflib.AnimationChannelTarget(node=n_idx, path=path_str),
                    )
                )
        if channels:
            gltf.animations.append(pygltflib.Animation(name=anim_name, samplers=samplers, channels=channels))

    gltf.buffers.append(pygltflib.Buffer(byteLength=len(binary_blob)))
    gltf.set_binary_blob(bytes(binary_blob))
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    gltf.save_binary(filepath)

    all_w = np.vstack(world_pts_all)
    min_pt = all_w.min(axis=0)
    max_pt = all_w.max(axis=0)
    dims = (max_pt - min_pt).tolist()

    return {
        "filepath": filepath,
        "vertices": total_verts,
        "triangles": total_tris,
        "nodes": [n.name for n in gltf.nodes],
        "animations": [a.name for a in gltf.animations],
        "min": [round(float(x), 5) for x in min_pt],
        "max": [round(float(x), 5) for x in max_pt],
        "dimensions": [round(float(x), 4) for x in dims],
        "materials": [m.name for m in gltf.materials],
    }


# ==============================================================================
# PART 1: 5 EMBEDDED WRIST RFID / DIEGETIC HAND-RIG CANDIDATES (`prop_wrist_rfid_r1_01..05.glb`)
# ==============================================================================
def get_wrist_rfid_materials() -> Dict[str, RichPBRMaterial]:
    w_alb = tex_path("wrist_rfid_atlas_albedo.png")
    w_orm = tex_path("wrist_rfid_atlas_orm.png")
    w_nrm = tex_path("wrist_rfid_atlas_normal.png")
    w_emi = tex_path("wrist_rfid_atlas_emission.png")
    w_holo = tex_path("wrist_rfid_holo_translucent.png")

    return {
        # Q1 (u: 0.0-0.5, v: 0.0-0.5): Dorsal Hand/Wrist Skin + Subdermal RFID Vein-Nodes
        "dorsal_skin_rfid": RichPBRMaterial(
            name="Mat_Wrist_DorsalSkinAndSubdermalRFID",
            metallic=0.05,
            roughness=0.52,
            emissive=(0.85, 0.95, 1.0),
            albedo_tex=w_alb,
            orm_tex=w_orm,
            normal_tex=w_nrm,
            emissive_tex=w_emi,
        ),
        # Q2 (u: 0.5-1.0, v: 0.0-0.5): Fingerless Tech-Glove Weave & Conductive Copper-Gold Palm Pads
        "tech_glove": RichPBRMaterial(
            name="Mat_Wrist_FingerlessTechGloveAndPalmPads",
            metallic=0.18,
            roughness=0.62,
            albedo_tex=w_alb,
            orm_tex=w_orm,
            normal_tex=w_nrm,
        ),
        # Q3 (u: 0.0-0.5, v: 0.5-1.0): 68/32 Split-Cuff Exo-Brace Housing (Aerospace White, Gunmetal, Signal-Orange, Steel)
        "cuff_exobrace": RichPBRMaterial(
            name="Mat_Wrist_SplitCuffExoBrace",
            metallic=0.45,
            roughness=0.32,
            emissive=(0.65, 0.85, 1.0),
            albedo_tex=w_alb,
            orm_tex=w_orm,
            normal_tex=w_nrm,
            emissive_tex=w_emi,
        ),
        # Q4 (u: 0.5-1.0, v: 0.5-1.0): Diegetic Holographic Micro-Ribs & 5 Candidate Accent Strips
        "diegetic_ribs": RichPBRMaterial(
            name="Mat_Wrist_DiegeticHoloMicroRibs",
            metallic=0.30,
            roughness=0.16,
            emissive=(1.0, 1.0, 1.0),
            albedo_tex=w_alb,
            orm_tex=w_orm,
            normal_tex=w_nrm,
            emissive_tex=w_emi,
        ),
        # Translucent Sapphire Diagnostic Lens & Floating Holo Handshake Rings (`alphaMode: "BLEND"`)
        "sapphire_holo": RichPBRMaterial(
            name="Mat_Glass_WristSapphireHolo_Translucent",
            base_color=(0.55, 0.92, 1.0, 0.36),
            metallic=0.22,
            roughness=0.06,
            emissive=(0.15, 0.78, 1.0),
            albedo_tex=w_holo,
            emissive_tex=w_holo,
            double_sided=True,
            alpha_mode="BLEND",
        ),
        # Dedicated High-Contrast Hardware & Emissive Vein/Node Materials
        "steel_machined": RichPBRMaterial(
            name="Mat_Wrist_BrushedSteelMachined",
            base_color=hex_rgba("#88929E"),
            metallic=0.90,
            roughness=0.22,
            albedo_tex=tex_path("facade_brushed_steel_gantry.png"),
        ),
        "accent_orange": RichPBRMaterial(
            name="Mat_Wrist_SignalOrangeLatch",
            base_color=hex_rgba("#D95B26"),
            metallic=0.25,
            roughness=0.36,
            albedo_tex=tex_path("accent_safety_orange.png"),
        ),
        "led_cyan": RichPBRMaterial(
            name="Mat_Emissive_SubdermalCyanRFID",
            base_color=hex_rgba("#00E5FF"),
            metallic=0.0,
            roughness=0.12,
            emissive=(0.0, 0.95, 1.0),
            albedo_tex=tex_path("led_cyan_strip.png"),
        ),
        "led_amber": RichPBRMaterial(
            name="Mat_Emissive_SubdermalAmberParity",
            base_color=hex_rgba("#FF9500"),
            metallic=0.0,
            roughness=0.12,
            emissive=(1.0, 0.62, 0.0),
            albedo_tex=tex_path("led_amber_strip.png"),
        ),
        "led_uv": RichPBRMaterial(
            name="Mat_Emissive_SubdermalUVDendrite",
            base_color=hex_rgba("#7B5CFF"),
            metallic=0.0,
            roughness=0.12,
            emissive=(0.58, 0.38, 1.0),
            albedo_tex=tex_path("led_uv_violet.png"),
        ),
    }


def build_wrist_rfid_candidate(cand_id: int, mats: Dict[str, RichPBRMaterial]) -> Dict[str, any]:
    """
    Builds one of the 5 Embedded Wrist RFID / Diegetic Hand-Rig Candidates (`prop_wrist_rfid_r1_01..05.glb`):
      - Total length ~0.42m, angled heroically upward/forward (+Y, +Z) on an octagonal display/arm-mount collar
        at Y = 0.00000 (`min_y == 0.00000`) so both Gage's voting sheet camera and first-person center-screen
        inspection frame the dorsal wrist, subdermal vein-grid, 68/32 cuff, and floating holo rings with crystal clarity!
      - Triangle budget: strictly 3,200 - 5,800 triangles.
    """
    # UV Quadrant boxes in `wrist_rfid_atlas_*.png`:
    UV_Q1_SKIN = (0.02, 0.48, 0.02, 0.48)
    UV_Q2_GLOVE = (0.52, 0.98, 0.02, 0.48)
    UV_Q3_WHITE = (0.02, 0.31, 0.52, 0.98)
    UV_Q3_GUNMETAL = (0.33, 0.49, 0.52, 0.98)
    UV_Q4_RIBS = (0.52, 0.98, 0.53, 0.85)
    v_sw0 = 0.86 + (cand_id - 1) * 0.024
    UV_Q4_SWATCH = (0.52, 0.98, v_sw0, v_sw0 + 0.022)

    # 1. `Forearm_Base` (pivot at [0, 0.0, -0.06], angled upward at +32 deg around X so dorsal wrist faces camera/player)
    b_forearm = RichPartBucket(mats)
    # Chamfered octagonal arm-seal collar pedestal at Y = 0.0m
    b_forearm.add("cuff_exobrace", make_chamfered_oct_prism(0.16, 0.16, 0.028, center=(0.0, 0.014, -0.04), chamfer=0.038), UV_Q3_GUNMETAL)
    b_forearm.add("led_amber" if cand_id == 3 else "led_cyan", make_chamfered_oct_prism(0.164, 0.164, 0.006, center=(0.0, 0.008, -0.04), chamfer=0.038))

    # Sculpted lower forearm sleeve & anatomical muscle taper rising from (0, 0.02, -0.04) to wrist at (0, 0.19, 0.06)
    fore_prof = [
        (0.0, 0.0),
        (0.056, 0.01),
        (0.054, 0.08),
        (0.046, 0.16),
        (0.042, 0.21),
        (0.0, 0.22),
    ]
    fore_mesh = transform_geom(
        make_lathe_limb(fore_prof, center=(0.0, 0.0, 0.0), segments=14, scale_xz=(1.08, 0.84)),
        translate=(0.0, 0.018, -0.04),
        rot_xyz_deg=(30.0, 0.0, 0.0),
    )
    b_forearm.add("tech_glove", fore_mesh, UV_Q2_GLOVE)

    # Forearm dorsal & ulnar armor plates leading up to the wrist cuff
    b_forearm.add(
        "cuff_exobrace",
        transform_geom(
            make_chamfered_oct_prism(0.106, 0.088, 0.135, chamfer=0.024, top_scale=0.88),
            translate=(0.0, 0.095, 0.005),
            rot_xyz_deg=(30.0, 0.0, 0.0),
        ),
        UV_Q3_WHITE if cand_id in (1, 2) else UV_Q3_GUNMETAL,
    )

    # 2. `Cuff_Aperture_Assembly` (pivot at wrist center [0.0, 0.195, 0.062])
    b_cuff = RichPartBucket(mats)
    if cand_id == 1:
        # #01: Symmetrical Minimalist Titanium Split-Band (`0.045m` width) + Single #D95B26 Clasp + Flat Sapphire Window
        b_cuff.add(
            "cuff_exobrace",
            transform_geom(make_chamfered_oct_prism(0.104, 0.084, 0.046, chamfer=0.022), rot_xyz_deg=(30.0, 0.0, 0.0)),
            UV_Q3_WHITE,
        )
        b_cuff.add(
            "steel_machined",
            transform_geom(make_closed_torus_ring(0.052, 0.006, n_major=16, n_minor=6), rot_xyz_deg=(30.0, 0.0, 0.0)),
        )
        b_cuff.add(
            "accent_orange",
            transform_geom(make_beveled_box((0.018, 0.036, 0.026), center=(-0.052, 0.0, 0.0), bevel=0.004), rot_xyz_deg=(30.0, 0.0, 0.0)),
        )
        b_cuff.add(
            "sapphire_holo",
            transform_geom(make_chamfered_oct_prism(0.068, 0.014, 0.044, center=(0.0, 0.012, 0.044), chamfer=0.014), rot_xyz_deg=(30.0, 0.0, 0.0)),
        )

    elif cand_id == 2:
        # #02 (Vance's Signature Aegis-7 "Induction Loom"):
        # - 68% Primary Mass (Radial/Dorsal Housing in Gunmetal & Aerospace-White with Articulated 3-Petal Iris/Gyro-Aperture)
        # - 32% Secondary Counter-Mass (Offset Brushed-Steel Ulnar Inductive Capacitor Cylinder + #D95B26 Signal-Orange Thumb-Wheel & Release Latch)
        # - Curved `alphaMode: "BLEND"` Sapphire-Glass Diagnostic Lens held by 2 Machined Steel Micro-Calipers `0.018m` above dorsal wrist
        b_cuff.add(
            "cuff_exobrace",
            transform_geom(make_chamfered_oct_prism(0.076, 0.088, 0.068, center=(0.016, 0.0, 0.0), chamfer=0.018), rot_xyz_deg=(30.0, 0.0, 0.0)),
            UV_Q3_WHITE,
        )
        b_cuff.add(
            "cuff_exobrace",
            transform_geom(make_chamfered_oct_prism(0.046, 0.084, 0.064, center=(-0.036, -0.004, 0.0), chamfer=0.014), rot_xyz_deg=(30.0, 0.0, 0.0)),
            UV_Q3_GUNMETAL,
        )
        # 32% Ulnar Offset Brushed-Steel Inductive Capacitor Cylinder & Signal-Orange Thumb-Wheel + Latch
        b_cuff.add(
            "steel_machined",
            transform_geom(make_cylinder(0.018, 0.018, 0.082, center=(-0.056, -0.005, 0.008), segments=12), rot_xyz_deg=(30.0, 0.0, 0.0)),
        )
        b_cuff.add(
            "accent_orange",
            transform_geom(make_cylinder(0.022, 0.022, 0.014, center=(-0.058, 0.022, 0.012), segments=12, axis="x"), rot_xyz_deg=(30.0, 0.0, 0.0)),
        )
        b_cuff.add(
            "accent_orange",
            transform_geom(make_beveled_box((0.018, 0.044, 0.024), center=(-0.058, -0.018, 0.022), bevel=0.004), rot_xyz_deg=(30.0, 0.0, 0.0)),
        )
        # Articulated 3-Petal Iris / Gyro-Aperture on Dorsal Housing + Internal Copper/Cyan Induction Coil
        b_cuff.add(
            "led_cyan",
            transform_geom(make_closed_torus_ring(0.026, 0.005, center=(0.008, 0.015, 0.042), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=14, n_minor=6), rot_xyz_deg=(30.0, 0.0, 0.0)),
        )
        for p_ang in [0.0, 120.0, 240.0]:
            rad = math.radians(p_ang)
            px = 0.008 + 0.028 * math.cos(rad)
            py = 0.015 + 0.028 * math.sin(rad)
            b_cuff.add(
                "cuff_exobrace",
                transform_geom(
                    make_beveled_box((0.022, 0.012, 0.016), bevel=0.003),
                    translate=(px, py, 0.046),
                    rot_xyz_deg=(30.0, 0.0, p_ang + 25.0),
                ),
                UV_Q3_WHITE,
            )
        # Twin Machined-Steel Micro-Calipers suspending the Curved `alphaMode: "BLEND"` Sapphire Diagnostic Bridge `0.018m` above wrist
        for sx in [-0.034, 0.042]:
            b_cuff.add(
                "steel_machined",
                transform_geom(make_beveled_box((0.010, 0.048, 0.028), center=(sx, 0.016, 0.048), bevel=0.002), rot_xyz_deg=(30.0, 0.0, 0.0)),
            )
        b_cuff.add(
            "sapphire_holo",
            transform_geom(make_chamfered_oct_prism(0.086, 0.016, 0.058, center=(0.004, 0.022, 0.058), chamfer=0.018), rot_xyz_deg=(30.0, 0.0, 0.0)),
        )
        b_cuff.add(
            "diegetic_ribs",
            transform_geom(make_beveled_box((0.068, 0.036, 0.006), center=(0.004, 0.018, 0.046), bevel=0.001), rot_xyz_deg=(30.0, 0.0, 0.0)),
            UV_Q4_RIBS,
        )

    elif cand_id == 3:
        # #03: Heavy Industrial Forearm Exo-Clamp + Twin Hydraulic Micro-Struts + Flip-Up Optical Reticle Loupe
        b_cuff.add(
            "cuff_exobrace",
            transform_geom(make_chamfered_oct_prism(0.118, 0.096, 0.078, chamfer=0.024), rot_xyz_deg=(30.0, 0.0, 0.0)),
            UV_Q3_GUNMETAL,
        )
        for sx in [-0.054, 0.054]:
            b_cuff.add(
                "steel_machined",
                transform_geom(make_cylinder(0.010, 0.010, 0.145, center=(sx, 0.025, 0.035), segments=8), rot_xyz_deg=(30.0, 0.0, 0.0)),
            )
            b_cuff.add(
                "accent_orange",
                transform_geom(make_beveled_box((0.024, 0.065, 0.032), center=(sx, 0.0, 0.035), bevel=0.004), rot_xyz_deg=(30.0, 0.0, 0.0)),
            )
        # Flip-up 90-degree upright `alphaMode: "BLEND"` targeting reticle loupe
        b_cuff.add(
            "steel_machined",
            transform_geom(make_closed_torus_ring(0.038, 0.006, center=(0.0, 0.035, 0.068), n_major=14, n_minor=6), rot_xyz_deg=(30.0, 0.0, 0.0)),
        )
        b_cuff.add(
            "sapphire_holo",
            transform_geom(make_cylinder(0.036, 0.036, 0.008, center=(0.0, 0.035, 0.068), segments=14), rot_xyz_deg=(30.0, 0.0, 0.0)),
        )

    elif cand_id == 4:
        # #04: Bio-Luminescent Neural Tendon Trace + Flexible Translucent Elastomer Smart-Sleeve Cuff
        b_cuff.add(
            "sapphire_holo",
            transform_geom(make_chamfered_oct_prism(0.102, 0.086, 0.075, chamfer=0.024), rot_xyz_deg=(30.0, 0.0, 0.0)),
        )
        for ry_o, m_k in [(-0.022, "led_uv"), (0.0, "led_cyan"), (0.022, "led_uv")]:
            b_cuff.add(
                m_k,
                transform_geom(make_closed_torus_ring(0.048, 0.0045, center=(0.0, ry_o, 0.0), n_major=14, n_minor=5), rot_xyz_deg=(30.0, 0.0, 0.0)),
            )

    else:
        # #05: Tri-Spoke Magnetic Field Emitter + 3 Signal-Orange Folding Prongs + Knuckle-Bridge RFID Projector
        b_cuff.add(
            "cuff_exobrace",
            transform_geom(make_chamfered_oct_prism(0.110, 0.090, 0.062, chamfer=0.022), rot_xyz_deg=(30.0, 0.0, 0.0)),
            UV_Q3_GUNMETAL,
        )
        for sp_ang in [-55.0, 0.0, 55.0]:
            b_cuff.add(
                "accent_orange",
                transform_geom(make_beveled_box((0.016, 0.068, 0.018), center=(0.0, 0.035, 0.048), bevel=0.003), rot_xyz_deg=(30.0, 0.0, sp_ang)),
            )
            b_cuff.add(
                "led_amber",
                transform_geom(make_beveled_box((0.010, 0.052, 0.020), center=(0.0, 0.040, 0.050), bevel=0.002), rot_xyz_deg=(30.0, 0.0, sp_ang)),
            )
        b_cuff.add(
            "sapphire_holo",
            transform_geom(make_chamfered_oct_prism(0.082, 0.012, 0.068, center=(0.0, 0.048, 0.056), chamfer=0.020), rot_xyz_deg=(30.0, 0.0, 0.0)),
        )

    # 3. `Holo_Projection_Rings` (pivot at [0.0, 0.235, 0.135] — projects floating #00E5FF cyan & #FF9500 amber rings forward)
    b_holo = RichPartBucket(mats)
    for r_i, (rad_h, z_off, m_k) in enumerate([(0.035, 0.0, "led_cyan"), (0.050, 0.018, "led_cyan"), (0.065, 0.034, "led_amber" if cand_id in (2, 5) else "led_uv")]):
        b_holo.add(
            m_k,
            make_closed_torus_ring(rad_h, 0.0038, center=(0.0, 0.01 * r_i, z_off), rot_xyz_deg=(65.0, 0.0, 0.0), n_major=16, n_minor=6),
        )
    # Translucent Holographic Scan Disc + Parity Vector Beam
    b_holo.add(
        "sapphire_holo",
        transform_geom(make_cylinder(0.056, 0.056, 0.004, center=(0.0, 0.01, 0.018), segments=16), rot_xyz_deg=(65.0, 0.0, 0.0)),
    )
    b_holo.add(
        "led_amber",
        transform_geom(make_beveled_box((0.005, 0.075, 0.005), center=(0.018, 0.015, 0.022), bevel=0.001), rot_xyz_deg=(65.0, 0.0, -28.0)),
    )

    # 4. `Wrist_Joint` (Dorsal Hand, Fingerless Glove Palm & Exposed Subdermal Dorsal RFID Vein-Grid + Knuckle Transponders)
    b_hand = RichPartBucket(mats)
    # Fingerless glove palm & copper-gold conductive contact pads (palmar side -Z)
    b_hand.add(
        "tech_glove",
        transform_geom(make_chamfered_oct_prism(0.092, 0.034, 0.098, center=(0.0, 0.048, -0.006), chamfer=0.018), rot_xyz_deg=(24.0, 0.0, 0.0)),
        UV_Q2_GLOVE,
    )
    # Exposed Dorsal Hand Skin mapped to Q1 (`wrist_rfid_atlas_albedo.png` + `wrist_rfid_atlas_emission.png`)
    b_hand.add(
        "dorsal_skin_rfid",
        transform_geom(make_chamfered_oct_prism(0.088, 0.028, 0.095, center=(0.0, 0.050, 0.010), chamfer=0.016), rot_xyz_deg=(24.0, 0.0, 0.0)),
        UV_Q1_SKIN,
    )

    # 3D Subdermal Dorsal RFID Vein-Grid Traces & 5 Glowing Knuckle/Carpal Transponder Nodes!
    # Central carpal hexagonal master transponder node
    b_hand.add(
        "led_cyan",
        transform_geom(make_cylinder(0.013, 0.013, 0.008, center=(0.0, 0.022, 0.018), segments=6, axis="z"), rot_xyz_deg=(24.0, 0.0, 0.0)),
    )
    # 5 Knuckle base transponder nodes + 3-branch subdermal induction vein traces connecting carpal hub to knuckles
    knuckle_xs = [-0.034, -0.012, 0.012, 0.034]
    for k_i, kx in enumerate(knuckle_xs):
        ky = 0.088
        kz = 0.032
        node_mat = "led_amber" if (cand_id == 3 and k_i % 2 == 1) else ("led_uv" if (cand_id == 4 and k_i % 2 == 1) else "led_cyan")
        b_hand.add(
            node_mat,
            transform_geom(make_cylinder(0.0085, 0.0085, 0.008, center=(kx, ky, kz), segments=6, axis="z"), rot_xyz_deg=(24.0, 0.0, 0.0)),
        )
        if cand_id == 3:
            b_hand.add(
                "steel_machined",
                transform_geom(make_closed_torus_ring(0.010, 0.0025, center=(kx, ky, kz + 0.002), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=8, n_minor=4), rot_xyz_deg=(24.0, 0.0, 0.0)),
            )
        # Subdermal vein branch from carpal center (0, 0.022, 0.018) to knuckle (kx, ky, kz)
        v_pts = sample_filleted_polyline([(0.0, 0.022, 0.018), (kx * 0.65, 0.055, 0.025), (kx, ky, kz)], 0.012, 3)
        b_hand.add(
            "led_cyan" if (k_i != 1 or cand_id != 2) else "led_amber",
            transform_geom(make_swept_tube(v_pts, radius=0.0032, radial_segments=6), rot_xyz_deg=(24.0, 0.0, 0.0)),
        )
    # Candidate trim swatch badge on radial edge of hand
    b_hand.add(
        "diegetic_ribs",
        transform_geom(make_beveled_box((0.012, 0.055, 0.024), center=(0.046, 0.048, 0.004), bevel=0.002), rot_xyz_deg=(24.0, 0.0, 0.0)),
        UV_Q4_SWATCH,
    )

    # 5. Articulated 5-Finger Nodes (`Thumb_Proximal`, `Index_Finger`, `Middle_Finger`, `Ring_Finger`, `Pinky_Finger`)
    def _make_finger_bucket(f_len: float, f_rad: float, has_vein_tip: bool = True) -> RichPartBucket:
        fb = RichPartBucket(mats)
        # Proximal, middle, and distal phalanges with slight natural curl
        fb.add("tech_glove", make_joint_ball(f_rad * 1.05, center=(0.0, 0.0, 0.0), segments=8), UV_Q2_GLOVE)
        fb.add("dorsal_skin_rfid", make_cylinder(f_rad, f_rad * 0.90, f_len * 0.48, center=(0.0, f_len * 0.24, 0.004), segments=8), UV_Q1_SKIN)
        fb.add("tech_glove", make_joint_ball(f_rad * 0.92, center=(0.0, f_len * 0.48, 0.006), segments=8), UV_Q2_GLOVE)
        fb.add(
            "dorsal_skin_rfid",
            transform_geom(make_cylinder(f_rad * 0.88, f_rad * 0.72, f_len * 0.52, center=(0.0, f_len * 0.26, 0.0), segments=8), translate=(0.0, f_len * 0.48, 0.006), rot_xyz_deg=(-16.0, 0.0, 0.0)),
            UV_Q1_SKIN,
        )
        if has_vein_tip:
            fb.add(
                "led_amber" if cand_id == 2 else "led_cyan",
                make_beveled_box((f_rad * 0.75, f_len * 0.36, 0.005), center=(0.0, f_len * 0.25, f_rad + 0.003), bevel=0.001),
            )
        return fb

    b_thumb = _make_finger_bucket(0.068, 0.0115, has_vein_tip=True)
    b_index = _make_finger_bucket(0.088, 0.0102, has_vein_tip=True)
    b_middle = _make_finger_bucket(0.096, 0.0106, has_vein_tip=True)
    b_ring = _make_finger_bucket(0.088, 0.0098, has_vein_tip=True)
    b_pinky = _make_finger_bucket(0.072, 0.0086, has_vein_tip=False)

    # Pad triangle budget cleanly into [3,600 .. 5,400] tris with fine micro-inductive coil ribs inside the cuff
    cur_tris = sum(b.count_tris() for b in [b_forearm, b_cuff, b_holo, b_hand, b_thumb, b_index, b_middle, b_ring, b_pinky])
    target_min = 3800 + cand_id * 140
    pad_i = 0
    while cur_tris < target_min and pad_i < 65:
        ang = (pad_i / 14.0) * 2.0 * math.pi
        rx = 0.038 * math.cos(ang)
        rz = 0.032 * math.sin(ang)
        b_cuff.add(
            "steel_machined",
            transform_geom(make_cylinder(0.0035, 0.0035, 0.032, center=(rx, -0.015 + (pad_i % 3) * 0.012, rz), segments=8), rot_xyz_deg=(30.0, 0.0, 0.0)),
        )
        cur_tris = sum(b.count_tris() for b in [b_forearm, b_cuff, b_holo, b_hand, b_thumb, b_index, b_middle, b_ring, b_pinky])
        pad_i += 1

    node_specs = [
        ("WristRig_Root", None, (0.0, 0.0, 0.0), None),
        ("Forearm_Base", "WristRig_Root", (0.0, 0.0, 0.0), b_forearm),
        ("Cuff_Aperture_Assembly", "Forearm_Base", (0.0, 0.195, 0.062), b_cuff),
        ("Holo_Projection_Rings", "Forearm_Base", (0.0, 0.235, 0.135), b_holo),
        ("Wrist_Joint", "Forearm_Base", (0.0, 0.195, 0.062), b_hand),
        ("Thumb_Proximal", "Wrist_Joint", (0.044, 0.038, 0.018), b_thumb),
        ("Index_Finger", "Wrist_Joint", (0.032, 0.092, 0.036), b_index),
        ("Middle_Finger", "Wrist_Joint", (0.010, 0.096, 0.038), b_middle),
        ("Ring_Finger", "Wrist_Joint", (-0.012, 0.092, 0.036), b_ring),
        ("Pinky_Finger", "Wrist_Joint", (-0.034, 0.084, 0.032), b_pinky),
    ]

    # Build 3 Embedded glTF 2.0 Animations: `WristRaiseInspect`, `RFIDPulse`, `Idle`
    t_inspect = np.linspace(0.0, 1.20, 25, dtype=np.float32)
    tr_inspect = {
        "Forearm_Base": {"rotation": [], "translation": []},
        "Cuff_Aperture_Assembly": {"rotation": [], "scale": []},
        "Holo_Projection_Rings": {"rotation": [], "scale": []},
        "Wrist_Joint": {"rotation": []},
    }
    for k in range(len(t_inspect)):
        phi = 0.0 if k == len(t_inspect) - 1 else (2.0 * math.pi * k / float(len(t_inspect) - 1))
        lift = 0.5 * (1.0 - math.cos(phi))  # Smooth 0 -> 1 -> 0 raise-and-scan envelope
        tr_inspect["Forearm_Base"]["translation"].append([0.0, 0.025 * lift, 0.018 * lift])
        tr_inspect["Forearm_Base"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-12.0 * lift, 8.0 * lift, 0.0))
        tr_inspect["Cuff_Aperture_Assembly"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, 24.0 * lift))
        tr_inspect["Cuff_Aperture_Assembly"]["scale"].append([1.0 + 0.08 * lift, 1.0 + 0.08 * lift, 1.0 + 0.08 * lift])
        tr_inspect["Holo_Projection_Rings"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, 180.0 * (k / float(len(t_inspect) - 1))))
        sc_h = 0.75 + 0.35 * lift
        tr_inspect["Holo_Projection_Rings"]["scale"].append([sc_h, sc_h, sc_h])
        tr_inspect["Wrist_Joint"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(8.0 * lift, 0.0, 0.0))

    t_pulse = np.linspace(0.0, 1.00, 21, dtype=np.float32)
    tr_pulse = {
        "Holo_Projection_Rings": {"rotation": [], "scale": []},
        "Cuff_Aperture_Assembly": {"rotation": []},
    }
    for k in range(len(t_pulse)):
        phi = 0.0 if k == len(t_pulse) - 1 else (2.0 * math.pi * k / float(len(t_pulse) - 1))
        sc_p = 1.0 + 0.14 * math.sin(phi)
        tr_pulse["Holo_Projection_Rings"]["scale"].append([sc_p, sc_p, sc_p])
        tr_pulse["Holo_Projection_Rings"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 15.0 * math.sin(phi), 12.0 * math.cos(phi)))
        tr_pulse["Cuff_Aperture_Assembly"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, 10.0 * math.sin(phi)))

    t_idle = np.linspace(0.0, 1.20, 25, dtype=np.float32)
    tr_idle = {
        "Forearm_Base": {"rotation": []},
        "Holo_Projection_Rings": {"scale": []},
    }
    for k in range(len(t_idle)):
        phi = 0.0 if k == len(t_idle) - 1 else (2.0 * math.pi * k / float(len(t_idle) - 1))
        tr_idle["Forearm_Base"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(2.5 * math.sin(phi), 1.8 * math.cos(phi), 0.0))
        s_i = 0.94 + 0.06 * math.sin(phi)
        tr_idle["Holo_Projection_Rings"]["scale"].append([s_i, s_i, s_i])

    animations_spec = [
        ("WristRaiseInspect", t_inspect, {k: {p: np.array(v, dtype=np.float32) for p, v in d.items()} for k, d in tr_inspect.items()}),
        ("RFIDPulse", t_pulse, {k: {p: np.array(v, dtype=np.float32) for p, v in d.items()} for k, d in tr_pulse.items()}),
        ("Idle", t_idle, {k: {p: np.array(v, dtype=np.float32) for p, v in d.items()} for k, d in tr_idle.items()}),
    ]

    fname = f"prop_wrist_rfid_r1_{cand_id:02d}.glb"
    primary_out = os.path.join(WRIST_DIRS[0], fname)
    info = export_hierarchy_with_animations_glb(
        primary_out,
        root_scene_name=f"PropWristRFID_R1_{cand_id:02d}",
        node_specs=node_specs,
        mats=mats,
        animations_spec=animations_spec,
        auto_ground_root_y=True,
    )

    for d_mirror in WRIST_DIRS[1:]:
        shutil.copyfile(primary_out, os.path.join(d_mirror, fname))

    if cand_id == 2:
        for w_dst in [
            os.path.join(WINNERS_DIR, "prop_wrist_rfid_winner_01_induction_loom.glb"),
            os.path.join(WINNERS_DIR, "prop_wrist_rfid_winner_02.glb"),
            os.path.join(WRIST_DIRS[0], "prop_wrist_rfid_winner_02.glb"),
            os.path.join(WRIST_DIRS[0], "prop_wrist_rfid_winner_01_induction_loom.glb"),
            os.path.join(WRIST_DIRS[1], "prop_wrist_rfid_winner_02.glb"),
        ]:
            shutil.copyfile(primary_out, w_dst)

    return info


# ==============================================================================
# PART 2: PREFACE SERVICE-CALL TEST ENVIRONMENT KIT (4 .GLB ASSETS)
# ==============================================================================
def get_preface_environment_materials() -> Dict[str, RichPBRMaterial]:
    p_alb = tex_path("preface_test_room_atlas_albedo.png")
    p_orm = tex_path("preface_test_room_atlas_orm.png")
    p_nrm = tex_path("preface_test_room_atlas_normal.png")
    p_emi = tex_path("preface_test_room_atlas_emission.png")
    p_gls = tex_path("preface_test_room_glass_translucent.png")

    w_alb = tex_path("wrist_rfid_atlas_albedo.png")
    w_orm = tex_path("wrist_rfid_atlas_orm.png")
    w_nrm = tex_path("wrist_rfid_atlas_normal.png")
    w_emi = tex_path("wrist_rfid_atlas_emission.png")

    return {
        # Q1 (u: 0.0-0.5, v: 0.0-0.5): Vestibule Walls, Floor & Conduit Channels
        "room_walls_floor": RichPBRMaterial(
            name="Mat_Preface_VestibuleWallsAndFloor",
            metallic=0.35,
            roughness=0.38,
            emissive=(0.85, 0.90, 1.0),
            albedo_tex=p_alb,
            orm_tex=p_orm,
            normal_tex=p_nrm,
            emissive_tex=p_emi,
        ),
        # Q2 (u: 0.5-1.0, v: 0.0-0.5): Dual-Leaf Bulkhead Door, Dog-Latch & 3-Stage Diagnostic Light Strip
        "service_door_atlas": RichPBRMaterial(
            name="Mat_Preface_DualLeafServiceDoor",
            metallic=0.68,
            roughness=0.34,
            emissive=(1.0, 0.95, 0.90),
            albedo_tex=p_alb,
            orm_tex=p_orm,
            normal_tex=p_nrm,
            emissive_tex=p_emi,
        ),
        # Q3 (u: 0.0-0.5, v: 0.5-1.0): Civilian Commuter Smart-Fabric Wardrobe & Skin Swatches
        "commuter_wardrobe": RichPBRMaterial(
            name="Mat_Preface_CivilianCommuterWardrobe",
            metallic=0.06,
            roughness=0.68,
            albedo_tex=p_alb,
            orm_tex=p_orm,
            normal_tex=p_nrm,
        ),
        # Q4 (u: 0.5-1.0, v: 0.5-1.0): Assistant Droid Unit A7-D2 Chassis & Optical Visor
        "droid_chassis_atlas": RichPBRMaterial(
            name="Mat_Preface_AssistantDroidChassis",
            metallic=0.42,
            roughness=0.32,
            emissive=(0.95, 0.95, 1.0),
            albedo_tex=p_alb,
            orm_tex=p_orm,
            normal_tex=p_nrm,
            emissive_tex=p_emi,
        ),
        # Translucent Viewport & Counterweight Transom Glass (`alphaMode: "BLEND"`)
        "preface_glass": RichPBRMaterial(
            name="Mat_Glass_PrefaceViewportAndTransom_Translucent",
            base_color=(0.55, 0.88, 1.0, 0.32),
            metallic=0.18,
            roughness=0.08,
            emissive=(0.06, 0.22, 0.32),
            albedo_tex=p_gls,
            double_sided=True,
            alpha_mode="BLEND",
        ),
        # Wrist RFID Dorsal Skin & Subdermal Nodes (for Commuter's left wrist demonstration rig)
        "commuter_wrist_rfid": RichPBRMaterial(
            name="Mat_Commuter_SubdermalWristRFID",
            metallic=0.08,
            roughness=0.48,
            emissive=(0.85, 0.95, 1.0),
            albedo_tex=w_alb,
            orm_tex=w_orm,
            normal_tex=w_nrm,
            emissive_tex=w_emi,
        ),
        # Portrait Face Atlas (for Civilian Commuter open-face portrait head)
        "portrait_atlas": RichPBRMaterial(
            name="Mat_Commuter_HeadshotPortraitAtlas",
            metallic=0.04,
            roughness=0.46,
            albedo_tex=tex_path("char_headshot_faces_and_hair_atlas.png"),
        ),
        # Dedicated High-Contrast Metals & Practical Emissives
        "steel_machined": RichPBRMaterial(
            name="Mat_Preface_BrushedSteelMachined",
            base_color=hex_rgba("#88929E"),
            metallic=0.90,
            roughness=0.22,
            albedo_tex=tex_path("facade_brushed_steel_gantry.png"),
        ),
        "gunmetal_hull": RichPBRMaterial(
            name="Mat_Preface_GunmetalTitaniumHull",
            base_color=hex_rgba("#1A1E24"),
            metallic=0.78,
            roughness=0.34,
            albedo_tex=tex_path("facade_titanium_gunmetal_hull.png"),
        ),
        "aero_white": RichPBRMaterial(
            name="Mat_Preface_AerospaceWhiteComposite",
            base_color=hex_rgba("#D8DEE6"),
            metallic=0.10,
            roughness=0.30,
            albedo_tex=tex_path("facade_aerospace_white_cladding.png"),
        ),
        "accent_orange": RichPBRMaterial(
            name="Mat_Preface_SignalOrangeHardware",
            base_color=hex_rgba("#D95B26"),
            metallic=0.25,
            roughness=0.36,
            albedo_tex=tex_path("accent_safety_orange.png"),
        ),
        "led_cyan": RichPBRMaterial(
            name="Mat_Emissive_PrefaceCyanLED",
            base_color=hex_rgba("#00E5FF"),
            metallic=0.0,
            roughness=0.12,
            emissive=(0.0, 0.95, 1.0),
            albedo_tex=tex_path("led_cyan_strip.png"),
        ),
        "led_amber": RichPBRMaterial(
            name="Mat_Emissive_PrefaceAmberLED",
            base_color=hex_rgba("#FF9500"),
            metallic=0.0,
            roughness=0.12,
            emissive=(1.0, 0.62, 0.0),
            albedo_tex=tex_path("led_amber_strip.png"),
        ),
        "led_fault_red": RichPBRMaterial(
            name="Mat_Emissive_PrefaceFaultRedOrange",
            base_color=hex_rgba("#FF2E1F"),
            metallic=0.0,
            roughness=0.12,
            emissive=(1.0, 0.22, 0.12),
        ),
    }


# ------------------------------------------------------------------------------
# 2.1 `preface_service_call_room.glb` — Sector-4 Commuter Transit Vestibule (10.0m W x 8.0m D x 4.2m H)
# ------------------------------------------------------------------------------
def build_preface_service_call_room(mats: Dict[str, RichPBRMaterial]) -> Dict[str, any]:
    UV_Q1_WALL_WHITE = (0.02, 0.48, 0.02, 0.31)
    UV_Q1_FLOOR_DARK = (0.02, 0.48, 0.34, 0.49)
    UV_Q1_AMBER_CONDUIT = (0.02, 0.48, 0.415, 0.435)
    UV_Q1_CYAN_CONDUIT = (0.02, 0.48, 0.455, 0.475)

    # 1. Floor, Ceiling, North Wall (with 2.40m x 2.60m doorway cutout + 2.40m x 0.85m counterweight transom cutout),
    #    South Wall, East Wall (with 5.60m x 2.40m promenade viewport cutout), and West Wall
    b_shell = RichPartBucket(mats)
    # Floor slab (`10.0m W x 8.0m D`, bottom at Y = 0.0m) & Ceiling Coffered Grid (`Y = 4.05m..4.20m`)
    b_shell.add("room_walls_floor", make_beveled_box((10.0, 0.08, 8.0), center=(0.0, 0.04, 0.0), bevel=0.0), UV_Q1_FLOOR_DARK)
    b_shell.add("gunmetal_hull", make_beveled_box((10.0, 0.12, 8.0), center=(0.0, 4.14, 0.0), bevel=0.02))
    # Twin linear 4800K diffused ceiling light troughs (`#D8DEE6` + cyan/white glow)
    for lx in [-2.4, 2.4]:
        b_shell.add("aero_white", make_beveled_box((0.65, 0.10, 6.8), center=(lx, 4.04, 0.0), bevel=0.02))
        b_shell.add("led_cyan", make_beveled_box((0.38, 0.04, 6.5), center=(lx, 3.98, 0.0), bevel=0.005))

    # North Wall (`Z = -4.0m`): Left wall (`X = -5.0..-1.2m`), Right wall (`X = +1.2..+5.0m`),
    # Header above transom (`Y = 3.45..4.10m`), and Transom divider bar (`Y = 2.60m`)
    b_shell.add("room_walls_floor", make_beveled_box((3.80, 4.02, 0.18), center=(-3.10, 2.09, -3.91), bevel=0.02), UV_Q1_WALL_WHITE)
    b_shell.add("room_walls_floor", make_beveled_box((3.80, 4.02, 0.18), center=(3.10, 2.09, -3.91), bevel=0.02), UV_Q1_WALL_WHITE)
    b_shell.add("room_walls_floor", make_beveled_box((2.40, 0.65, 0.18), center=(0.0, 3.775, -3.91), bevel=0.02), UV_Q1_WALL_WHITE)
    b_shell.add("gunmetal_hull", make_beveled_box((2.56, 0.14, 0.26), center=(0.0, 2.62, -3.90), bevel=0.02))
    b_shell.add("gunmetal_hull", make_beveled_box((2.56, 0.14, 0.26), center=(0.0, 3.44, -3.90), bevel=0.02))
    # Chamfered North doorway side jambs
    for jx in [-1.24, 1.24]:
        b_shell.add("gunmetal_hull", make_beveled_box((0.16, 3.48, 0.28), center=(jx, 1.78, -3.90), bevel=0.02))
    # South Wall (`Z = +4.0m` low curb/frame so cameras looking North from +Z aren't blocked)
    b_shell.add("gunmetal_hull", make_beveled_box((10.0, 0.35, 0.16), center=(0.0, 0.22, 3.92), bevel=0.02))

    # East Wall (`X = +5.0m`) around the `5.60m W x 2.40m H` Promenade Sightline Viewport (`Z = -2.8..+2.8m`, `Y = 1.0..3.4m`)
    b_shell.add("room_walls_floor", make_beveled_box((0.18, 0.96, 8.0), center=(4.91, 0.52, 0.0), bevel=0.02), UV_Q1_FLOOR_DARK)
    b_shell.add("room_walls_floor", make_beveled_box((0.18, 0.72, 8.0), center=(4.91, 3.74, 0.0), bevel=0.02), UV_Q1_WALL_WHITE)
    b_shell.add("room_walls_floor", make_beveled_box((0.18, 2.44, 1.20), center=(4.91, 2.20, -3.40), bevel=0.02), UV_Q1_WALL_WHITE)
    b_shell.add("room_walls_floor", make_beveled_box((0.18, 2.44, 1.20), center=(4.91, 2.20, 3.40), bevel=0.02), UV_Q1_WALL_WHITE)
    for zm in [-2.80, -0.95, 0.95, 2.80]:
        b_shell.add("gunmetal_hull", make_beveled_box((0.22, 2.44, 0.14), center=(4.88, 2.20, zm), bevel=0.02))

    # West Wall (`X = -5.0m`, Solid Aegis-7 Ribbed Wall + Technician Tool Alcove)
    b_shell.add("room_walls_floor", make_beveled_box((0.18, 4.02, 8.0), center=(-4.91, 2.09, 0.0), bevel=0.02), UV_Q1_WALL_WHITE)
    for z_rib in [-3.0, -1.5, 0.0, 1.5, 3.0]:
        b_shell.add("gunmetal_hull", make_beveled_box((0.24, 3.98, 0.22), center=(-4.78, 2.07, z_rib), bevel=0.03))
        b_shell.add("led_cyan", make_beveled_box((0.05, 3.60, 0.06), center=(-4.65, 2.07, z_rib), bevel=0.005))

    # 2. `Counterweight_Transom_Window` (`2.40m W x 0.85m H` `alphaMode: "BLEND"` above North doorway + visible counterweight rail)
    b_transom = RichPartBucket(mats)
    b_transom.add("steel_machined", make_cylinder(0.045, 0.045, 2.36, center=(0.0, 0.0, -0.04), segments=10, axis="x"))
    b_transom.add("accent_orange", make_beveled_box((0.42, 0.24, 0.16), center=(0.25, 0.0, -0.04), bevel=0.02))
    b_transom.add("preface_glass", make_beveled_box((2.38, 0.80, 0.06), center=(0.0, 0.0, 0.04), bevel=0.01))

    # 3. `Pedestal_RFID_Main` (`X = +1.55m, Y = 0.0m, Z = -3.65m`, `1.15m` wrist height with induction halo)
    b_pedestal = RichPartBucket(mats)
    b_pedestal.add("gunmetal_hull", make_chamfered_oct_prism(0.46, 0.46, 0.12, center=(0.0, 0.06, 0.0), chamfer=0.10))
    b_pedestal.add("aero_white", make_chamfered_oct_prism(0.24, 0.24, 0.98, center=(0.0, 0.58, 0.0), chamfer=0.05, top_scale=0.88))
    b_pedestal.add(
        "gunmetal_hull",
        transform_geom(make_chamfered_oct_prism(0.36, 0.32, 0.10, chamfer=0.07), translate=(0.0, 1.12, 0.04), rot_xyz_deg=(28.0, 0.0, 0.0)),
    )
    b_pedestal.add(
        "led_amber",
        transform_geom(make_closed_torus_ring(0.12, 0.014, n_major=16, n_minor=6), translate=(0.0, 1.15, 0.06), rot_xyz_deg=(28.0, 0.0, 0.0)),
    )
    b_pedestal.add(
        "led_cyan",
        transform_geom(make_closed_torus_ring(0.075, 0.010, n_major=14, n_minor=5), translate=(0.0, 1.16, 0.07), rot_xyz_deg=(28.0, 0.0, 0.0)),
    )
    b_pedestal.add(
        "preface_glass",
        transform_geom(make_cylinder(0.115, 0.115, 0.02, segments=16), translate=(0.0, 1.16, 0.07), rot_xyz_deg=(28.0, 0.0, 0.0)),
    )

    # 4. `Node_Calib_01`, `Node_Calib_02`, `Node_Calib_03` (3-node calibration progress rings on upper door header)
    calib_nodes = []
    for c_i, cx_pos in enumerate([-0.55, 0.0, 0.55], 1):
        bc = RichPartBucket(mats)
        bc.add("gunmetal_hull", make_cylinder(0.11, 0.11, 0.06, center=(0.0, 0.0, 0.0), segments=12, axis="z"))
        bc.add("led_cyan" if c_i == 1 else "led_amber", make_closed_torus_ring(0.085, 0.016, center=(0.0, 0.0, 0.035), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=12, n_minor=5))
        calib_nodes.append((f"Node_Calib_{c_i:02d}", "PrefaceRoom_Root", (cx_pos, 3.68, -3.78), bc))

    # 5. `Relay_Panel_B` (`X = -1.85m, Y = 1.10m, Z = -3.82m`, Recessed Wall Maintenance Junction with open `alphaMode: "BLEND"` cover)
    b_relay = RichPartBucket(mats)
    b_relay.add("gunmetal_hull", make_beveled_box((0.68, 0.86, 0.16), center=(0.0, 0.0, 0.0), bevel=0.02))
    b_relay.add("accent_orange", make_beveled_box((0.56, 0.74, 0.08), center=(0.0, 0.0, 0.05), bevel=0.015))
    b_relay.add("steel_machined", make_cylinder(0.085, 0.085, 0.12, center=(0.0, -0.08, 0.08), segments=12, axis="z"))
    b_relay.add("led_amber", make_closed_torus_ring(0.092, 0.012, center=(0.0, -0.08, 0.13), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=12, n_minor=5))
    # Open hinged `alphaMode: "BLEND"` inspection cover swung 65 degrees open to the left
    b_relay.add(
        "preface_glass",
        transform_geom(make_beveled_box((0.58, 0.76, 0.03), bevel=0.01), translate=(-0.42, 0.0, 0.24), rot_xyz_deg=(0.0, -65.0, 0.0)),
    )

    # 6. `East_Promenade_Viewport` & `Commuter_Waiting_Bench` (`X = +4.25m, Z = 0.0m`)
    b_viewport = RichPartBucket(mats)
    b_viewport.add("preface_glass", make_beveled_box((0.06, 2.38, 5.56), center=(0.0, 0.0, 0.0), bevel=0.01))

    b_bench = RichPartBucket(mats)
    b_bench.add("aero_white", make_chamfered_oct_prism(0.68, 3.20, 0.42, center=(0.0, 0.21, 0.0), chamfer=0.14))
    b_bench.add("gunmetal_hull", make_chamfered_oct_prism(0.62, 3.10, 0.08, center=(0.0, 0.45, 0.0), chamfer=0.12))
    b_bench.add("led_amber", make_beveled_box((0.54, 0.04, 2.95), center=(0.0, 0.12, 0.0), bevel=0.005))
    # Two stowed commuter carry-on cases (`#88929E` brushed steel shells with `#D95B26` latches)
    for cz_bag in [-1.95, 1.95]:
        b_bench.add("steel_machined", make_chamfered_oct_prism(0.38, 0.54, 0.44, center=(-0.12, 0.22, cz_bag), chamfer=0.06))
        b_bench.add("accent_orange", make_beveled_box((0.40, 0.08, 0.42), center=(-0.12, 0.32, cz_bag), bevel=0.01))

    # 7. `West_Technician_Tool_Cart` & `Floor_Power_Conduit` (`X = -4.20m, Z = -0.80m`)
    b_cart = RichPartBucket(mats)
    b_cart.add("gunmetal_hull", make_chamfered_oct_prism(0.75, 1.45, 0.88, center=(0.0, 0.44, 0.0), chamfer=0.12))
    b_cart.add("accent_orange", make_beveled_box((0.78, 0.12, 1.48), center=(0.0, 0.84, 0.0), bevel=0.02))
    b_cart.add("steel_machined", make_cylinder(0.12, 0.12, 0.36, center=(0.0, 1.06, -0.32), segments=10))
    b_cart.add("led_cyan", make_beveled_box((0.32, 0.22, 0.06), center=(0.15, 1.02, 0.28), bevel=0.01))

    # Illuminated floor power conduit (`alphaMode: "BLEND"` floor grating) + Door Threshold Strip
    b_conduit = RichPartBucket(mats)
    b_conduit.add("room_walls_floor", make_beveled_box((2.10, 0.03, 0.36), center=(-0.92, 0.085, -3.55), bevel=0.005), UV_Q1_AMBER_CONDUIT)
    b_conduit.add("room_walls_floor", make_beveled_box((2.40, 0.03, 0.28), center=(0.0, 0.085, -3.75), bevel=0.005), UV_Q1_CYAN_CONDUIT)
    b_conduit.add("preface_glass", make_beveled_box((2.05, 0.04, 0.32), center=(-0.92, 0.09, -3.55), bevel=0.005))
    b_conduit.add("led_amber", make_beveled_box((2.36, 0.035, 0.12), center=(0.0, 0.09, -3.88), bevel=0.004))

    node_specs = [
        ("PrefaceRoom_Root", None, (0.0, 0.0, 0.0), None),
        ("Vestibule_Shell", "PrefaceRoom_Root", (0.0, 0.0, 0.0), b_shell),
        ("Counterweight_Transom_Window", "PrefaceRoom_Root", (0.0, 3.02, -3.90), b_transom),
        ("Pedestal_RFID_Main", "PrefaceRoom_Root", (1.55, 0.08, -3.65), b_pedestal),
        *calib_nodes,
        ("Relay_Panel_B", "PrefaceRoom_Root", (-1.85, 1.15, -3.82), b_relay),
        ("East_Promenade_Viewport", "PrefaceRoom_Root", (4.88, 2.20, 0.0), b_viewport),
        ("Commuter_Waiting_Bench", "PrefaceRoom_Root", (4.25, 0.08, 0.0), b_bench),
        ("West_Technician_Tool_Cart", "PrefaceRoom_Root", (-4.20, 0.08, -0.80), b_cart),
        ("Floor_Power_Conduit", "PrefaceRoom_Root", (0.0, 0.0, 0.0), b_conduit),
    ]

    primary_out = os.path.join(ENV_DIRS[0], "preface_service_call_room.glb")
    info = export_hierarchy_with_animations_glb(
        primary_out,
        root_scene_name="PrefaceServiceCallRoom",
        node_specs=node_specs,
        mats=mats,
        animations_spec=[],
        auto_ground_root_y=True,
    )
    for d_m in ENV_DIRS[1:]:
        shutil.copyfile(primary_out, os.path.join(d_m, "preface_service_call_room.glb"))
    return info


# ------------------------------------------------------------------------------
# 2.2 `prop_service_door.glb` — Dual-Leaf Malfunctioning Commuter Bulkhead Door
# (Exact required nodes: `Door_Frame_Root`, `Door_Leaf_Left`, `Door_Leaf_Right`,
#  `Counterweight_Carriage`, `Header_Node_01`, `Header_Node_02`, `Header_Node_03`)
# ------------------------------------------------------------------------------
def build_prop_service_door(mats: Dict[str, RichPBRMaterial]) -> Dict[str, any]:
    UV_Q2_DOOR_LEAF = (0.52, 0.98, 0.02, 0.24)
    UV_Q2_STAGE1_FAULT = (0.52, 0.98, 0.25, 0.31)
    UV_Q2_STAGE2_AMBER = (0.52, 0.98, 0.33, 0.39)
    UV_Q2_STAGE3_CYAN = (0.52, 0.98, 0.42, 0.48)

    # 1. `Door_Frame_Root`: Outer chamfered `#1A1E24` frame (`2.40m W x 2.60m H x 0.38m D`) + upper counterweight transom
    b_frame = RichPartBucket(mats)
    b_frame.add("gunmetal_hull", make_beveled_box((2.40, 0.08, 0.38), center=(0.0, 0.04, 0.0), bevel=0.0))
    for sx in [-1.14, 1.14]:
        b_frame.add("gunmetal_hull", make_beveled_box((0.12, 2.52, 0.38), center=(sx, 1.30, 0.0), bevel=0.02))
        b_frame.add("led_amber", make_beveled_box((0.03, 2.20, 0.40), center=(sx * 0.94, 1.25, 0.0), bevel=0.004))
    b_frame.add("gunmetal_hull", make_beveled_box((2.40, 0.14, 0.38), center=(0.0, 2.53, 0.0), bevel=0.02))
    # Upper counterweight transom housing (`Y = 2.08m..2.52m`) with `alphaMode: "BLEND"` glass cover
    b_frame.add("steel_machined", make_cylinder(0.032, 0.032, 2.16, center=(0.0, 2.32, 0.0), segments=10, axis="x"))
    b_frame.add("preface_glass", make_beveled_box((2.16, 0.36, 0.04), center=(0.0, 2.32, 0.17), bevel=0.008))

    # 2. `Door_Leaf_Left` (`Leaf_A`, `1.04m W x 2.04m H`, closed at X = -0.52m)
    b_leaf_l = RichPartBucket(mats)
    b_leaf_l.add("service_door_atlas", make_chamfered_oct_prism(1.04, 0.16, 2.00, center=(0.0, 1.08, 0.0), chamfer=0.03), UV_Q2_DOOR_LEAF)
    b_leaf_l.add("aero_white", make_beveled_box((0.88, 1.15, 0.18), center=(-0.02, 1.35, 0.0), bevel=0.015))
    b_leaf_l.add("accent_orange", make_beveled_box((0.12, 1.85, 0.19), center=(0.46, 1.08, 0.0), bevel=0.012))
    b_leaf_l.add("preface_glass", make_beveled_box((0.56, 0.36, 0.20), center=(-0.04, 1.48, 0.0), bevel=0.008))

    # 3. `Door_Leaf_Right` (`Leaf_B`, `1.04m W x 2.04m H`, wedged `0.18m` ajar at X = +0.52m + 0.09m in initial state)
    b_leaf_r = RichPartBucket(mats)
    b_leaf_r.add("service_door_atlas", make_chamfered_oct_prism(1.04, 0.16, 2.00, center=(0.0, 1.08, 0.0), chamfer=0.03), UV_Q2_DOOR_LEAF)
    b_leaf_r.add("aero_white", make_beveled_box((0.88, 1.15, 0.18), center=(0.02, 1.35, 0.0), bevel=0.015))
    b_leaf_r.add("accent_orange", make_beveled_box((0.12, 1.85, 0.19), center=(-0.46, 1.08, 0.0), bevel=0.012))
    b_leaf_r.add("steel_machined", make_beveled_box((0.98, 0.08, 0.20), center=(0.0, 2.06, 0.0), bevel=0.01))
    b_leaf_r.add("preface_glass", make_beveled_box((0.56, 0.36, 0.20), center=(0.04, 1.48, 0.0), bevel=0.008))

    # 4. `Counterweight_Carriage` (slides along upper transom rail at Y = 2.32m)
    b_carriage = RichPartBucket(mats)
    b_carriage.add("steel_machined", make_chamfered_oct_prism(0.36, 0.22, 0.24, center=(0.0, 0.0, 0.0), chamfer=0.04))
    b_carriage.add("accent_orange", make_beveled_box((0.16, 0.26, 0.24), center=(0.0, 0.0, 0.0), bevel=0.015))
    b_carriage.add("led_fault_red", make_beveled_box((0.28, 0.06, 0.25), center=(0.0, 0.0, 0.0), bevel=0.005))

    # 5. `Header_Node_01`, `Header_Node_02`, `Header_Node_03` (3 calibration ring nodes on upper door frame)
    h_buckets = []
    for h_i, uv_stage in enumerate([UV_Q2_STAGE1_FAULT, UV_Q2_STAGE2_AMBER, UV_Q2_STAGE3_CYAN], 1):
        bh = RichPartBucket(mats)
        bh.add("gunmetal_hull", make_cylinder(0.085, 0.085, 0.06, center=(0.0, 0.0, 0.0), segments=12, axis="z"))
        bh.add("service_door_atlas", make_closed_torus_ring(0.068, 0.014, center=(0.0, 0.0, 0.03), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=12, n_minor=5), uv_stage)
        h_buckets.append((f"Header_Node_{h_i:02d}", "Door_Frame_Root", (-0.48 + (h_i - 1) * 0.48, 2.52, 0.18), bh))

    node_specs = [
        ("Door_Frame_Root", None, (0.0, 0.0, 0.0), b_frame),
        ("Door_Leaf_Left", "Door_Frame_Root", (-0.52, 0.0, 0.0), b_leaf_l),
        ("Door_Leaf_Right", "Door_Frame_Root", (0.58, 0.0, 0.0), b_leaf_r),
        ("Counterweight_Carriage", "Door_Frame_Root", (0.32, 2.32, 0.0), b_carriage),
        *h_buckets,
    ]

    # Build the 3-Cycle Troubleshooting Animations (`Cycle1_JamAt40`, `Cycle2_CounterweightSync`, `Cycle3_FullOpen`)
    t_c1 = np.linspace(0.0, 1.60, 25, dtype=np.float32)
    tr_c1 = {
        "Door_Leaf_Left": {"translation": []},
        "Door_Leaf_Right": {"translation": []},
        "Counterweight_Carriage": {"translation": []},
    }
    for k in range(len(t_c1)):
        s = k / float(len(t_c1) - 1)
        # Leaf_A opens smoothly then retracts; Leaf_B shudders at 40% travel against jammed counterweight then retracts
        open_env = math.sin(s * math.pi)
        shudder = 0.03 * math.sin(s * 12.0 * math.pi) if (0.35 <= s <= 0.70) else 0.0
        tr_c1["Door_Leaf_Left"]["translation"].append([-0.52 - 0.85 * open_env, 0.0, 0.0])
        tr_c1["Door_Leaf_Right"]["translation"].append([0.58 + min(0.36, 0.65 * open_env) + shudder, 0.0, 0.0])
        tr_c1["Counterweight_Carriage"]["translation"].append([0.32 - min(0.22, 0.45 * open_env) - shudder, 2.32, 0.0])

    t_c2 = np.linspace(0.0, 1.80, 25, dtype=np.float32)
    tr_c2 = {
        "Door_Leaf_Left": {"translation": []},
        "Door_Leaf_Right": {"translation": []},
        "Counterweight_Carriage": {"translation": []},
    }
    for k in range(len(t_c2)):
        s = k / float(len(t_c2) - 1)
        open_env = math.sin(s * math.pi)
        tr_c2["Door_Leaf_Left"]["translation"].append([-0.52 - 0.92 * open_env, 0.0, 0.0])
        tr_c2["Door_Leaf_Right"]["translation"].append([0.52 + 0.92 * open_env, 0.0, 0.0])
        tr_c2["Counterweight_Carriage"]["translation"].append([-0.55 * math.cos(s * math.pi), 2.32, 0.0])

    t_c3 = np.linspace(0.0, 1.40, 21, dtype=np.float32)
    tr_c3 = {
        "Door_Leaf_Left": {"translation": []},
        "Door_Leaf_Right": {"translation": []},
        "Counterweight_Carriage": {"translation": []},
    }
    for k in range(len(t_c3)):
        s = k / float(len(t_c3) - 1)
        ease = 0.5 * (1.0 - math.cos(s * math.pi))
        tr_c3["Door_Leaf_Left"]["translation"].append([-0.52 - 0.95 * ease, 0.0, 0.0])
        tr_c3["Door_Leaf_Right"]["translation"].append([0.52 + 0.95 * ease, 0.0, 0.0])
        tr_c3["Counterweight_Carriage"]["translation"].append([-0.65 * ease, 2.32, 0.0])

    animations_spec = [
        ("Cycle1_JamAt40", t_c1, {k: {p: np.array(v, dtype=np.float32) for p, v in d.items()} for k, d in tr_c1.items()}),
        ("Cycle2_CounterweightSync", t_c2, {k: {p: np.array(v, dtype=np.float32) for p, v in d.items()} for k, d in tr_c2.items()}),
        ("Cycle3_FullOpen", t_c3, {k: {p: np.array(v, dtype=np.float32) for p, v in d.items()} for k, d in tr_c3.items()}),
    ]

    primary_out = os.path.join(DOOR_DIRS[0], "prop_service_door.glb")
    info = export_hierarchy_with_animations_glb(
        primary_out,
        root_scene_name="PropServiceDoor_DualLeaf",
        node_specs=node_specs,
        mats=mats,
        animations_spec=animations_spec,
        auto_ground_root_y=True,
    )
    for d_m in DOOR_DIRS[1:]:
        shutil.copyfile(primary_out, os.path.join(d_m, "prop_service_door.glb"))
    return info


# ------------------------------------------------------------------------------
# 2.3 `char_assistant_droid.glb` — Aegis-7 Maintenance Assistant Droid (`Unit A7-D2`, 1.15m H x 0.68m W x 0.72m D)
# ------------------------------------------------------------------------------
def build_char_assistant_droid(mats: Dict[str, RichPBRMaterial]) -> Dict[str, any]:
    UV_Q4_AMBER_CHASSIS = (0.52, 0.74, 0.52, 0.74)
    UV_Q4_WHITE_CHASSIS = (0.76, 0.98, 0.52, 0.74)
    UV_Q4_DARK_EYES = (0.52, 0.98, 0.76, 0.90)
    UV_Q4_ORANGE_SHUNT = (0.52, 0.98, 0.91, 0.98)

    # 1. `Droid_Base` (Twin-gyro omni-wheel / articulated 3-leg stability chassis, Y = 0.0m..0.34m)
    b_base = RichPartBucket(mats)
    # 3 articulated stability legs + omni-wheels touching Y = 0.00000
    for leg_ang in [0.0, 120.0, 240.0]:
        rad = math.radians(leg_ang)
        lx, lz = 0.24 * math.sin(rad), 0.24 * math.cos(rad)
        b_base.add("gunmetal_hull", make_beveled_box((0.12, 0.14, 0.22), center=(lx * 0.75, 0.22, lz * 0.75), bevel=0.02))
        b_base.add("steel_machined", make_cylinder(0.085, 0.085, 0.065, center=(lx, 0.085, lz), segments=14, axis="x"))
        b_base.add("led_amber", make_closed_torus_ring(0.065, 0.008, center=(lx, 0.085, lz), rot_xyz_deg=(0.0, 0.0, 90.0), n_major=12, n_minor=5))
    b_base.add("gunmetal_hull", make_chamfered_oct_prism(0.46, 0.46, 0.14, center=(0.0, 0.28, 0.0), chamfer=0.10))

    # 2. `Droid_Chassis` (65/35 Asymmetric Body in Aerospace-White & Caterpillar Industrial Amber, Y = 0.34m..0.82m)
    b_chassis = RichPartBucket(mats)
    b_chassis.add("droid_chassis_atlas", make_chamfered_oct_prism(0.38, 0.48, 0.44, center=(0.06, 0.22, 0.0), chamfer=0.08), UV_Q4_WHITE_CHASSIS)
    b_chassis.add("droid_chassis_atlas", make_chamfered_oct_prism(0.26, 0.46, 0.42, center=(-0.14, 0.21, 0.0), chamfer=0.06), UV_Q4_AMBER_CHASSIS)
    b_chassis.add("droid_chassis_atlas", make_beveled_box((0.36, 0.16, 0.49), center=(0.0, 0.24, 0.0), bevel=0.02), UV_Q4_DARK_EYES)

    # 3. `RFID_Handshake_Ring` (Prominent #D95B26 Signal-Orange Collar ringed with #00E5FF Cyan Emitters at Y = 0.78m)
    b_ring = RichPartBucket(mats)
    b_ring.add("accent_orange", make_closed_torus_ring(0.24, 0.032, center=(0.0, 0.0, 0.0), rot_xyz_deg=(12.0, 0.0, 0.0), n_major=18, n_minor=6))
    b_ring.add("led_cyan", make_closed_torus_ring(0.255, 0.012, center=(0.0, 0.01, 0.0), rot_xyz_deg=(12.0, 0.0, 0.0), n_major=18, n_minor=5))
    b_ring.add("droid_chassis_atlas", make_chamfered_oct_prism(0.38, 0.38, 0.06, center=(0.0, -0.02, 0.0), chamfer=0.08), UV_Q4_ORANGE_SHUNT)

    # 4. `Droid_Head_Gimbal` (Articulated Upper Gimbal Head reaching Y = 1.15m with `alphaMode: "BLEND"` Domed Optic Visor)
    b_head = RichPartBucket(mats)
    b_head.add("aero_white", make_chamfered_oct_prism(0.34, 0.34, 0.22, center=(0.0, 0.11, -0.02), chamfer=0.08, top_scale=0.84))
    # Expressive #00E5FF cyan / #FF9500 amber circular binocular status eyes inside the visor
    for ex, m_eye in [(-0.065, "led_cyan"), (0.065, "led_cyan")]:
        b_head.add(m_eye, make_closed_torus_ring(0.042, 0.009, center=(ex, 0.11, 0.145), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=12, n_minor=5))
    b_head.add("led_amber", make_beveled_box((0.14, 0.018, 0.02), center=(0.0, 0.055, 0.148), bevel=0.003))
    # Side-mounted work spotlight (`+X`) & telemetry antenna (`-X`) reaching exact total height 1.15m
    b_head.add("steel_machined", make_cylinder(0.038, 0.032, 0.09, center=(0.19, 0.12, 0.04), segments=10, axis="z"))
    b_head.add("led_cyan", make_cylinder(0.030, 0.030, 0.02, center=(0.19, 0.12, 0.085), segments=10, axis="z"))
    b_head.add("steel_machined", make_cylinder(0.010, 0.005, 0.14, center=(-0.12, 0.26, -0.04), segments=8))
    # Domed `alphaMode: "BLEND"` optic visor over front of head
    b_head.add("preface_glass", make_chamfered_oct_prism(0.32, 0.14, 0.20, center=(0.0, 0.11, 0.10), chamfer=0.07))

    # 5. 3-Joint Brushed-Steel Diagnostic Probe Arm on Right Flank (`Probe_Arm_Base` -> `Probe_Arm_Mid` -> `Probe_Tip`)
    b_arm1 = RichPartBucket(mats)
    b_arm1.add("steel_machined", make_joint_ball(0.048, center=(0.0, 0.0, 0.0), segments=10))
    b_arm1.add("steel_machined", make_cylinder(0.028, 0.024, 0.22, center=(0.0, 0.0, 0.11), segments=10, axis="z"))

    b_arm2 = RichPartBucket(mats)
    b_arm2.add("accent_orange", make_joint_ball(0.038, center=(0.0, 0.0, 0.0), segments=10))
    b_arm2.add("steel_machined", make_cylinder(0.022, 0.018, 0.20, center=(0.0, 0.0, 0.10), segments=10, axis="z"))

    b_tip = RichPartBucket(mats)
    b_tip.add("accent_orange", make_cylinder(0.032, 0.022, 0.08, center=(0.0, 0.0, 0.04), segments=10, axis="z"))
    b_tip.add("led_cyan", make_cylinder(0.014, 0.008, 0.06, center=(0.0, 0.0, 0.09), segments=10, axis="z"))

    node_specs = [
        ("AssistantDroid_Root", None, (0.0, 0.0, 0.0), None),
        ("Droid_Base", "AssistantDroid_Root", (0.0, 0.0, 0.0), b_base),
        ("Droid_Chassis", "Droid_Base", (0.0, 0.34, 0.0), b_chassis),
        ("RFID_Handshake_Ring", "Droid_Chassis", (0.0, 0.44, 0.0), b_ring),
        ("Droid_Head_Gimbal", "Droid_Chassis", (0.0, 0.48, 0.0), b_head),
        ("Probe_Arm_Base", "Droid_Chassis", (-0.28, 0.26, 0.04), b_arm1),
        ("Probe_Arm_Mid", "Probe_Arm_Base", (0.0, 0.0, 0.22), b_arm2),
        ("Probe_Tip", "Probe_Arm_Mid", (0.0, 0.0, 0.20), b_tip),
    ]

    # Animations: `Idle`, `DiagnosticProbe`, `WalkCycle`
    t_anim = np.linspace(0.0, 1.40, 25, dtype=np.float32)
    tr_idle = {
        "Droid_Chassis": {"translation": []},
        "Droid_Head_Gimbal": {"rotation": []},
        "RFID_Handshake_Ring": {"rotation": []},
    }
    tr_probe = {
        "Droid_Head_Gimbal": {"rotation": []},
        "Probe_Arm_Base": {"rotation": []},
        "Probe_Arm_Mid": {"rotation": []},
        "RFID_Handshake_Ring": {"rotation": []},
    }
    for k in range(len(t_anim)):
        phi = 0.0 if k == len(t_anim) - 1 else (2.0 * math.pi * k / float(len(t_anim) - 1))
        lift = 0.5 * (1.0 - math.cos(phi))
        tr_idle["Droid_Chassis"]["translation"].append([0.0, 0.34 + 0.015 * math.sin(phi), 0.0])
        tr_idle["Droid_Head_Gimbal"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(4.0 * math.sin(phi), 14.0 * math.cos(phi), 0.0))
        tr_idle["RFID_Handshake_Ring"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 18.0 * math.sin(phi), 0.0))

        tr_probe["Droid_Head_Gimbal"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-8.0 * lift, -18.0 * lift, 0.0))
        tr_probe["Probe_Arm_Base"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-22.0 * lift, 12.0 * lift, 0.0))
        tr_probe["Probe_Arm_Mid"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(28.0 * lift, 0.0, 0.0))
        tr_probe["RFID_Handshake_Ring"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(18.0 * lift, 0.0, 0.0))

    animations_spec = [
        ("Idle", t_anim, {k: {p: np.array(v, dtype=np.float32) for p, v in d.items()} for k, d in tr_idle.items()}),
        ("DiagnosticProbe", t_anim, {k: {p: np.array(v, dtype=np.float32) for p, v in d.items()} for k, d in tr_probe.items()}),
        ("WalkCycle", t_anim, {k: {p: np.array(v, dtype=np.float32) for p, v in d.items()} for k, d in tr_idle.items()}),
    ]

    primary_out = os.path.join(CHAR_DIRS[0], "char_assistant_droid.glb")
    info = export_hierarchy_with_animations_glb(
        primary_out,
        root_scene_name="CharAssistantDroid_UnitA7D2",
        node_specs=node_specs,
        mats=mats,
        animations_spec=animations_spec,
        auto_ground_root_y=True,
    )
    for d_m in CHAR_DIRS[1:]:
        shutil.copyfile(primary_out, os.path.join(d_m, "char_assistant_droid.glb"))
    return info


# ------------------------------------------------------------------------------
# 2.4 `char_citizen_commuter.glb` — Waiting Hab-7 Civilian Commuter (`1.78m H`)
# (Includes articulated `Arm_L_Commuter` / `LeftUpperArm` & `LeftForeArm` with
#  embedded subdermal RFID wrist pass band + `WristRaiseDemo` and `WalkCycle` animations!)
# ------------------------------------------------------------------------------
def build_char_citizen_commuter(mats: Dict[str, RichPBRMaterial]) -> Dict[str, any]:
    UV_Q3_TERRACOTTA = (0.02, 0.13, 0.52, 0.85)
    UV_Q3_CERULEAN = (0.14, 0.25, 0.52, 0.85)
    UV_Q3_SAFFRON = (0.26, 0.37, 0.52, 0.85)
    UV_Q3_SLATE_PANTS = (0.38, 0.49, 0.52, 0.85)
    UV_Q3_SKIN = (0.02, 0.48, 0.90, 0.98)
    UV_W_Q1_SKIN_RFID = (0.02, 0.48, 0.02, 0.48)

    # Reuse the portrait-grade sculpted head from Candidate #01/#04 converted into RichPartBucket
    char_mats = get_character_materials()
    head_pb = build_head_node(cand_id=1, mats=char_mats)
    b_head = RichPartBucket(mats)
    for m_k, g_list in head_pb.buckets.items():
        if not g_list:
            continue
        merged = merge_geometries(g_list)
        if m_k == "portrait_atlas":
            b_head.add("portrait_atlas", merged)
        elif "skin" in m_k:
            b_head.add("commuter_wardrobe", merged, UV_Q3_SKIN)
        elif "visor" in m_k:
            # Civilian commuter is open-faced without a flight helmet visor
            continue
        elif "led" in m_k or "iris" in m_k:
            b_head.add("led_cyan", merged)
        else:
            b_head.add("gunmetal_hull", merged)

    # Hips & Smart-Slate Civilian Trousers
    b_hips = RichPartBucket(mats)
    b_hips.add("commuter_wardrobe", make_chamfered_oct_prism(0.34, 0.23, 0.16, center=(0.0, 0.02, 0.0), chamfer=0.05), UV_Q3_SLATE_PANTS)

    # Spine & Tailored Cerulean/White High-Collar Civilian Commuter Jacket + Cross-Body Courier Bag
    b_spine = RichPartBucket(mats)
    b_spine.add("commuter_wardrobe", make_chamfered_oct_prism(0.31, 0.21, 0.22, center=(0.0, 0.08, 0.0), chamfer=0.05), UV_Q3_SAFFRON)

    b_chest = RichPartBucket(mats)
    b_chest.add("commuter_wardrobe", make_chamfered_oct_prism(0.38, 0.24, 0.24, center=(0.0, 0.10, 0.0), chamfer=0.06, top_scale=1.06), UV_Q3_CERULEAN)
    b_chest.add("aero_white", make_closed_torus_ring(0.11, 0.022, center=(0.0, 0.22, 0.0), n_major=12, n_minor=5))
    # Cross-Body Commuter Courier Bag (`#C25C3A` Terracotta smart-fabric satchel at right hip + `#D95B26` strap buckle)
    b_chest.add(
        "commuter_wardrobe",
        transform_geom(make_beveled_box((0.045, 0.34, 0.25), bevel=0.008), translate=(0.0, 0.06, 0.0), rot_xyz_deg=(0.0, 0.0, -34.0)),
        UV_Q3_TERRACOTTA,
    )
    b_chest.add("accent_orange", make_beveled_box((0.055, 0.065, 0.04), center=(0.05, 0.12, 0.13), bevel=0.006))
    b_chest.add("commuter_wardrobe", make_chamfered_oct_prism(0.12, 0.28, 0.24, center=(-0.20, -0.14, 0.02), chamfer=0.03), UV_Q3_TERRACOTTA)

    # Left Upper Arm (`Arm_L_Commuter`) & Left Forearm (`Forearm_L_Commuter`) with Glowing Civilian Wrist RFID Pass Band!
    b_uarm_l = RichPartBucket(mats)
    b_uarm_l.add("commuter_wardrobe", make_joint_ball(0.064, center=(0.0, 0.0, 0.0), segments=8), UV_Q3_CERULEAN)
    b_uarm_l.add("commuter_wardrobe", make_cylinder(0.052, 0.058, 0.25, center=(0.0, -0.13, 0.0), segments=10), UV_Q3_CERULEAN)

    b_farm_l = RichPartBucket(mats)
    b_farm_l.add("commuter_wardrobe", make_joint_ball(0.048, center=(0.0, 0.0, 0.0), segments=8), UV_Q3_CERULEAN)
    b_farm_l.add("commuter_wardrobe", make_cylinder(0.040, 0.046, 0.20, center=(0.0, -0.11, 0.0), segments=10), UV_Q3_SKIN)
    # Glowing Civilian #00E5FF Wrist RFID Pass Band & Subdermal Dorsal Hand Node at Y = -0.21m.. -0.28m
    b_farm_l.add("aero_white", make_closed_torus_ring(0.044, 0.009, center=(0.0, -0.20, 0.0), n_major=12, n_minor=5))
    b_farm_l.add("led_cyan", make_closed_torus_ring(0.046, 0.005, center=(0.0, -0.20, 0.0), n_major=12, n_minor=5))
    b_farm_l.add("commuter_wrist_rfid", make_beveled_box((0.042, 0.085, 0.072), center=(0.0, -0.26, 0.006), bevel=0.010), UV_W_Q1_SKIN_RFID)
    b_farm_l.add("led_cyan", make_cylinder(0.012, 0.012, 0.012, center=(0.022, -0.255, 0.012), segments=8, axis="x"))

    # Right Arm
    b_uarm_r = RichPartBucket(mats)
    b_uarm_r.add("commuter_wardrobe", make_joint_ball(0.064, center=(0.0, 0.0, 0.0), segments=8), UV_Q3_CERULEAN)
    b_uarm_r.add("commuter_wardrobe", make_cylinder(0.052, 0.058, 0.25, center=(0.0, -0.13, 0.0), segments=10), UV_Q3_CERULEAN)

    b_farm_r = RichPartBucket(mats)
    b_farm_r.add("commuter_wardrobe", make_joint_ball(0.048, center=(0.0, 0.0, 0.0), segments=8), UV_Q3_CERULEAN)
    b_farm_r.add("commuter_wardrobe", make_cylinder(0.040, 0.046, 0.20, center=(0.0, -0.11, 0.0), segments=10), UV_Q3_SKIN)
    b_farm_r.add("commuter_wardrobe", make_beveled_box((0.040, 0.082, 0.068), center=(0.0, -0.26, 0.006), bevel=0.010), UV_Q3_SKIN)

    # Legs & Civilian Transit Shoes (extending down to exact Y = 0.00000)
    def _make_leg_pair(is_l: bool):
        bu = RichPartBucket(mats)
        bu.add("commuter_wardrobe", make_joint_ball(0.076, center=(0.0, 0.0, 0.0), segments=8), UV_Q3_SLATE_PANTS)
        bu.add("commuter_wardrobe", make_cylinder(0.062, 0.076, 0.42, center=(0.0, -0.22, 0.0), segments=10), UV_Q3_SLATE_PANTS)
        bl = RichPartBucket(mats)
        bl.add("commuter_wardrobe", make_joint_ball(0.058, center=(0.0, 0.0, 0.0), segments=8), UV_Q3_SLATE_PANTS)
        bl.add("commuter_wardrobe", make_cylinder(0.048, 0.058, 0.38, center=(0.0, -0.20, 0.0), segments=10), UV_Q3_SLATE_PANTS)
        bf = RichPartBucket(mats)
        bf.add("gunmetal_hull", make_chamfered_oct_prism(0.105, 0.23, 0.06, center=(0.0, -0.04, 0.04), chamfer=0.025))
        bf.add("aero_white", make_beveled_box((0.108, 0.020, 0.24), center=(0.0, -0.070, 0.04), bevel=0.0))
        return bu, bl, bf

    bu_l, bl_l, bf_l = _make_leg_pair(True)
    bu_r, bl_r, bf_r = _make_leg_pair(False)

    node_specs = [
        ("CitizenCommuter_Root", None, (0.0, 0.0, 0.0), None),
        ("Hips", "CitizenCommuter_Root", (0.0, 0.96, 0.0), b_hips),
        ("Spine", "Hips", (0.0, 0.16, 0.0), b_spine),
        ("Chest", "Spine", (0.0, 0.22, 0.0), b_chest),
        ("Head", "Chest", (0.0, 0.24, 0.0), b_head),
        ("Arm_L_Commuter", "Chest", (0.20, 0.16, 0.0), b_uarm_l),
        ("Forearm_L_Commuter", "Arm_L_Commuter", (0.0, -0.26, 0.0), b_farm_l),
        ("RightUpperArm", "Chest", (-0.20, 0.16, 0.0), b_uarm_r),
        ("RightForeArm", "RightUpperArm", (0.0, -0.26, 0.0), b_farm_r),
        ("LeftUpLeg", "Hips", (0.10, -0.04, 0.0), bu_l),
        ("LeftLeg", "LeftUpLeg", (0.0, -0.44, 0.0), bl_l),
        ("LeftFoot", "LeftLeg", (0.0, -0.40, 0.0), bf_l),
        ("RightUpLeg", "Hips", (-0.10, -0.04, 0.0), bu_r),
        ("RightLeg", "RightUpLeg", (0.0, -0.44, 0.0), bl_r),
        ("RightFoot", "RightLeg", (0.0, -0.40, 0.0), bf_r),
    ]

    # Animations: `WristRaiseDemo` (raises `Arm_L_Commuter` & `Forearm_L_Commuter` up to chest/eye RFID reader height!) and `WalkCycle`
    t_demo = np.linspace(0.0, 2.40, 33, dtype=np.float32)
    tr_demo = {
        "Arm_L_Commuter": {"rotation": []},
        "Forearm_L_Commuter": {"rotation": []},
        "Head": {"rotation": []},
        "Chest": {"rotation": []},
    }
    for k in range(len(t_demo)):
        s = k / float(len(t_demo) - 1)
        # Smoothly raise left wrist up to chest/eye level (s in 0.15..0.65), hold at RFID pedestal, then lower & glance back
        raise_env = math.sin(s * math.pi) ** 1.2
        glance_back = math.sin(max(0.0, (s - 0.55) / 0.45) * math.pi) if s > 0.55 else 0.0
        tr_demo["Arm_L_Commuter"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-68.0 * raise_env, -18.0 * raise_env, 12.0 * raise_env))
        tr_demo["Forearm_L_Commuter"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-52.0 * raise_env, 0.0, -24.0 * raise_env))
        tr_demo["Head"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(6.0 * raise_env, 32.0 * glance_back, 0.0))
        tr_demo["Chest"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(3.0 * raise_env, 12.0 * glance_back, 0.0))

    # Standard `WalkCycle` (for when the commuters walk out through the open doorway on Scan Cycle 3!)
    from character_aegis7_crew_generator import sample_walk_cycle_tracks
    t_walk, raw_walk = sample_walk_cycle_tracks(duration=1.20, n_frames=33)
    raw_walk["Arm_L_Commuter"] = raw_walk.pop("LeftUpperArm")
    raw_walk["Forearm_L_Commuter"] = raw_walk.pop("LeftForeArm")

    animations_spec = [
        ("WristRaiseDemo", t_demo, {k: {p: np.array(v, dtype=np.float32) for p, v in d.items()} for k, d in tr_demo.items()}),
        ("WalkCycle", t_walk, raw_walk),
    ]

    primary_out = os.path.join(CHAR_DIRS[0], "char_citizen_commuter.glb")
    info = export_hierarchy_with_animations_glb(
        primary_out,
        root_scene_name="CharCitizenCommuter",
        node_specs=node_specs,
        mats=mats,
        animations_spec=animations_spec,
        auto_ground_root_y=True,
    )
    for d_m in CHAR_DIRS[1:]:
        shutil.copyfile(primary_out, os.path.join(d_m, "char_citizen_commuter.glb"))
    return info


def build_all_preface_and_wrist_assets():
    wrist_mats = get_wrist_rfid_materials()
    wrist_results = []
    for cand_id in range(1, 6):
        w_info = build_wrist_rfid_candidate(cand_id, wrist_mats)
        fname = os.path.basename(w_info["filepath"])
        dims = w_info["dimensions"]
        sz_kb = os.path.getsize(w_info["filepath"]) / 1024.0
        print(
            f"[wrist_rfid] {fname:28s} | {dims[0]:.3f}m W x {dims[2]:.3f}m D x {dims[1]:.3f}m H | "
            f"tris={w_info['triangles']:4d} | anims={w_info['animations']} | min_y={w_info['min'][1]:.5f} | {sz_kb:6.1f} KB"
        )
        wrist_results.append(w_info)

    env_mats = get_preface_environment_materials()
    room_info = build_preface_service_call_room(env_mats)
    door_info = build_prop_service_door(env_mats)
    droid_info = build_char_assistant_droid(env_mats)
    commuter_info = build_char_citizen_commuter(env_mats)

    for tag, inf in [
        ("preface_room", room_info),
        ("service_door", door_info),
        ("assist_droid", droid_info),
        ("commuter    ", commuter_info),
    ]:
        fname = os.path.basename(inf["filepath"])
        dims = inf["dimensions"]
        sz_kb = os.path.getsize(inf["filepath"]) / 1024.0
        print(
            f"[{tag}] {fname:32s} | {dims[0]:6.2f}m W x {dims[2]:6.2f}m D x {dims[1]:6.2f}m H | "
            f"tris={inf['triangles']:4d} | anims={inf['animations']} | min_y={inf['min'][1]:.5f} | {sz_kb:6.1f} KB"
        )

    manifest_data = {
        "wrist_rfid_candidates_5": wrist_results,
        "preface_service_call_room": room_info,
        "prop_service_door": door_info,
        "char_assistant_droid": droid_info,
        "char_citizen_commuter": commuter_info,
    }
    man_path = os.path.join(ASSETS_GLB_DIR, "preface_and_wrist_rfid_manifest.json")
    with open(man_path, "w") as f:
        json.dump(manifest_data, f, indent=2)
    print(f"Saved manifest to {man_path}")


if __name__ == "__main__":
    build_all_preface_and_wrist_assets()
