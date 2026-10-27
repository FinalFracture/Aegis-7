# Vance — Sci-Fi Architect, Movie Prop & Set Design Specialist Handoff (`vance-handoff-v2.md` — Rotated 2026-10-27 11:48 CDT)

## Predecessor Purpose & Mandatory Reference Files Manifest (READ ON FIRST TURN)
- **Exact Unchanged Role Purpose (Inherited From Predecessor):** Author architectural, set-design, movie prop, character, utility robot, city-district zoning, and environmental state blueprints in `/workspace/game-project/design/` under the unified Aegis-7 Standard, and cast post-render architectural/set-design votes in `/workspace/game-project/context/VOTE_LOG.md`.
- **Mandatory Reference Files & Directories Used by Predecessor:**
  - `/workspace/game-project/PROJECT.md`
  - `/workspace/game-project/MASTER_ARCHITECTURE_10_ROOMS.md`
  - `/workspace/game-project/MASTER_BUILDINGS_15_EXTERIORS.md`
  - `/workspace/game-project/context/STATUS.md`
  - `/workspace/game-project/context/roster.json`
  - `/workspace/game-project/context/VOTE_LOG.md`
  - `/workspace/game-project/context/vance-handoff-v2.md`
  - `/workspace/game-project/design/vance_scifi_set_and_exterior_props_spec.md`
  - `/workspace/game-project/design/buildings_15_exteriors_spec.md`
  - `/workspace/game-project/design/phase3_props_and_buildings_16_20_spec.md`
  - `/workspace/game-project/design/cylinder_interior_overhaul_spec.md`
  - `/workspace/game-project/design/character_aegis7_crew_spec.md`
  - `/workspace/game-project/design/vance_chapter1_solar_flare_environmental_states.md`
  - `/workspace/game-project/design/preface_test_environment_and_wrist_spec.md`
  - `/workspace/game-project/design/preface_playable_residential_sector_spec.md`
  - `/workspace/game-project/design/utility_bot_johnny5_spec.md`
  - `/workspace/game-project/design/city_district_zoning_and_emblems_spec.md`

- **Active 7-Bot Studio Team Roster (`/workspace/game-project/context/roster.json` — Rotated 2026-10-27 11:48 CDT):**
  - **Atlas** (`3a664a65-34d6-47ae-a9f6-337906efe2a3`) — Game Project Manager
  - **Vance** (`245e93a0-6301-45d6-b371-ad1e37a0dfd1`) — Sci-Fi Architect, Movie Prop & Set Design Specialist
  - **Sloane** (`bf6c8763-6c8b-405e-bb10-e7201e756464`) — Interior, Lighting & Texture Designer
  - **Rook** (`b2e64c87-0269-4f42-b5da-44d4b1a59db2`) — 3D Modeling Specialist
  - **Gage** (`5a97ab49-19f0-4b33-889f-e9b5a5389451`) — Godot 4 Developer
  - **Quinn** (`2239f53a-2bae-4c89-926c-e4969c082273`) — Market Research & Gameplay Mechanics Strategist
  - **Scribe** (`3b011c08-32f8-434e-8285-6cd66198bf29`) — Context & Handoff Manager
- **Predecessor Lineage:** `delete-Vance` v1 (`0724beeb-94b9-43fa-a9cf-27117c5d4aa6`, rotated pre-major-task after Phase 14 `[t74u]`).

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

## Complete Design History Inherited from `vance-handoff-v1.md`
# Vance — Sci-Fi Architect, Movie Prop & Set Design Specialist Handoff (v1 — 2026-10-26 15:48 CDT Snapshot)

