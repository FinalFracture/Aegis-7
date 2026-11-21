# Repeat failures (Patch, 2026-11-02)
Bugs that failed re-test two or more times, or came back after being marked fixed, from `git log` and the history of `qa/MASTER_BUG_LIST.md` / `context/playtest_bug_report.md`. Only entries the history supports. M-06 (never claimed fixed) and M-69 (blocked: lighting look on hold per Jared) are excluded.

## M-02 — Prop43 spares dispenser position (resolved 2026-11-02 by fixing the spec)
| Commit | Attempt | Result at re-test |
|---|---|---|
| f80c0de, 4f5d639 | clear Rook SeamFix walls; nudge for pair gap/front zone | still clashing |
| 1a349a3 | on West Storage SeamFix wall face | Patch pass 1a349a3: placement 3 fails (clearance, mesh_clearance, front_zone) |
| 8b32d42, d58ccab, a4526df, 8855f8c, 11e51da | East Lounge north wall, rev2, option (a) x -8.00, rev3 east wall | GEO-10 (00914fd) found it at (-8.0, 0.235, 8.5), not rev3 |
| 04bbed0 | Rev C 101 east wall (-4.858, 0.12, 5.20) | QA-04 r2 LAY-14 / QA-02 GEO-11: overlaps the planned 101 wardrobe; Patch r2..r4: Δx +0.30 m, Δy -0.115 m vs rev3 target (-5.16, 0.235, 5.20) |
| 6c6c4f6, 4e9849a, cea80bc, ff057ff | wardrobe moved to the west wall (GEO-11) | wardrobe overlap fixed; position still off target at 9ecfdef |
**Likely cause:** the target moved with each wall rebuild (SeamFix walls, then the Rev C grid) and the design doc (rev3 on the old lounge face x -4.90) was never re-derived for the Rev C partition face x -4.6, so code and design disagree by design. **Resolution:** the 'misplacement' was a spec that kept moving. Vance locked a wall-relative rule in 0b4aa94 (x = x_wall -4.600 - 0.258, y = floor top, z 5.20, yaw -90), which matches the code already on main since 04bbed0. Patch verified on 0b4aa94: position = rule, floor contact 0.000 m, no overlaps; wardrobe on the west wall (GEO-11 closed).

## M-61 (with SEAM-02 / M-38 / M-45) — room-shell corner seams (fixed at 9ecfdef)
| Commit | Attempt | Result at re-test |
|---|---|---|
| 5da308c | Rook SEAM-01/02 corner-closing skins | Patch 1a349a3: SEAM-04 outer front corners still 0.05 m |
| 94a9f36 | Rev C rebuild | Patch r2 fec275e: SEAM_AUDIT 15/24 fail (audit still on the pre-Rev C corner list) |
| 3825a40 | Rev C corner table (68) | Patch probe 363b349: 64/68, 4 no-hit at (±10.10, -1.00); QA-02 R2 (f8e6982) same 4 |
| f5f97d4 | SEAM_AUDIT reads JSON; corner colliders | de15497/f5f97d4: 27 then 5 fail |
| 3c13c42, c7fe8ec | end tips marked SKIP; end-tip colliders dropped | Patch r3 c7fe8ec: SEAM_AUDIT 305/5 fail at L2 h 4.5-7.0 |
| 0205e56, 873d9be | 20 mm chamfer in 62 concave corners; table uses SEAM_AUDIT method + full height | **Patch r4 9ecfdef (fresh import): SEAM_AUDIT 336/0, probe 336/0 — fixed** |
**Likely cause:** the audit corner list, the GLB and the runtime colliders were changed independently (old grid coordinates, convex tips counted as corners, rays landing exactly on triangle edge lines at round heights), so each fix moved the failure rather than removing it.

## M-23 (SYS-03 / INPUT-01) — hardcoded input keys (fixed 0ee29a3, see below)
| Commit | Attempt | Result at re-test |
|---|---|---|
| 2195f8a | INPUT-01 | Patch 1a349a3 marked INPUT-01 FIXED (movement uses input actions) |
| — | — | QA-05 (7b46c85, 29b6c1a): interact/RFID/toggles still hardcoded KEY_E/KEY_F/Tab; reopened as M-23. Still present at 9ecfdef (PPA :2674, :3589-3593) |
**Likely cause:** the fix covered movement only; the fix and the QA check both tested move_forward, not interact, so the partial fix was signed off as complete.

