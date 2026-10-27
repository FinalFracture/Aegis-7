# Room 07 — Habitat Command & Spin-Gravity Telemetry Bridge: Aegis-7 Architectural Layout & Godot 4 Lighting Spec
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Target Godot Scene:** `/workspace/game-project/godot/scenes/rooms/room_07_command_bridge.tscn`  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)

---

## 1. Room 07 Architectural Envelope (`8.5m W × 9.5m D × 3.6m H`)

- **World Origin:** Center of the Command Bridge deck at `(0.0, 0.0, 0.0)` (`X: -4.25..+4.25, Z: -4.75..+4.75, Y: 0.00..3.60`).
- **Signature Aegis-7 Bridge Shell Features (`room_07_shell.glb`):**
  - **5 Repeating 45° Chamfered Octagonal Titanium Bridge Ribs** (`Z = -4.4m, -2.2m, 0.0m, +2.2m, +4.4m`) in dark anodized gunmetal titanium (`titanium_gunmetal_hull.png`, `#1A1E24`) with forward-raked bridge window mullions, matte aerospace-white (`composite_aerospace_white.png`, `#D8DEE6`) overhead acoustic baffles, and recessed **Orbital Cyan (`#00E5FF`) and Circadian Amber (`#FF9500`) command deck guide strips**.
  - **Wrap-Around Dual-Vista Command Viewports (`alphaMode: "BLEND"`, `alpha ~ 0.18`):**
    1. **North Panoramic Cylinder Axis Viewport (`Z = -4.70m, X = -3.4m to +3.4m, Y = 0.85m to 3.05m`):** 5-pane trapezoidal bridge window glazed with `glass_bridge_holo_translucent.png`, backed at `Z = -5.40m` by **`vista_oneill_cylinder_interior.png`** looking straight down the 800m × 400m O'Neill Cylinder spin axis!
    2. **West Outer-Hull Deep-Space Navigation Window (`X = -4.20m, Z = -3.2m to +1.2m`):** Backed at `X = -4.85m` by **`vista_deep_space.png`** showing the exterior orbital ring, nebula, and starfield!

---

## 2. Exact Asset Placement Blueprint (`room_07_command_bridge.tscn`)

| Slot | Asset File (`/workspace/game-project/assets/glb/winners/`) | Location | Position `(x, y, z)` | `rotation_y_deg` | Role in Scene |
|------|------------------------------------------------------------|----------|----------------------|------------------|---------------|
| **Hero Holographic Bridge Console** | `bridge_console_winner_01_...glb` *(Winner from `bridge_round1`)* | **Center Command Deck Stage** | `(0.00, 0.00, -1.15)` | `0.0°` | Focal centerpiece of the Command Bridge with its floating 3D O'Neill Cylinder hologram framed against the North bridge window! |
| **Port Helm & Comms Station (NW)** | `walldesk_winner_01_split_comms_station.glb` | **West Bridge Wing — North** | `(-3.45, 0.00, -1.95)` | `+90.0°` | Port-side navigation & subspace comms officer console facing East (`+X`). |
| **Port Systems & Telemetry Desk (SW)** | `walldesk_winner_01_split_comms_station.glb` | **West Bridge Wing — South** | `(-3.45, 0.00, +0.85)` | `+90.0°` | Secondary port telemetry & orbital docking workstation. |
| **Starboard Spin-Gravity Station (NE)** | `walldesk_winner_01_split_comms_station.glb` | **East Bridge Wing — North** | `(+3.45, 0.00, -1.95)` | `-90.0°` | Starboard spin-gravity & solar-mirror alignment officer console facing West (`-X`). |
| **Starboard Sector Ops Desk (SE)** | `walldesk_winner_01_split_comms_station.glb` | **East Bridge Wing — South** | `(+3.45, 0.00, +0.85)` | `-90.0°` | Starboard habitat sector operations & security workstation. |
| **Bridge Officer Emergency EVA Locker** | `locker_winner_01_dual_bay_bulkhead.glb` | **East Wall — Aft Command Ready Bay** | `(+3.55, 0.00, +2.85)` | `-90.0°` | Commander's emergency pressure suit & flight kit locker on the aft bridge bulkhead. |
| **Bridge Environmental & O2 Panel** | `climate_winner_01_split_env_o2_station.glb` *(or `climate_winner_01_split_o2_panel.glb`)* | **West Wall — Aft Command Pillar** | `(-3.75, 0.00, +2.85)` | `+90.0°` | Bridge atmospheric pressure & emergency drop-mask station. |
| **Navigation Data & Emergency Vault** | `footlocker_winner_01_split_cargo_trunk.glb` | **South-West Aft Deck Alcove** | `(-2.25, 0.00, +3.95)` | `180.0°` | Armored flight-recorder & emergency beacon chest. |
| **South Armored Bridge Blast Hatch** | `corridor_door_winner_01_...glb` | **South Bulkhead Center (`+Z`)** | `(0.00, 0.00, +4.45)` | `180.0°` | High-security bi-parting blast hatch connecting the Command Bridge to `Room 02 — Transit Corridor`. |

---

## 3. Godot 4 Lighting Rig & Camera Presets (`room_07_command_bridge.tscn`)

1. **Lighting Rig:**
   - **Central Hologram Cyan Beacon (`OmniLight3D` at `(0.0, 1.85, -1.15)`):** Color `#00E5FF`, Energy `1.75`, Range `5.5m` (casts dramatic cyan holographic illumination across the bridge deck and commander chairs).
   - **Port & Starboard Wing Console Task Lights (`OmniLight3D` × 2 at `(±2.65, 2.15, -0.55)`):** Color `#E0F4FF`, Energy `1.25`, Range `4.5m`.
   - **Aft Bridge Tactical Amber Guide Glow (`OmniLight3D` at `(0.0, 2.55, +3.45)`):** Color `#FF9500`, Energy `1.25`, Range `4.2m`.
2. **Standardized 3-Angle 1080p Beauty Camera Presets:**
   - **`cam_01_bridge_command_overview`:** Pos `(0.00, 2.05, +3.85)` looking at `(0.00, 1.15, -2.50)`, `FOV = 58°` — Sweeping symmetrical bridge overview framing the centerpiece Holographic Cylinder Projection Table & Flight-Director Tower against the 5-pane North O'Neill Cylinder viewport, flanked by the Port and Starboard telemetry wings!
   - **`cam_02_holotable_and_port_navigation`:** Pos `(+2.35, 1.65, +0.95)` looking at `(-1.65, 1.10, -1.85)`, `FOV = 52°` — Close 3/4 hero shot of the floating 3D O'Neill Cylinder hologram, Flight-Director OLED array, and Port Deep-Space navigation wing.
   - **`cam_03_starboard_ops_and_aft_ready_bay`:** Pos `(-2.15, 1.55, -0.85)` looking at `(+3.15, 1.15, +1.25)`, `FOV = 52°` — Highlights the Starboard telemetry consoles, Bridge Officer EVA Suit Locker, and South Armored Blast Hatch.
