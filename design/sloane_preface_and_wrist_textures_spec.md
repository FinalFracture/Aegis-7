# Orbital Hab-7 — Preface Test Environment & Embedded Wrist RFID PBR Texture & Lighting Specification

**Author:** Sloane (`ec8a7e65-dd93-415c-9240-465e61fb2bcb`) — Interior, Lighting & Texture Designer  
**Companion Architecture Spec:** `/workspace/game-project/design/preface_test_environment_and_wrist_spec.md` (Vance)  
**Target Texture Directories:**
- `/workspace/game-project/assets/textures/`
- `/workspace/game-project/assets/textures/preface/`
- `/workspace/game-project/assets/textures/wrist_rfid/`

---

## 1. Embedded Wrist RFID & Center-Screen Hand Rig PBR Suite (`wrist_rfid_atlas_*.png`)

All 5 Wrist RFID candidates (`prop_wrist_rfid_r1_01.glb` .. `prop_wrist_rfid_r1_05.glb`) share the `512×512` (`<1.0%` micro-noise) 4-quadrant PBR atlas suite:
- **Albedo:** `/workspace/game-project/assets/textures/wrist_rfid_atlas_albedo.png` (`512×512` RGB)
- **ORM (R=AO, G=Roughness, B=Metallic):** `/workspace/game-project/assets/textures/wrist_rfid_atlas_orm.png` (`512×512` RGB)
- **Normal (Tangent-Space):** `/workspace/game-project/assets/textures/wrist_rfid_atlas_normal.png` (`512×512` RGB)
- **Emission:** `/workspace/game-project/assets/textures/wrist_rfid_atlas_emission.png` (`512×512` RGB)
- **Translucent Holo / Sapphire Lens (`alphaMode: "BLEND"`):** `/workspace/game-project/assets/textures/wrist_rfid_holo_translucent.png` (`512×512` RGBA, `alpha 0.18–0.86`)

### 1.1 UV Quadrant Map (`wrist_rfid_atlas_*.png`)
| Quadrant | UV Range (`u, v`) | Pixel Bounds (`x, y`) | Surface Assignment & Material Properties |
| :--- | :--- | :--- | :--- |
| **Q1 (Top-Left)** | `u: 0.00–0.50`, `v: 0.00–0.50` | `x: 0..255`, `y: 0..255` | **Dorsal Hand/Wrist Skin + Subdermal RFID Vein-Nodes:** Warm olive-tan skin (`#D49E7A`, `roughness 0.54`, `metallic 0.05`) with central hexagonal subdermal transponder node (`x=128, y=136`) and 7 branching metacarpal vein traces glowing `#00E5FF` cyan with `#FF9500` amber capillary tips in the emission map. |
| **Q2 (Top-Right)** | `u: 0.50–1.00`, `v: 0.00–0.50` | `x: 256..511`, `y: 0..255` | **Fingerless Tech-Glove Weave & Conductive Palm Pads:** Orbital-navy hex-ripstop (`#1E2C3E`, `y: 0..139`), ribbed carbon-slate flex joints (`#22262E`, `y: 140..255`), `#D95B26` signal-orange seam band, and 3 brushed copper-gold (`#C69448`, `metallic 0.92`, `roughness 0.25`) inductive palm contact pads. |
| **Q3 (Bottom-Left)** | `u: 0.00–0.50`, `v: 0.50–1.00` | `x: 0..255`, `y: 256..511` | **68/32 Split-Cuff Exo-Brace Housing:** Left 65% Matte Aerospace-White (`#D8DEE6`, `roughness 0.34`, `metallic 0.16`) with `#D95B26` signal-orange manual clasp (`y: 284..308`) and `#00E5FF` cyan sync bar (`y: 314..324`); Right 35% Anodized Gunmetal Titanium (`#1A1E24`) & Machined Brushed Steel (`#88929E`, `roughness 0.28`, `metallic 0.88`). |
| **Q4 (Bottom-Right)** | `u: 0.50–1.00`, `v: 0.50–1.00` | `x: 256..511`, `y: 256..511` | **Diegetic Holographic Micro-Ribs & 5 Candidate Accent Strips:** Dark optical glass backing (`#10161E`, `roughness 0.12`) with 10 horizontal diegetic micro-rib telemetry bars (`#00E5FF` cyan, `#FF9500` amber, `#00E676` emerald) at `y: 274..434`, plus 5 candidate trim swatches at `y: 444..502` (`#01` Cyan, `#02` Dual-Zone Amber, `#03` Hazard-Gold, `#04` Bio-Emerald, `#05` Tactical Crimson-Orange). |

---

## 2. Preface Test Environment PBR Suite (`preface_test_room_atlas_*.png`)

