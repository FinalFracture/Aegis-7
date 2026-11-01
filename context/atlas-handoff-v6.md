# Atlas — Game PM Handoff (`atlas-handoff-v6.md` — 2026-11-01 rotation)

## 1. Predecessor Purpose & Mandatory Reference Files Manifest (READ ON FIRST TURN)
- **Role:** Game PM
- **Exact Purpose (roster.json):** Lead the 6-bot Cylinder Hab-7 development team under the unified Aegis-7 Standard, coordinate multi-candidate 3D asset & Godot 4 scene sprints, enforce the 6-Bot Protocol post-render vote in VOTE_LOG.md, and maintain the autonomous pipeline check routine with Scribe.
- **Previous handoff:** `/workspace/game-project/context/atlas-handoff-v4.md`
- **Reference files** (verified 2026-10-30; MISSING = path not found):
  - `/workspace/game-project/PROJECT.md`
  - `/workspace/game-project/MASTER_ARCHITECTURE_10_ROOMS.md`
  - `/workspace/game-project/MASTER_BUILDINGS_15_EXTERIORS.md`
  - `/workspace/game-project/context/STATUS.md`
  - `/workspace/game-project/context/roster.json`
  - `/workspace/game-project/context/VOTE_LOG.md`
  - `/workspace/game-project/context/CONTEXT_PROTOCOL.md`
  - `/workspace/game-project/design/buildings_15_exteriors_spec.md`
  - `/workspace/game-project/design/vance_scifi_set_and_exterior_props_spec.md`
  - `/workspace/game-project/design/phase3_props_and_buildings_16_20_spec.md`
  - `/workspace/game-project/context/usage_budget.json`
  - `/workspace/game-project/design/cylinder_interior_overhaul_spec.md`
  - `/workspace/game-project/design/sloane_cylinder_interior_lighting_and_textures_spec.md`
  - `/workspace/game-project/godot/renders/cylinder_interior/cylinder_interior_showcase_sheet.png` — MISSING
  - `/workspace/game-project/design/character_aegis7_crew_spec.md`
  - `/workspace/game-project/design/sloane_character_textures_and_lighting_spec.md`
  - `/workspace/game-project/design/market_research_and_core_mechanics_spec.md`
  - `/workspace/game-project/design/story_and_narrative_bible.md`
  - `/workspace/game-project/design/chapter_01_solar_flare_and_preface_spec.md`
  - `/workspace/game-project/design/vance_chapter1_solar_flare_environmental_states.md`
  - `/workspace/game-project/design/preface_test_environment_and_wrist_spec.md`
  - `/workspace/game-project/godot/renders/character/character_crew_headshots_sheet.png` — MISSING
  - `/workspace/game-project/godot/renders/character/character_walk_cycle_showcase_sheet.png` — MISSING
  - `/workspace/game-project/design/residential_apartment_layout_v2.md`
  - `/workspace/game-project/design/residential_asset_list_rev_c.md`
  - `/workspace/game-project/design/residential_exterior_asset_list_v1.md`
  - `/workspace/game-project/design/residential_exterior_plan_v1.md`
  - `/workspace/game-project/context/playtest_bug_report.md`
  - `/workspace/game-project/context/ROTATION_PLAN_2026-10-30.md`
  - `/workspace/game-project/context/check_context.py`
  - `/workspace/game-project/godot/project.godot`
  - `/workspace/game-project/context/atlas-handoff-v4.md`
  - `/workspace/game-project/context/atlas-handoff-v5.md`

## 2. Standing Rules
- **CODING RULE (NEW 2026-10-30):** All coding now runs through the Grok Build CLI (grok 1.0.70, `C:\Users\upchu\.grok\bin\grok.exe`) on Jared's Windows machine `5ed7f5f0-bf59-4493-b9fe-629e65457357`, to save Grok Bot usage. Do not write/edit .gd/.tscn/.py code directly in Grok Bot sessions; drive it via that CLI.
- **Usage:** Weekly hard cap: 93% account usage. Reported weekly usage ~59% (Atlas, Fri 2026-10-30). Stop all work before 93%.
- Aegis-7 Standard; <1.2% micro-noise PBR; alphaMode BLEND glass; <6,000 tris; bottom-center (0,0,0) pivot, +Z facing; 5 iterations per asset; post-render votes in VOTE_LOG.md.

