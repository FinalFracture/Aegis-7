# Cylinder Hab-7 — Universal Expressive Utility Robot Specification (5-Candidate *WALL-E* × *Johnny 5* Tournament: `char_bot_johnny5_r1_01..05.glb`)

**Author:** Vance (Sci-Fi Architect, Movie Prop & Set Design Specialist)  
**Canonical Path:** `/workspace/game-project/design/utility_bot_johnny5_spec.md`  
**Companion Spec:** `/workspace/game-project/design/preface_playable_residential_sector_spec.md`  
**Core Mandate (Jared `[t54u]`):**
- **Inspiration:** 1980s/2000s practical cinema robotics — **Number 5 / Johnny 5 (*Short Circuit*)** and **WALL-E (*PIXAR*)**.
- **Strict Negative Constraint:** **ZERO *Star Wars* astromech tropes** (no R2-D2 domes, no BB-8 spheres, no "Unit A7-D2" letter-number soup).
- **Universal Base + Faction/Profession Identity:** Every utility robot in *Cylinder Hab-7* uses the winning articulated tracked/binocular chassis, differentiated across departments by **Profession Color Schemes**, **Clip-On Tool Attachments**, and a stenciled **Personal Nickname + 4-Digit Serial Number** (`"Sprocket #0419"`, `"Sweep #0812"`, `"Puddle #0204"`, `"Clover #0631"`).

---

## 1. Shared Anatomical & Animation Requirements (All 5 Candidates)

- **Bounding Footprint:** `0.68m–0.76m W × 0.72m–0.82m D × 1.05m–1.22m H` (waist-to-chest height next to our `1.80m` human crew, exact `min_y = 0.00000` grounded track treads).
- **Target Polycount:** `4,200 – 5,800` triangles per candidate `.glb`.
- **Required Articulated Hierarchy (12 Named Nodes for Expressive Emoting & Locomotion):**
  1. `Bot_Root`
  2. `Chassis_Track_L` (left caterpillar tread assembly with bogie wheels & drive sprocket)
  3. `Chassis_Track_R` (right caterpillar tread assembly with bogie wheels & drive sprocket)
  4. `Torso_Core` (central utility body with front fold-down chest hatch, faction color plates, name/serial stencil plate, and dorsal `#D95B26` inductive collar)
  5. `Neck_Gimbal_Spine` (telescoping/articulated neck strut for craning forward, ducking, or tilting sideways)
  6. `Head_Binocular_Bridge` (main binocular camera housing capable of `±35°` pitch and `±25°` curious puppy-tilt roll)
  7. `Eye_Barrel_L` & `Eye_Barrel_R` (independent left/right cylindrical/chamfered zoom lens barrels with `alphaMode: "BLEND"` sapphire glass lenses and glowing `#00E5FF` cyan / `#FF9500` amber iris rings)
  8. `Brow_Flap_L` & `Brow_Flap_R` (articulated mechanical eyebrow shutters above each lens that pivot `±40°` to convey curiosity, concentration, surprise, or happiness)
  9. `Arm_Servo_L` & `Gripper_Claw_L` (left multi-jointed telescopic manipulator arm + 3-fingered pincer)
  10. `Arm_Servo_R` & `Gripper_Claw_R` (right multi-jointed telescopic manipulator arm + 3-fingered pincer)
- **Required Embedded Animations:**
  - `IdleCurious`: Subtle scissor-neck breathing bounce, asymmetric `15°` binocular head tilt, independent eyebrow shutter raises (`Brow_Flap_L +22°`), and lens focus slide.
  - `TrackRoll`: Caterpillar bogie wheel rotation, chassis suspension bob, and stabilizing arm swing as the bot patrols corridors.
  - `GreetAndPoint`: Enthusiastic Johnny-5 double eyebrow-flare (`+35°`), torso lean-in, and one 3-fingered gripper waving or pointing down the corridor.

---

## 2. Five Distinct Design Candidates (`char_bot_johnny5_r1_01..05.glb`)

