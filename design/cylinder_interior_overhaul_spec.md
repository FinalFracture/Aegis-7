# Cylinder Hab-7 Interior Macro-Biome, Asymmetric Sector Layout & Set-Piece Specification
**Author:** Vance (`0724beeb-94b9-43fa-a9cf-27117c5d4aa6`) — Sci-Fi Architect, Movie Prop & Set Design Specialist
**Canonical Path:** `/workspace/game-project/design/cylinder_interior_overhaul_spec.md`
**Target Scene & Script:** `/workspace/game-project/godot/scenes/buildings/cylinder_interior_showcase.tscn` & `/workspace/game-project/godot/scripts/cylinder_interior_showcase.gd`
**Reference Renders Critiqued:** `/workspace/game-project/godot/renders/cylinder_interior/cylinder_interior_showcase_sheet.png` (`cam_01`–`cam_04`)
**Cinema Pedigree:** *Elysium* (2013), *Interstellar* Cooper Station (2014), *Rendezvous with Rama*, *2001: A Space Odyssey* (1968), *Oblivion* (2013)
**Style Mandate:** Unified **Aegis-7 Standard** (`#1A1E24` gunmetal titanium, `#D8DEE6` matte aerospace white, `#282E38` dark carbon slate, `#88929E` brushed machined steel, `#00E5FF` cyan / `#7B5CFF` UV-violet / `#FF9500` amber / `#00E676` emerald LEDs, `#D95B26` signal-orange docking/safety hardware, and `alphaMode: "BLEND"` translucent glass/water).

---

## Section 1 — Root-Cause Critique of Current Interior (`cylinder_interior_showcase_sheet.png` & `cylinder_interior_showcase.gd`)

Visual inspection of `/workspace/game-project/godot/renders/cylinder_interior/cylinder_interior_showcase_sheet.png` (`cam_01` through `cam_04`) alongside `/workspace/game-project/godot/scripts/cylinder_interior_showcase.gd` reveals **six specific architectural and procedural root causes** that make the current 800m × 400m (`R = 200m`) interior read as repetitive, flat, and procedurally cloned rather than a lived-in cinema megastructure:

1. **Exact 3-Fold (`120°`) Rotational Cloning Across All 3 Valleys (`cylinder_interior_showcase.gd` lines 226 & 301–336):**
   - `for valley_phi: float in [180.0, 60.0, 300.0]:` builds the **exact same** `8.5m × 0.35m × 380.0m` straight ruler-line cyan box canal (`canal_box.size = Vector3(8.5, 0.35, 380.0)`) and the exact same 4 flanking light strips (`[-4.2, 4.2, -13.5, 13.5]`) in every single valley.
   - In `_populate_three_curved_valleys()`, all 3 valleys iterate over the same `x_stations` and `phi_offsets` and cycle sequentially through `bldg_01`..`bldg_20` via `(slot_counter + v_idx * 5) % bldg_templates.size()`. As a result, every valley mixes residential, agricultural, medical, reactor, and defense buildings indiscriminately instead of having a distinct functional biome identity.
2. **Rigid Orthogonal Grid Spacing (`x_stations` × `phi_offsets`, lines 299–300):**
   - Buildings are stamped at 8 uniform `50m` longitudinal intervals (`[-245, -195, -145, -95, -45, 5, 55, 102]`) and 6 fixed angular rows (`[-25.0°, -15.0°, -7.8°, +7.8°, +15.0°, +25.0°]`), with every building locked to `yaw = ±90.0°`. In `cam_01` and `cam_02`, this reads like soldiers on a parade ground or a circuit board rather than organic urban planning.
3. **Zero Radial Topography or Terraced Elevation Relief (`R_HULL_FLOOR = 185.5` Constant, line 22 & 322):**
   - Every single building and prop in the entire 520m drum is placed at a single constant radius `R_HULL_FLOOR = 185.5m` (plus baked low-poly strips inside `cylinder_r1_02.glb`). There are no stepped urban podiums (`R = 182m`, `176m`, `170m`), no terraced hillside ziggurats, no sunken amphitheater bowls, and no raised rocky/titanium promontories.
