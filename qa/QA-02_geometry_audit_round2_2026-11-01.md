# QA-02 Geometry & Collision Audit — Round 2 — 2026-11-01

- Build: fresh clone of origin/main @ 2384483 (Godot 4.7 headless, `res://scenes/preface/preface_playable_area.tscn`, `--qa-placement`). Authorized by Jared, directed by Atlas.
- Probe: `/tmp/qa02_round2_probe.gd` (authored with Grok Build CLI 1.0.70 on Jared's Windows machine, run from /tmp, not committed). Physics rays + CapsuleShape3D cast_motion (player capsule r 0.35, h 1.75, centre +0.995).
- No game code or assets changed. Text only, no renders. Usage 95.5% at start, 95.7% after probe.

## Summary
| | Count |
|---|---|
| New bugs | 2 (GEO-11, GEO-12) |
| Fixed / closed (of GEO-01..10) | 7 (GEO-01, 03, 05, 06, 07, 08, 10) |
| Still open (of GEO-01..10) | 3 (GEO-02, 04, 09) |
| Rev C corners | 68 checked: 64 PASS / 4 FAIL — Patch's M-61 result confirmed |
| Capsule sweep | 2,662 samples, 68/68 corner diagonals blocked, 0 confirmed walk-through gaps |

## GEO-01..10 re-verification
| ID | Master | Round 2 result | Status |
|---|---|---|---|
| GEO-01 | M-01 | Props 38/39/42/43 each have 1 collider; capsule driven at each prop is stopped at 46% of a 1.2 m move | Fixed |
| GEO-02 | M-08 | 4 of 7 pickups still in scene (Room1A spool, Room1B cell, Apt202 cell, Alcove2C x2); the shelf colliders measured in R1 are gone, so the sunk condition no longer reproduces, but see GEO-12. Apt201_ToolWall_Thermal_Jelly / _Battery_Cell not found | Open (changed → GEO-12) |
| GEO-03 | M-09 | Apt201_ToolWall_SuperWire_Spool and _BCI_Headband no longer exist in the scene | Closed (nodes removed) |
| GEO-04 | M-10 | Ext_47 decals 1002/1003: 3 layer pairs still 0.00017 m apart over 0.327 m2 | Open |
| GEO-05 | M-20 | 0 *SeamFix nodes | Fixed |
| GEO-06 | M-21 | 6 hubs; InductionRing top 4.300 vs Chevrons 4.3355 (Apt201 hub) — separated | Fixed |
| GEO-07 | M-39 | TalkPad 5.535 vs IntercomRing 5.538 (3 mm) on 6 hubs | Fixed |
| GEO-08 | M-40 | 0 Open_Portal_Sector_Exit nodes | Fixed |
| GEO-09 | M-24 | Load still prints "Navigation region synchronization had 8 edge error(s)" | Open |
| GEO-10 | M-02 | Runtime Prop43 = (-4.858, 0.120, 5.200), yaw -90 = final spot | Fixed (position); see GEO-11 |

## Prop43 at final spot (-4.858, 0.12, 5.20) yaw -90
- Mesh AABB x -5.108..-4.608, y 0.12..1.92, z 4.25..6.15.
- Wall: +X ray hits RevC_Shell_L1_col, back gap 0.008 m (limit 0–0.015) — no wall clip. (AABB overlap with RevC_Shell_L1 / CylinderHab7 meshes is whole-shell AABB containment, not a clip.)
- Wardrobe: 0 wardrobe nodes in the scene (101 wardrobe not placed), so no mesh overlap today. Against the design wardrobe rect x -5.1..-4.6, z 4.0..7.0 the footprint overlaps 0.492 x 1.900 m = 0.93 m2 → GEO-11.

## Rev C seam checks (design/rev_c_shell_corners.json, 68 corners x 5 heights)
- 64 PASS (gap <= 0.010 m). 4 FAIL, all no-hit (INF) at every height: 103 (-10.10,-1.00) L1, 104 (10.10,-1.00) L1, 203 (-10.10,-1.00) L2, 204 (10.10,-1.00) L2. Matches M-61 (missing runtime collision). Diagonal capsule casts at those 4 corners are blocked (by adjacent walls), so no walk-through proven there.

## Capsule sweep (every Rev C rect edge, 0.20 m step, 0.36 m inset, 0.80 m outward cast)
- 124 open runs: 98 slivers (mostly <=0.3 m at rect ends where the capsule meets the perpendicular wall — probe artifact) and 26 runs >= 0.70 m. All long runs sit on corridor-facing (N/S) edges at door positions or internal L-shape joins (e.g. 103/203 and 104/204 rect0↔rect1 joins at z -1.0, Maintenance 3.2 m front, StairCore 3.8 m front, corridor door runs 0.8 m). No open run found on any exterior or party wall (E/W edges, outer N/S edges). Patch: please cross-check the run list against the door table; raw output kept in /tmp/qa2out.log.
- 68/68 corner diagonal casts blocked.

## New bugs
### GEO-11 — Prop43 footprint overlaps the planned Room 101 wardrobe rect (Med, Gage + Vance)
- Prop43 XZ footprint x -5.108..-4.608, z 4.25..6.15 vs design wardrobe rect x -5.1..-4.6, z 4.0..7.0: overlap 0.93 m2. No wardrobe node exists yet, so this will clip as soon as the wardrobe is placed. Dedupe candidate: M-02 note.
### GEO-12 — Pickups with no collider beneath them (Med, Gage)
- Down rays from 0.5 m above mesh bottom hit only the floor: Room1A_Laundry_SuperWire_Spool / Room1B_Substation_Battery_Cell bottom 0.98 vs ExtGroundBody 0.12 (0.86 m); Apt202_Desk_Battery_Cell 5.10 vs 4.20 (0.90 m); Alcove2C_SuperWire_Expansion / Alcove2C_Battery_Expansion 5.02 vs 4.20 (0.82 m). Either the furniture they rest on lost its collider in Rev C, or they now float. Needs a visual check by QA-03. Supersedes GEO-02's sink values.
