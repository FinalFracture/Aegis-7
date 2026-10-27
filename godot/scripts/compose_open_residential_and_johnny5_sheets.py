#!/usr/bin/env python3
"""
Composes:
1. Open-Doorway 2-Story Playable Residential Building Showcase Sheet (`1920x1080`):
   - `preface_open_residential_building_showcase_sheet.png`
   - `preface_playable_residential_showcase_sheet.png`
   - `preface_residential_sector_showcase_sheet.png`
2. 5-Candidate *WALL-E* x *Johnny 5* Utility Robot Voting Sheet (`2728x1348`):
   - `johnny5_bot_round1_voting_sheet.png`
   - `utility_bot_johnny5_round1_voting_sheet.png`
   - `char_bot_johnny5_round1_voting_sheet.png`
3. 4-Department Universal Cylinder Hab-7 Livery & Canonical [t74u] District Zoning Emblems Showcase Sheet (`1920x1080`):
   - `utility_bot_r2_05_universal_livery_and_emblems_sheet.png`
   - `utility_bot_r2_05_faction_livery_showcase_sheet.png`
   - `johnny5_bot_faction_livery_showcase_sheet.png`
"""
import os
import json
import shutil
from PIL import Image, ImageDraw, ImageFont

RES_OUT_DIRS = [
    "./godot/renders/preface",
    "./godot/renders",
    "./assets/renders/preface",
    "./assets/renders",
]

BOT_OUT_DIRS = [
    "./godot/renders/characters/johnny5",
    "./godot/renders/characters/bots",
    "./godot/renders/character/bots",
    "./godot/renders/bots",
    "./godot/renders/preface",
    "./assets/renders/characters/johnny5",
    "./assets/renders/characters/bots",
    "./assets/renders/character/bots",
    "./assets/renders/bots",
    "./assets/renders/preface",
]

RES_VIEWS = [
    (
        "cam_01_top_floor_apartment_open_portal",
        "CAM 01 — TOP-FLOOR TECH APARTMENT (APT 201) & OPEN DOORLESS PORTAL",
        "Player Spawn with #04 Bio-Luminescent Neural Smart-Sleeve • BCI Headband & Super-Wire Workbench • Wide-Open Portal to Level 2",
    ),
    (
        "cam_02_two_story_atrium_staircase_and_sweep_bot",
        "CAM 02 — 2-STORY RESIDENTIAL ATRIUM, OPEN MEZZANINE & STAIRCASE OVERLOOK",
        "28m×18m×9m Contiguous Atrium • Open Portals 201 & 202 • Switchback Staircase • D-02 Civic Bot 'Sweep #0812' & Residents",
    ),
    (
        "cam_03_open_side_rooms_and_puddle_substation",
        "CAM 03 — OPEN-DOORWAY SIDE ROOMS & D-03 SCIENCE BOT ('QUASAR / KELVIN #0204') BAY",
        "Unobstructed 2.2m Open Portal into Room 1B Bot Dock • D-03 Science Bot (#7B5CFF Violet Trim & Atom Emblem) • +5A Battery & Wire Spools",
    ),
    (
        "cam_04_ground_concourse_open_exit_and_faction_bots",
        "CAM 04 — GROUND-FLOOR CONCOURSE & OPEN SECTOR-4 PROMENADE EXIT THRESHOLD",
        "100% Open 2.6m Grand Exit Archway (No Blocking Doors) • D-01 Engineering Bot 'Sprocket #0419' • Residents Strolling Freely",
    ),
]

BOT_CANDS = [
    (
        "01",
        "Compact Cube-Compactor Chassis + Twin Tilting Binocular Lens Hoods",
        "75% WALL-E / 25% Johnny 5 • Squat Cubic Utility Box Torso • Tall Triangular Tracks • Wrap-Around Eyelid Lens Hoods",
    ),
    (
        "02",
        "The 'Johnny-V' — 68/32 Split-Mass Scissor-Spine & Eyebrow-Shutter Binoculars (HERO #02)",
        "Aegis-7 68/32 Split-Mass • 3-Bogie Tracks & Scissor Neck • Independent Eyebrow Shutters • Offset Super-Wire Spool & 3-Finger Grippers",
    ),
    (
        "03",
        "Wide-Stance Quad-Bogie Tracked Base + Telescoping Periscope Binoculars",
        "Mars Rover × Short Circuit Loader • 0.76m Wide 4-Bogie Track Base • Elevating Periscope Column • Rectangular Rangefinder Optics",
    ),
    (
        "04",
        "Rounded Industrial Roll-Cage Torso + Dual Servo-Flap Camera Visor",
        "Cylindrical Pressure Belly in Tubular Steel Roll-Cage • Oversized Macro-Lenses in Oval Guard • Dual Rear Battery Canisters",
    ),
    (
        "05",
        "Tri-Track Articulated Stair-Climber + Split Asymmetric Zoom/Wide Optical Eyes",
        "Rotating 3-Sprocket Triangular Stair-Climbing Bogie Clusters • Asymmetric Wide/Telephoto Eyes • Gull-Wing Eyebrow Shutters",
    ),
]

