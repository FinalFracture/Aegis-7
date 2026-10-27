#!/usr/bin/env python3
"""
Composes the 5-Candidate Utility Robot Round 2 (`utility_bot_round2`) Head Shape Explorations
Voting Sheet (`2728x1348`) with Picture-in-Picture (PiP) Close-Up Head Insets:
- `./godot/renders/characters/bots/utility_bot_round2_head_explorations_sheet.png`
- `./godot/renders/characters/bots/utility_bot_round2_voting_sheet.png`
- `./godot/renders/characters/johnny5/utility_bot_round2_head_explorations_sheet.png`
- `./godot/renders/characters/johnny5/utility_bot_round2_voting_sheet.png`
- `./godot/renders/characters/johnny5/johnny5_bot_round2_voting_sheet.png`
- `./godot/renders/bots/utility_bot_round2_head_explorations_sheet.png`
(and mirrored to `./assets/renders/...`).
"""
import os
import json
from PIL import Image, ImageDraw, ImageFont

OUT_DIRS = [
    "./godot/renders/characters/bots",
    "./godot/renders/characters/johnny5",
    "./godot/renders/character/bots",
    "./godot/renders/bots",
    "./godot/renders/preface",
    "./assets/renders/characters/bots",
    "./assets/renders/characters/johnny5",
    "./assets/renders/character/bots",
    "./assets/renders/bots",
    "./assets/renders/preface",
]

R2_CANDS = [
    (
        "01",
        "Articulated Split-Shutter 'Camera-Bellows' Rangefinder Hood",
        "Trapezoidal Bellows Cowling • Asymmetric 11cm Wide + 5.5cm Laser Optics • Clapperboard Horizontal Louver Shutters",
    ),
    (
        "02",
        "Curved Visor-Box with Expressive Vector Eyes & Tilting Ear-Paddles (HERO #02)",
        "68/32 Split-Bevel Monitor Visor • Deep Shadow-Box Cyan/Amber Vector Irises • Expressive Tilting Side Ear-Paddles",
    ),
    (
        "03",
        "Tri-Faceted 'Periscope Prism' Mast-Cam Turret Head",
        "Octagonal Rotary Turret • Central 13cm Cyclops Sapphire Objective + 45° Side Slit Rangefinders • Armored Sun-Visor Cap",
    ),
    (
        "04",
        "Split-Hemisphere 'Clamshell Orb' Gimbal Head",
        "Oblate Spheroid Sensor Pod in U-Yoke Gimbal • Articulated Upper/Lower Clamshell Calottes • Recessed Pill Optic Emitters",
    ),
    (
        "05",
        "Cantilevered 'Hammerhead' Wide-Baseline Stereo-Scanner Bar",
        "0.48m Wide T-Wing Stereo Bar • Continuous Center Laser Slit + Outboard Corner Optical Pods & Winglet Shutters",
    ),
]


def load_font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def get_r2_stats():
    stats = {}
    manifest_paths = [
        "./assets/glb/utility_bot_round2_manifest.json",
        "./assets/glb/preface_multifloor_and_johnny5_manifest.json",
        "./godot/assets/models/characters/bots/utility_bot_round2_manifest.json",
        "./godot/assets/models/characters/johnny5/utility_bot_round2_manifest.json",
    ]
    for mp in manifest_paths:
        if os.path.exists(mp):
            try:
                with open(mp, "r") as f:
                    data = json.load(f)
                items = (
                    data
                    if isinstance(data, list)
                    else data.get("utility_bot_round2_candidates", data.get("round2_candidates", data.get("candidates", [])))
                )
                for it in items:
                    fn = os.path.basename(it.get("filepath", ""))
                    stats[fn] = it
            except Exception:
                pass
    return stats


