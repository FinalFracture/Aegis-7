# QA-04: Layout & Prop Compliance (2026-11-01)
Clone: fresh `main` @ 39eba42. Report only; no game files edited.
Specs: `design/residential_roomlayout_rev_c.py`, `residential_apartment_layout_v2.md` (Rev C.2a), `residential_asset_list_rev_c.md` (C.2a), `strip4_plan.md` v2.2, `cylinder_master_plan.md`, plus `strip4_preface_layout_v1.md` (13-prop table) and `prop43_relocation.md` (Rev 3).
Code checked: `godot/scripts/preface_playable_area.gd` (`ANIMATED_PROP_SPECS`, spawn + interact wiring), all `.tscn` under `godot/scenes`.
Headless Godot 4 probe (script outside repo) loaded GLBs and listed AnimationPlayer clips.
Position tolerance: ±0.10 m vs spec rect centre; yaw must put the back to the stated wall (exact).

## Context
The Rev C residential building isn't built in Godot yet ("Plan only, no build until Jared approves"). Only the preface building (`preface_playable_area.gd`) places props. So the Rev C room-by-room checks fail for every interior prop. Some of that is by design, but it's logged so the gap can be tracked. Interim placements in the preface are checked against `strip4_preface_layout_v1.md`.

## Animation check (PASS)
| GLB | Clips found | Wired |
|---|---|---|
| folding_counter_fold_leaf_3p0 | Leaf_Fold_Up/Down | yes, toggle (Prop38) |
| folding_counter_fold_leaf_3p5 | Leaf_Fold_Up/Down | NOT placed |
| laundry_bench_wall_flip_seat | Seat_Flip_Down/Up | yes, toggle (Prop39) |
| substation_wall_ladder_busway | Cell_Swap, Port_Ready_Blink | yes, action + idle loop (Prop42) |
| spares_gravity_dispenser | Capsule_Drop, Pick_Ready_Blink | yes, action + idle loop (Prop43) |
| service_wall_rail_shuttle | sprocket_arrive, shuttle_fetch, handoff, return_idle | NOT placed / not wired |
| sprocket_lift | call_open_L1, ride_up/down, arrive_open_L1/L2, sprocket_board/exit_L1/L2, idle | NOT placed / not wired |
The interact handler plays toggles in order, then plays the action and queues the idle clip. This is correct.

## Findings
| ID | Sev | Spec ref | Expected | Actual | File |
|---|---|---|---|---|---|
| LAY-01 | High | strip4_preface_layout_v1 #4; prop43_relocation.md Rev 3 | Prop43 at (-5.16, 0.235, 5.20), yaw -90, front zone clear | Still at (-8.00, 0.235, 8.50), yaw 180. Per Vance's table this fails the front-zone check, and the lounge N wall has built-ins at x -8.79..-7.36, so it overlaps furniture | godot/scripts/preface_playable_area.gd:1830 |
| LAY-02 | High | strip4_preface_layout_v1 #5–#12 | 8 interim props placed: suit storage, lost+found bins, tea set, clutter kit, telescope, lab crates 104/204, cycler lightbox | None of these GLBs is referenced in any script or .tscn (0 hits) | godot/scripts/preface_playable_area.gd |
| LAY-03 | High | asset list #51; layout_v2 §bot lift | Sprocket lift in Maintenance/202 SW shaft (X 0.6..2.2, Z 0.8..2.4) with 9 baked clips wired to call panels | GLB has clips but isn't placed or wired | godot/assets/models/sprocket_lift.glb |
| LAY-04 | High | asset list #25/#40/#41; layout_v2 Sprocket pads | Service wall (tool wall + 3 pads + coupler arms) in 101, 201 and Maintenance, with arrive/fetch/handoff clips wired | Not placed; clips not wired | godot/assets/models/service_wall_rail_shuttle.glb |
| LAY-05 | Medium | layout_v2 L1 Maintenance; roomlayout .py L1 `sub-station` X 5.3..5.9, Z 1..3.5 (E wall, yaw -90) | Substation in Maintenance, E wall | Prop42 at (10.68, 8.35), yaw 180, hall N wall (interim building). Room, wall and facing all differ from Rev C. Accepted as interim in strip4 table #3; must move at the rebuild | preface_playable_area.gd:1821 |
| LAY-06 | Medium | layout_v2 C.2a; .py L1 bench X -3.5..-2.3, Z 6.6..7.0; lost+found X -4.3..-3.0 N wall | Bench centre (-2.9, 6.8), free-standing; lost+found on the N wall | Prop39 at (-4.10, 8.55) on the N wall, in the lost+found slot (Δ 2.2 m). The lost+found was displaced to 1B in the interim table | preface_playable_area.gd:1809 |
| LAY-07 | Medium | .py L1 `folding counter ext.` X -2.6..0.4, Z 8.3..8.9 | Centre (-1.10, 8.60) | Prop38 at (-1.85, 8.45): Δx 0.75 m, outside tolerance (interim: avoids the hall pillar) | preface_playable_area.gd:1797 |
| LAY-08 | Medium | asset list #38 (2 runs); .py L1 `folding counter` X -0.2..0.4, Z 3..6.5 | 3.5 m run (fold_leaf_3p5) on the Laundry E wall | Not placed | folding_counter_fold_leaf_3p5.glb |
| LAY-09 | Medium | strip4_preface_layout_v1 #13; asset list #18 (203) | Reading bench placed | No clear spot exists (4.0 m vs ≤3.1 m runs). Needs Jared's call: (a) rebuild, (b) 3.0 m variant, (c) plaza | — |
| LAY-10 | Medium | asset list A–H; .py L1/L2 | All 48 active Rev C items placed per room | 37 Rev C GLBs have no scene/script reference at all (bath pod, kitchen, tables, chairs, sofa, armchair, beds, bunk, wardrobe, closet, lamp, desk, toy chest, plants, W/D ×4, stair set, guards, skylight, riser, …). Blocked on the Rev C build approval | godot/scenes/*, godot/scripts/* |
| LAY-11 | Low | asset list #6, #54 | Window cards ×8, removal decals | Not modeled (known; Sloane) | — |
| LAY-12 | Low | asset list #24/#29/#33 excluded; #34 superseded | Absent from the residential build | PASS: locker_run, specimen_rack, hydro_planter, moulded_trio and shared_tray are not referenced. Lab bench, workbench, emitter bench and fold-down desk are not placed. However, the script still spawns `Hatch_D204_EmitterPanel` at (-11.20, 5.45, -5.30) as a troubleshoot object. Confirm it isn't standing in for the moved emitter bench #31 | preface_playable_area.gd:~1779 |
| LAY-13 | Low | strip4_plan v2.2 §1.1 R=200 | Assets on R=200 | Preface assets were authored to R_HULL_FLOOR=185.5 (plan says no remodel; only the bend param changes). Not verified in code | — |

## Counts
Critical 0, High 4, Medium 6, Low 3 (13 total).