4. **Missing Macro-Scale Transition Landmarks Between `18m` Buildings and the `400m` Drum:**
   - Even with `sc = 2.15–2.45` (`~40m` tall buildings), the `400m` diameter interior volume (`R = 200m`) is `10×` taller than any individual building. Without **macro-scale set pieces**—such as a curved 120° Ring-Spanning Suspension Skybridge & Mag-Lev Viaduct climbing the cylinder wall, a multi-tier Waterfall Hydro-Dam, radial tether-elevator spokes descending from the `Y = 200m` solar axis, or stepped hemispherical endcap cliff terraces—the central volume of the drum feels empty save for a single uniform cylinder (`AxialSolarPlasmaSheath`, `radius = 9.2m`, line 207).
5. **Monochromatic Cyan Lighting Wash Across All Sectors (`_setup_interior_lighting`, lines 415–464):**
   - All three directional lights (`#F0F8FF`, `#DDF2FF`, `#8AD8FF`), all six axial spine lights (`#E8FAFF`), and all valley omni lights (`#00E5FF`) bathe the entire cylinder in the same cool cyan-white wash. There is zero color-temperature separation between the warm Amber/Gold Civic Metropolis, the Emerald/UV-Violet Agri-Biosphere, and the Sodium-Orange/Cyan Industrial Port, and no atmospheric haze/depth cueing along the `800m` axis.
6. **Baked Low-Poly Interior Clutter Inside `cylinder_r1_02.glb` Competing with High-Detail Instanced Winners:**
   - `cylinder_r1_02.glb` contains simplified procedural proxy blocks baked into the hull mesh for exterior viewports, which sit underneath the instanced high-detail `bldg_01`–`bldg_20` meshes at `R = 185.5m` and reinforce the flat 3-way stripe repetition.

---

## Section 2 — 3 Radially Asymmetric Land Valleys (Zero `120°` Rotational Cloning)

To make *Cylinder Hab-7* feel like a real, master-planned orbital world (*Elysium* meets *Cooper Station*), each of the three `120°` valleys is assigned a **radially asymmetric macro-biome**, a unique hydro/transit spine geometry, a dedicated subset of our 20 locked Aegis-7 buildings, and a distinct color-temperature signature:

### 1. Valley A (`phi = 180°` Bottom Nadir, `145° .. 215°`) — "Aegis-7 Civic Metropolis, Terraced Citadel & Grand Promenade"
- **Urban & Set-Design Identity:** High-density capital sector and residential/civic heart of *Orbital Hab-7*. Replaces the flat ruler-canal with a **3-Tier Stepped Octagonal Civic Canyon (`R = 185.5m` Waterfront Esplanade, `R = 180.5m` Mid-Terrace Boulevard, `R = 174.5m` High Citadel Acropolis Podium)** connected by diagonal (`±32°` and `±45°`) pedestrian skybridges and elevated twin-track Mag-Lev viaduct loops.
- **Assigned Building Cluster (Civic, Residential, Medical, Command & Cultural):**
  - **Focal Axis Landmarks:** `bldg_11` (Central Command Citadel Spire — placed on a raised `+11m` central acropolis podium at `X = -65m, phi = 180°`), flanked diagonally by `bldg_18` (Colonial Archives & Earth Holo-Planetarium) and `bldg_05` (Celestial Promenade Geodesic Dome).
  - **High-Density Terraced Wings:** `bldg_01` (Modular Crew Hab Spire), `bldg_02` (Elevated Mag-Lev Transit Rotunda), `bldg_03` (Culinary Commons & Herb Tower), `bldg_04` (Medical Trauma Center with rooftop Med-Evac pads), and `bldg_17` (Coriolis Kinetic Sports Arena & Centrifuge Gymnasium).
- **Street-Level Prop Density:** High concentration of `prop_01` (Elevated Mag-Lev Y-Pylons & Shuttle Pods forming a continuous elevated loop), `prop_02` (Octagonal Holo-Wayfinding Kiosks), `prop_04` (Crew Bench & Planter Pods), and `prop_05` (VTOL Med-Evac Pads outside `bldg_04` and `bldg_11`).
- **Lighting & Palette Signature:** Warm **Golden-Amber (`#FF9500` / `#FFB74D`)** plaza & promenade cove lighting contrasted against crisp **Cyan (`#00E5FF`)** sky-elevator atria and **Matte Aerospace White (`#D8DEE6`)** terraced towers.

