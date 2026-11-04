# Doc A — Map full-walk playtest findings (round 3, main a90071b)

Rules: APPEND ONLY to the end of this file. Do NOT read the existing entries before appending; write your own findings blind.
Each finding: `- [tester] [ID] location (x,y,z) | what happened | repro | severity`.
When you're done appending, open Doc B (`map-fullwalk-signoff.md`) and sign it.

---

## MAP-QA-3 — Stairs, Ramps & Vertical

- Date: 2026-11-03 · Round 3 · tested against main @ 91ea2d1 · Godot 4.7 headless, fresh clone, `godot --headless --import` run once first
- Method: real simulated input only. All keys (W/Shift/Space and E for doors) are real InputEventKey events sent through Input.parse_input_event (the scene's `_qa_key`), never Input.action_press. Mouse yaw uses InputEventMouseMotion. Long outdoor legs follow NavigationServer3D path points as steering targets. Throwaway SceneTree drivers in /tmp, outside the repo, run with `-- --qa-placement`. No position writes and no repo .gd/.tscn/.py edits.
- Built-in modes: `--qa-stairs` **PASS** (`DONE failures=0`); `--qa-egress` **PASS** (`DONE failures=0`).

| # | Location | Repro | Severity | Result |
|---|----------|-------|----------|--------|
| 1 | Stair core head L2 (1.15, 0.0) → F1 | (Round 2 Medium recheck) Hold W toward the F1 foot (1.15,-8.15) and tap Space every ~0.3 s. Unchanged: the player is thrown east to x≈3.65, pinned on `RevC_Shell_L2_col` ~3 s, then crosses all of F1 airborne at y≈4.1–5.3 (L2 height) and drops onto the landing (y 2.465). 298 frames vs ~92 walking. | Medium | FAIL (not fixed) |
| 2 | Tram kerb ramp top edge ≈ (9.4, -15.5) | (Round 2 Medium recheck) From the platform (12,-16.7) walk W/NW toward the paving (7.5,-15.0). Unchanged: y goes 0.351→0.305, then the player stops dead at (9.41,-15.47) y=0.305, on the floor with W held, for the rest of the 120-frame window. Never steps down to the paving (0.05). Walking up along the egress line still works. | Medium | FAIL (not fixed) |
| 3 | Stair core F1/F2 jump sweep | Jump-spam down F1/F2 and up F2/F1: all settle in band (landing 2.465, L1 0.00, L2 4.08). Up F1 arrives airborne and lands in 23 frames (normal arc). | — | PASS |
| 4 | Mid-flight F2 (-1.15,-5.0) | Stop on the ramp (y=1.048, on floor), turn 180° with the mouse, walk down to L1. No slide or snag. | — | PASS |
| 5 | Landings (±1.15,-8.15) | Standing jump dy=-0.001; crossing the landing both ways. | — | PASS |
| 6 | F1 sprint | Shift+W down/up F1 settles at 2.465 / 4.080. | — | PASS |
| 7 | Tram platform kerb front edge (z=-17.55) | Walk S past the kerb line: the surface continues at y 0.35 with no drop; walk back N onto the platform cleanly. | Info | PASS |
| 8 | Curb row `ext_curb_segment_21..23` (z≈19.35, x≈-10) | Walk N over it, walk S back, jump-cross N: all clean (curb top 0.15). | — | PASS |
| 9 | Egress route exterior paving + `--qa-egress` path | All in band. | — | PASS |

Totals: 0 Critical, 0 High, 2 Medium, 0 Low, 1 Info; 7 PASS, 2 FAIL.

## MAP-QA-5 — Freeform player playtest round 3 (main 91ea2d1, 2026-11-03)

Fresh clone at 91ea2d1, `godot --headless --import` once (rc 0). Godot 4.7.2 headless, `preface_playable_area.tscn` with `-- --qa-placement` (normal Apt 201 spawn (-9.35,4.25,6.20)). Movement via `Input.action_press`; E/F sent as real `InputEventKey` press+release through `Input.parse_input_event`. Driver scripts in /tmp, not in repo. Same route as round 2: Apt 201 → 2F corridor → switchback stairs → ground → SECTOR-4 exit (E at hub) → promenade both ways; plus Apt 201 corner/wall sprint+jump run and the north-railing jump run. Results are identical to round 2 coordinates — no change observed.

- **R2-N1 ground-floor blocker (1.55, 0.00, -0.99) — STILL PRESENT (MEDIUM).** Walking east along z -1.0 from the stair foot stops dead at x 1.55; heading north needs a jump (apex y 1.22, floor=false ~1 s) to clear it, landing (1.55,0,-4.35). Repro: stairs down → (-1.55,-1.0) → forward toward (3.5,-1.0), then toward (3.5,-7.9).
- **R2-N2 Apt 201 west-wall snag (-13.55, 4.08, 5.82) — STILL PRESENT (LOW).** Sprinting south along the west wall from (-13.3,8.4): stuck ~1 s+ with input held (4 samples mv=0.00); jump clears a ~1.2 m obstacle (apex y 5.29) and lands z 1.84. Repro: spawn → sprint to (-13.5,8.5) → sprint toward (-13.5,1.4).
- **R2-N3 exit-panel short stop (1.55, 0.00, -7.86) — STILL PRESENT (LOW).** Player is blocked ~1 m short of the hub (1.45,0,-8.90); real E keypress from there opens SECTOR4_EXIT and the exit walks fine to (0.06,0.06,-11.77).
- **Promenade bumps — STILL PRESENT (LOW).** y pops 0.15 at (-5.62,-10.35) and (-6.86,-9.96) on the diagonal from the exit; sprinting the wall at z≈-9.5: y 0.20 at x -2.94 and 0.19 at x +3.07. No wall hang.
- **Apt 201 door snag (-3.99, 4.08, 1.69) — STILL PRESENT (LOW).** Approach to the Apt 201 hub stops ~1 s; real E keypress opens APT201 from there and the doorway is walkable.
- **Regression checks — PASS.** North-railing jump at (0,4.08,-4.43) still contained (no drop to promenade). Apt 201/Alcove 2C/SECTOR-4 open with real E; closed Apt 202 not tested this round; stairs 4.08 → 2.46 → 0.00 clean; Apt 201 SE corner ledge not reproduced.

## MAP-QA-2 — Round 3 (91ea2d1)

Tested commit: `91ea2d1` (fresh clone; `godot --headless --import` run once first). Godot 4.7.2 headless, `--fixed-fps 60`, one run at a time. The untracked harness lives outside the repo. **All input this round is real `InputEventKey` events sent through `Input.parse_input_event`**: W, Shift, Space, and E for doors; no `Input.action_press`. The harness only teleports the player to each start point and sets yaw before a probe; everything after that is key input. The 0.5 m down-ray hole grid on L1 and L2 is identical to rounds 1 and 2. Walk probes: 113 (the full round-1/2 edge sweep, the 14 round-2 re-checks, and 8 new round-3 probes), plus 42 door steps (7 per door × 6 RFID doors).

**Counts:** falls / unguarded drops 0 · invisible walls over continuous floor 0 · holes 0 · walk-through solids 0 · wedge/stuck from normal play 0 · low 1 (still open from round 2) · info 1 (back from round 1).

**Doors (E key, all 6: APT201, APT202, ALCOVE2C, RM1A, RM1B, SECTOR4_EXIT): PASS.**
- Locked: walking into the field stops 0.45 m short of it.
- E pressed at the hub (from the corridor side, 0.9 m out, facing the door's direction) opens the door, and the player walks through.
- E pressed while the player stands in the doorway plane: the door sets `close_pending`, names `close_blocker=PlayerBody`, and stays open, so the player is never trapped or shoved. It closes once the player walks clear.
- Once it closes, a walk and a sprint-jump are both blocked again.
- Minor: `close_blocker` still reads `PlayerBody` after the door has closed. It's a stale field with no effect on collision.

**Re-check of round 2**
1. **[LOW] Alcove 2C rail sprint-jump: STILL REPRODUCES**, now in both directions. Nodes: `Seam03_Alcove2C_EastRail` (x -10.30) and `Seam03_Alcove2C_Rail` (x -10.18), 1.1 m tall.
   - Out of the alcove: start at (-12.5, 4.3, -4.2) or (-12.5, 4.3, -5.4) at yaw -90, hold W and Shift, then hold Space. The player clears both rails and crosses the atrium to (-2.45, ~4.1, -4.2 / -6.37).
   - Into the alcove: start at (-8.5, 4.3, -4.2 / -5.4) at yaw 90, same keys. The player clears both rails and reaches the alcove west wall at (-13.55, 4.08, z).
   - Plain walking is blocked at x -10.69. The floor is the same level on both sides, so there's no fall.
2. **[INFO] Shelf hang: REPRODUCES again**; round 2 marked it as not reproduced, so it's intermittent. After a teleport to (-11.0, 4.4, -4.8), between `Alcove2C_Battery_Expansion_Support/Shelf_Shape` and `Alcove2C_SuperWire_Expansion_Support/Shelf_Shape`, the player hangs at y 4.40 with `is_on_floor()=false`. Holding W works in neither direction. Only a teleport gets you there; walking from (-12.5, 4.3, -5.4) slides past the SuperWire shelf without sticking. It would matter only if a respawn or save point ever lands there.

Full edge sweep: every probe ends at the same place as round 2, within ±0.02 m. That covers the L2 inner wing edges at x ±2.45, the outer walls at x ±13.55 and z ±8.55, the old west-wing guardrail line (still clear), and the stairwell glass, where walking stops at z -4.42 and all six sprint-jumps are stopped by `StairwellHeadGlassCap`. It also covers the 0.37–0.40 gap before flight 2 (sealed), the ±10 m columns, all four L2 corners and the diagonal wall slides (no wedging), and the L1 radials (no falls; min y dipped to -0.09 once at the a22 threshold and recovered). The new ExtGround bounds and curb seam caps are exterior, MAP-QA-4's area, so I didn't test them here.

## MAP-QA-4 — Exterior & Tram (Round 3, 2026-11-03)

Build: main 91ea2d1, fresh clone, `godot --headless --path godot --import` (clean), then `-s <harness> -- --qa-placement` (harness kept outside the repo). Movement used `Input.action_press` move_forward/jump through the player controller. E/F used real `InputEventKey` press+release via `Input.parse_input_event`. `_qa_place` was used only for start points. Curb joins: 162 collinear seams across 197 curb segments were each crossed at the seam, and every failure was re-crossed 0.5 m off-seam to separate seam bugs from walls.

### Findings
- **HIGH — the map-edge bounds stop at z≈-28 (ExtGroundWestBound / ExtGroundEastBound, z range -28.0..42.5).** Repro: start at (±44, 0, -29.5) and walk outward (west/east) while jumping. Expected: a wall at x ±49. Actual: the player walks past the south end of the bound, falls off the ground (min y -7.87) and the fall recovery respawns them at (-11.96, 4.08, 1.36). Same result on both sides.
- **MEDIUM — the mid-air hang at y 0.72 is still there on the west/east guardrails (x ±18).** Repro: start at (∓15, 0, -30), walk toward the rail and jump every 20 frames. Actual: the player ends at (±17.53, 0.72, -30) with is_on_floor=false and 77–79 stuck frames. Expected: they slide down to the floor.
- **MEDIUM (new) — the same hang at y 0.72 happens in the new bound corners NW (-48.65, 42.15) and NE (48.65, 42.15).** Repro: start at (±45, 0, 38.5), walk diagonally into the corner and jump. Actual: stuck at y 0.72 with floor=false. The straight wall faces (x ±49 at z -25/0/20/40, and z 42.6 at x -40/-10/10/40) block correctly, ending at ±48.65 / 42.15 on the floor, and no climb-over was seen (max y 1.27).
- **LOW — the dead-foliage strip Ext_49_ext_ts4_dead_foliage_1004 can still be hopped.** Repro: start at (-14.5, 0, 0), yaw 90, jump. Actual: the player reaches x -24.37.
- **LOW (new) — curb seam snag on the rotY=90 curb row at x -16.95.** Seams Ext_41_ext_curb_segment_61|62 (z -5.0), 69|70 (z 0.0) and 77|78 (z 5.0). Repro: walk -x across the seam from x -15.55. Actual: the player stops on the curb at (-16.25, 0.35) after moving 0.7 m (22 stuck frames). 0.5 m off the seam they cross cleanly (2.08 m).
- Info: the other non-crossings (z 10.15, z -8.95/-10.15, z -18.35, z -21.8, x -15.25 rows) were blocked the same way off-seam, so they come from adjacent walls or colliders and are not seam bugs.

### Round 2 retest
- Guardrail south (z -45) mid-air hang: **FIXED** (ends at z -44.53 on the floor).
- Guardrail west/east mid-air hang at y 0.72: **STILL OPEN**.
- DOOR_SECTOR4_EXIT: **FIXED**. A real E key opens it from the north (-7.5) and from the south (-10.2), and the player walks through.
- Dead-foliage hop to x≈-24.4: **STILL OPEN** (x -24.37).
- Curb seam snag at x -7.0, z 19.35: **FIXED** (step-up and step-down are clean).

## MAP-QA-1 Round 3 — Traversal sweep — 2026-11-03

- Build: FinalFracture/Aegis-7 main @ 91ea2d1, fresh clone, `godot --headless --import` run first, Godot 4.7.2 headless `--fixed-fps 60`. Scene: preface_playable_area.tscn.
- Method: same harness, same 482-cell grid and same thresholds as Rounds 1–2. Movement uses `Input.action_press` (move_* / sprint / look_left / look_right). This round changed one thing: E (interact) and F (rfid_pulse) are now sent only as real `InputEventKey` events through `Input.parse_input_event` (pressed, then released 3 frames later), with no action_press. When the player stalls, F is tapped at stall frame 40/80 and E at 20/60/100. Batches ran one at a time, never in parallel.

### Coverage (Round 3; Round 2 in brackets)
| Region | Cells | Reached | Not reached |
|---|---|---|---|
| L1 | 118 | 45 (45) | 73 (73) |
| L2 | 36 | 7 (7) | 29 (29) |
| Apartments | 44 | 22 (22) | 22 (22) |
| Exterior plaza | 266 | 205 (187) | 61 (79) |
| Upper slab y≈8.95 | 18 | 0 (0) | 18 (18) |

Total reached: 279/482 (Round 2: 261). Stuck spots: **0**. Fall-through: **0**.

### Change vs Round 2
```
NEWLY_REACHED 22 ExteriorPlaza(-35.00,0.25,-21.00); ExteriorPlaza(-37.00,0.25,-19.00); ExteriorPlaza(-37.00,0.25,-21.00); ExteriorPlaza(-37.00,0.21,-23.00); ExteriorPlaza(-37.00,0.22,-27.00); ExteriorPlaza(-39.00,0.25,-19.00); ExteriorPlaza(-39.00,0.25,-21.00); ExteriorPlaza(-41.00,0.25,-19.00); ExteriorPlaza(-41.00,0.25,-21.00); ExteriorPlaza(-43.00,0.25,-19.00); L1(-9.00,0.30,-1.00); ExteriorPlaza(35.00,0.25,-19.00); ExteriorPlaza(35.00,0.25,-21.00); ExteriorPlaza(37.00,0.25,-19.00); ExteriorPlaza(37.00,0.25,-21.00); ExteriorPlaza(37.00,0.23,-23.00); ExteriorPlaza(37.00,0.22,-27.00); ExteriorPlaza(39.00,0.25,-19.00); ExteriorPlaza(39.00,0.25,-21.00); ExteriorPlaza(41.00,0.25,-21.00); ExteriorPlaza(7.00,0.20,-9.30); ExteriorPlaza(9.00,0.20,-9.30)
NEWLY_UNREACHED 4 ExteriorPlaza(-17.00,0.25,-19.00) blk=['Ext_44_ext_paving_promenade_387', 'ExtCollision']; ExteriorPlaza(27.00,0.24,-25.00) blk=['Ext_44_ext_paving_promenade_340', 'ExtCollision']; ExteriorPlaza(31.00,0.25,-19.00) blk=['Ext_17_ext_maglev_guideway_15', 'ExtCollision']; L1(2.93,0.30,-0.93) blk=['RevC_Shell_L1', 'RevC_Shell_L1_col']
```
Most of the gains are at the plaza's far east and west ends (x ±35…43, z -19…-27) and in two cells in front of the building (x 7–9, z -9.3).

### Not-reached cells (x, y, z) and the last collider hit
```
UNREACHABLE by region & blocker
Apartments 22 [('RevC_Shell_L1/RevC_Shell_L1_col', 20), ('SectorArchitecture/SectorSafetyFloorColliders', 2)]
    (5.00,4.40,3.00); (6.99,4.40,1.58); (7.00,4.40,3.20); (7.00,4.40,5.00); (7.00,4.40,7.00); (7.00,4.40,8.50); (9.00,4.40,1.00); (9.00,4.40,5.00); (9.00,4.40,7.00); (9.00,4.40,8.50); (9.05,4.40,3.10); (11.00,4.40,1.00); (11.00,4.40,3.10); (11.00,4.40,5.00); (11.00,5.25,7.00); (11.00,4.40,8.50); (11.25,4.40,6.50); (13.00,4.40,1.00); (13.00,4.40,3.10); (13.00,5.05,5.00); (13.00,4.40,7.00); (13.00,4.40,8.50)
ExteriorPlaza 61 [('Ext_19_ext_maglev_car_body_18/ExtCollision', 12), ('Ext_19_ext_maglev_car_body_17/ExtCollision', 10), ('Ext_17_ext_maglev_guideway_7/ExtCollision', 9), ('RevC_Shell_L1/RevC_Shell_L1_col', 4), ('Ext_44_ext_paving_promenade_387/ExtCollision', 3), ('RevC_Shell_L2/RevC_Shell_L2_col', 2)]
    (-35.00,0.25,-19.00); (-31.00,0.25,-19.00); (-29.00,0.25,-21.00); (-29.00,0.25,-19.00); (-27.00,0.25,-21.00); (-27.00,0.25,-19.00); (-25.00,0.25,-21.00); (-25.00,0.25,-19.00); (-23.00,0.21,-27.00); (-23.00,0.23,-25.00); (-23.00,0.25,-21.00); (-23.00,0.26,-19.00); (-21.00,0.25,-21.00); (-21.00,0.27,-19.01); (-19.00,0.22,-27.00); (-19.00,0.25,-21.00); (-19.00,0.26,-19.00); (-17.00,0.25,-21.00); (-17.00,0.25,-19.00); (-15.00,0.21,-33.00); (-15.00,0.23,-25.00); (-15.00,0.25,-21.00); (-15.00,0.25,-19.00); (-13.04,0.25,-9.30); (-13.00,0.25,-21.00); (-9.00,0.20,-9.30); (-7.00,0.20,-9.30); (-5.00,0.20,-9.30); (5.00,0.22,-39.00); (5.00,0.21,-23.00); (5.00,0.80,-20.40); (5.00,0.80,-19.35); (7.00,0.80,-20.87); (7.00,0.80,-19.00); (9.00,0.80,-20.35); (9.04,0.80,-19.40); (11.00,0.80,-20.86); (11.00,0.80,-19.00); (11.00,0.20,-9.30); (12.99,0.80,-20.37); (12.99,0.80,-19.38); (13.03,0.24,-9.30); (14.45,0.80,-20.85); (17.00,0.80,-20.35); (17.00,0.80,-19.40); (19.00,0.22,-27.00); (19.00,0.80,-20.86); (19.00,0.80,-19.00); (21.00,0.80,-20.35); (21.00,0.80,-19.40); (23.00,0.20,-27.00); (23.00,0.80,-20.87); (23.00,0.80,-19.00); (25.00,0.80,-20.40); (25.00,0.80,-19.35); (27.00,0.24,-25.00); (27.13,0.25,-21.35); (27.50,0.29,-19.00); (29.00,0.25,-21.00); (29.00,0.25,-19.00); (31.00,0.25,-19.00)
L1 73 [('RevC_Shell_L1/RevC_Shell_L1_col', 50), ('StairSetSwitchback/Flight1_Understair_Closure-colonly', 18), ('Ext_44_ext_paving_promenade_535/ExtCollision', 3), ('Ext_41_ext_curb_segment_894mm_118/ExtCollision', 2)]
    (-13.00,0.30,-7.00); (-13.00,0.30,-5.00); (-13.00,0.30,-1.00); (-13.00,0.30,1.00); (-13.00,0.30,3.00); (-13.00,0.30,5.00); (-13.00,0.30,7.00); (-11.45,0.75,5.00); (-11.00,0.30,-5.00); (-11.00,0.30,-3.00); (-11.00,0.30,-1.00); (-11.00,0.30,3.20); (-11.00,0.30,6.65); (-11.00,1.65,7.15); (-11.00,0.20,9.35); (-9.00,0.30,5.00); (-9.00,0.30,6.65); (-9.00,1.65,7.15); (-9.00,0.20,9.35); (-7.60,1.65,7.15); (-7.00,0.30,-5.00); (-7.00,0.30,3.20); (-7.00,0.30,5.00); (-7.00,0.20,9.35); (-6.55,1.15,6.90); (-5.00,0.30,-7.00); (-5.00,0.30,-5.00); (-5.00,0.70,-2.65); (-5.00,0.30,3.20); (-5.00,0.30,5.00); (-5.00,0.30,7.00); (-5.00,0.20,9.35); (-3.35,0.70,-2.65); (-3.00,0.30,-7.00); (-3.00,0.30,-5.00); (-3.00,0.20,9.35); (-2.95,0.30,-0.95); (-1.00,0.30,-7.00); (-1.00,0.30,3.00); (-1.00,0.30,5.00); (-1.00,0.30,7.00); (1.00,0.30,3.20); (1.00,0.30,5.00); (1.00,0.30,7.00); (2.93,0.30,-0.93); (3.00,0.30,-5.00); (3.00,0.30,5.00); (3.00,0.40,6.99); (3.30,0.70,-2.65); (4.95,0.45,6.95); (4.99,0.30,3.29); (5.00,0.30,-7.00); (5.00,0.70,-2.65); (5.00,0.30,5.00); (7.00,0.30,-7.00); (7.00,0.30,-5.00); (7.00,0.30,-3.00); (7.00,0.30,3.20); (7.00,0.30,5.00); (8.90,0.30,-7.00); (9.00,0.30,-1.00); (9.01,0.20,9.39); (11.00,0.93,-6.87); (11.00,2.27,-5.09); (11.00,0.30,-3.00); (11.00,0.30,-1.00); (11.00,0.30,1.00); (11.00,0.20,9.36); (12.99,0.20,9.38); (13.00,0.30,-7.00); (13.00,0.30,-5.00); (13.00,0.30,-1.00); (13.00,0.30,1.00)
L2 29 [('RevC_Shell_L1/RevC_Shell_L1_col', 23), ('Ext_15_ext_tram_shelter_0/ExtCollision', 2), ('Ext_0_ext_platform_infill_952/ExtCollision', 2), ('Ext_44_ext_paving_promenade_535/ExtCollision', 1), ('SectorArchitecture/SectorSafetyFloorColliders', 1)]
    (-13.00,4.40,-6.20); (-13.00,4.40,-5.00); (-13.00,4.40,-3.00); (-13.00,4.40,-1.00); (-11.00,4.40,-6.20); (-11.00,5.20,-5.00); (-11.00,4.40,-4.45); (-11.00,4.40,-1.00); (-9.00,4.40,-6.20); (-9.00,4.40,-5.00); (-9.00,4.40,-3.00); (-9.00,4.40,-1.00); (1.00,4.40,3.00); (1.00,4.40,5.00); (1.00,4.40,7.00); (1.00,4.40,8.50); (3.00,4.40,1.55); (3.00,4.40,7.00); (3.00,4.40,8.50); (9.00,4.40,-1.00); (9.55,4.05,-2.73); (11.00,4.07,-2.70); (11.00,4.41,-1.00); (13.00,3.20,-16.35); (13.00,3.20,-15.50); (13.00,4.40,-2.10); (13.00,4.40,-1.00); (15.00,3.20,-16.35); (15.00,3.20,-15.50)
Upper(y>6.5) 18 [('RevC_Shell_L1/RevC_Shell_L1_col', 17), ('SectorArchitecture/SectorSafetyFloorColliders', 1)]
    (-11.00,8.95,-5.00); (-11.00,8.95,7.00); (-9.00,8.95,-8.80); (-9.00,8.95,-1.00); (-9.00,8.95,1.00); (-9.00,8.95,3.00); (-7.00,8.95,-7.00); (-3.00,8.95,-8.80); (-3.00,8.95,3.00); (3.00,8.95,-7.00); (3.00,8.95,7.00); (7.00,8.95,-7.00); (9.00,8.95,-8.80); (9.00,8.95,-1.00); (9.00,8.95,1.00); (9.00,8.95,3.00); (11.00,8.95,-5.00); (11.00,8.95,7.00)
```

### Notes
- Same clusters as before. The navmesh crosses the L2 shell wall at about (0, 4.1, 1.7). The east apartments and the L1 side rooms are blocked by the shell. The L1 area under the stair is sealed by Flight1_Understair_Closure. The maglev car body and guideway block the plaza at z≈-19…-21. The y≈8.95 upper-slab navmesh has no route.
- There are no separate L1, L2, apartment or plaza scenes; all four areas are in preface_playable_area.tscn.
