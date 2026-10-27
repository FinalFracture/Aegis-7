#!/usr/bin/env python3
"""Sci-Fi Crew Desk / Telemetry Workstation — Round 1 (5 candidates).
Exports /workspace/game-project/assets/glb/desk_round1/desk_r1_01.glb .. desk_r1_05.glb
Front faces +Z (chair side), back wall at -Z, pivot bottom-center Y=0."""
import os, sys, json, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glb_builder import (sample_filleted_polyline, make_swept_tube, make_sculpted_cushion,
                         make_beveled_box, make_cylinder, make_quad_panel, merge_geometries,
                         transform_geom, make_lathe_dome)
from bunk_round1_generator import add_part, center_and_export_glb, make_chamfered_aperture_ring
from bunk_round2_generator import get_r2_materials, make_open_backwall_frame

OUT = "/workspace/game-project/assets/glb/desk_round1"
os.makedirs(OUT, exist_ok=True)


def tube(pts, r, fil=0.08, seg=10, **kw):
    return make_swept_tube(sample_filleted_polyline(pts, fillet_radius=fil, corner_subdivs=5), radius=r, radial_segments=seg, **kw)


def arc_pts(radius, a0, a1, y, n=16, cz=0.0):
    return [(radius * math.sin(math.radians(a)), y, cz - radius * math.cos(math.radians(a))) for a in np.linspace(a0, a1, n)]


def curved_screen(radius, a0, a1, y0, y1, cz=0.0, n=14):
    parts = []
    angs = np.linspace(a0, a1, n + 1)
    for i in range(n):
        pa, pb = angs[i], angs[i + 1]
        xa, za = radius * math.sin(math.radians(pa)), cz - radius * math.cos(math.radians(pa))
        xb, zb = radius * math.sin(math.radians(pb)), cz - radius * math.cos(math.radians(pb))
        parts.append(make_quad_panel((xa, y0, za), (xb, y0, zb), (xb, y1, zb), (xa, y1, za),
                                     uv_rect=(i / n, 0.0, (i + 1) / n, 1.0)))
    return merge_geometries(parts)


def swivel_chair(mats, sm, prefix, center=(0.0, 0.0, 0.75), yaw=180.0, high_back=False, arms=False,
                 seat_mat="pad_charcoal", frame_mat="steel_machined", base_mat="gunmetal", stool=False):
    cx, _, cz = center
    def T(g):
        return transform_geom(g, translate=(cx, 0.0, cz), rot_xyz_deg=(0.0, yaw, 0.0))
    legs = []
    for k in range(5):
        a = math.radians(k * 72.0)
        dx, dz = math.cos(a), math.sin(a)
        legs.append(tube([(0, 0.13, 0), (dx * 0.18, 0.10, dz * 0.18), (dx * 0.30, 0.06, dz * 0.30)], 0.022, fil=0.06, seg=8, oval_scale=(1.3, 0.8)))
        legs.append(make_cylinder(0.03, 0.03, 0.035, center=(dx * 0.30, 0.03, dz * 0.30), segments=10))
    legs.append(make_cylinder(0.045, 0.035, 0.32 if stool else 0.30, center=(0, 0.28, 0), segments=14))
    add_part(sm, f"{prefix}_SwivelBase", T(merge_geometries(legs)), mats[base_mat])
    seat_y = 0.47
    add_part(sm, f"{prefix}_SeatCushion", T(make_sculpted_cushion((0.50, 0.10, 0.48), center=(0, seat_y, 0),
             res=(8, 4, 8), roundness=0.4, belly_puff=0.10, pinch_corners=0.12)), mats[seat_mat])
    if stool:
        ring = tube([(0.22 * math.cos(t), 0.24, 0.22 * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 20)], 0.012, fil=0.0, seg=8)
        add_part(sm, f"{prefix}_FootRing", T(ring), mats[frame_mat])
        add_part(sm, f"{prefix}_LumbarPad", T(make_sculpted_cushion((0.40, 0.16, 0.08), center=(0, 0.66, -0.20),
                 res=(6, 4, 3), roundness=0.5, belly_puff=0.12)), mats[seat_mat])
        add_part(sm, f"{prefix}_LumbarSpine", T(tube([(0, 0.44, -0.12), (0, 0.50, -0.25), (0, 0.66, -0.25)], 0.016, fil=0.05)), mats[frame_mat])
        return
    bh = 0.62 if high_back else 0.42
    add_part(sm, f"{prefix}_BackCushion", T(transform_geom(make_sculpted_cushion((0.48, bh, 0.10), center=(0, 0, 0),
             res=(8, 8, 4), roundness=0.45, belly_puff=0.12, pinch_corners=0.10, crease_freq=4),
             translate=(0, seat_y + 0.06 + bh * 0.5, -0.26), rot_xyz_deg=(-10.0, 0, 0))), mats[seat_mat])
    spine = tube([(0, seat_y - 0.05, -0.05), (0, seat_y - 0.03, -0.30), (0, seat_y + bh * 0.8, -0.36)], 0.02, fil=0.08)
    add_part(sm, f"{prefix}_BackSpine", T(spine), mats[frame_mat])
    if high_back:
        add_part(sm, f"{prefix}_Headrest", T(make_sculpted_cushion((0.30, 0.14, 0.09), center=(0, seat_y + bh + 0.16, -0.38),
                 res=(6, 4, 3), roundness=0.55, belly_puff=0.14)), mats[seat_mat])
    if arms:
        for s in (-1, 1):
            add_part(sm, f"{prefix}_Arm{'L' if s<0 else 'R'}", T(tube([(s * 0.22, seat_y, -0.16), (s * 0.29, seat_y + 0.20, -0.12), (s * 0.29, seat_y + 0.21, 0.14)], 0.016, fil=0.06)), mats[frame_mat])
            add_part(sm, f"{prefix}_ArmPad{'L' if s<0 else 'R'}", T(make_sculpted_cushion((0.07, 0.04, 0.24), center=(s * 0.29, seat_y + 0.235, 0.03),
                     res=(3, 2, 5), roundness=0.5, belly_puff=0.1)), mats["pad_charcoal"])


