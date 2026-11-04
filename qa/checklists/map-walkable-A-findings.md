# Doc A — Map walkability playtest findings (round 1, main 42ceab7)

Rules: APPEND ONLY to the end of this file. Do NOT read the existing entries before appending; write your own findings blind.
Each finding: `- [tester] [ID] location (x,y,z) | what happened | repro | severity`.
When you're done appending, open Doc B (`map-walkable-B-signoff.md`) and sign it.

---

## MAP-QA-2 — Collision edges & falls (2026-11-03)

Tested commit: `e9fad26` (round 1 pin). Godot 4.7.2 headless, `--fixed-fps 60`. Untracked harness outside the repo (`/tmp/qa2/walk.gd`): loads `preface_playable_area.tscn`, teleports `PlayerBody` to a start point and yaw, then holds `move_forward` (plus `sprint`/`jump` where noted) with `Input.action_press`, recording the path, min Y, and slide collisions. A downward ray grid at 0.5 m on L1 (y 0) and L2 (y 4.2) checked for floor holes. 92 walk probes in all: L2 wing edges, stairwell glass, L2 perimeter on N/S/E/W, four L2 corners, ±10 m column cells, and L1 radials from (0,0,2), (-9,0,0), (9,0,0).

**Counts:** fall-through / unguarded drop 1 (High) · invisible wall over continuous floor 1 (Medium) · holes in floor 0 · walk-through solids 0 · wedge/stuck spots 0 (all four L2 corners and both diagonal wall slides along x=±2.45 slid cleanly to the end) · info 1.

1. **[HIGH] A sprint-jump clears the L2 stairwell glass guard and drops the player about 4 m.** Nodes: `Guard_Glass_14-convcolonly`, `Guard_Glass_16-convcolonly` (guard line z -4.83, top y 5.255, which is 1.05 m above the 4.2 slab). JUMP_VELOCITY 4.8 gives about 1.18 m of apex, so the capsule clears the guard.
   Repro: put the player at (0.0, 4.3, -3.0) facing yaw 0 (-Z). Hold W and Shift, and tap Space. The player clears the guard at about z -4.8, drops into the well, and lands at y 0.06 (out through the sector-4 doorway to (0.0, 0.06, -16.7)). The same move from (-1.2, 4.3, -3.0) clears `Guard_Glass_14` and lands on the flight or mid landing at y 2.46.
   Walking into the glass without jumping holds every time: x -1.2, 0.0, 0.30, 0.38 and 0.45 all stop at z -4.47. The 0.37–0.40 seam before flight 2 is sealed too. Fix: guard at least 1.3 m tall, or an invisible cap collider above the glass.
2. **[MEDIUM] Invisible wall on open L2 floor in the west wing.** `SectorSafetyFloorColliders/L2WestWingSouthGuardrail` (box 6.5×1.25×0.18 at (-10.65, 4.82, -6.55); x -13.9..-7.4) stands in the middle of floor: the ray scan and walk probes show L2 slab out to z -8.55 here.
   Repro: from (-12, 4.3, -6.5) or (-8, 4.3, -6.5), walk -Z. The player stops dead at z -6.11 with nothing visible there. From (-10, 4.3, -8.0), walk +Z and the player stops at z -6.99. The area behind it can be reached by walking around the east end: start at (-6, 4.3, -8) and walk -X along z -8 or -7.2 freely to x -13.55.
   This looks like a leftover from the pre-Rev C gallery (PATH-06). Remove it, or move it to the real edge if one exists.
3. **[INFO] Player hangs mid-air when placed inside a prop collider.** A teleport to (-11.0, 4.4, -4.8) lands inside `Alcove2C_Battery_Expansion_Support/Shelf_Shape`. The player stays at y 4.40 with `is_on_floor()=false`, never falls, and can't walk -X. Only the harness can reach this; normal walking can't. I couldn't test the Seam03 1.1 m rail from this start because of it.

