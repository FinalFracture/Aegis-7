#!/usr/bin/env python3
"""
Builds all 10 Round-2 Hard Sci-Fi Bunk Pod Tournament .glb models:
/workspace/game-project/assets/glb/bunk_round2/bunk_r2_01.glb .. bunk_r2_10.glb

Every candidate features:
- Sleek chamfered titanium / aerospace-composite / brushed-steel hard-surface hulls
- Organic contoured flight-couch mattresses, cranial cradles, and zero-G bolsters
- Ultra-clean low-noise PBR materials mapped to Sloane's textures in /workspace/game-project/assets/textures/bunk_round2/
- True open geometric viewport cutouts (zero opaque backing blocking sightlines)
- True alphaMode: "BLEND" translucent glass viewports & canopies (alpha ~ 0.22)
- Triangle budget: ~2,500 - 5,500 triangles per candidate, min Y == 0.0000, centered X/Z.
"""
import os
import sys
import math
import json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glb_builder import (
    PBRMaterialDef,
    SubMesh,
    transform_geom,
    merge_geometries,
    make_lathe_dome,
    sample_filleted_polyline,
    make_swept_tube,
    make_sculpted_cushion,
    make_draped_blanket,
    make_beveled_box,
    make_cylinder,
    make_quad_panel,
    export_glb,
)
from bunk_round1_generator import (
    hex_rgba,
    add_part,
    center_and_export_glb,
    make_chamfered_aperture_ring,
    make_contoured_flight_couch,
    make_cranial_head_cradle,
    make_curved_canopy_shield,
)

TEX_R2_DIR = "/workspace/game-project/assets/textures/bunk_round2"
OUT_GLB_DIR = "/workspace/game-project/assets/glb/bunk_round2"
os.makedirs(OUT_GLB_DIR, exist_ok=True)


def tex_r2(fname: str) -> str:
    return os.path.join(TEX_R2_DIR, fname)


