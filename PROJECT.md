# Project: O'Neill Cylinder Habitat (*Cylinder Hab-7*)

## Macro Setting & Hard Sci-Fi Visual Direction
- **Setting:** Inside a rotating **800m long × 400m diameter** O'Neill Cylinder deep-space habitat.
- **Art Direction — SLEEK HARD SCI-FI ("Aegis-7 Standard"):**
  - Gunmetal/charcoal anodized titanium bulkheads (`#1A1E24`), matte aerospace white/light-alloy molded composite shells (`#D8DEE6`), dark carbon-slate structural framing (`#282E38`), machined brushed titanium-steel gantries (`#88929E`), recessed cyan (`#00E5FF`), violet-UV (`#7B5CFF`), and amber (`#FF9500`) LED light strips, **true alpha-translucent glass** (`alphaMode: "BLEND"`, low opacity + specular reflection) for viewports, sterilizer doors, holo-HUD visors, cargo lids, and pressurized suit-bay doors.
  - Ultra-clean, low-noise PBR spacecraft surfaces (<1.2% micro-noise)—zero wood, zero wallpaper, zero busy patterns.

## Final Bunk Pod Lineup (4 Variations — LOCKED)
1. `bunk_winner_01_orbital_viewport.glb` — R1 #06 Orbital Viewport Pod (plus `_deepspace` / `_cylinder` vista variants)
2. `bunk_winner_02_medical_biomonitor.glb` — R2 #07 Medical Biomonitor Pod
3. `bunk_winner_03_hex_hive_stack.glb` — R2 #08 Modular Hex-Hive Stack
4. `bunk_winner_04_observation_lounge.glb` — R2 #09 Observation Lounge Sleeper
All in `/workspace/game-project/assets/glb/winners/`.

## Personal Crew Sleeping Quarters — Selected 5 Non-Bunk Fixtures/Furniture Lineup (`1, 2, 3, 6, 9` — ALL 5 LOCKED)
1. **#1 — EVA Suit & Personal Gear Locker (`locker_round1`):** **LOCKED WINNER `#02`** — `locker_winner_01_dual_bay_bulkhead.glb` (`#02 — Dual-Bay Recessed Bulkhead Suit & Kit Locker`, selected by Jared)
2. **#2 — Compact Hygiene & Sonic Wash Vanity (`vanity_round1`):** **LOCKED WINNER `#03` (5–0 Unanimous Vote)** — `vanity_winner_01_dual_zone_grooming.glb` (`#03 — Dual-Zone Split Grooming & UV Decon Station`)
3. **#3 — Personal Wall Terminal & Fold-Down Cabin Desk (`walldesk_round1`):** **LOCKED WINNER `#02` (5–0 Unanimous Vote)** — `walldesk_winner_01_split_comms_station.glb` (`#02 — Dual-Tier Split Comms & Storage Drop-Leaf Station`)
4. **#6 — Modular Cargo & Footlocker Chest (`footlocker_round1`):** **LOCKED WINNER `#02` (5–0 Unanimous Vote)** — `footlocker_winner_01_split_cargo_trunk.glb` (`#02 — Dual-Bay Split Cargo Trunk & Pull-Out Drawer Module`)
5. **#9 — Personal Climate & Life-Support Wall Panel (`climate_round1`):** **LOCKED WINNER `#02` (5–0 Unanimous Vote)** — `climate_winner_01_split_env_o2_station.glb` (`#02 — Dual-Zone Split Atmospheric Telemetry & Emergency Breather Bay`)

## 10-Room Master Architecture Pipeline (`MASTER_ARCHITECTURE_10_ROOMS.md`)
- **Room 01 — Crew Sleeping Quarters (`room_01_sleeping_quarters.tscn`):** **COMPLETE & RENDERED**
  - Renders: `/workspace/game-project/godot/renders/rooms/room_01/` (`cam_01`..`cam_04` + `room_01_sleeping_quarters_sheet.png`)
- **Room 02 — Curved Ring Transit Corridor & Airlock Junction (`corridor_round1`):** **COMPLETE & RENDERED (5–0 Unanimous Vote)**
  - Locked Hero Winner: `corridor_door_winner_01_dual_zone_portal.glb` (`#02 — Dual-Zone Airlock Portal & Emergency O2/Extinguisher Side Bay`, `5,472` tris) + `room_02_corridor_shell.glb`
  - Renders: `/workspace/game-project/godot/renders/rooms/room_02/` (`cam_01`..`cam_03`) + `/workspace/game-project/godot/renders/corridor_round1/corridor_door_round1_voting_sheet.png`
