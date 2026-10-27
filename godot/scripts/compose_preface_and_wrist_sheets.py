#!/usr/bin/env python3
"""
Composes:
1. 5-Candidate Embedded Wrist RFID / Center-Screen Hand-Rig Voting Sheet:
   - `wrist_rfid_round1_voting_sheet.png`
   - `prop_wrist_rfid_round1_voting_sheet.png`
2. 4-Camera (2x2) Preface Service-Call Test Environment Showcase Sheet:
   - `preface_test_environment_showcase_sheet.png`
   - `preface_service_call_test_sheet.png`
"""
import os
import json
from PIL import Image, ImageDraw, ImageFont

WRIST_OUT_DIRS = [
    "./godot/renders/wrist_rfid",
    "./godot/renders/props/wrist_rfid",
    "./godot/renders/preface",
    "./assets/renders/wrist_rfid",
    "./assets/renders/props/wrist_rfid",
    "./assets/renders/preface",
]

PREFACE_OUT_DIRS = [
    "./godot/renders/preface",
    "./godot/renders",
    "./assets/renders/preface",
    "./assets/renders",
]

WRIST_CANDS = [
    (
        "01",
        "Subdermal Hex-Node Array + Minimalist Titanium Split-Band",
        "7-Node Honeycomb Dorsal Metacarpal Array • Hinged Aerospace-White & Brushed-Steel Cuff • Sapphire Scan Ring",
    ),
    (
        "02",
        "The 'Induction Loom' — 68/32 Split-Mass Gyro-Aperture Cuff & Vein-Grid (HERO #02)",
        "Aegis-7 68/32 Split-Cuff • 3-Petal Iris Aperture & Ulnar Capacitor • 5-Node Subdermal Vein-Grid & Sapphire Holo Bridge",
    ),
    (
        "03",
        "Heavy Industrial Forearm Exo-Clamp + Flip-Up Optical Reticle Loupe",
        "Rugged Carbon-Slate & Signal-Orange Exo-Cage • Twin Hydraulic Wrist Struts • 3 Subdermal Socket Plugs & Flip-Up Loupe",
    ),
    (
        "04",
        "Bio-Luminescent Neural Tendon Trace + Flexible Polymer Smart-Sleeve",
        "Form-Fitting Carbon Weave Second-Skin Sleeve • Branching Cyan/UV-Violet Dendritic Fiber-Optics • Elastomer Holo Arc",
    ),
    (
        "05",
        "Tri-Spoke Magnetic Field Emitter + Knuckle-Bridge RFID Projector",
        "Gunmetal Tri-Spoke Collar with 3 Signal-Orange Deployable Fins • Transverse 4-Bar Subdermal Strip • Octagonal Beam-Splitter",
    ),
]

