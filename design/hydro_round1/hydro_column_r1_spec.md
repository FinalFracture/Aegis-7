# Room 06 Hero Asset: Vertical Translucent Aeroponic Planter & Bio-Air Scrubber Tower — Round 1 Design Spec
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Pipeline Stage:** Room 06 Hero Asset — 5-Choice Test (`hydro_column_r1_01` through `hydro_column_r1_05`)  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)  
**Target Teams:** Rook (3D Hard-Surface & Rotary Aeroponic Column/Bioreactor Modeling, Translucent Borosilicate Enclosure & UVs) & Gage (Godot 4 Scene Integration, UV-Violet/Cyan Photosynthetic Lighting & 1080p Beauty Renders)

---

## 1. Shared Standards & Technical Rules ("Aegis-7 Standard")

### 1.1 Output Paths & Naming Convention
- **3D Models (`.glb`):** `/workspace/game-project/assets/glb/hydro_round1/hydro_column_r1_01.glb` through `/workspace/game-project/assets/glb/hydro_round1/hydro_column_r1_05.glb`
- **Winner Export Path (after all 5 renders complete & 5-Bot Vote):** `/workspace/game-project/assets/glb/winners/hydro_column_winner_01_...glb`
- **Texture Suite (`.png`):** `/workspace/game-project/assets/textures/hydro_round1/` (and mirrored in `/workspace/game-project/assets/textures/`)
- **Individual 1080p Beauty Renders (`.png`):** `/workspace/game-project/assets/renders/hydro_round1/hydro_column_r1_01.png` through `hydro_column_r1_05.png` (and mirrored in `/workspace/game-project/godot/renders/hydro_round1/`)
- **5-Panel Voting Comparison Sheet:** `/workspace/game-project/assets/renders/hydro_round1/hydro_column_round1_voting_sheet.png` (and mirrored in `/workspace/game-project/godot/renders/hydro_round1/`)

### 1.2 Coordinate System, Bio-Tower Footprint & Pivot Convention
- **Metric Scale:** `1.0 unit = 1.0 meter`.
- **Target Aeroponic Tower Footprint:** `1.85m – 2.05m Wide (X) × 0.85m – 0.95m Deep (Z) × 2.40m – 2.50m Tall (Y)`.
- **World Origin & Pivot Point:** Bottom-center `(0.0, 0.0, 0.0)` resting flush on the `Y = 0.0` floor plane (`min_y == 0.0000`, centered in `X` and `Z`), front inspection glass & OLED console facing **`+Z`**, rear manifold spine at **`-Z`**.
- **Polygon Budget:** **`3,600 – 6,000 triangles`** per candidate.

### 1.3 Mandatory 4-Part 3D Aeroponic & Bio-Scrubber Kit (Required in Every Candidate!)
1. **45° Chamfered Octagonal Base Sump & Overhead O2 Scrubber Crown (`Y = 0.0m – 2.45m`):**
   - Dark gunmetal titanium (`titanium_gunmetal_hull.png` / `metal_gunmetal_hull.png`, `#1A1E24`) and carbon-slate (`carbon_slate_frame.png` / `metal_carbon_slate.png`, `#282E38`) structural base sump and top atmospheric intake plenum with sculpted laminar air-scrubber louvers.
2. **Translucent Borosilicate Aeroponic Growth Column (`glass_hydro_cylinder_translucent.png`, `alphaMode: "BLEND"`, `alpha ~ 0.19`) + 3D Multi-Tier Foliage Rings (`foliage_aeroponic_herbs.png`):**
   - Tall cylindrical or faceted **`alphaMode: "BLEND"` translucent borosilicate glass enclosure (`glass_hydro_cylinder_translucent.png`)** housing a central brushed-steel (`steel_machined_gantry.png` / `metal_brushed_steel.png`, `#88929E`) ultrasonic misting spindle and **4 stacked aerospace-white (`composite_aerospace_white.png` / `panel_aerospace_white.png`, `#D8DEE6`) rotary planter trays** overflowing with **3D sculpted emerald/jade botanical foliage clusters (`foliage_aeroponic_herbs.png`)**!
   - Each growth tier is ringed by an underside **UV-Violet (`#7B5CFF`, `led_uv_violet.png`) and Surgical Ice-White (`#E0F4FF`, `led_ice_white.png`) photosynthetic grow-light halo**.
