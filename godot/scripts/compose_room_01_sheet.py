#!/usr/bin/env python3
"""
Composes the 2x2 Quad Overview Sheet for Room 01 — Crew Sleeping Quarters (Aegis-7 Standard).
Writes to:
- ./godot/renders/rooms/room_01/room_01_sleeping_quarters_sheet.png
- ./assets/renders/rooms/room_01/room_01_sleeping_quarters_sheet.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

VIEWS = [
    ("cam_01_overview_south_entry", "CAM 01 — SOUTH AIRLOCK ENTRY WIDE OVERVIEW", "6.0m × 7.0m × 3.2m Aegis-7 Stateroom • North O'Neill Cylinder Viewport • Cyan/Amber Coves"),
    ("cam_02_west_bunks_and_footlocker", "CAM 02 — WEST BUNK BAYS & SPLIT CARGO FOOTLOCKER", "Bunk #01 Orbital Viewport (Deep-Space Vista) • Bunk #03 Hex-Hive Stack • Footlocker #02"),
    ("cam_03_east_aegis_utility_wall", "CAM 03 — EAST AEGIS-7 SPLIT-BAY UTILITY TRIAD", "Vanity #03 (UV Decon) • Wall Desk #02 (Drop-Leaf Comms) • EVA Suit Locker #02 (Gold Visor)"),
    ("cam_04_north_viewport_and_climate", "CAM 04 — SOUTH ENTRY BULKHEAD & CLIMATE/O2 STATION", "Climate & O2 Station #02 (UV Louvers & Breather Bay) • EVA Locker #02 • South Airlock Hatch"),
]

RENDER_DIR = "./godot/renders/rooms/room_01"
OUT_PATHS = [
    "./godot/renders/rooms/room_01/room_01_sleeping_quarters_sheet.png",
    "./assets/renders/rooms/room_01/room_01_sleeping_quarters_sheet.png",
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


def compose_sheet():
    cols = 2
    rows = 2
    cell_w = 1280
    cell_img_h = 720
    cell_footer_h = 76
    cell_h = cell_img_h + cell_footer_h
    pad = 24
    header_h = 112

    canvas_w = pad + cols * (cell_w + pad)
    canvas_h = header_h + pad + rows * (cell_h + pad)

    sheet = Image.new("RGB", (canvas_w, canvas_h), (12, 15, 20))
    draw = ImageDraw.Draw(sheet)

    font_title = load_font(34, bold=True)
    font_sub = load_font(19, bold=False)
    font_card_title = load_font(20, bold=True)
    font_card_desc = load_font(16, bold=False)

    draw.rectangle([0, 0, canvas_w, header_h], fill=(18, 22, 30))
    draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(0, 229, 255), width=3)
    draw.text(
        (pad, 22),
        "CYLINDER HAB-7 — ROOM 01: CREW SLEEPING QUARTERS (AEGIS-7 FULL STATEROOM SHOWCASE)",
        fill=(232, 242, 255),
        font=font_title,
    )
    draw.text(
        (pad, 68),
        "Godot 4.3 Real-Time 4-Camera Suite • All Locked Bunk & Utility Winners • Translucent O'Neill Cylinder & Deep-Space Viewports",
        fill=(0, 215, 245),
        font=font_sub,
    )

    for idx, (cname, title, desc) in enumerate(VIEWS):
        r = idx // cols
        c = idx % cols
        x0 = pad + c * (cell_w + pad)
        y0 = header_h + pad + r * (cell_h + pad)

        draw.rounded_rectangle(
            [x0 - 2, y0 - 2, x0 + cell_w + 2, y0 + cell_h + 2],
            radius=10,
            fill=(22, 27, 36),
            outline=(48, 72, 96),
            width=2,
        )

        img_path = os.path.join(RENDER_DIR, f"{cname}.png")
        if os.path.exists(img_path):
            im = Image.open(img_path).convert("RGB").resize((cell_w, cell_img_h), Image.Resampling.LANCZOS)
            sheet.paste(im, (x0, y0))

        fy0 = y0 + cell_img_h
        draw.rectangle([x0, fy0, x0 + cell_w, y0 + cell_h], fill=(16, 20, 27))
        draw.text((x0 + 16, fy0 + 12), title, fill=(235, 244, 255), font=font_card_title)
        draw.text((x0 + 16, fy0 + 42), desc, fill=(0, 215, 245), font=font_card_desc)

    for out_p in OUT_PATHS:
        os.makedirs(os.path.dirname(out_p), exist_ok=True)
        sheet.save(out_p, "PNG", optimize=True)
        print(f"[Room01Sheet] Saved {out_p} ({canvas_w}x{canvas_h})")


if __name__ == "__main__":
    compose_sheet()
