# Aegis-7 Orbital Crew & Explorer Character Specification (`char_crew_round1` + Articulated `WalkCycle` Animation)
**Author:** Vance (`0724beeb-94b9-43fa-a9cf-27117c5d4aa6`) — Sci-Fi Architect, Movie Prop & Set Design Specialist (with Sloane, Rook, Gage, Scribe & Atlas)
**Canonical Path:** `/workspace/game-project/design/character_aegis7_crew_spec.md`
**Candidate Models Path:** `/workspace/game-project/assets/glb/character/char_crew_round1/char_crew_r1_01.glb` .. `char_crew_r1_05.glb`
**Canonical Winner Path:** `/workspace/game-project/assets/glb/winners/char_crew_winner_01_aegis7_commander.glb`
**Renders & Animation Showcase Sheets:**
- Static/Posed 5-Candidate Voting Sheet: `/workspace/game-project/godot/renders/character/char_crew_round1/char_crew_round1_voting_sheet.png`
- 4-Phase + Multi-Angle `WalkCycle` Animation Sheet: `/workspace/game-project/godot/renders/character/char_crew_round1/char_crew_walk_cycle_sheet.png`

---

## 1. Human Scale, Heroic Proportions & Technical Budget
Every Aegis-7 crew character model (`char_crew_r1_01.glb` through `char_crew_r1_05.glb`) is engineered to anchor human scale (`1.80m`) inside our 10 interior rooms, 4 exterior districts, and the 800m × 400m O'Neill Cylinder megastructure:

1. **Exact Dimensions & World Origin:**
   - **Total Standing Height:** `1.800m` (`min_y = 0.00000` at the bottom soles of the magnetic EVA boots; helmet crown at `Y = 1.800m`; eye level at `Y = 1.655m`).
   - **Floor Pivot:** `(0.0, 0.0, 0.0)` centered directly between the left and right boot heels at floor level (`Y = 0.0`).
   - **Forward Facing Axis:** `+Z` (with glTF hierarchical node animation cleanly driving forward stride along `+Z`).
   - **Triangle Budget:** `3,500 – 6,000` triangles per `.glb` candidate (sweet spot `~4,200 – 5,400` tris), guaranteeing crisp chamfered armor bevels, articulated limbs, and a sculpted 3D interior human head/face inside the translucent helmet visor.
2. **7.5–8-Head Heroic Hard Sci-Fi Proportions (No Blocky Stick-Figures):**
   - **Head & Helmet Assembly (`Y = 1.54m .. 1.80m`):** Pressurized chamfered titanium neck-seal collar (`#1A1E24`), sculpted 3D interior human head (cranial vault, brow ridge, nose bridge, jawline, ears, comms headset boom mic, and illuminated cyan optical HUD visor arc), enclosed within a **true `alphaMode: "BLEND"` translucent polycarbonate helmet dome/visor (`alpha = 0.32–0.38`)**.
   - **Torso & Chest Cuirass (`Y = 0.98m .. 1.54m`):** Broad V-tapered anatomical chest plate in Matte Aerospace White (`#D8DEE6`) over a Dark Carbon-Slate (`#282E38`) ribbed ballistic pressure-suit abdomen, dorsal life-support backpack (`Z = -0.14m .. -0.26m`), and chest-mounted telemetry/breather console with Signal-Orange (`#D95B26`) emergency O2 purge latches.
   - **Pelvis & Utility Belt (`Y = 0.86m .. 0.98m`):** Contoured hip chassis with 45°-chamfered gunmetal (`#1A1E24`) utility belt pouches and brushed-steel (`#88929E`) EVA tether D-rings.
   - **Articulated Arms & Gloved Hands (`Shoulder Y = 1.44m` down to `Fingertip Y = 0.72m`):** Sculpted shoulder pauldrons, bicep armor sleeves, ribbed carbon-slate elbow joints, tapered forearm gauntlets (with left-arm illuminated cyan `#00E5FF` OLED wrist-holo-pad), and 3D gloved hands with distinct thumb and finger-cluster geometry.
   - **Articulated Legs & Magnetic EVA Boots (`Hip Y = 0.88m` down to `Sole Y = 0.00m`):** Contoured upper thigh plates, articulated knee guards (`Y = 0.48m`), sculpted shin greaves, ankle flexion cuffs, and heavy magnetic-grip EVA boots (`#1A1E24` gunmetal chassis, `#88929E` machined steel mag-soles, and `#FF9500` amber heel-strike telemetry LEDs).

