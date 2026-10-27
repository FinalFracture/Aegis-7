#!/usr/bin/env python3
"""
Composes:
1. 5-Character Close-Up Headshot Portrait Sheet (`character_crew_headshots_sheet.png`, `char_crew_headshots_sheet.png`, `character_headshots_showcase_sheet.png`)
2. 5-Candidate Aegis-7 Crew Character Voting Sheet (`character_crew_round1_voting_sheet.png` + aliases)
3. 6-Panel WalkCycle Keyframe & In-Cylinder Promenade Showcase Sheet (`character_walk_cycle_showcase_sheet.png` + aliases)
"""
import os
import json
from PIL import Image, ImageDraw, ImageFont

OUT_DIRS = [
    "./godot/renders/character",
    "./godot/renders/character/char_crew_round1",
    "./godot/renders/characters",
    "./assets/renders/character",
    "./assets/renders/character/char_crew_round1",
    "./assets/renders/characters",
]

HEADSHOT_CANDS = [
    (
        "01",
        "Lt. Marcus Vance-Lin — Flight-Suit Officer",
        "Warm Bronze Skin (#C68B63) • Hazel Irises • Dark Espresso Crew Cut • Retracted Flip-Up Flight Visor & Cobalt/Cyan Collar",
        "Headgear: Retracted Flip-Up Flight Crown • Dual-Ear Comms Pods • Symmetrical Aerospace-White Gorget",
    ),
    (
        "02",
        "Cmdr. Kaelen Rostov — Aegis-7 Commander (HERO #02)",
        "Warm Olive Skin (#D49E7A) • Trimmed Charcoal Beard & Silver Temple Streaks • Cyan AR Targeting Monocle & Cheek Scar",
        "Headgear: 65/35 Split Open Half-Cowl & Left-Eye AR Monocle • Signal-Orange EVA Strap & Right-Shoulder Camera Gimbal",
    ),
    (
        "03",
        "Chief Eng. Tarek Mensah — Heavy EVA Engineer",
        "Deep Rich Umber Skin (#6E422C) • Amber-Brown Irises • Textured Braided Hair Rows & Square-Jaw Chin Goatee",
        "Headgear: Open-Front Caterpillar-Amber (#FFB703) Exo-Roll-Cage Frame • Forehead LED Floodlamp & Jaw Bone-Mic",
    ),
    (
        "04",
        "Dr. Soren Sato — Bio-Med Recon Specialist",
        "Pale Warm Ivory Skin (#F0C8B0) • Emerald Irises (#34B276) • Asymmetric Platinum-Silver & Emerald-Tipped Angled Bob",
        "Headgear: Visorless Emerald/UV-Violet Neural-Telemetry Headband • Frameless Holographic Diagnostic Glasses",
    ),
    (
        "05",
        "Spec-Ops Vesper Kade — Tactical Recon",
        "Sunlit Tan Skin (#B98360) • Steel-Grey Irises • Buzzed Undercut Mohawk Crest, Left Cheek Scar & Amber Temple Implant",
        "Headgear: Faceted Stealth Carbon-Slate Jaw Rebreather Guard • Narrow Wrap-Around Amber/Cyan Tactical Optic Strip",
    ),
]

CANDS = [
    (
        "01",
        "Lt. Marcus Vance-Lin — Flight-Suit Officer",
        "Warm Bronze Complexion & Espresso Crew Cut • Retracted Flip-Up Visor Crown • Symmetrical Aerospace-White Cuirass",
    ),
    (
        "02",
        "Cmdr. Kaelen Rostov — Dual-Zone Split Commander Rig",
        "Aegis-7 65/35 Split-Rig • Silver-Templed Hair, Beard & Cyan AR Monocle • Shoulder Camera Gimbal & Wrist Holo-Projector",
    ),
    (
        "03",
        "Chief Eng. Tarek Mensah — Heavy EVA Exo-Engineer",
        "Deep Umber Complexion & Braids • Open Amber Roll-Cage Headgear • Twin Cylindrical MMU Nitrogen Thrusters",
    ),
    (
        "04",
        "Dr. Soren Sato — Bio-Med & Hydro-Biosphere Specialist",
        "Platinum/Emerald Bob & Holo-Glasses • Emerald & UV-Violet Bio-Isolation Trim • Translucent Cryo-Sample Pack",
    ),
    (
        "05",
        "Spec-Ops Vesper Kade — Tactical Recon Suit",
        "Mohawk Crest, Cheek Scar & Rebreather Jaw-Guard • Angular 45°-Faceted Stealth Armor & Dorsal Tachyon Fin",
    ),
]

