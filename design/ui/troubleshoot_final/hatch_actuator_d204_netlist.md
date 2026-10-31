# Hatch Field Emitter D-204 controller — schematic / netlist (art reference)

Source of truth for the troubleshoot UI board art (final). Machine-readable: `hatch_actuator_d204_netlist.json`. Every trace in the r3 mockups is routed from this netlist and checked by `validation_report.md`.

## Power path
- **J1** 2-pin input, 7 A supply (`VFLD_IN`) → **F1** 7 A fast fuse → `VFLD` emitter supply rail.
- **C5** 470 µF/35 V bulk electrolytic on `VFLD` (the scorched part in the fault).
- **U1** LM2596-3.3 async buck: `VFLD` → `SW_NODE` → **L1** 33 µH → `V3V3`; **D1** SS54 Schottky catch diode SW_NODE→GND; **C1** 22 µF input, **C2** 220 µF output. Fixed 3.3 V part: **U1.FB senses `V3V3` directly** (R1/R2 divider removed).
- **U3** DRV8871 H-bridge on `VFLD`, outputs `OUT1`/`OUT2` → **J2** field-emitter connector.

## Logic
- **U2** AEGIS-MCU-32 on `V3V3`; **C3**/**C4** 100 nF decoupling placed directly at VDD1/GND1 and VDD2/GND2.
- `DRV_IN1`/`DRV_IN2`: U2.PB0/PB1 → U3.IN1/IN2.
- **J4** service header: pin 1 GND, pin 2 `LOCK_HOLD` (U2.PA4), **pin 3 `RESET_N`** (U2.RESET_N, **R3** 10 k pull-up, test points **TP1**/**TP2**), pin 4 `AUX_BUZZ` (U2.PA5).
- **S1** limit switch to GND on `LIMIT_SW` (U2.PA3) with **R4** 10 k pull-up; low = hatch closed.
- **D2** green STATUS LED via **R5** 330 Ω (U2.PB6); **D3** amber FAULT LED via **R6** 330 Ω (U2.PB7).

## Intentional fault (gameplay)
- Stage 1: C5 scorched (VFLD bulk); `RESET_N` trace cracked between TP1 and TP2. Super Wire points SW1 = TP1, SW2 = TP2, SW3 = R3.2. Fix: bridge SW1→SW2.
- Stage 2: Python bug `J4_RESET_N = 4` (that is AUX_BUZZ); correct is 3.

## Components
| Ref | Value | Description | Pins |
|---|---|---|---|
| J1 | 7A IN | 2-pin supply input, 7 A | 1, 2 |
| F1 | 7A | Blade fuse 7 A fast | 1, 2 |
| C5 | 470uF 35V | VFLD bulk electrolytic | 1, 2 |
| C1 | 22uF 35V | Buck input cap | 1, 2 |
| U1 | LM2596-3.3 | Async buck regulator 3.3 V / 3 A | VIN, GND, SW, FB |
| D1 | SS54 | Schottky catch diode 5 A 40 V | 1, 2 |
| L1 | 33uH 3A | Buck inductor | 1, 2 |
| C2 | 220uF 10V | Buck output cap | 1, 2 |
| U2 | AEGIS-MCU-32 | Door controller MCU | VDD1, GND1, PA5_AUX, RESET_N, PA4_LOCK, PB6_LSTAT, VDD2, GND2, PB0_IN1, PB1_IN2, PA3_LIM, PB7_LFLT |
| C3 | 100nF | VDD1 decoupling | 1, 2 |
| C4 | 100nF | VDD2 decoupling | 1, 2 |
| U3 | DRV8871 | H-bridge field-emitter driver 3.6 A | IN1, IN2, GND, VM, OUT1, OUT2 |
| J2 | EMITTER | Force-field emitter (FE1) connector | 1, 2 |
| J4 | 4-pin | Service header: GND, LOCK_HOLD, RESET_N, AUX_BUZZ | 1, 2, 3, 4 |
| TP1 | TP | RESET_N test point (header side) | 1 |
| TP2 | TP | RESET_N test point (MCU side) | 1 |
| R3 | 10k | RESET_N pull-up | 1, 2 |
| S1 | LIMIT | Hatch-closed limit switch | 1, 2 |
| R4 | 10k | LIMIT_SW pull-up | 1, 2 |
| R5 | 330R | STATUS LED resistor | 1, 2 |
| D2 | GRN | STATUS LED | 1, 2 |
| R6 | 330R | FAULT LED resistor | 1, 2 |
| D3 | AMB | FAULT LED | 1, 2 |

## Nets
| Net | Class | Nodes |
|---|---|---|
| VFLD_IN | power | J1.1, F1.1 |
| VFLD | power | F1.2, C5.1, C1.1, U1.VIN, U3.VM |
| SW_NODE | power | U1.SW, D1.1, L1.1 |
| V3V3 | power | L1.2, C2.1, U1.FB, U2.VDD1, C3.1, U2.VDD2, C4.1, R3.1, R4.1 |
| GND | power | J1.2, C5.2, C1.2, U1.GND, D1.2, C2.2, U2.GND1, C3.2, U2.GND2, C4.2, U3.GND, J4.1, S1.2, D2.2, D3.2 |
| OUT1 | power | U3.OUT1, J2.1 |
| OUT2 | power | U3.OUT2, J2.2 |
| DRV_IN1 | signal | U2.PB0_IN1, U3.IN1 |
| DRV_IN2 | signal | U2.PB1_IN2, U3.IN2 |
| RESET_N | signal | J4.3, TP1, TP2, R3.2, U2.RESET_N |
| LOCK_HOLD | signal | J4.2, U2.PA4_LOCK |
| AUX_BUZZ | signal | J4.4, U2.PA5_AUX |
| LIMIT_SW | signal | S1.1, R4.2, U2.PA3_LIM |
| LED_STAT | signal | U2.PB6_LSTAT, R5.1 |
| LED_STAT_A | signal | R5.2, D2.1 |
| LED_FLT | signal | U2.PB7_LFLT, R6.1 |
| LED_FLT_A | signal | R6.2, D3.1 |
