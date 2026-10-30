# Simple tier r3 netlist — Hatch Actuator D-204
Same board in all 5 candidates (only visual treatment differs). Geometry: `simple_r3_board_geom.json`.

| Ref | Silkscreen | Part | Pins |
|---|---|---|---|
| J1 | GRID POWER | hab grid feed | +, − |
| U1 | CONTROLLER | door controller | VIN, GND, outputs 1 / 2 / 3 |
| M1 | DOOR MOTOR | hatch actuator motor | IN, GND |
| TP1–TP3 | (pads at ends of 1/2/3) | output landing pads | 1 |
| GND1–GND3 | ⏚ symbols | ground ties, joined on bottom layer | 1 |

| Net | Nodes | Notes |
|---|---|---|
| GRID_V+ | J1.+ → U1.VIN | **intended open**: trace chunk missing + small burn mark (no spark) |
| GND | J1.− → GND1, U1.GND → GND2, M1.GND → GND3; GND1–GND2–GND3 on bottom layer | |
| OUT1 / OUT2 / OUT3 | U1.n → TPn | **intentional stubs**: each ends at a bare landing pad, leads nowhere |
| MOTOR_IN | M1.IN | **intentional no-connect**: player draws Super Wire from TPn/U1.n to M1.IN |

Series loop: J1.+ → (break) → U1 → OUTn →(player trace)→ M1.IN → M1 → GND → J1.−. Loop is open, so no current and nothing glows.
**Win:** break repaired AND player trace OUTn → M1.IN AND Python `MOTOR_PIN == n`. Window stays open until the player presses EXIT.