WALK_PANELS = [
    (
        "walk_frame_01_t000",
        "01",
        "PHASE 0% (t = 0.00s) — LEFT HEEL STRIKE & RIGHT ARM FORWARD",
        "Left Thigh +24° Flexion • Right Leg -20° Extension • Right Arm +24° Counter-Swing • Hips Dip y = 0.896m",
    ),
    (
        "walk_frame_02_t025",
        "02",
        "PHASE 25% (t = 0.30s) — LEFT MID-STANCE & RIGHT KNEE PASSING LIFT",
        "Left Leg Weight-Bearing Stance • Right Knee +44° Foot-Clearance Flexion • Pelvis Peak y = 0.944m",
    ),
    (
        "walk_frame_03_t050",
        "03",
        "PHASE 50% (t = 0.60s) — RIGHT HEEL STRIKE & WRIST HOLO-PAD FORWARD",
        "Right Thigh +24° Flexion • Left Leg -20° Toe-Off • Left Forearm Wrist-Holo-Projector Raised Forward",
    ),
    (
        "walk_frame_04_t075",
        "04",
        "PHASE 75% (t = 0.90s) — RIGHT MID-STANCE & LEFT KNEE PASSING LIFT",
        "Right Leg Weight-Bearing Stance • Left Knee +44° Swing Lift • Thoracic Counter-Twist Stabilizing Gaze",
    ),
    (
        "walk_frame_05_rear_3q_rig",
        "05",
        "3/4 REAR VIEW — DUAL-ZONE SPLIT BACKPACK & CRYO-COOLANT COLUMN",
        "Left 65% Gunmetal O2 Pack & Vernier Nozzles • Right 35% Translucent Cyan/UV Cryo-Coolant Cell Column",
    ),
    (
        "walk_frame_06_promenade_insitu",
        "06",
        "IN-SITU WALK — STRIDING ALONG CYLINDER HAB-7 CIVIC PROMENADE",
        "#02 Commander Walking Past Wayfinding Kiosk, Specular Ring-River, Hab Spire #02 & Command Citadel #02",
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


def get_char_stats():
    stats = {}
    manifest_candidates = [
        "./assets/glb/character/character_aegis7_crew_manifest.json",
        "./assets/glb/character/char_crew_round1/character_aegis7_crew_manifest.json",
        "./assets/glb/character/char_crew_round1/char_crew_manifest.json",
        "./assets/glb/character/character_crew_manifest.json",
        "./assets/glb/character/char_01/char_01_manifest.json",
    ]
    for mp in manifest_candidates:
        if os.path.exists(mp):
            try:
                with open(mp, "r") as f:
                    data = json.load(f)
                items = data if isinstance(data, list) else data.get("candidates", data.get("models", []))
                for it in items:
                    fn = os.path.basename(it.get("filepath", ""))
                    stats[fn] = it
            except Exception:
                pass
    return stats


def compose_headshots_sheet():
    src_dir = OUT_DIRS[0]
    for num_str, _, _, _ in HEADSHOT_CANDS:
        if not os.path.exists(os.path.join(src_dir, f"char_crew_headshot_{num_str}.png")):
            return False

    stats_map = get_char_stats()
    cols, rows = 3, 2
    cell_w, cell_img_h, cell_footer_h = 880, 495, 92
    cell_h = cell_img_h + cell_footer_h
    pad, header_h = 22, 108

    canvas_w = pad + cols * (cell_w + pad)
    canvas_h = header_h + pad + rows * (cell_h + pad)

    sheet = Image.new("RGB", (canvas_w, canvas_h), (12, 15, 20))
    draw = ImageDraw.Draw(sheet)

    font_title = load_font(27, bold=True)
    font_sub = load_font(15, bold=False)
    font_badge = load_font(22, bold=True)
    font_tris = load_font(15, bold=True)
    font_card_title = load_font(17, bold=True)
    font_card_desc = load_font(13, bold=False)

    draw.rectangle([0, 0, canvas_w, header_h], fill=(18, 22, 30))
    draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(255, 183, 3), width=3)
    draw.text(
        (pad, 20),
        "CYLINDER HAB-7 — AEGIS-7 CREW CLOSE-UP PORTRAIT HEADSHOTS (5 DISTINCT INDIVIDUALS)",
        fill=(242, 245, 250),
        font=font_title,
    )
    draw.text(
        (pad, 64),
        "Unobstructed 3D Sculpted Faces, Eyes, Hair/Beards & Open/Retracted Headgear • 3-Point Rembrandt Studio Lighting (#FFF0DB Key + #66E8FF Rim)",
        fill=(255, 209, 102),
        font=font_sub,
    )

    for idx, (num_str, ctitle, cdesc1, cdesc2) in enumerate(HEADSHOT_CANDS):
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

        img_path = os.path.join(src_dir, f"char_crew_headshot_{num_str}.png")
        im = Image.open(img_path).convert("RGB").resize((cell_w, cell_img_h), Image.Resampling.LANCZOS)
        sheet.paste(im, (x0, y0))

        draw.rounded_rectangle([x0 + 12, y0 + 12, x0 + 68, y0 + 50], radius=6, fill=(255, 183, 3) if is_hero else (0, 210, 245))
        draw.text((x0 + 23, y0 + 17), num_str, fill=(10, 14, 20), font=font_badge)

        glb_fn = f"char_crew_r1_{num_str}.glb"
        st = stats_map.get(glb_fn, stats_map.get(f"character_crew_r1_{num_str}.glb", {}))
        tris = st.get("triangles", st.get("tris", 0))
        stat_txt = f"Headshot #{num_str} | {tris:,} Tris" if tris else f"Headshot #{num_str} | 3D Portrait"
        draw.rounded_rectangle([x0 + cell_w - 285, y0 + 12, x0 + cell_w - 12, y0 + 44], radius=6, fill=(14, 18, 25))
        draw.text((x0 + cell_w - 273, y0 + 19), stat_txt, fill=(255, 224, 150) if is_hero else (190, 225, 255), font=font_tris)

        fy0 = y0 + cell_img_h
        draw.rectangle([x0, fy0, x0 + cell_w, y0 + cell_h], fill=(16, 20, 27))
        draw.text((x0 + 14, fy0 + 10), f"#{num_str} — {ctitle}", fill=(240, 245, 255), font=font_card_title)
        draw.text((x0 + 14, fy0 + 38), cdesc1, fill=(255, 209, 102) if is_hero else (0, 215, 245), font=font_card_desc)
        draw.text((x0 + 14, fy0 + 62), cdesc2, fill=(165, 185, 208), font=font_card_desc)

    out_names = [
        "character_crew_headshots_sheet.png",
        "char_crew_headshots_sheet.png",
        "character_headshots_showcase_sheet.png",
    ]
    for d in OUT_DIRS:
        os.makedirs(d, exist_ok=True)
        for oname in out_names:
            out_p = os.path.join(d, oname)
            sheet.save(out_p, "PNG", compress_level=4)
            print(f"[CharacterHeadshotsSheet] Saved {out_p} ({canvas_w}x{canvas_h})")
    return True


def compose_voting_sheet():
    src_dir = OUT_DIRS[0]
    for num_str, _, _ in CANDS:
        if not os.path.exists(os.path.join(src_dir, f"char_crew_r1_{num_str}.png")):
            return False

    stats_map = get_char_stats()
    cols, rows = 3, 2
    cell_w, cell_img_h, cell_footer_h = 880, 495, 92
    cell_h = cell_img_h + cell_footer_h
    pad, header_h = 22, 108

    canvas_w = pad + cols * (cell_w + pad)
    canvas_h = header_h + pad + rows * (cell_h + pad)

    sheet = Image.new("RGB", (canvas_w, canvas_h), (12, 15, 20))
    draw = ImageDraw.Draw(sheet)

    font_title = load_font(27, bold=True)
    font_sub = load_font(15, bold=False)
    font_badge = load_font(22, bold=True)
    font_tris = load_font(15, bold=True)
    font_card_title = load_font(17, bold=True)
    font_card_desc = load_font(13, bold=False)

    draw.rectangle([0, 0, canvas_w, header_h], fill=(18, 22, 30))
    draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(255, 183, 3), width=3)
    draw.text(
        (pad, 20),
        "CYLINDER HAB-7 — RIGGED AEGIS-7 CREW CHARACTER & WALK CYCLE (5-CHOICE TEST)",
        fill=(242, 245, 250),
        font=font_title,
    )
    draw.text(
        (pad, 64),
        "1.80m Humanoid Rig • 5 Distinct Faces, Hair & Open Headgear • 1.20s Biomechanical WalkCycle • Golden-Hour & Cyan Rim Lighting",
        fill=(255, 209, 102),
        font=font_sub,
    )

    for idx, (num_str, ctitle, cdesc) in enumerate(CANDS):
        r, c = idx // cols, idx % cols
        if r == 1:
            row2_w = 2 * cell_w + pad
            start_x = (canvas_w - row2_w) // 2
            x0 = start_x + c * (cell_w + pad)
        else:
            x0 = pad + c * (cell_w + pad)
        y0 = header_h + pad + r * (cell_h + pad)

        is_hero = num_str == "02"
        outline_col = (255, 183, 3) if is_hero else (48, 72, 96)
        draw.rounded_rectangle(
            [x0 - 2, y0 - 2, x0 + cell_w + 2, y0 + cell_h + 2],
            radius=10,
            fill=(22, 27, 36),
            outline=outline_col,
            width=3 if is_hero else 2,
        )

        img_path = os.path.join(src_dir, f"char_crew_r1_{num_str}.png")
        im = Image.open(img_path).convert("RGB").resize((cell_w, cell_img_h), Image.Resampling.LANCZOS)
        sheet.paste(im, (x0, y0))

        draw.rounded_rectangle([x0 + 12, y0 + 12, x0 + 68, y0 + 50], radius=6, fill=(255, 183, 3) if is_hero else (0, 210, 245))
        draw.text((x0 + 23, y0 + 17), num_str, fill=(10, 14, 20), font=font_badge)

        glb_fn = f"char_crew_r1_{num_str}.glb"
        st = stats_map.get(glb_fn, stats_map.get(f"character_crew_r1_{num_str}.glb", {}))
        tris = st.get("triangles", st.get("tris", 0))
        stat_txt = f"{glb_fn} | {tris:,} Tris" if tris else f"{glb_fn} | Rigged + WalkCycle"
        draw.rounded_rectangle([x0 + cell_w - 318, y0 + 12, x0 + cell_w - 12, y0 + 44], radius=6, fill=(14, 18, 25))
        draw.text((x0 + cell_w - 306, y0 + 19), stat_txt, fill=(255, 224, 150) if is_hero else (190, 225, 255), font=font_tris)

        fy0 = y0 + cell_img_h
        draw.rectangle([x0, fy0, x0 + cell_w, y0 + cell_h], fill=(16, 20, 27))
        draw.text((x0 + 14, fy0 + 10), f"#{num_str} — {ctitle}", fill=(240, 245, 255), font=font_card_title)
        draw.text((x0 + 14, fy0 + 38), cdesc, fill=(255, 209, 102) if is_hero else (0, 215, 245), font=font_card_desc)
        draw.text(
            (x0 + 14, fy0 + 62),
            "Standing Height: 1.80m (min_y = 0.000m) • 15-Node Hierarchy + 1.20s WalkCycle Animation",
            fill=(155, 175, 198),
            font=font_card_desc,
        )

    out_names = [
        "character_crew_round1_voting_sheet.png",
        "char_crew_round1_voting_sheet.png",
    ]
    for d in OUT_DIRS:
        os.makedirs(d, exist_ok=True)
        for oname in out_names:
            out_p = os.path.join(d, oname)
            sheet.save(out_p, "PNG", compress_level=4)
            print(f"[CharacterVotingSheet] Saved {out_p} ({canvas_w}x{canvas_h})")
    return True