def keyboard(cx, y, cz, w=0.46, d=0.16):
    keys = [make_beveled_box((w, 0.022, d), center=(cx, y + 0.011, cz), bevel=0.006)]
    for r in range(3):
        keys.append(make_beveled_box((w * 0.9, 0.012, d * 0.2), center=(cx, y + 0.028, cz - d * 0.3 + r * d * 0.3), bevel=0.003))
    return merge_geometries(keys)


def build_01(m):
    sm = []
    add_part(sm, "Desk01_TitaniumWallSpine", merge_geometries([
        make_beveled_box((1.80, 1.90, 0.12), center=(0, 0.95, -0.40), bevel=0.03),
        make_beveled_box((0.20, 1.90, 0.06), center=(-0.70, 0.95, -0.32), bevel=0.02),
        make_beveled_box((0.20, 1.90, 0.06), center=(0.70, 0.95, -0.32), bevel=0.02)]), m["gunmetal"])
    top = transform_geom(make_sculpted_cushion((1.60, 0.06, 0.66), center=(0, 0, 0), res=(10, 2, 6), roundness=0.25, belly_puff=0.0, pinch_corners=0.0, crease_freq=0), translate=(0, 0.76, -0.02))
    add_part(sm, "Desk01_AeroWhiteCantileverTop", merge_geometries([top,
        make_beveled_box((1.50, 0.06, 0.10), center=(0, 0.70, -0.30), bevel=0.02)]), m["aero_white"])
    struts = []
    for s in (-0.55, 0.55):
        struts.append(transform_geom(make_cylinder(0.035, 0.035, 0.52, center=(0, 0, 0), segments=12), translate=(s, 0.50, -0.20), rot_xyz_deg=(-48, 0, 0)))
        struts.append(transform_geom(make_cylinder(0.022, 0.022, 0.40, segments=10), translate=(s, 0.62, -0.08), rot_xyz_deg=(-48, 0, 0)))
    add_part(sm, "Desk01_HydraulicStruts", merge_geometries(struts), m["steel_machined"])
    add_part(sm, "Desk01_CableConduits", merge_geometries([
        tube([(-0.62, 0.0, -0.33), (-0.62, 0.40, -0.33), (-0.40, 0.70, -0.31), (0.30, 0.70, -0.31)], 0.022, fil=0.15),
        tube([(-0.68, 0.0, -0.33), (-0.68, 0.46, -0.33), (-0.48, 0.72, -0.29), (0.20, 0.72, -0.29)], 0.016, fil=0.15)]), m["carbon_slate"])
    add_part(sm, "Desk01_KeyboardDeck", keyboard(0, 0.79, 0.12, w=0.62), m["carbon_slate"])
    add_part(sm, "Desk01_PanoramicHoloScreen", curved_screen(1.10, -32, 32, 1.00, 1.48, cz=0.95), m["glass_holo_visor"])
    add_part(sm, "Desk01_HoloEmitterBar", tube(arc_pts(1.10, -32, 32, 0.96, n=14, cz=0.95), 0.014, fil=0.0, seg=8), m["led_cyan"])
    add_part(sm, "Desk01_UnderglowStrip", make_beveled_box((1.40, 0.012, 0.02), center=(0, 0.725, 0.29), bevel=0.004), m["led_cyan"])
    swivel_chair(m, sm, "Desk01_FlightStool", center=(0.0, 0, 0.55), stool=True, seat_mat="pad_slate")
    return center_and_export_glb(os.path.join(OUT, "desk_r1_01.glb"), sm, "DeskR1_01_WallCantileverConsole")


