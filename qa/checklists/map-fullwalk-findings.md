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
