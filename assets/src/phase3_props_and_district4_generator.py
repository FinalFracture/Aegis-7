#!/usr/bin/env python3
"""
Phase 3 Generator for Rook (3D Modeling Specialist):
Builds 50 new binary glTF 2.0 (.glb) candidates under the strict "Make 5 Candidates First -> Render 5 -> 6-Bot Vote" rule:
  Part A — 5 Exterior Sci-Fi Movie Set & Street-Plaza Prop Rounds (25 .glb files):
    /workspace/game-project/assets/glb/props/prop_01/prop_01_r1_01.glb .. prop_01_r1_05.glb
    ...
    /workspace/game-project/assets/glb/props/prop_05/prop_05_r1_01.glb .. prop_05_r1_05.glb
    (Triangle Budget: strictly 1,800 - 4,200 triangles per .glb)

  Part B — 5 Additional District IV Building Exteriors (`bldg_16` through `bldg_20`, 25 .glb files):
    /workspace/game-project/assets/glb/buildings/bldg_16/bldg_16_r1_01.glb .. bldg_16_r1_05.glb
    ...
    /workspace/game-project/assets/glb/buildings/bldg_20/bldg_20_r1_01.glb .. bldg_20_r1_05.glb
    (Triangle Budget: strictly 3,500 - 6,000 triangles per .glb)

All 50 models have:
  - Bottom-center (0,0,0) floor pivot (`min_y == 0.00000`) facing `+Z`
  - Unified Aegis-7 PBR Material & Texture Kit (`#1A1E24`, `#D8DEE6`, `#282E38`, `#88929E`, `#D95B26`, `#00E5FF`, `#FF9500`, `#7B5CFF`)
  - True `alphaMode: "BLEND"` translucent glass/holo surfaces with rich 3D interior structures inside
  - Candidate `#02` as the canonical Aegis-7 Dual-Zone Split-Mass Signature
"""
import os
import sys
import math
import json
from typing import Dict, List, Tuple
import numpy as np

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
    make_sculpted_cushion,
    make_curved_leaf_blade,
    make_beveled_box,
    make_cylinder,
)
from bunk_round1_generator import (
    hex_rgba,
    add_part,
    center_and_export_glb,
)
import buildings_exteriors_generator as beg
from buildings_exteriors_generator import (
    get_building_materials,
    make_chamfered_oct_prism,
    make_closed_torus_ring,
    make_botanical_cluster,
    BuildingKit,
    add_plaza_plinth_and_entry,
    add_ribbed_oct_tower_block,
    add_translucent_atrium_tower,
    add_rooftop_helipad_or_comms,
)
from vance_exterior_props_generator import get_prop_materials

OUT_PROPS_ROOT = "/workspace/game-project/assets/glb/props"
OUT_BLDG_ROOT = "/workspace/game-project/assets/glb/buildings"
os.makedirs(OUT_PROPS_ROOT, exist_ok=True)
os.makedirs(OUT_BLDG_ROOT, exist_ok=True)


def adjust_kit_budget(kit: BuildingKit, min_tris: int, max_tris: int, y_base: float = 0.28, radius: float = 1.15):
    """Ensures triangle count lands strictly inside [min_tris, max_tris]."""
    cur = kit.count_tris()
    idx_p = 0
    while cur < min_tris and idx_p < 80:
        ang = (idx_p / 12.0) * 2.0 * math.pi
        rx = radius * math.cos(ang)
        rz = radius * math.sin(ang)
        kit.add("carbon_slate", make_beveled_box((0.22, 0.14, 0.22), center=(rx, y_base, rz), bevel=0.02))
        kit.add("steel_machined", make_cylinder(0.05, 0.04, 0.18, center=(rx, y_base + 0.12, rz), segments=10))
        cur = kit.count_tris()
        idx_p += 1


