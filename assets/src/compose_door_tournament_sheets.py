#!/usr/bin/env python3
"""
Composes the 5 RFID Door Tournament 6-panel contact sheets (3 camera angles x CLOSED & OPEN states)
plus the master 5-candidate comparison overview sheet, then deletes all 30 temporary `_tmp_door_cand_*` PNGs.
"""
import os
import sys
import glob
from PIL import Image, ImageDraw, ImageFont

QA_DIR = "/workspace/game-project/godot/renders/qa"

CANDIDATES = [
    (
        1,
        "door_cand_01_biparting_bulkhead_3angles_closed_open.png",
        "CANDIDATE 01 // HEAVY BI-PARTING INDUSTRIAL BULKHEAD DOOR",
        "Recessed vertical weather-seal seam, beveled brushed-titanium leaves, 12 hex frame bolts, dual vertical LED telemetry strips",
    ),
    (
        2,
        "door_cand_02_vertical_blast_shutter_3angles_closed_open.png",
        "CANDIDATE 02 // VERTICAL COUNTERBALANCED BLAST-SHUTTER DOOR",
        "Upper 70% ribbed blast leaf + lower 30% threshold drop-plate, hydraulic guide columns, twin full-height RFID status bars",
    ),
    (
        3,
        "door_cand_03_asymmetric_pocket_airlock_3angles_closed_open.png",
        "CANDIDATE 03 // ASYMMETRIC POCKET-SLIDE AIRLOCK DOOR",
        "Single wide armored leaf sliding into +X wall pocket, narrow multi-layer viewport slit, pressure wheel, 3-chevron status array",
    ),
    (
        4,
        "door_cand_04_interlocking_chevron_3angles_closed_open.png",
        "CANDIDATE 04 // ANGLED INTERLOCKING CHEVRON BULKHEAD DOOR",
        "Center-split mitered sawtooth/chevron interlocking teeth, 45° corner gussets, glowing chevron seam indicators",
    ),
    (
        5,
        "door_cand_05_twintrack_ceramic_frame_3angles_closed_open.png",
        "CANDIDATE 05 // TWIN-TRACK RECESSED SECURITY FRAME DOOR",
        "Matte ceramic-titanium composite leaves, flush horizontal light-pipe header, dual vertical smoked-glass slits, micro-bevel seams",
    ),
]

ANGLE_LABELS = [
    (1, "ANGLE 1 // STRAIGHT-ON 1ST-PERSON APPROACH"),
    (2, "ANGLE 2 // 35° ARCHITECTURAL THREE-QUARTER OBLIQUE"),
    (3, "ANGLE 3 // CLOSE-UP SEAM, LATCH & RFID TELEMETRY"),
]


