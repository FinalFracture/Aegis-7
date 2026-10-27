#!/usr/bin/env python3
"""
Builds all 5 Round-1 Hard Sci-Fi EVA Suit & Personal Gear Locker .glb models:
/workspace/game-project/assets/glb/locker_round1/locker_r1_01.glb .. locker_r1_05.glb

Follows /workspace/game-project/design/locker_round1/locker_r1_spec.md:
- Bottom-center (0.0, 0.0, 0.0) floor pivot (min_y == 0.0000, centered X/Z), front facing +Z
- Polygon budget: 3,000 - 6,000 triangles per candidate
- Mandatory 4-part 3D Interior EVA Gear Kit inside every locker:
  1. 3D EVA Helmet with Gold-Iridium Bubble Visor, side comm pods, headlamp bezel & neck ring
  2. 3D Hard-Shell EVA Suit Torso (HUT) with DCM OLED chest pack, signal-orange purge valve,
     articulated shoulder joints, hanging pressure sleeves, wrist rings & EVA gauntlets
  3. 3D Curved Spline Life-Support Umbilical Hoses with quick-disconnect couplings
  4. 3D Magnetic Boots Pair with machined steel soles, armored toe caps, calf gaiters & ankle clamps
- True alphaMode: "BLEND" translucent suit-bay doors (glass_suitbay_translucent.png / glass_uv_sterilizer_violet.png)
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
    make_curved_canopy_shield,
)

TEX_LOCKER_DIR = "/workspace/game-project/assets/textures/locker_round1"
OUT_GLB_DIR = "/workspace/game-project/assets/glb/locker_round1"
os.makedirs(OUT_GLB_DIR, exist_ok=True)


def tex_lk(fname: str) -> str:
    return os.path.join(TEX_LOCKER_DIR, fname)


def get_locker_materials():
    return {
        "gunmetal": PBRMaterialDef(
            name="Mat_Titanium_GunmetalHull",
            base_color=hex_rgba("#1A1E24"),
            metallic=0.78,
            roughness=0.34,
            texture_path=tex_lk("titanium_gunmetal_hull.png"),
        ),
        "aero_white": PBRMaterialDef(
            name="Mat_Composite_AerospaceWhite",
            base_color=hex_rgba("#D8DEE6"),
            metallic=0.08,
            roughness=0.30,
            texture_path=tex_lk("composite_aerospace_white.png"),
        ),
        "carbon_slate": PBRMaterialDef(
            name="Mat_Carbon_SlateFrame",
            base_color=hex_rgba("#282E38"),
            metallic=0.58,
            roughness=0.40,
            texture_path=tex_lk("carbon_slate_frame.png"),
        ),
        "steel_gantry": PBRMaterialDef(
            name="Mat_Steel_MachinedGantry",
            base_color=hex_rgba("#88929E"),
            metallic=0.90,
            roughness=0.22,
            texture_path=tex_lk("steel_machined_gantry.png"),
        ),
        "eva_charcoal": PBRMaterialDef(
            name="Mat_EVA_BallisticCharcoal",
            base_color=hex_rgba("#242932"),
            metallic=0.02,
            roughness=0.78,
            texture_path=tex_lk("eva_fabric_ballistic_charcoal.png"),
        ),
        "eva_navy": PBRMaterialDef(
            name="Mat_EVA_OrbitalNavy",
            base_color=hex_rgba("#1D2C3C"),
            metallic=0.02,
            roughness=0.76,
            texture_path=tex_lk("eva_fabric_orbital_navy.png"),
        ),
        "gold_visor": PBRMaterialDef(
            name="Mat_EVA_VisorGoldIridium",
            base_color=hex_rgba("#D49B35"),
            metallic=0.88,
            roughness=0.12,
            emissive=(0.18, 0.11, 0.02),
            texture_path=tex_lk("eva_visor_gold_iridium.png"),
        ),
        "accent_orange": PBRMaterialDef(
            name="Mat_Accent_SignalOrange",
            base_color=hex_rgba("#D95B26"),
            metallic=0.06,
            roughness=0.48,
            texture_path=tex_lk("accent_signal_orange.png"),
        ),
        "glass_suitbay": PBRMaterialDef(
            name="Mat_Glass_SuitBay_Translucent",
            base_color=(0.55, 0.85, 1.0, 0.18),
            metallic=0.10,
            roughness=0.08,
            emissive=(0.0, 0.10, 0.16),
            texture_path=tex_lk("glass_suitbay_translucent.png"),
            double_sided=True,
            alpha_mode="BLEND",
        ),
        "glass_uv_violet": PBRMaterialDef(
            name="Mat_Glass_UVSterilizer_Translucent",
            base_color=(0.68, 0.56, 1.0, 0.19),
            metallic=0.10,
            roughness=0.08,
            emissive=(0.12, 0.08, 0.24),
            texture_path=tex_lk("glass_uv_sterilizer_violet.png"),
            double_sided=True,
            alpha_mode="BLEND",
        ),
        "oled_diag": PBRMaterialDef(
            name="Mat_OLED_SuitDiagnostics",
            base_color=hex_rgba("#0A0E14"),
            metallic=0.10,
            roughness=0.15,
            emissive=(0.22, 0.82, 1.0),
            texture_path=tex_lk("oled_suit_diagnostics.png"),
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
        "led_uv": PBRMaterialDef(
            name="Mat_Emissive_UVSterilizerLED",
            base_color=hex_rgba("#7B5CFF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.55, 0.38, 1.0),
        ),
        "led_ice": PBRMaterialDef(
            name="Mat_Emissive_IceWhiteLED",
            base_color=hex_rgba("#E0F4FF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.86, 0.95, 1.0),
        ),
    }


# ==============================================================================
# SHARED 4-PART 3D INTERIOR EVA SUIT & LIFE-SUPPORT GEAR KIT GENERATOR
# ==============================================================================
def add_eva_suit_interior_kit(
    sm_list,
    mats,
    center_x: float = 0.0,
    center_z: float = -0.04,
    helmet_y: float = 1.56,
    torso_y: float = 1.12,
    boot_y: float = 0.20,
    num_umbilicals: int = 2,
):
    """
    Adds the Mandatory 4-Part 3D Interior EVA Suit & Gear Kit centered at (center_x, center_z):
    1. 3D EVA Helmet (white shell dome, side ear/comm pods, headlamp bezel, Gold-Iridium Bubble Visor, neck disconnect ring)
    2. 3D Hard-Shell EVA Suit Torso (HUT) & Articulated Shoulders/Arms/Gauntlets + DCM Chest Pack with OLED & Orange Purge Valve
    3. 3D Life-Support Umbilical Hoses with quick-disconnect couplings
    4. 3D Magnetic Boots Pair (machined steel magnetic soles, white armored toe caps, charcoal calf gaiters, ankle clamp rings)
    """
    white_armor = []
    gold_visor = []
    steel_parts = []
    charcoal_fabric = []
    navy_fabric = []
    orange_accents = []
    oled_parts = []

    # --- 1. 3D EVA HELMET (Y ~ helmet_y to helmet_y + 0.28m) ---
    # Outer pressure helmet shell dome & rear shroud
    helmet_profile = [
        (0.00, 0.00),
        (0.135, 0.01),
        (0.155, 0.06),
        (0.160, 0.14),
        (0.148, 0.22),
        (0.105, 0.27),
        (0.00, 0.29),
    ]
    white_armor.append(make_lathe_dome(helmet_profile, center=(center_x, helmet_y, center_z - 0.01), segments=16, subdivide_profile=1))
    # Top headlamp housing & side ear/comm pods
    white_armor.append(make_beveled_box((0.12, 0.045, 0.14), center=(center_x, helmet_y + 0.265, center_z + 0.04), bevel=0.01))
    steel_parts.append(make_cylinder(0.042, 0.042, 0.33, center=(center_x, helmet_y + 0.13, center_z), segments=12, axis="x"))

    # Curved spherical Gold-Iridium Bubble Visor facing +Z
    visor_dome = transform_geom(
        make_sculpted_cushion(
            (0.25, 0.19, 0.16),
            res=(6, 4, 4),
            roundness=0.52,
            belly_puff=0.08,
            pinch_corners=0.0,
            crease_freq=0,
        ),
        translate=(center_x, helmet_y + 0.135, center_z + 0.075),
        rot_xyz_deg=(6.0, 0.0, 0.0),
    )
    gold_visor.append(visor_dome)

    # Machined steel neck disconnect ring & overhead suspension yoke
    steel_parts.append(make_cylinder(0.145, 0.145, 0.032, center=(center_x, helmet_y - 0.01, center_z), segments=18, axis="y"))
    yoke_pts = sample_filleted_polyline(
        [
            (center_x - 0.24, torso_y + 0.28, center_z - 0.04),
            (center_x, helmet_y + 0.36, center_z - 0.04),
            (center_x + 0.24, torso_y + 0.28, center_z - 0.04),
        ],
        fillet_radius=0.08,
        corner_subdivs=5,
    )
    steel_parts.append(make_swept_tube(yoke_pts, radius=0.018, radial_segments=10))

    # --- 2. 3D HARD-SHELL EVA SUIT TORSO (HUT) & ARTICULATED ARMS ---
    # Sculpted Hard Upper Torso chestplate & shoulder bells
    white_armor.append(
        make_sculpted_cushion(
            (0.46, 0.48, 0.29),
            center=(center_x, torso_y + 0.06, center_z),
            res=(4, 3, 3),
            roundness=0.34,
            belly_puff=0.06,
            pinch_corners=0.10,
            crease_freq=0,
        )
    )
    # Chamfered pectoral armor plates & DCM chest pack housing
    white_armor.append(make_beveled_box((0.38, 0.18, 0.06), center=(center_x, torso_y + 0.16, center_z + 0.14), bevel=0.018))
    white_armor.append(make_beveled_box((0.22, 0.20, 0.08), center=(center_x, torso_y + 0.02, center_z + 0.155), bevel=0.015))
    # DCM OLED diagnostic display on front chest pack
    oled_parts.append(
        make_quad_panel(
            (center_x - 0.075, torso_y - 0.02, center_z + 0.197),
            (center_x + 0.075, torso_y - 0.02, center_z + 0.197),
            (center_x + 0.075, torso_y + 0.08, center_z + 0.197),
            (center_x - 0.075, torso_y + 0.08, center_z + 0.197),
        )
    )
    # Signal-orange O2 purge valve & emergency chest latch
    orange_accents.append(make_cylinder(0.024, 0.024, 0.03, center=(center_x + 0.06, torso_y - 0.05, center_z + 0.19), segments=10, axis="z"))
    orange_accents.append(make_beveled_box((0.08, 0.028, 0.03), center=(center_x - 0.05, torso_y - 0.05, center_z + 0.19), bevel=0.005))

    # Waist disconnect ring & lower pelvic/thigh pressure brief
    steel_parts.append(make_cylinder(0.19, 0.19, 0.035, center=(center_x, torso_y - 0.20, center_z), segments=18, axis="y"))
    navy_fabric.append(
        make_sculpted_cushion(
            (0.38, 0.22, 0.24),
            center=(center_x, torso_y - 0.31, center_z),
            res=(4, 3, 3),
            roundness=0.36,
            belly_puff=0.04,
            crease_freq=0,
        )
    )

    # Articulated Left & Right Shoulder Joints, Hanging Pressure Sleeves, Wrist Rings & EVA Gauntlets
    for side_s in [-1.0, 1.0]:
        sx = center_x + side_s * 0.27
        # Shoulder joint bell
        white_armor.append(
            transform_geom(
                make_sculpted_cushion((0.15, 0.17, 0.17), res=(4, 3, 3), roundness=0.45, belly_puff=0.05, crease_freq=0),
                translate=(sx, torso_y + 0.18, center_z),
                rot_xyz_deg=(0.0, 0.0, -side_s * 18.0),
            )
        )
        # Swept articulated sleeve (shoulder -> elbow -> wrist)
        arm_pts = sample_filleted_polyline(
            [
                (sx, torso_y + 0.14, center_z),
                (sx + side_s * 0.05, torso_y - 0.06, center_z + 0.04),
                (sx + side_s * 0.02, torso_y - 0.26, center_z + 0.10),
            ],
            fillet_radius=0.07,
            corner_subdivs=5,
        )
        charcoal_fabric.append(make_swept_tube(arm_pts, radius=0.068, radius_end=0.054, radial_segments=10))
        # Machined steel wrist disconnect ring
        wx, wy, wz = sx + side_s * 0.02, torso_y - 0.27, center_z + 0.10
        steel_parts.append(make_cylinder(0.058, 0.058, 0.026, center=(wx, wy, wz), segments=12, axis="y"))
        # Sculpted EVA Gauntlet
        navy_fabric.append(
            make_sculpted_cushion(
                (0.09, 0.13, 0.11),
                center=(wx, wy - 0.07, wz + 0.01),
                res=(4, 4, 4),
                roundness=0.40,
                belly_puff=0.04,
                crease_freq=0,
            )
        )

    # --- 3. 3D LIFE-SUPPORT UMBILICAL HOSES & QUICK-DISCONNECT COUPLINGS ---
    hose_configs = [
        (
            [
                (center_x - 0.34, torso_y + 0.22, center_z - 0.16),
                (center_x - 0.30, torso_y - 0.08, center_z + 0.10),
                (center_x - 0.09, torso_y + 0.01, center_z + 0.18),
            ],
            (center_x - 0.09, torso_y + 0.01, center_z + 0.18),
        ),
        (
            [
                (center_x + 0.34, torso_y + 0.18, center_z - 0.16),
                (center_x + 0.30, torso_y - 0.12, center_z + 0.08),
                (center_x + 0.11, torso_y - 0.14, center_z + 0.16),
            ],
            (center_x + 0.11, torso_y - 0.14, center_z + 0.16),
        ),
    ]
    if num_umbilicals >= 4:
        hose_configs.extend([
            (
                [
                    (center_x - 0.36, torso_y + 0.38, center_z - 0.14),
                    (center_x - 0.26, torso_y + 0.24, center_z + 0.12),
                    (center_x - 0.12, torso_y + 0.15, center_z + 0.17),
                ],
                (center_x - 0.12, torso_y + 0.15, center_z + 0.17),
            ),
            (
                [
                    (center_x + 0.36, torso_y + 0.38, center_z - 0.14),
                    (center_x + 0.26, torso_y + 0.24, center_z + 0.12),
                    (center_x + 0.12, torso_y + 0.15, center_z + 0.17),
                ],
                (center_x + 0.12, torso_y + 0.15, center_z + 0.17),
            ),
        ])

    for h_pts, c_pt in hose_configs:
        curve = sample_filleted_polyline(h_pts, fillet_radius=0.09, corner_subdivs=6)
        charcoal_fabric.append(make_swept_tube(curve, radius=0.020, radial_segments=8))
        orange_accents.append(make_cylinder(0.026, 0.026, 0.035, center=c_pt, segments=10, axis="z"))

    # --- 4. 3D MAGNETIC BOOTS PAIR (Y ~ boot_y to boot_y + 0.30m) ---
    for side_b in [-1.0, 1.0]:
        bx = center_x + side_b * 0.15
        bz = center_z + 0.02
        # Heavy machined-steel magnetic sole plate
        steel_parts.append(make_beveled_box((0.13, 0.036, 0.29), center=(bx, boot_y + 0.018, bz + 0.02), bevel=0.01))
        # Armored white toe cap & heel counter
        white_armor.append(
            make_sculpted_cushion(
                (0.125, 0.095, 0.26),
                center=(bx, boot_y + 0.075, bz + 0.025),
                res=(4, 2, 4),
                roundness=0.38,
                belly_puff=0.04,
                crease_freq=0,
            )
        )
        # Ballistic charcoal calf gaiter
        charcoal_fabric.append(make_cylinder(0.056, 0.064, 0.18, center=(bx, boot_y + 0.19, bz - 0.02), segments=12, axis="y"))
        # Machined steel ankle clamp ring & signal-orange toe lock tab
        steel_parts.append(make_cylinder(0.066, 0.066, 0.028, center=(bx, boot_y + 0.13, bz - 0.02), segments=12, axis="y"))
        orange_accents.append(make_beveled_box((0.06, 0.024, 0.035), center=(bx, boot_y + 0.04, bz + 0.165), bevel=0.005))

    add_part(sm_list, "EVAKit_WhiteHelmetAndTorsoArmor", merge_geometries(white_armor), mats["aero_white"])
    add_part(sm_list, "EVAKit_GoldIridiumBubbleVisor", merge_geometries(gold_visor), mats["gold_visor"])
    add_part(sm_list, "EVAKit_MachinedGantryRingsAndSoles", merge_geometries(steel_parts), mats["steel_gantry"])
    add_part(sm_list, "EVAKit_BallisticCharcoalSleevesAndHoses", merge_geometries(charcoal_fabric), mats["eva_charcoal"])
    add_part(sm_list, "EVAKit_OrbitalNavySuitLayers", merge_geometries(navy_fabric), mats["eva_navy"])
    add_part(sm_list, "EVAKit_SignalOrangeValvesAndCouplings", merge_geometries(orange_accents), mats["accent_orange"])
    add_part(sm_list, "EVAKit_ChestDCM_OLEDReadout", merge_geometries(oled_parts), mats["oled_diag"])


# ==============================================================================
# CANDIDATE 01: PRESSURIZED CYLINDRICAL AIRLOCK SUIT POD (`locker_r1_01.glb`)
# Dimensions: 1.10m W x 0.85m D x 2.15m H
# ==============================================================================
def build_01_cylindrical_airlock_pod(mats):
    sm = []
    # 1. Outer Cylindrical/Stadium Pressure Shell & Top/Bottom Bulkhead Collars
    outer_hull = [
        # Bottom pressure base collar (Y = 0.0 to 0.18)
        make_beveled_box((1.10, 0.18, 0.85), center=(0.0, 0.09, 0.0), bevel=0.04),
        # Top pressure crown cap (Y = 1.93 to 2.15)
        make_beveled_box((1.10, 0.22, 0.85), center=(0.0, 2.04, 0.0), bevel=0.04),
        # Left & right curved/chamfered airlock pillars & rear pressure shell
        make_beveled_box((0.14, 1.78, 0.82), center=(-0.48, 1.06, -0.01), bevel=0.045),
        make_beveled_box((0.14, 1.78, 0.82), center=(0.48, 1.06, -0.01), bevel=0.045),
        make_beveled_box((0.92, 1.78, 0.12), center=(0.0, 1.06, -0.36), bevel=0.03),
    ]
    add_part(sm, "Locker01_CylindricalAirlockHull", merge_geometries(outer_hull), mats["gunmetal"])

    # 2. Inner Concave Aerospace-White Suit Bay Liner
    inner_liner = [
        make_beveled_box((0.82, 1.72, 0.06), center=(0.0, 1.06, -0.28), bevel=0.02),
        make_beveled_box((0.06, 1.72, 0.56), center=(-0.39, 1.06, -0.04), bevel=0.015),
        make_beveled_box((0.06, 1.72, 0.56), center=(0.39, 1.06, -0.04), bevel=0.015),
    ]
    add_part(sm, "Locker01_WhiteConcaveBayLiner", merge_geometries(inner_liner), mats["aero_white"])

    # 3. Rotary Ceiling Carousel Gantry, Door Track Bezels & Circular Boot Charging Deck
    gantry_and_tracks = [
        make_cylinder(0.32, 0.32, 0.05, center=(0.0, 1.90, -0.04), segments=20, axis="y"),
        make_cylinder(0.36, 0.36, 0.04, center=(0.0, 0.19, -0.02), segments=20, axis="y"),
        make_chamfered_aperture_ring(0.98, 1.80, center_y=1.06, z_pos=0.38, tube_r=0.036, chamfer=0.18),
        # Vertical brushed-steel inner sealing edges of the parted sliding doors at X = -0.12 and +0.12
        make_beveled_box((0.028, 1.68, 0.035), center=(-0.13, 1.06, 0.40), bevel=0.006),
        make_beveled_box((0.028, 1.68, 0.035), center=(0.13, 1.06, 0.40), bevel=0.006),
    ]
    add_part(sm, "Locker01_RotaryGantryAndTracks", merge_geometries(gantry_and_tracks), mats["steel_gantry"])

    # 4. Mandatory 4-Part 3D Interior EVA Gear Kit
    add_eva_suit_interior_kit(sm, mats, center_x=0.0, center_z=-0.04, helmet_y=1.54, torso_y=1.10, boot_y=0.21, num_umbilicals=2)

    # 5. Signal-Orange Manual Airlock Override Latch Bar + Side OLED Status Panel
    add_part(
        sm,
        "Locker01_SignalOrangeAirlockLatch",
        make_beveled_box((0.05, 0.26, 0.04), center=(-0.16, 1.08, 0.42), bevel=0.008),
        mats["accent_orange"],
    )
    add_part(
        sm,
        "Locker01_SideOLEDStatus",
        make_quad_panel((0.39, 1.15, 0.425), (0.52, 1.15, 0.425), (0.52, 1.45, 0.425), (0.39, 1.45, 0.425)),
        mats["oled_diag"],
    )

    # 6. Dual Vertical Cyan Light Pillars + Warm Amber Boot Ring
    cyan_pillars = [
        make_beveled_box((0.028, 1.62, 0.035), center=(-0.36, 1.06, 0.22), bevel=0.005),
        make_beveled_box((0.028, 1.62, 0.035), center=(0.36, 1.06, 0.22), bevel=0.005),
        make_beveled_box((0.68, 0.026, 0.05), center=(0.0, 1.88, 0.14), bevel=0.005),
    ]
    add_part(sm, "Locker01_CyanLightPillars", merge_geometries(cyan_pillars), mats["led_cyan"])
    add_part(
        sm,
        "Locker01_AmberBootHalo",
        make_beveled_box((0.68, 0.024, 0.04), center=(0.0, 0.20, 0.34), bevel=0.004),
        mats["led_amber"],
    )

    # 7. Twin Curved Translucent Armored-Glass Sliding Doors Parted Open by 0.24m in Center (alphaMode: "BLEND")
    doors = [
        # Left sliding door wing (X = -0.44 to -0.12)
        make_quad_panel((-0.44, 0.22, 0.37), (-0.12, 0.22, 0.40), (-0.12, 1.90, 0.40), (-0.44, 1.90, 0.37)),
        # Right sliding door wing (X = +0.12 to +0.44)
        make_quad_panel((0.12, 0.22, 0.40), (0.44, 0.22, 0.37), (0.44, 1.90, 0.37), (0.12, 1.90, 0.40)),
    ]
    add_part(sm, "Locker01_PartedTranslucentGlassDoors", merge_geometries(doors), mats["glass_suitbay"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "locker_r1_01.glb"), sm, root_name="LockerR1_01_CylindricalAirlockPod")


# ==============================================================================
# CANDIDATE 02: DUAL-BAY RECESSED BULKHEAD SUIT & KIT LOCKER (`locker_r1_02.glb`)
# Dimensions: 1.35m W x 0.75m D x 2.10m H
# ==============================================================================
def build_02_dual_bay_bulkhead_locker(mats):
    sm = []
    # 1. Outer Asymmetric Split-Bay Bulkhead Frame (Left Bay: X=-0.675..+0.175, Right Bay: X=+0.175..+0.675)
    cabinet_frame = [
        make_beveled_box((1.35, 0.16, 0.75), center=(0.0, 0.08, 0.0), bevel=0.03),
        make_beveled_box((1.35, 0.16, 0.75), center=(0.0, 2.02, 0.0), bevel=0.03),
        make_beveled_box((0.10, 1.94, 0.74), center=(-0.625, 1.05, 0.0), bevel=0.03),
        make_beveled_box((0.10, 1.94, 0.74), center=(0.625, 1.05, 0.0), bevel=0.03),
        # Center vertical structural partition at X = +0.175
        make_beveled_box((0.08, 1.82, 0.70), center=(0.175, 1.05, -0.01), bevel=0.02),
        make_beveled_box((1.25, 1.84, 0.08), center=(0.0, 1.05, -0.33), bevel=0.02),
        # Right Bay 3-tier shelves at Y = 0.80 and Y = 1.42
        make_beveled_box((0.44, 0.04, 0.64), center=(0.40, 0.80, -0.02), bevel=0.01),
        make_beveled_box((0.44, 0.04, 0.64), center=(0.40, 1.42, -0.02), bevel=0.01),
    ]
    add_part(sm, "Locker02_SplitBayGunmetalCabinet", merge_geometries(cabinet_frame), mats["gunmetal"])

    # 2. Left Suit Bay White Backplate & Spare O2 Tank Bodies in Right Bay
    white_parts = [
        make_beveled_box((0.72, 1.72, 0.04), center=(-0.225, 1.05, -0.27), bevel=0.015),
        # Twin vertical spare O2/N2 cylinders in bottom-right compartment (Y = 0.18..0.72)
        make_cylinder(0.068, 0.068, 0.46, center=(0.31, 0.42, -0.02), segments=14, axis="y"),
        make_cylinder(0.068, 0.068, 0.46, center=(0.49, 0.42, -0.02), segments=14, axis="y"),
    ]
    add_part(sm, "Locker02_WhiteBayLinerAndO2Tanks", merge_geometries(white_parts), mats["aero_white"])

    # 3. Machined-Steel Left Door Bezel, Shelf Lips & O2 Tank Retaining Bar
    steel_trim = [
        make_chamfered_aperture_ring(0.78, 1.78, center_y=1.05, z_pos=0.34, tube_r=0.032, chamfer=0.14),
        make_beveled_box((0.42, 0.028, 0.03), center=(0.40, 0.42, 0.28), bevel=0.005),
        make_beveled_box((0.42, 0.028, 0.03), center=(0.40, 0.82, 0.30), bevel=0.005),
        make_beveled_box((0.42, 0.028, 0.03), center=(0.40, 1.44, 0.30), bevel=0.005),
    ]
    for elem in steel_trim[0:1]:
        # Shift aperture ring to center of Left Suit Bay (X = -0.225)
        elem[0][:, 0] -= 0.225
    add_part(sm, "Locker02_MachinedSteelFrameAndLips", merge_geometries(steel_trim), mats["steel_gantry"])

    # 4. Mandatory 4-Part 3D Interior EVA Suit Kit inside Left Bay (centered at X = -0.225)
    add_eva_suit_interior_kit(sm, mats, center_x=-0.225, center_z=-0.03, helmet_y=1.52, torso_y=1.08, boot_y=0.18, num_umbilicals=2)

    # 5. Right Bay Kit Items: Middle-Tier Sculpted Orbital-Navy Flight Bag, Top OLED Monitor & Signal-Orange Valves/Straps
    flight_bag = [
        make_sculpted_cushion(
            (0.34, 0.36, 0.32),
            center=(0.40, 1.04, 0.02),
            res=(6, 5, 5),
            roundness=0.35,
            belly_puff=0.06,
            pinch_corners=0.08,
            crease_freq=4,
        ),
    ]
    add_part(sm, "Locker02_StowedOrbitalNavyFlightBag", merge_geometries(flight_bag), mats["eva_navy"])

    orange_kit = [
        # Retention strap across flight bag
        make_beveled_box((0.36, 0.04, 0.34), center=(0.40, 1.04, 0.03), bevel=0.008),
        # O2 cylinder valve necks
        make_cylinder(0.035, 0.045, 0.08, center=(0.31, 0.68, -0.02), segments=10, axis="y"),
        make_cylinder(0.035, 0.045, 0.08, center=(0.49, 0.68, -0.02), segments=10, axis="y"),
    ]
    add_part(sm, "Locker02_SignalOrangeStrapsAndValves", merge_geometries(orange_kit), mats["accent_orange"])

    add_part(
        sm,
        "Locker02_RightBayOLEDTelemetry",
        make_quad_panel((0.23, 1.50, 0.08), (0.56, 1.50, 0.08), (0.56, 1.84, 0.02), (0.23, 1.84, 0.02)),
        mats["oled_diag"],
    )

    # 6. Left Bay Ice-Cyan LED Strips + Right Kit Bay Warm Amber Shelf Strips
    cyan_leds = [
        make_beveled_box((0.68, 0.026, 0.05), center=(-0.225, 1.88, 0.14), bevel=0.005),
        make_beveled_box((0.026, 1.62, 0.04), center=(-0.55, 1.05, 0.20), bevel=0.004),
        make_beveled_box((0.026, 1.62, 0.04), center=(0.10, 1.05, 0.20), bevel=0.004),
    ]
    add_part(sm, "Locker02_LeftBayCyanLED", merge_geometries(cyan_leds), mats["led_cyan"])

    amber_leds = [
        make_beveled_box((0.38, 0.022, 0.04), center=(0.40, 1.90, 0.18), bevel=0.004),
        make_beveled_box((0.38, 0.022, 0.04), center=(0.40, 1.38, 0.18), bevel=0.004),
        make_beveled_box((0.38, 0.022, 0.04), center=(0.40, 0.76, 0.18), bevel=0.004),
    ]
    add_part(sm, "Locker02_RightBayAmberShelfLED", merge_geometries(amber_leds), mats["led_amber"])

    # 7. Left Suit Bay Full-Height Single-Pane Translucent Glass Door (alphaMode: "BLEND")
    add_part(
        sm,
        "Locker02_LeftBayTranslucentGlassDoor",
        make_quad_panel((-0.58, 0.20, 0.35), (0.13, 0.20, 0.35), (0.13, 1.90, 0.35), (-0.58, 1.90, 0.35)),
        mats["glass_suitbay"],
    )

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "locker_r1_02.glb"), sm, root_name="LockerR1_02_DualBayBulkheadLocker")


# ==============================================================================
# CANDIDATE 03: HEX-FRAME EXOSUIT GANTRY & MAG-BOOT ALCOVE (`locker_r1_03.glb`)
# Dimensions: 1.20m W x 0.80m D x 2.15m H
# ==============================================================================
def build_03_hex_gantry_alcove(mats):
    sm = []
    # 1. Industrial Elongated Hexagonal Chamfered Alcove Hull (Carbon Slate & Gunmetal)
    hex_hull = [
        # Stepped magnetic boot-clamping platform (Y = 0.0 to 0.24)
        make_beveled_box((1.20, 0.16, 0.80), center=(0.0, 0.08, 0.0), bevel=0.03),
        make_beveled_box((0.96, 0.08, 0.72), center=(0.0, 0.20, 0.02), bevel=0.02),
        # Upper hex crown
        make_beveled_box((1.20, 0.18, 0.78), center=(0.0, 2.06, 0.0), bevel=0.035),
        # Side walls & rear plate
        make_beveled_box((0.14, 1.82, 0.74), center=(-0.53, 1.07, -0.01), bevel=0.035),
        make_beveled_box((0.14, 1.82, 0.74), center=(0.53, 1.07, -0.01), bevel=0.035),
        make_beveled_box((1.04, 1.84, 0.08), center=(0.0, 1.07, -0.35), bevel=0.02),
        # Hexagonal manifold blocks on left & right inner walls
        make_beveled_box((0.08, 0.36, 0.22), center=(-0.42, 1.18, -0.10), bevel=0.02),
        make_beveled_box((0.08, 0.36, 0.22), center=(0.42, 1.18, -0.10), bevel=0.02),
    ]
    add_part(sm, "Locker03_HexagonalCarbonAlcove", merge_geometries(hex_hull), mats["carbon_slate"])

    # 2. Inner White Hex Backplate
    add_part(
        sm,
        "Locker03_WhiteInnerHexBackplate",
        make_beveled_box((0.84, 1.68, 0.04), center=(0.0, 1.08, -0.29), bevel=0.015),
        mats["aero_white"],
    )

    # 3. Beefy Articulated Machined-Steel Overhead Cantilever Gantry Crane Arm & Hex Aperture Ring
    crane_l = sample_filleted_polyline([(-0.18, 1.88, -0.26), (-0.18, 1.88, 0.16), (-0.18, 1.50, 0.02)], 0.08, 5)
    crane_r = sample_filleted_polyline([(0.18, 1.88, -0.26), (0.18, 1.88, 0.16), (0.18, 1.50, 0.02)], 0.08, 5)
    gantry_parts = [
        make_chamfered_aperture_ring(1.08, 1.82, center_y=1.08, z_pos=0.35, tube_r=0.042, chamfer=0.28),
        make_swept_tube(crane_l, radius=0.028, radial_segments=10, oval_scale=(0.8, 1.4)),
        make_swept_tube(crane_r, radius=0.028, radial_segments=10, oval_scale=(0.8, 1.4)),
        make_beveled_box((0.52, 0.05, 0.12), center=(0.0, 1.88, 0.12), bevel=0.012),
    ]
    add_part(sm, "Locker03_CantileverGantryCrane", merge_geometries(gantry_parts), mats["steel_gantry"])

    # 4. Mandatory 4-Part 3D Interior EVA Suit Kit (with 4 sweeping umbilical hoses!)
    add_eva_suit_interior_kit(sm, mats, center_x=0.0, center_z=-0.02, helmet_y=1.55, torso_y=1.11, boot_y=0.24, num_umbilicals=4)

    # 5. Stepped Mag-Boot Mechanical Toe/Heel Clamp Bars in Signal Orange + Gantry OLED
    boot_clamps = [
        make_beveled_box((0.18, 0.035, 0.05), center=(-0.15, 0.25, 0.22), bevel=0.008),
        make_beveled_box((0.18, 0.035, 0.05), center=(0.15, 0.25, 0.22), bevel=0.008),
        make_beveled_box((0.46, 0.035, 0.04), center=(0.0, 1.88, 0.19), bevel=0.008),
    ]
    add_part(sm, "Locker03_SignalOrangeBootAndGantryLocks", merge_geometries(boot_clamps), mats["accent_orange"])

    # 6. Continuous Hex Perimeter Cyan Cove Strips + Ice-White Gantry Spot + Boot Clamp Amber LED
    cyan_coves = [
        make_beveled_box((0.028, 1.52, 0.04), center=(-0.44, 1.08, 0.22), bevel=0.005),
        make_beveled_box((0.028, 1.52, 0.04), center=(0.44, 1.08, 0.22), bevel=0.005),
        make_beveled_box((0.76, 0.028, 0.05), center=(0.0, 1.92, 0.22), bevel=0.005),
    ]
    add_part(sm, "Locker03_HexPerimeterCyanLED", merge_geometries(cyan_coves), mats["led_cyan"])
    add_part(sm, "Locker03_BootDeckAmberLED", make_beveled_box((0.78, 0.022, 0.04), center=(0.0, 0.17, 0.38), bevel=0.004), mats["led_amber"])

    # 7. Twin Faceted Hex-Cut Translucent Shield Doors (alphaMode: "BLEND")
    hex_doors = [
        make_quad_panel((-0.48, 0.24, 0.35), (-0.04, 0.24, 0.37), (-0.04, 1.92, 0.37), (-0.48, 1.92, 0.35)),
        make_quad_panel((0.04, 0.24, 0.37), (0.48, 0.24, 0.35), (0.48, 1.92, 0.35), (0.04, 1.92, 0.37)),
    ]
    add_part(sm, "Locker03_FacetedHexTranslucentDoors", merge_geometries(hex_doors), mats["glass_suitbay"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "locker_r1_03.glb"), sm, root_name="LockerR1_03_HexGantryAlcove")


# ==============================================================================
# CANDIDATE 04: SLEEK AEROSPACE CAPSULE WARDROBE & UV STERILIZER (`locker_r1_04.glb`)
# Dimensions: 1.15m W x 0.75m D x 2.12m H
# ==============================================================================
def build_04_aerospace_uv_wardrobe(mats):
    sm = []
    # 1. Recessed Dark Gunmetal Titanium Base Plinth
    plinth = [
        make_beveled_box((1.12, 0.16, 0.74), center=(0.0, 0.08, 0.0), bevel=0.035),
    ]
    add_part(sm, "Locker04_GunmetalBasePlinth", merge_geometries(plinth), mats["gunmetal"])

    # 2. Smooth Stadium-Filleted Matte Aerospace White Monocoque Capsule Shell
    capsule_shell = [
        make_sculpted_cushion((1.15, 0.20, 0.75), center=(0.0, 2.02, 0.0), res=(7, 3, 5), roundness=0.28, belly_puff=0.02, pinch_corners=0.0, crease_freq=0),
        make_beveled_box((0.14, 1.82, 0.73), center=(-0.505, 1.05, 0.0), bevel=0.05),
        make_beveled_box((0.14, 1.82, 0.73), center=(0.505, 1.05, 0.0), bevel=0.05),
        make_beveled_box((1.02, 1.84, 0.08), center=(0.0, 1.05, -0.33), bevel=0.025),
    ]
    add_part(sm, "Locker04_AerospaceWhiteCapsuleShell", merge_geometries(capsule_shell), mats["aero_white"])

    # 3. Stadium Door Collar, Top Circular Helmet Pedestal Shelf & Bottom Pull-Out Boot Sterilizer Tray
    steel_fixtures = [
        make_chamfered_aperture_ring(0.98, 1.80, center_y=1.06, z_pos=0.34, tube_r=0.035, chamfer=0.24),
        # Top helmet display pedestal ring at Y = 1.50
        make_cylinder(0.24, 0.24, 0.025, center=(0.0, 1.50, -0.02), segments=20, axis="y"),
        # Bottom pull-out machined steel boot sterilizer tray at Y = 0.18
        make_beveled_box((0.78, 0.04, 0.56), center=(0.0, 0.18, 0.02), bevel=0.012),
    ]
    add_part(sm, "Locker04_MachinedBezelAndBootTray", merge_geometries(steel_fixtures), mats["steel_gantry"])

    # 4. Mandatory 4-Part 3D Interior EVA Suit Kit
    add_eva_suit_interior_kit(sm, mats, center_x=0.0, center_z=-0.03, helmet_y=1.53, torso_y=1.05, boot_y=0.20, num_umbilicals=2)

    # 5. Four Vertical Glowing Ultraviolet (#7B5CFF) Emitter Tubes + Top Helmet Cyan Spot + Right Bezel Bio-Decon OLED
    uv_tubes = [
        make_cylinder(0.018, 0.018, 1.24, center=(-0.38, 0.96, 0.14), segments=10, axis="y"),
        make_cylinder(0.018, 0.018, 1.24, center=(-0.38, 0.96, -0.18), segments=10, axis="y"),
        make_cylinder(0.018, 0.018, 1.24, center=(0.38, 0.96, 0.14), segments=10, axis="y"),
        make_cylinder(0.018, 0.018, 1.24, center=(0.38, 0.96, -0.18), segments=10, axis="y"),
    ]
    add_part(sm, "Locker04_UVSterilizerEmitterTubes", merge_geometries(uv_tubes), mats["led_uv"])
    add_part(sm, "Locker04_HelmetNicheCyanRing", make_beveled_box((0.64, 0.025, 0.05), center=(0.0, 1.88, 0.12), bevel=0.005), mats["led_cyan"])
    add_part(
        sm,
        "Locker04_BioDeconOLEDReadout",
        make_quad_panel((0.43, 1.10, 0.372), (0.56, 1.10, 0.372), (0.56, 1.44, 0.372), (0.43, 1.44, 0.372)),
        mats["oled_diag"],
    )

    # 6. Full-Height Stadium-Curved Violet-Tinted Translucent UV Quartz Door (alphaMode: "BLEND")
    add_part(
        sm,
        "Locker04_VioletUVQuartzTranslucentDoor",
        make_quad_panel((-0.44, 0.20, 0.35), (0.44, 0.20, 0.35), (0.44, 1.90, 0.35), (-0.44, 1.90, 0.35)),
        mats["glass_uv_violet"],
    )

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "locker_r1_04.glb"), sm, root_name="LockerR1_04_AerospaceUVWardrobe")


# ==============================================================================
# CANDIDATE 05: CORNER-MOUNT ANGLED TACTICAL EVA PREP STATION (`locker_r1_05.glb`)
# Dimensions: 1.25m W x 0.85m D x 2.15m H
# ==============================================================================
def build_05_corner_tactical_prep_station(mats):
    sm = []
    # 1. Chamfered Wedge / Corner-Mount Gunmetal Chassis with Two 35-Degree Canted Side Utility Wings
    wedge_chassis = [
        make_beveled_box((1.25, 0.18, 0.85), center=(0.0, 0.09, 0.0), bevel=0.035),
        make_beveled_box((1.25, 0.18, 0.85), center=(0.0, 2.06, 0.0), bevel=0.035),
        make_beveled_box((0.92, 1.84, 0.08), center=(0.0, 1.07, -0.38), bevel=0.02),
        # Left 35°-angled utility wing housing
        transform_geom(
            make_beveled_box((0.26, 1.80, 0.62), center=(0.0, 0.0, 0.0), bevel=0.025),
            translate=(-0.44, 1.07, -0.02),
            rot_xyz_deg=(0.0, 28.0, 0.0),
        ),
        # Right 35°-angled utility wing housing (with recessed bay for 3 O2/N2 bottles)
        transform_geom(
            make_beveled_box((0.18, 1.80, 0.56), center=(0.0, 0.0, 0.0), bevel=0.025),
            translate=(0.45, 1.07, -0.06),
            rot_xyz_deg=(0.0, -28.0, 0.0),
        ),
    ]
    add_part(sm, "Locker05_AngledWedgeGunmetalChassis", merge_geometries(wedge_chassis), mats["gunmetal"])

    # 2. Center Suit Bay White Backwall + 3 Cylindrical High-Pressure O2/N2 Bottles on Right Wing
    white_and_tanks = [
        make_beveled_box((0.72, 1.72, 0.04), center=(0.0, 1.07, -0.32), bevel=0.015),
    ]
    for ty in [0.54, 1.06, 1.58]:
        white_and_tanks.append(make_cylinder(0.056, 0.056, 0.40, center=(0.46, ty, 0.14), segments=12, axis="y"))
    add_part(sm, "Locker05_WhiteLinerAndO2Bottles", merge_geometries(white_and_tanks), mats["aero_white"])

    # 3. Signal-Orange O2 Bottle Valve Necks & Regulator Dials
    orange_valves = []
    for ty in [0.54, 1.06, 1.58]:
        orange_valves.append(make_cylinder(0.032, 0.042, 0.07, center=(0.46, ty + 0.22, 0.14), segments=10, axis="y"))
    add_part(sm, "Locker05_SignalOrangeTankValves", merge_geometries(orange_valves), mats["accent_orange"])

    # 4. Machined-Steel Center Bezel, Raised Boot Deck Grate & Tank Retention Clamps
    steel_parts = [
        make_chamfered_aperture_ring(0.78, 1.78, center_y=1.07, z_pos=0.38, tube_r=0.034, chamfer=0.16),
        make_beveled_box((0.70, 0.04, 0.58), center=(0.0, 0.19, 0.0), bevel=0.012),
    ]
    for ty in [0.54, 1.06, 1.58]:
        steel_parts.append(make_beveled_box((0.14, 0.03, 0.14), center=(0.46, ty, 0.16), bevel=0.006))
    add_part(sm, "Locker05_MachinedBezelAndTankClamps", merge_geometries(steel_parts), mats["steel_gantry"])

    # 5. Mandatory 4-Part 3D Interior EVA Suit Kit in Center Bay
    add_eva_suit_interior_kit(sm, mats, center_x=0.0, center_z=-0.04, helmet_y=1.54, torso_y=1.10, boot_y=0.21, num_umbilicals=2)

    # 6. Left Angled Wing Flush-Mounted OLED Diagnostics Terminal
    oled_wing = transform_geom(
        make_quad_panel((-0.11, -0.32, 0.0), (0.11, -0.32, 0.0), (0.11, 0.32, 0.0), (-0.11, 0.32, 0.0)),
        translate=(-0.44, 1.24, 0.28),
        rot_xyz_deg=(0.0, 28.0, 0.0),
    )
    add_part(sm, "Locker05_LeftWingOLEDTerminal", oled_wing, mats["oled_diag"])

    # 7. Tactical Amber Interior Backlight Strips + Cool Cyan Front Rim
    amber_strips = [
        make_beveled_box((0.028, 1.62, 0.04), center=(-0.33, 1.07, -0.24), bevel=0.005),
        make_beveled_box((0.028, 1.62, 0.04), center=(0.33, 1.07, -0.24), bevel=0.005),
    ]
    add_part(sm, "Locker05_TacticalAmberBacklightLED", merge_geometries(amber_strips), mats["led_amber"])
    add_part(sm, "Locker05_FrontFrameCyanRimLED", make_beveled_box((0.68, 0.026, 0.05), center=(0.0, 1.90, 0.22), bevel=0.005), mats["led_cyan"])

    # 8. Center Bay Panoramic Translucent Armored Glass Door (alphaMode: "BLEND")
    add_part(
        sm,
        "Locker05_CenterTranslucentGlassDoor",
        make_quad_panel((-0.36, 0.20, 0.39), (0.36, 0.20, 0.39), (0.36, 1.92, 0.39), (-0.36, 1.92, 0.39)),
        mats["glass_suitbay"],
    )

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "locker_r1_05.glb"), sm, root_name="LockerR1_05_CornerTacticalPrepStation")


def build_all_locker_round1():
    mats = get_locker_materials()
    builders = [
        build_01_cylindrical_airlock_pod,
        build_02_dual_bay_bulkhead_locker,
        build_03_hex_gantry_alcove,
        build_04_aerospace_uv_wardrobe,
        build_05_corner_tactical_prep_station,
    ]
    results = []
    for fn in builders:
        info = fn(mats)
        fname = os.path.basename(info["filepath"])
        dims = info["dimensions"]
        print(
            f"[locker_r1] Built {fname:16s} | {dims[0]:.2f}m W x {dims[2]:.2f}m D x {dims[1]:.2f}m H | "
            f"verts={info['vertices']:4d} | tris={info['triangles']:4d} | min_y={info['min'][1]:.5f}"
        )
        results.append(info)
    with open(os.path.join(OUT_GLB_DIR, "locker_r1_manifest.json"), "w") as f:
        json.dump(results, f, indent=2)
    return results


if __name__ == "__main__":
    build_all_locker_round1()
