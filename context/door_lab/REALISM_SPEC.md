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
- **Player sprint (63 m/s in `tt_movers.gd`):** realistic timing can't beat a sprinting player. The lab tests at **walk speed**. In game scenes the proximity trigger radius is `v_player × t_open_to_clear` (time until the clear gap ≥ capsule diameter + 0.1 m). Don't compress the mechanism phases.
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

  If the tempo must be faster, Vance proposal: scale **only the S-curve phases** by up to 0.7× and keep the latch, seal, dog and equalize phases real, because those carry the "real machine" read.
- **Bay3:** Sloane specs a telescoping slider, but the built asset is an outswing swing door. This spec covers the as-built door, with the slider in §2.8 as the alternative.
- **Settle:** Sloane says "no bounce" for the sliders. This spec allows a 2 mm overshoot on a bumper (ζ 0.6, a single visible decay), which is within her ≤ 3 mm settle.

Label: Vance proposal on all design calls above that are not taken from the as-built GLBs or marked *real-world ref*.