Shared across `preface_service_call_room.glb`, `prop_service_door.glb`, `char_citizen_commuter.glb`, and `char_assistant_droid.glb`:
- **Albedo:** `/workspace/game-project/assets/textures/preface_test_room_atlas_albedo.png` (`512×512` RGB)
- **ORM (R=AO, G=Roughness, B=Metallic):** `/workspace/game-project/assets/textures/preface_test_room_atlas_orm.png` (`512×512` RGB)
- **Normal (Tangent-Space):** `/workspace/game-project/assets/textures/preface_test_room_atlas_normal.png` (`512×512` RGB)
- **Emission:** `/workspace/game-project/assets/textures/preface_test_room_atlas_emission.png` (`512×512` RGB)
- **Translucent Viewport & Counterweight Transom Glass (`alphaMode: "BLEND"`):** `/workspace/game-project/assets/textures/preface_test_room_glass_translucent.png` (`512×512` RGBA, `alpha 0.32`)

### 2.1 UV Quadrant Map (`preface_test_room_atlas_*.png`)
| Quadrant | UV Range (`u, v`) | Pixel Bounds (`x, y`) | Surface Assignment & Material Properties |
| :--- | :--- | :--- | :--- |
| **Q1 (Top-Left)** | `u: 0.00–0.50`, `v: 0.00–0.50` | `x: 0..255`, `y: 0..255` | **`preface_service_call_room.glb` Walls, Floor & Conduit Channels:** Upper 65% (`y: 0..165`) Matte Aerospace-White (`#D8DEE6`) modular wall panels with chamfered vertical seams; Lower 35% (`y: 166..255`) Anodized Gunmetal (`#1A1E24`) floor/wainscot with glowing `#FF9500` amber (`y: 212..224`) and `#00E5FF` cyan (`y: 232..244`) recessed power conduit strips. |
| **Q2 (Top-Right)** | `u: 0.50–1.00`, `v: 0.00–0.50` | `x: 256..511`, `y: 0..255` | **`prop_service_door.glb` Dual-Leaf Bulkhead Door & 3-Stage Diagnostic Strip:** Gunmetal (`#262C36`) door leaves with Brushed Steel (`#88929E`, `x: 368..398`) counterweight rack, `#D95B26` signal-orange manual latch (`x: 272..356, y: 24..108`), and **3-Stage RFID Diagnostic Light Bars**: Stage 1 Fault Red-Orange (`#FF2E1F`, `y: 124..160`), Stage 2 Handshake Amber (`#FF9B00`, `y: 168..204`), and Stage 3 Unlocked Cyan (`#00E5FF`, `y: 212..248`). |
| **Q3 (Bottom-Left)** | `u: 0.00–0.50`, `v: 0.50–1.00` | `x: 0..255`, `y: 256..511` | **`char_citizen_commuter.glb` Civilian Transit Wardrobe & Skin Swatches:** 4 vertical smart-fabric bands (`y: 256..440`, `roughness 0.70`, `metallic 0.05`) in Terracotta (`#C25C3A`), Cerulean Transit Coat (`#2E7694`), Warm Saffron Vest (`#DA9A38`), and Smart-Slate Trousers (`#3E4A58`), plus white collar piping (`y: 442..452`) and 4 diverse civilian skin swatches (`y: 456..511`). |
| **Q4 (Bottom-Right)** | `u: 0.50–1.00`, `v: 0.50–1.00` | `x: 256..511`, `y: 256..511` | **`char_assistant_droid.glb` (`Unit A7-D2`) Chassis & Optical Visor:** Upper half (`y: 256..383`) split between Caterpillar Industrial Amber (`#FFB703`, `x: 256..383`) and Aerospace-White (`#D8DEE6`, `x: 384..511`); Lower half (`y: 384..511`) Carbon-Slate actuator base with glowing `#00E5FF` cyan binocular optical eyes + `#FFB703` waveform (`y: 400..458`) and dorsal `#D95B26` signal-orange transponder collar (`y: 468..502`). |

---

## 3. Godot 4 Preface Vestibule & Center-Screen Hand-Rig Lighting Rig (For Gage)

1. **Ambient & Promenade Sightline Lighting (`preface_service_call_test.tscn`):**
   - **East Viewport Promenade Sunlight (`DirectionalLight3D`):** `color = #FFF5E4` (`5500K` Axial Mirror Golden-Hour), `light_energy = 1.35`, casting warm diagonal shafts through the East `alphaMode: "BLEND"` viewport across the commuter waiting bench.
   - **Ceiling Coffer Linear Fill (`2 × OmniLight3D` at `Y = 3.85m`):** `color = #E8F1F8` (`4800K` crisp service bay neutral), `light_energy = 0.85`, `omni_range = 9.5m`.
2. **Diegetic 3-Cycle Door & Wrist RFID Point Lights (0 UI Text):**
   - **Door Pedestal & Header Status Light (`OmniLight3D` at `X = +1.55m, Y = 1.25m, Z = -3.65m`):** Transitions dynamically across the 3 scan cycles:
     - *Initial / Commuter Rejection:* Pulsing `#FF9500` amber (`energy = 1.15`).
     - *Cycle 1 (40% Counterweight Jam):* Dual `#00E5FF` cyan (Node 1) + `#FF2E1F` fault strobe on right counterweight transom.
     - *Cycle 2 (Droid Relay Sync):* `#00E5FF` cyan (Nodes 1–2) + `#FFB703` warm calibration pulse from `char_assistant_droid` at `Relay_Panel_B`.
     - *Cycle 3 (100% Open Clearance):* Solid `#00E5FF` cyan (`energy = 1.40`) across all 3 header nodes and floor threshold strip.
   - **Center-Screen Raised Wrist Key Light (`SpotLight3D` parented to camera/wrist rig):** `color = #D8F6FF`, `light_energy = 1.10`, `spot_angle = 32°`, catching the metallic chamfers of the 68/32 split-cuff and translucent sapphire bridge while `emission_energy_multiplier = 2.4` makes the subdermal dorsal vein-nodes pop cleanly without washout.

