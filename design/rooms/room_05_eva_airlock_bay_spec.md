# Room 05 — EVA Prep & Airlock Staging Bay: Aegis-7 Architectural Layout & Godot 4 Lighting Spec
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Target Godot Scene:** `/workspace/game-project/godot/scenes/rooms/room_05_eva_airlock_bay.tscn`  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)

---

## 1. Room 05 Architectural Envelope (`7.5m W × 8.5m D × 3.4m H`)

- **World Origin:** Center of the EVA Staging Bay deck at `(0.0, 0.0, 0.0)` (`X: -3.75..+3.75, Z: -4.25..+4.25, Y: 0.00..3.40`).
- **Signature Aegis-7 Shell Features (`room_05_shell.glb`):**
  - **5 Repeating 45° Chamfered Octagonal Titanium Ribs** (`Z = -4.0m, -2.0m, 0.0m, +2.0m, +4.0m`) in dark anodized gunmetal titanium (`titanium_gunmetal_hull.png`, `#1A1E24`) with overhead machined-steel suit-handling monorail tracks (`Y = 3.05m`) and recessed amber (`#FF9500`) + cyan (`#00E5FF`) cycling beacons.
  - **Heavy Mag-Boot Charging Deck Grates:** Carbon-slate & brushed-steel floor grating along the West and East suit-donning lanes (`X = ±2.10m`) with recessed glowing amber (`#FF9500`) guide strips leading directly to the North Decompression Chamber.
  - **North Outer-Hull Deep-Space Observation Windows (`Z = -4.20m` flanking the Decompression Chamber at `X = ±2.35m`):** Twin octagonal translucent viewports (`glass_eva_airlock_translucent.png`, `alphaMode: "BLEND"`, `alpha ~ 0.18`) backed at `Z = -4.85m` by **`vista_deep_space.png`** so crew prepping for spacewalks look directly out at the orbital ring and deep-space nebula!
  - **Auxiliary Center Donning Bench (`eva_suit_prep_bench.glb`):** Low-profile `2.20m W × 0.85m D × 0.52m H` chamfered titanium & charcoal-flightpad crew suit-donning bench with center tool/tether rack and under-seat amber floor glow positioned in the center aisle.

---

## 2. Exact Asset Placement Blueprint (`room_05_eva_airlock_bay.tscn`)

