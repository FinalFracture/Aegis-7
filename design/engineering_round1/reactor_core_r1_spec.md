# Room 09 Hero Asset: Fusion/Spin-Drive Plasma Relay & Cryo-Coolant Containment Manifold — Round 1 Design Spec
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Pipeline Stage:** Room 09 Hero Asset — 5-Choice Test (`reactor_core_r1_01` through `reactor_core_r1_05`)  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)  
**Target Teams:** Rook (3D Hard-Surface & Plasma Pinch Spindle/Toroidal Coils/Coolant Manifold Modeling, Translucent Radiation Shield & UVs) & Gage (Godot 4 Scene Integration, Plasma/Coolant Lighting & 1080p Beauty Renders)

---

## 1. Shared Standards & Technical Rules ("Aegis-7 Standard")

### 1.1 Output Paths & Naming Convention
- **3D Models (`.glb`):** `/workspace/game-project/assets/glb/engineering_round1/reactor_core_r1_01.glb` through `/workspace/game-project/assets/glb/engineering_round1/reactor_core_r1_05.glb`
- **Winner Export Path (after all 5 renders complete & 5-Bot Vote):** `/workspace/game-project/assets/glb/winners/reactor_core_winner_01_...glb`
- **Texture Suite (`.png`):** `/workspace/game-project/assets/textures/engineering_round1/` (and mirrored in `/workspace/game-project/assets/textures/`)
- **Individual 1080p Beauty Renders (`.png`):** `/workspace/game-project/assets/renders/engineering_round1/reactor_core_r1_01.png` through `reactor_core_r1_05.png` (and mirrored in `/workspace/game-project/godot/renders/engineering_round1/`)
- **5-Panel Voting Comparison Sheet:** `/workspace/game-project/assets/renders/engineering_round1/reactor_core_round1_voting_sheet.png` (and mirrored in `/workspace/game-project/godot/renders/engineering_round1/`)

### 1.2 Coordinate System, Reactor Footprint & Pivot Convention
- **Metric Scale:** `1.0 unit = 1.0 meter`.
- **Target Reactor Relay Footprint:** `2.45m – 2.65m Wide (X) × 1.45m – 1.55m Deep (Z) × 2.60m – 2.70m Tall (Y)`.
- **World Origin & Pivot Point:** Bottom-center `(0.0, 0.0, 0.0)` resting flush on the `Y = 0.0` floor plane (`min_y == 0.0000`, centered in `X` and `Z`), front radiation shield viewport & Chief Engineer telemetry bay facing **`+Z`**, rear cryo-coolant bus trunk at **`-Z`**.
- **Polygon Budget:** **`4,000 – 6,400 triangles`** per candidate.

### 1.3 Mandatory 4-Part 3D Plasma Containment & Cryo-Coolant Kit (Required in Every Candidate!)
1. **45° Chamfered Octagonal Containment Vessel & Heavy Cryo-Coolant Manifolds (`Y = 0.0m – 2.65m`):**
   - Massive dark gunmetal titanium (`titanium_gunmetal_hull.png` / `metal_gunmetal_hull.png`, `#1A1E24`) and carbon-slate (`carbon_slate_frame.png` / `metal_carbon_slate.png`, `#282E38`) containment column with upper and lower swept machined-steel (`steel_machined_gantry.png` / `metal_brushed_steel.png`, `#88929E`) liquid-helium (`18.2 K`) cryo-coolant bus pipes and aerospace-white (`composite_aerospace_white.png` / `panel_aerospace_white.png`, `#D8DEE6`) insulated jacket collars.
2. **Translucent Radiation-Shielded Containment Window (`glass_reactor_shield_translucent.png`, `alphaMode: "BLEND"`, `alpha ~ 0.20`) + 3D Magnetic-Pinch Plasma Core:**
   - Behind a bevel-framed **`alphaMode: "BLEND"` borosilicate radiation shield (`glass_reactor_shield_translucent.png`)**:
     * **3D Glowing Plasma Magnetic-Pinch Spindle (`led_cyan_strip.png` & `led_amber_strip.png`):** Central vertical plasma column with high-intensity `#00E5FF` cyan & `#FF9500` amber core rings.
     * **3D Superconducting Toroidal Pinch Coils (`steel_machined_gantry.png` & `led_uv_violet.png`):** 4 to 6 stacked lathed/chamfered magnetic confinement rings encircling the plasma column!