- **Room 03 — Orbital Mess Hall & Hydro-Galley (`galley_round1`):** **COMPLETE & RENDERED (`5–0` Unanimous Vote for `#02` — Full-Room Sheet in `/workspace/game-project/godot/renders/rooms/`)**
  - Renders: `/workspace/game-project/godot/renders/galley_round1/galley_synth_round1_voting_sheet.png`
- **Room 04 — Zero-G / Low-G Medical & Biomonitoring Bay (`medbay_round1`):** **COMPLETE & RENDERED (`5–0` Unanimous Vote for `#02` — Full-Room Sheet in `/workspace/game-project/godot/renders/rooms/`)**
- **Room 05 — EVA Prep & Decompression Chamber (`eva_round1`):** **COMPLETE & RENDERED (`5–0` Unanimous Vote for `#02` — Full-Room Sheet in `/workspace/game-project/godot/renders/rooms/`)**
  - Renders: `/workspace/game-project/godot/renders/eva_round1/eva_chamber_round1_voting_sheet.png`
- **Room 06 — Hydroponics & Bio-Scrubber Bay (`hydro_round1`):** **COMPLETE & RENDERED (`5–0` Unanimous Vote for `#02` — Full-Room Sheet in `/workspace/game-project/godot/renders/rooms/`)**
  - Renders: `/workspace/game-project/godot/renders/hydro_round1/hydro_column_round1_voting_sheet.png`
- **Room 07 — Habitat Command & Spin-Gravity Bridge (`bridge_round1`):** **COMPLETE & RENDERED (`5–0` Unanimous Vote for `#02` — Full-Room Sheet in `/workspace/game-project/godot/renders/rooms/`)**
  - Renders: `/workspace/game-project/godot/renders/bridge_round1/bridge_console_round1_voting_sheet.png`
- **Room 08 — Zero-G Panoramic Observation Lounge (`lounge_round1`):** **COMPLETE & RENDERED (`5–0` Unanimous Vote for `#02` — Full-Room Sheet in `/workspace/game-project/godot/renders/rooms/`)**
  - Renders: `/workspace/game-project/godot/renders/lounge_round1/lounge_bar_round1_voting_sheet.png`
- **Room 09 — Engineering & Spin-Drive Reactor Core (`engineering_round1`):** **COMPLETE & RENDERED (`5–0` Unanimous Vote for `#02` — Full-Room Sheet in `/workspace/game-project/godot/renders/rooms/`)**
  - Renders: `/workspace/game-project/godot/renders/engineering_round1/reactor_core_round1_voting_sheet.png`
- **Room 10 — Modular Cargo Hold & Drone Bay (`cargo_round1`):** **COMPLETE & RENDERED (`5–0` Unanimous Vote for `#02` — Full-Room Sheet in `/workspace/game-project/godot/renders/rooms/`)**
  - Renders: `/workspace/game-project/godot/renders/cargo_round1/cargo_gantry_round1_voting_sheet.png`

## Phase 2: 15 O'Neill Cylinder Building Exteriors (`bldg_01`–`bldg_15`) & Metropolis Skyline (Until 6:00 AM CT)
- **Master Exterior Bible:** `/workspace/game-project/MASTER_BUILDINGS_15_EXTERIORS.md` ("Aegis-7 Exterior Standard")
- **Design Spec & Exterior Textures (`Sloane`):** `/workspace/game-project/design/buildings_15_exteriors_spec.md` & `/workspace/game-project/assets/textures/buildings/`
- **Candidate Models (`Rook`):** 5 variations per building (`_r1_01`..`_r1_05`, `3,000–6,000` tris) in `/workspace/game-project/assets/glb/buildings/bldg_01/` .. `bldg_15/` (locked winners in `/workspace/game-project/assets/glb/winners/`)
- **Godot 4 Renders & Voting Sheets (`Gage`):** `/workspace/game-project/godot/renders/buildings/bldg_01/` .. `bldg_15/` (`bldg_XX_round1_voting_sheet.png`)

