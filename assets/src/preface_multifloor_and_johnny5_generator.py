#!/usr/bin/env python3
"""
Builds and validates the complete Phase 6B Multi-Floor Playable Preface Residential Sector,
Promoted #04 Bio-Luminescent Neural Tendon Wrist Rig + Upgrade Pickups, Expressive WALL-E /
Johnny-5 Companion Robots (4 Faction Liveries), and Interactive PCBA ("I Spy" RESET Pin) +
Python (`def open_door(amperage):`) Door Terminal .glb Suite.

Owner: Rook (3D Modeling Specialist)
Specs:
  - `/workspace/game-project/design/preface_playable_residential_sector_spec.md` (Vance)
  - `/workspace/game-project/design/sloane_preface_and_wrist_textures_spec.md` (Sloane Section 4)
"""
import os
import sys
import io
import math
import json
import shutil
from typing import Dict, List, Tuple, Optional
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glb_builder import (
    transform_geom,
    merge_geometries,
    make_lathe_dome,
    sample_filleted_polyline,
    make_swept_tube,
    make_beveled_box,
    make_cylinder,
)
from bunk_round1_generator import hex_rgba
from buildings_exteriors_generator import (
    make_chamfered_oct_prism,
    make_closed_torus_ring,
    make_botanical_cluster,
)
from character_aegis7_crew_generator import (
    euler_xyz_deg_to_quat_xyzw,
    make_lathe_limb,
    make_joint_ball,
)
from preface_and_wrist_rfid_generator import (
    TEX_DIR,
    GODOT_MODELS_DIR,
    ASSETS_GLB_DIR,
    WINNERS_DIR,
    WRIST_DIRS,
    ENV_DIRS,
    DOOR_DIRS,
    CHAR_DIRS,
    tex_path,
    remap_uv,
    RichPBRMaterial,
    RichPartBucket,
    export_hierarchy_with_animations_glb,
)


