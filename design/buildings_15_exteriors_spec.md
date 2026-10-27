# AEGIS-7 EXTERIOR STANDARD — 15 O'NEILL CYLINDER BUILDING EXTERIORS SPECIFICATION
**Architect & Lead Designer:** Sloane (`59994a08-79aa-4cb8-b3bc-26eae0fb2a6e`)  
**3D Lead & Builder:** Rook (`61237674-1923-48c9-bc64-19c16cf2501e`)  
**Engine & Lighting Director:** Gage (`6ec49577-c331-44b3-8b56-dee044ba1d84`)  
**Canonical Bible Reference:** `/workspace/game-project/MASTER_BUILDINGS_15_EXTERIORS.md`

---

## 1. Unified "Aegis-7 Exterior Standard" Architectural Language

Every building exterior (`bldg_01` through `bldg_15`) across *Cylinder Hab-7* is designed by the **same master architect** who authored our 10 interior rooms. All 75 candidate `.glb` files (`15 buildings × 5 candidates`) must obey the following non-negotiable standards:

### 1.1 Dimensional Envelope, Origin & Geometry Budget
- **Standard Building Footprint:** `12.0m W (X) × 10.0m D (Z) × 14.0m–22.0m H (Y)`
- **World Origin / Pivot:** Bottom-center of the octagonal pedestrian plaza plinth at `(0.0, 0.0, 0.0)`, `+Y` up, `+Z` main pedestrian entrance / front plaza facade.
- **Triangle Budget:** `3,200 – 5,800` triangles per `.glb` candidate (zero degenerate faces, outward-facing normals, watertight chamfered solids, embedded PBR + RGBA translucent textures).
- **Mandatory Multi-Layer Architectural Anatomy:**
  1. **Chamfered Octagonal Plaza Plinth (`Y = 0.0m – 1.2m`):** Dark anodized gunmetal titanium (`#1A1E24`) terraced base with 45° chamfered corners, recessed amber (`#FF9500`) safety perimeter strip, front entrance steps/ramps, and a signal-orange (`#D95B26`) pressurized airlock portal frame (`+Z`).
  2. **Primary Structural Mass (`Y = 1.2m – 14.0m+`):** Moulded aerospace-white composite shell cladding (`#D8DEE6`) framed by 45° chamfered gunmetal vertical ribs (`#1A1E24`), recessed carbon-slate mechanical spandrels (`#282E38`), and illuminated habitat/lab window bays (`window_grid_lit_habitat.png`).
  3. **True `alphaMode: "BLEND"` Translucent Curtain Walls, Atria & Domes (`alpha 0.28–0.40`):** Every building incorporates genuine alpha-blended translucent glass (`glass_curtainwall_cyan_translucent.png` or `glass_biodome_emerald_translucent.png`) with **real 3D interior geometry visible behind the glass** (interior floor slabs, illuminated elevator cores, hydroponic foliage columns, cryo-helices, or plasma containment coils).
  4. **Rooftop Crown, Gantry & Beacon Assembly (`Y = 14.0m – 22.0m`):** Brushed machined steel (`#88929E`) communication masts, solar/radiator fins, octagonal med-evac/drone pads (`signage_aegis7_building_marquees.png`), and glowing cyan (`#00E5FF`) / amber (`#FF9500`) sector navigation beacons.

### 1.2 Signature Candidate `#02` Rule (65/35 Aegis-7 Dual-Zone Split-Mass Architecture)
Across all 15 buildings (`bldg_01` through `bldg_15`), **Candidate `#02` (`bldg_XX_r1_02.glb`)** is the canonical **Aegis-7 65/35 Dual-Zone Split-Mass Exterior**:
- **Left / Primary Zone (`65%–68%` width, `X = -6.0m to +1.8m`):** Primary stepped octagonal structural mass in matte aerospace white (`#D8DEE6`) and dark gunmetal titanium (`#1A1E24`) with illuminated multi-story window bays (`window_grid_lit_habitat.png`), cantilevered viewing terraces, and a signal-orange (`#D95B26`) main airlock entry portal.
- **Right / Secondary Vertical Spine (`32%–35%` width, `X = +1.8m to +5.6m`):** Full-height `alphaMode: "BLEND"` translucent vertical atrium, sky-elevator shaft, bioreactor column, cryo-tower, or drone/shuttle gantry framed in brushed steel (`#88929E`) and carbon slate (`#282E38`) with visible 3D interior decks/columns and vertical cyan (`#00E5FF`) LED cove strips.

---

## 2. Exterior PBR & Emissive Texture Kit (`/workspace/game-project/assets/textures/buildings/`)

All textures are staged in `/workspace/game-project/assets/textures/buildings/` (and mirrored in `/workspace/game-project/assets/textures/`):

| Texture Filename | Format | Hex / Tint | PBR (`Metallic / Roughness`) | Architectural Role |
| :--- | :--- | :--- | :--- | :--- |
| `facade_titanium_gunmetal_hull.png` | `512×512` RGB | `#1A1E24` (`<0.9%` var) | `M: 0.78`, `R: 0.34` | Octagonal plaza plinths, 45° chamfered structural ribs, heavy bulkhead frames |
| `facade_aerospace_white_cladding.png` | `512×512` RGB | `#D8DEE6` (`<0.8%` var) | `M: 0.08`, `R: 0.30` | Primary moulded exterior shell panels, cantilevered pod cladding, hospital/Spire hulls |
| `facade_carbon_slate_spandrel.png` | `512×512` RGB | `#282E38` (`<0.9%` var) | `M: 0.58`, `R: 0.40` | Recessed inter-floor spandrels, mechanical louver decks, window mullions |
| `facade_brushed_steel_gantry.png` | `512×512` RGB | `#88929E` (`<0.9%` var) | `M: 0.90`, `R: 0.22` | Machined exterior trusses, crane arches, dish gimbals, docking collars, roof masts |
| `glass_curtainwall_cyan_translucent.png` | `512×512` RGBA | `#16384C` / `#00E5FF` (`alpha 0.30–0.55`) | `M: 0.10`, `R: 0.12`, `BLEND` | Translucent curtain walls, sky-elevator shafts, command/lab atria (reveals 3D interior floors) |
| `glass_biodome_emerald_translucent.png` | `512×512` RGBA | `#184A3E` / `#00E5C0` (`alpha 0.28–0.50`) | `M: 0.08`, `R: 0.14`, `BLEND` | Geodesic/octagonal conservatory domes, algae bio-scrubber columns, park canopies |
| `window_grid_lit_habitat.png` | `512×512` RGB | `#0E131A` + `#FFE4B5`/`#00E5FF` | `M: 0.15`, `R: 0.25`, `Emissive` | Calm, architecturally proportioned illuminated recessed window bays for towers/hospitals/labs |
| `signage_aegis7_building_marquees.png` | `512×512` RGB | `#0A0E14` + `#00E5FF`/`#FF9500` | `M: 0.10`, `R: 0.20`, `Emissive` | Sector marquees (`HAB-01..15`, `COMMAND CITADEL`, `MAG-LEV TRANSIT`, `MED-EVAC PAD 04`) & pad reticles |
| `accent_safety_orange.png` | `512×512` RGB | `#D95B26` | `M: 0.35`, `R: 0.38` | Airlock portal collars, docking clamps, crane hooks, emergency blast doors |
| `led_cyan_strip.png` | `256×256` RGB | `#00E5FF` | Emissive (`1.8–2.4`) | Vertical architectural cove ribs, curtain-wall edge highlights, beacon rings |
| `led_amber_strip.png` | `256×256` RGB | `#FF9500` | Emissive (`1.6–2.2`) | Octagonal plaza plinth safety perimeter strips, helipad/cargo guidance bars |
| `led_uv_violet.png` | `256×256` RGB | `#7B5CFF` | Emissive (`1.6–2.2`) | Cryo-pharmacy, biolab, UV-sterilization & quantum telemetry accents |
| `foliage_aeroponic_herbs.png` | `512×512` RGB | `#2E8B57` | `M: 0.02`, `R: 0.65` | 3D interior aeroponic planters, vertical farm columns, and conservatory greenery |

