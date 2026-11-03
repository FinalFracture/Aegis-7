# QA-02 Corner-Fix Retest (GEO-17 / M-73) — 2026-11-03

- Tested: fresh origin/main @ 248257d (contains 248257d). Re-imported, Godot 4.7 headless, `--qa-placement`.
- Probes: throwaway, in /tmp, deleted afterwards, never committed. Probe body copied from PlayerBody: capsule r 0.35, h 1.75, mask 1, max floor 50°, snap 0.35, 3 m/s. All RFID fields opened via `_nav_qa_set_fields(true)`.
- Usage: 19.8% at start (stop line 92%).

## 1. Escapes (4 directions × 1.5 s at 3 m/s; escaped = moved > 0.5 m)
Each spot was tested twice: placed directly, and walked in diagonally from 1.5 m away.
| Spot | Placed | Walked in | Blocked directions | Verdict |
|---|---|---|---|---|
| SE (13.50, 0.05, -8.55) | 2/4 | 2/4 | +X (east shell wall), -Z (north shell wall) | **PASS**: both blocked directions are solid walls. -X and +Z move 2.80 m. Was 1/4 |
| NW (-13.55, 0.05, -8.55) | 2/4 | 2/4 | -X (west wall), -Z (north wall) | **PASS**: +X and +Z move 2.80 m. Was 0/4 |
| NW snag (-11.53, 0.05, -8.55) | 3/4 | 3/4 | -Z (north wall) | **PASS**: +X 2.80, -X 2.00, +Z 2.80 m |
- 4/4 isn't possible at a wall corner, so 2/4 at a corner and 3/4 along a wall is the maximum. GEO-17 and M-73 are **fixed**.

## 2. Capsule sweep along z -8.90 (x -13.45..13.45, 0.1 m step, L1 and L2, casts 0.45 m off the wall, 0.9 m)
| Level | Inside → out (from z -8.45) | Outside → in (from z -9.35) |
|---|---|---|
| L1 | 22/270 open: x -0.85..0.85 (Sector-4 exit door, open) + x ±1.95..2.05 | 18/270 open: x -0.85..0.85 (exit door) only |
| L2 | 8/270 open: x -0.15..0.15 (stair slot window, RevC_Window_Stair_Slot_Glass) + x ±1.95..2.05 | 4/270 open: x -0.15..0.15 only |
- The x ±1.95..2.05 samples sit inside the solid 103|StairCore and 104|StairCore partition walls (x ±1.9..2.1). A ray inside that wall touches no face, so the cast is a probe artifact. A real player can't get there.
- Real walks from 103/104 (x ±3.0) and from the stair core (x ±1.4) toward x ±2.0 and then north to z -10.5 all stop inside: x ±2.45 / ±1.55, z -8.55, on L1, L2 and the mid landing.
- Outside-in walks every 1 m from z -10.0 toward the shell (x -13.5..13.5): only x ±0.5 enter, through the open Sector-4 exit door (by design).
- **PASS**: no new gap through the shell along z -8.90 in either direction.
- The L2 slot x -0.15..0.15 is open to a 0.35 m capsule only by cast (centre samples in the window slot). It isn't walkable: L2 at z -8.45 is the stair-core void above the mid landing. Not filed.

## 3. GEO-14 along the z -8.90 line
- Scene-wide sunk ground pieces: 72 (71 last round; within probe sampling noise).
- Along z -9.6..-8.0, 3 paving pieces are still sunk: Ext_44_ext_paving_promenade_533 / _537 at -0.202 m, _556 at -0.111 m. Previously the worst paving was -0.250 m. The trim reduced the depth near the shell but didn't clear it. **GEO-14 still open**, slightly better on this line.

## New bugs
None (GEO-21 not used).