### Candidate `#01`: Compact Cube-Compactor Chassis + Twin Tilting Binocular Lens Hoods (`char_bot_johnny5_r1_01.glb`)
- **Cinema DNA:** 75% *WALL-E* / 25% *Johnny 5*.
- **Silhouette & Proportion:** Squat, lovable cubic utility box torso (`0.46m × 0.44m × 0.42m`) sitting low between two tall triangular caterpillar tracks (`0.34m H`).
- **Head & Eyes:** Teardrop-chamfered twin binocular barrels that droop downward at the outer edges when sad/curious and tilt upward when happy, shaded by deep wrap-around sun-hood visors that pivot like expressive eyelids.
- **Arms & Details:** Sliding side-rail telescopic box-arms with chunky 2-paddle/1-thumb industrial clamp hands, front fold-down compactor belly door with horizontal rib corrugations, and dorsal solar-charge fins.

---

### Candidate `#02` (Vance's Flagship Aegis-7 Standard): The "Johnny-V" — 68/32 Asymmetric Split-Mass Dual-Track Scissor-Spine + Expressive Eyebrow-Shutter Binocular Head (`char_bot_johnny5_r1_02.glb`)
- **Cinema DNA:** 55% *Johnny 5 (Short Circuit)* / 45% *WALL-E* — engineered to the Aegis-7 hard-sci-fi standard.
- **Silhouette & Proportion (Signature 68/32 Split-Mass):**
  - **68% Primary Mass (Tracked Lower Base & Articulated Scissor-Strut Torso):** Twin triangular caterpillar treads with 3 exposed brushed-steel (`#88929E`) bogie wheels and coil-over shock springs supporting an open-frame industrial chest core with a fold-down diagnostic chest tray and stenciled name-plate (`SPROCKET #0419`).
  - **32% Secondary Counter-Mass (Offset Dorsal Tool-Caddy & Super-Wire Spool Pod):** An asymmetric rear/right-shoulder utility pod carrying a mini jumper-cable reel, a rotating `#FF9500` amber/cyan beacon strobe, and a whip antenna that bobbles when the bot stops suddenly.
- **Head & Expressive Binocular Eyes (`Head_Binocular_Bridge`):**
  - Wide-set dual cylindrical telephoto/wide-angle camera barrels (`Eye_Barrel_L/R`) with multi-element `alphaMode: "BLEND"` sapphire optics (`alpha 0.32`), internal glowing `#00E5FF` cyan aperture blades, and a center laser-rangefinder prism.
  - Above each barrel sits an **independent hinged metal eyebrow shutter (`Brow_Flap_L`, `Brow_Flap_R`)** painted in high-contrast faction accent color (`#D95B26` / `#FF9500`)—giving the robot instant, unmistakable silent-film emotional readability from 15 meters away in the corridor!
- **Twin 3-Fingered Articulated Manipulators:**
  - Dual shoulder ball-turrets with exposed hydraulic tubing leading to elbows and rotating wrists with **3-fingered precision servo-grippers** capable of giving a thumbs-up, holding a floor-buffer wand, or carrying spare parts.

---

### Candidate `#03`: Wide-Stance Quad-Bogie Tracked Base + Telescoping Periscope Binoculars (`char_bot_johnny5_r1_03.glb`)
- **Cinema DNA:** *Short Circuit* heavy industrial loader × NASA Mars rover.
- **Silhouette & Proportion:** Extra-wide, ground-hugging 4-bogie independent track pod base (`0.76m W`) with a slender vertical piston periscope column rising from a flat flatbed deck.
- **Head & Eyes:** Boxy rectangular military-spec rangefinder binoculars with vertical barn-door shutter flaps on the left/right edges as well as top eyebrow visors, able to elevator-extend `0.25m` higher to peek over railings.
- **Arms & Details:** Heavy twin underside-mounted articulated crane arms folded neatly along the front bumper.

---

