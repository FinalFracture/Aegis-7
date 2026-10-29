# #51 Sprocket bot lift (stair core v1.1, option 1, SW stack)
Generator: `assets/src/lift_generator.py`. glb: `godot/assets/models/sprocket_lift.glb`, not placed anywhere. Sheet: `final_lift_sheet.png`. Sequence: `final_lift_sequence.png` and `.gif`.

- **Origin:** the building plan origin, the same as #3–#7. X is axial, Y is up from the L1 finished floor, and +Z is spinward.
- **Position:** shaft X 0.6..2.2, Z 0.8..2.4 (1.6 × 1.6), Y −0.15 (shallow pit, my assumption) .. 6.6 (cap, per the section).
  - Car 1.2 × 1.2 × 1.4 at X 0.8..2.0, Z 1.0..2.2, which gives 0.1 m running clearance in the 1.4 m well.
  - Landing doors 1.0 × 1.3 at X 0.9..1.9 in the south (corridor) wall, with sills at Y 0 (L1) and Y 4.2 (L2). They open onto the 1.2 m corridor landings at Z −0.4..0.8.
  - Call panels are on the west jamb, X 0.45..0.85 on the corridor face.
  - The controller cabinet is in the 202 slot (X 0.1..0.6, L2), per the plan. The lift is machine-room-less, with a rack-and-pinion drive on the east guide rail.
- **Riser:** it shares the north face Z 2.4. The car stays at least 0.20 m clear of it in every clip.
- **Build:**
  - White composite shaft and a gunmetal fire-separation band at the L2 slab (Y 3.9–4.2).
  - Telescoping two-speed sliding doors (4 panels per level) running in a 50 mm cavity in the south wall, with amber latch lights. Green and amber status lights above each door.
  - Alloy guide rails.
  - Inside the car: an amber dock pad, a charge contact at 0.45 m on the back wall, a rear bumper, and 2 latched side clamps that close to 10 mm from Sprocket's chassis for spin-down.
- **Sprocket:** it reverses in so its back port at 0.45 m meets the car's charge contact.

| Tris | Count |
|---|---|
| Static (shaft, rails, rack, doors frame, call panels, controller) | 960 |
| Moving (car + clamps + 8 door panels) | 608 |
| Sprocket stand-in | 696 |
| Total | 2,264 |

**Nodes:** `Shaft_Static`; `Door_L1_W2`, `Door_L1_W1`, `Door_L1_E1`, `Door_L1_E2` and the same four for `Door_L2`; `Lift_Car`, with children `Car_Clamp_W` and `Car_Clamp_E`; `Sprocket_Standin` (top level, hideable).

**Clips** (30 fps):

| Clip | Duration | What happens |
|---|---|---|
| `call_open_L1` | 2.0 s | L1 doors open |
| `sprocket_board` | 3.5 s | the stand-in reverses in from the landing and the clamps engage |
| `ride_up` | 6.5 s | L1 doors close, clamps engage, car rises 4.2 m, L2 doors open |
| `ride_down` | 6.5 s | the reverse; clamps release at the bottom |
| `idle` | 2.0 s | rest pose |

**Checks** (sampled every 1/15 s over all clips):
- The car and clamps stay at least 0.04 m from the shaft walls, pit and cap.
- The car stays 0.20 m from the riser face.
- The door panels stay inside the wall cavity (X 0.62..2.18, Z 0.825..0.875).
- The stand-in is inside the car: its port touches the charge pin (0.000) and the engaged clamps are 0.01 m from the chassis.
- The reloaded glb lists 13 nodes and 5 animations.
