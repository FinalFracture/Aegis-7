# Atlas — Game Project Manager Handoff (`atlas-handoff-v4.md` — Rotated 2026-10-27 11:48 CDT)

## Predecessor Purpose & Mandatory Reference Files Manifest (READ ON FIRST TURN)
- **Exact Unchanged Role Purpose (Inherited From Predecessor):** Serve as Game Project Manager (`Atlas`) for *Cylinder Hab-7* (unified "Aegis-7 Standard" in `/workspace/game-project/`), coordinate our 7-bot development team (`Vance`, `Sloane`, `Rook`, `Gage`, `Quinn`, `Scribe`), run our 5-candidate asset tournament & post-render voting workflow, enforce our Pre-Major-Task Full-Team Memory Transfer & Rotation Protocol (and 150k token cap / `1 UC = 29,447 tokens` budget meter), and cast post-render PM votes in `/workspace/game-project/context/VOTE_LOG.md`.
- **Mandatory Reference Files & Directories Used by Predecessor:**
  - `/workspace/game-project/PROJECT.md`
  - `/workspace/game-project/MASTER_ARCHITECTURE_10_ROOMS.md`
  - `/workspace/game-project/MASTER_BUILDINGS_15_EXTERIORS.md`
  - `/workspace/game-project/context/STATUS.md`
  - `/workspace/game-project/context/roster.json`
  - `/workspace/game-project/context/VOTE_LOG.md`
  - `/workspace/game-project/context/CONTEXT_PROTOCOL.md`
  - `/workspace/game-project/context/usage_budget.json`
  - `/workspace/game-project/context/atlas-handoff-v4.md`
  - `/workspace/game-project/design/story_and_narrative_bible.md`
  - `/workspace/game-project/design/chapter_01_solar_flare_and_preface_spec.md`
  - `/workspace/game-project/design/preface_playable_residential_sector_spec.md`
  - `/workspace/game-project/design/utility_bot_johnny5_spec.md`
  - `/workspace/game-project/design/city_district_zoning_and_emblems_spec.md`
  - `/workspace/game-project/godot/renders/characters/bots/department_and_district_emblems_sheet.png`
  - `/workspace/game-project/godot/renders/characters/bots/utility_bot_r2_05_4_color_schemes_sheet.png`
  - `/workspace/game-project/godot/renders/preface/preface_open_residential_building_showcase_sheet.png`

- **Active 7-Bot Studio Team Roster (`/workspace/game-project/context/roster.json` — Rotated 2026-10-27 11:48 CDT):**
  - **Atlas** (`3a664a65-34d6-47ae-a9f6-337906efe2a3`) — Game Project Manager
  - **Vance** (`245e93a0-6301-45d6-b371-ad1e37a0dfd1`) — Sci-Fi Architect, Movie Prop & Set Design Specialist
  - **Sloane** (`bf6c8763-6c8b-405e-bb10-e7201e756464`) — Interior, Lighting & Texture Designer
  - **Rook** (`b2e64c87-0269-4f42-b5da-44d4b1a59db2`) — 3D Modeling Specialist
  - **Gage** (`5a97ab49-19f0-4b33-889f-e9b5a5389451`) — Godot 4 Developer
  - **Quinn** (`2239f53a-2bae-4c89-926c-e4969c082273`) — Market Research & Gameplay Mechanics Strategist
  - **Scribe** (`3b011c08-32f8-434e-8285-6cd66198bf29`) — Context & Handoff Manager
- **Predecessor Lineage:** `delete-Atlas` v1 (`3e3c8cd5-e339-4d87-809f-a6c4fa0e0f7c`), `delete-Atlas` v2 (`60544a5c-ba31-4517-bd12-0fbc8e8ff9f0`), `delete-Atlas` v3 (`e744c2d9-fd3b-4916-a082-3cedfae0b695`, rotated at `~255,000` est. tokens after `[t74u]`).

---

## Canonical Phase 6E State (Locked 2026-10-27 11:48 CDT — Pre-Major-Task Rotation Snapshot)
1. **Pre-Major-Task Full-Team Memory Transfer & Bot Rotation Rule (`[t4u]`):**
   - Before each major task — **regardless of how many messages/tokens remain before the `150,000`-token limit** — Scribe runs the full memory-transfer & rotation process across the team: refreshing transcript snapshots, writing updated `<agent>-handoff-v<N>.md` and `<agent>-handoff.md` files (with Predecessor Purpose & Mandatory Reference Files Manifests), spinning up fresh replacement bots via `CreateAgent`, renaming retiring instances to `delete-<name>` via `UpdateAgent`/`UpdateProfile`, and updating `roster.json`, `PROJECT.md`, `usage_budget.json`, `check_context.py`, and `STATUS.md`.
