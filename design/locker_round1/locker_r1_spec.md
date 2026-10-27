# EVA Suit & Personal Gear Locker — Round 1 Design, 3D Interior Layout, Translucent Glass & Lighting Specification
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Pipeline Stage:** Non-Bunk Sleeping Quarters Fixture #1 — 5-Choice Test (`locker_r1_01` through `locker_r1_05`)  
**Art Direction:** **SLEEK HARD SCI-FI** (*Star Citizen* hab modules, *The Expanse*, *Alien: Isolation* aerospace pods, *2001* orbital crew bays)  
**Author:** Sloane (Interior, Lighting & Texture Designer)  
**Target Teams:** Rook (3D Hard-Surface & EVA Gear Modeling, Translucent Door Assembly & UVs) & Gage (Godot 4 Scene Integration, Interior Practical Lighting & 1080p Beauty Renders)

---

## 1. Shared Standards & Technical Rules for All 5 EVA Suit Locker Candidates

### 1.1 Output Paths & Naming Convention
- **3D Models (`.glb`):** `/workspace/game-project/assets/glb/locker_round1/locker_r1_01.glb` through `/workspace/game-project/assets/glb/locker_round1/locker_r1_05.glb`
- **Texture Suite (`.png`):** `/workspace/game-project/assets/textures/locker_round1/` (and mirrored in `/workspace/game-project/assets/textures/`)
- **Individual 1080p Beauty Renders (`.png`):** `/workspace/game-project/assets/renders/locker_round1/locker_r1_01.png` through `locker_r1_05.png` (and mirrored in `/workspace/game-project/godot/renders/locker_round1/`)
- **5-Panel Voting Comparison Sheet:** `/workspace/game-project/assets/renders/locker_round1/locker_round1_voting_sheet.png`

### 1.2 Coordinate System, Footprint & Pivot Convention
- **Metric Scale:** `1.0 unit = 1.0 meter`.
- **World Origin & Pivot Point:** Bottom-center `(0.0, 0.0, 0.0)` resting flush on the `Y = 0.0` floor plane (`min_y == 0.0000`, centered in `X` and `Z`).
- **Front Orientation (`+Z` Forward):** The translucent suit-bay door and front access face **`+Z`**, the rear bulkhead mounting frame rests at **`-Z`**, left side is **`-X`**, and right side is **`+X`**.
- **Polygon Budget:** **`3,000 – 6,000 triangles`** per candidate (including the full 3D interior EVA suit kit).

### 1.3 Mandatory Interior 3D EVA Gear Kit (Visible Inside Every Locker!)
Every single locker (`locker_r1_01` through `locker_r1_05`) MUST house a detailed, multi-part **3D EVA Suit & Life-Support Gear Kit** inside its lit interior bay, clearly visible through the **`alphaMode: "BLEND"` translucent glass door (`alpha ~ 0.18`)** (or partially open/parted door):
1. **3D EVA Helmet (`Y ~ 1.48m – 1.76m`):**
   - Sculpted rounded pressure helmet dome (`composite_aerospace_white.png` or `titanium_gunmetal_hull.png`) with side comm/ear pods and a top headlamp bezel.
   - Curved spherical/bubble **Gold-Iridium Visor** (`eva_visor_gold_iridium.png`, `metallic: 0.88`, `roughness: 0.12`) facing forward (`+Z`).
   - Machined metallic neck disconnect locking ring (`steel_machined_gantry.png`) resting on a pedestal or suspended from the upper gantry.
2. **3D Hard-Shell EVA Suit Torso / Chestplate & Articulated Shoulders (`Y ~ 0.72m – 1.44m`):**
   - Sculpted ergonomic **Hard Upper Torso (HUT)** armor chestplate (`composite_aerospace_white.png` or `carbon_slate_frame.png`) with chamfered pectoral plates and a front **DCM (Display & Control Module) chest pack** featuring an emissive status readout (`oled_suit_diagnostics.png`) and signal-orange O2 purge valve (`accent_signal_orange.png`).
   - Articulated fabric shoulder joints and hanging upper-arm/forearm pressure sleeves (`eva_fabric_ballistic_charcoal.png` and `eva_fabric_orbital_navy.png`) suspended from a machined overhead gantry yoke (`steel_machined_gantry.png`).
