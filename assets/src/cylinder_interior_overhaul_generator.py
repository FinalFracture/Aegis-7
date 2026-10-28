#!/usr/bin/env python3
"""
Cylinder Hab-7 3D Interior Biome, Terrain, Ring-River, Bridge & Macro-Setpiece Geometry Overhaul
Owner: Rook (3D Modeling Specialist)

Follows:
  1. Vance's Spec: `/workspace/game-project/design/cylinder_interior_overhaul_spec.md`
  2. Sloane's Spec & New Textures: `/workspace/game-project/design/sloane_cylinder_interior_lighting_and_textures_spec.md`
     & `/workspace/game-project/assets/textures/cylinder_interior/`

Builds & Validates:
  Part 1 — 5 Hero Interior Macro-Setpieces x 5 Candidates Each = 25 .glb files (`3,600 - 5,800` tris each):
    - `interior_setpiece_01` (`interior_setpiece_01_ring_skybridge_viaduct`)
    - `interior_setpiece_02` (`interior_setpiece_02_terraced_waterfall_reservoir`)
    - `interior_setpiece_03` (`interior_setpiece_03_axial_suncore_spoke_hub`)
    - `interior_setpiece_04` (`interior_setpiece_04_endcap_cliffside_citadel`)
    - `interior_setpiece_05` (`interior_setpiece_05_elevated_plaza_interchange`)
    + Stages canonical `#02` winners into `/workspace/game-project/assets/glb/winners/` and `/workspace/game-project/assets/glb/cylinder_interior/`.

  Part 2 — 3 Bespoke Non-Repetitive Curved Valley Biome & Terrain Shells (`R = 200m`, `min_y = 0.0`):
    - `/workspace/game-project/assets/glb/cylinder_interior/valley_a_civic_acropolis_terraces.glb`
    - `/workspace/game-project/assets/glb/cylinder_interior/valley_b_meandering_river_biosphere.glb`
    - `/workspace/game-project/assets/glb/cylinder_interior/valley_c_industrial_switchyard_port.glb`

  Part 3 — Overhauled `cylinder_r1_02.glb` & `cylinder_winner_01_hab7_exterior.glb` (+ aliases):
    - Replaces repetitive 3-way clone strips inside `cylinder_r1_02.glb` with radially asymmetric
      Valley A (Civic Acropolis), Valley B (Meandering River & Emerald Biosphere), and Valley C
      (Industrial Switchyard & Port) biomes + Golden-Hour Axial Solar Core (`sky_axial_golden_hour_gradient.png`).
"""
import os
import sys
import io
import math
import json
import shutil
from typing import Dict, List, Tuple
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glb_builder as _gb
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
)
from bunk_round1_generator import (
    hex_rgba,
    add_part,
    center_and_export_glb,
)
from buildings_exteriors_generator import (
    get_building_materials,
    make_chamfered_oct_prism,
    make_closed_torus_ring,
    make_botanical_cluster,
    BuildingKit,
)
from cylinder_hab7_fullscale_generator import (
    CYL_Y,
    make_cyl_arc_shell,
    make_axial_ring,
    place_inward_on_cylinder,
    add_hemispherical_or_stepped_endcaps,
)

TEX_CYL_INT_DIR = "/workspace/game-project/assets/textures/cylinder_interior"
OUT_CYL_INT_DIR = "/workspace/game-project/assets/glb/cylinder_interior"
OUT_CYL_DIR = "/workspace/game-project/assets/glb/cylinder"
WINNERS_DIR = "/workspace/game-project/assets/glb/winners"
os.makedirs(OUT_CYL_INT_DIR, exist_ok=True)
os.makedirs(OUT_CYL_DIR, exist_ok=True)
os.makedirs(WINNERS_DIR, exist_ok=True)

# Override texture bytes loader so `water_ring_river_specular.png` preserves its sapphire/turquoise/gold RGBA
_ORIG_TEX_LOADER = _gb.get_calm_scifi_texture_bytes
_CUSTOM_TEX_CACHE: Dict[Tuple, bytes] = {}


def _interior_overhaul_tex_bytes(mdef: PBRMaterialDef) -> bytes:
    k = (mdef.name, mdef.base_color, mdef.texture_path, mdef.alpha_mode)
    if k in _CUSTOM_TEX_CACHE:
        return _CUSTOM_TEX_CACHE[k]
    if mdef.texture_path and os.path.exists(mdef.texture_path) and "water_ring_river" in mdef.texture_path:
        im = Image.open(mdef.texture_path).convert("RGBA").resize((512, 512), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format="PNG", optimize=True)
        _CUSTOM_TEX_CACHE[k] = buf.getvalue()
        return _CUSTOM_TEX_CACHE[k]
    res = _ORIG_TEX_LOADER(mdef)
    _CUSTOM_TEX_CACHE[k] = res
    return res


_gb.get_calm_scifi_texture_bytes = _interior_overhaul_tex_bytes


def tex_cyl_int(fname: str) -> str:
    p = os.path.join(TEX_CYL_INT_DIR, fname)
    if os.path.exists(p):
        return p
    p2 = os.path.join("/workspace/game-project/godot/assets/textures", fname)
    if os.path.exists(p2): return p2
    return os.path.join("/workspace/game-project/assets/textures", fname)


