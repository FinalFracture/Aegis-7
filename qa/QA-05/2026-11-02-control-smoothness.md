# QA-05: Control smoothness sweep (2026-11-02)

- Build: fresh clone of main at `ee10b2b` (Rook: M-70 Rev C stair core collision). Godot 4.7.2, run on the QA box (Linux).
- Harness: `/tmp/qa05c/drv.gd` and `main.gd`, kept outside the repo. It sends real `InputEventKey` and `InputEventMouseMotion` through `Input.parse_input_event`, then flushes. Ran under xvfb with software GL (`LIBGL_ALWAYS_SOFTWARE=1`, opengl3, 1280x720) using `--qa-placement`. It logs these per physics tick: delta, position, velocity, is_on_floor, body yaw, pitch and camera position. It logs these per render frame: delta, wall-clock frame time and camera position.
- Test floor: the movement and step tests ran on a temporary flat collision floor that exists only at runtime, at (40,0,40), clear of apartment walls. The ledge boxes are 0.15, 0.30 and 0.40 m tall. Nothing was saved to the project. **The stairs (M-70) were not tested.**
- **All frame-time numbers come from the box's software renderer (llvmpipe, no GPU). They are not from Jared's GPU and they are not representative.** Re-measure on real hardware in T-02.

## Controller facts (from code, `scripts/preface_playable_area.gd`)
| Item | Value |
|---|---|
| WALK_SPEED / SPRINT_SPEED | 5.2 / 8.2 m/s |
| Acceleration / friction | **none**: `velocity = dir * speed` every tick (l.3685) |
| Air control | full: the same instant assignment applies in the air |
| JUMP_VELOCITY / GRAVITY | 4.8 m/s / 9.8 m/s² |
| Jump trigger | `Input.is_action_pressed("jump")` while on the floor (held, not just_pressed). No coyote time, no jump buffer |
| STEP_HEIGHT | 0.32 m, applied as a single `global_position += up` teleport (l.3686-3691) |
| floor_snap_length / floor_max_angle | 0.35 m / 50° |
| MOUSE_SENS | 0.0024 rad/px = **0.1375 °/px**, uses `screen_relative`, raw, no smoothing, no accel. Pitch clamp −80°/+75° |
| KEY_LOOK_SPEED | 2.2 rad/s (Q/Left/Right, PgUp/PgDn ×0.6) |
| Where it runs | movement in `_physics_process` (60 Hz). Mouse look in `_unhandled_input`. Camera is a child of the body (pivot at 1.62 m) |
| Physics interpolation | **off** (no `physics/common/physics_interpolation` in project.godot) |
| Head bob | none (camera Y range while walking: 0.0 m) |

## Measurements
**Acceleration and deceleration** (on the flat floor)
- Walk: 0 → 5.20 m/s in **1 tick (16.7 ms)**. Time to 90% = 16.7 ms. Stop takes 1 tick (0 m slide).
- Sprint: 0 → 8.20 m/s in 1 tick. Stop takes 1 tick. Steady-state speed SD is 0.000 (perfectly flat curve).
- Strafe and reverse also switch direction in 1 tick (D→A flips the full 5.2 m/s instantly).

**Mouse look** (constant 10 px/tick and 3 px/tick, with a y component of half that)
- Yaw per tick is −1.3751° (10 px) and −0.4125° (3 px), **SD 0.0000°**. Pitch is −0.6875° and −0.2063°, SD 0. That's an exact 0.1375 °/px with no smoothing and no jitter.
- Look is event-driven, so it doesn't depend on frame rate in total degrees. Camera rotation, however, only shows at render rate.

**Jump** (tap)
- Apex +1.216 m. Airtime 0.983 s (59 ticks). Landing vy is −4.67 m/s, then 0 in one tick.
- No bounce. Landing settles in 2 ticks (y +0.063 → −0.0001). No camera dip.
- Holding Space: re-jumps after **3 ground ticks**, so it auto-bunny-hops (3 takeoffs in 2.5 s).
- In-air horizontal speed stays at a constant 5.2 m/s (full air control).

