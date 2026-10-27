# Modular Cargo & Footlocker Chest — Round 1 Design, 3D Interior Kit, Translucent Lid & Lighting Specification
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Pipeline Stage:** Non-Bunk Sleeping Quarters Fixture #6 — 5-Choice Test (`footlocker_r1_01` through `footlocker_r1_05`)  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)  
**Target Teams:** Rook (3D Hard-Surface & Pneumatic Lid/Drawer Modeling, 3D Stowed Cargo Props, Translucent Lid Window & UVs) & Gage (Godot 4 Scene Integration, Interior/Skid Lighting & 1080p Beauty Renders)

---

## 1. Shared Standards & Technical Rules ("Aegis-7 Standard")

### 1.1 Output Paths & Naming Convention
- **3D Models (`.glb`):** `/workspace/game-project/assets/glb/footlocker_round1/footlocker_r1_01.glb` through `/workspace/game-project/assets/glb/footlocker_round1/footlocker_r1_05.glb`
- **Winner Export Path (after all 5 renders complete & 5-Bot Vote):** `/workspace/game-project/assets/glb/winners/footlocker_winner_01_...glb`
- **Texture Suite (`.png`):** `/workspace/game-project/assets/textures/footlocker_round1/` (and mirrored in `/workspace/game-project/assets/textures/`)
- **Individual 1080p Beauty Renders (`.png`):** `/workspace/game-project/assets/renders/footlocker_round1/footlocker_r1_01.png` through `footlocker_r1_05.png` (and mirrored in `/workspace/game-project/godot/renders/footlocker_round1/`)
- **5-Panel Voting Comparison Sheet:** `/workspace/game-project/assets/renders/footlocker_round1/footlocker_round1_voting_sheet.png`

### 1.2 Coordinate System, Footprint & Posed Showcase Configuration
- **Metric Scale:** `1.0 unit = 1.0 meter`.
- **Target Low-Profile Footlocker Footprint:**
  - **Width (`X`):** `0.98m – 1.12m`
  - **Depth (`Z`):** `0.50m – 0.60m`
  - **Height (`Y`):** `0.48m – 0.58m` main chest body height (reaching `0.74m – 0.88m` total height when the hinged lid / gullwing / cantilever cover is posed partially open at `~35°–42°`).
- **World Origin & Pivot Point:** Bottom-center `(0.0, 0.0, 0.0)` resting flush on the `Y = 0.0` floor plane (`min_y == 0.0000`, centered in `X` and `Z`).
- **Front Orientation (`+Z` Forward):** Front latches, digital OLED manifest strip, and open lid/drawer access face **`+Z`**, rear hinges face **`-Z`**.
- **Polygon Budget:** **`2,500 – 5,000 triangles`** per candidate.

### 1.3 Mandatory 4-Part 3D Cargo & Footlocker Kit (Required in Every Candidate!)
Every candidate (`footlocker_r1_01` through `footlocker_r1_05`) must include these four signature 3D sub-assemblies so it pairs seamlessly with our locked Sleeping Quarters fixtures (`locker_winner_01_dual_bay_bulkhead.glb`, `vanity_winner_01_dual_zone_grooming.glb`, and our incoming Wall Desk winner) AND scales directly into `Room 10 — Modular Cargo Hold & Logistics Drone Bay`:
1. **45° Chamfered Octagonal Armor Shell & Interlocking Magnetic Skid Base:**
   - Heavy-duty dark gunmetal titanium (`titanium_gunmetal_hull.png`, `#1A1E24`) and matte aerospace-white (`composite_aerospace_white.png`, `#D8DEE6`) trunk body with 45° beveled corners, protective carbon-slate (`carbon_slate_frame.png`, `#282E38`) floor-lock skids, machined-steel (`steel_machined_gantry.png`, `#88929E`) recessed swing carry handles on the left/right ends (`±X`), and **signal-orange (`accent_signal_orange.png`, `#D95B26`) heavy cam-lock latches + rotary pressure-equalization valve**.
2. **Translucent Inspection Window (`alphaMode: "BLEND"`) + Partially Open Lid on Pneumatic Struts:**
   - Pose the hinged lid / gullwing / cantilever cover **partially open (`~35°–42°`) supported by twin machined-steel telescoping pneumatic struts (`steel_machined_gantry.png`)**, AND build a bevel-framed **`alphaMode: "BLEND"` translucent polycarbonate inspection viewport (`glass_cargo_lid_translucent.png`, `alpha ~ 0.18`)** into the lid or inner dust cover so the 3D stowed interior kit is visible both directly and through the tinted glass!
