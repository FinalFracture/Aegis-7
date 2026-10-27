#!/usr/bin/env python3
"""
Composes 5-candidate voting sheets for Building Exteriors bldg_01 .. bldg_15 ("Aegis-7 Exterior Standard").
Writes to:
- ./godot/renders/buildings/bldg_XX/bldg_XX_round1_voting_sheet.png
- ./assets/renders/buildings/bldg_XX/bldg_XX_round1_voting_sheet.png
"""
import os
import sys
import json
from PIL import Image, ImageDraw, ImageFont

BUILDINGS_META = {
    "bldg_01": {
        "slug": "bldg_01_hab_spire",
        "title": "BUILDING 01: AEGIS-7 MODULAR CREW HABITAT TOWER (5-CHOICE TEST)",
        "sub": "District I: Residential & Civic Terrace • Translucent Sky-Elevator Atrium • Chamfered Octagonal Pod Spire • Vote 01–05",
        "cands": [
            ("01", "Symmetric Octagonal Stepped Pod Spire", "45° Chamfered Gunmetal Ribs • Symmetrical Residential Berths • Rooftop Beacon Spire"),
            ("02", "Dual-Zone Split Pod Spire & Sky-Elevator Atrium", "Aegis-7 65/35 Split-Mass • Stepped Hab Tower + Full-Height Translucent Sky-Elevator Atrium"),
            ("03", "Twin-Cantilevered Hex-Hive Terraced Block", "Interlocking Hexagonal Crew Pods • Central Structural Core • Dual Plaza Entries"),
            ("04", "Curved Cylinder-Slope Terraced Hab Ziggurat", "Stepped Garden Terraces • Sloped Solar Skylights • Wide Pedestrian Plinth"),
            ("05", "Suspended Modular Pod-Cluster & Skybridge Tower", "Twin Structural Pylons • Elevated Skybridge Concourse • Suspended Hab Modules"),
        ]
    },
    "bldg_02": {
        "slug": "bldg_02_transit_rotunda",
        "title": "BUILDING 02: ELEVATED MAG-LEV & RING TRANSIT ROTUNDA (5-CHOICE TEST)",
        "sub": "District I: Residential & Civic Terrace • Elevated Guideway Concourse • Vertical Shuttle-Pod Tower • Vote 01–05",
        "cands": [
            ("01", "Octagonal Central Mag-Lev Concourse Rotunda", "Domed Commuter Concourse • Through-Deck Guideway Portals • 360° Plaza Steps"),
            ("02", "Dual-Zone Split Mag-Lev Hall & Shuttle-Pod Tower", "Aegis-7 65/35 Split-Mass • Concourse Hall + Translucent Vertical Shuttle Boarding Tower"),
            ("03", "Twin-Tube Elevated Guideway Overpass Terminal", "Dual Parallel Mag-Lev Tubes • Suspended Ticketing Mezzanine • Brushed-Steel Arches"),
            ("04", "Cantilevered Ring-Line Commuter Hub & Control Pylon", "Overhanging Platform Canopy • Asymmetric Dispatch Pylon • Amber Track Beacons"),
            ("05", "Tri-Level Rotary Transit Interchange Plaza", "Stacked Circular Concourses • Spiral Pedestrian Ramps • Rooftop Drone Pad"),
        ]
    },
    "bldg_03": {
        "slug": "bldg_03_culinary_atrium",
        "title": "BUILDING 03: TERRACED SYNTHESIZER & CULINARY COMMONS PAVILION (5-CHOICE TEST)",
        "sub": "District I: Residential & Civic Terrace • Panoramic Dining Hall • Translucent Aeroponic Herb Tower • Vote 01–05",
        "cands": [
            ("01", "Octagonal Glass-Crowned Mess Hall Pavilion", "Chamfered Dining Rotunda • Translucent Skylight Crown • Wrap-Around Patio"),
            ("02", "Dual-Zone Split Culinary Pavilion & Herb Tower", "Aegis-7 65/35 Split-Mass • Terraced Dining Hall + Full-Height UV-Violet Aeroponic Herb Tower"),
            ("03", "Terraced Promenade Bistro & Zero-G Beverage Rotunda", "Multi-Tiered Open Dining Decks • Illuminated Siphon Bar Dome • Plaza Steps"),
            ("04", "Twin-Wing Civic Refectory & Solar-Lit Courtyard", "Symmetrical Mess Wings • Central Glazed Botanical Atrium • Overhead Sun Louvers"),
            ("05", "Cantilevered Overlook Dining Deck & Ration Silo", "Projecting Panorama Dining Box • Cylindrical Nutrient Silos • Service Loading Bay"),
        ]
    },
    "bldg_04": {
        "slug": "bldg_04_medical_trauma_center",
        "title": "BUILDING 04: ORBITAL TRAUMA & BIOMONITOR MEDICAL COMPLEX (5-CHOICE TEST)",
        "sub": "District I: Residential & Civic Terrace • Surgical Triage Wing • UV-Sterile Cryo-Pharmacy Tower • Vote 01–05",
        "cands": [
            ("01", "Octagonal Clinical Pavilion & Rooftop Med-Evac Pad", "Aerospace-White Sterile Facade • Rooftop Octagonal Landing Pad • Surgical Ice-White Halo"),
            ("02", "Dual-Zone Split Trauma Wing & UV Cryo-Pharmacy Tower", "Aegis-7 65/35 Split-Mass • Surgical Hospital Block + Translucent UV-Violet Pharmacy Tower"),
            ("03", "Twin-Dome Bio-Quarantine & Triage Center", "Dual Pressurized Isolation Domes • Central Decontamination Airlock • Amber Quarantine Strips"),
            ("04", "Stepped Aerospace-White Surgical Institute & Dock", "Terraced Recovery Ward Floors • Pressurized Ambulance Bay • Diagnostic Sensor Mast"),
            ("05", "Cantilevered Zero-G Recovery Sanatorium & Spire", "Elevated Low-G Patient Ring • Translucent Solarium Ward • Biomonitor Telemetry Spire"),
        ]
    },
    "bldg_05": {
        "slug": "bldg_05_celestial_promenade_dome",
        "title": "BUILDING 05: ZERO-G OBSERVATION & RECREATION DOME (5-CHOICE TEST)",
        "sub": "District I: Residential & Civic Terrace • Faceted Stargazer Dome • Illuminated Zero-G Ascent Tower • Vote 01–05",
        "cands": [
            ("01", "Faceted Octagonal Geodesic Observation Dome", "Full-Span Translucent Stargazer Dome • Titanium Octagonal Ribs • Viewing Gallery Ring"),
            ("02", "Dual-Zone Split Stargazer Dome & Zero-G Ascent Tower", "Aegis-7 65/35 Split-Mass • Faceted Observation Dome + Translucent Zero-G Float Tube Tower"),
            ("03", "Twin-Ringed Panoramabridge & Amphitheater Pavilion", "Concentric Viewing Decks • Open-Air Cylinder Overlook • Celestial Bar Canopy"),
            ("04", "Terraced Civic Park Conservatory & Holo-Fountain", "Stepped Leisure Decks • Central Holographic Water Feature • UV/Cyan Mood Lighting"),
            ("05", "Cantilevered Horizon Viewing Deck & Celestial Bar", "Dramatic Overhanging Glass Promenade • Illuminated Decanter Spire • Lounge Plaza"),
        ]
    },
    "bldg_06": {
        "slug": "bldg_06_hydroponic_biodome",
        "title": "BUILDING 06: AEROPONIC & BIO-SCRUBBER CONSERVATORY COMPLEX (5-CHOICE TEST)",
        "sub": "District II: Agri-Biosphere & Research • Translucent Botanical Conservatory • O2 Algae Bio-Scrubber Tower • Vote 01–05",
        "cands": [
            ("01", "Tri-Dome Geodesic Botanical Conservatory", "Three Interlinked Glass Bio-Domes • Internal Emerald Foliage • Overhead Irrigation Truss"),
            ("02", "Dual-Zone Split Conservatory & O2 Algae Bio-Tower", "Aegis-7 65/35 Split-Mass • Glazed Aeroponic Hall + Full-Height Cyan Algae Scrubber Tower"),
            ("03", "Stepped Agricultural Ziggurat & UV-Grow Terrace", "Tiered Illuminated Crop Trays • UV-Violet Grow Halos • Nutrient Pumping Plinth"),
            ("04", "Twin-Cylinder Vertical Farm & Nutrient Silo Array", "Dual Translucent Rotary Grow Columns • Central Control Bridge • Dosing Silos"),
            ("05", "Octagonal Biosphere Rotunda & Canopy Skywalk", "High-Bay Botanical Rotunda • Elevated Inspection Walkway • Solarium Skylight"),
        ]
    },
    "bldg_07": {
        "slug": "bldg_07_atmospheric_processor",
        "title": "BUILDING 07: SECTOR ATMOSPHERIC & O2/CO2 SCRUBBER PLANT (5-CHOICE TEST)",
        "sub": "District II: Agri-Biosphere & Research • Air-Exchange Turbine Hall • Translucent Cryo-O2 Distillation Tower • Vote 01–05",
        "cands": [
            ("01", "Octagonal Air-Exchange Intake & Turbine Hall", "Heavy Louvered Intake Facade • Twin Roof Exhaust Venturis • UV-Violet Filter Glow"),
            ("02", "Dual-Zone Split Processor Hall & Cryo-O2 Tower", "Aegis-7 65/35 Split-Mass • Scrubber Turbine Hall + Translucent Cryo-O2 Distillation Column"),
            ("03", "Quad-Stack Venturi Scrubber & Thermal Louver Plant", "Four Vertical Scrubber Stacks • Machined-Steel Piping Gantry • Amber Pressure Beacons"),
            ("04", "Twin-Sphere Liquid-Oxygen Storage & Barometric Hub", "Spherical Cryo-O2 Tanks • Octagonal Telemetry Control Block • Orange Purge Valves"),
            ("05", "Heavy Industrial Spin-Filter & Humidity Complex", "Cylindrical Centrifugal Air Filters • Brushed-Steel Ductwork • Service Gantry"),
        ]
    },
    "bldg_08": {
        "slug": "bldg_08_astrometry_observatory",
        "title": "BUILDING 08: DEEP-SPACE ASTROMETRY & SENSOR ARRAY COMPLEX (5-CHOICE TEST)",
        "sub": "District II: Agri-Biosphere & Research • Astrometry Charting Lab • Rotating Deep-Space Telemetry Dish Tower • Vote 01–05",
        "cands": [
            ("01", "Octagonal Clamshell Optical Telescope Observatory", "Segmented Telescope Dome • Deep-Space Sensor Aperture • Gunmetal Octagonal Base"),
            ("02", "Dual-Zone Split Astrometry Lab & Telemetry Dish Tower", "Aegis-7 65/35 Split-Mass •Holo-Charting Lab Wing + Translucent Gantry & Deep-Space Dish Tower"),
            ("03", "Tri-Dish Interferometer & Quantum Comms Building", "Three Roof-Mounted Parabolic Dishes • Optical Laser Link Spire • Shielded Data Vault"),
            ("04", "Stepped Sensor Dome & Subspace Beacon Annex", "Tiered Telemetry Decks • Glowing Cyan Subspace Emitter • Calibration Gantry"),
            ("05", "Cantilevered Deep-Sky Spectrograph & Charting Center", "Angled Spectrograph Boom • Translucent Star-Map Rotunda • Antenna Array"),
        ]
    },
    "bldg_09": {
        "slug": "bldg_09_aquifer_pumping_station",
        "title": "BUILDING 09: RING-GRAVITY WATER RECLAMATION & AQUIFER CASCADE (5-CHOICE TEST)",
        "sub": "District II: Agri-Biosphere & Research • Centrifugal Pumping Plant • Translucent Illuminated Water-Column Tower • Vote 01–05",
        "cands": [
            ("01", "Octagonal Hydro-Filtration Hall & Settling Basin", "Chamfered Filtration Plant • Glowing Cyan Settling Tanks • Machined-Steel Pipe Bridges"),
            ("02", "Dual-Zone Split Pumping Plant & Water-Column Tower", "Aegis-7 65/35 Split-Mass • Turbine Pump Hall + Full-Height Translucent Cyan Water-Column Tower"),
            ("03", "Terraced Cascade Spillway & UV-Purification Complex", "Stepped Illuminated Water Weirs • UV-Violet Sterilization Channels • Valve Gantry"),
            ("04", "Twin-Silo Greywater Recovery & Mineral Station", "Dual Pressurized Hydro-Silos • Central Telemetry Bridge • Signal-Orange Main Valves"),
            ("05", "Heavy Conduit Manifold & Pressure-Regulator Plant", "High-Pressure Ring-Main Headers • Octagonal Pump House • Inspection Catwalks"),
        ]
    },
    "bldg_10": {
        "slug": "bldg_10_cryo_seed_vault",
        "title": "BUILDING 10: COLONIAL CRYO-GENETICS & SEED ARCHIVE VAULT (5-CHOICE TEST)",
        "sub": "District II: Agri-Biosphere & Research • Armored Bio-Archive Vault • Translucent Cryo-Stasis Helix Tower • Vote 01–05",
        "cands": [
            ("01", "Armored Octagonal Sub-Zero Gene Bank Monolith", "Heavy Sloped Titanium Armor • Recessed Cryo-Blue Louvers • Biometric Vault Portal"),
            ("02", "Dual-Zone Split Seed Archive & Cryo-Helix Tower", "Aegis-7 65/35 Split-Mass • Armored Gene Vault + Translucent UV/Cyan Cryo-Vial Helix Tower"),
            ("03", "Subterranean-Plinth Cryogenic Silo & Radiator Array", "Fortified Low Vault • Vertical Liquid-Nitrogen Radiator Fins • Amber Security Perimeter"),
            ("04", "Twin-Buttressed Bio-Preservation Bunker & Lab Wing", "Dual Armored Archive Vaults • Glazed Genetics Research Bridge • Rooftop Cooling Towers"),
            ("05", "Cantilevered Deep-Freeze Repository & Security Portal", "Elevated Isolation Vault • Heavy Blast-Door Entrance • Cryo-Manifold Spine"),
        ]
    },
    "bldg_11": {
        "slug": "bldg_11_citadel_command_hq",
        "title": "BUILDING 11: CYLINDER HAB-7 CENTRAL COMMAND & TELEMETRY CITADEL (5-CHOICE TEST)",
        "sub": "District III: Command, Power & Industrial Port • Overwatch Bridge Spire • Translucent Quantum Flight-Director Tower • Vote 01–05",
        "cands": [
            ("01", "Monumental Octagonal Command Spire & Bridge Crown", "Soaring Stepped Titanium Spire • 360° Top-Floor Command Bridge • Axial Holo-Beacon"),
            ("02", "Dual-Zone Split Command Citadel & Flight-Director Tower", "Aegis-7 65/35 Split-Mass • Armored Command Spire + Translucent Quantum Flight-Director Tower"),
            ("03", "Twin-Obelisk Sector Governance & Defense HQ", "Dual Chamfered Command Towers • High-Altitude Glass Skybridge • Tactical Comms Array"),
            ("04", "Stepped Pyramidion Overwatch Citadel & Holo-Beacon", "Tiered Octagonal Command Decks • Rooftop Cylinder Holo-Projector • Blast-Hatch Plinth"),
            ("05", "Cantilevered High-Command Bridge & Comms Mast", "Forward-Raked Bridge Overlook • Vertical Telemetry Mast • VIP Shuttle Pad"),
        ]
    },
    "bldg_12": {
        "slug": "bldg_12_fusion_reactor_complex",
        "title": "BUILDING 12: D-HE3 FUSION POWER & SPIN-DRIVE REACTOR HALL (5-CHOICE TEST)",
        "sub": "District III: Command, Power & Industrial Port • Magnetic Confinement Hall • Translucent 5-Coil Plasma Pinch Tower • Vote 01–05",
        "cands": [
            ("01", "Octagonal Magnetic-Confinement Fusion Reactor Dome", "Armored Containment Rotunda • Glowing Cyan/Amber Bus-Bars • Cryo-Coolant Stacks"),
            ("02", "Dual-Zone Split Fusion Hall & 5-Coil Plasma Tower", "Aegis-7 65/35 Split-Mass • Heavy Reactor Hall + Translucent 5-Coil Plasma Pinch Column"),
            ("03", "Twin-Core Toroidal Tokamak & Radiator Fin Complex", "Dual Tokamak Containment Vessels • High-Bay Thermal Radiator Wings • Substation Plinth"),
            ("04", "Heavy Armored Spin-Drive Impulse Plant & Cryo Bay", "Reinforced Axial Thrust Housing • Liquid-Helium Cryo Silos • High-Voltage Gantry"),
            ("05", "High-Voltage Substation & Plasma Conduit Gantry Hall", "Exposed Toroidal Field Coils • Overhead Bus-Bar Bridges • SCRAM Control Tower"),
        ]
    },
    "bldg_13": {
        "slug": "bldg_13_cargo_logistics_port",
        "title": "BUILDING 13: HIGH-BAY INTERMODAL CARGO & DRONE GANTRY TERMINAL (5-CHOICE TEST)",
        "sub": "District III: Command, Power & Industrial Port • Intermodal Freight Hall • Translucent ISO Container & Drone Gantry • Vote 01–05",
        "cands": [
            ("01", "Octagonal High-Bay Freight Warehouse & Crane Arch", "Monumental Logistics Hall • Overhead Magnetic Bridge Crane • Amber Loading Bays"),
            ("02", "Dual-Zone Split Cargo Terminal & Drone Gantry Tower", "Aegis-7 65/35 Split-Mass • Intermodal Freight Hall + Translucent ISO Container & Drone Dock Tower"),
            ("03", "Twin-Gantry Open Container Yard & Mag-Loader Dock", "Dual Steel Crane Gantries • Stacked ISO Cargo Matrix • Loadmaster Control Booth"),
            ("04", "Automated Logistics Sorting Hub & Drone Hive Roof", "Multi-Bay Dispatch Warehouse • Rooftop Octo-Drone Landing Hive • RFID Manifest Spire"),
            ("05", "Heavy Bulkhead Freight Depot & Shuttle Unloading Bay", "Armored Cargo Airlock Doors • Cantilevered Hoist Boom • Pallet Staging Plaza"),
        ]
    },
    "bldg_14": {
        "slug": "bldg_14_eva_docking_pinnacle",
        "title": "BUILDING 14: AXIAL ZERO-G SHUTTLE & EVA DOCKING PINNACLE (5-CHOICE TEST)",
        "sub": "District III: Command, Power & Industrial Port • EVA Staging Terminal • Translucent Umbilical Shuttle Docking Pinnacle • Vote 01–05",
        "cands": [
            ("01", "Octagonal Vertical Airlock & Docking Collar Tower", "Vertical Decompression Spine • Twin Universal Docking Collars • Amber Approach Strobes"),
            ("02", "Dual-Zone Split EVA Terminal & Docking Pinnacle", "Aegis-7 65/35 Split-Mass • EVA Prep Hall + Translucent Umbilical Shuttle Docking Tower"),
            ("03", "Twin-Arm Cantilevered Orbital Tender Berth", "Dual Extending Mooring Arms • Pressurized Crew Boarding Tubes • Cryo-Fuel Umbilicals"),
            ("04", "Pressurized Passenger Boarding Spire & Suit Prep Hall", "Glazed Vertical Transfer Lift • Multi-Lock EVA Departure Bay • Radar Guidance Crown"),
            ("05", "Heavy Hull-Lock Checkpoint & Rescue Cutter Hangar", "Armored Outer-Hull Blast Portal • Enclosed Cutter Servicing Bay • Decon Gantry"),
        ]
    },
    "bldg_15": {
        "slug": "bldg_15_solar_mirror_control_pylon",
        "title": "BUILDING 15: ORBITAL SOLAR-MIRROR & MAG-SHIELD CONTROL PYLON (5-CHOICE TEST)",
        "sub": "District III: Command, Power & Industrial Port • Shield Control Bunker • Translucent Gyroscopic Field-Ring Pylon • Vote 01–05",
        "cands": [
            ("01", "Octagonal Heliostat & Magnetic Shield Emitter Pylon", "Chamfered Emitter Pylon • Glowing Cyan Field Rings • Armored Capacitor Plinth"),
            ("02", "Dual-Zone Split Shield Bunker & Field-Ring Pylon", "Aegis-7 65/35 Split-Mass • Heliostat Control Bunker + Translucent Gyroscopic Field-Ring Tower"),
            ("03", "Tri-Strut Solar Louver Actuator & Capacitor Tower", "Three Angled Titanium Struts • Suspended Plasma Field Core • High-Voltage Insulators"),
            ("04", "Twin-Coil Magnetosphere Deflector & Alignment Spire", "Dual Superconducting Deflector Coils • Precision Laser Alignment Turret • Cryo Base"),
            ("05", "Armored Axial Weather-Control & Daylight Relay Station", "Fortified Telemetry Bunker • Rotating Solar-Mirror Dish • Circadian Spectrum Beacon"),
        ]
    },
}


