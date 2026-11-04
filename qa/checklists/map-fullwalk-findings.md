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
