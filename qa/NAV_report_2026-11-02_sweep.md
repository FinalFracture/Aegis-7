# NAV sweep — QA-01 — 2026-11-02

Build: main @ ee10b2b (rebased onto fe60420 before commit). Godot 4.7.2, `--headless --fixed-fps 60`, after `--import`.
Harness outside repo (/tmp/qa01/sweep.gd, verify*.gd). Boot flag `--qa-placement` (the only headless boot flag that doesn't
start an in-game QA runner or validate-and-quit). Real input: KEY_W / KEY_SPACE / mouse-yaw through `Input.parse_input_event`.
Doors forced open in the walk tests so the route stays open. Stairs skipped (M-70 on hold): x 7..12.5, z -8.5..-0.5.
No game code edited.

## Coverage
- Grid sweep: 1 m grid, x -16..16, z -20..10, dropped from y 0.6 (L1/outdoor) and y 4.8 (L2): 1966 points tested
  (stairs box excluded). Per point: settle 24 frames, then W 14 frames in 4 yaw directions. Output is printed per point.
  Result: L1 pass 585 / snag 188 / trapped 210; L2 pass 658 / snag 247 / trapped 78; 0 fall-outs below y -1.
  Most trapped/snag points are teleports into walls or props (wall lines z=±1, ±9; prop AABBs), so they are not bugs by
  themselves. Every candidate was re-checked by walking in from a reachable point with real input (below).
- Walk tests (real input, from reachable points): 19 routes. RM1A, RM1B, APT201, APT202 and ALCOVE2C interior loops,
  L1 corridor loop, L2 gallery loop, gallery edges W/E, 4 L1 corners, plaza perimeter, tram platform, tram south edge.

## Re-checks
- NAV-04 (tram end point): CONFIRMED, worse than before. Walking from (10.20,0.31,-16.30) toward (12.8,-16.6) stalls at
  (9.98-10.48,0.33,-16.89..-17.00). Escape: 0/4 directions, and the only contact is floor ExtCollision#ExtShape_1, normal +Y.
  The player is TRAPPED on the tram platform deck. Raised to MAJOR. Likely an edge or seam catch in the platform floor shape.
- NAV-05 (L2 gallery z=0.95): NOT REPRODUCED as a stuck spot. Walking out from APT201/APT202 stops cleanly at z=1.35 on
  RevC_Shell_L2_col#CollisionShape3D (the gallery wall), and 3/4 escape directions work. r2 was a teleport artifact
  (z=0.95 is inside the wall).

## New bugs
### NAV-07 — MAJOR — L1 NW corner wedge trap
Repro: start (-12.0,0.0,-7.0), hold W toward (-14.3,-9.3). The player wedges at (-13.55,0.06,-8.55).
Escape 0/4 directions, and jump+W does not free them. Collider: RevC_Shell_L1_col#CollisionShape3D (contacts n=(1,0,0) and
(0,0,1), two shell faces). The other three L1 corners (NE 13.36,-8.55; SW -13.55,8.55; SE 13.55,8.55) block the walk but
allow escape (3/4).
### NAV-08 — MAJOR — Fall from L2 into L1 near x 1.55, z -1.26
Repro: start on the L2 gallery (-11.5,4.08,1.6), hold W toward (6.5,-2.5). The player follows the gallery wall east, then
drops below y 3.9 at (1.55,3.90,-1.26) and lands on L1 at (1.55,0.00,-1.96) against RevC_Shell_L1_col (n=-X).
No fall-out of the world, but there's an unguarded 4 m drop off L2. Missing guardrail/collider at the L2 edge near x 1.5.
Reverse direction (from 6.0,4.08,1.6 westward) stops at (2.59,4.08,1.09) on RevC_Shell_L2_col n=(0.96,0,0.27), no fall.
So the gap is on one side only.
### NAV-09 — MAJOR — Tram platform south edge trap
Repro: start (8.0,0.06,-16.0), hold W toward (8.0,-19.5). The player stops at (8.51,0.17,-18.24), escape 0/4.
Collider: ExtCollision#ExtShape_5 (n=(0,0,1), platform edge/guideway face). The player can't walk back onto the platform.
### NAV-10 — minor — Tram roof stands like a floor
Grid drops at y 4.8 over x 3..16, z -19..-20 land at y ~3.98-4.05 on TramRoofNoStand#TramRoofNoStand_Shape (SNAG1-3)
instead of sliding off. Drops at y 0.6 there settle at y ~1.70 (trapped, TramRoofNoStand contacts) inside the car volume.
Not reached by walking in this pass. Only an issue if the roof is reachable by jump. The name says no-stand, but
it stands.
### NAV-11 — minor — Plaza SW corner snag
Walking from (-12,0.06,-11) to (-14,-18) arrives, then heading to (2,-19) stalls at (-13.92,0.06,-17.95) on ExtCollision#ExtShape_2
(floor contact only). Escape 3/4 works, so it's a snag, not a trap.
### NAV-12 — minor — RM1B north/east interior unreachable from the west half
RM1B loop: (1.5,4.5) -> (1.5,8.5) blocked by PropAabbBody#@CollisionShape3D@54 at (1.47,0,4.34). East wall stops at x 5.55
(RevC_Shell_L1_col) both at z 7.87 and 5.12. The prop AABB box closes the west aisle. Check the prop @54 AABB size.
(APT201 west wall has a similar prop block, PropAabbBody@60 at (-13.55,4.08,3.93), but that loop still completes another way.)

## Not covered
- D-204 hatch: not run. It opens through the modal troubleshoot UI; driving it needs its own harness, so it wasn't cheap.
- Stairs (M-70) skipped on purpose.
- Doors themselves are covered in r2 (all open both sides).