# ==============================================================================
# PART A: 5 EXTERIOR SCI-FI MOVIE SET & STREET-PLAZA PROP ROUNDS (25 GLBs)
# Strictly 1,800 - 4,200 triangles per .glb
# ==============================================================================
def build_prop_01_candidate(cand_id: int, mats: Dict[str, PBRMaterialDef]) -> Dict[str, any]:
    kit = BuildingKit(mats)

    def _add_shuttle_car(cx: float, cy: float, cz: float, length: float = 4.6, glass_key: str = "glass_cyan"):
        kit.add("aero_white", make_chamfered_oct_prism(length, 1.68, 1.08, center=(cx, cy, cz), chamfer=0.50))
        kit.add("aero_white", transform_geom(make_cylinder(0.68, 0.20, 0.78, segments=10, axis="x"), translate=(cx + length * 0.54, cy - 0.04, cz)))
        kit.add("aero_white", transform_geom(make_cylinder(0.20, 0.68, 0.78, segments=10, axis="x"), translate=(cx - length * 0.54, cy - 0.04, cz)))
        kit.add("accent_orange", make_beveled_box((1.08, 0.92, 1.74), center=(cx, cy - 0.02, cz), bevel=0.04))
        for sx in [-1.25, -0.55, 0.55, 1.25]:
            kit.add("carbon_slate", make_beveled_box((0.34, 0.42, 1.10), center=(cx + sx, cy - 0.14, cz), bevel=0.03))
        kit.add("led_cyan", make_beveled_box((length * 0.78, 0.06, 0.20), center=(cx, cy + 0.42, cz), bevel=0.01))
        kit.add(glass_key, make_chamfered_oct_prism(length * 0.86, 1.74, 0.58, center=(cx, cy + 0.16, cz), chamfer=0.44))

    if cand_id == 1:
        for px in [-2.5, 2.5]:
            kit.add("gunmetal", make_chamfered_oct_prism(1.50, 1.50, 0.34, center=(px, 0.17, 0.0), chamfer=0.38))
            kit.add("led_amber", make_chamfered_oct_prism(1.54, 1.54, 0.06, center=(px, 0.12, 0.0), chamfer=0.38))
            kit.add("gunmetal", make_chamfered_oct_prism(0.84, 0.84, 2.80, center=(px, 1.72, 0.0), chamfer=0.22, top_scale=0.86))
            for z_arm in [-0.72, 0.72]:
                pts = sample_filleted_polyline([(px, 2.90, 0.0), (px, 3.60, z_arm * 0.65), (px, 4.05, z_arm)], 0.22, 3)
                kit.add("gunmetal", make_swept_tube(pts, radius=0.17, radial_segments=8))
            kit.add("carbon_slate", make_beveled_box((1.05, 0.26, 2.15), center=(px, 4.14, 0.0), bevel=0.04))
        for z_rail in [-0.72, 0.72]:
            kit.add("steel_machined", make_beveled_box((7.50, 0.24, 0.42), center=(0.0, 4.34, z_rail), bevel=0.04))
            kit.add("led_cyan", make_beveled_box((7.40, 0.06, 0.16), center=(0.0, 4.48, z_rail), bevel=0.01))
        _add_shuttle_car(0.0, 5.10, 0.0, length=4.6)

    elif cand_id == 2:
        kit.add("gunmetal", make_chamfered_oct_prism(7.80, 3.40, 0.34, center=(0.0, 0.17, 0.0), chamfer=0.75))
        kit.add("led_amber", make_chamfered_oct_prism(7.86, 3.46, 0.06, center=(0.0, 0.12, 0.0), chamfer=0.75))
        for px in [-2.6, 0.4]:
            kit.add("gunmetal", make_chamfered_oct_prism(0.92, 0.92, 3.85, center=(px, 2.10, -0.35), chamfer=0.24, top_scale=0.85))
            kit.add("led_cyan", make_beveled_box((0.10, 3.50, 0.96), center=(px, 2.10, -0.35), bevel=0.01))
        for z_rail in [-0.95, 0.25]:
            kit.add("steel_machined", make_beveled_box((6.20, 0.26, 0.42), center=(-1.0, 4.18, z_rail), bevel=0.04))
            kit.add("led_cyan", make_beveled_box((6.10, 0.07, 0.16), center=(-1.0, 4.33, z_rail), bevel=0.01))
        _add_shuttle_car(-1.05, 4.92, -0.35, length=4.5)
        kit.add("carbon_slate", make_chamfered_oct_prism(2.10, 2.20, 0.42, center=(2.35, 4.12, 0.15), chamfer=0.42))
        kit.add("accent_orange", make_beveled_box((0.36, 1.35, 1.15), center=(1.32, 4.78, 0.15), bevel=0.04))
        kit.add("marquee", make_beveled_box((1.85, 0.34, 0.14), center=(2.35, 5.75, 1.18), bevel=0.02))
        for sy_step in [1.2, 2.1, 3.0, 3.9]:
            kit.add("aero_white", make_chamfered_oct_prism(1.45, 1.45, 0.14, center=(2.35, sy_step, 0.35), chamfer=0.30))
        kit.add("steel_machined", make_cylinder(0.12, 0.12, 5.20, center=(2.35, 2.95, 0.35), segments=8))
        kit.add("accent_orange", make_chamfered_oct_prism(1.10, 1.10, 1.05, center=(2.35, 2.65, 0.35), chamfer=0.22))
        kit.add("glass_cyan", make_chamfered_oct_prism(1.85, 1.85, 5.10, center=(2.35, 2.95, 0.35), chamfer=0.38))

    elif cand_id == 3:
        kit.add("gunmetal", make_chamfered_oct_prism(7.40, 3.60, 0.32, center=(0.0, 0.16, 0.0), chamfer=0.70))
        arch_pts = sample_filleted_polyline([(-3.2, 0.3, 0.0), (-2.6, 4.3, 0.0), (2.6, 4.3, 0.0), (3.2, 0.3, 0.0)], 0.85, 4)
        kit.add("steel_machined", make_swept_tube(arch_pts, radius=0.26, radial_segments=8))
        for z_track, x_car in [(-0.95, -1.1), (0.95, 1.1)]:
            kit.add("carbon_slate", make_beveled_box((7.20, 0.24, 0.85), center=(0.0, 4.15, z_track), bevel=0.04))
            kit.add("led_cyan", make_beveled_box((7.10, 0.06, 0.18), center=(0.0, 4.29, z_track), bevel=0.01))
            _add_shuttle_car(x_car, 4.88, z_track, length=3.6)

    elif cand_id == 4:
        kit.add("gunmetal", make_chamfered_oct_prism(3.80, 2.80, 0.36, center=(0.0, 0.18, 0.0), chamfer=0.65))
        kit.add("gunmetal", make_chamfered_oct_prism(1.35, 1.35, 5.40, center=(0.0, 3.00, -0.55), chamfer=0.35, top_scale=0.80))
        kit.add("steel_machined", make_beveled_box((7.40, 0.42, 0.95), center=(0.0, 5.45, 0.45), bevel=0.05))
        kit.add("led_cyan", make_beveled_box((7.30, 0.08, 1.02), center=(0.0, 5.45, 0.45), bevel=0.01))
        kit.add("accent_orange", make_beveled_box((2.40, 0.65, 0.45), center=(0.0, 4.95, 0.45), bevel=0.04))
        _add_shuttle_car(0.0, 4.15, 0.45, length=4.4)

    else:
        kit.add("gunmetal", make_chamfered_oct_prism(7.60, 3.20, 0.32, center=(0.0, 0.16, 0.0), chamfer=0.65))
        for px in [-2.8, 0.0, 2.8]:
            kit.add("steel_machined", make_cylinder(0.24, 0.18, 4.10, center=(px, 2.20, -0.45), segments=10))
            kit.add("led_amber", make_closed_torus_ring(0.28, 0.04, center=(px, 3.80, -0.45), n_major=10, n_minor=5))
        kit.add("carbon_slate", make_beveled_box((7.50, 0.30, 1.65), center=(0.0, 4.25, 0.0), bevel=0.04))
        kit.add("led_cyan", make_beveled_box((7.40, 0.07, 1.72), center=(0.0, 4.35, 0.0), bevel=0.01))
        _add_shuttle_car(0.0, 5.02, 0.0, length=4.2, glass_key="glass_emerald")

    adjust_kit_budget(kit, min_tris=1950, max_tris=4000, y_base=0.38, radius=1.35)
    out_dir = os.path.join(OUT_PROPS_ROOT, "prop_01")
    os.makedirs(out_dir, exist_ok=True)
    out_p = os.path.join(out_dir, f"prop_01_r1_{cand_id:02d}.glb")
    return center_and_export_glb(out_p, kit.to_submeshes(f"Prop01_C{cand_id:02d}"), root_name=f"Prop01_R1_{cand_id:02d}")


