# Cylinder Hab-7 — Open-Doorway 2-Story Playable Residential Building (`preface_residential_sector.glb`) & Free-Roam Exploration Specification

**Author:** Vance (Sci-Fi Architect, Movie Prop & Set Design Specialist)  
**Canonical Path:** `/workspace/game-project/design/preface_playable_residential_sector_spec.md`  
**Companion Robot Spec:** `/workspace/game-project/design/utility_bot_johnny5_spec.md` (`char_bot_johnny5_r1_01..05.glb`)  
**Steering Update (Jared `[t54u]`):**
1. **NO Doors & NO Puzzle UI for Now:** Hold off completely on the PCBA/Python puzzle UI and remove all blocking door leaves from the building. Every doorway across both floors (`APT 201` Top-Floor Player Apartment, Neighbor Balcony Suite `APT 202`, Upper Vent/Cable Alcove `2C`, Ground-Floor Laundry Lounge `1A`, Bot Charging Substation `1B`, and the Main Ground-Floor Concourse Threshold) is an **open, unobstructed architectural portal (`2.0m – 2.6m` clear width)** so the player can freely walk and wander through every room, corridor, balcony, and staircase without interruption.
2. **5-Candidate *WALL-E* × *Johnny 5* Utility Robot Tournament (`char_bot_johnny5_r1_01..05.glb`):** Populate the open-doorway 2-story residential building with our expressive tracked/binocular utility robots (`"Sprocket #0419"`, `"Sweep #0812"`, `"Puddle #0204"`, `"Clover #0631"`) and civilian residents while rendering the 5-candidate robot voting sheet (`johnny5_bot_round1_voting_sheet.png`).

---

## 1. Architectural Layout: Open-Doorway 2-Story Residential Building (`preface_residential_sector.glb` — `28.0m L × 18.0m W × 8.8m H`)

The building is a seamless, two-story Aegis-7 residential atrium block where **every threshold is an open chamfered archway (`min 2.0m W × 2.5m H` clear walk-through opening)** with zero collision blockers in the doorways:

```
========================================================================================
LEVEL 2 (UPPER RESIDENTIAL MEZZANINE, Y = +4.20m — ALL DOORWAYS OPEN PORTALS!)
+--------------------------------------------------------------------------------------+
| [APT 201: PLAYER'S TOP-FLOOR APARTMENT]  | [APT 202: NEIGHBOR BALCONY SUITE]         |
| (8.0m x 6.0m)                            | (8.0m x 6.0m)                            |
| - Bunk Pod, Workbench, BCI Headband Dock | - Panoramic Window to Cylinder Valley A   |
| - #04 Neural Sleeve & Super-Wire Spool   | - Open Kitchenette & Battery Charge Cell  |
+--------- [OPEN PORTAL 201 (2.0m W)] -----+-------- [OPEN PORTAL 202 (2.0m W)] -------+
|                   [UPPER MEZZANINE GALLERY CORRIDOR (W = 3.2m)]                      |
|  * Janitorial Bot "Sweep #0812" rolling freely & tilting binocular eyes at player    |
|  +-------------------------------------------------------------------+               |
|  |         OPEN CENTRAL ATRIUM LIGHTWELL (alphaMode: "BLEND"         |  [OPEN STAIR  |
|  |         Glass Railing looking down to Ground Floor Concourse)     |   DOWN TO L1] |
|  +-------------------------------------------------------------------+   (3.0m W)    |
|  [OPEN ALCOVE 2C: UPPER VENTILATION & CABLE CHASE (1.8m W Open Arch)]                |
|  - Open walk-in maintenance nook with +5m Super-Wire Spool & Battery Capacitor       |
+--------------------------------------------------------------------------------------+

LEVEL 1 (GROUND FLOOR COMMUTER CONCOURSE, Y = 0.00m — ALL DOORWAYS OPEN PORTALS!)
+--------------------------------------------------------------------------------------+
| [ROOM 1A: RESIDENTIAL LAUNDRY & LOCKER   | [ROOM 1B: LOCAL SUB-STATION & BOT DOCK]  |
|  LOUNGE (7.5m x 5.5m)]                   | (7.5m x 5.5m)                            |
| - Open 2.4m archway into lounge          | - Open 2.2m portal into bot charging bays |
| - Hidden Super-Wire Spool on shelf       | - Hydro Bot "Puddle #0204" by manifold    |
+--------- [OPEN PORTAL 1A (2.4m W)] ------+-------- [OPEN PORTAL 1B (2.2m W)] --------+
|                   [GROUND FLOOR MAIN CONCOURSE PROMENADE (W = 6.0m)]                 |
|  * Civilian Commuters strolling; Agri Bot "Clover #0631" tending atrium planters     |
|  * Maintenance Bot "Sprocket #0419" waving binocular eyes by the South Threshold     |
|                                                                                      |
|  ======== [OPEN SECTOR-4 CONCOURSE GRAND PORTAL (2.6m W OPEN ARCH, Z = -9.0m)] ======|
|           (Completely open doorway looking out onto the sunlit Valley A Promenade!)   |
+--------------------------------------------------------------------------------------+
========================================================================================
```