3. **3D Life-Support Umbilical Hoses (`Y ~ 0.65m – 1.45m`):**
   - 2 to 4 curved 3D spline-extruded tubes (`R = 0.016m – 0.022m`) looping organically from the locker's interior bulkhead manifold into the EVA torso's chest/waist ports, terminated with machined steel & signal-orange quick-disconnect couplings (`steel_machined_gantry.png`, `accent_signal_orange.png`).
4. **3D Magnetic Boots Pair (`Y ~ 0.12m – 0.44m`):**
   - Left and right sculpted hard sci-fi EVA mag-boots resting on the lower boot deck/charging cradle: heavy metallic magnetic sole plates (`steel_machined_gantry.png`), armored toe caps (`composite_aerospace_white.png` / `titanium_gunmetal_hull.png`), calf gaiters (`eva_fabric_ballistic_charcoal.png`), and ankle clamp rings.

---

## 2. Texture & Material Library Manifest (`/workspace/game-project/assets/textures/locker_round1/`)

All 11 textures are `1024×1024` ultra-clean, low-noise (`<1.2%–1.5%` micro-variation) PNGs stored in `/workspace/game-project/assets/textures/locker_round1/` and mirrored in `/workspace/game-project/assets/textures/`.

| # | Filename | Format | Base Hex / Tone | Roughness | Metallic | Alpha / Emissive & Material Usage |
|---|----------|--------|-----------------|-----------|----------|-----------------------------------|
| 1 | `titanium_gunmetal_hull.png` | RGB | `#1A1E24` | `0.34` | `0.78` | Primary dark anodized gunmetal titanium locker enclosures & pressure rings |
| 2 | `composite_aerospace_white.png` | RGB | `#D8DEE6` | `0.30` | `0.08` | Smooth matte aerospace white interior bay liners, capsule shells & EVA helmet/HUT armor |
| 3 | `carbon_slate_frame.png` | RGB | `#282E38` | `0.40` | `0.58` | Dark carbon-slate structural framing, hex bevels, side kit shelves & boot trays |
| 4 | `steel_machined_gantry.png` | RGB | `#88929E` | `0.22` | `0.90` | Machined brushed steel for overhead suit suspension gantries, neck rings, couplings & boot soles |
| 5 | `eva_fabric_ballistic_charcoal.png` | RGB | `#242932` | `0.78` | `0.00` | Technical charcoal ballistic ripstop/neoprene for EVA suit sleeves, joints & tactical pouches |
| 6 | `eva_fabric_orbital_navy.png` | RGB | `#1D2C3C` | `0.76` | `0.00` | Deep orbital navy pressure-garment fabric for suit under-layers, flight bags & stowed packs |
| 7 | `eva_visor_gold_iridium.png` | RGB | `#D49B35` | `0.12` | `0.88` | Reflective metallic gold-amber iridium coating for the curved 3D EVA helmet bubble visor |
| 8 | `accent_signal_orange.png` | RGB | `#D95B26` | `0.48` | `0.06` | Matte aerospace signal-orange for emergency airlock latches, O2 tank valves & umbilical collars |
| 9 | `glass_suitbay_translucent.png` | **RGBA** | `#0E2230` | `0.08` | `0.10` | **`alphaMode: "BLEND"` (`alpha ~ 0.18`)**, cyan-tinted armored suit-bay glass door with specular sweep |
| 10 | `glass_uv_sterilizer_violet.png` | **RGBA** | `#1A1433` | `0.08` | `0.10` | **`alphaMode: "BLEND"` (`alpha ~ 0.19`)**, violet-tinted quartz UV-sterilizer glass door for `#04` |
| 11 | `oled_suit_diagnostics.png` | RGB | `#0A0E14` + `#00E5FF` | `0.15` | `0.10` | **`emission_enabled: true` (`energy = 2.0`)**, dark-glass OLED EVA suit telemetry & O2 diagnostic panel |

---

## 3. Detailed Per-Candidate Specifications (`locker_r1_01` through `locker_r1_05`)

---

### Candidate 01: `locker_r1_01` — `#01 — Pressurized Cylindrical Airlock Suit Pod`
*Dimensions: `1.10m W × 0.85m D × 2.15m H`*

