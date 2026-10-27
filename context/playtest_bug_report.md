# Cylinder Hab-7 (Aegis-7) — QA & Automated Playtest Audit Report (`playtest_bug_report.md`)

- **Date:** 2026-10-27 (CDT / UTC-5)
- **Audited By:** Patch (QA & Automated Playtester Specialist) & Gage (Godot 4 Integration Specialist)
- **Target Project:** `/workspace/game-project/godot/` (Godot `v4.3.stable.official.77dcf97d8`)
- **Primary Audited Scenes & Scripts:**
  - `/workspace/game-project/godot/project.godot`
  - `/workspace/game-project/godot/scenes/preface/preface_playable_area.tscn` & `res://scripts/preface_playable_area.gd`
  - `/workspace/game-project/godot/scripts/pcba_python_puzzle_ui.gd`
  - `/workspace/game-project/assets/src/preface_multifloor_and_johnny5_generator.py` & `patch_residential_sector_generator.py`
  - `/workspace/game-project/assets/src/generate_calm_residential_textures.py`
- **Live `F5` Verification Screenshots Saved:**
  - `/workspace/game-project/godot/renders/qa/qa_f5_hud_1st_person.png` (`1920x1080` — 1st-person view in Apt 201 with `#04` Wrist Smart-Sleeve, workbench pickups, `[E]` prompt, and diegetic HUD)
  - `/workspace/game-project/godot/renders/qa/qa_f5_hud_3rd_person.png` (`1920x1080` — 3rd-person Kaelen Rostov view in the Atrium Concourse with `#04` Wrist RFID pulse ring, `#05` Hammerhead bots, and live telemetry readout)
  - `/workspace/game-project/godot/renders/preface/preface_open_residential_building_showcase_sheet.png` (2x2 contact sheet of `res_cam_01.png` .. `res_cam_04.png`)

---

## Executive Summary: All 7 Audit Bugs (`BUG-01` .. `BUG-07`) + `[t3u]` Visual & Architectural Directives RESOLVED & VERIFIED

| Bug ID | Summary | Resolution Status |
| :--- | :--- | :---: |
| **BUG-01** | `project.godot` `run/main_scene` & `[input]` Action Map | **RESOLVED & VERIFIED** |
| **BUG-02** | Portable `res://` Path Resolution & Relative Symlinks across OSes | **RESOLVED & VERIFIED** |
| **BUG-03** | Static Trimesh + Safety Box Collisions & 1st/3rd-Person `CharacterBody3D` Controller | **RESOLVED & VERIFIED** |
| **BUG-04** | Live Looping `AnimationPlayer` Playback (`speed_scale = 1.0`) in Interactive `F5` Mode | **RESOLVED & VERIFIED** |
| **BUG-05** | Locked `#05` Hammerhead Department Bots (`Sprocket`, `Sweep`, `Kelvin [D-03 SCIENCE]`, `Clover`) | **RESOLVED & VERIFIED** |
| **BUG-06** | Interactive Pickups (`E`), Thermal Jelly (`prop_jelly_01.glb`), `#04` Wrist RFID Pulse (`R`) & Diegetic HUD | **RESOLVED & VERIFIED** |
| **BUG-07** | Unique `.tscn` UIDs & Null-Mesh Surface Guard in `_upgrade_sector_materials()` | **RESOLVED & VERIFIED** |
| **`[t3u]`** | Lower Lighting, 90/10 Controlled Saturation, World-Scaled UVs, Single Door Placards & Purposeful Interiors | **RESOLVED & VERIFIED** |

---

## Detailed Resolution Log

### BUG-01 [RESOLVED & VERIFIED]: `project.godot` Launches `res://scenes/preface/preface_playable_area.tscn` & Defines Full `[input]` Map
- `/workspace/game-project/godot/project.godot:15` sets `run/main_scene="res://scenes/preface/preface_playable_area.tscn"`.
- Full `[input]` map (`move_forward`, `move_back`, `move_left`, `move_right`, `jump`, `sprint`, `interact`, `raise_wrist`, `toggle_view`, `toggle_lighting`) is configured in `project.godot` and handled directly in `preface_playable_area.gd`.

### BUG-02 [RESOLVED & VERIFIED]: Portable `res://` Path Resolution & Zero `res://../` References
- Removed all `"res://../..."` entries from `SECTOR_GLB_PATHS`, `WRIST_04_PATHS`, `PICKUP_WIRE_PATHS`, `PICKUP_BATT_PATHS`, `PICKUP_BCI_PATHS`, `PICKUP_JELLY_PATHS`, `BOT_*_PATHS`, `COMMUTER_PATHS`, `ROSTOV_PATHS`, `TEX_DIRS`, and `OUT_DIRS` in `preface_playable_area.gd`.
- Added `func _resolve_path(p: String) -> String:` using `ProjectSettings.globalize_path(p)` so `FileAccess.file_exists()`, `GLTFDocument.append_from_file()`, `Image.load()`, and `DirAccess.make_dir_recursive_absolute()` work across Windows, macOS, and Linux regardless of clone path.

