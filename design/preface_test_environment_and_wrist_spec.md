# Orbital Hab-7 — Preface Test Environment & Embedded Wrist RFID / Diegetic Hand-Rig Specification

**Author:** Vance (Sci-Fi Architect, Movie Prop & Set Design Specialist)  
**Target Directory:** `/workspace/game-project/design/preface_test_environment_and_wrist_spec.md`  
**Companion Blueprint:** `/workspace/game-project/design/vance_chapter1_solar_flare_environmental_states.md`  
**Downstream Consumers:**
- **Sloane (`ec8a7e65-dd93-415c-9240-465e61fb2bcb`):** PBR Material Library, Subdermal Transponder Emissive Shaders, Commuter Vestibule Lighting, & Diegetic RFID Pulse States
- **Rook (`61237674-1923-48c9-bc64-19c16cf2501e`):** 3D Procedural `.glb` Generation for 5 Wrist RFID Candidates (`prop_wrist_rfid_r1_01..05.glb`) + Preface Test Room Kit (`preface_service_call_room.glb`, `prop_service_door.glb`, `char_assistant_droid.glb`, `char_citizen_commuter.glb`)
- **Gage (`5c9c9f64-e799-4958-97ab-f8cbf4f6ff90`):** Godot 4 Interactive Preface Test Scene (`preface_service_call_test.tscn`), 5-Candidate Wrist RFID Voting Sheet (`wrist_rfid_round1_voting_sheet.png`), & Test Environment Showcase Sheet (`preface_test_environment_showcase_sheet.png`)
- **Atlas (`e744c2d9-fd3b-4916-a082-3cedfae0b695`) & Scribe (`929b3cf3-1ba3-489f-945f-4734223c6605`):** 6-Bot Post-Render Voting in `/workspace/game-project/context/VOTE_LOG.md`

---

## 1. Design Philosophy: Grounded Service Call & Wordless RFID Discovery