| Slot | Asset File (`/workspace/game-project/assets/glb/winners/`) | Location | Position `(x, y, z)` | `rotation_y_deg` | Role in Scene |
|------|------------------------------------------------------------|----------|----------------------|------------------|---------------|
| **Hero Outer-Hull Decompression Chamber** | `eva_chamber_winner_01_...glb` *(Winner from `eva_round1`)* | **North Bulkhead Centerpiece (`-Z`)** | `(0.00, 0.00, -3.35)` | `0.0°` | Primary Outer-Hull Decompression Airlock & Umbilical Recharge Gantry facing South (`+Z`). |
| **West EVA Suit Locker #1 (North)** | `locker_winner_01_dual_bay_bulkhead.glb` | **West Wall — North Bay** | `(-3.25, 0.00, -1.65)` | `+90.0°` | Locked Dual-Bay EVA Suit & Kit Locker facing East (`+X`). |
| **West EVA Suit Locker #2 (South)** | `locker_winner_01_dual_bay_bulkhead.glb` | **West Wall — South Bay** | `(-3.25, 0.00, +0.25)` | `+90.0°` | Second West-bank EVA Suit Locker forming a continuous 2-suit prep bank. |
| **East EVA Suit Locker #3 (North)** | `locker_winner_01_dual_bay_bulkhead.glb` | **East Wall — North Bay** | `(+3.25, 0.00, -1.65)` | `-90.0°` | Locked Dual-Bay EVA Suit Locker on the East bulkhead facing West (`-X`). |
| **East EVA Suit Locker #4 (South)** | `locker_winner_01_dual_bay_bulkhead.glb` | **East Wall — South Bay** | `(+3.25, 0.00, +0.25)` | `-90.0°` | Fourth Dual-Bay EVA Suit Locker completing the 4-crew EVA staging squadron! |
| **Center Suit-Donning Bench** | `eva_suit_prep_bench.glb` *(or dual `footlocker_winner_01` back-to-back)* | **Center Staging Island** | `(0.00, 0.00, -0.65)` | `0.0°` | Central low-profile donning bench & mag-boot step platform keeping sightlines open to the North Chamber. |
| **EVA Tool & Tether Cargo Chest #1** | `footlocker_winner_01_split_cargo_trunk.glb` | **West Wall — South-West Staging** | `(-3.15, 0.00, +2.25)` | `+90.0°` | Open translucent cargo chest holding spare Li-S suit batteries & EVA tools. |
| **EVA Log & Check-Out Workstation** | `walldesk_winner_01_split_comms_station.glb` | **East Wall — South-East Staging** | `(+3.25, 0.00, +2.25)` | `-90.0°` | EVA Quartermaster flight-plan & umbilical checkout terminal. |
| **Bay Atmospheric & Emergency O2 Panel** | `climate_winner_01_split_env_o2_station.glb` *(or `climate_winner_01_split_o2_panel.glb`)* | **South Bulkhead — West Pillar** | `(-1.95, 0.00, +3.95)` | `180.0°` | Staging bay pressure equalizer & emergency breather-mask station. |
| **South Inner-Hull Pressure Hatch** | `corridor_door_winner_01_...glb` | **South Bulkhead Center (`+Z`)** | `(0.00, 0.00, +3.95)` | `180.0°` | Inner sector blast hatch connecting the EVA Staging Bay to `Room 02 — Transit Corridor`. |

---

## 3. Godot 4 Lighting Rig & Camera Presets (`room_05_eva_airlock_bay.tscn`)

1. **Lighting Rig:**
   - **Decompression Chamber Cyan & Amber Cycling Lights (`OmniLight3D` × 2 at `(0.0, 2.35, -2.50)` & `(0.0, 0.45, -2.50)`):** Colors `#00E5FF` (Energy `1.55`) and `#FF9500` (Energy `1.35`).
   - **West & East Suit Locker Bank Wash (`OmniLight3D` × 2 at `(±2.35, 2.25, -0.70)`):** Color `#E0F4FF`, Energy `1.35`, Range `5.0m` (illuminates the 4 translucent EVA suit lockers and gold helmet visors).
   - **Overhead Monorail Cyan Cove Lights (`OmniLight3D` × 2 at `(0.0, 3.05, ±1.20)`):** Color `#00E5FF`, Energy `1.15`, Range `6.0m`.
2. **Standardized 3-Angle 1080p Beauty Camera Presets:**
   - **`cam_01_eva_bay_symmetrical_overview`:** Pos `(0.00, 1.85, +3.45)` looking at `(0.00, 1.20, -3.35)`, `FOV = 58°` — Iconic symmetrical spacewalk staging shot framing the centerpiece Outer-Hull Decompression Chamber & Deep Space viewports at the North end, flanked by the West and East banks of Dual-Bay EVA Suit Lockers!
   - **`cam_02_decompression_chamber_and_west_lockers`:** Pos `(+2.15, 1.55, +0.85)` looking at `(-1.45, 1.20, -2.65)`, `FOV = 52°` — Close 3/4 view of the Decompression Chamber's translucent door, umbilical recharge gantry, UV helmet test hood, and the West EVA Suit Locker bank.
   - **`cam_03_east_lockers_and_checkout_station`:** Pos `(-2.05, 1.50, -0.45)` looking at `(+3.10, 1.15, +0.45)`, `FOV = 52°` — Highlights the East EVA Suit Locker squadron and EVA Quartermaster checkout desk.
