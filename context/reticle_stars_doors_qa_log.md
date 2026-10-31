# Reticle, Rotating Outer Starfield & RFID Sliding Doors QA ([t38u])

> **Note (2026-10-30, Sloane):** Jared confirmed that the D-204 hatch and **all sector doors are force fields**, not sliding or rolling doors. `SectorRFIDSlidingDoors` is to become force fields everywhere. In code this is already done for the 6 portals since [t45u] (`SectorRFIDForceFieldDoors` in `godot/scripts/preface_playable_area.gd`). The "sliding doors" wording in the entries below is historical and kept as-is. Remaining work: `design/force_field_door_godot_changes.md`.

display=X11  failures=0

PASS | reticle_project_stretch_settings | mode=canvas_items aspect=expand
PASS | reticle_centered_1920x1080 | vp=(1920.0, 1080.0) reticle_center=(960.0, 540.0) expected=(960.0, 540.0) err=0.0000 px ray_dot=1.00000000
PASS | reticle_centered_1600x900 | vp=(1920.0, 1080.0) reticle_center=(960.0, 540.0) expected=(960.0, 540.0) err=0.0000 px ray_dot=1.00000000
PASS | reticle_centered_1280x800 | vp=(1920.0, 1080.0) reticle_center=(960.0, 540.0) expected=(960.0, 540.0) err=0.0000 px ray_dot=1.00000000
PASS | reticle_centered_1920x1080 | vp=(1920.0, 1080.0) reticle_center=(960.0, 540.0) expected=(960.0, 540.0) err=0.0000 px ray_dot=1.00000000
PASS | starfield_outer_cylinder_geometry | exists=true R=2200.0 m L=4800.0 m camera_far=6500.0 m
PASS | starfield_rotates_while_vessel_stationary | star_drot=0.0713 rad (4.09 deg) hab_dpos=0.000000 hab_drot=0.000000
PASS | starfield_pixels_visible_and_moving | changed_sky_sample_pixels=741
PASS | rfid_doors_count_6 | door_count=6
PASS | door_apt201_blocks_when_closed | door_z=2.75 player_stopped_at_z=2.33 open=false
PASS | door_apt201_opens_on_F_rfid_scan | open=true blend=1.000
PASS | door_apt201_walk_through_when_open | door_z=2.75 player_crossed_to_z=6.66
PASS | door_alcove2c_blocks_when_closed | door_z=-3.55 player_stopped_at_z=-3.13 open=false
PASS | door_alcove2c_opens_on_F_rfid_scan | open=true blend=1.000
PASS | door_alcove2c_walk_through_when_open | door_z=-3.55 player_crossed_to_z=-4.37
PASS | door_apt202_blocks_when_closed | door_z=2.75 player_stopped_at_z=2.34 open=false
PASS | door_apt202_opens_on_F_rfid_scan | open=true blend=1.000
PASS | door_apt202_walk_through_when_open | door_z=2.75 player_crossed_to_z=6.02
PASS | door_rm1a_blocks_when_closed | door_z=2.85 player_stopped_at_z=2.43 open=false
PASS | door_rm1a_opens_on_F_rfid_scan | open=true blend=1.000
PASS | door_rm1a_walk_through_when_open | door_z=2.85 player_crossed_to_z=6.15
PASS | door_rm1b_blocks_when_closed | door_z=2.85 player_stopped_at_z=2.43 open=false
PASS | door_rm1b_opens_on_F_rfid_scan | open=true blend=1.000
PASS | door_rm1b_walk_through_when_open | door_z=2.85 player_crossed_to_z=6.15
PASS | door_sector4_exit_blocks_when_closed | door_z=-8.90 player_stopped_at_z=-8.48 open=false
PASS | door_sector4_exit_opens_on_F_rfid_scan | open=true blend=1.000
PASS | door_sector4_exit_walk_through_when_open | door_z=-8.90 player_crossed_to_z=-12.20

---

## [t45u] RFID Force-Field Door QA — 2026-10-28 23:09 CDT

glb: godot/assets/models/rfid_forcefield_door.glb (Rook v2 frame, sha1 0e9b6e46702793fdd228a653006e4abc0d28cbbf) | shader: godot/shaders/forcefield_door.gdshader (Rook, unmodified) | default field_color violet (0.72,0.35,1.0,1.0), opacity 0.45

`--qa-reticle-stars-doors`: failures=0, 0 SCRIPT ERRORs. `--validate-only`: Validate OK (interactables=20). `--qa-forcefield-door`: saved 4/4.