---

## 3. All 15 Building Exteriors & 5-Candidate Specifications (`bldg_01` – `bldg_15`)

### DISTRICT I — RESIDENTIAL & CIVIC TERRACE SECTOR (`bldg_01` – `bldg_05`)

#### 1. Building 01 (`bldg_01_hab_spire`) — Aegis-7 Modular Crew Habitat Tower
- **Output Path:** `/workspace/game-project/assets/glb/buildings/bldg_01/bldg_01_r1_01.glb` .. `bldg_01_r1_05.glb`
- **Envelope:** `12.0m W × 10.0m D × 18.5m H` | **Target Tris:** `3,800–5,200`
- **Candidates:**
  - **`#01` (`bldg_01_r1_01.glb`) — Symmetric Octagonal Stepped Pod Spire:** Central 6-tier stepped octagonal tower in `#D8DEE6` aerospace white with symmetric cantilevered sleep-pod bays, warm circadian `window_grid_lit_habitat.png` bands, and a central rooftop comms needle.
  - **`#02` (`bldg_01_r1_02.glb`) — Dual-Zone Split Residential Pod Spire & Translucent Sky-Elevator Atrium Tower (Aegis-7 65/35 Signature):** Left 65% stepped 6-story octagonal aerospace-white habitat tower with cantilevered crew pod bays, warm circadian window grids, and a `#D95B26` ground airlock lobby; Right 35% full-height (`18.5m`) `alphaMode: "BLEND"` translucent cyan glass sky-elevator atrium tower (`glass_curtainwall_cyan_translucent.png`) revealing 6 interior illuminated elevator landings, dual vertical guide rails, and a rooftop sky-lounge crown.
  - **`#03` (`bldg_01_r1_03.glb`) — Twin-Cantilevered Hex-Hive Terraced Apartment Block:** Dual interlocking hexagonal residential wings joined by 3 mid-air translucent glass skybridges over a sunken plaza courtyard.
  - **`#04` (`bldg_01_r1_04.glb`) — Curved Cylinder-Slope Terraced Habitat Ziggurat:** Stepped 5-level setback ziggurat with deep planted terrace balconies (`foliage_aeroponic_herbs.png`) and sloped panoramic skylights facing the cylinder axis.
  - **`#05` (`bldg_01_r1_05.glb`) — Suspended Modular Pod-Cluster & Skybridge Tower:** Brushed-steel (`#88929E`) exo-truss spine suspending 8 plug-in octagonal crew habitat modules above an open pedestrian concourse.

#### 2. Building 02 (`bldg_02_transit_rotunda`) — Elevated Mag-Lev & Ring Transit Rotunda
- **Output Path:** `/workspace/game-project/assets/glb/buildings/bldg_02/bldg_02_r1_01.glb` .. `bldg_02_r1_05.glb`
- **Envelope:** `12.5m W × 10.0m D × 15.0m H` | **Target Tris:** `3,600–5,000`
- **Candidates:**
  - **`#01` (`bldg_02_r1_01.glb`) — Octagonal Central Mag-Lev Concourse Rotunda:** Symmetric vaulted octagonal transit terminal bisected at `Y = 5.5m` by an elevated horizontal mag-lev guideway deck and translucent boarding canopy.
  - **`#02` (`bldg_02_r1_02.glb`) — Dual-Zone Split Mag-Lev Station Hall & Vertical Shuttle-Pod Boarding Tower (Aegis-7 65/35 Signature):** Left 65% aerospace-white & gunmetal vaulted concourse hall featuring an elevated `Y = 5.2m` cantilevered mag-lev guideway track, docked streamlined transit car silhouette, and glowing `MAG-LEV TRANSIT` marquee; Right 35% full-height (`15.0m`) translucent vertical commuter transfer tower revealing 4 interior escalator/elevator mezzanine decks and a rooftop shuttle-pod pad.
  - **`#03` (`bldg_02_r1_03.glb`) — Twin-Tube Elevated Guideway Overpass Terminal:** Dual parallel translucent transit tubes supported on heavy 45° chamfered gunmetal portal piers with a central ticketing mezzanine.
  - **`#04` (`bldg_02_r1_04.glb`) — Cantilevered Ring-Line Commuter Hub & Control Pylon:** Asymmetric high-line platform cantilevered from a single carbon-slate traffic control tower with amber track-status bars.
  - **`#05` (`bldg_02_r1_05.glb`) — Tri-Level Rotary Transit Interchange Plaza:** Circular three-tier hub uniting ground pedestrian ramps, mid-level mag-lev rails, and upper air-taxi docking rings.

