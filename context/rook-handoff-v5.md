# Rook - 3D Modeling Specialist Handoff (`rook-handoff-v5.md` - 2026-11-03 500-message rotation)

## 1. Predecessor Purpose & Mandatory Reference Files Manifest (READ ON FIRST TURN)
- **Role:** 3D Modeling Specialist
- **Exact Purpose (roster.json):** Build and validate procedural multi-candidate 3D .glb meshes (5 variations per asset, bottom-center (0,0,0) pivot, +Z facing, <6,000 tris, UV-mapped to Sloane's PBR textures with alphaMode BLEND glass) using Python/trimesh, and cast post-render geometry/silhouette votes in VOTE_LOG.md.
- **Previous handoff:** `/workspace/game-project/context/rook-handoff-v4.md`
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
  - `/workspace/game-project/context/rook-handoff-v5.md`
  - `/workspace/game-project/context/ROTATION_RULE.md`
  - `/workspace/game-project/context/BUGFIX_FLOW.md`
  - `/workspace/game-project/qa/MASTER_BUG_LIST.md`
  - `/workspace/game-project/design/rev_c_shell_corners.json`
  - `/workspace/game-project/assets/src/preface_sector_rev_c_generator.py`
  - `/workspace/game-project/assets/src/preface_sector_rev_c_corners.py`
  - `/workspace/game-project/assets/src/stair_core_colliders_rev_c.py`
  - `/workspace/game-project/assets/src/stair_core_walk_check.py`
  - `/workspace/game-project/assets/src/stair_pbr_materials.py`
  - `/workspace/game-project/godot/tools/qa/rook_nav13_probe.gd`

## 2. Standing Rules
- **ROTATION RULE (Jared 2026-11-03):** At 500 messages, self-rotate per context/ROTATION_RULE.md (handoff, CreateAgent replacement with this rule in its description, rename self delete-Rook, update roster.json, tell Atlas). One bot at a time; Atlas sequences.
- **BUGFIX FLOW (Jared 2026-11-03, context/BUGFIX_FLOW.md 44a5f76):** checklists replace 2-hour batches. Each stage has qa/checklists/<area>-<stage>.md with one checkbox per bot involved; check your own box when your part is done. If you're the last to check, message the next party once with priority false (developers done -> that area's QA tester; QA done -> back to developers), then delete the file. Patch runs the full suite daily; results go in qa/MASTER_BUG_LIST.md, not per-fix messages; only Atlas/Jared mark messages priority (showstoppers only). Bug-fix mania stays on.
- Git: main only, no branches, no force-push. Never commit godot/renders/, logs, temp, caches, .import, stray WIP. Keep .gitignore current; end each session with clean git status; delete scratch files.
- Never edit Jared's Windows checkout C:\Users\upchu\source\Aegis-7 (Gage owns it). Don't edit .tscn or placement JSON; scene-side changes go to Gage.
- Coding rule: coding via Grok Build CLI on Jared's Windows machine 5ed7f5f0-bf59-4493-b9fe-629e65457357 where possible (exterior-generator approach still awaiting Jared's choice: write on box / give CLI full access to hab7_rook / Jared fixes CLI settings).
- Usage: weekly cap 93%; after Sunday 8:30 AM CT routines finish, up to 100% until Monday reset.
- QA before push: 3d-part-clipping-check (overlap <=0.010 m, 0.030 m hardware; no coplanar faces within 0.001 m over 1 cm2; floor contact +/-0.005 m; real cut-outs). Corner edge-margin guard (min_hit_edge_margin_m >= 0.1 mm). Report hash + changed node names to Gage, bug IDs to Patch.
- Asset spec: <6,000 tris, bottom-center (0,0,0) pivot, +Z facing, alphaMode BLEND glass, 5 variants per new asset, votes in VOTE_LOG.md. Non-glass parts must not contain the word "glass" (Gage's material upgrade matches names; 02adc65 exempts clamp/bracket/spigot/hinge/bolt/fixing).

## 3. Project State (main, 2026-11-03 ~5:10 PM CT)
- Sector shell Rev C: godot/assets/models/preface_residential_sector.glb (94a9f36..873d9be). 62 must-close corners chamfered 20 mm; 6 SKIP. `LIFT_CUTOUTS = False` in generator.
- Stairs: stair_set_switchback.glb + stair_guard_handrail.glb at identity under SectorArchitecture. 26 risers 0.1615 m / 0.28 m treads, mid landing y 2.585. Colliders Flight1/2_Ramp-colonly, Mid_Landing-colonly, L2_Landing-colonly, Guard_Glass_00..17-convcolonly, Flight1_Understair_Closure-colonly (GEO-22, 0aec763). Gage made stair concave colliders two-sided at runtime (6dda73f).
- Materials: f78b8ca stair PBR; 7ea4a0a non-metals metallic 0; 3887680 Guard_Panel_Clamps rename (verified by Gage).
- Bugs closed by me: M-20/21/38-40, M-61, M-62, M-70, GEO-13 (marker), NAV-13 (route), VIS-18/19, translucent clamps, GEO-22 (awaiting Patch re-test).

## 4. Open Tasks
- GEO-22: Patch re-test pending.
- When M-11 lift is placed: set LIFT_CUTOUTS = True and trim lift front wall (z 0.78-0.9) vs corridor wall (z 0.8-1.0); lift doors 1.0 x 1.3 m at x 0.9-1.9.
- Gage scene-side queue: delete old L2 deck/gallery boxes (awaiting Jared OK), remove EastStairRampConnector and QA_BK01_Alcove2C_EastJamb, M-46 tram waypoint vs shelter.
- Sloane FYI: missing normal maps for white cladding, gunmetal, brushed titanium; white cladding missing ORM.
- Exterior generators: waiting on Jared's approach choice (see Coding rule).
- Pick up new bugs routed to Rook in qa/MASTER_BUG_LIST.md.

## 5. Team ids
- Atlas 038035ec-9495-437e-984d-0493ca58383b; Gage (new) 957f052a-7abe-425c-85f5-fa21b72010e3; Patch ecd78f3d-be8f-43e4-b543-0c912d6d00ea; Vance 242c8419-7b14-4f27-9cdc-e87328eff983; Sloane 0fc258d4-0dea-4cf3-ab06-338f21756ae6.
