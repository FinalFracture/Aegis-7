# Personal Wall Terminal & Fold-Down Cabin Desk — Round 1 Design, 3D Workstation Kit, Translucent Holo-HUD & Lighting Specification
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Pipeline Stage:** Non-Bunk Sleeping Quarters Fixture #3 — 5-Choice Test (`walldesk_r1_01` through `walldesk_r1_05`)  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)  
**Target Teams:** Rook (3D Hard-Surface & Fold-Down Strut/Hinge Modeling, Desktop Props, Translucent Holo-Glass & UVs) & Gage (Godot 4 Scene Integration, Task/Cove Lighting & 1080p Beauty Renders)

---

## 1. Shared Standards & Technical Rules ("Aegis-7 Standard")

### 1.1 Output Paths & Naming Convention
- **3D Models (`.glb`):** `/workspace/game-project/assets/glb/walldesk_round1/walldesk_r1_01.glb` through `/workspace/game-project/assets/glb/walldesk_round1/walldesk_r1_05.glb`
- **Winner Export Path (after all 5 renders complete & 5-Bot Vote):** `/workspace/game-project/assets/glb/winners/walldesk_winner_01_...glb`
- **Texture Suite (`.png`):** `/workspace/game-project/assets/textures/walldesk_round1/` (and mirrored in `/workspace/game-project/assets/textures/`)
- **Individual 1080p Beauty Renders (`.png`):** `/workspace/game-project/assets/renders/walldesk_round1/walldesk_r1_01.png` through `walldesk_r1_05.png` (and mirrored in `/workspace/game-project/godot/renders/walldesk_round1/`)
- **5-Panel Voting Comparison Sheet:** `/workspace/game-project/assets/renders/walldesk_round1/walldesk_round1_voting_sheet.png`

### 1.2 Coordinate System, Footprint & Deployed Configuration
- **Metric Scale:** `1.0 unit = 1.0 meter`.
- **Target Compact Crew Cabin Footprint:** `0.88m – 1.08m Wide (X) × 0.58m – 0.70m Deep (Z) × 1.88m – 2.02m Tall (Y)`.
- **World Origin & Pivot Point:** Bottom-center `(0.0, 0.0, 0.0)` resting flush on the `Y = 0.0` floor plane (`min_y == 0.0000`, centered in `X` and `Z`).
- **Front Orientation (`+Z` Forward — Deployed Working Mode):**
  - The recessed bulkhead housing sits toward **`-Z`**, while the **fold-down desk leaf is deployed horizontally forward (`+Z`, `Y ~ 0.74m–0.76m`)** and the **articulated swing-arm or tuck-away crew stool is positioned in front (`+Z`, `Y ~ 0.46m–0.48m`)** so the active crew workstation silhouette is clearly showcased!
- **Polygon Budget:** **`2,800 – 5,500 triangles`** per candidate.

### 1.3 Mandatory 4-Part 3D Cabin Workstation Kit (Required in Every Candidate!)
Every candidate (`walldesk_r1_01` through `walldesk_r1_05`) must include these four signature 3D sub-assemblies so it pairs seamlessly with our locked Sleeping Quarters fixtures (`locker_winner_01_dual_bay_bulkhead.glb` and `vanity_winner_01_dual_zone_grooming.glb`):
1. **45° Chamfered Bulkhead Housing & Deployed Fold-Down Desk Leaf (`Y ~ 0.74m – 0.76m`):**
   - Recessed dark gunmetal titanium (`titanium_gunmetal_hull.png`, `#1A1E24`) bulkhead cabinet with a deployed horizontal matte aerospace-white (`composite_aerospace_white.png`, `#D8DEE6`) and dark carbon-slate (`carbon_slate_frame.png`, `#282E38`) beveled desk surface.
   - Supported by **twin angled machined-steel (`steel_machined_gantry.png`, `#88929E`) hydraulic pistons / scissor struts**, heavy knuckle hinges, and **signal-orange (`accent_signal_orange.png`, `#D95B26`) fold-lock latches**.