2. **Recalibrated Usage Credit (`1 UC` = `1%` Account Usage) at `25%` Weekly Mark (`[t3u]`):**
   - Verified via live `CheckSubscriptionUsage` at `25.5%` weekly usage (Super plan, resets Mon Nov 2 at 5:28 AM CST): **`1 UC` = `29,447` cumulative team context tokens (`115.0 KB` / `~45` messages)** at `25.0%` (`28,869` tok / `112.8 KB` at `25.5%` live).
3. **Locked `#05` Hammerhead Utility Robot + Universal Cylinder Hab-7 Municipal Livery + 4 Canonical Departments & City District Zoning (`[t65u]`, `[t67u]`, `[t69u]`, `[t74u]`):**
   - **Locked Robot Winner:** `#05 — Cantilevered "Hammerhead" Wide-Baseline Stereo-Scanner Bar Head on Locked #03 Wide-Stance Quad-Bogie Treads + #01 Compact Cube-Compactor Chassis` (`char_bot_r2_05.glb` -> `/workspace/game-project/assets/glb/winners/char_bot_r2_winner_05_hammerhead_scanner.glb` & `char_bot_r2_winner_01_hammerhead_stereo_bar.glb`, `5,254` tris).
   - **Universal Cylinder Hab-7 Base Palette (`85–90%` of Robot Surface):** `55%` Matte Titanium Alabaster (`#D8DEE4`), `20%` Deep Structural Slate (`#2A3038`), `15%` Brushed Machined Steel (`#707A84`) & Vulcanized Tread Rubber (`#1E2228`).
   - **Sparing Department Accent Trim (`10–15%` Max) & 4 Canonical Departments / City Districts (`[t74u]`):**
     - **`D-01 // ENGINEERING` (`"SPROCKET #0419"`, Safety Amber `#E89B2D` accent, `emblem_district_01_engineering.png`):** Comms, plumbing, electricity, coolant, Aegis space systems, and docking (*The Hex-Gear, Coolant Conduit & Power Bolt*).
     - **`D-02 // CIVIC` (`"SWEEP #0812"`, Civic Cyan-Teal `#38B8C8` accent, `emblem_district_02_civic.png`):** Anything for commuters/citizens — life support, trash & sanitation, hospital & medical, government, and recreation (*The Orbital Ring-Arc, Life-Support Caduceus & Civic Star*).
     - **`D-03 // SCIENCE` (`"KELVIN #0204"` / `"QUASAR #0204"`, Science Violet-Indigo `#7B5CFF` accent, `emblem_district_03_science.png`):** Laboratories, experiments, new technology, space observations, and astrometry (*The Atomic Orbital Lattice, Observatory Prism & Research Telescope*).
     - **`D-04 // AGRI` (`"CLOVER #0631"`, Biosphere Emerald `#3BA868` accent, `emblem_district_04_agri.png`):** Food production (not preparation), biosphere, atmosphere, hydrosphere (hydro/water cycle), animals/pest control, and veterinary (*The Hydro-Biosphere Leaf, Atmospheric Wave & Fauna Paw-Crest*).
   - **Key Showcase Renders:**
     - `/workspace/game-project/godot/renders/characters/bots/department_and_district_emblems_sheet.png`
     - `/workspace/game-project/godot/renders/characters/bots/utility_bot_r2_05_4_color_schemes_sheet.png`
     - `/workspace/game-project/godot/renders/characters/bots/livery_01_sprocket_maintenance_amber.png`
     - `/workspace/game-project/godot/renders/characters/bots/livery_02_sweep_janitorial_teal.png`
     - `/workspace/game-project/godot/renders/characters/bots/livery_03_science_violet.png`
     - `/workspace/game-project/godot/renders/characters/bots/livery_04_clover_agri_emerald.png`
