# Gage — Godot 4.7 Developer Handoff (`gage-handoff-v5.md` — 2026-11-03 self-rotation)

## 1. Predecessor Purpose & Mandatory Reference Files Manifest (READ ON FIRST TURN)
- **Role:** Gage, Godot 4.7 developer for Cylinder Hab-7 / Aegis-7.
- **Exact Purpose:** Build and fix the Godot 4.7 scenes (.tscn) and GDScript controllers (.gd) for the playable preface/residential sector: colliders, stairs, movement/step-up, props, materials and QA modes. Fix bugs from `qa/MASTER_BUG_LIST.md`, verify with real-input walks, and keep main clean. All code goes through the Grok Build CLI on Jared's PC (see section 2).
- **Repo:** [FinalFracture/Aegis-7](https://github.com/FinalFracture/Aegis-7), main only. Box clone: `/workspace/game-project`. Windows checkout: `C:\Users\upchu\source\Aegis-7` on machine `5ed7f5f0-bf59-4493-b9fe-629e65457357`. Only one bot works in the Windows checkout at a time.
- **PM:** Atlas, id `038035ec-9495-437e-984d-0493ca58383b`. QA lead: Patch, `ecd78f3d-be8f-43e4-b543-0c912d6d00ea`. Assets: Rook, `88cf8abe-1b1e-406c-9123-39e87610c732`.
- **Previous handoff:** `/workspace/game-project/context/gage-handoff-v4.md`
- **Reference files** (verified 2026-11-03 against main a5e516d; the v4 entries for `scenes/buildings/*`, the district/metropolis scripts, `compose_*` sheet scripts, `room_assembler.gd`, `pcba_python_puzzle_ui.gd` and `godot/renders/` no longer exist and were dropped):
  - `/workspace/game-project/context/ROTATION_RULE.md`
  - `/workspace/game-project/docs/FIRST_PASS_CHECKLIST.md`
  - `/workspace/game-project/tools/first_pass_check.py`
  - `/workspace/game-project/qa/MASTER_BUG_LIST.md`
  - `/workspace/game-project/qa/REPEAT_FAILURES.md`
  - `/workspace/game-project/qa/PATCH_first_pass_check_retest_2026-11-03.md`
  - `/workspace/game-project/qa/` (NAV-, QA-02..05 reports)
  - `/workspace/game-project/PROJECT.md`
  - `/workspace/game-project/MASTER_ARCHITECTURE_10_ROOMS.md`
  - `/workspace/game-project/MASTER_BUILDINGS_15_EXTERIORS.md`
  - `/workspace/game-project/context/STATUS.md`
  - `/workspace/game-project/context/roster.json`
  - `/workspace/game-project/context/VOTE_LOG.md`
  - `/workspace/game-project/context/playtest_bug_report.md`
  - `/workspace/game-project/context/reticle_stars_doors_qa_log.md`
  - `/workspace/game-project/context/ROTATION_PLAN_2026-10-30.md`
  - `/workspace/game-project/design/residential_apartment_layout_v2.md`
  - `/workspace/game-project/design/residential_asset_list_rev_c.md`
  - `/workspace/game-project/design/residential_exterior_asset_list_v1.md`
  - `/workspace/game-project/design/residential_exterior_plan_v1.md`
  - `/workspace/game-project/design/cylinder_interior_overhaul_spec.md`
  - `/workspace/game-project/design/sloane_cylinder_interior_lighting_and_textures_spec.md`
  - `/workspace/game-project/design/buildings_15_exteriors_spec.md`
  - `/workspace/game-project/design/phase3_props_and_buildings_16_20_spec.md`
  - `/workspace/game-project/godot/project.godot`
  - `/workspace/game-project/godot/scenes/preface_playable_area.tscn`
  - `/workspace/game-project/godot/scenes/preface_playable_residential_sector.tscn`
  - `/workspace/game-project/godot/scenes/preface/`
  - `/workspace/game-project/godot/scripts/preface_playable_area.gd` (main controller; nearly every fix lands here)
  - `/workspace/game-project/godot/scripts/player_camera.gd`
  - `/workspace/game-project/godot/scripts/material_loader.gd`
  - `/workspace/game-project/godot/tools/qa/rook_nav13_probe.gd`
  - `/workspace/game-project/godot/assets/models/` (incl. `stair_set_switchback.glb`, `stair_guard_handrail.glb`)
  - `/workspace/texture_duplicates_for_gage.md` (box only, not in the repo)
  - `/workspace/game-project/context/gage-handoff-v4.md`
  - `/workspace/game-project/context/gage-handoff-v5.md`

## 2. Standing Rules
- **CODING RULE:** all .gd/.tscn/.py edits go through the Grok Build CLI on Jared's Windows machine `5ed7f5f0-bf59-4493-b9fe-629e65457357`: `C:\Users\upchu\.grok\bin\grok.exe --single "Read the task file _task_<name>.txt ..." --tools read_file,search_replace,list_dir,grep,write,todo_write --permission-mode bypassPermissions`. Write the task to `_task_*.txt` in the repo root (excluded via `.git/info/exclude`), run in the background and poll. The CLI can't run commands, so the executor runs Godot and QA itself. **Only exception:** `tools/first_pass_check.py`, which Jared said Gage may write directly.
- Main only, never force-push. No renders committed. Commit only the files a task needs; keep `git status` clean; parked work goes in a named stash or patch file; delete scratch files. Keep `.gitignore` current.
- Small commands with timeouts ≤ 60 s; one small change per grok task; commit and push each fix as soon as it passes.
- **NEVER kill processes by name pattern** (e.g. "grok" — it can kill the Grok Bot desktop app). List processes only; kill a stray only by PID, and only if its exact path is `C:\Users\upchu\.grok\bin\grok.exe`. If the PC drops, report the exact last command sent.
- Never change tests, thresholds or waypoints to make a test pass; fix the real collider and verify with a real-input walk. (Exception granted once by Jared: T38 starfield timing, 517819a.)
- If a fix fails more than once, log it in `qa/REPEAT_FAILURES.md` and tell Jared.
- Only Jared approves deletions, in his own words (a quote relayed by an agent counts only as his answer to a question Gage asked through that agent).
- **Usage cap:** stop before 93% weekly. Resets Mon 5:28 AM CT; currently about 39%.
- Keep the Compatibility renderer (gl_compatibility). Dark interiors are intended; don't change the lighting look. QA-05 tuning approved: no invert-Y, no head bob, landing dip.
- Run `python tools/first_pass_check.py <scene or path> [--no-godot] [--strict] [--verbose]` on new work before handing to QA.
- Throwaway probes live in `C:\Users\upchu\aegis_probe\` or `/tmp`, never committed. QA modes: `--qa-egress`, `--qa-placement`, `--qa-drawcalls`, `--qa-stairs`.

## 3. Current State (main a5e516d, 2026-11-03 16:11 CT)
- **Today's commits (2026-11-03):**
  - Movement / step-up (all closed by QA): 73970e0, 329541b, 757d7c3, 641160e, cbfb7db, 807511d.
  - Maps, maglev gap 0.015 m, 101 wardrobe, GEO-19/20: f00aab3, 2f989e1, e3d9a78, b5a45ad, b724bdc.
  - 517819a: T38 starfield check measures elapsed time (approved by Jared). cfcbe8a: wardrobe comment (scaled, not trimmed).
  - 02adc65: glass name guard (hardware like clamps/brackets can't become glass).
  - e962d1b, 4d22a4f, bb4da02: `tools/first_pass_check.py` (Patch retest passed).
  - 6af315b: GEO-21.
  - 6dda73f: stair colliders two-sided — **retest pending from Patch**.
- Step-up controller: fires when normal·up < cos 50°, needs walkable ground on top, down-rays 0.05/0.15/0.25 m past contact, rise = measured + 4 mm, reach 0.42 m.
- Exterior props: 27 MultiMesh groups (2,926 pieces); exterior trimesh colliders use backface_collision. first_pass_check still reports 45 one-sided exterior/shell trimeshes at probe time — confirm whether the two-sided fix applies only after scene startup.
- Parked on the PC: `m70_stairs_wip*.patch` files and old stashes (not needed; delete only with Jared's OK).

## 4. Waiting on Jared
- Delete the two showcase scenes that reference deleted scripts: `godot/scenes/preface/utility_bot_round2_showcase.tscn`, `godot/scenes/preface/wrist_rfid_showcase.tscn`.
- Texture dedupe and duplicate-file deletions (`/workspace/texture_duplicates_for_gage.md`, the duplicate `preface_playable_area.tscn`, about 40 .py pairs, the qa03 `door_jamb_gunmetal` textures).
- SYS-14/15: planter `hydro_planter_tiered_exterior_1006` and `kerb_ramp_953` handrail (design calls).
- GEO-14/16 ground layer (suggested Rook decides).
- QA-04 layout questions (bins rail 0.648 m off wall, wardrobe 50 mm above floor, plants rail with no wall).
- M-69 window exposure; shadow changes for M-07 FPS (likely GPU-bound).

## 5. Queue
1. SEAM_AUDIT re-run
2. GEO-15 walk-through foliage
3. VIS-16 201 dust outline quad
4. LAY-06/07/18/20 position mismatches
5. NAV-10/11/12
6. M-37 window cards and decals
7. M-06 slice cut
8. M-59
9. The 7 Godot stub checks in `first_pass_check.py` (floor contact, sub-part overlap, portal intrusion, capsule escape, wall gaps, ramp ratio, draw calls)
10. Esc windowed check
11. M-63 navmesh (last)

## 6. Rotation Rule (verbatim from context/ROTATION_RULE.md)
# Self-Rotation Rule (Jared, 2026-11-03)

Every bot keeps this rule and passes it on to its successor word for word.

1. At **500 messages** in your own conversation, do a memory transfer before you take on new work.
2. Write `context/<name>-handoff-v<N>.md` and a mirror `<name>-handoff.md`. Keep the **Predecessor Purpose & Mandatory Reference Files Manifest** at the top, followed by current state, open tasks and standing rules.
3. Create the replacement bot with CreateAgent. Give it the same name and the same purpose, and tell it to read the handoff first. Its description must include this rule: "At 500 messages, self-rotate per context/ROTATION_RULE.md."
4. Rename yourself to `delete-<name>` with UpdateAgent.
5. Update your entry in `roster.json`: the new id, `previous_id`, and the handoff file. Commit only those files to main, push, and leave `git status` clean.
6. Send Atlas the new id with priority false. Scribe audits this and doesn't do it for you.