---

## 2. Unified Aegis-7 Suit Material & Cinema Prop Language (*Oblivion*, *The Martian*, *Alien*, *2001*, *Interstellar*)
All 5 character candidates share our `< 1.2%` low-noise Aegis-7 PBR material palette:

| Material Slot | Hex / PBR Parameters | Suit & Prop Component Assignment |
| :--- | :--- | :--- |
| `Mat_Suit_AerospaceWhite` | `#D8DEE6` (`metal 0.08`, `rough 0.28`) | Contoured chest cuirass, shoulder pauldrons, thigh plates, shin greaves, forearm gauntlets, helmet crown |
| `Mat_Suit_GunmetalTitanium` | `#1A1E24` (`metal 0.78`, `rough 0.34`) | Helmet neck-lock ring, dorsal spine exoskeleton, hip chassis, knee/elbow armor caps, EVA boot upper chassis |
| `Mat_Suit_CarbonSlateUnder` | `#282E38` (`metal 0.25`, `rough 0.52`) | Flexible ribbed pressure-suit underlayer at neck, shoulders, elbows, abdomen, groin/hips, knees, and gloves |
| `Mat_Suit_BrushedSteel` | `#88929E` (`metal 0.90`, `rough 0.22`) | Life-support umbilical couplings, magnetic boot soles, dorsal thruster nozzles, shoulder camera gimbals |
| `Mat_Suit_SignalOrange` | `#D95B26` (`metal 0.25`, `rough 0.36`) | Chest O2 purge latch, shoulder EVA rescue grab-handles, utility belt emergency beacon, harness buckles |
| `Mat_Skin_CrewHead` | `#D6A88E` (`metal 0.02`, `rough 0.58`) / `#2C323B` hair & headset | Sculpted 3D interior human face/head, brow, nose, jaw, and comms earpiece visible through helmet visor |
| `Mat_Emissive_CyanHUD` | `#00E5FF` (`emission 2.2`) | Helmet internal HUD visor arc, chest biomonitor heart-line strip, left-forearm wrist-holo-projector, backpack core |
| `Mat_Emissive_AmberLED` | `#FF9500` (`emission 2.0`) | Boot heel-strike gravity indicators, shoulder strobe beacons, tactical visor trim |
| `Mat_Emissive_UVViolet` | `#7B5CFF` (`emission 2.0`) | Bio-scanner / cryo-coolant telemetry accents (`#02` & `#04`) |
| `Mat_Glass_HelmetVisor` | `#7CE8FF` (`alphaMode: "BLEND"`, `a = 0.32`, `rough 0.06`, `metal 0.15`) | Translucent anti-reflective polycarbonate helmet visor & dorsal cryo-cell window |

---

## 3. The 5-Candidate Aegis-7 Orbital Crew Lineup (`char_crew_r1_01.glb` – `char_crew_r1_05.glb`)

### Candidate `#01` (`char_crew_r1_01.glb`) — Aegis-7 Standard Symmetric Orbital Flight-Suit Officer
- **Target Budget:** `~4,400` tris | **Silhouette:** Clean, classic *2001* / *Oblivion* symmetrical orbital flight officer.
- **Design Features:** Symmetrical matte aerospace-white (`#D8DEE6`) chest cuirass and rounded shoulder pauldrons, centered cyan (`#00E5FF`) chest status bar, panoramic spherical `alphaMode: "BLEND"` bubble visor revealing the sculpted 3D officer head and headset inside, and a compact symmetrical gunmetal (`#1A1E24`) dorsal O2 pack.

