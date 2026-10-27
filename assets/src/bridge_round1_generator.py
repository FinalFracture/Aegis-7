#!/usr/bin/env python3
"""
Builds all 5 Round-1 Hard Sci-Fi Room 07 Hero Asset (Central Holographic O'Neill Cylinder
Wireframe Projection Table & Tiered Spin-Gravity Command Console) .glb models:
  /workspace/game-project/assets/glb/bridge_round1/bridge_console_r1_01.glb .. bridge_console_r1_05.glb
Plus exports Winner #02 to /workspace/game-project/assets/glb/winners/ and builds the
Room 07 Architectural Shell (room_07_shell.glb & aliases).

Follows /workspace/game-project/design/bridge_round1/bridge_console_r1_spec.md ("Aegis-7 Standard"):
- Bottom-center (0.0, 0.0, 0.0) floor pivot (min_y == 0.0000, centered X and Z), front facing +Z
- Polygon budget: 3,800 - 5,800 triangles per candidate
- Mandatory 4-Part 3D Holographic Bridge & Telemetry Kit in every candidate:
  1. 45° Chamfered Octagonal Projection Table & Recessed Emitter Well (Y = 0.0m-0.92m)
  2. Floating 3D Translucent O'Neill Cylinder Wireframe & Intersecting Gimbal Rings
     (glass_bridge_holo_translucent.png, alphaMode: "BLEND", alpha ~ 0.20)
  3. Tiered Flight-Director Spin-Gravity Telemetry Console (oled_bridge_spin_telemetry.png)
     + Tactile Vernier Controls + Translucent HUD Visor + Signal-Orange Spin-Lock Master Switch
  4. Contoured Commander Flight Chairs (fabric_orbital_navy_pad.png & fabric_charcoal_flightpad.png)
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
from corridor_door_round1_generator import make_portal_oct_ring

TEX_BRIDGE_DIR = "/workspace/game-project/assets/textures/bridge_round1"
OUT_GLB_DIR = "/workspace/game-project/assets/glb/bridge_round1"
WINNERS_DIR = "/workspace/game-project/assets/glb/winners"
ROOMS_DIR = "/workspace/game-project/assets/glb/rooms"
os.makedirs(OUT_GLB_DIR, exist_ok=True)
os.makedirs(WINNERS_DIR, exist_ok=True)
os.makedirs(ROOMS_DIR, exist_ok=True)


def tex_bridge(fname: str) -> str:
    return os.path.join(TEX_BRIDGE_DIR, fname)


def get_bridge_materials():
    return {
        "gunmetal": PBRMaterialDef(
            name="Mat_Titanium_GunmetalHull",
            base_color=hex_rgba("#1A1E24"),
            metallic=0.78,
            roughness=0.34,
            texture_path=tex_bridge("titanium_gunmetal_hull.png"),
        ),
        "aero_white": PBRMaterialDef(
            name="Mat_Composite_AerospaceWhite",
            base_color=hex_rgba("#D8DEE6"),
            metallic=0.08,
            roughness=0.28,
            texture_path=tex_bridge("composite_aerospace_white.png"),
        ),
        "carbon_slate": PBRMaterialDef(
            name="Mat_Carbon_SlateFrame",
            base_color=hex_rgba("#282E38"),
            metallic=0.58,
            roughness=0.40,
            texture_path=tex_bridge("carbon_slate_frame.png"),
        ),
        "steel_machined": PBRMaterialDef(
            name="Mat_Steel_MachinedGantry",
            base_color=hex_rgba("#88929E"),
            metallic=0.90,
            roughness=0.20,
            texture_path=tex_bridge("steel_machined_gantry.png"),
        ),
        "fabric_charcoal": PBRMaterialDef(
            name="Mat_Fabric_CharcoalFlightpad",
            base_color=hex_rgba("#242932"),
            metallic=0.0,
            roughness=0.78,
            texture_path=tex_bridge("fabric_charcoal_flightpad.png"),
        ),
        "fabric_navy": PBRMaterialDef(
            name="Mat_Fabric_OrbitalNavyPad",
            base_color=hex_rgba("#1D2C3C"),
            metallic=0.0,
            roughness=0.76,
            texture_path=tex_bridge("fabric_orbital_navy_pad.png"),
        ),
        "accent_orange": PBRMaterialDef(
            name="Mat_Accent_SignalOrange",
            base_color=hex_rgba("#D95B26"),
            metallic=0.06,
            roughness=0.48,
            texture_path=tex_bridge("accent_signal_orange.png"),
        ),
        "oled_telemetry": PBRMaterialDef(
            name="Mat_OLED_BridgeSpinTelemetry",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.10,
            roughness=0.14,
            emissive=(0.35, 0.90, 1.0),
            texture_path=tex_bridge("oled_bridge_spin_telemetry.png"),
        ),
        "glass_holo": PBRMaterialDef(
            name="Mat_Glass_BridgeHolo_Translucent",
            base_color=(0.45, 0.90, 1.0, 0.20),
            metallic=0.10,
            roughness=0.08,
            emissive=(0.0, 0.20, 0.30),
            texture_path=tex_bridge("glass_bridge_holo_translucent.png"),
            double_sided=True,
            alpha_mode="BLEND",
        ),
        "led_cyan": PBRMaterialDef(
            name="Mat_Emissive_CyanLED",
            base_color=hex_rgba("#00E5FF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.0, 0.92, 1.0),
            texture_path=tex_bridge("led_cyan_strip.png"),
        ),
        "led_amber": PBRMaterialDef(
            name="Mat_Emissive_AmberLED",
            base_color=hex_rgba("#FF9500"),
            metallic=0.0,
            roughness=0.15,
            emissive=(1.0, 0.58, 0.0),
            texture_path=tex_bridge("led_amber_strip.png"),
        ),
        "led_uv": PBRMaterialDef(
            name="Mat_Emissive_UVVioletLED",
            base_color=hex_rgba("#7B5CFF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.55, 0.38, 1.0),
            texture_path=tex_bridge("led_uv_violet.png"),
        ),
    }


def make_closed_circle_ring(radius: float, tube_r: float = 0.014, n_pts: int = 24, radial_segs: int = 6):
    pts = []
    for i in range(n_pts + 1):
        ang = 2.0 * math.pi * (i / float(n_pts))
        pts.append([radius * math.cos(ang), radius * math.sin(ang), 0.0])
    return make_swept_tube(np.array(pts, dtype=np.float32), radius=tube_r, radial_segments=radial_segs)


def make_floating_oneill_cylinder_hologram(cx: float = 0.0, cy: float = 1.34, cz: float = 0.0, scale: float = 1.0):
    """
    Builds Part 1 & Part 2:
    - Recessed Optical Emitter Lens Well at Y ~ 0.88m
    - Floating 3D Translucent O'Neill Cylinder Habitat Miniature (glass_bridge_holo_translucent.png)
    - 3D Structural Ring Ribs, Axial Solar Core Rod, and Two Intersecting Orbital Gimbal Rings
      (led_cyan_strip.png & led_amber_strip.png)
    Returns: (holo_glass_geom, cyan_wireframe_geom, amber_gimbal_geom, steel_emitter_geom, white_bezel_geom)
    """
    r_cyl = 0.19 * scale
    l_cyl = 0.58 * scale

    # 1. Translucent 3D O'Neill Cylinder Shell & Endcap Cones (alphaMode: "BLEND")
    holo_glass = [
        transform_geom(
            make_cylinder(r_cyl, r_cyl, l_cyl, center=(0.0, 0.0, 0.0), segments=18, axis="x"),
            translate=(cx, cy, cz),
            rot_xyz_deg=(0.0, -16.0, 12.0),
        ),
        transform_geom(
            make_cylinder(r_cyl * 0.45, r_cyl, 0.10 * scale, center=(-l_cyl * 0.55, 0.0, 0.0), segments=16, axis="x"),
            translate=(cx, cy, cz),
            rot_xyz_deg=(0.0, -16.0, 12.0),
        ),
        transform_geom(
            make_cylinder(r_cyl, r_cyl * 0.45, 0.10 * scale, center=(l_cyl * 0.55, 0.0, 0.0), segments=16, axis="x"),
            translate=(cx, cy, cz),
            rot_xyz_deg=(0.0, -16.0, 12.0),
        ),
    ]

    # 2. Cyan Wireframe Habitat Ring Ribs, Axial Solar Core Rod & Primary Gimbal Ring
    cyan_parts = [
        # Axial solar core rod running through the O'Neill Cylinder axis
        transform_geom(
            make_cylinder(0.016 * scale, 0.016 * scale, l_cyl * 1.38, center=(0.0, 0.0, 0.0), segments=10, axis="x"),
            translate=(cx, cy, cz),
            rot_xyz_deg=(0.0, -16.0, 12.0),
        ),
        # Outer tilted cyan orbital gimbal ring
        transform_geom(
            make_closed_circle_ring(radius=0.38 * scale, tube_r=0.012 * scale, n_pts=24, radial_segs=6),
            translate=(cx, cy, cz),
            rot_xyz_deg=(62.0, -18.0, 15.0),
        ),
        # Lower emitter well cyan lens ring
        make_cylinder(0.28 * scale, 0.30 * scale, 0.024, center=(cx, 0.90, cz), segments=18, axis="y"),
    ]
    for rx_off in [-0.22 * scale, -0.07 * scale, 0.07 * scale, 0.22 * scale]:
        rib = transform_geom(
            make_closed_circle_ring(radius=r_cyl * 1.03, tube_r=0.009 * scale, n_pts=18, radial_segs=6),
            translate=(rx_off, 0.0, 0.0),
            rot_xyz_deg=(0.0, 90.0, 0.0),
        )
        cyan_parts.append(transform_geom(rib, translate=(cx, cy, cz), rot_xyz_deg=(0.0, -16.0, 12.0)))

    # 3. Secondary Intersecting Amber Orbital Gimbal Ring & Emitter Ring
    amber_parts = [
        transform_geom(
            make_closed_circle_ring(radius=0.34 * scale, tube_r=0.011 * scale, n_pts=22, radial_segs=6),
            translate=(cx, cy, cz),
            rot_xyz_deg=(-48.0, 24.0, -20.0),
        ),
        make_cylinder(0.18 * scale, 0.20 * scale, 0.026, center=(cx, 0.91, cz), segments=16, axis="y"),
    ]

    # 4. Recessed Emitter Well & Brushed-Steel Leaning Rail
    steel_parts = [
        make_cylinder(0.36 * scale, 0.40 * scale, 0.04, center=(cx, 0.89, cz), segments=18, axis="y"),
    ]
    white_parts = [
        make_cylinder(0.44 * scale, 0.46 * scale, 0.03, center=(cx, 0.87, cz), segments=18, axis="y"),
    ]

    return (
        merge_geometries(holo_glass),
        merge_geometries(cyan_parts),
        merge_geometries(amber_parts),
        merge_geometries(steel_parts),
        merge_geometries(white_parts),
    )


def make_commander_flight_chair(cx: float, cz: float, rot_y_deg: float = 180.0):
    """
    Builds Part 4: Contoured Commander Flight Chair (Y ~ 0.48m seat height)
    with sculpted orbital-navy and charcoal cushions, aerospace-white shell,
    and cantilevered machined-steel pedestal.
    Returns: (navy_cushion_geom, charcoal_bolster_geom, white_shell_geom, steel_pedestal_geom)
    """
    navy_local = merge_geometries([
        make_sculpted_cushion((0.46, 0.09, 0.44), center=(0.0, 0.48, 0.0), res=(5, 3, 5), roundness=0.36, belly_puff=0.04, tuft_grid=(2, 2), tuft_depth=0.012, crease_freq=0),
        transform_geom(
            make_sculpted_cushion((0.44, 0.52, 0.09), res=(5, 5, 3), roundness=0.35, belly_puff=0.04, tuft_grid=(2, 2), tuft_depth=0.012, crease_freq=0),
            translate=(0.0, 0.78, -0.18),
            rot_xyz_deg=(-10.0, 0.0, 0.0),
        ),
    ])
    charcoal_local = merge_geometries([
        make_sculpted_cushion((0.28, 0.14, 0.08), center=(0.0, 1.09, -0.22), res=(4, 3, 3), roundness=0.40, belly_puff=0.04, crease_freq=0),
        make_beveled_box((0.07, 0.04, 0.30), center=(-0.25, 0.64, -0.02), bevel=0.012),
        make_beveled_box((0.07, 0.04, 0.30), center=(0.25, 0.64, -0.02), bevel=0.012),
    ])
    white_local = merge_geometries([
        make_beveled_box((0.50, 0.06, 0.46), center=(0.0, 0.42, -0.01), bevel=0.018),
        transform_geom(
            make_beveled_box((0.46, 0.56, 0.05), bevel=0.016),
            translate=(0.0, 0.78, -0.23),
            rot_xyz_deg=(-10.0, 0.0, 0.0),
        ),
    ])
    steel_local = merge_geometries([
        make_cylinder(0.22, 0.26, 0.04, center=(0.0, 0.02, 0.0), segments=14, axis="y"),
        make_cylinder(0.055, 0.065, 0.38, center=(0.0, 0.22, -0.02), segments=12, axis="y"),
        make_beveled_box((0.54, 0.03, 0.05), center=(0.0, 0.56, -0.10), bevel=0.008),
    ])

    return (
        transform_geom(navy_local, translate=(cx, 0.0, cz), rot_xyz_deg=(0.0, rot_y_deg, 0.0)),
        transform_geom(charcoal_local, translate=(cx, 0.0, cz), rot_xyz_deg=(0.0, rot_y_deg, 0.0)),
        transform_geom(white_local, translate=(cx, 0.0, cz), rot_xyz_deg=(0.0, rot_y_deg, 0.0)),
        transform_geom(steel_local, translate=(cx, 0.0, cz), rot_xyz_deg=(0.0, rot_y_deg, 0.0)),
    )


def make_flight_director_tower_controls(tx: float, tz: float = -0.10, deck_y: float = 0.92):
    """
    Builds Part 3:
    - Curved 3-panel widescreen OLED Spin-Gravity Telemetry Array (oled_bridge_spin_telemetry.png)
    - Angled alphaMode: "BLEND" Translucent Tactical HUD Combiner Visor (glass_bridge_holo_translucent.png)
    - 3D Machined-Steel Dual-Throttle Spin-Brake Levers, Rotary Attitude Verniers & Guarded Signal-Orange Master Switch
    - Lower Optical Core Bay with 6 Glowing Cyan/Violet Navigation Data-Cartridges behind Translucent Glass
    Returns: (oled_geom, hud_glass_geom, steel_throttles_geom, orange_switch_geom, cyan_carts_geom, uv_carts_geom)
    """
    oled_panels = [
        make_quad_panel(
            (tx - 0.36, deck_y + 0.34, tz + 0.18),
            (tx + 0.36, deck_y + 0.34, tz + 0.18),
            (tx + 0.36, deck_y + 0.82, tz + 0.10),
            (tx - 0.36, deck_y + 0.82, tz + 0.10),
        ),
        # Lower tilted deck touch screen
        make_quad_panel(
            (tx - 0.32, deck_y + 0.03, tz + 0.44),
            (tx + 0.04, deck_y + 0.03, tz + 0.44),
            (tx + 0.04, deck_y + 0.12, tz + 0.22),
            (tx - 0.32, deck_y + 0.12, tz + 0.22),
        ),
    ]
    hud_glass = [
        # Upper angled translucent holographic HUD combiner visor
        make_quad_panel(
            (tx - 0.38, deck_y + 0.84, tz + 0.12),
            (tx + 0.38, deck_y + 0.84, tz + 0.12),
            (tx + 0.38, deck_y + 1.02, tz + 0.28),
            (tx - 0.38, deck_y + 1.02, tz + 0.28),
        ),
        # Lower optical navigation core bay translucent window
        make_quad_panel(
            (tx - 0.34, 0.18, tz + 0.46),
            (tx + 0.34, 0.18, tz + 0.46),
            (tx + 0.34, deck_y - 0.08, tz + 0.46),
            (tx - 0.34, deck_y - 0.08, tz + 0.46),
        ),
    ]

    # Dual machined-steel throttle levers + rotary verniers + lower gyro-stabilizer cylinders
    steel_parts = [
        make_beveled_box((0.18, 0.04, 0.16), center=(tx + 0.18, deck_y + 0.04, tz + 0.34), bevel=0.008),
        make_cylinder(0.012, 0.012, 0.14, center=(tx + 0.14, deck_y + 0.11, tz + 0.34), segments=8, axis="y"),
        make_cylinder(0.012, 0.012, 0.14, center=(tx + 0.22, deck_y + 0.11, tz + 0.34), segments=8, axis="y"),
        make_cylinder(0.022, 0.022, 0.12, center=(tx + 0.18, deck_y + 0.18, tz + 0.34), segments=10, axis="x"),
        # Two backup gyro-stabilizer cylinders inside the lower optical bay
        make_cylinder(0.065, 0.065, 0.44, center=(tx - 0.20, 0.46, tz + 0.28), segments=12, axis="y"),
        make_cylinder(0.065, 0.065, 0.44, center=(tx + 0.20, 0.46, tz + 0.28), segments=12, axis="y"),
    ]

    # Guarded signal-orange emergency spin-lock master handle
    orange_parts = [
        make_beveled_box((0.10, 0.05, 0.10), center=(tx + 0.26, deck_y + 0.05, tz + 0.18), bevel=0.008),
        make_beveled_box((0.08, 0.08, 0.03), center=(tx + 0.26, deck_y + 0.11, tz + 0.18), bevel=0.005),
    ]

    # 6 vertical glowing cyan & UV-violet navigation data-cartridges inside lower bay
    cyan_carts = [
        make_beveled_box((0.035, 0.36, 0.08), center=(tx - 0.08, 0.48, tz + 0.32), bevel=0.005),
        make_beveled_box((0.035, 0.36, 0.08), center=(tx + 0.0, 0.48, tz + 0.32), bevel=0.005),
        make_beveled_box((0.035, 0.36, 0.08), center=(tx + 0.08, 0.48, tz + 0.32), bevel=0.005),
    ]
    uv_carts = [
        make_beveled_box((0.035, 0.28, 0.08), center=(tx - 0.04, 0.46, tz + 0.30), bevel=0.005),
        make_beveled_box((0.035, 0.28, 0.08), center=(tx + 0.04, 0.46, tz + 0.30), bevel=0.005),
    ]

    return (
        merge_geometries(oled_panels),
        merge_geometries(hud_glass),
        merge_geometries(steel_parts),
        merge_geometries(orange_parts),
        merge_geometries(cyan_carts),
        merge_geometries(uv_carts),
    )


# ==============================================================================
# CANDIDATE 01: AEGIS-7 OCTAGONAL HOLOGRAPHIC CYLINDER TABLE & TWIN HELM (`bridge_console_r1_01.glb`)
# Dimensions: 2.45m W x 1.65m D x 1.90m H
# ==============================================================================
def build_01_octagonal_holo_cylinder_table(mats):
    sm = []
    hull = [
        make_beveled_box((2.45, 0.14, 1.65), center=(0.0, 0.07, 0.0), bevel=0.03),
        make_beveled_box((1.68, 0.74, 1.12), center=(-0.32, 0.48, 0.02), bevel=0.045),
        make_beveled_box((0.86, 1.72, 0.96), center=(0.76, 0.96, -0.16), bevel=0.04),
    ]
    add_part(sm, "Bridge01_OctagonalGunmetalHull", merge_geometries(hull), mats["gunmetal"])

    holo_gl, cy_w, am_g, st_e, wh_b = make_floating_oneill_cylinder_hologram(cx=-0.32, cy=1.34, cz=0.02, scale=1.05)
    oled_t, hud_gl, st_t, or_t, cy_c, uv_c = make_flight_director_tower_controls(tx=0.76, tz=-0.16, deck_y=0.90)
    nv1, ch1, wh1, st1 = make_commander_flight_chair(cx=-0.68, cz=0.58, rot_y_deg=180.0)
    nv2, ch2, wh2, st2 = make_commander_flight_chair(cx=0.06, cz=0.58, rot_y_deg=180.0)

    add_part(sm, "Bridge01_AerospaceWhiteCowlingsAndChairs", merge_geometries([wh_b, wh1, wh2, make_beveled_box((1.74, 0.08, 1.18), center=(-0.32, 0.86, 0.02), bevel=0.02)]), mats["aero_white"])
    add_part(sm, "Bridge01_OrbitalNavyChairCushions", merge_geometries([nv1, nv2]), mats["fabric_navy"])
    add_part(sm, "Bridge01_CharcoalBolstersAndPads", merge_geometries([ch1, ch2]), mats["fabric_charcoal"])
    add_part(sm, "Bridge01_MachinedSteelGantryAndThrottles", merge_geometries([st_e, st_t, st1, st2]), mats["steel_machined"])
    add_part(sm, "Bridge01_SignalOrangeSpinLockSwitches", or_t, mats["accent_orange"])

    # Tabletop OLED touch screens + Tower OLED array
    table_oled = make_quad_panel((-0.78, 0.91, 0.52), (0.14, 0.91, 0.52), (0.14, 0.91, 0.28), (-0.78, 0.91, 0.28))
    add_part(sm, "Bridge01_OLEDSpinTelemetryScreens", merge_geometries([oled_t, table_oled]), mats["oled_telemetry"])
    add_part(sm, "Bridge01_CyanHoloWireframeAndCarts", merge_geometries([cy_w, cy_c]), mats["led_cyan"])
    add_part(sm, "Bridge01_AmberGimbalRingAndBaseLED", merge_geometries([am_g, make_beveled_box((1.60, 0.024, 0.04), center=(-0.32, 0.16, 0.58), bevel=0.004)]), mats["led_amber"])
    add_part(sm, "Bridge01_UVNavigationCartridges", uv_c, mats["led_uv"])
    add_part(sm, "Bridge01_TranslucentHoloCylinderAndHUD", merge_geometries([holo_gl, hud_gl]), mats["glass_holo"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bridge_console_r1_01.glb"), sm, root_name="BridgeConsoleR1_01_OctagonalHoloTable")


# ==============================================================================
# CANDIDATE 02: DUAL-ZONE SPLIT HOLOGRAPHIC CYLINDER TABLE & TIERED FLIGHT-DIRECTOR CONSOLE (`bridge_console_r1_02.glb`)
# Dimensions: 2.55m W x 1.65m D x 1.95m H (Signature 65% / 35% Asymmetric Split-Bay Sibling!)
# ==============================================================================
def build_02_dual_zone_split_holo_flight_director(mats):
    sm = []
    # 1. Signature 65% / 35% Split-Bay Hull:
    # Left Bay (X = -1.275 .. +0.385): Octagonal 45° Chamfered Holographic Projection Table (Y = 0.88m)
    # Right Bay (X = +0.385 .. +1.275): Elevated Tiered Flight-Director Spin-Gravity & Attitude Control Tower (Y = 0.0m..1.95m)
    hull = [
        make_beveled_box((2.55, 0.14, 1.65), center=(0.0, 0.07, 0.0), bevel=0.03),
        make_beveled_box((1.62, 0.74, 1.14), center=(-0.42, 0.48, 0.0), bevel=0.045),
        # Right Flight-Director Tower with open lower optical bay cutout
        make_beveled_box((0.88, 0.92, 0.92), center=(0.82, 1.34, -0.14), bevel=0.035),
        make_beveled_box((0.88, 0.72, 0.14), center=(0.82, 0.50, -0.52), bevel=0.02),
        make_beveled_box((0.12, 0.72, 0.82), center=(0.44, 0.50, -0.12), bevel=0.02),
        make_beveled_box((0.12, 0.72, 0.82), center=(1.20, 0.50, -0.12), bevel=0.02),
    ]
    add_part(sm, "Bridge02_SplitBayGunmetalHull", merge_geometries(hull), mats["gunmetal"])

    holo_gl, cy_w, am_g, st_e, wh_b = make_floating_oneill_cylinder_hologram(cx=-0.42, cy=1.35, cz=-0.02, scale=1.08)
    oled_t, hud_gl, st_t, or_t, cy_c, uv_c = make_flight_director_tower_controls(tx=0.82, tz=-0.12, deck_y=0.90)
    nv1, ch1, wh1, st1 = make_commander_flight_chair(cx=-0.80, cz=0.58, rot_y_deg=180.0)
    nv2, ch2, wh2, st2 = make_commander_flight_chair(cx=-0.04, cz=0.58, rot_y_deg=180.0)

    white_cowlings = [
        wh_b,
        wh1,
        wh2,
        make_beveled_box((1.68, 0.08, 1.20), center=(-0.42, 0.86, 0.0), bevel=0.022),
        make_beveled_box((0.90, 0.08, 0.96), center=(0.82, 0.88, -0.12), bevel=0.02),
    ]
    add_part(sm, "Bridge02_AerospaceWhiteCowlingsAndChairShells", merge_geometries(white_cowlings), mats["aero_white"])
    add_part(sm, "Bridge02_OrbitalNavyCommanderCushions", merge_geometries([nv1, nv2]), mats["fabric_navy"])
    add_part(sm, "Bridge02_CharcoalWristAndChairBolsters", merge_geometries([ch1, ch2, make_beveled_box((1.56, 0.04, 0.08), center=(-0.42, 0.90, 0.56), bevel=0.012)]), mats["fabric_charcoal"])
    add_part(sm, "Bridge02_MachinedSteelGimbalsAndThrottles", merge_geometries([st_e, st_t, st1, st2]), mats["steel_machined"])
    add_part(sm, "Bridge02_SignalOrangeSpinLockMasterSwitch", or_t, mats["accent_orange"])

    table_oled = make_quad_panel((-0.96, 0.91, 0.50), (0.12, 0.91, 0.50), (0.12, 0.91, 0.26), (-0.96, 0.91, 0.26))
    add_part(sm, "Bridge02_OLEDTelemetryArrayAndTouchDeck", merge_geometries([oled_t, table_oled]), mats["oled_telemetry"])
    add_part(sm, "Bridge02_CyanHoloCylinderWireframeAndCarts", merge_geometries([cy_w, cy_c]), mats["led_cyan"])
    add_part(
        sm,
        "Bridge02_AmberGimbalRingAndSafetyStrip",
        merge_geometries([
            am_g,
            make_beveled_box((1.58, 0.024, 0.04), center=(-0.42, 0.16, 0.58), bevel=0.004),
            make_beveled_box((0.82, 0.024, 0.04), center=(0.82, 0.16, 0.34), bevel=0.004),
        ]),
        mats["led_amber"],
    )
    add_part(sm, "Bridge02_UVNavigationCartridges", uv_c, mats["led_uv"])
    add_part(sm, "Bridge02_TranslucentHoloCylinderHUDAndCoreBay", merge_geometries([holo_gl, hud_gl]), mats["glass_holo"])

    out_p = os.path.join(OUT_GLB_DIR, "bridge_console_r1_02.glb")
    info = center_and_export_glb(out_p, sm, root_name="BridgeConsoleR1_02_DualZoneSplitHoloFlightDirector")

    for w_alias in [
        "bridge_console_winner_01_split_holo_flight_director.glb",
        "bridge_console_winner_01_dual_zone_holo_console.glb",
        "bridge_console_winner_01_holo_command_table.glb",
        "bridge_console_winner_01.glb",
    ]:
        shutil.copyfile(out_p, os.path.join(WINNERS_DIR, w_alias))
    return info


# ==============================================================================
# CANDIDATE 03: OVERHEAD GANTRY HOLO-PROJECTOR & CURVED BRIDGE PIT CONSOLE (`bridge_console_r1_03.glb`)
# Dimensions: 2.50m W x 1.68m D x 1.98m H
# ==============================================================================
def build_03_overhead_gantry_holo_projector(mats):
    sm = []
    hull = [
        make_beveled_box((2.50, 0.14, 1.68), center=(0.0, 0.07, 0.0), bevel=0.03),
        make_beveled_box((1.64, 0.74, 1.12), center=(-0.34, 0.48, 0.0), bevel=0.045),
        make_beveled_box((0.84, 1.74, 0.94), center=(0.78, 0.96, -0.14), bevel=0.035),
    ]
    add_part(sm, "Bridge03_GantryGunmetalHull", merge_geometries(hull), mats["gunmetal"])

    holo_gl, cy_w, am_g, st_e, wh_b = make_floating_oneill_cylinder_hologram(cx=-0.34, cy=1.32, cz=0.0, scale=1.04)
    oled_t, hud_gl, st_t, or_t, cy_c, uv_c = make_flight_director_tower_controls(tx=0.78, tz=-0.14, deck_y=0.90)
    nv1, ch1, wh1, st1 = make_commander_flight_chair(cx=-0.72, cz=0.58, rot_y_deg=180.0)
    nv2, ch2, wh2, st2 = make_commander_flight_chair(cx=0.04, cz=0.58, rot_y_deg=180.0)

    # Arched machined-steel overhead projector bridge spanning above the holotable (Y = 1.92m)
    arch_pts = sample_filleted_polyline([(-1.08, 0.88, -0.22), (-1.00, 1.92, -0.12), (0.32, 1.92, -0.12), (0.40, 0.88, -0.22)], 0.16, 5)
    gantry_arch = make_swept_tube(arch_pts, radius=0.034, radial_segments=10)

    add_part(sm, "Bridge03_WhiteCowlingsAndChairs", merge_geometries([wh_b, wh1, wh2, make_beveled_box((1.70, 0.08, 1.18), center=(-0.34, 0.86, 0.0), bevel=0.02)]), mats["aero_white"])
    add_part(sm, "Bridge03_OrbitalNavyCushions", merge_geometries([nv1, nv2]), mats["fabric_navy"])
    add_part(sm, "Bridge03_CharcoalBolsters", merge_geometries([ch1, ch2]), mats["fabric_charcoal"])
    add_part(sm, "Bridge03_MachinedOverheadArchAndThrottles", merge_geometries([st_e, st_t, st1, st2, gantry_arch]), mats["steel_machined"])
    add_part(sm, "Bridge03_SignalOrangeInterlocks", or_t, mats["accent_orange"])

    add_part(sm, "Bridge03_OLEDTelemetryArray", oled_t, mats["oled_telemetry"])
    add_part(sm, "Bridge03_CyanHoloWireframeAndProjector", merge_geometries([cy_w, cy_c, make_cylinder(0.18, 0.22, 0.04, center=(-0.34, 1.88, -0.12), segments=14, axis="y")]), mats["led_cyan"])
    add_part(sm, "Bridge03_AmberGimbalRing", am_g, mats["led_amber"])
    add_part(sm, "Bridge03_UVCartridges", uv_c, mats["led_uv"])
    add_part(sm, "Bridge03_TranslucentHoloCylinderAndHUD", merge_geometries([holo_gl, hud_gl]), mats["glass_holo"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bridge_console_r1_03.glb"), sm, root_name="BridgeConsoleR1_03_OverheadGantryProjector")


# ==============================================================================
# CANDIDATE 04: GIMBALED ORRERY SPIN-SIMULATOR & TACTICAL COMMAND DESK (`bridge_console_r1_04.glb`)
# Dimensions: 2.48m W x 1.62m D x 1.92m H
# ==============================================================================
def build_04_gimbaled_orrery_spin_simulator(mats):
    sm = []
    hull = [
        make_beveled_box((2.48, 0.14, 1.62), center=(0.0, 0.07, 0.0), bevel=0.03),
        make_beveled_box((1.62, 0.74, 1.10), center=(-0.34, 0.48, 0.0), bevel=0.045),
        make_beveled_box((0.84, 1.70, 0.92), center=(0.76, 0.95, -0.12), bevel=0.035),
    ]
    add_part(sm, "Bridge04_OrreryCarbonHull", merge_geometries(hull), mats["carbon_slate"])

    holo_gl, cy_w, am_g, st_e, wh_b = make_floating_oneill_cylinder_hologram(cx=-0.34, cy=1.34, cz=0.0, scale=1.05)
    oled_t, hud_gl, st_t, or_t, cy_c, uv_c = make_flight_director_tower_controls(tx=0.76, tz=-0.12, deck_y=0.90)
    nv1, ch1, wh1, st1 = make_commander_flight_chair(cx=-0.70, cz=0.56, rot_y_deg=180.0)
    nv2, ch2, wh2, st2 = make_commander_flight_chair(cx=0.04, cz=0.56, rot_y_deg=180.0)

    orrery_cradle = transform_geom(
        make_closed_circle_ring(radius=0.46, tube_r=0.022, n_pts=24, radial_segs=8),
        translate=(-0.34, 1.34, 0.0),
        rot_xyz_deg=(12.0, 0.0, 0.0),
    )

    add_part(sm, "Bridge04_WhiteCowlingsAndChairs", merge_geometries([wh_b, wh1, wh2, make_beveled_box((1.68, 0.08, 1.16), center=(-0.34, 0.86, 0.0), bevel=0.02)]), mats["aero_white"])
    add_part(sm, "Bridge04_OrbitalNavyCushions", merge_geometries([nv1, nv2]), mats["fabric_navy"])
    add_part(sm, "Bridge04_CharcoalBolsters", merge_geometries([ch1, ch2]), mats["fabric_charcoal"])
    add_part(sm, "Bridge04_MachinedOrreryCradleAndThrottles", merge_geometries([st_e, st_t, st1, st2, orrery_cradle]), mats["steel_machined"])
    add_part(sm, "Bridge04_SignalOrangeInterlocks", or_t, mats["accent_orange"])

    add_part(sm, "Bridge04_OLEDTelemetryArray", oled_t, mats["oled_telemetry"])
    add_part(sm, "Bridge04_CyanHoloWireframe", merge_geometries([cy_w, cy_c]), mats["led_cyan"])
    add_part(sm, "Bridge04_AmberGimbalRing", am_g, mats["led_amber"])
    add_part(sm, "Bridge04_UVCartridges", uv_c, mats["led_uv"])
    add_part(sm, "Bridge04_TranslucentHoloCylinderAndHUD", merge_geometries([holo_gl, hud_gl]), mats["glass_holo"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bridge_console_r1_04.glb"), sm, root_name="BridgeConsoleR1_04_GimbaledOrrerySimulator")


# ==============================================================================
# CANDIDATE 05: ELEVATED CAPTAIN'S COMMAND PODIUM & DUAL-WING TELEMETRY ARRAY (`bridge_console_r1_05.glb`)
# Dimensions: 2.55m W x 1.70m D x 1.96m H
# ==============================================================================
def build_05_elevated_captain_command_podium(mats):
    sm = []
    hull = [
        make_beveled_box((2.55, 0.16, 1.70), center=(0.0, 0.08, 0.0), bevel=0.03),
        make_beveled_box((1.66, 0.74, 1.12), center=(-0.38, 0.50, -0.02), bevel=0.045),
        make_beveled_box((0.86, 1.72, 0.94), center=(0.80, 0.98, -0.14), bevel=0.035),
    ]
    add_part(sm, "Bridge05_CommandPodiumGunmetalHull", merge_geometries(hull), mats["gunmetal"])

    holo_gl, cy_w, am_g, st_e, wh_b = make_floating_oneill_cylinder_hologram(cx=-0.38, cy=1.36, cz=-0.02, scale=1.06)
    oled_t, hud_gl, st_t, or_t, cy_c, uv_c = make_flight_director_tower_controls(tx=0.80, tz=-0.14, deck_y=0.92)
    nv1, ch1, wh1, st1 = make_commander_flight_chair(cx=-0.76, cz=0.60, rot_y_deg=180.0)
    nv2, ch2, wh2, st2 = make_commander_flight_chair(cx=0.02, cz=0.60, rot_y_deg=180.0)

    add_part(sm, "Bridge05_WhiteCowlingsAndChairs", merge_geometries([wh_b, wh1, wh2, make_beveled_box((1.72, 0.08, 1.18), center=(-0.38, 0.88, -0.02), bevel=0.02)]), mats["aero_white"])
    add_part(sm, "Bridge05_OrbitalNavyCushions", merge_geometries([nv1, nv2]), mats["fabric_navy"])
    add_part(sm, "Bridge05_CharcoalBolsters", merge_geometries([ch1, ch2]), mats["fabric_charcoal"])
    add_part(sm, "Bridge05_MachinedSteelGimbalsAndThrottles", merge_geometries([st_e, st_t, st1, st2]), mats["steel_machined"])
    add_part(sm, "Bridge05_SignalOrangeSwitches", or_t, mats["accent_orange"])

    add_part(sm, "Bridge05_OLEDTelemetryWings", oled_t, mats["oled_telemetry"])
    add_part(sm, "Bridge05_CyanHoloWireframe", merge_geometries([cy_w, cy_c]), mats["led_cyan"])
    add_part(sm, "Bridge05_AmberGimbalRingAndStepLED", merge_geometries([am_g, make_beveled_box((2.40, 0.024, 0.04), center=(0.0, 0.16, 0.82), bevel=0.004)]), mats["led_amber"])
    add_part(sm, "Bridge05_UVCartridges", uv_c, mats["led_uv"])
    add_part(sm, "Bridge05_TranslucentHoloCylinderAndHUD", merge_geometries([holo_gl, hud_gl]), mats["glass_holo"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bridge_console_r1_05.glb"), sm, root_name="BridgeConsoleR1_05_CaptainCommandPodium")


# ==============================================================================
# ROOM 07 ARCHITECTURAL SHELL (`room_07_shell.glb`)
# ==============================================================================
def build_room_07_command_bridge_shell(mats):
    """
    Builds Room 07 — Habitat Command & Spin-Gravity Telemetry Bridge Shell (8.5m W x 9.5m D x 3.6m H):
    - 5 Repeating 45° Chamfered Octagonal Titanium Bridge Ribs (Z = -4.4, -2.2, 0.0, +2.2, +4.4)
    - North Panoramic 5-Pane Cylinder Axis Viewport (Z = -4.70m, X = -3.4..+3.4m, Y = 0.85..3.05m)
      with open cutouts and alphaMode: "BLEND" translucent glass
    - West Outer-Hull Deep-Space Navigation Window (X = -4.20m, Z = -3.2..+1.2m)
    """
    sm = []
    slate_deck = [
        make_beveled_box((8.50, 0.06, 9.50), center=(0.0, 0.03, 0.0), bevel=0.015),
        # East solid bulkhead & West bulkhead around navigation window cutout
        make_beveled_box((0.12, 3.48, 9.40), center=(4.19, 1.80, 0.0), bevel=0.02),
        make_beveled_box((0.12, 0.84, 9.40), center=(-4.19, 0.45, 0.0), bevel=0.02),
        make_beveled_box((0.12, 0.65, 9.40), center=(-4.19, 3.25, 0.0), bevel=0.02),
        make_beveled_box((0.12, 2.15, 3.10), center=(-4.19, 1.90, 2.85), bevel=0.02),
        make_beveled_box((0.12, 2.15, 1.40), center=(-4.19, 1.90, -3.95), bevel=0.02),
        # North bridge viewport lower knee-wall & upper header (open window Y = 0.85..3.05m, X = -3.4..+3.4m)
        make_beveled_box((8.40, 0.82, 0.14), center=(0.0, 0.44, -4.68), bevel=0.02),
        make_beveled_box((8.40, 0.52, 0.14), center=(0.0, 3.30, -4.68), bevel=0.02),
    ]
    add_part(sm, "Room07_CarbonSlateDeckAndBulkheads", merge_geometries(slate_deck), mats["carbon_slate"])

    gunmetal_ribs = [
        make_beveled_box((8.50, 0.06, 9.50), center=(0.0, 3.57, 0.0), bevel=0.015),
    ]
    for z_rib in [-4.4, -2.2, 0.0, 2.2, 4.4]:
        gunmetal_ribs.extend([
            make_beveled_box((0.22, 3.48, 0.24), center=(-4.08, 1.80, z_rib), bevel=0.03),
            make_beveled_box((0.22, 3.48, 0.24), center=(4.08, 1.80, z_rib), bevel=0.03),
            make_beveled_box((8.36, 0.22, 0.24), center=(0.0, 3.44, z_rib), bevel=0.03),
            transform_geom(make_beveled_box((0.80, 0.20, 0.24), bevel=0.02), translate=(-3.72, 3.16, z_rib), rot_xyz_deg=(0.0, 0.0, 45.0)),
            transform_geom(make_beveled_box((0.80, 0.20, 0.24), bevel=0.02), translate=(3.72, 3.16, z_rib), rot_xyz_deg=(0.0, 0.0, -45.0)),
        ])
    # North 5-pane bridge window mullions
    for xm in [-3.40, -1.70, 0.0, 1.70, 3.40]:
        gunmetal_ribs.append(make_beveled_box((0.12, 2.24, 0.16), center=(xm, 1.95, -4.66), bevel=0.02))
    add_part(sm, "Room07_OctagonalTitaniumBridgeRibsAndMullions", merge_geometries(gunmetal_ribs), mats["gunmetal"])

    baffles = [
        make_beveled_box((5.60, 0.06, 1.60), center=(0.0, 3.32, -3.30), bevel=0.015),
        make_beveled_box((5.60, 0.06, 1.60), center=(0.0, 3.32, -1.10), bevel=0.015),
        make_beveled_box((5.60, 0.06, 1.60), center=(0.0, 3.32, 1.10), bevel=0.015),
        make_beveled_box((5.60, 0.06, 1.60), center=(0.0, 3.32, 3.30), bevel=0.015),
    ]
    add_part(sm, "Room07_AerospaceWhiteCeilingBaffles", merge_geometries(baffles), mats["aero_white"])

    cyan_strips = [
        make_beveled_box((0.05, 0.03, 8.80), center=(-2.85, 3.32, 0.0), bevel=0.005),
        make_beveled_box((0.05, 0.03, 8.80), center=(2.85, 3.32, 0.0), bevel=0.005),
    ]
    add_part(sm, "Room07_CyanBridgeCoveStrips", merge_geometries(cyan_strips), mats["led_cyan"])

    amber_strips = [
        make_beveled_box((0.04, 0.014, 8.60), center=(-1.85, 0.066, 0.0), bevel=0.003),
        make_beveled_box((0.04, 0.014, 8.60), center=(1.85, 0.066, 0.0), bevel=0.003),
    ]
    add_part(sm, "Room07_AmberDeckGuideStrips", merge_geometries(amber_strips), mats["led_amber"])

    viewports = [
        # North panoramic 5-pane bridge viewport
        make_quad_panel((-3.40, 0.85, -4.66), (3.40, 0.85, -4.66), (3.40, 3.05, -4.66), (-3.40, 3.05, -4.66)),
        # West outer-hull deep-space navigation window
        make_quad_panel((-4.16, 0.85, -3.20), (-4.16, 0.85, 1.20), (-4.16, 2.95, 1.20), (-4.16, 2.95, -3.20)),
    ]
    add_part(sm, "Room07_TranslucentBridgeViewports", merge_geometries(viewports), mats["glass_holo"])

    p_main = os.path.join(ROOMS_DIR, "room_07_shell.glb")
    info = center_and_export_glb(p_main, sm, root_name="Room07_CommandBridgeShell")
    for dst in [
        os.path.join(ROOMS_DIR, "room_07_bridge_shell.glb"),
        os.path.join(ROOMS_DIR, "room_07_command_bridge_shell.glb"),
        "/workspace/game-project/assets/glb/room_07_bridge_shell.glb",
        "/workspace/game-project/assets/glb/room_07_shell.glb",
    ]:
        shutil.copyfile(p_main, dst)
    print(f"[room_07_shell] Exported {p_main} and aliases ({info['triangles']} tris)")
    return info


def build_all_bridge_round1():
    mats = get_bridge_materials()
    builders = [
        build_01_octagonal_holo_cylinder_table,
        build_02_dual_zone_split_holo_flight_director,
        build_03_overhead_gantry_holo_projector,
        build_04_gimbaled_orrery_spin_simulator,
        build_05_elevated_captain_command_podium,
    ]
    results = []
    for fn in builders:
        info = fn(mats)
        fname = os.path.basename(info["filepath"])
        dims = info["dimensions"]
        print(
            f"[bridge_r1] Built {fname:26s} | {dims[0]:.2f}m W x {dims[2]:.2f}m D x {dims[1]:.2f}m H | "
            f"verts={info['vertices']:4d} | tris={info['triangles']:4d} | min_y={info['min'][1]:.5f}"
        )
        results.append(info)
    with open(os.path.join(OUT_GLB_DIR, "bridge_r1_manifest.json"), "w") as f:
        json.dump(results, f, indent=2)

    build_room_07_command_bridge_shell(mats)
    return results


if __name__ == "__main__":
    build_all_bridge_round1()