def world_box_uv(
    geom: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    scale_m: float = 2.5,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Computes consistent real-world meter-scaled box-projected UVs in [0, 1] so large walls/floors never stretch."""
    p, n, u, idx = geom
    uv = np.zeros_like(u, dtype=np.float32)
    an = np.abs(n)
    for i in range(len(p)):
        nx, ny, nz = an[i]
        px, py, pz = p[i]
        if ny >= nx and ny >= nz:
            u_raw, v_raw = px / scale_m, pz / scale_m
        elif nx >= ny and nx >= nz:
            u_raw, v_raw = pz / scale_m, py / scale_m
        else:
            u_raw, v_raw = px / scale_m, py / scale_m
        uv[i, 0] = 0.04 + (u_raw - math.floor(u_raw)) * 0.92
        uv[i, 1] = 0.04 + (v_raw - math.floor(v_raw)) * 0.92
    return p, n, uv, idx

PICKUP_DIRS = [
    os.path.join(GODOT_MODELS_DIR, "props/pickups"),
    os.path.join(ASSETS_GLB_DIR, "props/pickups"),
    os.path.join(GODOT_MODELS_DIR, "props/wrist_rfid"),
    os.path.join(ASSETS_GLB_DIR, "props/wrist_rfid"),
]
PCBA_DIRS = [
    os.path.join(GODOT_MODELS_DIR, "props/service_door"),
    os.path.join(GODOT_MODELS_DIR, "props/pcba_terminal"),
    os.path.join(ASSETS_GLB_DIR, "props/service_door"),
    os.path.join(ASSETS_GLB_DIR, "props/pcba_terminal"),
]
for d in PICKUP_DIRS + PCBA_DIRS:
    os.makedirs(d, exist_ok=True)


# ==============================================================================
# MATERIAL LIBRARIES (SLOANE PHASE 6B ATLAS SUITES)
# ==============================================================================
def get_phase6b_materials() -> Dict[str, RichPBRMaterial]:
    # 1. Wrist Winner #04 + Super-Wire Spool + BCI Headband Atlas (`512x512`)
    w4_alb = tex_path("wrist_rfid_winner_04_neural_tendon_and_bci_atlas_albedo.png")
    w4_orm = tex_path("wrist_rfid_winner_04_neural_tendon_and_bci_atlas_orm.png")
    w4_nrm = tex_path("wrist_rfid_winner_04_neural_tendon_and_bci_atlas_normal.png")
    w4_emi = tex_path("wrist_rfid_winner_04_neural_tendon_and_bci_atlas_emission.png")
    w_holo = tex_path("wrist_rfid_holo_translucent.png")

    # 2. Residential Atrium, Top-Floor Apartment & Pickups Atlas (`512x512`)
    res_alb = tex_path("residential_atrium_and_apartment_atlas_albedo.png")
    res_orm = tex_path("residential_atrium_and_apartment_atlas_orm.png")
    res_nrm = tex_path("residential_atrium_and_apartment_atlas_normal.png")
    res_emi = tex_path("residential_atrium_and_apartment_atlas_emission.png")
    res_gls = tex_path("residential_atrium_glass_translucent.png")

    # 3. Johnny-5 / WALL-E Expressive Utility Bot Atlas (`512x512`)
    j5_alb = tex_path("johnny5_utility_bot_atlas_albedo.png")
    j5_orm = tex_path("johnny5_utility_bot_atlas_orm.png")
    j5_nrm = tex_path("johnny5_utility_bot_atlas_normal.png")
    j5_emi = tex_path("johnny5_utility_bot_atlas_emission.png")
    j5_gls = tex_path("johnny5_optic_lens_translucent.png")

    # 4. Door Troubleshooting PCBA + Python UI Atlas (`1024x1024` & `512x512`)
    ui_alb = tex_path("door_troubleshooting_pcba_and_python_ui_albedo.png")
    ui_orm = tex_path("door_troubleshooting_pcba_and_python_ui_orm.png")
    ui_nrm = tex_path("door_troubleshooting_pcba_and_python_ui_normal.png")
    ui_emi = tex_path("door_troubleshooting_pcba_and_python_ui_emission.png")
    pcba_panel = tex_path("ui_pcba_circuit_board_panel.png")
    py_panel = tex_path("ui_python_code_editor_panel.png")

    return {
        "wrist04_atlas": RichPBRMaterial(
            name="Mat_Wrist04_NeuralTendonAndBCIAtlas",
            metallic=0.22,
            roughness=0.42,
            emissive=(0.95, 0.95, 1.0),
            albedo_tex=w4_alb,
            orm_tex=w4_orm,
            normal_tex=w4_nrm,
            emissive_tex=w4_emi,
        ),
        "wrist_holo": RichPBRMaterial(
            name="Mat_Glass_Wrist04ElastomerHolo_Translucent",
            base_color=(0.55, 0.90, 1.0, 0.35),
            metallic=0.20,
            roughness=0.08,
            emissive=(0.18, 0.72, 1.0),
            albedo_tex=w_holo,
            emissive_tex=w_holo,
            double_sided=True,
            alpha_mode="BLEND",
        ),
        "residential_atlas": RichPBRMaterial(
            name="Mat_Residential_AtriumAndApartmentAtlas",
            metallic=0.12,
            roughness=0.58,
            emissive=(0.45, 0.45, 0.48),
            albedo_tex=res_alb,
            orm_tex=res_orm,
            normal_tex=res_nrm,
            emissive_tex=res_emi,
        ),
        "residential_glass": RichPBRMaterial(
            name="Mat_Glass_ResidentialAtrium_Translucent",
            base_color=(0.58, 0.88, 1.0, 0.32),
            metallic=0.18,
            roughness=0.08,
            emissive=(0.06, 0.20, 0.30),
            albedo_tex=res_gls,
            double_sided=True,
            alpha_mode="BLEND",
        ),
        "johnny5_atlas": RichPBRMaterial(
            name="Mat_Johnny5_UtilityBotAtlas",
            metallic=0.48,
            roughness=0.34,
            emissive=(0.95, 0.95, 1.0),
            albedo_tex=j5_alb,
            orm_tex=j5_orm,
            normal_tex=j5_nrm,
            emissive_tex=j5_emi,
        ),
        "johnny5_lens": RichPBRMaterial(
            name="Mat_Glass_Johnny5OpticLens_Translucent",
            base_color=(0.50, 0.92, 1.0, 0.34),
            metallic=0.25,
            roughness=0.05,
            emissive=(0.12, 0.65, 0.95),
            albedo_tex=j5_gls,
            emissive_tex=j5_gls,
            double_sided=True,
            alpha_mode="BLEND",
        ),
        "pcba_python_atlas": RichPBRMaterial(
            name="Mat_DoorUI_PCBAAndPythonAtlas",
            metallic=0.35,
            roughness=0.30,
            emissive=(0.95, 0.98, 1.0),
            albedo_tex=ui_alb,
            orm_tex=ui_orm,
            normal_tex=ui_nrm,
            emissive_tex=ui_emi,
        ),
        "pcba_board_mat": RichPBRMaterial(
            name="Mat_PCBA_CircuitBoardPanel",
            metallic=0.40,
            roughness=0.32,
            emissive=(0.35, 0.85, 0.75),
            albedo_tex=pcba_panel,
            emissive_tex=pcba_panel,
        ),
        "python_screen_mat": RichPBRMaterial(
            name="Mat_UI_PythonCodeEditorScreen",
            metallic=0.12,
            roughness=0.16,
            emissive=(0.88, 0.95, 1.0),
            albedo_tex=py_panel,
            emissive_tex=py_panel,
        ),
        "steel_machined": RichPBRMaterial(
            name="Mat_Aegis_BrushedSteelMachined",
            base_color=hex_rgba("#88929E"),
            metallic=0.90,
            roughness=0.22,
            albedo_tex=tex_path("facade_brushed_steel_gantry.png"),
        ),
        "gunmetal_hull": RichPBRMaterial(
            name="Mat_Aegis_GunmetalTitaniumHull",
            base_color=hex_rgba("#1A1E24"),
            metallic=0.78,
            roughness=0.34,
            albedo_tex=tex_path("facade_titanium_gunmetal_hull.png"),
        ),
        "aero_white": RichPBRMaterial(
            name="Mat_Aegis_AerospaceWhiteComposite",
            base_color=hex_rgba("#D8DEE6"),
            metallic=0.12,
            roughness=0.30,
            albedo_tex=tex_path("facade_aerospace_white_cladding.png"),
        ),
        "copper_gold": RichPBRMaterial(
            name="Mat_Aegis_CopperGoldSuperconductor",
            base_color=hex_rgba("#E0A844"),
            metallic=0.92,
            roughness=0.20,
        ),
        "accent_orange": RichPBRMaterial(
            name="Mat_Aegis_SignalOrangeHardware",
            base_color=hex_rgba("#4E5662"),
            metallic=0.52,
            roughness=0.44,
        ),
        "caution_yellow": RichPBRMaterial(
            name="Mat_Aegis_CaterpillarAmberYellow",
            base_color=hex_rgba("#FFB703"),
            metallic=0.32,
            roughness=0.34,
        ),
        "janitor_teal": RichPBRMaterial(
            name="Mat_Aegis_SanitationCivicTeal",
            base_color=hex_rgba("#00B4D8"),
            metallic=0.28,
            roughness=0.32,
        ),
        "foliage_green": RichPBRMaterial(
            name="Mat_Aegis_BotanicalFoliage",
            base_color=hex_rgba("#2E8B57"),
            metallic=0.04,
            roughness=0.62,
            albedo_tex=tex_path("biome_terraced_botanical_canopy.png"),
            double_sided=True,
        ),
        "deck_slate_floor": RichPBRMaterial(
            name="Mat_Aegis_DeckSlateFloor",
            base_color=hex_rgba("#626870"),
            metallic=0.14,
            roughness=0.68,
            albedo_tex=tex_path("mat_deck_floor_albedo.png"),
        ),
        "matte_wall_cladding": RichPBRMaterial(
            name="Mat_Aegis_MatteWallCladding",
            base_color=hex_rgba("#8E949C"),
            metallic=0.08,
            roughness=0.62,
            albedo_tex=tex_path("bulkhead_wainscoting.png"),
        ),
        "warm_wood_parquet": RichPBRMaterial(
            name="Mat_Aegis_WarmWalnutWood",
            base_color=hex_rgba("#8A6A4E"),
            metallic=0.04,
            roughness=0.56,
            albedo_tex=tex_path("wood_parquet_warm.png"),
        ),
        "led_cyan": RichPBRMaterial(
            name="Mat_Emissive_CyanLED",
            base_color=hex_rgba("#2E96B2"),
            metallic=0.0,
            roughness=0.22,
            emissive=(0.18, 0.58, 0.70),
            albedo_tex=tex_path("led_cyan_strip.png"),
        ),
        "led_amber": RichPBRMaterial(
            name="Mat_Emissive_AmberLED",
            base_color=hex_rgba("#C47D2B"),
            metallic=0.0,
            roughness=0.24,
            emissive=(0.62, 0.38, 0.12),
            albedo_tex=tex_path("led_amber_strip.png"),
        ),
        "led_uv": RichPBRMaterial(
            name="Mat_Emissive_UVVioletLED",
            base_color=hex_rgba("#7B5CFF"),
            metallic=0.0,
            roughness=0.12,
            emissive=(0.58, 0.38, 1.0),
            albedo_tex=tex_path("led_uv_violet.png"),
        ),
        "led_emerald": RichPBRMaterial(
            name="Mat_Emissive_EmeraldBioLED",
            base_color=hex_rgba("#00E676"),
            metallic=0.0,
            roughness=0.12,
            emissive=(0.0, 0.95, 0.48),
        ),
        "led_fault_red": RichPBRMaterial(
            name="Mat_Emissive_FaultRedLED",
            base_color=hex_rgba("#FF3B30"),
            metallic=0.0,
            roughness=0.12,
            emissive=(1.0, 0.22, 0.16),
        ),
    }


# ==============================================================================
# PART 1: PROMOTED #04 WRIST WINNER & STANDALONE UPGRADE PICKUPS
# (`prop_wrist_rfid_winner_01_neural_tendon_sleeve.glb`, `prop_bci_headband.glb`,
#  `prop_super_wire_spool.glb`, `prop_pickup_battery_charge.glb`)
# ==============================================================================
def build_promoted_wrist_04_winner(mats: Dict[str, RichPBRMaterial]) -> Dict[str, any]:
    """
    Rebuilds & promotes #04 (`prop_wrist_rfid_r1_04.glb` -> `prop_wrist_rfid_winner_01_neural_tendon_sleeve.glb`)
    using `wrist_rfid_winner_04_neural_tendon_and_bci_atlas_*.png`:
      - Q1 (`u:0..0.5, v:0..0.5`): Dorsal skin + #00E5FF cyan & #7B5CFF violet-UV dendritic neural tendon veins
      - Q2 (`u:0.5..1, v:0..0.5`): Flexible polymer carbon-weave smart-sleeve + 5-bar cyan/violet battery charge gauge
      - Q3 (`u:0..0.5, v:0.5..1`): Integrated Carpal Super-Wire Spool (`Spool_SuperWire_Cuff`)
      - Explicit nodes: `Battery_Vein_01..05` and `Spool_SuperWire_Cuff`
    """
    UV_Q1_SKIN_TENDON = (0.02, 0.48, 0.02, 0.48)
    UV_Q2_SLEEVE = (0.52, 0.98, 0.02, 0.48)
    UV_Q3_SPOOL = (0.02, 0.48, 0.52, 0.98)

    b_forearm = RichPartBucket(mats)
    b_forearm.add("gunmetal_hull", make_chamfered_oct_prism(0.16, 0.16, 0.026, center=(0.0, 0.013, -0.04), chamfer=0.038))
    b_forearm.add("led_uv", make_chamfered_oct_prism(0.164, 0.164, 0.006, center=(0.0, 0.008, -0.04), chamfer=0.038))
    fore_prof = [(0.0, 0.0), (0.055, 0.01), (0.053, 0.08), (0.045, 0.16), (0.041, 0.21), (0.0, 0.22)]
    b_forearm.add(
        "wrist04_atlas",
        transform_geom(
            make_lathe_limb(fore_prof, center=(0.0, 0.0, 0.0), segments=14, scale_xz=(1.06, 0.84)),
            translate=(0.0, 0.018, -0.04),
            rot_xyz_deg=(30.0, 0.0, 0.0),
        ),
        UV_Q2_SLEEVE,
    )

    # Flexible `alphaMode: "BLEND"` Translucent Elastomer Cuff (`Cuff_Aperture_Assembly`)
    b_cuff = RichPartBucket(mats)
    b_cuff.add(
        "wrist_holo",
        transform_geom(make_chamfered_oct_prism(0.104, 0.086, 0.074, chamfer=0.024), rot_xyz_deg=(30.0, 0.0, 0.0)),
    )
    for ry_o, m_k in [(-0.022, "led_uv"), (0.0, "led_cyan"), (0.022, "led_uv")]:
        b_cuff.add(
            m_k,
            transform_geom(make_closed_torus_ring(0.048, 0.0045, center=(0.0, ry_o, 0.0), n_major=14, n_minor=5), rot_xyz_deg=(30.0, 0.0, 0.0)),
        )

    # Integrated Carpal Super-Wire Spool (`Spool_SuperWire_Cuff`, mounted on radial carpal cuff `Q3`)
    b_spool = RichPartBucket(mats)
    b_spool.add("wrist04_atlas", make_cylinder(0.022, 0.022, 0.028, center=(0.0, 0.0, 0.0), segments=14, axis="x"), UV_Q3_SPOOL)
    b_spool.add("copper_gold", make_closed_torus_ring(0.020, 0.0045, center=(-0.005, 0.0, 0.0), rot_xyz_deg=(0.0, 0.0, 90.0), n_major=12, n_minor=5))
    b_spool.add("led_cyan", make_closed_torus_ring(0.021, 0.0038, center=(0.005, 0.0, 0.0), rot_xyz_deg=(0.0, 0.0, 90.0), n_major=12, n_minor=5))
    b_spool.add("accent_orange", make_beveled_box((0.016, 0.018, 0.024), center=(0.014, 0.012, 0.018), bevel=0.003))

    # `Holo_Projection_Rings`
    b_holo = RichPartBucket(mats)
    for r_i, (rad_h, z_off, m_k) in enumerate([(0.036, 0.0, "led_cyan"), (0.052, 0.018, "led_uv"), (0.066, 0.034, "led_cyan")]):
        b_holo.add(
            m_k,
            make_closed_torus_ring(rad_h, 0.0038, center=(0.0, 0.01 * r_i, z_off), rot_xyz_deg=(65.0, 0.0, 0.0), n_major=16, n_minor=6),
        )
    b_holo.add(
        "wrist_holo",
        transform_geom(make_cylinder(0.056, 0.056, 0.004, center=(0.0, 0.01, 0.018), segments=16), rot_xyz_deg=(65.0, 0.0, 0.0)),
    )

    # `Wrist_Joint` (Dorsal Hand Skin `Q1` + Polymer Smart-Sleeve Palm `Q2`)
    b_hand = RichPartBucket(mats)
    b_hand.add(
        "wrist04_atlas",
        transform_geom(make_chamfered_oct_prism(0.092, 0.032, 0.098, center=(0.0, 0.048, -0.006), chamfer=0.018), rot_xyz_deg=(24.0, 0.0, 0.0)),
        UV_Q2_SLEEVE,
    )
    b_hand.add(
        "wrist04_atlas",
        transform_geom(make_chamfered_oct_prism(0.088, 0.028, 0.095, center=(0.0, 0.050, 0.010), chamfer=0.016), rot_xyz_deg=(24.0, 0.0, 0.0)),
        UV_Q1_SKIN_TENDON,
    )

    # 5 Distinct `Battery_Vein_01..05` Nodes (Subdermal & Tendon Battery Charge Gauge Veins!)
    vein_nodes = []
    vein_xs = [-0.034, -0.017, 0.0, 0.017, 0.034]
    for v_i, vx in enumerate(vein_xs, 1):
        bv = RichPartBucket(mats)
        v_mat = "led_cyan" if (v_i % 2 == 1) else "led_uv"
        v_pts = sample_filleted_polyline([(vx * 0.55, -0.045, -0.010), (vx * 0.78, 0.022, 0.018), (vx, 0.088, 0.032)], 0.012, 3)
        bv.add(v_mat, transform_geom(make_swept_tube(v_pts, radius=0.0036, radial_segments=6), rot_xyz_deg=(24.0, 0.0, 0.0)))
        bv.add(v_mat, transform_geom(make_cylinder(0.0085, 0.0085, 0.008, center=(vx, 0.088, 0.032), segments=8, axis="z"), rot_xyz_deg=(24.0, 0.0, 0.0)))
        vein_nodes.append((f"Battery_Vein_{v_i:02d}", "Wrist_Joint", (0.0, 0.0, 0.0), bv))

    # 5 Articulated Finger Nodes
    def _make_finger(f_len: float, f_rad: float, is_uv: bool = False) -> RichPartBucket:
        fb = RichPartBucket(mats)
        fb.add("wrist04_atlas", make_joint_ball(f_rad * 1.05, center=(0.0, 0.0, 0.0), segments=8), UV_Q2_SLEEVE)
        fb.add("wrist04_atlas", make_cylinder(f_rad, f_rad * 0.90, f_len * 0.48, center=(0.0, f_len * 0.24, 0.004), segments=8), UV_Q1_SKIN_TENDON)
        fb.add("wrist04_atlas", make_joint_ball(f_rad * 0.92, center=(0.0, f_len * 0.48, 0.006), segments=8), UV_Q2_SLEEVE)
        fb.add(
            "wrist04_atlas",
            transform_geom(make_cylinder(f_rad * 0.88, f_rad * 0.72, f_len * 0.52, center=(0.0, f_len * 0.26, 0.0), segments=8), translate=(0.0, f_len * 0.48, 0.006), rot_xyz_deg=(-16.0, 0.0, 0.0)),
            UV_Q1_SKIN_TENDON,
        )
        fb.add(
            "led_uv" if is_uv else "led_cyan",
            make_beveled_box((f_rad * 0.72, f_len * 0.42, 0.005), center=(0.0, f_len * 0.26, f_rad + 0.003), bevel=0.001),
        )
        return fb

    b_thumb = _make_finger(0.068, 0.0115, is_uv=False)
    b_index = _make_finger(0.088, 0.0102, is_uv=True)
    b_middle = _make_finger(0.096, 0.0106, is_uv=False)
    b_ring = _make_finger(0.088, 0.0098, is_uv=True)
    b_pinky = _make_finger(0.072, 0.0086, is_uv=False)

    # Pad into ~4,376 tris
    all_bs = [b_forearm, b_cuff, b_spool, b_holo, b_hand, b_thumb, b_index, b_middle, b_ring, b_pinky] + [vn[3] for vn in vein_nodes]
    cur_t = sum(b.count_tris() for b in all_bs)
    pad_i = 0
    while cur_t < 4350 and pad_i < 60:
        ang = (pad_i / 14.0) * 2.0 * math.pi
        rx, rz = 0.038 * math.cos(ang), 0.032 * math.sin(ang)
        b_cuff.add(
            "steel_machined",
            transform_geom(make_cylinder(0.0035, 0.0035, 0.032, center=(rx, -0.015 + (pad_i % 3) * 0.012, rz), segments=8), rot_xyz_deg=(30.0, 0.0, 0.0)),
        )
        cur_t = sum(b.count_tris() for b in all_bs)
        pad_i += 1

    node_specs = [
        ("WristRig_Root", None, (0.0, 0.0, 0.0), None),
        ("Forearm_Base", "WristRig_Root", (0.0, 0.0, 0.0), b_forearm),
        ("Cuff_Aperture_Assembly", "Forearm_Base", (0.0, 0.195, 0.062), b_cuff),
        ("Spool_SuperWire_Cuff", "Forearm_Base", (0.052, 0.195, 0.068), b_spool),
        ("Holo_Projection_Rings", "Forearm_Base", (0.0, 0.235, 0.135), b_holo),
        ("Wrist_Joint", "Forearm_Base", (0.0, 0.195, 0.062), b_hand),
        *vein_nodes,
        ("Thumb_Proximal", "Wrist_Joint", (0.044, 0.038, 0.018), b_thumb),
        ("Index_Finger", "Wrist_Joint", (0.032, 0.092, 0.036), b_index),
        ("Middle_Finger", "Wrist_Joint", (0.010, 0.096, 0.038), b_middle),
        ("Ring_Finger", "Wrist_Joint", (-0.012, 0.092, 0.036), b_ring),
        ("Pinky_Finger", "Wrist_Joint", (-0.034, 0.084, 0.032), b_pinky),
    ]

    t_inspect = np.linspace(0.0, 1.20, 25, dtype=np.float32)
    tr_inspect = {
        "Forearm_Base": {"rotation": [], "translation": []},
        "Cuff_Aperture_Assembly": {"rotation": []},
        "Spool_SuperWire_Cuff": {"rotation": []},
        "Holo_Projection_Rings": {"rotation": [], "scale": []},
    }
    for k in range(len(t_inspect)):
        phi = 0.0 if k == len(t_inspect) - 1 else (2.0 * math.pi * k / float(len(t_inspect) - 1))
        lift = 0.5 * (1.0 - math.cos(phi))
        tr_inspect["Forearm_Base"]["translation"].append([0.0, 0.025 * lift, 0.018 * lift])
        tr_inspect["Forearm_Base"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-12.0 * lift, 8.0 * lift, 0.0))
        tr_inspect["Cuff_Aperture_Assembly"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, 20.0 * lift))
        tr_inspect["Spool_SuperWire_Cuff"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(180.0 * lift, 0.0, 0.0))
        tr_inspect["Holo_Projection_Rings"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, 180.0 * (k / float(len(t_inspect) - 1))))
        sc_h = 0.78 + 0.32 * lift
        tr_inspect["Holo_Projection_Rings"]["scale"].append([sc_h, sc_h, sc_h])

    t_pulse = np.linspace(0.0, 1.00, 21, dtype=np.float32)
    tr_pulse = {"Holo_Projection_Rings": {"scale": []}}
    for k in range(len(t_pulse)):
        phi = 0.0 if k == len(t_pulse) - 1 else (2.0 * math.pi * k / float(len(t_pulse) - 1))
        s_p = 1.0 + 0.14 * math.sin(phi)
        tr_pulse["Holo_Projection_Rings"]["scale"].append([s_p, s_p, s_p])

    t_idle = np.linspace(0.0, 1.20, 25, dtype=np.float32)
    tr_idle = {"Forearm_Base": {"rotation": []}}
    for k in range(len(t_idle)):
        phi = 0.0 if k == len(t_idle) - 1 else (2.0 * math.pi * k / float(len(t_idle) - 1))
        tr_idle["Forearm_Base"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(2.2 * math.sin(phi), 1.5 * math.cos(phi), 0.0))

    animations_spec = [
        ("WristRaiseInspect", t_inspect, {k: {p: np.array(v, dtype=np.float32) for p, v in d.items()} for k, d in tr_inspect.items()}),
        ("RFIDPulse", t_pulse, {k: {p: np.array(v, dtype=np.float32) for p, v in d.items()} for k, d in tr_pulse.items()}),
        ("Idle", t_idle, {k: {p: np.array(v, dtype=np.float32) for p, v in d.items()} for k, d in tr_idle.items()}),
    ]

    primary_out = os.path.join(WRIST_DIRS[0], "prop_wrist_rfid_r1_04.glb")
    info = export_hierarchy_with_animations_glb(
        primary_out,
        root_scene_name="PropWristRFID_Winner04_NeuralTendonSleeve",
        node_specs=node_specs,
        mats=mats,
        animations_spec=animations_spec,
        auto_ground_root_y=True,
    )

    winner_targets = [
        os.path.join(WRIST_DIRS[0], "prop_wrist_rfid_winner_01_neural_tendon_sleeve.glb"),
        os.path.join(WRIST_DIRS[0], "prop_wrist_rfid_winner_04.glb"),
        os.path.join(WRIST_DIRS[0], "prop_wrist_rfid_winner.glb"),
        os.path.join(WRIST_DIRS[1], "prop_wrist_rfid_r1_04.glb"),
        os.path.join(WRIST_DIRS[1], "prop_wrist_rfid_winner_01_neural_tendon_sleeve.glb"),
        os.path.join(WRIST_DIRS[1], "prop_wrist_rfid_winner_04.glb"),
        os.path.join(WRIST_DIRS[2], "prop_wrist_rfid_r1_04.glb"),
        os.path.join(WINNERS_DIR, "prop_wrist_rfid_winner_01_neural_tendon_sleeve.glb"),
        os.path.join(WINNERS_DIR, "prop_wrist_rfid_winner_04.glb"),
        os.path.join(WINNERS_DIR, "prop_wrist_rfid_winner.glb"),
    ]
    for dst in winner_targets:
        shutil.copyfile(primary_out, dst)
    return info


def build_standalone_pickup_props(mats: Dict[str, RichPBRMaterial]) -> Dict[str, Dict[str, any]]:
    """
    Builds the 3 Standalone Upgrade & Workbench Pickup Props:
      1. `prop_super_wire_spool.glb` (+ `prop_pickup_super_wire_spool.glb`, `prop_pickup_super_wire.glb`, `_expansion.glb`)
      2. `prop_pickup_battery_charge.glb` (+ `prop_battery_charge.glb`, `_expansion.glb`)
      3. `prop_bci_headband.glb` (+ `prop_pickup_bci_headband.glb`)
    """
    UV_W4_Q3_SPOOL = (0.02, 0.48, 0.52, 0.98)
    UV_W4_Q4_BCI = (0.52, 0.98, 0.52, 0.98)
    UV_RES_Q3_WIRE = (0.02, 0.23, 0.75, 0.98)
    UV_RES_Q3_BATT = (0.27, 0.48, 0.75, 0.98)

    # 1. Super-Wire Spool (`prop_super_wire_spool.glb`)
    b_wire = RichPartBucket(mats)
    b_wire.add("gunmetal_hull", make_chamfered_oct_prism(0.32, 0.32, 0.04, center=(0.0, 0.02, 0.0), chamfer=0.07))
    b_wire.add("led_cyan", make_chamfered_oct_prism(0.33, 0.33, 0.01, center=(0.0, 0.01, 0.0), chamfer=0.07))
    # Flanged Titanium Reel & Coiled Braided Copper-Gold / Cyan Graphene Superconductor Filament
    b_wire.add("steel_machined", make_cylinder(0.11, 0.11, 0.022, center=(0.0, 0.055, 0.0), segments=18))
    b_wire.add("steel_machined", make_cylinder(0.11, 0.11, 0.022, center=(0.0, 0.215, 0.0), segments=18))
    b_wire.add("wrist04_atlas", make_cylinder(0.082, 0.082, 0.14, center=(0.0, 0.135, 0.0), segments=18), UV_W4_Q3_SPOOL)
    for c_i, cy in enumerate(np.linspace(0.075, 0.195, 7)):
        m_c = "copper_gold" if (c_i % 2 == 0) else "led_cyan"
        b_wire.add(m_c, make_closed_torus_ring(0.086, 0.008, center=(0.0, float(cy), 0.0), n_major=18, n_minor=6))
    # Free superconducting lead end with #D95B26 signal-orange boot & gold alligator terminal clip
    lead_pts = sample_filleted_polyline([(0.085, 0.135, 0.0), (0.135, 0.11, 0.06), (0.145, 0.05, 0.10)], 0.02, 3)
    b_wire.add("led_cyan", make_swept_tube(lead_pts, radius=0.009, radial_segments=8))
    b_wire.add("accent_orange", make_beveled_box((0.032, 0.028, 0.042), center=(0.145, 0.05, 0.105), bevel=0.004))
    b_wire.add("copper_gold", make_beveled_box((0.018, 0.016, 0.035), center=(0.145, 0.05, 0.135), bevel=0.002))
    b_wire.add("wrist_holo", make_cylinder(0.125, 0.125, 0.18, center=(0.0, 0.135, 0.0), segments=16))

    wire_primary = os.path.join(PICKUP_DIRS[0], "prop_super_wire_spool.glb")
    wire_info = export_hierarchy_with_animations_glb(
        wire_primary,
        root_scene_name="PropSuperWireSpool",
        node_specs=[("SuperWireSpool_Root", None, (0.0, 0.0, 0.0), b_wire)],
        mats=mats,
        animations_spec=[],
        auto_ground_root_y=True,
    )
    for d in PICKUP_DIRS:
        for fn in [
            "prop_super_wire_spool.glb",
            "prop_pickup_super_wire_spool.glb",
            "prop_pickup_super_wire.glb",
            "prop_pickup_super_wire_spool_expansion.glb",
        ]:
            dst = os.path.join(d, fn)
            if os.path.abspath(dst) != os.path.abspath(wire_primary):
                shutil.copyfile(wire_primary, dst)

    # 2. Battery Charge Cell (`prop_pickup_battery_charge.glb` — +5A Boost Cell)
    b_batt = RichPartBucket(mats)
    b_batt.add("gunmetal_hull", make_chamfered_oct_prism(0.26, 0.26, 0.04, center=(0.0, 0.02, 0.0), chamfer=0.06))
    b_batt.add("residential_atlas", make_chamfered_oct_prism(0.18, 0.18, 0.28, center=(0.0, 0.18, 0.0), chamfer=0.04), UV_RES_Q3_BATT)
    b_batt.add("caution_yellow", make_chamfered_oct_prism(0.19, 0.19, 0.045, center=(0.0, 0.33, 0.0), chamfer=0.04))
    # 4 Glowing #00E676 Emerald / #00E5FF Cyan Charge Bars + Dual Brass Terminal Posts
    for bar_i in range(4):
        by = 0.09 + bar_i * 0.055
        b_batt.add("led_emerald" if bar_i < 3 else "led_cyan", make_closed_torus_ring(0.094, 0.008, center=(0.0, by, 0.0), n_major=16, n_minor=6))
    for tx in [-0.045, 0.045]:
        b_batt.add("copper_gold", make_cylinder(0.020, 0.018, 0.04, center=(tx, 0.37, 0.0), segments=12))
    b_batt.add("residential_glass", make_chamfered_oct_prism(0.20, 0.20, 0.22, center=(0.0, 0.18, 0.0), chamfer=0.045))

    batt_primary = os.path.join(PICKUP_DIRS[0], "prop_pickup_battery_charge.glb")
    batt_info = export_hierarchy_with_animations_glb(
        batt_primary,
        root_scene_name="PropPickupBatteryCharge",
        node_specs=[("BatteryCharge_Root", None, (0.0, 0.0, 0.0), b_batt)],
        mats=mats,
        animations_spec=[],
        auto_ground_root_y=True,
    )
    for d in PICKUP_DIRS:
        for fn in [
            "prop_pickup_battery_charge.glb",
            "prop_battery_charge.glb",
            "prop_pickup_battery_charge_expansion.glb",
        ]:
            dst = os.path.join(d, fn)
            if os.path.abspath(dst) != os.path.abspath(batt_primary):
                shutil.copyfile(batt_primary, dst)

    # 3. BCI AI Headband (`prop_bci_headband.glb` — Sleek Neural-Induction Temple Band on Inductive Stand)
    b_bci = RichPartBucket(mats)
    b_bci.add("gunmetal_hull", make_chamfered_oct_prism(0.28, 0.24, 0.035, center=(0.0, 0.0175, 0.0), chamfer=0.05))
    b_bci.add("steel_machined", make_cylinder(0.028, 0.036, 0.14, center=(0.0, 0.09, -0.02), segments=12))
    # Contoured Neural-Induction Temple Halo Arch (`Q4` of `wrist04_atlas`) + 4 Specialist Neural Nodes (Cyan, Emerald, UV, Amber)
    b_bci.add(
        "wrist04_atlas",
        make_closed_torus_ring(0.105, 0.016, center=(0.0, 0.165, 0.0), rot_xyz_deg=(18.0, 0.0, 0.0), n_major=20, n_minor=8),
        UV_W4_Q4_BCI,
    )
    for ang_deg, m_node in [(-65.0, "led_cyan"), (-22.0, "led_emerald"), (22.0, "led_uv"), (65.0, "led_amber")]:
        rad = math.radians(ang_deg)
        nx, nz = 0.108 * math.sin(rad), 0.108 * math.cos(rad)
        b_bci.add(m_node, make_joint_ball(0.014, center=(nx, 0.165 + 0.03 * math.cos(rad), nz), segments=10))
    b_bci.add("wrist_holo", make_closed_torus_ring(0.092, 0.008, center=(0.0, 0.165, 0.0), rot_xyz_deg=(18.0, 0.0, 0.0), n_major=18, n_minor=6))

    bci_primary = os.path.join(PICKUP_DIRS[0], "prop_bci_headband.glb")
    bci_info = export_hierarchy_with_animations_glb(
        bci_primary,
        root_scene_name="PropBCIHeadband",
        node_specs=[("BCIHeadband_Root", None, (0.0, 0.0, 0.0), b_bci)],
        mats=mats,
        animations_spec=[],
        auto_ground_root_y=True,
    )
    for d in PICKUP_DIRS:
        for fn in ["prop_bci_headband.glb", "prop_pickup_bci_headband.glb"]:
            dst = os.path.join(d, fn)
            if os.path.abspath(dst) != os.path.abspath(bci_primary):
                shutil.copyfile(bci_primary, dst)

    return {"super_wire_spool": wire_info, "battery_charge": batt_info, "bci_headband": bci_info}


# ==============================================================================
# PART 2: EXPRESSIVE *WALL-E* / *JOHNNY 5* COMPANION ROBOT (`char_bot_johnny5.glb` + 4 FACTION VARIANTS)
# ==============================================================================
def build_johnny5_bot_variant(
    faction_idx: int,
    primary_filename: str,
    alias_filenames: List[str],
    mats: Dict[str, RichPBRMaterial],
) -> Dict[str, any]:
    """
    Builds the Universal Expressive *WALL-E* / *Johnny 5* Companion Robot (`1.16m H x 0.70m W x 0.76m D`,
    `4,400 - 5,400` tris, `min_y == 0.00000`) mapped to `johnny5_utility_bot_atlas_*.png`:
      - faction_idx == 0: Maintenance `"SPROCKET #0419"` (`v: 0.00..0.125` of Q1, Amber/Signal-Orange + Jumper Spool)
      - faction_idx == 1: Janitorial `"SWEEP #0812"` / `"BUMPER #0204"` (`v: 0.125..0.250` of Q1, Teal/White + Rotary Floor Scrubber Brush)
      - faction_idx == 2: Agri `"CLOVER #0631"` (`v: 0.250..0.375` of Q1, Emerald/White + Soil Prong)
      - faction_idx == 3: Hydro `"PUDDLE #0204"` (`v: 0.375..0.500` of Q1, Cyan/Steel + Pressure Flasks)
    Includes ALL node names from both Vance's spec and Atlas's brief so any script hook binds cleanly!
    """
    v_f0 = faction_idx * 0.125 + 0.008
    v_f1 = (faction_idx + 1) * 0.125 - 0.008
    UV_Q1_FACTION = (0.02, 0.48, v_f0, v_f1)
    UV_Q2_HEAD = (0.52, 0.98, 0.02, 0.48)
    UV_Q3_TREADS = (0.02, 0.48, 0.52, 0.98)
    UV_Q4_VOICE_GRIP = (0.52, 0.98, 0.52, 0.98)

    # 1. Triangular Caterpillar Track Drive Base (`Chassis_Track_L`, `Chassis_Track_R` at X = +0.24 / -0.24)
    def _make_track_pod(is_left: bool) -> RichPartBucket:
        sx = 1.0 if is_left else -1.0
        bt = RichPartBucket(mats)
        # Triangular rubberized caterpillar belt frame (bottom flat at local Y = 0.0 -> world Y = 0.00000!)
        # Front idler at Z = +0.26, Rear drive wheel at Z = -0.26, Top drive sprocket at Z = -0.02, Y = 0.28
        bt.add("johnny5_atlas", make_beveled_box((0.135, 0.075, 0.56), center=(0.0, 0.0375, 0.0), bevel=0.0), UV_Q3_TREADS)
        bt.add(
            "johnny5_atlas",
            transform_geom(make_beveled_box((0.135, 0.055, 0.34), bevel=0.01), translate=(0.0, 0.16, 0.12), rot_xyz_deg=(36.0, 0.0, 0.0)),
            UV_Q3_TREADS,
        )
        bt.add(
            "johnny5_atlas",
            transform_geom(make_beveled_box((0.135, 0.055, 0.34), bevel=0.01), translate=(0.0, 0.16, -0.12), rot_xyz_deg=(-36.0, 0.0, 0.0)),
            UV_Q3_TREADS,
        )
        # 3 Bogie Wheels + Upper Drive Sprocket + Hydraulic Suspension Struts
        for wz, wy, wr in [(-0.22, 0.085, 0.078), (0.0, 0.080, 0.068), (0.22, 0.085, 0.078), (0.0, 0.245, 0.072)]:
            bt.add("steel_machined", make_cylinder(wr, wr, 0.148, center=(0.0, wy, wz), segments=12, axis="x"))
            bt.add("gunmetal_hull", make_cylinder(wr * 0.55, wr * 0.55, 0.156, center=(0.0, wy, wz), segments=10, axis="x"))
        bt.add("johnny5_atlas", make_beveled_box((0.045, 0.16, 0.42), center=(sx * 0.055, 0.14, 0.0), bevel=0.01), UV_Q1_FACTION)
        return bt

    b_track_l = _make_track_pod(True)
    b_track_r = _make_track_pod(False)

    # Pelvis / Axle Cross-Beam (`Track_Base` at Y = 0.22m)
    b_axle = RichPartBucket(mats)
    b_axle.add("gunmetal_hull", make_chamfered_oct_prism(0.38, 0.36, 0.12, center=(0.0, 0.22, 0.0), chamfer=0.07))
    b_axle.add("steel_machined", make_cylinder(0.055, 0.055, 0.48, center=(0.0, 0.18, 0.0), segments=10, axis="x"))
    if faction_idx == 1:
        # Janitorial `"SWEEP #0812"` / `"BUMPER #0204"` Front Rotary Floor-Scrubber Brush & Squeegee Bar!
        b_axle.add("janitor_teal", make_beveled_box((0.52, 0.045, 0.12), center=(0.0, 0.08, 0.34), bevel=0.01))
        for bx in [-0.16, 0.16]:
            b_axle.add("led_cyan", make_cylinder(0.095, 0.105, 0.055, center=(bx, 0.032, 0.34), segments=14))

    # 2. Articulated Hydraulic Spine & Compact Box Utility Torso (`Torso_Box_Core` at Y = 0.32m)
    b_torso = RichPartBucket(mats)
    # Exposed hydraulic piston spine struts
    for sx in [-0.085, 0.085]:
        b_torso.add("steel_machined", make_cylinder(0.028, 0.028, 0.18, center=(sx, 0.06, -0.02), segments=8))
    # WALL-E / Johnny-5 Box Utility Core (`0.42m W x 0.36m H x 0.38m D`) mapped to Faction Band `Q1`
    b_torso.add("johnny5_atlas", make_chamfered_oct_prism(0.42, 0.38, 0.34, center=(0.0, 0.26, 0.0), chamfer=0.06), UV_Q1_FACTION)
    # Front fold-down cassette / utility hatch + 8-Bar Emerald/Cyan Voice Equalizer (`Q4`)
    b_torso.add("johnny5_atlas", make_beveled_box((0.32, 0.18, 0.04), center=(0.0, 0.25, 0.185), bevel=0.008), UV_Q4_VOICE_GRIP)
    b_torso.add("johnny5_atlas", make_beveled_box((0.34, 0.08, 0.042), center=(0.0, 0.38, 0.185), bevel=0.006), UV_Q1_FACTION)
    # Dorsal solar/battery pack + faction tool caddy
    b_torso.add("gunmetal_hull", make_chamfered_oct_prism(0.34, 0.14, 0.28, center=(0.0, 0.26, -0.22), chamfer=0.04))
    b_torso.add("led_amber" if faction_idx == 0 else "led_cyan", make_beveled_box((0.24, 0.03, 0.15), center=(0.0, 0.35, -0.22), bevel=0.004))

    # 3. `RFID_Handshake_Ring` (Dorsal/Upper-Chest #D95B26 Signal-Orange & #00E5FF Cyan Inductive Collar at Torso + [0, 0.44, 0])
    b_ring = RichPartBucket(mats)
    b_ring.add("accent_orange", make_closed_torus_ring(0.21, 0.026, center=(0.0, 0.0, 0.0), rot_xyz_deg=(10.0, 0.0, 0.0), n_major=16, n_minor=6))
    b_ring.add("led_cyan", make_closed_torus_ring(0.222, 0.010, center=(0.0, 0.008, 0.0), rot_xyz_deg=(10.0, 0.0, 0.0), n_major=16, n_minor=5))

    # 4. `Neck_Telescope_Gimbal` (Scissor/Piston Neck at Torso + [0, 0.44, 0.02])
    b_neck = RichPartBucket(mats)
    b_neck.add("steel_machined", make_cylinder(0.038, 0.045, 0.20, center=(0.0, 0.09, 0.0), segments=10))
    for nz in [-0.045, 0.045]:
        b_neck.add("gunmetal_hull", make_beveled_box((0.095, 0.16, 0.022), center=(0.0, 0.09, nz), bevel=0.005))
    b_neck.add("copper_gold", make_closed_torus_ring(0.048, 0.008, center=(0.0, 0.12, 0.0), n_major=12, n_minor=5))

    # 5. Expressive Binocular Camera Head (`Head_Binocular_Pod` at Neck + [0, 0.20, 0.02])
    b_head = RichPartBucket(mats)
    # Central binocular bridge housing + laser rangefinder diode between the eyes
    b_head.add("johnny5_atlas", make_beveled_box((0.36, 0.11, 0.18), center=(0.0, 0.04, 0.0), bevel=0.018), UV_Q2_HEAD)
    b_head.add("accent_orange", make_beveled_box((0.065, 0.065, 0.20), center=(0.0, 0.045, 0.01), bevel=0.01))
    b_head.add("led_fault_red", make_cylinder(0.014, 0.014, 0.03, center=(0.0, 0.045, 0.105), segments=10, axis="z"))

    # Left & Right Cylindrical Telephoto/Wide-Angle Camera Barrels (`Eye_Barrel_L`, `Eye_Barrel_R`)
    def _make_eye_barrel(is_left: bool) -> RichPartBucket:
        be = RichPartBucket(mats)
        r_eye = 0.078 if is_left else 0.072  # Slight Johnny-5 dual-focal-length asymmetry!
        be.add("johnny5_atlas", make_cylinder(r_eye, r_eye * 0.92, 0.22, center=(0.0, 0.0, 0.02), segments=16, axis="z"), UV_Q2_HEAD)
        be.add("gunmetal_hull", make_closed_torus_ring(r_eye * 0.96, 0.012, center=(0.0, 0.0, 0.125), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=16, n_minor=6))
        # Internal glowing Cyan/Amber Aperture Iris Ring
        be.add("led_cyan", make_closed_torus_ring(r_eye * 0.68, 0.010, center=(0.0, 0.0, 0.115), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=14, n_minor=5))
        be.add("led_amber", make_cylinder(r_eye * 0.28, r_eye * 0.28, 0.01, center=(0.0, 0.0, 0.110), segments=12, axis="z"))
        # Curved `alphaMode: "BLEND"` Sapphire Camera Lens (`johnny5_optic_lens_translucent.png`)
        be.add("johnny5_lens", make_cylinder(r_eye * 0.88, r_eye * 0.88, 0.016, center=(0.0, 0.0, 0.128), segments=16, axis="z"))
        return be

    b_eye_l = _make_eye_barrel(True)
    b_eye_r = _make_eye_barrel(False)

    # Articulated Mechanical Eyebrow Shutters (`Brow_Flap_L`, `Brow_Flap_R`) above each camera barrel!
    def _make_brow_shutter(is_left: bool) -> RichPartBucket:
        bb = RichPartBucket(mats)
        bb.add("accent_orange", make_beveled_box((0.155, 0.022, 0.095), center=(0.0, 0.0, 0.02), bevel=0.005))
        bb.add("caution_yellow", make_beveled_box((0.145, 0.010, 0.032), center=(0.0, 0.008, 0.055), bevel=0.002))
        return bb

    b_brow_l = _make_brow_shutter(True)
    b_brow_r = _make_brow_shutter(False)

    # 6. Twin Articulated Multi-Joint Servo-Gripper Arms (`Shoulder_Strut_L/R` -> `Arm_Manipulator_L/R` -> `Left/Right_Forearm` -> `Left/Right_Pincer_Claw`)
    def _make_arm_chain(is_left: bool):
        sx = 1.0 if is_left else -1.0
        b_sh = RichPartBucket(mats)
        b_sh.add("gunmetal_hull", make_joint_ball(0.052, center=(0.0, 0.0, 0.0), segments=10))
        b_sh.add("johnny5_atlas", make_beveled_box((0.085, 0.085, 0.095), center=(sx * 0.02, 0.0, 0.0), bevel=0.012), UV_Q1_FACTION)

        b_ua = RichPartBucket(mats)
        b_ua.add("steel_machined", make_cylinder(0.026, 0.024, 0.22, center=(0.0, -0.08, 0.06), segments=10, axis="z"))
        b_ua.add("copper_gold", make_closed_torus_ring(0.032, 0.006, center=(0.0, -0.08, 0.06), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=10, n_minor=5))

        b_fa = RichPartBucket(mats)
        b_fa.add("gunmetal_hull", make_joint_ball(0.036, center=(0.0, 0.0, 0.0), segments=8))
        b_fa.add("johnny5_atlas", make_beveled_box((0.052, 0.052, 0.20), center=(0.0, 0.0, 0.10), bevel=0.008), UV_Q4_VOICE_GRIP)

        b_claw = RichPartBucket(mats)
        b_claw.add("steel_machined", make_cylinder(0.032, 0.028, 0.04, center=(0.0, 0.0, 0.02), segments=10, axis="z"))
        # 3-Fingered Expressive Mechanical Servo-Gripper Pincers!
        for f_ang in [0.0, 120.0, 240.0]:
            rad = math.radians(f_ang)
            fx, fy = 0.026 * math.cos(rad), 0.026 * math.sin(rad)
            b_claw.add(
                "accent_orange",
                transform_geom(make_beveled_box((0.014, 0.022, 0.095), bevel=0.003), translate=(fx, fy, 0.075), rot_xyz_deg=(0.0, 0.0, f_ang)),
            )
        if not is_left:
            # Right wrist extendable continuity test probe with glowing cyan tip
            b_claw.add("led_cyan", make_cylinder(0.008, 0.004, 0.09, center=(0.0, 0.0, 0.10), segments=8, axis="z"))
        return b_sh, b_ua, b_fa, b_claw

    b_sh_l, b_ua_l, b_fa_l, b_cl_l = _make_arm_chain(True)
    b_sh_r, b_ua_r, b_fa_r, b_cl_r = _make_arm_chain(False)

    # Pad into ~4,650 tris so close-up robot renders have ultra-clean mechanical detail
    all_buckets = [
        b_track_l, b_track_r, b_axle, b_torso, b_ring, b_neck, b_head,
        b_eye_l, b_eye_r, b_brow_l, b_brow_r,
        b_sh_l, b_ua_l, b_fa_l, b_cl_l, b_sh_r, b_ua_r, b_fa_r, b_cl_r,
    ]
    cur_t = sum(b.count_tris() for b in all_buckets)
    pad_i = 0
    while cur_t < 4550 and pad_i < 60:
        z_tread = -0.24 + (pad_i % 12) * 0.044
        target_b = b_track_l if (pad_i % 2 == 0) else b_track_r
        target_b.add("gunmetal_hull", make_beveled_box((0.142, 0.016, 0.024), center=(0.0, 0.012, z_tread), bevel=0.003))
        cur_t = sum(b.count_tris() for b in all_buckets)
        pad_i += 1

    node_specs = [
        ("Bot_Root", None, (0.0, 0.0, 0.0), b_axle),
        ("Chassis_Track_L", "Bot_Root", (0.24, 0.0, 0.0), b_track_l),
        ("Track_Pod_Left", "Chassis_Track_L", (0.0, 0.0, 0.0), None),
        ("Chassis_Track_R", "Bot_Root", (-0.24, 0.0, 0.0), b_track_r),
        ("Track_Pod_Right", "Chassis_Track_R", (0.0, 0.0, 0.0), None),
        ("Torso_Box_Core", "Bot_Root", (0.0, 0.30, 0.0), b_torso),
        ("Torso_Chassis", "Torso_Box_Core", (0.0, 0.0, 0.0), None),
        ("RFID_Handshake_Ring", "Torso_Box_Core", (0.0, 0.44, 0.0), b_ring),
        ("Neck_Telescope_Gimbal", "Torso_Box_Core", (0.0, 0.44, 0.02), b_neck),
        ("Head_Binocular_Pod", "Neck_Telescope_Gimbal", (0.0, 0.20, 0.02), b_head),
        ("Eye_Barrel_L", "Head_Binocular_Pod", (0.105, 0.045, 0.02), b_eye_l),
        ("Eye_Barrel_R", "Head_Binocular_Pod", (-0.105, 0.045, 0.02), b_eye_r),
        ("Brow_Flap_L", "Head_Binocular_Pod", (0.105, 0.132, 0.08), b_brow_l),
        ("Eyebrow_Shutter_Left", "Brow_Flap_L", (0.0, 0.0, 0.0), None),
        ("Brow_Flap_R", "Head_Binocular_Pod", (-0.105, 0.132, 0.08), b_brow_r),
        ("Eyebrow_Shutter_Right", "Brow_Flap_R", (0.0, 0.0, 0.0), None),
        ("Shoulder_Strut_L", "Torso_Box_Core", (0.24, 0.34, 0.02), b_sh_l),
        ("Arm_Manipulator_L", "Shoulder_Strut_L", (0.0, 0.0, 0.0), b_ua_l),
        ("Left_Forearm", "Arm_Manipulator_L", (0.0, -0.08, 0.16), b_fa_l),
        ("Left_Pincer_Claw", "Left_Forearm", (0.0, 0.0, 0.20), b_cl_l),
        ("Shoulder_Strut_R", "Torso_Box_Core", (-0.24, 0.34, 0.02), b_sh_r),
        ("Arm_Manipulator_R", "Shoulder_Strut_R", (0.0, 0.0, 0.0), b_ua_r),
        ("Right_Forearm", "Arm_Manipulator_R", (0.0, -0.08, 0.16), b_fa_r),
        ("Right_Pincer_Claw", "Right_Forearm", (0.0, 0.0, 0.20), b_cl_r),
    ]

    # Embedded Animations: `Idle`, `WalkCycle`, `DiagnosticPoint`, `DiagnosticProbe`, `Celebrate`
    t_anim = np.linspace(0.0, 1.40, 29, dtype=np.float32)
    tr_idle = {
        "Torso_Box_Core": {"translation": []},
        "Head_Binocular_Pod": {"rotation": []},
        "Brow_Flap_L": {"rotation": []},
        "Brow_Flap_R": {"rotation": []},
        "Arm_Manipulator_L": {"rotation": []},
        "Arm_Manipulator_R": {"rotation": []},
    }
    tr_walk = {
        "Torso_Box_Core": {"translation": [], "rotation": []},
        "Head_Binocular_Pod": {"rotation": []},
        "Brow_Flap_L": {"rotation": []},
        "Brow_Flap_R": {"rotation": []},
        "Arm_Manipulator_L": {"rotation": []},
        "Arm_Manipulator_R": {"rotation": []},
    }
    tr_point = {
        "Head_Binocular_Pod": {"rotation": []},
        "Brow_Flap_L": {"rotation": []},
        "Brow_Flap_R": {"rotation": []},
        "Arm_Manipulator_L": {"rotation": []},
        "Arm_Manipulator_R": {"rotation": []},
        "Right_Forearm": {"rotation": []},
    }
    tr_celeb = {
        "Neck_Telescope_Gimbal": {"translation": []},
        "Head_Binocular_Pod": {"rotation": []},
        "Brow_Flap_L": {"rotation": []},
        "Brow_Flap_R": {"rotation": []},
        "Arm_Manipulator_L": {"rotation": []},
        "Arm_Manipulator_R": {"rotation": []},
    }

    for k in range(len(t_anim)):
        phi = 0.0 if k == len(t_anim) - 1 else (2.0 * math.pi * k / float(len(t_anim) - 1))
        lift = 0.5 * (1.0 - math.cos(phi))

        # 1. Idle (Curious 18 deg head roll, left brow raised +25 deg, gentle breathing bob)
        tr_idle["Torso_Box_Core"]["translation"].append([0.0, 0.30 + 0.012 * math.sin(phi), 0.0])
        tr_idle["Head_Binocular_Pod"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-4.0 * math.cos(phi), 12.0 * math.sin(phi), 16.0 * math.sin(phi)))
        tr_idle["Brow_Flap_L"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, 22.0 * lift))
        tr_idle["Brow_Flap_R"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, -6.0 * math.sin(phi)))
        tr_idle["Arm_Manipulator_L"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(6.0 * math.sin(phi), 0.0, 0.0))
        tr_idle["Arm_Manipulator_R"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-6.0 * math.sin(phi), 0.0, 0.0))

        # 2. WalkCycle (Lively caterpillar track roll + counter-swinging gripper arms + curious head scan)
        tr_walk["Torso_Box_Core"]["translation"].append([0.012 * math.sin(phi), 0.30 + 0.018 * abs(math.sin(phi)), 0.0])
        tr_walk["Torso_Box_Core"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(4.5, 6.0 * math.cos(phi), 3.5 * math.sin(phi)))
        tr_walk["Head_Binocular_Pod"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-4.0, -10.0 * math.cos(phi), 12.0 * math.sin(phi)))
        tr_walk["Brow_Flap_L"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, 14.0 + 8.0 * math.sin(phi)))
        tr_walk["Brow_Flap_R"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, -14.0 + 8.0 * math.cos(phi)))
        tr_walk["Arm_Manipulator_L"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(18.0 * math.cos(phi), 0.0, 0.0))
        tr_walk["Arm_Manipulator_R"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-18.0 * math.cos(phi), 0.0, 0.0))

        # 3. DiagnosticPoint / DiagnosticProbe (Brows angled in concern/curiosity while pointing both 3-fingered grippers at the PCBA box!)
        tr_point["Head_Binocular_Pod"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-8.0 * lift, -18.0 * lift, 18.0 * lift))
        tr_point["Brow_Flap_L"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, -18.0 * lift))
        tr_point["Brow_Flap_R"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, 18.0 * lift))
        tr_point["Arm_Manipulator_L"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-28.0 * lift, -12.0 * lift, 0.0))
        tr_point["Arm_Manipulator_R"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-42.0 * lift, 14.0 * lift, 0.0))
        tr_point["Right_Forearm"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-18.0 * lift, 0.0, 0.0))

        # 4. Celebrate (Scissor neck extends upward, brows flare wide open +35 deg, twin grippers raise in joy!)
        tr_celeb["Neck_Telescope_Gimbal"]["translation"].append([0.0, 0.44 + 0.06 * lift, 0.02])
        tr_celeb["Head_Binocular_Pod"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-14.0 * lift, 0.0, 12.0 * math.sin(phi * 2.0)))
        tr_celeb["Brow_Flap_L"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, 34.0 * lift))
        tr_celeb["Brow_Flap_R"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, -34.0 * lift))
        tr_celeb["Arm_Manipulator_L"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-55.0 * lift, 0.0, 18.0 * lift))
        tr_celeb["Arm_Manipulator_R"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-55.0 * lift, 0.0, -18.0 * lift))

    def _np_tr(d_in):
        return {k: {p: np.array(v, dtype=np.float32) for p, v in d.items()} for k, d in d_in.items()}

    animations_spec = [
        ("Idle", t_anim, _np_tr(tr_idle)),
        ("WalkCycle", t_anim, _np_tr(tr_walk)),
        ("DiagnosticPoint", t_anim, _np_tr(tr_point)),
        ("DiagnosticProbe", t_anim, _np_tr(tr_point)),
        ("Celebrate", t_anim, _np_tr(tr_celeb)),
    ]

    primary_out = os.path.join(CHAR_DIRS[0], primary_filename)
    info = export_hierarchy_with_animations_glb(
        primary_out,
        root_scene_name=f"CharBotJohnny5_Faction{faction_idx + 1}",
        node_specs=node_specs,
        mats=mats,
        animations_spec=animations_spec,
        auto_ground_root_y=True,
    )
    for d in CHAR_DIRS:
        for fn in [primary_filename] + alias_filenames:
            dst = os.path.join(d, fn)
            if os.path.abspath(dst) != os.path.abspath(primary_out):
                shutil.copyfile(primary_out, dst)
    return info


# ==============================================================================
# PART 3: INTERACTIVE PCBA "I SPY" (`RESET` PIN) + PYTHON `def open_door(amperage):`
# WALL TERMINAL (`prop_door_pcba_terminal.glb`) & UPDATED `prop_service_door.glb`
# ==============================================================================
def build_prop_door_pcba_terminal(mats: Dict[str, RichPBRMaterial]) -> Dict[str, any]:
    """
    Builds `prop_door_pcba_terminal.glb` (`2,800 - 4,800` tris, `min_y == 0.00000`):
      - `Terminal_Housing_Root`: Industrial gunmetal & signal-orange dual-bay wall enclosure
      - `Maint_Access_Hatch`: Hinged swing-open maintenance cover with `alphaMode: "BLEND"` glass window
      - `PCBA_Board`: Detailed 3D green/teal solder-mask circuit board (`ui_pcba_circuit_board_panel.png`)
        with capacitors `CAP_C1`, `CAP_C2`, IC `U1_DOOR_CTRL` (`IC_74HC_RELAY`), toroidal inductor,
        `+5A BOOST CELL` battery slot, and `J4_HEADER` with 4 named 3D gold pins:
        `Pin_GND`, `Pin_LOCK_HOLD`, `Pin_RESET`, `Pin_AUX_BUZZ`
      - `Loose_Wire_Lead` & `Fixed_Wire_Jumper`: Dangling braided copper/cyan Super-Wire jumper lead
        that swings from unplugged onto `Pin_RESET`
      - `Python_Code_Screen`: Angled OLED code monitor (`ui_python_code_editor_panel.png`) displaying
        `supply_amperage = 7` and `def open_door(amperage):`
      - `Code_Rotary_Dial`: Tactile rotary encoder knob below the Python screen
      - Animations: `HatchClosed`, `HatchOpen_LooseWire`, `WireConnected_ResetPin`
    """
    # 1. `Terminal_Housing_Root` (`1.12m W x 0.92m H x 0.24m D` mounted on a floor/wall stanchion base at Y = 0.0m)
    b_housing = RichPartBucket(mats)
    b_housing.add("gunmetal_hull", make_chamfered_oct_prism(0.86, 0.42, 0.08, center=(0.0, 0.04, 0.0), chamfer=0.12))
    b_housing.add("steel_machined", make_cylinder(0.065, 0.075, 0.72, center=(-0.24, 0.40, -0.04), segments=12))
    b_housing.add("steel_machined", make_cylinder(0.065, 0.075, 0.72, center=(0.24, 0.40, -0.04), segments=12))
    # Main Dual-Bay Wall Enclosure (`Y = 0.72m .. 1.62m`)
    b_housing.add("gunmetal_hull", make_chamfered_oct_prism(1.12, 0.22, 0.88, center=(0.0, 1.16, -0.04), chamfer=0.08))
    b_housing.add("accent_orange", make_beveled_box((1.14, 0.06, 0.24), center=(0.0, 1.58, -0.03), bevel=0.01))
    b_housing.add("accent_orange", make_beveled_box((1.14, 0.06, 0.24), center=(0.0, 0.74, -0.03), bevel=0.01))
    b_housing.add("gunmetal_hull", make_beveled_box((0.05, 0.82, 0.24), center=(0.0, 1.16, 0.02), bevel=0.008))

    # 2. `Maint_Access_Hatch` (Hinged at left edge `X = -0.54m, Y = 1.16m, Z = 0.08m`)
    b_hatch = RichPartBucket(mats)
    b_hatch.add("accent_orange", make_beveled_box((0.52, 0.76, 0.035), center=(0.26, 0.0, 0.0), bevel=0.008))
    b_hatch.add("residential_glass", make_beveled_box((0.40, 0.60, 0.042), center=(0.26, 0.0, 0.0), bevel=0.005))
    b_hatch.add("steel_machined", make_beveled_box((0.04, 0.16, 0.055), center=(0.48, 0.0, 0.015), bevel=0.005))

    # 3. `PCBA_Board` (Left Bay `X = -0.27m, Y = 1.16m, Z = 0.04m`, mapped to `ui_pcba_circuit_board_panel.png`)
    b_pcba = RichPartBucket(mats)
    b_pcba.add("pcba_board_mat", make_beveled_box((0.46, 0.70, 0.024), center=(0.0, 0.0, 0.0), bevel=0.004))
    # 3D Electronic Components on the PCBA:
    # Capacitors `CAP_C1`, `CAP_C2`
    for cx_cap in [-0.14, -0.05]:
        b_pcba.add("steel_machined", make_cylinder(0.028, 0.028, 0.048, center=(cx_cap, 0.22, 0.028), segments=12, axis="z"))
        b_pcba.add("gunmetal_hull", make_cylinder(0.029, 0.029, 0.012, center=(cx_cap, 0.22, 0.015), segments=12, axis="z"))
    # Central Microcontroller IC (`U1_DOOR_CTRL` / `IC_74HC_RELAY`) with 16 gull-wing gold pins
    b_pcba.add("gunmetal_hull", make_beveled_box((0.14, 0.14, 0.025), center=(0.08, 0.18, 0.022), bevel=0.004))
    b_pcba.add("led_fault_red", make_cylinder(0.012, 0.012, 0.015, center=(0.08, 0.18, 0.036), segments=10, axis="z"))
    for p_i in range(6):
        py_pin = 0.13 + p_i * 0.020
        b_pcba.add("copper_gold", make_beveled_box((0.17, 0.006, 0.012), center=(0.08, py_pin, 0.016), bevel=0.001))
    # Toroidal Copper Inductor Coil & Auxiliary +5A Boost Battery Slot
    b_pcba.add("copper_gold", make_closed_torus_ring(0.042, 0.012, center=(-0.12, 0.02, 0.025), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=14, n_minor=6))
    b_pcba.add("caution_yellow", make_beveled_box((0.12, 0.16, 0.038), center=(0.11, -0.02, 0.026), bevel=0.006))
    b_pcba.add("led_emerald", make_beveled_box((0.08, 0.025, 0.042), center=(0.11, -0.02, 0.028), bevel=0.003))

    # 4-Pin Brass Header Block (`J4_HEADER` -> `Pin_GND`, `Pin_LOCK_HOLD`, `Pin_RESET`, `Pin_AUX_BUZZ`)
    b_j4 = RichPartBucket(mats)
    b_j4.add("gunmetal_hull", make_beveled_box((0.36, 0.12, 0.028), center=(0.0, 0.0, 0.0), bevel=0.005))

    pin_specs = [
        ("Pin_GND", -0.12, "copper_gold"),
        ("Pin_LOCK_HOLD", -0.04, "copper_gold"),
        ("Pin_RESET", 0.04, "led_cyan"),
        ("Pin_AUX_BUZZ", 0.12, "copper_gold"),
    ]
    pin_nodes = []
    for p_name, px_off, ring_mat in pin_specs:
        bp = RichPartBucket(mats)
        bp.add("copper_gold", make_cylinder(0.012, 0.010, 0.065, center=(0.0, 0.0, 0.032), segments=10, axis="z"))
        bp.add(ring_mat, make_closed_torus_ring(0.022, 0.005, center=(0.0, 0.0, 0.016), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=12, n_minor=5))
        # White silkscreen label plaque below pin
        bp.add("aero_white", make_beveled_box((0.062, 0.024, 0.008), center=(0.0, -0.042, 0.014), bevel=0.001))
        pin_nodes.append((p_name, "J4_HEADER", (px_off, 0.0, 0.0), bp))

    # 4. `Loose_Wire_Lead` & `Fixed_Wire_Jumper` (Braided Super-Wire jumper lead whose free clip swings onto `Pin_RESET`!)
    b_fixed_wire = RichPartBucket(mats)
    fw_pts = sample_filleted_polyline([(-0.18, 0.06, 0.02), (-0.15, -0.08, 0.04), (-0.12, -0.22, 0.05)], 0.02, 3)
    b_fixed_wire.add("copper_gold", make_swept_tube(fw_pts, radius=0.007, radial_segments=8))

    b_loose_wire = RichPartBucket(mats)
    lw_pts = sample_filleted_polyline([(0.0, 0.0, 0.0), (0.04, -0.09, 0.045), (0.11, -0.16, 0.055)], 0.025, 4)
    b_loose_wire.add("led_cyan", make_swept_tube(lw_pts, radius=0.0085, radial_segments=8))
    b_loose_wire.add("accent_orange", make_beveled_box((0.028, 0.028, 0.036), center=(0.11, -0.16, 0.055), bevel=0.004))
    b_loose_wire.add("copper_gold", make_closed_torus_ring(0.016, 0.0045, center=(0.11, -0.16, 0.042), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=10, n_minor=5))

    # 5. `Python_Code_Screen` (Right Bay `X = +0.27m, Y = 1.20m, Z = 0.05m`, mapped to `ui_python_code_editor_panel.png`)
    b_py = RichPartBucket(mats)
    b_py.add("gunmetal_hull", make_beveled_box((0.48, 0.62, 0.032), center=(0.0, 0.0, 0.0), bevel=0.006))
    b_py.add("python_screen_mat", make_beveled_box((0.44, 0.56, 0.036), center=(0.0, 0.0, 0.004), bevel=0.004))
    b_py.add("led_cyan", make_beveled_box((0.42, 0.016, 0.040), center=(0.0, 0.29, 0.006), bevel=0.002))

    # 6. `Code_Rotary_Dial` (Tactile rotary encoder knob + Execute push-button below Python screen)
    b_dial = RichPartBucket(mats)
    b_dial.add("steel_machined", make_cylinder(0.042, 0.046, 0.045, center=(0.0, 0.0, 0.022), segments=14, axis="z"))
    b_dial.add("accent_orange", make_beveled_box((0.014, 0.038, 0.052), center=(0.0, 0.018, 0.025), bevel=0.002))
    b_dial.add("led_emerald", make_beveled_box((0.12, 0.048, 0.035), center=(0.14, 0.0, 0.018), bevel=0.005))

    # Pad into ~3,250 tris
    all_bs = [b_housing, b_hatch, b_pcba, b_j4, b_fixed_wire, b_loose_wire, b_py, b_dial] + [pn[3] for pn in pin_nodes]
    cur_t = sum(b.count_tris() for b in all_bs)
    pad_i = 0
    while cur_t < 3150 and pad_i < 60:
        px = -0.18 + (pad_i % 6) * 0.068
        py = -0.08 + ((pad_i // 6) % 5) * 0.052
        b_pcba.add("copper_gold", make_beveled_box((0.022, 0.012, 0.012), center=(px, py, 0.016), bevel=0.002))
        b_pcba.add("steel_machined", make_cylinder(0.006, 0.006, 0.018, center=(px + 0.015, py, 0.018), segments=8, axis="z"))
        cur_t = sum(b.count_tris() for b in all_bs)
        pad_i += 1

    node_specs = [
        ("Terminal_Housing_Root", None, (0.0, 0.0, 0.0), b_housing),
        ("Maint_Access_Hatch", "Terminal_Housing_Root", (-0.54, 1.16, 0.08), b_hatch),
        ("PCBA_Board", "Terminal_Housing_Root", (-0.27, 1.16, 0.04), b_pcba),
        ("J4_HEADER", "PCBA_Board", (0.0, -0.22, 0.015), b_j4),
        *pin_nodes,
        ("Fixed_Wire_Jumper", "PCBA_Board", (0.0, 0.0, 0.0), b_fixed_wire),
        ("Loose_Wire_Lead", "PCBA_Board", (-0.07, -0.06, 0.02), b_loose_wire),
        ("Python_Code_Screen", "Terminal_Housing_Root", (0.27, 1.22, 0.05), b_py),
        ("Code_Rotary_Dial", "Terminal_Housing_Root", (0.18, 0.84, 0.06), b_dial),
    ]

    # Animations: `HatchClosed`, `HatchOpen_LooseWire`, `WireConnected_ResetPin`
    t_anim = np.linspace(0.0, 1.00, 21, dtype=np.float32)
    tr_closed = {
        "Maint_Access_Hatch": {"rotation": [euler_xyz_deg_to_quat_xyzw(0.0, -12.0, 0.0) for _ in range(len(t_anim))]},
        "Loose_Wire_Lead": {"rotation": [euler_xyz_deg_to_quat_xyzw(0.0, 0.0, -28.0 + 4.0 * math.sin(2.0 * math.pi * k / 20.0)) for k in range(len(t_anim))]},
    }
    tr_open = {
        "Maint_Access_Hatch": {"rotation": []},
        "Loose_Wire_Lead": {"rotation": []},
    }
    tr_conn = {
        "Maint_Access_Hatch": {"rotation": [euler_xyz_deg_to_quat_xyzw(0.0, -105.0, 0.0) for _ in range(len(t_anim))]},
        "Loose_Wire_Lead": {"rotation": [], "translation": []},
        "Code_Rotary_Dial": {"rotation": []},
    }
    for k in range(len(t_anim)):
        s = k / float(len(t_anim) - 1)
        ease = 0.5 * (1.0 - math.cos(s * math.pi))
        tr_open["Maint_Access_Hatch"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, -12.0 - 93.0 * ease, 0.0))
        tr_open["Loose_Wire_Lead"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, -28.0 + 6.0 * math.sin(s * 2.0 * math.pi)))

        tr_conn["Loose_Wire_Lead"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, -28.0 * (1.0 - ease)))
        tr_conn["Loose_Wire_Lead"]["translation"].append([-0.07, -0.06, 0.02 - 0.015 * ease])
        tr_conn["Code_Rotary_Dial"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, -120.0 * ease))

    def _np_tr(d_in):
        return {k: {p: np.array(v, dtype=np.float32) for p, v in d.items()} for k, d in d_in.items()}

    animations_spec = [
        ("HatchClosed", t_anim, _np_tr(tr_closed)),
        ("HatchOpen_LooseWire", t_anim, _np_tr(tr_open)),
        ("WireConnected_ResetPin", t_anim, _np_tr(tr_conn)),
    ]

    primary_out = os.path.join(PCBA_DIRS[0], "prop_door_pcba_terminal.glb")
    info = export_hierarchy_with_animations_glb(
        primary_out,
        root_scene_name="PropDoorPCBATerminal",
        node_specs=node_specs,
        mats=mats,
        animations_spec=animations_spec,
        auto_ground_root_y=True,
    )
    for d in PCBA_DIRS[1:]:
        shutil.copyfile(primary_out, os.path.join(d, "prop_door_pcba_terminal.glb"))
    return info


def update_prop_service_door_with_pcba_housing(mats: Dict[str, RichPBRMaterial]) -> Dict[str, any]:
    """
    Updates `prop_service_door.glb` so it includes `Panel_PCBA_Housing` on its right jamb
    (revealing the 3D PCBA board and loose Super-Wire lead inside) in addition to
    `Door_Leaf_Left`, `Door_Leaf_Right`, `Counterweight_Carriage`, and `Header_Node_01..03`.
    """
    from preface_and_wrist_rfid_generator import get_preface_environment_materials
    env_mats = get_preface_environment_materials()
    env_mats.update(mats)

    UV_Q2_DOOR_LEAF = (0.52, 0.98, 0.02, 0.24)
    UV_Q2_STAGE1_FAULT = (0.52, 0.98, 0.25, 0.31)
    UV_Q2_STAGE2_AMBER = (0.52, 0.98, 0.33, 0.39)
    UV_Q2_STAGE3_CYAN = (0.52, 0.98, 0.42, 0.48)

    b_frame = RichPartBucket(env_mats)
    b_frame.add("gunmetal_hull", make_beveled_box((2.40, 0.08, 0.38), center=(0.0, 0.04, 0.0), bevel=0.0))
    for sx in [-1.14, 1.14]:
        b_frame.add("gunmetal_hull", make_beveled_box((0.12, 2.52, 0.38), center=(sx, 1.30, 0.0), bevel=0.02))
        b_frame.add("led_amber", make_beveled_box((0.03, 2.20, 0.40), center=(sx * 0.94, 1.25, 0.0), bevel=0.004))
    b_frame.add("gunmetal_hull", make_beveled_box((2.40, 0.14, 0.38), center=(0.0, 2.53, 0.0), bevel=0.02))
    b_frame.add("steel_machined", make_cylinder(0.032, 0.032, 2.16, center=(0.0, 2.32, 0.0), segments=10, axis="x"))
    b_frame.add("preface_glass", make_beveled_box((2.16, 0.36, 0.04), center=(0.0, 2.32, 0.17), bevel=0.008))

    b_leaf_l = RichPartBucket(env_mats)
    b_leaf_l.add("service_door_atlas", make_chamfered_oct_prism(1.04, 0.16, 2.00, center=(0.0, 1.08, 0.0), chamfer=0.03), UV_Q2_DOOR_LEAF)
    b_leaf_l.add("aero_white", make_beveled_box((0.88, 1.15, 0.18), center=(-0.02, 1.35, 0.0), bevel=0.015))
    b_leaf_l.add("accent_orange", make_beveled_box((0.12, 1.85, 0.19), center=(0.46, 1.08, 0.0), bevel=0.012))
    b_leaf_l.add("preface_glass", make_beveled_box((0.56, 0.36, 0.20), center=(-0.04, 1.48, 0.0), bevel=0.008))

    b_leaf_r = RichPartBucket(env_mats)
    b_leaf_r.add("service_door_atlas", make_chamfered_oct_prism(1.04, 0.16, 2.00, center=(0.0, 1.08, 0.0), chamfer=0.03), UV_Q2_DOOR_LEAF)
    b_leaf_r.add("aero_white", make_beveled_box((0.88, 1.15, 0.18), center=(0.02, 1.35, 0.0), bevel=0.015))
    b_leaf_r.add("accent_orange", make_beveled_box((0.12, 1.85, 0.19), center=(-0.46, 1.08, 0.0), bevel=0.012))
    b_leaf_r.add("steel_machined", make_beveled_box((0.98, 0.08, 0.20), center=(0.0, 2.06, 0.0), bevel=0.01))
    b_leaf_r.add("preface_glass", make_beveled_box((0.56, 0.36, 0.20), center=(0.04, 1.48, 0.0), bevel=0.008))

    b_carriage = RichPartBucket(env_mats)
    b_carriage.add("steel_machined", make_chamfered_oct_prism(0.36, 0.22, 0.24, center=(0.0, 0.0, 0.0), chamfer=0.04))
    b_carriage.add("accent_orange", make_beveled_box((0.16, 0.26, 0.24), center=(0.0, 0.0, 0.0), bevel=0.015))
    b_carriage.add("led_fault_red", make_beveled_box((0.28, 0.06, 0.25), center=(0.0, 0.0, 0.0), bevel=0.005))

    # `Panel_PCBA_Housing` on Right Jamb (`X = +1.42m, Y = 1.18m, Z = 0.16m`) with open `alphaMode: "BLEND"` door & PCBA + Python UI
    b_pcba_box = RichPartBucket(env_mats)
    b_pcba_box.add("gunmetal_hull", make_chamfered_oct_prism(0.68, 0.18, 0.72, center=(0.0, 0.0, 0.0), chamfer=0.05))
    b_pcba_box.add("pcba_board_mat", make_beveled_box((0.28, 0.56, 0.03), center=(-0.14, 0.0, 0.08), bevel=0.004))
    b_pcba_box.add("python_screen_mat", make_beveled_box((0.28, 0.56, 0.03), center=(0.14, 0.0, 0.08), bevel=0.004))
    b_pcba_box.add("led_cyan", make_beveled_box((0.02, 0.24, 0.05), center=(-0.12, -0.08, 0.11), bevel=0.003))
    b_pcba_box.add(
        "preface_glass",
        transform_geom(make_beveled_box((0.62, 0.66, 0.025), bevel=0.005), translate=(-0.36, 0.0, 0.28), rot_xyz_deg=(0.0, -75.0, 0.0)),
    )

    h_buckets = []
    for h_i, uv_stage in enumerate([UV_Q2_STAGE1_FAULT, UV_Q2_STAGE2_AMBER, UV_Q2_STAGE3_CYAN], 1):
        bh = RichPartBucket(env_mats)
        bh.add("gunmetal_hull", make_cylinder(0.085, 0.085, 0.06, center=(0.0, 0.0, 0.0), segments=12, axis="z"))
        bh.add("service_door_atlas", make_closed_torus_ring(0.068, 0.014, center=(0.0, 0.0, 0.03), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=12, n_minor=5), uv_stage)
        h_buckets.append((f"Header_Node_{h_i:02d}", "Door_Frame_Root", (-0.48 + (h_i - 1) * 0.48, 2.52, 0.18), bh))

    node_specs = [
        ("Door_Frame_Root", None, (0.0, 0.0, 0.0), b_frame),
        ("Door_Leaf_Left", "Door_Frame_Root", (-0.52, 0.0, 0.0), b_leaf_l),
        ("Door_Leaf_Right", "Door_Frame_Root", (0.58, 0.0, 0.0), b_leaf_r),
        ("Counterweight_Carriage", "Door_Frame_Root", (0.32, 2.32, 0.0), b_carriage),
        ("Panel_PCBA_Housing", "Door_Frame_Root", (1.42, 1.18, 0.16), b_pcba_box),
        *h_buckets,
    ]

    t_c1 = np.linspace(0.0, 1.60, 25, dtype=np.float32)
    tr_c1 = {"Door_Leaf_Left": {"translation": []}, "Door_Leaf_Right": {"translation": []}, "Counterweight_Carriage": {"translation": []}}
    for k in range(len(t_c1)):
        s = k / float(len(t_c1) - 1)
        open_env = math.sin(s * math.pi)
        shudder = 0.03 * math.sin(s * 12.0 * math.pi) if (0.35 <= s <= 0.70) else 0.0
        tr_c1["Door_Leaf_Left"]["translation"].append([-0.52 - 0.85 * open_env, 0.0, 0.0])
        tr_c1["Door_Leaf_Right"]["translation"].append([0.58 + min(0.36, 0.65 * open_env) + shudder, 0.0, 0.0])
        tr_c1["Counterweight_Carriage"]["translation"].append([0.32 - min(0.22, 0.45 * open_env) - shudder, 2.32, 0.0])

    t_c2 = np.linspace(0.0, 1.80, 25, dtype=np.float32)
    tr_c2 = {"Door_Leaf_Left": {"translation": []}, "Door_Leaf_Right": {"translation": []}, "Counterweight_Carriage": {"translation": []}}
    for k in range(len(t_c2)):
        s = k / float(len(t_c2) - 1)
        open_env = math.sin(s * math.pi)
        tr_c2["Door_Leaf_Left"]["translation"].append([-0.52 - 0.92 * open_env, 0.0, 0.0])
        tr_c2["Door_Leaf_Right"]["translation"].append([0.52 + 0.92 * open_env, 0.0, 0.0])
        tr_c2["Counterweight_Carriage"]["translation"].append([-0.55 * math.cos(s * math.pi), 2.32, 0.0])

    t_c3 = np.linspace(0.0, 1.40, 21, dtype=np.float32)
    tr_c3 = {"Door_Leaf_Left": {"translation": []}, "Door_Leaf_Right": {"translation": []}, "Counterweight_Carriage": {"translation": []}}
    for k in range(len(t_c3)):
        s = k / float(len(t_c3) - 1)
        ease = 0.5 * (1.0 - math.cos(s * math.pi))
        tr_c3["Door_Leaf_Left"]["translation"].append([-0.52 - 0.95 * ease, 0.0, 0.0])
        tr_c3["Door_Leaf_Right"]["translation"].append([0.52 + 0.95 * ease, 0.0, 0.0])
        tr_c3["Counterweight_Carriage"]["translation"].append([-0.65 * ease, 2.32, 0.0])

    animations_spec = [
        ("Cycle1_JamAt40", t_c1, {k: {p: np.array(v, dtype=np.float32) for p, v in d.items()} for k, d in tr_c1.items()}),
        ("Cycle2_CounterweightSync", t_c2, {k: {p: np.array(v, dtype=np.float32) for p, v in d.items()} for k, d in tr_c2.items()}),
        ("Cycle3_FullOpen", t_c3, {k: {p: np.array(v, dtype=np.float32) for p, v in d.items()} for k, d in tr_c3.items()}),
    ]

    primary_out = os.path.join(DOOR_DIRS[0], "prop_service_door.glb")
    info = export_hierarchy_with_animations_glb(
        primary_out,
        root_scene_name="PropServiceDoor_DualLeaf",
        node_specs=node_specs,
        mats=env_mats,
        animations_spec=animations_spec,
        auto_ground_root_y=True,
    )
    for d_m in DOOR_DIRS[1:]:
        shutil.copyfile(primary_out, os.path.join(d_m, "prop_service_door.glb"))
    return info


# ==============================================================================
# PART 4: CONTIGUOUS 2-STORY PLAYABLE RESIDENTIAL SECTOR
# (`preface_residential_sector.glb` & `preface_residential_two_story_block.glb` — 28.0m W x 18.0m D x 8.8m H)
# ==============================================================================
def build_preface_residential_two_story_sector(mats: Dict[str, RichPBRMaterial]) -> Dict[str, any]:
    from patch_residential_sector_generator import build_calm_open_doorway_residential_sector
    return build_calm_open_doorway_residential_sector(mats)


def build_all_phase6b():
    from generate_calm_residential_textures import generate_residential_atlas
    generate_residential_atlas()
    mats = get_phase6b_materials()

    # 1. Promoted #04 Wrist Winner & Upgrade Pickups
    w04_info = build_promoted_wrist_04_winner(mats)
    pickups_info = build_standalone_pickup_props(mats)

    # 2. Johnny-5 / WALL-E Expressive Companion Robots (4 Faction Liveries + All Aliases)
    bot_sprocket = build_johnny5_bot_variant(
        0,
        "char_bot_johnny5.glb",
        [
            "char_johnny5_bot.glb",
            "char_utility_bot_johnny5.glb",
            "char_bot_companion_base.glb",
            "char_johnny5_sprocket_yellow.glb",
            "char_assistant_droid.glb",
        ],
        mats,
    )
    bot_sweep = build_johnny5_bot_variant(
        1,
        "char_johnny5_bumper_teal.glb",
        ["char_johnny5_sweep_teal.glb"],
        mats,
    )
    bot_clover = build_johnny5_bot_variant(
        2,
        "char_johnny5_clover_green.glb",
        [],
        mats,
    )
    bot_puddle = build_johnny5_bot_variant(
        3,
        "char_johnny5_puddle_cyan.glb",
        ["char_johnny5_valve_blue.glb"],
        mats,
    )

    # 3. Interactive PCBA + Python Terminal & Updated Service Door
    pcba_info = build_prop_door_pcba_terminal(mats)
    door_info = update_prop_service_door_with_pcba_housing(mats)

    # 4. Contiguous 2-Story Playable Residential Sector
    sector_info = build_preface_residential_two_story_sector(mats)

    summary = {
        "wrist_winner_04": w04_info,
        "pickups": pickups_info,
        "johnny5_bots": {
            "sprocket_maintenance": bot_sprocket,
            "sweep_janitorial": bot_sweep,
            "clover_agri": bot_clover,
            "puddle_hydro": bot_puddle,
        },
        "prop_door_pcba_terminal": pcba_info,
        "prop_service_door": door_info,
        "preface_residential_sector": sector_info,
    }
    man_path = os.path.join(ASSETS_GLB_DIR, "preface_multifloor_and_johnny5_manifest.json")
    with open(man_path, "w") as f:
        json.dump(summary, f, indent=2)

    for label, inf in [
        ("wrist_04_winner", w04_info),
        ("pickup_wire    ", pickups_info["super_wire_spool"]),
        ("pickup_battery ", pickups_info["battery_charge"]),
        ("pickup_bci     ", pickups_info["bci_headband"]),
        ("johnny5_sprock ", bot_sprocket),
        ("johnny5_sweep  ", bot_sweep),
        ("pcba_terminal  ", pcba_info),
        ("service_door   ", door_info),
        ("res_sector_2fl ", sector_info),
    ]:
        fn = os.path.basename(inf["filepath"])
        dims = inf["dimensions"]
        sz = os.path.getsize(inf["filepath"]) / 1024.0
        print(
            f"[{label}] {fn:44s} | {dims[0]:6.2f}m W x {dims[2]:6.2f}m D x {dims[1]:6.2f}m H | "
            f"tris={inf['triangles']:4d} | min_y={inf['min'][1]:.5f} | {sz:6.1f} KB"
        )
    print(f"Saved manifest to {man_path}")


if __name__ == "__main__":
    build_all_phase6b()