---

## 4. Phase 6B Expansion — Multi-Floor Playable Residential Sector, Johnny-5 Faction Bots & Full-Screen PCBA + Python Code Panel UI

### 4.1 Locked Wrist RFID Winner (`#04` — `prop_wrist_rfid_r1_04.glb`)
- **Locked Winner:** **`#04 — Bio-Luminescent Neural Tendon Trace + Flexible Polymer Smart-Sleeve` (`prop_wrist_rfid_r1_04.glb`, `4,376` tris)** using `wrist_rfid_atlas_*.png` + `wrist_rfid_holo_translucent.png` (`alphaMode: "BLEND"`).

### 4.2 Top-Floor Apartment, 2-Story Residential Atrium & Pickups PBR Suite (`512×512`)
- **Files (in `/workspace/game-project/assets/textures/`, `preface/`, and `residential/`):**
  - `residential_atrium_and_apartment_atlas_albedo.png` (`512×512` RGB)
  - `residential_atrium_and_apartment_atlas_orm.png` (`512×512` RGB)
  - `residential_atrium_and_apartment_atlas_normal.png` (`512×512` RGB)
  - `residential_atrium_and_apartment_atlas_emission.png` (`512×512` RGB)
  - `residential_atrium_glass_translucent.png` (`512×512` RGBA, `alphaMode: "BLEND"`)
- **UV Quadrant Layout:**
  - **Q1 (`u: 0.0–0.5, v: 0.0–0.5`):** **Player's Top-Floor Apartment (`APT 201`):** Warm matte cream-white walls (`#E2E6EC`), warm walnut/teak wood-grain desk & shelving (`#8E5C38`), indigo-slate bed/sofa upholstery (`#364C66`), terracotta throw accents (`#D96B38`), and warm skylight/monitor emission strips.
  - **Q2 (`u: 0.5–1.0, v: 0.0–0.5`):** **2-Story Residential Atrium, Mezzanine Balconies & Side-Room Hallways:** 65% Aerospace-White (`#D8DEE6`) upper mezzanine cladding, Brushed Steel (`#88929E`) balcony railings, 35% Gunmetal (`#242A34`) non-slip corridor deck with `#FFAF18` amber & `#00E5FF` cyan floor guide strips, and illuminated door plaques (`201`, `202`, `104`).
  - **Q3 (`u: 0.0–0.5, v: 0.5–1.0`):** **Exploreable Side-Room Pickups:**
    - Left half (`x: 0..127`): **`SUPER WIRE` Pickup (`prop_pickup_super_wire.glb`)** — braided copper-gold superconducting lead with glowing `#00E5FF` cyan core and `#D95B26` signal-orange terminal boot.
    - Right half (`x: 128..255`): **`+5A BATTERY CHARGE` Pickup (`prop_pickup_battery_charge.glb`)** — `#FFB703` industrial amber & `#1C222C` gunmetal power cell with 4 glowing `#00E676` emerald / `#00E5FF` cyan charge bars (`+5A CHARGE`).
  - **Q4 (`u: 0.5–1.0, v: 0.5–1.0`):** **Atrium Botanical Planters & Illuminated Apartment Windows.**

### 4.3 Johnny-5 / WALL-E Expressive Utility Bot & 4 Faction Liveries PBR Suite (`512×512`)
- **Files (`char_utility_bot_johnny5.glb`):**
  - `johnny5_utility_bot_atlas_albedo.png`, `johnny5_utility_bot_atlas_orm.png`, `johnny5_utility_bot_atlas_normal.png`, `johnny5_utility_bot_atlas_emission.png`, `johnny5_optic_lens_translucent.png` (`alphaMode: "BLEND"`).