### 2. Valley B (`phi = 60°` Port-Upper Sector, `25° .. 95°`) — "Emerald Agri-Biosphere, Terraced Waterfall Cascades & Meandering Ring-River Delta"
- **Ecological & Set-Design Identity:** The living lungs and agricultural breadbasket of *Cylinder Hab-7*. **Zero straight ruler-line canals:** instead, a **Sinusoidally Meandering Ring-River (`phi_river(x) = 60° + 11.5° * sin(x / 48.0)`)** winds through sculpted, terraced **Aeroponic Botanical Contour Hills (`+4m`, `+10m`, `+18m` stepped emerald ziggurat plinths, `R = 185.5m` down to `R = 167.5m`)**, feeding a wide **Central Ring-Lake Reservoir & Stepped Waterfall Hydro-Dam** at `X = -85m`.
- **Assigned Building Cluster (Agri-Biosphere, Hydro, Atmospheric & Genetics Research):**
  - `bldg_06` (Hydroponic Biodome & O2 Algae Bio-Scrubber Tower), `bldg_09` (Aquifer Pumping Station & Waterfall Cascade — anchored directly into the stepped hydro-dam terraces), `bldg_07` (Atmospheric Processor & Cryo-O2 Tower), `bldg_10` (Cryo-Genetics & Seed Archive Vault set on an isolated high bio-quarantine bluff), and `bldg_08` (Deep-Space Astrometry Observatory perched on the highest ridgeline terrace).
- **Biosphere Canopy & Prop Layer:** Clustered `prop_04` (UV-Aeroponic Planter & Bench Pods) scaled and grouped into lush emerald botanical groves, `prop_03` (Venturi Atmo-Scrubber Bollards) lining the riverbanks, and translucent emerald dome canopies (`glass_biodome_emerald_translucent.png`) spanning between terraced agricultural ziggurats.
- **Lighting & Palette Signature:** Rich **Bioluminescent Emerald (`#00E676` / `#12C88A`)** and **Photosynthetic UV-Violet (`#7B5CFF`)** grow-light columns, with cool mist-cyan (`#48F0FF`) waterfall spillways—instantly distinguishable at a glance from Valley A and Valley C!

### 3. Valley C (`phi = 300°` Starboard-Upper Sector, `265° .. 335°`) — "High-Energy Industrial Port, Shipyard Drydock, Fusion Power & Defense Ridge"
- **Industrial & Set-Design Identity:** The heavy engineering, orbital manufacturing, fusion power, and defense backbone of the megaship. Built on massive **45°-Chamfered Dark Gunmetal (`#1A1E24`) and Brushed-Steel (`#88929E`) Stepped Industrial Switchyard Platforms (`R = 185.5m` Heavy Rail Deck, `R = 179.0m` Reactor Containment Shelf, `R = 172.0m` Crane Gantry Ridge)** with acoustic blast walls, overhead magnetic container crane bridges, and high-voltage plasma busbar conduits running aft into the Starport throat.
- **Assigned Building Cluster (Power, Logistics, Shipyard, Refinery & Defense):**
  - `bldg_12` (D-He3 Fusion Power & 5-Coil Plasma Pinch Tower), `bldg_13` (High-Bay Intermodal Cargo & ISO Container Gantry Terminal), `bldg_16` (Axial Zero-G Micro-Shuttle Assembly & Repair Drydock Hall), `bldg_19` (Bioreactor Protein Refinery & Botanical Distillation Plant), `bldg_20` (Point-Defense Laser Bastion & Tachyon Relay Tower), and `bldg_15` (Solar-Mirror & Mag-Shield Control Pylon).
- **Industrial Prop Layer:** Heavy clusters of `prop_05` (Octagonal VTOL Shuttle/Cargo Landing Pads with `#D95B26` magnetic skid clamps), `prop_03` (Spin-Gravity Harmonic Balancer & Scrubber Bollards), and overhead brushed-steel truss gantries spanning across the industrial canyon.
- **Lighting & Palette Signature:** High-contrast **Signal-Orange (`#D95B26`)** and **Industrial Amber (`#FF9500`)** hazard strobes, **Dark Gunmetal (`#1A1E24`)** armor masses, and blazing **Cyan-White (`#00E5FF`)** fusion plasma pinch cores.

---

## Section 3 — Longitudinal Zoning Along the 520m Habitat Drum (`X = -260m` to `+260m` Fore-to-Aft Progression)

Instead of repeating the same cross-section from front to back, the `520m` rotating habitat drum (`X = -320m` to `+160m` in world space) is divided into **4 distinct longitudinal zones** from Forward (`-X`) to Aft (`+X`):

