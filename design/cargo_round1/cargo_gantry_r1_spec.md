# Room 10 Hero Asset: Modular Hex/Chamfered Cargo Container Rack & Autonomous Logistics Drone Docking Gantry — Round 1 Design Spec
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Pipeline Stage:** Room 10 Hero Asset — 5-Choice Test (`cargo_gantry_r1_01` through `cargo_gantry_r1_05`)  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)  
**Target Teams:** Rook (3D Hard-Surface & Modular ISO Rack/Logistics Drone Modeling, Translucent Bay Glass & UVs) & Gage (Godot 4 Scene Integration, Logistics Lighting & 1080p Beauty Renders)

---

## 1. Shared Standards & Technical Rules ("Aegis-7 Standard")

### 1.1 Output Paths & Naming Convention
- **3D Models (`.glb`):** `/workspace/game-project/assets/glb/cargo_round1/cargo_gantry_r1_01.glb` through `/workspace/game-project/assets/glb/cargo_round1/cargo_gantry_r1_05.glb`
- **Winner Export Path (after all 5 renders complete & 5-Bot Vote):** `/workspace/game-project/assets/glb/winners/cargo_gantry_winner_01_...glb`
- **Texture Suite (`.png`):** `/workspace/game-project/assets/textures/cargo_round1/` (and mirrored in `/workspace/game-project/assets/textures/`)
- **Individual 1080p Beauty Renders (`.png`):** `/workspace/game-project/assets/renders/cargo_round1/cargo_gantry_r1_01.png` through `cargo_gantry_r1_05.png` (and mirrored in `/workspace/game-project/godot/renders/cargo_round1/`)
- **5-Panel Voting Comparison Sheet:** `/workspace/game-project/assets/renders/cargo_round1/cargo_gantry_round1_voting_sheet.png` (and mirrored in `/workspace/game-project/godot/renders/cargo_round1/`)

### 1.2 Coordinate System, Cargo Gantry Footprint & Pivot Convention
- **Metric Scale:** `1.0 unit = 1.0 meter`.
- **Target Cargo Gantry Footprint:** `2.50m – 2.70m Wide (X) × 1.40m – 1.50m Deep (Z) × 2.55m – 2.65m Tall (Y)`.
- **World Origin & Pivot Point:** Bottom-center `(0.0, 0.0, 0.0)` resting flush on the `Y = 0.0` floor plane (`min_y == 0.0000`, centered in `X` and `Z`), front container inspection windows, drone dock & manifest terminal facing **`+Z`**, rear structural stanchions at **`-Z`**.
- **Polygon Budget:** **`3,800 – 6,200 triangles`** per candidate.

### 1.3 Mandatory 4-Part 3D Orbital Logistics & Drone Kit (Required in Every Candidate!)
1. **Heavy 45° Chamfered Gantry Stanchions, Overhead Hoist Beam & Interlocking ISO Cargo Matrix (`Y = 0.0m – 2.60m`):**
   - Dark gunmetal titanium (`titanium_gunmetal_hull.png` / `metal_gunmetal_hull.png`, `#1A1E24`) and carbon-slate (`carbon_slate_frame.png` / `metal_carbon_slate.png`, `#282E38`) structural gantry frame with an overhead brushed-steel (`steel_machined_gantry.png` / `metal_brushed_steel.png`, `#88929E`) magnetic grappling hoist rail, housing a multi-bay matrix of **interlocking 45°-chamfered/hexagonal pressurized cargo containers** (scaling up our locked `footlocker_winner_01` aesthetic!) with **signal-orange (`accent_signal_orange.png` / `accent_safety_orange.png`, `#D95B26`) magnetic twist-locks**.
2. **Translucent Pressurized Container Windows & Drone Safety Shield (`glass_cargo_bay_translucent.png`, `alphaMode: "BLEND"`, `alpha ~ 0.19`):**
   - Each modular cargo container bay and the drone docking bay features a bevel-framed **`alphaMode: "BLEND"` translucent polycarbonate inspection viewport (`glass_cargo_bay_translucent.png`)**, revealing **3D stowed orbital supply drums (`composite_aerospace_white.png`), orbital-navy soft-goods pallet packs (`fabric_orbital_navy_pad.png`), and Li-S battery cylinders** inside!
