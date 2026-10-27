#!/usr/bin/env python3
"""
High-Craft Hard Sci-Fi Translucent Containment Renderer & 5-Panel Voting Sheet Composer for
Room 09 Hero Asset: Fusion/Spin-Drive Plasma Relay & Cryo-Coolant Containment Manifold
(reactor_core_r1_01.glb .. reactor_core_r1_05.glb).

Follows Section 4 of /workspace/game-project/design/engineering_round1/reactor_core_r1_spec.md:
- Target Look-At Point: (0.0, 1.30, 0.0)
- Camera Angles: Heroic 3/4 front-isometric beauty angle (yaw = ±18° to ±20°, pitch = -11°, distance ~ 3.28m, FOV = 46°)
- Renders 3D magnetic-pinch plasma core spindle, 5 superconducting toroidal coils, D-He3 moderator rods,
  and cryo-coolant pipes behind alphaMode: "BLEND" borosilicate radiation shields (glass_reactor_shield_translucent.png)
- Exports reactor_core_r1_01.png .. 05.png + engineering_round1_voting_sheet.png (and reactor_core_round1_voting_sheet.png)
  to /workspace/game-project/assets/renders/engineering_round1/ (and /workspace/game-project/godot/renders/engineering_round1/
  only if Gage hasn't rendered there yet).
"""
import os
import sys
import json
import shutil
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_bunk_round1 import load_font
from render_corridor_door_round1 import render_corridor_candidate

GLB_ENG_DIR = "/workspace/game-project/assets/glb/engineering_round1"
TEX_ENG_DIR = "/workspace/game-project/assets/textures/engineering_round1"
OUT_RENDER_DIR = "/workspace/game-project/assets/renders/engineering_round1"
GODOT_RENDER_DIR = "/workspace/game-project/godot/renders/engineering_round1"

os.makedirs(OUT_RENDER_DIR, exist_ok=True)
os.makedirs(GODOT_RENDER_DIR, exist_ok=True)

CANDIDATE_ENG_META = [
    (
        "reactor_core_r1_01",
        "01",
        "01_aegis7_octagonal_plasma_pinch_column",
        "AEGIS-7 OCTAGONAL PLASMA PINCH COLUMN",
        "Symmetrical Octagonal Containment Vessel + 5 Superconducting Toroidal Coils",
        "3D cyan/amber plasma spindle • 5 stacked toroidal field coils • Translucent radiation shield • 4.85 GW OLED",
        (18.0, -11.0),
        ((-0.20, 1.35, 0.45), (0.0, 0.92, 1.0), 1.75),
        ((0.85, 1.45, 0.48), (1.0, 0.65, 0.15), 1.40),
        (0.0, 0.90, 1.0),
    ),
    (
        "reactor_core_r1_02",
        "02",
        "02_dual_zone_split_plasma_cryo_bay",
        "DUAL-ZONE SPLIT PLASMA & CRYO CONTROL BAY",
        "65/35 Asymmetric Split Containment Column + D-He3 Moderator & 18.2 K Dewar Bay",
        "Sibling to Locked Winners • Left translucent plasma core & 5 coils • Right D-He3 rods, OLED, SCRAM & cryo wheel",
        (-19.0, -11.0),
        ((-0.42, 1.35, 0.45), (0.0, 0.92, 1.0), 1.75),
        ((0.82, 1.55, 0.48), (0.65, 0.48, 1.0), 1.45),
        (0.0, 0.90, 1.0),
    ),
    (
        "reactor_core_r1_03",
        "03",
        "03_spherical_tokamak_cryo_gantry",
        "SPHERICAL TOKAMAK CAGE & TWIN CRYO GANTRY",
        "Intersecting Meridian Field Ribs + Vertical Liquid-Helium Dewar Cylinders",
        "Spherical/octagonal tokamak cage • 3D plasma spindle & toroidal rings • Side D-He3 rod bay & OLED terminal",
        (19.0, -11.0),
        ((-0.18, 1.35, 0.45), (0.0, 0.92, 1.0), 1.70),
        ((0.85, 1.40, 0.48), (1.0, 0.65, 0.18), 1.40),
        (0.0, 0.90, 1.0),
    ),
    (
        "reactor_core_r1_04",
        "04",
        "04_twin_core_spindrive_conduit_arch",
        "TWIN-CORE SPIN-DRIVE & PLASMA CONDUIT ARCH",
        "Dual Vertical Translucent Plasma Relay Columns + Overhead Machined Bus Arch",
        "Twin glowing cyan plasma columns • Overhead steel plasma bus arch • D-He3 moderator hatch & SCRAM pillar",
        (-18.0, -11.0),
        ((-0.30, 1.35, 0.45), (0.0, 0.92, 1.0), 1.75),
        ((0.84, 1.45, 0.48), (1.0, 0.65, 0.18), 1.40),
        (0.0, 0.90, 1.0),
    ),
    (
        "reactor_core_r1_05",
        "05",
        "05_axial_spintorque_subcooler_manifold",
        "HEAVY AXIAL SPIN-TORQUE & SUB-COOLER MANIFOLD",
        "Industrial Spin-Gravity Torque Relay + Electromagnetic Stator Rings & Cryo Bank",
        "Translucent rotor drum shield • Glowing cyan stator rings & amber pulse • D-He3 fuel rods & 4-spoke handwheel",
        (18.0, -11.0),
        ((-0.20, 1.35, 0.45), (0.0, 0.92, 1.0), 1.75),
        ((0.86, 1.45, 0.48), (0.65, 0.48, 1.0), 1.45),
        (0.0, 0.90, 1.0),
    ),
]


