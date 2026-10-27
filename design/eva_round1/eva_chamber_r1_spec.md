# Room 05 Hero Asset: Heavy Cylindrical Outer-Hull Decompression Airlock & Umbilical Recharge Chamber — Round 1 Design Spec
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Pipeline Stage:** Room 05 Hero Asset — 5-Choice Test (`eva_chamber_r1_01` through `eva_chamber_r1_05`)  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)  
**Target Teams:** Rook (3D Hard-Surface & Decompression Cylinder/Umbilical Modeling, Translucent Viewport Door & UVs) & Gage (Godot 4 Scene Integration, Cycling Beacon Lighting & 1080p Beauty Renders)

---

## 1. Shared Standards & Technical Rules ("Aegis-7 Standard")

### 1.1 Output Paths & Naming Convention
- **3D Models (`.glb`):** `/workspace/game-project/assets/glb/eva_round1/eva_chamber_r1_01.glb` through `/workspace/game-project/assets/glb/eva_round1/eva_chamber_r1_05.glb`
- **Winner Export Path (after all 5 renders complete & 5-Bot Vote):** `/workspace/game-project/assets/glb/winners/eva_chamber_winner_01_...glb`
- **Texture Suite (`.png`):** `/workspace/game-project/assets/textures/eva_round1/` (and mirrored in `/workspace/game-project/assets/textures/`)
- **Individual 1080p Beauty Renders (`.png`):** `/workspace/game-project/assets/renders/eva_round1/eva_chamber_r1_01.png` through `eva_chamber_r1_05.png` (and mirrored in `/workspace/game-project/godot/renders/eva_round1/`)
- **5-Panel Voting Comparison Sheet:** `/workspace/game-project/assets/renders/eva_round1/eva_chamber_round1_voting_sheet.png` (and mirrored in `/workspace/game-project/godot/renders/eva_round1/`)

### 1.2 Coordinate System, Chamber Footprint & Pivot Convention
- **Metric Scale:** `1.0 unit = 1.0 meter`.
- **Target Decompression Chamber Footprint:** `2.20m – 2.40m Wide (X) × 1.40m – 1.50m Deep (Z) × 2.50m – 2.60m Tall (Y)`.
- **World Origin & Pivot Point:** Bottom-center `(0.0, 0.0, 0.0)` resting flush on the `Y = 0.0` floor plane (`min_y == 0.0000`, centered in `X` and `Z`), front staging bay entry facing **`+Z`**, outer-hull vacuum egress hatch & deep-space viewport facing **`-Z`**.
- **Polygon Budget:** **`3,800 – 6,200 triangles`** per candidate.

### 1.3 Mandatory 4-Part 3D Decompression & Umbilical Recharge Kit (Required in Every Candidate!)
1. **Heavy Cylindrical / Octagonal-Ringed Decompression Vessel & Mag-Boot Grate Deck (`Y = 0.0m – 2.55m`):**
   - Reinforced dark gunmetal titanium (`titanium_gunmetal_hull.png` / `metal_gunmetal_hull.png`, `#1A1E24`) and carbon-slate (`carbon_slate_frame.png` / `metal_carbon_slate.png`, `#282E38`) pressure vessel with 45° chamfered external pressure rings, a raised brushed-steel (`steel_machined_gantry.png` / `metal_brushed_steel.png`, `#88929E`) magnetic boot-charging deck grate (`Y = 0.16m`) with recessed amber (`#FF9500`) lock strips, interior aerospace-white (`composite_aerospace_white.png` / `panel_aerospace_white.png`, `#D8DEE6`) grab-rail wall liners, and overhead N2/O2 blowdown nozzle diffusers.
2. **Translucent Curved/Faceted Armored Airlock Door (`glass_eva_airlock_translucent.png`, `alphaMode: "BLEND"`, `alpha ~ 0.19`) + Rear Outer-Hull Deep-Space Sightline:**
   - Front chamber entry door is posed **partially open/rotated (`~30°–35°` gap)** AND glazed with **`alphaMode: "BLEND"` translucent armored glass (`glass_eva_airlock_translucent.png`)**, while the rear outer-hull hatch features a translucent porthole backed by `vista_deep_space.png` so the interior grab bars, overhead purge nozzles, and external stars/nebula read clearly!
3. **Umbilical Suit-Charge Manifold & Coiled 3D Life-Support Hoses:**
   - Integrated side or gantry recharge station with **3–4 sculpted 3D coiled/looped umbilical cables** (`eva_fabric_ballistic_charcoal.png` / `eva_fabric_orbital_navy.png`) terminated with machined-steel and **signal-orange (`accent_signal_orange.png` / `accent_safety_orange.png`, `#D95B26`) quick-disconnect couplings**, high-pressure O2/N2 cylinders, and a manual signal-orange emergency blowdown lever.
