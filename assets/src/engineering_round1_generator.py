#!/usr/bin/env python3
"""
Builds all 5 Round-1 Hard Sci-Fi Room 09 Hero Asset (Fusion/Spin-Drive Plasma Relay &
Cryo-Coolant Containment Manifold) .glb models:
  /workspace/game-project/assets/glb/engineering_round1/reactor_core_r1_01.glb .. reactor_core_r1_05.glb
Plus exports Winner #02 to /workspace/game-project/assets/glb/winners/,
the Auxiliary Cryo-Coolant Bus Manifold (engineering_coolant_manifold.glb),
and the Room 09 Architectural Shell (room_09_shell.glb & aliases).

Follows /workspace/game-project/design/engineering_round1/reactor_core_r1_spec.md ("Aegis-7 Standard"):
- Bottom-center (0.0, 0.0, 0.0) floor pivot (min_y == 0.0000, centered X and Z), front facing +Z
- Polygon budget: 3,500 - 5,800 triangles per candidate
- Mandatory 4-Part 3D Plasma Containment & Cryo-Coolant Kit in every candidate:
  1. 45° Chamfered Octagonal Containment Vessel & Heavy Cryo-Coolant Manifolds (Y = 0.0m-2.65m)
  2. Translucent Radiation-Shielded Containment Window (glass_reactor_shield_translucent.png, alphaMode: "BLEND", alpha ~ 0.20)
     + 3D Magnetic-Pinch Plasma Core Spindle & Superconducting Toroidal Pinch Coils
  3. Hot-Swappable D-He3 Moderator Rod Bay (behind translucent hatch) & Signal-Orange Manual SCRAM Blowdown Lever + Handwheel
  4. Chief Engineer Plasma & Spin-Drive OLED Telemetry Console (oled_reactor_plasma_telemetry.png)
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

TEX_ENG_DIR = "/workspace/game-project/assets/textures/engineering_round1"
OUT_GLB_DIR = "/workspace/game-project/assets/glb/engineering_round1"
WINNERS_DIR = "/workspace/game-project/assets/glb/winners"
ROOMS_DIR = "/workspace/game-project/assets/glb/rooms"
os.makedirs(OUT_GLB_DIR, exist_ok=True)
os.makedirs(WINNERS_DIR, exist_ok=True)
os.makedirs(ROOMS_DIR, exist_ok=True)


def tex_eng(fname: str) -> str:
    return os.path.join(TEX_ENG_DIR, fname)


def get_engineering_materials():
    return {
        "gunmetal": PBRMaterialDef(
            name="Mat_Titanium_GunmetalHull",
            base_color=hex_rgba("#1A1E24"),
            metallic=0.78,
            roughness=0.34,
            texture_path=tex_eng("titanium_gunmetal_hull.png"),
        ),
        "aero_white": PBRMaterialDef(
            name="Mat_Composite_AerospaceWhite",
            base_color=hex_rgba("#D8DEE6"),
            metallic=0.08,
            roughness=0.28,
            texture_path=tex_eng("composite_aerospace_white.png"),
        ),
        "carbon_slate": PBRMaterialDef(
            name="Mat_Carbon_SlateFrame",
            base_color=hex_rgba("#282E38"),
            metallic=0.58,
            roughness=0.40,
            texture_path=tex_eng("carbon_slate_frame.png"),
        ),
        "steel_machined": PBRMaterialDef(
            name="Mat_Steel_MachinedGantry",
            base_color=hex_rgba("#88929E"),
            metallic=0.90,
            roughness=0.20,
            texture_path=tex_eng("steel_machined_gantry.png"),
        ),
        "accent_orange": PBRMaterialDef(
            name="Mat_Accent_SignalOrange",
            base_color=hex_rgba("#D95B26"),
            metallic=0.06,
            roughness=0.48,
            texture_path=tex_eng("accent_signal_orange.png"),
        ),
        "oled_plasma": PBRMaterialDef(
            name="Mat_OLED_ReactorPlasmaTelemetry",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.10,
            roughness=0.14,
            emissive=(0.35, 0.90, 1.0),
            texture_path=tex_eng("oled_reactor_plasma_telemetry.png"),
        ),
        "glass_shield": PBRMaterialDef(
            name="Mat_Glass_ReactorShield_Translucent",
            base_color=(0.55, 0.90, 1.0, 0.20),
            metallic=0.10,
            roughness=0.08,
            emissive=(0.0, 0.16, 0.24),
            texture_path=tex_eng("glass_reactor_shield_translucent.png"),
            double_sided=True,
            alpha_mode="BLEND",
        ),
        "led_cyan": PBRMaterialDef(
            name="Mat_Emissive_CyanPlasmaLED",
            base_color=hex_rgba("#00E5FF"),
            metallic=0.0,
            roughness=0.12,
            emissive=(0.0, 0.92, 1.0),
            texture_path=tex_eng("led_cyan_strip.png"),
        ),
        "led_amber": PBRMaterialDef(
            name="Mat_Emissive_AmberPulseLED",
            base_color=hex_rgba("#FF9500"),
            metallic=0.0,
            roughness=0.15,
            emissive=(1.0, 0.58, 0.0),
            texture_path=tex_eng("led_amber_strip.png"),
        ),
        "led_uv": PBRMaterialDef(
            name="Mat_Emissive_UVFieldLED",
            base_color=hex_rgba("#7B5CFF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.55, 0.38, 1.0),
            texture_path=tex_eng("led_uv_violet.png"),
        ),
    }


# ==============================================================================
# SHARED 3D MAGNETIC-PINCH PLASMA CORE, TOROIDAL COILS & MODERATOR ROD HELPERS
# ==============================================================================
def make_plasma_pinch_column_and_toroids(
    cx: float = 0.0,
    cz: float = 0.0,
    y_bot: float = 0.32,
    y_top: float = 2.34,
    num_coils: int = 5,
    coil_r: float = 0.36,
):
    """
    Builds the 3D Magnetic-Pinch Plasma Core & Superconducting Toroidal Pinch Coils:
    - Central glowing cyan (#00E5FF) plasma spindle + high-intensity amber (#FF9500) pulse injector rings
    - 4 to 6 stacked machined-steel toroidal magnetic confinement rings with UV-violet (#7B5CFF) field injectors
    - Upper & lower swept cryo-coolant bus pipes (18.2 K liquid-helium) with aerospace-white insulated jacket collars
    Returns: (steel_coils_pipes_geom, white_insul_geom, cyan_plasma_geom, amber_pulse_geom, uv_field_geom, orange_valves_geom)
    """
    steel_parts = []
    white_parts = []
    cyan_parts = []
    amber_parts = []
    uv_parts = []
    orange_parts = []

    h_col = y_top - y_bot
    ymid = 0.5 * (y_bot + y_top)

    # 1. Central 3D Magnetic-Pinch Plasma Spindle (Cyan core + sculpted pinch waist + Amber injector collars)
    cyan_parts.extend([
        make_cylinder(0.088, 0.088, h_col - 0.16, center=(cx, ymid, cz), segments=16, axis="y"),
        make_sculpted_cushion((0.25, 0.42, 0.25), center=(cx, ymid, cz), res=(5, 4, 5), roundness=0.52, belly_puff=0.08, crease_freq=0),
    ])
    for ay in [y_bot + 0.24, ymid - 0.34, ymid + 0.34, y_top - 0.24]:
        amber_parts.append(make_cylinder(0.125, 0.125, 0.045, center=(cx, ay, cz), segments=14, axis="y"))

    # Upper & lower machined-steel magnetic injector nozzles & white cryo-insulation jackets
    for end_y, s_dir in [(y_bot + 0.06, 1.0), (y_top - 0.06, -1.0)]:
        steel_parts.append(make_cylinder(0.24, 0.30, 0.12, center=(cx, end_y, cz), segments=16, axis="y"))
        white_parts.append(make_cylinder(0.28, 0.28, 0.08, center=(cx, end_y + s_dir * 0.08, cz), segments=14, axis="y"))

    # 2. Stacked 3D Superconducting Toroidal Pinch Coils (lathed/octagonal ring tubes + UV-violet field injectors)
    ys = np.linspace(y_bot + 0.28, y_top - 0.28, num_coils)
    for cy_coil in ys:
        # Closed octagonal-chamfered toroidal coil ring in XZ plane
        pts_coil = []
        n_seg = 12
        for k in range(n_seg + 1):
            ang = (2.0 * math.pi * k) / n_seg
            pts_coil.append((cx + math.cos(ang) * coil_r, cy_coil, cz + math.sin(ang) * coil_r))
        steel_parts.append(make_swept_tube(pts_coil, radius=0.038, radial_segments=8))
        # UV-violet superconducting field-trim ring & front/side clamp struts
        uv_parts.append(make_cylinder(coil_r * 0.78, coil_r * 0.78, 0.024, center=(cx, cy_coil, cz), segments=14, axis="y"))
        for strut_x in [-coil_r - 0.04, coil_r + 0.04]:
            steel_parts.append(make_beveled_box((0.06, 0.06, 0.14), center=(cx + strut_x, cy_coil, cz - 0.06), bevel=0.01))

    # 3. Upper & Lower Swept 18.2 K Cryo-Coolant Bus Pipes feeding the containment column
    for s_x in [-1.0, 1.0]:
        px = cx + s_x * (coil_r + 0.16)
        up_pipe = sample_filleted_polyline(
            [(px, y_top - 0.12, cz - 0.05), (px, y_top + 0.18, cz + 0.14), (cx + s_x * 0.18, y_top + 0.18, cz - 0.28)],
            fillet_radius=0.08,
            corner_subdivs=4,
        )
        dn_pipe = sample_filleted_polyline(
            [(px, y_bot + 0.12, cz - 0.05), (px, y_bot - 0.12, cz + 0.14), (cx + s_x * 0.18, y_bot - 0.12, cz - 0.28)],
            fillet_radius=0.08,
            corner_subdivs=4,
        )
        steel_parts.extend([
            make_swept_tube(up_pipe, radius=0.032, radial_segments=8),
            make_swept_tube(dn_pipe, radius=0.032, radial_segments=8),
        ])
        white_parts.extend([
            make_cylinder(0.046, 0.046, 0.14, center=(px, y_top - 0.02, cz - 0.02), segments=10, axis="y"),
            make_cylinder(0.046, 0.046, 0.14, center=(px, y_bot + 0.02, cz - 0.02), segments=10, axis="y"),
        ])
        orange_parts.append(make_cylinder(0.048, 0.048, 0.036, center=(px, ymid, cz + 0.12), segments=10, axis="z"))

    return (
        merge_geometries(steel_parts),
        merge_geometries(white_parts),
        merge_geometries(cyan_parts),
        merge_geometries(amber_parts),
        merge_geometries(uv_parts),
        merge_geometries(orange_parts),
    )


def make_moderator_rod_bay_and_telemetry_kit(
    bay_cx: float,
    bay_cz: float = 0.0,
    rod_y: float = 1.92,
    console_y: float = 1.18,
):
    """
    Builds Part 3 & Part 4 in the Chief Engineer Control Bay:
    - Upper Recessed D-He3 Moderator Rod Bay holding 4 vertical 3D cylindrical Deuterium/Helium-3 fuel rods
      (composite_aerospace_white.png with glowing UV-violet & cyan tips and signal-orange locking collars)
      behind a translucent glass_reactor_shield_translucent.png hatch
    - Center Chief Engineer Plasma & Spin-Drive OLED Telemetry Console (oled_reactor_plasma_telemetry.png)
      + 3D machined-steel rotary field-trim vernier dials + Guarded Signal-Orange Manual SCRAM Blowdown Lever
    - Lower Twin Insulated Aerospace-White 18.2 K Liquid-Helium Dewar Flasks + Sculpted Signal-Orange 4-Spoke Handwheel
    Returns: (white_rods_dewars_geom, steel_verniers_pipes_geom, orange_scram_wheel_geom,
              oled_screen_geom, uv_led_geom, cyan_led_geom, glass_hatch_geom)
    """
    white_parts = [
        # Rear liner plate of D-He3 moderator rod bay
        make_beveled_box((0.64, 0.80, 0.03), center=(bay_cx, rod_y, bay_cz - 0.18), bevel=0.008),
        # Lower twin insulated aerospace-white 18.2 K liquid-helium Dewar flasks (Y = 0.18..0.82m)
        make_cylinder(0.115, 0.115, 0.56, center=(bay_cx - 0.16, 0.48, bay_cz + 0.02), segments=14, axis="y"),
        make_cylinder(0.115, 0.115, 0.56, center=(bay_cx + 0.16, 0.48, bay_cz + 0.02), segments=14, axis="y"),
    ]
    steel_parts = [
        make_beveled_box((0.62, 0.04, 0.28), center=(bay_cx, rod_y - 0.36, bay_cz + 0.02), bevel=0.008),
        make_beveled_box((0.62, 0.04, 0.28), center=(bay_cx, rod_y + 0.36, bay_cz + 0.02), bevel=0.008),
        # 3D machined-steel rotary magnetic-trim vernier dials below OLED console
        make_cylinder(0.032, 0.032, 0.035, center=(bay_cx - 0.18, console_y - 0.20, bay_cz + 0.28), segments=10, axis="z"),
        make_cylinder(0.032, 0.032, 0.035, center=(bay_cx - 0.06, console_y - 0.20, bay_cz + 0.28), segments=10, axis="z"),
    ]
    orange_parts = [
        # Guarded signal-orange manual SCRAM blowdown pull-lever
        make_beveled_box((0.14, 0.042, 0.055), center=(bay_cx + 0.16, console_y - 0.20, bay_cz + 0.30), bevel=0.008),
        make_cylinder(0.014, 0.014, 0.10, center=(bay_cx + 0.12, console_y - 0.20, bay_cz + 0.26), segments=8, axis="z"),
        make_cylinder(0.014, 0.014, 0.10, center=(bay_cx + 0.20, console_y - 0.20, bay_cz + 0.26), segments=8, axis="z"),
    ]
    uv_parts = []
    cyan_parts = []

    # 4 vertical cylindrical D-He3 moderator fuel rods inside the upper bay
    for r_idx, rx_off in enumerate([-0.21, -0.07, 0.07, 0.21]):
        rx = bay_cx + rx_off
        white_parts.append(make_cylinder(0.042, 0.042, 0.54, center=(rx, rod_y, bay_cz + 0.02), segments=10, axis="y"))
        orange_parts.append(make_cylinder(0.050, 0.050, 0.045, center=(rx, rod_y - 0.24, bay_cz + 0.02), segments=10, axis="y"))
        uv_parts.append(make_cylinder(0.046, 0.046, 0.055, center=(rx, rod_y + 0.18, bay_cz + 0.02), segments=10, axis="y"))
        cyan_parts.append(make_cylinder(0.046, 0.046, 0.045, center=(rx, rod_y - 0.02, bay_cz + 0.02), segments=10, axis="y"))

    # Sculpted signal-orange 4-spoke cryo-isolation handwheel in front of the lower Dewars
    wh_or, wh_st = make_rotary_override_handwheel(cx=bay_cx, cy=0.52, cz=bay_cz + 0.26, radius=0.125)
    orange_parts.append(wh_or)
    steel_parts.append(wh_st)

    oled_screen = make_quad_panel(
        (bay_cx - 0.26, console_y - 0.10, bay_cz + 0.28),
        (bay_cx + 0.26, console_y - 0.10, bay_cz + 0.28),
        (bay_cx + 0.26, console_y + 0.26, bay_cz + 0.28),
        (bay_cx - 0.26, console_y + 0.26, bay_cz + 0.28),
    )
    glass_hatch = make_quad_panel(
        (bay_cx - 0.30, rod_y - 0.38, bay_cz + 0.28),
        (bay_cx + 0.30, rod_y - 0.38, bay_cz + 0.28),
        (bay_cx + 0.30, rod_y + 0.38, bay_cz + 0.28),
        (bay_cx - 0.30, rod_y + 0.38, bay_cz + 0.28),
    )

    return (
        merge_geometries(white_parts),
        merge_geometries(steel_parts),
        merge_geometries(orange_parts),
        oled_screen,
        merge_geometries(uv_parts),
        merge_geometries(cyan_parts),
        glass_hatch,
    )


# ==============================================================================
# CANDIDATE 01: AEGIS-7 OCTAGONAL PLASMA PINCH COLUMN & TOROIDAL COIL STACK (`reactor_core_r1_01.glb`)
# Dimensions: 2.50m W x 1.50m D x 2.65m H
# ==============================================================================
def build_01_octagonal_plasma_pinch_column(mats):
    sm = []
    hull = [
        make_beveled_box((2.50, 0.18, 1.50), center=(0.0, 0.09, 0.0), bevel=0.035),
        make_beveled_box((2.50, 0.22, 1.50), center=(0.0, 2.54, 0.0), bevel=0.035),
        make_beveled_box((0.52, 2.30, 1.42), center=(-0.98, 1.32, 0.0), bevel=0.04),
        make_beveled_box((0.52, 2.30, 1.42), center=(0.98, 1.32, 0.0), bevel=0.04),
        make_beveled_box((1.56, 2.30, 0.14), center=(-0.12, 1.32, -0.66), bevel=0.025),
    ]
    add_part(sm, "Reactor01_OctagonalGunmetalVessel", merge_geometries(hull), mats["gunmetal"])

    st_p, wh_p, cy_p, am_p, uv_p, or_p = make_plasma_pinch_column_and_toroids(
        cx=-0.16, cz=-0.04, y_bot=0.28, y_top=2.38, num_coils=5, coil_r=0.38
    )
    wh_m, st_m, or_m, oled_m, uv_m, cy_m, gl_m = make_moderator_rod_bay_and_telemetry_kit(
        bay_cx=0.88, bay_cz=0.40, rod_y=1.90, console_y=1.18
    )

    front_bezel = make_portal_oct_ring(1.36, 2.22, center_y=1.32, z_pos=0.68, tube_r=0.038, chamfer=0.24)
    front_bezel[0][:, 0] -= 0.16
    add_part(sm, "Reactor01_ToroidalCoilsAndCryoPipes", merge_geometries([st_p, st_m, front_bezel]), mats["steel_machined"])
    add_part(sm, "Reactor01_WhiteModeratorRodsAndDewars", merge_geometries([wh_p, wh_m]), mats["aero_white"])
    add_part(sm, "Reactor01_SignalOrangeSCRAMAndWheel", merge_geometries([or_p, or_m]), mats["accent_orange"])

    add_part(sm, "Reactor01_OLEDPlasmaTelemetryConsole", oled_m, mats["oled_plasma"])
    add_part(sm, "Reactor01_CyanPlasmaSpindleCore", merge_geometries([cy_p, cy_m]), mats["led_cyan"])
    add_part(sm, "Reactor01_AmberInjectorRings", am_p, mats["led_amber"])
    add_part(sm, "Reactor01_UVFieldCoilsAndRodTips", merge_geometries([uv_p, uv_m]), mats["led_uv"])

    main_window = make_quad_panel((-0.78, 0.24, 0.68), (0.46, 0.24, 0.68), (0.46, 2.40, 0.68), (-0.78, 2.40, 0.68))
    add_part(sm, "Reactor01_TranslucentRadiationShields", merge_geometries([main_window, gl_m]), mats["glass_shield"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "reactor_core_r1_01.glb"), sm, root_name="ReactorCoreR1_01_OctagonalPinchColumn")


# ==============================================================================
# CANDIDATE 02: DUAL-ZONE SPLIT PLASMA CONTAINMENT COLUMN & CRYO-COOLANT CONTROL BAY (`reactor_core_r1_02.glb`)
# Dimensions: 2.60m W x 1.50m D x 2.65m H (Signature 65/35 Aegis-7 Split-Bay Sibling!)
# ==============================================================================
def build_02_dual_zone_split_plasma_cryo_bay(mats):
    sm = []
    # 1. Asymmetric 65% / 35% Split-Bay Hull (Left Plasma Column: X=-1.30..+0.39, Right Cryo/Moderator Bay: X=+0.39..+1.30)
    hull = [
        make_beveled_box((2.60, 0.18, 1.50), center=(0.0, 0.09, 0.0), bevel=0.035),
        make_beveled_box((2.60, 0.22, 1.50), center=(0.0, 2.54, 0.0), bevel=0.035),
        make_beveled_box((0.20, 2.30, 1.44), center=(-1.20, 1.32, 0.0), bevel=0.035),
        make_beveled_box((0.16, 2.30, 1.44), center=(1.22, 1.32, 0.0), bevel=0.035),
        # Center structural partition at X = +0.39
        make_beveled_box((0.12, 2.30, 1.42), center=(0.39, 1.32, 0.0), bevel=0.025),
        # Left Plasma Chamber octagonal rear radiation wall + Right Control Bay shelves
        make_beveled_box((1.56, 2.30, 0.14), center=(-0.42, 1.32, -0.66), bevel=0.025),
        make_beveled_box((0.82, 2.30, 0.12), center=(0.82, 1.32, -0.66), bevel=0.02),
        make_beveled_box((0.78, 0.05, 1.34), center=(0.82, 0.88, 0.0), bevel=0.012),
        make_beveled_box((0.78, 0.05, 1.34), center=(0.82, 1.48, 0.0), bevel=0.012),
    ]
    add_part(sm, "Reactor02_SplitBayGunmetalVessel", merge_geometries(hull), mats["gunmetal"])

    # 2. Left Bay 3D Plasma Pinch Column & 5 Toroidal Coils + Right Bay Moderator Rods, Dewars & Telemetry
    st_p, wh_p, cy_p, am_p, uv_p, or_p = make_plasma_pinch_column_and_toroids(
        cx=-0.42, cz=-0.02, y_bot=0.28, y_top=2.38, num_coils=5, coil_r=0.40
    )
    wh_m, st_m, or_m, oled_m, uv_m, cy_m, gl_m = make_moderator_rod_bay_and_telemetry_kit(
        bay_cx=0.82, bay_cz=0.42, rod_y=1.92, console_y=1.18
    )

    front_bezel = make_portal_oct_ring(1.48, 2.24, center_y=1.32, z_pos=0.70, tube_r=0.038, chamfer=0.24)
    front_bezel[0][:, 0] -= 0.42
    add_part(sm, "Reactor02_ToroidalCoilsCryoPipesAndBezel", merge_geometries([st_p, st_m, front_bezel]), mats["steel_machined"])
    add_part(sm, "Reactor02_WhiteModeratorRodsAndDewars", merge_geometries([wh_p, wh_m]), mats["aero_white"])
    add_part(sm, "Reactor02_SignalOrangeSCRAMAndCryoWheel", merge_geometries([or_p, or_m]), mats["accent_orange"])

    add_part(sm, "Reactor02_RightBayOLEDTelemetryConsole", oled_m, mats["oled_plasma"])
    add_part(sm, "Reactor02_CyanPlasmaSpindleCore", merge_geometries([cy_p, cy_m]), mats["led_cyan"])
    add_part(
        sm,
        "Reactor02_AmberPulseRingsAndDeckStrip",
        merge_geometries([
            am_p,
            make_beveled_box((1.38, 0.024, 0.05), center=(-0.42, 0.16, 0.70), bevel=0.005),
        ]),
        mats["led_amber"],
    )
    add_part(sm, "Reactor02_UVFieldCoilsAndModeratorTips", merge_geometries([uv_p, uv_m]), mats["led_uv"])

    left_shield = make_quad_panel((-1.08, 0.24, 0.70), (0.24, 0.24, 0.70), (0.24, 2.40, 0.70), (-1.08, 2.40, 0.70))
    add_part(sm, "Reactor02_TranslucentRadiationShields", merge_geometries([left_shield, gl_m]), mats["glass_shield"])

    out_p = os.path.join(OUT_GLB_DIR, "reactor_core_r1_02.glb")
    info = center_and_export_glb(out_p, sm, root_name="ReactorCoreR1_02_DualZoneSplitPlasmaCryo")

    # Copy Winner #02 to all canonical winner aliases
    for w_alias in [
        "reactor_core_winner_01_split_plasma_cryo.glb",
        "reactor_core_winner_01_dual_zone_plasma.glb",
        "reactor_core_winner_01_plasma_relay.glb",
        "reactor_core_winner_01.glb",
    ]:
        shutil.copyfile(out_p, os.path.join(WINNERS_DIR, w_alias))
    return info


# ==============================================================================
# CANDIDATE 03: SPHERICAL TOKAMAK MAGNETIC CAGE & TWIN CRYO-DEWAR GANTRY (`reactor_core_r1_03.glb`)
# Dimensions: 2.55m W x 1.52m D x 2.65m H
# ==============================================================================
def build_03_spherical_tokamak_cryo_gantry(mats):
    sm = []
    hull = [
        make_beveled_box((2.55, 0.18, 1.52), center=(0.0, 0.09, 0.0), bevel=0.035),
        make_beveled_box((2.55, 0.22, 1.52), center=(0.0, 2.54, 0.0), bevel=0.035),
        make_beveled_box((0.46, 2.30, 1.44), center=(-1.02, 1.32, 0.0), bevel=0.04),
        make_beveled_box((0.46, 2.30, 1.44), center=(1.02, 1.32, 0.0), bevel=0.04),
        make_beveled_box((1.62, 2.30, 0.14), center=(-0.14, 1.32, -0.68), bevel=0.025),
    ]
    add_part(sm, "Reactor03_TokamakCarbonHull", merge_geometries(hull), mats["carbon_slate"])

    st_p, wh_p, cy_p, am_p, uv_p, or_p = make_plasma_pinch_column_and_toroids(
        cx=-0.16, cz=-0.02, y_bot=0.30, y_top=2.36, num_coils=5, coil_r=0.40
    )
    wh_m, st_m, or_m, oled_m, uv_m, cy_m, gl_m = make_moderator_rod_bay_and_telemetry_kit(
        bay_cx=0.88, bay_cz=0.42, rod_y=1.90, console_y=1.18
    )

    # Intersecting meridian tokamak field ribs around center core
    meridian_ring = make_portal_oct_ring(1.12, 1.48, center_y=1.32, z_pos=0.18, tube_r=0.032, chamfer=0.38)
    meridian_ring[0][:, 0] -= 0.16
    add_part(sm, "Reactor03_TokamakCageAndCoils", merge_geometries([st_p, st_m, meridian_ring]), mats["steel_machined"])
    add_part(
        sm,
        "Reactor03_WhiteCryoDewarsAndRods",
        merge_geometries([
            wh_p,
            wh_m,
            make_cylinder(0.16, 0.16, 1.42, center=(-0.86, 1.12, 0.24), segments=14, axis="y"),
        ]),
        mats["aero_white"],
    )
    add_part(sm, "Reactor03_SignalOrangeValvesAndSCRAM", merge_geometries([or_p, or_m]), mats["accent_orange"])

    add_part(sm, "Reactor03_OLEDTelemetryTerminal", oled_m, mats["oled_plasma"])
    add_part(sm, "Reactor03_CyanTokamakPlasmaCore", merge_geometries([cy_p, cy_m]), mats["led_cyan"])
    add_part(sm, "Reactor03_AmberInjectorRings", am_p, mats["led_amber"])
    add_part(sm, "Reactor03_UVFieldRings", merge_geometries([uv_p, uv_m]), mats["led_uv"])

    tok_window = make_quad_panel((-0.78, 0.26, 0.68), (0.46, 0.26, 0.68), (0.46, 2.38, 0.68), (-0.78, 2.38, 0.68))
    add_part(sm, "Reactor03_CurvedTranslucentShields", merge_geometries([tok_window, gl_m]), mats["glass_shield"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "reactor_core_r1_03.glb"), sm, root_name="ReactorCoreR1_03_SphericalTokamakGantry")


# ==============================================================================
# CANDIDATE 04: TWIN-CORE SPIN-DRIVE CAPACITOR BANK & PLASMA CONDUIT ARCH (`reactor_core_r1_04.glb`)
# Dimensions: 2.58m W x 1.48m D x 2.65m H
# ==============================================================================
def build_04_twin_core_spindrive_conduit_arch(mats):
    sm = []
    hull = [
        make_beveled_box((2.58, 0.18, 1.48), center=(0.0, 0.09, 0.0), bevel=0.035),
        make_beveled_box((2.58, 0.24, 1.48), center=(0.0, 2.53, 0.0), bevel=0.035),
        make_beveled_box((0.44, 2.28, 1.40), center=(-1.04, 1.32, 0.0), bevel=0.035),
        make_beveled_box((0.44, 2.28, 1.40), center=(1.04, 1.32, 0.0), bevel=0.035),
        make_beveled_box((1.68, 2.28, 0.14), center=(-0.14, 1.32, -0.66), bevel=0.025),
    ]
    add_part(sm, "Reactor04_TwinCoreGunmetalFrame", merge_geometries(hull), mats["gunmetal"])

    st_p, wh_p, cy_p, am_p, uv_p, or_p = make_plasma_pinch_column_and_toroids(
        cx=-0.38, cz=-0.02, y_bot=0.28, y_top=2.36, num_coils=4, coil_r=0.32
    )
    wh_m, st_m, or_m, oled_m, uv_m, cy_m, gl_m = make_moderator_rod_bay_and_telemetry_kit(
        bay_cx=0.84, bay_cz=0.40, rod_y=1.90, console_y=1.18
    )

    # Secondary twin plasma relay column at X = +0.18
    cy_twin = make_cylinder(0.068, 0.068, 1.88, center=(0.18, 1.32, -0.02), segments=14, axis="y")
    arch_pipe = sample_filleted_polyline([(-0.38, 2.28, 0.08), (-0.10, 2.42, 0.18), (0.18, 2.28, 0.08)], 0.08, 4)

    add_part(
        sm,
        "Reactor04_TwinCoilsAndBusArch",
        merge_geometries([st_p, st_m, make_swept_tube(arch_pipe, 0.042, 8)]),
        mats["steel_machined"],
    )
    add_part(sm, "Reactor04_WhiteModeratorRodsAndDewars", merge_geometries([wh_p, wh_m]), mats["aero_white"])
    add_part(sm, "Reactor04_SignalOrangeSCRAMPillar", merge_geometries([or_p, or_m]), mats["accent_orange"])

    add_part(sm, "Reactor04_OLEDTelemetryPillar", oled_m, mats["oled_plasma"])
    add_part(sm, "Reactor04_TwinCyanPlasmaColumns", merge_geometries([cy_p, cy_m, cy_twin]), mats["led_cyan"])
    add_part(sm, "Reactor04_AmberCapacitorRings", am_p, mats["led_amber"])
    add_part(sm, "Reactor04_UVFieldCoils", merge_geometries([uv_p, uv_m]), mats["led_uv"])

    twin_win = make_quad_panel((-0.82, 0.24, 0.68), (0.44, 0.24, 0.68), (0.44, 2.38, 0.68), (-0.82, 2.38, 0.68))
    add_part(sm, "Reactor04_TwinTranslucentShields", merge_geometries([twin_win, gl_m]), mats["glass_shield"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "reactor_core_r1_04.glb"), sm, root_name="ReactorCoreR1_04_TwinCoreSpinDrive")


# ==============================================================================
# CANDIDATE 05: HEAVY AXIAL SPIN-TORQUE GENERATOR & SUB-COOLER MANIFOLD (`reactor_core_r1_05.glb`)
# Dimensions: 2.62m W x 1.52m D x 2.68m H
# ==============================================================================
def build_05_axial_spintorque_subcooler_manifold(mats):
    sm = []
    hull = [
        make_beveled_box((2.62, 0.18, 1.52), center=(0.0, 0.09, 0.0), bevel=0.035),
        make_beveled_box((2.62, 0.22, 1.52), center=(0.0, 2.57, 0.0), bevel=0.035),
        make_beveled_box((0.48, 2.34, 1.44), center=(-1.05, 1.34, 0.0), bevel=0.04),
        make_beveled_box((0.48, 2.34, 1.44), center=(1.05, 1.34, 0.0), bevel=0.04),
        make_beveled_box((1.64, 2.34, 0.14), center=(-0.16, 1.34, -0.68), bevel=0.025),
    ]
    add_part(sm, "Reactor05_SpinTorqueGunmetalHousing", merge_geometries(hull), mats["gunmetal"])

    st_p, wh_p, cy_p, am_p, uv_p, or_p = make_plasma_pinch_column_and_toroids(
        cx=-0.20, cz=-0.02, y_bot=0.32, y_top=2.40, num_coils=5, coil_r=0.38
    )
    wh_m, st_m, or_m, oled_m, uv_m, cy_m, gl_m = make_moderator_rod_bay_and_telemetry_kit(
        bay_cx=0.86, bay_cz=0.42, rod_y=1.92, console_y=1.18
    )

    stator_ring = make_portal_oct_ring(1.42, 2.26, center_y=1.34, z_pos=0.68, tube_r=0.040, chamfer=0.26)
    stator_ring[0][:, 0] -= 0.20
    add_part(sm, "Reactor05_StatorRingsAndSubCoolerPipes", merge_geometries([st_p, st_m, stator_ring]), mats["steel_machined"])
    add_part(sm, "Reactor05_WhiteSubCoolerManifoldAndRods", merge_geometries([wh_p, wh_m]), mats["aero_white"])
    add_part(sm, "Reactor05_SignalOrangeTorqueValves", merge_geometries([or_p, or_m]), mats["accent_orange"])

    add_part(sm, "Reactor05_OLEDTorqueConsole", oled_m, mats["oled_plasma"])
    add_part(sm, "Reactor05_CyanStatorPlasmaCore", merge_geometries([cy_p, cy_m]), mats["led_cyan"])
    add_part(sm, "Reactor05_AmberRotorPulseRings", am_p, mats["led_amber"])
    add_part(sm, "Reactor05_UVFieldRings", merge_geometries([uv_p, uv_m]), mats["led_uv"])

    drum_win = make_quad_panel((-0.84, 0.24, 0.70), (0.44, 0.24, 0.70), (0.44, 2.42, 0.70), (-0.84, 2.42, 0.70))
    add_part(sm, "Reactor05_TranslucentRotorDrumShields", merge_geometries([drum_win, gl_m]), mats["glass_shield"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "reactor_core_r1_05.glb"), sm, root_name="ReactorCoreR1_05_AxialSpinTorqueManifold")


# ==============================================================================
# ROOM 09 AUXILIARY PROP (`engineering_coolant_manifold.glb`) & SHELL (`room_09_shell.glb`)
# ==============================================================================
def build_engineering_coolant_manifold(mats):
    """
    Builds Auxiliary Cryo-Coolant Bus Manifold (engineering_coolant_manifold.glb):
    2.10m W x 0.85m D x 2.20m H companion manifold bank with 4 insulated aerospace-white 18.2 K liquid-helium
    cylinders behind a bevel-framed alphaMode: "BLEND" translucent radiation-shielded inspection window,
    brushed-steel cross-feed pipes, signal-orange isolation handwheels, and OLED cryo gauge (2,800-4,800 tris).
    """
    sm = []
    frame = [
        make_beveled_box((2.10, 0.16, 0.85), center=(0.0, 0.08, 0.0), bevel=0.03),
        make_beveled_box((2.10, 0.18, 0.85), center=(0.0, 2.11, 0.0), bevel=0.03),
        make_beveled_box((0.20, 1.88, 0.80), center=(-0.95, 1.10, 0.0), bevel=0.03),
        make_beveled_box((0.20, 1.88, 0.80), center=(0.95, 1.10, 0.0), bevel=0.03),
        make_beveled_box((1.74, 1.88, 0.10), center=(0.0, 1.10, -0.36), bevel=0.02),
    ]
    add_part(sm, "CoolantManifold_GunmetalFrame", merge_geometries(frame), mats["gunmetal"])

    white_tanks = []
    steel_pipes = []
    orange_wheels = []
    cyan_leds = []
    uv_leds = []

    # 4 vertical insulated aerospace-white 18.2 K liquid-helium cylinders + domes + cross-feed pipes + handwheels
    for idx, tx in enumerate([-0.60, -0.20, 0.20, 0.60]):
        white_tanks.append(make_cylinder(0.145, 0.145, 1.32, center=(tx, 1.04, -0.02), segments=16, axis="y"))
        d_prof = [(0.0, 0.0), (0.145, 0.01), (0.135, 0.06), (0.09, 0.11), (0.0, 0.13)]
        white_tanks.append(make_lathe_dome(d_prof, center=(tx, 1.70, -0.02), segments=14, subdivide_profile=1))

        # Swept cross-feed cryo pipe from tank dome to upper header bus
        p_pts = sample_filleted_polyline([(tx, 1.80, -0.02), (tx, 1.96, 0.18), (tx, 1.96, -0.18)], 0.06, 4)
        steel_pipes.append(make_swept_tube(p_pts, radius=0.028, radial_segments=8))
        steel_pipes.append(make_cylinder(0.155, 0.155, 0.04, center=(tx, 0.65, -0.02), segments=14, axis="y"))
        steel_pipes.append(make_cylinder(0.155, 0.155, 0.04, center=(tx, 1.42, -0.02), segments=14, axis="y"))

        cyan_leds.append(make_cylinder(0.152, 0.152, 0.035, center=(tx, 1.18, -0.02), segments=14, axis="y"))
        uv_leds.append(make_cylinder(0.152, 0.152, 0.035, center=(tx, 0.90, -0.02), segments=14, axis="y"))

        if idx in (0, 3):
            wh_or, wh_st = make_rotary_override_handwheel(cx=tx, cy=0.52, cz=0.22, radius=0.11)
            orange_wheels.append(wh_or)
            steel_pipes.append(wh_st)
        else:
            orange_wheels.append(make_cylinder(0.055, 0.055, 0.045, center=(tx, 1.78, 0.12), segments=10, axis="z"))

    # Horizontal header manifold tube & octagonal viewport bezel
    hdr_ring = make_portal_oct_ring(1.68, 1.82, center_y=1.10, z_pos=0.38, tube_r=0.032, chamfer=0.20)
    steel_pipes.append(hdr_ring)
    steel_pipes.append(make_cylinder(0.042, 0.042, 1.64, center=(0.0, 1.94, 0.10), segments=12, axis="x"))

    add_part(sm, "CoolantManifold_WhiteHeliumCylinders", merge_geometries(white_tanks), mats["aero_white"])
    add_part(sm, "CoolantManifold_BrushedSteelCrossFeedPipes", merge_geometries(steel_pipes), mats["steel_machined"])
    add_part(sm, "CoolantManifold_SignalOrangeHandwheels", merge_geometries(orange_wheels), mats["accent_orange"])
    add_part(sm, "CoolantManifold_CyanCryoLevelRings", merge_geometries(cyan_leds), mats["led_cyan"])
    add_part(sm, "CoolantManifold_UVSupercoolRings", merge_geometries(uv_leds), mats["led_uv"])

    oled_g = make_quad_panel((-0.22, 1.35, 0.40), (0.22, 1.35, 0.40), (0.22, 1.68, 0.40), (-0.22, 1.68, 0.40))
    add_part(sm, "CoolantManifold_OLEDTelemetryGauge", oled_g, mats["oled_plasma"])

    shield_win = make_quad_panel((-0.80, 0.22, 0.39), (0.80, 0.22, 0.39), (0.80, 1.98, 0.39), (-0.80, 1.98, 0.39))
    add_part(sm, "CoolantManifold_TranslucentInspectionShield", shield_win, mats["glass_shield"])

    p_main = os.path.join(WINNERS_DIR, "engineering_coolant_manifold.glb")
    info = center_and_export_glb(p_main, sm, root_name="EngineeringCoolantManifold")
    for dst in [
        os.path.join(OUT_GLB_DIR, "engineering_coolant_manifold.glb"),
        os.path.join(ROOMS_DIR, "engineering_coolant_manifold.glb"),
        "/workspace/game-project/assets/glb/engineering_coolant_manifold.glb",
    ]:
        shutil.copyfile(p_main, dst)
    print(f"[coolant_manifold] Exported {p_main} ({info['triangles']} tris)")
    return info


def build_room_09_engineering_core_shell(mats):
    """
    Builds Room 09 — Engineering & Life-Support Reactor Core Architectural Shell (8.5m W x 9.5m D x 3.8m H):
    - 5 Heavy 45° Chamfered Octagonal Titanium Ribs (Z = -4.4, -2.2, 0.0, +2.2, +4.4)
    - Overhead swept cryo-coolant bus pipes & recessed Orbital Cyan (#00E5FF) & High-Voltage Amber (#FF9500) bus-bar strips
    - Grated Diagnostic Walkways & Sub-Floor Plasma Conduit Trench (X = -1.2m..+1.2m)
    - North Outer-Hull Armored Radiator Viewport (Z = -4.70m, X = -2.8m to +2.8m, Y = 1.05m to 3.05m)
      glazed with glass_reactor_shield_translucent.png (alphaMode: "BLEND", alpha ~ 0.18)
    """
    sm = []
    slate_deck = [
        make_beveled_box((8.50, 0.06, 9.50), center=(0.0, 0.03, 0.0), bevel=0.015),
        make_beveled_box((0.12, 3.68, 9.40), center=(-4.19, 1.90, 0.0), bevel=0.02),
        make_beveled_box((0.12, 3.68, 9.40), center=(4.19, 1.90, 0.0), bevel=0.02),
        # North wall framing around 3-bay Armored Radiator Viewport (X = -2.8..+2.8, Y = 1.05..3.05)
        make_beveled_box((8.40, 1.00, 0.14), center=(0.0, 0.55, -4.68), bevel=0.02),
        make_beveled_box((8.40, 0.72, 0.14), center=(0.0, 3.41, -4.68), bevel=0.02),
        make_beveled_box((1.35, 2.02, 0.14), center=(-3.52, 2.05, -4.68), bevel=0.02),
        make_beveled_box((1.35, 2.02, 0.14), center=(3.52, 2.05, -4.68), bevel=0.02),
        make_beveled_box((0.22, 2.02, 0.14), center=(-0.95, 2.05, -4.68), bevel=0.02),
        make_beveled_box((0.22, 2.02, 0.14), center=(0.95, 2.05, -4.68), bevel=0.02),
    ]
    add_part(sm, "Room09_CarbonSlateDeckAndBulkheads", merge_geometries(slate_deck), mats["carbon_slate"])

    gunmetal_ribs = [
        make_beveled_box((8.50, 0.06, 9.50), center=(0.0, 3.77, 0.0), bevel=0.015),
    ]
    for z_rib in [-4.4, -2.2, 0.0, 2.2, 4.4]:
        gunmetal_ribs.extend([
            make_beveled_box((0.24, 3.68, 0.24), center=(-4.06, 1.90, z_rib), bevel=0.03),
            make_beveled_box((0.24, 3.68, 0.24), center=(4.06, 1.90, z_rib), bevel=0.03),
            make_beveled_box((8.32, 0.22, 0.24), center=(0.0, 3.65, z_rib), bevel=0.03),
            transform_geom(make_beveled_box((0.82, 0.20, 0.24), bevel=0.025), translate=(-3.70, 3.36, z_rib), rot_xyz_deg=(0.0, 0.0, 45.0)),
            transform_geom(make_beveled_box((0.82, 0.20, 0.24), bevel=0.025), translate=(3.70, 3.36, z_rib), rot_xyz_deg=(0.0, 0.0, -45.0)),
        ])
    add_part(sm, "Room09_OctagonalTitaniumRibs", merge_geometries(gunmetal_ribs), mats["gunmetal"])

    # Overhead cryo-coolant bus pipes, North viewport octagonal bezel & central grated walkway trench
    vp_bezel = make_portal_oct_ring(5.68, 2.06, center_y=2.05, z_pos=-4.62, tube_r=0.038, chamfer=0.28)
    steel_parts = [
        vp_bezel,
        make_cylinder(0.055, 0.055, 8.80, center=(-2.65, 3.46, 0.0), segments=12, axis="z"),
        make_cylinder(0.055, 0.055, 8.80, center=(2.65, 3.46, 0.0), segments=12, axis="z"),
        make_beveled_box((2.40, 0.018, 8.60), center=(0.0, 0.068, 0.0), bevel=0.004),
    ]
    add_part(sm, "Room09_CryoBusPipesAndTrenchGrates", merge_geometries(steel_parts), mats["steel_machined"])

    cyan_conduits = [
        make_beveled_box((0.12, 0.016, 8.40), center=(-0.55, 0.062, 0.0), bevel=0.004),
        make_beveled_box((0.12, 0.016, 8.40), center=(0.55, 0.062, 0.0), bevel=0.004),
        make_beveled_box((0.06, 0.032, 8.80), center=(-3.15, 3.52, 0.0), bevel=0.005),
        make_beveled_box((0.06, 0.032, 8.80), center=(3.15, 3.52, 0.0), bevel=0.005),
    ]
    add_part(sm, "Room09_CyanSubFloorPlasmaConduits", merge_geometries(cyan_conduits), mats["led_cyan"])

    amber_bars = [
        make_beveled_box((0.08, 0.016, 8.40), center=(0.0, 0.062, 0.0), bevel=0.004),
        make_beveled_box((0.05, 0.028, 8.60), center=(-1.25, 0.066, 0.0), bevel=0.004),
        make_beveled_box((0.05, 0.028, 8.60), center=(1.25, 0.066, 0.0), bevel=0.004),
    ]
    add_part(sm, "Room09_AmberHighVoltageBusBars", merge_geometries(amber_bars), mats["led_amber"])

    north_vp = make_quad_panel((-2.82, 1.04, -4.64), (2.82, 1.04, -4.64), (2.82, 3.06, -4.64), (-2.82, 3.06, -4.64))
    add_part(sm, "Room09_NorthDeepSpaceTranslucentViewport", north_vp, mats["glass_shield"])

    p_main = os.path.join(ROOMS_DIR, "room_09_shell.glb")
    info = center_and_export_glb(p_main, sm, root_name="Room09_EngineeringCoreShell")
    for dst in [
        os.path.join(ROOMS_DIR, "room_09_engineering_shell.glb"),
        os.path.join(ROOMS_DIR, "room_09_engineering_core_shell.glb"),
        "/workspace/game-project/assets/glb/room_09_engineering_shell.glb",
        "/workspace/game-project/assets/glb/room_09_shell.glb",
    ]:
        shutil.copyfile(p_main, dst)
    print(f"[room_09_shell] Exported {p_main} and aliases ({info['triangles']} tris)")
    return info


def build_all_engineering_round1():
    mats = get_engineering_materials()
    builders = [
        build_01_octagonal_plasma_pinch_column,
        build_02_dual_zone_split_plasma_cryo_bay,
        build_03_spherical_tokamak_cryo_gantry,
        build_04_twin_core_spindrive_conduit_arch,
        build_05_axial_spintorque_subcooler_manifold,
    ]
    results = []
    for fn in builders:
        info = fn(mats)
        fname = os.path.basename(info["filepath"])
        dims = info["dimensions"]
        print(
            f"[eng_r1] Built {fname:24s} | {dims[0]:.2f}m W x {dims[2]:.2f}m D x {dims[1]:.2f}m H | "
            f"verts={info['vertices']:4d} | tris={info['triangles']:4d} | min_y={info['min'][1]:.5f}"
        )
        results.append(info)
    with open(os.path.join(OUT_GLB_DIR, "engineering_r1_manifest.json"), "w") as f:
        json.dump(results, f, indent=2)

    build_engineering_coolant_manifold(mats)
    build_room_09_engineering_core_shell(mats)
    return results


if __name__ == "__main__":
    build_all_engineering_round1()
