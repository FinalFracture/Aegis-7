#!/usr/bin/env python3
"""
High-Craft Hard Sci-Fi Translucent Surgical Canopy & UV Pharmacy Renderer & 5-Panel Voting Sheet Composer for
Room 04 Hero Asset: Surgical Autodoc Gantry & Triage Console (med_autodoc_r1_01.glb .. med_autodoc_r1_05.glb).

Follows Section 4 of /workspace/game-project/design/medbay_round1/med_autodoc_r1_spec.md:
- Target Look-At Point: (0.0, 1.02, 0.0)
- Camera Angles: 3/4 front-isometric beauty angle (yaw = ±22° to ±24°, pitch = -14°, distance ~ 3.05m, FOV = 46°)
- Practical Lights:
  1. Surgical_Halo_Ice_Spot (#E0F4FF) casting crisp surgical ice-white light onto the robotic arms and patient table
  2. Scanner_Canopy_Cyan_Glow (#00E5FF) illuminating the translucent bio-isolation canopy & cryo-plasma vials
  3. Pharmacy_Tower_UV_Violet (#7B5CFF) illuminating the UV-C sterile pharmacy & supply bay
"""
import os
import io
import sys
import json
import math
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image, ImageDraw, ImageFont
import pygltflib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_bunk_round1 import load_font, make_spacecraft_bay_backdrop

GLB_MEDBAY_DIR = "/workspace/game-project/assets/glb/medbay_round1"
OUT_RENDER_DIR = "/workspace/game-project/assets/renders/medbay_round1"
GODOT_RENDER_DIR = "/workspace/game-project/godot/renders/medbay_round1"

os.makedirs(OUT_RENDER_DIR, exist_ok=True)
os.makedirs(GODOT_RENDER_DIR, exist_ok=True)

CANDIDATE_MEDBAY_META = [
    (
        "med_autodoc_r1_01",
        "01",
        "01_aegis7_octagonal_autodoc_ring_scanner",
        "AEGIS-7 OCTAGONAL AUTODOC & MRI RING SCANNER",
        "45° Chamfered Surgical Bay + Translating Octagonal MRI Ring & Twin Robotic Arms",
        "Translating octagonal MRI/CT scanner ring • Twin articulated robotic surgical arms • Translucent head canopy & UV pharmacy",
        (22.0, -14.0),
        ((0.0, 1.72, 0.25), (0.88, 0.96, 1.0), 1.65),
        ((0.55, 1.35, 0.35), (0.0, 0.92, 1.0), 1.50),
        (0.0, 0.90, 1.0),
    ),
    (
        "med_autodoc_r1_02",
        "02",
        "02_dual_zone_split_autodoc_pharmacy_tower",
        "DUAL-ZONE SPLIT AUTODOC & UV PHARMACY TOWER",
        "68/32 Asymmetric Split Surgical Gantry + Full-Height Translucent UV Pharmacy Tower",
        "Sibling to Locked Winners • Left surgical couch, twin robotic arms & halo lamp • Right 3-tier translucent UV pharmacy tower",
        (-22.0, -14.0),
        ((-0.30, 1.72, 0.25), (0.88, 0.96, 1.0), 1.65),
        ((0.76, 1.35, 0.45), (0.68, 0.56, 1.0), 1.55),
        (0.0, 0.90, 1.0),
    ),
    (
        "med_autodoc_r1_03",
        "03",
        "03_ceiling_cantilever_trauma_bay",
        "TWIN-HALO CEILING CANTILEVER ROBOTIC TRAUMA BAY",
        "Heavy C-Arm Ceiling Surgical Crane + 3 Articulated Manipulators & Clamshell Visor",
        "Open-access C-arm trauma bay • 3 articulated micro-surgery manipulators • Dual overhead surgical halo lamps & clamshell shield",
        (22.0, -14.0),
        ((0.0, 1.74, 0.25), (0.88, 0.96, 1.0), 1.65),
        ((-0.45, 1.25, 0.38), (0.0, 0.92, 1.0), 1.50),
        (0.0, 0.90, 1.0),
    ),
    (
        "med_autodoc_r1_04",
        "04",
        "04_cryo_stasis_toroidal_mri_gantry",
        "CRYO-STASIS ISOLATION POD & TOROIDAL MRI GANTRY",
        "Full-Length Semi-Cylindrical Translucent Cryo Canopy + Sliding Toroidal MRI Ring",
        "Full-length translucent cryo-isolation canopy • Sliding toroidal magnetic-resonance gantry • Twin surgical arms & UV vials",
        (-22.0, -14.0),
        ((0.0, 1.72, 0.25), (0.85, 0.95, 1.0), 1.60),
        ((-0.25, 1.20, 0.42), (0.0, 0.92, 1.0), 1.55),
        (0.0, 0.90, 1.0),
    ),
    (
        "med_autodoc_r1_05",
        "05",
        "05_zerog_gimbaled_surgical_cradle",
        "ZERO-G GIMBALED SURGICAL CRADLE & TRIAGE CONSOLE",
        "Spin-Down Emergency Rotary Trunnion Cradle + Twin Robotic Arms & Bio-Restraints",
        "Rotary gimbal trunnion towers for spin-down surgery • Twin overhead robotic arms • Translucent visor & UV pharmacy bay",
        (22.0, -14.0),
        ((0.0, 1.72, 0.25), (0.88, 0.96, 1.0), 1.65),
        ((0.55, 1.35, 0.38), (0.68, 0.56, 1.0), 1.50),
        (0.0, 0.90, 1.0),
    ),
]


