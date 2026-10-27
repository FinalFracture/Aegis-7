#!/usr/bin/env python3
"""
Builds all 5 High-Detail Articulated Aegis-7 Orbital Crew Character .glb Models
(`char_crew_r1_01.glb` .. `char_crew_r1_05.glb`) with:
  1. Exposed, Portrait-Grade 3D Sculpted Faces, Eyes, Eyebrows, Noses, Lips, Ears,
     Distinct Hairstyles, Facial Hair / Scars / Cybernetic Implants, and Open/Retracted Headgear
     UV-mapped to Sloane's `char_headshot_faces_and_hair_atlas.png` + dedicated 3D facial sub-meshes
  2. Radically Distinct Upper-Torso, Collar & Shoulder Silhouettes per Character (`#01`..`#05`)
  3. 15-Node Articulated Humanoid Hierarchy & Embedded 1.20s (33-keyframe) glTF 2.0 `WalkCycle` Animation

Owner: Rook (3D Modeling Specialist)
Follows:
  - `/workspace/game-project/design/character_aegis7_crew_spec.md` (including Section 6 Headshot Addendum)
  - `/workspace/game-project/design/sloane_character_textures_and_lighting_spec.md` (including Section 4 Atlas)
"""
import os
import sys
import io
import math
import json
import shutil
from typing import Dict, List, Tuple, Optional
import numpy as np
from PIL import Image
import pygltflib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glb_builder import (
    PBRMaterialDef,
    SubMesh,
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
)

TEX_CHAR_DIR = "/workspace/game-project/assets/textures/character"
OUT_CHAR_ROOT = "/workspace/game-project/assets/glb/character"
OUT_CHAR_R1_DIR = "/workspace/game-project/assets/glb/character/char_crew_round1"
OUT_CHAR_01_DIR = "/workspace/game-project/assets/glb/character/char_01"
WINNERS_DIR = "/workspace/game-project/assets/glb/winners"

for d in [OUT_CHAR_ROOT, OUT_CHAR_R1_DIR, OUT_CHAR_01_DIR, WINNERS_DIR]:
    os.makedirs(d, exist_ok=True)


def tex_char(fname: str) -> str:
    p = os.path.join(TEX_CHAR_DIR, fname)
    if os.path.exists(p):
        return p
    return os.path.join("/workspace/game-project/assets/textures", fname)