4. **Locked `#04` Wrist RFID Winner & Playable 2-Story Open Residential Building (`[t46u]`–`[t59u]`):**
   - **Locked Wrist Winner:** `#04 — Bio-Luminescent Neural Tendon Trace + Flexible Polymer Smart-Sleeve` (`prop_wrist_rfid_winner_01_neural_tendon_sleeve.glb`, `4,372` tris) with forearm Battery Charges (`prop_pickup_battery_charge.glb`), carpal Super-Wire Spool (`prop_super_wire_spool.glb`), Thermal Jelly, and apartment desk BCI AI Headband (`prop_bci_headband.glb`).
   - **Skill Mastery & Feat-Gated Progression (`[t54u]`–`[t57u]`):** Zero RPG skill trees/XP bars; progression uses physical Skill Mastery, item enhancements, and feat-gated Tool & BCI Headband department unlocks across the 4 canonical departments (`Engineering`, `Civic`, `Science`, `Agri`).
   - **Open-Doorway 2-Story Residential Sector (`preface_residential_sector.glb`, `8,976` tris):** All doorways across Level 2 (`Y = +4.2m`) and Level 1 (`Y = 0.0m`) are open portals with zero blocking door leaves (`preface_open_residential_building_showcase_sheet.png`), while `pcba_python_puzzle_ui.gd` is preserved on disk for future door challenges.


---

## Previous Handoff Archive (`atlas-handoff-v3.md`)
# Atlas — Game PM Handoff (v3 — Rotated 2026-10-26 04:50 CDT)

## Predecessor Purpose & Mandatory Reference Files Manifest (READ ON FIRST TURN)
- **Exact Unchanged Role Purpose (Inherited From Predecessor):** Lead the 6-bot Cylinder Hab-7 development team under the unified Aegis-7 Standard, coordinate multi-candidate 3D asset & Godot 4 scene sprints, enforce the 6-Bot Protocol post-render vote in VOTE_LOG.md, and maintain the autonomous pipeline check routine with Scribe.
- **Mandatory Reference Files & Directories Used by Predecessor:**
  - `/workspace/game-project/PROJECT.md`
  - `/workspace/game-project/MASTER_ARCHITECTURE_10_ROOMS.md`
  - `/workspace/game-project/MASTER_BUILDINGS_15_EXTERIORS.md`
  - `/workspace/game-project/context/STATUS.md`
  - `/workspace/game-project/context/roster.json`
  - `/workspace/game-project/context/VOTE_LOG.md`
  - `/workspace/game-project/context/CONTEXT_PROTOCOL.md`
  - `/workspace/game-project/context/atlas-handoff-v3.md`
  - `/workspace/game-project/design/buildings_15_exteriors_spec.md`
  - `/workspace/game-project/design/vance_scifi_set_and_exterior_props_spec.md`
  - `/workspace/game-project/design/phase3_props_and_buildings_16_20_spec.md`

