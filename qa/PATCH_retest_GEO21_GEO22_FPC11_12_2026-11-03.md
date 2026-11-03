# Patch (QA) re-test: GEO-21, GEO-22, FPC-11/12 — 2026-11-03 (~15:30 CST)
Fresh clone of main at 6af315b (includes bb4da02 FPC-11/12, 0aec763 GEO-22, 6af315b GEO-21) in /tmp/patch_retest_6af315b.
Godot 4.7.2, gl_compatibility, headless under xvfb, `--headless --import` first. Probes were throwaway SceneTree scripts
(scene loaded with `-- --qa-placement` so headless does not drop to validate-only), measured at frame 60, deleted after the run.
Capsule r 0.35 h 1.75. Casts start >0.4 m back from faces.

| Item | Owner / commit | Result |
|---|---|---|
| GEO-21 one-sided concave colliders | Gage 6af315b | **PASS** — 0 of the original 45 |
| GEO-22 head strike under flight 1 | Rook 0aec763 | **PASS** |
| FPC-11 list cap / --verbose | Gage bb4da02 | **PASS** |
| FPC-12 walkable-slope min area + allowlist | Gage bb4da02 | **PASS** |

## GEO-21
- Runtime count at frame 60: **3,079 ConcavePolygonShape3D, 4 with backface_collision=false.** Gage counted 3,078 / 3; the extra one is Rook's new closure.
- Of the original 45 (39 GEO-17 clipped curb/paving, 3 plaza `_ext_add_ground_colliders`, 3 RevC shell L1/L2/roof): **0 remain one-sided.** Log line `[EXT] ground_colliders=4`; `[GEO-17] ext shapes clipped at shell z -8.90: 51`.
- The 4 one-sided shapes left are all stair colonly shapes under StairSetSwitchback:
  - Flight1_Ramp-colonly AABB x -1.9..-0.4, y -0.17..2.58, z -7.50..-2.92
  - Flight2_Ramp-colonly AABB x 0.4..1.9, y 2.41..4.20, z -7.68..-4.78
  - L2_Landing-colonly AABB x -1.9..1.9, y 3.9..4.2, z -4.88..-0.80
  - Flight1_Understair_Closure-colonly (new, 0aec763) AABB x -1.9..-0.4, y 0..2.33, z -7.40..-3.32
- Are they a problem? **Not from outside, as tested.** They are closed prisms with outward faces:
  - A capsule rising from the L1 floor (center y 1.04) under Flight2 stops 0.79 / 1.22 / 1.63 m up at t 0.25 / 0.50 / 0.75. That puts the capsule top on the ramp underside, y 2.77 / 3.19 / 3.61.
  - Under L2_Landing it stops 1.98 m up, so the top is at the y 3.90 underside, 3 of 3 points.
  - Front-face-only rays (hit_back_faces=false) from y 1.10 hit Flight2 and L2 from below, 6 of 6.
  - Under Flight1 the space is now filled by the closure, so a capsule can't get there from outside.
  - Caveat: a capsule that starts **inside** the Flight1 ramp/closure volume rises freely: 4.0 m, 2.2 m, 2.0 m with no hit, because one-sided faces don't push it out. That only happens if something spawns or tunnels into the volume.
  - Recommendation (Low, not filed as a bug): set backface_collision=true on these 4 for consistency with GEO-21.
  - Note: `first_pass_check.py` godot.trimesh_two_sided reports 0 because its scope is exterior/thin-shell, so stairs are excluded.

## GEO-22
- Flight1_Understair_Closure-colonly is present: x -1.9..-0.4, y 0..2.335, z -7.40..-3.32.
- Inbound capsule from the north (z -9.0, under the mid landing, center y 1.035) heading +z:
  - x -1.55: stops at z -7.797 against the closure's vertical face at z -7.40, n (0,0,-1).
  - x -1.15: same stop and same face.
  - Neither lane hits the ramp underside.
  - x -0.75: stopped at z -8.93 by the Sector-4 exit FieldCollider (the closed portal field). The start point was inside the portal; this isn't a stair finding.
- From the south (z -1.92) heading -z, all 3 lanes meet Flight1_Ramp at the foot with n (0,0.87,0.50), the up-slope walk face. That is the normal stair entry, not a head strike.
- A capsule standing at x -1.15, z -6.48 would overlap the stair volume. The pocket where the y 1.82 head strike happened is now solid, so the spot can't be reached.
- Stairs walked with a CharacterBody3D capsule (floor_max_angle 50°, snap 0.4, 3 m/s) on 3 lanes per direction:
  - **Up: 3/3 pass.** L1 to mid landing (center y 3.46) to L2 (center y 5.08).
  - **Down: 3/3 pass.** L2 to mid landing to L1 (center y 0.995).
- `--qa-egress`: **23/23 waypoints PASS, `DONE failures=0`**, exit 0.

## FPC-11 / FPC-12 (`tools/first_pass_check.py`)
- Default run on preface_playable_area.tscn: exit 0 (101 lines). Lists are capped at 8 with a "... and N more (use --verbose for all)" line, 4 times:
  - status_clean: 18 = 8 + 10
  - missing_import_uid: 16 = 8 + 8
  - 2 more lists
- `--verbose`: exit 0, 284 lines, no truncation lines.
- Godot-pass lists go through the same limit (code comment at line 720). No Godot list in this scene had more than 8 items, so the Godot-side cap was confirmed in code only.
- FPC-12: `godot.walkable_slope` PASS, 0 colliders at 45–70°, min area 0.25 m2, 1 allowlisted (ThresholdChevrons). `godot.stair_slope` PASS, 0 steeper than 35°.
- Docs: docs/FIRST_PASS_CHECKLIST.md line 12 documents `--verbose`.
- Exit codes:
  - clean: 0
  - `--strict` (WARN treated as fail): 1
  - bad path: 2
  - a .md path with `--no-godot`: 0
- Side note: the checker's repo.status_clean / missing_import_uid WARNs show that `--import` on a fresh clone leaves 15 untracked texture .import files and 1 .gd.uid. These were not committed.

## Bugs
No new bugs and no second failures, so qa/REPEAT_FAILURES.md is unchanged.
Low observation for Gage/Rook: 4 one-sided stair colonly shapes (see GEO-21).
