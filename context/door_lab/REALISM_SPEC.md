# Door Lab: Realism Spec (Vance, 2026-11-20)

Scene `res://scenes/test/door_lab.tscn`. This file covers **mechanism realism only**: sequence, mass, kinematics, hardware, gaps and audio timing. The look belongs to Sloane (`AESTHETIC_SPEC.md`), and the pass bar belongs to Patch (`QUALITY_BAR.md`). Sector doors are force fields and are **not** covered. These are the mechanical tower, service and bulkhead doors.

Units: s, m, mm, kg, deg. Every timestamp is measured from the request (t = 0). "Leaf travel" is the distance from closed (0) to open. Lamp colours follow AESTHETIC_SPEC §3: red = locked, amber = closed idle, cyan = moving, green = open, red/amber blink = fault.

---

## 0. General rules (all door types)

### 0.1 Velocity profile: jerk-limited S-curve (7-segment trapezoid)
- Every powered move uses a **jerk-limited trapezoidal velocity profile**: jerk-up → constant accel → jerk-down → cruise → jerk-up → constant decel → jerk-down. No linear tweens, and no cubic ease standing in for the whole move. Cubic ease-in-out is acceptable **only** inside the short creep and back-check phases.
- If you need a closed form, use `t_j = a/j` and `t_acc = v/a + t_j`. Distance during accel (or decel) is `d_acc = v·t_acc/2`, and cruise time is `t_c = (d − 2·d_acc)/v`. If `2·d_acc > d`, drop the cruise and lower `v` until `2·d_acc = d`.
- Every number in the tables below came from these formulas, so Grok can regenerate them.
- **Crack-open lurch:** before the S-curve, every door has a short, fast, small move as the latch or seal lets go (stored seal compression plus belt or gear slack). It is a separate phase, not part of the curve.
- **Hard stop / settle:** model it as a damped spring on the final position, `x(t) = A·e^(−ζω_n t)·cos(ω_d t)`. Use `ω_n = 2π·f` with the f, A and ζ values given per door. Stop sampling once |x| < 0.2 mm (or 0.05°).

### 0.2 Godot implementation hints
- **One `DoorProfile` resource per type** holds the phase table below (name, t0, t1, quantity, start, end, v_peak, a, j). A single `sample(t) -> float` evaluates it. Drive it from `_physics_process` on the door script. Prefer this over an AnimationPlayer: the obstruction reverse needs to re-plan from the current position and velocity, and a baked animation can't do that.
- Use AnimationPlayer (or a method track) only for **audio and lamp cue events** fired at phase boundaries. Fire the cues from phase transitions, never from velocity thresholds.
- **Collider follows the leaf.** Each leaf's `*-colonly` shapes live on an `AnimatableBody3D` child of the leaf with `sync_to_physics = true`, which is the same pattern as `tt_movers.gd`. Frame colliders never move.
- **Collider-off window:** a leaf collider may be disabled only while the gap that leaf leaves is **narrower than the player capsule diameter + 0.10 m**. Then the player can't fit through, so nothing can clip. Use it to stop the closing leaf from shoving the capsule into the frame during the last creep or latch phase. Outside that window the collider stays on, and an obstruction triggers the safety reverse (per door below), never a pass-through.
- **Motor whine** is an `AudioStreamPlayer3D` loop with `pitch_scale = 0.8 + 0.4·|v|/v_peak` and `volume_db` ramped over the accel and decel phases. **Roller rumble** is a loop whose volume follows |v|. One-shots (clack, clunk, hiss) play at their exact timestamp, within one physics tick.
- **Headless proof:** log `t, leaf_pos[], leaf_vel[], phase, lamp_state, collider_enabled` every physics tick to `user://door_lab_<type>.csv`. The acceptance checks in §5 are computed from that log.
- **Player sprint (63 m/s in `tt_movers.gd`):** realistic timing can't beat a sprinting player. The lab tests at **walk speed**. In game scenes the proximity trigger radius is `v_player × t_open_to_clear` (time until the clear gap ≥ capsule diameter + 0.1 m). Don't compress the mechanism phases. *(Superseded for the shipped profile by §7, game tempo.)*
- **Lamp sync** (agrees with Sloane): the lamp goes cyan at the **first mechanical event** (latch, equalize valve or dog motor) and green at final settle.

### 0.3 Spin gravity (Hab-7: R = 200 m, 1.0 G nominal, Drum RPM range 0.08–1.45 G)
- ω = √(g/R) = √(9.81/200) = **0.221 rad/s (2.12 rpm)** at 1.0 G, and 0.267 rad/s at 1.45 G.
- **Coriolis:** `a_c = 2ω·v`.
  - A slider leaf at 1.3 m/s gets 0.58 m/s² (about 6% g). A swing-leaf tip at 1.7 m/s gets 0.75 m/s².
  - The effect is transient. Guide rollers and hinge bearings carry it, and it is **not visible at door scale**. **Do not animate any Coriolis deflection.**
  - Spinward/antispinward sliders feel it as a ±6% weight change on the rollers, and axial sliders feel none. Neither shows.
- **Gravity gradient:** g ∝ r, so it varies 1.2% over a 2.4 m door height. That is negligible.
- **Leaf weight:** all masses below are at 1.0 G. Hinges, rollers and counterbalance springs (the floor-hatch torsion bar, §4.6) are sized for **1.45 G** (the Drum RPM max). Every powered door is **actuator- and damper-driven, not gravity-driven**, so its timing is the same at any G.
- **At 0.08 G:**
  - A slider leaf weighs about 4 kgf, so belt jerk could lift it off the track. That is why the **anti-lift rollers are mandatory and visible**.
  - A spring-counterbalanced hatch (torsion bar, §4.6) sized for 1.0 G would spring open: 585 N·m of bar against a 55 N·m weight moment. That is why the hatch uses a **rotary hydraulic damper plus a powered lock** (§4.6).

---

## 1. Bi-parting sliding pocket door (service / tower interior)

### 1.1 Geometry and mass
| Item | Value |
|---|---|
| Clear opening | 2.00 W × 2.30 H m |
| Leaf | 2 leaves, each 1.05 W × 2.40 H × 0.05 T m (25 mm lap into each jamb pocket and the head) |
| Leaf build | aluminium honeycomb sandwich with alloy edge stiles, about 19 kg/m² |
| **Mass per leaf** | **48 kg** (471 N at 1.0 G, 683 N at 1.45 G) |
| Travel per leaf | **1.000 m** (each leaf parks 25 mm inside its pocket mouth, so clear = 2.00 m) |
| Drive | 1 head-mounted brushless DC motor + gearbox driving a toothed belt; leaf L on the upper belt run, leaf R on the lower, so they move mirrored |

### 1.2 Open sequence (both leaves mirrored, 0 ms stagger, since one belt drives both)
| # | Phase | t0–t1 (s) | Motion | Notes |
|---|---|---|---|---|
| 1 | Request / auth | 0.00–0.10 | — | radar/badge |
| 2 | Lamp amber → cyan | 0.10 | — | 0.15 s fade |
| 3 | Bolt retract (head solenoid lock) | 0.10–0.22 | — | |
| 4 | Seal unseat (meeting-stile bulb seals release 3 mm) | 0.22–0.30 | 0 → 3 mm | |
| 5 | Crack-open lurch (belt slack take-up) | 0.30–0.40 | 3 → 15 mm, peak 0.18 m/s | |
| 6 | Accel | 0.40–0.98 | 15 → 394 mm | v → **1.30 m/s**, a = 3.0 m/s², j = 20 m/s³ |
| 7 | Cruise | 0.98–1.15 | 394 → 565 mm | 1.30 m/s |
| 8 | Decel | 1.15–1.73 | 565 → 944 mm | a = 3.0, j = 20 |
| 9 | Creep to stop | 1.73–1.85 | 944 → 1000 mm | cubic ease, ≤ 0.5 m/s at the start |
| 10 | Hard stop / settle on bumper | 1.85–2.00 | overshoot **2 mm**, f = 6 Hz, ζ = 0.6 | lamp **green at 2.00** |

**Total open: 2.00 s** (leaf motion 0.30–1.85 s). Peak opening KE is 41 J per leaf.

### 1.3 Close sequence
| # | Phase | t0–t1 (s) | Motion | Notes |
|---|---|---|---|---|
| 1 | Hold timer expires (default 3.0 s after the zone clears) | 0.00 | — | lamp cyan, chase toward the centre; chime |
| 2 | Pre-warn (no motion) | 0.00–0.40 | — | |
| 3 | Accel | 0.40–1.20 | 1000 → 760 mm | v → **0.60 m/s**, a = 1.0, j = 5 |
| 4 | Cruise | 1.20–1.95 | 760 → 310 mm | 0.60 m/s |
| 5 | Decel | 1.95–2.75 | 310 → 70 mm | |
| 6 | Latch-check creep | 2.75–3.50 | 70 → 0 mm | ≤ 0.10 m/s |
| 7 | Seal contact (3 mm compression) | 3.45–3.50 | | soft thud |
| 8 | Bolt throw | 3.55–3.65 | — | |
| 9 | Lamp → amber (or red if locked) | 3.75 | — | |

**Total close: 3.75 s.** Closing KE is 8.6 J per leaf, which meets the **≤ 10 J** closing limit (EN 16005-style; *real-world ref*).

### 1.4 Obstruction / safety reverse
- **Detection:** jamb light curtain at 0.2 / 0.6 / 1.0 / 1.6 m, an overhead presence radar, and motor-current force sensing at **≥ 150 N static**.
- **Reaction:**
  - Stop at a = 3.0 m/s² (≤ 0.2 s, ≤ 60 mm).
  - Dwell 0.15 s.
  - Reopen to full on the open profile, capped at v = 0.60 m/s.
  - Hold 3 s, then retry.
- **Fault:** after 3 consecutive obstructions the door stays open and the lamp goes to fault blink.
- **Collider-off window:** gap < capsule diameter + 0.1 m, during phase 6 only.

### 1.5 Gaps and clearances (mm)
| Gap | Value |
|---|---|
| Leaf to jamb pocket faces (each side) | 6 |
| Pocket clearance: leaf face to pocket liner | 15 each face; 50 behind the leaf tail at full open |
| Leaf to floor | 8 (bottom guide shoe runs in a 12 deep × 14 wide floor channel) |
| Leaf top to head box soffit | 10 |
| Meeting stiles closed | 0 visible; 2 × 12 mm bulb seals compressed **3** |
| Meeting stiles at bolt release | 6 |
| Leaf lap into pocket at full open | 25 |

### 1.6 Visible hardware checklist
- [ ] Head box 120 H × 150 D with a removable access panel. In service areas leave the **track exposed**, otherwise show the carriage underside through a 20 mm slot.
- [ ] Extruded aluminium overhead track.
- [ ] **2 carriages per leaf**, each with 2 × Ø60 nylon rollers plus an **anti-lift roller** above the track.
- [ ] Toothed belt with a belt clamp bracket on each leaf; motor/gearbox at centre head with a belt tensioner pulley at each end.
- [ ] Floor guide shoe and floor channel.
- [ ] Rubber end-stop bumper in each pocket. *(Amended §13.1: a rubber track end stop at each outer carriage is the primary stop, and the pocket bumper is the secondary backstop.)*
- [ ] Meeting-stile bulb seals.
- [ ] Head solenoid bolt and keeper. *(Amended §13.2: the bolt is spring-thrown vertically (−Y) into a keeper on the leaf and is fail-secure, never gravity-dropped. It engages at least 10 mm.)*
- [ ] Lamp strip on the jamb, both faces.
- [ ] Jamb light-curtain lenses (4 per jamb).
- [ ] Radar head over the opening.
- [ ] **Manual override:** recessed hex-key release plate on the jamb face, plus "MANUAL" pull handles in both leaf edges. Manual push force 90 N.

### 1.7 Audio cues (0 dB = loudest cue of this door)
| t (s) | Cue | Rel. level |
|---|---|---|
| 0.10 | solenoid unlock clack | −6 dB |
| 0.28 | seal unstick "pop" | −18 dB |
| 0.30 → 1.85 | motor whine start → stop (pitch follows v, peak 0.98–1.15) | −12 dB peak |
| 0.40 → 1.80 | roller rumble (volume follows v) | −15 dB |
| 1.85 | bumper thud | 0 dB |
| Close 0.00 | chime | −10 dB |
| Close 0.40 → 3.50 | whine (lower pitch, v 0.6) and rumble | −15 / −18 dB |
| Close 3.48 | seal thud | −8 dB |
| Close 3.60 | bolt clack | −4 dB |

---

## 2. 3-leaf bay door (`tt_entrance_bay_3l` / "tt bay3"), **as built: outswing powered swing**