1. **Zone 1 — Forward Hemispherical Endcap & Axial Docking Bowl (`X = -310m` to `-210m`):**
   - **Architecture:** Replaces the flat concentric endcap rings (`cam_04` critique) with **Monumental Stepped Concentric Cliffside Terraces (`R = 185m` stepping up to `R = 45m`)** climbing the forward hemispherical bulkhead toward the central zero-G axis (`Y = 200m, Z = 0m`).
   - **Landmarks:** Anchored by `bldg_14` (Axial Zero-G Shuttle & EVA Docking Pinnacles) around the upper axial docking collar (`R = 45m..75m`), connected to the three valley floors below by **3 Asymmetric Radial Funicular / Tether-Elevator Gantry Tracks** running up the curved endcap slope.
2. **Zone 2 — Mid-Fore Metropolis & Ring-Viaduct Core (`X = -210m` to `-60m`):**
   - **Architecture:** Peak architectural density in Valley A (Command Citadel `bldg_11` Acropolis & Civic Canyon), the **Grand Ring-Lake Reservoir & Stepped Hydro-Dam** in Valley B (`bldg_09` + `bldg_06`), and the **Intermodal Cargo & Shipyard Drydock Complex** in Valley C (`bldg_13` + `bldg_16`).
   - **Overhead Macro-Landmark:** At `X = -115m`, the colossal **360° / 120° Ring-Spanning Suspension Skybridge & Multi-Tier Mag-Lev Viaduct Arch (`interior_setpiece_01`)** curves all the way up the inner cylinder hull wall (`R = 185m` to `R = 148m`), physically linking Valley A (`180°`), Valley B (`60°`), and Valley C (`300°`) across the solarium window strips!
3. **Zone 3 — Mid-Aft Elevated Promontories, Research Plateaus & Recreation Ridge (`X = -60m` to `+65m`):**
   - **Architecture:** The valleys narrow and rise onto **Stepped Titanium & Terraced Bedrock Plateaus (`R = 178m` to `R = 166m`)** overlooking the mid-fore basins.
   - **Landmarks:** Hosts the Coriolis Recreation Arena (`bldg_17`) and Celestial Observation Dome (`bldg_05`) on a scenic overlook bluff in Valley A; the Deep-Space Astrometry Observatory (`bldg_08`) and Cryo-Genetics Seed Vault (`bldg_10`) on an isolated research plateau in Valley B; and the D-He3 Fusion Reactor Complex (`bldg_12`) and Refinery (`bldg_19`) in Valley C.
4. **Zone 4 — Aft Starport Bulkhead, Ring-Sea Dam & Solar-Shield Transition (`X = +65m` to `+155m`):**
   - **Architecture:** Heavy 45°-chamfered gunmetal (`#1A1E24`) acoustic/radiation baffle bulkhead separating the spin-gravity habitat drum from the counter-rotating `280m` Aft Zero-G Starport & Fusion Drive (`X = +160m` to `+400m`).
   - **Landmarks:** Guarded by `bldg_15` (Solar-Mirror & Mag-Shield Control Pylons) and `bldg_20` (Point-Defense Laser Bastions) flanking a massive **Ring-Canal Spillway Weir** and a translucent `alphaMode: "BLEND"` observation gallery looking aft into the zero-G starport gantry and 5-coil fusion drive.

---

## Section 4 — 5 Hero Interior Macro-Setpieces / Landmarks (`interior_setpiece_01` – `interior_setpiece_05`)

To bridge the scale gap between `18m–40m` buildings and the `400m` diameter (`R = 200m`) O'Neill Cylinder drum, we introduce **5 Hero Macro-Setpieces**. Each setpiece follows our 5-Candidate Tournament Spec (`_r1_01`..`_r1_05`) with **`#02` executing the Aegis-7 65/35 Dual-Zone Split-Mass & `alphaMode: "BLEND"` Signature**:

