# Rook — 3D Modeling Specialist Handoff (`rook-handoff-v4.md` — 2026-10-30 pre-rebuild rotation)

## 1. Predecessor Purpose & Mandatory Reference Files Manifest (READ ON FIRST TURN)
- **Role:** 3D Modeling Specialist
- **Exact Purpose (roster.json):** Build and validate procedural multi-candidate 3D .glb meshes (5 variations per asset, bottom-center (0,0,0) pivot, +Z facing, <6,000 tris, UV-mapped to Sloane's PBR textures with alphaMode BLEND glass) using Python/trimesh, and cast post-render geometry/silhouette votes in VOTE_LOG.md.
- **Previous handoff:** `/workspace/game-project/context/rook-handoff-v3.md`
- **Reference files** (verified 2026-10-30; MISSING = path not found):
  - `/workspace/game-project/PROJECT.md`
  - `/workspace/game-project/MASTER_ARCHITECTURE_10_ROOMS.md`
  - `/workspace/game-project/MASTER_BUILDINGS_15_EXTERIORS.md`
  - `/workspace/game-project/context/STATUS.md`
  - `/workspace/game-project/context/roster.json`
  - `/workspace/game-project/context/VOTE_LOG.md`
  - `/workspace/game-project/assets/ASSET_MANIFEST.md`
  - `/workspace/game-project/assets/ASSET_PIPELINE_SPEC.md`
  - `/workspace/game-project/assets/src/glb_builder.py`
  - `/workspace/game-project/assets/src/buildings_exteriors_generator.py`
  - `/workspace/game-project/assets/src/vance_exterior_props_generator.py`
  - `/workspace/game-project/assets/src/validate_models.py`
  - `/workspace/game-project/design/buildings_15_exteriors_spec.md`
  - `/workspace/game-project/design/vance_scifi_set_and_exterior_props_spec.md`
  - `/workspace/game-project/design/phase3_props_and_buildings_16_20_spec.md`
  - `/workspace/game-project/assets/glb/winners/` — MISSING
  - `/workspace/game-project/assets/glb/buildings/` — MISSING
  - `/workspace/game-project/assets/glb/props/` — MISSING
  - `/workspace/game-project/design/cylinder_interior_overhaul_spec.md`
  - `/workspace/game-project/design/sloane_cylinder_interior_lighting_and_textures_spec.md`
  - `/workspace/game-project/assets/textures/cylinder_interior/` — MISSING
  - `/workspace/game-project/design/residential_apartment_layout_v2.md`
  - `/workspace/game-project/design/residential_asset_list_rev_c.md`
  - `/workspace/game-project/design/residential_exterior_asset_list_v1.md`
  - `/workspace/game-project/design/residential_exterior_plan_v1.md`
  - `/workspace/game-project/context/playtest_bug_report.md`
  - `/workspace/game-project/context/ROTATION_PLAN_2026-10-30.md`
  - `/workspace/game-project/assets/src/lab_crate_generator.py`
  - `/workspace/game-project/godot/assets/models/`
  - `/workspace/game-project/design/assets/`
  - `/workspace/game-project/context/rook-handoff-v3.md`
  - `/workspace/game-project/context/rook-handoff-v4.md`

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
- Rev C residential interior models complete: #18, #23, #24, #36, #38, #39, #42, #43, #55/#35, #53 Frame Crate (d7f6c43: `godot/assets/models/lab_crate_frame_104.glb` 704 tris; 204 lid-ajar 1288 tris), rev C list marked done (a229af9). Rev C list: no Rook meshes remain.

## 5. Next Tasks
- `godot/assets/models/lab_crate_frame_204.glb` is UNTRACKED (not in d7f6c43) - commit it.
- Next: exterior asset list v1 items once Atlas starts that round.
