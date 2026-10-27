# Personal Climate & Life-Support Wall Panel — Round 1 Design, 3D Emergency O2 Kit, Translucent Bay Glass & Lighting Specification
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Pipeline Stage:** Non-Bunk Sleeping Quarters Fixture #9 — 5-Choice Test (`climate_r1_01` through `climate_r1_05`)  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)  
**Target Teams:** Rook (3D Hard-Surface & Louver/Valve/Mask Modeling, Translucent O2 Bay Door & UVs) & Gage (Godot 4 Scene Integration, Practical Lighting & 1080p Beauty Renders)

---

## 1. Shared Standards & Technical Rules ("Aegis-7 Standard")

### 1.1 Output Paths & Naming Convention
- **3D Models (`.glb`):** `/workspace/game-project/assets/glb/climate_round1/climate_r1_01.glb` through `/workspace/game-project/assets/glb/climate_round1/climate_r1_05.glb`
- **Winner Export Path (after all 5 renders complete & 5-Bot Vote):** `/workspace/game-project/assets/glb/winners/climate_winner_01_...glb`
- **Texture Suite (`.png`):** `/workspace/game-project/assets/textures/climate_round1/` (and mirrored in `/workspace/game-project/assets/textures/`)
- **Individual 1080p Beauty Renders (`.png`):** `/workspace/game-project/assets/renders/climate_round1/climate_r1_01.png` through `climate_r1_05.png` (and mirrored in `/workspace/game-project/godot/renders/climate_round1/`)
- **5-Panel Voting Comparison Sheet:** `/workspace/game-project/assets/renders/climate_round1/climate_round1_voting_sheet.png` (and mirrored in `/workspace/game-project/godot/renders/climate_round1/`)

### 1.2 Coordinate System, Bulkhead Mounting Plinth & Footprint
- **Metric Scale:** `1.0 unit = 1.0 meter`.
- **Bulkhead Wall-Panel Footprint & Plinth Convention:**
  - Each `.glb` model represents a complete **recessed bulkhead wall-panel module** standing at eye-level crew height on a clean dark-titanium lower bulkhead wainscot plinth (`Y = 0.00m` to `Y = 0.52m`) with the active recessed environmental & emergency O2 control station spanning `Y = 0.52m` to `Y = 1.90m`.
  - **Total Envelope:** `0.86m – 0.98m Wide (X) × 0.28m – 0.35m Deep (Z) × 1.88m – 1.94m Tall (Y)`.
  - **World Origin & Pivot Point:** Bottom-center `(0.0, 0.0, 0.0)` resting flush on `Y = 0.0` (`min_y == 0.0000`, centered in `X` and `Z`) so it aligns seamlessly alongside `locker_winner_01`, `vanity_winner_01`, and `walldesk_winner_01` in `Room 01 — Crew Sleeping Quarters` and across the other 9 rooms!
  - **Front Orientation (`+Z` Forward):** Louvers, OLED displays, tactile dials, and translucent emergency O2 doors face **`+Z`**, rear bulkhead spine sits at **`-Z`**.
- **Polygon Budget:** **`2,500 – 5,000 triangles`** per candidate.

### 1.3 Mandatory 4-Part 3D Life-Support & Emergency O2 Kit (Required in Every Candidate!)
Every candidate (`climate_r1_01` through `climate_r1_05`) must include these four signature 3D sub-assemblies:
1. **45° Chamfered Bulkhead Housing & 3D Laminar Air-Diffuser Louvers (`Y ~ 1.48m – 1.85m`):**
   - Recessed dark gunmetal titanium (`titanium_gunmetal_hull.png`, `#1A1E24`) and carbon-slate (`carbon_slate_frame.png`, `#282E38`) bulkhead module housing **sculpted 3D angled laminar-flow air-diffuser vanes/louvers** backed by a glowing UV-violet (`#7B5CFF`) or cyan (`#00E5FF`) HEPA/ionizer light strip.