### District I — Residential & Civic Terrace Sector (`bldg_01` – `bldg_05`)
1. **Building 01 (`bldg_01_hab_spire`) — Aegis-7 Modular Crew Habitat Tower (`bldg_01_round1`):** COMPLETE & RENDERED (6–0 Unanimous Vote for `#02` in `VOTE_LOG.md`)
2. **Building 02 (`bldg_02_transit_rotunda`) — Elevated Mag-Lev & Ring Transit Rotunda (`bldg_02_round1`):** COMPLETE & RENDERED (6–0 Unanimous Vote for `#02` in `VOTE_LOG.md`)
3. **Building 03 (`bldg_03_culinary_atrium`) — Terraced Synthesizer & Culinary Commons Pavilion (`bldg_03_round1`):** COMPLETE & RENDERED (6–0 Unanimous Vote for `#02` in `VOTE_LOG.md`)
4. **Building 04 (`bldg_04_medical_trauma_center`) — Orbital Trauma & Biomonitor Medical Complex (`bldg_04_round1`):** COMPLETE & RENDERED (6–0 Unanimous Vote for `#02` in `VOTE_LOG.md`)
5. **Building 05 (`bldg_05_celestial_promenade_dome`) — Zero-G Observation & Recreation Dome (`bldg_05_round1`):** COMPLETE & RENDERED (6–0 Unanimous Vote for `#02` in `VOTE_LOG.md`)

### District II — Agri-Biosphere & Research Sector (`bldg_06` – `bldg_10`)
6. **Building 06 (`bldg_06_hydroponic_biodome`) — Aeroponic & Bio-Scrubber Conservatory Complex (`bldg_06_round1`):** COMPLETE & RENDERED (6–0 Unanimous Vote for `#02` in `VOTE_LOG.md`)
7. **Building 07 (`bldg_07_atmospheric_processor`) — Sector Atmospheric & O2/CO2 Scrubber Plant (`bldg_07_round1`):** COMPLETE & RENDERED (6–0 Unanimous Vote for `#02` in `VOTE_LOG.md`)
8. **Building 08 (`bldg_08_astrometry_observatory`) — Deep-Space Astrometry & Sensor Array Complex (`bldg_08_round1`):** COMPLETE & RENDERED (6–0 Unanimous Vote for `#02` in `VOTE_LOG.md`)
9. **Building 09 (`bldg_09_aquifer_pumping_station`) — Ring-Gravity Water Reclamation & Aquifer Cascade (`bldg_09_round1`):** COMPLETE & RENDERED (6–0 Unanimous Vote for `#02` in `VOTE_LOG.md`)
10. **Building 10 (`bldg_10_cryo_seed_vault`) — Colonial Cryo-Genetics & Seed Archive Vault (`bldg_10_round1`):** COMPLETE & RENDERED (6–0 Unanimous Vote for `#02` in `VOTE_LOG.md`)

### District III — Command, Power & Industrial Port Sector (`bldg_11` – `bldg_15`)
11. **Building 11 (`bldg_11_citadel_command_hq`) — Cylinder Hab-7 Central Command & Telemetry Citadel (`bldg_11_round1`):** COMPLETE & RENDERED (6–0 Unanimous Vote for `#02` in `VOTE_LOG.md`)
12. **Building 12 (`bldg_12_fusion_reactor_complex`) — D-He3 Fusion Power & Spin-Drive Reactor Hall (`bldg_12_round1`):** COMPLETE & RENDERED (6–0 Unanimous Vote for `#02` in `VOTE_LOG.md`)
13. **Building 13 (`bldg_13_cargo_logistics_port`) — High-Bay Intermodal Cargo & Drone Gantry Terminal (`bldg_13_round1`):** COMPLETE & RENDERED (6–0 Unanimous Vote for `#02` in `VOTE_LOG.md`)
14. **Building 14 (`bldg_14_eva_docking_pinnacle`) — Axial Zero-G Shuttle & EVA Docking Pinnacle (`bldg_14_round1`):** COMPLETE & RENDERED (6–0 Unanimous Vote for `#02` in `VOTE_LOG.md`)
15. **Building 15 (`bldg_15_solar_mirror_control_pylon`) — Orbital Solar-Mirror & Mag-Shield Control Pylon (`bldg_15_round1`):** COMPLETE & RENDERED (6–0 Unanimous Vote for `#02` in `VOTE_LOG.md`)

