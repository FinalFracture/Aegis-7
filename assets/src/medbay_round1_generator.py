#!/usr/bin/env python3
"""
Builds all 5 Round-1 Hard Sci-Fi Room 04 Hero Asset (Surgical Autodoc Gantry & Triage Console) .glb models:
  /workspace/game-project/assets/glb/medbay_round1/med_autodoc_r1_01.glb .. med_autodoc_r1_05.glb
Plus Room 04 Architectural Shell (6.5m W x 7.5m D x 3.2m H):
  /workspace/game-project/assets/glb/rooms/room_04_shell.glb
  /workspace/game-project/assets/glb/rooms/room_04_medbay_shell.glb
  /workspace/game-project/assets/glb/rooms/room_04_med_bay_shell.glb
  /workspace/game-project/assets/glb/room_04_shell.glb
  /workspace/game-project/assets/glb/room_04_medbay_shell.glb
  /workspace/game-project/assets/glb/room_04_med_bay_shell.glb

Follows /workspace/game-project/design/medbay_round1/med_autodoc_r1_spec.md ("Aegis-7 Standard"):
- Bottom-center (0.0, 0.0, 0.0) floor pivot (min_y == 0.0000, centered X and Z), front patient transfer facing +Z
- Polygon budget: 3,500 - 5,800 triangles per candidate
- Mapped cleanly to Sloane's 9 textures in /workspace/game-project/assets/textures/medbay_round1/
- Mandatory 4-Part 3D Surgical Autodoc & Pharmacy Kit in every candidate:
  1. 45° Chamfered Bulkhead Surgical Spine & Contoured Diagnostic Table (Y ~ 0.78m) padded in orbital-navy & charcoal
     biometric upholstery with head-cradle bolster (-X) and signal-orange emergency bio-isolation release latches
  2. Articulated 3D Multi-Joint Robotic Surgical Gantry Arms & Shadowless Surgical Halo Lamp (#E0F4FF ice-white + #00E5FF cyan)
  3. Translucent Bio-Isolation Scanner Canopy & UV-Sterile Pharmacy Supply Bay (glass_med_sterile_translucent.png,
     alphaMode: "BLEND", alpha ~ 0.19) displaying 3D glowing cryo-plasma vials, cylindrical hypospray injectors, and trauma packs
  4. Articulated Multi-Screen OLED Biomonitor Triage Array (oled_medbay_vitals.png)
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

TEX_MEDBAY_DIR = "/workspace/game-project/assets/textures/medbay_round1"
OUT_GLB_DIR = "/workspace/game-project/assets/glb/medbay_round1"
ROOMS_GLB_DIR = "/workspace/game-project/assets/glb/rooms"

os.makedirs(OUT_GLB_DIR, exist_ok=True)
os.makedirs(ROOMS_GLB_DIR, exist_ok=True)


def tex_mb(fname: str) -> str:
    return os.path.join(TEX_MEDBAY_DIR, fname)


def get_medbay_materials():
    return {
        "gunmetal": PBRMaterialDef(
            name="Mat_Titanium_GunmetalHull",
            base_color=hex_rgba("#1A1E24"),
            metallic=0.78,
            roughness=0.34,
            texture_path=tex_mb("titanium_gunmetal_hull.png"),
        ),
        "aero_white": PBRMaterialDef(
            name="Mat_Composite_AerospaceWhite",
            base_color=hex_rgba("#D8DEE6"),
            metallic=0.08,
            roughness=0.26,
            texture_path=tex_mb("composite_aerospace_white.png"),
        ),
        "carbon_slate": PBRMaterialDef(
            name="Mat_Carbon_SlateFrame",
            base_color=hex_rgba("#282E38"),
            metallic=0.58,
            roughness=0.40,
            texture_path=tex_mb("carbon_slate_frame.png"),
        ),
        "steel_machined": PBRMaterialDef(
            name="Mat_Steel_MachinedGantry",
            base_color=hex_rgba("#88929E"),
            metallic=0.90,
            roughness=0.20,
            texture_path=tex_mb("steel_machined_gantry.png"),
        ),
        "pad_charcoal": PBRMaterialDef(
            name="Mat_Fabric_CharcoalFlightpad",
            base_color=hex_rgba("#242932"),
            metallic=0.00,
            roughness=0.78,
            texture_path=tex_mb("fabric_charcoal_flightpad.png"),
        ),
        "pad_navy": PBRMaterialDef(
            name="Mat_Fabric_OrbitalNavyPad",
            base_color=hex_rgba("#1D2C3C"),
            metallic=0.00,
            roughness=0.76,
            texture_path=tex_mb("fabric_orbital_navy_pad.png"),
        ),
        "accent_orange": PBRMaterialDef(
            name="Mat_Accent_SignalOrange",
            base_color=hex_rgba("#D95B26"),
            metallic=0.06,
            roughness=0.48,
            texture_path=tex_mb("accent_signal_orange.png"),
        ),
        "oled_vitals": PBRMaterialDef(
            name="Mat_OLED_MedbayVitals",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.10,
            roughness=0.14,
            emissive=(0.35, 0.90, 1.0),
            texture_path=tex_mb("oled_medbay_vitals.png"),
        ),
        "glass_sterile": PBRMaterialDef(
            name="Mat_Glass_MedSterile_Translucent",
            base_color=(0.55, 0.88, 1.0, 0.19),
            metallic=0.10,
            roughness=0.08,
            emissive=(0.0, 0.14, 0.22),
            texture_path=tex_mb("glass_med_sterile_translucent.png"),
            double_sided=True,
            alpha_mode="BLEND",
        ),
        "led_ice": PBRMaterialDef(
            name="Mat_Emissive_SurgicalIceWhiteLED",
            base_color=hex_rgba("#E0F4FF"),
            metallic=0.0,
            roughness=0.12,
            emissive=(0.88, 0.96, 1.0),
        ),
        "led_cyan": PBRMaterialDef(
            name="Mat_Emissive_CyanLED",
            base_color=hex_rgba("#00E5FF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.0, 0.90, 1.0),
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
# SHARED 4-PART 3D SURGICAL AUTODOC & PHARMACY KIT HELPERS
# ==============================================================================

def make_contoured_surgical_bed(bed_cx: float = 0.0, bed_cz: float = 0.12, bed_w: float = 1.68, bed_d: float = 0.68, bed_y: float = 0.78):
    """
    Builds Part 1: Contoured Diagnostic & Surgical Patient Table (Y ~ 0.78m) on a chamfered carbon-slate &
    aerospace-white pedestal with orbital-navy biometric pad, charcoal side bolsters & head cradle (-X),
    and signal-orange emergency bio-isolation release latches.
    Returns: (white_shell_geom, slate_pedestal_geom, navy_mattress_geom, charcoal_bolsters_geom, orange_latches_geom, cyan_rim_geom)
    """
    slate_ped = [
        make_beveled_box((bed_w * 0.66, 0.08, bed_d * 0.86), center=(bed_cx, 0.04, bed_cz), bevel=0.015),
        make_beveled_box((bed_w * 0.44, bed_y - 0.14, bed_d * 0.54), center=(bed_cx, 0.08 + (bed_y - 0.14) * 0.5, bed_cz), bevel=0.025),
    ]
    white_shell = [
        make_beveled_box((bed_w, 0.09, bed_d), center=(bed_cx, bed_y - 0.06, bed_cz), bevel=0.02),
        make_beveled_box((bed_w * 0.52, 0.14, bed_d * 0.64), center=(bed_cx, bed_y - 0.15, bed_cz), bevel=0.02),
    ]
    navy_pad = make_sculpted_cushion(
        (bed_w * 0.92, 0.085, bed_d * 0.76),
        center=(bed_cx + 0.04, bed_y + 0.01, bed_cz),
        res=(6, 3, 4),
        roundness=0.36,
        belly_puff=0.04,
        crease_freq=4,
    )
    charcoal_bolsters = [
        # Sculpted head cradle at -X end of surgical couch
        make_sculpted_cushion(
            (0.26, 0.11, bed_d * 0.66),
            center=(bed_cx - bed_w * 0.36, bed_y + 0.055, bed_cz),
            res=(4, 3, 4),
            roundness=0.40,
            belly_puff=0.05,
            crease_freq=2,
        ),
        # Front & rear biometric restraint bolsters
        make_beveled_box((bed_w * 0.80, 0.045, 0.06), center=(bed_cx + 0.04, bed_y + 0.02, bed_cz + bed_d * 0.44), bevel=0.012),
        make_beveled_box((bed_w * 0.80, 0.045, 0.06), center=(bed_cx + 0.04, bed_y + 0.02, bed_cz - bed_d * 0.44), bevel=0.012),
    ]
    orange_latches = [
        make_beveled_box((0.14, 0.032, 0.035), center=(bed_cx - bed_w * 0.26, bed_y - 0.06, bed_cz + bed_d * 0.50), bevel=0.006),
        make_beveled_box((0.14, 0.032, 0.035), center=(bed_cx + bed_w * 0.26, bed_y - 0.06, bed_cz + bed_d * 0.50), bevel=0.006),
    ]
    cyan_rim = make_beveled_box((bed_w * 0.88, 0.014, 0.025), center=(bed_cx, bed_y - 0.09, bed_cz + bed_d * 0.50), bevel=0.003)

    return (
        merge_geometries(white_shell),
        merge_geometries(slate_ped),
        navy_pad,
        merge_geometries(charcoal_bolsters),
        merge_geometries(orange_latches),
        cyan_rim,
    )


def make_articulated_robotic_surgical_arm(mount_xyz, elbow_xyz, wrist_xyz, tip_xyz):
    """
    Builds Part 2: An articulated 3D multi-joint robotic surgical manipulator arm with:
    - Brushed machined-steel shoulder/elbow/wrist rotary actuators & laser/suture end-effector needles
    - Matte aerospace-white forearm cowling sleeves
    - Signal-orange laser-cautery warning collar
    - Cyan optical biopsy emitter tip
    Returns: (steel_joints_and_links_geom, white_cowling_geom, orange_collar_geom, cyan_laser_tip_geom)
    """
    m = np.array(mount_xyz, dtype=np.float32)
    e = np.array(elbow_xyz, dtype=np.float32)
    w = np.array(wrist_xyz, dtype=np.float32)
    t = np.array(tip_xyz, dtype=np.float32)

    pts = sample_filleted_polyline([mount_xyz, elbow_xyz, wrist_xyz, tip_xyz], fillet_radius=0.05, corner_subdivs=3)
    steel_parts = [
        make_swept_tube(pts, radius=0.024, radial_segments=8),
        make_cylinder(0.048, 0.048, 0.08, center=tuple(m), segments=10, axis="y"),
        make_cylinder(0.042, 0.042, 0.09, center=tuple(e), segments=10, axis="z"),
        make_cylinder(0.034, 0.034, 0.07, center=tuple(w), segments=10, axis="x"),
        # Micro-suture pincers / cautery cone at tip
        make_cylinder(0.022, 0.008, 0.09, center=(float(t[0]), float(t[1]) - 0.04, float(t[2])), segments=8, axis="y"),
    ]
    mid1 = 0.5 * (m + e)
    mid2 = 0.5 * (e + w)
    white_cowlings = [
        make_beveled_box((0.07, 0.16, 0.07), center=tuple(mid1), bevel=0.015),
        make_beveled_box((0.06, 0.14, 0.06), center=tuple(mid2), bevel=0.015),
    ]
    orange_collar = make_cylinder(0.028, 0.028, 0.032, center=(float(t[0]), float(t[1]), float(t[2])), segments=10, axis="y")
    cyan_tip = make_cylinder(0.012, 0.006, 0.03, center=(float(t[0]), float(t[1]) - 0.09, float(t[2])), segments=8, axis="y")

    return (
        merge_geometries(steel_parts),
        merge_geometries(white_cowlings),
        orange_collar,
        cyan_tip,
    )


def make_surgical_halo_lamp(cx: float, cy: float, cz: float, radius: float = 0.28):
    """
    Builds Part 2 overhead Circular/Octagonal Shadowless Surgical Halo Lamp (#E0F4FF ice-white + #00E5FF cyan ring).
    Returns: (white_housing_geom, ice_led_geom, cyan_ring_geom)
    """
    white_housing = make_cylinder(radius, radius * 0.88, 0.055, center=(cx, cy, cz), segments=14, axis="y")
    ice_led = make_cylinder(radius * 0.82, radius * 0.82, 0.020, center=(cx, cy - 0.022, cz), segments=14, axis="y")
    cyan_ring = make_cylinder(radius * 1.03, radius * 1.03, 0.018, center=(cx, cy, cz), segments=14, axis="y")
    return white_housing, ice_led, cyan_ring


def make_uv_pharmacy_vials_and_supplies(bay_cx: float, bay_cy: float, bay_cz: float, bay_w: float = 0.48, bay_h: float = 0.54):
    """
    Builds Part 3: 3D Cryo-Plasma Vials, Cylindrical Hypospray Injectors, Trauma Packs & O2 Cylinders
    enclosed behind a translucent UV-sterile pharmacy door (`glass_med_sterile_translucent.png`, `alphaMode: "BLEND"`).
    Returns: (white_liner_and_packs_geom, steel_vial_caps_geom, orange_valves_geom, cyan_vials_geom, uv_sterilizer_geom, glass_door_geom)
    """
    white_parts = [
        make_beveled_box((bay_w, bay_h, 0.024), center=(bay_cx, bay_cy, bay_cz - 0.12), bevel=0.008),
        make_beveled_box((bay_w * 0.92, 0.020, 0.18), center=(bay_cx, bay_cy, bay_cz - 0.03), bevel=0.005),
        # Emergency trauma packs on lower shelf
        make_beveled_box((bay_w * 0.38, 0.14, 0.12), center=(bay_cx - bay_w * 0.22, bay_cy - bay_h * 0.24, bay_cz - 0.02), bevel=0.012),
        make_beveled_box((bay_w * 0.38, 0.14, 0.12), center=(bay_cx + bay_w * 0.22, bay_cy - bay_h * 0.24, bay_cz - 0.02), bevel=0.012),
    ]
    steel_parts = []
    orange_parts = [
        make_beveled_box((bay_w * 0.28, 0.028, 0.02), center=(bay_cx - bay_w * 0.22, bay_cy - bay_h * 0.24, bay_cz + 0.045), bevel=0.004),
        make_beveled_box((bay_w * 0.28, 0.028, 0.02), center=(bay_cx + bay_w * 0.22, bay_cy - bay_h * 0.24, bay_cz + 0.045), bevel=0.004),
    ]
    cyan_vials = []

    # Top row of 5 glowing 3D cryo-plasma vials & hyposprays
    x0 = bay_cx - bay_w * 0.34
    for i in range(5):
        vx = x0 + (i / 4.0) * (bay_w * 0.68)
        vy = bay_cy + bay_h * 0.20
        cyan_vials.append(make_cylinder(0.020, 0.020, 0.12, center=(vx, vy, bay_cz - 0.01), segments=8, axis="y"))
        steel_parts.append(make_cylinder(0.023, 0.023, 0.025, center=(vx, vy + 0.065, bay_cz - 0.01), segments=8, axis="y"))
        steel_parts.append(make_cylinder(0.023, 0.023, 0.025, center=(vx, vy - 0.065, bay_cz - 0.01), segments=8, axis="y"))

    door_bezel = make_portal_oct_ring(bay_w + 0.04, bay_h + 0.04, center_y=bay_cy, z_pos=bay_cz + 0.08, tube_r=0.016, chamfer=0.06)
    door_bezel[0][:, 0] += bay_cx
    steel_parts.append(door_bezel)

    uv_bar = make_beveled_box((bay_w * 0.86, 0.024, 0.03), center=(bay_cx, bay_cy + bay_h * 0.42, bay_cz), bevel=0.004)
    glass_door = make_quad_panel(
        (bay_cx - bay_w * 0.48, bay_cy - bay_h * 0.48, bay_cz + 0.08),
        (bay_cx + bay_w * 0.48, bay_cy - bay_h * 0.48, bay_cz + 0.08),
        (bay_cx + bay_w * 0.48, bay_cy + bay_h * 0.48, bay_cz + 0.08),
        (bay_cx - bay_w * 0.48, bay_cy + bay_h * 0.48, bay_cz + 0.08),
    )
    return (
        merge_geometries(white_parts),
        merge_geometries(steel_parts),
        merge_geometries(orange_parts),
        merge_geometries(cyan_vials),
        uv_bar,
        glass_door,
    )


def make_curved_translucent_canopy(cx: float, cy: float, cz: float, width_x: float = 0.72, radius_z: float = 0.36, height_y: float = 0.32):
    """
    Builds a 3-facet arched translucent bio-isolation canopy visor (`glass_med_sterile_translucent.png`, `alphaMode: "BLEND"`)
    plus brushed-steel end arches over the head/torso zone of the surgical table.
    Returns: (steel_arches_geom, glass_canopy_geom)
    """
    x0 = cx - width_x * 0.5
    x1 = cx + width_x * 0.5
    z_back = cz - radius_z
    z_mid_b = cz - radius_z * 0.45
    z_mid_f = cz + radius_z * 0.45
    z_front = cz + radius_z
    y0 = cy
    y_top = cy + height_y

    panels = [
        make_quad_panel((x0, y0, z_back), (x1, y0, z_back), (x1, y_top, z_mid_b), (x0, y_top, z_mid_b)),
        make_quad_panel((x0, y_top, z_mid_b), (x1, y_top, z_mid_b), (x1, y_top, z_mid_f), (x0, y_top, z_mid_f)),
        make_quad_panel((x0, y_top, z_mid_f), (x1, y_top, z_mid_f), (x1, y0, z_front), (x0, y0, z_front)),
    ]
    arch_l = sample_filleted_polyline([(x0, y0, z_back), (x0, y_top, z_mid_b), (x0, y_top, z_mid_f), (x0, y0, z_front)], 0.05, 3)
    arch_r = sample_filleted_polyline([(x1, y0, z_back), (x1, y_top, z_mid_b), (x1, y_top, z_mid_f), (x1, y0, z_front)], 0.05, 3)
    steels = [
        make_swept_tube(arch_l, radius=0.016, radial_segments=8),
        make_swept_tube(arch_r, radius=0.016, radial_segments=8),
    ]
    return merge_geometries(steels), merge_geometries(panels)


# ==============================================================================
# CANDIDATE 01: AEGIS-7 OCTAGONAL BULKHEAD SURGICAL AUTODOC & RING SCANNER (`med_autodoc_r1_01.glb`)
# Dimensions: 2.18m W x 1.25m D x 2.12m H
# ==============================================================================
def build_01_octagonal_autodoc_ring_scanner(mats):
    sm = []
    # 1. Rear 45° Chamfered Octagonal Surgical Bulkhead Frame & Overhead Gantry Canopy
    gm = [
        make_beveled_box((2.18, 0.08, 1.25), center=(0.0, 0.04, 0.0), bevel=0.015),
        make_beveled_box((2.18, 2.04, 0.14), center=(0.0, 1.10, -0.55), bevel=0.03),
        make_beveled_box((0.16, 2.04, 0.90), center=(-1.01, 1.10, -0.17), bevel=0.03),
        make_beveled_box((0.16, 2.04, 0.90), center=(1.01, 1.10, -0.17), bevel=0.03),
        make_beveled_box((2.18, 0.16, 1.08), center=(0.0, 2.04, -0.08), bevel=0.03),
    ]
    add_part(sm, "Autodoc01_OctagonalGunmetalBulkhead", merge_geometries(gm), mats["gunmetal"])

    # Contoured Surgical Bed (Y = 0.78m) + Translating Octagonal MRI/CT Scanner Ring
    wh_bed, sl_ped, nv_bed, ch_bed, or_bed, cy_bed = make_contoured_surgical_bed(bed_cx=-0.05, bed_cz=0.14, bed_w=1.68, bed_d=0.66, bed_y=0.78)
    mri_ring_wh = make_portal_oct_ring(0.88, 1.18, center_y=1.08, z_pos=0.14, tube_r=0.065, chamfer=0.22)
    mri_ring_wh = transform_geom(mri_ring_wh, translate=(-0.38, 0.0, 0.0), rot_xyz_deg=(0.0, 90.0, 0.0))

    # 2. Twin Overhead Articulated Robotic Surgical Arms + Shadowless Halo Lamp
    st_a1, wh_a1, or_a1, cy_a1 = make_articulated_robotic_surgical_arm((-0.10, 1.92, -0.18), (-0.18, 1.56, 0.05), (-0.12, 1.32, 0.18), (-0.10, 1.10, 0.14))
    st_a2, wh_a2, or_a2, cy_a2 = make_articulated_robotic_surgical_arm((0.42, 1.92, -0.18), (0.48, 1.56, 0.05), (0.36, 1.32, 0.18), (0.26, 1.10, 0.14))
    wh_halo, ice_halo, cy_halo = make_surgical_halo_lamp(cx=0.12, cy=1.92, cz=0.14, radius=0.28)

    # 3. Translucent Bio-Isolation Head Canopy + Backwall UV-Sterile Pharmacy Bay
    st_canopy, gl_canopy = make_curved_translucent_canopy(cx=-0.52, cy=0.84, cz=0.14, width_x=0.62, radius_z=0.33, height_y=0.30)
    wh_ph, st_ph, or_ph, cy_ph, uv_ph, gl_ph = make_uv_pharmacy_vials_and_supplies(bay_cx=0.58, bay_cy=1.42, bay_cz=-0.38, bay_w=0.56, bay_h=0.56)

    add_part(sm, "Autodoc01_CarbonSlatePedestal", sl_ped, mats["carbon_slate"])
    add_part(sm, "Autodoc01_WhiteSurgicalBedScannerAndCowlings", merge_geometries([wh_bed, mri_ring_wh, wh_a1, wh_a2, wh_halo, wh_ph]), mats["aero_white"])
    add_part(sm, "Autodoc01_OrbitalNavyPatientPad", nv_bed, mats["pad_navy"])
    add_part(sm, "Autodoc01_CharcoalBiometricBolsters", ch_bed, mats["pad_charcoal"])
    add_part(sm, "Autodoc01_MachinedRoboticArmsAndGantry", merge_geometries([st_a1, st_a2, st_canopy, st_ph]), mats["steel_machined"])
    add_part(sm, "Autodoc01_SignalOrangeBioLocksAndLasers", merge_geometries([or_bed, or_a1, or_a2, or_ph]), mats["accent_orange"])

    # 4. Boom-Mounted OLED Vitals Display
    add_part(
        sm,
        "Autodoc01_OLEDMedbayVitals",
        make_quad_panel((-0.88, 1.24, -0.28), (-0.42, 1.24, -0.28), (-0.42, 1.66, -0.28), (-0.88, 1.66, -0.28)),
        mats["oled_vitals"],
    )
    add_part(sm, "Autodoc01_SurgicalIceWhiteHaloLED", ice_halo, mats["led_ice"])
    add_part(sm, "Autodoc01_CyanScannerAndVialsLED", merge_geometries([cy_bed, cy_a1, cy_a2, cy_halo, cy_ph]), mats["led_cyan"])
    add_part(sm, "Autodoc01_UVSterilizerPharmacyLED", uv_ph, mats["led_uv"])
    add_part(sm, "Autodoc01_TranslucentCanopyAndPharmacyGlass", merge_geometries([gl_canopy, gl_ph]), mats["glass_sterile"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "med_autodoc_r1_01.glb"), sm, root_name="MedAutodocR1_01_OctagonalRingScanner")


# ==============================================================================
# CANDIDATE 02: DUAL-ZONE SPLIT AUTODOC GANTRY & TRANSLUCENT UV PHARMACY TOWER (`med_autodoc_r1_02.glb`)
# Dimensions: 2.25m W x 1.28m D x 2.15m H (Direct 68% / 32% Split-Bay Sibling to All Locked Winners!)
# ==============================================================================
def build_02_dual_zone_split_autodoc_pharmacy_tower(mats):
    sm = []
    # Left Bay (68% width, X = -1.125..+0.405, 1.53m wide, centered at X = -0.36): Surgical Bed, Twin Robotic Arms, Halo Lamp & Canopy
    # Right Bay (32% width, X = +0.405..+1.125, 0.72m wide, centered at X = +0.765): Full-Height 3-Tier UV-Sterile Pharmacy & Cryo-Vial Tower
    gm = [
        make_beveled_box((2.25, 0.08, 1.28), center=(0.0, 0.04, 0.0), bevel=0.015),
        # Left Surgical Bay Rear Spine & Overhead Gantry Canopy
        make_beveled_box((1.53, 2.07, 0.14), center=(-0.36, 1.11, -0.57), bevel=0.03),
        make_beveled_box((0.14, 2.07, 0.96), center=(-1.05, 1.11, -0.16), bevel=0.03),
        make_beveled_box((1.53, 0.16, 1.10), center=(-0.36, 2.07, -0.08), bevel=0.03),
        # Right Full-Height 3-Tier UV Pharmacy & Cryo-Vial Tower (X = +0.405..+1.125, Y = 0.08..2.15)
        make_beveled_box((0.72, 0.14, 0.92), center=(0.765, 2.08, -0.18), bevel=0.025),
        make_beveled_box((0.08, 2.04, 0.92), center=(0.43, 1.08, -0.18), bevel=0.02),
        make_beveled_box((0.10, 2.04, 0.92), center=(1.07, 1.08, -0.18), bevel=0.02),
        make_beveled_box((0.70, 2.04, 0.10), center=(0.765, 1.08, -0.58), bevel=0.02),
        # Right Tower 3-tier shelves (Y = 1.44 and Y = 0.82)
        make_beveled_box((0.60, 0.04, 0.78), center=(0.765, 1.44, -0.18), bevel=0.01),
        make_beveled_box((0.60, 0.04, 0.78), center=(0.765, 0.82, -0.18), bevel=0.01),
    ]
    add_part(sm, "Autodoc02_SplitBayGunmetalHousing", merge_geometries(gm), mats["gunmetal"])

    # Left Bay: Contoured Surgical Bed (centered at X = -0.32, Z = 0.16, Y = 0.78m)
    wh_bed, sl_ped, nv_bed, ch_bed, or_bed, cy_bed = make_contoured_surgical_bed(bed_cx=-0.32, bed_cz=0.16, bed_w=1.42, bed_d=0.66, bed_y=0.78)

    # Left Bay: Twin Overhead Multi-Jointed Robotic Surgical Arms + Circular Shadowless Halo Lamp
    st_a1, wh_a1, or_a1, cy_a1 = make_articulated_robotic_surgical_arm((-0.52, 1.94, -0.16), (-0.58, 1.56, 0.06), (-0.48, 1.32, 0.18), (-0.42, 1.08, 0.16))
    st_a2, wh_a2, or_a2, cy_a2 = make_articulated_robotic_surgical_arm((0.02, 1.94, -0.16), (0.08, 1.56, 0.06), (-0.04, 1.32, 0.18), (-0.12, 1.08, 0.16))
    wh_halo, ice_halo, cy_halo = make_surgical_halo_lamp(cx=-0.26, cy=1.94, cz=0.14, radius=0.28)

    # Left Bay: Curved Translucent Bio-Isolation Head/Chest Visor
    st_canopy, gl_canopy = make_curved_translucent_canopy(cx=-0.68, cy=0.84, cz=0.16, width_x=0.58, radius_z=0.33, height_y=0.30)

    # Right Bay Full-Height 3-Tier UV-Sterile Pharmacy, Cryo-Vial & Trauma Supply Tower (X = +0.765)
    wh_ph, st_ph, or_ph, cy_ph, uv_ph, _ = make_uv_pharmacy_vials_and_supplies(bay_cx=0.765, bay_cy=1.48, bay_cz=-0.16, bay_w=0.56, bay_h=0.96)
    # Bottom tier of Right Tower: Twin Emergency Medical O2 / Anesthesia Cylinders + Trauma Defibrillator Case
    o2_tanks_wh = [
        make_beveled_box((0.58, 1.88, 0.025), center=(0.765, 1.06, -0.48), bevel=0.008),
        make_cylinder(0.064, 0.064, 0.48, center=(0.62, 0.38, -0.14), segments=10, axis="y"),
        make_cylinder(0.064, 0.064, 0.48, center=(0.78, 0.38, -0.14), segments=10, axis="y"),
    ]
    o2_valves_or = [
        make_cylinder(0.036, 0.046, 0.08, center=(0.62, 0.65, -0.14), segments=10, axis="y"),
        make_cylinder(0.036, 0.046, 0.08, center=(0.78, 0.65, -0.14), segments=10, axis="y"),
        make_beveled_box((0.18, 0.24, 0.16), center=(0.94, 0.30, -0.12), bevel=0.015),
    ]
    tower_bezel = make_portal_oct_ring(0.60, 1.88, center_y=1.06, z_pos=0.26, tube_r=0.020, chamfer=0.09)
    tower_bezel[0][:, 0] += 0.765

    add_part(sm, "Autodoc02_CarbonSlatePedestal", sl_ped, mats["carbon_slate"])
    add_part(
        sm,
        "Autodoc02_WhiteSurgicalBedArmsAndO2Tanks",
        merge_geometries([wh_bed, wh_a1, wh_a2, wh_halo, wh_ph] + o2_tanks_wh),
        mats["aero_white"],
    )
    add_part(sm, "Autodoc02_OrbitalNavyPatientPad", nv_bed, mats["pad_navy"])
    add_part(sm, "Autodoc02_CharcoalBiometricBolsters", ch_bed, mats["pad_charcoal"])
    add_part(
        sm,
        "Autodoc02_MachinedRoboticGantryAndTowerBezel",
        merge_geometries([st_a1, st_a2, st_canopy, st_ph, tower_bezel]),
        mats["steel_machined"],
    )
    add_part(
        sm,
        "Autodoc02_SignalOrangeValvesDefibAndLatches",
        merge_geometries([or_bed, or_a1, or_a2, or_ph] + o2_valves_or),
        mats["accent_orange"],
    )

    # Swiveling OLED Biomonitor Triage Screens (Left surgical boom + Right pharmacy diagnostic screen)
    oled_screens = [
        make_quad_panel((-0.94, 1.24, -0.36), (-0.44, 1.24, -0.36), (-0.44, 1.66, -0.36), (-0.94, 1.66, -0.36)),
        make_quad_panel((0.54, 0.90, 0.02), (0.98, 0.90, 0.02), (0.98, 1.18, 0.02), (0.54, 1.18, 0.02)),
    ]
    add_part(sm, "Autodoc02_OLEDMedbayVitalsArray", merge_geometries(oled_screens), mats["oled_vitals"])
    add_part(sm, "Autodoc02_SurgicalIceWhiteHaloLED", ice_halo, mats["led_ice"])
    add_part(sm, "Autodoc02_CyanCryoVialsAndBedLED", merge_geometries([cy_bed, cy_a1, cy_a2, cy_halo, cy_ph]), mats["led_cyan"])
    add_part(sm, "Autodoc02_UVSterilizerTowerLED", uv_ph, mats["led_uv"])

    tower_glass = make_quad_panel((0.48, 0.14, 0.26), (1.05, 0.14, 0.26), (1.05, 1.98, 0.26), (0.48, 1.98, 0.26))
    add_part(
        sm,
        "Autodoc02_TranslucentCanopyAndPharmacyTowerGlass",
        merge_geometries([gl_canopy, tower_glass]),
        mats["glass_sterile"],
    )

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "med_autodoc_r1_02.glb"), sm, root_name="MedAutodocR1_02_DualZoneSplitAutodocPharmacy")


# ==============================================================================
# CANDIDATE 03: TWIN-ARM CEILING CANTILEVER ROBOTIC TRAUMA BAY & HOLO-VISOR (`med_autodoc_r1_03.glb`)
# Dimensions: 2.15m W x 1.25m D x 2.15m H
# ==============================================================================
def build_03_ceiling_cantilever_trauma_bay(mats):
    sm = []
    gm = [
        make_beveled_box((2.15, 0.08, 1.25), center=(0.0, 0.04, 0.0), bevel=0.015),
        # Heavy C-Arm Ceiling Surgical Crane Spine
        make_beveled_box((1.95, 2.07, 0.18), center=(0.0, 1.11, -0.52), bevel=0.03),
        make_beveled_box((1.95, 0.20, 1.12), center=(0.0, 2.05, -0.05), bevel=0.03),
    ]
    add_part(sm, "Autodoc03_CArmGunmetalCrane", merge_geometries(gm), mats["gunmetal"])

    wh_bed, sl_ped, nv_bed, ch_bed, or_bed, cy_bed = make_contoured_surgical_bed(bed_cx=0.0, bed_cz=0.14, bed_w=1.68, bed_d=0.66, bed_y=0.78)
    st_a1, wh_a1, or_a1, cy_a1 = make_articulated_robotic_surgical_arm((-0.46, 1.94, -0.10), (-0.52, 1.54, 0.08), (-0.40, 1.30, 0.18), (-0.32, 1.08, 0.14))
    st_a2, wh_a2, or_a2, cy_a2 = make_articulated_robotic_surgical_arm((0.02, 1.94, -0.14), (0.04, 1.58, -0.02), (0.02, 1.34, 0.08), (0.00, 1.12, 0.12))
    st_a3, wh_a3, or_a3, cy_a3 = make_articulated_robotic_surgical_arm((0.44, 1.94, -0.10), (0.50, 1.54, 0.08), (0.38, 1.30, 0.18), (0.30, 1.08, 0.14))
    wh_halo, ice_halo, cy_halo = make_surgical_halo_lamp(cx=-0.22, cy=1.94, cz=0.14, radius=0.26)
    wh_halo2, ice_halo2, cy_halo2 = make_surgical_halo_lamp(cx=0.26, cy=1.94, cz=0.14, radius=0.26)

    st_canopy, gl_canopy = make_curved_translucent_canopy(cx=-0.46, cy=0.84, cz=0.14, width_x=0.66, radius_z=0.34, height_y=0.32)
    wh_ph, st_ph, or_ph, cy_ph, uv_ph, gl_ph = make_uv_pharmacy_vials_and_supplies(bay_cx=0.58, bay_cy=1.40, bay_cz=-0.34, bay_w=0.58, bay_h=0.56)

    add_part(sm, "Autodoc03_CarbonSlatePedestal", sl_ped, mats["carbon_slate"])
    add_part(sm, "Autodoc03_WhiteBedAndCowlings", merge_geometries([wh_bed, wh_a1, wh_a2, wh_a3, wh_halo, wh_halo2, wh_ph]), mats["aero_white"])
    add_part(sm, "Autodoc03_OrbitalNavyPad", nv_bed, mats["pad_navy"])
    add_part(sm, "Autodoc03_CharcoalBolsters", ch_bed, mats["pad_charcoal"])
    add_part(sm, "Autodoc03_MachinedRoboticManipulators", merge_geometries([st_a1, st_a2, st_a3, st_canopy, st_ph]), mats["steel_machined"])
    add_part(sm, "Autodoc03_SignalOrangeLocksAndLasers", merge_geometries([or_bed, or_a1, or_a2, or_a3, or_ph]), mats["accent_orange"])

    add_part(
        sm,
        "Autodoc03_OLEDVitalsConsole",
        make_quad_panel((-0.86, 1.22, -0.32), (-0.36, 1.22, -0.32), (-0.36, 1.66, -0.32), (-0.86, 1.66, -0.32)),
        mats["oled_vitals"],
    )
    add_part(sm, "Autodoc03_SurgicalIceHaloLED", merge_geometries([ice_halo, ice_halo2]), mats["led_ice"])
    add_part(sm, "Autodoc03_CyanScannerAndVialsLED", merge_geometries([cy_bed, cy_a1, cy_a2, cy_a3, cy_halo, cy_halo2, cy_ph]), mats["led_cyan"])
    add_part(sm, "Autodoc03_UVSterilizerLED", uv_ph, mats["led_uv"])
    add_part(sm, "Autodoc03_TranslucentClamshellShield", merge_geometries([gl_canopy, gl_ph]), mats["glass_sterile"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "med_autodoc_r1_03.glb"), sm, root_name="MedAutodocR1_03_CeilingCantileverTraumaBay")


# ==============================================================================
# CANDIDATE 04: CRYO-STASIS ISOLATION POD & SLIDING TOROIDAL MRI GANTRY (`med_autodoc_r1_04.glb`)
# Dimensions: 2.20m W x 1.30m D x 2.12m H
# ==============================================================================
def build_04_cryo_stasis_toroidal_mri_gantry(mats):
    sm = []
    gm = [
        make_beveled_box((2.20, 0.08, 1.30), center=(0.0, 0.04, 0.0), bevel=0.015),
        make_beveled_box((2.20, 2.04, 0.14), center=(0.0, 1.10, -0.58), bevel=0.03),
        make_beveled_box((2.20, 0.16, 1.14), center=(0.0, 2.04, -0.08), bevel=0.03),
    ]
    add_part(sm, "Autodoc04_CryoPodGunmetalFrame", merge_geometries(gm), mats["gunmetal"])

    wh_bed, sl_ped, nv_bed, ch_bed, or_bed, cy_bed = make_contoured_surgical_bed(bed_cx=-0.06, bed_cz=0.14, bed_w=1.72, bed_d=0.68, bed_y=0.78)
    # Heavy sliding toroidal MRI gantry ring around the center of the cryo-surgical bed
    toroid_wh = make_portal_oct_ring(0.92, 1.24, center_y=1.08, z_pos=0.14, tube_r=0.075, chamfer=0.24)
    toroid_wh = transform_geom(toroid_wh, translate=(0.08, 0.0, 0.0), rot_xyz_deg=(0.0, 90.0, 0.0))

    st_a1, wh_a1, or_a1, cy_a1 = make_articulated_robotic_surgical_arm((-0.46, 1.92, -0.14), (-0.52, 1.56, 0.06), (-0.42, 1.32, 0.18), (-0.36, 1.10, 0.14))
    st_a2, wh_a2, or_a2, cy_a2 = make_articulated_robotic_surgical_arm((0.46, 1.92, -0.14), (0.52, 1.56, 0.06), (0.42, 1.32, 0.18), (0.36, 1.10, 0.14))
    wh_halo, ice_halo, cy_halo = make_surgical_halo_lamp(cx=0.0, cy=1.92, cz=0.14, radius=0.28)

    # Full-length semi-cylindrical translucent cryo-isolation canopy
    st_canopy, gl_canopy = make_curved_translucent_canopy(cx=-0.22, cy=0.84, cz=0.14, width_x=1.08, radius_z=0.34, height_y=0.34)
    wh_ph, st_ph, or_ph, cy_ph, uv_ph, gl_ph = make_uv_pharmacy_vials_and_supplies(bay_cx=0.64, bay_cy=1.42, bay_cz=-0.40, bay_w=0.54, bay_h=0.54)

    add_part(sm, "Autodoc04_CarbonSlatePedestal", sl_ped, mats["carbon_slate"])
    add_part(sm, "Autodoc04_WhiteToroidalMRIAndBed", merge_geometries([wh_bed, toroid_wh, wh_a1, wh_a2, wh_halo, wh_ph]), mats["aero_white"])
    add_part(sm, "Autodoc04_OrbitalNavyPad", nv_bed, mats["pad_navy"])
    add_part(sm, "Autodoc04_CharcoalBolsters", ch_bed, mats["pad_charcoal"])
    add_part(sm, "Autodoc04_MachinedRoboticArmsAndCanopyArches", merge_geometries([st_a1, st_a2, st_canopy, st_ph]), mats["steel_machined"])
    add_part(sm, "Autodoc04_SignalOrangeCryoValves", merge_geometries([or_bed, or_a1, or_a2, or_ph]), mats["accent_orange"])

    add_part(
        sm,
        "Autodoc04_OLEDVitalsConsole",
        make_quad_panel((-0.92, 1.24, -0.40), (-0.42, 1.24, -0.40), (-0.42, 1.68, -0.40), (-0.92, 1.68, -0.40)),
        mats["oled_vitals"],
    )
    add_part(sm, "Autodoc04_SurgicalIceHaloLED", ice_halo, mats["led_ice"])
    add_part(sm, "Autodoc04_CyanCryoAndVialsLED", merge_geometries([cy_bed, cy_a1, cy_a2, cy_halo, cy_ph]), mats["led_cyan"])
    add_part(sm, "Autodoc04_UVSterilizerLED", uv_ph, mats["led_uv"])
    add_part(sm, "Autodoc04_TranslucentCryoCanopyAndPharmacy", merge_geometries([gl_canopy, gl_ph]), mats["glass_sterile"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "med_autodoc_r1_04.glb"), sm, root_name="MedAutodocR1_04_CryoStasisToroidalMRI")


# ==============================================================================
# CANDIDATE 05: ZERO-G GIMBALED SURGICAL CRADLE & BIOMETRIC TRIAGE CONSOLE (`med_autodoc_r1_05.glb`)
# Dimensions: 2.22m W x 1.28m D x 2.15m H
# ==============================================================================
def build_05_zerog_gimbaled_surgical_cradle(mats):
    sm = []
    gm = [
        make_beveled_box((2.22, 0.08, 1.28), center=(0.0, 0.04, 0.0), bevel=0.015),
        make_beveled_box((2.22, 2.07, 0.14), center=(0.0, 1.11, -0.57), bevel=0.03),
        # Left & Right Rotary Gimbal Trunnion Towers supporting the surgical table
        make_beveled_box((0.22, 1.38, 0.68), center=(-0.98, 0.77, 0.14), bevel=0.03),
        make_beveled_box((0.22, 1.38, 0.68), center=(0.98, 0.77, 0.14), bevel=0.03),
        make_beveled_box((2.22, 0.16, 1.10), center=(0.0, 2.07, -0.08), bevel=0.03),
    ]
    add_part(sm, "Autodoc05_GimbalTrunnionGunmetalFrame", merge_geometries(gm), mats["gunmetal"])

    wh_bed, sl_ped, nv_bed, ch_bed, or_bed, cy_bed = make_contoured_surgical_bed(bed_cx=0.0, bed_cz=0.14, bed_w=1.58, bed_d=0.66, bed_y=0.78)
    st_a1, wh_a1, or_a1, cy_a1 = make_articulated_robotic_surgical_arm((-0.38, 1.94, -0.14), (-0.44, 1.56, 0.06), (-0.34, 1.32, 0.18), (-0.26, 1.10, 0.14))
    st_a2, wh_a2, or_a2, cy_a2 = make_articulated_robotic_surgical_arm((0.38, 1.94, -0.14), (0.44, 1.56, 0.06), (0.34, 1.32, 0.18), (0.26, 1.10, 0.14))
    wh_halo, ice_halo, cy_halo = make_surgical_halo_lamp(cx=0.0, cy=1.94, cz=0.14, radius=0.28)

    st_canopy, gl_canopy = make_curved_translucent_canopy(cx=-0.38, cy=0.84, cz=0.14, width_x=0.64, radius_z=0.33, height_y=0.30)
    wh_ph, st_ph, or_ph, cy_ph, uv_ph, gl_ph = make_uv_pharmacy_vials_and_supplies(bay_cx=0.56, bay_cy=1.44, bay_cz=-0.38, bay_w=0.54, bay_h=0.54)

    trunnion_hubs = [
        make_cylinder(0.16, 0.16, 0.12, center=(-0.84, 0.82, 0.14), segments=12, axis="x"),
        make_cylinder(0.16, 0.16, 0.12, center=(0.84, 0.82, 0.14), segments=12, axis="x"),
    ]
    add_part(sm, "Autodoc05_CarbonSlatePedestal", sl_ped, mats["carbon_slate"])
    add_part(sm, "Autodoc05_WhiteBedAndCowlings", merge_geometries([wh_bed, wh_a1, wh_a2, wh_halo, wh_ph]), mats["aero_white"])
    add_part(sm, "Autodoc05_OrbitalNavyPad", nv_bed, mats["pad_navy"])
    add_part(sm, "Autodoc05_CharcoalBolsters", ch_bed, mats["pad_charcoal"])
    add_part(sm, "Autodoc05_MachinedGimbalHubsAndArms", merge_geometries([st_a1, st_a2, st_canopy, st_ph] + trunnion_hubs), mats["steel_machined"])
    add_part(sm, "Autodoc05_SignalOrangeGimbalLocks", merge_geometries([or_bed, or_a1, or_a2, or_ph]), mats["accent_orange"])

    add_part(
        sm,
        "Autodoc05_OLEDVitalsConsole",
        make_quad_panel((-0.86, 1.24, -0.38), (-0.36, 1.24, -0.38), (-0.36, 1.68, -0.38), (-0.86, 1.68, -0.38)),
        mats["oled_vitals"],
    )
    add_part(sm, "Autodoc05_SurgicalIceHaloLED", ice_halo, mats["led_ice"])
    add_part(sm, "Autodoc05_CyanScannerAndVialsLED", merge_geometries([cy_bed, cy_a1, cy_a2, cy_halo, cy_ph]), mats["led_cyan"])
    add_part(sm, "Autodoc05_UVSterilizerLED", uv_ph, mats["led_uv"])
    add_part(sm, "Autodoc05_TranslucentCanopyAndPharmacy", merge_geometries([gl_canopy, gl_ph]), mats["glass_sterile"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "med_autodoc_r1_05.glb"), sm, root_name="MedAutodocR1_05_ZeroGGimbaledSurgicalCradle")


# ==============================================================================
# ROOM 04 ARCHITECTURAL SHELL (`room_04_shell.glb` / `room_04_medbay_shell.glb`)
# ==============================================================================
def build_room_04_med_bay_shell(mats):
    """
    Builds Room 04 — Med-Bay & Biomonitor Triage Suite Architectural Shell (6.5m W x 7.5m D x 3.2m H)
    following `/workspace/game-project/design/rooms/room_04_med_bay_spec.md`:
    - Centered at (0,0,0) with floor deck min Y = 0.0000m (X: -3.25..+3.25, Z: -3.75..+3.75, Y: 0.00..3.20)
    - 5 Repeating 45° Chamfered Octagonal Titanium Ribs paired with high-purity matte aerospace-white sterile ceiling coffers,
      surgical ice-white (#E0F4FF) and cyan (#00E5FF) ceiling cove strips, and UV-violet (#7B5CFF) bio-decontamination perimeter strips
    - North Outer-Hull Deep-Space Observation Viewport (Z = -3.70m, X = -2.2m to +2.2m, Y = 0.95m to 2.45m):
      3-panel chamfered octagonal window glazed with `glass_med_sterile_translucent.png` (`alphaMode: "BLEND"`, `alpha ~ 0.18`)
    - South Bulkhead (+Z = +3.70m) with open center portal cutout for `corridor_door_winner_01` and camera sightlines.
    """
    sm = []
    slate_parts = [
        make_beveled_box((6.50, 0.06, 7.50), center=(0.0, 0.03, 0.0), bevel=0.015),
        make_beveled_box((0.10, 0.96, 7.38), center=(3.20, 0.51, 0.0), bevel=0.02),
        make_beveled_box((0.10, 0.96, 7.38), center=(-3.20, 0.51, 0.0), bevel=0.02),
        make_beveled_box((6.38, 0.89, 0.10), center=(0.0, 0.505, -3.70), bevel=0.02),
    ]
    add_part(sm, "Room04_CarbonSlateDeckAndWainscot", merge_geometries(slate_parts), mats["carbon_slate"])

    gunmetal_parts = [
        make_beveled_box((6.50, 0.06, 7.50), center=(0.0, 3.17, 0.0), bevel=0.015),
        make_beveled_box((0.10, 2.18, 7.38), center=(3.20, 2.06, 0.0), bevel=0.02),
        make_beveled_box((0.10, 2.18, 7.38), center=(-3.20, 2.06, 0.0), bevel=0.02),
        # North wall header & side piers around the 4.4m wide 3-panel Deep-Space viewport (X = -2.20..+2.20, Y = 0.95..2.45)
        make_beveled_box((6.38, 0.70, 0.10), center=(0.0, 2.80, -3.70), bevel=0.02),
        make_beveled_box((1.00, 1.54, 0.10), center=(-2.70, 1.70, -3.70), bevel=0.02),
        make_beveled_box((1.00, 1.54, 0.10), center=(2.70, 1.70, -3.70), bevel=0.02),
        # South Entry Bio-Airlock Bulkhead (Z = +3.70m) with wide open center portal/camera cutout
        make_beveled_box((1.95, 3.08, 0.10), center=(-2.22, 1.58, 3.70), bevel=0.02),
        make_beveled_box((1.95, 3.08, 0.10), center=(2.22, 1.58, 3.70), bevel=0.02),
        make_beveled_box((2.56, 0.52, 0.10), center=(0.0, 2.88, 3.70), bevel=0.02),
    ]
    for z_rib in [-3.60, -1.80, 0.00, 1.80, 3.60]:
        gunmetal_parts.extend([
            make_beveled_box((0.18, 3.08, 0.20), center=(-3.12, 1.58, z_rib), bevel=0.025),
            make_beveled_box((0.18, 3.08, 0.20), center=(3.12, 1.58, z_rib), bevel=0.025),
            make_beveled_box((6.38, 0.18, 0.20), center=(0.0, 3.06, z_rib), bevel=0.025),
            transform_geom(make_beveled_box((0.66, 0.16, 0.20), bevel=0.02), translate=(-2.84, 2.82, z_rib), rot_xyz_deg=(0.0, 0.0, 45.0)),
            transform_geom(make_beveled_box((0.66, 0.16, 0.20), bevel=0.02), translate=(2.84, 2.82, z_rib), rot_xyz_deg=(0.0, 0.0, -45.0)),
        ])
    add_part(sm, "Room04_OctagonalGunmetalRibsAndWalls", merge_geometries(gunmetal_parts), mats["gunmetal"])

    white_coffers = []
    for z_cof in [-2.70, -0.90, 0.90, 2.70]:
        white_coffers.append(make_beveled_box((4.96, 0.05, 1.52), center=(0.0, 3.12, z_cof), bevel=0.015))
    add_part(sm, "Room04_SterileAerospaceWhiteCoffers", merge_geometries(white_coffers), mats["aero_white"])

    steel_parts = [
        make_beveled_box((0.12, 0.05, 7.34), center=(3.15, 0.98, 0.0), bevel=0.01),
        make_beveled_box((0.12, 0.05, 7.34), center=(-3.15, 0.98, 0.0), bevel=0.01),
        make_portal_oct_ring(4.44, 1.54, center_y=1.70, z_pos=-3.67, tube_r=0.032, chamfer=0.22),
        make_beveled_box((0.06, 1.50, 0.14), center=(-0.74, 1.70, -3.68), bevel=0.012),
        make_beveled_box((0.06, 1.50, 0.14), center=(0.74, 1.70, -3.68), bevel=0.012),
    ]
    for z_strip in [-2.70, -0.90, 0.90, 2.70]:
        steel_parts.append(make_beveled_box((6.24, 0.010, 0.06), center=(0.0, 0.062, z_strip), bevel=0.002))
    add_part(sm, "Room04_MachinedSteelBezelsAndStrips", merge_geometries(steel_parts), mats["steel_machined"])

    ice_parts = [
        make_beveled_box((1.80, 0.025, 1.80), center=(0.0, 3.08, -1.65), bevel=0.005),
    ]
    add_part(sm, "Room04_SurgicalIceWhiteTheaterHalo", merge_geometries(ice_parts), mats["led_ice"])

    cyan_parts = [
        make_beveled_box((0.05, 0.03, 7.00), center=(-2.60, 2.98, 0.0), bevel=0.005),
        make_beveled_box((0.05, 0.03, 7.00), center=(2.60, 2.98, 0.0), bevel=0.005),
        make_beveled_box((4.30, 0.024, 0.04), center=(0.0, 0.96, -3.65), bevel=0.004),
    ]
    add_part(sm, "Room04_OrbitalCyanCovesAndWindowRim", merge_geometries(cyan_parts), mats["led_cyan"])

    uv_parts = [
        make_beveled_box((0.04, 0.014, 7.00), center=(-1.45, 0.063, 0.0), bevel=0.003),
        make_beveled_box((0.04, 0.014, 7.00), center=(1.45, 0.063, 0.0), bevel=0.003),
    ]
    add_part(sm, "Room04_UVVioletBioDeconPerimeterStrips", merge_geometries(uv_parts), mats["led_uv"])

    # North 3-Panel Deep-Space Viewport Translucent Glass (alphaMode: BLEND)
    north_glass = make_quad_panel((-2.18, 0.96, -3.69), (2.18, 0.96, -3.69), (2.18, 2.44, -3.69), (-2.18, 2.44, -3.69))
    add_part(sm, "Room04_NorthDeepSpaceTranslucentGlass", north_glass, mats["glass_sterile"])

    primary_p = os.path.join(ROOMS_GLB_DIR, "room_04_shell.glb")
    info = center_and_export_glb(primary_p, sm, root_name="Room04_MedBayShell")
    alias_paths = [
        os.path.join(ROOMS_GLB_DIR, "room_04_medbay_shell.glb"),
        os.path.join(ROOMS_GLB_DIR, "room_04_med_bay_shell.glb"),
        "/workspace/game-project/assets/glb/room_04_shell.glb",
        "/workspace/game-project/assets/glb/room_04_medbay_shell.glb",
        "/workspace/game-project/assets/glb/room_04_med_bay_shell.glb",
    ]
    for ap in alias_paths:
        shutil.copyfile(primary_p, ap)
    print(f"[room_04_shell] Exported {primary_p} + 5 alias paths ({info['triangles']} tris)")
    return info


def build_all_medbay_round1():
    mats = get_medbay_materials()
    builders = [
        build_01_octagonal_autodoc_ring_scanner,
        build_02_dual_zone_split_autodoc_pharmacy_tower,
        build_03_ceiling_cantilever_trauma_bay,
        build_04_cryo_stasis_toroidal_mri_gantry,
        build_05_zerog_gimbaled_surgical_cradle,
    ]
    results = []
    for fn in builders:
        info = fn(mats)
        fname = os.path.basename(info["filepath"])
        dims = info["dimensions"]
        print(
            f"[medbay_r1] Built {fname:24s} | {dims[0]:.2f}m W x {dims[2]:.2f}m D x {dims[1]:.2f}m H | "
            f"verts={info['vertices']:4d} | tris={info['triangles']:4d} | min_y={info['min'][1]:.5f}"
        )
        results.append(info)

    with open(os.path.join(OUT_GLB_DIR, "medbay_r1_manifest.json"), "w") as f:
        json.dump(results, f, indent=2)

    build_room_04_med_bay_shell(mats)
    return results


if __name__ == "__main__":
    build_all_medbay_round1()
