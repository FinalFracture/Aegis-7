# Phase 3 Master Architectural & Sci-Fi Movie Prop Specification (`prop_01`–`prop_05` & `bldg_16`–`bldg_20`)
**Author:** Vance (`0724beeb-94b9-43fa-a9cf-27117c5d4aa6`) — Sci-Fi Architect, Movie Prop & Set Design Specialist (with Sloane, Rook, Gage, Scribe & Atlas)
**Canonical Path:** `/workspace/game-project/design/phase3_props_and_buildings_16_20_spec.md`
**Standard:** Unified "Aegis-7 Standard" (Single-Architect Hard Sci-Fi Cinema Set Design — *2001*, *Alien*, *Oblivion*, *Elysium*, *Moon*)
**Scope:**
- **Part A — 5 Exterior Sci-Fi Movie Set & Plaza Prop Rounds (`prop_01`–`prop_05`):** 5 candidates each (`_r1_01`..`_r1_05` = 25 `.glb` models in `/workspace/game-project/assets/glb/props/prop_XX/`, `1,500–3,500` tris each), rendered to `/workspace/game-project/godot/renders/props/prop_XX/prop_XX_round1_voting_sheet.png`.
- **Part B — 5 District IV Building Exteriors (`bldg_16`–`bldg_20`):** 5 candidates each (`_r1_01`..`_r1_05` = 25 `.glb` models in `/workspace/game-project/assets/glb/buildings/bldg_XX/`, `3,000–6,000` tris each), rendered to `/workspace/game-project/godot/renders/buildings/bldg_XX/bldg_XX_round1_voting_sheet.png`.
- **Part C — District IV Showcase Scene & 20-Building Grand Metropolis Integration:** `district_04_shipyard_civic.tscn` (`renders/buildings/district_04/`) and the expanded 20-building + street-prop `cylinder_hab7_metropolis.tscn` (`renders/buildings/metropolis/`).

---

## 1. Unified Aegis-7 Exterior Material, Lighting & Geometry Rules
Every Phase 3 prop (`prop_01`–`prop_05`) and District IV building (`bldg_16`–`bldg_20`) strictly obeys the locked Aegis-7 Standard:

1. **65/35 & 68/32 Asymmetric Split-Mass Silhouette (`Candidate #02` Signature):**
   - **Candidate `#02` in every single round (`prop_01`–`prop_05` and `bldg_16`–`bldg_20`)** executes our signature **Aegis-7 Dual-Zone Split-Bay Architecture**:
     - **Left 65–68% Primary Zone:** Heavy load-bearing structural shell, hangar, arena, vault, or pylon in **Matte Aerospace White (`#D8DEE6`)** and **Dark Anodized Gunmetal Titanium (`#1A1E24`)** with 45° chamfered corner buttresses and **Signal-Orange (`#D95B26`)** functional latches, docking collars, or blast portals.
     - **Right 32–35% Secondary Zone:** Full-height **Machined Brushed Steel (`#88929E`)** and **Dark Carbon Slate (`#282E38`)** frame enclosing a **true `alphaMode: "BLEND"` translucent glass (`alpha 0.28–0.42`)** cabin, holo-chamber, ion-filter column, aeroponic canopy, radar mast, zero-G shuttle drydock gantry, centrifuge conditioning tower, Earth-biosphere holo-orrery spire, botanical distillation column, or tachyon beam-relay tower—revealing real 3D interior structures, floor slabs, coils, foliage, or holograms inside!
2. **Unified Material & Texture Assignments (`< 1.2%` Micro-Noise PBR):**
   - **Primary Hull & Chamfered Plinths:** Dark Anodized Gunmetal Titanium (`#1A1E24`, `metallic: 0.78`, `roughness: 0.34`, `facade_titanium_gunmetal_hull.png` / `metal_gunmetal_hull.png`)
   - **Molded Composite Cladding:** Matte Aerospace White (`#D8DEE6`, `metallic: 0.08`, `roughness: 0.30`, `facade_aerospace_white_cladding.png` / `panel_aerospace_white.png`)
   - **Spandrels, Louvers & Frames:** Dark Carbon Slate (`#282E38`, `metallic: 0.58`, `roughness: 0.40`, `facade_carbon_slate_spandrel.png` / `carbon_slate_frame.png`)
   - **Precision Gantries, Trusses & Dishes:** Brushed Machined Steel (`#88929E`, `metallic: 0.90`, `roughness: 0.22`, `facade_brushed_steel_gantry.png` / `metal_brushed_steel.png`)
   - **Functional Safety & Docking Hardware:** Signal-Orange (`#D95B26`, `metallic: 0.25`, `roughness: 0.38`, `accent_signal_orange.png`)
   - **Recessed Practical LEDs:** Cyan (`#00E5FF`, `led_cyan_strip.png`), UV-Violet (`#7B5CFF`, `led_uv_violet.png`), and Amber (`#FF9500`, `led_amber_strip.png`)
   - **Translucent Glass (`alphaMode: "BLEND"`, `alpha 0.28–0.42`):** `glass_curtainwall_cyan_translucent.png` (`#7CE8FF`) and `glass_biodome_emerald_translucent.png` (`#58E8B8`)