### Candidate `#02` (`char_crew_r1_02.glb`) — Dual-Zone Split Aegis-7 Flight-Suit Commander & Translucent Life-Support / Holo-Telemetry Rig (Aegis-7 65/35 Asymmetric Split-Rig Signature)
- **Target Budget:** `~4,950` tris | **Silhouette:** Our signature **Aegis-7 65/35 Asymmetric Split-Rig Commander**—combining heroic spacecraft armor with unmistakable movie-prop functional asymmetry:
  - **Asymmetric Chest & Shoulder Rig (65/35 Split):**
    - **Left 65% Primary Armor Zone:** Contoured matte aerospace-white (`#D8DEE6`) & chamfered gunmetal (`#1A1E24`) commander breastplate integrated with a diagonal **Signal-Orange (`#D95B26`) Quick-Release EVA Harness Strap & O2 Valve Latch**.
    - **Right 35% Secondary Telemetry Zone:** Recessed dark carbon-slate (`#282E38`) & cyan-lit (`#00E5FF`) biomonitor chest matrix paired with a **Right-Shoulder Articulated Brushed-Steel (`#88929E`) Micro-Camera & Laser-Telemetry Beacon Gimbal** (inspired by *Aliens* / *The Martian* EVA rigs).
  - **Asymmetric Forearm Prop Loadout:**
    - **Left Forearm:** Raised **Illuminated Cyan (`#00E5FF`) & `alphaMode: "BLEND"` Translucent Wrist-Holo-Projector Pad** casting a miniature glowing 3D O'Neill Cylinder telemetry ring above the gauntlet.
    - **Right Forearm:** Precision brushed-steel (`#88929E`) magnetic grapple-tether coupling with `#D95B26` release trigger.
  - **Dual-Zone Split Dorsal Life-Support Backpack:**
    - **Left 65% Module:** Chamfered gunmetal (`#1A1E24`) & aerospace-white primary O2/N2 pressure housing with brushed-steel micro-thruster vernier nozzles.
    - **Right 35% Module:** Full-height **`alphaMode: "BLEND"` Translucent Cyan/UV-Violet (`#00E5FF` / `#7B5CFF`) Cryo-Coolant & Biomonitor Cell Column** revealing 3D internal glowing coolant coils and battery cells!
  - **Chamfered Panoramic Helmet & Sculpted 3D Commander Head:**
    - 45°-chamfered aerospace-white helmet shell with twin amber (`#FF9500`) temple beacons and a crystal-clear **`alphaMode: "BLEND"` (`alpha = 0.32`) faceted panoramic visor** revealing the sculpted 3D commander head, facial features, comms mic boom, and an internal floating cyan (`#00E5FF`) HUD reticle arc.

### Candidate `#03` (`char_crew_r1_03.glb`) — Heavy Zero-G EVA & Shipyard Rig Engineer
- **Target Budget:** `~4,800` tris | **Silhouette:** Heavy-duty *Alien* / *Outland* industrial orbital shipyard & drydock engineer (`bldg_13` / `bldg_16` crew).
- **Design Features:** Reinforced chamfered gunmetal (`#1A1E24`) exo-shoulder roll-cage frame with high-visibility Signal-Orange (`#D95B26`) hazard chevrons, twin cylindrical dorsal MMU nitrogen thruster pods with brushed-steel (`#88929E`) nozzles, heavy magnetic clamp boots, and an armored slot-framed `alphaMode: "BLEND"` visor over the 3D engineer head.

### Candidate `#04` (`char_crew_r1_04.glb`) — Bio-Science & Medical Recon Specialist
- **Target Budget:** `~4,550` tris | **Silhouette:** Sleek, lightweight *Prometheus* / *Elysium* medical & agri-biosphere specialist (`bldg_04` / `bldg_06` crew).
- **Design Features:** Streamlined aerospace-white (`#D8DEE6`) contoured biosuit with emerald (`#00E676`) and UV-violet (`#7B5CFF`) bio-isolation trim, a dorsal `alphaMode: "BLEND"` translucent medical cryo-sample canister pack, and a wide geodesic `alphaMode: "BLEND"` visor revealing the 3D specialist head and surgical HUD halo.

### Candidate `#05` (`char_crew_r1_05.glb`) — Orbital Security & Point-Defense Tactical Recon Suit
- **Target Budget:** `~4,700` tris | **Silhouette:** Angular faceted *Oblivion* / *Expanse* orbital defense & citadel overwatch officer (`bldg_11` / `bldg_20` crew).
- **Design Features:** Angular 45°-faceted dark gunmetal (`#1A1E24`) and carbon-slate (`#282E38`) stealth composite plating, warm amber (`#FF9500`) & cyan (`#00E5FF`) tactical IFF strips, dorsal tachyon comms fin, and an angled `alphaMode: "BLEND"` smoked-cyan visor with an internal amber HUD targeting bar over the 3D head.

