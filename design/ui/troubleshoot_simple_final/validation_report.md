# Simple tier FINAL — validation report
Validator: `tools/pcb_validate.py` on `simple_final_board_geom.json` (mockup and board-only render the same geometry).

## Result: PASS
- 5 nets, 12 pads, 0 vias, 8 traces / 10 segments, 2 bends (45°), two layers (GND tie on bottom)
- Errors: 0
- Expected opens: OUT3: expected open between ['FE1.IN'] and ['U1.P3']
- Intentional no-connects: U1.P1 (OUT1): intentional no-connect; U1.P2 (OUT2): intentional no-connect
- Break moved to mid-trace (px 814-886); nearest silkscreen outline 64px away. Pads moved inside component edges: pad-edge to outline gap 7.5 px for every component pin (≥3 px required); details in README.