3. **Pivot & Orientation Convention:**
   - Every `.glb` model has its bottom-center pivot at `(0.0, 0.0, 0.0)` (`min Y = 0.00000`), faces `+Z`, and sits on a 45° chamfered octagonal `#1A1E24` gunmetal plinth with recessed `#FF9500` amber perimeter safety strips.

---

## 2. PART A — 5 Exterior Sci-Fi Movie Set & Plaza Prop Rounds (`prop_01` – `prop_05`)
*Output Directory: `/workspace/game-project/assets/glb/props/prop_01/` .. `prop_05/` | Renders: `/workspace/game-project/godot/renders/props/prop_01/` .. `prop_05/` | Budget: `1,500–3,500` tris per candidate.*

### 1. Prop 01 (`prop_01_maglev_shuttle_pylon`) — Elevated Mag-Lev Guideway Pylon & Aerodynamic Ring-Transit Pod
- **Envelope Dimensions:** `8.5m W × 4.8m D × 7.8m H` | **Target Triangle Budget:** `2,200–3,400` tris
- **Role in Scene:** Street-level and boulevard transit set piece bridging our District plazas; pairs an elevated mag-lev rail segment and support pylon with a docked sleek ring-transit passenger shuttle pod.
- **5-Candidate Lineup (`prop_01_r1_01.glb` .. `prop_01_r1_05.glb`):**
  1. `prop_01_r1_01.glb` — **#01 — Symmetric Octagonal Mag-Lev Guideway T-Pylon & Pod** (`~2,450` tris): Centered octagonal gunmetal T-column supporting a single overhead track beam and centered shuttle car.
  2. `prop_01_r1_02.glb` — **#02 — Dual-Zone Split Mag-Lev Guideway Y-Pylon, Docked Shuttle Pod & Translucent Telemetry Spine (Aegis-7 65/35 Signature)** (`~2,850` tris):
     - **Left 65% Primary Zone:** Heavy 45°-chamfered gunmetal (`#1A1E24`) and carbon-slate (`#282E38`) cantilevered Y-pylon supporting a brushed-steel (`#88929E`) magnetic induction guideway track (`Y = 5.2m`) with glowing cyan (`#00E5FF`) levitation coils, atop which sits an aerodynamic matte aerospace-white (`#D8DEE6`) **Ring-Transit Passenger Pod** featuring a `alphaMode: "BLEND"` wrap-around cockpit canopy (revealing 3D interior contoured crew seats and pilot console) and **Signal-Orange (`#D95B26`)** boarding door clamps.
     - **Right 35% Secondary Zone:** Full-height (`7.8m`) brushed-steel & `alphaMode: "BLEND"` translucent cyan glass **Traction Telemetry & Platform Boarding Spine** revealing 3D internal copper/cyan induction busbars, commuter status rings, and a ground-level emergency brake override cabinet (`#D95B26` handle).
  3. `prop_01_r1_03.glb` — **#03 — Twin-Cantilevered Mag-Lev Arch Gantry & Express Pod** (`~2,680` tris): Straddling portal arch with overhead catenary rails and suspended pod.
  4. `prop_01_r1_04.glb` — **#04 — Heavy Buttressed Traction Substation Pylon & Rail Segment** (`~2,520` tris): Industrial transformer base supporting a dual-rail mag-lev deck.
  5. `prop_01_r1_05.glb` — **#05 — Suspended Monorail Truss Pylon & Signal Portal** (`~2,610` tris): Open space-frame truss pylon with anunderslung transit car and amber signal bridge.