def build_02(m):
    sm = []
    R = 0.95
    segs = []
    for a in np.linspace(-80, 80, 17)[:-1]:
        ac = a + 5
        x, z = R * math.sin(math.radians(ac)), 0.45 - R * math.cos(math.radians(ac))
        segs.append(transform_geom(make_beveled_box((0.18, 0.05, 0.48), bevel=0.012), translate=(x, 0.76, z), rot_xyz_deg=(0, -ac, 0)))
    add_part(sm, "Desk02_CarbonSlateUTop", merge_geometries(segs), m["carbon_slate"])
    ped = []
    for a in (-70, 0, 70):
        x, z = (R + 0.05) * math.sin(math.radians(a)), 0.45 - (R + 0.05) * math.cos(math.radians(a))
        ped.append(transform_geom(make_beveled_box((0.30, 0.72, 0.36), bevel=0.03), translate=(x, 0.37, z), rot_xyz_deg=(0, -a, 0)))
    add_part(sm, "Desk02_TitaniumPedestals", merge_geometries(ped), m["steel_machined"])
    add_part(sm, "Desk02_CyanEdgeLED", tube(arc_pts(R - 0.24, -80, 80, 0.755, n=20, cz=0.45), 0.008, fil=0.0, seg=6), m["led_cyan"])
    add_part(sm, "Desk02_AmberUnderLED", tube(arc_pts(R + 0.20, -78, 78, 0.70, n=20, cz=0.45), 0.008, fil=0.0, seg=6), m["led_amber"])
    mons, bez = [], []
    for a in (-42, 0, 42):
        x, z = (R + 0.04) * math.sin(math.radians(a)), 0.45 - (R + 0.04) * math.cos(math.radians(a))
        panel = make_quad_panel((-0.26, 0.0, 0), (0.26, 0.0, 0), (0.26, 0.32, 0), (-0.26, 0.32, 0))
        mons.append(transform_geom(panel, translate=(x, 0.90, z + 0.005), rot_xyz_deg=(-8, -a, 0)))
        bez.append(transform_geom(make_beveled_box((0.56, 0.36, 0.03), bevel=0.01), translate=(x, 1.06, z - 0.02), rot_xyz_deg=(-8, -a, 0)))
        bez.append(transform_geom(make_cylinder(0.018, 0.018, 0.12, segments=8), translate=(x, 0.84, z - 0.04)))
    add_part(sm, "Desk02_OLEDTelemetryMonitors", merge_geometries(mons), m["oled_hud"])
    add_part(sm, "Desk02_MonitorBezelsAndMounts", merge_geometries(bez), m["gunmetal"])
    add_part(sm, "Desk02_TacticalHoloArc", curved_screen(R + 0.06, -60, 60, 1.30, 1.62, cz=0.45), m["glass_holo_visor"])
    add_part(sm, "Desk02_HoloArcRail", tube(arc_pts(R + 0.06, -60, 60, 1.27, n=16, cz=0.45), 0.012, fil=0.0, seg=8), m["led_cyan"])
    add_part(sm, "Desk02_KeyDeck", keyboard(0, 0.785, -0.30, w=0.50), m["gunmetal"])
    swivel_chair(m, sm, "Desk02_OrbitalChair", center=(0, 0, 0.30), high_back=True, arms=True, seat_mat="pad_navy")
    return center_and_export_glb(os.path.join(OUT, "desk_r1_02.glb"), sm, "DeskR1_02_WraparoundCommandStation")


