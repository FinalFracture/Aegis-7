#!/usr/bin/env python3
"""
Builds all 5 Round-1 Hard Sci-Fi Room 08 Hero Asset (Ambient Zero-G Beverage Bar &
Celestial Observatory Lounge Island) .glb models:
  /workspace/game-project/assets/glb/lounge_round1/lounge_bar_r1_01.glb .. lounge_bar_r1_05.glb
Plus exports Winner #02 to /workspace/game-project/assets/glb/winners/,
the Auxiliary Center Sunken Viewing Pit & Holo-Table Set (lounge_viewing_pit_set.glb),
and the Room 08 Architectural Shell (room_08_shell.glb & aliases).

Follows /workspace/game-project/design/lounge_round1/lounge_bar_r1_spec.md ("Aegis-7 Standard"):
- Bottom-center (0.0, 0.0, 0.0) floor pivot (min_y == 0.0000, centered X and Z), front facing +Z
- Polygon budget: 3,500 - 5,800 triangles per candidate
- Mandatory 4-Part 3D Celestial Lounge & Zero-G Beverage Kit in every candidate:
  1. 45° Chamfered Bulkhead Spine & Cantilevered Illuminated Bar Counter (Y = 0.0m-0.96m)
  2. Translucent Zero-G Botanical & Decanter Tower (glass_lounge_bar_translucent.png, alphaMode: "BLEND", alpha ~ 0.19)
     revealing 3D Illuminated Botanical Infusion Carafes, Spherical Drink Pods & Living Aeroponic Herb Trough
  3. Zero-G Beverage Dispensing Arch, Magnetic Bulb-Glasses & Celestial OLED Console (oled_lounge_celestial_bar.png)
  4. Two Pivoting Orbital-Navy & Charcoal Lounge Barstools (Y ~ 0.62m) on Brushed-Steel Pedestals
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

TEX_LOUNGE_DIR = "/workspace/game-project/assets/textures/lounge_round1"
OUT_GLB_DIR = "/workspace/game-project/assets/glb/lounge_round1"
WINNERS_DIR = "/workspace/game-project/assets/glb/winners"
ROOMS_DIR = "/workspace/game-project/assets/glb/rooms"
os.makedirs(OUT_GLB_DIR, exist_ok=True)
os.makedirs(WINNERS_DIR, exist_ok=True)
os.makedirs(ROOMS_DIR, exist_ok=True)


def tex_lounge(fname: str) -> str:
    return os.path.join(TEX_LOUNGE_DIR, fname)


def get_lounge_materials():
    return {
        "gunmetal": PBRMaterialDef(
            name="Mat_Titanium_GunmetalHull",
            base_color=hex_rgba("#1A1E24"),
            metallic=0.78,
            roughness=0.34,
            texture_path=tex_lounge("titanium_gunmetal_hull.png"),
        ),
        "aero_white": PBRMaterialDef(
            name="Mat_Composite_AerospaceWhite",
            base_color=hex_rgba("#D8DEE6"),
            metallic=0.08,
            roughness=0.26,
            texture_path=tex_lounge("composite_aerospace_white.png"),
        ),
        "carbon_slate": PBRMaterialDef(
            name="Mat_Carbon_SlateFrame",
            base_color=hex_rgba("#282E38"),
            metallic=0.58,
            roughness=0.40,
            texture_path=tex_lounge("carbon_slate_frame.png"),
        ),
        "steel_machined": PBRMaterialDef(
            name="Mat_Steel_MachinedGantry",
            base_color=hex_rgba("#88929E"),
            metallic=0.92,
            roughness=0.18,
            texture_path=tex_lounge("steel_machined_gantry.png"),
        ),
        "fabric_charcoal": PBRMaterialDef(
            name="Mat_Fabric_CharcoalFlightpad",
            base_color=hex_rgba("#242932"),
            metallic=0.0,
            roughness=0.78,
            texture_path=tex_lounge("fabric_charcoal_flightpad.png"),
        ),
        "fabric_navy": PBRMaterialDef(
            name="Mat_Fabric_OrbitalNavyPad",
            base_color=hex_rgba("#1D2C3C"),
            metallic=0.0,
            roughness=0.76,
            texture_path=tex_lounge("fabric_orbital_navy_pad.png"),
        ),
        "foliage_herbs": PBRMaterialDef(
            name="Mat_Foliage_AeroponicHerbs",
            base_color=hex_rgba("#2E5A36"),
            metallic=0.0,
            roughness=0.52,
            texture_path=tex_lounge("foliage_aeroponic_herbs.png"),
        ),
        "accent_orange": PBRMaterialDef(
            name="Mat_Accent_SignalOrange",
            base_color=hex_rgba("#D95B26"),
            metallic=0.06,
            roughness=0.48,
            texture_path=tex_lounge("accent_signal_orange.png"),
        ),
        "oled_celestial": PBRMaterialDef(
            name="Mat_OLED_LoungeCelestialBar",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.10,
            roughness=0.14,
            emissive=(0.35, 0.90, 1.0),
            texture_path=tex_lounge("oled_lounge_celestial_bar.png"),
        ),
        "glass_lounge": PBRMaterialDef(
            name="Mat_Glass_LoungeBar_Translucent",
            base_color=(0.48, 0.86, 1.0, 0.19),
            metallic=0.12,
            roughness=0.06,
            emissive=(0.0, 0.16, 0.28),
            texture_path=tex_lounge("glass_lounge_bar_translucent.png"),
            double_sided=True,
            alpha_mode="BLEND",
        ),
        "led_cyan": PBRMaterialDef(
            name="Mat_Emissive_CyanLED",
            base_color=hex_rgba("#00E5FF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.0, 0.92, 1.0),
            texture_path=tex_lounge("led_cyan_strip.png"),
        ),
        "led_amber": PBRMaterialDef(
            name="Mat_Emissive_AmberLED",
            base_color=hex_rgba("#FF9500"),
            metallic=0.0,
            roughness=0.15,
            emissive=(1.0, 0.58, 0.0),
            texture_path=tex_lounge("led_amber_strip.png"),
        ),
        "led_uv": PBRMaterialDef(
            name="Mat_Emissive_UVVioletLED",
            base_color=hex_rgba("#7B5CFF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.55, 0.38, 1.0),
            texture_path=tex_lounge("led_uv_violet.png"),
        ),
    }


def make_closed_circle_ring_xz(radius: float, tube_r: float = 0.012, cy: float = 0.24, cx: float = 0.0, cz: float = 0.0, n_pts: int = 18):
    pts = []
    for i in range(n_pts + 1):
        ang = 2.0 * math.pi * (i / float(n_pts))
        pts.append([cx + radius * math.cos(ang), cy, cz + radius * math.sin(ang)])
    return make_swept_tube(np.array(pts, dtype=np.float32), radius=tube_r, radial_segments=6)


def make_lounge_barstool(cx: float, cz: float, seat_y: float = 0.62):
    """
    Builds Part 4: Pivoting Orbital-Navy & Charcoal Lounge Barstool (Y ~ 0.62m)
    on a brushed-steel pedestal with tubular chrome footrest ring and signal-orange swivel lock.
    Returns: (navy_cushion_geom, charcoal_shell_geom, steel_pedestal_geom, orange_lock_geom)
    """
    navy_geom = merge_geometries([
        make_sculpted_cushion((0.38, 0.08, 0.36), center=(cx, seat_y, cz), res=(5, 3, 5), roundness=0.42, belly_puff=0.04, tuft_grid=(2, 2), tuft_depth=0.010, crease_freq=0),
        make_sculpted_cushion((0.36, 0.22, 0.07), center=(cx, seat_y + 0.15, cz + 0.15), res=(5, 4, 3), roundness=0.38, belly_puff=0.04, crease_freq=0),
    ])
    charcoal_geom = merge_geometries([
        make_beveled_box((0.40, 0.05, 0.38), center=(cx, seat_y - 0.05, cz), bevel=0.016),
        make_beveled_box((0.38, 0.24, 0.04), center=(cx, seat_y + 0.14, cz + 0.19), bevel=0.014),
    ])
    steel_geom = merge_geometries([
        make_cylinder(0.20, 0.23, 0.035, center=(cx, 0.018, cz), segments=14, axis="y"),
        make_cylinder(0.042, 0.048, seat_y - 0.08, center=(cx, (seat_y - 0.04) * 0.5, cz), segments=12, axis="y"),
        make_closed_circle_ring_xz(radius=0.18, tube_r=0.012, cy=0.24, cx=cx, cz=cz, n_pts=16),
    ])
    orange_geom = make_beveled_box((0.06, 0.025, 0.04), center=(cx + 0.06, seat_y - 0.09, cz), bevel=0.005)
    return navy_geom, charcoal_geom, steel_geom, orange_geom


def make_bar_siphon_arch_and_bulb_glasses(bar_cx: float, bar_cz: float = 0.08, counter_y: float = 0.94):
    """
    Builds Part 3:
    - Sculpted Brushed-Steel Triple-Nozzle Zero-G Siphon Tap Arch
    - 3 Spherical/Bulb Zero-G Sipper Glasses locked onto Glowing Cyan Coaster Rings on the counter
    - Signal-Orange Pressure-Infusion Valves
    - Flush-mounted OLED Star-Map & Beverage Synthesizer Display (oled_lounge_celestial_bar.png)
    Returns: (steel_arch_geom, cyan_coasters_and_bulbs_geom, orange_valves_geom, oled_screen_geom)
    """
    arch_pts = sample_filleted_polyline(
        [
            (bar_cx - 0.36, counter_y, bar_cz - 0.14),
            (bar_cx - 0.32, counter_y + 0.34, bar_cz - 0.06),
            (bar_cx + 0.32, counter_y + 0.34, bar_cz - 0.06),
            (bar_cx + 0.36, counter_y, bar_cz - 0.14),
        ],
        fillet_radius=0.08,
        corner_subdivs=5,
    )
    steel_parts = [make_swept_tube(arch_pts, radius=0.018, radial_segments=8)]
    cyan_parts = []
    orange_parts = []

    bulb_prof = [(0.0, 0.0), (0.038, 0.005), (0.052, 0.035), (0.048, 0.075), (0.024, 0.105), (0.014, 0.135), (0.0, 0.140)]
    for gx_off in [-0.22, 0.0, 0.22]:
        gx = bar_cx + gx_off
        # Nozzle tap & signal-orange valve
        steel_parts.append(make_cylinder(0.012, 0.009, 0.08, center=(gx, counter_y + 0.29, bar_cz - 0.06), segments=8, axis="y"))
        orange_parts.append(make_beveled_box((0.028, 0.045, 0.035), center=(gx, counter_y + 0.36, bar_cz - 0.04), bevel=0.005))
        # Magnetic coaster ring & lathed zero-G bulb sipper glass
        steel_parts.append(make_cylinder(0.055, 0.060, 0.014, center=(gx, counter_y + 0.007, bar_cz + 0.08), segments=12, axis="y"))
        cyan_parts.append(make_cylinder(0.046, 0.048, 0.018, center=(gx, counter_y + 0.009, bar_cz + 0.08), segments=12, axis="y"))
        cyan_parts.append(make_lathe_dome(bulb_prof, center=(gx, counter_y + 0.016, bar_cz + 0.08), segments=10, subdivide_profile=1))

    oled_screen = make_quad_panel(
        (bar_cx - 0.42, counter_y + 0.02, bar_cz - 0.18),
        (bar_cx + 0.42, counter_y + 0.02, bar_cz - 0.18),
        (bar_cx + 0.42, counter_y + 0.36, bar_cz - 0.26),
        (bar_cx - 0.42, counter_y + 0.36, bar_cz - 0.26),
    )

    return (
        merge_geometries(steel_parts),
        merge_geometries(cyan_parts),
        merge_geometries(orange_parts),
        oled_screen,
    )


def make_botanical_decanter_tower_internals(tx: float, tz: float = -0.10):
    """
    Builds Part 2 inside the Translucent Zero-G Botanical & Decanter Tower:
    - Top tier (Y = 1.38m..1.90m): 4 Glowing Cylindrical & Spherical Zero-G Infusion Decanters
      (Cyan, UV-Violet, Amber liquid cores) with Machined-Steel Dispensing Manifolds & Signal-Orange Valves
    - Middle tier (Y = 0.88m..1.30m): Living Aeroponic Botanical Garnish Trough (foliage_aeroponic_herbs.png)
      under a #7B5CFF UV-Violet Grow Bar
    - Bottom tier (Y = 0.22m..0.80m): Chilled Reserve Carafe Rack
    - Enclosed by alphaMode: "BLEND" Translucent Sapphire-Tinted Glass (glass_lounge_bar_translucent.png)
    Returns: (cyan_decanters, uv_decanters_and_growbar, amber_decanters, herbs_foliage, steel_manifolds, orange_valves, tower_glass)
    """
    carafe_prof = [(0.0, 0.0), (0.055, 0.01), (0.072, 0.10), (0.068, 0.24), (0.036, 0.34), (0.028, 0.40), (0.0, 0.41)]
    cyan_parts = [
        make_lathe_dome(carafe_prof, center=(tx - 0.22, 1.40, tz), segments=10, subdivide_profile=1),
        make_lathe_dome(carafe_prof, center=(tx + 0.08, 1.40, tz), segments=10, subdivide_profile=1),
        # Lower chilled reserve carafes
        make_cylinder(0.055, 0.055, 0.34, center=(tx - 0.16, 0.44, tz), segments=10, axis="y"),
        make_cylinder(0.055, 0.055, 0.34, center=(tx + 0.16, 0.44, tz), segments=10, axis="y"),
    ]
    uv_parts = [
        make_lathe_dome(carafe_prof, center=(tx - 0.07, 1.40, tz), segments=10, subdivide_profile=1),
        # UV-violet grow bar above the aeroponic herb trough
        make_beveled_box((0.58, 0.025, 0.06), center=(tx, 1.26, tz + 0.06), bevel=0.005),
    ]
    amber_parts = [
        make_lathe_dome(carafe_prof, center=(tx + 0.23, 1.40, tz), segments=10, subdivide_profile=1),
        make_cylinder(0.055, 0.055, 0.34, center=(tx, 0.44, tz), segments=10, axis="y"),
    ]

    # Living aeroponic botanical mint/herb garnish bed (Y = 0.92..1.08m)
    herbs = merge_geometries([
        make_sculpted_cushion((0.26, 0.14, 0.24), center=(tx - 0.15, 1.00, tz + 0.02), res=(4, 3, 4), roundness=0.45, belly_puff=0.06, crease_freq=0),
        make_sculpted_cushion((0.26, 0.15, 0.24), center=(tx + 0.15, 1.00, tz + 0.02), res=(4, 3, 4), roundness=0.45, belly_puff=0.06, crease_freq=0),
    ])

    steel_parts = [
        make_beveled_box((0.62, 0.035, 0.10), center=(tx, 1.84, tz), bevel=0.008),
        make_beveled_box((0.62, 0.04, 0.32), center=(tx, 0.90, tz + 0.02), bevel=0.008),
    ]
    orange_parts = [
        make_cylinder(0.022, 0.022, 0.04, center=(tx - 0.22, 1.84, tz + 0.06), segments=8, axis="z"),
        make_cylinder(0.022, 0.022, 0.04, center=(tx + 0.23, 1.84, tz + 0.06), segments=8, axis="z"),
    ]

    # Translucent front & side glass panes enclosing the Decanter & Botanical Tower
    tower_glass = merge_geometries([
        make_quad_panel((tx - 0.34, 0.18, tz + 0.24), (tx + 0.34, 0.18, tz + 0.24), (tx + 0.34, 1.94, tz + 0.24), (tx - 0.34, 1.94, tz + 0.24)),
        make_quad_panel((tx - 0.34, 0.92, tz - 0.20), (tx - 0.34, 0.92, tz + 0.24), (tx - 0.34, 1.94, tz + 0.24), (tx - 0.34, 1.94, tz - 0.20)),
    ])

    return (
        merge_geometries(cyan_parts),
        merge_geometries(uv_parts),
        merge_geometries(amber_parts),
        herbs,
        merge_geometries(steel_parts),
        merge_geometries(orange_parts),
        tower_glass,
    )


# ==============================================================================
# CANDIDATE 01: AEGIS-7 OCTAGONAL CELESTIAL BAR & ILLUMINATED CARAFE ARCH (`lounge_bar_r1_01.glb`)
# Dimensions: 2.25m W x 1.35m D x 2.05m H
# ==============================================================================
def build_01_octagonal_celestial_bar_arch(mats):
    sm = []
    hull = [
        make_beveled_box((2.25, 0.14, 1.35), center=(0.0, 0.07, 0.0), bevel=0.03),
        make_beveled_box((1.44, 0.80, 0.84), center=(-0.36, 0.50, 0.06), bevel=0.04),
        make_beveled_box((0.78, 1.90, 0.68), center=(0.70, 1.02, -0.12), bevel=0.035),
    ]
    add_part(sm, "Lounge01_OctagonalGunmetalChassis", merge_geometries(hull), mats["gunmetal"])

    cy_d, uv_d, am_d, herbs, st_d, or_d, gl_d = make_botanical_decanter_tower_internals(tx=0.70, tz=-0.08)
    st_a, cy_b, or_a, oled_b = make_bar_siphon_arch_and_bulb_glasses(bar_cx=-0.36, bar_cz=0.08, counter_y=0.94)
    nv1, ch1, st1, or1 = make_lounge_barstool(cx=-0.68, cz=0.46, seat_y=0.62)
    nv2, ch2, st2, or2 = make_lounge_barstool(cx=-0.04, cz=0.46, seat_y=0.62)

    white_parts = [
        make_beveled_box((1.52, 0.06, 0.92), center=(-0.36, 0.92, 0.06), bevel=0.02),
        make_beveled_box((0.70, 1.76, 0.06), center=(0.70, 1.04, -0.36), bevel=0.015),
    ]
    add_part(sm, "Lounge01_AerospaceWhiteCounterAndNiches", merge_geometries(white_parts), mats["aero_white"])
    add_part(sm, "Lounge01_OrbitalNavyBarstoolCushions", merge_geometries([nv1, nv2]), mats["fabric_navy"])
    add_part(sm, "Lounge01_CharcoalArmrestAndStoolShells", merge_geometries([ch1, ch2, make_beveled_box((1.48, 0.04, 0.08), center=(-0.36, 0.95, 0.50), bevel=0.012)]), mats["fabric_charcoal"])
    add_part(sm, "Lounge01_AeroponicHerbGarnishTrough", herbs, mats["foliage_herbs"])
    add_part(sm, "Lounge01_MachinedSteelSiphonArchAndPedestals", merge_geometries([st_d, st_a, st1, st2]), mats["steel_machined"])
    add_part(sm, "Lounge01_SignalOrangeInfusionValves", merge_geometries([or_d, or_a, or1, or2]), mats["accent_orange"])

    add_part(sm, "Lounge01_OLEDCelestialStarMapConsole", oled_b, mats["oled_celestial"])
    add_part(sm, "Lounge01_CyanDecantersAndBulbGlasses", merge_geometries([cy_d, cy_b]), mats["led_cyan"])
    add_part(sm, "Lounge01_UVVioletDecanterAndGrowBar", uv_d, mats["led_uv"])
    add_part(sm, "Lounge01_AmberDecantersAndFootrailGlow", merge_geometries([am_d, make_beveled_box((1.40, 0.024, 0.04), center=(-0.36, 0.16, 0.48), bevel=0.004)]), mats["led_amber"])
    add_part(sm, "Lounge01_TranslucentDecanterTowerGlass", gl_d, mats["glass_lounge"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "lounge_bar_r1_01.glb"), sm, root_name="LoungeBarR1_01_OctagonalCelestialBar")


# ==============================================================================
# CANDIDATE 02: DUAL-ZONE SPLIT CELESTIAL BEVERAGE BAR & ILLUMINATED ZERO-G DECANTER TOWER (`lounge_bar_r1_02.glb`)
# Dimensions: 2.35m W x 1.35m D x 2.05m H (Signature 65% / 35% Asymmetric Split-Bay Sibling!)
# ==============================================================================
def build_02_dual_zone_split_celestial_bar_decanter_tower(mats):
    sm = []
    # 1. Signature 65% / 35% Asymmetric Split-Bay Chassis:
    # Left Bay (65% width, 1.53m wide): Celestial Beverage Bar Counter (Y = 0.94m) + 2 Pivoting Barstools
    # Right Bay (35% width, 0.82m wide): Full-height 3-tier Translucent Zero-G Botanical & Decanter Tower (Y = 0.0m..2.05m)
    hull = [
        make_beveled_box((2.35, 0.14, 1.35), center=(0.0, 0.07, 0.0), bevel=0.03),
        make_beveled_box((1.48, 0.78, 0.82), center=(-0.40, 0.48, 0.04), bevel=0.04),
        # Right 3-tier Decanter Tower frame with open front & side windows
        make_beveled_box((0.82, 0.12, 0.76), center=(0.76, 1.99, -0.08), bevel=0.025),
        make_beveled_box((0.82, 1.88, 0.10), center=(0.76, 1.04, -0.42), bevel=0.02),
        make_beveled_box((0.10, 1.88, 0.72), center=(1.12, 1.04, -0.08), bevel=0.02),
        make_beveled_box((0.10, 1.88, 0.72), center=(0.40, 1.04, -0.08), bevel=0.02),
    ]
    add_part(sm, "Lounge02_SplitBayGunmetalChassis", merge_geometries(hull), mats["gunmetal"])

    cy_d, uv_d, am_d, herbs, st_d, or_d, gl_d = make_botanical_decanter_tower_internals(tx=0.76, tz=-0.08)
    st_a, cy_b, or_a, oled_b = make_bar_siphon_arch_and_bulb_glasses(bar_cx=-0.40, bar_cz=0.06, counter_y=0.94)
    nv1, ch1, st1, or1 = make_lounge_barstool(cx=-0.76, cz=0.46, seat_y=0.62)
    nv2, ch2, st2, or2 = make_lounge_barstool(cx=-0.06, cz=0.46, seat_y=0.62)

    white_parts = [
        make_beveled_box((1.54, 0.06, 0.90), center=(-0.40, 0.92, 0.06), bevel=0.022),
        make_beveled_box((0.70, 0.04, 0.62), center=(0.76, 1.36, -0.08), bevel=0.012),
        make_beveled_box((0.70, 0.04, 0.62), center=(0.76, 0.82, -0.08), bevel=0.012),
    ]
    add_part(sm, "Lounge02_AerospaceWhiteCounterAndTowerShelves", merge_geometries(white_parts), mats["aero_white"])
    add_part(sm, "Lounge02_OrbitalNavyBarstoolCushions", merge_geometries([nv1, nv2]), mats["fabric_navy"])
    add_part(sm, "Lounge02_CharcoalArmrestBolsterAndStools", merge_geometries([ch1, ch2, make_beveled_box((1.50, 0.04, 0.08), center=(-0.40, 0.95, 0.49), bevel=0.012)]), mats["fabric_charcoal"])
    add_part(sm, "Lounge02_AeroponicHerbGarnishTrough", herbs, mats["foliage_herbs"])
    add_part(sm, "Lounge02_MachinedSteelSiphonArchAndPedestals", merge_geometries([st_d, st_a, st1, st2]), mats["steel_machined"])
    add_part(sm, "Lounge02_SignalOrangePressureValvesAndLocks", merge_geometries([or_d, or_a, or1, or2]), mats["accent_orange"])

    add_part(sm, "Lounge02_OLEDCelestialStarMapConsole", oled_b, mats["oled_celestial"])
    add_part(sm, "Lounge02_CyanInfusionDecantersAndBulbGlasses", merge_geometries([cy_d, cy_b]), mats["led_cyan"])
    add_part(sm, "Lounge02_UVVioletDecanterAndGrowBar", uv_d, mats["led_uv"])
    add_part(
        sm,
        "Lounge02_AmberDecantersAndFootrailGlow",
        merge_geometries([
            am_d,
            make_beveled_box((1.44, 0.024, 0.04), center=(-0.40, 0.16, 0.46), bevel=0.004),
            make_beveled_box((0.72, 0.024, 0.04), center=(0.76, 0.16, 0.28), bevel=0.004),
        ]),
        mats["led_amber"],
    )
    add_part(sm, "Lounge02_TranslucentDecanterTowerGlass", gl_d, mats["glass_lounge"])

    out_p = os.path.join(OUT_GLB_DIR, "lounge_bar_r1_02.glb")
    info = center_and_export_glb(out_p, sm, root_name="LoungeBarR1_02_DualZoneSplitCelestialBar")

    for w_alias in [
        "lounge_bar_winner_01_split_celestial_decanter.glb",
        "lounge_bar_winner_01_dual_zone_celestial_bar.glb",
        "lounge_bar_winner_01_celestial_beverage_bar.glb",
        "lounge_bar_winner_01.glb",
    ]:
        shutil.copyfile(out_p, os.path.join(WINNERS_DIR, w_alias))
    return info


# ==============================================================================
# CANDIDATE 03: ROTARY ZERO-G SPHERE DISPENSER & CURVED STARGAZER BAR (`lounge_bar_r1_03.glb`)
# Dimensions: 2.28m W x 1.38m D x 2.05m H
# ==============================================================================
def build_03_rotary_sphere_dispenser_bar(mats):
    sm = []
    hull = [
        make_beveled_box((2.28, 0.14, 1.38), center=(0.0, 0.07, 0.0), bevel=0.03),
        make_beveled_box((1.46, 0.78, 0.84), center=(-0.36, 0.48, 0.04), bevel=0.04),
        make_beveled_box((0.78, 1.90, 0.72), center=(0.72, 1.02, -0.10), bevel=0.035),
    ]
    add_part(sm, "Lounge03_CurvedStargazerGunmetalHull", merge_geometries(hull), mats["gunmetal"])

    cy_d, uv_d, am_d, herbs, st_d, or_d, gl_d = make_botanical_decanter_tower_internals(tx=0.72, tz=-0.08)
    st_a, cy_b, or_a, oled_b = make_bar_siphon_arch_and_bulb_glasses(bar_cx=-0.36, bar_cz=0.06, counter_y=0.94)
    nv1, ch1, st1, or1 = make_lounge_barstool(cx=-0.70, cz=0.48, seat_y=0.62)
    nv2, ch2, st2, or2 = make_lounge_barstool(cx=-0.04, cz=0.48, seat_y=0.62)

    # Central cylindrical translucent levitation column
    lev_col = make_cylinder(0.22, 0.22, 0.92, center=(-0.36, 1.44, -0.22), segments=16, axis="y")

    add_part(sm, "Lounge03_AerospaceWhiteCounter", make_beveled_box((1.52, 0.06, 0.90), center=(-0.36, 0.92, 0.04), bevel=0.02), mats["aero_white"])
    add_part(sm, "Lounge03_OrbitalNavyBarstools", merge_geometries([nv1, nv2]), mats["fabric_navy"])
    add_part(sm, "Lounge03_CharcoalBolsters", merge_geometries([ch1, ch2]), mats["fabric_charcoal"])
    add_part(sm, "Lounge03_AeroponicHerbs", herbs, mats["foliage_herbs"])
    add_part(sm, "Lounge03_MachinedSteelSiphonAndPedestals", merge_geometries([st_d, st_a, st1, st2]), mats["steel_machined"])
    add_part(sm, "Lounge03_SignalOrangeValves", merge_geometries([or_d, or_a, or1, or2]), mats["accent_orange"])

    add_part(sm, "Lounge03_OLEDCelestialConsole", oled_b, mats["oled_celestial"])
    add_part(sm, "Lounge03_CyanSpheresAndGlasses", merge_geometries([cy_d, cy_b]), mats["led_cyan"])
    add_part(sm, "Lounge03_UVVioletGrowBar", uv_d, mats["led_uv"])
    add_part(sm, "Lounge03_AmberDecantersAndFootrail", merge_geometries([am_d, make_beveled_box((1.42, 0.024, 0.04), center=(-0.36, 0.16, 0.48), bevel=0.004)]), mats["led_amber"])
    add_part(sm, "Lounge03_TranslucentLevitationColumnAndTower", merge_geometries([gl_d, lev_col]), mats["glass_lounge"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "lounge_bar_r1_03.glb"), sm, root_name="LoungeBarR1_03_RotarySphereDispenserBar")


# ==============================================================================
# CANDIDATE 04: CANTILEVERED CANOPY LOUNGE ISLAND & BOTANICAL MIXOLOGY BAY (`lounge_bar_r1_04.glb`)
# Dimensions: 2.32m W x 1.36m D x 2.08m H
# ==============================================================================
def build_04_cantilevered_canopy_lounge_island(mats):
    sm = []
    hull = [
        make_beveled_box((2.32, 0.14, 1.36), center=(0.0, 0.07, 0.0), bevel=0.03),
        make_beveled_box((1.48, 0.78, 0.82), center=(-0.38, 0.48, 0.04), bevel=0.04),
        make_beveled_box((0.80, 1.92, 0.70), center=(0.74, 1.04, -0.10), bevel=0.035),
        # Cantilevered overhead canopy frame
        make_beveled_box((2.24, 0.08, 0.92), center=(0.0, 2.02, 0.04), bevel=0.02),
    ]
    add_part(sm, "Lounge04_CanopyCarbonSlateChassis", merge_geometries(hull), mats["carbon_slate"])

    cy_d, uv_d, am_d, herbs, st_d, or_d, gl_d = make_botanical_decanter_tower_internals(tx=0.74, tz=-0.08)
    st_a, cy_b, or_a, oled_b = make_bar_siphon_arch_and_bulb_glasses(bar_cx=-0.38, bar_cz=0.06, counter_y=0.94)
    nv1, ch1, st1, or1 = make_lounge_barstool(cx=-0.72, cz=0.46, seat_y=0.62)
    nv2, ch2, st2, or2 = make_lounge_barstool(cx=-0.04, cz=0.46, seat_y=0.62)

    canopy_glass = make_quad_panel((-1.04, 1.98, -0.32), (0.34, 1.98, -0.32), (0.34, 1.98, 0.46), (-1.04, 1.98, 0.46))

    add_part(sm, "Lounge04_AerospaceWhiteCounter", make_beveled_box((1.54, 0.06, 0.88), center=(-0.38, 0.92, 0.04), bevel=0.02), mats["aero_white"])
    add_part(sm, "Lounge04_OrbitalNavyBarstools", merge_geometries([nv1, nv2]), mats["fabric_navy"])
    add_part(sm, "Lounge04_CharcoalBolsters", merge_geometries([ch1, ch2]), mats["fabric_charcoal"])
    add_part(sm, "Lounge04_AeroponicHerbs", herbs, mats["foliage_herbs"])
    add_part(sm, "Lounge04_MachinedSteelSiphonAndPedestals", merge_geometries([st_d, st_a, st1, st2]), mats["steel_machined"])
    add_part(sm, "Lounge04_SignalOrangeValves", merge_geometries([or_d, or_a, or1, or2]), mats["accent_orange"])

    add_part(sm, "Lounge04_OLEDCelestialConsole", oled_b, mats["oled_celestial"])
    add_part(sm, "Lounge04_CyanDecantersAndGlasses", merge_geometries([cy_d, cy_b]), mats["led_cyan"])
    add_part(sm, "Lounge04_UVVioletGrowBar", uv_d, mats["led_uv"])
    add_part(sm, "Lounge04_AmberDecantersAndFootrail", merge_geometries([am_d, make_beveled_box((1.44, 0.024, 0.04), center=(-0.38, 0.16, 0.46), bevel=0.004)]), mats["led_amber"])
    add_part(sm, "Lounge04_TranslucentCanopyAndTowerGlass", merge_geometries([gl_d, canopy_glass]), mats["glass_lounge"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "lounge_bar_r1_04.glb"), sm, root_name="LoungeBarR1_04_CantileveredCanopyIsland")


# ==============================================================================
# CANDIDATE 05: SUNKEN PIT PERIMETER BAR & DUAL-TAP CRYO-CHILLER STATION (`lounge_bar_r1_05.glb`)
# Dimensions: 2.38m W x 1.35m D x 2.02m H
# ==============================================================================
def build_05_sunken_pit_cryo_chiller_bar(mats):
    sm = []
    hull = [
        make_beveled_box((2.38, 0.14, 1.35), center=(0.0, 0.07, 0.0), bevel=0.03),
        make_beveled_box((1.50, 0.78, 0.82), center=(-0.40, 0.48, 0.04), bevel=0.04),
        make_beveled_box((0.82, 1.88, 0.70), center=(0.76, 1.00, -0.10), bevel=0.035),
    ]
    add_part(sm, "Lounge05_CryoChillerGunmetalHull", merge_geometries(hull), mats["gunmetal"])

    cy_d, uv_d, am_d, herbs, st_d, or_d, gl_d = make_botanical_decanter_tower_internals(tx=0.76, tz=-0.08)
    st_a, cy_b, or_a, oled_b = make_bar_siphon_arch_and_bulb_glasses(bar_cx=-0.40, bar_cz=0.06, counter_y=0.94)
    nv1, ch1, st1, or1 = make_lounge_barstool(cx=-0.74, cz=0.46, seat_y=0.62)
    nv2, ch2, st2, or2 = make_lounge_barstool(cx=-0.06, cz=0.46, seat_y=0.62)

    add_part(sm, "Lounge05_AerospaceWhiteCounter", make_beveled_box((1.56, 0.06, 0.88), center=(-0.40, 0.92, 0.04), bevel=0.02), mats["aero_white"])
    add_part(sm, "Lounge05_OrbitalNavyBarstools", merge_geometries([nv1, nv2]), mats["fabric_navy"])
    add_part(sm, "Lounge05_CharcoalBolsters", merge_geometries([ch1, ch2]), mats["fabric_charcoal"])
    add_part(sm, "Lounge05_AeroponicHerbs", herbs, mats["foliage_herbs"])
    add_part(sm, "Lounge05_MachinedSteelSiphonAndPedestals", merge_geometries([st_d, st_a, st1, st2]), mats["steel_machined"])
    add_part(sm, "Lounge05_SignalOrangeValves", merge_geometries([or_d, or_a, or1, or2]), mats["accent_orange"])

    add_part(sm, "Lounge05_OLEDCelestialConsole", oled_b, mats["oled_celestial"])
    add_part(sm, "Lounge05_CyanCryoDrumsAndGlasses", merge_geometries([cy_d, cy_b]), mats["led_cyan"])
    add_part(sm, "Lounge05_UVVioletGrowBar", uv_d, mats["led_uv"])
    add_part(sm, "Lounge05_AmberDecantersAndFootrail", merge_geometries([am_d, make_beveled_box((1.46, 0.024, 0.04), center=(-0.40, 0.16, 0.46), bevel=0.004)]), mats["led_amber"])
    add_part(sm, "Lounge05_TranslucentCryoTowerGlass", gl_d, mats["glass_lounge"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "lounge_bar_r1_05.glb"), sm, root_name="LoungeBarR1_05_SunkenPitCryoChillerBar")


# ==============================================================================
# ROOM 08 AUXILIARY PROP (`lounge_viewing_pit_set.glb`) & SHELL (`room_08_shell.glb`)
# ==============================================================================
def build_lounge_viewing_pit_set(mats):
    """
    Builds Central Sunken Viewing Pit & Holo-Table Set (lounge_viewing_pit_set.glb):
    2.80m W x 2.40m D x 0.72m H chamfered carbon-slate & orbital-navy conversation lounge grouping
    positioned directly in front of the North Deep-Space window: two curved low-G orbital-navy lounge sofas
    flanking a low octagonal brushed-steel & translucent-glass holo-chess coffee table with recessed
    amber (#FF9500) step-down perimeter strips.
    """
    sm = []
    slate_base = [
        make_beveled_box((2.80, 0.08, 2.40), center=(0.0, 0.04, 0.0), bevel=0.02),
        make_beveled_box((0.68, 0.28, 2.16), center=(-0.98, 0.22, 0.0), bevel=0.03),
        make_beveled_box((0.68, 0.28, 2.16), center=(0.98, 0.22, 0.0), bevel=0.03),
        make_beveled_box((0.88, 0.34, 1.18), center=(0.0, 0.24, 0.0), bevel=0.03),
    ]
    add_part(sm, "ViewingPit_CarbonSlatePlinthAndTableBase", merge_geometries(slate_base), mats["carbon_slate"])

    navy_sofas = [
        make_sculpted_cushion((0.62, 0.12, 2.08), center=(-0.94, 0.42, 0.0), res=(5, 3, 6), roundness=0.36, belly_puff=0.04, tuft_grid=(2, 4), tuft_depth=0.012, crease_freq=0),
        make_sculpted_cushion((0.62, 0.12, 2.08), center=(0.94, 0.42, 0.0), res=(5, 3, 6), roundness=0.36, belly_puff=0.04, tuft_grid=(2, 4), tuft_depth=0.012, crease_freq=0),
        make_sculpted_cushion((0.14, 0.28, 2.06), center=(-1.22, 0.58, 0.0), res=(3, 4, 6), roundness=0.36, belly_puff=0.04, tuft_grid=(1, 4), tuft_depth=0.010, crease_freq=0),
        make_sculpted_cushion((0.14, 0.28, 2.06), center=(1.22, 0.58, 0.0), res=(3, 4, 6), roundness=0.36, belly_puff=0.04, tuft_grid=(1, 4), tuft_depth=0.010, crease_freq=0),
    ]
    add_part(sm, "ViewingPit_OrbitalNavySofaCushions", merge_geometries(navy_sofas), mats["fabric_navy"])

    steel_trim = [
        make_beveled_box((0.94, 0.04, 1.24), center=(0.0, 0.43, 0.0), bevel=0.012),
    ]
    add_part(sm, "ViewingPit_MachinedSteelTableBezel", merge_geometries(steel_trim), mats["steel_machined"])

    amber_strips = [
        make_beveled_box((2.64, 0.022, 0.04), center=(0.0, 0.085, 1.16), bevel=0.004),
        make_beveled_box((2.64, 0.022, 0.04), center=(0.0, 0.085, -1.16), bevel=0.004),
    ]
    add_part(sm, "ViewingPit_AmberPerimeterStrips", merge_geometries(amber_strips), mats["led_amber"])
    add_part(sm, "ViewingPit_CyanHoloChessCore", make_cylinder(0.18, 0.22, 0.06, center=(0.0, 0.48, 0.0), segments=14, axis="y"), mats["led_cyan"])

    table_glass = make_quad_panel((-0.42, 0.46, -0.56), (0.42, 0.46, -0.56), (0.42, 0.46, 0.56), (-0.42, 0.46, 0.56))
    add_part(sm, "ViewingPit_TranslucentHoloTableGlass", table_glass, mats["glass_lounge"])

    p_main = os.path.join(WINNERS_DIR, "lounge_viewing_pit_set.glb")
    info = center_and_export_glb(p_main, sm, root_name="LoungeViewingPitSet")
    for dst in [
        os.path.join(OUT_GLB_DIR, "lounge_viewing_pit_set.glb"),
        os.path.join(ROOMS_DIR, "lounge_viewing_pit_set.glb"),
        "/workspace/game-project/assets/glb/lounge_viewing_pit_set.glb",
    ]:
        shutil.copyfile(p_main, dst)
    print(f"[lounge_viewing_pit] Exported {p_main} ({info['triangles']} tris)")
    return info


def build_room_08_observation_lounge_shell(mats):
    """
    Builds Room 08 — Observation Lounge & Zero-G Recreation Deck Shell (8.0m W x 9.0m D x 3.6m H):
    - 5 Repeating 45° Chamfered Octagonal Titanium Ribs (Z = -4.2, -2.1, 0.0, +2.1, +4.2)
    - Floor-to-Ceiling Faceted Deep-Space Observation Dome (Z = -4.45m, X = -3.5..+3.5m, Y = 0.25..3.35m)
      with open cutouts and alphaMode: "BLEND" translucent glass
    - East Inner-Hull Cylinder Gallery Window (X = +3.95m, Z = -2.2..+1.8m)
    """
    sm = []
    slate_deck = [
        make_beveled_box((8.00, 0.06, 9.00), center=(0.0, 0.03, 0.0), bevel=0.015),
        # West solid stargazer alcove wall & East wall with open Cylinder Gallery Window (Z = -2.2..+1.8m, Y = 0.85..2.85m)
        make_beveled_box((0.12, 3.48, 8.90), center=(-3.94, 1.80, 0.0), bevel=0.02),
        make_beveled_box((0.12, 0.82, 8.90), center=(3.94, 0.44, 0.0), bevel=0.02),
        make_beveled_box((0.12, 0.68, 8.90), center=(3.94, 3.22, 0.0), bevel=0.02),
        make_beveled_box((0.12, 2.04, 2.60), center=(3.94, 1.85, 3.15), bevel=0.02),
        make_beveled_box((0.12, 2.04, 2.20), center=(3.94, 1.85, -3.35), bevel=0.02),
        # North floor-to-ceiling observation dome low sill & upper header (open window Y = 0.25..3.35m, X = -3.5..+3.5m)
        make_beveled_box((7.90, 0.24, 0.14), center=(0.0, 0.14, -4.43), bevel=0.02),
        make_beveled_box((7.90, 0.24, 0.14), center=(0.0, 3.46, -4.43), bevel=0.02),
    ]
    add_part(sm, "Room08_CarbonSlateDeckAndBulkheads", merge_geometries(slate_deck), mats["carbon_slate"])

    gunmetal_ribs = [
        make_beveled_box((8.00, 0.06, 9.00), center=(0.0, 3.57, 0.0), bevel=0.015),
    ]
    for z_rib in [-4.2, -2.1, 0.0, 2.1, 4.2]:
        gunmetal_ribs.extend([
            make_beveled_box((0.20, 3.48, 0.22), center=(-3.84, 1.80, z_rib), bevel=0.03),
            make_beveled_box((0.20, 3.48, 0.22), center=(3.84, 1.80, z_rib), bevel=0.03),
            make_beveled_box((7.86, 0.20, 0.22), center=(0.0, 3.44, z_rib), bevel=0.03),
            transform_geom(make_beveled_box((0.76, 0.18, 0.22), bevel=0.02), translate=(-3.50, 3.16, z_rib), rot_xyz_deg=(0.0, 0.0, 45.0)),
            transform_geom(make_beveled_box((0.76, 0.18, 0.22), bevel=0.02), translate=(3.50, 3.16, z_rib), rot_xyz_deg=(0.0, 0.0, -45.0)),
        ])
    # North floor-to-ceiling observation dome mullions
    for xm in [-3.50, -1.75, 0.0, 1.75, 3.50]:
        gunmetal_ribs.append(make_beveled_box((0.12, 3.12, 0.16), center=(xm, 1.80, -4.42), bevel=0.02))
    add_part(sm, "Room08_OctagonalTitaniumRibsAndDomeMullions", merge_geometries(gunmetal_ribs), mats["gunmetal"])

    uv_coves = [
        make_beveled_box((0.05, 0.03, 8.20), center=(-2.65, 3.32, 0.0), bevel=0.005),
        make_beveled_box((0.05, 0.03, 8.20), center=(2.65, 3.32, 0.0), bevel=0.005),
    ]
    add_part(sm, "Room08_UVVioletMoodCoveStrips", merge_geometries(uv_coves), mats["led_uv"])

    amber_strips = [
        make_beveled_box((0.04, 0.014, 8.00), center=(-1.65, 0.066, 0.0), bevel=0.003),
        make_beveled_box((0.04, 0.014, 8.00), center=(1.65, 0.066, 0.0), bevel=0.003),
    ]
    add_part(sm, "Room08_AmberDeckMoodStrips", merge_geometries(amber_strips), mats["led_amber"])

    viewports = [
        # North floor-to-ceiling Deep-Space observation dome
        make_quad_panel((-3.50, 0.25, -4.42), (3.50, 0.25, -4.42), (3.50, 3.35, -4.42), (-3.50, 3.35, -4.42)),
        # East inner-hull O'Neill Cylinder gallery window
        make_quad_panel((3.92, 0.85, -2.20), (3.92, 0.85, 1.80), (3.92, 2.85, 1.80), (3.92, 2.85, -2.20)),
    ]
    add_part(sm, "Room08_TranslucentStargazerViewports", merge_geometries(viewports), mats["glass_lounge"])

    p_main = os.path.join(ROOMS_DIR, "room_08_shell.glb")
    info = center_and_export_glb(p_main, sm, root_name="Room08_ObservationLoungeShell")
    for dst in [
        os.path.join(ROOMS_DIR, "room_08_lounge_shell.glb"),
        os.path.join(ROOMS_DIR, "room_08_observation_lounge_shell.glb"),
        "/workspace/game-project/assets/glb/room_08_lounge_shell.glb",
        "/workspace/game-project/assets/glb/room_08_shell.glb",
    ]:
        shutil.copyfile(p_main, dst)
    print(f"[room_08_shell] Exported {p_main} and aliases ({info['triangles']} tris)")
    return info


def build_all_lounge_round1():
    mats = get_lounge_materials()
    builders = [
        build_01_octagonal_celestial_bar_arch,
        build_02_dual_zone_split_celestial_bar_decanter_tower,
        build_03_rotary_sphere_dispenser_bar,
        build_04_cantilevered_canopy_lounge_island,
        build_05_sunken_pit_cryo_chiller_bar,
    ]
    results = []
    for fn in builders:
        info = fn(mats)
        fname = os.path.basename(info["filepath"])
        dims = info["dimensions"]
        print(
            f"[lounge_r1] Built {fname:24s} | {dims[0]:.2f}m W x {dims[2]:.2f}m D x {dims[1]:.2f}m H | "
            f"verts={info['vertices']:4d} | tris={info['triangles']:4d} | min_y={info['min'][1]:.5f}"
        )
        results.append(info)
    with open(os.path.join(OUT_GLB_DIR, "lounge_r1_manifest.json"), "w") as f:
        json.dump(results, f, indent=2)

    build_lounge_viewing_pit_set(mats)
    build_room_08_observation_lounge_shell(mats)
    return results


if __name__ == "__main__":
    build_all_lounge_round1()
