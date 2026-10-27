#!/usr/bin/env python3
"""
High-Craft Hard Sci-Fi Translucent Renderer & 5-Panel Voting Sheet Composer for
Room 05 Hero Asset: Heavy Cylindrical Outer-Hull Decompression Airlock & Umbilical Recharge Chamber
(eva_chamber_r1_01.glb .. eva_chamber_r1_05.glb).

Follows Section 4 of /workspace/game-project/design/eva_round1/eva_chamber_r1_spec.md:
- Target Look-At Point: (0.0, 1.25, 0.0)
- Camera Angles: Heroic 3/4 front-isometric beauty angle (yaw = ±18° to ±20°, pitch = -11°, distance ~ 3.15m, FOV = 46°)
- Pass 0: Renders vista_deep_space.png behind the rear outer-hull porthole cutout.
- Pass 1 (Opaque): Renders decompression pressure hull, mag-boot grate, 3D EVA hard-suit rig on umbilical gantry,
  3D gold-visor EVA helmet inside the UV seal-test hood, coiled umbilical hoses, O2/N2 cylinders, and OLED console.
- Pass 2 (Sorted alphaMode == "BLEND"): Composites the ajar translucent armored airlock door & UV helmet test hood.
- Pass 3 (Emissive Bloom): Soft bloom around Cyan, Amber, and UV-Violet LEDs.
"""
import os
import sys
import json
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_bunk_round1 import load_font
from render_corridor_door_round1 import render_corridor_candidate

GLB_EVA_DIR = "/workspace/game-project/assets/glb/eva_round1"
TEX_EVA_DIR = "/workspace/game-project/assets/textures/eva_round1"
OUT_RENDER_DIR = "/workspace/game-project/assets/renders/eva_round1"
GODOT_RENDER_DIR = "/workspace/game-project/godot/renders/eva_round1"

os.makedirs(OUT_RENDER_DIR, exist_ok=True)
os.makedirs(GODOT_RENDER_DIR, exist_ok=True)

CANDIDATE_EVA_META = [
    (
        "eva_chamber_r1_01",
        "01",
        "01_octagonal_ringed_decompression_lock",
        "AEGIS-7 OCTAGONAL-RINGED DECOMPRESSION LOCK",
        "3 External 45° Octagonal Collars + 32° Ajar Translucent Door & Suit Gantry",
        "3D EVA hard-suit rig on umbilical gantry • Ajar translucent door • Right UV helmet test hood & OLED console",
        (19.0, -11.0),
        ((-0.10, 1.65, 0.45), (0.35, 0.92, 1.0), 1.55),
        ((0.82, 1.55, 0.55), (0.68, 0.56, 1.0), 1.45),
        (0.0, 0.90, 1.0),
    ),
    (
        "eva_chamber_r1_02",
        "02",
        "02_dual_zone_split_decompression_gantry",
        "DUAL-ZONE SPLIT DECOMPRESSION & UMBILICAL GANTRY",
        "65/35 Asymmetric Split Decompression Cylinder + Suit-Charge & UV Helmet Tower",
        "Sibling to Locked Winners • Left chamber with 3D EVA suit & dog teeth • Right UV helmet hood, OLED & 3 umbilicals",
        (19.0, -11.0),
        ((-0.36, 1.65, 0.45), (0.35, 0.92, 1.0), 1.55),
        ((0.74, 1.55, 0.55), (0.68, 0.56, 1.0), 1.45),
        (0.0, 0.90, 1.0),
    ),
    (
        "eva_chamber_r1_03",
        "03",
        "03_rotary_carousel_decompression_pod",
        "TWIN-LOCK ROTARY CAROUSEL DECOMPRESSION POD",
        "Revolving Drum-Lock Viewport Panes + Overhead Magnetic Tether Winch",
        "Revolving translucent drum-lock doors • Overhead magnetic tether winch • 3D EVA suit rig & UV helmet hood",
        (-19.0, -11.0),
        ((-0.12, 1.65, 0.45), (0.35, 0.92, 1.0), 1.55),
        ((0.84, 1.55, 0.55), (0.68, 0.56, 1.0), 1.45),
        (0.0, 0.90, 1.0),
    ),
    (
        "eva_chamber_r1_04",
        "04",
        "04_hex_blowdown_donning_frame",
        "HEX-BULKHEAD RAPID BLOWDOWN & DONNING FRAME",
        "Elongated Hexagonal Blowdown Lock + Bi-Parting Translucent Blast Doors",
        "Hexagonal chamfered blowdown frame • Bi-parting translucent doors • Internal suit-donning gantry & umbilical booms",
        (19.0, -11.0),
        ((-0.10, 1.65, 0.45), (0.35, 0.92, 1.0), 1.55),
        ((0.84, 1.55, 0.55), (0.68, 0.56, 1.0), 1.45),
        (0.0, 0.90, 1.0),
    ),
    (
        "eva_chamber_r1_05",
        "05",
        "05_submarine_plughatch_cryo_lock",
        "SUBMARINE-STYLE PLUG-HATCH LOCK & CRYO-O2 BANK",
        "Outward-Swinging Plug Hatch with Spider Wheel + Side Cryo-O2 & Helmet Tower",
        "Outward-swinging translucent plug hatch • Signal-orange 4-spoke spider wheel • 3D EVA suit rig & cryo-O2 bank",
        (19.0, -11.0),
        ((-0.12, 1.65, 0.45), (0.35, 0.92, 1.0), 1.55),
        ((0.86, 1.55, 0.55), (1.0, 0.68, 0.20), 1.45),
        (0.0, 0.90, 1.0),
    ),
]


