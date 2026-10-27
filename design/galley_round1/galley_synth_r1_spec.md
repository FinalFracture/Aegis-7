# Room 03 Hero Asset: Ration & Beverage Synthesizer Bank — Round 1 Design, 3D Galley Kit, Translucent Chambers & Lighting Spec
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Pipeline Stage:** Room 03 Hero Asset — 5-Choice Test (`galley_synth_r1_01` through `galley_synth_r1_05`)  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)  
**Target Teams:** Rook (3D Hard-Surface & Synthesizer/Beverage/Herb Modeling, Translucent Chamber Glass & UVs) & Gage (Godot 4 Scene Integration, Practical Lighting & 1080p Beauty Renders)

---

## 1. Shared Standards & Technical Rules ("Aegis-7 Standard")

### 1.1 Output Paths & Naming Convention
- **3D Models (`.glb`):** `/workspace/game-project/assets/glb/galley_round1/galley_synth_r1_01.glb` through `/workspace/game-project/assets/glb/galley_round1/galley_synth_r1_05.glb`
- **Winner Export Path (after all 5 renders complete & 5-Bot Vote):** `/workspace/game-project/assets/glb/winners/galley_synth_winner_01_...glb`
- **Texture Suite (`.png`):** `/workspace/game-project/assets/textures/galley_round1/` (and mirrored in `/workspace/game-project/assets/textures/`)
- **Individual 1080p Beauty Renders (`.png`):** `/workspace/game-project/assets/renders/galley_round1/galley_synth_r1_01.png` through `galley_synth_r1_05.png` (and mirrored in `/workspace/game-project/godot/renders/galley_round1/`)
- **5-Panel Voting Comparison Sheet:** `/workspace/game-project/assets/renders/galley_round1/galley_synth_round1_voting_sheet.png` (and mirrored in `/workspace/game-project/godot/renders/galley_round1/`)

### 1.2 Coordinate System, Galley Footprint & Pivot Convention
- **Metric Scale:** `1.0 unit = 1.0 meter`.
- **Target Galley Synthesizer Bank Footprint:** `1.85m – 2.10m Wide (X) × 0.72m – 0.82m Deep (Z) × 2.05m – 2.15m Tall (Y)`.
- **World Origin & Pivot Point:** Bottom-center `(0.0, 0.0, 0.0)` resting flush on the `Y = 0.0` floor plane (`min_y == 0.0000`, centered in `X` and `Z`), front serving counter & dispensing bays facing **`+Z`**, rear bulkhead mounting spine at **`-Z`**.
- **Polygon Budget:** **`3,200 – 5,800 triangles`** per candidate.

### 1.3 Mandatory 4-Part 3D Galley Synthesizer Kit (Required in Every Candidate!)
1. **45° Chamfered Bulkhead Housing & Brushed-Steel Serving Counter Deck (`Y ~ 0.88m`):**
   - Dark gunmetal titanium (`titanium_gunmetal_hull.png`, `#1A1E24`) and carbon-slate (`carbon_slate_frame.png`, `#282E38`) bulkhead unit with a wide brushed machined-steel (`steel_machined_gantry.png`, `#88929E`) and matte aerospace-white (`composite_aerospace_white.png`, `#D8DEE6`) serving counter featuring **3D recessed magnetic meal-tray bays** and **glowing cyan (`#00E5FF`) zero-G cup lock rings**.
2. **Translucent Thermal Synthesis & Ration Dispensing Chambers (`glass_synth_chamber_translucent.png`, `alphaMode: "BLEND"`, `alpha ~ 0.19`):**
   - Enclosed behind bevel-framed **`alphaMode: "BLEND"` translucent armored glass doors (`glass_synth_chamber_translucent.png`)**:
     * **3D Compartmentalized Aerospace-White Meal Trays** (`composite_aerospace_white.png`) with sculpted ration blocks/domes resting on heated induction racks.
     * **3D Cylindrical Protein/Amino Nutrient Cartridges & Sealed Ration Canisters** with signal-orange (`accent_signal_orange.png`, `#D95B26`) locking collars.