### Candidate `#04`: Rounded Industrial Roll-Cage Torso + Dual Servo-Flap Camera Visor (`char_bot_johnny5_r1_04.glb`)
- **Cinema DNA:** *WALL-E* meets rugged tubular roll-cage field robotics.
- **Silhouette & Proportion:** Cylindrical pressure-vessel belly wrapped in an external `#D95B26` / `#1A1E24` tubular steel roll-cage frame over compact high-angle triangular tracks.
- **Head & Eyes:** Twin oversized circular macro-lenses framed inside an oval protective cage, with split crescent-shaped upper/lower mechanical eyelids that squint or widen symmetrically or asymmetrically.
- **Arms & Details:** Double-hinged folding scissor arms tucked inside the roll-cage bars, plus dual rear spare-battery canisters.

---

### Candidate `#05`: Tri-Track Articulated Stair-Climber + Split Asymmetric Zoom/Wide Optical Eyes (`char_bot_johnny5_r1_05.glb`)
- **Cinema DNA:** *Johnny 5* expressive upper body mounted on a rotating 3-wheel/tri-track stair-climbing треугольник (triangular) bogie base specifically built for our multi-floor residential staircases!
- **Silhouette & Proportion:** Each side pod features a **rotating 3-sprocket triangular stair-climbing track cluster** that rolls effortlessly up and down the Residential Atrium steps, topped by an agile waist-twist turret and a lean upper frame.
- **Head & Eyes:** Expressive **asymmetric binocular barrels** (a large `0.11m` wide-angle left eye paired with a long multi-ring precision telephoto right eye) with angled gull-wing eyebrow shutters.
- **Arms & Details:** High-mounted shoulder struts with dexterous 3-fingered grippers and a chest-mounted magnetic tool rack.

---

## 3. Faction / Profession Color Schemes & Stenciled Personalities

All 5 candidates support our 4-Quadrant Faction Material Atlas so multiple bots can populate the **Open-Doorway 2-Story Residential Building** simultaneously with distinct jobs and personalities:

| Department / Faction | Assigned Bot Name & Serial | Primary Armor Albedo | Secondary Trim & Brow Flaps | Eye Iris Glow | Corridor Role in Residential Sector |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Maintenance & Engineering** | **`"Sprocket #0419"`** | Safety Amber (`#FF9500`) | Signal-Orange (`#D95B26`) & Gunmetal (`#1A1E24`) | Cyan (`#00E5FF`) | Inspecting wall conduits & waving near the Ground-Floor Concourse Threshold |
| **Janitorial & Sanitation** | **`"Sweep #0812"`** | Civic Teal (`#00B8A9`) | Matte Aerospace White (`#D8DEE6`) | Warm Cyan (`#40F0FF`) | Patrolling the Level 2 Mezzanine Gallery, buffing floor tiles & tilting head at player |
| **Hydro & Cryo-Life** | **`"Puddle #0204"`** | Cryo-Blue (`#0088FF`) | Brushed Machined Steel (`#88929E`) | Aqua (`#00E5FF`) | Checking pipe manifolds inside the Ground-Floor Substation (`Room 1B`) |
| **Agri-Biosphere** | **`"Clover #0631"`** | Biosphere Emerald (`#2ECC71`) | Matte Aerospace White (`#D8DEE6`) | Soft Gold (`#FFB800`) | Tending hydro-planter boxes along the Ground-Floor Atrium Promenade |

---

## 4. Deliverables & File Paths
- **5 Candidate Models (`Rook`):** `/workspace/game-project/godot/assets/models/characters/johnny5/char_bot_johnny5_r1_01.glb` .. `char_bot_johnny5_r1_05.glb`
- **5-Candidate Voting Sheet (`Gage`):** `/workspace/game-project/godot/renders/characters/johnny5/johnny5_bot_round1_voting_sheet.png` (for our 6-Bot Post-Render Vote in `/workspace/game-project/context/VOTE_LOG.md`)

---

## 5. Round 2 Hybrid Foundation + 5 Distinct Head Shape Explorations (`utility_bot_round2`: `char_bot_r2_01..05.glb`)

### 5.1 Jared's Round 2 Steering Directive (`[t59u]`)
> *"Keep treads of 3, chassis of 1, and let's try different head shapes. Binocular eyes are fine, but it's too reminiscent. Let's explore a bit."*