No problems on: L2 east/west wing inner edges (x ±2.45, z -8.5..-1.2: solid wall `RevC_Shell_L2_col`), L2 outer walls (x ±13.55, z +8.55, z -8.55), the ±10 m "hole" cells at z -0.5..0.5 (they are solid columns, blocked at z ±1.35), the whole L1 floor (no ray holes and no falls on any radial), or the walk down flight 2 from (1.2, 4.3, -2.5), which steps smoothly to y 2.46.

## MAP-QA-4 — Exterior & Tram (2026-11-03)

Method: fresh clone of main, Godot 4.7.2 headless (`godot --headless --path godot -s <harness> -- --qa-placement`), harness kept outside the repo. Movement used real `Input.action_press` on move_forward / jump / interact / rfid_pulse through the CharacterBody3D controller; teleports were used only to choose start points. Ray grid: 1 m over x -17..17, z -44..-9 (plaza/promenade) and x -22..22, z -9..8 (planting strips).

1. **HIGH: you can climb promenade guardrails and leave bounds.** Nodes: `SectorArchitecture/SectorSafetyFloorColliders` → PromenadeSouthGuardrail (z -45), PromenadeWestGuardrail (x -18), PromenadeEastGuardrail (x +18). All are 1.25 m tall and 0.24 m thick.
   - Repro: start at (0, 0.3, -42) facing -Z, hold W, tap jump every 20 frames. Player reaches y=2.27 (standing on top of the rail and jumping again) and lands at (0, -0.88, -51.4), outside the deck. Same at x=-15 / x=+15, z=-30 facing out → ends at x=∓24.4, y=-0.88. Later the out-of-bounds reset sends the player back to spawn (-9.4, 4.08, 6.1).
   - Walking without jumping is blocked correctly (stops at z -44.53).
   - Expected: the rail cannot be stood on (taller collider or a no-stand cap like TramRoofNoStand). Actual: the rail top can be stood on and the player escapes.
2. **MEDIUM: DOOR_SECTOR4_EXIT does not open from E or RFID pulse.** Node: `InteractivePropsAndPickups/SectorRFIDForceFieldDoors/DOOR_SECTOR4_EXIT` (root (0,0,-9), FieldCollider top y=2.45, hub shift 0.31 at seat).
   - Repro: stand at (0, 0.05, -10.2) facing +Z, press interact (or rfid_pulse), wait 90 frames, hold W. Player stops at z -9.45. From the atrium side, (0,0,-7.5) facing -Z stops at z -8.54. Walking straight in does not pass either.
   - Expected: interacting opens the exit field, or else the door is clearly locked. Actual: the field stays solid both ways. This may be an intended RFID gate, so please confirm.
3. **LOW: dead-foliage planting strip can be hopped, reaching x ≈ -23.5.** Node: `ExteriorPlacements_v1_3/Ext_49_ext_ts4_dead_foliage_1004` at (-16.6, 0.17, 0.0), collider top y=0.68.
   - Repro: start at (-14.5, 0.3, 0.0) facing -X, hold W plus jump. Player crosses the strip and ends at (-23.5, 0.34, -0.17).
   - The neighbouring hydro planters 1006/1007 (same top, 0.68) block correctly at x -13.55. Please confirm x < -22 is meant to be walkable. If not, the strip needs a bounds blocker.
4. **INFO (pass): tram shelter and tram car roofs cannot be stood on.** `Ext_15_ext_tram_shelter_0` roof collider is y=3.13. Jumps from north, south and west reach at most y 1.57, so the roof can't be reached. `Ext_19_ext_maglev_car_body_17/18` roofs are y 3.58–3.83 and have TramRoofNoStand caps. Platform kerbs `Ext_16_*` (y≈0.31) step up cleanly.
5. **INFO (pass): no ground holes.** 0 ray misses across the plaza/promenade grid. Deck is at y≈0.0–0.06 and there are no sunk or floating ground tiles. 13 exterior visuals have no collider, and all of them are flat decals or litter (`Ext_47_ext_desire_path_decal_*`, `Ext_49_ext_ts4_wear_decal_1005`, `Ext_50_ext_litter_drift_*`, `Ext_51_ext_track_scuff_guideway_*`), so that is expected.