2. **Spin-Gravity / Coriolis & Atmospheric OLED Telemetry (`oled_climate_telemetry.png`) + Tactile Capacitive/Hardware Controls (`oled_circadian_sliders.png`):**
   - Primary high-contrast OLED screen (`oled_climate_telemetry.png`, `emissive_energy = 2.0`) displaying O'Neill Cylinder spin-gravity (`0.98 G`), cabin pressure (`101.3 kPa`), and `O2 / N2 / CO2` partial pressures.
   - Paired with the vertical capacitive fader panel (`oled_circadian_sliders.png`, `emissive_energy = 1.8`) AND **3D sculpted machined-steel rotary vernier dials, fader caps, and guarded toggle switches** (`steel_machined_gantry.png`).
3. **Translucent Emergency O2 Breather-Mask Bay (`glass_o2_bay_translucent.png`, `alphaMode: "BLEND"`, `alpha ~ 0.18`):**
   - Recessed emergency life-support compartment enclosed by a bevel-framed **`alphaMode: "BLEND"` translucent armored polycarbonate door (`glass_o2_bay_translucent.png`)**, clearly showcasing **3D stowed emergency gear inside**:
     * **Two 3D Molded Orbital Emergency Breather Masks:** Sculpted aerospace-white (`composite_aerospace_white.png`) nose/mouth oro-nasal cones with charcoal head-straps (`fabric_charcoal_flightpad.png`), signal-orange demand valves (`accent_signal_orange.png`), and **coiled/looped 3D oxygen feed tubes** hanging on machined-steel hooks.
     * **Twin High-Pressure Emergency O2 Cylinders:** Vertical or horizontal lathed cylinders (`composite_aerospace_white.png` / `steel_machined_gantry.png`) with signal-orange regulator collars and pressure gauges.
     * **Manual Hull-Breach / Depressurization Pull Lever:** Signal-orange (`accent_signal_orange.png`) T-handle or rotary isolation valve.
4. **Replaceable Zeolite CO2 Scrubber Cartridges & Pressure Manifold (`Y ~ 0.55m – 0.90m`):**
   - Exposed or semi-recessed **machined-steel (`steel_machined_gantry.png`) O2/N2 cross-feed pipes**, differential barometer dial, and **two cylindrical lithium-hydroxide / zeolite CO2 scrubber canisters** with glowing cyan/amber status rings.

---

## 2. Texture & Material Library Manifest (`/workspace/game-project/assets/textures/climate_round1/`)

All 10 textures are `1024×1024` ultra-clean, low-noise (`<1.0%–1.2%` micro-variation) PNGs stored in `/workspace/game-project/assets/textures/climate_round1/` and mirrored in `/workspace/game-project/assets/textures/`.

| # | Filename | Format | Base Hex / Tone | Roughness | Metallic | Alpha / Emissive & Material Usage |
|---|----------|--------|-----------------|-----------|----------|-----------------------------------|
| 1 | `titanium_gunmetal_hull.png` | RGB | `#1A1E24` | `0.34` | `0.78` | Primary 45° chamfered gunmetal titanium bulkhead housing & lower plinth |
| 2 | `composite_aerospace_white.png` | RGB | `#D8DEE6` | `0.28` | `0.08` | Smooth matte aerospace white emergency O2 bay liner, breather masks & CO2 scrubber cylinders |
| 3 | `carbon_slate_frame.png` | RGB | `#282E38` | `0.40` | `0.58` | Dark carbon-slate directional air-diffuser louver vanes, sub-bezels & mounting tracks |
| 4 | `steel_machined_gantry.png` | RGB | `#88929E` | `0.22` | `0.90` | Brushed machined steel for rotary vernier dials, O2 manifold pipes, mask hooks & latches |
| 5 | `fabric_charcoal_flightpad.png` | RGB | `#242932` | `0.78` | `0.00` | Charcoal ballistic weave for breather-mask harnesses, coiled hose sleeves & acoustic backing |
| 6 | `fabric_orbital_navy_pad.png` | RGB | `#1D2C3C` | `0.76` | `0.00` | Deep orbital navy fabric for stowed emergency smoke/thermal hood pouches |
| 7 | `accent_signal_orange.png` | RGB | `#D95B26` | `0.48` | `0.06` | Matte signal-orange for emergency O2 purge levers, regulator valves & hull-breach handles |
| 8 | `oled_climate_telemetry.png` | RGB | `#0A0E14` + `#00E5FF` | `0.14` | `0.10` | **`emission_enabled: true` (`energy = 2.0`)**, Coriolis spin-G, O2/N2/CO2 & solar-cycle OLED screen |
| 9 | `oled_circadian_sliders.png` | RGB | `#0A0E14` + `#00E5FF` | `0.14` | `0.10` | **`emission_enabled: true` (`energy = 1.8`)**, 4-channel capacitive airflow/temp/UV/circadian slider panel |
| 10 | `glass_o2_bay_translucent.png` | **RGBA** | `#0E2230` + `#00E5FF` | `0.08` | `0.10` | **`alphaMode: "BLEND"` (`alpha ~ 0.18`)**, translucent armored polycarbonate emergency O2 bay door |