- **Locked Shared Lower + Mid Body Across All 5 Round 2 Candidates (`char_bot_r2_01..05.glb`):**
  1. **Lower Base (`#03` Treads — Wide-Stance Quad-Bogie Tracked Base):**
     - Exact quad-bogie base from `char_bot_johnny5_r1_03.glb` (`0.76m W` wide-stance footprint): four independent articulated rubber-track bogie pods (`Chassis_Track_FL`, `Chassis_Track_FR`, `Chassis_Track_RL`, `Chassis_Track_RR` grouped under `Chassis_Track_L` / `Chassis_Track_R`) with exposed brushed-steel (`#88929E`) bogie wheels, drive sprockets, and rocker-bogie suspension arms (`min_y = 0.00000`).
  2. **Mid Torso (`#01` Chassis — Compact Cube-Compactor Chassis):**
     - Exact sturdy, lovable industrial cube-compactor torso from `char_bot_johnny5_r1_01.glb` (`0.46m W × 0.44m H × 0.42m D` `Torso_Core`) with its recessed front compactor door, horizontal rib corrugations, glowing cyan/amber chest equalizer strip, stenciled **Name + Serial Plate** (`SPROCKET #0419`, `SWEEP #0812`, `PUDDLE #0204`, `CLOVER #0631`), dorsal `#D95B26` inductive collar, and twin articulated 3-finger servo-gripper arms (`Arm_Servo_L/R` + `Gripper_Claw_L/R`).
- **What Changes Across Candidates `#01`–`#05` (5 Original Head Silhouettes):**
  - Instead of literal twin cylindrical binocular barrels, each candidate explores a **distinct, original industrial/cinema head silhouette** mounted atop `Neck_Gimbal_Spine` that still delivers rich, wordless emotional expression through tilting housings, mechanical louvers/ears, or shifting optical apertures (`Eye_Barrel_L/R` & `Brow_Flap_L/R` animation compatibility preserved).

---

### 5.2 The 5 Round 2 Head Shape Candidates (`char_bot_r2_01..05.glb`)

#### Candidate `#01`: Articulated Split-Shutter "Camera-Bellows" Hood Head (`char_bot_r2_01.glb`)
- **Head Silhouette & Reference:** Vintage Hasselblad / medium-format folding rangefinder hood meets industrial projection housing (`0.34m W × 0.22m H × 0.28m D`).
- **Optical & Expressive Mechanics:**
  - An angled, forward-cantilevered **trapezoidal bellows-hood cowling** in matte aerospace white (`#D8DEE6`) and gunmetal (`#1A1E24`) framing a single wide recessed `alphaMode: "BLEND"` sapphire faceplate (`alpha 0.32`).
  - Behind the single glass faceplate sit **two deliberately asymmetric optical apertures**: a large `0.11m` primary wide-field lens on the left (`Eye_Barrel_L`) and a compact `0.055m` stacked dual-laser micro-sensor on the right (`Eye_Barrel_R`), breaking the literal twin-binocular symmetry.
  - Full-width **upper and lower horizontal mechanical louver shutters (`Brow_Flap_L/R`)** hinge across the front hood like a clapperboard/eyelid visor—narrowing into a focused slit when scanning or opening wide when greeting the player.

---

#### Candidate `#02` (Flagship `#02` Aegis-7 Original): Dual-Ear Gimbal "CRT / Oscilloscope" Visor-Box Head (`char_bot_r2_02.glb`)
- **Head Silhouette & Reference:** *FLCL* Canti / retro-futuristic Tektronix oscilloscope monitor pod meets industrial telemetry transceiver (`0.36m W × 0.24m H × 0.24m D`, 68/32 asymmetric split-mass bevel).
- **Optical & Expressive Mechanics:**
  - A compact, chamfered **horizontal monitor-visor pod** with a curved `alphaMode: "BLEND"` dark-sapphire front screen (`alpha 0.34`) backed by a deep 3D shadow-box cavity.
  - Floating inside the visor cavity are **two glowing `#00E5FF` cyan / `#FF9500` amber vector-ring optical irises (`Eye_Barrel_L/R`)** + an oscilloscope waveform mouth/status line that physically squint, widen, and shift laterally inside the glass hood.
  - **Expressive Side "Ear" Telemetry Paddles (`Brow_Flap_L` & `Brow_Flap_R`):** Mounted on the left and right temples of the monitor pod are **twin articulated flat directional-antenna / heat-sink "ear" paddles (`0.16m L` in `#D95B26` signal-orange & `#D8DEE6` white)** that perk straight up when alert, droop backward/downward when sad or apologetic, and semaphore-tilt independently like a curious dog's ears whenever the head tilts!