## M-63 (old NAV-01/02 nav-reach) — interactables unreachable on the navmesh (open, Low)
| Commit | Attempt | Result at re-test |
|---|---|---|
| d487417 | NavLink3D per door + --qa-nav-reach | 0/25 (interiors dropped from bake) |
| 7b21a19, cd3b12b | bake keeps interiors | 24/25, then 25/25; 19/19 through fec275e |
| ff057ff (M-41 decks removed, doors moved to Rev C) | — | **came back:** Patch r3 0/19; r4 9ecfdef 0/19 |
**Likely cause:** the navmesh and NavLinks are baked/placed from geometry and door coordinates that keep changing (Rev C grid, M-41), and nothing rebakes them, so every layout change silently breaks reachability. Downgraded to Low by Jared (only the player navigates).

## M-46 (NAV-04) — tram platform end point / deck trap (reopened 2026-11-02; fixed be4159e, see below)
| Commit | Attempt | Result at re-test |
|---|---|---|
| (none, ee61cb6..fec275e) | — | Patch 1a349a3: stops 1.08 m short of (12.8, -16.6); Patch r2 fec275e: 1.24 m short; QA-01 r2: stalls at (10.26, 0.33, -16.97) |
| f5f97d4 | "M-46 tram waypoint": egress final waypoint moved to (11.0, 0.30, -16.1) | Patch r3 c7fe8ec marked Fixed because --qa-egress passed |
| — | — | **Came back:** QA-01 sweep 5e3c137 NAV-04 trapped at (9.98-10.48, 0.33, -16.89..-17.00), escape 0/4; Patch real-input repro on the same code: trapped at (10.20, 0.33, -16.97), floor contacts only (ExtCollision, n +Y), escape 0/4 |
**Likely cause:** the fix changed the test, not the geometry. Moving the egress waypoint made --qa-egress pass while the platform floor shape (ExtCollision ExtShape_1, likely an edge/seam catch in the deck) still traps the capsule; QA accepted a suite pass instead of a free walk at the original spot. Fix the platform collider and re-test with a real-input walk and an escape check.

## M-46 - tram platform trap (repeat failure, fixed and verified 2026-11-03)
| Commit | Attempt | Result at re-test |
|---|---|---|
| (earlier) | egress waypoint moved to (11.0, -16.1) west of the shelter | QA-01: player still trapped, 2 of 4 exits, stops 1.10 m short |
| be4159e | ext trimesh colliders made two-sided (backface_collision) | Gage real-input probe: platform end (11.81, -16.74) 3/3 exits PASS, snag (7.62, -17.95) 3/3 exits PASS |
| — | — | **QA-01 re-test be4159e (2026-11-03): PASS** — NAV-04 escape 4/4 from both approaches, NAV-09 free, egress 23/23; still free at 248257d. **Fixed (verified).** Residual NAV-14 kerb snag -> M-85 |
**Likely cause:** one-sided ConcavePolygonShape3D trimeshes on exterior props (tram platform kerb/shelter, paving/curb seams). The capsule slid past a face edge and sat on floor contacts only with no way to depenetrate, so every direction read as blocked. Earlier fixes moved the test target instead of the collider.

## M-23 - E / F / Tab hardcoded keys (repeat failure, fixed and verified 2026-11-03)
| Commit | Attempt | Result at re-test |
|---|---|---|
| (earlier) | INPUT-01 moved WASD/Shift/Space to the InputMap | E, F, Tab/V still matched on physical_keycode in _input |
| 0ee29a3 | E/F/Tab/V go through `interact` / `rfid_pulse` / `toggle_view` actions (event.is_action_pressed); Tab added to `toggle_view`; held-F arm raise uses Input.is_action_pressed | Gage real key events: Tab PASS, V PASS, E opens DOOR_APT201 PASS; F dispatch not state-checked (no pulse state var); --qa-egress 0 failures |
| — | — | **QA-05 re-test 8a2a33f (2026-11-03): PASS** — E/F/Tab/V each fire once, F sets _rfid_pulse_timer, runtime remap E->K works, egress 23/23. **Fixed (verified).** Remaining physical-key reads split out as M-90 (SYS-16) / M-91 (SYS-17) |
**Likely cause:** the movement fix only covered polled movement actions; the one-shot keys lived in a separate physical_keycode match and were never migrated.

## Door lab M-98 / M-99 / M-104 / M-105 / M-106 — re-test 3 (Patch, 2026-11-21): M-98 / M-99 / M-105 failed a 3rd time (escalate to Jared); M-104 / M-106 closed
These were logged at pass A (a603953). They were re-tested at pass C (4694ea7), pass E (6f39e8b / merge da136c5) and pass F (41ce6cf / merge 1381acf, scored at 572c4c6). Patch ran its own 60/20/15 Hz runs with 50 cycles, plus xvfb shots, scored against QUALITY_BAR c86527f + acea568. M-114 (pair retime, cut tables) is HELD for Jared and is not counted here.

