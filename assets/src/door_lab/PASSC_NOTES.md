# Door lab pass C: Rook hardware upgrade (Vance REALISM_SPEC §9, a84b576)

Run: `python3 assets/src/door_lab/door_lab_passC.py` builds all 15 variants, exports them, runs QA (`passC_qa.json`) and renders to `/workspace/renders/doorlab_passC/`.
V1 of each asset is also written to `godot/assets/models/door_lab/door_lab_<asset>.glb`. Variants go to `assets/glb/door_lab/<asset>/v1..v5.glb`.
Approach side = -Z for every asset. LH variants are X-mirrors: rotations about local Y/Z and translations along local X flip sign. The slider handed variants swap the _L/_R names, so `leaf_L` stays the -X leaf and no sign flips.

## Variants (visual tris, budget < 6000)
| asset | v1 (placed) | v2 | v3 | v4 | v5 |
|---|---|---|---|---|---|
| bulkhead_hatch (M-122) | RH 150 coaming 5798 | LH 5798 | RH 300 coaming 5810 | LH 300 5810 | RH, 6 ribs + kick 5992 |
| biparting_slide (M-122) | panel closed 5968 | panel shown swung up 5968 | no panel (service) 5728 | v1 handed 5968 | v2 handed 5968 |
| floor_hatch (rev 2, M-122) | RH stay, 0.45 well 4388 | LH 4388 | RH 0.75 well 4388 | LH 0.75 4388 | RH 0.30 well 4388 |

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
- `slide_roller_*`: spin about local Z by travel/r (r 0.030).
- `slide_AntiLiftRoller_{L,R}{1,2}` (pass G, was `slide_roller_*_antilift`): spin about local Z by travel/r, r 0.020 (was 0.015), opposite sign. Gage's `_tag_rollers` still matches on "antilift" (case-insensitive); `gage_doorlab_incr_G.patch` sets its radius to 0.020.
- `slide_SolenoidBolt`: local -Y 0.018 m (locked; pass G vertical throw, was +Z). Origin is on the bolt axis at its top end inside the can.
- `slide_HexRelease_socket`: about local Z, 90° (manual release).
- `slide_AccessPanel`: about local X; closed to open is +90°. M-122: V1 (placed) and V4 now bake the closed pose (was V2/V5), so the lab no longer turns it -90° at load; V2/V5 bake the open pose.
- `slide_Keeper`, `slide_BeltClamp_L/R` and `slide_AntiLiftRoller_*` ride on their leaf (`slide_Keeper` on leaf_L; on the handed v4/v5 it rides leaf_R, on the solenoid side).

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

## Floor hatch colliders (pass E, for Gage's open walk-collision issue)
All 5 variants and the placed copy carry these colliders. None of them is visible, and the tri counts above are visual only.

| node | shape | what it is |
|---|---|---|
| `hatch_leaf-convcolonly` | convex box 1.00 × 0.10 × 1.00 | the lid (on the `hatch_leaf` pivot, unchanged) |
| `hatch_frame-colonly` | trimesh, 7 boxes | flange and frame ring outside the rebate (top = finished floor), plus the hinge-channel floor |
| `hatch_well_wall_N/S/W/E-convcolonly` | convex box each | liner walls, inner face on the 0.900 column, from the well floor up to the rebate land (−0.106) |
| `hatch_well_floor-convcolonly` | convex box | well floor slab, top = −well depth |

- The 0.90 × 0.90 opening is open from the land down to the well floor.
- The well pieces are convex, so they are solid. As trimesh, a falling capsule tunnelled through the 12 mm floor slab's top face and stuck inside it.
- The wall boxes fill the keeper pockets and the stay recess behind the 0.450 face, so a capsule meets a flat liner. The dogs and the stay arm move inside that volume, but they are not colliders. Gage's leaf-collide check is clean at 60/20/15 fps.
- Before this change, one `hatch_frame-colonly` trimesh held the ring, the liner walls (below −0.20 only) and the floor.

