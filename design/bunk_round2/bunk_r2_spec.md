# Sci-Fi Bunk Pod — Round 2 Hard Sci-Fi Design, Translucent Viewport & Lighting Specification
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Pipeline Stage:** Prop Variation Tournament — Round 2 of 4 (`bunk_r2_01` through `bunk_r2_10`) + Winner #1 Upgrade (`bunk_winner_01_orbital_viewport.glb`)  
**Art Direction:** **SLEEK HARD SCI-FI** (*Star Citizen* hab modules, *The Expanse*, *Alien: Isolation* aerospace pods, *2001* orbital crew bays)  
**Author:** Sloane (Interior, Lighting & Texture Designer)  
**Target Teams:** Rook (3D Hard-Surface & Organic Modeling, Translucent Cutouts & UVs) & Gage (Godot 4 Scene Integration, Exterior Vista Backdrops, Lighting & Beauty Renders)

---

## 1. Round 1 Winner #1 Upgrade Spec (`#06 — Orbital Viewport Pod`)

- **Target Output File:** `/workspace/game-project/assets/glb/winners/bunk_winner_01_orbital_viewport.glb`
- **Jared's Direct Mandate:** *"I love #6, if the window was translucent and could see out into space or the cylinder, depending on room location."*
- **Required 3D Geometry & Material Upgrade for Rook & Gage:**
  1. **True Open Back-Wall Viewport Cutout:** The rear bulkhead wall (`-Z`) of `#06 — Orbital Viewport Pod` MUST have a clean, open **octagonal/stadium geometry cutout** (`~1.50m wide × 0.85m tall`, centered at `Y = 1.28m, Z = -0.48m`) framed by a chamfered dark-titanium & brushed-steel pressure bezel (`steel_brushed_machined.png`). There must be **no opaque back-wall polygons blocking the sightline** through the window aperture.
  2. **True Alpha-Translucent Spacecraft Glass (`Mat_Viewport_Glass_Translucent`):**
     - **glTF 2.0 Material:** `alphaMode: "BLEND"`, `doubleSided: true`
     - **`baseColorFactor`:** `[0.08, 0.18, 0.25, 0.20]` (or `1.0, 1.0, 1.0, 0.85` multiplied with `glass_viewport_translucent.png` whose RGBA alpha channel is `~0.20`)
     - **`metallicFactor`:** `0.10`, **`roughnessFactor`:** `0.08` (crisp orbital specular reflection)
     - **`emissiveFactor`:** `[0.00, 0.12, 0.18]` (subtle cyan edge-refraction glow)
  3. **Switchable Exterior Backdrop Plane (`Z = -0.88m` to `-1.08m` behind the pod):**
     - In both the standalone beauty renders and the Godot 4 room/showcase scene, place an unshaded/emissive exterior vista plane (`3.6m × 2.4m`, `SHADING_MODE_UNSHADED` or `emissive_energy = 1.4`) at `Z = -0.95m` directly behind the pod's open viewport so the viewer looks straight through the tinted translucent glass into:
       - **Outer-Hull Room Location:** `/workspace/game-project/assets/textures/vista_deep_space.png` (deep space starfield, cyan/indigo nebula, and neighboring orbital ring).
       - **Inner-Hull Room Location:** `/workspace/game-project/assets/textures/vista_oneill_cylinder_interior.png` (the curving 800m × 400m O'Neill cylinder interior at orbital dusk with glowing city sectors and terraced biospheres).

---

## 2. Shared Hard Sci-Fi Standards & Technical Rules for Round 2 (`bunk_r2_01` .. `bunk_r2_10`)

### 2.1 Output Paths & Naming Convention
- **Round 2 3D Models (`.glb`):** `/workspace/game-project/assets/glb/bunk_round2/bunk_r2_01.glb` through `/workspace/game-project/assets/glb/bunk_round2/bunk_r2_10.glb`
- **Round 2 Texture Suite (`.png`):** `/workspace/game-project/assets/textures/bunk_round2/` (and shared vistas in `/workspace/game-project/assets/textures/`)
- **Individual Beauty Renders (`.png`):** `/workspace/game-project/assets/renders/bunk_round2/bunk_r2_01.png` through `bunk_r2_10.png`
- **10-Panel Round 2 Voting Sheet:** `/workspace/game-project/assets/renders/bunk_round2/bunk_round2_voting_sheet.png`

### 2.2 Footprint, Pivot, Polygon Budget & Hard Sci-Fi Design Language
- **Metric Scale & Footprint:** `1 unit = 1.0m`. Target envelope: `~2.15m–2.30m wide (X) × 1.15m–1.35m deep (Z) × 1.95m–2.30m tall (Y)`.
- **Origin & Orientation:** Bottom-center `(0, 0, 0)` resting on the `Y = 0` deck plane, open entry facing **`+Z`**, headboard/pillow zone at **`-X` (Left)**, foot end at **`+X` (Right)**.
- **Triangle Budget:** **`2,500 – 5,500 triangles`** per candidate.
- **Strict Hard Sci-Fi Rules:**
  - **ZERO wood, ZERO wallpaper, ZERO vintage upholstery, ZERO noisy 2D patterns (`<1.5%` micro-variation).**
  - **Every single candidate (`01` through `10`) MUST have an open geometry cutout and an alpha-translucent viewport window (`alphaMode: "BLEND"`, `alpha ~ 0.18–0.24`)** with a clear sightline to an exterior backdrop vista (`vista_deep_space.png` or `vista_oneill_cylinder_interior.png`) so the external stars or O'Neill cylinder lights are unmistakably visible through the glass in every render!
  - Combine **precision-chamfered aerospace hard surfaces** (multi-segment beveled titanium shells, machined steel gyro rings, hexagonal pressure bezels, recessed LED light channels) with **ergonomic contoured crew comfort** (sculpted memory-foam flight pads, bolster pillows, zero-G knee wedges, and technical quilted/neoprene sleep pads).

---

## 3. Texture & Material Library Manifest (`/workspace/game-project/assets/textures/bunk_round2/`)

All textures are `1024×1024` ultra-clean, low-noise (`<1.5%` tonal delta) PNGs stored in `/workspace/game-project/assets/textures/bunk_round2/` (with vistas and studio textures also in `/workspace/game-project/assets/textures/`).

| # | Filename | Format | Base Hex / Tone | Roughness | Metallic | Alpha / Emissive & Material Usage |
|---|----------|--------|-----------------|-----------|----------|-----------------------------------|
| 1 | `titanium_gunmetal_dark.png` | RGB | `#1A1E24` | `0.34` | `0.78` | Primary dark anodized gunmetal titanium pressure hull & outer pod enclosures |
| 2 | `composite_aerospace_white.png` | RGB | `#DCE2EA` | `0.30` | `0.08` | Smooth matte aerospace white molded composite interior liners & med/capsule shells |
| 3 | `carbon_slate_structural.png` | RGB | `#282E38` | `0.42` | `0.55` | Dark carbon-slate structural ribs, bulkhead frames, step sills & side lockers |
| 4 | `steel_brushed_machined.png` | RGB | `#88929E` | `0.24` | `0.88` | Machined brushed steel/chrome for viewport bezels, gyro rings, ladders & grab bars |
| 5 | `fabric_charcoal_flightpad.png` | RGB | `#252A32` | `0.78` | `0.00` | Contoured technical charcoal flight-couch & memory-foam mattress upholstery |
| 6 | `fabric_orbital_navy_pad.png` | RGB | `#1E2D3D` | `0.76` | `0.00` | Deep orbital navy zero-G sleep pad, quilt & acoustic alcove wall padding |
| 7 | `fabric_slate_grey_cushion.png` | RGB | `#4A5564` | `0.78` | `0.00` | Cool slate-grey ergonomic head bolsters, knee wedges & coverlet folds |
| 8 | `accent_signal_orange.png` | RGB | `#D95B26` | `0.50` | `0.05` | Matte aerospace signal-orange grab handles, restraint straps & emergency latches |
| 9 | `glass_viewport_translucent.png` | **RGBA** | `#0E2230` | `0.08` | `0.10` | **`alphaMode: "BLEND"`** (`alpha ~ 0.20`), smoked cyan-tinted spacecraft viewport glass with specular sheen |
| 10 | `glass_holo_visor_cyan.png` | **RGBA** | `#0E2230` + `#00E5FF` | `0.08` | `0.10` | **`alphaMode: "BLEND"`** (`alpha ~ 0.22`), translucent HUD/biomonitor visor glass with glowing cyan reticle |
| 11 | `oled_telemetry_hud.png` | RGB | `#0A0E14` + `#00E5FF` | `0.15` | `0.10` | **`emission_enabled: true`** (`energy = 2.0`), dark-glass OLED orbital & sleep telemetry display |
| 12 | `vista_deep_space.png` | RGB | `#060A14` + `#00E5FF` | `1.00` | `0.00` | **Unshaded / Emissive (`energy = 1.35`)** Outer-Hull Deep Space backdrop (stars, cyan/indigo nebula, orbital ring) |
| 13 | `vista_oneill_cylinder_interior.png` | RGB | `#103238` + `#00E5FF` | `1.00` | `0.00` | **Unshaded / Emissive (`energy = 1.35`)** Inner-Hull 800m × 400m O'Neill Cylinder dusk city & biosphere vista |

---

## 4. Detailed Per-Candidate Specifications (`bunk_r2_01` through `bunk_r2_10`)

> **Important Note on Translucent Sightlines for Rook & Gage:**  
> In every candidate below, the viewport glass submesh MUST use `alphaMode: "BLEND"` (`alpha = 0.18–0.24`) with `glass_viewport_translucent.png` (or `glass_holo_visor_cyan.png`), and the pod's rear/upper shell MUST have a true geometric cutout behind the glass. Include a curved or planar exterior vista backdrop quad (`Z = -0.82m` to `-1.02m` behind the window, or directly outside the blister/skylight) mapped with the specified vista texture (`vista_deep_space.png` or `vista_oneill_cylinder_interior.png`, emissive `(0.85, 0.92, 1.0)`) so both software and Godot renders display the stars or O'Neill cylinder clearly through the translucent window!

---

### Candidate 01: `bunk_r2_01` (`01_panoramic_hull_blister_pod`) — Curved Bubble-Glass Hull Blister Berth
*Chamfered dark-titanium sleep bay whose entire rear and upper vault is a ribbed translucent armored-glass observation blister looking out into Deep Space.*

- **Assigned Exterior Vista:** `vista_deep_space.png` (Outer-Hull Deep Space Starfield, Cyan/Violet Nebula & Orbital Ring)
- **Color Palette (Hex Codes):**
  - Outer Chamfered Enclosure: Dark Gunmetal Titanium `#1A1E24`
  - Blister Ribs & Bezel Frame: Machined Brushed Steel `#88929E`
  - Contoured Flight Mattress & Bolsters: Charcoal Flightpad `#252A32` & Slate Grey `#4A5564`
  - Grab Bars & Emergency Release: Signal Orange `#D95B26`
  - Practical LED Accents: Orbital Cyan `#00E5FF` & Ice White `#E0F4FF`
- **Surface Material Assignments:**
  - `Outer_Hull_Chassis`: `titanium_gunmetal_dark.png` (`roughness: 0.34`, `metallic: 0.78`)
  - `Blister_Arch_Ribs` & `Entry_Sill_Bezel`: `steel_brushed_machined.png` (`roughness: 0.24`, `metallic: 0.88`)
  - `Curved_Blister_Viewport_Glass`: `glass_viewport_translucent.png` (`alphaMode: "BLEND"`, `baseColorFactor: [1.0, 1.0, 1.0, 0.22]`, `roughness: 0.08`, `metallic: 0.10`)
  - `Exterior_Space_Backdrop_Curve`: `vista_deep_space.png` (`emissive: [0.90, 0.95, 1.0]`)
  - `Contoured_Flight_Mattress`: `fabric_charcoal_flightpad.png` (`roughness: 0.78`)
  - `Sculpted_Head_And_Knee_Bolsters` & `Draped_Tech_Quilt`: `fabric_slate_grey_cushion.png` & `fabric_orbital_navy_pad.png`
  - `Side_OLED_Console`: `oled_telemetry_hud.png` (`emissive: [0.25, 0.85, 1.0]`)
- **3D Geometry & Translucent Cutout Brief for Rook:**
  - Build a chamfered dark-titanium lower berth (`Y = 0.0m–0.52m`) and side bulkheads (`X = ±1.06m`), leaving the **entire rear wall (`Z = -0.45m`) from `Y = 0.55m` up to the curved roof (`Y = 1.95m`) completely open**.
  - Span that open vault with a **sweeping quarter-cylinder curved translucent glass blister** reinforced by **3 curved machined-steel structural ribs** (`X = -0.52m, 0.0m, +0.52m`).
  - Place a slightly larger curved backdrop panel at `Z = -0.82m` mapped with `vista_deep_space.png` so the nebula and orbital ring shine through all four glass bays.
  - Sculpt an ergonomic multi-segment flight couch mattress with raised side bolsters, pinched head pillow (`-X`), knee elevation contour, and a draped navy technical coverlet.
- **3-Point + Practical Lighting Rig:**
  - **Key:** Pos `(2.2, 2.5, 2.6)`, Color `#DCEEFF` (cool crisp starlight/cabin key), Energy `1.25`.
  - **Fill:** Pos `(-2.4, 1.4, 2.2)`, Color `#78A8D8`, Energy `0.45`.
  - **Rim:** Pos `(0.0, 2.6, -1.6)`, Color `#00E5FF`, Energy `0.95`.
  - **Practicals:**
    1. `Cyan_Perimeter_Strip`: Local Pos `(0.0, 1.82, -0.18)`, Color `#00E5FF`, Energy `1.55`, Range `2.4m`.
    2. `Reading_Spot_Ice`: Local Pos `(-0.82, 1.25, -0.22)`, Color `#E0F4FF`, Energy `1.20`, Range `1.8m`.

---

### Candidate 02: `bunk_r2_02` (`02_hex_aperture_sleep_chamber`) — Deep Hexagonal Aperture Pod
*Asymmetric elongated hex-bevel composite hull in matte carbon-slate & aerospace white with a large hexagonal rear translucent viewport and an internal translucent glass head-end partition.*

- **Assigned Exterior Vista:** `vista_oneill_cylinder_interior.png` (Inner-Hull 800m × 400m O'Neill Cylinder Dusk City & Terraced Biospheres)
- **Color Palette (Hex Codes):**
  - Outer Hex Bevel Frame: Carbon Slate `#282E38` & Gunmetal `#1A1E24`
  - Inner Molded Chamber Shell: Matte Aerospace White `#DCE2EA`
  - Bedding & Acoustic Pads: Orbital Navy `#1E2D3D` & Slate Grey `#4A5564`
  - Dual Cove Lighting: Warm Amber `#FF9500` & Cyan `#00E5FF`
- **Surface Material Assignments:**
  - `Outer_Hex_Collar` & `Stepped_Entry_Sill`: `carbon_slate_structural.png` (`roughness: 0.40`, `metallic: 0.58`)
  - `Inner_Chamfered_Shell`: `composite_aerospace_white.png` (`roughness: 0.30`, `metallic: 0.08`)
  - `Rear_Hex_Viewport_Glass` & `Head_Partition_Glass`: `glass_viewport_translucent.png` (`alphaMode: "BLEND"`, `alpha: 0.20`)
  - `Exterior_Cylinder_Backdrop`: `vista_oneill_cylinder_interior.png` (`emissive: [0.88, 0.96, 0.94]`)
  - `Mattress_And_Quilt`: `fabric_orbital_navy_pad.png` & `fabric_slate_grey_cushion.png`
  - `Telemetry_Panel`: `oled_telemetry_hud.png`
- **3D Geometry & Translucent Cutout Brief for Rook:**
  - Construct a striking **elongated hexagonal aperture tunnel** (`2.22m wide × 1.28m deep × 2.05m tall`) with 45° chamfered upper/lower corners and a stepped machined entry sill at `Z = +0.58m`.
  - Cut a **wide hexagonal panoramic viewport (`1.45m × 0.82m`)** straight through the rear wall (`Z = -0.50m`) fitted with `glass_viewport_translucent.png` looking out onto `vista_oneill_cylinder_interior.png` at `Z = -0.85m`.
  - Add a sleek **half-width translucent smoked-glass draft shield / head partition** (`X = -0.68m, Z = +0.42m`) with glowing cyan bevel edges.
- **3-Point + Practical Lighting Rig:**
  - **Key:** Pos `(2.3, 2.6, 2.5)`, Color `#E8F2FF`, Energy `1.30`.
  - **Fill:** Pos `(-2.3, 1.5, 2.1)`, Color `#82B4C8`, Energy `0.48`.
  - **Rim:** Pos `(1.6, 2.5, -1.6)`, Color `#00E5FF`, Energy `0.90`.
  - **Practicals:**
    1. `Upper_Cyan_Hex_Cove`: Local Pos `(0.0, 1.78, 0.10)`, Color `#00E5FF`, Energy `1.45`, Range `2.2m`.
    2. `Lower_Amber_Step_Cove`: Local Pos `(0.0, 0.24, 0.52)`, Color `#FF9500`, Energy `1.25`, Range `1.6m`.

---

### Candidate 03: `bunk_r2_03` (`03_corvette_submarine_rack`) — Torpedo-Bay Style Recessed Rack
*Sleek MCRN / Expanse naval space-corvette berth with curved titanium rib arches, fold-down technical privacy baffle, integrated side gear lockers, and a long horizontal translucent hull slit viewport.*

- **Assigned Exterior Vista:** `vista_deep_space.png` (Outer-Hull Deep Space Starfield & Orbital Ring)
- **Color Palette (Hex Codes):**
  - Ribbed Hull Structure & Lockers: Dark Gunmetal Titanium `#1A1E24` & Carbon Slate `#282E38`
  - Machined Rib Flanges & Grab Rails: Brushed Steel `#88929E`
  - Flight Berth Bedding: Charcoal Flightpad `#252A32` & Signal Orange Straps `#D95B26`
  - Practical Accents: Tactical Amber `#FF9500` & Cyan `#00E5FF`
- **Surface Material Assignments:**
  - `Corvette_Hull_Bay` & `Side_Gear_Lockers`: `titanium_gunmetal_dark.png` & `carbon_slate_structural.png`
  - `Curved_Rib_Arches` & `Grab_Handles`: `steel_brushed_machined.png`
  - `Horizontal_Hull_Slit_Viewport`: `glass_viewport_translucent.png` (`alphaMode: "BLEND"`, `alpha: 0.20`)
  - `Exterior_Space_Backdrop`: `vista_deep_space.png` (`emissive: [0.90, 0.95, 1.0]`)
  - `Mattress_And_Fold_Down_Baffle`: `fabric_charcoal_flightpad.png` & `fabric_slate_grey_cushion.png`
  - `Tactical_Latches_And_Straps`: `accent_signal_orange.png`
  - `Rack_Telemetry_Unit`: `oled_telemetry_hud.png`
- **3D Geometry & Translucent Cutout Brief for Rook:**
  - Frame the recessed berth with **four heavy chamfered C-profile titanium rib arches** (`X = -1.05m, -0.35m, +0.35m, +1.05m`) and compact vertical tactical gear lockers on the far right (`+X`).
  - Cut a **long, sleek chamfered horizontal armour-glass slit viewport (`1.55m wide × 0.52m tall`, `Y = 1.05m–1.57m`)** right through the rear hull wall (`Z = -0.48m`) with `glass_viewport_translucent.png` and `vista_deep_space.png` behind it.
  - Model an **angled fold-down upper technical baffle/visor** along the top front edge (`Y = 1.68m`) and signal-orange grab handles.
- **3-Point + Practical Lighting Rig:**
  - **Key:** Pos `(2.2, 2.5, 2.6)`, Color `#E4F0FF`, Energy `1.28`.
  - **Fill:** Pos `(-2.4, 1.4, 2.0)`, Color `#7094B8`, Energy `0.42`.
  - **Rim:** Pos `(-1.8, 2.6, -1.5)`, Color `#FF9500`, Energy `0.90`.
  - **Practicals:**
    1. `Tactical_Amber_Baffle_Strip`: Local Pos `(-0.15, 1.62, 0.22)`, Color `#FF9500`, Energy `1.50`, Range `2.1m`.
    2. `Viewport_Cyan_Rim`: Local Pos `(0.0, 1.30, -0.42)`, Color `#00E5FF`, Energy `1.15`, Range `1.8m`.

---

### Candidate 04: `bunk_r2_04` (`04_sliding_canopy_cockpit_pod`) — Fighter-Canopy Gullwing Sleep Pod
*Contoured aerospace sleep pod with a multi-pane framed translucent smoked-glass gullwing canopy hinged open at 35° plus a rear panoramic viewport.*

- **Assigned Exterior Vista:** `vista_deep_space.png` (Outer-Hull Deep Space Starfield & Nebula)
- **Color Palette (Hex Codes):**
  - Lower Monocoque Pod Tub: Matte Aerospace White `#DCE2EA` & Carbon Slate Base `#282E38`
  - Gullwing Canopy Frame: Gunmetal Titanium `#1A1E24` & Brushed Steel Struts `#88929E`
  - Zero-G Contoured Pad: Deep Orbital Navy `#1E2D3D` & Signal Orange Piping `#D95B26`
  - Canopy HUD Glass: Translucent Cyan Holo-Visor `#00E5FF`
- **Surface Material Assignments:**
  - `Lower_Aerospace_Tub`: `composite_aerospace_white.png`
  - `Chassis_Skirt_And_Canopy_Frame`: `titanium_gunmetal_dark.png` & `carbon_slate_structural.png`
  - `Hydraulic_Canopy_Struts`: `steel_brushed_machined.png`
  - `Gullwing_Canopy_Panes`: `glass_holo_visor_cyan.png` (`alphaMode: "BLEND"`, `alpha: 0.22`)
  - `Rear_Cockpit_Viewport`: `glass_viewport_translucent.png` (`alphaMode: "BLEND"`, `alpha: 0.20`)
  - `Exterior_Space_Backdrop`: `vista_deep_space.png` (`emissive: [0.90, 0.95, 1.0]`)
  - `Sculpted_ZeroG_Navy_Couch`: `fabric_orbital_navy_pad.png` & `fabric_slate_grey_cushion.png`
- **3D Geometry & Translucent Cutout Brief for Rook:**
  - Sculpt a sleek, sloped **fighter-cockpit monocoque sleep tub** (`2.20m × 1.22m`) with chamfered intake-like side fairings and an open rear bulkhead window (`1.50m × 0.80m`) looking out at `vista_deep_space.png`.
  - Above the pod (`Y = 1.28m–1.98m`), model a **3-pane framed gullwing cockpit canopy** raised on twin brushed-steel pneumatic struts so the viewer sees both through the translucent cyan HUD canopy glass (`glass_holo_visor_cyan.png`) AND directly into the sculpted navy flight pad below.
- **3-Point + Practical Lighting Rig:**
  - **Key:** Pos `(2.3, 2.6, 2.5)`, Color `#E6F2FF`, Energy `1.32`.
  - **Fill:** Pos `(-2.3, 1.5, 2.2)`, Color `#7CA8D8`, Energy `0.46`.
  - **Rim:** Pos `(1.7, 2.6, -1.6)`, Color `#00E5FF`, Energy `0.95`.
  - **Practicals:**
    1. `Canopy_HUD_Cyan_Glow`: Local Pos `(0.0, 1.55, 0.15)`, Color `#00E5FF`, Energy `1.55`, Range `2.2m`.
    2. `Cockpit_Footwell_Amber`: Local Pos `(0.65, 0.72, -0.15)`, Color `#FF9500`, Energy `0.95`, Range `1.4m`.

---

### Candidate 05: `bunk_r2_05` (`05_corner_l_viewport_berth`) — Dual-Window Corner Observation Bunk
*Wrap-around L-shaped chamfered titanium sleep alcove with TWO translucent beveled viewports (rear wall + left side bulkhead) for corner hull cabins.*

- **Assigned Exterior Vista:** `vista_oneill_cylinder_interior.png` (Inner-Hull 800m × 400m O'Neill Cylinder Interior on both Rear & Left Vista Planes)
- **Color Palette (Hex Codes):**
  - L-Shaped Corner Bulkhead: Gunmetal Titanium `#1A1E24` & Carbon Slate `#282E38`
  - Dual Viewport Bezels: Brushed Machined Steel `#88929E`
  - Corner Lounge Mattress & Bolsters: Slate Grey `#4A5564` & Charcoal `#252A32`
  - Practical LED Strips: Cool Cyan `#00E5FF`
- **Surface Material Assignments:**
  - `L_Corner_Titanium_Enclosure`: `titanium_gunmetal_dark.png` & `carbon_slate_structural.png`
  - `Dual_Beveled_Viewport_Frames`: `steel_brushed_machined.png`
  - `Rear_And_Side_Viewport_Glass`: `glass_viewport_translucent.png` (`alphaMode: "BLEND"`, `alpha: 0.20`)
  - `Dual_L_Exterior_Vista_Planes`: `vista_oneill_cylinder_interior.png` (`emissive: [0.88, 0.96, 0.94]`)
  - `Corner_Bedding_And_Wrap_Bolsters`: `fabric_slate_grey_cushion.png` & `fabric_charcoal_flightpad.png`
  - `Corner_OLED_Monitor`: `oled_telemetry_hud.png`
- **3D Geometry & Translucent Cutout Brief for Rook:**
  - Build an asymmetric **L-shaped corner observation alcove** where the rear wall (`Z = -0.50m`) and the left head-end wall (`X = -1.05m`) meet at a chamfered 45° corner pillar, while the right foot-end (`+X`) is open/low-profile for panoramic viewing (`cam_yaw_deg = 24°` looks directly into both the `-Z` rear window and `-X` side window!).
  - Cut **two large chamfered panoramic viewports**:
    1. Rear window (`1.35m wide × 0.82m tall` at `Z = -0.48m`)
    2. Left head-wall window (`0.82m deep × 0.82m tall` at `X = -1.02m`)
  - Place L-shaped exterior vista planes behind both windows (`Z = -0.82m` and `X = -1.28m`) mapped with `vista_oneill_cylinder_interior.png`.
- **3-Point + Practical Lighting Rig:**
  - **Key:** Pos `(2.4, 2.5, 2.5)`, Color `#E8F4FF`, Energy `1.30`.
  - **Fill:** Pos `(-2.2, 1.5, 2.3)`, Color `#7EB8C8`, Energy `0.48`.
  - **Rim:** Pos `(-1.8, 2.5, -1.6)`, Color `#00E5FF`, Energy `0.95`.
  - **Practicals:**
    1. `Corner_Cyan_Edge_Strip`: Local Pos `(-0.35, 1.76, -0.25)`, Color `#00E5FF`, Energy `1.55`, Range `2.4m`.
    2. `Headboard_Reading_Spot`: Local Pos `(-0.78, 1.15, 0.18)`, Color `#E0F4FF`, Energy `1.20`, Range `1.7m`.

---

### Candidate 06: `bunk_r2_06` (`06_suspended_gyro_cradle`) — Gimbaled Centrifuge Sleep Cradle
*Sleek cylindrical sleep pod suspended inside twin machined steel/titanium gyro rings that auto-level during habitat spin-down, featuring a translucent upper/rear viewing canopy.*

- **Assigned Exterior Vista:** `vista_deep_space.png` (Outer-Hull Deep Space Starfield & Orbital Ring)
- **Color Palette (Hex Codes):**
  - Twin Machined Gyro Rings & Trunnion Mounts: Brushed Steel `#88929E` & Gunmetal `#1A1E24`
  - Suspended Pod Cradle Shell: Matte Aerospace White `#DCE2EA`
  - Contoured Zero-G Cradle Pad: Orbital Navy `#1E2D3D` & Charcoal `#252A32`
  - Gimbal Lock Accents: Signal Orange `#D95B26`
  - Practical Ring Glow: Cyan `#00E5FF` & Amber `#FF9500`
- **Surface Material Assignments:**
  - `Twin_Gimbal_Gyro_Rings` & `Pivot_Trunnions`: `steel_brushed_machined.png` (`roughness: 0.22`, `metallic: 0.90`)
  - `Base_Support_Cradle_Stands`: `titanium_gunmetal_dark.png` & `carbon_slate_structural.png`
  - `Suspended_Cylindrical_Pod_Shell`: `composite_aerospace_white.png`
  - `Curved_Upper_Rear_Canopy_Glass`: `glass_viewport_translucent.png` (`alphaMode: "BLEND"`, `alpha: 0.20`)
  - `Exterior_Space_Backdrop`: `vista_deep_space.png` (`emissive: [0.90, 0.95, 1.0]`)
  - `Ergonomic_Cradle_Mattress`: `fabric_orbital_navy_pad.png` & `fabric_slate_grey_cushion.png`
  - `Gimbal_Telemetry_Hub`: `oled_telemetry_hud.png`
- **3D Geometry & Translucent Cutout Brief for Rook:**
  - Model **two large precision-machined circular/octagonal gyro rings** (`R = 0.96m`, at `X = -0.78m` and `X = +0.78m`) mounted on heavy chamfered floor pedestals (`Y = 0.0m–0.35m`), suspending a sleek cylindrical sleep capsule (`Y = 0.38m–1.75m`) floating off the floor.
  - Leave the **rear and upper arc of the cylindrical capsule cut open** and glazed with curved `glass_viewport_translucent.png` panels between the gyro rings, looking out onto a wide rear `vista_deep_space.png` backdrop plane.
- **3-Point + Practical Lighting Rig:**
  - **Key:** Pos `(2.3, 2.6, 2.6)`, Color `#E8F2FF`, Energy `1.32`.
  - **Fill:** Pos `(-2.4, 1.5, 2.1)`, Color `#78A4D0`, Energy `0.46`.
  - **Rim:** Pos `(0.0, 2.7, -1.7)`, Color `#00E5FF`, Energy `0.95`.
  - **Practicals:**
    1. `Gyro_Ring_Cyan_Accent`: Local Pos `(0.0, 1.65, -0.15)`, Color `#00E5FF`, Energy `1.50`, Range `2.3m`.
    2. `Under_Cradle_Amber_Glow`: Local Pos `(0.0, 0.22, 0.10)`, Color `#FF9500`, Energy `1.10`, Range `1.6m`.

---

### Candidate 07: `bunk_r2_07` (`07_medical_biomonitor_pod`) — High-Tech Med/Cryo Diagnostic Berth
*Clean aerospace white-and-gunmetal diagnostic sleep bay with an arched translucent holographic vitals visor over the pillow zone, biometric sensor rails, and a rear translucent observation window.*

- **Assigned Exterior Vista:** `vista_deep_space.png` (Outer-Hull Deep Space Starfield & Cyan Nebula)
- **Color Palette (Hex Codes):**
  - Clean-Room Med Bay Shell: Matte Aerospace White `#DCE2EA`
  - Structural Frame & Diagnostic Arch: Gunmetal Titanium `#1A1E24` & Brushed Steel `#88929E`
  - Biometric Sleep Pad: Slate Grey `#4A5564` & Charcoal `#252A32`
  - Holographic Visor & Sensor Glow: Ice-Cyan `#00E5FF` & Diagnostic White `#E0F4FF`
- **Surface Material Assignments:**
  - `Med_Bay_White_Shell`: `composite_aerospace_white.png` (`roughness: 0.28`, `metallic: 0.08`)
  - `Diagnostic_Scanner_Arch` & `Lower_Instrument_Drawer`: `titanium_gunmetal_dark.png` & `steel_brushed_machined.png`
  - `Holographic_Vitals_Visor`: `glass_holo_visor_cyan.png` (`alphaMode: "BLEND"`, `alpha: 0.22`)
  - `Rear_Observation_Viewport`: `glass_viewport_translucent.png` (`alphaMode: "BLEND"`, `alpha: 0.20`)
  - `Exterior_Space_Backdrop`: `vista_deep_space.png` (`emissive: [0.90, 0.95, 1.0]`)
  - `Contoured_Biometric_Mattress`: `fabric_slate_grey_cushion.png` & `fabric_charcoal_flightpad.png`
  - `Dual_Biomonitor_Screens`: `oled_telemetry_hud.png` (`emissive: [0.30, 0.90, 1.0]`)
- **3D Geometry & Translucent Cutout Brief for Rook:**
  - Sculpt a pristine aerospace white sleep bay with a **pivoting arched diagnostic scanner ring (`X = -0.45m`)** supporting a **curved translucent cyan holographic vitals visor (`glass_holo_visor_cyan.png`)** over the head/chest zone (`X = -0.95m` to `-0.25m, Y = 0.85m–1.42m`).
  - Cut a **wide stadium-beveled translucent window (`1.45m × 0.78m`)** through the rear wall (`Z = -0.48m`) with `glass_viewport_translucent.png` looking out onto `vista_deep_space.png`.
- **3-Point + Practical Lighting Rig:**
  - **Key:** Pos `(2.2, 2.6, 2.6)`, Color `#EAF6FF`, Energy `1.35`.
  - **Fill:** Pos `(-2.3, 1.5, 2.2)`, Color `#88C4E8`, Energy `0.50`.
  - **Rim:** Pos `(-1.6, 2.6, -1.6)`, Color `#00E5FF`, Energy `0.95`.
  - **Practicals:**
    1. `Holo_Visor_Ice_Cyan`: Local Pos `(-0.55, 1.22, 0.05)`, Color `#00E5FF`, Energy `1.65`, Range `2.2m`.
    2. `Surgical_Cove_White`: Local Pos `(0.25, 1.75, -0.15)`, Color `#E0F4FF`, Energy `1.35`, Range `2.2m`.

---

### Candidate 08: `bunk_r2_08` (`08_modular_hex_hive_stack`) — Twin Offset Honeycomb Crew Pods
*Two interlocking hexagonal sleep tubes stacked at an offset with integrated machined step-rungs, chamfered alloy bezels, and translucent rear hexagonal viewport portholes at the back of EACH tube.*

- **Assigned Exterior Vista:** `vista_oneill_cylinder_interior.png` (Inner-Hull 800m × 400m O'Neill Cylinder Dusk City & Biospheres)
- **Color Palette (Hex Codes):**
  - Outer Honeycomb Structural Tubes: Gunmetal Titanium `#1A1E24` & Carbon Slate `#282E38`
  - Hex Entry Bezels & Step Rungs: Machined Steel `#88929E` & Aerospace White Inner Liner `#DCE2EA`
  - Lower & Upper Pod Bedding: Orbital Navy `#1E2D3D` & Charcoal `#252A32`
  - Dual Pod Lighting: Lower Amber `#FF9500` + Upper Cyan `#00E5FF`
- **Surface Material Assignments:**
  - `Hex_Outer_Tubes`: `titanium_gunmetal_dark.png` & `carbon_slate_structural.png`
  - `Inner_Tube_Walls`: `composite_aerospace_white.png`
  - `Hex_Entry_Bezels` & `Integrated_Step_Rungs`: `steel_brushed_machined.png`
  - `Upper_And_Lower_Rear_Hex_Viewports`: `glass_viewport_translucent.png` (`alphaMode: "BLEND"`, `alpha: 0.20`)
  - `Exterior_Cylinder_Backdrop`: `vista_oneill_cylinder_interior.png` (`emissive: [0.88, 0.96, 0.94]`)
  - `Crew_Mattresses_And_Bolsters`: `fabric_orbital_navy_pad.png` & `fabric_charcoal_flightpad.png`
  - `Safety_Handholds`: `accent_signal_orange.png`
- **3D Geometry & Translucent Cutout Brief for Rook:**
  - Construct **two interlocking hexagonal crew sleep pods (`2.25m total width × 1.28m depth × 2.25m total height`)**:
    - **Lower Hex Pod (`Y = 0.0m–1.15m`, shifted slightly `-X`)**
    - **Upper Hex Pod (`Y = 1.08m–2.24m`, shifted slightly `+X`)** with cantilevered machined steel access rungs climbing the right/center hexagon bevel.
  - **Cut open the rear hexagonal backwall (`Z = -0.48m`) of BOTH the lower and upper pods**, fitting each with a large hexagonal translucent glass window (`glass_viewport_translucent.png`) looking out onto `vista_oneill_cylinder_interior.png` (`Z = -0.85m`).
- **3-Point + Practical Lighting Rig:**
  - **Key:** Pos `(2.4, 2.7, 2.6)`, Color `#E8F2FF`, Energy `1.32`.
  - **Fill:** Pos `(-2.4, 1.5, 2.2)`, Color `#7EB0C8`, Energy `0.48`.
  - **Rim:** Pos `(1.8, 2.7, -1.6)`, Color `#00E5FF`, Energy `0.90`.
  - **Practicals:**
    1. `Upper_Hex_Cyan_Light`: Local Pos `(0.15, 1.98, -0.10)`, Color `#00E5FF`, Energy `1.45`, Range `2.0m`.
    2. `Lower_Hex_Amber_Light`: Local Pos `(-0.15, 0.92, -0.10)`, Color `#FF9500`, Energy `1.45`, Range `2.0m`.

---

### Candidate 09: `bunk_r2_09` (`09_observation_lounge_sleeper`) — Split-Level Daybed & Stargazer Pod
*Lower contoured sleep berth + raised angled stargazer headrest reclined directly beneath a huge slanted overhead & rear translucent skylight viewport framed in brushed steel and amber status LEDs.*

- **Assigned Exterior Vista:** `vista_deep_space.png` (Outer-Hull Deep Space Starfield, Cyan Nebula & Orbital Ring)
- **Color Palette (Hex Codes):**
  - Split-Level Chassis & Recliner Frame: Carbon Slate `#282E38` & Gunmetal Titanium `#1A1E24`
  - Slanted Skylight Frame: Brushed Machined Steel `#88929E`
  - Reclined Stargazer Daybed & Bolsters: Slate Grey `#4A5564` & Orbital Navy `#1E2D3D`
  - Practical LED Accents: Warm Amber Status `#FF9500` & Stargazer Cyan `#00E5FF`
- **Surface Material Assignments:**
  - `Split_Level_Deck_And_Sidewalls`: `titanium_gunmetal_dark.png` & `carbon_slate_structural.png`
  - `Slanted_Skylight_Mullions`: `steel_brushed_machined.png`
  - `Overhead_And_Rear_Skylight_Glass`: `glass_viewport_translucent.png` (`alphaMode: "BLEND"`, `alpha: 0.20`)
  - `Exterior_Space_Backdrop`: `vista_deep_space.png` (`emissive: [0.90, 0.95, 1.0]`)
  - `Reclined_Stargazer_Mattress_And_Lounger`: `fabric_slate_grey_cushion.png` & `fabric_orbital_navy_pad.png`
  - `Side_Armrest_OLED`: `oled_telemetry_hud.png`
- **3D Geometry & Translucent Cutout Brief for Rook:**
  - Sculpt a **split-level observation daybed** where the left third (`X = -1.02m` to `-0.25m`) rises into a **35° reclined stargazer lounge backrest** with a sculpted neck bolster, transitioning smoothly into the horizontal sleep deck (`X = -0.25m` to `+1.02m`).
  - Above and behind the berth (`Z = -0.50m, Y = 0.85m` curving/slanting forward to `Z = +0.15m, Y = 2.02m`), cut a **massive 2-panel slanted stargazer skylight & rear viewport** glazed with `glass_viewport_translucent.png` and backed by an angled `vista_deep_space.png` skyplane so the stars and nebula dominate the view.
- **3-Point + Practical Lighting Rig:**
  - **Key:** Pos `(2.2, 2.6, 2.5)`, Color `#E8F4FF`, Energy `1.30`.
  - **Fill:** Pos `(-2.3, 1.5, 2.2)`, Color `#78A8D8`, Energy `0.46`.
  - **Rim:** Pos `(0.0, 2.7, -1.6)`, Color `#00E5FF`, Energy `0.95`.
  - **Practicals:**
    1. `Skylight_Amber_Status_Strip`: Local Pos `(0.0, 1.88, -0.05)`, Color `#FF9500`, Energy `1.45`, Range `2.2m`.
    2. `Under_Lounger_Cyan_Strip`: Local Pos `(-0.45, 0.20, 0.48)`, Color `#00E5FF`, Energy `1.20`, Range `1.7m`.

---

### Candidate 10: `bunk_r2_10` (`10_captain_bridge_alcove`) — Command Deck Observation Berth
*Wide chamfered dark-gunmetal stateroom pod with a dramatic 3-panel trapezoidal translucent bridge-style window across the back wall, twin cantilevered side consoles, and dual cyan/amber cove lighting.*

- **Assigned Exterior Vista:** `vista_oneill_cylinder_interior.png` (Inner-Hull 800m × 400m O'Neill Cylinder Dusk City & Terraced Biospheres)
- **Color Palette (Hex Codes):**
  - Monumental Bridge Alcove Hull: Dark Gunmetal Titanium `#1A1E24`
  - Trapezoidal Bridge Window Mullions & Consoles: Brushed Machined Steel `#88929E` & Carbon Slate `#282E38`
  - Command Stateroom Bedding: Charcoal Flightpad `#252A32`, Orbital Navy `#1E2D3D` & Slate Grey `#4A5564`
  - Dual Cove Lighting: Command Cyan `#00E5FF` & Warm Amber `#FF9500`
- **Surface Material Assignments:**
  - `Chamfered_Bridge_Alcove_Shell`: `titanium_gunmetal_dark.png` (`roughness: 0.32`, `metallic: 0.80`)
  - `Trapezoidal_Bridge_Mullions` & `Console_Trim`: `steel_brushed_machined.png` (`roughness: 0.22`, `metallic: 0.90`)
  - `Cantilevered_Side_Consoles`: `carbon_slate_structural.png`
  - `Three_Panel_Bridge_Viewport_Glass`: `glass_viewport_translucent.png` (`alphaMode: "BLEND"`, `alpha: 0.20`)
  - `Exterior_Cylinder_Backdrop`: `vista_oneill_cylinder_interior.png` (`emissive: [0.88, 0.96, 0.94]`)
  - `Layered_Stateroom_Flight_Mattress`: `fabric_charcoal_flightpad.png`, `fabric_orbital_navy_pad.png` & `fabric_slate_grey_cushion.png`
  - `Twin_Wing_OLED_Displays`: `oled_telemetry_hud.png` (`emissive: [0.25, 0.85, 1.0]`)
- **3D Geometry & Translucent Cutout Brief for Rook:**
  - Build a wide, authoritative **spacecraft bridge-style chamfered gunmetal alcove** (`2.28m wide × 1.32m deep × 2.18m tall`) with angled inner side wings housing **twin cantilevered OLED command consoles**.
  - Across the entire rear bulkhead (`Z = -0.50m, Y = 0.88m–1.78m`), cut a **dramatic 3-pane trapezoidal bridge observation window** (wide center trapezoid flanked by two angled wing panes separated by forward-raked brushed-steel mullions) glazed with `glass_viewport_translucent.png` and backed by `vista_oneill_cylinder_interior.png` at `Z = -0.88m`.
  - Dress the raised titanium bed deck with a thick contoured charcoal mattress, four tiered slate/navy pillows, and a tailored navy coverlet with crisp chamfered folds.
- **3-Point + Practical Lighting Rig:**
  - **Key:** Pos `(2.3, 2.7, 2.6)`, Color `#E8F2FF`, Energy `1.32`.
  - **Fill:** Pos `(-2.4, 1.5, 2.2)`, Color `#7CB0CC`, Energy `0.48`.
  - **Rim:** Pos `(0.0, 2.8, -1.7)`, Color `#00E5FF`, Energy `0.95`.
  - **Practicals:**
    1. `Bridge_Crown_Cyan_Cove`: Local Pos `(0.0, 1.88, -0.22)`, Color `#00E5FF`, Energy `1.60`, Range `2.5m`.
    2. `Pedestal_Amber_Cove`: Local Pos `(0.0, 0.22, 0.52)`, Color `#FF9500`, Energy `1.35`, Range `1.9m`.

---

## 5. Render & Voting Sheet Framing Guide for Round 2 (`Gage` & `Rook`)

1. **Translucent Glass & Exterior Vista Rendering Requirement:**
   - Both the Python SSAA rasterizer and the Godot 4 OpenGL3 renderer MUST render **opaque geometry first**, and then alpha-blend (`alphaMode == "BLEND"`) the translucent glass triangles (`alpha ~ 0.20` + specular highlight) over the emissive exterior vista backdrop (`vista_deep_space.png` or `vista_oneill_cylinder_interior.png`) so every single render clearly shows the deep-space nebula/stars or O'Neill cylinder city lights shining through the tinted window!
2. **Dark Hard Sci-Fi Studio Environment:**
   - Studio floor and backwall use the updated dark gunmetal/composite textures (`#14181F` deck and `#1C2128` bulkhead) so there is zero retro wood or warm plaster anywhere in the frame.
3. **Output Files:**
   - Individual renders: `/workspace/game-project/assets/renders/bunk_round2/bunk_r2_01.png` .. `bunk_r2_10.png`
   - 5×2 Voting Sheet: `/workspace/game-project/assets/renders/bunk_round2/bunk_round2_voting_sheet.png`
   - Upgraded Winner #1 model: `/workspace/game-project/assets/glb/winners/bunk_winner_01_orbital_viewport.glb`
