# QA-02 Handoff v1 — Geometry & Collision Tester (Cylinder Hab-7)

Predecessor: QA-02, id 483886ab-b7b2-4913-953d-1bfb2e9b987a (to be renamed `delete-QA-02`).
Successor: QA-02, id a0b988cc-9e1d-48ad-bc0a-4f46fa3547e0.
Written by Scribe, Sun 2026-11-01 ~9:49 AM CT. Transcript snapshot (all 51 positions): `context/transcripts/483886ab-b7b2-4913-953d-1bfb2e9b987a_platest.txt`.
Repo state checked: origin/main @ c6f22b2. The shared `/workspace/game-project` checkout has uncommitted edits to `context/STATUS.md` and `context/roster.json` and was behind origin/main.

## 1. Predecessor Purpose & Mandatory Reference Files Manifest

**Exact purpose** (roster.json `purpose` for QA-02): "Cylinder Hab-7 tester, focus: Geometry & collision".
Role (roster.json): QA Tester. Atlas handoff v6 lists it as "QA-02 geometry/collision".
What the predecessor did with that purpose (its first message, 4:55 AM CT): audit Hab-7 geometry and collision on a fresh clone of main, covering every wall corner, seam, prop placement and collider, and send GEO-xx bug reports to Atlas and Patch.
Note: the predecessor's full profile description is not in the transcript (the teammate list there was truncated), so the line above is the only verbatim purpose text found.

**Mandatory reference files.** Each path was checked on origin/main at c6f22b2. The predecessor was given no explicit reading list. These are the files it actually used or produced, plus the files that define its pending Round 2 scope.
| # | File | Status | Why |
|---|---|---|---|
| 1 | `context/qa02-handoff.md` (this file) | OK | Start here |
| 2 | `qa/QA-02_geometry_audit_2026-11-01.md` | OK | QA-02's own log: Round 1 (cd17628) + GEO-10 (00914fd) |
| 3 | `qa/MASTER_BUG_LIST.md` | OK | Patch's deduped list, with current GEO status (M-xx ids) |
| 4 | `context/playtest_bug_report.md` | OK | SEAM-01..04 history; SEAM_AUDIT 15 pass / 24 fail details |
| 5 | `design/rev_c_shell_corners.json` | OK | Rook's Rev C corner table (3825a40: 68 corners) |
| 6 | `design/prop43_relocation.md` | OK | Prop43 intended position (GEO-10 / M-02) |
| 7 | `godot/scenes/preface/preface_playable_area.tscn` | OK | Main scene audited (`res://scenes/preface/preface_playable_area.tscn`, run with `--qa-placement`) |
| 8 | `godot/tools/placement_assert.gd` | OK | SEAM_AUDIT (SEAM_CORNERS const). Read only, never edit |
| 9 | `context/atlas-handoff-v6.md` | OK | Team rules, QA roster, "Rev C GLB fails 24 seam checks (Rook)" |
| 10 | `context/roster.json` | OK | Team ids |
| 11 | Skill `3d-part-clipping-check` | OK (skill) | Thresholds: floor ±0.005 m, wall back gap 0–0.015 m, overlap ≤0.010 m |