### 2. Prop 02 (`prop_02_holo_wayfinding_kiosk`) — Octagonal Pedestrian Wayfinding & Sector Telemetry Holo-Kiosk
- **Envelope Dimensions:** `3.2m W × 2.6m D × 3.8m H` | **Target Triangle Budget:** `1,800–3,100` tris
- **Role in Scene:** Human-scale pedestrian plaza movie prop placed outside building entrances to establish street-level scale (`1.8m` eye-level screens, `2.4m` holo-canopy) and sector signage.
- **5-Candidate Lineup (`prop_02_r1_01.glb` .. `prop_02_r1_05.glb`):**
  1. `prop_02_r1_01.glb` — **#01 — Symmetric Octagonal Holo-Directory Totem** (`~2,100` tris): Vertical 4-sided directory monolith with a top holo-ring.
  2. `prop_02_r1_02.glb` — **#02 — Dual-Zone Split Sector Wayfinding Holo-Kiosk & Translucent Emergency Breather Locker (Aegis-7 65/35 Signature)** (`~2,580` tris):
     - **Left 65% Primary Zone:** Chamfered aerospace-white (`#D8DEE6`) and gunmetal (`#1A1E24`) interactive wayfinding console with angled `signage_aegis7_building_marquees.png` touch-deck, overhead cantilevered weather/glare hood, and an `alphaMode: "BLEND"` translucent cyan **3D O'Neill Cylinder Holographic Sector Map Chamber** revealing a miniature glowing 3D cylinder wireframe and rotating sector ring inside.
     - **Right 35% Secondary Zone:** Full-height (`3.8m`) brushed-steel (`#88929E`) & `alphaMode: "BLEND"` translucent glass **Emergency O2 Breather, Defibrillator & Comms Totem** with a **Signal-Orange (`#D95B26`)** quick-release latch frame, visible 3D twin emergency O2 rebreather canisters inside, and an apex amber/cyan distress beacon.
  3. `prop_02_r1_03.glb` — **#03 — Tri-Wing Plaza Information Rotunda & Beacon** (`~2,320` tris): Three radial terminal wings around a central light column.
  4. `prop_02_r1_04.glb` — **#04 — Cantilevered Canopy Map Terminal & Comms Bench** (`~2,410` tris): L-shaped terminal with an integrated single-seat rest perch.
  5. `prop_02_r1_05.glb` — **#05 — Cylindrical Orbital Cylinder Map Projector Pedestal** (`~2,250` tris): Waist-high octagonal holo-table projector with overhead ring receiver.

### 3. Prop 03 (`prop_03_atmo_scrubber_bollard`) — Street-Level Atmospheric Scrubber Vent & Spin-Gravity Balancer Bollard
- **Envelope Dimensions:** `3.4m W × 2.8m D × 4.2m H` | **Target Triangle Budget:** `1,800–3,200` tris
- **Role in Scene:** Hard sci-fi environmental engineering movie prop lining promenade edges—scrubbing street-level CO2/particulates while providing heavy magnetic EVA safety tether rings.
- **5-Candidate Lineup (`prop_03_r1_01.glb` .. `prop_03_r1_05.glb`):**
  1. `prop_03_r1_01.glb` — **#01 — Octagonal Louvered Air-Intake Plaza Bollard** (`~2,050` tris): Symmetrical octagonal vent stack with carbon-slate intake grilles.
  2. `prop_03_r1_02.glb` — **#02 — Dual-Zone Split Venturi Scrubber Intake & Translucent Ion-Filter / EVA Tether Bollard (Aegis-7 65/35 Signature)** (`~2,640` tris):
     - **Left 65% Primary Zone:** Heavy 45°-chamfered gunmetal (`#1A1E24`) and aerospace-white (`#D8DEE6`) **Venturi Air-Intake & Acoustic Damper Housing** with recessed carbon-slate (`#282E38`) intake louvers, glowing cyan (`#00E5FF`) airflow telemetry bars, and heavy **Signal-Orange (`#D95B26`) EVA Safety Tether Anchor Rings** + pressure-relief handwheel.
     - **Right 35% Secondary Zone:** Full-height (`4.2m`) brushed-steel (`#88929E`) & `alphaMode: "BLEND"` translucent glass **Electrostatic Ion-Filter & UV Bio-Sterilizer Column** revealing 3D stacked glowing cyan (`#00E5FF`) and UV-violet (`#7B5CFF`) ionization baffle plates and a central spin-harmonic gyroscope core.
  3. `prop_03_r1_03.glb` — **#03 — Twin-Turbine Street Corner Air-Exchange Stack** (`~2,390` tris): Dual cylindrical intake cowls on a shared manifold plinth.
  4. `prop_03_r1_04.glb` — **#04 — Armored Spin-Harmonic Damper & O2 Monitor Post** (`~2,210` tris): Low-profile counterweight bunker with vertical sensor mast.
  5. `prop_03_r1_05.glb` — **#05 — Terraced UV-Biofilter Vent & Safety Strobe Pylon** (`~2,450` tris): Stepped louver bollard crowned by a 360° amber fog strobe.