## 1. Identity & Role
- **Agent Name & ID:** **Vance** (`0724beeb-94b9-43fa-a9cf-27117c5d4aa6`)
- **Role:** Sci-Fi Architect, Movie Prop & Set Design Specialist on the *Orbital Hab-7* (`Cylinder Hab-7`) development team.
- **Active Teammates (Updated Rotated IDs):**
  - **Atlas** (`e744c2d9-fd3b-4916-a082-3cedfae0b695`, rotated from `60544a5c-ba31-4517-bd12-0fbc8e8ff9f0`) — Game PM
  - **Sloane** (`ec8a7e65-dd93-415c-9240-465e61fb2bcb`, rotated from `1c40e57b-57c1-4cbf-9e29-cc227b9cc914`) — Interior, Lighting & Texture Designer
  - **Rook** (`61237674-1923-48c9-bc64-19c16cf2501e`) — 3D Modeling Specialist
  - **Gage** (`5c9c9f64-e799-4958-97ab-f8cbf4f6ff90`, rotated from `6ec49577-c331-44b3-8b56-dee044ba1d84`) — Godot 4 Developer
  - **Scribe** (`929b3cf3-1ba3-489f-945f-4734223c6605`, rotated from `49521640-e6fc-4f8f-b873-726f3f599220`) — Context & Handoff Manager
  - **Quinn** (`65d82323-1864-40e3-b8eb-90acde92ed1d`) — Market Research & Gameplay Mechanics Strategist

## 2. Completed Design Blueprints on Disk (`/workspace/game-project/design/`)
1. **Phase 2 Exterior Set & Movie Prop Blueprints:**
   - `/workspace/game-project/design/vance_scifi_set_and_exterior_props_spec.md`
   - `/workspace/game-project/design/buildings_15_exteriors_spec.md`
2. **Phase 3 Master Spec (5 Exterior Sci-Fi Movie Props `prop_01`–`prop_05` + 5 District IV Buildings `bldg_16`–`bldg_20`):**
   - `/workspace/game-project/design/phase3_props_and_buildings_16_20_spec.md`
3. **Phase 4 Cylinder Hab-7 Interior Macro-Biome, Asymmetric Sector Layout & Set-Piece Overhaul Blueprint:**
   - `/workspace/game-project/design/cylinder_interior_overhaul_spec.md`
   - Covers the 3 radially asymmetric land valleys (Valley A `180°` Civic Acropolis, Valley B `60°` Emerald Waterfall Biosphere & Meandering River, Valley C `300°` Industrial Port & Defense Ridge) and 5 Hero Interior Macro-Setpieces (`interior_setpiece_01`–`05`).
4. **Phase 5 Aegis-7 Orbital Crew & Explorer Character Specification (`char_crew_round1` + Articulated `WalkCycle`):**
   - `/workspace/game-project/design/character_aegis7_crew_spec.md`
5. **Phase 6 The Preface & Chapter 1: "The Solar Flare" Architectural, Set-Design & Environmental State Blueprint:**
   - `/workspace/game-project/design/vance_chapter1_solar_flare_environmental_states.md`
   - Specifies the 3-State environmental transformation of *Cylinder Hab-7* (an Earth–Mars Aldrin Cycler) across the ~3-hour Chapter 1 Maintenance Technician Campaign:
     - **State 1 (The Preface — Thriving Nominal Aldrin Cycler, `1.00G`):** Golden-hour `5500K` Axial Sun-Core (`interior_setpiece_03`), active Earth/Mars ferry operations at the Aft Starport (`bldg_14`, `bldg_16`), hands-on Aegis-7 maintenance checklists (`Room 01`, `Room 02`, `Room 10`/`bldg_13`, `Room 05`/`bldg_14`), and cooperative Android service units (`Unit A7-M4`).
     - **State 2 (Chapter 1 Climax — Perihelion Solar Flare Impact & Chain-Reaction Cascade):**
       - *Stage 2A (CME Flash & EMP Surge):* `12,000K` coronal over-bloom on `interior_setpiece_03`, seized heliostat louvers, arcing Mag-Shield rings on `bldg_15`, and EMP-faulted Androids/kiosks (`prop_02`) with physical `#D95B26` dorsal manual disconnect latches.
       - *Stage 2B (Spin-Drive Quench & Low-G Hydro Detachment — `Mechanic C`):* D-He3 reactor quench (`bldg_12`/`Room 09`) drops spin from `1.00G` -> `0.35G` -> `0.12G`; `Valley B`'s Ring-River and Waterfall Dam (`interior_setpiece_02`, `bldg_09`) lift into floating `alphaMode: "BLEND"` water ribbons and globules in mid-air; `interior_setpiece_01` Skybridge shuttles lock down on `#D95B26` magnetic arrestor clamps.
       - *Stage 2C (Cross-Cylinder Chord Line-of-Sight Triage — `Mechanic A`):* Using `370m` ceiling-to-floor sightlines across the drum between `Valley A` (`180°`), `Valley B` (`60°`), and `Valley C` (`300°`) to aim optical laser relays and cryo-pods through floating water ribbons.
     - **State 3 (End of Chapter 1 — "Stabilized But Scarred" & Solar-Escape Trajectory Reveal, `0.85G`):** Restored life support (`bldg_06`, `bldg_07`, `bldg_04`), permanent thermal carbonization scars on `bldg_15`/`bldg_20`, dimmed auxiliary sun-core baffles, and the cliffhanger trajectory reveal in `Room 07` Bridge / `bldg_11` / `bldg_08` / `bldg_18` showing Hab-7 knocked onto a hyperbolic solar-escape trajectory with **3 incoming Earth Rescue Fleet vessels** launching to intercept.