3. **3D Stowed Personal Crew Gear Inside the Foam-Lined Bay:**
   - Inside the chest cavity (`Y ~ 0.14m – 0.48m`), model a custom-contoured charcoal EVA foam organizer bed (`fabric_charcoal_flightpad.png`) cradling **3D stowed equipment**:
     * **Rolled Orbital-Navy Flight Garment / Kit Bundle** (`fabric_orbital_navy_pad.png`) secured with signal-orange retention straps.
     * **Two Cylindrical Li-S Power / Emergency Ration Canisters** (`composite_aerospace_white.png` & `steel_machined_gantry.png` with signal-orange end caps).
     * **Chamfered Hard-Shell Field Med / Multi-Tool Case** (`composite_aerospace_white.png` with cyan status indicator).
4. **Digital OLED Manifest Strip (`oled_cargo_manifest.png`) & Internal/Skid LED Indicators:**
   - Flush-mounted front-bevel **OLED RFID Cargo Manifest & Biometric Lock Display** (`oled_cargo_manifest.png`, `emissive_energy = 2.0`), paired with an **internal cyan (`#00E5FF`) compartment light strip** illuminating the 3D stowed gear and **amber (`#FF9500`) magnetic floor-lock beacons** on the base skids.

---

## 2. Texture & Material Library Manifest (`/workspace/game-project/assets/textures/footlocker_round1/`)

All 9 textures are `1024×1024` ultra-clean, low-noise (`<1.0%–1.2%` micro-variation) PNGs stored in `/workspace/game-project/assets/textures/footlocker_round1/` and mirrored in `/workspace/game-project/assets/textures/`.

| # | Filename | Format | Base Hex / Tone | Roughness | Metallic | Alpha / Emissive & Material Usage |
|---|----------|--------|-----------------|-----------|----------|-----------------------------------|
| 1 | `titanium_gunmetal_hull.png` | RGB | `#1A1E24` | `0.34` | `0.78` | Primary 45° chamfered gunmetal titanium chest hull & corner armor bumpers |
| 2 | `composite_aerospace_white.png` | RGB | `#D8DEE6` | `0.28` | `0.08` | Smooth matte aerospace white molded lid panels, inner trays & ration/battery canisters |
| 3 | `carbon_slate_frame.png` | RGB | `#282E38` | `0.40` | `0.58` | Dark carbon-slate magnetic floor-lock skids, stacking ribs & drawer rails |
| 4 | `steel_machined_gantry.png` | RGB | `#88929E` | `0.22` | `0.90` | Brushed machined steel for pneumatic lid struts, cam latches, side carry handles & D-rings |
| 5 | `fabric_charcoal_flightpad.png` | RGB | `#242932` | `0.78` | `0.00` | Contoured charcoal ballistic flightpad for bench seat cushions & die-cut EVA foam inserts |
| 6 | `fabric_orbital_navy_pad.png` | RGB | `#1D2C3C` | `0.76` | `0.00` | Deep orbital navy fabric for stowed crew garment rolls & soft-goods kit bags |
| 7 | `accent_signal_orange.png` | RGB | `#D95B26` | `0.48` | `0.06` | Matte signal-orange for heavy security cam-latches, rotary purge valves & canister caps |
| 8 | `oled_cargo_manifest.png` | RGB | `#0A0E14` + `#00E5FF` | `0.14` | `0.10` | **`emission_enabled: true` (`energy = 2.0`)**, digital RFID cargo manifest & biometric lock strip |
| 9 | `glass_cargo_lid_translucent.png` | **RGBA** | `#0E2230` + `#00E5FF` | `0.08` | `0.10` | **`alphaMode: "BLEND"` (`alpha ~ 0.18`)**, translucent armored polycarbonate lid viewport & inner dust shield |

---

## 3. Detailed Per-Candidate Specifications (`footlocker_r1_01` through `footlocker_r1_05`)

---

### Candidate 01: `footlocker_r1_01` — `#01 — Aegis-7 Octagonal Bulkhead Footlocker & Bench Chest`
*Dimensions: `1.05m W × 0.54m D × 0.55m H` (body) / `0.84m H` (with open right lid)*

- **Color Palette (Hex Codes):**
  - 45° Chamfered Trunk Hull: Gunmetal Titanium `#1A1E24` & Carbon Slate Skids `#282E38`
  - Molded Lid Trim & Inner Tray: Matte Aerospace White `#D8DEE6`
  - Left Bench Seat Pad & Inner Foam: Charcoal Flightpad `#242932` & Orbital Navy `#1D2C3C`
  - Pneumatic Lid Struts & Handles: Machined Steel `#88929E` & Signal Orange Latches `#D95B26`
  - Practical Lighting: Internal Tray Cyan `#00E5FF` + Skid Lock Amber `#FF9500`
