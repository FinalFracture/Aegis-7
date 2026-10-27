#!/usr/bin/env python3
"""
Composes the 1920x1080 2x2 Annotated Full-Scale Interior Showcase Contact Sheet
for Cylinder Hab-7 (Overhauled with Sloane's Golden-Hour Lighting & Biome Textures
+ Vance & Rook's Asymmetric 3-Valley Biomes & 5 Hero Interior Setpieces):
- ./godot/renders/cylinder_interior/cylinder_interior_showcase_sheet.png
- ./assets/renders/cylinder_interior/cylinder_interior_showcase_sheet.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT_DIRS = [
    "./godot/renders/cylinder_interior",
    "./assets/renders/cylinder_interior",
]

VIEWS = [
    (
        "cam_01_interior_axial_vista",
        "CAM 01 — FORWARD AXIAL MEGASTRUCTURE VISTA (GOLDEN-HOUR SUN SPINE & 3 ASYMMETRIC BIOME VALLEYS)",
        "Golden-Hour Axial Sun (#FFE3B3) • Aerial Perspective across 400m Ø • Civic Acropolis, Emerald River & Industrial Port",
    ),
    (
        "cam_02_interior_ground_looking_up_curve",
        "CAM 02 — VALLEY A CIVIC ACROPOLIS & SPECULAR RING-RIVER LOOKING UP 360° CURVED WALLS",
        "Warm Amber Windows (u: 0.0-0.5) • Travertine Promenade & Botanical Terraces • Ring-Spanning Skybridge & Overhead Biomes",
    ),
    (
        "cam_03_interior_midring_overlook",
        "CAM 03 — MID-RING TERRACE OVERLOOK ACROSS 400m DIAMETER TO WATERFALL BIOSPHERE & SKYBRIDGE",
        "Cross-Cylinder Aerial Perspective • Specular Ring-River & Stepped Hydro-Dam • Inverted 400m Overhead District",
    ),
    (
        "cam_04_interior_starport_throat_lookback",
        "CAM 04 — AFT ZERO-G STARPORT THROAT LOOKING BACK TOWARD GOLDEN-HOUR DRUM & ENDCAP CITADEL",
        "Cool Telemetry Industrial Ridge (u: 0.5-1.0) • Axial Sun-Core Spoke Hubs • Stepped Forward Endcap Cliffside Citadel",
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


def compose_interior_sheet():
    src_dir = OUT_DIRS[0]
    for v in VIEWS:
        p = os.path.join(src_dir, f"{v[0]}.png")
        if not os.path.exists(p):
            raise FileNotFoundError(f"Missing required interior render: {p}")

    canvas_w, canvas_h = 1920, 1080
    header_h = 84
    pad = 16
    cols, rows = 2, 2

    cell_w = (canvas_w - pad * (cols + 1)) // cols  # 936
    cell_h = (canvas_h - header_h - pad * (rows + 1)) // rows  # 474
    footer_h = 54
    img_h = cell_h - footer_h  # 420

    sheet = Image.new("RGB", (canvas_w, canvas_h), (10, 14, 20))
    draw = ImageDraw.Draw(sheet)

    font_title = load_font(22, bold=True)
    font_sub = load_font(13, bold=False)
    font_card_title = load_font(14, bold=True)
    font_card_desc = load_font(12, bold=False)

    # Header bar
    draw.rectangle([0, 0, canvas_w, header_h], fill=(16, 22, 32))
    draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(255, 183, 3), width=3)
    draw.text(
        (pad, 14),
        "CYLINDER HAB-7 — OVERHAULED FULL-SCALE (800m × 400m, R = 200m) INTERIOR BIOME & GOLDEN-HOUR SHOWCASE",
        fill=(245, 240, 230),
        font=font_title,
    )
    draw.text(
        (pad, 50),
        "Golden-Hour Axial Sun (#FFE3B3) • Aerial Perspective • 3 Asymmetric Biome Valleys • Specular Ring-River • 5 Hero Macro-Setpieces & 20 Locked #02 Buildings",
        fill=(255, 209, 102),
        font=font_sub,
    )

    for idx, (fname, ctitle, cdesc) in enumerate(VIEWS):
        r, c = idx // cols, idx % cols
        x0 = pad + c * (cell_w + pad)
        y0 = header_h + pad + r * (cell_h + pad)

        border_col = (255, 183, 3) if idx == 0 else (64, 96, 128)
        draw.rounded_rectangle(
            [x0 - 2, y0 - 2, x0 + cell_w + 2, y0 + cell_h + 2],
            radius=8,
            fill=(20, 26, 36),
            outline=border_col,
            width=2,
        )

        im_path = os.path.join(src_dir, f"{fname}.png")
        im = Image.open(im_path).convert("RGB").resize((cell_w, img_h), Image.Resampling.LANCZOS)
        sheet.paste(im, (x0, y0))

        fy0 = y0 + img_h
        draw.rectangle([x0, fy0, x0 + cell_w, y0 + cell_h], fill=(14, 18, 26))
        draw.text((x0 + 12, fy0 + 7), ctitle, fill=(245, 242, 235), font=font_card_title)
        draw.text((x0 + 12, fy0 + 29), cdesc, fill=(255, 209, 102) if idx < 2 else (88, 224, 255), font=font_card_desc)

    for d in OUT_DIRS:
        os.makedirs(d, exist_ok=True)
        for out_name in ["cylinder_interior_showcase_sheet.png", "cylinder_interior_sheet.png"]:
            out_p = os.path.join(d, out_name)
            sheet.save(out_p, "PNG", compress_level=4)
            print(f"[CylinderInteriorSheet] Saved {out_p} ({canvas_w}x{canvas_h})")


if __name__ == "__main__":
    compose_interior_sheet()