### 4. Prop 04 (`prop_04_civic_planter_bench_pod`) — Terraced Aeroponic Civic Planter & Contoured Crew Bench Pod
- **Envelope Dimensions:** `5.2m W × 3.4m D × 3.6m H` | **Target Triangle Budget:** `2,000–3,400` tris
- **Role in Scene:** Pedestrian rest and biophilic life-support island combining contoured crew seating with UV-lit aeroponic greenery (`foliage_aeroponic_herbs.png`).
- **5-Candidate Lineup (`prop_04_r1_01.glb` .. `prop_04_r1_05.glb`):**
  1. `prop_04_r1_01.glb` — **#01 — Octagonal Central Tree Planter & Perimeter Bench Ring** (`~2,280` tris): Wrap-around octagonal bench surrounding a central planter tub.
  2. `prop_04_r1_02.glb` — **#02 — Dual-Zone Split Contoured Crew Bench Lounge & Translucent UV-Aeroponic Planter Canopy (Aegis-7 65/35 Signature)** (`~2,790` tris):
     - **Left 65% Primary Zone:** Ergonomic cantilevered **Matte Aerospace-White (`#D8DEE6`) & Contoured Charcoal (`#242932`) Crew Seating Bench** on a chamfered gunmetal (`#1A1E24`) plinth with warm circadian **Amber (`#FF9500`) under-bench cove lighting**, brushed-steel (`#88929E`) armrests, a **Signal-Orange (`#D95B26`)** personal device inductive charge port, and an overhead angled solar-pergola louver wing.
     - **Right 35% Secondary Zone:** Full-height (`3.6m`) `alphaMode: "BLEND"` emerald/cyan glass (`glass_biodome_emerald_translucent.png`) **Vertical Aeroponic Botanical Column & Mist Terrarium** revealing 3D tiered green foliage clusters (`foliage_aeroponic_herbs.png`), UV-violet (`#7B5CFF`) grow-light rings, and an internal nutrient misting tube.
  3. `prop_04_r1_03.glb` — **#03 — Twin-Tiered Botanical Promenade Seating Island** (`~2,510` tris): Back-to-back contoured benches divided by a raised herb hedge.
  4. `prop_04_r1_04.glb` — **#04 — Curved Cylinder-Slope Leisure Bench & Herb Trough** (`~2,420` tris): Swept amphitheater-style bench matching the cylinder terrace curve.
  5. `prop_04_r1_05.glb` — **#05 — Cantilevered Solar-Pergola Bench & Hydro-Basin Pod** (`~2,630` tris): Shaded bench pod alongside a translucent water-reclamation fountain basin.

