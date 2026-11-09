"""Rook: Tennis Tower combined PREVIEW (box-side only, nothing here is a game scene).
Places every promoted tt_*.glb per design/tennis_tower_handoff/GAGE_NOTES.md + spec Rev 2.9 and the tt_struct_* blockout
in building coordinates, writes /workspace/renders/tennis_tower/structure_blockout/placements.json + a preview-only hull /
plinth mesh, then renders overview + cutaway shots with Godot (headless under xvfb, OpenGL3) from a throwaway project in
/tmp so no .import files land in the repo.  Usage: python3 assemble_preview.py [--no-render]"""
import os, sys, json, math, subprocess, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, trimesh
from tower_plan import *
ROOT = os.path.abspath(os.path.join(HERE, "../../../.."))
MD = os.path.join(ROOT, "godot/assets/models"); OUT = "/workspace/renders/tennis_tower/structure_blockout"
LAYOUT = json.load(open(os.path.join(MD, "tt_struct_layout.json")))
REPORT = {r["asset"]: r for r in json.load(open(os.path.join(OUT, "struct_report.json")))}
PL = []
def off(asset):  # bbox-centre offset of a recentred kit piece in its original local frame
    r = REPORT.get(asset); return r["world_offset"] if r else [0, 0, 0]
def put(asset, x, y, z, yaw=0, tag="misc", grid=False):
    """grid=True: (x,y,z) is the piece's design origin, so add the rotated recenter offset."""
    if grid:
        o = off(asset); a = math.radians(yaw); x += o[0]*math.cos(a) + o[2]*math.sin(a); z += -o[0]*math.sin(a) + o[2]*math.cos(a); y += o[1]
    PL.append(dict(glb=os.path.join(MD, asset + ".glb"), p=[round(x, 4), round(y, 4), round(z, 4)], yaw=yaw, tag=tag))
hull = lambda Z: (Z - 40) ** 2 / 400 - 4.0          # hull surface in building Y (F1 = +4.0 HD)

def structure():
    tags = dict(f1_slab="f1", f1_walls="f1", f2_slab="f2", f2_walls="f2", f3_slab="f3", f3_walls="f3", columns="cols", climb_frame="f2", void_guard="f3", diving_coffer="f3")
    for nm, d in LAYOUT.items():
        t = next((v for k, v in tags.items() if k in nm), "struct"); put(nm, *d["world_offset"], tag=t)
    for z in AQ_Z: put("tt_struct_aquatic_truss", 15, 9.7, z, tag="f2", grid=True)
    put("tt_struct_plant_stack", -6, 0, 5, 0, "plant", True); put("tt_struct_plant_stack", 134, 0, 74, 180, "plant", True)
    put("tt_struct_plant_stack_m", 134, 0, 5, 0, "plant", True); put("tt_struct_plant_stack_m", -6, 0, 74, 180, "plant", True)

def roof():
    Y = 22.325
    for i in range(7):
        for j in range(3): put("tt_roof_bay", -2 + 20*i, Y, 11.5 + 20*j, tag="roof")
        put("tt_roof_ridge_crown", -2 + 20*i + .075, Y + 3.346, 31.5 + .112 + 8, tag="roof")
    for x in (130, 134, 138):
        for j in range(15): put("tt_struct_roof_bay4", x, Y, 3.5 + 4*j, tag="roof", grid=True)
    for i in range(38):
        for z in (63.5, 67.5, 71.5, 75.5): put("tt_struct_roof_bay4", -10 + 4*i, Y, z, tag="roof", grid=True)
        put("tt_struct_roof_closure", -10 + 4*i, Y, .75, 180, "roof", True); put("tt_struct_roof_closure_chord", -10 + 4*i, Y, 78.25, 0, "roof", True)
    for j in range(19):
        put("tt_struct_roof_edge", -12, Y, 3.5 + 4*j, -90, "roof", True); put("tt_struct_roof_edge_chord", 140, Y, 3.5 + 4*j, 90, "roof", True)
    for x, z, yaw in ((-12, .75, -90), (-12, 78.25, -90), (140, .75, 90), (140, 78.25, 90)): put("tt_struct_roof_corner", x, Y, z, yaw, "roof", True)
    for x, yaw, s in ((-12, -90, 1), (140, 90, -1)):
        for z in (.75, 78.25): put("tt_struct_f3_corner_closure", x + s*.285, 12.2, z, yaw, "env", True)
    for i in range(4):
        for j in range(2): put("tt_struct_ball_net", 47.5 + 16*i, 21.5, 32 + 15*j, tag="roof", grid=True)

