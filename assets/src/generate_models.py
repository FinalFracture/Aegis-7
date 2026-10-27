#!/usr/bin/env python3
"""
Procedural 3D Asset Generator for Project Cylinder Hab-7 (Godot 4 .glb Pipeline).
Generates all 9 hero habitat Living Quarters models with multi-part beveled geometry,
clean normals, [0,1] UVs, and embedded PBR textures + emissive materials.
"""
import os
import sys
import math
import json
from typing import List, Dict
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glb_builder import (
    PBRMaterialDef,
    SubMesh,
    make_beveled_box,
    make_cylinder,
    make_lathe_dome,
    make_quad_panel,
    merge_geometries,
    export_glb,
)
import generate_textures

TEX_DIR = "/workspace/game-project/assets/textures"
GLB_DIR = "/workspace/game-project/assets/glb"
os.makedirs(GLB_DIR, exist_ok=True)


def resolve_texture(preferred_names, fallback_name):
    """If Sloane placed a texture matching preferred_names, use it; otherwise use fallback_name."""
    if os.path.exists(TEX_DIR):
        existing = os.listdir(TEX_DIR)
        for cand in preferred_names:
            if cand in existing:
                return os.path.join(TEX_DIR, cand)
    return os.path.join(TEX_DIR, fallback_name)


def get_materials():
    tex_wallpaper = resolve_texture(
        ["wallpaper_retro_70s.png", "wallpaper_habitat.png", "wallpaper_retro_geometric.png"],
        "wallpaper_retro_geometric.png",
    )
    tex_wainscot = resolve_texture(
        ["wainscoting_panel.png", "bulkhead_lower.png", "bulkhead_wainscoting.png"],
        "bulkhead_wainscoting.png",
    )
    tex_wood = resolve_texture(
        ["floor_parquet.png", "wood_laminate.png", "wood_parquet_warm.png"],
        "wood_parquet_warm.png",
    )
    tex_crt = resolve_texture(
        ["crt_screen.png", "crt_screen_telemetry.png"],
        "crt_screen_telemetry.png",
    )
    tex_rug = resolve_texture(
        ["rug_pattern.png", "area_rug.png", "rug_retro_woven.png"],
        "rug_retro_woven.png",
    )
    tex_fabric = resolve_texture(
        ["fabric_cushion.png", "fabric_terracotta_cushion.png"],
        "fabric_terracotta_cushion.png",
    )
    tex_brass = resolve_texture(
        ["metal_brass.png", "metal_brushed_brass.png"],
        "metal_brushed_brass.png",
    )

    return {
        "wallpaper_upper": PBRMaterialDef(
            name="Mat_Wallpaper_RetroGeometric",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.02,
            roughness=0.78,
            texture_path=tex_wallpaper,
            double_sided=True,
        ),
        "bulkhead_wainscot": PBRMaterialDef(
            name="Mat_Bulkhead_Wainscoting",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.18,
            roughness=0.52,
            texture_path=tex_wainscot,
            double_sided=True,
        ),
        "bulkhead_cream": PBRMaterialDef(
            name="Mat_Bulkhead_CreamPolymer",
            base_color=(0.86, 0.82, 0.75, 1.0),
            metallic=0.12,
            roughness=0.45,
        ),
        "bulkhead_structural": PBRMaterialDef(
            name="Mat_Bulkhead_StructuralSlate",
            base_color=(0.34, 0.36, 0.38, 1.0),
            metallic=0.55,
            roughness=0.42,
        ),
        "wood_parquet": PBRMaterialDef(
            name="Mat_Wood_WarmTeakParquet",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.04,
            roughness=0.48,
            texture_path=tex_wood,
        ),
        "wood_walnut": PBRMaterialDef(
            name="Mat_Wood_WalnutLaminate",
            base_color=(0.88, 0.76, 0.64, 1.0),
            metallic=0.05,
            roughness=0.42,
            texture_path=tex_wood,
        ),
        "brass_trim": PBRMaterialDef(
            name="Mat_Metal_BrushedBrass",
            base_color=(1.0, 0.92, 0.75, 1.0),
            metallic=0.82,
            roughness=0.28,
            texture_path=tex_brass,
        ),
        "chrome_steel": PBRMaterialDef(
            name="Mat_Metal_BrushedChrome",
            base_color=(0.82, 0.84, 0.86, 1.0),
            metallic=0.88,
            roughness=0.22,
        ),
        "crt_casing_ochre": PBRMaterialDef(
            name="Mat_Plastic_CassetteOchre",
            base_color=(0.86, 0.64, 0.26, 1.0),
            metallic=0.05,
            roughness=0.38,
        ),
        "crt_bezel_dark": PBRMaterialDef(
            name="Mat_Plastic_CharcoalBezel",
            base_color=(0.14, 0.14, 0.15, 1.0),
            metallic=0.15,
            roughness=0.35,
        ),
        "crt_screen_glow": PBRMaterialDef(
            name="Mat_CRT_PhosphorScreen",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.05,
            roughness=0.15,
            emissive=(0.95, 0.68, 0.18),
            texture_path=tex_crt,
        ),
        "emissive_warm_light": PBRMaterialDef(
            name="Mat_Emissive_WarmAmberLight",
            base_color=(1.0, 0.92, 0.76, 1.0),
            metallic=0.0,
            roughness=0.2,
            emissive=(1.0, 0.82, 0.48),
        ),
        "emissive_lamp_shade": PBRMaterialDef(
            name="Mat_Emissive_MushroomShade",
            base_color=(0.98, 0.84, 0.56, 1.0),
            metallic=0.02,
            roughness=0.32,
            emissive=(0.92, 0.66, 0.28),
            double_sided=True,
        ),
        "emissive_grow_light": PBRMaterialDef(
            name="Mat_Emissive_HydroGrowBar",
            base_color=(1.0, 0.95, 0.86, 1.0),
            metallic=0.0,
            roughness=0.2,
            emissive=(0.96, 0.86, 0.64),
        ),
        "fabric_terracotta": PBRMaterialDef(
            name="Mat_Fabric_TerracottaBoucle",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.0,
            roughness=0.85,
            texture_path=tex_fabric,
        ),
        "fabric_mustard": PBRMaterialDef(
            name="Mat_Fabric_MustardWool",
            base_color=(0.88, 0.66, 0.24, 1.0),
            metallic=0.0,
            roughness=0.82,
        ),
        "fabric_cream_quilt": PBRMaterialDef(
            name="Mat_Fabric_CreamQuilt",
            base_color=(0.93, 0.89, 0.81, 1.0),
            metallic=0.0,
            roughness=0.78,
        ),
        "fabric_avocado_blanket": PBRMaterialDef(
            name="Mat_Fabric_AvocadoThrow",
            base_color=(0.44, 0.53, 0.34, 1.0),
            metallic=0.0,
            roughness=0.84,
        ),
        "rug_woven": PBRMaterialDef(
            name="Mat_Rug_RetroGeometricWoven",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.0,
            roughness=0.90,
            texture_path=tex_rug,
        ),
        "smoked_amber_acrylic": PBRMaterialDef(
            name="Mat_Acrylic_SmokedAmber",
            base_color=(0.76, 0.46, 0.18, 1.0),
            metallic=0.10,
            roughness=0.16,
        ),
        "foliage_deep_green": PBRMaterialDef(
            name="Mat_Foliage_MonsteraGreen",
            base_color=(0.18, 0.46, 0.22, 1.0),
            metallic=0.02,
            roughness=0.55,
            double_sided=True,
        ),
        "foliage_bright_fern": PBRMaterialDef(
            name="Mat_Foliage_LushFern",
            base_color=(0.30, 0.60, 0.26, 1.0),
            metallic=0.02,
            roughness=0.58,
            double_sided=True,
        ),
        "hydro_soil_substrate": PBRMaterialDef(
            name="Mat_Hydro_ExpandedClayPebbles",
            base_color=(0.36, 0.24, 0.18, 1.0),
            metallic=0.0,
            roughness=0.92,
        ),
        "water_sight_cyan": PBRMaterialDef(
            name="Mat_Hydro_NutrientWater",
            base_color=(0.24, 0.68, 0.76, 1.0),
            metallic=0.1,
            roughness=0.15,
            emissive=(0.08, 0.28, 0.34),
        ),
    }