def load_font(size: int, bold: bool = True):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def compose_all() -> int:
    f_title = load_font(28, bold=True)
    f_sub = load_font(18, bold=False)
    f_badge = load_font(18, bold=True)

    tile_w, tile_h = 800, 450
    pad = 16
    header_h = 92
    row_banner_h = 38
    sheet_w = pad * 4 + tile_w * 3
    sheet_h = header_h + (row_banner_h + tile_h + pad) * 2 + pad

    overview_rows = []

    for cid, out_name, title, subtitle in CANDIDATES:
        sheet = Image.new("RGB", (sheet_w, sheet_h), (14, 18, 24))
        draw = ImageDraw.Draw(sheet)

        # Header banner
        draw.rectangle([0, 0, sheet_w, header_h], fill=(20, 26, 34))
        draw.rectangle([0, header_h - 3, sheet_w, header_h], fill=(46, 150, 178))
        draw.text((pad, 16), title, font=f_title, fill=(230, 240, 248))
        draw.text((pad, 54), subtitle, font=f_sub, fill=(158, 182, 200))

        for row_idx, (state_key, state_label, accent_rgb) in enumerate([
            ("closed", "STATE A: CLOSED [LOCKED — AMBER TELEMETRY 13.56 MHz]", (196, 125, 43)),
            ("open", "STATE B: OPEN [RFID UNLOCKED — EMERALD TELEMETRY // CLEAR PASSAGE]", (63, 175, 106)),
        ]):
            y_banner = header_h + pad + row_idx * (row_banner_h + tile_h + pad)
            draw.rectangle([pad, y_banner, sheet_w - pad, y_banner + row_banner_h - 4], fill=(24, 31, 40))
            draw.rectangle([pad, y_banner, pad + 6, y_banner + row_banner_h - 4], fill=accent_rgb)
            draw.text((pad + 16, y_banner + 6), state_label, font=f_badge, fill=accent_rgb)

            y_tile = y_banner + row_banner_h
            for col_idx, (ang_id, ang_title) in enumerate(ANGLE_LABELS):
                x_tile = pad + col_idx * (tile_w + pad)
                tmp_path = os.path.join(QA_DIR, f"_tmp_door_cand_{cid:02d}_ang{ang_id}_{state_key}.png")
                if os.path.exists(tmp_path):
                    im = Image.open(tmp_path).convert("RGB")
                    im_resized = im.resize((tile_w, tile_h), Image.Resampling.LANCZOS)
                    sheet.paste(im_resized, (x_tile, y_tile))
                else:
                    draw.rectangle([x_tile, y_tile, x_tile + tile_w, y_tile + tile_h], fill=(32, 24, 24))
                    draw.text((x_tile + 24, y_tile + 200), f"MISSING: {os.path.basename(tmp_path)}", font=f_badge, fill=(255, 90, 90))

                # Subtle border + top-left angle caption overlay
                draw.rectangle([x_tile, y_tile, x_tile + tile_w - 1, y_tile + tile_h - 1], outline=accent_rgb, width=2)
                draw.rectangle([x_tile + 2, y_tile + 2, x_tile + 470, y_tile + 32], fill=(12, 16, 22))
                draw.text((x_tile + 10, y_tile + 6), ang_title, font=f_sub, fill=(224, 234, 242))

        out_path = os.path.join(QA_DIR, out_name)
        sheet.save(out_path, "PNG", optimize=True)
        print(f"[DoorTournamentComposer] Saved 6-panel sheet: {out_path}")

        # Collect Angle 1 Closed, Angle 2 Closed, Angle 2 Open, Angle 3 Close-Up for the 5-candidate master overview
        overview_rows.append((cid, title, out_path))

    # Build master 5-candidate overview comparison sheet (5 rows = Candidates 01..05 x 4 cols = Ang1 Closed, Ang2 Closed, Ang3 Closeup Closed, Ang2 Open)
    ov_tile_w, ov_tile_h = 560, 315
    ov_pad = 14
    ov_hdr = 84
    ov_row_hdr = 34
    ov_w = ov_pad * 5 + ov_tile_w * 4
    ov_h = ov_hdr + (ov_row_hdr + ov_tile_h + ov_pad) * 5 + ov_pad
    ov_img = Image.new("RGB", (ov_w, ov_h), (12, 16, 22))
    ov_draw = ImageDraw.Draw(ov_img)
    ov_draw.rectangle([0, 0, ov_w, ov_hdr], fill=(20, 26, 34))
    ov_draw.rectangle([0, ov_hdr - 3, ov_w, ov_hdr], fill=(46, 150, 178))
    ov_draw.text((ov_pad, 14), "AEGIS-7 // 5-CANDIDATE SCI-FI RFID DOOR TOURNAMENT OVERVIEW ([t39u]-[t40u])", font=f_title, fill=(235, 242, 250))
    ov_draw.text((ov_pad, 50), "Columns: (1) Angle 1 Front [Closed]  |  (2) Angle 2 35° Oblique [Closed]  |  (3) Angle 3 Seam & RFID Detail [Closed]  |  (4) Angle 2 35° Oblique [Open / RFID Unlocked]", font=f_sub, fill=(160, 185, 205))

    cols_spec = [
        (1, "closed", "ANG 1 FRONT [CLOSED]", (196, 125, 43)),
        (2, "closed", "ANG 2 35° OBLIQUE [CLOSED]", (196, 125, 43)),
        (3, "closed", "ANG 3 RFID SEAM DETAIL [CLOSED]", (196, 125, 43)),
        (2, "open", "ANG 2 35° OBLIQUE [OPEN]", (63, 175, 106)),
    ]
    for r_i, (cid, out_name, title, subtitle) in enumerate(CANDIDATES):
        y_b = ov_hdr + ov_pad + r_i * (ov_row_hdr + ov_tile_h + ov_pad)
        ov_draw.rectangle([ov_pad, y_b, ov_w - ov_pad, y_b + ov_row_hdr - 4], fill=(22, 29, 38))
        ov_draw.text((ov_pad + 12, y_b + 5), title, font=f_badge, fill=(225, 236, 245))
        y_t = y_b + ov_row_hdr
        for c_i, (ang_id, st_key, cap, acc) in enumerate(cols_spec):
            x_t = ov_pad + c_i * (ov_tile_w + ov_pad)
            tp = os.path.join(QA_DIR, f"_tmp_door_cand_{cid:02d}_ang{ang_id}_{st_key}.png")
            if os.path.exists(tp):
                im = Image.open(tp).convert("RGB").resize((ov_tile_w, ov_tile_h), Image.Resampling.LANCZOS)
                ov_img.paste(im, (x_t, y_t))
            ov_draw.rectangle([x_t, y_t, x_t + ov_tile_w - 1, y_t + ov_tile_h - 1], outline=acc, width=2)
            ov_draw.rectangle([x_t + 2, y_t + 2, x_t + 320, y_t + 28], fill=(12, 16, 22))
            ov_draw.text((x_t + 8, y_t + 5), cap, font=f_sub, fill=acc)

    ov_out = os.path.join(QA_DIR, "door_tournament_all_5_candidates_overview.png")
    ov_img.save(ov_out, "PNG", optimize=True)
    print(f"[DoorTournamentComposer] Saved master overview: {ov_out}")

    # Clean up all 30 temporary raw angle files so zero repo bloat remains
    removed = 0
    for tmp_f in glob.glob(os.path.join(QA_DIR, "_tmp_door_cand_*.png")):
        try:
            os.remove(tmp_f)
            removed += 1
        except OSError:
            pass
    print(f"[DoorTournamentComposer] Cleaned up {removed} temporary _tmp_door_cand_*.png files.")
    return 0


if __name__ == "__main__":
    sys.exit(compose_all())
