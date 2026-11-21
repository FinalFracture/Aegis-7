# Door lab pass C: Rook hardware upgrade (Vance REALISM_SPEC §9, a84b576)

Run: `python3 assets/src/door_lab/door_lab_passC.py` builds all 15 variants, exports them, runs QA (`passC_qa.json`) and renders to `/workspace/renders/doorlab_passC/`.
V1 of each asset is also written to `godot/assets/models/door_lab/door_lab_<asset>.glb`. Variants go to `assets/glb/door_lab/<asset>/v1..v5.glb`.
Approach side = -Z for every asset. LH variants are X-mirrors: rotations about local Y/Z and translations along local X flip sign. The slider handed variants swap the _L/_R names, so `leaf_L` stays the -X leaf and no sign flips.

## Variants (visual tris, budget < 6000)
| asset | v1 (placed) | v2 | v3 | v4 | v5 |
|---|---|---|---|---|---|
| bulkhead_hatch | RH 150 coaming 5766 | LH 5766 | RH 300 coaming 5776 | LH 300 5776 | RH, 6 ribs + kick 5960 |
| biparting_slide | panel shown swung up 5808 | panel closed 5808 | no panel (service) 5568 | v1 handed 5808 | v2 handed 5808 |
| floor_hatch (rev 2) | RH stay, 0.45 well 4360 | LH 4360 | RH 0.75 well 4360 | LH 0.75 4360 | RH 0.30 well 4360 |

## Animated nodes (pivot on the axis, closed pose = modelled)
**bulkhead_hatch** (recenter shift z +0.0725; pass B was +0.0745)
- `leaf`: group on the hinge axis (0.65, -, 0.1585). Open = about +Y, +100°.
- `bulkhead_LockWheel`: about local Z, +90° (dogs thrown).
- `bulkhead_OverrideOrange_Handwheel`: coaxial, about local Z, 4320° (12 turns) for full throw.
- `bulkhead_Dog_01..08` / `bulkhead_Linkage_01..08`: local +X, +0.025 m.
- `bulkhead_InflatableSeal`: scale local Z ×1.385 when inflated (8 mm compression).
- `bulkhead_PushOffRam_1/2`: +Z 0.012 m.
- `bulkhead_Damper_body` (root) / `bulkhead_DamperRod` (leaf child): each aims local -Z at the other.
- `bulkhead_Gauge_needle_front/back`: about local Z, -270/110 (front) / +270/110 (back) deg per kPa.
- `bulkhead_EqualizeLever` (approach face): about local Z, -90°.

**biparting_slide**
- `leaf_L` / `leaf_R`: X -1.000 / +1.000 m.
- `slide_roller_*`: spin about local Z by travel/r (r 0.030; antilift r 0.015, opposite sign). Gage's `_tag_rollers` is unchanged.
- `slide_SolenoidBolt`: +Z 0.018 m (locked).
- `slide_HexRelease_socket`: about local Z, 90° (manual release).
- `slide_AccessPanel`: about local X; closed to open is +90°. V1 bakes the open pose, so closing from V1 is -90°.
- `slide_Keeper` rides on leaf_L.

