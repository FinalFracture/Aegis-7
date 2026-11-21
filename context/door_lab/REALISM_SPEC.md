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
- **Leaf weight:** all masses below are at 1.0 G. Hinges, rollers and struts are sized for **1.45 G** (the Drum RPM max). Every powered door is **actuator- and damper-driven, not gravity-driven**, so its timing is the same at any G.
- **At 0.08 G:**
  - A slider leaf weighs about 4 kgf, so belt jerk could lift it off the track. That is why the **anti-lift rollers are mandatory and visible**.
  - A gas-strut hatch counterbalanced for 1.0 G would spring open. That is why the hatch uses a **rotary hydraulic damper plus a powered lock** (§4.6).

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
- [ ] Rubber end-stop bumper in each pocket.
- [ ] Meeting-stile bulb seals.
- [ ] Head solenoid bolt and keeper.
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
| Counterbalance | **2 gas struts** giving **585 N·m (85%)**. A human can open it with ≤ 200 N on the handle, and gravity still holds it shut at 1.0 G. |
| Why also damper + powered lock | the Drum RPM range is 0.08–1.45 G. At 0.08 G the weight moment is 55 N·m and the struts would throw the leaf open, so a **rotary hydraulic damper caps the speed at 35°/s** and the actuator drives it closed against the struts (≤ 530 N·m). At 1.45 G the actuator adds 410 N·m to open. |
| Open timing | phases 1–6 as §4.2, then the S-curve 0.7 → 105° with ω 35°/s, α 35, j 105 (**4.28 s**) |
| Total open | **7.63 s** (3.35 + 4.28) |
| Hold-open | gas-strut lock sleeve + mechanical stay arm that drops into a detent (clunk) |

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
- [ ] Hatch only: 2 gas struts, stay arm, damper.

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

**Close: 6.39 s** (real 10.65). **Safety rule step 2:** 0.45× (44.4°/s) gives **14.0 J ✗**, so close travel runs at **0.6×**: ω **33.3°/s (7.9 J ✓)**, α 55.6°/s², j 278°/s³. Against the gas struts the actuator still has to deliver ≤ 530 N·m (§4.6); that doesn't change.

| # | Phase | k | t0–t1 (s) | Motion |
|---|---|---|---|---|
| 1 | Klaxon / beacon | 0.6 | 0.00–0.60 | — |
| 2 | Stay-arm / strut-lock release | — | 0.60 | release clunk |
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
- **Lab coverage:** the "hatch" is the wall plug bulkhead (vertical). There is no horizontal floor-hatch case (§4.6: 105°, 2 gas struts, stay-arm detent, damper), and R13 (0.08/1.0/1.45 G) is not reported. F-OBS-EMERGENCY (§4.4) isn't implemented.
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
  - Not shown: the 2 gas struts, stay arm with detent, rotary damper, seal, dogs, handle or frame flange.
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
