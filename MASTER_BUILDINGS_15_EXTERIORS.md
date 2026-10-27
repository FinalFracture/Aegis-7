# MASTER ARCHITECTURAL BIBLE — 15 O'NEILL CYLINDER BUILDING EXTERIORS ("AEGIS-7 EXTERIOR STANDARD")

## 1. Mandate & Single-Architect Exterior Vision
- **Target:** 15 distinct, cohesive sci-fi **Building Exteriors** (`bldg_01` through `bldg_15`) populating the curved inner landscape of our 800m × 400m O'Neill Cylinder space habitat (*Orbital Hab-7*).
- **Strict 5-Candidate Tournament & 5-Bot Voting Protocol:**
  - For **every single building exterior (`bldg_01` through `bldg_15`)**, the team must:
    1. **Design (`Sloane`):** Specify 5 distinct exterior architectural variations (`_r1_01` through `_r1_05`) plus exterior facade/window/roof/beacon textures in `/workspace/game-project/assets/textures/buildings/` and design specs in `/workspace/game-project/design/`.
    2. **Model (`Rook`):** Build all 5 candidate `.glb` models (`bldg_XX_r1_01.glb` .. `bldg_XX_r1_05.glb`) in `/workspace/game-project/assets/glb/buildings/bldg_XX/` with real multi-level architectural massing, 45° chamfered octagonal titanium ribs, cantilevered pods/terraces, `alphaMode: "BLEND"` translucent glass curtain walls/atria/domes with visible interior floors/structures, rooftop comms/HVAC/landing pads, and pedestrian plaza bases (`3,000–6,000` tris per building).
    3. **Render (`Gage`):** Render all 5 candidates in Godot 4 (`1920×1080`) + a 5-panel voting sheet (`bldg_XX_round1_voting_sheet.png`) in `/workspace/game-project/godot/renders/buildings/bldg_XX/`, and assemble the 3 District Exterior Showcase Scenes + the Grand 15-Building O'Neill Cylinder Metropolis Scene (`cylinder_hab7_metropolis.tscn`).
    4. **Vote (`All 5 Bots — Sloane, Rook, Gage, Scribe, Atlas`):** Only after all 5 candidates for a building are modeled and rendered in Godot 4 do all 5 bots inspect the voting sheet, log their post-render votes in `/workspace/game-project/context/VOTE_LOG.md`, and lock 1 canonical winner `.glb` per building into `/workspace/game-project/assets/glb/winners/`.

---

## 2. Unified "Aegis-7 Exterior Standard" Architectural Language
To guarantee all 15 buildings look designed by the **exact same master architect** as our 10 interior rooms:
- **Structural Massing:**
  - **65/35 or 68/32 Asymmetric Split-Mass Silhouette:** Candidate `#02` in every round embodies our signature Aegis-7 Dual-Zone Split-Bay Architecture—pairing a primary main structural volume (65–68% width: stepped octagonal tower, dome, or hall in matte aerospace white `#D8DEE6` and dark anodized gunmetal `#1A1E24`) with a full-height vertical secondary tower/gantry (32–35% width: `alphaMode: "BLEND"` translucent glass atrium, elevator spine, cryo-column, or drone/shuttle gantry in brushed machined steel `#88929E` and carbon slate `#282E38`).
  - **45° Chamfered Octagonal Buttresses & Plinths:** Every building sits on a dark gunmetal (`#1A1E24`) chamfered octagonal plaza plinth with glowing amber (`#FF9500`) safety perimeter strips, recessed cyan (`#00E5FF`) architectural facade ribs, and signal-orange (`#D95B26`) airlock doors / docking clamps.
  - **True `alphaMode: "BLEND"` Translucent Facades & Domes:** Curtain walls, sky-bridges, biodomes, and reactor columns use true alpha-blended glass (`alpha 0.28–0.42`) revealing 3D interior floor slabs, illuminated columns, foliage, or plasma cores inside.

---

## 3. The 15 O'Neill Cylinder Building Exteriors (3 Districts × 5 Buildings)

### District I — Residential & Civic Terrace Sector (`bldg_01` – `bldg_05`)
1. **Building 01 (`bldg_01_hab_spire`) — Aegis-7 Modular Crew Habitat Tower**
   - Footprint: `12m W × 10m D × 18m H` (scaled cleanly for showcase & district scenes)
   - `#01`: Symmetric Octagonal Stepped Pod Spire
   - `#02`: **Dual-Zone Split Residential Pod Spire & Translucent Sky-Elevator Atrium Tower** (Aegis-7 65/35 Split-Mass Signature)
   - `#03`: Twin-Cantilevered Hex-Hive Terraced Apartment Block
   - `#04`: Curved Cylinder-Slope Terraced Habitat Ziggurat
   - `#05`: Suspended Modular Pod-Cluster & Skybridge Tower