def build_prop_02_candidate(cand_id: int, mats: Dict[str, PBRMaterialDef]) -> Dict[str, any]:
    kit = BuildingKit(mats)

    def _add_holo_cylinder_case(cx: float, cy: float, cz: float, wx: float = 0.96, hy: float = 0.96, dz: float = 0.42):
        kit.add("led_cyan", make_closed_torus_ring(min(wx, hy) * 0.34, 0.022, center=(cx, cy, cz), rot_xyz_deg=(28.0, 18.0, 0.0), n_major=14, n_minor=6))
        kit.add("led_uv", make_closed_torus_ring(min(wx, hy) * 0.26, 0.018, center=(cx, cy, cz), rot_xyz_deg=(-35.0, -22.0, 0.0), n_major=12, n_minor=6))
        kit.add("led_cyan", transform_geom(make_cylinder(0.11, 0.11, wx * 0.52, segments=12, axis="x"), translate=(cx, cy, cz), rot_xyz_deg=(0.0, -16.0, 12.0)))
        kit.add("steel_machined", make_cylinder(0.18, 0.22, 0.06, center=(cx, cy - hy * 0.45, cz), segments=10))
        kit.add("glass_cyan", make_chamfered_oct_prism(wx, dz, hy, center=(cx, cy, cz), chamfer=0.12))

    if cand_id == 1:
        kit.add("gunmetal", make_chamfered_oct_prism(1.80, 1.40, 0.26, center=(0.0, 0.13, 0.0), chamfer=0.38))
        kit.add("led_amber", make_chamfered_oct_prism(1.84, 1.44, 0.05, center=(0.0, 0.10, 0.0), chamfer=0.38))
        kit.add("carbon_slate", make_chamfered_oct_prism(1.22, 0.72, 1.15, center=(0.0, 0.82, 0.0), chamfer=0.24))
        kit.add("accent_orange", make_beveled_box((0.68, 0.58, 0.76), center=(0.0, 0.78, 0.0), bevel=0.03))
        _add_holo_cylinder_case(0.0, 1.92, 0.0, wx=1.08, hy=1.02, dz=0.46)
        kit.add("marquee", make_chamfered_oct_prism(1.30, 0.78, 0.24, center=(0.0, 2.56, 0.0), chamfer=0.25))

    elif cand_id == 2:
        kit.add("gunmetal", make_chamfered_oct_prism(2.45, 1.45, 0.26, center=(0.0, 0.13, 0.0), chamfer=0.42))
        kit.add("led_amber", make_chamfered_oct_prism(2.50, 1.50, 0.05, center=(0.0, 0.10, 0.0), chamfer=0.42))
        kit.add("aero_white", make_chamfered_oct_prism(1.18, 0.82, 2.35, center=(-0.52, 1.42, 0.0), chamfer=0.24))
        kit.add("gunmetal", make_beveled_box((1.22, 0.22, 0.86), center=(-0.52, 2.52, 0.0), bevel=0.03))
        kit.add("accent_orange", make_beveled_box((0.72, 0.78, 0.86), center=(-0.52, 0.88, 0.0), bevel=0.03))
        kit.add("steel_machined", make_cylinder(0.08, 0.08, 0.90, center=(-0.28, 0.88, 0.0), segments=10, axis="z"))
        kit.add("marquee", make_beveled_box((0.84, 0.56, 0.86), center=(-0.52, 1.78, 0.0), bevel=0.02))
        kit.add("led_cyan", make_beveled_box((0.08, 2.20, 0.88), center=(-1.08, 1.42, 0.0), bevel=0.01))
        kit.add("carbon_slate", make_chamfered_oct_prism(1.04, 0.84, 0.52, center=(0.58, 0.50, 0.0), chamfer=0.22))
        _add_holo_cylinder_case(0.58, 1.62, 0.0, wx=0.98, hy=1.68, dz=0.72)
        kit.add("steel_machined", make_chamfered_oct_prism(1.06, 0.86, 0.20, center=(0.58, 2.56, 0.0), chamfer=0.22))

    elif cand_id == 3:
        kit.add("gunmetal", make_chamfered_oct_prism(2.80, 1.40, 0.24, center=(0.0, 0.12, 0.0), chamfer=0.42))
        for wx_s in [-0.88, 0.88]:
            kit.add("carbon_slate", make_chamfered_oct_prism(0.68, 0.72, 2.30, center=(wx_s, 1.38, 0.0), chamfer=0.16))
            kit.add("accent_orange", make_beveled_box((0.46, 0.58, 0.76), center=(wx_s, 0.82, 0.0), bevel=0.03))
        kit.add("aero_white", make_beveled_box((2.55, 0.28, 0.84), center=(0.0, 2.58, 0.0), bevel=0.04))
        _add_holo_cylinder_case(0.0, 1.56, 0.0, wx=1.05, hy=1.45, dz=0.58)

    elif cand_id == 4:
        kit.add("gunmetal", make_chamfered_oct_prism(2.20, 2.20, 0.28, center=(0.0, 0.14, 0.0), chamfer=0.52))
        kit.add("aero_white", make_chamfered_oct_prism(1.45, 1.45, 0.92, center=(0.0, 0.72, 0.0), chamfer=0.35))
        kit.add("accent_orange", make_beveled_box((0.62, 0.56, 1.50), center=(0.0, 0.72, 0.0), bevel=0.03))
        _add_holo_cylinder_case(0.0, 1.72, 0.0, wx=1.22, hy=1.08, dz=1.22)
        kit.add("steel_machined", make_cylinder(0.10, 0.04, 1.15, center=(0.0, 2.82, 0.0), segments=10))
        kit.add("led_cyan", make_closed_torus_ring(0.38, 0.035, center=(0.0, 2.95, 0.0), n_major=12, n_minor=6))

    else:
        kit.add("gunmetal", make_chamfered_oct_prism(2.30, 1.60, 0.26, center=(0.0, 0.13, 0.0), chamfer=0.42))
        kit.add("carbon_slate", make_chamfered_oct_prism(0.85, 0.85, 2.55, center=(-0.58, 1.50, -0.15), chamfer=0.20))
        kit.add("accent_orange", make_beveled_box((0.58, 0.82, 0.90), center=(-0.58, 0.95, -0.15), bevel=0.03))
        kit.add("aero_white", make_beveled_box((2.15, 0.24, 1.35), center=(0.12, 2.68, 0.10), bevel=0.04))
        _add_holo_cylinder_case(0.38, 1.52, 0.10, wx=1.08, hy=1.35, dz=0.68)

    adjust_kit_budget(kit, min_tris=1900, max_tris=3800, y_base=0.28, radius=0.75)
    out_dir = os.path.join(OUT_PROPS_ROOT, "prop_02")
    os.makedirs(out_dir, exist_ok=True)
    out_p = os.path.join(out_dir, f"prop_02_r1_{cand_id:02d}.glb")
    return center_and_export_glb(out_p, kit.to_submeshes(f"Prop02_C{cand_id:02d}"), root_name=f"Prop02_R1_{cand_id:02d}")


