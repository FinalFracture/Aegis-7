# Tutorial tier r1 — validation report
Validator: `tools/pcb_validate.py` on the tutorial netlist geometry (same board in all 5 candidates; only overlays/guidance differ).

## Result: PASS
- 3 nets, 9 pads, 0 vias, 7 traces / 9 segments, 2 bends
- Errors: 0
- Expected opens: DOOR_PWR: expected open between ['M1.1', 'TP2'] and ['TP1', 'U1.PIN3']