### 1. `interior_setpiece_01_ring_skybridge_viaduct` — Curved 120° Ring-Spanning Suspension Skybridge & Multi-Tier Mag-Lev Viaduct Arch
- **Macro Scale & Footprint:** Spans a `120°` arc (`~380m` arc length at `R = 185m..152m`, `28m` wide × `34m` radial height) at `X = -115m` | **Budget:** `3,800–5,600` tris
- **Candidate Lineup (`_r1_01`..`_r1_05`):**
  - `#01`: Symmetric Twin-Pylon Curved Mag-Lev Viaduct Arch
  - **`#02` (Aegis-7 65/35 Signature): Dual-Zone Split Curved Suspension Viaduct Deck & Translucent Mid-Span Sky-Transfer Rotunda:**
    - **Primary 65% Zone:** Monumental curved 45°-chamfered gunmetal (`#1A1E24`) and matte aerospace-white (`#D8DEE6`) twin-deck suspension viaduct climbing the inner cylinder wall across the solarium strip, complete with brushed-steel (`#88929E`) diagonal tension cables, glowing cyan (`#00E5FF`) mag-lev induction rails, docked shuttle trains, and amber (`#FF9500`) aviation warning strobes.
    - **Secondary 35% Zone:** Suspended mid-span **`alphaMode: "BLEND"` Translucent Cyan/Glass Sky-Transfer Rotunda & Zero-G Observation Pod (`R = 152m`)** cantilevered toward the cylinder axis, revealing 3D internal commuter transfer rings, holo-telemetry core, and signal-orange (`#D95B26`) emergency shuttle docking collars.
  - `#03`: Tri-Chord Space-Frame Truss Skybridge & Cargo Rail
  - `#04`: Cantilevered Solarium Overlook Arch & Pedestrian Promenade
  - `#05`: Heavy Buttressed Ring-Highway Interchange & Drone Pylon

### 2. `interior_setpiece_02_terraced_waterfall_reservoir` — Stepped Hydro-Dam, Meandering Ring-River Cascade & Emerald Biodome Conservatory Peninsula
- **Macro Scale & Footprint:** `140m L × 95m W × 26m Radial Height` in Valley B (`X = -150m..-10m, phi = 60°`) | **Budget:** `3,600–5,400` tris
- **Candidate Lineup (`_r1_01`..`_r1_05`):**
  - `#01`: Symmetric Stepped Octagonal Hydro-Dam & Reservoir Basin
  - **`#02` (Aegis-7 65/35 Signature): Dual-Zone Split Stepped Hydro-Dam Spillway & Translucent Emerald Botanical Terraced Ziggurat:**
    - **Primary 65% Zone:** 4-tier curved chamfered gunmetal (`#1A1E24`) and aerospace-white (`#D8DEE6`) **Hydro-Reclamation Dam & Meandering River Delta** featuring 4 cascading `alphaMode: "BLEND"` glowing cyan/aqua waterfall spillways (`#00E5FF` / `#48F0FF`), brushed-steel (`#88929E`) floodgate turbines (`#D95B26` valve wheels), and a sinuous river channel that curves organically through the valley.
    - **Secondary 35% Zone:** Terraced **`alphaMode: "BLEND"` Emerald Biodome Peninsula (`glass_biodome_emerald_translucent.png`, `+18m` high)** jutting into the reservoir lake, revealing 3D stepped green agricultural crop terraces (`#00E676`), UV-violet (`#7B5CFF`) grow-light rings, and cantilevered pedestrian viewing bridges.
  - `#03`: Twin-Spillway Aquifer Basin & Floating Hydroponic Islands
  - `#04`: Terraced Botanical Canyon & Mist-Scrubber Cascade
  - `#05`: Cantilevered Reservoir Overlook Dam & Intake Rotunda

### 3. `interior_setpiece_03_axial_suncore_spoke_hub` — Central Axial Zero-G Solar-Plasma Light-Line, Rotating Louver Baffles & Radial Tether-Elevator Spoke Hub
- **Macro Scale & Footprint:** Spans `520m` along the central axis (`Y = 200m, Z = 0m`) with `185m`-long radial tether spokes descending to Valleys A, B, and C at `X = -115m` | **Budget:** `3,800–5,600` tris
- **Candidate Lineup (`_r1_01`..`_r1_05`):**
  - `#01`: Symmetric 3-Spoke Axial Hub & Cylindrical Daylight Tube
  - **`#02` (Aegis-7 65/35 Signature): Dual-Zone Split Axial Zero-G Transfer Hub & Translucent Heliostat Plasma-Baffle Spine with Asymmetric Radial Elevator Spokes:**
    - **Primary 65% Zone:** Replaces the plain `AxialSolarPlasmaSheath` cylinder with an engineered **Segmented Axial Solar-Plasma Core** ringed every `65m` by 45°-chamfered gunmetal (`#1A1E24`) and brushed-steel (`#88929E`) **Articulated Heliostat Daylight Louver Baffles** (casting directional golden-white daylight toward the bottom valley and cool sky-fill above) plus **3 Radial High-Tension Elevator Spoke Gantries** descending `185m` from the central hub to the Valley A, B, and C skybridge terminals, complete with climbing illuminated zero-G transit climber cars!
    - **Secondary 35% Zone:** Central **`alphaMode: "BLEND"` Translucent Zero-G Axial Docking & Weather-Control Sphere (`R = 24m` at `X = -115m, Y = 200m, Z = 0m`)** revealing 3D internal gyroscopic solar-plasma pinch coils (`#00E5FF` / `#FF9500`), zero-G commuter transfer rings, and `#D95B26` signal-orange axial shuttle berths.
  - `#03`: Hexagonal Geodesic Sun-Core Truss & Cable-Car Spokes
  - `#04`: Twin-Node Axial Climate Controller & Heliostat Wing Array
  - `#05`: Heavy Armored Spin-Bearing Hub & Radial Umbilical Conduits