def envelope():
    for i in range(38):
        x = -10 + 4*i
        put("tt_curtain_wall_panel", x, 12.2, .285, 180, "env"); put("tt_curtain_wall_panel", x, 12.2, 79 - .285, 0, "env")
        for z0, yaw, s, sec in ((0, 180, -1, "s"), (79, 0, 1, "n")):
            if 68 < x < 76:
                if abs(x - 70) < .1: put(f"tt_secondary_entrance_{sec}", 72, 0, z0 + s*.98, yaw, "facade")
                continue
            put("tt_facade_bay", x, 0, z0 + s*.21, yaw, "facade")
    for j in range(19):
        z = 3.5 + 4*j
        put("tt_curtain_wall_panel", -12 + .285, 12.2, z, -90, "env"); put("tt_curtain_wall_panel", 140 - .285, 12.2, z, 90, "env")
        if 17.5 < z < 61.5: put("tt_entrance_bay", -12 - 1.07, 0, z, -90, "facade")  # 11 x 4 m, covers Z 17.5..61.5; no half bay
        else: put("tt_facade_bay", -12 - .21, 0, z, -90, "facade")
        if 33.5 < z < 41.5:
            if abs(z - 35.5) < .1: put("tt_secondary_entrance_e", 140 + .98, 0, 37.5, 90, "facade")
        else: put("tt_facade_bay", 140 + .21, 0, z, 90, "facade")
        if not 16 < z < 64:                                   # exposed plinth below the façade outside the terraces
            put("tt_plinth_skirt", -12, -4.0, z, -90, "site"); put("tt_plinth_skirt", 140, -4.0, z, 90, "site")

def site():
    for x0, x1 in ((-60, -12), (140, 168)):
        for x in np.arange(x0 + 2, x1, 4):
            for z in np.arange(18, 64, 4): put("tt_terrace_deck", float(x), -.3, float(z), tag="site")
        xo, yaw = (x0, -90) if x0 < 0 else (x1, 90)
        for z in np.arange(18, 64, 4):
            put("tt_terrace_edge", xo + (-1.25 if x0 < 0 else 1.25), -.3, float(z), yaw, "site"); put("tt_plinth_skirt_terrace", xo + (-2.3 if x0 < 0 else 2.3), -4.0, float(z), yaw, "site")
        for x in np.arange(x0 + 2, x1, 4):
            put("tt_terrace_edge", float(x), -.3, 16 - 1.25, 180, "site"); put("tt_terrace_edge", float(x), -.3, 64 + 1.25, 0, "site")
            put("tt_plinth_skirt_terrace", float(x), -4.0, 16 - 2.3, 180, "site"); put("tt_plinth_skirt_terrace", float(x), -4.0, 64 + 2.3, 0, "site")
    for x in (70, 74): put("tt_terrace_apron", x, -.27, 79.5, 0, "site")