3. **3D Autonomous Octo-Thruster Logistics Cargo Drone (`Y ~ 1.25m – 1.95m`):**
   - Docked inside its inductive charging cradle: a **sculpted 3D hard sci-fi utility cargo drone** featuring an octagonal aerospace-white & carbon-slate body (`composite_aerospace_white.png` / `carbon_slate_frame.png`), **4 angled thruster/rotor pods (`steel_machined_gantry.png`)**, ventral magnetic cargo grappling claws (`accent_signal_orange.png`), and a glowing cyan (`#00E5FF`) optical LiDAR sensor eye!
4. **Centrifuge Mass-Balance & RFID Manifest OLED Terminal (`oled_cargo_drone_logistics.png`):**
   - Flush-mounted **`oled_cargo_drone_logistics.png` display (`emissive_energy = 2.0`)** showing the 2×2 container rack grid, `0.002% DELTA` centrifuge mass-balance vector, and `98.6%` drone charge, paired with inductive charging umbilical arms and warm amber (`#FF9500`) floor-lock beacons.

---

## 2. Texture & Material Library Manifest (`/workspace/game-project/assets/textures/cargo_round1/`)

| # | Canonical Filename (Alias) | Format | Base Hex / Tone | Roughness | Metallic | Alpha / Emissive & Material Usage |
|---|----------------------------|--------|-----------------|-----------|----------|-----------------------------------|
| 1 | `titanium_gunmetal_hull.png` (`metal_gunmetal_hull.png`) | RGB | `#1A1E24` | `0.34` | `0.78` | Primary 45° chamfered gunmetal titanium gantry frame & ISO container hulls |
| 2 | `composite_aerospace_white.png` (`panel_aerospace_white.png`) | RGB | `#D8DEE6` | `0.28` | `0.08` | Smooth matte aerospace white drone carapace, container lids & supply drums |
| 3 | `carbon_slate_frame.png` (`metal_carbon_slate.png`) | RGB | `#282E38` | `0.40` | `0.58` | Dark carbon-slate floor pallet skids, stacking cones & drone bay liner |
| 4 | `steel_machined_gantry.png` (`metal_brushed_steel.png`) | RGB | `#88929E` | `0.20` | `0.90` | Brushed machined steel for overhead hoist I-beams, grappling claws & drone thrusters |
| 5 | `fabric_charcoal_flightpad.png` (`fabric_charcoal_cushion.png`) | RGB | `#242932` | `0.78` | `0.00` | Shock-absorbing bumper pads inside container cells & drone cradle |
| 6 | `fabric_orbital_navy_pad.png` (`fabric_navy_cushion.png`) | RGB | `#1D2C3C` | `0.76` | `0.00` | Deep orbital navy strapped cargo pallet bundles stowed inside containers |
| 7 | `accent_signal_orange.png` (`accent_safety_orange.png`) | RGB | `#D95B26` | `0.48` | `0.06` | Matte signal-orange for ISO twist-lock latches, crane hooks & drone grapple claws |
| 8 | `oled_cargo_drone_logistics.png` | RGB | `#0A0E14` + `#00E5FF` | `0.14` | `0.10` | **`emission_enabled: true` (`energy = 2.0`)**, 512×512 mass-balance & drone manifest OLED |
| 9 | `glass_cargo_bay_translucent.png` | **RGBA** | `#0E2230` + `#00E5FF` | `0.08` | `0.10` | **`alphaMode: "BLEND"` (`alpha ~ 0.19`)**, 256×256 translucent container & drone dock glass |
| 10 | `led_cyan_strip.png` / `led_amber_strip.png` / `led_uv_violet.png` / `led_ice_white.png` | RGB | `#00E5FF` / `#FF9500` / `#7B5CFF` / `#E0F4FF` | `0.15` | `0.00` | Emissive drone LiDAR eye, hoist hazard beacons & rack indicators |

---

## 3. Detailed Per-Candidate Specifications (`cargo_gantry_r1_01` through `cargo_gantry_r1_05`)

1. **`cargo_gantry_r1_01.glb` — `#01 — Aegis-7 Octagonal ISO Container Matrix & Overhead Crane Gantry` (`2.55m W × 1.45m D × 2.60m H`):**
   - Symmetrical 2×2 interlocking octagonal container rack under an overhead brushed-steel hoist beam, with a center-mounted `oled_cargo_drone_logistics.png` pillar and an upper-center drone docking perch.