def build_prop_03_candidate(cand_id: int, mats: Dict[str, PBRMaterialDef]) -> Dict[str, any]:
    kit = BuildingKit(mats)

    def _add_vortex_column(cx: float, cy_base: float, cz: float, radius: float = 0.56, height: float = 1.85):
        yc = cy_base + height * 0.5
        kit.add("steel_machined", make_cylinder(0.11, 0.11, height * 0.94, center=(cx, yc, cz), segments=10))
        for i in range(5):
            ry = cy_base + (i + 0.5) / 5.0 * height
            mat_ring = "led_cyan" if (i % 2 == 0) else "led_uv"
            kit.add(mat_ring, make_closed_torus_ring(radius * 0.76, 0.042, center=(cx, ry, cz), n_major=12, n_minor=6))
            kit.add("steel_machined", make_cylinder(radius * 0.82, radius * 0.68, 0.08, center=(cx, ry - 0.08, cz), segments=12))
        kit.add("glass_cyan", make_cylinder(radius, radius, height, center=(cx, yc, cz), segments=14))

    def _add_tether_bollard(bx: float, bz: float):
        kit.add("carbon_slate", make_cylinder(0.24, 0.20, 1.10, center=(bx, 0.76, bz), segments=10))
        kit.add("led_cyan", make_cylinder(0.22, 0.22, 0.10, center=(bx, 1.02, bz), segments=10))
        for z_r in [-0.22, 0.22]:
            kit.add("accent_orange", make_closed_torus_ring(0.11, 0.028, center=(bx, 0.80, bz + z_r), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=10, n_minor=5))

    if cand_id == 1:
        kit.add("gunmetal", make_chamfered_oct_prism(2.80, 1.70, 0.24, center=(0.0, 0.12, 0.0), chamfer=0.45))
        kit.add("led_amber", make_chamfered_oct_prism(2.84, 1.74, 0.05, center=(0.0, 0.09, 0.0), chamfer=0.45))
        _add_vortex_column(0.0, 0.24, 0.0, radius=0.62, height=1.90)
        kit.add("aero_white", make_chamfered_oct_prism(1.38, 1.38, 0.26, center=(0.0, 2.26, 0.0), chamfer=0.32))
        _add_tether_bollard(-1.02, 0.0)
        _add_tether_bollard(1.02, 0.0)

    elif cand_id == 2:
        kit.add("gunmetal", make_chamfered_oct_prism(3.10, 1.75, 0.26, center=(0.0, 0.13, 0.0), chamfer=0.48))
        kit.add("led_amber", make_chamfered_oct_prism(3.14, 1.79, 0.05, center=(0.0, 0.10, 0.0), chamfer=0.48))
        kit.add("gunmetal", make_chamfered_oct_prism(1.36, 1.22, 2.15, center=(-0.68, 1.32, 0.0), chamfer=0.30))
        for lv in range(5):
            ly = 0.56 + lv * 0.36
            kit.add("steel_machined", make_beveled_box((1.42, 0.10, 1.28), center=(-0.68, ly, 0.0), bevel=0.02))
        kit.add("accent_orange", make_closed_torus_ring(0.24, 0.04, center=(-0.68, 1.25, 0.65), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=12, n_minor=6))
        kit.add("accent_orange", make_closed_torus_ring(0.16, 0.032, center=(-1.38, 0.92, 0.0), rot_xyz_deg=(0.0, 0.0, 90.0), n_major=10, n_minor=5))
        _add_vortex_column(0.62, 0.26, 0.0, radius=0.58, height=2.12)
        kit.add("aero_white", make_chamfered_oct_prism(1.26, 1.26, 0.24, center=(0.62, 2.48, 0.0), chamfer=0.28))
        pipe = sample_filleted_polyline([(-0.68, 2.38, 0.0), (-0.68, 2.72, 0.0), (0.62, 2.72, 0.0), (0.62, 2.52, 0.0)], 0.18, 4)
        kit.add("steel_machined", make_swept_tube(pipe, radius=0.12, radial_segments=8))

    elif cand_id == 3:
        kit.add("gunmetal", make_chamfered_oct_prism(3.20, 1.75, 0.24, center=(0.0, 0.12, 0.0), chamfer=0.48))
        _add_vortex_column(-0.72, 0.24, 0.0, radius=0.48, height=1.80)
        _add_vortex_column(0.72, 0.24, 0.0, radius=0.48, height=1.80)
        kit.add("aero_white", make_chamfered_oct_prism(2.65, 1.35, 0.30, center=(0.0, 2.18, 0.0), chamfer=0.35))
        _add_tether_bollard(0.0, 0.45)

    elif cand_id == 4:
        kit.add("gunmetal", make_chamfered_oct_prism(2.70, 1.80, 0.26, center=(0.0, 0.13, 0.0), chamfer=0.45))
        kit.add("carbon_slate", make_chamfered_oct_prism(1.65, 1.35, 0.78, center=(-0.25, 0.64, 0.0), chamfer=0.35))
        _add_vortex_column(-0.25, 1.02, 0.0, radius=0.52, height=1.35)
        _add_tether_bollard(0.92, 0.0)
        kit.add("steel_machined", make_cylinder(0.06, 0.03, 1.15, center=(0.92, 1.85, 0.0), segments=8))

    else:
        kit.add("gunmetal", make_chamfered_oct_prism(3.00, 1.85, 0.26, center=(0.0, 0.13, 0.0), chamfer=0.48))
        kit.add("steel_machined", make_closed_torus_ring(0.85, 0.09, center=(-0.45, 1.25, 0.0), rot_xyz_deg=(25.0, 0.0, 0.0), n_major=14, n_minor=6))
        _add_vortex_column(-0.45, 0.26, 0.0, radius=0.52, height=1.95)
        _add_tether_bollard(0.95, 0.0)

    adjust_kit_budget(kit, min_tris=1900, max_tris=3800, y_base=0.26, radius=0.88)
    out_dir = os.path.join(OUT_PROPS_ROOT, "prop_03")
    os.makedirs(out_dir, exist_ok=True)
    out_p = os.path.join(out_dir, f"prop_03_r1_{cand_id:02d}.glb")
    return center_and_export_glb(out_p, kit.to_submeshes(f"Prop03_C{cand_id:02d}"), root_name=f"Prop03_R1_{cand_id:02d}")