3. **Dual-Nozzle Hydration / Espresso Tap Arch + Widescreen OLED Nutri-Telemetry Console (`oled_nutri_synthesizer.png`):**
   - Sculpted machined-steel (`steel_machined_gantry.png`) multi-tap beverage & electrolyte hydration manifold with **two 3D insulated zero-G thermal flasks/mugs** seated underneath, signal-orange hot-steam purge valves, and a flush-mounted **`oled_nutri_synthesizer.png` caloric & thermal telemetry screen (`emissive_energy = 2.0`)**.
4. **Integrated Living Aeroponic Culinary Herb Strip (`foliage_aeroponic_herbs.png`):**
   - Recessed hydroponic/aeroponic trough (`foliage_aeroponic_herbs.png`) with 3D mounded culinary greens/herbs illuminated by an overhead **UV-violet (`#7B5CFF`) & cyan (`#00E5FF`) grow-light strip** behind a translucent splash baffle.

---

## 2. Texture & Material Library Manifest (`/workspace/game-project/assets/textures/galley_round1/`)

| # | Filename | Format | Base Hex / Tone | Roughness | Metallic | Alpha / Emissive & Material Usage |
|---|----------|--------|-----------------|-----------|----------|-----------------------------------|
| 1 | `titanium_gunmetal_hull.png` | RGB | `#1A1E24` | `0.34` | `0.78` | Primary 45° chamfered gunmetal titanium galley bulkhead housing |
| 2 | `composite_aerospace_white.png` | RGB | `#D8DEE6` | `0.28` | `0.08` | Smooth matte aerospace white synthesis bay liners, meal trays & nutrient canisters |
| 3 | `carbon_slate_frame.png` | RGB | `#282E38` | `0.40` | `0.58` | Dark carbon-slate counter substructure, tray slots & lower storage drawers |
| 4 | `steel_machined_gantry.png` | RGB | `#88929E` | `0.20` | `0.90` | Brushed machined steel for serving counter top, beverage tap arches, flasks & rails |
| 5 | `fabric_charcoal_flightpad.png` | RGB | `#242932` | `0.78` | `0.00` | Anti-slip counter mat pads & insulated flask grips |
| 6 | `fabric_orbital_navy_pad.png` | RGB | `#1D2C3C` | `0.76` | `0.00` | Soft-goods insulated ration packs stowed in lower racks |
| 7 | `accent_signal_orange.png` | RGB | `#D95B26` | `0.48` | `0.06` | Matte signal-orange for steam purge valves, cartridge locks & emergency cutoffs |
| 8 | `oled_nutri_synthesizer.png` | RGB | `#0A0E14` + `#00E5FF` | `0.14` | `0.10` | **`emission_enabled: true` (`energy = 2.0`)**, caloric/macro & 68.5°C thermal OLED display |
| 9 | `glass_synth_chamber_translucent.png` | **RGBA** | `#0E2230` + `#00E5FF` | `0.08` | `0.10` | **`alphaMode: "BLEND"` (`alpha ~ 0.19`)**, translucent synthesis chamber & ration tower doors |
| 10 | `foliage_aeroponic_herbs.png` | RGB | `#2E5A36` | `0.55` | `0.00` | Calm emerald/jade living culinary herb & micro-greens bed inside aeroponic trough |

---

## 3. Detailed Per-Candidate Specifications (`galley_synth_r1_01` through `galley_synth_r1_05`)

1. **`galley_synth_r1_01.glb` — `#01 — Aegis-7 Octagonal Bulkhead Ration Synthesizer & Beverage Bar` (`1.90m W × 0.76m D × 2.10m H`):**
   - Symmetrical 45° chamfered octagonal gunmetal bulkhead station: twin central translucent thermal synthesis ovens (`glass_synth_chamber_translucent.png`) with 3D heated meal trays inside, flanked on the left by the dual-nozzle beverage tap arch + thermal flasks and on the right by `oled_nutri_synthesizer.png`, topped by a full-width recessed aeroponic culinary herb bay (`foliage_aeroponic_herbs.png`) under UV-violet/cyan grow lights.