Per Jared's core design directive (`[t38u]`):
1. **No Arbitrary "Sparks Throwing" Opening:** Starting a maintenance technician in a room randomly throwing Hollywood sparks without story justification feels contrived. Instead, the game opens with a grounded, everyday professional moment aboard the thriving Earth–Mars Aldrin Cycler: **Senior Tech Rostov (`#02`) has just arrived at a Sector-4 Commuter Transit Vestibule (`preface_service_call_room`) in response to a routine work order to troubleshoot a malfunctioning dual-leaf bulkhead door.**
2. **Repeatedly Practicing the Door/Interaction Action Without Leaving the Small Room:** Because the job *is* calibrating and cycling a stalling commuter force-field door, the player naturally performs the core interaction verb **three consecutive times in the same compact `10m × 8m × 4.2m` room**—with each scan producing a distinct physical, mechanical, and social reaction from the door field, the Assistant Droid, and the waiting civilian commuters.
3. **The Embedded Wrist RFID / Diegetic Wrist Rig (Distinct from Fallout's Pip-Boy):**
   - Unlike a bulky 1950s CRT television strapped to an arm, the Aegis-7 technician interface is an **embedded subdermal RFID/induction array implanted beneath the dorsal skin of the wrist and metacarpals**, paired with an **articulated hard-sci-fi precision split-cuff** worn over the forearm cuff link.
   - **Wordless Button-Mash + Citizen Demonstration Discovery:**
     - **Visual Clue (The Waiting Commuters):** Two civilian commuters (`char_citizen_commuter`) stand waiting by the jammed bulkhead door with commuter bags. Every 7 seconds, Commuter A steps up to the door's stanchion, **raises their left wrist up to chest/eye level in front of the RFID induction ring**, triggers an `#FF9500` amber rejection chime/flash on the door frame, sighs, and glances back at the player expectantly.
     - **Tactile Discovery (Button-Mashing Raises the Hand to Center Screen):** Whether the player copies the commuter immediately or experiments by pressing buttons, pressing the primary interact/wrist button raises the player's **left hand and forearm up to center screen**. As the hand rises into the center-screen focal zone, the subdermal dorsal nodes illuminate underneath the skin and the articulated wrist cuff mechanically fans open its induction aperture, emitting a crisp `#00E5FF` cyan harmonic wave that couples with any nearby RFID pad, door relay, or droid transponder!

---

## 2. The 3-Cycle Door Troubleshooting Loop (Inside `preface_service_call_room`)

To let the player practice and master the **Raise Hand to Center Screen -> Wrist RFID Scan** loop multiple times without ever leaving the `10m × 8m × 4.2m` room, the malfunctioning bulkhead door (`prop_service_door.glb`) progresses through three physical diagnostic states:

| Cycle | Player Action | Mechanical Door Response (`prop_service_door.glb`) | Assistant Droid & Citizen Response (0 UI Text) |
| :--- | :--- | :--- | :--- |
| **Initial State (Arrival)** | Player stands in the `10m × 8m × 4.2m` vestibule. Commuter A periodically raises their wrist to the door's RFID pedestal, triggering an `#FF9500` amber flash (`Denied — Maintenance Lockout Active`). | The force field (`Field_Plane`) fills the whole `2.20m` aperture of the emitter frame at full strength: a translucent `#FF9500`-tinted lockout sheet with a slow, even shimmer. An amber status strip pulses along the emitter jamb. | `char_assistant_droid` hovers/stands beside the wall relay box, pointing its optical headlamp at the RFID pedestal and chirping a soft two-tone attention harmonic. |
| **Scan Cycle 1 (Primary Field Drop)** | Player raises their wrist to center screen (`prop_wrist_rfid`) near the door pedestal. Subdermal RFID nodes pulse `#00E5FF` cyan, and an inductive arc bridges to the pedestal (`1st node out of 3` on the emitter header turns `#00E5FF` cyan). | The field powers down from the top, **but stalls at about `40%` strength**: the sheet thins and flickers irregularly between the two emitter rails with no passable gap, the left emitter coil bank (`Coil_A`) and the right one (`Coil_B`) visibly out of sync, and after ~2 s it surges back to full strength. | Commuter B steps forward hopefully as the field thins, then pauses and steps back when it surges back. `char_assistant_droid` rolls `1.2m` over to the lower wall junction box (`Relay_Panel_B`), extends its articulated probe arm into the socket, and rotates its `#D95B26` signal-orange transponder ring toward the player. |
| **Scan Cycle 2 (Droid Coil Sync & Cycle Test)** | Player raises their wrist to center screen (`prop_wrist_rfid`) aimed at `char_assistant_droid`'s transponder ring (`or` scans the door pedestal while the droid holds the relay). (`2nd node out of 3` on the emitter header turns `#00E5FF` cyan). | In the emitter header (seen through the `alphaMode: "BLEND"` glass inspection transom) the coil-phase indicator bars slide back into alignment. The field then **fully drops (`2.20m` clear aperture) and re-raises once** as a smooth self-calibration cycle, and the 3rd header ring flashes `#00E5FF` cyan (`Ready for Final Sign-Off Scan`). | `char_assistant_droid` nods its optic head (`#00E5FF` cyan ring), retracts its probe arm, and backs clear of the doorway. Both commuters pick up their bags and face the door. |
| **Scan Cycle 3 (Final Commuter Clearance & Field Release)** | Player raises their wrist to center screen (`prop_wrist_rfid`) one final time at the door pedestal (`All 3 header nodes lock solid #00E5FF cyan`). | The field collapses cleanly to `0%` (collider off) and the emitter rails idle with a faint `#00E5FF` standby glow. The floor threshold strip changes from `#FF9500` amber to solid `#00E5FF` cyan. | Commuter A raises their wrist in a quick thank-you wave as both citizens walk out through the open field aperture into the sunlit Sector-4 Promenade, leaving it open for the player to follow! |

---

## 3. Five-Candidate Tournament Specification: Embedded Wrist RFID / Diegetic Hand-Rig (`prop_wrist_rfid_r1_01..05.glb`)

All 5 candidates represent the **first-person / 3/4 inspection hero prop of the player's raised left hand, wrist, and lower forearm (`0.42m` total length × `0.14m` width × `0.12m` depth)** held up toward center screen in the active RFID scan pose.
- **Strict Differentiation from Pip-Boy:** No bulky rectangular CRT monitor or wrist-brick. Every candidate combines **subdermal glowing RFID micro-nodes embedded directly beneath the dorsal wrist/hand skin** with a **sleek, articulated aerospace wrist cuff/emitter** that physically transforms when raised to center screen.
- **Target Polycount:** `3,200 – 5,800` triangles per candidate `.glb`.
- **Unified Aegis-7 Palette Compliance:** Anodized gunmetal titanium (`#1A1E24`), matte aerospace white (`#D8DEE6`), dark carbon slate (`#282E38`), machined brushed steel (`#88929E`), recessed cyan (`#00E5FF`) & amber (`#FF9500`) LEDs, signal-orange (`#D95B26`) physical release/lock tabs, and true `alphaMode: "BLEND"` translucent glass/sapphire optics (`alpha 0.28–0.40`).

---

### Candidate `#01`: Subdermal Hex-Node Array + Minimalist Titanium Split-Band (`prop_wrist_rfid_r1_01.glb`)
- **Cinema Reference:** *Oblivion* (2013) sterile technician biometrics & *2001: A Space Odyssey* clean white/titanium minimalism.
- **Silhouette & Proportion:** Symmetrical ultra-low-profile minimalist band (`0.045m` cuff width) sitting flush behind the wrist bone, leaving the dorsal hand sleek and unencumbered.
- **Subdermal Implant Detail:** Seven hexagonal micro-transponder nodes arranged in a clean honeycomb cluster beneath the dorsal skin over the metacarpals, glowing `#00E5FF` cyan through translucent epidermal scatter zones.
- **Wrist Cuff & Emitter:**
  - Two-piece matte aerospace white (`#D8DEE6`) and brushed steel (`#88929E`) hinged band with a single `#D95B26` signal-orange micro-clasp on the ulnar side.
  - A thin `alphaMode: "BLEND"` sapphire crystal window (`alpha 0.32`) sits over the radial pulse point, projecting a clean flat circular `#00E5FF` RFID scan ring (`0.08m` diameter) `0.03m` above the back of the hand.

---

### Candidate `#02` (Vance's Signature Aegis-7 Standard): The "Induction Loom" — 68/32 Asymmetric Split-Mass Gyro-Aperture Cuff + Subdermal Dorsal Vein-Grid (`prop_wrist_rfid_r1_02.glb`)
- **Cinema Reference:** *Elysium* (2013) precision medical/industrial cybernetics meets *Alien* (1979) / *Moon* (2009) functional hard-sci-fi hardware.
- **Silhouette & Proportion (Signature 68/32 Asymmetric Split-Mass):**
  - **68% Primary Mass (Radial/Dorsal Housing):** A chamfered anodized gunmetal titanium (`#1A1E24`) and matte aerospace white (`#D8DEE6`) low-profile dorsal bridge anchored to the forearm cuff, featuring an **articulated 3-petal iris/gyro-aperture** that fans open when the hand rises to center screen.
  - **32% Secondary Counter-Mass (Ulnar Inductive Coil & Manual Override):** An offset brushed machined steel (`#88929E`) inductive capacitor cylinder along the outer ulnar edge with a tactile `#D95B26` signal-orange thumb-wheel and emergency manual release latch.
- **Subdermal Dorsal RFID Vein-Grid:**
  - Beneath the skin of the back of the hand and wrist, a precision **3-branch subdermal induction trace** follows the dorsal metacarpal tendons to **5 glowing subdermal transponder nodes** at the knuckle bases and carpal center.
  - During idle lowers, the subdermal nodes glow a soft standby `#00E5FF` cyan (`#FF9500` amber during fault/lockout); when raised to center screen, the subdermal traces pulse sequentially from wrist to knuckles like a phased-array antenna!
- **Floating Holo-Optic & `alphaMode: "BLEND"` Sapphire Bridge:**
  - Spanning `0.018m` above the dorsal wrist is a curved `alphaMode: "BLEND"` translucent sapphire-glass diagnostic lens (`alpha 0.34`) held by two machined steel micro-calipers.
  - Through the translucent sapphire lens, the internal copper/steel induction coil and subdermal skin glow are clearly visible in 3D depth, while three floating `#00E5FF` cyan holographic authentication rings (`r = 0.035m, 0.050m, 0.065m`) + a single `#FF9500` amber parity vector project `0.04m` forward toward the target door pad.
- **Ergonomic Hand & Glove Detailing:**
  - Fingerless Aegis-7 technician flight-glove palm in dark carbon slate (`#282E38`) with micro-ribbed grip pads on the thumb/index fingers, leaving the dorsal hand skin and knuckle transponder implants exposed so the subdermal glow reads unmistakably at center screen.

---

### Candidate `#03`: Heavy Industrial Forearm Exo-Clamp + Flip-Up Optical Reticle Lens (`prop_wrist_rfid_r1_03.glb`)
- **Cinema Reference:** *Alien* (1979) Nostromo heavy engineering gear & *Outland* (1981) zero-G maintenance rig.
- **Silhouette & Proportion:** Rugged, blocky industrial exo-frame (`0.22m` forearm cage) with twin external hydraulic micro-struts bridging across the wrist joint to a knuckle-guard bar.
- **Subdermal Implant Detail:** Three heavy circular subdermal socket plugs (`#88929E` steel collars embedded in the dorsal wrist skin) with `#FF9500` amber and `#00E5FF` cyan core LEDs.
- **Wrist Cuff & Emitter:**
  - Dark carbon slate (`#282E38`) and `#D95B26` signal-orange cage frame with an articulated flip-up `alphaMode: "BLEND"` targeting loupe (`alpha 0.38`) that swings 90° upright over the wrist when raised to center screen.

---

### Candidate `#04`: Bio-Luminescent Neural Tendon Trace + Flexible Polymer Smart-Sleeve (`prop_wrist_rfid_r1_04.glb`)
- **Cinema Reference:** *Annihilation* / high-tech orbital bio-med synth-skin & *Oblivion* seamless wearables.
- **Silhouette & Proportion:** Ultra-organic, form-fitting second-skin polymer half-sleeve (`#282E38` carbon weave) with zero rigid external brackets, relying almost entirely on subdermal illumination.
- **Subdermal Implant Detail:** An intricate branching dendritic network of `#00E5FF` cyan and `#7B5CFF` violet-UV subdermal fiber-optic threads running from the mid-forearm all the way to the fingertips.
- **Wrist Cuff & Emitter:**
  - A flexible `alphaMode: "BLEND"` translucent elastomer cuff (`alpha 0.35`) wraps the carpal tunnel, projecting a soft curved hologram arc across the knuckles without mechanical hinges.

---

### Candidate `#05`: Tri-Spoke Magnetic Field Emitter + Knuckle-Bridge RFID Projector (`prop_wrist_rfid_r1_05.glb`)
- **Cinema Reference:** *Elysium* chem-rail/exo-rig hardware & *Interstellar* CASE/TARS geometric articulation.
- **Silhouette & Proportion:** Angular geometric frame featuring three radiating deployable antenna fins (`120°` spread) and a rigid bridge over the knuckles.
- **Subdermal Implant Detail:** A linear 4-bar barcode-style subdermal light strip set transversely across the dorsal wrist crease (`#00E5FF` cyan / `#FF9500` amber).
- **Wrist Cuff & Emitter:**
  - Gunmetal titanium (`#1A1E24`) tri-spoke collar with three `#D95B26` signal-orange folding emitter prongs and a flat octagonal `alphaMode: "BLEND"` glass beam-splitter (`alpha 0.34`) hovering over the back of the hand.

---

## 4. Preface Test Environment & Supporting Asset Specifications

To build the playable, self-contained **Preface Test Environment (`preface_service_call_room`)**, Rook will generate four modular `.glb` assets and Gage will assemble them into `/workspace/game-project/godot/scenes/preface_service_call_test.tscn`.

### 4.1 `preface_service_call_room.glb` — Sector-4 Commuter Transit Vestibule (`10.0m W × 8.0m D × 4.2m H`)
- **Spatial Layout & Architectural Zones:**
  - **North Wall (`Z = -4.0m`, Primary Focal Wall):**
    - Centered `2.40m W × 2.60m H` chamfered bulkhead doorway opening framed for `prop_service_door.glb`.
    - Above the doorway sits a **`2.40m W × 0.85m H` `alphaMode: "BLEND"` translucent glass inspection transom (`alpha 0.32`)** over the emitter header, so the player can directly see the `#88929E` brushed-steel emitter coil banks and their `#D95B26` signal-orange coil-phase indicator bars drift out of sync (Scan 1 stall at ~40% strength) and lock back into alignment (Scan 2) whenever the door is scanned!
    - Right of the doorway (`X = +1.55m, Z = -3.75m`): The **Interactive RFID Induction Pedestal (`Pedestal_RFID_Main`)** at `1.15m` wrist height, ringed with a `#00E5FF` / `#FF9500` circular induction halo and a 3-node calibration progress bar (`Node_Calib_01..03`) mounted on the upper door header.
    - Left of the doorway (`X = -1.85m, Z = -3.82m`): The **Recessed Wall Maintenance Junction (`Relay_Panel_B`)** with an open `alphaMode: "BLEND"` inspection cover (`alpha 0.34`), `#D95B26` signal-orange service conduit, and the socket where `char_assistant_droid` plugs in during Scan Cycle 2.
  - **East Wall (`X = +5.0m`, Cylinder Promenade Sightline Window):**
    - A sweeping **`5.60m W × 2.40m H` `alphaMode: "BLEND"` panoramic structural viewport (`alpha 0.30`)** with chamfered `#1A1E24` titanium mullions looking out onto the sunlit `5500K` Sector-4 Promenade and overhead curved O'Neill valley sky—grounding the vestibule inside the thriving cycler habitat.
    - Below the window sits a cantilevered `#D8DEE6` aerospace-white and `#282E38` carbon-slate **Commuter Waiting Bench (`3.2m L`)** with two stowed commuter carry-on cases (`#88929E` brushed aluminum shells with `#D95B26` latches).
  - **West Wall (`X = -5.0m`, Technician Tool Alcove & Conduit Spine):**
    - Exposed floor-to-ceiling Aegis-7 modular wall ribs (`1.5m` pitch), an open **Technician Service Cart / Tool Rack** with `#D95B26` clamp mounts (marking where Rostov set down their gear upon arriving on the service call), and an illuminated floor-recessed power conduit (`alphaMode: "BLEND"` floor grating) running directly from `Relay_Panel_B` to the bulkhead door threshold.
  - **Floor & Ceiling (`Y = 0.0m` to `Y = 4.2m`):**
    - Non-slip dark carbon slate (`#282E38`) deck plates with `#D95B26` signal-orange caution chevrons around the door swing zone and a glowing `#FF9500` -> `#00E5FF` status threshold strip across the doorway.
    - Coffered `#1A1E24` gunmetal ceiling grid with twin linear `4800K` diffused light troughs (`#D8DEE6`) and overhead cable trays.

---

### 4.2 `prop_service_door.glb` — Malfunctioning Commuter Force-Field Door (emitter frame `2.40m W × 2.60m H × 0.38m D`) *(revised 2026-10-30: force field, no leaves)*
- **Node Hierarchy for Gage's 3-Stage Field States:**
  - `Door_Frame_Root`: Heavy chamfered `#1A1E24` gunmetal titanium outer frame with 3 header calibration ring nodes (`Header_Node_01`, `Header_Node_02`, `Header_Node_03`).
  - `Field_Plane` (`2.20m W × 2.50m H`): translucent field sheet (`alphaMode: "BLEND"`, scrolling-shimmer material) with a collider that's toggled on and off. Strength goes 100% (lockout, amber tint) → ~40% flicker/stall (Scan 1) → full drop and re-raise (Scan 2) → 0% (Scan 3).
  - `Emitter_Coil_A` / `Emitter_Coil_B`: left/right emitter coil banks in the jamb rails, with `#D95B26` coil-phase indicator bars in the header that are visibly out of phase on Scan 1 and realign on Scan 2. No leaves, drive racks, counterweight or latch dogs.

---

### 4.3 `char_assistant_droid.glb` — Aegis-7 Maintenance Assistant Droid (`Unit A7-D2`, `1.15m H × 0.68m W × 0.72m D`)
- **Role in Scene:** Rostov's waist-high mobile diagnostic partner assigned to the service call.
- **Silhouette & Detailing:**
  - Compact 65/35 asymmetric chassis in matte aerospace white (`#D8DEE6`) and anodized gunmetal (`#1A1E24`) riding on a twin-gyro omni-wheel / articulated stability-leg base (`#282E38`).
  - **Articulated Upper Gimbal Head:** Features an `alphaMode: "BLEND"` domed optic visor (`alpha 0.32`) housing an expressive `#00E5FF` cyan / `#FF9500` amber circular status eye and a side-mounted work spotlight.
  - **Interactive Dorsal/Front RFID Handshake Ring:** A prominent `#D95B26` signal-orange collar on its upper chassis ringed with `#00E5FF` cyan inductive emitters so the player can scan the droid with their raised wrist during Scan Cycle 2.
  - **Articulated Diagnostic Probe Arm:** A 3-joint `#88929E` brushed steel manipulator arm on its right flank that extends into the wall junction (`Relay_Panel_B`) to hold the counterweight circuit in phase while the player scans.

---

### 4.4 `char_citizen_commuter.glb` — Waiting Hab-7 Civilian Commuter (`1.78m H`, Instanced as 2 Distinct Commuters)
- **Role in Scene:** The two civilian passengers waiting for Rostov to finish fixing the Sector-4 commuter bulkhead door so they can catch the axial transit shuttle.
- **Wordless Teaching Pose & Animation Hooks:**
  - Dressed in sleek, non-industrial **Aegis-7 Civilian Transit Attire**: tailored matte white (`#D8DEE6`) and slate (`#282E38`) high-collar commuter jacket, slim trousers, a cross-body commuter courier bag with `#D95B26` strap buckle, and a civilian-grade `#00E5FF` wrist pass band on the left wrist.
  - **Articulated Left Arm / Wrist (`Arm_L_Commuter`):** Rigged so Gage can animate Commuter A periodically stepping toward the door pedestal and **raising their left wrist up to chest/center-view height** toward the RFID pad (demonstrating the exact hand-raise gesture to the player without a single word of UI text!).

---

## 5. Summary of Required Deliverables & Paths

1. **5 Wrist RFID Hero Candidates (`wrist_rfid_round1` for 6-Bot Protocol Vote):**
   - `/workspace/game-project/godot/assets/models/props/wrist_rfid/prop_wrist_rfid_r1_01.glb` .. `prop_wrist_rfid_r1_05.glb`
   - `/workspace/game-project/godot/renders/props/wrist_rfid/wrist_rfid_round1_voting_sheet.png`
2. **Preface Test Environment Kit & Interactive Test Scene:**
   - `/workspace/game-project/godot/assets/models/environments/preface_service_call_room.glb`
   - `/workspace/game-project/godot/assets/models/props/service_door/prop_service_door.glb`
   - `/workspace/game-project/godot/assets/models/characters/char_assistant_droid.glb`
   - `/workspace/game-project/godot/assets/models/characters/char_citizen_commuter.glb`
   - `/workspace/game-project/godot/scenes/preface_service_call_test.tscn`
   - `/workspace/game-project/godot/renders/preface/preface_test_environment_showcase_sheet.png` (showing the 3-cycle RFID door troubleshooting loop, the raised center-screen wrist scan, the waiting commuters demonstrating the wrist gesture, and the assistant droid counterweight handshake)
