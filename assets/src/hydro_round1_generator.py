#!/usr/bin/env python3
"""
Builds all 5 Round-1 Hard Sci-Fi Room 06 Hero Asset (Vertical Translucent Aeroponic Planter
& Bio-Air Scrubber Tower) .glb models:
  /workspace/game-project/assets/glb/hydro_round1/hydro_column_r1_01.glb .. hydro_column_r1_05.glb
Plus exports Winner #02 to /workspace/game-project/assets/glb/winners/,
the Central Nutrient & Botanical Analysis Island (hydro_sample_bench.glb),
and the Room 06 Architectural Shell (room_06_shell.glb & aliases).

Follows /workspace/game-project/design/hydro_round1/hydro_column_r1_spec.md ("Aegis-7 Standard"):
- Bottom-center (0.0, 0.0, 0.0) floor pivot (min_y == 0.0000, centered X and Z), front facing +Z
- Polygon budget: 3,500 - 5,800 triangles per candidate
- Mandatory 4-Part 3D Aeroponic & Bio-Scrubber Kit in every candidate:
  1. 45° Chamfered Octagonal Base Sump & Overhead O2 Scrubber Crown with laminar air-scrubber louvers
  2. Translucent Borosilicate Aeroponic Growth Column (glass_hydro_cylinder_translucent.png, alphaMode: "BLEND", alpha ~ 0.19)
     housing a central brushed-steel ultrasonic misting spindle + 4 stacked aerospace-white rotary planter trays
     overflowing with 3D sculpted emerald/jade botanical foliage clusters (foliage_aeroponic_herbs.png)
     and alternating UV-Violet (#7B5CFF) & Daylight Ice-White (#E0F4FF) grow-light halos
  3. Illuminated Chlorella Algae / Zeolite O2 Bio-Scrubber Cylinders & Nutrient Dosing Manifold with
     swept steel pipes and signal-orange rotary purge valves
  4. Photosynthetic & O2 Exchange OLED Telemetry Console (oled_hydro_bioscrubber.png)
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
    make_curved_leaf_blade,
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
from climate_round1_generator import make_laminar_louvers

TEX_HYDRO_DIR = "/workspace/game-project/assets/textures/hydro_round1"
OUT_GLB_DIR = "/workspace/game-project/assets/glb/hydro_round1"
WINNERS_DIR = "/workspace/game-project/assets/glb/winners"
ROOMS_DIR = "/workspace/game-project/assets/glb/rooms"
os.makedirs(OUT_GLB_DIR, exist_ok=True)
os.makedirs(WINNERS_DIR, exist_ok=True)
os.makedirs(ROOMS_DIR, exist_ok=True)


def tex_hy(fname: str) -> str:
    return os.path.join(TEX_HYDRO_DIR, fname)


def get_hydro_materials():
    return {
        "gunmetal": PBRMaterialDef(
            name="Mat_Titanium_GunmetalHull",
            base_color=hex_rgba("#1A1E24"),
            metallic=0.78,
            roughness=0.34,
            texture_path=tex_hy("titanium_gunmetal_hull.png"),
        ),
        "aero_white": PBRMaterialDef(
            name="Mat_Composite_AerospaceWhite",
            base_color=hex_rgba("#D8DEE6"),
            metallic=0.08,
            roughness=0.28,
            texture_path=tex_hy("composite_aerospace_white.png"),
        ),
        "carbon_slate": PBRMaterialDef(
            name="Mat_Carbon_SlateFrame",
            base_color=hex_rgba("#282E38"),
            metallic=0.58,
            roughness=0.40,
            texture_path=tex_hy("carbon_slate_frame.png"),
        ),
        "steel_machined": PBRMaterialDef(
            name="Mat_Steel_MachinedGantry",
            base_color=hex_rgba("#88929E"),
            metallic=0.90,
            roughness=0.20,
            texture_path=tex_hy("steel_machined_gantry.png"),
        ),
        "foliage_herbs": PBRMaterialDef(
            name="Mat_Foliage_AeroponicHerbs",
            base_color=hex_rgba("#2E5A36"),
            metallic=0.0,
            roughness=0.52,
            texture_path=tex_hy("foliage_aeroponic_herbs.png"),
            double_sided=True,
        ),
        "accent_orange": PBRMaterialDef(
            name="Mat_Accent_SignalOrange",
            base_color=hex_rgba("#D95B26"),
            metallic=0.06,
            roughness=0.48,
            texture_path=tex_hy("accent_signal_orange.png"),
        ),
        "oled_bio": PBRMaterialDef(
            name="Mat_OLED_HydroBioscrubber",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.10,
            roughness=0.14,
            emissive=(0.35, 0.90, 1.0),
            texture_path=tex_hy("oled_hydro_bioscrubber.png"),
        ),
        "glass_hydro": PBRMaterialDef(
            name="Mat_Glass_HydroCylinder_Translucent",
            base_color=(0.50, 0.90, 0.96, 0.19),
            metallic=0.10,
            roughness=0.08,
            emissive=(0.0, 0.14, 0.18),
            texture_path=tex_hy("glass_hydro_cylinder_translucent.png"),
            double_sided=True,
            alpha_mode="BLEND",
        ),
        "led_uv": PBRMaterialDef(
            name="Mat_Emissive_UVGrowLED",
            base_color=hex_rgba("#7B5CFF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.55, 0.38, 1.0),
            texture_path=tex_hy("led_uv_violet.png"),
        ),
        "led_ice": PBRMaterialDef(
            name="Mat_Emissive_IceDaylightLED",
            base_color=hex_rgba("#E0F4FF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.86, 0.95, 1.0),
            texture_path=tex_hy("led_ice_white.png"),
        ),
        "led_cyan": PBRMaterialDef(
            name="Mat_Emissive_CyanBioLED",
            base_color=hex_rgba("#00E5FF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.0, 0.90, 1.0),
            texture_path=tex_hy("led_cyan_strip.png"),
        ),
        "led_amber": PBRMaterialDef(
            name="Mat_Emissive_AmberLED",
            base_color=hex_rgba("#FF9500"),
            metallic=0.0,
            roughness=0.15,
            emissive=(1.0, 0.58, 0.0),
            texture_path=tex_hy("led_amber_strip.png"),
        ),
    }


# ==============================================================================
# SHARED 3D AEROPONIC PLANTER TIERS, FOLIAGE CLUSTERS & ALGAE BIOREACTOR HELPERS
# ==============================================================================
def make_aeroponic_rotary_column_kit(
    col_cx: float = 0.0,
    col_cz: float = 0.0,
    y_bot: float = 0.38,
    y_top: float = 2.18,
    tray_radius: float = 0.34,
    num_tiers: int = 4,
):
    """
    Builds Part 2 of the Mandatory 4-Part Aeroponic Kit:
    - Central brushed-steel ultrasonic misting spindle
    - 4 stacked aerospace-white rotary planter trays
    - Lush 3D sculpted emerald/jade botanical foliage clusters & arched leaf blades on each tier
    - Alternating UV-Violet (#7B5CFF) & Daylight Ice-White (#E0F4FF) grow-light halos
    - Open-top / front translucent borosilicate glass cylinder (alphaMode: "BLEND")
    Returns: (steel_spindle_geom, white_trays_geom, foliage_geom, uv_halos_geom, ice_halos_geom, glass_enclosure_geom)
    """
    col_h = y_top - y_bot
    steel_spindle = [
        make_cylinder(0.055, 0.055, col_h + 0.08, center=(col_cx, y_bot + col_h * 0.5, col_cz), segments=14, axis="y"),
    ]
    white_trays = []
    foliage_parts = []
    uv_halos = []
    ice_halos = []

    for t_idx in range(num_tiers):
        ty = y_bot + 0.16 + t_idx * ((col_h - 0.32) / max(1, num_tiers - 1))
        # Rotary aerospace-white planter ring tray
        white_trays.append(make_cylinder(tray_radius, tray_radius * 0.86, 0.065, center=(col_cx, ty, col_cz), segments=18, axis="y"))
        steel_spindle.append(make_cylinder(0.085, 0.085, 0.05, center=(col_cx, ty + 0.05, col_cz), segments=12, axis="y"))

        # 5 sculpted botanical foliage pillows arranged radially around the tray
        for k in range(5):
            ang_deg = k * 72.0 + (t_idx * 28.0)
            ang_rad = math.radians(ang_deg)
            fx = col_cx + (tray_radius * 0.70) * math.sin(ang_rad)
            fz = col_cz + (tray_radius * 0.70) * math.cos(ang_rad)
            foliage_parts.append(
                make_sculpted_cushion(
                    (0.18, 0.12, 0.18),
                    center=(fx, ty + 0.08, fz),
                    res=(4, 2, 3),
                    roundness=0.48,
                    belly_puff=0.07,
                    crease_freq=3,
                )
            )

        # Overhead grow-light halo above each tier
        halo_y = ty + 0.24
        halo_geom = make_cylinder(tray_radius * 0.92, tray_radius * 0.92, 0.022, center=(col_cx, halo_y, col_cz), segments=16, axis="y")
        if t_idx % 2 == 0:
            uv_halos.append(halo_geom)
        else:
            ice_halos.append(halo_geom)

    # Front faceted translucent borosilicate glass enclosure panels (alphaMode: "BLEND")
    r_glass = tray_radius + 0.08
    glass_panes = [
        make_quad_panel((col_cx - r_glass * 0.65, y_bot, col_cz + r_glass), (col_cx + r_glass * 0.65, y_bot, col_cz + r_glass), (col_cx + r_glass * 0.65, y_top, col_cz + r_glass), (col_cx - r_glass * 0.65, y_top, col_cz + r_glass)),
        make_quad_panel((col_cx - r_glass, y_bot, col_cz + r_glass * 0.45), (col_cx - r_glass * 0.65, y_bot, col_cz + r_glass), (col_cx - r_glass * 0.65, y_top, col_cz + r_glass), (col_cx - r_glass, y_top, col_cz + r_glass * 0.45)),
        make_quad_panel((col_cx + r_glass * 0.65, y_bot, col_cz + r_glass), (col_cx + r_glass, y_bot, col_cz + r_glass * 0.45), (col_cx + r_glass, y_top, col_cz + r_glass * 0.45), (col_cx + r_glass * 0.65, y_top, col_cz + r_glass)),
    ]

    return (
        merge_geometries(steel_spindle),
        merge_geometries(white_trays),
        merge_geometries(foliage_parts),
        merge_geometries(uv_halos),
        merge_geometries(ice_halos),
        merge_geometries(glass_panes),
    )


def make_algae_bioscrubber_and_nutrient_manifold(
    bay_cx: float,
    bay_cz: float = 0.0,
    oled_y: float = 1.15,
):
    """
    Builds Part 3 & Part 4 of the Mandatory Aeroponic Kit:
    - Twin vertical translucent Chlorella Algae / Zeolite Bioreactor Cylinders with glowing cyan (#00E5FF) cores
    - Flush OLED Photosynthetic & O2 Telemetry Console (oled_hydro_bioscrubber.png)
    - Twin aerospace-white nutrient reservoir canisters, swept steel manifold pipes & peristaltic dosing pumps
    - Sculpted signal-orange rotary purge handwheel & CO2 bypass valves
    Returns: (white_tanks_geom, steel_pipes_pumps_geom, orange_wheel_valves_geom, oled_screen_geom,
              cyan_reactor_cores_geom, glass_reactor_tubes_geom)
    """
    # 1. Lower Twin Aerospace-White Nutrient Reservoir Canisters (Y = 0.16..0.76m)
    white_tanks = [
        make_cylinder(0.072, 0.072, 0.48, center=(bay_cx - 0.14, 0.44, bay_cz + 0.04), segments=12, axis="y"),
        make_cylinder(0.072, 0.072, 0.48, center=(bay_cx + 0.14, 0.44, bay_cz + 0.04), segments=12, axis="y"),
    ]

    # 2. Upper Twin Chlorella Algae / Zeolite Bioreactor Glowing Cyan Cores & Translucent Glass Tubes (Y = 1.48..2.18m)
    cyan_cores = [
        make_cylinder(0.042, 0.042, 0.62, center=(bay_cx - 0.14, 1.82, bay_cz + 0.06), segments=12, axis="y"),
        make_cylinder(0.042, 0.042, 0.62, center=(bay_cx + 0.14, 1.82, bay_cz + 0.06), segments=12, axis="y"),
    ]
    glass_tubes = [
        make_quad_panel((bay_cx - 0.24, 1.48, bay_cz + 0.22), (bay_cx + 0.24, 1.48, bay_cz + 0.22), (bay_cx + 0.24, 2.16, bay_cz + 0.22), (bay_cx - 0.24, 2.16, bay_cz + 0.22)),
    ]

    # 3. Machined-Steel Nutrient Manifold Pipes & Peristaltic Dosing Pumps
    pipe_l = sample_filleted_polyline([(bay_cx - 0.14, 0.68, bay_cz + 0.04), (bay_cx - 0.14, 0.82, bay_cz + 0.18), (bay_cx + 0.14, 0.82, bay_cz + 0.18), (bay_cx + 0.14, 0.68, bay_cz + 0.04)], 0.04, 4)
    steel_parts = [
        make_swept_tube(pipe_l, radius=0.018, radial_segments=8),
        make_cylinder(0.082, 0.082, 0.04, center=(bay_cx - 0.14, 1.50, bay_cz + 0.06), segments=12, axis="y"),
        make_cylinder(0.082, 0.082, 0.04, center=(bay_cx + 0.14, 1.50, bay_cz + 0.06), segments=12, axis="y"),
        make_cylinder(0.082, 0.082, 0.04, center=(bay_cx - 0.14, 2.14, bay_cz + 0.06), segments=12, axis="y"),
        make_cylinder(0.082, 0.082, 0.04, center=(bay_cx + 0.14, 2.14, bay_cz + 0.06), segments=12, axis="y"),
    ]

    wheel_or, wheel_st = make_rotary_override_handwheel(cx=bay_cx, cy=0.52, cz=bay_cz + 0.22, radius=0.095)
    steel_parts.append(wheel_st)
    orange_parts = [
        wheel_or,
        make_cylinder(0.042, 0.052, 0.07, center=(bay_cx - 0.14, 0.71, bay_cz + 0.04), segments=10, axis="y"),
        make_cylinder(0.042, 0.052, 0.07, center=(bay_cx + 0.14, 0.71, bay_cz + 0.04), segments=10, axis="y"),
    ]

    oled_screen = make_quad_panel(
        (bay_cx - 0.24, oled_y - 0.16, bay_cz + 0.24),
        (bay_cx + 0.24, oled_y - 0.16, bay_cz + 0.24),
        (bay_cx + 0.24, oled_y + 0.22, bay_cz + 0.24),
        (bay_cx - 0.24, oled_y + 0.22, bay_cz + 0.24),
    )

    return (
        merge_geometries(white_tanks),
        merge_geometries(steel_parts),
        merge_geometries(orange_parts),
        oled_screen,
        merge_geometries(cyan_cores),
        merge_geometries(glass_tubes),
    )


# ==============================================================================
# CANDIDATE 01: AEGIS-7 OCTAGONAL TRANSLUCENT AEROPONIC BIO-TOWER (`hydro_column_r1_01.glb`)
# Dimensions: 1.90m W x 0.90m D x 2.45m H
# ==============================================================================
def build_01_octagonal_aeroponic_biotower(mats):
    sm = []
    hull = [
        make_beveled_box((1.90, 0.34, 0.90), center=(0.0, 0.17, 0.0), bevel=0.035),
        make_beveled_box((1.90, 0.24, 0.90), center=(0.0, 2.33, 0.0), bevel=0.035),
        make_beveled_box((0.18, 1.92, 0.86), center=(-0.86, 1.28, 0.0), bevel=0.035),
        make_beveled_box((0.52, 1.92, 0.86), center=(0.69, 1.28, -0.02), bevel=0.035),
        make_beveled_box((1.32, 1.92, 0.08), center=(-0.18, 1.28, -0.40), bevel=0.02),
    ]
    add_part(sm, "Hydro01_OctagonalGunmetalSumpAndCrown", merge_geometries(hull), mats["gunmetal"])

    louvers, _ = make_laminar_louvers(cx=-0.18, cy=2.33, cz=0.42, width_x=0.96, height_y=0.14, num_blades=4)
    add_part(sm, "Hydro01_TopScrubberLouvers", louvers, mats["carbon_slate"])

    spindle, trays, foliage, uv_h, ice_h, glass_col = make_aeroponic_rotary_column_kit(
        col_cx=-0.20, col_cz=0.0, y_bot=0.36, y_top=2.20, tray_radius=0.38, num_tiers=4
    )
    w_m, st_m, or_m, oled_m, cy_m, gl_m = make_algae_bioscrubber_and_nutrient_manifold(
        bay_cx=0.66, bay_cz=0.18, oled_y=1.16
    )

    add_part(sm, "Hydro01_WhiteRotaryPlanterTraysAndTanks", merge_geometries([trays, w_m]), mats["aero_white"])
    add_part(sm, "Hydro01_SculptedAeroponicFoliage", foliage, mats["foliage_herbs"])
    add_part(sm, "Hydro01_MachinedMistingSpindleAndPipes", merge_geometries([spindle, st_m]), mats["steel_machined"])
    add_part(sm, "Hydro01_SignalOrangeDosingValves", or_m, mats["accent_orange"])

    add_part(sm, "Hydro01_OLEDPhotosyntheticConsole", oled_m, mats["oled_bio"])
    add_part(sm, "Hydro01_UVVioletGrowHalos", uv_h, mats["led_uv"])
    add_part(sm, "Hydro01_DaylightIceGrowHalos", ice_h, mats["led_ice"])
    add_part(sm, "Hydro01_CyanBioreactorCores", cy_m, mats["led_cyan"])
    add_part(sm, "Hydro01_AmberSumpLED", make_beveled_box((1.56, 0.022, 0.04), center=(0.0, 0.14, 0.44), bevel=0.004), mats["led_amber"])
    add_part(sm, "Hydro01_TranslucentBorosilicateColumn", merge_geometries([glass_col, gl_m]), mats["glass_hydro"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "hydro_column_r1_01.glb"), sm, root_name="HydroColumnR1_01_OctagonalBioTower")


# ==============================================================================
# CANDIDATE 02: DUAL-ZONE SPLIT AEROPONIC ROTARY COLUMN & O2 ALGAE BIO-SCRUBBER BAY (`hydro_column_r1_02.glb`)
# Dimensions: 2.00m W x 0.90m D x 2.45m H (Signature 65/35 Aegis-7 Split-Bay Sibling!)
# ==============================================================================
def build_02_dual_zone_split_aeroponic_bioscrubber(mats):
    sm = []
    # 1. Asymmetric 65% / 35% Split-Bay Frame (Left Aeroponic Column: X=-1.00..+0.30, Right Bioreactor Bay: X=+0.30..+1.00)
    hull = [
        make_beveled_box((2.00, 0.32, 0.90), center=(0.0, 0.16, 0.0), bevel=0.035),
        make_beveled_box((2.00, 0.24, 0.90), center=(0.0, 2.33, 0.0), bevel=0.035),
        make_beveled_box((0.14, 1.94, 0.88), center=(-0.93, 1.28, 0.0), bevel=0.035),
        make_beveled_box((0.14, 1.94, 0.88), center=(0.93, 1.28, 0.0), bevel=0.035),
        # Center structural partition at X = +0.30
        make_beveled_box((0.10, 1.94, 0.86), center=(0.30, 1.28, 0.0), bevel=0.025),
        make_beveled_box((1.84, 1.94, 0.08), center=(0.0, 1.28, -0.40), bevel=0.02),
        # Right Bay horizontal dividers at Y = 0.84m and Y = 1.44m
        make_beveled_box((0.56, 0.04, 0.80), center=(0.62, 0.84, 0.0), bevel=0.01),
        make_beveled_box((0.56, 0.04, 0.80), center=(0.62, 1.44, 0.0), bevel=0.01),
    ]
    add_part(sm, "Hydro02_SplitBayGunmetalHull", merge_geometries(hull), mats["gunmetal"])

    louvers, _ = make_laminar_louvers(cx=0.62, cy=2.33, cz=0.42, width_x=0.52, height_y=0.14, num_blades=4)
    add_part(sm, "Hydro02_TopO2ExhaustLouvers", louvers, mats["carbon_slate"])

    # 2. Left Bay Rotary Aeroponic Planter Column (centered at X = -0.32) + Right Bay Algae Bio-Scrubber & OLED
    spindle, trays, foliage, uv_h, ice_h, glass_col = make_aeroponic_rotary_column_kit(
        col_cx=-0.32, col_cz=0.02, y_bot=0.34, y_top=2.20, tray_radius=0.40, num_tiers=4
    )
    w_m, st_m, or_m, oled_m, cy_m, gl_m = make_algae_bioscrubber_and_nutrient_manifold(
        bay_cx=0.62, bay_cz=0.18, oled_y=1.14
    )

    add_part(sm, "Hydro02_WhitePlanterRingsAndReservoirs", merge_geometries([trays, w_m]), mats["aero_white"])
    add_part(sm, "Hydro02_SculptedEmeraldFoliageClusters", foliage, mats["foliage_herbs"])

    left_bezel = make_portal_oct_ring(1.12, 1.88, center_y=1.28, z_pos=0.42, tube_r=0.028, chamfer=0.20)
    left_bezel[0][:, 0] -= 0.32
    add_part(sm, "Hydro02_MachinedSpindleBezelAndManifold", merge_geometries([spindle, st_m, left_bezel]), mats["steel_machined"])
    add_part(sm, "Hydro02_SignalOrangePurgeHandwheelAndValves", or_m, mats["accent_orange"])

    add_part(sm, "Hydro02_RightBayOLEDTelemetry", oled_m, mats["oled_bio"])
    add_part(sm, "Hydro02_UVVioletGrowHalos", uv_h, mats["led_uv"])
    add_part(sm, "Hydro02_DaylightIceGrowHalos", ice_h, mats["led_ice"])
    add_part(sm, "Hydro02_CyanAlgaeBioreactorCores", cy_m, mats["led_cyan"])
    add_part(
        sm,
        "Hydro02_AmberSumpAndShelfLED",
        merge_geometries([
            make_beveled_box((1.68, 0.022, 0.04), center=(0.0, 0.14, 0.44), bevel=0.004),
            make_beveled_box((0.50, 0.020, 0.03), center=(0.62, 0.82, 0.41), bevel=0.004),
        ]),
        mats["led_amber"],
    )
    add_part(sm, "Hydro02_TranslucentBorosilicateEnclosures", merge_geometries([glass_col, gl_m]), mats["glass_hydro"])

    out_p = os.path.join(OUT_GLB_DIR, "hydro_column_r1_02.glb")
    info = center_and_export_glb(out_p, sm, root_name="HydroColumnR1_02_DualZoneSplitBioScrubber")

    # Copy Winner #02 to all canonical winner aliases
    for w_alias in [
        "hydro_column_winner_01_split_aeroponic_bioscrubber.glb",
        "hydro_column_winner_01_dual_zone_bioscrubber.glb",
        "hydro_column_winner_01_aeroponic_tower.glb",
        "hydro_column_winner_01.glb",
    ]:
        shutil.copyfile(out_p, os.path.join(WINNERS_DIR, w_alias))
    return info


# ==============================================================================
# CANDIDATE 03: TWIN-HELIX VERTICAL BIOREACTOR & MICRO-GREENS CAROUSEL (`hydro_column_r1_03.glb`)
# Dimensions: 1.95m W x 0.90m D x 2.45m H
# ==============================================================================
def build_03_twin_helix_carousel(mats):
    sm = []
    hull = [
        make_beveled_box((1.95, 0.32, 0.90), center=(0.0, 0.16, 0.0), bevel=0.035),
        make_beveled_box((1.95, 0.24, 0.90), center=(0.0, 2.33, 0.0), bevel=0.035),
        make_beveled_box((0.36, 1.94, 0.86), center=(0.0, 1.28, -0.02), bevel=0.03),
        make_beveled_box((1.82, 1.94, 0.08), center=(0.0, 1.28, -0.40), bevel=0.02),
    ]
    add_part(sm, "Hydro03_TwinCarouselGunmetalHull", merge_geometries(hull), mats["gunmetal"])

    sp_l, tr_l, fol_l, uv_l, ice_l, gl_l = make_aeroponic_rotary_column_kit(
        col_cx=-0.52, col_cz=0.02, y_bot=0.34, y_top=2.20, tray_radius=0.28, num_tiers=2
    )
    sp_r, tr_r, fol_r, uv_r, ice_r, gl_r = make_aeroponic_rotary_column_kit(
        col_cx=0.52, col_cz=0.02, y_bot=0.34, y_top=2.20, tray_radius=0.28, num_tiers=2
    )
    w_m, st_m, or_m, oled_m, cy_m, _ = make_algae_bioscrubber_and_nutrient_manifold(
        bay_cx=0.0, bay_cz=0.18, oled_y=1.22
    )

    add_part(sm, "Hydro03_WhiteTwinPlanterTrays", merge_geometries([tr_l, tr_r, w_m]), mats["aero_white"])
    add_part(sm, "Hydro03_TwinCarouselFoliage", merge_geometries([fol_l, fol_r]), mats["foliage_herbs"])
    add_part(sm, "Hydro03_MachinedSpindlesAndManifold", merge_geometries([sp_l, sp_r, st_m]), mats["steel_machined"])
    add_part(sm, "Hydro03_SignalOrangeValves", or_m, mats["accent_orange"])

    add_part(sm, "Hydro03_CenterOLEDConsole", oled_m, mats["oled_bio"])
    add_part(sm, "Hydro03_UVGrowHalos", merge_geometries([uv_l, uv_r]), mats["led_uv"])
    add_part(sm, "Hydro03_IceGrowHalos", merge_geometries([ice_l, ice_r]), mats["led_ice"])
    add_part(sm, "Hydro03_CyanReactorCores", cy_m, mats["led_cyan"])
    add_part(sm, "Hydro03_AmberSumpLED", make_beveled_box((1.62, 0.022, 0.04), center=(0.0, 0.14, 0.44), bevel=0.004), mats["led_amber"])
    add_part(sm, "Hydro03_TwinTranslucentGlassColumns", merge_geometries([gl_l, gl_r]), mats["glass_hydro"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "hydro_column_r1_03.glb"), sm, root_name="HydroColumnR1_03_TwinHelixCarousel")


# ==============================================================================
# CANDIDATE 04: HEX-FACETED TERRACED TERRARIUM ALCOVE & UV MIST GANTRY (`hydro_column_r1_04.glb`)
# Dimensions: 2.02m W x 0.92m D x 2.45m H
# ==============================================================================
def build_04_hex_terraced_terrarium(mats):
    sm = []
    hull = [
        make_beveled_box((2.02, 0.32, 0.92), center=(0.0, 0.16, 0.0), bevel=0.035),
        make_beveled_box((2.02, 0.24, 0.92), center=(0.0, 2.33, 0.0), bevel=0.035),
        make_beveled_box((0.16, 1.94, 0.88), center=(-0.93, 1.28, 0.0), bevel=0.035),
        make_beveled_box((0.52, 1.94, 0.88), center=(0.74, 1.28, 0.0), bevel=0.035),
        make_beveled_box((1.88, 1.94, 0.08), center=(0.0, 1.28, -0.42), bevel=0.02),
    ]
    add_part(sm, "Hydro04_HexTerrariumCarbonHull", merge_geometries(hull), mats["carbon_slate"])

    spindle, trays, foliage, uv_h, ice_h, glass_col = make_aeroponic_rotary_column_kit(
        col_cx=-0.24, col_cz=0.02, y_bot=0.34, y_top=2.20, tray_radius=0.40, num_tiers=4
    )
    w_m, st_m, or_m, oled_m, cy_m, gl_m = make_algae_bioscrubber_and_nutrient_manifold(
        bay_cx=0.72, bay_cz=0.18, oled_y=1.16
    )

    add_part(sm, "Hydro04_WhiteTerracedTroughs", merge_geometries([trays, w_m]), mats["aero_white"])
    add_part(sm, "Hydro04_TerracedBotanicalFoliage", foliage, mats["foliage_herbs"])

    hex_ring = make_portal_oct_ring(1.22, 1.90, center_y=1.28, z_pos=0.42, tube_r=0.030, chamfer=0.28)
    hex_ring[0][:, 0] -= 0.24
    add_part(sm, "Hydro04_MachinedHexGantryAndPipes", merge_geometries([spindle, st_m, hex_ring]), mats["steel_machined"])
    add_part(sm, "Hydro04_SignalOrangeValves", or_m, mats["accent_orange"])

    add_part(sm, "Hydro04_OLEDTelemetryConsole", oled_m, mats["oled_bio"])
    add_part(sm, "Hydro04_UVGrowBars", uv_h, mats["led_uv"])
    add_part(sm, "Hydro04_IceGrowBars", ice_h, mats["led_ice"])
    add_part(sm, "Hydro04_CyanReactorCores", cy_m, mats["led_cyan"])
    add_part(sm, "Hydro04_AmberBaseLED", make_beveled_box((1.66, 0.022, 0.04), center=(0.0, 0.14, 0.45), bevel=0.004), mats["led_amber"])
    add_part(sm, "Hydro04_HexFacetedTranslucentDoors", merge_geometries([glass_col, gl_m]), mats["glass_hydro"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "hydro_column_r1_04.glb"), sm, root_name="HydroColumnR1_04_HexTerracedTerrarium")


# ==============================================================================
# CANDIDATE 05: ZERO-G CENTRIFUGAL DRUM PLANTER & ATMOSPHERIC REVITALIZER (`hydro_column_r1_05.glb`)
# Dimensions: 1.98m W x 0.94m D x 2.48m H
# ==============================================================================
def build_05_centrifugal_drum_revitalizer(mats):
    sm = []
    hull = [
        make_beveled_box((1.98, 0.34, 0.94), center=(0.0, 0.17, 0.0), bevel=0.035),
        make_beveled_box((1.98, 0.24, 0.94), center=(0.0, 2.36, 0.0), bevel=0.035),
        make_beveled_box((0.18, 1.96, 0.90), center=(-0.90, 1.30, 0.0), bevel=0.035),
        make_beveled_box((0.52, 1.96, 0.90), center=(0.72, 1.30, 0.0), bevel=0.035),
        make_beveled_box((1.84, 1.96, 0.08), center=(0.0, 1.30, -0.42), bevel=0.02),
    ]
    add_part(sm, "Hydro05_CentrifugeGunmetalHull", merge_geometries(hull), mats["gunmetal"])

    spindle, trays, foliage, uv_h, ice_h, glass_col = make_aeroponic_rotary_column_kit(
        col_cx=-0.22, col_cz=0.02, y_bot=0.36, y_top=2.22, tray_radius=0.39, num_tiers=4
    )
    w_m, st_m, or_m, oled_m, cy_m, gl_m = make_algae_bioscrubber_and_nutrient_manifold(
        bay_cx=0.70, bay_cz=0.18, oled_y=1.18
    )

    add_part(sm, "Hydro05_WhiteCentrifugeDrumRings", merge_geometries([trays, w_m]), mats["aero_white"])
    add_part(sm, "Hydro05_CentrifugeBotanicalFoliage", foliage, mats["foliage_herbs"])
    add_part(sm, "Hydro05_MachinedDrumTrunnionsAndPipes", merge_geometries([spindle, st_m]), mats["steel_machined"])
    add_part(sm, "Hydro05_SignalOrangeValves", or_m, mats["accent_orange"])

    add_part(sm, "Hydro05_OLEDRevitalizerConsole", oled_m, mats["oled_bio"])
    add_part(sm, "Hydro05_AxialUVGrowLamp", uv_h, mats["led_uv"])
    add_part(sm, "Hydro05_DaylightGrowHalos", ice_h, mats["led_ice"])
    add_part(sm, "Hydro05_CyanBioreactorCores", cy_m, mats["led_cyan"])
    add_part(sm, "Hydro05_AmberSumpLED", make_beveled_box((1.64, 0.022, 0.04), center=(0.0, 0.14, 0.46), bevel=0.004), mats["led_amber"])
    add_part(sm, "Hydro05_TranslucentDrumEnclosure", merge_geometries([glass_col, gl_m]), mats["glass_hydro"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "hydro_column_r1_05.glb"), sm, root_name="HydroColumnR1_05_CentrifugalDrumRevitalizer")


# ==============================================================================
# ROOM 06 AUXILIARY PROP (`hydro_sample_bench.glb`) & SHELL (`room_06_shell.glb`)
# ==============================================================================
def build_hydro_sample_bench(mats):
    """
    Builds Central Nutrient & Botanical Analysis Island (hydro_sample_bench.glb):
    2.10m W x 1.05m D x 0.88m H chamfered aerospace-white & gunmetal island workbench
    with recessed illuminated seedling propagation tray (foliage_aeroponic_herbs.png),
    3D borosilicate sample flasks, microscope gantry, and front oled_hydro_bioscrubber.png panel.
    """
    sm = []
    base = [
        make_beveled_box((2.10, 0.14, 1.05), center=(0.0, 0.07, 0.0), bevel=0.03),
        make_beveled_box((1.92, 0.56, 0.88), center=(0.0, 0.42, 0.0), bevel=0.03),
    ]
    add_part(sm, "SampleBench_GunmetalPedestal", merge_geometries(base), mats["gunmetal"])

    countertop = [
        make_beveled_box((2.10, 0.12, 1.05), center=(0.0, 0.76, 0.0), bevel=0.03),
    ]
    add_part(sm, "SampleBench_AerospaceWhiteCountertop", merge_geometries(countertop), mats["aero_white"])

    # Recessed seedling propagation foliage clusters
    seedlings = []
    for sx in [-0.65, -0.35, -0.05, 0.25]:
        for sz in [-0.18, 0.18]:
            seedlings.append(
                make_sculpted_cushion((0.20, 0.09, 0.20), center=(sx, 0.84, sz), res=(4, 2, 3), roundness=0.45, belly_puff=0.05, crease_freq=3)
            )
    add_part(sm, "SampleBench_SeedlingPropagationFoliage", merge_geometries(seedlings), mats["foliage_herbs"])

    # Overhead microscope & UV grow-light gantry arch
    gantry_pts = sample_filleted_polyline([(-0.88, 0.82, 0.0), (-0.88, 1.34, 0.0), (0.88, 1.34, 0.0), (0.88, 0.82, 0.0)], 0.10, 5)
    steel_gantry = [
        make_swept_tube(gantry_pts, radius=0.026, radial_segments=10),
        make_cylinder(0.05, 0.03, 0.22, center=(0.62, 0.94, -0.15), segments=10, axis="y"),
    ]
    add_part(sm, "SampleBench_MicroscopeGantry", merge_geometries(steel_gantry), mats["steel_machined"])
    add_part(sm, "SampleBench_SignalOrangeValves", make_cylinder(0.035, 0.035, 0.04, center=(0.62, 0.52, 0.45), segments=10, axis="z"), mats["accent_orange"])

    add_part(
        sm,
        "SampleBench_FrontOLEDTelemetry",
        make_quad_panel((-0.36, 0.36, 0.45), (0.36, 0.36, 0.45), (0.36, 0.64, 0.45), (-0.36, 0.64, 0.45)),
        mats["oled_bio"],
    )
    add_part(sm, "SampleBench_OverheadUVGrowBar", make_beveled_box((1.56, 0.025, 0.05), center=(0.0, 1.30, 0.0), bevel=0.005), mats["led_uv"])
    add_part(sm, "SampleBench_CyanTrayRim", make_beveled_box((1.72, 0.020, 0.04), center=(0.0, 0.82, 0.51), bevel=0.004), mats["led_cyan"])

    # Translucent borosilicate sample flasks & seedling hood
    flasks = [
        make_cylinder(0.055, 0.055, 0.22, center=(0.62, 0.93, 0.18), segments=12, axis="y"),
        make_cylinder(0.045, 0.045, 0.18, center=(0.76, 0.91, 0.12), segments=12, axis="y"),
    ]
    add_part(sm, "SampleBench_TranslucentSampleFlasks", merge_geometries(flasks), mats["glass_hydro"])

    p_main = os.path.join(WINNERS_DIR, "hydro_sample_bench.glb")
    info = center_and_export_glb(p_main, sm, root_name="HydroSampleBench")
    for dst in [
        os.path.join(OUT_GLB_DIR, "hydro_sample_bench.glb"),
        os.path.join(ROOMS_DIR, "hydro_sample_bench.glb"),
        "/workspace/game-project/assets/glb/hydro_sample_bench.glb",
    ]:
        shutil.copyfile(p_main, dst)
    print(f"[hydro_sample_bench] Exported {p_main} ({info['triangles']} tris)")
    return info


def build_room_06_hydroponics_dome_shell(mats):
    """
    Builds Room 06 — Hydroponics & Bio-Air Scrubber Dome Architectural Shell (8.0m W x 9.0m D x 3.6m H):
    - 5 Repeating 45° Chamfered Octagonal Dome Ribs (Z = -4.2, -2.1, 0.0, +2.1, +4.2)
    - Overhead Brushed-Steel Irrigation & Misting Conduit Pipes + Alternating UV-Violet (#7B5CFF) & Cyan (#00E5FF) Coves
    - North & Overhead Slanted Panoramic Solarium Viewports (Z = -4.45m, Y = 0.85m to 3.15m)
      glazed with alphaMode: "BLEND" translucent glass (alpha ~ 0.18)
    """
    sm = []
    slate_deck = [
        make_beveled_box((8.00, 0.06, 9.00), center=(0.0, 0.03, 0.0), bevel=0.015),
        make_beveled_box((0.12, 3.48, 8.88), center=(-3.94, 1.80, 0.0), bevel=0.02),
        make_beveled_box((0.12, 3.48, 8.88), center=(3.94, 1.80, 0.0), bevel=0.02),
        # North wall lower sill & side pillars around the wide 3-bay solarium window (X = -2.80..+2.80, Y = 0.85..3.05m)
        make_beveled_box((7.88, 0.80, 0.12), center=(0.0, 0.46, -4.44), bevel=0.02),
        make_beveled_box((7.88, 0.50, 0.12), center=(0.0, 3.30, -4.44), bevel=0.02),
        make_beveled_box((1.10, 2.24, 0.12), center=(-3.38, 1.95, -4.44), bevel=0.02),
        make_beveled_box((1.10, 2.24, 0.12), center=(3.38, 1.95, -4.44), bevel=0.02),
    ]
    add_part(sm, "Room06_CarbonSlateDeckAndWalls", merge_geometries(slate_deck), mats["carbon_slate"])

    gunmetal_ribs = [
        make_beveled_box((8.00, 0.06, 9.00), center=(0.0, 3.57, 0.0), bevel=0.015),
    ]
    for z_rib in [-4.2, -2.1, 0.0, 2.1, 4.2]:
        gunmetal_ribs.extend([
            make_beveled_box((0.20, 3.48, 0.22), center=(-3.82, 1.80, z_rib), bevel=0.03),
            make_beveled_box((0.20, 3.48, 0.22), center=(3.82, 1.80, z_rib), bevel=0.03),
            make_beveled_box((7.84, 0.20, 0.22), center=(0.0, 3.46, z_rib), bevel=0.03),
            transform_geom(make_beveled_box((0.78, 0.18, 0.22), bevel=0.02), translate=(-3.48, 3.18, z_rib), rot_xyz_deg=(0.0, 0.0, 45.0)),
            transform_geom(make_beveled_box((0.78, 0.18, 0.22), bevel=0.02), translate=(3.48, 3.18, z_rib), rot_xyz_deg=(0.0, 0.0, -45.0)),
        ])
    add_part(sm, "Room06_OctagonalDomeRibs", merge_geometries(gunmetal_ribs), mats["gunmetal"])

    # Overhead Brushed-Steel Irrigation Pipes & North Solarium Window Mullions
    solarium_bezel = make_portal_oct_ring(5.68, 2.24, center_y=1.95, z_pos=-4.38, tube_r=0.036, chamfer=0.28)
    steel_parts = [
        solarium_bezel,
        make_beveled_box((0.08, 2.20, 0.16), center=(-0.95, 1.95, -4.40), bevel=0.015),
        make_beveled_box((0.08, 2.20, 0.16), center=(0.95, 1.95, -4.40), bevel=0.015),
        make_cylinder(0.032, 0.032, 8.4, center=(-2.10, 3.28, 0.0), segments=10, axis="z"),
        make_cylinder(0.032, 0.032, 8.4, center=(2.10, 3.28, 0.0), segments=10, axis="z"),
    ]
    add_part(sm, "Room06_IrrigationPipesAndSolariumMullions", merge_geometries(steel_parts), mats["steel_machined"])

    uv_coves = [
        make_beveled_box((0.05, 0.03, 8.4), center=(-2.85, 3.36, 0.0), bevel=0.005),
        make_beveled_box((0.05, 0.03, 8.4), center=(2.85, 3.36, 0.0), bevel=0.005),
    ]
    add_part(sm, "Room06_UVVioletCeilingCoves", merge_geometries(uv_coves), mats["led_uv"])

    cyan_coves = [
        make_beveled_box((0.05, 0.03, 8.4), center=(-1.45, 3.42, 0.0), bevel=0.005),
        make_beveled_box((0.05, 0.03, 8.4), center=(1.45, 3.42, 0.0), bevel=0.005),
        make_beveled_box((5.40, 0.024, 0.04), center=(0.0, 0.87, -4.36), bevel=0.004),
    ]
    add_part(sm, "Room06_CyanSolariumAndCoveLED", merge_geometries(cyan_coves), mats["led_cyan"])

    solarium_glass = make_quad_panel((-2.80, 0.86, -4.40), (2.80, 0.86, -4.40), (2.80, 3.04, -4.40), (-2.80, 3.04, -4.40))
    add_part(sm, "Room06_NorthSolariumTranslucentGlass", solarium_glass, mats["glass_hydro"])

    p_main = os.path.join(ROOMS_DIR, "room_06_shell.glb")
    info = center_and_export_glb(p_main, sm, root_name="Room06_HydroponicsBayShell")
    for dst in [
        os.path.join(ROOMS_DIR, "room_06_hydro_shell.glb"),
        os.path.join(ROOMS_DIR, "room_06_hydroponics_bay_shell.glb"),
        "/workspace/game-project/assets/glb/room_06_hydro_shell.glb",
        "/workspace/game-project/assets/glb/room_06_shell.glb",
    ]:
        shutil.copyfile(p_main, dst)
    print(f"[room_06_shell] Exported {p_main} and aliases ({info['triangles']} tris)")
    return info


def build_all_hydro_round1():
    mats = get_hydro_materials()
    builders = [
        build_01_octagonal_aeroponic_biotower,
        build_02_dual_zone_split_aeroponic_bioscrubber,
        build_03_twin_helix_carousel,
        build_04_hex_terraced_terrarium,
        build_05_centrifugal_drum_revitalizer,
    ]
    results = []
    for fn in builders:
        info = fn(mats)
        fname = os.path.basename(info["filepath"])
        dims = info["dimensions"]
        print(
            f"[hydro_r1] Built {fname:22s} | {dims[0]:.2f}m W x {dims[2]:.2f}m D x {dims[1]:.2f}m H | "
            f"verts={info['vertices']:4d} | tris={info['triangles']:4d} | min_y={info['min'][1]:.5f}"
        )
        results.append(info)
    with open(os.path.join(OUT_GLB_DIR, "hydro_r1_manifest.json"), "w") as f:
        json.dump(results, f, indent=2)

    build_hydro_sample_bench(mats)
    build_room_06_hydroponics_dome_shell(mats)
    return results


if __name__ == "__main__":
    build_all_hydro_round1()