2. **`galley_synth_r1_02.glb` — `#02 — Dual-Zone Split Thermal Synthesizer & Translucent Ration/Herb Tower` (`2.00m W × 0.78m D × 2.12m H`):**
   - **Direct asymmetric 65% / 35% split-bay sibling to all 5 locked Aegis-7 winners!**
   - **Left Bay (65% width, `1.30m` wide):** Main chamfered galley counter (`Y = 0.88m`) with dual recessed translucent thermal synthesis chambers (`glass_synth_chamber_translucent.png`) holding 3D aerospace-white compartmentalized meal trays, the sculpted brushed-steel hydration/coffee dispenser arch with two 3D zero-G flasks on glowing cyan coaster rings, widescreen `oled_nutri_synthesizer.png` console, and lower pull-out tray-return/waste-compactor drawers with signal-orange latches.
   - **Right Bay (35% width, `0.70m` wide):** Full-height 3-tier **Translucent Nutrient Cartridge & Living Aeroponic Herb Tower** enclosed by a bevel-framed **`alphaMode: "BLEND"` translucent glass door (`glass_synth_chamber_translucent.png`)**:
     * Top tier: 6 vertical cylindrical protein/electrolyte nutrient canisters (`composite_aerospace_white.png` with signal-orange valve collars).
     * Middle tier: Illuminated living aeroponic culinary herb trough (`foliage_aeroponic_herbs.png`) with 3D mounded greens under a `#7B5CFF` UV-violet grow bar.
     * Bottom tier: Stacked 3D sealed crew ration cases & spare thermal flasks.
3. **`galley_synth_r1_03.glb` — `#03 — Rotary Carousel Automaton Dispenser & Espresso Tap Alcove` (`1.88m W × 0.80m D × 2.10m H`):**
   - Features a central vertical cylindrical **rotary ration carousel behind a curved `glass_synth_chamber_translucent.png` window** (displaying 3 rotating tiers of 3D meal trays & canisters), paired with a left high-pressure espresso/hydration tap bay with signal-orange steam wand and a right `oled_nutri_synthesizer.png` ordering kiosk + herb strip.
4. **`galley_synth_r1_04.glb` — `#04 — Cantilevered Island Galley Module & Overhead Nutrient Manifold` (`1.95m W × 0.78m D × 2.12m H`):**
   - Sleek cantilevered aerospace-white & brushed-steel serving counter suspended from heavy rear titanium pillars with an overhead canopy housing exposed cylindrical nutrient feed manifolds, suspended translucent herb trough, and eye-level translucent synthesis bays.
5. **`galley_synth_r1_05.glb` — `#05 — Heavy Crew Mess Quad-Chamber Induction Synthesizer & Tray Return` (`2.05m W × 0.78m D × 2.12m H`):**
   - High-capacity 2×2 quad-grid of bevel-framed translucent induction synthesis chambers (`glass_synth_chamber_translucent.png`) glowing with warm amber (`#FF9500`) and cyan (`#00E5FF`) chamber lights, dual central hydration taps, lower magnetic tray-stacking conveyor slot, and upper aeroponic herb trough.

---

## 4. Standardized Camera Framing & Lighting Guide (`Gage` & `Rook`)

- **Target Look-At Point:** `(0.0, 1.05, 0.0)`
- **Camera Angles:** 3/4 front-isometric beauty angle (`yaw = ±20° to ±24°`, `pitch = -12°`, distance `~2.75m – 3.00m`, `FOV = 46°`).
- **Practical Lights:**
  1. `Synth_Chamber_Warm_Amber`: Local Pos `(-0.30, 1.18, 0.10)`, Color `#FF9500`, Energy `1.45`, Range `2.0m` (warms the 3D meal trays inside the translucent synthesis chambers).
  2. `Counter_And_Tap_Cyan_Task`: Local Pos `(-0.35, 1.55, 0.25)`, Color `#00E5FF`, Energy `1.50`, Range `2.2m`.
  3. `Aeroponic_Herb_UV_Grow`: Local Pos `(+0.52, 1.35, 0.12)`, Color `#7B5CFF`, Energy `1.35`, Range `1.9m`.
