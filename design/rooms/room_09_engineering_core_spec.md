# Room 09 — Engineering & Life-Support Reactor Core: Aegis-7 Architectural Layout & Godot 4 Lighting Spec
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Target Godot Scene:** `/workspace/game-project/godot/scenes/rooms/room_09_engineering_core.tscn`  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)

---

## 1. Room 09 Architectural Envelope (`8.5m W × 9.5m D × 3.8m H`)

- **World Origin:** Center of the Engineering Core deck at `(0.0, 0.0, 0.0)` (`X: -4.25..+4.25, Z: -4.75..+4.75, Y: 0.00..3.80`).
- **Signature Aegis-7 Reactor Hall Features (`room_09_shell.glb`):**
  - **5 Heavy 45° Chamfered Octagonal Titanium Ribs** (`Z = -4.4m, -2.2m, 0.0m, +2.2m, +4.4m`) in dark anodized gunmetal titanium (`titanium_gunmetal_hull.png`, `#1A1E24`) with overhead swept cryo-coolant bus pipes (`steel_machined_gantry.png`, `#88929E`) and recessed **Orbital Cyan (`#00E5FF`) & High-Voltage Amber (`#FF9500`) bus-bar strips**.
  - **Grated Diagnostic Walkways & Sub-Floor Plasma Conduit Trench:** Carbon-slate & brushed-steel deck grates over a central recessed floor trench (`X = -1.2m..+1.2m`) glowing with `#00E5FF` cyan and `#FF9500` amber power conduits.
  - **North Outer-Hull Armored Radiator Viewport (`Z = -4.70m, X = -2.8m to +2.8m, Y = 1.05m to 3.05m`):** 3-bay chamfered radiation-shielded window glazed with `glass_reactor_shield_translucent.png` (`alphaMode: "BLEND"`, `alpha ~ 0.18`), backed at `Z = -5.40m` by **`vista_deep_space.png`** overlooking the deep-space nebula and orbital thermal radiator ring!
  - **Auxiliary Cryo-Coolant Bus Manifold (`engineering_coolant_manifold.glb`):** `2.10m W × 0.85m D × 2.20m H` companion manifold bank with 4 insulated aerospace-white `18.2 K` liquid-helium cylinders, brushed-steel cross-feed pipes, and signal-orange isolation handwheels.

---

## 2. Exact Asset Placement Blueprint (`room_09_engineering_core.tscn`)

| Slot | Asset File (`/workspace/game-project/assets/glb/winners/`) | Location | Position `(x, y, z)` | `rotation_y_deg` | Role in Scene |
|------|------------------------------------------------------------|----------|----------------------|------------------|---------------|
| **Hero Reactor Core Relay #1 (Primary)** | `reactor_core_winner_01_...glb` *(Winner from `engineering_round1`)* | **Center-North Primary Reactor Stage** | `(-1.45, 0.00, -2.25)` | `+15.0°` | Primary 4.85 GW Fusion/Spin-Drive Plasma Containment Column & Cryo Control Bay. |
| **Hero Reactor Core Relay #2 (Twin)** | `reactor_core_winner_01_...glb` | **Center-North Secondary Reactor Stage** | `(+1.45, 0.00, -2.25)` | `-15.0°` | Paired secondary Spin-Drive Plasma Relay forming a dramatic V-angled twin reactor core in front of the North Deep Space viewport! |
| **West Cryo-Coolant Bus Manifold** | `engineering_coolant_manifold.glb` *(or procedural coolant bank)* | **West Wall — North Coolant Bay** | `(-3.55, 0.00, -0.85)` | `+90.0°` | Auxiliary liquid-helium cryo-coolant manifold & pressure-relief bank. |
| **Chief Engineer Diagnostics Desk** | `walldesk_winner_01_split_comms_station.glb` | **East Wall — Center Engineering Bay** | `(+3.48, 0.00, +0.25)` | `-90.0°` | Chief Engineer's plasma harmonic & spin-drive telemetry workstation. |
| **Hazmat & Radiation EVA Suit Locker #1** | `locker_winner_01_dual_bay_bulkhead.glb` | **West Wall — South Hazmat Bay** | `(-3.45, 0.00, +1.95)` | `+90.0°` | Radiation-shielded EVA maintenance suit & umbilical kit locker. |
| **Reactor Hall Atmospheric & O2 Panel** | `climate_winner_01_split_env_o2_station.glb` *(or `climate_winner_01_split_o2_panel.glb`)* | **East Wall — South Safety Pillar** | `(+3.68, 0.00, +2.35)` | `-90.0°` | Emergency O2 breather-mask & coolant-leak scrubber station. |
| **Deuterium / Spare Parts Cargo Trunk** | `footlocker_winner_01_split_cargo_trunk.glb` | **Center-East Diagnostic Deck** | `(+2.15, 0.00, +2.45)` | `-90.0°` | Armored containment chest holding spare superconducting coils & fuel cartridges. |
| **South Armored Reactor Blast Hatch** | `corridor_door_winner_01_...glb` | **South Bulkhead Center (`+Z`)** | `(0.00, 0.00, +4.45)` | `180.0°` | Heavy radiation-shielded bulkhead airlock connecting Engineering to `Room 02 — Transit Corridor`. |

---

## 3. Godot 4 Lighting Rig & Camera Presets (`room_09_engineering_core.tscn`)

1. **Lighting Rig:**
   - **Twin Reactor Plasma Core Cyan Glow (`OmniLight3D` × 2 at `(±1.45, 1.55, -2.05)`):** Color `#00E5FF`, Energy `1.75`, Range `5.5m` (floods the reactor stage and grated walkways with intense cyan plasma light).
   - **Sub-Floor Conduit & SCRAM Amber Glow (`OmniLight3D` × 2 at `(0.0, 0.35, -0.50)` & `(0.0, 2.55, +3.65)`):** Color `#FF9500`, Energy `1.40`, Range `4.5m`.
   - **Moderator & Cryo UV-Violet Accent (`OmniLight3D` at `(0.0, 2.25, -2.25)`):** Color `#7B5CFF`, Energy `1.30`, Range `4.2m`.
2. **Standardized 3-Angle 1080p Beauty Camera Presets:**
   - **`cam_01_reactor_hall_symmetrical_overview`:** Pos `(0.00, 1.95, +3.85)` looking at `(0.00, 1.30, -2.45)`, `FOV = 58°` — Monumental wide view down the sub-floor plasma trench toward the twin V-angled Fusion/Spin-Drive Reactor Cores framed against the North Deep-Space viewport!
   - **`cam_02_reactor_core_and_chief_desk`:** Pos `(-2.25, 1.60, +1.15)` looking at `(+1.55, 1.25, -1.85)`, `FOV = 52°` — Close 3/4 hero shot of the Starboard Reactor Core's translucent plasma column, toroidal coils, D-He3 moderator rod bay, and Chief Engineer's workstation.
   - **`cam_03_west_coolant_and_hazmat_bay`:** Pos `(+2.25, 1.55, +0.45)` looking at `(-3.25, 1.20, +0.55)`, `FOV = 52°` — Frames the Port Reactor Core, West Cryo-Coolant Manifold, and Radiation EVA Suit Locker.
