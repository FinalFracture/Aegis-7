# Prop43 Spares Dispenser: new location (Vance, 2026-11-01)

West Storage's north wall no longer has a clear 1.9 m run after Rook's SeamFix walls (placement fails on clearance, mesh_clearance and front_zone).

**New spot: Side_Room_East_Lounge (Room 1A), north wall (inner face z 8.76).**
- Lounge interior is x -12.10..-4.90 (7.2 m run). The dispenser takes the west end: footprint x -8.95..-7.05 (rev 2: moved east of the built-in lounge counter at about x -10.5, z 7.86).
- `position = Vector3(-8.00, 0.235, 8.50)`, `yaw = 180.0` (local -Z onto world +Z, back to the north wall). The z of 8.50 keeps the same 0.26 m pivot-to-back offset as the current -X mount (8.10 - 7.84).
- Clear of: spool at (-6.15, 7.25), lounge light (-8.20, y 3.62), Apt201 slab above (y > 4.0, the dispenser is under 4.0 tall), and the door wall at z 3.00.
- Front zone: x -8.95..-7.05 by z 7.3..8.5 must stay empty.
- Gage: update `ANIMATED_PROP_SPECS` Prop43 and rerun placement_assert. If the wall check fails, nudge z by ±0.01, not x.

## Rev 3 (supersedes the north-wall spots)
Measured the lounge GLB: the north wall run is broken by built-in furniture at x -11.24..-10.16, -8.79..-7.36 and -6.80..-5.50, so it has no clear 1.9 m stretch. The east SeamFix wall (inner face x -4.90) is clear from z 3.05 to 6.45.
- `position = Vector3(-5.16, 0.235, 5.20)`, `yaw = -90.0` (same mount as the old West Storage x 8.10 placement, back to the wall, facing -X).
- Footprint z 4.25..6.15. Front zone x -6.4..-5.16, z 4.25..6.15 is clear (nearest furniture starts at z 6.5).


## Code vs design (2026-11-01)
- Code on main (04bbed0): `Vector3(-4.858, 0.12, 5.20)`, yaw -90, room 101 east wall (Rev C partition face x -4.6).
- Design rev3: `(-5.16, 0.235, 5.20)`, yaw -90.
- MISMATCH: x 0.30 m, y 0.115 m (code follows the Rev C wall/floor). Tracked in M-02; footprint may overlap the unplaced 101 wardrobe rect.
