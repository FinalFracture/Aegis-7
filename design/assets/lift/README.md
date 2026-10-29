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

**Nodes:** `Shaft_Static`; `Door_L1_W2`, `Door_L1_W1`, `Door_L1_E1`, `Door_L1_E2` and the same four for `Door_L2`; `Lift_Car`, with children `Car_Clamp_W`, `Car_Clamp_E` and `Sprocket_Standin`. The stand-in is parented to the car (hide it to remove it); its local Z animates for boarding and exit.

**Clips** (30 fps, sampled from the reloaded glb; the car rides between 2.6 and 6.0 s):

| Clip | Duration | What happens |
|---|---|---|
| `call_open_L1` | 2.0 s | L1 doors open |
| `sprocket_board` | 3.5 s | the stand-in reverses in from the L1 landing, then the clamps engage |
| `ride_up` | 6.5 s | L1 doors close (0–1.5 s), clamps (1.7–2.3 s), the car rises 4.2 m (2.6–6.0 s), doors stay shut |
| `arrive_open_L2` | 2.0 s | L2 doors open |
| `sprocket_exit_L2` | 3.5 s | clamps release, then the stand-in drives out to Z −0.1 on the L2 landing |
| `ride_down` | 6.5 s | L2 doors close, clamps, the car descends |
| `arrive_open_L1` | 2.0 s | L1 doors open |
| `sprocket_exit_L1` | 3.5 s | clamps release, then the stand-in drives out onto the L1 landing |
| `idle` | 2.0 s | rest pose |

## v2 fix (Atlas review of d7bf704)
- **The diagonal "brace" and the stray rod at the base** were a render artefact. The sequence used a framing-anchor triangle that I had not made degenerate. It was never in the glb. The anchor is now collinear and has zero area.
- **"Car out of the shaft" and "doors through the car"** were a view artefact from hiding the south wall. The doors sit in the wall cavity at Z 0.83–0.87, in front of the car face at Z 1.0. The checks below confirm there is no intersection.
- **L2 doors at the end of ride_up:** the data did open them. The opening is now its own clip, `arrive_open_L2`, plus the exit clips.
- **Other changes:** the stand-in is now parented to the car, the doors fully close before the clamps and the ride start, and the guide shoes and pinion have a 4 mm running gap.

## Clash check (v2)
Every animation was reloaded from the glb and every 30 fps key sampled (954 frames). Each component is a box; the check takes the AABB gap of every component pair. There are no intersections.

| Pair (worst case over all frames) | Min gap (m) |
|---|---|
| car+clamps vs guide rails / drive rack | 0.004 |
| car+clamps vs pit floor | 0.040 |
| car+clamps vs shaft walls W/E | 0.044 |
| car+clamps vs shaft walls N/S, sills | 0.100 |
| car+clamps vs door panels (8, animated) | 0.129 |
| car+clamps vs fire separation | 0.144 |
| car+clamps vs controller cabinet | 0.194 |
| stand-in vs car body | 0.010 |
| stand-in vs charge pin (contact by design) | 0.000 |
| stand-in vs door panels (8) | 0.115 |
| stand-in vs south wall / sill during exit | 0.015 |
| stand-in vs N wall, rails, rack | 0.165 / 0.275 / 0.275 |

Tris: 960 static, 608 moving, 696 stand-in, 2,264 total.

Renders:
- `final_lift_sheet.png`
- `final_lift_sequence.png` / `.gif`: 16 frames, normal view
- `final_lift_cutaway_sequence.png` / `.gif`: 16 frames, 900 px tiles, with the front and east walls and the corridor-face parts hidden and the doors ghosted