def add_part(submeshes: List[SubMesh], name: str, geom, mat: PBRMaterialDef):
    p, n, u, idx = geom
    submeshes.append(SubMesh(name=name, positions=p, normals=n, uvs=u, indices=idx, material=mat))


# ==============================================================================
# 1. ROOM SHELL (`room_shell.glb`)
# ==============================================================================
def build_room_shell(mats) -> Dict:
    """
    4.0m wide (X: -2.0 to +2.0) x 5.0m deep (Z: -2.5 to +2.5) x 3.0m tall (Y: 0.0 to 3.0).
    - Floor at Y=0 with warm parquet decking + perimeter bulkhead trim.
    - Lower bulkhead wainscoting (Y: 0.0 to 1.0m) with chamfered structural panels and brass dado rail at Y=1.0m.
    - Upper wallpapered walls (Y: 1.0m to 3.0m) mapped cleanly to retro geometric wallpaper.
    - Ceiling (Y=3.0m) with structural O'Neill hull ribs and recessed warm light strips.
    - North wall (Z = -2.5m): Panoramic chamfered habitat viewport window aperture
      (X: -1.25 to +1.25, Y: 0.85 to 2.35 left completely open so Gage's exterior vista & sunlight stream through!)
      with thick chamfered octagonal/rounded frame, deep window sill, and structural bolts.
    - South wall (Z = +2.5m): Framed bulkhead doorway opening (X: -0.55 to +0.55, Y: 0.0 to 2.20)
      with heavy cassette-futurism airlock/corridor frame and recessed sliding door panel.
    """
    sm = []

    # 1. Floor (Y = 0.0 to 0.02)
    add_part(
        sm,
        "Floor_ParquetDecking",
        make_quad_panel((-2.0, 0.002, 2.5), (2.0, 0.002, 2.5), (2.0, 0.002, -2.5), (-2.0, 0.002, -2.5)),
        mats["wood_parquet"],
    )
    # Thin outer floor sub-base at Y=0.0 so min Y is 0.0000 and max X/Z is exact (-2..2, -2.5..2.5)
    add_part(
        sm,
        "Floor_StructuralSlab-col",
        make_beveled_box((4.0, 0.02, 5.0), center=(0.0, 0.01, 0.0), bevel=0.002),
        mats["bulkhead_structural"],
    )

    # 2. Ceiling (Y = 2.96 to 3.00)
    add_part(
        sm,
        "Ceiling_HullDeck",
        make_beveled_box((4.0, 0.04, 5.0), center=(0.0, 2.98, 0.0), bevel=0.005),
        mats["bulkhead_cream"],
    )
    # O'Neill Cylinder structural ceiling hull ribs (running along X at intervals of Z)
    rib_z_positions = [-2.2, -1.1, 0.0, 1.1, 2.2]
    rib_geoms = []
    for rz in rib_z_positions:
        rib_geoms.append(make_beveled_box((3.92, 0.10, 0.14), center=(0.0, 2.92, rz), bevel=0.02))
    add_part(sm, "Ceiling_StructuralHullRibs", merge_geometries(rib_geoms), mats["bulkhead_structural"])

    # Recessed warm ceiling light strips between hull ribs
    light_geoms = []
    for lz in [-1.65, -0.55, 0.55, 1.65]:
        light_geoms.append(make_beveled_box((2.2, 0.03, 0.18), center=(0.0, 2.95, lz), bevel=0.005))
    add_part(sm, "Ceiling_LightStrips", merge_geometries(light_geoms), mats["emissive_warm_light"])

    # 3. West Wall (X = -2.0, facing +X inside)
    # Lower wainscoting (Y: 0.0 to 1.0)
    add_part(
        sm,
        "Wall_West_Wainscoting",
        make_quad_panel((-1.98, 0.0, -2.5), (-1.98, 0.0, 2.5), (-1.98, 1.0, 2.5), (-1.98, 1.0, -2.5)),
        mats["bulkhead_wainscot"],
    )
    # Upper wallpaper (Y: 1.0 to 2.96)
    add_part(
        sm,
        "Wall_West_Wallpaper",
        make_quad_panel((-1.98, 1.0, -2.5), (-1.98, 1.0, 2.5), (-1.98, 2.96, 2.5), (-1.98, 2.96, -2.5)),
        mats["wallpaper_upper"],
    )

    # 4. East Wall (X = +2.0, facing -X inside)
    add_part(
        sm,
        "Wall_East_Wainscoting",
        make_quad_panel((1.98, 0.0, 2.5), (1.98, 0.0, -2.5), (1.98, 1.0, -2.5), (1.98, 1.0, 2.5)),
        mats["bulkhead_wainscot"],
    )
    add_part(
        sm,
        "Wall_East_Wallpaper",
        make_quad_panel((1.98, 1.0, 2.5), (1.98, 1.0, -2.5), (1.98, 2.96, -2.5), (1.98, 2.96, 2.5)),
        mats["wallpaper_upper"],
    )

    # 5. North Wall (Z = -2.5, facing +Z inside) WITH OPEN PANORAMIC VIEWPORT APERTURE
    # Window opening: X in [-1.25, +1.25], Y in [0.85, 2.35]
    # Lower wainscoting under window (Y: 0.0 to 0.85 across X: -2.0 to +2.0, plus side strips 0.85..1.0)
    north_wainscot = [
        make_quad_panel((2.0, 0.0, -2.48), (-2.0, 0.0, -2.48), (-2.0, 0.85, -2.48), (2.0, 0.85, -2.48)),
        make_quad_panel((-1.25, 0.85, -2.48), (-2.0, 0.85, -2.48), (-2.0, 1.0, -2.48), (-1.25, 1.0, -2.48)),
        make_quad_panel((2.0, 0.85, -2.48), (1.25, 0.85, -2.48), (1.25, 1.0, -2.48), (2.0, 1.0, -2.48)),
    ]
    add_part(sm, "Wall_North_Wainscoting", merge_geometries(north_wainscot), mats["bulkhead_wainscot"])

    # Upper wallpaper around window opening (left pillar, right pillar, header above Y=2.35)
    north_wallpaper = [
        # Left of window (X: -2.0 to -1.25, Y: 1.0 to 2.96)
        make_quad_panel((-1.25, 1.0, -2.48), (-2.0, 1.0, -2.48), (-2.0, 2.96, -2.48), (-1.25, 2.96, -2.48)),
        # Right of window (X: +1.25 to +2.0, Y: 1.0 to 2.96)
        make_quad_panel((2.0, 1.0, -2.48), (1.25, 1.0, -2.48), (1.25, 2.96, -2.48), (2.0, 2.96, -2.48)),
        # Header above window (X: -1.25 to +1.25, Y: 2.35 to 2.96)
        make_quad_panel((1.25, 2.35, -2.48), (-1.25, 2.35, -2.48), (-1.25, 2.96, -2.48), (1.25, 2.96, -2.48)),
    ]
    add_part(sm, "Wall_North_Wallpaper", merge_geometries(north_wallpaper), mats["wallpaper_upper"])

    # North Window Chamfered Viewport Frame & Deep Habitat Sill (leaving center open!)
    win_frame = [
        # Bottom deep sill (warm wood/brass ledge + structural frame)
        make_beveled_box((2.74, 0.09, 0.24), center=(0.0, 0.83, -2.40), bevel=0.02),
        # Top lintel beam
        make_beveled_box((2.74, 0.10, 0.20), center=(0.0, 2.38, -2.42), bevel=0.02),
        # Left jamb
        make_beveled_box((0.12, 1.62, 0.20), center=(-1.31, 1.60, -2.42), bevel=0.02),
        # Right jamb
        make_beveled_box((0.12, 1.62, 0.20), center=(1.31, 1.60, -2.42), bevel=0.02),
    ]
    add_part(sm, "Viewport_North_Frame", merge_geometries(win_frame), mats["bulkhead_structural"])

    # Brass inner viewport bezel trim & corner chamfer gussets
    win_brass = [
        make_beveled_box((2.58, 0.035, 0.14), center=(0.0, 0.88, -2.42), bevel=0.008),
        make_beveled_box((2.58, 0.035, 0.14), center=(0.0, 2.32, -2.42), bevel=0.008),
        make_beveled_box((0.035, 1.46, 0.14), center=(-1.24, 1.60, -2.42), bevel=0.008),
        make_beveled_box((0.035, 1.46, 0.14), center=(1.24, 1.60, -2.42), bevel=0.008),
    ]
    add_part(sm, "Viewport_North_BrassBezel", merge_geometries(win_brass), mats["brass_trim"])

    # 6. South Wall (Z = +2.5, facing -Z inside) WITH HABITAT DOORFRAME AT X in [-0.55, +0.55], Y in [0.0, 2.20]
    south_wainscot = [
        # Left of door (X: -2.0 to -0.55, Y: 0.0 to 1.0)
        make_quad_panel((-2.0, 0.0, 2.48), (-0.55, 0.0, 2.48), (-0.55, 1.0, 2.48), (-2.0, 1.0, 2.48)),
        # Right of door (X: +0.55 to +2.0, Y: 0.0 to 1.0)
        make_quad_panel((0.55, 0.0, 2.48), (2.0, 0.0, 2.48), (2.0, 1.0, 2.48), (0.55, 1.0, 2.48)),
    ]
    add_part(sm, "Wall_South_Wainscoting", merge_geometries(south_wainscot), mats["bulkhead_wainscot"])

    south_wallpaper = [
        # Left of door (X: -2.0 to -0.55, Y: 1.0 to 2.96)
        make_quad_panel((-2.0, 1.0, 2.48), (-0.55, 1.0, 2.48), (-0.55, 2.96, 2.48), (-2.0, 2.96, 2.48)),
        # Right of door (X: +0.55 to +2.0, Y: 1.0 to 2.96)
        make_quad_panel((0.55, 1.0, 2.48), (2.0, 1.0, 2.48), (2.0, 2.96, 2.48), (0.55, 2.96, 2.48)),
        # Header above door (X: -0.55 to +0.55, Y: 2.20 to 2.96)
        make_quad_panel((-0.55, 2.20, 2.48), (0.55, 2.20, 2.48), (0.55, 2.96, 2.48), (-0.55, 2.96, 2.48)),
    ]
    add_part(sm, "Wall_South_Wallpaper", merge_geometries(south_wallpaper), mats["wallpaper_upper"])

    # South Bulkhead Doorframe + Recessed Sliding Habitat Door Panel
    door_frame = [
        make_beveled_box((0.12, 2.26, 0.16), center=(-0.58, 1.13, 2.42), bevel=0.02),
        make_beveled_box((0.12, 2.26, 0.16), center=(0.58, 1.13, 2.42), bevel=0.02),
        make_beveled_box((1.28, 0.12, 0.16), center=(0.0, 2.22, 2.42), bevel=0.02),
    ]
    add_part(sm, "Doorframe_South_Bulkhead", merge_geometries(door_frame), mats["bulkhead_structural"])
    add_part(
        sm,
        "Door_South_SlidingPanel",
        make_beveled_box((1.06, 2.16, 0.05), center=(0.0, 1.08, 2.46), bevel=0.015),
        mats["bulkhead_cream"],
    )

    # 7. Continuous Brushed Brass Dado Rail at Y = 1.0m & Corner Columns
    dado_rails = [
        # West rail
        make_beveled_box((0.04, 0.05, 4.96), center=(-1.96, 1.00, 0.0), bevel=0.008),
        # East rail
        make_beveled_box((0.04, 0.05, 4.96), center=(1.96, 1.00, 0.0), bevel=0.008),
        # North left & right of viewport
        make_beveled_box((0.72, 0.05, 0.04), center=(-1.62, 1.00, -2.46), bevel=0.008),
        make_beveled_box((0.72, 0.05, 0.04), center=(1.62, 1.00, -2.46), bevel=0.008),
        # South left & right of doorway
        make_beveled_box((1.40, 0.05, 0.04), center=(-1.28, 1.00, 2.46), bevel=0.008),
        make_beveled_box((1.40, 0.05, 0.04), center=(1.28, 1.00, 2.46), bevel=0.008),
    ]
    add_part(sm, "Trim_BrassDadoRail", merge_geometries(dado_rails), mats["brass_trim"])

    # Corner vertical structural columns
    corner_cols = [
        make_beveled_box((0.12, 2.96, 0.12), center=(-1.94, 1.48, -2.44), bevel=0.02),
        make_beveled_box((0.12, 2.96, 0.12), center=(1.94, 1.48, -2.44), bevel=0.02),
        make_beveled_box((0.12, 2.96, 0.12), center=(-1.94, 1.48, 2.44), bevel=0.02),
        make_beveled_box((0.12, 2.96, 0.12), center=(1.94, 1.48, 2.44), bevel=0.02),
    ]
    add_part(sm, "Columns_CornerBulkheads", merge_geometries(corner_cols), mats["bulkhead_structural"])

    return export_glb(os.path.join(GLB_DIR, "room_shell.glb"), sm, root_name="RoomShell")