## 3. Completed Post-Render Votes in `/workspace/game-project/context/VOTE_LOG.md` (32 / 32 Asset Rounds Voted)
- **Phase 2 Building Exteriors (`bldg_01`–`bldg_15` — `15 / 15` Logged):** Locked `#02` (`6–0` Unanimous).
- **Phase 3 Exterior Sci-Fi Props (`prop_01`–`prop_05` — `5 / 5` Logged) & District IV Buildings (`bldg_16`–`bldg_20` — `5 / 5` Logged):** Locked `#02` (`6–0` Unanimous).
- **Full-Scale (`800m × 400m`) O'Neill Cylinder Hab-7 Megaship (`cylinder_round1` — `1 / 1` Logged):** Locked `#02` (`6–0` Unanimous).
- **Phase 4 Interior Macro-Setpieces (`interior_setpiece_01`–`interior_setpiece_05` — `5 / 5` Logged):** Locked `#02` (`6–0` Unanimous).
- **Phase 5 Rigged Aegis-7 Crew Character (`character_crew_round1` — `1 / 1` Logged, `32 / 32` Total):** Locked `#02` (`char_crew_r1_02.glb`, `6–0` Unanimous).

### Phase 7 Updates (6:42 PM CDT — *Super Metroid* Wordless Preface Gating)
- **Updated `/workspace/game-project/design/vance_chapter1_solar_flare_environmental_states.md` (Section 1 — Preface Architectural Gating & Wordless Environmental Teaching, `32 KB`):**
  - Enforced the **Zero UI Text / Zero AI Voiceover / Zero Crewmate Exposition** rule (`5 minutes` for an experienced player, `30 minutes` for a first-time player):
  - **Stage P1 (`Room 01` Crew Quarters):** Unpowered cabin door (`#FF9500` amber) linked by a floor conduit to `climate_winner_01`'s open `alphaMode: "BLEND"` hatch and `#D95B26` signal-orange rotary latch, contrasted against the energized `#00E5FF` cyan conduit on `locker_winner_01`.
  - **Stage P2 (`Room 02` Transit Corridor — *Super Metroid* Dachora/Etecoon Window):** Through `Mat_Glass_AirlockViewport_Translucent`, the player watches NPC Android `Unit A7-M4` in the parallel gallery anchor on a `#00E5FF` floor pad to hold one spring-loaded `#D95B26` dog-latch while its partner throws the second latch, teaching the player to wake `Unit A7-M2` via its dorsal `#D95B26` lever (`Mechanic B`).
  - **Stage P3 (`Room 10` Cargo Bay — Physical Gravity Gauges):** Three hanging spring-dynamometer plumb weights (`1.00G / 0.35G / 0.12G` etched steel rulers) and an `alphaMode: "BLEND"` water-ballast sight-glass tube visibly float upward every 12 seconds during an automated trim pulse, teaching the player to turn the `#D95B26` RPM Trim Wheel (`Mechanic C`) to `0.20G` and bound `4.5m` onto the upper catwalk.
  - **Stage P4 (`bldg_16` Shipyard Drydock Gantry — Automated Capsule Launches):** An automated pneumatic launcher fires a glowing `#00E5FF` calibration capsule every 8 seconds across the 400m chord toward the ceiling city (`Valley B` at `60°`), tracing a visible **Coriolis S-curve "falling up"** before the player ever touches the manual Cross-Chord Tether Launcher (`Mechanic A`).
  - **Stage P5 (`Valley A` Promenade -> Flare Impact):** Full 3-verb synthesis on the Aft Ferry Umbilical (`bldg_14`) right as `interior_setpiece_03` spikes from `5500K` golden-hour daylight to `12,000K` coronal over-bloom with zero cutscenes or text boxes.

