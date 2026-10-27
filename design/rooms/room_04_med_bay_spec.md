# Room 04 — Med-Bay & Biomonitor Triage Suite: Aegis-7 Architectural Layout & Godot 4 Lighting Spec
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Deep-Space Habitat)  
**Target Godot Scene:** `/workspace/game-project/godot/scenes/rooms/room_04_med_bay.tscn`  
**Architectural Standard:** **Single-Architect Unified Style Bible ("Aegis-7 Standard")**  
**Author:** Sloane (Interior, Lighting & Texture Designer)

---

## 1. Room 04 Architectural Envelope (`6.5m W × 7.5m D × 3.2m H`)

- **World Origin:** Center of the Med-Bay deck at `(0.0, 0.0, 0.0)` (`X: -3.25..+3.25, Z: -3.75..+3.75, Y: 0.00..3.20`).
- **Signature Aegis-7 Surgical Shell Features:**
  - **5 Repeating 45° Chamfered Octagonal Ribs** in dark gunmetal titanium (`titanium_gunmetal_hull.png`, `#1A1E24`) paired with high-purity matte aerospace-white (`composite_aerospace_white.png`, `#D8DEE6`) sterile wall/ceiling coffers, surgical ice-white (`#E0F4FF`) and cyan (`#00E5FF`) ceiling cove strips, and UV-violet (`#7B5CFF`) bio-decontamination perimeter strips.
  - **North Outer-Hull Deep-Space Observation Viewport (`Z = -3.70m, X = -2.2m to +2.2m, Y = 0.95m to 2.45m`):** 3-panel chamfered octagonal window glazed with `glass_med_sterile_translucent.png` (`alphaMode: "BLEND"`, `alpha ~ 0.18`), backed at `Z = -4.35m` by **`vista_deep_space.png`** (deep-space starfield, cyan/indigo nebula, and neighboring orbital ring).

---

## 2. Exact Asset Placement Blueprint (`room_04_med_bay.tscn`)

| Slot | Asset File (`/workspace/game-project/assets/glb/winners/`) | Location | Position `(x, y, z)` | `rotation_y_deg` | Role in Scene |
|------|------------------------------------------------------------|----------|----------------------|------------------|---------------|
| **Hero Surgical Autodoc Bay** | `med_autodoc_winner_01_...glb` *(Winner from `medbay_round1`)* | **Center-North Primary Surgical Stage** | `(0.00, 0.00, -1.65)` | `0.0°` | Focal centerpiece of the Med-Bay framed right in front of the North Deep-Space viewport! |
| **Biomonitor Recovery Pod #1** | `bunk_winner_02_medical_biomonitor.glb` | **West Wall — North Recovery Bay** | `(-2.52, 0.00, -1.35)` | `+90.0°` | Locked R2 #07 Medical Biomonitor Pod with arched cyan holographic vitals visor facing East (`+X`). |
| **Biomonitor Recovery Pod #2** | `bunk_winner_02_medical_biomonitor.glb` | **West Wall — South Recovery Bay** | `(-2.52, 0.00, +1.45)` | `+90.0°` | Second inpatient diagnostic & cryo-recovery berth on the West wall. |
| **Chief Surgeon Triage Desk** | `walldesk_winner_01_split_comms_station.glb` | **East Wall — Center Diagnostics Bay** | `(+2.78, 0.00, -0.25)` | `-90.0°` | Medical officer's telemetry console, data-slate dock & swing-out stool facing the Autodoc. |
| **Surgical Scrub & UV Decon Vanity** | `vanity_winner_01_dual_zone_grooming.glb` | **East Wall — North Scrub Bay** | `(+2.82, 0.00, -2.05)` | `-90.0°` | Sonic surgical hand-scrub basin + UV-violet sterile instrument/towel tower. |
| **Bio-Isolation & O2 Panel** | `climate_winner_01_split_env_o2_station.glb` | **East Wall — South Triage Pillar** | `(+2.95, 0.00, +1.65)` | `-90.0°` | Positive-pressure HEPA/UV air-scrubber & emergency medical O2 manifold station. |
| **Sterile Medical Supply Chest** | `footlocker_winner_01_split_cargo_trunk.glb` | **Center-East Surgical Supply Zone** | `(+1.55, 0.00, +1.65)` | `-90.0°` | Mobile pressurized medical supply & plasma canister trunk. |
| **South Entry Bio-Airlock** | `corridor_door_winner_01_...glb` | **South Bulkhead (`+Z`)** | `(0.00, 0.00, +3.50)` | `180.0°` | Pressurized decontamination airlock connecting to `Room 02 — Transit Corridor`. |

---

## 3. Godot 4 Lighting Rig & Camera Presets (`room_04_med_bay.tscn`)

1. **Lighting Rig:**
   - **Overhead Surgical Theater Halo (`SpotLight3D` / `OmniLight3D` at `(0.0, 2.85, -1.65)`):** Color `#E0F4FF` (surgical ice-white), Energy `1.65`, Range `5.5m`.
   - **Recovery Bay Biomonitor Cyan Wash (`OmniLight3D` × 2 at `(-1.95, 1.65, -1.35)` & `(-1.95, 1.65, +1.45)`):** Color `#00E5FF`, Energy `1.25`, Range `4.0m`.
   - **East Scrub & Pharmacy UV-Violet Sterilization Glow (`OmniLight3D` at `(+2.20, 1.65, -1.15)`):** Color `#7B5CFF`, Energy `1.30`, Range `3.8m`.
   - **South Bio-Airlock Amber Quarantine Beacon (`OmniLight3D` at `(0.0, 2.45, +2.95)`):** Color `#FF9500`, Energy `1.20`, Range `3.5m`.
2. **Standardized 3-Angle 1080p Beauty Camera Presets:**
   - **`cam_01_medbay_surgical_overview`:** Pos `(0.00, 1.80, +3.05)` looking at `(0.00, 1.05, -1.65)`, `FOV = 58°` — Heroic wide shot framing the centerpiece Surgical Autodoc Gantry against the North Deep-Space viewport, flanked by the West Biomonitor Recovery Pods and East Scrub/Triage stations.
   - **`cam_02_autodoc_and_recovery_pods`:** Pos `(+1.85, 1.52, +0.65)` looking at `(-1.65, 1.05, -1.45)`, `FOV = 52°` — Highlights the Surgical Autodoc's robotic arms and translucent UV pharmacy tower alongside the twin `bunk_winner_02_medical_biomonitor` pods.
   - **`cam_03_east_surgical_scrub_and_triage`:** Pos `(-1.55, 1.48, +0.20)` looking at `(+2.65, 1.10, -0.35)`, `FOV = 52°` — Showcases the East surgical scrub vanity, medical officer's split comms desk, and O2 life-support station.
