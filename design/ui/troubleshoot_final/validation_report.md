# Troubleshoot UI final (r3 #02 balanced_twolayer) — PCB art validation report

Validator: `tools/pcb_validate.py` (union-find connectivity over pads/vias/traces/GND pours; shorts; stubs; unconnected pads; same-layer clearance >= 0.25 grid; 45-degree bends only, no acute angles).
Netlist: `hatch_actuator_d204_netlist.json` (R1/R2 divider removed; LM2596-3.3 FB pin senses V3V3 directly).

## Result: PASS
- Grid 89x31, via cost 6, GND pour on bot
- 17 nets, 62 pads, 3 vias, 49 traces / 116 segments, 67 bends, 1304 pour cells
- Errors: 0
- Expected opens: RESET_N: expected open between ['J4.3', 'TP1'] and ['R3.2', 'TP2', 'U2.RESET_N']

## Rev: force-field door (2026-10-30)
- J2 is now EMITTER (the force-field emitter connector), U3 is described as the field-emitter driver, and the title reads Hatch Field Emitter D-204.
- Nets were renamed VMOT_IN/VMOT → VFLD_IN/VFLD and MOT_IN1/2 → DRV_IN1/2. The routed geometry is byte-identical apart from the names.
- Re-validated: PASS, 17 nets / 62 pads / 0 errors, with the same single expected open (RESET_N).
