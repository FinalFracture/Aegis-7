# Vance — Sci-Fi Architect, Movie Prop & Set Design Specialist Handoff (`vance-handoff-v3.md` — 2026-10-30 pre-rebuild rotation)

## 1. Predecessor Purpose & Mandatory Reference Files Manifest (READ ON FIRST TURN)
- **Role:** Sci-Fi Architect, Movie Prop & Set Design Specialist
- **Exact Purpose (roster.json):** Design hard sci-fi architectural blueprints, movie-set silhouettes, human-scale greebling specs, and district placement layouts under the Aegis-7 Standard, and cast post-render architectural votes in VOTE_LOG.md.
- **Previous handoff:** `/workspace/game-project/context/vance-handoff-v2.md`
- **Reference files** (verified 2026-10-30; MISSING = path not found):
  - `/workspace/game-project/PROJECT.md`
  - `/workspace/game-project/MASTER_ARCHITECTURE_10_ROOMS.md`
  - `/workspace/game-project/MASTER_BUILDINGS_15_EXTERIORS.md`
  - `/workspace/game-project/context/STATUS.md`
  - `/workspace/game-project/context/roster.json`
  - `/workspace/game-project/context/VOTE_LOG.md`
  - `/workspace/game-project/design/vance_scifi_set_and_exterior_props_spec.md`
  - `/workspace/game-project/design/buildings_15_exteriors_spec.md`
  - `/workspace/game-project/design/phase3_props_and_buildings_16_20_spec.md`
  - `/workspace/game-project/design/cylinder_interior_overhaul_spec.md`
  - `/workspace/game-project/godot/renders/cylinder_interior/cylinder_interior_showcase_sheet.png` — MISSING
  - `/workspace/game-project/design/character_aegis7_crew_spec.md`
  - `/workspace/game-project/design/vance_chapter1_solar_flare_environmental_states.md`
  - `/workspace/game-project/design/preface_test_environment_and_wrist_spec.md`
  - `/workspace/game-project/design/residential_apartment_layout_v2.md`
  - `/workspace/game-project/design/residential_asset_list_rev_c.md`
  - `/workspace/game-project/design/residential_exterior_asset_list_v1.md`
  - `/workspace/game-project/design/residential_exterior_plan_v1.md`
  - `/workspace/game-project/context/playtest_bug_report.md`
  - `/workspace/game-project/context/ROTATION_PLAN_2026-10-30.md`
  - `/workspace/game-project/design/residential_apartment_layout_v2_revB.md`
  - `/workspace/game-project/design/residential_roomlayout_rev_c.py`
  - `/workspace/game-project/design/residential_floorplan_rev_c.py`
  - `/workspace/game-project/design/residential_exterior_plan_v1.py`
  - `/workspace/game-project/design/residential_exterior_tiered_steps_fit.py`
  - `/workspace/game-project/design/residential_stair_core_v1.md`
  - `/workspace/game-project/context/vance-handoff-v2.md`
  - `/workspace/game-project/context/vance-handoff-v3.md`

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
- Rev C.2 layout approved by Jared 2026-10-29 (`design/residential_apartment_layout_v2.md` §Rev C.2, commits 519cc5d, 759f4c8, f8565da).
- Exterior v1 plan approved 2026-10-29; exterior asset list v1 readiness pass (DRAFT).

## 5. Next Tasks
- Finalize exterior asset list v1 for modeling.
- Objective/tutorial anchors TBD (layout doc l.151) - coordinate with Gage at rebuild.