def compose_r2_sheet():
    src_dir = OUT_DIRS[0]
    for num_str, _, _ in R2_CANDS:
        if not os.path.exists(os.path.join(src_dir, f"char_bot_r2_{num_str}.png")):
            return False

    stats_map = get_r2_stats()
    cols, rows = 3, 2
    cell_w, cell_img_h, cell_footer_h = 880, 495, 92
    cell_h = cell_img_h + cell_footer_h
    pad, header_h = 22, 108

    canvas_w = pad + cols * (cell_w + pad)
    canvas_h = header_h + pad + rows * (cell_h + pad)

    sheet = Image.new("RGB", (canvas_w, canvas_h), (12, 15, 20))
    draw = ImageDraw.Draw(sheet)

    font_title = load_font(25, bold=True)
    font_sub = load_font(15, bold=False)
    font_badge = load_font(22, bold=True)
    font_tris = load_font(14, bold=True)
    font_inset = load_font(12, bold=True)
    font_card_title = load_font(16, bold=True)
    font_card_desc = load_font(13, bold=False)

    draw.rectangle([0, 0, canvas_w, header_h], fill=(18, 22, 30))
    draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(255, 183, 3), width=3)
    draw.text(
        (pad, 20),
        "CYLINDER HAB-7 — UTILITY ROBOT ROUND 2: 5 HEAD SHAPE EXPLORATIONS (TREADS #03 + CHASSIS #01)",
        fill=(242, 245, 250),
        font=font_title,
    )
    draw.text(
        (pad, 64),
        "Locked Base: #03 Wide-Stance Quad-Bogie Treads + #01 Compact Cube-Compactor Chassis • 5 Distinct Non-Binocular Head Explorations • Vote 01–05",
        fill=(255, 209, 102),
        font=font_sub,
    )

    for idx, (num_str, ctitle, cdesc) in enumerate(R2_CANDS):
        r, c = idx // cols, idx % cols
        if r == 1:
            row2_w = 2 * cell_w + pad
            start_x = (canvas_w - row2_w) // 2
            x0 = start_x + c * (cell_w + pad)
        else:
            x0 = pad + c * (cell_w + pad)
        y0 = header_h + pad + r * (cell_h + pad)

        is_hero = num_str == "02"
        outline_col = (255, 183, 3) if is_hero else (0, 210, 245)
        draw.rounded_rectangle(
            [x0 - 2, y0 - 2, x0 + cell_w + 2, y0 + cell_h + 2],
            radius=10,
            fill=(22, 27, 36),
            outline=outline_col,
            width=3 if is_hero else 2,
        )

        img_path = os.path.join(src_dir, f"char_bot_r2_{num_str}.png")
        im = Image.open(img_path).convert("RGB").resize((cell_w, cell_img_h), Image.Resampling.LANCZOS)
        sheet.paste(im, (x0, y0))

        # Paste Close-Up Head-Exploration Inset in Bottom-Right of the Image Panel!
        head_path = os.path.join(src_dir, f"char_bot_r2_head_{num_str}.png")
        if os.path.exists(head_path):
            in_w, in_h = 264, 198
            ix0 = x0 + cell_w - in_w - 12
            iy0 = y0 + cell_img_h - in_h - 12
            draw.rounded_rectangle(
                [ix0 - 3, iy0 - 24, ix0 + in_w + 3, iy0 + in_h + 3],
                radius=6,
                fill=(14, 18, 26),
                outline=outline_col,
                width=2,
            )
            im_h = Image.open(head_path).convert("RGB").resize((in_w, in_h), Image.Resampling.LANCZOS)
            sheet.paste(im_h, (ix0, iy0))
            draw.text((ix0 + 8, iy0 - 19), f"HEAD #{num_str} CLOSE-UP INSET", fill=(255, 224, 150) if is_hero else (140, 230, 255), font=font_inset)

        draw.rounded_rectangle(
            [x0 + 12, y0 + 12, x0 + 68, y0 + 50],
            radius=6,
            fill=(255, 183, 3) if is_hero else (0, 210, 245),
        )
        draw.text((x0 + 23, y0 + 17), num_str, fill=(10, 14, 20), font=font_badge)

        glb_fn = f"char_bot_r2_{num_str}.glb"
        st = stats_map.get(glb_fn, stats_map.get(f"char_bot_johnny5_r2_{num_str}.glb", {}))
        tris = st.get("triangles", st.get("tris", 0))
        stat_txt = f"{glb_fn} | {tris:,} Tris" if tris else f"{glb_fn} | Treads #03 + Chassis #01"
        draw.rounded_rectangle([x0 + cell_w - 335, y0 + 12, x0 + cell_w - 12, y0 + 44], radius=6, fill=(14, 18, 25))
        draw.text(
            (x0 + cell_w - 323, y0 + 19),
            stat_txt,
            fill=(255, 224, 150) if is_hero else (190, 225, 255),
            font=font_tris,
        )

        fy0 = y0 + cell_img_h
        draw.rectangle([x0, fy0, x0 + cell_w, y0 + cell_h], fill=(16, 20, 27))
        draw.text((x0 + 14, fy0 + 10), f"#{num_str} — {ctitle}", fill=(240, 245, 255), font=font_card_title)
        draw.text(
            (x0 + 14, fy0 + 38),
            cdesc,
            fill=(255, 209, 102) if is_hero else (0, 215, 245),
            font=font_card_desc,
        )
        draw.text(
            (x0 + 14, fy0 + 62),
            "Locked Hybrid Body: #03 Wide Quad-Bogie Treads + #01 Cube-Compactor Chassis • 20 Articulated Nodes",
            fill=(155, 175, 198),
            font=font_card_desc,
        )

    out_names = [
        "utility_bot_round2_head_explorations_sheet.png",
        "utility_bot_round2_voting_sheet.png",
        "johnny5_bot_round2_voting_sheet.png",
        "char_bot_r2_voting_sheet.png",
    ]
    for d in OUT_DIRS:
        os.makedirs(d, exist_ok=True)
        for oname in out_names:
            out_p = os.path.join(d, oname)
            sheet.save(out_p, "PNG", compress_level=4)
            print(f"[UtilityBotR2Sheet] Saved {out_p} ({canvas_w}x{canvas_h})")
    return True


if __name__ == "__main__":
    compose_r2_sheet()
