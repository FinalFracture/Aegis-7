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
