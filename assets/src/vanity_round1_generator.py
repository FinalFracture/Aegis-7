#!/usr/bin/env python3
"""
Builds all 5 Round-1 Hard Sci-Fi Compact Hygiene & Sonic Wash Vanity .glb models:
/workspace/game-project/assets/glb/vanity_round1/vanity_r1_01.glb .. vanity_r1_05.glb

Follows /workspace/game-project/design/vanity_round1/vanity_r1_spec.md ("Aegis-7 Standard"):
- Bottom-center (0.0, 0.0, 0.0) floor pivot (min_y == 0.0000, centered X and Z), front facing +Z
- Polygon budget: 3,000 - 5,500 triangles per candidate
- Mapped cleanly to Sloane's 10 textures in /workspace/game-project/assets/textures/vanity_round1/
- Mandatory 4-Part 3D Hygiene & Reclamation Kit inside every candidate:
  1. Contoured 3D Zero-Splash Washbasin & 42 kHz Sonic-Mist Emitter Faucet Arch + Cyan Atomizer Rim
  2. Backlit Smart-Mirror HUD (mirror_smart_hud_cyan.png) framed by surgical ice-white & cyan light bars
  3. UV-C Towel & Personal Grooming Sterilizer Cubby behind translucent alphaMode: "BLEND" glass
     (3D rolled/folded orbital-navy towels, sonic dental/grooming wands, dermal dispensers, UV-violet emitter)
  4. Lower Greywater Filtration & H2O Reclamation Manifold (twin cylindrical filter canisters,
     bent 3D swept metallic syphon/manifold pipes, and signal-orange emergency shutoff/purge valve)
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

TEX_VANITY_DIR = "/workspace/game-project/assets/textures/vanity_round1"
OUT_GLB_DIR = "/workspace/game-project/assets/glb/vanity_round1"
os.makedirs(OUT_GLB_DIR, exist_ok=True)


def tex_vn(fname: str) -> str:
    return os.path.join(TEX_VANITY_DIR, fname)


def get_vanity_materials():
    return {
        "gunmetal": PBRMaterialDef(
            name="Mat_Titanium_GunmetalHull",
            base_color=hex_rgba("#1A1E24"),
            metallic=0.78,
            roughness=0.34,
            texture_path=tex_vn("titanium_gunmetal_hull.png"),
        ),
        "aero_white": PBRMaterialDef(
            name="Mat_Composite_AerospaceWhite",
            base_color=hex_rgba("#D8DEE6"),
            metallic=0.08,
            roughness=0.26,
            texture_path=tex_vn("composite_aerospace_white.png"),
        ),
        "carbon_slate": PBRMaterialDef(
            name="Mat_Carbon_SlateFrame",
            base_color=hex_rgba("#282E38"),
            metallic=0.58,
            roughness=0.40,
            texture_path=tex_vn("carbon_slate_frame.png"),
        ),
        "steel_machined": PBRMaterialDef(
            name="Mat_Steel_MachinedGantry",
            base_color=hex_rgba("#88929E"),
            metallic=0.90,
            roughness=0.20,
            texture_path=tex_vn("steel_machined_gantry.png"),
        ),
        "navy_towel": PBRMaterialDef(
            name="Mat_Fabric_OrbitalNavyTowel",
            base_color=hex_rgba("#1D2C3C"),
            metallic=0.0,
            roughness=0.78,
            texture_path=tex_vn("fabric_orbital_navy_towel.png"),
        ),
        "accent_orange": PBRMaterialDef(
            name="Mat_Accent_SignalOrange",
            base_color=hex_rgba("#D95B26"),
            metallic=0.06,
            roughness=0.48,
            texture_path=tex_vn("accent_signal_orange.png"),
        ),
        "smart_mirror": PBRMaterialDef(
            name="Mat_Mirror_SmartHUDCyan",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.92,
            roughness=0.06,
            emissive=(0.06, 0.28, 0.38),
            texture_path=tex_vn("mirror_smart_hud_cyan.png"),
        ),
        "glass_sonic": PBRMaterialDef(
            name="Mat_Glass_SonicShield_Translucent",
            base_color=(0.55, 0.85, 1.0, 0.18),
            metallic=0.10,
            roughness=0.08,
            emissive=(0.0, 0.10, 0.16),
            texture_path=tex_vn("glass_sonic_shield_translucent.png"),
            double_sided=True,
            alpha_mode="BLEND",
        ),
        "glass_uv": PBRMaterialDef(
            name="Mat_Glass_UVCubby_Translucent",
            base_color=(0.68, 0.56, 1.0, 0.19),
            metallic=0.10,
            roughness=0.08,
            emissive=(0.12, 0.08, 0.24),
            texture_path=tex_vn("glass_uv_cubby_violet.png"),
            double_sided=True,
            alpha_mode="BLEND",
        ),
        "oled_hygiene": PBRMaterialDef(
            name="Mat_OLED_HygienePanel",
            base_color=hex_rgba("#0A0E14"),
            metallic=0.10,
            roughness=0.15,
            emissive=(0.22, 0.82, 1.0),
            texture_path=tex_vn("oled_hygiene_panel.png"),
        ),
        "led_cyan": PBRMaterialDef(
            name="Mat_Emissive_CyanLED",
            base_color=hex_rgba("#00E5FF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.0, 0.90, 1.0),
        ),
        "led_ice": PBRMaterialDef(
            name="Mat_Emissive_IceWhiteLED",
            base_color=hex_rgba("#E0F4FF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.86, 0.95, 1.0),
        ),
        "led_uv": PBRMaterialDef(
            name="Mat_Emissive_UVSterilizerLED",
            base_color=hex_rgba("#7B5CFF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.55, 0.38, 1.0),
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
# SHARED 4-PART 3D HYGIENE & RECLAMATION KIT HELPERS
# ==============================================================================
def make_concave_basin_and_faucet(
    center_x: float = 0.0,
    deck_y: float = 0.86,
    center_z: float = 0.04,
    scale_xz: tuple = (1.15, 0.85),
    halo_faucet: bool = False,
):
    """
    Builds Part 1 of the Mandatory Kit:
    - Lathed concave zero-splash washbasin bowl with rolled rim
    - Machined-steel drain ring & 42 kHz Sonic-Mist Faucet Arch
    - Glowing Cyan ultrasonic atomizer rim ring
    Returns: (basin_white_geom, steel_faucet_and_drain_geom, cyan_atomizer_ring_geom)
    """
    # Concave double-walled basin profile (outer wall + inner concave bowl)
    basin_profile = [
        (0.00, -0.13),
        (0.11, -0.13),
        (0.18, -0.08),
        (0.21, 0.00),
        (0.21, 0.025),
        (0.17, 0.025),
        (0.14, -0.07),
        (0.06, -0.105),
        (0.00, -0.105),
    ]
    bowl = transform_geom(
        make_lathe_dome(basin_profile, center=(0.0, 0.0, 0.0), segments=24, subdivide_profile=2),
        translate=(center_x, deck_y, center_z),
        scale=(scale_xz[0], 1.0, scale_xz[1]),
    )

    # Stainless drain ring + Sonic-Mist Faucet Arch
    steel_parts = [
        make_cylinder(0.042, 0.036, 0.016, center=(center_x, deck_y - 0.10, center_z), segments=16, axis="y"),
    ]
    if halo_faucet:
        stem = sample_filleted_polyline(
            [(center_x, deck_y, center_z - 0.14), (center_x, deck_y + 0.16, center_z - 0.12), (center_x, deck_y + 0.18, center_z - 0.02)],
            fillet_radius=0.05,
            corner_subdivs=5,
        )
        steel_parts.append(make_swept_tube(stem, radius=0.016, radial_segments=10))
        halo_pts = []
        for k in range(17):
            ang = (k / 16.0) * 2.0 * math.pi
            halo_pts.append([center_x + 0.085 * math.cos(ang), deck_y + 0.17, center_z + 0.085 * math.sin(ang)])
        steel_parts.append(make_swept_tube(np.array(halo_pts, dtype=np.float32), radius=0.012, radial_segments=8, closed_loop=True))
    else:
        faucet_pts = sample_filleted_polyline(
            [
                (center_x, deck_y, center_z - 0.15),
                (center_x, deck_y + 0.20, center_z - 0.14),
                (center_x, deck_y + 0.21, center_z + 0.02),
                (center_x, deck_y + 0.15, center_z + 0.04),
            ],
            fillet_radius=0.06,
            corner_subdivs=6,
        )
        steel_parts.append(make_swept_tube(faucet_pts, radius=0.016, radius_end=0.013, radial_segments=12))

    # Glowing cyan ultrasonic atomizer ring around inner basin lip
    ring_pts = []
    for k in range(21):
        ang = (k / 20.0) * 2.0 * math.pi
        ring_pts.append([
            center_x + 0.175 * scale_xz[0] * math.cos(ang),
            deck_y + 0.018,
            center_z + 0.175 * scale_xz[1] * math.sin(ang),
        ])
    cyan_ring = make_swept_tube(np.array(ring_pts, dtype=np.float32), radius=0.008, radial_segments=8, closed_loop=True)

    return bowl, merge_geometries(steel_parts), cyan_ring


def make_uv_towel_and_grooming_kit(
    cubby_x: float,
    cubby_y: float,
    cubby_z: float,
):
    """
    Builds Part 3 interior items:
    - 2 stacked folded orbital-navy microfiber towels + 2 cylindrical rolled hand towels
    - 3 cylindrical sonic dental/grooming wands in a machined dock + pressurized dermal dispenser
    - Vertical UV-violet (#7B5CFF) sterilizer emitter tube
    Returns: (navy_towels_geom, white_dispensers_geom, steel_holders_geom, orange_caps_geom, uv_tube_geom)
    """
    towels = [
        # Folded microfiber towel stack
        make_sculpted_cushion((0.18, 0.042, 0.16), center=(cubby_x, cubby_y + 0.022, cubby_z), res=(5, 3, 4), roundness=0.35, belly_puff=0.04, crease_freq=4),
        make_sculpted_cushion((0.17, 0.040, 0.15), center=(cubby_x, cubby_y + 0.064, cubby_z), res=(5, 3, 4), roundness=0.35, belly_puff=0.04, crease_freq=4),
        # 2 rolled cylindrical hand towels above/beside
        make_cylinder(0.032, 0.032, 0.16, center=(cubby_x - 0.045, cubby_y + 0.115, cubby_z + 0.01), segments=12, axis="z"),
        make_cylinder(0.032, 0.032, 0.16, center=(cubby_x + 0.045, cubby_y + 0.115, cubby_z + 0.01), segments=12, axis="z"),
    ]

    # Upper shelf sonic grooming wands & dermal dispenser
    wy = cubby_y + 0.26
    white_wands = [
        make_cylinder(0.012, 0.009, 0.14, center=(cubby_x - 0.055, wy + 0.07, cubby_z + 0.01), segments=10, axis="y"),
        make_cylinder(0.012, 0.009, 0.13, center=(cubby_x - 0.015, wy + 0.065, cubby_z + 0.01), segments=10, axis="y"),
        make_cylinder(0.028, 0.028, 0.13, center=(cubby_x + 0.045, wy + 0.065, cubby_z + 0.01), segments=12, axis="y"),
    ]
    steel_dock = [
        make_beveled_box((0.18, 0.022, 0.12), center=(cubby_x, wy, cubby_z + 0.01), bevel=0.005),
        make_cylinder(0.014, 0.014, 0.03, center=(cubby_x + 0.045, wy + 0.14, cubby_z + 0.01), segments=10, axis="y"),
    ]
    orange_caps = [
        make_cylinder(0.013, 0.013, 0.02, center=(cubby_x - 0.055, wy + 0.02, cubby_z + 0.01), segments=8, axis="y"),
        make_cylinder(0.013, 0.013, 0.02, center=(cubby_x - 0.015, wy + 0.02, cubby_z + 0.01), segments=8, axis="y"),
    ]
    uv_tube = make_cylinder(0.014, 0.014, 0.36, center=(cubby_x, cubby_y + 0.18, cubby_z - 0.06), segments=10, axis="y")

    return (
        merge_geometries(towels),
        merge_geometries(white_wands),
        merge_geometries(steel_dock),
        merge_geometries(orange_caps),
        uv_tube,
    )


def make_greywater_reclamation_manifold(
    center_x: float = 0.0,
    base_y: float = 0.16,
    center_z: float = 0.0,
):
    """
    Builds Part 4: Lower Greywater Filtration & H2O Reclamation Manifold:
    - Twin cylindrical greywater filter canisters
    - Swept 3D metallic syphon U-tubes & manifold pipes
    - Signal-orange emergency shutoff / purge valve wheel & collars
    Returns: (white_canisters_geom, steel_pipes_geom, orange_valves_geom)
    """
    canisters = [
        make_cylinder(0.068, 0.068, 0.34, center=(center_x - 0.13, base_y + 0.19, center_z - 0.01), segments=14, axis="y"),
        make_cylinder(0.068, 0.068, 0.34, center=(center_x + 0.13, base_y + 0.19, center_z - 0.01), segments=14, axis="y"),
    ]

    p_left = sample_filleted_polyline(
        [
            (center_x - 0.04, base_y + 0.50, center_z + 0.02),
            (center_x - 0.04, base_y + 0.42, center_z + 0.08),
            (center_x - 0.13, base_y + 0.42, center_z + 0.08),
            (center_x - 0.13, base_y + 0.36, center_z - 0.01),
        ],
        fillet_radius=0.04,
        corner_subdivs=5,
    )
    p_right = sample_filleted_polyline(
        [
            (center_x + 0.04, base_y + 0.50, center_z + 0.02),
            (center_x + 0.04, base_y + 0.42, center_z + 0.08),
            (center_x + 0.13, base_y + 0.42, center_z + 0.08),
            (center_x + 0.13, base_y + 0.36, center_z - 0.01),
        ],
        fillet_radius=0.04,
        corner_subdivs=5,
    )
    steel_pipes = [
        make_swept_tube(p_left, radius=0.020, radial_segments=10),
        make_swept_tube(p_right, radius=0.020, radial_segments=10),
        make_cylinder(0.074, 0.074, 0.04, center=(center_x - 0.13, base_y + 0.36, center_z - 0.01), segments=14, axis="y"),
        make_cylinder(0.074, 0.074, 0.04, center=(center_x + 0.13, base_y + 0.36, center_z - 0.01), segments=14, axis="y"),
    ]

    orange_valves = [
        # Central signal-orange emergency purge/shutoff valve wheel
        make_cylinder(0.052, 0.052, 0.028, center=(center_x, base_y + 0.28, center_z + 0.08), segments=12, axis="z"),
        make_beveled_box((0.12, 0.024, 0.03), center=(center_x, base_y + 0.28, center_z + 0.09), bevel=0.005),
        # Lower filter canister orange locking collars
        make_cylinder(0.072, 0.072, 0.035, center=(center_x - 0.13, base_y + 0.05, center_z - 0.01), segments=14, axis="y"),
        make_cylinder(0.072, 0.072, 0.035, center=(center_x + 0.13, base_y + 0.05, center_z - 0.01), segments=14, axis="y"),
    ]

    return merge_geometries(canisters), merge_geometries(steel_pipes), merge_geometries(orange_valves)


# ==============================================================================
# CANDIDATE 01: RECESSED OCTAGONAL BULKHEAD SONIC VANITY (`vanity_r1_01.glb`)
# Dimensions: 0.95m W x 0.55m D x 2.05m H
# ==============================================================================
def build_01_recessed_octagonal_vanity(mats):
    sm = []
    # 1. Outer 45° Chamfered Octagonal Gunmetal Titanium Housing
    hull = [
        make_beveled_box((0.95, 0.14, 0.55), center=(0.0, 0.07, 0.0), bevel=0.03),
        make_beveled_box((0.95, 0.15, 0.55), center=(0.0, 1.975, 0.0), bevel=0.03),
        make_beveled_box((0.09, 1.82, 0.54), center=(-0.43, 1.02, 0.0), bevel=0.025),
        make_beveled_box((0.09, 1.82, 0.54), center=(0.43, 1.02, 0.0), bevel=0.025),
        make_beveled_box((0.86, 1.84, 0.07), center=(0.0, 1.02, -0.24), bevel=0.02),
        # Vertical divider separating Left Wash/Mirror Zone (X=-0.38..+0.15) from Right UV Cubby Column (X=+0.15..+0.38)
        make_beveled_box((0.04, 1.02, 0.44), center=(0.15, 1.38, -0.02), bevel=0.01),
    ]
    add_part(sm, "Vanity01_OctagonalGunmetalHull", merge_geometries(hull), mats["gunmetal"])

    # 2. Aerospace-White Countertop Deck, Concave Washbasin, UV Cubby Liner & Filter Canisters
    bowl, faucet_steel, cyan_ring = make_concave_basin_and_faucet(center_x=-0.11, deck_y=0.86, center_z=0.04, scale_xz=(1.05, 0.80))
    towels, wands_white, dock_steel, orange_caps, uv_tube = make_uv_towel_and_grooming_kit(cubby_x=0.27, cubby_y=1.02, cubby_z=0.02)
    canisters_white, pipes_steel, valves_orange = make_greywater_reclamation_manifold(center_x=-0.05, base_y=0.15, center_z=0.0)

    white_parts = [
        make_beveled_box((0.84, 0.07, 0.50), center=(0.0, 0.83, 0.01), bevel=0.02),
        make_beveled_box((0.24, 0.96, 0.03), center=(0.27, 1.38, -0.18), bevel=0.01),
        bowl,
        wands_white,
        canisters_white,
    ]
    add_part(sm, "Vanity01_AerospaceWhiteDeckAndBasin", merge_geometries(white_parts), mats["aero_white"])

    # 3. Machined-Steel Faucet Arch, Octagonal Bezel, Towel Bar & Reclamation Pipes
    steel_parts = [
        make_chamfered_aperture_ring(0.86, 1.88, center_y=1.02, z_pos=0.25, tube_r=0.030, chamfer=0.18),
        faucet_steel,
        dock_steel,
        pipes_steel,
        make_cylinder(0.012, 0.012, 0.44, center=(-0.11, 0.76, 0.25), segments=10, axis="x"),
    ]
    add_part(sm, "Vanity01_MachinedSteelFaucetAndPlumbing", merge_geometries(steel_parts), mats["steel_machined"])

    # 4. Backlit Beveled Smart-Mirror HUD + OLED Hygiene Telemetry Strip
    add_part(
        sm,
        "Vanity01_SmartMirrorHUD",
        make_quad_panel((-0.35, 1.12, -0.17), (0.11, 1.12, -0.17), (0.11, 1.82, -0.17), (-0.35, 1.82, -0.17)),
        mats["smart_mirror"],
    )
    add_part(
        sm,
        "Vanity01_OLEDHygieneStrip",
        make_quad_panel((-0.33, 0.96, -0.17), (0.09, 0.96, -0.17), (0.09, 1.08, -0.17), (-0.33, 1.08, -0.17)),
        mats["oled_hygiene"],
    )

    # 5. 3D Folded/Rolled Orbital-Navy Towels + Signal-Orange Valves
    add_part(sm, "Vanity01_OrbitalNavyTowels", towels, mats["navy_towel"])
    add_part(sm, "Vanity01_SignalOrangeValves", merge_geometries([orange_caps, valves_orange]), mats["accent_orange"])

    # 6. Practical Emissive Lighting (Ice-White Mirror Bars, Cyan Basin Ring, UV-Violet Cubby, Amber Toe-Kick)
    ice_bars = [
        make_beveled_box((0.024, 0.68, 0.03), center=(-0.37, 1.47, -0.15), bevel=0.004),
        make_beveled_box((0.024, 0.68, 0.03), center=(0.13, 1.47, -0.15), bevel=0.004),
    ]
    add_part(sm, "Vanity01_SurgicalIceWhiteMirrorBars", merge_geometries(ice_bars), mats["led_ice"])
    add_part(sm, "Vanity01_CyanAtomizerAndCove", merge_geometries([cyan_ring, make_beveled_box((0.76, 0.024, 0.04), center=(0.0, 1.88, 0.14), bevel=0.004)]), mats["led_cyan"])
    add_part(sm, "Vanity01_UVSterilizerEmitter", uv_tube, mats["led_uv"])
    add_part(sm, "Vanity01_AmberToeKickLED", make_beveled_box((0.74, 0.022, 0.04), center=(0.0, 0.14, 0.24), bevel=0.004), mats["led_amber"])

    # 7. Translucent Doors: Upper-Right Violet UV Cubby Door + Lower Cyan Greywater Inspection Shield (alphaMode: "BLEND")
    add_part(
        sm,
        "Vanity01_UVCubbyTranslucentDoor",
        make_quad_panel((0.17, 0.92, 0.23), (0.38, 0.92, 0.23), (0.38, 1.84, 0.23), (0.17, 1.84, 0.23)),
        mats["glass_uv"],
    )
    add_part(
        sm,
        "Vanity01_LowerReclamationTranslucentShield",
        make_quad_panel((-0.36, 0.16, 0.23), (0.36, 0.16, 0.23), (0.36, 0.74, 0.23), (-0.36, 0.74, 0.23)),
        mats["glass_sonic"],
    )

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "vanity_r1_01.glb"), sm, root_name="VanityR1_01_RecessedOctagonalVanity")


# ==============================================================================
# CANDIDATE 02: CANTILEVERED AEROSPACE POD BASIN & FLOATING HALO MIRROR (`vanity_r1_02.glb`)
# Dimensions: 0.90m W x 0.55m D x 2.00m H
# ==============================================================================
def build_02_cantilevered_halo_vanity(mats):
    sm = []
    # 1. Wall-Mounted Carbon-Slate Vertical Structural Spine & Overhead Locker Housing
    spine = [
        make_beveled_box((0.90, 0.12, 0.52), center=(0.0, 0.06, -0.01), bevel=0.025),
        make_beveled_box((0.76, 1.96, 0.12), center=(0.0, 1.00, -0.21), bevel=0.025),
        # Top overhead towel & med-kit locker housing (Y = 1.66 to 2.00)
        make_beveled_box((0.90, 0.34, 0.48), center=(0.0, 1.83, -0.02), bevel=0.03),
    ]
    add_part(sm, "Vanity02_CarbonSlateVerticalSpine", merge_geometries(spine), mats["carbon_slate"])

    # 2. Cantilevered Stadium-Curved Aerospace-White Floating Washbasin Pod (Y = 0.78 to 0.92)
    bowl, faucet_steel, cyan_ring = make_concave_basin_and_faucet(center_x=0.0, deck_y=0.88, center_z=0.05, scale_xz=(1.15, 0.85))
    canisters_white, pipes_steel, valves_orange = make_greywater_reclamation_manifold(center_x=0.0, base_y=0.12, center_z=-0.02)

    floating_pod = [
        make_sculpted_cushion((0.88, 0.14, 0.52), center=(0.0, 0.83, 0.01), res=(7, 3, 5), roundness=0.32, belly_puff=0.02, pinch_corners=0.0, crease_freq=0),
        bowl,
        canisters_white,
    ]
    add_part(sm, "Vanity02_CantileveredWhiteBasinPod", merge_geometries(floating_pod), mats["aero_white"])

    # 3. Exposed Machined-Steel Cantilever Support Brackets, Syphon U-Tubes & Halo Mirror Frame
    cantilever_l = sample_filleted_polyline([(-0.34, 0.54, -0.16), (-0.34, 0.78, 0.22), (0.34, 0.78, 0.22), (0.34, 0.54, -0.16)], 0.06, 5)
    halo_bezel = make_chamfered_aperture_ring(0.58, 0.58, center_y=1.34, z_pos=-0.10, tube_r=0.026, chamfer=0.16)
    steel_parts = [
        make_swept_tube(cantilever_l, radius=0.020, radial_segments=10),
        halo_bezel,
        faucet_steel,
        pipes_steel,
    ]
    add_part(sm, "Vanity02_MachinedCantileverAndSyphons", merge_geometries(steel_parts), mats["steel_machined"])

    # 4. Circular/Octagonal Floating Halo Smart Mirror + 360° Glowing Halo Ring
    add_part(
        sm,
        "Vanity02_FloatingHaloSmartMirror",
        make_quad_panel((-0.27, 1.07, -0.11), (0.27, 1.07, -0.11), (0.27, 1.61, -0.11), (-0.27, 1.61, -0.11)),
        mats["smart_mirror"],
    )
    halo_glow = make_chamfered_aperture_ring(0.64, 0.64, center_y=1.34, z_pos=-0.12, tube_r=0.016, chamfer=0.18)
    add_part(sm, "Vanity02_HaloMirrorIceWhiteRing", halo_glow, mats["led_ice"])
    add_part(sm, "Vanity02_BasinCyanAtomizerRing", cyan_ring, mats["led_cyan"])

    # 5. Overhead Towel & Grooming Cubby Contents + OLED Strip + Signal-Orange Purge Valve
    towels_top = [
        make_sculpted_cushion((0.22, 0.045, 0.18), center=(-0.18, 1.74, 0.04), res=(5, 3, 4), roundness=0.35, belly_puff=0.04, crease_freq=4),
        make_sculpted_cushion((0.22, 0.045, 0.18), center=(-0.18, 1.79, 0.04), res=(5, 3, 4), roundness=0.35, belly_puff=0.04, crease_freq=4),
        make_cylinder(0.032, 0.032, 0.16, center=(0.14, 1.76, 0.04), segments=12, axis="z"),
        make_cylinder(0.032, 0.032, 0.16, center=(0.24, 1.76, 0.04), segments=12, axis="z"),
    ]
    add_part(sm, "Vanity02_OverheadFoldedNavyTowels", merge_geometries(towels_top), mats["navy_towel"])
    add_part(sm, "Vanity02_SignalOrangePurgeValve", valves_orange, mats["accent_orange"])
    add_part(sm, "Vanity02_OverheadUVEmitterBar", make_beveled_box((0.68, 0.022, 0.04), center=(0.0, 1.94, 0.12), bevel=0.004), mats["led_uv"])
    add_part(
        sm,
        "Vanity02_FrontBasinOLEDReadout",
        make_quad_panel((-0.18, 0.79, 0.272), (0.18, 0.79, 0.272), (0.18, 0.86, 0.272), (-0.18, 0.86, 0.272)),
        mats["oled_hygiene"],
    )

    # 6. Twin Sliding Translucent Doors on Overhead Cubby + Lower Inspection Shield (alphaMode: "BLEND")
    add_part(
        sm,
        "Vanity02_OverheadUVTranslucentDoor",
        make_quad_panel((-0.40, 1.69, 0.23), (0.40, 1.69, 0.23), (0.40, 1.96, 0.23), (-0.40, 1.96, 0.23)),
        mats["glass_uv"],
    )
    add_part(
        sm,
        "Vanity02_LowerSyphonTranslucentShield",
        make_quad_panel((-0.34, 0.14, 0.18), (0.34, 0.14, 0.18), (0.34, 0.56, 0.18), (-0.34, 0.56, 0.18)),
        mats["glass_sonic"],
    )

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "vanity_r1_02.glb"), sm, root_name="VanityR1_02_CantileveredHaloVanity")


# ==============================================================================
# CANDIDATE 03: DUAL-ZONE SPLIT GROOMING & UV DECON STATION (`vanity_r1_03.glb`)
# Dimensions: 1.05m W x 0.58m D x 2.08m H (Companion to Locker Winner #02)
# ==============================================================================
def build_03_dual_zone_split_station(mats):
    sm = []
    # 1. Asymmetric 65% / 35% Split-Bay Gunmetal Bulkhead Cabinet
    # Left Bay: X = -0.525 to +0.155 (0.68m wide); Right Bay: X = +0.155 to +0.525 (0.37m wide)
    cabinet = [
        make_beveled_box((1.05, 0.14, 0.58), center=(0.0, 0.07, 0.0), bevel=0.03),
        make_beveled_box((1.05, 0.14, 0.58), center=(0.0, 2.01, 0.0), bevel=0.03),
        make_beveled_box((0.08, 1.90, 0.56), center=(-0.485, 1.04, 0.0), bevel=0.025),
        make_beveled_box((0.08, 1.90, 0.56), center=(0.485, 1.04, 0.0), bevel=0.025),
        # Center vertical structural partition at X = +0.155
        make_beveled_box((0.06, 1.84, 0.54), center=(0.155, 1.04, -0.01), bevel=0.02),
        make_beveled_box((0.96, 1.86, 0.07), center=(0.0, 1.04, -0.25), bevel=0.02),
        # Right Bay 3-tier shelves at Y = 0.78 and Y = 1.38
        make_beveled_box((0.30, 0.035, 0.48), center=(0.32, 0.78, -0.01), bevel=0.01),
        make_beveled_box((0.30, 0.035, 0.48), center=(0.32, 1.38, -0.01), bevel=0.01),
    ]
    add_part(sm, "Vanity03_SplitBayGunmetalCabinet", merge_geometries(cabinet), mats["gunmetal"])

    # 2. Left Bay Aerospace-White Countertop & Basin + Right Bay Spare Filter & Grooming Wands
    bowl, faucet_steel, cyan_ring = make_concave_basin_and_faucet(
        center_x=-0.16, deck_y=0.86, center_z=0.04, scale_xz=(1.05, 0.80), halo_faucet=True
    )
    towels, wands_white, dock_steel, orange_caps, uv_tube = make_uv_towel_and_grooming_kit(
        cubby_x=0.32, cubby_y=0.82, cubby_z=0.02
    )
    canisters_white, pipes_steel, valves_orange = make_greywater_reclamation_manifold(
        center_x=-0.16, base_y=0.14, center_z=0.0
    )

    white_parts = [
        make_beveled_box((0.62, 0.07, 0.50), center=(-0.16, 0.83, 0.01), bevel=0.02),
        make_beveled_box((0.28, 1.76, 0.03), center=(0.32, 1.04, -0.20), bevel=0.01),
        bowl,
        wands_white,
        canisters_white,
        # Spare H2O filter cartridge in bottom-right shelf
        make_cylinder(0.056, 0.056, 0.36, center=(0.32, 0.42, 0.02), segments=12, axis="y"),
    ]
    add_part(sm, "Vanity03_WhiteBasinAndFilterCartridges", merge_geometries(white_parts), mats["aero_white"])

    # 3. Machined-Steel Halo Faucet, Bezel Frames & Reclamation Pipes
    steel_parts = [
        faucet_steel,
        dock_steel,
        pipes_steel,
        make_beveled_box((0.30, 0.025, 0.03), center=(0.32, 0.80, 0.23), bevel=0.005),
        make_beveled_box((0.30, 0.025, 0.03), center=(0.32, 1.40, 0.23), bevel=0.005),
    ]
    add_part(sm, "Vanity03_MachinedHaloFaucetAndBezels", merge_geometries(steel_parts), mats["steel_machined"])

    # 4. Left Bay Beveled Smart-Mirror HUD + Flush OLED Hygiene Telemetry Strip
    add_part(
        sm,
        "Vanity03_LeftBaySmartMirrorHUD",
        make_quad_panel((-0.41, 1.14, -0.19), (0.09, 1.14, -0.19), (0.09, 1.84, -0.19), (-0.41, 1.84, -0.19)),
        mats["smart_mirror"],
    )
    add_part(
        sm,
        "Vanity03_LeftBayOLEDTelemetry",
        make_quad_panel((-0.38, 0.96, -0.19), (0.06, 0.96, -0.19), (0.06, 1.09, -0.19), (-0.38, 1.09, -0.19)),
        mats["oled_hygiene"],
    )

    # 5. Right Tower 3D Folded/Rolled Orbital-Navy Towels + Signal-Orange Collars/Valves
    add_part(sm, "Vanity03_RightTowerOrbitalNavyTowels", towels, mats["navy_towel"])
    orange_all = [
        orange_caps,
        valves_orange,
        make_cylinder(0.060, 0.060, 0.04, center=(0.32, 0.61, 0.02), segments=12, axis="y"),
    ]
    add_part(sm, "Vanity03_SignalOrangeValvesAndCollars", merge_geometries(orange_all), mats["accent_orange"])

    # 6. Practical Lighting: Left Alcove Cyan/Ice-White + Right Tower UV-Violet + Lower Amber
    add_part(
        sm,
        "Vanity03_LeftAlcoveIceWhiteBars",
        merge_geometries([
            make_beveled_box((0.024, 0.68, 0.03), center=(-0.43, 1.48, -0.16), bevel=0.004),
            make_beveled_box((0.024, 0.68, 0.03), center=(0.11, 1.48, -0.16), bevel=0.004),
        ]),
        mats["led_ice"],
    )
    add_part(
        sm,
        "Vanity03_CyanAtomizerAndTopCove",
        merge_geometries([cyan_ring, make_beveled_box((0.56, 0.024, 0.04), center=(-0.16, 1.90, 0.14), bevel=0.004)]),
        mats["led_cyan"],
    )
    uv_bars = [
        uv_tube,
        make_cylinder(0.014, 0.014, 1.62, center=(0.43, 1.04, 0.10), segments=10, axis="y"),
    ]
    add_part(sm, "Vanity03_RightTowerUVVioletTubes", merge_geometries(uv_bars), mats["led_uv"])
    add_part(sm, "Vanity03_LowerAmberStrip", make_beveled_box((0.86, 0.022, 0.04), center=(0.0, 0.14, 0.25), bevel=0.004), mats["led_amber"])

    # 7. Translucent Doors: Right Full-Height Violet UV Tower Door + Lower-Left Cyan Reclamation Window (alphaMode: "BLEND")
    add_part(
        sm,
        "Vanity03_RightTowerUVTranslucentDoor",
        make_quad_panel((0.18, 0.18, 0.25), (0.45, 0.18, 0.25), (0.45, 1.90, 0.25), (0.18, 1.90, 0.25)),
        mats["glass_uv"],
    )
    add_part(
        sm,
        "Vanity03_LowerLeftReclamationTranslucentWindow",
        make_quad_panel((-0.42, 0.16, 0.24), (0.11, 0.16, 0.24), (0.11, 0.74, 0.24), (-0.42, 0.74, 0.24)),
        mats["glass_sonic"],
    )

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "vanity_r1_03.glb"), sm, root_name="VanityR1_03_DualZoneSplitStation")


# ==============================================================================
# CANDIDATE 04: CYLINDRICAL SONIC-MIST ALCOVE & PRIVACY SHIELD VANITY (`vanity_r1_04.glb`)
# Dimensions: 0.92m W x 0.62m D x 2.08m H
# ==============================================================================
def build_04_cylindrical_sonic_alcove(mats):
    sm = []
    # 1. Semi-Cylindrical Gunmetal Outer Column & Top/Bottom Pressure Collars
    outer_col = [
        make_beveled_box((0.92, 0.15, 0.62), center=(0.0, 0.075, 0.0), bevel=0.035),
        make_beveled_box((0.92, 0.16, 0.62), center=(0.0, 2.00, 0.0), bevel=0.035),
        make_beveled_box((0.11, 1.80, 0.58), center=(-0.405, 1.04, -0.01), bevel=0.04),
        make_beveled_box((0.11, 1.80, 0.58), center=(0.405, 1.04, -0.01), bevel=0.04),
        make_beveled_box((0.78, 1.82, 0.08), center=(0.0, 1.04, -0.26), bevel=0.025),
    ]
    add_part(sm, "Vanity04_CylindricalGunmetalColumn", merge_geometries(outer_col), mats["gunmetal"])

    # 2. Concave Aerospace-White Inner Wash Chamber, Countertop & Lower Filter Canisters
    bowl_steel, faucet_steel, cyan_ring = make_concave_basin_and_faucet(center_x=0.0, deck_y=0.86, center_z=0.05, scale_xz=(1.0, 0.90))
    towels, wands_white, dock_steel, orange_caps, uv_tube = make_uv_towel_and_grooming_kit(cubby_x=0.22, cubby_y=0.44, cubby_z=0.04)
    canisters_white, pipes_steel, valves_orange = make_greywater_reclamation_manifold(center_x=-0.12, base_y=0.15, center_z=0.0)

    white_chamber = [
        make_beveled_box((0.74, 0.06, 0.52), center=(0.0, 0.83, 0.01), bevel=0.02),
        make_beveled_box((0.72, 1.72, 0.04), center=(0.0, 1.04, -0.20), bevel=0.015),
        wands_white,
        canisters_white,
    ]
    add_part(sm, "Vanity04_ConcaveWhiteWashChamber", merge_geometries(white_chamber), mats["aero_white"])

    # 3. Hemispherical Brushed-Steel Basin Bowl, Overhead Sonic Ring & Curved Shield Tracks
    steel_parts = [
        bowl_steel,
        faucet_steel,
        dock_steel,
        pipes_steel,
        make_cylinder(0.32, 0.32, 0.035, center=(0.0, 1.88, 0.02), segments=20, axis="y"),
        make_chamfered_aperture_ring(0.82, 1.82, center_y=1.04, z_pos=0.26, tube_r=0.028, chamfer=0.18),
    ]
    add_part(sm, "Vanity04_HemisphericalSteelBasinAndTracks", merge_geometries(steel_parts), mats["steel_machined"])

    # 4. Curved Panoramic Smart-Mirror HUD + OLED Readout
    add_part(
        sm,
        "Vanity04_PanoramicSmartMirror",
        make_quad_panel((-0.28, 1.14, -0.17), (0.28, 1.14, -0.17), (0.28, 1.78, -0.17), (-0.28, 1.78, -0.17)),
        mats["smart_mirror"],
    )
    add_part(
        sm,
        "Vanity04_OLEDControlBadge",
        make_quad_panel((-0.18, 0.96, -0.17), (0.18, 0.96, -0.17), (0.18, 1.08, -0.17), (-0.18, 1.08, -0.17)),
        mats["oled_hygiene"],
    )

    # 5. Lower Compartment Folded Navy Towels + Signal-Orange Valves
    add_part(sm, "Vanity04_OrbitalNavyTowels", towels, mats["navy_towel"])
    add_part(sm, "Vanity04_SignalOrangeValves", merge_geometries([orange_caps, valves_orange]), mats["accent_orange"])

    # 6. Overhead Cyan Sonic Ring + Mirror Ice-White Strips + UV Cubby Tube + Amber Toe-Kick
    add_part(
        sm,
        "Vanity04_OverheadCyanSonicRing",
        merge_geometries([cyan_ring, make_beveled_box((0.62, 0.026, 0.05), center=(0.0, 1.85, 0.14), bevel=0.005)]),
        mats["led_cyan"],
    )
    add_part(
        sm,
        "Vanity04_MirrorIceWhiteBars",
        merge_geometries([
            make_beveled_box((0.022, 0.64, 0.03), center=(-0.31, 1.46, -0.15), bevel=0.004),
            make_beveled_box((0.022, 0.64, 0.03), center=(0.31, 1.46, -0.15), bevel=0.004),
        ]),
        mats["led_ice"],
    )
    add_part(sm, "Vanity04_UVSterilizerTube", uv_tube, mats["led_uv"])
    add_part(sm, "Vanity04_AmberToeKick", make_beveled_box((0.68, 0.022, 0.04), center=(0.0, 0.15, 0.28), bevel=0.004), mats["led_amber"])

    # 7. Parted Curved Translucent Sonic-Mist Splash Shields + Lower UV Compartment Door (alphaMode: "BLEND")
    parted_shields = [
        make_quad_panel((-0.36, 0.88, 0.25), (-0.14, 0.88, 0.28), (-0.14, 1.86, 0.28), (-0.36, 1.86, 0.25)),
        make_quad_panel((0.14, 0.88, 0.28), (0.36, 0.88, 0.25), (0.36, 1.86, 0.25), (0.14, 1.86, 0.28)),
    ]
    add_part(sm, "Vanity04_PartedSonicSplashShields", merge_geometries(parted_shields), mats["glass_sonic"])
    add_part(
        sm,
        "Vanity04_LowerUVTranslucentDoor",
        make_quad_panel((-0.34, 0.18, 0.26), (0.34, 0.18, 0.26), (0.34, 0.76, 0.26), (-0.34, 0.76, 0.26)),
        mats["glass_uv"],
    )

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "vanity_r1_04.glb"), sm, root_name="VanityR1_04_CylindricalSonicAlcove")


# ==============================================================================
# CANDIDATE 05: CORNER-CHAMFERED COMPACT CREW WASH & MED-DISPENSER (`vanity_r1_05.glb`)
# Dimensions: 0.98m W x 0.60m D x 2.05m H
# ==============================================================================
def build_05_corner_chamfered_vanity(mats):
    sm = []
    # 1. 45°-Angled Wedge/Corner-Fit Gunmetal Chassis with Two 35°-Canted Side Storage Wings
    wedge_hull = [
        make_beveled_box((0.98, 0.14, 0.60), center=(0.0, 0.07, 0.0), bevel=0.03),
        make_beveled_box((0.98, 0.15, 0.60), center=(0.0, 1.975, 0.0), bevel=0.03),
        make_beveled_box((0.68, 1.84, 0.07), center=(0.0, 1.02, -0.26), bevel=0.02),
        # Left 35°-canted storage wing housing
        transform_geom(
            make_beveled_box((0.20, 1.78, 0.44), center=(0.0, 0.0, 0.0), bevel=0.02),
            translate=(-0.36, 1.02, -0.02),
            rot_xyz_deg=(0.0, 28.0, 0.0),
        ),
        # Right 35°-canted storage wing housing
        transform_geom(
            make_beveled_box((0.20, 1.78, 0.44), center=(0.0, 0.0, 0.0), bevel=0.02),
            translate=(0.36, 1.02, -0.02),
            rot_xyz_deg=(0.0, -28.0, 0.0),
        ),
    ]
    add_part(sm, "Vanity05_CornerWedgeGunmetalHull", merge_geometries(wedge_hull), mats["gunmetal"])

    # 2. Trapezoidal Aerospace-White Countertop, Basin, Grooming Wands & Filter Canisters
    bowl, faucet_steel, cyan_ring = make_concave_basin_and_faucet(center_x=0.0, deck_y=0.86, center_z=0.05, scale_xz=(1.05, 0.82))
    towels, wands_white, dock_steel, orange_caps, uv_tube = make_uv_towel_and_grooming_kit(cubby_x=-0.30, cubby_y=1.08, cubby_z=0.08)
    canisters_white, pipes_steel, valves_orange = make_greywater_reclamation_manifold(center_x=0.0, base_y=0.14, center_z=0.0)

    white_parts = [
        make_beveled_box((0.78, 0.07, 0.52), center=(0.0, 0.83, 0.02), bevel=0.02),
        bowl,
        wands_white,
        canisters_white,
    ]
    add_part(sm, "Vanity05_TrapezoidalWhiteBasinAndFilters", merge_geometries(white_parts), mats["aero_white"])

    # 3. Machined-Steel Faucet Arch, Center Bezel & Plumbing Manifold
    steel_parts = [
        make_chamfered_aperture_ring(0.56, 1.78, center_y=1.02, z_pos=0.25, tube_r=0.026, chamfer=0.14),
        faucet_steel,
        dock_steel,
        pipes_steel,
    ]
    add_part(sm, "Vanity05_MachinedSteelFaucetAndBezel", merge_geometries(steel_parts), mats["steel_machined"])

    # 4. Central Trapezoidal Smart-Mirror HUD + OLED Hygiene Readout
    add_part(
        sm,
        "Vanity05_CenterTrapezoidalSmartMirror",
        make_quad_panel((-0.24, 1.14, -0.20), (0.24, 1.14, -0.20), (0.24, 1.82, -0.20), (-0.24, 1.82, -0.20)),
        mats["smart_mirror"],
    )
    add_part(
        sm,
        "Vanity05_CenterOLEDHygienePanel",
        make_quad_panel((-0.18, 0.96, -0.20), (0.18, 0.96, -0.20), (0.18, 1.09, -0.20), (-0.18, 1.09, -0.20)),
        mats["oled_hygiene"],
    )

    # 5. Right Wing Folded Orbital-Navy Towels + Signal-Orange Emergency Eye-Wash & Med Dispenser
    right_towels = transform_geom(towels, translate=(0.60, 0.0, 0.0))
    add_part(sm, "Vanity05_RightWingOrbitalNavyTowels", right_towels, mats["navy_towel"])

    orange_med = [
        orange_caps,
        valves_orange,
        # Right wing signal-orange emergency eye-wash & med-dispenser unit
        make_beveled_box((0.12, 0.22, 0.08), center=(0.30, 1.52, 0.12), bevel=0.012),
    ]
    add_part(sm, "Vanity05_SignalOrangeMedDispenserAndValves", merge_geometries(orange_med), mats["accent_orange"])

    # 6. Practical Lighting: Mirror Ice-White Bars, Cyan Basin Ring, Left UV-Violet Tube, Amber Toe-Kick
    add_part(
        sm,
        "Vanity05_MirrorIceWhiteBars",
        merge_geometries([
            make_beveled_box((0.022, 0.66, 0.03), center=(-0.25, 1.48, -0.18), bevel=0.004),
            make_beveled_box((0.022, 0.66, 0.03), center=(0.25, 1.48, -0.18), bevel=0.004),
        ]),
        mats["led_ice"],
    )
    add_part(
        sm,
        "Vanity05_CyanAtomizerAndCrownLED",
        merge_geometries([cyan_ring, make_beveled_box((0.52, 0.024, 0.04), center=(0.0, 1.88, 0.16), bevel=0.004)]),
        mats["led_cyan"],
    )
    add_part(sm, "Vanity05_LeftWingUVVioletTube", uv_tube, mats["led_uv"])
    add_part(sm, "Vanity05_AmberToeKickLED", make_beveled_box((0.56, 0.022, 0.04), center=(0.0, 0.14, 0.26), bevel=0.004), mats["led_amber"])

    # 7. Twin Angled Wing Translucent Doors + Lower Reclamation Shield (alphaMode: "BLEND")
    left_uv_door = transform_geom(
        make_quad_panel((-0.09, 0.90, 0.0), (0.09, 0.90, 0.0), (0.09, 1.82, 0.0), (-0.09, 1.82, 0.0)),
        translate=(-0.32, 0.0, 0.20),
        rot_xyz_deg=(0.0, 28.0, 0.0),
    )
    right_towel_door = transform_geom(
        make_quad_panel((-0.09, 0.90, 0.0), (0.09, 0.90, 0.0), (0.09, 1.82, 0.0), (-0.09, 1.82, 0.0)),
        translate=(0.32, 0.0, 0.20),
        rot_xyz_deg=(0.0, -28.0, 0.0),
    )
    add_part(sm, "Vanity05_LeftWingUVTranslucentDoor", left_uv_door, mats["glass_uv"])
    add_part(
        sm,
        "Vanity05_RightWingAndLowerTranslucentDoors",
        merge_geometries([
            right_towel_door,
            make_quad_panel((-0.25, 0.16, 0.25), (0.25, 0.16, 0.25), (0.25, 0.74, 0.25), (-0.25, 0.74, 0.25)),
        ]),
        mats["glass_sonic"],
    )

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "vanity_r1_05.glb"), sm, root_name="VanityR1_05_CornerChamferedVanity")


def build_all_vanity_round1():
    mats = get_vanity_materials()
    builders = [
        build_01_recessed_octagonal_vanity,
        build_02_cantilevered_halo_vanity,
        build_03_dual_zone_split_station,
        build_04_cylindrical_sonic_alcove,
        build_05_corner_chamfered_vanity,
    ]
    results = []
    for fn in builders:
        info = fn(mats)
        fname = os.path.basename(info["filepath"])
        dims = info["dimensions"]
        print(
            f"[vanity_r1] Built {fname:16s} | {dims[0]:.2f}m W x {dims[2]:.2f}m D x {dims[1]:.2f}m H | "
            f"verts={info['vertices']:4d} | tris={info['triangles']:4d} | min_y={info['min'][1]:.5f}"
        )
        results.append(info)
    with open(os.path.join(OUT_GLB_DIR, "vanity_r1_manifest.json"), "w") as f:
        json.dump(results, f, indent=2)
    return results


if __name__ == "__main__":
    build_all_vanity_round1()