LIVERY_VIEWS = [
    (
        "johnny5_livery_01_sprocket",
        "emblem_district_01_engineering.png",
        "D-01 // ENGINEERING — 'SPROCKET #0419' (COMMS, PLUMBING, ELECTRICITY, COOLANT, DOCKING)",
        "88% Universal Cylinder Alabaster (#D8DEE4) & Slate (#2A3038) Hull • 12% Safety Amber (#E89B2D) Trim • Hex-Gear & Power-Bolt Emblem",
    ),
    (
        "johnny5_livery_02_sweep",
        "emblem_district_02_civic.png",
        "D-02 // CIVIC — 'SWEEP #0812' (COMMUTERS, LIFE SUPPORT, SANITATION, MEDICAL, GOVT, REC)",
        "88% Universal Cylinder Alabaster (#D8DEE4) & Slate (#2A3038) Hull • 12% Civic Cyan-Teal (#38B8C8) Trim • Orbital Ring & Medical-Star Emblem",
    ),
    (
        "johnny5_livery_03_puddle",
        "emblem_district_03_science.png",
        "D-03 // SCIENCE — 'QUASAR / KELVIN #0204' (LABS, EXPERIMENTS, NEW TECH, SPACE OBSERVATION)",
        "88% Universal Cylinder Alabaster (#D8DEE4) & Steel (#707A84) Hull • 12% Science Violet-Indigo (#7B5CFF) Trim • Atom-Lattice & Star Emblem",
    ),
    (
        "johnny5_livery_04_clover",
        "emblem_district_04_agri.png",
        "D-04 // AGRI — 'CLOVER #0631' (FOOD PROD, BIOSPHERE, ATMOSPHERE, HYDROSPHERE, VET/FAUNA)",
        "88% Universal Cylinder Alabaster (#D8DEE4) & Slate (#2A3038) Hull • 12% Biosphere Emerald (#3BA868) Trim • Leaf-Hex & Hydro-Wave Emblem",
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


def get_bot_stats():
    stats = {}
    mp = "./assets/glb/preface_multifloor_and_johnny5_manifest.json"
    if os.path.exists(mp):
        try:
            with open(mp, "r") as f:
                data = json.load(f)
            for it in data.get("johnny5_candidates_5", []):
                fn = os.path.basename(it.get("filepath", ""))
                stats[fn] = it
        except Exception:
            pass
    return stats


def mirror_science_livery_portraits():
    for d in BOT_OUT_DIRS:
        src = os.path.join(d, "johnny5_livery_03_puddle.png")
        if os.path.exists(src):
            for alias in [
                "utility_bot_r2_05_livery_03_puddle.png",
                "utility_bot_r2_05_livery_03_science.png",
                "utility_bot_r2_05_livery_03_kelvin.png",
                "utility_bot_r2_05_livery_03_quasar.png",
                "utility_bot_r2_05_livery_03_kelvin_science.png",
                "johnny5_livery_03_science.png",
                "johnny5_livery_03_kelvin.png",
                "johnny5_livery_03_quasar.png",
            ]:
                dst = os.path.join(d, alias)
                if os.path.abspath(src) != os.path.abspath(dst):
                    shutil.copyfile(src, dst)


def compose_open_residential_sheet():
    src_dir = RES_OUT_DIRS[0]
    for fname, _, _ in RES_VIEWS:
        if not os.path.exists(os.path.join(src_dir, f"{fname}.png")):
            return False

    canvas_w, canvas_h = 1920, 1080
    header_h = 84
    pad = 16
    cols, rows = 2, 2

    cell_w = (canvas_w - pad * (cols + 1)) // cols
    cell_h = (canvas_h - header_h - pad * (rows + 1)) // rows
    footer_h = 54
    img_h = cell_h - footer_h

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
        "CYLINDER HAB-7 — OPEN-DOORWAY 2-STORY PLAYABLE RESIDENTIAL BUILDING WALKTHROUGH",
        fill=(242, 246, 255),
        font=font_title,
    )
    draw.text(
        (pad, 50),
        "100% Open Portals (Zero Blocking Doors & No Puzzle UI) • #04 Neural Smart-Sleeve & 4 Canonical Department #05 Hammerhead Robots (D-01..D-04)",
        fill=(255, 209, 102),
        font=font_sub,
    )

    for idx, (fname, ctitle, cdesc) in enumerate(RES_VIEWS):
        r, c = idx // cols, idx % cols
        x0 = pad + c * (cell_w + pad)
        y0 = header_h + pad + r * (cell_h + pad)

        border_col = (255, 183, 3) if idx in (0, 1) else (0, 210, 245)
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
            fill=(255, 209, 102) if idx in (0, 1) else (88, 224, 255),
            font=font_card_desc,
        )

    out_names = [
        "preface_open_residential_building_showcase_sheet.png",
        "preface_playable_residential_showcase_sheet.png",
        "preface_residential_sector_showcase_sheet.png",
    ]
    for d in RES_OUT_DIRS:
        os.makedirs(d, exist_ok=True)
        for oname in out_names:
            out_p = os.path.join(d, oname)
            sheet.save(out_p, "PNG", compress_level=4)
            print(f"[OpenResidentialSheet] Saved {out_p} ({canvas_w}x{canvas_h})")
    return True