#### 3. Building 03 (`bldg_03_culinary_atrium`) — Terraced Synthesizer & Culinary Commons Pavilion
- **Output Path:** `/workspace/game-project/assets/glb/buildings/bldg_03/bldg_03_r1_01.glb` .. `bldg_03_r1_05.glb`
- **Envelope:** `12.0m W × 10.0m D × 14.5m H` | **Target Tris:** `3,600–4,900`
- **Candidates:**
  - **`#01` (`bldg_03_r1_01.glb`) — Octagonal Glass-Crowned Mess Hall Pavilion:** Two-story aerospace-white dining pavilion topped by a centered octagonal translucent glass lantern dome with warm interior dining tables visible.
  - **`#02` (`bldg_03_r1_02.glb`) — Dual-Zone Split Culinary Dining Pavilion & Full-Height Translucent Aeroponic Herb Tower (Aegis-7 65/35 Signature):** Left 65% two-tier terraced dining hall in `#D8DEE6` aerospace white with wrap-around translucent promenade dining windows and an open upper balcony; Right 35% `14.5m` tall `alphaMode: "BLEND"` emerald/cyan translucent vertical aeroponic farm & nutrient synthesizer tower (`glass_biodome_emerald_translucent.png`) displaying 5 illuminated interior green herb tiers (`foliage_aeroponic_herbs.png`) feeding directly into the galley.
  - **`#03` (`bldg_03_r1_03.glb`) — Terraced Promenade Bistro & Zero-G Beverage Rotunda:** Stepped open-air dining decks wrapping a glowing cyan cylindrical beverage synthesizer rotunda.
  - **`#04` (`bldg_03_r1_04.glb`) — Twin-Wing Civic Refectory & Solar-Lit Courtyard:** U-shaped communal mess complex framing a glass-roofed central botanical dining atrium.
  - **`#05` (`bldg_03_r1_05.glb`) — Cantilevered Overlook Dining Deck & Ration Silo Complex:** Dramatic cantilevered panoramic dining deck balanced by 3 brushed-steel nutritional storage silos.

#### 4. Building 04 (`bldg_04_medical_trauma_center`) — Orbital Trauma & Biomonitor Medical Complex
- **Output Path:** `/workspace/game-project/assets/glb/buildings/bldg_04/bldg_04_r1_01.glb` .. `bldg_04_r1_05.glb`
- **Envelope:** `12.0m W × 10.0m D × 16.5m H` | **Target Tris:** `3,800–5,200`
- **Candidates:**
  - **`#01` (`bldg_04_r1_01.glb`) — Octagonal Med-Bay Clinical Pavilion with Rooftop Med-Evac Pad:** Crisp surgical aerospace-white octagonal hospital block crowned by a centered octagonal `MED-EVAC PAD 04` helipad.
  - **`#02` (`bldg_04_r1_02.glb`) — Dual-Zone Split Trauma Hospital Wing & Translucent UV-Sterile Cryo-Pharmacy Tower (Aegis-7 65/35 Signature):** Left 65% 4-story surgical aerospace-white (`#D8DEE6`) clinical wing with ice-white/cyan hospital window grids, `#D95B26` emergency ambulance airlock bay, and a cantilevered rooftop octagonal `MED-EVAC PAD 04` (`signage_aegis7_building_marquees.png`) with amber/cyan approach lights; Right 35% full-height (`16.5m`) translucent UV-sterile cryo-pharmacy & biomonitor tower revealing interior violet (`#7B5CFF`) and cyan (`#00E5FF`) sterile carousel columns.
  - **`#03` (`bldg_04_r1_03.glb`) — Twin-Dome Bio-Quarantine & Triage Center:** Two isolated positive-pressure translucent containment domes linked by a central decontamination airlock spine.
  - **`#04` (`bldg_04_r1_04.glb`) — Stepped Aerospace-White Surgical Institute & Ambulance Dock:** Terraced 4-level medical facility with recessed ground-level pressurized ambulance bays.
  - **`#05` (`bldg_04_r1_05.glb`) — Cantilevered Zero-G Recovery Sanatorium & Telemetry Spire:** Elevated zero-G recuperation pod ring supported above a clinical triage base.

#### 5. Building 05 (`bldg_05_celestial_promenade_dome`) — Zero-G Observation & Recreation Dome
- **Output Path:** `/workspace/game-project/assets/glb/buildings/bldg_05/bldg_05_r1_01.glb` .. `bldg_05_r1_05.glb`
- **Envelope:** `12.0m W × 10.5m D × 16.0m H` | **Target Tris:** `3,800–5,400`
- **Candidates:**
  - **`#01` (`bldg_05_r1_01.glb`) — Faceted Octagonal Geodesic Observation Dome:** Large central chamfered octagonal translucent glass dome (`glass_curtainwall_cyan_translucent.png`) revealing an interior circular celestial bar and holo-orrery.
  - **`#02` (`bldg_05_r1_02.glb`) — Dual-Zone Split Stargazer Lounge Dome & Illuminated Zero-G Ascent Tower (Aegis-7 65/35 Signature):** Left 65% faceted octagonal translucent observation dome set in a gunmetal & aerospace-white cradling ring with visible interior lounge tiers and glowing cyan/violet bar core; Right 35% `16.0m` tall translucent Zero-G vertical ascent tube & observation crow's-nest spire with illuminated floating ring baffles inside.
  - **`#03` (`bldg_05_r1_03.glb`) — Twin-Ringed Panoramabridge & Amphitheater Pavilion:** Dual inclined observation rings framing a stepped civic amphitheater and holo-stage.
  - **`#04` (`bldg_05_r1_04.glb`) — Terraced Civic Park Conservatory & Holo-Fountain Rotunda:** Open terraced park pavilion with emerald glass canopies and a glowing cyan central water/light column.
  - **`#05` (`bldg_05_r1_05.glb`) — Cantilevered Horizon Viewing Deck & Celestial Bar Complex:** Long cantilevered glass-floored skywalk jutting out from an octagonal recreation hall.

---

### DISTRICT II — AGRI-BIOSPHERE & RESEARCH SECTOR (`bldg_06` – `bldg_10`)