### Exterior District & Metropolis Godot 4 Scenes (`godot/scenes/buildings/` & `godot/renders/buildings/`)
- **`district_01_residential_civic.tscn` (`renders/buildings/district_01/district_01_sheet.png`):** Locked `#02` winners for Buildings 01–05
- **`district_02_agri_research.tscn` (`renders/buildings/district_02/district_02_sheet.png`):** Locked `#02` winners for Buildings 06–10
- **`district_03_command_industrial.tscn` (`renders/buildings/district_03/district_03_sheet.png`):** Locked `#02` winners for Buildings 11–15
- **`district_04_shipyard_civic.tscn` (`renders/buildings/district_04/district_04_sheet.png`):** Locked `#02` winners for Buildings 16–20 + Exterior Set Props 01–05
- **`cylinder_hab7_metropolis.tscn` (`renders/buildings/metropolis/cylinder_hab7_metropolis_sheet.png`):** Grand 20-Building + 5-Prop O'Neill Cylinder Exterior Metropolis Scene

## Active 7-Bot Studio Team Roster (`/workspace/game-project/context/roster.json`)
- **Atlas** (`e744c2d9-fd3b-4916-a082-3cedfae0b695`, rotated at 04:50 CDT; predecessor `60544a5c-ba31-4517-bd12-0fbc8e8ff9f0` renamed `delete-Atlas`) — Game PM (`/workspace/game-project/context/atlas-handoff-v3.md`)
- **Vance** (`0724beeb-94b9-43fa-a9cf-27117c5d4aa6`) — Sci-Fi Architect, Movie Prop & Set Design Specialist (`/workspace/game-project/context/vance-handoff-v1.md`)
- **Sloane** (`ec8a7e65-dd93-415c-9240-465e61fb2bcb`) — Interior, Lighting & Texture Designer (`/workspace/game-project/context/sloane-handoff-v2.md`)
- **Rook** (`61237674-1923-48c9-bc64-19c16cf2501e`) — 3D Modeling Specialist (`/workspace/game-project/context/rook-handoff-v2.md`)
- **Gage** (`5c9c9f64-e799-4958-97ab-f8cbf4f6ff90`, rotated at 05:27 CDT; predecessor `6ec49577-c331-44b3-8b56-dee044ba1d84` renamed `delete-Gage`) — Godot 4 Developer (`/workspace/game-project/context/gage-handoff-v2.md`)
- **Quinn** (`65d82323-1864-40e3-b8eb-90acde92ed1d`, created at 12:58 CDT) — Market Research & Gameplay Mechanics Strategist (`/workspace/game-project/context/quinn-handoff-v1.md`)
- **Scribe** (`929b3cf3-1ba3-489f-945f-4734223c6605`, rotated at 13:43 CDT; predecessor `49521640-e6fc-4f8f-b873-726f3f599220` renamed `delete-Scribe`) — Context & Handoff Manager (`/workspace/game-project/context/scribe-handoff-v4.md`)

### Phase 3: 5 Exterior Sci-Fi Movie Set & Plaza Props (`prop_01`–`prop_05`) & 5 District IV Building Exteriors (`bldg_16`–`bldg_20`) [COMPLETE & RENDERED — ALL 10 LOCKED 6–0 UNANIMOUS FOR `#02`]
- **Part A — 5 Exterior Sci-Fi Movie Set & Plaza Props (`prop_01_round1`..`prop_05_round1`, 25 `.glb`s in `/workspace/game-project/assets/glb/props/`, voting sheets in `/workspace/game-project/godot/renders/props/prop_01..05/`, canonical `#02` winners in `/workspace/game-project/assets/glb/winners/`):**
  - `prop_01_maglev_shuttle_pylon` (`prop_01_round1`): **LOCKED WINNER `#02` (6–0 Unanimous)** — `prop_01_winner_01_maglev_shuttle_pylon.glb` (`#02 — Dual-Zone Split Mag-Lev Guideway Y-Pylon, Docked Shuttle Pod & Translucent Telemetry Spine`, `2,016` tris)
  - `prop_02_holo_wayfinding_kiosk` (`prop_02_round1`): **LOCKED WINNER `#02` (6–0 Unanimous)** — `prop_02_winner_01_holo_wayfinding_kiosk.glb` (`#02 — Dual-Zone Split Sector Wayfinding Holo-Kiosk & Translucent Emergency Breather Locker`, `1,960` tris)
  - `prop_03_atmo_scrubber_bollard` (`prop_03_round1`): **LOCKED WINNER `#02` (6–0 Unanimous)** — `prop_03_winner_01_atmo_scrubber_bollard.glb` (`#02 — Dual-Zone Split Venturi Scrubber Intake & Translucent Ion-Filter / EVA Tether Bollard`, `1,908` tris)
  - `prop_04_civic_planter_bench_pod` (`prop_04_round1`): **LOCKED WINNER `#02` (6–0 Unanimous)** — `prop_04_winner_01_civic_planter_bench_pod.glb` (`#02 — Dual-Zone Split Contoured Crew Bench Lounge & Translucent UV-Aeroponic Planter Canopy`, `1,976` tris)
  - `prop_05_vtol_medevac_pad_array` (`prop_05_round1`): **LOCKED WINNER `#02` (6–0 Unanimous)** — `prop_05_winner_01_vtol_medevac_pad_array.glb` (`#02 — Dual-Zone Split Octagonal VTOL Landing Deck & Translucent Radar / Telemetry Dish Control Tower`, `2,212` tris)