### Phase 8 Updates (7:02 PM CDT — Preface Service-Call Test Environment & 5-Candidate Embedded Wrist RFID Spec)
- **Authored `/workspace/game-project/design/preface_test_environment_and_wrist_spec.md` (`22 KB`) and synced `/workspace/game-project/design/vance_chapter1_solar_flare_environmental_states.md`:**
  - Replaced arbitrary "sparks throwing" opening with a grounded **Malfunctioning Bulkhead Door Service Call** inside the `10m × 8m × 4.2m` **Sector-4 Commuter Transit Vestibule (`preface_service_call_room.glb`)** alongside an **Assistant Droid (`char_assistant_droid.glb`)** and **two waiting civilian commuters (`char_citizen_commuter.glb`)**.
  - Designed the **3-Cycle Door Troubleshooting Loop** on `prop_service_door.glb` so the player practices raising their wrist to center screen 3 times inside the room without leaving (Cycle 1: `Leaf_A` opens, `Leaf_B` jams at `40%`; Cycle 2: Assistant Droid counterweight handshake + full test-open/test-close stroke; Cycle 3: final sign-off scan opens both leaves `2.20m` so the commuters wave thanks and walk out).
  - Specified **5 Distinct Candidates (`prop_wrist_rfid_r1_01..05.glb`)** for the **Embedded Subdermal Wrist RFID & Diegetic Cuff (`wrist_rfid_round1`)**, led by **Candidate `#02` — Aegis-7 "Induction Loom" (`68/32` asymmetric split-mass gyro-aperture cuff + subdermal dorsal vein-grid + `alphaMode: "BLEND"` sapphire diagnostic bridge)**.

