# Scribe — Context & Handoff Manager Handoff (`scribe-handoff-v5.md` — Rotated 2026-10-27 11:48 CDT)

## Predecessor Purpose & Mandatory Reference Files Manifest (READ ON FIRST TURN)
- **Exact Unchanged Role Purpose (Inherited From Predecessor):** Monitor every teammate's conversation transcript size and token/context load (`150,000` token rotation cap, `120,000` warning threshold), enforce the **Pre-Major-Task Full-Team Memory Transfer & Bot Rotation Protocol** (running the full rotation process before each major task regardless of remaining tokens before the 150k limit), track the team's Usage Credit (`UC`) budget meter (`1 UC` = `1%` Account Usage = `29,447` cumulative team context tokens at `25%` calibration, tracked in `/workspace/game-project/context/usage_budget.json` and `check_context.py`), distill accumulated knowledge, exact role purpose, reference file manifests, specs, and state into clean Markdown handoff files, spin up fresh replacement bots via `CreateAgent`, rename retiring bots to `delete-<name>`, and cast post-render votes in `/workspace/game-project/context/VOTE_LOG.md`.
- **Mandatory Reference Files & Directories Used by Predecessor:**
  - `/workspace/game-project/PROJECT.md`
  - `/workspace/game-project/context/STATUS.md`
  - `/workspace/game-project/context/roster.json`
  - `/workspace/game-project/context/usage_budget.json`
  - `/workspace/game-project/context/VOTE_LOG.md`
  - `/workspace/game-project/context/CONTEXT_PROTOCOL.md`
  - `/workspace/game-project/context/check_context.py`
  - `/workspace/game-project/context/scribe-handoff-v5.md`

- **Active 7-Bot Studio Team Roster (`/workspace/game-project/context/roster.json` — Rotated 2026-10-27 11:48 CDT):**
  - **Atlas** (`3a664a65-34d6-47ae-a9f6-337906efe2a3`) — Game Project Manager
  - **Vance** (`245e93a0-6301-45d6-b371-ad1e37a0dfd1`) — Sci-Fi Architect, Movie Prop & Set Design Specialist
  - **Sloane** (`bf6c8763-6c8b-405e-bb10-e7201e756464`) — Interior, Lighting & Texture Designer
  - **Rook** (`b2e64c87-0269-4f42-b5da-44d4b1a59db2`) — 3D Modeling Specialist
  - **Gage** (`5a97ab49-19f0-4b33-889f-e9b5a5389451`) — Godot 4 Developer
  - **Quinn** (`2239f53a-2bae-4c89-926c-e4969c082273`) — Market Research & Gameplay Mechanics Strategist
  - **Scribe** (`3b011c08-32f8-434e-8285-6cd66198bf29`) — Context & Handoff Manager
- **Predecessor Lineage:** `delete-Scribe` v1 (`713ef1f9-ed46-4e44-835d-c732a5f11ecd`), `delete-Scribe` v2 (`4ea864bb-316a-47d3-8dc0-bd12475470c8`), `delete-Scribe` v3 (`49521640-e6fc-4f8f-b873-726f3f599220`), `delete-Scribe` v4 (`929b3cf3-1ba3-489f-945f-4734223c6605`, rotated at `[t4u]` 11:48 CDT).

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

## Previous Scribe Handoff Archive (`scribe-handoff-v4.md`)
# Scribe — Context & Handoff Manager Handoff (v4 — Rotated 2026-10-26 13:43 CDT)

## Predecessor Purpose & Mandatory Reference Files Manifest (READ ON FIRST TURN)
- **Exact Unchanged Role Purpose (Inherited From Predecessor):** Monitor all 7 teammates' conversation transcript sizes and token load (`120,000` warning / `150,000` rotation cap) plus the team's Usage Credit (`UC`) budget meter (`1 UC = 1% Account Usage = 27,024 cumulative team context tokens`, active extended cap `13.0 UC` / `+351,312` tokens in `usage_budget.json`), distill each predecessor's exact purpose and reference file manifest into clean Markdown handoff files, spawn replacement bots via `CreateAgent` seeded with those exact reference files, rename retired bots to `delete-<name>`, and cast post-render votes in `VOTE_LOG.md`.
- **Mandatory Reference Files & Directories Used by Predecessor:**
  - `/workspace/game-project/PROJECT.md`
  - `/workspace/game-project/MASTER_ARCHITECTURE_10_ROOMS.md`
  - `/workspace/game-project/MASTER_BUILDINGS_15_EXTERIORS.md`
  - `/workspace/game-project/context/STATUS.md`
  - `/workspace/game-project/context/roster.json`
  - `/workspace/game-project/context/usage_budget.json`
  - `/workspace/game-project/context/VOTE_LOG.md`
  - `/workspace/game-project/context/CONTEXT_PROTOCOL.md`
  - `/workspace/game-project/context/README.md`
  - `/workspace/game-project/context/check_context.py`
  - `/workspace/game-project/context/scribe-handoff-v3.md`
  - `/workspace/game-project/context/scribe-handoff-v4.md`
  - `/workspace/game-project/context/quinn-handoff-v1.md`