def build_03(m):
    sm = []
    py = []
    for s in (-0.62, 0.62):
        py.append(make_lathe_dome([(0.0, 0.0), (0.16, 0.0), (0.17, 0.03), (0.09, 0.08), (0.06, 0.30), (0.05, 0.62), (0.07, 0.66), (0.0, 0.66)], center=(s, 0, -0.05), segments=18, subdivide_profile=1))
    add_part(sm, "Desk03_MagLevPylons", merge_geometries(py), m["gunmetal"])
    rings = []
    for s in (-0.62, 0.62):
        for y in (0.22, 0.42, 0.62):
            rings.append(tube([(s + 0.085 * math.cos(t), y, -0.05 + 0.085 * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 18)], 0.012, fil=0.0, seg=6))
    add_part(sm, "Desk03_CyanInductionRings", merge_geometries(rings), m["led_cyan"])
    add_part(sm, "Desk03_SmokedGlassTop", make_beveled_box((1.60, 0.05, 0.72), center=(0, 0.74, -0.05), bevel=0.02), m["glass_viewport"])
    add_part(sm, "Desk03_SteelEdgeFrame", tube([(-0.80, 0.74, -0.41), (0.80, 0.74, -0.41), (0.80, 0.74, 0.31), (-0.80, 0.74, 0.31), (-0.80, 0.74, -0.41)], 0.016, fil=0.05, seg=8), m["steel_machined"])
    for i, (x, a) in enumerate(((-0.34, 14), (0.34, -14))):
        add_part(sm, f"Desk03_FloatingHoloScreen{i}", transform_geom(make_quad_panel((-0.30, 0, 0), (0.30, 0, 0), (0.30, 0.38, 0), (-0.30, 0.38, 0)), translate=(x, 0.98, -0.30), rot_xyz_deg=(0, a, 0)), m["glass_holo_visor"])
        add_part(sm, f"Desk03_HoloProjector{i}", make_lathe_dome([(0, 0), (0.05, 0), (0.035, 0.03), (0, 0.035)], center=(x, 0.765, -0.30), segments=14), m["led_cyan"])
    add_part(sm, "Desk03_KeyPad", keyboard(0, 0.765, 0.05, w=0.44), m["carbon_slate"])
    fr = []
    for s in (-0.24, 0.24):
        fr.append(tube([(s, 0.02, 0.95), (s, 0.02, 0.50), (s, 0.44, 0.62), (s, 0.44, 0.95), (s, 0.88, 1.08)], 0.016, fil=0.10))
    fr.append(tube([(-0.24, 0.02, 0.95), (0.24, 0.02, 0.95)], 0.016, fil=0.0))
    add_part(sm, "Desk03_CantileverChairFrame", merge_geometries(fr), m["steel_machined"])
    add_part(sm, "Desk03_LoungeSeat", make_sculpted_cushion((0.52, 0.09, 0.44), center=(0, 0.49, 0.76), res=(8, 3, 7), roundness=0.4, belly_puff=0.12), m["pad_charcoal"])
    add_part(sm, "Desk03_LoungeBack", transform_geom(make_sculpted_cushion((0.50, 0.46, 0.09), res=(8, 7, 3), roundness=0.4, belly_puff=0.12), translate=(0, 0.74, 1.00), rot_xyz_deg=(-18, 0, 0)), m["pad_charcoal"])
    return center_and_export_glb(os.path.join(OUT, "desk_r1_03.glb"), sm, "DeskR1_03_FloatingMagDesk")