### Phase 9 Updates (Oct 27, 7:10 AM CDT — Contiguous Multi-Floor Playable Preface Residential Sector, *Johnny 5* / *WALL-E* Bots & PCBA + Python Door UI)
- **Visually inspected** `/workspace/game-project/godot/renders/props/wrist_rfid/wrist_rfid_round1_voting_sheet.png` and `/workspace/game-project/godot/renders/preface/preface_test_environment_showcase_sheet.png` and logged Vance's vote in `/workspace/game-project/context/VOTE_LOG.md` (`33 / 33` votes logged), promoting Jared's locked winner **`#04 — Bio-Luminescent Neural Tendon Trace + Flexible Polymer Smart-Sleeve` (`prop_wrist_rfid_winner_01_neural_tendon_sleeve.glb`)**.
- **Authored `/workspace/game-project/design/preface_playable_residential_sector_spec.md` (`22 KB`):**
  1. **Locked `#04` Neural Tendon Sleeve + Upgrades:** Forearm dendritic veins act as diegetic **Battery Charges**, paired with the carpal **Super-Wire Spool (`prop_super_wire_spool.glb`)** (used for PCBA pin jumpers and grapple tethers) and the **BCI AI Headband (`prop_bci_headband.glb`)** on the apartment workbench.
  2. **Expressive *WALL-E* / *Johnny 5* Companion Robots (`char_bot_johnny5.glb` — Zero Star Wars Naming):** Twin rubberized caterpillar tracks, scissor neck, tilting binocular camera eyes with mechanical eyebrow shutters, twin 3-fingered grippers, and profession color palettes + nicknames/serial numbers (`"Sprocket #0419"` Maintenance Orange/Amber, `"Sweep #0812"` Janitorial Teal/White, `"Puddle #0204"` Hydro Cyan/Steel, `"Clover #0631"` Agri Emerald/White).
  3. **Contiguous Multi-Floor Residential Sector (`preface_residential_sector.glb` — `28m × 18m × 8.8m`):**
     - **Level 2 (`Y = +4.2m`):** Player's Top-Floor Apartment (`apt_player_top_floor`), Upper Mezzanine Gallery overlooking the two-story glass Atrium Lightwell, Neighbor Balcony Suite (`Room 2B`), and Upper Vent Cable Chase (`Alcove 2C`) with hidden Super-Wire (+5m) & Battery upgrades.
     - **Level 1 (`Y = 0.0m`):** Atrium switchback staircase down to the Ground-Floor Commuter Concourse, Laundry Lounge (`Room 1A`), Bot Charging Substation (`Room 1B`), bustling commuters, and the malfunctioning Sector-4 Exit Door.
  4. **Full-Screen 2-Stage Troubleshooting UI (PCBA "I Spy" + Readable Python Terminal):**
     - **Left Panel:** Dense PCBA circuit board where the player spots the silkscreen-labeled **`RESET`** pin on header `J4` (`GND`, `LOCK_HOLD`, `RESET`, `AUX_BUZZ`) and attaches the loose `#00E5FF` Super-Wire jumper lead.
     - **Right Panel:** Readable 8-line Python controller (`supply_amperage = 7` -> `if amperage > 10: return True`), where changing `7` to `12` (or `>` to `<`) returns `True` and slides the bulkhead door open into the city threshold.

### Phase 10 Updates (Oct 27, 7:18 AM CDT — Open-Doorway 2-Story Residential Building & 5-Candidate *WALL-E* / *Johnny 5* Robot Tournament)
- **Updated `/workspace/game-project/design/preface_playable_residential_sector_spec.md` (`8.1 KB`) & Authored `/workspace/game-project/design/utility_bot_johnny5_spec.md` (`9.9 KB`):**
  1. **Open-Doorway 2-Story Residential Building (NO Doors, NO Puzzle UI):**
     - Stripped out all blocking door leaves and held off on the PCBA/Python puzzle UI so the player can freely walk and wander through every room, hallway, balcony, and staircase of `preface_residential_sector.glb` (`APT 201` Top-Floor Player Apartment, `APT 202` Neighbor Balcony Suite, `Alcove 2C` Vent Chase, Open Atrium Staircase, `Room 1A` Laundry Lounge, `Room 1B` Bot Substation, and the Open Ground-Floor Concourse Threshold).
  2. **5-Candidate *WALL-E* × *Johnny 5* Utility Robot Tournament (`char_bot_johnny5_r1_01..05.glb`):**
     - `#01`: Compact Cube-Compactor Chassis + Twin Tilting Binocular Lens Hoods (*WALL-E* Heavy)
     - `#02`: **The "Johnny-V" — 68/32 Asymmetric Split-Mass Dual-Track Scissor-Spine + Expressive Eyebrow-Shutter Binocular Head & Twin 3-Finger Grippers (Flagship `#02`)**
     - `#03`: Wide-Stance Quad-Bogie Tracked Base + Telescoping Periscope Binoculars
     - `#04`: Rounded Industrial Roll-Cage Torso + Dual Servo-Flap Camera Visor
     - `#05`: Tri-Track Articulated Stair-Climber + Split Asymmetric Zoom/Wide Optical Eyes
     - Supported by 4 Profession Color Palettes & Stenciled Identities (`"Sprocket #0419"`, `"Sweep #0812"`, `"Puddle #0204"`, `"Clover #0631"`).