```
PASS | reticle_project_stretch_settings | mode=canvas_items aspect=expand
PASS | reticle_centered_1920x1080 | vp=(1920.0, 1080.0) reticle_center=(960.0, 540.0) expected=(960.0, 540.0) err=0.0000 px ray_dot=1.00000000
PASS | reticle_centered_1600x900 | vp=(1920.0, 1080.0) reticle_center=(960.0, 540.0) expected=(960.0, 540.0) err=0.0000 px ray_dot=1.00000000
PASS | reticle_centered_1280x800 | vp=(1920.0, 1080.0) reticle_center=(960.0, 540.0) expected=(960.0, 540.0) err=0.0000 px ray_dot=1.00000000
PASS | reticle_centered_1920x1080 | vp=(1920.0, 1080.0) reticle_center=(960.0, 540.0) expected=(960.0, 540.0) err=0.0000 px ray_dot=1.00000000
PASS | starfield_outer_cylinder_geometry | exists=true R=2200.0 m L=4800.0 m camera_far=6500.0 m
PASS | starfield_rotates_while_vessel_stationary | star_drot=0.0720 rad (4.13 deg) hab_dpos=0.000000 hab_drot=0.000000
PASS | starfield_pixels_visible_and_moving | changed_sky_sample_pixels=749
PASS | rfid_doors_count_6 | door_count=6
PASS | door_apt201_forcefield_shader_material | shader=res://shaders/forcefield_door.gdshader field_color=b859ffff
PASS | door_apt201_closed_state | dissolve=0.000 collision_on=true light=c47d2b
PASS | door_apt201_blocks_when_closed | door_z=2.75 player_stopped_at_z=2.30 open=false
PASS | door_apt201_F_scan_dissolves_open | during_tween dissolve=0.033 light_amber=true collision_on=true | after dissolve=1.000 collision_off=true light=3faf6a
PASS | door_apt201_walk_through_when_open | door_z=2.75 player_crossed_to_z=6.66
PASS | door_apt201_F_scan_closes_back | dissolve=0.000 collision_on=true light=c47d2b
PASS | door_alcove2c_forcefield_shader_material | shader=res://shaders/forcefield_door.gdshader field_color=b859ffff
PASS | door_alcove2c_closed_state | dissolve=0.000 collision_on=true light=c47d2b
PASS | door_alcove2c_blocks_when_closed | door_z=-3.55 player_stopped_at_z=-3.10 open=false
PASS | door_alcove2c_F_scan_dissolves_open | during_tween dissolve=0.033 light_amber=true collision_on=true | after dissolve=1.000 collision_off=true light=3faf6a
PASS | door_alcove2c_walk_through_when_open | door_z=-3.55 player_crossed_to_z=-4.37
PASS | door_alcove2c_F_scan_closes_back | dissolve=0.000 collision_on=true light=c47d2b
PASS | door_apt202_forcefield_shader_material | shader=res://shaders/forcefield_door.gdshader field_color=b859ffff
PASS | door_apt202_closed_state | dissolve=0.000 collision_on=true light=c47d2b
PASS | door_apt202_blocks_when_closed | door_z=2.75 player_stopped_at_z=2.29 open=false
PASS | door_apt202_F_scan_dissolves_open | during_tween dissolve=0.033 light_amber=true collision_on=true | after dissolve=1.000 collision_off=true light=3faf6a
PASS | door_apt202_walk_through_when_open | door_z=2.75 player_crossed_to_z=6.02
PASS | door_apt202_F_scan_closes_back | dissolve=0.000 collision_on=true light=c47d2b
PASS | door_rm1a_forcefield_shader_material | shader=res://shaders/forcefield_door.gdshader field_color=b859ffff
PASS | door_rm1a_closed_state | dissolve=0.000 collision_on=true light=c47d2b
PASS | door_rm1a_blocks_when_closed | door_z=2.85 player_stopped_at_z=2.40 open=false
PASS | door_rm1a_F_scan_dissolves_open | during_tween dissolve=0.033 light_amber=true collision_on=true | after dissolve=1.000 collision_off=true light=3faf6a
PASS | door_rm1a_walk_through_when_open | door_z=2.85 player_crossed_to_z=6.15
PASS | door_rm1a_F_scan_closes_back | dissolve=0.000 collision_on=true light=c47d2b
PASS | door_rm1b_forcefield_shader_material | shader=res://shaders/forcefield_door.gdshader field_color=b859ffff
PASS | door_rm1b_closed_state | dissolve=0.000 collision_on=true light=c47d2b
PASS | door_rm1b_blocks_when_closed | door_z=2.85 player_stopped_at_z=2.40 open=false
PASS | door_rm1b_F_scan_dissolves_open | during_tween dissolve=0.034 light_amber=true collision_on=true | after dissolve=1.000 collision_off=true light=3faf6a
PASS | door_rm1b_walk_through_when_open | door_z=2.85 player_crossed_to_z=6.15
PASS | door_rm1b_F_scan_closes_back | dissolve=0.000 collision_on=true light=c47d2b
PASS | door_sector4_exit_forcefield_shader_material | shader=res://shaders/forcefield_door.gdshader field_color=b859ffff
PASS | door_sector4_exit_closed_state | dissolve=0.000 collision_on=true light=c47d2b
PASS | door_sector4_exit_blocks_when_closed | door_z=-8.90 player_stopped_at_z=-8.45 open=false
PASS | door_sector4_exit_F_scan_dissolves_open | during_tween dissolve=0.034 light_amber=true collision_on=true | after dissolve=1.000 collision_off=true light=3faf6a
PASS | door_sector4_exit_walk_through_when_open | door_z=-8.90 player_crossed_to_z=-12.20
PASS | door_sector4_exit_F_scan_closes_back | dissolve=0.000 collision_on=true light=c47d2b
PASS | set_door_field_opacity_color_emitter | opacity=0.400 color=00ffffff emitters[EmitterStrip=00ffff@2.5, EmitterNodes=00ffff@3.0, Conduits=00ffff@1.6] other_door_opacity=0.450
PASS | set_door_field_clamps_opacity | 7.0->1.00 -3.0->0.00
PASS | door_field_json_overrides | applied=7 rm1a_opacity=0.70 rm1b_opacity=0.45 json=res://config/door_fields.json
PASS | interior_loaded_at_start | status={ "interiors_loaded": true, "managed_count": 25, "detached_nodes": 0, "live_pickups": 9, "collected_ids": [], "door_type": "rfid_forcefield" }
PASS | pickup_collected_before_exit | collected=["Workbench_BCI_Headband"] inv_bci=1
PASS | interior_despawn_on_promenade_exit | z=-12.0 loaded=false managed=24 props_left=0 interior_actors_left=0 workbench_in_tree=false doors=6
PASS | interior_respawn_on_vestibule_reentry | z=-6.0 loaded=true live_pickups=8 (before exit 8) collected_bci_respawned=false interior_actors=9 workbench_in_tree=true
```

