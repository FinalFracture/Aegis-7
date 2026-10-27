#!/usr/bin/env python3
"""
Builds all 5 Round-1 Hard Sci-Fi Room 02 Hero Fixture (Pressurized Bulkhead Airlock Hatch & Sector Checkpoint)
.glb models:
  /workspace/game-project/assets/glb/corridor_round1/corridor_door_r1_01.glb .. corridor_door_r1_05.glb
AND builds the Aegis-7 Room 01 & Room 02 architectural shell .glb models:
  /workspace/game-project/assets/glb/rooms/room_01_shell.glb
  /workspace/game-project/assets/glb/rooms/room_02_shell.glb
  /workspace/game-project/assets/glb/rooms/room_02_corridor_shell.glb
  /workspace/game-project/assets/glb/room_02_corridor_shell.glb

Follows /workspace/game-project/design/corridor_round1/corridor_door_r1_spec.md ("Aegis-7 Standard"):
- Bottom-center (0.0, 0.0, 0.0) floor pivot (min_y == 0.0000, centered X and Z), front checkpoint side facing +Z
- Polygon budget: 3,000 - 5,800 triangles per candidate
- Mapped cleanly to Sloane's 11 textures in /workspace/game-project/assets/textures/corridor_round1/
- Mandatory 4-Part 3D Airlock & Checkpoint Kit in every candidate:
  1. 45° Chamfered Octagonal Pressure Coaming & Raised Threshold Sill (Y = 0.0m-0.12m) with amber warning chevrons
  2. Partially Parted Blast-Door Leaves (0.38m-0.46m Center Gap) with Interlocking 3D Dog-Ear Locking Teeth
  3. Translucent Armored Inspection Windows (glass_airlock_viewport_translucent.png, alphaMode: "BLEND", alpha ~ 0.19)
     with true open cutouts through the door leaves (and side emergency locker doors)
  4. Sector Access OLED Terminal (oled_airlock_status.png), Signal-Orange Manual Override Wheel & Cycling Beacons
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

TEX_CORRIDOR_DIR = "/workspace/game-project/assets/textures/corridor_round1"
OUT_GLB_DIR = "/workspace/game-project/assets/glb/corridor_round1"
ROOMS_GLB_DIR = "/workspace/game-project/assets/glb/rooms"
os.makedirs(OUT_GLB_DIR, exist_ok=True)
os.makedirs(ROOMS_GLB_DIR, exist_ok=True)


def tex_cr(fname: str) -> str:
    return os.path.join(TEX_CORRIDOR_DIR, fname)


def get_corridor_materials():
    return {
        "gunmetal": PBRMaterialDef(
            name="Mat_Titanium_GunmetalHull",
            base_color=hex_rgba("#1A1E24"),
            metallic=0.78,
            roughness=0.34,
            texture_path=tex_cr("titanium_gunmetal_hull.png"),
        ),
        "aero_white": PBRMaterialDef(
            name="Mat_Composite_AerospaceWhite",
            base_color=hex_rgba("#D8DEE6"),
            metallic=0.08,
            roughness=0.28,
            texture_path=tex_cr("composite_aerospace_white.png"),
        ),
        "carbon_slate": PBRMaterialDef(
            name="Mat_Carbon_SlateFrame",
            base_color=hex_rgba("#282E38"),
            metallic=0.58,
            roughness=0.40,
            texture_path=tex_cr("carbon_slate_frame.png"),
        ),
        "steel_machined": PBRMaterialDef(
            name="Mat_Steel_MachinedGantry",
            base_color=hex_rgba("#88929E"),
            metallic=0.90,
            roughness=0.22,
            texture_path=tex_cr("steel_machined_gantry.png"),
        ),
        "pad_charcoal": PBRMaterialDef(
            name="Mat_Fabric_CharcoalFlightpad",
            base_color=hex_rgba("#242932"),
            metallic=0.02,
            roughness=0.78,
            texture_path=tex_cr("fabric_charcoal_flightpad.png"),
        ),
        "pad_navy": PBRMaterialDef(
            name="Mat_Fabric_OrbitalNavyPad",
            base_color=hex_rgba("#1D2C3C"),
            metallic=0.02,
            roughness=0.76,
            texture_path=tex_cr("fabric_orbital_navy_pad.png"),
        ),
        "accent_orange": PBRMaterialDef(
            name="Mat_Accent_SignalOrange",
            base_color=hex_rgba("#D95B26"),
            metallic=0.06,
            roughness=0.48,
            texture_path=tex_cr("accent_signal_orange.png"),
        ),
        "oled_status": PBRMaterialDef(
            name="Mat_OLED_AirlockStatus",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.10,
            roughness=0.14,
            emissive=(0.35, 0.90, 1.0),
            texture_path=tex_cr("oled_airlock_status.png"),
        ),
        "glass_viewport": PBRMaterialDef(
            name="Mat_Glass_AirlockViewport_Translucent",
            base_color=(0.55, 0.88, 1.0, 0.19),
            metallic=0.10,
            roughness=0.08,
            emissive=(0.0, 0.14, 0.22),
            texture_path=tex_cr("glass_airlock_viewport_translucent.png"),
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
        "led_amber": PBRMaterialDef(
            name="Mat_Emissive_AmberLED",
            base_color=hex_rgba("#FF9500"),
            metallic=0.0,
            roughness=0.15,
            emissive=(1.0, 0.58, 0.0),
        ),
        "led_uv": PBRMaterialDef(
            name="Mat_Emissive_UVDeconLED",
            base_color=hex_rgba("#7B5CFF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.55, 0.38, 1.0),
        ),
    }


# ==============================================================================
# SHARED 4-PART 3D AIRLOCK & CHECKPOINT KIT HELPERS
# ==============================================================================

def make_portal_oct_ring(width_x: float, height_y: float, center_y: float, z_pos: float, tube_r: float = 0.028, chamfer: float = 0.18):
    hx = width_x * 0.5
    hy = height_y * 0.5
    c = min(chamfer, hx * 0.45, hy * 0.45)
    corners = [
        (hx - c, center_y - hy),
        (hx, center_y - hy + c),
        (hx, center_y + hy - c),
        (hx - c, center_y + hy),
        (-hx + c, center_y + hy),
        (-hx, center_y + hy - c),
        (-hx, center_y - hy + c),
        (-hx + c, center_y - hy),
        (hx - c, center_y - hy),
    ]
    pts_3d = sample_filleted_polyline([(x, y, z_pos) for x, y in corners], fillet_radius=0.03, corner_subdivs=2)
    return make_swept_tube(pts_3d, radius=tube_r, radial_segments=8, closed_loop=True, oval_scale=(1.0, 1.5))


def make_parted_door_leaf_with_window_and_teeth(
    leaf_cx: float,
    leaf_w: float = 0.62,
    y_bot: float = 0.12,
    y_top: float = 2.34,
    z_pos: float = 0.0,
    thick_z: float = 0.12,
    win_w: float = 0.30,
    win_h: float = 0.84,
    win_cy: float = 1.44,
    inner_edge_sign: float = 1.0,  # +1 if inner meeting edge is on +X side of leaf (left door), -1 for right door
    num_teeth: int = 3,
):
    """
    Builds a heavy aerospace-white & carbon-slate blast-door leaf with:
    - True open window cutout (zero opaque polygons inside window aperture)
    - Machined-steel window bezel & 3D interlocking trapezoidal dog-latch teeth along the meeting edge
    - Translucent armored viewport pane (alphaMode: "BLEND")
    Returns: (white_door_body_geom, slate_armor_ribs_geom, steel_teeth_and_bezel_geom, glass_window_geom)
    """
    leaf_h = y_top - y_bot
    wy0 = win_cy - win_h * 0.5
    wy1 = win_cy + win_h * 0.5

    bot_h = max(0.10, wy0 - y_bot)
    top_h = max(0.10, y_top - wy1)
    pillar_w = max(0.08, (leaf_w - win_w) * 0.5)
    pillar_x_off = win_w * 0.5 + pillar_w * 0.5

    white_parts = [
        # Lower door section below window
        make_beveled_box((leaf_w, bot_h, thick_z), center=(leaf_cx, y_bot + bot_h * 0.5, z_pos), bevel=0.02),
        # Upper door section above window
        make_beveled_box((leaf_w, top_h, thick_z), center=(leaf_cx, wy1 + top_h * 0.5, z_pos), bevel=0.02),
        # Outer & inner vertical stiles flanking window cutout
        make_beveled_box((pillar_w, win_h + 0.04, thick_z), center=(leaf_cx - pillar_x_off, win_cy, z_pos), bevel=0.02),
        make_beveled_box((pillar_w, win_h + 0.04, thick_z), center=(leaf_cx + pillar_x_off, win_cy, z_pos), bevel=0.02),
    ]

    # Carbon-slate horizontal armor reinforcement ribs across lower & upper door leaf
    slate_ribs = [
        make_beveled_box((leaf_w * 0.88, 0.08, thick_z + 0.03), center=(leaf_cx, y_bot + bot_h * 0.38, z_pos), bevel=0.012),
        make_beveled_box((leaf_w * 0.88, 0.08, thick_z + 0.03), center=(leaf_cx, y_bot + bot_h * 0.72, z_pos), bevel=0.012),
        make_beveled_box((leaf_w * 0.88, 0.07, thick_z + 0.03), center=(leaf_cx, wy1 + top_h * 0.50, z_pos), bevel=0.012),
    ]

    # Machined-steel window bezel + 3D interlocking dog-ear locking teeth protruding into the center gap
    steel_parts = [
        make_portal_oct_ring(win_w + 0.05, win_h + 0.05, center_y=win_cy, z_pos=z_pos + thick_z * 0.52, tube_r=0.018, chamfer=0.07),
        make_portal_oct_ring(win_w + 0.05, win_h + 0.05, center_y=win_cy, z_pos=z_pos - thick_z * 0.52, tube_r=0.018, chamfer=0.07),
    ]
    for b_elem in steel_parts[:2]:
        b_elem[0][:, 0] += leaf_cx

    inner_edge_x = leaf_cx + inner_edge_sign * (leaf_w * 0.5)
    # Offset left and right door teeth slightly in Y so they visibly interlock when doors close
    y_phase = 0.06 if inner_edge_sign > 0 else -0.06
    for k in range(num_teeth):
        ty = y_bot + 0.36 + k * ((leaf_h - 0.72) / max(1, num_teeth - 1)) + y_phase
        tx = inner_edge_x + inner_edge_sign * 0.045
        steel_parts.append(make_beveled_box((0.11, 0.14, thick_z * 0.78), center=(tx, ty, z_pos), bevel=0.018))

    glass_pane = make_quad_panel(
        (leaf_cx - win_w * 0.5, wy0, z_pos),
        (leaf_cx + win_w * 0.5, wy0, z_pos),
        (leaf_cx + win_w * 0.5, wy1, z_pos),
        (leaf_cx - win_w * 0.5, wy1, z_pos),
    )

    return (
        merge_geometries(white_parts),
        merge_geometries(slate_ribs),
        merge_geometries(steel_parts),
        glass_pane,
    )


def make_rotary_override_handwheel(cx: float, cy: float, cz: float, radius: float = 0.12):
    """Builds a sculpted 4-spoke signal-orange rotary manual pressure-equalization handwheel + steel hub."""
    wheel_pts = []
    for k in range(17):
        ang = (k / 16.0) * 2.0 * math.pi
        wheel_pts.append([cx + radius * math.cos(ang), cy + radius * math.sin(ang), cz])
    orange_wheel = [
        make_swept_tube(np.array(wheel_pts, dtype=np.float32), radius=0.016, radial_segments=10, closed_loop=True),
        make_beveled_box((radius * 1.9, 0.022, 0.022), center=(cx, cy, cz), bevel=0.004),
        make_beveled_box((0.022, radius * 1.9, 0.022), center=(cx, cy, cz), bevel=0.004),
    ]
    steel_hub = make_cylinder(0.038, 0.032, 0.05, center=(cx, cy, cz - 0.015), segments=12, axis="z")
    return merge_geometries(orange_wheel), steel_hub


def make_octagonal_portal_coaming(
    portal_cx: float = 0.0,
    outer_w: float = 2.45,
    outer_h: float = 2.75,
    depth_z: float = 0.62,
    open_w: float = 1.68,
    open_h: float = 2.24,
    sill_h: float = 0.12,
):
    """
    Builds Part 1: Massive 45° Chamfered Octagonal Pressure Coaming & Ramped Machined-Steel Threshold Sill.
    Returns: (gunmetal_coaming_geom, charcoal_seal_geom, steel_sill_and_rings_geom, amber_chevrons_geom, cyan_arch_geom)
    """
    pillar_w = (outer_w - open_w) * 0.5
    header_h = outer_h - sill_h - open_h
    px_off = open_w * 0.5 + pillar_w * 0.5

    coaming = [
        # Left & Right structural bulkhead piers
        make_beveled_box((pillar_w, outer_h, depth_z), center=(portal_cx - px_off, outer_h * 0.5, 0.0), bevel=0.045),
        make_beveled_box((pillar_w, outer_h, depth_z), center=(portal_cx + px_off, outer_h * 0.5, 0.0), bevel=0.045),
        # Upper pressure header
        make_beveled_box((outer_w, header_h, depth_z), center=(portal_cx, sill_h + open_h + header_h * 0.5, 0.0), bevel=0.045),
        # Lower threshold base
        make_beveled_box((outer_w, sill_h, depth_z), center=(portal_cx, sill_h * 0.5, 0.0), bevel=0.025),
        # 45° upper corner chamfer gussets inside the aperture
        transform_geom(
            make_beveled_box((0.36, 0.14, depth_z * 0.92), center=(0.0, 0.0, 0.0), bevel=0.02),
            translate=(portal_cx - open_w * 0.5 + 0.10, sill_h + open_h - 0.10, 0.0),
            rot_xyz_deg=(0.0, 0.0, 45.0),
        ),
        transform_geom(
            make_beveled_box((0.36, 0.14, depth_z * 0.92), center=(0.0, 0.0, 0.0), bevel=0.02),
            translate=(portal_cx + open_w * 0.5 - 0.10, sill_h + open_h - 0.10, 0.0),
            rot_xyz_deg=(0.0, 0.0, -45.0),
        ),
    ]

    # Inflatable charcoal bladder seal lining the inner octagonal frame
    seal_ring = make_portal_oct_ring(open_w + 0.04, open_h + 0.04, center_y=sill_h + open_h * 0.5, z_pos=0.0, tube_r=0.032, chamfer=0.22)
    seal_ring[0][:, 0] += portal_cx

    # Ramped machined-steel threshold sill + front/rear octagonal pressure bezels
    f_ring = make_portal_oct_ring(open_w + 0.14, open_h + 0.14, center_y=sill_h + open_h * 0.5, z_pos=depth_z * 0.48, tube_r=0.036, chamfer=0.26)
    r_ring = make_portal_oct_ring(open_w + 0.14, open_h + 0.14, center_y=sill_h + open_h * 0.5, z_pos=-depth_z * 0.48, tube_r=0.036, chamfer=0.26)
    f_ring[0][:, 0] += portal_cx
    r_ring[0][:, 0] += portal_cx

    steel_sill = [
        f_ring,
        r_ring,
        make_beveled_box((open_w + 0.24, 0.035, depth_z + 0.08), center=(portal_cx, sill_h + 0.015, 0.0), bevel=0.01),
    ]

    # Recessed Amber threshold warning strips & overhead cycling beacon
    amber_parts = [
        make_beveled_box((open_w * 0.86, 0.022, 0.04), center=(portal_cx, 0.06, depth_z * 0.50), bevel=0.004),
        make_beveled_box((open_w * 0.52, 0.035, 0.06), center=(portal_cx, outer_h - 0.14, depth_z * 0.50), bevel=0.006),
    ]
    cyan_parts = [
        make_beveled_box((open_w * 0.82, 0.028, 0.06), center=(portal_cx, sill_h + open_h + 0.08, depth_z * 0.48), bevel=0.005),
    ]

    return (
        merge_geometries(coaming),
        seal_ring,
        merge_geometries(steel_sill),
        merge_geometries(amber_parts),
        merge_geometries(cyan_parts),
    )


# ==============================================================================
# CANDIDATE 01: AEGIS-7 OCTAGONAL BI-PARTING BLAST HATCH & CHECKPOINT (`corridor_door_r1_01.glb`)
# Dimensions: 2.45m W x 0.62m D x 2.75m H
# ==============================================================================
def build_01_octagonal_biparting_hatch(mats):
    sm = []
    # 1. Symmetrical 45° Chamfered Octagonal Pressure Coaming & Threshold Sill
    coaming, seal, steel_sill, amber_led, cyan_led = make_octagonal_portal_coaming(
        portal_cx=0.0, outer_w=2.45, outer_h=2.75, depth_z=0.62, open_w=1.68, open_h=2.22, sill_h=0.12
    )
    add_part(sm, "Corridor01_OctagonalGunmetalCoaming", coaming, mats["gunmetal"])
    add_part(sm, "Corridor01_CharcoalBladderSeal", seal, mats["pad_charcoal"])

    # 2. Left & Right Bi-Parting Blast-Door Leaves Parted Open by 0.42m in Center (X = -0.84..-0.21 and +0.21..+0.84)
    w_l, s_l, st_l, g_l = make_parted_door_leaf_with_window_and_teeth(
        leaf_cx=-0.525, leaf_w=0.63, y_bot=0.13, y_top=2.33, z_pos=0.0, thick_z=0.12, win_w=0.30, win_h=0.88, win_cy=1.42, inner_edge_sign=1.0, num_teeth=3
    )
    w_r, s_r, st_r, g_r = make_parted_door_leaf_with_window_and_teeth(
        leaf_cx=0.525, leaf_w=0.63, y_bot=0.13, y_top=2.33, z_pos=0.0, thick_z=0.12, win_w=0.30, win_h=0.88, win_cy=1.42, inner_edge_sign=-1.0, num_teeth=3
    )
    add_part(sm, "Corridor01_WhiteBlastDoorLeaves", merge_geometries([w_l, w_r]), mats["aero_white"])
    add_part(sm, "Corridor01_CarbonSlateDoorArmorRibs", merge_geometries([s_l, s_r]), mats["carbon_slate"])

    # 3. Overhead Exposed Machined-Steel Linear Actuator Gantry + Interlocking Dog Teeth + Rotary Wheel
    wheel_or, wheel_st = make_rotary_override_handwheel(cx=-1.02, cy=1.18, cz=0.33, radius=0.12)
    gantry = [
        steel_sill,
        st_l,
        st_r,
        wheel_st,
        make_cylinder(0.028, 0.028, 1.88, center=(0.0, 2.52, 0.30), segments=12, axis="x"),
        make_cylinder(0.042, 0.042, 0.34, center=(-0.48, 2.52, 0.30), segments=12, axis="x"),
        make_cylinder(0.042, 0.042, 0.34, center=(0.48, 2.52, 0.30), segments=12, axis="x"),
    ]
    add_part(sm, "Corridor01_MachinedGantryAndDogTeeth", merge_geometries(gantry), mats["steel_machined"])
    add_part(sm, "Corridor01_SignalOrangeOverrideWheel", wheel_or, mats["accent_orange"])

    # 4. Right Bulkhead Pier OLED Checkpoint Terminal + Cycling Beacons + Translucent Door Windows
    add_part(
        sm,
        "Corridor01_RightPierOLEDStatus",
        make_quad_panel((0.88, 1.18, 0.315), (1.16, 1.18, 0.315), (1.16, 1.62, 0.315), (0.88, 1.62, 0.315)),
        mats["oled_status"],
    )
    add_part(sm, "Corridor01_AmberThresholdAndBeaconLED", amber_led, mats["led_amber"])
    add_part(sm, "Corridor01_CyanArchLED", cyan_led, mats["led_cyan"])
    add_part(sm, "Corridor01_TranslucentDoorViewports", merge_geometries([g_l, g_r]), mats["glass_viewport"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "corridor_door_r1_01.glb"), sm, root_name="CorridorDoorR1_01_OctagonalBiPartingHatch")


# ==============================================================================
# CANDIDATE 02: DUAL-ZONE AIRLOCK PORTAL & EMERGENCY O2/EXTINGUISHER SIDE BAY (`corridor_door_r1_02.glb`)
# Dimensions: 2.60m W x 0.65m D x 2.75m H (Direct Split-Bay Sibling to All Locked Winners!)
# ==============================================================================
def build_02_dual_zone_airlock_sidebay(mats):
    sm = []
    # 1. Asymmetric 68% / 32% Split-Bay Sector Bulkhead Portal
    # Left Bay (X = -1.30 to +0.48, 1.78m wide, centered at X = -0.41): Full-height Octagonal Bi-Parting Blast Hatch
    # Right Bay (X = +0.48 to +1.30, 0.82m wide, centered at X = +0.89): Sector Checkpoint & Damage-Control Station
    coaming, seal, steel_sill, amber_led, cyan_led = make_octagonal_portal_coaming(
        portal_cx=-0.41, outer_w=1.78, outer_h=2.75, depth_z=0.65, open_w=1.32, open_h=2.22, sill_h=0.12
    )
    right_bay_hull = [
        coaming,
        make_beveled_box((0.82, 0.14, 0.65), center=(0.89, 0.07, 0.0), bevel=0.025),
        make_beveled_box((0.82, 0.22, 0.65), center=(0.89, 2.64, 0.0), bevel=0.03),
        make_beveled_box((0.12, 2.52, 0.65), center=(1.24, 1.32, 0.0), bevel=0.03),
        make_beveled_box((0.76, 2.52, 0.12), center=(0.89, 1.32, -0.26), bevel=0.02),
        # Horizontal divider between Upper Checkpoint Console (Y = 1.16..2.52) and Lower Emergency Locker (Y = 0.14..1.16)
        make_beveled_box((0.72, 0.05, 0.58), center=(0.89, 1.16, -0.02), bevel=0.012),
    ]
    add_part(sm, "Corridor02_SplitBayGunmetalPortal", merge_geometries(right_bay_hull), mats["gunmetal"])
    add_part(sm, "Corridor02_CharcoalBladderSeal", seal, mats["pad_charcoal"])

    # 2. Left Bay Bi-Parting Blast Doors Parted Open by 0.42m around X = -0.41
    # Left leaf: X in [-1.07, -0.62] (cx = -0.845, w = 0.45); Right leaf: X in [-0.20, +0.25] (cx = +0.025, w = 0.45)
    w_l, s_l, st_l, g_l = make_parted_door_leaf_with_window_and_teeth(
        leaf_cx=-0.845, leaf_w=0.45, y_bot=0.13, y_top=2.33, z_pos=0.0, thick_z=0.12, win_w=0.22, win_h=0.86, win_cy=1.42, inner_edge_sign=1.0, num_teeth=3
    )
    w_r, s_r, st_r, g_r = make_parted_door_leaf_with_window_and_teeth(
        leaf_cx=0.025, leaf_w=0.45, y_bot=0.13, y_top=2.33, z_pos=0.0, thick_z=0.12, win_w=0.22, win_h=0.86, win_cy=1.42, inner_edge_sign=-1.0, num_teeth=3
    )

    # 3. Right Bay Stowed Damage-Control Kit: Two 3D Cylindrical Fire Extinguishers + Trauma Pack + White Liner
    extinguishers_and_liner = [
        w_l,
        w_r,
        make_beveled_box((0.64, 0.98, 0.03), center=(0.89, 0.65, -0.18), bevel=0.01),
        make_cylinder(0.068, 0.068, 0.52, center=(0.72, 0.48, 0.02), segments=14, axis="y"),
        make_cylinder(0.068, 0.068, 0.52, center=(0.90, 0.48, 0.02), segments=14, axis="y"),
    ]
    add_part(sm, "Corridor02_WhiteBlastDoorsAndExtinguishers", merge_geometries(extinguishers_and_liner), mats["aero_white"])
    add_part(sm, "Corridor02_CarbonSlateDoorArmor", merge_geometries([s_l, s_r]), mats["carbon_slate"])

    trauma_pack = make_sculpted_cushion(
        (0.18, 0.32, 0.16), center=(1.08, 0.52, 0.02), res=(5, 4, 4), roundness=0.36, belly_puff=0.05, crease_freq=3
    )
    add_part(sm, "Corridor02_StowedNavyTraumaPack", trauma_pack, mats["pad_navy"])

    # 4. Right Bay Rotary Pressure Handwheel, Extinguisher Nozzles & Machined Manifold Pipes
    wheel_or, wheel_st = make_rotary_override_handwheel(cx=1.06, cy=1.46, cz=0.28, radius=0.11)
    orange_parts = [
        wheel_or,
        # Extinguisher valve heads & discharge horns
        make_cylinder(0.035, 0.048, 0.09, center=(0.72, 0.78, 0.02), segments=10, axis="y"),
        make_cylinder(0.035, 0.048, 0.09, center=(0.90, 0.78, 0.02), segments=10, axis="y"),
        make_beveled_box((0.20, 0.035, 0.04), center=(1.08, 0.52, 0.11), bevel=0.006),
        make_beveled_box((0.05, 0.16, 0.04), center=(1.06, 1.82, 0.26), bevel=0.006),
    ]
    add_part(sm, "Corridor02_SignalOrangeHandwheelAndValves", merge_geometries(orange_parts), mats["accent_orange"])

    pipe_pts = sample_filleted_polyline([(0.72, 1.98, 0.04), (0.72, 2.38, 0.04), (1.08, 2.38, 0.04), (1.08, 1.98, 0.04)], 0.06, 5)
    steel_all = [
        steel_sill,
        st_l,
        st_r,
        wheel_st,
        make_swept_tube(pipe_pts, radius=0.022, radial_segments=10),
        make_beveled_box((0.42, 0.03, 0.06), center=(0.81, 0.48, 0.08), bevel=0.005),
    ]
    add_part(sm, "Corridor02_MachinedTeethSillAndPipes", merge_geometries(steel_all), mats["steel_machined"])

    # 5. Upper Right Bay OLED Checkpoint Terminal + Beacons + Translucent Windows (Doors + Side Locker)
    add_part(
        sm,
        "Corridor02_RightBayOLEDStatus",
        make_quad_panel((0.58, 1.26, 0.24), (0.90, 1.26, 0.24), (0.90, 1.78, 0.24), (0.58, 1.78, 0.24)),
        mats["oled_status"],
    )
    add_part(
        sm,
        "Corridor02_AmberBeaconsAndSillLED",
        merge_geometries([
            amber_led,
            make_beveled_box((0.60, 0.022, 0.04), center=(0.89, 1.13, 0.25), bevel=0.004),
        ]),
        mats["led_amber"],
    )
    add_part(
        sm,
        "Corridor02_CyanArchAndLockerLED",
        merge_geometries([
            cyan_led,
            make_beveled_box((0.60, 0.024, 0.04), center=(0.89, 2.46, 0.24), bevel=0.004),
            make_beveled_box((0.58, 0.022, 0.04), center=(0.89, 1.08, 0.16), bevel=0.004),
        ]),
        mats["led_cyan"],
    )

    locker_glass = make_quad_panel((0.57, 0.18, 0.26), (1.17, 0.18, 0.26), (1.17, 1.12, 0.26), (0.57, 1.12, 0.26))
    add_part(sm, "Corridor02_TranslucentDoorAndLockerWindows", merge_geometries([g_l, g_r, locker_glass]), mats["glass_viewport"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "corridor_door_r1_02.glb"), sm, root_name="CorridorDoorR1_02_DualZoneAirlockSideBay")


# ==============================================================================
# CANDIDATE 03: CYLINDRICAL PLUG-DOOR PRESSURE LOCK & ROTARY DOG-LATCH PORTAL (`corridor_door_r1_03.glb`)
# Dimensions: 2.45m W x 0.70m D x 2.75m H
# ==============================================================================
def build_03_cylindrical_plug_door_portal(mats):
    sm = []
    # 1. Heavy Circular/Stadium Submarine-Style Orbital Pressure Bulkhead Coaming
    coaming, seal, steel_sill, amber_led, cyan_led = make_octagonal_portal_coaming(
        portal_cx=0.0, outer_w=2.45, outer_h=2.75, depth_z=0.70, open_w=1.68, open_h=2.22, sill_h=0.12
    )
    add_part(sm, "Corridor03_SubmarineGunmetalBulkhead", coaming, mats["gunmetal"])
    add_part(sm, "Corridor03_CharcoalPressureSeal", seal, mats["pad_charcoal"])

    # 2. Twin Plug-Door Halves Parted Open by 0.40m in Center + Swing-Link Arms & 8 Radial Locking Dogs
    w_l, s_l, st_l, g_l = make_parted_door_leaf_with_window_and_teeth(
        leaf_cx=-0.52, leaf_w=0.64, y_bot=0.13, y_top=2.33, z_pos=0.04, thick_z=0.14, win_w=0.30, win_h=0.72, win_cy=1.38, inner_edge_sign=1.0, num_teeth=4
    )
    w_r, s_r, st_r, g_r = make_parted_door_leaf_with_window_and_teeth(
        leaf_cx=0.52, leaf_w=0.64, y_bot=0.13, y_top=2.33, z_pos=0.04, thick_z=0.14, win_w=0.30, win_h=0.72, win_cy=1.38, inner_edge_sign=-1.0, num_teeth=4
    )
    add_part(sm, "Corridor03_WhitePlugDoorHalves", merge_geometries([w_l, w_r]), mats["aero_white"])
    add_part(sm, "Corridor03_CarbonSlatePlugRibs", merge_geometries([s_l, s_r]), mats["carbon_slate"])

    wheel_or, wheel_st = make_rotary_override_handwheel(cx=-0.52, cy=0.72, cz=0.14, radius=0.14)
    swing_arms = [
        steel_sill,
        st_l,
        st_r,
        wheel_st,
        make_swept_tube(sample_filleted_polyline([(-0.92, 1.82, 0.22), (-0.78, 1.82, 0.34), (-0.52, 1.82, 0.14)], 0.04, 4), radius=0.024, radial_segments=10),
        make_swept_tube(sample_filleted_polyline([(0.92, 1.82, 0.22), (0.78, 1.82, 0.34), (0.52, 1.82, 0.14)], 0.04, 4), radius=0.024, radial_segments=10),
    ]
    add_part(sm, "Corridor03_SwingArmsAndRadialDogs", merge_geometries(swing_arms), mats["steel_machined"])
    add_part(sm, "Corridor03_SignalOrangeSpiderWheel", wheel_or, mats["accent_orange"])

    # 3. Left Frame OLED Status Terminal + Beacons + Translucent Windows
    add_part(
        sm,
        "Corridor03_LeftFrameOLEDStatus",
        make_quad_panel((-1.16, 1.18, 0.355), (-0.88, 1.18, 0.355), (-0.88, 1.62, 0.355), (-1.16, 1.62, 0.355)),
        mats["oled_status"],
    )
    add_part(sm, "Corridor03_AmberThresholdLED", amber_led, mats["led_amber"])
    add_part(sm, "Corridor03_CyanArchLED", cyan_led, mats["led_cyan"])
    add_part(sm, "Corridor03_TranslucentPlugPortholes", merge_geometries([g_l, g_r]), mats["glass_viewport"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "corridor_door_r1_03.glb"), sm, root_name="CorridorDoorR1_03_CylindricalPlugDoorPortal")


# ==============================================================================
# CANDIDATE 04: HEX-APERTURE INTERLOCKING WEDGE-BLADE SECTOR BULKHEAD (`corridor_door_r1_04.glb`)
# Dimensions: 2.50m W x 0.62m D x 2.75m H
# ==============================================================================
def build_04_hex_wedge_blade_bulkhead(mats):
    sm = []
    # 1. Wide Hexagonal Pressure Bulkhead Coaming
    coaming, seal, steel_sill, amber_led, cyan_led = make_octagonal_portal_coaming(
        portal_cx=0.0, outer_w=2.50, outer_h=2.75, depth_z=0.62, open_w=1.74, open_h=2.22, sill_h=0.12
    )
    add_part(sm, "Corridor04_HexagonalGunmetalBulkhead", coaming, mats["gunmetal"])
    add_part(sm, "Corridor04_CharcoalHexSeal", seal, mats["pad_charcoal"])

    # 2. Bi-Parting Hex-Wedge Door Leaves with Diagonal Interlocking Shear Teeth & Translucent Windows
    w_l, s_l, st_l, g_l = make_parted_door_leaf_with_window_and_teeth(
        leaf_cx=-0.55, leaf_w=0.64, y_bot=0.13, y_top=2.33, z_pos=0.0, thick_z=0.12, win_w=0.32, win_h=0.92, win_cy=1.35, inner_edge_sign=1.0, num_teeth=4
    )
    w_r, s_r, st_r, g_r = make_parted_door_leaf_with_window_and_teeth(
        leaf_cx=0.55, leaf_w=0.64, y_bot=0.13, y_top=2.33, z_pos=0.0, thick_z=0.12, win_w=0.32, win_h=0.92, win_cy=1.35, inner_edge_sign=-1.0, num_teeth=4
    )
    add_part(sm, "Corridor04_WhiteWedgeBladeLeaves", merge_geometries([w_l, w_r]), mats["aero_white"])
    add_part(sm, "Corridor04_CarbonSlateHexRibs", merge_geometries([s_l, s_r]), mats["carbon_slate"])

    wheel_or, wheel_st = make_rotary_override_handwheel(cx=1.04, cy=0.92, cz=0.32, radius=0.11)
    add_part(sm, "Corridor04_MachinedShearTeethAndSill", merge_geometries([steel_sill, st_l, st_r, wheel_st]), mats["steel_machined"])
    add_part(sm, "Corridor04_SignalOrangeOverrideWheel", wheel_or, mats["accent_orange"])

    # 3. Dual Side OLED Status Pillars + Beacons + Translucent Windows
    oled_pillars = [
        make_quad_panel((-1.18, 1.22, 0.315), (-0.92, 1.22, 0.315), (-0.92, 1.66, 0.315), (-1.18, 1.66, 0.315)),
        make_quad_panel((0.92, 1.22, 0.315), (1.18, 1.22, 0.315), (1.18, 1.66, 0.315), (0.92, 1.66, 0.315)),
    ]
    add_part(sm, "Corridor04_DualSideOLEDStatus", merge_geometries(oled_pillars), mats["oled_status"])
    add_part(sm, "Corridor04_AmberHexBeaconLED", amber_led, mats["led_amber"])
    add_part(sm, "Corridor04_CyanHexArchLED", cyan_led, mats["led_cyan"])
    add_part(sm, "Corridor04_TranslucentWedgeWindows", merge_geometries([g_l, g_r]), mats["glass_viewport"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "corridor_door_r1_04.glb"), sm, root_name="CorridorDoorR1_04_HexWedgeBladeBulkhead")


# ==============================================================================
# CANDIDATE 05: PANORAMIC TWIN-WINDOW OBSERVATION AIRLOCK & DECON ARCH (`corridor_door_r1_05.glb`)
# Dimensions: 2.55m W x 0.68m D x 2.78m H
# ==============================================================================
def build_05_panoramic_decon_airlock_arch(mats):
    sm = []
    # 1. Wide Decontamination & Observation Airlock Arch Coaming
    coaming, seal, steel_sill, amber_led, cyan_led = make_octagonal_portal_coaming(
        portal_cx=0.0, outer_w=2.55, outer_h=2.78, depth_z=0.68, open_w=1.76, open_h=2.24, sill_h=0.12
    )
    add_part(sm, "Corridor05_DeconArchGunmetalCoaming", coaming, mats["gunmetal"])
    add_part(sm, "Corridor05_CharcoalDeconSeal", seal, mats["pad_charcoal"])

    # 2. Wide Bi-Parting Doors with Floor-to-Head-Height Panoramic Translucent Glass Panels
    w_l, s_l, st_l, g_l = make_parted_door_leaf_with_window_and_teeth(
        leaf_cx=-0.55, leaf_w=0.66, y_bot=0.13, y_top=2.35, z_pos=0.0, thick_z=0.12, win_w=0.38, win_h=1.42, win_cy=1.28, inner_edge_sign=1.0, num_teeth=3
    )
    w_r, s_r, st_r, g_r = make_parted_door_leaf_with_window_and_teeth(
        leaf_cx=0.55, leaf_w=0.66, y_bot=0.13, y_top=2.35, z_pos=0.0, thick_z=0.12, win_w=0.38, win_h=1.42, win_cy=1.28, inner_edge_sign=-1.0, num_teeth=3
    )
    add_part(sm, "Corridor05_WhitePanoramicDoorLeaves", merge_geometries([w_l, w_r]), mats["aero_white"])
    add_part(sm, "Corridor05_CarbonSlateDoorTrim", merge_geometries([s_l, s_r]), mats["carbon_slate"])

    # 3. Internal Sonic-Mist Decon Nozzles + UV-Violet (#7B5CFF) Sterilizer Bars + Emergency Purge Pull-Rings
    wheel_or, wheel_st = make_rotary_override_handwheel(cx=1.06, cy=1.02, cz=0.35, radius=0.11)
    decon_nozzles = [steel_sill, st_l, st_r, wheel_st]
    for ny in [0.75, 1.25, 1.75]:
        decon_nozzles.append(make_cylinder(0.025, 0.018, 0.06, center=(-0.85, ny, 0.18), segments=10, axis="x"))
        decon_nozzles.append(make_cylinder(0.025, 0.018, 0.06, center=(0.85, ny, 0.18), segments=10, axis="x"))
    add_part(sm, "Corridor05_MachinedDeconNozzlesAndTeeth", merge_geometries(decon_nozzles), mats["steel_machined"])

    pull_rings = [
        wheel_or,
        make_beveled_box((0.12, 0.03, 0.03), center=(-0.72, 2.26, 0.22), bevel=0.005),
        make_beveled_box((0.12, 0.03, 0.03), center=(0.72, 2.26, 0.22), bevel=0.005),
    ]
    add_part(sm, "Corridor05_SignalOrangePurgeHandlesAndWheel", merge_geometries(pull_rings), mats["accent_orange"])

    uv_bars = [
        make_beveled_box((0.03, 1.88, 0.04), center=(-0.86, 1.25, 0.24), bevel=0.005),
        make_beveled_box((0.03, 1.88, 0.04), center=(0.86, 1.25, 0.24), bevel=0.005),
    ]
    add_part(sm, "Corridor05_UVVioletDeconStrips", merge_geometries(uv_bars), mats["led_uv"])

    # 4. Side Biometric OLED Kiosk + Beacons + Panoramic Translucent Door Windows
    add_part(
        sm,
        "Corridor05_BiometricOLEDKiosk",
        make_quad_panel((0.92, 1.24, 0.345), (1.20, 1.24, 0.345), (1.20, 1.72, 0.345), (0.92, 1.72, 0.345)),
        mats["oled_status"],
    )
    add_part(sm, "Corridor05_AmberBeaconLED", amber_led, mats["led_amber"])
    add_part(sm, "Corridor05_CyanArchLED", cyan_led, mats["led_cyan"])
    add_part(sm, "Corridor05_PanoramicTranslucentDoorGlass", merge_geometries([g_l, g_r]), mats["glass_viewport"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "corridor_door_r1_05.glb"), sm, root_name="CorridorDoorR1_05_PanoramicDeconAirlockArch")


# ==============================================================================
# ROOM 01 & ROOM 02 ARCHITECTURAL SHELL GENERATORS (WITH ALIAS COPIES)
# ==============================================================================
def build_room_02_corridor_shell(mats):
    """
    Builds Room 02 — Orbital Sector Transit Corridor & Airlock Hub Shell (3.6m W x 12.0m D x 3.2m H):
    - 7 Repeating 45° Chamfered Octagonal Titanium Ribs (Z = -6.0, -4.0, -2.0, 0.0, +2.0, +4.0, +6.0)
    - West Continuous Translucent Observation Window Gallery (X = -1.78m, 6 faceted bays with alphaMode: BLEND glass)
    - Carbon-slate composite deck grating with twin Circadian Amber (#FF9500) guide strips & Orbital Cyan (#00E5FF) ceiling coves
    """
    sm = []
    slate_deck = [
        make_beveled_box((3.8, 0.08, 12.2), center=(0.0, 0.04, 0.0), bevel=0.02),
    ]
    gunmetal_ribs = [
        make_beveled_box((3.8, 0.08, 12.2), center=(0.0, 3.16, 0.0), bevel=0.02),
        # Lower & upper West wall rails around the 6 panoramic window bays
        make_beveled_box((0.12, 0.82, 12.0), center=(-1.80, 0.45, 0.0), bevel=0.02),
        make_beveled_box((0.12, 0.72, 12.0), center=(-1.80, 2.82, 0.0), bevel=0.02),
        # East stateroom bulkhead wall
        make_beveled_box((0.12, 3.12, 12.0), center=(1.80, 1.60, 0.0), bevel=0.02),
    ]
    white_coffers = []
    steel_rails = [
        make_cylinder(0.022, 0.022, 11.6, center=(-1.68, 1.02, 0.0), segments=10, axis="z"),
        make_cylinder(0.022, 0.022, 11.6, center=(1.68, 1.02, 0.0), segments=10, axis="z"),
    ]
    glass_bays = []

    for z_rib in [-6.0, -4.0, -2.0, 0.0, 2.0, 4.0, 6.0]:
        gunmetal_ribs.extend([
            make_beveled_box((0.20, 3.12, 0.22), center=(-1.72, 1.60, z_rib), bevel=0.03),
            make_beveled_box((0.20, 3.12, 0.22), center=(1.72, 1.60, z_rib), bevel=0.03),
            make_beveled_box((3.60, 0.20, 0.22), center=(0.0, 3.06, z_rib), bevel=0.03),
            transform_geom(make_beveled_box((0.60, 0.16, 0.22), bevel=0.02), translate=(-1.48, 2.84, z_rib), rot_xyz_deg=(0.0, 0.0, 45.0)),
            transform_geom(make_beveled_box((0.60, 0.16, 0.22), bevel=0.02), translate=(1.48, 2.84, z_rib), rot_xyz_deg=(0.0, 0.0, -45.0)),
        ])

    for z_bay in [-5.0, -3.0, -1.0, 1.0, 3.0, 5.0]:
        white_coffers.append(make_beveled_box((2.40, 0.05, 1.68), center=(0.0, 3.10, z_bay), bevel=0.015))
        glass_bays.append(
            make_quad_panel((-1.76, 0.86, z_bay + 0.84), (-1.76, 0.86, z_bay - 0.84), (-1.76, 2.46, z_bay - 0.84), (-1.76, 2.46, z_bay + 0.84))
        )

    amber_guides = [
        make_beveled_box((0.04, 0.012, 11.6), center=(-0.95, 0.085, 0.0), bevel=0.003),
        make_beveled_box((0.04, 0.012, 11.6), center=(0.95, 0.085, 0.0), bevel=0.003),
    ]
    cyan_coves = [
        make_beveled_box((0.05, 0.03, 11.6), center=(-1.15, 2.98, 0.0), bevel=0.005),
        make_beveled_box((0.05, 0.03, 11.6), center=(1.15, 2.98, 0.0), bevel=0.005),
    ]

    add_part(sm, "CorridorShell_CarbonSlateDeck", merge_geometries(slate_deck), mats["carbon_slate"])
    add_part(sm, "CorridorShell_OctagonalTitaniumRibs", merge_geometries(gunmetal_ribs), mats["gunmetal"])
    add_part(sm, "CorridorShell_AerospaceWhiteCoffers", merge_geometries(white_coffers), mats["aero_white"])
    add_part(sm, "CorridorShell_MachinedHandrails", merge_geometries(steel_rails), mats["steel_machined"])
    add_part(sm, "CorridorShell_AmberFloorGuides", merge_geometries(amber_guides), mats["led_amber"])
    add_part(sm, "CorridorShell_CyanCeilingCoves", merge_geometries(cyan_coves), mats["led_cyan"])
    add_part(sm, "CorridorShell_WestTranslucentWindowGallery", merge_geometries(glass_bays), mats["glass_viewport"])

    p1 = os.path.join(ROOMS_GLB_DIR, "room_02_shell.glb")
    p2 = os.path.join(ROOMS_GLB_DIR, "room_02_corridor_shell.glb")
    p3 = "/workspace/game-project/assets/glb/room_02_corridor_shell.glb"
    info = center_and_export_glb(p1, sm, root_name="Room02_TransitCorridorShell")
    shutil.copyfile(p1, p2)
    shutil.copyfile(p1, p3)
    print(f"[room_02_shell] Exported {p1} and mirrored to {p2} & {p3} ({info['triangles']} tris)")
    return info


def build_all_corridor_round1():
    mats = get_corridor_materials()
    builders = [
        build_01_octagonal_biparting_hatch,
        build_02_dual_zone_airlock_sidebay,
        build_03_cylindrical_plug_door_portal,
        build_04_hex_wedge_blade_bulkhead,
        build_05_panoramic_decon_airlock_arch,
    ]
    results = []
    for fn in builders:
        info = fn(mats)
        fname = os.path.basename(info["filepath"])
        dims = info["dimensions"]
        print(
            f"[corridor_r1] Built {fname:22s} | {dims[0]:.2f}m W x {dims[2]:.2f}m D x {dims[1]:.2f}m H | "
            f"verts={info['vertices']:4d} | tris={info['triangles']:4d} | min_y={info['min'][1]:.5f}"
        )
        results.append(info)
    with open(os.path.join(OUT_GLB_DIR, "corridor_r1_manifest.json"), "w") as f:
        json.dump(results, f, indent=2)

    build_room_01_sleeping_quarters_shell(mats)
    build_room_02_corridor_shell(mats)
    return results




def build_room_01_sleeping_quarters_shell(mats):
    """
    Builds Room 01 — Crew Sleeping Quarters Architectural Shell (6.0m W x 7.0m D x 3.2m H):
    - Centered at (0,0,0) with floor deck min Y = 0.0000m
    - 5 Dark Gunmetal Titanium (#1A1E24) 45° chamfered octagonal structural ring ribs (Z = -3.40, -1.70, 0.00, +1.70, +3.40)
    - Matte Aerospace-White (#D8DEE6) coffered ceiling panels with recessed Orbital Cyan (#00E5FF) LED cove channels (X = ±2.45m)
    - Carbon-Slate (#282E38) floor deck with Brushed Machined-Steel (#88929E) expansion strips & Circadian Amber (#FF9500) guide strips (X = ±1.35m)
    - North Wall (Z = -3.48m): 3-panel chamfered octagonal panoramic window cutout (X = -2.1m to +2.1m, Y = 0.85m to 2.55m)
      glazed with alphaMode: "BLEND" translucent glass (alpha ~ 0.18)
    - West Wall (X = -3.00m): Open viewport cutouts around Z = -2.25m..-1.35m and Z = +0.35m..+1.35m so Bunk #1 and Bunk #3
      viewports and exterior vistas are completely unobstructed
    - East Wall (X = +3.00m): Solid dark titanium & carbon-slate wainscot bulkhead with machined steel rail
    - South Wall (Z = +3.48m): Entry airlock bulkhead with chamfered corridor hatch frame and unobstructed center clearance
    """
    sm = []

    # 1. Carbon-Slate Floor Deck (6.0m W x 7.0m D, Y = 0.00..0.06m) + East & West Lower Wainscot Sills
    slate_parts = [
        make_beveled_box((6.00, 0.06, 7.00), center=(0.0, 0.03, 0.0), bevel=0.015),
        # East wall lower wainscot (X = +3.00m)
        make_beveled_box((0.10, 1.02, 6.88), center=(2.95, 0.54, 0.0), bevel=0.02),
        # West wall lower sill below bunk viewports (Y = 0.06..0.56m)
        make_beveled_box((0.10, 0.50, 6.88), center=(-2.95, 0.31, 0.0), bevel=0.02),
        # North wall lower sill below panoramic window (Y = 0.06..0.85m)
        make_beveled_box((5.88, 0.79, 0.10), center=(0.0, 0.455, -3.45), bevel=0.02),
    ]
    add_part(sm, "Room01_CarbonSlateDeckAndWainscot", merge_geometries(slate_parts), mats["carbon_slate"])

    # 2. 5 Repeating 45° Chamfered Octagonal Gunmetal Titanium Ribs & Bulkhead Walls (with North & West Open Cutouts!)
    gunmetal_parts = [
        # Ceiling structural deck (Y = 3.14..3.20m)
        make_beveled_box((6.00, 0.06, 7.00), center=(0.0, 3.17, 0.0), bevel=0.015),
        # East wall upper titanium bulkhead (X = +2.95m, Y = 1.06..3.14m)
        make_beveled_box((0.10, 2.08, 6.88), center=(2.95, 2.10, 0.0), bevel=0.02),
        # West wall upper header above bunk viewports (Y = 2.48..3.14m)
        make_beveled_box((0.10, 0.66, 6.88), center=(-2.95, 2.81, 0.0), bevel=0.02),
        # West wall structural piers leaving wide open cutouts at Z in [-2.85, -0.85] (covers Z=-2.25 & -1.85) and Z in [-0.15, +1.65] (covers Z=+0.55 & +0.85)
        make_beveled_box((0.10, 1.92, 0.56), center=(-2.95, 1.52, -3.16), bevel=0.02),
        make_beveled_box((0.10, 1.92, 0.66), center=(-2.95, 1.52, -0.50), bevel=0.02),
        make_beveled_box((0.10, 1.92, 1.72), center=(-2.95, 1.52, 2.56), bevel=0.02),
        # North wall upper header & side pillars around the 3-panel panoramic window cutout (X = -2.10..+2.10, Y = 0.85..2.55)
        make_beveled_box((5.88, 0.60, 0.10), center=(0.0, 2.85, -3.45), bevel=0.02),
        make_beveled_box((0.88, 1.72, 0.10), center=(-2.52, 1.70, -3.45), bevel=0.02),
        make_beveled_box((0.88, 1.72, 0.10), center=(2.52, 1.70, -3.45), bevel=0.02),
        # South Entry Airlock Bulkhead (Z = +3.45m) with wide open center corridor doorway/camera clearance (X = -1.10..+1.10 open)
        make_beveled_box((1.88, 3.08, 0.10), center=(-2.02, 1.58, 3.45), bevel=0.02),
        make_beveled_box((1.88, 3.08, 0.10), center=(2.02, 1.58, 3.45), bevel=0.02),
        make_beveled_box((2.24, 0.58, 0.10), center=(0.0, 2.86, 3.45), bevel=0.02),
    ]

    for z_rib in [-3.40, -1.70, 0.00, 1.70, 3.40]:
        gunmetal_parts.extend([
            make_beveled_box((0.18, 3.08, 0.18), center=(-2.88, 1.58, z_rib), bevel=0.025),
            make_beveled_box((0.18, 3.08, 0.18), center=(2.88, 1.58, z_rib), bevel=0.025),
            make_beveled_box((5.88, 0.18, 0.18), center=(0.0, 3.06, z_rib), bevel=0.025),
            transform_geom(make_beveled_box((0.64, 0.16, 0.18), bevel=0.02), translate=(-2.62, 2.84, z_rib), rot_xyz_deg=(0.0, 0.0, 45.0)),
            transform_geom(make_beveled_box((0.64, 0.16, 0.18), bevel=0.02), translate=(2.62, 2.84, z_rib), rot_xyz_deg=(0.0, 0.0, -45.0)),
        ])
    add_part(sm, "Room01_OctagonalGunmetalRibsAndWalls", merge_geometries(gunmetal_parts), mats["gunmetal"])

    # 3. Matte Aerospace-White Coffered Ceiling Panels
    white_coffers = []
    for z_cof in [-2.55, -0.85, 0.85, 2.55]:
        white_coffers.append(make_beveled_box((4.56, 0.05, 1.44), center=(0.0, 3.12, z_cof), bevel=0.015))
    add_part(sm, "Room01_AerospaceWhiteCeilingCoffers", merge_geometries(white_coffers), mats["aero_white"])

    # 4. Brushed Machined-Steel Deck Expansion Strips, East Dado Rail, North 3-Panel Window Mullions & South Entry Frame
    steel_parts = [
        # East wall dado rail at Y = 1.05m
        make_beveled_box((0.12, 0.05, 6.86), center=(2.92, 1.05, 0.0), bevel=0.01),
        # North 3-panel panoramic window bezel & 2 vertical mullions (X = -0.70m and +0.70m)
        make_portal_oct_ring(4.24, 1.74, center_y=1.70, z_pos=-3.42, tube_r=0.032, chamfer=0.24),
        make_beveled_box((0.06, 1.68, 0.14), center=(-0.70, 1.70, -3.43), bevel=0.012),
        make_beveled_box((0.06, 1.68, 0.14), center=(0.70, 1.70, -3.43), bevel=0.012),
        # South entry airlock frame
        make_portal_oct_ring(2.24, 2.52, center_y=1.32, z_pos=3.42, tube_r=0.032, chamfer=0.22),
    ]
    for z_strip in [-2.50, -0.80, 0.80, 2.50]:
        steel_parts.append(make_beveled_box((5.76, 0.010, 0.06), center=(0.0, 0.062, z_strip), bevel=0.002))
    add_part(sm, "Room01_MachinedSteelBezelsAndDeckStrips", merge_geometries(steel_parts), mats["steel_machined"])

    # 5. Orbital Cyan (#00E5FF) Ceiling Cove Channels & North Viewport Rim + Circadian Amber (#FF9500) Floor Guides
    cyan_parts = [
        make_beveled_box((0.05, 0.03, 6.60), center=(-2.45, 2.98, 0.0), bevel=0.005),
        make_beveled_box((0.05, 0.03, 6.60), center=(2.45, 2.98, 0.0), bevel=0.005),
        make_beveled_box((4.08, 0.024, 0.04), center=(0.0, 0.87, -3.40), bevel=0.004),
    ]
    add_part(sm, "Room01_OrbitalCyanCovesAndWindowRim", merge_geometries(cyan_parts), mats["led_cyan"])

    amber_parts = [
        make_beveled_box((0.04, 0.012, 6.60), center=(-1.35, 0.063, 0.0), bevel=0.003),
        make_beveled_box((0.04, 0.012, 6.60), center=(1.35, 0.063, 0.0), bevel=0.003),
        make_beveled_box((1.20, 0.03, 0.04), center=(0.0, 2.62, 3.40), bevel=0.005),
    ]
    add_part(sm, "Room01_CircadianAmberFloorGuides", merge_geometries(amber_parts), mats["led_amber"])

    # 6. North 3-Panel Panoramic Window Translucent Glass (alphaMode: "BLEND", alpha ~ 0.18)
    north_glass = make_quad_panel((-2.08, 0.86, -3.44), (2.08, 0.86, -3.44), (2.08, 2.54, -3.44), (-2.08, 2.54, -3.44))
    add_part(sm, "Room01_NorthPanoramicTranslucentGlass", north_glass, mats["glass_viewport"])

    p1 = os.path.join(ROOMS_GLB_DIR, "room_01_shell.glb")
    p2 = "/workspace/game-project/assets/glb/room_01_shell.glb"
    p3 = os.path.join(ROOMS_GLB_DIR, "room_01_sleeping_quarters_shell.glb")
    info = center_and_export_glb(p1, sm, root_name="Room01_SleepingQuartersShell")
    shutil.copyfile(p1, p2)
    shutil.copyfile(p1, p3)
    print(f"[room_01_shell] Exported {p1} and mirrored to {p2} & {p3} ({info['triangles']} tris)")
    return info


if __name__ == "__main__":
    build_all_corridor_round1()
