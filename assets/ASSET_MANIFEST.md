# 3D Asset & PBR Material Manifest — Project *Cylinder Hab-7* ("Aegis-7 Standard" Hard Sci-Fi)

**Owner:** Rook (3D Modeling Specialist — `11c68e8e-c070-4e83-a926-21e9dfb70523`)  
**Target Engine:** Godot 4 (`1.0 unit = 1.0 meter`, `-Z` Forward, `+Y` Up, Bottom-Center `Y = 0.000m` pivots)  
**Active Tests:**
- Room 02 Hero Fixture: Pressurized Bulkhead Airlock Hatch & Sector Checkpoint (`corridor_door_r1_01.glb` – `corridor_door_r1_05.glb`)
- Room 03 Hero Asset: Ration & Beverage Synthesizer Bank (`galley_synth_r1_01.glb` – `galley_synth_r1_05.glb`) + Companion `mess_dining_booth.glb`
- Room 04 Hero Asset: Surgical Autodoc Gantry & Triage Console (`med_autodoc_r1_01.glb` – `med_autodoc_r1_05.glb`)

---

## 1. Room 03 Hero Asset — Ration & Beverage Synthesizer Bank (`/workspace/game-project/assets/glb/galley_round1/`)

All 5 Ration & Beverage Synthesizer Bank candidates (`galley_synth_r1_01.glb` – `galley_synth_r1_05.glb`) are built at `4,258–5,386` triangles (`min Y = 0.0000m`, centered X/Z, front facing `+Z`, mapped to Sloane's 10 textures in `/workspace/game-project/assets/textures/galley_round1/`):

| # | Asset File | Hard Sci-Fi Galley Synthesizer Archetype Title | Bounding Box (W × D × H m) | Min Y (m) | Vertices | Triangles | Translucent Glass & Features | Beauty Render | Status |
| :- | :--- | :--- | :--- | :--- | ---: | ---: | :--- | :--- | :--- |
| `01` | `galley_synth_r1_01.glb` | **#01 — Aegis-7 Octagonal Bulkhead Ration Synthesizer & Beverage Bar** | `1.92 × 0.80 × 2.10` | `0.0000` | 6,468 | **4,594** | Twin `glass_synth_chamber_translucent.png` (`BLEND`) thermal synthesis ovens with 3D meal trays + Left beverage tap & flasks + Top aeroponic herb bay | `galley_synth_r1_01.png` | Validated |
| `02` | `galley_synth_r1_02.glb` | **#02 — Dual-Zone Split Thermal Synthesizer & Translucent Ration/Herb Tower** | `2.01 × 0.82 × 2.12` | `0.0000` | 7,492 | **5,386** | 65/35 Split sibling to Locked Winners • Left tap arch, flasks, OLED & ovens + Right full-height 3-tier translucent canister & herb tower (`BLEND`) | `galley_synth_r1_02.png` | Validated |
| `03` | `galley_synth_r1_03.glb` | **#03 — Rotary Carousel Automaton Dispenser & Espresso Tap Alcove** | `1.90 × 0.84 × 2.10` | `0.0000` | 6,160 | **4,510** | Central 3-tier rotary ration carousel behind translucent window + Left high-pressure espresso tap + Right ordering OLED & herb strip | `galley_synth_r1_03.png` | Validated |
| `04` | `galley_synth_r1_04.glb` | **#04 — Cantilevered Island Galley Module & Overhead Nutrient Manifold** | `1.97 × 0.82 × 2.12` | `0.0000` | 5,832 | **4,258** | Cantilevered serving counter on heavy titanium pillars + Overhead nutrient feed canisters & herb trough + Eye-level translucent ovens | `galley_synth_r1_04.png` | Validated |
| `05` | `galley_synth_r1_05.glb` | **#05 — Heavy Crew Mess Quad-Chamber Induction Synthesizer & Tray Return** | `2.07 × 0.82 × 2.12` | `0.0000` | 6,347 | **4,554** | 2×2 quad-grid of translucent induction synthesis chambers (`BLEND`) + Dual central hydration taps + Upper aeroponic herb trough | `galley_synth_r1_05.png` | Validated |
| — | `mess_dining_booth.glb` | **Custom Companion Mess Booth & Cantilevered Table** (`rooms/` & `galley_round1/`) | `1.84 × 2.04 × 0.94` | `0.0000` | 3,668 | **2,714** | Cantilevered steel/white table with 4 meal trays, magnetic mugs, cyan tray borders, translucent center shield (`BLEND`) & twin navy/charcoal booths | — | Validated |

---

## 2. Room 04 Hero Asset — Surgical Autodoc Gantry & Triage Console (`/workspace/game-project/assets/glb/medbay_round1/`)

All 5 Surgical Autodoc Gantry & Triage Console candidates (`med_autodoc_r1_01.glb` – `med_autodoc_r1_05.glb`) are built at `3,670–4,396` triangles (`min Y = 0.0000m`, centered X/Z, front facing `+Z`, mapped to Sloane's 9 textures in `/workspace/game-project/assets/textures/medbay_round1/`):

| # | Asset File | Hard Sci-Fi Surgical Autodoc Archetype Title | Bounding Box (W × D × H m) | Min Y (m) | Vertices | Triangles | Translucent Glass & Features | Beauty Render | Status |
| :- | :--- | :--- | :--- | :--- | ---: | ---: | :--- | :--- | :--- |
| `01` | `med_autodoc_r1_01.glb` | **#01 — Aegis-7 Octagonal Bulkhead Surgical Autodoc & Ring Scanner** | `2.18 × 1.25 × 2.12` | `0.0000` | 4,846 | **3,926** | Translating octagonal MRI/CT scanner ring + Twin articulated robotic surgical arms + Translucent head canopy & UV pharmacy (`BLEND`) | `med_autodoc_r1_01.png` | Validated |
| `02` | `med_autodoc_r1_02.glb` | **#02 — Dual-Zone Split Autodoc Gantry & Translucent UV Pharmacy Tower** | `2.25 × 1.28 × 2.15` | `0.0000` | 5,706 | **4,396** | 68/32 Split sibling to Locked Winners • Left surgical bed, twin robotic arms & halo lamp + Right full-height 3-tier translucent UV pharmacy tower (`BLEND`) | `med_autodoc_r1_02.png` | Validated |
| `03` | `med_autodoc_r1_03.glb` | **#03 — Twin-Arm Ceiling Cantilever Robotic Trauma Bay & Holo-Visor** | `2.15 × 1.25 × 2.15` | `0.0000` | 5,195 | **4,126** | Heavy C-arm ceiling surgical crane + 3 articulated micro-surgery manipulators + Dual surgical halo lamps + Clamshell translucent shield (`BLEND`) | `med_autodoc_r1_03.png` | Validated |
| `04` | `med_autodoc_r1_04.glb` | **#04 — Cryo-Stasis Isolation Pod & Sliding Toroidal MRI Gantry** | `2.20 × 1.30 × 2.12` | `0.0000` | 4,654 | **3,838** | Full-length semi-cylindrical translucent cryo-isolation canopy (`BLEND`) + Sliding toroidal magnetic-resonance gantry + Twin surgical arms | `med_autodoc_r1_04.png` | Validated |
| `05` | `med_autodoc_r1_05.glb` | **#05 — Zero-G Gimbaled Surgical Cradle & Biometric Triage Console** | `2.22 × 1.28 × 2.15` | `0.0000` | 4,747 | **3,670** | Rotary gimbal trunnion towers for spin-down surgery + Twin overhead robotic surgical arms + Translucent canopy & UV pharmacy (`BLEND`) | `med_autodoc_r1_05.png` | Validated |

---

## 3. Room 02 Hero Fixture — Pressurized Bulkhead Airlock Hatch (`/workspace/game-project/assets/glb/corridor_round1/`)

| # | Asset File | Hard Sci-Fi Airlock Hatch Archetype Title | Bounding Box (W × D × H m) | Min Y (m) | Vertices | Triangles | Translucent Glass & Features | Beauty Render | Status |
| :- | :--- | :--- | :--- | :--- | ---: | ---: | :--- | :--- | :--- |
| `01` | `corridor_door_r1_01.glb` | **#01 — Aegis-7 Octagonal Bi-Parting Blast Hatch & Checkpoint** | `2.45 × 0.70 × 2.75` | `0.0000` | 4,936 | **4,390** | Overhead linear actuator gantry • Parted doors with 3 interlocking steel dog-latch teeth per leaf • Twin `glass_airlock_viewport_translucent.png` (`BLEND`) windows | `corridor_door_r1_01.png` | Validated |
| `02` | `corridor_door_r1_02.glb` | **#02 — Dual-Zone Airlock Portal & Emergency O2/Extinguisher Side Bay** | `2.60 × 0.73 × 2.75` | `0.0000` | 6,494 | **5,472** | 68/32 Split sibling to Locked Winners • Left parted octagonal hatch + Right OLED checkpoint & `glass_airlock_viewport_translucent.png` (`BLEND`) fire-extinguisher/trauma locker | `corridor_door_r1_02.png` | Validated |
| `03` | `corridor_door_r1_03.glb` | **#03 — Cylindrical Plug-Door Pressure Lock & Rotary Dog-Latch Portal** | `2.45 × 0.78 × 2.75` | `0.0000` | 5,168 | **4,614** | Submarine-style swing-link plug-door halves + 8 radial locking dogs + signal-orange spider handwheel + translucent portholes | `corridor_door_r1_03.png` | Validated |
| `04` | `corridor_door_r1_04.glb` | **#04 — Hex-Aperture Interlocking Wedge-Blade Sector Bulkhead** | `2.50 × 0.70 × 2.75` | `0.0000` | 4,970 | **4,336** | Wide hexagonal pressure coaming + 4 interlocking shear-tooth wedge blades + trapezoidal translucent windows + dual side OLEDs | `corridor_door_r1_04.png` | Validated |
| `05` | `corridor_door_r1_05.glb` | **#05 — Panoramic Twin-Window Observation Airlock & Decon Arch** | `2.55 × 0.76 × 2.78` | `0.0000` | 5,434 | **4,662** | Internal UV-violet (`#7B5CFF`) & sonic-mist decon nozzles + Floor-to-head-height panoramic `glass_airlock_viewport_translucent.png` (`BLEND`) doors | `corridor_door_r1_05.png` | Validated |

---

## 4. Modular Room Shells (`/workspace/game-project/assets/glb/rooms/` & `/workspace/game-project/assets/glb/`)

| Room # | Asset Files | Architectural Envelope (W × D × H m) | Min Y (m) | Vertices | Triangles | Translucent Gallery | Status |
| :--- | :--- | :--- | :--- | ---: | ---: | :--- | :--- |
| **Room 01** | `rooms/room_01_shell.glb`, `rooms/room_01_sleeping_quarters_shell.glb`, `room_01_shell.glb` | `6.00 × 7.00 × 3.20` | `0.0000` | 5,986 | **3,258** | North 3-Panel Panoramic Translucent Window (`BLEND`) + West Open Bunk Viewport Cutouts + 5 Octagonal Ribs | Validated |
| **Room 02** | `rooms/room_02_shell.glb`, `rooms/room_02_corridor_shell.glb`, `room_02_corridor_shell.glb` | `3.80 × 12.22 × 3.20` | `0.0000` | 4,916 | **2,292** | 6-Bay West Panoramic Translucent Window Gallery (`BLEND`) + 7 Octagonal Titanium Ribs | Validated |
| **Room 03** | `rooms/room_03_shell.glb`, `rooms/room_03_mess_shell.glb`, `rooms/room_03_mess_galley_shell.glb`, `room_03_shell.glb`, `room_03_mess_shell.glb` | `7.00 × 8.00 × 3.20` | `0.0000` | 5,491 | **2,774** | North 3-Bay Panoramic O'Neill Cylinder Viewport (`BLEND`) + 5 Octagonal Titanium Ribs + Coffered Ceiling | Validated |
| **Room 04** | `rooms/room_04_shell.glb`, `rooms/room_04_medbay_shell.glb`, `rooms/room_04_med_bay_shell.glb`, `room_04_shell.glb`, `room_04_medbay_shell.glb` | `6.50 × 7.50 × 3.20` | `0.0000` | 5,587 | **2,818** | North 3-Panel Outer-Hull Deep-Space Viewport (`BLEND`) + Surgical Ice-White Theater Halo + UV Decon Strips | Validated |

---

## 5. Locked Tournament Winners (`/workspace/game-project/assets/glb/winners/`)

| Category | Winner File | Selected Candidate & Archetype Title | Bounding Box (W × D × H m) | Min Y (m) | Vertices | Triangles | Translucent Glass Material | Status |
| :--- | :--- | :--- | :--- | :--- | ---: | ---: | :--- | :--- |
| **Bunk Pod #1** | `bunk_winner_01_orbital_viewport.glb` | Round 1 `#06` — **Orbital Viewport Pod** (plus `_deepspace` & `_cylinder` variants) | `2.18 × 1.14 × 1.93` | `0.0000` | 3,414 | **4,094** | `Mat_Viewport_Glass_Translucent` (`BLEND`) | Locked & Validated |
| **Bunk Pod #2** | `bunk_winner_02_medical_biomonitor.glb` | Round 2 `#07` — **Medical Biomonitor Pod** | `2.19 × 1.14 × 1.90` | `0.0000` | 2,903 | **3,296** | `Mat_Glass_HoloVisor_Translucent` + `Mat_Viewport_Glass_Translucent` (`BLEND`) | Locked & Validated |
| **Bunk Pod #3** | `bunk_winner_03_hex_hive_stack.glb` | Round 2 `#08` — **Modular Hex-Hive Stack** | `2.22 × 1.17 × 2.09` | `0.0000` | 4,244 | **5,500** | Dual Lower/Upper `Mat_Viewport_Glass_Translucent` (`BLEND`) | Locked & Validated |
| **Bunk Pod #4** | `bunk_winner_04_observation_lounge.glb` | Round 2 `#09` — **Observation Lounge Sleeper** | `2.20 × 1.18 × 1.91` | `0.0000` | 2,880 | **3,522** | 2-Stage Slanted Skylight `Mat_Viewport_Glass_Translucent` (`BLEND`) | Locked & Validated |
| **Fixture #1 (EVA Locker)** | `locker_winner_01_dual_bay_bulkhead.glb` | Round 1 `#02` — **Dual-Bay Recessed Bulkhead Suit & Kit Locker** | `1.35 × 0.75 × 2.10` | `0.0000` | 6,028 | **5,574** | `Mat_Glass_SuitBay_Translucent` (`BLEND`) | Locked & Validated |
| **Fixture #2 (Hygiene Vanity)** | `vanity_winner_01_dual_zone_grooming.glb` | Round 1 `#03` — **Dual-Zone Split Grooming & UV Decon Station** | `1.05 × 0.58 × 2.08` | `0.0000` | 4,347 | **4,192** | `Mat_Glass_UVCubby_Translucent` + `Mat_Glass_SonicShield_Translucent` (`BLEND`) | Locked & Validated |
| **Fixture #3 (Wall Terminal Desk)** | `walldesk_winner_01_split_comms_station.glb` | Round 1 `#02` — **Dual-Tier Split Comms & Storage Drop-Leaf Station** | `1.05 × 0.70 × 2.00` | `0.0000` | 4,909 | **3,698** | `Mat_Glass_HoloHUD_Translucent` (`BLEND`) | Locked & Validated |
| **Fixture #6 (Cargo Footlocker)** | `footlocker_winner_01_split_cargo_trunk.glb` | Round 1 `#02` — **Dual-Bay Split Cargo Trunk & Pull-Out Drawer Module** | `1.16 × 0.69 × 0.84` | `0.0000` | 5,401 | **4,288** | `Mat_Glass_CargoLid_Translucent` (`BLEND`) | Locked & Validated |
| **Fixture #9 (Climate & O2 Panel)** | `climate_winner_01_split_env_o2_station.glb` | Round 1 `#02` — **Dual-Zone Split Atmospheric Telemetry & Emergency Breather Bay** | `0.96 × 0.32 × 1.92` | `0.0000` | 4,906 | **3,834** | `Mat_Glass_O2Bay_Translucent` (`BLEND`) | Locked & Validated |
