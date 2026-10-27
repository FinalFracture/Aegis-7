# Aegis-7 Exterior Architectural Silhouette, Practical Greebling, Cinema Scale Cues & Movie Prop Blueprint
**Author:** Vance (`0724beeb-94b9-43fa-a9cf-27117c5d4aa6`) — Sci-Fi Architect, Movie Prop & Set Design Specialist (collaborating with Sloane, Rook, Gage, Scribe & Atlas)
**Canonical Paths:**
- `/workspace/game-project/design/vance_scifi_set_and_exterior_props_spec.md`
- `/workspace/game-project/design/buildings_15_exteriors_spec.md`
**Phase:** Phase 2 — 15 O'Neill Cylinder Building Exteriors (`bldg_01`–`bldg_15`), 3 District Plazas & Grand Metropolis Scene (`cylinder_hab7_metropolis.tscn`)

---

## 1. Cinema Set-Design Philosophy & Hard Sci-Fi Pedigree (*2001*, *Alien*, *Oblivion*, *Elysium*, *Moon*)
Every exterior structure in *Orbital Hab-7* (an **800m long × 400m diameter rotating O'Neill Cylinder**) must read on camera as a tangible, engineered spacecraft-grade movie set designed by a single unified architectural bureau (**The Aegis-7 Bureau of Orbital Engineering**):

1. **The Signature 65/35 & 68/32 Asymmetric Split-Mass Silhouette (`Candidate #02` Standard):**
   - Purely symmetrical towers or domes flatten out under 3/4 isometric and street-level cinema cameras.
   - **Candidate `#02` in every single round (`bldg_01` through `bldg_15`)** executes our signature **Aegis-7 Dual-Zone Split-Bay Architecture**:
     - **Primary Structural Mass (65–68% Width):** Heavy load-bearing octagonal tower, terraced composite hall, or armored containment vault clad in **Matte Aerospace White (`#D8DEE6`)** and **Dark Anodized Gunmetal Titanium (`#1A1E24`)** with 45° chamfered corner buttresses.
     - **Secondary Vertical Functional Spine / Atrium / Gantry (32–35% Width):** Full-height **Machined Brushed Steel (`#88929E`)** and **Dark Carbon Slate (`#282E38`)** structural frame housing a **true `alphaMode: "BLEND"` translucent glass (`alpha 0.28–0.42`)** elevator atrium, aeroponic herb/algae bio-column, cryo-distillation stack, 5-coil plasma pinch tower, or orbital shuttle/drone gantry—with real 3D interior floor slabs, illuminated columns, foliage, or plasma cores visible inside!
2. **Human-Scale Cinema Cues (Preventing "Miniature Model" Syndrome):**
   - Every building sits on a **45° chamfered octagonal gunmetal plaza plinth (`#1A1E24` / `#1F2630`, `0.40m–0.60m` high)** with recessed **Amber (`#FF9500`) perimeter safety strips** and approached via **2.1m-tall × 1.8m-wide chamfered octagonal airlock blast portals** framed in **Signal-Orange (`#D95B26`)** pressure collars.
   - Pedestrian terraces and roof decks feature **1.1m-high brushed-steel safety handrails**, **0.45m EVA hatch dogs**, **1.4m umbilical manifold cabinets**, and **3.6m floor-to-floor spandrel rhythms** (`facade_carbon_slate_spandrel.png` + `window_grid_lit_habitat.png`).
3. **Practical Functional Greebling (Zero Random Box-Noise):**
   - Every exterior detail serves a legible life-support, spin-gravity, thermal, or orbital logistics function:
     - **Rooftop & Crown Movie Props:** Rotating deep-space telemetry/radar dishes, octagonal med-evac & shuttle VTOL landing pads with **Signal-Orange (`#D95B26`) magnetic deck clamps**, cryogenic boil-off relief stacks, louvered radiator fin banks, and elevated holo-sector beacons.
     - **Facade & Bulkhead Movie Props:** External EVA umbilical recharge manifolds, 45° chamfered titanium seismic/spin-load ribs with recessed **Cyan (`#00E5FF`) telemetry light strips**, magnetic cargo crane rails, and pressurized skybridge docking collars.

---

## 2. Unified Aegis-7 Exterior Material & Texture Palette (`< 1.2%` Micro-Noise)
All 15 buildings share the clean, calm PBR material library in `/workspace/game-project/assets/textures/buildings/` and `/workspace/game-project/assets/textures/`:

| Material Slot | Hex / PBR Target | Texture Map (`/workspace/game-project/assets/textures/buildings/`) | Architectural & Prop Usage |
| :--- | :--- | :--- | :--- |
| `Mat_Titanium_GunmetalHull` | `#1A1E24` (`metal 0.78`, `rough 0.34`) | `facade_titanium_gunmetal_hull.png` / `metal_gunmetal_hull.png` | 45° chamfered octagonal plinths, structural corner buttresses, blast shutters, armor monoliths |
| `Mat_Composite_AerospaceWhite` | `#D8DEE6` (`metal 0.08`, `rough 0.30`) | `facade_aerospace_white_cladding.png` / `panel_aerospace_white.png` | Primary molded composite building shells, terraced residential pods, clinical/command cladding |
| `Mat_Carbon_SlateFrame` | `#282E38` (`metal 0.58`, `rough 0.40`) | `facade_carbon_slate_spandrel.png` / `metal_carbon_slate.png` | Inter-floor spandrel beams, recessed window mullions, plaza deck slabs, radiator louvers |
| `Mat_Steel_MachinedGantry` | `#88929E` (`metal 0.90`, `rough 0.22`) | `facade_brushed_steel_gantry.png` / `metal_brushed_steel.png` | 35% secondary gantry spines, crane trusses, Dish/actuator gimbals, EVA handrails, docking rings |
| `Mat_Accent_SignalOrange` | `#D95B26` (`metal 0.25`, `rough 0.38`) | `accent_signal_orange.png` / `accent_safety_orange.png` | Airlock portal collars, VTOL landing pad clamps, ISO container corner castings, emergency valves |
| `Mat_Window_LitHabitat` | `#00E5FF` / `#E0F4FF` (`emission 1.65`) | `window_grid_lit_habitat.png` | Illuminated multi-story cabin/lab window bands |
| `Mat_Signage_AegisMarquee` | `#00E5FF` / `#FF9500` (`emission 1.65`) | `signage_aegis7_building_marquees.png` | Sector/building ID marquees (`HAB-01` .. `PYLON-15`), airlock status headers |
| `Mat_Emissive_CyanLED` | `#00E5FF` (`emission 2.0`) | `led_cyan_strip.png` | Vertical architectural rib light channels, telemetry rings, plasma pinch coils |
| `Mat_Emissive_AmberLED` | `#FF9500` (`emission 2.0`) | `led_amber_strip.png` | Octagonal plaza plinth safety perimeter strips, helipad perimeter strobes, cargo crane hazard bars |
| `Mat_Emissive_UVViolet` | `#7B5CFF` (`emission 2.0`) | `led_uv_violet.png` | Aeroponic grow-light columns, sterile cryo-pharmacy cores, zero-G lounge accents |
| `Mat_Glass_CurtainWall_Cyan` | `#7CE8FF` (`alphaMode: "BLEND"`, `a=0.28–0.36`) | `glass_curtainwall_cyan_translucent.png` | Translucent sky-elevator atria, command towers, cryo-columns, shuttle docking pinnacles |
| `Mat_Glass_Biodome_Emerald` | `#58E8B8` (`alphaMode: "BLEND"`, `a=0.28–0.36`) | `glass_biodome_emerald_translucent.png` | Translucent hydroponic domes, culinary herb towers, O2 algae bio-scrubber columns |

---

## 3. Street-Level Plaza & Rooftop Hero Movie Prop Catalog (Districts I–III & Metropolis)
To anchor the 3 District Showcase Scenes (`district_01_residential_civic.tscn`, `district_02_agri_research.tscn`, `district_03_command_industrial.tscn`) and the Grand 15-Building Metropolis (`cylinder_hab7_metropolis.tscn`):

1. **Elevated Mag-Lev Guideway Pylons & Ring-Transit Pods (`Prop_Set_01`):**
   - Chamfered gunmetal (`#1A1E24`) Y-pylons supporting twin brushed-steel (`#88929E`) magnetic guideway rails with continuous recessed **Cyan (`#00E5FF`) induction strips** and sleek aerodynamic aerospace-white (`#D8DEE6`) transit shuttle pods.
2. **Octagonal Pedestrian Wayfinding & Telemetry Holo-Kiosks (`Prop_Set_02`):**
   - `2.4m`-tall dark carbon-slate (`#282E38`) plaza totems with `alphaMode: "BLEND"` cyan holographic sector maps, emergency breather locker doors (`#D95B26` latch), and amber base plinth lighting (`#FF9500`).
3. **Atmospheric Scrubber Vents & Spin-Gravity Balancer Bollards (`Prop_Set_03`):**
   - Street-corner cylindrical intake louvers in `#1A1E24` and `#88929E` with glowing internal cyan fan baffles and heavy signal-orange (`#D95B26`) EVA tether rings along promenade edges.
4. **Terraced Civic Planter & Crew Bench Pods (`Prop_Set_04`):**
   - Octagonal aerospace-white (`#D8DEE6`) planter basins with integrated contoured charcoal seating pads (`#242932`), warm amber (`#FF9500`) under-bench cove strips, and UV-lit aeroponic greenery (`foliage_aeroponic_herbs.png`).
5. **Rooftop VTOL Med-Evac / Shuttle Landing Pads & Rotating Telemetry Arrays (`Prop_Set_05`):**
   - Cantilevered octagonal landing decks with glowing amber (`#FF9500`) H-reticles, 4 signal-orange (`#D95B26`) hydraulic wheel/skid lock clamps, and gimbaled brushed-steel (`#88929E`) deep-space dishes.

---

## 4. Building-by-Building Architectural & 5-Candidate Specification (`bldg_01` – `bldg_15`)
*All models: bottom-center pivot `(0,0,0)` (`min Y = 0.0`), front `+Z`, triangle budget `3,000–6,000` tris, `alphaMode: "BLEND"` on all translucent glass with 3D interior structures.*

### DISTRICT I — RESIDENTIAL & CIVIC TERRACE SECTOR (`bldg_01` – `bldg_05`)

#### 1. Building 01 (`bldg_01_hab_spire`) — Aegis-7 Modular Crew Habitat Tower
- **Footprint & Envelope:** `12.0m W × 10.0m D × 18.0m H` | **Target Budget:** `3,800–5,400` tris
- **Candidate Lineup (`bldg_01_r1_01.glb` .. `bldg_01_r1_05.glb`):**
  - `#01` (`bldg_01_r1_01.glb`) — *Symmetric Octagonal Stepped Pod Spire*: Central octagonal core with 4 tiers of symmetrical cantilevered sleeping pods; clean monumentality, though symmetrical silhouette is less dynamic from 3/4 angles.
  - `#02` (`bldg_01_r1_02.glb`) — **Dual-Zone Split Residential Pod Spire & Translucent Sky-Elevator Atrium Tower (Aegis-7 65/35 Signature)**:
    - **Left 65% Primary Zone:** 5-story stepped octagonal residential tower in matte aerospace white (`#D8DEE6`) and gunmetal titanium ribs (`#1A1E24`), featuring cantilevered Orbital Viewport Bunk bays, illuminated habitat window grids (`window_grid_lit_habitat.png`), and signal-orange (`#D95B26`) emergency EVA balcony hatches.
    - **Right 35% Secondary Zone:** Full-height (`18.0m`) brushed-steel (`#88929E`) & `alphaMode: "BLEND"` cyan glass (`glass_curtainwall_cyan_translucent.png`) Sky-Elevator Atrium revealing 5 interior floor landings, twin illuminated vertical elevator guide rails, a mid-height zero-G transfer skybridge, and a rooftop comms/HVAC beacon mast.
  - `#03` (`bldg_01_r1_03.glb`) — *Twin-Cantilevered Hex-Hive Terraced Apartment Block*: Interlocking hexagonal sleep-pod matrix over a dual-portal lobby base.
  - `#04` (`bldg_01_r1_04.glb`) — *Curved Cylinder-Slope Terraced Habitat Ziggurat*: Stepped terrace profile matching the inner curvature of the O'Neill cylinder with rooftop solar pergolas.
  - `#05` (`bldg_01_r1_05.glb`) — *Suspended Modular Pod-Cluster & Skybridge Tower*: Twin exterior truss pylons suspending plug-in habitat modules above an open plaza breezeway.

#### 2. Building 02 (`bldg_02_transit_rotunda`) — Elevated Mag-Lev & Ring Transit Rotunda
- **Footprint & Envelope:** `14.0m W × 11.0m D × 14.5m H` | **Target Budget:** `3,600–5,400` tris
- **Candidate Lineup (`bldg_02_r1_01.glb` .. `bldg_02_r1_05.glb`):**
  - `#01` (`bldg_02_r1_01.glb`) — *Octagonal Central Mag-Lev Concourse Rotunda*: Drum rotunda with radial guideway stubs and central skylight dome.
  - `#02` (`bldg_02_r1_02.glb`) — **Dual-Zone Split Mag-Lev Station Hall & Vertical Shuttle-Pod Boarding Tower (Aegis-7 65/35 Signature)**:
    - **Left 65% Primary Zone:** Elevated octagonal commuter concourse (`#D8DEE6` / `#1A1E24`) spanned by an elevated brushed-steel mag-lev guideway deck with a docked aerodynamic transit pod, signal-orange (`#D95B26`) platform safety gates, and `HAB-TRANSIT 02` marquee signage.
    - **Right 35% Secondary Zone:** Vertical `alphaMode: "BLEND"` translucent glass Shuttle-Pod Boarding & Escalator Spine revealing interior passenger mezzanine rings, cyan telemetry totem, and rooftop traffic-control radar beacon.
  - `#03` (`bldg_02_r1_03.glb`) — *Twin-Tube Elevated Guideway Overpass Terminal*: Parallel cylindrical transit tubes bridging an open ticket concourse.
  - `#04` (`bldg_02_r1_04.glb`) — *Cantilevered Ring-Line Commuter Hub & Control Pylon*: Single-sided cantilevered platform wing counterbalanced by a heavy traction-power pylon.
  - `#05` (`bldg_02_r1_05.glb`) — *Tri-Level Rotary Transit Interchange Plaza*: Stacked circular transfer decks with external spiral ramp trusses.

#### 3. Building 03 (`bldg_03_culinary_atrium`) — Terraced Synthesizer & Culinary Commons Pavilion
- **Footprint & Envelope:** `13.0m W × 11.0m D × 14.0m H` | **Target Budget:** `3,600–5,200` tris
- **Candidate Lineup (`bldg_03_r1_01.glb` .. `bldg_03_r1_05.glb`):**
  - `#01` (`bldg_03_r1_01.glb`) — *Octagonal Glass-Crowned Mess Hall Pavilion*: Symmetrical dining pavilion with a central faceted skylight cupola.
  - `#02` (`bldg_03_r1_02.glb`) — **Dual-Zone Split Culinary Dining Pavilion & Full-Height Translucent Aeroponic Herb Tower (Aegis-7 65/35 Signature)**:
    - **Left 65% Primary Zone:** 3-level terraced aerospace-white (`#D8DEE6`) and gunmetal (`#1A1E24`) culinary commons with cantilevered promenade dining balconies, warm amber (`#FF9500`) cove lighting, and external nutrient-synth storage tanks with signal-orange (`#D95B26`) couplings.
    - **Right 35% Secondary Zone:** Full-height `alphaMode: "BLEND"` emerald/cyan glass (`glass_biodome_emerald_translucent.png`) **Vertical Aeroponic Herb & Botanical Tower** revealing 4 internal rotating UV-violet (`#7B5CFF`) planter rings and lush greenery (`foliage_aeroponic_herbs.png`) feeding directly into the galley below.
  - `#03` (`bldg_03_r1_03.glb`) — *Terraced Promenade Bistro & Zero-G Beverage Rotunda*: Stepped outdoor dining decks paired with a spherical upper lounge.
  - `#04` (`bldg_03_r1_04.glb`) — *Twin-Wing Civic Refectory & Solar-Lit Courtyard*: U-shaped mess hall framing a recessed plaza courtyard.
  - `#05` (`bldg_03_r1_05.glb`) — *Cantilevered Overlook Dining Deck & Ration Silo Complex*: Long viewing deck cantilevered over triple cylindrical ration silos.

#### 4. Building 04 (`bldg_04_medical_trauma_center`) — Orbital Trauma & Biomonitor Medical Complex
- **Footprint & Envelope:** `13.5m W × 11.0m D × 16.0m H` | **Target Budget:** `3,800–5,500` tris
- **Candidate Lineup (`bldg_04_r1_01.glb` .. `bldg_04_r1_05.glb`):**
  - `#01` (`bldg_04_r1_01.glb`) — *Octagonal Med-Bay Clinical Pavilion with Rooftop Med-Evac Pad*: Central trauma block crowned by a centered helipad.
  - `#02` (`bldg_04_r1_02.glb`) — **Dual-Zone Split Trauma Hospital Wing & Translucent UV-Sterile Cryo-Pharmacy Tower (Aegis-7 65/35 Signature)**:
    - **Left 65% Primary Zone:** Clean molded aerospace-white (`#D8DEE6`) surgical & biomonitor trauma wing with chamfered gunmetal (`#1A1E24`) quarantine bulkheads, ambulance airlock bay (`#D95B26` collar), and a cantilevered **Rooftop Med-Evac VTOL Pad** with glowing amber (`#FF9500`) perimeter lights and medical cross beacon.
    - **Right 35% Secondary Zone:** Full-height `alphaMode: "BLEND"` translucent glass **UV-Sterile Cryo-Pharmacy & Autodoc Telemetry Tower** glowing with surgical cyan (`#00E5FF`) and UV-violet (`#7B5CFF`) internal light, revealing 3D vertical cryo-stasis carousel racks and floor slabs inside.
  - `#03` (`bldg_04_r1_03.glb`) — *Twin-Dome Bio-Quarantine & Triage Center*: Dual pressurized isolation domes linked by a decontamination airlock spine.
  - `#04` (`bldg_04_r1_04.glb`) — *Stepped Aerospace-White Surgical Institute & Ambulance Dock*: Ziggurat clinical block with ground-level pressurized rover bays.
  - `#05` (`bldg_04_r1_05.glb`) — *Cantilevered Zero-G Recovery Sanatorium & Telemetry Spire*: Elevated zero-G surgical pod cantilevered off a central life-support mast.

#### 5. Building 05 (`bldg_05_celestial_promenade_dome`) — Zero-G Observation & Recreation Dome
- **Footprint & Envelope:** `14.0m W × 12.0m D × 15.5m H` | **Target Budget:** `3,800–5,600` tris
- **Candidate Lineup (`bldg_05_r1_01.glb` .. `bldg_05_r1_05.glb`):**
  - `#01` (`bldg_05_r1_01.glb`) — *Faceted Octagonal Geodesic Observation Dome*: Single large central translucent dome on an octagonal plinth.
  - `#02` (`bldg_05_r1_02.glb`) — **Dual-Zone Split Stargazer Lounge Dome & Illuminated Zero-G Ascent Tower (Aegis-7 65/35 Signature)**:
    - **Left 65% Primary Zone:** Faceted octagonal `alphaMode: "BLEND"` geodesic **Stargazer Lounge Dome** cradled in chamfered aerospace-white (`#D8DEE6`) and gunmetal (`#1A1E24`) ribs, revealing an internal sunken zero-G viewing ring, celestial bar core, and floating holo-orrery inside.
    - **Right 35% Secondary Zone:** Full-height brushed-steel (`#88929E`) & translucent glass **Zero-G Ascent Tube & Sky-Promenade Tower** with glowing cyan (`#00E5FF`) & violet (`#7B5CFF`) rings, a cantilevered horizon viewing balcony, and an upper observation crow's-nest.
  - `#03` (`bldg_05_r1_03.glb`) — *Twin-Ringed Panoramabridge & Amphitheater Pavilion*: Dual concentric viewing rings over an open civic amphitheater.
  - `#04` (`bldg_05_r1_04.glb`) — *Terraced Civic Park Conservatory & Holo-Fountain Rotunda*: Stepped botanical recreation decks around a central holo-projector.
  - `#05` (`bldg_05_r1_05.glb`) — *Cantilevered Horizon Viewing Deck & Celestial Bar Complex*: Dramatic cantilevered glass prow extending over the plaza boulevard.

---

### DISTRICT II — AGRI-BIOSPHERE & RESEARCH SECTOR (`bldg_06` – `bldg_10`)

#### 6. Building 06 (`bldg_06_hydroponic_biodome`) — Aeroponic & Bio-Scrubber Conservatory Complex
- **Footprint & Envelope:** `14.0m W × 12.0m D × 16.0m H` | **Target Budget:** `3,800–5,600` tris
- **Candidate Lineup (`bldg_06_r1_01.glb` .. `bldg_06_r1_05.glb`):**
  - `#01` (`bldg_06_r1_01.glb`) — *Tri-Dome Geodesic Botanical Conservatory*: Cluster of three symmetrical octagonal glass domes.
  - `#02` (`bldg_06_r1_02.glb`) — **Dual-Zone Split Greenhouse Conservatory & Full-Height Translucent O2 Algae Bio-Scrubber Tower (Aegis-7 65/35 Signature)**:
    - **Left 65% Primary Zone:** Multi-tier octagonal `alphaMode: "BLEND"` emerald glass (`glass_biodome_emerald_translucent.png`) **Aeroponic Conservatory Hall** framed in aerospace-white (`#D8DEE6`) and gunmetal (`#1A1E24`) arches, revealing 3D terraced green crop beds (`foliage_aeroponic_herbs.png`) and UV-violet (`#7B5CFF`) grow-light bars inside.
    - **Right 35% Secondary Zone:** Towering `16.0m` brushed-steel (`#88929E`) & translucent cyan/emerald **O2 Photosynthetic Algae Bio-Scrubber Column** with visible internal helical bioreactor tubes, external nutrient dosing tanks (`#D95B26` valves), and rooftop atmospheric exhaust crown.
  - `#03` (`bldg_06_r1_03.glb`) — *Stepped Agricultural Ziggurat & UV-Grow Terrace*: Terraced horizontal tray-farm tiers with external irrigation manifolds.
  - `#04` (`bldg_06_r1_04.glb`) — *Twin-Cylinder Vertical Farm & Nutrient Silo Array*: Side-by-side vertical grow drums on an industrial manifold base.
  - `#05` (`bldg_06_r1_05.glb`) — *Octagonal Biosphere Rotunda & Canopy Skywalk*: Central conservatory drum encircled by an elevated steel inspection catwalk.

#### 7. Building 07 (`bldg_07_atmospheric_processor`) — Sector Atmospheric & O2/CO2 Scrubber Plant
- **Footprint & Envelope:** `13.5m W × 11.0m D × 17.0m H` | **Target Budget:** `3,800–5,500` tris
- **Candidate Lineup (`bldg_07_r1_01.glb` .. `bldg_07_r1_05.glb`):**
  - `#01` (`bldg_07_r1_01.glb`) — *Octagonal Air-Exchange Intake & Turbine Hall*: Heavy industrial air-handling block with roof intake cowls.
  - `#02` (`bldg_07_r1_02.glb`) — **Dual-Zone Split Atmospheric Processor Hall & Translucent Cryo-O2 Distillation Tower (Aegis-7 65/35 Signature)**:
    - **Left 65% Primary Zone:** Armored gunmetal (`#1A1E24`) and aerospace-white (`#D8DEE6`) **Venturi Air-Exchange & Sabatier Reactor Hall** featuring recessed carbon-slate intake louver banks, glowing cyan (`#00E5FF`) barometric telemetry bands, and signal-orange (`#D95B26`) high-pressure LOX manifold flanges.
    - **Right 35% Secondary Zone:** Full-height brushed-steel (`#88929E`) gantry framing a **Translucent `alphaMode: "BLEND"` Cryo-O2 Fractional Distillation Column**, revealing 3D internal frosted condenser plates, glowing cyan gas-ionization rings, and rooftop pressure-relief stack.
  - `#03` (`bldg_07_r1_03.glb`) — *Quad-Stack Venturi Scrubber & Thermal Louver Plant*: Four vertical exhaust chimneys over a rectangular filter hall.
  - `#04` (`bldg_07_r1_04.glb`) — *Twin-Sphere Liquid-Oxygen Storage & Barometric Station*: Dual spherical cryogenic tanks beside a control bunker.
  - `#05` (`bldg_07_r1_05.glb`) — *Heavy Industrial Spin-Filter & Humidity Control Complex*: Rotary drum scrubber housing with external ducting bridges.

#### 8. Building 08 (`bldg_08_astrometry_observatory`) — Deep-Space Astrometry & Sensor Array Complex
- **Footprint & Envelope:** `13.5m W × 11.5m D × 17.5m H` | **Target Budget:** `3,800–5,600` tris
- **Candidate Lineup (`bldg_08_r1_01.glb` .. `bldg_08_r1_05.glb`):**
  - `#01` (`bldg_08_r1_01.glb`) — *Octagonal Clamshell Optical Telescope Observatory*: Classic cylindrical observatory drum capped by a slotted dome.
  - `#02` (`bldg_08_r1_02.glb`) — **Dual-Zone Split Astrometry Research Lab & Rotating Deep-Space Telemetry Dish Tower (Aegis-7 65/35 Signature)**:
    - **Left 65% Primary Zone:** Stepped octagonal **Astrometry & Quantum Sensor Lab** (`#D8DEE6` / `#1A1E24`) crowned by a faceted `alphaMode: "BLEND"` translucent **Star-Charting Dome** revealing an internal 3D holographic star-map projector and telescope pier.
    - **Right 35% Secondary Zone:** Full-height brushed-steel (`#88929E`) **Deep-Space Telemetry Gantry Tower** with a translucent vertical wave-guide core, mid-level gimbaled sensor pods, and a hero **Rotating Parabolic Deep-Space Dish & Laser-Comms Emitter** at the summit (`#00E5FF` & `#D95B26` accents).
  - `#03` (`bldg_08_r1_03.glb`) — *Tri-Dish Interferometer & Quantum Comms Array Building*: Three roof-mounted dish antennas on a long sensor terrace.
  - `#04` (`bldg_08_r1_04.glb`) — *Stepped Sensor Dome & Subspace Beacon Annex*: Terraced research block with an angled subspace needle mast.
  - `#05` (`bldg_08_r1_05.glb`) — *Cantilevered Deep-Sky Spectrograph & Holo-Charting Center*: Angled spectrograph tube projecting from an octagonal lab core.

#### 9. Building 09 (`bldg_09_aquifer_pumping_station`) — Ring-Gravity Water Reclamation & Aquifer Cascade
- **Footprint & Envelope:** `13.5m W × 11.0m D × 16.0m H` | **Target Budget:** `3,600–5,400` tris
- **Candidate Lineup (`bldg_09_r1_01.glb` .. `bldg_09_r1_05.glb`):**
  - `#01` (`bldg_09_r1_01.glb`) — *Octagonal Hydro-Filtration Hall & Settling Basin*: Central pump house surrounded by a low perimeter water basin.
  - `#02` (`bldg_09_r1_02.glb`) — **Dual-Zone Split Centrifugal Pumping Plant & Translucent Illuminated Water-Column Tower (Aegis-7 65/35 Signature)**:
    - **Left 65% Primary Zone:** Heavy chamfered gunmetal (`#1A1E24`) and aerospace-white (`#D8DEE6`) **Centrifugal Hydro-Pumping & UV-Filtration Hall** with external brushed-steel (`#88929E`) main aquifer aqueduct pipes, signal-orange (`#D95B26`) floodgate wheel valves, and a stepped **Illuminated Cyan Water-Cascade Spillway** at the plaza front.
    - **Right 35% Secondary Zone:** Full-height `alphaMode: "BLEND"` translucent cyan glass **Hydro-Static Surge & UV-Purification Water Column Tower** revealing 3D internal vortex baffle rings, glowing cyan (`#00E5FF`) water-level telemetry bars, and a rooftop header tank.
  - `#03` (`bldg_09_r1_03.glb`) — *Terraced Cascade Spillway & UV-Purification Complex*: Multi-stepped water aeration waterfalls flanking a central pump room.
  - `#04` (`bldg_09_r1_04.glb`) — *Twin-Silo Greywater Recovery & Mineral Dosing Station*: Dual cylindrical water silos with overhead pipe bridges.
  - `#05` (`bldg_09_r1_05.glb`) — *Heavy Conduit Manifold & Pressure-Regulator Building*: Industrial pipeline junction station with external accumulator spheres.

#### 10. Building 10 (`bldg_10_cryo_seed_vault`) — Colonial Cryo-Genetics & Seed Archive Vault
- **Footprint & Envelope:** `13.0m W × 10.5m D × 16.5m H` | **Target Budget:** `3,600–5,400` tris
- **Candidate Lineup (`bldg_10_r1_01.glb` .. `bldg_10_r1_05.glb`):**
  - `#01` (`bldg_10_r1_01.glb`) — *Armored Octagonal Sub-Zero Gene Bank Monolith*: Fortress-like sloped titanium vault with minimal apertures.
  - `#02` (`bldg_10_r1_02.glb`) — **Dual-Zone Split Armored Seed Archive Vault & Translucent Cryo-Stasis Helix Tower (Aegis-7 65/35 Signature)**:
    - **Left 65% Primary Zone:** Heavily buttressed 45° chamfered gunmetal (`#1A1E24`) and matte aerospace-white (`#D8DEE6`) **Armored Sub-Zero Seed & Embryo Vault Monolith** with deep-recessed blast airlock portal (`#D95B26` dogs), external liquid-nitrogen radiator fin banks (`#282E38`), and cold cyan (`#00E5FF`) thermal telemetry strips.
    - **Right 35% Secondary Zone:** Full-height `alphaMode: "BLEND"` translucent glass **Cryo-Stasis DNA Helix & Robotic Retrieval Tower** illuminated in surgical cyan (`#00E5FF`) and UV-violet (`#7B5CFF`), revealing 3D stacked octagonal seed-carousel racks and a central robotic extractor column inside.
  - `#03` (`bldg_10_r1_03.glb`) — *Subterranean-Plinth Cryogenic Silo & Radiator Array*: Low armored dome ringed by tall vertical heat-rejection fins.
  - `#04` (`bldg_10_r1_04.glb`) — *Twin-Buttressed Bio-Preservation Bunker & Lab Wing*: Dual armored vaults bridged by an elevated genetics laboratory.
  - `#05` (`bldg_10_r1_05.glb`) — *Cantilevered Deep-Freeze Repository & Security Portal*: Elevated cryo-safe suspended above a security checkpoint plaza.

---

### DISTRICT III — COMMAND, POWER & INDUSTRIAL PORT SECTOR (`bldg_11` – `bldg_15`)

#### 11. Building 11 (`bldg_11_citadel_command_hq`) — Cylinder Hab-7 Central Command & Telemetry Citadel
- **Footprint & Envelope:** `14.5m W × 12.0m D × 21.0m H` (Tallest Civic/Command Landmark) | **Target Budget:** `4,200–5,900` tris
- **Candidate Lineup (`bldg_11_r1_01.glb` .. `bldg_11_r1_05.glb`):**
  - `#01` (`bldg_11_r1_01.glb`) — *Monumental Octagonal Command Spire & Bridge Crown*: Symmetrical high-rise command tower with an octagonal top bridge.
  - `#02` (`bldg_11_r1_02.glb`) — **Dual-Zone Split Command Citadel Spire & Translucent Quantum Flight-Director Tower (Aegis-7 65/35 Signature)**:
    - **Left 65% Primary Zone:** Soaring 6-tier chamfered octagonal **Central Command Citadel Spire** in aerospace-white (`#D8DEE6`) and gunmetal titanium (`#1A1E24`), crowned by a cantilevered wrap-around **Spin-Gravity Command Bridge** (`window_grid_lit_habitat.png` + `alphaMode: "BLEND"` bridge visor) and a rooftop **VIP Command Shuttle Pad** with signal-orange (`#D95B26`) clamps.
    - **Right 35% Secondary Zone:** Full-height (`21.0m`) brushed-steel (`#88929E`) & `alphaMode: "BLEND"` cyan glass **Quantum Flight-Director & Holo-Telemetry Tower** revealing a 3D vertical holographic O'Neill Cylinder status column, multi-deck command balconies, and a twin-array deep-space comms mast at the apex.
  - `#03` (`bldg_11_r1_03.glb`) — *Twin-Obelisk Sector Governance & Defense HQ*: Dual tapered towers connected by three skybridges.
  - `#04` (`bldg_11_r1_04.glb`) — *Stepped Pyramidion Overwatch Citadel & Holo-Beacon*: Tiered pyramid-octagonal fortress with a central holo-globe crown.
  - `#05` (`bldg_11_r1_05.glb`) — *Cantilevered High-Command Bridge & Comms Mast Complex*: Hammerhead command bridge projecting out from a heavy elevator core.

#### 12. Building 12 (`bldg_12_fusion_reactor_complex`) — D-He3 Fusion Power & Spin-Drive Reactor Hall
- **Footprint & Envelope:** `15.0m W × 12.5m D × 18.0m H` | **Target Budget:** `4,200–5,900` tris
- **Candidate Lineup (`bldg_12_r1_01.glb` .. `bldg_12_r1_05.glb`):**
  - `#01` (`bldg_12_r1_01.glb`) — *Octagonal Magnetic-Confinement Fusion Reactor Dome*: Central armored tokamak dome with radial transformer bays.
  - `#02` (`bldg_12_r1_02.glb`) — **Dual-Zone Split Fusion Containment Hall & Translucent 5-Coil Plasma Pinch Tower (Aegis-7 65/35 Signature)**:
    - **Left 65% Primary Zone:** Heavy armored gunmetal (`#1A1E24`) and aerospace-white (`#D8DEE6`) **D-He3 Magnetic Containment & Turbine Hall** with 45° chamfered radiation buttresses, dark carbon-slate (`#282E38`) graphene heat-rejection radiator wings, and signal-orange (`#D95B26`) cryogenic He3 transfer couplings.
    - **Right 35% Secondary Zone:** Full-height brushed-steel (`#88929E`) & `alphaMode: "BLEND"` translucent radiation-glass **5-Coil Axial Plasma Pinch & Cryo-Injector Tower**, showcasing 5 external toroidal magnetic confinement rings and a blazing internal **Cyan (`#00E5FF`) / UV-Violet (`#7B5CFF`) & Amber (`#FF9500`) Plasma Core Column** visible through the shield glass.
  - `#03` (`bldg_12_r1_03.glb`) — *Twin-Core Toroidal Tokamak & Radiator Fin Complex*: Dual reactor drums flanked by tall folded radiator arrays.
  - `#04` (`bldg_12_r1_04.glb`) — *Heavy Armored Spin-Drive Impulse Plant & Cryo Bay*: Industrial propulsion-grade power hall with heavy busbar conduits.
  - `#05` (`bldg_12_r1_05.glb`) — *High-Voltage Substation & Plasma Conduit Gantry Hall*: Open switchyard gantry paired with an armored control block.

#### 13. Building 13 (`bldg_13_cargo_logistics_port`) — High-Bay Intermodal Cargo & Drone Gantry Terminal
- **Footprint & Envelope:** `15.0m W × 12.0m D × 16.5m H` | **Target Budget:** `4,000–5,800` tris
- **Candidate Lineup (`bldg_13_r1_01.glb` .. `bldg_13_r1_05.glb`):**
  - `#01` (`bldg_13_r1_01.glb`) — *Octagonal High-Bay Freight Warehouse & Crane Arch*: Enclosed octagonal cargo warehouse spanned by a single roof arch.
  - `#02` (`bldg_13_r1_02.glb`) — **Dual-Zone Split Intermodal Cargo Terminal & Translucent ISO Container / Drone Gantry Tower (Aegis-7 65/35 Signature)**:
    - **Left 65% Primary Zone:** High-bay chamfered gunmetal (`#1A1E24`) and aerospace-white (`#D8DEE6`) **Automated Freight Sorting & Mag-Loader Warehouse** with oversized pressurized roll-up cargo bay doors (`#D95B26` hazard chevrons & clamps), external modular hex-cargo pods, and a rooftop **Heavy Cargo Drone Landing Deck**.
    - **Right 35% Secondary Zone:** Full-height brushed-steel (`#88929E`) & `alphaMode: "BLEND"` translucent glass **Vertical AS/RS Container Lift & Overhead Magnetic Crane Gantry Tower**, revealing 3D stacked Aegis-7 modular cargo containers, an articulated overhead crane bridge, and amber (`#FF9500`) warning strobes.
  - `#03` (`bldg_13_r1_03.glb`) — *Twin-Gantry Open Container Yard & Mag-Loader Dock*: Parallel truss cranes straddling an open container stack yard.
  - `#04` (`bldg_13_r1_04.glb`) — *Automated Logistics Sorting Hub & Drone Hive Roof*: Octagonal sorting rotunda with a multi-port drone launch crown.
  - `#05` (`bldg_13_r1_05.glb`) — *Heavy Bulkhead Freight Depot & Shuttle Unloading Bay*: Armored freight bunker with a cantilevered shuttle cargo ramp.

#### 14. Building 14 (`bldg_14_eva_docking_pinnacle`) — Axial Zero-G Shuttle & EVA Docking Pinnacle
- **Footprint & Envelope:** `13.5m W × 11.5m D × 19.5m H` | **Target Budget:** `4,000–5,800` tris
- **Candidate Lineup (`bldg_14_r1_01.glb` .. `bldg_14_r1_05.glb`):**
  - `#01` (`bldg_14_r1_01.glb`) — *Octagonal Vertical Airlock & Docking Collar Tower*: Single vertical docking shaft with radial airlock hatches.
  - `#02` (`bldg_14_r1_02.glb`) — **Dual-Zone Split EVA Staging Terminal & Translucent Umbilical Shuttle Docking Pinnacle (Aegis-7 65/35 Signature)**:
    - **Left 65% Primary Zone:** Pressurized aerospace-white (`#D8DEE6`) and gunmetal (`#1A1E24`) **EVA Suit Staging & Decompression Terminal** featuring external dual-ring **Signal-Orange (`#D95B26`) Orbital Docking Collars**, umbilical fuel/O2 hose banks, and an elevated EVA crew staging balcony.
    - **Right 35% Secondary Zone:** Towering `19.5m` brushed-steel (`#88929E`) & `alphaMode: "BLEND"` translucent glass **Zero-G Personnel Transfer Tube & Umbilical Docking Pinnacle**, revealing 3D internal airlock lock-rings, vertical zero-G guide rails (`#00E5FF`), and an apex magnetic shuttle capture ring with amber (`#FF9500`) approach beacons.
  - `#03` (`bldg_14_r1_03.glb`) — *Twin-Arm Cantilevered Orbital Tender Berth*: Y-shaped dual docking arms extending from a central airlock core.
  - `#04` (`bldg_14_r1_04.glb`) — *Pressurized Passenger Boarding Spire & Suit Prep Hall*: Passenger concourse tower with enclosed jetway bellows.
  - `#05` (`bldg_14_r1_05.glb`) — *Heavy Hull-Lock Checkpoint & Rescue Cutter Hangar*: Armored customs & rescue hangar with a rooftop cutter cradle.

#### 15. Building 15 (`bldg_15_solar_mirror_control_pylon`) — Orbital Solar-Mirror & Mag-Shield Control Pylon
- **Footprint & Envelope:** `14.0m W × 12.0m D × 20.0m H` | **Target Budget:** `4,000–5,800` tris
- **Candidate Lineup (`bldg_15_r1_01.glb` .. `bldg_15_r1_05.glb`):**
  - `#01` (`bldg_15_r1_01.glb`) — *Octagonal Heliostat & Magnetic Shield Emitter Pylon*: Symmetrical pylon crowned by a solar mirror dish.
  - `#02` (`bldg_15_r1_02.glb`) — **Dual-Zone Split Shield Control Bunker & Translucent Gyroscopic Field-Ring Pylon (Aegis-7 65/35 Signature)**:
    - **Left 65% Primary Zone:** Armored octagonal **Heliostat Actuator & Magnetosphere Control Bunker** (`#1A1E24` / `#D8DEE6`) with angled **Articulated Solar-Mirror Louver Wings** (`#88929E` / `#00E5FF` reflective trim), high-voltage capacitor banks, and signal-orange (`#D95B26`) servicing hatches.
    - **Right 35% Secondary Zone:** Full-height (`20.0m`) brushed-steel (`#88929E`) & `alphaMode: "BLEND"` translucent glass **Gyroscopic Mag-Shield Emitter & Axial Laser-Alignment Pylon**, revealing 3D concentric glowing cyan (`#00E5FF`) and amber (`#FF9500`) field-stabilizer rings and an apex axial beam projector.
  - `#03` (`bldg_15_r1_03.glb`) — *Tri-Strut Solar Louver Actuator & Capacitor Tower*: Tripod truss tower supporting a tilted heliostat mirror array.
  - `#04` (`bldg_15_r1_04.glb`) — *Twin-Coil Magnetosphere Deflector & Laser Alignment Spire*: Dual vertical solenoid coils flanking a central laser emitter.
  - `#05` (`bldg_15_r1_05.glb`) — *Armored Axial Weather-Control & Daylight Relay Station*: Heavy climate-control bunker with a rotating mirror cupola.

---

## 5. Post-Render 5+1 Bot Voting Checklist (Vance's Set-Design Criteria)
When Gage renders `/workspace/game-project/godot/renders/buildings/bldg_XX/bldg_XX_round1_voting_sheet.png`:
1. **Silhouette Readability:** Does the 65/35 asymmetric split-mass (`#02`) separate cleanly against the curved O'Neill Cylinder vista backdrop?
2. **True `alphaMode: "BLEND"` Depth:** Are the 3D interior floors, columns, aeroponic greenery, or plasma cores clearly visible through the translucent glass curtain walls and domes?
3. **Human-Scale Movie Prop Cues:** Do the 2.1m signal-orange (`#D95B26`) airlock portals, 45° chamfered gunmetal (`#1A1E24`) plaza plinths with amber (`#FF9500`) safety strips, and rooftop pads/dishes read as authentic hard sci-fi cinema sets?
