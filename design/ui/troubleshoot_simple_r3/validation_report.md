# Simple tier r3 — validation report
Validator: `tools/pcb_validate.py` (extended, backward compatible: optional `intentional_unconnected`) on `simple_r3_board_geom.json`. Board + silkscreen identical to r2 #01 in all 5 candidates; only the holo frame/chrome strength differs (light frame -> heavy projection). Circuit art unchanged from r2.

## Result: PASS
- 6 nets, 15 pads, 0 vias, 10 traces / 10 segments, 0 bends, two layers (GND tie on bottom)
- Errors: 0
- Expected opens: GRID_V+: expected open between ['J1.+'] and ['U1.VIN']
- Intentional no-connects: M1.IN (MOTOR_IN): intentional no-connect
- OUT1/OUT2/OUT3 stubs end on landing pads TP1–TP3 (pad-to-pad, so no dead-end errors); flagged intentional in the netlist.
- Regression: troubleshoot_final geometry still PASS (17 nets / 62 pads), tutorial r1 geometry still PASS.

| Candidate | Nets | Pads | Errors |
|---|---|---|---|
| 01 | 6 | 15 | 0 |
| 02 | 6 | 15 | 0 |
| 03 | 6 | 15 | 0 |
| 04 | 6 | 15 | 0 |
| 05 | 6 | 15 | 0 |