### 4. `interior_setpiece_04_endcap_cliffside_citadel` — Forward Hemispherical Bulkhead Cliffside Terraces, Radial Funicular Gantry & Axial Docking Bowl
- **Macro Scale & Footprint:** `R = 40m..185m` across the forward bulkhead bowl (`X = -305m..-225m`) | **Budget:** `3,800–5,500` tris
- **Candidate Lineup (`_r1_01`..`_r1_05`):**
  - `#01`: Concentric Stepped Octagonal Bulkhead Amphitheater Bowl
  - **`#02` (Aegis-7 65/35 Signature): Dual-Zone Split Stepped Cliffside Hanging-Terrace Podiums & Translucent Radial Funicular Elevator Spine:**
    - **Primary 65% Zone:** Monumental 5-tier stepped 45°-chamfered gunmetal (`#1A1E24`) and matte aerospace-white (`#D8DEE6`) **Cliffside Hanging Terraces** climbing the forward hemispherical bulkhead (`R = 185m` -> `150m` -> `115m` -> `80m` -> `48m` Axial Docking Collar), with recessed amber (`#FF9500`) and cyan (`#00E5FF`) retaining-wall light bands and cantilevered overlook plazas that eliminate the flat bullseye endcap look in `cam_01` and `cam_04`.
    - **Secondary 35% Zone:** Full-height **`alphaMode: "BLEND"` Translucent Radial Funicular & Zero-G Ascent Tube** climbing `140m` vertically up the forward bulkhead face from Valley A (`phi = 180°`) to the Axial Zero-G Docking Hub (`Y = 200m`), revealing 3D internal pressurized funicular rail cars, counterweights, and signal-orange (`#D95B26`) airlock transfer stations at each terrace tier.
  - `#03`: Tri-Radial Bulkhead Buttress Ribs & Overlook Balconies
  - `#04`: Terraced Botanical Hanging Gardens & Endcap Reservoir Weir
  - `#05`: Heavy Armored Spin-Bulkhead Shield Wall & Shuttle Launch Tubes

### 5. `interior_setpiece_05_elevated_plaza_interchange` — Multi-Level Asymmetric Civic Canyon, Diagonal Skywalk Network & Terraced Plaza Podium
- **Macro Scale & Footprint:** `160m L × 85m W × 22m H` multi-tier urban podium in Valley A (`X = -140m..+20m, phi = 180°`) | **Budget:** `3,800–5,600` tris
- **Candidate Lineup (`_r1_01`..`_r1_05`):**
  - `#01`: Octagonal 3-Tier Concentric Acropolis Plaza Podium
  - **`#02` (Aegis-7 65/35 Signature): Dual-Zone Split 3-Tier Asymmetric Acropolis Podium & Translucent Sunken Holo-Amphitheater / Diagonal Skywalk Network:**
    - **Primary 65% Zone:** Stepped 3-level chamfered gunmetal (`#1A1E24`), carbon-slate (`#282E38`), and aerospace-white (`#D8DEE6`) **Urban Canyon Podium (`+0m` Waterfront Deck, `+6.5m` Civic Terrace, `+13.5m` Citadel Acropolis)** with angled `30°/45°` oblique building pads, grand staircases with glowing amber (`#FF9500`) safety nosings, and elevated brushed-steel (`#88929E`) **Diagonal Pedestrian & Mag-Lev Skybridges** connecting upper building floors.
    - **Secondary 35% Zone:** **`alphaMode: "BLEND"` Translucent Cyan/Glass CoveredGalleria & Sunken Orbital Holo-Amphitheater** revealing a 3D glowing holographic O'Neill Cylinder monument at the plaza heart, subterranean transit concourse levels, and signal-orange (`#D95B26`) VIP shuttle pad clamps.
  - `#03`: Twin-Bridge Elevated Boulevard Canyon & Transit Rotunda Deck
  - `#04`: Terraced Civic Promenade Steps & Canal-Spanning Arcade
  - `#05`: Cantilevered Overlook Podium & Multi-Level Skywalk Hub

