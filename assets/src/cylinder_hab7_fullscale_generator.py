#!/usr/bin/env python3
"""
Builds all 5 Full-Scale (800m length x 400m diameter, R = 200m true 1:1 scale)
O'Neill Cylinder Hab-7 Concept Candidate .glb models:
  /workspace/game-project/assets/glb/cylinder/cylinder_r1_01.glb .. cylinder_r1_05.glb

Owner: Rook (3D Modeling Specialist)
Follows the Unified "Aegis-7 Standard":
  - Exact 1:1 Full Scale: 800.00m length (X in [-400m, +400m]) x 400.00m diameter
    (Y in [0.0m, 400.0m], Z in [-200.0m, +200.0m], cylinder axis at Y = 200.0m, Z = 0.0m)
  - Bottom-center (0.0, 0.0, 0.0) floor pivot (min_y == 0.00000), front facing +Z
  - Triangle budget: ~6,000 - 11,500 triangles per .glb (within 5,000 - 12,000 tris)
  - True `alphaMode: "BLEND"` translucent solarium windows, biodome strips, and cryo-tanks
    revealing 3D interior curved land-strips, 4-district city skylines, emerald agri-belts,
    mag-lev transit rings, and the 800m Axial Zero-G Solar/Docking Core Spine!
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
    BuildingKit,
)

OUT_CYL_DIR = "/workspace/game-project/assets/glb/cylinder"
os.makedirs(OUT_CYL_DIR, exist_ok=True)

CYL_Y = 200.0  # Center axis Y so bottom of R=200m hull sits at Y = 0.0m


# ==============================================================================
# CYLINDER ARC SHELL & RADIAL TRANSFORM HELPERS
# ==============================================================================
def make_cyl_arc_shell(
    x0: float,
    x1: float,
    r_in: float,
    r_out: float,
    theta0_deg: float,
    theta1_deg: float,
    segs_theta: int = 6,
    center_y: float = CYL_Y,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Builds a 3D watertight curved cylindrical sector shell along the X axis
    from x0 to x1, inner radius r_in, outer radius r_out, and angular span
    [theta0_deg, theta1_deg] around (Y = center_y, Z = 0.0).
    Produces 2 * (4 * segs_theta + 4) triangles.
    """
    t0 = math.radians(theta0_deg)
    t1 = math.radians(theta1_deg)
    thetas = [t0 + (t1 - t0) * (i / float(segs_theta)) for i in range(segs_theta + 1)]

    pos_list, norm_list, uv_list, idx_list = [], [], [], []

    def _add_quad(p0, p1, p2, p3):
        b = len(pos_list)
        pts = np.array([p0, p1, p2, p3], dtype=np.float32)
        n = np.cross(pts[1] - pts[0], pts[2] - pts[0])
        n_len = np.linalg.norm(n)
        n = n / (n_len if n_len > 1e-12 else 1.0)
        pos_list.extend(pts)
        norm_list.extend([n, n, n, n])
        uv_list.extend([[0.0, 1.0], [1.0, 1.0], [1.0, 0.0], [0.0, 0.0]])
        idx_list.append([b, b + 1, b + 2])
        idx_list.append([b, b + 2, b + 3])

    for i in range(segs_theta):
        a0, a1 = thetas[i], thetas[i + 1]
        cy0, sz0 = math.cos(a0), math.sin(a0)
        cy1, sz1 = math.cos(a1), math.sin(a1)

        # Outer hull surface (outward normal)
        _add_quad(
            [x0, center_y + r_out * cy0, r_out * sz0],
            [x1, center_y + r_out * cy0, r_out * sz0],
            [x1, center_y + r_out * cy1, r_out * sz1],
            [x0, center_y + r_out * cy1, r_out * sz1],
        )
        # Inner concave surface (inward normal toward cylinder axis)
        _add_quad(
            [x0, center_y + r_in * cy1, r_in * sz1],
            [x1, center_y + r_in * cy1, r_in * sz1],
            [x1, center_y + r_in * cy0, r_in * sz0],
            [x0, center_y + r_in * cy0, r_in * sz0],
        )
        # X0 end cap (-X normal)
        _add_quad(
            [x0, center_y + r_in * cy0, r_in * sz0],
            [x0, center_y + r_out * cy0, r_out * sz0],
            [x0, center_y + r_out * cy1, r_out * sz1],
            [x0, center_y + r_in * cy1, r_in * sz1],
        )
        # X1 end cap (+X normal)
        _add_quad(
            [x1, center_y + r_in * cy1, r_in * sz1],
            [x1, center_y + r_out * cy1, r_out * sz1],
            [x1, center_y + r_out * cy0, r_out * sz0],
            [x1, center_y + r_in * cy0, r_in * sz0],
        )

    # Theta0 and Theta1 longitudinal edge caps
    for a_edge, flip in [(thetas[0], False), (thetas[-1], True)]:
        cy, sz = math.cos(a_edge), math.sin(a_edge)
        p_in0 = [x0, center_y + r_in * cy, r_in * sz]
        p_in1 = [x1, center_y + r_in * cy, r_in * sz]
        p_out1 = [x1, center_y + r_out * cy, r_out * sz]
        p_out0 = [x0, center_y + r_out * cy, r_out * sz]
        if not flip:
            _add_quad(p_in0, p_in1, p_out1, p_out0)
        else:
            _add_quad(p_out0, p_out1, p_in1, p_in0)

    return (
        np.array(pos_list, dtype=np.float32),
        np.array(norm_list, dtype=np.float32),
        np.array(uv_list, dtype=np.float32),
        np.array(idx_list, dtype=np.uint32),
    )


