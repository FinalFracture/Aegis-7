# QA-05: Control smoothness re-test (2026-11-03)

- Build: fresh clone of main at `73970e0` (movement tuning). Godot 4.7.2 on the QA box (Linux), xvfb, software GL (`LIBGL_ALWAYS_SOFTWARE=1`, opengl3, llvmpipe), 1280x720, `--qa-placement`.
- Harness kept outside the repo (`/tmp/qa05r`, deleted after). It sends real `InputEventKey` / `InputEventMouseMotion` via `Input.parse_input_event` + flush, and logs every physics tick (pos, vel, floor, yaw, pitch, camera, pivot Y, `_land_dip`, `_step_ease_offset`) and every render frame (wall-clock frame time, interpolated camera).
- Movement, jump, buffer/coyote and ledge tests ran on a runtime-only flat floor at (40,0,40) with runtime-only boxes (0.15/0.30/0.40 m ledges, 1.0 m platform). Nothing saved to the project. Stairs (M-70) were walked on the real Rev C colliders (one teleport per flight, then held W).
- Sensitivity check: second run with `aegis/input/mouse_sensitivity` overridden at runtime to 0.0048 (ProjectSettings in-memory only).
- **All frame-time numbers come from the box's software renderer, not Jared's GPU.** Re-measure in T-02.

## Spec check (code + project.godot + measurement)
| Item | Spec | Code / measured | Result |
|---|---|---|---|
| Physics interpolation | on | `physics/common/physics_interpolation=true` | **PASS** (setting). Judder benefit can't be shown at ~4 fps software GL; confirm in T-02 |
| Ground accel | 45 m/s² | `GROUND_ACCEL 45`; +0.75 m/s per tick. Walk 0→90% 0.133 s, full 5.2 at 0.133 s; sprint 90% 0.183 s, full 8.2 at 0.200 s | **PASS** |
| Friction | 35 m/s² | `GROUND_FRICTION 35`; −0.583 m/s per tick. Walk stop 0.167 s / 0.34 m slide; sprint stop 0.267 s / ~0.96 m | **PASS** |
| Reverse (D→A) | – | +5.2 → −4.68 in 0.25 s (accel 45, no instant flip) | PASS |
| Air accel | 8 m/s² | `AIR_ACCEL 8`; standing jump + D: +0.1333 m/s per tick = **8.00 m/s²**, 5.2 m/s cap | **PASS** |
| Held jump = 1 jump | 1 | Space held 3 s: **1 takeoff** (`is_action_just_pressed`) | **PASS** |
| Jump buffer | 0.10 s | Press 0.067 s before landing → re-jump 1 tick after landing. Press 0.117 s / 0.183 s before → no jump | **PASS** (effective window ≈0.083 s, see SYS-19) |
| Coyote time | 0.10 s | Walk off 1.0 m ledge: Space 0.05 s after edge → jump (vy 4.8). At 0.10 s and 0.15 s → no jump | **PASS, borderline** (effective ≈0.083 s, SYS-19) |
| Step-up easing | ~0.10 s | `STEP_EASE_S 0.10`, rate 3.2 m/s. 0.40 m ledge: body +0.32 teleport, camera eased 0.053 m/tick over 6 ticks (0.10 s), max 0.053 m/tick (was 0.320) | **PASS** on 0.40 m; **0.30 m ledge FAIL** (SYS-18) |
| Landing dip | ~0.04 m | `LAND_DIP_M 0.05` × clamp(fall/8, 0.4, 1). Normal jump (vy −4.67): **0.026 m**, 0.10 s. 1 m drop (vy −3.92): **0.021 m**, 0.083 s. Drop is one tick, recovery linear 0.0046 m/tick | **FAIL (size)**: ~half the spec on normal landings (SYS-20). Smooth otherwise |
| mouse_sensitivity setting | exists, changes rate | `aegis/input/mouse_sensitivity=0.0024` (+ `user://settings.cfg [input]` override). 10 px/tick: 0.0024 → yaw −1.3751°/tick, SD 0; 0.0048 → −2.7502°/tick (×2.00), SD 0 | **PASS** |
| No invert-Y | – | pitch sign unchanged; +y mouse → pitch down (−0.6875°/tick at 5 px) | **PASS** |
| No head bob | – | camera Y range while walking 0.00000 m | **PASS** |