def build_prop_04_candidate(cand_id: int, mats: Dict[str, PBRMaterialDef]) -> Dict[str, any]:
    kit = BuildingKit(mats)

    def _add_bench_seat(cx: float, cz: float, width_x: float = 1.85):
        kit.add("aero_white", make_beveled_box((width_x, 0.26, 0.52), center=(cx, 0.34, cz), bevel=0.04))
        kit.add("led_amber", make_beveled_box((width_x * 0.92, 0.05, 0.42), center=(cx, 0.18, cz), bevel=0.01))
        kit.add(
            "pad_charcoal",
            make_sculpted_cushion((width_x * 0.94, 0.11, 0.46), center=(cx, 0.48, cz), res=(5, 3, 4), roundness=0.35, belly_puff=0.04, crease_freq=0),
        )

    def _add_biodome_planter(cx: float, cy_base: float, cz: float, wx: float = 1.85, dz: float = 1.45, hy: float = 1.45):
        kit.add("aero_white", make_chamfered_oct_prism(wx, dz, 0.52, center=(cx, cy_base + 0.26, cz), chamfer=0.36))
        kit.add("foliage", make_botanical_cluster((cx - 0.32, cy_base + 0.55, cz), radius=0.78, n_leaves=4))
        kit.add("foliage", make_botanical_cluster((cx + 0.32, cy_base + 0.55, cz), radius=0.78, n_leaves=4))
        kit.add("led_uv", make_closed_torus_ring(min(wx, dz) * 0.38, 0.04, center=(cx, cy_base + hy - 0.22, cz), n_major=12, n_minor=6))
        kit.add("steel_machined", make_cylinder(0.08, 0.07, hy, center=(cx, cy_base + hy * 0.5, cz), segments=8))
        kit.add("glass_emerald", make_chamfered_oct_prism(wx * 0.92, dz * 0.92, hy - 0.38, center=(cx, cy_base + 0.52 + (hy - 0.38) * 0.5, cz), chamfer=0.32))

    if cand_id == 1:
        kit.add("gunmetal", make_chamfered_oct_prism(3.50, 2.60, 0.20, center=(0.0, 0.10, 0.0), chamfer=0.65))
        _add_biodome_planter(0.0, 0.20, 0.0, wx=2.10, dz=1.45, hy=1.55)
        _add_bench_seat(0.0, 0.98, width_x=1.95)
        _add_bench_seat(0.0, -0.98, width_x=1.95)

    elif cand_id == 2:
        kit.add("gunmetal", make_chamfered_oct_prism(3.80, 2.40, 0.22, center=(0.0, 0.11, 0.0), chamfer=0.62))
        kit.add("led_amber", make_chamfered_oct_prism(3.84, 2.44, 0.05, center=(0.0, 0.09, 0.0), chamfer=0.62))
        _add_bench_seat(-0.78, 0.58, width_x=2.05)
        _add_bench_seat(-0.78, -0.58, width_x=2.05)
        kit.add("aero_white", make_beveled_box((2.10, 0.68, 0.24), center=(-0.78, 0.72, 0.0), bevel=0.04))
        kit.add("pad_charcoal", make_sculpted_cushion((1.95, 0.42, 0.32), center=(-0.78, 0.76, 0.0), res=(5, 3, 3), roundness=0.35, belly_puff=0.04, crease_freq=0))
        kit.add("accent_orange", make_beveled_box((0.26, 0.56, 1.65), center=(-1.82, 0.48, 0.0), bevel=0.03))
        _add_biodome_planter(1.02, 0.22, 0.0, wx=1.55, dz=1.65, hy=1.95)
        kit.add("aero_white", make_chamfered_oct_prism(1.62, 1.72, 0.22, center=(1.02, 2.28, 0.0), chamfer=0.35))

    elif cand_id == 3:
        kit.add("gunmetal", make_chamfered_oct_prism(3.70, 2.50, 0.20, center=(0.0, 0.10, 0.0), chamfer=0.60))
        _add_biodome_planter(-0.88, 0.20, 0.0, wx=1.45, dz=1.45, hy=1.65)
        _add_biodome_planter(0.88, 0.20, 0.0, wx=1.45, dz=1.45, hy=1.65)
        _add_bench_seat(0.0, 0.96, width_x=2.10)

    elif cand_id == 4:
        kit.add("gunmetal", make_chamfered_oct_prism(3.60, 2.60, 0.22, center=(0.0, 0.11, 0.0), chamfer=0.62))
        kit.add("aero_white", make_chamfered_oct_prism(2.60, 1.80, 0.42, center=(0.0, 0.42, 0.0), chamfer=0.48))
        _add_biodome_planter(0.0, 0.62, 0.0, wx=1.80, dz=1.35, hy=1.50)
        _add_bench_seat(0.0, 1.02, width_x=1.80)

    else:
        kit.add("gunmetal", make_chamfered_oct_prism(3.75, 2.45, 0.22, center=(0.0, 0.11, 0.0), chamfer=0.62))
        _add_biodome_planter(-0.65, 0.22, 0.0, wx=1.85, dz=1.55, hy=1.75)
        _add_bench_seat(0.85, 0.55, width_x=1.55)
        kit.add("steel_machined", make_beveled_box((2.90, 0.16, 1.45), center=(0.15, 2.18, 0.0), bevel=0.03))
        kit.add("accent_orange", make_beveled_box((0.42, 0.88, 0.42), center=(1.42, 0.66, -0.45), bevel=0.03))

    adjust_kit_budget(kit, min_tris=1950, max_tris=3800, y_base=0.24, radius=1.05)
    out_dir = os.path.join(OUT_PROPS_ROOT, "prop_04")
    os.makedirs(out_dir, exist_ok=True)
    out_p = os.path.join(out_dir, f"prop_04_r1_{cand_id:02d}.glb")
    return center_and_export_glb(out_p, kit.to_submeshes(f"Prop04_C{cand_id:02d}"), root_name=f"Prop04_R1_{cand_id:02d}")


