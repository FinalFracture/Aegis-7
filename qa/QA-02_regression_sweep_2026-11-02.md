# QA-02 Regression Sweep — 2026-11-02 — PARTIAL SWEEP

**PARTIAL:** Jared's Windows machine (Grok Build CLI) was offline, so no new probe could be written. Per Jared, only the existing CLI-written probe `/tmp/qa02_round2_probe.gd` was re-run, unchanged. Anything it can't test is **BLOCKED pending the CLI**. M-70 (stairs) was skipped because it is on hold.

- Build: fresh clone of origin/main @ 48d3143 (contains ee10b2b), re-imported, Godot 4.7 headless, `--qa-placement`. No game code, assets or scripts were written or changed. Text only, no renders.
- Thresholds (3d-part-clipping-check): floor ±0.005 m, wall back gap 0–0.015 m, overlap ≤0.010 m.
- Usage: 4.5% before, 5.3% after the probe (cap 93%).

## M-item status
| Item | Result | Evidence |
|---|---|---|
| M-01 | PASS | Props 38/39/42/43 have 1 collider each; the capsule is blocked (Prop42 at 76%, others at 46% of a 1.2 m move) |
| M-08 | PASS | All 5 remaining pickups sit on *_Support colliders, delta 0.000 m. Apt201 Thermal_Jelly/Battery_Cell and the GEO-03 spool/headband are still absent |
| M-20 | PASS | 0 SeamFix nodes |
| M-21 | PASS | 6 hubs; Apt201 InductionRing top 4.200 vs Chevrons 4.2155 (separated) |
| M-38 | PASS | All 8 APT 201/202 corners pass at every height |
| M-39 | PASS | TalkPad 5.415 vs IntercomRing 5.418 (3 mm), 6 hubs |
| M-40 | PASS | 0 Open_Portal_Sector_Exit nodes |
| M-42 | BLOCKED | Probe doesn't measure the #55 bins or the Maintenance tool wall |
| M-43 | BLOCKED | Probe doesn't measure Task_Lamp_104/204 |
| M-44 | PASS (partial) | Prop42 is at x 5.492 (Maintenance E wall), z 0.15 front probe, with its collider present. Back gap not measured |
| M-61 | PASS | 64/68 pass. The 4 "fails" at (±10.10, -1.00) are the corners the table marks SKIP (convex-tip, open by design; 3c13c42); the old probe ignores that status field. All 62 closure corners pass, and 68/68 corner diagonals are blocked |
| M-62 | PASS | Corridor_L1 N open run is now x 2.7–3.7 (one door around x 2.2–4.2 once the capsule radius is added). The x 0.6/1.1–2.2 opening is gone. (GEO-13 withdrawn: the Maintenance side is the closed DOOR_RM1B force field) |
| M-64 | BLOCKED | Probe doesn't measure Lost_And_Found_Rail_Bins |
| M-65 | BLOCKED | Probe doesn't measure Task_Lamp_201 |
| M-66 | STILL OPEN (no change) | Wardrobe_101 mesh bottom y 0.220 vs floor 0.12 = 0.100 m float. Measured from the mesh AABB only; no floor ray |
| M-70 | SKIPPED | On hold |

## Other probe results
- Prop43: (-4.858, 0.12, 5.20) yaw -90, back gap 0.008 m (pass). Wardrobe_101 is now placed at x -13.9..-13.41, which doesn't overlap Prop43. The GEO-11 rect overlap (0.93 m2) is only against the old design rect x -5.1..-4.6.
- GEO-04 / M-10: still 3 coplanar decal layer pairs (open).
- GEO-09 / M-24: still "8 edge error(s)" at load (open).
- Capsule sweep: 2,662 samples, 125 open runs (22 runs >= 0.7 m, 103 slivers, mostly at rect ends where the probe meets the perpendicular wall). No open run on any outer or shared wall.

## New bugs
### GEO-13 — WITHDRAWN (was: Maintenance front doorway blocked from inside)
- **Withdrawn 2026-11-02:** the blocker is the closed DOOR_RM1B force field, which works as designed. Not a bug.
- Original note follows.
- In R2 the capsule cast outward (-Z) from z 1.36 along the Maintenance S edge was open over x 0.6–3.8. Now it's blocked over the whole edge, even at the design door x 2.2–4.2, while the corridor side (Corridor_L1 N, x 2.7–3.7) is open. So something on the Maintenance side of the door between z ~0.56 and 1.36 now blocks a 0.35 m-radius capsule. The probe doesn't name the collider. It could be a new threshold or wall piece from the M-62 fix, or a prop. This could block egress from Maintenance. Needs a collider ID → BLOCKED pending the CLI.

## BLOCKED pending the CLI (no probe exists)
- Gage: colliders with no matching visible mesh (extra colliders).
- Gage: props with no collider (only Props 38/39/42/43 are covered).
- Gage: buried props scene-wide (only the 5 pickups and Prop43 are covered).
- Scene-wide floating-prop scan, plus M-42, M-43, M-64, M-65 and the M-66 floor ray.
- Scene-wide mesh-vs-mesh clipping/overlap at ≤0.010 m.

---

