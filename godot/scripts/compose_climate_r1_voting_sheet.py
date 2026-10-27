#!/usr/bin/env python3
"""
Composes the 5-panel Personal Climate & Life-Support Wall Panel Voting Comparison Sheet.
Writes to:
- ./godot/renders/climate_round1/climate_round1_voting_sheet.png
- ./assets/renders/climate_round1/climate_round1_voting_sheet.png
"""
import os
import json
from PIL import Image, ImageDraw, ImageFont

CANDIDATES = [
    (
        "climate_r1_01",
        "01",
        "01_recessed_octagonal_lifesupport_station",
        "Recessed Octagonal Life-Support & O2 Station",
        "0.90m W × 0.30m D × 1.90m H",
        "3-tier octagonal stack • UV-violet louvers • Translucent O2 bay",
    ),
    (
        "climate_r1_02",
        "02",
        "02_dual_zone_split_telemetry_breather_bay",
        "Dual-Zone Split Telemetry & Breather Bay",
        "0.96m W × 0.32m D × 1.92m H",
        "62/38 split bay (matches Locker/Vanity/Desk/Footlocker) • O2 tower",
    ),
    (
        "climate_r1_03",
        "03",
        "03_cylindrical_vortex_scrubber_column",
        "Cylindrical Vortex Scrubber & Barometer Column",
        "0.88m W × 0.34m D × 1.92m H",
        "Radial vortex turbine • Curved OLED collar • Glass scrubber bay",
    ),
    (
        "climate_r1_04",
        "04",
        "04_cantilevered_smartglass_dropmask_pod",
        "Cantilevered Smart-Glass & Quick-Drop Mask Pod",
        "0.92m W × 0.30m D × 1.88m H",
        "Floating translucent HUD pane • Quick-drop mask dispenser",
    ),
    (
        "climate_r1_05",
        "05",
        "05_pressure_bulkhead_damper_o2_manifold",
        "Pressure-Bulkhead Damper & Tactical O2 Manifold",
        "0.95m W × 0.32m D × 1.92m H",
        "Butterfly air-damper window • Orange 4-spoke O2 handwheel",
    ),
]

RENDER_DIR = "./godot/renders/climate_round1"
MANIFEST_PATH = "./assets/glb/climate_round1/climate_r1_manifest.json"
OUT_PATHS = [
    "./godot/renders/climate_round1/climate_round1_voting_sheet.png",
    "./assets/renders/climate_round1/climate_round1_voting_sheet.png",
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

    font_title = load_font(29, bold=True)
    font_sub = load_font(18, bold=False)
    font_badge = load_font(25, bold=True)
    font_card_title = load_font(17, bold=True)
    font_card_meta = load_font(14, bold=False)
    font_card_desc = load_font(14, bold=False)

    draw.rectangle([0, 0, canvas_w, header_h], fill=(18, 22, 30))
    draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(0, 229, 255), width=3)
    draw.text(
        (pad, 22),
        "CYLINDER HAB-7 — FIXTURE #9: PERSONAL CLIMATE & LIFE-SUPPORT WALL PANEL (5 CANDIDATES)",
        fill=(232, 242, 255),
        font=font_title,
    )
    draw.text(
        (pad, 68),
        "Godot 4.3 Real-Time Spacecraft Bay Renders • Laminar UV Louvers, Coriolis/O2 OLED Telemetry, Translucent Breather-Mask Bay & CO2 Scrubbers • Vote 01 – 05",
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
            crop_w = int(iw * 0.74)
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
        print(f"[ClimateVotingSheet] Saved {out_p} ({canvas_w}x{canvas_h})")


if __name__ == "__main__":
    compose_voting_sheet()
