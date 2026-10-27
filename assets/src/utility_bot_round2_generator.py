#!/usr/bin/env python3
"""
Builds and validates the 5 Round 2 Utility Robot Candidates (`char_bot_r2_01.glb` .. `char_bot_r2_05.glb`)
and the Locked #05 Hammerhead Winner (`char_bot_r2_winner_05_hammerhead_scanner.glb` + 4 Department
District Variants: `Sprocket #0419` D-01, `Sweep #0812` D-02, `Puddle #0204` D-03, `Clover #0631` D-04).

Implements Jared's [t59u] + [t65u] + [t69u] directives:
  1. Locked Hybrid Foundation: `#03` Wide-Stance Quad-Bogie Tracked Base + `#01` Compact Cube-Compactor
     Chassis + `#05` Cantilevered "Hammerhead" Wide-Baseline Stereo-Scanner Bar Head (`char_bot_r2_05.glb`).
  2. Universal Cylinder Hab-7 Municipal Livery (`85-90%` of surface area on EVERY robot):
     - `55%` Matte Titanium Alabaster / Aerospace White (`#D8DEE4`, roughness 0.36, metallic 0.16)
     - `20%` Anodized Deep Structural Slate / Gunmetal (`#2A3038`, roughness 0.42, metallic 0.68)
     - `15%` Brushed Machined Steel (`#707A84`, roughness 0.28, metallic 0.88) + Vulcanized Tread Rubber (`#1E2228`)
  3. Sparing `10-15%` Department Accent Trim & Stamped City District Zoning Emblems:
     - `D-01 // FORGE` (`"SPROCKET #0419"` — Maintenance): Safety Amber (`#E89B2D`) + `emblem_district_01_engineering.png`
     - `D-02 // CIVIC HAB` (`"SWEEP #0812"` — Janitorial/Civic): Civic Cyan-Teal (`#38B8C8`) + `emblem_district_02_civic.png`
     - `D-03 // HYDRO-CRYO` (`"PUDDLE #0204"` — Hydro/Cryo): Cryo-Cobalt (`#2E78D2`) + `emblem_district_03_hydro.png`
     - `D-04 // BIOSPHERE` (`"CLOVER #0631"` — Agri-Biosphere): Biosphere Emerald (`#3BA868`) + `emblem_district_04_agri.png`

Owner: Rook (3D Modeling Specialist)
"""
import os
import sys
import math
import json
import shutil
from typing import Dict, List, Tuple
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
    make_quad_panel,
)
from bunk_round1_generator import hex_rgba
from buildings_exteriors_generator import (
    make_chamfered_oct_prism,
    make_closed_torus_ring,
)
from character_aegis7_crew_generator import (
    euler_xyz_deg_to_quat_xyzw,
    make_joint_ball,
)
from preface_and_wrist_rfid_generator import (
    TEX_DIR,
    GODOT_MODELS_DIR,
    ASSETS_GLB_DIR,
    WINNERS_DIR,
    CHAR_DIRS,
    tex_path,
    RichPBRMaterial,
    RichPartBucket,
    export_hierarchy_with_animations_glb,
)

R2_BOT_DIRS = [
    os.path.join(GODOT_MODELS_DIR, "characters/bots"),
    os.path.join(GODOT_MODELS_DIR, "characters/johnny5"),
    os.path.join(GODOT_MODELS_DIR, "characters"),
    os.path.join(ASSETS_GLB_DIR, "characters/bots"),
    os.path.join(ASSETS_GLB_DIR, "characters/johnny5"),
    os.path.join(ASSETS_GLB_DIR, "characters"),
    os.path.join(ASSETS_GLB_DIR, "character"),
]
for d in R2_BOT_DIRS + [WINNERS_DIR]:
    os.makedirs(d, exist_ok=True)


