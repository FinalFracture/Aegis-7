# Room 02 Hero Fixture: Pressurized Bulkhead Airlock Hatch & Sector Checkpoint — Round 1 Design, 3D Mechanism, Translucent Viewport & Lighting Spec
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Pipeline Stage:** Room 02 Hero Fixture — 5-Choice Test (`corridor_door_r1_01` through `corridor_door_r1_05`)  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)  
**Target Teams:** Rook (3D Hard-Surface & Interlocking Blast-Door/Dog-Latch Modeling, Translucent Inspection Glass & UVs) & Gage (Godot 4 Scene Integration, Cycling Beacon Lighting & 1080p Beauty Renders)

---

## 1. Shared Standards & Technical Rules ("Aegis-7 Standard")

### 1.1 Output Paths & Naming Convention
- **3D Models (`.glb`):** `/workspace/game-project/assets/glb/corridor_round1/corridor_door_r1_01.glb` through `/workspace/game-project/assets/glb/corridor_round1/corridor_door_r1_05.glb`
- **Winner Export Path (after all 5 renders complete & 5-Bot Vote):** `/workspace/game-project/assets/glb/winners/corridor_door_winner_01_...glb`
- **Texture Suite (`.png`):** `/workspace/game-project/assets/textures/corridor_round1/` (and mirrored in `/workspace/game-project/assets/textures/`)
- **Individual 1080p Beauty Renders (`.png`):** `/workspace/game-project/assets/renders/corridor_round1/corridor_door_r1_01.png` through `corridor_door_r1_05.png` (and mirrored in `/workspace/game-project/godot/renders/corridor_round1/`)
- **5-Panel Voting Comparison Sheet:** `/workspace/game-project/assets/renders/corridor_round1/corridor_door_round1_voting_sheet.png` (and mirrored in `/workspace/game-project/godot/renders/corridor_round1/`)

### 1.2 Coordinate System, Portal Footprint & Posed Parted Configuration
- **Metric Scale:** `1.0 unit = 1.0 meter`.
- **Target Corridor Bulkhead Portal Footprint:**
  - **Width (`X`):** `2.40m – 2.65m` (spans a full sector corridor bulkhead bay)
  - **Depth (`Z`):** `0.55m – 0.75m` (deep 45° chamfered pressure bulkhead coaming)
  - **Height (`Y`):** `2.65m – 2.85m`
- **World Origin & Pivot Point:** Bottom-center `(0.0, 0.0, 0.0)` resting flush on the `Y = 0.0` deck sill (`min_y == 0.0000`, centered in `X` and `Z`), front checkpoint side facing **`+Z`**, rear corridor continuation facing **`-Z`**.
- **Polygon Budget:** **`3,000 – 5,800 triangles`** per candidate.

### 1.3 Mandatory 4-Part 3D Airlock & Checkpoint Kit (Required in Every Candidate!)
1. **45° Chamfered Octagonal Pressure Coaming & Raised Threshold Sill:**
   - Massive dark gunmetal titanium (`titanium_gunmetal_hull.png`, `#1A1E24`) and carbon-slate (`carbon_slate_frame.png`, `#282E38`) octagonal pressure bulkhead frame with a low-profile ramped machined-steel (`steel_machined_gantry.png`, `#88929E`) threshold sill at `Y = 0.0m–0.12m` and recessed amber (`#FF9500`) threshold warning chevrons.
2. **Partially Parted Blast-Door Leaves (`0.38m–0.46m` Center Gap) with Interlocking 3D Dog-Ear Locking Teeth:**
   - Pose the heavy aerospace-white (`composite_aerospace_white.png`, `#D8DEE6`) and carbon-slate blast doors **partially parted open (`~0.42m` center gap)** so the **sculpted 3D machined-steel interlocking wedge teeth / dog-latches** along the meeting edges AND the lit next-sector vista (`vista_oneill_cylinder_interior.png` backdrop plane at `Z = -0.55m`) are dramatically visible!
3. **Translucent Armored Inspection Windows (`glass_airlock_viewport_translucent.png`, `alphaMode: "BLEND"`, `alpha ~ 0.19`):**
   - Cut clean octagonal or stadium-beveled window apertures through the left and right door leaves (and any side emergency locker door), glazed with **`alphaMode: "BLEND"` translucent armored glass (`glass_airlock_viewport_translucent.png`)** so the viewer sees straight through the door windows into the illuminated sector beyond!
4. **Sector Access OLED Terminal (`oled_airlock_status.png`), Signal-Orange Manual Override Wheel & Cycling Beacons:**
   - Side bulkhead checkpoint station featuring the flush **`oled_airlock_status.png` biometric & differential pressure display**, a sculpted 3D **signal-orange (`accent_signal_orange.png`, `#D95B26`) rotary manual pressure-equalization handwheel or pull lever**, and overhead cyan (`#00E5FF`) / amber (`#FF9500`) airlock cycling light bars.

---

## 2. Texture & Material Library Manifest (`/workspace/game-project/assets/textures/corridor_round1/`)