#### 6. Building 06 (`bldg_06_hydroponic_biodome`) — Aeroponic & Bio-Scrubber Conservatory Complex
- **Output Path:** `/workspace/game-project/assets/glb/buildings/bldg_06/bldg_06_r1_01.glb` .. `bldg_06_r1_05.glb`
- **Envelope:** `12.0m W × 10.5m D × 16.5m H` | **Target Tris:** `3,800–5,400`
- **Candidates:**
  - **`#01` (`bldg_06_r1_01.glb`) — Tri-Dome Geodesic Botanical Conservatory:** Cluster of three interconnected octagonal emerald-tinted biodomes (`glass_biodome_emerald_translucent.png`) filled with interior greenery tiers.
  - **`#02` (`bldg_06_r1_02.glb`) — Dual-Zone Split Greenhouse Conservatory & Full-Height Translucent O2 Algae Bio-Scrubber Tower (Aegis-7 65/35 Signature):** Left 65% vaulted octagonal emerald-glass conservatory hall framed in `#D8DEE6` aerospace white and `#1A1E24` gunmetal ribs with 3 visible terraced interior crop beds (`foliage_aeroponic_herbs.png`); Right 35% `16.5m` tall translucent vertical O2 algae bio-scrubber column housing glowing cyan/emerald photobioreactor tubes and rooftop oxygen vents.
  - **`#03` (`bldg_06_r1_03.glb`) — Stepped Agricultural Ziggurat & UV-Grow Terrace:** 4-tier stepped agricultural pyramid with violet (`#7B5CFF`) UV grow-light canopies on each setback terrace.
  - **`#04` (`bldg_06_r1_04.glb`) — Twin-Cylinder Vertical Farm & Nutrient Silo Array:** Two tall translucent rotary drum greenhouses flanked by brushed-steel nutrient tanks.
  - **`#05` (`bldg_06_r1_05.glb`) — Octagonal Biosphere Rotunda & Canopy Skywalk:** High-vaulted botanical dome encircled by an exterior brushed-steel inspection catwalk.

#### 7. Building 07 (`bldg_07_atmospheric_processor`) — Sector Atmospheric & O2/CO2 Scrubber Plant
- **Output Path:** `/workspace/game-project/assets/glb/buildings/bldg_07/bldg_07_r1_01.glb` .. `bldg_07_r1_05.glb`
- **Envelope:** `12.0m W × 10.0m D × 17.5m H` | **Target Tris:** `3,600–5,200`
- **Candidates:**
  - **`#01` (`bldg_07_r1_01.glb`) — Octagonal Air-Exchange Intake & Turbine Hall:** Heavy carbon-slate and aerospace-white industrial hall with large octagonal intake louvers and twin rooftop exhaust stacks.
  - **`#02` (`bldg_07_r1_02.glb`) — Dual-Zone Split Atmospheric Processor Hall & Translucent Cryo-O2 Distillation Tower (Aegis-7 65/35 Signature):** Left 65% stepped carbon-slate (`#282E38`) and aerospace-white (`#D8DEE6`) turbine & CO2 scrubber hall with chamfered intake plenums and amber status strips; Right 35% `17.5m` tall `alphaMode: "BLEND"` translucent cryo-O2 fractionation tower (`glass_curtainwall_cyan_translucent.png`) revealing stacked interior glowing cyan condenser plates and brushed-steel piping manifolds.
  - **`#03` (`bldg_07_r1_03.glb`) — Quad-Stack Venturi Scrubber & Thermal Louver Plant:** Four vertical brushed-steel Venturi scrubber chimneys rising from a fortified gunmetal base.
  - **`#04` (`bldg_07_r1_04.glb`) — Twin-Sphere Liquid-Oxygen Storage & Barometric Station:** Dual spherical cryogenic LOX tanks cradled in an octagonal steel truss gantry beside a telemetry control block.
  - **`#05` (`bldg_07_r1_05.glb`) — Heavy Industrial Spin-Filter & Humidity Control Complex:** Low-slung high-volume air handler with inclined radiator fins and illuminated barometric gauges.

#### 8. Building 08 (`bldg_08_astrometry_observatory`) — Deep-Space Astrometry & Sensor Array Complex
- **Output Path:** `/workspace/game-project/assets/glb/buildings/bldg_08/bldg_08_r1_01.glb` .. `bldg_08_r1_05.glb`
- **Envelope:** `12.0m W × 10.0m D × 18.0m H` | **Target Tris:** `3,800–5,400`
- **Candidates:**
  - **`#01` (`bldg_08_r1_01.glb`) — Octagonal Clamshell Optical Telescope Observatory:** Aerospace-white octagonal drum topped by a rotatable slotted observatory dome and exposed brushed-steel telescope barrel.
  - **`#02` (`bldg_08_r1_02.glb`) — Dual-Zone Split Astrometry Research Lab & Rotating Deep-Space Telemetry Dish Tower (Aegis-7 65/35 Signature):** Left 65% 4-story aerospace-white & carbon-slate astrometry research lab with angled translucent star-charting bay windows (`glass_curtainwall_cyan_translucent.png`) revealing an interior holo-orrery core; Right 35% `18.0m` tall translucent sensor wave-guide spine crowned by a gimbaled octagonal brushed-steel deep-space telemetry dish (`#88929E`) with a glowing cyan feed horn.
  - **`#03` (`bldg_08_r1_03.glb`) — Tri-Dish Interferometer & Quantum Comms Array Building:** Stepped sensor bunker supporting three synchronized parabolic interferometer dishes on angled pylons.
  - **`#04` (`bldg_08_r1_04.glb`) — Stepped Sensor Dome & Subspace Beacon Annex:** Octagonal lab complex with a glowing violet/cyan quantum transceiver obelisk.
  - **`#05` (`bldg_08_r1_05.glb`) — Cantilevered Deep-Sky Spectrograph & Holo-Charting Center:** Angled spectrograph tube cantilevered at 35° from a multi-tier research pavilion.

#### 9. Building 09 (`bldg_09_aquifer_pumping_station`) — Ring-Gravity Water Reclamation & Aquifer Cascade
- **Output Path:** `/workspace/game-project/assets/glb/buildings/bldg_09/bldg_09_r1_01.glb` .. `bldg_09_r1_05.glb`
- **Envelope:** `12.0m W × 10.0m D × 16.5m H` | **Target Tris:** `3,600–5,100`
- **Candidates:**
  - **`#01` (`bldg_09_r1_01.glb`) — Octagonal Hydro-Filtration Hall & Settling Basin:** Central pump house flanked by translucent cyan water-settling basins in the plaza plinth.
  - **`#02` (`bldg_09_r1_02.glb`) — Dual-Zone Split Centrifugal Pumping Plant & Translucent Illuminated Water-Column Tower (Aegis-7 65/35 Signature):** Left 65% aerospace-white & gunmetal centrifugal hydro-pumping hall with brushed-steel aqueduct manifolds and `#D95B26` maintenance hatches; Right 35% `16.5m` tall `alphaMode: "BLEND"` translucent hydro-head pressure & UV-purification water column (`glass_curtainwall_cyan_translucent.png`) revealing illuminated cyan/violet vortex filtration rings inside.
  - **`#03` (`bldg_09_r1_03.glb`) — Terraced Cascade Spillway & UV-Purification Complex:** Stepped architectural waterfall terraces descending down a 4-level filtration ziggurat.
  - **`#04` (`bldg_09_r1_04.glb`) — Twin-Silo Greywater Recovery & Mineral Dosing Station:** Dual vertical stainless-steel hydro-silos connected by a glass-walled control bridge.
  - **`#05` (`bldg_09_r1_05.glb`) — Heavy Conduit Manifold & Pressure-Regulator Building:** Industrial ring-main pumping station with arched exterior pipeline buttresses.

