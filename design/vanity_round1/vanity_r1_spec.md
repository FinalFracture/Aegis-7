# Compact Hygiene & Sonic Wash Vanity — Round 1 Design, 3D Interior Layout, Translucent Glass & Lighting Specification
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Pipeline Stage:** Non-Bunk Sleeping Quarters Fixture #2 — 5-Choice Test (`vanity_r1_01` through `vanity_r1_05`)  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)  
**Target Teams:** Rook (3D Hard-Surface & Basin/Plumbing Modeling, Translucent UV-Cubby Assembly & UVs) & Gage (Godot 4 Scene Integration, Practical Lighting & 1080p Beauty Renders)

---

## 1. Shared Standards & Technical Rules ("Aegis-7 Standard")

### 1.1 Output Paths & Naming Convention
- **3D Models (`.glb`):** `/workspace/game-project/assets/glb/vanity_round1/vanity_r1_01.glb` through `/workspace/game-project/assets/glb/vanity_round1/vanity_r1_05.glb`
- **Winner Export Path (after 5-Bot Vote):** `/workspace/game-project/assets/glb/winners/vanity_winner_01_...glb`
- **Texture Suite (`.png`):** `/workspace/game-project/assets/textures/vanity_round1/` (and mirrored in `/workspace/game-project/assets/textures/`)
- **Individual 1080p Beauty Renders (`.png`):** `/workspace/game-project/assets/renders/vanity_round1/vanity_r1_01.png` through `vanity_r1_05.png` (and mirrored in `/workspace/game-project/godot/renders/vanity_round1/`)
- **5-Panel Voting Comparison Sheet:** `/workspace/game-project/assets/renders/vanity_round1/vanity_round1_voting_sheet.png`

### 1.2 Coordinate System, Footprint & Pivot Convention
- **Metric Scale:** `1.0 unit = 1.0 meter`.
- **Target Compact Crew Cabin Footprint:** `0.88m – 1.08m Wide (X) × 0.50m – 0.65m Deep (Z) × 1.98m – 2.10m Tall (Y)`.
- **World Origin & Pivot Point:** Bottom-center `(0.0, 0.0, 0.0)` resting flush on the `Y = 0.0` floor plane (`min_y == 0.0000`, centered in `X` and `Z`).
- **Front Orientation (`+Z` Forward):** Washbasin, smart mirror, and translucent sterilizer doors face **`+Z`**, rear bulkhead mounting frame rests at **`-Z`**.
- **Polygon Budget:** **`2,500 – 5,500 triangles`** per candidate.

### 1.3 Mandatory 4-Part 3D Hygiene & Reclamation Kit (Visible in Every Candidate!)
Every candidate (`vanity_r1_01` through `vanity_r1_05`) must include these four signature 3D architectural and functional details so it pairs seamlessly with Jared's locked EVA Locker Winner (`#02 — Dual-Bay Recessed Bulkhead Suit & Kit Locker`):
1. **Contoured 3D Zero-Splash Washbasin & Sonic-Mist Emitter Faucet (`Y ~ 0.80m – 0.96m`):**
   - Lathed/sculpted concave elliptical, hemispherical, or chamfered-trapezoidal basin in matte aerospace white (`composite_aerospace_white.png`) or brushed steel (`steel_machined_gantry.png`) with a recessed stainless drain ring and glowing cyan (`#00E5FF`) ultrasonic atomizer rim.
   - Curved/lathed **42 kHz Sonic-Mist Faucet Arch** (`steel_machined_gantry.png`) arching over the basin bowl.
2. **Backlit Smart-Mirror HUD (`Y ~ 1.12m – 1.78m`):**
   - Octagonal, stadium-rounded, or trapezoidal dark-silvered mirror surface (`mirror_smart_hud_cyan.png`, `metallic: 0.92`, `roughness: 0.06`) with crisp top/bottom cyan & amber biometric/H2O readouts and an unoccluded reflective center, framed by glare-free surgical ice-white (`#E0F4FF`) and cyan (`#00E5FF`) vanity light bars.
3. **UV-C Towel & Personal Grooming Sterilizer Cubby (Behind Translucent `alphaMode: "BLEND"` Glass):**
   - Recessed storage compartment enclosed by a **true alpha-translucent door** (`glass_uv_cubby_violet.png` or `glass_sonic_shield_translucent.png`, `alpha ~ 0.18`), showcasing **3D rolled/folded orbital-navy microfiber towels** (`fabric_orbital_navy_towel.png`), **3D cylindrical sonic dental/grooming wands**, and **pressurized dermal/soap dispensers** illuminated by an interior UV-violet (`#7B5CFF`) emitter tube.
