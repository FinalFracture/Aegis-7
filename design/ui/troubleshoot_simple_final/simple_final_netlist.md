# Simple tier FINAL netlist — Hatch Actuator D-204
From r3 #03 holo_panels. Geometry: `simple_final_board_geom.json`.

| Ref | Silkscreen | Part | Pins |
|---|---|---|---|
| J1 | GRID POWER | hab grid feed | +, − |
| U1 | CONTROLLER | door controller | VIN, GND, P1 / P2 / P3 (silk 1 / 2 / 3) |
| M1 | DOOR MOTOR | hatch actuator motor | IN, GND |
| TP1, TP2 | — | bare landing pads | 1 |
| GND1–GND3 | ⏚ | ground ties, joined on bottom layer | 1 |

| Net | Nodes | Notes |
|---|---|---|
| GRID_V+ | J1.+ → U1.VIN | intact |
| GND | J1.− → GND1, U1.GND → GND2, M1.GND → GND3; GND1–GND2–GND3 bottom layer | |
| OUT1 / OUT2 | U1.P1 → TP1, U1.P2 → TP2 | **intentional stubs**, lead nowhere |
| OUT3 | U1.P3 → M1.IN | **intended open**: trace chunk missing + subtle burn near M1.IN |

Series loop J1.+ → U1 → P3 →(break)→ M1.IN → M1 → GND → J1.− is open: no current, traces are uniform unlit neon.
**Win:** repair the OUT3 break AND set `MOTOR_PIN = 3` (default 1). Window stays open until EXIT.