def interiors():
    for cid, typ, (x0, x1, z0, z1) in CORES:
        a = "tt_stair_core_a" if typ == "A" else "tt_stair_core_b"; yaw = 90 if (x1 - x0) > (z1 - z0) else 0
        cx = (x0 + x1) / 2 if cid != "ST+S1" else 61.0
        for y in (0, 6.1): put(a, cx, y, (z0 + z1) / 2, yaw, "f1" if y == 0 else "f2")
    for _, (x0, x1, z0, z1), face in LIFTS:
        for y, t in ((-.15, "f1"), (5.95, "f2"), (12.05, "f3")): put("tt_lift_core", (x0 + x1) / 2, y, (z0 + z1) / 2, {"+z": 0, "-z": 180, "+x": 90, "-x": -90}[face], t)
    for x, z in TREES: put("tt_tree_column", x, 0, z, tag="cols")
    for x, z in TREES_W: put("tt_tree_column_west", x, 12.2, z, tag="f3")
    for y, t in ((0, "f1"), (6.1, "f2")):                                  # 5-row stands
        for x in (62.75, 55.25, 47.75, 80.25, 87.75, 95.25): put("tt_stand_module", x, y, 17.6, 0, t); put("tt_stand_module", x, y, 61.4, 180, t)
        for z in (30.75, 48.25): put("tt_stand_module", 32.6, y, z, 90, t); put("tt_stand_module", 110.4, y, z, -90, t)
    for x in (62.75, 55.25, 47.75, 80.25, 87.75, 95.25):
        for z, yaw in ((14.8, 0), (64.2, 180)):
            put("tt_stand_module_f3", x, 12.2, z, yaw, "f3"); put("tt_stand_module_f3_seats", x, 12.2, z, yaw, "f3")
    for z in (30.75, 48.25):
        for x, yaw in ((29.8, 90), (113.2, -90)):
            put("tt_stand_module_f3", x, 12.2, z, yaw, "f3"); put("tt_stand_module_f3_seats", x, 12.2, z, yaw, "f3")
    for x0, x1, z0, z1 in COURTS:                                          # F1 court boxes (2 m panels, door mid each long side)
        for k in range(10):
            x = x0 + 1 + 2*k; d = "tt_court_partition_door" if k == 4 else "tt_court_partition"
            put(d, x, 0, z0, 180, "f1"); put(d, x, 0, z1, 0, "f1")
        for k in range(5): z = z0 + 1 + 2*k; put("tt_court_partition", x0, 0, z, -90, "f1"); put("tt_court_partition", x1, 0, z, 90, "f1")
    # aquarium corridor kit (#80)
    for x in (3.75, 9.25, 14.75, 20.25): put("tt_aquarium_tank", x, 0, 42.9, 180, "f1")
    for x in (2.75, 8.25, 13.75, 19.25): put("tt_aquarium_floor", x, 0, 37.9, 0, "f1")
    for x in (5.0, 10.5, 16.0, 21.5): put("tt_aquarium_bench", x, 0, 40.9, 0, "f1")
    for x in (2.5, 23.5): put("tt_aquarium_plinth", x, 0, 36.0, 0, "f1")
    for x in (1.0, 24.0): put("tt_aquarium_sign", x, 2.6, 38.5, 90, "f1")
    for x in (6, 12, 18): put("tt_aquarium_caustic", x, 5.22, 40, 0, "f1")
    # foyer ticketing (#79 / Arrival 1bdac4f, §3.12.4): 2 desks, 2 staff-side backdrops, 8 kiosks, 30 stanchions
    for zc in (26, 53):
        put("tt_foyer_desk", -1.8036, 0, zc, -90, "f1"); put("tt_foyer_backdrop", -0.25, 0, zc, -90, "f1")
        for xl in (-5.5, -4.25, -3.0):
            for k in range(5): put("tt_foyer_stanchion", xl, 0, zc - 2.5 + 1.25*k, -90, "f1")
    for z0 in (30.5, 43.0):
        for k in range(4): put("tt_foyer_kiosk", -0.3495, 0, z0 + 0.875*k, -90, "f1")
    # aquatic slides
    put("tt_slide_tower", 22.5, 1.0, 53.5, 0, "f1"); put("tt_slide_tower", 22.5, 1.0, 59.5, 0, "f1")
    # restrooms (stall rows) per block
    for (x, z), y, t in [((107.5, 4), 0, "f1"), ((107.5, 9), 0, "f1"), ((37, 70), 0, "f1"), ((37, 74.5), 0, "f1"), ((107.5, 70), 0, "f1"), ((107.5, 74.5), 0, "f1"),
                         ((37, 70), 6.1, "f2"), ((37, 74.5), 6.1, "f2"), ((107.5, 70), 6.1, "f2"), ((107.5, 74.5), 6.1, "f2"), ((46, 12), 12.2, "f3"), ((97, 12), 12.2, "f3"), ((46, 67), 12.2, "f3"), ((97, 67), 12.2, "f3")]:
        put("tt_restroom", x, y, z, 0, t)
    # climbing (F2)
    for k in range(16):
        for c in range(5): put("tt_climbing_panel", 36.625 + 1.25*k, 6.1 + 2.3*c, 8.085, 180, "f2")
    for k in range(12): put("tt_climbing_panel_kids", 84.405, 6.1, .625 + 1.25*k, -90, "f2")
    for k in range(15): put("tt_climbing_panel_boulder", 94.625 + 1.25*k, 6.1, 14.31, 180, "f2")
    put("tt_climbing_panel_trim", 112.875, 6.1, 14.31, 180, "f2")
    for k in range(11): put("tt_climbing_panel_boulder", 112.61, 6.1, .625 + 1.25*k, -90, "f2"); put("tt_climbing_panel_boulder", 94.39, 6.1, .625 + 1.25*k, 90, "f2")
    # F3 W terrace: cabanas, bar
    for k in range(8): put("tt_cabana", -9, 12.2, 20 + 5.5*k, -90, "f3")
    put("tt_bar", 14, 12.2, 39.5, 180, "f3")
    for k in range(8): put("tt_bar_stool", 10.6 + k, 12.2, 37.4, 0, "f3")
    # F3 playground (Rev 2.9)
    for x in (131.3, 137.3):
        for z in np.arange(23.6, 59, 6): put("tt_play_surface", x, 12.2, float(z), 0, "f3")
    py = 12.2 + .038
    put("tt_toddler_zone", 134, py, 25.5, 0, "f3"); put("tt_soft_play", 132, py, 32.5, 0, "f3"); put("tt_see_saw", 136.5, py, 33, 90, "f3")
    put("tt_swing_set", 132.2, py, 40.5, 90, "f3"); put("tt_balance_trail", 137.3, py, 40.5, 90, "f3"); put("tt_dome_climber", 134, py, 48.4, 0, "f3")
    put("tt_play_tower", 134, py, 55.4, 0, "f3")
    for z in (25, 33, 41, 46): put("tt_aquarium_bench", 127.45, 12.2, z, 90, "f3")   # stand-in for the 1.8 x 0.5 playground bench (asset still needed)
    for z in np.arange(21.6, 58.4, 2):
        if 49.5 < z < 52: put("tt_fence_gate", 128.3, 12.2, 50.75, 90, "f3"); continue
        put("tt_fence_panel", 128.3, 12.2, float(z), 90, "f3")
    for x in np.arange(131, 140, 2): put("tt_fence_panel", float(x), 12.2, 20.6, 0, "f3"); put("tt_fence_panel", float(x), 12.2, 58.4, 0, "f3")
    put("tt_fence_gate", 129.25, 12.2, 20.6, 0, "f3"); put("tt_fence_gate", 129.25, 12.2, 58.4, 0, "f3")