def make_axial_ring(
    x_pos: float,
    r_in: float,
    r_out: float,
    width_x: float,
    segs: int = 20,
    center_y: float = CYL_Y,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Builds a full 360-degree structural spin-rib / docking ring around the X-axis at x_pos."""
    return make_cyl_arc_shell(
        x_pos - width_x * 0.5,
        x_pos + width_x * 0.5,
        r_in,
        r_out,
        0.0,
        360.0,
        segs_theta=segs,
        center_y=center_y,
    )


def place_inward_on_cylinder(
    geom: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    x_pos: float,
    theta_deg: float,
    r_floor: float = 186.0,
    center_y: float = CYL_Y,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Places a local building/tower geometry (whose local +Y is up) onto the inner concave
    wall of the O'Neill Cylinder at (x_pos, theta_deg, r_floor) so its local +Y points
    radially INWARD toward the cylinder central axis (Y = center_y, Z = 0.0)!
    """
    rad = math.radians(theta_deg)
    cy, sz = math.cos(rad), math.sin(rad)
    # At angle theta_deg (measured from +Y toward +Z):
    # Outward radial vector is (0, cos(theta), sin(theta))
    # Inward radial vector (+Y_local) is (0, -cos(theta), -sin(theta))
    # Rotating around X by (180 + theta_deg) maps local (0, 1, 0) -> (0, -cos(theta), -sin(theta))
    rot_x = 180.0 + theta_deg
    ty = center_y + r_floor * cy
    tz = r_floor * sz
    return transform_geom(geom, translate=(x_pos, ty, tz), rot_xyz_deg=(rot_x, 0.0, 0.0))


# ==============================================================================
# SHARED INTERIOR 800m AXIAL ZERO-G SOLAR CORE SPINE & 3D CITY SKYLINE BUILDERS
# ==============================================================================
def add_axial_zero_g_solar_spine(
    kit: BuildingKit,
    x_start: float = -385.0,
    x_end: float = 385.0,
    n_nodes: int = 7,
    n_spoke_rings: int = 3,
):
    """
    Builds the 800m full-length Axial Zero-G Solar/Daylight & Docking Core Spine
    running along (Y = 200m, Z = 0m) inside the cylinder:
      - Central glowing cyan (#00E5FF) & amber (#FF9500) plasma daylight beam column
      - Brushed-steel axial zero-G transport tube & octahedral transfer hub stations
      - Radial zero-G elevator spoke cables connecting the axial core to the inner hull
      - Toroidal UV-violet (#7B5CFF) & cyan solar-regulating field rings
    """
    length = x_end - x_start
    cx = 0.5 * (x_start + x_end)

    # Central glowing cyan plasma daylight core rod & brushed-steel conduit spine
    kit.add(
        "led_cyan",
        make_cylinder(5.5, 5.5, length, center=(cx, CYL_Y, 0.0), segments=14, axis="x"),
    )
    kit.add(
        "steel_machined",
        make_cylinder(8.2, 8.2, length * 0.96, center=(cx, CYL_Y, 0.0), segments=12, axis="x"),
    )

    # Axial Zero-G Transfer Hub Stations & Solar-Regulator Field Rings along the 800m spine
    for i in range(n_nodes):
        nx = x_start + (i + 0.5) / float(n_nodes) * length
        kit.add("aero_white", make_axial_ring(nx, r_in=8.5, r_out=21.0, width_x=18.0, segs=12))
        kit.add("glass_cyan", make_axial_ring(nx, r_in=19.0, r_out=24.0, width_x=12.0, segs=12))
        led_k = "led_amber" if (i % 2 == 0) else "led_uv"
        kit.add(led_k, make_axial_ring(nx - 11.0, r_in=9.0, r_out=16.5, width_x=4.5, segs=12))
        kit.add("led_cyan", make_axial_ring(nx + 11.0, r_in=9.0, r_out=16.5, width_x=4.5, segs=12))

    # Radial zero-G elevator spoke cables connecting axial spine to inner hull
    for s_i in range(n_spoke_rings):
        sx = x_start + (s_i + 1.0) / float(n_spoke_rings + 1) * length
        for ang_deg in [0.0, 60.0, 120.0, 180.0, 240.0, 300.0]:
            rad = math.radians(ang_deg)
            cy, sz = math.cos(rad), math.sin(rad)
            pts = np.array(
                [
                    [sx, CYL_Y + 14.0 * cy, 14.0 * sz],
                    [sx, CYL_Y + 186.0 * cy, 186.0 * sz],
                ],
                dtype=np.float32,
            )
            kit.add("steel_machined", make_swept_tube(pts, radius=1.8, radial_segments=6, capped=False))
            kit.add(
                "accent_orange",
                make_beveled_box(
                    (7.0, 7.0, 7.0),
                    center=(sx, CYL_Y + 98.0 * cy, 98.0 * sz),
                    bevel=0.8,
                ),
            )


def add_interior_land_strip_and_city_skyline(
    kit: BuildingKit,
    x0: float,
    x1: float,
    theta0_deg: float,
    theta1_deg: float,
    r_hull_in: float = 186.0,
    n_longitudinal_rows: int = 6,
):
    """
    Populates a curved interior land-valley sector with:
      - Curved carbon-slate boulevard & emerald botanical park belts
      - Continuous glowing cyan & amber mag-lev transit guideway lines
      - 3D Aegis-7 City District Towers (65/35 stepped aerospace-white & gunmetal towers,
        illuminated window grids, and translucent cyan/emerald bio-towers) pointing
        radially inward toward the cylinder axis!
    """
    t_mid = 0.5 * (theta0_deg + theta1_deg)
    t_span = (theta1_deg - theta0_deg)

    # 1. Interior emerald agri-parkland strip & cyan hydro-reclamation canal along valley center
    kit.add(
        "foliage",
        make_cyl_arc_shell(x0 + 8.0, x1 - 8.0, r_hull_in - 1.8, r_hull_in, t_mid - t_span * 0.36, t_mid + t_span * 0.36, segs_theta=4),
    )
    kit.add(
        "led_cyan",
        make_cyl_arc_shell(x0 + 10.0, x1 - 10.0, r_hull_in - 2.6, r_hull_in - 1.5, t_mid - 2.2, t_mid + 2.2, segs_theta=2),
    )
    for rail_off in [-t_span * 0.24, t_span * 0.24]:
        kit.add(
            "led_amber",
            make_cyl_arc_shell(x0 + 10.0, x1 - 10.0, r_hull_in - 2.4, r_hull_in - 1.5, t_mid + rail_off - 1.2, t_mid + rail_off + 1.2, segs_theta=1),
        )

    # 2. 3D Interior City District Towers oriented radially inward toward the cylinder center axis
    for r_idx in range(n_longitudinal_rows):
        bx = x0 + (r_idx + 0.5) / float(n_longitudinal_rows) * (x1 - x0)
        for side_idx, t_off in enumerate([-t_span * 0.18, t_span * 0.18]):
            b_theta = t_mid + t_off
            b_h = 26.0 + ((r_idx + side_idx) % 3) * 11.0
            # Primary 65% aerospace-white/window-lit tower mass + 35% translucent atrium spire
            t_plinth = make_beveled_box((22.0, 3.5, 18.0), center=(0.0, 1.75, 0.0), bevel=0.0)
            t_main = make_chamfered_oct_prism(14.0, 14.0, b_h, center=(-3.5, 3.5 + b_h * 0.5, 0.0), chamfer=2.6, top_scale=0.82, capped=False)
            t_win = make_beveled_box((14.6, b_h * 0.78, 10.5), center=(-3.5, 3.5 + b_h * 0.5, 0.0), bevel=0.0)
            t_glass = make_chamfered_oct_prism(8.5, 11.0, b_h * 1.08, center=(5.2, 3.5 + b_h * 0.54, 0.0), chamfer=1.8, capped=False)
            t_core = make_beveled_box((3.8, b_h * 1.10, 3.8), center=(5.2, 3.5 + b_h * 0.55, 0.0), bevel=0.0)

            kit.add("gunmetal", place_inward_on_cylinder(t_plinth, bx, b_theta, r_floor=r_hull_in))
            kit.add("aero_white" if (r_idx % 2 == 0) else "carbon_slate", place_inward_on_cylinder(t_main, bx, b_theta, r_floor=r_hull_in))
            kit.add("window_lit", place_inward_on_cylinder(t_win, bx, b_theta, r_floor=r_hull_in))
            kit.add("glass_cyan" if (side_idx == 0) else "glass_emerald", place_inward_on_cylinder(t_glass, bx, b_theta, r_floor=r_hull_in))
            kit.add("led_cyan" if (r_idx % 2 == 0) else "led_uv", place_inward_on_cylinder(t_core, bx, b_theta, r_floor=r_hull_in))


def add_hemispherical_or_stepped_endcaps(
    kit: BuildingKit,
    x_fwd: float = -290.0,
    x_aft: float = 290.0,
    include_aft_fusion_drive: bool = True,
):
    """
    Builds the forward (-X) Starport Docking Endcap Bowl and aft (+X) Endcap / D-He3
    Magnetic-Confinement Fusion Drive Assembly so the cylinder spans exactly X = -400m .. +400m.
    """
    # Forward Endcap (-X: x_fwd down to -400.0m)
    fwd_steps = [
        (x_fwd - 18.0, x_fwd, 152.0, 194.0),
        (x_fwd - 38.0, x_fwd - 18.0, 112.0, 160.0),
        (x_fwd - 58.0, x_fwd - 38.0, 72.0, 118.0),
        (x_fwd - 78.0, x_fwd - 58.0, 36.0, 78.0),
    ]
    for idx_s, (xa, xb, r_i, r_o) in enumerate(fwd_steps):
        mat_s = "aero_white" if (idx_s % 2 == 0) else "gunmetal"
        kit.add(mat_s, make_axial_ring(0.5 * (xa + xb), r_in=r_i, r_out=r_o, width_x=(xb - xa), segs=16))
    # Forward Translucent Starport Observation Ring & Signal-Orange Axial Docking Collar at X = -400.0m
    kit.add("glass_cyan", make_axial_ring(x_fwd - 28.0, r_in=115.0, r_out=163.0, width_x=10.0, segs=16))
    kit.add("steel_machined", make_axial_ring(-382.0, r_in=24.0, r_out=54.0, width_x=22.0, segs=16))
    kit.add("accent_orange", make_axial_ring(-396.0, r_in=18.0, r_out=42.0, width_x=8.0, segs=16))
    kit.add("led_cyan", make_axial_ring(-398.5, r_in=14.0, r_out=32.0, width_x=3.0, segs=16))

    # Aft Endcap (+X: x_aft up to +400.0m)
    aft_steps = [
        (x_aft, x_aft + 20.0, 148.0, 194.0),
        (x_aft + 20.0, x_aft + 42.0, 104.0, 156.0),
        (x_aft + 42.0, x_aft + 64.0, 62.0, 110.0),
    ]
    for idx_s, (xa, xb, r_i, r_o) in enumerate(aft_steps):
        mat_s = "gunmetal" if (idx_s % 2 == 0) else "carbon_slate"
        kit.add(mat_s, make_axial_ring(0.5 * (xa + xb), r_in=r_i, r_out=r_o, width_x=(xb - xa), segs=16))

    if include_aft_fusion_drive:
        # 5-Coil Toroidal D-He3 Magnetic-Nozzle Fusion Spin/Impulse Drive Crown (up to X = +400.0m)
        for c_i in range(5):
            cx_coil = x_aft + 56.0 + c_i * 11.0
            r_coil = 72.0 - c_i * 6.5
            kit.add("steel_machined", make_axial_ring(cx_coil, r_in=r_coil - 8.0, r_out=r_coil + 8.0, width_x=5.5, segs=12))
            kit.add("led_cyan" if (c_i % 2 == 0) else "led_amber", make_axial_ring(cx_coil, r_in=r_coil - 11.0, r_out=r_coil - 5.0, width_x=3.5, segs=16))
        # Translucent Radiation Shield Nozzle & Blazing Plasma Plume Core reaching exactly X = +400.0m
        kit.add("glass_cyan", make_axial_ring(378.0, r_in=34.0, r_out=56.0, width_x=36.0, segs=12))
        kit.add("led_cyan", make_cylinder(26.0, 12.0, 56.0, center=(372.0, CYL_Y, 0.0), segments=16, axis="x"))
        kit.add("accent_orange", make_axial_ring(397.0, r_in=38.0, r_out=52.0, width_x=6.0, segs=16))


# ==============================================================================
# CANDIDATE 01: CLASSIC 3-LAND / 3-WINDOW ALTERNATING SOLARIUM CYLINDER (800m x 400m)
# ==============================================================================
def build_cylinder_01_classic_solarium(mats: Dict[str, PBRMaterialDef]) -> Dict[str, any]:
    kit = BuildingKit(mats)
    x_body0, x_body1 = -280.0, 280.0

    # 1. 7 Full-Circumference 45° Chamfered Octagonal/Cylindrical Gunmetal Spin-Ribs (R = 200m)
    for rx in np.linspace(x_body0, x_body1, 7):
        kit.add("gunmetal", make_axial_ring(float(rx), r_in=191.0, r_out=200.0, width_x=12.0, segs=16))
        kit.add("led_amber", make_axial_ring(float(rx), r_in=198.5, r_out=200.0, width_x=3.0, segs=16))

    # 2. 3 Alternating 60° Land Valleys + 3 Alternating 60° Translucent Solarium Window Valleys (120° periodicity)
    for k in range(3):
        land_t0 = k * 120.0
        land_t1 = land_t0 + 62.0
        win_t0 = land_t0 + 60.0
        win_t1 = land_t0 + 120.0

        # Outer Aerospace-White & Carbon-Slate Hull + Inner Concave City Skyline
        kit.add("aero_white", make_cyl_arc_shell(x_body0, x_body1, 187.0, 195.0, land_t0, land_t1, segs_theta=6))
        kit.add("carbon_slate", make_cyl_arc_shell(x_body0 + 20.0, x_body1 - 20.0, 194.0, 197.0, land_t0 + 10.0, land_t1 - 10.0, segs_theta=4))
        add_interior_land_strip_and_city_skyline(kit, x_body0 + 30.0, x_body1 - 30.0, land_t0 + 6.0, land_t1 - 6.0, r_hull_in=187.0, n_longitudinal_rows=3)

        # Translucent Solarium Window Strip (`alphaMode: "BLEND"`) + Brushed-Steel Mullion Ribs
        kit.add("glass_cyan", make_cyl_arc_shell(x_body0, x_body1, 189.0, 193.0, win_t0, win_t1, segs_theta=6))
        for m_ang in [win_t0 + 20.0, win_t0 + 40.0]:
            kit.add("steel_machined", make_cyl_arc_shell(x_body0, x_body1, 188.5, 194.5, m_ang - 1.5, m_ang + 1.5, segs_theta=1))

        # 3 Giant Articulated External Solar Mirror Wings hinged at the aft endcap (angled outward)
        w_mid = math.radians(win_t0 + 30.0)
        wy = CYL_Y + 188.0 * math.cos(w_mid)
        wz = 188.0 * math.sin(w_mid)
        kit.add("steel_machined", make_cyl_arc_shell(180.0, 340.0, 192.0, 199.5, win_t0 + 8.0, win_t1 - 8.0, segs_theta=4))
        kit.add("glass_emerald", make_cyl_arc_shell(190.0, 330.0, 195.0, 200.0, win_t0 + 12.0, win_t1 - 12.0, segs_theta=4))
        kit.add("accent_orange", make_beveled_box((18.0, 14.0, 14.0), center=(180.0, wy, wz), bevel=1.5))

    add_axial_zero_g_solar_spine(kit, x_start=-375.0, x_end=355.0, n_nodes=4, n_spoke_rings=2)
    add_hemispherical_or_stepped_endcaps(kit, x_fwd=x_body0, x_aft=x_body1, include_aft_fusion_drive=True)

    out_p = os.path.join(OUT_CYL_DIR, "cylinder_r1_01.glb")
    return center_and_export_glb(out_p, kit.to_submeshes("Cyl01"), root_name="CylinderHab7_R1_01_ClassicSolarium")


# ==============================================================================
# CANDIDATE 02: AEGIS-7 DUAL-ZONE SPLIT-MASS O'NEILL CYLINDER & AXIAL CORE SPINE
# (Signature 65/35 Architecture — 520m Main Habitat Drum + 280m Counter-Rotating
#  Zero-G Starport, Heliostat Mirror Array & 5-Coil D-He3 Fusion Drive Assembly)
# ==============================================================================
def build_cylinder_02_aegis7_dual_zone_split(mats: Dict[str, PBRMaterialDef]) -> Dict[str, any]:
    kit = BuildingKit(mats)

    # LEFT 65% PRIMARY ZONE (X = -380m .. +140m, 520m Main Spin-Gravity Habitat Drum):
    x_hab0, x_hab1 = -290.0, 130.0
    for rx in np.linspace(x_hab0, x_hab1, 5):
        kit.add("gunmetal", make_axial_ring(float(rx), r_in=190.0, r_out=200.0, width_x=13.0, segs=16))
        kit.add("led_cyan", make_axial_ring(float(rx) - 4.0, r_in=198.2, r_out=200.0, width_x=2.4, segs=16))
        kit.add("led_amber", make_axial_ring(float(rx) + 4.0, r_in=198.2, r_out=200.0, width_x=2.4, segs=16))

    # 3 Land Valleys + 3 Translucent Cyan/Emerald Solarium & Biodome Window Valleys
    for k in range(3):
        land_t0 = k * 120.0 - 15.0
        land_t1 = land_t0 + 64.0
        win_t0 = land_t0 + 62.0
        win_t1 = land_t0 + 120.0

        kit.add("aero_white", make_cyl_arc_shell(x_hab0, x_hab1, 186.0, 195.0, land_t0, land_t1, segs_theta=6))
        kit.add("carbon_slate", make_cyl_arc_shell(x_hab0 + 15.0, x_hab1 - 15.0, 194.2, 197.2, land_t0 + 8.0, land_t1 - 8.0, segs_theta=4))
        kit.add("marquee", make_cyl_arc_shell(-140.0, -20.0, 196.5, 198.5, land_t0 + 20.0, land_t1 - 20.0, segs_theta=2))
        add_interior_land_strip_and_city_skyline(kit, x_hab0 + 25.0, x_hab1 - 25.0, land_t0 + 6.0, land_t1 - 6.0, r_hull_in=186.0, n_longitudinal_rows=3)

        # Dual-Band Translucent Solarium Window Valley (Cyan Curtain-Wall + Emerald Biosphere Band)
        kit.add("glass_cyan", make_cyl_arc_shell(x_hab0, x_hab1, 188.0, 192.5, win_t0, win_t0 + 38.0, segs_theta=4))
        kit.add("glass_emerald", make_cyl_arc_shell(x_hab0, x_hab1, 188.0, 192.5, win_t0 + 36.0, win_t1, segs_theta=3))
        kit.add("steel_machined", make_cyl_arc_shell(x_hab0, x_hab1, 187.5, 194.5, win_t0 + 35.5, win_t0 + 38.5, segs_theta=1))

    # RIGHT 35% SECONDARY ZONE (X = +130m .. +400m, 270m Counter-Rotating Zero-G Starport,
    # Heliostat Solar-Collector Wing Ring, Translucent Cryo-Tanks & 5-Coil D-He3 Fusion Drive):
    # Counter-rotating zero-G transfer bearing & brushed-steel gantry drum (X = +130m .. +295m)
    kit.add("carbon_slate", make_axial_ring(142.0, r_in=148.0, r_out=198.0, width_x=22.0, segs=16))
    kit.add("led_amber", make_axial_ring(142.0, r_in=196.5, r_out=199.5, width_x=5.0, segs=16))

    for gx in [175.0, 215.0, 255.0, 290.0]:
        kit.add("steel_machined", make_axial_ring(gx, r_in=154.0, r_out=192.0, width_x=10.0, segs=16))
        kit.add("led_cyan", make_axial_ring(gx, r_in=190.0, r_out=194.0, width_x=3.0, segs=16))

    # 6 Full-Length Brushed-Steel Gantry Trusses, 6 Signal-Orange Shuttle Docking Collars,
    # 6 Heliostat Solar Mirror Louver Wings & 6 Translucent Cryo-He3 Propellant Tanks
    for k in range(6):
        ang = k * 60.0
        rad = math.radians(ang)
        cy, sz = math.cos(rad), math.sin(rad)
        # Longitudinal brushed-steel gantry spine beam
        kit.add("steel_machined", make_cyl_arc_shell(140.0, 295.0, 168.0, 182.0, ang - 4.0, ang + 4.0, segs_theta=2))
        # Heliostat solar-collector mirror wing (`glass_cyan` + `aero_white` frame)
        kit.add("glass_cyan", make_cyl_arc_shell(155.0, 280.0, 182.0, 198.0, ang + 8.0, ang + 44.0, segs_theta=4))
        kit.add("aero_white", make_cyl_arc_shell(155.0, 280.0, 196.0, 199.5, ang + 8.0, ang + 12.0, segs_theta=1))
        # Signal-orange (#D95B26) radial zero-G shuttle docking berth collar
        kit.add(
            "accent_orange",
            make_beveled_box((22.0, 18.0, 18.0), center=(235.0, CYL_Y + 188.0 * cy, 188.0 * sz), bevel=2.0),
        )
        # Interior 3D Cylindrical Cryo-He3 Propellant Tank visible inside the gantry cage
        kit.add(
            "aero_white",
            make_cylinder(16.0, 16.0, 95.0, center=(215.0, CYL_Y + 115.0 * cy, 115.0 * sz), segments=12, axis="x"),
        )
        kit.add(
            "led_uv",
            make_cylinder(17.2, 17.2, 12.0, center=(215.0, CYL_Y + 115.0 * cy, 115.0 * sz), segments=12, axis="x"),
        )

    add_axial_zero_g_solar_spine(kit, x_start=-380.0, x_end=365.0, n_nodes=4, n_spoke_rings=2)
    add_hemispherical_or_stepped_endcaps(kit, x_fwd=x_hab0, x_aft=290.0, include_aft_fusion_drive=True)

    out_p = os.path.join(OUT_CYL_DIR, "cylinder_r1_02.glb")
    return center_and_export_glb(out_p, kit.to_submeshes("Cyl02"), root_name="CylinderHab7_R1_02_Aegis7DualZoneSplit")


# ==============================================================================
# CANDIDATE 03: HEXAGONAL GEODESIC MACRO-TRUSS & TERRACED RING-SEA BIOSPHERE CYLINDER
# ==============================================================================
def build_cylinder_03_geodesic_ring_sea_biosphere(mats: Dict[str, PBRMaterialDef]) -> Dict[str, any]:
    kit = BuildingKit(mats)
    x_body0, x_body1 = -285.0, 285.0

    # 1. Geodesic Exoskeletal Macro-Truss Rings & Intersecting Ribs
    for rx in np.linspace(x_body0, x_body1, 9):
        kit.add("steel_machined", make_axial_ring(float(rx), r_in=192.0, r_out=200.0, width_x=9.0, segs=16))
    # Central Equatorial Ring-Sea Reservoir (`glass_cyan` & `led_cyan` water band at X = -75m .. +75m)
    kit.add("gunmetal", make_axial_ring(-82.0, r_in=184.0, r_out=200.0, width_x=14.0, segs=16))
    kit.add("gunmetal", make_axial_ring(82.0, r_in=184.0, r_out=200.0, width_x=14.0, segs=16))
    kit.add("glass_cyan", make_axial_ring(0.0, r_in=182.0, r_out=192.0, width_x=148.0, segs=16))
    kit.add("led_cyan", make_axial_ring(0.0, r_in=180.0, r_out=183.0, width_x=120.0, segs=16))

    # 2. 4 Alternating Land & Emerald Geodesic Conservatory Quadrants (90° periodicity)
    for k in range(4):
        land_t0 = k * 90.0
        land_t1 = land_t0 + 46.0
        bio_t0 = land_t0 + 44.0
        bio_t1 = land_t0 + 90.0

        kit.add("aero_white", make_cyl_arc_shell(x_body0, x_body1, 186.0, 194.5, land_t0, land_t1, segs_theta=5))
        add_interior_land_strip_and_city_skyline(kit, x_body0 + 25.0, x_body1 - 25.0, land_t0 + 5.0, land_t1 - 5.0, r_hull_in=186.0, n_longitudinal_rows=3)
        kit.add("glass_emerald", make_cyl_arc_shell(x_body0, x_body1, 188.5, 194.0, bio_t0, bio_t1, segs_theta=5))
        kit.add("led_uv", make_cyl_arc_shell(x_body0 + 20.0, x_body1 - 20.0, 193.5, 195.5, bio_t0 + 20.0, bio_t0 + 24.0, segs_theta=1))

    add_axial_zero_g_solar_spine(kit, x_start=-375.0, x_end=355.0, n_nodes=4, n_spoke_rings=2)
    add_hemispherical_or_stepped_endcaps(kit, x_fwd=x_body0, x_aft=x_body1, include_aft_fusion_drive=True)

    out_p = os.path.join(OUT_CYL_DIR, "cylinder_r1_03.glb")
    return center_and_export_glb(out_p, kit.to_submeshes("Cyl03"), root_name="CylinderHab7_R1_03_GeodesicBiosphere")


# ==============================================================================
# CANDIDATE 04: HEAVY WHIPPLE-SHIELDED DEEP-SPACE BASTION CYLINDER (800m x 400m)
# ==============================================================================
def build_cylinder_04_whipple_shield_bastion(mats: Dict[str, PBRMaterialDef]) -> Dict[str, any]:
    kit = BuildingKit(mats)
    x_body0, x_body1 = -285.0, 285.0

    # 1. Heavy Layered Gunmetal & Carbon-Slate Whipple-Shield Armor Rings
    for idx_r, rx in enumerate(np.linspace(x_body0, x_body1, 8)):
        mat_r = "gunmetal" if (idx_r % 2 == 0) else "carbon_slate"
        kit.add(mat_r, make_axial_ring(float(rx), r_in=189.0, r_out=200.0, width_x=24.0, segs=16))
        kit.add("led_amber", make_axial_ring(float(rx), r_in=198.2, r_out=200.0, width_x=3.5, segs=16))

    # 2. 4 Armored Hull Sectors + 4 Recessed Translucent Slit Solariums + 4 Point-Defense Laser Bastion Sponsons
    for k in range(4):
        hull_t0 = k * 90.0
        hull_t1 = hull_t0 + 58.0
        win_t0 = hull_t0 + 56.0
        win_t1 = hull_t0 + 90.0

        kit.add("gunmetal", make_cyl_arc_shell(x_body0, x_body1, 186.0, 195.5, hull_t0, hull_t1, segs_theta=5))
        kit.add("aero_white", make_cyl_arc_shell(x_body0 + 25.0, x_body1 - 25.0, 194.5, 197.5, hull_t0 + 12.0, hull_t1 - 12.0, segs_theta=3))
        add_interior_land_strip_and_city_skyline(kit, x_body0 + 30.0, x_body1 - 30.0, hull_t0 + 6.0, hull_t1 - 6.0, r_hull_in=186.0, n_longitudinal_rows=3)

        kit.add("glass_cyan", make_cyl_arc_shell(x_body0, x_body1, 188.0, 192.0, win_t0, win_t1, segs_theta=4))

        # External Point-Defense Meteor Laser Turret Sponson at X = 0.0m
        rad = math.radians(hull_t0 + 29.0)
        cy, sz = math.cos(rad), math.sin(rad)
        kit.add("accent_orange", make_beveled_box((34.0, 18.0, 18.0), center=(0.0, CYL_Y + 190.0 * cy, 190.0 * sz), bevel=2.5))
        kit.add("led_cyan", make_cylinder(4.5, 4.5, 58.0, center=(0.0, CYL_Y + 196.0 * cy, 196.0 * sz), segments=10, axis="x"))

    add_axial_zero_g_solar_spine(kit, x_start=-375.0, x_end=355.0, n_nodes=4, n_spoke_rings=2)
    add_hemispherical_or_stepped_endcaps(kit, x_fwd=x_body0, x_aft=x_body1, include_aft_fusion_drive=True)

    out_p = os.path.join(OUT_CYL_DIR, "cylinder_r1_04.glb")
    return center_and_export_glb(out_p, kit.to_submeshes("Cyl04"), root_name="CylinderHab7_R1_04_WhippleShieldBastion")


# ==============================================================================
# CANDIDATE 05: MODULAR 5-RING SECTORIZED METROPOLIS & COUNTER-ROTATING SHIPYARD HUB
# ==============================================================================
def build_cylinder_05_modular_5ring_metropolis(mats: Dict[str, PBRMaterialDef]) -> Dict[str, any]:
    kit = BuildingKit(mats)
    x_body0, x_body1 = -285.0, 285.0

    # 5 Distinct Modular Rotating Habitat Drum Segments separated by 4 Full-Circumference
    # Translucent Observation Sky-Rings & Magnetic Bearing Joints
    ring_centers = [-220.0, -110.0, 0.0, 110.0, 220.0]
    for r_idx, rcx in enumerate(ring_centers):
        rx0, rx1 = rcx - 46.0, rcx + 46.0
        kit.add("gunmetal", make_axial_ring(rx0, r_in=190.0, r_out=200.0, width_x=8.0, segs=16))
        
        for k in range(3):
            t0 = k * 120.0 + (r_idx % 2) * 30.0
            kit.add("aero_white", make_cyl_arc_shell(rx0, rx1, 186.0, 195.0, t0, t0 + 68.0, segs_theta=5))
            add_interior_land_strip_and_city_skyline(kit, rx0 + 8.0, rx1 - 8.0, t0 + 6.0, t0 + 62.0, r_hull_in=186.0, n_longitudinal_rows=1)
            g_key = "glass_cyan" if ((r_idx + k) % 2 == 0) else "glass_emerald"
            kit.add(g_key, make_cyl_arc_shell(rx0, rx1, 188.5, 193.0, t0 + 66.0, t0 + 120.0, segs_theta=4))

    # 4 Translucent Observation Sky-Ring Joints between the 5 modular drums
    for jx in [-168.75, -56.25, 56.25, 168.75]:
        kit.add("glass_cyan", make_axial_ring(jx, r_in=187.0, r_out=195.0, width_x=18.0, segs=16))
        kit.add("led_cyan", make_axial_ring(jx - 6.0, r_in=194.5, r_out=198.5, width_x=3.0, segs=16))
        kit.add("led_amber", make_axial_ring(jx + 6.0, r_in=194.5, r_out=198.5, width_x=3.0, segs=16))

    add_axial_zero_g_solar_spine(kit, x_start=-375.0, x_end=355.0, n_nodes=4, n_spoke_rings=2)
    add_hemispherical_or_stepped_endcaps(kit, x_fwd=x_body0, x_aft=x_body1, include_aft_fusion_drive=True)

    out_p = os.path.join(OUT_CYL_DIR, "cylinder_r1_05.glb")
    return center_and_export_glb(out_p, kit.to_submeshes("Cyl05"), root_name="CylinderHab7_R1_05_Modular5RingMetropolis")


def build_all_fullscale_cylinders():
    mats = get_building_materials()
    builders = [
        build_cylinder_01_classic_solarium,
        build_cylinder_02_aegis7_dual_zone_split,
        build_cylinder_03_geodesic_ring_sea_biosphere,
        build_cylinder_04_whipple_shield_bastion,
        build_cylinder_05_modular_5ring_metropolis,
    ]
    results = []
    for fn in builders:
        info = fn(mats)
        fname = os.path.basename(info["filepath"])
        dims = info["dimensions"]
        sz_kb = os.path.getsize(info["filepath"]) / 1024.0
        print(
            f"[cylinder] {fname:22s} | {dims[0]:6.2f}m L x {dims[2]:6.2f}m W x {dims[1]:6.2f}m H | "
            f"tris={info['triangles']:5d} | min_y={info['min'][1]:.5f} | {sz_kb:6.1f} KB"
        )
        results.append(info)
    with open(os.path.join(OUT_CYL_DIR, "cylinder_r1_manifest.json"), "w") as f:
        json.dump(results, f, indent=2)
    return results


if __name__ == "__main__":
    build_all_fullscale_cylinders()