---

## 4. Articulated Humanoid Hierarchy & Biomechanical `WalkCycle` Animation Specification

Every `.glb` file (`char_crew_r1_01.glb` .. `char_crew_r1_05.glb`) must embed a **18-node articulated humanoid hierarchy** and a **seamlessly looping 1.20-second (`30 FPS`, `37 keyframes`, `t = 0.00s .. 1.20s`) glTF 2.0 `WalkCycle` animation** so the character walks smoothly in Godot 4 without foot sliding or robotic stiffness:

### 4.1 Hierarchical Node Tree & Joint Pivot Coordinates (Standing Rest Pose at `t = 0.0s` Reference)
All joint pivots are placed at exact anatomical rotation centers so rotating any limb node produces zero mesh tearing or gap separation (overlapping spherical/cylindrical carbon-slate `#282E38` joint ball-and-socket cuffs bridge every joint!):

- `Root` (`(0.0, 0.0, 0.0)` — ground origin between feet)
  - `Hips` (`(0.0, 0.92, 0.0)` — pelvis center of mass; drives vertical walk bob `Δy`, lateral sway `Δx`, and pelvic tilt/roll/yaw)
    - `Spine` (`(0.0, 0.14, 0.0)` relative to `Hips`, world `Y = 1.06m` — lower lumbar pivot)
      - `Chest` (`(0.0, 0.22, 0.0)` relative to `Spine`, world `Y = 1.28m` — thoracic ribcage, cuirass & dorsal backpack; counter-rotates in yaw against `Hips`)
        - `Neck` (`(0.0, 0.26, 0.0)` relative to `Chest`, world `Y = 1.54m` — helmet collar ring)
          - `Head` (`(0.0, 0.06, 0.0)` relative to `Neck`, world `Y = 1.60m` — 3D human head, HUD & `alphaMode: "BLEND"` helmet visor; stabilized gaze)
        - `Shoulder_L` (`(+0.21, 0.18, 0.0)` relative to `Chest`, world `Y = 1.46m`)
          - `UpperArm_L` (`(0.0, 0.0, 0.0)` — left pauldron & bicep)
            - `LowerArm_L` (`(0.0, -0.28, 0.0)` relative to `UpperArm_L`, world `Y = 1.18m` — left elbow & wrist-holo-pad)
              - `Hand_L` (`(0.0, -0.24, 0.0)` relative to `LowerArm_L`, world `Y = 0.94m` — left gloved hand)
        - `Shoulder_R` (`(-0.21, 0.18, 0.0)` relative to `Chest`, world `Y = 1.46m`)
          - `UpperArm_R` (`(0.0, 0.0, 0.0)` — right pauldron & bicep)
            - `LowerArm_R` (`(0.0, -0.28, 0.0)` relative to `UpperArm_R`, world `Y = 1.18m` — right elbow & grapple gauntlet)
              - `Hand_R` (`(0.0, -0.24, 0.0)` relative to `LowerArm_R`, world `Y = 0.94m` — right gloved hand)
    - `UpperLeg_L` (`(+0.115, -0.04, 0.0)` relative to `Hips`, world `Y = 0.88m` — left hip socket)
      - `LowerLeg_L` (`(0.0, -0.40, 0.0)` relative to `UpperLeg_L`, world `Y = 0.48m` — left knee hinge)
        - `Foot_L` (`(0.0, -0.38, 0.0)` relative to `LowerLeg_L`, world `Y = 0.10m` — left ankle & magnetic EVA boot)
    - `UpperLeg_R` (`(-0.115, -0.04, 0.0)` relative to `Hips`, world `Y = 0.88m` — right hip socket)
      - `LowerLeg_R` (`(0.0, -0.40, 0.0)` relative to `UpperLeg_R`, world `Y = 0.48m` — right knee hinge)
        - `Foot_R` (`(0.0, -0.38, 0.0)` relative to `LowerLeg_R`, world `Y = 0.10m` — right ankle & magnetic EVA boot)

### 4.2 Biomechanical `WalkCycle` Keyframe Equations (`T = 1.20s`, `ω = 2π / T`, Phase `φ ∈ [0, 2π]`)
Using smooth sinusoidal harmonic curves across `37` samples (`t_k = k / 30.0` for `k = 0..36`, where `k = 36` matches `k = 0` to `1e-6` precision for zero loop pop):