**floor_hatch**, rev 2 (Vance's counterbalance decision, 2026-11-20). The finished floor is GLB y 0.462; the opening is centred on GLB x/z = 0. Below, a "pre-recenter" coordinate is the pre-recenter frame (floor at y = 0); add 0.462 to get a GLB y.
- `hatch_leaf`: group whose origin is on the hinge axis, GLB (0, 0.430, -0.524). Open = rotate about local +X by -105°. The axis is now 32 mm below the floor (pass C had 16 mm), so the Ø56 tube top stays 4 mm under the floor.
- The leaf stays 1.00 × 1.00 × 0.10 and flush (0.0 mm). It has a 4 mm top and a 6 mm underside chamfer on the hinge edge, plus a 3 mm-clearance scallop around the tube.
- Hinge and counterbalance. There are no gas struts.
  - `hatch_HingeTube` (leaf child): Ø56 tube running x -0.490…+0.450, with end caps, a -X journal, and 4 webs to the leaf's rear face.
  - `hatch_TorsionBar` (fixed): Ø25 bar inside the tube, x -0.575…+0.467. It carries 585 N·m. Its round surface makes the twist invisible, so it is static in the GLB.
  - `hatch_TorsionAnchor_frame` (fixed): the exposed anchor clevis at the -X end. It has 2 cheeks on the channel floor, a pin, and the torque arm on the bar end. Its pin is at 200° and 30 mm about the axis.
  - `hatch_TorsionAnchor_leaf` (leaf child): the exposed anchor clevis on the tube's +X end cap. It has 2 cheeks, a pin, the torque arm on the bar end, and the journal stub through the +X bearing into the damper. Its pin is at 135° and 30 mm about the axis.
  - `hatch_HingeBearing_frame` (fixed): end bearings at x ±0.505…0.530.
  - `hatch_RotaryDamper` (fixed): on the hinge axis, outboard at x 0.535…0.590. Speed caps are 77.8°/s opening and 33.3°/s closing. These are in the GLB extras, which Godot imports as node meta `extras`, and in Gage's door metas `damper_open_dps` / `damper_close_dps`. They match floorhatch.json: 35/0.45 = 77.8 and close 0.60× = 33.3.
  - Everything sits in an open hinge channel behind the leaf: z -0.575…-0.506, floor 72 mm down, |x| ≤ 0.600. Under the flange it widens to z -0.488 at the bearing, damper and anchor ends. Nothing protrudes above the floor.
- Torque model at 1 G (phase timing unchanged):

| term | N·m |
|---|---|
| leaf weight moment | 687 |
| torsion bar | 585 |
| net closing at the closed position | about 102 |
| actuator | ≤ 530 |

  The figures are in `hatch_TorsionBar` extras and Gage's `torque_model` meta.
- Stay. It moved to the non-hinge +X side wall (mirrored on the LH variants) and lies entirely in the band x 0.4515…0.4805, which is outside the 0.45 column.
  - `hatch_stay_leaf_lug` (leaf child): x 0.4585…0.4615, on the column side of the seal bead. Its pin is at pre-recenter (y -0.125, z -0.274), i.e. 0.25 m from the axis.
  - `hatch_stay_arm` (leaf child): origin on the lug pin; it rotates about local X relative to the leaf. It is 5 × 20 mm flat bar, 0.40 m between pins, and carries its own pins.
    - Angle relative to the leaf: 0° closed, 89.19° at 52.5°, 173.29° at 105°.
  - `hatch_stay_slider` (root): origin on the foot pin at pre-recenter y -0.145. It travels along local Z in a slot in the side-wall recess.
    - Travel: 0 closed, +7.6 mm at 10.5°, back to 0 at 21°, -115.1 mm at 52.5°, -495.2 mm at 105°, the end of the slot.
  - Detent:
    - `hatch_stay_detent_housing` (fixed) sits under the slot.
    - `hatch_stay_detent_plunger` (root, local Z = world +Y) is up (0) whenever the slider is clear of it. It is pressed down -8.5 mm from 98.5° to 104.5° while the slider runs over it. At 105° it pops up behind the slider's trailing face (2.5 mm gap), so the stay locks at 105°.
    - `hatch_stay_detent_knob` (child of the plunger) is an OverrideOrange pull knob. It sits in the recess so it can be seen, and it rides with the plunger.
  - Recess in the liner wall: 12.5 mm deep (x 0.449…0.4625), z -0.40…+0.16, y -0.19 up to the land. The slot and plunger pocket go to x 0.482, i.e. 32 mm, within the 40 mm limit.
  - Tables are at 0.5° steps (211 entries) in `floor_hatch.stay_tables()` and Gage's `STAY_ARM_DEG` / `STAY_SLIDE_M` / `STAY_PLUNGER_M`.
  - On the LH variants, rotation about X and travel along Z keep their sign.
- `hatch_LockWheel`: about local Y, +90°.
- `hatch_OverrideOrange_Handwheel`: about local Y, 4320°.
- `hatch_OverrideOrange_Lever`: about local Z, +70°.
- `hatch_Dog_01..04` / `hatch_Linkage_01..04`: local +X, +0.025 m.
- `hatch_InflatableSeal`: scale local Y ×1.208.
- Removed in rev 2: `hatch_strut_L_body`, `hatch_strut_R_body`, `hatch_strut_L_rod`, `hatch_strut_R_rod`, `hatch_frame_strut_clevis`, `hatch_leaf_clevises`, `hatch_stay_pivot_bracket`, `hatch_stay_track_detent`, `hatch_HingeHeavy_frame`, `hatch_HingeHeavy_leaf`.

## QA (`passC_qa.json`)
- All 15 variants pass:
  - Clip check at every key pose: no bad overlaps, no coplanar faces, no open meshes.
  - Motion sweeps: worst penetration ≤ 0.1 mm.
  - Tri budget.
- Floor hatch, rev 2:
  - The leaf top is flush with the flange: 0.0 mm.
  - The liner clear opening measures 0.900 × 0.900 by ray cast (the throat ray reads 0.932 in x where it meets the stay recess).
  - Clear column sweep (`column_sweep` in `passC_qa.json`, plus `floor_hatch_column_sweep.txt`). The column is |x|, |z| < 0.450 from the well-floor top to floor +2 m, checked at 0…105° in 0.5° steps on all 5 variants:

| category | min clearance to the column | worst part |
|---|---|---|
| fixed hardware | 2.0 mm | `hatch_Keeper`, in its pocket |
| moving counterbalance / stay / damper | 1.5 mm | `hatch_stay_arm` |
| leaf and leaf-borne lock gear at 105° | 17.5 mm | — |

    Nothing in the first two categories enters the column at any step. The leaf (the lid) crosses the column from 0° to 94.5°, which it must do to open.
  - The stay, slider and detent have 0.0 mm penetration at 1° steps, and through the detent pop-up with Godot-style table interpolation at 0.1° steps from 100° to 105°.
  - The torsion bar ends sit 2 mm into the anchor hubs, as the splined engagement intends.
  - Lock-gear gaps (Vance, after accepting the leaf crossing the column). `lock_gear_gaps` in `passC_qa.json` and the LOCK GEAR lines in `floor_hatch_column_sweep.txt`. Parts: lock wheel, 4 dogs, 4 linkages, handle, OverrideOrange handwheel and lever. Targets: liner, frame flange, keepers. Swing 0…105° in 0.5° steps (211 poses), dogs retracted as the phases run it. The gap is the exact point-to-triangle distance from every vertex plus 6000 surface samples per part, and reads negative inside a solid. The minima are the same on all 5 variants, except the lock wheel and handwheel, which sit farther away in deeper wells:

| part | min gap | at | against |
|---|---|---|---|
| `hatch_Dog_01` / `_02` (far edge) | 9.62 mm | 3.0° | liner (rebate wall as the edge rises); keepers 13.47 mm at 2.0° |
| `hatch_Dog_03` / `_04` | 15.0 mm | 1.0° | liner; keepers 17.0 mm at 1.0° |
| `hatch_Linkage_01` / `_02` | 112.5 mm | 3.0° | liner |
| `hatch_Linkage_03` / `_04` | 117.0 mm | 0° | liner |
| `hatch_Handle` | 93.9 mm | 0° | liner |
| `hatch_OverrideOrange_Lever` | 121.0 mm | 0° | frame flange |
| `hatch_LockWheel` | 298 mm (V5: 148 mm) | 0° | liner |
| `hatch_OverrideOrange_Handwheel` | 333.4 mm (V5: 262 mm) | 0° | liner |

    Every part is at 3 mm or more, so no geometry changed and the GLBs are byte-identical to 2db8f7b. For reference, in the closed, dogs-thrown state (dogs in the keeper pockets, which is not part of the swing), each dog sits 3.97 mm from its keeper and 8.0 mm from the liner.
  - Dog retraction (`dog_retraction` in `passC_qa.json`). In `floorhatch.json` the open sequence runs dogs 1.7–2.5 s, then seal_deflate, then the leaf first moves in lurch at 3.0 s, so there is a 0.5 s margin. The close sequence seats the leaf (final_seat) at 8.15 s and starts the dogs at 8.2 s. Both times are before ×0.6 mech_phase_scale. In `mech_door.gd`, `_dog_throw_u` returns 1 − dogs-phase u on open, so dogs and linkages are at 0 throw from the end of the dogs phase onward. The patched Godot run at 60 fps measured the same thing: dogs end at 1.500 s and q first leaves 0 at 1.800 s (lurch); on close q = 0 at 11.000 s and the dogs start at 11.033 s.
  - Godot findings for the coming incremental patch (Gage-owned files, not edited here):
    1. `_floor_hatch` tags `_each_named(inst, "hatch_dog_")`. That is a case-insensitive substring match, so it also catches `hatch_dog_guides`, the fixed guide blocks on the leaf. The guides then slide 25 mm in +X with the dogs whenever the dogs are thrown, which includes the closed rest pose. `_tag_hatch` does the same with `bulkhead_dog_guides`. The fix is to match `hatch_dog_0` / `bulkhead_dog_0`.
    2. A forced pose (`force_q`) with 0 < q ≤ 2% of travel (≤ 2.1°) shows the dogs thrown while the leaf is lifted, because of the `travel_u > 0.02` test in `_dog_throw_u` / `_pose_dog`. The animated sequence never does this, but a static pose would. The fix is to test `travel_u > 0.0`.
