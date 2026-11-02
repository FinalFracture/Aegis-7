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
| M-62 | PASS | Corridor_L1 N open run is now x 2.7–3.7 (one door around x 2.2–4.2 once the capsule radius is added). The x 0.6/1.1–2.2 opening is gone. See GEO-13 for the Maintenance side |
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
### GEO-13 — Maintenance front doorway blocked from inside (Med, Gage; candidate)
- In R2 the capsule cast outward (-Z) from z 1.36 along the Maintenance S edge was open over x 0.6–3.8. Now it's blocked over the whole edge, even at the design door x 2.2–4.2, while the corridor side (Corridor_L1 N, x 2.7–3.7) is open. So something on the Maintenance side of the door between z ~0.56 and 1.36 now blocks a 0.35 m-radius capsule. The probe doesn't name the collider. It could be a new threshold or wall piece from the M-62 fix, or a prop. This could block egress from Maintenance. Needs a collider ID → BLOCKED pending the CLI.

## BLOCKED pending the CLI (no probe exists)
- Gage: colliders with no matching visible mesh (extra colliders).
- Gage: props with no collider (only Props 38/39/42/43 are covered).
- Gage: buried props scene-wide (only the 5 pickups and Prop43 are covered).
- Scene-wide floating-prop scan, plus M-42, M-43, M-64, M-65 and the M-66 floor ray.
- Scene-wide mesh-vs-mesh clipping/overlap at ≤0.010 m.