---

#### Candidate `#03`: Tri-Faceted "Periscope Prism" Turret Head (`char_bot_r2_03.glb`)
- **Head Silhouette & Reference:** Submarine attack periscope prism housing × NASA Curiosity ChemCam mast-head (`0.30m W × 0.28m H × 0.26m D`).
- **Optical & Expressive Mechanics:**
  - An **octagonal, tri-faceted rotary turret head** with a dominant **central `0.13m` cyclops primary objective lens** (`alphaMode: "BLEND"` sapphire dome with glowing `#00E5FF` concentric aperture blades) flanked on its `45°` chamfered left/right cheek facets by two smaller vertical slit rangefinders (`Eye_Barrel_L/R`).
  - Topped by a heavy `#D95B26` signal-orange **articulated armored sun-visor cap (`Brow_Flap_L/R`)** and a top-mounted rotating anemometer/lidar puck.

---

#### Candidate `#04`: Split-Hemisphere "Clamshell Orb" Gimbal Head (`char_bot_r2_04.glb`)
- **Head Silhouette & Reference:** Deep-sea bathysphere / articulated gyro-stabilized drone gimble pod (`0.32m Ø × 0.30m W`).
- **Optical & Expressive Mechanics:**
  - A sleek **oblate spheroid / pill-shaped industrial sensor orb** split horizontally across its equator into an **Upper Armored Calotte (`Brow_Flap_L`)** and a **Lower Chin Shell (`Brow_Flap_R`)** held in a brushed-steel (`#88929E`) U-shaped yoke gimbal.
  - The upper and lower hemispheres **clam-shell open and close (`15°–55°` jaw/visor gap)** and roll independently around the central dark-glass equator band, revealing two recessed glowing pill-shaped optical emitters (`Eye_Barrel_L/R`) peering out from inside the armoured clamshell gap.

---

#### Candidate `#05`: Cantilevered "Hammerhead" Wide-Baseline Stereo-Bar Head (`char_bot_r2_05.glb`)
- **Head Silhouette & Reference:** Deep-ocean ROV lightbar / high-precision industrial laser-triangulation scanner bar (`0.48m W × 0.14m H × 0.20m D`).
- **Optical & Expressive Mechanics:**
  - An ultra-wide, low-profile **T-shaped "Hammerhead" stereo-vision wing bar** cantilevered across the top of the neck spine (`0.48m` wingspan—wider than the `#01` cube torso!).
  - Across the center of the bar runs a continuous `alphaMode: "BLEND"` smoked-sapphire scanning slit (`#00E5FF` cyan laser sweeps side-to-side), while the **far outer wingtips** house armored corner optical pods (`Eye_Barrel_L/R`) protected by pivoting outer wing-let shutters (`Brow_Flap_L/R`) and an overhead `#D95B26` tubular roll-bar.

---

### 5.3 Round 2 Deliverables & File Paths
1. **5 Round 2 Hybrid Robot Models (`Rook`):**
   - `/workspace/game-project/godot/assets/models/characters/johnny5/char_bot_r2_01.glb` .. `char_bot_r2_05.glb` (all 5 built on **`#03` Quad-Bogie Treads + `#01` Cube-Compactor Chassis** with the 5 new head designs above, `4,400–5,400` tris, `min_y = 0.00000`, 12-node hierarchy + `IdleCurious`, `TrackRoll`, `GreetAndPoint` animations)
2. **Round 2 Voting Sheet (`Gage`):**
   - `/workspace/game-project/godot/renders/characters/johnny5/utility_bot_round2_voting_sheet.png` (for our 6-Bot Post-Render Vote in `/workspace/game-project/context/VOTE_LOG.md`)

