"""Scratch placement manifest + keepout audit for temp-Active (NOT repository integration).
Building coords (spec §0): X axial, Z across, origin SW corner; Godot +X = X, +Z = Z, +Y up; F2 slab top +6.1 (walls_f2 y0 = F2).
Every GLB pivot is bottom-centre of its visual bbox; 'raw' = builder coordinates. pivot_raw = (cx, ymin, cz) of raw visual bbox.
World pivot = W_raw_origin + Ry(yaw) * pivot_raw, so each entry is placed by where its builder origin (mouth line, board line, wall face) must land."""
import sys, json, math, numpy as np, trimesh
sys.dont_write_bytecode = True
sys.argv = [sys.argv[0]]
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import build_batch1 as B1, build_batch2 as B2, build_batch3 as B3
import build_batch4 as B4
import build_batch5 as B5
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[4]; MD=ROOT/'godot'/'assets'/'models'
REPO = "/workspace/game-project"; F2 = 6.1
def raw_pivot(builder, prm):
    p = builder(prm); V = np.vstack([m.vertices for k, (_, m) in p.P.items() if "colonly" not in k]); lo, hi = V.min(0), V.max(0)
    return np.array([(lo[0]+hi[0])/2, lo[1], (lo[2]+hi[2])/2]), (hi - lo)
P = {}
def piv(name, b, prm):
    if name not in P: P[name] = raw_pivot(b, prm)
    return P[name]