### 5. Prop 05 (`prop_05_vtol_medevac_pad_array`) — Octagonal VTOL Shuttle/Med-Evac Landing Pad & Gimbaled Telemetry Dish Array
- **Envelope Dimensions:** `10.5m W × 9.5m D × 6.8m H` | **Target Triangle Budget:** `2,400–3,500` tris
- **Role in Scene:** Hero aerospace movie-set prop for plazas, trauma centers, and port aprons—combining an elevated octagonal VTOL touchdown deck with magnetic wheel/skid clamps and a flight-control radar mast.
- **5-Candidate Lineup (`prop_05_r1_01.glb` .. `prop_05_r1_05.glb`):**
  1. `prop_05_r1_01.glb` — **#01 — Symmetric Octagonal Helipad Deck & Perimeter Strobes** (`~2,480` tris): Standard octagonal landing pad with perimeter safety net and corner strobes.
  2. `prop_05_r1_02.glb` — **#02 — Dual-Zone Split Octagonal VTOL Landing Deck & Translucent Radar / Telemetry Dish Control Tower (Aegis-7 65/35 Signature)** (`~3,180` tris):
     - **Left 65% Primary Zone:** Chamfered octagonal gunmetal (`#1A1E24`) and carbon-slate (`#282E38`) **Elevated VTOL Shuttle & Med-Evac Landing Pad** featuring a glowing **Cyan (`#00E5FF`) & Amber (`#FF9500`) H-Approach Reticle**, 4 articulated **Signal-Orange (`#D95B26`) Hydraulic Magnetic Skid-Lock Clamps**, recessed deck blast deflectors, and an angled crew boarding ramp.
     - **Right 35% Secondary Zone:** Full-height (`6.8m`) brushed-steel (`#88929E`) & `alphaMode: "BLEND"` translucent cyan glass **Flight-Control & Approach Telemetry Tower** revealing 3D internal optical glide-slope emitter rings, umbilical fuel/O2 reel drums, and a rooftop **Gimbaled Parabolic Radar Dish & Approach Strobe Beacon**.
  3. `prop_05_r1_03.glb` — **#03 — Cantilevered Med-Evac Docking Platform & Fuel Arm** (`~2,790` tris): Overhanging trauma pad with an articulated cryogenic refueling boom.
  4. `prop_05_r1_04.glb` — **#04 — Twin-Clamp Orbital Shuttle Berth & Approach Beacon** (`~2,690` tris): Heavy industrial cradle berth with dual magnetic arrestor rails.
  5. `prop_05_r1_05.glb` — **#05 — Elevated Magnetic Arrestor Pad & Weather Mast Array** (`~2,850` tris): Truss-supported landing deck flanked by twin anemometer/laser masts.

---

## 3. PART B — 5 District IV Building Exteriors (`bldg_16` – `bldg_20`): Shipyard, Arena, Museum, Refinery & Defense Sector
*Output Directory: `/workspace/game-project/assets/glb/buildings/bldg_16/` .. `bldg_20/` | Renders: `/workspace/game-project/godot/renders/buildings/bldg_16/` .. `bldg_20/` | Budget: `3,000–6,000` tris per candidate.*

### 16. Building 16 (`bldg_16_shipyard_drydock_hall`) — Axial Zero-G Micro-Shuttle Assembly & Repair Drydock Hall
- **Footprint & Envelope:** `13.0m W × 11.0m D × 18.5m H` | **Target Budget:** `4,200–5,800` tris
- **Candidate Lineup (`bldg_16_r1_01.glb` .. `bldg_16_r1_05.glb`):**
  1. `bldg_16_r1_01.glb` — **#01 — Octagonal High-Bay Spacecraft Hangar & Gantry Arch** (`~4,680` tris): Symmetrical high-bay drydock hall with an overhead structural crane arch.
  2. `bldg_16_r1_02.glb` — **#02 — Dual-Zone Split Shipyard Assembly Hall & Translucent Zero-G Micro-Shuttle Drydock Gantry Tower (Aegis-7 65/35 Signature)** (`~5,380` tris):
     - **Left 65% Primary Zone:** High-bay 45°-chamfered gunmetal (`#1A1E24`) and matte aerospace-white (`#D8DEE6`) **Pressurized Hull-Fabrication & Avionics Assembly Hall** with oversized **Signal-Orange (`#D95B26`)** segmented hangar blast doors, overhead brushed-steel (`#88929E`) magnetic crane bridge, and a rooftop **Flight-Test VTOL Pad**.
     - **Right 35% Secondary Zone:** Full-height (`18.5m`) brushed-steel & `alphaMode: "BLEND"` translucent cyan glass **Zero-G Vertical Micro-Shuttle Drydock Gantry Tower**, revealing a **3D orbital micro-shuttle airframe suspended vertically inside** surrounded by 4 articulated glowing cyan (`#00E5FF`) & amber (`#FF9500`) robotic laser-welding ring gantries.
  3. `bldg_16_r1_03.glb` — **#03 — Twin-Cradle Orbital Tender Repair Bay & Crane Truss** (`~4,890` tris): Dual external repair cradles flanked by parallel crane trusses.
  4. `bldg_16_r1_04.glb` — **#04 — Pressurized Hull-Fabrication Vault & Robotic Welding Spire** (`~4,750` tris): Armored metallurgy hall with a tall plasma-arc exhaust stack.
  5. `bldg_16_r1_05.glb` — **#05 — Cantilevered Flight-Test Launch Bay & Telemetry Dock** (`~5,020` tris): Elevated launch tube projecting out over a ground maintenance bay.