#### 10. Building 10 (`bldg_10_cryo_seed_vault`) — Colonial Cryo-Genetics & Seed Archive Vault
- **Output Path:** `/workspace/game-project/assets/glb/buildings/bldg_10/bldg_10_r1_01.glb` .. `bldg_10_r1_05.glb`
- **Envelope:** `12.0m W × 10.0m D × 17.0m H` | **Target Tris:** `3,600–5,200`
- **Candidates:**
  - **`#01` (`bldg_10_r1_01.glb`) — Armored Octagonal Sub-Zero Gene Bank Monolith:** Tapered gunmetal and aerospace-white armored vault monolith with narrow violet/cyan cryo-slit windows.
  - **`#02` (`bldg_10_r1_02.glb`) — Dual-Zone Split Armored Seed Archive Vault & Translucent Cryo-Stasis Helix Tower (Aegis-7 65/35 Signature):** Left 65% heavily buttressed 45° chamfered gunmetal (`#1A1E24`) and aerospace-white (`#D8DEE6`) cryo-vault bunker with a heavy `#D95B26` blast-door airlock and `BIOSPHERE // CRYO-10` marquee; Right 35% `17.0m` tall `alphaMode: "BLEND"` translucent cryo-stasis tower revealing stacked interior violet (`#7B5CFF`) and cyan (`#00E5FF`) genetic sample carousels and rooftop cryogenic radiator fins.
  - **`#03` (`bldg_10_r1_03.glb`) — Subterranean-Plinth Cryogenic Silo & Radiator Array:** Deep recessed cryo-well crown surrounded by 6 vertical heat-rejection radiator blades.
  - **`#04` (`bldg_10_r1_04.glb`) — Twin-Buttressed Bio-Preservation Bunker & Lab Wing:** Dual armored archive vaults joined by an elevated glazed genetics laboratory.
  - **`#05` (`bldg_10_r1_05.glb`) — Cantilevered Deep-Freeze Repository & Security Portal:** Elevated thermal-isolated vault box suspended on low-conductivity titanium struts.

---

### DISTRICT III — COMMAND, POWER & INDUSTRIAL PORT SECTOR (`bldg_11` – `bldg_15`)

#### 11. Building 11 (`bldg_11_citadel_command_hq`) — Cylinder Hab-7 Central Command & Telemetry Citadel
- **Output Path:** `/workspace/game-project/assets/glb/buildings/bldg_11/bldg_11_r1_01.glb` .. `bldg_11_r1_05.glb`
- **Envelope:** `12.5m W × 10.5m D × 21.5m H` (Tallest landmark spire) | **Target Tris:** `4,200–5,800`
- **Candidates:**
  - **`#01` (`bldg_11_r1_01.glb`) — Monumental Octagonal Command Spire & Bridge Crown:** Symmetric 8-story tapered octagonal command tower crowned by a 360° cantilevered glass bridge deck.
  - **`#02` (`bldg_11_r1_02.glb`) — Dual-Zone Split Command Citadel Spire & Translucent Quantum Flight-Director Tower (Aegis-7 65/35 Signature):** Left 65% monumental 7-tier stepped octagonal aerospace-white & gunmetal Citadel tower crowned by a cantilevered octagonal Overwatch Command Bridge and `COMMAND CITADEL` marquee; Right 35% `21.5m` tall `alphaMode: "BLEND"` translucent Quantum Flight-Director & Holo-Telemetry Spine (`glass_curtainwall_cyan_translucent.png`) revealing stacked interior glowing cyan holo-projection rings, high-speed command lift, and a twin-array telemetry mast.
  - **`#03` (`bldg_11_r1_03.glb`) — Twin-Obelisk Sector Governance & Defense HQ:** Two slender octagonal towers linked at the base, mid-deck, and crown by translucent command skybridges.
  - **`#04` (`bldg_11_r1_04.glb`) — Stepped Pyramidion Overwatch Citadel & Holo-Beacon:** Tiered command pyramidion with an open top-deck holographic cylinder projector.
  - **`#05` (`bldg_11_r1_05.glb`) — Cantilevered High-Command Bridge & Comms Mast Complex:** Forward-swept command bridge jutting dramatically over the central plaza from a heavy gunmetal core.

#### 12. Building 12 (`bldg_12_fusion_reactor_complex`) — D-He3 Fusion Power & Spin-Drive Reactor Hall
- **Output Path:** `/workspace/game-project/assets/glb/buildings/bldg_12/bldg_12_r1_01.glb` .. `bldg_12_r1_05.glb`
- **Envelope:** `12.5m W × 10.5m D × 18.5m H` | **Target Tris:** `4,000–5,600`
- **Candidates:**
  - **`#01` (`bldg_12_r1_01.glb`) — Octagonal Magnetic-Confinement Fusion Reactor Dome:** Heavy gunmetal and aerospace-white octagonal containment dome ringed by 8 external cryo-coolant buttresses.
  - **`#02` (`bldg_12_r1_02.glb`) — Dual-Zone Split Fusion Containment Hall & Translucent 5-Coil Plasma Pinch Tower (Aegis-7 65/35 Signature):** Left 65% armored octagonal D-He3 turbine & power-conditioning hall in `#1A1E24` gunmetal and `#D8DEE6` aerospace white with heavy radiator fins and amber hazard strips; Right 35% `18.5m` tall `alphaMode: "BLEND"` translucent magnetic-confinement plasma column (`glass_curtainwall_cyan_translucent.png`) with 5 exterior brushed-steel toroidal magnetic pinch rings encircling a glowing cyan/amber vertical plasma core inside.
  - **`#03` (`bldg_12_r1_03.glb`) — Twin-Core Toroidal Tokamak & Radiator Fin Complex:** Dual octagonal tokamak chambers flanked by tall vertical graphene radiator wings.
  - **`#04` (`bldg_12_r1_04.glb`) — Heavy Armored Spin-Drive Impulse Plant & Cryo Bay:** Fortified spin-gravity drive house with massive inclined thrust-vector reaction struts.
  - **`#05` (`bldg_12_r1_05.glb`) — High-Voltage Substation & Plasma Conduit Gantry Hall:** Industrial power distribution hall topped by brushed-steel superconducting busbar gantries.