def build_prop_05_candidate(cand_id: int, mats: Dict[str, PBRMaterialDef]) -> Dict[str, any]:
    kit = BuildingKit(mats)

    def _add_vtol_deck(cx: float, cz: float, size: float = 5.20):
        kit.add("gunmetal", make_chamfered_oct_prism(size, size, 0.32, center=(cx, 0.16, cz), chamfer=size * 0.24))
        kit.add("carbon_slate", make_chamfered_oct_prism(size * 0.90, size * 0.90, 0.12, center=(cx, 0.36, cz), chamfer=size * 0.21))
        kit.add("marquee", make_chamfered_oct_prism(size * 0.72, size * 0.72, 0.06, center=(cx, 0.43, cz), chamfer=size * 0.17))
        kit.add("led_amber", make_closed_torus_ring(size * 0.38, 0.05, center=(cx, 0.44, cz), n_major=16, n_minor=6))
        kit.add("led_amber", make_beveled_box((0.24, 0.06, size * 0.38), center=(cx - 0.65, 0.44, cz), bevel=0.01))
        kit.add("led_amber", make_beveled_box((0.24, 0.06, size * 0.38), center=(cx + 0.65, 0.44, cz), bevel=0.01))
        kit.add("led_amber", make_beveled_box((1.30, 0.06, 0.24), center=(cx, 0.44, cz), bevel=0.01))
        for sx in [-1.25, 1.25]:
            for sz in [-1.25, 1.25]:
                kit.add("accent_orange", make_beveled_box((0.48, 0.26, 0.36), center=(cx + sx, 0.52, cz + sz), bevel=0.03))
                kit.add("steel_machined", make_cylinder(0.07, 0.07, 0.42, center=(cx + sx, 0.58, cz + sz), segments=8, axis="x"))

    def _add_radar_dish_tower(tx: float, tz: float, tower_h: float = 2.20):
        kit.add("aero_white", make_chamfered_oct_prism(1.55, 1.55, tower_h * 0.55, center=(tx, 0.42 + tower_h * 0.275, tz), chamfer=0.36))
        kit.add("led_cyan", make_closed_torus_ring(0.42, 0.035, center=(tx, 0.42 + tower_h * 0.78, tz), n_major=12, n_minor=5))
        kit.add("glass_cyan", make_chamfered_oct_prism(1.42, 1.42, tower_h * 0.48, center=(tx, 0.42 + tower_h * 0.78, tz), chamfer=0.32))
        kit.add("steel_machined", make_cylinder(0.20, 0.15, 1.15, center=(tx, 0.42 + tower_h + 0.55, tz), segments=10))
        dish_prof = [(0.0, 0.0), (0.42, 0.06), (0.88, 0.24), (1.28, 0.52), (1.35, 0.58)]
        dish = make_lathe_dome(dish_prof, center=(0.0, 0.0, 0.0), segments=14, subdivide_profile=1)
        kit.add("steel_machined", transform_geom(dish, translate=(tx, 0.42 + tower_h + 1.05, tz), rot_xyz_deg=(30.0, 32.0, 0.0)))
        kit.add("led_cyan", make_cylinder(0.08, 0.03, 0.88, center=(tx, 0.42 + tower_h + 1.52, tz + 0.25), segments=8))

    if cand_id == 1:
        _add_vtol_deck(0.0, 0.0, size=5.40)
        _add_radar_dish_tower(0.0, -2.05, tower_h=1.80)

    elif cand_id == 2:
        _add_vtol_deck(-0.85, 0.0, size=5.20)
        _add_radar_dish_tower(2.25, -0.85, tower_h=2.45)
        for bx in [-2.2, -0.85, 0.5]:
            kit.add(
                "carbon_slate",
                transform_geom(make_beveled_box((1.10, 0.68, 0.16), bevel=0.03), translate=(bx, 0.68, -2.35), rot_xyz_deg=(-32.0, 0.0, 0.0)),
            )

    elif cand_id == 3:
        _add_vtol_deck(0.0, 0.35, size=4.80)
        _add_radar_dish_tower(-1.85, -1.65, tower_h=1.95)
        _add_radar_dish_tower(1.85, -1.65, tower_h=1.95)

    elif cand_id == 4:
        _add_vtol_deck(-0.65, 0.0, size=5.00)
        _add_radar_dish_tower(2.10, 0.85, tower_h=2.10)
        sph = [(0.0, -0.65), (0.48, -0.45), (0.68, 0.0), (0.48, 0.45), (0.0, 0.65)]
        kit.add("aero_white", make_lathe_dome(sph, center=(2.10, 1.15, -1.15), segments=12, subdivide_profile=1))

    else:
        _add_vtol_deck(0.0, 0.25, size=5.10)
        _add_radar_dish_tower(-2.05, -1.75, tower_h=2.25)
        kit.add("steel_machined", make_cylinder(0.12, 0.04, 3.40, center=(2.05, 2.10, -1.75), segments=8))
        kit.add("led_cyan", make_closed_torus_ring(0.45, 0.04, center=(2.05, 3.20, -1.75), n_major=12, n_minor=5))

    adjust_kit_budget(kit, min_tris=2150, max_tris=3850, y_base=0.45, radius=1.65)
    out_dir = os.path.join(OUT_PROPS_ROOT, "prop_05")
    os.makedirs(out_dir, exist_ok=True)
    out_p = os.path.join(out_dir, f"prop_05_r1_{cand_id:02d}.glb")
    return center_and_export_glb(out_p, kit.to_submeshes(f"Prop05_C{cand_id:02d}"), root_name=f"Prop05_R1_{cand_id:02d}")