2. **Recessed OLED Cabin Comms Terminal + Translucent Holo-HUD / Privacy Glass (`alphaMode: "BLEND"`):**
   - Wide-aspect chamfered or slightly curved **OLED Personal Comms & Cabin Log Monitor** (`oled_cabin_terminal.png`, `emissive_energy = 2.0`) mounted inside the recessed upper alcove (`Y ~ 1.05m – 1.48m`).
   - Paired with an **angled floating translucent Holo-HUD teleprompter combiner pane, translucent overhead glare canopy, or translucent side storage door** (`glass_holo_hud_translucent.png`, `alphaMode: "BLEND"`, `alpha ~ 0.19`) so the cyan reticle and the 3D elements behind the glass read clearly.
3. **3D Desktop Props (Docked Personal Data-Pad, Capacitive Keyboard Inlay & Magnetic Zero-G Mug):**
   - **Docked 3D Personal Data-Pad / Slate:** Angled desktop charging cradle holding a chamfered tablet mapped with `oled_datapad_screen.png` (`emissive_energy = 1.8`).
   - **Recessed Low-Profile Keyboard & Trackpad Zone:** Flush-inset carbon-slate tactile key matrix on the center-left of the desk leaf with subtle cyan edge illumination.
   - **Lathed 3D Magnetic Thermal Mug:** Brushed-steel (`steel_machined_gantry.png`) insulated zero-G mug with handle & sip-lid seated inside a glowing cyan magnetic coaster ring on the right side of the desk leaf.
4. **Articulated Swing-Arm or Tuck-Away Crew Stool (`Y ~ 0.46m – 0.48m`):**
   - Cantilevered machined-steel swing-arm tube (`steel_machined_gantry.png`) or recessed floor-track pedestal supporting a sculpted, ergonomic **charcoal/navy flightpad seat cushion** (`fabric_charcoal_flightpad.png` / `fabric_orbital_navy_pad.png`) with a tubular footrest ring and signal-orange swivel/height release lever.

---

## 2. Texture & Material Library Manifest (`/workspace/game-project/assets/textures/walldesk_round1/`)

All 10 textures are `1024×1024` ultra-clean, low-noise (`<1.0%–1.2%` micro-variation) PNGs stored in `/workspace/game-project/assets/textures/walldesk_round1/` and mirrored in `/workspace/game-project/assets/textures/`.

| # | Filename | Format | Base Hex / Tone | Roughness | Metallic | Alpha / Emissive & Material Usage |
|---|----------|--------|-----------------|-----------|----------|-----------------------------------|
| 1 | `titanium_gunmetal_hull.png` | RGB | `#1A1E24` | `0.34` | `0.78` | Primary 45° chamfered gunmetal titanium outer bulkhead cabinet |
| 2 | `composite_aerospace_white.png` | RGB | `#D8DEE6` | `0.28` | `0.08` | Smooth matte aerospace white fold-down desk leaf, inner alcove liner & docks |
| 3 | `carbon_slate_frame.png` | RGB | `#282E38` | `0.40` | `0.58` | Dark carbon-slate anti-glare desk inlay, keyboard bezel, side shelves & stool base |
| 4 | `steel_machined_gantry.png` | RGB | `#88929E` | `0.22` | `0.90` | Brushed machined steel for hydraulic fold-down struts, hinges, stool swing-arm & thermal mug |
| 5 | `fabric_charcoal_flightpad.png` | RGB | `#242932` | `0.78` | `0.00` | Contoured charcoal ballistic flightpad for crew stool seat cushion & wrist pad |
| 6 | `fabric_orbital_navy_pad.png` | RGB | `#1D2C3C` | `0.76` | `0.00` | Deep orbital navy acoustic alcove back-padding & stowed utility pouches |
| 7 | `accent_signal_orange.png` | RGB | `#D95B26` | `0.48` | `0.06` | Matte signal-orange for fold-down lock latches, stool release levers & cable clamps |
| 8 | `oled_cabin_terminal.png` | RGB | `#0A0E14` + `#00E5FF` | `0.14` | `0.10` | **`emission_enabled: true` (`energy = 2.0`)**, widescreen OLED crew comms, orbital arc & waveform terminal |
| 9 | `oled_datapad_screen.png` | RGB | `#0A0E14` + `#00E5FF` | `0.14` | `0.10` | **`emission_enabled: true` (`energy = 1.8`)**, docked 3D personal data-pad schematic & checklist UI |
| 10 | `glass_holo_hud_translucent.png` | **RGBA** | `#0E2230` + `#00E5FF` | `0.08` | `0.10` | **`alphaMode: "BLEND"` (`alpha ~ 0.19`)**, translucent cyan-tinted Holo-HUD combiner pane & locker door |

