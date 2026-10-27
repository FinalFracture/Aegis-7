# ORBITAL HAB-7 — UNIFIED ARCHITECTURAL BIBLE & 10-ROOM MASTER PLAN
**Lead Architect / Design Language:** "Aegis-7 Orbital Architecture" (Single-Architect Unified Aesthetic)
**Autonomous Run Window:** Now until 4:00 AM CT (Zero Spending, Full Team Voting on Every Item)

---

## 1. THE SINGLE-ARCHITECT UNIFIED STYLE BIBLE ("AEGIS-7 STANDARD")
Every single room, corridor, bulkhead, and furniture piece in *Orbital Hab-7* was designed by the same orbital habitat engineering bureau at the same time. Nothing looks mismatched, cobbled together, or from different eras.

1. **Unified Structural Geometry:**
   - **45° Chamfered Octagonal Ribs & Bulkheads:** Every room uses the same signature 45-degree beveled bulkhead ribs, recessed wall alcoves (`0.35m–0.85m` deep), and flush-mounted floor/ceiling expansion seams.
   - **Translucent Location-Aware Viewports (`alphaMode: "BLEND"`, `alpha ~ 0.18–0.22`):** Rooms on the Outer Hull look out into **Deep Space (`vista_deep_space.png`)**; rooms on the Inner Hull/Terrace look out into the **800m × 400m O'Neill Cylinder Interior (`vista_oneill_cylinder_interior.png`)**.
2. **Unified Material Palette (`< 1.2%` Micro-Noise, Ultra-Clean & Calm):**
   - **Primary Hull & Structure:** Dark Anodized Gunmetal Titanium (`#1A1E24`, `metallic: 0.78`, `roughness: 0.34`)
   - **Interior Moulded Shell Panels:** Matte Aerospace White Composite (`#D8DEE6`, `metallic: 0.08`, `roughness: 0.30`)
   - **Secondary Framing & Decking:** Dark Carbon-Slate (`#282E38`, `metallic: 0.58`, `roughness: 0.40`)
   - **Precision Hardware & Gantries:** Machined Brushed Titanium-Steel (`#88929E`, `metallic: 0.90`, `roughness: 0.22`)
   - **Soft Goods / Seating / Padding:** Contoured Charcoal Ballistic Flightpad (`#242932`) & Deep Orbital Navy (`#1D2C3C`)
   - **Functional Safety Accent:** Matte Aerospace Signal-Orange (`#D95B26`) on airlock latches, O2 valves, and emergency handles.
3. **Unified Practical Lighting Signature:**
   - **Primary Telemetry & Cove Trim:** Recessed Cyan LED (`#00E5FF`)
   - **Warm Circadian & Floor Safety Guide:** Recessed Amber LED (`#FF9500`)
   - **Medical / Sterilization / Bio-Support:** Soft UV-Violet (`#7B5CFF`) or Surgical Ice-White (`#E0F4FF`)

---

## 2. MANDATORY "MAKE 5 FIRST, THEN VOTE" PROTOCOL FOR EVERY ASSET
For **EVERY SINGLE ASSET** (both the Sleeping Quarters fixtures AND the hero assets for all 10 room types):
1. **Step 1 (Design 5):** Sloane designs 5 distinct candidate variations (`_01` through `_05`) adhering to the unified Aegis-7 architectural style.
2. **Step 2 (Model 5):** Rook models all 5 `.glb` files (`_01.glb` through `_05.glb`).
3. **Step 3 (Render 5):** Gage renders all 5 candidates at 1080p plus a 5-Panel Voting Comparison Sheet.
4. **Step 4 (5-Bot Vote on the Finished 5):** Only AFTER all 5 candidates are built and rendered do all 5 team members inspect the 5 renders and cast an explicit, reasoned vote recorded in `/workspace/game-project/context/VOTE_LOG.md` to lock the winner into `/workspace/game-project/assets/glb/winners/`:
- **Sloane** (Interior, Lighting & Texture Designer) — votes on architectural cohesion, silhouette, and lighting balance.
- **Rook** (3D Modeling Specialist) — votes on 3D form quality, bevel/lathe craftsmanship, and silhouette readability.
- **Gage** (Godot 4 Developer) — votes on in-engine shader look, translucent glass read, and frame-rate efficiency.
- **Scribe** (Context & Handoff Manager) — votes on alignment with Jared's core rules and continuity across rooms.
- **Atlas** (Game PM) — casts the final tie-breaking / PM vote and sends the winning render + voting sheet to Jared.

---

