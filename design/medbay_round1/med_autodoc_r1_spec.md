# Room 04 Hero Asset: Surgical Autodoc Gantry & Triage Console — Round 1 Design, 3D Robotic Arms, Translucent Canopy & Lighting Spec
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Pipeline Stage:** Room 04 Hero Asset — 5-Choice Test (`med_autodoc_r1_01` through `med_autodoc_r1_05`)  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)  
**Target Teams:** Rook (3D Hard-Surface & Robotic Surgical Gantry/Canopy Modeling, 3D Pharmacy Vials & UVs) & Gage (Godot 4 Scene Integration, Surgical Lighting & 1080p Beauty Renders)

---

## 1. Shared Standards & Technical Rules ("Aegis-7 Standard")

### 1.1 Output Paths & Naming Convention
- **3D Models (`.glb`):** `/workspace/game-project/assets/glb/medbay_round1/med_autodoc_r1_01.glb` through `/workspace/game-project/assets/glb/medbay_round1/med_autodoc_r1_05.glb`
- **Winner Export Path (after all 5 renders complete & 5-Bot Vote):** `/workspace/game-project/assets/glb/winners/med_autodoc_winner_01_...glb`
- **Texture Suite (`.png`):** `/workspace/game-project/assets/textures/medbay_round1/` (and mirrored in `/workspace/game-project/assets/textures/`)
- **Individual 1080p Beauty Renders (`.png`):** `/workspace/game-project/assets/renders/medbay_round1/med_autodoc_r1_01.png` through `med_autodoc_r1_05.png` (and mirrored in `/workspace/game-project/godot/renders/medbay_round1/`)
- **5-Panel Voting Comparison Sheet:** `/workspace/game-project/assets/renders/medbay_round1/med_autodoc_round1_voting_sheet.png` (and mirrored in `/workspace/game-project/godot/renders/medbay_round1/`)

### 1.2 Coordinate System, Autodoc Footprint & Pivot Convention
- **Metric Scale:** `1.0 unit = 1.0 meter`.
- **Target Surgical Autodoc Bay Footprint:** `2.10m – 2.30m Wide (X) × 1.15m – 1.35m Deep (Z) × 2.05m – 2.20m Tall (Y)`.
- **World Origin & Pivot Point:** Bottom-center `(0.0, 0.0, 0.0)` resting flush on the `Y = 0.0` floor plane (`min_y == 0.0000`, centered in `X` and `Z`), front patient transfer access facing **`+Z`**, rear surgical bulkhead spine at **`-Z`**.
- **Polygon Budget:** **`3,500 – 6,000 triangles`** per candidate.

### 1.3 Mandatory 4-Part 3D Surgical Autodoc & Pharmacy Kit (Required in Every Candidate!)
1. **45° Chamfered Bulkhead Surgical Spine & Contoured Diagnostic Table (`Y ~ 0.78m`):**
   - Dark gunmetal titanium (`titanium_gunmetal_hull.png`, `#1A1E24`) and matte aerospace-white (`composite_aerospace_white.png`, `#D8DEE6`) surgical bulkhead frame supporting a cantilevered, sculpted ergonomic patient table padded in orbital-navy & charcoal biometric upholstery (`fabric_orbital_navy_pad.png` / `fabric_charcoal_flightpad.png`) with sculpted head-cradle bolster (`-X`) and signal-orange (`accent_signal_orange.png`, `#D95B26`) emergency bio-isolation release latches.
2. **Articulated 3D Multi-Joint Robotic Surgical Gantry Arms & Shadowless Halo Lamp (`Y ~ 1.35m – 1.95m`):**
   - **Two or three articulated 3D robotic surgical arms** (`steel_machined_gantry.png` & `composite_aerospace_white.png`) suspended from an overhead machined-steel gantry rail, terminating in detailed 3D surgical end-effectors (laser cautery emitter cone, micro-suture pincers, and optical biopsy scanner) poised over the operating field.
   - **Overhead Circular/Octagonal Shadowless Surgical Halo Lamp** (`#E0F4FF` surgical ice-white + `#00E5FF` cyan ring).