# Part 2 — Collider / support sweep (2026-11-02 ~08:50 CT)

- Jared approved throwaway box probes. `/tmp/qa02probe/sweep3.gd` is not committed, and no repo code was touched. Fresh origin/main @ d1146b6, re-imported, Godot 4.7 headless, `--qa-placement`.
- Method:
  - Colliders vs meshes: every enabled CollisionShape3D's global AABB, taken from its shape debug mesh, is checked against all 4,006 visible mesh AABBs. A collider counts as orphaned when less than 25% of its volume is covered by any one mesh.
  - Props: the 1,034 direct children of InteractivePropsAndPickups and ExteriorPlacements_v1_3.
    - Collider check: an own CollisionObject3D, or any non-shell collider inside 80% of the prop AABB. Decals and quads under 2 cm tall are skipped.
    - Support check: 5 down-rays (centre plus 4 inset points) from 0.30 m above the mesh bottom, excluding the prop's own colliders. Highest hit = support. Buried means the bottom is more than 0.005 m below the support; floating means more than 0.005 m above it.
- Usage: 7.6% before.

## Results
| Check | Result |
|---|---|
| 1. Colliders with no visible mesh | **0 of 3,246** — pass |
| 2. Visible props with no collider | 12. 5 are pickups (no collider by design; each rests on its own *_Support collider). 6 are Ext_50 litter-drift decals 6.6–9 cm tall (fine to walk through). 1 is a real gap: GEO-15 |
| 3a. Buried (>0.005 m) | 70 hits. 69 are exterior ground pieces sunk into neighbouring ground colliders (GEO-14). 1 is the SectorRFIDForceFieldDoors container: mesh bottom 0.000 vs floor 0.120, which is the door hubs reaching below the 0.12 floor finish to the L1 slab at 0.0. Hidden, not filed |
| 3b. Floating | 19 hits, listed below |

### Floating cross-reference
| Item | Prop | Above support | Status |
|---|---|---|---|
| M-64 | Lost_And_Found_Rail_Bins (1.40, 0.12, 5.35) | +0.390 m (ExtGroundBody) | Still open |
| M-65 | Task_Lamp_201 (-13.2, 4.45, 5.6) | +0.215 m (RevC_Shell_L2_col) | Still open |
| M-66 | Wardrobe_101 (-13.65, 0.12, 5.75) | +0.100 m (ExtGroundBody) | Still open |
| M-71 | Apt201_ExBench_DustOutline (-12.05, 4.424, 7.65) | +0.224 m (RevC_Shell_L2_col) | Still open |
| M-72 | Potted_Plants_Rail_Cradles_102 (10.65, 0.12, 6.35) | +0.200 m (ExtGroundBody); no wall within the AABB footprint | Still open (floating) |
| GEO-16 | Ext_49 ts4_dead_foliage_1004, Ext_25 hydro_planter_tiered_exterior_1006 / _1007 (x -16.6, z 0 / -5 / 5) | +0.051 m | New |
| — | Ext_19 maglev_car_body_17 / _18 (21.15 / 8.85, -19.9) | +0.194 m over guideway | Not filed: maglev hover, assumed by design (Gage confirm) |
| — | Ext_47 desire_path_decal_1001 (+0.006), _1003 (+0.011) | decal offset | Not filed (z-fight offset; 1002/1003 coplanar stays M-10) |
| — | Ext_49 wear_decal_1005, Ext_50 litter 1008–1010 / 1011, Ext_51 track_scuff 1014 / 1015 | +0.005 m (at the limit) | Not filed |

## New bugs (Part 2)
### GEO-14 — Exterior ground pieces sunk into neighbouring ground colliders (Low, Gage)
- 69 props have their mesh bottom below the top of a neighbour's ExtCollision trimesh:
  - Ext_46 canal_edge ×42: -0.057 m
  - Ext_44 paving_promenade ×17: -0.052 to -0.250 m (6 at -0.250)
  - Ext_0 platform_infill and Ext_45 kerb_ramp: -0.052 m
  - Ext_41 curbs ×7: -0.006 m; curb_segment_809mm: -0.015 m on ExtGroundCol
- The tops render and the bases are hidden, so the risk is z-fight or seams where the top faces land within 1 mm of each other (the overlap limit is 0.010 m). Check the 6 paving pieces at -0.250 first: a 0.25 m step can make the walk surface uneven. Probably stacked ground layers; confirm which ones are intended.
### GEO-15 — Ext_49 ts4_dead_foliage_1004 has no collider (Low, Gage)
- At (-16.6, 0.17, 0.0), AABB 0.41 × 0.69 × 4.0 m. No own collider and no other collider in its footprint, so the player walks through a 0.69 m-tall, 4 m-long planting strip. Its neighbours, the hydro planters 1006/1007 (same footprint), do have colliders.
### GEO-16 — Exterior planting strips float 0.051 m (Low, Gage)
- Ext_49 ts4_dead_foliage_1004 and Ext_25 hydro_planter_tiered_exterior_1006 / _1007: mesh bottom 0.171 vs ExtGroundBody 0.120 (limit 0.005). They look placed for the curb-top datum 0.171 but sit off the curb, over plain ground.
