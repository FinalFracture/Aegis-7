#!/usr/bin/env python3
"""
Composes the 5-panel Room 02 Hero Fixture (Pressurized Bulkhead Airlock Hatch & Sector Checkpoint) Voting Sheet.
Writes to:
- ./godot/renders/corridor_round1/corridor_door_round1_voting_sheet.png
- ./assets/renders/corridor_round1/corridor_door_round1_voting_sheet.png
"""
import os
import json
from PIL import Image, ImageDraw, ImageFont

CANDIDATES = [
    (
        "corridor_door_r1_01",
        "01",
        "01_aegis7_octagonal_biparting_hatch",
        "Aegis-7 Octagonal Bi-Parting Blast Hatch",
        "2.45m W × 0.62m D × 2.75m H",
        "Parted blast doors • 3D dog-latch teeth • Dual octagonal windows",
    ),
    (
        "corridor_door_r1_02",
        "02",
        "02_dual_zone_airlock_emergency_sidebay",
        "Dual-Zone Airlock Portal & Emergency Side Bay",
        "2.60m W × 0.65m D × 2.75m H",
        "68/32 Aegis-7 split bay • Bi-parting hatch + O2/extinguisher locker",
    ),
    (
        "corridor_door_r1_03",
        "03",
        "03_cylindrical_plug_door_doglatch_portal",
        "Cylindrical Plug-Door & Rotary Dog-Latch Portal",
        "2.45m W × 0.70m D × 2.75m H",
        "Curved plug-door halves • 8 radial locking dogs • Spider wheel",
    ),
    (
        "corridor_door_r1_04",
        "04",
        "04_hex_aperture_wedge_blade_bulkhead",
        "Hex-Aperture 4-Blade Interlocking Bulkhead",
        "2.50m W × 0.62m D × 2.75m H",
        "4 diagonal wedge blades • Trapezoidal windows • Dual OLED piers",
    ),
    (
        "corridor_door_r1_05",
        "05",
        "05_panoramic_twin_window_decon_arch",
        "Panoramic Twin-Window Observation & Decon Arch",
        "2.55m W × 0.68m D × 2.78m H",
        "Full-height panoramic glass doors • UV/sonic decon arch • Biometric kiosk",
    ),
]

RENDER_DIR = "./godot/renders/corridor_round1"
MANIFEST_PATH = "./assets/glb/corridor_round1/corridor_door_r1_manifest.json"
OUT_PATHS = [
    "./godot/renders/corridor_round1/corridor_door_round1_voting_sheet.png",
    "./assets/renders/corridor_round1/corridor_door_round1_voting_sheet.png",
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

    font_title = load_font(28, bold=True)
    font_sub = load_font(18, bold=False)
    font_badge = load_font(25, bold=True)
    font_card_title = load_font(17, bold=True)
    font_card_meta = load_font(14, bold=False)
    font_card_desc = load_font(14, bold=False)

    draw.rectangle([0, 0, canvas_w, header_h], fill=(18, 22, 30))
    draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(0, 229, 255), width=3)
    draw.text(
        (pad, 22),
        "CYLINDER HAB-7 — ROOM 02 HERO FIXTURE: PRESSURIZED BULKHEAD AIRLOCK HATCH (5 CANDIDATES)",
        fill=(232, 242, 255),
        font=font_title,
    )
    draw.text(
        (pad, 68),
        "Godot 4.3 Real-Time Renders • Parted Blast Doors, 3D Interlocking Dog-Latch Teeth, Translucent Windows & Next-Sector Vista • Vote 01 – 05",
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
            iw, ih = im.size
            crop_w = int(iw * 0.84)
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
        print(f"[CorridorVotingSheet] Saved {out_p} ({canvas_w}x{canvas_h})")


if __name__ == "__main__":
    compose_voting_sheet()