def load_font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def get_manifest_stats(bid: str):
    stats = {}
    mpath = f"./assets/glb/buildings/{bid}/{bid}_r1_manifest.json"
    if not os.path.exists(mpath):
        mpath2 = f"./assets/glb/buildings/{bid}/manifest.json"
        if os.path.exists(mpath2):
            mpath = mpath2
    if os.path.exists(mpath):
        try:
            with open(mpath, "r") as f:
                data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    fn = os.path.basename(item.get("filepath", item.get("file", "")))
                    stats[fn] = item
            elif isinstance(data, dict) and "candidates" in data:
                for item in data["candidates"]:
                    fn = os.path.basename(item.get("filepath", item.get("file", "")))
                    stats[fn] = item
        except Exception:
            pass
    return stats


def compose_voting_sheet(bid: str):
    if bid not in BUILDINGS_META:
        return False
    meta = BUILDINGS_META[bid]
    rdir = f"./godot/renders/buildings/{bid}"
    adir = f"./assets/renders/buildings/{bid}"

    # Verify all 5 PNGs exist
    for i in range(1, 6):
        p = os.path.join(rdir, f"{bid}_r1_{i:02d}.png")
        if not os.path.exists(p):
            return False

    stats_map = get_manifest_stats(bid)

    cols = 3
    rows = 2
    cell_w = 880
    cell_img_h = 495
    cell_footer_h = 92
    cell_h = cell_img_h + cell_footer_h
    pad = 22
    header_h = 108

    canvas_w = pad + cols * (cell_w + pad)
    canvas_h = header_h + pad + rows * (cell_h + pad)

    sheet = Image.new("RGB", (canvas_w, canvas_h), (12, 15, 20))
    draw = ImageDraw.Draw(sheet)

    font_title = load_font(30, bold=True)
    font_sub = load_font(17, bold=False)
    font_badge = load_font(22, bold=True)
    font_tris = load_font(15, bold=True)
    font_card_title = load_font(18, bold=True)
    font_card_desc = load_font(14, bold=False)

    draw.rectangle([0, 0, canvas_w, header_h], fill=(18, 22, 30))
    draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(0, 229, 255), width=3)
    draw.text((pad, 20), f"CYLINDER HAB-7 — {meta['title']}", fill=(232, 242, 255), font=font_title)
    draw.text((pad, 64), meta["sub"], fill=(0, 215, 245), font=font_sub)

    for idx, (num_str, ctitle, cdesc) in enumerate(meta["cands"]):
        r = idx // cols
        c = idx % cols
        if r == 1:
            # Center the 2 bottom cards
            row2_w = 2 * cell_w + pad
            start_x = (canvas_w - row2_w) // 2
            x0 = start_x + c * (cell_w + pad)
        else:
            x0 = pad + c * (cell_w + pad)
        y0 = header_h + pad + r * (cell_h + pad)

        is_hero = (num_str == "02")
        outline_col = (0, 229, 255) if is_hero else (48, 72, 96)
        draw.rounded_rectangle(
            [x0 - 2, y0 - 2, x0 + cell_w + 2, y0 + cell_h + 2],
            radius=10,
            fill=(22, 27, 36),
            outline=outline_col,
            width=3 if is_hero else 2,
        )

        img_path = os.path.join(rdir, f"{bid}_r1_{num_str}.png")
        im = Image.open(img_path).convert("RGB").resize((cell_w, cell_img_h), Image.Resampling.LANCZOS)
        sheet.paste(im, (x0, y0))

        # Number badge top-left
        draw.rounded_rectangle([x0 + 12, y0 + 12, x0 + 68, y0 + 50], radius=6, fill=(0, 210, 245))
        draw.text((x0 + 23, y0 + 17), num_str, fill=(10, 14, 20), font=font_badge)

        # Stats badge top-right
        glb_fn = f"{bid}_r1_{num_str}.glb"
        st = stats_map.get(glb_fn, {})
        tris = st.get("triangles", st.get("tris", 0))
        dims = st.get("dimensions", [12.0, 18.0, 10.0])
        stat_txt = f"{glb_fn} | {tris:,} Tris" if tris else f"{glb_fn} | Aegis-7 Exterior"
        draw.rounded_rectangle([x0 + cell_w - 310, y0 + 12, x0 + cell_w - 12, y0 + 44], radius=6, fill=(14, 18, 25))
        draw.text((x0 + cell_w - 298, y0 + 19), stat_txt, fill=(190, 225, 255), font=font_tris)

        fy0 = y0 + cell_img_h
        draw.rectangle([x0, fy0, x0 + cell_w, y0 + cell_h], fill=(16, 20, 27))
        draw.text((x0 + 14, fy0 + 10), f"#{num_str} — {ctitle}", fill=(235, 244, 255), font=font_card_title)
        draw.text((x0 + 14, fy0 + 38), cdesc, fill=(0, 215, 245), font=font_card_desc)
        if dims and len(dims) == 3:
            dim_str = f"Envelope: {dims[0]:.1f}m W × {dims[2]:.1f}m D × {dims[1]:.1f}m H • Aegis-7 PBR + Translucent Glass"
        else:
            dim_str = "Envelope: 12.0m W × 10.0m D × 18.0m H • Aegis-7 PBR + Translucent Glass"
        draw.text((x0 + 14, fy0 + 62), dim_str, fill=(155, 175, 198), font=font_card_desc)

    slug = meta["slug"]
    for d in [rdir, adir]:
        os.makedirs(d, exist_ok=True)
        for sname in [f"{bid}_round1_voting_sheet.png", f"{slug}_round1_voting_sheet.png"]:
            out_p = os.path.join(d, sname)
            sheet.save(out_p, "PNG", compress_level=4)
            print(f"[VotingSheet] Saved {out_p} ({canvas_w}x{canvas_h})")
    return True


