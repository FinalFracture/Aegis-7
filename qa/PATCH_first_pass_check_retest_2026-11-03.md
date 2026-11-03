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