- **Color Palette (Hex Codes):**
  - Outer Cylindrical Pressure Shell & Bulkhead Rings: Gunmetal Titanium `#1A1E24` & Carbon Slate `#282E38`
  - Inner Concave Suit Bay Backwall & EVA Armor: Aerospace White `#D8DEE6`
  - EVA Helmet Visor: Gold Iridium `#D49B35`
  - Rotary Ceiling Gantry & Mag-Boot Deck: Brushed Machined Steel `#88929E`
  - Emergency Airlock Latch & Umbilical Collars: Signal Orange `#D95B26`
  - Practical Interior Lighting: Dual Vertical Cyan Light Pillars `#00E5FF` + Warm Amber Boot Ring `#FF9500`
- **Surface Material & Texture Assignments:**
  - `Cylindrical_Airlock_Shell`, `Top_Crown_Cap` & `Bottom_Pressure_Base`: `titanium_gunmetal_hull.png` (`roughness: 0.34`, `metallic: 0.78`)
  - `Inner_Curved_Bay_Liner` & `EVA_Helmet_And_HUT_Armor`: `composite_aerospace_white.png` (`roughness: 0.30`, `metallic: 0.08`)
  - `Rotary_Suspension_Gantry`, `Door_Track_Bezels` & `Boot_Clamp_Deck`: `steel_machined_gantry.png` (`roughness: 0.22`, `metallic: 0.90`)
  - `EVA_Helmet_Bubble_Visor`: `eva_visor_gold_iridium.png` (`roughness: 0.12`, `metallic: 0.88`)
  - `EVA_Suit_Sleeves_And_Umbilical_Hoses`: `eva_fabric_ballistic_charcoal.png` & `eva_fabric_orbital_navy.png`
  - `Airlock_Release_Handle_And_Couplings`: `accent_signal_orange.png`
  - `Curved_Sliding_Airlock_Glass_Doors`: `glass_suitbay_translucent.png` (`alphaMode: "BLEND"`, `alpha: 0.18`)
  - `Chest_PLSS_And_Side_OLED_Display`: `oled_suit_diagnostics.png` (`emissive: [0.22, 0.82, 1.0]`)
- **3D Geometry & Interior Layout Brief for Rook:**
  - Sculpt a sleek vertical **cylindrical/stadium-section pressurized airlock tube** (`1.10m W × 0.85m D × 2.15m H`) with heavy chamfered top (`Y = 1.92m–2.15m`) and bottom (`Y = 0.0m–0.20m`) pressure bulkhead collars.
  - Across the front (`+Z`) arc, build **twin curved translucent armored-glass sliding doors (`glass_suitbay_translucent.png`) parted open by `0.24m` in the center** (with vertical brushed-steel sealing edges and a signal-orange manual override latch bar) so the viewer sees the suit both directly through the center gap and through the curved translucent glass wings.
  - Inside the white-lined pressurized chamber, suspend the **white hard-shell EVA torso + gold-visor helmet** from a **central ceiling rotary carousel gantry (`Y = 1.85m`)**, route **two coiled/curved life-support umbilical hoses** from the left inner rib to the chestplate, and place the **pair of sculpted mag-boots** on a circular recessed charging deck at `Y = 0.20m` ringed by an amber emissive status halo.
- **3-Point + Interior Practical Lighting Rig:**
  - **Key:** Pos `(1.8, 2.3, 2.4)`, Color `#E6F2FF`, Energy `1.30`.
  - **Fill:** Pos `(-1.9, 1.4, 2.0)`, Color `#78A8D8`, Energy `0.48`.
  - **Rim:** Pos `(0.0, 2.5, -1.5)`, Color `#00E5FF`, Energy `0.90`.
  - **Interior Practicals:**
    1. `Internal_Suit_Spot_Cyan`: Local Pos `(0.0, 1.75, 0.12)`, Color `#00E5FF`, Energy `1.65`, Range `2.2m` (illuminates gold visor and white chestplate).
    2. `Boot_Deck_Amber_Glow`: Local Pos `(0.0, 0.28, 0.10)`, Color `#FF9500`, Energy `1.15`, Range `1.4m`.

---

### Candidate 02: `locker_r1_02` — `#02 — Dual-Bay Recessed Bulkhead Suit & Kit Locker`
*Dimensions: `1.35m W × 0.75m D × 2.10m H`*