## 2. Round 1 Results (commit cd17628)
- Audited origin/main @ 39eba42, headless Godot 4.7.2, with scripts kept in /tmp outside the repo. Scanned 3,790 MeshInstance3D and 3,266 CollisionShape3D nodes.
- 9 bugs: 0 Critical, 1 High, 5 Medium, 3 Low. Usage was 87.5% at the start and 88.1% at commit. The push was rebased after QA-03/QA-04 pushes (no force-push).
- Not covered: walk-through wall gaps (needs a capsule sweep; point queries can't read concave trimesh) and the merged CylinderHab7 drum (the AABB coplanar test gives false positives there).

## 3. Findings GEO-01 – GEO-10 (status from MASTER_BUG_LIST on origin/main)
| ID | Sev | Summary | Master | Status |
|---|---|---|---|---|
| GEO-01 | High | Props 38/39/42/43 have no collider; you can walk through them | M-01 | Fixed (04bbed0 AABB colliders; r2 capsule sweep blocks) |
| GEO-02 | Med | 7 pickups sunk 0.07–0.095 m into shelves/desks | M-08 | Open |
| GEO-03 | Med | Apt 201 spool + BCI headband float 0.675 m past the shelf edge | M-09 | Open |
| GEO-04 | Med | Ext_47 desire-path decals 1002/1003 z-fight (~2.0,0.18,-12.1) | M-10 | Open |
| GEO-05 | Med | SeamFix boxes coplanar with East Lounge/West Storage shells | M-20 | Fixed (verified, 363b349) |
| GEO-06 | Med | DockPad InductionRing/Chevrons coplanar at 6 hubs | M-21 | Fixed (verified, 363b349) |
| GEO-07 | Low | TalkPad/IntercomRing coplanar on 4 hubs | M-39 | Fixed (verified, 363b349) |
| GEO-08 | Low | Open_Portal_Sector_Exit coplanar with vestibule (z -8.76) | M-40 | Fixed (verified, 363b349) |
| GEO-09 | Low | Navmesh "8 edge errors" at load | M-24 | Open |
| GEO-10 | Med (→Gage) | Prop43 at ~(-8.0,0.235,8.5); intended (-5.16,0.235,5.20) yaw -90 (Vance via Atlas). Logged 00914fd | M-02 | Open. Patch's r2 probe shows runtime (-4.858,0.12,5.20) yaw -90, so GEO-10's position predates 04bbed0. Gage + Vance to pick one spot |
- Context: 11e51da ("Prop43 rev3: East Lounge east wall") was already in the 39eba42 build QA-02 audited, yet Prop43 sat at the old spot in that build.

## 4. Pending Round 2 Scope (never started)
At 8:44 AM CT Round 2 stopped before any work (usage 92.1%), and the repo was untouched. The scope, as briefed:
1. Re-verify GEO-01 – GEO-09 (now cross-check against the MASTER statuses above).
2. Rook's 24 Rev C GLB seam failures (§5).
3. All wall corner seams, including a capsule sweep along the wall lines for walk-through gaps.
4. Prop43 clipping and collision at (-5.16, 0.235, 5.20) yaw -90; also log both the found and intended positions.
- Log to `qa/QA-02_geometry_audit_round2_2026-11-01.md` and hand the results to Patch (priority). New bugs start at **GEO-11** (GEO-10 is taken).

## 5. The 24 Rev C Seam Checks (M-45; SEAM_AUDIT 15 pass / 24 fail on fec275e)
- 15 fails at L2 corners (-12.74,-5.69), (±5.35, 2.65), (±5.35, 8.55) at y 5.12 / 5.92 / 6.72: no hit at all (no wall where the audit expects one).
- 9 fails at L1 corners: (-4.75,7.98) and (0.75,8.16) leak 0.21 m through RevC_Shell_L1_col; (8.25,8.16) gets no hit.
- Cause: the SEAM_AUDIT corner table is the pre-Rev C grid. Rook's `design/rev_c_shell_corners.json` (68 corners, 0 fail in the GLB) can't be loaded without a code edit (Gage owns that). Patch's /tmp probe against runtime colliders: 64/68 pass, 4 fail (M-61). Status: Open.

## 6. Standing Rules
- Report only: never edit game code or assets (.gd/.tscn/.py/GLB). Text logs only under `qa/`; no renders/images committed; scripts run from /tmp.
- Work on a fresh main: fetch, and reset only if the tree is clean; otherwise use a temp checkout of origin/main. Commit directly to main, no branches, rebase on rejection, never force-push.
- Report GEO-xx findings to Atlas and Patch. Patch dedupes into MASTER_BUG_LIST and routes to owners.
- Usage (Jared, 11-01, relayed by Atlas): the weekly cap is 93% Monday through Sunday 8:30 AM CT. After the Sunday 8:30 AM CT routines finish, work may continue up to 100% until the Monday reset (Mon 11-02 5:28 AM CT). Jared at 9:42 AM CT: "Let all agents know that we can go up to 100% usage." Check CheckSubscriptionUsage before and during work.
- Approval: Round 2 is waiting on a go-ahead. Approval comes from Jared himself; Atlas assigns and coordinates the QA work.
- Destructive actions still need Jared's own words.

## 7. QA Team IDs
- QA-01 (nav/egress): 2545742b-97c1-463e-9e12-f54f21ef9e47
- QA-02 (geometry/collision): a0b988cc-9e1d-48ad-bc0a-4f46fa3547e0 (predecessor 483886ab-b7b2-4913-953d-1bfb2e9b987a)
- QA-03 (lighting/visuals): 58a63754-66ba-462b-ada0-e8c727d3d5a9
- QA-04 (layout/prop compliance): 38716c8a-2c0d-456b-9250-982d36ace0b5
- QA-05 (stability/perf/input): 5e75ca97-87eb-481b-b8e3-886a92426582
- Atlas: 038035ec-9495-437e-984d-0493ca58383b · Patch: ecd78f3d-be8f-43e4-b543-0c912d6d00ea