def build_04(m):
    sm = []
    add_part(sm, "Desk04_GunmetalBench", merge_geometries([
        make_beveled_box((1.80, 0.07, 0.78), center=(0, 0.86, 0), bevel=0.02),
        make_beveled_box((0.48, 0.80, 0.70), center=(0.62, 0.42, 0), bevel=0.025),
        make_beveled_box((0.08, 0.82, 0.70), center=(-0.84, 0.41, 0), bevel=0.02),
        make_beveled_box((1.70, 0.05, 0.60), center=(0, 0.14, -0.02), bevel=0.02)]), m["gunmetal"])
    add_part(sm, "Desk04_OrangeDrawerFronts", merge_geometries([
        make_beveled_box((0.42, 0.22, 0.03), center=(0.62, 0.70 - i * 0.25, 0.36), bevel=0.012) for i in range(3)]), m["accent_orange"])
    add_part(sm, "Desk04_DrawerPulls", merge_geometries([
        tube([(0.52, 0.72 - i * 0.25, 0.38), (0.52, 0.72 - i * 0.25, 0.40), (0.72, 0.72 - i * 0.25, 0.40), (0.72, 0.72 - i * 0.25, 0.38)], 0.008, fil=0.01, seg=6) for i in range(3)]), m["steel_machined"])
    gantry = [tube([(-0.86, 0.90, -0.36), (-0.86, 1.80, -0.36), (0.86, 1.80, -0.36), (0.86, 0.90, -0.36)], 0.03, fil=0.12)]
    gantry.append(make_beveled_box((1.66, 0.62, 0.03), center=(0, 1.30, -0.38), bevel=0.01))
    add_part(sm, "Desk04_PegConduitGantry", merge_geometries(gantry), m["carbon_slate"])
    pegs = [make_cylinder(0.012, 0.012, 0.08, center=(-0.70 + i * 0.14, 1.10 + (i % 3) * 0.18, -0.33), segments=6, axis="z") for i in range(10)]
    add_part(sm, "Desk04_ToolPegs", merge_geometries(pegs), m["steel_machined"])
    arm = tube([(-0.60, 1.80, -0.36), (-0.60, 1.95, -0.20), (-0.30, 1.75, 0.05), (-0.10, 1.40, 0.15)], 0.022, fil=0.12)
    add_part(sm, "Desk04_ArticulatedScannerArm", merge_geometries([arm,
        make_cylinder(0.04, 0.04, 0.06, center=(-0.60, 1.95, -0.20), segments=12, axis="x"),
        make_cylinder(0.035, 0.035, 0.05, center=(-0.30, 1.75, 0.05), segments=12, axis="x")]), m["accent_orange"])
    add_part(sm, "Desk04_ScannerHead", make_lathe_dome([(0, 0), (0.11, 0), (0.12, 0.02), (0.06, 0.10), (0, 0.12)], center=(-0.10, 1.28, 0.15), segments=18), m["steel_machined"])
    add_part(sm, "Desk04_ScannerLight", make_cylinder(0.10, 0.10, 0.01, center=(-0.10, 1.275, 0.15), segments=18), m["led_ice"])
    add_part(sm, "Desk04_DiagnosticScope", merge_geometries([
        make_cylinder(0.08, 0.10, 0.06, center=(0.10, 0.92, 0.05), segments=14),
        transform_geom(make_cylinder(0.03, 0.045, 0.34, segments=12), translate=(0.10, 1.10, 0.0), rot_xyz_deg=(25, 0, 0))]), m["steel_machined"])
    add_part(sm, "Desk04_BlueprintVisor", transform_geom(make_quad_panel((-0.32, 0, 0), (0.32, 0, 0), (0.32, 0.40, 0), (-0.32, 0.40, 0)), translate=(0.45, 1.05, -0.18), rot_xyz_deg=(-12, 0, 0)), m["glass_holo_visor"])
    add_part(sm, "Desk04_AmberWorkLED", make_beveled_box((1.60, 0.015, 0.02), center=(0, 1.78, -0.33), bevel=0.004), m["led_amber"])
    swivel_chair(m, sm, "Desk04_IndustrialStool", center=(-0.30, 0, 0.75), stool=True, seat_mat="pad_charcoal", frame_mat="accent_orange")
    return center_and_export_glb(os.path.join(OUT, "desk_r1_04.glb"), sm, "DeskR1_04_EngineeringWorkbench")


WIN_05 = dict(w=1.10, h=0.70, cy=1.32, z=-0.46)

