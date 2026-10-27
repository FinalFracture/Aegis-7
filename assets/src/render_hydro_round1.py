#!/usr/bin/env python3
"""
High-Craft Hard Sci-Fi Translucent Borosilicate Renderer & 5-Panel Voting Sheet Composer for
Room 06 Hero Asset: Vertical Translucent Aeroponic Planter & Bio-Air Scrubber Tower
(hydro_column_r1_01.glb .. hydro_column_r1_05.glb).

Follows Section 4 of /workspace/game-project/design/hydro_round1/hydro_column_r1_spec.md:
- Target Look-At Point: (0.0, 1.22, 0.0)
- Camera Angles: Heroic 3/4 front-isometric beauty angle (yaw = ±18° to ±20°, pitch = -11°, distance ~ 3.05m, FOV = 46°)
- Pass 1 (Opaque): Renders gunmetal sump & scrubber crown, 4 stacked rotary planter rings, 3D sculpted emerald/jade
  botanical foliage clusters, central misting spindle, Chlorella algae cyan bioreactor cores, nutrient tanks,
  signal-orange dosing valves, and photosynthetic OLED telemetry console.
- Pass 2 (Sorted alphaMode == "BLEND"): Composites the translucent borosilicate growth column & bioreactor tubes
  (glass_hydro_cylinder_translucent.png, alpha ~ 0.19) with crisp specular reflection and cyan Fresnel edge glow.
- Pass 3 (Emissive Bloom): Soft bloom around UV-Violet (#7B5CFF), Daylight Ice-White (#E0F4FF), and Cyan (#00E5FF) grow lights.
"""
import os
import sys
import json
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_bunk_round1 import load_font
from render_climate_round1 import render_climate_candidate

GLB_HYDRO_DIR = "/workspace/game-project/assets/glb/hydro_round1"
OUT_RENDER_DIR = "/workspace/game-project/assets/renders/hydro_round1"
GODOT_RENDER_DIR = "/workspace/game-project/godot/renders/hydro_round1"

os.makedirs(OUT_RENDER_DIR, exist_ok=True)
os.makedirs(GODOT_RENDER_DIR, exist_ok=True)

CANDIDATE_HYDRO_META = [
    (
        "hydro_column_r1_01",
        "01",
        "01_octagonal_aeroponic_biotower",
        "AEGIS-7 OCTAGONAL TRANSLUCENT AEROPONIC BIO-TOWER",
        "4 Stacked Rotary Planter Rings + UV/Daylight Grow Halos & Nutrient Manifold",
        "Translucent borosilicate column • 4 rotary trays of 3D emerald foliage • UV-violet & ice grow halos • OLED console",
        (19.0, -11.0),
        ((-0.20, 1.45, 0.35), (0.78, 0.88, 1.0), 1.55),
        ((0.66, 1.55, 0.38), (0.0, 0.92, 1.0), 1.45),
        (0.0, 0.90, 1.0),
    ),
    (
        "hydro_column_r1_02",
        "02",
        "02_dual_zone_split_aeroponic_bioscrubber",
        "DUAL-ZONE SPLIT AEROPONIC & O2 ALGAE BIO-SCRUBBER",
        "65/35 Asymmetric Split Rotary Planter Column + Chlorella Algae Bioreactor Bay",
        "Sibling to Locked Winners • Left 4-tier rotary aeroponic column • Right twin cyan algae bioreactors, OLED & dosing wheel",
        (19.0, -11.0),
        ((-0.32, 1.45, 0.35), (0.78, 0.88, 1.0), 1.55),
        ((0.62, 1.65, 0.38), (0.0, 0.92, 1.0), 1.50),
        (0.0, 0.90, 1.0),
    ),
    (
        "hydro_column_r1_03",
        "03",
        "03_twin_helix_carousel",
        "TWIN-HELIX VERTICAL BIOREACTOR & GREENS CAROUSEL",
        "Dual Side-by-Side Translucent Aeroponic Cylinders + Center OLED Control Pillar",
        "Twin translucent aeroponic carousels • Central photosynthetic OLED pillar • UV-violet & daylight grow rings",
        (-19.0, -11.0),
        ((-0.52, 1.45, 0.35), (0.78, 0.88, 1.0), 1.50),
        ((0.52, 1.45, 0.35), (0.68, 0.56, 1.0), 1.50),
        (0.0, 0.90, 1.0),
    ),
    (
        "hydro_column_r1_04",
        "04",
        "04_hex_terraced_terrarium",
        "HEX-FACETED TERRACED TERRARIUM & UV MIST GANTRY",
        "Hexagonal-Beveled Botanical Bay + Translucent Doors & Algae Scrubber",
        "Hexagonal chamfered botanical frame • 4 terraced foliage rings • UV misting halos & right bioreactor manifold",
        (19.0, -11.0),
        ((-0.24, 1.45, 0.35), (0.78, 0.88, 1.0), 1.55),
        ((0.72, 1.55, 0.38), (0.0, 0.92, 1.0), 1.45),
        (0.0, 0.90, 1.0),
    ),
    (
        "hydro_column_r1_05",
        "05",
        "05_centrifugal_drum_revitalizer",
        "ZERO-G CENTRIFUGAL DRUM PLANTER & REVITALIZER",
        "Rotary Drum Planter with Axial UV Grow Lamp + Twin CO2 Scrubber Sump",
        "Centrifugal rotary planter rings • Axial UV-violet & daylight grow halos • Twin algae bioreactors & OLED console",
        (-19.0, -11.0),
        ((-0.22, 1.45, 0.35), (0.78, 0.88, 1.0), 1.55),
        ((0.70, 1.55, 0.38), (0.0, 0.92, 1.0), 1.45),
        (0.0, 0.90, 1.0),
    ),
]