- **3D Geometry & Layout Brief for Rook:**
  - Build a low-profile **45° chamfered octagonal gunmetal titanium & carbon-slate footlocker (`1.05m W × 0.54m D × 0.55m H`)** with a split top deck:
    - **Left Half (`X = -0.52m` to `-0.02m`):** Fixed contoured **charcoal flightpad crew dressing-bench cushion (`fabric_charcoal_flightpad.png`)**.
    - **Right Half (`X = -0.02m` to `+0.52m`):** Hinged aerospace-white & titanium lid with a central **translucent `glass_cargo_lid_translucent.png` inspection window**, propped open at `38°` on twin machined-steel pneumatic struts to reveal the charcoal foam bay containing the 3D navy garment roll, twin power canisters, and med case.
  - Mount the `oled_cargo_manifest.png` biometric lock strip and two signal-orange cam latches on the front `+Z` bevel.

---

### Candidate 02: `footlocker_r1_02` — `#02 — Dual-Bay Split Cargo Trunk & Pull-Out Drawer Module`
*Dimensions: `1.10m W × 0.56m D × 0.58m H` (body) / `0.85m H` (open lid) — Direct asymmetric 65/35 sibling to Locked Locker `#02`, Vanity `#03`, and Desk `#02`!*

- **Color Palette (Hex Codes):**
  - Asymmetric 65% / 35% Split Trunk Chassis: Gunmetal Titanium `#1A1E24` & Carbon Slate Divider `#282E38`
  - Left Cargo Bay Lid & Right Pull-Out Drawers: Aerospace White `#D8DEE6` & Brushed Steel `#88929E`
  - Translucent Top Viewport Lid: `glass_cargo_lid_translucent.png` (`alpha ~ 0.18`)
  - Stowed Gear & Foam Inserts: Orbital Navy `#1D2C3C`, Charcoal `#242932` & Signal Orange `#D95B26`
  - Practical Lighting: Left Bay Cyan `#00E5FF` + Right Drawer Amber `#FF9500`
- **3D Geometry & Layout Brief for Rook:**
  - Design an **asymmetric 65% / 35% split-bay modular cargo chest (`1.10m W × 0.56m D × 0.58m H`)** that continues the exact Aegis-7 split-bay family language of our locked Sleeping Quarters fixtures:
    - **Left Bay (65% width, `0.71m` wide):** Deep pressurized equipment well topped by a chamfered aerospace-white & steel lid with a large **`alphaMode: "BLEND"` translucent polycarbonate window (`glass_cargo_lid_translucent.png`)**, posed open at `35°` on twin hydraulic struts. Inside: die-cut charcoal foam bed holding **two cylindrical white/orange Li-S power cells, a rolled orbital-navy EVA under-suit bundle, and a hard-shell diagnostic case** lit by a recessed cyan LED bar.
    - **Right Bay (35% width, `0.39m` wide):** Fixed contoured charcoal bench seat pad on top (`Y = 0.56m`), with **two stacked heavy-duty slide-out organizer drawers** below on machined-steel telescoping rails—pose the **lower drawer pulled forward `0.16m` (`+Z`)** showing 3D stowed spare ration bars and tool cartridges inside, while the upper drawer front carries the flush **`oled_cargo_manifest.png` digital manifest screen** and signal-orange cam-lock latch.

---

### Candidate 03: `footlocker_r1_03` — `#03 — Hex-Frame Interlocking Orbital Logistics Crate`
*Dimensions: `1.00m W × 0.58m D × 0.56m H` (body) / `0.80m H` (open gullwing doors)*

- **Color Palette (Hex Codes):**
  - Hexagonal Exo-Rib Cage: Carbon Slate `#282E38` & Machined Steel `#88929E`
  - Inner Pressurized Hull: Gunmetal Titanium `#1A1E24` & Aerospace White `#D8DEE6`
  - Center Gullwing Translucent Doors: `glass_cargo_lid_translucent.png` (`alpha ~ 0.18`)
  - Corner Stacking Cones & Latches: Signal Orange `#D95B26`
- **3D Geometry & Layout Brief for Rook:**
  - Sculpt an **elongated hexagonal-section orbital logistics crate (`1.00m W × 0.58m D × 0.56m H`)** wrapped in three external machined-steel & carbon-slate structural exo-ribs with four corner interlocking stacking cones.
  - Top the crate with **dual gullwing / butterfly hinged translucent doors (`glass_cargo_lid_translucent.png`)** parted open at `35°` on left and right pneumatic struts, revealing a shock-mounted internal rack holding **four cylindrical power/O2 canisters, a navy kit pack, and a central `oled_cargo_manifest.png` telemetry strip**.

---

### Candidate 04: `footlocker_r1_04` — `#04 — Cantilevered Biometric Vault & Sliding Tray Footlocker`
*Dimensions: `1.02m W × 0.52m D × 0.54m H` (body) / `0.78m H` (cantilevered lid)*