#### 13. Building 13 (`bldg_13_cargo_logistics_port`) — High-Bay Intermodal Cargo & Drone Gantry Terminal
- **Output Path:** `/workspace/game-project/assets/glb/buildings/bldg_13/bldg_13_r1_01.glb` .. `bldg_13_r1_05.glb`
- **Envelope:** `12.5m W × 10.5m D × 17.0m H` | **Target Tris:** `3,800–5,400`
- **Candidates:**
  - **`#01` (`bldg_13_r1_01.glb`) — Octagonal High-Bay Freight Warehouse & Crane Arch:** High-clearance logistics warehouse spanned by an exterior brushed-steel bridge crane arch.
  - **`#02` (`bldg_13_r1_02.glb`) — Dual-Zone Split Intermodal Cargo Terminal & Translucent ISO Container / Drone Gantry Tower (Aegis-7 65/35 Signature):** Left 65% high-bay aerospace-white & carbon-slate logistics warehouse with oversized `#D95B26` signal-orange cargo bay roll-doors and a rooftop octagonal `DRONE-13` landing pad (`signage_aegis7_building_marquees.png`); Right 35% `17.0m` tall brushed-steel & `alphaMode: "BLEND"` translucent vertical automated container AS/RS tower revealing stacked interior modular cargo pods and an upper drone launch chute.
  - **`#03` (`bldg_13_r1_03.glb`) — Twin-Gantry Open Container Yard & Mag-Loader Dock:** Dual overhead crane gantries straddling stacked octagonal freight containers and a dispatch tower.
  - **`#04` (`bldg_13_r1_04.glb`) — Automated Logistics Sorting Hub & Drone Hive Roof:** Octagonal sorting facility with 6 illuminated hexagonal drone launch bays on the roof.
  - **`#05` (`bldg_13_r1_05.glb`) — Heavy Bulkhead Freight Depot & Shuttle Unloading Bay:** Industrial freight terminal with a cantilevered heavy cargo loading apron.

#### 14. Building 14 (`bldg_14_eva_docking_pinnacle`) — Axial Zero-G Shuttle & EVA Docking Pinnacle
- **Output Path:** `/workspace/game-project/assets/glb/buildings/bldg_14/bldg_14_r1_01.glb` .. `bldg_14_r1_05.glb`
- **Envelope:** `12.0m W × 10.0m D × 19.5m H` | **Target Tris:** `3,800–5,500`
- **Candidates:**
  - **`#01` (`bldg_14_r1_01.glb`) — Octagonal Vertical Airlock & Docking Collar Tower:** Tall vertical airlock spire with 4 radial `#D95B26` signal-orange shuttle docking collars.
  - **`#02` (`bldg_14_r1_02.glb`) — Dual-Zone Split EVA Staging Terminal & Translucent Umbilical Shuttle Docking Pinnacle (Aegis-7 65/35 Signature):** Left 65% stepped aerospace-white & gunmetal EVA suit prep & decompression hall with pressurized ground airlocks and equipment galleries; Right 35% `19.5m` tall `alphaMode: "BLEND"` translucent vertical zero-G transfer shaft & brushed-steel docking pinnacle featuring cantilevered `#D95B26` docking collars, visible interior transfer cages, and cyan approach strobes.
  - **`#03` (`bldg_14_r1_03.glb`) — Twin-Arm Cantilevered Orbital Tender Berth:** Y-shaped twin docking arms extending from a central pressurized crew concourse.
  - **`#04` (`bldg_14_r1_04.glb`) — Pressurized Passenger Boarding Spire & Suit Prep Hall:** Sleek aerospace-white boarding tower with articulated telescopic boarding bridges.
  - **`#05` (`bldg_14_r1_05.glb`) — Heavy Hull-Lock Checkpoint & Rescue Cutter Hangar:** Fortified EVA rescue base with an elevated launch cradle and beacon mast.

#### 15. Building 15 (`bldg_15_solar_mirror_control_pylon`) — Orbital Solar-Mirror & Mag-Shield Control Pylon
- **Output Path:** `/workspace/game-project/assets/glb/buildings/bldg_15/bldg_15_r1_01.glb` .. `bldg_15_r1_05.glb`
- **Envelope:** `12.0m W × 10.0m D × 20.0m H` | **Target Tris:** `3,800–5,500`
- **Candidates:**
  - **`#01` (`bldg_15_r1_01.glb`) — Octagonal Heliostat & Magnetic Shield Emitter Pylon:** Central armored pylon crowned by angled solar-mirror actuator wings and a cyan shield ring.
  - **`#02` (`bldg_15_r1_02.glb`) — Dual-Zone Split Shield Control Bunker & Translucent Gyroscopic Field-Ring Pylon (Aegis-7 65/35 Signature):** Left 65% 45°-buttressed aerospace-white & carbon-slate heliostat control bunker with angled solar-alignment louver arrays and telemetry windows; Right 35% `20.0m` tall `alphaMode: "BLEND"` translucent wave-guide pylon encircled by 3 inclined brushed-steel gyroscopic magnetic-shield emitter rings and a glowing cyan/violet apex beacon.
  - **`#03` (`bldg_15_r1_03.glb`) — Tri-Strut Solar Louver Actuator & Capacitor Tower:** Three heavy gunmetal tripod struts supporting a high-altitude mirror alignment laser dome.
  - **`#04` (`bldg_15_r1_04.glb`) — Twin-Coil Magnetosphere Deflector & Laser Alignment Spire:** Dual vertical induction coils flanking a central optical alignment hall.
  - **`#05` (`bldg_15_r1_05.glb`) — Armored Axial Weather-Control & Daylight Relay Station:** Terraced environmental control station with rotating heliostat vanes on the roof.

---

## 4. Godot 4 Exterior Showcase, District & Metropolis Scenes