3. **Translucent Bio-Isolation Scanner Canopy & UV-Sterile Pharmacy Supply Bay (`glass_med_sterile_translucent.png`, `alphaMode: "BLEND"`, `alpha ~ 0.19`):**
   - Curved or faceted **`alphaMode: "BLEND"` translucent bio-isolation shield / toroidal scanner canopy (`glass_med_sterile_translucent.png`)** arcing over the head/torso zone of the surgical table.
   - Integrated **UV-C Sterile Pharmacy & Cryo-Vial Cabinet** behind a translucent `glass_med_sterile_translucent.png` door, displaying **3D glowing cyan/violet cryo-plasma vials, cylindrical hypospray injectors, and white/orange emergency trauma packs** inside!
4. **Articulated Multi-Screen OLED Biomonitor Triage Array (`oled_medbay_vitals.png`):**
   - Canted widescreen OLED surgical telemetry monitor (`oled_medbay_vitals.png`, `emissive_energy = 2.0`) mounted on a swiveling brushed-steel boom arm beside the surgical table.

---

## 2. Texture & Material Library Manifest (`/workspace/game-project/assets/textures/medbay_round1/`)

| # | Filename | Format | Base Hex / Tone | Roughness | Metallic | Alpha / Emissive & Material Usage |
|---|----------|--------|-----------------|-----------|----------|-----------------------------------|
| 1 | `titanium_gunmetal_hull.png` | RGB | `#1A1E24` | `0.34` | `0.78` | Primary 45° chamfered gunmetal titanium surgical bulkhead frame |
| 2 | `composite_aerospace_white.png` | RGB | `#D8DEE6` | `0.26` | `0.08` | Smooth matte aerospace white surgical table shell, robotic arm cowlings & scanner rings |
| 3 | `carbon_slate_frame.png` | RGB | `#282E38` | `0.40` | `0.58` | Dark carbon-slate base pedestal, gantry track housing & pharmacy shelves |
| 4 | `steel_machined_gantry.png` | RGB | `#88929E` | `0.20` | `0.90` | Brushed machined steel for articulated robotic joints, surgical tools, rails & vials |
| 5 | `fabric_charcoal_flightpad.png` | RGB | `#242932` | `0.78` | `0.00` | Contoured charcoal biometric table bolsters & restraint pads |
| 6 | `fabric_orbital_navy_pad.png` | RGB | `#1D2C3C` | `0.76` | `0.00` | Deep orbital navy sterile patient couch pad & head cradle |
| 7 | `accent_signal_orange.png` | RGB | `#D95B26` | `0.48` | `0.06` | Matte signal-orange for emergency bio-seal locks, laser warning collars & defibrillator paddles |
| 8 | `oled_medbay_vitals.png` | RGB | `#0A0E14` + `#00E5FF` | `0.14` | `0.10` | **`emission_enabled: true` (`energy = 2.0`)**, surgical ECG, SpO2 99.2% & neural triage OLED |
| 9 | `glass_med_sterile_translucent.png` | **RGBA** | `#0E2230` + `#00E5FF` | `0.08` | `0.10` | **`alphaMode: "BLEND"` (`alpha ~ 0.19`)**, translucent bio-isolation canopy & UV pharmacy door |

---

## 3. Detailed Per-Candidate Specifications (`med_autodoc_r1_01` through `med_autodoc_r1_05`)

1. **`med_autodoc_r1_01.glb` — `#01 — Aegis-7 Octagonal Bulkhead Surgical Autodoc & Ring Scanner` (`2.18m W × 1.25m D × 2.12m H`):**
   - Symmetrical 45° chamfered octagonal aerospace-white & gunmetal surgical bay with a central translating octagonal MRI/CT scanner ring, twin overhead articulated robotic surgical arms, curved `glass_med_sterile_translucent.png` head canopy, boom-mounted `oled_medbay_vitals.png` display, and recessed backwall UV pharmacy niches.