## Other measurements
- Mouse look: 10 px → −1.3751°/tick yaw, −0.6875° pitch; 3 px → −0.4125° / −0.2063°. SD 0 (no jitter, no smoothing).
- Jump: apex +1.216 m, airtime 0.983 s (59 ticks), unchanged.
- Step-up: 0.15 m rolls over (max cam 0.049 m/tick, no step trigger). 0.30 m: capsule slides up 0.08 m, then the step teleport fires, floor snap pulls the body back, but the ease offset still assumes 0.32 m → **camera drops 0.186 m in one tick**, then eases up over 3 ticks. 0.40 m: smooth (above). Speed never dropped below 5.2 m/s.
- **Stairs (M-70)**, held W at 5.2 m/s, 0 airborne ticks on all four runs, speed constant until the landing wall:
  - Flight 1 up: (-1.15, 0.05, -0.2) → mid landing (-1.15, 2.47, -8.52). Max cam dY 0.038 m/tick.
  - Flight 2 up: mid landing → L2 (1.15, 4.08, -0.14). Max cam dY 0.038 m/tick.
  - Flight 2 down: L2 → (1.15, 2.46, -8.52). Max 0.051 m/tick. Flight 1 down → L1 (-1.15, 0.00, 0.40). Max 0.053 m/tick.
  - No step-ups fired, no landing dips, no snags. Stairs walk cleanly both ways (not a regression; M-70 looks good here).
- **Frame time (software GL, not GPU)**: movement phases n=51 mean 225.5 ms, SD 19.2, p50 223.0, p95 255.0, p99 283.3, max 283.3. All non-settle frames n=671 mean 86.8, SD 73.9, p50 43.0, p95 242.7, p99 284.4, max 517.8. Interpolated camera moves 0.83–1.19 m per render frame while sprinting at this frame rate (box-only artefact).

## `--qa-egress`
`[EGRESS-QA] DONE failures=0` — all waypoints PASS.

## Verdict (plain)
Big improvement. Starts and stops now feel weighted instead of robotic (≈0.13 s to speed, ≈0.17 s / 0.34 m to stop when walking), air steering is limited, holding Space no longer pogo-sticks, and buffer/coyote make jumps forgiving. Look is still clean and the sensitivity setting works. Stairs are smooth. Two things still feel off: a ~0.19 m camera dip-and-rise on ~0.3 m edges (SYS-18), and the landing dip is subtle enough that most landings barely register (SYS-20).

## Tuning notes
1. SYS-18: add the actual rise, not `STEP_HEIGHT`, to `_step_ease_offset` (e.g. record `y` before the teleport and after `move_and_slide()`, and use `max(0, y_after - y_before)`), or skip the teleport when the capsule already climbed.
2. SYS-20: for ~0.04 m on a normal jump, use `LAND_DIP_M 0.07` with the same /8 scaling, or clamp(fall/5, 0.5, 1) with 0.05. Optionally ease into the dip over 2 ticks instead of 1.
3. SYS-19: check buffer/coyote before decrementing (or use 0.10 + one physics tick) to get the full 6-tick window.

## Bugs
| ID | Status | Notes |
|---|---|---|
| SYS-09 | **Closed** (pending T-02 feel check) | Physics interpolation on |
| SYS-10 | **Closed** | Accel 45 / friction 35 / air 8 measured exactly |
| SYS-11 | **Closed** | Held Space = 1 jump; buffer + coyote present |
| SYS-12 | **Closed** for 0.40 m | 0.32 m teleport now eased; the 0.30 m case is a new bug, SYS-18 |
| SYS-13 | **Closed in code** | Jump uses `is_action_just_pressed` + buffer; sub-frame tap loss not re-measured here, re-check in T-02 |
| SYS-18 | New, **Medium** | Step-up ease overshoots on ~0.30 m edges: ease offset adds 0.32 m but the body ends up only ~0.08–0.18 m higher, so the camera drops 0.186 m in one tick then rises. Repro: walk at 5.2 m/s into a 0.30 m box |
| SYS-19 | New, Low | Jump buffer and coyote windows are ~0.083 s (5 ticks), not 0.10 s, because the timers drain before the check. Coyote press at 0.10 s after the edge fails |
| SYS-20 | New, Low | Landing dip 0.026 m (jump) / 0.021 m (1 m drop) vs ~0.04 m spec, from `LAND_DIP_M 0.05 × fall/8` |