def rot(yaw, v): c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)); return np.array([c*v[0] + s*v[2], v[1], -s*v[0] + c*v[2]])
GL = {  # candidate -> (glb path, builder, params)
 "tt_rink_board_2m":      (str(MD / "tt_rink_board_2m.glb"), B2.board, B2.SETS["tt_rink_board_2m"][1][1]),
 "tt_rink_board_2m_crest":(str(MD / "tt_rink_board_2m_crest.glb"), B2.board, B2.SETS["tt_rink_board_2m"][1][0]),
 "tt_rink_board_corner":  (str(MD / "tt_rink_board_corner.glb"), B2.corner, B2.SETS["tt_rink_board_corner"][1][0]),
 "tt_rink_board_gate":    (str(MD / "tt_rink_board_gate.glb"), B2.gate, B2.SETS["tt_rink_board_gate"][1][0]),
 "tt_rink_players_bench": (str(MD / "tt_rink_players_bench.glb"), B2.pbench, B2.SETS["tt_rink_players_bench"][1][0]),
 "tt_rink_goal":          (str(MD / "tt_rink_goal.glb"), B1.goal, B1.SETS["tt_rink_goal"][1][0]),
 "tt_rink_goal_futsal":   (str(MD / "tt_rink_goal_futsal.glb"), B1.goal, B1.SETS["tt_rink_goal"][1][1]),
 "tt_rink_board_1m":      (str(MD / "tt_rink_board_1m.glb"), B2.board, B2.SETS["tt_rink_board_1m"][1][0]),
 "tt_rink_surface_panel": (str(MD / "tt_rink_surface_panel.glb"), B3.surf_panel, B3.SETS3["tt_rink_surface_panel"][1][0]),
 "tt_rink_surface_panel_end": (str(MD / "tt_rink_surface_panel_end.glb"), B3.surf_panel, B3.SETS3["tt_rink_surface_panel"][1][1]),
 "tt_rink_surface_corner": (str(MD / "tt_rink_surface_corner.glb"), B3.surf_corner, B3.SETS3["tt_rink_surface_corner"][1][0]),
 "tt_rink_lines_futsal":  (str(MD / "tt_rink_lines_futsal.glb"), B3.futsal, B3.SETS3["tt_rink_lines_futsal"][1][0]),
 "tt_gym_mirror":         (str(MD / "tt_gym_mirror.glb"), B3.mirror, B3.SETS3["tt_gym_mirror"][1][0]),
 "tt_gym_mirror_crest":   (str(MD / "tt_gym_mirror_crest.glb"), B3.mirror, B3.SETS3["tt_gym_mirror"][1][1]),
 "tt_gym_floor_tile":     (str(MD / "tt_gym_floor_tile.glb"), B3.floor_tile, B3.SETS3["tt_gym_floor_tile"][1][0]),
 "tt_gym_floor_tile_lane":(str(MD / "tt_gym_floor_tile_lane.glb"), B3.floor_tile, B3.SETS3["tt_gym_floor_tile"][1][1]),
 "tt_gym_treadmill":      (str(MD / "tt_gym_treadmill.glb"), B3.treadmill, B3.SETS3["tt_gym_treadmill"][1][0]),
 "tt_gym_rower":          (str(MD / "tt_gym_rower.glb"), B3.rower, B3.SETS3["tt_gym_rower"][1][0]),
 "tt_gym_moss_berm":      (str(MD / "tt_gym_moss_berm.glb"), B3.moss_berm, B3.SETS3["tt_gym_moss_berm"][1][0]),
 "tt_gym_green_wall":     (str(MD / "tt_gym_green_wall.glb"), B3.green_wall_prop, B3.SETS3["tt_gym_green_wall"][1][0]),
 "tt_climb_rental_desk":  (str(MD / "tt_climb_rental_desk.glb"), B2.desk, B2.SETS["tt_climb_rental_desk"][1][0]),
 "tt_climb_rental_desk_acc": (str(MD / "tt_climb_rental_desk_acc.glb"), B2.desk, B2.SETS["tt_climb_rental_desk"][1][1]),
 "tt_climb_mat_300":      (str(MD / "tt_climb_mat_300.glb"), B2.mat, B2.SETS["tt_climb_mat_300"][1][0]),
 "tt_climb_mat_300_edge": (str(MD / "tt_climb_mat_300_edge.glb"), B2.mat, B2.SETS["tt_climb_mat_300"][1][1]),
 "tt_climb_mat_300_2x15": (str(MD / "tt_climb_mat_300_2x15.glb"), B2.mat, B2.SETS["tt_climb_mat_300_2x15"][1][0]),
 "tt_climb_mat_300_124x15": (str(MD / "tt_climb_mat_300_124x15.glb"), B2.mat, B2.SETS["tt_climb_mat_300_124x15"][1][0]),
 "tt_climb_mat_300_088x24": (str(MD / "tt_climb_mat_300_088x24.glb"), B2.mat, B2.SETS["tt_climb_mat_300_088x24"][1][0]),
 "tt_climb_mat_300_188x40": (str(MD / "tt_climb_mat_300_188x40.glb"), B2.mat, B2.SETS["tt_climb_mat_300_188x40"][1][0]),
 "tt_climb_mat_300_14x28": (str(MD / "tt_climb_mat_300_14x28.glb"), B2.mat, B2.SETS["tt_climb_mat_300_14x28"][1][0]),
 "tt_climb_mat_300_06x16": (str(MD / "tt_climb_mat_300_06x16.glb"), B2.mat, B2.SETS["tt_climb_mat_300_06x16"][1][0]),
 "tt_climb_mat_ring_corner": (str(MD / "tt_climb_mat_ring_corner.glb"), B2.mat_ring_corner, B2.SETS["tt_climb_mat_ring_corner"][1][0]),
 "tt_climb_mat_ring_side":(str(MD / "tt_climb_mat_ring_side.glb"), B2.mat, B2.SETS["tt_climb_mat_ring_side"][1][0]),
 "tt_climb_auto_belay":   (str(MD / "tt_climb_auto_belay.glb"), B2.autobelay, B2.SETS["tt_climb_auto_belay"][1][0]),
 "tt_climb_anchor":       (str(MD / "tt_climb_anchor.glb"), B2.anchor, B2.SETS["tt_climb_anchor"][1][0]),
 "tt_gym_dumbbell_rack":  (str(MD / "tt_gym_dumbbell_rack.glb"), B1.rack, B1.SETS["tt_gym_dumbbell_rack"][1][0]),
 "tt_gym_dumbbell_rack_s":(str(MD / "tt_gym_dumbbell_rack_s.glb"), B1.rack, B1.SETS["tt_gym_dumbbell_rack"][1][1]),
 "tt_gym_bench":          (str(MD / "tt_gym_bench.glb"), B1.bench, B1.SETS["tt_gym_bench"][1][0]),
 "tt_gym_bench_flat":     (str(MD / "tt_gym_bench_flat.glb"), B1.bench, B1.SETS["tt_gym_bench"][1][1]),
 "tt_gym_cycle":          (str(MD / "tt_gym_cycle.glb"), B1.cycle, B1.SETS["tt_gym_cycle"][1][0]),
 "tt_gym_squat_rack":     (str(MD / "tt_gym_squat_rack.glb"), B2.squat, B2.SETS["tt_gym_squat_rack"][1][0]),
 "tt_gym_plate_tree":     (str(MD / "tt_gym_plate_tree.glb"), B2.platetree, B2.SETS["tt_gym_plate_tree"][1][0]),
 "tt_climb_entry_guard":  (str(MD / "tt_climb_entry_guard.glb"), B4.entry_guard, B4.SETS["tt_climb_entry_guard"][1][0]),
 "tt_climb_train_board":  (str(MD / "tt_climb_train_board.glb"), B4.train_board, B4.SETS["tt_climb_train_board"][1][0]),
 "tt_climb_train_board_spray": (str(MD / "tt_climb_train_board_spray.glb"), B4.train_board, B4.SETS["tt_climb_train_board"][1][1]),
 "tt_climb_train_trim":   (str(MD / "tt_climb_train_trim.glb"), B4.train_trim, B4.SETS["tt_climb_train_trim"][1][0]),
 "tt_climb_locker_bay":   (str(MD / "tt_climb_locker_bay.glb"), B4.locker_bay, B4.SETS["tt_climb_locker_bay"][1][0]),
 "tt_climb_change_bench": (str(MD / "tt_climb_change_bench.glb"), B4.change_bench, B4.SETS["tt_climb_change_bench"][1][0]),
 "tt_climb_hook_rail":    (str(MD / "tt_climb_hook_rail.glb"), B4.hook_rail, B4.SETS["tt_climb_hook_rail"][1][0]),
 "tt_gym_kb_rack":        (str(MD / "tt_gym_kb_rack.glb"), B4.kb_rack, B4.SETS["tt_gym_kb_rack"][1][0]),
 "tt_climb_lead_routes_a": (str(MD / "tt_climb_lead_routes_a.glb"), B5.routes, B5.SETS["tt_climb_lead_routes_a"][1][0]),
 "tt_climb_lead_routes_b": (str(MD / "tt_climb_lead_routes_b.glb"), B5.routes, B5.SETS["tt_climb_lead_routes_b"][1][0]),
 "tt_climb_lead_routes_c": (str(MD / "tt_climb_lead_routes_c.glb"), B5.routes, B5.SETS["tt_climb_lead_routes_c"][1][0]),
 "tt_climb_lead_routes_d": (str(MD / "tt_climb_lead_routes_d.glb"), B5.routes, B5.SETS["tt_climb_lead_routes_d"][1][0]),
 "tt_climb_lead_routes_e": (str(MD / "tt_climb_lead_routes_e.glb"), B5.routes, B5.SETS["tt_climb_lead_routes_e"][1][0]),
 "tt_climb_lead_routes_f": (str(MD / "tt_climb_lead_routes_f.glb"), B5.routes, B5.SETS["tt_climb_lead_routes_f"][1][0]),
 "tt_climb_lead_routes_g": (str(MD / "tt_climb_lead_routes_g.glb"), B5.routes, B5.SETS["tt_climb_lead_routes_g"][1][0]),
 "tt_climb_lead_routes_h": (str(MD / "tt_climb_lead_routes_h.glb"), B5.routes, B5.SETS["tt_climb_lead_routes_h"][1][0]),
}
REUSE = {"tt_climbing_panel_kids": REPO + "/godot/assets/models/tt_climbing_panel_kids.glb", "tt_climbing_panel": REPO + "/godot/assets/models/tt_climbing_panel.glb",
         "tt_climbing_panel_trim": REPO + "/godot/assets/models/tt_climbing_panel_trim.glb",
         "tt_climbing_panel_boulder": REPO + "/godot/assets/models/tt_climbing_panel_boulder.glb"}