### 17. Building 17 (`bldg_17_coriolis_recreation_arena`) — Coriolis Kinetic Sports Arena & Centrifuge Conditioning Gymnasium
- **Footprint & Envelope:** `13.5m W × 11.5m D × 17.5m H` | **Target Budget:** `4,200–5,800` tris
- **Candidate Lineup (`bldg_17_r1_01.glb` .. `bldg_17_r1_05.glb`):**
  1. `bldg_17_r1_01.glb` — **#01 — Octagonal Domed Zero-G Sports Colosseum** (`~4,520` tris): Central octagonal stadium crowned by a translucent geodesic sports dome.
  2. `bldg_17_r1_02.glb` — **#02 — Dual-Zone Split Coriolis Kinetic Arena Hall & Translucent Multi-G Centrifuge Conditioning Tower (Aegis-7 65/35 Signature)** (`~5,290` tris):
     - **Left 65% Primary Zone:** Monumental chamfered aerospace-white (`#D8DEE6`) and gunmetal (`#1A1E24`) **Coriolis Kinetic Sports Colosseum** crowned by a faceted `alphaMode: "BLEND"` translucent **Zero-G Arena Dome** (revealing 3D internal illuminated cyan/amber goal rings and spectator tiers) and a grand **Signal-Orange (`#D95B26`)** athlete concourse portal.
     - **Right 35% Secondary Zone:** Full-height (`17.5m`) brushed-steel (`#88929E`) & `alphaMode: "BLEND"` translucent glass **Multi-G Centrifuge Conditioning & 2001-Style Running Track Tower**, revealing 4 stacked **3D rotating high-gravity centrifuge conditioning rings** glowing in cyan (`#00E5FF`) and UV-violet (`#7B5CFF`) around a central drive spindle.
  3. `bldg_17_r1_03.glb` — **#03 — Twin-Ringed Low-Gravity Track & Aquatic Recovery Dome** (`~4,810` tris): Dual circular track drums paired with a hydro-therapy dome.
  4. `bldg_17_r1_04.glb` — **#04 — Stepped Spectator Stadium & Hyperbaric Training Wing** (`~4,690` tris): Tiered stadium seating terraces overlooking an indoor court.
  5. `bldg_17_r1_05.glb` — **#05 — Cantilevered Zero-G Combat/Flight Sphere & Fitness Spire** (`~4,950` tris): Suspended translucent flight-sphere cantilevered off an athletic tower.

### 18. Building 18 (`bldg_18_colonial_holo_museum`) — Aegis-7 Colonial Archives, Earth-Memory Vault & Holo-Planetarium
- **Footprint & Envelope:** `13.0m W × 11.0m D × 18.0m H` | **Target Budget:** `4,100–5,700` tris
- **Candidate Lineup (`bldg_18_r1_01.glb` .. `bldg_18_r1_05.glb`):**
  1. `bldg_18_r1_01.glb` — **#01 — Monumental Octagonal Planetarium & Archive Rotunda** (`~4,490` tris): Classical octagonal rotunda capped by a star-projector dome.
  2. `bldg_18_r1_02.glb` — **#02 — Dual-Zone Split Colonial Archive Pavilion & Translucent Earth-Biosphere Holo-Orrery Tower (Aegis-7 65/35 Signature)** (`~5,240` tris):
     - **Left 65% Primary Zone:** Stepped 5-story matte aerospace-white (`#D8DEE6`) and gunmetal (`#1A1E24`) **Colonial History & Earth-Relic Archive Pavilion** crowned by a hemispherical `alphaMode: "BLEND"` **Celestial Holo-Planetarium Dome** and approached via a ceremonial plaza stair with a **Signal-Orange (`#D95B26`)** heritage vault portal.
     - **Right 35% Secondary Zone:** Full-height (`18.0m`) brushed-steel (`#88929E`) & `alphaMode: "BLEND"` translucent glass **Earth-Memory Optical Crystal & Holo-Orrery Spire**, revealing a **3D glowing cyan/emerald holographic Earth-Sol orbital orrery globe** and stacked UV-violet (`#7B5CFF`) optical memory-crystal archive carousels inside.
  3. `bldg_18_r1_03.glb` — **#03 — Twin-Wing Cultural Conservatory & Time-Capsule Vault** (`~4,720` tris): Symmetrical exhibition wings flanking a central time-capsule obelisk.
  4. `bldg_18_r1_04.glb` — **#04 — Stepped Ziggurat History Museum & Solar Obelisk** (`~4,610` tris): Terraced museum galleries ascending toward a tall commemorative needle.
  5. `bldg_18_r1_05.glb` — **#05 — Cantilevered Stargazer Auditorium & Memory Crystal Spire** (`~4,880` tris): Overhanging lecture auditorium balanced by a memory-core tower.

