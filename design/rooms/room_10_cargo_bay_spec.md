# Room 10 — Modular Cargo Hold & Logistics Drone Bay: Aegis-7 Architectural Layout & Godot 4 Lighting Spec
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Target Godot Scene:** `/workspace/game-project/godot/scenes/rooms/room_10_cargo_bay.tscn`  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)

---

## 1. Room 10 Architectural Envelope (`9.0m W × 10.0m D × 4.0m H`)

- **World Origin:** Center of the Cargo Bay deck at `(0.0, 0.0, 0.0)` (`X: -4.50..+4.50, Z: -5.00..+5.00, Y: 0.00..4.00`).
- **Signature Aegis-7 Logistics Bay Features (`room_10_shell.glb`):**
  - **5 Heavy 45° Chamfered Octagonal Titanium Ribs** (`Z = -4.6m, -2.3m, 0.0m, +2.3m, +4.6m`) in dark anodized gunmetal titanium (`titanium_gunmetal_hull.png`, `#1A1E24`) with `4.00m` high-bay ceiling clearance, **twin overhead brushed-steel magnetic bridge-crane rails (`Y = 3.55m`)**, and recessed **Amber Hazard (`#FF9500`) & Orbital Cyan (`#00E5FF`) loading-zone floor guide strips**.
  - **Dual Location-Aware Logistics Observation Viewports (`alphaMode: "BLEND"`, `alpha ~ 0.18`):**
    1. **North Zero-G Docking Hub & Cylinder Viewport (`Z = -4.95m, X = -3.2m to +3.2m, Y = 1.15m to 3.35m`):** Wide 3-bay chamfered cargo observation window glazed with `glass_cargo_bay_translucent.png`, backed at `Z = -5.65m` by **`vista_oneill_cylinder_interior.png`** overlooking the central axial zero-G cargo transfer hub!
    2. **West Outer-Hull Freighter Approach Window (`X = -4.45m, Z = -3.2m to +0.8m`):** Backed at `X = -5.15m` by **`vista_deep_space.png`** showing the exterior orbital freighter ring and starfield!
  - **Center Magnetic Pallet Deck (`cargo_mag_pallet_deck.glb`):** Low-profile `2.60m W × 1.80m D × 0.14m H` chamfered carbon-slate & brushed-steel floor locking grid in the center loading lane with glowing amber corner lock beacons, holding 2 to 4 arrayed `footlocker_winner_01_split_cargo_trunk.glb` modular cargo chests!

---

## 2. Exact Asset Placement Blueprint (`room_10_cargo_bay.tscn`)