- **Color Palette (Hex Codes):**
  - Outer Bulkhead Cabinet Frame: Gunmetal Titanium `#1A1E24` & Carbon Slate Divider `#282E38`
  - Left Suit Bay Backplate & EVA Torso: Aerospace White `#D8DEE6`
  - Right Kit Bay Packs & Pouches: Orbital Navy `#1D2C3C` & Charcoal `#242932`
  - O2 Canister Collars & Latches: Signal Orange `#D95B26`
  - Practical Interior Lighting: Left Bay Ice-Cyan `#00E5FF` + Right Kit Bay Warm Amber `#FF9500`
- **Surface Material & Texture Assignments:**
  - `Outer_Bulkhead_Frame` & `Center_Partition`: `titanium_gunmetal_hull.png` & `carbon_slate_frame.png`
  - `Left_Suit_Bay_Liner` & `EVA_Suit_Armor`: `composite_aerospace_white.png`
  - `EVA_Helmet_Visor`: `eva_visor_gold_iridium.png`
  - `Overhead_Suit_Yoke`, `Shelf_Lips` & `Boot_Racks`: `steel_machined_gantry.png`
  - `Stowed_Flight_Bags_And_Suit_Arms`: `eva_fabric_orbital_navy.png` & `eva_fabric_ballistic_charcoal.png`
  - `O2_Canister_Valves_And_Straps`: `accent_signal_orange.png`
  - `Left_Suit_Bay_Translucent_Door`: `glass_suitbay_translucent.png` (`alphaMode: "BLEND"`, `alpha: 0.18`)
  - `Right_Bay_Telemetry_Screen`: `oled_suit_diagnostics.png` (`emissive: [0.22, 0.82, 1.0]`)
- **3D Geometry & Interior Layout Brief for Rook:**
  - Build an asymmetric **split-bay spacecraft bulkhead locker (`1.35m W × 0.75m D × 2.10m H`)**:
    - **Left Bay (`X = -0.675m` to `+0.175m`, `0.85m` wide):** Full-height pressurized EVA suit bay enclosed by a chamfered brushed-steel frame and a large single-pane **`alphaMode: "BLEND"` translucent glass door (`glass_suitbay_translucent.png`)**. Inside: sculpted EVA helmet on an upper cradle (`Y = 1.58m`), hard-shell chestplate + navy/charcoal arms (`Y = 0.80m–1.42m`), dual umbilical hoses, and mag-boots on the bottom grate (`Y = 0.16m`).
    - **Right Bay (`X = +0.175m` to `+0.675m`, `0.50m` wide):** Open/recessed 3-tier personal crew kit bay:
      * **Top Compartment (`Y = 1.45m–1.95m`):** Angled **`oled_suit_diagnostics.png` telemetry monitor** + stowed comm headset.
      * **Middle Compartment (`Y = 0.82m–1.42m`):** Sculpted soft-goods **orbital-navy flight bag & EVA gauntlets** secured with a signal-orange retention strap.
      * **Bottom Compartment (`Y = 0.16m–0.78m`):** Twin vertical cylindrical **spare O2/N2 life-support canisters** with signal-orange valve collars and pressure gauges.
- **3-Point + Interior Practical Lighting Rig:**
  - **Key:** Pos `(1.9, 2.3, 2.5)`, Color `#E8F2FF`, Energy `1.30`.
  - **Fill:** Pos `(-2.0, 1.4, 2.1)`, Color `#7CA8D8`, Energy `0.48`.
  - **Rim:** Pos `(-1.6, 2.5, -1.5)`, Color `#00E5FF`, Energy `0.90`.
  - **Interior Practicals:**
    1. `Left_SuitBay_Cyan_Wash`: Local Pos `(-0.25, 1.82, 0.08)`, Color `#00E5FF`, Energy `1.60`, Range `2.2m`.
    2. `Right_KitBay_Amber_Shelves`: Local Pos `(0.42, 1.15, 0.12)`, Color `#FF9500`, Energy `1.35`, Range `1.7m`.

---

### Candidate 03: `locker_r1_03` — `#03 — Hex-Frame Exosuit Gantry & Mag-Boot Alcove`
*Dimensions: `1.20m W × 0.80m D × 2.15m H`*