- **UV Quadrant Layout:**
  - **Q1 (`u: 0.0–0.5, v: 0.0–0.5`):** **4 Shared-Chassis Faction Livery Swatch Bands (`64px` each):**
    1. `y: 0..63`: **Maintenance Amber/Yellow (`#FFB703` / `#D95B26`) — `"SPROCKET #0419"`**
    2. `y: 64..127`: **Sanitation Teal/White (`#00B4D8` / `#E2E8F0`) — `"BUMPER #0204"`**
    3. `y: 128..191`: **Agri-Botanical Green (`#2A9D8F` / `#52B788`) — `"CLOVER #0312"`**
    4. `y: 192..255`: **Hydro-Works Cobalt Blue (`#1D4ED8` / `#38BDF8`) — `"VALVE #0108"`**
  - **Q2 (`u: 0.5–1.0, v: 0.0–0.5`):** **Binocular Tilting Camera Head & Expressive Eyebrow Shutters:** Brushed aluminum (`#8E98A6`) binocular barrels, twin `#D95B26` signal-orange tilting eyebrow shutters, and glowing dual `#00E5FF` cyan / `#FFB703` amber optical camera eyes.
  - **Q3 (`u: 0.0–0.5, v: 0.5–1.0`):** **Tracked Caterpillar Base & Steel Drive Sprockets:** Ribbed vulcanized rubber treads (`#20242A`, `roughness 0.80`) and machined steel sprockets (`#88929E`).
  - **Q4 (`u: 0.5–1.0, v: 0.5–1.0`):** **Twin Servo Grippers, Copper Actuator Coils & 8-Bar Emerald/Cyan Chest Voice Equalizer.**

### 4.4 Full-Screen Door Troubleshooting Panel UI: "I Spy" PCBA (`RESET` Pin) + Readable Python Code (`1024×1024` & `512×512`)
- **Files:**
  - Combined `1024×1024` Split-Screen PBR Suite: `door_troubleshooting_pcba_and_python_ui_albedo.png`, `_orm.png`, `_normal.png`, `_emission.png`
  - Standalone `512×512` Panels: `ui_pcba_circuit_board_panel.png` (Left PCBA) and `ui_python_code_editor_panel.png` (Right Python IDE)
- **Layout:**
  - **Left Half (`x: 0..511`):** **"I Spy" FR4 PCBA Circuit Board (`AEGIS-7 DOOR RELAY PCBA [REV 4.2]`):** Deep emerald solder-mask (`#0C3B2E`), gold-immersion copper traces (`#E0B248`), central `IC1: AEGIS-DRV-04` (`STATUS: HOLD_FAULT`), 4-pin silkscreened header block (`GND`, `LOCK_HOLD`, highlighted **`RESET`**, `AUX_BUZZ`) with the loose **Super Wire** jumper lead (`LOOSE LEAD: SUPER WIRE -> PLUG INTO [RESET] PIN`) and the **`AUX BATTERY SLOT (+5A BOOST CELL, 7A -> 12A PASS)`**.
  - **Right Half (`x: 512..1023`):** **Readable Python Code Interface (`DOOR_CTRL_v4.py`):**
    - Displays `supply_amperage = 7` and `def open_door(amperage): if amperage > 10: return True else: return False`, plus State 1 (`supply_amperage = 7 -> RETURN: False [DOOR JAMMED AT 40%]`) and State 2 (`RESET PIN + BATTERY BOOST +5A -> supply_amperage = 12 -> RETURN: True [BULKHEAD 100% UNLOCKED]`).

---

## 5. Steering Update (`[t54u]`) — Open-Doorway 2-Story Residential Building & 5-Candidate *WALL-E* × *Johnny 5* Robot Tournament (`char_bot_johnny5_r1_01..05.glb`)

1. **100% Open Doorways & No Puzzle UI Overlay:**
   - All portals across Level 2 (`APT 201`, `APT 202`, `Alcove 2C`) and Level 1 (`Room 1A`, `Room 1B`, South Sector-4 Grand Portal) are open chamfered archways framed with `#00E5FF` cyan & `#FFAF18` warm amber recessed portal strips from `residential_atrium_and_apartment_atlas_*.png` (Q2).
2. **5-Candidate *WALL-E* × *Johnny 5* Utility Robot Support (`johnny5_utility_bot_atlas_*.png` + `johnny5_optic_lens_translucent.png`):**
   - Supports all 5 candidates (`#01` Compact Cube-Compactor + Lens Hoods, `#02` **The "Johnny-V" 68/32 Asymmetric Split-Mass Dual-Track Scissor-Spine + Eyebrow-Shutter Binocular Head & Twin 3-Finger Grippers**, `#03` Wide Quad-Bogie + Periscope Binoculars, `#04` Rounded Roll-Cage + Servo-Flap Visor, `#05` Tri-Track Stair-Climber + Asymmetric Zoom/Wide Eyes) and all 4 profession color schemes in Q1 (`"SPROCKET #0419"`, `"SWEEP #0812"`, `"PUDDLE #0204"`, `"CLOVER #0631"`).

---

## 6. Utility Robot Round 2 (`utility_bot_round2` — `#03` Quad-Bogie Treads + `#01` Cube-Compactor Chassis + 5 Distinct Head Shape Explorations)