### 19. Building 19 (`bldg_19_synth_brewery_refinery`) — Bioreactor Protein Refinery & Zero-G Botanical Distillation Plant
- **Footprint & Envelope:** `13.0m W × 11.0m D × 17.5m H` | **Target Budget:** `4,200–5,800` tris
- **Candidate Lineup (`bldg_19_r1_01.glb` .. `bldg_19_r1_05.glb`):**
  1. `bldg_19_r1_01.glb` — **#01 — Octagonal Fermentation Hall & Copper/Steel Still Crown** (`~4,640` tris): Central fermentation plant with rooftop distillation domes.
  2. `bldg_19_r1_02.glb` — **#02 — Dual-Zone Split Protein Synthesis Refinery & Translucent Zero-G Botanical Distillation Column Tower (Aegis-7 65/35 Signature)** (`~5,410` tris):
     - **Left 65% Primary Zone:** Heavy chamfered gunmetal (`#1A1E24`) and aerospace-white (`#D8DEE6`) **Cellular Protein & Fermentation Refinery Hall** flanked by twin brushed-steel (`#88929E`) bioreactor vats, external nutrient transfer pipelines, **Signal-Orange (`#D95B26`)** tanker-docking valves, and an upper crew tasting balcony.
     - **Right 35% Secondary Zone:** Full-height (`17.5m`) brushed-steel & `alphaMode: "BLEND"` emerald/cyan translucent (`glass_biodome_emerald_translucent.png`) **Zero-G Botanical Fractional Distillation Tower**, revealing 6 stacked **3D glowing amber (`#FF9500`) & cyan (`#00E5FF`) copper/steel condensation bubble-plates**, helical vapor coils, and aeroponic botanical infusion rings.
  3. `bldg_19_r1_03.glb` — **#03 — Quad-Vat Bioreactor Array & Automated Bottling Hall** (`~4,920` tris): Four external fermentation cylinders over a bottling logistics bay.
  4. `bldg_19_r1_04.glb` — **#04 — Twin-Silo Cellular Agriculture Plant & Tasting Atrium** (`~4,780` tris): Dual protein silos paired with a glazed visitor tasting lounge.
  5. `bldg_19_r1_05.glb` — **#05 — Heavy Industrial Nutrient Fractionation & Storage Complex** (`~4,860` tris): Refinery pipe-rack block with overhead transfer gantries.

### 20. Building 20 (`bldg_20_meteor_defense_bastion`) — Point-Defense Laser Bastion & Deep-Space Tachyon Relay Tower
- **Footprint & Envelope:** `13.0m W × 11.0m D × 20.5m H` | **Target Budget:** `4,300–5,900` tris
- **Candidate Lineup (`bldg_20_r1_01.glb` .. `bldg_20_r1_05.glb`):**
  1. `bldg_20_r1_01.glb` — **#01 — Armored Octagonal Point-Defense Turret & Shield Citadel** (`~4,760` tris): Fortified octagonal bastion capped by a single heavy laser turret.
  2. `bldg_20_r1_02.glb` — **#02 — Dual-Zone Split Armored Defense Bastion & Translucent Tachyon / Capacitor Beam-Relay Tower (Aegis-7 65/35 Signature)** (`~5,540` tris):
     - **Left 65% Primary Zone:** Heavily buttressed 45°-chamfered dark gunmetal (`#1A1E24`) and aerospace-white (`#D8DEE6`) **Meteoroid Defense & Pulse-Capacitor Bastion** crowned by a gimbaled dual-barrel **Brushed-Steel (`#88929E`) & Cyan-Lens Point-Defense Coherent Laser Turret**, carbon-slate (`#282E38`) heat-sink fins, and a **Signal-Orange (`#D95B26`)** armored ordinance airlock.
     - **Right 35% Secondary Zone:** Full-height (`20.5m`) brushed-steel & `alphaMode: "BLEND"` translucent cyan glass **Tachyon Waveguide & Optical Beam-Relay Spire**, revealing 5 stacked **3D glowing cyan (`#00E5FF`) & UV-violet (`#7B5CFF`) optical focusing lenses**, a central pulse-laser excitation column, and an apex deep-space tachyon transceiver array.
  3. `bldg_20_r1_03.glb` — **#03 — Twin-Turret Meteoroid Interceptor & Radar Bunker** (`~5,010` tris): Dual elevated laser turrets flanking a central fire-control radar dome.
  4. `bldg_20_r1_04.glb` — **#04 — Stepped Capacitor Fortress & Subspace Phased-Array Spire** (`~4,890` tris): Tiered armor bunker supporting an angled phased-array radar panel.
  5. `bldg_20_r1_05.glb` — **#05 — Cantilevered Deep-Space Overwatch Battery & Comms Pylon** (`~5,120` tris): Overhanging gun-battery deck counterbalanced by a tall comms mast.

