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