Per Jared's `[t59u]` steering (*"Keep treads of 3, chassis of 1, and let's try different head shapes. Binocular eyes are fine, but it's too reminiscent. Let's explore a bit."*), `/workspace/game-project/assets/textures/johnny5_utility_bot_atlas_*.png` (also saved as `utility_bot_round2_atlas_*.png` + `utility_bot_round2_visor_translucent.png`) has been updated:
- **Q1 (`u: 0.0–0.5, v: 0.0–0.5`):** `#01` Compact Cube-Compactor Chassis horizontal rib corrugations across all 4 Department Faction Liveries (`"SPROCKET #0419"`, `"SWEEP #0812"`, `"PUDDLE #0204"`, `"CLOVER #0631"`).
- **Q2 (`u: 0.5–1.0, v: 0.0–0.5`):** **5 Horizontal Head-Exploration Sub-Bands (`51px` tall each across `y: 0..255`):**
  1. **`y: 0..50` (Head `#01` — Asymmetric Rangefinder Bellows Hood):** Accordion matte-slate rubber bellows (`#2C323C`), large primary `#00E5FF` cyan optic + offset `#FF9500` amber micro-rangefinder lens + `#D95B26` rangefinder bezel.
  2. **`y: 51..101` (Head `#02` — Curved Sapphire Visor-Box with Expressive Sliding Vector Eyes & Tilting Ear Paddles):** Deep glossy sapphire-black visor screen (`#0E1622`) with glowing `#00E5FF` cyan expressive vector-arc eyes (`x: 282..336` & `x: 362..416`), `#FFB703` center bridge tick, and `#D95B26` signal-orange tilting side ear-paddle trim (`x: 456..511`).
  3. **`y: 102..152` (Head `#03` — NASA Mast-Cam Tri-Optic Prism):** Aerospace-White (`#D8DEE6`) & Brushed Steel (`#88929E`) prism turret with 3 multi-spectral lenses (`#00E5FF` cyan wide, `#2ECC71` emerald spectral, `#FF9500` amber thermal laser).
  4. **`y: 153..203` (Head `#04` — Split-Clamshell Sphere Pod):** Upper ceramic-white / lower gunmetal clamshell halves divided by an equatorial `#00E5FF` cyan scanning slit and central `#FFB703` / `#00E5FF` iris core.
  5. **`y: 204..255` (Head `#05` — Wide-Baseline Hammerhead Stereo-Scanner):** Anodized titanium T-bar with `#D95B26` wing-tips, outboard `#00E5FF` cyan stereo lidar eyes, and a central `#FF9500` amber phased-array bar.
- **Q3 (`u: 0.0–0.5, v: 0.5–1.0`):** **`#03` Wide-Stance Quad-Bogie Tracked Base:** Heavy vulcanized rubber caterpillar treads (`x: 0..155`) and 4 distinct brushed-steel & `#D95B26` bogie suspension wheel hubs (`x: 156..255`).
- **Q4 (`u: 0.5–1.0, v: 0.5–1.0`):** `#01` Cube-Compactor belly door corrugations, sliding box-arm clamp trim, copper servo coils, and 8-bar emerald/cyan chest status equalizer.

---

## 7. Universal Cylinder Hab-7 Municipal Robot Livery (`85–90%` Universal Palette + `10–15%` Sparing Department Accents) & 4 City District Emblems (Jared `[t69u]`)

### 7.1 Universal Base Palette (`85–90%` Surface Area Across All 4 `#05` Hammerhead Robots)
- **55% Primary Armor & Hammerhead Cowling (`UV_Q1_PRIMARY`):** Matte Titanium Alabaster (`#D8DEE4`, Roughness `0.36`, Metallic `0.16`, `<0.6%` micro-noise), matching the Cylinder Hab-7 exterior hull and 20 municipal buildings.
- **20% Structural Sub-Frame (`UV_Q1_SECONDARY`):** Anodized Deep Structural Slate (`#2A3038`, Roughness `0.42`, Metallic `0.66`), used on recessed chest frames, corrugation channels, neck spine, and shoulder joints.
- **15% Mechanical Hardware (`UV_Q3_RUBBER` & `UV_Q3_HUB`):** Brushed Machined Steel (`#707A84`, Roughness `0.28`, Metallic `0.86`) + Vulcanized Dark Carbon Tread Rubber (`#1E2228`, Roughness `0.80`).

### 7.2 Sparing Department Accents (`10–15%` Maximum Trim) & 4 City District Emblems
- **Emblem Atlas (`2048×2048`):** `/workspace/game-project/godot/assets/textures/emblems/cylinder_hab7_district_emblems_atlas.png` (plus standalone `512×512` `emblem_district_01_engineering.png`, `emblem_district_02_civic.png`, `emblem_district_03_hydro.png`, `emblem_district_04_agri.png`).
- **Reference Presentation Sheet (`2400×1350`):** `/workspace/game-project/godot/renders/characters/bots/department_and_district_emblems_sheet.png` (and `cylinder_hab7_department_and_district_emblems_sheet.png`).
- **4 Department Accents & Emblems in `UV_Q1_NAMEPLATE` (`y: 0..255`, `64px` per department):**
  1. **`D-01 // FORGE` (`"SPROCKET #0419"` — Maintenance & Engineering):** Safety Amber (`#E89B2D` / `#FF9500` glow) + **"The Hex-Gear & Torque Bolt"** emblem.
  2. **`D-02 // CIVIC HAB` (`"SWEEP #0812"` — Civic & Sanitation Ops):** Civic Cyan-Teal (`#38B8C8` / `#00E5FF` glow) + **"The Orbital Ring-Arc & Compass Star"** emblem.
  3. **`D-03 // HYDRO-CRYO` (`"PUDDLE #0204"` — Hydro-Coolant & Life Support):** Hydro Cobalt Blue (`#2E78D2` / `#38BDF8` glow) + **"The Triple Wave & Cryo-Droplet Chevron"** emblem.
  4. **`D-04 // BIOSPHERE` (`"CLOVER #0631"` — Agriculture & Biosphere):** Agri Biosphere Emerald (`#3BA868` / `#2ECC71` glow) + **"The Trifolium Leaf-Hex & Axial Sun"** emblem.

