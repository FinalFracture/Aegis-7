#!/usr/bin/env python3
"""
Composes the Multi-Camera Overview Sheets for Room 02 through Room 10 (Aegis-7 Standard).
Saves both `<scene_name>_sheet.png` and `room_<num>_sheet.png` (and for room_05 also `room_05_eva_airlock_sheet.png`)
in `./godot/renders/rooms/room_XX/` and `./assets/renders/rooms/room_XX/`.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOM_SHEETS = [
    {
        "num": "02",
        "sheet_names": ["room_02_transit_corridor_sheet.png", "room_02_sheet.png"],
        "title": "CYLINDER HAB-7 — ROOM 02: ORBITAL SECTOR TRANSIT CORRIDOR & AIRLOCK HUB",
        "subtitle": "3.6m × 12.0m × 3.2m Aegis-7 Ring Corridor • Dual-Zone Airlock Portals #02 • 6-Bay West O'Neill Cylinder Window Gallery",
        "views": [
            ("cam_01_axial_corridor_perspective", "CAM 01 — AXIAL CORRIDOR PERSPECTIVE", "7 Repeating 45° Octagonal Titanium Ribs • North Airlock Checkpoint #02 • West Cylinder Gallery"),
            ("cam_02_window_gallery_and_east_bulkhead", "CAM 02 — EAST STATEROOM ENTRY & UTILITY BULKHEAD", "Cabin 01 Entry Hatch • Climate & O2 Panel #02 • Recessed EVA Suit Locker #02"),
            ("cam_03_airlock_checkpoint_closeup", "CAM 03 — NORTH SECTOR AIRLOCK CHECKPOINT CLOSEUP", "Parted Blast Doors & 3D Dog-Latch Teeth • OLED Pressure Status • Signal-Orange Override Wheel"),
        ]
    },
    {
        "num": "03",
        "sheet_names": ["room_03_mess_galley_sheet.png", "room_03_sheet.png"],
        "title": "CYLINDER HAB-7 — ROOM 03: CREW MESS HALL & SYNTHESIZER GALLEY",
        "subtitle": "7.0m × 8.0m × 3.2m Aegis-7 Mess Hall • Twin Galley Synthesizer & Herb Towers #02 • Cantilevered Booths • North Cylinder Viewport",
        "views": [
            ("cam_01_mess_hall_overview", "CAM 01 — MESS HALL WIDE OVERVIEW", "East Twin Galley Synthesizer Bank • West Cantilevered Booths • North O'Neill Cylinder Viewport"),
            ("cam_02_galley_synthesizer_line", "CAM 02 — DUAL RATION & HERB SYNTHESIZER LINE", "Galley Synthesizer #02 × 2 • Translucent Thermal Ovens • UV-Violet Living Herb Towers"),
            ("cam_03_dining_booths_and_viewport", "CAM 03 — CANTILEVERED DINING BOOTHS & VISTA", "Sculpted Brushed-Steel Tables • Orbital-Navy Flightpad Booths • O'Neill Cylinder Panorama"),
        ]
    },
    {
        "num": "04",
        "sheet_names": ["room_04_med_bay_sheet.png", "room_04_medbay_sheet.png", "room_04_sheet.png"],
        "title": "CYLINDER HAB-7 — ROOM 04: MED-BAY & BIOMONITOR TRIAGE SUITE",
        "subtitle": "6.5m × 7.5m × 3.2m Surgical Suite • Centerpiece Surgical Autodoc & UV Pharmacy #02 • Twin Biomonitor Pods • Deep-Space Viewport",
        "views": [
            ("cam_01_medbay_surgical_overview", "CAM 01 — MED-BAY SURGICAL SUITE OVERVIEW", "Centerpiece Surgical Autodoc #02 • North Deep-Space Viewport • West Recovery Pods & East Triage"),
            ("cam_02_autodoc_and_recovery_pods", "CAM 02 — AUTODOC GANTRY & BIOMONITOR RECOVERY PODS", "Articulated Surgical Arms & UV Pharmacy Tower • Twin Medical Biomonitor Pods (Bunk #02)"),
            ("cam_03_east_surgical_scrub_and_triage", "CAM 03 — EAST SURGICAL SCRUB & TRIAGE CONSOLE", "Sonic Scrub Vanity #03 • Chief Surgeon Split Comms Desk #02 • Bio-Isolation O2 Station #02"),
        ]
    },
    {
        "num": "05",
        "sheet_names": ["room_05_eva_airlock_bay_sheet.png", "room_05_eva_airlock_sheet.png", "room_05_sheet.png"],
        "title": "CYLINDER HAB-7 — ROOM 05: EVA PREP & AIRLOCK STAGING BAY",
        "subtitle": "7.5m × 8.5m × 3.4m EVA Staging Bay • Outer-Hull Decompression Gantry #02 • 4× Dual-Bay EVA Suit Lockers • Deep-Space Viewports",
        "views": [
            ("cam_01_eva_bay_symmetrical_overview", "CAM 01 — EVA STAGING BAY SYMMETRICAL OVERVIEW", "North Decompression Gantry #02 & Deep-Space Viewports • 4× EVA Suit Lockers • Donning Bench"),
            ("cam_02_decompression_chamber_and_west_lockers", "CAM 02 — DECOMPRESSION LOCK & WEST SUIT SQUADRON", "Translucent Blast Door & 3D EVA Hard-Suit • UV Helmet Test Hood • West Dual-Bay Suit Lockers"),
            ("cam_03_east_lockers_and_checkout_station", "CAM 03 — EAST SUIT LOCKERS & QUARTERMASTER DESK", "East Dual-Bay EVA Suit Lockers (Gold Iridium Visors) • Quartermaster Split Comms Station #02"),
        ]
    },
    {
        "num": "06",
        "sheet_names": ["room_06_hydroponics_bay_sheet.png", "room_06_sheet.png"],
        "title": "CYLINDER HAB-7 — ROOM 06: HYDROPONICS & BIO-AIR SCRUBBER DOME",
        "subtitle": "8.0m × 9.0m × 3.6m Bio-Dome • 4× Aeroponic & Algae Bio-Scrubber Towers #02 • Botanical Analysis Island • Solarium Viewport",
        "views": [
            ("cam_01_hydro_dome_symmetrical_overview", "CAM 01 — HYDROPONICS BIO-DOME SYMMETRICAL OVERVIEW", "4× Aeroponic & Algae Bio-Scrubber Towers #02 • Botanical Analysis Island • Solarium Vista"),
            ("cam_02_west_aeroponic_towers_and_island", "CAM 02 — WEST AEROPONIC TOWERS & ANALYSIS ISLAND", "Translucent Borosilicate Growth Columns • Cyan Algae O2 Tubes • Center Propagation Bench"),
            ("cam_03_east_towers_and_botanist_station", "CAM 03 — EAST AEROPONIC COLONNADE & BOTANIST LAB", "East Bio-Scrubber Towers • Chief Botanist Comms Station #02 • South Sector Airlock #02"),
        ]
    },
    {
        "num": "07",
        "sheet_names": ["room_07_command_bridge_sheet.png", "room_07_sheet.png"],
        "title": "CYLINDER HAB-7 — ROOM 07: HABITAT COMMAND & SPIN-GRAVITY TELEMETRY BRIDGE",
        "subtitle": "8.5m × 9.5m × 3.6m Command Bridge • Holo-Table & Flight Director #02 • 4× Helm Wings • Dual Cylinder & Deep-Space Viewports",
        "views": [
            ("cam_01_bridge_command_overview", "CAM 01 — COMMAND BRIDGE SYMMETRICAL OVERVIEW", "Holo-Table & Flight Director #02 • 5-Pane North Cylinder Axis Viewport • Port & Starboard Wings"),
            ("cam_02_holotable_and_port_navigation", "CAM 02 — HOLOGRAPHIC CYLINDER TABLE & PORT HELM", "3D Translucent O'Neill Cylinder Hologram • Flight-Director Tower • Port Deep-Space Window"),
            ("cam_03_starboard_ops_and_aft_ready_bay", "CAM 03 — STARBOARD TELEMETRY & AFT READY BAY", "Starboard Spin-Gravity Consoles • Commander EVA Suit Locker #02 • South Armored Blast Hatch"),
        ]
    },
    {
        "num": "08",
        "sheet_names": ["room_08_observation_lounge_sheet.png", "room_08_sheet.png"],
        "title": "CYLINDER HAB-7 — ROOM 08: OBSERVATION LOUNGE & ZERO-G RECREATION DECK",
        "subtitle": "8.0m × 9.0m × 3.6m Stargazer Dome • Celestial Beverage Bar #02 • Twin Stargazer Daybeds (Bunk #04) • Deep-Space & Cylinder Vistas",
        "views": [
            ("cam_01_observation_lounge_overview", "CAM 01 — OBSERVATION LOUNGE PANORAMIC OVERVIEW", "Floor-to-Ceiling Deep-Space Viewport • Center Viewing Pit • East Celestial Bar & West Daybeds"),
            ("cam_02_celestial_bar_hero", "CAM 02 — CELESTIAL BEVERAGE BAR & DECANTER TOWER", "Lounge Bar #02 • Translucent Zero-G Botanical Decanter Tower • Siphon Tap Arch & Barstools"),
            ("cam_03_stargazer_daybeds_and_deep_space", "CAM 03 — STARGAZER DAYBEDS & CONVERSATION PIT", "Twin Observation Lounge Sleepers (Bunk #04) • Holo-Chess Viewing Pit • Deep-Space Nebula"),
        ]
    },
    {
        "num": "09",
        "sheet_names": ["room_09_engineering_core_sheet.png", "room_09_sheet.png"],
        "title": "CYLINDER HAB-7 — ROOM 09: ENGINEERING & LIFE-SUPPORT REACTOR CORE",
        "subtitle": "8.5m × 9.5m × 3.8m Reactor Hall • Twin V-Angled 4.85 GW Plasma Relays #02 • Cryo-Coolant Manifold • Deep-Space Radiator Viewport",
        "views": [
            ("cam_01_reactor_hall_symmetrical_overview", "CAM 01 — ENGINEERING REACTOR HALL OVERVIEW", "Twin V-Angled 4.85 GW Plasma Relays #02 • Sub-Floor Plasma Trench • Deep-Space Viewport"),
            ("cam_02_reactor_core_and_chief_desk", "CAM 02 — STARBOARD REACTOR CORE & CHIEF ENGINEER DESK", "Translucent Magnetic-Pinch Plasma Column & Toroidal Coils • D-He3 Moderator Bay • Diagnostics Desk"),
            ("cam_03_west_coolant_and_hazmat_bay", "CAM 03 — WEST CRYO-COOLANT MANIFOLD & HAZMAT EVA BAY", "18.2K Liquid-Helium Coolant Manifold • Radiation EVA Suit Locker #02 • Port Reactor Core"),
        ]
    },
    {
        "num": "10",
        "sheet_names": ["room_10_cargo_bay_sheet.png", "room_10_sheet.png"],
        "title": "CYLINDER HAB-7 — ROOM 10: MODULAR CARGO HOLD & LOGISTICS DRONE BAY",
        "subtitle": "9.0m × 10.0m × 4.0m High-Bay Hold • Twin Cargo & Drone Gantries #02 • 4-Trunk Magnetic Pallet • Dual Cylinder & Deep-Space Vistas",
        "views": [
            ("cam_01_cargo_bay_symmetrical_overview", "CAM 01 — HIGH-BAY CARGO HOLD SYMMETRICAL OVERVIEW", "Opposing West & East Cargo/Drone Gantries #02 • 4-Trunk Center Pallet • North Cylinder Viewport"),
            ("cam_02_west_gantry_drone_and_pallet", "CAM 02 — WEST CARGO GANTRY, DRONE DOCK & PALLET", "2×2 Translucent ISO Container Matrix • Docked 3D Octo-Thruster Drone • Center Magnetic Pallet"),
            ("cam_03_east_gantry_and_loadmaster_station", "CAM 03 — EAST CARGO GANTRY & LOADMASTER OFFICE", "East Cargo & Drone Gantry #02 • Chief Loadmaster Manifest Desk #02 • South Cargo Bulkhead Hatch"),
        ]
    },
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


def compose_3cam_sheet(rm: dict):
    num = rm["num"]
    rdir = f"./godot/renders/rooms/room_{num}"
    adir = f"./assets/renders/rooms/room_{num}"

    # Layout: Hero wide CAM 01 on top (full width 1960x920), CAM 02 & CAM 03 side by side below (968x545 each)
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

    font_title = load_font(30, bold=True)
    font_sub = load_font(17, bold=False)
    font_card_title = load_font(19, bold=True)
    font_card_desc = load_font(15, bold=False)

    draw.rectangle([0, 0, canvas_w, header_h], fill=(18, 22, 30))
    draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(0, 229, 255), width=3)
    draw.text((pad, 22), rm["title"], fill=(232, 242, 255), font=font_title)
    draw.text((pad, 68), rm["subtitle"], fill=(0, 215, 245), font=font_sub)

    # Top panel (CAM 01)
    v0 = rm["views"][0]
    x0, y0 = pad, header_h + pad
    draw.rounded_rectangle([x0 - 2, y0 - 2, x0 + top_w + 2, y0 + top_h + 2], radius=10, fill=(22, 27, 36), outline=(48, 72, 96), width=2)
    p0 = os.path.join(rdir, f"{v0[0]}.png")
    if os.path.exists(p0):
        im0 = Image.open(p0).convert("RGB").resize((top_w, top_img_h), Image.Resampling.LANCZOS)
        sheet.paste(im0, (x0, y0))
    fy0 = y0 + top_img_h
    draw.rectangle([x0, fy0, x0 + top_w, y0 + top_h], fill=(16, 20, 27))
    draw.text((x0 + 16, fy0 + 12), v0[1], fill=(235, 244, 255), font=font_card_title)
    draw.text((x0 + 16, fy0 + 42), v0[2], fill=(0, 215, 245), font=font_card_desc)

    # Bottom 2 panels (CAM 02, CAM 03)
    for idx in range(2):
        v = rm["views"][idx + 1]
        bx = pad + idx * (bot_w + pad)
        by = header_h + pad + top_h + pad
        draw.rounded_rectangle([bx - 2, by - 2, bx + bot_w + 2, by + bot_h + 2], radius=10, fill=(22, 27, 36), outline=(48, 72, 96), width=2)
        p = os.path.join(rdir, f"{v[0]}.png")
        if os.path.exists(p):
            im = Image.open(p).convert("RGB").resize((bot_w, bot_img_h), Image.Resampling.LANCZOS)
            sheet.paste(im, (bx, by))
        bfy = by + bot_img_h
        draw.rectangle([bx, bfy, bx + bot_w, by + bot_h], fill=(16, 20, 27))
        draw.text((bx + 16, bfy + 12), v[1], fill=(235, 244, 255), font=font_card_title)
        draw.text((bx + 16, bfy + 42), v[2], fill=(0, 215, 245), font=font_card_desc)

    for d in [rdir, adir]:
        os.makedirs(d, exist_ok=True)
        for sname in rm["sheet_names"]:
            out_p = os.path.join(d, sname)
            sheet.save(out_p, "PNG", compress_level=4)
            print(f"[Room{num}Sheet] Saved {out_p} ({canvas_w}x{canvas_h})")


if __name__ == "__main__":
    for rm in ROOM_SHEETS:
        compose_3cam_sheet(rm)
