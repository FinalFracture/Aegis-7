#!/usr/bin/env python3
"""
Builds all 5 Round-1 Hard Sci-Fi Personal Wall Terminal & Fold-Down Cabin Desk .glb models:
/workspace/game-project/assets/glb/walldesk_round1/walldesk_r1_01.glb .. walldesk_r1_05.glb

Follows /workspace/game-project/design/walldesk_round1/walldesk_r1_spec.md ("Aegis-7 Standard"):
- Bottom-center (0.0, 0.0, 0.0) floor pivot (min_y == 0.0000, centered X and Z), front facing +Z
- Deployed Working Mode: bulkhead housing at -Z, fold-down desk leaf horizontal at Y ~ 0.75m,
  articulated swing-arm / tuck-away crew stool in front (+Z, Y ~ 0.47m)
- Polygon budget: 2,800 - 5,500 triangles per candidate
- Mapped cleanly to Sloane's 10 textures in /workspace/game-project/assets/textures/walldesk_round1/
- Mandatory 4-Part 3D Cabin Workstation Kit inside every candidate:
  1. 45° Chamfered Bulkhead Housing & Deployed Fold-Down Desk Leaf (Y ~ 0.75m) with twin angled
     machined-steel hydraulic pistons / scissor struts, heavy knuckle hinges & signal-orange latches
  2. Recessed OLED Cabin Comms Terminal (oled_cabin_terminal.png) + Translucent Holo-HUD / Privacy Glass
     (glass_holo_hud_translucent.png, alphaMode: "BLEND", alpha ~ 0.19)
  3. 3D Desktop Props: Docked 3D Personal Data-Pad (oled_datapad_screen.png), Recessed Low-Profile
     Keyboard & Trackpad Zone with cyan edge illumination, and Lathed 3D Magnetic Thermal Mug with
     swept handle & sip-lid seated inside a glowing cyan magnetic coaster ring
  4. Articulated Swing-Arm or Tuck-Away Crew Stool (Y ~ 0.47m) with sculpted charcoal/navy flightpad
     seat cushion, tubular footrest ring, and signal-orange swivel/height release lever
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

TEX_WALLDESK_DIR = "/workspace/game-project/assets/textures/walldesk_round1"
OUT_GLB_DIR = "/workspace/game-project/assets/glb/walldesk_round1"
os.makedirs(OUT_GLB_DIR, exist_ok=True)


def tex_wd(fname: str) -> str:
    return os.path.join(TEX_WALLDESK_DIR, fname)


def get_walldesk_materials():
    return {
        "gunmetal": PBRMaterialDef(
            name="Mat_Titanium_GunmetalHull",
            base_color=hex_rgba("#1A1E24"),
            metallic=0.78,
            roughness=0.34,
            texture_path=tex_wd("titanium_gunmetal_hull.png"),
        ),
        "aero_white": PBRMaterialDef(
            name="Mat_Composite_AerospaceWhite",
            base_color=hex_rgba("#D8DEE6"),
            metallic=0.08,
            roughness=0.28,
            texture_path=tex_wd("composite_aerospace_white.png"),
        ),
        "carbon_slate": PBRMaterialDef(
            name="Mat_Carbon_SlateFrame",
            base_color=hex_rgba("#282E38"),
            metallic=0.58,
            roughness=0.40,
            texture_path=tex_wd("carbon_slate_frame.png"),
        ),
        "steel_machined": PBRMaterialDef(
            name="Mat_Steel_MachinedGantry",
            base_color=hex_rgba("#88929E"),
            metallic=0.90,
            roughness=0.22,
            texture_path=tex_wd("steel_machined_gantry.png"),
        ),
        "pad_charcoal": PBRMaterialDef(
            name="Mat_Fabric_CharcoalFlightpad",
            base_color=hex_rgba("#242932"),
            metallic=0.02,
            roughness=0.78,
            texture_path=tex_wd("fabric_charcoal_flightpad.png"),
        ),
        "pad_navy": PBRMaterialDef(
            name="Mat_Fabric_OrbitalNavyPad",
            base_color=hex_rgba("#1D2C3C"),
            metallic=0.02,
            roughness=0.76,
            texture_path=tex_wd("fabric_orbital_navy_pad.png"),
        ),
        "accent_orange": PBRMaterialDef(
            name="Mat_Accent_SignalOrange",
            base_color=hex_rgba("#D95B26"),
            metallic=0.06,
            roughness=0.48,
            texture_path=tex_wd("accent_signal_orange.png"),
        ),
        "oled_terminal": PBRMaterialDef(
            name="Mat_OLED_CabinTerminal",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.10,
            roughness=0.14,
            emissive=(0.35, 0.90, 1.0),
            texture_path=tex_wd("oled_cabin_terminal.png"),
        ),
        "oled_datapad": PBRMaterialDef(
            name="Mat_OLED_DatapadScreen",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.10,
            roughness=0.14,
            emissive=(0.32, 0.85, 1.0),
            texture_path=tex_wd("oled_datapad_screen.png"),
        ),
        "glass_holo": PBRMaterialDef(
            name="Mat_Glass_HoloHUD_Translucent",
            base_color=(0.55, 0.88, 1.0, 0.19),
            metallic=0.10,
            roughness=0.08,
            emissive=(0.0, 0.14, 0.22),
            texture_path=tex_wd("glass_holo_hud_translucent.png"),
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
        "led_ice": PBRMaterialDef(
            name="Mat_Emissive_IceWhiteLED",
            base_color=hex_rgba("#E0F4FF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.86, 0.95, 1.0),
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
# SHARED 3D DESKTOP PROPS & CREW STOOL GENERATORS
# ==============================================================================
def make_desktop_props_kit(
    desk_cx: float = 0.0,
    desk_top_y: float = 0.775,
    desk_cz: float = 0.08,
):
    """
    Builds Part 3 of the Mandatory Workstation Kit on the deployed horizontal desk leaf:
    - Docked 3D Personal Data-Pad / Slate (angled charging cradle + chamfered tablet + oled_datapad_screen.png)
    - Recessed Low-Profile Capacitive Keyboard & Trackpad Zone (carbon-slate key matrix + cyan edge glow)
    - Lathed 3D Magnetic Thermal Mug (insulated brushed-steel zero-G mug with swept D-handle & sip-lid)
      seated inside a glowing cyan magnetic coaster ring
    Returns: (white_cradle_geom, slate_kbd_and_pad_geom, steel_mug_geom, oled_datapad_geom, cyan_coaster_and_kbd_geom)
    """
    # 1. Docked 3D Personal Data-Pad on left-rear of desk leaf
    dp_x, dp_z = desk_cx - 0.21, desk_cz - 0.08
    white_cradle = [
        make_beveled_box((0.20, 0.025, 0.08), center=(dp_x, desk_top_y + 0.012, dp_z), bevel=0.006),
    ]
    pad_body = transform_geom(
        make_beveled_box((0.21, 0.15, 0.016), center=(0.0, 0.0, 0.0), bevel=0.005),
        translate=(dp_x, desk_top_y + 0.075, dp_z - 0.01),
        rot_xyz_deg=(-28.0, 12.0, 0.0),
    )
    pad_screen = transform_geom(
        make_quad_panel((-0.095, -0.065, 0.009), (0.095, -0.065, 0.009), (0.095, 0.065, 0.009), (-0.095, 0.065, 0.009)),
        translate=(dp_x, desk_top_y + 0.075, dp_z - 0.01),
        rot_xyz_deg=(-28.0, 12.0, 0.0),
    )

    # 2. Recessed Low-Profile Keyboard & Trackpad Inlay in center-front of desk leaf
    kb_x, kb_z = desk_cx - 0.03, desk_cz + 0.06
    slate_parts = [
        pad_body,
        make_beveled_box((0.34, 0.014, 0.14), center=(kb_x, desk_top_y + 0.005, kb_z), bevel=0.004),
        # Raised tactile key-row blocks
        make_beveled_box((0.24, 0.018, 0.095), center=(kb_x - 0.035, desk_top_y + 0.008, kb_z - 0.005), bevel=0.003),
        make_beveled_box((0.065, 0.016, 0.095), center=(kb_x + 0.125, desk_top_y + 0.007, kb_z - 0.005), bevel=0.003),
    ]

    # 3. Lathed 3D Magnetic Thermal Mug on right side of desk leaf
    mug_x, mug_z = desk_cx + 0.24, desk_cz + 0.02
    mug_profile = [
        (0.000, 0.000),
        (0.042, 0.000),
        (0.045, 0.015),
        (0.043, 0.095),
        (0.046, 0.105),
        (0.038, 0.115),
        (0.028, 0.115),
        (0.024, 0.105),
        (0.000, 0.105),
    ]
    mug_body = make_lathe_dome(mug_profile, center=(mug_x, desk_top_y + 0.004, mug_z), segments=18, subdivide_profile=1)
    handle_pts = sample_filleted_polyline(
        [
            (mug_x + 0.040, desk_top_y + 0.085, mug_z),
            (mug_x + 0.068, desk_top_y + 0.085, mug_z),
            (mug_x + 0.068, desk_top_y + 0.030, mug_z),
            (mug_x + 0.040, desk_top_y + 0.030, mug_z),
        ],
        fillet_radius=0.012,
        corner_subdivs=4,
    )
    mug_handle = make_swept_tube(handle_pts, radius=0.006, radial_segments=8)
    steel_mug = merge_geometries([mug_body, mug_handle])

    # Glowing cyan magnetic coaster ring + keyboard backlit rim
    coaster_pts = []
    for k in range(17):
        ang = (k / 16.0) * 2.0 * math.pi
        coaster_pts.append([mug_x + 0.052 * math.cos(ang), desk_top_y + 0.004, mug_z + 0.052 * math.sin(ang)])
    cyan_parts = [
        make_swept_tube(np.array(coaster_pts, dtype=np.float32), radius=0.004, radial_segments=8, closed_loop=True),
        make_beveled_box((0.35, 0.006, 0.148), center=(kb_x, desk_top_y + 0.002, kb_z), bevel=0.002),
    ]

    return (
        merge_geometries(white_cradle),
        merge_geometries(slate_parts),
        steel_mug,
        pad_screen,
        merge_geometries(cyan_parts),
    )


def make_articulated_crew_stool(
    stool_x: float = 0.0,
    seat_y: float = 0.47,
    stool_z: float = 0.22,
    mount_x: float = -0.34,
    mount_z: float = -0.16,
    style: str = "swing_arm",
):
    """
    Builds Part 4 of the Mandatory Workstation Kit:
    - Articulated swing-arm, twin-rail pedestal, zero-G perch, or turret crew stool
    - Sculpted ergonomic charcoal flightpad seat cushion + navy bolster trim
    - Tubular machined-steel footrest ring & signal-orange swivel/height release lever
    Returns: (steel_frame_geom, charcoal_seat_geom, navy_trim_geom, orange_lever_geom)
    """
    steel_parts = []
    navy_parts = []

    if style == "swing_arm":
        # Cantilevered tubular steel swing-arm pivoting from bulkhead mount out to stool center
        arm_pts = sample_filleted_polyline(
            [
                (mount_x, 0.24, mount_z),
                (mount_x, 0.24, stool_z * 0.55),
                (stool_x, 0.24, stool_z),
                (stool_x, seat_y - 0.04, stool_z),
            ],
            fillet_radius=0.08,
            corner_subdivs=6,
        )
        steel_parts.append(make_swept_tube(arm_pts, radius=0.026, radial_segments=12))
        steel_parts.append(make_cylinder(0.045, 0.045, 0.16, center=(mount_x, 0.24, mount_z), segments=12, axis="y"))
        # Floor stabilizer pad directly under stool post so it looks rock-solid
        steel_parts.append(make_cylinder(0.08, 0.06, 0.03, center=(stool_x, 0.015, stool_z), segments=14, axis="y"))
        steel_parts.append(make_cylinder(0.024, 0.024, 0.24, center=(stool_x, 0.13, stool_z), segments=12, axis="y"))
    elif style == "pedestal_track":
        # Twin floor-track rails + telescoping pedestal column
        steel_parts.append(make_beveled_box((0.28, 0.025, 0.44), center=(stool_x, 0.0125, stool_z - 0.10), bevel=0.008))
        steel_parts.append(make_cylinder(0.042, 0.034, seat_y - 0.04, center=(stool_x, (seat_y - 0.04) * 0.5, stool_z), segments=14, axis="y"))
    elif style == "zero_g_perch":
        # Angled forward-leaning perch column + dual knee-bolster pads
        col_pts = sample_filleted_polyline(
            [(stool_x, 0.02, stool_z - 0.12), (stool_x, 0.26, stool_z + 0.02), (stool_x, seat_y - 0.03, stool_z)],
            fillet_radius=0.07,
            corner_subdivs=5,
        )
        steel_parts.append(make_swept_tube(col_pts, radius=0.028, radial_segments=12))
        steel_parts.append(make_beveled_box((0.32, 0.03, 0.36), center=(stool_x, 0.015, stool_z - 0.05), bevel=0.01))
        navy_parts.append(make_sculpted_cushion((0.12, 0.07, 0.14), center=(stool_x - 0.11, 0.28, stool_z + 0.08), res=(4, 3, 4), roundness=0.40, belly_puff=0.04, crease_freq=0))
        navy_parts.append(make_sculpted_cushion((0.12, 0.07, 0.14), center=(stool_x + 0.11, 0.28, stool_z + 0.08), res=(4, 3, 4), roundness=0.40, belly_puff=0.04, crease_freq=0))
    else:
        # Heavy turret pedestal or folding tubular X-stool
        steel_parts.append(make_cylinder(0.16, 0.12, 0.04, center=(stool_x, 0.02, stool_z), segments=16, axis="y"))
        steel_parts.append(make_cylinder(0.045, 0.038, seat_y - 0.04, center=(stool_x, (seat_y - 0.04) * 0.5, stool_z), segments=14, axis="y"))

    # Tubular footrest ring around stool column at Y = 0.18m
    foot_pts = []
    for k in range(17):
        ang = (k / 16.0) * 2.0 * math.pi
        foot_pts.append([stool_x + 0.145 * math.cos(ang), 0.18, stool_z + 0.145 * math.sin(ang)])
    steel_parts.append(make_swept_tube(np.array(foot_pts, dtype=np.float32), radius=0.012, radial_segments=8, closed_loop=True))

    # Sculpted contoured charcoal flightpad seat cushion + low lumbar lip
    seat_cushion = [
        make_sculpted_cushion(
            (0.36, 0.075, 0.34),
            center=(stool_x, seat_y, stool_z),
            res=(6, 3, 6),
            roundness=0.38,
            belly_puff=0.05,
            pinch_corners=0.12,
            sag_center=0.012,
            crease_freq=0,
        ),
    ]
    navy_parts.append(
        make_sculpted_cushion(
            (0.32, 0.08, 0.08),
            center=(stool_x, seat_y + 0.055, stool_z + 0.13),
            res=(5, 3, 3),
            roundness=0.38,
            belly_puff=0.04,
            crease_freq=0,
        )
    )

    # Signal-orange height/swivel release lever under right edge of seat
    orange_lever = make_beveled_box((0.09, 0.024, 0.035), center=(stool_x + 0.14, seat_y - 0.045, stool_z + 0.04), bevel=0.005)

    return (
        merge_geometries(steel_parts),
        merge_geometries(seat_cushion),
        merge_geometries(navy_parts),
        orange_lever,
    )


# ==============================================================================
# CANDIDATE 01: RECESSED OCTAGONAL BULKHEAD FOLD-DOWN COMMS DESK (`walldesk_r1_01.glb`)
# Dimensions: 0.95m W x 0.62m D x 1.95m H
# ==============================================================================
def build_01_octagonal_fold_down_desk(mats):
    sm = []
    # 1. Outer 45° Chamfered Octagonal Gunmetal Bulkhead Niche (Z = -0.31 to -0.02)
    hull = [
        make_beveled_box((0.95, 0.12, 0.38), center=(0.0, 0.06, -0.12), bevel=0.025),
        make_beveled_box((0.95, 0.14, 0.38), center=(0.0, 1.88, -0.12), bevel=0.03),
        make_beveled_box((0.09, 1.76, 0.36), center=(-0.43, 0.96, -0.12), bevel=0.025),
        make_beveled_box((0.09, 1.76, 0.36), center=(0.43, 0.96, -0.12), bevel=0.025),
        make_beveled_box((0.86, 1.82, 0.07), center=(0.0, 0.96, -0.275), bevel=0.02),
    ]
    add_part(sm, "WallDesk01_OctagonalGunmetalHull", merge_geometries(hull), mats["gunmetal"])

    # 2. Recessed Orbital-Navy Acoustic Back Panel + Stool Lumbar Trim
    steel_stool, charcoal_seat, navy_stool, orange_lever = make_articulated_stool_or_wrapper(
        stool_x=0.0, seat_y=0.47, stool_z=0.20, mount_x=-0.34, mount_z=-0.12, style="swing_arm"
    )
    navy_parts = [
        make_sculpted_cushion((0.74, 0.98, 0.04), center=(0.0, 1.30, -0.22), res=(6, 5, 2), roundness=0.22, belly_puff=0.03, tuft_grid=(3, 2), tuft_depth=0.012, crease_freq=0),
        navy_stool,
    ]
    add_part(sm, "WallDesk01_OrbitalNavyAcousticBackwall", merge_geometries(navy_parts), mats["pad_navy"])

    # 3. Deployed Horizontal Aerospace-White & Carbon-Slate Fold-Down Desk Leaf (0.84m W x 0.44m D at Y = 0.75m)
    white_cradle, slate_kbd, steel_mug, oled_pad, cyan_props = make_desktop_props_kit(desk_cx=0.0, desk_top_y=0.775, desk_cz=0.06)
    white_parts = [
        make_beveled_box((0.84, 0.048, 0.44), center=(0.0, 0.75, 0.04), bevel=0.016),
        make_beveled_box((0.76, 0.04, 0.24), center=(0.0, 1.76, -0.10), bevel=0.01),
        white_cradle,
    ]
    add_part(sm, "WallDesk01_AerospaceWhiteDeskLeaf", merge_geometries(white_parts), mats["aero_white"])

    slate_parts = [
        make_beveled_box((0.76, 0.016, 0.36), center=(0.0, 0.77, 0.04), bevel=0.005),
        slate_kbd,
    ]
    add_part(sm, "WallDesk01_CarbonSlateInlayAndPad", merge_geometries(slate_parts), mats["carbon_slate"])

    # 4. Twin Diagonal Machined-Steel Hydraulic Telescopic Struts, Octagonal Bezel, Holo Micro-Arms & Mug
    strut_l = sample_filleted_polyline([(-0.37, 0.46, -0.18), (-0.37, 0.74, 0.18)], 0.02, 3)
    strut_r = sample_filleted_polyline([(0.37, 0.46, -0.18), (0.37, 0.74, 0.18)], 0.02, 3)
    steel_all = [
        make_chamfered_aperture_ring(0.86, 1.80, center_y=0.98, z_pos=-0.02, tube_r=0.028, chamfer=0.18),
        make_swept_tube(strut_l, radius=0.018, radial_segments=10),
        make_swept_tube(strut_r, radius=0.018, radial_segments=10),
        # Knuckle hinges at rear of desk leaf
        make_cylinder(0.024, 0.024, 0.12, center=(-0.28, 0.75, -0.16), segments=10, axis="x"),
        make_cylinder(0.024, 0.024, 0.12, center=(0.28, 0.75, -0.16), segments=10, axis="x"),
        # Micro-arms suspending the Holo-HUD combiner pane
        make_cylinder(0.010, 0.010, 0.12, center=(-0.26, 1.48, -0.12), segments=8, axis="z"),
        make_cylinder(0.010, 0.010, 0.12, center=(0.26, 1.48, -0.12), segments=8, axis="z"),
        steel_mug,
        steel_stool,
    ]
    add_part(sm, "WallDesk01_MachinedStrutsStoolAndMug", merge_geometries(steel_all), mats["steel_machined"])

    # 5. Signal-Orange Strut Locking Collars & Stool Release Lever
    orange_all = [
        make_cylinder(0.024, 0.024, 0.045, center=(-0.37, 0.60, 0.0), segments=10, axis="y"),
        make_cylinder(0.024, 0.024, 0.045, center=(0.37, 0.60, 0.0), segments=10, axis="y"),
        make_beveled_box((0.06, 0.028, 0.03), center=(-0.38, 0.75, 0.24), bevel=0.005),
        make_beveled_box((0.06, 0.028, 0.03), center=(0.38, 0.75, 0.24), bevel=0.005),
        orange_lever,
    ]
    add_part(sm, "WallDesk01_SignalOrangeLatches", merge_geometries(orange_all), mats["accent_orange"])

    # 6. Sculpted Charcoal Stool Seat Cushion
    add_part(sm, "WallDesk01_CharcoalStoolCushion", charcoal_seat, mats["pad_charcoal"])

    # 7. Widescreen OLED Cabin Comms Terminal + Docked Data-Pad Screen
    add_part(
        sm,
        "WallDesk01_WidescreenOLEDTerminal",
        make_quad_panel((-0.34, 1.06, -0.18), (0.34, 1.06, -0.18), (0.34, 1.48, -0.18), (-0.34, 1.48, -0.18)),
        mats["oled_terminal"],
    )
    add_part(sm, "WallDesk01_DockedDatapadOLED", oled_pad, mats["oled_datapad"])

    # 8. Practical Lighting: Overhead Ice-White Task Bar, Cyan Coaster/Cove, Amber Footlight
    add_part(sm, "WallDesk01_OverheadTaskLightIce", make_beveled_box((0.68, 0.022, 0.04), center=(0.0, 1.73, -0.02), bevel=0.004), mats["led_ice"])
    add_part(
        sm,
        "WallDesk01_CyanCoasterAndCove",
        merge_geometries([cyan_props, make_beveled_box((0.70, 0.020, 0.03), center=(0.0, 1.02, -0.17), bevel=0.004)]),
        mats["led_cyan"],
    )
    add_part(sm, "WallDesk01_AmberToeGuideLED", make_beveled_box((0.72, 0.020, 0.03), center=(0.0, 0.13, -0.04), bevel=0.004), mats["led_amber"])

    # 9. Floating Angled Translucent Holo-HUD Teleprompter Combiner Pane (alphaMode: "BLEND")
    holo_pane = transform_geom(
        make_quad_panel((-0.32, -0.16, 0.0), (0.32, -0.16, 0.0), (0.32, 0.16, 0.0), (-0.32, 0.16, 0.0)),
        translate=(0.0, 1.46, -0.04),
        rot_xyz_deg=(-18.0, 0.0, 0.0),
    )
    add_part(sm, "WallDesk01_FloatingHoloHUDCombiner", holo_pane, mats["glass_holo"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "walldesk_r1_01.glb"), sm, root_name="WallDeskR1_01_OctagonalFoldDownDesk")


def make_articulated_stool_or_wrapper(*args, **kwargs):
    return make_articulated_crew_stool(*args, **kwargs)


# ==============================================================================
# CANDIDATE 02: DUAL-TIER SPLIT COMMS & STORAGE DROP-LEAF STATION (`walldesk_r1_02.glb`)
# Dimensions: 1.05m W x 0.65m D x 2.00m H (Companion to Locker #02 & Vanity #03!)
# ==============================================================================
def build_02_dual_tier_split_station(mats):
    sm = []
    # 1. Asymmetric 68% / 32% Split-Bay Gunmetal Bulkhead Housing
    # Left Bay: X = -0.525 to +0.185 (0.71m wide); Right Bay: X = +0.185 to +0.525 (0.34m wide)
    cabinet = [
        make_beveled_box((1.05, 0.12, 0.42), center=(0.0, 0.06, -0.11), bevel=0.025),
        make_beveled_box((1.05, 0.14, 0.42), center=(0.0, 1.93, -0.11), bevel=0.03),
        make_beveled_box((0.08, 1.82, 0.40), center=(-0.485, 0.99, -0.11), bevel=0.025),
        make_beveled_box((0.08, 1.82, 0.40), center=(0.485, 0.99, -0.11), bevel=0.025),
        # Center vertical structural partition at X = +0.185
        make_beveled_box((0.05, 1.80, 0.38), center=(0.185, 0.99, -0.11), bevel=0.015),
        make_beveled_box((0.96, 1.84, 0.06), center=(0.0, 0.99, -0.29), bevel=0.02),
        # Right Bay 3-tier shelves at Y = 0.75 and Y = 1.35
        make_beveled_box((0.28, 0.035, 0.34), center=(0.335, 0.75, -0.11), bevel=0.008),
        make_beveled_box((0.28, 0.035, 0.34), center=(0.335, 1.35, -0.11), bevel=0.008),
    ]
    add_part(sm, "WallDesk02_SplitBayGunmetalCabinet", merge_geometries(cabinet), mats["gunmetal"])

    # 2. Left Bay Deployed Fold-Down Desk Leaf (centered at X = -0.16, Y = 0.75m) + Right Bay Backup Power Cells
    white_cradle, slate_kbd, steel_mug, oled_pad, cyan_props = make_desktop_props_kit(desk_cx=-0.16, desk_top_y=0.775, desk_cz=0.06)
    white_parts = [
        make_beveled_box((0.64, 0.046, 0.44), center=(-0.16, 0.75, 0.04), bevel=0.015),
        make_beveled_box((0.26, 1.72, 0.03), center=(0.335, 0.99, -0.25), bevel=0.01),
        # Bottom-right twin cylindrical emergency backup power cells
        make_cylinder(0.048, 0.048, 0.38, center=(0.28, 0.36, -0.10), segments=12, axis="y"),
        make_cylinder(0.048, 0.048, 0.38, center=(0.39, 0.36, -0.10), segments=12, axis="y"),
        white_cradle,
    ]
    add_part(sm, "WallDesk02_WhiteDeskLeafAndPowerCells", merge_geometries(white_parts), mats["aero_white"])

    # 3. Carbon-Slate Desk Inlay, Top Data-Cartridges & Middle Log Module
    slate_all = [
        make_beveled_box((0.58, 0.015, 0.36), center=(-0.16, 0.77, 0.04), bevel=0.005),
        slate_kbd,
        # Top-right shelf: 3 vertical personal data-cartridges in charging rack
        make_beveled_box((0.03, 0.18, 0.14), center=(0.25, 1.48, -0.10), bevel=0.005),
        make_beveled_box((0.03, 0.18, 0.14), center=(0.30, 1.48, -0.10), bevel=0.005),
        make_beveled_box((0.03, 0.18, 0.14), center=(0.35, 1.48, -0.10), bevel=0.005),
    ]
    add_part(sm, "WallDesk02_CarbonSlateInlayAndCartridges", merge_geometries(slate_all), mats["carbon_slate"])

    # 4. Machined-Steel Diagonal Struts, Knuckle Hinges, Tuck-Away Pedestal Stool & Thermal Mug
    steel_stool, charcoal_seat, navy_stool, orange_lever = make_articulated_crew_stool(
        stool_x=-0.16, seat_y=0.47, stool_z=0.21, style="pedestal_track"
    )
    s_l = sample_filleted_polyline([(-0.43, 0.48, -0.18), (-0.43, 0.74, 0.18)], 0.02, 3)
    s_r = sample_filleted_polyline([(0.12, 0.48, -0.18), (0.12, 0.74, 0.18)], 0.02, 3)
    steel_all = [
        make_swept_tube(s_l, radius=0.016, radial_segments=10),
        make_swept_tube(s_r, radius=0.016, radial_segments=10),
        make_cylinder(0.022, 0.022, 0.10, center=(-0.34, 0.75, -0.16), segments=10, axis="x"),
        make_cylinder(0.022, 0.022, 0.10, center=(0.02, 0.75, -0.16), segments=10, axis="x"),
        make_beveled_box((0.28, 0.024, 0.03), center=(0.335, 0.76, 0.06), bevel=0.005),
        make_beveled_box((0.28, 0.024, 0.03), center=(0.335, 1.36, 0.06), bevel=0.005),
        steel_mug,
        steel_stool,
    ]
    add_part(sm, "WallDesk02_MachinedStrutsMugAndStool", merge_geometries(steel_all), mats["steel_machined"])

    # 5. Middle-Right Shelf Sculpted 3D Orbital-Navy Comms Headset + Left Acoustic Pad
    headset_arc = sample_filleted_polyline([(0.27, 1.06, -0.08), (0.335, 1.20, -0.08), (0.40, 1.06, -0.08)], 0.05, 5)
    navy_all = [
        make_beveled_box((0.62, 0.92, 0.03), center=(-0.16, 1.32, -0.24), bevel=0.01),
        make_swept_tube(headset_arc, radius=0.014, radial_segments=8),
        make_sculpted_cushion((0.05, 0.09, 0.08), center=(0.27, 1.04, -0.08), res=(4, 3, 3), roundness=0.42, belly_puff=0.04, crease_freq=0),
        make_sculpted_cushion((0.05, 0.09, 0.08), center=(0.40, 1.04, -0.08), res=(4, 3, 3), roundness=0.42, belly_puff=0.04, crease_freq=0),
        navy_stool,
    ]
    add_part(sm, "WallDesk02_OrbitalNavyHeadsetAndAcoustic", merge_geometries(navy_all), mats["pad_navy"])
    add_part(sm, "WallDesk02_CharcoalStoolSeat", charcoal_seat, mats["pad_charcoal"])

    # 6. Signal-Orange Fold Latches, Power-Cell Terminals & Stool Lever
    orange_all = [
        orange_lever,
        make_cylinder(0.052, 0.052, 0.04, center=(0.28, 0.56, -0.10), segments=12, axis="y"),
        make_cylinder(0.052, 0.052, 0.04, center=(0.39, 0.56, -0.10), segments=12, axis="y"),
        make_beveled_box((0.06, 0.026, 0.03), center=(-0.44, 0.75, 0.24), bevel=0.005),
        make_beveled_box((0.06, 0.026, 0.03), center=(0.12, 0.75, 0.24), bevel=0.005),
    ]
    add_part(sm, "WallDesk02_SignalOrangeLatchesAndTerminals", merge_geometries(orange_all), mats["accent_orange"])

    # 7. Left Bay Widescreen OLED Terminal + Docked & Right-Tower Auxiliary Data-Pads
    add_part(
        sm,
        "WallDesk02_LeftBayOLEDTerminal",
        make_quad_panel((-0.43, 1.06, -0.20), (0.11, 1.06, -0.20), (0.11, 1.48, -0.20), (-0.43, 1.48, -0.20)),
        mats["oled_terminal"],
    )
    aux_slate = make_quad_panel((0.37, 1.42, -0.04), (0.45, 1.42, -0.04), (0.45, 1.62, -0.08), (0.37, 1.62, -0.08))
    add_part(sm, "WallDesk02_DualDatapadScreens", merge_geometries([oled_pad, aux_slate]), mats["oled_datapad"])

    # 8. Practical Lighting: Task Ice-White, Cyan Coaster/Terminal, Right Tower Amber/Cyan
    add_part(sm, "WallDesk02_TaskLightIceWhite", make_beveled_box((0.56, 0.022, 0.04), center=(-0.16, 1.82, -0.02), bevel=0.004), mats["led_ice"])
    add_part(
        sm,
        "WallDesk02_CyanCoasterAndTowerLED",
        merge_geometries([
            cyan_props,
            make_beveled_box((0.24, 0.020, 0.03), center=(0.335, 1.82, 0.02), bevel=0.004),
            make_beveled_box((0.020, 1.66, 0.03), center=(0.43, 0.99, 0.02), bevel=0.004),
        ]),
        mats["led_cyan"],
    )
    add_part(
        sm,
        "WallDesk02_AmberShelfAndToeLED",
        merge_geometries([
            make_beveled_box((0.24, 0.020, 0.03), center=(0.335, 1.32, 0.02), bevel=0.004),
            make_beveled_box((0.24, 0.020, 0.03), center=(0.335, 0.72, 0.02), bevel=0.004),
            make_beveled_box((0.86, 0.020, 0.03), center=(0.0, 0.13, -0.02), bevel=0.004),
        ]),
        mats["led_amber"],
    )

    # 9. Right Tower Full-Height Translucent Door + Left Overhead Glare/HUD Visor (alphaMode: "BLEND")
    visor_canopy = transform_geom(
        make_quad_panel((-0.28, -0.10, 0.0), (0.28, -0.10, 0.0), (0.28, 0.10, 0.0), (-0.28, 0.10, 0.0)),
        translate=(-0.16, 1.62, -0.02),
        rot_xyz_deg=(-24.0, 0.0, 0.0),
    )
    tower_door = make_quad_panel((0.21, 0.16, 0.07), (0.45, 0.16, 0.07), (0.45, 1.84, 0.07), (0.21, 1.84, 0.07))
    add_part(sm, "WallDesk02_TranslucentTowerDoorAndVisor", merge_geometries([tower_door, visor_canopy]), mats["glass_holo"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "walldesk_r1_02.glb"), sm, root_name="WallDeskR1_02_DualTierSplitStation")


# ==============================================================================
# CANDIDATE 03: CANTILEVERED SCISSORS-STRUT DROP DESK & HOLO-VISOR ALCOVE (`walldesk_r1_03.glb`)
# Dimensions: 0.92m W x 0.65m D x 1.92m H
# ==============================================================================
def build_03_scissors_strut_holo_alcove(mats):
    sm = []
    # 1. Stadium-Beveled Aerospace-White & Gunmetal Wall Pod
    gunmetal_frame = [
        make_beveled_box((0.92, 0.12, 0.40), center=(0.0, 0.06, -0.12), bevel=0.03),
        make_beveled_box((0.92, 1.84, 0.08), center=(0.0, 0.96, -0.28), bevel=0.025),
    ]
    add_part(sm, "WallDesk03_GunmetalRearFrame", merge_geometries(gunmetal_frame), mats["gunmetal"])

    white_cradle, slate_kbd, steel_mug, oled_pad, cyan_props = make_desktop_props_kit(desk_cx=0.0, desk_top_y=0.775, desk_cz=0.06)
    white_pod = [
        make_sculpted_cushion((0.92, 0.16, 0.40), center=(0.0, 1.84, -0.10), res=(7, 3, 5), roundness=0.28, belly_puff=0.02, pinch_corners=0.0, crease_freq=0),
        make_beveled_box((0.09, 1.68, 0.36), center=(-0.415, 0.96, -0.12), bevel=0.035),
        make_beveled_box((0.09, 1.68, 0.36), center=(0.415, 0.96, -0.12), bevel=0.035),
        make_beveled_box((0.82, 0.048, 0.44), center=(0.0, 0.75, 0.04), bevel=0.016),
        white_cradle,
    ]
    add_part(sm, "WallDesk03_AerospaceWhiteCapsuleAndLeaf", merge_geometries(white_pod), mats["aero_white"])

    add_part(
        sm,
        "WallDesk03_CarbonSlateDeskSurface",
        merge_geometries([make_beveled_box((0.74, 0.015, 0.36), center=(0.0, 0.77, 0.04), bevel=0.005), slate_kbd]),
        mats["carbon_slate"],
    )

    # 2. External Articulated X-Frame / Scissor-Link Machined-Steel Pantograph Struts on Left & Right
    steel_stool, charcoal_seat, navy_stool, orange_lever = make_articulated_crew_stool(
        stool_x=0.0, seat_y=0.47, stool_z=0.21, style="zero_g_perch"
    )
    scissor_parts = [steel_mug, steel_stool]
    orange_pivots = [orange_lever]
    for sx in [-0.39, 0.39]:
        bar_a = sample_filleted_polyline([(sx, 0.52, -0.20), (sx, 0.75, 0.20)], 0.01, 2)
        bar_b = sample_filleted_polyline([(sx, 0.98, -0.20), (sx, 0.75, 0.02)], 0.01, 2)
        bar_c = sample_filleted_polyline([(sx, 0.64, 0.0), (sx, 0.86, 0.16)], 0.01, 2)
        scissor_parts.extend([
            make_swept_tube(bar_a, radius=0.015, radial_segments=8),
            make_swept_tube(bar_b, radius=0.015, radial_segments=8),
            make_swept_tube(bar_c, radius=0.014, radial_segments=8),
        ])
        for py, pz in [(0.64, 0.0), (0.75, 0.20), (0.86, -0.10)]:
            orange_pivots.append(make_cylinder(0.022, 0.022, 0.035, center=(sx, py, pz), segments=10, axis="x"))

    add_part(sm, "WallDesk03_ScissorPantographStrutsAndStool", merge_geometries(scissor_parts), mats["steel_machined"])
    add_part(sm, "WallDesk03_SignalOrangeScissorPivots", merge_geometries(orange_pivots), mats["accent_orange"])

    # 3. Zero-G Perch Stool Cushions & Acoustic Backwall
    add_part(sm, "WallDesk03_CharcoalPerchSeat", charcoal_seat, mats["pad_charcoal"])
    add_part(
        sm,
        "WallDesk03_NavyKneeBolstersAndBackpad",
        merge_geometries([navy_stool, make_beveled_box((0.72, 0.86, 0.03), center=(0.0, 1.28, -0.23), bevel=0.01)]),
        mats["pad_navy"],
    )

    # 4. Recessed OLED Comms Terminal + Docked Data-Pad
    add_part(
        sm,
        "WallDesk03_OLEDCommsTerminal",
        make_quad_panel((-0.33, 1.06, -0.19), (0.33, 1.06, -0.19), (0.33, 1.48, -0.19), (-0.33, 1.48, -0.19)),
        mats["oled_terminal"],
    )
    add_part(sm, "WallDesk03_DockedDatapadOLED", oled_pad, mats["oled_datapad"])

    # 5. Curved Quarter-Sphere Translucent Cyan HUD Privacy Hood (alphaMode: "BLEND")
    holo_hood = make_curved_canopy_shield(
        width_x=0.76,
        center_x=0.0,
        radius_yz=0.38,
        center_y=1.38,
        center_z=-0.16,
        ang_start_deg=15.0,
        ang_end_deg=85.0,
        segs_arc=10,
    )
    add_part(sm, "WallDesk03_CurvedHoloPrivacyHood", holo_hood, mats["glass_holo"])

    # 6. Practical Lighting
    add_part(sm, "WallDesk03_TaskLightIceWhite", make_beveled_box((0.64, 0.022, 0.04), center=(0.0, 1.72, -0.02), bevel=0.004), mats["led_ice"])
    add_part(
        sm,
        "WallDesk03_CyanCoasterAndHoodRim",
        merge_geometries([cyan_props, make_beveled_box((0.70, 0.022, 0.04), center=(0.0, 1.54, 0.16), bevel=0.004)]),
        mats["led_cyan"],
    )
    add_part(sm, "WallDesk03_AmberFootlightLED", make_beveled_box((0.68, 0.020, 0.03), center=(0.0, 0.13, -0.04), bevel=0.004), mats["led_amber"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "walldesk_r1_03.glb"), sm, root_name="WallDeskR1_03_ScissorsStrutHoloAlcove")


# ==============================================================================
# CANDIDATE 04: SLIDING TRACK BULKHEAD CONSOLE & STOWABLE FLIGHT STOOL (`walldesk_r1_04.glb`)
# Dimensions: 1.00m W x 0.60m D x 1.98m H
# ==============================================================================
def build_04_sliding_track_console(mats):
    sm = []
    # 1. Vertical Track Bulkhead Frame & Overhead Locker Housing (Y = 1.56 to 1.98)
    frame = [
        make_beveled_box((1.00, 0.12, 0.40), center=(0.0, 0.06, -0.10), bevel=0.025),
        make_beveled_box((1.00, 1.88, 0.07), center=(0.0, 0.98, -0.27), bevel=0.02),
        make_beveled_box((1.00, 0.40, 0.38), center=(0.0, 1.78, -0.10), bevel=0.03),
    ]
    add_part(sm, "WallDesk04_CarbonSlateTrackFrame", merge_geometries(frame), mats["carbon_slate"])

    # 2. Twin Prominent Vertical Machined-Steel Linear Guide Rails (X = ±0.42m, Y = 0.12..1.88m) + Struts + Stool
    steel_stool, charcoal_seat, navy_stool, orange_lever = make_articulated_crew_stool(
        stool_x=0.0, seat_y=0.47, stool_z=0.20, style="turret"
    )
    white_cradle, slate_kbd, steel_mug, oled_pad, cyan_props = make_desktop_props_kit(desk_cx=0.0, desk_top_y=0.775, desk_cz=0.06)

    rail_parts = [
        make_cylinder(0.026, 0.026, 1.74, center=(-0.42, 0.98, -0.16), segments=12, axis="y"),
        make_cylinder(0.026, 0.026, 1.74, center=(0.42, 0.98, -0.16), segments=12, axis="y"),
        # Linear bearing carriages on the rails at Y = 0.75m
        make_beveled_box((0.08, 0.14, 0.10), center=(-0.42, 0.75, -0.15), bevel=0.012),
        make_beveled_box((0.08, 0.14, 0.10), center=(0.42, 0.75, -0.15), bevel=0.012),
        # Diagonal cantilever support arms from bearing carriages to front of desk leaf
        make_swept_tube(sample_filleted_polyline([(-0.40, 0.52, -0.16), (-0.40, 0.74, 0.20)], 0.02, 3), radius=0.016, radial_segments=10),
        make_swept_tube(sample_filleted_polyline([(0.40, 0.52, -0.16), (0.40, 0.74, 0.20)], 0.02, 3), radius=0.016, radial_segments=10),
        steel_mug,
        steel_stool,
    ]
    add_part(sm, "WallDesk04_TwinLinearGuideRailsAndStool", merge_geometries(rail_parts), mats["steel_machined"])

    # 3. Height-Adjustable Cantilevered Aerospace-White Desk Leaf + Stowed Binders/Power Packs in Upper Locker
    white_parts = [
        make_beveled_box((0.86, 0.048, 0.44), center=(0.0, 0.75, 0.04), bevel=0.016),
        white_cradle,
        # Stowed binders & spare power packs inside overhead cabinet (Y = 1.62..1.86)
        make_beveled_box((0.05, 0.22, 0.20), center=(-0.28, 1.74, -0.08), bevel=0.008),
        make_beveled_box((0.05, 0.22, 0.20), center=(-0.20, 1.74, -0.08), bevel=0.008),
        make_beveled_box((0.05, 0.22, 0.20), center=(-0.12, 1.74, -0.08), bevel=0.008),
        make_cylinder(0.05, 0.05, 0.20, center=(0.18, 1.72, -0.08), segments=12, axis="y"),
        make_cylinder(0.05, 0.05, 0.20, center=(0.30, 1.72, -0.08), segments=12, axis="y"),
    ]
    add_part(sm, "WallDesk04_AdjustableWhiteDeskAndStowedKit", merge_geometries(white_parts), mats["aero_white"])

    # 4. Signal-Orange Rail-Lock Levers & Power Pack Collars
    orange_all = [
        orange_lever,
        make_beveled_box((0.06, 0.09, 0.05), center=(-0.44, 0.75, -0.10), bevel=0.008),
        make_beveled_box((0.06, 0.09, 0.05), center=(0.44, 0.75, -0.10), bevel=0.008),
        make_cylinder(0.054, 0.054, 0.03, center=(0.18, 1.82, -0.08), segments=12, axis="y"),
        make_cylinder(0.054, 0.054, 0.03, center=(0.30, 1.82, -0.08), segments=12, axis="y"),
    ]
    add_part(sm, "WallDesk04_SignalOrangeRailLocks", merge_geometries(orange_all), mats["accent_orange"])

    # 5. Stool Cushions & Desk Inlay
    add_part(sm, "WallDesk04_CharcoalStoolCushion", merge_geometries([charcoal_seat, slate_kbd]), mats["pad_charcoal"])
    add_part(
        sm,
        "WallDesk04_NavyBackwallPad",
        merge_geometries([navy_stool, make_sculpted_cushion((0.76, 0.78, 0.04), center=(0.0, 1.18, -0.22), res=(6, 5, 2), roundness=0.22, belly_puff=0.03, tuft_grid=(3, 2), tuft_depth=0.012, crease_freq=0)]),
        mats["pad_navy"],
    )

    # 6. Main OLED Cabin Terminal + Angled Side Telemetry Wings + Docked Data-Pad
    add_part(
        sm,
        "WallDesk04_MainOLEDTerminal",
        make_quad_panel((-0.34, 1.04, -0.18), (0.34, 1.04, -0.18), (0.34, 1.46, -0.18), (-0.34, 1.46, -0.18)),
        mats["oled_terminal"],
    )
    add_part(sm, "WallDesk04_DockedDatapadOLED", oled_pad, mats["oled_datapad"])

    # 7. Practical Lighting & Overhead Translucent Glass Storage Cabinet Door (alphaMode: "BLEND")
    add_part(sm, "WallDesk04_TaskLightIceWhite", make_beveled_box((0.76, 0.022, 0.04), center=(0.0, 1.56, 0.02), bevel=0.004), mats["led_ice"])
    add_part(
        sm,
        "WallDesk04_CyanCoasterAndRailLED",
        merge_geometries([
            cyan_props,
            make_beveled_box((0.78, 0.022, 0.04), center=(0.0, 1.92, 0.04), bevel=0.004),
        ]),
        mats["led_cyan"],
    )
    add_part(sm, "WallDesk04_AmberBaseLED", make_beveled_box((0.76, 0.020, 0.03), center=(0.0, 0.13, -0.02), bevel=0.004), mats["led_amber"])

    add_part(
        sm,
        "WallDesk04_OverheadTranslucentCabinetDoor",
        make_quad_panel((-0.42, 1.60, 0.08), (0.42, 1.60, 0.08), (0.42, 1.92, 0.08), (-0.42, 1.92, 0.08)),
        mats["glass_holo"],
    )

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "walldesk_r1_04.glb"), sm, root_name="WallDeskR1_04_SlidingTrackConsole")


# ==============================================================================
# CANDIDATE 05: CORNER-CHAMFERED COCKPIT CABIN TERMINAL & PIVOTING PERCH (`walldesk_r1_05.glb`)
# Dimensions: 1.08m W x 0.68m D x 2.00m H
# ==============================================================================
def build_05_corner_cockpit_terminal(mats):
    sm = []
    # 1. 45°-Chamfered Cockpit-Style Wrap-Around Gunmetal Bulkhead Enclosure
    cockpit_hull = [
        make_beveled_box((1.08, 0.14, 0.44), center=(0.0, 0.07, -0.10), bevel=0.03),
        make_beveled_box((1.08, 0.15, 0.44), center=(0.0, 1.925, -0.10), bevel=0.03),
        make_beveled_box((0.72, 1.84, 0.07), center=(0.0, 0.99, -0.28), bevel=0.02),
        # Left & Right 30°-canted cockpit wing walls
        transform_geom(
            make_beveled_box((0.26, 1.78, 0.36), center=(0.0, 0.0, 0.0), bevel=0.025),
            translate=(-0.35, 0.99, -0.10),
            rot_xyz_deg=(0.0, 28.0, 0.0),
        ),
        transform_geom(
            make_beveled_box((0.26, 1.78, 0.36), center=(0.0, 0.0, 0.0), bevel=0.025),
            translate=(0.35, 0.99, -0.10),
            rot_xyz_deg=(0.0, -28.0, 0.0),
        ),
    ]
    add_part(sm, "WallDesk05_CockpitGunmetalEnclosure", merge_geometries(cockpit_hull), mats["gunmetal"])

    # 2. Wide Trapezoidal Aerospace-White Fold-Down Desk Leaf (Y = 0.75m)
    white_cradle, slate_kbd, steel_mug, oled_pad, cyan_props = make_desktop_props_kit(desk_cx=0.0, desk_top_y=0.775, desk_cz=0.07)
    white_parts = [
        make_beveled_box((0.88, 0.048, 0.46), center=(0.0, 0.75, 0.05), bevel=0.016),
        white_cradle,
    ]
    add_part(sm, "WallDesk05_TrapezoidalWhiteDeskLeaf", merge_geometries(white_parts), mats["aero_white"])

    # 3. Twin Heavy Hydraulic Rams, Turret-Mounted Pivoting Crew Stool & Thermal Mug
    steel_stool, charcoal_seat, navy_stool, orange_lever = make_articulated_crew_stool(
        stool_x=0.0, seat_y=0.47, stool_z=0.22, style="turret"
    )
    ram_l = sample_filleted_polyline([(-0.36, 0.44, -0.18), (-0.36, 0.74, 0.20)], 0.02, 3)
    ram_r = sample_filleted_polyline([(0.36, 0.44, -0.18), (0.36, 0.74, 0.20)], 0.02, 3)
    steel_all = [
        make_swept_tube(ram_l, radius=0.020, radial_segments=10),
        make_swept_tube(ram_r, radius=0.020, radial_segments=10),
        make_chamfered_aperture_ring(0.68, 1.76, center_y=0.99, z_pos=-0.04, tube_r=0.026, chamfer=0.14),
        steel_mug,
        steel_stool,
    ]
    add_part(sm, "WallDesk05_HydraulicRamsTurretStoolAndMug", merge_geometries(steel_all), mats["steel_machined"])

    # 4. Padded Charcoal Wrist Bolster, Stool Seat & Signal-Orange Ram Collars
    charcoal_all = [
        charcoal_seat,
        slate_kbd,
        make_sculpted_cushion((0.76, 0.032, 0.06), center=(0.0, 0.77, 0.24), res=(6, 2, 3), roundness=0.35, belly_puff=0.03, crease_freq=0),
    ]
    add_part(sm, "WallDesk05_CharcoalStoolAndWristBolster", merge_geometries(charcoal_all), mats["pad_charcoal"])
    add_part(sm, "WallDesk05_NavyStoolBackrest", merge_geometries([navy_stool, make_sculpted_cushion((0.64, 0.82, 0.04), center=(0.0, 1.24, -0.24), res=(6, 5, 2), roundness=0.22, belly_puff=0.03, tuft_grid=(3, 2), tuft_depth=0.012, crease_freq=0)]), mats["pad_navy"])

    orange_all = [
        orange_lever,
        make_cylinder(0.026, 0.026, 0.05, center=(-0.36, 0.59, 0.01), segments=10, axis="y"),
        make_cylinder(0.026, 0.026, 0.05, center=(0.36, 0.59, 0.01), segments=10, axis="y"),
    ]
    add_part(sm, "WallDesk05_SignalOrangeRamCollars", merge_geometries(orange_all), mats["accent_orange"])

    # 5. 3-Panel Panoramic Display Array (Center OLED Terminal + Twin 30°-Angled Wing Monitors + Docked Data-Pad)
    add_part(
        sm,
        "WallDesk05_CenterWidescreenOLED",
        make_quad_panel((-0.28, 1.06, -0.22), (0.28, 1.06, -0.22), (0.28, 1.48, -0.22), (-0.28, 1.48, -0.22)),
        mats["oled_terminal"],
    )
    left_wing_mon = transform_geom(
        make_quad_panel((-0.11, -0.20, 0.0), (0.11, -0.20, 0.0), (0.11, 0.20, 0.0), (-0.11, 0.20, 0.0)),
        translate=(-0.36, 1.27, -0.06),
        rot_xyz_deg=(0.0, 28.0, 0.0),
    )
    right_wing_mon = transform_geom(
        make_quad_panel((-0.11, -0.20, 0.0), (0.11, -0.20, 0.0), (0.11, 0.20, 0.0), (-0.11, 0.20, 0.0)),
        translate=(0.36, 1.27, -0.06),
        rot_xyz_deg=(0.0, -28.0, 0.0),
    )
    add_part(sm, "WallDesk05_WingMonitorsAndDatapad", merge_geometries([left_wing_mon, right_wing_mon, oled_pad]), mats["oled_datapad"])

    # 6. Practical Lighting & Angled Translucent HUD Combiner Visor (alphaMode: "BLEND")
    add_part(sm, "WallDesk05_TaskLightIceWhite", make_beveled_box((0.62, 0.022, 0.04), center=(0.0, 1.80, -0.02), bevel=0.004), mats["led_ice"])
    add_part(
        sm,
        "WallDesk05_CyanCoasterAndCrownLED",
        merge_geometries([cyan_props, make_beveled_box((0.64, 0.022, 0.04), center=(0.0, 1.86, 0.04), bevel=0.004)]),
        mats["led_cyan"],
    )
    add_part(sm, "WallDesk05_AmberToeKickLED", make_beveled_box((0.64, 0.020, 0.03), center=(0.0, 0.14, 0.06), bevel=0.004), mats["led_amber"])

    hud_visor = transform_geom(
        make_quad_panel((-0.34, -0.15, 0.0), (0.34, -0.15, 0.0), (0.34, 0.15, 0.0), (-0.34, 0.15, 0.0)),
        translate=(0.0, 1.60, 0.02),
        rot_xyz_deg=(-22.0, 0.0, 0.0),
    )
    add_part(sm, "WallDesk05_CockpitHoloHUDVisor", hud_visor, mats["glass_holo"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "walldesk_r1_05.glb"), sm, root_name="WallDeskR1_05_CornerCockpitTerminal")


def build_all_walldesk_round1():
    mats = get_walldesk_materials()
    builders = [
        build_01_octagonal_fold_down_desk,
        build_02_dual_tier_split_station,
        build_03_scissors_strut_holo_alcove,
        build_04_sliding_track_console,
        build_05_corner_cockpit_terminal,
    ]
    results = []
    for fn in builders:
        info = fn(mats)
        fname = os.path.basename(info["filepath"])
        dims = info["dimensions"]
        print(
            f"[walldesk_r1] Built {fname:18s} | {dims[0]:.2f}m W x {dims[2]:.2f}m D x {dims[1]:.2f}m H | "
            f"verts={info['vertices']:4d} | tris={info['triangles']:4d} | min_y={info['min'][1]:.5f}"
        )
        results.append(info)
    with open(os.path.join(OUT_GLB_DIR, "walldesk_r1_manifest.json"), "w") as f:
        json.dump(results, f, indent=2)
    return results


if __name__ == "__main__":
    build_all_walldesk_round1()
