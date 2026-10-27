#!/usr/bin/env python3
"""
Composes the 5-panel EVA Suit & Personal Gear Locker Voting Comparison Sheet.
Writes to:
- ./godot/renders/locker_round1/locker_round1_voting_sheet.png
- ./assets/renders/locker_round1/locker_round1_voting_sheet.png
"""
import os
import json
from PIL import Image, ImageDraw, ImageFont

CANDIDATES = [
    (
        "locker_r1_01",
        "01",
        "01_pressurized_airlock_suit_pod",
        "Pressurized Cylindrical Airlock Suit Pod",
        "1.10m W × 0.85m D × 2.15m H",
        "Parted curved glass doors • Gold-visor EVA suit • Cyan & amber rings",
    ),
    (
        "locker_r1_02",
        "02",
        "02_dual_bay_recessed_suit_locker",
        "Dual-Bay Recessed Bulkhead Suit & Kit Locker",
        "1.35m W × 0.75m D × 2.10m H",
        "Left glass suit bay • Right 3-tier kit, flight bag & O2 bottles",
    ),
    (
        "locker_r1_03",
        "03",
        "03_hex_frame_exosuit_gantry",
        "Hex-Frame Exosuit Gantry & Mag-Boot Alcove",
        "1.20m W × 0.80m D × 2.15m H",
        "45° hex chamfer alcove • Overhead crane arm • Clamped mag-boots",
    ),
    (
        "locker_r1_04",
        "04",
        "04_aerospace_capsule_uv_sterilizer",
        "Aerospace Capsule Wardrobe & UV Sterilizer",
        "1.15m W × 0.75m D × 2.12m H",
        "Monocoque white capsule • Violet UV-C quartz door • Helmet niche",
    ),
    (
        "locker_r1_05",
        "05",
        "05_corner_mount_tactical_prep_station",
        "Corner-Mount Angled Tactical EVA Prep Station",
        "1.25m W × 0.85m D × 2.15m H",
        "35° angled side wings • OLED terminal & O2 rack • Amber backlight",
    ),
]

RENDER_DIR = "./godot/renders/locker_round1"
MANIFEST_PATH = "./assets/glb/locker_round1/locker_r1_manifest.json"
OUT_PATHS = [
    "./godot/renders/locker_round1/locker_round1_voting_sheet.png",
    "./assets/renders/locker_round1/locker_round1_voting_sheet.png",
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


def compose_voting_sheet():
    tris_by_id = {}
    if os.path.exists(MANIFEST_PATH):
        try:
            with open(MANIFEST_PATH, "r") as f:
                data = json.load(f)
            for item in data:
                cid = os.path.splitext(os.path.basename(item.get("filepath", "")))[0]
                tris_by_id[cid] = item.get("triangles", 0)
        except Exception:
            pass

    cols = 5
    rows = 1
    cell_w = 640
    cell_img_h = 420
    cell_footer_h = 104
    cell_h = cell_img_h + cell_footer_h
    pad = 24
    header_h = 112

    canvas_w = pad + cols * (cell_w + pad)
    canvas_h = header_h + pad + rows * (cell_h + pad)

    sheet = Image.new("RGB", (canvas_w, canvas_h), (12, 15, 20))
    draw = ImageDraw.Draw(sheet)

    font_title = load_font(31, bold=True)
    font_sub = load_font(18, bold=False)
    font_badge = load_font(25, bold=True)
    font_card_title = load_font(17, bold=True)
    font_card_meta = load_font(14, bold=False)
    font_card_desc = load_font(14, bold=False)

    draw.rectangle([0, 0, canvas_w, header_h], fill=(18, 22, 30))
    draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(0, 229, 255), width=3)
    draw.text(
        (pad, 22),
        "CYLINDER HAB-7 — FIXTURE #1: EVA SUIT & PERSONAL GEAR LOCKER (5 CANDIDATES)",
        fill=(232, 242, 255),
        font=font_title,
    )
    draw.text(
        (pad, 68),
        "Godot 4.3 Real-Time Spacecraft Bay Renders • Translucent Suit-Bay Glass, 3D Gold-Visor EVA Suit, Umbilicals & Mag-Boots • Vote 01 – 05",
        fill=(0, 215, 245),
        font=font_sub,
    )

    for idx, (cid, num_str, slug, title, dims_str, desc) in enumerate(CANDIDATES):
        x0 = pad + idx * (cell_w + pad)
        y0 = header_h + pad

        draw.rounded_rectangle(
            [x0 - 2, y0 - 2, x0 + cell_w + 2, y0 + cell_h + 2],
            radius=10,
            fill=(22, 27, 36),
            outline=(48, 72, 96),
            width=2,
        )

        img_path = os.path.join(RENDER_DIR, f"{cid}.png")
        if os.path.exists(img_path):
            im = Image.open(img_path).convert("RGB")
            # Center-crop slightly to emphasize vertical locker silhouette inside 640x420 panel
            iw, ih = im.size
            crop_w = int(iw * 0.78)
            left = (iw - crop_w) // 2
            im_cropped = im.crop((left, 0, left + crop_w, ih)).resize((cell_w, cell_img_h), Image.Resampling.LANCZOS)
            sheet.paste(im_cropped, (x0, y0))

        bx0, by0 = x0 + 12, y0 + 12
        draw.rounded_rectangle(
            [bx0, by0, bx0 + 58, by0 + 42],
            radius=8,
            fill=(0, 200, 235),
            outline=(210, 248, 255),
            width=2,
        )
        draw.text((bx0 + 12, by0 + 7), num_str, fill=(10, 14, 20), font=font_badge)

        tris_txt = f" • {tris_by_id[cid]:,} tris" if cid in tris_by_id else ""
        fy0 = y0 + cell_img_h
        draw.rectangle([x0, fy0, x0 + cell_w, y0 + cell_h], fill=(16, 20, 27))
        draw.text((x0 + 14, fy0 + 10), f"#{num_str} — {title}", fill=(235, 244, 255), font=font_card_title)
        draw.text((x0 + 14, fy0 + 36), f"{cid}.glb • {dims_str}{tris_txt}", fill=(0, 215, 245), font=font_card_meta)
        draw.text((x0 + 14, fy0 + 64), desc, fill=(164, 178, 196), font=font_card_desc)

    for out_p in OUT_PATHS:
        os.makedirs(os.path.dirname(out_p), exist_ok=True)
        sheet.save(out_p, "PNG", optimize=True)
        print(f"[LockerVotingSheet] Saved {out_p} ({canvas_w}x{canvas_h})")


if __name__ == "__main__":
    compose_voting_sheet()
