# QA-02 Retest — 2026-11-02 evening

- Tested: fresh clone of origin/main @ 278e995, re-imported, Godot 4.7 headless, `--qa-placement`. Main later moved to 480b2d0, but that is a design doc only (no godot/ or assets/ changes), so the results hold for 480b2d0.
- Probe: throwaway `/tmp/qa02probe/eve.gd`, not committed. No repo code touched. Text only.
- Method:
  - All RFID door fields opened via `_nav_qa_set_fields(true)` before any sweep.
  - Probe CharacterBody3D cloned from PlayerBody: capsule r 0.35, h 1.75, mask 1, max floor 50°, snap 0.35, 3 m/s, gravity 9.8. The game player was parked and disabled.
  - Capsule wall sweep: casts start 0.45 m in from every wall (more than 0.4 m), 0.9 m outward.
- Usage: 9.8% at start, 11% mid-run (stop line 92%).

## Status
| Item | Result | Evidence |
|---|---|---|
| Gage fixes since a9f394d | **None to retest** | `git log a9f394d..HEAD` has no commit touching godot/ or assets/ (only QA-05's report and a design doc) |
| M-70 stairs | **FAIL / still open** | See below. 0 stair colliders and 0 stair meshes at runtime: stair_set_switchback.glb and stair_guard_handrail.glb (Rook ee10b2b) aren't referenced by any .tscn/.gd, so they never load. Down-ray profile at x ±1.15: L2 4.20 until z -0.7, then a 4.08 m drop straight to 0.12 from z -0.95 to -8.6 (no treads, ramps or landing). Climb from L1 (-1.15, -0.2) → landing → (1.15, -0.3) ends at y 0.00 (never reaches L2). "Descend" from L2 just drops 4.2 m at z -0.8. NAV-08 repro: gallery walk (-11.5, 4.3, 1.6) → (6.5, -2.5) falls into the stair core and lands at (1.55, 0.0, -1.68). Only core collider: MezzanineGlassBalustrade_L2Edge (x -1.89..0.37, z -4.86, y 4.26–5.30). Gaps/overlaps between stair colliders can't be tested because none exist |
| M-46 tram platform | **Still open (improved)** | Walk from (10.2, 0.45, -16.3) → (12.8, -16.6) stops at (11.71, 0.33, -16.47), 1.10 m short. The player escapes 2/4 directions now (Patch had 0/4), so it's no longer a full trap, but it still can't reach the tram point |
| M-73 NW corner | **Still open** | From (-12.0, 0.3, -7.0) → (-14.3, -9.3) the player wedges at (-13.55, 0.05, -8.55), matching QA-01's coordinates; escapes 0/4 (0.00 m moved each way). See GEO-17 for the mirror corner |
| Capsule sweep (doors open, >0.4 m inset) | **PASS** | 17 rects, 2,322 samples, 38 open runs. All 35 runs ≥0.5 m sit at doors, corridor openings or internal rect joins (103/104/203/204 L-joins, StairCore front 2.8 m, Corridor 3.0 m). No open run on any outer or party wall. Maintenance S door is open x 2.65–3.65 with fields open, so the GEO-13 false positive is gone |
| M-64 Lost_And_Found_Rail_Bins | Still open | +0.390 m over ExtGroundBody |
| M-65 Task_Lamp_201 | Still open | +0.215 m over L2 |
| M-66 Wardrobe_101 | Still open | +0.100 m |
| M-71 Apt201_ExBench_DustOutline | Still open | +0.224 m over L2 |
| M-72 Potted_Plants_Rail_Cradles_102 | Still open | +0.200 m |
| GEO-14 ground pieces buried | Still open | canal_edge 42 (-0.057), paving_promenade 19 (worst -0.250), curbs 8 (-0.015), platform_infill 1 / kerb_ramp 1 (-0.052) |
| GEO-15 dead_foliage_1004 no collider | Still open | 0 own colliders |
| GEO-16 planting strips float | Still open | 1004 / 1006 / 1007 at +0.051 m |

## New bugs
### GEO-17 — L1 SE corner wedges the player too, mirror of M-73 (High, Gage; Rook if shell/chamfer)
- From (12.0, 0.3, -7.0) walking toward (14.3, -9.3), the player stops at (13.50, 0.05, -8.55) and escapes 0/4 directions (0.00 m each). This is the same trap as M-73 at the mirrored corner. QA-01 reported this corner as escapable. With this probe body (PlayerBody mask/floor settings) it is not.
- The two z -0.5 corners, (±13.55, -0.70), escape 3/4 (pass).
- Both trapped corners sit at y 0.05: the body rests 0.05 m into/above the L1 slab where the 0.12 floor finish (ExtGroundBody) ends. Check the floor-finish edge plus the 0205e56 chamfer at z -8.55, x ±13.5.
### GEO-18 — Rev C stair GLBs never loaded at runtime (High, Gage; part of M-70)
- `stair_set_switchback.glb` and `stair_guard_handrail.glb` (with Rook's ee10b2b `-colonly` ramps, landings and guard hulls) have no reference in any .tscn or .gd, so the runtime stair core has no stair meshes or colliders. Rook's GLB-level walk PASS doesn't carry over to the game. Gage needs to instance both GLBs in the stair core. Dedupe candidate: M-70.
