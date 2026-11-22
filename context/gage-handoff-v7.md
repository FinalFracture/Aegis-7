# Gage - Godot 4.7 Developer Handoff (`gage-handoff-v7.md` - 2026-11-22 self-rotation)

## 1. Predecessor Purpose & Mandatory Reference Files Manifest (READ ON FIRST TURN)
- **Role:** Gage, Godot 4.7 developer for Cylinder Hab-7 / Aegis-7.
- **Exact Purpose:** Fix bugs and build Godot 4.7 scenes (.tscn) and GDScript controllers (.gd), work QA bugs from `qa/MASTER_BUG_LIST.md`, place locked .glbs, keep the repo clean. All code goes through the Grok Build CLI on Jared's PC (section 2).
- **Repo:** [FinalFracture/Aegis-7](https://github.com/FinalFracture/Aegis-7), main only. Box clone `/workspace/game-project`. Windows checkout `C:\Users\upchu\source\Aegis-7` on machine `5ed7f5f0-bf59-4493-b9fe-629e65457357`.
- **Team ids:** PM Atlas `038035ec-9495-437e-984d-0493ca58383b`. Rook `0e05a2c3-418b-4ba6-9d9f-cdc3900cd505`. Vance `242c8419-7b14-4f27-9cdc-e87328eff983`. Patch `a5010790-2c81-497b-9869-aec9934cdfd6`. Scribe `61a860b0-0159-406a-af8c-a969dff4722b`. Tidy `1978edff-d218-42b1-98dd-dfe78b7938bc`. Sloane `0fc258d4-0dea-4cf3-ab06-338f21756ae6`.
- **Previous handoff:** `/workspace/game-project/context/gage-handoff-v6.md` (predecessor f00a0b4e-9ccf-4c20-b874-c2c1f5c9f41d, now delete-Gage).
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
  - `/workspace/game-project/context/gage-handoff-v6.md`
  - `/workspace/game-project/context/gage-handoff-v7.md` (this file)
  - `/workspace/game-project/godot/resources/door_lab/` (door profiles + contact_allowlist.json), `godot/scripts/door_lab*`, `mech_door*.gd`, `door_lab_qa.gd`, `door_lab_shots.gd`
  - `/workspace/game-project/qa/door_lab/` (runA..runG summaries; `runG/PASS_G_REPORT.md`), `context/door_lab/REALISM_SPEC.md` (Vance), `assets/src/door_lab/PASSC_NOTES.md` (Rook)
  - `/workspace/ttfix_tasks/_task_doorlab_H.txt` + `_task_doorlab_H_pending.txt` (box; H also in PC checkout root)
  - `/workspace/door_lab_shots/` (box; per-pass shot folders A..G, `G/heroes_grid_G.png`)
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
- **Counts file: SKIP.** Jared said on 2026-11-15 not to do the per-turn `context/counts/Gage.json` rule in ROTATION_RULE.md. Gage does not write it.

- **Questions to Jared:** always a tappable widget card, never prose (Jared 2026-11-20).
- **SendToAgent:** text only; image attachments fail. Send reviewers file paths instead.
- **grok launch flags now:** add `--background-wait-timeout 5400`; logs `C:\Users\upchu\aegis_shots\grok_doorlab_<X>.log/.err`.
- **Door lab commit pattern:** `git add` door_lab resources/scripts/qa/shots scripts; `git add -f` runX summary/meta/metrics/cue_log/motion*.csv (<3 MB)/*curve*.png/report; commit; `git pull --no-rebase --no-edit origin main`; push.
- **Shots to box:** one CopyToBox per file into `/workspace/door_lab_shots/<pass>/`; PIL grid 3x2 at 640x360 (5 heroes + overview).

## 3. Current State (main cc04a95, 2026-11-22 ~5 PM CT)

### !!! ALL COMPUTER WORK IS PAUSED !!!
Jared, 2026-11-21 (t43u): "Pause al work on the computer". Pass H grok (PID 3960) was killed by PID, no Godot left running, reviewers (Patch/Vance/Sloane/Rook) stopped, routine `door-lab-pass-h-recheck-1` paused. **Do not relaunch grok, ping reviewers, or resume routines until Jared explicitly says to resume.** (Jared allowed only this rotation on 11-22.)

### Mechanical door lab (Jared t7u, 2026-11-20)
- Goal: small test lab (not the full map) of Tennis Tower doors with renders, headless runs and finished-product screenshots; a reusable process for doors that work and look good. Reviewers own the bar: Patch = pass/fail quality, Vance = mechanical realism, Sloane = aesthetics, Rook = models. Iterate until all four pass, then send Jared final shots + PROCESS.md.
- Locked: snappier, game-like doors; bulkhead close stays 7.8 s; M-114 HELD.
- Passes A-G pushed (ac35bfd, b77b2a9, 4694ea7, 17180c5, 6f39e8b, 41ce6cf, afbbc47 merge 7319f96).
- **Pass G = harness FAIL**, 7 rows: hatch hinge/damper 86/76/69.7/59.7 mm, floor bearing 70, rotary damper 35.8, floor leaf vs frame 15.2. All V-* pass. Patch later showed G's clip metric (depth to triangle plane) was invalid and G was stamped from b530847 + dirty tree, not main.
- Patch verdicts on G (664c231): M-98/M-99/M-105 4th fail (Patch routed to Jared), M-112 3rd, M-119/M-120 2nd, M-122 fail, M-121 verified, new M-123 (pair head strip clip; Rook fixing in GLB), M-124 (telemetry tick stamp).
- Vance §14 (507aef6): CONDITIONAL PASS 9.6. Sloane #87 (bc70ada) scores pocket 3.88, bay3 3.63, pair 3.63, hatch 3.88, floor 3.50.
- **Pass H is written, not run:** `/workspace/ttfix_tasks/_task_doorlab_H.txt` (copied to PC checkout root). STEP 0 clean base at HEAD >= 66fc9af, delete doorlab_g_*.idx; apply Rook patches from `C:\Users\upchu\aegis_shots\` in order incr_M122, threshold, saddle, brush, clipvol, floorframe (Rook says fails=0 with all six); Patch P1-P8 (real per-pair containment, no unlogged runtime edits, M-124 tick stamp, phase tol max(10%,1 tick), cues vs motion events, seal vs frame, pair exposure + amber median/p90, pushed-tree stamp, M-120 5.0 mm on GLB); Sloane H-S1-S5 and Vance H-V3-V11 in `_task_doorlab_H_pending.txt`. Output runH dirs, mirror to `aegis_shots/doorlab_H`, `PASS_H_REPORT.md`.
- **On resume:** first check `git status` in the PC checkout (the killed run may have left half-applied patches/edits), then relaunch grok with `_task_doorlab_H.txt`. After it: commit/push runH, sync shots to `/workspace/door_lab_shots/H/`, ping Patch/Vance/Sloane/Rook (Patch asked "Ping me when pass H is on main"), send Jared screenshots. Delete or resume routine `door-lab-pass-h-recheck-1`.

### Tennis Tower
- Passes A (220d095), B (a3ac2de), ring fix (2ff7e28), C (4bea163), perf (2246095), D (fda1388) all pushed, full suite green at each.
- Jared answered: 6 bowling lanes, a Services suite, 10x20 m courts, corner stairs approved. Rook's corner stair patch: `terrace_stairs_placement_after_cheeks.patch` (not the earlier one). Vance says Rev 3.10.1 is pending Jared.
- Next: tower pass E (apply the answers above), then r3 re-audit + Page update.

### UI / interactables overhaul
- Plan `context/UI_INTERACT_PLAN.md` with Jared's decisions (see v6 section 3). Queued after door lab + tower pass E. Usage exception past 93% was approved for it through the week of 2026-11-16 only; check with Jared before relying on it now.

## 4. Waiting on Jared
- Resume order for computer work (everything paused).
- Patch-routed repeat failures M-98/M-99/M-105.
- Vance Rev 3.10.1 tower items.

## 5. Queue (after Jared resumes)
1. Door lab pass H, then iterate until Patch, Vance, Sloane and Rook all pass; final shots + PROCESS.md to Jared.
2. Tower pass E, r3 audit, Page update.
3. UI overhaul P1 HUD -> P11.

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

## Standing rule: questions to Jared (added 2026-11-20)
Every question to Jared must be sent as a tappable card/widget with answer options, never as prose. Jared, 2026-11-20 1:49 PM CT, his own words in Gage's chat: "anytime you guys ask me a question I need you to output it with a card and UI so I can tap the answer".