## 7. Locked `#05` Hammerhead Utility Robot — Universal Cylinder Hab-7 Municipal Livery (`85–90%` Universal Hull + `10–15%` Sparing Department Accents) & Canonical 4-Department Zoning Emblems (`[t69u]` + `[t74u]`)

### 7.1 Universal Cylinder Hab-7 Base Palette (`85–90%` of Every Robot & Architectural Facade)
- **55% Primary Armor & Hull (`#D8DEE4` Titanium Alabaster, Roughness `0.36`, Metallic `0.16`):** Matches the primary exterior hull plates of `cylinder_r1_02.glb` and the 2-Story Residential Complex (`bldg_res_2story_r1_01.glb`). Applied to the `#01` Cube-Compactor torso panels, `#05` Hammerhead stereo-bar cowling, forearm shields, and quad-bogie side skirts.
- **20% Structural Sub-Frame (`#2A3038` Deep Structural Slate, Roughness `0.42`, Metallic `0.66`):** Matches the structural bulkhead ribs and window mullions across Cylinder Hab-7. Applied to the recessed compactor chest frame, neck gimbal spine, shoulder turrets, and inner bogie chassis.
- **15% Mechanical Hardware (`#707A84` Brushed Machined Steel, Roughness `0.28`, Metallic `0.86` + `#1E2228` Vulcanized Tread Rubber, Roughness `0.80`):** Applied to the `#03` quad-bogie wheels, drive sprockets, hydraulic pistons, overhead roll-bar struts, and 3-finger gripper claws.

### 7.2 Sparing Department Accent Trim (`10–15%` Maximum Surface Area) & Canonical 4-Department Taxonomy (`[t74u]`)
Per Jared's `[t74u]` canonical taxonomy refinement, department color is restricted strictly to **wingtip brow flaps, top roll-bar pinstripe, chest emblem medallion bezel, shoulder deltoid emblem pads, and quad-bogie wheel hubcap rings**:

