# NAV / Egress QA pass r2 — QA-01 — 2026-11-01

Build: main @ 27a8e35, Godot 4.7.2, xvfb, after `godot --headless --import`. Harness outside repo (/tmp/qa01/h2.gd).
Method: one fresh Godot process (fresh scene) per door x side. Player placed 1.8 m from the door plane (setup
teleport only), then real input: mouse-yaw to face, [E] x2 (toggle check), [E] again if closed, hold W 300 frames.
No game code edited.

## Per-door results (fresh scene each)
| Door | Side | start | open0 | E1 | E2 | crossed | end |
|---|---|---|---|---|---|---|---|
| APT201 | + (gallery) | (-11.20,4.80,0.95) | closed | open | closed | NO* | (-11.20,4.08,0.95) |
| APT201 | - (apt) | (-11.20,4.80,4.55) | closed | open | closed | yes | (-11.37,4.08,1.66) |
| ALCOVE2C | + | (-11.50,4.80,-1.75) | closed | open | closed | yes | (-11.67,4.08,-4.64) |
| ALCOVE2C | - | (-11.50,4.80,-5.35) | closed | open | closed | yes | (-11.46,4.08,-2.48) |
| APT202 | + (gallery) | (7.80,5.28,0.95) | closed | open | closed | NO* | (7.80,5.29,0.95) |
| APT202 | - | (7.80,4.80,4.55) | closed | open | closed | yes | (7.63,4.08,1.68) |
| RM1A | + | (-8.51,0.55,1.35) | closed | open | closed | yes | (-8.72,0.00,3.92) |
| RM1A | - | (-8.50,0.60,4.65) | closed | open | closed | yes | (-8.67,0.00,1.76) |
| RM1B | + | (4.54,0.60,1.35) | closed | open | closed | yes | (4.59,0.00,3.88) |
| RM1B | - | (4.50,0.60,4.65) | closed | open | closed | yes | (4.33,0.00,1.76) |
| SECTOR4_EXIT | + | (0.00,0.60,-7.10) | closed | open | closed | yes | (-0.17,0.05,-9.97) |
| SECTOR4_EXIT | - | (0.00,0.60,-10.70) | closed | open | closed | yes | (0.04,0.00,-7.83) |

[E] toggles every door (open -> closed -> open), as coded in `_scan_rfid_doors`. Every door opens from both sides.
*Both gallery-side starts at z=0.95 on L2 never moved (APT202 start settled at y 5.28, i.e. on top of geometry).
In r1 the player walked through APT201 from the apartment side to the gallery fine, so this is likely the
start point landing on the gallery rail/edge, not the door. Logged as NAV-05.

## Status of r1 bugs
- NAV-01 (one-sided ground doors): NOT REPRODUCED. RM1A, RM1B, SECTOR4_EXIT open and cross from both sides. r1 was a toggle confound.
- NAV-02 (APT201 locks both sides): NOT REPRODUCED as a bug. A second [E] closes it, by design (toggle). UX note: no
  "press again to close" hint. Downgraded to UX observation.
- NAV-03 (ALCOVE2C won't open from inside): NOT REPRODUCED. Opens and crosses from (-11.50,4.80,-5.35).
- NAV-04 (tram end point unreachable): CONFIRMED. Start (10.2,0.5,-16.3), walking to (12.8,-16.6) stops at
  (10.26,0.33,-16.97) after ~0.7 m. r1 stopped at (11.97,0.34,-16.84). Something on the platform blocks eastward travel. minor -> major? kept minor: the game's own egress check passes.

## New bugs
### NAV-05 — minor (needs confirm) — Body placed at L2 gallery z=0.95 in front of APT201/APT202 can't move
Repro: put body at (-11.20,4.80,0.95) or (7.80,4.80,0.95), hold W toward the door: zero displacement over 300 frames.
APT202 case settles at y 5.28 (about 1 m above the 4.23 gallery deck). Probably a rail or collider top the player can
stand on. If a player can jump onto it, they could get stuck. Check colliders at gallery z~0.95.
### NAV-06 — minor — Wayfinding only on door headers, none on the route
Text check of scripts/preface_playable_area.gd: the only signage is 7 `_add_skinned_door_header_sign` lintels
(APT201, ALCOVE2C, APT202, RM1A, RM1B, Sector4Exit interior + exterior). APT/RM signs face the corridor only, none
inside the rooms. No directional signs at the L2 to ground stair/ramp junction (~9.7,-5.9), the plaza fork
(~2.9,-11.5), or the tram platform (~12,-16.6). No Label3D anywhere.

## Not covered (stopped short)
- D-204 hatch via the troubleshooting screen: not run. The screen is a modal circuit UI; driving it with real input
  needs its own harness. Deferred.
- Grid sweep of navigable points: tried a 6 m grid on 2 floors. It hit the 500 s timeout before printing, so no results.
  Re-run with a lighter per-point test.
- Usage was at 92.1% of the weekly limit at start, so I kept the pass short.