def hull_mesh():  # preview-only hull + plinth / terrace fill, exported through the house pipeline (not a game asset)
    import struct_lib as SLB
    SLB.ML._m("pv_hull", "PV_HullTurf", (.34, .44, .33), 0, .95); SLB.ML._m("pv_fill", "PV_PlinthFill", (.27, .29, .31), 0, .9)
    xs = np.arange(-80, 200.1, 4.0); zs = np.arange(-12, 91.1, 1.0)
    X, Z = np.meshgrid(xs, zs); Y = hull(Z) - .02
    V = np.c_[X.ravel(), Y.ravel(), Z.ravel()]; nx = len(xs); F = []
    for j in range(len(zs) - 1):
        for i in range(nx - 1):
            a_ = j*nx + i; F += [[a_, a_ + nx, a_ + 1], [a_ + 1, a_ + nx, a_ + nx + 1]]
    g = trimesh.Trimesh(V, F, process=False); g.metadata["uv"] = np.c_[V[:, 0] / 8, V[:, 2] / 8]
    fills = [SLB.box(-12, 140, -4.4, -.41, 0, 79), SLB.box(-62.5, -12.01, -4.2, -.31, 13.5, 66.5), SLB.box(140.01, 170.5, -4.2, -.31, 13.5, 66.5)]
    p = os.path.join(OUT, "preview_hull.glb"); SLB.export_final({"Hull": ("pv_hull", g), "Fill": ("pv_fill", SLB.merge(fills))}, [p])
    PL.append(dict(glb=p, p=[0, 0, 0], yaw=0, tag="ground"))