def compose_johnny5_voting_sheet():
    src_dir = BOT_OUT_DIRS[0]
    for num_str, _, _ in BOT_CANDS:
        if not os.path.exists(os.path.join(src_dir, f"char_bot_johnny5_r1_{num_str}.png")):
            return False

    stats_map = get_bot_stats()
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
    draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(255, 183, 3), width=3)
    draw.text(
        (pad, 20),
        "CYLINDER HAB-7 — EXPRESSIVE WALL-E × JOHNNY-5 UTILITY ROBOT (5-CHOICE TEST)",
        fill=(242, 245, 250),
        font=font_title,
    )
    draw.text(
        (pad, 64),
        "Zero Star Wars Tropes • Caterpillar Tracks, Scissor Neck, Binocular Camera Eyes & Eyebrow Shutters • 4 Faction Liveries • Vote 01–05",
        fill=(255, 209, 102),
        font=font_sub,
    )

    for idx, (num_str, ctitle, cdesc) in enumerate(BOT_CANDS):
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

        img_path = os.path.join(src_dir, f"char_bot_johnny5_r1_{num_str}.png")
        im = Image.open(img_path).convert("RGB").resize((cell_w, cell_img_h), Image.Resampling.LANCZOS)
        sheet.paste(im, (x0, y0))

        draw.rounded_rectangle(
            [x0 + 12, y0 + 12, x0 + 68, y0 + 50],
            radius=6,
            fill=(255, 183, 3) if is_hero else (0, 210, 245),
        )
        draw.text((x0 + 23, y0 + 17), num_str, fill=(10, 14, 20), font=font_badge)

        glb_fn = f"char_bot_johnny5_r1_{num_str}.glb"
        st = stats_map.get(glb_fn, {})
        tris = st.get("triangles", st.get("tris", 0))
        stat_txt = f"{glb_fn} | {tris:,} Tris" if tris else f"{glb_fn} | 12+ Nodes"
        draw.rounded_rectangle([x0 + cell_w - 355, y0 + 12, x0 + cell_w - 12, y0 + 44], radius=6, fill=(14, 18, 25))
        draw.text(
            (x0 + cell_w - 343, y0 + 19),
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
            "12+ Articulated Nodes + Embedded Animations (IdleCurious, TrackRoll, GreetAndPoint) • min_y = 0.000m",
            fill=(155, 175, 198),
            font=font_card_desc,
        )

    out_names = [
        "johnny5_bot_round1_voting_sheet.png",
        "utility_bot_johnny5_round1_voting_sheet.png",
        "char_bot_johnny5_round1_voting_sheet.png",
    ]
    for d in BOT_OUT_DIRS:
        os.makedirs(d, exist_ok=True)
        for oname in out_names:
            out_p = os.path.join(d, oname)
            sheet.save(out_p, "PNG", compress_level=4)
            print(f"[Johnny5VotingSheet] Saved {out_p} ({canvas_w}x{canvas_h})")
    return True


