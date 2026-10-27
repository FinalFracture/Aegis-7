# Room 07 Hero Asset: Central Holographic O'Neill Cylinder Wireframe Projection Table & Tiered Spin-Gravity Command Console — Round 1 Design Spec
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Pipeline Stage:** Room 07 Hero Asset — 5-Choice Test (`bridge_console_r1_01` through `bridge_console_r1_05`)  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)  
**Target Teams:** Rook (3D Hard-Surface & Holographic Cylinder Wireframe/Console Modeling, Translucent Holo-Glass & UVs) & Gage (Godot 4 Scene Integration, Holographic/Bridge Lighting & 1080p Beauty Renders)

---

## 1. Shared Standards & Technical Rules ("Aegis-7 Standard")

### 1.1 Output Paths & Naming Convention
- **3D Models (`.glb`):** `/workspace/game-project/assets/glb/bridge_round1/bridge_console_r1_01.glb` through `/workspace/game-project/assets/glb/bridge_round1/bridge_console_r1_05.glb`
- **Winner Export Path (after all 5 renders complete & 5-Bot Vote):** `/workspace/game-project/assets/glb/winners/bridge_console_winner_01_...glb`
- **Texture Suite (`.png`):** `/workspace/game-project/assets/textures/bridge_round1/` (and mirrored in `/workspace/game-project/assets/textures/`)
- **Individual 1080p Beauty Renders (`.png`):** `/workspace/game-project/assets/renders/bridge_round1/bridge_console_r1_01.png` through `bridge_console_r1_05.png` (and mirrored in `/workspace/game-project/godot/renders/bridge_round1/`)
- **5-Panel Voting Comparison Sheet:** `/workspace/game-project/assets/renders/bridge_round1/bridge_console_round1_voting_sheet.png` (and mirrored in `/workspace/game-project/godot/renders/bridge_round1/`)

### 1.2 Coordinate System, Command Table Footprint & Pivot Convention
- **Metric Scale:** `1.0 unit = 1.0 meter`.
- **Target Command Console Footprint:** `2.40m – 2.60m Wide (X) × 1.55m – 1.70m Deep (Z) × 1.85m – 2.00m Tall (Y)`.
- **World Origin & Pivot Point:** Bottom-center `(0.0, 0.0, 0.0)` resting flush on the `Y = 0.0` bridge deck (`min_y == 0.0000`, centered in `X` and `Z`), front commander stations facing **`+Z`**, elevated flight-director telemetry array at **`-Z` / `+X`**.
- **Polygon Budget:** **`3,800 – 6,200 triangles`** per candidate.

### 1.3 Mandatory 4-Part 3D Holographic Bridge & Telemetry Kit (Required in Every Candidate!)
1. **45° Chamfered Octagonal Projection Table & Recessed Emitter Well (`Y = 0.0m – 0.92m`):**
   - Heavy dark gunmetal titanium (`titanium_gunmetal_hull.png` / `metal_gunmetal_hull.png`, `#1A1E24`) and carbon-slate (`carbon_slate_frame.png` / `metal_carbon_slate.png`, `#282E38`) octagonal holotable base with matte aerospace-white (`composite_aerospace_white.png` / `panel_aerospace_white.png`, `#D8DEE6`) beveled knee bolsters, brushed-steel (`steel_machined_gantry.png` / `metal_brushed_steel.png`, `#88929E`) leaning rails, and a recessed optical projector lens well glowing with `#00E5FF` cyan & `#FF9500` amber emitter rings.
2. **Floating 3D Translucent O'Neill Cylinder Wireframe & Gimbal Rings (`glass_bridge_holo_translucent.png`, `alphaMode: "BLEND"`, `alpha ~ 0.20`):**
   - Suspended in mid-air above the projection well (`Y ~ 1.05m – 1.65m`): a **sculpted 3D miniature of the 800m × 400m O'Neill Cylinder habitat** consisting of a translucent cyan-tinted cylinder shell (`glass_bridge_holo_translucent.png`), 3D structural ring ribs, axial solar core rod (`led_cyan_strip.png`), and **two intersecting 3D orbital gimbal rings (`led_cyan_strip.png` & `led_amber_strip.png`)**!
