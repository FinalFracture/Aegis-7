#!/usr/bin/env python3
"""
High-Resolution 3D Shaded Asset Preview Sheet Renderer for Project Cylinder Hab-7.
Renders all 9 .glb models with directional + ambient lighting, texture sampling,
and PBR colors, plus the 8 seamless texture swatches, into:
  /workspace/game-project/assets/renders/asset_sheet.png
"""
import os
import io
import math
import numpy as np
from PIL import Image
import pygltflib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

GLB_DIR = "/workspace/game-project/assets/glb"
TEX_DIR = "/workspace/game-project/assets/textures"
RENDER_DIR = "/workspace/game-project/assets/renders"
os.makedirs(RENDER_DIR, exist_ok=True)


def extract_glb_colored_triangles(glb_path: str, cutaway_room: bool = False):
    """
    Reads a .glb file via pygltflib, decodes its embedded PNG textures, and computes
    per-triangle shaded RGB colors (sampling the texture at each triangle's UV centroid
    multiplied by baseColorFactor + directional/hemisphere lighting + emissive boost).
    """
    gltf = pygltflib.GLTF2().load(glb_path)
    blob = gltf.binary_blob()

    # Decode embedded images into numpy RGB float arrays [0, 1]
    tex_images = {}
    for t_idx, tex in enumerate(gltf.textures):
        if tex.source is not None:
            img_obj = gltf.images[tex.source]
            bv = gltf.bufferViews[img_obj.bufferView]
            png_bytes = blob[bv.byteOffset : bv.byteOffset + bv.byteLength]
            pil_img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
            tex_images[t_idx] = np.asarray(pil_img, dtype=np.float32) / 255.0

    def _read_accessor(acc_idx: int) -> np.ndarray:
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

    tris_xyz = []
    tris_rgb = []
    tris_edge = []
    all_pts = []

    light_dir1 = np.array([0.52, 0.78, 0.34], dtype=np.float32)
    light_dir1 /= np.linalg.norm(light_dir1)
    light_dir2 = np.array([-0.60, 0.35, -0.72], dtype=np.float32)
    light_dir2 /= np.linalg.norm(light_dir2)

    for mesh in gltf.meshes:
        mname = mesh.name or ""
        # For room_shell cutaway isometric view, hide East & South walls and ceiling deck so interior + North viewport show clearly
        if cutaway_room and any(k in mname for k in ["Wall_East", "Wall_South", "Door", "Ceiling_HullDeck"]):
            continue

        for prim in mesh.primitives:
            pos = _read_accessor(prim.attributes.POSITION)
            norms = _read_accessor(prim.attributes.NORMAL)
            uvs = _read_accessor(prim.attributes.TEXCOORD_0)
            idx = _read_accessor(prim.indices).reshape(-1, 3)
            all_pts.append(pos)

            mat = gltf.materials[prim.material] if prim.material is not None else None
            base_cf = np.array(mat.pbrMetallicRoughness.baseColorFactor[:3], dtype=np.float32) if mat else np.ones(3)
            emissive = np.array(mat.emissiveFactor[:3], dtype=np.float32) if (mat and mat.emissiveFactor) else np.zeros(3)
            tex_arr = None
            if mat and mat.pbrMetallicRoughness.baseColorTexture is not None:
                t_i = mat.pbrMetallicRoughness.baseColorTexture.index
                tex_arr = tex_images.get(t_i)

            for tri in idx:
                p0, p1, p2 = pos[tri[0]], pos[tri[1]], pos[tri[2]]
                n = (norms[tri[0]] + norms[tri[1]] + norms[tri[2]]) / 3.0
                nlen = np.linalg.norm(n)
                if nlen > 1e-8:
                    n = n / nlen

                color = base_cf.copy()
                if tex_arr is not None:
                    # Sample 4 points inside triangle for rich texture fidelity
                    uv_c = (uvs[tri[0]] + uvs[tri[1]] + uvs[tri[2]]) / 3.0
                    h, w, _ = tex_arr.shape
                    samples = [uv_c, uvs[tri[0]], uvs[tri[1]], uvs[tri[2]]]
                    s_col = np.zeros(3, dtype=np.float32)
                    for uv_s in samples:
                        px = int(np.clip(uv_s[0], 0.0, 0.9999) * w)
                        py = int(np.clip(uv_s[1], 0.0, 0.9999) * h)
                        s_col += tex_arr[py, px]
                    color = color * (s_col / len(samples))

                # Two-point studio lighting + warm hemisphere ambient
                ndotl1 = max(float(np.dot(n, light_dir1)), 0.0)
                ndotl2 = max(float(np.dot(n, light_dir2)), 0.0)
                hemi = 0.52 + 0.14 * float(n[1])
                shade = hemi + 0.42 * ndotl1 + 0.18 * ndotl2

                lit_rgb = np.clip(color * shade + emissive * 0.55, 0.0, 1.0)
                edge_rgb = np.clip(lit_rgb * 0.72, 0.0, 1.0)

                # Convert glTF (X, Y-up, Z) -> Matplotlib 3D (X, -Z, Y-up)
                tri_mpl = np.array([
                    [p0[0], -p0[2], p0[1]],
                    [p1[0], -p1[2], p1[1]],
                    [p2[0], -p2[2], p2[1]],
                ], dtype=np.float32)
                tris_xyz.append(tri_mpl)
                tris_rgb.append(lit_rgb)
                tris_edge.append(edge_rgb)

    pts_stack = np.vstack(all_pts)
    min_pt = pts_stack.min(axis=0)
    max_pt = pts_stack.max(axis=0)
    return tris_xyz, tris_rgb, tris_edge, min_pt, max_pt, len(pts_stack), len(tris_xyz)