# ==============================================================================
# PART B: 5 DISTRICT IV BUILDING EXTERIORS (`bldg_16` .. `bldg_20`, 25 GLBs)
# Strictly 3,500 - 6,000 triangles per .glb
# ==============================================================================
DISTRICT_4_CONFIGS = [
    {
        "id": 16,
        "slug": "bldg_16_shipyard_drydock_hall",
        "width": 12.5,
        "depth": 10.5,
        "height": 19.5,
        "n_floors": 5,
        "primary_mat": "gunmetal",
        "glass_mat": "glass_cyan",
        "interior_theme": "docking",
        "has_helipad": False,
        "has_dish": False,
        "spire_h": 3.4,
    },
    {
        "id": 17,
        "slug": "bldg_17_coriolis_recreation_arena",
        "width": 12.5,
        "depth": 10.5,
        "height": 17.5,
        "n_floors": 4,
        "primary_mat": "aero_white",
        "glass_mat": "glass_cyan",
        "interior_theme": "holo",
        "has_helipad": False,
        "has_dish": False,
        "spire_h": 2.8,
    },
    {
        "id": 18,
        "slug": "bldg_18_colonial_holo_museum",
        "width": 12.0,
        "depth": 10.5,
        "height": 18.5,
        "n_floors": 4,
        "primary_mat": "aero_white",
        "glass_mat": "glass_emerald",
        "interior_theme": "holo",
        "has_helipad": False,
        "has_dish": False,
        "spire_h": 3.2,
    },
    {
        "id": 19,
        "slug": "bldg_19_synth_brewery_refinery",
        "width": 12.0,
        "depth": 10.0,
        "height": 18.0,
        "n_floors": 4,
        "primary_mat": "aero_white",
        "glass_mat": "glass_cyan",
        "interior_theme": "distillation",
        "has_helipad": False,
        "has_dish": False,
        "spire_h": 3.0,
    },
    {
        "id": 20,
        "slug": "bldg_20_meteor_defense_bastion",
        "width": 12.5,
        "depth": 10.5,
        "height": 20.5,
        "n_floors": 5,
        "primary_mat": "gunmetal",
        "glass_mat": "glass_cyan",
        "interior_theme": "plasma",
        "has_helipad": False,
        "has_dish": True,
        "spire_h": 3.8,
    },
]

_orig_sig_fn = beg.add_building_specific_signature_features


