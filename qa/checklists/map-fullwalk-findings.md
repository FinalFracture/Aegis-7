# Doc A — Map full-walk playtest findings (round 4, main 2680651)

Rules: APPEND ONLY to the end of this file. Do NOT read the existing entries before appending; write your own findings blind.
Each finding: `- [tester] [ID] location (x,y,z) | what happened | repro | severity`.
When you're done appending, open Doc B (`map-fullwalk-signoff.md`) and sign it.

---

## MAP-QA-3 — Stairs, Ramps & Vertical

- Date: 2026-11-03 · Round 4 · tested against main @ b15a245 · Godot 4.7 headless, fresh clone, `godot --headless --import` run once first
- Method: real simulated input only. All keys (W/Shift/Space, and E for doors) are real InputEventKey events sent through Input.parse_input_event (the scene's `_qa_key`), never Input.action_press. Mouse yaw uses InputEventMouseMotion. Long outdoor legs follow NavigationServer3D path points as steering targets. Throwaway SceneTree drivers in /tmp, outside the repo, run with `-- --qa-placement`. No position writes and no repo .gd/.tscn/.py edits.
- Built-in modes: `--qa-stairs` **PASS** (`DONE failures=0`); `--qa-egress` **PASS** (`DONE failures=0`).

| # | Location | Repro | Severity | Result |
|---|----------|-------|----------|--------|
| 1 | Stair core head L2 (1.15, 0.0) → F1 | (Round 3 Medium recheck) Hold W toward the F1 foot (1.15,-8.15) and tap Space every ~0.3 s. Unchanged, frame-for-frame identical to R1–R3: the player is thrown east to x≈3.65, pinned on `RevC_Shell_L2_col` ~3 s, then crosses all of F1 airborne at y≈4.1–5.3 (L2 height) before dropping onto the landing (y 2.465). 298 frames vs ~92 walking. | Medium | FAIL (not fixed) |
| 2 | Tram kerb ramp top edge ≈ (9.4, -15.5) | (Round 3 Medium recheck) From the platform (12,-16.7) walk W/NW toward the paving (7.5,-15.0). Unchanged: y goes 0.351→0.304, then the player stops dead at (9.41,-15.47), on the floor with W held, for the rest of the 120-frame window (10 consecutive samples). Never reaches the paving (0.05). Walking up along the egress line still works. | Medium | FAIL (not fixed) |
| 3 | Stair core F1/F2 jump sweep | Jump-spam down F1/F2 and up F2/F1: all settle in band (landing 2.465, L1 0.00, L2 4.08). | — | PASS |
| 4 | Mid-flight F2 (-1.15,-5.0) | Stop on the ramp (y=1.048, on floor), turn 180° with the mouse, walk down to L1. | — | PASS |
| 5 | Landings (±1.15,-8.15) | Standing jump dy=-0.001; crossing both ways. | — | PASS |
| 6 | F1 sprint | Shift+W down/up F1 settles at 2.465 / 4.080. | — | PASS |
| 7 | Tram platform kerb front edge (z=-17.55) | The surface continues at y 0.35 past the kerb line with no drop; walking back onto the platform is clean. | Info | PASS |
| 8 | Curb row `ext_curb_segment_21..23` (z≈19.35, x≈-10) | Walk N over it, walk S back, jump-cross N: clean (curb top 0.15; jump lands on top at 0.151). | — | PASS |
| 9 | Egress route exterior paving + `--qa-egress` path | All in band. | — | PASS |

Totals: 0 Critical, 0 High, 2 Medium, 0 Low, 1 Info; 7 PASS, 2 FAIL.

## MAP-QA-2 — Round 4 (b15a245)

Tested commit: `b15a245` (fresh clone; `godot --headless --import` run once first). Godot 4.7.2 headless, `--fixed-fps 60`, one run at a time. The untracked harness is outside the repo, and all input is real `InputEventKey` events sent through `Input.parse_input_event`: W, Shift, Space, E and F. The harness only teleports the player to each start point and sets yaw before a probe. The only script change since round 3 is the exterior `ExtGroundSouth*Bound` boxes, and every interior result matches round 3. The 0.5 m down-ray hole grid on L1 and L2 is identical to rounds 1–3. Coverage: 114 walk probes and 54 door steps (9 per door × 6).

**Counts:** falls / unguarded drops 0 · invisible walls over continuous floor 0 · holes 0 · walk-through solids 0 · wedge/stuck from normal play 0 · low 1 (still open) · info 1 (still open).

**Re-checks**
1. **[LOW] Alcove 2C rail sprint-jump: STILL REPRODUCES**, with the same result as round 3. Nodes: `Seam03_Alcove2C_EastRail` (x -10.30) and `Seam03_Alcove2C_Rail` (x -10.18), 1.1 m tall.
   - Out of the alcove: start at (-12.5, 4.3, -4.2) or (-12.5, 4.3, -5.4) at yaw -90, hold W and Shift, then hold Space. The player clears both rails and stops at x -2.45.
   - Into the alcove: start at (-8.5, 4.3, -4.2 / -5.4) at yaw 90, same keys. The player clears both rails and stops at x -13.55.
   - Plain walking is blocked at x -10.69, and the floor is level on both sides, so there's no fall.
2. **[INFO] Shelf hang: STILL REPRODUCES.** After a teleport to (-11.0, 4.4, -4.8), between `Alcove2C_Battery_Expansion_Support/Shelf_Shape` and `Alcove2C_SuperWire_Expansion_Support/Shelf_Shape`, the player hangs at y 4.40 with `is_on_floor()=false`. Holding W does nothing in either direction. Only a teleport gets you there; normal walking slides past the shelves.
3. **Doors, all 6 (APT201, APT202, ALCOVE2C, RM1A, RM1B, SECTOR4_EXIT): PASS.**
   - Locked: walking stops 0.45 m short of the field.
   - New this round: tapping F (RFID pulse) at the hub does not open the door, and the walk stays blocked, which matches the QA-HUB-01 design.
   - E at the hub opens the door, and the player walks through.
   - E pressed while standing in the doorway sets `close_pending`/`close_blocker=PlayerBody`. The door holds open, the player isn't trapped, and it closes once they leave.
   - Once it closes, a walk and a sprint-jump are both blocked again.

Full edge sweep: every probe ends where it did in round 3, within ±0.01 m. Covered: the L2 inner wing edges at x ±2.45, the outer walls at x ±13.55 and z ±8.55, the old west-wing guardrail line (still clear), and the stairwell glass, where walking stops at z -4.42 and all six sprint-jumps are stopped by `StairwellHeadGlassCap`. Also covered: the gap before flight 2 (sealed), the ±10 m columns, all four L2 corners and the diagonal wall slides (no wedging), flight 2 (smooth descent to y 2.46), and the L1 radials (no falls). The new `ExtGroundSouth*Bound` boxes are exterior, MAP-QA-4's area, so I didn't test them here.

## MAP-QA-5 — Freeform player playtest round 4 (main b15a245, 2026-11-03)

Fresh clone at b15a245, `godot --headless --import` once (rc 0). Godot 4.7.2 headless, `preface_playable_area.tscn` with `-- --qa-placement` (normal Apt 201 spawn (-9.35,4.25,6.20)). Movement via `Input.action_press`; E/F as real `InputEventKey` press+release via `Input.parse_input_event`. Driver scripts in /tmp, not in repo. Route: Apt 201 → 2F corridor (incl. closed Apt 202) → switchback stairs → ground → SECTOR-4 exit (E at hub) → promenade both ways; Apt 201 corner/wall sprint+jump; north-railing jump. All coordinates match round 3 — no change observed.

- **Ground-floor blocker (1.55, 0.00, -0.99) — STILL PRESENT (MEDIUM).** East along z -1.0 from stair foot stops dead at x 1.55; northward needs a jump (apex ~1.2 m) to clear it. Repro: stairs down → (-1.55,-1.0) → forward toward (3.5,-1.0), then (3.5,-7.9).
- **Apt 201 west-wall snag (-13.55, 4.08, 5.82) — STILL PRESENT (LOW).** Sprinting south along west wall from (-13.3,8.4): 4 samples mv=0.00 with input held until a jump clears a ~1.2 m obstacle. Repro: spawn → sprint (-13.5,8.5) → sprint toward (-13.5,1.4).
- **Exit-panel short stop (1.55, 0.00, -7.86) — STILL PRESENT (LOW).** Blocked ~1 m short of hub (1.45,0,-8.90); real E opens SECTOR4_EXIT from there; exit walkable to (0.07,0.06,-11.77).
- **Promenade bumps — STILL PRESENT (LOW).** y 0.15 at (-5.62,-10.35)/(-6.86,-9.96); sprinting wall z≈-9.5: y 0.20 at x -2.94 and x +3.07.
- **Apt 201 door snag (-3.99, 4.08, 1.69) — STILL PRESENT (LOW).** ~1 s stop approaching the hub; real E opens APT201; doorway walkable.
- **Closed Apt 202 door — PASS (solid).** Sprinting from (2.70,4.08,0) at the closed field stops at (3.25,4.08,0.35) for 2 s (field at z 0.8); a jump there tops out y 5.28 and lands back at z 0.30 — no pass-through. APT202 stays closed.
- **Regression — PASS.** North-railing jump at (0,4.08,-4.43) still contained; stairs 4.08 → 2.46 → 0.00 clean; Apt 201 SE corner ledge not reproduced.

## MAP-QA-4 — Exterior & Tram (Round 4, 2026-11-03)

Main b15a245, fresh clone, `godot --headless --path godot --import` clean, harness /workspace/mapqa4-harness/r4.gd + r4d.gd run with `--qa-placement`. Movement via move_forward/jump actions on the player controller; E via real InputEventKey press+release (Input.parse_input_event).

### Findings
- **HIGH — south ends of map-edge walls x ±49 (still open from R3).** Repro: place (-44, 0.3, -29.5) yaw 90 (or (44, 0.3, -29.5) yaw -90), hold forward with jumps. Expected: blocked by wall/south bound. Actual: falls to y -7.87 and respawns at (-11.88, 4.08, 1.44). The new south bound at z -28.1 does not close the gap below z ≈ -28 outside the guardrails.
- **MEDIUM — south bound z -28.1 can be jumped over near the centre (|x| ≈ 10).** Repro: place (±10, 0.3, -24) yaw 0, forward + jump every 15 frames (also 30° diagonal). Expected: blocked at ≈ -25.4 like walking. Actual: crosses bound, lands at z -36.9 (x 10 → -36.91; diag → (2.68, -36.68) / (-17.32, -36.68)). Walking is blocked at -25.42; at x ±30/±45 jumping is blocked at -27.65. Not off-map (lands on lower promenade), but bound is climbable.
- **MEDIUM — west/east promenade guardrail mid-air hang (still open).** Repro: place (±15, 0.3, -30) yaw ±90, forward + jump. Actual: stuck at (±17.53, 0.72, -30), is_on_floor=false, ~77 stuck frames. South rail is clean (stops at z -44.53 on floor).
- **LOW — dead-foliage strip Ext_49_ext_ts4_dead_foliage_1004 hop (still open).** Repro: (-14.5, 0.3, 0) yaw 90, forward + jump. Actual: reaches x -24.37 on floor.
- **LOW — curb seams at x -16.95, z -5 / 0 / 5 (still open).** Repro: (-15.5, 0.3, z) yaw 90 walk 45 frames. Expected: step over. Actual: moves only 0.75 m, 21 stuck frames at x -16.25; reverse from (-18.4, z) yaw -90 stalls at -17.15 (26 stuck frames).

### Passed
- Map-edge walls x ±49 (z -27.5, -20, 0, 20, 40) and z 42.6 (x -45…45): walk, jump, diagonal all blocked at x ±48.65 / z 42.15; no escape. Corners NW/NE/SW/SE walk + jump blocked. Re-check showed no mid-air hang at walls (player lands on floor within 30 frames) — NW/NE corner hang from R3 FIXED.
- DOOR_SECTOR4_EXIT opens with real E from south and from north (fresh run); walk-through both sides OK.
- Curb x -7.0 at z≈19.35 steps up cleanly; south promenade rail jump blocked.

### Round 3 status
- Fixed: NW/NE wall corner hang.
- Still open: wall south-end fall-off (High), W/E guardrail hang at y 0.72, dead-foliage hop to x -24.37, curb seams x -16.95.
- Confirmed: DOOR_SECTOR4_EXIT still opens.

## MAP-QA-1 Round 4 — Traversal sweep — 2026-11-03

- Build: FinalFracture/Aegis-7 main @ b15a245, fresh clone, `godot --headless --import` run first, Godot 4.7.2 headless `--fixed-fps 60`. Scene: preface_playable_area.tscn.
- Method: same as Round 3. Same harness, same 482-cell grid, same thresholds. Movement uses `Input.action_press`. E and F are sent only as real `InputEventKey` press/release events through `Input.parse_input_event`. Batches ran one at a time.

### Coverage (Round 4; Round 3 in brackets)
| Region | Cells | Reached | Not reached |
|---|---|---|---|
| L1 | 118 | 45 (45) | 73 (73) |
| L2 | 36 | 7 (7) | 29 (29) |
| Apartments | 44 | 22 (22) | 22 (22) |
| Exterior plaza | 266 | 204 (205) | 62 (61) |
| Upper slab y≈8.95 | 18 | 0 (0) | 18 (18) |

Total reached: 278/482 (Round 3: 279). Stuck spots: **0**. Fall-through: **0**.

### Change vs Round 3
```
NEWLY_REACHED 0 
NEWLY_UNREACHED 1 ExteriorPlaza(9.00,0.20,-9.30) blk=['SectorArchitecture', 'SectorSafetyFloorColliders']
```
Only one cell flipped. Every other cell had the same result as Round 3.

### Not-reached cells (x, y, z) and the last collider hit
```
UNREACHABLE by region & blocker
Apartments 22 [('RevC_Shell_L1/RevC_Shell_L1_col', 19), ('SectorArchitecture/SectorSafetyFloorColliders', 3)]
    (5.00,4.40,3.00); (6.99,4.40,1.58); (7.00,4.40,3.20); (7.00,4.40,5.00); (7.00,4.40,7.00); (7.00,4.40,8.50); (9.00,4.40,1.00); (9.00,4.40,5.00); (9.00,4.40,7.00); (9.00,4.40,8.50); (9.05,4.40,3.10); (11.00,4.40,1.00); (11.00,4.40,3.10); (11.00,4.40,5.00); (11.00,5.25,7.00); (11.00,4.40,8.50); (11.25,4.40,6.50); (13.00,4.40,1.00); (13.00,4.40,3.10); (13.00,5.05,5.00); (13.00,4.40,7.00); (13.00,4.40,8.50)
ExteriorPlaza 62 [('Ext_19_ext_maglev_car_body_18/ExtCollision', 12), ('Ext_19_ext_maglev_car_body_17/ExtCollision', 10), ('Ext_17_ext_maglev_guideway_7/ExtCollision', 9), ('RevC_Shell_L1/RevC_Shell_L1_col', 4), ('Ext_44_ext_paving_promenade_387/ExtCollision', 3), ('Ext_44_ext_paving_promenade_510/ExtCollision', 3)]
    (-35.00,0.25,-19.00); (-31.00,0.25,-19.00); (-29.00,0.25,-21.00); (-29.00,0.25,-19.00); (-27.00,0.25,-21.00); (-27.00,0.25,-19.00); (-25.00,0.25,-21.00); (-25.00,0.25,-19.00); (-23.00,0.21,-27.00); (-23.00,0.23,-25.00); (-23.00,0.25,-21.00); (-23.00,0.26,-19.00); (-21.00,0.25,-21.00); (-21.00,0.27,-19.01); (-19.00,0.22,-27.00); (-19.00,0.25,-21.00); (-19.00,0.26,-19.00); (-17.00,0.25,-21.00); (-17.00,0.25,-19.00); (-15.00,0.21,-33.00); (-15.00,0.23,-25.00); (-15.00,0.25,-21.00); (-15.00,0.25,-19.00); (-13.04,0.25,-9.30); (-13.00,0.25,-21.00); (-9.00,0.20,-9.30); (-7.00,0.20,-9.30); (-5.00,0.20,-9.30); (5.00,0.22,-39.00); (5.00,0.21,-23.00); (5.00,0.80,-20.40); (5.00,0.80,-19.35); (7.00,0.80,-20.87); (7.00,0.80,-19.00); (9.00,0.80,-20.35); (9.00,0.20,-9.30); (9.04,0.80,-19.40); (11.00,0.80,-20.86); (11.00,0.80,-19.00); (11.00,0.20,-9.30); (12.99,0.80,-20.37); (12.99,0.80,-19.38); (13.03,0.24,-9.30); (14.45,0.80,-20.85); (17.00,0.80,-20.35); (17.00,0.80,-19.40); (19.00,0.22,-27.00); (19.00,0.80,-20.86); (19.00,0.80,-19.00); (21.00,0.80,-20.35); (21.00,0.80,-19.40); (23.00,0.20,-27.00); (23.00,0.80,-20.87); (23.00,0.80,-19.00); (25.00,0.80,-20.40); (25.00,0.80,-19.35); (27.00,0.24,-25.00); (27.13,0.25,-21.35); (27.50,0.29,-19.00); (29.00,0.25,-21.00); (29.00,0.25,-19.00); (31.00,0.25,-19.00)
L1 73 [('RevC_Shell_L1/RevC_Shell_L1_col', 50), ('StairSetSwitchback/Flight1_Understair_Closure-colonly', 18), ('Ext_44_ext_paving_promenade_535/ExtCollision', 3), ('Ext_41_ext_curb_segment_894mm_118/ExtCollision', 2)]
    (-13.00,0.30,-7.00); (-13.00,0.30,-5.00); (-13.00,0.30,-1.00); (-13.00,0.30,1.00); (-13.00,0.30,3.00); (-13.00,0.30,5.00); (-13.00,0.30,7.00); (-11.45,0.75,5.00); (-11.00,0.30,-5.00); (-11.00,0.30,-3.00); (-11.00,0.30,-1.00); (-11.00,0.30,3.20); (-11.00,0.30,6.65); (-11.00,1.65,7.15); (-11.00,0.20,9.35); (-9.00,0.30,5.00); (-9.00,0.30,6.65); (-9.00,1.65,7.15); (-9.00,0.20,9.35); (-7.60,1.65,7.15); (-7.00,0.30,-5.00); (-7.00,0.30,3.20); (-7.00,0.30,5.00); (-7.00,0.20,9.35); (-6.55,1.15,6.90); (-5.00,0.30,-7.00); (-5.00,0.30,-5.00); (-5.00,0.70,-2.65); (-5.00,0.30,3.20); (-5.00,0.30,5.00); (-5.00,0.30,7.00); (-5.00,0.20,9.35); (-3.35,0.70,-2.65); (-3.00,0.30,-7.00); (-3.00,0.30,-5.00); (-3.00,0.20,9.35); (-2.95,0.30,-0.95); (-1.00,0.30,-7.00); (-1.00,0.30,3.00); (-1.00,0.30,5.00); (-1.00,0.30,7.00); (1.00,0.30,3.20); (1.00,0.30,5.00); (1.00,0.30,7.00); (2.93,0.30,-0.93); (3.00,0.30,-5.00); (3.00,0.30,5.00); (3.00,0.40,6.99); (3.30,0.70,-2.65); (4.95,0.45,6.95); (4.99,0.30,3.29); (5.00,0.30,-7.00); (5.00,0.70,-2.65); (5.00,0.30,5.00); (7.00,0.30,-7.00); (7.00,0.30,-5.00); (7.00,0.30,-3.00); (7.00,0.30,3.20); (7.00,0.30,5.00); (8.90,0.30,-7.00); (9.00,0.30,-1.00); (9.01,0.20,9.39); (11.00,0.93,-6.87); (11.00,2.27,-5.09); (11.00,0.30,-3.00); (11.00,0.30,-1.00); (11.00,0.30,1.00); (11.00,0.20,9.36); (12.99,0.20,9.38); (13.00,0.30,-7.00); (13.00,0.30,-5.00); (13.00,0.30,-1.00); (13.00,0.30,1.00)
L2 29 [('RevC_Shell_L1/RevC_Shell_L1_col', 23), ('Ext_15_ext_tram_shelter_0/ExtCollision', 2), ('Ext_0_ext_platform_infill_952/ExtCollision', 2), ('Ext_44_ext_paving_promenade_535/ExtCollision', 1), ('SectorArchitecture/SectorSafetyFloorColliders', 1)]
    (-13.00,4.40,-6.20); (-13.00,4.40,-5.00); (-13.00,4.40,-3.00); (-13.00,4.40,-1.00); (-11.00,4.40,-6.20); (-11.00,5.20,-5.00); (-11.00,4.40,-4.45); (-11.00,4.40,-1.00); (-9.00,4.40,-6.20); (-9.00,4.40,-5.00); (-9.00,4.40,-3.00); (-9.00,4.40,-1.00); (1.00,4.40,3.00); (1.00,4.40,5.00); (1.00,4.40,7.00); (1.00,4.40,8.50); (3.00,4.40,1.55); (3.00,4.40,7.00); (3.00,4.40,8.50); (9.00,4.40,-1.00); (9.55,4.05,-2.73); (11.00,4.07,-2.70); (11.00,4.41,-1.00); (13.00,3.20,-16.35); (13.00,3.20,-15.50); (13.00,4.40,-2.10); (13.00,4.40,-1.00); (15.00,3.20,-16.35); (15.00,3.20,-15.50)
Upper(y>6.5) 18 [('RevC_Shell_L1/RevC_Shell_L1_col', 17), ('SectorArchitecture/SectorSafetyFloorColliders', 1)]
    (-11.00,8.95,-5.00); (-11.00,8.95,7.00); (-9.00,8.95,-8.80); (-9.00,8.95,-1.00); (-9.00,8.95,1.00); (-9.00,8.95,3.00); (-7.00,8.95,-7.00); (-3.00,8.95,-8.80); (-3.00,8.95,3.00); (3.00,8.95,-7.00); (3.00,8.95,7.00); (7.00,8.95,-7.00); (9.00,8.95,-8.80); (9.00,8.95,-1.00); (9.00,8.95,1.00); (9.00,8.95,3.00); (11.00,8.95,-5.00); (11.00,8.95,7.00)
```

### Notes
- Same clusters as earlier rounds. The navmesh crosses the L2 shell wall at about (0, 4.1, 1.7). The east apartments and the L1 side rooms are blocked by the shell. The L1 area under the stair is sealed by Flight1_Understair_Closure. The maglev car body and guideway block the plaza at z≈-19…-21. The y≈8.95 upper-slab navmesh has no route.