- **Color Palette (Hex Codes):**
  - Elongated Hex Alcove Hull: Carbon Slate `#282E38` & Gunmetal Titanium `#1A1E24`
  - Articulated Overhead Gantry Crane & Boot Clamps: Brushed Machined Steel `#88929E`
  - Exosuit Armor & Inner Backplate: Aerospace White `#D8DEE6` & Charcoal `#242932`
  - Gantry Locks & Umbilical Disconnects: Signal Orange `#D95B26`
  - Practical Interior Lighting: Ice-White Gantry Spot `#E0F4FF` + Hex Perimeter Cyan `#00E5FF` + Boot Clamp Orange `#FF6B1A`
- **Surface Material & Texture Assignments:**
  - `Hex_Outer_Enclosure`: `carbon_slate_frame.png` & `titanium_gunmetal_hull.png`
  - `Inner_Hex_Backplate` & `Exosuit_Chestplate`: `composite_aerospace_white.png`
  - `Cantilever_Gantry_Crane_Arms` & `Mag_Boot_Clamps`: `steel_machined_gantry.png`
  - `EVA_Helmet_Visor`: `eva_visor_gold_iridium.png`
  - `Heavy_Braided_Umbilicals` & `Suit_Underlayer`: `eva_fabric_ballistic_charcoal.png`
  - `Gantry_Release_Latches`: `accent_signal_orange.png`
  - `Faceted_Hex_Translucent_Shield_Doors`: `glass_suitbay_translucent.png` (`alphaMode: "BLEND"`, `alpha: 0.18`)
  - `Gantry_Diagnostic_HUD`: `oled_suit_diagnostics.png`
- **3D Geometry & Interior Layout Brief for Rook:**
  - Construct an industrial **elongated hexagonal chamfered alcove** (`1.20m W × 0.80m D × 2.15m H`) with 45° beveled upper and lower side shoulders lined with continuous cyan LED cove strips.
  - Mount a beefy **articulated machined-steel overhead cantilever gantry arm** (`Y = 1.82m`) that reaches forward to suspend the sculpted EVA helmet and armored torso in a ready-to-don posture.
  - Along the angled left and right inner walls, model **four sweeping 3D umbilical hoses** connected to hexagonal manifold blocks.
  - At the base (`Y = 0.0m–0.26m`), build a **stepped magnetic boot-clamping platform** with mechanical toe/heel lock bars gripping the 3D mag-boots.
  - Enclose the front aperture with **two faceted hex-cut translucent glass doors (`glass_suitbay_translucent.png`)** with machined steel edge hinges.
- **3-Point + Interior Practical Lighting Rig:**
  - **Key:** Pos `(1.8, 2.3, 2.4)`, Color `#EAF4FF`, Energy `1.32`.
  - **Fill:** Pos `(-1.9, 1.4, 2.0)`, Color `#78A8D8`, Energy `0.48`.
  - **Rim:** Pos `(1.6, 2.5, -1.5)`, Color `#00E5FF`, Energy `0.92`.
  - **Interior Practicals:**
    1. `Gantry_Overhead_Ice_Spot`: Local Pos `(0.0, 1.80, 0.10)`, Color `#E0F4FF`, Energy `1.65`, Range `2.2m`.
    2. `Hex_Perimeter_Cyan_Cove`: Local Pos `(0.0, 1.15, 0.18)`, Color `#00E5FF`, Energy `1.35`, Range `2.0m`.

---

### Candidate 04: `locker_r1_04` — `#04 — Sleek Aerospace Capsule Wardrobe & UV Sterilizer`
*Dimensions: `1.15m W × 0.75m D × 2.12m H`*

- **Color Palette (Hex Codes):**
  - Molded Monocoque Capsule Shell: Matte Aerospace White `#D8DEE6`
  - Recessed Trim Collar & Base Plinth: Gunmetal Titanium `#1A1E24`
  - Translucent UV Quartz Door: Violet-Tinted Glass `#1A1433` (`alpha ~ 0.19`)
  - EVA Suit & Soft-Goods: Aerospace White `#D8DEE6`, Orbital Navy `#1D2C3C` & Gold Visor `#D49B35`
  - Practical Interior Lighting: Ultraviolet-Indigo Sterilizer Glow `#7B5CFF` + Cyan `#00E5FF` + External Amber Status `#FF9500`