V-GAP-HATCH (pass E read 114 mm). The GLB perimeter gap is 6.0 mm on the W, E and S sides: the rebate wall is at ±0.506 and the leaf edge at ±0.500. Gage's `_floor_side_mm` compared the leaf AABB with the `hatch_frame` AABB, which is the flange's outer edge at ±0.62. That gives 120 mm, which reads as 114 mm off the 6 mm target. The measurement is fixed in the pass E incremental patch, which now reads W, E and S at 6.00 mm. The N side is the open hinge channel, which the lid's hinge edge needs through the 105° swing, so it has no rebate wall.

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

## Pass G: pocket slider head readability (Gage's pass F open-detail shot)
Applies to all biparting_slide variants v1..v5. The handed variants v4/v5 swap `_L`/`_R` (regex `_([LR])(?=\d|_|-|$)`), so `_L` stays on the -X leaf.
New material slots (`door_lab_lib.py`) use the same UV0 planar projection as every other slot, so Sloane's PBR textures drop in per slot. None of the names contains "rubber"/"seal", so Gage's `_retint` can lift them and still clamps them at 0.90.

| part | before (pass F) | after (pass G) | parent |
|---|---|---|---|
| (a) anti-lift roller | `slide_roller_{L,R}{1,2}_antilift`, Ø30 × 20, DL_SealRubber, hidden behind the carriage plate | `slide_AntiLiftRoller_{L,R}{1,2}`, Ø40 × 24 acetal tyre (Ø24 bore), DL_AcetalWhite (0.80, 0.80, 0.76). The carriage plate is lowered to the roller line so it shows. Ø14 axle cap. | leaf_L / leaf_R |
| (b) belt clamp | `slide_BeltClamp_{L,R}`, 60 mm long on carriage 1, TT_BrushedSteel | same names. A 100 mm jaw pair with a 100 × 32 × 4 front plate and 2 Ø13 cap-screw heads, on its own hanger at the leaf centre. DL_YellowZincPlate (0.70, 0.59, 0.30, metallic 0.55, roughness 0.42). On v1–v3 leaf L grips the upper belt run and leaf R the lower; the handed v4/v5 mirror this. 2 mm to the belt over the full travel. | leaf_L / leaf_R |
| (c) end-stop bumper | `slide_Bumper` (4 pocket buffers 25 × 80 × 30, DL_SealRubber, hidden in the pocket) | `slide_Bumper_{L,R}` (the same buffers, DL_BumperRubber 0.06 grey) + new `slide_EndStop_{L,R}` track stops 60 × 46 × 27, DL_BumperRubber, at x ±1.934. 4.0 mm to the carriage at full open, 2.0 mm at 2 mm overshoot. | root (fixed) |
| (d) solenoid body | `slide_Solenoid` 40 × 22 × 22, TT_BrushedSteel | `slide_Solenoid` 60 × 38 × 28, DL_SolenoidRed (0.56, 0.05, 0.04), plus `slide_Solenoid_mount` (DL alloy) bracket on the upper rail face. Centre x -0.055 (+0.055 on v4/v5). | root (fixed) |
| (d) solenoid bolt | `slide_SolenoidBolt` Ø8 × 20, Z throw | `slide_SolenoidBolt` Ø12 × 30, DL_PolishedSteel (0.86, metallic 1, roughness 0.12). Vertical throw 18 mm down through the keeper hole. Retracted it clears the keeper by 14.3 mm; thrown, 3.0 mm to the hole walls. | root, origin on the throw axis |
| (d) keeper | `slide_Keeper` U-staple, TT_BrushedSteel | `slide_Keeper` 52 × 8 × 30 windowed tab with an 18 × 18 hole on a post and riser, DL_PolishedSteel | leaf_L (leaf_R on v4/v5, the handed solenoid side) |