# ==============================================================================
# 2. BUNK BED (`bunk_bed.glb`)
# ==============================================================================
def build_bunk_bed(mats) -> Dict:
    """
    Built-in retro habitat sleep pod / bunk (~2.10m wide x 1.10m deep x 1.80m tall).
    Bottom-center pivot at (0, 0, 0).
    Includes:
    - Outer cassette-futurism sleep pod alcove shell (headboard, footboard, back wall, top privacy canopy valence).
    - Warm walnut interior acoustic paneling.
    - Lower storage drawer plinth with 3 under-bed drawers & brass recessed pulls.
    - Thick quilted cream mattress, two plush terracotta pillows, folded avocado throw blanket.
    - Warm glowing amber reading light strip + bedside telemetry control panel.
    """
    sm = []

    # Base plinth & under-bed drawer housing (2.10 x 0.42 x 1.10)
    pod_shell = [
        # Lower base frame
        make_beveled_box((2.10, 0.42, 1.10), center=(0.0, 0.21, 0.0), bevel=0.025),
        # Left headboard bulkhead wall
        make_beveled_box((0.12, 1.80, 1.10), center=(-0.99, 0.90, 0.0), bevel=0.03),
        # Right footboard bulkhead wall
        make_beveled_box((0.12, 1.80, 1.10), center=(0.99, 0.90, 0.0), bevel=0.03),
        # Back alcove wall
        make_beveled_box((1.90, 1.80, 0.10), center=(0.0, 0.90, -0.50), bevel=0.02),
        # Top privacy valence / canopy hood
        make_beveled_box((2.10, 0.24, 1.10), center=(0.0, 1.68, 0.0), bevel=0.035),
        # Front upper rounded fascia valence
        make_beveled_box((1.88, 0.18, 0.12), center=(0.0, 1.54, 0.49), bevel=0.03),
    ]
    add_part(sm, "Bunk_PodAlcoveFrame", merge_geometries(pod_shell), mats["bulkhead_cream"])

    # Warm wood interior alcove lining & drawer fronts
    wood_parts = [
        # Back acoustic wood panel inside alcove
        make_beveled_box((1.84, 1.05, 0.04), center=(0.0, 1.00, -0.43), bevel=0.01),
        # 3 under-bed storage drawer fronts
        make_beveled_box((0.58, 0.28, 0.04), center=(-0.62, 0.21, 0.55), bevel=0.012),
        make_beveled_box((0.58, 0.28, 0.04), center=(0.0, 0.21, 0.55), bevel=0.012),
        make_beveled_box((0.58, 0.28, 0.04), center=(0.62, 0.21, 0.55), bevel=0.012),
    ]
    add_part(sm, "Bunk_WoodPanelingAndDrawers", merge_geometries(wood_parts), mats["wood_walnut"])

    # Brass drawer handles & safety rail
    brass_parts = [
        make_beveled_box((0.22, 0.03, 0.03), center=(-0.62, 0.24, 0.58), bevel=0.006),
        make_beveled_box((0.22, 0.03, 0.03), center=(0.0, 0.24, 0.58), bevel=0.006),
        make_beveled_box((0.22, 0.03, 0.03), center=(0.62, 0.24, 0.58), bevel=0.006),
        # Front bunk safety rail bar
        make_cylinder(0.018, 0.018, 1.15, center=(0.25, 0.58, 0.51), segments=16, axis="x"),
        make_cylinder(0.016, 0.016, 0.16, center=(-0.30, 0.50, 0.51), segments=12, axis="y"),
        make_cylinder(0.016, 0.016, 0.16, center=(0.80, 0.50, 0.51), segments=12, axis="y"),
    ]
    add_part(sm, "Bunk_BrassHardware", merge_geometries(brass_parts), mats["brass_trim"])

    # Thick quilted mattress
    add_part(
        sm,
        "Bunk_Mattress",
        make_beveled_box((1.84, 0.18, 0.94), center=(0.0, 0.50, 0.01), bevel=0.045),
        mats["fabric_cream_quilt"],
    )

    # Two plush pillows at headboard (-X end)
    pillows = [
        make_beveled_box((0.36, 0.13, 0.40), center=(-0.70, 0.64, -0.20), bevel=0.04),
        make_beveled_box((0.36, 0.13, 0.40), center=(-0.70, 0.64, 0.24), bevel=0.04),
    ]
    add_part(sm, "Bunk_Pillows", merge_geometries(pillows), mats["fabric_terracotta"])

    # Folded throw blanket at foot of bed (+X end)
    add_part(
        sm,
        "Bunk_ThrowBlanket",
        make_beveled_box((0.68, 0.06, 0.96), center=(0.54, 0.59, 0.01), bevel=0.02),
        mats["fabric_avocado_blanket"],
    )

    # Emissive warm reading light panel at headboard + overhead alcove strip
    lights = [
        make_beveled_box((0.04, 0.24, 0.52), center=(-0.91, 0.98, 0.0), bevel=0.008),
        make_beveled_box((1.40, 0.03, 0.12), center=(0.0, 1.55, -0.32), bevel=0.006),
    ]
    add_part(sm, "Bunk_ReadingLightPanel", merge_geometries(lights), mats["emissive_warm_light"])

    return export_glb(os.path.join(GLB_DIR, "bunk_bed.glb"), sm, root_name="BunkBed")