---

## 3. Detailed Per-Candidate Specifications (`walldesk_r1_01` through `walldesk_r1_05`)

---

### Candidate 01: `walldesk_r1_01` — `#01 — Recessed Octagonal Bulkhead Fold-Down Comms Desk`
*Dimensions: `0.95m W × 0.62m D × 1.95m H`*

- **Color Palette (Hex Codes):**
  - Outer 45° Chamfered Bulkhead Niche: Gunmetal Titanium `#1A1E24` & Carbon Slate `#282E38`
  - Deployed Fold-Down Desk Leaf & Inner Alcove: Matte Aerospace White `#D8DEE6`
  - Hydraulic Pistons, Stool Swing-Arm & Thermal Mug: Machined Steel `#88929E`
  - Stool Cushion & Acoustic Backwall: Charcoal Flightpad `#242932` & Orbital Navy `#1D2C3C`
  - Fold-Lock Collars: Signal Orange `#D95B26`
  - Practical Lighting: Downward Task Spot `#E0F4FF`, Terminal/Coaster Cyan `#00E5FF`, Under-Desk Toe Guide `#FF9500`
- **3D Geometry & Layout Brief for Rook:**
  - Frame a **45° chamfered octagonal gunmetal titanium bulkhead niche (`0.95m W × 0.62m D × 1.95m H`)** with a recessed navy acoustic back panel.
  - Hinge a **chamfered aerospace-white & carbon-slate fold-down desk leaf (`0.84m W × 0.44m D` at `Y = 0.75m`)** supported by **twin diagonal machined-steel hydraulic telescopic struts** with signal-orange locking collars.
  - Inside the upper niche (`Y = 1.05m–1.52m`), mount a **curved 24-inch widescreen OLED comms terminal (`oled_cabin_terminal.png`)** with an **angled floating translucent `alphaMode: "BLEND"` Holo-HUD teleprompter combiner pane (`glass_holo_hud_translucent.png`)** suspended 0.10m in front of the screen on brushed-steel micro-arms.
  - Populate the desk leaf with the **3D docked data-pad (`oled_datapad_screen.png`)**, recessed carbon-slate keyboard/wrist pad, and **lathed steel magnetic thermal mug** on a glowing cyan coaster ring.
  - Below the desk, model a **cantilevered single-arm tubular steel swing-out crew stool (`Y = 0.47m`)** with a sculpted charcoal flightpad cushion.

---

### Candidate 02: `walldesk_r1_02` — `#02 — Dual-Tier Split Comms & Storage Drop-Leaf Station`
*Dimensions: `1.05m W × 0.65m D × 2.00m H` — Asymmetric split-bay companion to `locker_winner_01` and `vanity_winner_01`!*

- **Color Palette (Hex Codes):**
  - Asymmetric 68% / 32% Split Bulkhead Housing: Gunmetal Titanium `#1A1E24` & Carbon Slate Divider `#282E38`
  - Left Fold-Down Desk Leaf & Terminal Bay: Aerospace White `#D8DEE6` & Brushed Steel `#88929E`
  - Right Translucent Personal Log & Slate Tower: `glass_holo_hud_translucent.png` (`alpha ~ 0.19`), Orbital Navy `#1D2C3C` & Signal Orange `#D95B26`
  - Practical Lighting: Left Terminal Cyan/Ice-White (`#00E5FF` / `#E0F4FF`) + Right Storage Tower Amber/Cyan (`#FF9500` / `#00E5FF`)
