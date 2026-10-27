#!/usr/bin/env python3
"""
Composes the 10-panel Round 1 Hard Sci-Fi Bunk Pod Tournament Voting Sheet from the 10 Godot 4 renders.
Writes to:
- ./godot/renders/bunk_round1/bunk_round1_voting_sheet.png
- ./assets/renders/bunk_round1/bunk_round1_voting_sheet.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

CANDIDATES = [
    ("bunk_r1_01", "01", "01_aerospace_cryo_berth", "Molded White Aerospace Sleep Capsule", "Smoked canopy • Cyan LED strip • Vitals HUD"),
    ("bunk_r1_02", "02", "02_expanse_bulkhead_rack", "High-G Armored Bulkhead Berth", "Gunmetal hull bay • G-force bolsters • Amber strip"),
    ("bunk_r1_03", "03", "03_zero_g_mag_couchette", "Cantilevered Mag-Lock Orbital Pod", "Floating magnetic rails • Shock dampers • Cyan LED"),
    ("bunk_r1_04", "04", "04_blast_shutter_pod", "Armored Blast-Shutter Crew Pod", "Segmented titanium shutter • Gasket rim • Telemetry"),
    ("bunk_r1_05", "05", "05_spin_transition_harness_bunk", "Zero-G / Spin-Gravity Restraint Pod", "EVA lockdown bars • Tensioned webbing • Flight couch"),
    ("bunk_r1_06", "06", "06_orbital_viewport_pod", "Deep-Space Observation Sleep Bay", "Chamfered hull viewport • Cyan bezel • Starlit core"),
    ("bunk_r1_07", "07", "07_stacked_corvette_bunks", "Naval Frigate Dual Pod Stack", "Twin enclosed tubes • BAY 01/02 plates • Cyan strips"),
    ("bunk_r1_08", "08", "08_recessed_stasis_alcove", "Pressurized Stasis-Style Chamber", "Octagonal bulkhead • Amber hazard step • Bi-level pad"),
    ("bunk_r1_09", "09", "09_bio_lifesupport_pod", "Closed-Loop O2 Scrubber & Hydro-Bay", "Sealed glass O2 bio-tube • UV/Cyan LEDs • Conduits"),
    ("bunk_r1_10", "10", "10_command_stateroom_capsule", "Officer's Panoramic Smart-Pod", "Dark titanium bay • Twin OLED wings • Cyan cove arch"),
]

RENDER_DIR = "./godot/renders/bunk_round1"
OUT_PATHS = [
    "./godot/renders/bunk_round1/bunk_round1_voting_sheet.png",
    "./assets/renders/bunk_round1/bunk_round1_voting_sheet.png",
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
    cols = 5
    rows = 2
    cell_w = 640
    cell_img_h = 360
    cell_footer_h = 92
    cell_h = cell_img_h + cell_footer_h
    pad = 24
    header_h = 110

    canvas_w = pad + cols * (cell_w + pad)
    canvas_h = header_h + pad + rows * (cell_h + pad)

    sheet = Image.new("RGB", (canvas_w, canvas_h), (12, 15, 20))
    draw = ImageDraw.Draw(sheet)

    font_title = load_font(33, bold=True)
    font_sub = load_font(18, bold=False)
    font_badge = load_font(25, bold=True)
    font_card_title = load_font(18, bold=True)
    font_card_slug = load_font(14, bold=False)
    font_card_desc = load_font(14, bold=False)

    # Header bar
    draw.rectangle([0, 0, canvas_w, header_h], fill=(18, 22, 30))
    draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(0, 229, 255), width=3)
    draw.text(
        (pad, 22),
        "CYLINDER HAB-7 — HARD SCI-FI BUNK POD TOURNAMENT: ROUND 1 OF 4 (10 CANDIDATES)",
        fill=(232, 242, 255),
        font=font_title,
    )
    draw.text(
        (pad, 68),
        "Godot 4.3 Real-Time Spacecraft Bay Renders • Anodized Gunmetal, Aerospace Composite & Cyan/Amber LED Rigs • Vote 01 – 10",
        fill=(0, 215, 245),
        font=font_sub,
    )

    for idx, (cid, num_str, slug, title, desc) in enumerate(CANDIDATES):
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

        img_path = os.path.join(RENDER_DIR, f"{cid}.png")
        if os.path.exists(img_path):
            im = Image.open(img_path).convert("RGB")
            im = im.resize((cell_w, cell_img_h), Image.Resampling.LANCZOS)
            sheet.paste(im, (x0, y0))

        bx0, by0 = x0 + 12, y0 + 12
        draw.rounded_rectangle(
            [bx0, by0, bx0 + 58, by0 + 42],
            radius=8,
            fill=(0, 200, 235),
            outline=(210, 248, 255),
            width=2,
        )
        draw.text((bx0 + 12, by0 + 7), num_str, fill=(10, 14, 20), font=font_badge)

        fy0 = y0 + cell_img_h
        draw.rectangle([x0, fy0, x0 + cell_w, y0 + cell_h], fill=(16, 20, 27))
        draw.text((x0 + 14, fy0 + 10), f"#{num_str} — {title}", fill=(235, 244, 255), font=font_card_title)
        draw.text((x0 + 14, fy0 + 36), f"ID: {slug} ({cid}.glb)", fill=(0, 215, 245), font=font_card_slug)
        draw.text((x0 + 14, fy0 + 60), desc, fill=(164, 178, 196), font=font_card_desc)

    for out_p in OUT_PATHS:
        os.makedirs(os.path.dirname(out_p), exist_ok=True)
        sheet.save(out_p, "PNG", optimize=True)
        print(f"[VotingSheet] Saved {out_p} ({canvas_w}x{canvas_h})")


if __name__ == "__main__":
    compose_voting_sheet()
