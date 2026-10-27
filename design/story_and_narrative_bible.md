# Cylinder Hab-7 — Canonical Story & Campaign Bible: The Earth–Mars Aldrin Cycler
**Author:** Quinn (`65d82323-1864-40e3-b8eb-90acde92ed1d`) — Market Research & Gameplay Mechanics Strategist  
**Canonical Path:** `/workspace/game-project/design/story_and_narrative_bible.md`  
**Detailed Preface + Chapter 1 (3-Hour Slice) Spec:** `/workspace/game-project/design/chapter_01_solar_flare_and_preface_spec.md`  
**Locked Canon (Approved by Jared `[t36u]`):**

---

## 1. The Vessel & World: A Thriving Earth–Mars Aldrin Cycler (NOT a Generation Ship)
- **What Cylinder Hab-7 Is:**
  - *Cylinder Hab-7* is an **800m long × 400m diameter (`R = 200m`) rotating O'Neill Cylinder Aldrin Cycler** operating in a continuous heliocentric elliptical orbit between **Earth, the Sun (Perihelion), and Mars**.
  - Unlike a lonely deep-space generation ark, Hab-7 is the **bustling, larger-than-life Grand Central Station of the Inner Solar System**: at every Earth and Mars orbital rendezvous window, shuttle fleets dock at the **Aft Zero-G Starport (`CAM 04`)** and **Forward Axial Pinnacle (`bldg_14`)** to perform massive passenger, tourist, colonist, and interplanetary cargo pick-ups and drop-offs.
  - Inside the drum, **50,000+ passengers and residents** fill the three asymmetric valleys (**Valley A `180°` Civic Metropolis**, **Valley B `60°` Emerald Waterfall Biosphere**, and **Valley C `300°` Industrial Shipyard & Fusion Port**), riding Mag-Lev trains up the `120°` Suspension Skybridge (`interior_setpiece_01`) and looking up across 400m of open air at the other two cities hanging upside-down on the ceiling.

---

## 2. Who You Play As: The 5 Shift-7 Maintenance Technicians (Interfacing with Androids & Ship AI)
- You control **Shift-7 Orbital Maintenance**—a 5-person team of hands-on mechanical, transit, hydro-biosphere, and EVA technicians (`character_crew_headshots_sheet.png` & `char_crew_r1_01..05.glb`) who keep the giant spinning cycler running smoothly day-to-day:
  1. **`#02` Kaelen Rostov (*Lead Shift Foreman & Systems Diagnostician*):** Equipped with his Left-Eye `#00E5FF` Cyan AR Monocle, Wrist Holo-Projector, and Right-Forearm Grapple-Tether. Directs AI node overrides (`bldg_11` / `Room 07`), operates the **Drum RPM Dial (`Mechanic C`)**, and calibrates **Cross-Cylinder Chord Launchers (`Mechanic A`)**.
  2. **`#01` Marcus Vance-Lin (*Transit, Mag-Lev & Docking Logistics Tech*):** Coordinates shuttle docking (`bldg_14`), Cargo Loader Androids (`Room 10` / `bldg_13`), and the `120°` Ring-Spanning Skybridge Mag-Lev network (`interior_setpiece_01` / `bldg_02`).
  3. **`#03` Tarek Mensah (*Heavy Hull, Spin-Drive & Fusion Boilermaker*):** Wears the Caterpillar-Amber exo-roll-cage with forehead floodlamp; commands heavy industrial Androids in `Valley C` (`bldg_12` D-He3 Fusion Core, `bldg_16` Shipyard Drydock, `Room 09` Spin-Drive Reactor).
  4. **`#04` Dr. Soren Sato (*Hydro-Ecology, Scrubber & Bio-Med Tech*):** Wears the Emerald/UV neural headband and holo-glasses; supervises Biosphere & Medical Androids across `Valley B` (`interior_setpiece_02` Waterfall Hydro-Dam, `bldg_06` Biodome, `bldg_07` Atmo Plant, `bldg_09` Aquifer Pump, `bldg_10` Cryo Vault, `Room 04` Medbay).
  5. **`#05` Vesper Kade (*High-Altitude Rigging, Heliostat & Exterior EVA Tech*):** Equipped with cybernetic temple uplink and zero-O2 rebreather; handles high-risk zero-G rigging along the `R = 0m` **Axial Sun-Core (`interior_setpiece_03`)**, **Forward Cliffside Citadel (`interior_setpiece_04`)**, **Astrometry Observatory (`bldg_08`)**, **Solar-Mirror Pylons (`bldg_15`)**, and **Meteor Defense Bastions (`bldg_20`)**.
- **Android Work-Crews & Ship AI (`AEGIS-7`):**
  - Your 5 human technicians command local **Service & Industrial Androids** and interface with the vessel's distributed **AI Operating System (`AEGIS-7`)**—which works seamlessly during the **Preface**, but fractures into haywire Android loops and rigid quarantine lockouts when struck by the **Chapter 1 Solar Flare EMP**.

---

## 3. Locked Campaign Structure (Preface + Chapter 1 Focus; Intermediary Chapters Held; Final Evacuation Goal)

