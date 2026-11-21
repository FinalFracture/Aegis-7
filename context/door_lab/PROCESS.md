# Door lab process

Isolated scene `res://scenes/test/door_lab.tscn`. All four doors instance GLBs. Pocket is `door_lab_biparting_slide.glb`. The wall hatch is `door_lab_bulkhead_hatch.glb` (100°, eight dogs, hinge +Y, swing toward +Z). Bay3 and the pair instance `tt_entrance_bay_3l.glb` and `tt_door_pair_18.glb`. Do not edit those glb files, `project.godot`, `tt_movers.gd`, or the tower and preface scenes. The lab ships four doors. The floor-hatch timing in section 7.5 is not a fifth station.

## Settlement

Game tempo, Jared 2026-11-20 13:50 CT. Vance phase tables stay the timing source. Leaf travel uses `travel_time_scale` 0.45 on the open. Close is per door: pair 0.45, bay3 0.60, pocket capped at 0.64 m/s, wall hatch capped at 19.4 deg/s (7.80 s). Latch, seal, dog, equalize, and the control gaps use `mech_phase_scale` 0.60. Lurch and settle stay at 1.00. Targets (open/close): pocket 1.08/2.40 s, bay3 1.54/2.85 s, pair 1.21/2.05 s, wall hatch 4.64/7.80 s. The run writes this into `meta.json`.

## Add a profile

1. Copy `godot/resources/door_lab/pocket.json` (or the closest type).
2. Keep the phase rows in Vance's units. The compiler groups phases by name and kind: travel, lurch, settle, or mech. The JSON `scale` flag is not the switch.
3. Point a `MechDoorProfile` `.tres` at the json. `sample(direction, t)` is the only pose source. Put scalars, caps, mass, and inertia in the json.
4. Instance it from `DoorLabRig` with a leaf table: body, hinge sign, stagger, rest. Slides move the body origin (the body is the pivot). Swings rotate the body on its hinge.
5. Run the QA below. Do not add a second tween.

## Hatch swing

Rook's hinge is the leaf origin. Sign +1 rotates about +Y and the free edge swings toward +Z. The closed plug sits 6 mm off the frame with the seal deflated. Lab-only parts (hold-open catch, equalize lever, hazard band, davit) are parented on the rig, not written into the glb.

## Lab-only parts on the as-built meshes

The bay frame mesh has no post in the 106 mm stile slots. The rig adds mullions there, 3 mm off each stile, collision included. Finger guards fill the 55 mm hinge gap down to a 5 mm visible gap per side, on the approach face, parented to the rig. Floor sweeps bring the leaf bottom to the 8 mm visual gap. The bay threshold mat is moved down on the instance only, so the sweep can sit on that gap. Pair sweeps are the same idea. Pocket and hatch hardware that the GLB folds into one mesh (motor, tensioner, bumper, solenoid, keeper) is a named lab marker on that part. None of these edits are written back to the glb. The lab wall stops 40 mm outside each frame.

## Lab light

The key is pitch −35° and yaw 30° off the approach normal (−Z), energy 0.5, so it strikes the faces the cameras see. A raw euler of (−35°, 30°, 0°) points the other way and leaves those faces black. Each door has its own fill (energy 0.2) on the approach side, a rim, and a 4000 K downlight. On Windows the compatibility renderer tints every surface inside a ReflectionProbe green (Godot issue 98382). The probe still covers the lab, with intensity 0 on that driver, and metals reflect the slate background instead.

## Run QA

Godot 4.7.2, from the repo root. Pass `--qa-door-lab-out`. Relative paths join `res://`. One process at a time, in the foreground.

Functional:

```
godot --headless --path godot --fixed-fps 60 res://scenes/test/door_lab.tscn -- --qa-door-lab --qa-door-lab-out ../qa/door_lab/runB
godot --headless --path godot --fixed-fps 20 res://scenes/test/door_lab.tscn -- --qa-door-lab --qa-door-lab-out ../qa/door_lab/runB_20fps
godot --headless --path godot --fixed-fps 15 res://scenes/test/door_lab.tscn -- --qa-door-lab --qa-door-lab-out ../qa/door_lab/runB_15fps
```

The harness sets `physics_ticks_per_second` to the fps and `max_physics_steps_per_frame` to 1. Exit 0 only when every functional check passes. The last line is `DONE --qa-door-lab fails=N`.

Shots are windowed. Windows has no xvfb; opengl3 is the driver. Shots rewrite V-LUMA in `runB` (limit 0.25) and copy PNGs to `C:\Users\upchu\aegis_shots\doorlab_B`.

```
godot --path godot --rendering-driver opengl3 --fixed-fps 60 res://scenes/test/door_lab.tscn -- --qa-door-lab-shots --qa-door-lab-out ../qa/door_lab/runB
```

`tools/door_lab_contact_sheet.py` writes `contact_sheet.png` and a `motion.png` per door from `motion.csv`. Half-open heroes are `hero_final_<door>.png`. The four-door frame is `overview.png`.
