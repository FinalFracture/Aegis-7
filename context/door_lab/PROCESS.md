# Door lab process

Isolated scene `res://scenes/test/door_lab.tscn`. Pocket and hatch are procedural. Bay3 and the pair instance `tt_entrance_bay_3l.glb` and `tt_door_pair_18.glb`. Do not edit those glb files, `project.godot`, `tt_movers.gd`, or the tower and preface scenes.

## Settlement

Vance phase tables are the timing source. Latch, seal, dog, and equalize run at the published duration. Only leaf travel is compressed, by `travel_time_scale` (0.7) on the profile. One scalar, no code change, is how pass B retunes travel. Bay3 is the as-built outswing, not a telescoping slider. Sloane's 0.9 / 0.8 / 1.8 s targets are superseded. The run writes this into `meta.json`.

## Add a profile

1. Copy `godot/resources/door_lab/pocket.json` (or the closest type).
2. Keep the phase rows in Vance's units. Mark travel phases with `"scale": true` so `travel_time_scale` applies. Leave latch, seal, dog, and equalize unscaled.
3. Point a `MechDoorProfile` `.tres` at the json. `sample(direction, t)` is the only pose source.
4. Instance it from `DoorLabRig` with a leaf table: body, hinge sign, stagger, rest. Slides move the body origin. Swings rotate the body on its hinge.
5. Run the QA below. Do not add a second tween.

## Hatch swing

The plug is wider than the clear hole, so it cannot swing through the opening. The hinge sign is +1 and the plug swings toward the approach (−Z). The closed corridor face sits 6 mm off the wall. That shift is on the lab mesh, not a glb.

## Lab-only parts on the as-built meshes

The bay frame mesh has no post in the 106 mm stile slots. The rig adds mullions there, 3 mm off each stile, collision included. Finger guards fill the 55 mm hinge gap down to a 5 mm visible gap per side, on the approach face, parented to the rig. Floor sweeps bring the leaf bottom to the 8 mm visual gap. The bay threshold mat is moved down on the instance only, so the sweep can sit on that gap. Pair sweeps are the same idea. None of these edits are written back to the glb.

## Lab light

The key is pitch −35° and yaw 30° off the approach normal (−Z), so it strikes the faces the cameras see. A raw euler of (−35°, 30°, 0°) points the other way and leaves those faces black. On Windows the compatibility renderer tints every surface inside a ReflectionProbe green (Godot issue 98382). The probe still covers the lab, with intensity 0 on that driver, and metals reflect the slate background instead.

## Run QA

Godot 4.7.2, from the repo root. Pass `--qa-door-lab-out`. Relative paths join `res://`.

Functional, one process at a time:

```
godot --headless --path godot --fixed-fps 60 res://scenes/test/door_lab.tscn -- --qa-door-lab --qa-door-lab-out ../qa/door_lab/run60
godot --headless --path godot --fixed-fps 20 res://scenes/test/door_lab.tscn -- --qa-door-lab --qa-door-lab-out ../qa/door_lab/run60_20fps
godot --headless --path godot --fixed-fps 15 res://scenes/test/door_lab.tscn -- --qa-door-lab --qa-door-lab-out ../qa/door_lab/run60_15fps
```

The harness sets `physics_ticks_per_second` to the fps and `max_physics_steps_per_frame` to 1. Exit 0 only when every functional check passes. The last line is `DONE --qa-door-lab fails=N`.

Shots are windowed. Windows has no xvfb; opengl3 is the driver:

```
godot --path godot --rendering-driver opengl3 --fixed-fps 60 res://scenes/test/door_lab.tscn -- --qa-door-lab-shots --qa-door-lab-out ../qa/door_lab/run60
```

`tools/door_lab_contact_sheet.py` writes `contact_sheet.png` and a `motion.png` per door from `motion.csv`.
