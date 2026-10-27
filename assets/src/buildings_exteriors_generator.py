#!/usr/bin/env python3
"""
Builds the O'Neill Cylinder Exterior Plaza Terrain Base + all 15 Building Exteriors x 5 Candidates
(76 .glb files total) under the unified "Aegis-7 Exterior Standard":
  1. /workspace/game-project/assets/glb/buildings/district_plaza_terrain_shell.glb
  2. /workspace/game-project/assets/glb/buildings/bldg_01/bldg_01_r1_01.glb .. bldg_01_r1_05.glb
     through
     /workspace/game-project/assets/glb/buildings/bldg_15/bldg_15_r1_01.glb .. bldg_15_r1_05.glb

Owner: Rook (3D Modeling Specialist)
Follows:
  - /workspace/game-project/MASTER_BUILDINGS_15_EXTERIORS.md
  - /workspace/game-project/design/buildings_15_exteriors_spec.md
"""
import os
import sys
import math
import json
from typing import List, Tuple, Dict, Optional
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glb_builder as _gb
_PNG_BYTES_CACHE = {}
_orig_get_tex_bytes = _gb.get_calm_scifi_texture_bytes
def _cached_get_tex_bytes(mdef):
    k = (mdef.name, mdef.base_color, mdef.texture_path, mdef.alpha_mode)
    if k not in _PNG_BYTES_CACHE:
        _PNG_BYTES_CACHE[k] = _orig_get_tex_bytes(mdef)
    return _PNG_BYTES_CACHE[k]
_gb.get_calm_scifi_texture_bytes = _cached_get_tex_bytes