### 4.1 Individual Building 5-Candidate Voting Sheets (`bldg_01` – `bldg_15`)
- **Render Output Directory:** `/workspace/game-project/godot/renders/buildings/bldg_XX/`
  - Individual 1080p renders: `bldg_XX_r1_01.png` .. `bldg_XX_r1_05.png` (`1920×1080`)
  - 5-Panel Voting Sheet: `bldg_XX_round1_voting_sheet.png`
- **Showcase Camera & Lighting Standard:**
  - Three-quarter architectural hero angle (`Cam Pos: (16.5, 13.5, 19.5)`, looking at `(0.0, 7.5, 0.0)`, `FOV: 38°`) so both the 65% primary mass and 35% translucent atrium/tower read with crystal clarity.
  - **Solar Mirror Key Light (`DirectionalLight3D`):** Warm orbital daylight (`#FFF6E8`, `energy: 1.35`, pitch `-42°`, yaw `+35°`, soft shadows enabled).
  - **Cylinder Earthlight Bounce Fill (`DirectionalLight3D`):** Cool atmospheric sky fill from the opposite cylinder land-strip (`#7CC8FF`, `energy: 0.55`, pitch `-25°`, yaw `-140°`).
  - **Rim / Backlight (`DirectionalLight3D`):** Crisp architectural silhouette rim (`#00E5FF`, `energy: 0.40`, pitch `-15°`, yaw `+165°`).
  - **WorldEnvironment:** ACES Filmic tonemapping (`exposure: 1.05`), subtle SSAO (`radius: 1.2`, `intensity: 0.75`), SSR enabled for glass/plinth reflections, subtle Glow (`intensity: 0.35`, `bloom: 0.08`) so window grids and cyan/amber strips glow cleanly without washout.

### 4.2 Three District Showcase Scenes (`godot/scenes/buildings/`)
1. **`district_01_residential_civic.tscn` (`/workspace/game-project/godot/renders/buildings/district_01/`):**
   - Places locked `#02` winners for **Buildings 01–05** (`bldg_01_winner.glb` .. `bldg_05_winner.glb`) along a `75m × 45m` curved O'Neill Cylinder Civic Boulevard (`X = -28m, -14m, 0m, +14m, +28m` with staggered `Z = -6m / +6m` plaza setbacks), joined by illuminated cyan/amber pedestrian promenades, elevated mag-lev guideway rails, and aeroponic planter islands.
2. **`district_02_agri_research.tscn` (`/workspace/game-project/godot/renders/buildings/district_02/`):**
   - Places locked `#02` winners for **Buildings 06–10** (`bldg_06_winner.glb` .. `bldg_10_winner.glb`) across a `75m × 45m` Biosphere & Research Terrace featuring illuminated hydro-reclamation canals (`glass_curtainwall_cyan_translucent.png`), botanical walkways, and deep-space sensor lines.
3. **`district_03_command_industrial.tscn` (`/workspace/game-project/godot/renders/buildings/district_03/`):**
   - Places locked `#02` winners for **Buildings 11–15** (`bldg_11_winner.glb` .. `bldg_15_winner.glb`) anchored by the `21.5m` Central Command Citadel (`bldg_11`) at center plaza, flanked by the Fusion Reactor Hall (`bldg_12`), Cargo Logistics Port (`bldg_13`), EVA Docking Pinnacle (`bldg_14`), and Solar-Mirror Shield Pylon (`bldg_15`).