3. **Hot-Swappable D-He3 Moderator Rod Bay & Manual SCRAM Blowdown Lever:**
   - Recessed side chamber behind a translucent `glass_reactor_shield_translucent.png` hatch holding **3D cylindrical Deuterium / Helium-3 fuel moderator rods** (`composite_aerospace_white.png` with glowing `#7B5CFF` UV-violet & `#00E5FF` cyan tips), plus a heavy **signal-orange (`accent_signal_orange.png` / `accent_safety_orange.png`, `#D95B26`) manual SCRAM blowdown lever and rotary cryo-isolation handwheel**.
4. **Chief Engineer Plasma & Spin-Drive OLED Telemetry Console (`oled_reactor_plasma_telemetry.png`):**
   - Flush-mounted **`oled_reactor_plasma_telemetry.png` display (`emissive_energy = 2.0`)** showing `4.85 GW` spin-drive output, `18.2 K` cryo-loop status, and `99.94%` magnetic pinch stability, accompanied by 3D machined-steel rotary field-trim verniers.

---

## 2. Texture & Material Library Manifest (`/workspace/game-project/assets/textures/engineering_round1/`)

| # | Canonical Filename (Alias) | Format | Base Hex / Tone | Roughness | Metallic | Alpha / Emissive & Material Usage |
|---|----------------------------|--------|-----------------|-----------|----------|-----------------------------------|
| 1 | `titanium_gunmetal_hull.png` (`metal_gunmetal_hull.png`) | RGB | `#1A1E24` | `0.34` | `0.78` | Primary 45° chamfered gunmetal titanium reactor containment housing |
| 2 | `composite_aerospace_white.png` (`panel_aerospace_white.png`) | RGB | `#D8DEE6` | `0.28` | `0.08` | Smooth matte aerospace white cryo-insulation jackets & D-He3 fuel rod casings |
| 3 | `carbon_slate_frame.png` (`metal_carbon_slate.png`) | RGB | `#282E38` | `0.40` | `0.58` | Dark carbon-slate reactor pedestal, radiation baffles & shock mounts |
| 4 | `steel_machined_gantry.png` (`metal_brushed_steel.png`) | RGB | `#88929E` | `0.20` | `0.90` | Brushed machined steel for toroidal pinch coils, cryo-coolant pipes & verniers |
| 5 | `accent_signal_orange.png` (`accent_safety_orange.png`) | RGB | `#D95B26` | `0.48` | `0.06` | Matte signal-orange for manual SCRAM blowdown levers & cryo-isolation handwheels |
| 6 | `oled_reactor_plasma_telemetry.png` | RGB | `#0A0E14` + `#00E5FF` | `0.14` | `0.10` | **`emission_enabled: true` (`energy = 2.0`)**, 512×512 4.85 GW plasma & 18.2 K cryo OLED |
| 7 | `glass_reactor_shield_translucent.png` | **RGBA** | `#102230` + `#00E5FF` | `0.08` | `0.10` | **`alphaMode: "BLEND"` (`alpha ~ 0.20`)**, 256×256 translucent radiation-shielded containment glass |
| 8 | `led_cyan_strip.png` / `led_amber_strip.png` / `led_uv_violet.png` / `led_ice_white.png` | RGB | `#00E5FF` / `#FF9500` / `#7B5CFF` / `#E0F4FF` | `0.15` | `0.00` | Emissive 3D plasma spindle core, pinch coil rings & warning beacons |

---

## 3. Detailed Per-Candidate Specifications (`reactor_core_r1_01` through `reactor_core_r1_05`)

1. **`reactor_core_r1_01.glb` — `#01 — Aegis-7 Octagonal Plasma Pinch Column & Toroidal Coil Stack` (`2.50m W × 1.50m D × 2.65m H`):**
   - Symmetrical octagonal containment vessel with a wide central `glass_reactor_shield_translucent.png` radiation window showing the 3D glowing cyan/amber plasma spindle and 5 stacked superconducting toroidal coils, flanked by twin swept liquid-helium coolant pipes and a front-mounted `oled_reactor_plasma_telemetry.png` podium.
