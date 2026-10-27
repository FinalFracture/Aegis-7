# Room 06 — Hydroponics & Bio-Air Scrubber Dome: Aegis-7 Architectural Layout & Godot 4 Lighting Spec
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Target Godot Scene:** `/workspace/game-project/godot/scenes/rooms/room_06_hydroponics_bay.tscn`  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)

---

## 1. Room 06 Architectural Envelope (`8.0m W × 9.0m D × 3.6m H`)

- **World Origin:** Center of the Hydroponics Dome deck at `(0.0, 0.0, 0.0)` (`X: -4.00..+4.00, Z: -4.50..+4.50, Y: 0.00..3.60`).
- **Signature Aegis-7 Bio-Dome Shell Features (`room_06_shell.glb`):**
  - **5 Repeating 45° Chamfered Octagonal Dome Ribs** (`Z = -4.2m, -2.1m, 0.0m, +2.1m, +4.2m`) in dark anodized gunmetal titanium (`titanium_gunmetal_hull.png`, `#1A1E24`) with higher `3.60m` vaulted ceiling clearance, overhead brushed-steel irrigation & misting conduit pipes, and alternating **UV-Violet (`#7B5CFF`) and Orbital Cyan (`#00E5FF`) ceiling cove strips**.
  - **North & Overhead Slanted Panoramic Solarium Viewports (`Z = -4.45m, Y = 0.85m to 3.15m`):** Wide 3-bay chamfered octagonal window wall + upper 45° skylight panels glazed with `glass_hydro_cylinder_translucent.png` (`alphaMode: "BLEND"`, `alpha ~ 0.18`), backed at `Z = -5.10m` by an expansive curved **`vista_oneill_cylinder_interior.png`** backdrop showing the 800m × 400m O'Neill Cylinder agricultural valleys and axial sun!
  - **Central Nutrient & Botanical Analysis Island (`hydro_sample_bench.glb`):**
    - Sculpted `2.10m W × 1.05m D × 0.88m H` chamfered aerospace-white & gunmetal island workbench positioned in the center of the dome, featuring a recessed illuminated seedling propagation tray (`foliage_aeroponic_herbs.png`), 3D borosilicate sample flasks, microscope gantry, and a front `oled_hydro_bioscrubber.png` telemetry panel.

---

## 2. Exact Asset Placement Blueprint (`room_06_hydroponics_bay.tscn`)

| Slot | Asset File (`/workspace/game-project/assets/glb/winners/`) | Location | Position `(x, y, z)` | `rotation_y_deg` | Role in Scene |
|------|------------------------------------------------------------|----------|----------------------|------------------|---------------|
| **Hero Aeroponic Tower #1 (NW)** | `hydro_column_winner_01_...glb` *(Winner from `hydro_round1`)* | **West Botanical Aisle — North** | `(-2.85, 0.00, -1.85)` | `+90.0°` | First Vertical Translucent Aeroponic Planter & Bio-Scrubber Tower facing East (`+X`). |
| **Hero Aeroponic Tower #2 (SW)** | `hydro_column_winner_01_...glb` | **West Botanical Aisle — South** | `(-2.85, 0.00, +0.65)` | `+90.0°` | Second West-bank Aeroponic Tower forming a glowing living green wall. |
| **Hero Aeroponic Tower #3 (NE)** | `hydro_column_winner_01_...glb` | **East Botanical Aisle — North** | `(+2.85, 0.00, -1.85)` | `-90.0°` | Third Aeroponic Planter & Bio-Scrubber Tower on the East aisle facing West (`-X`). |
| **Hero Aeroponic Tower #4 (SE)** | `hydro_column_winner_01_...glb` | **East Botanical Aisle — South** | `(+2.85, 0.00, +0.65)` | `-90.0°` | Fourth Aeroponic Tower completing the 4-tower photosynthetic scrubber array! |
| **Center Botanical Analysis Island** | `hydro_sample_bench.glb` *(or procedural island assembly)* | **Center Dome Research Island** | `(0.00, 0.00, -0.85)` | `0.0°` | Central seedling propagation & nutrient titration bench framed against the North O'Neill Cylinder viewport. |
| **Botanist Comms & Log Workstation** | `walldesk_winner_01_split_comms_station.glb` | **East Wall — South Lab Bay** | `(+3.35, 0.00, +2.65)` | `-90.0°` | Chief Botanist's fold-down desk, OLED terminal & data-slate station. |
| **Bio-Wash & Decontamination Vanity** | `vanity_winner_01_dual_zone_grooming.glb` | **West Wall — South Lab Bay** | `(-3.38, 0.00, +2.65)` | `+90.0°` | Sonic hand-wash basin & UV-sterilizer station for handling sterile cultures. |
| **Dome Atmospheric & O2 Panel** | `climate_winner_01_split_env_o2_station.glb` | **South Bulkhead — East Pillar** | `(+2.15, 0.00, +4.18)` | `180.0°` | Primary O2/CO2 exchange telemetry & emergency breather station. |
| **Seed & Nutrient Cargo Chest** | `footlocker_winner_01_split_cargo_trunk.glb` | **South Bulkhead — West Alcove** | `(-2.15, 0.00, +3.85)` | `180.0°` | Staged seed-vault & nutrient cartridge crate. |
| **South Entry Sector Airlock** | `corridor_door_winner_01_...glb` | **South Bulkhead Center (`+Z`)** | `(0.00, 0.00, +4.20)` | `180.0°` | Pressurized bulkhead portal connecting the Hydroponics Dome to `Room 02 — Transit Corridor`. |

---

## 3. Godot 4 Lighting Rig & Camera Presets (`room_06_hydroponics_bay.tscn`)

1. **Lighting Rig:**
   - **North Solarium Cylinder Sunlight (`DirectionalLight3D`):** Color `#D4F2FF`, Energy `0.95`, `shadow_enabled = true`.
   - **West & East Aeroponic Grow-Light Wash (`OmniLight3D` × 4 at `(±2.15, 1.85, -1.85)` & `(±2.15, 1.85, +0.65)`):** Alternating UV-Violet `#7B5CFF` (Energy `1.35`) and Surgical Daylight `#E0F4FF` (Energy `1.40`), Range `4.5m`.
   - **Center Island & Ceiling Cyan Cove (`OmniLight3D` × 2 at `(0.0, 2.95, -0.85)` & `(0.0, 2.95, +2.10)`):** Color `#00E5FF`, Energy `1.30`, Range `5.5m`.
2. **Standardized 3-Angle 1080p Beauty Camera Presets:**
   - **`cam_01_hydro_dome_symmetrical_overview`:** Pos `(0.00, 1.95, +3.65)` looking at `(0.00, 1.25, -2.50)`, `FOV = 58°` — Sweeping wide shot down the luminous 4-tower aeroponic colonnade toward the Center Botanical Analysis Island and North O'Neill Cylinder panoramic viewport!
   - **`cam_02_west_aeroponic_towers_and_island`:** Pos `(+2.15, 1.60, +1.25)` looking at `(-2.55, 1.25, -1.25)`, `FOV = 52°` — Close 3/4 view of the West `hydro_column_winner_01` towers (showing the 3D emerald foliage inside the translucent borosilicate columns and the cyan bioreactor tubes) plus the Center Analysis Island.
   - **`cam_03_east_towers_and_botanist_station`:** Pos `(-2.10, 1.55, -0.65)` looking at `(+2.85, 1.20, +0.85)`, `FOV = 52°` — Highlights the East Aeroponic Towers and the South-East Botanist Comms Workstation.
