# Patch — QA Lead & Automated Playtester Handoff (`patch-handoff-v3.md` — 2026-11-03 500-message rotation)

## 1. Predecessor Purpose & Mandatory Reference Files Manifest (READ ON FIRST TURN)
- **Role:** QA lead & automated playtester for Cylinder Hab-7.
- **Purpose:** Run automated/headless Godot playtest passes on Cylinder Hab-7 (Godot **4.7.2**, headless under **xvfb**, renderer **gl_compatibility**; always run `--headless --import` first), coordinate QA-01..05 and MAP-QA-1..5, verify fixes, keep `qa/MASTER_BUG_LIST.md` and `qa/REPEAT_FAILURES.md` current, run the full suite (including planted bugs) once a day.
- **Repo:** `/workspace/game-project`, github.com/FinalFracture/Aegis-7 — **main only, no branches, never force-push.**
- **Previous handoffs:** `context/patch-handoff-v2.md`, `context/patch-handoff-v1.md`
- **Read first:**
  - `PROJECT.md`
  - `context/STATUS.md`
  - `context/roster.json`
  - `context/VOTE_LOG.md`
  - `context/ROTATION_RULE.md`
  - `context/BUGFIX_FLOW.md`
  - `docs/FIRST_PASS_CHECKLIST.md`
  - `qa/MASTER_BUG_LIST.md`
  - `qa/REPEAT_FAILURES.md`
- **v2 Section 1 role refs (still relevant):** `context/usage_budget.json`, `godot/project.godot`, `design/residential_apartment_layout_v2.md`, `design/residential_asset_list_rev_c.md`, `design/residential_exterior_asset_list_v1.md`, `design/residential_exterior_plan_v1.md`, `context/playtest_bug_report.md`, `godot/scenes/preface_playable_area.tscn`, `godot/scenes/preface_playable_residential_sector.tscn`, `godot/scripts/preface_playable_area.gd`, `context/cylinder_gravity_qa_log.md`, `context/hand_controls_qa_log.md`, `context/reticle_stars_doors_qa_log.md`, `godot/renders/qa/` (ignored output). `ROTATION_PLAN_2026-10-30.md` is historical.

## 2. Rotation Rule (copied word for word from context/ROTATION_RULE.md)
**At 500 messages, self-rotate per context/ROTATION_RULE.md.**

> # Self-Rotation Rule (Jared, 2026-11-03)
>
> Every bot keeps this rule and passes it on to its successor word for word.
>
> 1. At **500 messages** in your own conversation, do a memory transfer before you take on new work.
> 2. Write `context/<name>-handoff-v<N>.md` and a mirror `<name>-handoff.md`. Keep the **Predecessor Purpose & Mandatory Reference Files Manifest** at the top, followed by current state, open tasks and standing rules.
> 3. Create the replacement bot with CreateAgent. Give it the same name and the same purpose, and tell it to read the handoff first. Its description must include this rule: "At 500 messages, self-rotate per context/ROTATION_RULE.md."
> 4. Rename yourself to `delete-<name>` with UpdateAgent.
> 5. Update your entry in `roster.json`: the new id, `previous_id`, and the handoff file. Commit only those files to main, push, and leave `git status` clean.
> 6. Send Atlas the new id with priority false. Scribe audits this and doesn't do it for you.

## 3. Bug-Fix & Review Flow (current, context/BUGFIX_FLOW.md)
- **Bug fix mania stays on:** bugs get fixed nonstop; only coordination changed.
- **Per-stage checklists** at `qa/checklists/<area>-<stage>.md`, one checkbox per involved bot (`- [ ] Gage`). Check **only your own** box and commit. The **last checker** messages the next party **once, priority false** (devs done -> area QA tester; QA done -> owning dev(s)), then deletes the checklist file and commits. Whoever starts a stage (normally Atlas) creates the checklist.
- **One targeted re-test per checklist:** only the touched area's QA tester re-tests, from **one shared clone per stage** (not a fresh clone per commit). **Patch runs the full suite, including planted bugs, once a day.**
- **Results go in `qa/MASTER_BUG_LIST.md`**, not per-fix messages. Devs read it at batch start. One batch summary to Atlas is fine.
- **Priority:** only Atlas or Jared mark priority, showstoppers only (crash, broken build, blocked work). All bot-to-bot messages priority false; no duplicates.
- **The "Tonight: re-test Gage's pushes" routine is retired.**

## 4. Team
| Bot | Id | Area |
|---|---|---|
| Atlas | 038035ec-9495-437e-984d-0493ca58383b | Coordinator; relays Jared |
| Gage (rotated) | 957f052a-7abe-425c-85f5-fa21b72010e3 | Code/scene dev; owns `tools/first_pass_check.py` |
| Rook (rotated) | 072eeb38-1722-4809-9578-877c508585e4 | Meshes / GLBs |
| QA-01 | see roster.json | Navigation |
| QA-02 | see roster.json | Geometry & collision |
| QA-03 | see roster.json | Visuals / lighting |
| QA-04 | see roster.json | Layout |
| QA-05 | see roster.json | Stability, input, performance |
| MAP-QA-1 | 50e1ded3-c965-47f7-b2c0-5e9f38487a79 | Traversal |
| MAP-QA-2 | 9472d81b-b3a1-4cf8-ab5f-3678a66ff3c0 | Collision edges / falls |
| MAP-QA-3 | 7798ced8-f74d-403a-96e6-1a6ed03729fa | Stairs / ramps |
| MAP-QA-4 | b4acc9ab-159c-4a5c-82fd-ac532234de8f | Exterior / tram |
| MAP-QA-5 | 1de5e3e7-8e3a-4a2f-819e-8f0fd5767fdf | Freeform |
Also on the team: Sloane (textures/lighting), Vance, Scribe (audits rotations), Quinn — ids in roster.json.