3. **Illuminated Chlorella Algae / Zeolite O2 Bio-Scrubber Cylinders & Nutrient Dosing Manifold:**
   - Twin auxiliary translucent bioreactor tubes (`glass_hydro_cylinder_translucent.png`) glowing with cyan/emerald oxygenation light (`#00E5FF`), connected via swept machined-steel nutrient pipes, peristaltic dosing pumps, and **signal-orange (`accent_signal_orange.png` / `accent_safety_orange.png`, `#D95B26`) nutrient purge & CO2 bypass valves**.
4. **Photosynthetic & O2 Exchange OLED Telemetry Console (`oled_hydro_bioscrubber.png`):**
   - Flush-mounted **`oled_hydro_bioscrubber.png` display (`emissive_energy = 2.0`)** showing `+42.8 L/min O2` output, `99.4% CO2` scrubbing efficiency, and chlorophyll fluorescence curves.

---

## 2. Texture & Material Library Manifest (`/workspace/game-project/assets/textures/hydro_round1/`)

| # | Canonical Filename (Alias) | Format | Base Hex / Tone | Roughness | Metallic | Alpha / Emissive & Material Usage |
|---|----------------------------|--------|-----------------|-----------|----------|-----------------------------------|
| 1 | `titanium_gunmetal_hull.png` (`metal_gunmetal_hull.png`) | RGB | `#1A1E24` | `0.34` | `0.78` | Primary 45° chamfered gunmetal titanium base sump & top O2 scrubber plenum |
| 2 | `composite_aerospace_white.png` (`panel_aerospace_white.png`) | RGB | `#D8DEE6` | `0.28` | `0.08` | Smooth matte aerospace white rotary aeroponic planter rings & nutrient tanks |
| 3 | `carbon_slate_frame.png` (`metal_carbon_slate.png`) | RGB | `#282E38` | `0.40` | `0.58` | Dark carbon-slate structural pillars, intake louvers & pump housings |
| 4 | `steel_machined_gantry.png` (`metal_brushed_steel.png`) | RGB | `#88929E` | `0.20` | `0.90` | Brushed machined steel for central ultrasonic misting spindle, pipes & clamps |
| 5 | `foliage_aeroponic_herbs.png` | RGB | `#2E5A36` | `0.52` | `0.00` | Calm emerald/jade 3D botanical foliage clusters & micro-greens |
| 6 | `accent_signal_orange.png` (`accent_safety_orange.png`) | RGB | `#D95B26` | `0.48` | `0.06` | Matte signal-orange for nutrient dosing valves, CO2 bypass wheels & drain latches |
| 7 | `oled_hydro_bioscrubber.png` | RGB | `#0A0E14` + `#00E5FF` | `0.14` | `0.10` | **`emission_enabled: true` (`energy = 2.0`)**, 512×512 O2/CO2 & photosynthetic OLED |
| 8 | `glass_hydro_cylinder_translucent.png` | **RGBA** | `#0D262C` + `#00E5FF` | `0.08` | `0.10` | **`alphaMode: "BLEND"` (`alpha ~ 0.19`)**, 256×256 translucent borosilicate planter & bioreactor glass |
| 9 | `led_uv_violet.png` / `led_cyan_strip.png` / `led_ice_white.png` / `led_amber_strip.png` | RGB | `#7B5CFF` / `#00E5FF` / `#E0F4FF` / `#FF9500` | `0.15` | `0.00` | Emissive photosynthetic grow-light rings & status indicators |

---

## 3. Detailed Per-Candidate Specifications (`hydro_column_r1_01` through `hydro_column_r1_05`)

1. **`hydro_column_r1_01.glb` — `#01 — Aegis-7 Octagonal Translucent Aeroponic Bio-Tower` (`1.90m W × 0.90m D × 2.45m H`):**
   - Symmetrical octagonal-framed vertical borosilicate glass growth cylinder (`glass_hydro_cylinder_translucent.png`) containing 4 stacked aerospace-white rotary planter tiers with lush 3D foliage (`foliage_aeroponic_herbs.png`), flanked by twin vertical machined-steel nutrient columns and a front-center `oled_hydro_bioscrubber.png` pedestal.