## MAP-QA-3 — Stairs, Ramps & Vertical

- Date: 2026-11-03 · Round 1 · tested against main @ e9fad26 · Godot 4.7 headless
- Method: real simulated input only (InputEventKey W/Shift/Space/E + InputEventMouseMotion yaw via the scene's own `_qa_key`/`_qa_mouse`/`_qa_egress_steer`); throwaway SceneTree drivers in /tmp (outside repo), run with `-- --qa-placement`. No position writes. No repo .gd/.tscn/.py edited.
- Built-in modes: `--qa-stairs` → **PASS** (12/12 waypoints, `DONE failures=0`); `--qa-egress` → **PASS** (18/18 waypoints, `DONE failures=0`). Note: on a fresh clone both fail to parse (`TroubleshootSimpleUI` class not found) until `godot --headless --import` has built the class cache once.

| # | Location | Repro | Severity | Result |
|---|----------|-------|----------|--------|
| 1 | Stair core head, L2 (1.15, 0.0) → F1 | From the stair head hold W toward F1 foot (1.15,-8.15) and tap Space every ~0.3 s. First jump carries the player sideways east to x≈3.65 against `RevC_Shell_L2_col` and pins them there ~3 s; then the player crosses the whole F1 flight airborne at y≈4.1–5.3 (L2 height, flight surface is 2.5–4.1) and only drops to the landing at the end. Walk time 92 frames vs 298 with jumps. Looks like a jump-height surface/collider over the F1 stairwell or air-jump chaining. | Medium | FAIL |
| 2 | Stair core F1/F2, jump-down/jump-up | Repeated jumps descending F2, ascending F2 and F1: all arrive and settle on floor in Y band (L1 y=0.00, landing y=2.465, L2 y=4.08). No fall-through, no snag. | — | PASS |
| 3 | Mid-flight F2 (-1.15,-5.0) | Stop on the ramp (y=1.048, on_floor), 180° mouse turn, walk back down: stays on floor, no slide, reaches L1. | — | PASS |
| 4 | Landings (±1.15,-8.15) | Standing jump on landing: lands dy=-0.001, on_floor. Turning across landing between flights: PASS both directions. | — | PASS |
| 5 | Stair core F1 sprint | Shift+W down F1 and up F1: arrives, settles on floor (2.465 / 4.080). | — | PASS |
| 6 | Up F1 after jumping | Arrival at L2 airborne (y=5.23); needs ~23 frames to land. Normal jump arc, not a bug. | Info | PASS |
| 7 | Exterior kerb ramp `ext_kerb_ramp` → tram platform (10–12,-16.5) | Walk up, walk down, jump-spam up: up and jump reach platform y=0.351 on floor. Walking down, the player is still at y≈0.31 at (9.35,-16.49); the ramp's rise sits in the last ~0.5 m toward the paving, so it reads as a short steep kerb, not a gentle ramp. | Low | PASS (note) |
| 8 | Egress route exterior paving (0..8.9, -9.8..-15.9) | Small paving step (0.00→0.05) passes, no snag. | — | PASS |
| 9 | Coverage gap: `ext_curb_segment_*` row at z≈19.35 (x -12..-8) and tram platform kerb front edge (z=-17.55) | Not driven this round (outside reachable route in the 60 s budget). | Info | NOT TESTED |

Totals: 0 Critical, 0 High, 1 Medium, 1 Low, 3 Info (incl. 1 coverage gap); 7 PASS rows, 1 FAIL.

## MAP-QA-5 — Freeform player playtest (2026-11-03)

Tested SHA: main e9fad26 (fresh clone). Godot 4.7.2 headless, scene `preface_playable_area.tscn` booted with `-- --qa-placement` (passive mode, spawn Apt 201 (-9.35,4.25,6.20)). Input via a throwaway driver in /tmp (not in repo): `Input.action_press` for move_forward/sprint/jump, and `InputEventKey` (E/F) via `Input.parse_input_event` for interact/pulse. Position traces every 0.25–0.5 s.

**F1 — HIGH — Upper-floor north opening lets player vault and drop outside the building, bypassing the locked SECTOR-4 exit (soft-lock).**
- Location: 2F corridor centre, north opening at x=0. Player stops at (0.01, 4.08, -4.47) against a ~1.2 m blocker (rail/guard).
- What happens: one jump clears it (apex y≈5.29 at z -4.85), player falls through (0,3.30,-8.20) → (0,2.75,-9.59) → lands on exterior promenade (0, 0.06, -12.19) in ~1 s. DOOR_SECTOR4_EXIT still reports closed. Walking back south stops at z=-9.45 (closed field / shell); the exit hub is on the inside (1.45,0,-8.90), so the player cannot get back in.
- Repro: spawn → walk to (-4.0,1.7), face hub (-4.14,0.797), E → walk (-3,1.6)→(-3,0)→(0,0)→ hold forward toward (0,-8.5); when stuck at z -4.47 press jump while holding forward.
- Variant: jumping at the same spot while steering west lands at (-1.69, 0.05, -9.45) on ground after drop from y≈2.4.

**F2 — LOW — Small bumps on exterior promenade strip at z≈-9.45.** At x≈-3.1/-3.4 and x≈+3.0 player pops to y 0.13–0.19 (floor=false briefly) walking along z -9.45; at (0,·,-18.5) y 0.20. Also when sprinting into the wall at z -9.45 near x -3.9..+2.6 the player hangs (STUCK) repeatedly until jumping. Repro: from F1 landing, walk to (-8,-9.4) then (8,-9.4).

**F3 — INFO (pass) — Doors / walls behave.** APT201 and ALCOVE2C open with E at hub and are passable; closed APT202 field holds (player stops z=0.30 sprinting at it from (3,0)). 2F corridor end walls at x=±9.55 and side walls z=±0.45 solid; jumps against them return to floor 4.08, no clipping. Apt 201 interior bounds x[-13.55,-0.45] z[1.35,8.55] solid incl. sprint/bunnyhop into corners.

**F4 — LOW — Apt 201 SE corner perch.** Bunnyhop into (-0.45, ·, 1.35) leaves player resting at y≈5.2 (≈1.15 m above floor) for several seconds while still pushing into corner (slowly sinks 5.25→5.16). Feels like standing on an invisible ledge/furniture top. Repro: from spawn sprint to (-0.45,1.35) holding jump.

**F5 — LOW — Snags at hub approach.** Standing at (-3.99,4.08,1.69) heading for hub/door, and at (-3.38,4.08,-0.45) by the Alcove 2C jamb, the player gets stuck for 1–1.5 s until a jump/side-step. Repro: route in F1.

## MAP-QA-1 — Traversal sweep — 2026-11-03

- Build: FinalFracture/Aegis-7 main @ e9fad26, Godot 4.7.2 headless (`--fixed-fps 60`), scene `res://scenes/preface/preface_playable_area.tscn` (main scene; residential sector). Harness at /workspace/qa-harness/sweep.gd (outside the repo; no repo files changed).
- Input: the player was moved only with `Input.action_press` (analog move_* + sprint, look_left/look_right to face travel direction) and injected `InputEventKey` E taps when stalled at doors (forcefield doors open this way). Movement was never done by teleport. The one exception: before each attempt the player is reset to SPAWN_POS (-9.35, 4.25, 6.20).
- Routing: for each cell, the harness walked to the target from spawn, and then from checkpoints along the game's own `--qa-egress` route (L2 corridor (1.15,0), L1 stair foot (1.15,-2.0), plaza (12.3,-16.7)). Between those points it followed the baked navmesh path. A cell is OK when the player reaches it within 0.6 m horizontally and 1.3 m vertically. A cell is "not reached" after 160 frames with no progress.
- Stuck test: at each reached cell the harness held each of the four move keys for 18 frames. Stuck = max displacement < 0.15 m. Fall-through = y ends > 2 m below the cell.
- Grid: 2 m XZ cells × 1.5 m Y bands, one cell per navmesh-covered bin, 482 cells total. Region labels come from coordinates and are approximate.

### Coverage
| Region | Cells | Reached | Not reached |
|---|---|---|---|
| Apartments | 44 | 22 | 22 |
| ExteriorPlaza | 266 | 187 | 79 |
| L1 | 118 | 44 | 74 |
| L2 | 36 | 7 | 29 |
| Upper(y>6.5) | 18 | 0 | 18 |

Total reached: 260/482. Stuck spots: **0**. Fall-through: **0**. Every reached cell allowed movement back out (all esc > 0.15 m).

### Not-reached cells (x, y, z) with the last collider hit

```
Apartments 22 [('RevC_Shell_L1/RevC_Shell_L1_col', 22)]
    (5.00,4.40,3.00); (6.99,4.40,1.58); (7.00,4.40,3.20); (7.00,4.40,5.00); (7.00,4.40,7.00); (7.00,4.40,8.50); (9.00,4.40,1.00); (9.05,4.40,3.10); (9.00,4.40,5.00); (9.00,4.40,7.00); (9.00,4.40,8.50); (11.00,4.40,1.00); (11.00,4.40,3.10); (11.00,4.40,5.00); (11.25,4.40,6.50); (11.00,4.40,8.50); (11.00,5.25,7.00); (13.00,4.40,1.00); (13.00,4.40,3.10); (13.00,4.40,7.00); (13.00,4.40,8.50); (13.00,5.05,5.00)
ExteriorPlaza 79 [('RevC_Shell_L2/RevC_Shell_L2_col', 22), ('Ext_19_ext_maglev_car_body_18/ExtCollision', 12), ('Ext_19_ext_maglev_car_body_17/ExtCollision', 10), ('Ext_17_ext_maglev_guideway_7/ExtCollision', 8), ('RevC_Shell_L1/RevC_Shell_L1_col', 5), ('Ext_17_ext_maglev_guideway_15/ExtCollision', 3)]
    (-19.00,0.26,-19.00); (-19.00,0.25,-21.00); (-19.00,0.22,-27.00); (-21.00,0.27,-19.01); (-21.00,0.25,-21.00); (-23.00,0.26,-19.00); (-23.00,0.25,-21.00); (-23.00,0.23,-25.00); (-23.00,0.21,-27.00); (-25.00,0.25,-19.00); (-25.00,0.25,-21.00); (-27.00,0.25,-19.00); (-27.00,0.25,-21.00); (-29.00,0.25,-19.00); (-29.00,0.25,-21.00); (-31.00,0.25,-19.00); (-35.00,0.25,-19.00); (-35.00,0.25,-21.00); (-37.00,0.25,-19.00); (-37.00,0.25,-21.00); (-37.00,0.21,-23.00); (-37.00,0.22,-27.00); (-39.00,0.25,-19.00); (-39.00,0.25,-21.00); (-41.00,0.25,-19.00); (-41.00,0.25,-21.00); (-5.00,0.20,-9.30); (-7.00,0.20,-9.30); (-9.00,0.20,-9.30); (-13.00,0.25,-21.00); (-13.04,0.25,-9.30); (-15.00,0.25,-19.00); (-15.00,0.25,-21.00); (-15.00,0.23,-25.00); (-15.00,0.21,-33.00); (-17.00,0.25,-21.00); (21.00,0.80,-19.40); (21.00,0.80,-20.35); (23.00,0.80,-19.00); (23.00,0.80,-20.87); (23.00,0.20,-27.00); (25.00,0.80,-19.35); (25.00,0.80,-20.40); (27.50,0.29,-19.00); (27.13,0.25,-21.35); (29.00,0.25,-19.00); (29.00,0.25,-21.00); (35.00,0.25,-19.00); (35.00,0.25,-21.00); (37.00,0.25,-19.00); (37.00,0.25,-21.00); (37.00,0.23,-23.00); (37.00,0.22,-27.00); (39.00,0.25,-19.00); (39.00,0.25,-21.00); (41.00,0.25,-19.00); (41.00,0.25,-21.00); (5.00,0.80,-19.35); (5.00,0.80,-20.40); (5.00,0.21,-23.00); (5.00,0.22,-39.00); (7.00,0.80,-19.00); (7.00,0.80,-20.87); (7.00,0.20,-9.30); (9.04,0.80,-19.40); (9.00,0.80,-20.35); (9.00,0.20,-9.30); (11.00,0.80,-19.00); (11.00,0.80,-20.86); (11.00,0.20,-9.30); (12.99,0.80,-19.38); (12.99,0.80,-20.37); (13.03,0.24,-9.30); (14.45,0.80,-20.85); (17.00,0.80,-19.40); (17.00,0.80,-20.35); (19.00,0.80,-19.00); (19.00,0.80,-20.86); (19.00,0.22,-27.00)
L1 74 [('RevC_Shell_L1/RevC_Shell_L1_col', 55), ('StairSetSwitchback/Flight1_Understair_Closure-colonly', 11), ('Ext_44_ext_paving_promenade_535/ExtCollision', 4), ('Ext_41_ext_curb_segment_894mm_118/ExtCollision', 2), ('DOOR_RM1A/PortalJambCollider_R', 1), ('ExtGroundNorth/ExtGroundBody', 1)]
    (-1.00,0.30,-7.00); (-1.00,0.30,3.00); (-1.00,0.30,5.00); (-1.00,0.30,7.00); (-2.95,0.30,-0.95); (-3.35,0.70,-2.65); (-3.00,0.30,-5.00); (-3.00,0.30,-7.00); (-3.00,0.20,9.35); (-5.00,0.30,-0.80); (-5.00,0.70,-2.65); (-5.00,0.30,-5.00); (-5.00,0.30,-7.00); (-5.00,0.30,3.20); (-5.00,0.30,5.00); (-5.00,0.30,7.00); (-5.00,0.20,9.35); (-7.00,0.30,-1.00); (-7.00,0.30,-5.00); (-7.00,0.30,3.20); (-7.00,0.30,5.00); (-6.55,1.15,6.90); (-7.00,0.20,9.35); (-7.60,1.65,7.15); (-9.00,0.30,5.00); (-9.00,0.30,6.65); (-9.00,0.20,9.35); (-9.00,1.65,7.15); (-11.00,0.30,-1.00); (-11.00,0.30,-3.00); (-11.00,0.30,-5.00); (-11.00,0.30,3.20); (-11.45,0.75,5.00); (-11.00,0.30,6.65); (-11.00,0.20,9.35); (-11.00,1.65,7.15); (-13.00,0.30,-1.00); (-13.00,0.30,-5.00); (-13.00,0.30,-7.00); (-13.00,0.30,1.00); (-13.00,0.30,3.00); (-13.00,0.30,5.00); (-13.00,0.30,7.00); (1.00,0.30,3.20); (1.00,0.30,5.00); (1.00,0.30,7.00); (3.30,0.70,-2.65); (3.00,0.30,-5.00); (3.00,0.30,5.00); (3.00,0.40,6.99); (5.00,0.70,-2.65); (5.00,0.30,-7.00); (4.99,0.30,3.29); (5.00,0.30,5.00); (4.95,0.45,6.95); (7.00,0.30,-3.00); (7.00,0.30,-5.00); (7.00,0.30,-7.00); (7.00,0.30,3.20); (7.00,0.30,5.00); (9.00,0.30,-1.00); (8.90,0.30,-7.00); (9.01,0.20,9.39); (11.00,0.30,-1.00); (11.00,0.30,-3.00); (11.00,0.93,-6.87); (11.00,0.30,1.00); (11.00,0.20,9.36); (11.00,2.27,-5.09); (13.00,0.30,-1.00); (13.00,0.30,-5.00); (13.00,0.30,-7.00); (13.00,0.30,1.00); (12.99,0.20,9.38)
L2 29 [('RevC_Shell_L1/RevC_Shell_L1_col', 23), ('Ext_44_ext_paving_promenade_535/ExtCollision', 2), ('Ext_15_ext_tram_shelter_0/ExtCollision', 2), ('Ext_0_ext_platform_infill_952/ExtCollision', 2)]
    (-9.00,4.40,-1.00); (-9.00,4.40,-3.00); (-9.00,4.40,-5.00); (-9.00,4.40,-6.20); (-11.00,4.40,-1.00); (-11.00,4.40,-4.45); (-11.00,4.40,-6.20); (-11.00,5.20,-5.00); (-13.00,4.40,-1.00); (-13.00,4.40,-3.00); (-13.00,4.40,-5.00); (-13.00,4.40,-6.20); (1.00,4.40,3.00); (1.00,4.40,5.00); (1.00,4.40,7.00); (1.00,4.40,8.50); (3.00,4.40,1.55); (3.00,4.40,7.00); (3.00,4.40,8.50); (9.00,4.40,-1.00); (9.55,4.05,-2.73); (11.00,4.41,-1.00); (11.00,4.07,-2.70); (13.00,4.40,-1.00); (13.00,4.40,-2.10); (13.00,3.20,-15.50); (13.00,3.20,-16.35); (15.00,3.20,-15.50); (15.00,3.20,-16.35)
Upper(y>6.5) 18 [('RevC_Shell_L1/RevC_Shell_L1_col', 15), ('Ext_41_ext_curb_segment_894mm_118/ExtCollision', 2), ('Ext_44_ext_paving_promenade_535/ExtCollision', 1)]
    (-3.00,8.95,-8.80); (-3.00,8.95,3.00); (-7.00,8.95,-7.00); (-9.00,8.95,-1.00); (-9.00,8.95,-8.80); (-9.00,8.95,1.00); (-9.00,8.95,3.00); (-11.00,8.95,-5.00); (-11.00,8.95,7.00); (3.00,8.95,-7.00); (3.00,8.95,7.00); (7.00,8.95,-7.00); (9.00,8.95,-1.00); (9.00,8.95,-8.80); (9.00,8.95,1.00); (9.00,8.95,3.00); (11.00,8.95,-5.00); (11.00,8.95,7.00)
```

### Notes / likely causes (please triage; some may be harness limitations)
- The navmesh path from spawn runs straight through the RevC_Shell_L2 wall at about (0, 4.1, 1.7) on L2. The player is blocked there by `RevC_Shell_L2_col`. The real route is through the DOOR_APT201 forcefield (open with E), then (1.15, 0) and the stairs. **The navmesh does not match collision here.**
- Most not-reached L1, L2 and apartment cells end on `RevC_Shell_L1_col` / `RevC_Shell_L2_col`. These are likely closed side rooms or apartments (DOOR_RM1A/RM1B/APT202/ALCOVE2C). It is also possible that the nav path cuts through walls the way it does above. The harness only tapped E when stalled, so a door that needs a different approach angle could explain some of these.
- 11 L1 cells under the stair end on `StairSetSwitchback/Flight1_Understair_Closure-colonly`. The navmesh covers space that collision closes off.
- Exterior plaza: cells at z ≈ -19…-21 and y≈0.8 are blocked by the maglev car body and guideway colliders (`Ext_19_*`, `Ext_17_*`). The navmesh is baked over or under the maglev, and the player can't walk there.
- The plaza cells at z = -9.3 (x -13…13) end on `RevC_Shell_L2_col`, which suggests the navmesh hugs the facade outside the exit.
- The 18 cells at y = 8.95 are navmesh on the roof or upper slab. No route reaches them; they may not be intended as walkable.
- Scene check: the repo has no separately named L1/L2/apartment/plaza scenes. All four areas are in `preface_playable_area.tscn` (built by `preface_playable_area.gd`, exterior = `Sector4_Promenade_ExteriorPlaza`). `preface_playable_residential_sector.tscn` exists but was not swept.