4. **Lower Greywater Filtration & H2O Reclamation Manifold (`Y ~ 0.12m – 0.65m`):**
   - Visible through a lower recessed service bay or translucent inspection window: **twin cylindrical greywater filter canisters** (`composite_aerospace_white.png` / `steel_machined_gantry.png`), bent metallic syphon/manifold pipes, and a **signal-orange (`accent_signal_orange.png`, `#D95B26`) emergency shutoff/purge valve**.

---

## 2. Texture & Material Library Manifest (`/workspace/game-project/assets/textures/vanity_round1/`)

All 10 textures are `1024×1024` ultra-clean, low-noise (`<1.2%` micro-variation) PNGs stored in `/workspace/game-project/assets/textures/vanity_round1/` and mirrored in `/workspace/game-project/assets/textures/`.

| # | Filename | Format | Base Hex / Tone | Roughness | Metallic | Alpha / Emissive & Material Usage |
|---|----------|--------|-----------------|-----------|----------|-----------------------------------|
| 1 | `titanium_gunmetal_hull.png` | RGB | `#1A1E24` | `0.34` | `0.78` | Primary 45° chamfered gunmetal titanium outer bulkhead housing |
| 2 | `composite_aerospace_white.png` | RGB | `#D8DEE6` | `0.26` | `0.08` | Smooth molded aerospace white washbasins, countertops & inner sterilizer bays |
| 3 | `carbon_slate_frame.png` | RGB | `#282E38` | `0.40` | `0.58` | Dark carbon-slate structural framing, shelf dividers & lower service bays |
| 4 | `steel_machined_gantry.png` | RGB | `#88929E` | `0.20` | `0.90` | Brushed machined steel for sonic-mist faucet arches, towel rails, drain rings & plumbing pipes |
| 5 | `fabric_orbital_navy_towel.png` | RGB | `#1D2C3C` | `0.78` | `0.00` | Deep orbital navy microfiber weave for 3D folded/rolled hand towels & hygiene pouches |
| 6 | `accent_signal_orange.png` | RGB | `#D95B26` | `0.48` | `0.06` | Matte signal-orange for greywater reclamation valves, filter collars & eye-wash latches |
| 7 | `mirror_smart_hud_cyan.png` | RGB | `#141C26` + `#00E5FF` | `0.06` | `0.92` | High-reflectivity dark-silvered smart mirror with top/bottom cyan & amber telemetry bezels |
| 8 | `glass_sonic_shield_translucent.png` | **RGBA** | `#0E2230` | `0.08` | `0.10` | **`alphaMode: "BLEND"` (`alpha ~ 0.18`)**, cyan-tinted translucent splash shields & cabinet doors |
| 9 | `glass_uv_cubby_violet.png` | **RGBA** | `#1A1433` | `0.08` | `0.10` | **`alphaMode: "BLEND"` (`alpha ~ 0.19`)**, violet-tinted quartz UV-sterilizer compartment door |
| 10 | `oled_hygiene_panel.png` | RGB | `#0A0E14` + `#00E5FF` | `0.15` | `0.10` | **`emission_enabled: true` (`energy = 2.0`)**, 42 kHz sonic-pulse & 98.4% H2O recovery OLED display |

---

## 3. Detailed Per-Candidate Specifications (`vanity_r1_01` through `vanity_r1_05`)

---

### Candidate 01: `vanity_r1_01` — `#01 — Recessed Octagonal Bulkhead Sonic Vanity`
*Dimensions: `0.95m W × 0.55m D × 2.05m H` — Direct architectural companion to `locker_winner_01_dual_bay_bulkhead.glb`.*

- **Color Palette (Hex Codes):**
  - Outer 45° Chamfered Bulkhead Frame: Gunmetal Titanium `#1A1E24` & Carbon Slate `#282E38`
  - Sculpted Basin & Countertop Deck: Matte Aerospace White `#D8DEE6`
  - Sonic-Mist Faucet Arch, Towel Bar & Plumbing: Machined Steel `#88929E`
  - Folded Towels & Grooming Kit: Orbital Navy `#1D2C3C` & Signal Orange `#D95B26`
  - Practical Lighting: Surgical Ice-White Mirror Strips `#E0F4FF`, Cyan Basin Ring `#00E5FF`, UV-Violet Cubby `#7B5CFF`, Amber Toe-Kick `#FF9500`
