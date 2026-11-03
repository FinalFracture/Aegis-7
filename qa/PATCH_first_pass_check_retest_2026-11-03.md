# Patch (QA) re-test: tools/first_pass_check.py @ e962d1b (2026-11-03)

Fresh clone of main at e962d1b. Test only; no .py/.gd/.tscn edited. Godot 4.7.2.stable under xvfb.

## Verdict
**PASS WITH TUNING BUGS.** Exit codes, read-only behaviour, static checks and 5/6 sabotage cases work as specified. The Godot pass runs, but its two FAILs on the main scene are false positives (FPC-01, FPC-02), so a clean scene currently can't get exit 0 with Godot on. Fix FPC-01/02 before it is used as a gate.

## Runs
| Run | PASS | WARN | FAIL | Exit | Time |
|---|---|---|---|---|---|
| main scene `--no-godot` | 18 | 16 | 0 | 0 | 0.13 s |
| `godot/ --no-godot` | 17 | 20 | 1 | 1 | 0.31 s |
| main scene `--no-godot --strict` | 18 | 16 | 0 | 1 | ~0.13 s |
| `godot/ --no-godot --strict` | 17 | 20 | 1 | 1 | ~0.31 s |
| bad path `nope/x.tscn` | - | - | - | 2 | <0.1 s |
| `--headless --import` (clone) | - | - | - | 0 | 13 s, 0 errors |
| main scene, Godot pass (xvfb) | 19 | 20 | 2 | 1 | 4 s |

Godot pass ran: probe (1078 static bodies, 4084 meshes), trimesh_two_sided (WARN 49), duplicate_static_colliders (FAIL 2101), walkable_slope (WARN 578), stair_slope (FAIL 4), surfaces_have_material (PASS), textured_without_uv (WARN 1), prop_triangles (PASS).
Stubs (WARN "not implemented"): floor_contact, subpart_overlap, portal_intrusion, capsule_escape, wall_gaps, ramp_ratio, draw_calls.

## Sabotage (throwaway copy under /tmp, never committed)
The control scene (1 StaticBody, 1 box, grey material, InputMap-only script) had no file-specific findings and exit 0.
| Sabotage | Caught by | Level | Exit |
|---|---|---|---|
| `KEY_F9` literal in .gd | input.no_hardcoded_keys | FAIL | 1 ✅ |
| duplicated CollisionShape3D | colliders.duplicate_shape_transforms | FAIL | 1 ✅ |
| node `debug_box` | names.debug_nodes | WARN | **0** ❌ (FPC-04) |
| missing res:// ext_resource in .tscn | refs.ext_resources | FAIL | 1 ✅ |
| missing res:// literal in .gd, unguarded | refs.gd_res_paths | WARN | **0** ❌ (FPC-03) |
| albedo 1.0, no texture | materials.tscn_tres | WARN | **0** ❌ (FPC-04) |
| `sab_debug.log` untracked | none (`*.log` is in .gitignore, by design) | - | 0 |
| same .log force-added | repo.no_tracked_junk | FAIL | 1 ✅ |
| untracked `sab_render_out.txt` | repo.untracked_outputs_ignored | WARN | 0 ✅ |
Every case is detected, but 3 of them WARN and so exit 0 without `--strict`.

## Noisy-check judgement
- **refs.ext_resources FAIL (2 scenes): REAL.** `utility_bot_round2_showcase.gd` and `wrist_rfid_showcase.gd` were deleted in 2f35758 (Godot 4.7 purge), but the scenes still reference them. Remove or repair the two showcase scenes.
- **textures.unused 269: mostly NOISE.** By my count, 273 of 302 tracked textures aren't referenced by name. 224 of them are GLB-extracted (`<glb_name>_<material>.png`, referenced through the GLB's import). The other 49 are under `assets/textures/` and are found by `material_loader.gd` scanning the directory and matching suffixes (`_albedo/_normal/_orm/...`). Only the `qa03/` and `removal_decals/` leftovers are worth a look. The output also prints only 8 of 269 (FPC-07).
- **refs.gd_res_paths 28–31: NOISE.** All the listed hits are fallback candidates in `*_PATHS` arrays checked with `FileAccess.file_exists`/`_resolve_path`, or output directories (`res://renders`, `res://../assets/renders`, `res://../assets/textures`). The checker only recognises `ResourceLoader.exists` as a guard.
- **textures.vram_compressed 287 lossless: REAL but low.** 288 .import files have compress/mode=0. 224 are GLB-extracted (their compression is set in the GLB import). This is a valid VRAM/perf note, not a first-pass blocker.
- **Import side effect (real hygiene finding):** after `--import`, 15 textures under `assets/textures/{qa03,removal_decals,window_cards}` gained `.import` files that aren't in git, plus `tools/qa/rook_nav13_probe.gd.uid`. The repo is missing them, and the checker doesn't detect this.

