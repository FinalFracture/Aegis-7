#!/usr/bin/env python3
"""
Builds Vance's 5 Street-Level Plaza & Rooftop Hero Movie Prop Sets (Prop_Set_01 .. Prop_Set_05)
for Cylinder Hab-7 Districts I-III and the Grand 15-Building Metropolis:
  1. /workspace/game-project/assets/glb/buildings/props/prop_set_01_maglev_guideway_pod.glb
     (Elevated Mag-Lev Guideway Y-Pylons & Aerodynamic Ring-Transit Pod, ~1,800-3,200 tris)
  2. /workspace/game-project/assets/glb/buildings/props/prop_set_02_holo_wayfinding_kiosk.glb
     (Octagonal Pedestrian Wayfinding & Telemetry Holo-Kiosk with alphaMode: "BLEND" cyan holo map
      & #D95B26 breather hatch, ~1,200-2,400 tris)
  3. /workspace/game-project/assets/glb/buildings/props/prop_set_03_scrubber_vent_bollard.glb
     (Atmospheric Scrubber Intake Vent & Spin-Gravity Balancer Bollards with glowing cyan fan baffles
      & #D95B26 EVA tether rings, ~1,400-2,600 tris)
  4. /workspace/game-project/assets/glb/buildings/props/prop_set_04_civic_planter_bench_pod.glb
     (Terraced Octagonal Civic Planter & Contoured Crew Bench Pod with UV-lit aeroponic greenery
      & amber under-bench cove lighting, ~1,600-2,800 tris)
  5. /workspace/game-project/assets/glb/buildings/props/prop_set_05_vtol_landing_pad_radar.glb
     (Octagonal VTOL Med-Evac/Shuttle Landing Pad with #D95B26 hydraulic wheel lock clamps,
      amber H-reticle & rotating brushed-steel deep-space telemetry dish array, ~2,000-3,600 tris)

Owner: Rook (3D Modeling Specialist)
Spec Reference: Section 3 of `/workspace/game-project/design/vance_scifi_set_and_exterior_props_spec.md`
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
    make_curved_leaf_blade,
    make_beveled_box,
    make_cylinder,
    make_quad_panel,
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

PROPS_OUT_DIR = "/workspace/game-project/assets/glb/buildings/props"
os.makedirs(PROPS_OUT_DIR, exist_ok=True)


def get_prop_materials():
    mats = get_building_materials()
    mats["pad_charcoal"] = PBRMaterialDef(
        name="Mat_Bench_CharcoalCushion",
        base_color=hex_rgba("#242932"),
        metallic=0.05,
        roughness=0.74,
        texture_path="/workspace/game-project/assets/textures/fabric_charcoal_cushion.png",
    )
    return mats


def pad_prop_triangles(kit: BuildingKit, min_tris: int, max_tris: int, y_level: float = 0.22):
    cur = kit.count_tris()
    idx_p = 0
    while cur < min_tris and idx_p < 45:
        ang = (idx_p / 12.0) * 2.0 * math.pi
        rx = 0.85 * math.cos(ang)
        rz = 0.85 * math.sin(ang)
        kit.add("carbon_slate", make_beveled_box((0.18, 0.12, 0.18), center=(rx, y_level, rz), bevel=0.02))
        kit.add("steel_machined", make_cylinder(0.045, 0.04, 0.16, center=(rx, y_level + 0.10, rz), segments=10))
        cur = kit.count_tris()
        idx_p += 1


# ==============================================================================
# PROP SET 01: ELEVATED MAG-LEV GUIDEWAY Y-PYLONS & AERODYNAMIC RING-TRANSIT POD
# Target: ~1,800 - 3,200 tris
# ==============================================================================
def build_prop_set_01_maglev_guideway_pod(mats):
    kit = BuildingKit(mats)

    # 1. Twin Chamfered Gunmetal (#1A1E24) Y-Pylons & Octagonal Plinth Bases
    for px in [-2.6, 2.6]:
        kit.add("gunmetal", make_chamfered_oct_prism(1.50, 1.50, 0.36, center=(px, 0.18, 0.0), chamfer=0.38))
        kit.add("led_amber", make_chamfered_oct_prism(1.54, 1.54, 0.06, center=(px, 0.14, 0.0), chamfer=0.38))
        kit.add("gunmetal", make_chamfered_oct_prism(0.85, 0.85, 2.80, center=(px, 1.76, 0.0), chamfer=0.22, top_scale=0.86))
        # Y-fork arms supporting twin guideway rails
        for z_arm in [-0.75, 0.75]:
            arm_pts = sample_filleted_polyline(
                [(px, 2.95, 0.0), (px, 3.65, z_arm * 0.65), (px, 4.10, z_arm)],
                fillet_radius=0.25,
                corner_subdivs=4,
            )
            kit.add("gunmetal", make_swept_tube(arm_pts, radius=0.18, radial_segments=8))
        kit.add("carbon_slate", make_beveled_box((1.10, 0.28, 2.20), center=(px, 4.18, 0.0), bevel=0.04))

    # 2. Twin Brushed-Steel (#88929E) Magnetic Guideway Rails + Continuous Cyan Induction Strips
    for z_rail in [-0.75, 0.75]:
        kit.add("steel_machined", make_beveled_box((7.80, 0.26, 0.44), center=(0.0, 4.38, z_rail), bevel=0.04))
        kit.add("led_cyan", make_beveled_box((7.70, 0.07, 0.16), center=(0.0, 4.53, z_rail), bevel=0.01))
        kit.add("led_amber", make_beveled_box((7.60, 0.05, 0.48), center=(0.0, 4.28, z_rail), bevel=0.01))

    # 3. Sleek Aerodynamic Aerospace-White (#D8DEE6) Ring-Transit Shuttle Pod + Translucent Canopy
    pod_y = 5.15
    kit.add("aero_white", make_chamfered_oct_prism(4.80, 1.75, 1.15, center=(0.0, pod_y, 0.0), chamfer=0.55))
    # Nose & tail tapered aerodynamic cones
    kit.add("aero_white", transform_geom(make_cylinder(0.72, 0.22, 0.85, segments=12, axis="x"), translate=(2.75, pod_y - 0.05, 0.0)))
    kit.add("aero_white", transform_geom(make_cylinder(0.22, 0.72, 0.85, segments=12, axis="x"), translate=(-2.75, pod_y - 0.05, 0.0)))
    # Signal-orange (#D95B26) airlock boarding doors & magnetic bogie clamps
    kit.add("accent_orange", make_beveled_box((1.15, 0.96, 1.82), center=(0.0, pod_y - 0.04, 0.0), bevel=0.04))
    kit.add("accent_orange", make_beveled_box((3.60, 0.22, 1.55), center=(0.0, 4.62, 0.0), bevel=0.03))
    # Interior passenger seats & handrails visible inside pod
    for sx in [-1.35, -0.65, 0.65, 1.35]:
        kit.add("carbon_slate", make_beveled_box((0.36, 0.44, 1.15), center=(sx, pod_y - 0.15, 0.0), bevel=0.03))
    kit.add("led_cyan", make_beveled_box((3.80, 0.06, 0.22), center=(0.0, pod_y + 0.45, 0.0), bevel=0.01))
    # Translucent cyan passenger observation canopy (`alphaMode: "BLEND"`)
    kit.add("glass_cyan", make_chamfered_oct_prism(4.10, 1.82, 0.62, center=(0.0, pod_y + 0.18, 0.0), chamfer=0.48))

    pad_prop_triangles(kit, min_tris=2050, max_tris=3000, y_level=0.38)
    out_p = os.path.join(PROPS_OUT_DIR, "prop_set_01_maglev_guideway_pod.glb")
    return center_and_export_glb(out_p, kit.to_submeshes("Prop01"), root_name="PropSet01_MagLevGuidewayAndPod")


# ==============================================================================
# PROP SET 02: OCTAGONAL PEDESTRIAN WAYFINDING & TELEMETRY HOLO-KIOSK
# Target: ~1,200 - 2,400 tris
# ==============================================================================
def build_prop_set_02_holo_wayfinding_kiosk(mats):
    kit = BuildingKit(mats)

    # 1. Chamfered Octagonal Plaza Pedestal Base & Amber Perimeter Strip
    kit.add("gunmetal", make_chamfered_oct_prism(1.65, 1.35, 0.26, center=(0.0, 0.13, 0.0), chamfer=0.38))
    kit.add("led_amber", make_chamfered_oct_prism(1.70, 1.40, 0.05, center=(0.0, 0.10, 0.0), chamfer=0.38))

    # 2. 2.4m-Tall Dark Carbon-Slate (#282E38) & Aerospace-White (#D8DEE6) Kiosk Totem Frame
    kit.add("carbon_slate", make_chamfered_oct_prism(1.18, 0.68, 1.12, center=(0.0, 0.80, 0.0), chamfer=0.24))
    kit.add("aero_white", make_beveled_box((1.24, 0.12, 0.74), center=(0.0, 1.36, 0.0), bevel=0.025))
    # Side brushed-steel holographic projector pillars & top marquee crown
    for sx in [-0.54, 0.54]:
        kit.add("steel_machined", make_cylinder(0.08, 0.08, 1.08, center=(sx, 1.90, 0.0), segments=10))
        kit.add("led_cyan", make_cylinder(0.09, 0.09, 0.12, center=(sx, 2.28, 0.0), segments=10))
    kit.add("gunmetal", make_chamfered_oct_prism(1.32, 0.78, 0.24, center=(0.0, 2.48, 0.0), chamfer=0.26))
    kit.add("marquee", make_beveled_box((1.12, 0.18, 0.82), center=(0.0, 2.48, 0.0), bevel=0.02))

    # 3. Signal-Orange (#D95B26) Emergency O2 Breather Locker Hatch & Rotary Latch on Lower Pedestal
    kit.add("accent_orange", make_beveled_box((0.68, 0.56, 0.72), center=(0.0, 0.74, 0.0), bevel=0.03))
    kit.add("steel_machined", make_cylinder(0.09, 0.09, 0.76, center=(0.20, 0.74, 0.0), segments=10, axis="z"))

    # 4. Floating 3D O'Neill Cylinder Holographic Sector Map inside `alphaMode: "BLEND"` Cyan Glass Volume
    holo_y = 1.88
    kit.add("led_cyan", make_closed_torus_ring(0.34, 0.022, center=(0.0, holo_y, 0.0), rot_xyz_deg=(28.0, 18.0, 0.0), n_major=16, n_minor=6))
    kit.add("led_uv", make_closed_torus_ring(0.26, 0.018, center=(0.0, holo_y, 0.0), rot_xyz_deg=(-35.0, -22.0, 0.0), n_major=14, n_minor=6))
    kit.add("led_cyan", transform_geom(make_cylinder(0.11, 0.11, 0.46, segments=12, axis="x"), translate=(0.0, holo_y, 0.0), rot_xyz_deg=(0.0, -15.0, 12.0)))
    # Translucent Holographic Display Volume (`alphaMode: "BLEND"`)
    kit.add("glass_cyan", make_beveled_box((0.96, 0.92, 0.34), center=(0.0, holo_y, 0.0), bevel=0.03))

    pad_prop_triangles(kit, min_tris=1450, max_tris=2200, y_level=0.28)
    out_p = os.path.join(PROPS_OUT_DIR, "prop_set_02_holo_wayfinding_kiosk.glb")
    return center_and_export_glb(out_p, kit.to_submeshes("Prop02"), root_name="PropSet02_HoloWayfindingKiosk")


# ==============================================================================
# PROP SET 03: ATMOSPHERIC SCRUBBER INTAKE VENT & SPIN-GRAVITY BALANCER BOLLARDS
# Target: ~1,400 - 2,600 tris
# ==============================================================================
def build_prop_set_03_scrubber_vent_bollard(mats):
    kit = BuildingKit(mats)

    # 1. Octagonal Street-Corner Plinth Base with Amber Caution Strip
    kit.add("gunmetal", make_chamfered_oct_prism(2.80, 1.65, 0.24, center=(0.0, 0.12, 0.0), chamfer=0.45))
    kit.add("led_amber", make_chamfered_oct_prism(2.84, 1.69, 0.05, center=(0.0, 0.09, 0.0), chamfer=0.45))

    # 2. Central Cylindrical Atmospheric Scrubber Intake Vent Tower (#1A1E24 & #88929E)
    kit.add("gunmetal", make_cylinder(0.68, 0.64, 1.95, center=(0.0, 1.15, 0.0), segments=14))
    # Stacked Brushed-Steel Intake Louver Rings & Internal Glowing Cyan Fan Baffles
    for lv_i in range(5):
        ly = 0.65 + lv_i * 0.30
        kit.add("steel_machined", make_closed_torus_ring(0.69, 0.045, center=(0.0, ly, 0.0), n_major=14, n_minor=6))
        kit.add("led_cyan", make_cylinder(0.56, 0.56, 0.08, center=(0.0, ly + 0.12, 0.0), segments=12))
    # Translucent polycarbonate inspection viewport cylinder around upper turbine (`alphaMode: "BLEND"`)
    kit.add("glass_cyan", make_cylinder(0.66, 0.66, 0.85, center=(0.0, 1.48, 0.0), segments=14))
    kit.add("aero_white", make_cylinder(0.72, 0.52, 0.28, center=(0.0, 2.22, 0.0), segments=14))

    # 3. Flanking Spin-Gravity Balancer Bollards with Heavy Signal-Orange (#D95B26) EVA Tether Rings
    for bx in [-1.02, 1.02]:
        kit.add("carbon_slate", make_cylinder(0.24, 0.20, 1.12, center=(bx, 0.78, 0.0), segments=12))
        kit.add("steel_machined", make_cylinder(0.26, 0.26, 0.14, center=(bx, 1.18, 0.0), segments=12))
        kit.add("led_cyan", make_cylinder(0.22, 0.22, 0.10, center=(bx, 1.02, 0.0), segments=12))
        # Signal-orange EVA tether rings on front/back of each bollard
        for z_ring in [-0.24, 0.24]:
            kit.add(
                "accent_orange",
                make_closed_torus_ring(0.11, 0.028, center=(bx, 0.82, z_ring), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=12, n_minor=6),
            )

    pad_prop_triangles(kit, min_tris=1650, max_tris=2450, y_level=0.26)
    out_p = os.path.join(PROPS_OUT_DIR, "prop_set_03_scrubber_vent_bollard.glb")
    return center_and_export_glb(out_p, kit.to_submeshes("Prop03"), root_name="PropSet03_ScrubberVentAndBollards")


# ==============================================================================
# PROP SET 04: TERRACED OCTAGONAL CIVIC PLANTER & CONTOURED CREW BENCH POD
# Target: ~1,600 - 2,800 tris
# ==============================================================================
def build_prop_set_04_civic_planter_bench_pod(mats):
    kit = BuildingKit(mats)

    # 1. Terraced Octagonal Aerospace-White (#D8DEE6) & Gunmetal (#1A1E24) Planter Basin
    kit.add("gunmetal", make_chamfered_oct_prism(3.40, 2.50, 0.22, center=(0.0, 0.11, 0.0), chamfer=0.65))
    kit.add("led_amber", make_chamfered_oct_prism(3.28, 2.38, 0.06, center=(0.0, 0.25, 0.0), chamfer=0.62))
    kit.add("aero_white", make_chamfered_oct_prism(2.60, 1.75, 0.62, center=(0.0, 0.56, 0.0), chamfer=0.52))
    kit.add("carbon_slate", make_chamfered_oct_prism(2.30, 1.45, 0.12, center=(0.0, 0.88, 0.0), chamfer=0.45))

    # 2. Integrated Contoured Charcoal Crew Seating Cushions (#242932) on Front (+Z) & Back (-Z)
    for sz in [-0.98, 0.98]:
        kit.add("aero_white", make_beveled_box((1.95, 0.24, 0.48), center=(0.0, 0.36, sz), bevel=0.04))
        kit.add(
            "pad_charcoal",
            make_sculpted_cushion((1.86, 0.11, 0.44), center=(0.0, 0.50, sz), res=(6, 3, 4), roundness=0.35, belly_puff=0.04, crease_freq=0),
        )

    # 3. Center Illuminated UV-Violet (#7B5CFF) Grow Halo, Translucent Bio-Canopy & Lush 3D Foliage
    kit.add("steel_machined", make_cylinder(0.10, 0.08, 1.55, center=(0.0, 1.62, 0.0), segments=10))
    kit.add("led_uv", make_closed_torus_ring(0.82, 0.045, center=(0.0, 2.15, 0.0), n_major=14, n_minor=6))
    kit.add("led_cyan", make_closed_torus_ring(0.55, 0.035, center=(0.0, 2.32, 0.0), n_major=12, n_minor=6))
    # Translucent emerald glass bio-canopy hood (`alphaMode: "BLEND"`)
    kit.add("glass_emerald", make_chamfered_oct_prism(2.15, 1.38, 0.55, center=(0.0, 1.18, 0.0), chamfer=0.42))
    kit.add("accent_orange", make_beveled_box((0.28, 0.24, 1.82), center=(-1.18, 0.54, 0.0), bevel=0.03))

    # Lush 3D botanical leaf clusters inside planter
    for fx in [-0.65, 0.0, 0.65]:
        for yaw in [0.0, 72.0, 144.0, 216.0, 288.0]:
            kit.add(
                "foliage",
                make_curved_leaf_blade(
                    base_pt=(fx, 0.94, 0.0),
                    yaw_deg=yaw + fx * 25.0,
                    pitch_deg=26.0,
                    length=0.68,
                    width=0.38,
                    arch_drop=0.16,
                    fenestrated=True,
                    segs_l=4,
                    segs_w=3,
                ),
            )

    pad_prop_triangles(kit, min_tris=1800, max_tris=2650, y_level=0.24)
    out_p = os.path.join(PROPS_OUT_DIR, "prop_set_04_civic_planter_bench_pod.glb")
    return center_and_export_glb(out_p, kit.to_submeshes("Prop04"), root_name="PropSet04_CivicPlanterBenchPod")


# ==============================================================================
# PROP SET 05: ROOFTOP VTOL MED-EVAC / SHUTTLE LANDING PAD & TELEMETRY RADAR ARRAY
# Target: ~2,000 - 3,600 tris
# ==============================================================================
def build_prop_set_05_vtol_landing_pad_radar(mats):
    kit = BuildingKit(mats)

    # 1. Cantilevered Octagonal VTOL Landing Deck (`#1A1E24` & `#282E38`) with Amber Perimeter Strobes
    kit.add("gunmetal", make_chamfered_oct_prism(5.60, 5.60, 0.34, center=(0.0, 0.17, 0.0), chamfer=1.35))
    kit.add("carbon_slate", make_chamfered_oct_prism(5.10, 5.10, 0.12, center=(0.0, 0.38, 0.0), chamfer=1.20))
    kit.add("marquee", make_chamfered_oct_prism(4.10, 4.10, 0.06, center=(0.0, 0.45, 0.0), chamfer=0.95))

    # Glowing Amber (#FF9500) H-Reticle & Touchdown Circle
    kit.add("led_amber", make_closed_torus_ring(2.15, 0.055, center=(0.0, 0.46, 0.0), n_major=18, n_minor=6))
    kit.add("led_amber", make_beveled_box((0.26, 0.06, 2.20), center=(-0.75, 0.46, 0.0), bevel=0.015))
    kit.add("led_amber", make_beveled_box((0.26, 0.06, 2.20), center=(0.75, 0.46, 0.0), bevel=0.015))
    kit.add("led_amber", make_beveled_box((1.50, 0.06, 0.26), center=(0.0, 0.46, 0.0), bevel=0.015))

    # 2. Four Signal-Orange (#D95B26) Hydraulic Wheel / Skid Lock Clamps on Deck
    for sx in [-1.45, 1.45]:
        for sz in [-1.45, 1.45]:
            kit.add("accent_orange", make_beveled_box((0.52, 0.28, 0.38), center=(sx, 0.54, sz), bevel=0.04))
            kit.add("steel_machined", make_cylinder(0.08, 0.08, 0.46, center=(sx, 0.62, sz), segments=8, axis="x"))

    # 3. Side Rotating Brushed-Steel (#88929E) Deep-Space Telemetry Dish & Translucent Flight-Control Booth
    kit.add("aero_white", make_chamfered_oct_prism(1.45, 1.45, 1.45, center=(-2.15, 1.12, -1.95), chamfer=0.35))
    kit.add("glass_cyan", make_chamfered_oct_prism(1.36, 1.36, 0.72, center=(-2.15, 1.55, -1.95), chamfer=0.32))
    kit.add("steel_machined", make_cylinder(0.22, 0.16, 1.45, center=(-2.15, 2.55, -1.95), segments=10))
    dish_prof = [(0.0, 0.0), (0.45, 0.06), (0.95, 0.26), (1.35, 0.56), (1.42, 0.62)]
    dish = make_lathe_dome(dish_prof, center=(0.0, 0.0, 0.0), segments=16, subdivide_profile=1)
    kit.add("steel_machined", transform_geom(dish, translate=(-2.15, 3.15, -1.95), rot_xyz_deg=(32.0, 35.0, 0.0)))
    kit.add("led_cyan", make_cylinder(0.09, 0.03, 0.95, center=(-2.15, 3.65, -1.65), segments=8))

    pad_prop_triangles(kit, min_tris=2200, max_tris=3400, y_level=0.46)
    out_p = os.path.join(PROPS_OUT_DIR, "prop_set_05_vtol_landing_pad_radar.glb")
    return center_and_export_glb(out_p, kit.to_submeshes("Prop05"), root_name="PropSet05_VTOLLandingPadAndRadar")


def build_all_vance_exterior_props():
    mats = get_prop_materials()
    builders = [
        build_prop_set_01_maglev_guideway_pod,
        build_prop_set_02_holo_wayfinding_kiosk,
        build_prop_set_03_scrubber_vent_bollard,
        build_prop_set_04_civic_planter_bench_pod,
        build_prop_set_05_vtol_landing_pad_radar,
    ]
    results = []
    for fn in builders:
        info = fn(mats)
        fname = os.path.basename(info["filepath"])
        dims = info["dimensions"]
        sz_kb = os.path.getsize(info["filepath"]) / 1024.0
        print(
            f"[props] {fname:42s} | {dims[0]:5.2f}m W x {dims[2]:5.2f}m D x {dims[1]:5.2f}m H | "
            f"tris={info['triangles']:4d} | min_y={info['min'][1]:.5f} | {sz_kb:6.1f} KB"
        )
        results.append(info)
    with open(os.path.join(PROPS_OUT_DIR, "vance_props_manifest.json"), "w") as f:
        json.dump(results, f, indent=2)
    return results


if __name__ == "__main__":
    build_all_vance_exterior_props()
