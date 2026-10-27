#!/usr/bin/env python3
"""
Builds all 5 Round-1 Hard Sci-Fi Room 05 Hero Asset (Heavy Cylindrical Outer-Hull Decompression
Airlock & Umbilical Recharge Chamber) .glb models:
  /workspace/game-project/assets/glb/eva_round1/eva_chamber_r1_01.glb .. eva_chamber_r1_05.glb
Plus exports Winner #02 to /workspace/game-project/assets/glb/winners/,
the Auxiliary Center Donning Bench (eva_suit_prep_bench.glb),
and the Room 05 Architectural Shell (room_05_shell.glb & aliases).

Follows /workspace/game-project/design/eva_round1/eva_chamber_r1_spec.md ("Aegis-7 Standard"):
- Bottom-center (0.0, 0.0, 0.0) floor pivot (min_y == 0.0000, centered X and Z), front facing +Z
- Polygon budget: 3,500 - 5,800 triangles per candidate
- Mandatory 4-Part 3D Decompression & Umbilical Recharge Kit in every candidate:
  1. Heavy Cylindrical / Octagonal-Ringed Decompression Vessel & Mag-Boot Grate Deck (Y = 0.0m-2.55m)
  2. Translucent Curved/Faceted Armored Airlock Door (glass_eva_airlock_translucent.png, alphaMode: "BLEND", alpha ~ 0.19)
     posed partially open/rotated (~32°) + Rear Outer-Hull Deep-Space Porthole Sightline
  3. 3D Sculpted EVA Hard-Suit Rig on Umbilical Gantry inside the chamber + Coiled 3D Life-Support Hoses,
     High-Pressure O2/N2 Cylinders, and Signal-Orange Manual Blowdown Lever
  4. Decompression Telemetry Console (oled_eva_decompression.png) & Translucent UV-Violet (#7B5CFF)
     Helmet Seal-Test / Sterilizer Hood holding a 3D Gold-Visor EVA Test Helmet (eva_visor_gold_iridium.png)
"""
import os
import sys
import math
import json
import shutil
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
)
from corridor_door_round1_generator import make_portal_oct_ring, make_rotary_override_handwheel

TEX_EVA_DIR = "/workspace/game-project/assets/textures/eva_round1"
OUT_GLB_DIR = "/workspace/game-project/assets/glb/eva_round1"
WINNERS_DIR = "/workspace/game-project/assets/glb/winners"
ROOMS_DIR = "/workspace/game-project/assets/glb/rooms"
os.makedirs(OUT_GLB_DIR, exist_ok=True)
os.makedirs(WINNERS_DIR, exist_ok=True)
os.makedirs(ROOMS_DIR, exist_ok=True)


def tex_eva(fname: str) -> str:
    return os.path.join(TEX_EVA_DIR, fname)