- **3D Geometry & Layout Brief for Rook:**
  - Build an **asymmetric 68% / 32% split-bay bulkhead workstation (`1.05m W × 0.65m D × 2.00m H`)** that directly matches the architectural rhythm of our locked Dual-Bay EVA Locker (`#02`) and locked Dual-Zone Hygiene Vanity (`#03`):
    - **Left Bay (68% width, `0.71m` wide):** Houses the deployed aerospace-white fold-down desk leaf (`Y = 0.75m`) on heavy machined knuckle hinges & diagonal struts, the recessed widescreen `oled_cabin_terminal.png` display, an angled overhead **translucent `glass_holo_hud_translucent.png` glare/HUD canopy visor**, the 3D docked data-pad (`oled_datapad_screen.png`), keyboard inlay, magnetic mug, and a **twin-rail tuck-away pedestal crew stool (`Y = 0.47m`)** with charcoal flightpad seat and signal-orange release latch.
    - **Right Bay (32% width, `0.34m` wide):** Full-height 3-tier **Personal Comms & Data-Slate Locker Tower** enclosed by a beveled **`alphaMode: "BLEND"` translucent glass door (`glass_holo_hud_translucent.png`)**, displaying:
      * Top shelf: 3D vertical charging rack with 3 metallic/glowing personal data-cartridges & auxiliary `oled_datapad_screen.png` diagnostic slate.
      * Middle shelf: Sculpted 3D orbital-navy aviation/comms headset hanging on a machined steel hook + personal log module.
      * Bottom shelf: Twin cylindrical emergency backup power cells with signal-orange terminals.

---

### Candidate 03: `walldesk_r1_03` — `#03 — Cantilevered Scissors-Strut Drop Desk & Holo-Visor Alcove`
*Dimensions: `0.92m W × 0.65m D × 1.92m H`*

- **Color Palette (Hex Codes):**
  - Molded Capsule Alcove: Matte Aerospace White `#D8DEE6` & Gunmetal Titanium Frame `#1A1E24`
  - External Pantograph Scissor-Link Struts: Brushed Machined Steel `#88929E` & Signal Orange Pivots `#D95B26`
  - Wrap-Around Translucent Privacy Canopy: `glass_holo_hud_translucent.png` (`alpha ~ 0.19`)
  - Zero-G Perch Stool: Orbital Navy `#1D2C3C` & Charcoal `#242932`
- **3D Geometry & Layout Brief for Rook:**
  - Sculpt a stadium-beveled aerospace-white & titanium wall pod (`0.92m W × 0.65m D × 1.92m H`) where the fold-down desk leaf (`Y = 0.75m`) is suspended by **external articulated X-frame / scissor-link machined-steel pantograph struts** on the left and right sides with signal-orange pivot bolts.
  - Over the upper terminal bay (`Y = 1.25m–1.78m`), model a **curved quarter-sphere translucent cyan HUD privacy hood (`glass_holo_hud_translucent.png`)** arcing out over the recessed `oled_cabin_terminal.png` display.
  - Include the docked `oled_datapad_screen.png` tablet, keyboard inlay, magnetic steel mug, and an ergonomic **angled zero-G perch stool with knee-bolster pads**.

---

### Candidate 04: `walldesk_r1_04` — `#04 — Sliding Track Bulkhead Console & Stowable Flight Stool`
*Dimensions: `1.00m W × 0.60m D × 1.98m H`*

- **Color Palette (Hex Codes):**
  - Vertical Track Bulkhead Frame: Carbon Slate `#282E38` & Gunmetal Titanium `#1A1E24`
  - Twin Linear Guide Rails & Folding Stool Frame: Machined Steel `#88929E`
  - Adjustable Desk Carriage & Upper Locker: Aerospace White `#D8DEE6` & `glass_holo_hud_translucent.png`
- **3D Geometry & Layout Brief for Rook:**
  - Feature **two prominent vertical machined-steel linear guide rails (`X = ±0.42m, Y = 0.12m–1.88m`)** mounted inside a dark gunmetal bulkhead frame, carrying a height-adjustable cantilevered desk leaf (`Y = 0.75m`) with signal-orange rail-lock levers.
  - Mount the main `oled_cabin_terminal.png` monitor + angled side telemetry wings at `Y = 1.15m`, and top the unit (`Y = 1.56m–1.90m`) with an **overhead translucent glass storage cabinet (`glass_holo_hud_translucent.png`)** containing 3D stowed binders/slates and spare power packs.
  - Below the desk, place a **folding tubular-steel flight stool (`Y = 0.47m`)** with a contoured charcoal cushion.

