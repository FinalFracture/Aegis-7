# Room 08 Hero Asset: Ambient Zero-G Beverage Bar & Celestial Observatory Lounge Island — Round 1 Design Spec
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Pipeline Stage:** Room 08 Hero Asset — 5-Choice Test (`lounge_bar_r1_01` through `lounge_bar_r1_05`)  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)  
**Target Teams:** Rook (3D Hard-Surface & Bar/Decanter/Stool Modeling, Translucent Decanter Tower & UVs) & Gage (Godot 4 Scene Integration, Celestial Lounge Lighting & 1080p Beauty Renders)

---

## 1. Shared Standards & Technical Rules ("Aegis-7 Standard")

### 1.1 Output Paths & Naming Convention
- **3D Models (`.glb`):** `/workspace/game-project/assets/glb/lounge_round1/lounge_bar_r1_01.glb` through `/workspace/game-project/assets/glb/lounge_round1/lounge_bar_r1_05.glb`
- **Winner Export Path (after all 5 renders complete & 5-Bot Vote):** `/workspace/game-project/assets/glb/winners/lounge_bar_winner_01_...glb`
- **Texture Suite (`.png`):** `/workspace/game-project/assets/textures/lounge_round1/` (and mirrored in `/workspace/game-project/assets/textures/`)
- **Individual 1080p Beauty Renders (`.png`):** `/workspace/game-project/assets/renders/lounge_round1/lounge_bar_r1_01.png` through `lounge_bar_r1_05.png` (and mirrored in `/workspace/game-project/godot/renders/lounge_round1/`)
- **5-Panel Voting Comparison Sheet:** `/workspace/game-project/assets/renders/lounge_round1/lounge_bar_round1_voting_sheet.png` (and mirrored in `/workspace/game-project/godot/renders/lounge_round1/`)

### 1.2 Coordinate System, Lounge Bar Footprint & Pivot Convention
- **Metric Scale:** `1.0 unit = 1.0 meter`.
- **Target Lounge Bar Island Footprint:** `2.20m – 2.40m Wide (X) × 1.30m – 1.40m Deep (Z) × 2.00m – 2.10m Tall (Y)`.
- **World Origin & Pivot Point:** Bottom-center `(0.0, 0.0, 0.0)` resting flush on the `Y = 0.0` floor plane (`min_y == 0.0000`, centered in `X` and `Z`), front guest bar counter & pivoting lounge barstools facing **`+Z`**, rear decanter & botanical infusion tower at **`-Z`**.
- **Polygon Budget:** **`3,500 – 5,800 triangles`** per candidate.

### 1.3 Mandatory 4-Part 3D Celestial Lounge & Zero-G Beverage Kit (Required in Every Candidate!)
1. **45° Chamfered Bulkhead Spine & Cantilevered Illuminated Bar Counter (`Y = 0.0m – 0.96m`):**
   - Dark gunmetal titanium (`titanium_gunmetal_hull.png` / `metal_gunmetal_hull.png`, `#1A1E24`) and carbon-slate (`carbon_slate_frame.png` / `metal_carbon_slate.png`, `#282E38`) bar chassis with a sculpted matte aerospace-white (`composite_aerospace_white.png` / `panel_aerospace_white.png`, `#D8DEE6`) and brushed-steel (`steel_machined_gantry.png` / `metal_brushed_steel.png`, `#88929E`) bar top (`Y = 0.94m`), accented by recessed **Orbital Cyan (`#00E5FF`) & Circadian Amber (`#FF9500`) under-counter foot-rail glow**.
2. **Translucent Zero-G Botanical & Decanter Tower (`glass_lounge_bar_translucent.png`, `alphaMode: "BLEND"`, `alpha ~ 0.19`):**
   - Enclosed behind bevel-framed **`alphaMode: "BLEND"` sapphire/cyan-tinted translucent glass (`glass_lounge_bar_translucent.png`)**:
     * **3D Illuminated Botanical Infusion Carafes & Spherical Zero-G Drink Pods** (`led_cyan_strip.png`, `led_uv_violet.png`, `led_amber_strip.png` cores inside lathed glass/steel vessels).
     * **Integrated Living Aeroponic Botanical Garnish Trough (`foliage_aeroponic_herbs.png`)** under a soft `#7B5CFF` UV-violet accent bar.