### BUG-03 [RESOLVED & VERIFIED]: Static Collisions & Walkable 1st/3rd-Person `CharacterBody3D` Player Controller
- `_assemble_open_doorless_sector()` generates static trimesh colliders (`mi.create_trimesh_collision()`) on all visible architectural meshes and adds `SectorSafetyFloorColliders` (`StaticBody3D`) covering the Ground Floor Deck (`Y = 0.0m`), Upper Level 2 North Deck (`Y = 4.20m`), Upper Level 2 West Wing (`Y = 4.20m`), and East Stair-Ramp Connector (`X = 10.65m`).
- `_setup_player_controller()` spawns `PlayerBody` (`CharacterBody3D` with `CapsuleShape3D` `radius = 0.35m, height = 1.75m`) in Apt 201 with `WASD`/Arrow movement (`5.2 m/s` walk, `8.2 m/s` sprint), `Space` jump (`4.8 m/s`), `9.8 m/s²` gravity, smooth step-up, mouse look + `Q`/`E`/Arrow look, `V`/`Tab` 1st/3rd-person toggle, `1`–`4` showcase camera presets (`0` returns to player), and `N` emergency lighting toggle.

### BUG-04 [RESOLVED & VERIFIED]: Live Looping Animations in Interactive `F5` Mode
- `_play_actor_anim()` sets `ap.speed_scale = 1.0` and `anim.loop_mode = Animation.LOOP_LINEAR` during interactive `F5` runs, while preserving `ap.speed_scale = 0.0` only when `_batch_render` or `_validate_only` is active.

### BUG-05 [RESOLVED & VERIFIED]: Locked `#05` Hammerhead Bots & Canonical `D-03 // SCIENCE` (`Kelvin #0204`)
- `BOT_SPROCKET_PATHS`, `BOT_SWEEP_PATHS`, `BOT_KELVIN_PATHS` (`BOT_PUDDLE_PATHS` alias), and `BOT_CLOVER_PATHS` prioritize the locked `#05` Hammerhead stereo-scanner liveries (`res://assets/models/char_bot_r2_05_livery_01_sprocket.glb` .. `04_clover.glb`), stationed at their functional posts.

### BUG-06 [RESOLVED & VERIFIED]: Interactive Pickups (`E`), Thermal Jelly (`prop_jelly_01.glb`), `#04` Wrist RFID Pulse (`R`) & Diegetic HUD
- Spawns `Workbench_Thermal_Jelly` (`res://assets/models/prop_jelly_01.glb`) on the Apt 201 workbench alongside `Workbench_BCI_Headband`, `Workbench_SuperWire_Spool`, and `Workbench_Battery_Cell`.
- Pressing `E` within `2.8m` collects pickups into the live HUD inventory (`BCI: 0/1 | JELLY: 0/1 | WIRE: 0/3 | BATT: 0/4`) or queries `#05` Hammerhead bots and the workbench diagnostic terminal.
- Pressing `R` triggers the `#04` Wrist Smart-Sleeve 13.56 MHz RFID pulse (`RFIDPulse` animation + expanding cyan torus wave + right-side telemetry readout of nearby tags).

### BUG-07 [RESOLVED & VERIFIED]: Unique `.tscn` UIDs & Null-Mesh Guard
- `_upgrade_sector_materials()` guards `if imp.mesh != null and imp.mesh.get_surface_count() > 0:` before `imp.mesh.get_mesh()`, and all `.tscn` scene files have unique `uid://` identifiers.

### `[t3u]` Course Correction [RESOLVED & VERIFIED]: Low-Key Lighting, 90/10 Saturation, World-Space UVs & Single Door Placards
- Reduced `tonemap_exposure` to `0.78`, `ambient_light_energy` to `0.20`, `background_energy_multiplier` to `0.35`, `AtriumGoldenHourSunlight` to `0.42`, `AtriumSkyBounceFill` to `0.16`, localized warm task `OmniLight3D`s to `0.46–0.58` (`range 5.5m–7.5m`), and `emission_energy_multiplier` to `0.55`.
- Removed column/floor neon strips, eliminated baked room numbers from architectural wall/floor regions of `residential_atrium_and_apartment_atlas_*.png`, applied world-space meter-scaled UVs (`make_world_uv_box`), and placed a single eye-level placard (`APT 201`, `APT 202`, `RM 1A`, `RM 1B`) beside each portal.