3. **Tiered Flight-Director Spin-Gravity Telemetry Console (`oled_bridge_spin_telemetry.png`) + Tactile Vernier Controls:**
   - Widescreen curved/angled OLED telemetry array (`oled_bridge_spin_telemetry.png`, `emissive_energy = 2.0`) paired with an angled **`alphaMode: "BLEND"` translucent tactical HUD visor (`glass_bridge_holo_translucent.png`)**, 3D machined-steel dual-throttle spin-brake levers, rotary attitude verniers, and a guarded **signal-orange (`accent_signal_orange.png` / `accent_safety_orange.png`, `#D95B26`) emergency spin-lock master switch**.
4. **Contoured Commander Flight Chairs (`fabric_orbital_navy_pad.png` / `fabric_charcoal_flightpad.png`):**
   - One or two cantilevered/pedestal bridge officer chairs (`Y ~ 0.48m` seat height) with sculpted orbital-navy and charcoal cushions, armrests, and headrest bolsters positioned at the console stations.

---

## 2. Texture & Material Library Manifest (`/workspace/game-project/assets/textures/bridge_round1/`)

| # | Canonical Filename (Alias) | Format | Base Hex / Tone | Roughness | Metallic | Alpha / Emissive & Material Usage |
|---|----------------------------|--------|-----------------|-----------|----------|-----------------------------------|
| 1 | `titanium_gunmetal_hull.png` (`metal_gunmetal_hull.png`) | RGB | `#1A1E24` | `0.34` | `0.78` | Primary 45° chamfered gunmetal titanium holotable hull & command tower |
| 2 | `composite_aerospace_white.png` (`panel_aerospace_white.png`) | RGB | `#D8DEE6` | `0.28` | `0.08` | Smooth matte aerospace white console cowlings, chair shells & emitter bezels |
| 3 | `carbon_slate_frame.png` (`metal_carbon_slate.png`) | RGB | `#282E38` | `0.40` | `0.58` | Dark carbon-slate deck plinth, keyboard surfaces & projector well |
| 4 | `steel_machined_gantry.png` (`metal_brushed_steel.png`) | RGB | `#88929E` | `0.20` | `0.90` | Brushed machined steel for gimbal arches, throttle levers, chair pedestals & rails |
| 5 | `fabric_charcoal_flightpad.png` (`fabric_charcoal_cushion.png`) | RGB | `#242932` | `0.78` | `0.00` | Contoured charcoal wrist bolsters & chair side bolsters |
| 6 | `fabric_orbital_navy_pad.png` (`fabric_navy_cushion.png`) | RGB | `#1D2C3C` | `0.76` | `0.00` | Deep orbital navy commander flight-chair upholstery |
| 7 | `accent_signal_orange.png` (`accent_safety_orange.png`) | RGB | `#D95B26` | `0.48` | `0.06` | Matte signal-orange for emergency spin-lock master switch & thruster interlock handles |
| 8 | `oled_bridge_spin_telemetry.png` | RGB | `#0A0E14` + `#00E5FF` | `0.14` | `0.10` | **`emission_enabled: true` (`energy = 2.0`)**, 512×512 O'Neill Cylinder spin-G & attitude OLED |
| 9 | `glass_bridge_holo_translucent.png` | **RGBA** | `#0A2636` + `#00E5FF` | `0.08` | `0.10` | **`alphaMode: "BLEND"` (`alpha ~ 0.20`)**, 256×256 translucent 3D holo-cylinder & HUD visor glass |
| 10 | `led_cyan_strip.png` / `led_amber_strip.png` / `led_uv_violet.png` / `led_ice_white.png` | RGB | `#00E5FF` / `#FF9500` / `#7B5CFF` / `#E0F4FF` | `0.15` | `0.00` | Emissive holographic wireframe rings & console status strips |

---

## 3. Detailed Per-Candidate Specifications (`bridge_console_r1_01` through `bridge_console_r1_05`)

1. **`bridge_console_r1_01.glb` — `#01 — Aegis-7 Octagonal Holographic Cylinder Table & Twin Helm` (`2.45m W × 1.65m D × 1.90m H`):**
   - Symmetrical octagonal holotable with a large central floating 3D translucent O'Neill Cylinder hologram (`glass_bridge_holo_translucent.png`) ringed by 4倾斜 `oled_bridge_spin_telemetry.png` bevel screens and flanked by twin orbital-navy commander chairs.
