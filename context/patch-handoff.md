# Patch — QA & Automated Playtester Specialist Handoff (`patch-handoff-v2.md` — 2026-10-30 pre-rebuild rotation)

## 1. Predecessor Purpose & Mandatory Reference Files Manifest (READ ON FIRST TURN)
- **Role:** QA & Automated Playtester Specialist
- **Exact Purpose (roster.json):** Run automated and headless Godot 4.3 playtest passes, audit scene/script/collision/interaction bugs across Cylinder Hab-7 playable scenes, verify fixes with Gage so git pull + Godot F5 works out of the box, and participate in post-render/playtest sign-offs in VOTE_LOG.md.
- **Previous handoff:** `/workspace/game-project/context/patch-handoff-v1.md`
- **Reference files** (verified 2026-10-30; MISSING = path not found):
  - `/workspace/game-project/PROJECT.md`
  - `/workspace/game-project/context/STATUS.md`
  - `/workspace/game-project/context/roster.json`
  - `/workspace/game-project/context/usage_budget.json`
  - `/workspace/game-project/context/VOTE_LOG.md`
  - `/workspace/game-project/godot/project.godot`
  - `/workspace/game-project/design/residential_apartment_layout_v2.md`
  - `/workspace/game-project/design/residential_asset_list_rev_c.md`
  - `/workspace/game-project/design/residential_exterior_asset_list_v1.md`
  - `/workspace/game-project/design/residential_exterior_plan_v1.md`
  - `/workspace/game-project/context/playtest_bug_report.md`
  - `/workspace/game-project/context/ROTATION_PLAN_2026-10-30.md`
  - `/workspace/game-project/godot/scenes/preface_playable_area.tscn`
  - `/workspace/game-project/godot/scenes/preface_playable_residential_sector.tscn`
  - `/workspace/game-project/godot/scripts/preface_playable_area.gd`
  - `/workspace/game-project/context/cylinder_gravity_qa_log.md`
  - `/workspace/game-project/context/hand_controls_qa_log.md`
  - `/workspace/game-project/context/reticle_stars_doors_qa_log.md`
  - `/workspace/game-project/godot/renders/qa/`
  - `/workspace/game-project/context/patch-handoff-v1.md`
  - `/workspace/game-project/context/patch-handoff-v2.md`

## 2. Standing Rules
- **CODING RULE (NEW 2026-10-30):** All coding now runs through the Grok Build CLI (grok 1.0.70, `C:\Users\upchu\.grok\bin\grok.exe`) on Jared's Windows machine `5ed7f5f0-bf59-4493-b9fe-629e65457357`, to save Grok Bot usage. Do not write/edit .gd/.tscn/.py code directly in Grok Bot sessions; drive it via that CLI.
- **Usage:** Weekly hard cap: 93% account usage. Reported weekly usage ~59% (Atlas, Fri 2026-10-30). Stop all work before 93%.
- Aegis-7 Standard; <1.2% micro-noise PBR; alphaMode BLEND glass; <6,000 tris; bottom-center (0,0,0) pivot, +Z facing; 5 iterations per asset; post-render votes in VOTE_LOG.md.

## 3. Project State (git HEAD a229af9, 2026-10-30 03:50 CDT)
- Residential interior (rev C) models all done incl. #53 Frame Crate (d7f6c43, a229af9). Remaining rev C 'still to model': #6, #54 — Sloane texture/decal jobs.
- Rev C.2 layouts APPROVED by Jared 2026-10-29.
- Exterior asset list v1: DRAFT, next up.
- Pending Gage rebuild: baked-animation triggers #38/#39/#42/#43; workbench/objective re-pointing; review stray playtest_bug_report.md edits in 495e4ce.
- Untracked: `godot/assets/models/lab_crate_frame_204.glb`.

## 4. Completed Deliverables (this role)
- Playtest passes logged in `context/playtest_bug_report.md` incl. REAL-01..05 audit and c29df73 doorway backing visual check (QA-BK-01).

## 5. Next Tasks
- After Gage rebuild: re-run QA (REAL-04 stair width/headroom >=2.1 m, QA-BK-01, door hubs), verify git pull + F5 works.
- Runs of Godot/QA scripts go through Grok Build CLI on Jared's Windows box.