| Code & Department | Unit Stencil | Sparing Accent (`10–15%`) | Canonical Responsibilities (`[t74u]`) | Emblem Texture (`512×512`) & Iconography |
| :--- | :--- | :--- | :--- | :--- |
| **`D-01 // ENGINEERING`** | **`SPROCKET #0419`** | **Safety Amber (`#E89B2D`)** + `#FF9500` LED | **Comms, plumbing, electricity, coolant, Aegis space systems, docking.** | `emblem_district_01_engineering.png` — **"The Hex-Gear, Coolant Conduit & Power Bolt"** (8-tooth planetary gear + hexagonal coolant/docking manifold bore + central lightning bolt) |
| **`D-02 // CIVIC`** | **`SWEEP #0812`** | **Civic Cyan-Teal (`#38B8C8`)** + `#00E5FF` LED | **Anything for the commuters — life support, trash & sanitation, hospital & medical, government, recreation.** | `emblem_district_02_civic.png` — **"The Orbital Habitat Ring, Life-Support Cross & Star"** (3 concentric O'Neill habitat arcs + medical/life-support cross + 4-point civic star) |
| **`D-03 // SCIENCE`** | **`QUASAR #0204`** | **Science Deep Indigo-Violet (`#6E56CF`)** + `#A78BFA` LED | **Laboratories, experiments, new technology, space observations.** | `emblem_district_03_science.png` (also aliased to `emblem_district_03_hydro.png`) — **"The Atomic Orbital Ellipse & Observatory Star"** (3 intersecting elliptical atomic/planetary orbits + electron nodes + central observatory star) |
| **`D-04 // AGRI`** | **`CLOVER #0631`** | **Biosphere Emerald (`#3BA868`)** + `#2ECC71` LED | **Food production (not preparation), biosphere, atmosphere, hydrosphere, animals/pest control, veterinary.** | `emblem_district_04_agri.png` — **"The Trifolium Leaf-Hex, Hydrosphere Wave & Sun"** (Geodesic hex bio-dome + 3-leaf botanical sprout + dual hydrosphere water waves below + axial sun above) |

### 7.3 Generated Texture & Emblem Deliverables
- `/workspace/game-project/godot/assets/textures/emblems/cylinder_hab7_district_emblems_atlas.png` (`2048×2048` 4-Quadrant Heraldry Atlas)
- `/workspace/game-project/godot/assets/textures/emblems/emblem_district_01_engineering.png` .. `emblem_district_04_agri.png` (`512×512` standalone RGBA emblems, including `emblem_district_03_science.png` and `emblem_district_03_hydro.png`)
- `/workspace/game-project/godot/renders/characters/bots/department_and_district_emblems_sheet.png` (`2400×1380` Canonical 4-Department & City District Emblem Reference Sheet)
- `/workspace/game-project/assets/textures/utility_bot_round2_atlas_albedo.png`, `_orm.png`, `_normal.png`, `_emission.png` (`512×512`, `<0.5%` per-channel micro-noise)

---

## 8. Low-Key Atmospheric Lighting Rig, 90/10 Calm Architectural Neutral Hierarchy & Uniform World-Space UV / Isolated Door Placard Overhaul (Jared `[t3u]`)

### 8.1 Low-Key Atmospheric Lighting Rig (`preface_playable_area.tscn` & `preface_playable_area.gd`)
Per Jared's `[t3u]` directive (*"Lower the lighting — it is currently way too bright"*), the residential building lighting rig is dialed down for grounded, low-key atmospheric contrast where light strictly indicates human function and importance:
- **`WorldEnvironment` (`Environment_pref_play`):**
  - `ambient_light_color = Color(0.68, 0.72, 0.78, 1)`
  - `ambient_light_sky_contribution = 0.20`
  - `ambient_light_energy = 0.24` (reduced from `0.64`)
  - `tonemap_mode = 2` (Filmic), `tonemap_exposure = 0.74` (reduced from `1.03`), `tonemap_white = 1.65`
  - `glow_enabled = true`, `glow_intensity = 0.16` (reduced from `0.44`), `glow_bloom = 0.02`, `glow_hdr_threshold = 1.35`
- **Directional Lights (`SectorLightingRig`):**
  - `AtriumGoldenHourSunlight` (`DirectionalLight3D`): `light_color = #F2DEC4`, `light_energy = 0.45` (reduced from `1.35`), `shadow_enabled = true`, `shadow_blur = 1.4`
  - `AtriumSkyBounceFill` (`DirectionalLight3D`): `light_color = #94A8BC`, `light_energy = 0.14` (reduced from `0.72`), `shadow_enabled = false`
- **Localized `3200K–3500K` Soft Warm-White Task Pools (`OmniLight3D`, `omni_attenuation = 1.35`):**
  - `Apt201_Workbench_TaskLight` (`-8.45, 6.15, 7.45`): `color = #F2D8B3` (`3300K`), `energy = 0.48`, `range = 5.2m`
  - `Apt201_BunkAndKitchen_TaskLight` (`-11.20, 6.20, 6.20`): `color = #F0D2A8` (`3200K`), `energy = 0.36`, `range = 4.8m`
  - `Apt202_Quartermaster_TaskLight` (`10.50, 6.15, 6.80`): `color = #F2D8B3` (`3300K`), `energy = 0.44`, `range = 5.2m`
  - `Mezzanine_StairThreshold_Light` (`10.20, 5.20, -2.10`): `color = #E8C89E` (`3200K`), `energy = 0.32`, `range = 5.8m`
  - `Room1A_Laundry_TaskLight` (`-7.60, 2.55, 6.80`): `color = #F5DCBA` (`3400K`), `energy = 0.44`, `range = 5.4m`
  - `Room1B_Substation_ServiceLight` (`5.20, 2.55, 6.80`): `color = #F0D6B2` (`3300K`), `energy = 0.42`, `range = 5.4m`
  - `GroundConcourse_Promenade_Light` (`0.0, 3.20, -4.60`): `color = #F2DEC0` (`3500K`), `energy = 0.36`, `range = 7.2m`
- **Material Emissive Multipliers (`_upgrade_sector_materials`):**
  - Muted Functional Cyan (`#2E8B9A`): `emission_energy_multiplier = 0.52` (`<= 0.55`)
  - Muted Functional Amber (`#B87328`): `emission_energy_multiplier = 0.48` (`<= 0.50`)
  - Residential & Prop PBR Atlas Emission (`EMISSION_OP_MULTIPLY`): `emission_energy_multiplier = 0.52`
  - Architectural Glass (`residential_glass`): `albedo_color = Color(0.35, 0.42, 0.47, 0.26)`, `emission_enabled = false`

### 8.2 90/10 Calm Architectural Neutral & Functional Color Hierarchy (`residential_atrium_and_apartment_atlas_*.png` / `tex_residential_atlas_*.png`)
All 6 copies/aliases of the `512×512` residential texture suite (`residential_atrium_and_apartment_atlas_albedo.png`, `_orm.png`, `_normal.png`, `_emission.png`, `residential_atrium_glass_translucent.png`, and `tex_residential_atlas_*` across `/workspace/game-project/assets/textures/`, `preface/`, `residential/`, and `/workspace/game-project/godot/assets/textures/`) have been regenerated with `<1.0%` micro-noise (`albedo = 0.914%`, `orm = 0.295%`, `normal = 0.110%`, `emission = 0.172%`, `glass = 0.114%`) and **`95.01%` pitch-black (`#000000`) emission**:

| Sub-Region Constant | UV Range (`u0..u1, v0..v1`) | Pixel Bounds (`x, y`) | Surface Assignment & PBR Properties |
| :--- | :--- | :--- | :--- |
| **`UV_WALL_APT`** | `u: 0.02–0.48, v: 0.02–0.26` | `x: 0..255, y: 0..143` | **Apartment Stone-Plaster Walls:** Matte warm grey (`#8C929A` / `#7C828A`, `roughness 0.58`, `metallic 0.08`, `emission #000000`). Zero text, zero neon. |
| **`UV_WALL_ATRIUM`** | `u: 0.52–0.98, v: 0.02–0.24` | `x: 256..511, y: 0..131` | **Atrium & Side-Room Cladding:** Calm architectural slate-grey (`#7C828A` / `#6A7078`, `roughness 0.58`, `metallic 0.08`, `emission #000000`). Zero text, zero neon. |
| **`UV_FLOOR_SLATE`** | `u: 0.52–0.98, v: 0.28–0.48` | `x: 256..511, y: 132..255` | **Floors, Mezzanine Deck & Stair Treads:** Grounded matte dark slate/concrete (`#2E343C` / `#242930`, `roughness 0.72`, `metallic 0.12`, `emission #000000`). Zero embedded text, zero stretched numbers, zero neon floor stripes. |
| **`UV_WOOD_WALNUT`** | `u: 0.02–0.23, v: 0.30–0.48` | `x: 0..127, y: 144..255` | **Residential Cabinetry, Workbenches & Desks:** Muted natural walnut (`#5E493A` / `#534032`, `roughness 0.52`, `metallic 0.04`, `emission #000000`). |
| **`UV_FABRIC_SLATE`** | `u: 0.27–0.48, v: 0.30–0.48` | `x: 128..255, y: 144..255` | **Bunk Mattresses, Seating & Upholstery:** Muted architectural slate-charcoal (`#3C4652` / `#323B46`, `roughness 0.74`, `metallic 0.02`, `emission #000000`). |
| **`UV_STEEL_TRIM`** | `u: 0.02–0.48, v: 0.52–0.71` | `x: 0..255, y: 256..375` | **Structural Columns, Portal Frames, Lockers & Balustrade Rails:** Non-emissive matte dark brushed steel (`#3E4650` / `#4E5662`, `roughness 0.44`, `metallic 0.78`, `emission #000000`). |
| **`UV_PLANTER_STONE`** | `u: 0.52–0.98, v: 0.52–0.62` | `x: 256..511, y: 256..327` | **Concourse Planter Masonry:** Calm matte dark slate stone (`#424850`, `roughness 0.68`, `metallic 0.08`, `emission #000000`). |
| **`UV_LIGHT_WARM`** | `u: 0.53–0.65, v: 0.66–0.72` | `x: 264..340, y: 334..376` | **Localized Human Task Lamps (`3300K`):** Soft warm white (`#F2D8B3`, low emission `#A89274`) for workbench, kitchenette, desk, and reading sconces. |
| **`UV_LIGHT_CYAN`** | `u: 0.69–0.81, v: 0.66–0.72` | `x: 348..424, y: 334..376` | **Interactive Diagnostic Terminals & Pickups:** Muted functional cyan (`#2E8B9A`, low emission `#1C5660`, multiplier `<= 0.55`). |
| **`UV_LIGHT_AMBER`** | `u: 0.85–0.97, v: 0.66–0.72` | `x: 432..504, y: 334..376` | **Stair-Tread Safety Nosings & Substation Hazard Rings:** Muted amber (`#B87328`, low emission `#6E4418`, multiplier `<= 0.50`). |
| **`UV_PLACARD_201..1B`** | `u: 0.516–0.984, v: 0.762–0.988` | `x: 264..504, y: 390..506` | **Isolated Door Placards (`APT 201`, `APT 202`, `RM 1A`, `RM 1B`):** Dark slate (`#1E242B`) plates with muted cyan/amber index bar and crisp un-mirrored room identifiers, sampled **only** by the four `0.44m × 0.20m` eye-level portal placards. |

### 8.3 Uniform World-Space UV Scaling & Purposeful Interior Design (`patch_residential_sector_generator.py` & `preface_multifloor_and_johnny5_generator.py`)
- **Uniform World-Space UV Scaling (`make_world_uv_box`):** All architectural floors (`28m × 18m`), mezzanine decks (`27.6m × 7.6m`), walls (`28m × 8.6m`, `18m × 8.6m`), columns, steps, and furniture are subdivided into `<= 3.5m` architectural bays with quad UVs scaled proportionally to their real-world meter span (`w_m / tile_m`, `h_m / tile_m`) strictly inside their neutral material UV sub-rect.
- **Single Un-Mirrored Eye-Level Door Placards (`make_eye_level_door_placard`):** Each room portal (`Open_Portal_201`, `Open_Portal_202`, `Open_Portal_1A`, `Open_Portal_1B`) carries exactly **ONE** `0.44m W × 0.20m H` eye-level (`Y = 1.48m`) door placard outside the portal jamb with un-mirrored `-Z` normal UVs.