def render_sheet():
    models = [
        ("room_shell.glb", "1. Room Shell (Cutaway View)", "North Viewport + Wallpaper + Hull Ribs", True),
        ("bunk_bed.glb", "2. Habitat Bunk Pod", "Built-in Sleep Alcove + Reading Light", False),
        ("retro_desk_crt.glb", "3. Cantilever Desk & CRT", "Phosphor Telemetry + Tape Deck", False),
        ("wardrobe_locker.glb", "4. Crew Wardrobe Locker", "Louvers + Ochre Stripe + Boot Drawer", False),
        ("lounge_chair.glb", "5. 70s Modular Lounge Chair", "Bent-Walnut Shell + Terracotta Cushions", False),
        ("coffee_table.glb", "6. Smoked-Amber Coffee Table", "Walnut Shelf + Brass Tray & Carafe", False),
        ("floor_lamp.glb", "7. Space-Age Mushroom Lamp", "Brushed Brass Stem + Glowing Dome", False),
        ("area_rug.glb", "8. Woven Geometric Area Rug", "Low-Profile Beveled + Retro Motif", False),
        ("hydro_planter.glb", "9. Hydroponic Planter Unit", "Grow-Light Gantry + Monstera Foliage", False),
    ]

    fig = plt.figure(figsize=(20, 15.5), dpi=140, facecolor="#161412")
    fig.suptitle(
        "PROJECT CYLINDER HAB-7 — 3D GLB ASSET & PBR TEXTURE SHEET (GODOT 4 PIPELINE)",
        color="#F5ECD6",
        fontsize=18,
        fontweight="bold",
        y=0.975,
    )
    fig.text(
        0.5,
        0.950,
        "Owner: Rook (3D Modeling Specialist)  |  Scale: 1 unit = 1.0m  |  Pivots: Bottom-Center (Y = 0.000m)  |  Format: Binary glTF 2.0 (.glb)",
        color="#D89E36",
        fontsize=11.5,
        ha="center",
    )

    # Top 3x3 grid for the 9 3D models (occupying y from 0.24 to 0.93)
    gs_models = fig.add_gridspec(
        3, 3, left=0.03, right=0.97, bottom=0.23, top=0.92, wspace=0.10, hspace=0.18
    )

    for idx, (fname, title, subtitle, is_cutaway) in enumerate(models):
        r, c = divmod(idx, 3)
        ax = fig.add_subplot(gs_models[r, c], projection="3d", facecolor="#211D1A")
        glb_path = os.path.join(GLB_DIR, fname)
        tris_xyz, tris_rgb, tris_edge, min_pt, max_pt, n_verts, n_tris = extract_glb_colored_triangles(
            glb_path, cutaway_room=is_cutaway
        )

        poly = Poly3DCollection(
            tris_xyz,
            facecolors=tris_rgb,
            edgecolors=tris_edge,
            linewidths=0.35,
            antialiased=True,
        )
        ax.add_collection3d(poly)

        dims = max_pt - min_pt  # glTF (X, Y-height, Z-depth)
        mpl_pts = np.vstack(tris_xyz)
        mn = mpl_pts.min(axis=0)
        mx = mpl_pts.max(axis=0)
        ctr = 0.5 * (mn + mx)
        span = max(float((mx - mn).max()) * 0.56, 0.35)

        ax.set_xlim(ctr[0] - span, ctr[0] + span)
        ax.set_ylim(ctr[1] - span, ctr[1] + span)
        ax.set_zlim(ctr[2] - span * 0.85, ctr[2] + span * 0.85)
        ax.set_box_aspect((1.0, 1.0, 0.85))

        if fname == "area_rug.glb":
            ax.view_init(elev=38, azim=-55)
        elif fname == "room_shell.glb":
            ax.view_init(elev=24, azim=-48)
        else:
            ax.view_init(elev=24, azim=-52)

        ax.set_axis_off()
        ax.set_title(
            f"{title}\n{fname}  ({dims[0]:.2f}m W × {dims[2]:.2f}m D × {dims[1]:.2f}m H | {n_tris} tris)",
            color="#F5ECD6",
            fontsize=10.0,
            fontweight="bold",
            pad=2,
        )

    # Bottom row: 8 seamless texture swatches (occupying y from 0.03 to 0.18)
    tex_files = [
        ("wallpaper_retro_geometric.png", "Retro Wallpaper"),
        ("bulkhead_wainscoting.png", "Bulkhead Wainscot"),
        ("wood_parquet_warm.png", "Teak Parquet Deck"),
        ("crt_screen_telemetry.png", "CRT Telemetry UI"),
        ("rug_retro_woven.png", "Woven Area Rug"),
        ("fabric_terracotta_cushion.png", "Terracotta Boucle"),
        ("metal_brushed_brass.png", "Brushed Brass Trim"),
        ("oneill_exterior_vista.png", "O'Neill Cylinder Vista"),
    ]
    gs_tex = fig.add_gridspec(1, 8, left=0.04, right=0.96, bottom=0.035, top=0.175, wspace=0.18)
    for t_i, (tfname, tlabel) in enumerate(tex_files):
        tax = fig.add_subplot(gs_tex[0, t_i])
        tpath = os.path.join(TEX_DIR, tfname)
        if os.path.exists(tpath):
            im = Image.open(tpath)
            tax.imshow(im)
        tax.set_xticks([])
        tax.set_yticks([])
        for spine in tax.spines.values():
            spine.set_edgecolor("#D89E36")
            spine.set_linewidth(1.5)
        tax.set_title(f"{tlabel}\n({tfname})", color="#E8DEC8", fontsize=8.0, pad=4)

    out_path = os.path.join(RENDER_DIR, "asset_sheet.png")
    fig.savefig(out_path, dpi=140, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"[render] Saved high-resolution preview sheet: {out_path} ({os.path.getsize(out_path) // 1024} KB)")


if __name__ == "__main__":
    render_sheet()