- **3D Geometry & Layout Brief for Rook:**
  - Frame the unit in a **45° chamfered octagonal dark gunmetal titanium housing (`0.95m W × 0.55m D × 2.05m H`)** with a sculpted aerospace-white countertop deck at `Y = 0.85m`.
  - Recess an **elliptical zero-splash aerospace-white basin (`0.46m W × 0.34m D × 0.14m deep`)** on the left/center with a curved brushed-steel sonic-mist emitter arch and glowing cyan atomizer ring.
  - Mount a **beveled octagonal smart mirror (`mirror_smart_hud_cyan.png`, `0.54m W × 0.68m H`)** on the upper backwall flanked by vertical surgical ice-white (`#E0F4FF`) light bars.
  - Along the right side (`X = +0.20m` to `+0.44m, Y = 0.90m–1.85m`), carve a **2-tier UV-C sterilizer column** behind a translucent violet quartz door (`glass_uv_cubby_violet.png`, `alphaMode: "BLEND"`), housing **3D rolled navy microfiber towels** and **3 cylindrical sonic grooming wands**.
  - Below the basin (`Y = 0.12m–0.72m`), recess the **H2O greywater reclamation bay** behind a translucent cyan inspection shield (`glass_sonic_shield_translucent.png`), revealing **two vertical white/steel filter cylinders, bent manifold pipes, and a signal-orange shutoff valve**.

---

### Candidate 02: `vanity_r1_02` — `#02 — Cantilevered Aerospace Pod Basin & Floating Halo Mirror`
*Dimensions: `0.90m W × 0.55m D × 2.00m H`*

- **Color Palette (Hex Codes):**
  - Rear Structural Spine: Carbon Slate `#282E38` & Gunmetal Titanium `#1A1E24`
  - Cantilevered Floating Basin Pod: Matte Aerospace White `#D8DEE6`
  - Halo Mirror Frame & Exposed Syphon Tubes: Brushed Steel `#88929E`
  - Practical Lighting: Dual Halo Ring (`#E0F4FF` + `#00E5FF`) & Overhead Cabinet Glow
- **3D Geometry & Layout Brief for Rook:**
  - Build a sleek **wall-mounted carbon-slate vertical spine (`0.90m W × 2.00m H`)** supporting a **cantilevered, stadium-curved aerospace-white floating washbasin pod (`Y = 0.78m–0.92m`)** with open leg clearance underneath, exposing twin machined-steel water-reclamation syphon U-tubes and a signal-orange purge valve.
  - Above the basin (`Y = 1.08m–1.64m`), suspend a **circular/octagonal floating Halo Smart Mirror (`mirror_smart_hud_cyan.png`)** ringed by a continuous 360° glowing ice-white and cyan halo tube.
  - At the top crown (`Y = 1.68m–1.98m`), build a **horizontal overhead towel & med-kit locker** behind twin sliding translucent doors (`glass_sonic_shield_translucent.png`) with 3D folded navy towels and hygiene canisters inside.

---

### Candidate 03: `vanity_r1_03` — `#03 — Dual-Zone Split Grooming & UV Decon Station`
*Dimensions: `1.05m W × 0.58m D × 2.08m H` — Asymmetric split-bay companion mirroring `locker_winner_01_dual_bay_bulkhead.glb`.*

- **Color Palette (Hex Codes):**
  - Split-Bay Bulkhead Housing: Gunmetal Titanium `#1A1E24` & Carbon Slate Partition `#282E38`
  - Left Sonic Wash Alcove & Basin: Aerospace White `#D8DEE6` & Brushed Steel `#88929E`
  - Right Full-Height UV Sterilizer & Towel Tower: Violet Quartz Glass `#1A1433` (`alpha ~ 0.19`), Orbital Navy Towels `#1D2C3C` & Signal Orange `#D95B26`
  - Practical Lighting: Left Alcove Cyan/Ice-White (`#00E5FF` / `#E0F4FF`) + Right Tower UV-Violet (`#7B5CFF`) + Lower Amber (`#FF9500`)