### 1.1 Key Architectural Features for Seamless Free-Roam Wandering
1. **`APT 201` — Player's Top-Floor Apartment (`Level 2 North-West`, `Y = +4.20m`):**
   - Player spawns standing inside `APT 201` with the locked **`#04` Bio-Luminescent Neural Tendon Sleeve (`prop_wrist_rfid_winner_01_neural_tendon_sleeve.glb`)**, **BCI AI Headband (`prop_bci_headband.glb`)**, and **Super-Wire Spool (`prop_super_wire_spool.glb`)** on the workbench.
   - The apartment entrance (`Open_Portal_201`, `2.0m W × 2.5m H`) has **no door leaf**—recessed `#00E5FF` cyan frame lighting invites the player to walk straight out onto the Level 2 Mezzanine Gallery.
2. **Upper Mezzanine Gallery, `APT 202` Neighbor Suite & `Alcove 2C` Cable Chase (`Level 2`, `Y = +4.20m`):**
   - **Open Atrium Lightwell (`12.0m × 5.0m` void):** Framed by a `1.10m`-tall `alphaMode: "BLEND"` structural glass balustrade (`alpha 0.30`) with `#1A1E24` gunmetal handrails so the player can look directly down into the Ground-Floor Concourse while walking along the upper hallway.
   - **`APT 202` (`Open_Portal_202`, `2.0m W`):** Completely open neighbor apartment with a sunlit `alphaMode: "BLEND"` panoramic window overlooking the O'Neill Cylinder valley and a collectible **Battery Charge Cell** on the counter.
   - **`Alcove 2C` (`Open_Arch_2C`, `1.8m W`):** Walk-in maintenance cable chase on the West wall housing an exposed conduit rack and a collectible **`+5m Super-Wire Spool`**.
3. **Open Switchback Atrium Staircase (`3.0m W`, connecting `Y = +4.20m` to `Y = 0.00m`):**
   - Wide, gentle-slope architectural stairs with `#D95B26` signal-orange non-slip nosing strips, `#00E5FF` cyan stringer LEDs, and a mid-landing overlook window.
4. **Ground-Floor Concourse, `Room 1A` Laundry Lounge, `Room 1B` Bot Dock & Open South City Threshold (`Level 1`, `Y = 0.00m`):**
   - Both **`Room 1A` (`2.4m W` open portal)** and **`Room 1B` (`2.2m W` open portal)** are wide open so the player can wander into the Laundry Lounge and the Bot Charging Substation without touching a single door button.
   - The **South Sector-4 Exit (`Open_Portal_Sector_Exit`, `2.6m W × 2.8m H` at `Z = -9.0m`)** has its dual bulkhead leaves **permanently retracted into the wall pockets (`100%` open, zero door mesh blocking the threshold)**, framing a bright `5500K` sunlit vista of the exterior Promenade!

---

## 2. Summary of Deliverables & File Paths
1. **Open-Doorway 2-Story Residential Building (`Rook` + `Gage`):**
   - `/workspace/game-project/godot/assets/models/environments/preface_residential_sector.glb` (rebuilt with **100% open doorways and zero blocking door leaves**)
   - `/workspace/game-project/godot/scenes/preface_playable_residential_sector.tscn` (free-roam playable scene with **no puzzle UI overlays** and **no closed doors**, populated with our faction-colored *WALL-E* / *Johnny 5* utility robots and civilian commuters)
   - `/workspace/game-project/godot/renders/preface/preface_residential_sector_showcase_sheet.png` (4-camera architectural walk-through sheet showing the open-doorway 2-story building from `APT 201`, the Upper Mezzanine & Open Side Rooms, the Atrium Staircase & Bot Substation, and the Open Ground-Floor Concourse)
2. **5-Candidate *WALL-E* × *Johnny 5* Utility Robot Tournament (`Rook` + `Sloane` + `Gage`):**
   - `/workspace/game-project/godot/assets/models/characters/johnny5/char_bot_johnny5_r1_01.glb` .. `char_bot_johnny5_r1_05.glb`
   - `/workspace/game-project/godot/renders/characters/johnny5/johnny5_bot_round1_voting_sheet.png`
