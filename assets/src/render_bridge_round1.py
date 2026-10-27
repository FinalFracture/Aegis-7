#!/usr/bin/env python3
"""
High-Craft Hard Sci-Fi Translucent Hologram Renderer & 5-Panel Voting Sheet Composer for
Room 07 Hero Asset: Central Holographic O'Neill Cylinder Wireframe Projection Table &
Tiered Spin-Gravity Command Console (bridge_console_r1_01.glb .. bridge_console_r1_05.glb).

Follows Section 4 of /workspace/game-project/design/bridge_round1/bridge_console_r1_spec.md:
- Target Look-At Point: (0.0, 1.05, 0.0)
- Camera Angles: Elevated 3/4 front-isometric beauty angle (yaw = ±20° to ±23°, pitch = -15°, distance ~ 3.15m, FOV = 46°)
- Renders in /workspace/game-project/assets/renders/bridge_round1/ and mirrors to
  /workspace/game-project/godot/renders/bridge_round1/ (only if not yet rendered there by Gage).
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

GLB_BRIDGE_DIR = "/workspace/game-project/assets/glb/bridge_round1"
TEX_BRIDGE_DIR = "/workspace/game-project/assets/textures/bridge_round1"
OUT_RENDER_DIR = "/workspace/game-project/assets/renders/bridge_round1"
GODOT_RENDER_DIR = "/workspace/game-project/godot/renders/bridge_round1"

os.makedirs(OUT_RENDER_DIR, exist_ok=True)
os.makedirs(GODOT_RENDER_DIR, exist_ok=True)

CANDIDATE_BRIDGE_META = [
    (
        "bridge_console_r1_01",
        "01",
        "01_aegis7_octagonal_holo_cylinder_table",
        "AEGIS-7 OCTAGONAL HOLOGRAPHIC CYLINDER TABLE",
        "Symmetrical Octagonal Holotable + 3D O'Neill Cylinder Hologram & Twin Helm",
        "Floating 3D translucent O'Neill Cylinder & gimbal rings • Spin-gravity OLED array • Twin orbital-navy commander chairs",
        (21.0, -15.0),
        ((-0.35, 1.32, 0.0), (0.0, 0.90, 1.0), 1.70),
        ((0.68, 1.45, -0.10), (0.48, 0.36, 1.0), 1.35),
        (0.0, 0.90, 1.0),
    ),
    (
        "bridge_console_r1_02",
        "02",
        "02_dual_zone_split_holo_flight_director",
        "DUAL-ZONE SPLIT HOLO-TABLE & FLIGHT-DIRECTOR TOWER",
        "65/35 Asymmetric Split Holographic Cylinder Table + Tiered Spin-Gravity Control Tower",
        "Sibling to Locked Winners • Left 3D O'Neill Cylinder hologram + twin chairs • Right 3-tier OLED & HUD visor + optical core bay",
        (-21.0, -15.0),
        ((-0.35, 1.32, 0.0), (0.0, 0.90, 1.0), 1.70),
        ((0.68, 1.45, -0.10), (0.48, 0.36, 1.0), 1.35),
        (0.0, 0.90, 1.0),
    ),
    (
        "bridge_console_r1_03",
        "03",
        "03_overhead_gantry_holo_projector_pit",
        "OVERHEAD GANTRY HOLO-PROJECTOR & BRIDGE PIT CONSOLE",
        "Arched Machined-Steel Overhead Projector Bridge + U-Shaped OLED Telemetry Console",
        "Overhead steel projector arch beaming onto 3D O'Neill Cylinder • Wraparound spin-telemetry OLEDs • Twin commander chairs",
        (22.0, -15.0),
        ((-0.35, 1.32, 0.0), (0.0, 0.90, 1.0), 1.70),
        ((0.68, 1.45, -0.10), (1.0, 0.60, 0.15), 1.30),
        (0.0, 0.90, 1.0),
    ),
    (
        "bridge_console_r1_04",
        "04",
        "04_gimbaled_orrery_spin_simulator",
        "GIMBALED ORRERY SPIN-SIMULATOR & TACTICAL DESK",
        "Physical Machined-Steel 3-Axis Motorized Orrery Ring Cradle + Winged OLED Stations",
        "3-axis machined-steel orrery ring cradle around translucent cylinder • Dual throttle verniers • Signal-orange spin-lock",
        (-21.0, -15.0),
        ((-0.35, 1.32, 0.0), (0.0, 0.90, 1.0), 1.70),
        ((0.68, 1.45, -0.10), (0.48, 0.36, 1.0), 1.35),
        (0.0, 0.90, 1.0),
    ),
    (
        "bridge_console_r1_05",
        "05",
        "05_elevated_captain_command_podium",
        "ELEVATED CAPTAIN'S COMMAND PODIUM & TELEMETRY WINGS",
        "Raised Command Podium + Forward O'Neill Cylinder Projection Well & HUD Wings",
        "Raised command deck with amber step strip • Floating 3D O'Neill Cylinder hologram • Angled translucent HUD combiner visor",
        (21.0, -15.0),
        ((-0.35, 1.32, 0.0), (0.0, 0.90, 1.0), 1.70),
        ((0.68, 1.45, -0.10), (1.0, 0.60, 0.15), 1.35),
        (0.0, 0.90, 1.0),
    ),
]


def render_all_bridge_consoles_and_voting_sheet():
    manifest_path = os.path.join(GLB_BRIDGE_DIR, "bridge_r1_manifest.json")
    with open(manifest_path, "r") as f:
        manifest_data = json.load(f)

    stats_by_id = {os.path.splitext(os.path.basename(item["filepath"]))[0]: item for item in manifest_data}
    vista_path = os.path.join(TEX_BRIDGE_DIR, "vista_oneill_cylinder_interior.png")

    font_badge = load_font(28, bold=True)
    font_title = load_font(24, bold=True)
    font_sub = load_font(17, bold=False)
    font_stats = load_font(18, bold=True)
    font_callouts = load_font(16, bold=False)

    for cid, num_str, slug, short_title, subtitle, callouts, (yaw, pitch), l1_cfg, l2_cfg, accent_rgb in CANDIDATE_BRIDGE_META:
        glb_path = os.path.join(GLB_BRIDGE_DIR, f"{cid}.glb")
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
        dims = st.get("dimensions", [2.50, 1.92, 1.65])

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
        draw.text((44, h - 53), f"COMMAND BRIDGE SPEC:  {callouts}", fill=(220, 232, 244), font=font_callouts)

        out_path = os.path.join(OUT_RENDER_DIR, f"{cid}.png")
        overlay.save(out_path, "PNG", optimize=True)
        print(f"[render_bridge] Saved beauty shot: {out_path} ({w}x{h}, {n_tris} tris)")

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
        "CYLINDER HAB-7 — ROOM 07 HERO ASSET: HOLOGRAPHIC COMMAND TABLE & SPIN-GRAVITY CONSOLE (5-CHOICE TEST)",
        fill=(238, 246, 255),
        font=font_h_title,
    )
    draw.text(
        (pad, 68),
        "Floating 3D Translucent O'Neill Cylinder Wireframe & Gimbal Rings • Spin-Gravity OLED Array & HUD Visor • Commander Flight Chairs • Vote 01 – 05",
        fill=(110, 214, 245),
        font=font_h_sub,
    )

    for idx, (cid, num_str, slug, short_title, subtitle, callouts, _, _, _, _) in enumerate(CANDIDATE_BRIDGE_META):
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
        dims = st.get("dimensions", [2.50, 1.92, 1.65])

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

    for s_name in ["bridge_round1_voting_sheet.png", "bridge_console_round1_voting_sheet.png"]:
        out_p = os.path.join(OUT_RENDER_DIR, s_name)
        sheet.save(out_p, "PNG", optimize=True)
        g_p = os.path.join(GODOT_RENDER_DIR, s_name)
        if not os.path.exists(g_p):
            sheet.save(g_p, "PNG", optimize=True)
        print(f"[render_bridge] Saved 5-panel voting sheet: {out_p} ({canvas_w}x{canvas_h})")


if __name__ == "__main__":
    render_all_bridge_consoles_and_voting_sheet()
