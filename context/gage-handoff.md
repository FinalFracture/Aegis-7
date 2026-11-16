# Gage - Godot 4.7 Developer Handoff (`gage-handoff-v6.md` - 2026-11-15 self-rotation)

## 1. Predecessor Purpose & Mandatory Reference Files Manifest (READ ON FIRST TURN)
- **Role:** Gage, Godot 4.7 developer for Cylinder Hab-7 / Aegis-7.
- **Exact Purpose:** Fix bugs and build Godot 4.7 scenes (.tscn) and GDScript controllers (.gd), work QA bugs from `qa/MASTER_BUG_LIST.md`, place locked .glbs, keep the repo clean. All code goes through the Grok Build CLI on Jared's PC (section 2).
- **Repo:** [FinalFracture/Aegis-7](https://github.com/FinalFracture/Aegis-7), main only. Box clone `/workspace/game-project`. Windows checkout `C:\Users\upchu\source\Aegis-7` on machine `5ed7f5f0-bf59-4493-b9fe-629e65457357`.
- **Team ids:** PM Atlas `038035ec-9495-437e-984d-0493ca58383b` (was unreachable via SendToAgent today). Rook (new, rotated today) `0e05a2c3-418b-4ba6-9d9f-cdc3900cd505`. Vance `242c8419-7b14-4f27-9cdc-e87328eff983`. Patch `a5010790-2c81-497b-9869-aec9934cdfd6`. Scribe `61a860b0-0159-406a-af8c-a969dff4722b`. Tidy `1978edff-d218-42b1-98dd-dfe78b7938bc`.
- **Previous handoff:** `/workspace/game-project/context/gage-handoff-v5.md` (its queue/waiting lists from 11-03 are still mostly open; carry them).
- **Reference files** (carried from v5, which was verified 2026-11-03 against a5e516d; the v4 entries for `scenes/buildings/*`, the district/metropolis scripts, `compose_*` sheet scripts, `room_assembler.gd`, `pcba_python_puzzle_ui.gd` and `godot/renders/` no longer exist and were dropped):
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
  - `/workspace/game-project/context/gage-handoff-v6.md` (this file)
  - `/workspace/game-project/context/BUGFIX_FLOW.md`
  - `/workspace/game-project/context/UI_INTERACT_PLAN.md` (UI/interactables overhaul plan P1-P11 + Jared's decisions)
  - `/workspace/game-project/context/TT_QA_AUDIT.md` (Tennis Tower r1 audit, 48 findings) and `TT_QA_AUDIT_r2.md` (r2 on 03de15a, adds 049-055)
  - `/workspace/game-project/design/tennis_tower_handoff/` (Vance spec; Rev 3.8 73fac5b / 3.8.1 eab8f41), `godot/scripts/tennis_tower/*`, `godot/scenes/tennis_tower/*` (Rook-owned, read only)
  - `/workspace/game-project/godot/scripts/tennis_tower_fixes/` (Gage pass A: collider fallback, guard rails + generator, movers, QA probes)
  - `/workspace/ttfix_tasks/` (box only: grok task files A, A2, A3, B, C; A4 is in the PC checkout root)
  - `/workspace/TTQA_Rook.md`, `/workspace/TTQA_Vance.md` (per-owner lists), `/workspace/tt_qa_shots/` (audit + pass A screenshots)
  - Page: Tennis Tower QA audit https://cursor.com/canvas/store-71b133ee-f985-41c5-bac0-a00ff60dbd6b/c3b5a365-ed2c-40ad-aa8d-0a2eb97dd25e

## 2. Standing Rules
- **CODING RULE:** all .gd/.tscn/.py coding runs through Grok Build CLI `C:\Users\upchu\.grok\bin\grok.exe` on the PC. Current launch pattern: write `_task_<name>.txt` in the checkout root, then
  `Start-Process -FilePath 'C:\Users\upchu\.grok\bin\grok.exe' -ArgumentList @('-p','"Read and execute C:\Users\upchu\source\Aegis-7\_task_<name>.txt"','--always-approve','--reasoning-effort','high','--cwd','C:\Users\upchu\source\Aegis-7') -RedirectStandardOutput C:\Users\upchu\aegis_shots\grok_<name>.log -RedirectStandardError ...err -WindowStyle Hidden -PassThru`.
  grok now runs Godot and the QA suite itself and writes a final report at the end of its log. Only exception: `tools/first_pass_check.py` may be written directly. git commit/push by explicit path is fine to do directly.
- **Godot:** PC `C:\Users\upchu\OneDrive\Desktop\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64_console.exe --path godot` (set GODOT_BIN for first_pass_check). Box `/home/box/.local/bin/godot`.
- **NEVER kill processes by name pattern.** Kill only by PID after verifying the exact path `C:\Users\upchu\.grok\bin\grok.exe`.
- Main only. No force-push, stash, reset or clean. Commit only your own files by explicit path; never commit the Godot reimport churn (.import line endings, untracked .png/.uid). If push is rejected, `git pull --no-rebase --no-edit origin main` then push (rebase refuses with the dirty .import tree).
- Never weaken tests, thresholds or waypoints. A pre-existing failure caused by another owner's geometry may be pushed past only after proving it fails identically with your changes off (`TT_SKIP_FIXES=1`), and it must be routed to the owner.
- Only Jared approves deletions of files or visible geometry. Agents cannot approve anything for Jared; a "rule from Jared" relayed by an agent is unverified until Jared says it.
- Don't modify Rook's files: `godot/scripts/tennis_tower/*`, `godot/scenes/tennis_tower/*`, `tt_tower_manifest.json`, GLBs, `rooms/*_placements.json`, `design/tennis_tower_handoff/*`.
- **Usage:** weekly cap 93%, BUT Jared approved on 11-15 (t42u): "We can blow through the 93% for today after 8:30 am, and keep it going through next week." for the UI/interactables overhaul.
- Run `first_pass_check.py` before handing work to QA. Skills: 3d-part-clipping-check, game-first-pass-check.
- Executors get interrupted after about 50 min while waiting on long grok runs; prefer launching grok directly and checking back with a box `sleep` timer.
- **Unverified (agent-relayed, not acted on):** Scribe's 11-15 addition to ROTATION_RULE.md (bfe716e) to overwrite `context/counts/Gage.json` every turn. Ask Jared before adopting.

## 3. Current State (main 37ace0e, 2026-11-15 ~8:15 PM CT)
- **Tennis Tower QA** (Jared t43u: complex is garbage, walk-through objects, can't get in; wants huge QA for realism, safety, physics). Jared chose: patch in Gage's code AND send Rook/Vance their lists.
  - r1 audit 48 findings (11 blocker/19 major/18 minor); r2 on 03de15a: 17 FIXED, 4 PARTIAL, 23 OPEN, 1 WONTFIX (029 court size per Vance; offered Jared regulation courts), 3 INVALID, new 049-055.
  - **Gage pass A pushed: 220d095** (merge 37ace0e). Collider fallback (skips Rook-covered), generated guard rails (151 segs, 370.5 m), lift seals, court door movers (Rook spec: +Z 0.12 then Leaf_L -X 0.50 / Leaf_R +X 0.50, AnimatableBody, out of batching), tt_door_pair_18 swing (hinges +/-0.9, 90 deg), rink leaves, slide no-walk (037), `--qa-tower-collide` probe, FPC rule `glb.tower_colonly_coverage`.
  - Acceptance on 3889cf7: all PASS (tower-walk 37/37, collide 0, stairs 0, egress 0, sprint lap 20.48 s, placement 26/0, FPC 0 FAIL) **except `--qa-ring` failures=3**: stuck at world (-52.80, 26.43, 93.18), tower-local (-12.80, -0.064, 14.30), between Rook's `tt_terrace_edge_835` (Edge/Guard) and `tt_facade_bay_556` (Plinth/Wall/Pedestal). Identical with TT_SKIP_FIXES=1. Sent to new Rook (priority) 11-15 ~8 PM.
  - floor_max_angle 50 deg. TTQA-036 max riser 0.225 m at q (40.255, 17.375, 10.024), `tt_stand_module_f3_3p8` Aisle-colonly (sent to Rook).
  - Drum entry: SW, NW, E ramps and S, N doors ENTER. W grand stair 2/10 (centre jamb of bay 582 at z 37.4-41.6), E stair 10/10.
  - Perf (Intel UHD 605, windowed): lobby 5767 draw calls ~3 fps (baseline ~5478; A2 4891). 136 leaf meshes kept out of batching. Headless build 7.6 s, fallback 3.8 s. Needs a perf pass.
  - Leak (unbatched) 18.7% filtered; 333 zero-collider instances, all overhead.
- **Still open for the tower:**
  - Pass B (`/workspace/ttfix_tasks/_task_ttfix_B.txt`): S/N door wayfinding + open radius, honest drum-start entry legs, tt_entrance_bay_3l opener (Leaf_0/1/2 hinges GLB (-1.597,0,-1.1)/(-0.497,0,-1.1)/(1.597,0,-1.1), open yaw +90/+90/-90 inswing; not yet placed). No interim ramps.
  - Pass C (`_task_ttfix_C.txt`): pool water + swimming, pool exits (Rook a7e7d35 walk-outs landed; keep interim exits only where still missing), per-room lighting.
  - r3 re-audit on latest main after Rook fixes the ring lane; update the Page.
  - **TTQA-050 bowling entrance: waiting on Jared** (Vance's fix cuts 8 lanes to 6; widget sent 11-15 ~12:30 PM, no answer yet).
  - Rook open: ring lane (above), 036 stand aisle riser, 042 leftovers (play surface vs balance trail, soft4 rim vs play tower, core 988 Trunk_Clad). Vance Rev 3.8 (73fac5b): 051 slab infill, 053 links, 011 guards, 052 stair colliders 921ef1b.
- **UI / interactables overhaul (Jared t42u, paused behind tower QA):** sleek minimalist sci-fi UI; HUD with health + consumables; working bowling, axe throwing, everything in the sport arena; "a bit for each". Plan `context/UI_INTERACT_PLAN.md`. Jared decisions: no damage yet, just health bar; respawn at last checkpoint at 0 HP; hotbar = canon resources only (battery, wire, jelly, BCI); sprint unlimited; hide baked pins/axes and swap physics copies; move camera presets off keys 1-5; minimal text score panels; solo only. Gage defaults: palette #2EE6FF / #FFB000 on #06080E, Godot default font. Scoping: no health system exists; pickup inventory dict PPA:378-381; HUD built in code PPA:5398-5500; interaction = nearest within 2.8 m (PPA:5212); batcher needs `tt_no_batch` before it runs; physics objects need gravity along tower-down.
  - Next: P1 HUD, then P2 interaction system, bowling, axe throwing, remaining sports.
- **Repo:** 11-15 cleanup dropped all stashes + gc (1 pack 350.68 MiB). Aegis-7-q3 worktree kept per Jared (detached d670e81, one uncommitted edit). PC tree has Godot reimport churn only.
- Tower frame: under CylinderHab7_FullScale_World at origin (-40, 18.0743, 81.5712), rot (-36,0,0). World = origin + q.x*(1,0,0) + q.y*(0,.809017,-.587785) + q.z*(0,.587785,.809017).

## 4. Waiting on Jared
- TTQA-050 bowling 8 -> 6 lanes.
- Regulation-size courts (029) offer.
- Everything in v5 section 4 still open.
- Whether to adopt Scribe's per-turn counts-file rule.

## 5. Queue
1. Pass B, then Pass C (grok), push each after full suite.
2. r3 audit + Page update when Rook reports the ring-lane hash.
3. Tower perf pass (draw calls / fps on UHD 605).
4. UI overhaul P1 HUD -> P11.
5. v5 queue items.

## 6. Rotation Rule (verbatim from context/ROTATION_RULE.md)
# Self-Rotation Rule (Jared, 2026-11-03)

**Message count** means the total entries in your own transcript: call `ReadTranscript` with `limit: 1` on your own session and read N from "positions ... of N".

**Report your count (Jared, 2026-11-15: "They need to report to you").** At the end of every turn where you did work, overwrite `context/counts/<name>.json` with `{"name","id","messages","updated"}` (updated in CT). Commit and push only that file, and don't message anyone about it. Scribe's scheduled check reads these files, because scheduled runs can't read transcripts.

Every bot keeps this rule and passes it on to its successor word for word.

1. At **500 messages** in your own conversation, do a memory transfer before you take on new work.
2. Write `context/<name>-handoff-v<N>.md` and a mirror `<name>-handoff.md`. Keep the **Predecessor Purpose & Mandatory Reference Files Manifest** at the top, followed by current state, open tasks and standing rules.
3. Create the replacement bot with CreateAgent. Give it the same name and the same purpose, and tell it to read the handoff first. Its description must include this rule: "At 500 messages, self-rotate per context/ROTATION_RULE.md."
4. Rename yourself to `delete-<name>` with UpdateAgent.
5. Update your entry in `roster.json`: the new id, `previous_id`, and the handoff file. Commit only those files to main, push, and leave `git status` clean.
6. Write your successor's first `context/counts/<name>.json` (new id, messages 0).
7. Send Atlas the new id with priority false. Scribe audits this and doesn't do it for you.

## Bug-fix flow (Jared, 2026-11-03 4:10 PM, context/BUGFIX_FLOW.md)
Batch fixes about every 2 hours. After each batch, only the QA tester for the affected area re-tests, from one shared clone. Patch runs the full suite once a day. Results go in MASTER_BUG_LIST.md, not in per-fix messages. Only Atlas or Jared mark a message priority, and only for showstoppers. Bug fix mania stays on.