# ==============================================================================
# 3. RETRO DESK + CRT (`retro_desk_crt.glb`)
# ==============================================================================
def build_retro_desk_crt(mats) -> Dict:
    """
    Cantilevered habitat work desk (~1.40m wide x 0.75m deep x 0.75m desk surface, total height ~1.22m):
    - Tubular sled/cantilever legs in brushed steel + brass feet.
    - Warm walnut laminate desktop with beveled cassette-futurism edge & side drawer module.
    - Chunky 1970s CRT terminal monitor (ochre/amber casing, charcoal bezel, glowing phosphor telemetry screen).
    - Mechanical wedge keyboard with sculpted keycap rows.
    - Dual cassette data-tape drive + stacked data cartridges & ceramic habitat mug.
    """
    sm = []

    # 1. Tubular Cantilever Frame & Legs (Y: 0.0 to 0.72)
    legs = [
        # Left sled base runner, front vertical post, top support bar
        make_beveled_box((0.05, 0.04, 0.70), center=(-0.64, 0.02, 0.0), bevel=0.01),
        make_beveled_box((0.05, 0.70, 0.05), center=(-0.64, 0.37, -0.30), bevel=0.01),
        make_beveled_box((0.05, 0.70, 0.05), center=(-0.64, 0.37, 0.26), bevel=0.01),
        # Right sled base runner & vertical posts
        make_beveled_box((0.05, 0.04, 0.70), center=(0.64, 0.02, 0.0), bevel=0.01),
        make_beveled_box((0.05, 0.70, 0.05), center=(0.64, 0.37, -0.30), bevel=0.01),
        make_beveled_box((0.05, 0.70, 0.05), center=(0.64, 0.37, 0.26), bevel=0.01),
        # Rear crossbeam stretcher
        make_beveled_box((1.28, 0.05, 0.04), center=(0.0, 0.28, -0.30), bevel=0.008),
    ]
    add_part(sm, "Desk_CantileverLegs", merge_geometries(legs), mats["chrome_steel"])

    # 2. Desktop Surface & Under-Desk Pedestal Drawer (Y: 0.71 to 0.76)
    wood_desk = [
        make_beveled_box((1.40, 0.05, 0.75), center=(0.0, 0.735, 0.0), bevel=0.015),
        # Right-side suspended drawer pedestal
        make_beveled_box((0.40, 0.26, 0.62), center=(0.42, 0.58, -0.02), bevel=0.015),
    ]
    add_part(sm, "Desk_WoodTopAndPedestal", merge_geometries(wood_desk), mats["wood_walnut"])

    # Raised rear instrument shelf / cable raceway
    add_part(
        sm,
        "Desk_RearConsoleRiser",
        make_beveled_box((1.36, 0.10, 0.26), center=(0.0, 0.81, -0.23), bevel=0.015),
        mats["bulkhead_cream"],
    )

    # 3. Chunky 1970s Cassette-Futurism CRT Terminal (centered slightly left at X = -0.18)
    crt_casing = [
        # Swivel pedestal base
        make_cylinder(0.16, 0.13, 0.05, center=(-0.18, 0.885, -0.20), segments=20, axis="y"),
        # Main CRT outer cowling (0.46 x 0.36 x 0.36)
        make_beveled_box((0.46, 0.35, 0.34), center=(-0.18, 1.06, -0.18), bevel=0.035),
        # Rear CRT electron-gun tube housing
        make_beveled_box((0.32, 0.24, 0.14), center=(-0.18, 1.06, -0.36), bevel=0.025),
        # Dual cassette data-tape deck on right side (X = +0.36)
        make_beveled_box((0.34, 0.14, 0.26), center=(0.36, 0.92, -0.20), bevel=0.02),
    ]
    add_part(sm, "CRT_OchreCasingAndTapeDeck", merge_geometries(crt_casing), mats["crt_casing_ochre"])

    # Charcoal recessed bezel & keyboard wedge base + tape slots
    dark_parts = [
        # CRT dark glass surround bezel
        make_beveled_box((0.40, 0.29, 0.03), center=(-0.18, 1.06, -0.005), bevel=0.015),
        # Mechanical keyboard wedge body in front of CRT
        make_beveled_box((0.44, 0.045, 0.18), center=(-0.18, 0.78, 0.16), bevel=0.01),
        # Cassette tape deck dark slots
        make_beveled_box((0.12, 0.06, 0.02), center=(0.28, 0.93, -0.07), bevel=0.004),
        make_beveled_box((0.12, 0.06, 0.02), center=(0.44, 0.93, -0.07), bevel=0.004),
    ]
    add_part(sm, "CRT_BezelAndKeyboardBase", merge_geometries(dark_parts), mats["crt_bezel_dark"])

    # Glowing Phosphor CRT Screen Quad (facing +Z towards user)
    add_part(
        sm,
        "CRT_PhosphorScreen",
        make_quad_panel(
            (-0.35, 0.94, 0.012),
            (-0.01, 0.94, 0.012),
            (-0.01, 1.18, 0.012),
            (-0.35, 1.18, 0.012),
        ),
        mats["crt_screen_glow"],
    )

    # Sculpted retro keycap blocks + stacked data cartridges + coffee mug
    accents = [
        # Keycap bank (cream keys)
        make_beveled_box((0.38, 0.02, 0.12), center=(-0.18, 0.808, 0.16), bevel=0.005),
        # Stacked cassette cartridges on right side of desk
        make_beveled_box((0.11, 0.022, 0.075), center=(0.50, 0.771, 0.14), bevel=0.004),
        make_beveled_box((0.11, 0.022, 0.075), center=(0.51, 0.795, 0.13), bevel=0.004),
        make_beveled_box((0.11, 0.022, 0.075), center=(0.49, 0.819, 0.145), bevel=0.004),
        # Cozy ceramic coffee mug
        make_cylinder(0.042, 0.045, 0.095, center=(-0.54, 0.808, 0.14), segments=18, axis="y"),
    ]
    add_part(sm, "Desk_KeycapsTapesAndMug", merge_geometries(accents), mats["fabric_terracotta"])

    return export_glb(os.path.join(GLB_DIR, "retro_desk_crt.glb"), sm, root_name="RetroDeskCRT")