def render_medbay_candidate(
    glb_path: str,
    width: int = 1920,
    height: int = 1080,
    cam_yaw_deg: float = 22.0,
    cam_pitch_deg: float = -14.0,
    light1_cfg=((0.0, 1.72, 0.25), (0.88, 0.96, 1.0), 1.65),
    light2_cfg=((0.55, 1.35, 0.35), (0.0, 0.92, 1.0), 1.50),
    accent_rgb=(0.0, 0.90, 1.0),
) -> Image.Image:
    gltf = pygltflib.GLTF2().load(glb_path)
    blob = gltf.binary_blob()

    tex_images = {}
    for t_idx, tex in enumerate(gltf.textures):
        if tex.source is not None:
            img_obj = gltf.images[tex.source]
            bv = gltf.bufferViews[img_obj.bufferView]
            png_bytes = blob[bv.byteOffset : bv.byteOffset + bv.byteLength]
            pil_img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
            tex_images[t_idx] = np.asarray(pil_img, dtype=np.float32) / 255.0

    def _read_acc(acc_idx: int) -> np.ndarray:
        acc = gltf.accessors[acc_idx]
        bv = gltf.bufferViews[img_obj.bufferView] if False else gltf.bufferViews[acc.bufferView]
        offset = (bv.byteOffset or 0) + (acc.byteOffset or 0)
        comp_map = {
            pygltflib.FLOAT: np.float32,
            pygltflib.UNSIGNED_INT: np.uint32,
            pygltflib.UNSIGNED_SHORT: np.uint16,
        }
        dt = comp_map[acc.componentType]
        cnt_map = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}
        n_comp = cnt_map[acc.type]
        arr = np.frombuffer(blob, dtype=dt, count=acc.count * n_comp, offset=offset)
        return arr.reshape(acc.count, n_comp) if n_comp > 1 else arr

    rw, rh = width, height
    fbuf = make_spacecraft_bay_backdrop(rw, rh, accent_rgb)
    zbuf = np.full((rh, rw), np.inf, dtype=np.float32)
    nbuf = np.zeros((rh, rw, 3), dtype=np.float32)
    ebuf = np.zeros((rh, rw, 3), dtype=np.float32)
    obj_mask = np.zeros((rh, rw), dtype=bool)

    opaque_prims = []
    blend_prims = []
    all_pts = []

    for mesh in gltf.meshes:
        for prim in mesh.primitives:
            pos = _read_acc(prim.attributes.POSITION).astype(np.float32)
            norms = _read_acc(prim.attributes.NORMAL).astype(np.float32)
            uvs = _read_acc(prim.attributes.TEXCOORD_0).astype(np.float32)
            idx = _read_acc(prim.indices).reshape(-1, 3)
            all_pts.append(pos)

            mat = gltf.materials[prim.material] if prim.material is not None else None
            bcf = np.array(mat.pbrMetallicRoughness.baseColorFactor, dtype=np.float32) if (mat and mat.pbrMetallicRoughness.baseColorFactor) else np.ones(4, dtype=np.float32)
            roughness = float(mat.pbrMetallicRoughness.roughnessFactor) if (mat and mat.pbrMetallicRoughness.roughnessFactor is not None) else 0.45
            metallic = float(mat.pbrMetallicRoughness.metallicFactor) if (mat and mat.pbrMetallicRoughness.metallicFactor is not None) else 0.2
            emissive = np.array(mat.emissiveFactor[:3], dtype=np.float32) if (mat and mat.emissiveFactor) else np.zeros(3, dtype=np.float32)
            alpha_mode = (mat.alphaMode or "OPAQUE") if mat else "OPAQUE"
            tex_arr = None
            if mat and mat.pbrMetallicRoughness.baseColorTexture is not None:
                tex_arr = tex_images.get(mat.pbrMetallicRoughness.baseColorTexture.index)

            item = (pos, norms, uvs, idx, bcf, roughness, metallic, emissive, tex_arr)
            if alpha_mode == "BLEND":
                blend_prims.append(item)
            else:
                opaque_prims.append(item)

    pts_stack = np.vstack(all_pts)
    min_pt = pts_stack.min(axis=0)
    max_pt = pts_stack.max(axis=0)
    size = max_pt - min_pt

    target = np.array([0.0, 1.02, 0.0], dtype=np.float32)
    yaw = math.radians(cam_yaw_deg)
    pitch = math.radians(cam_pitch_deg)
    radius = 3.05
    cam_pos = target + np.array([
        math.sin(yaw) * math.cos(pitch) * radius,
        -math.sin(pitch) * radius,
        math.cos(yaw) * math.cos(pitch) * radius,
    ], dtype=np.float32)

    fwd = target - cam_pos
    fwd /= np.linalg.norm(fwd)
    right = np.cross(fwd, np.array([0.0, 1.0, 0.0], dtype=np.float32))
    right /= np.linalg.norm(right)
    up = np.cross(right, fwd)

    fov_y = math.radians(46.0)
    f_scale = 1.0 / math.tan(fov_y * 0.5)
    aspect = rw / float(rh)

    def _project_pts(pts_3d: np.ndarray):
        rel = pts_3d - cam_pos
        cx = rel @ right
        cy = rel @ up
        cz = np.maximum(rel @ fwd, 0.1)
        sx = (cx / cz) * (f_scale / aspect)
        sy = (cy / cz) * f_scale
        px = (sx * 0.5 + 0.5) * rw
        py = (0.5 - sy * 0.5) * rh
        return px, py, cz

    # Floor contact shadow
    foot_corners = np.array([
        [min_pt[0], 0.0, min_pt[2]],
        [max_pt[0], 0.0, min_pt[2]],
        [max_pt[0], 0.0, max_pt[2]],
        [min_pt[0], 0.0, max_pt[2]],
        [0.0, 0.0, 0.0],
    ], dtype=np.float32)
    fpx, fpy, _ = _project_pts(foot_corners)
    fcx, fcy = float(fpx[4]), float(fpy[4])
    rx_foot = max(float(np.max(np.abs(fpx[:4] - fcx))) * 1.08, 160.0)
    ry_foot = max(float(np.max(np.abs(fpy[:4] - fcy))) * 1.15, 45.0)
    yy_g, xx_g = np.mgrid[0:rh, 0:rw].astype(np.float32)
    ell_d2 = ((xx_g - fcx) / rx_foot) ** 2 + ((yy_g - fcy) / ry_foot) ** 2
    fbuf *= (1.0 - 0.62 * np.exp(-ell_d2 * 1.65))[:, :, None]

    key_dir = np.array([0.44, 0.68, 0.58], dtype=np.float32)
    key_dir /= np.linalg.norm(key_dir)
    fill_dir = np.array([-0.64, 0.34, 0.68], dtype=np.float32)
    fill_dir /= np.linalg.norm(fill_dir)
    rim_dir = np.array([0.0, 0.65, -0.76], dtype=np.float32)
    rim_dir /= np.linalg.norm(rim_dir)

    p1_pos, p1_col, p1_e = np.array(light1_cfg[0], dtype=np.float32), np.array(light1_cfg[1], dtype=np.float32), float(light1_cfg[2])
    p2_pos, p2_col, p2_e = np.array(light2_cfg[0], dtype=np.float32), np.array(light2_cfg[1], dtype=np.float32), float(light2_cfg[2])

    # PASS 1: OPAQUE GEOMETRY
    for pos, norms, uvs, idx, bcf, roughness, metallic, emissive, tex_arr in opaque_prims:
        base_cf = bcf[:3]
        px, py, cz = _project_pts(pos)
        valid_v = cz > 0.15

        v_to_cam = cam_pos - pos
        v_to_cam /= np.maximum(np.linalg.norm(v_to_cam, axis=1, keepdims=True), 1e-6)
        ndotl_k = np.maximum(norms @ key_dir, 0.0)
        ndotl_f = np.maximum(norms @ fill_dir, 0.0)
        ndotl_r = np.maximum(norms @ rim_dir, 0.0)

        h_key = key_dir + v_to_cam
        h_key /= np.maximum(np.linalg.norm(h_key, axis=1, keepdims=True), 1e-6)
        shininess = max(8.0, (1.0 - roughness) * 76.0)
        spec_strength = 0.24 + 0.72 * metallic + (0.40 if roughness < 0.22 else 0.0)
        spec_k = (np.maximum(np.sum(norms * h_key, axis=1), 0.0) ** shininess) * spec_strength

        ndotv = np.clip(np.sum(norms * v_to_cam, axis=1), 0.0, 1.0)
        fresnel = ((1.0 - ndotv) ** 3.0) * (0.18 + 0.34 * metallic)

        l1_vec = p1_pos - pos
        l1_dist = np.maximum(np.linalg.norm(l1_vec, axis=1, keepdims=True), 0.18)
        l1_dir = l1_vec / l1_dist
        atten1 = p1_e / (1.0 + 0.55 * (l1_dist[:, 0] ** 2))
        ndotl_p1 = np.maximum(np.sum(norms * l1_dir, axis=1), 0.0) * atten1

        l2_vec = p2_pos - pos
        l2_dist = np.maximum(np.linalg.norm(l2_vec, axis=1, keepdims=True), 0.18)
        l2_dir = l2_vec / l2_dist
        atten2 = p2_e / (1.0 + 0.55 * (l2_dist[:, 0] ** 2))
        ndotl_p2 = np.maximum(np.sum(norms * l2_dir, axis=1), 0.0) * atten2

        ao_vert = np.clip(0.66 + 0.34 * (pos[:, 1] / max(float(size[1]), 1.0)), 0.62, 1.0)

        v_shade = (
            (0.30 + 0.10 * norms[:, 1])[:, None] * np.array([0.84, 0.90, 0.98], dtype=np.float32)
            + (0.66 * ndotl_k)[:, None] * np.array([0.96, 0.98, 1.00], dtype=np.float32)
            + (0.30 * ndotl_f)[:, None] * np.array([0.65, 0.80, 0.98], dtype=np.float32)
            + (0.28 * ndotl_r)[:, None] * np.array([0.65, 0.92, 1.00], dtype=np.float32)
            + (0.52 * ndotl_p1)[:, None] * p1_col[None, :]
            + (0.52 * ndotl_p2)[:, None] * p2_col[None, :]
        ) * ao_vert[:, None]

        v_spec = (
            spec_k[:, None] * np.array([0.98, 0.96, 0.92], dtype=np.float32)
            + fresnel[:, None] * (0.5 * np.array([0.78, 0.90, 1.0], dtype=np.float32) + 0.5 * p1_col[None, :])
        )

        th, tw = (tex_arr.shape[0], tex_arr.shape[1]) if tex_arr is not None else (0, 0)
        is_pure_led = (float(np.max(emissive)) > 0.35) and (tex_arr is None or tw <= 256)
        is_oled_screen = (float(np.max(emissive)) > 0.25) and (tex_arr is not None and tw >= 512)

        for tri in idx:
            i0, i1, i2 = tri[0], tri[1], tri[2]
            if not (valid_v[i0] and valid_v[i1] and valid_v[i2]):
                continue
            x0, y0, z0 = px[i0], py[i0], cz[i0]
            x1, y1, z1 = px[i1], py[i1], cz[i1]
            x2, y2, z2 = px[i2], py[i2], cz[i2]
            xmin, xmax = max(0, int(min(x0, x1, x2))), min(rw - 1, int(max(x0, x1, x2)) + 1)
            ymin, ymax = max(0, int(min(y0, y1, y2))), min(rh - 1, int(max(y0, y1, y2)) + 1)
            if xmin >= xmax or ymin >= ymax:
                continue
            denom = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
            if abs(denom) < 1e-5:
                continue
            inv_d = 1.0 / denom
            gy, gx = np.mgrid[ymin : ymax + 1, xmin : xmax + 1]
            w0 = ((y1 - y2) * (gx - x2) + (x2 - x1) * (gy - y2)) * inv_d
            w1 = ((y2 - y0) * (gx - x2) + (x0 - x2) * (gy - y2)) * inv_d
            w2 = 1.0 - w0 - w1
            mask = (w0 >= 0.0) & (w1 >= 0.0) & (w2 >= 0.0)
            if not np.any(mask):
                continue
            z_interp = w0 * z0 + w1 * z1 + w2 * z2
            z_sub = zbuf[ymin : ymax + 1, xmin : xmax + 1]
            vis = mask & (z_interp < z_sub)
            if not np.any(vis):
                continue
            z_sub[vis] = z_interp[vis]
            obj_mask[ymin : ymax + 1, xmin : xmax + 1][vis] = True
            vw0, vw1, vw2 = w0[vis], w1[vis], w2[vis]

            if tex_arr is not None:
                uv_interp = vw0[:, None] * uvs[i0] + vw1[:, None] * uvs[i1] + vw2[:, None] * uvs[i2]
                tx = np.clip((uv_interp[:, 0] % 1.0) * tw, 0, tw - 1).astype(np.int32)
                ty = np.clip((uv_interp[:, 1] % 1.0) * th, 0, th - 1).astype(np.int32)
                albedo = tex_arr[ty, tx, :3] * base_cf
            else:
                albedo = base_cf[None, :]

            n_interp = vw0[:, None] * norms[i0] + vw1[:, None] * norms[i1] + vw2[:, None] * norms[i2]
            nbuf[ymin : ymax + 1, xmin : xmax + 1][vis] = n_interp

            if is_oled_screen:
                spec_i = vw0[:, None] * v_spec[i0] + vw1[:, None] * v_spec[i1] + vw2[:, None] * v_spec[i2]
                col = np.clip(albedo * 1.45 + spec_i * 0.35, 0.0, 1.0)
                ebuf[ymin : ymax + 1, xmin : xmax + 1][vis] = np.clip(albedo * 0.75, 0.0, 1.0)
            elif is_pure_led:
                col = np.clip(albedo * 0.45 + emissive * 0.95, 0.0, 1.0)
                ebuf[ymin : ymax + 1, xmin : xmax + 1][vis] = emissive
            else:
                shade_i = vw0[:, None] * v_shade[i0] + vw1[:, None] * v_shade[i1] + vw2[:, None] * v_shade[i2]
                spec_i = vw0[:, None] * v_spec[i0] + vw1[:, None] * v_spec[i1] + vw2[:, None] * v_spec[i2]
                col = np.clip(albedo * shade_i + spec_i + emissive * 0.35, 0.0, 1.0)

            fbuf[ymin : ymax + 1, xmin : xmax + 1][vis] = col

    # Apply SSAO to opaque surfaces
    z_clean = np.where(obj_mask, zbuf, np.nanmedian(zbuf[obj_mask]) if np.any(obj_mask) else 3.0)
    z_blur_fine = gaussian_filter(z_clean, sigma=3.5)
    z_blur_wide = gaussian_filter(z_clean, sigma=14.0)
    cavity_fine = np.clip((z_clean - z_blur_fine) * 4.2, 0.0, 0.34)
    cavity_wide = np.clip((z_clean - z_blur_wide) * 2.0, 0.0, 0.28)
    n_grad = np.zeros((rh, rw), dtype=np.float32)
    for c in range(3):
        gy_n, gx_n = np.gradient(nbuf[:, :, c])
        n_grad += np.hypot(gx_n, gy_n)
    crease_ao = np.clip(n_grad * 0.20, 0.0, 0.25)
    ssao = np.where(obj_mask, np.clip(1.0 - (cavity_fine + cavity_wide + crease_ao), 0.46, 1.0), 1.0)
    fbuf *= ssao[:, :, None]

    # PASS 2: SORTED ALPHA-BLEND TRANSPARENCY PASS (alphaMode == 'BLEND' Canopy & UV Pharmacy Glass)
    blend_tris_sorted = []
    for pos, norms, uvs, idx, bcf, roughness, metallic, emissive, tex_arr in blend_prims:
        px, py, cz = _project_pts(pos)
        v_to_cam = cam_pos - pos
        v_to_cam /= np.maximum(np.linalg.norm(v_to_cam, axis=1, keepdims=True), 1e-6)
        h_key = key_dir + v_to_cam
        h_key /= np.maximum(np.linalg.norm(h_key, axis=1, keepdims=True), 1e-6)
        spec_k = (np.maximum(np.sum(norms * h_key, axis=1), 0.0) ** 95.0) * 0.75
        ndotv = np.clip(np.abs(np.sum(norms * v_to_cam, axis=1)), 0.0, 1.0)
        fresnel = ((1.0 - ndotv) ** 2.4) * 0.48

        for tri in idx:
            i0, i1, i2 = tri[0], tri[1], tri[2]
            z_mean = float(cz[i0] + cz[i1] + cz[i2]) / 3.0
            blend_tris_sorted.append((z_mean, pos, norms, uvs, (i0, i1, i2), px, py, cz, spec_k, fresnel, bcf, emissive, tex_arr))

    blend_tris_sorted.sort(key=lambda item: item[0], reverse=True)

    for _, pos, norms, uvs, (i0, i1, i2), px, py, cz, spec_k, fresnel, bcf, emissive, tex_arr in blend_tris_sorted:
        x0, y0, z0 = px[i0], py[i0], cz[i0]
        x1, y1, z1 = px[i1], py[i1], cz[i1]
        x2, y2, z2 = px[i2], py[i2], cz[i2]
        xmin, xmax = max(0, int(min(x0, x1, x2))), min(rw - 1, int(max(x0, x1, x2)) + 1)
        ymin, ymax = max(0, int(min(y0, y1, y2))), min(rh - 1, int(max(y0, y1, y2)) + 1)
        if xmin >= xmax or ymin >= ymax:
            continue
        denom = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(denom) < 1e-5:
            continue
        inv_d = 1.0 / denom
        gy, gx = np.mgrid[ymin : ymax + 1, xmin : xmax + 1]
        w0 = ((y1 - y2) * (gx - x2) + (x2 - x1) * (gy - y2)) * inv_d
        w1 = ((y2 - y0) * (gx - x2) + (x0 - x2) * (gy - y2)) * inv_d
        w2 = 1.0 - w0 - w1
        mask = (w0 >= 0.0) & (w1 >= 0.0) & (w2 >= 0.0)
        if not np.any(mask):
            continue
        z_interp = w0 * z0 + w1 * z1 + w2 * z2
        z_sub = zbuf[ymin : ymax + 1, xmin : xmax + 1]
        vis = mask & (z_interp < z_sub)
        if not np.any(vis):
            continue

        vw0, vw1, vw2 = w0[vis], w1[vis], w2[vis]
        uv_i = vw0[:, None] * uvs[i0] + vw1[:, None] * uvs[i1] + vw2[:, None] * uvs[i2]
        u_coord, v_coord = uv_i[:, 0], uv_i[:, 1]

        if tex_arr is not None:
            th, tw = tex_arr.shape[0], tex_arr.shape[1]
            tx = np.clip((u_coord % 1.0) * tw, 0, tw - 1).astype(np.int32)
            ty = np.clip((v_coord % 1.0) * th, 0, th - 1).astype(np.int32)
            samp = tex_arr[ty, tx]
            glass_rgb = samp[:, :3] * bcf[:3]
            alpha = np.clip(samp[:, 3] * bcf[3], 0.14, 0.24)
        else:
            glass_rgb = np.broadcast_to(bcf[:3], (len(u_coord), 3)).copy()
            alpha = np.full(len(u_coord), float(bcf[3]), dtype=np.float32)

        diag_band1 = np.exp(-(((u_coord * 0.85 + v_coord * 0.45 - 0.58) / 0.038) ** 2)) * 0.22
        diag_band2 = np.exp(-(((u_coord * 0.85 + v_coord * 0.45 - 0.72) / 0.018) ** 2)) * 0.15
        edge_dist = np.minimum(np.minimum(u_coord, 1.0 - u_coord), np.minimum(v_coord, 1.0 - v_coord))
        edge_glow = np.exp(-((edge_dist / 0.035) ** 2)) * 0.44

        spec_i = vw0 * spec_k[i0] + vw1 * spec_k[i1] + vw2 * spec_k[i2] + diag_band1 + diag_band2
        fres_i = vw0 * fresnel[i0] + vw1 * fresnel[i1] + vw2 * fresnel[i2] + edge_glow

        rim_tint = np.array(accent_rgb, dtype=np.float32)
        glass_tint = glass_rgb + emissive[None, :] + fres_i[:, None] * rim_tint[None, :]
        bg_sub = fbuf[ymin : ymax + 1, xmin : xmax + 1][vis]
        blended = bg_sub * (1.0 - alpha[:, None]) + glass_tint * alpha[:, None] + spec_i[:, None] * np.array([0.88, 0.96, 1.0], dtype=np.float32)
        fbuf[ymin : ymax + 1, xmin : xmax + 1][vis] = np.clip(blended, 0.0, 1.0)
        ebuf[ymin : ymax + 1, xmin : xmax + 1][vis] += (edge_glow * 0.32)[:, None] * rim_tint[None, :]

    # PASS 3: EMISSIVE BLOOM
    bloom_tight = gaussian_filter(ebuf, sigma=(5.0, 5.0, 0.0))
    bloom_wide = gaussian_filter(ebuf, sigma=(18.0, 18.0, 0.0))
    fbuf = np.clip(fbuf + bloom_tight * 0.38 + bloom_wide * 0.26, 0.0, 1.0)

    return Image.fromarray((fbuf * 255.0).astype(np.uint8), mode="RGB")