---

## 3. Detailed Per-Candidate Specifications (`climate_r1_01` through `climate_r1_05`)

---

### Candidate 01: `climate_r1_01` — `#01 — Recessed Octagonal Bulkhead Life-Support & O2 Station`
*Dimensions: `0.90m W × 0.30m D × 1.90m H`*

- **Color Palette (Hex Codes):**
  - 45° Chamfered Bulkhead Frame & Plinth: Gunmetal Titanium `#1A1E24` & Carbon Slate `#282E38`
  - Emergency O2 Alcove Liner, Masks & Canisters: Matte Aerospace White `#D8DEE6`
  - Rotary Vernier Dials & Manifold Pipes: Machined Steel `#88929E`
  - Emergency Valves & Pull Handle: Signal Orange `#D95B26`
  - Practical Lighting: Louver UV-Violet `#7B5CFF`, O2 Bay & Telemetry Cyan `#00E5FF`, Valve Amber `#FF9500`
- **3D Geometry & Layout Brief for Rook:**
  - Build a classic vertically stacked **45° chamfered octagonal bulkhead life-support station (`0.90m W × 0.30m D × 1.90m H`)** above a `0.52m` dark-titanium wainscot plinth:
    - **Upper Tier (`Y = 1.50m–1.84m`):** Recessed bank of 6 angled carbon-slate laminar air-diffuser blades with an internal UV-violet (`#7B5CFF`) ionizer light bar.
    - **Middle Tier (`Y = 1.04m–1.48m`):** Widescreen `oled_climate_telemetry.png` display on the left + `oled_circadian_sliders.png` capacitive fader bank and 3 sculpted machined-steel rotary vernier knobs on the right.
    - **Lower Tier (`Y = 0.54m–1.02m`):** Bevel-framed **`alphaMode: "BLEND"` translucent emergency O2 bay (`glass_o2_bay_translucent.png`)** housing **two 3D white/charcoal breather masks on hooks, coiled hoses, two vertical O2 cylinders with signal-orange valves, and a signal-orange manual pull T-handle**.

---

### Candidate 02: `climate_r1_02` — `#02 — Dual-Zone Split Atmospheric Telemetry & Emergency Breather Bay`
*Dimensions: `0.96m W × 0.32m D × 1.92m H` — Direct asymmetric split-bay sibling to Locked Locker `#02`, Vanity `#03`, Desk `#02`, and Footlocker `#02`!*

- **Color Palette (Hex Codes):**
  - Asymmetric 62% / 38% Split Bulkhead Frame: Gunmetal Titanium `#1A1E24` & Carbon Slate Divider `#282E38`
  - Left Environmental Control Bay: `oled_climate_telemetry.png`, `oled_circadian_sliders.png` & Machined Steel `#88929E`
  - Right Full-Height Translucent Emergency O2 Tower: `glass_o2_bay_translucent.png` (`alpha ~ 0.18`), Aerospace White `#D8DEE6`, Orbital Navy `#1D2C3C` & Signal Orange `#D95B26`
  - Practical Lighting: Left Louver UV-Violet `#7B5CFF` & Telemetry Cyan `#00E5FF` + Right O2 Tower Cyan/Amber (`#00E5FF` / `#FF9500`)
