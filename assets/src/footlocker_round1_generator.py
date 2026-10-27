#!/usr/bin/env python3
"""
Builds all 5 Round-1 Hard Sci-Fi Modular Cargo & Footlocker Chest .glb models:
/workspace/game-project/assets/glb/footlocker_round1/footlocker_r1_01.glb .. footlocker_r1_05.glb

Follows /workspace/game-project/design/footlocker_round1/footlocker_r1_spec.md ("Aegis-7 Standard"):
- Bottom-center (0.0, 0.0, 0.0) floor pivot (min_y == 0.0000, centered X and Z), front facing +Z
- Polygon budget: 2,500 - 5,000 triangles per candidate
- Mapped cleanly to Sloane's 9 textures in /workspace/game-project/assets/textures/footlocker_round1/
- Mandatory 4-Part 3D Cargo & Footlocker Kit inside every candidate:
  1. 45° Chamfered Octagonal Armor Shell & Interlocking Magnetic Skid Base + Recessed Side Carry Handles
     + Signal-Orange Heavy Cam-Lock Latches & Rotary Pressure-Equalization Valve
  2. Translucent Inspection Window (glass_cargo_lid_translucent.png, alphaMode: "BLEND", alpha ~ 0.18)
     + Partially Open Lid (~35°-42°) on Twin Machined-Steel Telescoping Pneumatic Struts
  3. 3D Stowed Personal Crew Gear Inside the Foam-Lined Bay:
     - Rolled Orbital-Navy Flight Garment / Kit Bundle secured with signal-orange retention straps
     - Two Cylindrical Li-S Power / Emergency Ration Canisters with signal-orange end caps
     - Chamfered Hard-Shell Field Med / Multi-Tool Case with cyan status indicator
  4. Digital OLED Manifest Strip (oled_cargo_manifest.png) & Internal Cyan / Skid Amber LED Indicators
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
)

TEX_FOOTLOCKER_DIR = "/workspace/game-project/assets/textures/footlocker_round1"
OUT_GLB_DIR = "/workspace/game-project/assets/glb/footlocker_round1"
os.makedirs(OUT_GLB_DIR, exist_ok=True)


def tex_fl(fname: str) -> str:
    return os.path.join(TEX_FOOTLOCKER_DIR, fname)


def get_footlocker_materials():
    return {
        "gunmetal": PBRMaterialDef(
            name="Mat_Titanium_GunmetalHull",
            base_color=hex_rgba("#1A1E24"),
            metallic=0.78,
            roughness=0.34,
            texture_path=tex_fl("titanium_gunmetal_hull.png"),
        ),
        "aero_white": PBRMaterialDef(
            name="Mat_Composite_AerospaceWhite",
            base_color=hex_rgba("#D8DEE6"),
            metallic=0.08,
            roughness=0.28,
            texture_path=tex_fl("composite_aerospace_white.png"),
        ),
        "carbon_slate": PBRMaterialDef(
            name="Mat_Carbon_SlateFrame",
            base_color=hex_rgba("#282E38"),
            metallic=0.58,
            roughness=0.40,
            texture_path=tex_fl("carbon_slate_frame.png"),
        ),
        "steel_machined": PBRMaterialDef(
            name="Mat_Steel_MachinedGantry",
            base_color=hex_rgba("#88929E"),
            metallic=0.90,
            roughness=0.22,
            texture_path=tex_fl("steel_machined_gantry.png"),
        ),
        "pad_charcoal": PBRMaterialDef(
            name="Mat_Fabric_CharcoalFlightpad",
            base_color=hex_rgba("#242932"),
            metallic=0.02,
            roughness=0.78,
            texture_path=tex_fl("fabric_charcoal_flightpad.png"),
        ),
        "pad_navy": PBRMaterialDef(
            name="Mat_Fabric_OrbitalNavyPad",
            base_color=hex_rgba("#1D2C3C"),
            metallic=0.02,
            roughness=0.76,
            texture_path=tex_fl("fabric_orbital_navy_pad.png"),
        ),
        "accent_orange": PBRMaterialDef(
            name="Mat_Accent_SignalOrange",
            base_color=hex_rgba("#D95B26"),
            metallic=0.06,
            roughness=0.48,
            texture_path=tex_fl("accent_signal_orange.png"),
        ),
        "oled_manifest": PBRMaterialDef(
            name="Mat_OLED_CargoManifest",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.10,
            roughness=0.14,
            emissive=(0.35, 0.90, 1.0),
            texture_path=tex_fl("oled_cargo_manifest.png"),
        ),
        "glass_lid": PBRMaterialDef(
            name="Mat_Glass_CargoLid_Translucent",
            base_color=(0.55, 0.88, 1.0, 0.18),
            metallic=0.10,
            roughness=0.08,
            emissive=(0.0, 0.14, 0.22),
            texture_path=tex_fl("glass_cargo_lid_translucent.png"),
            double_sided=True,
            alpha_mode="BLEND",
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
    }


# ==============================================================================
# SHARED 3D STOWED CARGO KIT & HARDWARE GENERATORS
# ==============================================================================
def make_stowed_cargo_kit(
    bay_cx: float = 0.0,
    bay_y: float = 0.24,
    bay_cz: float = 0.0,
    bay_w: float = 0.58,
    bay_d: float = 0.42,
):
    """
    Builds Part 3 of the Mandatory 4-Part Footlocker Kit inside the open foam-lined bay:
    - Contoured charcoal EVA foam organizer bed
    - Rolled Orbital-Navy Flight Garment / Kit Bundle with signal-orange retention straps
    - Two Cylindrical Li-S Power / Emergency Ration Canisters with signal-orange end caps
    - Chamfered Hard-Shell Field Med / Multi-Tool Case with cyan status indicator
    Returns: (charcoal_foam_geom, navy_garment_geom, white_canisters_and_case_geom,
              steel_rings_geom, orange_straps_and_caps_geom, cyan_case_led_geom)
    """
    foam_bed = [
        make_sculpted_cushion(
            (bay_w, 0.08, bay_d),
            center=(bay_cx, bay_y, bay_cz),
            res=(6, 2, 5),
            roundness=0.25,
            belly_puff=0.02,
            tuft_grid=(3, 2),
            tuft_depth=0.015,
            crease_freq=0,
        ),
    ]

    # 1. Rolled Orbital-Navy Flight Garment Bundle on left/back of bay
    gx = bay_cx - bay_w * 0.24
    gz = bay_cz - 0.02
    gy = bay_y + 0.085
    navy_roll = [
        make_sculpted_cushion(
            (bay_w * 0.38, 0.11, bay_d * 0.72),
            center=(gx, gy, gz),
            res=(6, 4, 5),
            roundness=0.45,
            belly_puff=0.06,
            pinch_corners=0.12,
            crease_freq=4,
        ),
    ]
    orange_parts = [
        make_beveled_box((bay_w * 0.40, 0.118, 0.028), center=(gx, gy, gz - 0.06), bevel=0.005),
        make_beveled_box((bay_w * 0.40, 0.118, 0.028), center=(gx, gy, gz + 0.06), bevel=0.005),
    ]

    # 2. Two Cylindrical Li-S Power / Ration Canisters in center of bay
    cx1 = bay_cx + bay_w * 0.06
    cx2 = bay_cx + bay_w * 0.22
    cy = bay_y + 0.075
    white_parts = [
        make_cylinder(0.036, 0.036, bay_d * 0.68, center=(cx1, cy, bay_cz), segments=14, axis="z"),
        make_cylinder(0.036, 0.036, bay_d * 0.68, center=(cx2, cy, bay_cz), segments=14, axis="z"),
    ]
    steel_parts = [
        make_cylinder(0.038, 0.038, 0.03, center=(cx1, cy, bay_cz), segments=14, axis="z"),
        make_cylinder(0.038, 0.038, 0.03, center=(cx2, cy, bay_cz), segments=14, axis="z"),
    ]
    for cx_i in [cx1, cx2]:
        orange_parts.append(make_cylinder(0.038, 0.038, 0.032, center=(cx_i, cy, bay_cz + bay_d * 0.34), segments=14, axis="z"))
        orange_parts.append(make_cylinder(0.038, 0.038, 0.032, center=(cx_i, cy, bay_cz - bay_d * 0.34), segments=14, axis="z"))

    # 3. Chamfered Hard-Shell Field Med / Multi-Tool Case on right/front of bay
    mx = bay_cx + bay_w * 0.36
    my = bay_y + 0.075
    white_parts.append(make_beveled_box((bay_w * 0.20, 0.08, bay_d * 0.66), center=(mx, my, bay_cz), bevel=0.015))
    cyan_parts = [
        make_beveled_box((bay_w * 0.14, 0.012, 0.04), center=(mx, my + 0.042, bay_cz + 0.04), bevel=0.003),
        # Internal bay perimeter cyan light bar along rear inner rim
        make_beveled_box((bay_w * 0.92, 0.018, 0.025), center=(bay_cx, bay_y + 0.15, bay_cz - bay_d * 0.46), bevel=0.004),
    ]

    return (
        merge_geometries(foam_bed),
        merge_geometries(navy_roll),
        merge_geometries(white_parts),
        merge_geometries(steel_parts),
        merge_geometries(orange_parts),
        merge_geometries(cyan_parts),
    )


def make_side_handles_and_valve(half_w: float = 0.525, mid_y: float = 0.28):
    """
    Builds recessed machined-steel side carry handles at ±X and a signal-orange
    4-spoke rotary pressure-equalization valve on the left (-X) end cap.
    Returns: (steel_handles_geom, orange_valve_geom)
    """
    h_left = sample_filleted_polyline(
        [(-half_w, mid_y + 0.04, -0.09), (-half_w - 0.028, mid_y - 0.02, -0.09), (-half_w - 0.028, mid_y - 0.02, 0.09), (-half_w, mid_y + 0.04, 0.09)],
        fillet_radius=0.02,
        corner_subdivs=4,
    )
    h_right = sample_filleted_polyline(
        [(half_w, mid_y + 0.04, -0.09), (half_w + 0.028, mid_y - 0.02, -0.09), (half_w + 0.028, mid_y - 0.02, 0.09), (half_w, mid_y + 0.04, 0.09)],
        fillet_radius=0.02,
        corner_subdivs=4,
    )
    steel_handles = [
        make_swept_tube(h_left, radius=0.011, radial_segments=10),
        make_swept_tube(h_right, radius=0.011, radial_segments=10),
    ]

    # Signal-orange rotary pressure-equalization valve on left (-X) or front corner
    vx, vy, vz = -half_w - 0.012, mid_y + 0.08, 0.14
    orange_valve = [
        make_cylinder(0.042, 0.042, 0.022, center=(vx, vy, vz), segments=14, axis="x"),
        make_beveled_box((0.026, 0.095, 0.018), center=(vx - 0.005, vy, vz), bevel=0.004),
        make_beveled_box((0.026, 0.018, 0.095), center=(vx - 0.005, vy, vz), bevel=0.004),
    ]
    return merge_geometries(steel_handles), merge_geometries(orange_valve)


def make_open_hinged_lid_with_window(
    lid_w: float,
    lid_d: float,
    hinge_pos: tuple,
    open_angle_deg: float = 38.0,
):
    """
    Builds a hinged chamfered aerospace-white & machined-steel lid with a true open cutout
    and an alphaMode: "BLEND" translucent polycarbonate viewport (glass_cargo_lid_translucent.png),
    tilted open by open_angle_deg around the rear hinge line, plus twin pneumatic struts.
    Returns: (white_lid_frame_geom, steel_bezel_and_struts_geom, translucent_glass_geom)
    """
    hx, hy, hz = hinge_pos
    border_x = max(0.06, lid_w * 0.13)
    border_z = max(0.06, lid_d * 0.15)
    win_w = lid_w - 2.0 * border_x
    win_d = lid_d - 2.0 * border_z

    # Local coordinates relative to rear hinge (y=0, z=0, extending forward to z=+lid_d)
    local_frame = [
        # Rear rail (z: 0 to border_z)
        make_beveled_box((lid_w, 0.042, border_z), center=(0.0, 0.021, border_z * 0.5), bevel=0.012),
        # Front rail (z: lid_d - border_z to lid_d)
        make_beveled_box((lid_w, 0.042, border_z), center=(0.0, 0.021, lid_d - border_z * 0.5), bevel=0.012),
        # Left rail
        make_beveled_box((border_x, 0.042, win_d + 0.02), center=(-lid_w * 0.5 + border_x * 0.5, 0.021, lid_d * 0.5), bevel=0.012),
        # Right rail
        make_beveled_box((border_x, 0.042, win_d + 0.02), center=(lid_w * 0.5 - border_x * 0.5, 0.021, lid_d * 0.5), bevel=0.012),
    ]
    local_glass = make_quad_panel(
        (-win_w * 0.5, 0.024, lid_d - border_z),
        (win_w * 0.5, 0.024, lid_d - border_z),
        (win_w * 0.5, 0.024, border_z),
        (-win_w * 0.5, 0.024, border_z),
    )
    local_bezel = transform_geom(
        make_chamfered_aperture_ring(win_w + 0.03, win_d + 0.03, center_y=0.0, z_pos=0.0, tube_r=0.014, chamfer=0.06),
        translate=(0.0, 0.028, lid_d * 0.5),
        rot_xyz_deg=(-90.0, 0.0, 0.0),
    )

    # Rotate around X by -open_angle_deg so +Z lifts up into +Y
    frame_world = transform_geom(merge_geometries(local_frame), translate=hinge_pos, rot_xyz_deg=(-open_angle_deg, 0.0, 0.0))
    glass_world = transform_geom(local_glass, translate=hinge_pos, rot_xyz_deg=(-open_angle_deg, 0.0, 0.0))
    bezel_world = transform_geom(local_bezel, translate=hinge_pos, rot_xyz_deg=(-open_angle_deg, 0.0, 0.0))

    # Twin telescoping pneumatic struts connecting chest inner wall to lifted lid
    rad = math.radians(open_angle_deg)
    attach_z = hz + (lid_d * 0.65) * math.cos(rad)
    attach_y = hy + (lid_d * 0.65) * math.sin(rad)
    sx_off = lid_w * 0.44
    strut_l = sample_filleted_polyline([(hx - sx_off, hy - 0.14, hz + lid_d * 0.35), (hx - sx_off, attach_y, attach_z)], 0.01, 2)
    strut_r = sample_filleted_polyline([(hx + sx_off, hy - 0.14, hz + lid_d * 0.35), (hx + sx_off, attach_y, attach_z)], 0.01, 2)
    struts = [
        bezel_world,
        make_swept_tube(strut_l, radius=0.012, radial_segments=8),
        make_swept_tube(strut_r, radius=0.012, radial_segments=8),
        make_cylinder(0.018, 0.018, 0.08, center=(hx - lid_w * 0.32, hy, hz), segments=10, axis="x"),
        make_cylinder(0.018, 0.018, 0.08, center=(hx + lid_w * 0.32, hy, hz), segments=10, axis="x"),
    ]

    return frame_world, merge_geometries(struts), glass_world


# ==============================================================================
# CANDIDATE 01: AEGIS-7 OCTAGONAL BULKHEAD FOOTLOCKER & BENCH CHEST (`footlocker_r1_01.glb`)
# Dimensions: 1.05m W x 0.54m D x 0.55m H (body) / ~0.84m H (open right lid)
# ==============================================================================
def build_01_octagonal_bench_footlocker(mats):
    sm = []
    # 1. Carbon-Slate Interlocking Magnetic Floor-Lock Skids
    skids = [
        make_beveled_box((1.05, 0.07, 0.54), center=(0.0, 0.035, 0.0), bevel=0.02),
        make_beveled_box((0.18, 0.09, 0.56), center=(-0.40, 0.045, 0.0), bevel=0.02),
        make_beveled_box((0.18, 0.09, 0.56), center=(0.40, 0.045, 0.0), bevel=0.02),
    ]
    add_part(sm, "Footlocker01_CarbonSlateMagneticSkids", merge_geometries(skids), mats["carbon_slate"])

    # 2. 45° Chamfered Octagonal Gunmetal Trunk Hull (Left closed bench support + Right open cargo well)
    hull = [
        # Lower floor & left bench enclosure
        make_beveled_box((1.03, 0.14, 0.52), center=(0.0, 0.14, 0.0), bevel=0.025),
        make_beveled_box((0.50, 0.36, 0.52), center=(-0.265, 0.32, 0.0), bevel=0.025),
        # Right cargo well walls (front, rear, right, center partition) leaving top open
        make_beveled_box((0.52, 0.36, 0.05), center=(0.25, 0.32, 0.235), bevel=0.015),
        make_beveled_box((0.52, 0.36, 0.05), center=(0.25, 0.32, -0.235), bevel=0.015),
        make_beveled_box((0.06, 0.36, 0.52), center=(0.485, 0.32, 0.0), bevel=0.015),
    ]
    add_part(sm, "Footlocker01_OctagonalGunmetalHull", merge_geometries(hull), mats["gunmetal"])

    # 3. Left Half Fixed Contoured Charcoal Bench Cushion + Right Half Stowed Foam & Gear Kit
    foam_bed, navy_roll, white_kit, steel_kit, orange_kit, cyan_kit = make_stowed_cargo_kit(
        bay_cx=0.23, bay_y=0.22, bay_cz=0.0, bay_w=0.44, bay_d=0.40
    )
    bench_cushion = make_sculpted_cushion(
        (0.48, 0.075, 0.48),
        center=(-0.265, 0.525, 0.0),
        res=(7, 3, 6),
        roundness=0.34,
        belly_puff=0.04,
        tuft_grid=(3, 2),
        tuft_depth=0.014,
        crease_freq=0,
    )
    add_part(sm, "Footlocker01_CharcoalBenchAndFoam", merge_geometries([bench_cushion, foam_bed]), mats["pad_charcoal"])
    add_part(sm, "Footlocker01_StowedOrbitalNavyBundle", navy_roll, mats["pad_navy"])

    # 4. Right Half Hinged Lid Propped Open at 38° with Translucent Inspection Window
    lid_white, lid_steel, lid_glass = make_open_hinged_lid_with_window(
        lid_w=0.50, lid_d=0.50, hinge_pos=(0.25, 0.50, -0.24), open_angle_deg=38.0
    )
    add_part(sm, "Footlocker01_WhiteLidAndStowedCanisters", merge_geometries([lid_white, white_kit]), mats["aero_white"])

    # 5. Machined-Steel Struts, Side Handles & Signal-Orange Cam Latches / Rotary Valve
    handles_steel, valve_orange = make_side_handles_and_valve(half_w=0.515, mid_y=0.30)
    add_part(sm, "Footlocker01_MachinedStrutsAndHandles", merge_geometries([lid_steel, steel_kit, handles_steel]), mats["steel_machined"])

    latches = [
        orange_kit,
        valve_orange,
        make_beveled_box((0.055, 0.11, 0.03), center=(-0.32, 0.34, 0.265), bevel=0.006),
        make_beveled_box((0.055, 0.11, 0.03), center=(0.32, 0.34, 0.265), bevel=0.006),
    ]
    add_part(sm, "Footlocker01_SignalOrangeLatchesAndValve", merge_geometries(latches), mats["accent_orange"])

    # 6. Front Bevel Digital OLED Manifest Strip + Internal Cyan & Skid Amber LEDs
    add_part(
        sm,
        "Footlocker01_FrontOLEDManifest",
        make_quad_panel((-0.22, 0.26, 0.264), (0.22, 0.26, 0.264), (0.22, 0.42, 0.264), (-0.22, 0.42, 0.264)),
        mats["oled_manifest"],
    )
    add_part(sm, "Footlocker01_InternalCyanLED", cyan_kit, mats["led_cyan"])
    amber_skids = [
        make_beveled_box((0.14, 0.018, 0.03), center=(-0.40, 0.05, 0.275), bevel=0.004),
        make_beveled_box((0.14, 0.018, 0.03), center=(0.40, 0.05, 0.275), bevel=0.004),
    ]
    add_part(sm, "Footlocker01_SkidAmberBeacons", merge_geometries(amber_skids), mats["led_amber"])

    # 7. Translucent Polycarbonate Lid Inspection Viewport (alphaMode: "BLEND")
    add_part(sm, "Footlocker01_TranslucentLidViewport", lid_glass, mats["glass_lid"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "footlocker_r1_01.glb"), sm, root_name="FootlockerR1_01_OctagonalBenchChest")


# ==============================================================================
# CANDIDATE 02: DUAL-BAY SPLIT CARGO TRUNK & PULL-OUT DRAWER MODULE (`footlocker_r1_02.glb`)
# Dimensions: 1.10m W x 0.56m D x 0.58m H (body) / ~0.85m H (open lid)
# ==============================================================================
def build_02_dual_bay_split_drawer_trunk(mats):
    sm = []
    # 1. Asymmetric 65% / 35% Split-Bay Skid Base & Partition (Left Bay: X=-0.55..+0.16, Right Bay: X=+0.16..+0.55)
    skids = [
        make_beveled_box((1.10, 0.07, 0.54), center=(0.0, 0.035, -0.02), bevel=0.02),
        make_beveled_box((0.05, 0.46, 0.52), center=(0.16, 0.28, -0.02), bevel=0.015),
    ]
    add_part(sm, "Footlocker02_CarbonSlateSplitSkids", merge_geometries(skids), mats["carbon_slate"])

    # 2. Gunmetal Titanium Split Trunk Chassis (Left Open Equipment Well + Right 2-Drawer Housing)
    hull = [
        make_beveled_box((1.08, 0.12, 0.52), center=(0.0, 0.12, -0.02), bevel=0.025),
        # Left Bay walls (X = -0.54 to +0.16)
        make_beveled_box((0.70, 0.38, 0.05), center=(-0.19, 0.33, 0.215), bevel=0.015),
        make_beveled_box((0.70, 0.38, 0.05), center=(-0.19, 0.33, -0.255), bevel=0.015),
        make_beveled_box((0.06, 0.38, 0.52), center=(-0.51, 0.33, -0.02), bevel=0.015),
        # Right Bay outer wall & top deck supporting bench cushion
        make_beveled_box((0.06, 0.40, 0.52), center=(0.51, 0.34, -0.02), bevel=0.015),
        make_beveled_box((0.38, 0.40, 0.05), center=(0.35, 0.34, -0.255), bevel=0.015),
        make_beveled_box((0.38, 0.05, 0.52), center=(0.35, 0.515, -0.02), bevel=0.015),
    ]
    add_part(sm, "Footlocker02_SplitBayGunmetalChassis", merge_geometries(hull), mats["gunmetal"])

    # 3. Left Bay 3D Stowed Gear Kit + Right Bay Fixed Bench Cushion & Pulled-Out Lower Drawer
    foam_bed, navy_roll, white_kit, steel_kit, orange_kit, cyan_kit = make_stowed_cargo_kit(
        bay_cx=-0.18, bay_y=0.21, bay_cz=-0.02, bay_w=0.60, bay_d=0.40
    )
    right_bench = make_sculpted_cushion(
        (0.36, 0.065, 0.48),
        center=(0.35, 0.56, -0.02),
        res=(6, 3, 5),
        roundness=0.34,
        belly_puff=0.04,
        tuft_grid=(2, 2),
        tuft_depth=0.012,
        crease_freq=0,
    )
    drawer_foam = make_beveled_box((0.28, 0.04, 0.24), center=(0.35, 0.20, 0.14), bevel=0.008)
    add_part(sm, "Footlocker02_BenchCushionAndFoamBeds", merge_geometries([right_bench, foam_bed, drawer_foam]), mats["pad_charcoal"])
    add_part(sm, "Footlocker02_StowedNavyEVABundle", navy_roll, mats["pad_navy"])

    # 4. Left Bay Open Lid (35°) + Right Bay Upper Closed Drawer & Lower Pulled-Out Drawer (+0.16m forward)
    lid_white, lid_steel, lid_glass = make_open_hinged_lid_with_window(
        lid_w=0.68, lid_d=0.50, hinge_pos=(-0.18, 0.52, -0.26), open_angle_deg=35.0
    )
    drawers_white = [
        lid_white,
        white_kit,
        # Upper right drawer front (closed at Z = +0.23)
        make_beveled_box((0.32, 0.15, 0.04), center=(0.35, 0.41, 0.22), bevel=0.01),
        # Lower right drawer box pulled forward +0.16m (extending to Z = +0.38)
        make_beveled_box((0.32, 0.14, 0.04), center=(0.35, 0.23, 0.36), bevel=0.01),
        make_beveled_box((0.30, 0.09, 0.28), center=(0.35, 0.21, 0.20), bevel=0.008),
        # Stowed ration bars & tool cartridges inside pulled-out lower drawer
        make_beveled_box((0.08, 0.05, 0.14), center=(0.29, 0.24, 0.18), bevel=0.006),
        make_beveled_box((0.08, 0.05, 0.14), center=(0.40, 0.24, 0.18), bevel=0.006),
    ]
    add_part(sm, "Footlocker02_WhiteLidAndSlideOutDrawers", merge_geometries(drawers_white), mats["aero_white"])

    # 5. Machined-Steel Struts, Telescoping Drawer Rails, Side Handles & Orange Cam Latches
    handles_steel, valve_orange = make_side_handles_and_valve(half_w=0.54, mid_y=0.30)
    drawer_rails = [
        lid_steel,
        steel_kit,
        handles_steel,
        make_beveled_box((0.02, 0.025, 0.34), center=(0.19, 0.22, 0.16), bevel=0.004),
        make_beveled_box((0.02, 0.025, 0.34), center=(0.49, 0.22, 0.16), bevel=0.004),
        make_cylinder(0.010, 0.010, 0.16, center=(0.35, 0.23, 0.39), segments=10, axis="x"),
    ]
    add_part(sm, "Footlocker02_MachinedStrutsAndDrawerRails", merge_geometries(drawer_rails), mats["steel_machined"])

    orange_all = [
        orange_kit,
        valve_orange,
        make_beveled_box((0.055, 0.10, 0.03), center=(-0.38, 0.36, 0.245), bevel=0.006),
        make_beveled_box((0.055, 0.10, 0.03), center=(0.02, 0.36, 0.245), bevel=0.006),
        make_beveled_box((0.045, 0.08, 0.025), center=(0.48, 0.41, 0.245), bevel=0.005),
    ]
    add_part(sm, "Footlocker02_SignalOrangeLatchesAndCaps", merge_geometries(orange_all), mats["accent_orange"])

    # 6. Upper Right Drawer OLED Manifest Screen + Left Bay Cyan & Right Drawer Amber LEDs
    add_part(
        sm,
        "Footlocker02_UpperDrawerOLEDManifest",
        make_quad_panel((0.20, 0.35, 0.242), (0.45, 0.35, 0.242), (0.45, 0.47, 0.242), (0.20, 0.47, 0.242)),
        mats["oled_manifest"],
    )
    add_part(sm, "Footlocker02_LeftBayCyanLED", cyan_kit, mats["led_cyan"])
    amber_leds = [
        make_beveled_box((0.28, 0.016, 0.025), center=(0.35, 0.32, 0.23), bevel=0.003),
        make_beveled_box((0.18, 0.018, 0.03), center=(-0.36, 0.05, 0.255), bevel=0.004),
        make_beveled_box((0.18, 0.018, 0.03), center=(0.35, 0.05, 0.255), bevel=0.004),
    ]
    add_part(sm, "Footlocker02_DrawerAndSkidAmberLED", merge_geometries(amber_leds), mats["led_amber"])

    # 7. Left Bay Open Lid Translucent Polycarbonate Viewport (alphaMode: "BLEND")
    add_part(sm, "Footlocker02_LeftLidTranslucentViewport", lid_glass, mats["glass_lid"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "footlocker_r1_02.glb"), sm, root_name="FootlockerR1_02_DualBaySplitDrawerTrunk")


# ==============================================================================
# CANDIDATE 03: HEX-FRAME INTERLOCKING ORBITAL LOGISTICS CRATE (`footlocker_r1_03.glb`)
# Dimensions: 1.00m W x 0.58m D x 0.56m H (body) / ~0.80m H (open gullwing doors)
# ==============================================================================
def build_03_hex_interlocking_crate(mats):
    sm = []
    # 1. Three External Carbon-Slate & Machined-Steel Hexagonal Exo-Ribs
    ribs = []
    for rx in [-0.42, 0.0, 0.42]:
        rib_pts = sample_filleted_polyline(
            [(rx, 0.02, 0.27), (rx, 0.28, 0.29), (rx, 0.52, 0.24), (rx, 0.52, -0.24), (rx, 0.28, -0.29), (rx, 0.02, -0.27), (rx, 0.02, 0.27)],
            fillet_radius=0.05,
            corner_subdivs=4,
        )
        ribs.append(make_swept_tube(rib_pts, radius=0.028, radial_segments=10, closed_loop=True, oval_scale=(1.2, 0.85)))
    add_part(sm, "Footlocker03_HexagonalExoRibs", merge_geometries(ribs), mats["carbon_slate"])

    # 2. Inner Gunmetal Pressurized Crate Hull
    crate_hull = [
        make_beveled_box((0.96, 0.14, 0.52), center=(0.0, 0.11, 0.0), bevel=0.025),
        make_beveled_box((0.96, 0.34, 0.05), center=(0.0, 0.32, 0.235), bevel=0.015),
        make_beveled_box((0.96, 0.34, 0.05), center=(0.0, 0.32, -0.235), bevel=0.015),
        make_beveled_box((0.06, 0.34, 0.52), center=(-0.45, 0.32, 0.0), bevel=0.015),
        make_beveled_box((0.06, 0.34, 0.52), center=(0.45, 0.32, 0.0), bevel=0.015),
    ]
    add_part(sm, "Footlocker03_GunmetalPressurizedCrate", merge_geometries(crate_hull), mats["gunmetal"])

    # 3. Stowed 3D Cargo Kit + 2 Extra Cylindrical O2/Power Cells
    foam_bed, navy_roll, white_kit, steel_kit, orange_kit, cyan_kit = make_stowed_cargo_kit(
        bay_cx=0.0, bay_y=0.20, bay_cz=0.0, bay_w=0.82, bay_d=0.40
    )
    add_part(sm, "Footlocker03_CharcoalShockFoam", foam_bed, mats["pad_charcoal"])
    add_part(sm, "Footlocker03_StowedNavyPack", navy_roll, mats["pad_navy"])

    # 4. Dual Gullwing / Butterfly Hinged Translucent Doors Parted Open at 35° on Left & Right
    gull_l_frame = transform_geom(
        make_beveled_box((0.42, 0.036, 0.46), center=(0.21, 0.018, 0.0), bevel=0.01),
        translate=(-0.46, 0.50, 0.0),
        rot_xyz_deg=(0.0, 0.0, 35.0),
    )
    gull_r_frame = transform_geom(
        make_beveled_box((0.42, 0.036, 0.46), center=(-0.21, 0.018, 0.0), bevel=0.01),
        translate=(0.46, 0.50, 0.0),
        rot_xyz_deg=(0.0, 0.0, -35.0),
    )
    gull_l_glass = transform_geom(
        make_quad_panel((0.05, 0.022, 0.18), (0.37, 0.022, 0.18), (0.37, 0.022, -0.18), (0.05, 0.022, -0.18)),
        translate=(-0.46, 0.50, 0.0),
        rot_xyz_deg=(0.0, 0.0, 35.0),
    )
    gull_r_glass = transform_geom(
        make_quad_panel((-0.37, 0.022, 0.18), (-0.05, 0.022, 0.18), (-0.05, 0.022, -0.18), (-0.37, 0.022, -0.18)),
        translate=(0.46, 0.50, 0.0),
        rot_xyz_deg=(0.0, 0.0, -35.0),
    )

    add_part(sm, "Footlocker03_WhiteGullwingRimsAndCanisters", merge_geometries([gull_l_frame, gull_r_frame, white_kit]), mats["aero_white"])

    # 5. Machined-Steel Gullwing Struts, Handles & Four Corner Signal-Orange Stacking Cones
    handles_steel, valve_orange = make_side_handles_and_valve(half_w=0.48, mid_y=0.30)
    g_struts = [
        steel_kit,
        handles_steel,
        make_swept_tube(sample_filleted_polyline([(-0.34, 0.36, 0.18), (-0.24, 0.65, 0.18)], 0.01, 2), radius=0.012, radial_segments=8),
        make_swept_tube(sample_filleted_polyline([(0.34, 0.36, 0.18), (0.24, 0.65, 0.18)], 0.01, 2), radius=0.012, radial_segments=8),
    ]
    add_part(sm, "Footlocker03_MachinedGullwingStruts", merge_geometries(g_struts), mats["steel_machined"])

    cones = [orange_kit, valve_orange]
    for cx_c in [-0.44, 0.44]:
        for cz_c in [-0.22, 0.22]:
            cones.append(make_cylinder(0.032, 0.018, 0.04, center=(cx_c, 0.52, cz_c), segments=10, axis="y"))
    cones.append(make_beveled_box((0.06, 0.10, 0.03), center=(-0.22, 0.34, 0.265), bevel=0.006))
    cones.append(make_beveled_box((0.06, 0.10, 0.03), center=(0.22, 0.34, 0.265), bevel=0.006))
    add_part(sm, "Footlocker03_SignalOrangeStackingCones", merge_geometries(cones), mats["accent_orange"])

    # 6. Central OLED Manifest Strip + Cyan/Amber LEDs + Dual Gullwing Translucent Windows
    add_part(
        sm,
        "Footlocker03_CenterOLEDManifest",
        make_quad_panel((-0.18, 0.25, 0.265), (0.18, 0.25, 0.265), (0.18, 0.41, 0.265), (-0.18, 0.41, 0.265)),
        mats["oled_manifest"],
    )
    add_part(sm, "Footlocker03_InternalCyanLED", cyan_kit, mats["led_cyan"])
    add_part(
        sm,
        "Footlocker03_SkidAmberLED",
        merge_geometries([
            make_beveled_box((0.18, 0.018, 0.03), center=(-0.24, 0.05, 0.27), bevel=0.004),
            make_beveled_box((0.18, 0.018, 0.03), center=(0.24, 0.05, 0.27), bevel=0.004),
        ]),
        mats["led_amber"],
    )
    add_part(sm, "Footlocker03_DualGullwingTranslucentWindows", merge_geometries([gull_l_glass, gull_r_glass]), mats["glass_lid"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "footlocker_r1_03.glb"), sm, root_name="FootlockerR1_03_HexInterlockingCrate")


# ==============================================================================
# CANDIDATE 04: CANTILEVERED BIOMETRIC VAULT & SLIDING TRAY FOOTLOCKER (`footlocker_r1_04.glb`)
# Dimensions: 1.02m W x 0.52m D x 0.54m H (body) / ~0.78m H (cantilevered lid)
# ==============================================================================
def build_04_cantilevered_biometric_vault(mats):
    sm = []
    # 1. Gunmetal Titanium Base Plinth & Angled Biometric Console Housing
    base_hull = [
        make_beveled_box((1.02, 0.14, 0.52), center=(0.0, 0.07, 0.0), bevel=0.03),
        make_beveled_box((0.92, 0.16, 0.10), center=(0.0, 0.34, 0.22), bevel=0.02),
    ]
    add_part(sm, "Footlocker04_GunmetalVaultBase", merge_geometries(base_hull), mats["gunmetal"])

    # 2. Filleted Matte Aerospace-White Vault Body & Cantilevered Rearward-Lifted Lid
    foam_bed, navy_roll, white_kit, steel_kit, orange_kit, cyan_kit = make_stowed_cargo_kit(
        bay_cx=0.0, bay_y=0.22, bay_cz=0.0, bay_w=0.84, bay_d=0.38
    )
    vault_white = [
        make_beveled_box((1.00, 0.34, 0.05), center=(0.0, 0.29, -0.23), bevel=0.02),
        make_beveled_box((0.06, 0.34, 0.48), center=(-0.47, 0.29, 0.0), bevel=0.02),
        make_beveled_box((0.06, 0.34, 0.48), center=(0.47, 0.29, 0.0), bevel=0.02),
        # Cantilevered upper vault lid lifted and shifted rearward (Y = 0.68..0.76, Z = -0.14)
        transform_geom(
            make_sculpted_cushion((0.98, 0.07, 0.46), res=(7, 3, 5), roundness=0.28, belly_puff=0.02, pinch_corners=0.0, crease_freq=0),
            translate=(0.0, 0.71, -0.10),
            rot_xyz_deg=(-18.0, 0.0, 0.0),
        ),
        white_kit,
    ]
    add_part(sm, "Footlocker04_AerospaceWhiteVaultShellAndLid", merge_geometries(vault_white), mats["aero_white"])

    # 3. Four Machined-Steel Pantograph Cantilever Link Arms + Side Handles
    handles_steel, valve_orange = make_side_handles_and_valve(half_w=0.50, mid_y=0.28)
    panto_arms = [steel_kit, handles_steel]
    for sx in [-0.44, 0.44]:
        for sz in [-0.18, 0.02]:
            link = sample_filleted_polyline([(sx, 0.42, sz + 0.08), (sx, 0.70, sz - 0.06)], 0.01, 2)
            panto_arms.append(make_swept_tube(link, radius=0.014, radial_segments=8))
    add_part(sm, "Footlocker04_PantographCantileverArms", merge_geometries(panto_arms), mats["steel_machined"])

    # 4. Precision Charcoal Foam Cutouts & Stowed Navy Flight Kit + Signal-Orange Biometric Locks
    add_part(sm, "Footlocker04_PrecisionCharcoalFoam", foam_bed, mats["pad_charcoal"])
    add_part(sm, "Footlocker04_StowedNavyFlightKit", navy_roll, mats["pad_navy"])
    add_part(
        sm,
        "Footlocker04_SignalOrangeVaultLatches",
        merge_geometries([
            orange_kit,
            valve_orange,
            make_beveled_box((0.06, 0.09, 0.03), center=(-0.34, 0.34, 0.265), bevel=0.006),
            make_beveled_box((0.06, 0.09, 0.03), center=(0.34, 0.34, 0.265), bevel=0.006),
        ]),
        mats["accent_orange"],
    )

    # 5. Prominent Angled Front OLED Biometric Scanner Console + Cyan/Amber LEDs
    add_part(
        sm,
        "Footlocker04_FrontBiometricOLEDConsole",
        make_quad_panel((-0.26, 0.27, 0.272), (0.26, 0.27, 0.272), (0.26, 0.42, 0.272), (-0.26, 0.42, 0.272)),
        mats["oled_manifest"],
    )
    add_part(sm, "Footlocker04_InternalCyanLED", cyan_kit, mats["led_cyan"])
    add_part(
        sm,
        "Footlocker04_SkidAmberLED",
        merge_geometries([
            make_beveled_box((0.18, 0.018, 0.03), center=(-0.32, 0.05, 0.26), bevel=0.004),
            make_beveled_box((0.18, 0.018, 0.03), center=(0.32, 0.05, 0.26), bevel=0.004),
        ]),
        mats["led_amber"],
    )

    # 6. Inner Translucent Polycarbonate Dust Shield over Upper Tool Tier (alphaMode: "BLEND")
    dust_shield = make_quad_panel((-0.43, 0.44, 0.18), (0.43, 0.44, 0.18), (0.43, 0.44, -0.20), (-0.43, 0.44, -0.20))
    add_part(sm, "Footlocker04_TranslucentDustShield", dust_shield, mats["glass_lid"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "footlocker_r1_04.glb"), sm, root_name="FootlockerR1_04_CantileveredBiometricVault")


# ==============================================================================
# CANDIDATE 05: TWIN-CYLINDER PRESSURIZED SURVIVAL & GEAR POD CHEST (`footlocker_r1_05.glb`)
# Dimensions: 1.08m W x 0.56m D x 0.56m H (body) / ~0.82m H (open clamshell)
# ==============================================================================
def build_05_twin_cylinder_survival_chest(mats):
    sm = []
    # 1. 45° Chamfered Gunmetal Cradle & End Bulkhead Caps
    cradle = [
        make_beveled_box((1.08, 0.12, 0.56), center=(0.0, 0.06, 0.0), bevel=0.025),
        make_beveled_box((0.08, 0.44, 0.54), center=(-0.49, 0.28, 0.0), bevel=0.03),
        make_beveled_box((0.08, 0.44, 0.54), center=(0.49, 0.28, 0.0), bevel=0.03),
        make_beveled_box((0.96, 0.24, 0.12), center=(0.0, 0.24, 0.22), bevel=0.02),
    ]
    add_part(sm, "Footlocker05_GunmetalPressureCradle", merge_geometries(cradle), mats["gunmetal"])

    # 2. Twin Horizontal Rounded-Stadium Aerospace-White Pressure Vessels
    foam_bed, navy_roll, white_kit, steel_kit, orange_kit, cyan_kit = make_stowed_cargo_kit(
        bay_cx=0.0, bay_y=0.22, bay_cz=0.0, bay_w=0.84, bay_d=0.40
    )
    vessels = [
        make_cylinder(0.13, 0.13, 0.92, center=(0.0, 0.22, -0.12), segments=16, axis="x"),
        make_cylinder(0.13, 0.13, 0.92, center=(0.0, 0.22, 0.12), segments=16, axis="x"),
        white_kit,
    ]
    add_part(sm, "Footlocker05_TwinHorizontalPressurePods", merge_geometries(vessels), mats["aero_white"])

    # 3. Stowed Foam Bed & Navy Survival Pack
    add_part(sm, "Footlocker05_CharcoalSurvivalFoam", foam_bed, mats["pad_charcoal"])
    add_part(sm, "Footlocker05_StowedNavyPressurePack", navy_roll, mats["pad_navy"])

    # 4. Upper Curved Clamshell Frame & Translucent Viewport Hood Raised at 36° on Twin Struts
    lid_white, lid_steel, lid_glass = make_open_hinged_lid_with_window(
        lid_w=0.90, lid_d=0.48, hinge_pos=(0.0, 0.48, -0.24), open_angle_deg=36.0
    )
    handles_steel, _ = make_side_handles_and_valve(half_w=0.53, mid_y=0.28)
    add_part(sm, "Footlocker05_ClamshellMachinedStrutsAndRims", merge_geometries([lid_white, lid_steel, steel_kit, handles_steel]), mats["steel_machined"])

    # 5. Prominent Sculpted Signal-Orange 4-Spoke Rotary Pressure-Equalization Handwheel on Left End Cap (-X)
    wheel_pts = []
    for k in range(17):
        ang = (k / 16.0) * 2.0 * math.pi
        wheel_pts.append([-0.545, 0.30 + 0.095 * math.sin(ang), 0.095 * math.cos(ang)])
    handwheel = [
        orange_kit,
        make_swept_tube(np.array(wheel_pts, dtype=np.float32), radius=0.014, radial_segments=8, closed_loop=True),
        make_beveled_box((0.025, 0.18, 0.022), center=(-0.545, 0.30, 0.0), bevel=0.004),
        make_beveled_box((0.025, 0.022, 0.18), center=(-0.545, 0.30, 0.0), bevel=0.004),
        make_beveled_box((0.06, 0.10, 0.03), center=(-0.32, 0.28, 0.28), bevel=0.006),
        make_beveled_box((0.06, 0.10, 0.03), center=(0.32, 0.28, 0.28), bevel=0.006),
    ]
    add_part(sm, "Footlocker05_SignalOrangeRotaryHandwheel", merge_geometries(handwheel), mats["accent_orange"])

    # 6. Front Bezel OLED Manifest + Cyan/Amber LEDs + Clamshell Translucent Viewport
    add_part(
        sm,
        "Footlocker05_FrontOLEDManifest",
        make_quad_panel((-0.24, 0.20, 0.282), (0.24, 0.20, 0.282), (0.24, 0.35, 0.282), (-0.24, 0.35, 0.282)),
        mats["oled_manifest"],
    )
    add_part(sm, "Footlocker05_InternalCyanLED", cyan_kit, mats["led_cyan"])
    add_part(
        sm,
        "Footlocker05_SkidAmberLED",
        merge_geometries([
            make_beveled_box((0.18, 0.018, 0.03), center=(-0.34, 0.05, 0.28), bevel=0.004),
            make_beveled_box((0.18, 0.018, 0.03), center=(0.34, 0.05, 0.28), bevel=0.004),
        ]),
        mats["led_amber"],
    )
    add_part(sm, "Footlocker05_ClamshellTranslucentHood", lid_glass, mats["glass_lid"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "footlocker_r1_05.glb"), sm, root_name="FootlockerR1_05_TwinCylinderSurvivalChest")


def build_all_footlocker_round1():
    mats = get_footlocker_materials()
    builders = [
        build_01_octagonal_bench_footlocker,
        build_02_dual_bay_split_drawer_trunk,
        build_03_hex_interlocking_crate,
        build_04_cantilevered_biometric_vault,
        build_05_twin_cylinder_survival_chest,
    ]
    results = []
    for fn in builders:
        info = fn(mats)
        fname = os.path.basename(info["filepath"])
        dims = info["dimensions"]
        print(
            f"[footlocker_r1] Built {fname:20s} | {dims[0]:.2f}m W x {dims[2]:.2f}m D x {dims[1]:.2f}m H | "
            f"verts={info['vertices']:4d} | tris={info['triangles']:4d} | min_y={info['min'][1]:.5f}"
        )
        results.append(info)
    with open(os.path.join(OUT_GLB_DIR, "footlocker_r1_manifest.json"), "w") as f:
        json.dump(results, f, indent=2)
    return results


if __name__ == "__main__":
    build_all_footlocker_round1()
