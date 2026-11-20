# Door Lab: Quality Bar (Patch, 2026-11-20)

Numeric PASS/FAIL bar for mechanical doors proven in the isolated scene `res://scenes/test/door_lab.tscn`. This file is the ship gate. Vance owns mechanism realism (`REALISM_SPEC.md`). Sloane owns the look (`AESTHETIC_SPEC.md`). This bar cites their sections where scores overlap and does not redefine their tables.

**A run that fails any functional item is FAIL**, regardless of how it looks. Visual metrics and Vance/Sloane scores cannot salvage a functional fail.

### Authority and known conflicts

| Domain | Authority | Pointers |
|---|---|---|
| Kinematics, phase tables, masses, obstruction, gaps, settle, stagger, collider-off window, audio timestamps, G-invariance | Vance | `REALISM_SPEC.md` §0–4; acceptance **R1–R14** in §5 |
| Materials, lamps, lab lighting, wear, aesthetic cameras, 1–5 rubric | Sloane | `AESTHETIC_SPEC.md` §1–5, §7 |
| Duration / bay type / settle bounce | **Conflict**, `REALISM_SPEC.md` §6 | Until Jared or Gage records a settlement (including Vance's optional 0.7× S-curve scale), **this bar uses Vance's phase tables** for all `F-*` timing. Sloane §7.6 scores the **shipped** profile (no snaps, lamps synced, character), not her 0.9 / 0.8 / 1.8 s figures. `bay3` is the **as-built outswing** (`tt_entrance_bay_3l`, R14), not Sloane's telescoping slider (Vance §2.8 is alt only). Vance's 2 mm bumper overshoot (ζ 0.6) is allowed and is within Sloane's ≤ 3 mm settle; "no bounce" means no second bounce and no sustained oscillation (R4). |

---

## 0. Lab constants (from current main)

Grounded in `godot/scripts/preface_playable_area.gd` and `godot/scripts/tennis_tower_fixes/tt_movers.gd`. Do not silently change these in the lab; if the game values move, update this table.

| Item | Value | Source |
|---|---|---|
| Engine | Godot 4.7.2, `gl_compatibility` (`opengl3`) | `project.godot`; box bin `/home/box/.local/bin/godot` or `$GODOT_BIN` |
| Physics | 60 ticks/s (project default); `common/physics_interpolation=true` | `project.godot` |
| Player capsule | `CapsuleShape3D` r **0.35** m, h **1.75** m; shape Y = 0.875+0.12 (bottom 0.12 m above body origin) | `_setup_player_controller` |
| Eye height | **1.62** m (`CameraPivot` at 1.50+0.12). Sloane cam D uses 1.65 m for aesthetic scoring only. | same; `AESTHETIC_SPEC.md` §5 |
| Walk / sprint | **5.2** / **63.0** m/s | `WALK_SPEED`, `SPRINT_SPEED` |
| Interact | **[E]** within **2.8** m | `INTERACT_RANGE` |
| Leaf collider | `AnimatableBody3D` `TT_LeafBody`, `sync_to_physics=true`, layer 1; `_sync_body` writes `PhysicsServer3D.BODY_STATE_TRANSFORM` from `_physics_process` | `tt_movers.gd`; Vance §0.2 |

Vance §0.2: **the lab tests at walk speed**. Realistic timing cannot beat a 63 m/s sprint; do not compress phases. In game scenes the proximity radius is `v_player × t_open_to_clear` (time until the clear gap ≥ capsule diameter + 0.10 m = **0.80** m).

| Lab id | Asset / rig | Current mover (fails §1.4 until retuned) | Lab / as-built geometry |
|---|---|---|---|
| `pocket` | bi-parting sliding pocket. Preferred: Vance §1.1 (2.00 m clear, 1.000 m travel/leaf, 48 kg). Existing `tt_court_partition_door_closed` is a **1.0 m** court opening (VOTE_LOG; +Z 0.12 then ±X 0.50). | proximity 4.2 m, rate 3.4 (**0.294** s), linear Z-then-X, no ease | If the 1.0 m court asset is instanced, keep Vance times and (v, a, j); drop cruise if `2·d_acc >` actual travel. Record the choice in `meta.json`. |
| `bay3` | `tt_entrance_bay_3l`, `Leaf_0/1/2`, outswing `BAY_YAW = [-90, -90, 90]` | proximity `BAY_OPEN` **24.0** m, rate 3.2 (**0.312** s), `smoothstep` | As-built GLB, R14. Clear width ≈ **0.877** m per leaf at 90°. |
| `pair` | `tt_door_pair_18`, 90° | proximity 3.4 m, rate 3.6 (**0.278** s), `smoothstep`; latches off-closed so a walker does not reverse into the opening | As-built GLB, R14. Casing 1.96 m; meeting gap 8 mm. |
| `hatch` | heavy pressure bulkhead / hatch (Vance §4.1: 0.90 × 1.90 m clear, 1.10 × 2.10 × 0.12 m plug leaf) | **no mechanical leaf mover on main** | `door_hub_bulkhead.glb` is the RFID **hub**, not this leaf. Preface D-204 is a **force field**, out of scope. |

Clipping thresholds are the 3d-part-clipping-check skill: overlap **0.010** m, hardware embed **0.030** m, coplanar **0.001** m over **>1 cm²**, floor contact **±0.005** m. Vance R7 uses the same skill.

---

## 1. Functional (any FAIL = run FAIL)

Measure every item with the real `PlayerBody` capsule, real input (`Input.parse_input_event` / `action_press`), at 60 Hz first, then at 15 and 20 fps (§1.8). Report measured value and limit in `metrics.json`. Vance **R1–R14** are required and must appear as ids `R1`–`R14` (per door where applicable; R13 is `hatch` plus any other type that claims G-invariance).

### 1.1 Closed door blocks

**Method:** From 3.0 m on the approach normal, walk (5.2 m/s) into the fully closed door, both sides, 2.0 s of held input. Repeat a **sprint-into-closed** probe as a robustness check (same pass limits); it is not a timing test.

| Check | Limit |
|---|---|
| F-BLOCK-ORIG | Capsule origin stays **≥ 0.30** m from the closed leaf approach face (a correct r=0.35 contact is 0.35 m) |
| F-BLOCK-PEN | Capsule vs visual leaf AABB penetration **≤ 0.001** m |
| F-BLOCK-STOP | After 1.0 s of held input, speed along the approach **≤ 0.05** m/s |
| F-BLOCK-CROSS | Leading capsule point (origin + 0.35 m along approach) must not cross the closed leaf plane |

### 1.2 Opens on approach or interact

Proximity: `pocket`, `bay3`, `pair`. Interact: `hatch` uses **[E]** within 2.8 m (Vance §4.2 also has a 0.2 s badge hold). Auto-open is not required for `hatch`.

Latency clock starts at trigger-enter or the E press (t = 0 in Vance's tables). First **mechanical** event (bolt, strike, equalize valve, dog motor) must occur on the published t0, ±10% or ±1 tick, whichever is looser for sub-100 ms phases.

| Check | Limit |
|---|---|
| F-LAT-MECH | First mechanical event within Vance §n.2 t0–t1 (±10%, R2). Lamp goes cyan at that event, ±0.05 s (R12, Sloane §3 fade 0.15 s is allowed). |
| F-LAT-MOVE | First leaf travel **≥ 1 mm** (or **≥ 0.2°**) by the end of the published lurch phase, +10%. |
| F-WALK-CLEAR | Approaching at **5.2** m/s from outside the trigger, the clear gap is **≥ 0.80** m before the capsule origin is 0.50 m from the opening plane. Size `r_trigger ≥ 5.2 × t_open_to_clear + 0.85` m using Vance's profile (do not shorten phases). |
| F-SPRINT-CLEAR | **Not required in the lab** (Vance §0.2). Game scenes must set `r_trigger = v_player × t_open_to_clear`. Current `BAY_OPEN` 24.0 m is sized for the old 0.31 s move and will be wrong after the retune; flag it, do not compress `bay3` to keep 24 m. |
| F-INTERACT | `hatch`: E inside 2.8 m starts the sequence; E outside 2.8 m is a no-op. Lab may start pre-equalized (ΔP < 0.05 kPa, 7.30 s open path) if the gauge is shown. |

### 1.3 Pinch / crush and reopen-on-obstruction

**Not implemented in `tt_movers.gd`** (the pair only latches to avoid reversing into a walker). REQUIRED HOOK. Limits are Vance §n.4 (R10).

**Method:** Park the capsule in the clear opening (and separately in the leaf sweep). Command close. Also step into the sweep at 25/50/75%.

| Check | Limit |
|---|---|
| F-OBS-DETECT | Detection within **one physics tick** of the capsule intersecting the published sensor volume (light curtain / radar / leading-edge tape / current limit). |
| F-OBS-STOP | `pocket`: stop at a = 3.0 m/s², **≤ 0.20 s**, **≤ 60 mm** after detect, dwell 0.15 s, reopen on the open profile capped at **0.60** m/s, hold 3 s, retry. `bay3`: stop **≤ 0.15 s**, reopen to 90° at ω **≤ 40°/s**, hold 3 s; if the **opening** (approach) path is blocked, **stall and hold** instead of reversing. `pair`: stop **≤ 0.10 s**, reopen to 90° at ω **≤ 60°/s**, hold 2.5 s. `hatch` normal: stop at α = 40°/s² (**≤ 0.60 s**), reopen to 30°, retry after 5 s. Edge force **≤ 150 N** (`hatch`), **≤ 67 N** at the leading edge (`bay3`, `pair`), current-sense **≥ 150 N** static (`pocket`). |
| F-OBS-PASS | No pass-through; no shove of the capsule into the frame (origin teleport **≤ 0.005** m; Δv from the door **≤ 1.0** m/s). |
| F-OBS-FAULT | After **3** consecutive obstructions the door stays open (or `hatch` holds the last safe pose) and the lamp goes to Sloane's fault blink (2 Hz, 50% duty). |
| F-OBS-OFF | Collider may be disabled only while that leaf's remaining gap **< 0.80** m, and only in the published close creep / latch phase (Vance §0.2, R9). Outside that window the collider stays on. |
| F-OBS-EMERGENCY | `hatch` pressure-emergency (ΔP rising > 2 kPa) does **not** reverse (Vance §4.4). Optional lab probe; if unimplemented, list as a hook and skip, do not PASS it. |

### 1.4 Open / close time windows

Vance phase tables, **±10%** on each phase t0/t1 and on the totals (R2). Profile is a jerk-limited S-curve (Vance §0.1); cubic ease is allowed **only** in published creep / back-check phases. Current `tt_movers` rates (0.278–0.312 s) **fail this section**.

| Type | Open (t=0 = request) | Close | Stagger / settle |
|---|---|---|---|
| `pocket` | **2.00 s** total; leaf motion 0.30–1.85 s; v_peak **1.30** m/s, a = 3.0, j = 20 | **3.75 s**; v_peak **0.60** m/s; closing KE **≤ 10 J**/leaf (measured 8.6 J) | 0 ms (one belt). Bumper overshoot **2 mm**, f = 6 Hz, ζ = 0.6; stop sampling at \|x\| < 0.2 mm |
| `bay3` | **2.95 s** (last leaf **3.07 s**); ω_peak **80°/s** | last leaf **4.87 s**; ω_peak **30°/s** | Open: Leaf_1 0, Leaf_0 **+60 ms**, Leaf_2 **+120 ms**. Close: reverse (Leaf_2 0, Leaf_0 +60, Leaf_1 +120). ±20 ms (R5). Settle overshoot **0.8°**, f = 3 Hz, ζ = 0.5 |
| `pair` | **2.25 s** (Leaf_R **2.31 s**); ω_peak **110°/s** | Leaf_L **4.46 s**; closer sweep ω_peak **30°/s** | Leaf_L leads open **+0 / +60 ms**; close Leaf_R leads **+0 / +60 ms**. ±20 ms. Open settle **1.0°**, f = 3 Hz, ζ = 0.45. Close bounce **0.3°**, ζ = 0.6 |
| `hatch` | **8.40 s** (7.30 s pre-equalized); leaf swing starts after dogs + deflate; ω_peak **30°/s** | **10.40 s**; ω_peak **20°/s** | 8 dogs, **30 ms** stagger. Settle **0.3°**, f = 1.5 Hz, ζ = 0.7. Wheel/dogs **before** the leaf, not after |

Peak velocities within **±10%** (R3). Every published phase occurs in order; latch / seal / lurch may not be skipped (R1).

### 1.5 Collider tracks the visual every physics frame

**Method:** Every physics tick during open, close, hold, and obstructed reverse, compare `TT_LeafBody.global_transform` (and `PhysicsServer3D.body_get_state(..., BODY_STATE_TRANSFORM)`) to the visual leaf mesh origin. Sample the **physics** pose, not the interpolated render pose.

| Check | Limit |
|---|---|
| F-DRIFT | Max translational drift visual mesh origin vs physics body **≤ 2 mm** every tick (R9: "equals" — 2 mm is the measurement epsilon) |
| F-DRIFT-ANG | Max rotational drift **≤ 0.15°** |
| F-DRIFT-SHAPE | Each moved `CollisionShape3D` under `TT_LeafBody`, AABB centre vs the matching visual submesh, **≤ 2 mm** |
| F-DRIFT-OFF | `collider_enabled` is false only inside F-OBS-OFF (R9) |

### 1.6 No leaf clipping (sampled poses and in motion)

Run 3d-part-clipping-check at **0 / 25 / 50 / 75 / 100%** of leaf travel and at mid-close, and also every physics tick (or every 5% if a tick-level mesh query is too heavy — still **required** to fail a tick that would breach). R7.

| Check | Limit |
|---|---|
| F-CLIP-LEAF | Leaf vs frame / jamb / header **visible** faces, leaf vs leaf, leaf vs floor / mullion / pocket liner: overlap **≤ 0.010** m |
| F-CLIP-HW | Intentional hardware embeds (hinges, tracks, dogs, bolts, seals, pull / push hardware) **≤ 0.030** m |
| F-CLIP-COPLANAR | No coplanar faces within **0.001** m over an area **> 1 cm²** |
| F-CLIP-POCKET | `pocket` leaves may occupy the **header / jamb pocket envelope**. Overlap with any **visible** frame face still uses 0.010 m. Pocket liner clearance is Vance §1.5 (15 mm each face; 50 mm behind the tail at full open), judged under R8 not as a clip fail. |
| F-CLIP-SWEEP | `bay3` / `pair` / `hatch` sweep: 0 hits vs lab bollards, floor, soffit, and adjacent leaves above the limits. `bay3` tip vs bollards as-built ≈ 455 mm, required ≥ 300 mm (Vance §2.5). |

Report failures as a table: asset, parts, penetration depth (m), pose %, severity, suggested fix. A single breach is FAIL.

### 1.7 Sprint-through and walk-through without snagging

Walk-through is the lab circulation test. Sprint-through is run only with the door **already fully open** (leaves parked), to catch snags; it does not require the door to beat 63 m/s.

| Check | Limit |
|---|---|
| F-SNAG-WALK | Walk 5.2 m/s through the open opening on the centreline: no stop > 50 ms, speed ≥ 5.0 m/s once past, lateral deviation **≤ 0.10** m, **0** contacts with leaves or frame |
| F-SNAG-SPRINT | Same, already-open, at 63.0 m/s: once past, speed **≥ SPRINT_SPEED − 3.0** m/s (or ≥ 95% of a control run with leaf collision off); no stop > 50 ms; lateral deviation **≤ 0.10** m; **0** leaf/frame contacts at the open pose |
| F-SNAG-CLEAR | Open clear width minus 0.70 m leaves **≥ 0.08** m per side on the centreline. Vance pocket 2.00 m is well clear. As-built `bay3` ≈ 0.877 m per leaf is tight (0.177 m total, 0.088 m/side if centred) — PASS only if the measured centreline clearance holds; do not average across mullions. `pair` 1.8 m class opening is comfortable. `hatch` 0.90 m clear → 0.10 m/side, in spec if centred. |

### 1.8 Low-fps robustness

The harness **must** set `Engine.max_physics_steps_per_frame = 1` (same pattern as `--qa-stairs`, `--qa-tower-entry`, `--qa-tower-collide`). Run the full functional set at `--fixed-fps 60`, **20**, and **15**. Pass criteria are identical. Time-based limits (ms, seconds) do not scale. §2.3 residuals stay time-normalized.

### 1.9 Repeated cycling

| Check | Limit |
|---|---|
| F-CYCLE | **50** full open/close cycles per type, no obstruction (hold timers may be shortened in the harness if recorded; phase shapes must not change) |
| F-CYCLE-POSE | Final closed pose vs cycle 1: translation **≤ 1 mm**, rotation **≤ 0.1°** |
| F-CYCLE-STATE | Phase machine returns to idle closed; no desync, no stuck mid-pose |
| F-CYCLE-LOG | 0 script errors, 0 physics warnings about moved static bodies |
| F-CYCLE-G | `hatch` (R13): timings unchanged at 0.08 / 1.0 / 1.45 G, **±5%**. Other types claim the same if they are actuator-driven (Vance §0.3); at least one 1.0 vs 1.45 G spot check per type. |

---

## 2. Measurable visual checks (renders + motion samples)

Any `V-*` fail is a visual FAIL. Sloane's 1–5 rubric (`AESTHETIC_SPEC.md` §7) and Vance R6 / R8 / R11 / R12 are additional, not substitutes.

Capture rules: **do not use `--headless` for screenshots**. `DisplayServer=headless` cannot read the viewport (`player_camera.gd`). Use xvfb + `opengl3` (§3). Prefer 1920×1080; 1280×720 is an allowed box fallback at the same FOV, flagged in `meta.json`.

### 2.1 Z-fighting

| Check | Limit | Method |
|---|---|---|
| V-ZFIGHT-GEO | Same as F-CLIP-COPLANAR: 0.001 m, >1 cm² | mesh query at closed, 50%, open |
| V-ZFIGHT-FLICKER | Static closed, 8 frames, seam ROI (meeting stile + jamb, 16 px band). Mean \|Δ\| vs previous frame **≤ 2/255**. Pixels with \|Δ\| **> 8/255** in **≥ 3** of 8 frames: **0**. | front + jamb cams, lab rig on, no camera motion |

### 2.2 Closed-gap uniformity and alignment

Gaps follow Vance §n.5, **±2 mm** (R8). Swing angles in the open pose **±0.5°**.

| Check | Limit (closed unless noted) |
|---|---|
| V-GAP-POCKET | Meeting stiles: **0 mm** visible (2 × 12 mm bulbs compressed **3 mm**). At bolt release: **6 mm**. Leaf–jamb pocket faces **6 mm**. Leaf–floor **8 mm**. Leaf–soffit **10 mm**. Full-open lap into pocket **25 mm**. |
| V-GAP-BAY | Meeting / mullion **3 mm** each side. Hinge stile to frame: as-built 55 mm must be covered by a finger guard so **visible** gap **≤ 10 mm** (Vance §2.5; if the guard is missing, R6/R8 FAIL, do not silently accept 55 mm). Leaf–floor required **8 mm** (as-built 60 mm / 48 mm visible is a known Rook flag — FAIL V-GAP-BAY until filled or formally waived). |
| V-GAP-PAIR | Meeting stile **3–8 mm** (as-built 8 mm, at the limit). Hinge edge **3–5 mm**. Leaf–floor **8–12 mm** (as-built 10 mm). |
| V-GAP-HATCH | Leaf to frame, seal deflated, **6 mm** all round. Inflated compression **8 mm**. Leaf to sill **6 mm**. |
| V-GAP-STD | Along any one gap, ≥ 8 samples over the clear height: std dev **≤ 1.0 mm**, max deviation from the mean **≤ 2.0 mm**. |
| V-ALIGN-YAW | Closed leaf yaw vs frame **≤ 0.25°**. Open angle vs 90° (or hatch 100°) **±0.5°** (R8). |

### 2.3 Motion curve, popping, jumps

Sample every physics tick (Vance's `t, leaf_pos[], leaf_vel[], phase, lamp_state, collider_enabled` log, plus drift and gap). Compare to the published S-curve, not to a single cubic.

| Check | Limit |
|---|---|
| V-EASE-SCURVE | No linear whole-move tween. Velocity steps **> 5% of v_peak** in one 60 Hz tick are FAIL (R3). Cubic ease only inside published creep / back-check. Crack-open lurch is a separate phase. |
| V-POP | Residual from the published `sample(t)` curve **> 2 mm** (or **> 0.15°** on swing types) at any tick is FAIL. At 15/20 fps the same residual vs the time-parameterized curve applies (do not scale by dt). |
| V-JUMP | C0 break: a raw second difference \|p[i] − 2 p[i−1] + p[i−2]\| **> 4 mm** at 60 Hz (scale that second-difference limit by (dt / 1/60)² at 15/20 fps) outside a published phase boundary. Phase boundaries must still be C0 (no position jump **> 2 mm** / **0.15°**). |
| V-SETTLE | Overshoot amplitude **±25%** of the published A (R4); decays (no sustained oscillation). Stop criterion \|x\| < 0.2 mm or 0.05°. |
| V-LAMP-SYNC | Cyan at the first mechanical event and green at final settle, **±0.05 s** (R12). Fade **0.15 s**, no hard snap (`AESTHETIC_SPEC.md` §3). |
| V-AUDIO | Every published cue fires within **±1 physics tick** of its timestamp (R11). If the lab has no audio yet, this is a hook, not a silent PASS. |

### 2.4 Texture, lighting, closed look

| Check | Limit | Method |
|---|---|---|
| V-STRETCH | Rigid leaves: per-triangle area and UV Jacobian change vs rest **≤ 1%** at 0/25/50/75/100% | mesh query |
| V-LUMA | Leaf-face mean luma **≥ 0.10** (sRGB) under the lab rig | Sloane cam A and front, closed and open |
| V-SHADOW | Same flicker limits as V-ZFIGHT-FLICKER on the lit leaf face. Lab downlight / key have shadows on (`AESTHETIC_SPEC.md` §4–5). | A + front, closed |
| V-ALBEDO | No leaf or frame albedo **> 0.90**. Door-lab `TT_WhiteComposite` target is **0.847 / 0.871 / 0.902** (`AESTHETIC_SPEC.md` §1.1). | material dump |
| V-HW | Vance R6: every item in §n.6 / §4.7 is visible in at least one of cameras A/B/C/E, or is legitimately behind a shown access panel. | renders |

---

## 3. Reviewer kit

### 3.1 REQUIRED HOOKS (not on main as of this commit)

Flag for Gage. Until these exist, do not mark a type PASS.

1. **`res://scenes/test/door_lab.tscn`** — isolated lab, all four types, Sloane §5 rig (do not copy that rig into game scenes), real `PlayerBody` capsule, named cameras below. Does not exist.
2. **`--qa-door-lab`** — functional harness: §1 probes, `Engine.max_physics_steps_per_frame = 1`, JSON + Vance CSV log, exit code 0 only if every functional check PASSes. Current `--qa-*` flags live on `preface_playable_area.gd` and do not cover this scene.
3. **`--qa-door-lab-shots`** — xvfb / `opengl3` capture of §3.3, plus a contact sheet. Cannot run under `DisplayServer=headless`.
4. **`--qa-door-lab-out <dir>`** — write the layout in §3.2. Relative paths are from the Godot project (`godot/`); prefer `../qa/door_lab/<run>/`.
5. **`DoorProfile` (or equivalent) + obstruction planner** — Vance §0.2: jerk-limited `sample(t)`, re-plan from current pose/velocity on obstruction. Reopen-on-obstruction / anti-crush for all four types (§1.3). Pair's current latch is not sufficient.
6. **Hatch / bulkhead mechanical leaf rig and mover** — plug leaf, 8 dogs, wheel, inflatable seal, equalize gauge, sequences in Vance §4. `door_hub_bulkhead.glb` is not that leaf.
7. **Per-tick telemetry** — at least `t, leaf_pos[], leaf_vel[], phase, lamp_state, collider_enabled` (Vance §0.2) plus `drift_mm, gap_mm, contacts` in `motion.csv`.
8. **Motion retune** to Vance §n.2/§n.3 (S-curve, lurch, creep, published staggers, settle). Court two-phase linear Z-then-X is a V-EASE-SCURVE / V-POP fail. Do not compress phases to preserve the old 24 m bay trigger.
9. **Walk-trigger retune** so F-WALK-CLEAR passes at the new `t_open_to_clear`. Game-scene sprint triggers are a follow-up, not a lab compress.
10. **Clipping assert** in the lab at 0/25/50/75/100% and mid-close, skill thresholds, fail the run on a breach (R7).
11. **Cycle + low-fps + G modes** — 50 cycles; `--fixed-fps 15` and `20` with 1 physics step/frame; R13 gravity spot checks.
12. **Interact path for `hatch`** — [E] / `INTERACT_RANGE` 2.8 m, 0.2 s hold. Proximity types may stay automatic (radar / push-bar as published).
13. **Audio one-shots and loops** (R11) if the lab is to take a ship PASS; otherwise leave V-AUDIO / R11 as an open hook.
14. **`bay3` finger guards and leaf-to-floor sweep** (Vance §2.5) — as-built gaps fail R8 until Rook fills them or Jared waives.

### 3.2 Commands

Always import first. `--` starts user args. `GODOT_BIN` defaults to the box binary.

```bash
GODOT_BIN="${GODOT_BIN:-/home/box/.local/bin/godot}"
RUN="qa/door_lab/$(date +%Y%m%d-%H%M)-CT-$(git -C . rev-parse --short HEAD)"

# 1) Import (always, headless)
"$GODOT_BIN" --headless --path godot --import --quit

# 2) Functional, 60 Hz
"$GODOT_BIN" --headless --path godot --fixed-fps 60 \
  res://scenes/test/door_lab.tscn -- --qa-door-lab --qa-door-lab-out "../${RUN}"

# 3) Functional, low fps (harness caps physics at 1 step/frame)
"$GODOT_BIN" --headless --path godot --fixed-fps 20 \
  res://scenes/test/door_lab.tscn -- --qa-door-lab --qa-door-lab-out "../${RUN}_20fps"
"$GODOT_BIN" --headless --path godot --fixed-fps 15 \
  res://scenes/test/door_lab.tscn -- --qa-door-lab --qa-door-lab-out "../${RUN}_15fps"

# 4) Screenshots + contact sheet (xvfb / opengl3, NOT --headless)
xvfb-run -a -s "-screen 0 1920x1080x24" \
  env LIBGL_ALWAYS_SOFTWARE=1 \
  "$GODOT_BIN" --path godot --rendering-driver opengl3 --fixed-fps 60 \
  res://scenes/test/door_lab.tscn -- --qa-door-lab-shots --qa-door-lab-out "../${RUN}"
```

`--import` is required on a fresh clone (class cache). Functional runs may use `--headless`. Shot runs must not. Box software GL is `LIBGL_ALWAYS_SOFTWARE=1` / llvmpipe; note that in `meta.json` (`renderer: "llvmpipe"` vs a GPU name).

### 3.3 Output layout

```
qa/door_lab/<run>/
  meta.json
  summary.json
  contact_sheet.png
  <door>/                    # pocket | bay3 | pair | hatch
    metrics.json
    clips.json
    motion.csv
    shots/
      <camera>_<state>.png
```

`<camera>` = `front` | `oblique45` | `jamb` | `top` | `player` plus Sloane's `A`–`E` when those are also shot (`hero`, `square`, `detail`, `player_sloane`, `threshold`).
`<state>` = `closed` | `025` | `050` | `open` | `closing` (closing = 50% of leaf travel on the close curve).

**Required QA matrix (this bar):** cameras `front`, `oblique45`, `jamb`, `top`, `player` × all five states, every door (100 frames) + `contact_sheet.png`.

Camera placement (QA set). Door opening centre is the look-at unless noted. Player eye uses the **repo** 1.62 m pivot.

| ID | Placement | FOV |
|---|---|---|
| `front` | 4.0 m on axis, 1.62 m high (square-on) | 40° |
| `oblique45` | 3.2 m, 1.62 m high, **45°** off the door normal | 50° |
| `jamb` | 0.9 m from jamb or handle, 1.1 m high, 45° | 35° |
| `top` | 4.0 m above the opening, looking down, up-axis = door normal | 40° |
| `player` | 1.8 m on axis, **1.62** m high | project player FOV **70°** (`_camera.fov = 70.0`). If the project FOV moves, use that value and record it. |

Sloane `AESTHETIC_SPEC.md` §5 (A–E, including player-eye at 1.65 m / 75°) is the **aesthetic** set and must also be captured when Sloane scores. Do not replace the QA matrix with A–E; her listed subset (A all 5 states, B closed, C closed+open, D mid-travel, E open, plus a 24 fps 8-frame open strip on A) is required for her rubric. Vance R6 uses A/B/C/E.

### 3.4 JSON schemas

`meta.json`:

```json
{
  "commit": "<full sha>",
  "godot": "4.7.2",
  "renderer": "gl_compatibility/opengl3",
  "gpu": "llvmpipe|...",
  "fixed_fps": 60,
  "physics_ticks_per_second": 60,
  "max_physics_steps_per_frame": 1,
  "resolution": [1920, 1080],
  "timing_authority": "vance",
  "pocket_geometry": "vance_2m|court_1m",
  "updated": "YYYY-MM-DD HH:MM CT",
  "scene": "res://scenes/test/door_lab.tscn"
}
```

`summary.json`:

```json
{
  "verdict": "PASS|FAIL|CONDITIONAL",
  "functional": "PASS|FAIL",
  "visual": "PASS|FAIL",
  "sloane": "PASS|FAIL|PENDING",
  "vance": "PASS|FAIL|PENDING",
  "doors": {
    "pocket": {"functional": "PASS|FAIL", "visual": "PASS|FAIL"},
    "bay3":   {"functional": "PASS|FAIL", "visual": "PASS|FAIL"},
    "pair":   {"functional": "PASS|FAIL", "visual": "PASS|FAIL"},
    "hatch":  {"functional": "PASS|FAIL", "visual": "PASS|FAIL"}
  },
  "hooks_missing": ["..."]
}
```

`metrics.json` (per door): an array of `{ "id": "F-BLOCK-ORIG", "pass": true, "measured": 0.352, "limit": 0.30, "unit": "m", "note": "" }`. Include every `F-*`, `V-*`, and `R1`–`R14` id. `clips.json` is the failure table from §1.6 (empty array on pass). `motion.csv` headers: `tick,time_s,phase,leaf,px,py,pz,yaw_deg,vel,drift_mm,gap_mm,contacts,lamp,collider_enabled`.

Exit code of `--qa-door-lab` is **1** if `functional` is FAIL or any required hook is missing; **0** only on functional PASS (visual shots are a second process).

### 3.5 Verdict rules

1. **Any functional FAIL (`F-*` or Vance R1–R5, R7, R9, R10, R13, R14) => overall FAIL.** One failed door fails the lab.
2. **Any measurable visual FAIL (`V-*` or Vance R6, R8, R11, R12) => overall FAIL**, even if functional passed. Open hooks for audio (R11) do not let you mark R11 PASS; they keep the door from a ship PASS until done or waived.
3. **Sloane** (`AESTHETIC_SPEC.md` §7): average **≥ 4.0**, no criterion **< 3**, and criteria **1, 3, 6 ≥ 4**. Logged in `context/VOTE_LOG.md`. Overall cannot be PASS while Sloane is FAIL. While her scores are not yet logged, `sloane` is `PENDING`. Criterion 6 is judged against the **shipped** (Vance) profile until the §6 duration conflict is settled.
4. **Vance** (R1–R14 plus his review of renders): overall cannot be PASS while `vance` is FAIL. While he has not logged a review, `vance` is `PENDING`.
5. **Combine:** `overall = PASS` iff functional PASS **and** visual PASS **and** Sloane PASS **and** Vance PASS. If Sloane and/or Vance are `PENDING` but F+V pass, the run is **`CONDITIONAL`** — not a ship PASS.
6. Missing REQUIRED HOOKS => **FAIL** (or do not score that type). List them in `hooks_missing`.
7. Unsettled `REALISM_SPEC.md` §6 duration / bay-type conflict is not itself a FAIL, provided this bar's Vance-timing rule is followed and the conflict is noted in `meta.json`. A later settlement that picks Sloane's times requires a QUALITY_BAR amendment.

A `CONDITIONAL` run is useful progress. It is not permission to place the lab doors as finished in the tower.
