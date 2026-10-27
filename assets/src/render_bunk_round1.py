#!/usr/bin/env python3
"""
High-Craft Hard Sci-Fi Spacecraft Bay Renderer & Voting Sheet Composer for
Sci-Fi Bunk Pod — Round 1 (bunk_r1_01.glb .. bunk_r1_10.glb).

Renders every candidate inside a dark, moody, sleek spacecraft bay environment:
- Dark gunmetal paneled bulkhead wall (#12161D to #1B222C) with subtle chamfered spacecraft hull seam lines
  and soft recessed cyan/amber rim lighting.
- Dark metallic composite deck floor (#0F1318 to #171C24) with subtle metallic specular reflection,
  soft contact AO shadow under the pod, and a clean recessed deck light line.
- True Z-buffered Supersampled (SSAA) 3D rasterization with smooth vertex normal interpolation,
  Blinn-Phong metallic/roughness specular highlights, Screen-Space Ambient Occlusion (SSAO) in crevices,
  and Gaussian emissive bloom from cyan (#00E5FF) & amber (#FF9500) practical LED strips.
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
from glb_builder import make_quad_panel

GLB_DIR = "/workspace/game-project/assets/glb/bunk_round1"
OUT_RENDER_DIR = "/workspace/game-project/assets/renders/bunk_round1"
GODOT_RENDER_DIR = "/workspace/game-project/godot/renders/bunk_round1"

os.makedirs(OUT_RENDER_DIR, exist_ok=True)
os.makedirs(GODOT_RENDER_DIR, exist_ok=True)

CANDIDATE_META = [
    (
        "bunk_r1_01",
        "01",
        "01_aerospace_cryo_berth",
        "AEROSPACE CRYO BERTH",
        "Molded White Aerospace Sleep Capsule",
        "Chamfered white composite hull • Smoked polycarbonate sliding canopy • Cyan LED cove • OLED vitals HUD",
        (24.0, -15.0),
        (0.0, 0.90, 1.0),
    ),
    (
        "bunk_r1_02",
        "02",
        "02_expanse_bulkhead_rack",
        "EXPANSE BULKHEAD RACK",
        "High-G Armored Bulkhead Berth",
        "Gunmetal titanium hull bay • Curved C-channel ribs • Gimbaled shock mounts & G-bolsters • Amber caution LEDs",
        (-22.0, -15.0),
        (1.0, 0.58, 0.0),
    ),
    (
        "bunk_r1_03",
        "03",
        "03_zero_g_mag_couchette",
        "ZERO-G MAG COUCHETTE",
        "Cantilevered Mag-Lock Orbital Pod",
        "Floating carbon-slate & titanium sleep sled • Twin magnetic guide rails • Cyan indicators • Surgical LED arms",
        (25.0, -16.0),
        (0.0, 0.90, 1.0),
    ),
    (
        "bunk_r1_04",
        "04",
        "04_blast_shutter_pod",
        "BLAST-SHUTTER POD",
        "Armored Blast-Shutter Crew Pod",
        "Segmented curved titanium blast shutter • Pressurized gasket rim • Contoured charcoal pad • Telemetry HUD",
        (-23.0, -14.0),
        (1.0, 0.65, 0.15),
    ),
    (
        "bunk_r1_05",
        "05",
        "05_spin_transition_harness_bunk",
        "SPIN-TRANSITION HARNESS BUNK",
        "Zero-G / Spin-Gravity Restraint Pod",
        "Tubular EVA lockdown bars • 4-point ballistic webbing & cam buckles • Grey/orange flight couch • Cyan cove",
        (22.0, -16.0),
        (0.0, 0.90, 1.0),
    ),
    (
        "bunk_r1_06",
        "06",
        "06_orbital_viewport_pod",
        "ORBITAL VIEWPORT POD",
        "Deep-Space Observation Sleep Bay",
        "Chamfered octagonal spacecraft viewport • Starlit O'Neill core vista • Cyan edge-lit bezel • Zero-G couch",
        (-20.0, -14.0),
        (0.0, 0.90, 1.0),
    ),
    (
        "bunk_r1_07",
        "07",
        "07_stacked_corvette_bunks",
        "STACKED CORVETTE BUNKS",
        "Naval Frigate Dual Pod Stack",
        "Dual enclosed composite sleep tubes (BAY 01 / BAY 02) • Angled titanium ladder • Smoked shields • Cyan/Amber LEDs",
        (24.0, -14.0),
        (0.25, 0.85, 1.0),
    ),
    (
        "bunk_r1_08",
        "08",
        "08_recessed_stasis_alcove",
        "RECESSED STASIS ALCOVE",
        "Pressurized Stasis-Style Sleep Chamber",
        "Octagonal stasis aperture • Stepped metallic deck with amber hazard strip • Cranial scanner halo & cryo tubes",
        (-24.0, -16.0),
        (1.0, 0.62, 0.10),
    ),
    (
        "bunk_r1_09",
        "09",
        "09_bio_lifesupport_pod",
        "BIO-LIFESUPPORT POD",
        "Closed-Loop O2 Scrubber & Hydro-Bay Pod",
        "Sealed cylindrical glass photobioreactor tube • Cyan/UV grow-LEDs • Titanium O2 scrubber conduits & gauges",
        (23.0, -15.0),
        (0.0, 0.95, 0.88),
    ),
    (
        "bunk_r1_10",
        "10",
        "10_command_stateroom_capsule",
        "COMMAND STATEROOM CAPSULE",
        "Officer's Panoramic Smart-Pod",
        "Sweeping brushed-titanium canopy arch • Twin angled OLED status wings • Cyan & amber cove arches • Wide couch",
        (-22.0, -15.0),
        (0.15, 0.85, 1.0),
    ),
]


def load_font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def make_spacecraft_bay_backdrop(width: int, height: int, accent_rgb: tuple) -> np.ndarray:
    """
    Generates a sleek, dark, moody spacecraft bay background (#12161D bulkhead wall & #0F1318 deck floor)
    with subtle chamfered hull seam lines, recessed deck light line, and atmospheric cyan/amber rim glow.
    """
    yy, xx = np.mgrid[0:height, 0:width].astype(np.float32)
    yn = yy / float(height)
    xn = xx / float(width)

    bg = np.zeros((height, width, 3), dtype=np.float32)
    horizon_y = 0.66

    # Upper spacecraft bulkhead wall (#12161D to #1B222C)
    wall_mask = yn <= horizon_y
    wy = np.clip(yn / horizon_y, 0.0, 1.0)
    wall_top = np.array([0.070, 0.086, 0.114], dtype=np.float32)   # #12161D
    wall_bot = np.array([0.106, 0.133, 0.173], dtype=np.float32)   # #1B222C
    radial = np.exp(-(((xn - 0.5) * 1.35) ** 2 + ((yn - 0.44) * 1.65) ** 2))

    for c in range(3):
        w_col = wall_top[c] * (1.0 - wy) + wall_bot[c] * wy + 0.038 * radial
        bg[:, :, c] = w_col

    # Subtle chamfered spacecraft bulkhead panel seams on rear wall
    v_seam1 = np.abs(xn - 0.22) < 0.0016
    v_seam2 = np.abs(xn - 0.78) < 0.0016
    h_seam1 = np.abs(yn - 0.24) < 0.0018
    seams = (v_seam1 | v_seam2 | h_seam1) & wall_mask
    bg[seams] *= 0.74

    # Lower metallic composite deck floor (#0F1318 to #171C24)
    floor_mask = yn > horizon_y
    fy = np.clip((yn - horizon_y) / (1.0 - horizon_y), 0.0, 1.0)
    floor_near = np.array([0.059, 0.075, 0.094], dtype=np.float32)  # #0F1318
    floor_mid = np.array([0.090, 0.110, 0.141], dtype=np.float32)   # #171C24
    spec_pool = np.exp(-(((xn - 0.5) * 1.6) ** 2 + ((fy - 0.32) * 2.4) ** 2))

    for c in range(3):
        f_col = floor_mid[c] * (1.0 - fy) + floor_near[c] * fy + (0.032 + 0.025 * accent_rgb[c]) * spec_pool
        bg[:, :, c] = np.where(floor_mask, f_col, bg[:, :, c])

    # Recessed bulkhead-to-deck cove shadow & subtle glowing deck trim line
    cove_band = np.abs(yn - horizon_y) < 0.0035
    bg[cove_band] *= 0.55

    deck_line = (np.abs(yn - (horizon_y + 0.012)) < 0.0018) & (xn > 0.18) & (xn < 0.82)
    for c in range(3):
        bg[:, :, c] = np.where(deck_line, 0.22 + 0.45 * accent_rgb[c], bg[:, :, c])

    return np.clip(bg, 0.0, 1.0)


def render_scifi_bunk_glb(
    glb_path: str,
    width: int = 1920,
    height: int = 1080,
    cam_yaw_deg: float = 24.0,
    cam_pitch_deg: float = -15.0,
    accent_rgb: tuple = (0.0, 0.90, 1.0),
) -> Image.Image:
    """
    Renders a Hard Sci-Fi Bunk Pod .glb model at 1920x1080 with:
    - Dark gunmetal spacecraft bay backdrop + 3D perspective metallic floor contact shadow
    - True Z-buffer & Normal-buffer rasterization
    - Screen-Space Ambient Occlusion (SSAO) & crevice cavity enhancement
    - 3-point cool-white/cyan studio rig + practical emissive point light + Gaussian bloom
    """
    gltf = pygltflib.GLTF2().load(glb_path)
    blob = gltf.binary_blob()

    tex_images = {}
    for t_idx, tex in enumerate(gltf.textures):
        if tex.source is not None:
            img_obj = gltf.images[tex.source]
            bv = gltf.bufferViews[img_obj.bufferView]
            png_bytes = blob[bv.byteOffset : bv.byteOffset + bv.byteLength]
            pil_img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
            tex_images[t_idx] = np.asarray(pil_img, dtype=np.float32) / 255.0

    def _read_acc(acc_idx: int) -> np.ndarray:
        acc = gltf.accessors[acc_idx]
        bv = gltf.bufferViews[acc.bufferView]
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

    prims_data = []
    all_pts = []
    for mesh in gltf.meshes:
        for prim in mesh.primitives:
            pos = _read_acc(prim.attributes.POSITION).astype(np.float32)
            norms = _read_acc(prim.attributes.NORMAL).astype(np.float32)
            uvs = _read_acc(prim.attributes.TEXCOORD_0).astype(np.float32)
            idx = _read_acc(prim.indices).reshape(-1, 3)
            all_pts.append(pos)

            mat = gltf.materials[prim.material] if prim.material is not None else None
            base_cf = np.array(mat.pbrMetallicRoughness.baseColorFactor[:3], dtype=np.float32) if mat else np.ones(3, dtype=np.float32)
            roughness = float(mat.pbrMetallicRoughness.roughnessFactor) if (mat and mat.pbrMetallicRoughness.roughnessFactor is not None) else 0.45
            metallic = float(mat.pbrMetallicRoughness.metallicFactor) if (mat and mat.pbrMetallicRoughness.metallicFactor is not None) else 0.2
            emissive = np.array(mat.emissiveFactor[:3], dtype=np.float32) if (mat and mat.emissiveFactor) else np.zeros(3, dtype=np.float32)
            tex_arr = None
            if mat and mat.pbrMetallicRoughness.baseColorTexture is not None:
                tex_arr = tex_images.get(mat.pbrMetallicRoughness.baseColorTexture.index)
            prims_data.append((pos, norms, uvs, idx, base_cf, roughness, metallic, emissive, tex_arr))

    pts_stack = np.vstack(all_pts)
    min_pt = pts_stack.min(axis=0)
    max_pt = pts_stack.max(axis=0)
    size = max_pt - min_pt

    # Camera setup
    target = np.array([0.0, size[1] * 0.48, 0.0], dtype=np.float32)
    yaw = math.radians(cam_yaw_deg)
    pitch = math.radians(cam_pitch_deg)
    radius = max(float(size[0]), float(size[1])) * 1.48
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

    # Project floor footprint to cast a soft contact shadow & subtle cyan/amber under-glow on the deck
    foot_corners = np.array([
        [min_pt[0], 0.0, min_pt[2]],
        [max_pt[0], 0.0, min_pt[2]],
        [max_pt[0], 0.0, max_pt[2]],
        [min_pt[0], 0.0, max_pt[2]],
        [0.0, 0.0, 0.0],
    ], dtype=np.float32)
    fpx, fpy, _ = _project_pts(foot_corners)
    fcx, fcy = float(fpx[4]), float(fpy[4])
    rx_foot = max(float(np.max(np.abs(fpx[:4] - fcx))) * 1.08, 120.0)
    ry_foot = max(float(np.max(np.abs(fpy[:4] - fcy))) * 1.15, 45.0)
    yy_g, xx_g = np.mgrid[0:rh, 0:rw].astype(np.float32)
    ell_d2 = ((xx_g - fcx) / rx_foot) ** 2 + ((yy_g - fcy) / ry_foot) ** 2
    contact_shadow = 1.0 - 0.62 * np.exp(-ell_d2 * 1.65)
    fbuf *= contact_shadow[:, :, None]

    # 3-Point Sci-Fi Studio Lighting + Practical Bay Point Light
    key_dir = np.array([0.46, 0.72, 0.52], dtype=np.float32)
    key_dir /= np.linalg.norm(key_dir)
    fill_dir = np.array([-0.68, 0.36, 0.64], dtype=np.float32)
    fill_dir /= np.linalg.norm(fill_dir)
    rim_dir = np.array([0.0, 0.65, -0.76], dtype=np.float32)
    rim_dir /= np.linalg.norm(rim_dir)

    pt_light_pos = np.array([0.0, size[1] * 0.68, 0.18], dtype=np.float32)
    pt_light_col = np.array(accent_rgb, dtype=np.float32)

    for pos, norms, uvs, idx, base_cf, roughness, metallic, emissive, tex_arr in prims_data:
        px, py, cz = _project_pts(pos)
        valid_v = cz > 0.15

        v_to_cam = cam_pos - pos
        v_to_cam /= np.maximum(np.linalg.norm(v_to_cam, axis=1, keepdims=True), 1e-6)

        ndotl_k = np.maximum(norms @ key_dir, 0.0)
        ndotl_f = np.maximum(norms @ fill_dir, 0.0)
        ndotl_r = np.maximum(norms @ rim_dir, 0.0)

        # Blinn-Phong specular for key & fill lights
        h_key = key_dir + v_to_cam
        h_key /= np.maximum(np.linalg.norm(h_key, axis=1, keepdims=True), 1e-6)
        shininess = max(8.0, (1.0 - roughness) * 72.0)
        spec_strength = 0.22 + 0.68 * metallic + (0.35 if roughness < 0.25 else 0.0)
        spec_k = (np.maximum(np.sum(norms * h_key, axis=1), 0.0) ** shininess) * spec_strength

        # Fresnel rim sheen for sleek spacecraft hulls & polycarbonate canopies
        ndotv = np.clip(np.sum(norms * v_to_cam, axis=1), 0.0, 1.0)
        fresnel = ((1.0 - ndotv) ** 3.0) * (0.18 + 0.32 * metallic)

        # Practical interior bay point light
        l_vec = pt_light_pos - pos
        l_dist = np.maximum(np.linalg.norm(l_vec, axis=1, keepdims=True), 0.22)
        l_dir = l_vec / l_dist
        atten = 1.0 / (1.0 + 0.55 * (l_dist[:, 0] ** 2))
        ndotl_p = np.maximum(np.sum(norms * l_dir, axis=1), 0.0) * atten

        # Vertical & cavity ambient occlusion weight
        ao_vert = np.clip(0.62 + 0.38 * (pos[:, 1] / max(float(size[1]), 1.0)), 0.60, 1.0)

        v_shade = (
            (0.28 + 0.10 * norms[:, 1])[:, None] * np.array([0.82, 0.88, 0.96], dtype=np.float32)
            + (0.64 * ndotl_k)[:, None] * np.array([0.96, 0.98, 1.00], dtype=np.float32)
            + (0.28 * ndotl_f)[:, None] * np.array([0.62, 0.78, 0.96], dtype=np.float32)
            + (0.24 * ndotl_r)[:, None] * np.array([0.70, 0.88, 1.00], dtype=np.float32)
            + (0.58 * ndotl_p)[:, None] * pt_light_col[None, :]
        ) * ao_vert[:, None]

        v_spec = (
            spec_k[:, None] * np.array([0.95, 0.98, 1.0], dtype=np.float32)
            + fresnel[:, None] * (0.5 * np.array([0.75, 0.88, 1.0], dtype=np.float32) + 0.5 * pt_light_col[None, :])
        )

        th, tw = (tex_arr.shape[0], tex_arr.shape[1]) if tex_arr is not None else (0, 0)
        is_emissive = float(np.max(emissive)) > 0.05

        for tri in idx:
            i0, i1, i2 = tri[0], tri[1], tri[2]
            if not (valid_v[i0] and valid_v[i1] and valid_v[i2]):
                continue
            x0, y0, z0 = px[i0], py[i0], cz[i0]
            x1, y1, z1 = px[i1], py[i1], cz[i1]
            x2, y2, z2 = px[i2], py[i2], cz[i2]

            xmin = max(0, int(min(x0, x1, x2)))
            xmax = min(rw - 1, int(max(x0, x1, x2)) + 1)
            ymin = max(0, int(min(y0, y1, y2)))
            ymax = min(rh - 1, int(max(y0, y1, y2)) + 1)
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
                albedo = tex_arr[ty, tx] * base_cf
            else:
                albedo = base_cf[None, :]

            n_interp = vw0[:, None] * norms[i0] + vw1[:, None] * norms[i1] + vw2[:, None] * norms[i2]
            nbuf[ymin : ymax + 1, xmin : xmax + 1][vis] = n_interp

            if is_emissive:
                col = np.clip(albedo * 0.45 + emissive * 0.95, 0.0, 1.0)
                ebuf[ymin : ymax + 1, xmin : xmax + 1][vis] = emissive
            else:
                shade_i = vw0[:, None] * v_shade[i0] + vw1[:, None] * v_shade[i1] + vw2[:, None] * v_shade[i2]
                spec_i = vw0[:, None] * v_spec[i0] + vw1[:, None] * v_spec[i1] + vw2[:, None] * v_spec[i2]
                col = np.clip(albedo * shade_i + spec_i, 0.0, 1.0)

            fbuf[ymin : ymax + 1, xmin : xmax + 1][vis] = col

    # Compute Screen-Space Ambient Occlusion (SSAO) & Crevice Accentuation from Z-buffer and Normal-buffer
    z_clean = np.where(obj_mask, zbuf, np.nanmedian(zbuf[obj_mask]) if np.any(obj_mask) else 3.0)
    z_blur_fine = gaussian_filter(z_clean, sigma=3.5)
    z_blur_wide = gaussian_filter(z_clean, sigma=14.0)
    # Positive (z_clean - z_blur) means pixel is recessed inside a crease/crevice/cavity
    cavity_fine = np.clip((z_clean - z_blur_fine) * 4.5, 0.0, 0.38)
    cavity_wide = np.clip((z_clean - z_blur_wide) * 2.2, 0.0, 0.32)

    # Normal discontinuity crease detection (highlights bevel seams, shutter slats, cushion joints)
    n_grad = np.zeros((rh, rw), dtype=np.float32)
    for c in range(3):
        gy_n, gx_n = np.gradient(nbuf[:, :, c])
        n_grad += np.hypot(gx_n, gy_n)
    crease_ao = np.clip(n_grad * 0.22, 0.0, 0.28)

    ssao = np.where(obj_mask, np.clip(1.0 - (cavity_fine + cavity_wide + crease_ao), 0.42, 1.0), 1.0)
    fbuf *= ssao[:, :, None]

    # Add soft atmospheric Sci-Fi Emissive Bloom around Cyan & Amber LEDs
    bloom_tight = gaussian_filter(ebuf, sigma=(6.0, 6.0, 0.0))
    bloom_wide = gaussian_filter(ebuf, sigma=(22.0, 22.0, 0.0))
    fbuf = np.clip(fbuf + bloom_tight * 0.45 + bloom_wide * 0.35, 0.0, 1.0)

    return Image.fromarray((fbuf * 255.0).astype(np.uint8), mode="RGB")


def render_all_and_compose(manifest_data: list):
    stats_by_id = {os.path.splitext(os.path.basename(item["filepath"]))[0]: item for item in manifest_data}

    font_badge = load_font(28, bold=True)
    font_title = load_font(26, bold=True)
    font_sub = load_font(18, bold=False)
    font_stats = load_font(18, bold=True)
    font_callouts = load_font(17, bold=False)

    for cid, num_str, slug, short_title, subtitle, callouts, (yaw, pitch), accent_rgb in CANDIDATE_META:
        glb_path = os.path.join(GLB_DIR, f"{cid}.glb")
        raw_img = render_scifi_bunk_glb(
            glb_path,
            width=1920,
            height=1080,
            cam_yaw_deg=yaw,
            cam_pitch_deg=pitch,
            accent_rgb=accent_rgb,
        )

        # Save clean unannotated render to GODOT_RENDER_DIR for voting sheet & Godot showcase parity
        raw_out_path = os.path.join(GODOT_RENDER_DIR, f"{cid}.png")
        raw_img.save(raw_out_path, "PNG", optimize=True)

        # Annotate with sleek Sci-Fi HUD Title Badge & Spec Callouts for OUT_RENDER_DIR
        w, h = raw_img.size
        st = stats_by_id.get(cid, {})
        n_tris = st.get("triangles", 0)
        n_verts = st.get("vertices", 0)
        dims = st.get("dimensions", [2.16, 1.80, 1.14])

        overlay = raw_img.copy()
        draw = ImageDraw.Draw(overlay)

        # Top-left Sci-Fi HUD Title Badge Card
        draw.rounded_rectangle([24, 22, 820, 108], radius=10, fill=(14, 19, 26), outline=(0, 195, 235), width=2)
        draw.rounded_rectangle([38, 34, 114, 96], radius=8, fill=(0, 185, 225), outline=(185, 245, 255), width=2)
        draw.text((48, 48), f"#{num_str}", fill=(10, 14, 20), font=font_badge)

        draw.text((132, 34), f"#{num_str} — {short_title}", fill=(236, 244, 252), font=font_title)
        draw.text((132, 68), f"{subtitle}  ({slug})", fill=(110, 210, 240), font=font_sub)

        # Top-right Triangle & Spec Badge
        spec_text = f"{n_tris:,} Tris  |  {n_verts:,} Verts  |  {dims[0]:.2f}m W × {dims[2]:.2f}m D × {dims[1]:.2f}m H"
        draw.rounded_rectangle([w - 620, 22, w - 24, 76], radius=8, fill=(14, 19, 26), outline=(64, 96, 128), width=2)
        draw.text((w - 600, 38), spec_text, fill=(186, 224, 248), font=font_stats)

        # Bottom Callout Bar
        draw.rounded_rectangle([24, h - 68, w - 24, h - 18], radius=8, fill=(14, 19, 26), outline=(56, 82, 108), width=2)
        draw.text((44, h - 53), f"HARD SCI-FI SPEC:  {callouts}", fill=(220, 232, 244), font=font_callouts)

        out_path = os.path.join(OUT_RENDER_DIR, f"{cid}.png")
        overlay.save(out_path, "PNG", optimize=True)
        print(f"[render_scifi] Saved beauty shot: {out_path} ({w}x{h}, {n_tris} tris)")

    # Compose the 10-Panel Comparison Voting Sheet (5x2 grid)
    cols = 5
    rows = 2
    cell_w = 640
    cell_img_h = 360
    cell_footer_h = 104
    cell_h = cell_img_h + cell_footer_h
    pad = 24
    header_h = 112

    canvas_w = pad + cols * (cell_w + pad)
    canvas_h = header_h + pad + rows * (cell_h + pad)

    sheet = Image.new("RGB", (canvas_w, canvas_h), (12, 16, 22))
    draw = ImageDraw.Draw(sheet)

    font_h_title = load_font(34, bold=True)
    font_h_sub = load_font(19, bold=False)
    font_c_badge = load_font(26, bold=True)
    font_c_title = load_font(18, bold=True)
    font_c_meta = load_font(14, bold=True)
    font_c_desc = load_font(13, bold=False)

    draw.rectangle([0, 0, canvas_w, header_h], fill=(18, 24, 33))
    draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(0, 195, 235), width=3)
    draw.text(
        (pad, 20),
        "CYLINDER HAB-7 — HARD SCI-FI BUNK POD TOURNAMENT: ROUND 1 OF 4 (10 CANDIDATES)",
        fill=(238, 246, 255),
        font=font_h_title,
    )
    draw.text(
        (pad, 68),
        "Sleek Aerospace & Orbital Crew Bays (2,522 – 4,364 Tris) • Gunmetal, Aerospace White & Titanium PBR • Vote 01 – 10",
        fill=(110, 214, 245),
        font=font_h_sub,
    )

    for idx, (cid, num_str, slug, short_title, subtitle, callouts, _, _) in enumerate(CANDIDATE_META):
        r = idx // cols
        c = idx % cols
        x0 = pad + c * (cell_w + pad)
        y0 = header_h + pad + r * (cell_h + pad)

        draw.rounded_rectangle(
            [x0 - 2, y0 - 2, x0 + cell_w + 2, y0 + cell_h + 2],
            radius=10,
            fill=(22, 28, 38),
            outline=(58, 88, 118),
            width=2,
        )

        raw_path = os.path.join(GODOT_RENDER_DIR, f"{cid}.png")
        if os.path.exists(raw_path):
            im = Image.open(raw_path).convert("RGB").resize((cell_w, cell_img_h), Image.Resampling.LANCZOS)
            sheet.paste(im, (x0, y0))

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
        dims = st.get("dimensions", [2.16, 1.80, 1.14])

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
        draw.text((x0 + 14, fy0 + 8), f"#{num_str} — {short_title}", fill=(238, 246, 255), font=font_c_title)
        draw.text(
            (x0 + 14, fy0 + 35),
            f"{cid}.glb ({slug})  •  {dims[0]:.2f}m W × {dims[2]:.2f}m D × {dims[1]:.2f}m H  •  {n_tris:,} tris",
            fill=(96, 206, 240),
            font=font_c_meta,
        )
        short_callout = callouts if len(callouts) <= 78 else callouts[:75] + "..."
        draw.text((x0 + 14, fy0 + 62), short_callout, fill=(176, 190, 206), font=font_c_desc)

    for out_p in [
        os.path.join(OUT_RENDER_DIR, "bunk_round1_voting_sheet.png"),
        os.path.join(GODOT_RENDER_DIR, "bunk_round1_voting_sheet.png"),
    ]:
        sheet.save(out_p, "PNG", optimize=True)
        print(f"[render_scifi] Saved 10-panel voting sheet: {out_p} ({canvas_w}x{canvas_h})")


def main():
    manifest_path = os.path.join(GLB_DIR, "bunk_r1_manifest.json")
    with open(manifest_path, "r") as f:
        manifest_data = json.load(f)
    render_all_and_compose(manifest_data)


if __name__ == "__main__":
    main()


def render_translucent_viewport_pod(
    glb_path: str,
    vista_tex_path: str,
    width: int = 1600,
    height: int = 1000,
    cam_yaw_deg: float = -16.0,
    cam_pitch_deg: float = -12.0,
    accent_rgb: tuple = (0.0, 0.90, 1.0),
) -> Image.Image:
    """
    Renders a Bunk Pod with a two-pass pipeline:
    Pass 1: Opaque pod geometry + 3D exterior vista skybox plane placed behind the pod's open viewport cutout.
    Pass 2: Sorted alphaMode == 'BLEND' translucent glass triangles blended over the vista with
            Fresnel edge tint, diagonal glass reflection sheen, and crisp Blinn-Phong specular highlights.
    """
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

    vista_arr = np.asarray(Image.open(vista_tex_path).convert("RGB"), dtype=np.float32) / 255.0

    def _read_acc(acc_idx: int) -> np.ndarray:
        acc = gltf.accessors[acc_idx]
        bv = gltf.bufferViews[acc.bufferView]
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
    vista_mask = np.zeros((rh, rw), dtype=bool)

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

    target = np.array([0.0, size[1] * 0.48, 0.0], dtype=np.float32)
    yaw = math.radians(cam_yaw_deg)
    pitch = math.radians(cam_pitch_deg)
    radius = max(float(size[0]), float(size[1])) * 1.42
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
    rx_foot = max(float(np.max(np.abs(fpx[:4] - fcx))) * 1.08, 120.0)
    ry_foot = max(float(np.max(np.abs(fpy[:4] - fcy))) * 1.15, 45.0)
    yy_g, xx_g = np.mgrid[0:rh, 0:rw].astype(np.float32)
    ell_d2 = ((xx_g - fcx) / rx_foot) ** 2 + ((yy_g - fcy) / ry_foot) ** 2
    fbuf *= (1.0 - 0.62 * np.exp(-ell_d2 * 1.65))[:, :, None]

    # Rasterize the exterior vista backdrop plane at Z = min_pt[2] - 0.06m covering the window aperture
    vz = float(min_pt[2]) - 0.06
    v_pos, v_norm, v_uv, v_idx = make_quad_panel(
        (-0.96, 0.58, vz),
        (0.96, 0.58, vz),
        (0.96, 1.72, vz),
        (-0.96, 1.72, vz),
    )
    vpx, vpy, vcz = _project_pts(v_pos)
    vh, vw = vista_arr.shape[0], vista_arr.shape[1]
    for tri in v_idx:
        i0, i1, i2 = tri[0], tri[1], tri[2]
        x0, y0, z0 = vpx[i0], vpy[i0], vcz[i0]
        x1, y1, z1 = vpx[i1], vpy[i1], vcz[i1]
        x2, y2, z2 = vpx[i2], vpy[i2], vcz[i2]
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
        vista_mask[ymin : ymax + 1, xmin : xmax + 1][vis] = True
        vw0, vw1, vw2 = w0[vis], w1[vis], w2[vis]
        uv_i = vw0[:, None] * v_uv[i0] + vw1[:, None] * v_uv[i1] + vw2[:, None] * v_uv[i2]
        tx = np.clip(uv_i[:, 0] * vw, 0, vw - 1).astype(np.int32)
        ty = np.clip(uv_i[:, 1] * vh, 0, vh - 1).astype(np.int32)
        fbuf[ymin : ymax + 1, xmin : xmax + 1][vis] = np.clip(vista_arr[ty, tx] * 1.18, 0.0, 1.0)

    key_dir = np.array([0.46, 0.72, 0.52], dtype=np.float32)
    key_dir /= np.linalg.norm(key_dir)
    fill_dir = np.array([-0.68, 0.36, 0.64], dtype=np.float32)
    fill_dir /= np.linalg.norm(fill_dir)
    rim_dir = np.array([0.0, 0.65, -0.76], dtype=np.float32)
    rim_dir /= np.linalg.norm(rim_dir)
    pt_light_pos = np.array([0.0, size[1] * 0.68, 0.18], dtype=np.float32)
    pt_light_col = np.array(accent_rgb, dtype=np.float32)

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
        shininess = max(8.0, (1.0 - roughness) * 72.0)
        spec_strength = 0.22 + 0.68 * metallic + (0.35 if roughness < 0.25 else 0.0)
        spec_k = (np.maximum(np.sum(norms * h_key, axis=1), 0.0) ** shininess) * spec_strength

        ndotv = np.clip(np.sum(norms * v_to_cam, axis=1), 0.0, 1.0)
        fresnel = ((1.0 - ndotv) ** 3.0) * (0.18 + 0.32 * metallic)

        l_vec = pt_light_pos - pos
        l_dist = np.maximum(np.linalg.norm(l_vec, axis=1, keepdims=True), 0.22)
        l_dir = l_vec / l_dist
        atten = 1.0 / (1.0 + 0.55 * (l_dist[:, 0] ** 2))
        ndotl_p = np.maximum(np.sum(norms * l_dir, axis=1), 0.0) * atten
        ao_vert = np.clip(0.62 + 0.38 * (pos[:, 1] / max(float(size[1]), 1.0)), 0.60, 1.0)

        v_shade = (
            (0.28 + 0.10 * norms[:, 1])[:, None] * np.array([0.82, 0.88, 0.96], dtype=np.float32)
            + (0.64 * ndotl_k)[:, None] * np.array([0.96, 0.98, 1.00], dtype=np.float32)
            + (0.28 * ndotl_f)[:, None] * np.array([0.62, 0.78, 0.96], dtype=np.float32)
            + (0.24 * ndotl_r)[:, None] * np.array([0.70, 0.88, 1.00], dtype=np.float32)
            + (0.58 * ndotl_p)[:, None] * pt_light_col[None, :]
        ) * ao_vert[:, None]

        v_spec = (
            spec_k[:, None] * np.array([0.95, 0.98, 1.0], dtype=np.float32)
            + fresnel[:, None] * (0.5 * np.array([0.75, 0.88, 1.0], dtype=np.float32) + 0.5 * pt_light_col[None, :])
        )

        th, tw = (tex_arr.shape[0], tex_arr.shape[1]) if tex_arr is not None else (0, 0)
        is_emissive = float(np.max(emissive)) > 0.05

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
            vista_mask[ymin : ymax + 1, xmin : xmax + 1][vis] = False
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

            if is_emissive:
                col = np.clip(albedo * 0.45 + emissive * 0.95, 0.0, 1.0)
                ebuf[ymin : ymax + 1, xmin : xmax + 1][vis] = emissive
            else:
                shade_i = vw0[:, None] * v_shade[i0] + vw1[:, None] * v_shade[i1] + vw2[:, None] * v_shade[i2]
                spec_i = vw0[:, None] * v_spec[i0] + vw1[:, None] * v_spec[i1] + vw2[:, None] * v_spec[i2]
                col = np.clip(albedo * shade_i + spec_i, 0.0, 1.0)

            fbuf[ymin : ymax + 1, xmin : xmax + 1][vis] = col

    # Apply SSAO to opaque pod surfaces (excluding the exterior vista skybox)
    z_clean = np.where(obj_mask, zbuf, np.nanmedian(zbuf[obj_mask]) if np.any(obj_mask) else 3.0)
    z_blur_fine = gaussian_filter(z_clean, sigma=3.5)
    z_blur_wide = gaussian_filter(z_clean, sigma=14.0)
    cavity_fine = np.clip((z_clean - z_blur_fine) * 4.5, 0.0, 0.38)
    cavity_wide = np.clip((z_clean - z_blur_wide) * 2.2, 0.0, 0.32)
    n_grad = np.zeros((rh, rw), dtype=np.float32)
    for c in range(3):
        gy_n, gx_n = np.gradient(nbuf[:, :, c])
        n_grad += np.hypot(gx_n, gy_n)
    crease_ao = np.clip(n_grad * 0.22, 0.0, 0.28)
    ssao = np.where(obj_mask & (~vista_mask), np.clip(1.0 - (cavity_fine + cavity_wide + crease_ao), 0.42, 1.0), 1.0)
    fbuf *= ssao[:, :, None]

    # PASS 2: SORTED ALPHA-BLEND TRANSPARENCY PASS (alphaMode == 'BLEND')
    blend_tris_sorted = []
    for pos, norms, uvs, idx, bcf, roughness, metallic, emissive, tex_arr in blend_prims:
        px, py, cz = _project_pts(pos)
        v_to_cam = cam_pos - pos
        v_to_cam /= np.maximum(np.linalg.norm(v_to_cam, axis=1, keepdims=True), 1e-6)
        h_key = key_dir + v_to_cam
        h_key /= np.maximum(np.linalg.norm(h_key, axis=1, keepdims=True), 1e-6)
        spec_k = (np.maximum(np.sum(norms * h_key, axis=1), 0.0) ** 90.0) * 0.85
        ndotv = np.clip(np.abs(np.sum(norms * v_to_cam, axis=1)), 0.0, 1.0)
        fresnel = ((1.0 - ndotv) ** 2.2) * 0.55

        for tri in idx:
            i0, i1, i2 = tri[0], tri[1], tri[2]
            z_mean = float(cz[i0] + cz[i1] + cz[i2]) / 3.0
            blend_tris_sorted.append((z_mean, pos, norms, uvs, (i0, i1, i2), px, py, cz, spec_k, fresnel, bcf, emissive, tex_arr))

    # Sort back-to-front (largest z_mean first)
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
            alpha = np.clip(samp[:, 3] * bcf[3], 0.14, 0.42)
        else:
            glass_rgb = np.broadcast_to(bcf[:3], (len(u_coord), 3)).copy()
            alpha = np.full(len(u_coord), float(bcf[3]), dtype=np.float32)

        # Crisp diagonal spacecraft glass reflection streak & edge refraction glow
        diag_band1 = np.exp(-(((u_coord * 0.85 + v_coord * 0.55 - 0.62) / 0.045) ** 2)) * 0.26
        diag_band2 = np.exp(-(((u_coord * 0.85 + v_coord * 0.55 - 0.74) / 0.022) ** 2)) * 0.18
        edge_dist = np.minimum(np.minimum(u_coord, 1.0 - u_coord), np.minimum(v_coord, 1.0 - v_coord))
        edge_glow = np.exp(-((edge_dist / 0.04) ** 2)) * 0.42

        spec_i = vw0 * spec_k[i0] + vw1 * spec_k[i1] + vw2 * spec_k[i2] + diag_band1 + diag_band2
        fres_i = vw0 * fresnel[i0] + vw1 * fresnel[i1] + vw2 * fresnel[i2] + edge_glow

        glass_tint = glass_rgb + emissive[None, :] + fres_i[:, None] * np.array([0.0, 0.88, 1.0], dtype=np.float32)
        bg_sub = fbuf[ymin : ymax + 1, xmin : xmax + 1][vis]
        blended = bg_sub * (1.0 - alpha[:, None]) + glass_tint * alpha[:, None] + spec_i[:, None] * np.array([0.85, 0.96, 1.0], dtype=np.float32)
        fbuf[ymin : ymax + 1, xmin : xmax + 1][vis] = np.clip(blended, 0.0, 1.0)
        ebuf[ymin : ymax + 1, xmin : xmax + 1][vis] += (edge_glow * 0.35)[:, None] * np.array([0.0, 0.9, 1.0], dtype=np.float32)

    # PASS 3: EMISSIVE BLOOM
    bloom_tight = gaussian_filter(ebuf, sigma=(6.0, 6.0, 0.0))
    bloom_wide = gaussian_filter(ebuf, sigma=(22.0, 22.0, 0.0))
    fbuf = np.clip(fbuf + bloom_tight * 0.45 + bloom_wide * 0.35, 0.0, 1.0)

    return Image.fromarray((fbuf * 255.0).astype(np.uint8), mode="RGB")


def render_winner_01_comparison():
    winner_glb = "/workspace/game-project/assets/glb/winners/bunk_winner_01_orbital_viewport.glb"
    vista_space = "/workspace/game-project/assets/textures/bunk_round2/vista_deep_space.png"
    vista_cyl = "/workspace/game-project/assets/textures/bunk_round2/vista_oneill_cylinder_interior.png"

    img_space = render_translucent_viewport_pod(
        winner_glb, vista_space, width=1280, height=920, cam_yaw_deg=-15.0, cam_pitch_deg=-12.0
    )
    img_cyl = render_translucent_viewport_pod(
        winner_glb, vista_cyl, width=1280, height=920, cam_yaw_deg=15.0, cam_pitch_deg=-12.0
    )

    # Also update bunk_r1_06.png with the translucent deep-space viewport render
    r1_06_raw = render_translucent_viewport_pod(
        "/workspace/game-project/assets/glb/bunk_round1/bunk_r1_06.glb",
        vista_space,
        width=1920,
        height=1080,
        cam_yaw_deg=-16.0,
        cam_pitch_deg=-12.0,
    )
    r1_06_raw.save(os.path.join(GODOT_RENDER_DIR, "bunk_r1_06.png"), "PNG", optimize=True)

    # Compose side-by-side comparison sheet: bunk_winner_01_translucent_views.png (2640 x 1140)
    pad = 24
    header_h = 116
    footer_h = 84
    pw, ph = 1280, 920
    cw = pad * 3 + pw * 2
    ch = header_h + ph + footer_h + pad

    comp = Image.new("RGB", (cw, ch), (12, 16, 22))
    draw = ImageDraw.Draw(comp)
    f_title = load_font(32, bold=True)
    f_sub = load_font(19, bold=False)
    f_panel = load_font(22, bold=True)
    f_desc = load_font(16, bold=False)

    draw.rectangle([0, 0, cw, header_h], fill=(18, 24, 33))
    draw.line([(0, header_h - 2), (cw, header_h - 2)], fill=(0, 195, 235), width=3)
    draw.text(
        (pad, 20),
        "ROUND 1 WINNER #1 UPGRADE: #06 — ORBITAL VIEWPORT POD (TRANSLUCENT GLASS SIGHTLINES)",
        fill=(238, 246, 255),
        font=f_title,
    )
    draw.text(
        (pad, 68),
        "Asset: bunk_winner_01_orbital_viewport.glb  •  True Open Backwall Cutout + alphaMode: BLEND Glass (alpha=0.22)  •  3,168 Tris",
        fill=(110, 214, 245),
        font=f_sub,
    )

    panels = [
        (
            img_space,
            "OUTER-HULL CABIN LOCATION — DEEP SPACE VISTA",
            "Looking through translucent octagonal glass into deep-space starfield, cyan nebula & orbital ring (vista_deep_space.png)",
        ),
        (
            img_cyl,
            "INNER-HULL CABIN LOCATION — O'NEILL CYLINDER INTERIOR VISTA",
            "Looking through translucent octagonal glass into the 800m × 400m O'Neill cylinder biosphere & city lights (vista_oneill_cylinder_interior.png)",
        ),
    ]

    for i, (pim, ptitle, pdesc) in enumerate(panels):
        x0 = pad + i * (pw + pad)
        y0 = header_h
        draw.rounded_rectangle([x0 - 2, y0 - 2, x0 + pw + 2, y0 + ph + footer_h + 2], radius=10, fill=(20, 26, 36), outline=(0, 185, 225), width=2)
        comp.paste(pim, (x0, y0))
        fy0 = y0 + ph
        draw.rectangle([x0, fy0, x0 + pw, fy0 + footer_h], fill=(16, 21, 29))
        draw.text((x0 + 18, fy0 + 12), ptitle, fill=(238, 246, 255), font=f_panel)
        draw.text((x0 + 18, fy0 + 46), pdesc, fill=(140, 214, 242), font=f_desc)

    out_comp = os.path.join(OUT_RENDER_DIR, "bunk_winner_01_translucent_views.png")
    comp.save(out_comp, "PNG", optimize=True)
    print(f"[winner_01] Saved dual translucent comparison sheet: {out_comp} ({cw}x{ch})")