2. **`med_autodoc_r1_02.glb` — `#02 — Dual-Zone Split Autodoc Gantry & Translucent UV Pharmacy Tower` (`2.25m W × 1.28m D × 2.15m H`):**
   - **Direct asymmetric 68% / 32% split-bay sibling to all locked Aegis-7 winners!**
   - **Left Bay (68% width, `1.53m` wide):** Houses the cantilevered aerospace-white & orbital-navy contoured surgical bed (`Y = 0.78m`) on a chamfered pedestal, **twin overhead multi-jointed robotic surgical arms (`steel_machined_gantry.png` & `composite_aerospace_white.png`)** descending from a linear gantry rail with a circular surgical ice-white (`#E0F4FF`) halo lamp, a curved **`alphaMode: "BLEND"` translucent bio-isolation head/chest visor (`glass_med_sterile_translucent.png`)**, and a swiveling `oled_medbay_vitals.png` triage monitor arm.
   - **Right Bay (32% width, `0.72m` wide):** Full-height 3-tier **UV-C Sterile Pharmacy, Cryo-Vial & Trauma Supply Tower** enclosed by a bevel-framed **`alphaMode: "BLEND"` translucent glass door (`glass_med_sterile_translucent.png`)**:
     * Top tier: Glowing cyan/violet rack of 8 cylindrical cryo-plasma & stem-cell vials under a `#7B5CFF` UV-sterilizer bar.
     * Middle tier: 3D arrayed hypospray injectors, surgical laser cartridges, and secondary `oled_medbay_vitals.png` diagnostic screen.
     * Bottom tier: Twin emergency O2/anesthesia cylinders with signal-orange regulator valves and portable trauma defibrillator case.
3. **`med_autodoc_r1_03.glb` — `#03 — Twin-Arm Ceiling Cantilever Robotic Trauma Bay & Holo-Visor` (`2.15m W × 1.25m D × 2.15m H`):**
   - Open-access high-speed orbital trauma bay with a heavy C-arm ceiling surgical crane carrying three articulated micro-surgery manipulators, dual overhead surgical halo lamps, and a clamshell translucent `glass_med_sterile_translucent.png` splash/laser shield.
4. **`med_autodoc_r1_04.glb` — `#04 — Cryo-Stasis Isolation Pod & Sliding Toroidal MRI Gantry` (`2.20m W × 1.30m D × 2.12m H`):**
   - Deep-space cryo-surgical pod featuring a full-length semi-cylindrical `glass_med_sterile_translucent.png` isolation canopy that slides through a heavy chamfered toroidal magnetic-resonance gantry ring with external cryo-coolant manifolds and signal-orange purge valves.
5. **`med_autodoc_r1_05.glb` — `#05 — Zero-G Gimbaled Surgical Cradle & Biometric Triage Console` (`2.22m W × 1.28m D × 2.15m H`):**
   - Designed for surgery during Cylinder Hab-7 spin-down emergencies: the surgical table and twin robotic arms are mounted inside a precision machined-steel rotary trunnion ring with bio-restraint straps, translucent canopy visor, and dual side pharmacy/telemetry consoles.

---

## 4. Standardized Camera Framing & Lighting Guide (`Gage` & `Rook`)

- **Target Look-At Point:** `(0.0, 1.02, 0.0)`
- **Camera Angles:** 3/4 front-isometric beauty angle (`yaw = ±22° to ±25°`, `pitch = -14°`, distance `~2.75m – 3.00m`, `FOV = 46°`).
- **Practical Lights:**
  1. `Surgical_Halo_Ice_Spot`: Local Pos `(-0.25, 1.72, 0.05)`, Color `#E0F4FF`, Energy `1.65`, Range `2.4m` (casts crisp surgical light onto the robotic arms and patient table).
  2. `Scanner_Canopy_Cyan_Glow`: Local Pos `(-0.45, 1.18, 0.05)`, Color `#00E5FF`, Energy `1.45`, Range `2.0m`.
  3. `Pharmacy_Tower_UV_Violet`: Local Pos `(+0.68, 1.35, 0.10)`, Color `#7B5CFF`, Energy `1.40`, Range `1.9m`.