ALL_UPPER = ["f2", "f3", "roof", "env", "facade", "plant"]
SHOTS = [  # name, camera pos, look-at, fov, hidden tags
 ("01_overview_sw_aerial", (-95, 70, -70), (60, 8, 40), 50, []),
 ("02_overview_ne_aerial", (215, 75, 150), (64, 8, 40), 50, []),
 ("03_west_arrival_terrace", (-58, 6, 6), (-12, 6, 42), 60, []),
 ("04_east_plaza_entrance", (172, 5, 22), (140, 5, 38), 60, []),
 ("05_south_face_grade", (72, 3, -38), (72, 10, 20), 65, []),
 ("06_roof_space_frame_aerial", (64, 60, -40), (64, 24, 40), 55, []),
 ("07_cutaway_f1_plan_aerial", (64, 120, -30), (64, 0, 40), 55, ALL_UPPER),
 ("08_cutaway_f1_aquatic_aerial", (-30, 45, -18), (15, 0, 40), 55, ALL_UPPER),
 ("09_cutaway_f1_courts", (64, 40, -10), (71.5, 0, 39.5), 55, ALL_UPPER),
 ("10_cutaway_f1_s_band_bowling_axe", (70, 30, -22), (70, 0, 8), 60, ALL_UPPER),
 ("11_cutaway_f1_food_court_n", (70, 30, 101), (70, 0, 71), 60, ALL_UPPER),
 ("12_cutaway_f1_arcade_e", (165, 35, 40), (126, 0, 40), 60, ALL_UPPER),
 ("13_cutaway_f2_plan_aerial", (64, 120, -30), (64, 6, 40), 55, ["f3", "roof", "env", "facade", "plant"]),
 ("14_cutaway_f2_climbing", (55, 32, -20), (65, 7, 8), 60, ["f3", "roof", "env", "facade", "plant"]),
 ("15_cutaway_f2_gallery_aquatic_hall", (-28, 36, 10), (10, 6, 45), 55, ["f3", "roof", "env", "facade", "plant"]),
 ("16_cutaway_f3_plan_aerial", (64, 125, -30), (64, 12, 40), 55, ["roof", "env"]),
 ("17_cutaway_f3_playground", (155, 40, 10), (134, 12, 40), 55, ["roof", "env"]),
 ("18_cutaway_f3_w_terrace_cabanas", (-35, 38, 10), (5, 12, 40), 55, ["roof", "env"]),
 ("19_int_foyer_main_entrance", (-9, 1.7, 14), (-6, 1.7, 40), 70, []),
 ("20_int_aquarium_corridor", (1.5, 1.7, 36.2), (22, 1.5, 40.5), 70, []),
 ("21_int_lap_pool_diving_hall", (1.2, 4.0, 2.0), (22, 2.5, 26), 75, []),
 ("22_int_leisure_river_slides", (2.0, 3.5, 77), (20, 3, 55), 75, []),
 ("23_int_f1_concourse_courts", (36, 2.0, 22.5), (72, 2.5, 40), 70, []),
 ("24_int_f1_court_box", (50, 1.7, 29), (66, 1.5, 36), 75, []),
 ("25_int_f1_bowling", (31, 1.7, 7.5), (56, 1.2, 7.5), 70, []),
 ("26_int_f2_rink_from_stand", (55, 9.2, 18), (72, 6.5, 40), 70, []),
 ("27_int_f2_lead_wall", (46, 7.8, 1.2), (46, 12, 8.2), 75, []),
 ("28_int_f2_bouldering", (96, 7.8, 2.0), (110, 8, 13), 75, []),
 ("29_int_f3_basketball_hall", (40, 15, 22), (100, 16, 55), 75, []),
 ("30_int_f3_stands_top_row", (70, 19.5, 10.5), (72, 12, 40), 75, []),
 ("31_int_f3_glass_box_roof_up", (72, 13.8, 40), (72, 22.5, 60), 85, []),
 ("32_int_f3_climbing_void_guard", (47, 13.9, 1.6), (40, 12, 8), 70, []),
 ("33_int_f3_cabanas_lounge", (-3.5, 13.9, 16), (-6, 13.6, 45), 70, []),
 ("34_int_f3_playground", (129, 14, 19), (135, 12.8, 45), 70, []),
 ("35_int_f3_track_s_straight", (2, 13.9, 1.6), (60, 13.5, 1.6), 70, []),
 ("36_int_f2_gallery_window", (-4.5, 7.8, 24), (12, 5, 40), 75, []),
 ("37_section_cut_x50_looking_e", (-30, 14, 40), (60, 10, 40), 60, ["facade", "env", "plant", "site", "ground"]),
 ("38_aquatic_trusses_coffer_from_below", (10, 3.5, 20), (16, 11, 28), 80, []),
]

def render():
    tmp = "/tmp/tt_preview"; os.makedirs(tmp, exist_ok=True)
    open(os.path.join(tmp, "project.godot"), "w").write('config_version=5\n[application]\nconfig/name="tt_preview"\n[rendering]\nrenderer/rendering_method="gl_compatibility"\n')
    shutil.copy(os.path.join(HERE, "render_preview.gd"), os.path.join(tmp, "render_preview.gd"))
    json.dump(dict(placements=PL, shots=[dict(name=n, pos=p, look=l, fov=f, hide=h, amb=(1.5 if "_int_" in n or n.startswith("38") else .6), out=os.path.join(OUT, n + ".png")) for n, p, l, f, h in SHOTS]), open(os.path.join(tmp, "job.json"), "w"))
    cmd = ["xvfb-run", "-a", "-s", "-screen 0 1920x1080x24", "godot", "--rendering-driver", "opengl3", "--resolution", "1600x900", "--path", tmp, "-s", "render_preview.gd"]
    print(" ".join(cmd)); subprocess.run(cmd, check=False, timeout=3000)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); structure(); roof(); envelope(); site(); interiors(); hull_mesh()
    json.dump(PL, open(os.path.join(OUT, "placements.json"), "w"), indent=0)
    from collections import Counter; c = Counter(os.path.basename(p["glb"]) for p in PL); print("placements", len(PL), "unique", len(c))
    miss = [p["glb"] for p in PL if not os.path.exists(p["glb"])]; print("missing", set(miss))
    if "--no-render" not in sys.argv: render()
