# Room 01 — Crew Sleeping Quarters: Aegis-7 Architectural Layout, Fixture Blueprint & Godot 4 Lighting Spec
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Target Godot Scene:** `/workspace/game-project/godot/scenes/rooms/room_01_sleeping_quarters.tscn` (and `/workspace/game-project/godot/scenes/living_quarters.tscn`)  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)  
**Target Teams:** Rook (Room Shell / Modular Bulkhead Geometry) & Gage (Godot 4 Scene Assembly, Lighting & Multi-Angle 1080p Beauty Renders)

---

## 1. Room 01 Architectural Envelope & Unified "Aegis-7" Shell

To support both a **Full Multi-Berth Crew Stateroom Showcase (`6.0m W × 7.0m D × 3.2m H`)** that displays all 4 locked Bunk Pod winners plus all 5 non-bunk Aegis-7 fixtures with a wide walkable center aisle, AND a **Compact Single-Crew Cabin Variant (`4.5m W × 5.5m D × 3.0m H`)**, this specification provides exact non-overlapping coordinates for both!

### 1.1 Primary Stateroom Shell Envelope (`6.0m W × 7.0m D × 3.2m H`)
- **World Origin:** Center of the floor deck at `(0.0, 0.0, 0.0)`
  - **West Bulkhead Wall (`-X`):** `X = -3.00m`
  - **East Bulkhead Wall (`+X`):** `X = +3.00m`
  - **North Observation Bulkhead (`-Z`):** `Z = -3.50m`
  - **South Entry Airlock Bulkhead (`+Z`):** `Z = +3.50m`
  - **Deck Floor (`Y = 0.00m`)** to **Overhead Ceiling Crown (`Y = 3.20m`)**