# ==============================================================================
# 4. WARDROBE LOCKER (`wardrobe_locker.glb`)
# ==============================================================================
def build_wardrobe_locker(mats) -> Dict:
    """
    Curved-edge modular crew wardrobe / storage locker (~1.00m wide x 0.60m deep x 2.00m tall):
    - Heavy chamfered aerospace polymer shell.
    - Dual upper wardrobe doors with recessed louver vent grilles.
    - Lower heavy-duty boot drawer.
    - Warm ochre/mustard crew division stripe & brushed brass vertical grab handles.
    """
    sm = []

    # Main chamfered locker body (1.00 x 1.94 x 0.56 on a 0.06m recessed toe kick)
    shell = [
        # Recessed dark plinth/toe kick (ensures Y=0.0 bottom pivot)
        make_beveled_box((0.94, 0.08, 0.54), center=(0.0, 0.04, 0.0), bevel=0.01),
        # Main cabinet hull (Y: 0.08 to 2.00)
        make_beveled_box((1.00, 1.92, 0.58), center=(0.0, 1.04, -0.01), bevel=0.045),
    ]
    add_part(sm, "Wardrobe_CabinetHull", merge_geometries(shell), mats["bulkhead_cream"])

    # Dual upper locker doors & lower boot drawer front
    doors = [
        # Left upper door
        make_beveled_box((0.44, 1.38, 0.04), center=(-0.23, 1.24, 0.28), bevel=0.015),
        # Right upper door
        make_beveled_box((0.44, 1.38, 0.04), center=(0.23, 1.24, 0.28), bevel=0.015),
        # Lower boot drawer front
        make_beveled_box((0.90, 0.36, 0.04), center=(0.0, 0.32, 0.28), bevel=0.015),
    ]
    add_part(sm, "Wardrobe_DoorsAndBootDrawer", merge_geometries(doors), mats["wood_walnut"])

    # Ochre cassette-futurism identification stripe across upper doors
    stripes = [
        make_beveled_box((0.42, 0.11, 0.015), center=(-0.23, 1.56, 0.302), bevel=0.004),
        make_beveled_box((0.42, 0.11, 0.015), center=(0.23, 1.56, 0.302), bevel=0.004),
    ]
    add_part(sm, "Wardrobe_CrewStatusStripe", merge_geometries(stripes), mats["crt_casing_ochre"])

    # Louver vents & recessed handle wells
    vents = []
    for side_x in (-0.23, 0.23):
        for i in range(5):
            vy = 1.70 + i * 0.032
            vents.append(make_beveled_box((0.26, 0.014, 0.015), center=(side_x, vy, 0.302), bevel=0.002))
        for i in range(4):
            vy = 0.72 + i * 0.032
            vents.append(make_beveled_box((0.26, 0.014, 0.015), center=(side_x, vy, 0.302), bevel=0.002))
    add_part(sm, "Wardrobe_LouverVents", merge_geometries(vents), mats["bulkhead_structural"])

    # Brushed brass vertical grab handles & boot drawer pull
    handles = [
        make_beveled_box((0.028, 0.28, 0.035), center=(-0.06, 1.18, 0.31), bevel=0.006),
        make_beveled_box((0.028, 0.28, 0.035), center=(0.06, 1.18, 0.31), bevel=0.006),
        make_beveled_box((0.32, 0.028, 0.035), center=(0.0, 0.36, 0.31), bevel=0.006),
    ]
    add_part(sm, "Wardrobe_BrassHandles", merge_geometries(handles), mats["brass_trim"])

    return export_glb(os.path.join(GLB_DIR, "wardrobe_locker.glb"), sm, root_name="WardrobeLocker")


