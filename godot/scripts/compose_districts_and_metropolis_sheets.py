#!/usr/bin/env python3
"""
Composes the Multi-Camera Overview Sheets for:
- District I (district_01_sheet.png + district_01_residential_civic_sheet.png)
- District II (district_02_sheet.png + district_02_agri_research_sheet.png)
- District III (district_03_sheet.png + district_03_command_industrial_sheet.png)
- Grand 15-Building Metropolis (cylinder_hab7_metropolis_sheet.png + cylinder_hab7_metropolis_showcase_sheet.png)
Also saves exact camera filename aliases required by Sloane's spec (`metropolis_cam1_grand_overview.png`, etc.).
"""
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

SHEETS = [
    {
        "sub": "district_01",
        "out_names": ["district_01_sheet.png", "district_01_residential_civic_sheet.png"],
        "title": "CYLINDER HAB-7 — DISTRICT I: RESIDENTIAL & CIVIC TERRACE SECTOR (BLDG 01–05)",
        "subtitle": "Aegis-7 65/35 Split-Mass Winners • Hab Spire #02 • Mag-Lev Rotunda #02 • Culinary Atrium #02 • Trauma Center #02 • Celestial Dome #02",
        "layout": "3cam",
        "views": [
            ("cam_01_district_01_skyline_overview", "CAM 01 — DISTRICT I CIVIC BOULEVARD & SKYLINE OVERVIEW", "Buildings 01–05 Along the Elevated Mag-Lev Guideway & O'Neill Cylinder Arch Vista"),
            ("cam_02_hab_spire_and_transit_rotunda", "CAM 02 — HABITAT SPIRE #02, MAG-LEV ROTUNDA #02 & CULINARY ATRIUM #02", "Sky-Elevator Atrium Tower • Elevated Transit Concourse • UV-Violet Aeroponic Herb Tower"),
            ("cam_03_trauma_center_and_celestial_dome", "CAM 03 — TRAUMA MEDICAL COMPLEX #02 & CELESTIAL PROMENADE DOME #02", "UV-Sterile Cryo-Pharmacy Tower • Faceted Geodesic Stargazer Dome & Zero-G Ascent Tube"),
        ]
    },
    {
        "sub": "district_02",
        "out_names": ["district_02_sheet.png", "district_02_agri_research_sheet.png"],
        "title": "CYLINDER HAB-7 — DISTRICT II: AGRI-BIOSPHERE & RESEARCH TERRACE (BLDG 06–10)",
        "subtitle": "Aegis-7 65/35 Split-Mass Winners • Hydroponic Biodome #02 • Atmo Processor #02 • Astrometry Lab #02 • Aquifer Cascade #02 • Cryo Seed Vault #02",
        "layout": "3cam",
        "views": [
            ("cam_01_district_02_biosphere_overview", "CAM 01 — DISTRICT II AGRI-BIOSPHERE & HYDRO-CANAL OVERVIEW", "Buildings 06–10 Framing the Illuminated Hydro-Reclamation Canal & Botanical Terraces"),
            ("cam_02_biodome_and_atmo_processor", "CAM 02 — HYDROPONIC BIODOME #02, ATMO PROCESSOR #02 & ASTROMETRY #02", "O2 Algae Scrubber Tower • Cryo-O2 Distillation Column • Rotating Deep-Space Telemetry Dish"),
            ("cam_03_aquifer_station_and_seed_vault", "CAM 03 — AQUIFER PUMPING PLANT #02 & CRYO-GENETICS SEED VAULT #02", "Illuminated Cyan Water-Column Tower • Armored Gene Archive & Translucent Cryo-Helix Spire"),
        ]
    },
    {
        "sub": "district_03",
        "out_names": ["district_03_sheet.png", "district_03_command_industrial_sheet.png"],
        "title": "CYLINDER HAB-7 — DISTRICT III: COMMAND CITADEL, FUSION POWER & CARGO PORT (BLDG 11–15)",
        "subtitle": "Aegis-7 65/35 Split-Mass Winners • Command Citadel #02 • Fusion Reactor #02 • Cargo Port #02 • EVA Docking Pinnacle #02 • Solar Pylon #02",
        "layout": "3cam",
        "views": [
            ("cam_01_district_03_command_port_overview", "CAM 01 — DISTRICT III COMMAND CITADEL & INDUSTRIAL PORT OVERVIEW", "Central Command Citadel #02 Flanked by Fusion Reactor #02, Cargo Port #02, EVA Pinnacle #02 & Solar Pylon #02"),
            ("cam_02_fusion_reactor_and_cargo_port", "CAM 02 — D-HE3 FUSION REACTOR #02, CARGO PORT #02 & COMMAND CITADEL #02", "5-Coil Plasma Pinch Tower • Intermodal ISO Container & Drone Gantry • Command Flight-Director Tower"),
            ("cam_03_eva_pinnacle_and_solar_pylon", "CAM 03 — AXIAL EVA DOCKING PINNACLE #02 & SOLAR/SHIELD PYLON #02", "Umbilical Shuttle Docking Tower • Gyroscopic Magnetic-Shield Field-Ring Pylon • O'Neill Cylinder Vista"),
        ]
    },
    {
        "sub": "district_04",
        "out_names": ["district_04_sheet.png", "district_04_shipyard_civic_sheet.png"],
        "title": "CYLINDER HAB-7 — DISTRICT IV: SHIPYARD, ARENA, MUSEUM, REFINERY & DEFENSE (BLDG 16–20 + PROPS 01–05)",
        "subtitle": "Aegis-7 65/35 Split-Mass Winners • Shipyard Drydock #02 • Coriolis Arena #02 • Holo Museum #02 • Refinery #02 • Defense Bastion #02",
        "layout": "3cam",
        "views": [
            ("cam_01_district_04_shipyard_civic_overview", "CAM 01 — DISTRICT IV SHIPYARD, ARENA, MUSEUM & DEFENSE OVERVIEW", "Buildings 16–20 & Exterior Sci-Fi Set Props 01–05 Along the Orbital Promenade"),
            ("cam_02_shipyard_drydock_and_coriolis_arena", "CAM 02 — ZERO-G SHIPYARD DRYDOCK #02, CORIOLIS ARENA #02 & HOLO MUSEUM #02", "Micro-Shuttle Drydock Tower • 4-Ring Centrifuge Tower • Earth-Biosphere Holo-Orrery"),
            ("cam_03_synth_refinery_defense_bastion_and_vtol_pad", "CAM 03 — PROTEIN REFINERY #02, LASER DEFENSE BASTION #02 & VTOL PAD #02", "Botanical Distillation Column • Tachyon Beam-Relay Spire • Octagonal VTOL Med-Evac Pad #02"),
        ]
    },
    {
        "sub": "metropolis",
        "out_names": ["cylinder_hab7_metropolis_sheet.png", "cylinder_hab7_metropolis_showcase_sheet.png", "metropolis_sheet.png"],
        "title": "CYLINDER HAB-7 — GRAND 20-BUILDING O'NEILL CYLINDER METROPOLIS SHOWCASE",
        "subtitle": "All 20 Locked Aegis-7 Building Exteriors (Bldg 01–20) + 5 Exterior Sci-Fi Movie Props (Prop 01–05) United Across the Curved 800m × 400m Orbital Habitat Landscape",
        "layout": "4cam",
        "views": [
            ("cam_01_metropolis_grand_skyline", "CAM 01 — GRAND 20-BUILDING O'NEILL CYLINDER METROPOLIS SKYLINE", "All 3 Districts (15 Locked Aegis-7 Buildings) Spanning the Civic Boulevard, Hydro-Canal & Command Citadel"),
            ("cam_02_west_civic_and_biosphere_wing", "CAM 02 — WEST METROPOLIS: RESIDENTIAL SPIRE, TRANSIT HUB, BIODOME & FUSION CORE", "Buildings 01, 02, 03, 06, 07, 12 & 13 Along the Western Cylinder Curve"),
            ("cam_03_east_medical_aquifer_and_docking_wing", "CAM 03 — EAST METROPOLIS: TRAUMA CENTER, CELESTIAL DOME, AQUIFER & EVA PINNACLE", "Buildings 04, 05, 09, 10, 14 & 15 Along the Eastern Cylinder Curve"),
            ("cam_04_axial_boulevard_toward_command_citadel", "CAM 04 — LOW-ALTITUDE AXIAL PROMENADE TOWARD CENTRAL COMMAND CITADEL", "Street-Level Perspective Past Astrometry Lab #02 & Hydro-Canal Toward Command Citadel #02"),
        ]
    }
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


def compose_sheet(sc: dict):
    sub = sc["sub"]
    rdir = f"./godot/renders/buildings/{sub}"
    adir = f"./assets/renders/buildings/{sub}"
    for v in sc["views"]:
        if not os.path.exists(os.path.join(rdir, f"{v[0]}.png")):
            return False

    # Create Sloane's exact camera filename aliases for metropolis
    if sub == "metropolis":
        alias_map = {
            "cam_01_metropolis_grand_skyline.png": "metropolis_cam1_grand_overview.png",
            "cam_04_axial_boulevard_toward_command_citadel.png": "metropolis_cam2_boulevard_axis.png",
            "cam_02_west_civic_and_biosphere_wing.png": "metropolis_cam3_cylinder_horizon.png",
        }
        for d in [rdir, adir]:
            os.makedirs(d, exist_ok=True)
            for src_n, dst_n in alias_map.items():
                sp = os.path.join(d, src_n)
                dp = os.path.join(d, dst_n)
                if os.path.exists(sp):
                    shutil.copyfile(sp, dp)

    font_title = load_font(30, bold=True)
    font_sub = load_font(17, bold=False)
    font_card_title = load_font(19, bold=True)
    font_card_desc = load_font(15, bold=False)

    if sc["layout"] == "3cam":
        pad = 24
        header_h = 112
        top_w = 1960
        top_img_h = 840
        top_footer_h = 74
        top_h = top_img_h + top_footer_h

        bot_w = (top_w - pad) // 2
        bot_img_h = 544
        bot_footer_h = 74
        bot_h = bot_img_h + bot_footer_h

        canvas_w = pad * 2 + top_w
        canvas_h = header_h + pad + top_h + pad + bot_h + pad

        sheet = Image.new("RGB", (canvas_w, canvas_h), (12, 15, 20))
        draw = ImageDraw.Draw(sheet)

        draw.rectangle([0, 0, canvas_w, header_h], fill=(18, 22, 30))
        draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(0, 229, 255), width=3)
        draw.text((pad, 22), sc["title"], fill=(232, 242, 255), font=font_title)
        draw.text((pad, 68), sc["subtitle"], fill=(0, 215, 245), font=font_sub)

        v0 = sc["views"][0]
        x0, y0 = pad, header_h + pad
        draw.rounded_rectangle([x0 - 2, y0 - 2, x0 + top_w + 2, y0 + top_h + 2], radius=10, fill=(22, 27, 36), outline=(0, 229, 255), width=2)
        im0 = Image.open(os.path.join(rdir, f"{v0[0]}.png")).convert("RGB").resize((top_w, top_img_h), Image.Resampling.LANCZOS)
        sheet.paste(im0, (x0, y0))
        fy0 = y0 + top_img_h
        draw.rectangle([x0, fy0, x0 + top_w, y0 + top_h], fill=(16, 20, 27))
        draw.text((x0 + 16, fy0 + 12), v0[1], fill=(235, 244, 255), font=font_card_title)
        draw.text((x0 + 16, fy0 + 42), v0[2], fill=(0, 215, 245), font=font_card_desc)

        for idx in range(2):
            v = sc["views"][idx + 1]
            bx = pad + idx * (bot_w + pad)
            by = header_h + pad + top_h + pad
            draw.rounded_rectangle([bx - 2, by - 2, bx + bot_w + 2, by + bot_h + 2], radius=10, fill=(22, 27, 36), outline=(48, 72, 96), width=2)
            im = Image.open(os.path.join(rdir, f"{v[0]}.png")).convert("RGB").resize((bot_w, bot_img_h), Image.Resampling.LANCZOS)
            sheet.paste(im, (bx, by))
            bfy = by + bot_img_h
            draw.rectangle([bx, bfy, bx + bot_w, by + bot_h], fill=(16, 20, 27))
            draw.text((bx + 16, bfy + 12), v[1], fill=(235, 244, 255), font=font_card_title)
            draw.text((bx + 16, bfy + 42), v[2], fill=(0, 215, 245), font=font_card_desc)
    else:
        # 2x2 grid for 4cam Metropolis
        cols, rows = 2, 2
        cell_w, cell_img_h, cell_footer_h = 1280, 720, 76
        cell_h = cell_img_h + cell_footer_h
        pad, header_h = 24, 112
        canvas_w = pad + cols * (cell_w + pad)
        canvas_h = header_h + pad + rows * (cell_h + pad)

        sheet = Image.new("RGB", (canvas_w, canvas_h), (12, 15, 20))
        draw = ImageDraw.Draw(sheet)

        draw.rectangle([0, 0, canvas_w, header_h], fill=(18, 22, 30))
        draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(0, 229, 255), width=3)
        draw.text((pad, 22), sc["title"], fill=(232, 242, 255), font=font_title)
        draw.text((pad, 68), sc["subtitle"], fill=(0, 215, 245), font=font_sub)

        for idx, v in enumerate(sc["views"]):
            r, c = idx // cols, idx % cols
            x0 = pad + c * (cell_w + pad)
            y0 = header_h + pad + r * (cell_h + pad)
            draw.rounded_rectangle([x0 - 2, y0 - 2, x0 + cell_w + 2, y0 + cell_h + 2], radius=10, fill=(22, 27, 36), outline=(0, 229, 255) if idx == 0 else (48, 72, 96), width=2)
            im = Image.open(os.path.join(rdir, f"{v[0]}.png")).convert("RGB").resize((cell_w, cell_img_h), Image.Resampling.LANCZOS)
            sheet.paste(im, (x0, y0))
            fy0 = y0 + cell_img_h
            draw.rectangle([x0, fy0, x0 + cell_w, y0 + cell_h], fill=(16, 20, 27))
            draw.text((x0 + 16, fy0 + 12), v[1], fill=(235, 244, 255), font=font_card_title)
            draw.text((x0 + 16, fy0 + 42), v[2], fill=(0, 215, 245), font=font_card_desc)

    for d in [rdir, adir]:
        os.makedirs(d, exist_ok=True)
        for sname in sc["out_names"]:
            out_p = os.path.join(d, sname)
            sheet.save(out_p, "PNG", compress_level=4)
            print(f"[DistrictSheet] Saved {out_p} ({canvas_w}x{canvas_h})")
    return True


if __name__ == "__main__":
    for sc in SHEETS:
        compose_sheet(sc)