def compose_johnny5_livery_sheet():
    src_dir = BOT_OUT_DIRS[0]
    for fname, _, _, _ in LIVERY_VIEWS:
        if not os.path.exists(os.path.join(src_dir, f"{fname}.png")):
            return False

    canvas_w, canvas_h = 1920, 1080
    header_h = 84
    pad = 16
    cols, rows = 2, 2

    cell_w = (canvas_w - pad * (cols + 1)) // cols
    cell_h = (canvas_h - header_h - pad * (rows + 1)) // rows
    footer_h = 54
    img_h = cell_h - footer_h

    sheet = Image.new("RGB", (canvas_w, canvas_h), (10, 14, 20))
    draw = ImageDraw.Draw(sheet)

    font_title = load_font(20, bold=True)
    font_sub = load_font(13, bold=False)
    font_inset = load_font(11, bold=True)
    font_card_title = load_font(13, bold=True)
    font_card_desc = load_font(11, bold=False)

    draw.rectangle([0, 0, canvas_w, header_h], fill=(16, 22, 32))
    draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(255, 183, 3), width=3)
    draw.text(
        (pad, 14),
        "CYLINDER HAB-7 — WINNER #05 HAMMERHEAD ROBOT: 4 CANONICAL DEPARTMENTS & DISTRICT EMBLEMS",
        fill=(242, 246, 255),
        font=font_title,
    )
    draw.text(
        (pad, 50),
        "88% Universal Cylinder Palette (#D8DEE4 Titanium Alabaster / #2A3038 Slate / #707A84 Steel) + 12% Sparing Department Accents (D-01 Eng, D-02 Civic, D-03 Science, D-04 Agri)",
        fill=(255, 209, 102),
        font=font_sub,
    )

    border_cols = [(232, 155, 45), (56, 184, 200), (138, 114, 255), (59, 168, 104)]
    emblem_codes = ["D-01 // ENG EMBLEM", "D-02 // CIVIC EMBLEM", "D-03 // SCIENCE EMBLEM", "D-04 // AGRI EMBLEM"]

    for idx, (fname, emb_fn, ctitle, cdesc) in enumerate(LIVERY_VIEWS):
        r, c = idx // cols, idx % cols
        x0 = pad + c * (cell_w + pad)
        y0 = header_h + pad + r * (cell_h + pad)

        bcol = border_cols[idx]
        draw.rounded_rectangle(
            [x0 - 2, y0 - 2, x0 + cell_w + 2, y0 + cell_h + 2],
            radius=8,
            fill=(20, 26, 36),
            outline=bcol,
            width=2,
        )

        im_path = os.path.join(src_dir, f"{fname}.png")
        im = Image.open(im_path).convert("RGB").resize((cell_w, img_h), Image.Resampling.LANCZOS)
        sheet.paste(im, (x0, y0))

        # Paste crisp Department & City District Zoning Emblem Badge Inset in Top-Right of each panel!
        emb_p = os.path.join("./assets/textures/emblems", emb_fn)
        if os.path.exists(emb_p):
            ew, eh = 136, 136
            ex0 = x0 + cell_w - ew - 14
            ey0 = y0 + 32
            draw.rounded_rectangle(
                [ex0 - 4, ey0 - 22, ex0 + ew + 4, ey0 + eh + 4],
                radius=6,
                fill=(14, 18, 26),
                outline=bcol,
                width=2,
            )
            e_im = Image.open(emb_p).convert("RGBA")
            bg = Image.new("RGBA", e_im.size, (18, 23, 32, 255))
            e_comp = Image.alpha_composite(bg, e_im).convert("RGB").resize((ew, eh), Image.Resampling.LANCZOS)
            sheet.paste(e_comp, (ex0, ey0))
            draw.text((ex0 + 4, ey0 - 18), emblem_codes[idx], fill=bcol, font=font_inset)

        fy0 = y0 + img_h
        draw.rectangle([x0, fy0, x0 + cell_w, y0 + cell_h], fill=(14, 18, 26))
        draw.text((x0 + 12, fy0 + 7), ctitle, fill=(242, 246, 255), font=font_card_title)
        draw.text((x0 + 12, fy0 + 29), cdesc, fill=bcol, font=font_card_desc)

    out_names = [
        "utility_bot_r2_05_universal_livery_and_emblems_sheet.png",
        "utility_bot_r2_05_faction_livery_showcase_sheet.png",
        "johnny5_bot_faction_livery_showcase_sheet.png",
        "utility_bot_johnny5_faction_livery_sheet.png",
    ]
    for d in BOT_OUT_DIRS:
        os.makedirs(d, exist_ok=True)
        for oname in out_names:
            out_p = os.path.join(d, oname)
            sheet.save(out_p, "PNG", compress_level=4)
            print(f"[Johnny5LiverySheet] Saved {out_p} ({canvas_w}x{canvas_h})")
    return True


if __name__ == "__main__":
    mirror_science_livery_portraits()
    compose_open_residential_sheet()
    compose_johnny5_voting_sheet()
    compose_johnny5_livery_sheet()