def render_all_engineering_and_voting_sheet():
    manifest_path = os.path.join(GLB_ENG_DIR, "engineering_r1_manifest.json")
    with open(manifest_path, "r") as f:
        manifest_data = json.load(f)

    stats_by_id = {os.path.splitext(os.path.basename(item["filepath"]))[0]: item for item in manifest_data}
    vista_path = os.path.join(TEX_ENG_DIR, "vista_deep_space.png")

    font_badge = load_font(28, bold=True)
    font_title = load_font(24, bold=True)
    font_sub = load_font(17, bold=False)
    font_stats = load_font(18, bold=True)
    font_callouts = load_font(16, bold=False)

    godot_already_rendered = os.path.exists(os.path.join(GODOT_RENDER_DIR, "engineering_round1_voting_sheet.png"))

    for cid, num_str, slug, short_title, subtitle, callouts, (yaw, pitch), l1_cfg, l2_cfg, accent_rgb in CANDIDATE_ENG_META:
        glb_path = os.path.join(GLB_ENG_DIR, f"{cid}.glb")
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

        godot_png = os.path.join(GODOT_RENDER_DIR, f"{cid}.png")
        if not godot_already_rendered and not os.path.exists(godot_png):
            raw_img.save(godot_png, "PNG", optimize=True)

        w, h = raw_img.size
        st = stats_by_id.get(cid, {})
        n_tris = st.get("triangles", 0)
        n_verts = st.get("vertices", 0)
        dims = st.get("dimensions", [2.60, 2.65, 1.50])

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
        draw.text((44, h - 53), f"REACTOR CORE SPEC:  {callouts}", fill=(220, 232, 244), font=font_callouts)

        out_path = os.path.join(OUT_RENDER_DIR, f"{cid}.png")
        overlay.save(out_path, "PNG", optimize=True)
        print(f"[render_eng] Saved beauty shot: {out_path} ({w}x{h}, {n_tris} tris)")

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
        "CYLINDER HAB-7 — ROOM 09 HERO ASSET: FUSION/SPIN-DRIVE PLASMA RELAY & CRYO MANIFOLD (5-CHOICE TEST)",
        fill=(238, 246, 255),
        font=font_h_title,
    )
    draw.text(
        (pad, 68),
        "Translucent Radiation Shield • 3D Magnetic-Pinch Plasma Core & Toroidal Coils • D-He3 Moderator Rods & 4.85 GW OLED • Vote 01 – 05",
        fill=(110, 214, 245),
        font=font_h_sub,
    )

    for idx, (cid, num_str, slug, short_title, subtitle, callouts, _, _, _, _) in enumerate(CANDIDATE_ENG_META):
        x0 = pad + idx * (cell_w + pad)
        y0 = header_h + pad

        draw.rounded_rectangle(
            [x0 - 2, y0 - 2, x0 + cell_w + 2, y0 + cell_h + 2],
            radius=10,
            fill=(22, 28, 38),
            outline=(58, 88, 118),
            width=2,
        )

        src_png = os.path.join(OUT_RENDER_DIR, f"{cid}.png")
        if os.path.exists(src_png):
            im = Image.open(src_png).convert("RGB")
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
        dims = st.get("dimensions", [2.60, 2.65, 1.50])

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

    sheet_names = ["engineering_round1_voting_sheet.png", "reactor_core_round1_voting_sheet.png"]
    for sname in sheet_names:
        out_p = os.path.join(OUT_RENDER_DIR, sname)
        sheet.save(out_p, "PNG", optimize=True)
        print(f"[render_eng] Saved 5-panel voting sheet: {out_p} ({canvas_w}x{canvas_h})")
        godot_s = os.path.join(GODOT_RENDER_DIR, sname)
        if not godot_already_rendered and not os.path.exists(godot_s):
            shutil.copyfile(out_p, godot_s)


if __name__ == "__main__":
    render_all_engineering_and_voting_sheet()