- **3D Geometry & Layout Brief for Rook:**
  - Design an **asymmetric 65% / 35% split-bay bulkhead cabinet (`1.05m W × 0.58m D × 2.08m H`)** that directly echoes the architectural rhythm of our winning `#02 — Dual-Bay Recessed Bulkhead Suit & Kit Locker`:
    - **Left Bay (65% width, `0.68m` wide):** Deep chamfered sonic wash alcove featuring a sculpted aerospace-white basin (`Y = 0.84m`), halo-ring sonic-mist emitter faucet, large beveled smart-mirror HUD (`mirror_smart_hud_cyan.png`), flush-mounted `oled_hygiene_panel.png` telemetry strip, and a lower translucent greywater reclamation bay with twin filter cylinders and signal-orange valve.
    - **Right Bay (35% width, `0.37m` wide):** Full-height 3-tier **UV-C Towel & Grooming Sterilizer Tower** enclosed by a full-height beveled **`alphaMode: "BLEND"` translucent violet quartz door (`glass_uv_cubby_violet.png`)**, displaying:
      * Top shelf: 3D sonic dental/dermal wand dock + medical dispenser canisters.
      * Middle shelf: 3D stack of folded & rolled orbital-navy microfiber towels (`fabric_orbital_navy_towel.png`).
      * Bottom shelf: Spare H2O filter cartridge with signal-orange collar + soiled-linen vacuum chute.

---

### Candidate 04: `vanity_r1_04` — `#04 — Cylindrical Sonic-Mist Alcove & Privacy Shield Vanity`
*Dimensions: `0.92m W × 0.62m D × 2.08m H`*

- **Color Palette (Hex Codes):**
  - Semi-Cylindrical Outer Column: Gunmetal Titanium `#1A1E24` & Aerospace White Inner Shell `#D8DEE6`
  - Hemispherical Basin & Overhead Sonic Ring: Brushed Machined Steel `#88929E`
  - Curved Splash Shield: Translucent Cyan Glass `#0E2230` (`alpha ~ 0.18`)
  - Practical Lighting: Overhead Cyan Sonic Ring `#00E5FF`, Mirror Ice-White `#E0F4FF`, Toe-Kick Amber `#FF9500`
- **3D Geometry & Layout Brief for Rook:**
  - Sculpt a **curved semi-cylindrical capsule vanity (`0.92m W × 0.62m D × 2.08m H`)** with a deep concave aerospace-white wash chamber, a **hemispherical brushed-steel basin bowl** at `Y = 0.85m`, and a curved panoramic smart mirror (`mirror_smart_hud_cyan.png`).
  - Wrap the left and right front curves with **parted curved `alphaMode: "BLEND"` translucent sonic-mist splash shields (`glass_sonic_shield_translucent.png`)** on machined-steel tracks, plus a lower translucent UV towel/filter compartment at `Y = 0.18m–0.74m`.

---

### Candidate 05: `vanity_r1_05` — `#05 — Corner-Chamfered Compact Crew Wash & Med-Dispenser`
*Dimensions: `0.98m W × 0.60m D × 2.05m H`*

- **Color Palette (Hex Codes):**
  - 45° Angled Corner Chassis: Gunmetal Titanium `#1A1E24` & Carbon Slate `#282E38`
  - Trapezoidal Basin & Med-Dispenser Niche: Aerospace White `#D8DEE6` & Signal Orange `#D95B26`
  - Twin Angled Translucent Wing Doors: `glass_uv_cubby_violet.png` & `glass_sonic_shield_translucent.png`
- **3D Geometry & Layout Brief for Rook:**
  - Build a **45°-angled wedge/corner-fit crew wash station (`0.98m W × 0.60m D × 2.05m H`)** with a central trapezoidal smart mirror (`mirror_smart_hud_cyan.png`) and deep trapezoidal aerospace-white basin (`Y = 0.85m`), flanked by **two 35°-canted side storage wings** behind translucent glass doors (left wing: UV-violet sterilizer rack with grooming wands; right wing: folded orbital-navy towels & signal-orange emergency eye-wash/med dispenser), and a lower exposed H2O reclamation manifold.

---

## 4. Standardized Camera Framing & Lighting Guide (`Gage` & `Rook`)

1. **1080p Hero Framing (`/workspace/game-project/assets/renders/vanity_round1/vanity_r1_01.png` .. `vanity_r1_05.png`):**
   - **Target Look-At Point:** `(0.0, 1.02, 0.0)`
   - **Camera Angles:** 3/4 front-isometric beauty angle (`yaw = ±18° to ±22°`, `pitch = -12°`, distance `~2.45m – 2.65m`, `FOV = 46°`) looking into the sculpted washbasin bowl, smart-mirror HUD, and translucent UV towel/filter compartments.
2. **5-Panel Voting Comparison Sheet (`/workspace/game-project/assets/renders/vanity_round1/vanity_round1_voting_sheet.png`):**
   - Composite all 5 candidates (`#01` through `#05`) with clear title badges, dimensions, and triangle counts.