# ==============================================================================
# 5. LOUNGE CHAIR (`lounge_chair.glb`)
# ==============================================================================
def build_lounge_chair(mats) -> Dict:
    """
    Low-profile 1970s sci-fi modular lounge armchair (~0.86m wide x 0.85m deep x 0.78m tall):
    - Brushed brass / steel 4-star swivel or sled base.
    - Molded bent-walnut / cream fiberglass cradle shell.
    - Plush tufted terracotta seat, backrest, and bolster armrests.
    """
    sm = []

    # 1. Brushed Brass Sled / Cantilever Base (Y: 0.0 to 0.22)
    base_parts = [
        # Left & right floor skids
        make_beveled_box((0.045, 0.03, 0.74), center=(-0.35, 0.015, 0.0), bevel=0.008),
        make_beveled_box((0.045, 0.03, 0.74), center=(0.35, 0.015, 0.0), bevel=0.008),
        # Angled risers
        make_beveled_box((0.045, 0.22, 0.05), center=(-0.35, 0.12, 0.24), bevel=0.008),
        make_beveled_box((0.045, 0.22, 0.05), center=(0.35, 0.12, 0.24), bevel=0.008),
        make_beveled_box((0.045, 0.20, 0.05), center=(-0.35, 0.11, -0.24), bevel=0.008),
        make_beveled_box((0.045, 0.20, 0.05), center=(0.35, 0.11, -0.24), bevel=0.008),
        # Crossbars
        make_beveled_box((0.74, 0.04, 0.05), center=(0.0, 0.20, 0.24), bevel=0.008),
        make_beveled_box((0.74, 0.04, 0.05), center=(0.0, 0.19, -0.24), bevel=0.008),
    ]
    add_part(sm, "Chair_BrassFrameBase", merge_geometries(base_parts), mats["brass_trim"])

    # 2. Molded Bent-Wood / Fiberglass Outer Shell
    shell_parts = [
        # Under-seat cradle pan
        make_beveled_box((0.84, 0.08, 0.78), center=(0.0, 0.24, 0.02), bevel=0.03),
        # Curved outer back shell
        make_beveled_box((0.84, 0.52, 0.10), center=(0.0, 0.52, -0.35), bevel=0.035),
        # Left & right sculpted wing sides
        make_beveled_box((0.09, 0.36, 0.76), center=(-0.40, 0.42, 0.01), bevel=0.03),
        make_beveled_box((0.09, 0.36, 0.76), center=(0.40, 0.42, 0.01), bevel=0.03),
    ]
    add_part(sm, "Chair_MoldedWoodShell", merge_geometries(shell_parts), mats["wood_walnut"])

    # 3. Plush Tufted Terracotta Cushions (2-tier segmented seat + 2-tier backrest + arm bolsters)
    cushions = [
        # Seat cushion rear & front bolsters
        make_beveled_box((0.70, 0.14, 0.36), center=(0.0, 0.34, -0.09), bevel=0.045),
        make_beveled_box((0.70, 0.14, 0.36), center=(0.0, 0.35, 0.25), bevel=0.045),
        # Lower lumbar cushion & upper headrest cushion
        make_beveled_box((0.70, 0.22, 0.16), center=(0.0, 0.50, -0.23), bevel=0.045),
        make_beveled_box((0.70, 0.22, 0.15), center=(0.0, 0.69, -0.25), bevel=0.045),
        # Inner arm pad bolsters
        make_beveled_box((0.10, 0.14, 0.58), center=(-0.32, 0.48, 0.04), bevel=0.035),
        make_beveled_box((0.10, 0.14, 0.58), center=(0.32, 0.48, 0.04), bevel=0.035),
    ]
    add_part(sm, "Chair_TuftedTerracottaCushions", merge_geometries(cushions), mats["fabric_terracotta"])

    return export_glb(os.path.join(GLB_DIR, "lounge_chair.glb"), sm, root_name="LoungeChair")


