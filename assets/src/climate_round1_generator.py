#!/usr/bin/env python3
"""
Builds all 5 Round-1 Hard Sci-Fi Personal Climate & Life-Support Wall Panel .glb models:
/workspace/game-project/assets/glb/climate_round1/climate_r1_01.glb .. climate_r1_05.glb

Follows /workspace/game-project/design/climate_round1/climate_r1_spec.md ("Aegis-7 Standard"):
- Bottom-center (0.0, 0.0, 0.0) floor pivot (min_y == 0.0000, centered X and Z) on a 0.52m dark-titanium wainscot plinth
- Active recessed environmental & emergency O2 control station spanning Y = 0.52m to Y = 1.92m, facing +Z
- Polygon budget: 2,500 - 5,000 triangles per candidate
- Mapped cleanly to Sloane's 10 textures in /workspace/game-project/assets/textures/climate_round1/
- Mandatory 4-Part 3D Life-Support & Emergency O2 Kit inside every candidate:
  1. 45° Chamfered Bulkhead Housing & 3D Laminar Air-Diffuser Louvers backed by UV-violet (#7B5CFF) ionizer glow
  2. Spin-Gravity / Coriolis & Atmospheric OLED Telemetry (oled_climate_telemetry.png) + Tactile Capacitive
     Slider Panel (oled_circadian_sliders.png) + 3D Machined-Steel Rotary Vernier Dials & Guarded Toggles
  3. Translucent Emergency O2 Breather-Mask Bay (glass_o2_bay_translucent.png, alphaMode: "BLEND", alpha ~ 0.18)
     housing Two 3D Molded Orbital Breather Masks on hooks, coiled hoses, Twin High-Pressure Emergency O2 Cylinders
     with signal-orange valves, and a Signal-Orange Manual Hull-Breach Pull Lever / Isolation Valve
  4. Replaceable Zeolite CO2 Scrubber Cartridges & Machined-Steel Pressure Manifold with glowing status rings
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
)

TEX_CLIMATE_DIR = "/workspace/game-project/assets/textures/climate_round1"
OUT_GLB_DIR = "/workspace/game-project/assets/glb/climate_round1"
os.makedirs(OUT_GLB_DIR, exist_ok=True)


def tex_cl(fname: str) -> str:
    return os.path.join(TEX_CLIMATE_DIR, fname)


def get_climate_materials():
    return {
        "gunmetal": PBRMaterialDef(
            name="Mat_Titanium_GunmetalHull",
            base_color=hex_rgba("#1A1E24"),
            metallic=0.78,
            roughness=0.34,
            texture_path=tex_cl("titanium_gunmetal_hull.png"),
        ),
        "aero_white": PBRMaterialDef(
            name="Mat_Composite_AerospaceWhite",
            base_color=hex_rgba("#D8DEE6"),
            metallic=0.08,
            roughness=0.28,
            texture_path=tex_cl("composite_aerospace_white.png"),
        ),
        "carbon_slate": PBRMaterialDef(
            name="Mat_Carbon_SlateFrame",
            base_color=hex_rgba("#282E38"),
            metallic=0.58,
            roughness=0.40,
            texture_path=tex_cl("carbon_slate_frame.png"),
        ),
        "steel_machined": PBRMaterialDef(
            name="Mat_Steel_MachinedGantry",
            base_color=hex_rgba("#88929E"),
            metallic=0.90,
            roughness=0.22,
            texture_path=tex_cl("steel_machined_gantry.png"),
        ),
        "pad_charcoal": PBRMaterialDef(
            name="Mat_Fabric_CharcoalFlightpad",
            base_color=hex_rgba("#242932"),
            metallic=0.02,
            roughness=0.78,
            texture_path=tex_cl("fabric_charcoal_flightpad.png"),
        ),
        "pad_navy": PBRMaterialDef(
            name="Mat_Fabric_OrbitalNavyPad",
            base_color=hex_rgba("#1D2C3C"),
            metallic=0.02,
            roughness=0.76,
            texture_path=tex_cl("fabric_orbital_navy_pad.png"),
        ),
        "accent_orange": PBRMaterialDef(
            name="Mat_Accent_SignalOrange",
            base_color=hex_rgba("#D95B26"),
            metallic=0.06,
            roughness=0.48,
            texture_path=tex_cl("accent_signal_orange.png"),
        ),
        "oled_telemetry": PBRMaterialDef(
            name="Mat_OLED_ClimateTelemetry",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.10,
            roughness=0.14,
            emissive=(0.35, 0.90, 1.0),
            texture_path=tex_cl("oled_climate_telemetry.png"),
        ),
        "oled_sliders": PBRMaterialDef(
            name="Mat_OLED_CircadianSliders",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.10,
            roughness=0.14,
            emissive=(0.32, 0.85, 1.0),
            texture_path=tex_cl("oled_circadian_sliders.png"),
        ),
        "glass_o2": PBRMaterialDef(
            name="Mat_Glass_O2Bay_Translucent",
            base_color=(0.55, 0.88, 1.0, 0.18),
            metallic=0.10,
            roughness=0.08,
            emissive=(0.0, 0.14, 0.22),
            texture_path=tex_cl("glass_o2_bay_translucent.png"),
            double_sided=True,
            alpha_mode="BLEND",
        ),
        "led_uv": PBRMaterialDef(
            name="Mat_Emissive_UVIonizerLED",
            base_color=hex_rgba("#7B5CFF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.55, 0.38, 1.0),
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
    }


# ==============================================================================
# SHARED 4-PART 3D LIFE-SUPPORT & EMERGENCY O2 KIT HELPERS
# ==============================================================================
def make_laminar_louvers(
    cx: float = 0.0,
    cy: float = 1.66,
    cz: float = 0.06,
    width_x: float = 0.72,
    height_y: float = 0.26,
    num_blades: int = 6,
):
    """
    Builds Part 1: 3D Angled Laminar-Flow Air-Diffuser Louver Vanes + UV-Violet (#7B5CFF) Ionizer Strip.
    Returns: (carbon_slate_louvers_geom, uv_ionizer_bar_geom)
    """
    blades = []
    y0 = cy - height_y * 0.44
    y1 = cy + height_y * 0.44
    for i in range(num_blades):
        t = i / max(1, num_blades - 1)
        by = y0 + t * (y1 - y0)
        blades.append(
            transform_geom(
                make_beveled_box((width_x, 0.016, 0.055), center=(0.0, 0.0, 0.0), bevel=0.004),
                translate=(cx, by, cz),
                rot_xyz_deg=(24.0, 0.0, 0.0),
            )
        )
    uv_bar = make_beveled_box((width_x * 0.92, 0.028, 0.03), center=(cx, cy, cz - 0.04), bevel=0.005)
    return merge_geometries(blades), uv_bar


def make_emergency_o2_breather_kit(
    bay_cx: float = 0.0,
    bay_cy: float = 0.80,
    bay_cz: float = 0.02,
    bay_w: float = 0.48,
    bay_h: float = 0.44,
    vertical_layout: bool = False,
):
    """
    Builds Part 3: 3D Stowed Emergency O2 Breather-Mask Kit inside the translucent O2 Bay:
    - Two 3D Molded Orbital Emergency Breather Masks (white oro-nasal cones, charcoal straps, orange demand valves)
    - Coiled/looped 3D oxygen feed hoses hanging on machined-steel hooks
    - Twin High-Pressure Emergency O2 Cylinders with signal-orange regulator collars
    - Signal-orange Manual Hull-Breach / Depressurization Pull T-Handle
    - Stowed Orbital-Navy Emergency Thermal Hood Pouch
    Returns: (white_liner_masks_tanks_geom, charcoal_straps_hoses_geom, navy_pouch_geom,
              steel_hooks_pipes_geom, orange_valves_handle_geom, cyan_bay_led_geom)
    """
    white_parts = [
        # Bright aerospace-white inner bay backplate so the 3D masks & cylinders pop behind translucent glass
        make_beveled_box((bay_w, bay_h, 0.025), center=(bay_cx, bay_cy, bay_cz - 0.08), bevel=0.008),
    ]
    charcoal_parts = []
    navy_parts = []
    steel_parts = []
    orange_parts = []

    if vertical_layout:
        # Used for Candidate #02's tall Right Emergency O2 Tower (bay_h ~ 1.24m)
        mask_positions = [(bay_cx - 0.06, bay_cy + 0.36), (bay_cx + 0.06, bay_cy + 0.14)]
        tank_positions = [(bay_cx - 0.065, bay_cy - 0.32), (bay_cx + 0.065, bay_cy - 0.32)]
        pouch_pos = (bay_cx, bay_cy - 0.05)
        handle_pos = (bay_cx, bay_cy - 0.52)
    else:
        # Horizontal / compact lower bay layout
        mask_positions = [(bay_cx - bay_w * 0.28, bay_cy + 0.06), (bay_cx - bay_w * 0.04, bay_cy + 0.06)]
        tank_positions = [(bay_cx + bay_w * 0.20, bay_cy - 0.02), (bay_cx + bay_w * 0.36, bay_cy - 0.02)]
        pouch_pos = (bay_cx - bay_w * 0.16, bay_cy - 0.12)
        handle_pos = (bay_cx + bay_w * 0.28, bay_cy + 0.15)

    # 1. Two 3D Molded Breather Masks + Coiled Hoses + Steel Hooks
    for mx, my in mask_positions:
        mz = bay_cz + 0.01
        # Sculpted white oro-nasal mask cone
        white_parts.append(
            transform_geom(
                make_sculpted_cushion((0.11, 0.12, 0.09), res=(5, 4, 4), roundness=0.46, belly_puff=0.06, pinch_corners=0.15, crease_freq=0),
                translate=(mx, my, mz),
                rot_xyz_deg=(10.0, 0.0, 0.0),
            )
        )
        # Signal-orange front demand regulator valve
        orange_parts.append(make_cylinder(0.024, 0.020, 0.032, center=(mx, my - 0.01, mz + 0.045), segments=10, axis="z"))
        # Charcoal elastic head-strap harness
        strap_pts = sample_filleted_polyline(
            [(mx - 0.045, my + 0.02, mz), (mx - 0.05, my + 0.08, mz - 0.04), (mx + 0.05, my + 0.08, mz - 0.04), (mx + 0.045, my + 0.02, mz)],
            fillet_radius=0.02,
            corner_subdivs=4,
        )
        charcoal_parts.append(make_swept_tube(strap_pts, radius=0.008, radial_segments=8))
        # Looped 3D oxygen feed hose
        hose_pts = sample_filleted_polyline(
            [(mx, my - 0.03, mz + 0.03), (mx - 0.04, my - 0.14, mz + 0.04), (mx + 0.04, my - 0.14, mz - 0.02), (mx + 0.05, my - 0.04, mz - 0.05)],
            fillet_radius=0.035,
            corner_subdivs=5,
        )
        charcoal_parts.append(make_swept_tube(hose_pts, radius=0.010, radial_segments=8))
        # Machined steel wall hook
        steel_parts.append(make_beveled_box((0.02, 0.04, 0.05), center=(mx, my + 0.08, mz - 0.05), bevel=0.004))

    # 2. Twin High-Pressure Emergency O2 Cylinders + Signal-Orange Valves
    for tx, ty in tank_positions:
        tz = bay_cz - 0.01
        white_parts.append(make_cylinder(0.038, 0.038, 0.24, center=(tx, ty, tz), segments=12, axis="y"))
        orange_parts.append(make_cylinder(0.024, 0.032, 0.045, center=(tx, ty + 0.135, tz), segments=10, axis="y"))
        steel_parts.append(make_beveled_box((0.09, 0.024, 0.05), center=(tx, ty, tz + 0.01), bevel=0.004))

    # 3. Stowed Orbital-Navy Thermal Hood Pouch
    px, py = pouch_pos
    navy_parts.append(
        make_sculpted_cushion((0.18, 0.09, 0.07), center=(px, py, bay_cz - 0.01), res=(5, 3, 3), roundness=0.38, belly_puff=0.04, crease_freq=0)
    )

    # 4. Signal-Orange Manual Hull-Breach Pull T-Handle
    hx, hy = handle_pos
    orange_parts.append(make_beveled_box((0.11, 0.028, 0.032), center=(hx, hy, bay_cz + 0.03), bevel=0.006))
    steel_parts.append(make_cylinder(0.010, 0.010, 0.06, center=(hx, hy, bay_cz), segments=8, axis="z"))

    # 5. Internal Cyan Bay Illumination Strip
    cyan_led = make_beveled_box((bay_w * 0.88, 0.022, 0.03), center=(bay_cx, bay_cy + bay_h * 0.45, bay_cz + 0.02), bevel=0.004)

    return (
        merge_geometries(white_parts),
        merge_geometries(charcoal_parts),
        merge_geometries(navy_parts),
        merge_geometries(steel_parts),
        merge_geometries(orange_parts),
        cyan_led,
    )


def make_zeolite_co2_scrubber_manifold(
    cx: float = -0.18,
    cy: float = 0.72,
    cz: float = 0.03,
):
    """
    Builds Part 4: Replaceable Zeolite CO2 Scrubber Cartridges & Machined-Steel Pressure Manifold.
    Returns: (white_scrubbers_geom, steel_manifold_geom, orange_valve_geom, cyan_status_rings_geom)
    """
    scrubbers = [
        make_cylinder(0.044, 0.044, 0.24, center=(cx - 0.08, cy, cz), segments=14, axis="y"),
        make_cylinder(0.044, 0.044, 0.24, center=(cx + 0.08, cy, cz), segments=14, axis="y"),
    ]
    pipe_pts = sample_filleted_polyline(
        [(cx - 0.16, cy + 0.15, cz - 0.02), (cx - 0.08, cy + 0.15, cz + 0.03), (cx + 0.08, cy + 0.15, cz + 0.03), (cx + 0.16, cy + 0.15, cz - 0.02)],
        fillet_radius=0.03,
        corner_subdivs=4,
    )
    steel_manifold = [
        make_swept_tube(pipe_pts, radius=0.016, radial_segments=10),
        make_cylinder(0.048, 0.048, 0.03, center=(cx - 0.08, cy + 0.11, cz), segments=14, axis="y"),
        make_cylinder(0.048, 0.048, 0.03, center=(cx + 0.08, cy + 0.11, cz), segments=14, axis="y"),
        make_cylinder(0.048, 0.048, 0.03, center=(cx - 0.08, cy - 0.11, cz), segments=14, axis="y"),
        make_cylinder(0.048, 0.048, 0.03, center=(cx + 0.08, cy - 0.11, cz), segments=14, axis="y"),
    ]
    orange_valve = make_cylinder(0.032, 0.032, 0.025, center=(cx, cy + 0.15, cz + 0.045), segments=10, axis="z")
    cyan_rings = [
        make_cylinder(0.046, 0.046, 0.016, center=(cx - 0.08, cy, cz), segments=14, axis="y"),
        make_cylinder(0.046, 0.046, 0.016, center=(cx + 0.08, cy, cz), segments=14, axis="y"),
    ]
    return merge_geometries(scrubbers), merge_geometries(steel_manifold), orange_valve, merge_geometries(cyan_rings)


def make_rotary_verniers_and_fader_caps(cx: float, cy: float, cz: float):
    """Builds 3 sculpted machined-steel rotary vernier dials & 4 physical fader caps."""
    parts = []
    for k in range(3):
        ky = cy + (k - 1) * 0.09
        parts.append(make_cylinder(0.026, 0.022, 0.028, center=(cx, ky, cz), segments=12, axis="z"))
        parts.append(make_beveled_box((0.010, 0.036, 0.032), center=(cx, ky, cz + 0.004), bevel=0.002))
    return merge_geometries(parts)


# ==============================================================================
# CANDIDATE 01: RECESSED OCTAGONAL BULKHEAD LIFE-SUPPORT & O2 STATION (`climate_r1_01.glb`)
# Dimensions: 0.90m W x 0.30m D x 1.90m H
# ==============================================================================
def build_01_octagonal_lifesupport_station(mats):
    sm = []
    # 1. Lower Wainscot Plinth (Y = 0.00..0.52m) & 45° Chamfered Octagonal Bulkhead Frame (Y = 0.52..1.90m)
    hull = [
        make_beveled_box((0.90, 0.52, 0.28), center=(0.0, 0.26, -0.01), bevel=0.025),
        make_beveled_box((0.90, 0.12, 0.30), center=(0.0, 1.84, 0.0), bevel=0.025),
        make_beveled_box((0.08, 1.38, 0.30), center=(-0.41, 1.21, 0.0), bevel=0.025),
        make_beveled_box((0.08, 1.38, 0.30), center=(0.41, 1.21, 0.0), bevel=0.025),
        make_beveled_box((0.84, 1.40, 0.06), center=(0.0, 1.21, -0.12), bevel=0.015),
        # Horizontal tier dividers at Y = 1.02m and Y = 1.48m
        make_beveled_box((0.76, 0.04, 0.26), center=(0.0, 1.02, 0.0), bevel=0.01),
        make_beveled_box((0.76, 0.04, 0.26), center=(0.0, 1.48, 0.0), bevel=0.01),
    ]
    add_part(sm, "Climate01_OctagonalGunmetalHull", merge_geometries(hull), mats["gunmetal"])

    # 2. Upper Tier (Y = 1.50..1.80m): 6 Angled Carbon-Slate Laminar Air-Diffuser Blades + UV-Violet Ionizer
    louvers, uv_bar = make_laminar_louvers(cx=0.0, cy=1.66, cz=0.06, width_x=0.72, height_y=0.26, num_blades=6)
    add_part(sm, "Climate01_CarbonSlateLaminarLouvers", louvers, mats["carbon_slate"])
    add_part(sm, "Climate01_UVVioletIonizerGlow", uv_bar, mats["led_uv"])

    # 3. Middle Tier (Y = 1.04..1.46m): Widescreen OLED Telemetry + Circadian Sliders + 3D Rotary Verniers
    add_part(
        sm,
        "Climate01_WidescreenOLEDTelemetry",
        make_quad_panel((-0.35, 1.07, 0.06), (0.08, 1.07, 0.06), (0.08, 1.44, 0.06), (-0.35, 1.44, 0.06)),
        mats["oled_telemetry"],
    )
    add_part(
        sm,
        "Climate01_CircadianSlidersOLED",
        make_quad_panel((0.11, 1.07, 0.06), (0.26, 1.07, 0.06), (0.26, 1.44, 0.06), (0.11, 1.44, 0.06)),
        mats["oled_sliders"],
    )

    # 4. Lower Tier (Y = 0.54..1.00m): Left Zeolite CO2 Scrubbers + Right Emergency O2 Breather Bay
    scrub_w, scrub_s, scrub_o, scrub_c = make_zeolite_co2_scrubber_manifold(cx=-0.22, cy=0.76, cz=0.04)
    o2_w, o2_ch, o2_nv, o2_st, o2_or, o2_cy = make_emergency_o2_breather_kit(
        bay_cx=0.14, bay_cy=0.76, bay_cz=0.03, bay_w=0.42, bay_h=0.42, vertical_layout=False
    )

    add_part(sm, "Climate01_WhiteMasksTanksAndScrubbers", merge_geometries([scrub_w, o2_w]), mats["aero_white"])
    add_part(sm, "Climate01_CharcoalMaskStrapsAndHoses", o2_ch, mats["pad_charcoal"])
    add_part(sm, "Climate01_NavyThermalHoodPouch", o2_nv, mats["pad_navy"])

    verniers = make_rotary_verniers_and_fader_caps(cx=0.32, cy=1.25, cz=0.07)
    bezel_ring = make_chamfered_aperture_ring(0.84, 1.34, center_y=1.21, z_pos=0.14, tube_r=0.024, chamfer=0.16)
    add_part(sm, "Climate01_MachinedVerniersAndManifold", merge_geometries([verniers, bezel_ring, scrub_s, o2_st]), mats["steel_machined"])
    add_part(sm, "Climate01_SignalOrangeValvesAndPullHandle", merge_geometries([scrub_o, o2_or]), mats["accent_orange"])

    # 5. Cyan & Amber Status LEDs + Translucent Emergency O2 Bay Door (alphaMode: "BLEND")
    add_part(sm, "Climate01_CyanStatusRingsAndBayLight", merge_geometries([scrub_c, o2_cy]), mats["led_cyan"])
    add_part(sm, "Climate01_PlinthAmberStatusLED", make_beveled_box((0.68, 0.020, 0.03), center=(0.0, 0.48, 0.14), bevel=0.004), mats["led_amber"])
    add_part(
        sm,
        "Climate01_TranslucentO2BayDoor",
        make_quad_panel((-0.06, 0.55, 0.13), (0.35, 0.55, 0.13), (0.35, 0.99, 0.13), (-0.06, 0.99, 0.13)),
        mats["glass_o2"],
    )

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "climate_r1_01.glb"), sm, root_name="ClimateR1_01_OctagonalLifesupportStation")


# ==============================================================================
# CANDIDATE 02: DUAL-ZONE SPLIT ATMOSPHERIC TELEMETRY & EMERGENCY BREATHER BAY (`climate_r1_02.glb`)
# Dimensions: 0.96m W x 0.32m D x 1.92m H (Direct Split-Bay Sibling to Locked Winners!)
# ==============================================================================
def build_02_dual_zone_split_station(mats):
    sm = []
    # 1. Asymmetric 62% / 38% Split Bulkhead Frame & Plinth (Left Bay: X=-0.48..+0.11, Right Bay: X=+0.11..+0.48)
    hull = [
        make_beveled_box((0.96, 0.52, 0.30), center=(0.0, 0.26, -0.01), bevel=0.025),
        make_beveled_box((0.96, 0.10, 0.32), center=(0.0, 1.87, 0.0), bevel=0.025),
        make_beveled_box((0.07, 1.40, 0.32), center=(-0.445, 1.22, 0.0), bevel=0.025),
        make_beveled_box((0.07, 1.40, 0.32), center=(0.445, 1.22, 0.0), bevel=0.025),
        # Center vertical structural partition at X = +0.11
        make_beveled_box((0.05, 1.36, 0.30), center=(0.11, 1.22, 0.0), bevel=0.015),
        make_beveled_box((0.90, 1.38, 0.06), center=(0.0, 1.22, -0.13), bevel=0.015),
        # Left Bay horizontal dividers at Y = 0.94m and Y = 1.52m
        make_beveled_box((0.54, 0.035, 0.28), center=(-0.16, 0.94, 0.0), bevel=0.008),
        make_beveled_box((0.54, 0.035, 0.28), center=(-0.16, 1.52, 0.0), bevel=0.008),
    ]
    add_part(sm, "Climate02_SplitBayGunmetalHull", merge_geometries(hull), mats["gunmetal"])

    # 2. Left Top (Y = 1.54..1.82m): Angled Laminar Air-Diffuser Louver Bank + UV-Violet Ionizer Strip
    louvers, uv_bar = make_laminar_louvers(cx=-0.16, cy=1.68, cz=0.06, width_x=0.48, height_y=0.24, num_blades=5)
    add_part(sm, "Climate02_LeftBayLaminarLouvers", louvers, mats["carbon_slate"])
    add_part(sm, "Climate02_LeftBayUVIonizerLED", uv_bar, mats["led_uv"])

    # 3. Left Center (Y = 0.96..1.50m): Coriolis & Gas-Mix OLED + Circadian Sliders + 3D Rotary Verniers
    add_part(
        sm,
        "Climate02_LeftCoriolisOLEDMonitor",
        make_quad_panel((-0.39, 1.18, 0.06), (0.06, 1.18, 0.06), (0.06, 1.48, 0.06), (-0.39, 1.48, 0.06)),
        mats["oled_telemetry"],
    )
    add_part(
        sm,
        "Climate02_LeftCircadianSlidersOLED",
        make_quad_panel((-0.39, 0.98, 0.06), (-0.06, 0.98, 0.06), (-0.06, 1.15, 0.06), (-0.39, 1.15, 0.06)),
        mats["oled_sliders"],
    )

    # 4. Left Bottom (Y = 0.54..0.92m): Zeolite CO2 Scrubber Cartridges + Right Full-Height Emergency O2 Tower
    scrub_w, scrub_s, scrub_o, scrub_c = make_zeolite_co2_scrubber_manifold(cx=-0.16, cy=0.73, cz=0.04)
    o2_w, o2_ch, o2_nv, o2_st, o2_or, o2_cy = make_emergency_o2_breather_kit(
        bay_cx=0.28, bay_cy=1.18, bay_cz=0.03, bay_w=0.28, bay_h=1.24, vertical_layout=True
    )

    add_part(sm, "Climate02_WhiteO2TowerAndScrubbers", merge_geometries([scrub_w, o2_w]), mats["aero_white"])
    add_part(sm, "Climate02_CharcoalMaskHarnessesAndHoses", o2_ch, mats["pad_charcoal"])
    add_part(sm, "Climate02_NavyThermalHoodPouch", o2_nv, mats["pad_navy"])

    verniers = make_rotary_verniers_and_fader_caps(cx=0.01, cy=1.06, cz=0.07)
    tower_bezel = [
        verniers,
        scrub_s,
        o2_st,
        make_beveled_box((0.28, 0.024, 0.03), center=(0.28, 1.12, 0.14), bevel=0.004),
    ]
    add_part(sm, "Climate02_MachinedVerniersAndManifold", merge_geometries(tower_bezel), mats["steel_machined"])
    add_part(sm, "Climate02_SignalOrangeValvesAndBreachLever", merge_geometries([scrub_o, o2_or]), mats["accent_orange"])

    # 5. Cyan & Amber Practical LEDs + Right Full-Height Translucent O2 Tower Door (alphaMode: "BLEND")
    cyan_all = [
        scrub_c,
        o2_cy,
        make_beveled_box((0.020, 1.24, 0.03), center=(0.40, 1.18, 0.11), bevel=0.004),
    ]
    add_part(sm, "Climate02_CyanTowerAndScrubberLED", merge_geometries(cyan_all), mats["led_cyan"])
    add_part(
        sm,
        "Climate02_AmberTowerAndPlinthLED",
        merge_geometries([
            make_beveled_box((0.26, 0.020, 0.03), center=(0.28, 0.56, 0.13), bevel=0.004),
            make_beveled_box((0.76, 0.020, 0.03), center=(0.0, 0.48, 0.14), bevel=0.004),
        ]),
        mats["led_amber"],
    )

    add_part(
        sm,
        "Climate02_RightTowerTranslucentO2Door",
        make_quad_panel((0.14, 0.55, 0.14), (0.41, 0.55, 0.14), (0.41, 1.81, 0.14), (0.14, 1.81, 0.14)),
        mats["glass_o2"],
    )

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "climate_r1_02.glb"), sm, root_name="ClimateR1_02_DualZoneSplitStation")


# ==============================================================================
# CANDIDATE 03: CYLINDRICAL VORTEX SCRUBBER & HOLO-BAROMETER COLUMN (`climate_r1_03.glb`)
# Dimensions: 0.88m W x 0.34m D x 1.92m H
# ==============================================================================
def build_03_cylindrical_vortex_column(mats):
    sm = []
    # 1. Semi-Cylindrical Gunmetal Column Housing & Wainscot Plinth
    hull = [
        make_beveled_box((0.88, 0.52, 0.32), center=(0.0, 0.26, -0.01), bevel=0.03),
        make_beveled_box((0.88, 0.12, 0.34), center=(0.0, 1.86, 0.0), bevel=0.03),
        make_beveled_box((0.09, 1.38, 0.32), center=(-0.395, 1.21, 0.0), bevel=0.035),
        make_beveled_box((0.09, 1.38, 0.32), center=(0.395, 1.21, 0.0), bevel=0.035),
        make_beveled_box((0.80, 1.40, 0.06), center=(0.0, 1.21, -0.14), bevel=0.02),
    ]
    add_part(sm, "Climate03_SemiCylindricalGunmetalColumn", merge_geometries(hull), mats["gunmetal"])

    # 2. Top Circular Radial-Blade Vortex Air-Scrubber Turbine (Y = 1.62m) + UV-Violet Core Glow
    vortex_blades = [
        make_cylinder(0.18, 0.18, 0.04, center=(0.0, 1.64, 0.06), segments=20, axis="z"),
    ]
    for k in range(8):
        ang = k * 45.0
        vortex_blades.append(
            transform_geom(
                make_beveled_box((0.30, 0.022, 0.045), center=(0.0, 0.0, 0.0), bevel=0.004),
                translate=(0.0, 1.64, 0.07),
                rot_xyz_deg=(0.0, 0.0, ang),
            )
        )
    add_part(sm, "Climate03_VortexTurbineBlades", merge_geometries(vortex_blades), mats["carbon_slate"])
    add_part(sm, "Climate03_VortexUVVioletCore", make_cylinder(0.14, 0.14, 0.03, center=(0.0, 1.64, 0.05), segments=18, axis="z"), mats["led_uv"])

    # 3. Middle Collar (Y = 1.16..1.44m): OLED Telemetry + Circadian Sliders
    add_part(
        sm,
        "Climate03_CollarOLEDTelemetry",
        make_quad_panel((-0.32, 1.16, 0.08), (0.08, 1.16, 0.08), (0.08, 1.44, 0.08), (-0.32, 1.44, 0.08)),
        mats["oled_telemetry"],
    )
    add_part(
        sm,
        "Climate03_CollarCircadianSliders",
        make_quad_panel((0.11, 1.16, 0.08), (0.32, 1.16, 0.08), (0.32, 1.44, 0.08), (0.11, 1.44, 0.08)),
        mats["oled_sliders"],
    )

    # 4. Lower Curved Bay (Y = 0.56..1.12m): Twin Breather Masks, 3 Vertical Zeolite Scrubber Rods & O2 Cylinders
    scrub_w, scrub_s, scrub_o, scrub_c = make_zeolite_co2_scrubber_manifold(cx=-0.18, cy=0.82, cz=0.04)
    o2_w, o2_ch, o2_nv, o2_st, o2_or, o2_cy = make_emergency_o2_breather_kit(
        bay_cx=0.14, bay_cy=0.82, bay_cz=0.03, bay_w=0.38, bay_h=0.50, vertical_layout=False
    )

    add_part(sm, "Climate03_WhiteMasksTanksAndScrubbers", merge_geometries([scrub_w, o2_w]), mats["aero_white"])
    add_part(sm, "Climate03_CharcoalStrapsAndHoses", o2_ch, mats["pad_charcoal"])
    add_part(sm, "Climate03_NavyHoodPouch", o2_nv, mats["pad_navy"])

    steel_all = [
        scrub_s,
        o2_st,
        make_chamfered_aperture_ring(0.76, 1.32, center_y=1.20, z_pos=0.14, tube_r=0.024, chamfer=0.18),
    ]
    add_part(sm, "Climate03_MachinedRingAndManifold", merge_geometries(steel_all), mats["steel_machined"])
    add_part(sm, "Climate03_SignalOrangeValves", merge_geometries([scrub_o, o2_or]), mats["accent_orange"])

    # 5. Cyan/Amber LEDs + Curved Translucent Mid-Chamber Door (alphaMode: "BLEND")
    add_part(sm, "Climate03_CyanStatusLED", merge_geometries([scrub_c, o2_cy]), mats["led_cyan"])
    add_part(sm, "Climate03_AmberPlinthLED", make_beveled_box((0.66, 0.020, 0.03), center=(0.0, 0.48, 0.15), bevel=0.004), mats["led_amber"])
    add_part(
        sm,
        "Climate03_TranslucentCylinderChamberDoor",
        make_quad_panel((-0.34, 0.56, 0.15), (0.34, 0.56, 0.15), (0.34, 1.12, 0.15), (-0.34, 1.12, 0.15)),
        mats["glass_o2"],
    )

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "climate_r1_03.glb"), sm, root_name="ClimateR1_03_CylindricalVortexColumn")


# ==============================================================================
# CANDIDATE 04: CANTILEVERED SMART-GLASS VITALS CONSOLE & QUICK-DROP MASK POD (`climate_r1_04.glb`)
# Dimensions: 0.92m W x 0.30m D x 1.88m H
# ==============================================================================
def build_04_cantilevered_smartglass_console(mats):
    sm = []
    # 1. Gunmetal Base Plinth & Rear Frame
    plinth = [
        make_beveled_box((0.92, 0.52, 0.28), center=(0.0, 0.26, -0.01), bevel=0.025),
        make_beveled_box((0.90, 1.38, 0.06), center=(0.0, 1.20, -0.12), bevel=0.015),
    ]
    add_part(sm, "Climate04_GunmetalPlinthAndSpine", merge_geometries(plinth), mats["gunmetal"])

    # 2. Molded Matte Aerospace-White Capsule Bulkhead Panel + Masks/Tanks/Scrubbers
    scrub_w, scrub_s, scrub_o, scrub_c = make_zeolite_co2_scrubber_manifold(cx=-0.22, cy=0.76, cz=0.04)
    o2_w, o2_ch, o2_nv, o2_st, o2_or, o2_cy = make_emergency_o2_breather_kit(
        bay_cx=0.14, bay_cy=0.76, bay_cz=0.03, bay_w=0.42, bay_h=0.42, vertical_layout=False
    )
    white_capsule = [
        make_sculpted_cushion((0.92, 0.14, 0.30), center=(0.0, 1.81, 0.0), res=(7, 3, 5), roundness=0.28, belly_puff=0.02, pinch_corners=0.0, crease_freq=0),
        make_beveled_box((0.08, 1.32, 0.28), center=(-0.42, 1.18, 0.0), bevel=0.03),
        make_beveled_box((0.08, 1.32, 0.28), center=(0.42, 1.18, 0.0), bevel=0.03),
        scrub_w,
        o2_w,
    ]
    add_part(sm, "Climate04_AerospaceWhiteCapsuleShell", merge_geometries(white_capsule), mats["aero_white"])

    # 3. Upper Laminar Louvers + UV-Violet Ionizer
    louvers, uv_bar = make_laminar_louvers(cx=0.0, cy=1.62, cz=0.06, width_x=0.72, height_y=0.22, num_blades=5)
    add_part(sm, "Climate04_CarbonSlateLouvers", louvers, mats["carbon_slate"])
    add_part(sm, "Climate04_UVIonizerBar", uv_bar, mats["led_uv"])

    # 4. OLED Telemetry & Sliders + Machined Cantilever Stand-Offs & Verniers
    add_part(
        sm,
        "Climate04_OLEDTelemetryScreen",
        make_quad_panel((-0.34, 1.06, 0.05), (0.08, 1.06, 0.05), (0.08, 1.44, 0.05), (-0.34, 1.44, 0.05)),
        mats["oled_telemetry"],
    )
    add_part(
        sm,
        "Climate04_OLEDCircadianSliders",
        make_quad_panel((0.11, 1.06, 0.05), (0.28, 1.06, 0.05), (0.28, 1.44, 0.05), (0.11, 1.44, 0.05)),
        mats["oled_sliders"],
    )

    verniers = make_rotary_verniers_and_fader_caps(cx=0.33, cy=1.25, cz=0.06)
    standoffs = [
        verniers,
        scrub_s,
        o2_st,
        make_cylinder(0.012, 0.012, 0.10, center=(-0.32, 1.42, 0.09), segments=8, axis="z"),
        make_cylinder(0.012, 0.012, 0.10, center=(0.32, 1.42, 0.09), segments=8, axis="z"),
    ]
    add_part(sm, "Climate04_MachinedStandoffsAndVerniers", merge_geometries(standoffs), mats["steel_machined"])
    add_part(sm, "Climate04_CharcoalMaskHoses", o2_ch, mats["pad_charcoal"])
    add_part(sm, "Climate04_NavyHoodPouch", o2_nv, mats["pad_navy"])
    add_part(sm, "Climate04_SignalOrangeLanyardsAndValves", merge_geometries([scrub_o, o2_or]), mats["accent_orange"])

    # 5. Cyan/Amber LEDs + Cantilevered Floating Translucent HUD Overlay & Quick-Drop O2 Door (alphaMode: "BLEND")
    add_part(sm, "Climate04_CyanStatusLED", merge_geometries([scrub_c, o2_cy]), mats["led_cyan"])
    add_part(sm, "Climate04_AmberPlinthLED", make_beveled_box((0.70, 0.020, 0.03), center=(0.0, 0.48, 0.14), bevel=0.004), mats["led_amber"])

    glass_parts = [
        make_quad_panel((-0.35, 1.04, 0.13), (0.35, 1.04, 0.13), (0.35, 1.46, 0.13), (-0.35, 1.46, 0.13)),
        make_quad_panel((-0.06, 0.54, 0.13), (0.36, 0.54, 0.13), (0.36, 0.98, 0.13), (-0.06, 0.98, 0.13)),
    ]
    add_part(sm, "Climate04_FloatingHUDAndQuickDropGlass", merge_geometries(glass_parts), mats["glass_o2"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "climate_r1_04.glb"), sm, root_name="ClimateR1_04_CantileveredSmartGlassConsole")


# ==============================================================================
# CANDIDATE 05: HEAVY PRESSURE-BULKHEAD DAMPER & TACTICAL O2 MANIFOLD (`climate_r1_05.glb`)
# Dimensions: 0.95m W x 0.32m D x 1.92m H
# ==============================================================================
def build_05_pressure_damper_manifold(mats):
    sm = []
    # 1. Armored Pressure-Bulkhead Frame & Wainscot Plinth
    hull = [
        make_beveled_box((0.95, 0.52, 0.30), center=(0.0, 0.26, -0.01), bevel=0.025),
        make_beveled_box((0.95, 0.12, 0.32), center=(0.0, 1.86, 0.0), bevel=0.025),
        make_beveled_box((0.08, 1.40, 0.32), center=(-0.435, 1.22, 0.0), bevel=0.025),
        make_beveled_box((0.08, 1.40, 0.32), center=(0.435, 1.22, 0.0), bevel=0.025),
        make_beveled_box((0.88, 1.40, 0.06), center=(0.0, 1.22, -0.13), bevel=0.015),
        make_beveled_box((0.80, 0.04, 0.28), center=(0.0, 1.02, 0.0), bevel=0.01),
        make_beveled_box((0.80, 0.04, 0.28), center=(0.0, 1.50, 0.0), bevel=0.01),
    ]
    add_part(sm, "Climate05_ArmoredPressureBulkheadHull", merge_geometries(hull), mats["gunmetal"])

    # 2. Upper Motorized Butterfly Air-Damper Blades + UV-Violet Ionizer Glow
    louvers, uv_bar = make_laminar_louvers(cx=0.0, cy=1.66, cz=0.05, width_x=0.74, height_y=0.24, num_blades=6)
    add_part(sm, "Climate05_MotorizedDamperBlades", louvers, mats["carbon_slate"])
    add_part(sm, "Climate05_DamperUVIonizerGlow", uv_bar, mats["led_uv"])

    # 3. Dual Side-by-Side OLED Telemetry & Sliders
    add_part(
        sm,
        "Climate05_OLEDTelemetry",
        make_quad_panel((-0.36, 1.07, 0.06), (0.04, 1.07, 0.06), (0.04, 1.45, 0.06), (-0.36, 1.45, 0.06)),
        mats["oled_telemetry"],
    )
    add_part(
        sm,
        "Climate05_OLEDSliders",
        make_quad_panel((0.08, 1.07, 0.06), (0.25, 1.07, 0.06), (0.25, 1.45, 0.06), (0.08, 1.45, 0.06)),
        mats["oled_sliders"],
    )

    # 4. Lower Tactical O2 Manifold, Sculpted Signal-Orange 4-Spoke Rotary Isolation Handwheel & Emergency O2 Locker
    scrub_w, scrub_s, scrub_o, scrub_c = make_zeolite_co2_scrubber_manifold(cx=-0.22, cy=0.76, cz=0.04)
    o2_w, o2_ch, o2_nv, o2_st, o2_or, o2_cy = make_emergency_o2_breather_kit(
        bay_cx=0.15, bay_cy=0.76, bay_cz=0.03, bay_w=0.40, bay_h=0.42, vertical_layout=False
    )

    add_part(sm, "Climate05_WhiteMasksTanksAndScrubbers", merge_geometries([scrub_w, o2_w]), mats["aero_white"])
    add_part(sm, "Climate05_CharcoalStrapsAndHoses", o2_ch, mats["pad_charcoal"])
    add_part(sm, "Climate05_NavyHoodPouch", o2_nv, mats["pad_navy"])

    verniers = make_rotary_verniers_and_fader_caps(cx=0.33, cy=1.25, cz=0.07)
    add_part(sm, "Climate05_MachinedCrossFeedPipesAndVerniers", merge_geometries([verniers, scrub_s, o2_st]), mats["steel_machined"])

    # Sculpted 4-spoke rotary O2 isolation handwheel on left manifold
    wheel_pts = []
    for k in range(17):
        ang = (k / 16.0) * 2.0 * math.pi
        wheel_pts.append([-0.22 + 0.075 * math.cos(ang), 0.76 + 0.075 * math.sin(ang), 0.13])
    handwheel = [
        scrub_o,
        o2_or,
        make_swept_tube(np.array(wheel_pts, dtype=np.float32), radius=0.012, radial_segments=8, closed_loop=True),
        make_beveled_box((0.14, 0.020, 0.020), center=(-0.22, 0.76, 0.13), bevel=0.004),
        make_beveled_box((0.020, 0.14, 0.020), center=(-0.22, 0.76, 0.13), bevel=0.004),
    ]
    add_part(sm, "Climate05_SignalOrangeRotaryHandwheel", merge_geometries(handwheel), mats["accent_orange"])

    # 5. Cyan/Amber LEDs + Translucent Damper Window & Lower O2 Locker Door (alphaMode: "BLEND")
    add_part(sm, "Climate05_CyanStatusLED", merge_geometries([scrub_c, o2_cy]), mats["led_cyan"])
    add_part(sm, "Climate05_AmberPlinthLED", make_beveled_box((0.72, 0.020, 0.03), center=(0.0, 0.48, 0.14), bevel=0.004), mats["led_amber"])

    glass_windows = [
        make_quad_panel((-0.36, 1.53, 0.14), (0.36, 1.53, 0.14), (0.36, 1.79, 0.14), (-0.36, 1.79, 0.14)),
        make_quad_panel((-0.05, 0.55, 0.14), (0.36, 0.55, 0.14), (0.36, 0.99, 0.14), (-0.05, 0.99, 0.14)),
    ]
    add_part(sm, "Climate05_TranslucentDamperAndO2Doors", merge_geometries(glass_windows), mats["glass_o2"])

    return center_and_export_glb(os.path.join(OUT_GLB_DIR, "climate_r1_05.glb"), sm, root_name="ClimateR1_05_PressureDamperManifold")


def build_all_climate_round1():
    mats = get_climate_materials()
    builders = [
        build_01_octagonal_lifesupport_station,
        build_02_dual_zone_split_station,
        build_03_cylindrical_vortex_column,
        build_04_cantilevered_smartglass_console,
        build_05_pressure_damper_manifold,
    ]
    results = []
    for fn in builders:
        info = fn(mats)
        fname = os.path.basename(info["filepath"])
        dims = info["dimensions"]
        print(
            f"[climate_r1] Built {fname:18s} | {dims[0]:.2f}m W x {dims[2]:.2f}m D x {dims[1]:.2f}m H | "
            f"verts={info['vertices']:4d} | tris={info['triangles']:4d} | min_y={info['min'][1]:.5f}"
        )
        results.append(info)
    with open(os.path.join(OUT_GLB_DIR, "climate_r1_manifest.json"), "w") as f:
        json.dump(results, f, indent=2)
    return results


if __name__ == "__main__":
    build_all_climate_round1()