2. **Building 02 (`bldg_02_transit_rotunda`) — Elevated Mag-Lev & Ring Transit Rotunda**
   - `#01`: Octagonal Central Mag-Lev Concourse Rotunda
   - `#02`: **Dual-Zone Split Mag-Lev Station Hall & Vertical Shuttle-Pod Boarding Tower**
   - `#03`: Twin-Tube Elevated Guideway Overpass Terminal
   - `#04`: Cantilevered Ring-Line Commuter Hub & Control Pylon
   - `#05`: Tri-Level Rotary Transit Interchange Plaza
3. **Building 03 (`bldg_03_culinary_atrium`) — Terraced Synthesizer & Culinary Commons Pavilion**
   - `#01`: Octagonal Glass-Crowned Mess Hall Pavilion
   - `#02`: **Dual-Zone Split Culinary Dining Pavilion & Full-Height Translucent Aeroponic Herb Tower**
   - `#03`: Terraced Promenade Bistro & Zero-G Beverage Rotunda
   - `#04`: Twin-Wing Civic Refectory & Solar-Lit Courtyard
   - `#05`: Cantilevered Overlook Dining Deck & Ration Silo Complex
4. **Building 04 (`bldg_04_medical_trauma_center`) — Orbital Trauma & Biomonitor Medical Complex**
   - `#01`: Octagonal Med-Bay Clinical Pavilion with Rooftop Med-Evac Pad
   - `#02`: **Dual-Zone Split Trauma Hospital Wing & Translucent UV-Sterile Cryo-Pharmacy Tower**
   - `#03`: Twin-Dome Bio-Quarantine & Triage Center
   - `#04`: Stepped Aerospace-White Surgical Institute & Ambulance Dock
   - `#05`: Cantilevered Zero-G Recovery Sanatorium & Telemetry Spire
5. **Building 05 (`bldg_05_celestial_promenade_dome`) — Zero-G Observation & Recreation Dome**
   - `#01`: Faceted Octagonal Geodesic Observation Dome
   - `#02`: **Dual-Zone Split Stargazer Lounge Dome & Illuminated Zero-G Ascent Tower**
   - `#03`: Twin-Ringed Panoramabridge & Amphitheater Pavilion
   - `#04`: Terraced Civic Park Conservatory & Holo-Fountain Rotunda
   - `#05`: Cantilevered Horizon Viewing Deck & Celestial Bar Complex

### District II — Agri-Biosphere & Research Sector (`bldg_06` – `bldg_10`)
6. **Building 06 (`bldg_06_hydroponic_biodome`) — Aeroponic & Bio-Scrubber Conservatory Complex**
   - `#01`: Tri-Dome Geodesic Botanical Conservatory
   - `#02`: **Dual-Zone Split Greenhouse Conservatory & Full-Height Translucent O2 Algae Bio-Scrubber Tower**
   - `#03`: Stepped Agricultural Ziggurat & UV-Grow Terrace
   - `#04`: Twin-Cylinder Vertical Farm & Nutrient Silo Array
   - `#05`: Octagonal Biosphere Rotunda & Canopy Skywalk
7. **Building 07 (`bldg_07_atmospheric_processor`) — Sector Atmospheric & O2/CO2 Scrubber Plant**
   - `#01`: Octagonal Air-Exchange Intake & Turbine Hall
   - `#02`: **Dual-Zone Split Atmospheric Processor Hall & Translucent Cryo-O2 Distillation Tower**
   - `#03`: Quad-Stack Venturi Scrubber & Thermal Louver Plant
   - `#04`: Twin-Sphere Liquid-Oxygen Storage & Barometric Station
   - `#05`: Heavy Industrial Spin-Filter & Humidity Control Complex
8. **Building 08 (`bldg_08_astrometry_observatory`) — Deep-Space Astrometry & Sensor Array Complex**
   - `#01`: Octagonal Clamshell Optical Telescope Observatory
   - `#02`: **Dual-Zone Split Astrometry Research Lab & Rotating Deep-Space Telemetry Dish Tower**
   - `#03`: Tri-Dish Interferometer & Quantum Comms Array Building
   - `#04`: Stepped Sensor Dome & Subspace Beacon Annex
   - `#05`: Cantilevered Deep-Sky Spectrograph & Holo-Charting Center
9. **Building 09 (`bldg_09_aquifer_pumping_station`) — Ring-Gravity Water Reclamation & Aquifer Cascade**
   - `#01`: Octagonal Hydro-Filtration Hall & Settling Basin
   - `#02`: **Dual-Zone Split Centrifugal Pumping Plant & Translucent Illuminated Water-Column Tower**
   - `#03`: Terraced Cascade Spillway & UV-Purification Complex
   - `#04`: Twin-Silo Greywater Recovery & Mineral Dosing Station
   - `#05`: Heavy Conduit Manifold & Pressure-Regulator Building
