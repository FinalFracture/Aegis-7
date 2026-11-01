# NAV / Egress QA pass — QA-01 — 2026-11-01

Build: main @ 39eba42, Godot 4.7.2.stable, xvfb-run, scene `res://scenes/preface/preface_playable_area.tscn`.
Harness: external SceneTree script (/tmp/qa01/harness.gd, not in repo). Input via `Input.parse_input_event`
(KEY_W hold, KEY_E scan, mouse-motion yaw with `_qa_hand=true`). Door tests teleport the body 1.8 m
either side of each door plane as setup only, then use real input. Stuck = <0.15 m moved over 3x30 physics frames.
No game code edited. Fresh clone needed `godot --headless --import` first (class_name cache).

## Egress route (spawn -> tram) — 17/18 waypoints PASS
Spawn (-9.35,4.34,6.20) -> APT201 door (opened, ff=open) -> L2 gallery (-8.31,4.23,1.42) -> (7.01,4.23,1.99)
-> (10.13,4.22,-1.35) -> stair/ramp down (9.60,2.69,-5.16) (9.49,0.93,-6.67) -> concourse (3.99,0.12,-7.69)
-> SECTOR4_EXIT (opened) -> (0.12,0.17,-9.07) -> plaza (2.24,0.05,-11.07) (8.55,0.05,-15.25)
-> kerb/platform (9.49,0.31,-15.98) (11.67,0.31,-16.34) -> STUCK (11.97,0.34,-16.84).
No falls through geometry: min Y over whole run 0.05 (plaza deck).

## Door both-sides matrix (+ = side along door +Z basis)
| Door | + side | - side |
|---|---|---|
| DOOR_APT201 | no open, stuck (-10.79,4.23,2.28) | no open, stuck (-11.01,4.35,3.20) |
| DOOR_ALCOVE2C | open, crossed | no open, stuck (-11.00,4.23,-4.00) |
| DOOR_APT202 | open, crossed | open, crossed |
| DOOR_RM1A | no open, blocked (-8.85,0.12,2.40) | open, crossed |
| DOOR_RM1B | no open, stuck (3.98,0.12,2.40) | open, crossed |
| DOOR_SECTOR4_EXIT | no open, stuck (-0.60,0.16,-8.45) | open, crossed |

CAVEAT: [E] appears to toggle door state and tests ran sequentially on a persistent scene (APT201 and
SECTOR4_EXIT were already opened by the egress walk). Some "no open" results may be a second [E] closing
an already-open field rather than a one-way door. Needs a re-run with a fresh scene per door side.

## Bugs
### NAV-01 — major (needs confirm) — Ground-floor doors only open from one side
RM1A, RM1B, SECTOR4_EXIT: scan from corridor/+ side at 1.8 m, facing door, [E] -> ff=locked, walk blocked.
Same doors open fine from the - side. Repro: stand at (-8.38,0.60,0.63) facing +Z, press E, hold W.
Coords: RM1A (-8.85,0.12,2.40), RM1B (3.98,0.12,2.40), SECTOR4 (-0.60,0.16,-8.45). Possibly toggle confound.
### NAV-02 — major (needs confirm) — DOOR_APT201 re-scan locks it from both sides
After egress opened APT201, scans from both sides returned locked; player stuck at (-10.79,4.23,2.28) /
(-11.01,4.35,3.20). If [E] toggles, a player who presses E twice locks themselves in/out with no feedback.
### NAV-03 — major (needs confirm) — DOOR_ALCOVE2C won't open from inside alcove
From (-11.52,4.99,-5.16) facing +Z, [E] -> locked; stuck (-11.00,4.23,-4.00). Opened from gallery side.
### NAV-04 — minor — Tram platform end point unreachable
Final egress waypoint (12.8,-16.6): player halts at (11.97,0.34,-16.84) ~0.85 m short (on deck, y 0.34),
something blocks at the platform edge/shelter. In-game egress QA criterion (<=1.5 m, y>=0.25) still passes.

## Not covered
Hatch D-204 field gate (needs troubleshoot UI flow), wayfinding/signage (text-only pass, no renders),
full unreachable-area sweep beyond the route + doors.