def get_eva_materials():
    return {
        "gunmetal": PBRMaterialDef(
            name="Mat_Titanium_GunmetalHull",
            base_color=hex_rgba("#1A1E24"),
            metallic=0.78,
            roughness=0.34,
            texture_path=tex_eva("titanium_gunmetal_hull.png"),
        ),
        "aero_white": PBRMaterialDef(
            name="Mat_Composite_AerospaceWhite",
            base_color=hex_rgba("#D8DEE6"),
            metallic=0.08,
            roughness=0.28,
            texture_path=tex_eva("composite_aerospace_white.png"),
        ),
        "carbon_slate": PBRMaterialDef(
            name="Mat_Carbon_SlateFrame",
            base_color=hex_rgba("#282E38"),
            metallic=0.58,
            roughness=0.40,
            texture_path=tex_eva("carbon_slate_frame.png"),
        ),
        "steel_machined": PBRMaterialDef(
            name="Mat_Steel_MachinedGantry",
            base_color=hex_rgba("#88929E"),
            metallic=0.90,
            roughness=0.20,
            texture_path=tex_eva("steel_machined_gantry.png"),
        ),
        "eva_charcoal": PBRMaterialDef(
            name="Mat_Fabric_CharcoalFlightpad",
            base_color=hex_rgba("#242932"),
            metallic=0.02,
            roughness=0.78,
            texture_path=tex_eva("eva_fabric_ballistic_charcoal.png"),
        ),
        "eva_navy": PBRMaterialDef(
            name="Mat_Fabric_OrbitalNavyPad",
            base_color=hex_rgba("#1D2C3C"),
            metallic=0.02,
            roughness=0.76,
            texture_path=tex_eva("eva_fabric_orbital_navy.png"),
        ),
        "gold_visor": PBRMaterialDef(
            name="Mat_EVA_VisorGoldIridium",
            base_color=hex_rgba("#D49B35"),
            metallic=0.88,
            roughness=0.12,
            emissive=(0.18, 0.11, 0.02),
            texture_path=tex_eva("eva_visor_gold_iridium.png"),
        ),
        "accent_orange": PBRMaterialDef(
            name="Mat_Accent_SignalOrange",
            base_color=hex_rgba("#D95B26"),
            metallic=0.06,
            roughness=0.48,
            texture_path=tex_eva("accent_signal_orange.png"),
        ),
        "oled_decomp": PBRMaterialDef(
            name="Mat_OLED_EVADecompression",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.10,
            roughness=0.14,
            emissive=(0.35, 0.90, 1.0),
            texture_path=tex_eva("oled_eva_decompression.png"),
        ),
        "glass_airlock": PBRMaterialDef(
            name="Mat_Glass_EVAAirlock_Translucent",
            base_color=(0.55, 0.88, 1.0, 0.19),
            metallic=0.10,
            roughness=0.08,
            emissive=(0.0, 0.14, 0.22),
            texture_path=tex_eva("glass_eva_airlock_translucent.png"),
            double_sided=True,
            alpha_mode="BLEND",
        ),
        "led_cyan": PBRMaterialDef(
            name="Mat_Emissive_CyanLED",
            base_color=hex_rgba("#00E5FF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.0, 0.90, 1.0),
            texture_path=tex_eva("led_cyan_strip.png"),
        ),
        "led_amber": PBRMaterialDef(
            name="Mat_Emissive_AmberLED",
            base_color=hex_rgba("#FF9500"),
            metallic=0.0,
            roughness=0.15,
            emissive=(1.0, 0.58, 0.0),
            texture_path=tex_eva("led_amber_strip.png"),
        ),
        "led_uv": PBRMaterialDef(
            name="Mat_Emissive_UVSterilizerLED",
            base_color=hex_rgba("#7B5CFF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.55, 0.38, 1.0),
            texture_path=tex_eva("led_uv_violet.png"),
        ),
    }


# ==============================================================================
# SHARED 3D DECOMPRESSION CHAMBER, EVA HARD-SUIT RIG & UV HELMET HOOD HELPERS
# ==============================================================================
def make_chamber_eva_suit_and_gantry_kit(cx: float = 0.0, cz: float = -0.05, floor_y: float = 0.20):
    """
    Builds a 3D sculpted EVA Hard-Suit Rig + PLSS backpack + Overhead Umbilical Gantry
    + Grab-Rails + Mag-Boots inside the decompression chamber:
    Returns: (white_suit_geom, gold_visor_geom, steel_gantry_geom, charcoal_sleeves_hoses_geom,
              navy_joint_geom, orange_valves_geom, cyan_nozzle_led_geom)
    """
    white_parts = []
    gold_parts = []
    steel_parts = []
    charcoal_parts = []
    navy_parts = []
    orange_parts = []

    # 1. Overhead Machined-Steel Umbilical Suspension Gantry & Blowdown Ring (Y = 2.18m)
    steel_parts.append(make_cylinder(0.42, 0.42, 0.04, center=(cx, 2.22, cz), segments=18, axis="y"))
    yoke = sample_filleted_polyline([(cx - 0.28, 1.54, cz - 0.06), (cx, 2.20, cz - 0.06), (cx + 0.28, 1.54, cz - 0.06)], 0.08, 4)
    steel_parts.append(make_swept_tube(yoke, radius=0.020, radial_segments=8))

    # Interior horizontal curved/angled brushed-steel grab-rails along chamber walls
    for gy in [0.95, 1.45]:
        grab_l = sample_filleted_polyline([(cx - 0.56, gy, cz + 0.32), (cx - 0.56, gy, cz - 0.32)], 0.02, 2)
        grab_r = sample_filleted_polyline([(cx + 0.56, gy, cz + 0.32), (cx + 0.56, gy, cz - 0.32)], 0.02, 2)
        steel_parts.extend([make_swept_tube(grab_l, 0.016, 8), make_swept_tube(grab_r, 0.016, 8)])

    # 2. 3D EVA Helmet (Y = 1.62m..1.90m) with Gold-Iridium Bubble Visor
    h_prof = [(0.0, 0.0), (0.14, 0.01), (0.16, 0.07), (0.165, 0.15), (0.15, 0.23), (0.10, 0.28), (0.0, 0.30)]
    white_parts.append(make_lathe_dome(h_prof, center=(cx, 1.62, cz), segments=12, subdivide_profile=1))
    gold_parts.append(
        transform_geom(
            make_sculpted_cushion((0.26, 0.20, 0.16), res=(4, 3, 3), roundness=0.52, belly_puff=0.08, crease_freq=0),
            translate=(cx, 1.76, cz + 0.08),
            rot_xyz_deg=(6.0, 0.0, 0.0),
        )
    )
    steel_parts.append(make_cylinder(0.15, 0.15, 0.032, center=(cx, 1.61, cz), segments=14, axis="y"))

    # 3. 3D Hard Upper Torso (HUT), Rear PLSS Life-Support Backpack & DCM Chest Pack (Y = 1.05..1.58m)
    white_parts.extend([
        make_sculpted_cushion((0.48, 0.50, 0.30), center=(cx, 1.32, cz), res=(4, 3, 3), roundness=0.34, belly_puff=0.06, pinch_corners=0.10, crease_freq=0),
        make_beveled_box((0.24, 0.22, 0.09), center=(cx, 1.30, cz + 0.16), bevel=0.016),
        # Rear PLSS backpack visible in 3/4 view
        make_beveled_box((0.42, 0.54, 0.18), center=(cx, 1.34, cz - 0.18), bevel=0.025),
    ])
    orange_parts.extend([
        make_cylinder(0.028, 0.028, 0.035, center=(cx + 0.07, 1.24, cz + 0.20), segments=10, axis="z"),
        make_beveled_box((0.09, 0.03, 0.035), center=(cx - 0.06, 1.24, cz + 0.20), bevel=0.005),
    ])

    # Articulated arms & gauntlets
    for s_dir in [-1.0, 1.0]:
        sx = cx + s_dir * 0.29
        arm_pts = sample_filleted_polyline([(sx, 1.44, cz), (sx + s_dir * 0.06, 1.18, cz + 0.05), (sx + s_dir * 0.03, 0.94, cz + 0.12)], 0.06, 4)
        charcoal_parts.append(make_swept_tube(arm_pts, radius=0.070, radius_end=0.055, radial_segments=8))
        steel_parts.append(make_cylinder(0.060, 0.060, 0.028, center=(sx + s_dir * 0.03, 0.93, cz + 0.12), segments=10, axis="y"))
        navy_parts.append(make_sculpted_cushion((0.10, 0.14, 0.12), center=(sx + s_dir * 0.03, 0.85, cz + 0.13), res=(4, 3, 3), roundness=0.40, belly_puff=0.04, crease_freq=0))

    # Waist ring, lower pressure legs & mag-boots on floor grate
    steel_parts.append(make_cylinder(0.20, 0.20, 0.036, center=(cx, 1.04, cz), segments=14, axis="y"))
    navy_parts.append(make_sculpted_cushion((0.40, 0.24, 0.26), center=(cx, 0.92, cz), res=(4, 3, 3), roundness=0.36, belly_puff=0.04, crease_freq=0))
    for b_dir in [-1.0, 1.0]:
        bx = cx + b_dir * 0.16
        leg_pts = sample_filleted_polyline([(bx, 0.82, cz), (bx, 0.54, cz + 0.03), (bx, floor_y + 0.12, cz + 0.02)], 0.05, 3)
        charcoal_parts.append(make_swept_tube(leg_pts, radius=0.078, radius_end=0.064, radial_segments=8))
        steel_parts.append(make_beveled_box((0.14, 0.04, 0.30), center=(bx, floor_y + 0.02, cz + 0.04), bevel=0.01))
        white_parts.append(make_sculpted_cushion((0.13, 0.10, 0.27), center=(bx, floor_y + 0.08, cz + 0.045), res=(4, 2, 4), roundness=0.38, belly_puff=0.04, crease_freq=0))
        orange_parts.append(make_beveled_box((0.06, 0.026, 0.035), center=(bx, floor_y + 0.045, cz + 0.19), bevel=0.005))

    # 4. Two Sweeping Overhead Umbilical Recharge Hoses feeding into the suit's chest/PLSS
    for h_dir in [-1.0, 1.0]:
        u_pts = sample_filleted_polyline(
            [(cx + h_dir * 0.44, 1.98, cz - 0.18), (cx + h_dir * 0.38, 1.48, cz + 0.10), (cx + h_dir * 0.12, 1.32, cz + 0.18)],
            fillet_radius=0.10,
            corner_subdivs=5,
        )
        charcoal_parts.append(make_swept_tube(u_pts, radius=0.022, radial_segments=8))
        orange_parts.append(make_cylinder(0.028, 0.028, 0.038, center=(cx + h_dir * 0.12, 1.32, cz + 0.18), segments=10, axis="z"))

    cyan_led = make_beveled_box((0.76, 0.028, 0.06), center=(cx, 2.24, cz + 0.18), bevel=0.005)

    return (
        merge_geometries(white_parts),
        merge_geometries(gold_parts),
        merge_geometries(steel_parts),
        merge_geometries(charcoal_parts),
        merge_geometries(navy_parts),
        merge_geometries(orange_parts),
        cyan_led,
    )


def make_uv_helmet_test_alcove_and_umbilicals(
    gantry_cx: float,
    gantry_cz: float = 0.0,
    hood_y: float = 1.82,
    console_y: float = 1.15,
):
    """
    Builds Part 3 & Part 4 on the side umbilical gantry:
    - Pressurized UV-Violet (#7B5CFF) Helmet Seal-Test & Sterilization Alcove with a 3D Gold-Visor EVA Helmet
      behind a translucent glass hood
    - Flush OLED Decompression Console (oled_eva_decompression.png)
    - 3 Coiled 3D Umbilical Hoses + Twin High-Pressure O2/N2 Purge Cylinders + Signal-Orange Blowdown Lever
    Returns: (white_helmet_tanks_geom, gold_visor_geom, steel_pedestal_geom, charcoal_hoses_geom,
              orange_valves_lever_geom, oled_screen_geom, uv_led_geom, glass_hood_geom)
    """
    # 1. 3D Gold-Visor EVA Test Helmet inside the UV Sterilizer Alcove
    h_prof = [(0.0, 0.0), (0.12, 0.01), (0.14, 0.06), (0.145, 0.13), (0.13, 0.20), (0.09, 0.25), (0.0, 0.27)]
    white_parts = [
        make_beveled_box((0.54, 0.62, 0.03), center=(gantry_cx, hood_y + 0.12, gantry_cz - 0.22), bevel=0.01),
        make_lathe_dome(h_prof, center=(gantry_cx, hood_y, gantry_cz + 0.02), segments=12, subdivide_profile=1),
        # Lower twin high-pressure O2/N2 purge cylinders (Y = 0.18..0.74m)
        make_cylinder(0.068, 0.068, 0.50, center=(gantry_cx - 0.12, 0.45, gantry_cz + 0.04), segments=12, axis="y"),
        make_cylinder(0.068, 0.068, 0.50, center=(gantry_cx + 0.12, 0.45, gantry_cz + 0.04), segments=12, axis="y"),
    ]
    gold_visor = transform_geom(
        make_sculpted_cushion((0.22, 0.17, 0.14), res=(4, 3, 3), roundness=0.52, belly_puff=0.07, crease_freq=0),
        translate=(gantry_cx, hood_y + 0.12, gantry_cz + 0.09),
        rot_xyz_deg=(6.0, 0.0, 0.0),
    )
    steel_parts = [
        make_cylinder(0.16, 0.16, 0.03, center=(gantry_cx, hood_y - 0.01, gantry_cz + 0.02), segments=14, axis="y"),
        make_beveled_box((0.48, 0.03, 0.05), center=(gantry_cx, 0.46, gantry_cz + 0.14), bevel=0.005),
    ]

    # 2. Three 3D Coiled/Draped Umbilical Recharge Hoses + Signal-Orange Quick-Disconnects & Blowdown Lever
    charcoal_hoses = []
    orange_parts = [
        make_cylinder(0.038, 0.048, 0.08, center=(gantry_cx - 0.12, 0.73, gantry_cz + 0.04), segments=10, axis="y"),
        make_cylinder(0.038, 0.048, 0.08, center=(gantry_cx + 0.12, 0.73, gantry_cz + 0.04), segments=10, axis="y"),
        # Manual signal-orange vacuum blowdown pull lever
        make_beveled_box((0.12, 0.035, 0.04), center=(gantry_cx + 0.16, console_y - 0.18, gantry_cz + 0.28), bevel=0.006),
    ]
    for k, hx_off in enumerate([-0.16, 0.0, 0.14]):
        h_pts = sample_filleted_polyline(
            [
                (gantry_cx + hx_off, console_y - 0.08, gantry_cz + 0.22),
                (gantry_cx + hx_off - 0.04, console_y - 0.26, gantry_cz + 0.28),
                (gantry_cx + hx_off + 0.04, console_y - 0.26, gantry_cz + 0.16),
                (gantry_cx + hx_off, console_y - 0.10, gantry_cz + 0.14),
            ],
            fillet_radius=0.05,
            corner_subdivs=4,
        )
        charcoal_hoses.append(make_swept_tube(h_pts, radius=0.016, radial_segments=8))
        orange_parts.append(make_cylinder(0.022, 0.022, 0.032, center=(gantry_cx + hx_off, console_y - 0.08, gantry_cz + 0.24), segments=8, axis="z"))

    oled_screen = make_quad_panel(
        (gantry_cx - 0.22, console_y - 0.02, gantry_cz + 0.26),
        (gantry_cx + 0.22, console_y - 0.02, gantry_cz + 0.26),
        (gantry_cx + 0.22, console_y + 0.34, gantry_cz + 0.26),
        (gantry_cx - 0.22, console_y + 0.34, gantry_cz + 0.26),
    )
    uv_led = make_beveled_box((0.46, 0.026, 0.04), center=(gantry_cx, hood_y + 0.38, gantry_cz + 0.14), bevel=0.005)
    glass_hood = make_quad_panel(
        (gantry_cx - 0.26, hood_y - 0.08, gantry_cz + 0.26),
        (gantry_cx + 0.26, hood_y - 0.08, gantry_cz + 0.26),
        (gantry_cx + 0.26, hood_y + 0.42, gantry_cz + 0.26),
        (gantry_cx - 0.26, hood_y + 0.42, gantry_cz + 0.26),
    )

    return (
        merge_geometries(white_parts),
        gold_visor,
        merge_geometries(steel_parts),
        merge_geometries(charcoal_hoses),
        merge_geometries(orange_parts),
        oled_screen,
        uv_led,
        glass_hood,
    )


# ==============================================================================
# CANDIDATE 01: AEGIS-7 OCTAGONAL-RINGED CYLINDRICAL DECOMPRESSION LOCK (`eva_chamber_r1_01.glb`)
# Dimensions: 2.25m W x 1.45m D x 2.55m H
# ==============================================================================
def build_01_octagonal_ringed_decompression_lock(mats):
    sm = []
    # 1. Symmetrical Cylindrical Chamber Wrapped in 3 External 45° Octagonal Gunmetal Pressure Collars
    hull = [
        make_beveled_box((2.25, 0.18, 1.45), center=(0.0, 0.09, 0.0), bevel=0.035),
        make_beveled_box((2.25, 0.20, 1.45), center=(0.0, 2.45, 0.0), bevel=0.035),
        make_beveled_box((0.52, 2.22, 1.36), center=(-0.86, 1.26, -0.02), bevel=0.04),
        make_beveled_box((0.52, 2.22, 1.36), center=(0.86, 1.26, -0.02), bevel=0.04),
        # Rear wall with open porthole cutout (X in [-0.34, +0.34], Y in [1.10, 1.78])
        make_beveled_box((1.32, 0.92, 0.12), center=(0.0, 0.64, -0.66), bevel=0.02),
        make_beveled_box((1.32, 0.58, 0.12), center=(0.0, 2.08, -0.66), bevel=0.02),
        make_beveled_box((0.32, 0.72, 0.12), center=(-0.50, 1.44, -0.66), bevel=0.02),
        make_beveled_box((0.32, 0.72, 0.12), center=(0.50, 1.44, -0.66), bevel=0.02),
    ]
    add_part(sm, "EVA01_OctagonalGunmetalPressureHull", merge_geometries(hull), mats["gunmetal"])

    # 2. 3D EVA Hard-Suit Rig on Umbilical Gantry inside Center Chamber + Right Side Helmet Hood & Umbilicals
    w_s, g_s, st_s, ch_s, nv_s, or_s, cy_s = make_chamber_eva_suit_and_gantry_kit(cx=-0.10, cz=-0.04, floor_y=0.19)
    w_u, g_u, st_u, ch_u, or_u, oled_u, uv_u, gl_u = make_uv_helmet_test_alcove_and_umbilicals(
        gantry_cx=0.82, gantry_cz=0.38, hood_y=1.78, console_y=1.14
    )

    add_part(sm, "EVA01_WhiteSuitArmorAndTanks", merge_geometries([w_s, w_u]), mats["aero_white"])
    add_part(sm, "EVA01_GoldIridiumHelmetVisors", merge_geometries([g_s, g_u]), mats["gold_visor"])
    add_part(sm, "EVA01_CharcoalSleevesAndUmbilicalHoses", merge_geometries([ch_s, ch_u]), mats["eva_charcoal"])
    add_part(sm, "EVA01_OrbitalNavySuitJoints", nv_s, mats["eva_navy"])

    # 3. Machined-Steel Mag-Boot Grate Deck, Octagonal Bezel Rings & Dog Latches
    front_ring = make_portal_oct_ring(1.24, 2.18, center_y=1.26, z_pos=0.68, tube_r=0.036, chamfer=0.22)
    front_ring[0][:, 0] -= 0.10
    rear_ring = make_portal_oct_ring(0.74, 0.74, center_y=1.44, z_pos=-0.62, tube_r=0.028, chamfer=0.16)
    steel_all = [
        st_s,
        st_u,
        front_ring,
        rear_ring,
        make_beveled_box((1.16, 0.03, 1.18), center=(-0.10, 0.19, 0.0), bevel=0.008),
    ]
    add_part(sm, "EVA01_MachinedGantryAndBootGrate", merge_geometries(steel_all), mats["steel_machined"])

    wheel_or, _ = make_rotary_override_handwheel(cx=-0.86, cy=1.24, cz=0.68, radius=0.12)
    add_part(sm, "EVA01_SignalOrangeWheelAndValves", merge_geometries([or_s, or_u, wheel_or]), mats["accent_orange"])

    # 4. OLED Console + Practical LEDs + Parted/Rotated Translucent Airlock Door & Rear Porthole (alphaMode: "BLEND")
    add_part(sm, "EVA01_OLEDDecompressionConsole", oled_u, mats["oled_decomp"])
    add_part(sm, "EVA01_CyanPurgeNozzleLED", cy_s, mats["led_cyan"])
    add_part(sm, "EVA01_UVHelmetHoodLED", uv_u, mats["led_uv"])
    add_part(sm, "EVA01_AmberBootDeckLED", make_beveled_box((1.12, 0.024, 0.05), center=(-0.10, 0.16, 0.68), bevel=0.005), mats["led_amber"])

    ajar_door = transform_geom(
        make_quad_panel((-0.52, 0.22, 0.0), (0.36, 0.22, 0.0), (0.36, 2.24, 0.0), (-0.52, 2.24, 0.0)),
        translate=(-0.22, 0.0, 0.68),
        rot_xyz_deg=(0.0, -32.0, 0.0),
    )
    rear_porthole = make_quad_panel((-0.36, 1.08, -0.64), (0.36, 1.08, -0.64), (0.36, 1.80, -0.64), (-0.36, 1.80, -0.64))
    add_part(sm, "EVA01_TranslucentAirlockDoorAndHood", merge_geometries([ajar_door, rear_porthole, gl_u]), mats["glass_airlock"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "eva_chamber_r1_01.glb"), sm, root_name="EVAChamberR1_01_OctagonalDecompressionLock")


# ==============================================================================
# CANDIDATE 02: DUAL-ZONE SPLIT DECOMPRESSION CYLINDER & UMBILICAL SUIT-CHARGE GANTRY (`eva_chamber_r1_02.glb`)
# Dimensions: 2.35m W x 1.45m D x 2.55m H (Signature 65/35 Aegis-7 Split-Bay Sibling!)
# ==============================================================================
def build_02_dual_zone_split_decompression_gantry(mats):
    sm = []
    # 1. Asymmetric 65% / 35% Split-Bay Hull (Left Decompression Chamber: X=-1.175..+0.355, Right Gantry Tower: X=+0.355..+1.175)
    hull = [
        make_beveled_box((2.35, 0.18, 1.45), center=(0.0, 0.09, 0.0), bevel=0.035),
        make_beveled_box((2.35, 0.20, 1.45), center=(0.0, 2.45, 0.0), bevel=0.035),
        make_beveled_box((0.18, 2.24, 1.40), center=(-1.085, 1.26, 0.0), bevel=0.035),
        make_beveled_box((0.14, 2.24, 1.40), center=(1.105, 1.26, 0.0), bevel=0.035),
        # Center structural partition at X = +0.355
        make_beveled_box((0.12, 2.24, 1.38), center=(0.355, 1.26, 0.0), bevel=0.025),
        # Right Gantry Tower shelves & rear plate
        make_beveled_box((0.76, 2.24, 0.10), center=(0.74, 1.26, -0.64), bevel=0.02),
        make_beveled_box((0.72, 0.05, 1.28), center=(0.74, 0.84, 0.0), bevel=0.012),
        make_beveled_box((0.72, 0.05, 1.28), center=(0.74, 1.62, 0.0), bevel=0.012),
        # Left Chamber rear wall with open outer-hull porthole cutout (centered at X = -0.36, Y = 1.44)
        make_beveled_box((1.38, 0.92, 0.12), center=(-0.36, 0.64, -0.66), bevel=0.02),
        make_beveled_box((1.38, 0.58, 0.12), center=(-0.36, 2.08, -0.66), bevel=0.02),
        make_beveled_box((0.34, 0.72, 0.12), center=(-0.88, 1.44, -0.66), bevel=0.02),
        make_beveled_box((0.34, 0.72, 0.12), center=(0.16, 1.44, -0.66), bevel=0.02),
    ]
    add_part(sm, "EVA02_SplitBayGunmetalHull", merge_geometries(hull), mats["gunmetal"])

    # 2. Left Bay 3D EVA Hard-Suit Rig on Umbilical Gantry + Right Tower UV Helmet Test Alcove & Umbilicals
    w_s, g_s, st_s, ch_s, nv_s, or_s, cy_s = make_chamber_eva_suit_and_gantry_kit(cx=-0.36, cz=-0.04, floor_y=0.19)
    w_u, g_u, st_u, ch_u, or_u, oled_u, uv_u, gl_u = make_uv_helmet_test_alcove_and_umbilicals(
        gantry_cx=0.74, gantry_cz=0.40, hood_y=1.74, console_y=1.16
    )

    add_part(sm, "EVA02_WhiteSuitHelmetAndTanks", merge_geometries([w_s, w_u]), mats["aero_white"])
    add_part(sm, "EVA02_GoldIridiumHelmetVisors", merge_geometries([g_s, g_u]), mats["gold_visor"])
    add_part(sm, "EVA02_CharcoalSleevesAndUmbilicalHoses", merge_geometries([ch_s, ch_u]), mats["eva_charcoal"])
    add_part(sm, "EVA02_OrbitalNavySuitJoints", nv_s, mats["eva_navy"])

    # 3. Machined-Steel Mag-Boot Grate, Octagonal Portal Bezel & Interlocking Dog Teeth
    front_ring = make_portal_oct_ring(1.32, 2.20, center_y=1.26, z_pos=0.68, tube_r=0.036, chamfer=0.22)
    front_ring[0][:, 0] -= 0.36
    rear_ring = make_portal_oct_ring(0.74, 0.74, center_y=1.44, z_pos=-0.62, tube_r=0.028, chamfer=0.16)
    rear_ring[0][:, 0] -= 0.36
    steel_all = [
        st_s,
        st_u,
        front_ring,
        rear_ring,
        make_beveled_box((1.24, 0.03, 1.20), center=(-0.36, 0.19, 0.0), bevel=0.008),
        # Interlocking dog-latch teeth along the right edge of the Left Chamber door frame
        make_beveled_box((0.08, 0.12, 0.08), center=(0.26, 0.75, 0.68), bevel=0.012),
        make_beveled_box((0.08, 0.12, 0.08), center=(0.26, 1.26, 0.68), bevel=0.012),
        make_beveled_box((0.08, 0.12, 0.08), center=(0.26, 1.77, 0.68), bevel=0.012),
    ]
    add_part(sm, "EVA02_MachinedGantryGrateAndDogTeeth", merge_geometries(steel_all), mats["steel_machined"])
    add_part(sm, "EVA02_SignalOrangeValvesAndBlowdownLever", merge_geometries([or_s, or_u]), mats["accent_orange"])

    # 4. Right Tower OLED Decompression Console + Practical LEDs + Translucent Airlock Door & UV Helmet Hood
    add_part(sm, "EVA02_RightTowerOLEDConsole", oled_u, mats["oled_decomp"])
    add_part(sm, "EVA02_CyanPurgeNozzleLED", cy_s, mats["led_cyan"])
    add_part(sm, "EVA02_UVHelmetTestHoodLED", uv_u, mats["led_uv"])
    add_part(
        sm,
        "EVA02_AmberBootDeckAndTowerLED",
        merge_geometries([
            make_beveled_box((1.18, 0.024, 0.05), center=(-0.36, 0.16, 0.68), bevel=0.005),
            make_beveled_box((0.62, 0.022, 0.04), center=(0.74, 0.82, 0.66), bevel=0.004),
        ]),
        mats["led_amber"],
    )

    ajar_door = transform_geom(
        make_quad_panel((-0.56, 0.22, 0.0), (0.38, 0.22, 0.0), (0.38, 2.24, 0.0), (-0.56, 2.24, 0.0)),
        translate=(-0.48, 0.0, 0.68),
        rot_xyz_deg=(0.0, -32.0, 0.0),
    )
    rear_porthole = make_quad_panel((-0.72, 1.08, -0.64), (0.0, 1.08, -0.64), (0.0, 1.80, -0.64), (-0.72, 1.80, -0.64))
    add_part(sm, "EVA02_TranslucentAirlockDoorAndHelmetHood", merge_geometries([ajar_door, rear_porthole, gl_u]), mats["glass_airlock"])

    out_p = os.path.join(OUT_GLB_DIR, "eva_chamber_r1_02.glb")
    info = center_and_export_glb(out_p, sm, root_name="EVAChamberR1_02_DualZoneSplitGantry")

    # Copy Winner #02 to all canonical winner aliases
    for w_alias in [
        "eva_chamber_winner_01_split_umbilical_gantry.glb",
        "eva_chamber_winner_01_dual_zone_gantry.glb",
        "eva_chamber_winner_01_decompression_gantry.glb",
        "eva_chamber_winner_01.glb",
    ]:
        shutil.copyfile(out_p, os.path.join(WINNERS_DIR, w_alias))
    return info


# ==============================================================================
# CANDIDATE 03: TWIN-LOCK ROTARY CAROUSEL DECOMPRESSION POD & TETHER RACK (`eva_chamber_r1_03.glb`)
# Dimensions: 2.30m W x 1.48m D x 2.55m H
# ==============================================================================
def build_03_rotary_carousel_decompression_pod(mats):
    sm = []
    hull = [
        make_beveled_box((2.30, 0.18, 1.48), center=(0.0, 0.09, 0.0), bevel=0.035),
        make_beveled_box((2.30, 0.22, 1.48), center=(0.0, 2.44, 0.0), bevel=0.035),
        make_beveled_box((0.48, 2.22, 1.40), center=(-0.91, 1.26, 0.0), bevel=0.04),
        make_beveled_box((0.48, 2.22, 1.40), center=(0.91, 1.26, 0.0), bevel=0.04),
        make_beveled_box((1.38, 0.92, 0.12), center=(0.0, 0.64, -0.68), bevel=0.02),
        make_beveled_box((1.38, 0.58, 0.12), center=(0.0, 2.08, -0.68), bevel=0.02),
    ]
    add_part(sm, "EVA03_RotaryCarouselGunmetalHull", merge_geometries(hull), mats["gunmetal"])

    w_s, g_s, st_s, ch_s, nv_s, or_s, cy_s = make_chamber_eva_suit_and_gantry_kit(cx=-0.12, cz=-0.04, floor_y=0.19)
    w_u, g_u, st_u, ch_u, or_u, oled_u, uv_u, gl_u = make_uv_helmet_test_alcove_and_umbilicals(
        gantry_cx=0.84, gantry_cz=0.40, hood_y=1.76, console_y=1.14
    )

    add_part(sm, "EVA03_WhiteSuitAndTanks", merge_geometries([w_s, w_u]), mats["aero_white"])
    add_part(sm, "EVA03_GoldIridiumVisors", merge_geometries([g_s, g_u]), mats["gold_visor"])
    add_part(sm, "EVA03_CharcoalSleevesAndTethers", merge_geometries([ch_s, ch_u]), mats["eva_charcoal"])
    add_part(sm, "EVA03_NavyTetherPack", nv_s, mats["eva_navy"])

    steel_all = [
        st_s,
        st_u,
        make_cylinder(0.68, 0.68, 0.06, center=(-0.12, 2.30, 0.0), segments=18, axis="y"),
        make_cylinder(0.68, 0.68, 0.06, center=(-0.12, 0.20, 0.0), segments=18, axis="y"),
        make_cylinder(0.08, 0.08, 0.44, center=(-0.88, 1.54, 0.68), segments=12, axis="x"),
    ]
    add_part(sm, "EVA03_CarouselDrumRingsAndWinch", merge_geometries(steel_all), mats["steel_machined"])
    add_part(sm, "EVA03_SignalOrangeTetherHooks", merge_geometries([or_s, or_u]), mats["accent_orange"])

    add_part(sm, "EVA03_OLEDDecompressionPillar", oled_u, mats["oled_decomp"])
    add_part(sm, "EVA03_CyanPurgeLED", cy_s, mats["led_cyan"])
    add_part(sm, "EVA03_UVHelmetLED", uv_u, mats["led_uv"])
    add_part(sm, "EVA03_AmberCarouselLED", make_beveled_box((1.24, 0.024, 0.05), center=(-0.12, 0.16, 0.70), bevel=0.005), mats["led_amber"])

    drum_panes = [
        make_quad_panel((-0.64, 0.24, 0.66), (-0.18, 0.24, 0.72), (-0.18, 2.26, 0.72), (-0.64, 2.26, 0.66)),
        make_quad_panel((0.02, 0.24, 0.72), (0.42, 0.24, 0.64), (0.42, 2.26, 0.64), (0.02, 2.26, 0.72)),
        gl_u,
    ]
    add_part(sm, "EVA03_RevolvingDrumTranslucentPanes", merge_geometries(drum_panes), mats["glass_airlock"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "eva_chamber_r1_03.glb"), sm, root_name="EVAChamberR1_03_RotaryCarouselPod")


# ==============================================================================
# CANDIDATE 04: HEX-BULKHEAD RAPID BLOWDOWN AIRLOCK & SUIT DONNING FRAME (`eva_chamber_r1_04.glb`)
# Dimensions: 2.28m W x 1.42m D x 2.55m H
# ==============================================================================
def build_04_hex_blowdown_donning_frame(mats):
    sm = []
    hull = [
        make_beveled_box((2.28, 0.18, 1.42), center=(0.0, 0.09, 0.0), bevel=0.035),
        make_beveled_box((2.28, 0.20, 1.42), center=(0.0, 2.45, 0.0), bevel=0.035),
        make_beveled_box((0.46, 2.24, 1.36), center=(-0.91, 1.26, 0.0), bevel=0.035),
        make_beveled_box((0.46, 2.24, 1.36), center=(0.91, 1.26, 0.0), bevel=0.035),
        make_beveled_box((1.42, 0.92, 0.12), center=(0.0, 0.64, -0.65), bevel=0.02),
        make_beveled_box((1.42, 0.58, 0.12), center=(0.0, 2.08, -0.65), bevel=0.02),
    ]
    add_part(sm, "EVA04_HexBlowdownCarbonHull", merge_geometries(hull), mats["carbon_slate"])

    w_s, g_s, st_s, ch_s, nv_s, or_s, cy_s = make_chamber_eva_suit_and_gantry_kit(cx=-0.10, cz=-0.04, floor_y=0.19)
    w_u, g_u, st_u, ch_u, or_u, oled_u, uv_u, gl_u = make_uv_helmet_test_alcove_and_umbilicals(
        gantry_cx=0.84, gantry_cz=0.38, hood_y=1.76, console_y=1.14
    )

    add_part(sm, "EVA04_WhiteSuitAndTanks", merge_geometries([w_s, w_u]), mats["aero_white"])
    add_part(sm, "EVA04_GoldIridiumVisors", merge_geometries([g_s, g_u]), mats["gold_visor"])
    add_part(sm, "EVA04_CharcoalSleevesAndBooms", merge_geometries([ch_s, ch_u]), mats["eva_charcoal"])
    add_part(sm, "EVA04_NavySuitJoints", nv_s, mats["eva_navy"])

    hex_ring = make_portal_oct_ring(1.36, 2.22, center_y=1.26, z_pos=0.66, tube_r=0.038, chamfer=0.34)
    hex_ring[0][:, 0] -= 0.10
    add_part(sm, "EVA04_MachinedHexFrameAndDonningRing", merge_geometries([st_s, st_u, hex_ring]), mats["steel_machined"])
    add_part(sm, "EVA04_SignalOrangeBlowdownValves", merge_geometries([or_s, or_u]), mats["accent_orange"])

    add_part(sm, "EVA04_OLEDTelemetryConsole", oled_u, mats["oled_decomp"])
    add_part(sm, "EVA04_CyanPlasmaDeconLED", cy_s, mats["led_cyan"])
    add_part(sm, "EVA04_UVSterilizerLED", uv_u, mats["led_uv"])
    add_part(sm, "EVA04_AmberStepLED", make_beveled_box((1.20, 0.024, 0.05), center=(-0.10, 0.16, 0.68), bevel=0.005), mats["led_amber"])

    hex_doors = [
        make_quad_panel((-0.68, 0.22, 0.66), (-0.24, 0.22, 0.68), (-0.24, 2.26, 0.68), (-0.68, 2.26, 0.66)),
        make_quad_panel((0.04, 0.22, 0.68), (0.48, 0.22, 0.66), (0.48, 2.26, 0.66), (0.04, 2.26, 0.68)),
        gl_u,
    ]
    add_part(sm, "EVA04_BiPartingHexTranslucentDoors", merge_geometries(hex_doors), mats["glass_airlock"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "eva_chamber_r1_04.glb"), sm, root_name="EVAChamberR1_04_HexBlowdownDonningFrame")


# ==============================================================================
# CANDIDATE 05: HEAVY SUBMARINE-STYLE PLUG-HATCH EVA LOCK & CRYO-O2 BANK (`eva_chamber_r1_05.glb`)
# Dimensions: 2.35m W x 1.50m D x 2.58m H
# ==============================================================================
def build_05_submarine_plughatch_cryo_lock(mats):
    sm = []
    hull = [
        make_beveled_box((2.35, 0.18, 1.50), center=(0.0, 0.09, 0.0), bevel=0.035),
        make_beveled_box((2.35, 0.22, 1.50), center=(0.0, 2.47, 0.0), bevel=0.035),
        make_beveled_box((0.50, 2.24, 1.42), center=(-0.925, 1.28, 0.0), bevel=0.04),
        make_beveled_box((0.50, 2.24, 1.42), center=(0.925, 1.28, 0.0), bevel=0.04),
        make_beveled_box((1.42, 0.92, 0.12), center=(0.0, 0.64, -0.68), bevel=0.02),
        make_beveled_box((1.42, 0.58, 0.12), center=(0.0, 2.10, -0.68), bevel=0.02),
    ]
    add_part(sm, "EVA05_SubmarinePlugGunmetalHull", merge_geometries(hull), mats["gunmetal"])

    w_s, g_s, st_s, ch_s, nv_s, or_s, cy_s = make_chamber_eva_suit_and_gantry_kit(cx=-0.12, cz=-0.04, floor_y=0.19)
    w_u, g_u, st_u, ch_u, or_u, oled_u, uv_u, gl_u = make_uv_helmet_test_alcove_and_umbilicals(
        gantry_cx=0.86, gantry_cz=0.40, hood_y=1.78, console_y=1.16
    )

    add_part(sm, "EVA05_WhiteSuitAndCryoO2Bank", merge_geometries([w_s, w_u]), mats["aero_white"])
    add_part(sm, "EVA05_GoldIridiumVisors", merge_geometries([g_s, g_u]), mats["gold_visor"])
    add_part(sm, "EVA05_CharcoalSleevesAndHoses", merge_geometries([ch_s, ch_u]), mats["eva_charcoal"])
    add_part(sm, "EVA05_NavySuitJoints", nv_s, mats["eva_navy"])

    wheel_or, wheel_st = make_rotary_override_handwheel(cx=-0.56, cy=1.24, cz=0.75, radius=0.15)
    plug_ring = make_portal_oct_ring(1.32, 2.20, center_y=1.28, z_pos=0.68, tube_r=0.040, chamfer=0.28)
    plug_ring[0][:, 0] -= 0.12
    add_part(sm, "EVA05_MachinedPlugRingAndRadialDogs", merge_geometries([st_s, st_u, plug_ring, wheel_st]), mats["steel_machined"])
    add_part(sm, "EVA05_SignalOrangeSpiderHandwheel", merge_geometries([or_s, or_u, wheel_or]), mats["accent_orange"])

    add_part(sm, "EVA05_OLEDDecompressionConsole", oled_u, mats["oled_decomp"])
    add_part(sm, "EVA05_CyanPurgeLED", cy_s, mats["led_cyan"])
    add_part(sm, "EVA05_UVHelmetLED", uv_u, mats["led_uv"])
    add_part(sm, "EVA05_AmberThresholdLED", make_beveled_box((1.22, 0.024, 0.05), center=(-0.12, 0.16, 0.70), bevel=0.005), mats["led_amber"])

    plug_glass = transform_geom(
        make_quad_panel((-0.54, 0.24, 0.0), (0.36, 0.24, 0.0), (0.36, 2.26, 0.0), (-0.54, 2.26, 0.0)),
        translate=(-0.24, 0.0, 0.69),
        rot_xyz_deg=(0.0, -34.0, 0.0),
    )
    add_part(sm, "EVA05_OutwardSwingingPlugTranslucentGlass", merge_geometries([plug_glass, gl_u]), mats["glass_airlock"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "eva_chamber_r1_05.glb"), sm, root_name="EVAChamberR1_05_SubmarinePlugHatchLock")


# ==============================================================================
# ROOM 05 AUXILIARY PROP (`eva_suit_prep_bench.glb`) & SHELL (`room_05_shell.glb`)
# ==============================================================================
def build_eva_suit_prep_bench(mats):
    """
    Builds Auxiliary Center Donning Bench (eva_suit_prep_bench.glb):
    Low-profile 2.20m W x 0.85m D x 0.52m H chamfered titanium & charcoal-flightpad crew suit-donning bench
    with center tool/tether rack and under-seat amber floor glow.
    """
    sm = []
    chassis = [
        make_beveled_box((2.20, 0.12, 0.85), center=(0.0, 0.06, 0.0), bevel=0.025),
        make_beveled_box((1.96, 0.28, 0.68), center=(0.0, 0.24, 0.0), bevel=0.025),
    ]
    add_part(sm, "PrepBench_GunmetalChassis", merge_geometries(chassis), mats["gunmetal"])

    cushions = [
        make_sculpted_cushion((0.92, 0.09, 0.36), center=(-0.56, 0.44, -0.21), res=(6, 3, 5), roundness=0.35, belly_puff=0.04, tuft_grid=(3, 2), tuft_depth=0.012, crease_freq=0),
        make_sculpted_cushion((0.92, 0.09, 0.36), center=(0.56, 0.44, -0.21), res=(6, 3, 5), roundness=0.35, belly_puff=0.04, tuft_grid=(3, 2), tuft_depth=0.012, crease_freq=0),
        make_sculpted_cushion((0.92, 0.09, 0.36), center=(-0.56, 0.44, 0.21), res=(6, 3, 5), roundness=0.35, belly_puff=0.04, tuft_grid=(3, 2), tuft_depth=0.012, crease_freq=0),
        make_sculpted_cushion((0.92, 0.09, 0.36), center=(0.56, 0.44, 0.21), res=(6, 3, 5), roundness=0.35, belly_puff=0.04, tuft_grid=(3, 2), tuft_depth=0.012, crease_freq=0),
    ]
    add_part(sm, "PrepBench_CharcoalFlightpadSeats", merge_geometries(cushions), mats["eva_charcoal"])

    rack = [
        make_beveled_box((0.16, 0.14, 0.82), center=(0.0, 0.45, 0.0), bevel=0.02),
        make_cylinder(0.016, 0.016, 2.04, center=(0.0, 0.50, 0.0), segments=10, axis="x"),
    ]
    add_part(sm, "PrepBench_CenterToolAndTetherRack", merge_geometries(rack), mats["steel_machined"])
    add_part(
        sm,
        "PrepBench_SignalOrangeTetherClamps",
        merge_geometries([
            make_beveled_box((0.08, 0.04, 0.12), center=(-0.45, 0.50, 0.0), bevel=0.006),
            make_beveled_box((0.08, 0.04, 0.12), center=(0.45, 0.50, 0.0), bevel=0.006),
        ]),
        mats["accent_orange"],
    )
    add_part(
        sm,
        "PrepBench_UnderSeatAmberGlow",
        merge_geometries([
            make_beveled_box((1.88, 0.022, 0.04), center=(0.0, 0.14, 0.38), bevel=0.004),
            make_beveled_box((1.88, 0.022, 0.04), center=(0.0, 0.14, -0.38), bevel=0.004),
        ]),
        mats["led_amber"],
    )

    p_main = os.path.join(WINNERS_DIR, "eva_suit_prep_bench.glb")
    info = center_and_export_glb(p_main, sm, root_name="EVASuitPrepBench")
    for dst in [
        os.path.join(OUT_GLB_DIR, "eva_suit_prep_bench.glb"),
        os.path.join(ROOMS_DIR, "eva_suit_prep_bench.glb"),
        "/workspace/game-project/assets/glb/eva_suit_prep_bench.glb",
    ]:
        shutil.copyfile(p_main, dst)
    print(f"[eva_prep_bench] Exported {p_main} ({info['triangles']} tris)")
    return info


def build_room_05_eva_airlock_shell(mats):
    """
    Builds Room 05 — EVA Prep & Airlock Staging Bay Architectural Shell (7.5m W x 8.5m D x 3.4m H):
    - 5 Repeating 45° Chamfered Octagonal Titanium Ribs (Z = -4.0, -2.0, 0.0, +2.0, +4.0)
    - Overhead Machined-Steel Suit-Handling Monorail Tracks (Y = 3.05m)
    - Heavy Mag-Boot Charging Deck Grates (X = ±2.10m) with recessed Amber (#FF9500) guide strips
    - North Outer-Hull Deep-Space Observation Windows (Z = -4.20m flanking the Decompression Chamber at X = ±2.35m)
      glazed with alphaMode: "BLEND" translucent glass (alpha ~ 0.18)
    """
    sm = []
    slate_deck = [
        make_beveled_box((7.50, 0.06, 8.50), center=(0.0, 0.03, 0.0), bevel=0.015),
        make_beveled_box((0.12, 3.28, 8.40), center=(-3.69, 1.70, 0.0), bevel=0.02),
        make_beveled_box((0.12, 3.28, 8.40), center=(3.69, 1.70, 0.0), bevel=0.02),
        # North wall lower sill & upper header around twin outer-hull observation windows (X = ±2.35m, Y = 0.90..2.45m)
        make_beveled_box((7.40, 0.84, 0.12), center=(0.0, 0.48, -4.19), bevel=0.02),
        make_beveled_box((7.40, 0.90, 0.12), center=(0.0, 2.90, -4.19), bevel=0.02),
        make_beveled_box((2.40, 1.60, 0.12), center=(0.0, 1.68, -4.19), bevel=0.02),
        make_beveled_box((0.50, 1.60, 0.12), center=(-3.45, 1.68, -4.19), bevel=0.02),
        make_beveled_box((0.50, 1.60, 0.12), center=(3.45, 1.68, -4.19), bevel=0.02),
    ]
    add_part(sm, "Room05_CarbonSlateDeckAndBulkheads", merge_geometries(slate_deck), mats["carbon_slate"])

    gunmetal_ribs = [
        make_beveled_box((7.50, 0.06, 8.50), center=(0.0, 3.37, 0.0), bevel=0.015),
    ]
    for z_rib in [-4.0, -2.0, 0.0, 2.0, 4.0]:
        gunmetal_ribs.extend([
            make_beveled_box((0.20, 3.28, 0.22), center=(-3.58, 1.70, z_rib), bevel=0.03),
            make_beveled_box((0.20, 3.28, 0.22), center=(3.58, 1.70, z_rib), bevel=0.03),
            make_beveled_box((7.36, 0.20, 0.22), center=(0.0, 3.26, z_rib), bevel=0.03),
            transform_geom(make_beveled_box((0.72, 0.18, 0.22), bevel=0.02), translate=(-3.26, 3.00, z_rib), rot_xyz_deg=(0.0, 0.0, 45.0)),
            transform_geom(make_beveled_box((0.72, 0.18, 0.22), bevel=0.02), translate=(3.26, 3.00, z_rib), rot_xyz_deg=(0.0, 0.0, -45.0)),
        ])
    add_part(sm, "Room05_OctagonalTitaniumRibs", merge_geometries(gunmetal_ribs), mats["gunmetal"])

    # Overhead Machined-Steel Monorail Tracks & Floor Mag-Boot Grates
    win_bezel_l = make_portal_oct_ring(1.96, 1.56, center_y=1.68, z_pos=-4.14, tube_r=0.032, chamfer=0.22)
    win_bezel_l[0][:, 0] -= 2.20
    win_bezel_r = make_portal_oct_ring(1.96, 1.56, center_y=1.68, z_pos=-4.14, tube_r=0.032, chamfer=0.22)
    win_bezel_r[0][:, 0] += 2.20

    steel_parts = [
        win_bezel_l,
        win_bezel_r,
        make_beveled_box((0.08, 0.12, 8.0), center=(-1.85, 3.05, 0.0), bevel=0.015),
        make_beveled_box((0.08, 0.12, 8.0), center=(1.85, 3.05, 0.0), bevel=0.015),
        make_beveled_box((0.85, 0.016, 7.6), center=(-2.10, 0.065, 0.0), bevel=0.004),
        make_beveled_box((0.85, 0.016, 7.6), center=(2.10, 0.065, 0.0), bevel=0.004),
    ]
    add_part(sm, "Room05_MonorailTracksAndBootGrates", merge_geometries(steel_parts), mats["steel_machined"])

    amber_guides = [
        make_beveled_box((0.04, 0.014, 7.6), center=(-1.55, 0.066, 0.0), bevel=0.003),
        make_beveled_box((0.04, 0.014, 7.6), center=(1.55, 0.066, 0.0), bevel=0.003),
    ]
    add_part(sm, "Room05_AmberFloorGuides", merge_geometries(amber_guides), mats["led_amber"])

    cyan_coves = [
        make_beveled_box((0.05, 0.03, 7.8), center=(-2.45, 3.16, 0.0), bevel=0.005),
        make_beveled_box((0.05, 0.03, 7.8), center=(2.45, 3.16, 0.0), bevel=0.005),
    ]
    add_part(sm, "Room05_CyanCeilingCoves", merge_geometries(cyan_coves), mats["led_cyan"])

    north_windows = [
        make_quad_panel((-3.16, 0.90, -4.16), (-1.24, 0.90, -4.16), (-1.24, 2.46, -4.16), (-3.16, 2.46, -4.16)),
        make_quad_panel((1.24, 0.90, -4.16), (3.16, 0.90, -4.16), (3.16, 2.46, -4.16), (1.24, 2.46, -4.16)),
    ]
    add_part(sm, "Room05_NorthDeepSpaceTranslucentViewports", merge_geometries(north_windows), mats["glass_airlock"])

    p_main = os.path.join(ROOMS_DIR, "room_05_shell.glb")
    info = center_and_export_glb(p_main, sm, root_name="Room05_EVAAirlockBayShell")
    for dst in [
        os.path.join(ROOMS_DIR, "room_05_eva_shell.glb"),
        os.path.join(ROOMS_DIR, "room_05_eva_airlock_bay_shell.glb"),
        "/workspace/game-project/assets/glb/room_05_eva_shell.glb",
        "/workspace/game-project/assets/glb/room_05_shell.glb",
    ]:
        shutil.copyfile(p_main, dst)
    print(f"[room_05_shell] Exported {p_main} and aliases ({info['triangles']} tris)")
    return info


def build_all_eva_round1():
    mats = get_eva_materials()
    builders = [
        build_01_octagonal_ringed_decompression_lock,
        build_02_dual_zone_split_decompression_gantry,
        build_03_rotary_carousel_decompression_pod,
        build_04_hex_blowdown_donning_frame,
        build_05_submarine_plughatch_cryo_lock,
    ]
    results = []
    for fn in builders:
        info = fn(mats)
        fname = os.path.basename(info["filepath"])
        dims = info["dimensions"]
        print(
            f"[eva_r1] Built {fname:22s} | {dims[0]:.2f}m W x {dims[2]:.2f}m D x {dims[1]:.2f}m H | "
            f"verts={info['vertices']:4d} | tris={info['triangles']:4d} | min_y={info['min'][1]:.5f}"
        )
        results.append(info)
    with open(os.path.join(OUT_GLB_DIR, "eva_r1_manifest.json"), "w") as f:
        json.dump(results, f, indent=2)

    build_eva_suit_prep_bench(mats)
    build_room_05_eva_airlock_shell(mats)
    return results


if __name__ == "__main__":
    build_all_eva_round1()
