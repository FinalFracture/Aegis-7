#!/usr/bin/env python3
"""
High-Craft Hard Sci-Fi Translucent Bar Renderer & 5-Panel Voting Sheet Composer for
Room 08 Hero Asset: Ambient Zero-G Beverage Bar & Celestial Observatory Lounge Island
(lounge_bar_r1_01.glb .. lounge_bar_r1_05.glb).

Follows Section 4 of /workspace/game-project/design/lounge_round1/lounge_bar_r1_spec.md:
- Target Look-At Point: (0.0, 1.02, 0.0)
- Camera Angles: 3/4 front-isometric beauty angle (yaw = ±20° to ±23°, pitch = -13°, distance ~ 2.95m, FOV = 46°)
- Renders in /workspace/game-project/assets/renders/lounge_round1/ and mirrors to
  /workspace/game-project/godot/renders/lounge_round1/ (only if not yet rendered there by Gage).
"""
import os
import io
import sys
import json
import math
import shutil
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image, ImageDraw
import pygltflib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_bunk_round1 import load_font, make_spacecraft_bay_backdrop
from render_corridor_door_round1 import render_corridor_candidate

GLB_LOUNGE_DIR = "/workspace/game-project/assets/glb/lounge_round1"
TEX_LOUNGE_DIR = "/workspace/game-project/assets/textures/lounge_round1"
OUT_RENDER_DIR = "/workspace/game-project/assets/renders/lounge_round1"
GODOT_RENDER_DIR = "/workspace/game-project/godot/renders/lounge_round1"

os.makedirs(OUT_RENDER_DIR, exist_ok=True)
os.makedirs(GODOT_RENDER_DIR, exist_ok=True)

CANDIDATE_LOUNGE_META = [
    (
        "lounge_bar_r1_01",
        "01",
        "01_aegis7_octagonal_celestial_bar_arch",
        "AEGIS-7 OCTAGONAL CELESTIAL BAR & CARAFE ARCH",
        "Octagonal Beveled Bar Counter + Rear Translucent Infusion Carafe Vault & Barstools",
        "6 glowing cyan/violet/amber infusion carafes • Siphon tap arch & bulb-glasses • Celestial star-map OLED • 2 navy barstools",
        (21.0, -13.0),
        ((-0.35, 1.15, 0.25), (0.0, 0.90, 1.0), 1.50),
        ((0.65, 1.45, -0.05), (0.48, 0.36, 1.0), 1.45),
        (0.0, 0.90, 1.0),
    ),
    (
        "lounge_bar_r1_02",
        "02",
        "02_dual_zone_split_celestial_decanter_tower",
        "DUAL-ZONE SPLIT CELESTIAL BAR & DECANTER TOWER",
        "65/35 Asymmetric Split Beverage Counter + 3-Tier Translucent Botanical & Decanter Tower",
        "Sibling to Locked Winners • Left siphon arch, bulb-glasses & 2 barstools • Right translucent decanter tower & aeroponic herbs",
        (-21.0, -13.0),
        ((-0.35, 1.15, 0.25), (0.0, 0.90, 1.0), 1.50),
        ((0.65, 1.45, -0.05), (0.48, 0.36, 1.0), 1.45),
        (0.0, 0.90, 1.0),
    ),
    (
        "lounge_bar_r1_03",
        "03",
        "03_rotary_sphere_dispenser_stargazer_bar",
        "ROTARY ZERO-G SPHERE DISPENSER & STARGAZER BAR",
        "Curved Stargazer Bar Counter + Translucent Magnetic Levitation Drink Column",
        "Translucent zero-G beverage levitation column • Triple-nozzle siphon tap arch • Star-map OLED & twin cantilevered barstools",
        (22.0, -13.0),
        ((-0.35, 1.15, 0.25), (0.0, 0.90, 1.0), 1.50),
        ((0.65, 1.45, -0.05), (0.48, 0.36, 1.0), 1.45),
        (0.0, 0.90, 1.0),
    ),
    (
        "lounge_bar_r1_04",
        "04",
        "04_cantilevered_canopy_botanical_island",
        "CANTILEVERED CANOPY LOUNGE ISLAND & MIXOLOGY BAY",
        "Overhead Translucent Acoustic/Light Canopy + Botanical Herb & Decanter Wall",
        "Overhead translucent sapphire canopy • Living aeroponic herb garnish bed • Glowing zero-G bulb-glasses & 2 navy barstools",
        (-21.0, -13.0),
        ((-0.35, 1.15, 0.25), (0.0, 0.90, 1.0), 1.50),
        ((0.65, 1.45, -0.05), (0.48, 0.36, 1.0), 1.45),
        (0.48, 0.36, 1.0),
    ),
    (
        "lounge_bar_r1_05",
        "05",
        "05_sunken_pit_cryo_chiller_station",
        "SUNKEN PIT PERIMETER BAR & CRYO-CHILLER STATION",
        "Low-Slung Viewing Pit Bar + Translucent Cryo-Chiller Drums & Celestial Console",
        "Twin translucent cryo-chiller decanters • Signal-orange nitro infusion valves • Celestial OLED & 2 orbital-navy perch stools",
        (21.0, -13.0),
        ((-0.35, 1.15, 0.25), (0.0, 0.90, 1.0), 1.50),
        ((0.65, 1.45, -0.05), (1.0, 0.60, 0.15), 1.40),
        (0.0, 0.90, 1.0),
    ),
]