4. **Decompression Telemetry Console (`oled_eva_decompression.png`) & Translucent UV Helmet Test/Sterilizer Hood:**
   - Flush-mounted **`oled_eva_decompression.png` OLED vacuum blowdown & suit-charge display (`emissive_energy = 2.0`)**, paired with a pressurized helmet seal-test & UV-violet (`#7B5CFF`) sterilization alcove holding a **3D gold-visor EVA test helmet (`eva_visor_gold_iridium.png`)** behind a translucent `glass_eva_airlock_translucent.png` hood!

---

## 2. Texture & Material Library Manifest (`/workspace/game-project/assets/textures/eva_round1/`)

*(Note: Both canonical Aegis-7 filenames and shorthand alias filenames are present in `/workspace/game-project/assets/textures/eva_round1/` and `/workspace/game-project/assets/textures/`.)*

| # | Canonical Filename (Alias) | Format | Base Hex / Tone | Roughness | Metallic | Alpha / Emissive & Material Usage |
|---|----------------------------|--------|-----------------|-----------|----------|-----------------------------------|
| 1 | `titanium_gunmetal_hull.png` (`metal_gunmetal_hull.png`) | RGB | `#1A1E24` | `0.34` | `0.78` | Primary 45° chamfered gunmetal titanium decompression hull & external pressure rings |
| 2 | `composite_aerospace_white.png` (`panel_aerospace_white.png`) | RGB | `#D8DEE6` | `0.28` | `0.08` | Smooth matte aerospace white inner airlock liner, EVA helmet shell & O2 cylinders |
| 3 | `carbon_slate_frame.png` (`metal_carbon_slate.png`) | RGB | `#282E38` | `0.40` | `0.58` | Dark carbon-slate deck base, structural ribs & umbilical manifold housing |
| 4 | `steel_machined_gantry.png` (`metal_brushed_steel.png`) | RGB | `#88929E` | `0.20` | `0.90` | Brushed machined steel for locking dogs, interior grab-rails, floor grates & couplings |
| 5 | `fabric_charcoal_flightpad.png` (`fabric_charcoal_cushion.png`) | RGB | `#242932` | `0.78` | `0.00` | Braided charcoal umbilical hose jackets & inflatable airlock door seals |
| 6 | `fabric_orbital_navy_pad.png` (`fabric_navy_cushion.png`) | RGB | `#1D2C3C` | `0.76` | `0.00` | Deep orbital navy tether packs & acoustic shoulder bumpers |
| 7 | `eva_visor_gold_iridium.png` | RGB | `#D49B35` | `0.12` | `0.88` | Reflective metallic gold-iridium visor on the 3D EVA helmet in the seal-test hood |
| 8 | `accent_signal_orange.png` (`accent_safety_orange.png`) | RGB | `#D95B26` | `0.48` | `0.06` | Matte signal-orange for manual vacuum blowdown levers, rotary handwheels & O2 valves |
| 9 | `oled_eva_decompression.png` | RGB | `#0A0E14` + `#00E5FF` | `0.14` | `0.10` | **`emission_enabled: true` (`energy = 2.0`)**, 512×512 vacuum blowdown & suit-charge OLED |
| 10 | `glass_eva_airlock_translucent.png` | **RGBA** | `#0E2230` + `#00E5FF` | `0.08` | `0.10` | **`alphaMode: "BLEND"` (`alpha ~ 0.19`)**, 256×256 translucent airlock door & helmet test hood |
| 11 | `led_cyan_strip.png` / `led_amber_strip.png` / `led_uv_violet.png` / `led_ice_white.png` | RGB | `#00E5FF` / `#FF9500` / `#7B5CFF` / `#E0F4FF` | `0.15` | `0.00` | Emissive LED strip textures for chamber cycling beacons & UV helmet decon |

---

## 3. Detailed Per-Candidate Specifications (`eva_chamber_r1_01` through `eva_chamber_r1_05`)

1. **`eva_chamber_r1_01.glb` — `#01 — Aegis-7 Octagonal-Ringed Cylindrical Decompression Lock` (`2.25m W × 1.45m D × 2.55m H`):**
   - Symmetrical vertical cylindrical decompression chamber wrapped in three 45° chamfered octagonal gunmetal pressure collars, featuring a curved sliding `alphaMode: "BLEND"` translucent door (`glass_eva_airlock_translucent.png`) parted open 35°, interior brushed-steel grab rails and overhead N2 purge nozzles, rear deep-space porthole (`vista_deep_space.png`), left-side umbilical hose reel, and right-side `oled_eva_decompression.png` console.