---

## 4. PART C — Godot 4 Scene Integration Coordinates (`district_04_shipyard_civic.tscn` & 20-Building `cylinder_hab7_metropolis.tscn`)

### 1. District IV Showcase Scene (`godot/scenes/buildings/district_04_shipyard_civic.tscn`)
- **Renders Output:** `/workspace/game-project/godot/renders/buildings/district_04/` (`cam_01`..`cam_03` + `district_04_shipyard_civic_sheet.png`)
- **Building Placements (`District04ShipyardCivic`):**
  - `Bldg16_ShipyardDrydockHall` (`bldg_16_winner_01_shipyard_drydock_hall.glb` / `bldg_16_r1_02.glb`): `pos = Vector3(-28.0, 0.0, -8.0)`, `rot_y = 15.0`
  - `Bldg17_CoriolisRecreationArena` (`bldg_17_winner_01_coriolis_recreation_arena.glb` / `bldg_17_r1_02.glb`): `pos = Vector3(-15.0, 0.0, 8.0)`, `rot_y = 5.0`
  - `Bldg18_ColonialHoloMuseum` (`bldg_18_winner_01_colonial_holo_museum.glb` / `bldg_18_r1_02.glb`): `pos = Vector3(0.0, 0.0, -14.0)`, `rot_y = 0.0`
  - `Bldg19_SynthBreweryRefinery` (`bldg_19_winner_01_synth_brewery_refinery.glb` / `bldg_19_r1_02.glb`): `pos = Vector3(15.0, 0.0, 8.0)`, `rot_y = -5.0`
  - `Bldg20_MeteorDefenseBastion` (`bldg_20_winner_01_meteor_defense_bastion.glb` / `bldg_20_r1_02.glb`): `pos = Vector3(28.0, 0.0, -8.0)`, `rot_y = -15.0`
- **Exterior Street-Level Props (`prop_01`–`prop_05` `#02` Winners) in District IV Plaza:**
  - `Prop01_MaglevShuttlePylon`: `Vector3(-22.0, 0.0, 6.0)` & `Vector3(22.0, 0.0, 6.0)`
  - `Prop02_HoloWayfindingKiosk`: `Vector3(-6.0, 0.0, 14.0)` & `Vector3(6.0, 0.0, 14.0)`
  - `Prop03_AtmoScrubberBollard`: `Vector3(-18.0, 0.0, 14.0)` & `Vector3(18.0, 0.0, 14.0)`
  - `Prop04_CivicPlanterBenchPod`: `Vector3(-10.0, 0.0, 4.0)` & `Vector3(10.0, 0.0, 4.0)`
  - `Prop05_VtolMedevacPadArray`: `Vector3(0.0, 0.0, 20.0)`

### 2. Expanded 20-Building + Street-Prop Grand Metropolis (`godot/scenes/buildings/cylinder_hab7_metropolis.tscn`)
- Expands `BUILDINGS` array in `cylinder_hab7_metropolis.gd` from 15 to **all 20 locked `#02` building winners (`bldg_01`–`bldg_20`)** arranged in 4 terraced O'Neill Cylinder rings (`Z = +22m`, `Z = +6m`, `Z = -14m`, `Z = -34m`), plus instances of all **5 locked `#02` exterior sci-fi street props (`prop_01`–`prop_05`)** along the central axial promenade, hydro-canal, and elevated mag-lev guideway!
