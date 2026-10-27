#!/usr/bin/env python3
"""
Builds all 5 Round-1 Hard Sci-Fi Room 03 Hero Asset (Ration & Beverage Synthesizer Bank) .glb models:
  /workspace/game-project/assets/glb/galley_round1/galley_synth_r1_01.glb .. galley_synth_r1_05.glb
Plus pre-staged Winner #02 copies:
  /workspace/game-project/assets/glb/winners/galley_synth_winner_01_dual_zone_dispenser.glb
  /workspace/game-project/assets/glb/winners/galley_synth_winner_01_split_ration_tower.glb
Plus Custom Companion Mess Booth & Cantilevered Table:
  /workspace/game-project/assets/glb/rooms/mess_dining_booth.glb
  /workspace/game-project/assets/glb/galley_round1/mess_dining_booth.glb
  /workspace/game-project/assets/glb/mess_dining_booth.glb
Plus Room 03 Architectural Shell (7.0m W x 8.0m D x 3.2m H):
  /workspace/game-project/assets/glb/rooms/room_03_shell.glb
  /workspace/game-project/assets/glb/rooms/room_03_mess_shell.glb
  /workspace/game-project/assets/glb/rooms/room_03_mess_galley_shell.glb
  /workspace/game-project/assets/glb/room_03_shell.glb
  /workspace/game-project/assets/glb/room_03_mess_shell.glb
  /workspace/game-project/assets/glb/room_03_mess_galley_shell.glb

Follows /workspace/game-project/design/galley_round1/galley_synth_r1_spec.md ("Aegis-7 Standard"):
- Bottom-center (0.0, 0.0, 0.0) floor pivot (min_y == 0.0000, centered X and Z), front facing +Z
- Polygon budget: 3,200 - 5,500 triangles per candidate
- Mapped cleanly to Sloane's textures in /workspace/game-project/assets/textures/galley_round1/
- Mandatory 4-Part 3D Galley Synthesizer Kit in every candidate:
  1. 45° Chamfered Bulkhead Housing & Brushed-Steel Serving Counter Deck (Y ~ 0.88m) with magnetic meal-tray bays & cyan cup rings
  2. Translucent Thermal Synthesis & Ration Dispensing Chambers (glass_synth_chamber_translucent.png, alphaMode: "BLEND", alpha ~ 0.19)
     enclosing 3D compartmentalized aerospace-white meal trays with ration domes/blocks and 3D cylindrical protein/amino canisters
  3. Dual-Nozzle Hydration / Espresso Tap Arch + Widescreen OLED Nutri-Telemetry Console (oled_nutri_synthesizer.png) + 3D zero-G flasks
  4. Integrated Living Aeroponic Culinary Herb Strip (foliage_aeroponic_herbs.png) under UV-violet (#7B5CFF) & cyan (#00E5FF) grow bar
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
    make_chamfered_aperture_ring,
)
from corridor_door_round1_generator import make_portal_oct_ring

TEX_GALLEY_DIR = "/workspace/game-project/assets/textures/galley_round1"
OUT_GLB_DIR = "/workspace/game-project/assets/glb/galley_round1"
ROOMS_GLB_DIR = "/workspace/game-project/assets/glb/rooms"
WINNERS_GLB_DIR = "/workspace/game-project/assets/glb/winners"

os.makedirs(OUT_GLB_DIR, exist_ok=True)
os.makedirs(ROOMS_GLB_DIR, exist_ok=True)
os.makedirs(WINNERS_GLB_DIR, exist_ok=True)


def tex_gl(fname: str) -> str:
    return os.path.join(TEX_GALLEY_DIR, fname)


def get_galley_materials():
    return {
        "gunmetal": PBRMaterialDef(
            name="Mat_Titanium_GunmetalHull",
            base_color=hex_rgba("#1A1E24"),
            metallic=0.78,
            roughness=0.34,
            texture_path=tex_gl("titanium_gunmetal_hull.png"),
        ),
        "aero_white": PBRMaterialDef(
            name="Mat_Composite_AerospaceWhite",
            base_color=hex_rgba("#D8DEE6"),
            metallic=0.08,
            roughness=0.28,
            texture_path=tex_gl("composite_aerospace_white.png"),
        ),
        "carbon_slate": PBRMaterialDef(
            name="Mat_Carbon_SlateFrame",
            base_color=hex_rgba("#282E38"),
            metallic=0.58,
            roughness=0.40,
            texture_path=tex_gl("carbon_slate_frame.png"),
        ),
        "steel_machined": PBRMaterialDef(
            name="Mat_Steel_MachinedGantry",
            base_color=hex_rgba("#88929E"),
            metallic=0.90,
            roughness=0.20,
            texture_path=tex_gl("steel_machined_gantry.png"),
        ),
        "pad_charcoal": PBRMaterialDef(
            name="Mat_Fabric_CharcoalFlightpad",
            base_color=hex_rgba("#242932"),
            metallic=0.00,
            roughness=0.78,
            texture_path=tex_gl("fabric_charcoal_flightpad.png"),
        ),
        "pad_navy": PBRMaterialDef(
            name="Mat_Fabric_OrbitalNavyPad",
            base_color=hex_rgba("#1D2C3C"),
            metallic=0.00,
            roughness=0.76,
            texture_path=tex_gl("fabric_orbital_navy_pad.png"),
        ),
        "accent_orange": PBRMaterialDef(
            name="Mat_Accent_SignalOrange",
            base_color=hex_rgba("#D95B26"),
            metallic=0.06,
            roughness=0.48,
            texture_path=tex_gl("accent_signal_orange.png"),
        ),
        "oled_nutri": PBRMaterialDef(
            name="Mat_OLED_NutriSynthesizer",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.10,
            roughness=0.14,
            emissive=(0.35, 0.90, 1.0),
            texture_path=tex_gl("oled_nutri_synthesizer.png"),
        ),
        "glass_chamber": PBRMaterialDef(
            name="Mat_Glass_SynthChamber_Translucent",
            base_color=(0.55, 0.88, 1.0, 0.19),
            metallic=0.10,
            roughness=0.08,
            emissive=(0.0, 0.14, 0.22),
            texture_path=tex_gl("glass_synth_chamber_translucent.png"),
            double_sided=True,
            alpha_mode="BLEND",
        ),
        "foliage_herbs": PBRMaterialDef(
            name="Mat_Foliage_AeroponicHerbs",
            base_color=hex_rgba("#2E5A36"),
            metallic=0.00,
            roughness=0.55,
            texture_path=tex_gl("foliage_aeroponic_herbs.png"),
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
            name="Mat_Emissive_UVGrowLED",
            base_color=hex_rgba("#7B5CFF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.55, 0.38, 1.0),
        ),
    }


# ==============================================================================
# SHARED 4-PART 3D GALLEY SYNTHESIZER KIT HELPERS
# ==============================================================================

def make_3d_meal_tray_with_rations(cx: float, cy: float, cz: float, scale: float = 1.0):
    """
    Builds a 3D compartmentalized aerospace-white meal tray with sculpted ration blocks/domes,
    thermal protein pouch, and machined-steel induction rack rails.
    Returns: (white_tray_geom, navy_pouch_geom, orange_ration_geom, steel_rack_geom, amber_heater_geom)
    """
    tw = 0.28 * scale
    td = 0.22 * scale
    white_parts = [
        # Base meal tray Rim & Divider ribs
        make_beveled_box((tw, 0.022, td), center=(cx, cy, cz), bevel=0.006),
        make_beveled_box((tw * 0.42, 0.036, td * 0.40), center=(cx - tw * 0.22, cy + 0.018, cz - td * 0.18), bevel=0.008),
        make_lathe_dome([(0.048 * scale, 0.0), (0.036 * scale, 0.022 * scale), (0.0, 0.034 * scale)], center=(cx + tw * 0.20, cy + 0.011, cz - td * 0.16), segments=10, subdivide_profile=1),
    ]
    navy_pouch = make_sculpted_cushion(
        (tw * 0.40, 0.028 * scale, td * 0.36),
        center=(cx - tw * 0.20, cy + 0.022, cz + td * 0.20),
        res=(3, 2, 3),
        roundness=0.35,
        belly_puff=0.04,
        crease_freq=2,
    )
    orange_ration = make_cylinder(0.034 * scale, 0.030 * scale, 0.042 * scale, center=(cx + tw * 0.22, cy + 0.028, cz + td * 0.18), segments=10, axis="y")
    steel_rack = make_beveled_box((tw + 0.04, 0.010, td + 0.02), center=(cx, cy - 0.014, cz), bevel=0.003)
    amber_heater = make_beveled_box((tw * 0.86, 0.008, 0.022), center=(cx, cy - 0.018, cz + td * 0.42), bevel=0.002)
    return merge_geometries(white_parts), navy_pouch, orange_ration, steel_rack, amber_heater


def make_nutrient_canister_row(cx: float, cy: float, cz: float, count: int = 4, spacing: float = 0.11, radius: float = 0.040, height: float = 0.22):
    """
    Builds a row of 3D cylindrical protein/amino nutrient cartridges with signal-orange locking collars
    and machined-steel top/bottom manifold caps.
    Returns: (white_canisters_geom, orange_collars_geom, steel_caps_geom, cyan_level_strips_geom)
    """
    whites, oranges, steels, cyans = [], [], [], []
    x0 = cx - 0.5 * (count - 1) * spacing
    for i in range(count):
        px = x0 + i * spacing
        whites.append(make_cylinder(radius, radius, height, center=(px, cy, cz), segments=10, axis="y"))
        oranges.append(make_cylinder(radius * 1.12, radius * 1.12, height * 0.18, center=(px, cy + height * 0.34, cz), segments=10, axis="y"))
        steels.append(make_cylinder(radius * 0.82, radius * 0.82, height * 0.14, center=(px, cy + height * 0.52, cz), segments=10, axis="y"))
        steels.append(make_cylinder(radius * 1.06, radius * 1.06, height * 0.10, center=(px, cy - height * 0.48, cz), segments=10, axis="y"))
        cyans.append(make_beveled_box((0.012, height * 0.55, 0.012), center=(px, cy - 0.01, cz + radius), bevel=0.002))
    return (
        merge_geometries(whites),
        merge_geometries(oranges),
        merge_geometries(steels),
        merge_geometries(cyans),
    )


def make_hydration_tap_and_flasks(cx: float, cy_deck: float, cz: float):
    """
    Builds Part 3: Sculpted machined-steel Dual-Nozzle Hydration / Espresso Tap Arch +
    two 3D insulated zero-G thermal flasks/carafes seated on glowing cyan cup-lock coaster rings +
    signal-orange hot-steam purge valve.
    Returns: (steel_tap_and_flasks_geom, charcoal_grips_and_mat_geom, orange_valves_geom, cyan_coasters_geom)
    """
    arch_pts = sample_filleted_polyline(
        [
            (cx - 0.16, cy_deck, cz - 0.10),
            (cx - 0.16, cy_deck + 0.32, cz - 0.10),
            (cx - 0.16, cy_deck + 0.32, cz + 0.06),
            (cx + 0.16, cy_deck + 0.32, cz + 0.06),
            (cx + 0.16, cy_deck + 0.32, cz - 0.10),
            (cx + 0.16, cy_deck, cz - 0.10),
        ],
        fillet_radius=0.04,
        corner_subdivs=4,
    )
    steel_parts = [
        make_swept_tube(arch_pts, radius=0.020, radial_segments=8),
        # Dual dispensing nozzles
        make_cylinder(0.016, 0.012, 0.06, center=(cx - 0.08, cy_deck + 0.28, cz + 0.06), segments=10, axis="y"),
        make_cylinder(0.016, 0.012, 0.06, center=(cx + 0.08, cy_deck + 0.28, cz + 0.06), segments=10, axis="y"),
        # Two 3D zero-G thermal flasks/carafes seated below nozzles
        make_cylinder(0.044, 0.038, 0.16, center=(cx - 0.08, cy_deck + 0.09, cz + 0.06), segments=10, axis="y"),
        make_cylinder(0.044, 0.038, 0.16, center=(cx + 0.08, cy_deck + 0.09, cz + 0.06), segments=10, axis="y"),
    ]
    charcoal_parts = [
        # Anti-slip drip-tray mat + insulated flask grip sleeves
        make_beveled_box((0.38, 0.014, 0.24), center=(cx, cy_deck + 0.006, cz + 0.05), bevel=0.004),
        make_cylinder(0.046, 0.046, 0.07, center=(cx - 0.08, cy_deck + 0.09, cz + 0.06), segments=10, axis="y"),
        make_cylinder(0.046, 0.046, 0.07, center=(cx + 0.08, cy_deck + 0.09, cz + 0.06), segments=10, axis="y"),
    ]
    orange_parts = [
        # Hot-steam purge valve & flask sipper lock caps
        make_cylinder(0.020, 0.020, 0.045, center=(cx, cy_deck + 0.32, cz + 0.08), segments=10, axis="z"),
        make_cylinder(0.028, 0.024, 0.025, center=(cx - 0.08, cy_deck + 0.18, cz + 0.06), segments=10, axis="y"),
        make_cylinder(0.028, 0.024, 0.025, center=(cx + 0.08, cy_deck + 0.18, cz + 0.06), segments=10, axis="y"),
    ]
    cyan_parts = [
        # Glowing cyan magnetic zero-G coaster lock rings
        make_cylinder(0.054, 0.054, 0.010, center=(cx - 0.08, cy_deck + 0.014, cz + 0.06), segments=10, axis="y"),
        make_cylinder(0.054, 0.054, 0.010, center=(cx + 0.08, cy_deck + 0.014, cz + 0.06), segments=10, axis="y"),
    ]
    return (
        merge_geometries(steel_parts),
        merge_geometries(charcoal_parts),
        merge_geometries(orange_parts),
        merge_geometries(cyan_parts),
    )


def make_aeroponic_herb_bay(cx: float, cy: float, cz: float, width_x: float = 0.62, height_y: float = 0.28, depth_z: float = 0.24):
    """
    Builds Part 4: Integrated Living Aeroponic Culinary Herb Strip (foliage_aeroponic_herbs.png)
    with 3D mounded culinary micro-greens/herbs inside an aerospace-white & steel hydroponic trough,
    illuminated by an overhead UV-violet (#7B5CFF) & cyan (#00E5FF) grow-light strip behind a translucent splash baffle.
    Returns: (foliage_geom, white_trough_geom, steel_trim_geom, uv_grow_geom, cyan_grow_geom, glass_baffle_geom)
    """
    mounds = [
        make_sculpted_cushion(
            (width_x * 0.90, 0.065, depth_z * 0.72),
            center=(cx, cy - height_y * 0.24, cz),
            res=(4, 3, 3),
            roundness=0.42,
            belly_puff=0.06,
            crease_freq=3,
        ),
    ]
    n_clumps = max(2, min(4, int(width_x / 0.22)))
    x0 = cx - width_x * 0.36
    for i in range(n_clumps):
        mx = x0 + (i / max(1, n_clumps - 1)) * (width_x * 0.72)
        mz = cz + (0.02 if i % 2 == 0 else -0.02)
        mounds.append(make_lathe_dome([(0.065, 0.0), (0.048, 0.038), (0.0, 0.058)], center=(mx, cy - height_y * 0.16, mz), segments=9, subdivide_profile=1))

    white_trough = [
        make_beveled_box((width_x, 0.045, depth_z), center=(cx, cy - height_y * 0.38, cz), bevel=0.01),
        make_beveled_box((width_x, height_y, 0.024), center=(cx, cy, cz - depth_z * 0.45), bevel=0.008),
    ]
    steel_trim = make_portal_oct_ring(width_x + 0.04, height_y + 0.04, center_y=cy, z_pos=cz + depth_z * 0.48, tube_r=0.015, chamfer=0.05)
    steel_trim[0][:, 0] += cx

    uv_grow = make_beveled_box((width_x * 0.88, 0.024, 0.04), center=(cx, cy + height_y * 0.38, cz + 0.01), bevel=0.004)
    cyan_grow = make_beveled_box((width_x * 0.84, 0.014, 0.025), center=(cx, cy - height_y * 0.36, cz + depth_z * 0.48), bevel=0.003)

    glass_baffle = make_quad_panel(
        (cx - width_x * 0.48, cy - height_y * 0.34, cz + depth_z * 0.47),
        (cx + width_x * 0.48, cy - height_y * 0.34, cz + depth_z * 0.47),
        (cx + width_x * 0.48, cy + height_y * 0.34, cz + depth_z * 0.47),
        (cx - width_x * 0.48, cy + height_y * 0.34, cz + depth_z * 0.47),
    )
    return (
        merge_geometries(mounds),
        merge_geometries(white_trough),
        steel_trim,
        uv_grow,
        cyan_grow,
        glass_baffle,
    )


def make_galley_base_counter(width_x: float = 1.92, depth_z: float = 0.76, deck_y: float = 0.88, counter_cx: float = 0.0):
    """
    Builds Part 1 lower counter substructure:
    - 45° chamfered gunmetal titanium outer piers & kickplate
    - Carbon-slate lower storage / waste-compactor drawers
    - Brushed machined-steel & aerospace-white serving counter deck at Y = deck_y
    - Signal-orange drawer latches
    - Amber kickplate strip & cyan counter-edge strip
    """
    gunmetal = [
        make_beveled_box((width_x, 0.08, depth_z), center=(counter_cx, 0.04, 0.0), bevel=0.015),
        make_beveled_box((0.10, deck_y, depth_z), center=(counter_cx - width_x * 0.5 + 0.05, deck_y * 0.5, 0.0), bevel=0.02),
        make_beveled_box((0.10, deck_y, depth_z), center=(counter_cx + width_x * 0.5 - 0.05, deck_y * 0.5, 0.0), bevel=0.02),
        make_beveled_box((width_x, deck_y, 0.08), center=(counter_cx, deck_y * 0.5, -depth_z * 0.5 + 0.04), bevel=0.02),
    ]
    inner_w = width_x - 0.22
    slate_drawers = [
        make_beveled_box((inner_w * 0.48, 0.34, depth_z - 0.10), center=(counter_cx - inner_w * 0.25, 0.27, 0.02), bevel=0.015),
        make_beveled_box((inner_w * 0.48, 0.34, depth_z - 0.10), center=(counter_cx + inner_w * 0.25, 0.27, 0.02), bevel=0.015),
        make_beveled_box((inner_w * 0.48, 0.34, depth_z - 0.10), center=(counter_cx - inner_w * 0.25, 0.64, 0.02), bevel=0.015),
        make_beveled_box((inner_w * 0.48, 0.34, depth_z - 0.10), center=(counter_cx + inner_w * 0.25, 0.64, 0.02), bevel=0.015),
    ]
    steel_deck = [
        make_beveled_box((width_x + 0.02, 0.045, depth_z + 0.03), center=(counter_cx, deck_y - 0.01, 0.01), bevel=0.012),
    ]
    orange_latches = [
        make_beveled_box((0.14, 0.024, 0.03), center=(counter_cx - inner_w * 0.25, 0.35, depth_z * 0.49), bevel=0.005),
        make_beveled_box((0.14, 0.024, 0.03), center=(counter_cx + inner_w * 0.25, 0.35, depth_z * 0.49), bevel=0.005),
        make_beveled_box((0.14, 0.024, 0.03), center=(counter_cx - inner_w * 0.25, 0.72, depth_z * 0.49), bevel=0.005),
        make_beveled_box((0.14, 0.024, 0.03), center=(counter_cx + inner_w * 0.25, 0.72, depth_z * 0.49), bevel=0.005),
    ]
    amber_strip = make_beveled_box((width_x * 0.86, 0.016, 0.03), center=(counter_cx, 0.06, depth_z * 0.49), bevel=0.003)
    cyan_strip = make_beveled_box((width_x * 0.92, 0.016, 0.03), center=(counter_cx, deck_y - 0.01, depth_z * 0.52), bevel=0.003)
    return (
        merge_geometries(gunmetal),
        merge_geometries(slate_drawers),
        merge_geometries(steel_deck),
        merge_geometries(orange_latches),
        amber_strip,
        cyan_strip,
    )


# ==============================================================================
# CANDIDATE 01: AEGIS-7 OCTAGONAL BULKHEAD RATION SYNTHESIZER & BEVERAGE BAR (`galley_synth_r1_01.glb`)
# Dimensions: 1.90m W x 0.76m D x 2.10m H
# ==============================================================================
def build_01_octagonal_ration_synthesizer(mats):
    sm = []
    gm_base, sl_drawers, st_deck, or_latches, am_kick, cy_deck = make_galley_base_counter(width_x=1.90, depth_z=0.76, deck_y=0.88, counter_cx=0.0)

    # Upper octagonal bulkhead housing (Y = 0.88..2.10m) with open central synthesis chambers & top herb bay
    upper_gm = [
        gm_base,
        make_beveled_box((1.90, 1.22, 0.10), center=(0.0, 1.49, -0.33), bevel=0.025),
        make_beveled_box((0.12, 1.22, 0.52), center=(-0.89, 1.49, -0.10), bevel=0.025),
        make_beveled_box((0.12, 1.22, 0.52), center=(0.89, 1.49, -0.10), bevel=0.025),
        make_beveled_box((1.90, 0.12, 0.62), center=(0.0, 2.04, -0.05), bevel=0.025),
        # Central vertical divider & shelf framing the twin translucent thermal synthesis ovens
        make_beveled_box((0.06, 0.74, 0.44), center=(-0.22, 1.25, -0.08), bevel=0.012),
        make_beveled_box((0.06, 0.74, 0.44), center=(0.36, 1.25, -0.08), bevel=0.012),
        make_beveled_box((1.72, 0.05, 0.48), center=(0.0, 1.62, -0.06), bevel=0.012),
        # 45° chamfered upper corner gussets
        transform_geom(make_beveled_box((0.30, 0.10, 0.52), bevel=0.015), translate=(-0.74, 1.92, -0.08), rot_xyz_deg=(0.0, 0.0, 45.0)),
        transform_geom(make_beveled_box((0.30, 0.10, 0.52), bevel=0.015), translate=(0.74, 1.92, -0.08), rot_xyz_deg=(0.0, 0.0, -45.0)),
    ]
    add_part(sm, "Galley01_OctagonalGunmetalBulkhead", merge_geometries(upper_gm), mats["gunmetal"])
    add_part(sm, "Galley01_CarbonSlateDrawers", sl_drawers, mats["carbon_slate"])

    # Central Twin Translucent Synthesis Ovens (X = -0.18..+0.32, Y = 0.94..1.58) with 2 tiers of 3D meal trays & canisters
    w_t1, nv_t1, or_t1, st_t1, am_t1 = make_3d_meal_tray_with_rations(0.07, 1.04, -0.04, scale=1.05)
    w_t2, nv_t2, or_t2, st_t2, am_t2 = make_3d_meal_tray_with_rations(0.07, 1.26, -0.04, scale=1.05)
    w_can, or_can, st_can, cy_can = make_nutrient_canister_row(0.07, 1.47, -0.06, count=4, spacing=0.105, radius=0.034, height=0.16)

    # Left Dual-Nozzle Beverage Tap Arch + Zero-G Flasks (X = -0.55)
    st_tap, ch_tap, or_tap, cy_tap = make_hydration_tap_and_flasks(cx=-0.55, cy_deck=0.89, cz=0.08)

    # Top Full-Width Living Aeroponic Herb Bay (Y = 1.66..1.96, X = -0.68..+0.68)
    fol_h, wh_h, st_h, uv_h, cy_h, gl_h = make_aeroponic_herb_bay(cx=0.0, cy=1.80, cz=-0.04, width_x=1.28, height_y=0.26, depth_z=0.32)

    # Oven inner white liner + meal trays + canisters + herb trough
    oven_liner = make_beveled_box((0.52, 0.66, 0.025), center=(0.07, 1.26, -0.24), bevel=0.008)
    add_part(sm, "Galley01_WhiteTraysCanistersAndLiner", merge_geometries([oven_liner, w_t1, w_t2, w_can, wh_h]), mats["aero_white"])
    add_part(sm, "Galley01_CharcoalPadsAndFlaskGrips", ch_tap, mats["pad_charcoal"])
    add_part(sm, "Galley01_NavyRationPouches", merge_geometries([nv_t1, nv_t2]), mats["pad_navy"])
    add_part(sm, "Galley01_SignalOrangeValvesAndLatches", merge_geometries([or_latches, or_t1, or_t2, or_can, or_tap]), mats["accent_orange"])
    add_part(sm, "Galley01_AeroponicCulinaryHerbs", fol_h, mats["foliage_herbs"])

    # Oven bevel frame + counter + tap + racks
    oven_ring = make_portal_oct_ring(0.54, 0.66, center_y=1.26, z_pos=0.14, tube_r=0.016, chamfer=0.06)
    oven_ring[0][:, 0] += 0.07
    add_part(sm, "Galley01_MachinedCounterTapAndRacks", merge_geometries([st_deck, st_t1, st_t2, st_can, st_tap, st_h, oven_ring]), mats["steel_machined"])

    # Right Widescreen OLED Nutri-Telemetry Console (X = +0.42..+0.80, Y = 1.06..1.52)
    add_part(
        sm,
        "Galley01_OLEDNutriSynthesizer",
        make_quad_panel((0.42, 1.04, 0.14), (0.80, 1.04, 0.14), (0.80, 1.54, 0.14), (0.42, 1.54, 0.14)),
        mats["oled_nutri"],
    )
    add_part(sm, "Galley01_AmberInductionAndKickLED", merge_geometries([am_kick, am_t1, am_t2]), mats["led_amber"])
    add_part(sm, "Galley01_CyanCoastersAndCounterLED", merge_geometries([cy_deck, cy_can, cy_tap, cy_h]), mats["led_cyan"])
    add_part(sm, "Galley01_UVGrowBarLED", uv_h, mats["led_uv"])

    # Translucent Synth Chamber Door + Herb Baffle (alphaMode: BLEND)
    oven_glass = make_quad_panel((-0.18, 0.94, 0.14), (0.32, 0.94, 0.14), (0.32, 1.58, 0.14), (-0.18, 1.58, 0.14))
    add_part(sm, "Galley01_TranslucentSynthChamberGlass", merge_geometries([oven_glass, gl_h]), mats["glass_chamber"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "galley_synth_r1_01.glb"), sm, root_name="GalleySynthR1_01_OctagonalBulkheadSynthesizer")


# ==============================================================================
# CANDIDATE 02: DUAL-ZONE SPLIT THERMAL SYNTHESIZER & TRANSLUCENT RATION/HERB TOWER (`galley_synth_r1_02.glb`)
# Dimensions: 2.00m W x 0.78m D x 2.12m H (Direct 65% / 35% Split-Bay Sibling to All Locked Winners!)
# ==============================================================================
def build_02_dual_zone_split_synthesizer(mats):
    sm = []
    # Left Bay (65% width, X = -1.00..+0.30, 1.30m wide, centered at X = -0.35): Main Galley Counter, Twin Ovens, Tap Arch & OLED
    # Right Bay (35% width, X = +0.30..+1.00, 0.70m wide, centered at X = +0.65): Full-Height 3-Tier Translucent Ration & Herb Tower
    gm_left, sl_drawers, st_deck, or_latches, am_kick, cy_deck = make_galley_base_counter(width_x=1.30, depth_z=0.78, deck_y=0.88, counter_cx=-0.35)

    right_tower_gm = [
        gm_left,
        # Left upper bulkhead housing (Y = 0.88..2.12m)
        make_beveled_box((1.30, 1.24, 0.10), center=(-0.35, 1.50, -0.34), bevel=0.025),
        make_beveled_box((0.10, 1.24, 0.54), center=(-0.95, 1.50, -0.10), bevel=0.025),
        make_beveled_box((1.30, 0.14, 0.62), center=(-0.35, 2.05, -0.06), bevel=0.025),
        # Right Full-Height 3-Tier Tower Frame (X = +0.30..+1.00, Y = 0.00..2.12m)
        make_beveled_box((0.70, 0.12, 0.78), center=(0.65, 0.06, 0.0), bevel=0.02),
        make_beveled_box((0.70, 0.14, 0.78), center=(0.65, 2.05, 0.0), bevel=0.025),
        make_beveled_box((0.08, 2.00, 0.74), center=(0.32, 1.04, 0.0), bevel=0.02),
        make_beveled_box((0.10, 2.00, 0.74), center=(0.95, 1.04, 0.0), bevel=0.02),
        make_beveled_box((0.68, 2.00, 0.10), center=(0.65, 1.04, -0.34), bevel=0.02),
        # Tower internal horizontal shelf dividers (Top Canister tier Y=1.45..1.98, Mid Herb tier Y=0.82..1.45, Bot Ration tier Y=0.12..0.82)
        make_beveled_box((0.58, 0.04, 0.62), center=(0.65, 1.44, -0.02), bevel=0.01),
        make_beveled_box((0.58, 0.04, 0.62), center=(0.65, 0.82, -0.02), bevel=0.01),
    ]
    add_part(sm, "Galley02_SplitBayGunmetalHousing", merge_geometries(right_tower_gm), mats["gunmetal"])
    add_part(sm, "Galley02_LeftBayCarbonSlateDrawers", sl_drawers, mats["carbon_slate"])

    # Left Bay: Beverage Tap Arch + Two 3D Zero-G Flasks at X = -0.68, Deck Y = 0.89
    st_tap, ch_tap, or_tap, cy_tap = make_hydration_tap_and_flasks(cx=-0.68, cy_deck=0.89, cz=0.08)

    # Left Bay: Dual Recessed Translucent Synthesis Chambers at X = -0.08, Y = 0.94..1.58
    w_t1, nv_t1, or_t1, st_t1, am_t1 = make_3d_meal_tray_with_rations(-0.08, 1.06, -0.02, scale=1.08)
    w_t2, nv_t2, or_t2, st_t2, am_t2 = make_3d_meal_tray_with_rations(-0.08, 1.34, -0.02, scale=1.08)

    # Right Bay Top Tier (Y = 1.48..1.96): 6 Vertical Cylindrical Protein/Electrolyte Canisters with Signal-Orange Collars
    w_can, or_can, st_can, cy_can = make_nutrient_canister_row(0.65, 1.70, 0.02, count=4, spacing=0.12, radius=0.038, height=0.28)

    # Right Bay Middle Tier (Y = 0.86..1.42): Illuminated Living Aeroponic Culinary Herb Trough under #7B5CFF UV-Violet Grow Bar
    fol_h, wh_h, st_h, uv_h, cy_h, _ = make_aeroponic_herb_bay(cx=0.65, cy=1.14, cz=0.04, width_x=0.52, height_y=0.46, depth_z=0.38)

    # Right Bay Bottom Tier (Y = 0.14..0.80): Stacked 3D Sealed Crew Ration Cases & Spare Thermal Carafes
    w_t3, nv_t3, or_t3, st_t3, am_t3 = make_3d_meal_tray_with_rations(0.65, 0.56, 0.04, scale=1.10)
    spare_cases = [
        make_beveled_box((0.54, 1.84, 0.025), center=(0.65, 1.05, -0.26), bevel=0.008),
        make_beveled_box((0.46, 0.62, 0.025), center=(-0.08, 1.24, -0.24), bevel=0.008),
        make_beveled_box((0.22, 0.20, 0.28), center=(0.53, 0.28, 0.04), bevel=0.015),
        make_cylinder(0.052, 0.046, 0.22, center=(0.77, 0.29, 0.06), segments=10, axis="y"),
    ]
    add_part(
        sm,
        "Galley02_WhiteMealTraysAndNutrientCanisters",
        merge_geometries([w_t1, w_t2, w_t3, w_can, wh_h] + spare_cases),
        mats["aero_white"],
    )
    add_part(sm, "Galley02_CharcoalMatsAndFlaskGrips", ch_tap, mats["pad_charcoal"])
    add_part(sm, "Galley02_NavyRationPacks", merge_geometries([nv_t1, nv_t2, nv_t3]), mats["pad_navy"])
    add_part(
        sm,
        "Galley02_SignalOrangeValvesCollarsAndLatches",
        merge_geometries([or_latches, or_tap, or_t1, or_t2, or_t3, or_can]),
        mats["accent_orange"],
    )
    add_part(sm, "Galley02_RightTowerAeroponicHerbs", fol_h, mats["foliage_herbs"])

    # Beveled Machined-Steel Frames around Left Synthesis Chamber & Right Full-Height Translucent Tower Door
    left_oven_ring = make_portal_oct_ring(0.50, 0.64, center_y=1.24, z_pos=0.16, tube_r=0.016, chamfer=0.06)
    left_oven_ring[0][:, 0] -= 0.08
    right_tower_ring = make_portal_oct_ring(0.58, 1.84, center_y=1.05, z_pos=0.35, tube_r=0.020, chamfer=0.09)
    right_tower_ring[0][:, 0] += 0.65

    add_part(
        sm,
        "Galley02_MachinedCounterTapAndTowerBezel",
        merge_geometries([st_deck, st_tap, st_t1, st_t2, st_t3, st_can, st_h, left_oven_ring, right_tower_ring]),
        mats["steel_machined"],
    )

    # Left Bay Upper Widescreen OLED Nutri-Telemetry Console (X = -0.84..-0.36, Y = 1.58..1.94)
    add_part(
        sm,
        "Galley02_WidescreenOLEDNutriConsole",
        make_quad_panel((-0.86, 1.56, 0.14), (-0.34, 1.56, 0.14), (-0.34, 1.94, 0.14), (-0.86, 1.94, 0.14)),
        mats["oled_nutri"],
    )
    add_part(sm, "Galley02_WarmAmberInductionLED", merge_geometries([am_kick, am_t1, am_t2, am_t3]), mats["led_amber"])
    add_part(sm, "Galley02_CyanCoastersAndTowerLED", merge_geometries([cy_deck, cy_tap, cy_can, cy_h]), mats["led_cyan"])
    add_part(sm, "Galley02_UVGrowBarLED", uv_h, mats["led_uv"])

    # Translucent Glass Doors (Left Oven + Right Full-Height 3-Tier Ration/Herb Tower)
    left_oven_glass = make_quad_panel((-0.31, 0.94, 0.16), (0.15, 0.94, 0.16), (0.15, 1.54, 0.16), (-0.31, 1.54, 0.16))
    right_tower_glass = make_quad_panel((0.37, 0.15, 0.35), (0.93, 0.15, 0.35), (0.93, 1.95, 0.35), (0.37, 1.95, 0.35))
    add_part(
        sm,
        "Galley02_TranslucentOvenAndTowerDoors",
        merge_geometries([left_oven_glass, right_tower_glass]),
        mats["glass_chamber"],
    )

    out_p = os.path.join(OUT_GLB_DIR, "galley_synth_r1_02.glb")
    info = center_and_export_glb(out_p, sm, root_name="GalleySynthR1_02_DualZoneSplitSynthesizer")
    # Winner copy is exported only after the 5-Bot post-render vote completes
    return info


# ==============================================================================
# CANDIDATE 03: ROTARY CAROUSEL AUTOMATON DISPENSER & ESPRESSO TAP ALCOVE (`galley_synth_r1_03.glb`)
# Dimensions: 1.88m W x 0.80m D x 2.10m H
# ==============================================================================
def build_03_rotary_carousel_automaton(mats):
    sm = []
    gm_base, sl_drawers, st_deck, or_latches, am_kick, cy_deck = make_galley_base_counter(width_x=1.88, depth_z=0.80, deck_y=0.88, counter_cx=0.0)

    upper_gm = [
        gm_base,
        make_beveled_box((1.88, 1.22, 0.10), center=(0.0, 1.49, -0.35), bevel=0.025),
        make_beveled_box((0.12, 1.22, 0.56), center=(-0.88, 1.49, -0.10), bevel=0.025),
        make_beveled_box((0.12, 1.22, 0.56), center=(0.88, 1.49, -0.10), bevel=0.025),
        make_beveled_box((1.88, 0.14, 0.64), center=(0.0, 2.03, -0.05), bevel=0.025),
    ]
    add_part(sm, "Galley03_GunmetalAutomatonHousing", merge_geometries(upper_gm), mats["gunmetal"])
    add_part(sm, "Galley03_CarbonSlateDrawers", sl_drawers, mats["carbon_slate"])

    # Central 3-Tier Rotary Ration Carousel (X = 0.0, Y = 0.94..1.92) with central steel spindle & 3 rotating turntables
    w_t1, nv_t1, or_t1, st_t1, am_t1 = make_3d_meal_tray_with_rations(0.0, 1.06, 0.02, scale=1.05)
    w_t2, nv_t2, or_t2, st_t2, am_t2 = make_3d_meal_tray_with_rations(0.0, 1.38, 0.02, scale=1.05)
    w_can, or_can, st_can, cy_can = make_nutrient_canister_row(0.0, 1.72, 0.02, count=4, spacing=0.11, radius=0.036, height=0.22)

    carousel_disks = [
        make_cylinder(0.28, 0.28, 0.02, center=(0.0, 1.02, 0.0), segments=14, axis="y"),
        make_cylinder(0.28, 0.28, 0.02, center=(0.0, 1.34, 0.0), segments=14, axis="y"),
        make_cylinder(0.28, 0.28, 0.02, center=(0.0, 1.58, 0.0), segments=14, axis="y"),
        make_cylinder(0.025, 0.025, 0.96, center=(0.0, 1.42, 0.0), segments=10, axis="y"),
    ]
    # Left High-Pressure Espresso & Hydration Tap Bay (X = -0.58)
    st_tap, ch_tap, or_tap, cy_tap = make_hydration_tap_and_flasks(cx=-0.58, cy_deck=0.89, cz=0.08)

    # Right Living Herb Strip (X = +0.58, Y = 1.62..1.92) + Lower Right Ordering OLED Kiosk (Y = 1.02..1.52)
    fol_h, wh_h, st_h, uv_h, cy_h, gl_h = make_aeroponic_herb_bay(cx=0.58, cy=1.74, cz=-0.02, width_x=0.46, height_y=0.28, depth_z=0.30)

    back_liner = make_beveled_box((0.68, 0.98, 0.025), center=(0.0, 1.43, -0.26), bevel=0.008)
    add_part(sm, "Galley03_WhiteTraysAndCanisters", merge_geometries([back_liner, w_t1, w_t2, w_can, wh_h]), mats["aero_white"])
    add_part(sm, "Galley03_CharcoalPads", ch_tap, mats["pad_charcoal"])
    add_part(sm, "Galley03_NavyPouches", merge_geometries([nv_t1, nv_t2]), mats["pad_navy"])
    add_part(sm, "Galley03_SignalOrangeValves", merge_geometries([or_latches, or_t1, or_t2, or_can, or_tap]), mats["accent_orange"])
    add_part(sm, "Galley03_AeroponicHerbs", fol_h, mats["foliage_herbs"])

    carousel_ring = make_portal_oct_ring(0.66, 0.98, center_y=1.43, z_pos=0.22, tube_r=0.018, chamfer=0.09)
    add_part(
        sm,
        "Galley03_MachinedCarouselAndTap",
        merge_geometries([st_deck, st_t1, st_t2, st_can, st_tap, st_h, carousel_ring] + carousel_disks),
        mats["steel_machined"],
    )
    add_part(
        sm,
        "Galley03_RightOLEDOrderingKiosk",
        make_quad_panel((0.38, 1.02, 0.16), (0.78, 1.02, 0.16), (0.78, 1.50, 0.16), (0.38, 1.50, 0.16)),
        mats["oled_nutri"],
    )
    add_part(sm, "Galley03_AmberCarouselLED", merge_geometries([am_kick, am_t1, am_t2]), mats["led_amber"])
    add_part(sm, "Galley03_CyanCoastersAndCarouselLED", merge_geometries([cy_deck, cy_can, cy_tap, cy_h]), mats["led_cyan"])
    add_part(sm, "Galley03_UVGrowLED", uv_h, mats["led_uv"])

    carousel_glass = make_quad_panel((-0.31, 0.95, 0.22), (0.31, 0.95, 0.22), (0.31, 1.91, 0.22), (-0.31, 1.91, 0.22))
    add_part(sm, "Galley03_TranslucentCarouselWindow", merge_geometries([carousel_glass, gl_h]), mats["glass_chamber"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "galley_synth_r1_03.glb"), sm, root_name="GalleySynthR1_03_RotaryCarouselAutomaton")


# ==============================================================================
# CANDIDATE 04: CANTILEVERED ISLAND GALLEY MODULE & OVERHEAD NUTRIENT MANIFOLD (`galley_synth_r1_04.glb`)
# Dimensions: 1.95m W x 0.78m D x 2.12m H
# ==============================================================================
def build_04_cantilevered_island_galley(mats):
    sm = []
    gm_base, sl_drawers, st_deck, or_latches, am_kick, cy_deck = make_galley_base_counter(width_x=1.95, depth_z=0.78, deck_y=0.88, counter_cx=0.0)

    # Heavy rear titanium pillars & overhead cantilevered nutrient canopy
    upper_gm = [
        gm_base,
        make_beveled_box((0.22, 1.24, 0.28), center=(-0.78, 1.50, -0.22), bevel=0.025),
        make_beveled_box((0.22, 1.24, 0.28), center=(0.78, 1.50, -0.22), bevel=0.025),
        make_beveled_box((1.95, 0.22, 0.72), center=(0.0, 2.01, -0.02), bevel=0.03),
    ]
    add_part(sm, "Galley04_CantileveredGunmetalPillars", merge_geometries(upper_gm), mats["gunmetal"])
    add_part(sm, "Galley04_CarbonSlateDrawers", sl_drawers, mats["carbon_slate"])

    # Overhead exposed nutrient feed canisters (Y = 1.68..1.90) + Eye-level translucent synthesis bays (Y = 1.00..1.52)
    w_can, or_can, st_can, cy_can = make_nutrient_canister_row(-0.28, 1.74, 0.04, count=4, spacing=0.11, radius=0.036, height=0.22)
    w_t1, nv_t1, or_t1, st_t1, am_t1 = make_3d_meal_tray_with_rations(-0.28, 1.08, 0.02, scale=1.08)
    w_t2, nv_t2, or_t2, st_t2, am_t2 = make_3d_meal_tray_with_rations(-0.28, 1.32, 0.02, scale=1.08)

    st_tap, ch_tap, or_tap, cy_tap = make_hydration_tap_and_flasks(cx=0.36, cy_deck=0.89, cz=0.08)
    fol_h, wh_h, st_h, uv_h, cy_h, gl_h = make_aeroponic_herb_bay(cx=0.38, cy=1.74, cz=0.02, width_x=0.58, height_y=0.26, depth_z=0.32)

    liner = make_beveled_box((0.64, 0.56, 0.025), center=(-0.28, 1.22, -0.20), bevel=0.008)
    add_part(sm, "Galley04_WhiteTraysAndCanisters", merge_geometries([liner, w_t1, w_t2, w_can, wh_h]), mats["aero_white"])
    add_part(sm, "Galley04_CharcoalPads", ch_tap, mats["pad_charcoal"])
    add_part(sm, "Galley04_NavyPouches", merge_geometries([nv_t1, nv_t2]), mats["pad_navy"])
    add_part(sm, "Galley04_SignalOrangeValves", merge_geometries([or_latches, or_t1, or_t2, or_can, or_tap]), mats["accent_orange"])
    add_part(sm, "Galley04_AeroponicHerbs", fol_h, mats["foliage_herbs"])

    oven_ring = make_portal_oct_ring(0.62, 0.56, center_y=1.22, z_pos=0.18, tube_r=0.016, chamfer=0.06)
    oven_ring[0][:, 0] -= 0.28
    add_part(sm, "Galley04_MachinedManifoldsAndCounter", merge_geometries([st_deck, st_t1, st_t2, st_can, st_tap, st_h, oven_ring]), mats["steel_machined"])

    add_part(
        sm,
        "Galley04_OLEDNutriConsole",
        make_quad_panel((-0.86, 1.04, 0.14), (-0.62, 1.04, 0.14), (-0.62, 1.54, 0.14), (-0.86, 1.54, 0.14)),
        mats["oled_nutri"],
    )
    add_part(sm, "Galley04_AmberInductionLED", merge_geometries([am_kick, am_t1, am_t2]), mats["led_amber"])
    add_part(sm, "Galley04_CyanCoastersLED", merge_geometries([cy_deck, cy_can, cy_tap, cy_h]), mats["led_cyan"])
    add_part(sm, "Galley04_UVGrowLED", uv_h, mats["led_uv"])

    oven_glass = make_quad_panel((-0.58, 0.95, 0.18), (0.02, 0.95, 0.18), (0.02, 1.49, 0.18), (-0.58, 1.49, 0.18))
    add_part(sm, "Galley04_TranslucentCanopyGlass", merge_geometries([oven_glass, gl_h]), mats["glass_chamber"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "galley_synth_r1_04.glb"), sm, root_name="GalleySynthR1_04_CantileveredIslandGalley")


# ==============================================================================
# CANDIDATE 05: HEAVY CREW MESS QUAD-CHAMBER INDUCTION SYNTHESIZER (`galley_synth_r1_05.glb`)
# Dimensions: 2.05m W x 0.78m D x 2.12m H
# ==============================================================================
def build_05_quad_chamber_induction_synthesizer(mats):
    sm = []
    gm_base, sl_drawers, st_deck, or_latches, am_kick, cy_deck = make_galley_base_counter(width_x=2.05, depth_z=0.78, deck_y=0.88, counter_cx=0.0)

    upper_gm = [
        gm_base,
        make_beveled_box((2.05, 1.24, 0.10), center=(0.0, 1.50, -0.34), bevel=0.025),
        make_beveled_box((0.12, 1.24, 0.56), center=(-0.96, 1.50, -0.10), bevel=0.025),
        make_beveled_box((0.12, 1.24, 0.56), center=(0.96, 1.50, -0.10), bevel=0.025),
        make_beveled_box((2.05, 0.12, 0.64), center=(0.0, 2.06, -0.05), bevel=0.025),
        make_beveled_box((1.84, 0.05, 0.50), center=(0.0, 1.66, -0.06), bevel=0.012),
    ]
    add_part(sm, "Galley05_QuadChamberGunmetalBulkhead", merge_geometries(upper_gm), mats["gunmetal"])
    add_part(sm, "Galley05_CarbonSlateDrawers", sl_drawers, mats["carbon_slate"])

    # 2x2 Quad-Grid of Induction Synthesis Chambers on Left/Center (X = -0.58 and -0.14, Y = 1.06 and 1.38)
    w_t1, nv_t1, or_t1, st_t1, am_t1 = make_3d_meal_tray_with_rations(-0.56, 1.06, -0.02, scale=0.92)
    w_t2, nv_t2, or_t2, st_t2, am_t2 = make_3d_meal_tray_with_rations(-0.14, 1.06, -0.02, scale=0.92)
    w_t3, nv_t3, or_t3, st_t3, am_t3 = make_3d_meal_tray_with_rations(-0.56, 1.38, -0.02, scale=0.92)
    w_can, or_can, st_can, cy_can = make_nutrient_canister_row(-0.14, 1.42, -0.02, count=3, spacing=0.095, radius=0.032, height=0.18)

    st_tap, ch_tap, or_tap, cy_tap = make_hydration_tap_and_flasks(cx=0.32, cy_deck=0.89, cz=0.08)
    fol_h, wh_h, st_h, uv_h, cy_h, gl_h = make_aeroponic_herb_bay(cx=0.0, cy=1.84, cz=-0.02, width_x=1.42, height_y=0.24, depth_z=0.30)

    liner = make_beveled_box((0.86, 0.68, 0.025), center=(-0.35, 1.25, -0.24), bevel=0.008)
    add_part(sm, "Galley05_WhiteQuadTraysAndCanisters", merge_geometries([liner, w_t1, w_t2, w_t3, w_can, wh_h]), mats["aero_white"])
    add_part(sm, "Galley05_CharcoalPads", ch_tap, mats["pad_charcoal"])
    add_part(sm, "Galley05_NavyPouches", merge_geometries([nv_t1, nv_t2, nv_t3]), mats["pad_navy"])
    add_part(sm, "Galley05_SignalOrangeValves", merge_geometries([or_latches, or_t1, or_t2, or_t3, or_can, or_tap]), mats["accent_orange"])
    add_part(sm, "Galley05_AeroponicHerbs", fol_h, mats["foliage_herbs"])

    quad_ring = make_portal_oct_ring(0.84, 0.66, center_y=1.25, z_pos=0.16, tube_r=0.016, chamfer=0.07)
    quad_ring[0][:, 0] -= 0.35
    add_part(sm, "Galley05_MachinedQuadFrameAndTap", merge_geometries([st_deck, st_t1, st_t2, st_t3, st_can, st_tap, st_h, quad_ring]), mats["steel_machined"])

    add_part(
        sm,
        "Galley05_RightOLEDNutriConsole",
        make_quad_panel((0.56, 1.04, 0.14), (0.88, 1.04, 0.14), (0.88, 1.54, 0.14), (0.56, 1.54, 0.14)),
        mats["oled_nutri"],
    )
    add_part(sm, "Galley05_AmberQuadInductionLED", merge_geometries([am_kick, am_t1, am_t2, am_t3]), mats["led_amber"])
    add_part(sm, "Galley05_CyanCoastersLED", merge_geometries([cy_deck, cy_can, cy_tap, cy_h]), mats["led_cyan"])
    add_part(sm, "Galley05_UVGrowLED", uv_h, mats["led_uv"])

    quad_glass = make_quad_panel((-0.76, 0.94, 0.16), (0.06, 0.94, 0.16), (0.06, 1.56, 0.16), (-0.76, 1.56, 0.16))
    add_part(sm, "Galley05_TranslucentQuadChamberGlass", merge_geometries([quad_glass, gl_h]), mats["glass_chamber"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "galley_synth_r1_05.glb"), sm, root_name="GalleySynthR1_05_QuadChamberInductionSynthesizer")


# ==============================================================================
# COMPANION ASSET: MESS DINING BOOTH & CANTILEVERED TABLE (`mess_dining_booth.glb`)
# ==============================================================================
def build_mess_dining_booth(mats):
    """
    Builds Custom Companion Mess Booth & Cantilevered Table (`mess_dining_booth.glb`)
    following `/workspace/game-project/design/rooms/room_03_mess_galley_spec.md`:
    - Sculpted cantilevered brushed-steel & matte aerospace-white dining table (1.80m W x 0.95m D x 0.76m H)
      with recessed glowing cyan tray borders, 3D compartmentalized meal trays, magnetic mugs, and translucent
      center smart-glass table telemetry/herb centerpiece (`alphaMode: "BLEND"`).
    - Twin contoured orbital-navy & charcoal flightpad bench booths (total envelope ~1.84m W x 2.10m D x 0.94m H).
    """
    sm = []
    # 1. Gunmetal Titanium & Carbon-Slate Bench Frames + Central Cantilever Pedestal Spine
    gunmetal_parts = [
        # Central floor spine connecting both booths & table pedestal (Y = 0.00..0.06m)
        make_beveled_box((1.76, 0.06, 2.04), center=(0.0, 0.03, 0.0), bevel=0.015),
        # North Bench Base & Angled Backrest Shell (Z = -0.82m)
        make_beveled_box((1.80, 0.40, 0.52), center=(0.0, 0.23, -0.76), bevel=0.025),
        make_beveled_box((1.80, 0.52, 0.12), center=(0.0, 0.68, -0.96), bevel=0.025),
        # South Bench Base & Angled Backrest Shell (Z = +0.82m)
        make_beveled_box((1.80, 0.40, 0.52), center=(0.0, 0.23, 0.76), bevel=0.025),
        make_beveled_box((1.80, 0.52, 0.12), center=(0.0, 0.68, 0.96), bevel=0.025),
    ]
    add_part(sm, "MessBooth_GunmetalFramesAndPlinth", merge_geometries(gunmetal_parts), mats["gunmetal"])

    slate_parts = [
        # Central table pedestal column
        make_beveled_box((0.92, 0.68, 0.24), center=(0.0, 0.38, 0.0), bevel=0.025),
    ]
    add_part(sm, "MessBooth_CarbonSlateTablePedestal", merge_geometries(slate_parts), mats["carbon_slate"])

    # 2. Contoured Orbital-Navy Seat Cushions & Charcoal Flightpad Lumbar Bolsters
    navy_cushions = [
        make_sculpted_cushion((1.72, 0.10, 0.48), center=(0.0, 0.45, -0.74), res=(8, 3, 5), roundness=0.36, belly_puff=0.04, crease_freq=4),
        make_sculpted_cushion((1.72, 0.10, 0.48), center=(0.0, 0.45, 0.74), res=(8, 3, 5), roundness=0.36, belly_puff=0.04, crease_freq=4),
    ]
    add_part(sm, "MessBooth_OrbitalNavySeatCushions", merge_geometries(navy_cushions), mats["pad_navy"])

    charcoal_backs = [
        make_sculpted_cushion((1.70, 0.42, 0.10), center=(0.0, 0.70, -0.88), res=(8, 4, 3), roundness=0.35, belly_puff=0.04, crease_freq=4),
        make_sculpted_cushion((1.70, 0.42, 0.10), center=(0.0, 0.70, 0.88), res=(8, 4, 3), roundness=0.35, belly_puff=0.04, crease_freq=4),
    ]
    add_part(sm, "MessBooth_CharcoalFlightpadBackrests", merge_geometries(charcoal_backs), mats["pad_charcoal"])

    # 3. Cantilevered Aerospace-White & Brushed-Steel Dining Table (1.80m W x 0.92m D at Y = 0.76m) + 4 Meal Trays & Mugs
    w_t1, _, or_t1, st_t1, _ = make_3d_meal_tray_with_rations(-0.46, 0.785, -0.22, scale=0.95)
    w_t2, _, or_t2, st_t2, _ = make_3d_meal_tray_with_rations(0.46, 0.785, -0.22, scale=0.95)
    w_t3, _, or_t3, st_t3, _ = make_3d_meal_tray_with_rations(-0.46, 0.785, 0.22, scale=0.95)
    w_t4, _, or_t4, st_t4, _ = make_3d_meal_tray_with_rations(0.46, 0.785, 0.22, scale=0.95)

    table_white = [
        make_beveled_box((1.80, 0.045, 0.92), center=(0.0, 0.74, 0.0), bevel=0.015),
        w_t1,
        w_t2,
        w_t3,
        w_t4,
    ]
    add_part(sm, "MessBooth_AerospaceWhiteTableAndTrays", merge_geometries(table_white), mats["aero_white"])

    steel_parts = [
        make_beveled_box((1.84, 0.032, 0.96), center=(0.0, 0.735, 0.0), bevel=0.012),
        st_t1,
        st_t2,
        st_t3,
        st_t4,
        # 4 Magnetic Zero-G Thermal Mugs on the dining table
        make_cylinder(0.036, 0.032, 0.11, center=(-0.20, 0.81, -0.20), segments=10, axis="y"),
        make_cylinder(0.036, 0.032, 0.11, center=(0.20, 0.81, -0.20), segments=10, axis="y"),
        make_cylinder(0.036, 0.032, 0.11, center=(-0.20, 0.81, 0.20), segments=10, axis="y"),
        make_cylinder(0.036, 0.032, 0.11, center=(0.20, 0.81, 0.20), segments=10, axis="y"),
    ]
    add_part(sm, "MessBooth_MachinedSteelRimAndMugs", merge_geometries(steel_parts), mats["steel_machined"])
    add_part(sm, "MessBooth_SignalOrangeRationCaps", merge_geometries([or_t1, or_t2, or_t3, or_t4]), mats["accent_orange"])

    cyan_strips = [
        make_beveled_box((1.72, 0.014, 0.025), center=(0.0, 0.764, -0.43), bevel=0.003),
        make_beveled_box((1.72, 0.014, 0.025), center=(0.0, 0.764, 0.43), bevel=0.003),
    ]
    add_part(sm, "MessBooth_CyanTableTrayBorders", merge_geometries(cyan_strips), mats["led_cyan"])

    amber_strips = [
        make_beveled_box((1.68, 0.014, 0.025), center=(0.0, 0.055, -0.48), bevel=0.003),
        make_beveled_box((1.68, 0.014, 0.025), center=(0.0, 0.055, 0.48), bevel=0.003),
    ]
    add_part(sm, "MessBooth_AmberBaseGuideStrips", merge_geometries(amber_strips), mats["led_amber"])

    # Translucent center table condiment/telemetry sneeze-shield strip (alphaMode: BLEND)
    center_glass = make_quad_panel((-0.55, 0.765, 0.0), (0.55, 0.765, 0.0), (0.55, 0.90, 0.0), (-0.55, 0.90, 0.0))
    add_part(sm, "MessBooth_TranslucentTableCenterShield", center_glass, mats["glass_chamber"])

    p1 = os.path.join(ROOMS_GLB_DIR, "mess_dining_booth.glb")
    p2 = os.path.join(OUT_GLB_DIR, "mess_dining_booth.glb")
    p3 = "/workspace/game-project/assets/glb/mess_dining_booth.glb"
    info = center_and_export_glb(p1, sm, root_name="Room03_MessDiningBooth")
    shutil.copyfile(p1, p2)
    shutil.copyfile(p1, p3)
    print(f"[mess_dining_booth] Exported {p1} and mirrored to {p2} & {p3} ({info['triangles']} tris)")
    return info


# ==============================================================================
# ROOM 03 ARCHITECTURAL SHELL (`room_03_shell.glb` / `room_03_mess_shell.glb`)
# ==============================================================================
def build_room_03_mess_galley_shell(mats):
    """
    Builds Room 03 — Crew Mess Hall & Synthesizer Galley Architectural Shell (7.0m W x 8.0m D x 3.2m H)
    following `/workspace/game-project/design/rooms/room_03_mess_galley_spec.md`:
    - Centered at (0,0,0) with floor deck min Y = 0.0000m (X: -3.50..+3.50, Z: -4.00..+4.00, Y: 0.00..3.20)
    - 5 Repeating 45° Chamfered Octagonal Titanium Ribs (Z = -3.8m, -1.9m, 0.0m, +1.9m, +3.8m)
    - Matte aerospace-white coffered ceiling panels + recessed cyan (#00E5FF) ceiling cove strips
    - North Panoramic Cylinder Viewport Wall (Z = -3.95m, X = -2.6m to +2.6m, Y = 0.90m to 2.55m):
      3-bay chamfered open cutout glazed with `glass_synth_chamber_translucent.png` (`alphaMode: "BLEND"`, `alpha ~ 0.18`)
    - South Bulkhead (+Z = +3.95m) with open center portal cutout for `corridor_door_winner_01` and camera sightlines.
    """
    sm = []
    slate_parts = [
        # Floor deck (7.0m W x 8.0m D, Y = 0.00..0.06m)
        make_beveled_box((7.00, 0.06, 8.00), center=(0.0, 0.03, 0.0), bevel=0.015),
        # East & West lower wainscot sills
        make_beveled_box((0.10, 0.96, 7.88), center=(3.45, 0.51, 0.0), bevel=0.02),
        make_beveled_box((0.10, 0.96, 7.88), center=(-3.45, 0.51, 0.0), bevel=0.02),
        # North wall lower sill below panoramic window (Y = 0.06..0.90m)
        make_beveled_box((6.88, 0.84, 0.10), center=(0.0, 0.48, -3.95), bevel=0.02),
    ]
    add_part(sm, "Room03_CarbonSlateDeckAndWainscot", merge_geometries(slate_parts), mats["carbon_slate"])

    gunmetal_parts = [
        # Ceiling deck (Y = 3.14..3.20m)
        make_beveled_box((7.00, 0.06, 8.00), center=(0.0, 3.17, 0.0), bevel=0.015),
        # East & West upper titanium walls
        make_beveled_box((0.10, 2.18, 7.88), center=(3.45, 2.06, 0.0), bevel=0.02),
        make_beveled_box((0.10, 2.18, 7.88), center=(-3.45, 2.06, 0.0), bevel=0.02),
        # North wall header & side piers around the 5.2m wide 3-bay panoramic viewport (X = -2.60..+2.60, Y = 0.90..2.55)
        make_beveled_box((6.88, 0.60, 0.10), center=(0.0, 2.85, -3.95), bevel=0.02),
        make_beveled_box((0.88, 1.68, 0.10), center=(-3.02, 1.72, -3.95), bevel=0.02),
        make_beveled_box((0.88, 1.68, 0.10), center=(3.02, 1.72, -3.95), bevel=0.02),
        # South Entry Airlock Bulkhead (Z = +3.95m) with wide open center portal/camera cutout
        make_beveled_box((2.10, 3.08, 0.10), center=(-2.40, 1.58, 3.95), bevel=0.02),
        make_beveled_box((2.10, 3.08, 0.10), center=(2.40, 1.58, 3.95), bevel=0.02),
        make_beveled_box((2.76, 0.52, 0.10), center=(0.0, 2.88, 3.95), bevel=0.02),
    ]
    for z_rib in [-3.80, -1.90, 0.00, 1.90, 3.80]:
        gunmetal_parts.extend([
            make_beveled_box((0.18, 3.08, 0.20), center=(-3.38, 1.58, z_rib), bevel=0.025),
            make_beveled_box((0.18, 3.08, 0.20), center=(3.38, 1.58, z_rib), bevel=0.025),
            make_beveled_box((6.88, 0.18, 0.20), center=(0.0, 3.06, z_rib), bevel=0.025),
            transform_geom(make_beveled_box((0.68, 0.16, 0.20), bevel=0.02), translate=(-3.10, 2.82, z_rib), rot_xyz_deg=(0.0, 0.0, 45.0)),
            transform_geom(make_beveled_box((0.68, 0.16, 0.20), bevel=0.02), translate=(3.10, 2.82, z_rib), rot_xyz_deg=(0.0, 0.0, -45.0)),
        ])
    add_part(sm, "Room03_OctagonalGunmetalRibsAndWalls", merge_geometries(gunmetal_parts), mats["gunmetal"])

    white_coffers = []
    for z_cof in [-2.85, -0.95, 0.95, 2.85]:
        white_coffers.append(make_beveled_box((5.40, 0.05, 1.62), center=(0.0, 3.12, z_cof), bevel=0.015))
    add_part(sm, "Room03_AerospaceWhiteCeilingCoffers", merge_geometries(white_coffers), mats["aero_white"])

    steel_parts = [
        make_beveled_box((0.12, 0.05, 7.84), center=(3.40, 0.98, 0.0), bevel=0.01),
        make_beveled_box((0.12, 0.05, 7.84), center=(-3.40, 0.98, 0.0), bevel=0.01),
        # North 3-bay panoramic window bezel & 2 vertical mullions (X = -0.86m and +0.86m)
        make_portal_oct_ring(5.24, 1.68, center_y=1.72, z_pos=-3.92, tube_r=0.032, chamfer=0.24),
        make_beveled_box((0.06, 1.64, 0.14), center=(-0.86, 1.72, -3.93), bevel=0.012),
        make_beveled_box((0.06, 1.64, 0.14), center=(0.86, 1.72, -3.93), bevel=0.012),
    ]
    for z_strip in [-2.85, -0.95, 0.95, 2.85]:
        steel_parts.append(make_beveled_box((6.76, 0.010, 0.06), center=(0.0, 0.062, z_strip), bevel=0.002))
    add_part(sm, "Room03_MachinedSteelBezelsAndStrips", merge_geometries(steel_parts), mats["steel_machined"])

    cyan_parts = [
        make_beveled_box((0.05, 0.03, 7.50), center=(-2.85, 2.98, 0.0), bevel=0.005),
        make_beveled_box((0.05, 0.03, 7.50), center=(2.85, 2.98, 0.0), bevel=0.005),
        make_beveled_box((5.10, 0.024, 0.04), center=(0.0, 0.91, -3.90), bevel=0.004),
    ]
    add_part(sm, "Room03_OrbitalCyanCovesAndWindowRim", merge_geometries(cyan_parts), mats["led_cyan"])

    amber_parts = [
        make_beveled_box((0.04, 0.012, 7.50), center=(-0.45, 0.063, 0.0), bevel=0.003),
        make_beveled_box((0.04, 0.012, 7.50), center=(1.85, 0.063, 0.0), bevel=0.003),
    ]
    add_part(sm, "Room03_CircadianAmberFloorGuides", merge_geometries(amber_parts), mats["led_amber"])

    # North 3-Bay Panoramic Window Translucent Glass (alphaMode: BLEND)
    north_glass = make_quad_panel((-2.58, 0.91, -3.94), (2.58, 0.91, -3.94), (2.58, 2.54, -3.94), (-2.58, 2.54, -3.94))
    add_part(sm, "Room03_NorthPanoramicTranslucentGlass", north_glass, mats["glass_chamber"])

    primary_p = os.path.join(ROOMS_GLB_DIR, "room_03_shell.glb")
    info = center_and_export_glb(primary_p, sm, root_name="Room03_MessGalleyShell")
    alias_paths = [
        os.path.join(ROOMS_GLB_DIR, "room_03_mess_shell.glb"),
        os.path.join(ROOMS_GLB_DIR, "room_03_mess_galley_shell.glb"),
        "/workspace/game-project/assets/glb/room_03_shell.glb",
        "/workspace/game-project/assets/glb/room_03_mess_shell.glb",
        "/workspace/game-project/assets/glb/room_03_mess_galley_shell.glb",
    ]
    for ap in alias_paths:
        shutil.copyfile(primary_p, ap)
    print(f"[room_03_shell] Exported {primary_p} + 5 alias paths ({info['triangles']} tris)")
    return info


def build_all_galley_round1():
    mats = get_galley_materials()
    builders = [
        build_01_octagonal_ration_synthesizer,
        build_02_dual_zone_split_synthesizer,
        build_03_rotary_carousel_automaton,
        build_04_cantilevered_island_galley,
        build_05_quad_chamber_induction_synthesizer,
    ]
    results = []
    for fn in builders:
        info = fn(mats)
        fname = os.path.basename(info["filepath"])
        dims = info["dimensions"]
        print(
            f"[galley_r1] Built {fname:24s} | {dims[0]:.2f}m W x {dims[2]:.2f}m D x {dims[1]:.2f}m H | "
            f"verts={info['vertices']:4d} | tris={info['triangles']:4d} | min_y={info['min'][1]:.5f}"
        )
        results.append(info)

    with open(os.path.join(OUT_GLB_DIR, "galley_r1_manifest.json"), "w") as f:
        json.dump(results, f, indent=2)

    build_mess_dining_booth(mats)
    build_room_03_mess_galley_shell(mats)
    return results


if __name__ == "__main__":
    build_all_galley_round1()