2. **`eva_chamber_r1_02.glb` — `#02 — Dual-Zone Split Decompression Cylinder & Umbilical Suit-Charge Gantry` (`2.35m W × 1.45m D × 2.55m H`):**
   - **Signature 65% / 35% asymmetric split-bay Aegis-7 sibling to all locked winners!**
   - **Left Bay (65% width, `1.53m` wide):** Heavy octagonal-ringed cylindrical decompression chamber with a curved **`alphaMode: "BLEND"` translucent armored viewport door (`glass_eva_airlock_translucent.png`)** rotated 32° ajar on heavy machined-steel hinge arms with interlocking dog teeth. Inside: raised brushed-steel mag-boot floor grate ringed with `#FF9500` amber cycling strips, curved aerospace-white inner wall panels with machined grab-bars, overhead N2/O2 blowdown nozzle ring (`#00E5FF` cyan glow), and a rear outer-hull translucent porthole backed by `vista_deep_space.png`.
   - **Right Bay (35% width, `0.82m` wide):** Full-height **Recessed Umbilical Suit-Charge & Helmet Seal-Test Gantry Tower**:
     * Top/Upper Bay (`Y = 1.45m–2.35m`): Pressurized **UV-Violet (`#7B5CFF`) Helmet Seal-Test & Sterilization Chamber** behind a bevel-framed translucent `glass_eva_airlock_translucent.png` hood, showcasing a **3D white/gold-visor EVA helmet (`eva_visor_gold_iridium.png`)** mounted on a machined diagnostic neck ring!
     * Center Bay (`Y = 0.85m–1.42m`): Flush **`oled_eva_decompression.png` vacuum & battery telemetry display**, flanked by **three 3D coiled/draped umbilical recharge hoses** with signal-orange quick-disconnect couplings and a guarded **signal-orange manual blowdown lever**.
     * Lower Bay (`Y = 0.15m–0.82m`): Twin high-pressure O2/N2 purge cylinders with signal-orange regulator wheels behind a machined-steel guard rail.
3. **`eva_chamber_r1_03.glb` — `#03 — Twin-Lock Rotary Carousel Decompression Pod & Tether Rack` (`2.30m W × 1.48m D × 2.55m H`):**
   - Features a revolving drum-lock inner/outer door mechanism with three vertical `glass_eva_airlock_translucent.png` viewport panes, overhead magnetic tether winch, side `oled_eva_decompression.png` pillar, and external O2 manifold bottles.
4. **`eva_chamber_r1_04.glb` — `#04 — Hex-Bulkhead Rapid Blowdown Airlock & Suit Donning Frame` (`2.28m W × 1.42m D × 2.55m H`):**
   - Elongated hexagonal decompression chamber with bi-parting chamfered translucent blast doors, internal rear suit-donning docking ring, overhead plasma-decon light arch, and dual side umbilical booms.
5. **`eva_chamber_r1_05.glb` — `#05 — Heavy Submarine-Style Plug-Hatch EVA Lock & Cryo-O2 Bank` (`2.35m W × 1.50m D × 2.58m H`):**
   - Massive outward-swinging circular plug hatch with a central translucent porthole (`glass_eva_airlock_translucent.png`), 8 radial machined-steel locking dogs, a prominent signal-orange 4-spoke handwheel, and a side rack of four spherical/cylindrical cryo-O2 tanks + helmet test dome.

---

## 4. Standardized Camera Framing & Lighting Guide (`Gage` & `Rook`)

- **Target Look-At Point:** `(0.0, 1.25, 0.0)`
- **Camera Angles:** Heroic 3/4 front-isometric beauty angle (`yaw = ±18° to ±22°`, `pitch = -11°`, distance `~3.05m – 3.30m`, `FOV = 46°`).
- **Practical Lights:**
  1. `Chamber_Interior_Cyan_Purge`: Local Pos `(-0.35, 1.95, 0.0)`, Color `#00E5FF`, Energy `1.60`, Range `2.4m`.
  2. `Chamber_Floor_Amber_Beacon`: Local Pos `(-0.35, 0.25, 0.20)`, Color `#FF9500`, Energy `1.35`, Range `1.9m`.
  3. `Helmet_Test_Hood_UV_Violet`: Local Pos `(+0.68, 1.75, 0.15)`, Color `#7B5CFF`, Energy `1.40`, Range `1.8m`.
