#!/usr/bin/env python3
"""
Builds the Mid-Key Balanced & Forensic Environmental Storytelling 2-Story Residential Sector
(`preface_residential_sector.glb` & `preface_residential_two_story_block.glb`) per Jared's [t4u], [t6u], & [t8u] directives:
  1. All general walls, floors, ceilings, columns, stairs, and furniture use clean, uniform
     world-space UV scaling (`make_world_uv_box`) mapped ONLY to readable mid-tone architectural
     neutral regions (`UV_WALL_APT`, `UV_WALL_ATRIUM`, `UV_FLOOR_SLATE`, `UV_STEEL_TRIM`,
     `UV_WOOD_WALNUT`, `UV_FABRIC_SLATE`, `UV_PLANTER_STONE`) with ZERO repeating text or decals.
  2. Cohesive Forensic Conspiracy Trail ("The 03:14 UTC Sub-Bus Load Spike & Unit #0204 Re-Designation")
     mapped strictly to dedicated, non-tiled UV regions:
     - CUE-001 (`UV_WORKBENCH_TOP` & `UV_WORKBENCH_PEGBOARD` on `Apartment_Workbench` in Apt 201):
       Blown 3rd capacitor coil (`C3 [BLOWN]`) plasma scorch mark, `A7-0204-MEM // III` scratch tally,
       taped `03:14 UTC B-14` 13.56 MHz / 412 Hz oscilloscope note (`#0204: PUDDLE -> KELVIN`),
       wear-polished forearm rest, and pegboard `D-03 HYDRO [REMOVED]` ghost mark + `RFID BUS TAP` schematic.
     - CUE-002 (`UV_FLOOR_SKID_TRAIL` on `Forensic_Skid_Trail_0204` from East Stairwell into Room 1B):
       Asymmetric single-locked-tread rubber skid mark + glossy violet/cyan cryo-coolant drip trail
       leading through `Open_Portal_1B` to `Kelvin #0204`'s parked position over Sub-Bus B-14 Hatch 04.
     - CUE-003 (`UV_PLACARD_201` .. `UV_PLACARD_1B` on the 4 eye-level doorway placards):
       * `APT 201`: Pried-bezel screwdriver nicks on the left edge + scratched-out `CLR-4 [REVOKED] -> TECH-2 // 13.56MHz`.
       * `RM 1B`: Ghost stenciling bleeding through underneath as `SEC-04 // TELEMETRY RELAY [RESTRICTED // CLR-4 ONLY]`
         + broken security seal stamped `2026-10-19 // 03:14`.
"""
import os
import sys
import math
import json
import shutil
from typing import Dict, List, Tuple, Optional
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glb_builder import (
    transform_geom,
    merge_geometries,
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
from character_aegis7_crew_generator import make_joint_ball
from preface_and_wrist_rfid_generator import (
    GODOT_MODELS_DIR,
    ASSETS_GLB_DIR,
    ENV_DIRS,
    RichPBRMaterial,
    RichPartBucket,
    export_hierarchy_with_animations_glb,
    remap_uv,
    tex_path,
)

# ==============================================================================
# MID-TONE ARCHITECTURAL & FORENSIC UV SUB-RECTS (`residential_atrium_and_apartment_atlas_*.png`)
# ==============================================================================
UV_WALL_APT           = (0.02, 0.48, 0.02, 0.25)   # Warm titanium-putty / light slate grey (#8E949C, rough 0.54)
UV_WALL_ATRIUM        = (0.52, 0.98, 0.02, 0.24)   # Mid-tone slate-putty bulkhead panels (#888E96, rough 0.54)
UV_FLOOR_SLATE        = (0.52, 0.98, 0.26, 0.48)   # Mid-tone slate terrazzo (#626870, worn center rough 0.32 / edge 0.78)
UV_WOOD_WALNUT        = (0.02, 0.23, 0.28, 0.48)   # Warm natural honey-teak / birch-walnut wood (#8A6A4E, rough 0.46)
UV_FABRIC_SLATE       = (0.26, 0.48, 0.28, 0.48)   # Mid-tone woven slate upholstery (#566270, rough 0.72)
UV_STEEL_TRIM         = (0.02, 0.48, 0.52, 0.70)   # Brushed structural steel (#545C66, rough 0.38, met 0.78)
UV_RES_Q3_WIRE        = (0.02, 0.23, 0.75, 0.98)   # Coiled copper/dark-steel spool housing
UV_RES_Q3_BATT        = (0.27, 0.48, 0.75, 0.98)   # Matte slate battery cell housing
UV_PLANTER_STONE      = (0.52, 0.74, 0.51, 0.63)   # Mid-tone planter masonry (#5E656E)

# Dedicated Non-Tiled Forensic Storytelling Sub-Rects (CUE-001, CUE-002)
UV_WORKBENCH_TOP      = (0.755, 0.995, 0.505, 0.635)  # CUE-001A: Blown C3 scorch ring, 03:14 UTC B-14 note, A7-0204-MEM
UV_WORKBENCH_PEGBOARD = (0.512, 0.748, 0.638, 0.720)  # CUE-001B: D-03 HYDRO [REMOVED] ghost mark + RFID BUS TAP diagram
UV_FLOOR_SKID_TRAIL   = (0.755, 0.995, 0.640, 0.720)  # CUE-002: Single-locked-tread skid + cryo-coolant drip trail

# Functional low-intensity light diffuser swatches
UV_LIGHT_WARM         = (0.520, 0.660, 0.728, 0.756)  # 3300K soft warm-white localized task light (#F2D8B3)
UV_LIGHT_CYAN         = (0.682, 0.825, 0.728, 0.756)  # Muted functional cyan (#2E8B9A, emi <= 0.65)
UV_LIGHT_AMBER        = (0.845, 0.984, 0.728, 0.756)  # Muted functional amber (#B87328, emi <= 0.60)

# Isolated Door Placard Sub-Rects (CUE-003 — never overlapped by walls, floors, columns, or trim!)
UV_PLACARD_201        = (0.516, 0.742, 0.762, 0.867)  # APT 201 // CLR-4 [REVOKED] -> TECH-2 (pried bezel)
UV_PLACARD_202        = (0.758, 0.984, 0.762, 0.867)  # APT 202 // QUARTERMASTER (SEC-04 // BUS B-14)
UV_PLACARD_1A         = (0.516, 0.742, 0.883, 0.988)  # RM 1A // LAUNDRY LOUNGE
UV_PLACARD_1B         = (0.758, 0.984, 0.883, 0.988)  # RM 1B // Ghost SEC-04 TELEMETRY RELAY + Broken Seal 03:14


def make_world_uv_box(
    size: Tuple[float, float, float],
    center: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    bevel: float = 0.0,
    uv_rect: Tuple[float, float, float, float] = UV_WALL_ATRIUM,
    tile_m: float = 3.5,
    subdivide_max_m: float = 4.0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Builds an architectural box or subdivided slab with uniform world-space UV scaling
    inside `uv_rect = (u0, u1, v0, v1)`.
    """
    sx, sy, sz = size
    cx, cy, cz = center
    u0, u1, v0, v1 = uv_rect
    du_max = u1 - u0
    dv_max = v1 - v0

    nx = max(1, int(math.ceil(sx / subdivide_max_m))) if sx > subdivide_max_m else 1
    ny = max(1, int(math.ceil(sy / subdivide_max_m))) if sy > subdivide_max_m else 1
    nz = max(1, int(math.ceil(sz / subdivide_max_m))) if sz > subdivide_max_m else 1

    dx, dy, dz = sx / nx, sy / ny, sz / nz
    x_start = cx - 0.5 * sx + 0.5 * dx
    y_start = cy - 0.5 * sy + 0.5 * dy
    z_start = cz - 0.5 * sz + 0.5 * dz

    geoms = []
    for ix in range(nx):
        for iy in range(ny):
            for iz in range(nz):
                sub_c = (x_start + ix * dx, y_start + iy * dy, z_start + iz * dz)
                p, n, uv, idx = make_beveled_box((dx, dy, dz), center=sub_c, bevel=min(bevel, 0.15 * min(dx, dy, dz)))
                uv_new = uv.copy()
                n_quads = min(len(p) // 4, 18 if bevel > 1e-5 else 6)
                for q in range(n_quads):
                    b_i = q * 4
                    w_m = float(np.linalg.norm(p[b_i + 1] - p[b_i]))
                    h_m = float(np.linalg.norm(p[b_i + 3] - p[b_i]))
                    fu = max(0.06, min(1.0, w_m / tile_m))
                    fv = max(0.06, min(1.0, h_m / tile_m))
                    uv_new[b_i + 0] = [u0, v0 + dv_max * fv]
                    uv_new[b_i + 1] = [u0 + du_max * fu, v0 + dv_max * fv]
                    uv_new[b_i + 2] = [u0 + du_max * fu, v0]
                    uv_new[b_i + 3] = [u0, v0]
                if n_quads * 4 < len(p):
                    rem = uv_new[n_quads * 4 :]
                    rem[:, 0] = u0 + np.clip(rem[:, 0], 0.0, 1.0) * (du_max * 0.15)
                    rem[:, 1] = v0 + np.clip(rem[:, 1], 0.0, 1.0) * (dv_max * 0.15)
                geoms.append((p, n, uv_new, idx))
    return merge_geometries(geoms)


def make_eye_level_door_placard(
    center: Tuple[float, float, float],
    uv_placard: Tuple[float, float, float, float],
    width: float = 0.48,
    height: float = 0.22,
    depth: float = 0.024,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Creates ONE eye-level architectural door placard (`0.48m W x 0.22m H x 0.024m D`)
    whose corridor-facing (`-Z`) front surface maps un-mirrored to `uv_placard`,
    while its backing plate and edges map to `UV_STEEL_TRIM`.
    """
    cx, cy, cz = center
    hx, hy, hz = width * 0.5, height * 0.5, depth * 0.5
    back_geom = make_world_uv_box((width + 0.03, height + 0.03, depth), center=(cx, cy, cz + 0.004), bevel=0.003, uv_rect=UV_STEEL_TRIM, tile_m=0.8)

    u0, u1, v0, v1 = uv_placard
    z_f = cz - hz - 0.001
    pos_f = np.array([
        [cx - hx, cy - hy, z_f],
        [cx + hx, cy - hy, z_f],
        [cx + hx, cy + hy, z_f],
        [cx - hx, cy + hy, z_f],
    ], dtype=np.float32)
    norm_f = np.array([[0.0, 0.0, -1.0]] * 4, dtype=np.float32)
    uv_f = np.array([
        [u1, v1],
        [u0, v1],
        [u0, v0],
        [u1, v0],
    ], dtype=np.float32)
    idx_f = np.array([[0, 2, 1], [0, 3, 2]], dtype=np.uint32)
    return merge_geometries([back_geom, (pos_f, norm_f, uv_f, idx_f)])


def make_forensic_workbench_top(
    size: Tuple[float, float, float],
    center: Tuple[float, float, float],
    uv_top: Tuple[float, float, float, float] = UV_WORKBENCH_TOP,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Builds the Apartment 201 Workbench butcher-block slab (`size` at `center`) where the
    base/edges use `UV_WOOD_WALNUT` and the top `+Y` work surface maps 1:1 right-reading
    to `uv_top` (so the blown C3 capacitor scorch mark, A7-0204-MEM tally, wear-polished
    forearm rest along the `-Z` front edge, and taped 03:14 UTC oscilloscope note read clearly).
    """
    cx, cy, cz = center
    sx, sy, sz = size
    hx, hy, hz = sx * 0.5, sy * 0.5, sz * 0.5
    base_box = make_world_uv_box(size, center=center, bevel=0.012, uv_rect=UV_WOOD_WALNUT, tile_m=1.5)
    u0, u1, v0, v1 = uv_top
    y_top = cy + hy + 0.0015
    # Player stands on -Z side looking +Z: +X is viewer-left (u0), -X is viewer-right (u1), +Z is far/top (v0), -Z is near/bottom (v1)
    pos_t = np.array([
        [cx + hx - 0.01, y_top, cz - hz + 0.01],  # Front-Left (u0, v1)
        [cx - hx + 0.01, y_top, cz - hz + 0.01],  # Front-Right (u1, v1)
        [cx - hx + 0.01, y_top, cz + hz - 0.01],  # Back-Right (u1, v0)
        [cx + hx - 0.01, y_top, cz + hz - 0.01],  # Back-Left (u0, v0)
    ], dtype=np.float32)
    norm_t = np.array([[0.0, 1.0, 0.0]] * 4, dtype=np.float32)
    uv_t = np.array([
        [u0, v1],
        [u1, v1],
        [u1, v0],
        [u0, v0],
    ], dtype=np.float32)
    idx_t = np.array([[0, 1, 2], [0, 2, 3]], dtype=np.uint32)
    return merge_geometries([base_box, (pos_t, norm_t, uv_t, idx_t)])


def make_forensic_pegboard(
    size: Tuple[float, float, float],
    center: Tuple[float, float, float],
    uv_front: Tuple[float, float, float, float] = UV_WORKBENCH_PEGBOARD,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Builds the Apartment 201 Workbench tool pegboard where the `-Z` front face maps 1:1
    right-reading to `UV_WORKBENCH_PEGBOARD` (`D-03 HYDRO [REMOVED]` ghost mark + `RFID BUS TAP` diagram).
    """
    cx, cy, cz = center
    sx, sy, sz = size
    hx, hy, hz = sx * 0.5, sy * 0.5, sz * 0.5
    base_box = make_world_uv_box(size, center=center, bevel=0.008, uv_rect=UV_STEEL_TRIM, tile_m=1.5)
    u0, u1, v0, v1 = uv_front
    z_f = cz - hz - 0.0015
    pos_f = np.array([
        [cx - hx + 0.02, cy - hy + 0.02, z_f],
        [cx + hx - 0.02, cy - hy + 0.02, z_f],
        [cx + hx - 0.02, cy + hy - 0.02, z_f],
        [cx - hx + 0.02, cy + hy - 0.02, z_f],
    ], dtype=np.float32)
    norm_f = np.array([[0.0, 0.0, -1.0]] * 4, dtype=np.float32)
    uv_f = np.array([
        [u1, v1],
        [u0, v1],
        [u0, v0],
        [u1, v0],
    ], dtype=np.float32)
    idx_f = np.array([[0, 2, 1], [0, 3, 2]], dtype=np.uint32)
    return merge_geometries([base_box, (pos_f, norm_f, uv_f, idx_f)])


def make_forensic_skid_strip(
    p_start: Tuple[float, float],
    p_end: Tuple[float, float],
    y_height: float = 0.123,
    width: float = 0.92,
    uv_skid: Tuple[float, float, float, float] = UV_FLOOR_SKID_TRAIL,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Creates a flush floor forensic trail quad from `p_start = (x0, z0)` to `p_end = (x1, z1)`
    at `y = y_height` mapped to `UV_FLOOR_SKID_TRAIL` (single-locked-tread rubber skid mark +
    cryo-coolant drip trail).
    """
    x0, z0 = p_start
    x1, z1 = p_end
    dx, dz = x1 - x0, z1 - z0
    length = math.hypot(dx, dz)
    if length < 1e-4:
        length = 1.0
    nx, nz = -dz / length * (width * 0.5), dx / length * (width * 0.5)
    u0, u1, v0, v1 = uv_skid
    pos = np.array([
        [x0 - nx, y_height, z0 - nz],
        [x1 - nx, y_height, z1 - nz],
        [x1 + nx, y_height, z1 + nz],
        [x0 + nx, y_height, z0 + nz],
    ], dtype=np.float32)
    norm = np.array([[0.0, 1.0, 0.0]] * 4, dtype=np.float32)
    uv = np.array([
        [u0, v0],
        [u1, v0],
        [u1, v1],
        [u0, v1],
    ], dtype=np.float32)
    idx = np.array([[0, 2, 1], [0, 3, 2]], dtype=np.uint32)
    return pos, norm, uv, idx


def make_calm_open_portal_arch_frame(
    mats: Dict[str, RichPBRMaterial],
    clear_w: float = 2.0,
    clear_h: float = 2.55,
    placard_uv: Optional[Tuple[float, float, float, float]] = None,
    placard_x_side: float = -1.0,
) -> RichPartBucket:
    bp = RichPartBucket(mats)
    hw = clear_w * 0.5
    for sx in [-1.0, 1.0]:
        bp.add(
            "residential_atlas",
            make_world_uv_box(
                (0.18, clear_h + 0.14, 0.26),
                center=(sx * (hw + 0.09), (clear_h + 0.14) * 0.5, 0.0),
                bevel=0.02,
                uv_rect=UV_STEEL_TRIM,
                tile_m=2.0,
            ),
        )
    bp.add(
        "residential_atlas",
        make_world_uv_box(
            (clear_w + 0.36, 0.20, 0.28),
            center=(0.0, clear_h + 0.10, 0.0),
            bevel=0.02,
            uv_rect=UV_STEEL_TRIM,
            tile_m=2.0,
        ),
    )
    if placard_uv is not None:
        px = placard_x_side * (hw + 0.46)
        bp.add(
            "residential_atlas",
            make_eye_level_door_placard(
                center=(px, 1.48, -0.105),
                uv_placard=placard_uv,
                width=0.48,
                height=0.22,
                depth=0.024,
            ),
        )
    return bp


def build_calm_open_doorway_residential_sector(mats: Dict[str, RichPBRMaterial]) -> Dict[str, any]:
    # --------------------------------------------------------------------------
    # 1. `Residential_Hallway_Atrium` (Main 28.0m W x 18.0m D x 8.8m H Ground Deck, Non-Emissive Columns & Skylight)
    # --------------------------------------------------------------------------
    b_atrium = RichPartBucket(mats)
    b_atrium.add(
        "residential_atlas",
        make_world_uv_box((28.0, 0.12, 18.0), center=(0.0, 0.06, 0.0), bevel=0.0, uv_rect=UV_FLOOR_SLATE, tile_m=3.5, subdivide_max_m=3.5),
    )
    # CUE-002: Physical Drag / Single-Locked-Tread Skid & Cryo-Coolant Trail from East Stairwell (`X=8.8, Z=-3.4`)
    # across the East Atrium into Room 1B Bot Substation (`X=4.65, Z=2.0 -> X=5.55, Z=6.1`) under `Kelvin #0204`!
    b_atrium.add("residential_atlas", make_forensic_skid_strip((8.80, -3.40), (5.20, 0.85), y_height=0.123, width=0.88))
    b_atrium.add("residential_atlas", make_forensic_skid_strip((5.20, 0.85), (4.65, 3.85), y_height=0.124, width=0.88))
    b_atrium.add("residential_atlas", make_forensic_skid_strip((4.65, 3.85), (5.60, 6.20), y_height=0.125, width=0.92))

    # Roof Ceiling Structural Beams (`Y = 8.64m..8.80m`) with central architectural glass skylight
    b_atrium.add("residential_atlas", make_world_uv_box((28.0, 0.16, 4.5), center=(0.0, 8.72, 6.75), bevel=0.02, uv_rect=UV_STEEL_TRIM, tile_m=3.5))
    b_atrium.add("residential_atlas", make_world_uv_box((28.0, 0.16, 4.5), center=(0.0, 8.72, -6.75), bevel=0.02, uv_rect=UV_STEEL_TRIM, tile_m=3.5))
    b_atrium.add("residential_atlas", make_world_uv_box((5.5, 0.16, 9.0), center=(-11.25, 8.72, 0.0), bevel=0.02, uv_rect=UV_STEEL_TRIM, tile_m=3.5))
    b_atrium.add("residential_atlas", make_world_uv_box((5.5, 0.16, 9.0), center=(11.25, 8.72, 0.0), bevel=0.02, uv_rect=UV_STEEL_TRIM, tile_m=3.5))
    b_atrium.add("residential_glass", make_beveled_box((17.0, 0.08, 9.0), center=(0.0, 8.70, 0.0), bevel=0.01))

    # North Backdrop Wall (`Z = +8.90m`), West Wall (`X = -13.90m`), and East 7.2m-Tall Atrium Curtain-Wall Viewport (`X = +13.90m`)
    b_atrium.add(
        "residential_atlas",
        make_world_uv_box((28.0, 8.60, 0.20), center=(0.0, 4.36, 8.90), bevel=0.02, uv_rect=UV_WALL_ATRIUM, tile_m=3.5, subdivide_max_m=3.5),
    )
    b_atrium.add(
        "residential_atlas",
        make_world_uv_box((0.20, 8.60, 18.0), center=(-13.90, 4.36, 0.0), bevel=0.02, uv_rect=UV_WALL_ATRIUM, tile_m=3.5, subdivide_max_m=3.5),
    )
    b_atrium.add("residential_atlas", make_world_uv_box((0.24, 1.10, 18.0), center=(13.88, 0.60, 0.0), bevel=0.02, uv_rect=UV_STEEL_TRIM, tile_m=3.5))
    b_atrium.add("residential_atlas", make_world_uv_box((0.24, 0.90, 18.0), center=(13.88, 8.25, 0.0), bevel=0.02, uv_rect=UV_STEEL_TRIM, tile_m=3.5))
    b_atrium.add("residential_glass", make_beveled_box((0.08, 6.70, 16.8), center=(13.88, 4.50, 0.0), bevel=0.01))
    for mz in [-5.6, 0.0, 5.6]:
        b_atrium.add("residential_atlas", make_world_uv_box((0.18, 6.75, 0.14), center=(13.86, 4.50, mz), bevel=0.01, uv_rect=UV_STEEL_TRIM, tile_m=2.5))

    for cx_col in [-12.5, -5.5, 0.0, 5.5, 12.5]:
        for cz_col in [-8.2, 2.2, 8.2]:
            b_atrium.add(
                "residential_atlas",
                make_chamfered_oct_prism(0.52, 0.52, 8.60, center=(cx_col, 4.36, cz_col), chamfer=0.11),
                UV_STEEL_TRIM,
            )

    for px_pl in [-4.2, 4.2]:
        b_atrium.add(
            "residential_atlas",
            make_chamfered_oct_prism(2.60, 1.45, 0.50, center=(px_pl, 0.37, -1.8), chamfer=0.30),
            UV_PLANTER_STONE,
        )
        b_atrium.add(
            "residential_atlas",
            make_world_uv_box((2.20, 0.08, 0.42), center=(px_pl, 0.46, -2.68), bevel=0.015, uv_rect=UV_WOOD_WALNUT, tile_m=1.5),
        )
        b_atrium.add("foliage_green", make_botanical_cluster((px_pl, 0.65, -1.8), radius=0.95, n_leaves=4))

    # --------------------------------------------------------------------------
    # 2. `Upper_Mezzanine_Walkway` (`Y = +4.20m` Deck with `Atrium_Void` & Tempered Glass Balustrade)
    # --------------------------------------------------------------------------
    b_mezz = RichPartBucket(mats)
    b_mezz.add(
        "residential_atlas",
        make_world_uv_box((27.6, 0.18, 7.6), center=(0.0, 0.0, 5.0), bevel=0.02, uv_rect=UV_FLOOR_SLATE, tile_m=3.5, subdivide_max_m=3.5),
    )
    b_mezz.add(
        "residential_atlas",
        make_world_uv_box((6.3, 0.18, 7.7), center=(-10.65, 0.0, -2.65), bevel=0.02, uv_rect=UV_FLOOR_SLATE, tile_m=3.5, subdivide_max_m=3.5),
    )
    b_mezz.add(
        "residential_atlas",
        make_world_uv_box((6.3, 0.18, 3.4), center=(10.65, 0.0, -0.50), bevel=0.02, uv_rect=UV_FLOOR_SLATE, tile_m=3.5, subdivide_max_m=3.5),
    )
    b_mezz.add("residential_glass", make_beveled_box((15.2, 1.06, 0.05), center=(0.0, 0.62, 1.25), bevel=0.008))
    b_mezz.add("residential_atlas", make_world_uv_box((15.4, 0.06, 0.09), center=(0.0, 1.16, 1.25), bevel=0.01, uv_rect=UV_STEEL_TRIM, tile_m=2.5))
    b_mezz.add("residential_atlas", make_world_uv_box((15.4, 0.08, 0.12), center=(0.0, 0.11, 1.25), bevel=0.01, uv_rect=UV_STEEL_TRIM, tile_m=2.5))
    for post_x in [-7.5, -3.75, 0.0, 3.75, 7.5]:
        b_mezz.add("residential_atlas", make_world_uv_box((0.08, 1.12, 0.08), center=(post_x, 0.62, 1.25), bevel=0.01, uv_rect=UV_STEEL_TRIM, tile_m=1.5))

    b_mezz.add("residential_glass", make_beveled_box((0.05, 1.06, 7.6), center=(-7.55, 0.62, -2.60), bevel=0.008))
    b_mezz.add("residential_atlas", make_world_uv_box((0.09, 0.06, 7.6), center=(-7.55, 1.16, -2.60), bevel=0.01, uv_rect=UV_STEEL_TRIM, tile_m=2.5))
    b_mezz.add("residential_atlas", make_world_uv_box((0.12, 0.08, 7.6), center=(-7.55, 0.11, -2.60), bevel=0.01, uv_rect=UV_STEEL_TRIM, tile_m=2.5))

    # --------------------------------------------------------------------------
    # 3. `Tech_Apartment_Upper` / `APT 201` (`X = -9.5m, Y = +4.20m, Z = +5.6m`, `8.2m W x 5.8m D x 3.8m H`)
    # --------------------------------------------------------------------------
    b_apt = RichPartBucket(mats)
    b_apt.add("residential_atlas", make_world_uv_box((8.2, 0.06, 5.8), center=(0.0, 0.12, 0.0), bevel=0.01, uv_rect=UV_FLOOR_SLATE, tile_m=3.5))
    b_apt.add("residential_atlas", make_world_uv_box((0.16, 3.8, 5.8), center=(4.05, 1.98, 0.0), bevel=0.02, uv_rect=UV_WALL_APT, tile_m=3.5))
    b_apt.add("residential_atlas", make_world_uv_box((1.4, 3.8, 0.16), center=(-3.40, 1.98, -2.85), bevel=0.02, uv_rect=UV_WALL_APT, tile_m=3.5))
    b_apt.add("residential_atlas", make_world_uv_box((2.0, 1.15, 0.16), center=(-1.70, 3.30, -2.85), bevel=0.02, uv_rect=UV_WALL_APT, tile_m=3.5))
    b_apt.add("residential_atlas", make_world_uv_box((4.8, 1.10, 0.16), center=(1.70, 0.64, -2.85), bevel=0.02, uv_rect=UV_WALL_APT, tile_m=3.5))
    b_apt.add("residential_atlas", make_world_uv_box((4.8, 0.85, 0.16), center=(1.70, 3.45, -2.85), bevel=0.02, uv_rect=UV_WALL_APT, tile_m=3.5))

    # Compact Kitchenette Counter along East wall of Apt 201 (`X = +3.35m, Z = +0.40m`)
    b_apt.add("residential_atlas", make_world_uv_box((1.15, 0.86, 2.10), center=(3.42, 0.56, 0.45), bevel=0.02, uv_rect=UV_STEEL_TRIM, tile_m=1.5))
    b_apt.add("residential_atlas", make_world_uv_box((1.20, 0.06, 2.16), center=(3.40, 1.01, 0.45), bevel=0.01, uv_rect=UV_WOOD_WALNUT, tile_m=1.5))
    b_apt.add("residential_atlas", make_world_uv_box((0.55, 0.68, 2.05), center=(3.70, 2.25, 0.45), bevel=0.015, uv_rect=UV_WOOD_WALNUT, tile_m=1.5))
    b_apt.add("residential_atlas", make_beveled_box((0.12, 0.025, 1.75), center=(3.58, 1.89, 0.45), bevel=0.003), UV_LIGHT_WARM)

    b_portal_201 = make_calm_open_portal_arch_frame(mats, clear_w=2.0, clear_h=2.55, placard_uv=UV_PLACARD_201, placard_x_side=-1.0)

    b_apt_win = RichPartBucket(mats)
    b_apt_win.add("residential_glass", make_beveled_box((4.50, 1.85, 0.05), center=(0.0, 0.0, 0.0), bevel=0.008))

    b_bunk = RichPartBucket(mats)
    b_bunk.add("residential_atlas", make_world_uv_box((1.35, 0.42, 2.20), center=(0.0, 0.34, 0.0), bevel=0.02, uv_rect=UV_WOOD_WALNUT, tile_m=1.5))
    b_bunk.add("residential_atlas", make_world_uv_box((1.26, 0.18, 2.08), center=(0.02, 0.62, 0.0), bevel=0.03, uv_rect=UV_FABRIC_SLATE, tile_m=1.5))
    b_bunk.add("residential_atlas", make_world_uv_box((0.85, 0.12, 0.38), center=(0.02, 0.75, 0.76), bevel=0.025, uv_rect=UV_WALL_APT, tile_m=1.0))
    b_bunk.add("residential_atlas", make_world_uv_box((1.38, 1.45, 0.14), center=(0.0, 1.15, 1.05), bevel=0.02, uv_rect=UV_WOOD_WALNUT, tile_m=1.5))
    b_bunk.add("residential_atlas", make_beveled_box((0.68, 0.035, 0.06), center=(0.0, 1.68, 0.96), bevel=0.004), UV_LIGHT_WARM)

    # `Apartment_Workbench` (`Workbench_Player`): CUE-001A (`UV_WORKBENCH_TOP`) + CUE-001B (`UV_WORKBENCH_PEGBOARD`)!
    b_wb = RichPartBucket(mats)
    b_wb.add("residential_atlas", make_world_uv_box((2.40, 0.78, 0.84), center=(0.0, 0.45, 0.0), bevel=0.02, uv_rect=UV_STEEL_TRIM, tile_m=1.5))
    b_wb.add("residential_atlas", make_forensic_workbench_top((2.46, 0.07, 0.90), center=(0.0, 0.87, 0.0), uv_top=UV_WORKBENCH_TOP))
    b_wb.add("residential_atlas", make_forensic_pegboard((2.32, 1.05, 0.06), center=(0.0, 1.44, 0.38), uv_front=UV_WORKBENCH_PEGBOARD))
    b_wb.add("residential_atlas", make_world_uv_box((1.85, 0.06, 0.28), center=(0.0, 1.96, 0.26), bevel=0.01, uv_rect=UV_STEEL_TRIM, tile_m=1.5))
    b_wb.add("residential_atlas", make_beveled_box((1.65, 0.025, 0.12), center=(0.0, 1.92, 0.24), bevel=0.003), UV_LIGHT_WARM)
    # Compact diagnostic terminal screen in muted functional cyan (#2E8B9A)
    b_wb.add("residential_atlas", make_world_uv_box((0.46, 0.32, 0.06), center=(-0.82, 1.32, 0.34), bevel=0.008, uv_rect=UV_STEEL_TRIM, tile_m=1.0))
    b_wb.add("residential_atlas", make_beveled_box((0.40, 0.26, 0.065), center=(-0.82, 1.32, 0.34), bevel=0.004), UV_LIGHT_CYAN)
    for bx_bin in [0.48, 0.81]:
        b_wb.add("residential_atlas", make_world_uv_box((0.24, 0.14, 0.14), center=(bx_bin, 1.26, 0.30), bevel=0.008, uv_rect=UV_STEEL_TRIM, tile_m=0.8))

    # Starter Pickups on Workbench (positioned on the +X / left side of the bench so the CUE-001 scorch mark & 03:14 UTC note on -X are 100% unobstructed!)
    b_pw_start = RichPartBucket(mats)
    b_pw_start.add("residential_atlas", make_cylinder(0.08, 0.08, 0.12, center=(0.0, 0.06, 0.0), segments=14), UV_RES_Q3_WIRE)
    b_pw_start.add("residential_atlas", make_closed_torus_ring(0.084, 0.008, center=(0.0, 0.06, 0.0), n_major=14, n_minor=5), UV_LIGHT_CYAN)

    b_pb_start = RichPartBucket(mats)
    b_pb_start.add("residential_atlas", make_chamfered_oct_prism(0.12, 0.12, 0.18, center=(0.0, 0.09, 0.0), chamfer=0.025), UV_RES_Q3_BATT)
    b_pb_start.add("residential_atlas", make_closed_torus_ring(0.065, 0.007, center=(0.0, 0.11, 0.0), n_major=12, n_minor=5), UV_LIGHT_CYAN)

    b_bci_dock = RichPartBucket(mats)
    b_bci_dock.add("steel_machined", make_cylinder(0.032, 0.048, 0.11, center=(0.0, 0.055, 0.0), segments=10))
    b_bci_dock.add("residential_atlas", make_closed_torus_ring(0.085, 0.010, center=(0.0, 0.12, 0.0), rot_xyz_deg=(18.0, 0.0, 0.0), n_major=16, n_minor=6), UV_LIGHT_CYAN)

    # --------------------------------------------------------------------------
    # 4. `Room_2B_Neighbor_Balcony_Suite` / `APT 202` (Quartermaster Quarters, `X = +9.5m, Y = +4.20m, Z = +5.6m`)
    # --------------------------------------------------------------------------
    b_room2b = RichPartBucket(mats)
    b_room2b.add("residential_atlas", make_world_uv_box((0.16, 3.8, 5.8), center=(-4.05, 1.98, 0.0), bevel=0.02, uv_rect=UV_WALL_APT, tile_m=3.5))
    b_room2b.add("residential_atlas", make_world_uv_box((1.4, 3.8, 0.16), center=(-3.40, 1.98, -2.85), bevel=0.02, uv_rect=UV_WALL_APT, tile_m=3.5))
    b_room2b.add("residential_atlas", make_world_uv_box((2.0, 1.15, 0.16), center=(-1.70, 3.30, -2.85), bevel=0.02, uv_rect=UV_WALL_APT, tile_m=3.5))
    b_room2b.add("residential_atlas", make_world_uv_box((4.8, 3.8, 0.16), center=(1.70, 1.98, -2.85), bevel=0.02, uv_rect=UV_WALL_APT, tile_m=3.5))
    b_room2b.add("residential_atlas", make_world_uv_box((1.95, 0.76, 0.82), center=(1.2, 0.44, 1.6), bevel=0.02, uv_rect=UV_STEEL_TRIM, tile_m=1.5))
    b_room2b.add("residential_atlas", make_world_uv_box((2.02, 0.06, 0.88), center=(1.2, 0.85, 1.6), bevel=0.015, uv_rect=UV_WOOD_WALNUT, tile_m=1.5))
    b_room2b.add("residential_atlas", make_beveled_box((0.55, 0.03, 0.12), center=(0.65, 1.32, 1.85), bevel=0.004), UV_LIGHT_WARM)
    b_room2b.add("residential_atlas", make_world_uv_box((0.56, 0.48, 0.54), center=(1.2, 0.30, 0.82), bevel=0.02, uv_rect=UV_FABRIC_SLATE, tile_m=1.0))
    b_room2b.add("residential_atlas", make_world_uv_box((0.68, 2.10, 1.45), center=(-3.30, 1.12, 1.20), bevel=0.02, uv_rect=UV_STEEL_TRIM, tile_m=1.8))
    b_room2b.add("residential_atlas", make_world_uv_box((1.25, 0.40, 2.05), center=(3.10, 0.32, -0.55), bevel=0.02, uv_rect=UV_WOOD_WALNUT, tile_m=1.5))
    b_room2b.add("residential_atlas", make_world_uv_box((1.18, 0.16, 1.96), center=(3.10, 0.58, -0.55), bevel=0.025, uv_rect=UV_FABRIC_SLATE, tile_m=1.5))

    b_portal_202 = make_calm_open_portal_arch_frame(mats, clear_w=2.0, clear_h=2.55, placard_uv=UV_PLACARD_202, placard_x_side=1.0)

    # --------------------------------------------------------------------------
    # 5. `Alcove_2C_Upper_Vent_Chase` (`X = -11.5m, Y = +4.20m, Z = -4.5m`)
    # --------------------------------------------------------------------------
    b_alcove2c = RichPartBucket(mats)
    b_alcove2c.add("residential_atlas", make_world_uv_box((2.40, 2.65, 0.18), center=(0.0, 1.40, -1.10), bevel=0.02, uv_rect=UV_STEEL_TRIM, tile_m=2.0))
    b_alcove2c.add("residential_atlas", make_world_uv_box((0.18, 2.65, 2.20), center=(-1.15, 1.40, 0.0), bevel=0.02, uv_rect=UV_STEEL_TRIM, tile_m=2.0))
    b_alcove2c.add("residential_atlas", make_world_uv_box((1.80, 0.75, 0.65), center=(0.0, 0.42, -0.55), bevel=0.02, uv_rect=UV_STEEL_TRIM, tile_m=1.5))

    b_arch_2c = make_calm_open_portal_arch_frame(mats, clear_w=1.8, clear_h=2.45, placard_uv=None)

    b_pw_exp = RichPartBucket(mats)
    b_pw_exp.add("residential_atlas", make_cylinder(0.12, 0.12, 0.18, center=(0.0, 0.09, 0.0), segments=14), UV_RES_Q3_WIRE)
    b_pw_exp.add("residential_atlas", make_closed_torus_ring(0.125, 0.012, center=(0.0, 0.09, 0.0), n_major=14, n_minor=5), UV_LIGHT_CYAN)

    b_pb_exp = RichPartBucket(mats)
    b_pb_exp.add("residential_atlas", make_chamfered_oct_prism(0.18, 0.18, 0.25, center=(0.0, 0.125, 0.0), chamfer=0.03), UV_RES_Q3_BATT)
    b_pb_exp.add("residential_atlas", make_closed_torus_ring(0.095, 0.010, center=(0.0, 0.15, 0.0), n_major=12, n_minor=5), UV_LIGHT_CYAN)

    # --------------------------------------------------------------------------
    # 6. `Stair_Ramp_Connector` (`3.0m` wide switchback staircase at East side `X = +10.65m`)
    # --------------------------------------------------------------------------
    b_stair = RichPartBucket(mats)
    n_steps = 16
    for s_i in range(n_steps):
        frac = (s_i + 0.5) / float(n_steps)
        sy = 4.20 * (1.0 - frac)
        sz = -2.20 - frac * 5.60
        b_stair.add(
            "residential_atlas",
            make_world_uv_box((2.95, 0.22, 0.42), center=(0.0, sy, sz), bevel=0.015, uv_rect=UV_FLOOR_SLATE, tile_m=2.0),
        )
        b_stair.add(
            "residential_atlas",
            make_beveled_box((2.75, 0.018, 0.028), center=(0.0, sy + 0.112, sz - 0.195), bevel=0.002),
            UV_LIGHT_AMBER,
        )
    for sx_r in [-1.45, 1.45]:
        r_pts = np.array([[sx_r, 5.15, -2.20], [sx_r, 0.95, -7.80]], dtype=np.float32)
        b_stair.add("steel_machined", make_swept_tube(r_pts, radius=0.042, radial_segments=8))
        b_stair.add("residential_atlas", make_swept_tube(r_pts + np.array([0.0, -0.38, 0.0], dtype=np.float32), radius=0.024, radial_segments=6), UV_STEEL_TRIM)

    # --------------------------------------------------------------------------
    # 7. Level 1 Room 1A (`Side_Room_East_Lounge` / `Room_1A_Laundry_Lounge`, West `X = -8.5m, Z = +5.6m`)
    # --------------------------------------------------------------------------
    b_room1a = RichPartBucket(mats)
    b_room1a.add("residential_atlas", make_world_uv_box((2.55, 3.8, 0.18), center=(-2.475, 2.00, -2.75), bevel=0.02, uv_rect=UV_WALL_ATRIUM, tile_m=3.5))
    b_room1a.add("residential_atlas", make_world_uv_box((2.55, 3.8, 0.18), center=(2.475, 2.00, -2.75), bevel=0.02, uv_rect=UV_WALL_ATRIUM, tile_m=3.5))
    b_room1a.add("residential_atlas", make_world_uv_box((2.40, 1.15, 0.18), center=(0.0, 3.32, -2.75), bevel=0.02, uv_rect=UV_WALL_ATRIUM, tile_m=3.5))
    for wx in [-2.2, -0.8, 0.6]:
        b_room1a.add("residential_atlas", make_world_uv_box((1.08, 1.32, 0.92), center=(wx, 0.78, 1.80), bevel=0.03, uv_rect=UV_WALL_APT, tile_m=1.5))
        b_room1a.add("residential_atlas", make_world_uv_box((1.04, 0.18, 0.94), center=(wx, 1.34, 1.80), bevel=0.015, uv_rect=UV_STEEL_TRIM, tile_m=1.0))
        b_room1a.add("residential_glass", make_cylinder(0.30, 0.30, 0.05, center=(wx, 0.82, 1.33), segments=12, axis="z"))
    b_room1a.add("residential_atlas", make_world_uv_box((1.25, 0.82, 1.40), center=(2.35, 0.50, 1.65), bevel=0.02, uv_rect=UV_STEEL_TRIM, tile_m=1.5))
    b_room1a.add("residential_atlas", make_world_uv_box((1.30, 0.06, 1.46), center=(2.35, 0.93, 1.65), bevel=0.015, uv_rect=UV_WOOD_WALNUT, tile_m=1.5))
    b_room1a.add("residential_atlas", make_beveled_box((0.85, 0.025, 0.12), center=(2.35, 2.25, 1.65), bevel=0.003), UV_LIGHT_WARM)
    b_room1a.add("residential_atlas", make_world_uv_box((0.75, 0.44, 1.85), center=(-3.10, 0.34, -0.45), bevel=0.02, uv_rect=UV_FABRIC_SLATE, tile_m=1.5))

    b_portal_1a = make_calm_open_portal_arch_frame(mats, clear_w=2.4, clear_h=2.60, placard_uv=UV_PLACARD_1A, placard_x_side=-1.0)

    # --------------------------------------------------------------------------
    # 8. Level 1 Room 1B (`Side_Room_West_Storage` / `Room_1B_Bot_Substation`, East `X = +4.5m, Z = +5.6m`)
    # --------------------------------------------------------------------------
    b_room1b = RichPartBucket(mats)
    b_room1b.add("residential_atlas", make_world_uv_box((2.65, 3.8, 0.18), center=(-2.425, 2.00, -2.75), bevel=0.02, uv_rect=UV_WALL_ATRIUM, tile_m=3.5))
    b_room1b.add("residential_atlas", make_world_uv_box((2.65, 3.8, 0.18), center=(2.425, 2.00, -2.75), bevel=0.02, uv_rect=UV_WALL_ATRIUM, tile_m=3.5))
    b_room1b.add("residential_atlas", make_world_uv_box((2.20, 1.15, 0.18), center=(0.0, 3.32, -2.75), bevel=0.02, uv_rect=UV_WALL_ATRIUM, tile_m=3.5))
    for bx_dock in [-1.8, 0.2]:
        b_room1b.add("residential_atlas", make_chamfered_oct_prism(1.22, 1.12, 0.12, center=(bx_dock, 0.16, 1.65), chamfer=0.14), UV_STEEL_TRIM)
        b_room1b.add("residential_atlas", make_world_uv_box((0.78, 1.85, 0.42), center=(bx_dock, 1.05, 2.35), bevel=0.02, uv_rect=UV_STEEL_TRIM, tile_m=1.5))
        b_room1b.add("residential_atlas", make_closed_torus_ring(0.42, 0.018, center=(bx_dock, 0.22, 1.65), n_major=14, n_minor=5), UV_LIGHT_AMBER)
    # Substation calibration workbench (`X = +2.2m, Z = +1.5m`) with forensic pegboard card & honey-teak top
    b_room1b.add("residential_atlas", make_world_uv_box((1.95, 0.82, 0.84), center=(2.20, 0.49, 1.50), bevel=0.02, uv_rect=UV_STEEL_TRIM, tile_m=1.5))
    b_room1b.add("residential_atlas", make_world_uv_box((2.02, 0.06, 0.88), center=(2.20, 0.92, 1.50), bevel=0.015, uv_rect=UV_WOOD_WALNUT, tile_m=1.5))
    b_room1b.add("residential_atlas", make_beveled_box((0.95, 0.025, 0.12), center=(2.20, 2.15, 1.80), bevel=0.003), UV_LIGHT_WARM)

    b_portal_1b = make_calm_open_portal_arch_frame(mats, clear_w=2.2, clear_h=2.60, placard_uv=UV_PLACARD_1B, placard_x_side=-1.0)

    # --------------------------------------------------------------------------
    # 9. `Ground_Service_Vestibule` & `Open_Portal_Sector_Exit` (`2.6m W x 2.8m H` Open South Concourse Exit at `Z = -8.90m`)
    # --------------------------------------------------------------------------
    b_vest = RichPartBucket(mats)
    b_vest.add(
        "residential_atlas",
        make_world_uv_box((12.6, 8.60, 0.22), center=(-7.70, 4.36, -8.90), bevel=0.02, uv_rect=UV_WALL_ATRIUM, tile_m=3.5, subdivide_max_m=3.5),
    )
    b_vest.add(
        "residential_atlas",
        make_world_uv_box((12.6, 8.60, 0.22), center=(7.70, 4.36, -8.90), bevel=0.02, uv_rect=UV_WALL_ATRIUM, tile_m=3.5, subdivide_max_m=3.5),
    )
    b_vest.add(
        "residential_atlas",
        make_world_uv_box((2.80, 4.95, 0.22), center=(0.0, 6.18, -8.90), bevel=0.02, uv_rect=UV_WALL_ATRIUM, tile_m=3.5, subdivide_max_m=3.5),
    )
    b_vest.add("steel_machined", make_cylinder(0.045, 0.045, 2.60, center=(0.0, 3.25, -8.88), segments=10, axis="x"))
    b_vest.add("residential_glass", make_beveled_box((2.60, 0.82, 0.06), center=(0.0, 3.25, -8.80), bevel=0.01))
    b_vest.add("residential_atlas", make_beveled_box((2.52, 0.018, 0.12), center=(0.0, 0.128, -8.82), bevel=0.003), UV_LIGHT_AMBER)

    b_portal_exit = make_calm_open_portal_arch_frame(mats, clear_w=2.6, clear_h=2.80, placard_uv=None)

    node_specs = [
        ("PrefaceResidentialSector_Root", None, (0.0, 0.0, 0.0), None),
        ("Residential_Hallway_Atrium", "PrefaceResidentialSector_Root", (0.0, 0.0, 0.0), b_atrium),
        ("Atrium_Void", "PrefaceResidentialSector_Root", (0.0, 4.20, -2.50), None),
        ("Upper_Mezzanine_Walkway", "PrefaceResidentialSector_Root", (0.0, 4.20, 0.0), b_mezz),
        ("Tech_Apartment_Upper", "PrefaceResidentialSector_Root", (-9.50, 4.20, 5.60), b_apt),
        ("apt_player_top_floor", "Tech_Apartment_Upper", (0.0, 0.0, 0.0), None),
        ("Open_Portal_201", "Tech_Apartment_Upper", (-1.70, 0.12, -2.85), b_portal_201),
        ("Apartment_Atrium_Window", "Tech_Apartment_Upper", (1.70, 2.05, -2.85), b_apt_win),
        ("Apartment_Bunk_Pod", "Tech_Apartment_Upper", (-2.85, 0.0, 1.20), b_bunk),
        ("Apartment_Workbench", "Tech_Apartment_Upper", (1.05, 0.0, 2.15), b_wb),
        ("Workbench_Player", "Apartment_Workbench", (0.0, 0.0, 0.0), None),
        ("Pickup_Super_Wire_Starter", "Apartment_Workbench", (0.85, 0.91, 0.18), b_pw_start),
        ("Pickup_Battery_Cell_Starter", "Apartment_Workbench", (1.08, 0.91, -0.12), b_pb_start),
        ("Pickup_BCI_Headband_Dock", "Apartment_Workbench", (0.52, 0.91, 0.18), b_bci_dock),
        ("Room_2B_Neighbor_Balcony_Suite", "PrefaceResidentialSector_Root", (9.50, 4.20, 5.60), b_room2b),
        ("Open_Portal_202", "Room_2B_Neighbor_Balcony_Suite", (-1.70, 0.12, -2.85), b_portal_202),
        ("Alcove_2C_Upper_Vent_Chase", "PrefaceResidentialSector_Root", (-11.50, 4.20, -4.50), b_alcove2c),
        ("Open_Arch_2C", "Alcove_2C_Upper_Vent_Chase", (0.0, 0.12, 0.95), b_arch_2c),
        ("Pickup_Super_Wire_Expansion", "Alcove_2C_Upper_Vent_Chase", (-0.42, 0.82, -0.55), b_pw_exp),
        ("Pickup_Battery_Expansion", "Alcove_2C_Upper_Vent_Chase", (0.42, 0.82, -0.55), b_pb_exp),
        ("Stair_Ramp_Connector", "PrefaceResidentialSector_Root", (10.65, 0.0, 0.0), b_stair),
        ("Side_Room_East_Lounge", "PrefaceResidentialSector_Root", (-8.50, 0.0, 5.60), b_room1a),
        ("Room_1A_Laundry_Lounge", "Side_Room_East_Lounge", (0.0, 0.0, 0.0), None),
        ("Open_Portal_1A", "Side_Room_East_Lounge", (0.0, 0.12, -2.75), b_portal_1a),
        ("Side_Room_West_Storage", "PrefaceResidentialSector_Root", (4.50, 0.0, 5.60), b_room1b),
        ("Room_1B_Bot_Substation", "Side_Room_West_Storage", (0.0, 0.0, 0.0), None),
        ("Open_Portal_1B", "Side_Room_West_Storage", (0.0, 0.12, -2.75), b_portal_1b),
        ("Ground_Service_Vestibule", "PrefaceResidentialSector_Root", (0.0, 0.0, 0.0), b_vest),
        ("Open_Portal_Sector_Exit", "Ground_Service_Vestibule", (0.0, 0.12, -8.90), b_portal_exit),
    ]

    primary_out = os.path.join(ENV_DIRS[0], "preface_residential_sector.glb")
    info = export_hierarchy_with_animations_glb(
        primary_out,
        root_scene_name="PrefaceResidentialSector_OpenDoorways",
        node_specs=node_specs,
        mats=mats,
        animations_spec=[],
        auto_ground_root_y=True,
    )
    extra_targets = [
        os.path.join(GODOT_MODELS_DIR, "preface_residential_sector.glb"),
    ]
    for d in ENV_DIRS:
        for fn in ["preface_residential_sector.glb", "preface_residential_two_story_block.glb"]:
            extra_targets.append(os.path.join(d, fn))
    for dst in extra_targets:
        if os.path.abspath(dst) != os.path.abspath(primary_out):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(primary_out, dst)
    return info