| Bug | 4694ea7 (pass C) | 6f39e8b (pass E) | 41ce6cf (pass F) |
|---|---|---|---|
| M-98 harness integrity | ids added, R3 1.1 a′dt; but R3 on commanded `leaf_vel`, F-TIME totals only, F-TRES-SRC on `.json` | R3 raw pose and F-TRES-SRC `.tres` fixed; F-TIME "per phase" (`_phases_within`) only checks that a sample exists in each window, which is always true, so it passed hatch final_seat 0.483 vs 0.30 s (M-117); R5 returns 0 by construction | **FAIL (3rd).** Fixed: per-tick phase labels gated against §7 windows, R2/R11 against §7, R5 measured from pose. Still: F-TRES-SRC PASS while the harness hard-codes parallel §7 phase/total/cue tables (the bar requires a FAIL), `_measured_phase_spans` samples the profile, F-LAMP-FADE is one synthetic pocket loop recorded for all 5 doors, and the shots summary writes PASS when metrics.json fails to parse |
| M-99 clip checks | colliders at 6 poses, bay3 concave query empty | concave warning gone, 22 poses; still colliders plus ~60-vertex sphere probes; no visible mesh-vs-mesh test, hardware meshes untested | **FAIL (3rd).** A triangle test exists, but hinge/knuckle/damper/seal/sweep/brush are excluded from hardware. Only leaf-borne meshes are walked, so leaf vs frame and frame hardware are never tested. ≤ 80 sampled triangles, 3 poses, edge-only hits fixed at 2.5 mm, coplanar still a depth test. Patch measured the excluded contacts at ≤ 4.0 mm, so the exclusion hides a metric bug. Pair rig knuckles are unmeasured (could reach ~40 mm) |
| M-104 pocket V-ZFIGHT-FLICKER | 0.01141 vs ≤ 0.00784 | 0.01494 vs ≤ 0.00784 (worse each pass: A 0.00894) | **Closed.** 0.00536 ≤ 0.00784, hot 0 (llvmpipe, two shot runs) |
| M-105 R6 / render artifacts | flat disc wheel; pair plates lemon yellow | wheel/linkage fixed; plates and bay3 bars still render (255, 251, 37) vs amber (0.85, 0.45, 0.02); hatch back cameras flat (σ 0) | **FAIL (3rd).** Hatch back face fixed. Pair plates render (255, 222, 9) and bay3 bars (255, 189–230, 6–18), gold-yellow ~52° hue vs amber ~32°, R clipped. V-PLATE checks material albedo, not pixels |
| M-106 lamp fade | `lamp_energy` constant 0.45 | energy now logged, but the fade is an exponential lerp(dt/0.15): 90% at 0.33 s, 99% at 0.65 s vs "over 0.15 s", fps-dependent; no harness check | **Closed.** smoothstep 0.15 s in telemetry at 60/20/15 Hz, 50% at 0.075 s |

**Likely cause:** each fix targeted the harness's own report, not the bar's measurement. Checks were added that can't fail (phase windows, profile-inverted stagger), or the visible output was never re-checked (shots, colours, fade curve). M-99 has asked for a mesh-vs-mesh test twice and got more collider sampling each time. In pass F, the triangle test's false positives at hinges and dampers were "fixed" by excluding those parts. M-105's colour fix checks the material, not the render. M-98's new tables were hard-coded into the harness, which is the thing F-TRES-SRC exists to catch. **Third-time fails (M-98, M-99, M-105) go to Jared.**

## Door lab M-112 — gates looser than QUALITY_BAR, failed re-test 2 of 2 (Patch, 2026-11-21)
| Commit | Attempt | Result at re-test |
|---|---|---|
| 6f39e8b (pass E) | F-TIME / V-LAMP-SYNC +dt reverted, F-OBS-DETECT 1 tick, V-GAP-PAIR ±0.05 removed, pocket bolt pose q 0.003 | partial: F-OBS-STOP snapped a stop time in (stop_s, stop_s + dt] onto stop_s; `_hatch_gap_mm` sampled one straight side |
| 41ce6cf (pass F) | snap removed; 4-edge bulkhead gap | **FAIL:** F-OBS-STOP now gates `t_stopped ≤ stop_s + dt` on the state-flag tick (pair 60 Hz 0.117 vs 0.10 s passes only on the +dt). Bulkhead inflated compression 8 mm is unmeasured but PASS. V-AUDIO allows dt + 1 ms. New pass F removals are in M-99 (clip exclusions/sampling) and M-98 (F-TRES-SRC) |

**Likely cause:** the hidden slack moved into the gate expression instead of being removed, and stop time is still taken from a state flag rather than measured (v ≈ 0). Either measure the v ≤ 2% tick and gate at stop_s, or ask for a bar change that grants ±1 tick (bar owner's call), not a silent +dt.