All 11 textures are `1024×1024` ultra-clean, low-noise (`<1.0%–1.2%` micro-variation) PNGs stored in `/workspace/game-project/assets/textures/corridor_round1/` and mirrored in `/workspace/game-project/assets/textures/`.

| # | Filename | Format | Base Hex / Tone | Roughness | Metallic | Alpha / Emissive & Material Usage |
|---|----------|--------|-----------------|-----------|----------|-----------------------------------|
| 1 | `titanium_gunmetal_hull.png` | RGB | `#1A1E24` | `0.34` | `0.78` | Primary 45° chamfered octagonal bulkhead pressure frame |
| 2 | `composite_aerospace_white.png` | RGB | `#D8DEE6` | `0.28` | `0.08` | Smooth matte aerospace white blast-door leaves, inner coaming & fire extinguishers |
| 3 | `carbon_slate_frame.png` | RGB | `#282E38` | `0.40` | `0.58` | Dark carbon-slate door armor ribs, threshold ramps & side locker recesses |
| 4 | `steel_machined_gantry.png` | RGB | `#88929E` | `0.22` | `0.90` | Brushed machined steel for interlocking dog-latch teeth, hydraulic header tracks & grab bars |
| 5 | `fabric_charcoal_flightpad.png` | RGB | `#242932` | `0.78` | `0.00` | Padded inflatable airlock perimeter bladder seals |
| 6 | `fabric_orbital_navy_pad.png` | RGB | `#1D2C3C` | `0.76` | `0.00` | Stowed emergency trauma/breather kit packs in side lockers |
| 7 | `accent_signal_orange.png` | RGB | `#D95B26` | `0.48` | `0.06` | Matte signal-orange for manual override handwheels, emergency levers & extinguisher collars |
| 8 | `oled_airlock_status.png` | RGB | `#0A0E14` + `#00E5FF` | `0.14` | `0.10` | **`emission_enabled: true` (`energy = 2.0`)**, sector pressure, seal integrity & biometric OLED |
| 9 | `glass_airlock_viewport_translucent.png` | **RGBA** | `#0E2230` + `#00E5FF` | `0.08` | `0.10` | **`alphaMode: "BLEND"` (`alpha ~ 0.19`)**, translucent armored blast-door inspection windows |
| 10 | `vista_oneill_cylinder_interior.png` | RGB | `#103238` + `#00E5FF` | `1.00` | `0.00` | **Unshaded / Emissive (`energy = 1.35`)** next-sector corridor/cylinder vista plane behind portal |
| 11 | `vista_deep_space.png` | RGB | `#060A14` + `#00E5FF` | `1.00` | `0.00` | **Unshaded / Emissive (`energy = 1.35`)** outer-hull EVA airlock vista option |

---

## 3. Detailed Per-Candidate Specifications (`corridor_door_r1_01` through `corridor_door_r1_05`)

---

### Candidate 01: `corridor_door_r1_01` — `#01 — Aegis-7 Octagonal Bi-Parting Blast Hatch & Checkpoint`
*Dimensions: `2.45m W × 0.62m D × 2.75m H`*

- **3D Geometry & Layout Brief for Rook:**
  - Build a symmetrical **45° chamfered octagonal dark gunmetal titanium bulkhead portal (`2.45m W × 0.62m D × 2.75m H`)** with an overhead exposed machined-steel linear actuator gantry (`Y = 2.35m–2.65m`).
  - Inside the octagonal aperture, model **left and right aerospace-white & carbon-slate bi-parting blast-door leaves** parted open by `0.42m` in the center, showcasing **3 interlocking trapezoidal machined-steel dog-latch teeth** on each inner edge and **twin vertical octagonal `alphaMode: "BLEND"` translucent inspection windows (`glass_airlock_viewport_translucent.png`)** cut through the doors.
  - On the right bulkhead pier (`X = +0.98m`), mount the **`oled_airlock_status.png` checkpoint terminal** and a **sculpted 4-spoke signal-orange rotary manual override wheel**.

---

### Candidate 02: `corridor_door_r1_02` — `#02 — Dual-Zone Airlock Portal & Emergency O2/Extinguisher Side Bay`
*Dimensions: `2.60m W × 0.65m D × 2.75m H` — Direct asymmetric 68/32 Aegis-7 split-bay sibling to all 4 locked Sleeping Quarters winners!*

