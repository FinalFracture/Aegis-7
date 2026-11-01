# QA-04 r2: Layout & Prop Compliance (2026-11-01, 08:45 CST)
Fresh clone of `main` @ 27a8e35. Report only; no game files edited. r1 was run on 39eba42 (r1 log commit b5b551a).
Spec docs re-read: `residential_roomlayout_rev_c.py`, `residential_apartment_layout_v2.md`, `residential_asset_list_rev_c.md`, `strip4_plan.md`, `cylinder_master_plan.md`, `strip4_preface_layout_v1.md` (now Rev 1.1), `prop43_relocation.md`.
Since r1, the only spec doc that changed is `strip4_preface_layout_v1.md`. Rev 1.1 adds the 180° building rotation and moves the memorial; the cubbies now wait for the rebuild; the interior table is unchanged. The asset list, apartment layout v2 and the room-layout `.py` are unchanged.
What changed in the build: the sector GLB is rebuilt to the Rev C grid (94a9f36). `preface_playable_area.gd` now has `REV_C_STATIC_PROP_SPECS` (13 static props) and the updated `ANIMATED_PROP_SPECS`. Per the code comments the frame is XZ identity with Rev C, L1 y=0.12 and L2 y=4.2.
Tolerance: ±0.10 m to the spec rect centre; yaw puts the back against the stated wall.
Headless Godot probe (outside the repo): all baked clips are present. Leaf_Fold_Up/Down, Seat_Flip_Down/Up, Cell_Swap + Port_Ready_Blink and Capsule_Drop + Pick_Ready_Blink are wired (toggle, or action + queued idle). service_wall_rail_shuttle (4 clips) and sprocket_lift (9 clips) are not wired.