1. **THE PREFACE (*Super Metroid*-Style Wordless Intro — `5 Minutes Experienced / 30 Minutes New Player`):**
   - ***"Zero Prompts. Zero Hand-Holding. The Geometry Teaches the Game."*** (Locked by Jared `[t37u]`)
   - **Strict Rules:** ZERO on-screen button prompts/pop-ups, and ZERO AI voiceovers or crewmates explaining controls. Assumes the player knows what's going on and feeds mechanics at a steady pace across **5 Contiguous Physical Zones** using visual cause-and-effect and *Super Metroid* Dachora/Etecoon-style environmental demonstrations:
     - **Zone 1 (`preface_test_room` — Routine Door Service Call & Subdermal Wrist-Loom):** No silly unexplained sparks—you start on the clock answering a routine Door Malfunction Service Call in a commuter vestibule with 2–3 waiting citizens and your Compact Utility Assistant Droid. Watching citizens hold their wrists to the door sensor + button-mashing raises your left hand to center-screen, lighting up your **Subdermal RFID Nodes (`#00E5FF`) & Induction Split-Cuff** (distinct from a Pip-Boy) so you repeatedly cycle the out-of-phase door leaves (`4–5` wrist-scans in one small room) and sync your Assistant Droid until the door opens and the commuters walk through.
     - **Zone 2 (`Room 10` Cargo Pit):** Watching an autonomous Service Android behind a glass partition plug in a battery and lower a lift teaches Android command by imitation.
     - **Zone 3 (`Room 05` Pressure Gate):** A counterweight gate that snaps shut when released—paired with `#03` Mensah standing right beside the gate behind an observation window—teaches 5-Technician body-swapping (`Tab` / `3`) to walk through while `#02` Rostov holds the lever.
     - **Zone 4 (`bldg_16` / `Room 09` Drydock Gap):** A `6.5m` vertical ledge (unjumpable in `1.00G`) next to a physical **Spin-Trim Flywheel Lever (`Mechanic C`)** and spring-suspended 5-ton weight teaches dialing gravity down to `0.18G` to bound `8m` up onto the exit deck.
     - **Zone 5 (`Valley A 180°` -> `Valley B 60°` Ceiling):** Stepping into the thriving 800m city, an automated pneumatic mail tube fires glowing capsules straight up into the sky every 8 seconds—letting the player *watch* them curve under Coriolis force, flip at `R = 0m`, and "fall upward" into `Valley B` on the ceiling before aligning Barrel #2 (`Mechanic A`) to shoot the counterweight core into `#04` Dr. Sato's dock overhead.
2. **CHAPTER 1 (`~3.0 Hours / 180 Minutes` for a By-the-Book Player):**
   - ***"The Solar Flare"*** (Full 5-Phase specification in `/workspace/game-project/design/chapter_01_solar_flare_and_preface_spec.md`)
   - **Rising Action (`0–35m`):** As the cycler swings through **Perihelion** (closest approach to the Sun), magnetic precursor anomalies escalate until the crew scrambles to shelter the bustling city and string cross-sky surge arrestors (`Mechanic A`).
   - **Climax Impact (`35–60m`):** A massive **X-90 Coronal Mass Ejection (Solar Flare)** slams into Cylinder Hab-7.
   - **The Domino Chain-Reaction Cascade (`60–155m`):** The flare's EMP scrambles unshielded **Service Androids**, locks `AEGIS-7` into a 3-valley quarantine split, jams the `R = 0m` **Axial Sun-Core louvers (`interior_setpiece_03`)**, throws the **Drum RPM (`Mechanic C`)** into runaway oscillations (`1.45G` -> `0.08G`), and fractures the coolant mains to the **D-He3 Fusion Reactor (`bldg_12`)**. To prevent a meltdown, the 5 technicians must regain manual control of the **Drum RPM Dial (`Mechanic C`)**, drop cylinder gravity to **`0.08G`** so `Valley B`'s **Ring-River lifts into the sky**, and **shoot a 350m floating water ribbon across the chord-line (`Mechanic A`)** straight into `Valley C`'s reactor intake!
   - **End of Chapter 1 State (`155–180m`):** The crew resolves the chain reaction and puts Cylinder Hab-7 into a **100% stable internal state where life is no longer immediately threatened**—**BUT** sustained damage to the aft propulsion gimbals during the perihelion flare has kicked the cycler onto an unbound hyperbolic trajectory that will eventually slip **out of the Sun's Sphere of Influence (SOI)** into deep interstellar space. Earth & Mars Command immediately launch a **Fleet of Deep-Space Rescue Vessels** to intercept Hab-7.
3. **INTERMEDIARY CHAPTERS (On Hold per Jared `[t36u]`):**
   - Reserved for future design after Preface + Chapter 1 are built.
4. **THE FINAL CHAPTER (Overarching Endgame "Okay, I Win!" Objective):**
   - ***"Operation Lifeboat — The Solar Boundary Evacuation"***
   - Before Cylinder Hab-7 crosses the heliopause and leaves the Sun's Sphere of Influence forever, your 5 maintenance technicians must prepare the damaged, spinning 800m city to rendezvous with the incoming **Earth/Mars Rescue Fleet** and safely evacuate all **50,000+ citizens, Android crews, and the Cryo-Vault archives** without losing a single soul!