def render_all_eva_and_voting_sheet():
    manifest_path = os.path.join(GLB_EVA_DIR, "eva_r1_manifest.json")
    with open(manifest_path, "r") as f:
        manifest_data = json.load(f)

    stats_by_id = {os.path.splitext(os.path.basename(item["filepath"]))[0]: item for item in manifest_data}
    vista_path = os.path.join(TEX_EVA_DIR, "vista_deep_space.png")

    font_badge = load_font(28, bold=True)
    font_title = load_font(24, bold=True)
    font_sub = load_font(17, bold=False)
    font_stats = load_font(18, bold=True)
    font_callouts = load_font(16, bold=False)

    raw_images = {}
    for cid, num_str, slug, short_title, subtitle, callouts, (yaw, pitch), l1_cfg, l2_cfg, accent_rgb in CANDIDATE_EVA_META:
        glb_path = os.path.join(GLB_EVA_DIR, f"{cid}.glb")
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
        raw_images[cid] = raw_img

        # Only write to GODOT_RENDER_DIR if Gage hasn't already rendered it
        raw_out_path = os.path.join(GODOT_RENDER_DIR, f"{cid}.png")
        if not os.path.exists(raw_out_path):
            raw_img.save(raw_out_path, "PNG", optimize=True)

        w, h = raw_img.size
        st = stats_by_id.get(cid, {})
        n_tris = st.get("triangles", 0)
        n_verts = st.get("vertices", 0)
        dims = st.get("dimensions", [2.30, 2.55, 1.50])

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
        draw.text((44, h - 53), f"EVA DECOMPRESSION SPEC:  {callouts}", fill=(220, 232, 244), font=font_callouts)

        out_path = os.path.join(OUT_RENDER_DIR, f"{cid}.png")
        overlay.save(out_path, "PNG", optimize=True)
        print(f"[render_eva] Saved beauty shot: {out_path} ({w}x{h}, {n_tris} tris)")

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
        "CYLINDER HAB-7 — ROOM 05 HERO: EVA DECOMPRESSION & UMBILICAL GANTRY (5-CHOICE TEST)",
        fill=(238, 246, 255),
        font=font_h_title,
    )
    draw.text(
        (pad, 68),
        "3D EVA Hard-Suit Rig on Umbilical Gantry • Ajar Translucent Airlock Door • UV Helmet Test Hood & Blowdown OLED • Vote 01 – 05",
        fill=(110, 214, 245),
        font=font_h_sub,
    )

    for idx, (cid, num_str, slug, short_title, subtitle, callouts, _, _, _, _) in enumerate(CANDIDATE_EVA_META):
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
        dims = st.get("dimensions", [2.30, 2.55, 1.50])

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

    for fname in ["eva_round1_voting_sheet.png", "eva_chamber_round1_voting_sheet.png"]:
        out_p = os.path.join(OUT_RENDER_DIR, fname)
        sheet.save(out_p, "PNG", optimize=True)
        g_p = os.path.join(GODOT_RENDER_DIR, fname)
        if not os.path.exists(g_p):
            sheet.save(g_p, "PNG", optimize=True)
    print(f"[render_eva] Saved voting sheets in {OUT_RENDER_DIR}")


if __name__ == "__main__":
    render_all_eva_and_voting_sheet()