1. **Pelvis (`Hips`) Double-Frequency Vertical Bob, Lateral Sway & Counter-Tilt:**
   - **Vertical Bob (`Y` translation):** Peaks at mid-stance (`φ = π/2, 3π/2`) and dips at heel-strike (`φ = 0, π`):
     `y_hips(φ) = 0.920 - 0.024 * cos(2φ)` (`±2.4cm` natural human gait oscillation).
   - **Lateral Weight Shift (`X` translation):** Shifts over the supporting leg:
     `x_hips(φ) = -0.018 * sin(φ)`.
   - **Pelvic Rotation (`pitch_x`, `yaw_y`, `roll_z`):**
     - Forward lean: `+3.5° + 1.5° * cos(2φ)`
     - Pelvic axial twist (`yaw_y`): `+5.5° * cos(φ)` (left hip rotates forward as left leg swings forward at `φ = 0`)
     - Pelvic coronal list (`roll_z`): `+3.0° * sin(φ)`
2. **Upper Legs (`UpperLeg_L` at phase `φ`, `UpperLeg_R` at phase `φ + π`):**
   - **Hip Flexion/Extension (`pitch_x`):** Swings from `+24°` forward flexion at heel-strike (`φ = 0`) to `-20°` rear extension at toe-off (`φ = π`):
     `pitch_thigh(θ) = -22.0° * cos(θ) + 2.0°` (where `θ = φ` for Left, `θ = φ + π` for Right).
3. **Lower Legs / Knees (`LowerLeg_L` at `φ`, `LowerLeg_R` at `φ + π`):**
   - **Knee Flexion (`pitch_x`, always bends backward):** Combines a slight `8°` shock-absorption bend during weight-bearing stance (`θ ∈ [0, π]`) with a crisp `44°` foot-clearance lift during mid-swing (`θ ≈ 3π/2`):
     `pitch_knee(θ) = 22.0° * max(0, -sin(θ))^1.3 + 7.0° * max(0, sin(θ)) + 4.0°`.
4. **Feet / Ankles (`Foot_L` at `φ`, `Foot_R` at `φ + π`):**
   - **Ankle Dorsiflexion / Plantarflexion (`pitch_x`):** Heel-up dorsiflexion (`-12°`) at contact (`θ = 0`), plantar push-off (`+18°`) at toe-off (`θ = π`), and toe-up clearance (`-10°`) during mid-swing (`θ = 3π/2`):
     `pitch_foot(θ) = 14.0° * sin(θ - 0.35) - 6.0° * cos(2θ)`.
5. **Torso & Chest Counter-Rotation (`Spine` & `Chest`):**
   - **Thoracic Counter-Twist (`yaw_y`):** Opposes pelvic rotation to keep momentum balanced:
     `yaw_chest(φ) = -6.5° * cos(φ)`, `pitch_chest(φ) = +4.0° + 1.2° * cos(2φ)`.
   - **Head Stabilization (`Head`):** Compensates for chest yaw (`yaw_head(φ) = +4.5° * cos(φ)`) so the commander's helmet visor looks steadily down the promenade!
6. **Natural Counter-Swinging Arms (`UpperArm_L` at `φ + π`, `UpperArm_R` at `φ`):**
   - Left arm swings forward when Right leg steps forward (`φ = π`), and Right arm swings forward when Left leg steps forward (`φ = 0`):
     - `pitch_upper_arm(α) = -20.0° * cos(α) + 4.0°`
     - `pitch_lower_arm(α) = -20.0° - 14.0° * max(0, -cos(α))` (natural `20°` baseline elbow bend flexing to `34°` on the forward swing).

---

## 5. Godot 4 Showcase & Multi-Phase `WalkCycle` Contact Sheet Requirements (For Gage)
1. **5-Candidate Voting Sheet (`/workspace/game-project/godot/renders/character/char_crew_round1/char_crew_round1_voting_sheet.png`):**
   - Renders `char_crew_r1_01.glb` through `char_crew_r1_05.glb` at `t = 0.15s` (dynamic mid-stride heroic pose) on an illuminated Aegis-7 octagonal turntable pad against the O'Neill Cylinder backdrop, highlighting the `alphaMode: "BLEND"` visor, 3D interior head, and 65/35 split-rig details on `#02`.