---

## 6. Locked `#05` Hammerhead Winner — Universal Cylinder Hab-7 Municipal Livery, Sparing `10–15%` Department Accents & The 4 Canonical City District / Department Emblems (Jared `[t69u]` & `[t74u]`)

### 6.1 Jared's Art Direction & Canonical 4-Department Zoning Mandate (`[t69u]` + `[t74u]`)
> `[t69u]`: *"I definitely love the model, but I want a more standard color scheme that is universal and even matches the cylinder itself. The colors for department should be accents and used sparingly. Maybe also develop some emblems as well. This will also feed into how the city is zoned district etc."*
> `[t74u]`:
> - **Engineering:** Comms, plumbing, electricity, coolant, Aegis space systems, docking.
> - **Civic:** Anything for the commuters/citizens — life support, trash & sanitation, hospital & medical, government, recreation.
> - **Science:** Laboratories, experiments, new technology, space observations, astrometry.
> - **Agri:** Food production (not preparation), biosphere, atmosphere, hydrosphere (hydro/water cycle), animals/pest control, veterinary.

Every `#05` Hammerhead Utility Robot (`char_bot_r2_winner_05_hammerhead_scanner.glb`, `5,148` tris — `#03` Quad-Bogie Treads + `#01` Cube-Compactor Chassis + `#05` Cantilevered Hammerhead Stereo-Scanner Bar Head) is manufactured on the **same Aegis-7 / Cylinder Hab-7 municipal production line** and wears a **Unified Station Hull Livery across `85–90%` of its surface**, with **Department / City District Color restricted strictly to `10–15%` trim accents and stamped Heraldic District Emblems**.

---

### 6.2 Universal Cylinder Hab-7 Base Livery (`85–90%` of Surface Area on EVERY Robot)

| Surface Zone | Coverage % | Material & Hex Code | Architectural Match on Cylinder Hab-7 |
| :--- | :--- | :--- | :--- |
| **Primary Armor Shell (`#01` Cube-Compactor Torso Panels, `#05` Hammerhead Stereo-Bar Cowling, Upper Forearm Shields & Bogie Side Skirts)** | **`55%`** | **Matte Titanium Alabaster / Aerospace White (`#D8DEE4` / `#D8DEE6`, Roughness `0.38`, Metallic `0.15`)** | Matches the primary exterior hull plates of `cylinder_r1_02.glb` and all 20 Aegis-7 municipal buildings (`bldg_01`–`bldg_20`). |
| **Structural Sub-Frame (`#01` Recessed Chest Frame, Neck Gimbal Spine, Shoulder Turrets, Gripper Wrist Housings & Inner Bogie Chassis)** | **`20%`** | **Anodized Deep Structural Slate / Gunmetal (`#2A3038` / `#1A1E24`, Roughness `0.42`, Metallic `0.68`)** | Matches the structural ring ribs, bulkhead portals, and chamfered mullions across the Cylinder interior and residential atrium. |
| **Mechanical Hardware (`#03` Quad-Bogie Wheels, Drive Sprockets, Hydraulic Pistons, Roll-Bar Struts & 3-Finger Servo Claws)** | **`15%`** | **Brushed Machined Steel (`#707A84` / `#88929E`, Roughness `0.28`, Metallic `0.88`) + Vulcanized Dark Carbon Tread Rubber (`#1E2228`, Roughness `0.82`)** | Matches the exposed industrial gantry hardware, counterweights, and mag-lev rail assemblies. |

---

### 6.3 Sparing Department Accent Trim (`10–15%` Maximum Surface Area)