def build_05(m):
    sm = []
    w, h, cy, z = WIN_05["w"], WIN_05["h"], WIN_05["cy"], WIN_05["z"]
    alc = [make_open_backwall_frame(total_w=2.00, total_h=2.10, center_y=1.05, z_pos=-0.50, win_w=w, win_h=h, win_cy=cy, thick_z=0.10),
           make_beveled_box((0.14, 2.10, 1.10), center=(-0.93, 1.05, 0.0), bevel=0.03),
           make_beveled_box((0.14, 2.10, 1.10), center=(0.93, 1.05, 0.0), bevel=0.03),
           make_beveled_box((2.00, 0.14, 1.10), center=(0, 2.17, 0.0), bevel=0.03)]
    add_part(sm, "Desk05_TitaniumAlcoveShell", merge_geometries(alc), m["gunmetal"])
    add_part(sm, "Desk05_OctagonalWindowBezel", make_chamfered_aperture_ring(w + 0.06, h + 0.06, center_y=cy, z_pos=-0.44, tube_r=0.035, chamfer=0.16), m["steel_machined"])
    add_part(sm, "Desk05_TranslucentHullWindow", make_quad_panel((-w / 2, cy - h / 2, -0.47), (w / 2, cy - h / 2, -0.47), (w / 2, cy + h / 2, -0.47), (-w / 2, cy + h / 2, -0.47)), m["glass_viewport"])
    add_part(sm, "Desk05_BuiltInDeskTop", merge_geometries([
        make_beveled_box((1.72, 0.06, 0.62), center=(0, 0.76, -0.14), bevel=0.02),
        make_beveled_box((1.60, 0.10, 0.04), center=(0, 0.69, 0.15), bevel=0.012)]), m["aero_white"])
    cub = []
    for s in (-1, 1):
        x = s * 0.72
        cub.append(make_beveled_box((0.26, 0.02, 0.36), center=(x, 1.10, -0.28), bevel=0.006))
        cub.append(make_beveled_box((0.26, 0.02, 0.36), center=(x, 1.45, -0.28), bevel=0.006))
        cub.append(make_beveled_box((0.02, 0.90, 0.36), center=(x - s * 0.13, 1.33, -0.28), bevel=0.006))
    add_part(sm, "Desk05_SideCubbies", merge_geometries(cub), m["carbon_slate"])
    books = [make_beveled_box((0.03, 0.18 + 0.03 * (i % 3), 0.20), center=(s * 0.72 - 0.08 + i * 0.045, 1.21 + 0.015 * (i % 3), -0.30), bevel=0.004) for s in (-1, 1) for i in range(4)]
    add_part(sm, "Desk05_DataSlates", merge_geometries(books), m["accent_orange"])
    add_part(sm, "Desk05_AmberTaskLED", make_beveled_box((1.50, 0.014, 0.025), center=(0, 2.09, 0.30), bevel=0.004), m["led_amber"])
    add_part(sm, "Desk05_CyanWindowLED", tube([(-w / 2 - 0.06, cy - h / 2 - 0.08, -0.43), (w / 2 + 0.06, cy - h / 2 - 0.08, -0.43)], 0.008, fil=0.0, seg=6), m["led_cyan"])
    add_part(sm, "Desk05_TaskLampArm", tube([(0.62, 0.79, -0.36), (0.62, 1.00, -0.36), (0.45, 1.12, -0.10), (0.38, 1.05, 0.0)], 0.012, fil=0.08), m["steel_machined"])
    add_part(sm, "Desk05_TaskLampHead", make_lathe_dome([(0, 0), (0.06, 0), (0.05, 0.03), (0, 0.04)], center=(0.38, 1.02, 0.0), segments=14), m["led_amber"])
    add_part(sm, "Desk05_SlimOLED", transform_geom(make_quad_panel((-0.22, 0, 0), (0.22, 0, 0), (0.22, 0.14, 0), (-0.22, 0.14, 0)), translate=(-0.35, 0.80, -0.28), rot_xyz_deg=(-60, 0, 0)), m["oled_hud"])
    swivel_chair(m, sm, "Desk05_NavyFlightChair", center=(0, 0, 0.62), high_back=True, arms=True, seat_mat="pad_navy")
    return center_and_export_glb(os.path.join(OUT, "desk_r1_05.glb"), sm, "DeskR1_05_ViewportStudyNook")


if __name__ == "__main__":
    m = get_r2_materials()
    res = []
    for fn in (build_01, build_02, build_03, build_04, build_05):
        info = fn(m)
        d = info["dimensions"]
        print(f"{os.path.basename(info['filepath'])} tris={info['triangles']} dims={d[0]:.2f}x{d[1]:.2f}x{d[2]:.2f} min_y={info['min'][1]:.4f}")
        res.append(info)
    with open(os.path.join(OUT, "desk_r1_manifest.json"), "w") as f:
        json.dump(res, f, indent=2)
