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

## M-23 (SYS-03 / INPUT-01) — hardcoded input keys (open)
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
