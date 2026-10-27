#!/usr/bin/env python3
"""
Builds all 10 Round-1 Hard Sci-Fi Bunk Pod Tournament .glb models:
/workspace/game-project/assets/glb/bunk_round1/bunk_r1_01.glb .. bunk_r1_10.glb
Visual Direction: Sleek Hard Sci-Fi (Star Citizen hab pods, The Expanse high-G racks,
Alien: Isolation Sevastopol aerospace pods, 2001 / Halo cryo-sleep capsules).
Zero wood, zero domestic beds, zero busy textures.
Target budget: ~2,500 - 5,500 triangles per candidate, min_y == 0.0000, centered X/Z.
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
    make_draped_blanket,
    make_curved_leaf_blade,
    make_beveled_box,
    make_cylinder,
    make_quad_panel,
    export_glb,
)

OUT_GLB_DIR = "/workspace/game-project/assets/glb/bunk_round1"
os.makedirs(OUT_GLB_DIR, exist_ok=True)


def hex_rgba(h: str, alpha: float = 1.0):
    h = h.lstrip("#")
    return (int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0, alpha)


def get_scifi_materials():
    """Hard Sci-Fi Spacecraft Material Palette (zero wood, zero stripes, zero domestic fabrics)."""
    return {
        "aero_white": PBRMaterialDef(
            name="Mat_Aerospace_WhiteComposite",
            base_color=hex_rgba("#DDE3EA"),
            metallic=0.10,
            roughness=0.35,
        ),
        "gunmetal": PBRMaterialDef(
            name="Mat_Anodized_GunmetalTitanium",
            base_color=hex_rgba("#1E242D"),
            metallic=0.78,
            roughness=0.38,
        ),
        "carbon_slate": PBRMaterialDef(
            name="Mat_Carbon_SlateAlloy",
            base_color=hex_rgba("#2B333E"),
            metallic=0.60,
            roughness=0.45,
        ),
        "brushed_titanium": PBRMaterialDef(
            name="Mat_Brushed_TitaniumSteel",
            base_color=hex_rgba("#828C99"),
            metallic=0.85,
            roughness=0.28,
        ),
        "smoked_canopy": PBRMaterialDef(
            name="Mat_Smoked_PolycarbonateGlass",
            base_color=hex_rgba("#142230"),
            metallic=0.25,
            roughness=0.14,
            double_sided=True,
        ),
        "pad_charcoal": PBRMaterialDef(
            name="Mat_FlightCouch_CharcoalSlate",
            base_color=hex_rgba("#242B35"),
            metallic=0.05,
            roughness=0.72,
        ),
        "pad_navy": PBRMaterialDef(
            name="Mat_FlightCouch_OrbitalNavy",
            base_color=hex_rgba("#1C2838"),
            metallic=0.06,
            roughness=0.70,
        ),
        "pad_cool_grey": PBRMaterialDef(
            name="Mat_FlightCouch_TechGrey",
            base_color=hex_rgba("#363F4C"),
            metallic=0.05,
            roughness=0.68,
        ),
        "accent_orange": PBRMaterialDef(
            name="Mat_EVA_SignalOrangeAccent",
            base_color=hex_rgba("#E86A17"),
            metallic=0.08,
            roughness=0.58,
        ),
        "led_cyan": PBRMaterialDef(
            name="Mat_Emissive_CyanLED",
            base_color=hex_rgba("#00E5FF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.0, 0.90, 1.0),
        ),
        "led_amber": PBRMaterialDef(
            name="Mat_Emissive_AmberCautionLED",
            base_color=hex_rgba("#FF9500"),
            metallic=0.0,
            roughness=0.15,
            emissive=(1.0, 0.58, 0.0),
        ),
        "led_white": PBRMaterialDef(
            name="Mat_Emissive_CoolWhiteMedicalLED",
            base_color=hex_rgba("#E6F4FF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.88, 0.95, 1.0),
        ),
        "oled_hud": PBRMaterialDef(
            name="Mat_OLED_VitalsTelemetryHUD",
            base_color=hex_rgba("#0B1520"),
            metallic=0.10,
            roughness=0.16,
            emissive=(0.05, 0.42, 0.58),
        ),
        "orbital_vista": PBRMaterialDef(
            name="Mat_Orbital_NightCoreVista",
            base_color=hex_rgba("#060B14"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.08, 0.28, 0.44),
        ),
        "bio_flora": PBRMaterialDef(
            name="Mat_BioReactor_OxygenFlora",
            base_color=hex_rgba("#1B6B52"),
            metallic=0.05,
            roughness=0.48,
            double_sided=True,
        ),
    }


def add_part(sm_list, name, geom, mat):
    p, n, u, idx = geom
    sm_list.append(SubMesh(name=name, positions=p, normals=n, uvs=u, indices=idx, material=mat))


def center_and_export_glb(filepath: str, submeshes, root_name: str):
    all_pts = np.vstack([sm.positions for sm in submeshes])
    min_pt = all_pts.min(axis=0)
    max_pt = all_pts.max(axis=0)
    cx = 0.5 * (min_pt[0] + max_pt[0])
    cz = 0.5 * (min_pt[2] + max_pt[2])
    y0 = min_pt[1]
    shift = np.array([-cx, -y0, -cz], dtype=np.float32)
    for sm in submeshes:
        sm.positions += shift
    return export_glb(filepath, submeshes, root_name=root_name)


# ==============================================================================
# HARD SCI-FI PROCEDURAL GEOMETRY GENERATORS
# ==============================================================================
def make_chamfered_aperture_ring(
    width_x: float,
    height_y: float,
    center_y: float,
    z_pos: float,
    tube_r: float = 0.06,
    chamfer: float = 0.28,
    oval_scale=(1.0, 1.6),
):
    """Creates an octagonal chamfered spacecraft bay aperture ring."""
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
    pts_3d = sample_filleted_polyline([(x, y, z_pos) for x, y in corners], fillet_radius=0.05, corner_subdivs=4)
    return make_swept_tube(pts_3d, radius=tube_r, radial_segments=12, closed_loop=True, oval_scale=oval_scale)


def make_contoured_flight_couch(
    length_x: float = 1.84,
    width_z: float = 0.88,
    base_y: float = 0.44,
    res=(7, 3, 5),
):
    """
    Builds a multi-zone ergonomic zero-G / high-G spacecraft flight-couch sleep pad:
    - Segmented torso pad, lumbar bolster, elevated knee-bolster wave, calf ramp,
      lateral g-force kidney bolsters, and an anatomical U-shaped cranial/neck cradle at -X.
    """
    parts = [
        # Torso & lumbar ergonomic main pad
        make_sculpted_cushion(
            (length_x * 0.56, 0.13, width_z * 0.88),
            center=(-length_x * 0.14, base_y, 0.0),
            res=res,
            roundness=0.28,
            belly_puff=0.04,
            pinch_corners=0.08,
            tuft_grid=(3, 2),
            tuft_depth=0.015,
            crease_freq=0,
        ),
        # Elevated knee-support bolster wave
        transform_geom(
            make_sculpted_cushion(
                (length_x * 0.22, 0.15, width_z * 0.86),
                res=(5, 3, 5),
                roundness=0.34,
                belly_puff=0.06,
                pinch_corners=0.08,
                crease_freq=0,
            ),
            translate=(length_x * 0.24, base_y + 0.03, 0.0),
            rot_xyz_deg=(0.0, 0.0, 8.0),
        ),
        # Lower calf/foot pad
        transform_geom(
            make_sculpted_cushion(
                (length_x * 0.22, 0.12, width_z * 0.84),
                res=(5, 3, 5),
                roundness=0.28,
                belly_puff=0.03,
                pinch_corners=0.08,
                crease_freq=0,
            ),
            translate=(length_x * 0.42, base_y + 0.01, 0.0),
            rot_xyz_deg=(0.0, 0.0, -6.0),
        ),
        # Lateral G-force kidney bolsters (front & rear edges)
        make_sculpted_cushion(
            (length_x * 0.72, 0.11, 0.11),
            center=(-0.05, base_y + 0.05, width_z * 0.46),
            res=(6, 3, 3),
            roundness=0.36,
            belly_puff=0.04,
            crease_freq=0,
        ),
        make_sculpted_cushion(
            (length_x * 0.72, 0.11, 0.11),
            center=(-0.05, base_y + 0.05, -width_z * 0.46),
            res=(6, 3, 3),
            roundness=0.36,
            belly_puff=0.04,
            crease_freq=0,
        ),
    ]
    return merge_geometries(parts)


def make_cranial_head_cradle(center=(-0.68, 0.56, 0.0), tilt_deg=-14.0):
    """Sculpted U-shaped aerospace head/neck stabilizer cradle (replaces domestic pillows)."""
    u_pts = sample_filleted_polyline(
        [
            (-0.12, 0.03, -0.22),
            (0.10, 0.0, -0.22),
            (0.10, 0.0, 0.22),
            (-0.12, 0.03, 0.22),
        ],
        fillet_radius=0.08,
        corner_subdivs=5,
    )
    cradle_rim = make_swept_tube(u_pts, radius=0.055, radial_segments=10, oval_scale=(1.2, 0.85))
    center_pad = make_sculpted_cushion(
        (0.26, 0.08, 0.34),
        center=(0.0, -0.02, 0.0),
        res=(5, 3, 5),
        roundness=0.36,
        belly_puff=0.04,
        sag_center=0.02,
        crease_freq=0,
    )
    return transform_geom(merge_geometries([cradle_rim, center_pad]), translate=center, rot_xyz_deg=(0.0, 0.0, tilt_deg))


def make_curved_canopy_shield(
    width_x: float = 1.12,
    center_x: float = -0.36,
    radius_yz: float = 0.54,
    center_y: float = 1.06,
    center_z: float = 0.0,
    ang_start_deg: float = -15.0,
    ang_end_deg: float = 78.0,
    segs_arc: int = 12,
):
    """Generates a curved smoked-polycarbonate sliding canopy shield with titanium edge ribs."""
    arc_pts = []
    for k in range(segs_arc + 1):
        t = k / float(segs_arc)
        ang = math.radians(ang_start_deg + (ang_end_deg - ang_start_deg) * t)
        py = center_y + radius_yz * math.sin(ang)
        pz = center_z + radius_yz * math.cos(ang)
        arc_pts.append((py, pz))

    quads = []
    hx = width_x * 0.5
    for k in range(segs_arc):
        y0, z0 = arc_pts[k]
        y1, z1 = arc_pts[k + 1]
        quads.append(
            make_quad_panel(
                (center_x - hx, y0, z0),
                (center_x + hx, y0, z0),
                (center_x + hx, y1, z1),
                (center_x - hx, y1, z1),
            )
        )
    return merge_geometries(quads)


# ==============================================================================
# 01: MOLDED WHITE AEROSPACE SLEEP CAPSULE (`bunk_r1_01.glb`)
# ==============================================================================
def build_01_aerospace_cryo_berth(mats):
    sm = []
    # 1. Dark Gunmetal Titanium shock-absorbing pedestal base & rear spine
    pedestal = [
        make_beveled_box((2.14, 0.28, 1.10), center=(0.0, 0.14, 0.0), bevel=0.04),
        make_beveled_box((1.92, 0.08, 1.14), center=(0.0, 0.04, 0.0), bevel=0.02),
    ]
    add_part(sm, "CryoBerth_GunmetalPedestal", merge_geometries(pedestal), mats["gunmetal"])

    # 2. Chamfered Matte Aerospace White Composite monocoque capsule hull
    white_hull = [
        make_sculpted_cushion((2.18, 0.20, 1.14), center=(0.0, 0.34, 0.0), res=(6, 3, 5), roundness=0.22, belly_puff=0.01, pinch_corners=0.0, crease_freq=0),
        make_sculpted_cushion((2.18, 0.22, 1.14), center=(0.0, 1.68, 0.0), res=(6, 3, 5), roundness=0.26, belly_puff=0.02, pinch_corners=0.0, crease_freq=0),
        make_beveled_box((0.16, 1.38, 1.12), center=(-1.01, 1.01, 0.0), bevel=0.05),
        make_beveled_box((0.16, 1.38, 1.12), center=(1.01, 1.01, 0.0), bevel=0.05),
        make_beveled_box((1.96, 1.38, 0.10), center=(0.0, 1.01, -0.51), bevel=0.03),
        make_chamfered_aperture_ring(1.98, 1.26, center_y=1.02, z_pos=0.51, tube_r=0.058, chamfer=0.28),
    ]
    add_part(sm, "CryoBerth_AerospaceWhiteHull", merge_geometries(white_hull), mats["aero_white"])

    # 3. Curved smoked-polycarbonate sliding canopy half-closed on brushed titanium tracks
    add_part(
        sm,
        "CryoBerth_SmokedPolycarbonateCanopy",
        make_curved_canopy_shield(width_x=1.02, center_x=-0.42, radius_yz=0.55, center_y=1.04, center_z=0.02, ang_start_deg=-6.0, ang_end_deg=82.0, segs_arc=12),
        mats["smoked_canopy"],
    )
    canopy_trim = [
        make_cylinder(0.018, 0.018, 1.92, center=(0.0, 1.56, 0.48), segments=12, axis="x"),
        make_cylinder(0.018, 0.018, 1.92, center=(0.0, 0.44, 0.54), segments=12, axis="x"),
    ]
    add_part(sm, "CryoBerth_TitaniumCanopyTracks", merge_geometries(canopy_trim), mats["brushed_titanium"])

    # 4. Contoured dark-slate ergonomic memory-foam flight couch + cranial cradle
    add_part(sm, "CryoBerth_ContouredFlightCouch", make_contoured_flight_couch(1.84, 0.88, base_y=0.47), mats["pad_charcoal"])
    add_part(sm, "CryoBerth_CranialHeadCradle", make_cranial_head_cradle(center=(-0.68, 0.58, 0.0)), mats["pad_cool_grey"])

    # 5. Recessed Cyan LED perimeter strip + angled OLED vitals HUD console
    cyan_leds = [
        make_beveled_box((1.68, 0.028, 0.06), center=(0.0, 1.54, 0.12), bevel=0.006),
        make_beveled_box((1.68, 0.022, 0.04), center=(0.0, 0.38, 0.55), bevel=0.004),
    ]
    add_part(sm, "CryoBerth_CyanLEDPerimeter", merge_geometries(cyan_leds), mats["led_cyan"])
    add_part(
        sm,
        "CryoBerth_VitalsOLEDConsole",
        make_quad_panel((-0.52, 0.94, -0.44), (-0.08, 0.94, -0.44), (-0.08, 1.24, -0.44), (-0.52, 1.24, -0.44)),
        mats["oled_hud"],
    )

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bunk_r1_01.glb"), sm, root_name="BunkR1_01_AerospaceCryoBerth")


# ==============================================================================
# 02: HIGH-G ARMORED BULKHEAD BERTH (`bunk_r1_02.glb`)
# ==============================================================================
def build_02_expanse_bulkhead_rack(mats):
    sm = []
    # 1. Heavy Gunmetal Titanium recessed hull bay & armored ordnance drawers
    hull_bay = [
        make_beveled_box((2.18, 0.34, 1.14), center=(0.0, 0.17, 0.0), bevel=0.03),
        make_beveled_box((2.18, 0.20, 1.14), center=(0.0, 1.74, 0.0), bevel=0.03),
        make_beveled_box((2.04, 1.48, 0.09), center=(0.0, 0.98, -0.52), bevel=0.02),
        make_beveled_box((0.90, 0.22, 0.06), center=(-0.50, 0.17, 0.57), bevel=0.015),
        make_beveled_box((0.90, 0.22, 0.06), center=(0.50, 0.17, 0.57), bevel=0.015),
    ]
    add_part(sm, "ExpanseRack_ArmoredGunmetalBay", merge_geometries(hull_bay), mats["gunmetal"])

    # 2. 4 Heavy chamfered curved C-channel structural ribs matching spacecraft hull
    ribs = []
    for rx in [-1.02, -0.34, 0.34, 1.02]:
        rib_pts = sample_filleted_polyline(
            [(rx, 0.32, 0.54), (rx, 0.32, -0.48), (rx, 1.72, -0.48), (rx, 1.72, 0.50)],
            fillet_radius=0.22,
            corner_subdivs=6,
        )
        ribs.append(make_swept_tube(rib_pts, radius=0.056, radial_segments=10, oval_scale=(0.85, 1.45)))
    add_part(sm, "ExpanseRack_StructuralCChannelRibs", merge_geometries(ribs), mats["carbon_slate"])

    # 3. Gimbaled shock mounts + Deep Orbital Navy high-G contoured flight couch
    shocks = []
    for sx in [-0.72, -0.24, 0.24, 0.72]:
        shocks.append(make_cylinder(0.038, 0.038, 0.14, center=(sx, 0.38, 0.28), segments=10, axis="y"))
        shocks.append(make_cylinder(0.038, 0.038, 0.14, center=(sx, 0.38, -0.28), segments=10, axis="y"))
    grab_l = sample_filleted_polyline([(-0.98, 0.68, 0.52), (-0.98, 0.68, 0.62), (-0.98, 1.34, 0.62), (-0.98, 1.34, 0.52)], 0.04, 5)
    grab_r = sample_filleted_polyline([(0.98, 0.68, 0.52), (0.98, 0.68, 0.62), (0.98, 1.34, 0.62), (0.98, 1.34, 0.52)], 0.04, 5)
    shocks.extend([make_swept_tube(grab_l, 0.018, 10), make_swept_tube(grab_r, 0.018, 10)])
    add_part(sm, "ExpanseRack_GimbalShocksAndGrabRails", merge_geometries(shocks), mats["brushed_titanium"])

    add_part(sm, "ExpanseRack_HighGFlightCouch", make_contoured_flight_couch(1.86, 0.90, base_y=0.48), mats["pad_navy"])

    # 4. Signal-orange articulated G-force side crash bolsters & cranial stabilizer
    bolsters = [
        make_cranial_head_cradle(center=(-0.68, 0.59, 0.0)),
        make_sculpted_cushion((0.52, 0.18, 0.14), center=(-0.38, 0.62, -0.38), res=(5, 3, 3), roundness=0.35, belly_puff=0.05, crease_freq=0),
        make_sculpted_cushion((0.52, 0.18, 0.14), center=(-0.38, 0.62, 0.38), res=(5, 3, 3), roundness=0.35, belly_puff=0.05, crease_freq=0),
    ]
    add_part(sm, "ExpanseRack_GForceCrashBolsters", merge_geometries(bolsters), mats["accent_orange"])

    # 5. Recessed Amber caution LED strips
    amber_leds = [
        make_beveled_box((1.84, 0.028, 0.07), center=(0.0, 1.62, 0.18), bevel=0.005),
        make_beveled_box((1.84, 0.022, 0.04), center=(0.0, 0.32, 0.56), bevel=0.004),
    ]
    add_part(sm, "ExpanseRack_AmberCautionStrips", merge_geometries(amber_leds), mats["led_amber"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bunk_r1_02.glb"), sm, root_name="BunkR1_02_ExpanseBulkheadRack")


# ==============================================================================
# 03: CANTILEVERED MAG-LOCK ORBITAL POD (`bunk_r1_03.glb`)
# ==============================================================================
def build_03_zero_g_mag_couchette(mats):
    sm = []
    # 1. Twin vertical magnetic guide columns & rear structural spine
    mag_columns = [
        make_beveled_box((0.12, 1.82, 0.14), center=(-0.74, 0.91, -0.48), bevel=0.025),
        make_beveled_box((0.12, 1.82, 0.14), center=(0.74, 0.91, -0.48), bevel=0.025),
        make_beveled_box((1.84, 0.06, 0.44), center=(0.0, 0.03, -0.34), bevel=0.015),
    ]
    add_part(sm, "MagCouchette_VerticalGuideColumns", merge_geometries(mag_columns), mats["gunmetal"])

    # 2. Floating aerodynamic carbon-slate sleep sled hull
    sled_hull = [
        make_sculpted_cushion((2.10, 0.14, 1.02), center=(0.0, 0.42, 0.02), res=(7, 3, 5), roundness=0.28, belly_puff=0.02, pinch_corners=0.06, crease_freq=0),
        make_beveled_box((1.96, 0.46, 0.07), center=(0.0, 0.86, -0.42), bevel=0.02),
    ]
    add_part(sm, "MagCouchette_CarbonAerodynamicSled", merge_geometries(sled_hull), mats["carbon_slate"])

    # 3. Swept brushed-titanium cantilever struts, hydraulic dampers & twin articulated LED task arms
    ti_parts = []
    for sx in [-0.74, 0.74]:
        arm_pts = sample_filleted_polyline(
            [(sx, 0.18, -0.44), (sx, 0.38, 0.48), (sx, 0.54, 0.48), (sx, 0.54, -0.44)],
            fillet_radius=0.09,
            corner_subdivs=7,
        )
        ti_parts.append(make_swept_tube(arm_pts, radius=0.028, radial_segments=12))
    for lx, tx in [(-0.56, -0.44), (-0.16, -0.08)]:
        neck = sample_filleted_polyline(
            [(lx, 1.12, -0.44), (lx, 1.44, -0.22), (tx, 1.32, 0.06)],
            fillet_radius=0.12,
            corner_subdivs=7,
        )
        ti_parts.append(make_swept_tube(neck, radius=0.014, radial_segments=10))
    add_part(sm, "MagCouchette_TitaniumStrutsAndArms", merge_geometries(ti_parts), mats["brushed_titanium"])

    # 4. Technical cool-grey memory-foam flight couch + charcoal cranial cradle
    add_part(sm, "MagCouchette_TechGreyFlightPad", make_contoured_flight_couch(1.90, 0.90, base_y=0.52), mats["pad_cool_grey"])
    add_part(sm, "MagCouchette_CharcoalCranialCradle", make_cranial_head_cradle(center=(-0.68, 0.63, 0.0)), mats["pad_charcoal"])

    # 5. Glowing Cyan mag-lock track indicators + twin task light heads
    cyan_parts = [
        make_beveled_box((0.03, 1.62, 0.03), center=(-0.74, 0.92, -0.40), bevel=0.005),
        make_beveled_box((0.03, 1.62, 0.03), center=(0.74, 0.92, -0.40), bevel=0.005),
        make_beveled_box((1.72, 0.02, 0.05), center=(0.0, 0.34, 0.48), bevel=0.004),
    ]
    add_part(sm, "MagCouchette_CyanMagIndicators", merge_geometries(cyan_parts), mats["led_cyan"])

    task_heads = [
        make_lathe_dome([(0.0, 0.0), (0.065, 0.0), (0.045, 0.08), (0.015, 0.11)], center=(-0.44, 1.24, 0.06), segments=16),
        make_lathe_dome([(0.0, 0.0), (0.065, 0.0), (0.045, 0.08), (0.015, 0.11)], center=(-0.08, 1.24, 0.06), segments=16),
    ]
    add_part(sm, "MagCouchette_SurgicalTaskLights", merge_geometries(task_heads), mats["led_white"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bunk_r1_03.glb"), sm, root_name="BunkR1_03_ZeroGMagCouchette")


# ==============================================================================
# 04: ARMORED BLAST-SHUTTER CREW POD (`bunk_r1_04.glb`)
# ==============================================================================
def build_04_blast_shutter_pod(mats):
    sm = []
    # 1. Chamfered Aerospace White & Gunmetal pressurized pod enclosure
    pod_shell = [
        make_beveled_box((2.14, 0.36, 1.12), center=(0.0, 0.18, 0.0), bevel=0.035),
        make_beveled_box((0.14, 1.54, 1.10), center=(-1.00, 0.95, 0.0), bevel=0.04),
        make_beveled_box((0.14, 1.54, 1.10), center=(1.00, 0.95, 0.0), bevel=0.04),
        make_beveled_box((1.92, 1.54, 0.10), center=(0.0, 0.95, -0.50), bevel=0.025),
    ]
    add_part(sm, "BlastPod_AerospaceShell", merge_geometries(pod_shell), mats["aero_white"])

    # 2. Segmented curved Brushed-Titanium blast shutter retracting along arched geared tracks
    shutter_plates = []
    num_plates = 14
    for i in range(num_plates):
        t = i / float(num_plates - 1)
        ang = t * (math.pi * 0.52)
        sz_pos = -0.44 + 0.94 * math.sin(ang)
        sy_pos = 1.06 + 0.64 * math.cos(ang)
        rot_x = math.degrees(ang)
        shutter_plates.append(
            transform_geom(
                make_beveled_box((1.88, 0.032, 0.072), center=(0.0, 0.0, 0.0), bevel=0.008),
                translate=(0.0, sy_pos, sz_pos),
                rot_xyz_deg=(rot_x, 0.0, 0.0),
            )
        )
    shutter_plates.append(make_cylinder(0.020, 0.020, 1.56, center=(0.0, 1.02, 0.54), segments=14, axis="x"))
    add_part(sm, "BlastPod_SegmentedTitaniumShutter", merge_geometries(shutter_plates), mats["brushed_titanium"])

    # 3. Pressurized gasket rim & Contoured dark-charcoal sleep couch
    gasket_rim = [
        make_beveled_box((1.94, 0.08, 0.12), center=(0.0, 0.36, 0.52), bevel=0.02),
        make_contoured_flight_couch(1.84, 0.88, base_y=0.45),
    ]
    add_part(sm, "BlastPod_CharcoalFlightCouch", merge_geometries(gasket_rim), mats["pad_charcoal"])
    add_part(sm, "BlastPod_CranialCradle", make_cranial_head_cradle(center=(-0.66, 0.56, 0.0)), mats["pad_navy"])

    # 4. Angled interior OLED telemetry console + Medical white/amber bay lights
    add_part(
        sm,
        "BlastPod_InteriorTelemetryHUD",
        make_quad_panel((0.28, 0.84, -0.43), (0.72, 0.84, -0.43), (0.72, 1.14, -0.43), (0.28, 1.14, -0.43)),
        mats["oled_hud"],
    )
    add_part(
        sm,
        "BlastPod_AmberStatusStrip",
        make_beveled_box((1.52, 0.025, 0.05), center=(0.0, 0.99, 0.54), bevel=0.005),
        mats["led_amber"],
    )

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bunk_r1_04.glb"), sm, root_name="BunkR1_04_BlastShutterPod")


# ==============================================================================
# 05: ZERO-G / SPIN-GRAVITY RESTRAINT POD (`bunk_r1_05.glb`)
# ==============================================================================
def build_05_spin_transition_harness_bunk(mats):
    sm = []
    # 1. Aerospace White & Carbon-Slate spin-transition shell with recessed gear lockers
    shell = [
        make_beveled_box((2.14, 0.36, 1.12), center=(0.0, 0.18, 0.0), bevel=0.035),
        make_beveled_box((2.14, 0.20, 1.12), center=(0.0, 1.68, 0.0), bevel=0.035),
        make_beveled_box((0.14, 1.56, 1.10), center=(-1.00, 0.92, 0.0), bevel=0.035),
        make_beveled_box((0.14, 1.56, 1.10), center=(1.00, 0.92, 0.0), bevel=0.035),
        make_beveled_box((1.92, 1.56, 0.10), center=(0.0, 0.92, -0.50), bevel=0.025),
    ]
    add_part(sm, "SpinPod_AerospaceShell", merge_geometries(shell), mats["aero_white"])

    # 2. Sculpted EVA tubular lockdown bars on hydraulic pivots
    lock_bars = []
    for rx in [-0.86, 0.0, 0.86]:
        rb_pts = sample_filleted_polyline(
            [(rx, 0.36, 0.52), (rx, 1.56, 0.52), (rx, 1.56, -0.44)],
            fillet_radius=0.18,
            corner_subdivs=7,
        )
        lock_bars.append(make_swept_tube(rb_pts, radius=0.038, radial_segments=12))
    add_part(sm, "SpinPod_EVALockdownBars", merge_geometries(lock_bars), mats["carbon_slate"])

    # 3. Segmented Technical Grey & Signal-Orange flight couch
    add_part(sm, "SpinPod_TechGreyFlightCouch", make_contoured_flight_couch(1.84, 0.88, base_y=0.45), mats["pad_cool_grey"])
    orange_pads = [
        make_cranial_head_cradle(center=(-0.66, 0.56, 0.0)),
        make_sculpted_cushion((1.24, 0.06, 0.72), center=(0.18, 0.52, 0.0), res=(6, 2, 5), roundness=0.25, belly_puff=0.03, tuft_grid=(4, 2), tuft_depth=0.015, crease_freq=0),
    ]
    add_part(sm, "SpinPod_SignalOrangeStabilizerPads", merge_geometries(orange_pads), mats["accent_orange"])

    # 4. 4-Point contoured ballistic webbing harness & machined titanium cam buckles
    straps = []
    buckles = []
    for sx in [-0.16, 0.22, 0.60]:
        s_pts = sample_filleted_polyline(
            [(sx, 0.38, -0.46), (sx, 0.60, -0.32), (sx, 0.62, 0.32), (sx, 0.38, 0.48)],
            fillet_radius=0.10,
            corner_subdivs=5,
        )
        straps.append(make_swept_tube(s_pts, radius=0.028, radial_segments=10, oval_scale=(1.8, 0.32)))
        buckles.append(make_beveled_box((0.09, 0.032, 0.13), center=(sx, 0.62, 0.02), bevel=0.006))
    add_part(sm, "SpinPod_BallisticHarnessWebbing", merge_geometries(straps), mats["gunmetal"])
    add_part(sm, "SpinPod_TitaniumCamBuckles", merge_geometries(buckles), mats["brushed_titanium"])

    # 5. Cyan indirect perimeter cove lighting
    add_part(
        sm,
        "SpinPod_CyanCoveLight",
        make_beveled_box((1.78, 0.032, 0.08), center=(0.0, 1.54, -0.36), bevel=0.006),
        mats["led_cyan"],
    )

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bunk_r1_05.glb"), sm, root_name="BunkR1_05_SpinTransitionHarnessBunk")


# ==============================================================================
# 06: DEEP-SPACE OBSERVATION SLEEP BAY (`bunk_r1_06.glb` & `bunk_winner_01_orbital_viewport.glb`)
# ==============================================================================
def build_06_orbital_viewport_pod(mats):
    sm = []
    # 1. Dark Anodized Gunmetal Titanium observation alcove hull with TRUE OPEN REAR VIEWPORT CUTOUT
    # Cutout spans X in [-0.76, +0.76], Y in [0.76, 1.52] at Z = -0.50m (zero opaque polygons blocking sightline)
    alcove = [
        make_beveled_box((2.18, 0.38, 1.14), center=(0.0, 0.19, 0.0), bevel=0.035),
        make_beveled_box((2.18, 0.22, 1.14), center=(0.0, 1.82, 0.0), bevel=0.035),
        make_beveled_box((0.15, 1.72, 1.12), center=(-1.01, 1.00, 0.0), bevel=0.04),
        make_beveled_box((0.15, 1.72, 1.12), center=(1.01, 1.00, 0.0), bevel=0.04),
        # Lower sill & upper header around the open octagonal viewport cutout
        make_beveled_box((1.96, 0.38, 0.10), center=(0.0, 0.56, -0.50), bevel=0.02),
        make_beveled_box((1.96, 0.20, 0.10), center=(0.0, 1.63, -0.50), bevel=0.02),
        # Left & right rear pillars flanking the open viewport cutout
        make_beveled_box((0.20, 0.80, 0.10), center=(-0.86, 1.14, -0.50), bevel=0.02),
        make_beveled_box((0.20, 0.80, 0.10), center=(0.86, 1.14, -0.50), bevel=0.02),
    ]
    add_part(sm, "ViewportPod_GunmetalHullAlcove", merge_geometries(alcove), mats["gunmetal"])

    # 2. Deep chamfered octagonal brushed-titanium pressure bezel framing the open cutout
    bezel_parts = [
        make_chamfered_aperture_ring(1.62, 0.82, center_y=1.14, z_pos=-0.45, tube_r=0.048, chamfer=0.22),
        make_chamfered_aperture_ring(1.68, 0.88, center_y=1.14, z_pos=-0.52, tube_r=0.036, chamfer=0.24),
    ]
    add_part(
        sm,
        "ViewportPod_OctagonalTitaniumBezel",
        merge_geometries(bezel_parts),
        mats["brushed_titanium"],
    )

    # 3. True Alpha-Translucent Spacecraft Viewport Glass (alphaMode: "BLEND", baseColorFactor: [0.55, 0.85, 1.0, 0.22])
    glass_mat = PBRMaterialDef(
        name="Mat_Viewport_Glass_Translucent",
        base_color=(0.55, 0.85, 1.0, 0.22),
        metallic=0.10,
        roughness=0.08,
        emissive=(0.0, 0.12, 0.18),
        texture_path="/workspace/game-project/assets/textures/bunk_round2/glass_viewport_translucent.png",
        double_sided=True,
        alpha_mode="BLEND",
    )
    add_part(
        sm,
        "ViewportPod_TranslucentViewportGlass",
        make_quad_panel((-0.78, 0.74, -0.47), (0.78, 0.74, -0.47), (0.78, 1.54, -0.47), (-0.78, 1.54, -0.47)),
        glass_mat,
    )

    # 4. Contoured zero-gravity charcoal & orbital-navy lounge-sleep couch
    add_part(sm, "ViewportPod_ZeroGLoungeCouch", make_contoured_flight_couch(1.88, 0.92, base_y=0.47, res=(8, 3, 6)), mats["pad_charcoal"])
    bolsters = [
        make_cranial_head_cradle(center=(-0.68, 0.58, 0.0)),
        transform_geom(
            make_sculpted_cushion((0.36, 0.16, 0.76), res=(5, 3, 5), roundness=0.38, belly_puff=0.08, crease_freq=0),
            translate=(0.68, 0.58, 0.0),
            rot_xyz_deg=(0.0, 0.0, 16.0),
        ),
    ]
    add_part(sm, "ViewportPod_OrbitalNavyBolsters", merge_geometries(bolsters), mats["pad_navy"])

    # 5. Glowing Cyan edge-lit viewport strip & overhead task array
    cyan_strips = [
        make_beveled_box((1.56, 0.025, 0.06), center=(0.0, 1.68, 0.12), bevel=0.005),
        make_beveled_box((1.48, 0.020, 0.035), center=(0.0, 0.73, -0.43), bevel=0.004),
        make_beveled_box((1.48, 0.020, 0.035), center=(0.0, 1.55, -0.43), bevel=0.004),
    ]
    add_part(sm, "ViewportPod_CyanEdgeLighting", merge_geometries(cyan_strips), mats["led_cyan"])

    # Export both Winner #1 and updated Round 1 #06
    winner_dir = "/workspace/game-project/assets/glb/winners"
    os.makedirs(winner_dir, exist_ok=True)
    center_and_export_glb(
        os.path.join(winner_dir, "bunk_winner_01_orbital_viewport.glb"),
        [SubMesh(s.name, s.positions.copy(), s.normals.copy(), s.uvs.copy(), s.indices.copy(), s.material) for s in sm],
        root_name="BunkWinner01_OrbitalViewportPod",
    )
    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bunk_r1_06.glb"), sm, root_name="BunkR1_06_OrbitalViewportPod")


# ==============================================================================
# 07: NAVAL FRIGATE DUAL POD STACK (`bunk_r1_07.glb`)
# ==============================================================================
def build_07_stacked_corvette_bunks(mats):
    sm = []
    # 1. Gunmetal Titanium frigate structural rack & twin Aerospace White sleep tubes
    rack_frame = [
        make_beveled_box((0.14, 2.04, 1.12), center=(-1.02, 1.02, 0.0), bevel=0.035),
        make_beveled_box((0.14, 2.04, 1.12), center=(1.02, 1.02, 0.0), bevel=0.035),
        make_beveled_box((2.06, 2.02, 0.09), center=(0.0, 1.01, -0.51), bevel=0.02),
    ]
    add_part(sm, "CorvetteRack_GunmetalBulkheadFrame", merge_geometries(rack_frame), mats["gunmetal"])

    tubes = [
        make_beveled_box((1.92, 0.26, 1.10), center=(0.0, 0.13, 0.0), bevel=0.03),
        make_beveled_box((1.92, 0.14, 1.08), center=(0.0, 1.08, 0.0), bevel=0.025),
        make_beveled_box((1.92, 0.14, 1.08), center=(0.0, 1.97, 0.0), bevel=0.025),
    ]
    add_part(sm, "CorvetteRack_AerospaceCompositeTubes", merge_geometries(tubes), mats["aero_white"])

    # 2. Lower & upper contoured Orbital Navy flight-couch pads + signal-orange head cradles
    couches = [
        make_contoured_flight_couch(1.78, 0.86, base_y=0.33, res=(6, 3, 5)),
        make_contoured_flight_couch(1.78, 0.86, base_y=1.22, res=(6, 3, 5)),
    ]
    add_part(sm, "CorvetteRack_DualFlightCouches", merge_geometries(couches), mats["pad_navy"])

    cradles = [
        make_cranial_head_cradle(center=(-0.64, 0.44, 0.0)),
        make_cranial_head_cradle(center=(-0.64, 1.33, 0.0)),
    ]
    add_part(sm, "CorvetteRack_DualCranialCradles", merge_geometries(cradles), mats["accent_orange"])

    # 3. Angled Brushed-Titanium boarding ladder + smoked-polycarbonate sliding half-shields
    ladder = []
    for lx in [-0.56, -0.18]:
        rail_pts = sample_filleted_polyline(
            [(lx, 0.0, 0.62), (lx, 1.24, 0.54), (lx, 1.58, 0.54), (lx, 1.58, 0.42)],
            fillet_radius=0.08,
            corner_subdivs=5,
        )
        ladder.append(make_swept_tube(rail_pts, radius=0.018, radial_segments=10))
    for ry, rz in [(0.30, 0.60), (0.60, 0.58), (0.90, 0.56), (1.20, 0.54)]:
        ladder.append(make_cylinder(0.014, 0.014, 0.38, center=(-0.37, ry, rz), segments=10, axis="x"))
    add_part(sm, "CorvetteRack_TitaniumBoardingLadder", merge_geometries(ladder), mats["brushed_titanium"])

    shields = [
        make_beveled_box((0.68, 0.72, 0.025), center=(0.56, 0.66, 0.51), bevel=0.008),
        make_beveled_box((0.68, 0.72, 0.025), center=(0.56, 1.54, 0.51), bevel=0.008),
    ]
    add_part(sm, "CorvetteRack_SmokedPrivacyShields", merge_geometries(shields), mats["smoked_canopy"])

    # 4. Individual glowing Cyan (BAY 01) and Amber (BAY 02) bay lights
    add_part(sm, "CorvetteRack_Bay01CyanLight", make_beveled_box((1.40, 0.025, 0.06), center=(0.0, 0.98, -0.20), bevel=0.005), mats["led_cyan"])
    add_part(sm, "CorvetteRack_Bay02AmberLight", make_beveled_box((1.40, 0.025, 0.06), center=(0.0, 1.88, -0.20), bevel=0.005), mats["led_amber"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bunk_r1_07.glb"), sm, root_name="BunkR1_07_StackedCorvetteBunks")


# ==============================================================================
# 08: PRESSURIZED STASIS-STYLE SLEEP CHAMBER (`bunk_r1_08.glb`)
# ==============================================================================
def build_08_recessed_stasis_alcove(mats):
    sm = []
    # 1. Stepped metallic deck threshold + octagonal chamfered stasis chamber armor
    deck_and_hull = [
        make_beveled_box((2.24, 0.32, 1.28), center=(0.0, 0.16, -0.06), bevel=0.035),
        make_beveled_box((1.56, 0.14, 0.30), center=(0.0, 0.07, 0.66), bevel=0.025),
        make_beveled_box((1.68, 0.24, 0.26), center=(0.0, 0.12, 0.52), bevel=0.025),
        make_beveled_box((2.24, 0.20, 1.20), center=(0.0, 1.74, -0.06), bevel=0.035),
        make_beveled_box((0.16, 1.56, 1.18), center=(-1.04, 0.96, -0.06), bevel=0.04),
        make_beveled_box((0.16, 1.56, 1.18), center=(1.04, 0.96, -0.06), bevel=0.04),
        make_beveled_box((2.04, 1.56, 0.10), center=(0.0, 0.96, -0.60), bevel=0.025),
    ]
    add_part(sm, "StasisAlcove_ArmoredDeckAndChamber", merge_geometries(deck_and_hull), mats["gunmetal"])

    # 2. Chamfered octagonal aperture ring + cranial halo scanner arch & cryo manifold tubes
    halo_pts = sample_filleted_polyline(
        [(-0.78, 0.44, -0.34), (-0.54, 0.88, -0.34), (-0.54, 0.88, 0.24), (-0.78, 0.44, 0.24)],
        fillet_radius=0.14,
        corner_subdivs=6,
    )
    ti_parts = [
        make_chamfered_aperture_ring(2.02, 1.34, center_y=1.02, z_pos=0.46, tube_r=0.055, chamfer=0.28),
        make_swept_tube(halo_pts, radius=0.026, radial_segments=12),
        make_cylinder(0.035, 0.035, 1.18, center=(0.42, 1.02, -0.50), segments=12, axis="y"),
        make_cylinder(0.035, 0.035, 1.18, center=(0.64, 1.02, -0.50), segments=12, axis="y"),
    ]
    add_part(sm, "StasisAlcove_ApertureAndScannerHalo", merge_geometries(ti_parts), mats["brushed_titanium"])

    # 3. Bi-level ergonomic stasis sleep couch & dark-slate acoustic tech-panels
    couch_and_panels = [
        make_contoured_flight_couch(1.80, 0.86, base_y=0.44, res=(7, 3, 5)),
        make_cranial_head_cradle(center=(-0.66, 0.55, -0.04)),
    ]
    add_part(sm, "StasisAlcove_BiLevelStasisCouch", merge_geometries(couch_and_panels), mats["pad_charcoal"])

    # 4. Glowing Amber deck hazard strips + Cyan cranial scanner & coolant glow
    amber_strips = [
        make_beveled_box((1.44, 0.024, 0.03), center=(0.0, 0.13, 0.81), bevel=0.004),
        make_beveled_box((1.56, 0.024, 0.03), center=(0.0, 0.23, 0.65), bevel=0.004),
    ]
    add_part(sm, "StasisAlcove_AmberDeckHazardStrips", merge_geometries(amber_strips), mats["led_amber"])
    add_part(
        sm,
        "StasisAlcove_CyanScannerGlow",
        make_beveled_box((1.62, 0.028, 0.07), center=(0.0, 1.58, -0.10), bevel=0.005),
        mats["led_cyan"],
    )

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bunk_r1_08.glb"), sm, root_name="BunkR1_08_RecessedStasisAlcove")


# ==============================================================================
# 09: CLOSED-LOOP O2 SCRUBBER & HYDRO-BAY POD (`bunk_r1_09.glb`)
# ==============================================================================
def build_09_bio_lifesupport_pod(mats):
    sm = []
    # 1. Clean Aerospace White & Carbon-Slate long-duration sleep module
    hull = [
        make_beveled_box((2.14, 0.36, 1.12), center=(0.0, 0.18, 0.0), bevel=0.035),
        make_beveled_box((0.14, 1.62, 1.10), center=(-1.00, 0.92, 0.0), bevel=0.035),
        make_beveled_box((0.14, 1.62, 1.10), center=(1.00, 0.92, 0.0), bevel=0.035),
        make_beveled_box((1.94, 1.48, 0.10), center=(0.0, 0.90, -0.50), bevel=0.025),
    ]
    add_part(sm, "BioPod_AerospaceCompositeModule", merge_geometries(hull), mats["aero_white"])

    # 2. Overhead sealed cylindrical smoked-glass photobioreactor / bio-oxygenation tube
    add_part(
        sm,
        "BioPod_SealedGlassPhotobioreactorTube",
        make_cylinder(0.18, 0.18, 1.84, center=(0.0, 1.66, -0.06), segments=18, axis="x"),
        mats["smoked_canopy"],
    )

    # 3. Brushed-titanium O2 scrubber conduit pipes, end manifolds & pressure canisters
    p_left = sample_filleted_polyline([(-0.92, 1.66, -0.06), (-0.92, 1.66, 0.48), (-0.92, 0.36, 0.48)], 0.12, 6)
    p_right = sample_filleted_polyline([(0.92, 1.66, -0.06), (0.92, 1.66, 0.48), (0.92, 0.36, 0.48)], 0.12, 6)
    conduits = [
        make_cylinder(0.20, 0.20, 0.10, center=(-0.92, 1.66, -0.06), segments=16, axis="x"),
        make_cylinder(0.20, 0.20, 0.10, center=(0.92, 1.66, -0.06), segments=16, axis="x"),
        make_swept_tube(p_left, radius=0.032, radial_segments=10),
        make_swept_tube(p_right, radius=0.032, radial_segments=10),
        make_cylinder(0.065, 0.065, 0.42, center=(0.82, 0.88, -0.38), segments=12, axis="y"),
        make_cylinder(0.065, 0.065, 0.42, center=(0.64, 0.88, -0.38), segments=12, axis="y"),
    ]
    add_part(sm, "BioPod_TitaniumO2ScrubberConduits", merge_geometries(conduits), mats["brushed_titanium"])

    # 4. Compact sculptural bio-oxygenation flora inside the sealed glass photobioreactor
    flora = []
    for lx, yaw in [(-0.62, -25.0), (-0.30, -10.0), (0.0, 12.0), (0.30, -18.0), (0.62, 28.0)]:
        flora.append(
            make_curved_leaf_blade((lx, 1.60, -0.06), yaw_deg=yaw, pitch_deg=12.0, length=0.22, width=0.14, arch_drop=0.04, segs_l=5, segs_w=4)
        )
    add_part(sm, "BioPod_InternalOxygenationFlora", merge_geometries(flora), mats["bio_flora"])

    # 5. Contoured Flight Couch + Cool Cyan/UV photobioreactor grow-LED bar
    add_part(sm, "BioPod_ContouredFlightCouch", make_contoured_flight_couch(1.84, 0.88, base_y=0.45, res=(6, 3, 5)), mats["pad_charcoal"])
    add_part(sm, "BioPod_CranialCradle", make_cranial_head_cradle(center=(-0.66, 0.56, 0.0)), mats["pad_cool_grey"])
    add_part(
        sm,
        "BioPod_CyanUVReactorLight",
        make_beveled_box((1.74, 0.03, 0.09), center=(0.0, 1.46, -0.06), bevel=0.006),
        mats["led_cyan"],
    )

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bunk_r1_09.glb"), sm, root_name="BunkR1_09_BioLifesupportPod")


# ==============================================================================
# 10: OFFICER'S PANORAMIC SMART-POD (`bunk_r1_10.glb`)
# ==============================================================================
def build_10_command_stateroom_capsule(mats):
    sm = []
    # 1. Wide Anodized Gunmetal Titanium & Carbon-Slate command sleep bay
    command_hull = [
        make_beveled_box((2.26, 0.36, 1.16), center=(0.0, 0.18, 0.0), bevel=0.04),
        make_beveled_box((2.26, 1.88, 0.10), center=(0.0, 0.94, -0.53), bevel=0.03),
        make_beveled_box((0.22, 1.82, 1.12), center=(-1.02, 0.91, 0.0), bevel=0.04),
        make_beveled_box((0.22, 1.82, 1.12), center=(1.02, 0.91, 0.0), bevel=0.04),
    ]
    add_part(sm, "CommandPod_GunmetalBulkheadBay", merge_geometries(command_hull), mats["gunmetal"])

    # 2. Sweeping chamfered Brushed-Titanium overhead canopy arch & side instrument decks
    arch_pts = []
    for k in range(25):
        t = k / 24.0
        ang = math.pi * (1.0 - t)
        ax = 0.96 * math.cos(ang)
        ay = 1.16 + 0.72 * math.sin(ang)
        arch_pts.append([ax, ay, 0.48])
    ti_arch = [
        make_swept_tube(np.array(arch_pts, dtype=np.float32), radius=0.052, radial_segments=14, oval_scale=(1.2, 1.6)),
        make_beveled_box((0.26, 0.06, 0.48), center=(-0.82, 0.74, -0.22), bevel=0.015),
        make_beveled_box((0.26, 0.06, 0.48), center=(0.82, 0.74, -0.22), bevel=0.015),
    ]
    add_part(sm, "CommandPod_SweepingTitaniumArch", merge_geometries(ti_arch), mats["brushed_titanium"])

    # 3. Sculpted Charcoal & Orbital-Navy acoustic command backwall & wide ergonomic sleep couch
    backwall_pads = [
        make_sculpted_cushion((1.68, 0.72, 0.12), center=(0.0, 0.90, -0.42), res=(8, 4, 3), roundness=0.30, belly_puff=0.06, tuft_grid=(4, 2), tuft_depth=0.022, crease_freq=0),
        make_contoured_flight_couch(1.78, 0.94, base_y=0.46, res=(7, 3, 6)),
    ]
    add_part(sm, "CommandPod_ErgonomicCommandCouch", merge_geometries(backwall_pads), mats["pad_charcoal"])

    bolsters = [
        make_cranial_head_cradle(center=(-0.62, 0.58, -0.18)),
        make_cranial_head_cradle(center=(-0.62, 0.58, 0.18)),
    ]
    add_part(sm, "CommandPod_DualCranialCradles", merge_geometries(bolsters), mats["pad_navy"])

    # 4. Twin angled OLED holographic/telemetry wing displays + Cyan & Amber cove light arches
    oled_wings = [
        make_quad_panel((-0.86, 0.92, -0.38), (-0.54, 0.92, -0.44), (-0.54, 1.32, -0.44), (-0.86, 1.32, -0.38)),
        make_quad_panel((0.54, 0.92, -0.44), (0.86, 0.92, -0.38), (0.86, 1.32, -0.38), (0.54, 1.32, -0.44)),
    ]
    add_part(sm, "CommandPod_TwinOLEDStatusWings", merge_geometries(oled_wings), mats["oled_hud"])

    add_part(sm, "CommandPod_CyanCoveStrip", make_beveled_box((1.64, 0.03, 0.08), center=(0.0, 1.66, 0.10), bevel=0.006), mats["led_cyan"])
    add_part(sm, "CommandPod_AmberDeckStrip", make_beveled_box((1.84, 0.024, 0.05), center=(0.0, 0.34, 0.56), bevel=0.004), mats["led_amber"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "bunk_r1_10.glb"), sm, root_name="BunkR1_10_CommandStateroomCapsule")


def build_all_round1():
    mats = get_scifi_materials()
    builders = [
        build_01_aerospace_cryo_berth,
        build_02_expanse_bulkhead_rack,
        build_03_zero_g_mag_couchette,
        build_04_blast_shutter_pod,
        build_05_spin_transition_harness_bunk,
        build_06_orbital_viewport_pod,
        build_07_stacked_corvette_bunks,
        build_08_recessed_stasis_alcove,
        build_09_bio_lifesupport_pod,
        build_10_command_stateroom_capsule,
    ]
    results = []
    for fn in builders:
        info = fn(mats)
        fname = os.path.basename(info["filepath"])
        dims = info["dimensions"]
        print(
            f"[bunk_r1_scifi] Built {fname:16s} | {dims[0]:.2f}m x {dims[2]:.2f}m x {dims[1]:.2f}m | "
            f"verts={info['vertices']:4d} | tris={info['triangles']:4d} | min_y={info['min'][1]:.5f}"
        )
        results.append(info)
    with open("/workspace/game-project/assets/glb/bunk_round1/bunk_r1_manifest.json", "w") as f:
        json.dump(results, f, indent=2)
    return results


if __name__ == "__main__":
    build_all_round1()
