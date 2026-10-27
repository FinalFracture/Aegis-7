# Room 08 — Observation Lounge & Zero-G Recreation Deck: Aegis-7 Architectural Layout & Godot 4 Lighting Spec
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Target Godot Scene:** `/workspace/game-project/godot/scenes/rooms/room_08_observation_lounge.tscn`  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)

---

## 1. Room 08 Architectural Envelope (`8.0m W × 9.0m D × 3.6m H`)

- **World Origin:** Center of the Observation Lounge deck at `(0.0, 0.0, 0.0)` (`X: -4.00..+4.00, Z: -4.50..+4.50, Y: 0.00..3.60`).
- **Signature Aegis-7 Stargazer Shell Features (`room_08_shell.glb`):**
  - **5 Repeating 45° Chamfered Octagonal Titanium Ribs** (`Z = -4.2m, -2.1m, 0.0m, +2.1m, +4.2m`) in dark anodized gunmetal titanium (`titanium_gunmetal_hull.png`, `#1A1E24`) with vaulted acoustic ceiling baffles and recessed **UV-Violet (`#7B5CFF`), Orbital Cyan (`#00E5FF`), and Warm Circadian Amber (`#FF9500`) mood cove channels**.
  - **Floor-to-Ceiling Faceted Deep-Space Observation Dome (`Z = -4.45m, X = -3.5m to +3.5m, Y = 0.25m to 3.35m`):**
    - Monumental 5-facet floor-to-ceiling chamfered viewport wall + angled upper stargazer skylights glazed with `glass_lounge_bar_translucent.png` (`alphaMode: "BLEND"`, `alpha ~ 0.18`), backed at `Z = -5.20m` by a panoramic **`vista_deep_space.png`** skybox showing the cyan/indigo nebula, multi-magnitude starfield, and illuminated orbital ring!
  - **East Inner-Hull Cylinder Gallery Window (`X = +3.95m, Z = -2.2m to +1.8m`):** Secondary translucent observation window backed by **`vista_oneill_cylinder_interior.png`** so guests see both Deep Space to the North and the curving O'Neill Cylinder interior to the East!
  - **Central Sunken Viewing Pit & Holo-Table Set (`lounge_viewing_pit_set.glb`):**
    - `2.80m W × 2.40m D × 0.72m H` chamfered carbon-slate & orbital-navy conversation lounge grouping positioned directly in front of the North Deep-Space window: two curved low-G orbital-navy lounge sofas (`fabric_orbital_navy_pad.png`) flanking a low octagonal brushed-steel & translucent-glass holo-chess coffee table with recessed amber (`#FF9500`) step-down perimeter strips.

---

## 2. Exact Asset Placement Blueprint (`room_08_observation_lounge.tscn`)

