# Tutorial-tier netlist — Hatch Actuator D-204 (first door)
Simplified, still electrically true. Advanced tier = `design/ui/troubleshoot_final/hatch_actuator_d204_netlist.md`.

| Ref | Player label | Part | Pins |
|---|---|---|---|
| B1 | BATTERY | 7 V pack | +, − |
| U1 | CONTROL BOX | door controller | PWR, GND, PIN 3 (door icon) |
| M1 | DOOR MOTOR | hatch actuator motor | 1, 2 |
| TP1 / TP2 | wire spots A / B | test points either side of the crack | 1 |

| Net | Nodes |
|---|---|
| BAT_PLUS | B1.+ → U1.PWR |
| DOOR_PWR | U1.PIN3 → TP1 ~~crack~~ TP2 → M1.1 |
| GND | B1.− → U1.GND → M1.2 |

**Fault:** DOOR_PWR cracked between TP1 and TP2 (the only open). Power glows from the battery through the control box to the crack; everything after it is dark.
**Fix 1 (board):** drag Super Wire TP1 → TP2. **Fix 2 (code):** `door_motor_pin = 4` → `3` (matches the PIN 3 label). Door light turns green.