2. **`cargo_gantry_r1_02.glb` — `#02 — Dual-Zone Split Interlocking Cargo Rack & Autonomous Drone Recharge Dock` (`2.65m W × 1.45m D × 2.60m H`):**
   - **Signature 65% / 35% asymmetric split-bay Aegis-7 sibling to all locked winners!**
   - **Left Bay (65% width, `1.72m` wide):** Heavy 45°-chamfered gunmetal & brushed-steel **2×2 Interlocking Modular Cargo Container Matrix** topped by an overhead magnetic grappling hoist beam (`Y = 2.38m`) with signal-orange crane trolley hooks. Each of the 4 modular containers (directly scaling up our locked `footlocker_winner_01` design!) features a bevel-framed **`alphaMode: "BLEND"` translucent polycarbonate inspection window (`glass_cargo_bay_translucent.png`)**—with the lower-left container lid posed 35° open on pneumatic struts—revealing **3D stowed white/orange supply drums, strapped orbital-navy cargo bundles, and Li-S power cylinders** lit by internal `#00E5FF` cyan strips!
   - **Right Bay (35% width, `0.93m` wide):** Full-height **Autonomous Logistics Drone Docking & Manifest Tower**:
     * Upper/Center Hangar Bay (`Y = 1.15m–2.35m`): Enclosed by a bevel-framed **`alphaMode: "BLEND"` translucent safety shield (`glass_cargo_bay_translucent.png`)**, housing the **3D Autonomous Octo-Thruster Utility Cargo Drone** suspended in its inductive recharge cradle with glowing `#00E5FF` cyan LiDAR eye, 4 angled thruster pods, and signal-orange ventral grappling claws!
     * Lower Control Console (`Y = 0.15m–1.10m`): Flush-mounted **`oled_cargo_drone_logistics.png` mass-balance & RFID manifest terminal**, coiled inductive power umbilical hoses, and a guarded **signal-orange magnetic pallet release lever**.
3. **`cargo_gantry_r1_03.glb` — `#03 — Honeycomb Hex-Cell Container Hive & Cantilevered Loader Arm` (`2.60m W × 1.48m D × 2.60m H`):**
   - Features 3 interlocking hexagonal cargo cells with translucent front portholes (`glass_cargo_bay_translucent.png`) and an articulated side robotic forklift/grappling arm holding a 3D logistics drone and cargo pod.
4. **`cargo_gantry_r1_04.glb` — `#04 — Vertical Paternoster Carousel Rack & Twin Drone Perch` (`2.55m W × 1.46m D × 2.62m H`):**
   - Vertical automated paternoster chain elevator cycling 4 translucent-windowed cargo pods past a central `oled_cargo_drone_logistics.png` operator bridge, flanked by twin upper drone charging pads.
5. **`cargo_gantry_r1_05.glb` — `#05 — Heavy Pressurized Cryo-Tanker ISO Frame & Telemetry Dock` (`2.65m W × 1.50m D × 2.60m H`):**
   - Combines two lower chamfered dry-cargo containers (with `glass_cargo_bay_translucent.png` windows) beneath a massive upper horizontal cylindrical cryo-fluid ISO tank with signal-orange valves, plus a side drone dock and `oled_cargo_drone_logistics.png` kiosk.

---

## 4. Standardized Camera Framing & Lighting Guide (`Gage` & `Rook`)

- **Target Look-At Point:** `(0.0, 1.28, 0.0)`
- **Camera Angles:** Heroic 3/4 front-isometric beauty angle (`yaw = ±18° to ±22°`, `pitch = -11°`, distance `~3.15m – 3.40m`, `FOV = 46°`).
- **Practical Lights:**
  1. `Container_Cells_Cyan_Glow`: Local Pos `(-0.42, 1.25, 0.12)`, Color `#00E5FF`, Energy `1.55`, Range `2.4m` (illuminates the 3D drums and navy packs inside the translucent container windows).
  2. `Drone_Bay_Ice_And_Violet`: Local Pos `(+0.72, 1.75, 0.15)`, Color `#E0F4FF`, Energy `1.50`, Range `2.1m` (spotlights the 3D autonomous cargo drone behind its translucent shield).
  3. `Hoist_And_Skid_Amber_Beacon`: Local Pos `(0.0, 2.35, 0.25)`, Color `#FF9500`, Energy `1.35`, Range `2.2m`.