- **Part B — 5 District IV Building Exteriors (`bldg_16_round1`..`bldg_20_round1`, 25 `.glb`s in `/workspace/game-project/assets/glb/buildings/`, voting sheets in `/workspace/game-project/godot/renders/buildings/bldg_16..20/`, canonical `#02` winners in `/workspace/game-project/assets/glb/winners/`):**
  - `bldg_16_shipyard_drydock_hall` (`bldg_16_round1`): **LOCKED WINNER `#02` (6–0 Unanimous)** — `bldg_16_winner_01_shipyard_drydock_hall.glb` (`#02 — Dual-Zone Split Shipyard Assembly Hall & Translucent Zero-G Micro-Shuttle Drydock Gantry Tower`, `4,664` tris)
  - `bldg_17_coriolis_recreation_arena` (`bldg_17_round1`): **LOCKED WINNER `#02` (6–0 Unanimous)** — `bldg_17_winner_01_coriolis_recreation_arena.glb` (`#02 — Dual-Zone Split Coriolis Kinetic Arena Hall & Translucent Multi-G Centrifuge Conditioning Tower`, `4,996` tris)
  - `bldg_18_colonial_holo_museum` (`bldg_18_round1`): **LOCKED WINNER `#02` (6–0 Unanimous)** — `bldg_18_winner_01_colonial_holo_museum.glb` (`#02 — Dual-Zone Split Colonial Archive Pavilion & Translucent Earth-Biosphere Holo-Orrery Tower`, `4,532` tris)
  - `bldg_19_synth_brewery_refinery` (`bldg_19_round1`): **LOCKED WINNER `#02` (6–0 Unanimous)** — `bldg_19_winner_01_synth_brewery_refinery.glb` (`#02 — Dual-Zone Split Protein Synthesis Refinery & Translucent Zero-G Botanical Distillation Column Tower`, `5,328` tris)
  - `bldg_20_meteor_defense_bastion` (`bldg_20_round1`): **LOCKED WINNER `#02` (6–0 Unanimous)** — `bldg_20_winner_01_meteor_defense_bastion.glb` (`#02 — Dual-Zone Split Armored Defense Bastion & Translucent Tachyon / Capacitor Beam-Relay Tower`, `5,328` tris)
- **District IV & Expanded 20-Building Metropolis Renders:**
  - **District IV (`district_04_shipyard_civic.tscn`):** `/workspace/game-project/godot/renders/buildings/district_04/district_04_sheet.png`
  - **Grand 20-Building + 5-Prop Metropolis (`cylinder_hab7_metropolis.tscn`):** `/workspace/game-project/godot/renders/buildings/metropolis/cylinder_hab7_metropolis_sheet.png`


## Standing Rules (added 2026-10-30)
- **Coding rule:** All coding now runs through the Grok Build CLI (grok 1.0.70, `C:\Users\upchu\.grok\bin\grok.exe`) on Jared's Windows machine `5ed7f5f0-bf59-4493-b9fe-629e65457357`, to save Grok Bot usage.
- **Usage cap:** Weekly hard cap 93% account usage; reported weekly usage ~59% (Atlas, Fri 2026-10-30).