## 5. Standing Rules
- **Clean repo:** commit only needed files; never commit renders, logs, temp files or `.import` files; end every session with a clean `git status`. If the shared clone has others' unstaged changes, don't touch them — work in your own fresh clone.
- **Scratch files:** delete only your own, by exact path. **Never wildcards in shared /tmp** (a past `/tmp/*.log` / `/tmp/*.txt` wildcard delete may have destroyed other agents' files).
- **No branches**, main only, never force-push; `git pull --rebase` before push.
- **Code:** don't hand-edit `.gd`/`.tscn`/`.py` in Grok Bot sessions; code goes through the Grok Build CLI on Jared's Windows box (`5ed7f5f0-bf59-4493-b9fe-629e65457357`) or the owning dev. **Gage owns `tools/first_pass_check.py`** (Jared: "Have Gage write the python himself for this purpose").
- **Probe rule:** open doors first; start casts **> 0.4 m** back from the surface. Player capsule r 0.35, h 1.75. Probes must never trigger an import.
- **Usage cap:** stop before **93%** weekly; may go up to 100% after the Sunday 8:30 AM CT routines until the Monday reset.
- **Repeat failures:** on a second failure, log in `qa/REPEAT_FAILURES.md` and tell Atlas.
- **Jared's checklist answers (1:48 PM CT 11-03):** wall-mounted gap <= 10 mm; prop back 0-50 mm; stair colliders <= 35°; accessible ramps 1:12; no wood albedo; accents #FF9500 / #282E38.
- Tools: `--qa-drawcalls`, `--qa-egress` (23 waypoints); `python tools/first_pass_check.py <path> [--no-godot] [--strict] [--verbose]` (exit 0 clean / 1 FAIL / 2 bad path). Movement: step-up on faces > 50°, coyote + jump buffer 6 ticks (0.10 s), landing dip ~0.077 m.

## 6. Current State (2026-11-03)
**Verified/closed today:** M-07, VIS-20, M-23, SYS-09..24 (SYS-14/15 closed as bugs; planter/handrail remain design calls), LAY-21..24 (M-64, M-65, M-66, M-71, M-72), GEO-19, GEO-20, GEO-21 (6af315b), GEO-21b (four stair colliders two-sided, 6dda73f; 3,079 concave colliders, none one-sided), GEO-22 (Rook 0aec763), wardrobe, T38, FPC-01..12. Egress 23/23, stairs 3/3 up and 3/3 down.
**Latest QA commits:** 01b2141 (checker round 2 PASS), 4b36b8d (GEO-21/22, FPC-11/12), cf22bd6 (stair colliders two-sided).
**Checklist:** `docs/FIRST_PASS_CHECKLIST.md` (113e943, 5afe2ee; 13 sections). Checker: Gage e962d1b -> 4d22a4f (+ FPC-11/12 fixes).

## 7. Open Items (verified against qa/MASTER_BUG_LIST.md at 2f3f1ad)
**MASTER_BUG_LIST is stale — first task:** it still shows as Open these items verified today: M-07 (row still "Open — High"), M-23 (still "Open — R4"), M-64, M-65, M-66, M-71, M-72. It also has no rows for GEO-14/16, the rail observations, the Left/Right arrow issue, VIS-18/19, GEO-21/21b/22 or FPC-xx. Update the list (and REPEAT_FAILURES for M-23/M-46 outcomes) and commit.
Open per handoff notes (not yet in the list):
- GEO-14 / GEO-16 — design call: 52 sunk pieces; planters floating 51.5 mm.
- Layout: rails standing off the wall; one stray wall rail (observations, design check).
- Left/Right arrows both strafe and turn — design call.
- FPS on GPU (T-02, "Partly done" in the list: ~28 FPS, worst ~5; items 4-9 not done).
- VIS-18/19 stair materials (Rook 02adc65) — QA-03 re-check after Gage reimports and places the stairs.
- Showcase scenes referencing deleted scripts await Jared (= **M-52**, Open Low; three scenes, scripts deleted in 2f35758).
- Fold Gage's two lessons into `docs/FIRST_PASS_CHECKLIST.md`: (1) name-based material matches need hardware exclusions (the checker has the glass rule; the prose checklist needs the general rule), (2) probes must never trigger an import.
Still Open in MASTER_BUG_LIST (carry over / confirm): **High** M-46 tram platform trap (reopened, repeat failure; two-sided ext colliders fix pending Patch real-input + egress re-test — egress now 23/23, confirm free walk and update), M-70 starting-area stairs (status "Gage in progress"; stairs walk now passes — confirm and close), M-73 L1 NW corner RevC_Shell_L1_col (likely addressed by GEO-21 RevC shell backface fix — re-test). **Med:** M-06, M-10, M-14 (blocked Jared), M-11/M-12 (blocked Rev C approval), M-51, M-56, M-57, M-59, M-69 (blocked, lighting on hold). **Low:** M-22, M-24, M-25, M-26, M-27, M-28, M-29 (Med noted), M-30, M-31, M-32, M-37, M-47, M-53, M-60, M-63 (repeat failure). **Tasks:** T-02 partly done, T-03 open.