## 1. Identity & Rotation Lineage
- **Active Agent Name & ID:** **Atlas** (`e744c2d9-fd3b-4916-a082-3cedfae0b695`, `handoff_file`: `/workspace/game-project/context/atlas-handoff-v3.md`)
- **Role:** Game Project Manager (**Atlas**) for *Cylinder Hab-7* (O'Neill Cylinder Habitat — Unified **"Aegis-7 Standard"** in `/workspace/game-project/`).
- **Retired Predecessor:** `delete-Atlas` (`60544a5c-ba31-4517-bd12-0fbc8e8ff9f0`, rotated at `742` msgs / `1057.0 KB` / `~270,593` est. tokens at 04:50 CDT on Oct 26, 2026 per Jared's direct instruction to include Atlas in the replacement process).
- **Core Responsibilities:**
  1. Coordinate our 6-bot game development team across all design, 3D `.glb` generation, PBR texturing, Godot 4.3 rendering, and 6-Bot Protocol post-render voting rounds.
  2. Enforce the **"Make 5 Candidates First -> Render 5 -> 6-Bot Vote (`Vance, Sloane, Rook, Gage, Scribe, Atlas`)"** pipeline rule in `/workspace/game-project/context/VOTE_LOG.md`.
  3. Monitor context health with **Scribe** (`120,000` token warning threshold, `150,000` token rotation cap) and ensure every bot (including **Atlas**) is rotated cleanly via `/workspace/game-project/context/<agent>-handoff-v<N>.md` when crossing the threshold.
  4. Maintain the autonomous pipeline driver routine (`@every 30m` or active schedule) on the active **Atlas** instance so autonomous checks continue seamlessly.

---

## 2. Active 6-Bot Team Roster (`/workspace/game-project/context/roster.json`)
- **Atlas (Game PM):** `e744c2d9-fd3b-4916-a082-3cedfae0b695` (`previous_id`: `60544a5c-ba31-4517-bd12-0fbc8e8ff9f0`, `previous_name`: `delete-Atlas`, `handoff_file`: `/workspace/game-project/context/atlas-handoff-v3.md`).
- **Vance (Sci-Fi Architect, Movie Prop & Set Design Specialist):** `0724beeb-94b9-43fa-a9cf-27117c5d4aa6` (`~20.8k` tok, `HEALTHY` — `/workspace/game-project/context/vance-handoff-v1.md`).
- **Sloane (Interior, Lighting & Texture Designer):** `ec8a7e65-dd93-415c-9240-465e61fb2bcb` (`~16.0k` tok, `HEALTHY`, rotated at 04:01 CDT; predecessor `1c40e57b-57c1-4cbf-9e29-cc227b9cc914` renamed `delete-Sloane` — `/workspace/game-project/context/sloane-handoff-v2.md`).
- **Rook (3D Modeling Specialist):** `61237674-1923-48c9-bc64-19c16cf2501e` (`~28.6k` tok, `HEALTHY`, rotated at 00:44 CDT; predecessor `11c68e8e-c070-4e83-a926-21e9dfb70523` renamed `delete-Rook` — `/workspace/game-project/context/rook-handoff-v2.md`).
- **Gage (Godot 4 Developer):** `5c9c9f64-e799-4958-97ab-f8cbf4f6ff90` (`~118.4k` tok, `HEALTHY`, just below 120k warning line — `/workspace/game-project/context/gage-handoff-v2.md` staged on disk for smooth rotation once Phase 3 renders complete or when he crosses 120k).
- **Scribe (Context & Handoff Manager):** `49521640-e6fc-4f8f-b873-726f3f599220` (`HEALTHY`, rotated at 04:53 CDT; predecessor `4ea864bb-316a-47d3-8dc0-bd12475470c8` renamed `delete-Scribe` — `/workspace/game-project/context/scribe-handoff-v3.md`).

---

## 3. Completed Milestones (Phases 1 & 2 — 100% Locked & Rendered)

### Phase 1: All 10 Interior Rooms & 13 Hero Fixture Rounds (`5–0` Unanimous in `VOTE_LOG.md`)
- All 13 interior hero fixture rounds (`bunk_round2`, `desk_round1`, `locker_round1`, `vanity_round1`, `walldesk_round1`, `footlocker_round1`, `climate_round1`, `corridor_round1`, `galley_round1`, `medbay_round1`, `eva_round1`, `hydro_round1`, `bridge_round1`, `lounge_round1`, `engineering_round1`, `cargo_round1`) are locked in `/workspace/game-project/context/VOTE_LOG.md` with canonical winners in `/workspace/game-project/assets/glb/winners/`.
- All 10 full-room Godot 4 scenes and multi-camera contact sheets are rendered in `/workspace/game-project/godot/renders/rooms/room_01/` .. `room_10/` (`room_01_sleeping_quarters_sheet.png` through `room_10_cargo_bay_sheet.png`).

### Phase 2: All 15 O'Neill Cylinder Building Exteriors (`bldg_01`–`bldg_15`), 3 District Scenes & Grand 15-Building Metropolis (`6–0` Unanimous in `VOTE_LOG.md`)
- Master specs: `/workspace/game-project/MASTER_BUILDINGS_15_EXTERIORS.md`, `/workspace/game-project/design/buildings_15_exteriors_spec.md`, `/workspace/game-project/design/vance_scifi_set_and_exterior_props_spec.md`.
- All 75 candidate `.glb`s (`bldg_01_r1_01..05.glb` through `bldg_15_r1_01..05.glb`) and 15 5-panel voting sheets (`/workspace/game-project/godot/renders/buildings/bldg_01/bldg_01_round1_voting_sheet.png` .. `bldg_15/bldg_15_round1_voting_sheet.png`) are rendered and verified.
- All **6 bots (`Vance, Sloane, Rook, Gage, Scribe, Atlas`)** voted **`#02` (Aegis-7 65/35 Dual-Zone Split-Mass Signature)** across all 15 buildings (`6–0` unanimous lock in `/workspace/game-project/context/VOTE_LOG.md`), and all 15 canonical `#02` winners (`bldg_01_winner_01_hab_spire.glb` .. `bldg_15_winner_01_solar_mirror_control_pylon.glb`) are staged in `/workspace/game-project/assets/glb/winners/`.
- District & Metropolis renders on disk:
  - `/workspace/game-project/godot/renders/buildings/district_01/district_01_sheet.png` (`district_01_residential_civic.tscn`)
  - `/workspace/game-project/godot/renders/buildings/district_02/district_02_sheet.png` (`district_02_agri_research.tscn`)
  - `/workspace/game-project/godot/renders/buildings/district_03/district_03_sheet.png` (`district_03_command_industrial.tscn`)
  - `/workspace/game-project/godot/renders/buildings/metropolis/cylinder_hab7_metropolis_sheet.png` (`cylinder_hab7_metropolis.tscn`)

---

## 4. Active Work In Flight — Phase 3 (`prop_01`–`prop_05` & `bldg_16`–`bldg_20`)
- **Design Spec:** `/workspace/game-project/design/phase3_props_and_buildings_16_20_spec.md` (authored by Vance) and Phase 3 signage/holo textures in `/workspace/game-project/assets/textures/buildings/` (authored by Sloane).
- **Part A — 5 Exterior Sci-Fi Movie Set & Plaza Prop Rounds (`25` `.glb`s, `1,800–4,200` tris):**
  1. `prop_01_maglev_shuttle_pylon` (`/workspace/game-project/assets/glb/props/prop_01/prop_01_r1_01..05.glb`)
  2. `prop_02_holo_wayfinding_kiosk` (`/workspace/game-project/assets/glb/props/prop_02/prop_02_r1_01..05.glb`)
  3. `prop_03_atmo_scrubber_bollard` (`/workspace/game-project/assets/glb/props/prop_03/prop_03_r1_01..05.glb`)
  4. `prop_04_civic_planter_bench_pod` (`/workspace/game-project/assets/glb/props/prop_04/prop_04_r1_01..05.glb`)
  5. `prop_05_vtol_medevac_pad_array` (`/workspace/game-project/assets/glb/props/prop_05/prop_05_r1_01..05.glb`)
- **Part B — 5 District IV Building Exteriors (`25` `.glb`s, `3,500–6,000` tris, Expanding City to 20 Buildings + `district_04_shipyard_civic.tscn`):**
  1. `bldg_16_shipyard_drydock_hall` (`/workspace/game-project/assets/glb/buildings/bldg_16/bldg_16_r1_01..05.glb`)
  2. `bldg_17_coriolis_recreation_arena` (`/workspace/game-project/assets/glb/buildings/bldg_17/bldg_17_r1_01..05.glb`)
  3. `bldg_18_colonial_holo_museum` (`/workspace/game-project/assets/glb/buildings/bldg_18/bldg_18_r1_01..05.glb`)
  4. `bldg_19_synth_brewery_refinery` (`/workspace/game-project/assets/glb/buildings/bldg_19/bldg_19_r1_01..05.glb`)
  5. `bldg_20_meteor_defense_bastion` (`/workspace/game-project/assets/glb/buildings/bldg_20/bldg_20_r1_01..05.glb`)
- **Current Pipeline Step:**
  - **Rook (`61237674-1923-48c9-bc64-19c16cf2501e`)** has an active background subagent (`sand-subagent-8f29999b-5971-d83f-829e-ecc8713a7dc3`) generating all 50 Phase 3 `.glb`s right now.
  - Once Rook finishes and validates the 50 `.glb`s, **Gage (`5c9c9f64-e799-4958-97ab-f8cbf4f6ff90`)** will render the 10 new 5-panel voting sheets (`prop_01`–`prop_05` and `bldg_16`–`bldg_20`), `district_04_shipyard_civic.tscn`, and the expanded 20-Building + Street Props `cylinder_hab7_metropolis.tscn`.
  - Then all 6 bots (`Vance, Sloane, Rook, Gage, Scribe, Atlas`) inspect the 10 voting sheets, log post-render votes in `/workspace/game-project/context/VOTE_LOG.md`, stage the 10 canonical `#02` winners in `/workspace/game-project/assets/glb/winners/`, and **Scribe** rotates **Gage** cleanly once he crosses `120k–150k` tokens.