def render_all_hydro_and_voting_sheet():
    manifest_path = os.path.join(GLB_HYDRO_DIR, "hydro_r1_manifest.json")
    with open(manifest_path, "r") as f:
        manifest_data = json.load(f)

    stats_by_id = {os.path.splitext(os.path.basename(item["filepath"]))[0]: item for item in manifest_data}

    font_badge = load_font(28, bold=True)
    font_title = load_font(24, bold=True)
    font_sub = load_font(17, bold=False)
    font_stats = load_font(18, bold=True)
    font_callouts = load_font(16, bold=False)

    raw_images = {}
    for cid, num_str, slug, short_title, subtitle, callouts, (yaw, pitch), l1_cfg, l2_cfg, accent_rgb in CANDIDATE_HYDRO_META:
        glb_path = os.path.join(GLB_HYDRO_DIR, f"{cid}.glb")
        raw_img = render_climate_candidate(
            glb_path,
            width=1920,
            height=1080,
            cam_yaw_deg=yaw,
            cam_pitch_deg=pitch,
            light1_cfg=l1_cfg,
            light2_cfg=l2_cfg,
            accent_rgb=accent_rgb,
        )
        raw_images[cid] = raw_img

        raw_out_path = os.path.join(GODOT_RENDER_DIR, f"{cid}.png")
        if not os.path.exists(raw_out_path):
            raw_img.save(raw_out_path, "PNG", optimize=True)

        w, h = raw_img.size
        st = stats_by_id.get(cid, {})
        n_tris = st.get("triangles", 0)
        n_verts = st.get("vertices", 0)
        dims = st.get("dimensions", [1.98, 2.45, 0.92])

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
        draw.text((44, h - 53), f"AEROPONIC TOWER SPEC:  {callouts}", fill=(220, 232, 244), font=font_callouts)

        out_path = os.path.join(OUT_RENDER_DIR, f"{cid}.png")
        overlay.save(out_path, "PNG", optimize=True)
        print(f"[render_hydro] Saved beauty shot: {out_path} ({w}x{h}, {n_tris} tris)")

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
        "CYLINDER HAB-7 — ROOM 06 HERO: AEROPONIC PLANTER & BIO-SCRUBBER TOWER (5-CHOICE TEST)",
        fill=(238, 246, 255),
        font=font_h_title,
    )
    draw.text(
        (pad, 68),
        "Translucent Borosilicate Growth Column • 3D Emerald Foliage Tiers • UV-Violet/Daylight Grow Halos & Algae O2 Bioreactors • Vote 01 – 05",
        fill=(110, 214, 245),
        font=font_h_sub,
    )

    for idx, (cid, num_str, slug, short_title, subtitle, callouts, _, _, _, _) in enumerate(CANDIDATE_HYDRO_META):
        x0 = pad + idx * (cell_w + pad)
        y0 = header_h + pad

        draw.rounded_rectangle([x0 - 2, y0 - 2, x0 + cell_w + 2, y0 + cell_h + 2], radius=10, fill=(22, 28, 38), outline=(58, 88, 118), width=2)

        im = raw_images[cid]
        iw, ih = im.size
        crop_w = 1330
        left = (iw - crop_w) // 2
        im_cropped = im.crop((left, 0, left + crop_w, ih)).resize((cell_w, cell_img_h), Image.Resampling.LANCZOS)
        sheet.paste(im_cropped, (x0, y0))

        bx0, by0 = x0 + 12, y0 + 12
        draw.rounded_rectangle([bx0, by0, bx0 + 62, by0 + 44], radius=8, fill=(0, 185, 225), outline=(195, 248, 255), width=2)
        draw.text((bx0 + 13, by0 + 8), num_str, fill=(10, 14, 20), font=font_c_badge)

        st = stats_by_id.get(cid, {})
        n_tris = st.get("triangles", 0)
        dims = st.get("dimensions", [1.98, 2.45, 0.92])

        tb_w = 132
        draw.rounded_rectangle([x0 + cell_w - tb_w - 12, y0 + 12, x0 + cell_w - 12, y0 + 42], radius=6, fill=(14, 19, 26), outline=(72, 112, 148), width=1)
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

    for fname in ["hydro_round1_voting_sheet.png", "hydro_column_round1_voting_sheet.png"]:
        out_p = os.path.join(OUT_RENDER_DIR, fname)
        sheet.save(out_p, "PNG", optimize=True)
        g_p = os.path.join(GODOT_RENDER_DIR, fname)
        if not os.path.exists(g_p):
            sheet.save(g_p, "PNG", optimize=True)
    print(f"[render_hydro] Saved voting sheets in {OUT_RENDER_DIR}")


if __name__ == "__main__":
    render_all_hydro_and_voting_sheet()