pass

PHASE3_META = {
    "prop_01": {
        "category": "props",
        "slug": "prop_01_maglev_shuttle_pylon",
        "title": "EXTERIOR PROP 01: ELEVATED MAG-LEV GUIDEWAY PYLON & RING-TRANSIT POD (5-CHOICE TEST)",
        "sub": "Phase 3 Sci-Fi Movie Set Prop • Elevated Mag-Lev Induction Track • Aerodynamic Passenger Pod • Vote 01–05",
        "cands": [
            ("01", "Symmetric Octagonal Mag-Lev Guideway T-Pylon & Pod", "Centered Octagonal T-Column • Overhead Track Beam • Aerodynamic Shuttle Car"),
            ("02", "Dual-Zone Split Mag-Lev Y-Pylon, Pod & Telemetry Spine", "Aegis-7 65/35 Split-Mass • Cantilevered Track & Shuttle Pod + Translucent Telemetry Spine"),
            ("03", "Twin-Cantilevered Mag-Lev Arch Gantry & Express Pod", "Straddling Portal Arch • Overhead Catenary Rails • Suspended Passenger Pod"),
            ("04", "Heavy Buttressed Traction Substation Pylon & Rail", "Industrial Transformer Plinth • Dual-Rail Mag-Lev Deck • Signal-Orange Couplings"),
            ("05", "Suspended Monorail Truss Pylon & Signal Portal", "Open Space-Frame Truss Pylon • Underslung Transit Car • Amber Signal Bridge"),
        ]
    },
    "prop_02": {
        "category": "props",
        "slug": "prop_02_holo_wayfinding_kiosk",
        "title": "EXTERIOR PROP 02: OCTAGONAL PEDESTRIAN WAYFINDING & HOLO-KIOSK (5-CHOICE TEST)",
        "sub": "Phase 3 Sci-Fi Movie Set Prop • 3D O'Neill Cylinder Holo-Map • Emergency O2 Breather Locker • Vote 01–05",
        "cands": [
            ("01", "Symmetric Octagonal Holo-Directory Totem", "4-Sided Directory Monolith • Top Holo-Ring Beacon • Chamfered Plinth"),
            ("02", "Dual-Zone Split Holo-Kiosk & Emergency Breather Locker", "Aegis-7 65/35 Split-Mass • 3D Cylinder Holo-Map Console + Translucent O2 Breather Totem"),
            ("03", "Tri-Wing Plaza Information Rotunda & Beacon", "Three Radial Terminal Wings • Central Light Column • Sector Marquee Header"),
            ("04", "Cantilevered Canopy Map Terminal & Comms Bench", "L-Shaped Interactive Terminal • Integrated Rest Perch • Glare Hood"),
            ("05", "Cylindrical Orbital Cylinder Map Projector Pedestal", "Waist-High Octagonal Holo-Table • Overhead Ring Receiver • Cyan Telemetry"),
        ]
    },
    "prop_03": {
        "category": "props",
        "slug": "prop_03_atmo_scrubber_bollard",
        "title": "EXTERIOR PROP 03: STREET-LEVEL ATMO SCRUBBER & SPIN-BALANCER BOLLARD (5-CHOICE TEST)",
        "sub": "Phase 3 Sci-Fi Movie Set Prop • Venturi Air-Exchange Louvers • Translucent Ion-Filter & EVA Tether • Vote 01–05",
        "cands": [
            ("01", "Octagonal Louvered Air-Intake Plaza Bollard", "Symmetrical Octagonal Vent Stack • Carbon-Slate Intake Grilles • Amber Base Strip"),
            ("02", "Dual-Zone Split Venturi Intake & Translucent Ion-Filter Bollard", "Aegis-7 65/35 Split-Mass • Venturi Scrubber & EVA Tether Rings + Translucent UV/Cyan Ion Column"),
            ("03", "Twin-Turbine Street Corner Air-Exchange Stack", "Dual Cylindrical Intake Cowls • Shared Manifold Plinth • Cyan Airflow Bars"),
            ("04", "Armored Spin-Harmonic Damper & O2 Monitor Post", "Counterweight Gyro Bunker • Vertical Sensor Mast • Signal-Orange Purge Valve"),
            ("05", "Terraced UV-Biofilter Vent & Safety Strobe Pylon", "Stepped Louver Bollard • 360° Amber Fog Strobe • Internal UV Sterilizer"),
        ]
    },
    "prop_04": {
        "category": "props",
        "slug": "prop_04_civic_planter_bench_pod",
        "title": "EXTERIOR PROP 04: TERRACED AEROPONIC CIVIC PLANTER & CREW BENCH POD (5-CHOICE TEST)",
        "sub": "Phase 3 Sci-Fi Movie Set Prop • Contoured Crew Seating • Translucent UV-Aeroponic Planter Canopy • Vote 01–05",
        "cands": [
            ("01", "Octagonal Central Tree Planter & Perimeter Bench Ring", "Wrap-Around Octagonal Seating • Central Botanical Tub • Warm Amber Under-Glow"),
            ("02", "Dual-Zone Split Crew Bench Lounge & UV-Aeroponic Canopy", "Aegis-7 65/35 Split-Mass • Contoured Bench & Solar Pergola + Translucent Emerald Mist Terrarium"),
            ("03", "Twin-Tiered Botanical Promenade Seating Island", "Back-to-Back Contoured Benches • Raised Aeroponic Herb Hedge • Charge Ports"),
            ("04", "Curved Cylinder-Slope Leisure Bench & Herb Trough", "Swept Amphitheater Bench • Integrated Foliage Trough • Brushed-Steel Armrests"),
            ("05", "Cantilevered Solar-Pergola Bench & Hydro-Basin Pod", "Shaded Crew Bench Pod • Translucent Water-Reclamation Basin • UV Grow Halo"),
        ]
    },
    "prop_05": {
        "category": "props",
        "slug": "prop_05_vtol_medevac_pad_array",
        "title": "EXTERIOR PROP 05: OCTAGONAL VTOL MED-EVAC PAD & TELEMETRY DISH ARRAY (5-CHOICE TEST)",
        "sub": "Phase 3 Sci-Fi Movie Set Prop • Hydraulic Skid-Lock Clamps • Translucent Flight-Control Radar Tower • Vote 01–05",
        "cands": [
            ("01", "Symmetric Octagonal Helipad Deck & Perimeter Strobes", "Octagonal Touchdown Deck • Glowing H-Reticle • Corner Approach Strobes"),
            ("02", "Dual-Zone Split VTOL Pad & Translucent Radar Control Tower", "Aegis-7 65/35 Split-Mass • Octagonal Pad & Orange Clamps + Translucent Radar Dish Tower"),
            ("03", "Cantilevered Med-Evac Docking Platform & Fuel Arm", "Overhanging Trauma Deck • Articulated Cryo-Refueling Boom • Boarding Ramp"),
            ("04", "Twin-Clamp Orbital Shuttle Berth & Approach Beacon", "Heavy Cradle Berth • Dual Magnetic Arrestor Rails • Glide-Slope Emitter"),
            ("05", "Elevated Magnetic Arrestor Pad & Weather Mast Array", "Truss-Supported Landing Deck • Twin Anemometer & Laser Alignment Masts"),
        ]
    },
    "bldg_16": {
        "category": "buildings",
        "slug": "bldg_16_shipyard_drydock_hall",
        "title": "BUILDING 16: AXIAL ZERO-G MICRO-SHUTTLE ASSEMBLY & DRYDOCK HALL (5-CHOICE TEST)",
        "sub": "District IV: Shipyard, Arena, Museum & Defense • Hull Fabrication Hall • Translucent Zero-G Shuttle Drydock Tower • Vote 01–05",
        "cands": [
            ("01", "Octagonal High-Bay Spacecraft Hangar & Gantry Arch", "Symmetrical High-Bay Drydock • Overhead Bridge-Crane Arch • Signal-Orange Blast Doors"),
            ("02", "Dual-Zone Split Shipyard Hall & Zero-G Drydock Gantry Tower", "Aegis-7 65/35 Split-Mass • Avionics Hangar + Translucent Vertical Micro-Shuttle Drydock Tower"),
            ("03", "Twin-Cradle Orbital Tender Repair Bay & Crane Truss", "Dual External Repair Cradles • Parallel Crane Trusses • Welding Gantry"),
            ("04", "Pressurized Hull-Fabrication Vault & Welding Spire", "Armored Metallurgy Hall • Plasma-Arc Exhaust Stack • Rooftop Flight Pad"),
            ("05", "Cantilevered Flight-Test Launch Bay & Telemetry Dock", "Elevated Launch Tube • Ground Maintenance Bay • Approach Radar Crown"),
        ]
    },
    "bldg_17": {
        "category": "buildings",
        "slug": "bldg_17_coriolis_recreation_arena",
        "title": "BUILDING 17: CORIOLIS KINETIC SPORTS ARENA & CENTRIFUGE GYMNASIUM (5-CHOICE TEST)",
        "sub": "District IV: Shipyard, Arena, Museum & Defense • Zero-G Sports Colosseum • Translucent Multi-G Centrifuge Tower • Vote 01–05",
        "cands": [
            ("01", "Octagonal Domed Zero-G Sports Colosseum", "Central Octagonal Stadium • Translucent Geodesic Sports Dome • Athlete Concourse"),
            ("02", "Dual-Zone Split Kinetic Arena & Centrifuge Conditioning Tower", "Aegis-7 65/35 Split-Mass • Domed Sports Colosseum + Translucent 4-Ring Centrifuge Tower"),
            ("03", "Twin-Ringed Low-Gravity Track & Aquatic Recovery Dome", "Dual Circular Track Drums • Hydro-Therapy Dome • Spectator Terraces"),
            ("04", "Stepped Spectator Stadium & Hyperbaric Training Wing", "Tiered Stadium Seating • Indoor Kinetic Court • Biomonitor Spire"),
            ("05", "Cantilevered Zero-G Combat/Flight Sphere & Fitness Spire", "Suspended Translucent Flight-Sphere • Athletic Conditioning Tower • Plaza Steps"),
        ]
    },
    "bldg_18": {
        "category": "buildings",
        "slug": "bldg_18_colonial_holo_museum",
        "title": "BUILDING 18: AEGIS-7 COLONIAL ARCHIVES & HOLO-PLANETARIUM (5-CHOICE TEST)",
        "sub": "District IV: Shipyard, Arena, Museum & Defense • Colonial Relic Pavilion • Translucent Earth-Biosphere Holo-Orrery Tower • Vote 01–05",
        "cands": [
            ("01", "Monumental Octagonal Planetarium & Archive Rotunda", "Classical Octagonal Rotunda • Star-Projector Dome • Ceremonial Plaza Stair"),
            ("02", "Dual-Zone Split Archive Pavilion & Earth Holo-Orrery Tower", "Aegis-7 65/35 Split-Mass • Planetarium Pavilion + Translucent 3D Earth-Orrery & Memory Tower"),
            ("03", "Twin-Wing Cultural Conservatory & Time-Capsule Vault", "Symmetrical Exhibition Wings • Central Time-Capsule Obelisk • Heritage Portal"),
            ("04", "Stepped Ziggurat History Museum & Solar Obelisk", "Terraced Museum Galleries • Tall Commemorative Needle • Illuminated Windows"),
            ("05", "Cantilevered Stargazer Auditorium & Memory Crystal Spire", "Overhanging Lecture Hall • UV-Violet Optical Memory Core Tower • Plaza Plinth"),
        ]
    },
    "bldg_19": {
        "category": "buildings",
        "slug": "bldg_19_synth_brewery_refinery",
        "title": "BUILDING 19: BIOREACTOR PROTEIN REFINERY & BOTANICAL DISTILLATION PLANT (5-CHOICE TEST)",
        "sub": "District IV: Shipyard, Arena, Museum & Defense • Cellular Fermentation Hall • Translucent Zero-G Distillation Tower • Vote 01–05",
        "cands": [
            ("01", "Octagonal Fermentation Hall & Copper/Steel Still Crown", "Central Fermentation Plant • Rooftop Distillation Domes • Bioreactor Vats"),
            ("02", "Dual-Zone Split Protein Refinery & Botanical Still Tower", "Aegis-7 65/35 Split-Mass • Bioreactor Refinery + Translucent Amber/Cyan Distillation Column"),
            ("03", "Quad-Vat Bioreactor Array & Automated Bottling Hall", "Four External Fermentation Cylinders • Bottling Logistics Bay • Transfer Pipes"),
            ("04", "Twin-Silo Cellular Agriculture Plant & Tasting Atrium", "Dual Protein Silos • Glazed Visitor Tasting Lounge • Signal-Orange Valves"),
            ("05", "Heavy Industrial Nutrient Fractionation & Storage Complex", "Refinery Pipe-Rack Block • Overhead Transfer Gantries • Tanker Dock"),
        ]
    },
    "bldg_20": {
        "category": "buildings",
        "slug": "bldg_20_meteor_defense_bastion",
        "title": "BUILDING 20: POINT-DEFENSE LASER BASTION & TACHYON RELAY TOWER (5-CHOICE TEST)",
        "sub": "District IV: Shipyard, Arena, Museum & Defense • Coherent Laser Turret Bastion • Translucent Tachyon Beam-Relay Spire • Vote 01–05",
        "cands": [
            ("01", "Armored Octagonal Point-Defense Turret & Shield Citadel", "Fortified Octagonal Bastion • Heavy Dual-Barrel Laser Turret • Heat-Sink Fins"),
            ("02", "Dual-Zone Split Defense Bastion & Tachyon Beam-Relay Tower", "Aegis-7 65/35 Split-Mass • Laser Turret Bastion + Translucent 5-Lens Tachyon Relay Spire"),
            ("03", "Twin-Turret Meteoroid Interceptor & Radar Bunker", "Dual Elevated Laser Turrets • Central Fire-Control Radar Dome • Ordinance Airlock"),
            ("04", "Stepped Capacitor Fortress & Subspace Phased-Array Spire", "Tiered Armor Bunker • Angled Phased-Array Radar Panel • Pulse Capacitors"),
            ("05", "Cantilevered Deep-Space Overwatch Battery & Comms Pylon", "Overhanging Gun-Battery Deck • Tall Deep-Space Comms Mast • Shielded Plinth"),
        ]
    },
}