def render_all_medbay_autodocs_and_voting_sheet():
    manifest_path = os.path.join(GLB_MEDBAY_DIR, "medbay_r1_manifest.json")
    with open(manifest_path, "r") as f:
        manifest_data = json.load(f)

    stats_by_id = {os.path.splitext(os.path.basename(item["filepath"]))[0]: item for item in manifest_data}

    font_badge = load_font(28, bold=True)
    font_title = load_font(24, bold=True)
    font_sub = load_font(17, bold=False)
    font_stats = load_font(18, bold=True)
    font_callouts = load_font(16, bold=False)

    for cid, num_str, slug, short_title, subtitle, callouts, (yaw, pitch), l1_cfg, l2_cfg, accent_rgb in CANDIDATE_MEDBAY_META:
        glb_path = os.path.join(GLB_MEDBAY_DIR, f"{cid}.glb")
        raw_img = render_medbay_candidate(
            glb_path,
            width=1920,
            height=1080,
            cam_yaw_deg=yaw,
            cam_pitch_deg=pitch,
            light1_cfg=l1_cfg,
            light2_cfg=l2_cfg,
            accent_rgb=accent_rgb,
        )

        raw_out_path = os.path.join(GODOT_RENDER_DIR, f"{cid}.png")
        raw_img.save(raw_out_path, "PNG", optimize=True)

        w, h = raw_img.size
        st = stats_by_id.get(cid, {})
        n_tris = st.get("triangles", 0)
        n_verts = st.get("vertices", 0)
        dims = st.get("dimensions", [2.20, 2.15, 1.28])

        overlay = raw_img.copy()
        draw = ImageDraw.Draw(overlay)

        draw.rounded_rectangle([24, 22, 1020, 108], radius=10, fill=(14, 19, 26), outline=(0, 195, 235), width=2)
        draw.rounded_rectangle([38, 34, 114, 96], radius=8, fill=(0, 185, 225), outline=(185, 245, 255), width=2)
        draw.text((48, 48), f"#{num_str}", fill=(10, 14, 20), font=font_badge)

        draw.text((132, 34), f"#{num_str} — {short_title}", fill=(236, 244, 252), font=font_title)
        draw.text((132, 68), f"{subtitle}  ({slug})", fill=(110, 210, 240), font=font_sub)

        spec_text = f"{n_tris:,} Tris  |  {n_verts:,} Verts  |  {dims[0]:.2f}m W × {dims[2]:.2f}m D × {dims[1]:.2f}m H"
        draw.rounded_rectangle([w - 620, 22, w - 24, 76], radius=8, fill=(14, 19, 26), outline=(64, 96, 128), width=2)
        draw.text((w - 600, 38), spec_text, fill=(186, 224, 248), font=font_stats)

        draw.rounded_rectangle([24, h - 68, w - 24, h - 18], radius=8, fill=(14, 19, 26), outline=(56, 82, 108), width=2)
        draw.text((44, h - 53), f"SURGICAL AUTODOC SPEC:  {callouts}", fill=(220, 232, 244), font=font_callouts)

        out_path = os.path.join(OUT_RENDER_DIR, f"{cid}.png")
        overlay.save(out_path, "PNG", optimize=True)
        print(f"[render_medbay] Saved beauty shot: {out_path} ({w}x{h}, {n_tris} tris)")

    # Compose 5-Panel Comparison Voting Sheet (3344 x 798)
    cols = 5
    cell_w = 640
    cell_img_h = 520
    cell_footer_h = 116
    cell_h = cell_img_h + cell_footer_h
    pad = 24
    header_h = 114

    canvas_w = pad + cols * (cell_w + pad)
    canvas_h = header_h + pad + cell_h + pad

    sheet = Image.new("RGB", (canvas_w, canvas_h), (12, 16, 22))
    draw = ImageDraw.Draw(sheet)

    font_h_title = load_font(34, bold=True)
    font_h_sub = load_font(19, bold=False)
    font_c_badge = load_font(26, bold=True)
    font_c_title = load_font(15, bold=True)
    font_c_meta = load_font(14, bold=True)
    font_c_desc = load_font(13, bold=False)

    draw.rectangle([0, 0, canvas_w, header_h], fill=(18, 24, 33))
    draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(0, 195, 235), width=3)
    draw.text(
        (pad, 20),
        "CYLINDER HAB-7 — ROOM 04 HERO ASSET: SURGICAL AUTODOC GANTRY & TRIAGE CONSOLE (5-CHOICE TEST)",
        fill=(238, 246, 255),
        font=font_h_title,
    )
    draw.text(
        (pad, 68),
        "Articulated 3D Robotic Surgical Arms • Translucent Bio-Isolation Canopy • UV-Sterile Pharmacy & Cryo-Vial Tower • Vote 01 – 05",
        fill=(110, 214, 245),
        font=font_h_sub,
    )

    for idx, (cid, num_str, slug, short_title, subtitle, callouts, _, _, _, _) in enumerate(CANDIDATE_MEDBAY_META):
        x0 = pad + idx * (cell_w + pad)
        y0 = header_h + pad

        draw.rounded_rectangle(
            [x0 - 2, y0 - 2, x0 + cell_w + 2, y0 + cell_h + 2],
            radius=10,
            fill=(22, 28, 38),
            outline=(58, 88, 118),
            width=2,
        )

        raw_path = os.path.join(GODOT_RENDER_DIR, f"{cid}.png")
        if os.path.exists(raw_path):
            im = Image.open(raw_path).convert("RGB")
            iw, ih = im.size
            crop_w = 1330
            left = (iw - crop_w) // 2
            im_cropped = im.crop((left, 0, left + crop_w, ih)).resize((cell_w, cell_img_h), Image.Resampling.LANCZOS)
            sheet.paste(im_cropped, (x0, y0))

        bx0, by0 = x0 + 12, y0 + 12
        draw.rounded_rectangle(
            [bx0, by0, bx0 + 62, by0 + 44],
            radius=8,
            fill=(0, 185, 225),
            outline=(195, 248, 255),
            width=2,
        )
        draw.text((bx0 + 13, by0 + 8), num_str, fill=(10, 14, 20), font=font_c_badge)

        st = stats_by_id.get(cid, {})
        n_tris = st.get("triangles", 0)
        dims = st.get("dimensions", [2.20, 2.15, 1.28])

        tb_w = 132
        draw.rounded_rectangle(
            [x0 + cell_w - tb_w - 12, y0 + 12, x0 + cell_w - 12, y0 + 42],
            radius=6,
            fill=(14, 19, 26),
            outline=(72, 112, 148),
            width=1,
        )
        draw.text((x0 + cell_w - tb_w - 2, y0 + 19), f"{n_tris:,} TRIS", fill=(176, 228, 252), font=font_c_meta)

        fy0 = y0 + cell_img_h
        draw.rectangle([x0, fy0, x0 + cell_w, y0 + cell_h], fill=(17, 22, 30))
        draw.text((x0 + 14, fy0 + 10), f"#{num_str} — {short_title}", fill=(238, 246, 255), font=font_c_title)
        draw.text(
            (x0 + 14, fy0 + 38),
            f"{cid}.glb  •  {dims[0]:.2f}m W × {dims[2]:.2f}m D × {dims[1]:.2f}m H  •  {n_tris:,} tris",
            fill=(96, 206, 240),
            font=font_c_meta,
        )
        short_callout = callouts if len(callouts) <= 78 else callouts[:75] + "..."
        draw.text((x0 + 14, fy0 + 68), short_callout, fill=(176, 190, 206), font=font_c_desc)

    for out_p in [
        os.path.join(OUT_RENDER_DIR, "medbay_round1_voting_sheet.png"),
        os.path.join(OUT_RENDER_DIR, "med_autodoc_round1_voting_sheet.png"),
        os.path.join(GODOT_RENDER_DIR, "medbay_round1_voting_sheet.png"),
        os.path.join(GODOT_RENDER_DIR, "med_autodoc_round1_voting_sheet.png"),
    ]:
        sheet.save(out_p, "PNG", optimize=True)
        print(f"[render_medbay] Saved 5-panel voting sheet: {out_p} ({canvas_w}x{canvas_h})")


if __name__ == "__main__":
    render_all_medbay_autodocs_and_voting_sheet()