---

## Section 5 — Lighting, Atmospheric Depth, Color Temperature Contrast & Godot 4 Implementation Blueprint (For Sloane, Rook & Gage)

### 5.1 Sector-Specific Color Temperature & Practical Lighting Blueprint (`_setup_interior_lighting`)
To immediately cure the monochromatic cyan wash seen in `cylinder_interior_showcase_sheet.png`, replace the uniform `#00E5FF` valley lights with **3 Distinct Sector Lighting Rigs + Axial Depth Gradient**:

| Sector / Zone | Primary Key / Fill Color | Practical Omni / Strip Accents | Visual Mood & Film Reference |
| :--- | :--- | :--- | :--- |
| **Axial Sun-Core Spine (`Y = 200m, Z = 0m`)** | Warm Solar Daylight (`#FFF4E0`, `energy = 2.2`) forward -> Crisp Ice-Cyan (`#C8F4FF`, `energy = 1.8`) aft | Alternating `#FF9500` amber heliostat louver rings & `#48F0FF` plasma core | *Interstellar* Cooper Station / *Rama* central sun-line |
| **Valley A (`180°` Bottom — Civic Metropolis)** | Warm Golden-White Key (`#FFE8C2`, `energy = 1.35`) | Warm Circadian Amber (`#FF9500`, `60%`) + Cyan (`#00E5FF`, `40%`) | *Elysium* / *Oblivion* high-contrast warm civic capital |
| **Valley B (`60°` Port — Agri-Biosphere)** | Lush Solar-Emerald Fill (`#B8FFE0`, `energy = 1.15`) | Bioluminescent Emerald (`#00E676`, `65%`) + UV-Violet (`#7B5CFF`, `35%`) | *Silent Running* / *Avatar* bioluminescent terraced forest |
| **Valley C (`300°` Starboard — Industrial Port)** | Cool Steel-Blue Rim (`#88C8FF`, `energy = 1.10`) | Sodium Signal-Orange (`#D95B26` / `#FF6D00`, `70%`) + Plasma Cyan (`#00E5FF`, `30%`) | *Alien* / *Blade Runner* heavy orbital drydock & fusion plant |
| **Atmospheric Depth / Aerial Perspective** | Godot `WorldEnvironment` Volumetric/Depth Fog (`fog_enabled = true`, `fog_light_color = Color("#0D1E2D")`, `fog_density = 0.00085`, `fog_sky_affect = 0.25`) | Subtle atmospheric scattering over `800m` distance so distant `X = +150m` and endcap structures recede with true aerial perspective! | Eliminates flat foreground-vs-background contrast |

### 5.2 Concrete Algorithm & Transform Table for Gage's `cylinder_interior_showcase.gd` (Zero Grid Loops)
Replace the uniform `x_stations` × `phi_offsets` nested grid loop in `_populate_three_curved_valleys()` with **3 Biome-Specific Placement Tables + Multi-Tier Radial Elevations (`r_floor`) + Oblique Yaw Angles**:

1. **Multi-Tier Radial Terracing (`r_floor` Variation):**
   - Instead of fixed `R_HULL_FLOOR = 185.5`, compute `r_floor = R_HULL_FLOOR - terrace_height_m` accompanied by a chamfered octagonal/stepped plinth mesh beneath each elevated cluster:
     - **Waterfront / Canal Edge:** `r_floor = 185.5m` (`+0.0m` base elevation)
     - **Mid-Terrace Podium:** `r_floor = 179.5m` (`+6.0m` stepped titanium/emerald terrace podium)
     - **High Acropolis / Bluff Promontory:** `r_floor = 171.5m` (`+14.0m` landmark citadel/observatory bluff)