- **3D Geometry & Layout Brief for Rook:**
  - Design an **asymmetric 62% / 38% split-bay bulkhead life-support station (`0.96m W × 0.32m D × 1.92m H`)** that matches the exact Aegis-7 split-bay architectural language of all our locked Sleeping Quarters winners:
    - **Left Bay (62% width, `0.59m` wide):**
      * Top (`Y = 1.54m–1.84m`): Angled laminar HVAC air-diffuser louver bank with glowing UV-violet (`#7B5CFF`) sterilization strip.
      * Center (`Y = 0.96m–1.50m`): Recessed widescreen **`oled_climate_telemetry.png` Coriolis & gas-mix monitor** above the **`oled_circadian_sliders.png` 4-channel fader strip** with 3D physical machined-steel slider caps and rotary pressure verniers.
      * Bottom (`Y = 0.54m–0.92m`): Recessed service bay housing **two vertical cylindrical zeolite CO2 scrubber cartridges** (`composite_aerospace_white.png` / `steel_machined_gantry.png`) with glowing cyan status rings and a signal-orange purge valve.
    - **Right Bay (38% width, `0.37m` wide):** Full-height (`Y = 0.54m–1.84m`) **Emergency O2 & Breather-Mask Tower** enclosed by a full-height beveled **`alphaMode: "BLEND"` translucent polycarbonate door (`glass_o2_bay_translucent.png`)**, showcasing:
      * Upper & middle hooks: **Two 3D sculpted white/charcoal oro-nasal breather masks** with signal-orange demand regulators, coiled oxygen hoses, and a stowed orbital-navy thermal hood pouch.
      * Lower rack: **Twin high-pressure emergency O2 cylinders** connected by swept machined-steel manifold pipes to a guarded **signal-orange manual hull-breach override lever**.

---

### Candidate 03: `climate_r1_03` — `#03 — Cylindrical Vortex Scrubber & Holo-Barometer Column`
*Dimensions: `0.88m W × 0.34m D × 1.92m H`*

- **Color Palette (Hex Codes):**
  - Semi-Cylindrical Column Housing: Gunmetal Titanium `#1A1E24` & Aerospace White `#D8DEE6`
  - Top Vortex Diffuser Turbine & Lower Manifold: Machined Steel `#88929E` & Carbon Slate `#282E38`
  - Curved Translucent Mid-Chamber: `glass_o2_bay_translucent.png` (`alpha ~ 0.18`)
- **3D Geometry & Layout Brief for Rook:**
  - Sculpt a sleek **semi-cylindrical vertical life-support column (`0.88m W × 0.34m D × 1.92m H`)** featuring a circular radial-blade vortex air-scrubber diffuser at the top (`Y = 1.62m`) with UV-violet (`#7B5CFF`) core glow, a curved `oled_climate_telemetry.png` + `oled_circadian_sliders.png` collar at `Y = 1.22m`, and a curved **`alphaMode: "BLEND"` translucent glass cylinder bay (`Y = 0.56m–1.15m`)** displaying 3D twin breather masks, three vertical zeolite scrubber rods, and signal-orange O2 valves.

---

### Candidate 04: `climate_r1_04` — `#04 — Cantilevered Smart-Glass Vitals Console & Quick-Drop Mask Pod`
*Dimensions: `0.92m W × 0.30m D × 1.88m H`*

- **Color Palette (Hex Codes):**
  - Molded Capsule Bulkhead Panel: Matte Aerospace White `#D8DEE6` & Gunmetal Titanium `#1A1E24`
  - Floating Cantilevered Translucent HUD & Drop-Mask Door: `glass_o2_bay_translucent.png` (`alpha ~ 0.18`)
  - Quick-Release Lanyards & O2 Valves: Signal Orange `#D95B26` & Machined Steel `#88929E`