---

### [QA 129b91d fixes] — Gage, 2026-10-28 23:36 CDT
- **QA-FF-01 RESOLVED:** before a close, `_door_opening_blocker()` overlap-tests the 1.50 × 2.45 × 0.60 m opening (physics `intersect_shape` for CharacterBody3D/RigidBody3D plus an origin test of collider-less bots/props). If anything is inside, the close is held (field open, collision off) and retried every 0.5 s until clear. QA: bot held 2 retries then closed, rigid crate held then closed. PASS 3/3.
- **QA-FF-02 RESOLVED:** `INTERIOR_DESPAWN_Z` -14.0 / `INTERIOR_RESPAWN_Z` -13.0 (1 m hysteresis); interiors stay loaded while `DOOR_SECTOR4_EXIT` is open or opening. QA: thresholds, loaded at z=-16 with the exit open, despawn at -16 with it closed, still despawned at -13.5, respawn at -12.5. PASS 5/5.
- **QA-FF-03 RESOLVED:** RFID panel +10 mm, StatusLight +14 mm (light face ~5 mm proud of the panel face instead of 1 mm).
- **QA-FF-04 RESOLVED:** `tools/door_field_ui.py` lazy-imports tkinter; `--set DOOR_ID|ALL --opacity X --color r,g,b[,a]` writes JSON and exits; `--user` / `--user-dir` / `--print-paths`. Game reads `res://config/door_fields.json` when `OS.has_feature("editor")`, else `user://door_fields.json` (exact user folder printed at boot). `godot/config/` gitignored. py_compile + `--set` round-trip verified.
- **QA-FF-05 HARDENED:** reticle uses `PRESET_CENTER` anchors + `GROW_DIRECTION_BOTH` (no manual positioning). Centering QA still 0.000 px at all 4 sizes; Windows embedded-Game-view repro still pending (needs Jared's Windows run).
- Full run `--qa-reticle-stars-doors`: 58 PASS / 0 FAIL, 0 script errors; `--validate-only` OK.

---

## [Bulkhead Hub] door_hub_bulkhead.glb on all 6 force-field doors — Gage, 2026-10-29 04:08 CDT

`--qa-reticle-stars-doors`: 73 PASS / 0 FAIL, 0 script errors (hub mounted at door-local (1.14,0,0.15)+0.022 m standoff on 6/6, [F] target = ScanZone, 8 glow parts amber→#3FAF6A on grant and back on close, coupler arm stowed x6 / deploys on Sprocket dock RM1B / sprocket_dock() hook). `--validate-only` OK. Screenshot: godot/renders/qa/door_hub_ingame_rm1b.png. Dock pads lifted to the measured floor (ground floor +0.115 m, upper +0.025 m).

```
PASS | door_apt201_bulkhead_hub_mounted | hub=DoorHub_DOOR_APT201 pos_err=0.0000 m rot_err=0.0000 offset=(1.14, 0.0, 0.15)+standoff 0.022 scan_target=ScanZone
PASS | door_apt201_hub_8_glow_parts_green_on_grant | parts=8 emission=3faf6a
PASS | door_alcove2c_bulkhead_hub_mounted | hub=DoorHub_DOOR_ALCOVE2C pos_err=0.0000 m rot_err=0.0000 offset=(1.14, 0.0, 0.15)+standoff 0.022 scan_target=ScanZone
PASS | door_alcove2c_hub_8_glow_parts_green_on_grant | parts=8 emission=3faf6a
PASS | door_apt202_bulkhead_hub_mounted | hub=DoorHub_DOOR_APT202 pos_err=0.0000 m rot_err=0.0000 offset=(1.14, 0.0, 0.15)+standoff 0.022 scan_target=ScanZone
PASS | door_apt202_hub_8_glow_parts_green_on_grant | parts=8 emission=3faf6a
PASS | door_rm1a_bulkhead_hub_mounted | hub=DoorHub_DOOR_RM1A pos_err=0.0000 m rot_err=0.0000 offset=(1.14, 0.0, 0.15)+standoff 0.022 scan_target=ScanZone
PASS | door_rm1a_hub_8_glow_parts_green_on_grant | parts=8 emission=3faf6a
PASS | door_rm1b_bulkhead_hub_mounted | hub=DoorHub_DOOR_RM1B pos_err=0.0000 m rot_err=0.0000 offset=(1.14, 0.0, 0.15)+standoff 0.022 scan_target=ScanZone
PASS | door_rm1b_hub_8_glow_parts_green_on_grant | parts=8 emission=3faf6a
PASS | door_sector4_exit_bulkhead_hub_mounted | hub=DoorHub_DOOR_SECTOR4_EXIT pos_err=0.0000 m rot_err=0.0000 offset=(1.14, 0.0, 0.15)+standoff 0.022 scan_target=ScanZone
PASS | door_sector4_exit_hub_8_glow_parts_green_on_grant | parts=8 emission=3faf6a
PASS | hub_coupler_arm_stowed_by_default_x6 | stowed_deg=90.0
PASS | hub_arm_deploys_on_sprocket_dock_rm1b | marker=SprocketDock_DOOR_RM1B parked_deg=0.0 after_leave_deg=90.0
PASS | hub_sprocket_dock_hook | hook parked_deg=0.0 released_deg=90.0
```

---

## [QA-HUB-01] single-target [E] hub scan — 2026-10-29 04:42 CDT

`--qa-reticle-stars-doors`: 80 PASS / 0 FAIL, 0 script errors; `--validate-only` OK.

```
PASS | door_apt201_E_scan_dissolves_open | during_tween dissolve=0.034 glow_not_yet_green=true collision_on=true | after dissolve=1.000 collision_off=true light=3faf6a
PASS | door_apt201_E_scan_closes_back_glow_amber | dissolve=0.000 collision_on=true light=ff9500
PASS | door_alcove2c_E_scan_dissolves_open | during_tween dissolve=0.034 glow_not_yet_green=true collision_on=true | after dissolve=1.000 collision_off=true light=3faf6a
PASS | door_alcove2c_E_scan_closes_back_glow_amber | dissolve=0.000 collision_on=true light=ff9500
PASS | door_apt202_E_scan_dissolves_open | during_tween dissolve=0.034 glow_not_yet_green=true collision_on=true | after dissolve=1.000 collision_off=true light=3faf6a
PASS | door_apt202_E_scan_closes_back_glow_amber | dissolve=0.000 collision_on=true light=ff9500
PASS | door_rm1a_E_scan_dissolves_open | during_tween dissolve=0.033 glow_not_yet_green=true collision_on=true | after dissolve=1.000 collision_off=true light=3faf6a
PASS | door_rm1a_E_scan_closes_back_glow_amber | dissolve=0.000 collision_on=true light=ff9500
PASS | door_rm1b_E_scan_dissolves_open | during_tween dissolve=0.032 glow_not_yet_green=true collision_on=true | after dissolve=1.000 collision_off=true light=3faf6a
PASS | door_rm1b_E_scan_closes_back_glow_amber | dissolve=0.000 collision_on=true light=ff9500
PASS | door_sector4_exit_E_scan_dissolves_open | during_tween dissolve=0.034 glow_not_yet_green=true collision_on=true | after dissolve=1.000 collision_off=true light=3faf6a
PASS | door_sector4_exit_E_scan_closes_back_glow_amber | dissolve=0.000 collision_on=true light=ff9500
PASS | qa_hub_01_scan_toggles_only_rm1b | rm1b_open=true apt202_open=false apt202_dissolve=0.00 doors_open=1 prompt='[E] RFID SCAN // RM 1B SUBSTATION // RFID FORCE-FIELD DOOR // OPEN'
PASS | qa_hub_01_scan_close_held_while_occupied | held=true then open=false dissolve=0.000
PASS | qa_hub_01_facing_away_noop | rm1b_open=false dissolve=0.00 prompt=''
PASS | qa_hub_01_out_of_range_noop | dist=2.74 m any_door_open=false
PASS | qa_hub_01_far_side_of_wall_noop | dist=1.24 m (in range) rm1b_open=false
PASS | qa_hub_01_E_toggles_door_not_pickup | rm1b_open=true pickup=SUPER-WIRE SPOOL in_reach=true collected=false inventory_unchanged=true
PASS | qa_hub_01_player_on_dock_pad_can_close | open=false pending=false blocker='Hammerhead05_Kelvin_0204_Science' dissolve=0.000 dist_to_scanzone=1.13
```

---

### [REAL-01..03] resolution (Gage, 2026-10-29 05:04 CDT)
- **REAL-03 DONE:** `_zone_name` shows RM 1A / RM 1B only inside `ROOM_1A_INTERIOR` / `ROOM_1B_INTERIOR`. These are AABBs from the sector glb shells (`Side_Room_East_Lounge` x[-12.25,-4.75] z[2.76,7.98]; `Side_Room_West_Storage` x[0.75,8.25] z[2.76,8.16]), inset 0.15 m for the walls, and they start behind the door wall (z ≥ 3.00). Everywhere else on L1 falls back to the concourse/vestibule/promenade names. QA `real_03_room_zone_labels_interior_only`: room centres labelled; the corridor outside each door (z 2.2), x -13.2 and x -2.0 are not.
- **REAL-02 DONE:** `MezzanineGlassBalustrade_North` (15.2 × 1.06 × 0.06 m @ z 1.25) and `_West` (0.06 × 1.06 × 7.6 m @ x -7.55) are StaticBody3D boxes matching the glb panes (y 4.405–5.465). Neither touches the east stair (x ≥ 9.16) or any doorway. QA `real_02_glass_balustrade_collider_hit`: 6/6 rays across the runs, masked to the glass layer, hit the right run. Note: on the north run at y 4.9, an unmasked ray hits `Upper_Mezzanine_Walkway_col` first, so part of that edge was already covered.
- **REAL-01 DONE (backing panel):** `_fit_hub_backing()` casts 9 rays from each hub face straight back. Where any finds no solid within 5 cm, it adds a wall-toned gunmetal backing plinth with a collider (0.695 × 1.44 × 0.25 m, face 2 mm proud of the hub's wall plane). ALCOVE2C had 6/9 rays with no wall even within 0.20 m (the void Patch found). **All 5 other hubs also got a plinth:** the baked wall faces sit 5–20 cm behind the 0.30 m frame plane at every portal (3–6/9 rays missed at 5 cm; 9/9 hit within 20 cm). QA `<door>_hub_solid_wall_behind_5cm`: 6/6 doors, 0 misses. No render was taken, so the plinth look (and the door frame/infill standing proud of the real wall) needs a visual check.
- `--qa-reticle-stars-doors` 88 PASS / 0 FAIL, 0 script errors; `--validate-only` OK.