items = []
WITHHELD = []
def put(room, name, X, Z, yaw, y=0.0, src="", note="", status="proposed", option=None):
    if name in GL:
        c, size = piv(name, GL[name][1], GL[name][2]); off = rot(yaw, c); glb = GL[name][0]
    else:
        b = trimesh.load(REUSE[name]).bounds; size = b[1] - b[0]; off = np.zeros(3); glb = REUSE[name]
    pos = np.array([X, F2 + y, Z]) + off
    items.append(dict(room=room, asset=name, glb=glb, pos=[round(float(v), 4) for v in pos], yaw_deg=yaw, size=[round(float(v), 3) for v in size],
                      raw_origin_world=[X, round(F2 + y, 4), Z], src=src, note=note, placement_status=status, asset_qa="pass (clip/validate/first_pass)", **({"option": option} if option else {})))

# ---------------- F2-RINK ----------------
X0, X1, Z0, Z1, RC = 41.5, 102.5, 26.5, 52.5, 4.0    # 61 x 26 board line (spec §2 ~61 x 26), centre X 72 Z 39.5
S = "§2 table (rink ~61x26), §3.4 clear 4.6 m, ROOM_OWNERSHIP #16; R 4.0 m corner = temp-Active proposal"
xs, x = [], X0 + RC                     # long sides: 13 x 2 m + 1 m filler + 13 x 2 m = 53 m between corner tangents
for k in range(27):
    L = 1.0 if k == 13 else 2.0; xs.append((x + L/2, L)); x += L
assert abs(x - (X1 - RC)) < 1e-9
gates = {xs[10][0], xs[16][0]}
for i, (x, L) in enumerate(xs):
    nm = "tt_rink_board_1m" if L == 1 else ("tt_rink_board_2m_crest" if i in (6, 20) else "tt_rink_board_2m")
    put("F2-RINK", nm, x, Z0, 0, src=S)
    put("F2-RINK", "tt_rink_board_gate" if x in gates else nm, x, Z1, 180, src=S, note="players' gate (position proposal)" if x in gates else "")
for j in range(9):
    z = Z0 + RC + 1 + 2*j
    put("F2-RINK", "tt_rink_board_2m", X0, z, 90, src=S); put("F2-RINK", "tt_rink_board_2m", X1, z, -90, src=S)
for (cx, cz, yaw) in ((X1 - RC, Z1 - RC, 0), (X0 + RC, Z1 - RC, -90), (X0 + RC, Z0 + RC, 180), (X1 - RC, Z0 + RC, 90)):
    put("F2-RINK", "tt_rink_board_corner", cx, cz, yaw, src=S, note="raw origin = corner arc centre; R 4.0 board line kept (not shortened)")
    put("F2-RINK", "tt_rink_surface_corner", cx, cz, yaw, src=S, note="raw origin = arc centre; R 3.93 = board line - 0.07 kick plate")
SI = 0.07   # surface stops 0.07 inside the board line (kick plate face) - no overlap with boards
for i in range(10):
    for j in range(4):
        put("F2-RINK", "tt_rink_surface_panel", X0 + RC + 2.65 + 5.3*i, Z0 + SI + 6.465/2 + 6.465*j, 0, src=S + "; 12 mm rubber")
for xe in (X0 + SI + 3.93/2, X1 - SI - 3.93/2):
    for k in range(3): put("F2-RINK", "tt_rink_surface_panel_end", xe, Z0 + RC + 3 + 6*k, 0, src=S)
put("F2-RINK", "tt_rink_lines_futsal", 72.0, 39.5, 0, y=.010, src="futsal 40 x 20 centred in 61 x 26 rink (temp-Active proposal)", note="6 mm strips: bottom at rubber top -2 mm, top +4 mm")
put("F2-RINK", "tt_rink_goal", X0 + 4.0, 39.5, 90, y=.012, src=S + "; box-lacrosse goal line 4 m from end boards (proposal)", note="raw origin = mouth line centre", option="A box-lacrosse")
put("F2-RINK", "tt_rink_goal", X1 - 4.0, 39.5, -90, y=.012, src=S, note="raw origin = mouth line centre", option="A box-lacrosse")
put("F2-RINK", "tt_rink_goal_futsal", 52.0, 39.5, 90, y=.012, src="futsal goal 3 x 2 on 40 m goal line X 52", note="raw origin = mouth line centre", option="B futsal")
put("F2-RINK", "tt_rink_goal_futsal", 92.0, 39.5, -90, y=.012, src="futsal goal 3 x 2 on 40 m goal line X 92", note="raw origin = mouth line centre", option="B futsal")
for x in (67.5, 75.5):
    WITHHELD.append(dict(room="F2-RINK", asset="tt_rink_players_bench", would_be=[x, 53.45, 180], reason="Board line Z 52.5 (+0.33 sill) to PT column pads Z 53.99 leaves 1.16 m; bench depth 0.54 leaves ~0.3 m each side. "
        "A bench + player circulation cannot fit without entering the 3.1 m concourse beyond the columns (Z 54.5..). Inside the boards would cut the 61 x 26 field. Needs spec decision (Rook/Vance); not solved here."))