BUILDINGS_META.update(PHASE3_META)


def get_cyl_stats():
    stats = {}
    cpath = "./assets/glb/cylinder/cylinder_r1_manifest.json"
    if os.path.exists(cpath):
        try:
            with open(cpath, "r") as f:
                for item in json.load(f):
                    stats[os.path.basename(item.get("filepath", ""))] = item
        except Exception:
            pass
    return stats

def get_phase3_stats():
    stats = {}
    p3_path = "./assets/glb/buildings/phase3_50_manifest.json"
    if os.path.exists(p3_path):
        try:
            with open(p3_path, "r") as f:
                data = json.load(f)
            for k in ["props_25", "buildings_district4_25"]:
                for item in data.get(k, []):
                    fn = os.path.basename(item.get("filepath", ""))
                    stats[fn] = item
        except Exception:
            pass
    return stats


def compose_any_voting_sheet(tid: str):
    if tid not in BUILDINGS_META:
        return False
    meta = BUILDINGS_META[tid]
    cat = meta.get("category", "buildings")
    rdir = f"./godot/renders/{cat}/{tid}" if cat != "cylinder" else "./godot/renders/cylinder"
    adir = f"./assets/renders/{cat}/{tid}" if cat != "cylinder" else "./assets/renders/cylinder"

    for i in range(1, 6):
        p = os.path.join(rdir, f"{tid}_r1_{i:02d}.png")
        if not os.path.exists(p):
            return False

    stats_map = get_manifest_stats(tid)
    stats_map.update(get_phase3_stats())
    stats_map.update(get_cyl_stats())
    stats_map.update(get_setpiece_stats())

    cols, rows = 3, 2
    cell_w, cell_img_h, cell_footer_h = 880, 495, 92
    cell_h = cell_img_h + cell_footer_h
    pad, header_h = 22, 108

    canvas_w = pad + cols * (cell_w + pad)
    canvas_h = header_h + pad + rows * (cell_h + pad)

    sheet = Image.new("RGB", (canvas_w, canvas_h), (12, 15, 20))
    draw = ImageDraw.Draw(sheet)

    font_title = load_font(28, bold=True)
    font_sub = load_font(16, bold=False)
    font_badge = load_font(22, bold=True)
    font_tris = load_font(15, bold=True)
    font_card_title = load_font(17, bold=True)
    font_card_desc = load_font(14, bold=False)

    draw.rectangle([0, 0, canvas_w, header_h], fill=(18, 22, 30))
    draw.line([(0, header_h - 2), (canvas_w, header_h - 2)], fill=(0, 229, 255), width=3)
    draw.text((pad, 20), f"CYLINDER HAB-7 — {meta['title']}", fill=(232, 242, 255), font=font_title)
    draw.text((pad, 64), meta["sub"], fill=(0, 215, 245), font=font_sub)

    for idx, (num_str, ctitle, cdesc) in enumerate(meta["cands"]):
        r, c = idx // cols, idx % cols
        if r == 1:
            row2_w = 2 * cell_w + pad
            start_x = (canvas_w - row2_w) // 2
            x0 = start_x + c * (cell_w + pad)
        else:
            x0 = pad + c * (cell_w + pad)
        y0 = header_h + pad + r * (cell_h + pad)

        is_hero = (num_str == "02")
        outline_col = (0, 229, 255) if is_hero else (48, 72, 96)
        draw.rounded_rectangle(
            [x0 - 2, y0 - 2, x0 + cell_w + 2, y0 + cell_h + 2],
            radius=10,
            fill=(22, 27, 36),
            outline=outline_col,
            width=3 if is_hero else 2,
        )

        img_path = os.path.join(rdir, f"{tid}_r1_{num_str}.png")
        im = Image.open(img_path).convert("RGB").resize((cell_w, cell_img_h), Image.Resampling.LANCZOS)
        sheet.paste(im, (x0, y0))

        draw.rounded_rectangle([x0 + 12, y0 + 12, x0 + 68, y0 + 50], radius=6, fill=(0, 210, 245))
        draw.text((x0 + 23, y0 + 17), num_str, fill=(10, 14, 20), font=font_badge)

        glb_fn = f"{tid}_r1_{num_str}.glb"
        st = stats_map.get(glb_fn, {})
        tris = st.get("triangles", st.get("tris", 0))
        dims = st.get("dimensions", [12.0, 18.0, 10.0])
        stat_txt = f"{glb_fn} | {tris:,} Tris" if tris else f"{glb_fn} | Aegis-7 Standard"
        draw.rounded_rectangle([x0 + cell_w - 310, y0 + 12, x0 + cell_w - 12, y0 + 44], radius=6, fill=(14, 18, 25))
        draw.text((x0 + cell_w - 298, y0 + 19), stat_txt, fill=(190, 225, 255), font=font_tris)

        fy0 = y0 + cell_img_h
        draw.rectangle([x0, fy0, x0 + cell_w, y0 + cell_h], fill=(16, 20, 27))
        draw.text((x0 + 14, fy0 + 10), f"#{num_str} — {ctitle}", fill=(235, 244, 255), font=font_card_title)
        draw.text((x0 + 14, fy0 + 38), cdesc, fill=(0, 215, 245), font=font_card_desc)
        if dims and len(dims) == 3:
            dim_str = f"Envelope: {dims[0]:.1f}m W × {dims[2]:.1f}m D × {dims[1]:.1f}m H • Aegis-7 PBR + Translucent Glass"
        else:
            dim_str = "Envelope: Aegis-7 Standard PBR + Translucent Glass"
        draw.text((x0 + 14, fy0 + 62), dim_str, fill=(155, 175, 198), font=font_card_desc)

    slug = meta["slug"]
    for d in [rdir, adir]:
        os.makedirs(d, exist_ok=True)
        for sname in [f"{tid}_round1_voting_sheet.png", f"{slug}_round1_voting_sheet.png"]:
            out_p = os.path.join(d, sname)
            sheet.save(out_p, "PNG", compress_level=4)
            print(f"[VotingSheet] Saved {out_p} ({canvas_w}x{canvas_h})")
    return True