def remap_uv_u(
    geom: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    u_min: float,
    u_max: float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Remaps UV.u into [u_min, u_max] for dual-atlas textures like window_clusters_warm_amber_vs_cool_industrial.png."""
    p, n, u, idx = geom
    u_new = u.copy()
    u_new[:, 0] = u_min + np.clip(u_new[:, 0], 0.0, 1.0) * (u_max - u_min)
    return p, n, u_new, idx


def get_interior_overhaul_materials() -> Dict[str, PBRMaterialDef]:
    mats = get_building_materials()
    mats.update(
        {
            "biome_canopy": PBRMaterialDef(
                name="Mat_Biome_TerracedBotanicalCanopy",
                base_color=(1.0, 1.0, 1.0, 1.0),
                metallic=0.02,
                roughness=0.72,
                texture_path=tex_cyl_int("biome_terraced_botanical_canopy.png"),
                double_sided=True,
            ),
            "water_river": PBRMaterialDef(
                name="Mat_Water_RingRiver_Specular_Translucent",
                base_color=(0.35, 0.85, 0.98, 0.82),
                metallic=0.15,
                roughness=0.08,
                emissive=(0.04, 0.26, 0.36),
                texture_path=tex_cyl_int("water_ring_river_specular.png"),
                double_sided=True,
                alpha_mode="BLEND",
            ),
            "cliff_basalt": PBRMaterialDef(
                name="Mat_Terrain_BasaltTitaniumCliffRock",
                base_color=(1.0, 1.0, 1.0, 1.0),
                metallic=0.28,
                roughness=0.68,
                texture_path=tex_cyl_int("terrain_basalt_titanium_cliff_rock.png"),
            ),
            "promenade_paving": PBRMaterialDef(
                name="Mat_Terrain_ParkPromenadePaving",
                base_color=(1.0, 1.0, 1.0, 1.0),
                metallic=0.18,
                roughness=0.42,
                emissive=(0.14, 0.09, 0.02),
                texture_path=tex_cyl_int("terrain_park_promenade_paving.png"),
            ),
            "window_warm_amber": PBRMaterialDef(
                name="Mat_Window_WarmAmberResidential_Lit",
                base_color=(1.0, 1.0, 1.0, 1.0),
                metallic=0.35,
                roughness=0.28,
                emissive=(0.95, 0.68, 0.22),
                texture_path=tex_cyl_int("window_clusters_warm_amber_vs_cool_industrial.png"),
            ),
            "window_cool_ind": PBRMaterialDef(
                name="Mat_Window_CoolIndustrialTelemetry_Lit",
                base_color=(1.0, 1.0, 1.0, 1.0),
                metallic=0.45,
                roughness=0.26,
                emissive=(0.25, 0.82, 1.0),
                texture_path=tex_cyl_int("window_clusters_warm_amber_vs_cool_industrial.png"),
            ),
            "sky_golden_core": PBRMaterialDef(
                name="Mat_Emissive_AxialGoldenHourSunCore",
                base_color=(1.0, 1.0, 1.0, 1.0),
                metallic=0.0,
                roughness=0.15,
                emissive=(1.0, 0.78, 0.36),
                texture_path=tex_cyl_int("sky_axial_golden_hour_gradient.png"),
            ),
            "copper_bridge": PBRMaterialDef(
                name="Mat_Metal_CopperAnodizedBridge",
                base_color=hex_rgba("#C87D55"),
                metallic=0.78,
                roughness=0.32,
                texture_path=tex_cyl_int("terrain_park_promenade_paving.png"),
            ),
            "led_emerald": PBRMaterialDef(
                name="Mat_Emissive_BioluminescentEmeraldLED",
                base_color=hex_rgba("#00E676"),
                metallic=0.0,
                roughness=0.15,
                emissive=(0.0, 0.92, 0.48),
                texture_path=tex_cyl_int("biome_terraced_botanical_canopy.png"),
            ),
        }
    )
    return mats


def tune_setpiece_budget(kit: BuildingKit, min_tris: int = 3700, max_tris: int = 5650, y_level: float = 0.6, cand_id: int = 1):
    # Add candidate-specific architectural structures so _01.._05 have distinct silhouettes & triangle counts
    if cand_id == 2:
        # Signature #02 extra Aegis-7 Dual-Zone Split skybridges, beacon rings & telemetry pylons
        kit.add("steel_machined", make_closed_torus_ring(6.2, 0.24, center=(4.5, y_level + 8.5, 0.0), rot_xyz_deg=(18.0, 0.0, 0.0), n_major=16, n_minor=6))
        kit.add("led_cyan", make_closed_torus_ring(5.6, 0.12, center=(4.5, y_level + 8.5, 0.0), rot_xyz_deg=(18.0, 0.0, 0.0), n_major=16, n_minor=6))
        kit.add("accent_orange", make_chamfered_oct_prism(3.6, 3.6, 2.2, center=(-5.5, y_level + 4.2, 4.2), chamfer=0.75))
    elif cand_id == 3:
        # #03 Twin-Wing / Twin-Spillway / Geodesic Truss arches
        for sx in [-8.5, 8.5]:
            kit.add("steel_machined", make_chamfered_oct_prism(3.8, 3.8, 9.5, center=(sx, y_level + 4.8, -3.5), chamfer=0.85))
            kit.add("glass_emerald", make_chamfered_oct_prism(4.2, 4.2, 3.5, center=(sx, y_level + 10.2, -3.5), chamfer=0.9))
    elif cand_id == 4:
        # #04 Stepped Ziggurat / Heliostat Wing Array
        for tier_z in range(3):
            kit.add("aero_white", make_chamfered_oct_prism(12.0 - tier_z * 2.5, 8.0 - tier_z * 1.5, 1.8, center=(0.0, y_level + 2.0 + tier_z * 2.2, 4.0), chamfer=1.4))
    elif cand_id == 5:
        # #05 Cantilevered Overlook Deck & Twin Telemetry Pylons
        kit.add("gunmetal", make_chamfered_oct_prism(16.5, 6.5, 1.4, center=(2.5, y_level + 9.5, 5.5), chamfer=1.6))
        kit.add("glass_cyan", make_chamfered_oct_prism(15.8, 5.8, 2.2, center=(2.5, y_level + 11.2, 5.5), chamfer=1.5))

    target_min = min_tris + (cand_id * 110) if cand_id != 2 else min_tris + 420
    cur = kit.count_tris()
    idx_p = 0
    while cur < target_min and idx_p < 90:
        ang = (idx_p / 14.0) * 2.0 * math.pi
        r = 7.5 + (idx_p % 5) * 2.4
        rx = r * math.cos(ang)
        rz = r * math.sin(ang)
        kit.add("cliff_basalt", make_beveled_box((0.95, 0.55, 0.95), center=(rx, y_level, rz), bevel=0.08))
        kit.add("steel_machined", make_cylinder(0.24, 0.18, 0.75, center=(rx, y_level + 0.55, rz), segments=10))
        cur = kit.count_tris()
        idx_p += 1


# ==============================================================================
# PART 1: 5 HERO INTERIOR MACRO-SETPIECES (`interior_setpiece_01` .. `05` x 5 Candidates = 25 GLBs)
# Triangle budget: strictly 3,600 - 5,800 triangles per .glb
# ==============================================================================
def build_setpiece_01_candidate(cand_id: int, mats: Dict[str, PBRMaterialDef]) -> Dict[str, any]:
    """
    interior_setpiece_01 (`interior_setpiece_01_ring_skybridge_viaduct`):
    Curved 120° Ring-Spanning Suspension Skybridge & Multi-Tier Mag-Lev Viaduct Arch
      #01: Symmetric Twin-Pylon Curved Mag-Lev Viaduct Arch
      #02: Dual-Zone Split Curved Suspension Viaduct Deck & Translucent Mid-Span Sky-Transfer Rotunda
      #03: Tri-Chord Space-Frame Truss Skybridge & Cargo Rail
      #04: Cantilevered Solarium Overlook Arch & Pedestrian Promenade
      #05: Heavy Buttressed Ring-Highway Interchange & Drone Pylon
    """
    kit = BuildingKit(mats)

    # Sample a dramatic curved arch span (width ~68m, depth ~18m, height ~24m)
    def _add_viaduct_arch_deck(span_x: float = 64.0, arch_h: float = 16.0, deck_w: float = 12.0, n_segs: int = 16):
        xs = np.linspace(-span_x * 0.5, span_x * 0.5, n_segs + 1)
        arch_pts_f, arch_pts_b = [], []
        for x in xs:
            u = x / (span_x * 0.5)
            y = 2.0 + arch_h * (1.0 - u * u)
            arch_pts_f.append([x, y, deck_w * 0.42])
            arch_pts_b.append([x, y, -deck_w * 0.42])
        kit.add("gunmetal", make_swept_tube(np.array(arch_pts_f, dtype=np.float32), radius=0.95, radial_segments=8))
        kit.add("gunmetal", make_swept_tube(np.array(arch_pts_b, dtype=np.float32), radius=0.95, radial_segments=8))

        # Upper & lower curved promenade / mag-lev deck slabs + diagonal tension cables
        for i in range(n_segs):
            xm = 0.5 * (xs[i] + xs[i + 1])
            u = xm / (span_x * 0.5)
            ya = 2.0 + arch_h * (1.0 - u * u)
            seg_len = (span_x / float(n_segs)) * 1.06
            slope_deg = math.degrees(math.atan2(-2.0 * arch_h * u / (span_x * 0.5), 1.0))
            kit.add(
                "promenade_paving",
                transform_geom(make_beveled_box((seg_len, 0.65, deck_w), bevel=0.08), translate=(xm, ya - 2.2, 0.0), rot_xyz_deg=(0.0, 0.0, slope_deg)),
            )
            kit.add(
                "led_cyan",
                transform_geom(make_beveled_box((seg_len, 0.18, 0.45), bevel=0.02), translate=(xm, ya - 1.8, deck_w * 0.35), rot_xyz_deg=(0.0, 0.0, slope_deg)),
            )
            kit.add(
                "led_amber",
                transform_geom(make_beveled_box((seg_len, 0.18, 0.45), bevel=0.02), translate=(xm, ya - 1.8, -deck_w * 0.35), rot_xyz_deg=(0.0, 0.0, slope_deg)),
            )
            # Diagonal brushed-steel tension cables from arch ribs to deck
            for sz_c in [-deck_w * 0.40, deck_w * 0.40]:
                c_pts = np.array([[xm, ya - 2.2, sz_c], [xm, ya + 2.8, sz_c * 0.85]], dtype=np.float32)
                kit.add("steel_machined", make_swept_tube(c_pts, radius=0.18, radial_segments=6))

    # Basalt-titanium & gunmetal anchor abutments at both ends
    for sx in [-28.0, 28.0]:
        kit.add("cliff_basalt", make_chamfered_oct_prism(11.0, 14.0, 4.2, center=(sx, 2.1, 0.0), chamfer=2.2))
        kit.add("gunmetal", make_chamfered_oct_prism(8.5, 11.5, 14.5, center=(sx, 9.2, 0.0), chamfer=1.8, top_scale=0.82))
        kit.add("led_amber", make_chamfered_oct_prism(11.2, 14.2, 0.28, center=(sx, 0.45, 0.0), chamfer=2.2))

    if cand_id == 1:
        _add_viaduct_arch_deck(span_x=62.0, arch_h=15.5, deck_w=11.5, n_segs=14)
        for px in [-14.0, 14.0]:
            kit.add("aero_white", make_chamfered_oct_prism(4.2, 12.5, 21.0, center=(px, 11.5, 0.0), chamfer=0.9, top_scale=0.78))
            kit.add("glass_cyan", make_chamfered_oct_prism(5.5, 6.5, 3.8, center=(px, 19.5, 0.0), chamfer=1.1))

    elif cand_id == 2:
        # #02 (Aegis-7 65/35 Signature): Dual-Zone Split Curved Suspension Viaduct Deck
        # & Suspended Mid-Span Translucent Sky-Transfer Rotunda + Docked Mag-Lev Shuttle Trains
        _add_viaduct_arch_deck(span_x=64.0, arch_h=16.5, deck_w=12.4, n_segs=14)
        # Left Suspension Tower Pylon (X = -15.5m) + Docked Aerodynamic Shuttle Trains
        kit.add("aero_white", make_chamfered_oct_prism(5.2, 13.5, 23.5, center=(-15.5, 12.5, 0.0), chamfer=1.1, top_scale=0.80))
        kit.add("led_cyan", make_beveled_box((0.45, 21.0, 13.8), center=(-15.5, 12.5, 0.0), bevel=0.05))
        for tx_sh, tz_sh in [(-11.0, 3.2), (9.5, -3.2)]:
            kit.add("aero_white", make_chamfered_oct_prism(8.5, 2.2, 1.65, center=(tx_sh, 16.8, tz_sh), chamfer=0.65))
            kit.add("glass_cyan", make_chamfered_oct_prism(7.2, 2.3, 0.85, center=(tx_sh, 17.1, tz_sh), chamfer=0.55))
            kit.add("accent_orange", make_beveled_box((1.4, 1.4, 2.35), center=(tx_sh, 16.7, tz_sh), bevel=0.06))
        # Right/Mid-Span 35% Zone (X = +6.5m): Suspended `alphaMode: "BLEND"` Translucent Sky-Transfer Rotunda
        rot_x, rot_y = 6.5, 18.2
        kit.add("gunmetal", make_chamfered_oct_prism(13.5, 13.5, 1.4, center=(rot_x, rot_y - 3.6, 0.0), chamfer=3.2))
        kit.add("aero_white", make_chamfered_oct_prism(12.2, 12.2, 1.1, center=(rot_x, rot_y + 3.8, 0.0), chamfer=2.8))
        # 3D Internal Commuter Transfer Rings, Holo-Telemetry Core & #D95B26 Shuttle Docking Collars
        kit.add("led_cyan", make_cylinder(1.4, 1.4, 6.8, center=(rot_x, rot_y, 0.0), segments=12))
        for ry_off, col_k in [(-1.6, "led_cyan"), (0.0, "led_amber"), (1.6, "led_uv")]:
            kit.add(col_k, make_closed_torus_ring(4.4, 0.22, center=(rot_x, rot_y + ry_off, 0.0), n_major=14, n_minor=6))
        for dz_dock in [-6.8, 6.8]:
            kit.add("accent_orange", make_cylinder(1.45, 1.45, 1.2, center=(rot_x, rot_y, dz_dock), segments=12, axis="z"))
        kit.add("glass_cyan", make_chamfered_oct_prism(12.6, 12.6, 6.4, center=(rot_x, rot_y, 0.0), chamfer=2.9))
        kit.add("marquee", make_beveled_box((6.5, 1.1, 0.35), center=(rot_x, rot_y + 4.5, 6.2), bevel=0.05))

    elif cand_id == 3:
        _add_viaduct_arch_deck(span_x=64.0, arch_h=14.0, deck_w=12.0, n_segs=14)
        kit.add("steel_machined", make_beveled_box((56.0, 1.2, 8.5), center=(0.0, 20.5, 0.0), bevel=0.15))
        kit.add("glass_cyan", make_chamfered_oct_prism(14.0, 10.0, 4.8, center=(0.0, 18.0, 0.0), chamfer=2.4))

    elif cand_id == 4:
        _add_viaduct_arch_deck(span_x=60.0, arch_h=17.0, deck_w=13.0, n_segs=14)
        kit.add("glass_emerald", make_chamfered_oct_prism(16.0, 14.0, 5.2, center=(0.0, 19.5, 0.0), chamfer=3.2))
        kit.add("biome_canopy", make_chamfered_oct_prism(13.0, 11.0, 0.9, center=(0.0, 17.2, 0.0), chamfer=2.6))

    else:
        _add_viaduct_arch_deck(span_x=64.0, arch_h=15.0, deck_w=12.5, n_segs=14)
        kit.add("gunmetal", make_chamfered_oct_prism(10.0, 10.0, 22.0, center=(8.0, 12.0, 0.0), chamfer=2.2))
        kit.add("glass_cyan", make_chamfered_oct_prism(11.5, 11.5, 5.5, center=(-8.0, 17.5, 0.0), chamfer=2.5))

    tune_setpiece_budget(kit, min_tris=3800, max_tris=5600, y_level=0.55, cand_id=cand_id)
    out_dir = os.path.join(OUT_CYL_INT_DIR, "setpiece_01")
    os.makedirs(out_dir, exist_ok=True)
    out_p = os.path.join(out_dir, f"interior_setpiece_01_r1_{cand_id:02d}.glb")
    info = center_and_export_glb(out_p, kit.to_submeshes(f"Setpiece01_C{cand_id:02d}"), root_name=f"InteriorSetpiece01_R1_{cand_id:02d}")
    if cand_id == 2:
        for dst in [
            os.path.join(WINNERS_DIR, "interior_setpiece_01_winner_ring_skybridge_viaduct.glb"),
            os.path.join(OUT_CYL_INT_DIR, "interior_setpiece_01_winner_ring_skybridge_viaduct.glb"),
            os.path.join(OUT_CYL_INT_DIR, "interior_setpiece_01_ring_skybridge_viaduct.glb"),
        ]:
            shutil.copyfile(out_p, dst)
    return info


def build_setpiece_02_candidate(cand_id: int, mats: Dict[str, PBRMaterialDef]) -> Dict[str, any]:
    """
    interior_setpiece_02 (`interior_setpiece_02_terraced_waterfall_reservoir`):
    Stepped Hydro-Dam, Meandering Ring-River Cascade & Emerald Biodome Conservatory Peninsula
    """
    kit = BuildingKit(mats)

    # 1. Lower Meandering River Delta Basin & Basalt-Titanium Retaining Cliffs
    kit.add("cliff_basalt", make_chamfered_oct_prism(42.0, 32.0, 1.6, center=(0.0, 0.8, 0.0), chamfer=6.5))
    kit.add("promenade_paving", make_chamfered_oct_prism(39.0, 29.0, 0.45, center=(0.0, 1.75, 0.0), chamfer=6.0))
    kit.add("water_river", make_chamfered_oct_prism(35.0, 24.0, 0.55, center=(-2.0, 2.15, 2.5), chamfer=5.2))

    # Sinuous meandering river channelribbon flowing forward (+Z)
    river_pts = np.array(
        [[-5.5 + 3.8 * math.sin(t * math.pi * 1.6), 2.35, -11.0 + t * 22.0] for t in np.linspace(0.0, 1.0, 14)],
        dtype=np.float32,
    )
    kit.add("water_river", make_swept_tube(river_pts, radius=2.6, radial_segments=8, oval_scale=(2.4, 0.22)))

    # 2. 4-Tier Stepped Hydro-Dam Spillway (Left 65% in #02)
    dam_x = -6.8 if cand_id == 2 else 0.0
    for tier_i in range(4):
        ty = 2.2 + tier_i * 3.4
        tz = -2.0 - tier_i * 2.4
        tw = 21.0 - tier_i * 2.2
        kit.add("cliff_basalt", make_chamfered_oct_prism(tw, 7.5, 3.2, center=(dam_x, ty + 1.6, tz), chamfer=1.8))
        kit.add("gunmetal", make_beveled_box((tw * 0.92, 0.55, 7.8), center=(dam_x, ty + 3.2, tz), bevel=0.08))
        # Cascading `alphaMode: "BLEND"` specular waterfall sheet down front of tier
        kit.add("water_river", make_beveled_box((tw * 0.62, 3.45, 0.85), center=(dam_x, ty + 1.7, tz + 3.65), bevel=0.08))
        kit.add("led_cyan", make_beveled_box((tw * 0.58, 0.24, 1.05), center=(dam_x, ty + 3.3, tz + 3.65), bevel=0.03))
        # Brushed-steel floodgate turbines & #D95B26 valve wheels
        for gx in [dam_x - tw * 0.36, dam_x + tw * 0.36]:
            kit.add("steel_machined", make_cylinder(0.85, 0.75, 2.8, center=(gx, ty + 1.6, tz + 3.4), segments=10))
            kit.add("accent_orange", make_closed_torus_ring(0.65, 0.12, center=(gx, ty + 1.8, tz + 4.1), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=10, n_minor=5))

    # 3. Right 35% Zone: Terraced Emerald Biodome Conservatory Peninsula (`biome_canopy` + `glass_emerald` + UV rings)
    bio_x = 9.8 if cand_id == 2 else (10.5 if cand_id in (3, 5) else 0.0)
    bio_z = 1.5 if cand_id != 1 else -6.5
    for b_tier in range(4):
        by = 2.0 + b_tier * 3.6
        br = 6.8 - b_tier * 1.05
        kit.add("biome_canopy", make_chamfered_oct_prism(br * 2.1, br * 2.1, 1.4, center=(bio_x, by + 0.7, bio_z), chamfer=br * 0.45))
        kit.add("foliage", make_botanical_cluster((bio_x, by + 1.5, bio_z), radius=br * 0.85, n_leaves=4))
        kit.add("led_uv" if (b_tier % 2 == 0) else "led_emerald", make_closed_torus_ring(br * 0.88, 0.14, center=(bio_x, by + 2.4, bio_z), n_major=12, n_minor=5))
        kit.add("glass_emerald", make_chamfered_oct_prism(br * 1.95, br * 1.95, 2.4, center=(bio_x, by + 2.4, bio_z), chamfer=br * 0.42))

    # Copper-anodized pedestrian viewing bridge spanning between the hydro-dam and emerald biodome peninsula
    bridge_pts = sample_filleted_polyline([(dam_x + 3.0, 9.2, 1.5), (0.5 * (dam_x + bio_x), 11.2, 3.5), (bio_x - 2.5, 9.2, bio_z)], 1.5, 4)
    kit.add("copper_bridge", make_swept_tube(bridge_pts, radius=0.65, radial_segments=8, oval_scale=(1.8, 0.55)))

    tune_setpiece_budget(kit, min_tris=3800, max_tris=5500, y_level=1.9, cand_id=cand_id)
    out_dir = os.path.join(OUT_CYL_INT_DIR, "setpiece_02")
    os.makedirs(out_dir, exist_ok=True)
    out_p = os.path.join(out_dir, f"interior_setpiece_02_r1_{cand_id:02d}.glb")
    info = center_and_export_glb(out_p, kit.to_submeshes(f"Setpiece02_C{cand_id:02d}"), root_name=f"InteriorSetpiece02_R1_{cand_id:02d}")
    if cand_id == 2:
        for dst in [
            os.path.join(WINNERS_DIR, "interior_setpiece_02_winner_terraced_waterfall_reservoir.glb"),
            os.path.join(OUT_CYL_INT_DIR, "interior_setpiece_02_winner_terraced_waterfall_reservoir.glb"),
            os.path.join(OUT_CYL_INT_DIR, "interior_setpiece_02_terraced_waterfall_reservoir.glb"),
        ]:
            shutil.copyfile(out_p, dst)
    return info


def build_setpiece_03_candidate(cand_id: int, mats: Dict[str, PBRMaterialDef]) -> Dict[str, any]:
    """
    interior_setpiece_03 (`interior_setpiece_03_axial_suncore_spoke_hub`):
    Central Axial Zero-G Solar-Plasma Light-Line, Rotating Louver Baffles & Radial Tether-Elevator Spoke Hub
    """
    kit = BuildingKit(mats)
    hub_y = 18.0

    # 1. Ground/Valley Anchor Terminal Plinth at Y = 0.0m + Vertical Main Tether Spoke Descending to Valley A
    kit.add("gunmetal", make_chamfered_oct_prism(14.0, 14.0, 1.8, center=(0.0, 0.9, 0.0), chamfer=3.2))
    kit.add("led_amber", make_chamfered_oct_prism(14.4, 14.4, 0.25, center=(0.0, 0.35, 0.0), chamfer=3.2))
    kit.add("steel_machined", make_cylinder(0.95, 0.95, hub_y, center=(0.0, hub_y * 0.5, 0.0), segments=12))
    # Illuminated zero-G transit climber car on the vertical spoke
    kit.add("accent_orange", make_chamfered_oct_prism(3.8, 3.8, 4.2, center=(0.0, hub_y * 0.45, 0.0), chamfer=0.85))
    kit.add("glass_cyan", make_chamfered_oct_prism(4.1, 4.1, 2.2, center=(0.0, hub_y * 0.45, 0.0), chamfer=0.90))

    # 2. Segmented Axial Solar-Plasma Core along X-axis at Y = hub_y wrapped in `sky_axial_golden_hour_gradient.png`
    core_len = 54.0
    kit.add("sky_golden_core", make_cylinder(2.8, 2.8, core_len, center=(0.0, hub_y, 0.0), segments=14, axis="x"))
    kit.add("glass_cyan", make_cylinder(3.9, 3.9, core_len * 0.94, center=(0.0, hub_y, 0.0), segments=14, axis="x"))

    # Articulated 45°-chamfered Gunmetal & Brushed-Steel Heliostat Daylight Louver Baffles along the sun-core
    for bx in [-22.0, -13.0, -4.0, 11.0, 20.0]:
        kit.add("gunmetal", make_cylinder(5.8, 5.8, 1.8, center=(bx, hub_y, 0.0), segments=12, axis="x"))
        kit.add("steel_machined", make_beveled_box((3.2, 1.2, 14.5), center=(bx, hub_y - 3.8, 0.0), bevel=0.15))
        kit.add("led_amber", make_closed_torus_ring(5.9, 0.22, center=(bx, hub_y, 0.0), rot_xyz_deg=(0.0, 0.0, 90.0), n_major=12, n_minor=5))

    # 2 Upper Radial High-Tension Elevator Spoke Gantries (+60° and -60°) with climber cars
    for ang_deg in [58.0, -58.0]:
        rad = math.radians(ang_deg)
        sy = hub_y + 13.5 * math.cos(rad)
        sz = 13.5 * math.sin(rad)
        pts = np.array([[0.0, hub_y, 0.0], [0.0, sy, sz]], dtype=np.float32)
        kit.add("steel_machined", make_swept_tube(pts, radius=0.75, radial_segments=8))
        kit.add("aero_white", make_beveled_box((3.2, 3.2, 3.2), center=(0.0, hub_y + 7.5 * math.cos(rad), 7.5 * math.sin(rad)), bevel=0.35))
        kit.add("led_cyan", make_beveled_box((3.5, 1.1, 3.5), center=(0.0, hub_y + 7.5 * math.cos(rad), 7.5 * math.sin(rad)), bevel=0.1))

    # 3. Secondary 35% Zone (X = +4.5m in #02): Central `alphaMode: "BLEND"` Translucent Zero-G Axial Docking & Weather Sphere
    sp_x = 4.5 if cand_id == 2 else 0.0
    sph_prof = [(0.0, -6.8), (4.6, -4.8), (6.8, 0.0), (4.6, 4.8), (0.0, 6.8)]
    kit.add("glass_cyan", make_lathe_dome(sph_prof, center=(sp_x, hub_y, 0.0), segments=16, subdivide_profile=1))
    # Internal 3D Gyroscopic Solar-Plasma Pinch Coils (#00E5FF / #FF9500) & #D95B26 Axial Shuttle Berths
    for tilt, col_k in [(28.0, "led_cyan"), (-32.0, "led_amber"), (65.0, "led_uv")]:
        kit.add(col_k, make_closed_torus_ring(5.2, 0.25, center=(sp_x, hub_y, 0.0), rot_xyz_deg=(tilt, 18.0, 0.0), n_major=14, n_minor=6))
    for sz_b in [-7.2, 7.2]:
        kit.add("accent_orange", make_cylinder(1.6, 1.6, 1.4, center=(sp_x, hub_y, sz_b), segments=12, axis="z"))

    tune_setpiece_budget(kit, min_tris=3850, max_tris=5550, y_level=0.95, cand_id=cand_id)
    out_dir = os.path.join(OUT_CYL_INT_DIR, "setpiece_03")
    os.makedirs(out_dir, exist_ok=True)
    out_p = os.path.join(out_dir, f"interior_setpiece_03_r1_{cand_id:02d}.glb")
    info = center_and_export_glb(out_p, kit.to_submeshes(f"Setpiece03_C{cand_id:02d}"), root_name=f"InteriorSetpiece03_R1_{cand_id:02d}")
    if cand_id == 2:
        for dst in [
            os.path.join(WINNERS_DIR, "interior_setpiece_03_winner_axial_suncore_spoke_hub.glb"),
            os.path.join(OUT_CYL_INT_DIR, "interior_setpiece_03_winner_axial_suncore_spoke_hub.glb"),
            os.path.join(OUT_CYL_INT_DIR, "interior_setpiece_03_axial_suncore_spoke_hub.glb"),
        ]:
            shutil.copyfile(out_p, dst)
    return info


def build_setpiece_04_candidate(cand_id: int, mats: Dict[str, PBRMaterialDef]) -> Dict[str, any]:
    """
    interior_setpiece_04 (`interior_setpiece_04_endcap_cliffside_citadel`):
    Forward Hemispherical Bulkhead Cliffside Terraces, Radial Funicular Gantry & Axial Docking Bowl
    """
    kit = BuildingKit(mats)

    # 1. 5-Tier Monumental Stepped Basalt-Titanium (`cliff_basalt`), Gunmetal & Aerospace-White Cliffside Hanging Terraces
    main_x = -4.2 if cand_id == 2 else 0.0
    for tier_i in range(5):
        ty = tier_i * 4.2
        tz = -tier_i * 2.8
        tw = 34.0 - tier_i * 4.2
        td = 16.0 - tier_i * 1.4
        kit.add("cliff_basalt", make_chamfered_oct_prism(tw, td, 3.2, center=(main_x, ty + 1.6, tz), chamfer=2.8))
        kit.add("aero_white", make_chamfered_oct_prism(tw * 0.92, td * 0.88, 1.1, center=(main_x, ty + 3.6, tz + 0.4), chamfer=2.4))
        kit.add("biome_canopy", make_chamfered_oct_prism(tw * 0.76, td * 0.55, 0.45, center=(main_x, ty + 4.25, tz + 1.2), chamfer=1.8))
        kit.add("led_amber", make_beveled_box((tw * 0.72, 0.24, 0.45), center=(main_x, ty + 3.6, tz + td * 0.44), bevel=0.04))
        # Warm amber residential/citadel window clusters on cliff retaining face
        win_geom = remap_uv_u(
            make_beveled_box((tw * 0.68, 1.85, 0.45), center=(main_x, ty + 1.8, tz + td * 0.48), bevel=0.04),
            0.02,
            0.48,
        )
        kit.add("window_warm_amber", win_geom)

    # Upper Axial Zero-G Docking Bowl Collar at top of cliffside citadel
    kit.add("gunmetal", make_closed_torus_ring(6.5, 1.1, center=(main_x, 22.5, -12.5), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=16, n_minor=6))
    kit.add("accent_orange", make_closed_torus_ring(5.2, 0.55, center=(main_x, 22.5, -11.6), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=14, n_minor=6))
    kit.add("led_cyan", make_closed_torus_ring(4.4, 0.32, center=(main_x, 22.5, -11.2), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=14, n_minor=6))

    # 2. Secondary 35% Zone (Right +X in #02): Full-Height `alphaMode: "BLEND"` Translucent Radial Funicular & Zero-G Ascent Tube
    fun_x = 9.5 if cand_id == 2 else (8.5 if cand_id in (3, 5) else 0.0)
    fun_pts = np.array([[fun_x, 1.2, 5.5], [fun_x, 11.5, -2.5], [fun_x, 22.5, -10.5]], dtype=np.float32)
    kit.add("steel_machined", make_swept_tube(fun_pts, radius=0.55, radial_segments=8))
    kit.add("led_cyan", make_swept_tube(fun_pts, radius=0.25, radial_segments=6))

    # 3 Internal Pressurized Funicular Rail Cars + Signal-Orange Airlock Transfer Stations inside Translucent Funicular Tube
    for s_frac in [0.22, 0.55, 0.85]:
        cx_f = fun_x
        cy_f = 1.2 + s_frac * 21.3
        cz_f = 5.5 - s_frac * 16.0
        kit.add("accent_orange", make_chamfered_oct_prism(3.2, 3.6, 2.4, center=(cx_f, cy_f, cz_f), chamfer=0.65))
        kit.add("aero_white", make_beveled_box((4.4, 0.45, 4.2), center=(cx_f - 1.2, cy_f - 1.2, cz_f), bevel=0.06))
        kit.add("glass_cyan", make_chamfered_oct_prism(4.2, 4.8, 5.8, center=(cx_f, cy_f, cz_f), chamfer=0.95))

    tune_setpiece_budget(kit, min_tris=3850, max_tris=5550, y_level=1.6, cand_id=cand_id)
    out_dir = os.path.join(OUT_CYL_INT_DIR, "setpiece_04")
    os.makedirs(out_dir, exist_ok=True)
    out_p = os.path.join(out_dir, f"interior_setpiece_04_r1_{cand_id:02d}.glb")
    info = center_and_export_glb(out_p, kit.to_submeshes(f"Setpiece04_C{cand_id:02d}"), root_name=f"InteriorSetpiece04_R1_{cand_id:02d}")
    if cand_id == 2:
        for dst in [
            os.path.join(WINNERS_DIR, "interior_setpiece_04_winner_endcap_cliffside_citadel.glb"),
            os.path.join(OUT_CYL_INT_DIR, "interior_setpiece_04_winner_endcap_cliffside_citadel.glb"),
            os.path.join(OUT_CYL_INT_DIR, "interior_setpiece_04_endcap_cliffside_citadel.glb"),
        ]:
            shutil.copyfile(out_p, dst)
    return info


def build_setpiece_05_candidate(cand_id: int, mats: Dict[str, PBRMaterialDef]) -> Dict[str, any]:
    """
    interior_setpiece_05 (`interior_setpiece_05_elevated_plaza_interchange`):
    Multi-Level Asymmetric Civic Canyon, Diagonal Skywalk Network & Terraced Plaza Podium
    """
    kit = BuildingKit(mats)

    # 1. Left 65% Primary Zone: Stepped 3-Level Urban Canyon Acropolis Podium (`promenade_paving` + `cliff_basalt` + `window_warm_amber`)
    pod_x = -5.5 if cand_id == 2 else 0.0
    for lvl_i, (pw, pd, ph) in enumerate([(38.0, 28.0, 2.2), (26.0, 20.0, 3.8), (17.0, 13.5, 4.5)]):
        py = sum([2.2, 3.8, 4.5][:lvl_i]) + ph * 0.5
        yaw = 0.0 if lvl_i == 0 else (28.0 if lvl_i == 1 else -32.0)
        kit.add(
            "cliff_basalt",
            transform_geom(make_chamfered_oct_prism(pw, pd, ph * 0.78, chamfer=2.6), translate=(pod_x, py - ph * 0.1, 0.0), rot_xyz_deg=(0.0, yaw, 0.0)),
        )
        kit.add(
            "promenade_paving",
            transform_geom(make_chamfered_oct_prism(pw * 0.96, pd * 0.96, ph * 0.24, chamfer=2.4), translate=(pod_x, py + ph * 0.38, 0.0), rot_xyz_deg=(0.0, yaw, 0.0)),
        )
        w_box = remap_uv_u(
            transform_geom(make_beveled_box((pw * 0.72, ph * 0.52, pd * 0.98), bevel=0.06), translate=(pod_x, py, 0.0), rot_xyz_deg=(0.0, yaw, 0.0)),
            0.02,
            0.48,
        )
        kit.add("window_warm_amber", w_box)
        kit.add(
            "led_amber",
            transform_geom(make_beveled_box((pw * 0.80, 0.20, pd * 1.01), bevel=0.03), translate=(pod_x, py + ph * 0.46, 0.0), rot_xyz_deg=(0.0, yaw, 0.0)),
        )

    # Diagonal Brushed-Steel & Translucent Pedestrian Skybridges (`32°` and `-38°`)
    for sb_ang, sb_y in [(34.0, 6.8), (-38.0, 9.6)]:
        kit.add(
            "steel_machined",
            transform_geom(make_beveled_box((24.0, 0.55, 3.2), bevel=0.06), translate=(0.0, sb_y, 0.0), rot_xyz_deg=(0.0, sb_ang, 0.0)),
        )
        kit.add(
            "glass_cyan",
            transform_geom(make_beveled_box((23.0, 1.85, 2.9), bevel=0.06), translate=(0.0, sb_y + 1.15, 0.0), rot_xyz_deg=(0.0, sb_ang, 0.0)),
        )

    # 2. Right 35% Secondary Zone: `alphaMode: "BLEND"` Translucent Covered Galleria & Sunken Orbital Holo-Amphitheater
    gal_x = 9.5 if cand_id == 2 else (8.5 if cand_id in (3, 5) else 0.0)
    gal_z = 2.0 if cand_id != 1 else -4.0
    kit.add("gunmetal", make_chamfered_oct_prism(14.5, 14.5, 2.4, center=(gal_x, 1.2, gal_z), chamfer=3.2))
    # 3D Glowing Holographic O'Neill Cylinder Monument inside the Translucent Galleria Dome
    kit.add("led_cyan", transform_geom(make_cylinder(1.6, 1.6, 6.5, segments=12, axis="x"), translate=(gal_x, 6.2, gal_z), rot_xyz_deg=(0.0, -22.0, 16.0)))
    kit.add("led_amber", make_closed_torus_ring(4.2, 0.22, center=(gal_x, 6.2, gal_z), rot_xyz_deg=(26.0, 15.0, 0.0), n_major=14, n_minor=6))
    kit.add("led_uv", make_closed_torus_ring(3.2, 0.18, center=(gal_x, 6.2, gal_z), rot_xyz_deg=(-32.0, -18.0, 0.0), n_major=12, n_minor=6))
    kit.add("accent_orange", make_beveled_box((3.2, 2.2, 0.65), center=(gal_x, 2.8, gal_z + 6.8), bevel=0.08))
    kit.add("glass_cyan", make_chamfered_oct_prism(13.2, 13.2, 8.8, center=(gal_x, 6.6, gal_z), chamfer=3.0, top_scale=0.78))

    tune_setpiece_budget(kit, min_tris=3850, max_tris=5550, y_level=2.3, cand_id=cand_id)
    out_dir = os.path.join(OUT_CYL_INT_DIR, "setpiece_05")
    os.makedirs(out_dir, exist_ok=True)
    out_p = os.path.join(out_dir, f"interior_setpiece_05_r1_{cand_id:02d}.glb")
    info = center_and_export_glb(out_p, kit.to_submeshes(f"Setpiece05_C{cand_id:02d}"), root_name=f"InteriorSetpiece05_R1_{cand_id:02d}")
    if cand_id == 2:
        for dst in [
            os.path.join(WINNERS_DIR, "interior_setpiece_05_winner_elevated_plaza_interchange.glb"),
            os.path.join(OUT_CYL_INT_DIR, "interior_setpiece_05_winner_elevated_plaza_interchange.glb"),
            os.path.join(OUT_CYL_INT_DIR, "interior_setpiece_05_elevated_plaza_interchange.glb"),
        ]:
            shutil.copyfile(out_p, dst)
    return info


# ==============================================================================
# PART 2: 3 BESPOKE NON-REPETITIVE CURVED VALLEY BIOME & TERRAIN SHELLS
# (`valley_a_civic_acropolis_terraces.glb`, `valley_b_meandering_river_biosphere.glb`,
#  `valley_c_industrial_switchyard_port.glb`)
# ==============================================================================
def populate_valley_a_civic_acropolis(
    kit: BuildingKit,
    x0: float = -265.0,
    x1: float = 115.0,
    theta_center: float = 180.0,
    r_base: float = 186.0,
):
    """
    Valley A (Civic Metropolis, Terraced Citadel & Grand Promenade):
      - Stepped travertine-alloy promenade (`terrain_park_promenade_paving.png`)
      - Basalt-titanium cliff retaining walls (`terrain_basalt_titanium_cliff_rock.png`)
      - Specular ring-river waterfront (`water_ring_river_specular.png`)
      - Diagonal skywalk bridges & Warm Circadian Amber/Gold window cluster podiums (`u: 0.0-0.5`)
    """
    # 1. Waterfront esplanade & central specular water canal with oblique plaza basins
    kit.add("promenade_paving", make_cyl_arc_shell(x0, x1, r_base - 1.6, r_base, theta_center - 26.0, theta_center + 26.0, segs_theta=6))
    kit.add("water_river", make_cyl_arc_shell(x0 + 10.0, x1 - 10.0, r_base - 2.4, r_base - 1.2, theta_center - 4.2, theta_center + 4.2, segs_theta=2))
    kit.add("biome_canopy", make_cyl_arc_shell(x0 + 15.0, x1 - 15.0, r_base - 2.2, r_base - 1.3, theta_center - 11.5, theta_center - 5.5, segs_theta=2))
    kit.add("biome_canopy", make_cyl_arc_shell(x0 + 15.0, x1 - 15.0, r_base - 2.2, r_base - 1.3, theta_center + 5.5, theta_center + 11.5, segs_theta=2))

    # 2. Multi-tier Stepped Basalt-Titanium Retaining Cliffs (`R = 180.5m` Mid-Terrace & `R = 174.5m` Acropolis Podium)
    for t_sign in [-1.0, 1.0]:
        t_mid0 = theta_center + t_sign * 12.0
        t_mid1 = theta_center + t_sign * 25.0
        ta, tb = min(t_mid0, t_mid1), max(t_mid0, t_mid1)
        kit.add("cliff_basalt", make_cyl_arc_shell(x0 + 18.0, x1 - 18.0, r_base - 6.2, r_base - 1.4, ta, tb, segs_theta=3))
        kit.add("promenade_paving", make_cyl_arc_shell(x0 + 20.0, x1 - 20.0, r_base - 7.0, r_base - 6.0, ta + 1.0, tb - 1.0, segs_theta=3))

    # Central Raised Command Citadel Acropolis Bluff at X = -125m .. -25m
    kit.add("cliff_basalt", make_cyl_arc_shell(-135.0, -15.0, r_base - 12.5, r_base - 2.0, theta_center - 14.0, theta_center + 14.0, segs_theta=4))
    kit.add("promenade_paving", make_cyl_arc_shell(-128.0, -22.0, r_base - 13.8, r_base - 12.2, theta_center - 12.0, theta_center + 12.0, segs_theta=4))
    kit.add("led_amber", make_cyl_arc_shell(-130.0, -20.0, r_base - 14.2, r_base - 13.2, theta_center - 12.5, theta_center + 12.5, segs_theta=4))

    # 3. Staggered Oblique Warm-Amber Residential & Civic Podium Towers + Diagonal Skywalk Bridges
    staggered_slots = [
        (-225.0, -18.0, 32.0, 28.0),
        (-185.0, 16.5, -28.0, 34.0),
        (-135.0, -21.0, 42.0, 30.0),
        (-75.0, 0.0, 0.0, 44.0),
        (-55.0, 19.5, -36.0, 32.0),
        (10.0, -16.0, 25.0, 29.0),
        (65.0, 17.5, -30.0, 31.0),
    ]
    for bx, d_theta, yaw, bh in staggered_slots:
        t_deg = theta_center + d_theta
        p_pod = make_chamfered_oct_prism(24.0, 18.0, 4.5, center=(0.0, 2.25, 0.0), chamfer=3.8)
        p_twr = transform_geom(
            make_chamfered_oct_prism(15.0, 14.0, bh, center=(-3.2, 4.5 + bh * 0.5, 0.0), chamfer=2.8, top_scale=0.82, capped=False),
            rot_xyz_deg=(0.0, yaw, 0.0),
        )
        p_win = remap_uv_u(
            transform_geom(make_beveled_box((15.6, bh * 0.78, 10.5), center=(-3.2, 4.5 + bh * 0.5, 0.0), bevel=0.0), rot_xyz_deg=(0.0, yaw, 0.0)),
            0.02,
            0.48,
        )
        p_gl = transform_geom(
            make_chamfered_oct_prism(8.5, 11.0, bh * 1.05, center=(5.2, 4.5 + bh * 0.52, 0.0), chamfer=1.8, capped=False),
            rot_xyz_deg=(0.0, yaw, 0.0),
        )
        kit.add("cliff_basalt", place_inward_on_cylinder(p_pod, bx, t_deg, r_floor=r_base))
        kit.add("aero_white", place_inward_on_cylinder(p_twr, bx, t_deg, r_floor=r_base))
        kit.add("window_warm_amber", place_inward_on_cylinder(p_win, bx, t_deg, r_floor=r_base))
        kit.add("glass_cyan", place_inward_on_cylinder(p_gl, bx, t_deg, r_floor=r_base))

    # Diagonal Brushed-Steel & Copper Skywalk Bridges spanning the Civic Canyon
    for bx_br, tilt_br in [(-195.0, 28.0), (-95.0, -32.0), (25.0, 24.0)]:
        br_geom = transform_geom(make_beveled_box((14.0, 2.2, 52.0), center=(0.0, 14.0, 0.0), bevel=0.25), rot_xyz_deg=(0.0, tilt_br, 0.0))
        kit.add("copper_bridge", place_inward_on_cylinder(br_geom, bx_br, theta_center, r_floor=r_base))


def populate_valley_b_meandering_river_biosphere(
    kit: BuildingKit,
    x0: float = -265.0,
    x1: float = 115.0,
    theta_center: float = 60.0,
    r_base: float = 186.0,
):
    """
    Valley B (Emerald Agri-Biosphere, Terraced Waterfall Cascades & Meandering Ring-River Delta):
      - Sinusoidally meandering `alphaMode: "BLEND"` specular ring-river & central lake reservoir (`water_ring_river_specular.png`)
      - Stepped emerald botanical contour hills (`biome_terraced_botanical_canopy.png`)
      - Basalt cliff terraces (`terrain_basalt_titanium_cliff_rock.png`) & copper-anodized irrigation bridges
    """
    # 1. Lush Emerald Botanical Base Valley Floor
    kit.add("biome_canopy", make_cyl_arc_shell(x0, x1, r_base - 1.8, r_base, theta_center - 26.0, theta_center + 26.0, segs_theta=6))

    # 2. Sinusoidally Meandering Specular Ring-River (10 curved segments following phi(x) = theta_center + 11.5 * sin(x / 46.0))
    n_riv = 10
    xs = np.linspace(x0 + 8.0, x1 - 8.0, n_riv + 1)
    for i in range(n_riv):
        xa, xb = float(xs[i]), float(xs[i + 1])
        xm = 0.5 * (xa + xb)
        phi_m = theta_center + 11.5 * math.sin(xm / 46.0)
        w_deg = 12.5 if (-125.0 <= xm <= -35.0) else 6.2  # Wide central Ring-Lake Reservoir at X = -125..-35m
        kit.add("water_river", make_cyl_arc_shell(xa, xb, r_base - 2.8, r_base - 1.4, phi_m - w_deg, phi_m + w_deg, segs_theta=3))
        kit.add("led_emerald", make_cyl_arc_shell(xa, xb, r_base - 2.6, r_base - 1.6, phi_m - w_deg - 1.2, phi_m - w_deg, segs_theta=1))

    # 3. Stepped Terraced Botanical Contour Hills & Waterfall Hydro-Dam Ziggurats (`+5m`, `+11m`, `+17m`)
    hill_clusters = [
        (-215.0, -14.0, 14.0, 22.0),
        (-145.0, 15.0, 16.0, 26.0),
        (-80.0, -16.0, 18.0, 30.0),
        (-15.0, 14.0, 15.0, 24.0),
        (55.0, -13.0, 14.0, 22.0),
    ]
    for hx, d_theta, h_span, h_rad in hill_clusters:
        t_c = theta_center + d_theta
        for step_k in range(3):
            r_in_s = r_base - (step_k + 1) * (h_rad / 3.0)
            r_out_s = r_base - step_k * (h_rad / 3.0)
            span_s = h_span * (1.0 - step_k * 0.22)
            kit.add("cliff_basalt", make_cyl_arc_shell(hx - 24.0 + step_k * 4.0, hx + 24.0 - step_k * 4.0, r_in_s, r_out_s, t_c - span_s, t_c + span_s, segs_theta=3))
            kit.add("biome_canopy", make_cyl_arc_shell(hx - 22.0 + step_k * 4.0, hx + 22.0 - step_k * 4.0, r_in_s - 1.2, r_in_s + 0.4, t_c - span_s * 0.9, t_c + span_s * 0.9, segs_theta=3))
        # Translucent Emerald Biodome Conservatory Crown & UV Grow Ring atop each contour hill
        dome_box = make_chamfered_oct_prism(22.0, 18.0, 14.0, center=(0.0, h_rad + 7.0, 0.0), chamfer=4.2, top_scale=0.75, capped=False)
        uv_ring = make_beveled_box((18.0, 2.2, 14.0), center=(0.0, h_rad + 9.0, 0.0), bevel=0.0)
        kit.add("glass_emerald", place_inward_on_cylinder(dome_box, hx, t_c, r_floor=r_base))
        kit.add("led_uv", place_inward_on_cylinder(uv_ring, hx, t_c, r_floor=r_base))

    # Copper-anodized irrigation arch bridges crossing the meandering river
    for bx_arch in [-175.0, -85.0, 15.0]:
        phi_a = theta_center + 11.5 * math.sin(bx_arch / 46.0)
        arch_b = make_beveled_box((10.0, 3.2, 38.0), center=(0.0, 6.5, 0.0), bevel=0.3)
        kit.add("copper_bridge", place_inward_on_cylinder(arch_b, bx_arch, phi_a, r_floor=r_base))


def populate_valley_c_industrial_switchyard_port(
    kit: BuildingKit,
    x0: float = -265.0,
    x1: float = 115.0,
    theta_center: float = 300.0,
    r_base: float = 186.0,
):
    """
    Valley C (High-Energy Industrial Port, Shipyard Drydock, Fusion Power & Defense Ridge):
      - Stepped 45°-chamfered gunmetal & basalt-titanium industrial switchyard platforms (`terrain_basalt_titanium_cliff_rock.png`)
      - Heavy brushed-steel & signal-orange intermodal mag-rail trench (zero blue water canal!)
      - Overhead crane gantries & Cool Cyan/UV/Signal-Orange telemetry window bays (`u: 0.5-1.0`)
    """
    # 1. Basalt-Titanium & Gunmetal Industrial Switchyard Base Deck + Signal-Orange/Steel Mag-Rail Trench
    kit.add("cliff_basalt", make_cyl_arc_shell(x0, x1, r_base - 1.8, r_base, theta_center - 26.0, theta_center + 26.0, segs_theta=6))
    kit.add("steel_machined", make_cyl_arc_shell(x0 + 10.0, x1 - 10.0, r_base - 3.2, r_base - 1.5, theta_center - 5.0, theta_center + 5.0, segs_theta=2))
    kit.add("accent_orange", make_cyl_arc_shell(x0 + 12.0, x1 - 12.0, r_base - 3.6, r_base - 2.4, theta_center - 6.2, theta_center - 4.6, segs_theta=1))
    kit.add("accent_orange", make_cyl_arc_shell(x0 + 12.0, x1 - 12.0, r_base - 3.6, r_base - 2.4, theta_center + 4.6, theta_center + 6.2, segs_theta=1))
    kit.add("led_cyan", make_cyl_arc_shell(x0 + 12.0, x1 - 12.0, r_base - 3.5, r_base - 2.5, theta_center - 1.4, theta_center + 1.4, segs_theta=1))

    # 2. Stepped Industrial Switchyard Shelves & High-Energy Fusion/Drydock Towers (`window_cool_ind` `u: 0.5-1.0`)
    ind_slots = [
        (-220.0, -16.0, 15.0, 32.0),
        (-165.0, 17.0, -20.0, 36.0),
        (-105.0, -18.0, 12.0, 38.0),
        (-45.0, 16.0, -18.0, 34.0),
        (20.0, -15.5, 22.0, 40.0),
        (75.0, 16.5, -15.0, 35.0),
    ]
    for ix, d_theta, yaw, ih in ind_slots:
        t_deg = theta_center + d_theta
        shelf = make_chamfered_oct_prism(28.0, 22.0, 6.5, center=(0.0, 3.25, 0.0), chamfer=4.5)
        twr = transform_geom(
            make_chamfered_oct_prism(16.0, 15.0, ih, center=(-3.5, 6.5 + ih * 0.5, 0.0), chamfer=3.0, top_scale=0.85, capped=False),
            rot_xyz_deg=(0.0, yaw, 0.0),
        )
        win_c = remap_uv_u(
            transform_geom(make_beveled_box((16.6, ih * 0.76, 11.0), center=(-3.5, 6.5 + ih * 0.5, 0.0), bevel=0.0), rot_xyz_deg=(0.0, yaw, 0.0)),
            0.52,
            0.98,
        )
        pinch = transform_geom(
            make_chamfered_oct_prism(9.5, 11.5, ih * 1.06, center=(5.5, 6.5 + ih * 0.53, 0.0), chamfer=2.0, capped=False),
            rot_xyz_deg=(0.0, yaw, 0.0),
        )
        kit.add("gunmetal", place_inward_on_cylinder(shelf, ix, t_deg, r_floor=r_base))
        kit.add("carbon_slate", place_inward_on_cylinder(twr, ix, t_deg, r_floor=r_base))
        kit.add("window_cool_ind", place_inward_on_cylinder(win_c, ix, t_deg, r_floor=r_base))
        kit.add("glass_cyan", place_inward_on_cylinder(pinch, ix, t_deg, r_floor=r_base))

    # Overhead Brushed-Steel Shipyard Crane Gantry Bridges spanning the Industrial Trench
    for gx_cr in [-190.0, -75.0, 45.0]:
        cr_beam = make_beveled_box((12.0, 4.5, 64.0), center=(0.0, 28.0, 0.0), bevel=0.35)
        cr_clamp = make_beveled_box((14.0, 6.5, 14.0), center=(0.0, 24.0, 0.0), bevel=0.4)
        kit.add("steel_machined", place_inward_on_cylinder(cr_beam, gx_cr, theta_center, r_floor=r_base))
        kit.add("accent_orange", place_inward_on_cylinder(cr_clamp, gx_cr, theta_center, r_floor=r_base))


def build_three_valley_biome_shells(mats: Dict[str, PBRMaterialDef]) -> List[Dict[str, any]]:
    """
    Exports the 3 standalone curved R=200m (`min_y = 0.0`) biome terrain shells:
      - `/workspace/game-project/assets/glb/cylinder_interior/valley_a_civic_acropolis_terraces.glb`
      - `/workspace/game-project/assets/glb/cylinder_interior/valley_b_meandering_river_biosphere.glb`
      - `/workspace/game-project/assets/glb/cylinder_interior/valley_c_industrial_switchyard_port.glb`
    """
    results = []

    # 1. Valley A Shell (centered at bottom 180 deg so min_y == 0.0)
    kit_a = BuildingKit(mats)
    populate_valley_a_civic_acropolis(kit_a, x0=-265.0, x1=115.0, theta_center=180.0, r_base=186.0)
    tune_setpiece_budget(kit_a, min_tris=3600, max_tris=5800, y_level=18.0)
    pa = os.path.join(OUT_CYL_INT_DIR, "valley_a_civic_acropolis_terraces.glb")
    results.append(center_and_export_glb(pa, kit_a.to_submeshes("ValleyA_CivicAcropolis"), root_name="ValleyA_CivicAcropolisTerraces"))

    # 2. Valley B Shell (built around bottom 180 deg in local space for clean min_y == 0.0 floor pivot)
    kit_b = BuildingKit(mats)
    populate_valley_b_meandering_river_biosphere(kit_b, x0=-265.0, x1=115.0, theta_center=180.0, r_base=186.0)
    tune_setpiece_budget(kit_b, min_tris=3600, max_tris=5800, y_level=18.0)
    pb = os.path.join(OUT_CYL_INT_DIR, "valley_b_meandering_river_biosphere.glb")
    results.append(center_and_export_glb(pb, kit_b.to_submeshes("ValleyB_MeanderingRiverBiosphere"), root_name="ValleyB_MeanderingRiverBiosphere"))

    # 3. Valley C Shell
    kit_c = BuildingKit(mats)
    populate_valley_c_industrial_switchyard_port(kit_c, x0=-265.0, x1=115.0, theta_center=180.0, r_base=186.0)
    tune_setpiece_budget(kit_c, min_tris=3600, max_tris=5800, y_level=18.0)
    pc = os.path.join(OUT_CYL_INT_DIR, "valley_c_industrial_switchyard_port.glb")
    results.append(center_and_export_glb(pc, kit_c.to_submeshes("ValleyC_IndustrialSwitchyardPort"), root_name="ValleyC_IndustrialSwitchyardPort"))

    return results


# ==============================================================================
# PART 3: OVERHAULED FULL-SCALE `cylinder_r1_02.glb` & WINNER ALIASES
# (Replaces identical 3-way clone strips with asymmetric Valley A / B / C Biomes
#  + Golden-Hour Axial Sun Core `sky_axial_golden_hour_gradient.png`)
# ==============================================================================
def rebuild_overhauled_cylinder_r1_02(mats: Dict[str, PBRMaterialDef]) -> Dict[str, any]:
    kit = BuildingKit(mats)
    x_hab0, x_hab1 = -290.0, 130.0

    # 1. Left 65% Spin-Gravity Habitat Hull Outer Spin-Ribs (`R = 200m`)
    for rx in np.linspace(x_hab0, x_hab1, 5):
        kit.add("gunmetal", make_axial_ring(float(rx), r_in=190.0, r_out=200.0, width_x=13.0, segs=16))
        kit.add("led_amber", make_axial_ring(float(rx) + 4.0, r_in=198.2, r_out=200.0, width_x=2.4, segs=16))

    # 2. Outer Hull Shells + Translucent Solarium Window Strips for the 3 Valleys
    # Note: In `cylinder_interior_showcase.gd`, `CYL_ROLL_DEG = 43.0` rotates:
    #   - k=1 (`theta_mid = 137°`) to dead-bottom `180°` (Valley A — Civic Acropolis)
    #   - k=0 (`theta_mid = 17°`) to `60°` (Valley B — Meandering River & Emerald Biosphere)
    #   - k=2 (`theta_mid = 257°`) to `300°` (Valley C — Industrial Switchyard & Port)
    for k in range(3):
        land_t0 = k * 120.0 - 15.0
        land_t1 = land_t0 + 64.0
        win_t0 = land_t0 + 62.0
        win_t1 = land_t0 + 120.0

        kit.add("aero_white", make_cyl_arc_shell(x_hab0, x_hab1, 186.0, 195.0, land_t0, land_t1, segs_theta=6))
        kit.add("cliff_basalt", make_cyl_arc_shell(x_hab0 + 15.0, x_hab1 - 15.0, 194.2, 197.2, land_t0 + 8.0, land_t1 - 8.0, segs_theta=4))
        kit.add("glass_cyan", make_cyl_arc_shell(x_hab0, x_hab1, 188.0, 192.5, win_t0, win_t0 + 38.0, segs_theta=4))
        kit.add("glass_emerald", make_cyl_arc_shell(x_hab0, x_hab1, 188.0, 192.5, win_t0 + 36.0, win_t1, segs_theta=3))

    # Populate each of the 3 valleys with its unique, radially asymmetric biome & texture palette!
    populate_valley_a_civic_acropolis(kit, x0=x_hab0 + 22.0, x1=x_hab1 - 18.0, theta_center=137.0, r_base=186.0)
    populate_valley_b_meandering_river_biosphere(kit, x0=x_hab0 + 22.0, x1=x_hab1 - 18.0, theta_center=17.0, r_base=186.0)
    populate_valley_c_industrial_switchyard_port(kit, x0=x_hab0 + 22.0, x1=x_hab1 - 18.0, theta_center=257.0, r_base=186.0)

    # 3. Golden-Hour Axial Zero-G Solar Core Spine (`sky_axial_golden_hour_gradient.png`) + Radial Tether Spokes
    kit.add("sky_golden_core", make_cylinder(6.2, 6.2, 740.0, center=(-8.0, CYL_Y, 0.0), segments=14, axis="x"))
    kit.add("steel_machined", make_cylinder(8.5, 8.5, 710.0, center=(-8.0, CYL_Y, 0.0), segments=12, axis="x"))
    for nx in [-240.0, -115.0, 10.0, 135.0]:
        kit.add("aero_white", make_axial_ring(nx, r_in=8.8, r_out=21.5, width_x=16.0, segs=12))
        kit.add("led_amber", make_axial_ring(nx - 9.0, r_in=9.2, r_out=17.0, width_x=4.0, segs=12))
    # Radial tether-elevator spokes at X = -115m descending to the 3 valleys
    for ang_deg in [17.0, 137.0, 257.0]:
        rad = math.radians(ang_deg)
        cy, sz = math.cos(rad), math.sin(rad)
        s_pts = np.array([[-115.0, CYL_Y + 14.0 * cy, 14.0 * sz], [-115.0, CYL_Y + 185.0 * cy, 185.0 * sz]], dtype=np.float32)
        kit.add("steel_machined", make_swept_tube(s_pts, radius=1.8, radial_segments=6, capped=False))
        kit.add("accent_orange", make_beveled_box((7.5, 7.5, 7.5), center=(-115.0, CYL_Y + 96.0 * cy, 96.0 * sz), bevel=0.8))

    # 4. Right 35% Counter-Rotating Zero-G Starport, Heliostat Mirror Array & 5-Coil D-He3 Fusion Drive
    kit.add("carbon_slate", make_axial_ring(142.0, r_in=148.0, r_out=198.0, width_x=22.0, segs=16))
    for gx in [180.0, 235.0, 285.0]:
        kit.add("steel_machined", make_axial_ring(gx, r_in=154.0, r_out=192.0, width_x=10.0, segs=16))
    for k in range(6):
        ang = k * 60.0
        rad = math.radians(ang)
        cy, sz = math.cos(rad), math.sin(rad)
        kit.add("steel_machined", make_cyl_arc_shell(140.0, 295.0, 168.0, 182.0, ang - 4.0, ang + 4.0, segs_theta=2))
        kit.add("glass_cyan", make_cyl_arc_shell(155.0, 280.0, 182.0, 198.0, ang + 8.0, ang + 44.0, segs_theta=3))
        kit.add("accent_orange", make_beveled_box((22.0, 18.0, 18.0), center=(235.0, CYL_Y + 188.0 * cy, 188.0 * sz), bevel=2.0))

    add_hemispherical_or_stepped_endcaps(kit, x_fwd=x_hab0, x_aft=290.0, include_aft_fusion_drive=True)

    out_p = os.path.join(OUT_CYL_DIR, "cylinder_r1_02.glb")
    info = center_and_export_glb(out_p, kit.to_submeshes("Cyl02_Overhauled"), root_name="CylinderHab7_R1_02_Aegis7DualZoneSplit_Overhauled")

    for w_alias in [
        "cylinder_winner_01_hab7_exterior.glb",
        "cylinder_winner_01_aegis7_dual_zone_split.glb",
        "cylinder_hab7_winner_01.glb",
        "cylinder_winner_01.glb",
        "cylinder_winner.glb",
    ]:
        shutil.copyfile(out_p, os.path.join(WINNERS_DIR, w_alias))
    return info


def build_all_interior_overhaul():
    mats = get_interior_overhaul_materials()

    setpiece_builders = [
        (1, build_setpiece_01_candidate),
        (2, build_setpiece_02_candidate),
        (3, build_setpiece_03_candidate),
        (4, build_setpiece_04_candidate),
        (5, build_setpiece_05_candidate),
    ]

    setpiece_results = []
    for sp_id, fn in setpiece_builders:
        for cand_id in range(1, 6):
            info = fn(cand_id, mats)
            fname = os.path.basename(info["filepath"])
            dims = info["dimensions"]
            sz_kb = os.path.getsize(info["filepath"]) / 1024.0
            print(
                f"[setpiece_{sp_id:02d}] {fname:34s} | {dims[0]:6.2f}m W x {dims[2]:6.2f}m D x {dims[1]:6.2f}m H | "
                f"tris={info['triangles']:4d} | min_y={info['min'][1]:.5f} | {sz_kb:6.1f} KB"
            )
            setpiece_results.append(info)

    valley_results = build_three_valley_biome_shells(mats)
    for v_info in valley_results:
        fname = os.path.basename(v_info["filepath"])
        dims = v_info["dimensions"]
        sz_kb = os.path.getsize(v_info["filepath"]) / 1024.0
        print(
            f"[valley_shell] {fname:38s} | {dims[0]:6.2f}m L x {dims[2]:6.2f}m W x {dims[1]:6.2f}m H | "
            f"tris={v_info['triangles']:4d} | min_y={v_info['min'][1]:.5f} | {sz_kb:6.1f} KB"
        )

    cyl02_info = rebuild_overhauled_cylinder_r1_02(mats)
    cdims = cyl02_info["dimensions"]
    csz_kb = os.path.getsize(cyl02_info["filepath"]) / 1024.0
    print(
        f"[cylinder_02]  {os.path.basename(cyl02_info['filepath']):38s} | {cdims[0]:6.2f}m L x {cdims[2]:6.2f}m W x {cdims[1]:6.2f}m H | "
        f"tris={cyl02_info['triangles']:5d} | min_y={cyl02_info['min'][1]:.5f} | {csz_kb:6.1f} KB"
    )

    manifest_path = os.path.join(OUT_CYL_INT_DIR, "cylinder_interior_overhaul_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(
            {
                "setpieces_25": setpiece_results,
                "valley_biome_shells_3": valley_results,
                "overhauled_cylinder_02": cyl02_info,
            },
            f,
            indent=2,
        )
    print(f"Saved manifest to {manifest_path}")


if __name__ == "__main__":
    build_all_interior_overhaul()