| Slot | Asset File (`/workspace/game-project/assets/glb/winners/`) | Location | Position `(x, y, z)` | `rotation_y_deg` | Role in Scene |
|------|------------------------------------------------------------|----------|----------------------|------------------|---------------|
| **Hero Cargo & Drone Gantry #1 (West)** | `cargo_gantry_winner_01_...glb` *(Winner from `cargo_round1`)* | **West High-Bay Rack — North** | `(-3.25, 0.00, -1.65)` | `+90.0°` | Primary 2×2 Interlocking Cargo Container Rack & Autonomous Drone Dock facing East (`+X`). |
| **Hero Cargo & Drone Gantry #2 (East)** | `cargo_gantry_winner_01_...glb` | **East High-Bay Rack — North** | `(+3.25, 0.00, -1.65)` | `-90.0°` | Opposing 2×2 Interlocking Cargo Container Rack & Drone Dock facing West (`-X`), forming a monumental logistics canyon! |
| **Staged Modular Cargo Trunk #1 (NW Pallet)** | `footlocker_winner_01_split_cargo_trunk.glb` | **Center Magnetic Pallet — North-West** | `(-0.70, 0.12, -1.25)` | `0.0°` | Locked Aegis-7 Split Cargo Trunk clamped onto the center magnetic pallet deck. |
| **Staged Modular Cargo Trunk #2 (NE Pallet)** | `footlocker_winner_01_split_cargo_trunk.glb` | **Center Magnetic Pallet — North-East** | `(+0.70, 0.12, -1.25)` | `0.0°` | Second Split Cargo Trunk paired side-by-side on the center pallet. |
| **Staged Modular Cargo Trunk #3 (SW Pallet)** | `footlocker_winner_01_split_cargo_trunk.glb` | **Center Magnetic Pallet — South-West** | `(-0.70, 0.12, -0.35)` | `180.0°` | Third Split Cargo Trunk completing the central 4-trunk logistics pallet! |
| **Staged Modular Cargo Trunk #4 (SE Pallet)** | `footlocker_winner_01_split_cargo_trunk.glb` | **Center Magnetic Pallet — South-East** | `(+0.70, 0.12, -0.35)` | `180.0°` | Fourth Split Cargo Trunk on the center pallet. |
| **Loadmaster Manifest Workstation** | `walldesk_winner_01_split_comms_station.glb` | **East Wall — South Logistics Office** | `(+3.85, 0.00, +1.85)` | `-90.0°` | Chief Loadmaster's RFID manifest & centrifuge mass-balance terminal. |
| **Cargo Handler EVA Suit Locker** | `locker_winner_01_dual_bay_bulkhead.glb` | **West Wall — South Handler Bay** | `(-3.82, 0.00, +1.85)` | `+90.0°` | Zero-G cargo handler EVA suit & magnetic-grapple kit locker. |
| **Bay Atmospheric & Emergency O2 Panel** | `climate_winner_01_split_env_o2_station.glb` *(or `climate_winner_01_split_o2_panel.glb`)* | **South Bulkhead — East Pillar** | `(+2.35, 0.00, +4.68)` | `180.0°` | Cargo hold pressure sensor & emergency breather-mask station. |
| **South Heavy Cargo Bulkhead Hatch** | `corridor_door_winner_01_...glb` | **South Bulkhead Center (`+Z`)** | `(0.00, 0.00, +4.65)` | `180.0°` | Pressurized bulkhead portal connecting the Cargo Hold to `Room 02 — Transit Corridor`. |

---

## 3. Godot 4 Lighting Rig & Camera Presets (`room_10_cargo_bay.tscn`)

1. **Lighting Rig:**
   - **Overhead Bridge-Crane High-Bay Floods (`OmniLight3D` × 2 at `(0.0, 3.45, -1.65)` & `(0.0, 3.45, +1.85)`):** Color `#E0F4FF`, Energy `1.45`, Range `6.5m`.
   - **West & East Gantry Drone/Container Cyan Glow (`OmniLight3D` × 2 at `(±2.45, 1.65, -1.65)`):** Color `#00E5FF`, Energy `1.45`, Range `4.8m`.
   - **Center Magnetic Pallet & Crane Amber Hazard Beacons (`OmniLight3D` × 2 at `(0.0, 0.85, -0.80)` & `(0.0, 2.85, +3.85)`):** Color `#FF9500`, Energy `1.35`, Range `4.5m`.
2. **Standardized 3-Angle 1080p Beauty Camera Presets:**
   - **`cam_01_cargo_bay_symmetrical_overview`:** Pos `(0.00, 2.15, +4.10)` looking at `(0.00, 1.30, -2.50)`, `FOV = 58°` — Commanding wide view down the high-bay cargo canyon showing the opposing West and East `cargo_gantry_winner_01` racks & docked drones, the central 4-trunk magnetic pallet, and the North O'Neill Cylinder docking viewport!
   - **`cam_02_west_gantry_drone_and_pallet`:** Pos `(+2.35, 1.70, +0.95)` looking at `(-2.85, 1.25, -1.55)`, `FOV = 52°` — Close 3/4 hero shot of the West Cargo Gantry's 2×2 translucent container matrix, docked 3D octo-thruster drone, and the center pallet of `footlocker_winner_01` trunks.
   - **`cam_03_east_gantry_and_loadmaster_station`:** Pos `(-2.25, 1.60, -0.45)` looking at `(+3.25, 1.25, +0.45)`, `FOV = 52°` — Highlights the East Cargo Gantry and the Chief Loadmaster's manifest workstation.