---

### Candidate 05: `walldesk_r1_05` — `#05 — Corner-Chamfered Cockpit Cabin Terminal & Pivoting Perch`
*Dimensions: `1.08m W × 0.68m D × 2.00m H`*

- **Color Palette (Hex Codes):**
  - 45° Angled Cockpit Bulkhead Enclosure: Gunmetal Titanium `#1A1E24` & Carbon Slate `#282E38`
  - Panoramic 3-Screen Array & Holo Combiner: `oled_cabin_terminal.png`, `oled_datapad_screen.png` & `glass_holo_hud_translucent.png`
  - Trapezoidal Fold-Down Desk & Turret Stool: Aerospace White `#D8DEE6`, Charcoal `#242932` & Signal Orange `#D95B26`
- **3D Geometry & Layout Brief for Rook:**
  - Build a **45°-chamfered cockpit-style wrap-around workstation (`1.08m W × 0.68m D × 2.00m H`)** with a **3-panel panoramic display array** (center widescreen `oled_cabin_terminal.png` flanked by two 30°-angled auxiliary `oled_datapad_screen.png` wing monitors) and an angled **translucent `glass_holo_hud_translucent.png` HUD combiner visor** mounted above the center screen.
  - Deploy a wide **trapezoidal aerospace-white fold-down desk leaf (`Y = 0.75m`)** on twin heavy hydraulic rams, equipped with a padded charcoal wrist bolster, recessed keyboard, docked data-slate, and magnetic mug, paired with a **heavy turret-mounted pivoting crew stool (`Y = 0.47m`)**.

---

## 4. Standardized Camera Framing & Lighting Guide (`Gage` & `Rook`)

1. **1080p Hero Framing (`/workspace/game-project/assets/renders/walldesk_round1/walldesk_r1_01.png` .. `walldesk_r1_05.png`):**
   - **Target Look-At Point:** `(0.0, 0.96, 0.05)` (centers on the deployed desk leaf, desktop props, recessed OLED terminal, and stool).
   - **Camera Angles:** 3/4 front-isometric beauty angle (`yaw = ±22° to ±26°`, `pitch = -15°`, distance `~2.40m – 2.60m`, `FOV = 46°`) so both the deployed horizontal desk surface (with the glowing data-pad, keyboard, and mug) AND the recessed OLED terminal + translucent Holo-HUD glass + swing-out stool are clearly visible without occlusion.
2. **3-Point + Practical Workstation Lighting Rig:**
   - **Key Light:** Pos `(2.0, 2.4, 2.4)`, Color `#E8F2FF`, Energy `1.30`.
   - **Fill Light:** Pos `(-2.0, 1.4, 2.0)`, Color `#78A8D8`, Energy `0.48`.
   - **Rim Light:** Pos `(0.0, 2.5, -1.5)`, Color `#00E5FF`, Energy `0.90`.
   - **Workstation Practicals:**
     1. `Downward_Desk_Task_Spot`: Local Pos `(0.0, 1.52, 0.18)`, Color `#E0F4FF` (surgical ice-white task light illuminating the desk leaf, mug & data-pad), Energy `1.55`, Range `1.9m`.
     2. `Terminal_Cyan_Glow`: Local Pos `(0.0, 1.22, -0.05)`, Color `#00E5FF`, Energy `1.45`, Range `2.0m`.
     3. `Under_Desk_Amber_Footlight`: Local Pos `(0.0, 0.32, 0.15)`, Color `#FF9500`, Energy `1.10`, Range `1.5m`.
3. **5-Panel Voting Comparison Sheet (`/workspace/game-project/assets/renders/walldesk_round1/walldesk_round1_voting_sheet.png`):**
   - Composite all 5 candidates (`#01` through `#05`) with clear title badges, dimensions, and triangle counts.
