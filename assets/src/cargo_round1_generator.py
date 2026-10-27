#!/usr/bin/env python3
"""
Builds all 5 Round-1 Hard Sci-Fi Room 10 Hero Asset (Modular Hex/Chamfered Cargo Container Rack &
Autonomous Logistics Drone Docking Gantry) .glb models:
  /workspace/game-project/assets/glb/cargo_round1/cargo_gantry_r1_01.glb .. cargo_gantry_r1_05.glb
Plus exports Winner #02 to /workspace/game-project/assets/glb/winners/,
the Auxiliary Center Magnetic Pallet Deck (cargo_mag_pallet_deck.glb),
and the Room 10 Architectural Shell (room_10_shell.glb & aliases).

Follows /workspace/game-project/design/cargo_round1/cargo_gantry_r1_spec.md ("Aegis-7 Standard"):
- Bottom-center (0.0, 0.0, 0.0) floor pivot (min_y == 0.0000, centered X and Z), front facing +Z
- Polygon budget: 3,500 - 5,800 triangles per candidate
- Mandatory 4-Part 3D Orbital Logistics & Drone Kit in every candidate:
  1. Heavy 45° Chamfered Gantry Stanchions, Overhead Hoist Beam & Interlocking ISO Cargo Matrix (Y = 0.0m-2.60m)
  2. Translucent Pressurized Container Windows & Drone Safety Shield (glass_cargo_bay_translucent.png, alphaMode: "BLEND", alpha ~ 0.19)
     revealing 3D stowed supply drums, strapped orbital-navy pallet bundles, and Li-S power cylinders
  3. 3D Autonomous Octo-Thruster Logistics Cargo Drone in its inductive charging cradle with 4 angled thruster pods,
     ventral signal-orange magnetic grappling claws, and glowing cyan LiDAR sensor eye
  4. Centrifuge Mass-Balance & RFID Manifest OLED Terminal (oled_cargo_drone_logistics.png) + coiled umbilical hoses
     and signal-orange tie-down winches/levers
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

TEX_CARGO_DIR = "/workspace/game-project/assets/textures/cargo_round1"
OUT_GLB_DIR = "/workspace/game-project/assets/glb/cargo_round1"
WINNERS_DIR = "/workspace/game-project/assets/glb/winners"
ROOMS_DIR = "/workspace/game-project/assets/glb/rooms"
os.makedirs(OUT_GLB_DIR, exist_ok=True)
os.makedirs(WINNERS_DIR, exist_ok=True)
os.makedirs(ROOMS_DIR, exist_ok=True)


def tex_cargo(fname: str) -> str:
    return os.path.join(TEX_CARGO_DIR, fname)


def get_cargo_materials():
    return {
        "gunmetal": PBRMaterialDef(
            name="Mat_Titanium_GunmetalHull",
            base_color=hex_rgba("#1A1E24"),
            metallic=0.78,
            roughness=0.34,
            texture_path=tex_cargo("titanium_gunmetal_hull.png"),
        ),
        "aero_white": PBRMaterialDef(
            name="Mat_Composite_AerospaceWhite",
            base_color=hex_rgba("#D8DEE6"),
            metallic=0.08,
            roughness=0.28,
            texture_path=tex_cargo("composite_aerospace_white.png"),
        ),
        "carbon_slate": PBRMaterialDef(
            name="Mat_Carbon_SlateFrame",
            base_color=hex_rgba("#282E38"),
            metallic=0.58,
            roughness=0.40,
            texture_path=tex_cargo("carbon_slate_frame.png"),
        ),
        "steel_machined": PBRMaterialDef(
            name="Mat_Steel_MachinedGantry",
            base_color=hex_rgba("#88929E"),
            metallic=0.90,
            roughness=0.20,
            texture_path=tex_cargo("steel_machined_gantry.png"),
        ),
        "charcoal_pad": PBRMaterialDef(
            name="Mat_Fabric_CharcoalFlightpad",
            base_color=hex_rgba("#242932"),
            metallic=0.02,
            roughness=0.78,
            texture_path=tex_cargo("fabric_charcoal_flightpad.png"),
        ),
        "navy_pad": PBRMaterialDef(
            name="Mat_Fabric_OrbitalNavyPad",
            base_color=hex_rgba("#1D2C3C"),
            metallic=0.02,
            roughness=0.76,
            texture_path=tex_cargo("fabric_orbital_navy_pad.png"),
        ),
        "accent_orange": PBRMaterialDef(
            name="Mat_Accent_SignalOrange",
            base_color=hex_rgba("#D95B26"),
            metallic=0.06,
            roughness=0.48,
            texture_path=tex_cargo("accent_signal_orange.png"),
        ),
        "oled_logistics": PBRMaterialDef(
            name="Mat_OLED_CargoDroneLogistics",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.10,
            roughness=0.14,
            emissive=(0.35, 0.90, 1.0),
            texture_path=tex_cargo("oled_cargo_drone_logistics.png"),
        ),
        "glass_cargo": PBRMaterialDef(
            name="Mat_Glass_CargoBay_Translucent",
            base_color=(0.55, 0.90, 1.0, 0.19),
            metallic=0.10,
            roughness=0.08,
            emissive=(0.0, 0.15, 0.22),
            texture_path=tex_cargo("glass_cargo_bay_translucent.png"),
            double_sided=True,
            alpha_mode="BLEND",
        ),
        "led_cyan": PBRMaterialDef(
            name="Mat_Emissive_CyanLiDARLED",
            base_color=hex_rgba("#00E5FF"),
            metallic=0.0,
            roughness=0.14,
            emissive=(0.0, 0.92, 1.0),
            texture_path=tex_cargo("led_cyan_strip.png"),
        ),
        "led_amber": PBRMaterialDef(
            name="Mat_Emissive_AmberBeaconLED",
            base_color=hex_rgba("#FF9500"),
            metallic=0.0,
            roughness=0.15,
            emissive=(1.0, 0.58, 0.0),
            texture_path=tex_cargo("led_amber_strip.png"),
        ),
        "led_uv": PBRMaterialDef(
            name="Mat_Emissive_UVChargeLED",
            base_color=hex_rgba("#7B5CFF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.55, 0.38, 1.0),
            texture_path=tex_cargo("led_uv_violet.png"),
        ),
    }


# ==============================================================================
# SHARED 3D ISO CONTAINER MATRIX & AUTONOMOUS LOGISTICS DRONE HELPERS
# ==============================================================================
def make_interlocking_iso_container_matrix(
    cx: float = -0.36,
    cz: float = 0.0,
    y_bot: float = 0.22,
    y_top: float = 2.28,
    width: float = 1.54,
):
    """
    Builds a 2x2 Matrix of Interlocking 45°-Chamfered Pressurized ISO Cargo Containers
    (scaling up the locked footlocker_winner_01 aesthetic) under an overhead magnetic hoist rail:
    - Each container has a bevel-framed translucent inspection window (glass_cargo_bay_translucent.png)
    - Inside each container: 3D stowed aerospace-white supply drums, strapped orbital-navy cargo pallet bundles,
      Li-S power cylinders, and internal cyan LED strips
    - Lower-left container features an angled 35° open lid on pneumatic struts
    Returns: (slate_rack_geom, steel_hoist_geom, white_drums_geom, navy_pallets_geom,
              orange_locks_geom, cyan_leds_geom, glass_windows_geom)
    """
    slate_parts = []
    steel_parts = [
        # Overhead brushed-steel magnetic grappling hoist I-beam & crane trolley
        make_beveled_box((width + 0.14, 0.12, 0.26), center=(cx, y_top + 0.14, cz + 0.18), bevel=0.02),
        make_beveled_box((0.36, 0.10, 0.34), center=(cx - 0.18, y_top + 0.04, cz + 0.22), bevel=0.015),
    ]
    white_parts = []
    navy_parts = []
    orange_parts = [
        # Overhead crane trolley magnetic grappling hooks
        make_beveled_box((0.24, 0.08, 0.14), center=(cx - 0.18, y_top - 0.04, cz + 0.24), bevel=0.012),
    ]
    cyan_parts = []
    glass_windows = []

    col_offs = [-0.38 * width / 1.54, 0.38 * width / 1.54]
    row_ys = [y_bot + 0.44, y_bot + 1.42]
    cell_w = 0.68 * (width / 1.54)
    cell_h = 0.84

    for r_idx, cy_cell in enumerate(row_ys):
        # Horizontal rack shelf beam
        slate_parts.append(make_beveled_box((width, 0.06, 1.24), center=(cx, cy_cell - 0.44, cz), bevel=0.012))
        for c_idx, x_off in enumerate(col_offs):
            ccx = cx + x_off
            # Outer chamfered container shell with open front inspection cutout
            slate_parts.extend([
                make_beveled_box((cell_w, 0.08, 1.16), center=(ccx, cy_cell - 0.36, cz), bevel=0.015),
                make_beveled_box((cell_w, 0.08, 1.16), center=(ccx, cy_cell + 0.36, cz), bevel=0.015),
                make_beveled_box((0.08, cell_h, 1.16), center=(ccx - cell_w * 0.44, cy_cell, cz), bevel=0.015),
                make_beveled_box((0.08, cell_h, 1.16), center=(ccx + cell_w * 0.44, cy_cell, cz), bevel=0.015),
                make_beveled_box((cell_w - 0.06, cell_h - 0.06, 0.06), center=(ccx, cy_cell, cz - 0.54), bevel=0.01),
            ])
            # Brushed-steel chamfered container bezel frame
            steel_parts.extend([
                make_beveled_box((cell_w - 0.04, 0.036, 0.04), center=(ccx, cy_cell + 0.34, cz + 0.56), bevel=0.006),
                make_beveled_box((cell_w - 0.04, 0.036, 0.04), center=(ccx, cy_cell - 0.34, cz + 0.56), bevel=0.006),
            ])

            # Signal-orange corner ISO magnetic twist-locks
            for sx in [-1.0, 1.0]:
                orange_parts.append(
                    make_beveled_box((0.08, 0.05, 0.06), center=(ccx + sx * (cell_w * 0.36), cy_cell - 0.34, cz + 0.58), bevel=0.008)
                )

            # 3D Interior Stowed Cargo inside every translucent container bay:
            # 1) Two vertical aerospace-white orbital supply drums + orange cap
            white_parts.extend([
                make_cylinder(0.095, 0.095, 0.46, center=(ccx - 0.14, cy_cell - 0.08, cz + 0.12), segments=12, axis="y"),
                make_cylinder(0.082, 0.082, 0.42, center=(ccx - 0.14, cy_cell - 0.10, cz - 0.18), segments=10, axis="y"),
            ])
            orange_parts.append(make_cylinder(0.065, 0.065, 0.04, center=(ccx - 0.14, cy_cell + 0.16, cz + 0.12), segments=10, axis="y"))
            # 2) Sculpted orbital-navy strapped soft-goods cargo bundle
            navy_parts.append(
                make_sculpted_cushion(
                    (0.24, 0.34, 0.36),
                    center=(ccx + 0.12, cy_cell - 0.12, cz + 0.10),
                    res=(4, 3, 3),
                    roundness=0.32,
                    belly_puff=0.05,
                    tuft_grid=(2, 2),
                    tuft_depth=0.012,
                    crease_freq=0,
                )
            )
            # 3) Internal top cyan LED strip lighting the container interior
            cyan_parts.append(make_beveled_box((cell_w - 0.18, 0.022, 0.04), center=(ccx, cy_cell + 0.29, cz + 0.42), bevel=0.004))

            # Translucent polycarbonate container window (lower-left container posed 30° ajar on pneumatic struts!)
            if r_idx == 0 and c_idx == 0:
                ajar_win = transform_geom(
                    make_quad_panel((-cell_w * 0.40, -0.30, 0.0), (cell_w * 0.40, -0.30, 0.0), (cell_w * 0.40, 0.30, 0.0), (-cell_w * 0.40, 0.30, 0.0)),
                    translate=(ccx, cy_cell + 0.08, cz + 0.62),
                    rot_xyz_deg=(-26.0, 0.0, 0.0),
                )
                glass_windows.append(ajar_win)
            else:
                glass_windows.append(
                    make_quad_panel(
                        (ccx - cell_w * 0.40, cy_cell - 0.30, cz + 0.57),
                        (ccx + cell_w * 0.40, cy_cell - 0.30, cz + 0.57),
                        (ccx + cell_w * 0.40, cy_cell + 0.30, cz + 0.57),
                        (ccx - cell_w * 0.40, cy_cell + 0.30, cz + 0.57),
                    )
                )

    return (
        merge_geometries(slate_parts),
        merge_geometries(steel_parts),
        merge_geometries(white_parts),
        merge_geometries(navy_parts),
        merge_geometries(orange_parts),
        merge_geometries(cyan_parts),
        merge_geometries(glass_windows),
    )


def make_autonomous_logistics_drone_and_dock(
    dock_cx: float,
    dock_cz: float = 0.0,
    drone_y: float = 1.72,
    console_y: float = 0.78,
):
    """
    Builds Part 3 & Part 4 in the Autonomous Logistics Drone Docking & Manifest Tower:
    - 3D Autonomous Octo-Thruster Utility Cargo Drone suspended in its inductive recharge cradle:
      * Octagonal aerospace-white & carbon-slate carapace + upper LiDAR sensor dome
      * 4 angled brushed-steel ducted thruster/rotor pods
      * Ventral signal-orange magnetic cargo grappling claws holding a mini Li-S power cell
      * Glowing cyan (#00E5FF) optical LiDAR sensor eye & UV-violet inductive charge ring
    - Translucent polycarbonate drone hangar safety shield (glass_cargo_bay_translucent.png)
    - Lower Centrifuge Mass-Balance & RFID Manifest OLED Terminal (oled_cargo_drone_logistics.png)
      + coiled inductive power umbilical hoses + signal-orange tie-down winch/release lever
    Returns: (white_drone_geom, steel_thrusters_cradle_geom, charcoal_hoses_pads_geom,
              orange_claws_winch_geom, oled_screen_geom, cyan_lidar_geom, uv_charge_geom, glass_shield_geom)
    """
    # 1. 3D Autonomous Octo-Thruster Utility Cargo Drone (Y ~ drone_y)
    d_prof = [(0.0, 0.0), (0.20, 0.01), (0.22, 0.06), (0.18, 0.13), (0.10, 0.17), (0.0, 0.19)]
    white_parts = [
        # Main octagonal aerospace-white drone carapace & upper LiDAR dome
        make_sculpted_cushion((0.46, 0.22, 0.42), center=(dock_cx, drone_y, dock_cz + 0.04), res=(5, 3, 4), roundness=0.38, belly_puff=0.05, crease_freq=0),
        make_lathe_dome(d_prof, center=(dock_cx, drone_y + 0.08, dock_cz + 0.04), segments=12, subdivide_profile=1),
        # Rear hangar reflective liner plate
        make_beveled_box((0.68, 1.06, 0.03), center=(dock_cx, drone_y - 0.02, dock_cz - 0.24), bevel=0.008),
    ]

    steel_parts = [
        # Inductive recharge cradle yoke & upper/lower hangar bezels
        make_cylinder(0.26, 0.26, 0.035, center=(dock_cx, drone_y - 0.34, dock_cz + 0.04), segments=16, axis="y"),
        make_beveled_box((0.68, 0.04, 0.36), center=(dock_cx, drone_y - 0.50, dock_cz + 0.06), bevel=0.008),
        make_beveled_box((0.68, 0.04, 0.36), center=(dock_cx, drone_y + 0.48, dock_cz + 0.06), bevel=0.008),
    ]
    # 4 angled ducted thruster/rotor pods around the drone body
    for tx_s in [-1.0, 1.0]:
        for tz_s in [-1.0, 1.0]:
            px = dock_cx + tx_s * 0.26
            pz = dock_cz + 0.04 + tz_s * 0.20
            arm_pts = sample_filleted_polyline([(dock_cx + tx_s * 0.14, drone_y, dock_cz + 0.04), (px, drone_y + 0.03, pz)], 0.03, 2)
            steel_parts.append(make_swept_tube(arm_pts, radius=0.018, radial_segments=8))
            steel_parts.append(
                transform_geom(
                    make_cylinder(0.085, 0.075, 0.11, segments=12, axis="y"),
                    translate=(px, drone_y + 0.02, pz),
                    rot_xyz_deg=(tz_s * 8.0, 0.0, -tx_s * 10.0),
                )
            )

    # Ventral signal-orange magnetic cargo grappling claws + lower tie-down winch handwheel
    orange_parts = []
    for cx_s in [-1.0, 1.0]:
        claw_pts = sample_filleted_polyline(
            [
                (dock_cx + cx_s * 0.14, drone_y - 0.10, dock_cz + 0.06),
                (dock_cx + cx_s * 0.19, drone_y - 0.22, dock_cz + 0.08),
                (dock_cx + cx_s * 0.09, drone_y - 0.30, dock_cz + 0.08),
            ],
            fillet_radius=0.04,
            corner_subdivs=3,
        )
        orange_parts.append(make_swept_tube(claw_pts, radius=0.018, radial_segments=8))

    wh_or, wh_st = make_rotary_override_handwheel(cx=dock_cx + 0.16, cy=0.38, cz=dock_cz + 0.30, radius=0.11)
    orange_parts.append(wh_or)
    steel_parts.append(wh_st)
    # Guarded signal-orange magnetic pallet release lever
    orange_parts.append(make_beveled_box((0.14, 0.04, 0.05), center=(dock_cx - 0.16, 0.38, dock_cz + 0.30), bevel=0.008))

    # Charcoal flightpad bumper cushions & coiled inductive power umbilical hoses
    charcoal_parts = [
        make_sculpted_cushion((0.56, 0.06, 0.32), center=(dock_cx, drone_y - 0.44, dock_cz + 0.04), res=(4, 2, 3), roundness=0.35, belly_puff=0.03, crease_freq=0),
    ]
    for hx_off in [-0.16, 0.16]:
        u_pts = sample_filleted_polyline(
            [
                (dock_cx + hx_off, drone_y - 0.44, dock_cz + 0.14),
                (dock_cx + hx_off * 1.25, drone_y - 0.24, dock_cz + 0.20),
                (dock_cx + hx_off * 0.75, drone_y - 0.06, dock_cz + 0.10),
            ],
            fillet_radius=0.06,
            corner_subdivs=4,
        )
        charcoal_parts.append(make_swept_tube(u_pts, radius=0.016, radial_segments=8))

    # Glowing Cyan optical LiDAR eye on front of drone + UV-violet inductive charge ring
    cyan_lidar = merge_geometries([
        make_cylinder(0.058, 0.058, 0.04, center=(dock_cx, drone_y + 0.02, dock_cz + 0.25), segments=12, axis="z"),
        make_beveled_box((0.56, 0.024, 0.04), center=(dock_cx, drone_y + 0.44, dock_cz + 0.22), bevel=0.004),
    ])
    uv_charge = make_cylinder(0.22, 0.22, 0.028, center=(dock_cx, drone_y - 0.32, dock_cz + 0.04), segments=14, axis="y")

    oled_screen = make_quad_panel(
        (dock_cx - 0.26, console_y - 0.16, dock_cz + 0.30),
        (dock_cx + 0.26, console_y - 0.16, dock_cz + 0.30),
        (dock_cx + 0.26, console_y + 0.22, dock_cz + 0.30),
        (dock_cx - 0.26, console_y + 0.22, dock_cz + 0.30),
    )
    glass_shield = make_quad_panel(
        (dock_cx - 0.32, drone_y - 0.48, dock_cz + 0.30),
        (dock_cx + 0.32, drone_y - 0.48, dock_cz + 0.30),
        (dock_cx + 0.32, drone_y + 0.46, dock_cz + 0.30),
        (dock_cx - 0.32, drone_y + 0.46, dock_cz + 0.30),
    )

    return (
        merge_geometries(white_parts),
        merge_geometries(steel_parts),
        merge_geometries(charcoal_parts),
        merge_geometries(orange_parts),
        oled_screen,
        cyan_lidar,
        uv_charge,
        glass_shield,
    )


# ==============================================================================
# CANDIDATE 01: AEGIS-7 OCTAGONAL ISO CONTAINER MATRIX & OVERHEAD CRANE GANTRY (`cargo_gantry_r1_01.glb`)
# Dimensions: 2.55m W x 1.45m D x 2.60m H
# ==============================================================================
def build_01_octagonal_iso_container_matrix(mats):
    sm = []
    hull = [
        make_beveled_box((2.55, 0.18, 1.45), center=(0.0, 0.09, 0.0), bevel=0.035),
        make_beveled_box((2.55, 0.20, 1.45), center=(0.0, 2.50, 0.0), bevel=0.035),
        make_beveled_box((0.20, 2.26, 1.38), center=(-1.16, 1.28, 0.0), bevel=0.035),
        make_beveled_box((0.20, 2.26, 1.38), center=(1.16, 1.28, 0.0), bevel=0.035),
    ]
    add_part(sm, "Cargo01_OctagonalGantryStanchions", merge_geometries(hull), mats["gunmetal"])

    sl_c, st_c, wh_c, nv_c, or_c, cy_c, gl_c = make_interlocking_iso_container_matrix(
        cx=-0.38, cz=0.0, y_bot=0.20, y_top=2.24, width=1.48
    )
    wh_d, st_d, ch_d, or_d, oled_d, cy_d, uv_d, gl_d = make_autonomous_logistics_drone_and_dock(
        dock_cx=0.76, dock_cz=0.28, drone_y=1.72, console_y=0.80
    )

    add_part(sm, "Cargo01_CarbonSlateContainerMatrix", sl_c, mats["carbon_slate"])
    add_part(sm, "Cargo01_MachinedHoistBeamAndDroneThrusters", merge_geometries([st_c, st_d]), mats["steel_machined"])
    add_part(sm, "Cargo01_WhiteDroneCarapaceAndSupplyDrums", merge_geometries([wh_c, wh_d]), mats["aero_white"])
    add_part(sm, "Cargo01_OrbitalNavyCargoBundles", nv_c, mats["navy_pad"])
    add_part(sm, "Cargo01_CharcoalDroneCradleAndHoses", ch_d, mats["charcoal_pad"])
    add_part(sm, "Cargo01_SignalOrangeTwistLocksAndClaws", merge_geometries([or_c, or_d]), mats["accent_orange"])

    add_part(sm, "Cargo01_OLEDManifestTerminal", oled_d, mats["oled_logistics"])
    add_part(sm, "Cargo01_CyanLiDARAndCellLEDs", merge_geometries([cy_c, cy_d]), mats["led_cyan"])
    add_part(sm, "Cargo01_UVInductiveChargeRing", uv_d, mats["led_uv"])
    add_part(sm, "Cargo01_AmberHoistBeacon", make_beveled_box((2.20, 0.024, 0.05), center=(0.0, 2.38, 0.68), bevel=0.005), mats["led_amber"])
    add_part(sm, "Cargo01_TranslucentContainerAndDroneGlass", merge_geometries([gl_c, gl_d]), mats["glass_cargo"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "cargo_gantry_r1_01.glb"), sm, root_name="CargoGantryR1_01_OctagonalContainerMatrix")


# ==============================================================================
# CANDIDATE 02: DUAL-ZONE SPLIT INTERLOCKING CARGO RACK & AUTONOMOUS DRONE RECHARGE DOCK (`cargo_gantry_r1_02.glb`)
# Dimensions: 2.65m W x 1.45m D x 2.60m H (Signature 65/35 Aegis-7 Split-Bay Sibling!)
# ==============================================================================
def build_02_dual_zone_split_cargo_drone_dock(mats):
    sm = []
    # 1. Asymmetric 65% / 35% Split-Bay Gantry Frame (Left 2x2 ISO Matrix: X=-1.325..+0.395, Right Drone Tower: X=+0.395..+1.325)
    hull = [
        make_beveled_box((2.65, 0.18, 1.45), center=(0.0, 0.09, 0.0), bevel=0.035),
        make_beveled_box((2.65, 0.20, 1.45), center=(0.0, 2.50, 0.0), bevel=0.035),
        make_beveled_box((0.18, 2.26, 1.40), center=(-1.22, 1.28, 0.0), bevel=0.035),
        make_beveled_box((0.16, 2.26, 1.40), center=(1.23, 1.28, 0.0), bevel=0.035),
        # Center structural partition at X = +0.395
        make_beveled_box((0.12, 2.26, 1.38), center=(0.395, 1.28, 0.0), bevel=0.025),
        make_beveled_box((0.82, 2.26, 0.10), center=(0.82, 1.28, -0.64), bevel=0.02),
        make_beveled_box((0.78, 0.05, 1.32), center=(0.82, 1.12, 0.0), bevel=0.012),
    ]
    add_part(sm, "Cargo02_SplitBayGunmetalGantry", merge_geometries(hull), mats["gunmetal"])

    # 2. Left Bay 2x2 Interlocking ISO Container Matrix + Right Bay Autonomous Drone Dock & Manifest Tower
    sl_c, st_c, wh_c, nv_c, or_c, cy_c, gl_c = make_interlocking_iso_container_matrix(
        cx=-0.42, cz=0.0, y_bot=0.20, y_top=2.24, width=1.54
    )
    wh_d, st_d, ch_d, or_d, oled_d, cy_d, uv_d, gl_d = make_autonomous_logistics_drone_and_dock(
        dock_cx=0.82, dock_cz=0.30, drone_y=1.74, console_y=0.80
    )

    add_part(sm, "Cargo02_CarbonSlateInterlockingMatrix", sl_c, mats["carbon_slate"])
    add_part(sm, "Cargo02_MachinedHoistBeamAndDroneThrusters", merge_geometries([st_c, st_d]), mats["steel_machined"])
    add_part(sm, "Cargo02_WhiteDroneCarapaceAndSupplyDrums", merge_geometries([wh_c, wh_d]), mats["aero_white"])
    add_part(sm, "Cargo02_OrbitalNavyCargoBundles", nv_c, mats["navy_pad"])
    add_part(sm, "Cargo02_CharcoalDroneCradleAndUmbilicals", ch_d, mats["charcoal_pad"])
    add_part(sm, "Cargo02_SignalOrangeTwistLocksClawsAndWinch", merge_geometries([or_c, or_d]), mats["accent_orange"])

    add_part(sm, "Cargo02_RightTowerOLEDManifestTerminal", oled_d, mats["oled_logistics"])
    add_part(sm, "Cargo02_CyanLiDARAndContainerLEDs", merge_geometries([cy_c, cy_d]), mats["led_cyan"])
    add_part(sm, "Cargo02_UVInductiveChargeCradle", uv_d, mats["led_uv"])
    add_part(
        sm,
        "Cargo02_AmberHoistAndSkidBeacons",
        merge_geometries([
            make_beveled_box((1.58, 0.024, 0.05), center=(-0.42, 2.38, 0.68), bevel=0.005),
            make_beveled_box((2.36, 0.022, 0.04), center=(0.0, 0.16, 0.68), bevel=0.004),
        ]),
        mats["led_amber"],
    )
    add_part(sm, "Cargo02_TranslucentContainerWindowsAndDroneShield", merge_geometries([gl_c, gl_d]), mats["glass_cargo"])

    out_p = os.path.join(OUT_GLB_DIR, "cargo_gantry_r1_02.glb")
    info = center_and_export_glb(out_p, sm, root_name="CargoGantryR1_02_DualZoneSplitCargoDroneDock")

    # Copy Winner #02 to all canonical winner aliases
    for w_alias in [
        "cargo_gantry_winner_01_split_drone_rack.glb",
        "cargo_gantry_winner_01_dual_zone_gantry.glb",
        "cargo_gantry_winner_01_logistics_gantry.glb",
        "cargo_gantry_winner_01.glb",
    ]:
        shutil.copyfile(out_p, os.path.join(WINNERS_DIR, w_alias))
    return info


# ==============================================================================
# CANDIDATE 03: HONEYCOMB HEX-CELL CONTAINER HIVE & CANTILEVERED LOADER ARM (`cargo_gantry_r1_03.glb`)
# Dimensions: 2.60m W x 1.48m D x 2.60m H
# ==============================================================================
def build_03_honeycomb_hexcell_loader_arm(mats):
    sm = []
    hull = [
        make_beveled_box((2.60, 0.18, 1.48), center=(0.0, 0.09, 0.0), bevel=0.035),
        make_beveled_box((2.60, 0.20, 1.48), center=(0.0, 2.50, 0.0), bevel=0.035),
        make_beveled_box((0.20, 2.26, 1.40), center=(-1.18, 1.28, 0.0), bevel=0.035),
        make_beveled_box((0.20, 2.26, 1.40), center=(1.18, 1.28, 0.0), bevel=0.035),
    ]
    add_part(sm, "Cargo03_HexHiveGunmetalFrame", merge_geometries(hull), mats["gunmetal"])

    sl_c, st_c, wh_c, nv_c, or_c, cy_c, gl_c = make_interlocking_iso_container_matrix(
        cx=-0.40, cz=0.0, y_bot=0.20, y_top=2.24, width=1.50
    )
    wh_d, st_d, ch_d, or_d, oled_d, cy_d, uv_d, gl_d = make_autonomous_logistics_drone_and_dock(
        dock_cx=0.78, dock_cz=0.28, drone_y=1.70, console_y=0.80
    )

    loader_arm = sample_filleted_polyline([(0.42, 2.20, 0.20), (0.78, 2.15, 0.44), (0.78, 1.92, 0.34)], 0.06, 4)
    add_part(sm, "Cargo03_CarbonSlateHexCells", sl_c, mats["carbon_slate"])
    add_part(sm, "Cargo03_LoaderArmAndThrusters", merge_geometries([st_c, st_d, make_swept_tube(loader_arm, 0.034, 8)]), mats["steel_machined"])
    add_part(sm, "Cargo03_WhiteDroneAndDrums", merge_geometries([wh_c, wh_d]), mats["aero_white"])
    add_part(sm, "Cargo03_NavyPalletPacks", nv_c, mats["navy_pad"])
    add_part(sm, "Cargo03_CharcoalPadsAndHoses", ch_d, mats["charcoal_pad"])
    add_part(sm, "Cargo03_SignalOrangeForkliftClaws", merge_geometries([or_c, or_d]), mats["accent_orange"])

    add_part(sm, "Cargo03_OLEDManifestConsole", oled_d, mats["oled_logistics"])
    add_part(sm, "Cargo03_CyanHiveLEDs", merge_geometries([cy_c, cy_d]), mats["led_cyan"])
    add_part(sm, "Cargo03_UVChargeRing", uv_d, mats["led_uv"])
    add_part(sm, "Cargo03_AmberSafetyStrip", make_beveled_box((2.24, 0.024, 0.05), center=(0.0, 2.38, 0.68), bevel=0.005), mats["led_amber"])
    add_part(sm, "Cargo03_TranslucentHexPortholesAndShield", merge_geometries([gl_c, gl_d]), mats["glass_cargo"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "cargo_gantry_r1_03.glb"), sm, root_name="CargoGantryR1_03_HoneycombHexLoaderArm")


# ==============================================================================
# CANDIDATE 04: VERTICAL PATERNOSTER CAROUSEL RACK & TWIN DRONE PERCH (`cargo_gantry_r1_04.glb`)
# Dimensions: 2.55m W x 1.46m D x 2.62m H
# ==============================================================================
def build_04_vertical_paternoster_carousel_rack(mats):
    sm = []
    hull = [
        make_beveled_box((2.55, 0.18, 1.46), center=(0.0, 0.09, 0.0), bevel=0.035),
        make_beveled_box((2.55, 0.22, 1.46), center=(0.0, 2.51, 0.0), bevel=0.035),
        make_beveled_box((0.20, 2.28, 1.38), center=(-1.16, 1.29, 0.0), bevel=0.035),
        make_beveled_box((0.20, 2.28, 1.38), center=(1.16, 1.29, 0.0), bevel=0.035),
    ]
    add_part(sm, "Cargo04_PaternosterCarbonFrame", merge_geometries(hull), mats["carbon_slate"])

    sl_c, st_c, wh_c, nv_c, or_c, cy_c, gl_c = make_interlocking_iso_container_matrix(
        cx=-0.38, cz=0.0, y_bot=0.20, y_top=2.24, width=1.48
    )
    wh_d, st_d, ch_d, or_d, oled_d, cy_d, uv_d, gl_d = make_autonomous_logistics_drone_and_dock(
        dock_cx=0.76, dock_cz=0.28, drone_y=1.74, console_y=0.80
    )

    add_part(sm, "Cargo04_GunmetalCarouselPods", sl_c, mats["gunmetal"])
    add_part(sm, "Cargo04_PaternosterDriveAndThrusters", merge_geometries([st_c, st_d]), mats["steel_machined"])
    add_part(sm, "Cargo04_WhiteDroneAndDrums", merge_geometries([wh_c, wh_d]), mats["aero_white"])
    add_part(sm, "Cargo04_NavyCargoPacks", nv_c, mats["navy_pad"])
    add_part(sm, "Cargo04_CharcoalCradlePads", ch_d, mats["charcoal_pad"])
    add_part(sm, "Cargo04_SignalOrangeChainLocks", merge_geometries([or_c, or_d]), mats["accent_orange"])

    add_part(sm, "Cargo04_OLEDOperatorBridge", oled_d, mats["oled_logistics"])
    add_part(sm, "Cargo04_CyanCarouselLEDs", merge_geometries([cy_c, cy_d]), mats["led_cyan"])
    add_part(sm, "Cargo04_UVChargePerch", uv_d, mats["led_uv"])
    add_part(sm, "Cargo04_AmberElevatorBeacons", make_beveled_box((2.20, 0.024, 0.05), center=(0.0, 2.38, 0.68), bevel=0.005), mats["led_amber"])
    add_part(sm, "Cargo04_TranslucentPodWindows", merge_geometries([gl_c, gl_d]), mats["glass_cargo"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "cargo_gantry_r1_04.glb"), sm, root_name="CargoGantryR1_04_VerticalPaternosterRack")


# ==============================================================================
# CANDIDATE 05: HEAVY PRESSURIZED CRYO-TANKER ISO FRAME & TELEMETRY DOCK (`cargo_gantry_r1_05.glb`)
# Dimensions: 2.65m W x 1.50m D x 2.60m H
# ==============================================================================
def build_05_heavy_cryotanker_iso_frame(mats):
    sm = []
    hull = [
        make_beveled_box((2.65, 0.18, 1.50), center=(0.0, 0.09, 0.0), bevel=0.035),
        make_beveled_box((2.65, 0.20, 1.50), center=(0.0, 2.50, 0.0), bevel=0.035),
        make_beveled_box((0.20, 2.26, 1.42), center=(-1.20, 1.28, 0.0), bevel=0.035),
        make_beveled_box((0.20, 2.26, 1.42), center=(1.20, 1.28, 0.0), bevel=0.035),
    ]
    add_part(sm, "Cargo05_CryoTankerGunmetalFrame", merge_geometries(hull), mats["gunmetal"])

    sl_c, st_c, wh_c, nv_c, or_c, cy_c, gl_c = make_interlocking_iso_container_matrix(
        cx=-0.40, cz=0.0, y_bot=0.20, y_top=2.24, width=1.52
    )
    wh_d, st_d, ch_d, or_d, oled_d, cy_d, uv_d, gl_d = make_autonomous_logistics_drone_and_dock(
        dock_cx=0.80, dock_cz=0.30, drone_y=1.72, console_y=0.80
    )

    add_part(sm, "Cargo05_CarbonSlateISOFrame", sl_c, mats["carbon_slate"])
    add_part(sm, "Cargo05_MachinedHoistAndThrusters", merge_geometries([st_c, st_d]), mats["steel_machined"])
    add_part(sm, "Cargo05_WhiteCryoDrumsAndDrone", merge_geometries([wh_c, wh_d]), mats["aero_white"])
    add_part(sm, "Cargo05_NavyPalletBundles", nv_c, mats["navy_pad"])
    add_part(sm, "Cargo05_CharcoalBumperPads", ch_d, mats["charcoal_pad"])
    add_part(sm, "Cargo05_SignalOrangeTankValvesAndClaws", merge_geometries([or_c, or_d]), mats["accent_orange"])

    add_part(sm, "Cargo05_OLEDTelemetryKiosk", oled_d, mats["oled_logistics"])
    add_part(sm, "Cargo05_CyanLiDARAndBayLEDs", merge_geometries([cy_c, cy_d]), mats["led_cyan"])
    add_part(sm, "Cargo05_UVChargePad", uv_d, mats["led_uv"])
    add_part(sm, "Cargo05_AmberTankerBeacon", make_beveled_box((2.28, 0.024, 0.05), center=(0.0, 2.38, 0.70), bevel=0.005), mats["led_amber"])
    add_part(sm, "Cargo05_TranslucentCargoAndDroneGlass", merge_geometries([gl_c, gl_d]), mats["glass_cargo"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "cargo_gantry_r1_05.glb"), sm, root_name="CargoGantryR1_05_CryoTankerISOFrame")


# ==============================================================================
# ROOM 10 AUXILIARY PROP (`cargo_mag_pallet_deck.glb`) & SHELL (`room_10_shell.glb`)
# ==============================================================================
def build_cargo_mag_pallet_deck(mats):
    """
    Builds Center Magnetic Pallet Deck (cargo_mag_pallet_deck.glb):
    2.60m W x 1.80m D chamfered carbon-slate & brushed-steel floor locking grid in the center loading lane
    with glowing amber corner lock beacons, signal-orange magnetic tie-down winches, and recessed translucent
    polycarbonate sub-floor mass-balance sensor windows (2,800-4,500 tris, BLEND glass).
    """
    sm = []
    skid = [
        make_beveled_box((2.60, 0.10, 1.80), center=(0.0, 0.05, 0.0), bevel=0.025),
        make_beveled_box((2.42, 0.05, 1.62), center=(0.0, 0.11, 0.0), bevel=0.015),
    ]
    add_part(sm, "MagPallet_CarbonSlateSkid", merge_geometries(skid), mats["carbon_slate"])

    steel_parts = []
    orange_parts = []
    amber_leds = []
    cyan_leds = []
    glass_windows = []

    # 4 quadrant magnetic locking rings + rotary tie-down winches + translucent mass-balance inspection ports
    for qx in [-0.68, 0.68]:
        for qz in [-0.46, 0.46]:
            ring = make_portal_oct_ring(0.92, 0.64, center_y=0.135, z_pos=qz, tube_r=0.018, chamfer=0.14)
            # Rotate ring to lie flat on XZ plane around (qx, 0.135, qz)
            r_flat = transform_geom(
                make_cylinder(0.32, 0.32, 0.024, segments=16, axis="y"),
                translate=(qx, 0.132, qz),
            )
            steel_parts.append(r_flat)
            wh_or, wh_st = make_rotary_override_handwheel(cx=qx, cy=0.14, cz=qz + (0.36 if qz > 0 else -0.36), radius=0.09)
            orange_parts.append(wh_or)
            steel_parts.append(wh_st)

            amber_leds.append(make_beveled_box((0.26, 0.02, 0.06), center=(qx, 0.135, qz + (0.28 if qz > 0 else -0.28)), bevel=0.004))
            cyan_leds.append(make_cylinder(0.18, 0.18, 0.018, center=(qx, 0.128, qz), segments=14, axis="y"))
            glass_windows.append(
                make_quad_panel(
                    (qx - 0.28, 0.142, qz - 0.22),
                    (qx + 0.28, 0.142, qz - 0.22),
                    (qx + 0.28, 0.142, qz + 0.22),
                    (qx - 0.28, 0.142, qz + 0.22),
                )
            )

    # Side guide rails & coiled power umbilicals along the pallet perimeter
    for sx in [-1.22, 1.22]:
        rail_pts = sample_filleted_polyline([(sx, 0.12, -0.78), (sx, 0.22, -0.45), (sx, 0.22, 0.45), (sx, 0.12, 0.78)], 0.06, 4)
        steel_parts.append(make_swept_tube(rail_pts, radius=0.022, radial_segments=8))

    add_part(sm, "MagPallet_MachinedLockRingsAndRails", merge_geometries(steel_parts), mats["steel_machined"])
    add_part(sm, "MagPallet_SignalOrangeTieDownWinches", merge_geometries(orange_parts), mats["accent_orange"])
    add_part(sm, "MagPallet_AmberCornerLockBeacons", merge_geometries(amber_leds), mats["led_amber"])
    add_part(sm, "MagPallet_CyanMassBalanceCoils", merge_geometries(cyan_leds), mats["led_cyan"])
    add_part(sm, "MagPallet_TranslucentSensorDeckPorts", merge_geometries(glass_windows), mats["glass_cargo"])

    p_main = os.path.join(WINNERS_DIR, "cargo_mag_pallet_deck.glb")
    info = center_and_export_glb(p_main, sm, root_name="CargoMagPalletDeck")
    for dst in [
        os.path.join(OUT_GLB_DIR, "cargo_mag_pallet_deck.glb"),
        os.path.join(ROOMS_DIR, "cargo_mag_pallet_deck.glb"),
        "/workspace/game-project/assets/glb/cargo_mag_pallet_deck.glb",
    ]:
        shutil.copyfile(p_main, dst)
    print(f"[cargo_mag_pallet_deck] Exported {p_main} ({info['triangles']} tris)")
    return info


def build_room_10_cargo_bay_shell(mats):
    """
    Builds Room 10 — Modular Cargo Hold & Logistics Drone Bay Architectural Shell (9.0m W x 10.0m D x 4.0m H):
    - 5 Heavy 45° Chamfered Octagonal Titanium Ribs (Z = -4.6, -2.3, 0.0, +2.3, +4.6)
    - Twin overhead brushed-steel magnetic bridge-crane rails (Y = 3.55m)
    - Recessed Amber Hazard (#FF9500) & Orbital Cyan (#00E5FF) loading-zone floor guide strips
    - Dual Location-Aware Logistics Observation Viewports (alphaMode: "BLEND", alpha ~ 0.18):
      1) North Zero-G Docking Hub & Cylinder Viewport (Z = -4.95m, X = -3.2m to +3.2m, Y = 1.15m to 3.35m)
      2) West Outer-Hull Freighter Approach Window (X = -4.45m, Z = -3.2m to +0.8m)
    """
    sm = []
    slate_deck = [
        make_beveled_box((9.00, 0.06, 10.00), center=(0.0, 0.03, 0.0), bevel=0.015),
        # East solid bulkhead wall
        make_beveled_box((0.12, 3.88, 9.90), center=(4.44, 2.00, 0.0), bevel=0.02),
        # West wall framing around Freighter Approach Window (Z = -3.2..+0.8, Y = 1.15..3.15)
        make_beveled_box((0.12, 1.10, 9.90), center=(-4.44, 0.58, 0.0), bevel=0.02),
        make_beveled_box((0.12, 0.80, 9.90), center=(-4.44, 3.56, 0.0), bevel=0.02),
        make_beveled_box((0.12, 2.04, 1.75), center=(-4.44, 2.15, -4.08), bevel=0.02),
        make_beveled_box((0.12, 2.04, 4.10), center=(-4.44, 2.15, 2.88), bevel=0.02),
        # North wall framing around 3-bay Zero-G Docking Hub Viewport (X = -3.2..+3.2, Y = 1.15..3.35)
        make_beveled_box((8.90, 1.10, 0.14), center=(0.0, 0.58, -4.93), bevel=0.02),
        make_beveled_box((8.90, 0.62, 0.14), center=(0.0, 3.66, -4.93), bevel=0.02),
        make_beveled_box((1.25, 2.22, 0.14), center=(-3.82, 2.25, -4.93), bevel=0.02),
        make_beveled_box((1.25, 2.22, 0.14), center=(3.82, 2.25, -4.93), bevel=0.02),
        make_beveled_box((0.22, 2.22, 0.14), center=(-1.06, 2.25, -4.93), bevel=0.02),
        make_beveled_box((0.22, 2.22, 0.14), center=(1.06, 2.25, -4.93), bevel=0.02),
    ]
    add_part(sm, "Room10_CarbonSlateDeckAndBulkheads", merge_geometries(slate_deck), mats["carbon_slate"])

    gunmetal_ribs = [
        make_beveled_box((9.00, 0.06, 10.00), center=(0.0, 3.97, 0.0), bevel=0.015),
    ]
    for z_rib in [-4.6, -2.3, 0.0, 2.3, 4.6]:
        gunmetal_ribs.extend([
            make_beveled_box((0.24, 3.88, 0.24), center=(-4.30, 2.00, z_rib), bevel=0.03),
            make_beveled_box((0.24, 3.88, 0.24), center=(4.30, 2.00, z_rib), bevel=0.03),
            make_beveled_box((8.80, 0.22, 0.24), center=(0.0, 3.85, z_rib), bevel=0.03),
            transform_geom(make_beveled_box((0.88, 0.20, 0.24), bevel=0.025), translate=(-3.92, 3.54, z_rib), rot_xyz_deg=(0.0, 0.0, 45.0)),
            transform_geom(make_beveled_box((0.88, 0.20, 0.24), bevel=0.025), translate=(3.92, 3.54, z_rib), rot_xyz_deg=(0.0, 0.0, -45.0)),
        ])
    add_part(sm, "Room10_OctagonalTitaniumRibs", merge_geometries(gunmetal_ribs), mats["gunmetal"])

    # Twin overhead brushed-steel magnetic bridge-crane rails (Y = 3.55m) & viewport bezels
    north_bezel = make_portal_oct_ring(6.46, 2.24, center_y=2.25, z_pos=-4.86, tube_r=0.038, chamfer=0.28)
    steel_parts = [
        north_bezel,
        make_beveled_box((0.12, 0.16, 9.20), center=(-2.35, 3.55, 0.0), bevel=0.02),
        make_beveled_box((0.12, 0.16, 9.20), center=(2.35, 3.55, 0.0), bevel=0.02),
        make_beveled_box((4.86, 0.14, 0.22), center=(0.0, 3.45, -1.65), bevel=0.02),
    ]
    add_part(sm, "Room10_BridgeCraneRailsAndBezels", merge_geometries(steel_parts), mats["steel_machined"])

    amber_strips = [
        make_beveled_box((0.06, 0.016, 8.80), center=(-1.65, 0.064, 0.0), bevel=0.004),
        make_beveled_box((0.06, 0.016, 8.80), center=(1.65, 0.064, 0.0), bevel=0.004),
    ]
    add_part(sm, "Room10_AmberHazardFloorGuides", merge_geometries(amber_strips), mats["led_amber"])

    cyan_strips = [
        make_beveled_box((0.06, 0.016, 8.80), center=(-2.15, 0.064, 0.0), bevel=0.004),
        make_beveled_box((0.06, 0.016, 8.80), center=(2.15, 0.064, 0.0), bevel=0.004),
        make_beveled_box((0.06, 0.032, 9.20), center=(-3.20, 3.72, 0.0), bevel=0.005),
        make_beveled_box((0.06, 0.032, 9.20), center=(3.20, 3.72, 0.0), bevel=0.005),
    ]
    add_part(sm, "Room10_CyanLoadingLaneGuides", merge_geometries(cyan_strips), mats["led_cyan"])

    viewports = [
        # North Zero-G Docking Hub & Cylinder Viewport (Z = -4.90m)
        make_quad_panel((-3.20, 1.14, -4.88), (3.20, 1.14, -4.88), (3.20, 3.36, -4.88), (-3.20, 3.36, -4.88)),
        # West Outer-Hull Freighter Approach Window (X = -4.40m, Z = -3.2..+0.8)
        make_quad_panel((-4.40, 1.14, 0.80), (-4.40, 1.14, -3.20), (-4.40, 3.16, -3.20), (-4.40, 3.16, 0.80)),
    ]
    add_part(sm, "Room10_DualTranslucentLogisticsViewports", merge_geometries(viewports), mats["glass_cargo"])

    p_main = os.path.join(ROOMS_DIR, "room_10_shell.glb")
    info = center_and_export_glb(p_main, sm, root_name="Room10_CargoBayShell")
    for dst in [
        os.path.join(ROOMS_DIR, "room_10_cargo_shell.glb"),
        os.path.join(ROOMS_DIR, "room_10_cargo_bay_shell.glb"),
        "/workspace/game-project/assets/glb/room_10_cargo_shell.glb",
        "/workspace/game-project/assets/glb/room_10_shell.glb",
    ]:
        shutil.copyfile(p_main, dst)
    print(f"[room_10_shell] Exported {p_main} and aliases ({info['triangles']} tris)")
    return info


def build_all_cargo_round1():
    mats = get_cargo_materials()
    builders = [
        build_01_octagonal_iso_container_matrix,
        build_02_dual_zone_split_cargo_drone_dock,
        build_03_honeycomb_hexcell_loader_arm,
        build_04_vertical_paternoster_carousel_rack,
        build_05_heavy_cryotanker_iso_frame,
    ]
    results = []
    for fn in builders:
        info = fn(mats)
        fname = os.path.basename(info["filepath"])
        dims = info["dimensions"]
        print(
            f"[cargo_r1] Built {fname:24s} | {dims[0]:.2f}m W x {dims[2]:.2f}m D x {dims[1]:.2f}m H | "
            f"verts={info['vertices']:4d} | tris={info['triangles']:4d} | min_y={info['min'][1]:.5f}"
        )
        results.append(info)
    with open(os.path.join(OUT_GLB_DIR, "cargo_r1_manifest.json"), "w") as f:
        json.dump(results, f, indent=2)

    build_cargo_mag_pallet_deck(mats)
    build_room_10_cargo_bay_shell(mats)
    return results


if __name__ == "__main__":
    build_all_cargo_round1()
