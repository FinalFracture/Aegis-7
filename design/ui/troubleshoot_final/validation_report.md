# Troubleshoot UI final (r3 #02 balanced_twolayer) — PCB art validation report

Validator: `tools/pcb_validate.py` (union-find connectivity over pads/vias/traces/GND pours; shorts; stubs; unconnected pads; same-layer clearance >= 0.25 grid; 45-degree bends only, no acute angles).
Netlist: `hatch_actuator_d204_netlist.json` (R1/R2 divider removed; LM2596-3.3 FB pin senses V3V3 directly).

## Result: PASS
- Grid 89x31, via cost 6, GND pour on bot
- 17 nets, 62 pads, 3 vias, 49 traces / 116 segments, 67 bends, 1304 pour cells
- Errors: 0
- Expected opens: RESET_N: expected open between ['J4.3', 'TP1'] and ['R3.2', 'TP2', 'U2.RESET_N']