## 3. REMAINING SLEEPING QUARTERS FIXTURES (QUEUE)
- **Fixture #1 — EVA Suit & Personal Gear Locker:** **LOCKED WINNER `#02`** (`locker_winner_01_dual_bay_bulkhead.glb`, picked by Jared)
- **Fixture #2 — Compact Hygiene & Sonic Wash Vanity:** 5 candidates (`vanity_r1_01..05.glb`) -> 5-Bot Vote -> Winner Locked
- **Fixture #3 — Personal Wall Terminal & Fold-Down Cabin Desk:** 5 candidates (`walldesk_r1_01..05.glb`) -> 5-Bot Vote -> Winner Locked
- **Fixture #6 — Modular Cargo & Footlocker Chest:** 5 candidates (`footlocker_r1_01..05.glb`) -> 5-Bot Vote -> Winner Locked
- **Fixture #9 — Personal Climate & Life-Support Wall Panel:** 5 candidates (`climate_r1_01..05.glb`) -> 5-Bot Vote -> Winner Locked

---

## 4. THE 10 COHESIVE O'NEILL CYLINDER ROOM TYPES
Every room is built with modular architectural shell pieces + custom room-specific hero props, assembled into a complete Godot 4 `.tscn` scene in `/workspace/game-project/godot/scenes/rooms/`, and rendered at 1080p from multiple angles:

1. **Room 01 — Crew Sleeping Quarters (`room_01_sleeping_quarters.tscn`)**
   - Combines our 4 winning Bunk Pods (`bunk_winner_01..04`), Winning EVA Locker `#02` (`locker_winner_01`), Hygiene Vanity winner, Fold-Down Cabin Desk winner, Modular Cargo Footlocker winner, and Climate/Life-Support Wall Panel winner, with panoramic translucent viewports overlooking Deep Space & the O'Neill Cylinder.
2. **Room 02 — Orbital Sector Transit Corridor & Airlock Hub (`room_02_transit_corridor.tscn`)**
   - Signature 45° octagonal titanium rib corridor, recessed floor amber guide strips, pressurized bulkhead hatch airlocks, emergency O2 station, and a continuous curved window gallery looking out into the 800m O'Neill cylinder interior.
3. **Room 03 — Crew Mess Hall & Synthesizer Galley (`room_03_mess_galley.tscn`)**
   - Industrial-sleek beverage/ration synthesizer bank, cantilevered brushed-steel & aerospace-white dining tables with contoured orbital-navy booths, hydroponic herb strip, and wide observation viewport.
4. **Room 04 — Med-Bay & Biomonitor Triage Suite (`room_04_med_bay.tscn`)**
   - Built around our Medical Biomonitor Pod (`bunk_winner_02`), surgical autodoc articulated gantry arm, UV-sterilizer supply cabinets, cryo-stasis diagnostic alcove, and clean ice-white/cyan lighting.
5. **Room 05 — EVA Prep & Airlock Staging Bay (`room_05_eva_airlock_bay.tscn`)**
   - Banks of Dual-Bay EVA Suit Lockers (`locker_winner_01`), heavy cylindrical outer-hull decompression airlock chamber, mag-boot charging deck grates, umbilical recharge manifolds, and amber cycling beacons.
6. **Room 06 — Hydroponics & Bio-Air Scrubber Dome (`room_06_hydroponics_bay.tscn`)**
   - Vertical translucent glass aeroponic planter columns (`alphaMode: "BLEND"`), oxygen/humidity scrubbing towers, nutrient flow manifolds, and views of the central O'Neill cylinder solar axis.
7. **Room 07 — Habitat Command & Spin-Gravity Telemetry Bridge (`room_07_command_bridge.tscn`)**
   - Tiered curved telemetry consoles (repurposing and refining our hard sci-fi telemetry workstations where they belong!), central holographic O'Neill Cylinder wireframe projection table, and wrap-around command viewport.
8. **Room 08 — Observation Lounge & Zero-G Recreation Deck (`room_08_observation_lounge.tscn`)**
   - Built around our Observation Lounge Sleeper/Daybed (`bunk_winner_04`), contoured low-G recliners, sunken viewing pit, ambient beverage bar, and floor-to-ceiling faceted glass overlooking Deep Space nebula & stars.
9. **Room 09 — Engineering & Life-Support Reactor Core (`room_09_engineering_core.tscn`)**
   - Coolant conduit manifolds, fusion/spin-drive power relays behind translucent radiation shields, diagnostic walkways, and heavy titanium bulkheads with cyan/amber plasma status gauges.
10. **Room 10 — Modular Cargo Hold & Logistics Drone Bay (`room_10_cargo_bay.tscn`)**
    - Stacked modular hex/chamfered cargo containers (scaling up our Modular Cargo Chest aesthetic), overhead magnetic crane rail, cargo loader dock, and pressurized bay doors.