3. **Zero-G Beverage Dispensing Arch, Magnetic Bulb-Glasses & Celestial OLED Console (`oled_lounge_celestial_bar.png`):**
   - Sculpted brushed-steel multi-nozzle zero-G siphon tap arch with **3D spherical/bulb zero-G sipper glasses** locked onto glowing cyan coaster rings on the counter, signal-orange (`accent_signal_orange.png` / `accent_safety_orange.png`, `#D95B26`) pressure-infusion valves, and a flush-mounted **`oled_lounge_celestial_bar.png` star-map & beverage synthesizer display (`emissive_energy = 2.0`)**.
4. **Two Pivoting Orbital-Navy & Charcoal Lounge Barstools (`Y ~ 0.62m`):**
   - Positioned along the front (`+Z`) of the bar counter: **two cantilevered/pedestal brushed-steel barstools** with sculpted ergonomic orbital-navy (`fabric_orbital_navy_pad.png`) and charcoal (`fabric_charcoal_flightpad.png`) bucket cushions and tubular chrome footrest rings!

---

## 2. Texture & Material Library Manifest (`/workspace/game-project/assets/textures/lounge_round1/`)

| # | Canonical Filename (Alias) | Format | Base Hex / Tone | Roughness | Metallic | Alpha / Emissive & Material Usage |
|---|----------------------------|--------|-----------------|-----------|----------|-----------------------------------|
| 1 | `titanium_gunmetal_hull.png` (`metal_gunmetal_hull.png`) | RGB | `#1A1E24` | `0.34` | `0.78` | Primary 45° chamfered gunmetal titanium bar chassis & rear tower housing |
| 2 | `composite_aerospace_white.png` (`panel_aerospace_white.png`) | RGB | `#D8DEE6` | `0.26` | `0.08` | Smooth matte aerospace white sculpted bar counter top & inner decanter niches |
| 3 | `carbon_slate_frame.png` (`metal_carbon_slate.png`) | RGB | `#282E38` | `0.40` | `0.58` | Dark carbon-slate bar front knee-wall, coaster inlay & stool base plinths |
| 4 | `steel_machined_gantry.png` (`metal_brushed_steel.png`) | RGB | `#88929E` | `0.18` | `0.92` | Brushed machined steel for siphon tap arch, barstool pedestals, footrests & flask caps |
| 5 | `fabric_charcoal_flightpad.png` (`fabric_charcoal_cushion.png`) | RGB | `#242932` | `0.78` | `0.00` | Padded bar edge armrest bolster & stool outer shell |
| 6 | `fabric_orbital_navy_pad.png` (`fabric_navy_cushion.png`) | RGB | `#1D2C3C` | `0.76` | `0.00` | Deep orbital navy lounge barstool seat & backrest upholstery |
| 7 | `foliage_aeroponic_herbs.png` | RGB | `#2E5A36` | `0.52` | `0.00` | Living aeroponic botanical mint/herb garnish bed inside the bar tower |
| 8 | `accent_signal_orange.png` (`accent_safety_orange.png`) | RGB | `#D95B26` | `0.48` | `0.06` | Matte signal-orange for nitro/pressure-infusion valves & barstool swivel locks |
| 9 | `oled_lounge_celestial_bar.png` | RGB | `#0A0E14` + `#00E5FF` | `0.14` | `0.10` | **`emission_enabled: true` (`energy = 2.0`)**, 512×512 star-map & infusion bar OLED |
| 10 | `glass_lounge_bar_translucent.png` | **RGBA** | `#101E32` + `#00E5FF` | `0.06` | `0.12` | **`alphaMode: "BLEND"` (`alpha ~ 0.19`)**, 256×256 translucent decanter tower & privacy canopy glass |
| 11 | `led_cyan_strip.png` / `led_uv_violet.png` / `led_amber_strip.png` / `led_ice_white.png` | RGB | `#00E5FF` / `#7B5CFF` / `#FF9500` / `#E0F4FF` | `0.15` | `0.00` | Emissive glowing carafes, coaster rings & under-bar mood lighting |

---

## 3. Detailed Per-Candidate Specifications (`lounge_bar_r1_01` through `lounge_bar_r1_05`)