2. **`reactor_core_r1_02.glb` — `#02 — Dual-Zone Split Plasma Containment Column & Cryo-Coolant Control Bay` (`2.60m W × 1.50m D × 2.65m H`):**
   - **Signature 65% / 35% asymmetric split-bay Aegis-7 sibling to all locked winners!**
   - **Left Bay (65% width, `1.69m` wide):** Heavy 45° chamfered octagonal **Fusion/Spin-Drive Plasma Containment Column** enclosed across the front by a tall bevel-framed **`alphaMode: "BLEND"` borosilicate radiation shield (`glass_reactor_shield_translucent.png`)**. Inside the lit chamber: a **sculpted 3D vertical magnetic-pinch plasma core spindle (`led_cyan_strip.png` & `led_amber_strip.png`)** encircled by **5 precision-machined superconducting toroidal field coils (`steel_machined_gantry.png` with `#7B5CFF` UV-violet field injectors)**, fed at top and bottom by heavy swept cryo-coolant bus pipes.
   - **Right Bay (35% width, `0.91m` wide):** Integrated **Chief Engineer Cryo-Coolant & Moderator Rod Control Bay**:
     * Upper Tier (`Y = 1.50m–2.45m`): Bevel-framed **`alphaMode: "BLEND"` translucent fuel-moderator hatch (`glass_reactor_shield_translucent.png`)** displaying **4 vertical cylindrical Deuterium/Helium-3 moderator rods** (`composite_aerospace_white.png` with glowing cyan/violet status rings and signal-orange locking collars).
     * Center Tier (`Y = 0.90m–1.46m`): Flush-mounted **`oled_reactor_plasma_telemetry.png` 4.85 GW plasma & cryo telemetry console**, 3D machined-steel rotary magnetic-trim vernier dials, and a guarded **signal-orange manual SCRAM blowdown lever**.
     * Lower Tier (`Y = 0.15m–0.86m`): Twin insulated aerospace-white `18.2 K` liquid-helium Dewar flasks with a **sculpted signal-orange 4-spoke cryo-isolation handwheel**.
3. **`reactor_core_r1_03.glb` — `#03 — Spherical Tokamak Magnetic Cage & Twin Cryo-Dewar Gantry` (`2.55m W × 1.52m D × 2.65m H`):**
   - Features a central spherical/octagonal tokamak chamber behind curved `glass_reactor_shield_translucent.png` shields with intersecting meridian field ribs, flanked by two massive vertical white/steel liquid-helium Dewar cylinders and a side `oled_reactor_plasma_telemetry.png` terminal.
4. **`reactor_core_r1_04.glb` — `#04 — Twin-Core Spin-Drive Capacitor Bank & Plasma Conduit Arch` (`2.58m W × 1.48m D × 2.65m H`):**
   - Dual side-by-side vertical translucent plasma relay columns linked by an overhead heavy machined-steel plasma bus arch and a central `oled_reactor_plasma_telemetry.png` + SCRAM control pillar.
5. **`reactor_core_r1_05.glb` — `#05 — Heavy Axial Spin-Torque Generator & Sub-Cooler Manifold` (`2.62m W × 1.52m D × 2.68m H`):**
   - Industrial spin-gravity torque relay featuring a horizontal/angled translucent rotor drum (`glass_reactor_shield_translucent.png`) showing glowing cyan electromagnetic stator rings above a 4-cylinder cryo-cooler manifold and side `oled_reactor_plasma_telemetry.png` console.

---

## 4. Standardized Camera Framing & Lighting Guide (`Gage` & `Rook`)

- **Target Look-At Point:** `(0.0, 1.30, 0.0)`
- **Camera Angles:** Heroic 3/4 front-isometric beauty angle (`yaw = ±18° to ±22°`, `pitch = -11°`, distance `~3.15m – 3.40m`, `FOV = 46°`).
- **Practical Lights:**
  1. `Plasma_Spindle_Cyan_Core`: Local Pos `(-0.38, 1.35, 0.0)`, Color `#00E5FF`, Energy `1.75`, Range `2.6m` (illuminates the 3D toroidal coils inside the translucent radiation shield).
  2. `Plasma_Injector_Amber_Pulse`: Local Pos `(-0.38, 0.85, 0.10)`, Color `#FF9500`, Energy `1.40`, Range `2.0m`.
  3. `Moderator_Bay_UV_Violet`: Local Pos `(+0.72, 1.85, 0.12)`, Color `#7B5CFF`, Energy `1.40`, Range `1.9m`.
