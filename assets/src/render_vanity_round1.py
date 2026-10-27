#!/usr/bin/env python3
"""
High-Craft Hard Sci-Fi Translucent Renderer & 5-Panel Voting Sheet Composer for
Fixture #2: Compact Hygiene & Sonic Wash Vanity — Round 1 (vanity_r1_01.glb .. vanity_r1_05.glb).

Follows Section 4 of /workspace/game-project/design/vanity_round1/vanity_r1_spec.md:
- Target Look-At Point: (0.0, 1.02, 0.0)
- Camera Angles: 3/4 front-isometric beauty angle (yaw = ±18° to ±20°, pitch = -12°, distance ~ 2.55m, FOV = 46°)
- Pass 1 (Opaque): Renders vanity hull, concave zero-splash washbasin, sonic-mist faucet arch, backlit smart-mirror HUD,
  interior 3D folded/rolled orbital-navy towels, sonic grooming wands, and lower greywater filter canisters/pipes/orange valve.
- Pass 2 (Sorted alphaMode == "BLEND"): Composites the translucent UV-violet sterilizer doors and cyan sonic-shield
  inspection windows (alpha ~ 0.16-0.19) with crisp glass specular reflection and Fresnel edge glow.
- Pass 3 (Emissive Bloom): Soft atmospheric bloom around Ice-White, Cyan, UV-Violet, and Amber LEDs.
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
from render_bunk_round1 import load_font
from render_locker_round1 import render_locker_candidate

GLB_VANITY_DIR = "/workspace/game-project/assets/glb/vanity_round1"
OUT_RENDER_DIR = "/workspace/game-project/assets/renders/vanity_round1"
GODOT_RENDER_DIR = "/workspace/game-project/godot/renders/vanity_round1"

os.makedirs(OUT_RENDER_DIR, exist_ok=True)
os.makedirs(GODOT_RENDER_DIR, exist_ok=True)

CANDIDATE_VANITY_META = [
    (
        "vanity_r1_01",
        "01",
        "01_recessed_octagonal_vanity",
        "RECESSED OCTAGONAL BULKHEAD SONIC VANITY",
        "45° Chamfered Octagonal Housing + Right UV Cubby & Lower H2O Bay",
        "Concave white basin & sonic-mist arch • Beveled smart-mirror HUD • Right UV-violet towel/wand cubby • Lower H2O filter bay",
        (19.0, -12.0),
        ((0.0, 1.45, 0.25), (0.75, 0.96, 1.0), 1.45),
        ((0.18, 0.65, 0.25), (0.68, 0.56, 1.0), 1.25),
        (0.0, 0.90, 1.0),
    ),
    (
        "vanity_r1_02",
        "02",
        "02_cantilevered_halo_vanity",
        "CANTILEVERED POD BASIN & FLOATING HALO MIRROR",
        "Floating Stadium Washbasin Pod + 360° Halo Mirror & Overhead UV Locker",
        "Cantilevered white basin pod • 360° backlit Halo smart mirror • Overhead UV towel locker • Exposed steel syphons & filter",
        (-19.0, -12.0),
        ((0.0, 1.35, 0.24), (0.82, 0.96, 1.0), 1.50),
        ((0.0, 0.55, 0.24), (0.35, 0.90, 1.0), 1.20),
        (0.0, 0.90, 1.0),
    ),
    (
        "vanity_r1_03",
        "03",
        "03_dual_zone_split_station",
        "DUAL-ZONE SPLIT GROOMING & UV DECON STATION",
        "65/35 Asymmetric Split Wash Alcove + Full-Height UV Towel Tower",
        "Direct companion to Locker #02 • Left sonic washbasin & halo faucet • Right 3-tier UV-violet towel & grooming tower",
        (19.0, -12.0),
        ((-0.16, 1.38, 0.25), (0.70, 0.95, 1.0), 1.45),
        ((0.32, 1.05, 0.26), (0.68, 0.56, 1.0), 1.35),
        (0.0, 0.90, 1.0),
    ),
    (
        "vanity_r1_04",
        "04",
        "04_cylindrical_sonic_alcove",
        "CYLINDRICAL SONIC-MIST ALCOVE & PRIVACY VANITY",
        "Semi-Cylindrical Capsule with Hemispherical Steel Basin & Parted Shields",
        "Hemispherical brushed-steel basin • Parted curved translucent splash shields • Panoramic smart mirror • Lower UV filter bay",
        (-19.0, -12.0),
        ((0.0, 1.42, 0.26), (0.65, 0.95, 1.0), 1.48),
        ((0.0, 0.50, 0.26), (0.68, 0.56, 1.0), 1.25),
        (0.0, 0.90, 1.0),
    ),
    (
        "vanity_r1_05",
        "05",
        "05_corner_chamfered_vanity",
        "CORNER-CHAMFERED CREW WASH & MED-DISPENSER",
        "45° Wedge Station with Twin 35° Canted UV & Med-Dispenser Wings",
        "Central trapezoidal basin & smart mirror • Left 35° UV grooming wing • Right 35° towel & orange med-dispenser wing",
        (19.0, -12.0),
        ((0.0, 1.38, 0.26), (0.75, 0.96, 1.0), 1.45),
        ((0.0, 0.52, 0.26), (1.0, 0.72, 0.25), 1.25),
        (0.0, 0.90, 1.0),
    ),
]


def render_all_vanities_and_voting_sheet():
    manifest_path = os.path.join(GLB_VANITY_DIR, "vanity_r1_manifest.json")
    with open(manifest_path, "r") as f:
        manifest_data = json.load(f)

    stats_by_id = {os.path.splitext(os.path.basename(item["filepath"]))[0]: item for item in manifest_data}

    font_badge = load_font(28, bold=True)
    font_title = load_font(24, bold=True)
    font_sub = load_font(17, bold=False)
    font_stats = load_font(18, bold=True)
    font_callouts = load_font(16, bold=False)

    for cid, num_str, slug, short_title, subtitle, callouts, (yaw, pitch), l1_cfg, l2_cfg, accent_rgb in CANDIDATE_VANITY_META:
        glb_path = os.path.join(GLB_VANITY_DIR, f"{cid}.glb")
        raw_img = render_locker_candidate(
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
        dims = st.get("dimensions", [0.95, 2.05, 0.56])

        overlay = raw_img.copy()
        draw = ImageDraw.Draw(overlay)

        draw.rounded_rectangle([24, 22, 960, 108], radius=10, fill=(14, 19, 26), outline=(0, 195, 235), width=2)
        draw.rounded_rectangle([38, 34, 114, 96], radius=8, fill=(0, 185, 225), outline=(185, 245, 255), width=2)
        draw.text((48, 48), f"#{num_str}", fill=(10, 14, 20), font=font_badge)

        draw.text((132, 34), f"#{num_str} — {short_title}", fill=(236, 244, 252), font=font_title)
        draw.text((132, 68), f"{subtitle}  ({slug})", fill=(110, 210, 240), font=font_sub)

        spec_text = f"{n_tris:,} Tris  |  {n_verts:,} Verts  |  {dims[0]:.2f}m W × {dims[2]:.2f}m D × {dims[1]:.2f}m H"
        draw.rounded_rectangle([w - 620, 22, w - 24, 76], radius=8, fill=(14, 19, 26), outline=(64, 96, 128), width=2)
        draw.text((w - 600, 38), spec_text, fill=(186, 224, 248), font=font_stats)

        draw.rounded_rectangle([24, h - 68, w - 24, h - 18], radius=8, fill=(14, 19, 26), outline=(56, 82, 108), width=2)
        draw.text((44, h - 53), f"SONIC VANITY SPEC:  {callouts}", fill=(220, 232, 244), font=font_callouts)

        out_path = os.path.join(OUT_RENDER_DIR, f"{cid}.png")
        overlay.save(out_path, "PNG", optimize=True)
        print(f"[render_vanity] Saved beauty shot: {out_path} ({w}x{h}, {n_tris} tris)")

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
    font_c_title = load_font(16, bold=True)
    font_c_meta = load_font(14, bold=True)
    font_c_desc = load_font(13, bold=False)

    draw.rectangle([0, 0, canvas_w, header_h], fill=(18, 24, 33))
    draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(0, 195, 235), width=3)
    draw.text(
        (pad, 20),
        "CYLINDER HAB-7 — FIXTURE #2: COMPACT HYGIENE & SONIC WASH VANITY (5-CHOICE TEST)",
        fill=(238, 246, 255),
        font=font_h_title,
    )
    draw.text(
        (pad, 68),
        "Zero-Splash Sonic Basin • Smart-Mirror HUD • Translucent UV-C Towel Cubby & Greywater Reclamation Manifold • Vote 01 – 05",
        fill=(110, 214, 245),
        font=font_h_sub,
    )

    for idx, (cid, num_str, slug, short_title, subtitle, callouts, _, _, _, _) in enumerate(CANDIDATE_VANITY_META):
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
        dims = st.get("dimensions", [0.95, 2.05, 0.56])

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
        os.path.join(OUT_RENDER_DIR, "vanity_round1_voting_sheet.png"),
        os.path.join(GODOT_RENDER_DIR, "vanity_round1_voting_sheet.png"),
    ]:
        sheet.save(out_p, "PNG", optimize=True)
        print(f"[render_vanity] Saved 5-panel voting sheet: {out_p} ({canvas_w}x{canvas_h})")


if __name__ == "__main__":
    render_all_vanities_and_voting_sheet()