- **Structural Architecture ("Aegis-7 Standard"):**
  - **45° Chamfered Octagonal Ribs:** 5 dark anodized gunmetal titanium (`titanium_gunmetal_hull.png`, `#1A1E24`) structural ring frames at `Z = -3.40m, -1.70m, 0.00m, +1.70m, +3.40m` with `0.45m × 0.45m` 45-degree upper/lower corner chamfers.
  - **Upper Cove & Ceiling Panels:** Matte aerospace-white composite (`composite_aerospace_white.png`, `#D8DEE6`) coffered ceiling panels with continuous recessed **Orbital Cyan (`#00E5FF`) LED cove channels** at `X = ±2.45m, Y = 2.95m`.
  - **Composite Deck Plating:** Dark carbon-slate (`carbon_slate_frame.png`, `#282E38`, `roughness: 0.40, metallic: 0.58`) floor deck with brushed machined-steel (`steel_machined_gantry.png`, `#88929E`) expansion strips and **recessed Circadian Amber (`#FF9500`) floor guide strips** running along `X = ±1.35m`.
  - **Dual Location-Aware Translucent Viewports (`alphaMode: "BLEND"`, `alpha ~ 0.18`):**
    1. **North Panoramic Cylinder Viewport (`Z = -3.48m, Y = 1.05m–2.45m`):** 3-panel chamfered octagonal window glazed with `glass_viewport_translucent.png`, backed at `Z = -3.95m` by an unshaded/emissive curved vista backdrop mapped with **`vista_oneill_cylinder_interior.png`** (800m × 400m O'Neill Cylinder interior at orbital dusk).
    2. **West Outer-Hull Deep-Space Viewport (`X = -3.45m` behind the Observation & Orbital Bunk alcoves):** Backed by **`vista_deep_space.png`** so looking through the translucent pod windows on the West wall reveals the deep-space starfield, cyan/indigo nebula, and neighboring orbital ring!

---

## 2. Exact Asset Placement Blueprint (`6.0m × 7.0m × 3.2m` Full Stateroom Showcase)

All coordinates `(x, y, z)` use the bottom-center `Y = 0.0` floor pivot of each `.glb` in `/workspace/game-project/assets/glb/winners/`, with `rotation_y_deg` following Godot's standard right-handed Y-up rotation (`0°` = front `+Z` of prop faces `+Z` South; `90°` = front faces `+X` East into the center aisle; `-90°` = front faces `-X` West into the center aisle; `180°` = front faces `-Z` North).

| Slot | Asset File (`/workspace/game-project/assets/glb/winners/`) | Zone / Wall | Position `(x, y, z)` | `rotation_y_deg` | Footprint `(W × D × H)` | Clear Sightline & Functional Notes |
|------|------------------------------------------------------------|-------------|----------------------|------------------|-------------------------|------------------------------------|
| **Bunk #1 (R1 #06)** | `bunk_winner_01_orbital_viewport.glb` (or `_deepspace.glb`) | **West Wall — North Bay** | `(-2.32, 0.00, -1.85)` | `+90.0°` | `2.20m × 1.25m × 2.05m` | Faces East (`+X`) into center aisle; octagonal translucent rear viewport looks out into Deep Space (`vista_deep_space.png`). |
| **Bunk #2 (R2 #09)** | `bunk_winner_04_observation_lounge.glb` | **North-East Panorama Corner** | `(+1.65, 0.00, -2.72)` | `0.0°` | `2.20m × 1.25m × 2.05m` | Faces South (`+Z`) right under the North Panoramic Cylinder Viewport (`vista_oneill_cylinder_interior.png`). |
| **Bunk #3 (R2 #08)** | `bunk_winner_03_hex_hive_stack.glb` | **West Wall — South Bay** | `(-2.32, 0.00, +0.85)` | `+90.0°` | `2.25m × 1.28m × 2.25m` | Faces East (`+X`) into center aisle; twin offset honeycomb crew pods with dual rear hex viewports. |
| **Bunk #4 (R2 #07)** | `bunk_winner_02_medical_biomonitor.glb` | **Optional East Med/Bio Berth** *(or Room 04 hero)* | `(+2.32, 0.00, -0.55)` *(if 4-bunk mode)* | `-90.0°` | `2.20m × 1.25m × 2.05m` | In 3-bunk + full utility stateroom mode, East wall is dedicated to the 3 split-bay utility stations below for maximum breathing room. |
| **Fixture #1 (EVA Locker #02)** | `locker_winner_01_dual_bay_bulkhead.glb` | **East Wall — South Utility Bay** | `(+2.52, 0.00, +1.95)` | `-90.0°` | `1.35m × 0.75m × 2.10m` | Faces West (`-X`) near the South entry door; 3D EVA suit & gold visor visible behind translucent door. |
| **Fixture #2 (Hygiene Vanity #03)** | `vanity_winner_01_dual_zone_grooming.glb` | **East Wall — North Hygiene Bay** | `(+2.62, 0.00, -1.65)` | `-90.0°` | `1.05m × 0.58m × 2.08m` | Faces West (`-X`); cyan smart-mirror HUD, zero-splash basin & UV-violet towel sterilizer tower. |
| **Fixture #3 (Cabin Desk #02)** | `walldesk_winner_01_split_comms_station.glb` | **East Wall — Center Comms Bay** | `(+2.58, 0.00, +0.15)` | `-90.0°` | `1.05m × 0.65m × 2.00m` | Faces West (`-X`); deployed fold-down desk leaf, widescreen OLED comms terminal, data-pad, mug & stool. |
| **Fixture #6 (Cargo Footlocker #02)** | `footlocker_winner_01_split_cargo_trunk.glb` | **Foot of Bunk #1 / Center-West Deck** | `(-1.05, 0.00, -1.85)` | `+90.0°` | `1.10m × 0.56m × 0.58m` | Rests at the foot/aisle edge of the primary Orbital Viewport Bunk with open translucent lid & pull-out drawer. |
| **Fixture #9 (Climate Panel #02)** | `climate_winner_01_split_env_o2_station.glb` *(or `climate_r1_02.glb`)* | **South Entry Bulkhead (`+Z`)** | `(+1.25, 0.00, +3.28)` | `180.0°` | `0.96m × 0.32m × 1.92m` | Flush against the South entry bulkhead (`+Z`) facing North (`-Z`) beside the corridor entry hatch. |

### 2.1 Compact Single-Crew Cabin Variant (`4.5m W × 5.5m D × 3.0m H`)
For tight single-berth cabin scenes (`X: -2.25..+2.25, Z: -2.75..+2.75`):
- **Primary Bunk (`bunk_winner_01_orbital_viewport.glb`):** `(-1.55, 0.00, -1.10)`, `rot_y = +90°`
- **Cargo Footlocker (`footlocker_winner_01_split_cargo_trunk.glb`):** `(-1.55, 0.00, +0.55)`, `rot_y = 0°`
- **EVA Suit Locker (`locker_winner_01_dual_bay_bulkhead.glb`):** `(+1.80, 0.00, +1.45)`, `rot_y = -90°`
- **Fold-Down Cabin Desk (`walldesk_winner_01_split_comms_station.glb`):** `(+1.85, 0.00, -0.15)`, `rot_y = -90°`
- **Hygiene & Sonic Vanity (`vanity_winner_01_dual_zone_grooming.glb`):** `(+1.88, 0.00, -1.65)`, `rot_y = -90°`
- **Climate & O2 Panel (`climate_winner_01`):** `(-0.95, 0.00, +2.55)`, `rot_y = 180°`

---

## 3. Godot 4 Lighting Rig & Environment Parameters (`room_01_sleeping_quarters.tscn`)

1. **`WorldEnvironment` Settings:**
   - `background_mode = BG_COLOR`, `background_color = #090D14`
   - `ambient_light_source = AMBIENT_SOURCE_COLOR`, `ambient_light_color = #1C2838`, `ambient_light_energy = 0.42`
   - `tonemap_mode = TONEMAPPER_ACES`, `tonemap_exposure = 1.05`
   - `ssao_enabled = true` (`radius = 0.45`, `intensity = 1.65`), `glow_enabled = true` (`intensity = 0.38`, `bloom = 0.06`)
2. **Primary & Practical Lights:**
   - **`DirectionalLight3D` (`Cylinder_Axial_Skylight`):** Rotation `(-32°, -28°, 0°)`, Color `#CFE8FF`, Energy `0.85`, `shadow_enabled = true`, `shadow_blur = 1.4` (angles through the North panoramic viewport into the cabin).
   - **`OmniLight3D` (`Ceiling_Cyan_Cove_North`):** Pos `(0.0, 2.85, -1.65)`, Color `#00E5FF`, Energy `1.25`, Range `5.5m`.
   - **`OmniLight3D` (`Ceiling_Cyan_Cove_South`):** Pos `(0.0, 2.85, +1.65)`, Color `#00E5FF`, Energy `1.15`, Range `5.5m`.
   - **`OmniLight3D` (`Bunk_Alcove_Warm_Reading`):** Pos `(-1.85, 1.35, -1.85)`, Color `#FF9500`, Energy `1.35`, Range `3.2m`.
   - **`OmniLight3D` (`Vanity_And_Desk_Task_Ice`):** Pos `(+2.10, 1.55, -0.75)`, Color `#E0F4FF`, Energy `1.45`, Range `3.8m`.
   - **`OmniLight3D` (`Vanity_UV_Sterilizer_Accent`):** Pos `(+2.35, 1.35, -1.45)`, Color `#7B5CFF`, Energy `1.10`, Range `2.2m`.
   - **`OmniLight3D` (`Locker_And_Climate_Amber_Safety`):** Pos `(+1.85, 0.95, +2.10)`, Color `#FF9500`, Energy `1.15`, Range `3.2m`.

---

## 4. Standardized 4-Angle 1080p Beauty Camera Presets (`Room 01`)

1. **`cam_01_overview_south_entry`:** Pos `(0.00, 1.75, +3.10)` looking at `(0.00, 1.05, -1.20)`, `FOV = 58°` — Wide heroic view from the entry airlock looking across the bunk bays, footlocker, East utility wall, and North O'Neill Cylinder panoramic window.
2. **`cam_02_west_bunks_and_footlocker`:** Pos `(+1.95, 1.52, +0.25)` looking at `(-2.10, 1.00, -0.85)`, `FOV = 52°` — Frames `bunk_winner_01_orbital_viewport` (with Deep Space visible through its translucent octagonal window), `bunk_winner_03_hex_hive_stack`, and `footlocker_winner_01` at the berth foot.
3. **`cam_03_east_aegis_utility_wall`:** Pos `(-1.75, 1.48, +0.20)` looking at `(+2.45, 1.08, +0.15)`, `FOV = 52°` — Showcases the unified Aegis-7 split-bay triad side-by-side on the East bulkhead: `vanity_winner_01`, `walldesk_winner_01`, and `locker_winner_01` (with the 3D EVA suit glowing inside).
4. **`cam_04_north_viewport_and_climate`:** Pos `(-1.40, 1.55, -1.60)` looking at `(+1.35, 1.15, +2.60)`, `FOV = 54°` — Reverse angle highlighting the South entry bulkhead, `climate_winner_01` life-support & O2 station, and `locker_winner_01`.