2. **`hydro_column_r1_02.glb` — `#02 — Dual-Zone Split Aeroponic Rotary Column & O2 Algae Bio-Scrubber Bay` (`2.00m W × 0.90m D × 2.45m H`):**
   - **Signature 65% / 35% asymmetric split-bay Aegis-7 sibling to all locked winners!**
   - **Left Bay (65% width, `1.30m` wide):** Full-height **Vertical Translucent Rotary Aeroponic Planter Column** enclosed by curved/faceted **`alphaMode: "BLEND"` borosilicate glass (`glass_hydro_cylinder_translucent.png`)** inside a 45° chamfered gunmetal titanium frame. Inside: a central brushed-steel ultrasonic misting spindle supporting **4 stacked spiral/tiered aerospace-white planter rings** packed with **3D sculpted emerald/jade botanical leaf clusters (`foliage_aeroponic_herbs.png`)**, each illuminated from above by alternating **UV-Violet (`#7B5CFF`) and Daylight Ice-White (`#E0F4FF`) grow-light halos**!
   - **Right Bay (35% width, `0.70m` wide):** Integrated **Atmospheric O2 Bio-Scrubber & Nutrient Manifold Bay**:
     * Upper Tier (`Y = 1.45m–2.30m`): **Twin vertical translucent Chlorella Algae / Zeolite Bioreactor Cylinders** (`glass_hydro_cylinder_translucent.png`) with internal glowing cyan (`#00E5FF`) bubble-diffuser cores and top laminar O2 exhaust louvers.
     * Center Tier (`Y = 0.88m–1.42m`): Flush-mounted **`oled_hydro_bioscrubber.png` photosynthetic & O2 telemetry console**, paired with 3D machined-steel peristaltic nutrient dosing pumps.
     * Lower Tier (`Y = 0.14m–0.84m`): Twin aerospace-white nutrient reservoir canisters with swept steel manifold pipes and a **sculpted signal-orange rotary purge handwheel**.
3. **`hydro_column_r1_03.glb` — `#03 — Twin-Helix Vertical Bioreactor & Micro-Greens Carousel` (`1.95m W × 0.90m D × 2.45m H`):**
   - Twin side-by-side translucent glass aeroponic cylinders linked by a central helical brushed-steel irrigation spine and central `oled_hydro_bioscrubber.png` control pillar.
4. **`hydro_column_r1_04.glb` — `#04 — Hex-Faceted Terraced Terrarium Alcove & UV Mist Gantry` (`2.02m W × 0.92m D × 2.45m H`):**
   - Wide hexagonal-beveled botanical bay with 3 stepped amphitheater hydroponic troughs behind angled sliding `glass_hydro_cylinder_translucent.png` doors and an overhead translating UV-violet misting bar.
5. **`hydro_column_r1_05.glb` — `#05 — Zero-G Centrifugal Drum Planter & Atmospheric Revitalizer` (`1.98m W × 0.94m D × 2.48m H`):**
   - Features a horizontal/tilted rotating cylindrical drum planter glazed with `glass_hydro_cylinder_translucent.png` (where plants grow radially inward toward a central axial UV-violet grow lamp), mounted above a twin-canister CO2 scrubber & nutrient sump base.

---

## 4. Standardized Camera Framing & Lighting Guide (`Gage` & `Rook`)

- **Target Look-At Point:** `(0.0, 1.22, 0.0)`
- **Camera Angles:** Heroic 3/4 front-isometric beauty angle (`yaw = ±18° to ±22°`, `pitch = -11°`, distance `~2.95m – 3.20m`, `FOV = 46°`).
- **Practical Lights:**
  1. `Aeroponic_Column_UV_Grow`: Local Pos `(-0.32, 1.65, 0.05)`, Color `#7B5CFF`, Energy `1.55`, Range `2.3m`.
  2. `Aeroponic_Foliage_Daylight_Ice`: Local Pos `(-0.32, 1.10, 0.15)`, Color `#E0F4FF`, Energy `1.45`, Range `2.2m` (brings out the lush emerald green of the 3D foliage inside the glass column).
  3. `Bioreactor_O2_Cyan_Glow`: Local Pos `(+0.58, 1.75, 0.10)`, Color `#00E5FF`, Energy `1.50`, Range `2.0m`.
