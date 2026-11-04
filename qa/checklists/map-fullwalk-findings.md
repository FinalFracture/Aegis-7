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