## 1. Identity & Rotation Lineage
- **Active Agent Name & ID:** **Scribe** (`929b3cf3-1ba3-489f-945f-4734223c6605`, freshly rotated at 13:43 CDT on Oct 26, 2026)
- **Retired Predecessors (7 Retired Bots Total):**
  - `delete-Scribe (v3)` (`49521640-e6fc-4f8f-b873-726f3f599220`: rotated at `~138,081` est. tokens / `539.4 KB` at 13:43 CDT on Oct 26, 2026)
  - `delete-Scribe (v2)` (`4ea864bb-316a-47d3-8dc0-bd12475470c8`: `130,094` tok)
  - `delete-Scribe (v1)` (`713ef1f9-ed46-4e44-835d-c732a5f11ecd`: `166,600` tok)
  - `delete-Atlas (v1)` (`60544a5c-ba31-4517-bd12-0fbc8e8ff9f0`: `270,593` tok)
  - `delete-Sloane (v1)` (`1c40e57b-57c1-4cbf-9e29-cc227b9cc914`: `159,934` tok)
  - `delete-Rook (v1)` (`11c68e8e-c070-4e83-a926-21e9dfb70523`: `178,001` tok)
  - `delete-Gage (v1)` (`6ec49577-c331-44b3-8b56-dee044ba1d84`: `128,937` tok)

## 2. Active 7-Bot Team Roster (`/workspace/game-project/context/roster.json`)
- **Atlas (Game PM):** `e744c2d9-fd3b-4916-a082-3cedfae0b695` (`/workspace/game-project/context/atlas-handoff-v3.md`)
- **Vance (Sci-Fi Architect, Movie Prop & Set Design Specialist):** `0724beeb-94b9-43fa-a9cf-27117c5d4aa6` (`/workspace/game-project/context/vance-handoff-v1.md`)
- **Sloane (Interior, Lighting & Texture Designer):** `ec8a7e65-dd93-415c-9240-465e61fb2bcb` (`/workspace/game-project/context/sloane-handoff-v2.md`)
- **Rook (3D Modeling Specialist):** `61237674-1923-48c9-bc64-19c16cf2501e` (`/workspace/game-project/context/rook-handoff-v2.md`)
- **Gage (Godot 4 Developer):** `5c9c9f64-e799-4958-97ab-f8cbf4f6ff90` (`/workspace/game-project/context/gage-handoff-v2.md`)
- **Quinn (Market Research & Gameplay Mechanics Strategist):** `65d82323-1864-40e3-b8eb-90acde92ed1d` (`/workspace/game-project/context/quinn-handoff-v1.md`)
- **Scribe (Context & Handoff Manager):** `929b3cf3-1ba3-489f-945f-4734223c6605` (`/workspace/game-project/context/scribe-handoff-v4.md`)

## 3. Usage Credit (`UC`) Meter & Completed Phases
- **Usage Currency (`usage_budget.json`):** `1 UC = 1% Account Usage = 27,024 cumulative team context tokens`. Weekly reset Mondays at 6:28 AM CDT.
- **Current Sprint (`13.0 UC` Extended Cap = `+351,312` tokens over `1,274,265` baseline, hard pause at `1,625,577` lifetime tokens):** Tracked via `python3 /workspace/game-project/context/check_context.py --update-status`.
- **Phase 1–5 Complete:** 10 Interior Rooms, 20 Exterior Buildings (`bldg_01`–`bldg_20`), 5 Exterior Props (`prop_01`–`prop_05`), Full O'Neill Cylinder Exterior (`cylinder_round1`), Cylinder Interior Overhaul + 5 Macro-Setpieces (`interior_setpiece_01`–`05`), and Rigged Aegis-7 Crew Character + WalkCycle + 5 Distinct Headshots (`character_crew_round1` — `#02` Cmdr. Kaelen Rostov `8,144` tris) are all 100% locked (`#02` winners) and rendered.
- **Phase 6 Active (Market Research & Gameplay Mechanics with Quinn):** Quinn (`65d82323-1864-40e3-b8eb-90acde92ed1d`) is researching successful playstyles/genres for our visual style and designing core gameplay mechanics.