- **Surface Material & Texture Assignments:**
  - `Molded_Capsule_Outer_Shell` & `Inner_Sterilizer_Chamber`: `composite_aerospace_white.png` (`roughness: 0.28`, `metallic: 0.08`)
  - `Base_Plinth_And_Bezel_Collar`: `titanium_gunmetal_hull.png` & `steel_machined_gantry.png`
  - `EVA_Helmet_Visor`: `eva_visor_gold_iridium.png`
  - `EVA_Suit_Arms_And_Pouches`: `eva_fabric_orbital_navy.png` & `eva_fabric_ballistic_charcoal.png`
  - `Curved_UV_Quartz_Translucent_Door`: `glass_uv_sterilizer_violet.png` (`alphaMode: "BLEND"`, `alpha: 0.19`)
  - `Side_Bio_Decon_OLED_Panel`: `oled_suit_diagnostics.png` (`emissive: [0.35, 0.30, 1.0]`)
- **3D Geometry & Interior Layout Brief for Rook:**
  - Sculpt a **smooth stadium-filleted aerospace-white monocoque capsule wardrobe** (`1.15m W × 0.75m D × 2.12m H`) with rounded `R = 0.22m` vertical corner fillets and a dark titanium recessed base plinth.
  - Divide the bright white interior into three clean ergonomic zones visible behind the **full-height stadium-curved violet-tinted translucent quartz door (`glass_uv_sterilizer_violet.png`)**:
    1. **Top Helmet Pedestal Niche (`Y = 1.48m–1.88m`):** Backlit circular glass shelf displaying the 3D gold-visor EVA helmet.
    2. **Main UV-C Suit Sterilization Bay (`Y = 0.60m–1.45m`):** Suspended EVA hard torso + navy sleeves flanked by **four vertical glowing ultraviolet (`#7B5CFF`) emitter tubes** embedded in the left and right inner walls, plus clean braided umbilical loops.
    3. **Bottom Pull-Out Boot Sterilizer Tray (`Y = 0.15m–0.52m`):** Machined steel tray cradling the pair of 3D mag-boots.
  - Embed a vertical `oled_suit_diagnostics.png` bio-decontamination readout screen on the right front bezel (`X = +0.48m, Y = 1.25m, Z = +0.36m`).
- **3-Point + Interior Practical Lighting Rig:**
  - **Key:** Pos `(1.8, 2.3, 2.4)`, Color `#ECE8FF`, Energy `1.30`.
  - **Fill:** Pos `(-1.9, 1.4, 2.0)`, Color `#82A8E0`, Energy `0.48`.
  - **Rim:** Pos `(-1.5, 2.5, -1.5)`, Color `#7B5CFF`, Energy `0.95`.
  - **Interior Practicals:**
    1. `UV_Sterilizer_Violet_Glow`: Local Pos `(0.0, 1.25, 0.08)`, Color `#7B5CFF`, Energy `1.65`, Range `2.2m` + emissive UV-C emitter bars (`emissive: [0.55, 0.38, 1.0]`).
    2. `Helmet_Niche_Cyan_Spot`: Local Pos `(0.0, 1.78, 0.05)`, Color `#00E5FF`, Energy `1.35`, Range `1.6m`.

---

### Candidate 05: `locker_r1_05` — `#05 — Corner-Mount Angled Tactical EVA Prep Station`
*Dimensions: `1.25m W × 0.85m D × 2.15m H`*

- **Color Palette (Hex Codes):**
  - 45°-Angled Corner Bulkhead Chassis: Gunmetal Titanium `#1A1E24` & Carbon Slate `#282E38`
  - Center Suit Bay Backwall & Tank Racks: Brushed Machined Steel `#88929E` & Aerospace White `#D8DEE6`
  - Tactical EVA Suit & Mag-Boots: Charcoal `#242932`, Aerospace White `#D8DEE6` & Gold Visor `#D49B35`
  - Life-Support O2/N2 Cylinders & Valves: Signal Orange `#D95B26`
  - Practical Interior Lighting: Tactical Amber Backlight `#FF9500` + Cool Cyan Rim & OLED `#00E5FF`