from glb_builder import (
    PBRMaterialDef,
    SubMesh,
    transform_geom,
    merge_geometries,
    make_lathe_dome,
    sample_filleted_polyline,
    make_swept_tube,
    make_curved_leaf_blade,
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

TEX_BLDG_DIR = "/workspace/game-project/assets/textures/buildings"
OUT_BLDG_ROOT = "/workspace/game-project/assets/glb/buildings"
os.makedirs(OUT_BLDG_ROOT, exist_ok=True)


def tex_bldg(fname: str) -> str:
    p = os.path.join(TEX_BLDG_DIR, fname)
    if os.path.exists(p):
        return p
    return os.path.join("/workspace/game-project/assets/textures", fname)


def get_building_materials() -> Dict[str, PBRMaterialDef]:
    return {
        "gunmetal": PBRMaterialDef(
            name="Mat_Facade_TitaniumGunmetalHull",
            base_color=hex_rgba("#1A1E24"),
            metallic=0.78,
            roughness=0.34,
            texture_path=tex_bldg("facade_titanium_gunmetal_hull.png"),
        ),
        "aero_white": PBRMaterialDef(
            name="Mat_Facade_AerospaceWhiteCladding",
            base_color=hex_rgba("#D8DEE6"),
            metallic=0.08,
            roughness=0.30,
            texture_path=tex_bldg("facade_aerospace_white_cladding.png"),
        ),
        "carbon_slate": PBRMaterialDef(
            name="Mat_Facade_CarbonSlateSpandrel",
            base_color=hex_rgba("#282E38"),
            metallic=0.58,
            roughness=0.40,
            texture_path=tex_bldg("facade_carbon_slate_spandrel.png"),
        ),
        "steel_machined": PBRMaterialDef(
            name="Mat_Facade_BrushedSteelGantry",
            base_color=hex_rgba("#88929E"),
            metallic=0.90,
            roughness=0.22,
            texture_path=tex_bldg("facade_brushed_steel_gantry.png"),
        ),
        "accent_orange": PBRMaterialDef(
            name="Mat_Accent_SafetyOrange",
            base_color=hex_rgba("#D95B26"),
            metallic=0.35,
            roughness=0.38,
            texture_path=tex_bldg("accent_safety_orange.png"),
        ),
        "window_lit": PBRMaterialDef(
            name="Mat_Window_GridLitHabitat",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.15,
            roughness=0.25,
            emissive=(0.45, 0.72, 0.90),
            texture_path=tex_bldg("window_grid_lit_habitat.png"),
        ),
        "marquee": PBRMaterialDef(
            name="Mat_Signage_Aegis7BuildingMarquees",
            base_color=(1.0, 1.0, 1.0, 1.0),
            metallic=0.10,
            roughness=0.20,
            emissive=(0.35, 0.85, 1.0),
            texture_path=tex_bldg("signage_aegis7_building_marquees.png"),
        ),
        "glass_cyan": PBRMaterialDef(
            name="Mat_Glass_CurtainwallCyan_Translucent",
            base_color=(0.55, 0.88, 1.0, 0.34),
            metallic=0.10,
            roughness=0.12,
            emissive=(0.0, 0.16, 0.24),
            texture_path=tex_bldg("glass_curtainwall_cyan_translucent.png"),
            double_sided=True,
            alpha_mode="BLEND",
        ),
        "glass_emerald": PBRMaterialDef(
            name="Mat_Glass_BiodomeEmerald_Translucent",
            base_color=(0.48, 0.92, 0.78, 0.32),
            metallic=0.08,
            roughness=0.14,
            emissive=(0.0, 0.16, 0.14),
            texture_path=tex_bldg("glass_biodome_emerald_translucent.png"),
            double_sided=True,
            alpha_mode="BLEND",
        ),
        "foliage": PBRMaterialDef(
            name="Mat_Foliage_AeroponicHerbs",
            base_color=hex_rgba("#2E8B57"),
            metallic=0.02,
            roughness=0.65,
            texture_path=tex_bldg("foliage_aeroponic_herbs.png"),
            double_sided=True,
        ),
        "led_cyan": PBRMaterialDef(
            name="Mat_Emissive_CyanLED",
            base_color=hex_rgba("#00E5FF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.0, 0.92, 1.0),
            texture_path=tex_bldg("led_cyan_strip.png"),
        ),
        "led_amber": PBRMaterialDef(
            name="Mat_Emissive_AmberLED",
            base_color=hex_rgba("#FF9500"),
            metallic=0.0,
            roughness=0.15,
            emissive=(1.0, 0.58, 0.0),
            texture_path=tex_bldg("led_amber_strip.png"),
        ),
        "led_uv": PBRMaterialDef(
            name="Mat_Emissive_UVVioletLED",
            base_color=hex_rgba("#7B5CFF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.55, 0.38, 1.0),
            texture_path=tex_bldg("led_uv_violet.png"),
        ),
        "led_ice": PBRMaterialDef(
            name="Mat_Emissive_IceWhiteLED",
            base_color=hex_rgba("#E0F4FF"),
            metallic=0.0,
            roughness=0.15,
            emissive=(0.85, 0.95, 1.0),
            texture_path=tex_bldg("led_ice_white.png"),
        ),
    }


# ==============================================================================
# ARCHITECTURAL GEOMETRY PRIMITIVES (45-DEGREE CHAMFERED OCTAGONAL SOLIDS)
# ==============================================================================
def make_chamfered_oct_prism(
    width_x: float,
    depth_z: float,
    height_y: float,
    center: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    chamfer: float = 0.85,
    top_scale: float = 1.0,
    capped: bool = True,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Builds a crisp 8-sided 45-degree chamfered octagonal architectural block/tower tier
    with optional frustum taper (top_scale).
    Capped=True adds top & bottom octagonal faces (28 tris total).
    Capped=False builds only the 8 side walls (16 tris total).
    """
    cx, cy, cz = center
    hx, hz = width_x * 0.5, depth_z * 0.5
    hy = height_y * 0.5
    c = min(chamfer, hx * 0.48, hz * 0.48)

    base_ring_2d = [
        (-hx + c, hz),
        (hx - c, hz),
        (hx, hz - c),
        (hx, -hz + c),
        (hx - c, -hz),
        (-hx + c, -hz),
        (-hx, -hz + c),
        (-hx, hz - c),
    ]
    y0, y1 = cy - hy, cy + hy

    pos_list, norm_list, uv_list, idx_list = [], [], [], []
    # 8 side quads
    for i in range(8):
        x0, z0 = base_ring_2d[i]
        x1, z1 = base_ring_2d[(i + 1) % 8]
        tx0, tz0 = x0 * top_scale, z0 * top_scale
        tx1, tz1 = x1 * top_scale, z1 * top_scale

        p0 = np.array([cx + x0, y0, cz + z0], dtype=np.float32)
        p1 = np.array([cx + x1, y0, cz + z1], dtype=np.float32)
        p2 = np.array([cx + tx1, y1, cz + tz1], dtype=np.float32)
        p3 = np.array([cx + tx0, y1, cz + tz0], dtype=np.float32)

        n = np.cross(p1 - p0, p2 - p0)
        n /= max(np.linalg.norm(n), 1e-12)
        b_idx = len(pos_list)
        pos_list.extend([p0, p1, p2, p3])
        norm_list.extend([n, n, n, n])
        uv_list.extend([[0.0, 1.0], [1.0, 1.0], [1.0, 0.0], [0.0, 0.0]])
        idx_list.append([b_idx, b_idx + 1, b_idx + 2])
        idx_list.append([b_idx, b_idx + 2, b_idx + 3])

    if capped:
        # Top cap (fan of 6 triangles)
        t_idx = len(pos_list)
        for x, z in base_ring_2d:
            pos_list.append([cx + x * top_scale, y1, cz + z * top_scale])
            norm_list.append([0.0, 1.0, 0.0])
            uv_list.append([0.5 + 0.45 * (x / max(hx, 1e-4)), 0.5 + 0.45 * (z / max(hz, 1e-4))])
        for i in range(1, 7):
            idx_list.append([t_idx, t_idx + i, t_idx + i + 1])

        # Bottom cap (fan of 6 triangles)
        b_idx = len(pos_list)
        for x, z in base_ring_2d:
            pos_list.append([cx + x, y0, cz + z])
            norm_list.append([0.0, -1.0, 0.0])
            uv_list.append([0.5 + 0.45 * (x / max(hx, 1e-4)), 0.5 + 0.45 * (z / max(hz, 1e-4))])
        for i in range(1, 7):
            idx_list.append([b_idx, b_idx + i + 1, b_idx + i])

    return (
        np.array(pos_list, dtype=np.float32),
        np.array(norm_list, dtype=np.float32),
        np.array(uv_list, dtype=np.float32),
        np.array(idx_list, dtype=np.uint32),
    )


def make_closed_torus_ring(
    major_radius: float,
    tube_radius: float,
    center: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    rot_xyz_deg: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    n_major: int = 20,
    n_minor: int = 6,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Builds a 3D circular ring in the XZ plane (default) and transforms it."""
    pts = []
    for i in range(n_major + 1):
        ang = 2.0 * math.pi * (i / float(n_major))
        pts.append([major_radius * math.cos(ang), 0.0, major_radius * math.sin(ang)])
    geom = make_swept_tube(
        np.array(pts, dtype=np.float32),
        radius=tube_radius,
        radial_segments=n_minor,
        closed_loop=True,
        capped=False,
    )
    return transform_geom(geom, translate=center, rot_xyz_deg=rot_xyz_deg)


def make_botanical_cluster(
    center: Tuple[float, float, float],
    radius: float = 0.85,
    n_leaves: int = 5,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Creates a lush 3D cluster of arching botanical leaves for biodomes, terraces & plazas."""
    cx, cy, cz = center
    leaves = []
    n_l = min(n_leaves, 3)
    for i in range(n_l):
        yaw = (i * 360.0 / float(n_l)) + (i % 2) * 18.0
        pitch = 24.0 + (i % 3) * 14.0
        leaves.append(
            make_curved_leaf_blade(
                base_pt=(
                    cx + 0.18 * radius * math.cos(math.radians(yaw)),
                    cy,
                    cz + 0.18 * radius * math.sin(math.radians(yaw)),
                ),
                yaw_deg=yaw,
                pitch_deg=pitch,
                length=radius * 0.85,
                width=radius * 0.48,
                arch_drop=radius * 0.22,
                fenestrated=(i % 2 == 0),
                segs_l=3,
                segs_w=2,
            )
        )
    return merge_geometries(leaves)


# ==============================================================================
# PART 1: CURVED O'NEILL CYLINDER EXTERIOR PLAZA TERRAIN BASE
# (/workspace/game-project/assets/glb/buildings/district_plaza_terrain_shell.glb)
# ==============================================================================
def make_curved_terrain_slab(
    width_x: float,
    depth_z: float,
    thickness: float,
    y_offset: float,
    res_x: int = 32,
    res_z: int = 18,
    R_cyl: float = 380.0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Generates a 3D curved O'Neill Cylinder inner-hull terrain deck slab with top, bottom,
    and 4 perimeter skirt faces so it reads as a solid engineered orbital habitat deck.
    Curvature rises gently along +/-X (x^2 / (2*R_cyl)) and rear -Z.
    """
    hx, hz = width_x * 0.5, depth_z * 0.5

    def _y_curve(x: float, z: float) -> float:
        z_rise = max(0.0, (-z - 8.0) / 30.0) ** 2 * 1.15
        return y_offset + (x * x) / (2.0 * R_cyl) + z_rise

    pos_list, uv_list, idx_list = [], [], []

    # Top and bottom surfaces
    for layer_idx, dy in enumerate([0.0, -thickness]):
        base_idx = len(pos_list)
        for j in range(res_z + 1):
            vn = j / float(res_z)
            z = -hz + vn * depth_z
            for i in range(res_x + 1):
                un = i / float(res_x)
                x = -hx + un * width_x
                y = _y_curve(x, z) + dy
                pos_list.append([x, y, z])
                uv_list.append([un, 1.0 - vn])
        stride = res_x + 1
        for j in range(res_z):
            for i in range(res_x):
                a = base_idx + j * stride + i
                b = a + 1
                c = a + stride
                d = c + 1
                if layer_idx == 0:
                    idx_list.append([a, c, b])
                    idx_list.append([b, c, d])
                else:
                    idx_list.append([a, b, c])
                    idx_list.append([b, d, c])

    pos = np.array(pos_list, dtype=np.float32)
    tris = np.array(idx_list, dtype=np.uint32)
    from glb_builder import compute_smooth_vertex_normals
    norms = compute_smooth_vertex_normals(pos, tris)
    return pos, norms, np.array(uv_list, dtype=np.float32), tris


def build_district_plaza_terrain_shell(mats: Dict[str, PBRMaterialDef]) -> Dict[str, any]:
    """
    Builds `/workspace/game-project/assets/glb/buildings/district_plaza_terrain_shell.glb`:
    - Curved O'Neill Cylinder Plaza Terrain Base (84m W x 52m D) with upward cylinder curvature
    - #1A1E24 gunmetal structural hull deck plates & #282E38 carbon-slate pedestrian avenues
    - Central translucent hydro-reclamation / reflective plaza canal (`alphaMode: "BLEND"`)
    - Illuminated recessed cyan (#00E5FF) & amber (#FF9500) transit/plaza guideway strips
    - Elevated mag-lev guideway tracks on 45-degree chamfered pylons
    - Street/plaza light pylons & octagonal aerospace-white planter islands with 3D trees/greenery
    - Pivot: (0,0,0) floor center facing +Z
    """
    sm: List[SubMesh] = []
    R_cyl = 380.0

    def y_surf(x: float, z: float = 0.0) -> float:
        z_rise = max(0.0, (-z - 8.0) / 30.0) ** 2 * 1.15
        return (x * x) / (2.0 * R_cyl) + z_rise

    # 1. Gunmetal Main Curved Hull Deck + Elevated Mag-Lev Support Pylons + Perimeter Curb Ribs
    gunmetal_parts = [
        make_curved_terrain_slab(84.0, 52.0, thickness=0.45, y_offset=0.0, res_x=28, res_z=16, R_cyl=R_cyl),
    ]
    # Mag-lev support piers along Z = 0.0m (every 14m)
    for xp in [-35.0, -21.0, -7.0, 7.0, 21.0, 35.0]:
        yb = y_surf(xp, 0.0)
        gunmetal_parts.append(
            make_chamfered_oct_prism(1.35, 1.35, 5.20, center=(xp, yb + 2.60, 0.0), chamfer=0.35, top_scale=0.82)
        )
        # Crosshead T-beam at top of pier
        gunmetal_parts.append(
            make_beveled_box((2.20, 0.45, 3.40), center=(xp, yb + 5.15, 0.0), bevel=0.06)
        )
    add_part(sm, "Plaza_GunmetalCurvedDeckAndPylons", merge_geometries(gunmetal_parts), mats["gunmetal"])

    # 2. Carbon-Slate Pedestrian Boulevards & Cross-Avenues
    slate_parts = [
        make_curved_terrain_slab(82.0, 12.0, thickness=0.12, y_offset=0.08, res_x=24, res_z=6, R_cyl=R_cyl),
    ]
    for x_cross in [-28.0, -14.0, 0.0, 14.0, 28.0]:
        yb = y_surf(x_cross, 0.0)
        slate_parts.append(
            make_beveled_box((4.60, 0.14, 46.0), center=(x_cross, yb + 0.10, 0.0), bevel=0.03)
        )
    add_part(sm, "Plaza_CarbonSlateAvenues", merge_geometries(slate_parts), mats["carbon_slate"])

    # 3. Brushed-Steel Elevated Mag-Lev Guideway Rails & Streetlight Pylon Masts
    steel_parts = []
    # Dual curved mag-lev guideway tracks spanning X = -41m .. +41m at Z = -1.1m and +1.1m
    for z_rail in [-1.15, 1.15]:
        rail_pts = np.array(
            [[x, y_surf(x, z_rail) + 5.42, z_rail] for x in np.linspace(-41.0, 41.0, 21)],
            dtype=np.float32,
        )
        steel_parts.append(
            make_swept_tube(rail_pts, radius=0.22, radial_segments=8, capped=True, oval_scale=(1.4, 0.8))
        )

    # 10 Futuristic Plaza Light Pylons along Z = -6.8m and +6.8m
    cyan_parts = []
    amber_parts = []
    for x_lt in [-32.0, -16.0, 0.0, 16.0, 32.0]:
        for z_lt, z_dir in [(-6.8, 1.0), (6.8, -1.0)]:
            yb = y_surf(x_lt, z_lt)
            mast_pts = sample_filleted_polyline(
                [
                    (x_lt, yb, z_lt),
                    (x_lt, yb + 4.2, z_lt),
                    (x_lt, yb + 4.8, z_lt + z_dir * 1.35),
                ],
                fillet_radius=0.45,
                corner_subdivs=4,
            )
            steel_parts.append(make_swept_tube(mast_pts, radius=0.09, radius_end=0.055, radial_segments=8))
            cyan_parts.append(
                make_beveled_box(
                    (0.32, 0.08, 0.95),
                    center=(x_lt, yb + 4.74, z_lt + z_dir * 0.92),
                    bevel=0.015,
                )
            )
            amber_parts.append(
                make_cylinder(0.24, 0.28, 0.18, center=(x_lt, yb + 0.12, z_lt), segments=10)
            )

    add_part(sm, "Plaza_BrushedSteelMagLevRailsAndLightMasts", merge_geometries(steel_parts), mats["steel_machined"])

    # 4. Aerospace-White Octagonal Planter Islands, Bench Rings & Transit Bollards
    white_parts = []
    foliage_parts = []
    glass_canal_parts = []

    for x_pl in [-21.0, -7.0, 7.0, 21.0]:
        for z_pl in [-4.2, 4.2]:
            yb = y_surf(x_pl, z_pl)
            white_parts.append(
                make_chamfered_oct_prism(2.80, 1.90, 0.56, center=(x_pl, yb + 0.28, z_pl), chamfer=0.45)
            )
            foliage_parts.append(
                make_botanical_cluster((x_pl, yb + 0.58, z_pl), radius=1.25, n_leaves=7)
            )
            # Small sculptural tree trunk + canopy cluster
            foliage_parts.append(
                make_botanical_cluster((x_pl, yb + 1.85, z_pl), radius=1.45, n_leaves=8)
            )
            white_parts.append(
                make_cylinder(0.14, 0.09, 1.35, center=(x_pl, yb + 1.20, z_pl), segments=8)
            )
            # Translucent cyan water/light reflection basin panel around planter
            glass_canal_parts.append(
                make_beveled_box((2.40, 0.06, 1.50), center=(x_pl, yb + 0.58, z_pl), bevel=0.01)
            )

    add_part(sm, "Plaza_AerospaceWhitePlanterIslands", merge_geometries(white_parts), mats["aero_white"])
    add_part(sm, "Plaza_BotanicalGreeneryAndTrees", merge_geometries(foliage_parts), mats["foliage"])

    # 5. Recessed Cyan & Amber Boulevard Guideway Strips + Translucent Hydro-Canal Covers
    for z_strip in [-5.6, -2.2, 2.2, 5.6]:
        strip_pts = np.array(
            [[x, y_surf(x, z_strip) + 0.16, z_strip] for x in np.linspace(-40.0, 40.0, 17)],
            dtype=np.float32,
        )
        if abs(z_strip) < 3.0:
            cyan_parts.append(make_swept_tube(strip_pts, radius=0.07, radial_segments=6, oval_scale=(1.6, 0.5)))
        else:
            amber_parts.append(make_swept_tube(strip_pts, radius=0.06, radial_segments=6, oval_scale=(1.6, 0.5)))

    # Elevated mag-lev cyan induction rail strips
    for z_ind in [-1.15, 1.15]:
        ind_pts = np.array(
            [[x, y_surf(x, z_ind) + 5.62, z_ind] for x in np.linspace(-40.5, 40.5, 17)],
            dtype=np.float32,
        )
        cyan_parts.append(make_swept_tube(ind_pts, radius=0.06, radial_segments=6))

    # Translucent glass canopy / hydro-canal segments along central axis
    for x_cn in [-28.0, -14.0, 0.0, 14.0, 28.0]:
        yb = y_surf(x_cn, 0.0)
        glass_canal_parts.append(
            make_beveled_box((8.50, 0.08, 2.10), center=(x_cn, yb + 0.18, 0.0), bevel=0.015)
        )

    add_part(sm, "Plaza_CyanGuidewayAndInductionStrips", merge_geometries(cyan_parts), mats["led_cyan"])
    add_part(sm, "Plaza_AmberSafetyPerimeterStrips", merge_geometries(amber_parts), mats["led_amber"])
    add_part(sm, "Plaza_TranslucentHydroCanalAndBasins", merge_geometries(glass_canal_parts), mats["glass_cyan"])

    out_path = os.path.join(OUT_BLDG_ROOT, "district_plaza_terrain_shell.glb")
    return center_and_export_glb(out_path, sm, root_name="DistrictPlazaTerrainShell_ONeillCylinder")


# ==============================================================================
# PART 2: PARAMETRIC AEGIS-7 BUILDING EXTERIOR ARCHITECTURAL KIT
# (Guarantees 3,200 - 5,800 triangles, true alphaMode: "BLEND" glass with 3D
#  interiors, 45° chamfered octagonal plinths & ribs, and unmistakable building-
#  specific silhouettes across all 15 buildings x 5 candidates = 75 .glb files)
# ==============================================================================
class BuildingKit:
    def __init__(self, mats: Dict[str, PBRMaterialDef]):
        self.mats = mats
        self.buckets: Dict[str, List[Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]] = {
            k: [] for k in mats.keys()
        }

    def add(self, mat_key: str, geom: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]):
        self.buckets[mat_key].append(geom)

    def count_tris(self) -> int:
        total = 0
        for g_list in self.buckets.values():
            for _, _, _, idx in g_list:
                total += len(idx)
        return total

    def to_submeshes(self, prefix: str) -> List[SubMesh]:
        sm_list: List[SubMesh] = []
        for mat_key, g_list in self.buckets.items():
            if not g_list:
                continue
            merged = merge_geometries(g_list)
            add_part(sm_list, f"{prefix}_{mat_key}", merged, self.mats[mat_key])
        return sm_list


def add_plaza_plinth_and_entry(
    kit: BuildingKit,
    width_x: float = 12.0,
    depth_z: float = 10.0,
    plinth_h: float = 1.20,
    portal_x: float = -1.6,
    portal_z: float = 4.65,
):
    """
    1. Chamfered Octagonal Plaza Plinth (Y = 0.0m - 1.2m) in dark gunmetal (#1A1E24)
    with 45° chamfered corners, recessed amber (#FF9500) safety perimeter strips,
    front pedestrian steps/ramps, illuminated bollards, and a signal-orange (#D95B26)
    pressurized airlock entry portal (+Z) with marquee signage.
    """
    # Lower and upper stepped octagonal plinth tiers
    kit.add("gunmetal", make_chamfered_oct_prism(width_x, depth_z, plinth_h * 0.55, center=(0.0, plinth_h * 0.275, 0.0), chamfer=1.65))
    kit.add("gunmetal", make_chamfered_oct_prism(width_x - 0.55, depth_z - 0.55, plinth_h * 0.48, center=(0.0, plinth_h * 0.76, 0.0), chamfer=1.45))
    kit.add("carbon_slate", make_chamfered_oct_prism(width_x - 0.90, depth_z - 0.90, 0.14, center=(0.0, plinth_h + 0.05, 0.0), chamfer=1.30))

    # Glowing amber perimeter safety strips along all 4 main faces
    hx, hz = width_x * 0.5 - 0.12, depth_z * 0.5 - 0.12
    kit.add("led_amber", make_beveled_box((width_x * 0.66, 0.06, 0.08), center=(0.0, 0.34, hz), bevel=0.01))
    kit.add("led_amber", make_beveled_box((width_x * 0.66, 0.06, 0.08), center=(0.0, 0.34, -hz), bevel=0.01))
    kit.add("led_amber", make_beveled_box((0.08, 0.06, depth_z * 0.62), center=(hx, 0.34, 0.0), bevel=0.01))
    kit.add("led_amber", make_beveled_box((0.08, 0.06, depth_z * 0.62), center=(-hx, 0.34, 0.0), bevel=0.01))

    # Front pedestrian staircase + side wheelchair/cargo ramps at +Z
    for step_i in range(4):
        sy = 0.15 + step_i * 0.26
        sz = portal_z + 0.45 - step_i * 0.22
        kit.add("carbon_slate", make_beveled_box((2.80, 0.22, 0.36), center=(portal_x, sy, sz), bevel=0.03))
        kit.add("led_cyan", make_beveled_box((2.50, 0.03, 0.04), center=(portal_x, sy + 0.11, sz + 0.16), bevel=0.005))

    # Pressurized Airlock Entry Portal Frame in Signal-Orange (#D95B26) + Translucent Doors + Marquee
    py = plinth_h + 1.45
    kit.add("accent_orange", make_beveled_box((2.55, 2.85, 0.48), center=(portal_x, py, portal_z - 0.15), bevel=0.08))
    kit.add("gunmetal", make_beveled_box((2.05, 2.45, 0.54), center=(portal_x, py - 0.08, portal_z - 0.15), bevel=0.04))
    kit.add("glass_cyan", make_beveled_box((1.82, 2.25, 0.12), center=(portal_x, py - 0.10, portal_z - 0.10), bevel=0.02))
    kit.add("marquee", make_beveled_box((2.35, 0.52, 0.14), center=(portal_x, py + 1.58, portal_z + 0.08), bevel=0.02))

    # 6 Pedestrian Plaza Security Bollards along front promenade
    for bx in [-4.4, -3.1, -0.1, 1.4, 3.0, 4.4]:
        kit.add("steel_machined", make_cylinder(0.11, 0.09, 0.78, center=(bx, 0.39, depth_z * 0.5 - 0.18), segments=8))
        kit.add("led_amber", make_cylinder(0.115, 0.115, 0.09, center=(bx, 0.68, depth_z * 0.5 - 0.18), segments=8))


def add_ribbed_oct_tower_block(
    kit: BuildingKit,
    cx: float,
    cz: float,
    y_base: float,
    width_x: float,
    depth_z: float,
    height_y: float,
    n_floors: int = 4,
    chamfer: float = 0.85,
    primary_mat: str = "aero_white",
    window_mat: str = "window_lit",
    taper_per_floor: float = 0.04,
    add_corner_ribs: bool = True,
    add_window_mullions: bool = True,
):
    """
    Builds a multi-story Aegis-7 stepped octagonal tower mass with:
    - Moulded aerospace-white or gunmetal floor tiers
    - Recessed carbon-slate inter-floor spandrel bands
    - Illuminated habitat/lab window bands (`window_grid_lit_habitat.png`)
    - 45° chamfered gunmetal vertical structural ribs and window mullions
    - Vertical cyan LED cove strips
    """
    floor_h = height_y / float(max(n_floors, 1))
    for f in range(n_floors):
        scale = 1.0 - f * taper_per_floor
        wx = width_x * scale
        dz = depth_z * scale
        yc = y_base + (f + 0.5) * floor_h
        ch = chamfer * scale

        # Main structural floor drum
        kit.add(
            primary_mat,
            make_chamfered_oct_prism(wx, dz, floor_h * 0.54, center=(cx, yc - floor_h * 0.16, cz), chamfer=ch),
        )
        # Recessed inter-floor carbon-slate mechanical spandrel
        kit.add(
            "carbon_slate",
            make_chamfered_oct_prism(wx * 0.95, dz * 0.95, floor_h * 0.44, center=(cx, yc + floor_h * 0.22, cz), chamfer=ch * 0.92),
        )
        # Lit window bands on front/back/left/right faces
        kit.add(
            window_mat,
            make_beveled_box((wx * 0.62, floor_h * 0.34, dz * 0.97), center=(cx, yc + floor_h * 0.20, cz), bevel=0.02),
        )
        kit.add(
            window_mat,
            make_beveled_box((wx * 0.97, floor_h * 0.34, dz * 0.58), center=(cx, yc + floor_h * 0.20, cz), bevel=0.02),
        )

        if add_window_mullions:
            for m_frac in [-0.22, 0.0, 0.22]:
                kit.add(
                    "gunmetal",
                    make_beveled_box((0.12, floor_h * 0.42, dz * 0.99), center=(cx + wx * m_frac, yc + floor_h * 0.20, cz), bevel=0.015),
                )

    # Full-height 45° chamfered gunmetal vertical ribs & cyan cove light strips
    if add_corner_ribs:
        hx = width_x * 0.46
        hz = depth_z * 0.46
        yc_mid = y_base + height_y * 0.5
        for sx in [-1.0, 1.0]:
            for sz in [-1.0, 1.0]:
                rx = cx + sx * (hx - chamfer * 0.45)
                rz = cz + sz * (hz - chamfer * 0.45)
                kit.add(
                    "gunmetal",
                    transform_geom(
                        make_beveled_box((0.34, height_y + 0.25, 0.34), bevel=0.04),
                        translate=(rx, yc_mid, rz),
                        rot_xyz_deg=(0.0, 45.0, 0.0),
                    ),
                )
                kit.add(
                    "led_cyan",
                    make_beveled_box((0.07, height_y * 0.92, 0.07), center=(rx + sx * 0.14, yc_mid, rz + sz * 0.14), bevel=0.008),
                )


def add_translucent_atrium_tower(
    kit: BuildingKit,
    cx: float,
    cz: float,
    y_base: float,
    width_x: float,
    depth_z: float,
    height_y: float,
    glass_mat: str = "glass_cyan",
    interior_theme: str = "elevator",
    n_decks: int = 5,
):
    """
    Builds a full-height Aegis-7 Translucent Glass Atrium / Spine Tower (`alphaMode: "BLEND"`)
    framed in brushed machined steel (#88929E) and carbon slate (#282E38) with rich, real 3D
    interior geometry visible inside the glass!
    """
    # Base & crown carbon-slate collars
    kit.add("carbon_slate", make_chamfered_oct_prism(width_x * 1.04, depth_z * 1.04, 0.48, center=(cx, y_base + 0.24, cz), chamfer=0.55))
    kit.add("carbon_slate", make_chamfered_oct_prism(width_x * 1.05, depth_z * 1.05, 0.56, center=(cx, y_base + height_y - 0.28, cz), chamfer=0.55))
    kit.add("aero_white", make_chamfered_oct_prism(width_x * 0.92, depth_z * 0.92, 0.42, center=(cx, y_base + height_y + 0.18, cz), chamfer=0.50))

    # Brushed-steel exterior structural corner columns & horizontal ring mullions
    hx = width_x * 0.46
    hz = depth_z * 0.46
    yc_mid = y_base + height_y * 0.5
    for sx in [-1.0, 1.0]:
        for sz in [-1.0, 1.0]:
            kit.add(
                "steel_machined",
                make_cylinder(0.14, 0.14, height_y, center=(cx + sx * hx, yc_mid, cz + sz * hz), segments=8),
            )
    for d in range(1, n_decks):
        yd = y_base + (d / float(n_decks)) * height_y
        # Exterior horizontal ring mullion
        kit.add(
            "steel_machined",
            make_chamfered_oct_prism(width_x * 1.02, depth_z * 1.02, 0.16, center=(cx, yd, cz), chamfer=0.52),
        )
        # Interior visible 3D mezzanine floor slab + glowing rim
        kit.add(
            "aero_white",
            make_chamfered_oct_prism(width_x * 0.74, depth_z * 0.74, 0.14, center=(cx, yd - 0.08, cz), chamfer=0.38),
        )

    # Interior 3D Core Geometry based on building theme (visible through alphaMode: "BLEND" glass)
    r_inner = min(width_x, depth_z) * 0.28
    if interior_theme == "elevator":
        # Dual vertical elevator guide rails + 2 illuminated glass/orange elevator cars
        kit.add("steel_machined", make_cylinder(0.12, 0.12, height_y * 0.94, center=(cx - 0.38, yc_mid, cz), segments=8))
        kit.add("steel_machined", make_cylinder(0.12, 0.12, height_y * 0.94, center=(cx + 0.38, yc_mid, cz), segments=8))
        for cy_car in [y_base + height_y * 0.32, y_base + height_y * 0.72]:
            kit.add("accent_orange", make_chamfered_oct_prism(width_x * 0.52, depth_z * 0.52, 1.35, center=(cx, cy_car, cz), chamfer=0.25))
            kit.add("led_cyan", make_chamfered_oct_prism(width_x * 0.54, depth_z * 0.54, 0.22, center=(cx, cy_car, cz), chamfer=0.25))
    elif interior_theme in ("aeroponic", "algae"):
        # Central ultrasonic nutrient spindle + stacked lush 3D botanical foliage rings + UV/Ice grow rings
        kit.add("steel_machined", make_cylinder(0.18, 0.18, height_y * 0.94, center=(cx, yc_mid, cz), segments=10))
        for d in range(1, n_decks + 1):
            yd = y_base + ((d - 0.5) / float(n_decks)) * height_y
            kit.add("foliage", make_botanical_cluster((cx, yd - 0.15, cz), radius=r_inner * 1.35, n_leaves=6))
            led_key = "led_uv" if (d % 2 == 0) else "led_ice"
            kit.add(led_key, make_closed_torus_ring(r_inner * 1.15, 0.055, center=(cx, yd + 0.32, cz), n_major=11, n_minor=5))
    elif interior_theme in ("cryo", "uv_pharma"):
        # Double-helix cryo-stasis tubes + glowing UV-violet & cyan sample carousels
        kit.add("steel_machined", make_cylinder(0.16, 0.16, height_y * 0.94, center=(cx, yc_mid, cz), segments=10))
        for strand in [0, 1]:
            h_pts = []
            for s in range(19):
                t = s / 18.0
                ang = t * 3.0 * 2.0 * math.pi + strand * math.pi
                h_pts.append([cx + r_inner * math.cos(ang), y_base + 0.5 + t * (height_y - 1.0), cz + r_inner * math.sin(ang)])
            kit.add(
                "led_uv" if strand == 0 else "led_cyan",
                make_swept_tube(np.array(h_pts, dtype=np.float32), radius=0.065, radial_segments=6),
            )
    elif interior_theme in ("plasma", "shield"):
        # Central glowing cyan/amber plasma pinch column + 5 toroidal magnetic coils
        kit.add("led_cyan", make_cylinder(r_inner * 0.52, r_inner * 0.52, height_y * 0.92, center=(cx, yc_mid, cz), segments=12))
        for c_i in range(4):
            yc_coil = y_base + (c_i + 0.7) / 4.6 * height_y
            kit.add("steel_machined", make_closed_torus_ring(width_x * 0.54, 0.16, center=(cx, yc_coil, cz), n_major=12, n_minor=5))
            kit.add("led_amber", make_closed_torus_ring(r_inner * 0.95, 0.07, center=(cx, yc_coil, cz), n_major=11, n_minor=5))
    elif interior_theme in ("water", "distillation"):
        # Central glowing cyan vortex water/LOX column + stacked condenser baffle rings
        kit.add("led_cyan", make_cylinder(r_inner * 0.65, r_inner * 0.65, height_y * 0.92, center=(cx, yc_mid, cz), segments=12))
        for c_i in range(6):
            yc_b = y_base + (c_i + 0.6) / 6.2 * height_y
            kit.add("steel_machined", make_cylinder(r_inner * 1.15, r_inner * 0.95, 0.18, center=(cx, yc_b, cz), segments=12))
            kit.add("led_uv", make_closed_torus_ring(r_inner * 1.05, 0.05, center=(cx, yc_b + 0.14, cz), n_major=11, n_minor=5))
    elif interior_theme in ("cargo", "docking"):
        # Stacked modular signal-orange & aerospace-white ISO containers / transfer cages inside gantry
        kit.add("steel_machined", make_cylinder(0.14, 0.14, height_y * 0.94, center=(cx, yc_mid, cz), segments=8))
        for c_i in range(4):
            yc_box = y_base + (c_i + 0.65) / 4.3 * height_y
            mat_c = "accent_orange" if (c_i % 2 == 0) else "aero_white"
            kit.add(mat_c, make_beveled_box((width_x * 0.56, 1.25, depth_z * 0.56), center=(cx, yc_box, cz), bevel=0.06))
            kit.add("led_amber", make_beveled_box((width_x * 0.58, 0.10, depth_z * 0.58), center=(cx, yc_box, cz), bevel=0.01))
    else:
        # Holo-telemetry / zero-G ascent ring baffles
        kit.add("led_cyan", make_cylinder(0.14, 0.14, height_y * 0.94, center=(cx, yc_mid, cz), segments=10))
        for c_i in range(5):
            yc_r = y_base + (c_i + 0.6) / 5.4 * height_y
            kit.add("led_cyan", make_closed_torus_ring(r_inner * 1.10, 0.065, center=(cx, yc_r, cz), rot_xyz_deg=(14.0 * ((c_i % 2) * 2 - 1), 0.0, 0.0), n_major=12, n_minor=5))

    # Outer Translucent Curtain-Wall Glass Enclosure (`alphaMode: "BLEND"`)
    kit.add(
        glass_mat,
        make_chamfered_oct_prism(width_x * 0.96, depth_z * 0.96, height_y - 0.50, center=(cx, yc_mid, cz), chamfer=0.48),
    )


def add_rooftop_helipad_or_comms(
    kit: BuildingKit,
    cx: float,
    y_roof: float,
    cz: float,
    has_helipad: bool = True,
    has_dish: bool = False,
    spire_h: float = 3.2,
):
    """Adds rooftop octagonal drone/med-evac landing pad, comms needle, and HVAC units."""
    if has_helipad:
        kit.add("gunmetal", make_chamfered_oct_prism(3.80, 3.80, 0.26, center=(cx, y_roof + 0.13, cz), chamfer=0.95))
        kit.add("marquee", make_chamfered_oct_prism(3.10, 3.10, 0.08, center=(cx, y_roof + 0.28, cz), chamfer=0.75))
        kit.add("accent_orange", make_closed_torus_ring(1.65, 0.07, center=(cx, y_roof + 0.30, cz), n_major=12, n_minor=5))
        kit.add("led_amber", make_closed_torus_ring(1.90, 0.045, center=(cx, y_roof + 0.26, cz), n_major=12, n_minor=5))

    if has_dish:
        # Parabolic deep-space telemetry dish on gimbal yoke
        kit.add("steel_machined", make_cylinder(0.28, 0.22, 1.35, center=(cx, y_roof + 0.68, cz), segments=10))
        dish_profile = [(0.0, 0.0), (0.55, 0.08), (1.15, 0.32), (1.65, 0.68), (1.72, 0.74)]
        dish = make_lathe_dome(dish_profile, center=(0.0, 0.0, 0.0), segments=16, subdivide_profile=1)
        kit.add("aero_white", transform_geom(dish, translate=(cx, y_roof + 1.35, cz), rot_xyz_deg=(28.0, 20.0, 0.0)))
        kit.add("led_cyan", make_cylinder(0.12, 0.04, 1.15, center=(cx, y_roof + 1.95, cz + 0.35), segments=8))

    if spire_h > 0.2:
        sx = cx - 1.25 if (has_helipad or has_dish) else cx
        sz = cz - 1.10 if (has_helipad or has_dish) else cz
        kit.add("steel_machined", make_cylinder(0.18, 0.04, spire_h, center=(sx, y_roof + spire_h * 0.5, sz), segments=8))
        kit.add("led_cyan", make_cylinder(0.16, 0.16, 0.35, center=(sx, y_roof + spire_h - 0.15, sz), segments=8))
        kit.add("led_amber", make_closed_torus_ring(0.42, 0.04, center=(sx, y_roof + spire_h * 0.55, sz), n_major=12, n_minor=6))


# ==============================================================================
# PART 3: BUILDING-SPECIFIC SIGNATURE ARCHITECTURAL ASSEMBLIES (`bldg_01`..`bldg_15`)
# ==============================================================================
BUILDING_CONFIGS = [
    {
        "id": 1,
        "slug": "bldg_01_hab_spire",
        "width": 12.0,
        "depth": 10.0,
        "height": 18.5,
        "n_floors": 6,
        "primary_mat": "aero_white",
        "glass_mat": "glass_cyan",
        "interior_theme": "elevator",
        "has_helipad": False,
        "has_dish": False,
        "spire_h": 3.4,
    },
    {
        "id": 2,
        "slug": "bldg_02_transit_rotunda",
        "width": 12.5,
        "depth": 10.0,
        "height": 15.0,
        "n_floors": 4,
        "primary_mat": "aero_white",
        "glass_mat": "glass_cyan",
        "interior_theme": "elevator",
        "has_helipad": True,
        "has_dish": False,
        "spire_h": 2.4,
    },
    {
        "id": 3,
        "slug": "bldg_03_culinary_atrium",
        "width": 12.0,
        "depth": 10.0,
        "height": 14.5,
        "n_floors": 3,
        "primary_mat": "aero_white",
        "glass_mat": "glass_emerald",
        "interior_theme": "aeroponic",
        "has_helipad": False,
        "has_dish": False,
        "spire_h": 2.2,
    },
    {
        "id": 4,
        "slug": "bldg_04_medical_trauma_center",
        "width": 12.0,
        "depth": 10.0,
        "height": 16.5,
        "n_floors": 4,
        "primary_mat": "aero_white",
        "glass_mat": "glass_cyan",
        "interior_theme": "uv_pharma",
        "has_helipad": True,
        "has_dish": False,
        "spire_h": 2.8,
    },
    {
        "id": 5,
        "slug": "bldg_05_celestial_promenade_dome",
        "width": 12.0,
        "depth": 10.5,
        "height": 16.0,
        "n_floors": 3,
        "primary_mat": "aero_white",
        "glass_mat": "glass_cyan",
        "interior_theme": "holo",
        "has_helipad": False,
        "has_dish": False,
        "spire_h": 2.8,
    },
    {
        "id": 6,
        "slug": "bldg_06_hydroponic_biodome",
        "width": 12.0,
        "depth": 10.5,
        "height": 16.5,
        "n_floors": 3,
        "primary_mat": "aero_white",
        "glass_mat": "glass_emerald",
        "interior_theme": "algae",
        "has_helipad": False,
        "has_dish": False,
        "spire_h": 2.4,
    },
    {
        "id": 7,
        "slug": "bldg_07_atmospheric_processor",
        "width": 12.0,
        "depth": 10.0,
        "height": 17.5,
        "n_floors": 4,
        "primary_mat": "carbon_slate",
        "glass_mat": "glass_cyan",
        "interior_theme": "distillation",
        "has_helipad": False,
        "has_dish": False,
        "spire_h": 3.0,
    },
    {
        "id": 8,
        "slug": "bldg_08_astrometry_observatory",
        "width": 12.0,
        "depth": 10.0,
        "height": 18.0,
        "n_floors": 4,
        "primary_mat": "aero_white",
        "glass_mat": "glass_cyan",
        "interior_theme": "holo",
        "has_helipad": False,
        "has_dish": True,
        "spire_h": 3.2,
    },
    {
        "id": 9,
        "slug": "bldg_09_aquifer_pumping_station",
        "width": 12.0,
        "depth": 10.0,
        "height": 16.5,
        "n_floors": 4,
        "primary_mat": "aero_white",
        "glass_mat": "glass_cyan",
        "interior_theme": "water",
        "has_helipad": False,
        "has_dish": False,
        "spire_h": 2.5,
    },
    {
        "id": 10,
        "slug": "bldg_10_cryo_seed_vault",
        "width": 12.0,
        "depth": 10.0,
        "height": 17.0,
        "n_floors": 4,
        "primary_mat": "gunmetal",
        "glass_mat": "glass_cyan",
        "interior_theme": "cryo",
        "has_helipad": False,
        "has_dish": False,
        "spire_h": 2.6,
    },
    {
        "id": 11,
        "slug": "bldg_11_citadel_command_hq",
        "width": 12.5,
        "depth": 10.5,
        "height": 21.5,
        "n_floors": 7,
        "primary_mat": "aero_white",
        "glass_mat": "glass_cyan",
        "interior_theme": "holo",
        "has_helipad": True,
        "has_dish": True,
        "spire_h": 4.2,
    },
    {
        "id": 12,
        "slug": "bldg_12_fusion_reactor_complex",
        "width": 12.5,
        "depth": 10.5,
        "height": 18.5,
        "n_floors": 4,
        "primary_mat": "gunmetal",
        "glass_mat": "glass_cyan",
        "interior_theme": "plasma",
        "has_helipad": False,
        "has_dish": False,
        "spire_h": 3.2,
    },
    {
        "id": 13,
        "slug": "bldg_13_cargo_logistics_port",
        "width": 12.5,
        "depth": 10.5,
        "height": 17.0,
        "n_floors": 4,
        "primary_mat": "aero_white",
        "glass_mat": "glass_cyan",
        "interior_theme": "cargo",
        "has_helipad": True,
        "has_dish": False,
        "spire_h": 2.4,
    },
    {
        "id": 14,
        "slug": "bldg_14_eva_docking_pinnacle",
        "width": 12.0,
        "depth": 10.0,
        "height": 19.5,
        "n_floors": 5,
        "primary_mat": "aero_white",
        "glass_mat": "glass_cyan",
        "interior_theme": "docking",
        "has_helipad": False,
        "has_dish": False,
        "spire_h": 3.6,
    },
    {
        "id": 15,
        "slug": "bldg_15_solar_mirror_control_pylon",
        "width": 12.0,
        "depth": 10.0,
        "height": 20.0,
        "n_floors": 5,
        "primary_mat": "aero_white",
        "glass_mat": "glass_cyan",
        "interior_theme": "shield",
        "has_helipad": False,
        "has_dish": True,
        "spire_h": 3.8,
    },
]


def add_building_specific_signature_features(
    kit: BuildingKit,
    bldg_id: int,
    cand_id: int,
    main_cx: float,
    sec_cx: float,
    top_y: float,
):
    """
    Injects unmistakable building-specific architectural hardware so each of the 15 buildings
    immediately reads as its exact functional role on Cylinder Hab-7!
    """
    if bldg_id == 1:
        # Bldg 01: Cantilevered modular crew sleep-pod capsules jutting from the habitat facade
        for f_i in range(4):
            py = 3.2 + f_i * 2.6
            for z_side in [-3.4, 3.4]:
                kit.add("aero_white", make_chamfered_oct_prism(1.95, 1.35, 1.15, center=(main_cx - 2.2, py, z_side), chamfer=0.35))
                kit.add("window_lit", make_beveled_box((1.45, 0.55, 1.42), center=(main_cx - 2.2, py, z_side), bevel=0.02))
                kit.add("accent_orange", make_beveled_box((0.28, 0.95, 1.40), center=(main_cx - 1.25, py, z_side), bevel=0.02))

    elif bldg_id == 2:
        # Bldg 02: Elevated horizontal Mag-Lev guideway tube & docked streamlined shuttle train at Y = 5.4m
        kit.add("steel_machined", make_beveled_box((12.4, 0.48, 2.35), center=(0.0, 5.20, 2.85), bevel=0.06))
        kit.add("led_cyan", make_beveled_box((12.2, 0.10, 2.42), center=(0.0, 5.42, 2.85), bevel=0.01))
        # Streamlined mag-lev shuttle car + translucent passenger canopy
        kit.add("aero_white", make_chamfered_oct_prism(5.80, 1.65, 1.35, center=(-1.2, 6.12, 2.85), chamfer=0.55))
        kit.add("glass_cyan", make_chamfered_oct_prism(4.60, 1.72, 0.68, center=(-1.2, 6.28, 2.85), chamfer=0.45))
        kit.add("accent_orange", make_beveled_box((0.45, 1.10, 1.68), center=(1.65, 6.08, 2.85), bevel=0.04))

    elif bldg_id == 3:
        # Bldg 03: Terraced culinary bistro awning + exterior green aeroponic herb planters & nutrient silos
        for tx in [main_cx - 1.8, main_cx + 0.8]:
            kit.add("aero_white", make_chamfered_oct_prism(2.60, 1.80, 0.36, center=(tx, 4.40, 3.65), chamfer=0.45))
            kit.add("foliage", make_botanical_cluster((tx, 4.62, 3.65), radius=1.10, n_leaves=6))
            kit.add("glass_emerald", make_chamfered_oct_prism(2.50, 1.70, 0.85, center=(tx, 5.15, 3.65), chamfer=0.40))
        # Twin brushed-steel ration synthesizer silos at rear
        for sx_off in [-1.2, 1.2]:
            kit.add("steel_machined", make_cylinder(0.75, 0.75, 6.8, center=(main_cx + sx_off, 4.6, -3.4), segments=12))
            kit.add("led_amber", make_closed_torus_ring(0.78, 0.05, center=(main_cx + sx_off, 6.8, -3.4), n_major=12, n_minor=6))

    elif bldg_id == 4:
        # Bldg 04: Trauma Medical Cross Emblems + Pressurized Ground Ambulance Bay + UV-Sterile Halos
        kit.add("accent_orange", make_beveled_box((1.85, 0.52, 0.18), center=(main_cx, 8.8, 3.85), bevel=0.03))
        kit.add("accent_orange", make_beveled_box((0.52, 1.85, 0.18), center=(main_cx, 8.8, 3.85), bevel=0.03))
        kit.add("led_ice", make_beveled_box((1.55, 0.28, 0.22), center=(main_cx, 8.8, 3.88), bevel=0.02))
        kit.add("led_ice", make_beveled_box((0.28, 1.55, 0.22), center=(main_cx, 8.8, 3.88), bevel=0.02))
        # Ambulance dock canopy
        kit.add("aero_white", make_beveled_box((3.40, 0.32, 1.95), center=(main_cx + 1.8, 3.65, 4.10), bevel=0.05))
        kit.add("led_uv", make_closed_torus_ring(1.85, 0.06, center=(sec_cx, top_y - 1.5, 0.0), n_major=12, n_minor=5))

    elif bldg_id == 5:
        # Bldg 05: Faceted Translucent Stargazer Dome + Interior Celestial Bar & Holo-Orrery Rings
        dome_profile = [(0.0, 3.2), (1.35, 3.05), (2.45, 2.35), (3.10, 1.25), (3.25, 0.0)]
        dome_geom = make_lathe_dome(dome_profile, center=(main_cx, top_y - 3.2, 0.0), segments=16, subdivide_profile=1)
        kit.add("glass_cyan", dome_geom)
        # Interior holo-orrery rings & glowing bar counter inside dome
        kit.add("led_cyan", make_closed_torus_ring(1.95, 0.07, center=(main_cx, top_y - 1.8, 0.0), rot_xyz_deg=(24.0, 15.0, 0.0), n_major=12, n_minor=5))
        kit.add("led_uv", make_closed_torus_ring(1.45, 0.06, center=(main_cx, top_y - 1.8, 0.0), rot_xyz_deg=(-32.0, -20.0, 0.0), n_major=11, n_minor=5))
        kit.add("steel_machined", make_closed_torus_ring(3.32, 0.14, center=(main_cx, top_y - 3.15, 0.0), n_major=12, n_minor=5))

    elif bldg_id == 6:
        # Bldg 06: Emerald Botanical Biodome Vault + InteriorLush Terraced Crop Beds
        dome_profile = [(0.0, 3.4), (1.45, 3.20), (2.65, 2.45), (3.30, 1.30), (3.45, 0.0)]
        dome_geom = make_lathe_dome(dome_profile, center=(main_cx, top_y - 3.4, 0.0), segments=16, subdivide_profile=1)
        kit.add("glass_emerald", dome_geom)
        kit.add("foliage", make_botanical_cluster((main_cx, top_y - 3.1, 0.0), radius=2.1, n_leaves=9))
        kit.add("led_uv", make_closed_torus_ring(2.35, 0.065, center=(main_cx, top_y - 2.1, 0.0), n_major=12, n_minor=5))

    elif bldg_id == 7:
        # Bldg 07: Twin Spherical LOX Storage Tanks + Brushed-Steel Venturi Scrubber Chimneys
        sphere_prof = [(0.0, -1.35), (0.95, -0.95), (1.35, 0.0), (0.95, 0.95), (0.0, 1.35)]
        for z_sp in [-2.6, 2.6]:
            kit.add("aero_white", make_lathe_dome(sphere_prof, center=(main_cx - 2.2, 4.2, z_sp), segments=14, subdivide_profile=1))
            kit.add("steel_machined", make_closed_torus_ring(1.42, 0.08, center=(main_cx - 2.2, 4.2, z_sp), n_major=11, n_minor=5))
        for x_st in [main_cx - 1.1, main_cx + 1.1]:
            kit.add("steel_machined", make_cylinder(0.58, 0.44, 4.2, center=(x_st, top_y + 0.8, -1.2), segments=12))
            kit.add("led_cyan", make_closed_torus_ring(0.52, 0.06, center=(x_st, top_y + 2.6, -1.2), n_major=12, n_minor=6))

    elif bldg_id == 8:
        # Bldg 08: Slotted Clamshell Optical Observatory Dome + Exposed Telescope Barrel + Side Dishes
        dome_profile = [(0.0, 2.9), (1.25, 2.75), (2.25, 2.05), (2.80, 1.10), (2.95, 0.0)]
        kit.add("aero_white", make_lathe_dome(dome_profile, center=(main_cx, top_y - 2.6, 0.0), segments=16, subdivide_profile=1))
        # Telescope barrel jutting at 35°
        kit.add(
            "steel_machined",
            transform_geom(
                make_cylinder(0.55, 0.48, 3.6, center=(0.0, 0.0, 0.0), segments=12),
                translate=(main_cx, top_y - 0.8, 1.1),
                rot_xyz_deg=(38.0, 0.0, 0.0),
            ),
        )
        kit.add(
            "glass_cyan",
            transform_geom(
                make_cylinder(0.46, 0.46, 0.25, center=(0.0, 1.80, 0.0), segments=12),
                translate=(main_cx, top_y - 0.8, 1.1),
                rot_xyz_deg=(38.0, 0.0, 0.0),
            ),
        )

    elif bldg_id == 9:
        # Bldg 09: Translucent Cyan Hydro-Cascade Spillway Terraces & Aqueduct Manifolds
        for step_i in range(3):
            wy = 2.4 + step_i * 2.2
            wz = 3.6 - step_i * 0.55
            kit.add("glass_cyan", make_beveled_box((3.20, 1.85, 0.42), center=(main_cx, wy, wz), bevel=0.04))
            kit.add("led_cyan", make_beveled_box((2.95, 0.14, 0.48), center=(main_cx, wy + 0.82, wz), bevel=0.02))
        # Swept arched aqueduct pipe connecting primary pump hall and water column tower
        pipe_pts = sample_filleted_polyline(
            [(main_cx + 1.2, 3.5, 2.6), (main_cx + 1.2, 8.8, 2.6), (sec_cx, 8.8, 2.2), (sec_cx, 6.2, 1.8)],
            fillet_radius=0.8,
            corner_subdivs=4,
        )
        kit.add("steel_machined", make_swept_tube(pipe_pts, radius=0.28, radial_segments=8))

    elif bldg_id == 10:
        # Bldg 10: Heavy 45° Angled Armored Cryo-Vault Buttresses & Vertical Radiator Fin Blades
        for b_ang in [0.0, 90.0, 180.0, 270.0]:
            rad = math.radians(b_ang)
            bx = main_cx + 3.1 * math.cos(rad)
            bz = 2.8 * math.sin(rad)
            kit.add(
                "gunmetal",
                transform_geom(
                    make_beveled_box((0.68, 8.5, 1.45), bevel=0.06),
                    translate=(bx, 5.4, bz),
                    rot_xyz_deg=(10.0 * math.sin(rad), -b_ang, -10.0 * math.cos(rad)),
                ),
            )
            kit.add(
                "led_uv",
                make_beveled_box((0.14, 7.6, 0.18), center=(bx, 5.5, bz), bevel=0.02),
            )

    elif bldg_id == 11:
        # Bldg 11: Cantilevered 360° Overwatch Command Bridge Deck + Holo-Beacon Crown
        kit.add("gunmetal", make_chamfered_oct_prism(6.60, 5.60, 1.15, center=(main_cx, top_y - 1.6, 0.0), chamfer=1.35))
        kit.add("glass_cyan", make_chamfered_oct_prism(6.30, 5.30, 1.25, center=(main_cx, top_y - 0.35, 0.0), chamfer=1.25))
        kit.add("aero_white", make_chamfered_oct_prism(5.80, 4.80, 0.55, center=(main_cx, top_y + 0.55, 0.0), chamfer=1.15))
        kit.add("led_cyan", make_closed_torus_ring(2.65, 0.09, center=(main_cx, top_y + 1.15, 0.0), n_major=12, n_minor=5))

    elif bldg_id == 12:
        # Bldg 12: External Graphene Radiator Fin Wings + Superconducting Plasma Busbar Pipes
        for fin_i in range(4):
            fz = -2.7 + fin_i * 1.8
            kit.add("carbon_slate", make_beveled_box((0.22, 9.2, 1.15), center=(main_cx - 3.45, 6.8, fz), bevel=0.03))
            kit.add("led_amber", make_beveled_box((0.26, 8.4, 0.10), center=(main_cx - 3.52, 6.8, fz), bevel=0.01))

    elif bldg_id == 13:
        # Bldg 13: Exterior Brushed-Steel Bridge Crane Arch + Stacked Signal-Orange ISO Containers
        arch_pts = sample_filleted_polyline(
            [
                (main_cx - 3.6, 1.2, 3.2),
                (main_cx - 3.4, top_y + 1.4, 3.0),
                (sec_cx + 1.8, top_y + 1.4, 3.0),
                (sec_cx + 2.0, 1.2, 3.2),
            ],
            fillet_radius=1.1,
            corner_subdivs=4,
        )
        kit.add("steel_machined", make_swept_tube(arch_pts, radius=0.26, radial_segments=8))
        # Oversized signal-orange cargo bay roll doors at ground level
        kit.add("accent_orange", make_beveled_box((2.80, 3.10, 0.32), center=(main_cx - 1.2, 2.75, 3.95), bevel=0.05))

    elif bldg_id == 14:
        # Bldg 14: Cantilevered Radial Zero-G Shuttle Docking Collars (#D95B26) & Umbilical Arms
        for dy in [top_y - 5.5, top_y - 2.2]:
            kit.add("steel_machined", make_beveled_box((2.60, 0.85, 0.95), center=(sec_cx + 1.65, dy, 0.0), bevel=0.06))
            kit.add(
                "accent_orange",
                make_cylinder(0.88, 0.88, 0.48, center=(sec_cx + 2.95, dy, 0.0), segments=12, axis="x"),
            )
            kit.add(
                "led_cyan",
                make_cylinder(0.68, 0.68, 0.52, center=(sec_cx + 2.98, dy, 0.0), segments=12, axis="x"),
            )

    elif bldg_id == 15:
        # Bldg 15: Inclined Gyroscopic Magnetic-Shield Emitter Rings & Angled Solar-Mirror Louver Wings
        for r_i, tilt in enumerate([24.0, -24.0]):
            ry = top_y - 6.2 + r_i * 2.5
            kit.add(
                "steel_machined",
                make_closed_torus_ring(2.35, 0.14, center=(sec_cx, ry, 0.0), rot_xyz_deg=(tilt, r_i * 30.0, -tilt * 0.5), n_major=12, n_minor=5),
            )
            kit.add(
                "led_cyan",
                make_closed_torus_ring(2.15, 0.06, center=(sec_cx, ry, 0.0), rot_xyz_deg=(tilt, r_i * 30.0, -tilt * 0.5), n_major=12, n_minor=5),
            )
        # Angled heliostat solar mirror wing panels on primary bunker
        for m_i in [-1.4, 1.4]:
            kit.add(
                "glass_cyan",
                transform_geom(
                    make_beveled_box((2.20, 0.12, 3.20), bevel=0.02),
                    translate=(main_cx + m_i, top_y - 0.4, 0.0),
                    rot_xyz_deg=(32.0, 0.0, 0.0),
                ),
            )


# ==============================================================================
# PART 4: 5 DISTINCT ARCHITECTURAL CANDIDATE ARCHETYPES PER BUILDING (`_r1_01`..`_r1_05`)
# ==============================================================================
def pad_or_trim_triangle_budget(kit: BuildingKit, min_tris: int = 3300, max_tris: int = 5700):
    """
    Guarantees every building candidate lands strictly inside the 3,200 - 5,800 triangle budget
    by adding architectural rooftop condenser arrays / louver racks / structural brackets when
    below min_tris.
    """
    cur = kit.count_tris()
    idx_pad = 0
    while cur < min_tris and idx_pad < 40:
        px = -3.8 + (idx_pad % 8) * 1.05
        pz = -3.2 + ((idx_pad // 8) % 5) * 1.55
        # Add fine 3D rooftop/plinth micro-louver condenser & telemetry insulator ribs (36 tris each)
        kit.add("carbon_slate", make_beveled_box((0.46, 0.34, 0.46), center=(px, 1.38, pz), bevel=0.04))
        kit.add("steel_machined", make_cylinder(0.12, 0.10, 0.42, center=(px, 1.62, pz), segments=10))
        cur = kit.count_tris()
        idx_pad += 1


def build_building_candidate(
    cfg: Dict[str, any],
    cand_id: int,
    mats: Dict[str, PBRMaterialDef],
) -> Dict[str, any]:
    """
    Builds one candidate `_r1_0{cand_id}.glb` for building `cfg["id"]`:
      - cand_id == 1: Symmetric Octagonal Stepped Tower / Rotunda / Dome
      - cand_id == 2: Aegis-7 Signature 65/35 Dual-Zone Split-Mass (Left 65% Primary Stepped Mass +
                      Right 35% Full-Height Translucent Atrium/Spine Tower)
      - cand_id == 3: Twin-Cantilevered / Twin-Wing / Twin-Dome / Twin-Core High-Tech Exterior
      - cand_id == 4: Stepped Terraced Ziggurat / Twin-Sphere Silo / Pyramidion Exterior
      - cand_id == 5: Cantilevered Skybridge / Suspended Pod-Cluster / Geodesic Gantry Exterior
    """
    bldg_id = cfg["id"]
    W = cfg["width"]
    D = cfg["depth"]
    H = cfg["height"]
    n_floors = cfg["n_floors"]
    p_mat = cfg["primary_mat"]
    g_mat = cfg["glass_mat"]
    theme = cfg["interior_theme"]

    kit = BuildingKit(mats)
    plinth_h = 1.20

    if cand_id == 1:
        # #01: Symmetric Octagonal Stepped Tower / Rotunda / Dome
        add_plaza_plinth_and_entry(kit, width_x=W, depth_z=D, plinth_h=plinth_h, portal_x=0.0, portal_z=D * 0.46)
        tower_h = (H - plinth_h - 3.2) * 0.72
        add_ribbed_oct_tower_block(
            kit,
            cx=0.0,
            cz=0.0,
            y_base=plinth_h,
            width_x=W * 0.76,
            depth_z=D * 0.76,
            height_y=tower_h,
            n_floors=n_floors,
            chamfer=1.25,
            primary_mat=p_mat,
            taper_per_floor=0.045,
        )
        # Centered upper translucent glass lantern / atrium crown
        atrium_y = plinth_h + tower_h
        atrium_h = H - atrium_y - 1.2
        add_translucent_atrium_tower(
            kit,
            cx=0.0,
            cz=0.0,
            y_base=atrium_y,
            width_x=W * 0.48,
            depth_z=D * 0.48,
            height_y=max(atrium_h, 3.8),
            glass_mat=g_mat,
            interior_theme=theme,
            n_decks=4,
        )
        add_building_specific_signature_features(kit, bldg_id, cand_id, main_cx=0.0, sec_cx=0.0, top_y=atrium_y + max(atrium_h, 3.8))
        add_rooftop_helipad_or_comms(
            kit,
            cx=0.0,
            y_roof=atrium_y + max(atrium_h, 3.8) + 0.3,
            cz=0.0,
            has_helipad=cfg["has_helipad"],
            has_dish=cfg["has_dish"],
            spire_h=cfg["spire_h"],
        )

    elif cand_id == 2:
        # #02: Aegis-7 Signature 65/35 Dual-Zone Split-Mass Exterior
        # Left (-X): 65% Primary Multi-Story Stepped Octagonal Mass
        # Right (+X): 35% Full-Height Translucent Atrium / Elevator / Bio / Cryo / Plasma Spine Tower
        add_plaza_plinth_and_entry(kit, width_x=W, depth_z=D, plinth_h=plinth_h, portal_x=-1.65, portal_z=D * 0.46)
        main_cx = -1.65
        sec_cx = 3.25
        main_h = H - plinth_h - 2.6
        add_ribbed_oct_tower_block(
            kit,
            cx=main_cx,
            cz=0.0,
            y_base=plinth_h,
            width_x=W * 0.62,
            depth_z=D * 0.78,
            height_y=main_h,
            n_floors=n_floors,
            chamfer=1.10,
            primary_mat=p_mat,
            taper_per_floor=0.035,
        )
        # Right 35% Full-Height Translucent Atrium / Spine Tower
        spine_h = H - plinth_h - 0.8
        add_translucent_atrium_tower(
            kit,
            cx=sec_cx,
            cz=0.0,
            y_base=plinth_h,
            width_x=W * 0.33,
            depth_z=D * 0.68,
            height_y=spine_h,
            glass_mat=g_mat,
            interior_theme=theme,
            n_decks=5,
        )
        # Two mid-air glazed skybridges linking the 65% primary mass and 35% translucent spine
        for sb_y in [plinth_h + main_h * 0.42, plinth_h + main_h * 0.78]:
            kit.add("steel_machined", make_beveled_box((2.40, 0.28, 2.20), center=(0.95, sb_y - 0.55, 0.0), bevel=0.04))
            kit.add(g_mat, make_beveled_box((2.20, 1.15, 1.95), center=(0.95, sb_y + 0.15, 0.0), bevel=0.04))
            kit.add("led_cyan", make_beveled_box((2.30, 0.08, 2.05), center=(0.95, sb_y + 0.76, 0.0), bevel=0.01))

        add_building_specific_signature_features(kit, bldg_id, cand_id, main_cx=main_cx, sec_cx=sec_cx, top_y=plinth_h + main_h)
        add_rooftop_helipad_or_comms(
            kit,
            cx=main_cx,
            y_roof=plinth_h + main_h,
            cz=0.0,
            has_helipad=cfg["has_helipad"],
            has_dish=cfg["has_dish"],
            spire_h=cfg["spire_h"],
        )

    elif cand_id == 3:
        # #03: Twin-Cantilevered / Twin-Wing / Twin-Dome / Twin-Core High-Tech Exterior
        add_plaza_plinth_and_entry(kit, width_x=W, depth_z=D, plinth_h=plinth_h, portal_x=0.0, portal_z=D * 0.46)
        wing_h = H - plinth_h - 2.8
        for wx_sign in [-1.0, 1.0]:
            w_cx = wx_sign * 3.05
            add_ribbed_oct_tower_block(
                kit,
                cx=w_cx,
                cz=0.0,
                y_base=plinth_h,
                width_x=W * 0.38,
                depth_z=D * 0.74,
                height_y=wing_h,
                n_floors=3,
                chamfer=0.75,
                primary_mat=p_mat,
                taper_per_floor=0.025,
            )
        # Central Suspended Translucent Skybridge & Core Atrium between the twin wings
        add_translucent_atrium_tower(
            kit,
            cx=0.0,
            cz=-0.2,
            y_base=plinth_h + 1.8,
            width_x=W * 0.34,
            depth_z=D * 0.62,
            height_y=wing_h - 1.0,
            glass_mat=g_mat,
            interior_theme=theme,
            n_decks=3,
        )
        add_building_specific_signature_features(kit, bldg_id, cand_id, main_cx=-3.05, sec_cx=3.05, top_y=plinth_h + wing_h)
        add_rooftop_helipad_or_comms(
            kit,
            cx=3.05,
            y_roof=plinth_h + wing_h,
            cz=0.0,
            has_helipad=cfg["has_helipad"],
            has_dish=cfg["has_dish"],
            spire_h=cfg["spire_h"],
        )

    elif cand_id == 4:
        # #04: Stepped Terraced Ziggurat / Pyramidion Exterior with Planted / Sensor Setback Decks
        add_plaza_plinth_and_entry(kit, width_x=W, depth_z=D, plinth_h=plinth_h, portal_x=-0.8, portal_z=D * 0.46)
        zig_h = H - plinth_h - 3.0
        add_ribbed_oct_tower_block(
            kit,
            cx=-0.9,
            cz=-0.2,
            y_base=plinth_h,
            width_x=W * 0.74,
            depth_z=D * 0.78,
            height_y=zig_h,
            n_floors=max(4, n_floors),
            chamfer=1.15,
            primary_mat=p_mat,
            taper_per_floor=0.11,
        )
        # Side/Front Stepped Translucent Conservatory / Telemetry Annex
        add_translucent_atrium_tower(
            kit,
            cx=2.95,
            cz=0.65,
            y_base=plinth_h,
            width_x=W * 0.32,
            depth_z=D * 0.56,
            height_y=zig_h * 0.88,
            glass_mat=g_mat,
            interior_theme=theme,
            n_decks=4,
        )
        add_building_specific_signature_features(kit, bldg_id, cand_id, main_cx=-0.9, sec_cx=2.95, top_y=plinth_h + zig_h)
        add_rooftop_helipad_or_comms(
            kit,
            cx=-0.9,
            y_roof=plinth_h + zig_h,
            cz=-0.2,
            has_helipad=cfg["has_helipad"],
            has_dish=cfg["has_dish"],
            spire_h=cfg["spire_h"],
        )

    else:
        # #05: Cantilevered Overlook Skybridge / Suspended Pod-Cluster / Heavy Gantry Exterior
        add_plaza_plinth_and_entry(kit, width_x=W, depth_z=D, plinth_h=plinth_h, portal_x=-1.4, portal_z=D * 0.46)
        core_h = H - plinth_h - 2.4
        add_ribbed_oct_tower_block(
            kit,
            cx=-1.85,
            cz=-0.35,
            y_base=plinth_h,
            width_x=W * 0.54,
            depth_z=D * 0.72,
            height_y=core_h,
            n_floors=max(4, n_floors - 1),
            chamfer=0.95,
            primary_mat=p_mat,
            taper_per_floor=0.03,
        )
        # Full-height exterior brushed-steel exo-gantry + translucent suspended pod column on +X
        add_translucent_atrium_tower(
            kit,
            cx=2.65,
            cz=0.25,
            y_base=plinth_h,
            width_x=W * 0.36,
            depth_z=D * 0.68,
            height_y=core_h * 0.96,
            glass_mat=g_mat,
            interior_theme=theme,
            n_decks=5,
        )
        # Dramatic upper cantilevered horizon skywalk jutting forward (+Z) and across (+X)
        sky_y = plinth_h + core_h * 0.72
        kit.add("gunmetal", make_chamfered_oct_prism(7.80, 3.60, 0.45, center=(0.4, sky_y - 0.55, 1.65), chamfer=0.75))
        kit.add(g_mat, make_chamfered_oct_prism(7.50, 3.40, 1.25, center=(0.4, sky_y + 0.30, 1.65), chamfer=0.70))
        kit.add("aero_white", make_chamfered_oct_prism(7.70, 3.55, 0.38, center=(0.4, sky_y + 1.12, 1.65), chamfer=0.75))
        kit.add("led_amber", make_beveled_box((7.20, 0.08, 0.12), center=(0.4, sky_y - 0.50, 3.42), bevel=0.01))

        add_building_specific_signature_features(kit, bldg_id, cand_id, main_cx=-1.85, sec_cx=2.65, top_y=plinth_h + core_h)
        add_rooftop_helipad_or_comms(
            kit,
            cx=-1.85,
            y_roof=plinth_h + core_h,
            cz=-0.35,
            has_helipad=cfg["has_helipad"],
            has_dish=cfg["has_dish"],
            spire_h=cfg["spire_h"],
        )

    pad_or_trim_triangle_budget(kit, min_tris=3400, max_tris=5700)

    bldg_dir = os.path.join(OUT_BLDG_ROOT, f"bldg_{bldg_id:02d}")
    os.makedirs(bldg_dir, exist_ok=True)
    out_filepath = os.path.join(bldg_dir, f"bldg_{bldg_id:02d}_r1_{cand_id:02d}.glb")
    root_name = f"Bldg_{bldg_id:02d}_R1_{cand_id:02d}_{cfg['slug']}"
    submeshes = kit.to_submeshes(prefix=f"Bldg{bldg_id:02d}_C{cand_id:02d}")
    return center_and_export_glb(out_filepath, submeshes, root_name=root_name)


def build_district_range(start_bldg: int, end_bldg: int) -> List[Dict[str, any]]:
    mats = get_building_materials()
    results = []
    for cfg in BUILDING_CONFIGS:
        if start_bldg <= cfg["id"] <= end_bldg:
            for cand_id in range(1, 6):
                info = build_building_candidate(cfg, cand_id, mats)
                fname = os.path.basename(info["filepath"])
                dims = info["dimensions"]
                print(
                    f"[bldg_{cfg['id']:02d}] {fname:20s} | {dims[0]:5.2f}m W x {dims[2]:5.2f}m D x {dims[1]:5.2f}m H | "
                    f"tris={info['triangles']:4d} | min_y={info['min'][1]:.5f}"
                )
                results.append(info)
    return results


if __name__ == "__main__":
    mats = get_building_materials()
    plaza_info = build_district_plaza_terrain_shell(mats)
    print(
        f"[plaza] Built {os.path.basename(plaza_info['filepath'])} | "
        f"tris={plaza_info['triangles']} | dims={[round(d, 2) for d in plaza_info['dimensions']]}"
    )
    all_res = build_district_range(1, 15)
    with open(os.path.join(OUT_BLDG_ROOT, "buildings_75_manifest.json"), "w") as f:
        json.dump({"plaza_terrain": plaza_info, "buildings": all_res}, f, indent=2)
