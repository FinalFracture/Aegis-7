# Force-field doors: Godot change list (for Gage)
_Sloane, 2026-10-30 (CDT). Read-only audit of `godot/`; no game code was edited._

**Decision (Jared):** the D-204 hatch and all sector doors are **force fields**, not sliding, rolling or leaf doors. The updated design specs are `design/preface_test_environment_and_wrist_spec.md` §2 and §4.2, and `design/chapter_01_solar_flare_and_preface_spec.md` Beat 2. The UI boards are in `design/ui/troubleshoot_final/` and `design/ui/troubleshoot_simple_final/`.

## Current state (already a force field, keep it)
`godot/scripts/preface_playable_area.gd` already builds force fields for all 6 Residential portals ([t45u]):
- `_build_rfid_forcefield_doors()` (~:3746) builds the `SectorRFIDForceFieldDoors` root and covers `DOOR_APT201`, `DOOR_ALCOVE2C`, `DOOR_APT202`, `DOOR_RM1A`, `DOOR_RM1B` and `DOOR_SECTOR4_EXIT` (~:3757-3763).
- **Model and shader:** `rfid_forcefield_door.glb` (Frame, FrameInset, EmitterStrip, RFIDPanel, StatusLight, FieldPlane) with `shaders/forcefield_door.gdshader` (opacity, dissolve, static, arcs, jitter).
- **Colliders:** jamb and header are static; `FieldCollider` is toggled (~:3826-3835, toggled at ~:4090).
- **RFID gating:** an [E] scan at the `door_hub_bulkhead.glb` ScanZone; `_set_door_open_state()` (~:4131) dissolves the field over 0.8 s and only then switches the collider. QA-FF-01 keeps the field open while something is standing in the opening.
- **Python hook:** `set_door_field(door_id, opacity, color)` (~:4176) plus `door_fields.json` polling.

No sliding leaves, tweens or leaf colliders are left in the 6-portal logic.

## Changes needed
| # | File / node | Replace or remove | New behaviour |
|---|---|---|---|
| 1 | `preface_playable_area.gd` `_remove_all_doors_and_grates()` (~:432-441); baked nodes `*door_slide*`, `*door_leaf*` and `*door_apt*` inside `preface_residential_sector.glb` | The baked sliding leaves are only **hidden**. They get no collider only because `_add_sector_trimesh_collisions()` skips invisible meshes (~:472). | Ask Rook to strip the leaf and slide meshes from the sector GLB (or `free()` them instead of hiding them). Rename the helper, e.g. `_remove_baked_leaf_doors_and_grates`. No behaviour change. |
| 2 | `preface_playable_area.gd`: door state machine (`_set_door_open_state` / `_update_rfid_doors`, ~:4131 and ~:4244) | Currently binary (open/closed dissolve). | Add a **`STALL` / partial-power state**: field at ~40% strength, irregular flicker (drive `opacity` and `static_strength`/`jitter_strength`/`arc_strength` with noise), **collider stays ON**, amber hub light, then a surge back to 100% after ~2 s. Use it for failed or partial-power scans (Preface Scan 1, solar-flare brownouts). Also add a short **deny flicker** (0.3 s amber pulse) for a refused RFID scan. |
| 3 | `rfid_forcefield_door.glb` `FieldPlane`, and the field material per door | One plane. | For the preface puzzle door, support **two halves** (`FieldPlane_A` and `FieldPlane_B`, Phase A/B), each with its own ShaderMaterial and collider (`FieldCollider_A/B`). Scan beats: A drops while B holds → B drops while A comes back → droid holds A → sync both → field collapses. Optional `Emitter_Coil_A/B` emissive phase bars in the header. |
| 4 | `godot/scenes/preface/preface_service_call_test.tscn` (`DoorContainer`, line ~37) | The scene references `res://scripts/preface_service_call_test.gd`, **which doesn't exist**, and `DoorContainer` is empty. `prop_service_door.glb` (the old leaf door spec) was never built. | Build the service-call door as a force-field emitter frame: reuse `rfid_forcefield_door.glb` at the 2.40 × 2.60 m frame, add the split field from #3, the stall state from #2, 3 header calibration nodes (`Node_Calib_01..03`) and the RFID pedestal. Follow the 3-cycle table in the preface spec §2. |
| 5 | `godot/scripts/pcba_python_puzzle_ui.gd` (used by `preface_playable_area.tscn` and `preface_playable_residential_sector.tscn`) | It still uses door/bulkhead wording: line 10 `def open_door(amperage)`, line 117 "SLIDE +5A BATTERY", line 200 the `open_door` label, line 289 `"[BULKHEAD 100% UNLOCKED!]"` / `"[DOOR JAMMED AT 40%]"`. | Reword for a field, e.g. `"[FIELD RELEASED]"` / `"[FIELD STALLED AT 40%]"` and `enable_field()`. Longer term, replace it with the new troubleshoot UIs (`design/ui/troubleshoot_simple_final/`: `FIELD_PIN`, commit-on-Enter, EXIT-only; `design/ui/troubleshoot_final/`: `enable_field`, `FIELD_OK`). |
| 6 | QA: `--qa-reticle-stars-doors` / `--qa-forcefield-door` (~:308-312) | Logs still say "Sliding Doors" (see the notes in `context/`). | Add QA checks for the stall state: the collider stays on at partial strength, nothing can pass during the flicker, and the field releases only from full sync. |

## Behaviour spec (all force-field doors)
- **Emitter frame** with emitter rails or strip, a header and status light; the hub carries the RFID panel.
- **Translucent field mesh:** shader opacity ~0.45, colour by state. Locked/lockout = amber tint, ready = cyan/violet (the current in-game default is violet), released = dissolved. The collider is on whenever field strength is above 0.
- **RFID gating** stays as it is (hub ScanZone, single-target [E], QA-FF-01 blocker hold-open).
- **Fail or partial power:** the STALL flicker, deny pulse and solar-flare brownout reuse the same state. Never leave a passable gap while stalled.
- **D-204 hatch:** the troubleshoot puzzle target (`DEVICE: Hatch Field Emitter D-204`). On a win it runs the normal release dissolve. Success never closes the UI; the player exits it.

## Textures / materials needed from Sloane
1. **Lockout amber field variant** and a **stall/flicker noise mask** (tileable, 512²) for `FieldPlane` (the existing one is `rfid_forcefield_door_Mat_FF_FieldPlane.png`).
2. **Split-field seam treatment** for Phase A/B halves: centre emitter edge glow strip, albedo + emission.
3. **Emitter coil bank** atlas: brushed steel `#88929E` coils plus `#D95B26` coil-phase indicator bars, emission mask with 3 states (in phase, out of phase, off).
4. **Header calibration nodes** `Node_Calib_01..03` emission states (off / amber / cyan).
5. **Threshold strip** amber → cyan states (extending `Mat_FF_Threshold_Chevron`).
6. **Inspection transom glass** over the emitter header (BLEND, alpha ~0.32) for the preface room.

All of these will be ORM-packed (R = AO, G = roughness, B = metallic) to match the existing atlas conventions.