| Slot | Asset File (`/workspace/game-project/assets/glb/winners/`) | Location | Position `(x, y, z)` | `rotation_y_deg` | Role in Scene |
|------|------------------------------------------------------------|----------|----------------------|------------------|---------------|
| **Hero Celestial Beverage Bar** | `lounge_bar_winner_01_...glb` *(Winner from `lounge_round1`)* | **East Lounge Zone — South-Center** | `(+2.45, 0.00, +1.35)` | `-90.0°` | Focal Ambient Zero-G Beverage Bar & Illuminated Decanter Tower facing West (`-X`) across the lounge! |
| **Observation Lounge Sleeper #1 (NW)** | `bunk_winner_04_observation_lounge.glb` | **West Stargazer Alcove — North** | `(-2.95, 0.00, -1.85)` | `+90.0°` | Locked R2 #09 Split-Level Daybed & Stargazer Pod facing East/North toward the Deep Space dome. |
| **Observation Lounge Sleeper #2 (SW)** | `bunk_winner_04_observation_lounge.glb` | **West Stargazer Alcove — South** | `(-2.95, 0.00, +0.95)` | `+90.0°` | Second Split-Level Stargazer Daybed on the West observation wall. |
| **Center Sunken Viewing Pit & Table** | `lounge_viewing_pit_set.glb` *(or procedural sofa/table pit)* | **North-Center Stargazer Pit** | `(0.00, 0.00, -1.95)` | `0.0°` | Low-profile conversation pit & holo-coffee table right in front of the floor-to-ceiling Deep Space viewport! |
| **Celestial Astrometry & Music Console** | `walldesk_winner_01_split_comms_station.glb` | **East Wall — North Gallery Bay** | `(+3.35, 0.00, -1.65)` | `-90.0°` | Telescope/astrometry chart terminal & ambient audio station. |
| **Lounge Refreshment & Wash Vanity** | `vanity_winner_01_dual_zone_grooming.glb` | **West Wall — Aft Service Alcove** | `(-3.38, 0.00, +2.95)` | `+90.0°` | Guest sonic hand-refreshment & UV glassware sterilizer station. |
| **Lounge Atmospheric & O2 Panel** | `climate_winner_01_split_env_o2_station.glb` *(or `climate_winner_01_split_o2_panel.glb`)* | **South Bulkhead — East Pillar** | `(+2.15, 0.00, +4.18)` | `180.0°` | Lounge circadian lighting & emergency breather-mask station. |
| **Recreation Gear & Game Chest** | `footlocker_winner_01_split_cargo_trunk.glb` | **South Bulkhead — West Alcove** | `(-2.05, 0.00, +3.85)` | `180.0°` | Staged zero-G recreation &光学 visor kit trunk. |
| **South Entry Sector Airlock** | `corridor_door_winner_01_...glb` | **South Bulkhead Center (`+Z`)** | `(0.00, 0.00, +4.20)` | `180.0°` | Pressurized bulkhead portal connecting the Observation Lounge to `Room 02 — Transit Corridor`. |

---

## 3. Godot 4 Lighting Rig & Camera Presets (`room_08_observation_lounge.tscn`)

1. **Lighting Rig:**
   - **North Deep-Space Nebula Backlight (`DirectionalLight3D` / `OmniLight3D` at `(0.0, 2.15, -3.85)`):** Color `#00E5FF`, Energy `1.45`, Range `6.5m` (streams cool cyan starlight through the floor-to-ceiling viewport across the viewing pit).
   - **Celestial Beverage Bar Warm Amber & UV-Violet Glow (`OmniLight3D` × 2 at `(+2.05, 1.55, +1.35)` & `(+2.45, 0.45, +1.35)`):** Colors `#7B5CFF` (Energy `1.40`) and `#FF9500` (Energy `1.35`), Range `4.2m`.
   - **West Stargazer Daybed Cove Lights (`OmniLight3D` × 2 at `(-2.35, 1.75, -1.85)` & `(-2.35, 1.75, +0.95)`):** Color `#FF9500` / `#00E5FF`, Energy `1.25`, Range `4.0m`.
2. **Standardized 3-Angle 1080p Beauty Camera Presets:**
   - **`cam_01_observation_lounge_overview`:** Pos `(0.00, 1.85, +3.55)` looking at `(0.00, 1.15, -2.85)`, `FOV = 58°` — Breathtaking wide view across the East Celestial Beverage Bar, West Stargazer Daybeds, and Center Viewing Pit toward the floor-to-ceiling Deep Space nebula & orbital ring viewport!
   - **`cam_02_celestial_bar_hero`:** Pos `(-1.25, 1.48, +0.65)` looking at `(+2.35, 1.05, +1.25)`, `FOV = 50°` — Hero closeup of the `lounge_bar_winner_01` Celestial Beverage Bar, glowing translucent decanter tower, zero-G bulb-glasses, and orbital-navy barstools.
   - **`cam_03_stargazer_daybeds_and_deep_space`:** Pos `(+2.15, 1.55, +0.85)` looking at `(-2.45, 1.05, -1.85)`, `FOV = 54°` — Frames the twin `bunk_winner_04_observation_lounge` stargazer pods and center viewing pit against the glowing Deep Space viewport.