- **Color Palette (Hex Codes):**
  - Molded High-Security Vault Shell: Matte Aerospace White `#D8DEE6` & Gunmetal Titanium Base `#1A1E24`
  - Pantograph Cantilever Arms: Brushed Machined Steel `#88929E`
  - Inner Translucent Dust Shield: `glass_cargo_lid_translucent.png` (`alpha ~ 0.18`)
  - Precision Foam Cutouts & Gear: Charcoal Flightpad `#242932`, Orbital Navy `#1D2C3C` & Signal Orange `#D95B26`
- **3D Geometry & Layout Brief for Rook:**
  - Build a sleek, filleted **aerospace-white & dark-titanium personal biometric vault (`1.02m W × 0.52m D × 0.54m H`)** whose upper lid lifts and cantilevers rearward on **four machined-steel pantograph link arms**.
  - Directly over the upper tool tier, place a sleek **`alphaMode: "BLEND"` translucent polycarbonate dust shield (`glass_cargo_lid_translucent.png`)** revealing precision charcoal foam cutouts containing 3D optical data-cubes, cylindrical power cells, and a navy flight kit, with a prominent angled front **`oled_cargo_manifest.png` biometric scanner console**.

---

### Candidate 05: `footlocker_r1_05` — `#05 — Twin-Cylinder Pressurized Survival & Gear Pod Chest`
*Dimensions: `1.08m W × 0.56m D × 0.56m H` (body) / `0.82m H` (open clamshell)*

- **Color Palette (Hex Codes):**
  - Twin Horizontal Pressure Pods: Aerospace White `#D8DEE6` & Gunmetal Titanium Cradle `#1A1E24`
  - Clamshell Translucent Viewport Hood: `glass_cargo_lid_translucent.png` (`alpha ~ 0.18`)
  - Rotary Pressure Handwheel & Latches: Signal Orange `#D95B26` & Machined Steel `#88929E`
- **3D Geometry & Layout Brief for Rook:**
  - Construct a heavy-duty **pressurized EVA survival chest (`1.08m W × 0.56m D × 0.56m H`)** formed by twin horizontal rounded-stadium pressure vessels seated inside a 45° chamfered gunmetal skid frame, with a **sculpted signal-orange 4-spoke rotary pressure-equalization handwheel** on the left end cap (`-X`), `oled_cargo_manifest.png` on the front bezel, and an upper **curved clamshell translucent hood (`glass_cargo_lid_translucent.png`)** raised on twin struts to expose the 3D emergency survival canisters and navy pressure pack inside.

---

## 4. Standardized Camera Framing & Lighting Guide (`Gage` & `Rook`)

1. **1080p Hero Framing (`/workspace/game-project/assets/renders/footlocker_round1/footlocker_r1_01.png` .. `footlocker_r1_05.png`):**
   - Because the Modular Cargo & Footlocker Chest is a low-profile horizontal prop (`~1.05m W × 0.55m D × 0.55m–0.85m H`):
     - **Target Look-At Point:** `(0.0, 0.36, 0.0)`
     - **Camera Angles:** Elevated 3/4 front-isometric beauty angle (`yaw = ±24° to ±28°`, `pitch = -22° to -25°`, distance `~1.65m – 1.85m`, `FOV = 45°`) looking down at `~24°` into the open lid, translucent polycarbonate window, 3D stowed foam-lined gear tray, and front OLED manifest display!
2. **3-Point + Practical Cargo Lighting Rig:**
   - **Key Light:** Pos `(1.8, 2.2, 2.0)`, Color `#E8F2FF`, Energy `1.32`.
   - **Fill Light:** Pos `(-1.9, 1.3, 1.8)`, Color `#78A8D8`, Energy `0.48`.
   - **Rim Light:** Pos `(0.0, 2.0, -1.5)`, Color `#00E5FF`, Energy `0.92`.
   - **Footlocker Practicals:**
     1. `Internal_Tray_Cyan_Glow`: Local Pos `(0.0, 0.48, 0.0)`, Color `#00E5FF` (illuminates the 3D canisters, navy garment roll, and foam tray inside the chest), Energy `1.55`, Range `1.6m`.
     2. `Skid_Lock_Amber_Glow`: Local Pos `(0.0, 0.10, 0.28)`, Color `#FF9500`, Energy `1.15`, Range `1.3m`.
3. **5-Panel Voting Comparison Sheet (`/workspace/game-project/assets/renders/footlocker_round1/footlocker_round1_voting_sheet.png`):**
   - Composite all 5 candidates (`#01` through `#05`) with clear title badges, dimensions, and triangle counts.
