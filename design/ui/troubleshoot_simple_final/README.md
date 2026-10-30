# Troubleshoot — simple tier FINAL (Hatch Actuator D-204)
Source: simple r3 #03 holo_panels, picked by Jared with changes.

- **Board:** green PCB and off-white silkscreen from r2/r3, inside the cyan/amber wrist-holo frame (#03 chrome level).
- **Traces:** uniform blue neon. There is no current-flow animation and no brightness variation, so lit versus unlit doesn't hint at anything.
- **Fault:** the U1 pin 3 → M1.IN (DOOR MOTOR input) trace has a missing chunk and a subtle burn, with no spark. GRID POWER → U1.VIN is intact. Pins 1 and 2 are bare stubs.
- **Python:** the only editable value is `MOTOR_PIN` (amber entry box, default 1, correct 3).
- **Decision: no RUN button.** The value applies when the player commits the entry box, by pressing Enter or leaving the field (focus-out). DUTY was removed.
- **Win:** repair the break AND set `MOTOR_PIN = 3`. The window never auto-closes; it closes only on EXIT.
- **No hints:** consumables show as icons with quantities only.

Files: `troubleshoot_simple_final_mockup.png`, `troubleshoot_simple_final_board_only.png`, `simple_final_netlist.json/.md`, `simple_final_board_geom.json`, `validation_report.md`.