### 4.3 Grand 15-Building O'Neill Cylinder Metropolis Scene (`cylinder_hab7_metropolis.tscn`)
- **Scene Path:** `/workspace/game-project/godot/scenes/buildings/cylinder_hab7_metropolis.tscn`
- **Render Output Directory:** `/workspace/game-project/godot/renders/buildings/metropolis/`
  - `metropolis_cam1_grand_overview.png` (`1920×1080` sweeping elevated vista across all 3 districts and all 15 buildings curving upward along the O'Neill Cylinder terrain deck)
  - `metropolis_cam2_boulevard_axis.png` (`1920×1080` low-angle architectural promenade view looking down the central mag-lev & hydro-canal boulevard toward the Command Citadel spire)
  - `metropolis_cam3_cylinder_horizon.png` (`1920×1080` dramatic cross-sector skyline view highlighting the unified 65/35 Aegis-7 silhouettes and glowing translucent towers)
  - `cylinder_hab7_metropolis_showcase_sheet.png` (composite multi-angle Metropolis Master Sheet)
- **Curved O'Neill Cylinder Terrain Architecture:**
  - The Metropolis ground deck (`140m × 90m`) incorporates gentle upward cylinder curvature (`+Y` rise along `±X` and `-Z` flanks) with an overhead illuminated O'Neill Cylinder land-strip/solar-mirror sky backdrop (`vista_oneill_cylinder_interior.png`), uniting District I (West Terrace), District II (Central Biosphere Canal), and District III (East Command & Port Plaza) into one seamless single-architect orbital city.

---

## 5. Phase 3 Addendum — Street-Plaza Movie Props (`prop_01`–`prop_05`) & District IV Building Exteriors (`bldg_16`–`bldg_20`)

### 5.1 Phase 3 Signage, OLED & Translucent Holo-Glass Texture Suite (`/workspace/game-project/assets/textures/buildings/` & `/workspace/game-project/assets/textures/`)
All Phase 3 textures obey the `<1.2%` micro-noise Aegis-7 spacecraft surface standard and are staged in both `/workspace/game-project/assets/textures/buildings/` and `/workspace/game-project/assets/textures/`:

| Texture Filename | Format | Hex / Tint | PBR (`Metallic / Roughness`) | Architectural & Prop Role |
| :--- | :--- | :--- | :--- | :--- |
| `oled_holo_wayfinding_map.png` | `512×512` RGB | `#0A0E14` + `#00E5FF`/`#FF9500`/`#7B5CFF`/`#00E5C0` | `M: 0.08`, `R: 0.18`, `Emissive` | Axial O'Neill Cylinder Hab-7 3D sector map, `0.98g SPIN` readout, amber `"YOU ARE HERE // PLAZA"` beacon, and Districts I–IV directory HUD for `prop_02` Holo-Wayfinding Kiosks and plaza concourses |
| `signage_district4_marquees.png` | `512×512` RGB | `#0A0E14` + `#00E5FF`/`#FF9500`/`#7B5CFF`/`#00E5C0` | `M: 0.10`, `R: 0.20`, `Emissive` | High-contrast marquee & badge atlas for District IV buildings (`BLDG-16` Shipyard Drydock, `BLDG-17` Coriolis Centrifuge Arena, `BLDG-18` Colonial Archives & Museum, `BLDG-19` Hydro-Brewery & Synth Plant, `BLDG-20` Orbital Defense & Laser Comms), `PROP-01`..`PROP-05` badges, and VTOL `H` landing reticle |
| `glass_holo_kiosk_cyan_translucent.png` | `512×512` RGBA | `#124058` / `#00E5FF` (`alpha ~ 0.32`) | `M: 0.10`, `R: 0.10`, `BLEND` | True `alphaMode: "BLEND"` translucent holographic projection glass with subtle cyan scanlines and amber/cyan targeting reticles for `prop_02` wayfinding totems, `bldg_18` Holo-Museum projection domes, and `bldg_20` tactical visors |
| `oled_plaza_transit_telemetry.png` | `512×512` RGB | `#0A0E14` + `#00E5FF`/`#FF9500`/`#00E5C0` | `M: 0.08`, `R: 0.18`, `Emissive` | Mag-Lev Ring Line & Shuttle arrival schedule, `0.98g` / `2.10 RPM` Coriolis spin-gravity gauge, and Plaza Atmospheric Scrubber (`O2 21.4 kPa`, `CO2 0.038%`) telemetry panel for `prop_01`, `prop_03`, and District IV terminals |

### 5.2 Phase 3A — 5 Sci-Fi Movie Set Street-Plaza Prop Rounds (`prop_01` – `prop_05`)
Each prop round follows the 5-candidate tournament (`_r1_01.glb` .. `_r1_05.glb`) with **Candidate `#02`** embodying the signature **65/35 Aegis-7 Asymmetric Split-Mass + `alphaMode: "BLEND"` Translucent/Holo Element**:
1. **`prop_01` (`prop_01_maglev_shuttle_pylon`) — Elevated Mag-Lev Guideway Pylon & Ring-Transit Shuttle Pod:** Uses `facade_titanium_gunmetal_hull.png`, `facade_aerospace_white_cladding.png`, `glass_curtainwall_cyan_translucent.png`, `oled_plaza_transit_telemetry.png`, and `led_cyan_strip.png`.
2. **`prop_02` (`prop_02_holo_wayfinding_kiosk`) — Octagonal Pedestrian Wayfinding & Telemetry Holo-Kiosk:** Uses `facade_carbon_slate_spandrel.png`, `glass_holo_kiosk_cyan_translucent.png`, `oled_holo_wayfinding_map.png`, `accent_safety_orange.png` (`#D95B26` breather hatch), and `led_amber_strip.png`.
3. **`prop_03` (`prop_03_atmo_scrubber_bollard`) — Atmospheric Scrubber Intake Vent & Spin-Gravity Balancer Bollards:** Uses `facade_titanium_gunmetal_hull.png`, `facade_brushed_steel_gantry.png`, `oled_plaza_transit_telemetry.png`, `accent_safety_orange.png`, and `led_cyan_strip.png`.
4. **`prop_04` (`prop_04_civic_planter_bench_pod`) — Terraced Octagonal Civic Planter & Contoured Crew Bench Pod:** Uses `facade_aerospace_white_cladding.png`, `glass_biodome_emerald_translucent.png`, `foliage_aeroponic_herbs.png`, `led_uv_violet.png`, and `led_amber_strip.png`.
5. **`prop_05` (`prop_05_vtol_landing_pad_radar`) — Octagonal VTOL Med-Evac / Shuttle Landing Pad & Rotating Telemetry Dish Array:** Uses `facade_titanium_gunmetal_hull.png`, `facade_brushed_steel_gantry.png`, `signage_district4_marquees.png`, `accent_safety_orange.png`, and `led_amber_strip.png`.

### 5.3 Phase 3B — District IV Building Exteriors (`bldg_16` – `bldg_20`)
All 5 District IV buildings (`12.0m–15.0m W × 10.0m–12.0m D × 16.0m–22.0m H`, `3,200–5,800` tris) feature **Candidate `#02`** as the canonical **65/35 Aegis-7 Dual-Zone Split-Mass Exterior + Full-Height `alphaMode: "BLEND"` Translucent Tower/Atrium**:
16. **Building 16 (`bldg_16_zero_g_shipyard_drydock`) — Zero-G Axial Shipyard & Orbital Drydock Gantry:** Left 65% armored assembly hall (`#1A1E24` / `#D8DEE6`) with `BLDG-16 // ZERO-G SHIPYARD DRYDOCK` marquee (`signage_district4_marquees.png`); Right 35% full-height translucent drydock gantry spine revealing a 3D orbital utility craft berth and cyan laser-welding rings.
17. **Building 17 (`bldg_17_coriolis_centrifuge_arena`) — Coriolis Spin-Gravity Centrifuge Gym & Zero-G Sports Arena:** Left 65% chamfered aerospace-white athletic pavilion with `BLDG-17 // CORIOLIS CENTRIFUGE ARENA` marquee; Right 35% full-height translucent training tower revealing rotating `1.25g` centrifuge rings and `oled_plaza_transit_telemetry.png` biomonitors.
18. **Building 18 (`bldg_18_colonial_archives_museum`) — Colonial Archives Vault & Founders Holo-Museum:** Left 65% stepped titanium & aerospace-white archive monolith with `BLDG-18 // COLONIAL ARCHIVES & MUSEUM` marquee; Right 35% full-height `glass_holo_kiosk_cyan_translucent.png` Holo-Museum rotunda tower projecting a 3D O'Neill Cylinder heritage hologram (`oled_holo_wayfinding_map.png`).
19. **Building 19 (`bldg_19_hydro_brewery_synth_plant`) — Automated Hydro-Brewery & Bio-Nutrient Fermentation Plant:** Left 65% terraced synthesizer hall (`BLDG-19 // HYDRO-BREWERY & SYNTH PLANT`); Right 35% full-height `glass_biodome_emerald_translucent.png` fermentation column revealing 3D copper/steel distillation coils and emerald/amber bioluminescent vats.
20. **Building 20 (`bldg_20_orbital_defense_laser_bastion`) — Orbital Point-Defense & Deep-Space Laser Comms Bastion:** Left 65% heavily buttressed gunmetal & carbon-slate command bunker (`BLDG-20 // ORBITAL DEFENSE & LASER COMMS`); Right 35% full-height translucent optical-capacitor tower crowned by a gimbaled deep-space laser comms turret.