PREFACE_VIEWS = [
    (
        "cam_01_initial_commuter_wrist_demo",
        "CAM 01 — INITIAL ARRIVAL & WORDLESS CITIZEN WRIST-RAISE DEMONSTRATION",
        "10m×8m×4.2m Sector-4 Vestibule • East 5500K Promenade Window • Commuter A Raising Left Wrist (#FF9500 Lockout Flash)",
    ),
    (
        "cam_02_cycle1_center_screen_wrist_scan_40pct_jam",
        "CAM 02 — SCAN CYCLE 1: CENTER-SCREEN WRIST RFID RAISE & 40% COUNTERWEIGHT JAM",
        "Button-Mash Center-Screen Hand Raise (#02 Induction Loom) • Subdermal Cyan Vein-Grid • Leaf_B Jams at 40% in Glass Transom",
    ),
    (
        "cam_03_cycle2_droid_relay_counterweight_sync",
        "CAM 03 — SCAN CYCLE 2: ASSISTANT DROID (UNIT A7-D2) RELAY HANDSHAKE & SYNC",
        "Center-Screen Wrist Coupled to Droid #D95B26 Collar • Probe Arm Holding Relay_Panel_B • Counterweight Rail Re-Indexing",
    ),
    (
        "cam_04_cycle3_final_unlock_commuters_exit",
        "CAM 04 — SCAN CYCLE 3: 100% OPEN CLEARANCE & COMMUTER THANK-YOU WAVE EXIT",
        "All 3 Header Nodes & Threshold Solid #00E5FF Cyan • Both Leaves 100% Open (2.20m) • Commuters Waving as They Exit to Promenade",
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


def get_wrist_stats():
    stats = {}
    manifest_paths = [
        "./godot/assets/models/props/wrist_rfid/wrist_rfid_manifest.json",
        "./assets/glb/props/wrist_rfid/wrist_rfid_manifest.json",
        "./assets/glb/wrist_rfid/wrist_rfid_manifest.json",
        "./assets/glb/preface_and_wrist_rfid_manifest.json",
        "./assets/glb/preface_and_wrist_manifest.json",
    ]
    for mp in manifest_paths:
        if os.path.exists(mp):
            try:
                with open(mp, "r") as f:
                    data = json.load(f)
                items = (
                    data
                    if isinstance(data, list)
                    else data.get("wrist_rfid_candidates_5", data.get("wrist_rfid_candidates", data.get("wrist_candidates", data.get("candidates", []))))
                )
                for it in items:
                    fn = os.path.basename(it.get("filepath", ""))
                    stats[fn] = it
            except Exception:
                pass
    return stats


def compose_wrist_voting_sheet():
    src_dir = WRIST_OUT_DIRS[0]
    for num_str, _, _ in WRIST_CANDS:
        if not os.path.exists(os.path.join(src_dir, f"prop_wrist_rfid_r1_{num_str}.png")):
            return False

    stats_map = get_wrist_stats()
    cols, rows = 3, 2
    cell_w, cell_img_h, cell_footer_h = 880, 495, 92
    cell_h = cell_img_h + cell_footer_h
    pad, header_h = 22, 108

    canvas_w = pad + cols * (cell_w + pad)
    canvas_h = header_h + pad + rows * (cell_h + pad)

    sheet = Image.new("RGB", (canvas_w, canvas_h), (12, 15, 20))
    draw = ImageDraw.Draw(sheet)

    font_title = load_font(26, bold=True)
    font_sub = load_font(15, bold=False)
    font_badge = load_font(22, bold=True)
    font_tris = load_font(15, bold=True)
    font_card_title = load_font(16, bold=True)
    font_card_desc = load_font(13, bold=False)

    draw.rectangle([0, 0, canvas_w, header_h], fill=(18, 22, 30))
    draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(0, 229, 255), width=3)
    draw.text(
        (pad, 20),
        "CYLINDER HAB-7 — EMBEDDED SUBDERMAL WRIST RFID & DIEGETIC HAND-RIG (5-CHOICE TEST)",
        fill=(242, 245, 250),
        font=font_title,
    )
    draw.text(
        (pad, 64),
        "Center-Screen Raised Left Hand & Forearm (0.42m × 0.14m × 0.12m) • Subdermal Glowing Vein-Nodes • Translucent Sapphire Holo Optics • Vote 01–05",
        fill=(0, 215, 245),
        font=font_sub,
    )

    for idx, (num_str, ctitle, cdesc) in enumerate(WRIST_CANDS):
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

        img_path = os.path.join(src_dir, f"prop_wrist_rfid_r1_{num_str}.png")
        im = Image.open(img_path).convert("RGB").resize((cell_w, cell_img_h), Image.Resampling.LANCZOS)
        sheet.paste(im, (x0, y0))

        draw.rounded_rectangle(
            [x0 + 12, y0 + 12, x0 + 68, y0 + 50],
            radius=6,
            fill=(255, 183, 3) if is_hero else (0, 210, 245),
        )
        draw.text((x0 + 23, y0 + 17), num_str, fill=(10, 14, 20), font=font_badge)

        glb_fn = f"prop_wrist_rfid_r1_{num_str}.glb"
        st = stats_map.get(glb_fn, {})
        tris = st.get("triangles", st.get("tris", 0))
        stat_txt = f"{glb_fn} | {tris:,} Tris" if tris else f"{glb_fn} | Aegis-7 PBR"
        draw.rounded_rectangle([x0 + cell_w - 340, y0 + 12, x0 + cell_w - 12, y0 + 44], radius=6, fill=(14, 18, 25))
        draw.text(
            (x0 + cell_w - 328, y0 + 19),
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
            "4-Quadrant PBR Atlas (Albedo/ORM/Normal/Emission 2.4x) + alphaMode: BLEND Sapphire Lens",
            fill=(155, 175, 198),
            font=font_card_desc,
        )

    out_names = [
        "wrist_rfid_round1_voting_sheet.png",
        "prop_wrist_rfid_round1_voting_sheet.png",
    ]
    for d in WRIST_OUT_DIRS:
        os.makedirs(d, exist_ok=True)
        for oname in out_names:
            out_p = os.path.join(d, oname)
            sheet.save(out_p, "PNG", compress_level=4)
            print(f"[WristVotingSheet] Saved {out_p} ({canvas_w}x{canvas_h})")
    return True


def compose_preface_showcase_sheet():
    src_dir = PREFACE_OUT_DIRS[0]
    for fname, _, _ in PREFACE_VIEWS:
        if not os.path.exists(os.path.join(src_dir, f"{fname}.png")):
            return False

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

    draw.rectangle([0, 0, canvas_w, header_h], fill=(16, 22, 32))
    draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(0, 229, 255), width=3)
    draw.text(
        (pad, 14),
        "CYLINDER HAB-7 — PREFACE SERVICE-CALL TEST ENVIRONMENT & 3-CYCLE WRIST RFID LOOP",
        fill=(242, 246, 255),
        font=font_title,
    )
    draw.text(
        (pad, 50),
        "Sector-4 Commuter Vestibule (preface_service_call_test.tscn) • Zero UI Text • Wordless Citizen Wrist Demo • Center-Screen Wrist RFID (#02) & Unit A7-D2 Droid Sync",
        fill=(255, 209, 102),
        font=font_sub,
    )

    for idx, (fname, ctitle, cdesc) in enumerate(PREFACE_VIEWS):
        r, c = idx // cols, idx % cols
        x0 = pad + c * (cell_w + pad)
        y0 = header_h + pad + r * (cell_h + pad)

        border_col = (255, 183, 3) if idx in (1, 2) else (0, 210, 245)
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
        draw.text((x0 + 12, fy0 + 7), ctitle, fill=(242, 246, 255), font=font_card_title)
        draw.text(
            (x0 + 12, fy0 + 29),
            cdesc,
            fill=(255, 209, 102) if idx in (1, 2) else (88, 224, 255),
            font=font_card_desc,
        )

    out_names = [
        "preface_test_environment_showcase_sheet.png",
        "preface_service_call_test_sheet.png",
    ]
    for d in PREFACE_OUT_DIRS:
        os.makedirs(d, exist_ok=True)
        for oname in out_names:
            out_p = os.path.join(d, oname)
            sheet.save(out_p, "PNG", compress_level=4)
            print(f"[PrefaceShowcaseSheet] Saved {out_p} ({canvas_w}x{canvas_h})")
    return True


if __name__ == "__main__":
    compose_wrist_voting_sheet()
    compose_preface_showcase_sheet()
