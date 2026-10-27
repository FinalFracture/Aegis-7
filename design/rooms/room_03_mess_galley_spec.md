# Room 03 — Crew Mess Hall & Synthesizer Galley: Aegis-7 Architectural Layout & Godot 4 Lighting Spec
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Target Godot Scene:** `/workspace/game-project/godot/scenes/rooms/room_03_mess_galley.tscn`  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)

---

## 1. Room 03 Architectural Envelope (`7.0m W × 8.0m D × 3.2m H`)

- **World Origin:** Center of the mess hall deck at `(0.0, 0.0, 0.0)` (`X: -3.50..+3.50, Z: -4.00..+4.00, Y: 0.00..3.20`).
- **Signature Aegis-7 Shell Features:**
  - **5 Repeating 45° Chamfered Octagonal Titanium Ribs** (`Z = -3.8m, -1.9m, 0.0m, +1.9m, +3.8m`) in dark anodized gunmetal titanium (`titanium_gunmetal_hull.png`, `#1A1E24`) with matte aerospace-white (`composite_aerospace_white.png`, `#D8DEE6`) coffered ceiling panels and recessed cyan (`#00E5FF`) ceiling cove strips.
  - **North Panoramic Cylinder Viewport Wall (`Z = -3.95m, X = -2.6m to +2.6m, Y = 0.90m to 2.55m`):** 3-bay chamfered translucent observation window (`glass_synth_chamber_translucent.png`, `alphaMode: "BLEND"`, `alpha ~ 0.18`) looking out onto a wide curved exterior backdrop (`Z = -4.60m`) mapped with **`vista_oneill_cylinder_interior.png`** so crew dine overlooking the curving 800m × 400m O'Neill Cylinder biosphere!
  - **Custom Companion Mess Booth & Cantilevered Table (`mess_dining_booth.glb`):**
    - Sculpted cantilevered brushed-steel (`steel_machined_gantry.png`) and matte aerospace-white (`composite_aerospace_white.png`) dining table (`1.80m W × 0.95m D × 0.76m H`) with recessed glowing cyan tray borders, 3D meal trays, and magnetic mugs, flanked by twin contoured orbital-navy & charcoal flightpad bench booths (`fabric_orbital_navy_pad.png` / `fabric_charcoal_flightpad.png`).

---

## 2. Exact Asset Placement Blueprint (`room_03_mess_galley.tscn`)

| Slot | Asset File | Location | Position `(x, y, z)` | `rotation_y_deg` | Role in Scene |
|------|------------|----------|----------------------|------------------|---------------|
| **Hero Galley Synthesizer #1** | `galley_synth_winner_01_...glb` *(Winner from `galley_round1`)* | **East Galley Counter Wall — North** | `(+2.85, 0.00, -1.25)` | `-90.0°` | Primary Ration & Beverage Synthesizer Bank facing West (`-X`) toward the dining booths. |
| **Hero Galley Synthesizer #2** | `galley_synth_winner_01_...glb` | **East Galley Counter Wall — South** | `(+2.85, 0.00, +1.25)` | `-90.0°` | Secondary Ration & Hydration Synthesizer Bank forming a continuous `4.0m` galley counter line! |
| **Dining Booth Set #1 (North)** | `mess_dining_booth.glb` *(or procedural booth assembly)* | **West Observation Dining Zone — North** | `(-1.55, 0.00, -1.65)` | `0.0°` | 4-person cantilevered dining booth right beside the North panoramic O'Neill Cylinder viewport. |
| **Dining Booth Set #2 (South)** | `mess_dining_booth.glb` | **West Observation Dining Zone — South** | `(-1.55, 0.00, +1.45)` | `0.0°` | Second 4-person cantilevered dining booth on the West deck. |
| **Mess Hall Climate & O2 Panel** | `climate_winner_01_split_env_o2_station.glb` | **West Wall — Center Pillar** | `(-3.28, 0.00, -0.10)` | `+90.0°` | Environmental scrubber & emergency breather station on the West bulkhead. |
| **South Entry Sector Airlock** | `corridor_door_winner_01_...glb` | **South Bulkhead (`+Z`)** | `(0.00, 0.00, +3.75)` | `180.0°` | Pressurized bulkhead portal connecting the Mess Hall to `Room 02 — Transit Corridor`. |
| **Supply Cargo Crate** | `footlocker_winner_01_split_cargo_trunk.glb` | **South-East Galley Storage Corner** | `(+2.35, 0.00, +3.15)` | `180.0°` | Staged ration/supply crate beside the galley counter. |

---

## 3. Godot 4 Lighting Rig & Camera Presets (`room_03_mess_galley.tscn`)

1. **Lighting Rig:**
   - **North Viewport Cylinder Daylight (`DirectionalLight3D`):** Color `#C8EAFF`, Energy `0.90`, `shadow_enabled = true`.
   - **Ceiling Cyan Cove Lights (`OmniLight3D` × 2 at `(0.0, 2.88, ±1.65)`):** Color `#00E5FF`, Energy `1.20`, Range `6.0m`.
   - **Galley Counter Warm Amber & UV Herb Accents (`OmniLight3D` × 2 at `(+2.25, 1.45, ±1.25)`):** Color `#FF9500` / `#7B5CFF`, Energy `1.35`, Range `3.8m`.
   - **Dining Table Pendant Task Spots (`OmniLight3D` × 2 at `(-1.55, 1.85, -1.65)` & `(-1.55, 1.85, +1.45)`):** Color `#E0F4FF`, Energy `1.35`, Range `3.5m`.
2. **Standardized 3-Angle 1080p Beauty Camera Presets:**
   - **`cam_01_mess_hall_overview`:** Pos `(0.00, 1.85, +3.35)` looking at `(0.00, 1.10, -1.80)`, `FOV = 58°` — Wide heroic view showing the East twin Synthesizer Galley Bank, West cantilevered dining booths, and North panoramic O'Neill Cylinder viewport.
   - **`cam_02_galley_synthesizer_line`:** Pos `(-0.95, 1.48, +0.20)` looking at `(+2.75, 1.10, -0.45)`, `FOV = 50°` — Hero shot of the dual Ration & Beverage Synthesizer Banks with glowing OLED panels, translucent synthesis ovens, and aeroponic herb troughs.
   - **`cam_03_dining_booths_and_viewport`:** Pos `(+1.85, 1.52, +1.60)` looking at `(-1.65, 1.05, -2.20)`, `FOV = 54°` — Frames the cantilevered dining booths against the glowing 800m × 400m O'Neill Cylinder vista.