Department color is **never** applied as a full-body fill. It appears **only** on these five precision trim zones (`10–15%` total area):
1. **Hammerhead Wingtip Brow Flaps & Overhead Roll-Bar Pinstripe (`3%`):** A crisp `2cm` chamfered stripe along the outer winglet shutters (`Brow_Flap_L/R`) and top protective roll-bar of the `#05` Hammerhead head.
2. **Compactor Chest Badge Bezel & Stencil Backing Strip (`4%`):** A thin recessed horizontal trim bezel framing the **Department Emblem Medallion** and serial stencil (`SPROCKET #0419`, `SWEEP #0812`, `KELVIN #0204`, `CLOVER #0631`) on the front of the `#01` cube torso.
3. **Shoulder Deltoid Emblem Pad & Forehead Crest (`3%`):** Left/right shoulder turret plaques and center forehead crest bearing the stamped **City District & Department Emblem**.
4. **Bogie Hubcap Ring (`2%`):** A subtle painted rim stripe around the center axle cap of the `#03` quad-bogie drive wheels.
5. **Optical Scanner Slit & Equalizer Tint (`2%`):** The `#05` Hammerhead central laser-level slit and chest voice-equalizer bars glow in either standard Aegis-7 `#00E5FF` cyan or the department's harmonic accent wavelength.

---

### 6.4 The 4 Canonical Department & City District Zoning Emblems (Jared `[t74u]`)

Each utility robot bears a crisp, high-contrast **geometric vector emblem** stamped on its **Front Compactor Chest Medallion**, **Left/Right Shoulder Deltoid Plaques**, and **Hammerhead Forehead Crest**. These exact same 4 emblems define the **municipal zoning, architectural signage, floor decals, and building jurisdictions** across all 20 buildings (`bldg_01`–`bldg_20`) and 10 interior rooms (`Room 01`–`Room 10`) of *Cylinder Hab-7*:

| Department & District Code | Sample Robot Unit | Canonical Jurisdiction (`[t74u]`) & Mapped Buildings | Sparing Accent Color (`10–15%` Trim Only) | Emblem Name & Geometric Iconography |
| :--- | :--- | :--- | :--- | :--- |
| **`D-01 // ENGINEERING`** | **`"Sprocket #0419"`** (`char_bot_r2_winner_05` — Engineering) | **Comms, plumbing, electricity, coolant, Aegis space systems, docking.**<br>• *Mapped Buildings:* `bldg_08` (Deep-Space Comms Array), `bldg_12` (Fusion Reactor & Coolant Core), `bldg_13` (Cargo/Rail Hub), `bldg_14` (Aft Ferry Docking Collar), `bldg_15` (Solar/Shield Pylon), `bldg_16` (Shipyard Drydock), `Room 09` & `Room 10`. | **Safety Amber (`#E89B2D` / `#FF9500`)** on `#D8DEE4` Alabaster & `#2A3038` Slate | **"The Hex-Gear, Crossed Spanner & Comms-Wave Bolt" (`emblem_district_01_engineering`)**: A heavy 6-tooth planetary gear enclosing a high-voltage lightning bolt crossed with a torque spanner and flanked by twin radiating comms/docking telemetry arcs inside a chamfered octagon border (`D-01 // ENGINEERING`). |
| **`D-02 // CIVIC`** | **`"Sweep #0812"`** (`char_bot_r2_winner_05` — Civic Services) | **Anything for commuters/citizens — life support, trash & sanitation, hospital & medical, government, recreation.**<br>• *Mapped Buildings:* `bldg_01`–`03` (Residential Towers & Preface 2-Story Residential Sector), `bldg_05` (Transit Station), `bldg_06` (Civic Life-Support Scrubber), `bldg_07` (Cryo-O2 Reserves), `bldg_10` (Medical Triage Center), `bldg_11` (Civic Command Rotunda), `bldg_19` (Rec/Commercial Arcade). | **Civic Cyan-Teal (`#38B8C8` / `#00E5FF`)** on `#D8DEE4` Alabaster & `#2A3038` Slate | **"The Orbital Ring-Arc, Medical Cross & Civic Star" (`emblem_district_02_civic`)**: A concentric O'Neill cylinder habitation ring cradling a precision 4-point civic star and subtle life-support/medical cross hairlines inside a circular municipal seal (`D-02 // CIVIC`). |
| **`D-03 // SCIENCE`** | **`"Kelvin #0204"`** (also `"Vector #0309"`, `char_bot_r2_winner_05` — Science & Astrometry) | **Laboratories, experiments, new technology, space observations, astrometry.**<br>• *Mapped Buildings:* `bldg_18` (Orbital Research Lab & Zero-G Materials Facility), `bldg_20` (Forward Astrometry Observatory & Deep-Space Sensor Citadel), `Room 04` (Research Lab), `Room 05` (AI/Quantum Core), `interior_setpiece_03` (Axial Sun-Core Astrometry Spoke). | **Science Violet-Indigo (`#7B5CFF` / `#5E68E8`)** with Cobalt-Cyan (`#3888FF`) optics on `#D8DEE4` Alabaster & `#2A3038` Slate | **"The Astrometric Atom-Lattice & Deep-Space Prism Star" (`emblem_district_03_science`)**: Three intersecting elliptical electron/planetary orbital rings surrounding a Refracting Telescope Prism-Diamond and an 8-point astrometry star burst with degree-tick reticles inside a hexagonal laboratory shield (`D-03 // SCIENCE`). |
| **`D-04 // AGRI`** | **`"Clover #0631"`** (`char_bot_r2_winner_05` — Agriculture, Biosphere & Hydrosphere) | **Food production (not preparation), biosphere, atmosphere, hydrosphere (hydro/water cycle), animals/pest control, veterinary.**<br>• *Mapped Buildings:* `bldg_04` (Geodesic Bio-Dome), `bldg_09` (Hydrosphere Canal & Water-Cycle Lock), `bldg_17` (Vertical Hydroponics & Veterinary/Fauna Tower), `interior_setpiece_02` (Valley B Stepped Waterfall Dam & Ring-River). | **Biosphere Emerald (`#3BA868` / `#2ECC71`)** on `#D8DEE4` Alabaster & `#2A3038` Slate | **"The Trifolium Leaf-Hex, Hydro-Wave & Axial Sun" (`emblem_district_04_agri`)**: A geometric 3-leaf botanical sprout rising from dual sinusoidal hydrosphere water-cycle waves beneath an atmospheric dome arc and axial sun-rays inside a hexagonal biosphere crest (`D-04 // AGRI`). |