2. **`bridge_console_r1_02.glb` — `#02 — Dual-Zone Split Holographic Cylinder Table & Tiered Flight-Director Console` (`2.55m W × 1.65m D × 1.95m H`):**
   - **Signature 65% / 35% asymmetric split-bay Aegis-7 sibling to all locked winners!**
   - **Left Bay (65% width, `1.66m` wide):** Octagonal 45° chamfered Holographic Projection Table (`Y = 0.88m`) with a stepped emitter lens well projecting a **floating 3D translucent O'Neill Cylinder wireframe & dual intersecting orbital gimbal rings (`glass_bridge_holo_translucent.png`, `led_cyan_strip.png`, `led_amber_strip.png` at `Y = 1.05m–1.68m`)**, accompanied by **two contoured orbital-navy & charcoal commander chairs** on cantilevered steel pedestals and flush tabletop `oled_bridge_spin_telemetry.png` touch panels.
   - **Right Bay (35% width, `0.89m` wide):** Elevated **Tiered Flight-Director Spin-Gravity & Attitude Control Tower (`Y = 0.0m–1.95m`)**:
     * Upper Tier (`Y = 1.25m–1.92m`): Curved 3-panel widescreen **`oled_bridge_spin_telemetry.png` command array** topped by an angled **`alphaMode: "BLEND"` translucent holographic HUD combiner visor (`glass_bridge_holo_translucent.png`)**.
     * Middle Tier (`Y = 0.85m–1.22m`): Tactile flight-director deck with **3D twin machined-steel spin-thruster throttle levers**, rotary Coriolis trim verniers, and a guarded **signal-orange emergency spin-lock master handle**.
     * Lower Tier (`Y = 0.15m–0.82m`): Bevel-framed **`alphaMode: "BLEND"` translucent optical core bay (`glass_bridge_holo_translucent.png`)** housing **6 vertical glowing cyan/violet navigation data-cartridges** and twin backup gyro-stabilizer cylinders!
3. **`bridge_console_r1_03.glb` — `#03 — Overhead Gantry Holo-Projector & Curved Bridge Pit Console` (`2.50m W × 1.68m D × 1.98m H`):**
   - Features an arched machined-steel overhead projector bridge spanning above the holotable, beaming down onto the 3D translucent O'Neill Cylinder model with a wrap-around U-shaped `oled_bridge_spin_telemetry.png` console and captain's chair.
4. **`bridge_console_r1_04.glb` — `#04 — Gimbaled Orrey Spin-Simulator & Tactical Command Desk` (`2.48m W × 1.62m D × 1.92m H`):**
   - Combines a physical machined-steel 3-axis motorized orrery ring cradle around the translucent holographic cylinder with dual winged `oled_bridge_spin_telemetry.png` stations and signal-orange thruster interlocks.
5. **`bridge_console_r1_05.glb` — `#05 — Elevated Captain's Command Podium & Dual-Wing Telemetry Array` (`2.55m W × 1.70m D × 1.96m H`):**
   - Raised two-step command podium with a central captain's throne overlooking a forward holographic cylinder projection well and twin angled `oled_bridge_spin_telemetry.png` + `glass_bridge_holo_translucent.png` wing consoles.

---

## 4. Standardized Camera Framing & Lighting Guide (`Gage` & `Rook`)

- **Target Look-At Point:** `(0.0, 1.05, 0.0)`
- **Camera Angles:** Elevated 3/4 front-isometric beauty angle (`yaw = ±20° to ±24°`, `pitch = -15°`, distance `~3.05m – 3.30m`, `FOV = 46°`).
- **Practical Lights:**
  1. `Holo_Cylinder_Core_Cyan`: Local Pos `(-0.35, 1.32, 0.0)`, Color `#00E5FF`, Energy `1.70`, Range `2.5m` (illuminates the floating 3D O'Neill Cylinder hologram and commander chairs).
  2. `Flight_Director_Tower_Violet`: Local Pos `(+0.68, 1.45, -0.10)`, Color `#7B5CFF`, Energy `1.35`, Range `2.0m`.
  3. `Table_Base_Amber_Safety`: Local Pos `(0.0, 0.22, 0.45)`, Color `#FF9500`, Energy `1.20`, Range `1.8m`.