1. **`lounge_bar_r1_01.glb` — `#01 — Aegis-7 Octagonal Celestial Bar & Illuminated Carafe Arch` (`2.25m W × 1.35m D × 2.05m H`):**
   - Symmetrical octagonal-beveled bar counter with a rear arched `glass_lounge_bar_translucent.png` display vault holding 6 glowing cyan/violet/amber infusion carafes, central `oled_lounge_celestial_bar.png` star-map screen, siphon tap arch, and two front orbital-navy barstools.
2. **`lounge_bar_r1_02.glb` — `#02 — Dual-Zone Split Celestial Beverage Bar & Illuminated Zero-G Decanter Tower` (`2.35m W × 1.35m D × 2.05m H`):**
   - **Signature 65% / 35% asymmetric split-bay Aegis-7 sibling to all locked winners!**
   - **Left Bay (65% width, `1.53m` wide):** Cantilevered aerospace-white & brushed-steel **Celestial Beverage Bar Counter (`Y = 0.94m`)** with a padded charcoal front armrest bolster, recessed cyan/amber star-chart counter inlay, flush **`oled_lounge_celestial_bar.png` telemetry console**, sculpted brushed-steel **triple-nozzle zero-G siphon tap arch**, **3 spherical zero-G bulb-glasses** locked onto glowing cyan coaster rings, a lower recessed chiller bay, and **two pivoting orbital-navy & charcoal lounge barstools (`Y = 0.62m`)** on brushed-steel pedestals with tubular footrests.
   - **Right Bay (35% width, `0.82m` wide):** Full-height 3-tier **Translucent Zero-G Botanical & Decanter Tower (`Y = 0.0m–2.05m`)** enclosed by bevel-framed **`alphaMode: "BLEND"` sapphire-tinted glass (`glass_lounge_bar_translucent.png`)**:
     * Top tier: **4 glowing cylindrical & spherical zero-G infusion decanters** (`#00E5FF` cyan, `#7B5CFF` violet, `#FF9500` amber liquid cores) with machined-steel dispensing manifolds and signal-orange pressure valves.
     * Middle tier: **Living Aeroponic Botanical Garnish Trough (`foliage_aeroponic_herbs.png`)** under a `#7B5CFF` UV-violet grow bar.
     * Bottom tier: Chilled reserve carafe rack & glassware sterilizer bay.
3. **`lounge_bar_r1_03.glb` — `#03 — Rotary Zero-G Sphere Dispenser & Curved Stargazer Bar` (`2.28m W × 1.38m D × 2.05m H`):**
   - Sweeping stadium-curved bar counter with a central vertical cylindrical `glass_lounge_bar_translucent.png` magnetic levitation column suspending glowing zero-G beverage spheres, flanked by `oled_lounge_celestial_bar.png` and two cantilevered barstools.
4. **`lounge_bar_r1_04.glb` — `#04 — Cantilevered Canopy Lounge Island & Botanical Mixology Bay` (`2.32m W × 1.36m D × 2.08m H`):**
   - Features an overhead cantilevered `glass_lounge_bar_translucent.png` acoustic/light canopy projecting forward over the bar counter and barstools, with suspended glass racks and a rear botanical infusion wall.
5. **`lounge_bar_r1_05.glb` — `#05 — Sunken Pit Perimeter Bar & Dual-Tap Cryo-Chiller Station` (`2.38m W × 1.35m D × 2.02m H`):**
   - Low-slung architectural lounge bar designed to border a sunken viewing pit, featuring twin translucent cryo-chiller drums, central `oled_lounge_celestial_bar.png` celestial console, and two low-G perch stools.

---

## 4. Standardized Camera Framing & Lighting Guide (`Gage` & `Rook`)

- **Target Look-At Point:** `(0.0, 1.02, 0.0)`
- **Camera Angles:** 3/4 front-isometric beauty angle (`yaw = ±20° to ±24°`, `pitch = -13°`, distance `~2.85m – 3.10m`, `FOV = 46°`).
- **Practical Lights:**
  1. `Bar_Counter_Cyan_Coasters`: Local Pos `(-0.35, 1.15, 0.25)`, Color `#00E5FF`, Energy `1.50`, Range `2.2m`.
  2. `Decanter_Tower_UV_Violet`: Local Pos `(+0.65, 1.45, -0.05)`, Color `#7B5CFF`, Energy `1.45`, Range `2.0m`.
  3. `Under_Bar_Footrail_Amber`: Local Pos `(-0.30, 0.24, 0.45)`, Color `#FF9500`, Energy `1.30`, Range `1.9m`.