Gaps are checked every run in `door_lab_passC.py` (`hw_gaps_passG` in `passC_qa.json`); all variants pass. Unchanged in pass G: `slide_AccessPanel_hinge` keeps its name (renaming it made Gage's V-HW test the panel origin on the hinge axis, which is outside his frustums).
Gage patch: `/workspace/rook_ttqa/doorlab_passC/gage_doorlab_incr_G.patch` (against 41ce6cf):
- `door_lab_rig.gd` `_tag_rollers`: antilift `roller_r` 0.015 → 0.020.
- `door_lab_shots.gd` `_set_access_panel`: exact-name lookup of `slide_AccessPanel` (the substring lookup picked `slide_AccessPanel_hinge`, so the panel stayed closed over the head box) and a +90° open (-110° swung the panel inward through the track).
The open-pose `detail_open` framing covers x ±1.1, so the open clamps (x ±1.52) and the end stops (x ±1.93) are outside it. Gage still needs to add a closed-pose head shot or a pocket-end shot; the patch does not change that framing.

## M-122: runtime GLB edits baked into the generators (2026-11-21)
Patch M-122: Gage's lab edited the as-built GLBs at load. Found with a scratch probe (`rook_ttqa/m122/rook_m122_probe.gd`: every GLB node vs a fresh instance; logs `probe_before.log` / `probe_after.log`). Gage confirmed none is test-only. Baked:

| runtime edit (door_lab_rig.gd) | nodes / delta (pass G, 41ce6cf + incr_G) | baked as |
|---|---|---|
| `_open_pair_meeting` | `tt_door_pair_18` Leaf_L/R children (Panel, Vision_Scissor, Kick_Plate, Push_Bar, collider) ×1.001603 in x about the hinge edge, ±1.51 mm → meet 8.0 → 5.0 mm | `links_rev38.py` `MEET = .0025`: leaves run x ±0.0025…±0.895 (were ±0.004). Pivots ±0.900 and node names unchanged |
| `_trim_pair_frame` | Frame concave collider: 112 vertices, jamb inner faces x ∓0.896 → ∓0.957 on both casings ("cheek past 0.0550") | `links_rev38.py` `SWING_JAMB = .057`: the +Z (swing-side) casing jambs start at \|x\| 0.957 = hinge + 55 mm push-bar reach + 2 mm, in mesh and collider. The -Z casing stays (the leaf never swings through it); a ~62 mm reveal (0.957 - 0.895) shows beside each hinge stile on the +Z face |
| `_clamp_rods` (bulkhead) | Dog_01..08 ×0.6829, Linkage_01..08 ×0.5385 toward the shell centre (z-limited: the gear stood proud of the plug face) | housed gear: plug-face tray `TRAY_IN .024` deep to `PZ0+.0485`; dogs 14 mm thick at `PZ0+.004…+.018` in 8 slots through the tray rim (2 mm clear); U guides (1.5 mm clear strap, 0.5 mm behind the face); keepers `KEEP_IN .009`; linkages `DOG_Z1+.002…+.012`, disc behind them, lobes 2 mm off the tray floor; gearbox from `LINK_Z0-.002` |
| `_clamp_rods` (floor hatch) | Dog_01..04 ×0.4182, Linkage_01..04 ×0.4894 (y-limited: the gear hung under the lid) | underside pocket \|x\| ≤ 0.455, z -0.135…0.455, to y -0.040; dogs (y -0.095…-0.075) run in enclosed edge bores, tips 0.495 retracted / 0.520 thrown into rebate-wall keeper pockets; LockWheel and linkages raised into the pocket (`GEAR_DY .065`) |
| pocket `_pocket` loop / `_nudge_named_z` | leaf_R_seal z +3 mm (leaf_R_face too, hidden anyway) | `biparting_slide.bake_meet_seal` (`MEET_SEAL_DZ .003`) on all variants |
| `_set_access_panel` at load | slide_AccessPanel -90° about X (closing v1's baked-open panel) | v1/v4 model the panel closed (v1/v2 and v4/v5 definitions swapped) |

Check: `door_lab_passC.gear_housed()` repeats Gage's clamp criterion on the GLB (leaf_shell AABB shrunk 4 mm). Min factor is 1.0 on all 10 hatch variants, so the clamp would be a no-op; it is part of the pass criterion (`gear_housed_M122`).
Floor hatch lock gear: swing min gap 9.05 mm (was 9.62), thrown dog to keeper 3.10 mm (was 3.97), retracted dog to keeper 11.70 mm (was 13.47), all ≥ 3 mm. LockWheel to liner 327 mm (was 298). Sweeps unchanged (TorsionBar/anchor 0.002 by design).
Removal patch: `rook_ttqa/doorlab_passC/gage_doorlab_incr_M122.patch` (stacked on incr_G; also applies on bare b530847). It removes the calls and deletes `_open_pair_meeting`, `_clamp_rods`, `_trim_pair_frame`, `_hinge_swing`, `_visual_jamb_past`. `_nudge_named_z` skips GLB `leaf_*` nodes, and the QA scores hardware against its own leaf in the leaf-body frame (see below). `..._rig_only.patch` is the same without the QA hunk.
QA hunk: `_mesh_tri_depth` hw-vs-skin now runs in the leaf-body frame. In world space a 50° yawed leaf inflates the triangle AABBs, and the plane test paired bulkhead_Linkage_05 with bulkhead_Rib_back 86 mm away (0.103 m F-CLIP-HW). An exhaustive (no-stride) replica (`rook_ttqa/m122/tri_depth*.py`) finds 24 such false pairs (>30 mm) at 50° even on the pass G GLB with the clamp applied, and 0 at 0°/100° or in the leaf frame. Only the stride sampling had hidden it.
Left in, flagged (not M-122 GLB edits): `hatch_Handle` ×2 (scaled about the hinge axis, which throws it about 0.8 m off the lid, a rig bug), floor walk collider +0.12 m (test harness), bay3 Threshold_Mat -8 mm (tower asset), placements, hides/overlays (pocket skins → Gage's vision-lite), readout quads, collision layers, convex conversion, animated poses.

## REALISM_SPEC §13 (Vance, de5561f): pocket-slider end stop + solenoid (all v1–v5; handed variants follow swap_lr)
- `slide_EndStop_{L,R}` moved 4.0 mm inboard to x ±1.930–1.990 (y 2.466–2.512, z −0.044…−0.017 unchanged; `END_STOP_X` lost its +0.004). It is the primary stop. The outer carriage plate meets it at q = 1.000 (signed gap 0.0 mm, contact 46 × 19 mm in y × z), and the 2 mm overshoot squeezes the rubber −2.0 mm.
- `slide_Bumper_{L,R}` is unchanged as the backstop: leaf tail gap 25.0 mm at full open, 23.0 mm at the overshoot (≥ 20).
- `slide_Solenoid`, `slide_Solenoid_mount` and `slide_SolenoidBolt` are 6.3 mm lower (`SOL_DY`); the throw is still 18 mm (−Y).
  - Retracted tip: 7.7 mm vertically above the tab top; 8.26 mm surface distance (Vance's metric, was 14.32).
  - Thrown: 10.3 mm engagement (through the 8 mm tab, 2.3 mm below it). Window 3.0 mm radial; `bolt_thrown_to_track` 11.84 (was 16.64); `bolt_thrown_tip_to_keeper_post` 12.0.
  - Throw 18 = 7.7 + 10.3, so the ruling's "8.0 retracted" holds on the surface-distance metric, not vertically.
- Mount (advisory): front face now at z −0.024 (was −0.022). A truly flush back face at −0.019 is coplanar with `slide_Track`, which the clip check flags as z-fighting, so the back face sits 1.5 mm into the track (was 2 mm); mount z −0.024…−0.0175.
- Clip allowance (`door_lab_passC._designed_contact`, per §13.1): only the outer carriage plate vs its own `slide_EndStop` may touch, be coplanar, or overlap ≤ 2.05 mm. New clip pose `open_overshoot_2mm`; `hw_gaps_passG` adds the signed end-stop, bumper and bolt metrics with Vance's limits.
- Material slots unchanged (waiting on Sloane). Tris 5968/5968/5728/5968/5968.

## Tennis tower Rev 3.10.1 (Vance de5561f): tt_entrance_bay_3l 12 mm saddle + leaf sweeps
- Source: `assets/src/tennis_tower/rooms/temp-Arrival/entrance_bay_arrival.py` (3l only; 2-leaf/half GLBs byte-identical, keep 50 mm plinth).
- Frame: per leaf opening (x -1.6..-0.6, -0.5..0.5, 0.6..1.6) a 12 mm saddle: inside bevel z -1.720..-1.696 (0 -> 0.012), flat 0.012 z -1.696..-0.966, outside bevel z -0.966..-0.950 (0.012 -> 0.004 mat). 50 mm block kept under mullions and side jambs.
- `Leaf_{0,1,2}_Sweep` (TT_CarbonSlate, parented to each leaf): y 0.020..0.062, z -1.076..-1.064. No gasket groove existed in the leaf, so the top is bedded 2 mm into the bottom rail instead of a coplanar 0.060.
- DoorClear-colonly 4 pieces: P1 inside wedge, P2 flat 0..0.012, P3 outside wedge 0.012 -> 0.004, P4 mat strip 0..0.004. Frame-colonly opening piers now start at y 0.012 (was 0.05).
- Measured: max walk step 4.00 mm (mat edge into Deck); visual vs collider |dy| 0.00 mm on walk lanes (mullion plinth 50 mm visual vs pier collider, not walkable); sweep to sill min 8.0 mm over the full swing; tris 1964 (was 1784).
- Tower probe 11 bays x 3 lanes: 0 misses; `--qa-tower-entry` failures=0 (14 routes). Clipping closed + 21-step swing: no new overlaps/coplanars (pre-existing sidelight glass bottoms coplanar with jamb plinth, flagged not fixed). first_pass_check 0 FAIL.
- Gage door lab: his rig's runtime bay3 FloorSweep (to y 0.008) would sink 4 mm into the saddle and double the GLB sweep. `gage_doorlab_incr_saddle.patch` (on main + incr_G + incr_M122 + incr_threshold) skips it when a leaf has a GLB sweep and makes QA measure sweep-to-sill. Without it QA still passes (fails=0) but on the runtime sweep; with it, fails=0 at 60/20/15, bay3 floor 8.00 mm on the GLB sweep.

## Sloane VOTE_LOG #87 (bc70ada) DL_ slot ruling: pocket slider v1-v5
- door_lab_lib.py: BUMP -> dl_seal (DL_SealRubber), POL and YZN -> tt_alloy (TT_BrushedAlloy; the belt clamp is clear zinc now, polish only via the 2 wear rule, roughness -0.15), ACET -> tt_white (TT_WhiteComposite). DL_SolenoidRed kept. The DL_BumperRubber / DL_PolishedSteel / DL_YellowZincPlate / DL_AcetalWhite definitions are removed.
- Node names, UVs and geometry unchanged (tris 5968/5968/5728/5968/5968, passC 15/15). Every variant's GLB now lists DL_GaugeFace, DL_PearlComposite, DL_SealRubber, DL_SolenoidRed, DL_StatusLamp, TT_BrushedAlloy, TT_BrushedSteel, TT_CarbonSlate, TT_CyanLED, TT_Gunmetal, TT_WhiteComposite.
- Gage's lab _retint keys on "material + node name": slide_Bumper_* / slide_EndStop_* hit the "seal"/"rubber" branch before and after (it was "...Rubber" already), so they still get only the 0.90 clamp, no dark-lift. The acetal tyres now hit his "whitecomposite" branch (albedo 0.78/0.80/0.80, texture cleared, roughness 0.35, was the generic clamp). Keeper/bolt/belt clamp take the generic branch (0.80 albedo, no lift).

## Tennis tower Rev 3.10.2 B4 (Vance 507aef6 14.5): tt_entrance_bay_3l sidelight setting blocks
- Side_Scissor_0/1 glass bottom y 0.050 -> 0.056 (top 2.529 unchanged): glass to the 50 mm jamb block 6.0 mm (ray-measured at 9 x stations per lite).
- Side_SettingBlock_{0,1}{a,b} (TT_CarbonSlate EPDM): x -1.898..-1.798 / -1.767..-1.667 and 1.677..1.777 / 1.828..1.928, y 0.049..0.057, z -1.0825..-1.0575. Glass bed 1.0 mm (top 0.057 vs glass bottom 0.056).
  - Two deviations from the spec box, both for the coplanar rule (14.5 B2: designed contact gets a 1.0-2.0 mm bed): bottom 0.049 instead of 0.050 (sitting exactly on the 0.050 jamb-block top was flagged coplanar, Frame vs block), and 25 mm deep instead of 22 (22 = the glass thickness, so both block side faces were coplanar with the glass faces; now 1.5 mm proud each side).
- Colliders unchanged. Tris 2028 (was 1964). Clip check: the pre-existing Frame vs Side_Scissor glass coplanar pair is gone; Side_*+Frame clean at n=600/1500, worst 0.003. The full-asset check still shows a sampler-dependent Fascia_Slate/Fascia_Gunmetal(/Court_Line_LED) coplanar flag whose geometry is byte-identical to HEAD (not touched). first_pass_check 0 FAIL.
- Independent of 49d6505 (Rev 3.10.1 sill): tested in a scratch clone, `git revert 49d6505` on top of B4 reverts the generator cleanly and keeps the setting blocks (the plinth top is 0.050 either way). The 3l GLB is binary, so a revert conflicts on it and needs a re-export (regen) afterwards; PASSC_NOTES.md also conflicts (notes only).

## Pass H (Gage pass G afbbc47 / 7319f96): clip rows + brush bake
### Gage's 7 GLB-side clip rows: all lab-side (Vance 14.5 agrees: beds 4.0 mm, leaf vs frame 0.0 mm)
Re-run at HEAD + incr_M122 + threshold + saddle (rebased onto 7319f96), current GLBs. The pre-M122 runtime edits were not the cause: the same depths repeat without them. Two lab-side causes, found with a per-mesh dump and a volume re-score (winding-number inside test, distance to the nearest surface):
| door | pair | G report | rerun (poke) | true volume | cause | after (clipvol + floorframe) |
|---|---|---|---|---|---|---|
| hatch | bulkhead_HingeHeavy_frame vs frame_skin | 86 | 86 | 4.0 (vs bulkhead_frame_collar, designed bed) | poke metric: a collar vertex 4 mm under the bracket is measured to the bracket's far side face (bracket width) | 4.0 pass |
| hatch | bulkhead_damper_mount vs frame_skin | 76 | 76 | 4.0 (collar) | same | 4.0 pass |
| hatch | bulkhead_HingeHeavy_leaf vs leaf_skin | 69.7 | 69.7 | 4.0 (bulkhead_leaf_shell) | same | 4.0 pass |
| hatch | bulkhead_leaf_damper_mount vs leaf_skin | 59.7 | 59.7 | 4.0 (leaf shell) | same | 4.0 pass |
| floorhatch | hatch_HingeBearing_frame vs frame_skin | 70 | 70 | 24.8 vs the lab's runtime FloorFrameN; 4.0 vs hatch_frame | rig _floor_frame N bar (50 mm deep, z -0.078..-0.008) sits in the open hinge channel; W/E bars run 8 mm into it (12 mm) | 4.0 pass |
| floorhatch | hatch_RotaryDamper vs frame_skin | 35.8 | 35.8 / 33.0 | 24.8 FloorFrameN, 12.0 FloorFrameE; 4.0 vs hatch_frame | same | 4.0 pass |
| floorhatch | leaf_skin vs frame_skin (q 105) | 15.2 | 15.2 | 23.2 hatch_TorsionAnchor_leaf vs FloorFrameN; 0 vs the GLB frame | same (N bar) + poke | 9.2 pass |
Also over the limit in the rerun, all 0.0 mm true volume (poke-only, neighbouring-bin triangles up to 11 mm apart): floorhatch hatch_Dog_01-04 vs frame_skin 14.5, hatch_Linkage_01-04 vs leaf_skin 14.0, pocket leaf_skin vs frame_skin 15.7 (q 0).
- Not re-seated (Vance 14.5). Advisory HingeHeavy_frame vs Actuator_housing 4 mm: no gate flags it, so not separated.
- `gage_doorlab_incr_clipvol.patch` (QA): an over-limit pair is re-scored as a volume (deepest vertex inside the other closed mesh, to its nearest surface; 2.5 mm edge-cross floor kept; poke and the two mesh names logged). Pairs at or under their limit are unchanged.
- `gage_doorlab_incr_floorframe.patch` (rig): no FloorFrameN when the hatch has a hinge channel (hatch_HingeBearing_frame present), and W/E bars start at z 0.006 (2 mm past the damper).
### Brush bake (Gage pass G runtime BrushSeal moved "onto the meeting face")
- The rig adds BrushSeal at runtime to bay3 (tt_entrance_bay_3l) and pair (tt_door_pair_18) leaves; there is no brush in the biparting slide (its leaf_*_seal is unchanged). Gage's boxes floated 6 mm (bay3) / 4 mm (pair) off the approach face, ran 4 mm past the meeting edge, and the two pair brushes overlapped each other 3 mm.
- Baked as Leaf_<i>_BrushSeal (bay3, entrance_bay_arrival.py) and Leaf_<L|R>_BrushSeal (pair, links_rev38.py), TT_CarbonSlate, parented to each leaf: 6 mm wide on the -Z approach face, outer edge 1.5 mm inboard of the meeting edge, 10 mm deep with 1.5 mm bedded (B2 rule), 0.90 / 0.88 of the stile / leaf height. Inboard because any face part reaching the edge swings 0.64 mm from the bay3 mullion at 4.5 deg, and an overhang leaves its end face < 1 mm off the panel edge face (coplanar).
- `gage_doorlab_incr_brush.patch`: rig skips its BrushSeal when the leaf has a GLB brushseal; allowlist rows renamed to the per-leaf nodes (same 0.010 m seal limit).
- bay3 sweep re-hang: pass G hangs FloorSweep from the whole leaf; 49d6505's Leaf_i_Sweep already covers it (8.00 mm over the saddle), so `incr_saddle` (rebased) skips the runtime sweep when the leaf has a *_Sweep.
- Gates: tris 3l 2076, pair 576; closed clip + 21-step swing clean for the brushes (3l, pair); first_pass_check 0 FAIL (both GLBs + both sources). QA pair meet 5.00, bay3 floor 8.00, BrushSeal vs leaf 8.5 mm poke (1.5 mm true) under 0.010.

## M-123 (Patch 664c231): tt_door_pair_18 leaves vs Head_Court_Line (Vance ruling 2026-11-23: fix the strip, not the leaf)
- Reproduced on the as-built GLB (66fc9af = 679eb4e for this file) with a swing check (`rook_ttqa/m123/swing_pair.py`, `angles.py`: each leaf rotated about its pivot x -/+0.900 over 0-90 deg on the +Z swing side, fcl contact/clearance plus closed-solid containment depth). Leaf_L/R_Panel are in contact with Head_Court_Line from 6.8 to 80.7 deg (0.1 deg steps); containment peaks at 24.9 mm near 69 deg (21.4 mm at 67.5 deg), in line with Patch's 21.5-24.2 mm. Cause: both strips hung at y 2.355..2.395, below the 2.39 leaf top; the +Z one (z 0.130..0.152) is inside the swing disc.
- Fix (strip only; leaf top 2.39, the 3.5 head gap, leaf proportions, meet 5.00 mm, pivots +/-0.900, node names and BrushSeals unchanged): both strips trimmed in place to y 2.394..2.4015. Underside 4 mm over the leaf top (3.5 band 3-5 mm). The top beds 1.5 mm into the Walls_F1/F2 opening soffit (2.40, checked at all 5 placements), and the outer edge (z +/-0.1515, was +/-0.152) beds 1.5 mm into the casing head. The 40 mm visible face becomes a 6 mm soffit line, in the same place.
- Door stop: Head_Court_Line is not a stop. At 0 deg the nearest leaf point is 105 mm away, and no other head stop exists in the GLB. So there is no stop lip to keep.
- Door_Casing vs Head_Court_Line coplanar pairs (41.1 + 29.8 cm2, a 1 mm flush gap under the casing head): gone; now 1.5 mm beds (clip check overlap 0.0015, within 0.010).
- After: leaf vs Head_Court_Line 105.1 / 89.4 / 4.00 / 4.00 / 4.00 / 25.3 mm at 0 / 1 / 22.5 / 45 / 67.5 / 90 deg; fine min 4.00 mm (0.1 deg steps, 0 contacts). Full 0.25 deg swing vs every static part: no contact, Door_Casing 6.00 mm (unchanged). Tris 448 visual / 576 total (unchanged); colliders unchanged.
- Pre-existing and out of scope: the Leaf_R_Vision_Scissor vs Leaf_R_Panel coplanar row (7.0 cm2, glass top edge hidden inside the top rail).