### 2.1 As-built geometry (from the GLB, local frame)
| Item | Value |
|---|---|
| Frame opening | X −2.00..+2.00, frame plane Z −1.15..−0.95 |
| Leaves | `Leaf_0` X −1.597..−0.603 (hinge −1.597); `Leaf_1` X −0.497..+0.497 (hinge −0.497); `Leaf_2` X +0.603..+1.597 (hinge +1.597, mirrored) |
| Leaf size | **0.994 W × 2.46 H (Y 0.06..2.52) × 0.06 T m**, glazed alloy stile frame + `Door_Scissor` glass |
| Mullion gap | 106 (0.10 m mullion + 3 mm each side) |
| Clear width per leaf at 90° | **≈ 0.877 m** (Rook's figure after the stile and stop projections) |
| Swing | **90° outswing** (`tt_movers.gd` `BAY_YAW = [-90, -90, +90]`, TTQA-031, Rook bd43144) |
| **Mass per leaf** | **62 kg** (glass 12 mm laminated about 30 kg + alloy stiles and rails about 32 kg) |
| Leaf inertia about the hinge | I = m·w²/3 = **20.4 kg·m²** |
| Drive | one concealed overhead electromechanical swing operator per leaf in the head (motor + gearbox + spring return, arm to the leaf), with top/bottom offset pivots |

### 2.2 Open sequence (per leaf; stagger **Leaf_1 0 ms → Leaf_0 +60 ms → Leaf_2 +120 ms**)
| # | Phase | t0–t1 (s) | Angle | Notes |
|---|---|---|---|---|
| 1 | Request / auth | 0.00–0.10 | — | |
| 2 | Lamp → cyan; electric strike release | 0.10–0.22 | — | |
| 3 | Brush weatherseal unseat + lurch | 0.22–0.32 | 0 → 2° | peak 30°/s |
| 4 | Accel | 0.32–0.92 | 2 → 26° | ω → **80°/s**, α = 200°/s², j = 1000°/s³ |
| 5 | Cruise | 0.92–1.32 | 26 → 58° | 80°/s |
| 6 | Decel to back-check | 1.32–1.92 | 58 → 82° | |
| 7 | Back-check creep | 1.92–2.72 | 82 → 90° | ≤ 12°/s, cubic |
| 8 | Hard stop on the hold-open stop | 2.72–2.95 | overshoot **0.8°**, f = 3 Hz, ζ = 0.5 | lamp green when the last leaf settles |

**Total open: 2.95 s** (last leaf **3.07 s**). Peak KE is 19.9 J per leaf, a full-power operator with sensors (ANSI A156.10-style, *real-world ref*).

### 2.3 Close sequence (reverse stagger **Leaf_2 0 → Leaf_0 +60 → Leaf_1 +120 ms**)
| # | Phase | t0–t1 (s) | Angle | Notes |
|---|---|---|---|---|
| 1 | Hold expires; lamp cyan | 0.00 | — | |
| 2 | Pre-warn | 0.00–0.30 | 90° | |
| 3 | Accel | 0.30–1.00 | 90 → 79.5° | ω → **30°/s**, α = 60, j = 300 |
| 4 | Cruise | 1.00–2.97 | 79.5 → 20.5° | |
| 5 | Decel | 2.97–3.67 | 20.5 → 10° | |
| 6 | Latch check | 3.67–4.67 | 10 → 0° | ≤ 10°/s, last 2° at 15°/s (latch kick) |
| 7 | Strike catch, seal compress | 4.67 | | |
| 8 | Lamp amber | 4.75 | | (last leaf 4.87) |

Closing KE is 2.8 J per leaf.

### 2.4 Obstruction / safety reverse
- **Detection:** a swing-side presence sensor covering the full 90° arc (leaf-mounted sensor bar), an approach-side radar, and operator current limit = **67 N at the leading edge**.
- **Reaction:**
  - Stop within 0.15 s.
  - Reopen to 90° at the open profile with ω ≤ 40°/s.
  - Hold 3 s.
- **Behaviour on the approach path:** an outswing leaf swings into the path, so if the opening is blocked the leaf **stalls and holds** instead of reversing.
- **Fault:** after 3 obstructions, fault blink.
- **Collider-off window:** gap < capsule diameter + 0.1 m, during phase 6 only.

### 2.5 Gaps and clearances (mm), as built vs required
| Gap | As built (GLB) | Required |
|---|---|---|
| Leaf to mullion / meeting edge | 3 each side | 3 ✓ |
| Hinge stile to frame (Leaf_0/2 to side panel at ±1.652) | 55 | ≤ 10 visible; cover with a hinge-stile finger guard (55 mm is the finger-guard zone) |
| Leaf to floor | 60 (Y 0.06) over a 12 mm mat = 48 visible | **8**: add a bottom sweep/rail fill; flagged to Rook (read only here) |
| Leaf top to head | 2.52 to the canopy underside 2.66 → head rail zone | 3 to the head stop |
| Leaf to outswing obstacles at 90° | leaf tip about Z −0.05 vs bollards Z +0.405 → **455** | ≥ 300 ✓ |
| Brush weatherseal compression | — | 2 |

### 2.6 Visible hardware checklist
- [ ] Head transom box housing 3 operators.
- [ ] Operator arm (visible drive arm, or a slide arm in a track on the leaf top rail).
- [ ] Top and bottom offset pivots per leaf.
- [ ] Electric strike in the head or mullion.
- [ ] Hinge-stile finger guards.
- [ ] Hold-open floor stop or overhead stop at 90°.
- [ ] Leaf-mounted presence sensor bars on the swing face.
- [ ] Push bars (exist: `Leaf_n_Push_Bar` Y 1.03..1.07).
- [ ] Brush weatherseals on the leaf edges.
- [ ] Lamp strip.
- [ ] **Manual override:** breakaway/emergency push. Any leaf swings manually at 90 N on the push bar with the operator spring-returning.

### 2.7 Audio cues
| t (s, per leaf incl. stagger) | Cue | Rel. level |
|---|---|---|
| 0.12 | strike release clack | −6 dB |
| 0.30 → 2.72 | operator gear whine (3 voices staggered) | −12 dB |
| 2.72 | stop tap | −6 dB |
| Close 0.30 → 4.67 | whine, lower | −15 dB |
| Close 4.67 | latch clack (×3, staggered 60 ms) | 0 dB |

### 2.8 Alternative (Vance proposal, not built): 3-leaf telescoping slider
- This is what Sloane's AESTHETIC_SPEC §1/§6 assumes. If adopted it needs a rebuild by Rook, and it would retire TTQA-031.
- **Layout:** three leaves on three parallel tracks, all stacking to one side. Leaf speeds are in the ratio **1 : 2 : 3**, driven by a cable/pulley ganging.
- **Leaf size:** 3 leaves of 1.05 m each, 45 kg each.
- **Travel and timing:** the fastest leaf travels 2.10 m with v_peak 1.2 m/s, a = 2.5, j = 15. The open profile is the same shape as §1.2, scaled to the fastest leaf. The leaves start together because the cable gangs them, so there is **no stagger in a real one**.
- **Note on Sloane's 60 ms stagger:** a real ganged slider has none. If a stagger is wanted, it is the slack take-up only: ≤ 30 ms and ≤ 5 mm.

---

## 3. Double swing pair (`tt_door_pair_18`)

### 3.1 As-built geometry (GLB, local frame; placed e.g. at **(91.5, 6.1, 14.85) yaw 0**, swinging into the hall **+Z**)
| Item | Value |
|---|---|
| Casing | 1.96 W × 2.48 H × 0.35 D m |
| Leaves | `Leaf_L` X −0.895..−0.004 (pivot −0.90); `Leaf_R` +0.004..+0.895 (pivot +0.90) |
| Leaf size | **0.891 W × 2.38 H (Y 0.01..2.39) × 0.05 T m**, vision panel 0.50 × 1.01 m, kick plate 0.22 m, push bar Y 0.95..1.15 |
| Swing | 90° (`PAIR_DEG = 90`) |
| **Mass per leaf** | **38 kg** (solid composite core + vision glazing) |
| Leaf inertia about the hinge | **10.1 kg·m²** |
| Drive | push-bar actuated with a **power-assist low-profile operator** per leaf in the casing head; hydraulic closer valving (sweep + latch + back-check) |

### 3.2 Open sequence (stagger **Leaf_L leads, Leaf_R +60 ms**)
| # | Phase | t0–t1 (s) | Angle | Notes |
|---|---|---|---|---|
| 1 | Request (proximity or push-bar touch) | 0.00–0.08 | — | |
| 2 | Lamp cyan; electrified rim latch retract | 0.08–0.20 | — | |
| 3 | Smoke-seal unseat + lurch | 0.20–0.28 | 0 → 1.5° | |
| 4 | Accel | 0.28–0.85 | 1.5 → 32.7° | ω → **110°/s**, α = 300, j = 1500 |
| 5 | Cruise | 0.85–1.06 | 32.7 → 55.3° | |
| 6 | Decel | 1.06–1.63 | 55.3 → 86.5° | |
| 7 | Back-check | 1.63–2.03 | 86.5 → 90° | ≤ 12°/s |
| 8 | Stop / settle | 2.03–2.25 | overshoot **1.0°**, f = 3 Hz, ζ = 0.45 | lamp green after Leaf_R settles at 2.31 |

**Total open: 2.25 s** (Leaf_R 2.31 s). Peak KE is 18.6 J per leaf.

### 3.3 Close sequence (stagger **Leaf_R leads, Leaf_L +60 ms**; no coordinator needed, since there is no astragal and both leaves are active)
| # | Phase | t0–t1 (s) | Angle | Notes |
|---|---|---|---|---|
| 1 | Hold expires (2.5 s after clear); lamp cyan | 0.00 | | |
| 2 | Accel (closer sweep) | 0.00–0.70 | 90 → 79.5° | ω → **30°/s**, α = 60, j = 300 |
| 3 | Sweep | 0.70–2.67 | 79.5 → 20.5° | |
| 4 | Decel | 2.67–3.37 | 20.5 → 10° | |
| 5 | Latch speed + kick | 3.37–4.27 | 10 → 0° | 10°/s, last 2° at 20°/s |
| 6 | Latch clack; bounce **0.3°**, ζ = 0.6 | 4.27–4.40 | | lamp amber 4.40 (Leaf_L 4.46) |

Closing KE is 1.4 J per leaf.

### 3.4 Obstruction / safety reverse
- **Detection:** stall force > **67 N at the leading edge**, plus the presence sensor on the swing (+Z) face.
- **Reaction:**
  - Stop within 0.10 s.
  - Reopen to 90° at ω ≤ 60°/s.
  - Hold 2.5 s, then retry.
- **Manual push:** opens at any time with **≤ 30 N** at the push bar (power assist).

### 3.5 Gaps and clearances (mm)
| Gap | As built | Required |
|---|---|---|
| Meeting-stile gap | **8** (±0.004) | 3–8 ✓ (no astragal; 8 is the upper limit) |
| Hinge edge to pivot / casing | 5 | 3–5 ✓ |
| Leaf to floor | **10** (Y 0.01) | 8–12 ✓ |
| Leaf top to casing head | 90 to the casing top (2.39 vs 2.48); head stop sits in this zone | 3 to the head stop |
| Leaf face to casing jamb stop | — | 2 (smoke seal compression 2) |
| Push-bar projection | 55 | ≤ 100 ✓ |

### 3.6 Visible hardware checklist
- [ ] 3 butt hinges per leaf, or top/bottom pivots (one or the other must be modelled; 4.5 in. heavy-duty knuckles at 0.25 / 1.20 / 2.15 m).
- [ ] Operator/closer arm per leaf on the pull (−Z) face, or a concealed head operator with a visible slide-track arm.
- [ ] Electrified push bar with a rim latch, or a top/bottom vertical rod latch.
- [ ] Floor stop or overhead stop at 90°.
- [ ] Smoke/brush seal on the meeting stiles and jambs.
- [ ] Kick plates (exist).
- [ ] Vision panel (exists).
- [ ] Amber lamp above each leaf (Sloane).
- [ ] **Manual override:** the push bar itself (always mechanically free egress).

### 3.7 Audio cues
| t (s) | Cue | Rel. level |
|---|---|---|
| 0.08 | push-bar / latch clack | −3 dB |
| 0.28 → 2.03 | assist motor hum | −16 dB |
| 2.03 | stop tap | −8 dB |
| Close 0.00 → 3.37 | closer hydraulic hiss (very faint) | −24 dB |
| Close 4.27 | latch clack (two, 60 ms apart) | 0 dB |

---

## 4. Heavy pressure bulkhead / hatch (service, plant, emergency zones)

### 4.1 Geometry and mass (wall bulkhead, primary)
| Item | Value |
|---|---|
| Clear opening | 0.90 W × 1.90 H m, R150 corners |
| Leaf | **1.10 W × 2.10 H × 0.12 T m** plug door, Al-Li 40 mm skin + ribs |
| **Mass** | **420 kg** (4.1 kN at 1.0 G, 6.0 kN at 1.45 G; carried on 2 hinges + a davit arm) |
| Leaf inertia about the hinge | about **174 kg·m²** (hinge axis 0.10 m outboard of the leaf edge) |
| Pressure rating | ΔP 101 kPa → about **205 kN** on the 2.0 m² seal area. The leaf opens **toward the high-pressure side** (plug), so pressure seats it. |
| Locking | **8 dogs** (2 per side), ganged by linkage to a central locking wheel, motor-driven with a manual handwheel |
| Seal | inflatable EPDM seal, 30 mm section, inflated at 200 kPa(g), **8 mm compression** |
| Swing | **100°**, hydraulic rotary actuator at the lower hinge + linear damper |
| Interlock | opens only when **ΔP ≤ 0.5 kPa** |
| Sill | accessible routes: 20 mm bevelled threshold, seal lands on it (Vance proposal). Plant-only: 150 mm coaming. |

### 4.2 Open sequence
| # | Phase | t0–t1 (s) | Motion | Notes |
|---|---|---|---|---|
| 1 | Request / auth (badge + 0.2 s hold) | 0.00–0.20 | — | |
| 2 | Lamp red → cyan; equalize valve opens | 0.20 | — | |
| 3 | Pressure equalize | 0.20–1.70 | gauge needle → 0 | **0.20–0.60** if already ΔP < 0.05 kPa |
| 4 | Dogs retract (locking wheel turns 90°) | 1.70–2.50 | 8 dogs, staggered 30 ms | |
| 5 | Seal deflate | 2.50–3.00 | seal visibly shrinks 8 mm | |
| 6 | Unseat / crack lurch (push-off rams break stiction) | 3.00–3.35 | 0 → 0.7° (12 mm at the edge) | |
| 7 | Accel | 3.35–4.68 | 0.7 → 20.7° | ω → **30°/s**, α = 30°/s², j = 90°/s³ |
| 8 | Cruise | 4.68–6.68 | 20.7 → 80° | |
| 9 | Decel | 6.68–8.01 | 80 → 100° | |
| 10 | Hold-open catch, settle | 8.01–8.40 | overshoot **0.3°**, f = 1.5 Hz, ζ = 0.7 | lamp green 8.40 |

**Total open: 8.40 s** (7.30 s pre-equalized). Peak KE is 24 J.

### 4.3 Close sequence
| # | Phase | t0–t1 (s) | Motion | Notes |
|---|---|---|---|---|
| 1 | Close command; lamp cyan chase + amber beacon; klaxon 2 × 0.3 s | 0.00–1.00 | — | |
| 2 | Hold-open catch release | 1.00 | — | |
| 3 | Accel | 1.00–2.33 | 100 → 86.7° | ω → **20°/s**, α = 20, j = 60 |
| 4 | Cruise | 2.33–5.90 | 86.7 → 15.3° | |
| 5 | Decel | 5.90–7.23 | 15.3 → 2° | |
| 6 | Final seat | 7.23–7.90 | 2 → 0° | ≤ 3°/s |
| 7 | Seal contact | 7.85 | | |
| 8 | Dogs drive | 7.95–8.75 | 8 dogs, staggered 30 ms | |
| 9 | Seal inflate | 8.80–9.40 | | |
| 10 | Leak check (gauge hold) | 9.40–10.40 | | |
| 11 | Lamp red (locked) or amber | 10.40 | | |

**Total close: 10.40 s.**

### 4.4 Obstruction / safety reverse
- **Normal mode:**
  - **Detection:** light curtain in the opening plus a leaf-edge tape switch.
  - **Reaction:** stop at α = 40°/s² (≤ 0.6 s), reopen to 30°, then retry after 5 s. Edge force limit **150 N**.
- **Pressure-emergency mode** (ΔP rising > 2 kPa, a breach). **Vance proposal, story beat:**
  - The close **does not reverse**.
  - The light curtain only slows the leaf to 5°/s, and a klaxon sounds continuously.
  - The manual handwheel can still stop the leaf.

### 4.5 Gaps and clearances (mm)
| Gap | Value |
|---|---|
| Leaf to frame (plug land, closed, seal deflated) | 6 all round |
| Seal compression (inflated) | 8 |
| Leaf to sill | 6 to the threshold, seal fills it |
| Dog engagement on the frame wedges | 25 throw, 3 lead-in |
| Hinge knuckle clearance | 2 |
| Open leaf to wall (hold-open catch) | 40 |

### 4.6 Floor/ceiling hatch variant
| Item | Value |
|---|---|
| Clear opening | 0.90 × 0.90 m |
| Leaf | 1.00 × 1.00 × 0.10 m, **140 kg** |
| Swing | **105°** |
| Weight moment closed | 140 × 9.81 × 0.5 = **687 N·m** at 1.0 G |
| Counterbalance (**Vance proposal, adopted 2026-11-20, realism owner's call; replaces the Rev 1.0 2 gas struts**) | **No gas struts.** A **585 N·m (85%) torsion bar**: a Ø25 bar inside a **Ø56 hinge tube** that runs the hinge edge (tube x −0.490…+0.450; bar x −0.575…+0.467). It sits outboard of the liner in an open hinge channel behind the leaf (z −0.575…−0.506, channel floor 72 mm down, \|x\| ≤ 0.600). There is an **exposed anchor clevis at each end**: the fixed frame anchor at −X and the leaf anchor on the +X tube end cap. The **tube top is 4 mm below the floor**, the **hinge axis is 32 mm below the floor**, and nothing protrudes above the floor. Torque at 1 G: weight moment **687 N·m**, bar **585 N·m**, net **≈ 102 N·m closing** at the closed position, actuator **≤ 530 N·m**. A human can open it with ≤ 200 N on the handle, and gravity still holds it shut at 1.0 G. Phase timing is unchanged. |
| Damper | **Rotary hydraulic damper on the hinge axis, outboard** (x 0.535…0.590), capped at **77.8°/s open / 33.3°/s close** at game tempo (35°/s real open). |
| Stay | Stay arm (5 × 20 mm flat bar, 0.40 m between pins), slider and **105° detent** on the **+X side wall** (band x 0.4515…0.4805, outside the column). It folds into a **12.5 mm liner recess** (x 0.449…0.4625); the slot and plunger pocket are **32 mm** deep (to x 0.482, inside the 40 mm limit). The detent plunger pops up behind the slider at 105° (2.5 mm gap) and has an **OverrideOrange detent pull knob** visible in the recess. |
| Clear-column rule | Column = \|x\|, \|z\| < 0.450 from the well floor to floor + 2 m. **No frame-fixed, counterbalance, stay or damper part may enter it at any angle (0–105°), and no part at all may enter it at 105°.** The leaf and its leaf-borne lock gear may sweep the column during travel (the leaf crosses it 0–94.5°). The lock gear (wheel, 4 dogs, 4 linkages, handle, OverrideOrange handwheel and lever) must clear the liner, flange and keepers by **≥ 3 mm (target)**, and the **dogs must fully retract before lift-off** (dogs end 1.50 s, lurch starts 1.80 s at game tempo). As built (Rook 2db8f7b / 83c56e3, PASSC_NOTES): fixed hardware ≥ 2.0 mm outside the column (keeper), moving stay ≥ 1.5 mm, leaf gear at 105° 17.5 mm, lock-gear minimum **9.62 mm** (Dog_01/02 at 3.0° against the liner). |
| Leaf-to-rebate gap | **6.0 mm** on the W, E and S sides (rebate wall ±0.506, leaf edge ±0.500; Rook 54d2e05). The N (hinge) side is the open hinge channel and has no rebate wall. The leaf sits flush with the flange (0.0 mm). |
| Why also damper + powered lock | the Drum RPM range is 0.08–1.45 G. At 0.08 G the weight moment is 55 N·m and the torsion bar (585 N·m) would throw the leaf open, so a **rotary hydraulic damper caps the speed at 35°/s** (77.8°/s at game tempo) and the actuator drives it closed against the bar (≤ 530 N·m). At 1.45 G the weight moment is 996 N·m, and the actuator adds about 411 N·m to open. |
| Open timing | phases 1–6 as §4.2, then the S-curve 0.7 → 105° with ω 35°/s, α 35, j 105 (**4.28 s**) |
| Total open | **7.63 s** (3.35 + 4.28) |
| Hold-open | mechanical stay arm whose slider drops into the 105° detent (clunk); OverrideOrange knob pulls the plunger to release. No strut lock sleeve. |

### 4.7 Visible hardware checklist
- [ ] 2 heavy hinges plus a davit arm.
- [ ] Hydraulic rotary actuator housing at the lower hinge.
- [ ] Linear damper.
- [ ] **8 dogs** with linkage bars to the **central locking wheel** (wheel turns 90° in phase 4).
- [ ] Frame wedges / dog keepers.
- [ ] Inflatable seal (visible bead) in the frame groove.
- [ ] Push-off rams (2, near the latch edge).
- [ ] **Pressure indicator both sides:** analog ΔP gauge (0–110 kPa, green band ≤ 0.5) plus a digital readout.
- [ ] Equalize valve with a visible port/grille.
- [ ] Hold-open catch.
- [ ] Hub lamp ring (Sloane) + amber beacon.
- [ ] **Manual override:** handwheel (OverrideOrange) driving the dogs at **12 turns** full throw, plus a manual equalize lever.
- [ ] Hatch only (Vance proposal, adopted 2026-11-20): torsion bar in the Ø56 hinge tube with an exposed anchor clevis at each end, rotary damper outboard on the hinge axis, stay arm + slider + 105° detent with an OverrideOrange knob in the +X liner recess. **No gas struts.**

### 4.8 Audio cues
| t (s) | Cue | Rel. level |
|---|---|---|
| 0.20 → 1.65 | equalize hiss (falls with ΔP) | −3 dB |
| 1.70 → 2.45 | dog motor whine | −10 dB |
| 2.30 → 2.51 | dog clunks ×8, 30 ms apart | −4 dB each |
| 2.50 → 2.95 | seal deflate hiss | −8 dB |
| 3.05 | unseat **thunk** | **0 dB** |
| 3.35 → 8.01 | actuator hydraulic hum + hinge groan (low) | −14 dB |
| 8.05 | hold-open catch clunk | −5 dB |
| Close 0.00 / 0.50 | klaxon | −2 dB |
| Close 7.85 | seat thud | −1 dB |
| Close 7.95 → 8.75 | dog whine | −10 dB |
| Close 8.55 → 8.76 | dog clunks | −4 dB |
| Close 8.80 → 9.40 | inflate hiss | −10 dB |

---

## 5. Acceptance checks Vance will use when reviewing renders and headless logs
| # | Check | Pass criterion | Source |
|---|---|---|---|
| R1 | Phase order | every phase in §n.2/§n.3 occurs in order; nothing skipped (latch/seal/lurch present) | CSV `phase` column |
| R2 | Timing | each phase t0/t1 and the total open/close within **±10%** | CSV |
| R3 | Velocity profile | no velocity step > 5% of v_peak in one tick (jerk-limited); peaks within ±10% | CSV `leaf_vel` |
| R4 | Settle | overshoot amplitude ±25% of spec, and decays (no sustained oscillation, no bounce on doors specced without one) | CSV |
| R5 | Stagger | per-leaf start offsets within ±20 ms | CSV |
| R6 | Hardware visible | every checklist item in §n.6 / §4.7 is visible in at least one camera (A/B/C/E), or legitimately covered with an access panel shown | renders |
| R7 | No clipping | no leaf intersects the frame, pocket, mullion, floor or another leaf at any sampled frame (run `3d-part-clipping-check`) | renders + collision log |
| R8 | Gaps | modelled gaps within **±2 mm** of §n.5 (swing angles ±0.5°) | GLB bounds + render C/E |
| R9 | Collider follows leaf | collider transform equals the leaf transform every tick; collider disabled only inside the collider-off window | CSV `collider_enabled` |
| R10 | Obstruction | a test capsule in the opening during close triggers stop + reverse per §n.4, with no pass-through and no player shove into the frame | headless test |
| R11 | Audio sync | every cue fires within **±1 physics tick** of its timestamp | cue log |
| R12 | Lamp sync | cyan at the first mechanical event and green at settle (±0.05 s) | CSV |
| R13 | G invariance | bulkhead and hatch timings unchanged at 0.08 / 1.0 / 1.45 G (±5%) | headless run ×3 |
| R14 | As-built fidelity | bay3 and pair_18 use the GLB leaf nodes and pivots unchanged (outswing bay3, +Z pair) | scene |

Floor hatch (Vance proposal, adopted 2026-11-20): **R6** looks for the torsion-bar hardware in the §4.7 hatch line, **not gas struts**. **R7** includes the §4.6 clear-column rule. **R8** checks the 6.0 mm W/E/S leaf-to-rebate gap.

## 6. Conflicts with AESTHETIC_SPEC (for Gage / Jared to settle)
- **Durations:**

  | Door | Sloane | This spec | What Sloane's figure would need |
  |---|---|---|---|
  | Slider | 0.9 s open | 2.00 s total, 1.55 s of leaf motion | a 1.0 m leaf in 0.9 s needs about 1.8 m/s and 7 m/s², beyond real door operators |
  | Pair | 0.8 s to 90° | 1.83 s of motion | |
  | Bulkhead | 1.8 s leaf swing | 4.66 s for a 420 kg leaf | |

  ~~If the tempo must be faster, Vance proposal: scale **only the S-curve phases** by up to 0.7× and keep the latch, seal, dog and equalize phases real, because those carry the "real machine" read.~~ **Superseded by §7 (Jared, 2026-11-20: snappier, game-like; leaf travel 0.45×, latch/seal/dog 0.6×).**
- **Bay3:** Sloane specs a telescoping slider, but the built asset is an outswing swing door. This spec covers the as-built door, with the slider in §2.8 as the alternative.
- **Settle:** Sloane says "no bounce" for the sliders. This spec allows a 2 mm overshoot on a bumper (ζ 0.6, a single visible decay), which is within her ≤ 3 mm settle.

Label: Vance proposal on all design calls above that are not taken from the as-built GLBs or marked *real-world ref*.

---

## §7 Rev 1.1 — Game-tempo profile (Jared, 2026-11-20)

**Decision (Jared, 2026-11-20 1:50 PM CT, relayed by Gage):** doors are **snappier and more game-like**. This replaces the §6 0.7× proposal. The Rev 1.0 tables (§1–§4) stay as the *real-drive reference*; **this section is the shipped profile** that Grok implements and that R1–R14 check.

### 7.0 Scalars and rules
- **Scalars.** No door_lab `.tres` exists on main or in the box checkout yet (searched `godot/` for `door_lab` and `*.tres` tempo/scale/compress scalars on 2026-11-20; only the two GLBs exist). So this section uses Gage's stated values. **If the `DoorProfile` `.tres` files land with different scalars, they win, and every number here rescales by the same rules.**

  | Scalar | Value | Applies to |
  |---|---|---|
  | `k_leaf` | **0.45** | leaf-travel phases: accel, cruise, decel, creep, back-check, latch-check, final seat |
  | `k_mech` | **0.60** | latch / bolt / strike, seal unseat / deflate / inflate, dogs, pressure equalize, plus control phases (request/auth, pre-warn, klaxon, leak check) and the small gaps between them (Vance proposal for the control phases) |
  | lurch | **1.0 (real)** | crack-open lurch: same duration, displacement and peak speed as Rev 1.0 |
  | settle | **1.0 (real)** | hard stop / settle / latch bounce: same A, f, ζ and duration as Rev 1.0 |
  | stagger | **1.0 (real)** | per-leaf start offsets (bay3 0/+60/+120 ms, pair +60 ms) stay as they are, because they're a visual read and R5 checks them at ±20 ms (Vance proposal) |
  | dog stagger | × `k_mech` | 30 ms → **18 ms** between dogs |
- **Kinematics scale consistently with time.** Distances and angles are unchanged. For any compressed phase with factor k: **v' = v/k, a' = a/k², j' = j/k³**. At k = 0.45 that is ×2.222 / ×4.938 / ×10.97, and at k = 0.6 it is ×1.667 / ×2.778 / ×4.630. The §0.1 S-curve formulas regenerate every row.
- **Closing-safety rule (Vance proposal).** The **≤ 10 J closing-KE limit (EN 16005-style, *real-world ref*)**, the force limits (150 N slider/bulkhead, 67 N swing) and every §n.4 safety reverse **still apply at game tempo**. For each **close** move:
  1. Use `k_leaf` = 0.45 if closing KE ≤ 10 J.
  2. Otherwise use **0.6×** on close leaf travel if that brings it to ≤ 10 J.
  3. Otherwise **cap v_peak (ω_peak) at the 10 J speed**, keeping the game-tempo a and j (the 0.45 values) so the move still starts and stops crisply. The cruise just gets longer.
- **Safety reactions are not compressed:** the detection thresholds, the reopen speed caps, the hold and retry timers, and the 3-strike fault all keep their §n.4 values. The only change is the **stop** decel, which must still meet the §n.4 stop time and distance from the new close speeds: slider 4.94 m/s² (0.13 s / 41 mm from 0.64 m/s), bay3 ≥ 333°/s², pair ≥ 667°/s², and bulkhead/hatch use the existing 40°/s² (≤ 0.6 s).
- **Hardware, gaps and masses: unchanged** (§n.1, §n.5, §n.6, §4.7). The faster drive is a story-level upgrade (higher-torque operators) and gets no new visible parts (Vance proposal).
- **Coriolis** at the new peak speeds: the slider leaf at 2.89 m/s gets 1.28 m/s². That still isn't visible at door scale, so §0.3 stands and nothing gets animated.

### 7.1 Pocket slider (bi-parting), game tempo
**Open: 1.08 s** (real 2.00). v_peak **2.89 m/s**, a **14.8 m/s²**, j **219 m/s³**. Peak opening KE is 200 J per leaf (see 7.7).

| # | Phase | k | t0–t1 (s) | Motion / kinematics |
|---|---|---|---|---|
| 1 | Request / auth | 0.6 | 0.00–0.06 | — |
| 2 | Lamp amber → cyan | — | 0.06 | 0.15 s fade |
| 3 | Bolt retract | 0.6 | 0.06–0.13 | — |
| 4 | Seal unseat | 0.6 | 0.13–0.18 | 0 → 3 mm |
| 5 | Crack-open lurch | real | 0.18–0.28 | 3 → 15 mm, peak 0.18 m/s |
| 6 | Accel | 0.45 | 0.28–0.54 | 15 → 394 mm; v → 2.89, a 14.8, j 219 |
| 7 | Cruise | 0.45 | 0.54–0.62 | 394 → 565 mm at 2.89 m/s |
| 8 | Decel | 0.45 | 0.62–0.88 | 565 → 944 mm |
| 9 | Creep to stop | 0.45 | 0.88–0.93 | 944 → 1000 mm, ≤ 1.11 m/s at the start |
| 10 | Bumper settle | real | 0.93–1.08 | 2 mm, f 6 Hz, ζ 0.6; **lamp green 1.08** |

**Close: 2.40 s** (real 3.75). **Safety cap applies:** at 0.45×, v = 1.33 m/s gives **42.7 J per leaf ✗**, and 0.6× (v 1.00) gives **24 J ✗**. The 10 J speed for a 48 kg leaf is 0.645 m/s, so close cruise is **capped at 0.64 m/s (9.8 J ✓)**, with a 4.94 m/s² and j 54.9 m/s³.

| # | Phase | k | t0–t1 (s) | Motion |
|---|---|---|---|---|
| 1 | Hold expires; lamp cyan; chime | — | 0.00 | — |
| 2 | Pre-warn | 0.6 | 0.00–0.24 | — |
| 3 | Accel | cap | 0.24–0.46 | 1000 → 930 mm; v → 0.64 |
| 4 | Cruise | cap | 0.46–1.69 | 930 → 140 mm at 0.64 m/s |
| 5 | Decel | cap | 1.69–1.91 | 140 → 70 mm |
| 6 | Latch-check creep | 0.45 | 1.91–2.25 | 70 → 0 mm, ≤ 0.22 m/s (1.2 J) |
| 7 | Seal contact | — | 2.23–2.25 | soft thud |
| 8 | Bolt throw | 0.6 | 2.28–2.34 | — |
| 9 | Lamp → amber / red | — | 2.40 | — |

Audio (replaces §1.7 timestamps; levels unchanged):

| Open t (s) | Cue | Close t (s) | Cue |
|---|---|---|---|
| 0.06 | solenoid clack | 0.00 | chime |
| 0.17 | seal pop | 0.24 → 2.25 | whine (pitch follows v) + rumble |
| 0.18 → 0.93 | motor whine (peak 0.54–0.62) | 2.24 | seal thud |
| 0.28 → 0.91 | roller rumble | 2.31 | bolt clack |
| 0.93 | bumper thud | | |

Collider-off window: unchanged rule, now phase 6 of the close (1.91–2.25).

### 7.2 Bay3 (as-built outswing swing, per leaf; stagger 0 / +60 / +120 ms unchanged)
**Open: 1.54 s per leaf, last leaf 1.66 s** (real 2.95 / 3.07). ω_peak **177.8°/s**, α **988°/s²**, j **10,974°/s³**. Opening KE is 98 J per leaf (see 7.7).

| # | Phase | k | t0–t1 (s) | Angle |
|---|---|---|---|---|
| 1 | Request / auth | 0.6 | 0.00–0.06 | — |
| 2 | Lamp cyan; strike release | 0.6 | 0.06–0.13 | — |
| 3 | Weatherseal unseat + lurch | real | 0.13–0.23 | 0 → 2°, peak 30°/s |
| 4 | Accel | 0.45 | 0.23–0.50 | 2 → 26° |
| 5 | Cruise | 0.45 | 0.50–0.68 | 26 → 58° at 177.8°/s |
| 6 | Decel | 0.45 | 0.68–0.95 | 58 → 82° |
| 7 | Back-check creep | 0.45 | 0.95–1.31 | 82 → 90°, ≤ 26.7°/s |
| 8 | Hold-open stop settle | real | 1.31–1.54 | 0.8°, f 3 Hz, ζ 0.5; green when the last leaf settles (1.66) |

**Close: 2.85 s per leaf, last leaf 2.97 s** (real 4.75 / 4.87). **Safety rule step 2:** 0.45× (66.7°/s) gives **13.8 J per leaf ✗**, so close leaf travel runs at **0.6×**: ω **50°/s** (I = 20.4 kg·m² → **7.8 J ✓**), α 166.7°/s², j 1,389°/s³.

| # | Phase | k | t0–t1 (s) | Angle |
|---|---|---|---|---|
| 1 | Hold expires; lamp cyan | — | 0.00 | — |
| 2 | Pre-warn | 0.6 | 0.00–0.18 | 90° |
| 3 | Accel | 0.6 | 0.18–0.60 | 90 → 79.5° |
| 4 | Cruise | 0.6 | 0.60–1.78 | 79.5 → 20.5° at 50°/s |
| 5 | Decel | 0.6 | 1.78–2.20 | 20.5 → 10° |
| 6 | Latch check | 0.6 | 2.20–2.80 | 10 → 0°, ≤ 16.7°/s, last 2° at 25°/s (1.9 J) |
| 7 | Strike catch | — | 2.80 | — |
| 8 | Lamp amber | — | 2.85 (last leaf 2.97) | — |

Audio: strike clack 0.07; gear whine 0.21 → 1.31 (3 staggered voices); stop tap 1.31. Close: whine 0.18 → 2.80; latch clack ×3 at 2.80 (+60 ms stagger).

### 7.3 Pair_18 (stagger: Leaf_L leads open, Leaf_R leads close, +60 ms, unchanged)
**Open: 1.21 s, Leaf_R 1.27 s** (real 2.25 / 2.31). ω_peak **244.4°/s**, α **1,481°/s²**, j **16,461°/s³**. Opening KE is 92 J per leaf (see 7.7).

| # | Phase | k | t0–t1 (s) | Angle |
|---|---|---|---|---|
| 1 | Request | 0.6 | 0.00–0.05 | — |
| 2 | Lamp cyan; rim latch retract | 0.6 | 0.05–0.12 | — |
| 3 | Smoke-seal unseat + lurch | real | 0.12–0.20 | 0 → 1.5° |
| 4 | Accel | 0.45 | 0.20–0.46 | 1.5 → 32.7° |
| 5 | Cruise | 0.45 | 0.46–0.55 | 32.7 → 55.3° at 244.4°/s |
| 6 | Decel | 0.45 | 0.55–0.81 | 55.3 → 86.5° |
| 7 | Back-check | 0.45 | 0.81–0.99 | 86.5 → 90°, ≤ 26.7°/s |
| 8 | Stop / settle | real | 0.99–1.21 | 1.0°, f 3 Hz, ζ 0.45; green after Leaf_R settles (1.27) |

**Close: 2.05 s, Leaf_L 2.11 s** (real 4.40 / 4.46). **0.45× passes:** ω **66.7°/s** (I = 10.1 kg·m² → **6.8 J ✓**), α 296.3°/s², j 3,292°/s³.

| # | Phase | k | t0–t1 (s) | Angle |
|---|---|---|---|---|
| 1 | Hold expires; lamp cyan | — | 0.00 | — |
| 2 | Accel (closer sweep) | 0.45 | 0.00–0.32 | 90 → 79.5° |
| 3 | Sweep | 0.45 | 0.32–1.20 | 79.5 → 20.5° at 66.7°/s |
| 4 | Decel | 0.45 | 1.20–1.52 | 20.5 → 10° |
| 5 | Latch speed + kick | 0.45 | 1.52–1.92 | 10 → 0°, 22.2°/s, last 2° at 44.4°/s (3.0 J) |
| 6 | Latch clack; bounce 0.3°, ζ 0.6 | real | 1.92–2.05 | lamp amber 2.05 (Leaf_L 2.11) |

Audio: latch clack 0.05; assist hum 0.20 → 0.99; stop tap 0.99. Close: closer hiss 0.00 → 1.52; latch clacks at 1.92 (two, 60 ms apart).

### 7.4 Pressure bulkhead (wall), game tempo
**Open: 4.64 s, or 3.98 s pre-equalized** (real 8.40 / 7.30). ω_peak **66.7°/s**, α **148.1°/s²**, j **988°/s³**. Opening KE is 118 J (see 7.7).

| # | Phase | k | t0–t1 (s) | Motion |
|---|---|---|---|---|
| 1 | Request / auth (badge hold) | 0.6 | 0.00–0.12 | — |
| 2 | Lamp red → cyan; equalize valve | — | 0.12 | — |
| 3 | Pressure equalize | 0.6 | 0.12–1.02 | 0.12–0.36 if already ΔP < 0.05 kPa |
| 4 | Dogs retract (wheel 90°) | 0.6 | 1.02–1.50 | 8 dogs, 18 ms stagger |
| 5 | Seal deflate | 0.6 | 1.50–1.80 | 8 mm |
| 6 | Unseat lurch | real | 1.80–2.15 | 0 → 0.7° |
| 7 | Accel | 0.45 | 2.15–2.75 | 0.7 → 20.7° |
| 8 | Cruise | 0.45 | 2.75–3.65 | 20.7 → 80° at 66.7°/s |
| 9 | Decel | 0.45 | 3.65–4.25 | 80 → 100° |
| 10 | Hold-open catch settle | real | 4.25–4.64 | 0.3°, f 1.5 Hz, ζ 0.7; **lamp green 4.64** |

**Close: 7.80 s** (real 10.40). **Safety rule step 3:** 0.45× (44.4°/s) gives **52 J ✗** and 0.6× (33.3°/s) gives **29 J ✗**. The 10 J speed for I = 174 kg·m² is 19.4°/s, so close cruise is **capped at 19.4°/s (9.97 J ✓)**, with α 98.8°/s² and j 658°/s³. **Correction to Rev 1.0:** §4.3's 20°/s close was **10.6 J**, slightly over the limit, and this cap fixes it. Pressure-emergency mode (§4.4) is unchanged: no reverse, and the curtain slows the leaf to 5°/s.

| # | Phase | k | t0–t1 (s) | Motion |
|---|---|---|---|---|
| 1 | Close command; cyan chase + beacon; klaxon 2 × 0.3 s | 0.6 | 0.00–0.60 | — |
| 2 | Hold-open catch release | — | 0.60 | — |
| 3 | Accel | cap | 0.60–0.95 | 100 → 96.6° |
| 4 | Cruise | cap | 0.95–5.65 | 96.6 → 5.4° at 19.4°/s |
| 5 | Decel | cap | 5.65–6.00 | 5.4 → 2° |
| 6 | Final seat | 0.45 | 6.00–6.30 | 2 → 0°, ≤ 6.7°/s |
| 7 | Seal contact | — | 6.28 | — |
| 8 | Dogs drive | 0.6 | 6.33–6.81 | 8 dogs, 18 ms stagger |
| 9 | Seal inflate | 0.6 | 6.84–7.20 | — |
| 10 | Leak check | 0.6 | 7.20–7.80 | — |
| 11 | Lamp red / amber | — | 7.80 | — |

Audio: equalize hiss 0.12 → 0.99; dog whine 1.02 → 1.47; dog clunks 1.38 → 1.51 (×8, 18 ms); deflate hiss 1.50 → 1.77; **unseat thunk 1.85**; hydraulic hum + groan 2.15 → 4.25; catch clunk 4.29. Close: klaxon 0.00 / 0.30; seat thud 6.28; dog whine 6.33 → 6.81; dog clunks 6.69 → 6.82; inflate hiss 6.84 → 7.20.

**For Jared (if a snappier close is wanted):** taking the bulkhead close at 0.6× would make it 5.6 s with 29 J. The protection would then rest only on the light curtain, the 150 N edge limit and the klaxon. That is a departure from the 10 J rule, so it isn't adopted here.

### 7.5 Floor / ceiling hatch (§4.6), game tempo
**Correction to Rev 1.0:** the §4.6 S-curve (0.7 → 105°, ω 35, α 35, j 105) is 1.333 + 1.647 + 1.333 = **4.31 s**, not 4.28 s, so the real total open is **7.66 s**, not 7.63 s. Rev 1.0 gave no hatch close, so the real close below is derived from §4.3 with a 105° swing (ω 20, α 20, j 60, travel 6.48 s, **total 10.65 s**, 2.8 J). I = 140 × 1.0²/3 = 46.7 kg·m².

**Open: 4.09 s, or 3.43 s pre-equalized** (real 7.66 / 6.56). ω_peak **77.8°/s**, α **172.8°/s²**, j **1,152°/s³**. In-game, the rotary damper's speed cap scales with it, from 35 to **77.8°/s**. Opening KE is 43 J.

| # | Phase | k | t0–t1 (s) | Motion |
|---|---|---|---|---|
| 1–5 | Request, equalize, dogs, deflate | as 7.4 | 0.00–1.80 | as 7.4 rows 1–5 |
| 6 | Unseat lurch | real | 1.80–2.15 | 0 → 0.7° |
| 7 | Accel | 0.45 | 2.15–2.75 | 0.7 → 24.0° |
| 8 | Cruise | 0.45 | 2.75–3.49 | 24.0 → 81.7° at 77.8°/s |
| 9 | Decel → stay arm drops into detent | 0.45 | 3.49–4.09 | 81.7 → 105°; **detent clunk + lamp green 4.09** |

**Close: 6.39 s** (real 10.65). **Safety rule step 2:** 0.45× (44.4°/s) gives **14.0 J ✗**, so close travel runs at **0.6×**: ω **33.3°/s (7.9 J ✓)**, α 55.6°/s², j 278°/s³. Against the torsion bar (585 N·m; net ≈ 102 N·m closing at 1 G) the actuator still has to deliver ≤ 530 N·m (§4.6, Vance proposal adopted 2026-11-20; no gas struts). That doesn't change, and neither does the phase timing.

| # | Phase | k | t0–t1 (s) | Motion |
|---|---|---|---|---|
| 1 | Klaxon / beacon | 0.6 | 0.00–0.60 | — |
| 2 | Stay-arm detent release | — | 0.60 | release clunk |
| 3 | Accel | 0.6 | 0.60–1.40 | 105 → 91.7° |
| 4 | Cruise | 0.6 | 1.40–3.69 | 91.7 → 15.3° at 33.3°/s |
| 5 | Decel | 0.6 | 3.69–4.49 | 15.3 → 2° |
| 6 | Final seat | 0.6 | 4.49–4.89 | 2 → 0°, ≤ 5°/s; seal contact 4.86 |
| 7 | Dogs drive | 0.6 | 4.92–5.40 | 18 ms stagger |
| 8 | Seal inflate | 0.6 | 5.43–5.79 | — |
| 9 | Leak check → lamp | 0.6 | 5.79–6.39 | lamp red / amber 6.39 |

Audio: front cues as 7.4 to the thunk (1.85); hydraulic hum 2.15 → 4.09; detent clunk 4.09. Close: klaxon 0.00 / 0.30; release clunk 0.60; seat thud 4.86; dog whine 4.92 → 5.40; inflate hiss 5.43 → 5.79.

### 7.6 Totals summary (game tempo vs Rev 1.0 real)
| Door | Open (s) | Close (s) | Close v/ω peak | Close KE | Close rule |
|---|---|---|---|---|---|
| Pocket slider | **1.08** (2.00) | **2.40** (3.75) | 0.64 m/s | 9.8 J ✓ | 10 J cap (0.45× = 42.7 J, 0.6× = 24 J) |
| Bay3 (per leaf / last leaf) | **1.54 / 1.66** (2.95 / 3.07) | **2.85 / 2.97** (4.75 / 4.87) | 50°/s | 7.8 J ✓ | 0.6× (0.45× = 13.8 J) |
| Pair_18 (lead / trail leaf) | **1.21 / 1.27** (2.25 / 2.31) | **2.05 / 2.11** (4.40 / 4.46) | 66.7°/s | 6.8 J ✓ | 0.45× |
| Bulkhead (pre-equalized) | **4.64 (3.98)** (8.40 / 7.30) | **7.80** (10.40) | 19.4°/s | 9.97 J ✓ | 10 J cap (0.45× = 52 J, 0.6× = 29 J) |
| Floor hatch (pre-equalized) | **4.09 (3.43)** (7.66 / 6.56) | **6.39** (10.65) | 33.3°/s | 7.9 J ✓ | 0.6× (0.45× = 14.0 J) |

### 7.7 Safety flags
1. **Closing KE:** a straight 0.45× close breaks 10 J on the slider (42.7 J), bay3 (13.8 J), bulkhead (52 J) and hatch (14.0 J). The 7.0 rule fixes all of them. **The slider and bulkhead fail even at 0.6×**, so they need the speed cap.
2. **Opening KE rises about 4.9×:** slider 200 J/leaf, bay3 98 J, pair 92 J, bulkhead 118 J, hatch 43 J. The swing doors open **toward people** (bay3 outswing into the approach path, pair into the hall +Z), so the swing-side presence sensors (§2.4, §3.4) **must stall and hold the opening leaf** whenever the player capsule is in its sweep arc. Gage: in game, an opening swing leaf must never push the capsule (stall instead), and the collider still follows the leaf (R9).
3. **The §0.2 sprint note changes:** at game tempo, `t_open_to_clear` is shorter (slider clear gap ≥ 0.80 m at about 0.55 s, end of accel), so recompute the proximity radius from the game-tempo CSV.
4. **QUALITY_BAR (Patch) §F timing rows** still quote the Rev 1.0 totals. Patch needs to repoint them at §7.6, which is Patch's file, not mine.

### 7.8 Acceptance checks R1–R14 restated for game tempo
| # | Check | Pass criterion (game tempo) | Source |
|---|---|---|---|
| R1 | Phase order | every phase in §7.1–§7.5 occurs in order; nothing skipped (latch/seal/dog, **lurch and settle present at real duration**) | CSV `phase` |
| R2 | Timing | each phase t0/t1 and each **game-tempo total in §7.6** within **±10%**; lurch and settle durations within ±10% of Rev 1.0 | CSV |
| R3 | Velocity profile | jerk-limited: per-tick Δv ≤ 1.1 × a′ × dt and per-tick Δa ≤ 1.1 × j′ × dt (a′, j′ from §7). At 60 Hz this allows about 9–10% of v_peak per tick on the slider, bay3 and pair, which replaces the Rev 1.0 "5% of v_peak", unreachable at 60 Hz with these accels. Peaks (open v/ω and the capped close v/ω) within ±10% | CSV `leaf_vel` |
| R4 | Settle | unchanged: overshoot ±25% of the Rev 1.0 values, decays, no sustained oscillation | CSV |
| R5 | Stagger | unchanged: ±20 ms of 0/+60/+120 (bay3) and +60 ms (pair) | CSV |
| R6 | Hardware visible | **unchanged** (§n.6 / §4.7) | renders |
| R7 | No clipping | unchanged; sample every physics tick (the faster leaves move up to 48 mm per tick at 60 Hz) | renders + collision log |
| R8 | Gaps | **unchanged**: ±2 mm of §n.5, swing angles ±0.5° | GLB + renders |
| R9 | Collider follows leaf | unchanged; collider-off window is now the game-tempo latch/creep phase (slider 1.91–2.25 close) | CSV |
| R10 | Obstruction | unchanged reaction (§n.4) from the game-tempo close speeds; stop within the §n.4 time/distance using the 7.0 stop decels; **opening swing leaves stall on the capsule (7.7 #2)** | headless test |
| R11 | Audio sync | every cue fires within ±1 physics tick of its **§7 timestamp** | cue log |
| R12 | Lamp sync | cyan at the first mechanical event, green/amber at the §7 settle/lamp time (±0.05 s) | CSV |
| R13 | G invariance | unchanged: §7 timings identical at 0.08 / 1.0 / 1.45 G (±5%) | headless ×3 |
| R14 | As-built fidelity | unchanged | scene |
| R15 *(new)* | Closing KE | ½ m v² (or ½ I ω²) per leaf **≤ 10 J** at every close tick, computed from the CSV | CSV |

Label: §7 tables are derived from Jared's 2026-11-20 tempo decision via Gage's scalars. The 10 J close rule, the uncompressed safety reactions, the control-phase scaling, the real-time stagger and the hatch close are **Vance proposals**.

---

## §8 Pass A review (Vance, 2026-11-20, against ac35bfd/c13382c)
Reviewed: `/workspace/door_lab_shots/A/` renders + motion PNGs, `qa/door_lab/run60/{summary,meta}.json`. Pass A ran at the old 0.7× travel scale, so it is checked for hardware, sequence and shape only. §7 timing/R3/R15 are checked in pass B.
- **No numbers to check:** the per-tick CSVs and cue logs are not on main, and the motion PNGs have no time or value axes, so R2/R3/R5/R9/R11/R12/R15 can't be verified from the artifacts yet.
- **R15 at 0.7×:** slider close ≈ 17.6 J ✗ (m ≈ 47.9 kg/leaf, v ≈ 0.86 m/s). Bay3 5.7 J, pair 2.8 J and hatch 5.7 J pass. Pass B must apply the 0.64 m/s slider cap.
- **Lab coverage:** the "hatch" is the wall plug bulkhead (vertical). There is no horizontal floor-hatch case (§4.6: 105°, ~~2 gas struts~~ torsion bar per the 2026-11-20 amendment, stay-arm detent, damper), and R13 (0.08/1.0/1.45 G) is not reported. F-OBS-EMERGENCY (§4.4) isn't implemented.
- **Hardware (R6):** the bulkhead shows a box plus one bar where §4.7 calls for 8 dogs with linkage to a central wheel, plus gauges, an equalize port, push-off rams, a seal bead and a handwheel. The back face of the open leaf is a featureless black slab. The detail/jamb cameras are underexposed, so the hinge, seal and strike can't be judged.
- **Lamps (R6/R7):** the bay3 and bulkhead cyan lamp lines stay fixed in space while the leaves move. They sit mid-leaf, not on the jambs or mullions.
- **meta.json** records commit f2ccf57 (Patch count 78), not the pass A commit.
- **Looks right:** phase order and shape (lurch knee, back-check/latch-check knees on the swing doors, slider close creep), the bi-parting mirror, the bay3 3-leaf stagger, outswing bay3 and +Z pair (R14), kick plates, push bars, finger guards, the 8 mm sweeps, and fails=0 at 60/20/15 fps.

---

## §9 Pass C review (Vance, 2026-11-20, against 4694ea7). Verdict: **FAIL**
I recomputed everything from `qa/door_lab/runC{,_20fps,_15fps}/*/motion.csv` and `cue_log.csv`. I did not use the self-report.
- **PASS: R2.** All §7.6 totals are within ±10%: pocket 1.08/2.40; bay3 1.55/2.85 (last leaf 1.67/2.97); pair 1.27/2.05 (+4.7% open; trailing leaf 1.32/2.10); bulkhead 4.62/7.78; floor hatch 4.08/6.38. The bulkhead and floor-hatch phase t0/t1 values match §7.4/§7.5 to within one tick.
- **PASS: R15.** Max close KE over every tick: pocket 9.81 J (v 0.640 m/s), bay3 7.77 J (50.0°/s), pair 6.84 J (66.7°/s), bulkhead 9.97 J (19.4°/s), floor hatch 7.90 J (33.3°/s). The values are identical at 60/20/15 Hz.
- **PASS: R5.** Bay3 open is 0/+67/+133 ms and close (L2/L0/L1) is 0/+67/+133 ms. Pair is +50 ms each way.
- **PASS: peaks.** Open peaks: pocket 2.89 m/s, bay3 177.8°/s, pair 244.4°/s, bulkhead 66.7°/s, floor hatch 77.8°/s.
- **Minor: R3, raw per-tick values (60 Hz only).** The harness averages 3 ticks; §7.8 does not.
  - Pocket open: seal_unseat jerk 1.60× and creep jerk 1.52× the 1.1·j′·dt limit.
  - Pair close latch_check: Δv 1.16×.
  - Bulkhead final_seat: Δv 1.12×, Δa 1.33×.
  - Floor hatch final_seat: Δv 1.25×, Δa 1.35× (also present at 20/15 Hz).
  - **Vance proposal:** accept a 3-tick average only on phase-entry ticks, and smooth the final_seat entry anyway.
- **FAIL: R11.**
  - The bulkhead close has 1 dog clunk; §7.4 calls for ×8 at 6.69→6.82 s on an 18 ms stagger. The floor hatch close also has 1 (it should have ×8 at the end of the 4.92–5.40 dog drive).
  - The floor hatch close has no release clunk at 0.60 s.
  - The bay3 latch_clack_l1 fires at 2.85 s, but Leaf_1 strike_catch is at 2.917 s (§7.2: 2.80/2.86/2.92).
  - Pair stop_tap is at 1.067 s against 0.99 s in §7.3. The pair open back-check runs 0.867–1.033 against 0.81–0.99, about 50 ms late.
  - The bay3 strike clack for l2 is at 0.167 s against 0.19 s, and stop_tap is at 1.333 s against 1.31 s.
- **Not verifiable: R13 / F-STALL-OPEN / F-OBS-EMERGENCY.** `metrics.json` is not committed.
  - `_gravity()` changes only `_player.gravity_scale` and samples once at 55% of open. The kinematic door cannot change, so R13 passes by construction and the test is vacuous.
  - The stall hold is checked for only 8 ticks.
  - The emergency test sets `door.emergency` directly instead of a ΔP > 2 kPa rise, and checks klaxon-fired rather than a continuous klaxon.
- **FAIL: meta.json.** `commit` is a80cc47 (the pass B merge); the code changes are in 4694ea7. The `profiles` list omits floorhatch, and the settlement text still says "Four doors".
- **FAIL: R6, bulkhead (§4.7)**, from the heroes only.
  - Visible: about 8 dog blocks on the face with no linkage bars and no central locking wheel. The orange disc is flat, with no rim or spokes.
  - Visible and good: the gauge, readout and keypad on the jamb (one face only).
  - Not visible: seal bead or groove, keepers, push-off rams, hinges, davit, actuator, damper, equalize port or lever, and the far-face gauge.
  - The edge is still a slab. The R150 corners are good.
  - There is no open or back-face render.
- **FAIL: R6, floor hatch (§4.6).**
  - The closed leaf sits about 100 mm proud of the floor on loose frame strips.
  - Not shown: ~~the 2 gas struts~~ the counterbalance (now the torsion bar and anchor clevises, §4.6 amendment 2026-11-20), stay arm with detent, rotary damper, seal, dogs, handle or frame flange.
- **Partial: pocket (§1.6).** Visible: radar head, jamb sensors (3 of 4), leaf pulls and floor guide. Not visible: carriages, anti-lift rollers, belt clamp, end bumpers, solenoid bolt and keeper, and the hex-key plate. There is no access slot or panel.
- **Fixed: exposure and lamps.** Exposure is good in the heroes, but no detail or jamb cameras were rendered in pass C. The lamp strips now sit on the jambs and mullions, and the floating mid-leaf lines are gone. Pair glazing now reads as a tinted lite with a pattern.

---

## §10 Pass E review (Vance, 2026-11-21, against 6f39e8b / merge da136c5). Verdict: **FAIL** (narrowed)
I recomputed from `qa/door_lab/runE{,_20fps,_15fps}/*/{motion,cue_log,metrics}` and viewed the renders: the box heroes in `/workspace/door_lab_shots/E` plus the Windows mirror `aegis_shots/doorlab_E/<door>/shots`. The floor hatch GLB is deferred to pass F (Rook rev 2). The N2 pair retime is **blocked** by Patch M-114 (Jared's call) and is not failed here.

**PASS:**
- **R3 (raw tick).** No interior violations at any rate. All excursions are on accel or settled phase-entry ticks only (worst jerk 3.9× on bay3 Leaf_1 accel entry at 60 Hz). This is consistent with the logged entry exceptions.
- **R5.** Bay3 is 0/+67/+133 ms on open and on close; pair is +50 ms.
- **R15.** Pocket 9.81 J at 0.640 m/s; bay3 7.77 J at 50.0°/s; pair 6.84 J at 66.7°/s; bulkhead 9.97 J at 19.4°/s; floor hatch 7.90 J at 33.3°/s. Same at 60/20/15 Hz.
- **R13, floor hatch.** The torque model is real (passive torque 585 − 687·g·cosθ, actuator ±530 N·m, damper 77.8/33.3°/s); worst 0.00216 against 0.05. Advisory: commit the 0.08 G and 1.45 G CSVs, since the shipped CSVs are g = 1.0 only.
- **R13, bulkhead.** Accepted by construction: the hinge axis is vertical, so gravity produces no torque about it.
- **F-STALL-OPEN.** Real PlayerBody, displacement 0.000 m, stop 0.000°/s within 6 ticks, held 2.02 s with no resume (bay3 and pair).
- **F-OBS-EMERGENCY.** Triggered by `delta_p = 3.0` kPa (no forced flag), 5.0°/s, no reverse, klaxon every 1.0 s (`_klaxon_age`).
- **N1 cue fixes.** The bulkhead and floor hatch each have 8 close clunks, the floor hatch release clunk is at 0.60, bay3 is 2.80/2.867/2.933, and pair stop_tap is at 1.00.
- **1a2668c is in pass E.** The bulkhead GLB is the 1a2668c version, and meta base cfc8e95 descends from it. It shows 8 dogs with linkage bars to a spoked central wheel, keepers, a plug liner with R150 corners, and on the jamb a gauge, readout, equalize lever and port grille.

**FAIL:**
- **Bulkhead and floor-hatch final seat stretched (R2/R4, Jared's 7.80 s).** Decel now runs to zero at 2°, then a separate final_seat move follows:
  - Bulkhead: 0.483 s, peak 8.46°/s, against §7.4's 0.30 s at ≤ 6.7°/s. Close total is 7.98 s against 7.80 s.
  - Floor hatch: 0.633 s, peak 6.34°/s, against §7.5's 0.40 s at ≤ 5°/s. Close total is 6.63 s against 6.39 s.
  - Every downstream cue is late against §7: bulkhead dog whine 6.517 (target 6.33), inflate 7.033 (target 6.84); floor hatch dog whine 5.167 (target 4.92), inflate 5.683 (target 5.43).
  - seat_thud (6.283 and 4.867) now fires about 0.2 s **before** the leaf actually seats.
  - R2 and R11 in metrics compare against the shipped profile, not §7.6/§7 timestamps, so they can't catch this.
- **Pocket cues against §7.1.** roller_rumble_start 0.317 (target 0.28); bolt_clack 2.35 (target 2.31, after bolt_throw ends at 2.333). Minor phase drift: decel 0.65–0.783 (target 0.62–0.88), creep 0.80–0.90 (target 0.88–0.93).
- **Self-report.** metrics.json logs **V-GAP-PAIR and R8 FAIL on pair at all 3 rates** (measured 0.0001 mm against 2 mm, so the gate logic looks wrong), and V-GAP-HATCH 114 mm on the floor hatch, which is deferred to pass F. That contradicts "fails=0".
- **Meta stamp.** `dirty: true`, but `tree` 9c0b6a3 is cfc8e95's own tree, not the working tree that actually ran.
- **Renders.**
  - `back_closed` and `back_open` for the bulkhead are flat grey (the camera is inside geometry), so the far-face gauge and readout, ribs, hinges, davit, actuator, damper and rams can't be verified.
  - A hard-edged white quad behind the openings blows out pocket detail_open and threshold_open and the bulkhead detail_open and threshold_open.
  - The pocket pearl leaves clip to white in jamb_closed.
  - The bulkhead readout renders blank white.
- **Pocket §1.6, partly visible.** Seen: exposed track end with carriage at the head, 4 lenses per jamb, hex-key plate, pulls, floor guide. Not seen: anti-lift roller, belt clamp, end bumpers, solenoid bolt and keeper. Re-check once the cameras are fixed.

---

## §11 Amendment: floor-hatch counterbalance (Vance proposal, adopted 2026-11-20, realism owner's call; recorded 2026-11-21 per Patch M-118)
§0.3, §4.6, §4.7, §5, §7.5, §8 and §9 now specify the **torsion bar instead of 2 gas struts**, with the damper, stay, clear-column rule and 6.0 mm gap above. §10 had no strut targets. Numbers are cross-checked against `assets/src/door_lab/PASSC_NOTES.md` (Rook 2db8f7b / 83c56e3 / 54d2e05). Where the brief and the notes differ, the notes win:
- **"Full-length" tube:** the tube runs x −0.490…+0.450 (0.94 m), not the full 1.00 m leaf edge. The bar runs x −0.575…+0.467 into the anchor hubs.
- **Rebate gap:** 6.0 mm applies to the W, E and S sides only. The N hinge side has no rebate wall.
- **Column clearances as built:** keeper 2.0 mm and stay arm 1.5 mm, both outside the column. Lock gear 9.62 mm minimum, which meets the ≥ 3 mm target.
- **Open item (not strut-related):** the floor hatch has **4 dogs** (`hatch_Dog_01..04`), but §7.5 rows 1–5 and 7 say "as 7.4" (8 dogs, 18 ms stagger), and the runE floor-hatch cue log plays 8 clunks. This needs reconciling in pass F: 4 clunks on an 18 ms stagger, or the GLB gets 8 dogs.
- **Decision (Vance proposal, adopted 2026-11-21, realism owner's call): the floor hatch keeps 4 dogs** (`hatch_Dog_01..04` with `hatch_Linkage_01..04`, as built in Rook 2db8f7b). §7.5 rows 1–5 and 7 now read **"as 7.4, except 4 dogs"**, and the dog cues are **4 clunks, 18 ms apart, end-aligned to each dog phase**:
  - Open: `dog_clunk_1..4` at **1.456 / 1.474 / 1.492 / 1.510 s**.
  - Close: `dog_clunk_close_1..4` at **5.346 / 5.364 / 5.382 / 5.400 s**.
  - Dog whine, phase windows, timing and totals are unchanged (open 4.09 s, close 6.39 s).
  - R11 tolerance is ±16.7 ms on each clunk. The wall bulkhead keeps 8 dogs and 8 clunks.

---

## §12 Pass F review (Vance, 2026-11-21, against 41ce6cf / merge 1381acf). Verdict: **CONDITIONAL PASS**. Functional is all PASS; 4 visual/audio items remain for pass G.
I recomputed from `qa/door_lab/runF{,_20fps,_15fps}/*/{motion,cue_log,metrics}.csv/json` and `runF/floorhatch/motion_g008.csv` / `motion_g145.csv`. I viewed `/workspace/door_lab_shots/F` and the Windows mirror `aegis_shots/doorlab_F/<door>/shots` (back, detail, jamb, threshold, top). The N2 pair retime is still **blocked** by Patch M-114 (Jared's call) and is not scored against.

**Pass E fixes confirmed:**
- **Moving 2° handoff.**
  - Bulkhead: decel ends at 6.70°/s, then a constant 6.70°/s final seat for 0.300 s (5.98–6.28 rel). Close **7.783 s** against 7.80; Jared's 7.80 s holds.
  - Floor hatch: decel ends at 5.00°/s, then a constant 5.00°/s final seat for 0.400 s (4.48–4.88). Close **6.383 s** against 6.39.
  - The same at 20/15 Hz (bulkhead seat 0.333 s at 15 Hz, which is tick quantization).
- **R2/R11 now reference §7.6/§7** ("spec 7.800+0.000", "section7 … tol 0.0167"), not the shipped profile.
- **Cues against §7, all within ±16.7 ms:**
  - Bulkhead: seat 6.283, dog whine 6.333, clunks 6.700–6.833, inflate 6.850, hold-open 4.300.
  - Floor hatch: seat 4.867, whine 4.933, inflate 5.433, release 0.600, detent 4.100.
  - Pocket: rumble 0.283, bolt 2.317.
  - Bay3 2.800/2.867/2.933; pair stop_tap 1.000.
- **Pocket phase table.** Decel 0.617–0.850 (+1 tick = 0.867), creep 0.867–0.917 (+1 tick = 0.933), against 0.62–0.88 / 0.88–0.93. Open 1.08 s.
- **Gaps / V-GAP-PAIR gate.** Pair meet 5.00 (3–8), hinge 4.81 (3–5), floor 10.00 (8–12). Bulkhead 6.00 mm deflated. Floor hatch W/E/S 6.00 mm (N excluded per §11). No R8 fails at any rate.
- **R13.** Real 0.08 G and 1.45 G CSVs. My worst phase-bound deviation is **2.05%** (1.45 G open decel ends 4.150 against 4.067 s; actuator saturation stretch) against 0.05, so PASS. Gage's 0.00216 normalizes differently.
- **R15.** 9.81 / 7.77 / 6.84 / 9.97 / 7.90 J at all rates.
- **R5.** Unchanged and passing.
- **Stall and emergency.** F-STALL-OPEN held 2.02 s. F-OBS-EMERGENCY 5.0°/s, no reverse.
- **Torsion-bar hatch.** Unchanged (M-118 closed). The clear column holds per Rook 83c56e3.
- **Renders.**
  - The bulkhead back camera is now outside the geometry and shows the ribbed back face, the back gauge with a "100" readout, and 2 heavy hinges.
  - The white backdrop blowout is gone.

**Accepted (Vance proposal, adopted 2026-11-21):** the final-seat → seal-contact stop (6.7 → 0°/s bulkhead, 5 → 0°/s floor hatch in one tick: raw Δv 4.1× and 5.4×) counts as a contact event, like lurch and settle, and is excluded from R3. Contact KE is 1.19 J and 0.36 J. Remaining raw-tick R3 interior excursions are minor: pocket seal_unseat jerk 1.60×; pair latch_check Δv 1.16× (N2-blocked).

**Open for pass G:**
1. **R11, floor hatch dogs (Gage lab, data only).** It still plays 8 clunks on open (1.383–1.517) and close (5.283–5.400). Target: 4 clunks per the §11 decision (open 1.456/1.474/1.492/1.510; close 5.346/5.364/5.382/5.400). This is a `floorhatch.json` cue-table edit. Deferring was defensible only while §11 left it as an open item; it is decided now and must land in G.
2. **R6, framing (Gage lab).**
   - The pocket head internals exist in the GLB (`slide_carriage_*`, `slide_roller_*_antilift`, `slide_BeltClamp_*`, `slide_Bumper`, `slide_Solenoid`/`SolenoidBolt`, `slide_AccessPanel`) but aren't in frame. detail_open looks at the closed head soffit from +Z. Target: shoot from the −Z approach side with `slide_AccessPanel` posed +90° open, and add a pocket-end shot for the bumper.
   - **Node names updated for pass G (`b530847`, 2026-11-21).** Use these names in any framing or lookup code:
     - `slide_carriage_{L,R}{1,2}` (no change).
     - `slide_AntiLiftRoller_{L,R}{1,2}` replaces `slide_roller_*_antilift`. It is now a Ø40 acetal tyre.
     - `slide_BeltClamp_{L,R}` (no change).
     - `slide_Bumper_{L,R}` replaces `slide_Bumper`. These are the pocket backstops at x ±2.050–2.079.
     - **New:** `slide_EndStop_{L,R}`, the track end stops at x ±1.934–1.994. §13.1 moves them to ±1.930–1.990.
     - `slide_Solenoid`, `slide_SolenoidBolt` (it now throws −Y), and the **new** `slide_Solenoid_mount`.
     - `slide_Keeper` is now the polished tab with its post.
     - `slide_AccessPanel` and `slide_AccessPanel_hinge` (no change).
   - **Framing targets restated for pass G.**
     - detail_open covers only x ±1.1. At full open the clamps sit at x ±1.52 and the end stops at x ±1.93, so they fall outside it.
     - The clamps, anti-lift rollers, solenoid and keeper need a **closed-pose head shot** from −Z with `slide_AccessPanel` at +90°. Look it up by exact name; `slide_AccessPanel_hinge` must not match.
     - The end stops and bumpers need a **pocket-end shot at each end at full open** (q = 1.000, plus one frame at the 2 mm overshoot). That shot shows the carriage on the stop (§13.1) and the bumper 23–25 mm behind the leaf tail.
     - Rook's `rook_ttqa/doorlab_passC/gage_doorlab_incr_G.patch` (antilift r 0.020, exact panel lookup at +90°) is the starting point. Gage owns it.
     - Pass G shots 1–8 in `/workspace/renders/doorlab_passG/` already show the parts. Shot 1 (gage_open_detail) still shows mostly soffit, so this item stays open until the head shot and end shots become standard lab cameras.
   - Bulkhead back_closed/back_open crop the davit (top) and miss the actuator housing (under the lower hinge), `bulkhead_Damper_body`/`DamperRod`, and `bulkhead_PushOffRam_1/2` (latch-edge bores, +12 mm at unseat). Target: frame the full leaf plus 0.3 m margin, and add a latch-edge close-up at t = 1.9 s (rams extended).
3. **R6, front readout blank (Gage lab).** The front digital readout renders as a plain grey panel, while the back shows "100". Target: the front readout matches the back, showing ΔP in kPa.
4. **Exposure (Gage lab).** The pocket lower leaf panels still clip to white in the hero and jamb shots. Target: leaf-face mean luma ≤ 0.25 V-LUMA with no clipped region larger than 5% of the leaf.
- **Advisory.** meta `tree` 932f8ec is not an object on origin, so it can't be checked; it does differ from base a1a426c's tree (37ae0a6), so the bug is fixed. Also record `godot_tree` (the run's `godot/` subtree hash) so it can be compared with the commit's `HEAD:godot`. The bulkhead handwheel renders yellow-gold; confirm the OverrideOrange swatch with Sloane.

**Scores (0–10):** R1 10 · R2 10 · R3 9 · R4 10 · R5 10 · R6 7 · R7 10 · R8 10 · R9 10 · R10 10 · R11 8 · R12 10 · R13 10 · R14 10 · R15 10. **Overall 9.6 / 10** (pass E ≈ 8.0).


## §13 Pass G pocket-slider hardware ruling (Vance, 2026-11-21, against Rook `b530847`)
I checked the v1–v5 GLB node bounds with trimesh, plus `hw_gaps_passG` in `passC_qa.json` and PASSC_NOTES. I viewed the 24 renders in `/workspace/renders/doorlab_passG/` (before / after_panel90 / after_panel-110, shots 1–8). Every call in this section is a **Vance proposal**. Jared approves.

**Confirmed as built:**
- **Anti-lift roller:** Ø40×24 acetal tyre (measured 40×40×24). Clearances: 2 mm to the rail/track, 6.8 mm to the Ø60 rollers, 2 mm under the upper rail.
- **Belt clamps:** 100 mm jaw, 2 mm to the belt over the full travel.
- **Solenoid:** can 60×38×28, mount 72×39×5, bolt Ø12×30.
- **Keeper:** tab 52×8×30 with an 18×18 hole, top at y 2.500.
- **Clearances (all variants):** solenoid to carriages/clamps (closed) 23.46; keeper to solenoid 22.0; bolt to keeper window (thrown) 3.0 radial.
- **Tris:** 5968 / 5968 / 5728 / 5968 / 5968.
- **Renders:**
  - The end stops, anti-lift rollers, solenoid (red), keeper tab and clamps all read in shots 3–8.
  - Belt clamps render cream/near-white, not yellow zinc (see §13.3).
  - Carriage plates blow out to white. That is the §12 item 4 exposure issue, still open.

### 13.1 End stops: keep both parts, and make the track stop take contact
- **They aren't redundant.** `slide_EndStop_{L,R}` (60×46×27 rubber block on the track, in line with the outer carriage) is the **primary mechanical stop**. On a real bi-parting operator, the carriage stops on a track-mounted rubber stop, not on the leaf tail.
  - `slide_Bumper_{L,R}` (2 × 25×80×30 buffers in the pocket) is the **secondary backstop**. It catches a leaf pushed by hand past the operator stop or a carriage that has come off the stop. Keep both.
- **The 4.0 mm gap is wrong for this profile.**
  - §7.1 has a 2 mm bumper-settle overshoot (6 Hz, ζ 0.6) and a `bumper_thud` cue at 0.93 s, so both say the leaf hits rubber.
  - With 4.0 mm at q = 1.000 and 2.0 mm at the overshoot, nothing touches: the thud plays against air, and the settle has no cause.
- **Ruling:** move the track stops **4.0 mm inboard to x ±1.930–1.990** (y 2.466–2.512 and z −0.044…−0.017 stay the same; Rook GLB).
  - The outer carriage (L1 outer face at x −0.930 closed, so −1.930 at full open) then **meets the stop at q = 1.000** (gap 0.0 mm).
  - The 2 mm overshoot compresses the rubber by **2.0 mm, which is 3.3% of the 60 mm block**. That is a realistic rubber-stop deflection and drives the 6 Hz settle.
  - The contact face is 46 (y) × 19 (z) mm of carriage-to-stop overlap ✓.
- **Pocket bumper stays where it is.** It sits 25 mm off the leaf tail at full open, and **23 mm at the overshoot**. It must never touch in the normal cycle. Add a QA gap `leaf_tail_to_pocket_bumper ≥ 20 mm` at max overshoot.
- **QA (Gage lab):** `carriage_to_endstop` reads 0.0 mm at q = 1.000 and −2.0 mm (compression) at the overshoot peak. The 3d-part-clipping-check must allow this one pair up to 2.0 mm, because it is a designed rubber compression.

### 13.2 Bolt: vertical (−Y) throw approved, with a spring throw and deeper engagement
- **Vertical vs Z.** A vertical down-throw from the head into a keeper on the leaf is the usual head-lock form on bi-parting operators (*real-world ref*). It shears against the leaf's opening direction (X), which is the forcing direction, and doesn't depend on the leaf's Z play. A Z throw would rely on the 2 mm anti-lift/guide play to hold the keeper. **The −Y 18 mm throw is approved** and replaces the old +Z.
- **Throw drive.** Spin gravity runs 0.08–1.45 G, so the bolt must be **spring-thrown and solenoid-retracted (fail-secure)**, never gravity-dropped. This is a description and audio point only: the `solenoid_clack` at 2.31 s is the spring snap. No extra geometry.
- **Engagement fails as built.**
  - Retracted, the bolt sits 14.32 mm above the tab top.
  - An 18 mm throw puts the tip at y 2.496, only **≈ 4 mm into an 8 mm tab** (≈ 3.7 mm from the measured gap). That's less than half the tab, and a 2 mm anti-lift lift would almost unseat it.
- **Ruling (Rook GLB):** lower the whole solenoid group (`slide_Solenoid`, `slide_Solenoid_mount`, `slide_SolenoidBolt`) **6.3 mm (−0.0063 Y)**, and keep the 18 mm throw so the §7.1 bolt timing (2.28–2.34 s, clack 2.31) holds. Results:
  - Retracted tip to tab top: **8.0 mm**. That is ≥ 4× the 2 mm vertical leaf play, so the bolt clears the keeper as the leaf moves. *(Amended §14.B1: the governing number is **7.7 mm vertical**, tip to tab-top plane, with 8.26 mm on the surface metric. 18 = 7.7 + 10.3. Minimum 6 mm, which is 3× the play.)*
  - Thrown engagement: **10.3 mm**, all the way through the 8 mm tab and 2.3 mm below it.
  - Radial window: 3.0 mm, acceptable. (Advisory: 1–2 mm is more typical; leave it unless it's cheap.)
  - Re-measure and report: `bolt_thrown_to_track ≥ 3 mm` (was 16.64; it should drop to about 10) and **`bolt_thrown_tip_to_keeper_post ≥ 3 mm`**. The tip now goes below the tab, so the post/riser under the hole must clear it.
- **Advisory (Rook GLB):** `slide_Solenoid_mount` (z −0.022…−0.017) overlaps `slide_Track` (z min −0.019) by 2 mm. Seat it flush (z −0.024…−0.019) unless the track profile is open there. *(Amended §14.B2: a 1.0–2.0 mm bed is accepted instead of flush; as built it is 1.5 mm.)*

### 13.3 Materials: recommendation only (Sloane's call)
AESTHETIC_SPEC §1 says to reuse existing slots unless one is missing. Pass G added 5 DL_ slots. My realism view:
- **DL_BumperRubber → fold into DL_SealRubber.** Both fall in the AESTHETIC gasket row (0.06–0.09, rough 0.80–0.90). 0.06 vs 0.07–0.08 can't be told apart at head distance.
- **DL_PolishedSteel → fold into TT_BrushedAlloy / Mat_Hub_BrushedSteel** (the hardware row: 0.75–0.82, metal 0.9–1.0, rough 0.30–0.40).
  - Its 0.86 albedo is above the row's 0.82 cap.
  - Brushed stainless is just as real for a keeper and bolt.
  - If Sloane wants a polish read, use the AESTHETIC §2 wear rule (ORM roughness −0.15, about 0.18–0.25) on the same slot rather than adding a new one.
- **DL_YellowZincPlate:** no existing slot. It currently renders cream/white (pass G shots 4–7), so the hue is lost.
  - Either Gage exempts it from the lab retint lift, or it **folds into TT_BrushedAlloy as clear zinc**, which is equally real.
  - No realism objection either way.
- **DL_AcetalWhite:** keep. Natural acetal is warm off-white, and the bluish Pearl/WhiteComposite slots would read as painted metal. It's a minor item, and a fold into TT_WhiteComposite is acceptable if Sloane prefers.
- **DL_SolenoidRed:** keep. There is no red paint slot. It is non-emissive and darker than the Locked lamp #FF2A2A, and it doesn't touch OverrideOrange, which stays reserved for the manual release. A black can (TT_Gunmetal) is equally real if Sloane wants fewer accents.

### 13.4 Status
- §1.6 is amended (end-stop and bolt lines).
- §12 item 2 has the node-name and framing update.
- **Open for Rook (GLB):** 13.1 end-stop move; 13.2 solenoid group −6.3 mm plus the two new gap reports; the mount flush advisory.
- **Open for Gage (lab):** 13.1 QA gaps and clip allowance; §12 item 2 head and end shots with the new names.
- **Sloane:** 13.3 recommendations.

## §14 Pass G review (Vance, 2026-11-21, against Gage afbbc47 / merge 7319f96) and Rook §13 / Rev 3.10.1 deviation rulings
Verdict: **CONDITIONAL PASS.**
- Every realism row passes on the unmodified GLBs.
- The harness's 7 FAIL rows (hatch and floor hatch F-CLIP-HW / F-CLIP-ALLOW / R7, and floor hatch F-CLIP-LEAF) come from the lab, not the models (§14.2).
- Four §12 items are still partial (§14.3). Every call here is a **Vance proposal**. Jared approves.

**Inputs.**
- `qa/door_lab/runG/{PASS_G_REPORT.md, meta.json, summary.json}` at afbbc47.
- The 60 Hz run tree from the Windows mirror `aegis_shots\doorlab_G`: `*/motion.csv`, `cue_log.csv`, `metrics.json`, `floorhatch/motion_g008.csv` / `motion_g145.csv`, and the shots.
- `/workspace/door_lab_shots/G/`.
- GLB measurements with exact point-to-triangle containment: surface samples plus vertices, inside test by 3-axis ray parity. Run on both the b530847 GLBs that pass G ran on and the current main GLBs (c675aca M-122 bake, d855824, 49d6505).

### 14.1 Base, and what pass G actually tested
- **Stale base.** Pass G ran on **b530847 plus a dirty tree**. That is before Rook's M-122 bake (c675aca), the pair meet fix (80570f1), §13 (d855824) and Rev 3.10.1 (49d6505).
  - The lab still applied its runtime M-122 edits (pair x-scale 0.9973, hatch dogs ×0.683 / linkages ×0.538, floor dogs ×0.418 / linkages ×0.489).
  - Those edits are adaptive, so on the baked GLBs they should fall to factor 1. Pass H must still run on current main with Rook's `incr_G` + `incr_M122` + `incr_threshold` patches applied, so the lab tests the GLB as shipped (R14).
- **Accepted:** deferring the §13.1 end-stop QA and the tower re-probe to pass H. Both depend on commits that came after the pass G base.

### 14.2 Clip rows: lab issues, not model issues
| Door | Pair (Gage) | Gage depth | My exact depth, both GLB versions | Owner and fix |
|---|---|---|---|---|
| hatch | `bulkhead_HingeHeavy_frame` vs frame_skin | 86 mm | **4.0 mm** (bedded into `bulkhead_frame_collar` and `bulkhead_Actuator_housing`) | Gage lab: depth metric |
| hatch | `bulkhead_damper_mount` vs frame_skin | 76 mm | **4.0 mm** (collar) | Gage lab: depth metric |
| hatch | `bulkhead_HingeHeavy_leaf` vs leaf_skin | 69.7 mm | **4.0 mm** (`bulkhead_leaf_shell`) | Gage lab: depth metric |
| hatch | `bulkhead_leaf_damper_mount` vs leaf_skin | 59.7 mm | **4.0 mm** (leaf shell, Davit_arm) | Gage lab: depth metric |
| floor | `hatch_HingeBearing_frame` vs frame_skin | 70 mm | **4.0 mm** (`hatch_frame`) | Gage lab: depth metric |
| floor | `hatch_RotaryDamper` vs frame_skin | 35.8 mm | **4.0 mm** (`hatch_frame`) | Gage lab: depth metric |
| floor | leaf_skin vs frame_skin | 11.5 / 11.3 / 15.2 mm (q 0 / 26.25 / 105) | **0.0 mm** at 0 / 26.25 / 52.5 / 78.75 / 105° (pivot (0, 0.430, −0.524), axis X). Every leaf part was tested against every frame part. | Gage lab: overlays and pose |

- **Hardware rows.** All six are the same deliberate **4.0 mm mounting bed**, a bolted bracket seated in the frame or leaf face. That is under the 3d-part-clipping-check hardware cap (0.030 m) and under the 0.010 m default.
  - The depth doesn't change with pose, and it isn't a physical depth. The poke-or-slab metric measures through the plate's extent, not the distance back out of the host.
- **Fix 1 (Gage lab).** Replace poke-or-slab with exact containment, the same method as Rook's passC `hw_gaps` / `lock_gear_gaps`:
  - depth(A in B) = max over A's vertices plus ≥ 3000 surface samples that test inside B (3-axis ray parity, majority) of the exact point-to-triangle distance to B's surface.
  - Keep leaf_skin and frame_skin as unions for the gate, but log the **source mesh name** of the deepest point.
  - Expected: all six hardware pairs at 4.0 mm, PASS with no allowlist row needed.
- **Fix 2 (Gage lab, floor leaf vs frame).** The unmodified GLB is clean, so the 11.5–15.2 mm comes from the rig. Two definite lab bugs:
  - `_dress_floor_lid`: `handle.scale *= 2.0` scales `hatch_Handle` about its node origin, which is the leaf pivot. That throws the handle to GLB z 1.308…1.340, about 0.8 m off the leaf (in front of the frame, 12 mm above the deck plane). **Remove it.** If Sloane wants a larger handle, Rook models it.
  - `CornerLampNE` / `CornerLampSW` are 40×32×40 boxes standing **32 mm proud** of a walk-on lid. That's a trip edge and not real. Make them **flush lenses: 40 × 6 × 40, top at the lid top** (leaf-body y 0.026…0.032), or move them to the frame.
  - Re-run, and if leaf vs frame is still > 0.5 mm, report the two mesh names and the world point.
- **Rook GLB: no clip fix required** on the hatch or floor hatch. Advisory only: `bulkhead_HingeHeavy_frame` and `bulkhead_Actuator_housing` overlap each other by 4.0 mm (y). That's acceptable as a bolted interface. Separate them by 1 mm only if a gate flags hardware vs hardware.

### 14.3 §12 items G1–G7
| # | Item | Result | Evidence and pass H target |
|---|---|---|---|
| G1 | Floor-hatch 4 clunks from the door JSON | **PASS** | See detail below. |
| G2 | Pocket framing with the new node names | **PARTIAL** | See detail below. |
| G3 | Bulkhead back framing | **PARTIAL** | See detail below. |
| G4 | Front readout ΔP kPa | **PARTIAL** | See detail below. |
| G5 | Pocket exposure | **PASS** | V-LUMA 0.2041 ≤ 0.25 (leaf mean 0.137); V-CLIP 0.00% on hero_final / jamb_closed / head_closed / pocket_end_open. |
| G6 | Meta stamp `godot_tree` | **PARTIAL** | See detail below. |
| G7 | Handwheel vs OverrideOrange | **OPEN (Sloane)** | See detail below. |

- **G1, floor-hatch clunks.**
  - `floorhatch.json` `section7.cues` has 1.456 / 1.474 / 1.492 / 1.510 and 5.346 / 5.364 / 5.382 / 5.400. The bulkhead keeps 8.
  - `cue_log.csv` (60 Hz): open 1.467 / 1.483 / 1.500 / 1.517, close 5.350 / 5.367 / 5.383 / 5.400. Worst error is 11 ms, under one tick.
- **G2, pocket framing.**
  - `head_closed` shows the head from −Z: carriages, anti-lift rollers, clamps, red solenoid and the end stops at the ends. These are small but readable, so that part passes.
  - `pocket_end_open` shows only the leaf face and green strip. The end stop, carriage and bumper are out of frame, and there's no overshoot frame.
  - Shots used the pre-d855824 GLB.
  - **Target:** aim `pocket_end_open` at (±1.96, 2.49, 0) from −Z, about 0.6 m off, panel +90° (v1). Show the carriage on the stop at q = 1.000 and at the overshoot peak, with the bumper top visible.
- **G3, bulkhead back framing.**
  - `back_open` shows the plug, handwheel, both readouts and the damper/davit bar at the top. It cuts off the hinge edge, so `bulkhead_Actuator_housing` (x 0.585…0.745, y 0.17…0.30) and `bulkhead_Davit_bracket` aren't in frame.
  - `latch_edge_19` shows a dog-rod tip. The rams were nudged −12 mm for the shot only.
  - **Target:** frame the full leaf plus 0.3 m including the hinge edge. **Animate `bulkhead_PushOffRam_1/2` in the rig, not per shot:** +Z 0 → 12 mm over 1.80–2.10 s (tracking the lurch), hold to 2.15, retract to 0 by 2.45, open only. Move the latch-edge shot to **t = 2.12 s**.
- **G4, front readout.**
  - Both faces now read "100" and match. But the value is static: `back_open` also reads 100 with the leaf open. That contradicts the §4 interlock (opens only at ΔP ≤ 0.5 kPa).
  - **Target:** both readouts and the needle show live ΔP in kPa. Start at the lab ΔP (100) at the request, ramp to **0.0 by the end of equalize (1.02 s)**, hold 0.0 while open and through the close. Add a "ΔP kPa" legend. Open shots must read 0.0.
- **G6, meta stamp.**
  - `head_godot` 731a9e8 = `b530847:godot` ✓.
  - `godot_tree` 88ce84e isn't an object on origin and doesn't match the committed `afbbc47:godot` (58d7a50), so the run tree can't be tied to the commit. The likely cause is a write-tree that included untracked files.
  - **Target:** run from a clean checkout and stamp `commit`, `dirty: false`, and `godot_tree` == `git rev-parse <commit>:godot`. The harness fails the run if they differ.
- **G7, handwheel vs OverrideOrange.**
  - The wheel is now **unshaded Color8 (217, 115, 5)**, which is the amber *accent* target. It is not `Mat_Hub_OverrideOrange` (0.851, 0.357, 0.149, metal 0.1, rough 0.45).
  - Realism view: manual-release hardware should be lit (real paint) and keep the override colour distinct from status amber.
  - **Recommendation to Sloane:** use `Mat_Hub_OverrideOrange` lit, and give the wheel its own V-AMBER reference.

### 14.4 R1–R15 recompute (60 Hz run tree)
- **Timing (R2).**
  - Pocket: open 1.083, close 2.417 (prewarn 4.117 → settled 6.517); spec 1.08 / 2.40.
  - Bulkhead close: **7.800 s** (close request 7.633 → settled 15.433). Final seat 6.000–6.283 relative, dogs 6.333–6.800, clunks 6.700–6.833.
  - Floor-hatch close: 6.400 (spec 6.39, one tick).
  - Gage's 20 / 15 Hz tables were not re-derived; those CSVs weren't in the mirror.
- **R11:** floor clunks as in G1. Pocket bumper_thud 0.933, bolt_clack 2.317.
- **R13:** floor hatch at 1.45 G, open decel ends 4.150 against 4.067, a 2.0% stretch. 0.08 G and 1.45 G close are both 6.384 s. PASS.
- **R15 (from motion, close only):** 9.81 / 7.77 / 6.84 / 9.97 / 7.90 J.
- **R3:** the harness reports PASS (worst raw ratio about 0.91). I did not independently re-derive it this pass, so it stays at 9.
- **R7:** model clean (§14.2), harness FAIL is the lab (scored 8).
- **R14:** the lab still edits the GLB at runtime, and the run used the pre-bake GLBs (scored 9).

**Scores (0–10):** R1 10 · R2 10 · R3 9 · R4 10 · R5 10 · R6 8 · R7 8 · R8 10 · R9 10 · R10 10 · R11 10 · R12 10 · R13 10 · R14 9 · R15 10. **Overall 9.6 / 10** (pass F 9.6). R11 is up from 8 to 10. R6 is up from 7 to 8. R7 drops to 8 and R14 to 9, both lab-side.

### 14.5 Rook deviations on d855824 (§13) and 49d6505 (Rev 3.10.1). Verified in the GLBs
**Verified on all five pocket variants (v1 and v3 measured in full):**
- `slide_EndStop_{L,R}` at x ±1.930–1.990, y 2.466–2.512, z −0.044…−0.017. The carriage L1 outer face at full open is −1.930, so contact is 0.0 mm.
- Solenoid group lowered 6.3 mm: can y 2.5157–2.5537, bolt 2.5077–2.5377. The thrown tip is at 2.4897, giving **10.3 mm engagement**, 2.3 mm through the tab.
- Exact distances: bolt retracted to keeper 8.26; thrown bolt to track 11.84; thrown bolt to keeper window 3.0.
- Mount bed into the track: 1.5 mm.

**Tower bay (49d6505, `tt_entrance_bay_3l`):**
- The ray probe at x −1.1 / 0 / +1.1 gives visual = collider exactly: 0 (z −1.720) → 6 (−1.708) → 12 (−1.696…−0.966) → 8 (−0.958) → 4 (−0.950 onward). Max step is 4 mm.
- `Leaf_{0,1,2}_Sweep` is at y 0.020–0.062 and z −1.076…−1.064, leaf width minus 5 mm each end, so it sits **8.0 mm** over the flat sill.
- `Frame-colonly` starts at y 0.012.

**Rulings:**
- **B1. Retracted gap 7.7 vertical vs 8.26 surface: accepted.**
  - The surface metric finds the hole edge diagonally: √(7.7² + 3.0²) = 8.26.
  - The governing number is **7.7 mm vertical**, from the tip to the tab-top plane, and 18 = 7.7 + 10.3 is the right stack. My "8.0" came from the surface reading.
  - The requirement becomes **≥ 6 mm vertical (3× the 2 mm leaf play)**. §13.2 is amended to match. No change.
- **B2. Mount bedded 1.5 mm instead of flush: accepted.**
  - Exactly flush faces fail the coplanar rule (≤ 1 mm over > 1 cm²).
  - A designed contact that would otherwise be coplanar gets a **1.0–2.0 mm bed**. 1.5 mm reads as flush and stays under the 0.010 m cap. §13.2 is amended. No change.
- **B3. Sweep top 0.062, 2 mm into the leaf bottom rail: accepted.**
  - It reads as a kerf-mounted sweep, the way a real one is retained (insert in a routed kerf, or screwed into a retainer), centred in the leaf's thickness and invisible.
  - It's under the 0.010 m cap. No gasket slot is needed. No change.
  - If a lab gate flags it, the allowlist row is `Leaf_*_Sweep` vs leaf_skin ≤ 0.003 m "kerf insertion".
- **B4. Sidelight glass sitting flush on the jamb block: specify setting blocks** (tennis tower Rev 3.10.2, Vance proposal).
  - Real practice is two EPDM/neoprene setting blocks (80–90 Shore A) at the quarter points, with about 6 mm (¼") bottom clearance and blocks ≥ 100 mm long (*real-world ref*: GANA Glazing Manual).
  - Exact numbers are in `design/strip5_tennis_tower_v1.md` Rev 3.10.2. This is Rook GLB work.

### 14.6 Open for pass H
- **Gage lab:** §14.1 base and patches, §14.2 Fix 1 and Fix 2, G2 / G3 / G4 / G6 targets, the §13.1 end-stop QA, and the tower re-probe for Rev 3.10.1.
  - Also: the bay3 lab `FloorSweep` (`_bay_guards`) must be skipped when a leaf has a `*_Sweep` child. With 49d6505 the leaf AABB bottom is 0.020, so the rig would add a second sweep at y 0.008…0.016. That puts it **4 mm into the 12 mm saddle**.
  - Drop `_sink_mat` (mat top is already 0.004).
- **Rook GLB:** Rev 3.10.2 setting blocks. The hinge/actuator 1 mm separation is advisory only.
- **Sloane:** G7.
- **Jared:** Rev 3.10.1 (12 mm sill) is built (49d6505) but still **pending Jared's approval**. If he declines it, 49d6505 is reverted, not patched.