BUILDINGS_META["cylinder"] = {
    "category": "cylinder",
    "slug": "cylinder_hab7_fullscale",
    "title": "FULL-SCALE (800m × 400m) O'NEILL CYLINDER HAB-7 MEGASHIP (5-CHOICE TEST)",
    "sub": "1:1 Macro Orbital Habitat (800m L × 400m Ø) • Translucent Solariums • Axial Zero-G Solar Spine • 5-Coil D-He3 Fusion Drive • Vote 01–05",
    "cands": [
        ("01", "Classic 3-Land / 3-Window Alternating Solarium Cylinder", "7 Gunmetal Spin-Ribs • 3 Translucent Solariums • Articulated Aft Solar Mirror Wings"),
        ("02", "Aegis-7 Dual-Zone Split Habitat Drum & Zero-G Starport", "65/35 Split-Mass • 520m Spin-Gravity Habitat Drum + 280m Zero-G Starport & 5-Coil Fusion Drive"),
        ("03", "Hexagonal Geodesic Macro-Truss & Ring-Sea Biosphere", "Central Equatorial Ring-Sea Reservoir • 4 Emerald Conservatory Quadrants • Axial Solar Spine"),
        ("04", "Heavy Whipple-Shielded Deep-Space Bastion Cylinder", "Layered Gunmetal/Slate Whipple Armor • 4 Point-Defense Laser Sponsons • Slit Solariums"),
        ("05", "Modular 5-Ring Sectorized Metropolis & Shipyard Hub", "5 Counter-Rotating Habitat Drums • 4 Translucent Observation Sky-Ring Joints • Fusion Drive"),
    ]
}