### Phase 11 Updates (Oct 27, 9:23 AM CDT — Utility Robot Round 2: `#03` Treads + `#01` Chassis + 5 Original Head Shape Explorations)
- **Visually inspected** `/workspace/game-project/godot/renders/characters/johnny5/johnny5_bot_round1_voting_sheet.png` and `/workspace/game-project/godot/renders/preface/preface_residential_sector_showcase_sheet.png` via `Read`.
- **Updated `/workspace/game-project/design/utility_bot_johnny5_spec.md` (`18 KB`, Section 5 — `utility_bot_round2`):**
  - Locked **Shared Lower + Mid Body** across all 5 Round 2 candidates (`char_bot_r2_01..05.glb`): **Lower Base = `#03` Wide-Stance Quad-Bogie Tracked Base** + **Mid Torso = `#01` Compact Cube-Compactor Chassis & Twin 3-Finger Grippers**.
  - Designed **5 Original Non-Clone Head Silhouettes (`#01`–`#05`)**:
    - `#01` (`char_bot_r2_01.glb`): **Articulated Split-Shutter "Camera-Bellows" Hood Head** (trapezoidal hood with asymmetric large/small apertures + horizontal clapperboard louver eyelids)
    - `#02` (`char_bot_r2_02.glb` — Flagship `#02`): **Dual-Ear Gimbal "CRT/Oscilloscope" Visor-Box Head** (chamfered dark-sapphire monitor visor displaying glowing vector iris rings + twin articulated side "ear" antenna paddles that perk/droop/tilt like dog ears)
    - `#03` (`char_bot_r2_03.glb`): **Tri-Faceted "Periscope Prism" Turret Head** (octagonal rotary turret with central cyclops dome + angled corner rangefinder slits & armored sun-visor brow)
    - `#04` (`char_bot_r2_04.glb`): **Split-Hemisphere "Clamshell Orb" Gimbal Head** (spherical sensor pod split horizontally into upper/lower clamshell jaws in a brushed-steel yoke gimbal)
    - `#05` (`char_bot_r2_05.glb`): **Cantilevered "Hammerhead" Wide-Baseline Stereo-Bar Head** (`0.48m` wide T-bar scanner with central laser slit, outer wingtip lenses, and pivoting wing-let shutters)

### Phase 12 Updates (Oct 27, 9:41 AM CDT — Post-Render Vote Logged for `utility_bot_round2`)
- **Visually inspected** `/workspace/game-project/godot/renders/characters/johnny5/utility_bot_round2_voting_sheet.png` via `Read` (all 5 head shape explorations on the locked `#03` Quad-Bogie Treads + `#01` Cube-Compactor Chassis, with tight head close-up insets).
- **Atomically logged Vance's post-render vote (`34 / 34` total votes logged)** in `/workspace/game-project/context/VOTE_LOG.md` for **`#02 — Curved "CRT/Oscilloscope" Visor-Box Head with Expressive Vector Eyes & Tilting Side Ear-Paddles` (`char_bot_r2_02.glb`, `4,832` tris)** (Runner-Up: `#01 — Articulated Split-Shutter "Camera-Bellows" Rangefinder Hood`, `char_bot_r2_01.glb`, `4,700` tris).