def get_r2_materials():
    return {
        "gunmetal": PBRMaterialDef(
            name="Mat_Titanium_GunmetalDark",
            base_color=hex_rgba("#1A1E24"),
            metallic=0.78,
            roughness=0.34,
            texture_path=tex_r2("titanium_gunmetal_dark.png"),
        ),
        "aero_white": PBRMaterialDef(
            name="Mat_Composite_AerospaceWhite",
            base_color=hex_rgba("#DCE2EA"),
            metallic=0.08,
            roughness=0.30,
            texture_path=tex_r2("composite_aerospace_white.png"),
        ),
        "carbon_slate": PBRMaterialDef(
            name="Mat_Carbon_SlateStructural",
            base_color=hex_rgba("#282E38"),
            metallic=0.55,
            roughness=0.42,
            texture_path=tex_r2("carbon_slate_structural.png"),
        ),
        "steel_machined": PBRMaterialDef(
            name="Mat_Steel_BrushedMachined",
            base_color=hex_rgba("#88929E"),
            metallic=0.88,
            roughness=0.24,
            texture_path=tex_r2("steel_brushed_machined.png"),
        ),
        "pad_charcoal": PBRMaterialDef(
            name="Mat_Fabric_CharcoalFlightpad",
            base_color=hex_rgba("#252A32"),
            metallic=0.02,
            roughness=0.78,
            texture_path=tex_r2("fabric_charcoal_flightpad.png"),
        ),
        "pad_navy": PBRMaterialDef(
            name="Mat_Fabric_OrbitalNavyPad",
            base_color=hex_rgba("#1E2D3D"),
            metallic=0.02,
            roughness=0.76,
            texture_path=tex_r2("fabric_orbital_navy_pad.png"),
            double_sided=True,
        ),
        "pad_slate": PBRMaterialDef(
            name="Mat_Fabric_SlateGreyCushion",
            base_color=hex_rgba("#4A5564"),
            metallic=0.02,
            roughness=0.78,
            texture_path=tex_r2("fabric_slate_grey_cushion.png"),
            double_sided=True,
        ),
        "accent_orange": PBRMaterialDef(
            name="Mat_Accent_SignalOrange",
            base_color=hex_rgba("#D95B26"),
            metallic=0.05,
            roughness=0.50,
            texture_path=tex_r2("accent_signal_orange.png"),
        ),
        "glass_viewport": PBRMaterialDef(
            name="Mat_Viewport_Glass_Translucent",
            base_color=(0.55, 0.85, 1.0, 0.22),
            metallic=0.10,
            roughness=0.08,
            emissive=(0.0, 0.12, 0.18),
            texture_path=tex_r2("glass_viewport_translucent.png"),
            double_sided=True,
            alpha_mode="BLEND",
        ),
        "glass_holo_visor": PBRMaterialDef(
            name="Mat_Glass_HoloVisor_Translucent",
            base_color=(0.45, 0.92, 1.0, 0.24),
            metallic=0.12,
            roughness=0.08,
            emissive=(0.0, 0.20, 0.28),
            texture_path=tex_r2("glass_holo_visor_cyan.png"),
            double_sided=True,
            alpha_mode="BLEND",
        ),
        "oled_hud": PBRMaterialDef(
            name="Mat_OLED_TelemetryHUD",
            base_color=hex_rgba("#0A0E14"),
            metallic=0.10,
            roughness=0.15,
            emissive=(0.15, 0.72, 0.92),
            texture_path=tex_r2("oled_telemetry_hud.png"),
        ),
        "led_cyan": PBRMaterialDef(
            name="Mat_Emissive_CyanLED",
            base_color=hex_rgba("#00E5FF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.0, 0.90, 1.0),
        ),
        "led_amber": PBRMaterialDef(
            name="Mat_Emissive_AmberLED",
            base_color=hex_rgba("#FF9500"),
            metallic=0.0,
            roughness=0.15,
            emissive=(1.0, 0.58, 0.0),
        ),
        "led_ice": PBRMaterialDef(
            name="Mat_Emissive_IceWhiteLED",
            base_color=hex_rgba("#E0F4FF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.86, 0.95, 1.0),
        ),
    }


def make_open_backwall_frame(
    total_w: float = 2.04,
    total_h: float = 1.48,
    center_y: float = 1.12,
    z_pos: float = -0.50,
    win_w: float = 1.52,
    win_h: float = 0.82,
    win_cy: float = 1.16,
    thick_z: float = 0.10,
):
    """
    Builds a 4-piece rear bulkhead wall with a TRUE OPEN CUTOUT (zero polygons inside the window rectangle).
    """
    y_min = center_y - total_h * 0.5
    y_max = center_y + total_h * 0.5
    wy0 = win_cy - win_h * 0.5
    wy1 = win_cy + win_h * 0.5

    sill_h = max(0.08, wy0 - y_min)
    head_h = max(0.08, y_max - wy1)
    pillar_w = max(0.10, (total_w - win_w) * 0.5)
    pillar_x = win_w * 0.5 + pillar_w * 0.5

    parts = [
        # Lower sill below window
        make_beveled_box((total_w, sill_h, thick_z), center=(0.0, y_min + sill_h * 0.5, z_pos), bevel=0.02),
        # Upper header above window
        make_beveled_box((total_w, head_h, thick_z), center=(0.0, wy1 + head_h * 0.5, z_pos), bevel=0.02),
        # Left & right pillars flanking window cutout
        make_beveled_box((pillar_w, win_h + 0.04, thick_z), center=(-pillar_x, win_cy, z_pos), bevel=0.02),
        make_beveled_box((pillar_w, win_h + 0.04, thick_z), center=(pillar_x, win_cy, z_pos), bevel=0.02),
    ]
    return merge_geometries(parts)


# ==============================================================================
# 01: CURVED BUBBLE-GLASS HULL BLISTER BERTH (`bunk_r2_01.glb`)
# ==============================================================================
def build_01_panoramic_hull_blister_pod(mats):
    sm = []
    # 1. Chamfered Dark Gunmetal Titanium lower berth & side bulkheads (rear & top vault left wide open!)
    chassis = [
        make_beveled_box((2.18, 0.38, 1.16), center=(0.0, 0.19, 0.0), bevel=0.035),
        make_beveled_box((0.15, 1.56, 1.14), center=(-1.02, 0.94, 0.0), bevel=0.04),
        make_beveled_box((0.15, 1.56, 1.14), center=(1.02, 0.94, 0.0), bevel=0.04),
        # Low rear sill only (Y = 0.36 to 0.62) so entire Y = 0.62..1.90 rear & roof vault is open
        make_beveled_box((1.96, 0.26, 0.10), center=(0.0, 0.49, -0.50), bevel=0.02),
        make_beveled_box((2.18, 0.12, 0.24), center=(0.0, 1.84, 0.38), bevel=0.025),
    ]
    add_part(sm, "BlisterPod_GunmetalChassis", merge_geometries(chassis), mats["gunmetal"])

    # 2. 4 Curved Machined-Steel Blister Ribs arching from rear sill (Z=-0.50, Y=0.60) up to front header (Z=+0.36, Y=1.84)
    ribs = [
        make_chamfered_aperture_ring(1.98, 1.32, center_y=1.14, z_pos=0.48, tube_r=0.045, chamfer=0.26),
    ]
    for rx in [-0.92, -0.32, 0.32, 0.92]:
        arc_pts = []
        for k in range(15):
            t = k / 14.0
            ang = math.radians(t * 95.0)
            pz = 0.28 - 0.78 * math.cos(ang)
            py = 0.60 + 1.24 * math.sin(ang)
            arc_pts.append([rx, py, pz])
        ribs.append(make_swept_tube(np.array(arc_pts, dtype=np.float32), radius=0.034, radial_segments=10, oval_scale=(0.8, 1.4)))
    add_part(sm, "BlisterPod_MachinedSteelRibs", merge_geometries(ribs), mats["steel_machined"])

    # 3. Sweeping Curved Bubble-Glass Translucent Observation Blister (alphaMode: "BLEND")
    blister_glass = make_curved_canopy_shield(
        width_x=1.84,
        center_x=0.0,
        radius_yz=0.92,
        center_y=0.62,
        center_z=0.36,
        ang_start_deg=92.0,
        ang_end_deg=182.0,
        segs_arc=14,
    )
    add_part(sm, "BlisterPod_TranslucentBlisterGlass", blister_glass, mats["glass_viewport"])

    # 4. Contoured Charcoal Flight Couch + Slate Bolsters + Draped Navy Coverlet
    add_part(sm, "BlisterPod_CharcoalFlightCouch", make_contoured_flight_couch(1.86, 0.90, base_y=0.46, res=(7, 3, 5)), mats["pad_charcoal"])
    add_part(sm, "BlisterPod_SlateHeadCradle", make_cranial_head_cradle(center=(-0.68, 0.57, 0.0)), mats["pad_slate"])
    add_part(
        sm,
        "BlisterPod_DrapedNavyCoverlet",
        make_draped_blanket(1.06, 0.88, top_y=0.54, drape_drop=0.18, center_xz=(0.24, 0.02), res_x=11, res_z=13),
        mats["pad_navy"],
    )

    # 5. Signal-Orange Grab Bars + Side OLED Console + Cyan Perimeter Lighting
    grab_l = sample_filleted_polyline([(-0.92, 0.72, 0.52), (-0.92, 0.72, 0.60), (-0.92, 1.26, 0.60), (-0.92, 1.26, 0.52)], 0.04, 5)
    add_part(sm, "BlisterPod_SignalOrangeGrabBar", make_swept_tube(grab_l, 0.018, 10), mats["accent_orange"])
    add_part(
        sm,
        "BlisterPod_SideOLEDConsole",
        make_quad_panel((-0.93, 0.88, -0.32), (-0.93, 0.88, 0.12), (-0.93, 1.18, 0.12), (-0.93, 1.18, -0.32)),
        mats["oled_hud"],
    )
    cyan_strips = [
        make_beveled_box((1.76, 0.026, 0.06), center=(0.0, 1.76, 0.28), bevel=0.005),
        make_beveled_box((1.76, 0.022, 0.04), center=(0.0, 0.61, -0.46), bevel=0.004),
    ]
    add_part(sm, "BlisterPod_CyanPerimeterLED", merge_geometries(cyan_strips), mats["led_cyan"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bunk_r2_01.glb"), sm, root_name="BunkR2_01_PanoramicHullBlisterPod")


# ==============================================================================
# 02: DEEP HEXAGONAL APERTURE POD (`bunk_r2_02.glb`)
# ==============================================================================
def build_02_hex_aperture_sleep_chamber(mats):
    sm = []
    # 1. Outer Carbon-Slate Hexagonal Collar & Stepped Entry Sill
    outer_collar = [
        make_beveled_box((2.20, 0.34, 1.20), center=(0.0, 0.17, 0.0), bevel=0.035),
        make_beveled_box((1.62, 0.14, 0.22), center=(0.0, 0.07, 0.62), bevel=0.02),
        make_chamfered_aperture_ring(2.12, 1.48, center_y=1.08, z_pos=0.52, tube_r=0.065, chamfer=0.38),
        make_chamfered_aperture_ring(1.66, 0.92, center_y=1.16, z_pos=-0.46, tube_r=0.048, chamfer=0.26),
    ]
    add_part(sm, "HexPod_CarbonSlateHexCollar", merge_geometries(outer_collar), mats["carbon_slate"])

    # 2. Inner Matte Aerospace White Chamfered Chamber with Open Rear Hex Viewport Cutout
    white_liner = [
        make_beveled_box((2.16, 0.20, 1.14), center=(0.0, 1.82, 0.0), bevel=0.035),
        make_beveled_box((0.15, 1.62, 1.12), center=(-1.01, 1.02, 0.0), bevel=0.035),
        make_beveled_box((0.15, 1.62, 1.12), center=(1.01, 1.02, 0.0), bevel=0.035),
        make_open_backwall_frame(total_w=1.96, total_h=1.52, center_y=1.10, z_pos=-0.50, win_w=1.54, win_h=0.84, win_cy=1.16),
    ]
    add_part(sm, "HexPod_AerospaceWhiteLiner", merge_geometries(white_liner), mats["aero_white"])

    # 3. Rear Hex Translucent Viewport Glass + Front-Left Translucent Head Draft Partition (alphaMode: "BLEND")
    glass_panes = [
        make_quad_panel((-0.78, 0.74, -0.47), (0.78, 0.74, -0.47), (0.78, 1.58, -0.47), (-0.78, 1.58, -0.47)),
        make_quad_panel((-0.94, 0.44, 0.46), (-0.36, 0.44, 0.46), (-0.36, 1.58, 0.46), (-0.94, 1.58, 0.46)),
    ]
    add_part(sm, "HexPod_TranslucentViewportAndPartition", merge_geometries(glass_panes), mats["glass_viewport"])

    # 4. Orbital Navy Contoured Flight Couch + Slate Bolsters
    add_part(sm, "HexPod_OrbitalNavyFlightCouch", make_contoured_flight_couch(1.86, 0.90, base_y=0.45, res=(7, 3, 5)), mats["pad_navy"])
    bolsters = [
        make_cranial_head_cradle(center=(-0.66, 0.56, 0.0)),
        make_draped_blanket(1.04, 0.88, top_y=0.53, drape_drop=0.18, center_xz=(0.24, 0.02), res_x=11, res_z=12),
    ]
    add_part(sm, "HexPod_SlateBolsterAndCoverlet", merge_geometries(bolsters), mats["pad_slate"])

    # 5. Dual Cyan Upper Cove + Warm Amber Step Cove
    add_part(sm, "HexPod_UpperCyanCove", make_beveled_box((1.62, 0.028, 0.06), center=(0.0, 1.70, 0.12), bevel=0.005), mats["led_cyan"])
    add_part(sm, "HexPod_LowerAmberStepCove", make_beveled_box((1.48, 0.024, 0.04), center=(0.0, 0.16, 0.72), bevel=0.004), mats["led_amber"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bunk_r2_02.glb"), sm, root_name="BunkR2_02_HexApertureSleepChamber")


# ==============================================================================
# 03: TORPEDO-BAY STYLE RECESSED RACK (`bunk_r2_03.glb`)
# ==============================================================================
def build_03_corvette_submarine_rack(mats):
    sm = []
    # 1. Dark Gunmetal Corvette Berth Hull with Open Horizontal Slit Viewport Cutout & Side Gear Lockers
    bay_hull = [
        make_beveled_box((2.20, 0.36, 1.16), center=(0.0, 0.18, 0.0), bevel=0.03),
        make_beveled_box((2.20, 0.18, 1.16), center=(0.0, 1.80, 0.0), bevel=0.03),
        make_beveled_box((0.14, 1.62, 1.14), center=(-1.03, 0.99, 0.0), bevel=0.03),
        # Right side integrated tactical gear locker column
        make_beveled_box((0.28, 1.62, 1.14), center=(0.96, 0.99, 0.0), bevel=0.03),
        make_open_backwall_frame(total_w=1.84, total_h=1.50, center_y=1.08, z_pos=-0.50, win_w=1.56, win_h=0.62, win_cy=1.18),
    ]
    add_part(sm, "CorvetteRack_GunmetalHullAndLockers", merge_geometries(bay_hull), mats["gunmetal"])

    # 2. 4 Curved Machined-Steel Rib Arches & Horizontal Slit Viewport Bezel
    steel_parts = [
        make_chamfered_aperture_ring(1.62, 0.68, center_y=1.18, z_pos=-0.45, tube_r=0.042, chamfer=0.16),
    ]
    for rx in [-0.94, -0.34, 0.26, 0.82]:
        rib_pts = sample_filleted_polyline(
            [(rx, 0.34, 0.54), (rx, 0.34, -0.48), (rx, 1.74, -0.48), (rx, 1.74, 0.52)],
            fillet_radius=0.20,
            corner_subdivs=6,
        )
        steel_parts.append(make_swept_tube(rib_pts, radius=0.046, radial_segments=10, oval_scale=(0.8, 1.4)))
    add_part(sm, "CorvetteRack_MachinedRibArches", merge_geometries(steel_parts), mats["steel_machined"])

    # 3. Horizontal Hull Slit Translucent Viewport Glass (alphaMode: "BLEND")
    add_part(
        sm,
        "CorvetteRack_TranslucentSlitViewport",
        make_quad_panel((-0.79, 0.86, -0.47), (0.79, 0.86, -0.47), (0.79, 1.50, -0.47), (-0.79, 1.50, -0.47)),
        mats["glass_viewport"],
    )

    # 4. Contoured Charcoal Flight Couch + Angled Fold-Down Upper Technical Baffle
    baffle_and_couch = [
        make_contoured_flight_couch(1.74, 0.88, base_y=0.45, res=(6, 3, 5)),
        transform_geom(
            make_beveled_box((1.68, 0.26, 0.05), center=(0.0, 0.0, 0.0), bevel=0.015),
            translate=(-0.06, 1.58, 0.48),
            rot_xyz_deg=(-28.0, 0.0, 0.0),
        ),
    ]
    add_part(sm, "CorvetteRack_FlightCouchAndBaffle", merge_geometries(baffle_and_couch), mats["pad_charcoal"])
    add_part(sm, "CorvetteRack_SlateHeadCradle", make_cranial_head_cradle(center=(-0.68, 0.56, 0.0)), mats["pad_slate"])

    # 5. Signal-Orange Tactical Straps & Grab Handles + Amber/Cyan Practical Strips
    orange_parts = [
        make_beveled_box((0.06, 0.28, 0.04), center=(-0.94, 1.04, 0.57), bevel=0.008),
        make_beveled_box((0.06, 0.28, 0.04), center=(0.82, 1.04, 0.57), bevel=0.008),
    ]
    add_part(sm, "CorvetteRack_SignalOrangeHandles", merge_geometries(orange_parts), mats["accent_orange"])
    add_part(sm, "CorvetteRack_AmberBaffleLED", make_beveled_box((1.56, 0.025, 0.05), center=(-0.06, 1.68, 0.36), bevel=0.005), mats["led_amber"])
    add_part(sm, "CorvetteRack_CyanViewportRim", make_beveled_box((1.50, 0.020, 0.04), center=(0.0, 0.85, -0.43), bevel=0.004), mats["led_cyan"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bunk_r2_03.glb"), sm, root_name="BunkR2_03_CorvetteSubmarineRack")


# ==============================================================================
# 04: FIGHTER-CANOPY GULLWING SLEEP POD (`bunk_r2_04.glb`)
# ==============================================================================
def build_04_sliding_canopy_cockpit_pod(mats):
    sm = []
    # 1. Aerospace White & Carbon-Slate Sloped Cockpit Monocoque Tub with Open Rear Viewport Cutout
    cockpit_tub = [
        make_sculpted_cushion((2.18, 0.34, 1.16), center=(0.0, 0.17, 0.0), res=(6, 3, 5), roundness=0.22, belly_puff=0.02, pinch_corners=0.0, crease_freq=0),
        make_beveled_box((0.15, 1.48, 1.14), center=(-1.02, 0.90, 0.0), bevel=0.04),
        make_beveled_box((0.15, 1.48, 1.14), center=(1.02, 0.90, 0.0), bevel=0.04),
        make_open_backwall_frame(total_w=1.96, total_h=1.44, center_y=1.02, z_pos=-0.50, win_w=1.54, win_h=0.80, win_cy=1.12),
    ]
    add_part(sm, "CockpitPod_AerospaceMonocoqueTub", merge_geometries(cockpit_tub), mats["aero_white"])

    # 2. GunmetalGullwing Canopy Frame & Twin Machined-Steel Hydraulic Struts
    canopy_frame = [
        make_chamfered_aperture_ring(1.62, 0.86, center_y=1.12, z_pos=-0.45, tube_r=0.042, chamfer=0.20),
        transform_geom(
            make_beveled_box((1.92, 0.05, 0.72), center=(0.0, 0.0, 0.0), bevel=0.015),
            translate=(0.0, 1.66, 0.08),
            rot_xyz_deg=(-26.0, 0.0, 0.0),
        ),
        make_cylinder(0.022, 0.018, 0.68, center=(-0.86, 1.28, -0.18), segments=10, axis="y"),
        make_cylinder(0.022, 0.018, 0.68, center=(0.86, 1.28, -0.18), segments=10, axis="y"),
    ]
    add_part(sm, "CockpitPod_GullwingFrameAndStruts", merge_geometries(canopy_frame), mats["steel_machined"])

    # 3. Rear Cockpit Translucent Viewport + Hinged Gullwing Holo-Visor Canopy Glass (alphaMode: "BLEND")
    add_part(
        sm,
        "CockpitPod_RearTranslucentViewport",
        make_quad_panel((-0.78, 0.72, -0.47), (0.78, 0.72, -0.47), (0.78, 1.52, -0.47), (-0.78, 1.52, -0.47)),
        mats["glass_viewport"],
    )
    gullwing_glass = make_curved_canopy_shield(
        width_x=1.82,
        center_x=0.0,
        radius_yz=0.58,
        center_y=1.22,
        center_z=0.02,
        ang_start_deg=18.0,
        ang_end_deg=92.0,
        segs_arc=10,
    )
    add_part(sm, "CockpitPod_GullwingHoloCanopyGlass", gullwing_glass, mats["glass_holo_visor"])

    # 4. Sculpted Deep Orbital Navy Zero-G Couch + Signal-Orange Bolsters
    add_part(sm, "CockpitPod_OrbitalNavyZeroGCouch", make_contoured_flight_couch(1.86, 0.90, base_y=0.44, res=(7, 3, 5)), mats["pad_navy"])
    add_part(sm, "CockpitPod_SignalOrangeCradle", make_cranial_head_cradle(center=(-0.68, 0.55, 0.0)), mats["accent_orange"])

    # 5. Cyan Canopy HUD Strip + Footwell Telemetry
    add_part(sm, "CockpitPod_CyanCanopyLED", make_beveled_box((1.68, 0.026, 0.06), center=(0.0, 1.54, -0.12), bevel=0.005), mats["led_cyan"])
    add_part(
        sm,
        "CockpitPod_InternalOLEDHUD",
        make_quad_panel((0.36, 0.48, -0.42), (0.76, 0.48, -0.42), (0.76, 0.70, -0.42), (0.36, 0.70, -0.42)),
        mats["oled_hud"],
    )

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bunk_r2_04.glb"), sm, root_name="BunkR2_04_SlidingCanopyCockpitPod")


# ==============================================================================
# 05: DUAL-WINDOW CORNER OBSERVATION BUNK (`bunk_r2_05.glb`)
# ==============================================================================
def build_05_corner_l_viewport_berth(mats):
    sm = []
    # 1. L-Shaped Corner Gunmetal Enclosure (Rear -Z wall + Left -X wall with open cutouts; Right +X is low-profile!)
    corner_hull = [
        make_beveled_box((2.20, 0.36, 1.16), center=(0.0, 0.18, 0.0), bevel=0.035),
        make_beveled_box((2.20, 0.18, 1.16), center=(0.0, 1.82, 0.0), bevel=0.035),
        # Low-profile right foot-end armrest wall so camera at +X/+Z looks into both -Z and -X windows
        make_beveled_box((0.16, 0.62, 1.14), center=(1.02, 0.48, 0.0), bevel=0.03),
        # Rear wall with open cutout (X in [-0.72, +0.72], Y in [0.74, 1.54])
        make_open_backwall_frame(total_w=2.04, total_h=1.48, center_y=1.10, z_pos=-0.50, win_w=1.48, win_h=0.80, win_cy=1.14),
        # Left head-wall (-X = -1.01) with open side viewport cutout (Z in [-0.36, +0.36], Y in [0.74, 1.54])
        make_beveled_box((0.12, 0.38, 1.12), center=(-1.01, 0.55, 0.0), bevel=0.02),
        make_beveled_box((0.12, 0.22, 1.12), center=(-1.01, 1.65, 0.0), bevel=0.02),
        make_beveled_box((0.12, 0.82, 0.20), center=(-1.01, 1.14, -0.46), bevel=0.02),
        make_beveled_box((0.12, 0.82, 0.20), center=(-1.01, 1.14, 0.46), bevel=0.02),
    ]
    add_part(sm, "CornerPod_LShapedGunmetalHull", merge_geometries(corner_hull), mats["gunmetal"])

    # 2. Dual Machined-Steel Viewport Bezels (Rear + Left Side)
    side_bezel = transform_geom(
        make_chamfered_aperture_ring(0.82, 0.84, center_y=1.14, z_pos=0.0, tube_r=0.042, chamfer=0.18),
        translate=(-0.96, 0.0, 0.0),
        rot_xyz_deg=(0.0, 90.0, 0.0),
    )
    rear_bezel = make_chamfered_aperture_ring(1.54, 0.84, center_y=1.14, z_pos=-0.45, tube_r=0.044, chamfer=0.20)
    add_part(sm, "CornerPod_DualMachinedBezels", merge_geometries([rear_bezel, side_bezel]), mats["steel_machined"])

    # 3. Dual Translucent Viewport Glass Panes (Rear -Z + Left -X, alphaMode: "BLEND")
    dual_glass = [
        make_quad_panel((-0.75, 0.74, -0.47), (0.75, 0.74, -0.47), (0.75, 1.54, -0.47), (-0.75, 1.54, -0.47)),
        make_quad_panel((-0.98, 0.74, 0.38), (-0.98, 0.74, -0.38), (-0.98, 1.54, -0.38), (-0.98, 1.54, 0.38)),
    ]
    add_part(sm, "CornerPod_DualTranslucentViewports", merge_geometries(dual_glass), mats["glass_viewport"])

    # 4. Contoured Slate & Charcoal Corner Lounge Couch
    add_part(sm, "CornerPod_CharcoalLoungeCouch", make_contoured_flight_couch(1.84, 0.90, base_y=0.45, res=(7, 3, 5)), mats["pad_charcoal"])
    bolsters = [
        make_cranial_head_cradle(center=(-0.66, 0.56, 0.0)),
        make_draped_blanket(1.06, 0.88, top_y=0.53, drape_drop=0.18, center_xz=(0.24, 0.02), res_x=11, res_z=12),
    ]
    add_part(sm, "CornerPod_SlateBolstersAndThrow", merge_geometries(bolsters), mats["pad_slate"])

    # 5. Cool Cyan Corner Edge Lighting Strips
    cyan_leds = [
        make_beveled_box((1.72, 0.026, 0.06), center=(0.0, 1.70, 0.10), bevel=0.005),
        make_beveled_box((1.44, 0.020, 0.035), center=(0.0, 0.73, -0.43), bevel=0.004),
        make_beveled_box((0.035, 0.020, 0.72), center=(-0.94, 0.73, 0.0), bevel=0.004),
    ]
    add_part(sm, "CornerPod_CyanCornerEdgeLED", merge_geometries(cyan_leds), mats["led_cyan"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bunk_r2_05.glb"), sm, root_name="BunkR2_05_CornerLViewportBerth")


# ==============================================================================
# 06: GIMBALED CENTRIFUGE SLEEP CRADLE (`bunk_r2_06.glb`)
# ==============================================================================
def build_06_suspended_gyro_cradle(mats):
    sm = []
    # 1. Heavy Gunmetal Pedestal Stands & Gimbal Trunnion Mounts
    stands = [
        make_beveled_box((2.20, 0.22, 1.12), center=(0.0, 0.11, 0.0), bevel=0.03),
        make_beveled_box((0.18, 0.96, 0.42), center=(-1.01, 0.58, 0.0), bevel=0.03),
        make_beveled_box((0.18, 0.96, 0.42), center=(1.01, 0.58, 0.0), bevel=0.03),
    ]
    add_part(sm, "GyroCradle_GunmetalPedestalStands", merge_geometries(stands), mats["gunmetal"])

    # 2. Twin Large Precision-Machined Brushed-Steel Gyro Rings (R = 0.84m at X = -0.82m and +0.82m)
    gyro_rings = []
    for gx in [-0.82, 0.82]:
        ring_pts = []
        for k in range(25):
            ang = (k / 24.0) * 2.0 * math.pi
            ring_pts.append([gx, 1.04 + 0.82 * math.sin(ang), 0.82 * math.cos(ang)])
        gyro_rings.append(make_swept_tube(np.array(ring_pts, dtype=np.float32), radius=0.052, radial_segments=12, closed_loop=True, oval_scale=(0.8, 1.4)))
    gyro_rings.append(make_cylinder(0.055, 0.055, 0.24, center=(-0.94, 1.04, 0.0), segments=12, axis="x"))
    gyro_rings.append(make_cylinder(0.055, 0.055, 0.24, center=(0.94, 1.04, 0.0), segments=12, axis="x"))
    add_part(sm, "GyroCradle_MachinedSteelGyroRings", merge_geometries(gyro_rings), mats["steel_machined"])

    # 3. Suspended Cylindrical Aerospace White Lower Cradle Shell (rear & upper arc cut open for viewing!)
    cradle_shell = [
        make_sculpted_cushion((1.72, 0.24, 0.96), center=(0.0, 0.42, 0.0), res=(7, 3, 5), roundness=0.35, belly_puff=0.04, pinch_corners=0.0, crease_freq=0),
        make_beveled_box((1.72, 0.12, 0.36), center=(0.0, 1.78, 0.14), bevel=0.025),
    ]
    add_part(sm, "GyroCradle_SuspendedWhitePodShell", merge_geometries(cradle_shell), mats["aero_white"])

    # 4. Curved Upper & Rear Translucent Viewing Canopy (alphaMode: "BLEND")
    canopy_glass = make_curved_canopy_shield(
        width_x=1.64,
        center_x=0.0,
        radius_yz=0.76,
        center_y=1.02,
        center_z=0.0,
        ang_start_deg=105.0,
        ang_end_deg=205.0,
        segs_arc=14,
    )
    add_part(sm, "GyroCradle_TranslucentViewingCanopy", canopy_glass, mats["glass_viewport"])

    # 5. Orbital Navy Contoured Zero-G Cradle Pad + Signal-Orange Trunnion Locks + Cyan/Amber LEDs
    add_part(sm, "GyroCradle_OrbitalNavyFlightCouch", make_contoured_flight_couch(1.62, 0.84, base_y=0.54, res=(6, 3, 5)), mats["pad_navy"])
    add_part(sm, "GyroCradle_SignalOrangeHeadCradle", make_cranial_head_cradle(center=(-0.58, 0.65, 0.0)), mats["accent_orange"])
    add_part(sm, "GyroCradle_CyanRingLED", make_beveled_box((1.58, 0.026, 0.06), center=(0.0, 1.72, 0.12), bevel=0.005), mats["led_cyan"])
    add_part(sm, "GyroCradle_AmberBaseLED", make_beveled_box((1.68, 0.022, 0.04), center=(0.0, 0.23, 0.52), bevel=0.004), mats["led_amber"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bunk_r2_06.glb"), sm, root_name="BunkR2_06_SuspendedGyroCradle")


# ==============================================================================
# 07: HIGH-TECH MED/CRYO DIAGNOSTIC BERTH (`bunk_r2_07.glb`)
# ==============================================================================
def build_07_medical_biomonitor_pod(mats):
    sm = []
    # 1. Clean-Room Aerospace White Med-Bay Shell with Open Rear Observation Viewport Cutout
    med_shell = [
        make_beveled_box((2.18, 0.36, 1.14), center=(0.0, 0.18, 0.0), bevel=0.035),
        make_beveled_box((2.18, 0.20, 1.14), center=(0.0, 1.80, 0.0), bevel=0.035),
        make_beveled_box((0.15, 1.62, 1.12), center=(-1.02, 0.99, 0.0), bevel=0.04),
        make_beveled_box((0.15, 1.62, 1.12), center=(1.02, 0.99, 0.0), bevel=0.04),
        make_open_backwall_frame(total_w=1.96, total_h=1.48, center_y=1.08, z_pos=-0.50, win_w=1.50, win_h=0.80, win_cy=1.14),
    ]
    add_part(sm, "MedPod_AerospaceWhiteCleanShell", merge_geometries(med_shell), mats["aero_white"])

    # 2. Pivoting Brushed-Steel Diagnostic Scanner Arch & Rear Viewport Bezel
    scanner_pts = sample_filleted_polyline(
        [(-0.38, 0.38, -0.46), (-0.38, 1.48, -0.46), (-0.38, 1.48, 0.50), (-0.38, 0.38, 0.50)],
        fillet_radius=0.18,
        corner_subdivs=6,
    )
    steel_arch = [
        make_swept_tube(scanner_pts, radius=0.038, radial_segments=12, oval_scale=(1.2, 0.9)),
        make_chamfered_aperture_ring(1.56, 0.84, center_y=1.14, z_pos=-0.45, tube_r=0.044, chamfer=0.20),
    ]
    add_part(sm, "MedPod_DiagnosticScannerArchAndBezel", merge_geometries(steel_arch), mats["steel_machined"])

    # 3. Arched Translucent Holographic Vitals Visor + Rear Translucent Window (alphaMode: "BLEND")
    holo_visor = make_curved_canopy_shield(
        width_x=0.64,
        center_x=-0.68,
        radius_yz=0.52,
        center_y=0.92,
        center_z=0.0,
        ang_start_deg=-10.0,
        ang_end_deg=85.0,
        segs_arc=10,
    )
    add_part(sm, "MedPod_TranslucentHoloVitalsVisor", holo_visor, mats["glass_holo_visor"])
    add_part(
        sm,
        "MedPod_RearTranslucentViewport",
        make_quad_panel((-0.76, 0.74, -0.47), (0.76, 0.74, -0.47), (0.76, 1.54, -0.47), (-0.76, 1.54, -0.47)),
        mats["glass_viewport"],
    )

    # 4. Contoured Biometric Slate & Charcoal Sleep Pad + Dual Biomonitor OLED Screens
    add_part(sm, "MedPod_BiometricSlateCouch", make_contoured_flight_couch(1.86, 0.88, base_y=0.45, res=(7, 3, 5)), mats["pad_slate"])
    add_part(sm, "MedPod_CharcoalCranialCradle", make_cranial_head_cradle(center=(-0.68, 0.56, 0.0)), mats["pad_charcoal"])
    add_part(
        sm,
        "MedPod_BiomonitorOLEDDisplay",
        make_quad_panel((-0.93, 0.86, -0.34), (-0.93, 0.86, 0.14), (-0.93, 1.18, 0.14), (-0.93, 1.18, -0.34)),
        mats["oled_hud"],
    )

    # 5. Ice-Cyan & Surgical White Recessed Illumination
    add_part(sm, "MedPod_IceCyanSensorStrip", make_beveled_box((1.68, 0.026, 0.06), center=(0.0, 1.68, 0.12), bevel=0.005), mats["led_cyan"])
    add_part(sm, "MedPod_SurgicalWhiteStrip", make_beveled_box((1.46, 0.020, 0.04), center=(0.0, 0.73, -0.43), bevel=0.004), mats["led_ice"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bunk_r2_07.glb"), sm, root_name="BunkR2_07_MedicalBiomonitorPod")


# ==============================================================================
# 08: TWIN OFFSET HONEYCOMB CREW PODS (`bunk_r2_08.glb`)
# ==============================================================================
def build_08_modular_hex_hive_stack(mats):
    sm = []
    # 1. Twin Offset Hexagonal Outer Tubes with Open Rear Hex Viewport Cutouts in BOTH Lower & Upper Pods!
    hive_hull = [
        # Lower pod deck & ceiling (centered slightly left X=-0.10)
        make_beveled_box((1.96, 0.24, 1.14), center=(-0.10, 0.12, 0.0), bevel=0.03),
        make_beveled_box((2.12, 0.12, 1.12), center=(0.0, 1.06, 0.0), bevel=0.025),
        # Upper pod ceiling (centered slightly right X=+0.10)
        make_beveled_box((1.96, 0.14, 1.12), center=(0.10, 2.02, 0.0), bevel=0.03),
        # Outer side walls
        make_beveled_box((0.14, 2.04, 1.12), center=(-1.04, 1.02, 0.0), bevel=0.035),
        make_beveled_box((0.14, 2.04, 1.12), center=(1.04, 1.02, 0.0), bevel=0.035),
        # Rear wall pillars leaving TWO wide open viewport cutouts: Lower (Y=0.42..0.94) & Upper (Y=1.28..1.84)
        make_beveled_box((0.24, 1.96, 0.10), center=(-0.88, 1.02, -0.50), bevel=0.02),
        make_beveled_box((0.24, 1.96, 0.10), center=(0.88, 1.02, -0.50), bevel=0.02),
        make_beveled_box((1.60, 0.22, 0.10), center=(0.0, 0.31, -0.50), bevel=0.02),
        make_beveled_box((1.60, 0.30, 0.10), center=(0.0, 1.11, -0.50), bevel=0.02),
        make_beveled_box((1.60, 0.18, 0.10), center=(0.0, 1.93, -0.50), bevel=0.02),
    ]
    add_part(sm, "HexHive_GunmetalHoneycombTubes", merge_geometries(hive_hull), mats["gunmetal"])

    # 2. Machined-Steel Hex Entry Bezels, Rear Viewport Bezels & Integrated Step-Rungs
    steel_parts = [
        make_chamfered_aperture_ring(1.86, 0.88, center_y=0.64, z_pos=0.52, tube_r=0.042, chamfer=0.22),
        make_chamfered_aperture_ring(1.86, 0.88, center_y=1.54, z_pos=0.52, tube_r=0.042, chamfer=0.22),
        make_chamfered_aperture_ring(1.48, 0.56, center_y=0.68, z_pos=-0.46, tube_r=0.034, chamfer=0.14),
        make_chamfered_aperture_ring(1.48, 0.56, center_y=1.56, z_pos=-0.46, tube_r=0.034, chamfer=0.14),
    ]
    for ry, rz in [(0.34, 0.58), (0.68, 0.57), (1.02, 0.56), (1.36, 0.55)]:
        steel_parts.append(make_cylinder(0.016, 0.016, 0.36, center=(-0.48, ry, rz), segments=10, axis="x"))
    add_part(sm, "HexHive_MachinedBezelsAndRungs", merge_geometries(steel_parts), mats["steel_machined"])

    # 3. Dual Rear Hex Translucent Viewport Windows (Lower & Upper Pods, alphaMode: "BLEND")
    dual_viewports = [
        make_quad_panel((-0.74, 0.40, -0.47), (0.74, 0.40, -0.47), (0.74, 0.96, -0.47), (-0.74, 0.96, -0.47)),
        make_quad_panel((-0.74, 1.26, -0.47), (0.74, 1.26, -0.47), (0.74, 1.84, -0.47), (-0.74, 1.84, -0.47)),
    ]
    add_part(sm, "HexHive_DualTranslucentRearViewports", merge_geometries(dual_viewports), mats["glass_viewport"])

    # 4. Lower & Upper Contoured Orbital Navy Flight Couches + Signal-Orange Head Cradles
    couches = [
        make_sculpted_cushion((1.72, 0.14, 0.84), center=(0.0, 0.31, 0.0), res=(6, 2, 4), roundness=0.28, belly_puff=0.04, tuft_grid=(3, 2), tuft_depth=0.015, crease_freq=0),
        make_sculpted_cushion((1.72, 0.14, 0.84), center=(0.0, 1.19, 0.0), res=(6, 2, 4), roundness=0.28, belly_puff=0.04, tuft_grid=(3, 2), tuft_depth=0.015, crease_freq=0),
    ]
    add_part(sm, "HexHive_DualCrewFlightCouches", merge_geometries(couches), mats["pad_navy"])
    cradles = [
        make_cranial_head_cradle(center=(-0.64, 0.41, 0.0)),
        make_cranial_head_cradle(center=(-0.64, 1.29, 0.0)),
    ]
    add_part(sm, "HexHive_SignalOrangeCradles", merge_geometries(cradles), mats["accent_orange"])

    # 5. Lower Amber + Upper Cyan Pod Lighting
    add_part(sm, "HexHive_UpperCyanLED", make_beveled_box((1.38, 0.024, 0.05), center=(0.0, 1.90, 0.10), bevel=0.004), mats["led_cyan"])
    add_part(sm, "HexHive_LowerAmberLED", make_beveled_box((1.38, 0.024, 0.05), center=(0.0, 0.98, 0.10), bevel=0.004), mats["led_amber"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bunk_r2_08.glb"), sm, root_name="BunkR2_08_ModularHexHiveStack")


# ==============================================================================
# 09: SPLIT-LEVEL DAYBED & STARGAZER POD (`bunk_r2_09.glb`)
# ==============================================================================
def build_09_observation_lounge_sleeper(mats):
    sm = []
    # 1. Split-Level Carbon-Slate & Gunmetal Daybed Chassis (open rear & slanted upper skylight!)
    chassis = [
        make_beveled_box((2.20, 0.34, 1.18), center=(0.0, 0.17, 0.0), bevel=0.035),
        make_beveled_box((0.15, 1.58, 1.14), center=(-1.02, 0.94, 0.0), bevel=0.04),
        make_beveled_box((0.15, 1.58, 1.14), center=(1.02, 0.94, 0.0), bevel=0.04),
        # Low rear sill at Y=0.34..0.64 so everything above Y=0.64 is an open stargazer skylight
        make_beveled_box((1.96, 0.30, 0.10), center=(0.0, 0.49, -0.51), bevel=0.02),
        make_beveled_box((2.20, 0.14, 0.28), center=(0.0, 1.84, 0.28), bevel=0.025),
    ]
    add_part(sm, "StargazerPod_CarbonSlateChassis", merge_geometries(chassis), mats["carbon_slate"])

    # 2. Slanted Machined-Steel Skylight Mullion Frame
    mullions = [
        make_chamfered_aperture_ring(1.94, 1.28, center_y=1.14, z_pos=0.46, tube_r=0.045, chamfer=0.24),
    ]
    for mx in [-0.90, 0.0, 0.90]:
        m_pts = sample_filleted_polyline([(mx, 0.62, -0.50), (mx, 1.32, -0.46), (mx, 1.84, 0.24)], fillet_radius=0.16, corner_subdivs=6)
        mullions.append(make_swept_tube(m_pts, radius=0.032, radial_segments=10, oval_scale=(0.85, 1.35)))
    add_part(sm, "StargazerPod_SkylightSteelMullions", merge_geometries(mullions), mats["steel_machined"])

    # 3. Massive 2-Stage Slanted Overhead & Rear Translucent Skylight Glass (alphaMode: "BLEND")
    skylight_glass = [
        make_quad_panel((-0.88, 0.64, -0.47), (0.88, 0.64, -0.47), (0.88, 1.32, -0.45), (-0.88, 1.32, -0.45)),
        make_quad_panel((-0.88, 1.32, -0.45), (0.88, 1.32, -0.45), (0.88, 1.82, 0.22), (-0.88, 1.82, 0.22)),
    ]
    add_part(sm, "StargazerPod_TranslucentSkylightGlass", merge_geometries(skylight_glass), mats["glass_viewport"])

    # 4. Split-Level Reclined Stargazer Lounger Backrest (-X) + Horizontal Sleep Deck (+X)
    recliner_parts = [
        transform_geom(
            make_sculpted_cushion((0.68, 0.16, 0.88), res=(6, 3, 5), roundness=0.30, belly_puff=0.05, tuft_grid=(3, 2), tuft_depth=0.015, crease_freq=0),
            translate=(-0.62, 0.64, 0.0),
            rot_xyz_deg=(0.0, 0.0, -32.0),
        ),
        make_contoured_flight_couch(1.42, 0.88, base_y=0.44, res=(6, 3, 5)),
    ]
    add_part(sm, "StargazerPod_SplitLevelLoungerPad", merge_geometries(recliner_parts), mats["pad_slate"])
    add_part(sm, "StargazerPod_ReclinedNeckBolster", make_cranial_head_cradle(center=(-0.74, 0.82, 0.0), tilt_deg=-32.0), mats["pad_navy"])

    # 5. Side Armrest OLED + Warm Amber Skylight Status LED & Cyan Under-Lounger LED
    add_part(
        sm,
        "StargazerPod_ArmrestOLED",
        make_quad_panel((-0.93, 0.82, -0.28), (-0.93, 0.82, 0.18), (-0.93, 1.12, 0.18), (-0.93, 1.12, -0.28)),
        mats["oled_hud"],
    )
    add_part(sm, "StargazerPod_AmberSkylightLED", make_beveled_box((1.72, 0.026, 0.06), center=(0.0, 1.76, 0.20), bevel=0.005), mats["led_amber"])
    add_part(sm, "StargazerPod_CyanDeckLED", make_beveled_box((1.76, 0.022, 0.04), center=(0.0, 0.24, 0.56), bevel=0.004), mats["led_cyan"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bunk_r2_09.glb"), sm, root_name="BunkR2_09_ObservationLoungeSleeper")


# ==============================================================================
# 10: COMMAND DECK OBSERVATION BERTH (`bunk_r2_10.glb`)
# ==============================================================================
def build_10_captain_bridge_alcove(mats):
    sm = []
    # 1. Monumental Chamfered Dark-Gunmetal Bridge Stateroom Hull with Wide Open Rear Cutout
    bridge_hull = [
        make_beveled_box((2.28, 0.36, 1.20), center=(0.0, 0.18, 0.0), bevel=0.04),
        make_beveled_box((2.28, 0.22, 1.20), center=(0.0, 1.88, 0.0), bevel=0.04),
        make_beveled_box((0.20, 1.72, 1.16), center=(-1.04, 1.02, 0.0), bevel=0.04),
        make_beveled_box((0.20, 1.72, 1.16), center=(1.04, 1.02, 0.0), bevel=0.04),
        make_open_backwall_frame(total_w=2.04, total_h=1.56, center_y=1.12, z_pos=-0.52, win_w=1.68, win_h=0.88, win_cy=1.18),
    ]
    add_part(sm, "BridgeAlcove_GunmetalStateroomHull", merge_geometries(bridge_hull), mats["gunmetal"])

    # 2. 3-Panel Trapezoidal Brushed-Steel Bridge Window Mullions & Sweeping Arch Crown
    arch_pts = []
    for k in range(25):
        t = k / 24.0
        ang = math.pi * (1.0 - t)
        arch_pts.append([0.98 * math.cos(ang), 1.18 + 0.68 * math.sin(ang), 0.50])

    mullion_l = sample_filleted_polyline([(-0.42, 0.72, -0.48), (-0.32, 1.64, -0.44)], 0.04, 4)
    mullion_r = sample_filleted_polyline([(0.42, 0.72, -0.48), (0.32, 1.64, -0.44)], 0.04, 4)
    bridge_steel = [
        make_swept_tube(np.array(arch_pts, dtype=np.float32), radius=0.048, radial_segments=14, oval_scale=(1.2, 1.5)),
        make_chamfered_aperture_ring(1.74, 0.92, center_y=1.18, z_pos=-0.46, tube_r=0.045, chamfer=0.22),
        make_swept_tube(mullion_l, radius=0.028, radial_segments=10, oval_scale=(0.8, 1.5)),
        make_swept_tube(mullion_r, radius=0.028, radial_segments=10, oval_scale=(0.8, 1.5)),
        make_beveled_box((0.26, 0.06, 0.52), center=(-0.84, 0.72, -0.18), bevel=0.015),
        make_beveled_box((0.26, 0.06, 0.52), center=(0.84, 0.72, -0.18), bevel=0.015),
    ]
    add_part(sm, "BridgeAlcove_TrapezoidalBridgeMullions", merge_geometries(bridge_steel), mats["steel_machined"])

    # 3. 3-Panel Trapezoidal Bridge Viewport Translucent Glass (alphaMode: "BLEND")
    add_part(
        sm,
        "BridgeAlcove_ThreePanelBridgeGlass",
        make_quad_panel((-0.84, 0.74, -0.48), (0.84, 0.74, -0.48), (0.84, 1.62, -0.48), (-0.84, 1.62, -0.48)),
        mats["glass_viewport"],
    )

    # 4. Layered Command Stateroom Flight Couch + Dual Cranial Cradles + Draped Navy Coverlet
    add_part(sm, "BridgeAlcove_CommandCharcoalCouch", make_contoured_flight_couch(1.86, 0.94, base_y=0.46, res=(7, 3, 5)), mats["pad_charcoal"])
    cradles = [
        make_cranial_head_cradle(center=(-0.64, 0.58, -0.18)),
        make_cranial_head_cradle(center=(-0.64, 0.58, 0.18)),
    ]
    add_part(sm, "BridgeAlcove_DualSlateCradles", merge_geometries(cradles), mats["pad_slate"])
    add_part(
        sm,
        "BridgeAlcove_TailoredNavyCoverlet",
        make_draped_blanket(1.08, 0.92, top_y=0.54, drape_drop=0.20, center_xz=(0.24, 0.02), res_x=11, res_z=13),
        mats["pad_navy"],
    )

    # 5. Twin Cantilevered Wing OLED Displays + Dual Command Cyan & Pedestal Amber Cove Strips
    oled_wings = [
        make_quad_panel((-0.92, 0.84, -0.36), (-0.92, 0.84, 0.08), (-0.92, 1.18, 0.08), (-0.92, 1.18, -0.36)),
        make_quad_panel((0.92, 0.84, 0.08), (0.92, 0.84, -0.36), (0.92, 1.18, -0.36), (0.92, 1.18, 0.08)),
    ]
    add_part(sm, "BridgeAlcove_TwinWingOLEDConsoles", merge_geometries(oled_wings), mats["oled_hud"])
    add_part(sm, "BridgeAlcove_CrownCyanCove", make_beveled_box((1.72, 0.028, 0.07), center=(0.0, 1.72, 0.12), bevel=0.005), mats["led_cyan"])
    add_part(sm, "BridgeAlcove_PedestalAmberCove", make_beveled_box((1.88, 0.024, 0.05), center=(0.0, 0.32, 0.58), bevel=0.004), mats["led_amber"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bunk_r2_10.glb"), sm, root_name="BunkR2_10_CaptainBridgeAlcove")


def build_all_round2():
    mats = get_r2_materials()
    builders = [
        build_01_panoramic_hull_blister_pod,
        build_02_hex_aperture_sleep_chamber,
        build_03_corvette_submarine_rack,
        build_04_sliding_canopy_cockpit_pod,
        build_05_corner_l_viewport_berth,
        build_06_suspended_gyro_cradle,
        build_07_medical_biomonitor_pod,
        build_08_modular_hex_hive_stack,
        build_09_observation_lounge_sleeper,
        build_10_captain_bridge_alcove,
    ]
    results = []
    for fn in builders:
        info = fn(mats)
        fname = os.path.basename(info["filepath"])
        dims = info["dimensions"]
        print(
            f"[bunk_r2] Built {fname:16s} | {dims[0]:.2f}m x {dims[2]:.2f}m x {dims[1]:.2f}m | "
            f"verts={info['vertices']:4d} | tris={info['triangles']:4d} | min_y={info['min'][1]:.5f}"
        )
        results.append(info)
    with open(os.path.join(OUT_GLB_DIR, "bunk_r2_manifest.json"), "w") as f:
        json.dump(results, f, indent=2)
    return results


if __name__ == "__main__":
    build_all_round2()