def remap_uv_rect(
    geom: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    u_min: float = 0.0,
    u_max: float = 1.0,
    v_min: float = 0.0,
    v_max: float = 1.0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    p, n, u, idx = geom
    uv = u.copy()
    uv[:, 0] = u_min + np.clip(uv[:, 0], 0.0, 1.0) * (u_max - u_min)
    uv[:, 1] = v_min + np.clip(uv[:, 1], 0.0, 1.0) * (v_max - v_min)
    return p, n, uv, idx


def project_frontal_face_uv(
    geom: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    cand_id: int,
    x_half_width: float = 0.076,
    y_chin: float = 0.015,
    y_forehead: float = 0.165,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Maps the front face (z > 0.015) of the sculpted 3D cranium onto the character's row in
    `char_headshot_faces_and_hair_atlas.png` (`u: 0.02..0.48`, `v: row_v0..row_v1`), while
    mapping the sides/back of the head onto the clean skin-tone region of that row so the
    painted eyes/mouth only appear on the front face!
    """
    p, n, u, idx = geom
    uv = np.zeros_like(u, dtype=np.float32)
    v_row0 = (cand_id - 1) * 0.20 + 0.008
    v_row1 = cand_id * 0.20 - 0.008

    px = p[:, 0]
    py = p[:, 1]
    pz = p[:, 2]

    # Normalized frontal coordinates in [0, 1]
    nx_u = np.clip((px / (2.0 * x_half_width)) + 0.5, 0.02, 0.98)
    ny_v = np.clip(1.0 - (py - y_chin) / max(y_forehead - y_chin, 1e-4), 0.02, 0.98)

    is_front = pz > 0.018
    # Front face maps across u in [0.03, 0.47], v in [v_row0, v_row1]
    uv[:, 0] = np.where(is_front, 0.03 + nx_u * 0.44, 0.03 + (nx_u * 0.06))
    uv[:, 1] = np.where(is_front, v_row0 + ny_v * (v_row1 - v_row0), v_row0 + 0.02 + ny_v * 0.04)
    return p, n, uv, idx


def get_character_materials() -> Dict[str, PBRMaterialDef]:
    return {
        # Suit & Armor Materials
        "armor_white": PBRMaterialDef(
            name="Mat_Suit_AerospaceWhiteArmor",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.15,
            roughness=0.32,
            texture_path=tex_char("char_suit_armor_albedo.png"),
        ),
        "armor_gunmetal": PBRMaterialDef(
            name="Mat_Suit_GunmetalTitaniumChassis",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.78,
            roughness=0.38,
            texture_path=tex_char("char_suit_armor_albedo.png"),
        ),
        "steel_machined": PBRMaterialDef(
            name="Mat_Suit_BrushedSteelActuators",
            base_color=hex_rgba("#88929E"),
            metallic=0.88,
            roughness=0.24,
            texture_path=tex_char("facade_brushed_steel_gantry.png"),
        ),
        "undersuit_navy": PBRMaterialDef(
            name="Mat_Undersuit_OrbitalNavyRipstop",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.06,
            roughness=0.74,
            texture_path=tex_char("char_undersuit_ribbed_fabric.png"),
        ),
        "joint_bellows": PBRMaterialDef(
            name="Mat_Undersuit_CharcoalFlexBellows",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.12,
            roughness=0.66,
            texture_path=tex_char("char_undersuit_ribbed_fabric.png"),
        ),
        "accent_orange": PBRMaterialDef(
            name="Mat_Suit_SignalOrangeHardware",
            base_color=hex_rgba("#D95B26"),
            metallic=0.25,
            roughness=0.36,
            texture_path=tex_char("accent_safety_orange.png"),
        ),
        "chest_telemetry": PBRMaterialDef(
            name="Mat_OLED_ChestTelemetryAndLEDs",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.15,
            roughness=0.18,
            emissive=(0.45, 0.88, 0.95),
            texture_path=tex_char("char_chest_telemetry_emissive.png"),
        ),
        "visor_glass": PBRMaterialDef(
            name="Mat_Glass_HelmetVisor_Translucent",
            base_color=(0.65, 0.88, 1.0, 0.34),
            metallic=0.22,
            roughness=0.06,
            emissive=(0.04, 0.22, 0.32),
            texture_path=tex_char("char_visor_hud_translucent.png"),
            double_sided=True,
            alpha_mode="BLEND",
        ),
        # Sloane's 5-Character Headshot Portrait Atlas Material
        "portrait_atlas": PBRMaterialDef(
            name="Mat_Character_HeadshotPortraitAtlas",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.04,
            roughness=0.48,
            texture_path=tex_char("char_headshot_faces_and_hair_atlas.png"),
        ),
        # Dedicated High-Contrast 3D Facial Feature, Skin, Hair & Role Materials
        "skin_01_bronze": PBRMaterialDef(name="Mat_Skin01_WarmBronze", base_color=hex_rgba("#C2845C"), metallic=0.02, roughness=0.46),
        "skin_02_olive": PBRMaterialDef(name="Mat_Skin02_MediumOliveTan", base_color=hex_rgba("#CE9672"), metallic=0.02, roughness=0.46),
        "skin_03_umber": PBRMaterialDef(name="Mat_Skin03_DeepRichUmber", base_color=hex_rgba("#683E29"), metallic=0.03, roughness=0.44),
        "skin_04_ivory": PBRMaterialDef(name="Mat_Skin04_WarmPorcelainIvory", base_color=hex_rgba("#ECC4AC"), metallic=0.02, roughness=0.45),
        "skin_05_tan": PBRMaterialDef(name="Mat_Skin05_CoolGoldenTan", base_color=hex_rgba("#B6805C"), metallic=0.02, roughness=0.46),
        "hair_01_espresso": PBRMaterialDef(name="Mat_Hair01_DarkEspresso", base_color=hex_rgba("#241711"), metallic=0.06, roughness=0.62),
        "hair_02_charcoal": PBRMaterialDef(name="Mat_Hair02_CommanderCharcoal", base_color=hex_rgba("#282C34"), metallic=0.08, roughness=0.58),
        "hair_02_silver": PBRMaterialDef(name="Mat_Hair02_SilverTempleStreak", base_color=hex_rgba("#C4CED8"), metallic=0.18, roughness=0.42),
        "hair_03_braids": PBRMaterialDef(name="Mat_Hair03_TexturedDreadlocks", base_color=hex_rgba("#181210"), metallic=0.05, roughness=0.68),
        "hair_04_platinum": PBRMaterialDef(name="Mat_Hair04_PlatinumSilverBob", base_color=hex_rgba("#E2E8F0"), metallic=0.15, roughness=0.38),
        "hair_05_mohawk": PBRMaterialDef(name="Mat_Hair05_JetBlackMohawk", base_color=hex_rgba("#181B22"), metallic=0.08, roughness=0.56),
        "eye_sclera": PBRMaterialDef(name="Mat_Eye_ScleraWhite", base_color=hex_rgba("#F4F6F8"), metallic=0.02, roughness=0.14),
        "eye_pupil": PBRMaterialDef(name="Mat_Eye_PupilDark", base_color=hex_rgba("#0B0E14"), metallic=0.10, roughness=0.08),
        "iris_01_hazel": PBRMaterialDef(name="Mat_Iris01_WarmHazelBrown", base_color=hex_rgba("#8E6836"), metallic=0.08, roughness=0.16),
        "iris_02_cyan": PBRMaterialDef(name="Mat_Iris02_IceSteelCyan", base_color=hex_rgba("#38B6E8"), metallic=0.12, roughness=0.14, emissive=(0.05, 0.28, 0.42)),
        "iris_03_amber": PBRMaterialDef(name="Mat_Iris03_GoldAmber", base_color=hex_rgba("#C88228"), metallic=0.08, roughness=0.16),
        "iris_04_emerald": PBRMaterialDef(name="Mat_Iris04_VividEmerald", base_color=hex_rgba("#2ECC71"), metallic=0.10, roughness=0.14, emissive=(0.04, 0.32, 0.16)),
        "iris_05_amber": PBRMaterialDef(name="Mat_Iris05_TacticalGold", base_color=hex_rgba("#E09424"), metallic=0.10, roughness=0.14, emissive=(0.25, 0.14, 0.0)),
        "lip_natural": PBRMaterialDef(name="Mat_Lip_SculptedNatural", base_color=hex_rgba("#9E5E52"), metallic=0.02, roughness=0.42),
        "lip_03_umber": PBRMaterialDef(name="Mat_Lip03_DeepUmber", base_color=hex_rgba("#4E2C20"), metallic=0.02, roughness=0.42),
        "lip_04_plum": PBRMaterialDef(name="Mat_Lip04_PlumRose", base_color=hex_rgba("#B85866"), metallic=0.04, roughness=0.36),
        "role_cobalt_blue": PBRMaterialDef(name="Mat_Role01_CobaltFlightBlue", base_color=hex_rgba("#1E5AA8"), metallic=0.35, roughness=0.32),
        "role_caution_yellow": PBRMaterialDef(name="Mat_Role03_CaterpillarHazardYellow", base_color=hex_rgba("#FFB703"), metallic=0.32, roughness=0.34),
        "role_bio_emerald": PBRMaterialDef(name="Mat_Role04_BotanicalBioEmerald", base_color=hex_rgba("#2D8A62"), metallic=0.18, roughness=0.34),
        # Emissives
        "led_cyan": PBRMaterialDef(
            name="Mat_Emissive_CyanHUD",
            base_color=hex_rgba("#00E5FF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.0, 0.92, 1.0),
            texture_path=tex_char("led_cyan_strip.png"),
        ),
        "led_amber": PBRMaterialDef(
            name="Mat_Emissive_AmberBeacon",
            base_color=hex_rgba("#FF9500"),
            metallic=0.0,
            roughness=0.15,
            emissive=(1.0, 0.62, 0.0),
            texture_path=tex_char("led_amber_strip.png"),
        ),
        "led_uv": PBRMaterialDef(
            name="Mat_Emissive_UVVioletBio",
            base_color=hex_rgba("#9D4EDD"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.65, 0.32, 1.0),
            texture_path=tex_char("led_uv_violet.png"),
        ),
        "led_emerald": PBRMaterialDef(
            name="Mat_Emissive_EmeraldBioLED",
            base_color=hex_rgba("#00E676"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.0, 0.92, 0.48),
        ),
        "led_flood_white": PBRMaterialDef(
            name="Mat_Emissive_WorkFloodlampWhite",
            base_color=hex_rgba("#FFF5CC"),
            metallic=0.0,
            roughness=0.12,
            emissive=(1.0, 0.96, 0.80),
        ),
    }


class NodePartBuilder:
    def __init__(self, mats: Dict[str, PBRMaterialDef], cand_id: int = 1):
        self.mats = mats
        self.cand_id = cand_id
        self.buckets: Dict[str, List[Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]] = {
            k: [] for k in mats.keys()
        }

    def add(
        self,
        mat_key: str,
        geom: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
        atlas_subcol: Optional[str] = None,
    ):
        v0 = (self.cand_id - 1) * 0.20 + 0.008
        v1 = self.cand_id * 0.20 - 0.008
        if mat_key == "armor_white":
            geom = remap_uv_rect(geom, 0.02, 0.98, 0.02, 0.62)
        elif mat_key == "armor_gunmetal":
            geom = remap_uv_rect(geom, 0.02, 0.98, 0.66, 0.98)
        elif mat_key == "undersuit_navy":
            geom = remap_uv_rect(geom, 0.02, 0.48, 0.02, 0.98)
        elif mat_key == "joint_bellows":
            geom = remap_uv_rect(geom, 0.52, 0.98, 0.02, 0.98)
        elif mat_key == "chest_telemetry":
            geom = remap_uv_rect(geom, 0.04, 0.96, 0.04, 0.62)
        elif mat_key == "portrait_atlas" and atlas_subcol is not None:
            if atlas_subcol == "hair":
                geom = remap_uv_rect(geom, 0.52, 0.73, v0, v1)
            elif atlas_subcol == "trim":
                geom = remap_uv_rect(geom, 0.77, 0.98, v0, v1)
        self.buckets[mat_key].append(geom)

    def count_tris(self) -> int:
        return sum(len(idx) for g_list in self.buckets.values() for _, _, _, idx in g_list)


def make_lathe_limb(
    profile_ry: List[Tuple[float, float]],
    center: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    segments: int = 12,
    scale_xz: Tuple[float, float] = (1.0, 1.0),
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    geom = make_lathe_dome(profile_ry, center=(0.0, 0.0, 0.0), segments=segments, subdivide_profile=1)
    return transform_geom(geom, translate=center, scale=(scale_xz[0], 1.0, scale_xz[1]))


def make_joint_ball(
    radius: float,
    center: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    segments: int = 10,
    scale: Tuple[float, float, float] = (1.0, 1.0, 1.0),
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    prof = [
        (0.0, -radius),
        (radius * 0.72, -radius * 0.70),
        (radius, 0.0),
        (radius * 0.72, radius * 0.70),
        (0.0, radius),
    ]
    g = make_lathe_dome(prof, center=(0.0, 0.0, 0.0), segments=segments, subdivide_profile=1)
    return transform_geom(g, translate=center, scale=scale)


# ==============================================================================
# ANATOMICAL BODY, COLLAR & DISTINCT UPPER-TORSO SILHOUETTE BUILDERS
# ==============================================================================
def build_hips_node(cand_id: int, mats: Dict[str, PBRMaterialDef]) -> NodePartBuilder:
    b = NodePartBuilder(mats, cand_id=cand_id)
    pelvis_prof = [(0.0, -0.10), (0.11, -0.08), (0.155, -0.02), (0.165, 0.05), (0.145, 0.11), (0.0, 0.12)]
    b.add("undersuit_navy", make_lathe_limb(pelvis_prof, center=(0.0, 0.0, 0.0), segments=10, scale_xz=(1.12, 0.78)))
    b.add("armor_gunmetal", make_chamfered_oct_prism(0.36, 0.25, 0.085, center=(0.0, 0.055, 0.0), chamfer=0.06))
    belt_mat = "role_caution_yellow" if cand_id == 3 else ("role_bio_emerald" if cand_id == 4 else "armor_white")
    b.add(belt_mat, make_chamfered_oct_prism(0.34, 0.24, 0.07, center=(0.0, -0.015, 0.0), chamfer=0.055, top_scale=1.08))
    b.add("accent_orange", make_beveled_box((0.085, 0.065, 0.035), center=(0.0, 0.055, 0.125), bevel=0.008))
    b.add("led_amber", make_beveled_box((0.055, 0.022, 0.04), center=(0.0, 0.055, 0.13), bevel=0.004))
    for sx in [-1.0, 1.0]:
        b.add("armor_gunmetal", make_beveled_box((0.055, 0.095, 0.085), center=(sx * 0.185, 0.04, 0.01), bevel=0.01))
        b.add("steel_machined", make_closed_torus_ring(0.028, 0.006, center=(sx * 0.19, -0.01, 0.05), rot_xyz_deg=(0.0, 0.0, 90.0), n_major=8, n_minor=4))
    return b


def build_spine_node(cand_id: int, mats: Dict[str, PBRMaterialDef]) -> NodePartBuilder:
    b = NodePartBuilder(mats, cand_id=cand_id)
    b.add("joint_bellows", make_joint_ball(0.125, center=(0.0, -0.02, 0.0), segments=8, scale=(1.18, 0.9, 0.82)))
    abd_prof = [(0.0, -0.04), (0.135, 0.0), (0.142, 0.08), (0.155, 0.17), (0.162, 0.23), (0.0, 0.25)]
    b.add("undersuit_navy", make_lathe_limb(abd_prof, center=(0.0, 0.0, 0.0), segments=10, scale_xz=(1.14, 0.78)))
    for r_y in [0.04, 0.10, 0.16]:
        b.add("joint_bellows", make_chamfered_oct_prism(0.31, 0.22, 0.032, center=(0.0, r_y, 0.0), chamfer=0.05))
        b.add("steel_machined", make_beveled_box((0.065, 0.042, 0.045), center=(0.0, r_y, -0.115), bevel=0.008))
    return b


def build_chest_node(cand_id: int, mats: Dict[str, PBRMaterialDef]) -> NodePartBuilder:
    """
    Chest pivot at Spine + (0.0, 0.22, 0.0) -> world Y = 1.34m.
    Builds radically distinct collar, shoulder-frame, and upper-chest silhouettes per candidate
    so even from neck/shoulders alone, all 5 headshots are 100% distinct!
    """
    b = NodePartBuilder(mats, cand_id=cand_id)
    chest_prof = [(0.0, -0.04), (0.155, 0.0), (0.185, 0.09), (0.195, 0.18), (0.155, 0.24), (0.0, 0.26)]
    b.add("undersuit_navy", make_lathe_limb(chest_prof, center=(0.0, 0.0, 0.0), segments=10, scale_xz=(1.18, 0.82)))

    # Recessed Chest OLED Telemetry Console
    b.add("armor_gunmetal", make_beveled_box((0.15, 0.11, 0.04), center=(0.0, 0.10, 0.148), bevel=0.008))
    b.add("chest_telemetry", make_beveled_box((0.125, 0.085, 0.044), center=(0.0, 0.10, 0.150), bevel=0.004))

    if cand_id == 1:
        # #01 Flight Officer: Clean Aerospace-White Cuirass + Circular Orbital Collar Ring + Cobalt-Blue & Signal-Orange Rank Epaulettes
        b.add("armor_white", make_chamfered_oct_prism(0.41, 0.27, 0.21, center=(0.0, 0.10, 0.01), chamfer=0.075, top_scale=1.08))
        for sx in [-0.095, 0.095]:
            b.add("armor_white", make_beveled_box((0.165, 0.15, 0.06), center=(sx, 0.12, 0.125), bevel=0.016))
        # Circular aerospace-white collar ring + cobalt-blue & signal-orange shoulder rank epaulettes
        b.add("armor_white", make_closed_torus_ring(0.122, 0.026, center=(0.0, 0.225, 0.0), rot_xyz_deg=(5.0, 0.0, 0.0), n_major=14, n_minor=6))
        b.add("led_cyan", make_closed_torus_ring(0.128, 0.008, center=(0.0, 0.232, 0.0), rot_xyz_deg=(5.0, 0.0, 0.0), n_major=14, n_minor=5))
        for sx in [-1.0, 1.0]:
            b.add("role_cobalt_blue", make_beveled_box((0.11, 0.032, 0.12), center=(sx * 0.155, 0.218, 0.01), bevel=0.008))
            b.add("accent_orange", make_beveled_box((0.035, 0.038, 0.095), center=(sx * 0.185, 0.220, 0.01), bevel=0.005))
            b.add("led_cyan", make_beveled_box((0.022, 0.016, 0.025), center=(sx * 0.085, 0.215, 0.115), bevel=0.003))
        # Compact dorsal flight O2 pack
        b.add("armor_white", make_chamfered_oct_prism(0.28, 0.12, 0.28, center=(0.0, 0.09, -0.175), chamfer=0.04))
        b.add("role_cobalt_blue", make_beveled_box((0.20, 0.08, 0.13), center=(0.0, 0.18, -0.18), bevel=0.012))

    elif cand_id == 2:
        # #02 Aegis-7 Commander (HERO 65/35 Split):
        # Left (+X) 65% Aerospace-White Breastplate + Diagonal Signal-Orange EVA Harness & High Command Gorget
        # Right (-X) 35% Gunmetal Biomonitor Matrix + Right-Shoulder Articulated Brushed-Steel Micro-Camera/Laser Boom beside Head!
        b.add("armor_white", make_chamfered_oct_prism(0.25, 0.27, 0.22, center=(0.075, 0.10, 0.01), chamfer=0.055, top_scale=1.08))
        b.add("armor_gunmetal", make_chamfered_oct_prism(0.18, 0.26, 0.22, center=(-0.11, 0.10, 0.01), chamfer=0.045, top_scale=1.06))
        b.add("armor_white", make_beveled_box((0.17, 0.16, 0.065), center=(0.095, 0.12, 0.125), bevel=0.018))
        b.add("armor_gunmetal", make_beveled_box((0.17, 0.16, 0.065), center=(-0.095, 0.12, 0.125), bevel=0.018))
        # Diagonal Signal-Orange EVA Quick-Release Harness Strap & O2 Latch
        b.add(
            "accent_orange",
            transform_geom(make_beveled_box((0.052, 0.29, 0.032), bevel=0.006), translate=(0.035, 0.12, 0.142), rot_xyz_deg=(0.0, 0.0, -32.0)),
        )
        b.add("accent_orange", make_beveled_box((0.055, 0.095, 0.048), center=(0.115, 0.16, 0.145), bevel=0.008))
        # Asymmetric High Command Gorget Collar (Left Signal-Orange & White, Right Gunmetal & Cyan)
        b.add("armor_white", make_chamfered_oct_prism(0.15, 0.23, 0.065, center=(0.06, 0.235, -0.01), chamfer=0.035))
        b.add("accent_orange", make_beveled_box((0.095, 0.062, 0.045), center=(0.105, 0.242, 0.085), bevel=0.008))
        b.add("armor_gunmetal", make_chamfered_oct_prism(0.15, 0.23, 0.065, center=(-0.06, 0.235, -0.01), chamfer=0.035))
        b.add("led_cyan", make_beveled_box((0.075, 0.018, 0.035), center=(-0.095, 0.245, 0.095), bevel=0.004))
        # Right-Shoulder (-X) Articulated Brushed-Steel Micro-Camera & Laser Targeter Boom sitting right beside the Commander's Head!
        boom_pts = sample_filleted_polyline([(-0.165, 0.21, -0.06), (-0.185, 0.34, -0.04), (-0.165, 0.38, 0.04)], 0.03, 3)
        b.add("steel_machined", make_swept_tube(boom_pts, radius=0.015, radial_segments=8))
        b.add("armor_gunmetal", make_beveled_box((0.062, 0.052, 0.088), center=(-0.165, 0.385, 0.055), bevel=0.010))
        b.add("led_cyan", make_cylinder(0.018, 0.018, 0.024, center=(-0.165, 0.385, 0.098), segments=10, axis="z"))
        b.add("led_amber", make_cylinder(0.009, 0.009, 0.024, center=(-0.142, 0.398, 0.096), segments=8, axis="z"))
        # Dual-Zone Split Dorsal Life-Support Pack (Left O2 Housing + Right Translucent Cryo-Coolant Column)
        b.add("armor_white", make_chamfered_oct_prism(0.20, 0.13, 0.30, center=(0.055, 0.09, -0.18), chamfer=0.035))
        b.add("led_cyan", make_cylinder(0.028, 0.028, 0.26, center=(-0.105, 0.09, -0.18), segments=8))
        for c_y in [0.01, 0.09, 0.17]:
            b.add("led_uv", make_closed_torus_ring(0.042, 0.008, center=(-0.105, c_y, -0.18), n_major=8, n_minor=4))
        b.add("visor_glass", make_cylinder(0.055, 0.055, 0.28, center=(-0.105, 0.09, -0.18), segments=10))

    elif cand_id == 3:
        # #03 Heavy EVA Engineer: Massive Wide Gunmetal & Caterpillar-Yellow Hydraulic Exo-Yoke Collar + Twin Vertical Piston Struts
        b.add("armor_gunmetal", make_chamfered_oct_prism(0.45, 0.29, 0.23, center=(0.0, 0.10, 0.01), chamfer=0.08, top_scale=1.10))
        for sx in [-1.0, 1.0]:
            b.add("role_caution_yellow", make_beveled_box((0.16, 0.15, 0.07), center=(sx * 0.105, 0.12, 0.13), bevel=0.015))
            b.add("armor_gunmetal", make_beveled_box((0.14, 0.035, 0.078), center=(sx * 0.105, 0.12, 0.132), bevel=0.005))
            # Heavy Hydraulic Exo-Yoke Shoulder Guards & Twin Vertical Piston Struts flanking the neck/head
            b.add("role_caution_yellow", make_chamfered_oct_prism(0.14, 0.24, 0.085, center=(sx * 0.175, 0.245, 0.0), chamfer=0.03))
            b.add("steel_machined", make_cylinder(0.022, 0.022, 0.19, center=(sx * 0.155, 0.26, -0.055), segments=8))
            b.add("accent_orange", make_cylinder(0.028, 0.028, 0.06, center=(sx * 0.155, 0.22, -0.055), segments=8))
        b.add("armor_gunmetal", make_closed_torus_ring(0.132, 0.032, center=(0.0, 0.22, 0.0), n_major=12, n_minor=6))
        # Twin dorsal MMU nitrogen thruster cylinders
        for sx in [-0.10, 0.10]:
            b.add("armor_gunmetal", make_cylinder(0.068, 0.068, 0.32, center=(sx, 0.09, -0.19), segments=10))
            b.add("role_caution_yellow", make_closed_torus_ring(0.072, 0.012, center=(sx, 0.18, -0.19), n_major=8, n_minor=4))

    elif cand_id == 4:
        # #04 Bio-Science & Medical Specialist: High Contoured White & Botanical-Emerald Petal Collar + Twin Floating Cryo-Sample Pods
        b.add("armor_white", make_chamfered_oct_prism(0.38, 0.25, 0.21, center=(0.0, 0.10, 0.01), chamfer=0.07, top_scale=1.05))
        for sx in [-1.0, 1.0]:
            b.add("role_bio_emerald", make_beveled_box((0.15, 0.14, 0.055), center=(sx * 0.09, 0.12, 0.122), bevel=0.016))
            # High angled Botanical-Emerald & White Medical Isolation Petal Collar framing the jaw/neck
            b.add(
                "role_bio_emerald",
                transform_geom(make_beveled_box((0.045, 0.115, 0.18), bevel=0.010), translate=(sx * 0.118, 0.255, -0.01), rot_xyz_deg=(0.0, 0.0, -sx * 22.0)),
            )
            b.add(
                "armor_white",
                transform_geom(make_beveled_box((0.035, 0.105, 0.16), bevel=0.008), translate=(sx * 0.126, 0.252, -0.01), rot_xyz_deg=(0.0, 0.0, -sx * 22.0)),
            )
            b.add("led_uv", make_cylinder(0.012, 0.012, 0.04, center=(sx * 0.108, 0.265, 0.075), segments=8, axis="z"))
            # Cantilevered Translucent Emerald & UV-Violet Bio-Sample Shoulder Pods visible in Headshot!
            b.add("steel_machined", make_cylinder(0.014, 0.014, 0.11, center=(sx * 0.175, 0.24, -0.06), segments=8))
            b.add("led_emerald" if sx > 0 else "led_uv", make_cylinder(0.026, 0.026, 0.13, center=(sx * 0.185, 0.31, -0.06), segments=10))
            b.add("visor_glass", make_cylinder(0.042, 0.042, 0.15, center=(sx * 0.185, 0.31, -0.06), segments=10))
        b.add("armor_white", make_chamfered_oct_prism(0.26, 0.11, 0.26, center=(0.0, 0.09, -0.16), chamfer=0.035))

    else:
        # #05 Tactical Recon: Angular 45°-Faceted Stealth Gunmetal V-Wing Collar + Sharp Raised Shoulder Fins + Tall Dorsal Comms Fin
        b.add("armor_gunmetal", make_chamfered_oct_prism(0.40, 0.26, 0.22, center=(0.0, 0.10, 0.01), chamfer=0.08, top_scale=1.08))
        for sx in [-1.0, 1.0]:
            b.add("armor_gunmetal", make_beveled_box((0.16, 0.15, 0.065), center=(sx * 0.092, 0.12, 0.125), bevel=0.012))
            b.add("led_amber", make_beveled_box((0.12, 0.018, 0.068), center=(sx * 0.092, 0.15, 0.126), bevel=0.003))
            # Sharp Raised V-Wing Stealth Shoulder Fins framing the head in portrait view
            b.add(
                "armor_gunmetal",
                transform_geom(make_beveled_box((0.038, 0.16, 0.19), bevel=0.008), translate=(sx * 0.155, 0.275, -0.015), rot_xyz_deg=(8.0, 0.0, -sx * 26.0)),
            )
            b.add(
                "accent_orange",
                transform_geom(make_beveled_box((0.042, 0.14, 0.032), bevel=0.005), translate=(sx * 0.158, 0.280, 0.065), rot_xyz_deg=(8.0, 0.0, -sx * 26.0)),
            )
        # Tall Dorsal Stealth Comms Fin Antenna rising behind the head/left shoulder
        b.add("armor_gunmetal", make_chamfered_oct_prism(0.28, 0.12, 0.29, center=(0.0, 0.09, -0.18), chamfer=0.04))
        b.add("armor_gunmetal", make_beveled_box((0.026, 0.34, 0.11), center=(-0.095, 0.32, -0.15), bevel=0.005))
        b.add("led_amber", make_beveled_box((0.030, 0.28, 0.018), center=(-0.095, 0.33, -0.095), bevel=0.003))

    return b


# ==============================================================================
# PORTRAIT-GRADE 3D SCULPTED HEAD, FACE, EYES, HAIR & OPEN HEADGEAR BUILDER
# ==============================================================================
def build_head_node(cand_id: int, mats: Dict[str, PBRMaterialDef]) -> NodePartBuilder:
    """
    Head pivot at Chest + (0.0, 0.24, 0.0) -> world Y = 1.58m.
    Crown of head / headgear reaches local Y = +0.220m -> world Y = 1.800m.
    Zero full-face opaque/blurry bubble visor! Every face is directly exposed with:
      - Multi-plane 3D cranium, zygomatic cheekbones, brow ridge & character-specific jawline
        UV-mapped to `char_headshot_faces_and_hair_atlas.png` + skin material sculpting
      - Prominent 3D nose bridge, dorsum, tip, and nostrils (+Z)
      - 3D eyes: white sclera spheres, distinct colored iris discs, dark pupils, white corneal
        catchlights, and sculpted upper/lower eyelids
      - Sculpted 3D eyebrows, upper & lower lips, and 3D ears with helix/tragus detail
      - Character-specific 3D hair locks/braids/bob/mohawk, facial hair, scars & open headgear!
    """
    b = NodePartBuilder(mats, cand_id=cand_id)

    skin_key = {
        1: "skin_01_bronze",
        2: "skin_02_olive",
        3: "skin_03_umber",
        4: "skin_04_ivory",
        5: "skin_05_tan",
    }[cand_id]
    hair_key = {
        1: "hair_01_espresso",
        2: "hair_02_charcoal",
        3: "hair_03_braids",
        4: "hair_04_platinum",
        5: "hair_05_mohawk",
    }[cand_id]
    iris_key = {
        1: "iris_01_hazel",
        2: "iris_02_cyan",
        3: "iris_03_amber",
        4: "iris_04_emerald",
        5: "iris_05_amber",
    }[cand_id]
    lip_key = "lip_03_umber" if cand_id == 3 else ("lip_04_plum" if cand_id == 4 else "lip_natural")

    # Distinct cranial width & jaw proportions per candidate
    jaw_w_scale = {1: 0.96, 2: 1.00, 3: 1.08, 4: 0.88, 5: 0.91}[cand_id]
    depth_scale = {1: 1.04, 2: 1.06, 3: 1.08, 4: 0.98, 5: 1.03}[cand_id]

    # 1. Sculpted Anatomical Neck Column & Sternocleidomastoid Contours
    b.add("joint_bellows", make_cylinder(0.056, 0.064, 0.045, center=(0.0, -0.005, -0.006), segments=10))
    b.add(skin_key, make_cylinder(0.052 * jaw_w_scale, 0.056 * jaw_w_scale, 0.055, center=(0.0, 0.022, 0.002), segments=12))

    # 2. Sculpted Multi-Plane 3D Cranium & Face Base (UV-mapped to Sloane's Portrait Atlas + 3D Facial Planes)
    head_prof = [
        (0.0, 0.016),
        (0.046 * jaw_w_scale, 0.022),  # Chin base
        (0.068 * jaw_w_scale, 0.048),  # Jawline angle (gonion)
        (0.075 * jaw_w_scale, 0.078),  # Mid-cheek / maxilla
        (0.078 * jaw_w_scale, 0.104),  # Zygomatic arch / eye level
        (0.076, 0.136),                # Forehead / frontal bone
        (0.062, 0.164),                # Parietal dome
        (0.032, 0.178),
        (0.0, 0.182),                  # Cranial vertex
    ]
    cranium_geom = make_lathe_limb(head_prof, center=(0.0, 0.0, 0.006), segments=16, scale_xz=(0.94, depth_scale))
    b.add("portrait_atlas", project_frontal_face_uv(cranium_geom, cand_id=cand_id, x_half_width=0.074 * jaw_w_scale, y_chin=0.018, y_forehead=0.168))

    # 3. Sculpted 3D Zygomatic Cheekbones, Chin Mentum, Jawline Planes & Brow Ridge
    for sx in [-1.0, 1.0]:
        # Zygomatic cheekbone prominence
        b.add(
            skin_key,
            transform_geom(
                make_beveled_box((0.032 * jaw_w_scale, 0.028, 0.026), bevel=0.008),
                translate=(sx * 0.044 * jaw_w_scale, 0.082, 0.064),
                rot_xyz_deg=(6.0, sx * 22.0, 0.0),
            ),
        )
        # Mandibular jawline ridge
        b.add(
            skin_key,
            transform_geom(
                make_beveled_box((0.024, 0.022, 0.062), bevel=0.006),
                translate=(sx * 0.048 * jaw_w_scale, 0.044, 0.036),
                rot_xyz_deg=(18.0, sx * 26.0, 0.0),
            ),
        )
    # Sculpted Chin Pad (Mentum)
    b.add(skin_key, make_beveled_box((0.038 * jaw_w_scale, 0.024, 0.026), center=(0.0, 0.028, 0.072), bevel=0.007))
    # Supraorbital Brow Ridge
    b.add(skin_key, make_beveled_box((0.094 * jaw_w_scale, 0.018, 0.024), center=(0.0, 0.116, 0.074), bevel=0.006))

    # 4. Prominent 3D Sculpted Nose (Bridge, Dorsum, Rounded Tip & Nostrils projecting +Z)
    nose_w = 0.024 if cand_id == 3 else (0.017 if cand_id == 4 else 0.020)
    b.add(
        skin_key,
        transform_geom(
            make_beveled_box((nose_w, 0.042, 0.026), bevel=0.006),
            translate=(0.0, 0.088, 0.082),
            rot_xyz_deg=(-14.0, 0.0, 0.0),
        ),
    )
    # Nose tip ball & nostril wings (alae)
    b.add(skin_key, make_joint_ball(nose_w * 0.62, center=(0.0, 0.072, 0.095), segments=8))
    for sx in [-1.0, 1.0]:
        b.add(skin_key, make_beveled_box((nose_w * 0.55, 0.012, 0.016), center=(sx * nose_w * 0.52, 0.070, 0.086), bevel=0.004))

    # 5. High-Contrast 3D Eyes (White Sclera, Colored Iris, Dark Pupil, Catchlight & Eyelids)
    eye_x = 0.029 * jaw_w_scale
    eye_y = 0.099
    eye_z = 0.072
    brow_tilt = {1: 4.0, 2: 7.0, 3: 5.0, 4: -3.0, 5: 11.0}[cand_id]
    brow_thick = 0.0085 if cand_id in (2, 3) else 0.0065

    for sx in [-1.0, 1.0]:
        ex = sx * eye_x
        # White Sclera Eyeball
        b.add("eye_sclera", make_beveled_box((0.022, 0.013, 0.012), center=(ex, eye_y, eye_z), bevel=0.004))
        # Colored 3D Iris Disc
        b.add(iris_key, make_cylinder(0.0062, 0.0062, 0.006, center=(ex, eye_y, eye_z + 0.005), segments=10, axis="z"))
        # Dark Pupil Core
        b.add("eye_pupil", make_cylinder(0.0032, 0.0032, 0.006, center=(ex, eye_y, eye_z + 0.0065), segments=8, axis="z"))
        # Bright Studio Corneal Catchlight Specular Dot (upper-left of each iris)
        b.add("eye_sclera", make_beveled_box((0.0024, 0.0024, 0.003), center=(ex + 0.0022, eye_y + 0.0022, eye_z + 0.008), bevel=0.0))
        # Upper & Lower Sculpted Eyelid Folds
        b.add(skin_key, make_beveled_box((0.025, 0.0045, 0.014), center=(ex, eye_y + 0.0068, eye_z + 0.001), bevel=0.0015))
        b.add(skin_key, make_beveled_box((0.024, 0.0035, 0.012), center=(ex, eye_y - 0.0062, eye_z + 0.0005), bevel=0.001))
        # Sculpted 3D Eyebrow Arch
        b.add(
            hair_key,
            transform_geom(
                make_beveled_box((0.030, brow_thick, 0.012), bevel=0.002),
                translate=(ex, eye_y + 0.015, eye_z + 0.005),
                rot_xyz_deg=(0.0, sx * 12.0, -sx * brow_tilt),
            ),
        )

    # 6. Sculpted 3D Upper & Lower Lips + Mouth Line
    lip_w = 0.034 * jaw_w_scale
    b.add(lip_key, make_beveled_box((lip_w, 0.0065, 0.014), center=(0.0, 0.053, 0.080), bevel=0.0025))
    b.add(lip_key, make_beveled_box((lip_w * 0.92, 0.0072, 0.015), center=(0.0, 0.045, 0.079), bevel=0.0028))
    b.add("eye_pupil", make_beveled_box((lip_w * 0.96, 0.0018, 0.014), center=(0.0, 0.049, 0.081), bevel=0.0))

    # 7. Anatomically Positioned 3D Ears with Helix Rim & Tragus
    for sx in [-1.0, 1.0]:
        ear_x = sx * 0.075 * jaw_w_scale
        b.add(
            skin_key,
            transform_geom(
                make_beveled_box((0.014, 0.036, 0.022), bevel=0.005),
                translate=(ear_x, 0.090, 0.002),
                rot_xyz_deg=(-8.0, -sx * 14.0, 0.0),
            ),
        )

    # ==========================================================================
    # 8. CANDIDATE-SPECIFIC 3D HAIRSTYLES, FACIAL HAIR & OPEN HEADGEAR (`#01`..`#05`)
    # ==========================================================================
    if cand_id == 1:
        # #01 ("Lt. Marcus Vance-Lin" — Standard Flight Officer):
        # - Sculpted dark-espresso (`#241711`) parted crew-cut hair with volumetric swept top ridges & tapered sides
        # - Retracted flip-up white/cobalt-blue flight visor resting high above the forehead (open face!)
        # - Compact dual-ear flight comms pods
        hair_cap = [(0.0, 0.125), (0.076, 0.130), (0.079, 0.158), (0.066, 0.184), (0.0, 0.194)]
        b.add("hair_01_espresso", make_lathe_limb(hair_cap, center=(0.0, 0.0, -0.006), segments=14, scale_xz=(0.96, 1.06)))
        # Sculpted parted crew-cut top ridges
        for rx_off, rz_rot in [(-0.032, 12.0), (-0.008, 6.0), (0.018, -4.0), (0.042, -14.0)]:
            b.add(
                "hair_01_espresso",
                transform_geom(
                    make_beveled_box((0.024, 0.026, 0.095), bevel=0.006),
                    translate=(rx_off, 0.180, 0.022),
                    rot_xyz_deg=(-8.0, 0.0, rz_rot),
                ),
            )
        # Sideburns / tapered temple hair
        for sx in [-1.0, 1.0]:
            b.add("hair_01_espresso", make_beveled_box((0.014, 0.048, 0.055), center=(sx * 0.072, 0.118, -0.008), bevel=0.004))
            # Compact Cobalt-Blue & White Ear-Comms Pods
            b.add("role_cobalt_blue", make_cylinder(0.022, 0.022, 0.018, center=(sx * 0.082, 0.088, 0.002), segments=10, axis="x"))
            b.add("led_cyan", make_cylinder(0.010, 0.010, 0.022, center=(sx * 0.084, 0.088, 0.002), segments=8, axis="x"))

        # Retracted Flip-Up Aerospace-White & Cobalt-Blue Flight Visor Crown resting high above the forehead (Y = 0.152..0.218m)
        b.add(
            "armor_white",
            transform_geom(
                make_chamfered_oct_prism(0.182, 0.145, 0.042, chamfer=0.038),
                translate=(0.0, 0.172, 0.018),
                rot_xyz_deg=(-26.0, 0.0, 0.0),
            ),
        )
        b.add(
            "role_cobalt_blue",
            transform_geom(
                make_beveled_box((0.155, 0.022, 0.035), bevel=0.005),
                translate=(0.0, 0.194, 0.058),
                rot_xyz_deg=(-26.0, 0.0, 0.0),
            ),
        )
        b.add(
            "visor_glass",
            transform_geom(
                make_chamfered_oct_prism(0.168, 0.085, 0.038, chamfer=0.032),
                translate=(0.0, 0.162, 0.068),
                rot_xyz_deg=(-32.0, 0.0, 0.0),
            ),
        )

    elif cand_id == 2:
        # #02 ("Commander Kaelen Rostov" — HERO 65/35 Asymmetric Split Commander):
        # - Sculpted swept-back charcoal commander hair (`#282C34`) with 3D silver-grey temple streaks (`#C4CED8`)
        # - Sculpted 3D trimmed full beard, mustache & chin goatee
        # - Glowing Cyan (`#00E5FF`, `alphaMode: "BLEND"`) AR Targeting Monocle over the Left Eye (+X)
        # - Asymmetric Right-Side (-X) Gunmetal & Signal-Orange Open Tactical Ear-Cowl + Boom Mic
        hair_cap = [(0.0, 0.122), (0.078, 0.128), (0.082, 0.160), (0.068, 0.188), (0.0, 0.198)]
        b.add("hair_02_charcoal", make_lathe_limb(hair_cap, center=(0.0, 0.0, -0.010), segments=14, scale_xz=(0.98, 1.08)))
        # Dynamic swept-back charcoal crown locks
        for rx_off in [-0.045, -0.015, 0.015, 0.045]:
            b.add(
                "hair_02_charcoal",
                transform_geom(
                    make_beveled_box((0.026, 0.030, 0.115), bevel=0.007),
                    translate=(rx_off, 0.184, 0.015),
                    rot_xyz_deg=(14.0, 0.0, -rx_off * 180.0),
                ),
            )
        # Distinct 3D Silver-Grey Temple Streaks (`#C4CED8`) along both temples & sideburns
        for sx in [-1.0, 1.0]:
            b.add(
                "hair_02_silver",
                transform_geom(
                    make_beveled_box((0.018, 0.034, 0.082), bevel=0.005),
                    translate=(sx * 0.074, 0.132, 0.012),
                    rot_xyz_deg=(10.0, sx * 8.0, 0.0),
                ),
            )
            b.add("hair_02_silver", make_beveled_box((0.016, 0.042, 0.028), center=(sx * 0.072, 0.095, 0.022), bevel=0.004))

        # Sculpted 3D Trimmed Full Beard, Mustache & Chin Goatee (`#282C34` charcoal + silver chin streak)
        # Mustache wings above upper lip
        for sx in [-1.0, 1.0]:
            b.add(
                "hair_02_charcoal",
                transform_geom(
                    make_beveled_box((0.024, 0.010, 0.018), bevel=0.003),
                    translate=(sx * 0.011, 0.059, 0.080),
                    rot_xyz_deg=(0.0, 0.0, -sx * 14.0),
                ),
            )
            # Jawline beard strap from sideburns to chin
            b.add(
                "hair_02_charcoal",
                transform_geom(
                    make_beveled_box((0.022, 0.028, 0.068), bevel=0.006),
                    translate=(sx * 0.050, 0.042, 0.038),
                    rot_xyz_deg=(18.0, sx * 25.0, 0.0),
                ),
            )
        # Sculpted Chin Goatee & Soul-Patch
        b.add("hair_02_charcoal", make_beveled_box((0.046, 0.032, 0.032), center=(0.0, 0.026, 0.070), bevel=0.008))
        b.add("hair_02_silver", make_beveled_box((0.014, 0.028, 0.034), center=(0.0, 0.025, 0.071), bevel=0.004))

        # Left-Eye (+X) Glowing Cyan AR Tactical Monocle (`alphaMode: "BLEND"` lens + gold/steel brow bracket)
        b.add("steel_machined", make_beveled_box((0.045, 0.010, 0.055), center=(0.058, 0.118, 0.045), bevel=0.002))
        b.add("led_cyan", make_closed_torus_ring(0.021, 0.0032, center=(0.030, 0.099, 0.088), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=12, n_minor=5))
        b.add("visor_glass", make_cylinder(0.020, 0.020, 0.005, center=(0.030, 0.099, 0.088), segments=12, axis="z"))

        # Asymmetric Right-Side (-X) Gunmetal & Signal-Orange Open Tactical Ear-Cowl + Boom Mic
        b.add("armor_gunmetal", make_beveled_box((0.028, 0.095, 0.085), center=(-0.082, 0.092, -0.008), bevel=0.008))
        b.add("accent_orange", make_beveled_box((0.032, 0.045, 0.042), center=(-0.084, 0.092, 0.012), bevel=0.005))
        b.add("led_amber", make_cylinder(0.010, 0.010, 0.034, center=(-0.085, 0.122, 0.015), segments=8, axis="x"))
        mic_pts = sample_filleted_polyline([(-0.082, 0.072, 0.018), (-0.068, 0.048, 0.065), (-0.028, 0.046, 0.086)], 0.015, 3)
        b.add("steel_machined", make_swept_tube(mic_pts, radius=0.0045, radial_segments=6))
        b.add("led_cyan", make_joint_ball(0.006, center=(-0.026, 0.046, 0.086), segments=6))

    elif cand_id == 3:
        # #03 ("Chief Engineer Tarek Mensah" — Heavy Zero-G EVA & Shipyard Engineer):
        # - Deep rich umber skin (`#683E29`), broad powerful jaw with heavy chin goatee/stubble
        # - Sculpted textured dreadlock / braided hair crown bundled with `#FFB703` brass/amber cuffs
        # - Open Caterpillar-Yellow (`#FFB703`) & Signal-Orange Industrial Exo-Roll-Cage Frame + Twin Forehead LED Floodlamps
        b.add("hair_03_braids", make_beveled_box((0.048, 0.028, 0.030), center=(0.0, 0.025, 0.072), bevel=0.007))
        b.add("hair_03_braids", make_beveled_box((0.038, 0.009, 0.016), center=(0.0, 0.058, 0.081), bevel=0.002))
        # Sculpted Dreadlock / Braided Rows sweeping back across the crown with brass cuffs
        for bx_off in [-0.056, -0.034, -0.012, 0.012, 0.034, 0.056]:
            b_pts = sample_filleted_polyline(
                [(bx_off, 0.155, 0.045), (bx_off * 1.05, 0.186, -0.005), (bx_off * 0.92, 0.145, -0.078), (bx_off * 0.85, 0.085, -0.088)],
                0.025,
                3,
            )
            b.add("hair_03_braids", make_swept_tube(b_pts, radius=0.013, radial_segments=6))
            b.add("role_caution_yellow", make_cylinder(0.015, 0.015, 0.012, center=(bx_off, 0.172, 0.015), segments=8, axis="z"))

        # Open Caterpillar-Yellow (`#FFB703`) Tubular Industrial Exo-Roll-Cage around sides/top of head (100% open in front!)
        cage_outer = sample_filleted_polyline(
            [(-0.108, 0.01, 0.01), (-0.112, 0.195, 0.02), (0.0, 0.215, 0.025), (0.112, 0.195, 0.02), (0.108, 0.01, 0.01)],
            0.035,
            4,
        )
        cage_rear = sample_filleted_polyline(
            [(-0.108, 0.08, 0.01), (-0.105, 0.16, -0.085), (0.105, 0.16, -0.085), (0.108, 0.08, 0.01)],
            0.035,
            3,
        )
        b.add("role_caution_yellow", make_swept_tube(cage_outer, radius=0.013, radial_segments=8))
        b.add("armor_gunmetal", make_swept_tube(cage_rear, radius=0.012, radial_segments=8))
        # Twin Glowing Forehead LED Work-Floodlamps (`#FFF5CC`) mounted atop the open roll-cage bar
        b.add("armor_gunmetal", make_beveled_box((0.125, 0.028, 0.038), center=(0.0, 0.206, 0.038), bevel=0.005))
        for lx in [-0.038, 0.038]:
            b.add("led_flood_white", make_beveled_box((0.038, 0.018, 0.022), center=(lx, 0.206, 0.052), bevel=0.003))
        # Heavy goose-neck jaw mic arm
        g_mic = sample_filleted_polyline([(0.102, 0.065, 0.01), (0.082, 0.045, 0.068), (0.035, 0.045, 0.088)], 0.015, 3)
        b.add("accent_orange", make_swept_tube(g_mic, radius=0.0055, radial_segments=6))

    elif cand_id == 4:
        # #04 ("Dr. Soren Sato" — Botanical & Hydro-Biosphere Medical Specialist):
        # - Warm porcelain-ivory skin (`#ECC4AC`), vivid emerald irises (`#2ECC71`), plum-rose lips (`#B85866`)
        # - Sculpted Platinum-Silver (`#E2E8F0`) Asymmetrical Bob Haircut with `#52B788` Emerald Tips (Zero helmet shell!)
        # - Glowing Emerald (`#00E676`) & UV-Violet (`#9D4EDD`) Floating Neural Temple Halo Crown + Rimless Holo-Glasses
        bob_cap = [(0.0, 0.115), (0.080, 0.125), (0.085, 0.162), (0.068, 0.188), (0.0, 0.196)]
        b.add("hair_04_platinum", make_lathe_limb(bob_cap, center=(0.0, 0.0, -0.006), segments=14, scale_xz=(0.98, 1.06)))
        # Sculpted asymmetrical bob side panels (longer sweeping front side-lock on right `-X`, tucked on left `+X`)
        b.add(
            "hair_04_platinum",
            transform_geom(
                make_beveled_box((0.026, 0.125, 0.095), bevel=0.008),
                translate=(-0.072, 0.098, 0.015),
                rot_xyz_deg=(8.0, -12.0, -10.0),
            ),
        )
        b.add(
            "led_emerald",
            transform_geom(
                make_beveled_box((0.027, 0.032, 0.088), bevel=0.006),
                translate=(-0.066, 0.042, 0.022),
                rot_xyz_deg=(8.0, -12.0, -10.0),
            ),
        )
        # Left side bob panel & emerald tip
        b.add(
            "hair_04_platinum",
            transform_geom(
                make_beveled_box((0.024, 0.105, 0.088), bevel=0.008),
                translate=(0.072, 0.108, 0.008),
                rot_xyz_deg=(6.0, 10.0, 10.0),
            ),
        )
        b.add(
            "led_emerald",
            transform_geom(
                make_beveled_box((0.025, 0.028, 0.082), bevel=0.005),
                translate=(0.068, 0.058, 0.012),
                rot_xyz_deg=(6.0, 10.0, 10.0),
            ),
        )
        # Swept diagonal platinum/emerald front fringe bang across upper right forehead
        b.add(
            "hair_04_platinum",
            transform_geom(
                make_beveled_box((0.068, 0.028, 0.022), bevel=0.006),
                translate=(-0.022, 0.138, 0.074),
                rot_xyz_deg=(12.0, -14.0, -18.0),
            ),
        )
        # Floating Neural Temple Halo Crown (`#00E676` Emerald & `#9D4EDD` UV-Violet)
        b.add("led_emerald", make_closed_torus_ring(0.098, 0.0055, center=(0.0, 0.158, 0.005), rot_xyz_deg=(-12.0, 0.0, 0.0), n_major=16, n_minor=5))
        b.add("led_uv", make_closed_torus_ring(0.094, 0.0045, center=(0.0, 0.168, 0.002), rot_xyz_deg=(-12.0, 0.0, 0.0), n_major=16, n_minor=5))
        # Sleek Rimless Translucent Holo-Diagnostic Glasses across the eyes
        b.add("steel_machined", make_beveled_box((0.098, 0.0035, 0.006), center=(0.0, 0.106, 0.088), bevel=0.001))
        for sx in [-1.0, 1.0]:
            b.add("visor_glass", make_beveled_box((0.034, 0.018, 0.004), center=(sx * 0.028, 0.099, 0.088), bevel=0.001))

    else:
        # #05 ("Spec-Ops Recon Vesper Kade" — Citadel Command & Point-Defense Tactical Recon):
        # - Cool golden-tan skin (`#B6805C`), diagonal left-cheek scar & `#FF6D24` IFF stripe
        # - Sculpted High-Top Jet-Black (`#181B22`) & Signal-Orange (`#D95B26`) Tactical Mohawk Crest with undercut temples
        # - Angular 45°-Faceted Stealth-Gunmetal Lower-Jaw Breather Half-Mask (upper nose, eyes, brow & mohawk exposed!)
        # - Glowing Amber (`#FFB703`) Tactical Visor Strip over Right Eye (-X) + Left Forehead Cybernetic Implant
        # Shaved/undercut dark temple base
        undercut = [(0.0, 0.120), (0.072, 0.125), (0.073, 0.155), (0.056, 0.175), (0.0, 0.180)]
        b.add("hair_05_mohawk", make_lathe_limb(undercut, center=(0.0, 0.0, -0.008), segments=12, scale_xz=(0.92, 1.04)))
        # High-Top Sculpted Tactical Mohawk Spikes & Crimson-Orange Crest Highlights (reaching Y = 0.220m)
        for m_i, (my, mz, mh) in enumerate([
            (0.186, 0.048, 0.045),
            (0.194, 0.022, 0.052),
            (0.196, -0.008, 0.054),
            (0.188, -0.038, 0.048),
            (0.174, -0.065, 0.042),
        ]):
            b.add(
                "hair_05_mohawk",
                transform_geom(
                    make_beveled_box((0.032, mh, 0.034), bevel=0.006),
                    translate=(0.0, my, mz),
                    rot_xyz_deg=(-12.0 + m_i * 8.0, 0.0, 0.0),
                ),
            )
            b.add(
                "accent_orange",
                transform_geom(
                    make_beveled_box((0.014, mh * 0.45, 0.036), bevel=0.003),
                    translate=(0.0, my + mh * 0.32, mz),
                    rot_xyz_deg=(-12.0 + m_i * 8.0, 0.0, 0.0),
                ),
            )
        # Left Forehead (+X) Cybernetic Neural Temple Implant & Cheek Scar / IFF Stripe
        b.add("accent_orange", make_beveled_box((0.022, 0.016, 0.014), center=(0.048, 0.132, 0.064), bevel=0.003))
        b.add("led_amber", make_beveled_box((0.014, 0.008, 0.016), center=(0.048, 0.132, 0.066), bevel=0.002))
        b.add("accent_orange", make_beveled_box((0.028, 0.005, 0.012), center=(0.042, 0.080, 0.072), bevel=0.001))

        # Angular 45°-Faceted Stealth-Gunmetal Lower-Jaw Rebreather Half-Mask (covers chin/mouth Y = 0.012..0.062m ONLY!)
        b.add("armor_gunmetal", make_chamfered_oct_prism(0.118, 0.115, 0.050, center=(0.0, 0.038, 0.038), chamfer=0.028))
        for sx in [-1.0, 1.0]:
            b.add("led_amber", make_beveled_box((0.024, 0.006, 0.018), center=(sx * 0.034, 0.042, 0.088), bevel=0.001))
            b.add("steel_machined", make_cylinder(0.016, 0.016, 0.024, center=(sx * 0.052, 0.034, 0.072), segments=8, axis="z"))

        # Glowing Amber Tactical Optic Visor Strip over Right Eye (-X) only
        b.add("armor_gunmetal", make_beveled_box((0.048, 0.018, 0.022), center=(-0.034, 0.099, 0.080), bevel=0.004))
        b.add("led_amber", make_beveled_box((0.042, 0.010, 0.025), center=(-0.030, 0.099, 0.082), bevel=0.002))

    return b


# ==============================================================================
# ARTICULATED ARMS & LEGS (WITH ROLE-SPECIFIC SILHOUETTE & COLOR VARIATION)
# ==============================================================================
def build_upper_arm_node(is_left: bool, cand_id: int, mats: Dict[str, PBRMaterialDef]) -> NodePartBuilder:
    b = NodePartBuilder(mats, cand_id=cand_id)
    sx = 1.0 if is_left else -1.0
    b.add("joint_bellows", make_joint_ball(0.072, center=(0.0, 0.0, 0.0), segments=8))

    if cand_id == 1:
        p_mat = "role_cobalt_blue" if is_left else "armor_white"
        p_size = (0.125, 0.140, 0.120)
    elif cand_id == 2:
        p_mat = "accent_orange" if is_left else "armor_gunmetal"
        p_size = (0.150, 0.150, 0.135) if is_left else (0.120, 0.135, 0.115)
    elif cand_id == 3:
        p_mat = "role_caution_yellow"
        p_size = (0.160, 0.165, 0.145)
    elif cand_id == 4:
        p_mat = "role_bio_emerald" if is_left else "armor_white"
        p_size = (0.115, 0.130, 0.110)
    else:
        p_mat = "armor_gunmetal"
        p_size = (0.140, 0.155, 0.135)

    b.add(
        p_mat,
        transform_geom(
            make_chamfered_oct_prism(p_size[0], p_size[1], p_size[2], chamfer=0.030, top_scale=0.82),
            translate=(sx * 0.025, 0.01, 0.0),
            rot_xyz_deg=(0.0, 0.0, -sx * 16.0),
        ),
    )
    if cand_id == 2 and is_left:
        b.add("led_cyan", make_beveled_box((0.032, 0.085, 0.095), center=(sx * 0.095, 0.015, 0.0), bevel=0.004))
    elif cand_id == 3:
        b.add("armor_gunmetal", make_beveled_box((0.035, 0.045, 0.155), center=(sx * 0.088, 0.015, 0.0), bevel=0.005))

    bicep_prof = [(0.0, -0.26), (0.048, -0.24), (0.056, -0.14), (0.062, -0.04), (0.0, -0.02)]
    b.add("undersuit_navy", make_lathe_limb(bicep_prof, center=(0.0, 0.0, 0.0), segments=8))
    b.add("armor_white" if cand_id in (1, 2, 4) else "armor_gunmetal", make_cylinder(0.058, 0.064, 0.15, center=(0.0, -0.14, 0.0), segments=8))
    b.add("armor_gunmetal", make_closed_torus_ring(0.060, 0.009, center=(0.0, -0.21, 0.0), n_major=8, n_minor=4))
    return b


def build_forearm_node(is_left: bool, cand_id: int, mats: Dict[str, PBRMaterialDef]) -> NodePartBuilder:
    b = NodePartBuilder(mats, cand_id=cand_id)
    sx = 1.0 if is_left else -1.0
    b.add("joint_bellows", make_joint_ball(0.054, center=(0.0, 0.0, 0.0), segments=8))
    b.add("armor_gunmetal", make_beveled_box((0.082, 0.065, 0.055), center=(0.0, 0.0, -0.032), bevel=0.012))

    fore_prof = [(0.0, -0.24), (0.042, -0.22), (0.052, -0.11), (0.055, -0.03), (0.0, -0.01)]
    b.add("armor_white" if cand_id in (1, 2, 4) else "armor_gunmetal", make_lathe_limb(fore_prof, center=(0.0, 0.0, 0.0), segments=8))
    b.add("steel_machined", make_closed_torus_ring(0.046, 0.008, center=(0.0, -0.215, 0.0), n_major=8, n_minor=4))

    if is_left:
        b.add("armor_gunmetal", make_beveled_box((0.052, 0.115, 0.048), center=(sx * 0.032, -0.125, 0.025), bevel=0.008))
        b.add("chest_telemetry", make_beveled_box((0.038, 0.095, 0.052), center=(sx * 0.036, -0.125, 0.028), bevel=0.004))
        if cand_id == 2:
            b.add("led_cyan", make_closed_torus_ring(0.036, 0.005, center=(sx * 0.055, -0.125, 0.055), rot_xyz_deg=(0.0, 0.0, 90.0), n_major=8, n_minor=4))
            b.add("visor_glass", make_beveled_box((0.024, 0.105, 0.065), center=(sx * 0.058, -0.125, 0.045), bevel=0.004))
    else:
        b.add("steel_machined", make_beveled_box((0.048, 0.095, 0.045), center=(sx * 0.032, -0.13, 0.015), bevel=0.008))
        b.add("accent_orange", make_beveled_box((0.052, 0.035, 0.048), center=(sx * 0.035, -0.16, 0.018), bevel=0.005))

    b.add("undersuit_navy", make_beveled_box((0.042, 0.068, 0.078), center=(0.0, -0.258, 0.006), bevel=0.010))
    b.add("armor_white" if cand_id != 5 else "armor_gunmetal", make_beveled_box((0.046, 0.052, 0.068), center=(sx * 0.006, -0.254, 0.006), bevel=0.008))
    b.add(
        "joint_bellows",
        transform_geom(make_beveled_box((0.022, 0.052, 0.024), bevel=0.006), translate=(-sx * 0.012, -0.275, 0.045), rot_xyz_deg=(-28.0, 0.0, 0.0)),
    )
    for f_z, f_len in [(0.026, 0.058), (0.002, 0.062), (-0.022, 0.054)]:
        b.add("joint_bellows", make_beveled_box((0.036, f_len, 0.020), center=(0.0, -0.308, f_z), bevel=0.005))
    return b


def build_upleg_node(is_left: bool, cand_id: int, mats: Dict[str, PBRMaterialDef]) -> NodePartBuilder:
    b = NodePartBuilder(mats, cand_id=cand_id)
    sx = 1.0 if is_left else -1.0
    b.add("joint_bellows", make_joint_ball(0.084, center=(0.0, 0.0, 0.0), segments=8))
    thigh_prof = [(0.0, -0.43), (0.066, -0.40), (0.082, -0.22), (0.094, -0.06), (0.0, -0.02)]
    b.add("undersuit_navy", make_lathe_limb(thigh_prof, center=(0.0, 0.0, 0.0), segments=10, scale_xz=(0.96, 1.06)))
    thigh_mat = "armor_gunmetal" if (cand_id == 2 and not is_left) else ("armor_gunmetal" if cand_id == 5 else "armor_white")
    b.add(thigh_mat, make_chamfered_oct_prism(0.165, 0.185, 0.29, center=(sx * 0.008, -0.21, 0.012), chamfer=0.038, top_scale=1.12))
    b.add("accent_orange" if is_left else "steel_machined", make_beveled_box((0.038, 0.14, 0.075), center=(sx * 0.086, -0.19, 0.0), bevel=0.008))
    b.add("led_cyan", make_beveled_box((0.042, 0.10, 0.018), center=(sx * 0.088, -0.19, 0.042), bevel=0.003))
    return b


def build_leg_node(is_left: bool, cand_id: int, mats: Dict[str, PBRMaterialDef]) -> NodePartBuilder:
    b = NodePartBuilder(mats, cand_id=cand_id)
    b.add("joint_bellows", make_joint_ball(0.068, center=(0.0, 0.0, 0.0), segments=8))
    b.add("armor_gunmetal", make_chamfered_oct_prism(0.135, 0.145, 0.105, center=(0.0, 0.005, 0.028), chamfer=0.032))
    b.add("steel_machined", make_cylinder(0.032, 0.032, 0.148, center=(0.0, 0.0, 0.0), segments=8, axis="x"))
    calf_prof = [(0.0, -0.39), (0.054, -0.36), (0.074, -0.16), (0.068, -0.05), (0.0, -0.02)]
    b.add("armor_white" if cand_id != 5 else "armor_gunmetal", make_lathe_limb(calf_prof, center=(0.0, 0.0, 0.0), segments=10, scale_xz=(0.94, 1.08)))
    b.add("armor_gunmetal", make_beveled_box((0.085, 0.25, 0.065), center=(0.0, -0.21, 0.048), bevel=0.014))
    b.add("accent_orange", make_closed_torus_ring(0.062, 0.009, center=(0.0, -0.33, 0.0), n_major=8, n_minor=4))
    return b


def build_foot_node(is_left: bool, cand_id: int, mats: Dict[str, PBRMaterialDef]) -> NodePartBuilder:
    b = NodePartBuilder(mats, cand_id=cand_id)
    b.add("joint_bellows", make_joint_ball(0.054, center=(0.0, 0.0, 0.0), segments=8))
    b.add("steel_machined", make_closed_torus_ring(0.058, 0.010, center=(0.0, -0.015, 0.0), n_major=8, n_minor=4))
    b.add("armor_white" if cand_id != 5 else "armor_gunmetal", make_chamfered_oct_prism(0.118, 0.245, 0.056, center=(0.0, -0.034, 0.042), chamfer=0.028, top_scale=0.86))
    b.add("armor_gunmetal", make_chamfered_oct_prism(0.112, 0.115, 0.048, center=(0.0, -0.032, 0.115), chamfer=0.026, top_scale=0.78))
    b.add("steel_machined", make_beveled_box((0.122, 0.020, 0.258), center=(0.0, -0.070, 0.042), bevel=0.0))
    b.add("led_amber", make_beveled_box((0.075, 0.016, 0.018), center=(0.0, -0.052, -0.084), bevel=0.002))
    b.add("led_cyan", make_beveled_box((0.065, 0.012, 0.015), center=(0.0, -0.054, 0.168), bevel=0.002))
    return b


# ==============================================================================
# QUATERNION & BIOMECHANICAL `WalkCycle` ANIMATION GENERATOR (1.20s, 33 KEYFRAMES)
# ==============================================================================
def euler_xyz_deg_to_quat_xyzw(rx_deg: float, ry_deg: float, rz_deg: float) -> List[float]:
    hx = math.radians(rx_deg) * 0.5
    hy = math.radians(ry_deg) * 0.5
    hz = math.radians(rz_deg) * 0.5
    cx, sx = math.cos(hx), math.sin(hx)
    cy, sy = math.cos(hy), math.sin(hy)
    cz, sz = math.cos(hz), math.sin(hz)
    qx = sx * cy * cz - cx * sy * sz
    qy = cx * sy * cz + sx * cy * sz
    qz = cx * cy * sz - sx * sy * cz
    qw = cx * cy * cz + sx * sy * sz
    n = math.sqrt(qx * qx + qy * qy + qz * qz + qw * qw)
    return [float(qx / n), float(qy / n), float(qz / n), float(qw / n)]


def sample_walk_cycle_tracks(duration: float = 1.20, n_frames: int = 33) -> Tuple[np.ndarray, Dict[str, Dict[str, np.ndarray]]]:
    times = np.linspace(0.0, duration, n_frames, dtype=np.float32)
    tracks: Dict[str, Dict[str, List[List[float]]]] = {
        "Hips": {"translation": [], "rotation": []},
        "Spine": {"rotation": []},
        "Chest": {"rotation": []},
        "Head": {"rotation": []},
        "LeftUpperArm": {"rotation": []},
        "LeftForeArm": {"rotation": []},
        "RightUpperArm": {"rotation": []},
        "RightForeArm": {"rotation": []},
        "LeftUpLeg": {"rotation": []},
        "LeftLeg": {"rotation": []},
        "LeftFoot": {"rotation": []},
        "RightUpLeg": {"rotation": []},
        "RightLeg": {"rotation": []},
        "RightFoot": {"rotation": []},
    }

    for k in range(n_frames):
        phi = 0.0 if (k == n_frames - 1) else (2.0 * math.pi * (k / float(n_frames - 1)))

        hx = -0.016 * math.sin(phi)
        hy = 0.960 - 0.022 * math.cos(2.0 * phi)
        hz = 0.008 * math.sin(2.0 * phi)
        tracks["Hips"]["translation"].append([hx, hy, hz])

        hips_rx = 2.5 + 1.2 * math.cos(2.0 * phi)
        hips_ry = -5.5 * math.cos(phi)
        hips_rz = 3.0 * math.sin(phi)
        tracks["Hips"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(hips_rx, hips_ry, hips_rz))

        spine_rx = 2.0 + 0.8 * math.cos(2.0 * phi)
        spine_ry = 3.2 * math.cos(phi)
        spine_rz = -1.5 * math.sin(phi)
        tracks["Spine"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(spine_rx, spine_ry, spine_rz))

        chest_rx = 2.5 + 1.0 * math.cos(2.0 * phi)
        chest_ry = 4.8 * math.cos(phi)
        chest_rz = -2.0 * math.sin(phi)
        tracks["Chest"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(chest_rx, chest_ry, chest_rz))

        head_rx = -2.5 - 1.0 * math.cos(2.0 * phi)
        head_ry = -3.0 * math.cos(phi)
        head_rz = 1.0 * math.sin(phi)
        tracks["Head"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(head_rx, head_ry, head_rz))

        for leg_prefix, th in [("Left", phi), ("Right", phi + math.pi)]:
            thigh_rx = -23.0 * math.cos(th) - 2.0
            tracks[f"{leg_prefix}UpLeg"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(thigh_rx, 0.0, 0.0))

            swing_lift = max(0.0, -math.sin(th)) ** 1.25
            stance_cushion = max(0.0, math.sin(th))
            knee_rx = 5.0 + 36.0 * swing_lift + 7.0 * stance_cushion
            tracks[f"{leg_prefix}Leg"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(knee_rx, 0.0, 0.0))

            foot_rx = -10.0 * math.cos(th) + 9.0 * math.sin(th)
            tracks[f"{leg_prefix}Foot"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(foot_rx, 0.0, 0.0))

        for arm_prefix, al, rz_abduct in [("Left", phi + math.pi, 5.0), ("Right", phi, -5.0)]:
            uarm_rx = -19.0 * math.cos(al) + 2.0
            tracks[f"{arm_prefix}UpperArm"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(uarm_rx, 0.0, rz_abduct))

            fore_rx = -18.0 - 15.0 * max(0.0, math.cos(al))
            tracks[f"{arm_prefix}ForeArm"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(fore_rx, 0.0, 0.0))

    np_tracks: Dict[str, Dict[str, np.ndarray]] = {}
    for node_name, ch_dict in tracks.items():
        np_tracks[node_name] = {k: np.array(v, dtype=np.float32) for k, v in ch_dict.items()}
    return times, np_tracks


_CHAR_TEX_BYTES_CACHE: Dict[Tuple, bytes] = {}


def _get_char_texture_png_bytes(mdef: PBRMaterialDef) -> bytes:
    key = (mdef.name, mdef.base_color, mdef.texture_path, mdef.alpha_mode)
    if key in _CHAR_TEX_BYTES_CACHE:
        return _CHAR_TEX_BYTES_CACHE[key]

    if mdef.texture_path and os.path.exists(mdef.texture_path):
        if mdef.alpha_mode == "BLEND":
            im = Image.open(mdef.texture_path).convert("RGBA").resize((512, 512), Image.Resampling.LANCZOS)
        else:
            im = Image.open(mdef.texture_path).convert("RGB").resize((512, 512), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format="PNG", optimize=True)
        _CHAR_TEX_BYTES_CACHE[key] = buf.getvalue()
        return _CHAR_TEX_BYTES_CACHE[key]

    N = 64
    yy, xx = np.mgrid[0:N, 0:N].astype(np.float32) / float(N)
    base_rgb = np.array(mdef.base_color[:3], dtype=np.float32) * 255.0
    micro = (0.6 * np.sin(2.0 * math.pi * xx) * np.cos(2.0 * math.pi * yy))[:, :, None]
    arr = np.clip(base_rgb[None, None, :] + micro, 0.0, 255.0).astype(np.uint8)
    im = Image.fromarray(arr, mode="RGB")
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    _CHAR_TEX_BYTES_CACHE[key] = buf.getvalue()
    return _CHAR_TEX_BYTES_CACHE[key]


def build_and_export_character_glb(cand_id: int, filepath: str, mats: Dict[str, PBRMaterialDef]) -> Dict[str, any]:
    node_specs = [
        ("CharacterRoot", None, (0.0, 0.0, 0.0), None),
        ("Hips", "CharacterRoot", (0.0, 0.96, 0.0), build_hips_node(cand_id, mats)),
        ("Spine", "Hips", (0.0, 0.16, 0.0), build_spine_node(cand_id, mats)),
        ("Chest", "Spine", (0.0, 0.22, 0.0), build_chest_node(cand_id, mats)),
        ("Head", "Chest", (0.0, 0.24, 0.0), build_head_node(cand_id, mats)),
        ("LeftUpperArm", "Chest", (0.21, 0.16, 0.0), build_upper_arm_node(True, cand_id, mats)),
        ("LeftForeArm", "LeftUpperArm", (0.0, -0.27, 0.0), build_forearm_node(True, cand_id, mats)),
        ("RightUpperArm", "Chest", (-0.21, 0.16, 0.0), build_upper_arm_node(False, cand_id, mats)),
        ("RightForeArm", "RightUpperArm", (0.0, -0.27, 0.0), build_forearm_node(False, cand_id, mats)),
        ("LeftUpLeg", "Hips", (0.105, -0.04, 0.0), build_upleg_node(True, cand_id, mats)),
        ("LeftLeg", "LeftUpLeg", (0.0, -0.44, 0.0), build_leg_node(True, cand_id, mats)),
        ("LeftFoot", "LeftLeg", (0.0, -0.40, 0.0), build_foot_node(True, cand_id, mats)),
        ("RightUpLeg", "Hips", (-0.105, -0.04, 0.0), build_upleg_node(False, cand_id, mats)),
        ("RightLeg", "RightUpLeg", (0.0, -0.44, 0.0), build_leg_node(False, cand_id, mats)),
        ("RightFoot", "RightLeg", (0.0, -0.40, 0.0), build_foot_node(False, cand_id, mats)),
    ]

    gltf = pygltflib.GLTF2(
        asset=pygltflib.Asset(version="2.0", generator="CylinderHab7-Rook-ArticulatedCharacterGLBBuilder"),
        scene=0,
        scenes=[pygltflib.Scene(name=f"Aegis7Crew_R1_{cand_id:02d}", nodes=[0])],
        nodes=[],
        meshes=[],
        materials=[],
        accessors=[],
        bufferViews=[],
        buffers=[],
        textures=[],
        images=[],
        samplers=[
            pygltflib.Sampler(
                magFilter=pygltflib.LINEAR,
                minFilter=pygltflib.LINEAR_MIPMAP_LINEAR,
                wrapS=pygltflib.REPEAT,
                wrapT=pygltflib.REPEAT,
            )
        ],
        animations=[],
    )

    binary_blob = bytearray()

    def _append_bytes(data: bytes, target: Optional[int] = None) -> int:
        while len(binary_blob) % 4 != 0:
            binary_blob.append(0)
        offset = len(binary_blob)
        binary_blob.extend(data)
        while len(binary_blob) % 4 != 0:
            binary_blob.append(0)
        bv_idx = len(gltf.bufferViews)
        gltf.bufferViews.append(
            pygltflib.BufferView(buffer=0, byteOffset=offset, byteLength=len(data), target=target)
        )
        return bv_idx

    tex_cache: Dict[str, int] = {}
    mat_cache: Dict[str, int] = {}

    def _get_or_create_mat(mdef: PBRMaterialDef) -> int:
        if mdef.name in mat_cache:
            return mat_cache[mdef.name]
        t_key = f"{mdef.name}_{mdef.texture_path}_{mdef.alpha_mode}"
        if t_key not in tex_cache:
            png_bytes = _get_char_texture_png_bytes(mdef)
            bv_idx = _append_bytes(png_bytes, target=None)
            img_idx = len(gltf.images)
            gltf.images.append(pygltflib.Image(bufferView=bv_idx, mimeType="image/png", name=f"{mdef.name}.png"))
            tex_idx = len(gltf.textures)
            gltf.textures.append(pygltflib.Texture(sampler=0, source=img_idx, name=f"{mdef.name}_tex"))
            tex_cache[t_key] = tex_idx

        tex_info = pygltflib.TextureInfo(index=tex_cache[t_key], texCoord=0)
        bcf = (
            [float(c) for c in mdef.base_color]
            if mdef.alpha_mode == "BLEND"
            else [1.0, 1.0, 1.0, 1.0]
        )
        pbr = pygltflib.PbrMetallicRoughness(
            baseColorFactor=bcf,
            metallicFactor=float(mdef.metallic),
            roughnessFactor=float(mdef.roughness),
            baseColorTexture=tex_info,
        )
        mat = pygltflib.Material(
            name=mdef.name,
            pbrMetallicRoughness=pbr,
            emissiveFactor=list(mdef.emissive) if max(mdef.emissive) > 0.01 else None,
            emissiveTexture=tex_info if (mdef.name == "Mat_OLED_ChestTelemetryAndLEDs") else None,
            doubleSided=mdef.double_sided,
            alphaMode=mdef.alpha_mode,
        )
        m_idx = len(gltf.materials)
        gltf.materials.append(mat)
        mat_cache[mdef.name] = m_idx
        return m_idx

    name_to_node_idx: Dict[str, int] = {}
    world_offset_by_node: Dict[str, np.ndarray] = {}

    for idx_n, (n_name, parent_name, trans_xyz, _) in enumerate(node_specs):
        name_to_node_idx[n_name] = idx_n
        t_arr = np.array(trans_xyz, dtype=np.float32)
        if parent_name is None:
            world_offset_by_node[n_name] = t_arr
        else:
            world_offset_by_node[n_name] = world_offset_by_node[parent_name] + t_arr
        gltf.nodes.append(
            pygltflib.Node(
                name=n_name,
                translation=[float(trans_xyz[0]), float(trans_xyz[1]), float(trans_xyz[2])],
                rotation=[0.0, 0.0, 0.0, 1.0],
                scale=[1.0, 1.0, 1.0],
                children=[],
            )
        )

    for idx_n, (n_name, parent_name, _, _) in enumerate(node_specs):
        if parent_name is not None:
            p_idx = name_to_node_idx[parent_name]
            gltf.nodes[p_idx].children.append(idx_n)

    total_verts = 0
    total_tris = 0
    world_pts_all: List[np.ndarray] = []

    for idx_n, (n_name, _, _, part_builder) in enumerate(node_specs):
        if part_builder is None:
            continue
        prims: List[pygltflib.Primitive] = []
        w_off = world_offset_by_node[n_name]
        for mat_key, g_list in part_builder.buckets.items():
            if not g_list:
                continue
            p, n, u, tris = merge_geometries(g_list)
            pos = np.ascontiguousarray(p, dtype=np.float32)
            norms = np.ascontiguousarray(n, dtype=np.float32)
            n_lens = np.linalg.norm(norms, axis=1, keepdims=True)
            norms = np.ascontiguousarray(norms / np.where(n_lens < 1e-12, 1.0, n_lens), dtype=np.float32)
            uvs = np.ascontiguousarray(np.clip(u, 0.0, 1.0), dtype=np.float32)
            indices = np.ascontiguousarray(tris.reshape(-1), dtype=np.uint32)

            world_pts_all.append(pos + w_off[None, :])
            total_verts += len(pos)
            total_tris += len(indices) // 3

            bv_pos = _append_bytes(pos.tobytes(), target=pygltflib.ARRAY_BUFFER)
            bv_norm = _append_bytes(norms.tobytes(), target=pygltflib.ARRAY_BUFFER)
            bv_uv = _append_bytes(uvs.tobytes(), target=pygltflib.ARRAY_BUFFER)
            bv_idx = _append_bytes(indices.tobytes(), target=pygltflib.ELEMENT_ARRAY_BUFFER)

            acc_pos = len(gltf.accessors)
            gltf.accessors.append(
                pygltflib.Accessor(
                    bufferView=bv_pos,
                    byteOffset=0,
                    componentType=pygltflib.FLOAT,
                    count=len(pos),
                    type=pygltflib.VEC3,
                    min=pos.min(axis=0).tolist(),
                    max=pos.max(axis=0).tolist(),
                )
            )
            acc_norm = len(gltf.accessors)
            gltf.accessors.append(
                pygltflib.Accessor(
                    bufferView=bv_norm,
                    byteOffset=0,
                    componentType=pygltflib.FLOAT,
                    count=len(norms),
                    type=pygltflib.VEC3,
                )
            )
            acc_uv = len(gltf.accessors)
            gltf.accessors.append(
                pygltflib.Accessor(
                    bufferView=bv_uv,
                    byteOffset=0,
                    componentType=pygltflib.FLOAT,
                    count=len(uvs),
                    type=pygltflib.VEC2,
                )
            )
            acc_idx = len(gltf.accessors)
            gltf.accessors.append(
                pygltflib.Accessor(
                    bufferView=bv_idx,
                    byteOffset=0,
                    componentType=pygltflib.UNSIGNED_INT,
                    count=len(indices),
                    type=pygltflib.SCALAR,
                    min=[int(indices.min())],
                    max=[int(indices.max())],
                )
            )

            mat_idx = _get_or_create_mat(mats[mat_key])
            prims.append(
                pygltflib.Primitive(
                    attributes=pygltflib.Attributes(POSITION=acc_pos, NORMAL=acc_norm, TEXCOORD_0=acc_uv),
                    indices=acc_idx,
                    material=mat_idx,
                    mode=pygltflib.TRIANGLES,
                )
            )

        if prims:
            m_idx = len(gltf.meshes)
            gltf.meshes.append(pygltflib.Mesh(name=f"{n_name}_Mesh", primitives=prims))
            gltf.nodes[idx_n].mesh = m_idx

    # Embed `WalkCycle` Animation (duration 1.20s, 33 keyframes)
    times, tracks = sample_walk_cycle_tracks(duration=1.20, n_frames=33)
    bv_time = _append_bytes(times.tobytes(), target=None)
    acc_time = len(gltf.accessors)
    gltf.accessors.append(
        pygltflib.Accessor(
            bufferView=bv_time,
            byteOffset=0,
            componentType=pygltflib.FLOAT,
            count=len(times),
            type=pygltflib.SCALAR,
            min=[float(times.min())],
            max=[float(times.max())],
        )
    )

    anim_samplers: List[pygltflib.AnimationSampler] = []
    anim_channels: List[pygltflib.AnimationChannel] = []

    for node_name, ch_dict in tracks.items():
        node_idx = name_to_node_idx[node_name]
        for path_name, arr_val in ch_dict.items():
            arr_c = np.ascontiguousarray(arr_val, dtype=np.float32)
            bv_val = _append_bytes(arr_c.tobytes(), target=None)
            acc_val = len(gltf.accessors)
            acc_type = pygltflib.VEC3 if path_name == "translation" else pygltflib.VEC4
            gltf.accessors.append(
                pygltflib.Accessor(
                    bufferView=bv_val,
                    byteOffset=0,
                    componentType=pygltflib.FLOAT,
                    count=len(arr_c),
                    type=acc_type,
                    min=arr_c.min(axis=0).tolist(),
                    max=arr_c.max(axis=0).tolist(),
                )
            )
            samp_idx = len(anim_samplers)
            anim_samplers.append(
                pygltflib.AnimationSampler(
                    input=acc_time,
                    interpolation="LINEAR",
                    output=acc_val,
                )
            )
            anim_channels.append(
                pygltflib.AnimationChannel(
                    sampler=samp_idx,
                    target=pygltflib.AnimationChannelTarget(node=node_idx, path=path_name),
                )
            )

    gltf.animations.append(
        pygltflib.Animation(
            name="WalkCycle",
            samplers=anim_samplers,
            channels=anim_channels,
        )
    )

    gltf.buffers.append(pygltflib.Buffer(byteLength=len(binary_blob)))
    gltf.set_binary_blob(bytes(binary_blob))
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    gltf.save_binary(filepath)

    all_w = np.vstack(world_pts_all)
    min_pt = all_w.min(axis=0)
    max_pt = all_w.max(axis=0)
    dims = (max_pt - min_pt).tolist()

    return {
        "candidate_id": cand_id,
        "filepath": filepath,
        "vertices": total_verts,
        "triangles": total_tris,
        "nodes": len(gltf.nodes),
        "animations": [a.name for a in gltf.animations],
        "animation_channels": len(anim_channels),
        "keyframes": len(times),
        "duration_s": float(times[-1]),
        "min": [round(float(x), 5) for x in min_pt],
        "max": [round(float(x), 5) for x in max_pt],
        "dimensions": [round(float(x), 4) for x in dims],
        "materials": [m.name for m in gltf.materials],
    }


def build_all_aegis7_characters():
    mats = get_character_materials()
    results = []
    for cand_id in range(1, 6):
        main_p = os.path.join(OUT_CHAR_ROOT, f"char_crew_r1_{cand_id:02d}.glb")
        info = build_and_export_character_glb(cand_id, main_p, mats)

        aliases = [
            os.path.join(OUT_CHAR_R1_DIR, f"char_crew_r1_{cand_id:02d}.glb"),
            os.path.join(OUT_CHAR_ROOT, f"char_01_r1_{cand_id:02d}.glb"),
            os.path.join(OUT_CHAR_01_DIR, f"char_01_r1_{cand_id:02d}.glb"),
        ]
        for dst in aliases:
            shutil.copyfile(main_p, dst)

        if cand_id == 2:
            for w_name in [
                "char_crew_winner_01_aegis7_officer.glb",
                "char_crew_winner_01_aegis7_commander.glb",
                "char_crew_winner_01.glb",
                "char_01_winner_01.glb",
                "char_winner_01.glb",
            ]:
                shutil.copyfile(main_p, os.path.join(WINNERS_DIR, w_name))

        dims = info["dimensions"]
        sz_kb = os.path.getsize(main_p) / 1024.0
        print(
            f"[character] char_crew_r1_{cand_id:02d}.glb | {dims[0]:.3f}m W x {dims[2]:.3f}m D x {dims[1]:.3f}m H | "
            f"tris={info['triangles']:4d} | nodes={info['nodes']:2d} | anims={info['animations']} ({info['keyframes']} kf) | "
            f"min_y={info['min'][1]:.5f} | {sz_kb:6.1f} KB"
        )
        results.append(info)

    manifest_path = os.path.join(OUT_CHAR_ROOT, "character_aegis7_crew_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(results, f, indent=2)
    shutil.copyfile(manifest_path, os.path.join(OUT_CHAR_R1_DIR, "character_aegis7_crew_manifest.json"))
    print(f"Saved character manifest to {manifest_path}")
    return results


if __name__ == "__main__":
    build_all_aegis7_characters()
