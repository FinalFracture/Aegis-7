# QA-04 r3: Layout & Prop Compliance regression (2026-11-02, 08:27 CST)
Fresh clone of `main` @ ee10b2b (contains ee10b2b). Spec: Rev C.3 (6c6c4f6) plus later doc commits c6f22b2/2541a7b/4e9849a; Prop43 lock 0b4aa94. Report only; no game files edited.
Method: a headless Godot 4.7 runtime probe (script outside the repo) ran `preface_playable_area.tscn` with `--qa-placement`. For every placed prop it read the world pose and mesh AABB, ray-cast down from the AABB bottom for floor contact (prop's own colliders excluded), and checked AABB overlaps between props (threshold 0.01 m). Tolerance: ±0.10 m to the spec rect centre; floor contact limit 0.005 m. Skipped: M-70 stairs and unbuilt Rev C scope.

## Probe results (all 19 placed props)
| Prop | Pos | Yaw | AABB x / y / z | Support gap | Verdict |
|---|---|---|---|---|---|
| Prop38_FoldingCounter | (-1.64, 0.12, 8.592) | 180 | -3.140..-0.140 / 0.120..1.020 / 8.442..8.892 | 0.000 | on floor; Δx 0.54 vs .py (LAY-07) |
| Prop39_FlipSeat | (-3.77, 0.12, 8.692) | 180 | -4.370..-3.170 / 0.120..0.920 / 8.492..8.892 | 0.000 | on floor; not at .py bench rect (LAY-06) |
| Prop42_Substation | (5.492, 0.12, 2.40) | -90 | 5.092..5.892 / 0.120..2.320 / 1.150..3.650 | 0.000 | Maintenance E wall, back to +x ✔; Δz 0.15 (LAY-20) |
| Prop43_SparesDispenser | (-4.858, 0.12, 5.20) | -90 | -5.108..-4.608 / 0.120..1.920 / 4.250..6.150 | 0.000 | **matches lock 0b4aa94** ✔ |
| Cycler_Route_Lightbox | (-10.75, 4.2, -8.8) | 0 | -11.20..-10.30 / 4.20..5.20 / -8.92..-8.80 | 0.000 | ✔ |
| Telescope_Pier_Dobsonian | (9.2, 0.12, -8.6) | 180 | 8.94..9.46 / 0.12..1.55 / -8.94..-8.34 | 0.000 | ✔ |
| Tea_Set_Rail_Caddy | (1.50, 0.12, 7.89) | 180 | 1.31..1.69 / 0.12..0.32 / 7.785..7.995 | 0.000 | ✔ (Maintenance per spec) |
| Suit_Storage_Service_Combo | (7.82, 0.12, 4.85) | -90 | 7.57..8.07 / 0.12..2.22 / 3.60..6.10 | 0.000 | Δ≈2.0 m from .py (LAY-18) |
| Clutter_Kit_Magnet_Dock | (5.69, 4.2, 5.025) | 90 | 5.57..5.81 / 4.20..4.41 / 4.545..5.755 | 0.000 | on floor (LAY-19) |
| Lost_And_Found_Rail_Bins | (1.40, 0.12, 5.35) | 90 | 1.248..1.548 / **0.510**..1.520 / 4.70..6.00 | **0.390** | **floating** (LAY-21 / M-64) |
| Lab_Crate_Frame_104 | (7.9, 0.12, -8.6) | 0 | 7.40..8.40 / 0.12..0.62 / -8.89..-8.29 | 0.000 | ✔ |
| Lab_Crate_Frame_204 | (10.75, 4.2, -8.55) | 0 | 10.30..11.20 / 4.20..5.00 / -8.90..-8.19 | 0.000 | ✔ |
| Task_Lamp_201 | (-13.2, 4.45, 5.6) | 180 | -13.255..-13.145 / **4.415**..4.890 / 5.338..5.634 | **0.215** | **floating** (LAY-22 / M-65) |
| Task_Lamp_104 | (5.0, 0.155, -8.7) | 0 | 4.945..5.055 / 0.120..0.595 / -8.734..-8.438 | 0.000 | on floor (no longer floating); doc says desk-top height (LAY-25) |
| Task_Lamp_204 | (5.0, 4.235, -8.7) | 0 | 4.945..5.055 / 4.200..4.675 / -8.734..-8.438 | 0.000 | same as 104 |
| Armchair_Reading_201 | (-12.9, 4.2, 4.7) | -90 | -13.35..-12.42 / 4.20..5.15 / 4.22..5.18 | 0.000 | ✔ |
| Potted_Plants_Rail_Cradles_102 | (10.65, 0.12, 6.35) | 0 | 10.05..11.25 / **0.320**..0.873 / 6.226..6.474 | **0.200** | **floating, mid-room, no rail/wall** (LAY-24) |
| Potted_Plants_Pocket_Column_203 | (-9.2, 4.2, -8.6) | 0 | -9.648..-8.752 / 4.20..4.98 / -8.80..-8.40 | 0.000 | ✔ |
| Wardrobe_101 | (-13.65, 0.12, 5.75) | 90 | -13.900..-13.412 / **0.220**..2.220 / 4.40..7.10 | **0.100** | west wall ✔ (C.3), but floating (LAY-23 / M-66) |
Prop-vs-prop AABB overlaps: **0**. The baked clips (Leaf_Fold, Seat_Flip, Cell_Swap, Capsule_Drop) are unchanged and wired (r1/r2).

## Specific checks
- **Prop43:** (-4.858, 0.12, 5.20), yaw -90, back face x -4.608 against x_wall -4.600 (8 mm gap). This matches the lock. The front zone to x -6.32 is clear, and the 101 wardrobe is on the west wall (x -13.9..-13.41). PASS.
- **Prop42 / M-44:** now on the Maintenance E wall with its back to +x. PASS, except for small residuals (LAY-20).
- **#55 bins / M-64:** still floating 0.39 m above the floor, with the back 0.648 m off the W wall (x 0.6). FAIL.
- **201 lamp / M-65:** floating 0.215 m with no support under it. FAIL. **101 wardrobe / M-66:** 0.100 m above the floor. FAIL.
- **104/204 lamps:** sit on the floor (gap 0.000). They don't float any more, but the asset list #28 text still says "desk-top height".

## LAY status
| ID | Sev | Status | One-liner |
|---|---|---|---|
| LAY-01 | — | **Closed** | Prop43 docs updated and the position locked (0b4aa94); the code matches |
| LAY-02 | — | Closed (r2) | Interim props placed |
| LAY-03 | — | Deferred (unbuilt Rev C scope, skipped) | Sprocket lift not placed/wired |
| LAY-04 | — | Deferred (unbuilt Rev C scope, skipped) | Service wall not placed/wired |
| LAY-05 | — | **Closed** | Prop42 now on the Maintenance E wall (M-44); residual → LAY-20 |
| LAY-06 | Medium | Open | Prop39 flip seat on the Laundry N wall (-4.37..-3.17 × 8.49..8.89); .py bench rect is X -3.5..-2.3, Z 6.6..7.0 |
| LAY-07 | Medium | Open | Prop38 x span -3.14..-0.14 vs .py "folding counter 3.0" X -2.6..0.4 (Δx 0.54) |
| LAY-08 | — | **Closed** | 3.5 m counter removed from spec (c6f22b2) and absent from code |
| LAY-09 | — | Deferred | Reading-bench cubbies wait for the Rev C rebuild (strip4 Rev 1.1) |
| LAY-10 | — | Deferred (unbuilt Rev C scope, skipped) | Remaining Rev C furniture not placed |
| LAY-11 | Low | Open | Window cards and #54 decal textures now exist (f7651a2), but nothing references them in `preface_playable_area.gd` (not applied) |
| LAY-12 | — | **Closed** | `Hatch_D204_EmitterPanel` is no longer spawned (dead lookups remain at lines 547 and 8021) |
| LAY-13 | — | **Closed** | No R 185.5 reference left in scripts |
| LAY-14 | — | **Closed** | 101 wardrobe moved to the W wall (C.3); no overlap with Prop43 |
| LAY-15 | — | **Closed** | Spec now puts #14 and #55 in Maintenance (c6f22b2) |
| LAY-16 | — | **Closed** | #55 bins clear of the tool wall rect (x ≥ 1.248) |
| LAY-17 | — | **Closed** | #28 desks dropped from spec; lamps rest on the floor |
| LAY-18 | Medium | Open | Suit storage (7.82, 4.85) vs .py 102 rect centre (6.35, 6.25), Δ≈2.0 m |
| LAY-19 | Low (was Med) | Open | 202 clutter kit footprint overlaps the unbuilt 202 sofa rect F(5,5.5,7.5,6.4); a future collision at the rebuild |

## New findings
| ID | Sev | Spec / bug ref | Expected | Actual | File |
|---|---|---|---|---|---|
| LAY-20 | Low | .py `sub-station` F(5.3,1,5.9,3.5); asset #42 0.6 deep | centre (5.6, 2.25), 0.6 deep | AABB 5.092..5.892 × 1.15..3.65 (0.8 deep, centre z 2.40, Δz 0.15) | preface_playable_area.gd:2223 |
| LAY-21 | Medium | M-64; .py `lost+found` F(0.93,4.7,1.23,6.0); asset #55 doc says code x 1.08 | wall-mounted rail bins against the W wall (x 0.6), or floor-supported | at x 1.40, mesh bottom y 0.51 (0.39 m air gap), back 0.648 m from the wall, no rail; Δx 0.32 vs the .py rect | preface_playable_area.gd:2293 |
| LAY-22 | Low | M-65; .py `lamp` F(-13.4,5.4,-13.0,5.8) | rests on the L2 floor or a support | bottom y 4.415, 0.215 m above the floor (XZ ✔) | preface_playable_area.gd:2315 |
| LAY-23 | Low | M-66; C.3 wardrobe x -13.9..-13.4, z 4.5..7.0 | on the floor (≤0.005) | bottom y 0.220 (0.100 m gap); z extent 4.40..7.10 (mesh 2.7 m vs the 2.5 m rect; still 0.20 m from the bed) | preface_playable_area.gd:2361 |
| LAY-24 | Medium | .py 102 `plants` F(10.3,6,11,6.7); asset #34 "wall rail" | on a rail/wall or the floor, within the rect | mesh bottom y 0.32 (0.20 m air gap), free-standing mid-room with no wall behind (back z 6.474); 1.2 m wide vs the 0.7 m rect | preface_playable_area.gd:2344 |
| LAY-25 | Low | asset list #28 and #55 text | docs match code | #28 says the lamps are "at desk-top height" (code: on the floor, y 0.155); #55 says code x 1.08 (code: 1.40) | design/residential_asset_list_rev_c.md |

## Counts (open)
Critical 0 · High 0 · Medium 5 (LAY-06, 07, 18, 21, 24) · Low 6 (LAY-11, 19, 20, 22, 23, 25) · Deferred/skipped 4 (LAY-03, 04, 09, 10) · Closed 10 (LAY-01, 02, 05, 08, 12, 13, 14, 15, 16, 17).
