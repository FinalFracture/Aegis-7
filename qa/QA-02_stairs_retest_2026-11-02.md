# QA-02 Stairs Retest (M-70) — 2026-11-02 late

- Tested: fresh origin/main @ 2ecba00, which contains 5d8a9d9 (stairs + colliders placed) and 88e3c68 (EastStairRampConnector removed). Re-imported, Godot 4.7 headless, `--qa-placement`. Main later moved to 56a9f39 (QA-01 report only).
- Probe: throwaway `/tmp/qa02probe/stairs.gd`, deleted after the run and never committed.
  - Probe body copied from PlayerBody: capsule r 0.35, h 1.75, mask 1, max floor 50°, snap 0.35, 3 m/s, gravity 9.8.
  - All RFID fields opened via `_nav_qa_set_fields(true)`. Sweep casts start 0.45 m in from the wall faces.
- Usage: 16.7% at start, 17.3% after the probe (stop line 92%).

## Status
| # | Check | Status | Evidence |
|---|---|---|---|
| 1 | Stair colliders: gaps / overlaps / walkability | **PASS** (2 Low notes: GEO-19, GEO-20) | 4 ramp/landing colliders: Flight1_Ramp, Mid_Landing, Flight2_Ramp, L2_Landing (all `-colonly` trimesh), plus 18 guard-glass hulls. Down-ray profile, 5 cm steps at x ±0.70/±1.15/±1.60: flight 1 rises 0.12→2.58 over z -2.9..-7.5 (~29°); mid landing 2.58 at z -7.5..-8.9; flight 2 rises 2.58→4.20 over z -7.7..-4.9 (~29°); no holes along either flight. Ramps-only colliders, so the effective rise per step is 0 and the slope is 29° < 50° max floor. **Walk up:** L1 (-1.15, -0.2) → mid landing feet y 2.585 → L2 feet y 4.20, reaching (1.15, 4.08, 0.43). **Walk down:** L2 → mid landing → L1 (-1.15, 0.00, -0.38). Both reach the end with no snag. One 5 cm sample at z -0.80 reads 0.12 (seam between the L2 slab edge and L2_Landing); the capsule isn't affected |
| 2 | Capsule sweep around the stair core (doors open, 0.45 m inset) | **PASS** | StairCore / Corridor_L1 / Corridor_L2: 500 samples, 13 open runs, all at doors or the designed stair-core / corridor openings (StairCore N 2.8 m, corridor S 3.0 m on L1 and L2). No open run on any core wall |
| 3 | L2 edge at x 1.55 (NAV-08) | **PASS** — no fall, a guard exists | NAV-08 gallery walk (-11.5, 4.4, 1.6) → (6.5, -2.5) ends on L2 at (1.55, 4.08, -1.18). Walks toward the core from 6 x positions (-1.6..2.3) and 8 side angles all stay on L2 (y 4.07–4.08). The stairwell edge at z -4.84 is guarded by Guard_Glass_13..17 (y 4.26–5.26). No extra guard needed. QA-01 56a9f39 also closed NAV-08 |
| 4 | GEO-18 (stair GLBs not in scene) | **RESOLVED** | `StairSetSwitchback` and `StairGuardHandrail` are under SectorArchitecture at runtime (STAIR_SET_GLB / STAIR_GUARD_GLB in preface_playable_area.gd) with 4 + 18 colliders |
| 5a | GEO-17 SE corner (13.50, 0.05, -8.55) | **Still open (partial)** | Wedges at (13.55, 0.05, -8.55). Escape 1/4: +Z moved 2.80 m; -X 0.22 m (counts as stuck); +X and -Z 0.00 m. Better than last round's 0/4, but the player still pins and can only back out the way they came |
| 5b | M-73 NW corner (-13.55, 0.05, -8.55) | **Still open** | Wedges at (-13.55, 0.05, -8.55). Escape 0/4 (0.00 m every way) |

## New bugs
### GEO-19 — Mid landing collider runs into the Sector-4 exit portal header/jambs (Low, Gage/Rook)
- Mid_Landing-colonly (x -1.9..1.9, y 2.335–2.585, z -8.9..-7.4) overlaps PortalHeaderCollider (y 2.45–2.83, z -9.15..-8.85) by 0.05 m (z) × 0.135 m (y) across 2.6 m. It also overlaps PortalJambCollider_L/R by 0.05 m (overlap limit 0.010 m).
- The 2.33 m landing underside clears the 1.87 m capsule, so egress isn't blocked. But the landing's north edge sits inside the exit portal header, which is a visual/collision clip at the portal.
### GEO-20 — Duplicate guard collider at the L2 stairwell edge (Low, Gage)
- The old MezzanineGlassBalustrade_L2Edge box (x -1.89..0.37, y 4.26–5.30, z -4.86..-4.80) sits on the same line as the new Guard_Glass_13..17 hulls (z -4.836..-4.824). Their AABBs overlap fully along 2.26 m.
- Walking isn't affected, but the old balustrade's visible glass (if any) may coplanar-fight with the new guard glass. Check whether the old balustrade should be removed now that 5d8a9d9 places the Rev C guard.