def _extended_signature_features(
    kit: BuildingKit,
    bldg_id: int,
    cand_id: int,
    main_cx: float,
    sec_cx: float,
    top_y: float,
):
    if bldg_id <= 15:
        return _orig_sig_fn(kit, bldg_id, cand_id, main_cx, sec_cx, top_y)

    if bldg_id == 16:
        kit.add("accent_orange", make_beveled_box((3.20, 3.60, 0.36), center=(main_cx, 3.10, 3.95), bevel=0.05))
        crane_pts = sample_filleted_polyline(
            [(main_cx - 3.2, top_y - 0.5, 0.0), (main_cx - 3.0, top_y + 2.2, 0.0), (sec_cx + 1.4, top_y + 2.2, 0.0), (sec_cx + 1.6, top_y - 0.5, 0.0)],
            fillet_radius=0.85,
            corner_subdivs=4,
        )
        kit.add("steel_machined", make_swept_tube(crane_pts, radius=0.24, radial_segments=8))
        sh_y = 8.5
        kit.add("aero_white", make_cylinder(0.68, 0.24, 4.80, center=(sec_cx, sh_y, 0.0), segments=10))
        kit.add("accent_orange", make_beveled_box((2.45, 1.85, 0.18), center=(sec_cx, sh_y - 0.6, 0.0), bevel=0.03))
        kit.add("led_cyan", make_closed_torus_ring(1.35, 0.06, center=(sec_cx, sh_y + 0.8, 0.0), n_major=12, n_minor=5))

    elif bldg_id == 17:
        kit.add("glass_cyan", make_chamfered_oct_prism(5.80, 5.20, 1.35, center=(main_cx, top_y + 0.45, 0.0), chamfer=1.15, top_scale=0.72))
        kit.add("marquee", make_beveled_box((3.60, 0.72, 0.22), center=(main_cx, top_y - 1.25, 3.85), bevel=0.03))
        for r_y, tilt in [(5.5, 18.0), (9.0, -18.0), (12.5, 16.0)]:
            kit.add("steel_machined", make_closed_torus_ring(1.95, 0.14, center=(sec_cx, r_y, 0.0), rot_xyz_deg=(tilt, 0.0, 0.0), n_major=12, n_minor=5))
            kit.add("led_amber", make_closed_torus_ring(1.78, 0.055, center=(sec_cx, r_y, 0.0), rot_xyz_deg=(tilt, 0.0, 0.0), n_major=12, n_minor=5))

    elif bldg_id == 18:
        dome_prof = [(0.0, 3.1), (1.35, 2.90), (2.40, 2.20), (3.00, 1.15), (3.15, 0.0)]
        kit.add("glass_emerald", make_lathe_dome(dome_prof, center=(main_cx, top_y - 2.8, 0.0), segments=14, subdivide_profile=1))
        earth_prof = [(0.0, -0.95), (0.68, -0.68), (0.95, 0.0), (0.68, 0.68), (0.0, 0.95)]
        kit.add("led_cyan", make_lathe_dome(earth_prof, center=(main_cx, top_y - 1.2, 0.0), segments=12, subdivide_profile=1))
        kit.add("led_uv", make_closed_torus_ring(1.85, 0.06, center=(main_cx, top_y - 1.2, 0.0), rot_xyz_deg=(23.5, 15.0, 0.0), n_major=12, n_minor=5))

    elif bldg_id == 19:
        for z_tk in [-2.4, 2.4]:
            kit.add("steel_machined", make_cylinder(0.88, 0.88, 7.50, center=(main_cx - 2.1, 5.0, z_tk), segments=12))
            kit.add("led_amber", make_closed_torus_ring(0.92, 0.06, center=(main_cx - 2.1, 7.2, z_tk), n_major=12, n_minor=5))
            kit.add("led_uv", make_closed_torus_ring(0.92, 0.06, center=(main_cx - 2.1, 4.2, z_tk), n_major=12, n_minor=5))
        pipe_pts = sample_filleted_polyline(
            [(main_cx, top_y - 0.5, 0.0), (main_cx, top_y + 1.4, 0.0), (sec_cx, top_y + 1.4, 0.0), (sec_cx, top_y - 0.8, 0.0)],
            fillet_radius=0.65,
            corner_subdivs=4,
        )
        kit.add("accent_orange", make_swept_tube(pipe_pts, radius=0.22, radial_segments=8))

    elif bldg_id == 20:
        for b_z in [-2.6, 2.6]:
            kit.add(
                "gunmetal",
                transform_geom(make_beveled_box((0.72, 8.20, 1.40), bevel=0.06), translate=(main_cx - 3.1, 5.2, b_z), rot_xyz_deg=(0.0, 0.0, -14.0)),
            )
        kit.add("gunmetal", make_chamfered_oct_prism(3.20, 3.20, 1.35, center=(main_cx, top_y + 0.65, 0.0), chamfer=0.75, top_scale=0.82))
        for z_brl in [-0.55, 0.55]:
            kit.add(
                "steel_machined",
                transform_geom(
                    make_cylinder(0.26, 0.18, 4.20, segments=10),
                    translate=(main_cx + 0.6, top_y + 1.85, z_brl),
                    rot_xyz_deg=(0.0, 0.0, -48.0),
                ),
            )
            kit.add(
                "led_cyan",
                transform_geom(
                    make_cylinder(0.28, 0.28, 0.45, segments=10),
                    translate=(main_cx + 1.8, top_y + 2.95, z_brl),
                    rot_xyz_deg=(0.0, 0.0, -48.0),
                ),
            )
        kit.add("accent_orange", make_beveled_box((1.65, 0.95, 2.10), center=(main_cx, top_y + 1.25, 0.0), bevel=0.05))


beg.add_building_specific_signature_features = _extended_signature_features
for d4_cfg in DISTRICT_4_CONFIGS:
    if not any(c["id"] == d4_cfg["id"] for c in beg.BUILDING_CONFIGS):
        beg.BUILDING_CONFIGS.append(d4_cfg)


def build_all_phase3():
    prop_mats = get_prop_materials()
    bldg_mats = get_building_materials()

    prop_builders = [
        (1, build_prop_01_candidate),
        (2, build_prop_02_candidate),
        (3, build_prop_03_candidate),
        (4, build_prop_04_candidate),
        (5, build_prop_05_candidate),
    ]

    prop_results = []
    for p_id, fn in prop_builders:
        for cand_id in range(1, 6):
            info = fn(cand_id, prop_mats)
            fname = os.path.basename(info["filepath"])
            dims = info["dimensions"]
            sz_kb = os.path.getsize(info["filepath"]) / 1024.0
            print(
                f"[prop_{p_id:02d}] {fname:22s} | {dims[0]:5.2f}m W x {dims[2]:5.2f}m D x {dims[1]:5.2f}m H | "
                f"tris={info['triangles']:4d} | min_y={info['min'][1]:.5f} | {sz_kb:6.1f} KB"
            )
            prop_results.append(info)

    bldg_d4_results = beg.build_district_range(16, 20)

    phase3_man_path = os.path.join(OUT_BLDG_ROOT, "phase3_50_manifest.json")
    with open(phase3_man_path, "w") as f:
        json.dump({"props_25": prop_results, "buildings_district4_25": bldg_d4_results}, f, indent=2)

    b75_path = os.path.join(OUT_BLDG_ROOT, "buildings_75_manifest.json")
    if os.path.exists(b75_path):
        with open(b75_path, "r") as f:
            b75 = json.load(f)
        existing_map = {b["filepath"]: b for b in b75.get("buildings", [])}
        for b in bldg_d4_results:
            existing_map[b["filepath"]] = b
        b75["buildings"] = list(existing_map.values())
        b75["props_25"] = prop_results
        with open(b75_path, "w") as f:
            json.dump(b75, f, indent=2)

    print(f"Exported {len(prop_results)} prop GLBs and {len(bldg_d4_results)} District IV building GLBs!")


if __name__ == "__main__":
    build_all_phase3()