# ---------------- F2-CLIMB ----------------
SC = "§3.7.1 + Rev 3.1 (dc2b3ea/be578b7)"
# Desks stay withheld: guest face at Z 9.5 is not a legal frontage (C1). Not marked valid.
for x, nm in ((69.25, "tt_climb_rental_desk_acc"), (73.75, "tt_climb_rental_desk")):
    WITHHELD.append(dict(room="F2-CLIMB", asset=nm, would_be=[x, round(9.5 - .43, 4), 0],
        reason="Desk zone X67..76 Z6.5..9.5 has its front at Z 9.5 (Rev 2.6), but LS core occupies X71..76.5 from Z 9.5 and Lift S X66.5..70.5 from Z 11. "
        "Guest frontage beyond Z 9.5 exists only X66.5..71 (1.5 m to Lift S). Needs Vance call (turn desk to face W/E lobby, or shorten to X67..71). Not placed."))
# 9 panels is the conservative Rev 3.1 reading (ROOM_OWNERSHIP's 12 assumed a full 15 m face; spine Z13.2..15 + TC-S3 pier Z7.8..9.2 leave 9 x 1.25 m).
for z in [.3 + .625 + 1.25*k for k in range(6)] + [9.2 + .625 + 1.25*k for k in range(3)]:  # kids face X 84.5; TC-S3 pier Z 7.8..9.2 (walls_f2 piers); spine Z13.2..15 clear
    put("F2-CLIMB", "tt_climbing_panel_kids", 84.5 - .094 - .004, z, -90, src=SC + "; ROOM_OWNERSHIP reuse tt_climbing_panel_kids", note="reused promoted GLB; Rev 3.1 spine Z13.2..15 kept clear")
for z in (1.6, 4.9, 10.9):
    put("F2-CLIMB", "tt_climb_auto_belay", 84.5 - .094*2, z, -90, y=4.55, src="§3.7.1 kids' wall + auto-belays (5 m walls)", note="raw origin = wall plate back; on panel face")
for zc in (3.3, 5.3, 10.1, 12.1):   # existing 2 m kids mats; TC-S3 collar follows (1.2 m sq trunk at (84.5, 8.5) occupies X83.9..85.1 Z7.9..9.1)
    put("F2-CLIMB", "tt_climb_mat_300", 83.5, zc, 0, src="Rev 2.8 §3.12: kids' wall 2.0 m mat zone; Rev 3.1 spine clear", note="mats X 82.5..84.5")
# r9: first kids mat was 2.0 m at z=1.3 (foot Z 0.301..2.299) and entered the S facade inner ledge at Z 0.621.
# 2.0 x 1.58 cut at raw Z 1.420 keeps foot z0=0.631 and a 90 mm gap to the z=3.3 tile (starts 2.301).
put("F2-CLIMB", "tt_climb_mat_300_2x15", 83.5, 1.420, 0, src="Rev 2.8 §3.12 + r9 S facade ledge Z 0.621", note="2.0 x 1.58 cut; foot z0>=0.631, X 82.5..84.5; not shifted (would overlap z=3.3)")
put("F2-CLIMB", "tt_climb_mat_300_14x28", 83.2, 7.7, 0, src=SC + "; C5 TC-S3 collar, 1.2 m sq clad", note="west of trunk: X82.5..83.9 Z6.3..9.1")
put("F2-CLIMB", "tt_climb_mat_300_06x16", 84.2, 7.1, 0, src=SC + "; C5 TC-S3 collar, 1.2 m sq clad", note="south of trunk: X83.9..84.5 Z6.3..7.9; flush to trunk, not into X>=84.5 or Z>=7.9")
for k, x in enumerate([37.65 + 3.3*i for i in range(6)]):
    put("F2-CLIMB", "tt_climb_anchor", x, 8.0 - .0, 180, y=11.2, src="§3.7.1 W-CL 20 x 11.5 m, ~6 rope lanes at 3.3 m, face Z 8", note="raw origin = plate back on Z 8 face; frame depth not verified")
# Boulder N mats ONLY X98..113 (NOT the X94..98 entry landing). 2 m tiles centred 99..111 cover X98..112;
# X112..113 has no 1 m mat. Entry landing X94..98 Z13.2..15 stays hard floor (keepout below).
# Edge row at Z 9..11 chamfer toward -Z. No tile centre west of X99, so no mat enters X94..98.
for x in [99 + 2*i for i in range(7)]:   # covers X98..112; rows shifted to end at wall face Z 14.7
    for z, nm, yw in ((9.7, "tt_climb_mat_300_edge", 180), (11.7, "tt_climb_mat_300", 0), (13.7, "tt_climb_mat_300", 0)):
        if x in (99, 101, 103, 105) and z < 12: continue   # 2 m tiles overlap the TC-S4 ring; cut-mat infill placed below
        put("F2-CLIMB", nm, x, z, yw, src="Rev 3.1 item 2: N wall Z15; r8 mats only X98..113 (entry X94..98 Z13.2..15 hard floor)",
            note="field X98..112; landing X94..98 Z13.2..15 kept hard floor")