2. **Valley-Specific Building Specialization (Zero Cross-Valley Cloning):**
   - **Valley A (`phi_center = 180°` Civic Metropolis):**
     - Place `bldg_11` (Citadel Command HQ, `scale = 3.2`, `r_floor = 171.5m`, `yaw = 0°`) on the central Acropolis Podium at `X = -85.0m, phi = 180.0°`, flanked by `bldg_18` (`X = -125m, phi = 166°, yaw = 58°`) and `bldg_05` (`X = -125m, phi = 194°, yaw = -58°`).
     - Populate asymmetric diagonal avenues (`yaw ∈ {-62°, -35°, +35°, +62°, +115°}`) with `bldg_01`, `bldg_02`, `bldg_03`, `bldg_04`, and `bldg_17` using staggered longitudinal offsets (`Δx = ±14m..28m` jitter) and variable scales (`sc = 2.05..2.85`).
   - **Valley B (`phi_center = 60°` Emerald Agri-Biosphere & Meandering River):**
     - Replace the straight canal box with **12 curved river segments** following `phi_river(x) = 60.0 + 11.0 * sin(x * 0.022)` and a `48m`-wide **Central Emerald Reservoir Lake & 3-Step Waterfall Dam** at `X = -95m`.
     - Cluster `bldg_06` (Hydroponic Biodome), `bldg_09` (Aquifer Pumping Station right on the waterfall dam step at `r_floor = 178.0m`), `bldg_07` (Atmo Processor), `bldg_10` (Cryo Seed Vault on a `+12m` bluff at `r_floor = 173.5m`), and `bldg_08` (Astrometry Observatory on a `+16m` summit at `r_floor = 169.5m`), interleaved with dense organic groves of `prop_04` (Emerald Planter Pods) at `sc = 2.8..3.8`.
   - **Valley C (`phi_center = 300°` Industrial Port, Shipyard & Fusion Ridge):**
     - Replace the blue water canal with a **Heavy Brushed-Steel (`#88929E`) & Signal-Orange (`#D95B26`) Intermodal Mag-Rail Trench & Plasma Busbar Conduit**.
     - Arrange `bldg_12` (Fusion Reactor), `bldg_13` (Cargo Port), `bldg_16` (Shipyard Drydock), `bldg_19` (Refinery), `bldg_20` (Meteor Defense Bastion), and `bldg_15` (Solar/Shield Pylon) on heavy gunmetal (`#1A1E24`) stepped industrial switchyard decks (`r_floor = 185.5m, 179.0m, 173.0m`) spanned overhead by crane gantries and `prop_05` VTOL cargo pads.
3. **Macro-Setpiece & Radial Spoke Injection (`_build_interior_axial_and_valley_infrastructure`):**
   - Add the **3 Radial Tether-Elevator Spokes** connecting the Axial Hub (`X = -115m, Y = 200m, Z = 0m`) down to Valley A (`180°`), Valley B (`60°`), and Valley C (`300°`), with glowing elevator cars along the cables.
   - Add the **120° Curved Ring-Spanning Suspension Skybridge Viaduct** at `X = -115m` curving up the cylinder hull from `phi = 180°` through `phi = 120°` (across the solarium window strip!) to `phi = 60°` and `phi = 300°`.
   - Add the **Forward Endcap Stepped Cliffside Terraces & Radial Funicular Spine** at `X = -285m..-225m`.
4. **Upgraded 6-Camera Cinema Framing (`CAMERAS` Array):**
   - `cam_01_axial_megastructure_overview`: Wide forward-to-aft vista showcasing the 3 distinct color-coded valleys (Amber/Cyan Civic at `180°`, Emerald/UV Biosphere at `60°`, Orange/Steel Industrial at `300°`), the radial elevator spokes, and the curved Ring-Spanning Skybridge Viaduct.
   - `cam_02_valley_a_acropolis_looking_up`: Low-altitude human-scale shot in Valley A's stepped Civic Canyon looking past the Command Citadel Acropolis and diagonal skywalks up the curved Ring-Spanning Viaduct toward the overhead Emerald Biosphere valley (`60°`).
   - `cam_03_valley_b_waterfall_biosphere_delta`: Scenic overlook in Valley B (`60°`) framing the meandering river delta, stepped cyan/emerald waterfall dam, terraced biodome hills, and radial tether spoke rising to the sun-core.
   - `cam_04_valley_c_shipyard_and_fusion_port`: Dramatic industrial angle in Valley C (`300°`) across the Shipyard Drydock (`bldg_16`), 5-Coil Fusion Reactor (`bldg_12`), and Point-Defense Laser Bastions (`bldg_20`) toward the Aft Starport throat.
   - `cam_05_ring_skybridge_midspan_vista`: Camera perched on the `R = 152m` Mid-Span Sky-Transfer Rotunda of the curved suspension viaduct looking across the 400m diameter drum.
   - `cam_06_aft_starport_throat_to_forward_cliff_citadel`: View from the Aft Zero-G Starport throat looking forward toward the stepped Forward Endcap Cliffside Citadel (`X = -285m`).