- **3D Geometry & Layout Brief for Rook:**
  - Build a clean aerospace-white & dark-titanium recessed module where the center `oled_climate_telemetry.png` and `oled_circadian_sliders.png` displays are fronted by a **cantilevered floating `alphaMode: "BLEND"` translucent glass HUD overlay pane**, while the lower bay (`Y = 0.56m–1.02m`) is a **quick-drop overhead/front translucent breather-mask dispenser (`glass_o2_bay_translucent.png`)** holding two 3D masks, coiled hoses, and twin horizontal O2 bottles.

---

### Candidate 05: `climate_r1_05` — `#05 — Heavy Pressure-Bulkhead Damper & Tactical O2 Manifold`
*Dimensions: `0.95m W × 0.32m D × 1.92m H`*

- **Color Palette (Hex Codes):**
  - Armored Pressure-Bulkhead Frame: Gunmetal Titanium `#1A1E24` & Carbon Slate `#282E38`
  - Exposed O2/N2 Cross-Feed Pipes & Damper Blades: Machined Steel `#88929E`
  - Rotary Isolation Handwheel & Breather Valves: Signal Orange `#D95B26`
  - Translucent Damper Window & O2 Locker: `glass_o2_bay_translucent.png` (`alpha ~ 0.18`)
- **3D Geometry & Layout Brief for Rook:**
  - Construct a heavy orbital pressure-sector control station featuring an upper **motorized butterfly air-damper chamber behind a translucent window**, dual side-by-side `oled_climate_telemetry.png` and `oled_circadian_sliders.png` screens, an exposed **sculpted signal-orange 4-spoke rotary O2 isolation handwheel** on machined-steel manifold pipes, and a lower translucent emergency breather-mask locker (`glass_o2_bay_translucent.png`).

---

## 4. Standardized Camera Framing & Lighting Guide (`Gage` & `Rook`)

1. **1080p Hero Framing (`/workspace/game-project/godot/renders/climate_round1/climate_r1_01.png` .. `climate_r1_05.png` & `/workspace/game-project/assets/renders/climate_round1/`):**
   - **Target Look-At Point:** `(0.0, 1.12, 0.0)` (centers on the active life-support console, laminar louvers, OLED telemetry displays, and translucent emergency O2 breather bay).
   - **Camera Angles:** Slight 3/4 front beauty angle (`yaw = ±16° to ±20°`, `pitch = -8° to -10°`, distance `~2.15m – 2.35m`, `FOV = 45°`) so the 3D recessed depth, rotary verniers, CO2 scrubber cylinders, and 3D breather masks behind the `alphaMode: "BLEND"` glass door read with razor-sharp clarity!
2. **3-Point + Practical Life-Support Lighting Rig:**
   - **Key Light:** Pos `(1.8, 2.2, 2.4)`, Color `#E8F2FF`, Energy `1.30`.
   - **Fill Light:** Pos `(-1.9, 1.4, 2.0)`, Color `#78A8D8`, Energy `0.48`.
   - **Rim Light:** Pos `(0.0, 2.4, -1.4)`, Color `#00E5FF`, Energy `0.90`.
   - **Life-Support Practicals:**
     1. `Louver_UV_Ionizer_Glow`: Local Pos `(0.0, 1.68, 0.08)`, Color `#7B5CFF`, Energy `1.45`, Range `1.6m`.
     2. `Emergency_O2_Bay_Cyan_Light`: Local Pos `(0.0, 0.85, 0.10)`, Color `#00E5FF` (illuminates the 3D breather masks and O2 cylinders behind the translucent door), Energy `1.60`, Range `1.8m`.
     3. `Manifold_Amber_Status`: Local Pos `(0.0, 0.58, 0.14)`, Color `#FF9500`, Energy `1.15`, Range `1.3m`.
3. **5-Panel Voting Comparison Sheet (`/workspace/game-project/assets/renders/climate_round1/climate_round1_voting_sheet.png`):**
   - Composite all 5 candidates (`#01` through `#05`) with clear title badges, dimensions, and triangle counts.