# ==============================================================================
# 6. COFFEE TABLE (`coffee_table.glb`)
# ==============================================================================
def build_coffee_table(mats) -> Dict:
    """
    Low-profile retro habitat coffee table (~1.10m wide x 0.65m deep x 0.42m tall):
    - Warm walnut base frame and lower slatted magazine shelf.
    - Smoked amber acrylic inset tabletop with chamfered cream/brass rim.
    - Decorative brass serving tray, space-age carafe, and cassette-futurism art book.
    """
    sm = []

    # 1. Sculpted Wood Legs & Lower Shelf (Y: 0.0 to 0.36)
    wood_parts = [
        # 4 angled pillar legs
        make_beveled_box((0.07, 0.37, 0.07), center=(-0.44, 0.185, -0.22), bevel=0.015),
        make_beveled_box((0.07, 0.37, 0.07), center=(0.44, 0.185, -0.22), bevel=0.015),
        make_beveled_box((0.07, 0.37, 0.07), center=(-0.44, 0.185, 0.22), bevel=0.015),
        make_beveled_box((0.07, 0.37, 0.07), center=(0.44, 0.185, 0.22), bevel=0.015),
        # Lower magazine shelf
        make_beveled_box((0.92, 0.03, 0.48), center=(0.0, 0.14, 0.0), bevel=0.01),
        # Outer tabletop surround frame
        make_beveled_box((1.10, 0.05, 0.65), center=(0.0, 0.38, 0.0), bevel=0.022),
    ]
    add_part(sm, "Table_WalnutFrameAndShelf", merge_geometries(wood_parts), mats["wood_walnut"])

    # 2. Smoked Amber Acrylic Inset Top
    add_part(
        sm,
        "Table_SmokedAmberTop",
        make_beveled_box((0.98, 0.025, 0.53), center=(0.0, 0.402, 0.0), bevel=0.008),
        mats["smoked_amber_acrylic"],
    )

    # 3. Tabletop Props: Brass Tray + Carafe + Hardcover Habitat Manual
    brass_props = [
        # Circular brass tray
        make_cylinder(0.16, 0.17, 0.022, center=(0.22, 0.422, 0.02), segments=24, axis="y"),
        # Space-age hourglass carafe
        make_lathe_dome(
            [(0.0, 0.0), (0.055, 0.0), (0.062, 0.04), (0.032, 0.10), (0.042, 0.14), (0.0, 0.14)],
            center=(0.18, 0.43, 0.0),
            segments=20,
        ),
        # Two small espresso tumblers
        make_cylinder(0.026, 0.030, 0.055, center=(0.28, 0.455, 0.06), segments=16, axis="y"),
    ]
    add_part(sm, "Table_BrassTrayAndCarafe", merge_geometries(brass_props), mats["brass_trim"])

    books = [
        make_beveled_box((0.24, 0.028, 0.18), center=(-0.24, 0.426, -0.02), bevel=0.005),
        make_beveled_box((0.20, 0.022, 0.15), center=(-0.23, 0.450, -0.01), bevel=0.004),
    ]
    add_part(sm, "Table_HabitatJournals", merge_geometries(books), mats["fabric_terracotta"])

    return export_glb(os.path.join(GLB_DIR, "coffee_table.glb"), sm, root_name="CoffeeTable")


# ==============================================================================
# 7. FLOOR LAMP (`floor_lamp.glb`)
# ==============================================================================
def build_floor_lamp(mats) -> Dict:
    """
    Cozy 1970s space-age multi-tier mushroom floor lamp (~0.46m diameter x 1.56m tall):
    - Weighted stepped brushed-brass cylindrical base (Y=0.0).
    - Slender brass stem with warm walnut mid-column grip accent.
    - Iconic layered Guzzini/Panthella mushroom dome shade with warm glowing emissive core.
    """
    sm = []

    # 1. Weighted Brass Base & Stem + Finial
    brass_parts = [
        # Stepped circular base at Y=0.0
        make_cylinder(0.19, 0.17, 0.045, center=(0.0, 0.0225, 0.0), segments=28, axis="y"),
        make_cylinder(0.11, 0.06, 0.04, center=(0.0, 0.065, 0.0), segments=24, axis="y"),
        # Slender vertical stem
        make_cylinder(0.018, 0.018, 1.34, center=(0.0, 0.74, 0.0), segments=20, axis="y"),
        # Top brass finial cap at Y=1.56
        make_cylinder(0.045, 0.02, 0.04, center=(0.0, 1.54, 0.0), segments=20, axis="y"),
    ]
    add_part(sm, "Lamp_BrassBaseAndStem", merge_geometries(brass_parts), mats["brass_trim"])

    # 2. Warm Wood Mid-Stem Collar
    add_part(
        sm,
        "Lamp_WoodStemAccent",
        make_cylinder(0.032, 0.032, 0.28, center=(0.0, 0.52, 0.0), segments=20, axis="y"),
        mats["wood_walnut"],
    )

    # 3. Layered Space-Age Mushroom Dome Shade (revolved smooth profile, diameter 0.46m)
    dome_profile = [
        (0.14, 1.24),
        (0.22, 1.26),
        (0.23, 1.32),
        (0.21, 1.39),
        (0.16, 1.46),
        (0.09, 1.51),
        (0.02, 1.53),
    ]
    add_part(
        sm,
        "Lamp_MushroomDomeShade",
        make_lathe_dome(dome_profile, center=(0.0, 0.0, 0.0), segments=32),
        mats["emissive_lamp_shade"],
    )

    # 4. Inner High-Glow Bulb Diffuser Column
    add_part(
        sm,
        "Lamp_InnerGlowCore",
        make_cylinder(0.075, 0.075, 0.18, center=(0.0, 1.34, 0.0), segments=20, axis="y"),
        mats["emissive_warm_light"],
    )

    return export_glb(os.path.join(GLB_DIR, "floor_lamp.glb"), sm, root_name="FloorLamp")


