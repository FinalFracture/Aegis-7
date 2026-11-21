# Door lab process

Isolated scene `res://scenes/test/door_lab.tscn`. Pocket, bay3, the pair, and the wall hatch instance GLBs. Pocket is `door_lab_biparting_slide.glb`. The wall hatch is `door_lab_bulkhead_hatch.glb` (100°, eight dogs, hinge +Y, swing toward +Z, I=174). Bay3 and the pair instance `tt_entrance_bay_3l.glb` and `tt_door_pair_18.glb`. The floor hatch is a fifth lab station (1.0 m leaf, 140 kg, I=46.7, hinge local X) and is not walked. Do not edit those glb files, `project.godot`, `tt_movers.gd`, or the tower and preface scenes.

## Settlement

Game tempo, Jared 2026-11-20 13:50 CT. The shipped `.tres` / JSON table is the timing authority (`timing_authority: shipped_tres`). Leaf travel uses `travel_time_scale` 0.45 on the open. Close is per door: pair 0.45, bay3 0.60, pocket capped at 0.64 m/s (mass 47.9 kg, 9.81 J), wall hatch capped at 19.4 deg/s (I=174, 9.97 J, 7.80 s). Floor hatch close is 0.60× (33.3 deg/s, I=46.7, 7.9 J, 6.39 s). Section 8's 5.7 J is that floor-hatch inertia at the retired 0.7× cruise, not the wall plug. Latch, seal, dog, equalize, and the control gaps use `mech_phase_scale` 0.60. Lurch and settle stay at 1.00. Targets (open/close): pocket 1.08/2.40 s, bay3 1.54/2.85 s, pair 1.21/2.05 s, wall hatch 4.64/7.80 s, floor hatch 4.09/6.39 s. The run writes this into `meta.json`.

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

The key is pitch −35° and yaw 30° off the approach normal (−Z), energy 1.0, shadows on. A raw euler of (−35°, 30°, 0°) points the other way and leaves those faces black. Ambient is #5A6470 at 0.35, tonemap exposure 1.3, filmic. Each door has one omni at 3 m in front and 2.2 m up (energy 0.8, range 8, attenuation 1), a rim at 0.8, and a doorway downlight at 1.2 with a 45° cone. A 2×4 m reflection card sits behind each hero camera. On Windows the compatibility renderer tints every surface inside a ReflectionProbe green (Godot issue 98382). The probe still covers the lab, with intensity 0 and ambient disabled on that driver, and metals reflect the background instead.

## Run QA

Godot 4.7.2, from the repo root. Pass `--qa-door-lab-out`. Relative paths join `res://`. One process at a time, in the foreground.

Functional:

```
godot --headless --path godot --fixed-fps 60 res://scenes/test/door_lab.tscn -- --qa-door-lab --qa-door-lab-fps 60 --qa-door-lab-out ../qa/door_lab/runD
godot --headless --path godot --fixed-fps 20 res://scenes/test/door_lab.tscn -- --qa-door-lab --qa-door-lab-fps 20 --qa-door-lab-out ../qa/door_lab/runD_20fps
godot --headless --path godot --fixed-fps 15 res://scenes/test/door_lab.tscn -- --qa-door-lab --qa-door-lab-fps 15 --qa-door-lab-out ../qa/door_lab/runD_15fps
```

`--fixed-fps` alone is not enough: the engine consumes it, so the harness requires `--qa-door-lab-fps N`, prints `Engine.physics_ticks_per_second` and the measured physics dt, and fails the run when the measured rate is not N.

The harness sets `physics_ticks_per_second` to N and `max_physics_steps_per_frame` to 1. Exit 0 only when every functional check passes. The last line is `DONE --qa-door-lab fails=N`.

Shots are windowed. Windows has no xvfb; opengl3 is the driver. Shots rewrite V-LUMA (leaf-face mean, limit 0.25) and copy PNGs only when `--qa-door-lab-mirror` names a directory that already exists.

```
godot --path godot --rendering-driver opengl3 --fixed-fps 60 res://scenes/test/door_lab.tscn -- --qa-door-lab-shots --qa-door-lab-out ../qa/door_lab/runD --qa-door-lab-mirror C:\Users\upchu\aegis_shots\doorlab_D
```

`tools/door_lab_contact_sheet.py` writes `contact_sheet.png` and a `motion.png` per door from `motion.csv`. Half-open heroes are `hero_final_<door>.png`. The four-door frame is `overview.png`. Shots also write `<door>_motion_strip.png` (closed, lurch, 25/50/75%, open, close mid, settle) and `<door>_curve.png` (position and velocity against time, with axes and phase markers) at the run root.

## Pass D look

Lab only. Pocket vision lites use TT_GlassScissor at albedo (0.55, 0.62, 0.68), alpha 0.35, roughness 0.10, with the lower 60% of the core as opaque pearl. Pocket cladding and the hatch surround use albedo (0.16, 0.18, 0.21), metallic 0.5, roughness 0.45. Each door has a 10×300 mm status strip on the camera-facing jamb, centred at 1.4 m (the floor hatch strip lies in the frame). Lamp colours follow AESTHETIC_SPEC §3. Cyan reveals are 15 mm at emission 0.7. The key shadow opacity is 0.5 and the bay canopy does not cast, so the slat grid does not stripe the leaves. Pair push plates are non-emissive amber (0.85, 0.45, 0.02). Bay scissor materials use anisotropic mipmaps and a 2× pattern scale. The hatch handwheel is a 4-spoke tube rim (30 mm tube), dogs have pivot blocks, the leaf edges have 3 mm bevels, and the loose lugs are one ID plate. Touch-zone wear is a ~150 mm patch, roughness −0.10, albedo +3.5%, capped at 0.90. The floor hatch frame is flush with the floor (±2 mm), with a gasket line, a recessed lift handle, a 50 mm hazard border, and the lid sitting in the frame.