2. **4-Phase `WalkCycle` Animation Showcase Sheet (`/workspace/game-project/godot/renders/character/char_crew_round1/char_crew_walk_cycle_sheet.png`):**
   - Captures locked winner `#02` (`char_crew_winner_01_aegis7_commander.glb` / `char_crew_r1_02.glb`) across 4 distinct keyframe phases of the embedded `WalkCycle` animation (`t = 0.00s` `[0% Heel Strike Contact]`, `t = 0.30s` `[25% Mid-Stance Passing]`, `t = 0.60s` `[50% Opposite Contact]`, `t = 0.90s` `[75% Opposite Passing]`) plus a 3/4 rear/side view showing the Dual-Zone Split Backpack (`alphaMode: "BLEND"` cryo-coolant column) and an in-situ walk render on the Cylinder Hab-7 Civic Promenade!

---

## 6. Addendum: Distinct Facial Sculpts, Retracted/Open Headgear & Close-Up Portrait Headshot Specification (`char_crew_headshots_sheet.png`)

To ensure all 5 character candidates (`#01`–`#05`) read as **unmistakably distinct individuals** in both close-up portrait headshots (`Y = 1.42m..1.84m`, tight 50mm–85mm portrait framing on head, face, neck, and upper shoulders) and full-body silhouettes, each candidate must feature **exposed, unobstructed facial geometry** (retracted flip-up visor crown, asymmetric open half-cowl, open roll-cage frame, or visorless neural-headband/eyewear) paired with unique cranial proportions, skin tone, hair/facial-hair sculpt, cybernetic/optical implants, and collar/shoulder color blocking:

### 6.1 Individual Portrait, Facial Sculpt & Headgear Breakdown (`#01`–`#05`)

1. **Candidate `#01` (`char_crew_r1_01.glb`) — Standard Symmetric Flight-Suit Officer ("Lt. Marcus Vance-Lin")**
   - **Facial Sculpt & Skin Tone:** Clean-shaven, chiseled athletic jawline, warm bronze skin (`#B87D56`), defined brow ridge, dark-brown eyes with corneal specular highlights, and a neatly parted dark-espresso crew cut (`#231A14`) with sculpted side-taper volume.
   - **Open/Retracted Headgear & Collar:** Retracted aerospace-white (`#D8DEE6`) and cobalt-blue (`#1E6091`) **flip-up flight visor crown** resting open above the forehead (`alphaMode: "BLEND"` cyan upper visor rim raised completely clear of the eyes/nose/mouth), compact dual-ear comms pods, and a symmetrical matte aerospace-white gorget collar with twin cyan (`#00E5FF`) collar pips.

2. **Candidate `#02` (`char_crew_r1_02.glb`) — Dual-Zone Split Aegis-7 Commander ("Commander Kaelen Rostov" — HERO SIGNATURE)**
   - **Facial Sculpt & Skin Tone:** Seasoned, commanding visage with strong cheekbones, medium warm olive skin (`#C68E68`), swept-back charcoal-dark hair (`#1E2229`) with **distinct silver-grey temple streaks (`#C0C8D2`)**, a sculpted **trimmed full beard & mustache (`#242830`)**, and a subtle cheek scar on the right zygomatic arch.
   - **Asymmetric 65/35 Split Headgear, AR Monocle & Collar:**
     - **Left Side (35% Tech/Telemetry):** Illuminated **Cyan (`#00E5FF`) `alphaMode: "BLEND"` Holographic AR Targeting Monocle/Reticle** suspended over the left eye from a brushed-steel (`#88929E`) temple mount + articulated jaw-boom microphone.
     - **Right Side (65% Armored Cowl):** Retracted split gunmetal (`#1A1E24`) & aerospace-white (`#D8DEE6`) half-cowl sweeps back behind the right ear, leaving the commander's entire face, silver-streaked hair, and beard completely unobstructed in portrait view!
     - **Shoulder & Collar Silhouette:** High asymmetric **Signal-Orange (`#D95B26`)** left EVA harness latch & chest strap paired with a right-shoulder articulated brushed-steel camera gimbal pod and glowing cyan lens ring.

