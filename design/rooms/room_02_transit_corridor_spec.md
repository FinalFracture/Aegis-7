# Room 02 — Orbital Sector Transit Corridor & Airlock Hub: Aegis-7 Architectural Layout & Godot 4 Lighting Spec
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Target Godot Scene:** `/workspace/game-project/godot/scenes/rooms/room_02_transit_corridor.tscn`  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)  
**Target Teams:** Rook (Modular Corridor Rib/Window Bay & Airlock Hatch Geometry) & Gage (Godot 4 Scene Assembly, Lighting & Multi-Angle 1080p Beauty Renders)

---

## 1. Room 02 Architectural Envelope (`3.6m W × 12.0m D × 3.2m H`)

- **World Origin:** Center of the corridor deck at `(0.0, 0.0, 0.0)`
  - **West Observation Gallery Wall (`-X`):** `X = -1.80m` (continuous 4-bay translucent panoramic window wall overlooking the 800m × 400m O'Neill Cylinder interior!)
  - **East Stateroom Bulkhead Wall (`+X`):** `X = +1.80m` (recessed cabin entry alcoves leading to Room 01 Sleeping Quarters + flush life-support stations)
  - **North Sector Bulkhead Portal (`-Z`):** `Z = -6.00m`
  - **South Sector Bulkhead Portal (`+Z`):** `Z = +6.00m`
  - **Deck Floor (`Y = 0.00m`)** to **Overhead Ceiling Crown (`Y = 3.20m`)**
- **Signature "Aegis-7 Standard" Structural Elements:**
  1. **7 Repeating 45° Chamfered Octagonal Titanium Ribs (`Z = -6.0m, -4.0m, -2.0m, 0.0m, +2.0m, +4.0m, +6.0m`):**
     - Dark anodized gunmetal titanium (`titanium_gunmetal_hull.png`, `#1A1E24`) ring ribs with `0.50m × 0.50m` 45° upper and lower corner chamfers, brushed machined-steel (`steel_machined_gantry.png`, `#88929E`) handrail grab-bars along `Y = 1.05m`, and matte aerospace-white (`composite_aerospace_white.png`, `#D8DEE6`) upper ceiling coffers.
  2. **West Continuous Translucent Observation Window Gallery (`X = -1.78m, Z = -5.5m to +5.5m, Y = 0.85m to 2.45m`):**
     - 6 faceted/chamfered panoramic window bays between the structural ribs, glazed with **`alphaMode: "BLEND"` translucent armored glass (`glass_airlock_viewport_translucent.png`, `alpha ~ 0.19`)** and backed at `X = -2.40m` by a full-length emissive/unshaded exterior backdrop (`13.0m × 4.5m`) mapped with **`vista_oneill_cylinder_interior.png`**.
  3. **Composite Deck Grating & Recessed Guide Strips:**
     - Carbon-slate (`carbon_slate_frame.png`, `#282E38`) center walkway deck flanked by twin continuous **recessed Circadian Amber (`#FF9500`) floor guide strips** at `X = ±0.95m` and overhead **Orbital Cyan (`#00E5FF`) ceiling cove strips** at `X = ±1.10m, Y = 2.98m`.

---

## 2. Exact Asset Placement Blueprint (`room_02_transit_corridor.tscn`)

| Slot | Asset File (`/workspace/game-project/assets/glb/winners/`) | Location | Position `(x, y, z)` | `rotation_y_deg` | Role in Scene |
|------|------------------------------------------------------------|----------|----------------------|------------------|---------------|
| **North Main Sector Airlock** | `corridor_door_winner_01_...glb` *(Hero Winner from `corridor_round1`)* | **North End (`-Z`)** | `(0.00, 0.00, -5.65)` | `0.0°` | Primary pressurized sector bulkhead checkpoint facing South (`+Z`) down the corridor. |
| **South Main Sector Airlock** | `corridor_door_winner_01_...glb` | **South End (`+Z`)** | `(0.00, 0.00, +5.65)` | `180.0°` | Opposing pressurized sector bulkhead portal facing North (`-Z`). |
| **Cabin 01 Entry Portal** | `corridor_door_winner_01_...glb` *(scaled `0.85×` width or flush cabin hatch)* | **East Wall — North Bay** | `(+1.72, 0.00, -2.00)` | `-90.0°` | Stateroom branch airlock leading into `Room 01 — Crew Sleeping Quarters`. |
| **Corridor Life-Support & O2 Panel #1** | `climate_winner_01_...glb` *(from `climate_round1`)* | **East Wall — Center Pillar** | `(+1.62, 0.00, +0.00)` | `-90.0°` | Sector environmental telemetry & emergency breather-mask station at midpoint. |
| **Corridor EVA Locker Alcove** | `locker_winner_01_dual_bay_bulkhead.glb` | **East Wall — South Emergency Bay** | `(+1.52, 0.00, +3.00)` | `-90.0°` | Recessed corridor emergency EVA suit & damage-control kit station. |
| **Staged Logistics Cargo Crate** | `footlocker_winner_01_split_cargo_trunk.glb` | **East Deck Side Alcove** | `(+1.15, 0.00, -4.15)` | `-90.0°` | Locked onto magnetic floor skids beside the North checkpoint. |

---

## 3. Godot 4 Lighting Rig & Camera Presets (`room_02_transit_corridor.tscn`)

1. **Lighting Rig:**
   - **Axial Cylinder Sunlight (`DirectionalLight3D`):** Angles in from `-X` through the 6 West translucent panoramic windows (`Color: #BCE8FF`, `Energy: 0.95`, `shadow_enabled = true`), casting rhythmic chamfered rib shadows across the carbon-slate deck!
   - **Repeating Ceiling Cyan Cove Lights (`OmniLight3D` × 3 at `Z = -3.5m, 0.0m, +3.5m, Y = 2.85m`):** Color `#00E5FF`, Energy `1.20`, Range `5.5m`.
   - **North & South Airlock Cycling Beacons (`OmniLight3D` × 2 at `Z = ±5.1m, Y = 2.35m`):** Color `#FF9500`, Energy `1.45`, Range `4.2m`.
2. **Standardized 3-Angle 1080p Beauty Camera Presets:**
   - **`cam_01_axial_corridor_perspective`:** Pos `(0.25, 1.55, +4.65)` looking at `(-0.15, 1.35, -5.65)`, `FOV = 54°` — Iconic one-point hard sci-fi corridor shot showing the repeating 45° octagonal ribs, West translucent window gallery overlooking the O'Neill Cylinder, East life-support/EVA stations, and the North Pressurized Bulkhead Airlock Hatch at the focal point.
   - **`cam_02_window_gallery_and_east_bulkhead`:** Pos `(-1.15, 1.48, +1.85)` looking at `(+1.55, 1.25, -1.50)`, `FOV = 52°` — Frames the East stateroom entry hatch, `climate_winner_01` O2 station, and `locker_winner_01`.
   - **`cam_03_airlock_checkpoint_closeup`:** Pos `(+0.85, 1.42, -2.65)` looking at `(0.00, 1.32, -5.65)`, `FOV = 48°` — Hero closeup of the North Pressurized Bulkhead Airlock Hatch, parted blast doors with interlocking dog teeth, translucent inspection windows, and West O'Neill Cylinder vista.