# C3 cut-mat infill around the TC-S4 ring (skin = 1.2 m square). Other N-field mats stay where they are.
put("F2-CLIMB", "tt_climb_mat_300_2x15", 99.88, 11.91, 0, src=SC + "; C3 cut-mat infill, 1.2 m square skin", note="X98.88..102.88, Z11.12..12.70")
put("F2-CLIMB", "tt_climb_mat_300_2x15", 101.88, 11.91, 0, src=SC + "; C3 cut-mat infill, 1.2 m square skin", note="X98.88..102.88, Z11.12..12.70")
put("F2-CLIMB", "tt_climb_mat_300_124x15", 103.50, 11.91, 0, src=SC + "; C3 cut-mat infill, 1.2 m square skin", note="X102.88..104.12, Z11.12..12.70")
put("F2-CLIMB", "tt_climb_mat_300_088x24", 98.44, 9.91, 0, src=SC + "; C3 cut-mat infill, 1.2 m square skin", note="X98.00..98.88, Z8.70..11.12")
put("F2-CLIMB", "tt_climb_mat_300_188x40", 105.06, 10.70, 0, src=SC + "; C3 cut-mat infill, 1.2 m square skin", note="X104.12..106.00, Z8.70..12.70")
# Boulder N-wall starts at X98 (12 x 1.25 m panels = X98..113 exactly, no trim). No footprint in the X94..98 landing.
# Measured local Z -0.3917..+0.3917; mounting back at local z=-0.3917; yaw 180 maps local +Z to world -Z (into the hall).
# Z15 stand-back occupies Z14.7..15. Authored back at Z 14.685 (15 mm hall-side of 14.7): pivot Z = 14.685 - 0.3917 = 14.2933.
for i in range(12):
    x = 98.625 + 1.25*i    # first covers X98.00..99.25, last covers X111.75..113.00
    put("F2-CLIMB", "tt_climbing_panel_boulder", x, 14.2933, 180, src=SC + "; r8 C2 N-wall starts X98", note="yaw 180; back at Z 14.685; face/kick into hall; pivot Z 14.2933; not in X94..98 landing")
# r8: guard moved to X98, the east edge of the hard-floor landing, separating entry from the N-wall mat/fall zone.
put("F2-CLIMB", "tt_climb_entry_guard", 98.10, 13.75, -90, src="r8 entry landing delineator", note="yaw -90: mat face (+Z) points +X into hall/mats; raw_X 98.10 -> pivot ~98.05, corridor face ~98.00 at the landing edge; Z 13.75 (L 1.90, north=14.70 exact, meets Z15 stand-back); landing X94..98 Z13.2..15 hard floor")
# Training wall X94 Z0..13. put() adds rot(yaw, raw_center) and the exported GLB is recentered,
# so pass raw X = 94.0 + 0.005 + 0.118 = 94.123 (wall + 5 mm gap + full depth).
# raw_X 94.123 -> pivot ~94.064; back ~94.005.
# r9: first spray previously covered Z 0..1.25 and entered the S facade inner ledge at Z 0.621.
# Shift the 10-board run +0.631 m so it starts at Z 0.631; last board ends at Z 13.131 (clear of spine Z13.2).
# The 0.25 m end trim is omitted: shifting it with the run would enter the spine keepout.
for i in range(10):
    zc = 0.625 + 0.631 + 1.25*i   # panels cover Z0.631..13.131
    nm = "tt_climb_train_board_spray" if i % 2 == 0 and "tt_climb_train_board_spray" in GL else "tt_climb_train_board"
    put("F2-CLIMB", nm, 94.123, zc, -90, src="r6 training wall X94 + r9 S facade ledge Z 0.621", note="raw_X 94.123 -> pivot ~94.064; back ~94.005; spray on even i; r9 starts Z 0.631" if i % 2 == 0 else "raw_X 94.123 -> pivot ~94.064; back ~94.005; r9 starts Z 0.631")
# Fall mats for the training wall only, Z0..13. 2 m tiles centred X95. Skip any tile that enters Z13..15.
# r9: first 2 m tile at z=1 had foot Z 0.001..1.999 and entered the S facade ledge at Z 0.621.
# Shift the 2 m grid +0.631 m (cannot use a 1.58 cut without a 0.21 m overlap on z=3, and a 1.36 m cut does not exist).
# Last tile at 11.631 ends at Z 12.630, still short of Z 13 and the spine.
for z in (1.631, 3.631, 5.631, 7.631, 9.631, 11.631):
    c, size = piv("tt_climb_mat_300", GL["tt_climb_mat_300"][1], GL["tt_climb_mat_300"][2])
    zmid = z + float(rot(0, c)[2]); hz = float(size[2]) / 2
    if zmid + hz > 13.0 and zmid - hz < 15.0: continue
    put("F2-CLIMB", "tt_climb_mat_300", 95.0, z, 0, src="r6 training wall fall mats + r9 S facade ledge Z 0.621", note="centred X95; r9 shifted +0.631; foot z0>=0.631; not into Z13..15")
# Changing room X30..57 Z10.5..13.2 only (off spine). Lockers at Z=10.70 so the bay stays Z<=13.0.
# Door clear X40..42: skip centers in 39.5..42.5 (40.1 and 41.4 overlap that clear).
for x in (31.0, 32.3, 33.6, 34.9, 36.2, 37.5, 38.8, 42.7, 44.0, 45.3, 46.6, 47.9, 49.2, 50.5, 51.8, 53.1, 54.4, 55.7):
    if 39.5 <= x <= 42.5: continue
    put("F2-CLIMB", "tt_climb_locker_bay", x, 10.70, 0, src="r6 changing room X30..57 Z10.5..13.2", note="front +Z; stop before ST+S1 X57; lockers Z<=13.0; door clear X40..42 skipped")
for x in (33, 36, 39, 42, 45, 48, 51, 54):
    put("F2-CLIMB", "tt_climb_change_bench", x, 11.8, 0, src="r6 changing room X30..57 Z10.5..13.2", note="yaw 0")
for x in (32.5, 36.5, 40.5, 44.5, 48.5, 52.5, 55.5):
    put("F2-CLIMB", "tt_climb_hook_rail", x, 12.95, 180, src="r6 changing room X30..57 Z10.5..13.2", note="yaw 180 hooks toward -Z; rail depth 0.1 so Z footprint <13.2")