10. **Building 10 (`bldg_10_cryo_seed_vault`) — Colonial Cryo-Genetics & Seed Archive Vault**
    - `#01`: Armored Octagonal Sub-Zero Gene Bank Monolith
    - `#02`: **Dual-Zone Split Armored Seed Archive Vault & Translucent Cryo-Stasis Helix Tower**
    - `#03`: Subterranean-Plinth Cryogenic Silo & Radiator Array
    - `#04`: Twin-Buttressed Bio-Preservation Bunker & Lab Wing
    - `#05`: Cantilevered Deep-Freeze Repository & Security Portal

### District III — Command, Power & Industrial Port Sector (`bldg_11` – `bldg_15`)
11. **Building 11 (`bldg_11_citadel_command_hq`) — Cylinder Hab-7 Central Command & Telemetry Citadel**
    - `#01`: Monumental Octagonal Command Spire & Bridge Crown
    - `#02`: **Dual-Zone Split Command Citadel Spire & Translucent Quantum Flight-Director Tower**
    - `#03`: Twin-Obelisk Sector Governance & Defense HQ
    - `#04`: Stepped Pyramidion Overwatch Citadel & Holo-Beacon
    - `#05`: Cantilevered High-Command Bridge & Comms Mast Complex
12. **Building 12 (`bldg_12_fusion_reactor_complex`) — D-He3 Fusion Power & Spin-Drive Reactor Hall**
    - `#01`: Octagonal Magnetic-Confinement Fusion Reactor Dome
    - `#02`: **Dual-Zone Split Fusion Containment Hall & Translucent 5-Coil Plasma Pinch Tower**
    - `#03`: Twin-Core Toroidal Tokamak & Radiator Fin Complex
    - `#04`: Heavy Armored Spin-Drive Impulse Plant & Cryo Bay
    - `#05`: High-Voltage Substation & Plasma Conduit Gantry Hall
13. **Building 13 (`bldg_13_cargo_logistics_port`) — High-Bay Intermodal Cargo & Drone Gantry Terminal**
    - `#01`: Octagonal High-Bay Freight Warehouse & Crane Arch
    - `#02`: **Dual-Zone Split Intermodal Cargo Terminal & Translucent ISO Container / Drone Gantry Tower**
    - `#03`: Twin-Gantry Open Container Yard & Mag-Loader Dock
    - `#04`: Automated Logistics Sorting Hub & Drone Hive Roof
    - `#05`: Heavy Bulkhead Freight Depot & Shuttle Unloading Bay
14. **Building 14 (`bldg_14_eva_docking_pinnacle`) — Axial Zero-G Shuttle & EVA Docking Pinnacle**
    - `#01`: Octagonal Vertical Airlock & Docking Collar Tower
    - `#02`: **Dual-Zone Split EVA Staging Terminal & Translucent Umbilical Shuttle Docking Pinnacle**
    - `#03`: Twin-Arm Cantilevered Orbital Tender Berth
    - `#04`: Pressurized Passenger Boarding Spire & Suit Prep Hall
    - `#05`: Heavy Hull-Lock Checkpoint & Rescue Cutter Hangar
15. **Building 15 (`bldg_15_solar_mirror_control_pylon`) — Orbital Solar-Mirror & Mag-Shield Control Pylon**
    - `#01`: Octagonal Heliostat & Magnetic Shield Emitter Pylon
    - `#02`: **Dual-Zone Split Shield Control Bunker & Translucent Gyroscopic Field-Ring Pylon**
    - `#03`: Tri-Strut Solar Louver Actuator & Capacitor Tower
    - `#04`: Twin-Coil Magnetosphere Deflector & Laser Alignment Spire
    - `#05`: Armored Axial Weather-Control & Daylight Relay Station

---

## 4. Exterior District & Metropolis Godot 4 Scenes (`godot/scenes/buildings/` & `godot/renders/buildings/`)
In addition to the 15 individual 5-candidate voting sheets (`bldg_01_round1_voting_sheet.png` .. `bldg_15_round1_voting_sheet.png`) and winner renders:
1. **`district_01_residential_civic.tscn` (`renders/buildings/district_01/`):** Assembles the locked `#02` winners for **Buildings 01–05** along a curved O'Neill Cylinder civic plaza boulevard with illuminated transit guideways, pedestrian walkways, and overhead cylinder-arch vistas.
2. **`district_02_agri_research.tscn` (`renders/buildings/district_02/`):** Assembles the locked `#02` winners for **Buildings 06–10** across a terraced biosphere & research park with hydro-canals, aeroponic greenery, and deep-space sensor lines.
3. **`district_03_command_industrial.tscn` (`renders/buildings/district_03/`):** Assembles the locked `#02` winners for **Buildings 11–15** in the high-energy Command Citadel, Fusion Power, and Cargo Port sector.
4. **`cylinder_hab7_metropolis.tscn` (`renders/buildings/metropolis/`):** Grand 15-Building O'Neill Cylinder Exterior Metropolis showcase uniting all 15 locked building exteriors across the curved habitat landscape!