3. **Candidate `#03` (`char_crew_r1_03.glb`) — Heavy Zero-G EVA & Shipyard Exo-Harness Engineer ("Chief Engineer Tarek Mensah")**
   - **Facial Sculpt & Skin Tone:** Broad, heavy-set rugged features, deep rich umber skin (`#5C3824`), wide square jaw with a heavy chin goatee (`#181210`), and sculpted **textured braided/locked hair rows** pulled back at the crown.
   - **Industrial Open Roll-Cage Headgear & Collar:** No glass dome over the face—instead, an open-front **Caterpillar-Amber / Signal-Yellow (`#FFB703`) & Gunmetal (`#1A1E24`) octagonal tubular exo-roll-cage frame** surrounds the head with a dual-LED forehead floodlamp bar (`#FFF3D1` emissive), a heavy left-cheek acoustic bone-conduction jaw mic, and a thick ribbed hydraulic neck-ring with hazard chevron plates.

4. **Candidate `#04` (`char_crew_r1_04.glb`) — Botanical & Hydro-Biosphere Medical Recon Specialist ("Dr. Soren Sato")**
   - **Facial Sculpt & Skin Tone:** Angular, refined East-Asian facial structure, pale warm ivory skin (`#E5B89B`), slender jawline, and a striking **asymmetric platinum-silver & bioluminescent-emerald-tipped (`#52B788`) angled bob haircut** sweeping across the right brow.
   - **Helmetless Neural-Headband & Holo-Eyewear:** **Zero helmet shell**—wears a sleek temple-hugging **Bioluminescent Emerald (`#00E676`) & UV-Violet (`#7B5CFF`) neural-telemetry headband** paired with ultra-thin frameless `alphaMode: "BLEND"` cyan/emerald **holographic diagnostic glasses** resting across the nose bridge, plus a high contoured white/emerald medical isolation collar (`#D8DEE6` / `#52B788`) with glowing UV-violet bio-sterilizer pips.

5. **Candidate `#05` (`char_crew_r1_05.glb`) — Citadel Command & Point-Defense Tactical Recon ("Spec-Ops Recon Vesper Kade")**
   - **Facial Sculpt & Skin Tone:** Sharp, gaunt high-cheekbone tactical profile, cool tan skin (`#AD795B`), buzzed military side-undercut with a high charcoal-platinum mohawk crest, a sculpted **amber/crimson (`#FF5500`) cybernetic neural temple implant** on the left forehead, and a vertical brow scar.
   - **Faceted Stealth Half-Cowl & Tactical Visor Strip:** Wears an angular faceted **Carbon-Slate (`#282E38`) & Anodized Gunmetal (`#1A1E24`) lower jaw/cheek rebreather guard** with glowing **Amber (`#FF9500`) IFF slits**, a narrow wrap-around amber/cyan tactical optic visor strip across the eyes (leaving the upper forehead, cybernetic temple implant, and hair crest fully exposed), and a dorsal stealth sensor fin rising behind the neck.

---

### 6.2 Close-Up Portrait Headshot Showcase Sheet Requirements (`character_headshots_showcase_sheet.png`)
In addition to regenerating `character_crew_round1_voting_sheet.png` and `character_walk_cycle_showcase_sheet.png` with these 5 distinct head/face/headgear models:
- **Gage (`render_character_showcase.gd`):** Render a dedicated 5-panel (or 6-panel with `#02` 3/4 portrait hero) **Close-Up Portrait Headshot Sheet** at `/workspace/game-project/godot/renders/character/character_headshots_showcase_sheet.png` (plus individual `headshot_01.png` .. `headshot_05.png`):
  - **Camera Framing:** Tight portrait lens (`FOV = 28°–32°`), camera positioned at `Y = 1.62m`, distance `0.55m–0.68m` in front of the head (`Z = +0.62m`, slight `12°` 3/4 portrait angle), framing from mid-chest/shoulder pauldrons (`Y = 1.32m`) to above the head crest (`Y = 1.86m`).
  - **Portrait Rim & Catchlight Rig:** Warm key light (`#FFE8C8`) to bring out skin-tone subsurface warmth, hair sculpt planes, eye catchlights, and facial hair, paired with signature Aegis-7 cyan (`#00E5FF`) and amber (`#FF9500`) rim kickers.
