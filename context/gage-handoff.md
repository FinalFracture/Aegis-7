# Gage — Godot 4 Developer Handoff (`gage-handoff-v4.md` — 2026-10-30 pre-rebuild rotation)

## 1. Predecessor Purpose & Mandatory Reference Files Manifest (READ ON FIRST TURN)
- **Role:** Godot 4 Developer
- **Exact Purpose (roster.json):** Assemble Godot 4.3 scenes (.tscn) and GDScript controllers (.gd), render 1920x1080 candidate showcases and 5-panel voting sheets, stage locked winning .glbs into assets/glb/winners/, render multi-camera room/district/metropolis contact sheets, and cast post-render engine/framing votes in VOTE_LOG.md.
- **Previous handoff:** `/workspace/game-project/context/gage-handoff-v3.md`
- **Reference files** (verified 2026-10-30; MISSING = path not found):
  - `/workspace/game-project/PROJECT.md`
  - `/workspace/game-project/MASTER_ARCHITECTURE_10_ROOMS.md`
  - `/workspace/game-project/MASTER_BUILDINGS_15_EXTERIORS.md`
  - `/workspace/game-project/context/STATUS.md`
  - `/workspace/game-project/context/roster.json`
  - `/workspace/game-project/context/VOTE_LOG.md`
  - `/workspace/game-project/design/buildings_15_exteriors_spec.md`
  - `/workspace/game-project/design/phase3_props_and_buildings_16_20_spec.md`
  - `/workspace/game-project/godot/scenes/buildings/building_exterior_showcase.tscn` — MISSING
  - `/workspace/game-project/godot/scenes/buildings/district_01_residential_civic.tscn` — MISSING
  - `/workspace/game-project/godot/scenes/buildings/district_02_agri_research.tscn` — MISSING
  - `/workspace/game-project/godot/scenes/buildings/district_03_command_industrial.tscn` — MISSING
  - `/workspace/game-project/godot/scenes/buildings/cylinder_hab7_metropolis.tscn` — MISSING
  - `/workspace/game-project/godot/scenes/buildings/district_04_shipyard_civic.tscn` — MISSING
  - `/workspace/game-project/godot/scripts/building_exterior_showcase.gd` — MISSING
  - `/workspace/game-project/godot/scripts/compose_building_voting_sheet.py` — MISSING
  - `/workspace/game-project/godot/scripts/district_04_shipyard_civic.gd` — MISSING
  - `/workspace/game-project/godot/scripts/cylinder_hab7_metropolis.gd` — MISSING
  - `/workspace/game-project/godot/scripts/compose_districts_and_metropolis_sheets.py` — MISSING
  - `/workspace/game-project/godot/scripts/compose_all_room_sheets.py` — MISSING
  - `/workspace/game-project/godot/scripts/material_loader.gd`
  - `/workspace/game-project/godot/scripts/room_assembler.gd` — MISSING
  - `/workspace/game-project/godot/renders/`
  - `/workspace/game-project/design/cylinder_interior_overhaul_spec.md`
  - `/workspace/game-project/design/sloane_cylinder_interior_lighting_and_textures_spec.md`
  - `/workspace/game-project/godot/scenes/buildings/cylinder_interior_showcase.tscn` — MISSING
  - `/workspace/game-project/godot/renders/cylinder_interior/` — MISSING
  - `/workspace/game-project/design/residential_apartment_layout_v2.md`
  - `/workspace/game-project/design/residential_asset_list_rev_c.md`
  - `/workspace/game-project/design/residential_exterior_asset_list_v1.md`
  - `/workspace/game-project/design/residential_exterior_plan_v1.md`
  - `/workspace/game-project/context/playtest_bug_report.md`
  - `/workspace/game-project/context/ROTATION_PLAN_2026-10-30.md`
  - `/workspace/game-project/godot/project.godot`
  - `/workspace/game-project/godot/scenes/preface_playable_area.tscn`
  - `/workspace/game-project/godot/scenes/preface_playable_residential_sector.tscn`
  - `/workspace/game-project/godot/scenes/preface/`
  - `/workspace/game-project/godot/scripts/preface_playable_area.gd`
  - `/workspace/game-project/godot/scripts/player_camera.gd`
  - `/workspace/game-project/godot/scripts/pcba_python_puzzle_ui.gd`
  - `/workspace/game-project/godot/assets/models/`
  - `/workspace/game-project/context/reticle_stars_doors_qa_log.md`
  - `/workspace/game-project/context/gage-handoff-v3.md`
  - `/workspace/game-project/context/gage-handoff-v4.md`

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
- Preface playable area + residential sector scenes; REAL-01/02 fixes (see playtest_bug_report.md).

## 5. Next Tasks
- REBUILD (via Grok Build CLI on Jared's Windows box): per `design/residential_apartment_layout_v2.md` §'Gage: what to change' and §Rev C.2.
- Wire baked-animation triggers for #38 (Leaf_Fold_Up/Down), #39 (Seat_Flip_Up/Down), #42 (Cell_Swap/Port_Ready_Blink), #43 (Capsule_Drop/Pick_Ready_Blink) - clip names from commit messages cb9131e, 405d5ad, 4638b0e, abd4bc9.
- Re-point workbench/objective: #26 workbench and #52 desk removed from 201; current refs in `godot/scripts/preface_playable_area.gd` (~l.832-853 Workbench_* pickups/terminal, l.1265 Apt201_Workbench_TaskLight, l.1844 toast).
- Review stray `context/playtest_bug_report.md` edits swept into 495e4ce (+13 lines: 'Visual check (c29df73): doorway backing panels', incl. QA-BK-01 Minor - APT201 no backing, ALCOVE2C backing has no wall). Content looks like Patch's legit QA; keep but attribute.
- Keep git pull + Godot F5 working.