## Requested checks
| Check | Spec says | Code | Verdict |
|---|---|---|---|
| (a) Prop43 on the 101 east wall | `prop43_relocation.md` Rev 3: "1A East Lounge" east wall, (-5.16, 5.20) yaw -90. The asset list (#43) still says Maintenance, and no doc says "101" | (-4.858, 0.12, 5.20), yaw -90, comment "Room 101 east wall", back against the x=-4.6 face | **Code is on the 101 east wall, matching the Rev 3 intent. The docs haven't been updated to say 101 (LAY-01).** It collides with the 101 wardrobe (LAY-14) |
| (b) #14 and #55 in Maintenance, not Laundry | Asset list: #14 in 102/203; #55 on the Laundry N wall X -4.3..-3.0. Preface table: "1B West Storage" (1B = Maintenance in Rev C) | Tea set (1.50, 7.89) and bins (1.08, 5.35) are both inside Maintenance (X 0.5..6) | **Code: yes, both are in Maintenance. Spec: the Rev C asset list doesn't match (LAY-15).** The bins overlap the Maintenance tool wall (LAY-16) |
| (c) 104/204 lamps with no desk | Asset list #27: "on the 104 and 204 window desks"; #28 window desk active for 104/204 | Lamps at (5.0, -8.7) on the desk-top plane (y 0.985 / 5.165); "desk GLBs are not placed" | **Code: correct, no desk. Spec: doesn't match, because the spec requires the desk.** The lamps float 0.75 m in the air (LAY-17) |
| (d) 3.5 m folding counter removed from the spec and absent | Asset list #38 still says qty 2 incl. `fold_leaf_3p5`; `.py` L1 still has `folding counter` X -0.2..0.4, Z 3..6.5 | Not placed | **Doesn't match. It's absent from the code but still in the spec (LAY-08 open).** One side needs to change |

## Recheck of LAY-01..13
| ID | Sev (r2) | Status | Note |
|---|---|---|---|
| LAY-01 | Low | Code fixed, docs stale | Prop43 moved to the 101 east wall (yaw -90). `prop43_relocation.md` and the strip4 table still say "1A East Lounge (-5.16)" and "Not applied yet"; asset list #43 still says Maintenance |
| LAY-02 | — | **Closed** | Interim props #5–#12 are now placed. #13 cubbies deferred by Rev 1.1 |
| LAY-03 | High | Open | `sprocket_lift.glb` not placed or wired (shaft X 0.6..2.2, Z 0.8..2.4) |
| LAY-04 | High | Open | `service_wall_rail_shuttle.glb` (tool wall + pads + arms; 101, 201, Maint) not placed; clips not wired |
| LAY-05 | High (was Med) | Open, worse | Prop42 substation is still at (10.68, 8.492), yaw 180. On the Rev C grid that's inside **apartment 102** (X 6..14), not Maintenance E wall X 5.3..5.9, Z 1..3.5 |
| LAY-06 | Medium | Open | Prop39 at (-3.77, 8.692), footprint ~-4.37..-3.17: on the N wall in the #55 slot. Spec bench is X -3.5..-2.3, Z 6.6..7.0 |
| LAY-07 | Medium | Open | Prop38 at x -1.64, span ~-3.14..-0.14. The spec is X -2.6..0.4 (centre -1.10), so Δx is 0.54. With the frame now at identity, the old "doc - 0.75" offset no longer applies |
| LAY-08 | Medium | Open | See (d) |
| LAY-09 | Low (was Med) | Deferred/accepted | Reading bench cubbies wait for the Rev C rebuild (strip4 Rev 1.1) |
| LAY-10 | Medium | Open, reduced | Still not placed: bath pods, kitchens, tables, chairs, sofas, beds, bunks, wardrobes, closets, toy chest, window desks, W/D ×4, stair set/guards/skylight, riser, sprocket lift, service wall, armchairs in 102/203/204. Only the 201 armchair is placed |
| LAY-11 | Low | Open | Window cards #6 and removal decals #54 still not modeled |
| LAY-12 | Low | Open | Excluded items are still absent (PASS). `Hatch_D204_EmitterPanel` is still spawned; confirm it isn't standing in for #31 |
| LAY-13 | Low | Not verified | R=200 vs the authored 185.5 bend parameter is not confirmed in code |

## New findings
| ID | Sev | Spec ref | Expected | Actual | File |
|---|---|---|---|---|---|
| LAY-14 | High | `.py` L1 101 `wardrobe` F(-5.1,4,-4.6,7) | Clear of fixed furniture | Prop43 footprint ~x -5.11..-4.61, z 4.25..6.15 sits inside the 101 wardrobe rect (same wall, same z) | godot/scripts/preface_playable_area.gd:1854 |
| LAY-15 | Medium | Asset list #14 (102, 203), #55 (Laundry N wall) | Tea sets in 102 and 203 (qty 2); bins on the Laundry N wall | One tea set in Maintenance at (1.50, 7.89); bins in Maintenance at (1.08, 5.35). The asset list wasn't updated to match | preface_playable_area.gd:1888, :1909 |
| LAY-16 | High | `.py` L1 Maintenance `tool wall` F(0.6,3.6,1.1,6.4) | Clear | #55 bins footprint 0.93..1.23 × 4.70..6.00 overlaps the tool wall rect. The tea caddy (z 7.79..7.99) touches pad X 0.8..2.0, Z 6.6..7.8 by 0.01 m | preface_playable_area.gd:1909 |
| LAY-17 | High | Asset list #27, #28 | Lamp on a window desk (desk 3..7 × -8.9..-8.5) | Lamps hang at desk height with no desk mesh in 104 and 204 | preface_playable_area.gd:1938, :1945 |
| LAY-18 | Medium | `.py` L1 102 `suit hook + storage` F(6.1,5,6.6,7.5), centre (6.35, 6.25) | Within ±0.10 | (7.82, 4.85): Δ≈2.0 m (interim table position kept after the Rev C rebuild) | preface_playable_area.gd:1895 |
| LAY-19 | Medium | `.py` L2 202 `sofa` F(5,5.5,7.5,6.4); asset list #36 rooms 101/102/104/202 | Clear; kit in 4 rooms | Clutter kit footprint 5.57..5.81 × 4.545..5.755 overlaps the 202 sofa rect; it's placed in 202 only | preface_playable_area.gd:1902 |

## Counts (open)
Critical 0 · High 6 (LAY-03, 04, 05, 14, 16, 17) · Medium 7 (LAY-06, 07, 08, 10, 15, 18, 19) · Low 5 (LAY-01, 09, 11, 12, 13) · Closed 1 (LAY-02). 18 open.