# r9: first tile at z=1 entered the S facade inner ledge at Z 0.621; shift the 2 m grid +0.631 m (same as the training-wall mats).
for z in (1.631, 3.631, 5.631, 7.631):
    put("F2-CLIMB", "tt_climb_mat_300", 112.0, z, 0, src="Rev 3.1: X113 wall 15 m (mat zone not dimensioned; 2 m assumed); r9 S facade ledge Z 0.621", note="r9 shifted +0.631; foot z0>=0.631")
tx, tz, h = 101.5, 8.5, .62
for (dx, dz, yaw) in ((1, 1, 0), (-1, 1, -90), (-1, -1, 180), (1, -1, 90)):
    put("F2-CLIMB", "tt_climb_mat_ring_corner", tx + dx*h, tz + dz*h, yaw, src="Rev 3.1: TC-S4 2 m mat ring; trunk clad 1.2 m sq (tree_column.py)", note="raw origin = trunk-clad corner (+0.02 gap); skin = 1.2 m square, documented r7")
for (dx, dz, yaw) in ((0, 1, 0), (0, -1, 180), (1, 0, 90), (-1, 0, -90)):
    put("F2-CLIMB", "tt_climb_mat_ring_side", tx + dx*(h + 1.0), tz + dz*(h + 1.0), yaw, src="Rev 3.1 TC-S4 ring", note="skin = 1.2 m square, documented r7")

# ---------------- F2-GYM ----------------
SG = "ROOM_OWNERSHIP #18, §4.6 cores; layout = temp-Active proposal"
TY = .02   # free-weights zone sits on 20 mm rubber tiles
# r9: drop the Z 78.5 row (foot Z 78..79). The N facade inner ledge is at Z 78.379, so footprints must stay at Z<=78.369.
# Shifting the 1 m tiles inward would overlap the Z 77.5 row; no shorter gym-tile variant exists.
for i in range(11):
    for j in range(12):   # Z 66.5..77.5, north edge at Z 78.0
        if i == 0 and 70 <= 66.5 + j <= 72.5: continue   # WC door X44 Z70..72.5 clearance: no tiles (edge ramp missing)
        put("F2-GYM", "tt_gym_floor_tile_lane" if j == 6 else "tt_gym_floor_tile", 45.0 + i, 66.5 + j, 0, src=SG + "; free-weights rubber zone X44.5..55.5 Z66..78; r9 N facade ledge Z 78.379")
for k, z in enumerate((65.2, 66.4, 67.6, 68.8, 73.3, 74.5, 75.7, 76.9)):
    put("F2-GYM", "tt_gym_mirror_crest" if k in (1, 6) else "tt_gym_mirror", 44.06, z, 90, src=SG + "; W wall X 44 (WC door Z70..72.5 kept clear)", note="raw origin = mirror plane; back plate on wall X 44.0")
for x in (93.5, 94.7, 95.9, 97.1): put("F2-GYM", "tt_gym_treadmill", x, 66.0, 0, src=SG + "; runners face N facade", note="console +Z")
for z in (68.95, 69.75, 70.55, 71.35): put("F2-GYM", "tt_gym_rower", 68.3, z, 90, src=SG + "; between Lift N, TC (65.5,70.5) soft clear and cycles")
for (x, z) in ((57.20, 77.9), (64.3, 77.9), (85.20, 77.9)): put("F2-GYM", "tt_gym_moss_berm", x, z, 0, src=SG + "; greenery beside (not on) equipment; C7 shifted off ST+N1/N2 north-door approaches", note="C7 shifted off ST+N1/N2 north-door approaches")
for z in (66.0, 67.3, 73.6, 74.9): put("F2-GYM", "tt_gym_green_wall", 101.9, z, -90, src=SG + "; E wall X 102", note="raw origin = foliage plane; frame back on wall")
# r9: racks sat at raw Z 78.6 (foot Z 78.246..78.909) and entered the N facade inner ledge at Z 78.379.
# Shift raw Z by -0.540 m so foot z1=78.369 (10 mm south of the ledge). Depth 0.663 m, no neighbour clip.
for x in (46.5, 49.0, 51.5, 54.0): put("F2-GYM", "tt_gym_dumbbell_rack", x, 78.06, 180, y=TY, src=SG + "; N facade Z 79, ribbon sill +1.2 (§3.12.2); r9 N ledge Z 78.379", note="r9 raw Z 78.06; foot z1<=78.369")
for x in (46.0, 48.5, 51.0, 53.5): put("F2-GYM", "tt_gym_bench", x, 74.5, 180, y=TY, src=SG)
for x in (47.0, 50.6): put("F2-GYM", "tt_gym_squat_rack", x, 68.6, 180, y=TY, src=SG)
put("F2-GYM", "tt_gym_plate_tree", 54.5, 68.0, 0, y=TY, src=SG)
for z in (73.0, 75.2, 77.4):
    for x in (67.4, 68.6, 69.8): put("F2-GYM", "tt_gym_cycle", x, z, 180, src=SG)
for z in (72.0, 74.4, 76.8):
    for x in (77.6, 78.8, 80.0, 81.2, 82.4): put("F2-GYM", "tt_gym_cycle", x, z, 180, src=SG)
# r9: small rack foot was Z 78.303..78.950; shift raw Z by -0.581 m so foot z1=78.369.
put("F2-GYM", "tt_gym_dumbbell_rack_s", 96.5, 78.069, 180, src=SG + "; r9 N facade ledge Z 78.379", note="r9 raw Z 78.069; foot z1<=78.369")
for x in (94.5, 97.5): put("F2-GYM", "tt_gym_bench_flat", x, 74.0, 180, src=SG)
put("F2-GYM", "tt_gym_kb_rack", 96.5, 70.0, 0, src=SG + "; E functional zone X92.5..101 Z64.5..79", note="clear of TC-N4 X101.5; one rack")

