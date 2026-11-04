# Doc A — Map full-walk playtest findings (round 2, main 87c8978)

Rules: APPEND ONLY to the end of this file. Do NOT read the existing entries before appending; write your own findings blind.
Each finding: `- [tester] [ID] location (x,y,z) | what happened | repro | severity`.
When you're done appending, open Doc B (`map-fullwalk-signoff.md`) and sign it.

---

## MAP-QA-3 — Stairs, Ramps & Vertical

- Date: 2026-11-03 · Round 2 · tested against main @ 63ee92e · Godot 4.7 headless, fresh clone, `godot --headless --import` run once first
- Method: real simulated input only (InputEventKey W/Shift/Space/E + InputEventMouseMotion yaw via the scene's `_qa_key`/`_qa_mouse`/`_qa_egress_steer`; long exterior legs follow NavigationServer3D path points as steering targets). Throwaway SceneTree drivers in /tmp, outside repo, run with `-- --qa-placement`. No position writes, no repo .gd/.tscn/.py edits.
- Built-in modes: `--qa-stairs` **PASS** (`DONE failures=0`); `--qa-egress` **PASS** (`DONE failures=0`).

| # | Location | Repro | Severity | Result |
|---|----------|-------|----------|--------|
| 1 | Stair core head L2 (1.15, 0.0) → F1 | (Round 1 recheck) Hold W toward F1 foot (1.15,-8.15), tap Space every ~0.3 s. Still reproduces identically: first jump carries player east to x≈3.65, pinned against `RevC_Shell_L2_col` ~3 s, then crosses the entire F1 flight airborne at y≈4.1–5.3 (L2 height) before dropping onto the landing (y 2.465). 298 frames vs 92 walking. | Medium | FAIL (not fixed) |
| 2 | Tram kerb ramp `ext_kerb_ramp`, top edge ≈ (9.4, -15.5) | (Round 1 Low recheck, now escalated) From platform (12,-16.7) walk W/NW toward paving (7.5,-15.0). Player descends 0.351→0.305 then stops dead at (9.41,-15.47) y=0.305, on_floor, W held, for 60+ frames; never steps down to paving (0.05). Round 1 saw same stop at (9.35,-16.49). Walking up the ramp along the egress line works. Off-ramp westward is blocked by a lip / missing step-down. | Medium | FAIL |
| 3 | Tram platform kerb front edge (z = -17.55, x≈12) | Walk S off platform to (12,-18.4): player reaches (12.46,-17.79) still at y=0.35 on floor (no drop past kerb line — surface continues); walk back N onto platform y=0.307. No snag, no fall. | Info | PASS |
| 4 | Curb row `ext_curb_segment_21..23` at z≈19.35 (x≈-10) | Nav-walked from platform to (-10,18.6) (y 0.00). Walk N over curb (top y=0.15) to y=0.00 beyond; walk S back over; jump-cross N, lands y=0.07 on floor. No snag, no bounce. | — | PASS |
| 5 | Stair core F1/F2 normal walk + exterior egress route | Covered by `--qa-stairs`/`--qa-egress` and driver walks; all in Y band. | — | PASS |

Totals: 0 Critical, 0 High, 2 Medium, 0 Low, 1 Info; 3 PASS, 2 FAIL.

## MAP-QA-2 — Round 2 (63ee92e)

Tested commit: `63ee92e` (fresh clone, `godot --headless --import` run once first). Godot 4.7.2 headless, `--fixed-fps 60`. Same untracked harness as round 1, outside the repo: it teleports `PlayerBody` to each start point, then holds `move_forward`/`sprint`/`jump` with `Input.action_press`. I also re-ran the 0.5 m downward ray grid on L1 (y 0) and L2 (y 4.2). The L1 and L2 x -17..16.5 / z -13..10.5 hole grid is identical to round 1. 106 walk probes in all: the round-1 sweep repeated in full (L2 wing edges, stairwell glass, L2 perimeter N/S/E/W, four L2 corners, ±10 m column cells, L1 radials) plus 14 targeted re-verify probes.

**Counts:** falls / unguarded drops 0 · invisible walls over continuous floor 0 · holes in floor 0 · walk-through solids 0 · wedge/stuck spots 0 · low 1.

**Round-1 re-verify**
1. Stairwell glass sprint-jump: **FIXED.** I sprint-jumped at x -1.8, -1.2, -0.6, 0.0, 0.3 and 0.36 from z -3.0 toward -Z. Every jump is stopped by `StairwellHeadGlassCap` at z -4.43, the player peaks at y 5.27 and lands back on L2, and none of them enters the well. Walking into the glass at x -1.2..0.45 still stops at z -4.43, and the 0.37–0.40 gap before flight 2 is still sealed.
2. `L2WestWingSouthGuardrail` invisible wall: **FIXED** (collider removed). At x -12, -10 and -8 the player walks freely across the old line at z -6.55 in both directions, out to the real shell wall at z -8.55. The SW corner wedge probe now slides cleanly into (-13.55, -8.55).
3. Shelf hang at (-11.0, 4.4, -4.8): **not reproduced.** The player is pushed clear of `Alcove2C_Battery_Expansion_Support/Shelf_Shape` and lands on the floor at y 4.08 within 0.1 s. It walks normally both ways: -X reaches the rail at x -10.69, and +X reaches the west wall at x -13.55.

**New**
- **[LOW] A sprint-jump clears the Seam03 Alcove 2C rails.** Nodes: `Seam03_Alcove2C_EastRail` (x -10.30) and `Seam03_Alcove2C_Rail` (x -10.18), both 1.1 m tall with top y 5.42. Repro: start at (-11.0, 4.4, -4.8) facing +X (yaw -90), hold W and Shift, and tap Space. The player clears both rails and keeps going east to (-2.45, 4.08, -4.07). The floor is the same height on both sides (min y 4.08), so there is no fall. It's only a guard bypass, and it matters only if the rails are meant to keep the player inside Alcove 2C.

Everything else matches round 1. The L2 inner wing edges (x ±2.45), the outer walls (x ±13.55, z ±8.55) and the ±10 m column cells all block solidly. Every L1 radial ends at the same point as in round 1, with no falls, and the walk down flight 2 from (1.2, 4.3, -2.5) is still smooth. The new `Promenade*GuardrailCap` boxes are outside this interior sweep, so I didn't test them here; that's MAP-QA-4's exterior job.

## MAP-QA-5 — Freeform player playtest round 2 (main 63ee92e, 2026-11-03)

Fresh clone at 63ee92e, `godot --headless --import` run once (rc 0), Godot 4.7.2 headless, `preface_playable_area.tscn` with `-- --qa-placement` (passive mode, normal Apt 201 spawn (-9.35,4.25,6.20)). Input: `Input.action_press` move/sprint/jump plus `InputEventKey` E/F via `Input.parse_input_event`; driver scripts in /tmp, not in repo. Traces every 0.25–0.5 s. Full route walked: Apt 201 → 2F corridor (both ends, Alcove 2C, closed Apt 202) → switchback stairs → ground → SECTOR-4 exit (opened with E at hub) → promenade both directions.

### Round-1 rechecks
- **R1 north-railing jump to promenade — FIXED.** At (0.00,4.08,-4.43) repeated jumps (apex y 5.29) now land back at z -4.43; walking/jumping north 10 s never leaves the floor. Exit stays closed, no bypass.
- **R1 promenade wall bumps — STILL PRESENT (LOW).** Sprinting along the wall at z≈-9.5 from x -8 → +8: pop to y 0.21 (floor=false) at x≈-3.24; walking the diagonal from the exit to (-8,-9.6): y 0.15/0.14 at (-5.62,-10.35)/(-6.86,-9.96). No longer hangs on the wall (sprint run was continuous).
- **R1 Apt 201 SE corner ledge — NOT REPRODUCED.** Same sprint/bunnyhop sequence into (-0.45,·,1.35) stays at floor y 4.08.
- **R1 door snags — PARTLY PRESENT (LOW).** (-3.99,4.08,1.69) on Apt 201 hub approach still stops ~1 s (hub E still works from there). Alcove 2C jamb snag (-3.38,-0.45) not seen this round.

### New findings
- **N1 — MEDIUM — Ground floor: invisible/waist-high blocker at (1.55, 0.00, -0.99).** Walking east along z -1.0 from the stair foot (-1.55,0,-1.29) stops dead at x 1.55; continuing north requires a jump (apex y 1.22, floor=false ~1 s) to get over it, then you land at (1.55,0,-4.35). Repro: stairs down → (-1.55,-1.0) → hold forward toward (3.5,-1.0), then toward (3.5,-7.9).
- **N2 — LOW — Apt 201 west wall snag at (-13.55, 4.08, 5.82).** Sliding south along the west wall (sprint, yaw ~58°) the player sticks for 4+ s with input held; only a jump frees it (it then glides over at y 5.29 to z 1.84, i.e. there's a ~1.2 m obstacle you can hop). Reproduced in two separate runs. Repro: spawn → sprint to (-13.5,8.5) → sprint toward (-13.5,1.4).
- **N3 — LOW — Ground route to SECTOR-4 hub stops 1 m short.** Heading north at x 1.55 the player is blocked at (1.55,0,-7.86) (hub at (1.45,0,-8.90)); E still opens SECTOR4_EXIT from there and the exit/promenade route walks fine (0.06,-11.77).
- **Pass:** Apt 201/Alcove 2C open with E and are walkable; closed Apt 202 field holds (stops z 0.30 sprinting); 2F corridor walls x ±9.55 / z ±0.45 solid; switchback stairs walk cleanly 4.08 → landing 2.46 (z -8.1..-8.55) → 0.00 at (-1.55,-2.93); jumps on the landing return to y 2.46.

## MAP-QA-4 — Exterior & Tram (Round 2, 2026-11-03)

Build: main 63ee92e, fresh clone, `godot --headless --path godot --import`, and then `-s <harness> -- --qa-placement` (the harness is kept outside the repo). Movement used real `Input.action_press` (move_forward / jump / interact / rfid_pulse) through the player controller. `_qa_place` was used only to pick start points. Ray grids: x -14..-1, z 15..25 (curb row) and x 8..21, z -21..-15 (tram platform) → 252 rays, 0 misses.

### Round 1 retest
- R1-1 promenade guardrails jump-over (HIGH): **FIXED (escape)**, but there is a new side effect (see F1). Jumping at the S/W/E rails (every 10 or 20 frames, for up to 200 frames) peaks at y 1.22. The player never stands on the rail or leaves bounds.
- R1-2 DOOR_SECTOR4_EXIT not opening (MEDIUM): **STILL OPEN.** Interact plus rfid_pulse from the south (0,0.05,-10.2) and from the north (0,0,-7.5): `_sector4_exit_open_or_opening()` stays false. Walking in stops at z -9.45 from the south and -8.54 from the north. It may be an intended RFID gate; this still needs confirming.
- R1-3 dead-foliage strip hop `Ext_49_ext_ts4_dead_foliage_1004` (LOW): **STILL OPEN.** Start at (-14.5,0.3,0) facing -X, hold W and jump every 20 frames: the player ends at (-24.37, 0.05, 0.0). Without jumping, the player is stopped on the strip at x -16.26.

### New findings
- **F1 MEDIUM: the player hangs in mid-air against the promenade guardrails.** Nodes: PromenadeSouth/West/EastGuardrail (z -45, x ±18). Repro: start at (-15,0.3,-30) facing -X (or at (15,..) facing +X, or at (0,0.3,-44) facing -Z), hold W and tap jump. The player ends at (-17.53, 0.72, -30) / (17.53, 0.72, -30) / (0, 0.72, -44.53) with is_on_floor()=false. They stay there after all input is released for 30 frames, even though the ground below is y 0.12 (ExtGroundCol). Expected: the player slides down to the deck. Actual: the player is pinned on the rail face about 0.6 m up.
- **F2 LOW: the curb row at z≈19.35 snags at a segment seam at x = -7.0.** Repro: start at (-7.0,0.3,17.5) facing +Z and hold W for 60 frames. The player stops at z 18.9 (stuck for 40 frames) and does not step up. At x -7.05, -6.95, -3.4, -4, -5, -9, -10, -11 and -12.5 the player steps up to the 0.27 curb top and back down cleanly. Walking along the row (z 19.35 and 19.2, x -2.9 ↔ -13.1, both ways) has no snags or drops. Jumping onto the curb works. Expected: no snag at the seam. Actual: the player is blocked on the exact seam line between the curbs at x -8.0 and -6.003.
- **F3 INFO (pass): tram platform kerb `Ext_16_ext_tram_platform_kerb_1..6` (z -17.55, x 10..20).** The kerb steps up from the platform end at x 8 and can be jumped onto from the end. Walking along it at z -17.55 and -17.7 from x 9.3 → 17.53 (stopped by the east guardrail, as expected) and back west to x 4.42 has no snag or fall-through. Stepping or jumping toward the track side stops at z -18.24 (on floor, y 0.35) at x 9.5, 11, 13, 15, 19 and 21, so the player can't fall onto the guideway. Note: walking -Z at x 17 stops early at z -16.11 (prop/shelter collider, probably intended).
- **F4 INFO (pass): no ground holes or sunk/floating ground** in either grid. The curb top is y 0.27 and the deck is y 0.12.

## MAP-QA-1 Round 2 — Traversal sweep — 2026-11-03

- Build: FinalFracture/Aegis-7 main @ 63ee92e, fresh clone, `godot --headless --import` run first, Godot 4.7.2 headless `--fixed-fps 60`. Scene: `res://scenes/preface/preface_playable_area.tscn`.
- Method: same harness and grid as Round 1. Movement used only `Input.action_press` (move_* / sprint / look_left / look_right) plus `InputEventKey` E taps to open doors. The only reset is back to SPAWN_POS before each attempt. Routes go from spawn and from the `--qa-egress` checkpoints, then follow the navmesh. 482 cells (2 m XZ × 1.5 m Y), the same cell set as Round 1. Stuck = max escape displacement < 0.15 m. Fall-through = ends > 2 m below the cell.

### Coverage (Round 2; Round 1 in brackets)
| Region | Cells | Reached | Not reached |
|---|---|---|---|
| L1 | 118 | 45 (44) | 73 (74) |
| L2 | 36 | 7 (7) | 29 (29) |
| Apartments | 44 | 22 (22) | 22 (22) |
| Exterior plaza | 266 | 187 (187) | 79 (79) |
| Upper slab y≈8.95 | 18 | 0 (0) | 18 (18) |

Total reached: 261/482 (Round 1: 260/482). Stuck spots: **0**. Fall-through: **0**. Neither changed from Round 1.

### Change vs Round 1
- Newly reached: L1 (-5.00,0.30,-0.80), L1 (-7.00,0.30,-1.00), Plaza (41.00,0.25,-19.00)
- Newly not reached: Plaza (-43.00,0.25,-19.00), blocked by Ext_17_ext_maglev_guideway_8. L1 (-9.00,0.30,-1.00), blocked by RevC_Shell_L1_col.
- All other cells had the same result. These flips are at cluster edges, so they may be route noise rather than map changes.

### Not-reached cells (x, y, z) and the last collider hit
```
UNREACHABLE by region & blocker
Apartments 22 [('RevC_Shell_L1/RevC_Shell_L1_col', 22)]
    (5.00,4.40,3.00); (6.99,4.40,1.58); (7.00,4.40,3.20); (7.00,4.40,5.00); (7.00,4.40,7.00); (7.00,4.40,8.50); (9.00,4.40,1.00); (9.00,4.40,5.00); (9.00,4.40,7.00); (9.00,4.40,8.50); (9.05,4.40,3.10); (11.00,4.40,1.00); (11.00,4.40,3.10); (11.00,4.40,5.00); (11.00,5.25,7.00); (11.00,4.40,8.50); (11.25,4.40,6.50); (13.00,4.40,1.00); (13.00,4.40,3.10); (13.00,5.05,5.00); (13.00,4.40,7.00); (13.00,4.40,8.50)
ExteriorPlaza 79 [('RevC_Shell_L2/RevC_Shell_L2_col', 22), ('Ext_19_ext_maglev_car_body_18/ExtCollision', 12), ('Ext_19_ext_maglev_car_body_17/ExtCollision', 10), ('Ext_17_ext_maglev_guideway_7/ExtCollision', 8), ('RevC_Shell_L1/RevC_Shell_L1_col', 5), ('Ext_17_ext_maglev_guideway_8/ExtCollision', 3)]
    (-43.00,0.25,-19.00); (-41.00,0.25,-21.00); (-41.00,0.25,-19.00); (-39.00,0.25,-21.00); (-39.00,0.25,-19.00); (-37.00,0.22,-27.00); (-37.00,0.21,-23.00); (-37.00,0.25,-21.00); (-37.00,0.25,-19.00); (-35.00,0.25,-21.00); (-35.00,0.25,-19.00); (-31.00,0.25,-19.00); (-29.00,0.25,-21.00); (-29.00,0.25,-19.00); (-27.00,0.25,-21.00); (-27.00,0.25,-19.00); (-25.00,0.25,-21.00); (-25.00,0.25,-19.00); (-23.00,0.21,-27.00); (-23.00,0.23,-25.00); (-23.00,0.25,-21.00); (-23.00,0.26,-19.00); (-21.00,0.25,-21.00); (-21.00,0.27,-19.01); (-19.00,0.22,-27.00); (-19.00,0.25,-21.00); (-19.00,0.26,-19.00); (-17.00,0.25,-21.00); (-15.00,0.21,-33.00); (-15.00,0.23,-25.00); (-15.00,0.25,-21.00); (-15.00,0.25,-19.00); (-13.04,0.25,-9.30); (-13.00,0.25,-21.00); (-9.00,0.20,-9.30); (-7.00,0.20,-9.30); (-5.00,0.20,-9.30); (5.00,0.22,-39.00); (5.00,0.21,-23.00); (5.00,0.80,-20.40); (5.00,0.80,-19.35); (7.00,0.80,-20.87); (7.00,0.80,-19.00); (7.00,0.20,-9.30); (9.00,0.80,-20.35); (9.00,0.20,-9.30); (9.04,0.80,-19.40); (11.00,0.80,-20.86); (11.00,0.80,-19.00); (11.00,0.20,-9.30); (12.99,0.80,-20.37); (12.99,0.80,-19.38); (13.03,0.24,-9.30); (14.45,0.80,-20.85); (17.00,0.80,-20.35); (17.00,0.80,-19.40); (19.00,0.22,-27.00); (19.00,0.80,-20.86); (19.00,0.80,-19.00); (21.00,0.80,-20.35); (21.00,0.80,-19.40); (23.00,0.20,-27.00); (23.00,0.80,-20.87); (23.00,0.80,-19.00); (25.00,0.80,-20.40); (25.00,0.80,-19.35); (27.13,0.25,-21.35); (27.50,0.29,-19.00); (29.00,0.25,-21.00); (29.00,0.25,-19.00); (35.00,0.25,-21.00); (35.00,0.25,-19.00); (37.00,0.22,-27.00); (37.00,0.23,-23.00); (37.00,0.25,-21.00); (37.00,0.25,-19.00); (39.00,0.25,-21.00); (39.00,0.25,-19.00); (41.00,0.25,-21.00)
L1 73 [('RevC_Shell_L1/RevC_Shell_L1_col', 56), ('StairSetSwitchback/Flight1_Understair_Closure-colonly', 8), ('Ext_44_ext_paving_promenade_535/ExtCollision', 4), ('Ext_41_ext_curb_segment_894mm_118/ExtCollision', 3), ('DOOR_RM1A/PortalJambCollider_R', 1), ('ExtGroundNorth/ExtGroundBody', 1)]
    (-13.00,0.30,-7.00); (-13.00,0.30,-5.00); (-13.00,0.30,-1.00); (-13.00,0.30,1.00); (-13.00,0.30,3.00); (-13.00,0.30,5.00); (-13.00,0.30,7.00); (-11.45,0.75,5.00); (-11.00,0.30,-5.00); (-11.00,0.30,-3.00); (-11.00,0.30,-1.00); (-11.00,0.30,3.20); (-11.00,0.30,6.65); (-11.00,1.65,7.15); (-11.00,0.20,9.35); (-9.00,0.30,-1.00); (-9.00,0.30,5.00); (-9.00,0.30,6.65); (-9.00,1.65,7.15); (-9.00,0.20,9.35); (-7.60,1.65,7.15); (-7.00,0.30,-5.00); (-7.00,0.30,3.20); (-7.00,0.30,5.00); (-7.00,0.20,9.35); (-6.55,1.15,6.90); (-5.00,0.30,-7.00); (-5.00,0.30,-5.00); (-5.00,0.70,-2.65); (-5.00,0.30,3.20); (-5.00,0.30,5.00); (-5.00,0.30,7.00); (-5.00,0.20,9.35); (-3.35,0.70,-2.65); (-3.00,0.30,-7.00); (-3.00,0.30,-5.00); (-3.00,0.20,9.35); (-2.95,0.30,-0.95); (-1.00,0.30,-7.00); (-1.00,0.30,3.00); (-1.00,0.30,5.00); (-1.00,0.30,7.00); (1.00,0.30,3.20); (1.00,0.30,5.00); (1.00,0.30,7.00); (3.00,0.30,-5.00); (3.00,0.30,5.00); (3.00,0.40,6.99); (3.30,0.70,-2.65); (4.95,0.45,6.95); (4.99,0.30,3.29); (5.00,0.30,-7.00); (5.00,0.70,-2.65); (5.00,0.30,5.00); (7.00,0.30,-7.00); (7.00,0.30,-5.00); (7.00,0.30,-3.00); (7.00,0.30,3.20); (7.00,0.30,5.00); (8.90,0.30,-7.00); (9.00,0.30,-1.00); (9.01,0.20,9.39); (11.00,0.93,-6.87); (11.00,2.27,-5.09); (11.00,0.30,-3.00); (11.00,0.30,-1.00); (11.00,0.30,1.00); (11.00,0.20,9.36); (12.99,0.20,9.38); (13.00,0.30,-7.00); (13.00,0.30,-5.00); (13.00,0.30,-1.00); (13.00,0.30,1.00)
L2 29 [('RevC_Shell_L1/RevC_Shell_L1_col', 23), ('Ext_44_ext_paving_promenade_535/ExtCollision', 2), ('Ext_15_ext_tram_shelter_0/ExtCollision', 2), ('Ext_0_ext_platform_infill_952/ExtCollision', 2)]
    (-13.00,4.40,-6.20); (-13.00,4.40,-5.00); (-13.00,4.40,-3.00); (-13.00,4.40,-1.00); (-11.00,4.40,-6.20); (-11.00,5.20,-5.00); (-11.00,4.40,-4.45); (-11.00,4.40,-1.00); (-9.00,4.40,-6.20); (-9.00,4.40,-5.00); (-9.00,4.40,-3.00); (-9.00,4.40,-1.00); (1.00,4.40,3.00); (1.00,4.40,5.00); (1.00,4.40,7.00); (1.00,4.40,8.50); (3.00,4.40,1.55); (3.00,4.40,7.00); (3.00,4.40,8.50); (9.00,4.40,-1.00); (9.55,4.05,-2.73); (11.00,4.07,-2.70); (11.00,4.41,-1.00); (13.00,3.20,-16.35); (13.00,3.20,-15.50); (13.00,4.40,-2.10); (13.00,4.40,-1.00); (15.00,3.20,-16.35); (15.00,3.20,-15.50)
Upper(y>6.5) 18 [('RevC_Shell_L1/RevC_Shell_L1_col', 15), ('Ext_41_ext_curb_segment_894mm_118/ExtCollision', 2), ('Ext_44_ext_paving_promenade_535/ExtCollision', 1)]
    (-11.00,8.95,-5.00); (-11.00,8.95,7.00); (-9.00,8.95,-8.80); (-9.00,8.95,-1.00); (-9.00,8.95,1.00); (-9.00,8.95,3.00); (-7.00,8.95,-7.00); (-3.00,8.95,-8.80); (-3.00,8.95,3.00); (3.00,8.95,-7.00); (3.00,8.95,7.00); (7.00,8.95,-7.00); (9.00,8.95,-8.80); (9.00,8.95,-1.00); (9.00,8.95,1.00); (9.00,8.95,3.00); (11.00,8.95,-5.00); (11.00,8.95,7.00)
```

### Notes (same causes as Round 1; please triage)
- The navmesh still runs through RevC_Shell_L2_col at about (0, 4.1, 1.7). The real route is through DOOR_APT201, then the stairs.
- The east apartments (x 5–13, z 1–8.5) and the L1 side rooms end on the shell colliders. These are likely closed rooms or doors, or the navmesh passing through walls.
- The L1 cells under the stair are sealed by Flight1_Understair_Closure.
- Plaza: the maglev car body and guideway block z≈-19…-21, and the building face blocks z=-9.3.
- The y≈8.95 navmesh on the upper slab has no route to it.
- Scene check: there are no separate L1, L2, apartment or plaza scenes. All four areas are in preface_playable_area.tscn.