## Bugs
| ID | Pri | Bug |
|---|---|---|
| FPC-01 | High | `godot.duplicate_static_colliders` gives 2101 false positives. The key is class + origin + `size`; trimesh/convex shapes have no `size`, and GLB `_col` shapes all sit at the origin, so every shell (RevC_Shell_L1/L2/Roof...) "duplicates" every other. Key on shape resource/face hash + full transform, and FAIL only for the same shape and transform. |
| FPC-02 | High | `godot.stair_slope` FAILs on StairSetSwitchback `Flight1/2_Ramp-colonly` at 60° (stairs walk 4/4 up and 3/3 down, per QA-02). It counts every upward face of a stair trimesh, including wedge ends/edges, not the walk surface. It also flags `CylinderSpinGravityTestRing/FloorTile_08` at 40° because it measures against world +Y, while the ring's "up" is radial. Measure the main walk face (largest-area upward face), and skip or handle spin-gravity floors. The example list also mixes in walkable_slope hits. |
| FPC-03 | Med | `refs.gd_res_paths`: also treat `FileAccess.file_exists`, `_resolve_path`, and candidate `*_PATHS` arrays as guards, and ignore directory/output literals. Then promote unguarded misses to FAIL, as the message promises (sabotage currently exits 0). |
| FPC-04 | Med | `debug_*` node names and albedo ≥0.9 with no texture only WARN, so they exit 0. The checklist treats leftover debug geometry as a fail: make `names.debug_nodes` a FAIL in .tscn, with an allowlist. |
| FPC-05 | Med | `textures.unused`: resolve GLB-extracted textures through the `.glb` files and their `.import` files, and count directory-scanned `assets/textures/` as used when `material_loader` scans it. Expected to drop 269 to a handful. |
| FPC-06 | Med | Add a hygiene check for tracked assets that have no committed `.import`/`.uid` file (15 + 1 found after import). Running `--import` dirties the tree. |
| FPC-07 | Low | Details are capped at 8 (`limit=8`) with no "...and N more" line and no `--verbose`. You can't triage 269 items. |
| FPC-08 | Low | `--no-godot` still prints the 7 Godot stub WARNs, which inflates WARN counts (16 for main). Skip stubs when `--no-godot`. |
| FPC-09 | Low | `textures.vram_compressed`: exclude GLB-extracted textures (their compression comes from the GLB import) and report the 63 standalone ones separately. Keep it WARN. |
| FPC-10 | Low | `godot.trimesh_two_sided` WARN 49 is plausible, but it should limit itself to exterior/thin shells (Gage's rule 4) rather than every one-sided concave shape. |

Probe hygiene: the clone is clean after the run; the import cache and the untracked `.import`/`.uid` files were removed. Scratch under /tmp is deleted.

---

# Round 2: re-test at 4d22a4f (2026-11-03, 2:11 PM CT)

Fresh clone `/tmp/fpc_r2_patch` at 4d22a4f (only tools/first_pass_check.py changed). Test only; no .py/.gd/.tscn edited. Godot 4.7.2 under xvfb.

## Verdict
**PASS.** All ten r1 bugs (FPC-01..10) are fixed and verified. The main scene with Godot on now gives **0 FAIL, exit 0**. All 6 sabotage cases exit 1 and the clean control exits 0. One new low bug (FPC-11). Gage's 3a/3b findings are explained below. 3a is a real collider gap in game code, not a checker bug.

## Runs (r1 -> r2)
| Run | r1 P/W/F, exit | r2 P/W/F, exit | r2 time |
|---|---|---|---|
| main scene `--no-godot` | 18/16/0, 0 | **20/7/0, 0** | 0.28 s |
| `godot/ --no-godot` | 17/20/1, 1 | **19/11/1, 1** (only the real 2 deleted-script refs) | 0.30 s |
| main `--no-godot --strict` | 18/16/0, 1 | 20/7/0, 1 | 0.15 s |
| `godot/ --strict` | 17/20/1, 1 | 19/11/1, 1 | 0.29 s |
| bad path | exit 2 | exit 2 | <0.1 s |
| `--headless --import` | 0 | 0 | ~13 s |
| main scene, Godot pass | 19/20/2, 1 | **23/19/0, 0** | 5 s |

The 19 WARNs with Godot on are 7 stubs (expected), trimesh_two_sided 45 (real, see 3a), walkable_slope 1 (see 3b), textured_without_uv 1, and the repo/design WARNs.

## Sabotage (throwaway copy `/tmp/fpc_r2_patch_sab`, never committed)
| Case | Check | r1 | r2 |
|---|---|---|---|
| clean control | - | exit 0 | **exit 0**, no file-specific findings |
| `KEY_F9` literal | input.no_hardcoded_keys | FAIL, 1 | FAIL, 1 ✅ |
| duplicated CollisionShape3D | colliders.duplicate_shape_transforms | FAIL, 1 | FAIL, 1 ✅ |
| `debug_box` node | names.debug_nodes | WARN, 0 | **FAIL, 1** ✅ |
| missing res:// ext_resource | refs.ext_resources | FAIL, 1 | FAIL, 1 ✅ |
| unguarded missing res:// in .gd | refs.gd_res_paths | WARN, 0 | **FAIL, 1** ✅ |
| albedo 1.0, no texture | materials.tscn_tres | WARN, 0 | **FAIL, 1** ✅ |
| `.log`, force-tracked | repo.no_tracked_junk + repo.tracked_but_ignored | FAIL, 1 | FAIL, 1 ✅ |
| `.log` untracked (gitignored) | - (by design) | 0 | 0 |
| untracked `*render*` file | repo.untracked_outputs_ignored | WARN | WARN ✅ |

## FPC fix verification
| ID | Status | Evidence |
|---|---|---|
| FPC-01 | Fixed | duplicate_static_colliders 2101 -> 0 |
| FPC-02 | Fixed | stair_slope 0 (main walk face; 74 spin-gravity shapes skipped) |
| FPC-03 | Fixed | gd_res_paths PASS on main (1 guarded miss); the unguarded sabotage FAILs |
| FPC-04 | Fixed | debug node and white albedo now FAIL |
| FPC-05 | Fixed | textures.unused 269 -> 9, all plausibly real orphans (4 removal_decals, biome canopy, johnny5 lens, 2 ui panels, O'Neill vista) |
| FPC-06 | Fixed | repo.missing_import_uid: 15 .import + 1 .uid (matches r1 observation) |
| FPC-07 | Fixed (static) | `--verbose` prints full lists, e.g. all 9 unused textures. See FPC-11. |
| FPC-08 | Fixed | `--no-godot` no longer prints stubs (main WARN 16 -> 7) |
| FPC-09 | Fixed | 41 standalone lossless; 246 GLB-extracted excluded |
| FPC-10 | Fixed | scoped to exterior/thin shells: 49 -> 45 |

## Gage's findings
**3a. 45 one-sided trimesh colliders: REAL at runtime, not a checker artifact.** A windowed run (xvfb, opengl3) of the main scene read `backface_collision` on every ConcavePolygonShape3D under a StaticBody in scope. Both frame 1 and frame 60 showed **45 one-sided / 3029 two-sided**, so nothing set later fixes them. The M-46 line (be4159e, `preface_playable_area.gd` ~8948) only covers the unclipped `_ext_add_solid_collision` fill path. The 45 fall into three groups:
- 39 `ExteriorPlacements_v1_3/Ext_41_ext_curb_*` and `Ext_44_ext_paving_promenade_533..537` `ExtCollision` shapes. These are the per-instance **clipped** shapes from GEO-17/M-73 (z = -8.90 clip), which create a new `ConcavePolygonShape3D` without copying `backface_collision`.
- 3 `Sector4_Promenade_ExteriorPlaza/.../ExtGroundCol/ExtGroundShape`, from `_ext_add_ground_colliders()` (~line 9158), which never sets it.
- 3 `RevC_Shell_L1/L2/Roof_col` GLB-imported shells.
Suggested fix (game code, Gage): set `backface_collision = true` on the clipped shape and in `_ext_add_ground_colliders`, then decide whether the RevC shells need it. The checker WARN is correct.

**3b. ThresholdChevrons ExtGroundCol at DOOR_SECTOR4_EXIT, 50°: REAL but harmless, no snag.**
- **Geometry:** 144 faces totalling 0.0111 m². The 45–70° band is only 0.0029 m² (0.0014 m² at about 50°); the rest is vertical, 30° and 40°. It's a tiny raised chevron inlay at x ±0.91, z -9.15..-8.85. The player's floor_max_angle is 50°.
- **Probe:** door opened first (`_set_door_open_state` + `_finish_door_field`), and the player moved aside. A CharacterBody3D capsule (r 0.35, h 1.75, snap 0.35, same floor settings, **no step-up assist**, so this is a worst case) started 1.2 m back on each side and walked at 4 m/s at x = -0.6, 0, +0.6, both directions: 6/6 runs crossed the threshold at full speed, with 0 steep contacts on the chevrons.
- **Not a chevron issue:** one inbound run (x -0.6) later stopped 2.6 m inside, at z -6.48, with its head on the `StairSetSwitchback/Flight1_Ramp-colonly` underside at y 1.82. That's the stair soffit, not the chevron. FYI for Vance/Rook: check whether the area under the stair should be blocked off or kept to 2.1 m headroom.
Verdict: the WARN is accurate, but the face is a decorative sliver. Suggest allowing a minimum face area (e.g. ignore steep faces < 0.01 m² total per collider) or an allowlist entry, rather than a geometry change.

## Remaining bugs
| ID | Pri | Bug |
|---|---|---|
| FPC-11 | Low | Godot-side checks still cap examples at 5 (`ex.size() < 5`) even with `--verbose`. trimesh_two_sided listed 5 of 45. Pass `--verbose` through to the probe. |
| FPC-12 | Low | walkable_slope: add a minimum steep-face area / allowlist so decorative slivers (ThresholdChevrons, 0.0014 m² at 50°) don't WARN. |
Real project items, not checker bugs: 45 one-sided ext colliders (3a), 2 deleted-script scenes, 15 .import + 1 .uid untracked, 9 orphan textures.

Cleanup: deleted only `/tmp/fpc_r2_patch`, `/tmp/fpc_r2_patch_sab` and `/tmp/fpc_r2_patch_out`, by exact name.