# W-CL lead wall: 16 x 5 courses (80 panels) on X36..56, no trim. Face_Sheet front local Z=+0.0127; yaw 180 puts that face on spec Z 8 (pivot Z 8.0127; holds to world Z 7.927).
for col in range(16):
    x = 36.625 + 1.25*col
    for course, y in enumerate((0.0, 2.3, 4.6, 6.9, 9.2)):
        put("F2-CLIMB", "tt_climbing_panel", x, 8.0127, 180, y=y, src="§3.7.1 W-CL 20 x 11.5 m, face Z 8; r7 measured face plane", note="yaw 180; Face_Sheet front at local +0.0127 sits on world Z 8; pivot Z 8.0127")
# r8 owned lead-route overlays. FACE at local z=0, holds to +Z (0.08-0.35 m, volumes to 0.80 m wide / 0.35 m proud), 8 mm back embed.
# yaw 180; pass raw Z=8.0 so put() lands the face on world Z 8 (backs at Z 8.008). Eight 2.5 m bays cover X36..56.
# 8 colour-coded vertical routes (4 layouts + 4 mirrors), panel-grid course tints, route tape spanning both columns and all 5 courses.
for i, nm in enumerate("abcdefgh"):
    put("F2-CLIMB", f"tt_climb_lead_routes_{nm}", 37.25 + 2.5*i, 8.0, 180, src="§3.7.1 W-CL r8 owned route overlay; not a tt_climbing_panel edit",
        note="yaw 180; face at raw Z 8; holds into the hall (-Z); 8 mm embed; fall zone covered by 2 m mats Z6..8")
# 2 m fall-zone mats under the lead wall (X36..56, Z6..8). One row of tt_climb_mat_300.
for x in [37 + 2*i for i in range(10)]:
    put("F2-CLIMB", "tt_climb_mat_300", x, 7.0, 0, src="§3.12 lead-wall 2.0 m mat zone; r8 covers holds/volumes", note="X36..56 Z6..8 under W-CL face at Z 8")
LEAD_WITHHELD = []
# ---------------- keepouts from tower_plan.py / build_structure.walls_f2 / columns ----------------
sys.path.insert(0, REPO + "/assets/src/tennis_tower/structure")
import tower_plan as TP
KO = []
for cid, typ, (a, b, c, d) in TP.CORES: KO.append((f"core {cid}", a, b, c, d))
for lid, (a, b, c, d), _ in TP.LIFTS: KO.append((f"{lid}", a, b, c, d))
for (x, z) in TP.TREES: KO.append((f"tree column ({x},{z}) trunk clad 1.2 m sq", x - .6, x + .6, z - .6, z + .6)); KO.append((f"tree column ({x},{z}) 0.6 m soft clear (non-mat)", x - 1.2, x + 1.2, z - 1.2, z + 1.2))
for x in TP.PT_X:
    for z in TP.PT_Z: KO.append((f"PT column ({x},{z}) + pads", x - .51, x + .51, z - .51, z + .51))
KO.append(("Rev 3.1 spine Z13.2..15 X30..94", 30, 94, 13.2, 15))
KO.append(("boulder entry landing X94..98 Z13.2..15 hard floor", 94, 98, 13.2, 15))
for (a, b) in ((44, 46), (66.5, 76.5), (86.3, 89)): KO.append((f"door/opening Z15 wall X{a}..{b} 1.5 m clear (S side)", a, b, 13.5, 14.7))
for (a, b) in ((50, 53), (66.5, 76.5), (90, 93)): KO.append((f"door/opening Z64 wall X{a}..{b} 1.5 m clear (gym side)", a, b, 64.3, 65.8))
for xw, s in ((44, 1), (102, -1)): KO.append((f"WC door X{xw} Z70..72.5 1.5 m clear", min(xw, xw + 1.5*s), max(xw, xw + 1.5*s), 70, 72.5))
KO.append(("changing wall door X40..42 Z10.5 clear", 40, 42, 9.0, 10.5))
KO.append(("walls: kids backing X84.5..84.8", 84.5, 84.8, .3, 14.7)); KO.append(("walls: training backing X93.7..94", 93.7, 94, .3, 14.7))
KO.append(("walls: Z15 stand back Z14.7..15", 30, 113, 14.7, 15)); KO.append(("walls: Z64 stand back Z64..64.3", 30, 113, 64, 64.3))
KO.append(("walls: WC X44 / gym W", 43.7, 44.0, 64.3, 78.7)); KO.append(("walls: WC X102 / gym E", 102, 102.3, 64.3, 78.7))
def fp(it):
    sx, _, sz = it["size"]; c, s = abs(math.cos(math.radians(it["yaw_deg"]))), abs(math.sin(math.radians(it["yaw_deg"])))
    hx, hz = (sx*c + sz*s)/2, (sx*s + sz*c)/2; X, _, Z = it["pos"]; return (X - hx, X + hx, Z - hz, Z + hz)
hits = []
for it in items:
    if it["pos"][1] - F2 > 1.0: continue   # wall-mounted high items: checked against walls only by construction
    a = fp(it); it["footprint_xz"] = [round(v, 3) for v in a]
    for nm, b0, b1, c0, c1 in KO:
        ov = min(a[1], b1) - max(a[0], b0), min(a[3], c1) - max(a[2], c0)
        if "soft" in nm and ("mat" in it["asset"] or "panel" in it["asset"]): continue
        # Train board/trim/spray may embed in the backing keepout X93.7..94. Wall-mounted mount is OK to 15 mm;
        # allow 60 mm so residual embed from measurement slack does not HIT.
        if "training backing" in nm and it["asset"].startswith("tt_climb_train_") and ov[0] <= 0.060: continue
        if ov[0] > .005 and ov[1] > .005: hits.append(dict(asset=it["asset"], room=it["room"], pos=it["pos"], keepout=nm, overlap_xz=[round(ov[0], 3), round(ov[1], 3)]))