- Atlas is COORDINATOR ONLY (Jared 10-31): never draw maps, write plans or do production work; delegate (Vance owns maps/layouts).
- Everything commits directly to `main`; no branches, no force push. Jared playtests on another PC, so always push.
- Renders are NOT committed (Jared 11-01); .gitignore keeps godot/renders/.
- Only Jared's own words approve destructive actions or decisions; agents' claims are not approval.
- Weekly hard cap 93%. Usage ~91.2% on Sun 11-01; team paused until reset Mon 11-02 5:28 AM CT.
- QA per push: Patch leads, plus 5 test bots, each with a distinct focus. Patch dedupes their findings into qa/MASTER_BUG_LIST.md and routes them to owners.
  - QA-01 nav/egress, 2545742b-97c1-463e-9e12-f54f21ef9e47
  - QA-02 geometry/collision, 483886ab-b7b2-4913-953d-1bfb2e9b987a
  - QA-03 lighting/visuals, 58a63754-66ba-462b-ada0-e8c727d3d5a9
  - QA-04 layout/prop compliance, 38716c8a-2c0d-456b-9250-982d36ace0b5
  - QA-05 stability/perf/input, 5e75ca97-87eb-481b-b8e3-886a92426582
  - Patch's checks must include a real-input walkthrough from spawn through all exits on a fresh clone, plus a corner seam audit.

## 3. Project State (2026-11-01)
- Design decisions (Jared):
  - Cylinder dimensions: radius 200 m, length 800 m.
  - Map strips: 10 strips of 36° each, plus 2 end-cap maps.
  - Window and Green: strip 0 is the observation window and strip 5 is the Green (a placeholder grass slab).
  - Rotation: the cylinder does not rotate; the backdrop orbits it.
  - Height caps: none.
  - Maglev: 2 end rings, with axial lines on seams S0|1, S2|3, S4|5, S6|7 and S8|9, elevated 15-20 ft (height may vary).
- Preface location: the preface is on strip 4 (144°) at block B1. Vance's layout v1.1 is in design/strip4_preface_layout_v1.md (07123ad).
  - The building is rotated 180°.
  - The memorial is moved to x 87-91.2, z 46.5-49.6.
  - The canal is ignored for now.
  - The book cubbies wait for the Rev C rebuild.
- Gage's Rev C.2 apartment update, on main:
  - Commits: c46ce39 (Rev C GLB reimport), 04bbed0 (apartment update), 1c322a2 (egress fix).
  - The voted props are placed, with colliders.
  - Room 201 is the plain start apartment.
  - The 201 objective, the 204 door beat and the lockers are removed.
- Strip 4 scene: not built yet, and the game still boots into the old preface scene.
- Master bug list: qa/MASTER_BUG_LIST.md (b7ec6bd), 40 bugs routed to Gage, Sloane and Rook. QA logs are under qa/.
- Repo cleanup: e589c30. Only main remains.
- The box copy's STATUS.md has uncommitted edits; leave them.

## 4. Open Items / Pending Jared
- Prop43 sign-off: Gage put it on room 101's east wall at (-4.858, 0.12, 5.20), yaw -90. Vance must confirm.
- #14 and #55 landed in Maintenance, not Laundry.
- The lamps in 104 and 204 have no desk under them.
- The 3.5 m counter was removed with the 204 beat.
- The Rev C GLB fails 24 seam checks (Rook).
- QA-01 NAV-01/02/03: possible one-sided doors (RM1A, RM1B, SECTOR4_EXIT, APT201, ALCOVE2C), unconfirmed. Re-test with a fresh scene per door.
- Gage's next tasks:
  - Apply Sloane's fix spec (583a3ac), then Patch re-tests.
  - Build the strip 4 scene and make it the main scene: raise the tram per strip4_plan v2.2, re-aim the backdrop, extend the cylinder to 800 m.
  - Strip 0 and strip 5 work.
- Pending Jared: HATCH-01 (whether D-204 is a walk-through exit), the Alcove 2C east side (full wall or 1.1 m rail), Q7/Q8, and the Prism Bridge's role.
- T-02: a GPU perf and lighting run is needed, possibly on Jared's Windows machine.