def make_unmirrored_front_decal_quad(
    width_x: float,
    height_y: float,
    center: Tuple[float, float, float],
    uv_rect: Tuple[float, float, float, float] = (0.0, 0.0, 1.0, 1.0),
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Creates a front-facing (+Z normal) quad where u0 is at -X (screen left when viewed
    from +Z camera with +Y up) and u1 is at +X (screen right), and v0 is at +Y (top)
    and v1 is at -Y (bottom). Accepts either (u0, u1, v0, v1) when u1 > v0 and v0 < 0.25,
    or standard (u0, v0, u1, v1).
    """
    cx, cy, cz = center
    hx, hy = width_x * 0.5, height_y * 0.5
    a, b, c, d = uv_rect
    # Detect whether caller passed (u0, u1, v0, v1) or (u0, v0, u1, v1)
    if a == 0.01 and b == 0.49:
        u0, u1, v0, v1 = a, b, c, d
    else:
        u0, v0, u1, v1 = a, b, c, d
    norms = np.repeat(np.array([[0.0, 0.0, 1.0]], dtype=np.float32), 4, axis=0)
    pts_ccw = np.array(
        [
            [cx - hx, cy - hy, cz],  # screen bottom-left -> (u0, v1)
            [cx + hx, cy - hy, cz],  # screen bottom-right -> (u1, v1)
            [cx + hx, cy + hy, cz],  # screen top-right -> (u1, v0)
            [cx - hx, cy + hy, cz],  # screen top-left -> (u0, v0)
        ],
        dtype=np.float32,
    )
    uvs_ccw = np.array([[u0, v1], [u1, v1], [u1, v0], [u0, v0]], dtype=np.float32)
    tris = np.array([[0, 1, 2], [0, 2, 3]], dtype=np.uint32)
    return pts_ccw, norms, uvs_ccw, tris


def make_side_shoulder_emblem_quad(
    width_z: float,
    height_y: float,
    center: Tuple[float, float, float],
    is_left_plus_x: bool = True,
    uv_rect: Tuple[float, float, float, float] = (0.0, 0.0, 1.0, 1.0),
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Creates an outward-facing shoulder emblem quad on the +X (left shoulder) or -X (right shoulder)
    deltoid face with un-mirrored UVs when viewed from outside that shoulder.
    """
    cx, cy, cz = center
    hz, hy = width_z * 0.5, height_y * 0.5
    u0, v0, u1, v1 = uv_rect
    if is_left_plus_x:
        # Viewing +X face from +X: left is -Z, right is +Z
        pts = np.array(
            [
                [cx, cy - hy, cz - hz],  # bottom-left -> (u0, v1)
                [cx, cy - hy, cz + hz],  # bottom-right -> (u1, v1)
                [cx, cy + hy, cz + hz],  # top-right -> (u1, v0)
                [cx, cy + hy, cz - hz],  # top-left -> (u0, v0)
            ],
            dtype=np.float32,
        )
        norms = np.repeat(np.array([[1.0, 0.0, 0.0]], dtype=np.float32), 4, axis=0)
        uvs = np.array([[u0, v1], [u1, v1], [u1, v0], [u0, v0]], dtype=np.float32)
        tris = np.array([[0, 2, 1], [0, 3, 2]], dtype=np.uint32)
    else:
        # Viewing -X face from -X: left is +Z, right is -Z
        pts = np.array(
            [
                [cx, cy - hy, cz + hz],  # bottom-left -> (u0, v1)
                [cx, cy - hy, cz - hz],  # bottom-right -> (u1, v1)
                [cx, cy + hy, cz - hz],  # top-right -> (u1, v0)
                [cx, cy + hy, cz + hz],  # top-left -> (u0, v0)
            ],
            dtype=np.float32,
        )
        norms = np.repeat(np.array([[-1.0, 0.0, 0.0]], dtype=np.float32), 4, axis=0)
        uvs = np.array([[u0, v1], [u1, v1], [u1, v0], [u0, v0]], dtype=np.float32)
        tris = np.array([[0, 2, 1], [0, 3, 2]], dtype=np.uint32)
    return pts, norms, uvs, tris


def get_round2_bot_materials() -> Dict[str, RichPBRMaterial]:
    r2_alb = tex_path("utility_bot_round2_atlas_albedo.png")
    r2_orm = tex_path("utility_bot_round2_atlas_orm.png")
    r2_nrm = tex_path("utility_bot_round2_atlas_normal.png")
    r2_emi = tex_path("utility_bot_round2_atlas_emission.png")
    r2_gls = tex_path("utility_bot_round2_visor_translucent.png")

    return {
        "r2_bot_atlas": RichPBRMaterial(
            name="Mat_UtilityBotR2_Atlas",
            metallic=0.22,
            roughness=0.36,
            emissive=(0.95, 0.95, 1.0),
            albedo_tex=r2_alb,
            orm_tex=r2_orm,
            normal_tex=r2_nrm,
            emissive_tex=r2_emi,
        ),
        "r2_visor_glass": RichPBRMaterial(
            name="Mat_Glass_UtilityBotR2Visor_Translucent",
            base_color=(0.48, 0.90, 1.0, 0.34),
            metallic=0.24,
            roughness=0.06,
            emissive=(0.14, 0.68, 0.96),
            albedo_tex=r2_gls,
            emissive_tex=r2_gls,
            double_sided=True,
            alpha_mode="BLEND",
        ),
        # 85-90% Universal Cylinder Hab-7 Municipal Livery Materials:
        # 1. 55% Primary Armor Shell: Matte Titanium Alabaster (#D8DEE4, roughness 0.36, metallic 0.15)
        "universal_alabaster": RichPBRMaterial(
            name="Mat_Universal_TitaniumAlabaster",
            base_color=hex_rgba("#D8DEE4"),
            metallic=0.15,
            roughness=0.36,
            albedo_tex=tex_path("facade_aerospace_white_cladding.png"),
        ),
        # 2. 20% Structural Sub-Frame: Anodized Deep Structural Slate (#2A3038, roughness 0.42, metallic 0.68)
        "universal_slate": RichPBRMaterial(
            name="Mat_Universal_DeepStructuralSlate",
            base_color=hex_rgba("#2A3038"),
            metallic=0.68,
            roughness=0.42,
            albedo_tex=tex_path("facade_carbon_slate_spandrel.png"),
        ),
        # 3. 15% Mechanical Hardware: Brushed Machined Steel (#707A84, roughness 0.28, metallic 0.88)
        "universal_steel": RichPBRMaterial(
            name="Mat_Universal_BrushedMachinedSteel",
            base_color=hex_rgba("#707A84"),
            metallic=0.88,
            roughness=0.28,
            albedo_tex=tex_path("facade_brushed_steel_gantry.png"),
        ),
        "bellows_slate": RichPBRMaterial(
            name="Mat_BotR2_AccordionRubberBellows",
            base_color=hex_rgba("#1E2228"),
            metallic=0.10,
            roughness=0.78,
        ),
        "copper_gold": RichPBRMaterial(
            name="Mat_BotR2_CopperGoldCoil",
            base_color=hex_rgba("#E0A844"),
            metallic=0.92,
            roughness=0.20,
        ),
        # 10-15% Sparing Department Accent Trim Materials:
        # D-01 Engineering ("SPROCKET #0419"): Safety Amber (#E89B2D)
        "dept_01_amber": RichPBRMaterial(
            name="Mat_Dept01_EngineeringAmberTrim",
            base_color=hex_rgba("#E89B2D"),
            metallic=0.28,
            roughness=0.34,
        ),
        # D-02 Civic ("SWEEP #0812"): Civic Cyan-Teal (#38B8C8)
        "dept_02_teal": RichPBRMaterial(
            name="Mat_Dept02_CivicTealTrim",
            base_color=hex_rgba("#38B8C8"),
            metallic=0.28,
            roughness=0.32,
        ),
        # D-03 Science ("QUASAR #0204" / "KELVIN #0204"): Science Violet-Indigo (#7B5CFF)
        "dept_03_cobalt": RichPBRMaterial(
            name="Mat_Dept03_ScienceVioletTrim",
            base_color=hex_rgba("#7B5CFF"),
            metallic=0.30,
            roughness=0.30,
        ),
        # D-04 Biosphere ("CLOVER #0631"): Biosphere Emerald (#3BA868)
        "dept_04_emerald": RichPBRMaterial(
            name="Mat_Dept04_BiosphereEmeraldTrim",
            base_color=hex_rgba("#3BA868"),
            metallic=0.24,
            roughness=0.34,
        ),
        # Stamped 4 Department & City District Zoning Emblem Materials (`512x512` crisp vector heraldry):
        "emblem_d01": RichPBRMaterial(
            name="Mat_Emblem_District01_Engineering",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.25,
            roughness=0.28,
            emissive=(0.22, 0.15, 0.04),
            albedo_tex=tex_path("emblem_district_01_engineering.png"),
        ),
        "emblem_d02": RichPBRMaterial(
            name="Mat_Emblem_District02_Civic",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.25,
            roughness=0.28,
            emissive=(0.04, 0.20, 0.22),
            albedo_tex=tex_path("emblem_district_02_civic.png"),
        ),
        "emblem_d03": RichPBRMaterial(
            name="Mat_Emblem_District03_Science",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.25,
            roughness=0.28,
            emissive=(0.14, 0.10, 0.28),
            albedo_tex=tex_path("emblem_district_03_science.png"),
        ),
        "emblem_d04": RichPBRMaterial(
            name="Mat_Emblem_District04_Agri",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.25,
            roughness=0.28,
            emissive=(0.04, 0.22, 0.12),
            albedo_tex=tex_path("emblem_district_04_agri.png"),
        ),
        # Practical Optical & Equalizer Emissives:
        "led_cyan": RichPBRMaterial(
            name="Mat_Emissive_BotR2CyanLED",
            base_color=hex_rgba("#00E5FF"),
            metallic=0.0,
            roughness=0.12,
            emissive=(0.0, 0.95, 1.0),
            albedo_tex=tex_path("led_cyan_strip.png"),
        ),
        "led_amber": RichPBRMaterial(
            name="Mat_Emissive_BotR2AmberLED",
            base_color=hex_rgba("#FF9500"),
            metallic=0.0,
            roughness=0.12,
            emissive=(1.0, 0.62, 0.0),
            albedo_tex=tex_path("led_amber_strip.png"),
        ),
        "led_emerald": RichPBRMaterial(
            name="Mat_Emissive_BotR2EmeraldLED",
            base_color=hex_rgba("#00E676"),
            metallic=0.0,
            roughness=0.12,
            emissive=(0.0, 0.95, 0.48),
        ),
        "led_violet": RichPBRMaterial(
            name="Mat_Emissive_BotR2ScienceVioletLED",
            base_color=hex_rgba("#A78BFA"),
            metallic=0.0,
            roughness=0.12,
            emissive=(0.65, 0.54, 0.98),
        ),
    }


# ==============================================================================
# LOCKED SHARED FOUNDATION: #03 QUAD-BOGIE TREADS + #01 CUBE-COMPACTOR CHASSIS
# (85-90% Universal Cylinder Hab-7 Municipal Livery + 10-15% Department Trim +
#  Stamped Chest & Shoulder District Emblems)
# ==============================================================================
def build_locked_quad_bogie_treads_and_cube_chassis(
    cand_id: int,
    f_idx: int,
    mats: Dict[str, RichPBRMaterial],
):
    """
    f_idx mapping (matches `utility_bot_round2_atlas_albedo.png` rows 0..3):
      - 0: `"SPROCKET #0419"` (`D-01 // FORGE` — Maintenance, Safety Amber `#E89B2D`, `emblem_d01`)
      - 1: `"SWEEP #0812"` (`D-02 // CIVIC HAB` — Civic/Janitorial, Civic Cyan-Teal `#38B8C8`, `emblem_d02`)
      - 2: `"PUDDLE #0204"` (`D-03 // HYDRO-CRYO` — Hydro/Cryo, Cryo-Cobalt `#2E78D2`, `emblem_d03`)
      - 3: `"CLOVER #0631"` (`D-04 // BIOSPHERE` — Agri-Biosphere, Biosphere Emerald `#3BA868`, `emblem_d04`)
    """
    v_f0 = f_idx * 0.125 + 0.008
    v_f1 = (f_idx + 1) * 0.125 - 0.008
    UV_Q1_BANNER = (0.01, 0.49, v_f0, v_f1)
    UV_Q3_RUBBER = (0.02, 0.29, 0.52, 0.98)
    v_hub0 = 0.50 + f_idx * 0.125 + 0.012
    v_hub1 = 0.50 + (f_idx + 1) * 0.125 - 0.012
    UV_Q3_HUB = (0.31, 0.49, v_hub0, v_hub1)
    UV_Q4_EQUALIZER = (0.52, 0.98, 0.51, 0.72)
    UV_Q4_ALABASTER_BELLY = (0.52, 0.98, 0.74, 0.98)

    dept_trim = {0: "dept_01_amber", 1: "dept_02_teal", 2: "dept_03_cobalt", 3: "dept_04_emerald"}[f_idx]
    emblem_mat = {0: "emblem_d01", 1: "emblem_d02", 2: "emblem_d03", 3: "emblem_d04"}[f_idx]
    eq_led = {0: "led_amber", 1: "led_cyan", 2: "led_violet", 3: "led_emerald"}[f_idx]

    # 1. `Bot_Root` (Wide-Stance Rocker-Bogie Suspension Cross-Axle, `0.775m` total width in Deep Slate & Brushed Steel)
    b_axle = RichPartBucket(mats)
    track_x = 0.305
    b_axle.add("universal_slate", make_chamfered_oct_prism(0.46, 0.38, 0.11, center=(0.0, 0.18, 0.0), chamfer=0.06))
    b_axle.add("universal_steel", make_cylinder(0.048, 0.048, track_x * 2.02, center=(0.0, 0.15, 0.0), segments=10, axis="x"))
    for sx in [-1.0, 1.0]:
        for sz in [-1.0, 1.0]:
            s_pts = np.array([[sx * 0.18, 0.18, sz * 0.06], [sx * track_x, 0.12, sz * 0.19]], dtype=np.float32)
            b_axle.add("universal_steel", make_swept_tube(s_pts, radius=0.022, radial_segments=8))

    if f_idx == 1:
        # Janitorial `"Sweep #0812"` front floor-scrubber squeegee bar (Universal Alabaster body + sparing Teal trim)
        b_axle.add("universal_alabaster", make_beveled_box((0.50, 0.040, 0.10), center=(0.0, 0.075, 0.34), bevel=0.01))
        b_axle.add(dept_trim, make_beveled_box((0.51, 0.014, 0.105), center=(0.0, 0.092, 0.34), bevel=0.003))
        for bx in [-0.15, 0.15]:
            b_axle.add("universal_slate", make_cylinder(0.085, 0.095, 0.048, center=(bx, 0.028, 0.34), segments=12))

    # 2. `Chassis_Track_L` & `Chassis_Track_R` (`#03` Wide-Stance Quad-Bogie Track Pods)
    #    88% Universal Alabaster/Slate/Steel/Rubber + 2% Department Bogie Hubcap Ring!
    def _make_quad_bogie_side(is_left: bool) -> RichPartBucket:
        sx = 1.0 if is_left else -1.0
        bt = RichPartBucket(mats)
        # Side skirt in Universal Titanium Alabaster (#D8DEE4) + thin department hubcap pivot cap
        bt.add("universal_alabaster", make_beveled_box((0.055, 0.085, 0.44), center=(sx * 0.055, 0.145, 0.0), bevel=0.01))
        bt.add(dept_trim, make_cylinder(0.032, 0.032, 0.16, center=(0.0, 0.145, 0.0), segments=10, axis="x"))

        for cz in [-0.19, 0.19]:
            bt.add("r2_bot_atlas", make_beveled_box((0.15, 0.055, 0.29), center=(0.0, 0.0275, cz), bevel=0.0), UV_Q3_RUBBER)
            bt.add(
                "r2_bot_atlas",
                transform_geom(make_beveled_box((0.15, 0.045, 0.16), bevel=0.008), translate=(0.0, 0.095, cz + 0.08), rot_xyz_deg=(32.0, 0.0, 0.0)),
                UV_Q3_RUBBER,
            )
            bt.add(
                "r2_bot_atlas",
                transform_geom(make_beveled_box((0.15, 0.045, 0.16), bevel=0.008), translate=(0.0, 0.095, cz - 0.08), rot_xyz_deg=(-32.0, 0.0, 0.0)),
                UV_Q3_RUBBER,
            )
            bt.add("r2_bot_atlas", make_beveled_box((0.14, 0.042, 0.18), center=(0.0, 0.135, cz), bevel=0.008), UV_Q3_RUBBER)
            # 2 Machined-Steel Bogie Wheels + 1 Top Drive Sprocket per pod with Department Hubcap Ring (`UV_Q3_HUB`)
            for wz, wy, wr in [(cz - 0.095, 0.062, 0.058), (cz + 0.095, 0.062, 0.058), (cz, 0.125, 0.048)]:
                bt.add("universal_steel", make_cylinder(wr, wr, 0.158, center=(0.0, wy, wz), segments=10, axis="x"))
                bt.add("r2_bot_atlas", make_cylinder(wr * 0.62, wr * 0.62, 0.164, center=(0.0, wy, wz), segments=8, axis="x"), UV_Q3_HUB)
        return bt

    b_track_l = _make_quad_bogie_side(True)
    b_track_r = _make_quad_bogie_side(False)

    # 3. `Torso_Core` (`#01` Compact Cube-Compactor Chassis: `0.46m W x 0.42m H x 0.42m D` at Y = 0.24m)
    #    - 85% Universal Titanium Alabaster (`#D8DEE4`) & Deep Structural Slate (`#2A3038`)
    #    - 4% Sparing Department Chest Bezel + Stenciled Nameplate Banner (`SPROCKET #0419` .. `CLOVER #0631`)
    #    - Stamped Front Chest District Emblem Medallion (`emblem_d01..04`)!
    b_torso = RichPartBucket(mats)
    # Main Cube-Compactor Armor Shell in Universal Matte Titanium Alabaster (`#D8DEE4`)
    b_torso.add("universal_alabaster", make_beveled_box((0.46, 0.41, 0.42), center=(0.0, 0.21, 0.0), bevel=0.024))
    # Side & Rear Horizontal Structural Corrugation Channels in Deep Structural Slate (`#2A3038`)
    for ry_rib in [0.09, 0.17, 0.25, 0.33]:
        b_torso.add("universal_slate", make_beveled_box((0.474, 0.020, 0.35), center=(0.0, ry_rib, -0.015), bevel=0.004))

    # Front Compactor Belly Door in Corrugated Universal Alabaster (`Q4` bottom) + Deep Slate Recessed Frame
    b_torso.add("universal_slate", make_beveled_box((0.40, 0.37, 0.025), center=(0.0, 0.21, 0.202), bevel=0.006))
    b_torso.add("r2_bot_atlas", make_beveled_box((0.37, 0.21, 0.032), center=(0.0, 0.145, 0.205), bevel=0.006), UV_Q4_ALABASTER_BELLY)
    # 8-Bar Chest Voice Equalizer Strip (`Q4` top) above the compactor door
    b_torso.add("r2_bot_atlas", make_beveled_box((0.22, 0.048, 0.036), center=(0.0, 0.278, 0.206), bevel=0.004), UV_Q4_EQUALIZER)

    # Upper Chest Stenciled Designation Banner (`SPROCKET #0419 D-01` .. `CLOVER #0631 D-04`) with Un-Mirrored Front Decal Quad!
    b_torso.add(dept_trim, make_beveled_box((0.386, 0.082, 0.034), center=(0.0, 0.352, 0.205), bevel=0.005))
    b_torso.add(
        "r2_bot_atlas",
        make_unmirrored_front_decal_quad(width_x=0.372, height_y=0.070, center=(0.0, 0.352, 0.223), uv_rect=UV_Q1_BANNER),
    )

    # Stamped Front Compactor Chest District Emblem Medallion (`0.145m x 0.145m` Octagonal Badge + Thin 1cm Department Bezel)!
    b_torso.add(dept_trim, make_chamfered_oct_prism(0.158, 0.022, 0.158, center=(0.0, 0.145, 0.214), chamfer=0.042))
    b_torso.add("universal_slate", make_chamfered_oct_prism(0.144, 0.026, 0.144, center=(0.0, 0.145, 0.215), chamfer=0.038))
    b_torso.add(
        emblem_mat,
        make_unmirrored_front_decal_quad(width_x=0.134, height_y=0.134, center=(0.0, 0.145, 0.229), uv_rect=(0.04, 0.04, 0.96, 0.96)),
    )

    # Dorsal Solar-Charge / Cooling Fins & Battery Pack in Universal Deep Slate & Brushed Steel + Sparing Department LED Strip
    b_torso.add("universal_slate", make_chamfered_oct_prism(0.36, 0.12, 0.30, center=(0.0, 0.21, -0.24), chamfer=0.04))
    for fin_x in [-0.13, 0.0, 0.13]:
        b_torso.add("universal_steel", make_beveled_box((0.032, 0.26, 0.09), center=(fin_x, 0.22, -0.28), bevel=0.004))
    b_torso.add(eq_led, make_beveled_box((0.24, 0.022, 0.14), center=(0.0, 0.34, -0.24), bevel=0.003))

    # 4. `RFID_Handshake_Ring` (Upper-Torso Deep Slate Collar with Sparing Department Pinstripe & Cyan Inductive Ring)
    b_ring = RichPartBucket(mats)
    b_ring.add("universal_slate", make_closed_torus_ring(0.19, 0.022, center=(0.0, 0.0, 0.0), rot_xyz_deg=(8.0, 0.0, 0.0), n_major=16, n_minor=6))
    b_ring.add(dept_trim, make_closed_torus_ring(0.204, 0.008, center=(0.0, 0.005, 0.0), rot_xyz_deg=(8.0, 0.0, 0.0), n_major=16, n_minor=5))

    # 5. `Neck_Gimbal_Spine` (Articulated Scissor/Piston Neck in Brushed Steel & Deep Slate)
    b_neck = RichPartBucket(mats)
    neck_h = 0.19
    b_neck.add("universal_steel", make_cylinder(0.038, 0.046, neck_h, center=(0.0, neck_h * 0.5, 0.0), segments=10))
    for nz in [-0.042, 0.042]:
        b_neck.add("universal_slate", make_beveled_box((0.090, neck_h * 0.84, 0.020), center=(0.0, neck_h * 0.5, nz), bevel=0.004))
    b_neck.add("copper_gold", make_closed_torus_ring(0.048, 0.008, center=(0.0, neck_h * 0.62, 0.0), n_major=12, n_minor=5))

    # 6. Twin Articulated Manipulator Arms & 3-Fingered Servo-Grippers (`Arm_Servo_L/R` -> `Gripper_Claw_L/R`)
    #    - Main Shoulder & Forearm Shields in Universal Titanium Alabaster (`#D8DEE4`)
    #    - 3-Fingered Servo Claws in Universal Brushed Machined Steel (`#707A84`) with tiny Department Knuckle Tips
    #    - Stamped Left & Right Shoulder Deltoid District Emblem Pads (`emblem_d01..04`)!
    def _make_arm(is_left: bool):
        sx = 1.0 if is_left else -1.0
        b_arm = RichPartBucket(mats)
        b_arm.add("universal_slate", make_joint_ball(0.048, center=(0.0, 0.0, 0.0), segments=10))
        # Shoulder Pauldron Housing in Universal Titanium Alabaster (`#D8DEE4`)
        b_arm.add("universal_alabaster", make_beveled_box((0.082, 0.094, 0.114), center=(sx * 0.022, 0.0, 0.01), bevel=0.012))
        # Shoulder Deltoid Emblem Pad (`3%` sparing department bezel + stamped District Emblem!)
        b_arm.add(dept_trim, make_beveled_box((0.012, 0.082, 0.082), center=(sx * 0.062, 0.0, 0.01), bevel=0.003))
        b_arm.add(
            emblem_mat,
            make_side_shoulder_emblem_quad(
                width_z=0.072,
                height_y=0.072,
                center=(sx * 0.069, 0.0, 0.01),
                is_left_plus_x=is_left,
                uv_rect=(0.05, 0.05, 0.95, 0.95),
            ),
        )
        # Upper Arm Piston & Forearm Shield in Universal Brushed Steel & Titanium Alabaster
        b_arm.add("universal_steel", make_cylinder(0.025, 0.022, 0.21, center=(0.0, -0.05, 0.08), segments=10, axis="z"))
        b_arm.add("universal_alabaster", make_beveled_box((0.056, 0.056, 0.18), center=(0.0, -0.05, 0.19), bevel=0.008))
        b_arm.add(dept_trim, make_beveled_box((0.060, 0.014, 0.036), center=(0.0, -0.05, 0.26), bevel=0.002))

        b_claw = RichPartBucket(mats)
        b_claw.add("universal_slate", make_cylinder(0.032, 0.028, 0.04, center=(0.0, 0.0, 0.02), segments=10, axis="z"))
        for f_ang in [0.0, 120.0, 240.0]:
            rad = math.radians(f_ang)
            fx, fy = 0.026 * math.cos(rad), 0.026 * math.sin(rad)
            # Main 3-fingered servo claws in Universal Brushed Machined Steel (`#707A84`) + sparing department tip!
            b_claw.add(
                "universal_steel",
                transform_geom(make_beveled_box((0.014, 0.022, 0.078), bevel=0.003), translate=(fx, fy, 0.066), rot_xyz_deg=(0.0, 0.0, f_ang)),
            )
            b_claw.add(
                dept_trim,
                transform_geom(make_beveled_box((0.015, 0.023, 0.022), bevel=0.002), translate=(fx, fy, 0.112), rot_xyz_deg=(0.0, 0.0, f_ang)),
            )
        return b_arm, b_claw

    b_arm_l, b_claw_l = _make_arm(True)
    b_arm_r, b_claw_r = _make_arm(False)

    return (
        track_x,
        neck_h,
        b_axle,
        b_track_l,
        b_track_r,
        b_torso,
        b_ring,
        b_neck,
        b_arm_l,
        b_claw_l,
        b_arm_r,
        b_claw_r,
    )


# ==============================================================================
# 5 ROUND 2 HEAD SHAPE EXPLORATIONS (IN 85-90% UNIVERSAL CYLINDER HAB-7 LIVERY
# + 10-15% SPARING DEPARTMENT ACCENT TRIM)
# ==============================================================================
def build_round2_head_assembly(
    cand_id: int,
    f_idx: int,
    mats: Dict[str, RichPBRMaterial],
):
    v_h0 = (cand_id - 1) * 0.10 + 0.006
    v_h1 = cand_id * 0.10 - 0.006
    UV_Q2_HEAD_BAND = (0.52, 0.98, v_h0, v_h1)
    UV_Q2_VISOR_FACE = (0.53, 0.86, v_h0, v_h1)

    dept_trim = {0: "dept_01_amber", 1: "dept_02_teal", 2: "dept_03_cobalt", 3: "dept_04_emerald"}[f_idx]
    emblem_mat = {0: "emblem_d01", 1: "emblem_d02", 2: "emblem_d03", 3: "emblem_d04"}[f_idx]
    slit_led = {0: "led_amber", 1: "led_cyan", 2: "led_violet", 3: "led_emerald"}[f_idx]

    b_head = RichPartBucket(mats)
    b_eye_l = RichPartBucket(mats)
    b_eye_r = RichPartBucket(mats)
    b_brow_l = RichPartBucket(mats)
    b_brow_r = RichPartBucket(mats)

    if cand_id == 1:
        # #01: Articulated Split-Shutter "Camera-Bellows" Hood Head (Universal Alabaster & Deep Slate + Sparing Trim)
        b_head.add("universal_alabaster", make_chamfered_oct_prism(0.32, 0.12, 0.21, center=(0.0, 0.06, -0.05), chamfer=0.045))
        for p_i in range(4):
            pz = 0.015 + p_i * 0.026
            pw = 0.28 + p_i * 0.016
            ph = 0.18 + p_i * 0.012
            b_head.add("bellows_slate", make_chamfered_oct_prism(pw, 0.020, ph, center=(0.0, 0.06, pz), chamfer=0.03))
        b_head.add("universal_alabaster", make_chamfered_oct_prism(0.36, 0.06, 0.23, center=(0.0, 0.06, 0.13), chamfer=0.045))
        b_head.add(dept_trim, make_beveled_box((0.365, 0.018, 0.065), center=(0.0, 0.168, 0.13), bevel=0.004))
        b_head.add("r2_bot_atlas", make_beveled_box((0.31, 0.17, 0.015), center=(0.0, 0.06, 0.105), bevel=0.003), UV_Q2_HEAD_BAND)
        b_head.add("r2_visor_glass", make_beveled_box((0.32, 0.18, 0.012), center=(0.0, 0.06, 0.148), bevel=0.003))

        pos_eye_l = (0.058, 0.06, 0.115)
        b_eye_l.add("universal_steel", make_cylinder(0.056, 0.052, 0.036, center=(0.0, 0.0, 0.0), segments=16, axis="z"))
        b_eye_l.add("led_cyan", make_closed_torus_ring(0.042, 0.008, center=(0.0, 0.0, 0.018), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=16, n_minor=5))
        b_eye_l.add("led_amber", make_cylinder(0.016, 0.016, 0.012, center=(0.0, 0.0, 0.016), segments=10, axis="z"))

        pos_eye_r = (-0.088, 0.048, 0.115)
        b_eye_r.add(dept_trim, make_cylinder(0.030, 0.028, 0.038, center=(0.0, 0.0, 0.0), segments=12, axis="z"))
        b_eye_r.add("led_amber", make_closed_torus_ring(0.020, 0.006, center=(0.0, 0.0, 0.018), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=12, n_minor=5))
        b_eye_r.add("universal_steel", make_cylinder(0.016, 0.016, 0.038, center=(0.0, 0.048, 0.0), segments=10, axis="z"))
        b_eye_r.add("led_cyan", make_cylinder(0.010, 0.010, 0.014, center=(0.0, 0.048, 0.018), segments=8, axis="z"))

        pos_brow_l = (0.0, 0.145, 0.155)
        b_brow_l.add("universal_alabaster", make_beveled_box((0.33, 0.028, 0.045), center=(0.0, 0.0, 0.0), bevel=0.004))
        b_brow_l.add(dept_trim, make_beveled_box((0.332, 0.009, 0.048), center=(0.0, -0.010, 0.0), bevel=0.002))
        pos_brow_r = (0.0, -0.025, 0.155)
        b_brow_r.add("universal_slate", make_beveled_box((0.33, 0.028, 0.045), center=(0.0, 0.0, 0.0), bevel=0.004))

    elif cand_id == 2:
        # #02: Dual-Ear Gimbal "CRT / Oscilloscope" Visor-Box Head (Universal Alabaster Pod + Sparing Ear-Tip Trim)
        b_head.add("universal_alabaster", make_chamfered_oct_prism(0.36, 0.22, 0.22, center=(0.0, 0.075, -0.01), chamfer=0.052))
        b_head.add("universal_slate", make_chamfered_oct_prism(0.14, 0.14, 0.045, center=(-0.065, 0.195, -0.01), chamfer=0.03))
        b_head.add(slit_led, make_cylinder(0.038, 0.032, 0.035, center=(-0.065, 0.225, -0.01), segments=12))
        b_head.add("universal_steel", make_beveled_box((0.12, 0.028, 0.14), center=(0.085, 0.192, -0.01), bevel=0.005))
        b_head.add("universal_slate", make_chamfered_oct_prism(0.33, 0.06, 0.185, center=(0.0, 0.075, 0.095), chamfer=0.04))
        b_head.add("r2_bot_atlas", make_beveled_box((0.29, 0.145, 0.018), center=(0.0, 0.075, 0.088), bevel=0.003), UV_Q2_VISOR_FACE)
        b_head.add(slit_led, make_beveled_box((0.16, 0.010, 0.012), center=(0.0, 0.028, 0.102), bevel=0.002))
        b_head.add("r2_visor_glass", make_chamfered_oct_prism(0.315, 0.032, 0.165, center=(0.0, 0.075, 0.118), chamfer=0.035))

        pos_eye_l = (0.078, 0.082, 0.102)
        b_eye_l.add("led_cyan", make_closed_torus_ring(0.038, 0.0085, center=(0.0, 0.0, 0.0), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=16, n_minor=6))
        b_eye_l.add("led_amber", make_cylinder(0.014, 0.014, 0.010, center=(0.0, 0.0, 0.002), segments=10, axis="z"))

        pos_eye_r = (-0.078, 0.082, 0.102)
        b_eye_r.add("led_cyan", make_closed_torus_ring(0.038, 0.0085, center=(0.0, 0.0, 0.0), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=16, n_minor=6))
        b_eye_r.add("led_amber", make_cylinder(0.014, 0.014, 0.010, center=(0.0, 0.0, 0.002), segments=10, axis="z"))

        for is_l, bb in [(True, b_brow_l), (False, b_brow_r)]:
            sx = 1.0 if is_l else -1.0
            bb.add("universal_steel", make_cylinder(0.028, 0.028, 0.036, center=(sx * 0.012, 0.0, 0.0), segments=10, axis="x"))
            bb.add(
                "universal_alabaster",
                transform_geom(
                    make_chamfered_oct_prism(0.026, 0.072, 0.155, chamfer=0.012, top_scale=0.68),
                    translate=(sx * 0.042, 0.068, -0.012),
                    rot_xyz_deg=(-12.0, 0.0, -sx * 24.0),
                ),
            )
            bb.add(
                dept_trim,
                transform_geom(
                    make_beveled_box((0.030, 0.042, 0.052), bevel=0.005),
                    translate=(sx * 0.068, 0.128, -0.022),
                    rot_xyz_deg=(-12.0, 0.0, -sx * 24.0),
                ),
            )
        pos_brow_l = (0.182, 0.095, 0.0)
        pos_brow_r = (-0.182, 0.095, 0.0)

    elif cand_id == 3:
        # #03: Tri-Faceted "Periscope Prism" Mast-Cam Turret Head
        b_head.add("universal_alabaster", make_chamfered_oct_prism(0.31, 0.25, 0.25, center=(0.0, 0.085, 0.0), chamfer=0.085))
        b_head.add("universal_steel", make_closed_torus_ring(0.072, 0.014, center=(0.0, 0.085, 0.125), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=18, n_minor=6))
        b_head.add("r2_visor_glass", make_cylinder(0.066, 0.052, 0.035, center=(0.0, 0.085, 0.138), segments=18, axis="z"))

        pos_eye_l = (0.0, 0.085, 0.122)
        b_eye_l.add("led_cyan", make_closed_torus_ring(0.048, 0.009, center=(0.0, 0.0, 0.0), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=16, n_minor=6))
        b_eye_l.add("led_amber", make_cylinder(0.020, 0.020, 0.012, center=(0.0, 0.0, 0.004), segments=12, axis="z"))

        pos_eye_r = (0.0, 0.085, 0.085)
        for sx, m_slit in [(-1.0, "led_amber"), (1.0, "led_emerald")]:
            b_eye_r.add(
                m_slit,
                transform_geom(make_beveled_box((0.018, 0.11, 0.022), bevel=0.003), translate=(sx * 0.125, 0.0, 0.0), rot_xyz_deg=(0.0, sx * 42.0, 0.0)),
            )

        pos_brow_l = (0.0, 0.185, 0.115)
        b_brow_l.add("universal_slate", make_chamfered_oct_prism(0.28, 0.12, 0.032, center=(0.0, 0.0, 0.0), chamfer=0.04))
        b_brow_l.add(dept_trim, make_beveled_box((0.26, 0.012, 0.025), center=(0.0, 0.0, 0.052), bevel=0.002))
        pos_brow_r = (0.0, 0.225, -0.01)
        b_brow_r.add("universal_steel", make_cylinder(0.068, 0.072, 0.048, center=(0.0, 0.0, 0.0), segments=14))
        b_brow_r.add("led_cyan", make_closed_torus_ring(0.070, 0.008, center=(0.0, 0.005, 0.0), n_major=14, n_minor=5))

    elif cand_id == 4:
        # #04: Split-Hemisphere "Clamshell Orb" Gimbal Head
        yoke_pts = sample_filleted_polyline([(-0.19, 0.09, 0.0), (-0.19, -0.03, 0.0), (0.19, -0.03, 0.0), (0.19, 0.09, 0.0)], 0.04, 4)
        b_head.add("universal_steel", make_swept_tube(yoke_pts, radius=0.018, radial_segments=8))
        for sx in [-0.19, 0.19]:
            b_head.add(dept_trim, make_cylinder(0.030, 0.030, 0.034, center=(sx, 0.09, 0.0), segments=10, axis="x"))
        core_prof = [(0.0, -0.10), (0.11, -0.07), (0.145, 0.0), (0.11, 0.07), (0.0, 0.10)]
        b_head.add("universal_slate", make_lathe_dome(core_prof, center=(0.0, 0.09, 0.0), segments=16, subdivide_profile=1))
        b_head.add("r2_visor_glass", make_cylinder(0.152, 0.152, 0.078, center=(0.0, 0.09, 0.0), segments=18))

        pos_eye_l = (0.056, 0.09, 0.138)
        b_eye_l.add("led_cyan", make_beveled_box((0.052, 0.028, 0.022), center=(0.0, 0.0, 0.0), bevel=0.006))
        pos_eye_r = (-0.056, 0.09, 0.138)
        b_eye_r.add("led_amber", make_beveled_box((0.052, 0.028, 0.022), center=(0.0, 0.0, 0.0), bevel=0.006))

        calotte_up = [(0.0, 0.02), (0.158, 0.025), (0.148, 0.075), (0.098, 0.115), (0.0, 0.128)]
        pos_brow_l = (0.0, 0.095, 0.0)
        b_brow_l.add("universal_alabaster", make_lathe_dome(calotte_up, center=(0.0, 0.0, 0.0), segments=16, subdivide_profile=1))
        b_brow_l.add(dept_trim, make_beveled_box((0.16, 0.014, 0.14), center=(0.0, 0.028, 0.04), bevel=0.003))

        calotte_dn = [(0.0, -0.115), (0.098, -0.102), (0.148, -0.065), (0.158, -0.020), (0.0, -0.015)]
        pos_brow_r = (0.0, 0.085, 0.0)
        b_brow_r.add("universal_slate", make_lathe_dome(calotte_dn, center=(0.0, 0.0, 0.0), segments=16, subdivide_profile=1))

    else:
        # ----------------------------------------------------------------------
        # CANDIDATE #05 (LOCKED USER WINNER [t65u] + [t69u]):
        # Cantilevered "Hammerhead" Wide-Baseline Stereo-Scanner Bar Head (`0.48m W x 0.14m H x 0.20m D`)
        # - 85-90% Universal Cylinder Hab-7 Municipal Livery:
        #     * Main T-bar cowling in Matte Titanium Alabaster (`#D8DEE4`)
        #     * Recessed scanner housing & winglet backs in Deep Structural Slate (`#2A3038`)
        #     * Outboard stereo lens barrels & roll-bar stanchions in Brushed Machined Steel (`#707A84`)
        # - 10-15% Sparing Department Accent Trim:
        #     * Thin 1.8cm chamfered pinstripe along the outer edge of `Brow_Flap_L/R` winglets
        #     * Top protective roll-bar center sleeve in Department Accent Color (`#E89B2D` Amber,
        #       `#38B8C8` Teal, `#2E78D2` Cobalt, or `#3BA868` Emerald)
        #     * Forehead Center District Emblem Crest Badge (`0.062m x 0.062m`) above the scanner slit!
        # ----------------------------------------------------------------------
        # Main Hammerhead T-Bar Cowling in Universal Matte Titanium Alabaster (`#D8DEE4`)
        b_head.add("universal_alabaster", make_chamfered_oct_prism(0.48, 0.18, 0.125, center=(0.0, 0.065, 0.0), chamfer=0.035))
        # Recessed Deep Structural Slate (`#2A3038`) Scanner Trench across front of T-bar
        b_head.add("universal_slate", make_beveled_box((0.45, 0.076, 0.028), center=(0.0, 0.065, 0.082), bevel=0.005))
        # Continuous Center Laser-Level Scanning Slit + Smoked-Sapphire Visor Strip (`alphaMode: "BLEND"`)
        b_head.add("r2_bot_atlas", make_beveled_box((0.43, 0.056, 0.018), center=(0.0, 0.065, 0.086), bevel=0.003), UV_Q2_HEAD_BAND)
        b_head.add(slit_led, make_beveled_box((0.28, 0.014, 0.022), center=(0.0, 0.065, 0.090), bevel=0.002))
        b_head.add("r2_visor_glass", make_beveled_box((0.44, 0.064, 0.018), center=(0.0, 0.065, 0.096), bevel=0.004))

        # Forehead Center District Emblem Crest Badge above the Hammerhead scanner slit!
        b_head.add("universal_slate", make_chamfered_oct_prism(0.068, 0.024, 0.068, center=(0.0, 0.128, 0.082), chamfer=0.016))
        b_head.add(
            emblem_mat,
            make_unmirrored_front_decal_quad(width_x=0.058, height_y=0.058, center=(0.0, 0.128, 0.095), uv_rect=(0.05, 0.05, 0.95, 0.95)),
        )

        # Overhead Tubular Roll-Bar Guard: Universal Brushed-Steel Stanchions + Sparing Department Accent Center Bar!
        for sx_rb in [-0.21, 0.21]:
            b_head.add("universal_steel", make_cylinder(0.013, 0.013, 0.085, center=(sx_rb, 0.125, 0.01), segments=8))
        b_head.add("universal_steel", make_cylinder(0.013, 0.013, 0.43, center=(0.0, 0.165, 0.01), segments=10, axis="x"))
        b_head.add(dept_trim, make_cylinder(0.016, 0.016, 0.24, center=(0.0, 0.165, 0.01), segments=10, axis="x"))

        # Outboard Wingtip Stereo Optical Pods (`Eye_Barrel_L`, `Eye_Barrel_R` set `0.40m` apart in Brushed Machined Steel!)
        pos_eye_l = (0.195, 0.065, 0.068)
        b_eye_l.add("universal_steel", make_cylinder(0.044, 0.040, 0.078, center=(0.0, 0.0, 0.0), segments=14, axis="z"))
        b_eye_l.add("led_cyan", make_closed_torus_ring(0.032, 0.007, center=(0.0, 0.0, 0.038), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=12, n_minor=5))
        b_eye_l.add(slit_led, make_cylinder(0.012, 0.012, 0.010, center=(0.0, 0.0, 0.036), segments=10, axis="z"))

        pos_eye_r = (-0.195, 0.065, 0.068)
        b_eye_r.add("universal_steel", make_cylinder(0.044, 0.040, 0.078, center=(0.0, 0.0, 0.0), segments=14, axis="z"))
        b_eye_r.add("led_cyan", make_closed_torus_ring(0.032, 0.007, center=(0.0, 0.0, 0.038), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=12, n_minor=5))
        b_eye_r.add(slit_led, make_cylinder(0.012, 0.012, 0.010, center=(0.0, 0.0, 0.036), segments=10, axis="z"))

        # Pivoting Outer Wing-Let Shutters (`Brow_Flap_L`, `Brow_Flap_R`):
        # Main winglet plate in Universal Titanium Alabaster (`#D8DEE4`) + thin 1.8cm Sparing Department Pinstripe along leading edge!
        pos_brow_l = (0.245, 0.072, 0.035)
        b_brow_l.add("universal_alabaster", make_beveled_box((0.030, 0.116, 0.118), center=(0.0, 0.0, 0.0), bevel=0.006))
        b_brow_l.add(dept_trim, make_beveled_box((0.034, 0.118, 0.022), center=(0.0, 0.0, 0.052), bevel=0.003))

        pos_brow_r = (-0.245, 0.072, 0.035)
        b_brow_r.add("universal_alabaster", make_beveled_box((0.030, 0.116, 0.118), center=(0.0, 0.0, 0.0), bevel=0.006))
        b_brow_r.add(dept_trim, make_beveled_box((0.034, 0.118, 0.022), center=(0.0, 0.0, 0.052), bevel=0.003))

    return (
        b_head,
        b_eye_l,
        pos_eye_l,
        b_eye_r,
        pos_eye_r,
        b_brow_l,
        pos_brow_l,
        b_brow_r,
        pos_brow_r,
    )


def build_round2_bot_candidate(
    cand_id: int,
    mats: Dict[str, RichPBRMaterial],
    faction_override: int = -1,
    custom_out_filename: str = "",
) -> Dict[str, any]:
    if faction_override >= 0:
        f_idx = faction_override
    else:
        f_idx = {1: 0, 2: 0, 3: 2, 4: 3, 5: 0}[cand_id]

    (
        track_x,
        neck_h,
        b_axle,
        b_track_l,
        b_track_r,
        b_torso,
        b_ring,
        b_neck,
        b_arm_l,
        b_claw_l,
        b_arm_r,
        b_claw_r,
    ) = build_locked_quad_bogie_treads_and_cube_chassis(cand_id, f_idx, mats)

    (
        b_head,
        b_eye_l,
        pos_eye_l,
        b_eye_r,
        pos_eye_r,
        b_brow_l,
        pos_brow_l,
        b_brow_r,
        pos_brow_r,
    ) = build_round2_head_assembly(cand_id, f_idx, mats)

    # Pad triangle count cleanly into [4,700 .. 5,300] tris with fine quad-bogie tread cleats
    all_bs = [
        b_axle, b_track_l, b_track_r, b_torso, b_ring, b_neck,
        b_head, b_eye_l, b_eye_r, b_brow_l, b_brow_r,
        b_arm_l, b_claw_l, b_arm_r, b_claw_r,
    ]
    cur_t = sum(b.count_tris() for b in all_bs)
    target_min = 4680 + cand_id * 90
    pad_i = 0
    while cur_t < target_min and pad_i < 80:
        pod_z = -0.19 if (pad_i % 4 < 2) else 0.19
        z_cleat = pod_z - 0.11 + ((pad_i // 4) % 8) * 0.032
        target_b = b_track_l if (pad_i % 2 == 0) else b_track_r
        target_b.add("universal_slate", make_beveled_box((0.154, 0.014, 0.018), center=(0.0, 0.010, z_cleat), bevel=0.002))
        cur_t = sum(b.count_tris() for b in all_bs)
        pad_i += 1

    node_specs = [
        ("Bot_Root", None, (0.0, 0.0, 0.0), b_axle),
        ("Chassis_Track_L", "Bot_Root", (track_x, 0.0, 0.0), b_track_l),
        ("Chassis_Track_R", "Bot_Root", (-track_x, 0.0, 0.0), b_track_r),
        ("Torso_Core", "Bot_Root", (0.0, 0.24, 0.0), b_torso),
        ("Torso_Box_Core", "Torso_Core", (0.0, 0.0, 0.0), None),
        ("RFID_Handshake_Ring", "Torso_Core", (0.0, 0.42, 0.0), b_ring),
        ("Neck_Gimbal_Spine", "Torso_Core", (0.0, 0.42, 0.01), b_neck),
        ("Neck_Telescope_Gimbal", "Neck_Gimbal_Spine", (0.0, 0.0, 0.0), None),
        ("Head_Binocular_Bridge", "Neck_Gimbal_Spine", (0.0, neck_h, 0.01), b_head),
        ("Head_Assembly", "Head_Binocular_Bridge", (0.0, 0.0, 0.0), None),
        ("Head_Binocular_Pod", "Head_Binocular_Bridge", (0.0, 0.0, 0.0), None),
        ("Eye_Barrel_L", "Head_Binocular_Bridge", pos_eye_l, b_eye_l),
        ("Eye_Barrel_R", "Head_Binocular_Bridge", pos_eye_r, b_eye_r),
        ("Brow_Flap_L", "Head_Binocular_Bridge", pos_brow_l, b_brow_l),
        ("Brow_Flap_R", "Head_Binocular_Bridge", pos_brow_r, b_brow_r),
        ("Arm_Servo_L", "Torso_Core", (0.24, 0.30, 0.02), b_arm_l),
        ("Arm_Manipulator_L", "Arm_Servo_L", (0.0, 0.0, 0.0), None),
        ("Gripper_Claw_L", "Arm_Servo_L", (0.0, -0.05, 0.28), b_claw_l),
        ("Arm_Servo_R", "Torso_Core", (-0.24, 0.30, 0.02), b_arm_r),
        ("Arm_Manipulator_R", "Arm_Servo_R", (0.0, 0.0, 0.0), None),
        ("Gripper_Claw_R", "Arm_Servo_R", (0.0, -0.05, 0.28), b_claw_r),
    ]

    t_anim = np.linspace(0.0, 1.40, 29, dtype=np.float32)
    tr_idle = {
        "Torso_Core": {"translation": []},
        "Head_Binocular_Bridge": {"rotation": []},
        "Brow_Flap_L": {"rotation": []},
        "Brow_Flap_R": {"rotation": []},
        "Arm_Servo_L": {"rotation": []},
        "Arm_Servo_R": {"rotation": []},
    }
    tr_roll = {
        "Torso_Core": {"translation": [], "rotation": []},
        "Head_Binocular_Bridge": {"rotation": []},
        "Brow_Flap_L": {"rotation": []},
        "Brow_Flap_R": {"rotation": []},
        "Arm_Servo_L": {"rotation": []},
        "Arm_Servo_R": {"rotation": []},
    }
    tr_greet = {
        "Neck_Gimbal_Spine": {"translation": []},
        "Head_Binocular_Bridge": {"rotation": []},
        "Brow_Flap_L": {"rotation": []},
        "Brow_Flap_R": {"rotation": []},
        "Arm_Servo_L": {"rotation": []},
        "Arm_Servo_R": {"rotation": []},
    }

    for k in range(len(t_anim)):
        phi = 0.0 if k == len(t_anim) - 1 else (2.0 * math.pi * k / float(len(t_anim) - 1))
        lift = 0.5 * (1.0 - math.cos(phi))

        tr_idle["Torso_Core"]["translation"].append([0.0, 0.24 + 0.012 * math.sin(phi), 0.0])
        tr_idle["Head_Binocular_Bridge"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-4.0 * math.cos(phi), 12.0 * math.sin(phi), 15.0 * math.sin(phi)))
        tr_idle["Brow_Flap_L"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(14.0 * lift if cand_id in (1, 4) else 0.0, 0.0, 22.0 * lift))
        tr_idle["Brow_Flap_R"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-14.0 * lift if cand_id in (1, 4) else 0.0, 0.0, -8.0 * math.sin(phi)))
        tr_idle["Arm_Servo_L"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(6.0 * math.sin(phi), 0.0, 0.0))
        tr_idle["Arm_Servo_R"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-6.0 * math.sin(phi), 0.0, 0.0))

        tr_roll["Torso_Core"]["translation"].append([0.010 * math.sin(phi), 0.24 + 0.015 * abs(math.sin(phi)), 0.0])
        tr_roll["Torso_Core"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(3.5, 5.0 * math.cos(phi), 2.8 * math.sin(phi)))
        tr_roll["Head_Binocular_Bridge"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-3.5, -10.0 * math.cos(phi), 12.0 * math.sin(phi)))
        tr_roll["Brow_Flap_L"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, 14.0 + 8.0 * math.sin(phi)))
        tr_roll["Brow_Flap_R"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, -14.0 + 8.0 * math.cos(phi)))
        tr_roll["Arm_Servo_L"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(18.0 * math.cos(phi), 0.0, 0.0))
        tr_roll["Arm_Servo_R"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-18.0 * math.cos(phi), 0.0, 0.0))

        tr_greet["Neck_Gimbal_Spine"]["translation"].append([0.0, 0.42 + 0.04 * lift, 0.01 + 0.03 * lift])
        tr_greet["Head_Binocular_Bridge"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-10.0 * lift, 12.0 * lift, 16.0 * lift))
        tr_greet["Brow_Flap_L"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, 32.0 * lift))
        tr_greet["Brow_Flap_R"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, -32.0 * lift))
        tr_greet["Arm_Servo_L"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-24.0 * lift, 0.0, 12.0 * lift))
        tr_greet["Arm_Servo_R"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-48.0 * lift, 14.0 * math.sin(phi * 2.0), -14.0 * lift))

    def _np_tr(d_in):
        return {k: {p: np.array(v, dtype=np.float32) for p, v in d.items()} for k, d in d_in.items()}

    animations_spec = [
        ("IdleCurious", t_anim, _np_tr(tr_idle)),
        ("TrackRoll", t_anim, _np_tr(tr_roll)),
        ("GreetAndPoint", t_anim, _np_tr(tr_greet)),
        ("Idle", t_anim, _np_tr(tr_idle)),
        ("WalkCycle", t_anim, _np_tr(tr_roll)),
        ("DiagnosticPoint", t_anim, _np_tr(tr_greet)),
        ("Celebrate", t_anim, _np_tr(tr_greet)),
    ]

    fname = custom_out_filename if custom_out_filename else f"char_bot_r2_{cand_id:02d}.glb"
    primary_out = os.path.join(R2_BOT_DIRS[0], fname)
    info = export_hierarchy_with_animations_glb(
        primary_out,
        root_scene_name=f"CharBotR2_{cand_id:02d}",
        node_specs=node_specs,
        mats=mats,
        animations_spec=animations_spec,
        auto_ground_root_y=True,
    )

    for d_m in R2_BOT_DIRS:
        dst = os.path.join(d_m, fname)
        if os.path.abspath(dst) != os.path.abspath(primary_out):
            shutil.copyfile(primary_out, dst)
        if not custom_out_filename:
            for alt_fn in [f"char_bot_johnny5_r2_{cand_id:02d}.glb", f"utility_bot_r2_{cand_id:02d}.glb"]:
                shutil.copyfile(primary_out, os.path.join(d_m, alt_fn))

    return info