def render_all_lounge_bars_and_voting_sheet():
    manifest_path = os.path.join(GLB_LOUNGE_DIR, "lounge_r1_manifest.json")
    with open(manifest_path, "r") as f:
        manifest_data = json.load(f)

    stats_by_id = {os.path.splitext(os.path.basename(item["filepath"]))[0]: item for item in manifest_data}
    vista_path = os.path.join(TEX_LOUNGE_DIR, "vista_deep_space.png")

    font_badge = load_font(28, bold=True)
    font_title = load_font(24, bold=True)
    font_sub = load_font(17, bold=False)
    font_stats = load_font(18, bold=True)
    font_callouts = load_font(16, bold=False)

    for cid, num_str, slug, short_title, subtitle, callouts, (yaw, pitch), l1_cfg, l2_cfg, accent_rgb in CANDIDATE_LOUNGE_META:
        glb_path = os.path.join(GLB_LOUNGE_DIR, f"{cid}.glb")
        raw_img = render_corridor_candidate(
            glb_path,
            vista_path,
            width=1920,
            height=1080,
            cam_yaw_deg=yaw,
            cam_pitch_deg=pitch,
            light1_cfg=l1_cfg,
            light2_cfg=l2_cfg,
            accent_rgb=accent_rgb,
        )

        godot_raw_path = os.path.join(GODOT_RENDER_DIR, f"{cid}.png")
        if not os.path.exists(godot_raw_path):
            raw_img.save(godot_raw_path, "PNG", optimize=True)

        w, h = raw_img.size
        st = stats_by_id.get(cid, {})
        n_tris = st.get("triangles", 0)
        n_verts = st.get("vertices", 0)
        dims = st.get("dimensions", [2.35, 2.05, 1.35])

        overlay = raw_img.copy()
        draw = ImageDraw.Draw(overlay)

        draw.rounded_rectangle([24, 22, 980, 108], radius=10, fill=(14, 19, 26), outline=(0, 195, 235), width=2)
        draw.rounded_rectangle([38, 34, 114, 96], radius=8, fill=(0, 185, 225), outline=(185, 245, 255), width=2)
        draw.text((48, 48), f"#{num_str}", fill=(10, 14, 20), font=font_badge)

        draw.text((132, 34), f"#{num_str} — {short_title}", fill=(236, 244, 252), font=font_title)
        draw.text((132, 68), f"{subtitle}  ({slug})", fill=(110, 210, 240), font=font_sub)

        spec_text = f"{n_tris:,} Tris  |  {n_verts:,} Verts  |  {dims[0]:.2f}m W × {dims[2]:.2f}m D × {dims[1]:.2f}m H"
        draw.rounded_rectangle([w - 620, 22, w - 24, 76], radius=8, fill=(14, 19, 26), outline=(64, 96, 128), width=2)
        draw.text((w - 600, 38), spec_text, fill=(186, 224, 248), font=font_stats)

        draw.rounded_rectangle([24, h - 68, w - 24, h - 18], radius=8, fill=(14, 19, 26), outline=(56, 82, 108), width=2)
        draw.text((44, h - 53), f"CELESTIAL LOUNGE SPEC:  {callouts}", fill=(220, 232, 244), font=font_callouts)

        out_path = os.path.join(OUT_RENDER_DIR, f"{cid}.png")
        overlay.save(out_path, "PNG", optimize=True)
        print(f"[render_lounge] Saved beauty shot: {out_path} ({w}x{h}, {n_tris} tris)")

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
        "CYLINDER HAB-7 — ROOM 08 HERO ASSET: ZERO-G BEVERAGE BAR & CELESTIAL LOUNGE ISLAND (5-CHOICE TEST)",
        fill=(238, 246, 255),
        font=font_h_title,
    )
    draw.text(
        (pad, 68),
        "Translucent Zero-G Botanical & Decanter Tower • Siphon Tap Arch & Glowing Bulb-Glasses • Celestial OLED & Orbital-Navy Barstools • Vote 01 – 05",
        fill=(110, 214, 245),
        font=font_h_sub,
    )

    for idx, (cid, num_str, slug, short_title, subtitle, callouts, _, _, _, _) in enumerate(CANDIDATE_LOUNGE_META):
        x0 = pad + idx * (cell_w + pad)
        y0 = header_h + pad

        draw.rounded_rectangle(
            [x0 - 2, y0 - 2, x0 + cell_w + 2, y0 + cell_h + 2],
            radius=10,
            fill=(22, 28, 38),
            outline=(58, 88, 118),
            width=2,
        )

        raw_path = os.path.join(OUT_RENDER_DIR, f"{cid}.png")
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
        dims = st.get("dimensions", [2.35, 2.05, 1.35])

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

    for s_name in ["lounge_round1_voting_sheet.png", "lounge_bar_round1_voting_sheet.png"]:
        out_p = os.path.join(OUT_RENDER_DIR, s_name)
        sheet.save(out_p, "PNG", optimize=True)
        g_p = os.path.join(GODOT_RENDER_DIR, s_name)
        if not os.path.exists(g_p):
            sheet.save(g_p, "PNG", optimize=True)
        print(f"[render_lounge] Saved 5-panel voting sheet: {out_p} ({canvas_w}x{canvas_h})")


if __name__ == "__main__":
    render_all_lounge_bars_and_voting_sheet()