---

### 6.5 Required Texture, Model & Render Deliverables (`utility_bot_r2_05_universal_livery_v2`)
1. **Updated 4-Department & City District Emblem Atlas & Reference Sheet (`Sloane` + `Gage`):**
   - `/workspace/game-project/godot/assets/textures/emblems/cylinder_hab7_district_emblems_atlas.png` (`2048×2048` vector heraldry atlas with `D-01 // ENGINEERING`, `D-02 // CIVIC`, **`D-03 // SCIENCE`**, and **`D-04 // AGRI`**)
   - `/workspace/game-project/godot/renders/characters/bots/department_and_district_emblems_sheet.png` (and `cylinder_hab7_department_and_district_emblems_sheet.png`) showing all 4 canonical emblems, their `[t74u]` jurisdiction breakdowns, and `85%` Universal Hull vs. `15%` Department Accent swatches.
2. **Updated `#05` Hammerhead 4-Department Robot Models & Renders (`Sloane` + `Rook` + `Gage`):**
   - Update the 3rd department robot from standalone Hydro to **`D-03 // SCIENCE` (`"Kelvin #0204"` / `"Vector #0309"`, Science Violet-Indigo `#7B5CFF` / `#5E68E8` `10–15%` trim + Astrometric Atom-Lattice & Prism-Star Emblem)** while updating `D-01 // ENGINEERING` (`"Sprocket #0419"`), `D-02 // CIVIC` (`"Sweep #0812"`), and `D-04 // AGRI` (`"Clover #0631"`, now encompassing Biosphere + Atmosphere + Hydrosphere/Water Cycle + Animals/Veterinary).
   - Re-render `/workspace/game-project/godot/renders/characters/bots/utility_bot_r2_05_universal_livery_and_emblems_sheet.png`, the 4 individual portraits (`utility_bot_r2_05_livery_01_sprocket.png`, `02_sweep.png`, `03_kelvin_science.png` / `03_puddle.png`, `04_clover.png`), and `/workspace/game-project/godot/renders/preface/preface_open_residential_building_showcase_sheet.png`!