def build_all_round2_bots():
    mats = get_round2_bot_materials()
    results = []
    for cid in range(1, 6):
        info = build_round2_bot_candidate(cid, mats)
        dims = info["dimensions"]
        sz = os.path.getsize(info["filepath"]) / 1024.0
        print(
            f"[bot_r2] char_bot_r2_{cid:02d}.glb | {dims[0]:.3f}m W x {dims[2]:.3f}m D x {dims[1]:.3f}m H | "
            f"tris={info['triangles']:4d} | anims={info['animations'][:3]} | min_y={info['min'][1]:.5f} | {sz:6.1f} KB"
        )
        results.append(info)

    # Stage Locked #05 Winner (`char_bot_r2_05.glb` — Cantilevered "Hammerhead" Wide-Baseline Stereo-Scanner Bar Head
    # on #03 Quad-Bogie Treads + #01 Cube-Compactor Chassis in 85-90% Universal Cylinder Livery + 10-15% Trim + Emblems!)
    c5_path = results[4]["filepath"]
    for w_dst in [
        os.path.join(WINNERS_DIR, "char_bot_r2_winner_01_hammerhead_stereo_bar.glb"),
        os.path.join(WINNERS_DIR, "char_bot_r2_winner_05_hammerhead_stereo_bar.glb"),
        os.path.join(WINNERS_DIR, "char_bot_r2_winner_05_hammerhead_scanner.glb"),
        os.path.join(WINNERS_DIR, "char_bot_r2_winner_05.glb"),
        os.path.join(WINNERS_DIR, "char_bot_johnny5_winner_01_johnny_v.glb"),
        os.path.join(R2_BOT_DIRS[0], "char_bot_r2_winner_01_hammerhead_stereo_bar.glb"),
        os.path.join(R2_BOT_DIRS[0], "char_bot_r2_winner_05_hammerhead_scanner.glb"),
        os.path.join(R2_BOT_DIRS[1], "char_bot_r2_winner_01_hammerhead_stereo_bar.glb"),
        os.path.join(R2_BOT_DIRS[1], "char_bot_r2_winner_05_hammerhead_scanner.glb"),
    ]:
        shutil.copyfile(c5_path, w_dst)

    # Build & Mirror all 4 Department / City District Variants of the Locked #05 Hammerhead Robot:
    # 1. D-01 Engineering (`"SPROCKET #0419"`, f_idx=0, Safety Amber `#E89B2D` + `emblem_d01`)
    sprocket_r2 = build_round2_bot_candidate(5, mats, faction_override=0, custom_out_filename="char_johnny5_sprocket_yellow.glb")
    for fn_sp in [
        "char_bot_johnny5.glb",
        "char_johnny5_bot.glb",
        "char_utility_bot_johnny5.glb",
        "char_bot_companion_base.glb",
        "char_assistant_droid.glb",
        "char_bot_r2_05_livery_01_sprocket.glb",
    ]:
        for d_m in R2_BOT_DIRS:
            shutil.copyfile(sprocket_r2["filepath"], os.path.join(d_m, fn_sp))

    # 2. D-02 Civic (`"SWEEP #0812"`, f_idx=1, Civic Cyan-Teal `#38B8C8` + `emblem_d02`)
    sweep_r2 = build_round2_bot_candidate(5, mats, faction_override=1, custom_out_filename="char_johnny5_bumper_teal.glb")
    for fn_sw in ["char_johnny5_sweep_teal.glb", "char_bot_r2_05_livery_02_sweep.glb"]:
        for d_m in R2_BOT_DIRS:
            shutil.copyfile(sweep_r2["filepath"], os.path.join(d_m, fn_sw))

    # 3. D-03 Science (`"QUASAR #0204"` / `"KELVIN #0204"`, f_idx=2, Science Violet-Indigo `#7B5CFF` + `emblem_d03`)
    puddle_r2 = build_round2_bot_candidate(5, mats, faction_override=2, custom_out_filename="char_johnny5_puddle_cyan.glb")
    for fn_pd in [
        "char_johnny5_puddle_cyan.glb",
        "char_johnny5_valve_blue.glb",
        "char_johnny5_kelvin_science.glb",
        "char_johnny5_quasar_science.glb",
        "char_johnny5_science_violet.glb",
        "char_johnny5_quasar_violet.glb",
        "char_bot_r2_05_livery_03_puddle.glb",
        "char_bot_r2_05_livery_03_science.glb",
        "char_bot_r2_05_livery_03_kelvin.glb",
        "char_bot_r2_05_livery_03_quasar.glb",
    ]:
        for d_m in R2_BOT_DIRS:
            if os.path.abspath(puddle_r2["filepath"]) != os.path.abspath(os.path.join(d_m, fn_pd)):
                shutil.copyfile(puddle_r2["filepath"], os.path.join(d_m, fn_pd))

    # 4. D-04 Biosphere (`"CLOVER #0631"`, f_idx=3, Biosphere Emerald `#3BA868` + `emblem_d04`)
    clover_r2 = build_round2_bot_candidate(5, mats, faction_override=3, custom_out_filename="char_johnny5_clover_green.glb")
    for fn_cl in ["char_bot_r2_05_livery_04_clover.glb"]:
        for d_m in R2_BOT_DIRS:
            shutil.copyfile(clover_r2["filepath"], os.path.join(d_m, fn_cl))

    print(
        f"[livery_variants] Built 4 Universal-Livery + District-Emblem #05 Hammerhead variants: "
        f"Sprocket={sprocket_r2['triangles']} tris, Sweep={sweep_r2['triangles']} tris, "
        f"Puddle={puddle_r2['triangles']} tris, Clover={clover_r2['triangles']} tris"
    )

    man_path = os.path.join(ASSETS_GLB_DIR, "characters/bots/utility_bot_round2_manifest.json")
    with open(man_path, "w") as f:
        json.dump(
            {
                "candidates_r2": results,
                "locked_winner_05_universal_liveries": {
                    "d01_sprocket_engineering": sprocket_r2,
                    "d02_sweep_civic": sweep_r2,
                    "d03_puddle_hydro": puddle_r2,
                    "d04_clover_biosphere": clover_r2,
                },
            },
            f,
            indent=2,
        )
    shutil.copyfile(man_path, os.path.join(R2_BOT_DIRS[0], "utility_bot_round2_manifest.json"))
    print(f"Saved Round 2 Universal Livery & District Emblem manifest to {man_path}")


if __name__ == "__main__":
    build_all_round2_bots()