**Step-up** (ledge heights are box height. The capsule bottom sits 0.12 m above the body origin, so the effective lift is height − 0.12)
| Ledge | Result | Largest per-tick camera dY |
|---|---|---|
| 0.15 m | rolls over, no visible rise | 0.049 m |
| 0.30 m | climbs via capsule slide, +0.079 m in one tick, then −0.149 m over 2 ticks stepping off | 0.092 m |
| 0.40 m | **steps up by a 0.32 m teleport in one tick (a pop)**, speed kept at 5.2 | **0.320 m** |
Nothing caught and speed never dropped below 5.2 m/s.

**Frame time** (software renderer on the box, **not GPU**)
- During movement: mean 222.8 ms, SD 23.1, p95 258.8, p99 305.6, max 305.6 ms (n=48). All were above 100 ms.
- All non-settle frames: mean 70.9, SD 69.4, p50 33.8, p95 231.4, p99 267.0, max 330.5 ms.
- At this frame rate the camera jumps 1.093 m per render frame while sprinting. That's 8 physics ticks per frame and no interpolation. It's exaggerated here, but it's the same mechanism behind SYS-09.

## Verdict (plain)
Look feels clean: it's raw, exact and jitter-free. Movement feels **robotic and twitchy**. There's zero acceleration, a dead stop and instant 180° direction flips. You also get full air steering, so jumps feel floaty but fully steerable. Holding jump pogo-sticks. The 0.32 m step-up teleport causes a visible camera pop on ~0.4 m edges. With physics interpolation off, motion will judder on any display that isn't locked at 60 Hz (144 Hz monitors, or frame-rate dips). That's probably the biggest "doesn't feel smooth" factor on Jared's machine. Confirm in T-02.

## Tuning suggestions
1. Turn on `physics/common/physics_interpolation=true`. Call `reset_physics_interpolation()` on the body and camera after teleports (respawn, presets, step-up).
2. Ground accel: `velocity_h = velocity_h.move_toward(dir*speed, ACCEL*delta)` with ACCEL ≈ **45 m/s²** (t90 ≈ 0.10 s walk, 0.16 s sprint). Friction when there's no input ≈ **35 m/s²** (walk stops in ~0.15 s, ~0.4 m slide).
3. Air accel ≈ **8 m/s²**, and keep horizontal momentum on takeoff.
4. Jump: trigger on `is_action_just_pressed`, add a **0.10 s jump buffer** and **0.10 s coyote time**. For a snappier arc, try GRAVITY 13, JUMP_VELOCITY 5.4 (apex ≈1.12 m, airtime ≈0.83 s).
5. Step-up: after the teleport, offset the camera pivot down by the step amount and ease it back over **~0.10 s** (lerp the rate ≈ 10/s). Alternatively, rely on interpolation from item 1.
6. Optional head bob: 0.025 m vertical at ~1.8 Hz walk and 2.3 Hz sprint, with a settings toggle. Optional landing dip of 0.04 m when vy < −4.
7. Sensitivity 0.0024 rad/px is fine. Expose it in settings (0.0010–0.0060) along with invert-Y.

## Bugs
| ID | Sev | Title | Repro |
|---|---|---|---|
| SYS-09 | Medium | Physics interpolation off. Movement and camera update at 60 Hz physics only, so it judders at render rates ≠ 60 Hz | Run on a 144 Hz display or with uncapped FPS and strafe past a wall edge. On the box at ~7 fps the camera stepped 1.09 m/frame while sprinting. Confirm on GPU (T-02) |
| SYS-10 | Medium | No acceleration, friction or air-control limit (0→top speed and top→0 in 1 tick, full steering mid-air) | Hold W then release, or tap D/A. The velocity log shows a 0 / 5.2 / 8.2 step function |
| SYS-11 | Low | Holding Space auto-bunny-hops. No coyote time or jump buffer | Hold Space on flat ground. It re-jumps after 3 ground ticks |
| SYS-12 | Low | Step-up is a one-tick 0.32 m teleport, so the camera pops on ~0.3–0.45 m edges | Walk into a 0.40 m box (runtime test box, not the stairs). Camera Y jumps 0.32 m in one tick |
| SYS-13 | Low (low-FPS only) | Key taps shorter than one render frame can be lost. Buffered input is flushed per render frame, and `jump` is polled as a held state | At ~7 fps (software GL), a 2-tick Space tap gave no jump until the harness flushed input explicitly. Using just_pressed plus a buffer (SYS-11 fix) covers it |

Not tested: the stairs (M-70, on hold). GPU frame-time is left for T-02.