- **Surface Material & Texture Assignments:**
  - `Angled_Corner_Chassis` & `Side_Wing_Housings`: `titanium_gunmetal_hull.png` & `carbon_slate_frame.png`
  - `Center_Suit_Bay_Liner` & `EVA_Torso_Armor`: `composite_aerospace_white.png`
  - `Gantry_Yoke`, `Grated_Boot_Deck` & `Tank_Clamps`: `steel_machined_gantry.png`
  - `EVA_Helmet_Visor`: `eva_visor_gold_iridium.png`
  - `Tactical_Suit_Sleeves_And_Hoses`: `eva_fabric_ballistic_charcoal.png` & `eva_fabric_orbital_navy.png`
  - `O2_Tank_Valves_And_Quick_Releases`: `accent_signal_orange.png`
  - `Panoramic_Center_Translucent_Door`: `glass_suitbay_translucent.png` (`alphaMode: "BLEND"`, `alpha: 0.18`)
  - `Left_Wing_OLED_Diagnostics_Terminal`: `oled_suit_diagnostics.png` (`emissive: [0.22, 0.82, 1.0]`)
- **3D Geometry & Interior Layout Brief for Rook:**
  - Design a **chamfered wedge/corner-mount EVA prep station** (`1.25m W × 0.85m D × 2.15m H`) with a wide center pressurized suit bay (`0.78m` wide) flanked by **two 35°-angled forward-canted side utility wings**:
    - **Left Angled Wing (`-X`):** Houses a flush-mounted **`oled_suit_diagnostics.png` diagnostics terminal**, pressure regulator dials, and the dual umbilical manifold feeding into the center bay.
    - **Right Angled Wing (`+X`):** Houses a vertical recessed rack of **three cylindrical high-pressure O2/N2 life-support bottles** with signal-orange valve necks and machined steel retention clamps.
    - **Center Suit Bay:** Covered by a tall beveled **`alphaMode: "BLEND"` translucent armored glass door (`glass_suitbay_translucent.png`)**, showcasing the 3D gold-visor helmet, armored chestplate with PLSS pack, looped umbilical hoses, and mag-boots standing on a raised machined-steel deck grate.
- **3-Point + Interior Practical Lighting Rig:**
  - **Key:** Pos `(1.8, 2.3, 2.5)`, Color `#E8F2FF`, Energy `1.32`.
  - **Fill:** Pos `(-1.9, 1.4, 2.1)`, Color `#78A4D0`, Energy `0.48`.
  - **Rim:** Pos `(0.0, 2.5, -1.6)`, Color `#FF9500`, Energy `0.90`.
  - **Interior Practicals:**
    1. `Tactical_Suit_Backlight_Amber`: Local Pos `(0.0, 1.28, -0.18)`, Color `#FF9500`, Energy `1.55`, Range `2.1m`.
    2. `Front_Frame_Cyan_Rim`: Local Pos `(0.0, 1.82, 0.22)`, Color `#00E5FF`, Energy `1.50`, Range `2.2m`.

---

## 4. Standardized Camera Framing & Render Guide (`Gage` & `Rook`)

1. **Heroic Full-Height Vertical Framing (`1920 × 1080` Individual Renders):**
   - Because each EVA Suit Locker stands **`2.10m – 2.15m` tall** and `1.10m – 1.35m` wide:
     - **Target Look-At Point:** `(0.0, 1.06, 0.0)` (vertical midpoint at chestplate/umbilical height).
     - **Camera Yaw / Pitch:** Gently alternating 3/4 beauty angles (`yaw = ±18° to ±22°`, `pitch = -10° to -12°`) at distance `~2.65m – 2.85m` (`FOV = 46°`) so the entire locker from `Y = 0.0m` floor plinth to `Y = 2.15m` top crown fits comfortably with clean breathing room around HUD badges.
2. **Translucent Glass Door Rendering (`alphaMode: "BLEND"`):**
   - Render all **opaque submeshes first** (including the interior 3D EVA helmet, gold iridium visor, white/charcoal chestplate, umbilical hoses, O2 tanks, and mag-boots, illuminated by the interior point lights), and then composite the **`alphaMode: "BLEND"` translucent glass door (`alpha ~ 0.18` + specular reflection)** over the interior so the suit inside is sharp, bright, and unmistakable!
3. **5-Panel Voting Comparison Sheet (`/workspace/game-project/assets/renders/locker_round1/locker_round1_voting_sheet.png`):**
   - Arrange all 5 candidates (`#01` through `#05`) in a crisp high-resolution comparison grid (e.g., `5 × 1` panoramic strip or `3 + 2` two-row gallery sheet) with clear numbered title badges (`#01 — PRESSURIZED CYLINDRICAL AIRLOCK SUIT POD` .. `#05 — CORNER-MOUNT ANGLED TACTICAL EVA PREP STATION`), dimensions, and triangle counts.
