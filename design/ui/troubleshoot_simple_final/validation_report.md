# Simple tier FINAL — validation report
Validator: `tools/pcb_validate.py` on `simple_final_board_geom.json` (mockup and board-only render the same geometry).

## Result: PASS
- 5 nets, 14 pads, 0 vias, 10 traces / 12 segments, 2 bends (45°), two layers (GND tie on bottom)
- Errors: 0
- Expected opens: OUT3: expected open between ['M1.IN'] and ['U1.P3']
- Intentional no-connects: none (M1.IN flag removed; it is on OUT3)
- OUT1/OUT2 stubs end on bare pads TP1/TP2 (pad-to-pad), declared intentional in the netlist.
