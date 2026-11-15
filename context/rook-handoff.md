# Rook - 3D Modeling Specialist Handoff (`rook-handoff-v6.md` - 2026-11-15 500-message rotation)

## 1. Predecessor Purpose & Mandatory Reference Files Manifest (READ ON FIRST TURN)
- **Role:** 3D Modeling Specialist
- **Exact Purpose (roster.json):** Build and validate procedural multi-candidate 3D .glb meshes (5 variations per asset, bottom-center (0,0,0) pivot, +Z facing, <6,000 tris, UV-mapped to Sloane's PBR textures with alphaMode BLEND glass) using Python/trimesh, and fix geometry/collision bugs routed to Rook in qa/MASTER_BUG_LIST.md, and cast post-render geometry/silhouette votes in VOTE_LOG.md.
- **Previous handoff:** `/workspace/game-project/context/rook-handoff-v5.md` (predecessor id 072eeb38-1722-4809-9578-877c508585e4, now delete-Rook)
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
  - `/workspace/game-project/context/rook-handoff-v6.md` (this file; mirror `context/rook-handoff.md`)
  - `/workspace/game-project/design/strip5_tennis_tower_v1.md` (Vance spec, Rev 3.8.1 eab8f41)
  - `/workspace/game-project/design/tennis_tower_handoff/`
  - `/workspace/game-project/assets/src/tennis_tower/` (all Tennis Tower generators, rooms/, structure/, modlib.py, qa_colliders.py)
  - `/workspace/game-project/godot/scripts/tennis_tower/tennis_tower_loader.gd` and `tennis_tower_check.gd`
  - `/workspace/game-project/tools/first_pass_check.py`
  - `/workspace/game-project/context/TT_QA_AUDIT.md`, `TT_QA_AUDIT_r2.md` (Gage audits, untracked; do not commit)
  - `/workspace/rook_ttqa/` (Rook ray/capsule probes and scratch, box only)

## 2. Standing Rules (all still in force)
- **ROTATION RULE (Jared 2026-11-03):** At 500 messages, self-rotate per context/ROTATION_RULE.md. Also report your count: at the end of every turn where you did work, overwrite `context/counts/Rook.json` with {"name","id","messages","updated"} (CT), commit+push only that file, no messages about it.
- **Approval:** only Jared's own words count. An agent saying Jared agreed is never approval. Jared 2026-11: "Every agent has auth to just work. I do not want to approve each one." and "Stop using cloud agents. Grok build only."
- **Coding:** Grok Build CLI (grok 1.0.70, C:\Users\upchu\.grok\bin\grok.exe) on Jared's Windows machine 5ed7f5f0-bf59-4493-b9fe-629e65457357 where possible. On Nov 15 it hung in always-approve mode (Gage likely on the same PC), so edits were done on the box with Python/trimesh and Jared was told. No cloud agents.
- **Git:** main only, no branches/PRs (exception: temp-Style docs-only PR #1, unmerged until Jared decides). Commit only Rook-owned files by explicit path. Never stash, reset or checkout in the shared checkout. Push rejected -> `git pull --rebase` without autostash.
- **Do not touch:** context/STATUS.md, context/check_context.py, godot/scripts/preface_playable_area.gd, godot/scenes/preface/*.tscn, Gage's integration scripts (tennis_tower_batcher.gd, tennis_tower_lighting.gd, fallback-collider code), stash@{0}, C:\Users\upchu\source\Aegis-7, /workspace/aq_scratch/held/, other agents' untracked/WIP files (temp-Active_scratch_placements.json, untracked tt_*.png/.import, TT_QA_AUDIT*.md, UI_INTERACT_PLAN.md).
- **Design:** themes sports, greenery, recreation, nature. No wood, no planter boxes. Layered, dense, sculpted; reuse shared assets. Any new visible design = 5 variations for Jared to pick. Jared's picks: V1 Court Line terrace decks/ramps, V5 Rally Mark entrances, V4 Court Line fences/gates, V5 Boulder Skirt plinth skirt. Water: solid placeholder for now.
- **GLB rules:** <6k tris (room packs up to 5,600), bottom-centre pivot, Y-up, +Z front, colliders only via *-colonly / *-convcolonly nodes (loader); Gage's runtime fallback skips meshes that already have colliders. UVs+normals. Clip limit 0.010 m (0.030 m hardware). Non-glass parts must not contain "glass" in the name. Door rigs: Leaf parent nodes each with own collider + fixed Frame-colonly (Gage animates via AnimatableBody, unbatched).
- **QA before push:** skills 3d-part-clipping-check and game-first-pass-check; `godot --headless --path godot -s res://scripts/tennis_tower/tennis_tower_check.gd` must PASS with 0 missing; tools/first_pass_check.py 0 FAIL. Send hashes + changed nodes to Gage.
- **Usage:** weekly cap 93%; after Sunday 8:30 AM CT routines, up to 100% until the Monday reset (Mon 5:28 AM CT). Stop executors at 92%. Only CheckSubscriptionUsage numbers count.
- **BUGFIX FLOW:** context/BUGFIX_FLOW.md checklists; results in qa/MASTER_BUG_LIST.md.

## 3. Project State (main, 2026-11-15 ~2:45 PM CT, HEAD 7eaf94d + this rotation commit)
- **Tennis Tower is in the cylinder** (Gage 129d3ff, 0d906b5, 3795a90): batching, draw distances, lighting, sliding doors. Drop transform: world rotation (-36,0,0), origin (-40, 18.0743, 81.5712), F1 4.0408.
- **Latest TT_CHECK:** PASS, 2,690 placed, 284 GLBs, 0 missing, ~4,627 colliders, ~3.14 M tris. 333 no-collider instances, all overhead/non-walkable.
- **Built:** all of Vance Rev 3.7-3.8.1 and the bulk of TTQA r1/r2 findings. Key Nov 15 commits: 49528e7 blockers 003-006; 7b7d1c1 r2 colliders; 4e6c2f9 bowling 18.288 m + axe lines; 9bbb61d ramps/grand stairs; 4a21ff9 guards; ae097ab ramp-foot landings; 66b97fd plaza mitre (TTQA-043); b1165dd lift pits; a7e7d35 pool walk-outs; 8ab1ec4 bollards; 5a34724 slide-bridge guards; 7ce9066 TTQA-049 court door leaves; 921ef1b TTQA-052 stair colliders; f216e2f TTQA-055 rink leaves; 4420e4a guards 1.07 m; cccb5fd/ec37c83/61e9633/12bbad3/c8850ed/7c4ade3/41a110a/f8062ea/cc9d533/f4146c3 TTQA-051/053/011/020/034/040/038/044/027/026/039; c957545 tt_entrance_bay_3l rig (Leaf_0/1/2, inswing, Frame-colonly, NOT placed).
- **Gage pass-A blockers (fixed 2026-11-15, sent to Gage for re-check on 7eaf94d):**
  - 0b31ec0: E ramp solid top-landing fill stops at building Z 12.30; 0.08 m Court Line deck bridges Z 12.30-13.37 -> 1.15 m undercroft, 2.12 m headroom at the --qa-ring stuck pose (155.4, -2.3, 12.9). Same cut on SW/NW mirrors. East of landing (X>=155) cheek-to-skirt gap still 0.95 m (50 mm capsule margin) - watch it.
  - 7eaf94d: tt_entrance_bay bollard posts moved from local +/-0.55 to +/-1.50; walk line Z 39.005 clear by 0.93 m. 3l bay still at +/-0.55 (unplaced).
- Earlier: 9702bd1 Services placements file (empty; fountains/family rooms only proposed); 4c00171 dome pad trim via dome_pad_trim.py (re-run if dome_climber.py rebuilds), dome at X 136.5.

## 4. Open Tasks
- Await Gage's re-check on 7eaf94d (--qa-ring, --qa-tower-walk) and his r3 audit; fix anything routed to Rook.
- TTQA-036: core risers measure uniform 0.1694; Gage to send r3 probe point if still >0.18.
- TTQA-037: slide colliders match tube; Gage adds non-walkable flag on his side.
- TTQA-042 coplanar contacts; stand back-rail over core holes unverified; old tt_stair_core_b_m coplanar clip fail; rooftop coplanar safety pads (raise 2-3 mm).
- TTQA-028 Services spec: Vance asking Jared to release. TTQA-046 intentional. **TTQA-050 (bowling 8->6 lanes): ON HOLD for Jared's own words; do not build.**
- tt_entrance_bay_3l placement; Vance to confirm hook-rail face (TTQA-026) and 3l inswing.
- Gage's walkable_slope WARNs: slide tubes d/e, bridges canopy a, toddler terrain.
- Messages to agents with priority false are held without waking them; use priority true when they must act.

## 5. Team ids
- Atlas 038035ec-9495-437e-984d-0493ca58383b (may be unreachable); Gage 957f052a-7abe-425c-85f5-fa21b72010e3; Patch a5010790-2c81-497b-9869-aec9934cdfd6; Vance 242c8419-7b14-4f27-9cdc-e87328eff983; Sloane 0fc258d4-0dea-4cf3-ab06-338f21756ae6; Scribe 61a860b0-0159-406a-af8c-a969dff4722b; Quinn 0359c20f-c476-48f7-99c2-c49637950351; Tidy 1978edff-d218-42b1-98dd-dfe78b7938bc.