# ==============================================================================
# 8. AREA RUG (`area_rug.glb`)
# ==============================================================================
def build_area_rug(mats) -> Dict:
    """
    Cozy woven geometric retro area rug (~2.40m wide x 1.80m deep x 0.016m thick):
    - Beveled anti-slip perimeter backing & woven fringe border.
    - Clean planar UV0 top face mapped 1:1 to `rug_retro_woven.png`.
    """
    sm = []

    # Thin beveled rug pad & border (2.40 x 0.014 x 1.80)
    border = [
        make_beveled_box((2.40, 0.014, 1.80), center=(0.0, 0.007, 0.0), bevel=0.005),
        # Fringe end trims at X = -1.21 and X = +1.21
        make_beveled_box((0.03, 0.008, 1.76), center=(-1.205, 0.004, 0.0), bevel=0.002),
        make_beveled_box((0.03, 0.008, 1.76), center=(1.205, 0.004, 0.0), bevel=0.002),
    ]
    add_part(sm, "Rug_BorderAndFringe", merge_geometries(border), mats["fabric_cream_quilt"])

    # Top woven patterned surface quad at Y = 0.015m with full [0,1] UV0
    add_part(
        sm,
        "Rug_WovenPatternTop",
        make_quad_panel((-1.18, 0.015, 0.88), (1.18, 0.015, 0.88), (1.18, 0.015, -0.88), (-1.18, 0.015, -0.88)),
        mats["rug_woven"],
    )

    return export_glb(os.path.join(GLB_DIR, "area_rug.glb"), sm, root_name="AreaRug")


# ==============================================================================
# 9. HYDRO PLANTER (`hydro_planter.glb`)
# ==============================================================================
def build_hydro_planter(mats) -> Dict:
    """
    Hydroponic habitat greenery planter unit (~0.82m wide x 0.40m deep x 1.12m tall):
    - Modular aerospace cream trough with chamfered ribs & ochre accent badge.
    - Illuminated cyan nutrient-water sight glass gauge on front face.
    - Brushed chrome overhead grow-light gantry arch + warm emissive grow-light bar.
    - Expanded clay substrate bed + lush 3D multi-layered botanical foliage (monstera/fern leaves).
    """
    sm = []

    # 1. Modular Hydroponic Trough Cabinet (Y: 0.0 to 0.48)
    trough = [
        # Recessed base plinth
        make_beveled_box((0.76, 0.06, 0.36), center=(0.0, 0.03, 0.0), bevel=0.01),
        # Main planter trough hull
        make_beveled_box((0.82, 0.42, 0.40), center=(0.0, 0.27, 0.0), bevel=0.025),
    ]
    add_part(sm, "Hydro_TroughCabinet", merge_geometries(trough), mats["bulkhead_cream"])

    # Ochre front control panel & sight-glass housing
    add_part(
        sm,
        "Hydro_ControlBadge",
        make_beveled_box((0.52, 0.14, 0.02), center=(-0.08, 0.26, 0.202), bevel=0.005),
        mats["crt_casing_ochre"],
    )

    # Illuminated cyan water-level sight glass strip
    add_part(
        sm,
        "Hydro_WaterSightGlass",
        make_beveled_box((0.045, 0.26, 0.022), center=(0.28, 0.27, 0.202), bevel=0.004),
        mats["water_sight_cyan"],
    )

    # 2. Expanded Clay Hydroponic Substrate Bed
    add_part(
        sm,
        "Hydro_ClaySubstrate",
        make_beveled_box((0.74, 0.04, 0.32), center=(0.0, 0.47, 0.0), bevel=0.01),
        mats["hydro_soil_substrate"],
    )

    # 3. Overhead Grow-Light Gantry Frame & Emissive Bar (up to Y = 1.12m)
    gantry = [
        make_cylinder(0.018, 0.018, 0.64, center=(-0.35, 0.78, 0.0), segments=16, axis="y"),
        make_cylinder(0.018, 0.018, 0.64, center=(0.35, 0.78, 0.0), segments=16, axis="y"),
        make_beveled_box((0.76, 0.045, 0.12), center=(0.0, 1.10, 0.0), bevel=0.01),
    ]
    add_part(sm, "Hydro_GrowGantryFrame", merge_geometries(gantry), mats["chrome_steel"])

    add_part(
        sm,
        "Hydro_GrowLightEmitter",
        make_beveled_box((0.66, 0.02, 0.08), center=(0.0, 1.072, 0.0), bevel=0.004),
        mats["emissive_grow_light"],
    )

    # 4. Lush 3D Botanical Foliage (Cluster of sculpted leaf blades & stems in 2 greens)
    deep_leaves = []
    bright_leaves = []

    leaf_specs = [
        # (cx, cy, cz, sx, sy, sz, is_bright)
        (-0.22, 0.62, 0.04, 0.22, 0.24, 0.18, False),
        (0.0, 0.68, -0.03, 0.26, 0.30, 0.22, False),
        (0.22, 0.60, 0.05, 0.22, 0.22, 0.18, False),
        (-0.14, 0.76, -0.06, 0.20, 0.22, 0.16, True),
        (0.14, 0.74, 0.06, 0.20, 0.24, 0.16, True),
        (-0.26, 0.55, -0.08, 0.18, 0.16, 0.16, True),
        (0.26, 0.56, -0.06, 0.18, 0.18, 0.15, True),
        (0.02, 0.82, 0.02, 0.22, 0.18, 0.20, True),
    ]
    for cx, cy, cz, sx, sy, sz, is_b in leaf_specs:
        geom = make_beveled_box((sx, sy, sz), center=(cx, cy, cz), bevel=min(sx, sy, sz) * 0.34)
        if is_b:
            bright_leaves.append(geom)
        else:
            deep_leaves.append(geom)

    add_part(sm, "Hydro_FoliageMonstera", merge_geometries(deep_leaves), mats["foliage_deep_green"])
    add_part(sm, "Hydro_FoliageFern", merge_geometries(bright_leaves), mats["foliage_bright_fern"])

    return export_glb(os.path.join(GLB_DIR, "hydro_planter.glb"), sm, root_name="HydroPlanter")


def build_all():
    generate_textures.generate_all(force=False)
    mats = get_materials()
    builders = [
        build_room_shell,
        build_bunk_bed,
        build_retro_desk_crt,
        build_wardrobe_locker,
        build_lounge_chair,
        build_coffee_table,
        build_floor_lamp,
        build_area_rug,
        build_hydro_planter,
    ]
    manifest_data = []
    for fn in builders:
        info = fn(mats)
        fname = os.path.basename(info["filepath"])
        dims = info["dimensions"]
        print(
            f"[glb] Built {fname:22s} | {dims[0]:.2f}m x {dims[2]:.2f}m x {dims[1]:.2f}m | "
            f"verts={info['vertices']:4d} | tris={info['triangles']:4d} | min_y={info['min'][1]:.5f}"
        )
        manifest_data.append(info)

    summary_path = "/workspace/game-project/assets/src/manifest_summary.json"
    with open(summary_path, "w") as f:
        json.dump(manifest_data, f, indent=2)
    return manifest_data


if __name__ == "__main__":
    build_all()