def get_setpiece_stats():
    stats = {}
    sp_path = "./assets/glb/cylinder_interior/cylinder_interior_overhaul_manifest.json"
    if os.path.exists(sp_path):
        try:
            with open(sp_path, "r") as f:
                data = json.load(f)
            for item in data.get("setpieces_25", []):
                fn = os.path.basename(item.get("filepath", ""))
                stats[fn] = item
        except Exception:
            pass
    return stats

BUILDINGS_META.update({
    "interior_setpiece_01": {
        "category": "cylinder_interior",
        "slug": "interior_setpiece_01_ring_skybridge_viaduct",
        "title": "INTERIOR SETPIECE 01: 120° RING-SPANNING SUSPENSION SKYBRIDGE & VIADUCT (5-CHOICE TEST)",
        "sub": "Cylinder Interior Macro-Landmark • Curved Mag-Lev Viaduct Arch • Translucent Mid-Span Sky-Transfer Rotunda • Vote 01–05",
        "cands": [
            ("01", "Symmetric Twin-Pylon Curved Mag-Lev Viaduct Arch", "Twin Suspension Pylons • Curved Dual-Track Mag-Lev Deck • Brushed-Steel Stay Cables"),
            ("02", "Dual-Zone Split Suspension Viaduct & Sky-Transfer Rotunda", "Aegis-7 65/35 Split-Mass • Curved Mag-Lev Viaduct + Translucent Mid-Span Sky-Transfer Rotunda"),
            ("03", "Tri-Chord Space-Frame Truss Skybridge & Cargo Rail", "Heavy Space-Frame Truss Arch • Intermodal Shuttle Track • Cyan Induction Rails"),
            ("04", "Cantilevered Solarium Overlook Arch & Botanical Promenade", "Tiered Botanical Sky-Park Deck • Translucent Emerald Canopy • Pedestrian Overlook"),
            ("05", "Heavy Buttressed Ring-Highway Interchange & Drone Pylon", "Chamfered Basalt-Titanium Pylons • Multi-Level Transit Deck • Aviation Warning Beacons"),
        ]
    },
    "interior_setpiece_02": {
        "category": "cylinder_interior",
        "slug": "interior_setpiece_02_terraced_waterfall_reservoir",
        "title": "INTERIOR SETPIECE 02: STEPPED HYDRO-DAM, WATERFALL CASCADE & BIODOME DELTA (5-CHOICE TEST)",
        "sub": "Valley B Macro-Landmark • Specular Ring-River Spillway • Terraced Emerald Botanical Ziggurat • Vote 01–05",
        "cands": [
            ("01", "Symmetric Stepped Octagonal Hydro-Dam & Reservoir Basin", "4-Tier Basalt-Titanium Weir • Specular Ring-River Basin • Copper-Anodized Footbridge"),
            ("02", "Dual-Zone Split Hydro-Dam Spillway & Emerald Biodome Ziggurat", "Aegis-7 65/35 Split-Mass • Cascading Hydro-Dam + Translucent Emerald Botanical Peninsula"),
            ("03", "Twin-Spillway Aquifer Basin & Floating Hydroponic Islands", "Dual Floodgate Spillways • Terraced Canopy Islands • Bioluminescent Emerald Strips"),
            ("04", "Terraced Botanical Canyon & Mist-Scrubber Cascade", "Stepped Arboretum Cliffs • UV-Violet & Emerald Bio-Filters • Specular River Delta"),
            ("05", "Cantilevered Reservoir Overlook Dam & Intake Rotunda", "Projecting Hydro-Control Rotunda • High-Flow Turbine Weirs • Copper Arch Bridge"),
        ]
    },
    "interior_setpiece_03": {
        "category": "cylinder_interior",
        "slug": "interior_setpiece_03_axial_suncore_spoke_hub",
        "title": "INTERIOR SETPIECE 03: GOLDEN-HOUR AXIAL SUN-CORE & RADIAL SPOKE HUB (5-CHOICE TEST)",
        "sub": "Central Zero-G Axis Landmark • Golden-Hour Heliostat Louvers • Radial Tether-Elevator Spokes • Vote 01–05",
        "cands": [
            ("01", "Symmetric 3-Spoke Axial Hub & Golden Daylight Tube", "Golden-Hour Solar Core • 3 Radial Elevator Spoke Collars • Brushed-Steel Louver Rings"),
            ("02", "Dual-Zone Split Axial Transfer Hub & Heliostat Plasma Spine", "Aegis-7 65/35 Split-Mass • Articulated Heliostat Louver Spine + Translucent Zero-G Docking Sphere"),
            ("03", "Hexagonal Geodesic Sun-Core Truss & Cable-Car Spokes", "Geodesic Solar Truss Cage • Radial Tether Climber Cars • Amber/Cyan Field Rings"),
            ("04", "Twin-Node Axial Climate Controller & Heliostat Wing Array", "Dual Barometric Control Nodes • Articulated Daylight Reflectors • Zero-G Shuttle Berths"),
            ("05", "Heavy Armored Spin-Bearing Hub & Radial Umbilical Conduits", "Chamfered Gunmetal Spin-Bearing • High-Tension Spoke Cables • Golden Solar Sheath"),
        ]
    },
    "interior_setpiece_04": {
        "category": "cylinder_interior",
        "slug": "interior_setpiece_04_endcap_cliffside_citadel",
        "title": "INTERIOR SETPIECE 04: FORWARD ENDCAP CLIFFSIDE TERRACES & FUNICULAR BOWL (5-CHOICE TEST)",
        "sub": "Forward Bulkhead Macro-Landmark • 5-Tier Hanging Cliff Terraces • Translucent Radial Funicular Spine • Vote 01–05",
        "cands": [
            ("01", "Concentric Stepped Octagonal Bulkhead Amphitheater Bowl", "5-Tier Basalt-Titanium Cliff Terraces • Warm Amber Retaining Strips • Botanical Ledges"),
            ("02", "Dual-Zone Split Cliffside Hanging Terraces & Funicular Spine", "Aegis-7 65/35 Split-Mass • Stepped Cliffside Citadel + Full-Height Translucent Radial Funicular Tube"),
            ("03", "Tri-Radial Bulkhead Buttress Ribs & Overlook Balconies", "Heavy Radial Structural Buttresses • Cantilevered Civic Balconies • Warm Amber Windows"),
            ("04", "Terraced Botanical Hanging Gardens & Endcap Reservoir Weir", "Stepped Arboretum Cliff Decks • High-Altitude Cascade Basin • Axial Docking Collar"),
            ("05", "Heavy Armored Spin-Bulkhead Shield Wall & Funicular Gantry", "Chamfered Gunmetal Bulkhead Tiers • Pressurized Ascent Rail • Signal-Orange Airlocks"),
        ]
    },
    "interior_setpiece_05": {
        "category": "cylinder_interior",
        "slug": "interior_setpiece_05_elevated_plaza_interchange",
        "title": "INTERIOR SETPIECE 05: ASYMMETRIC CIVIC ACROPOLIS & SKYWALK INTERCHANGE (5-CHOICE TEST)",
        "sub": "Valley A Macro-Landmark • 3-Tier Stepped Urban Canyon • Diagonal Skybridges & Holo-Amphitheater • Vote 01–05",
        "cands": [
            ("01", "Octagonal 3-Tier Concentric Acropolis Plaza Podium", "Travertine-Alloy Promenade Decks • Basalt Retaining Walls • Warm Amber Stair Nosings"),
            ("02", "Dual-Zone Split 3-Tier Acropolis Podium & Holo-Amphitheater", "Aegis-7 65/35 Split-Mass • Stepped Civic Canyon & Diagonal Skywalks + Translucent Galleria Dome"),
            ("03", "Twin-Bridge Elevated Boulevard Canyon & Transit Rotunda Deck", "Dual Diagonal Pedestrian Skybridges • Sunken Canal Plaza • Warm Amber Residential Base"),
            ("04", "Terraced Civic Promenade Steps & Canal-Spanning Arcade", "Grand Monumental Staircase • Glazed Waterfront Arcade • Octagonal Citadel Plinth"),
            ("05", "Cantilevered Overlook Podium & Multi-Level Skywalk Hub", "Projecting Civic Overlook Deck • Brushed-Steel Skywalk Truss • VIP Shuttle Clamps"),
        ]
    },
})

if __name__ == "__main__":
    targets = sys.argv[1:] if len(sys.argv) > 1 else ([f"prop_{i:02d}" for i in range(1, 6)] + [f"bldg_{i:02d}" for i in range(16, 21)])
    for t in targets:
        compose_any_voting_sheet(t)