- **3D Geometry & Layout Brief for Rook:**
  - Design an **asymmetric 68% / 32% split-bay sector bulkhead portal (`2.60m W × 0.65m D × 2.75m H`)** that extends our locked Aegis-7 split-bay architectural signature directly into `Room 02 — Orbital Sector Transit Corridor`:
    - **Left Bay (68% width, `1.78m` wide):** Full-height **45° chamfered octagonal bi-parting blast hatch** with aerospace-white & carbon-slate door leaves parted `0.42m` at the center, **3D machined-steel interlocking dog-ear locking teeth**, **twin octagonal `alphaMode: "BLEND"` translucent armored windows (`glass_airlock_viewport_translucent.png`)** in the doors (looking through to an illuminated `vista_oneill_cylinder_interior.png` sector plane behind the portal), overhead cyan/amber cycling beacon arch, and ramped steel threshold sill.
    - **Right Bay (32% width, `0.82m` wide):** Integrated **Sector Checkpoint & Emergency Damage-Control Station**:
      * Upper/Center Console (`Y = 1.15m–1.72m`): Flush-mounted **`oled_airlock_status.png` biometric & differential pressure terminal** paired with a **sculpted signal-orange rotary pressure-equalization handwheel** and guarded manual release lever.
      * Lower/Side Translucent Emergency Locker (`Y = 0.22m–1.10m` or full-height split column): Enclosed by a bevel-framed **`alphaMode: "BLEND"` translucent glass door (`glass_airlock_viewport_translucent.png`)**, displaying **two 3D cylindrical CO2/Halon fire-suppression extinguishers** (with signal-orange nozzles & pressure gauges), a **3D orbital-navy emergency breather/trauma pack**, and machined-steel O2 recharge manifold pipes!

---

### Candidate 03: `corridor_door_r1_03` — `#03 — Cylindrical Plug-Door Pressure Lock & Rotary Dog-Latch Portal`
*Dimensions: `2.45m W × 0.70m D × 2.75m H`*

- **3D Geometry & Layout Brief for Rook:**
  - Construct a heavy **circular/stadium submarine-style orbital pressure bulkhead (`2.45m W × 0.70m D × 2.75m H`)** where twin curved plug-door halves translate outward on heavy machined-steel swing-link arms, featuring a central **circular translucent observation porthole (`glass_airlock_viewport_translucent.png`)** framed by 8 radial machined-steel locking dogs and a central signal-orange spider handwheel, with `oled_airlock_status.png` on the left frame.

---

### Candidate 04: `corridor_door_r1_04` — `#04 — Hex-Aperture Interlocking Wedge-Blade Sector Bulkhead`
*Dimensions: `2.50m W × 0.62m D × 2.75m H`*

- **3D Geometry & Layout Brief for Rook:**
  - Sculpt a wide **hexagonal pressure bulkhead (`2.50m W × 0.62m D × 2.75m H`)** featuring **four diagonal interlocking wedge-blade blast doors** (upper-left, lower-left, upper-right, lower-right) retracted partway into the 45° hex corners to leave a central diamond/hex opening, with triangular/trapezoidal **`glass_airlock_viewport_translucent.png` translucent windows** set into each blade and dual side `oled_airlock_status.png` status pillars.

---

### Candidate 05: `corridor_door_r1_05` — `#05 — Panoramic Twin-Window Observation Airlock & Decon Arch`
*Dimensions: `2.55m W × 0.68m D × 2.78m H`*

- **3D Geometry & Layout Brief for Rook:**
  - Build a wide **decontamination & observation airlock arch (`2.55m W × 0.68m D × 2.78m H`)** lined with internal UV-violet (`#7B5CFF`) and cyan (`#00E5FF`) sonic-mist decon nozzles inside the deep chamfered frame, wide bi-parting doors with **floor-to-head-height panoramic `glass_airlock_viewport_translucent.png` translucent glass panels**, a side `oled_airlock_status.png` biometric kiosk, and signal-orange emergency shower/purge pull-rings.

---

## 4. Standardized Camera Framing & Lighting Guide (`Gage` & `Rook`)

1. **1080p Hero Framing (`/workspace/game-project/godot/renders/corridor_round1/corridor_door_r1_01.png` .. `05.png` & `/workspace/game-project/assets/renders/corridor_round1/`):**
   - **Target Look-At Point:** `(0.0, 1.35, 0.0)`
   - **Camera Angles:** Heroic 3/4 corridor checkpoint angle (`yaw = ±16° to ±20°`, `pitch = -10°`, distance `~3.20m – 3.50m`, `FOV = 46°`) showing the full 2.75m tall octagonal pressure frame, the parted blast-door leaves with 3D interlocking dog teeth, the `vista_oneill_cylinder_interior.png` glow shining through both the center gap and the `alphaMode: "BLEND"` door windows, and the side `oled_airlock_status.png` checkpoint station!
2. **3-Point + Airlock Cycling Lighting Rig:**
   - **Key Light:** Pos `(2.4, 2.8, 2.8)`, Color `#E8F2FF`, Energy `1.30`.
   - **Fill Light:** Pos `(-2.4, 1.6, 2.4)`, Color `#78A8D8`, Energy `0.48`.
   - **Rim / Backlight (Through Parted Doors):** Pos `(0.0, 1.8, -1.6)`, Color `#00E5FF`, Energy `1.35`.
   - **Airlock Practicals:**
     1. `Arch_Cycling_Beacon_Amber`: Local Pos `(0.0, 2.48, 0.28)`, Color `#FF9500`, Energy `1.45`, Range `2.4m`.
     2. `Threshold_And_Checkpoint_Cyan`: Local Pos `(0.85, 1.35, 0.32)`, Color `#00E5FF`, Energy `1.50`, Range `2.2m`.