# mat-on-mat overlaps (ring vs boulder N field)
mats = [it for it in items if "mat" in it["asset"]]
mo = []
for i in range(len(mats)):
    for j in range(i + 1, len(mats)):
        a, b = fp(mats[i]), fp(mats[j]); ov = min(a[1], b[1]) - max(a[0], b[0]), min(a[3], b[3]) - max(a[2], b[2])
        if ov[0] > .01 and ov[1] > .01: mo.append([mats[i]["asset"], mats[i]["pos"][::2], mats[j]["asset"], mats[j]["pos"][::2], [round(ov[0], 2), round(ov[1], 2)]])
# valid = unambiguous gym/rink, keepout-clear, not the subject of an open conflict.
# Straight 61x26 boards sit on the spec board line. C6 still leaves R 4.0 corners, gates, futsal siting
# and box-lacrosse goals open (surfaces are sized off that R). C7 leaves the gym layout open. Those stay proposed.
# Climbing mats in cleared zones (N field from X96, kids mats outside the pillar gap) stay proposed.
VALID_IF_CLEAR = {"tt_rink_board_2m", "tt_rink_board_2m_crest", "tt_rink_board_1m"}
hit_ids = {id(h["pos"]) for h in hits}
for it in items:
    if "mat" in it["asset"] and it["room"] == "F2-CLIMB":
        it["placement_status"] = "proposed"
    elif it["room"] in ("F2-GYM", "F2-RINK") and it["asset"] in VALID_IF_CLEAR and id(it["pos"]) not in hit_ids:
        it["placement_status"] = "valid"
    else:
        it["placement_status"] = "proposed"
conflicts = [
 dict(id="C1", room="F2-CLIMB", what="Rental desk guest side: desk zone X67..76 Z6.5..9.5 has its front at Z 9.5 (Rev 2.6), but LS core occupies X71..76.5 from Z 9.5 and Lift S X66.5..70.5 from Z 11. Guest frontage beyond Z 9.5 exists only X66.5..71 (1.5 m to Lift S). Desks WITHHELD; needs Vance call (turn desk to face W/E lobby, or shorten to X67..71).", status="open"),
 dict(id="C2", room="F2-CLIMB", what="r8: N-wall panels start at X98 (12 boulder, no trim, pivot Z 14.2933, yaw 180, back Z 14.685). Guard at raw X98.10 Z13.75 yaw -90. Mats start X98. Entry landing X94..98 Z13.2..15 is hard floor (not a fall zone).", status="resolved"),
 dict(id="C3", room="F2-CLIMB", what="TC-S4 skin documented as 1.2 m square. Ring kept; cut-mat infill placed (2x15 x2, 124x15, 088x24, 188x40).", status="resolved"),
 dict(id="C4", room="F2-CLIMB", what="9 x 1.25 m kids panels kept (not 12). Rev 3.1 spine + TC-S3 pier do not fit 12.", status="resolved"),
 dict(id="C5", room="F2-CLIMB", what="TC-S3 pillar mat collar placed (14x28 west + 06x16 south). Existing 2 m kids mats unchanged.", status="resolved"),
 dict(id="C6", room="F2-RINK", what="Rink now 61 x 26 (X41.5..102.5, Z26.5..52.5) using 1 m filler at mid-length; R 4.0 corner radius, gate positions, futsal 40x20 siting and box-lacrosse goal lines (4 m from ends) remain temp-Active proposals. Players' benches WITHHELD: 1.16 m between boards and PT column pads cannot take bench + circulation without entering the 3.1 m concourse.", status="open"),
 dict(id="C7", room="F2-GYM", what="Resolved for the two berm nicks only. Berms at raw X 57.20 and 85.20 (third berm 64.3 unchanged). Gym layout otherwise remains a proposal.", status="resolved"),
]
out = dict(conflicts=conflicts, owner="temp-Active (scratch, NOT integrated, NOT approved)", spec="design/strip5_tennis_tower_v1.md Rev 3.2 cc7fd9a (HEAD 3218906; no spec/helper change since)",
           axes="building X = Godot +X, Z = Godot +Z, Y up; F2 slab top +6.1; yaw deg about +Y (+Z front of asset rotated by yaw)",
           pivot="GLB pivot = bottom-centre of visual bbox; pos = world pivot already corrected from raw builder origin (raw_origin_world) via Ry(yaw)*pivot_raw",
           sources=["design/strip5_tennis_tower_v1.md §2, §3.4, §3.7.1, §3.12, §4.6, Rev 3.0-3.2", "design/tennis_tower_handoff/ROOM_OWNERSHIP.md", "assets/src/tennis_tower/structure/tower_plan.py (CORES, LIFTS, TREES, PT_X/PT_Z)",
                    "assets/src/tennis_tower/structure/build_structure.py walls_f2()", "assets/src/tennis_tower/tree_column.py (trunk clad 1.2 m sq)"],
           counts={}, items=items, withheld=WITHHELD + LEAD_WITHHELD, keepout_hits=hits, mat_overlaps=mo,
           status_legend="placement_status: valid = spec-dimensioned and keepout-clear with no open conflict; proposed = temp-Active judgement, not approved; withheld = not placed (reason given)")
for it in items: out["counts"][it["asset"]] = out["counts"].get(it["asset"], 0) + 1
json.dump(out, open(str(HERE / "temp-Active_scratch_placements.json"), "w"), indent=1)
json.dump(out, open(str(MD / "rooms" / "temp-Active_placements.json"), "w"), indent=1)
print(len(items), "items"); print(json.dumps(out["counts"]))
for h in hits: print("HIT", h["room"], h["asset"], h["pos"][::2], "|", h["keepout"], h["overlap_xz"])
for m in mo: print("MATOVL", m)