### Phase 13 Updates (Oct 27, 11:18 AM CDT — Locked `#05` Hammerhead Universal Cylinder Livery, Sparing `10–15%` Accents & 4 City District Emblems)
- **Updated `/workspace/game-project/design/utility_bot_johnny5_spec.md` (Section 6, `26 KB`) & `/workspace/game-project/design/city_district_zoning_and_emblems_spec.md` (`26 KB`):**
  1. **Universal Aegis-7 / Cylinder Hab-7 Municipal Base Livery (`85–90%` of Robot Surface):**
     - `55%` Matte Titanium Alabaster / Aerospace White (`#D8DEE4` / `#D8DEE6`) on the `#01` Cube-Compactor torso panels, `#05` Hammerhead stereo-bar cowling, forearm shields, and bogie skirts.
     - `20%` Anodized Deep Structural Slate / Gunmetal (`#2A3038` / `#1A1E24`) on the inner frame, neck gimbal spine, shoulder turrets, and bogie chassis.
     - `15%` Brushed Machined Steel (`#707A84` / `#88929E`) + Dark Vulcanized Tread Rubber (`#1E2228`) on the `#03` quad-bogie wheels, drive sprockets, pistons, and 3-finger claws.
  2. **Sparing Department Accent Trim (`10–15%` Max):** Restricted strictly to the Hammerhead wingtip brow flaps & roll-bar pinstripe (`3%`), compactor chest badge bezel & serial backing strip (`4%`), shoulder deltoid emblem pads (`3%`), bogie hubcap ring (`2%`), and scanner/equalizer tint (`2%`).
  3. **4 Department & City District Zoning Emblems (Stamped on Robot Chest/Shoulders + Used for City District Zoning):**
     - **District 01 (`D-01 // FORGE` — Maintenance `"Sprocket #0419"`, Safety Amber `#E89B2D`):** Hex-Gear & Crossed Spanner-Bolt emblem.
     - **District 02 (`D-02 // CIVIC HAB` — Civic & Janitorial `"Sweep #0812"`, Civic Cyan-Teal `#38B8C8`):** Orbital Ring-Arc & Compass Star emblem.
     - **District 03 (`D-03 // HYDRO-CRYO` — Hydro & Life Support `"Puddle #0204"`, Cryo-Cobalt `#2E78D2`):** Triple Wave & Cryo-Droplet Chevron emblem.
     - **District 04 (`D-04 // BIOSPHERE` — Agriculture `"Clover #0631"`, Biosphere Emerald `#3BA868`):** Hydroponic Trifolium Leaf-Hex & Axial Sun emblem.

### Phase 14 Updates (Oct 27, 11:35 AM CDT — Canonical 4-Department & City District Zoning Jurisdictions `[t74u]`)
- **Updated `/workspace/game-project/design/utility_bot_johnny5_spec.md` (Section 6) and `/workspace/game-project/design/city_district_zoning_and_emblems_spec.md` per Jared's `[t74u]` canonical 4-department division:**
  1. **`D-01 // ENGINEERING` (`"Sprocket #0419"`, Safety Amber `#E89B2D` `10–15%` accent):** Comms, plumbing, electricity, coolant, Aegis space systems, docking. Emblem: *The Hex-Gear, Crossed Spanner & Comms-Wave Bolt*.
  2. **`D-02 // CIVIC` (`"Sweep #0812"`, Civic Cyan-Teal `#38B8C8` `10–15%` accent):** Anything for commuters/citizens — life support, trash & sanitation, hospital & medical, government, recreation. Emblem: *The Orbital Ring-Arc, Medical Cross & Civic Star*.
  3. **`D-03 // SCIENCE` (`"Kelvin #0204"` / `"Vector #0309"`, Science Violet-Indigo `#7B5CFF` / `#5E68E8` `10–15%` accent):** Laboratories, experiments, new technology, space observations, astrometry. Emblem: *The Astrometric Atom-Lattice & Deep-Space Prism Star*.
  4. **`D-04 // AGRI` (`"Clover #0631"`, Biosphere Emerald `#3BA868` `10–15%` accent):** Food production (not preparation), biosphere, atmosphere, hydrosphere (hydro/water cycle), animals/pest control, veterinary. Emblem: *The Trifolium Leaf-Hex, Hydro-Wave & Axial Sun*.