def compose_walk_cycle_sheet():
    src_dir = OUT_DIRS[0]
    for fname, _, _, _ in WALK_PANELS:
        if not os.path.exists(os.path.join(src_dir, f"{fname}.png")):
            return False

    cols, rows = 3, 2
    cell_w, cell_img_h, cell_footer_h = 880, 495, 88
    cell_h = cell_img_h + cell_footer_h
    pad, header_h = 22, 108

    canvas_w = pad + cols * (cell_w + pad)
    canvas_h = header_h + pad + rows * (cell_h + pad)

    sheet = Image.new("RGB", (canvas_w, canvas_h), (10, 14, 20))
    draw = ImageDraw.Draw(sheet)

    font_title = load_font(26, bold=True)
    font_sub = load_font(15, bold=False)
    font_badge = load_font(20, bold=True)
    font_card_title = load_font(16, bold=True)
    font_card_desc = load_font(13, bold=False)

    draw.rectangle([0, 0, canvas_w, header_h], fill=(16, 22, 32))
    draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(255, 183, 3), width=3)
    draw.text(
        (pad, 20),
        "CYLINDER HAB-7 — #02 CMDR. KAELEN ROSTOV WALK-CYCLE ANIMATION & PROMENADE SHOWCASE",
        fill=(245, 242, 235),
        font=font_title,
    )
    draw.text(
        (pad, 64),
        "4-Phase Biomechanical WalkCycle Keyframes (t = 0.00s, 0.30s, 0.60s, 0.90s) • 3/4 Rear Dual-Zone Backpack Rig • In-Situ Cylinder Hab-7 Promenade Walk",
        fill=(255, 209, 102),
        font=font_sub,
    )

    for idx, (fname, badge, ctitle, cdesc) in enumerate(WALK_PANELS):
        r, c = idx // cols, idx % cols
        x0 = pad + c * (cell_w + pad)
        y0 = header_h + pad + r * (cell_h + pad)

        outline_col = (255, 183, 3) if idx in (0, 5) else (0, 210, 245)
        draw.rounded_rectangle(
            [x0 - 2, y0 - 2, x0 + cell_w + 2, y0 + cell_h + 2],
            radius=10,
            fill=(20, 26, 36),
            outline=outline_col,
            width=2,
        )

        img_path = os.path.join(src_dir, f"{fname}.png")
        im = Image.open(img_path).convert("RGB").resize((cell_w, cell_img_h), Image.Resampling.LANCZOS)
        sheet.paste(im, (x0, y0))

        draw.rounded_rectangle([x0 + 12, y0 + 12, x0 + 64, y0 + 48], radius=6, fill=outline_col)
        draw.text((x0 + 22, y0 + 17), badge, fill=(10, 14, 20), font=font_badge)

        fy0 = y0 + cell_img_h
        draw.rectangle([x0, fy0, x0 + cell_w, y0 + cell_h], fill=(14, 18, 26))
        draw.text((x0 + 14, fy0 + 12), ctitle, fill=(242, 246, 255), font=font_card_title)
        draw.text((x0 + 14, fy0 + 44), cdesc, fill=(255, 209, 102) if idx in (0, 5) else (88, 224, 255), font=font_card_desc)

    out_names = [
        "character_walk_cycle_showcase_sheet.png",
        "char_crew_walk_cycle_sheet.png",
        "character_crew_walk_cycle_sheet.png",
    ]
    for d in OUT_DIRS:
        os.makedirs(d, exist_ok=True)
        for oname in out_names:
            out_p = os.path.join(d, oname)
            sheet.save(out_p, "PNG", compress_level=4)
            print(f"[CharacterWalkSheet] Saved {out_p} ({canvas_w}x{canvas_h})")
    return True


if __name__ == "__main__":
    compose_headshots_sheet()
    compose_voting_sheet()
    compose_walk_cycle_sheet()
